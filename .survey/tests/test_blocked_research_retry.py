from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class ResearchBlockedRetryPolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.state = {
            "stats": {
                "research_completed": 0,
                "rejected": 0,
            }
        }

    def _job(self) -> dict:
        return {
            "job_id": "job-research-test",
            "type": "research",
            "status": "ready",
            "priority": 80,
            "canonical_id": "arxiv:2609.99999",
        }

    def test_first_and_second_block_remain_retryable_then_third_becomes_permanent(self) -> None:
        job = self._job()

        queue_worker.process_research(
            {"status": "blocked", "reason": "primary source temporarily unavailable", "_file": "submission-1.json"},
            job,
            self.state,
        )
        self.assertEqual(job["status"], "blocked")
        self.assertEqual(job["blocked_attempts"], 1)
        self.assertEqual(len(job["block_history"]), 1)
        self.assertEqual(job["block_history"][0]["reason"], "primary source temporarily unavailable")
        self.assertIn("retry_not_before", job)

        job["status"] = "ready"
        queue_worker.process_research(
            {"status": "blocked", "reason": "upstream returned 503", "_file": "submission-2.json"},
            job,
            self.state,
        )
        self.assertEqual(job["status"], "blocked")
        self.assertEqual(job["blocked_attempts"], 2)
        self.assertEqual(len(job["block_history"]), 2)

        job["status"] = "ready"
        queue_worker.process_research(
            {"status": "blocked", "reason": "primary source still unavailable", "_file": "submission-3.json"},
            job,
            self.state,
        )
        self.assertEqual(job["status"], "blocked_permanent")
        self.assertEqual(job["blocked_attempts"], 3)
        self.assertEqual(len(job["block_history"]), 3)
        self.assertNotIn("retry_not_before", job)
        self.assertIn("completed_at", job)

    def test_due_blocked_research_job_is_requeued_without_losing_history(self) -> None:
        original_jobs = queue_worker.JOBS
        try:
            with tempfile.TemporaryDirectory() as td:
                jobs_dir = Path(td)
                queue_worker.JOBS = jobs_dir
                job_path = jobs_dir / "job-research-test.json"
                job_path.write_text(
                    json.dumps(
                        {
                            "job_id": "job-research-test",
                            "type": "research",
                            "status": "blocked",
                            "blocked_attempts": 1,
                            "blocker": "temporary fetch failure",
                            "block_history": [
                                {
                                    "attempt": 1,
                                    "blocked_at": "2026-09-12T08:00:00+00:00",
                                    "reason": "temporary fetch failure",
                                    "submission": "submission-1.json",
                                }
                            ],
                            "retry_not_before": "2026-09-12T09:00:00+00:00",
                        },
                        ensure_ascii=False,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                changed = queue_worker.requeue_retryable_blocked_research_jobs(
                    datetime(2026, 9, 12, 9, 0, 1, tzinfo=timezone.utc)
                )

                self.assertEqual(changed, 1)
                updated = json.loads(job_path.read_text(encoding="utf-8"))
                self.assertEqual(updated["status"], "ready")
                self.assertEqual(updated["blocked_attempts"], 1)
                self.assertEqual(len(updated["block_history"]), 1)
                self.assertNotIn("retry_not_before", updated)
                self.assertIn("retry_queued_at", updated)
        finally:
            queue_worker.JOBS = original_jobs

    def test_blocked_job_before_cooldown_is_not_requeued(self) -> None:
        original_jobs = queue_worker.JOBS
        try:
            with tempfile.TemporaryDirectory() as td:
                jobs_dir = Path(td)
                queue_worker.JOBS = jobs_dir
                job_path = jobs_dir / "job-research-test.json"
                job_path.write_text(
                    json.dumps(
                        {
                            "job_id": "job-research-test",
                            "type": "research",
                            "status": "blocked",
                            "blocked_attempts": 2,
                            "retry_not_before": "2026-09-12T10:00:00+00:00",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )

                changed = queue_worker.requeue_retryable_blocked_research_jobs(
                    datetime(2026, 9, 12, 9, 59, 59, tzinfo=timezone.utc)
                )

                self.assertEqual(changed, 0)
                updated = json.loads(job_path.read_text(encoding="utf-8"))
                self.assertEqual(updated["status"], "blocked")
        finally:
            queue_worker.JOBS = original_jobs

    def test_legacy_blocked_job_at_or_over_limit_becomes_permanent(self) -> None:
        original_jobs = queue_worker.JOBS
        try:
            with tempfile.TemporaryDirectory() as td:
                jobs_dir = Path(td)
                queue_worker.JOBS = jobs_dir
                job_path = jobs_dir / "job-research-test.json"
                job_path.write_text(
                    json.dumps(
                        {
                            "job_id": "job-research-test",
                            "type": "research",
                            "status": "blocked",
                            "blocked_attempts": 3,
                            "blocker": "repeated source failure",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )

                changed = queue_worker.requeue_retryable_blocked_research_jobs(
                    datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)
                )

                self.assertEqual(changed, 1)
                updated = json.loads(job_path.read_text(encoding="utf-8"))
                self.assertEqual(updated["status"], "blocked_permanent")
                self.assertIn("completed_at", updated)
        finally:
            queue_worker.JOBS = original_jobs


if __name__ == "__main__":
    unittest.main()
