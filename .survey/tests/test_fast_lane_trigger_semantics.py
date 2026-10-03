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

    def test_claim_fast_is_manual_only_under_library_first(self):
        text = (ROOT / ".github/workflows/survey-claim-fast.yml").read_text(encoding="utf-8")
        trigger = text.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("push:", trigger)
        self.assertNotIn("schedule:", trigger)

    def test_library_import_kick_is_manual_only_and_orchestrator_owns_kick(self):
        legacy = (ROOT / ".github/workflows/library-import-kick.yml").read_text(encoding="utf-8")
        legacy_trigger = legacy.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", legacy_trigger)
        self.assertNotIn("push:", legacy_trigger)

        orchestrator = (ROOT / ".github/workflows/survey-orchestrator.yml").read_text(encoding="utf-8")
        trigger = orchestrator.split("permissions:", 1)[0]
        self.assertIn(".survey/scheduler/library-import-kick.json", trigger)
        self.assertIn("dispatch_if_idle library-import.yml", orchestrator)

    def test_submission_fast_is_manual_only(self):
        text = (ROOT / ".github/workflows/survey-submission-fast.yml").read_text(encoding="utf-8")
        trigger = text.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("push:", trigger)
        self.assertNotIn("schedule:", trigger)

    def test_survey_helper_routes_record_fallback_to_immutable_replay(self):
        text = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertIn("replay_record_fallback.py", text)
        self.assertIn("dispatch_fallback_inbox.py", text)
        self.assertNotIn("chat-inbox.json", text)
        self.assertNotIn("preflight_chat_record.py", text)
        self.assertNotIn("reusable_transport_baseline.py", text)


if __name__ == "__main__":
    unittest.main()
