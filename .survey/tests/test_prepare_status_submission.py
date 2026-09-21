import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location("prepare_status_submission", SCRIPTS / "prepare_status_submission.py")
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class PrepareStatusSubmissionTests(unittest.TestCase):
    def test_strips_transport_fields_before_validation(self):
        draft = {
            "schema_version": 1,
            "transport_version": 10,
            "kind": "research",
            "attempt_id": "attempt-test",
            "job_id": "job-test",
            "status": "blocked",
            "reason": "primary source unavailable",
            "paper_path": "papers/inference/example.md",
            "record_bank": "a",
            "record_slots": [],
            "expected_blob_sha": "0" * 40,
        }
        with tempfile.TemporaryDirectory() as tmp:
            normalized, removed = module.prepare(Path(tmp), draft)
        self.assertEqual(
            removed,
            ["record_bank", "record_slots", "paper_path", "expected_blob_sha"],
        )
        self.assertEqual(normalized["status"], "blocked")
        for field in module.TRANSPORT_FIELDS:
            self.assertNotIn(field, normalized)

    def test_rejects_completed_descriptor(self):
        draft = {
            "schema_version": 1,
            "transport_version": 10,
            "kind": "research",
            "attempt_id": "attempt-test",
            "job_id": "job-test",
            "status": "completed",
            "reason": "not a status-only submission",
        }
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "only accepts"):
                module.prepare(Path(tmp), draft)


if __name__ == "__main__":
    unittest.main()
