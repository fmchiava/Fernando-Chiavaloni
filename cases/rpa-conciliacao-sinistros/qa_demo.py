"""Cliente de demonstração: lê a fila web, consulta API e gera evidências."""

import argparse
import csv
import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
TRANSIENT_CODES = {429, 500, 502, 503, 504}


class SystemFailure(Exception):
    pass


class DecisionUnverified(SystemFailure):
    def __init__(self, reason_code, request_id):
        super().__init__(reason_code)
        self.request_id = request_id


class ClaimParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.claims = []

    def handle_starttag(self, tag, attrs):
        if tag != "tr":
            return
        data = dict(attrs)
        if "data-claim-id" in data:
            if not {"data-policy-id", "data-amount-cents", "data-status"}.issubset(data):
                raise SystemFailure("UI_CONTRACT_CHANGED")
            try:
                amount_cents = int(data["data-amount-cents"])
            except ValueError as error:
                raise SystemFailure("UI_AMOUNT_INVALID") from error
            self.claims.append({
                "claim_id": data["data-claim-id"],
                "policy_id": data["data-policy-id"],
                "amount_cents": amount_cents,
                "status": data["data-status"],
            })


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_ledger(path):
    ledger = {}
    try:
        with Path(path).open(newline="", encoding="utf-8") as source:
            rows = csv.DictReader(source)
            if rows.fieldnames != ["claim_id", "paid_cents"]:
                raise ValueError("Cabeçalho do arquivo de pagamentos deve ser claim_id,paid_cents")
            for row in rows:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Linha truncada ou com colunas extras no arquivo de pagamentos")
                claim_id = row["claim_id"]
                paid = int(row["paid_cents"])
                if not claim_id or claim_id in ledger or paid < 0:
                    raise ValueError("Arquivo de pagamentos duplicado ou inválido")
                ledger[claim_id] = paid
    except OSError as error:
        raise SystemFailure("LEDGER_FILE_UNAVAILABLE") from error
    return ledger


def fetch_queue(base_url):
    with urlopen(base_url + "/claims", timeout=3) as response:
        page = response.read().decode("utf-8")
    parser = ClaimParser()
    parser.feed(page)
    if not parser.claims:
        raise SystemFailure("UI_QUEUE_EMPTY_OR_CHANGED")
    return parser.claims


def fetch_coverage(base_url, policy_id, max_attempts, log, claim_id, correlation_id):
    for attempt in range(1, max_attempts + 1):
        start = time.monotonic()
        try:
            with urlopen(base_url + "/api/coverage/" + policy_id, timeout=3) as response:
                payload = json.load(response)
            if (not isinstance(payload, dict) or payload.get("policy_id") != policy_id
                    or not isinstance(payload.get("active"), bool)
                    or type(payload.get("limit_cents")) is not int
                    or payload["limit_cents"] < 0):
                raise SystemFailure("COVERAGE_CONTRACT_INVALID")
            log("api_coverage", claim_id, correlation_id, "OK", attempt=attempt,
                duration_ms=round((time.monotonic() - start) * 1000))
            return payload
        except HTTPError as error:
            code = error.code
            error.close()
            if code == 404:
                log("api_coverage", claim_id, correlation_id, "BUSINESS_EXCEPTION",
                    reason_code="POLICY_NOT_FOUND", attempt=attempt, http_status=code)
                return None
            if code not in TRANSIENT_CODES or attempt == max_attempts:
                raise SystemFailure(f"COVERAGE_HTTP_{code}") from error
            log("api_retry", claim_id, correlation_id, "RETRY", attempt=attempt, http_status=code)
        except (URLError, TimeoutError) as error:
            if attempt == max_attempts:
                raise SystemFailure("COVERAGE_TIMEOUT_OR_NETWORK") from error
            log("api_retry", claim_id, correlation_id, "RETRY", attempt=attempt, reason_code="NETWORK")
        time.sleep(0.05 * 2 ** (attempt - 1))
    raise SystemFailure("COVERAGE_UNAVAILABLE")


def decide(claim, coverage, ledger):
    if coverage is None:
        return "REVIEW", "POLICY_NOT_FOUND"
    if not coverage["active"]:
        return "REVIEW", "INACTIVE_POLICY"
    if claim["amount_cents"] > coverage["limit_cents"]:
        return "REVIEW", "OVER_LIMIT"
    paid = ledger.get(claim["claim_id"])
    if paid is None:
        return "REVIEW", "MISSING_LEDGER"
    if paid != claim["amount_cents"]:
        return "REVIEW", "AMOUNT_MISMATCH"
    return "CONCILIATED", "MATCHED"


def submit_and_verify(base_url, claim_id, outcome, reason, max_attempts, log, correlation_id):
    request_id = "REQ-" + hashlib.sha256(f"{claim_id}|{outcome}|{reason}".encode()).hexdigest()[:20]
    data = urlencode({"outcome": outcome, "reason_code": reason, "request_id": request_id}).encode()
    try:
        with urlopen(Request(base_url + f"/claims/{claim_id}/decision", data=data, method="POST"), timeout=3):
            pass
    except (HTTPError, URLError, TimeoutError) as error:
        if isinstance(error, HTTPError):
            error.close()
        raise DecisionUnverified("DECISION_SUBMISSION_UNCONFIRMED", request_id) from error
    log("decision_submitted", claim_id, correlation_id, "AWAITING_VERIFICATION",
        request_id=request_id)

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(base_url + f"/api/claims/{claim_id}", timeout=3) as response:
                saved = json.load(response)
        except (HTTPError, URLError, TimeoutError) as error:
            status = error.code if isinstance(error, HTTPError) else None
            if isinstance(error, HTTPError):
                error.close()
            if attempt == max_attempts or (status is not None and status not in TRANSIENT_CODES):
                raise DecisionUnverified("DECISION_VERIFICATION_UNAVAILABLE", request_id) from error
            log("decision_verify_retry", claim_id, correlation_id, "RETRY",
                attempt=attempt, http_status=status)
            time.sleep(0.05 * 2 ** (attempt - 1))
            continue
        except ValueError as error:
            raise DecisionUnverified("DECISION_VERIFICATION_INVALID", request_id) from error
        if not isinstance(saved, dict) or (saved.get("status"), saved.get("reason_code")) != (outcome, reason):
            raise DecisionUnverified("DECISION_STATE_MISMATCH", request_id)
        return request_id

    raise DecisionUnverified("DECISION_VERIFICATION_UNAVAILABLE", request_id)


def run_case(base_url, ledger_csv, output_dir, claim_ids=None, max_attempts=3):
    """Run the synthetic QA flow; returns summary and writes auditable artifacts."""
    if max_attempts < 1 or max_attempts > 10:
        raise ValueError("max_attempts deve estar entre 1 e 10")
    base_url = base_url.rstrip("/")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    counts = {"conciliated": 0, "review": 0, "system_error": 0}
    decisions = []

    with (output_dir / "events.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        def log(event, claim_id, correlation_id, outcome, **extra):
            record = {
                "ts_utc": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id,
                "claim_id": claim_id,
                "correlation_id": correlation_id,
                "component": "qa_demo",
                "event": event,
                "outcome": outcome,
                **extra,
            }
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()

        try:
            ledger = read_ledger(ledger_csv)
            claims = fetch_queue(base_url)
            requested = set(claim_ids) if claim_ids is not None else None
            selected_all = [c for c in claims if requested is None or c["claim_id"] in requested]
            if requested is not None and len(selected_all) != len(requested):
                raise SystemFailure("CLAIM_NOT_IN_UI_QUEUE")
            selected = [c for c in selected_all if c["status"] == "PENDING"]
            for claim in selected_all:
                if claim["status"] != "PENDING":
                    log("claim_skipped", claim["claim_id"], None, "SKIPPED",
                        reason_code="ALREADY_PROCESSED")
            for claim in selected:
                claim_id = claim["claim_id"]
                correlation_id = uuid.uuid4().hex
                log("claim_started", claim_id, correlation_id, "STARTED")
                try:
                    coverage = fetch_coverage(base_url, claim["policy_id"], max_attempts,
                                              log, claim_id, correlation_id)
                    outcome, reason = decide(claim, coverage, ledger)
                    request_id = submit_and_verify(base_url, claim_id, outcome, reason,
                                                   max_attempts, log, correlation_id)
                    counts["conciliated" if outcome == "CONCILIATED" else "review"] += 1
                    decisions.append({"claim_id": claim_id, "status": outcome, "reason_code": reason,
                                      "request_id": request_id})
                    log("decision_verified", claim_id, correlation_id, outcome, reason_code=reason,
                        request_id=request_id)
                except DecisionUnverified as error:
                    counts["system_error"] += 1
                    decisions.append({"claim_id": claim_id, "status": "UNVERIFIED",
                                      "reason_code": str(error), "request_id": error.request_id})
                    log("decision_unverified", claim_id, correlation_id, "UNVERIFIED",
                        reason_code=str(error), request_id=error.request_id)
                except (SystemFailure, HTTPError, URLError, TimeoutError, ValueError) as error:
                    counts["system_error"] += 1
                    reason_code = str(error) if isinstance(error, SystemFailure) else type(error).__name__
                    decisions.append({"claim_id": claim_id, "status": "PENDING", "reason_code": reason_code})
                    log("system_exception", claim_id, correlation_id, "PENDING", reason_code=reason_code)
                    if isinstance(error, HTTPError):
                        error.close()
        except (SystemFailure, HTTPError, URLError, TimeoutError, ValueError) as error:
            counts["system_error"] += 1
            reason_code = str(error) if isinstance(error, SystemFailure) else type(error).__name__
            log("run_exception", None, None, "NO_GO", reason_code=reason_code)
            if isinstance(error, HTTPError):
                error.close()

    summary = {
        "run_id": run_id,
        "data_classification": "SYNTHETIC",
        "counts": counts,
        "gate": "NO_GO" if counts["system_error"] else "GO",
        "decisions": decisions,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    lines = ["# Parecer da execução sintética", "", f"Run ID: `{run_id}`", "",
             f"Gate técnico: **{summary['gate']}**", "",
             f"Conciliados: {counts['conciliated']} | Revisão humana: {counts['review']} | Erros técnicos: {counts['system_error']}",
             "", "| Sinistro | Estado | Motivo |", "|---|---|---|"]
    lines += [f"| {d['claim_id']} | {d['status']} | {d['reason_code']} |" for d in decisions]
    lines += ["", "A decisão final de implantação requer aprovação humana e os demais controles do checklist de Go/No-Go.", ""]
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    artifacts = {name: sha256(output_dir / name) for name in ("events.jsonl", "summary.json", "report.md")}
    manifest = {
        "run_id": run_id,
        "data_classification": "SYNTHETIC",
        "artifacts": artifacts,
        "input_ledger_sha256": sha256(ledger_csv) if Path(ledger_csv).is_file() else None,
        "input_claims_sha256": sha256(ROOT / "fixtures/sinistros.csv"),
        "source_sha256": {name: sha256(ROOT / name) for name in ("app.py", "qa_demo.py")},
        "hash_algorithm": "SHA-256",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description="Executa o case sintético de QA")
    parser.add_argument("--url", default="http://127.0.0.1:8765")
    parser.add_argument("--ledger", type=Path, default=ROOT / "fixtures/pagamentos.csv")
    parser.add_argument("--out", type=Path, default=ROOT / "runs/latest")
    parser.add_argument("--claim-id", action="append")
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()
    summary = run_case(args.url, args.ledger, args.out, args.claim_id, args.max_attempts)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(0 if summary["gate"] == "GO" else 2)


if __name__ == "__main__":
    main()
