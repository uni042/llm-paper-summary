from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPTS))

import blocked_retry  # noqa: E402


UTC = timezone.utc
AT = datetime(2026, 9, 1, 8, 0, tzinfo=UTC)


class ResearchBlockedRetryPolicyTest(unittest.TestCase):
    def _write_job(self, jobs_dir: Path, job: dict) -> Path:
        path = jobs_dir / f"{job['job_id']}.json"
        path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _read_job(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _seed_blocked(self, jobs_dir: Path, **extra) -> Path:
        job = {
            "job_id": "job-research-test",
            "type": "research",
            "status": "blocked",
            "completed_at": AT.isoformat(),
            "blocker": "primary source temporarily unavailable",
        }
        job.update(extra)
        return self._write_job(jobs_dir, job)

    def test_new_block_event_schedules_retry_seven_days_later(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._seed_blocked(jobs_dir)

            result = blocked_retry.process_blocked_research_jobs(root, AT)
            job = self._read_job(path)

            self.assertEqual(result["new_block_events"], 1)
            self.assertEqual(job["status"], "blocked")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(
                blocked_retry.parse_time(job["retry_not_before"]),
                AT + timedelta(days=7),
            )
            self.assertNotIn("blocked_permanent_at", job)
            self.assertFalse(job.get("blocked_retry_dormant", False))

    def test_job_is_not_requeued_before_seven_day_cooldown(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._seed_blocked(jobs_dir)
            blocked_retry.process_blocked_research_jobs(root, AT)

            result = blocked_retry.process_blocked_research_jobs(
                root, AT + timedelta(days=6, hours=23, minutes=59)
            )
            job = self._read_job(path)

            self.assertEqual(result["requeued"], 0)
            self.assertEqual(job["status"], "blocked")

    def test_due_blocked_research_job_is_requeued_after_seven_days(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._seed_blocked(jobs_dir)
            blocked_retry.process_blocked_research_jobs(root, AT)

            result = blocked_retry.process_blocked_research_jobs(root, AT + timedelta(days=7))
            job = self._read_job(path)

            self.assertEqual(result["requeued"], 1)
            self.assertEqual(job["status"], "ready")
            self.assertEqual(job["blocked_attempts"], 1)
            self.assertNotIn("retry_not_before", job)
            self.assertIn("retry_queued_at", job)

    def test_same_block_event_is_not_double_counted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._seed_blocked(jobs_dir)

            blocked_retry.process_blocked_research_jobs(root, AT)
            blocked_retry.process_blocked_research_jobs(root, AT + timedelta(hours=1))
            job = self._read_job(path)

            self.assertEqual(job["blocked_attempts"], 1)
            self.assertEqual(len(job["block_history"]), 1)

    def test_fifth_failure_after_28_days_becomes_dormant_not_permanent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            current = AT + timedelta(days=28)
            history = [
                {
                    "attempt": i + 1,
                    "blocked_at": (AT + timedelta(days=7 * i)).isoformat(),
                    "reason": "primary source temporarily unavailable",
                }
                for i in range(4)
            ]
            path = self._seed_blocked(
                jobs_dir,
                completed_at=current.isoformat(),
                blocked_attempts=4,
                block_history=history,
                first_blocked_at=AT.isoformat(),
                last_recorded_blocked_event=history[-1]["blocked_at"],
                last_blocked_at=history[-1]["blocked_at"],
            )

            result = blocked_retry.process_blocked_research_jobs(root, current)
            job = self._read_job(path)

            self.assertEqual(job["blocked_attempts"], 5)
            self.assertEqual(job["status"], "blocked")
            self.assertTrue(job["blocked_retry_dormant"])
            self.assertEqual(job["blocked_retry_state"], "dormant")
            self.assertIn("blocked_dormant_at", job)
            self.assertNotIn("retry_not_before", job)
            self.assertNotIn("blocked_permanent_at", job)
            self.assertEqual(result["dormant"], 1)
            self.assertEqual(result["permanent"], 0)

    def test_fifth_failure_before_28_days_stays_retryable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            current = AT + timedelta(days=20)
            history = [
                {
                    "attempt": i + 1,
                    "blocked_at": (AT + timedelta(days=5 * i)).isoformat(),
                    "reason": "primary source temporarily unavailable",
                }
                for i in range(4)
            ]
            path = self._seed_blocked(
                jobs_dir,
                completed_at=current.isoformat(),
                blocked_attempts=4,
                block_history=history,
                first_blocked_at=AT.isoformat(),
                last_recorded_blocked_event=history[-1]["blocked_at"],
                last_blocked_at=history[-1]["blocked_at"],
            )

            blocked_retry.process_blocked_research_jobs(root, current)
            job = self._read_job(path)

            self.assertEqual(job["blocked_attempts"], 5)
            self.assertFalse(job.get("blocked_retry_dormant", False))
            self.assertEqual(
                blocked_retry.parse_time(job["retry_not_before"]),
                current + timedelta(days=7),
            )
            self.assertNotIn("blocked_permanent_at", job)

    def test_dormant_job_is_not_periodically_requeued(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs_dir = root / "work-queue" / "jobs"
            jobs_dir.mkdir(parents=True)
            path = self._seed_blocked(
                jobs_dir,
                blocked_attempts=5,
                blocked_retry_dormant=True,
                blocked_retry_state="dormant",
                blocked_dormant_at=AT.isoformat(),
            )

            result = blocked_retry.process_blocked_research_jobs(root, AT + timedelta(days=60))
            job = self._read_job(path)

            self.assertEqual(result["requeued"], 0)
            self.assertEqual(result["changed"], 0)
            self.assertEqual(job["status"], "blocked")
            self.assertTrue(job["blocked_retry_dormant"])

    def test_router_keeps_flexible_primary_source_retrieval_policy(self) -> None:
        text = (ROOT / ".survey/docs/survey-workflow/worker-router.md").read_text(encoding="utf-8")
        self.assertIn("固定された4経路を各1回だけ試して打ち切る方式は使わない", text)
        self.assertIn("blocked Researchは原則7日後に再確認", text)
        self.assertIn("取得失敗だけを永久除外理由にしない", text)
        self.assertNotIn("全文取得経路はワーカーの気分で増減させず", text)


if __name__ == "__main__":
    unittest.main()
