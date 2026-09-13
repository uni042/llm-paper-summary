import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "process_immutable_submission.py"
QUEUE_SCRIPT = Path(__file__).parents[1] / "scripts" / "queue_worker.py"


def _load(path=SCRIPT, name="immutable_repair_cleanup"):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepairStateCleanupTests(unittest.TestCase):
    def test_successful_retry_clears_stale_validation_repair_state(self):
        module = _load()
        job = {
            "job_id": "job-test",
            "type": "research",
            "status": "completed",
            "repair_required": True,
            "validation_error": "ValueError: old validation failure",
            "last_validation_failed_at": "2026-09-13T00:00:00+00:00",
        }

        module._clear_repair_state(job)

        self.assertNotIn("repair_required", job)
        self.assertNotIn("validation_error", job)
        self.assertNotIn("last_validation_failed_at", job)

    def test_reusable_research_success_clears_stale_validation_repair_state(self):
        module = _load(QUEUE_SCRIPT, "queue_worker_repair_cleanup")
        job = {
            "job_id": "job-test",
            "type": "research",
            "status": "ready",
            "repair_required": True,
            "validation_error": "ValueError: old validation failure",
            "last_validation_failed_at": "2026-09-13T00:00:00+00:00",
        }
        state = {
            "stats": {"research_completed": 0},
            "maintenance": {},
        }
        submission = {
            "status": "completed",
            "content": "あ" * 600,
            "_file": "work-queue/submissions/chat-inbox.json",
        }

        module.process_research(submission, job, state)

        self.assertEqual(job["status"], "completed")
        self.assertNotIn("repair_required", job)
        self.assertNotIn("validation_error", job)
        self.assertNotIn("last_validation_failed_at", job)


if __name__ == "__main__":
    unittest.main()
