from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_search_filter  # noqa: E402
import queue_worker  # noqa: E402


class DiscoveryRejectionLedgerTest(unittest.TestCase):
    GLOBALS = ("ROOT", "QUEUE", "JOBS", "SUBMISSIONS", "RESULTS", "STATE", "ARCHIVE", "DISCOVERY_STATE")

    def setUp(self) -> None:
        self.originals = {name: getattr(queue_worker, name) for name in self.GLOBALS}
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / ".survey"
        self.queue = self.root / "work-queue"
        queue_worker.ROOT = self.root
        queue_worker.QUEUE = self.queue
        queue_worker.JOBS = self.queue / "jobs"
        queue_worker.SUBMISSIONS = self.queue / "submissions"
        queue_worker.RESULTS = self.queue / "results"
        queue_worker.STATE = self.queue / "state.json"
        queue_worker.ARCHIVE = self.queue / "archive"
        queue_worker.DISCOVERY_STATE = self.queue / "discovery-state.json"
        queue_worker.SUBMISSIONS.mkdir(parents=True)
        queue_worker.JOBS.mkdir(parents=True)
        queue_worker.DISCOVERY_STATE.write_text(
            json.dumps({"schema_version": 2, "history_limit": 24, "history": [], "axes": {}}),
            encoding="utf-8",
        )

        self.snapshot = self.queue / "discovery-identities"
        self.snapshot.mkdir(parents=True)
        (self.snapshot / "_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "source": "queue_worker.existing_candidate_keys",
                    "code_search_is_authority": False,
                    "shards": {},
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            setattr(queue_worker, name, value)
        self.tmp.cleanup()

    @staticmethod
    def _state() -> dict:
        return {
            "stats": {
                "discovered": 0,
                "selected": 0,
                "research_completed": 0,
                "audit_completed": 0,
                "rejected": 0,
            }
        }

    def test_candidate_evaluation_rejection_is_persisted_and_filtered_next_time(self) -> None:
        payload = {
            "schema_version": 1,
            "workflow_version": 10,
            "operation": "submit_discovery_round",
            "candidates": [],
            "rejected_candidates": [
                {
                    "canonical_id": "arXiv:2609.95555",
                    "title": "Rejected Systems Paper",
                    "source_url": "https://arxiv.org/abs/2609.95555",
                    "rejection_reason": "insufficient systems novelty for the survey",
                }
            ],
            "discovery_stats": {
                "run_key": "2026-09-17T02:00:00+09:00",
                "round": "rejection-ledger-regression",
                "axis": "test-axis",
                "candidate_count": 0,
                "duplicate_filtered_count": 0,
            },
        }
        source = queue_worker.SUBMISSIONS / "rejected-round.json"
        source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        queue_worker.process_submissions(self._state())

        ledger_path = self.queue / "discovery-rejections.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        records = ledger["records"]
        self.assertIn("id:arXiv:2609.95555", records)
        row = records["id:arXiv:2609.95555"]
        self.assertEqual(row["rejection_reason"], "insufficient systems novelty for the survey")
        self.assertIn("id:arXiv:2609.95555", row["identity_tokens"])
        self.assertEqual(row["axis"], "test-axis")

        result = discovery_search_filter.filter_search_batch(
            [
                {
                    "arxiv_id": "2609.95555",
                    "title": "Rejected Systems Paper",
                },
                {
                    "arxiv_id": "2609.95556",
                    "title": "Fresh Systems Paper",
                },
            ],
            snapshot_dir=self.snapshot,
        )

        self.assertEqual([item["arxiv_id"] for item in result["results"]], ["2609.95556"])
        self.assertEqual(result["rejection_ledger_filtered_count"], 1)
        self.assertEqual(result["rejection_ledger_filtered_tokens"], ["id:arXiv:2609.95555"])

    def test_repeated_rejection_updates_reason_without_duplicate_ledger_rows(self) -> None:
        first = {
            "canonical_id": "arXiv:2609.96666",
            "title": "Repeated Reject",
            "rejection_reason": "weak evaluation",
        }
        second = {
            "canonical_id": "arXiv:2609.96666",
            "title": "Repeated Reject",
            "rejection_reason": "still lacks relevant system evaluation",
        }

        queue_worker.record_discovery_rejections(
            {"rejected_candidates": [first], "discovery_stats": {"axis": "axis-a"}, "_file": "first.json"}
        )
        queue_worker.record_discovery_rejections(
            {"rejected_candidates": [second], "discovery_stats": {"axis": "axis-b"}, "_file": "second.json"}
        )

        ledger = json.loads((self.queue / "discovery-rejections.json").read_text(encoding="utf-8"))
        self.assertEqual(len(ledger["records"]), 1)
        row = ledger["records"]["id:arXiv:2609.96666"]
        self.assertEqual(row["rejection_count"], 2)
        self.assertEqual(row["rejection_reason"], "still lacks relevant system evaluation")
        self.assertEqual(row["axis"], "axis-b")


if __name__ == "__main__":
    unittest.main()
