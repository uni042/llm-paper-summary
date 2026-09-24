import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "queue_worker.py"


def _load():
    spec = importlib.util.spec_from_file_location("queue_worker_paper_path", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class JobPaperPathPersistenceTests(unittest.TestCase):
    def test_research_completion_persists_submission_paper_path(self):
        module = _load()
        job = {
            "job_id": "job-research-test",
            "type": "research",
            "status": "ready",
            "paper_path": None,
        }
        state = {"stats": {"research_completed": 0}, "maintenance": {}}
        submission = {
            "status": "completed",
            "paper_path": "papers/inference/test/persisted.md",
            "content": "日本語の検証本文です。" * 80,
            "_file": "work-queue/submissions/research/attempt-test.json",
        }

        module.process_research(submission, job, state)

        self.assertEqual(job["status"], "completed")
        self.assertEqual(job["paper_path"], submission["paper_path"])

    def test_audit_completion_persists_submission_paper_path(self):
        module = _load()
        job = {
            "job_id": "job-audit-test",
            "type": "audit",
            "status": "ready",
            "paper_path": None,
        }
        state = {"stats": {"audit_completed": 0}, "maintenance": {}}
        submission = {
            "status": "completed",
            "paper_path": "papers/inference/test/persisted.md",
            "content": "日本語の監査本文です。" * 80,
            "_file": "work-queue/submissions/audit/attempt-test.json",
        }

        module.process_audit(submission, job, state)

        self.assertEqual(job["status"], "completed")
        self.assertEqual(job["paper_path"], submission["paper_path"])


if __name__ == "__main__":
    unittest.main()
