"""Aplicação local fictícia: fila web, API de cobertura e decisões em SQLite."""

import argparse
import csv
import html
import json
import re
import sqlite3
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
COVERAGE = {
    "POL-1001": {"active": True, "limit_cents": 100000},
    "POL-1002": {"active": True, "limit_cents": 100000},
    "POL-1003": {"active": False, "limit_cents": 100000},
}
ALLOWED_DECISIONS = {
    ("CONCILIATED", "MATCHED"),
    ("REVIEW", "INACTIVE_POLICY"),
    ("REVIEW", "OVER_LIMIT"),
    ("REVIEW", "MISSING_LEDGER"),
    ("REVIEW", "AMOUNT_MISMATCH"),
    ("REVIEW", "POLICY_NOT_FOUND"),
}


def connect(db_path):
    connection = sqlite3.connect(db_path, timeout=5)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_session(db_path):
    connection = connect(db_path)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db(db_path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with db_session(db_path) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS claims (
            claim_id TEXT PRIMARY KEY, policy_id TEXT NOT NULL,
            amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0))""")
        connection.execute("""CREATE TABLE IF NOT EXISTS decisions (
            claim_id TEXT PRIMARY KEY REFERENCES claims(claim_id),
            outcome TEXT NOT NULL, reason_code TEXT NOT NULL,
            request_id TEXT NOT NULL UNIQUE)""")
        with (ROOT / "fixtures/sinistros.csv").open(newline="", encoding="utf-8") as source:
            for row in csv.DictReader(source):
                connection.execute(
                    "INSERT OR IGNORE INTO claims VALUES (?, ?, ?)",
                    (row["claim_id"], row["policy_id"], int(row["amount_cents"])),
                )


def claim_data(db_path, claim_id):
    with db_session(db_path) as connection:
        row = connection.execute("""SELECT c.claim_id, c.policy_id, c.amount_cents,
            COALESCE(d.outcome, 'PENDING') AS status, d.reason_code
            FROM claims c LEFT JOIN decisions d ON d.claim_id = c.claim_id
            WHERE c.claim_id = ?""", (claim_id,)).fetchone()
    return dict(row) if row else None


def make_server(db_path, fault_mode="none", host="127.0.0.1", port=0):
    """Create a localhost demo server with deterministic fault injection."""
    if fault_mode not in {"none", "first", "always", "ui_changed", "malformed_api",
                          "verify_first", "verify_always"}:
        raise ValueError("fault_mode inválido")
    init_db(db_path)
    fault_lock = threading.Lock()
    coverage_calls = 0
    verification_calls = 0

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # Dados do case ficam apenas nos artefatos JSONL controlados.

        def send_body(self, status, body, content_type="text/plain; charset=utf-8"):
            raw = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def send_json(self, status, payload):
            self.send_body(status, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")

        def do_GET(self):
            nonlocal coverage_calls, verification_calls
            path = urlparse(self.path).path
            if path == "/claims":
                with db_session(db_path) as connection:
                    rows = connection.execute("""SELECT c.claim_id, c.policy_id, c.amount_cents,
                        COALESCE(d.outcome, 'PENDING') AS status
                        FROM claims c LEFT JOIN decisions d ON d.claim_id = c.claim_id
                        ORDER BY c.claim_id""").fetchall()
                def row_html(row):
                    policy_attr = "" if fault_mode == "ui_changed" else f'data-policy-id="{html.escape(row["policy_id"])}" '
                    return (
                        f'<tr data-claim-id="{html.escape(row["claim_id"])}" '
                        f'{policy_attr}data-amount-cents="{row["amount_cents"]}" '
                        f'data-status="{html.escape(row["status"])}">'
                        f'<td><a href="/claims/{html.escape(row["claim_id"])}">{html.escape(row["claim_id"])}</a></td>'
                        f'<td>{html.escape(row["policy_id"])}</td><td>{row["amount_cents"] / 100:.2f}</td>'
                        f'<td>{html.escape(row["status"])}</td></tr>'
                    )

                table = "".join(row_html(row) for row in rows)
                page = ("<!doctype html><html lang='pt-BR'><meta charset='utf-8'>"
                        "<title>Fila sintética de sinistros</title><h1>Fila de sinistros</h1>"
                        "<table><thead><tr><th>ID</th><th>Apólice</th><th>Valor</th><th>Status</th>"
                        f"</tr></thead><tbody>{table}</tbody></table></html>")
                return self.send_body(200, page, "text/html; charset=utf-8")
            match = re.fullmatch(r"/claims/(SIN-\d+)", path)
            if match:
                claim = claim_data(db_path, match.group(1))
                if not claim:
                    return self.send_body(404, "Sinistro não encontrado")
                page = ("<!doctype html><html lang='pt-BR'><meta charset='utf-8'>"
                        f"<title>{claim['claim_id']}</title><h1>{claim['claim_id']}</h1>"
                        f"<p>Apólice: {claim['policy_id']} | Valor: {claim['amount_cents'] / 100:.2f}"
                        f" | Status: {claim['status']}</p>"
                        f"<form method='post' action='/claims/{claim['claim_id']}/decision'>"
                        "<label>Resultado <select name='outcome'><option>CONCILIATED</option>"
                        "<option>REVIEW</option></select></label>"
                        "<label>Motivo <input name='reason_code'></label>"
                        "<label>Requisição <input name='request_id'></label>"
                        "<button type='submit'>Salvar decisão</button></form></html>")
                return self.send_body(200, page, "text/html; charset=utf-8")
            match = re.fullmatch(r"/api/coverage/(POL-\d+)", path)
            if match:
                with fault_lock:
                    coverage_calls += 1
                    fail = fault_mode == "always" or (fault_mode == "first" and coverage_calls == 1)
                if fail:
                    return self.send_json(503, {"error": "COVERAGE_TEMPORARILY_UNAVAILABLE"})
                if fault_mode == "malformed_api":
                    return self.send_json(200, {"policy_id": match.group(1)})
                data = COVERAGE.get(match.group(1))
                return self.send_json(200, {"policy_id": match.group(1), **data}) if data else self.send_json(404, {"error": "POLICY_NOT_FOUND"})
            match = re.fullmatch(r"/api/claims/(SIN-\d+)", path)
            if match:
                data = claim_data(db_path, match.group(1))
                if data and data["status"] != "PENDING" and fault_mode in {"verify_first", "verify_always"}:
                    with fault_lock:
                        verification_calls += 1
                        fail = fault_mode == "verify_always" or verification_calls == 1
                    if fail:
                        return self.send_json(503, {"error": "VERIFICATION_TEMPORARILY_UNAVAILABLE"})
                return self.send_json(200, data) if data else self.send_json(404, {"error": "CLAIM_NOT_FOUND"})
            self.send_body(404, "Rota não encontrada")

        def do_POST(self):
            match = re.fullmatch(r"/claims/(SIN-\d+)/decision", urlparse(self.path).path)
            if not match:
                return self.send_body(404, "Rota não encontrada")
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                return self.send_json(400, {"error": "INVALID_BODY"})
            params = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
            outcome = params.get("outcome", [""])[0]
            reason = params.get("reason_code", [""])[0]
            request_id = params.get("request_id", [""])[0]
            if (outcome, reason) not in ALLOWED_DECISIONS or not re.fullmatch(r"[A-Za-z0-9-]{1,80}", request_id):
                return self.send_json(400, {"error": "INVALID_DECISION"})
            claim_id = match.group(1)
            with db_session(db_path) as connection:
                connection.execute("BEGIN IMMEDIATE")
                claim = connection.execute("SELECT 1 FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
                if not claim:
                    return self.send_json(404, {"error": "CLAIM_NOT_FOUND"})
                existing = connection.execute("SELECT * FROM decisions WHERE claim_id = ?", (claim_id,)).fetchone()
                if existing:
                    if (existing["outcome"], existing["reason_code"], existing["request_id"]) != (outcome, reason, request_id):
                        return self.send_json(409, {"error": "DECISION_CONFLICT"})
                else:
                    connection.execute("INSERT INTO decisions VALUES (?, ?, ?, ?)", (claim_id, outcome, reason, request_id))
            self.send_json(200, {"claim_id": claim_id, "status": outcome, "reason_code": reason})

    return ThreadingHTTPServer((host, port), Handler)


def main():
    parser = argparse.ArgumentParser(description="Aplicação local sintética do case")
    parser.add_argument("--db", type=Path, default=ROOT / "runs/demo.db")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--fault", choices=["none", "first", "always", "ui_changed", "malformed_api",
                                           "verify_first", "verify_always"], default="none")
    args = parser.parse_args()
    server = make_server(args.db, fault_mode=args.fault, port=args.port)
    print(f"UI: http://127.0.0.1:{server.server_port}/claims | falha: {args.fault}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
