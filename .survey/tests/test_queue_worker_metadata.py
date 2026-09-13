from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class AuditMetadataRoutingTest(unittest.TestCase):
    def test_nested_submission_audit_flags_create_audit_job(self) -> None:
        submission = {
            "paper_path": "papers/inference/test/paper.md",
            "submission": {
                "audit_required": True,
                "audit_reason": "会議版の数値を再確認",
                "audit_flags": ["final-version"],
            },
        }
        research_job = {
            "job_id": "job-research-test",
            "canonical_id": "arXiv:2601.00001",
            "priority": 80,
        }
        with patch.object(queue_worker, "add_job", return_value=True) as add_job:
            self.assertTrue(queue_worker.make_audit_job(submission, research_job))
        created = add_job.call_args.args[0]
        self.assertEqual(created["reason"], "会議版の数値を再確認")
        self.assertEqual(created["paper_path"], "papers/inference/test/paper.md")

    def test_short_completed_artifact_is_rejected_before_write(self) -> None:
        original_root = queue_worker.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                repo_root = Path(td)
                survey_root = repo_root / ".survey"
                survey_root.mkdir()
                queue_worker.ROOT = survey_root

                submission = {
                    "status": "completed",
                    "paper_path": "papers/inference/test/short.md",
                    "content": "短すぎる成果物",
                }
                job = {
                    "job_id": "job-research-short",
                    "type": "research",
                    "paper_path": submission["paper_path"],
                }
                target = repo_root / submission["paper_path"]

                fake_result = SimpleNamespace(returncode=0, stdout="ok", stderr="")
                with patch("subprocess.run", return_value=fake_result):
                    with self.assertRaisesRegex(ValueError, "complete Markdown"):
                        queue_worker.apply_artifact(submission, job)

                self.assertFalse(target.exists())
        finally:
            queue_worker.ROOT = original_root


class DiscoveryReplenishmentTest(unittest.TestCase):
    def test_active_claim_hides_ready_job_and_reports_claiming_summary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            survey_root = root / ".survey"
            (survey_root / "work-queue/claims").mkdir(parents=True)
            (survey_root / "work-queue/claims/job-research-0.json").write_text(
                '{"job_id":"job-research-0","claim_id":"claim-a","expires_at":"2999-01-01T00:00:00+00:00"}',
                encoding="utf-8",
            )
            jobs = [{
                "job_id": "job-research-0", "type": "research", "lane": "research",
                "status": "ready", "priority": 90, "created_at": "2026-09-12T00:00:00+00:00",
            }, {
                "job_id": "job-research-1", "type": "research", "lane": "research",
                "status": "ready", "priority": 80, "created_at": "2026-09-12T00:00:01+00:00",
            }, {
                "job_id": "job-discovery", "type": "discovery", "lane": "discovery",
                "status": "ready", "priority": 50, "created_at": "2026-09-12T00:00:02+00:00",
            }]
            original_root = queue_worker.ROOT
            try:
                queue_worker.ROOT = survey_root
                with patch.object(queue_worker, "iter_jobs", return_value=iter(jobs)):
                    snapshot = queue_worker.queue_snapshot()
            finally:
                queue_worker.ROOT = original_root
            visible = {row["job_id"] for row in snapshot["next_jobs"]}
            self.assertNotIn("job-research-0", visible)
            self.assertIn("job-research-1", visible)
            self.assertIn("job-discovery", visible)
            self.assertEqual(snapshot["claiming"], {"ready_research_audit": 2, "actively_claimed": 1, "claimable": 1})
    def test_ready_research_does_not_block_discovery_replenishment(self) -> None:
        jobs = [
            {
                "job_id": "job-research-existing",
                "type": "research",
                "lane": "research",
                "status": "ready",
                "priority": 90,
            }
        ]
        with patch.object(queue_worker, "iter_jobs", return_value=iter(jobs)):
            with patch.object(queue_worker, "add_job", return_value=True) as add_job:
                self.assertTrue(queue_worker.ensure_discovery_job())

        created = add_job.call_args.args[0]
        self.assertEqual(created["type"], "discovery")
        self.assertEqual(created["lane"], "discovery")

    def test_existing_active_discovery_prevents_duplicate_replenishment(self) -> None:
        jobs = [
            {
                "job_id": "job-research-existing",
                "type": "research",
                "status": "ready",
            },
            {
                "job_id": "job-discovery-existing",
                "type": "discovery",
                "lane": "discovery",
                "status": "ready",
            },
        ]
        with patch.object(queue_worker, "iter_jobs", return_value=iter(jobs)):
            with patch.object(queue_worker, "add_job", return_value=True) as add_job:
                self.assertFalse(queue_worker.ensure_discovery_job())

        add_job.assert_not_called()

    def test_snapshot_keeps_discovery_visible_when_research_fills_priority_window(self) -> None:
        jobs = [
            {
                "job_id": f"job-research-{index}",
                "type": "research",
                "lane": "research",
                "status": "ready",
                "priority": 90 - index,
                "created_at": f"2026-09-12T00:00:{index:02d}+00:00",
            }
            for index in range(9)
        ]
        jobs.append(
            {
                "job_id": "job-discovery-existing",
                "type": "discovery",
                "lane": "discovery",
                "status": "ready",
                "priority": 50,
                "created_at": "2026-09-12T00:01:00+00:00",
            }
        )

        with patch.object(queue_worker, "iter_jobs", return_value=iter(jobs)):
            snapshot = queue_worker.queue_snapshot()

        visible_ids = {job["job_id"] for job in snapshot["next_jobs"]}
        self.assertIn("job-discovery-existing", visible_ids)
        self.assertTrue({f"job-research-{index}" for index in range(8)}.issubset(visible_ids))


if __name__ == "__main__":
    unittest.main()
