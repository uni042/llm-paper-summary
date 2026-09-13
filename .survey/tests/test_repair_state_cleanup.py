import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "process_immutable_submission.py"


def _load():
    spec = importlib.util.spec_from_file_location("immutable_repair_cleanup", SCRIPT)
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


if __name__ == "__main__":
    unittest.main()
