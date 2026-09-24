from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_discovery_rejection_ledger  # noqa: E402
import discovery_search_filter  # noqa: E402


class DiscoveryRejectionLedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / ".survey"
        self.queue = self.root / "work-queue"
        self.submissions = self.queue / "submissions" / "discovery"
        self.submissions.mkdir(parents=True)

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
        self.tmp.cleanup()

    def _write_submission(
        self,
        filename: str,
        *,
        rejected_candidates: list[dict[str, object]],
        submitted_at: str,
        axis: str,
    ) -> None:
        payload = {
            "schema_version": 1,
            "workflow_version": 10,
            "operation": "submit_discovery_round",
            "submitted_at": submitted_at,
            "candidates": [],
            "rejected_candidates": rejected_candidates,
            "discovery_stats": {
                "run_key": "2026-09-17T02:00:00+09:00",
                "round": filename,
                "axis": axis,
                "candidate_count": 0,
                "duplicate_filtered_count": 0,
            },
        }
        (self.submissions / filename).write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    def _write_job(self, filename: str, payload: dict[str, object]) -> None:
        jobs = self.queue / "jobs"
        jobs.mkdir(parents=True, exist_ok=True)
        (jobs / filename).write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_candidate_evaluation_rejection_is_persisted_and_filtered_next_time(self) -> None:
        self._write_submission(
            "rejected-round.json",
            rejected_candidates=[
                {
                    "canonical_id": "arXiv:2609.95555",
                    "title": "Rejected Systems Paper",
                    "source_url": "https://arxiv.org/abs/2609.95555",
                    "rejection_reason": "insufficient systems novelty for the survey",
                }
            ],
            submitted_at="2026-09-16T17:00:00+00:00",
            axis="test-axis",
        )

        summary = build_discovery_rejection_ledger.build_ledger(self.root)

        self.assertEqual(summary["rejection_record_count"], 1)
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

    def test_repeated_rejection_updates_latest_reason_without_duplicate_ledger_rows(self) -> None:
        candidate = {
            "canonical_id": "arXiv:2609.96666",
            "title": "Repeated Reject",
        }
        self._write_submission(
            "first.json",
            rejected_candidates=[{**candidate, "rejection_reason": "weak evaluation"}],
            submitted_at="2026-09-16T17:00:00+00:00",
            axis="axis-a",
        )
        self._write_submission(
            "second.json",
            rejected_candidates=[{**candidate, "rejection_reason": "still lacks relevant system evaluation"}],
            submitted_at="2026-09-16T18:00:00+00:00",
            axis="axis-b",
        )

        build_discovery_rejection_ledger.build_ledger(self.root)

        ledger = json.loads((self.queue / "discovery-rejections.json").read_text(encoding="utf-8"))
        self.assertEqual(len(ledger["records"]), 1)
        row = ledger["records"]["id:arXiv:2609.96666"]
        self.assertEqual(row["rejection_count"], 2)
        self.assertEqual(row["rejection_reason"], "still lacks relevant system evaluation")
        self.assertEqual(row["axis"], "axis-b")
        self.assertEqual(row["first_rejected_at"], "2026-09-16T17:00:00+00:00")
        self.assertEqual(row["last_rejected_at"], "2026-09-16T18:00:00+00:00")

    def test_submission_without_rejected_candidates_does_not_create_false_entries(self) -> None:
        self._write_submission(
            "accepted-only.json",
            rejected_candidates=[],
            submitted_at="2026-09-16T19:00:00+00:00",
            axis="axis-c",
        )

        summary = build_discovery_rejection_ledger.build_ledger(self.root)

        self.assertEqual(summary["rejection_record_count"], 0)
        ledger = json.loads((self.queue / "discovery-rejections.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["records"], {})

    def test_terminal_research_rejection_is_added_and_filtered(self) -> None:
        self._write_job(
            "job-research-rejected.json",
            {
                "job_id": "job-research-rejected",
                "type": "research",
                "status": "rejected",
                "canonical_id": "arXiv:2609.97777",
                "title": "Withdrawn Research Candidate",
                "source_url": "https://arxiv.org/abs/2609.97777",
                "blocker": "primary source was withdrawn and cannot be verified",
                "completed_at": "2026-09-17T05:00:00+00:00",
                "status_submission": ".survey/work-queue/submissions/research/attempt-rejected.json",
            },
        )

        summary = build_discovery_rejection_ledger.build_ledger(self.root)

        self.assertEqual(summary["rejection_record_count"], 1)
        ledger = json.loads((self.queue / "discovery-rejections.json").read_text(encoding="utf-8"))
        row = ledger["records"]["id:arXiv:2609.97777"]
        self.assertEqual(row["rejection_reason"], "primary source was withdrawn and cannot be verified")
        self.assertEqual(row["origin"], "research_terminal_rejection")
        self.assertEqual(row["source_submission"], ".survey/work-queue/submissions/research/attempt-rejected.json")

        result = discovery_search_filter.filter_search_batch(
            [{"arxiv_id": "2609.97777", "title": "Withdrawn Research Candidate"}],
            snapshot_dir=self.snapshot,
        )
        self.assertEqual(result["results"], [])
        self.assertEqual(result["rejection_ledger_filtered_count"], 1)

    def test_retrieval_blocks_are_not_added_even_with_legacy_permanent_status(self) -> None:
        self._write_job(
            "job-research-blocked.json",
            {
                "job_id": "job-research-blocked",
                "type": "research",
                "status": "blocked",
                "canonical_id": "arXiv:2609.98881",
                "title": "Temporary Source Failure",
                "source_url": "https://arxiv.org/abs/2609.98881",
                "blocker": "temporary upstream 503",
                "completed_at": "2026-09-17T05:10:00+00:00",
            },
        )
        self._write_job(
            "job-research-blocked-permanent.json",
            {
                "job_id": "job-research-blocked-permanent",
                "type": "research",
                "status": "blocked_permanent",
                "canonical_id": "arXiv:2609.98882",
                "title": "Legacy Retrieval Block",
                "source_url": "https://arxiv.org/abs/2609.98882",
                "blocker": "primary source remained unavailable after retired retry policy",
                "blocked_attempts": 3,
                "blocked_permanent_at": "2026-09-17T05:20:00+00:00",
            },
        )

        summary = build_discovery_rejection_ledger.build_ledger(self.root)

        self.assertEqual(summary["rejection_record_count"], 0)
        self.assertEqual(summary["research_terminal_rejection_count"], 0)
        ledger = json.loads((self.queue / "discovery-rejections.json").read_text(encoding="utf-8"))
        self.assertNotIn("id:arXiv:2609.98881", ledger["records"])
        self.assertNotIn("id:arXiv:2609.98882", ledger["records"])


if __name__ == "__main__":
    unittest.main()
