import unittest
from pathlib import Path


WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "maintenance.yml"


class MaintenanceLatestMainSyncTests(unittest.TestCase):
    def test_maintenance_syncs_latest_main_before_request_selection(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        sync = "- name: Sync latest main before maintenance"
        pending = "- name: Select pending immutable maintenance request"
        self.assertIn(sync, text)
        self.assertLess(text.index(sync), text.index(pending))
        self.assertIn("git fetch origin main", text[text.index(sync):text.index(pending)])
        self.assertIn("git reset --hard origin/main", text[text.index(sync):text.index(pending)])


if __name__ == "__main__":
    unittest.main()
