import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import select_record_bank  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class FastLaneTriggerSemanticsTests(unittest.TestCase):
    def test_failed_immutable_result_still_owns_pending_bank(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
            }
            write_json(root / ".survey/work-queue/submissions/research/attempt-a.json", descriptor)
            result = root / ".survey/work-queue/results/research/attempt-a.json"
            write_json(result, {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "attempt_id": "attempt-a",
                "job_id": "job-a",
            })

            self.assertEqual(
                select_record_bank.pending_immutable_bank_owners(root),
                {"a": {("attempt-a", "job-a")}},
            )

            write_json(result, {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": True,
                "attempt_id": "attempt-a",
                "job_id": "job-a",
            })
            self.assertEqual(select_record_bank.pending_immutable_bank_owners(root), {})

    def test_claim_fast_push_trigger_is_request_only(self):
        text = (ROOT / ".github/workflows/survey-claim-fast.yml").read_text(encoding="utf-8")
        trigger = text.split("  workflow_dispatch:", 1)[0]
        self.assertIn(".survey/work-queue/claim-requests/*.json", trigger)
        self.assertNotIn(".survey/scripts/", trigger)
        self.assertNotIn(".github/workflows/survey-claim-fast.yml", trigger)

    def test_submission_fast_push_trigger_is_descriptor_only(self):
        text = (ROOT / ".github/workflows/survey-submission-fast.yml").read_text(encoding="utf-8")
        trigger = text.split("  workflow_dispatch:", 1)[0]
        self.assertIn(".survey/work-queue/submissions/research/*.json", trigger)
        self.assertIn(".survey/work-queue/submissions/audit/*.json", trigger)
        self.assertNotIn(".survey/scripts/", trigger)
        self.assertNotIn(".github/workflows/survey-submission-fast.yml", trigger)

    def test_survey_helper_routes_record_fallback_to_immutable_replay(self):
        text = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertIn("replay_record_fallback.py", text)
        self.assertIn("dispatch_fallback_inbox.py", text)
        self.assertNotIn("chat-inbox.json", text)
        self.assertNotIn("preflight_chat_record.py", text)
        self.assertNotIn("reusable_transport_baseline.py", text)


if __name__ == "__main__":
    unittest.main()
