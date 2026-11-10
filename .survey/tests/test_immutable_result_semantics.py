import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402
import immutable_submission  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ImmutableResultSemanticsTests(unittest.TestCase):
    def test_shared_success_predicate_requires_matching_identity_and_ok_true(self):
        descriptor = {"job_id": "job-a", "attempt_id": "attempt-a"}
        self.assertFalse(immutable_submission.result_is_success_for({}, descriptor))
        self.assertFalse(immutable_submission.result_is_success_for({
            "ok": False, "job_id": "job-a", "attempt_id": "attempt-a",
        }, descriptor))
        self.assertFalse(immutable_submission.result_is_success_for({
            "ok": True, "job_id": "job-b", "attempt_id": "attempt-a",
        }, descriptor))
        self.assertTrue(immutable_submission.result_is_success_for({
            "ok": True, "job_id": "job-a", "attempt_id": "attempt-a",
        }, descriptor))

    def test_claim_pending_set_agrees_with_shared_success_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "record_bank": "a",
            }
            submission = root / ".survey/work-queue/submissions/research/attempt-a.json"
            result = root / ".survey/work-queue/results/research/attempt-a.json"
            write_json(submission, descriptor)

            write_json(result, {"ok": False, "job_id": "job-a", "attempt_id": "attempt-a"})
            self.assertFalse(immutable_submission.result_is_success_for(json.loads(result.read_text()), descriptor))
            self.assertEqual(len(claim_worker._immutable_descriptors(root)), 1)

            write_json(result, {"ok": True, "job_id": "job-a", "attempt_id": "attempt-a"})
            self.assertTrue(immutable_submission.result_is_success_for(json.loads(result.read_text()), descriptor))
            self.assertEqual(claim_worker._immutable_descriptors(root), [])


if __name__ == "__main__":
    unittest.main()
