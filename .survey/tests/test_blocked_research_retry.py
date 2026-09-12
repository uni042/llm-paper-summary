from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import blocked_retry  # noqa: E402


UTC = timezone.utc


class ResearchBlockedRetryPolicyTest(unittest.TestCase):
    def _write_job(self, jobs_dir: Path, job: dict) -> Path:
        path = jobs_dir / f"{job['job_id']}.json"
        path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _read_job(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_three_distinct_block_events_promote_research_job_to_permanent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._write_job(
                jobs_dir,
                {
                    "job_id": "job-research-test",
                    "type": "research",
                    "status": "blocked",
                    "completed_at": "2026-09-12T08:00:00+00:00",
                    "blocker": "primary source temporarily unavailable",
                },
            )

            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 8, 1, tzinfo=UTC))
            job = self._read_job(path)
            self.assertEqual(job["status"], "blocked")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(len(job["block_history"]), 1)
            self.assertEqual(job["block_history"][0]["reason"], "primary source temporarily unavailable")
            self.assertIn("retry_not_before", job)

            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 9, 2, tzinfo=UTC))
            job = self._read_job(path)
            self.assertEqual(job["status"], "ready")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(len(job["block_history"]), 1)
            self.assertNotIn("retry_not_before", job)
            self.assertIn("retry_queued_at", job)

            job.update(
                status="blocked",
                completed_at="2026-09-12T10:00:00+00:00",
                blocker="upstream returned 503",
            )
            self._write_job(jobs_dir, job)
            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 10, 1, tzinfo=UTC))
            job = self._read_job(path)
            self.assertEqual(job["status"], "blocked")
            self.assertEqual(job["blocked_attempts"], 2)
            self.assertEqual(len(job["block_history"]), 2)

            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 11, 2, tzinfo=UTC))
            job = self._read_job(path)
            self.assertEqual(job["status"], "ready")

            job.update(
                status="blocked",
                completed_at="2026-09-12T12:00:00+00:00",
                blocker="primary source still unavailable",
            )
            self._write_job(jobs_dir, job)
            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 12, 1, tzinfo=UTC))
            job = self._read_job(path)
            self.assertEqual(job["status"], "blocked_permanent")
            self.assertEqual(job["blocked_attempts"], 3)
            self.assertEqual(len(job["block_history"]), 3)
            self.assertNotIn("retry_not_before", job)
            self.assertIn("blocked_permanent_at", job)

    def test_same_block_event_is_not_double_counted_before_retry(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._write_job(
                jobs_dir,
                {
                    "job_id": "job-research-test",
                    "type": "research",
                    "status": "blocked",
                    "completed_at": "2026-09-12T08:00:00+00:00",
                    "blocker": "temporary fetch failure",
                },
            )

            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 8, 1, tzinfo=UTC))
            blocked_retry.process_blocked_research_jobs(root, datetime(2026, 9, 12, 8, 30, tzinfo=UTC))

            job = self._read_job(path)
            self.assertEqual(job["status"], "blocked")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(len(job["block_history"]), 1)

    def test_due_blocked_research_job_is_requeued_without_losing_history(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._write_job(
                jobs_dir,
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
                        }
                    ],
                    "last_recorded_blocked_event": "2026-09-12T08:00:00+00:00",
                    "retry_not_before": "2026-09-12T09:00:00+00:00",
                },
            )

            result = blocked_retry.process_blocked_research_jobs(
                root, datetime(2026, 9, 12, 9, 0, 1, tzinfo=UTC)
            )

            self.assertEqual(result["requeued"], 1)
            job = self._read_job(path)
            self.assertEqual(job["status"], "ready")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(len(job["block_history"]), 1)
            self.assertNotIn("retry_not_before", job)
            self.assertIn("retry_queued_at", job)

    def test_legacy_blocked_job_at_or_over_limit_becomes_permanent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._write_job(
                jobs_dir,
                {
                    "job_id": "job-research-test",
                    "type": "research",
                    "status": "blocked",
                    "blocked_attempts": 3,
                    "blocker": "repeated source failure",
                },
            )

            result = blocked_retry.process_blocked_research_jobs(
                root, datetime(2026, 9, 12, 12, 0, 0, tzinfo=UTC)
            )

            self.assertEqual(result["permanent"], 1)
            job = self._read_job(path)
            self.assertEqual(job["status"], "blocked_permanent")
            self.assertIn("blocked_permanent_at", job)


if __name__ == "__main__":
    unittest.main()
