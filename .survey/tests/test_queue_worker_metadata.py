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


if __name__ == "__main__":
    unittest.main()
