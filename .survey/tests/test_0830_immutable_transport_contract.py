import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
UPDATE_WORKFLOW = ROOT / ".github" / "workflows" / "update-helper.yml"
MAINTENANCE_WORKFLOW = ROOT / ".github" / "workflows" / "maintenance.yml"
ROUTER = ROOT / ".survey" / "docs" / "survey-workflow" / "worker-router.md"


class ScheduledImmutableTransportContractTests(unittest.TestCase):
    def test_update_helper_is_triggered_by_create_only_requests(self):
        text = UPDATE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(".survey/update-worker/requests/**.json", text)
        self.assertNotIn(
            "- '.survey/update-worker/update-inbox.json'",
            text,
        )

    def test_maintenance_is_triggered_by_create_only_requests(self):
        text = MAINTENANCE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(".survey/work-queue/maintenance-requests/**.json", text)
        self.assertNotIn(
            "- '.survey/work-queue/maintenance-cycle.json'",
            text,
        )
        self.assertIn("maintenance-results", text)

    def test_router_forbids_scheduled_chat_mutable_control_writes(self):
        text = ROUTER.read_text(encoding="utf-8")
        section = text[text.index("## 9. 08:30更新とmaintenance"):]
        self.assertIn(".survey/update-worker/requests/<attempt_id>.json", section)
        self.assertIn(".survey/work-queue/maintenance-requests/<request_id>.json", section)
        self.assertIn("既存制御ファイルを update しない", section)


if __name__ == "__main__":
    unittest.main()
