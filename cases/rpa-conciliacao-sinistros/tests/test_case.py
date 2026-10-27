import hashlib
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import claim_data, make_server
from analyze_logs import analyze_package
from qa_demo import run_case


ROOT = Path(__file__).resolve().parents[1]


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.server = None

    def tearDown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=2)
        self.temp.cleanup()

    def start_server(self, fault_mode="none"):
        self.server = make_server(self.root / "case.db", fault_mode=fault_mode)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def get_json(self, route):
        with urlopen(self.base + route) as response:
            return json.load(response)

    def test_ui_queue_and_coverage_api_expose_synthetic_claim(self):
        self.start_server()
        with urlopen(self.base + "/claims") as response:
            html = response.read().decode()
        self.assertIn('data-claim-id="SIN-001"', html)
        self.assertEqual(
            self.get_json("/api/coverage/POL-1001"),
            {"policy_id": "POL-1001", "active": True, "limit_cents": 100000},
        )

    def test_transient_503_is_retried_without_false_business_rejection(self):
        self.start_server(fault_mode="first")
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-001"], max_attempts=3,
        )
        self.assertEqual(result["counts"], {"conciliated": 1, "review": 0, "system_error": 0})
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "CONCILIATED")
        events = [json.loads(line) for line in (self.root / "evidence/events.jsonl").read_text().splitlines()]
        self.assertTrue(any(e["event"] == "api_retry" and e["attempt"] == 1 for e in events))

    def test_persistent_503_keeps_claim_pending(self):
        self.start_server(fault_mode="always")
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-001"], max_attempts=2,
        )
        self.assertEqual(result["counts"]["system_error"], 1)
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")
        self.assertEqual(result["gate"], "NO_GO")

    def test_transient_verification_failure_recovers_without_second_post(self):
        self.start_server(fault_mode="verify_first")
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-001"], max_attempts=2,
        )
        self.assertEqual(result["gate"], "GO")
        self.assertEqual(result["counts"]["conciliated"], 1)
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "CONCILIATED")
        events = [json.loads(line) for line in (self.root / "evidence/events.jsonl").read_text().splitlines()]
        self.assertEqual(sum(e["event"] == "decision_submitted" for e in events), 1)
        self.assertEqual(sum(e["event"] == "decision_verify_retry" for e in events), 1)
        self.assertEqual(sum(e["event"] == "decision_verified" for e in events), 1)

    def test_persistent_verification_failure_is_unverified_not_pending(self):
        self.start_server(fault_mode="verify_always")
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-001"], max_attempts=2,
        )
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(result["decisions"][0]["status"], "UNVERIFIED")
        self.assertEqual(claim_data(self.root / "case.db", "SIN-001")["status"], "CONCILIATED")
        analysis = analyze_package(self.root / "evidence")
        self.assertEqual(analysis["unclosed_claims"], [])
        self.assertEqual(analysis["system_exceptions"], 1)

    def test_changed_ui_contract_keeps_claim_pending(self):
        self.start_server(fault_mode="ui_changed")
        result = run_case(self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
                          claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")

    def test_malformed_coverage_response_keeps_claim_pending(self):
        self.start_server(fault_mode="malformed_api")
        result = run_case(self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
                          claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")

    def test_amount_mismatch_goes_to_manual_review(self):
        self.start_server()
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-002"],
        )
        self.assertEqual(result["counts"]["review"], 1)
        claim = self.get_json("/api/claims/SIN-002")
        self.assertEqual((claim["status"], claim["reason_code"]), ("REVIEW", "AMOUNT_MISMATCH"))

    def test_inactive_policy_goes_to_manual_review(self):
        self.start_server()
        result = run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-003"],
        )
        self.assertEqual(result["counts"]["review"], 1)
        self.assertEqual(self.get_json("/api/claims/SIN-003")["reason_code"], "INACTIVE_POLICY")

    def test_duplicate_ledger_blocks_batch_with_evidence(self):
        self.start_server()
        bad_ledger = self.root / "duplicate.csv"
        bad_ledger.write_text("claim_id,paid_cents\nSIN-001,80000\nSIN-001,80000\n", encoding="utf-8")
        result = run_case(self.base, bad_ledger, self.root / "evidence", claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")
        self.assertTrue((self.root / "evidence/manifest.json").exists())

    def test_missing_ledger_column_blocks_batch(self):
        self.start_server()
        bad_ledger = self.root / "missing-column.csv"
        bad_ledger.write_text("claim_id,amount\nSIN-001,80000\n", encoding="utf-8")
        result = run_case(self.base, bad_ledger, self.root / "evidence", claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")

    def test_duplicate_ledger_header_blocks_batch(self):
        self.start_server()
        bad_ledger = self.root / "duplicate-header.csv"
        bad_ledger.write_text(
            "claim_id,paid_cents,paid_cents\nSIN-001,80000,1\n", encoding="utf-8"
        )
        result = run_case(self.base, bad_ledger, self.root / "evidence", claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")

    def test_extra_ledger_column_blocks_batch(self):
        self.start_server()
        bad_ledger = self.root / "extra-column.csv"
        bad_ledger.write_text(
            "claim_id,paid_cents,account_number\nSIN-001,80000,123\n", encoding="utf-8"
        )
        result = run_case(self.base, bad_ledger, self.root / "evidence", claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")

    def test_missing_ledger_file_blocks_batch_and_marks_manifest(self):
        self.start_server()
        result = run_case(self.base, self.root / "not-found.csv", self.root / "evidence",
                          claim_ids=["SIN-001"])
        self.assertEqual(result["gate"], "NO_GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "PENDING")
        manifest = json.loads((self.root / "evidence/manifest.json").read_text())
        self.assertIsNone(manifest["input_ledger_sha256"])

    def test_second_run_skips_already_processed_claim(self):
        self.start_server()
        first = run_case(self.base, ROOT / "fixtures/pagamentos.csv", self.root / "first",
                         claim_ids=["SIN-001"])
        second = run_case(self.base, ROOT / "fixtures/pagamentos.csv", self.root / "second",
                          claim_ids=["SIN-001"])
        self.assertEqual(first["counts"]["conciliated"], 1)
        self.assertEqual(second["counts"], {"conciliated": 0, "review": 0, "system_error": 0})
        self.assertEqual(second["gate"], "GO")
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "CONCILIATED")

    def test_duplicate_submission_is_idempotent_and_conflict_is_rejected(self):
        self.start_server()
        route = self.base + "/claims/SIN-001/decision"
        data = {"outcome": "CONCILIATED", "reason_code": "MATCHED", "request_id": "REQ-001"}
        for _ in range(2):
            with urlopen(Request(route, data=urlencode(data).encode(), method="POST")) as response:
                self.assertEqual(response.status, 200)
        changed = {**data, "outcome": "REVIEW", "reason_code": "AMOUNT_MISMATCH"}
        with self.assertRaises(HTTPError) as error:
            urlopen(Request(route, data=urlencode(changed).encode(), method="POST"))
        self.assertEqual(error.exception.code, 409)
        error.exception.close()
        self.assertEqual(self.get_json("/api/claims/SIN-001")["status"], "CONCILIATED")

    def test_evidence_manifest_hash_matches_log(self):
        self.start_server()
        run_case(
            self.base, ROOT / "fixtures/pagamentos.csv", self.root / "evidence",
            claim_ids=["SIN-001"],
        )
        manifest = json.loads((self.root / "evidence/manifest.json").read_text())
        digest = hashlib.sha256((self.root / "evidence/events.jsonl").read_bytes()).hexdigest()
        self.assertEqual(manifest["artifacts"]["events.jsonl"], digest)
        self.assertEqual(manifest["data_classification"], "SYNTHETIC")
        self.assertEqual(manifest["source_sha256"]["qa_demo.py"],
                         hashlib.sha256((ROOT / "qa_demo.py").read_bytes()).hexdigest())
        self.assertEqual(manifest["input_claims_sha256"],
                         hashlib.sha256((ROOT / "fixtures/sinistros.csv").read_bytes()).hexdigest())

    def test_log_analysis_counts_retry_and_rejects_tampering(self):
        self.start_server(fault_mode="first")
        package = self.root / "evidence"
        run_case(self.base, ROOT / "fixtures/pagamentos.csv", package, claim_ids=["SIN-001"])
        analysis = analyze_package(package)
        self.assertEqual(analysis["retry_events"], 1)
        self.assertEqual(analysis["verified_decisions"], 1)
        with (package / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write("{}\n")
        with self.assertRaises(ValueError):
            analyze_package(package)


if __name__ == "__main__":
    unittest.main()
