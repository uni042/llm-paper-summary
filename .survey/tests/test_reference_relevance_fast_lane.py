from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_reference_relevance_requests as processor  # noqa: E402


class ReferenceRelevanceFastLaneTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.requests = (
            self.root / ".survey" / "work-queue" / "reference-curation" / "requests"
        )
        self.requests.mkdir(parents=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _request(self, request_id: str, **overrides: object) -> Path:
        payload: dict[str, object] = {
            "schema_version": 1,
            "request_id": request_id,
            "operation": "mark_unrelated",
            "canonical_id": "arXiv:2609.90001",
            "title": "Clearly unrelated paper",
            "reason": "outside the LLM systems survey scope",
            "identity_tokens": ["arXiv:2609.90001"],
            "linked_from": ["papers/inference/01-test/source.md"],
            "worker_id": "worker-7",
            "run_key": "worker-7-test",
            "scheduled_slot": "adhoc",
            "actual_invocation_start": "2026-09-24T22:00:00+09:00",
            "source_precheck_request_id": "precheck-1",
        }
        payload.update(overrides)
        path = self.requests / f"{request_id}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_request_updates_ledger_and_emits_continue_result(self) -> None:
        self._request("req-unrelated")
        summary = processor.process_pending(self.root)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["processed_count"], 1)

        ledger = json.loads(
            (self.root / ".survey/work-queue/reference-curation/unrelated-papers.json").read_text(encoding="utf-8")
        )
        self.assertIn("arXiv:2609.90001", ledger["records"])

        result = json.loads(
            (self.root / ".survey/work-queue/reference-curation/results/req-unrelated.json").read_text(encoding="utf-8")
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["classification"], "unrelated")
        self.assertEqual(result["next_action"], "CONTINUE_DISCOVERY_EVALUATION")
        self.assertEqual(result["worker_id"], "worker-7")
        self.assertEqual(result["run_key"], "worker-7-test")

    def test_borderline_request_moves_existing_opposite_classification(self) -> None:
        self._request("req-first")
        processor.process_pending(self.root)
        self._request(
            "req-second",
            operation="mark_borderline",
            reason="related but currently too weak for Research",
        )
        summary = processor.process_pending(self.root)
        self.assertTrue(summary["ok"])

        unrelated = json.loads(
            (self.root / ".survey/work-queue/reference-curation/unrelated-papers.json").read_text(encoding="utf-8")
        )
        borderline = json.loads(
            (self.root / ".survey/work-queue/reference-curation/borderline-papers.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("arXiv:2609.90001", unrelated["records"])
        self.assertIn("arXiv:2609.90001", borderline["records"])

    def test_invalid_request_is_isolated_from_valid_sibling(self) -> None:
        bad = {
            "schema_version": 1,
            "request_id": "bad",
            "operation": "delete_everything",
            "canonical_id": "arXiv:2609.90002",
            "reason": "bad operation",
        }
        (self.requests / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
        self._request(
            "good",
            canonical_id="arXiv:2609.90003",
            identity_tokens=["arXiv:2609.90003"],
        )

        summary = processor.process_pending(self.root)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["processed_count"], 1)
        self.assertEqual(summary["invalid_request_count"], 1)

        bad_result = json.loads(
            (self.root / ".survey/work-queue/reference-curation/results/bad.json").read_text(encoding="utf-8")
        )
        self.assertFalse(bad_result["ok"])
        self.assertEqual(bad_result["failure_class"], "invalid_request")

        ledger = json.loads(
            (self.root / ".survey/work-queue/reference-curation/unrelated-papers.json").read_text(encoding="utf-8")
        )
        self.assertIn("arXiv:2609.90003", ledger["records"])

    def test_existing_result_makes_request_idempotent(self) -> None:
        self._request("req-idempotent")
        first = processor.process_pending(self.root)
        second = processor.process_pending(self.root)
        self.assertEqual(first["processed_count"], 1)
        self.assertEqual(second["processed_count"], 0)
        self.assertEqual(second["already_processed_count"], 1)


if __name__ == "__main__":
    unittest.main()
