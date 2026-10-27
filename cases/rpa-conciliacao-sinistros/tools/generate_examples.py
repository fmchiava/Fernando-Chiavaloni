"""Regenera os dois pacotes de evidência sintética em bancos isolados."""

import tempfile
import threading
from pathlib import Path

from app import claim_data, make_server
from qa_demo import run_case


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "fixtures/pagamentos.csv"


def generate(name, fault_mode, claim_ids=None, max_attempts=3, expected_db_status=None):
    with tempfile.TemporaryDirectory() as temporary:
        db_path = Path(temporary) / "case.db"
        server = make_server(db_path, fault_mode=fault_mode)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}"
            summary = run_case(
                url, LEDGER, ROOT / "examples" / name,
                claim_ids=claim_ids, max_attempts=max_attempts,
            )
            if expected_db_status and claim_data(db_path, "SIN-001")["status"] != expected_db_status:
                raise RuntimeError(f"Estado persistido inesperado para {name}")
            return summary
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


def main():
    go = generate("go", "first")
    no_go = generate("no-go", "always", claim_ids=["SIN-001"], max_attempts=2)
    unverified = generate("unverified", "verify_always", claim_ids=["SIN-001"],
                          max_attempts=2, expected_db_status="CONCILIATED")
    if go["counts"] != {"conciliated": 1, "review": 2, "system_error": 0} or go["gate"] != "GO":
        raise RuntimeError("Resultado GO inesperado")
    if no_go["counts"] != {"conciliated": 0, "review": 0, "system_error": 1} or no_go["gate"] != "NO_GO":
        raise RuntimeError("Resultado NO_GO inesperado")
    if unverified["gate"] != "NO_GO" or unverified["decisions"][0]["status"] != "UNVERIFIED":
        raise RuntimeError("Resultado UNVERIFIED inesperado")
    print("Exemplos sintéticos GO, NO_GO e UNVERIFIED regenerados.")


if __name__ == "__main__":
    main()
