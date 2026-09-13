import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "queue_worker.py"


def _load():
    spec = importlib.util.spec_from_file_location("queue_worker_repair_cleanup", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepairStateCleanupTests(unittest.TestCase):
    def test_completed_research_clears_stale_validation_repair_state(self):
        module = _load()
        job = {
            "job_id": "job-test",
            "type": "research",
            "status": "ready",
            "repair_required": True,
            "validation_error": "ValueError: old validation failure",
            "last_validation_failed_at": "2026-09-13T00:00:00+00:00",
        }
        sub = {
            "status": "completed",
            "content": "あ" * 600,
            "_file": "work-queue/submissions/test.json",
        }
        state = {
            "stats": {"research_completed": 0},
            "maintenance": {},
        }

        module.process_research(sub, job, state)

        self.assertEqual(job["status"], "completed")
        self.assertNotIn("repair_required", job)
        self.assertNotIn("validation_error", job)
        self.assertNotIn("last_validation_failed_at", job)


if __name__ == "__main__":
    unittest.main()
