from __future__ import annotations

import sys
import unittest
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
