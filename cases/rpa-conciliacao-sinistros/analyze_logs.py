"""Confere integridade e resume um pacote de evidências JSONL sintético."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


ARTIFACTS = ("events.jsonl", "summary.json", "report.md")


def analyze_package(package_dir):
    package = Path(package_dir)
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    for name in ARTIFACTS:
        expected = manifest["artifacts"].get(name)
        actual = hashlib.sha256((package / name).read_bytes()).hexdigest()
        if expected != actual:
            raise ValueError(f"Hash inválido: {name}")

    summary = json.loads((package / "summary.json").read_text(encoding="utf-8"))
    if summary["run_id"] != manifest["run_id"]:
        raise ValueError("run_id inconsistente entre resumo e manifesto")
    events = [json.loads(line) for line in (package / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    if any(event.get("run_id") != summary["run_id"] for event in events):
        raise ValueError("run_id inconsistente no log")

    started = {event["claim_id"] for event in events if event["event"] == "claim_started"}
    finished = {event["claim_id"] for event in events
                if event["event"] in {"decision_verified", "decision_unverified", "system_exception"}}
    return {
        "run_id": summary["run_id"],
        "integrity": "OK",
        "gate": summary["gate"],
        "retry_events": sum(event["event"] == "api_retry" for event in events),
        "verification_retry_events": sum(event["event"] == "decision_verify_retry" for event in events),
        "verified_decisions": sum(event["event"] == "decision_verified" for event in events),
        "system_exceptions": sum(event["event"] in {"system_exception", "decision_unverified", "run_exception"} for event in events),
        "unclosed_claims": sorted(started - finished),
    }


def main():
    parser = argparse.ArgumentParser(description="Analisa pacote de evidências do case")
    parser.add_argument("package_dir", type=Path)
    args = parser.parse_args()
    try:
        result = analyze_package(args.package_dir)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Pacote inválido: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not result["unclosed_claims"] else 2)


if __name__ == "__main__":
    main()
