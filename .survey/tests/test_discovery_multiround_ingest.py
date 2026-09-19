from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402
import recover_discovery_submissions  # noqa: E402


class DiscoveryMultiRoundIngestTest(unittest.TestCase):
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

    @staticmethod
    def _round_payload() -> dict:
        return {
            "schema_version": 1,
            "workflow_version": 10,
            "operation": "submit_discovery_round",
            "candidates": [
                {
                    "canonical_id": "arXiv:2609.99991",
                    "title": "Test Multi-round Discovery Paper",
                    "source_url": "https://arxiv.org/abs/2609.99991",
                    "paper_path": "papers/inference/99-test/2609.99991.md",
                    "priority": 90,
                    "reason": "regression fixture",
                }
            ],
            "discovery_stats": {
                "run_key": "2026-09-16T08:00:00+09:00",
                "round": "specialist-regression-1",
                "axis": "regression-axis",
                "query_summary": "multi-round transport regression",
                "candidate_count": 1,
                "duplicate_filtered_count": 0,
            },
        }

    def test_explicit_discovery_round_does_not_require_preissued_job(self) -> None:
        payload = self._round_payload()
        source = queue_worker.SUBMISSIONS / "round-without-job.json"
        source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        queue_worker.process_submissions(self._state())

        result = json.loads((queue_worker.RESULTS / source.name).read_text(encoding="utf-8"))
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["job_type"], "discovery")
        self.assertEqual(result["job_status"], "completed")
        research = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in queue_worker.JOBS.glob("*.json")
            if json.loads(path.read_text(encoding="utf-8")).get("type") == "research"
        ]
        self.assertEqual([row.get("canonical_id") for row in research], ["arXiv:2609.99991"])

    def test_discovery_preserves_identity_aliases_on_research_job(self) -> None:
        payload = self._round_payload()
        payload["candidates"][0]["openreview_id"] = "alias-review-id"
        payload["candidates"][0]["identifiers"] = ["DOI:10.5555/example"]
        source = queue_worker.SUBMISSIONS / "round-with-aliases.json"
        source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        queue_worker.process_submissions(self._state())

        research = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in queue_worker.JOBS.glob("*.json")
            if json.loads(path.read_text(encoding="utf-8")).get("type") == "research"
        ]
        self.assertEqual(len(research), 1)
        self.assertEqual(research[0].get("openreview_id"), "alias-review-id")
        self.assertEqual(research[0].get("identifiers"), ["DOI:10.5555/example"])

    def test_recovery_accepts_legacy_unknown_specialist_job_id(self) -> None:
        payload = self._round_payload()
        payload.pop("operation")
        payload["job_id"] = "job-discovery-specialist-20260916-0800-regression-1"
        source = queue_worker.SUBMISSIONS / "legacy-unknown-job.json"
        source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        queue_worker.RESULTS.mkdir(parents=True)
        (queue_worker.RESULTS / source.name).write_text(
            json.dumps({
                "schema_version": 1,
                "workflow_version": 10,
                "submission": "work-queue/submissions/legacy-unknown-job.json",
                "ok": False,
                "error": "ValueError: unknown job_id",
            }),
            encoding="utf-8",
        )

        summary = recover_discovery_submissions.recover(self.root)

        self.assertEqual(summary["recovered_count"], 1, summary)
        result = json.loads((queue_worker.RESULTS / source.name).read_text(encoding="utf-8"))
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["recovered"])
        self.assertEqual(result["submitted_job_id"], payload["job_id"])
        research_ids = {
            row.get("canonical_id")
            for path in queue_worker.JOBS.glob("*.json")
            for row in [json.loads(path.read_text(encoding="utf-8"))]
            if row.get("type") == "research"
        }
        self.assertIn("arXiv:2609.99991", research_ids)

    def test_arbitrary_unknown_job_id_is_still_rejected(self) -> None:
        payload = {
            "schema_version": 1,
            "workflow_version": 10,
            "job_id": "job-does-not-exist",
            "status": "completed",
            "content": "x" * 600,
        }
        source = queue_worker.SUBMISSIONS / "unknown-nondiscovery.json"
        source.write_text(json.dumps(payload), encoding="utf-8")

        queue_worker.process_submissions(self._state())

        result = json.loads((queue_worker.RESULTS / source.name).read_text(encoding="utf-8"))
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "ValueError: unknown job_id")


if __name__ == "__main__":
    unittest.main()
