import unittest
from pathlib import Path


WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "status-dashboard.yml"


class StatusDashboardMergePublishTests(unittest.TestCase):
    def test_publish_gate_expands_merge_commit_parents(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('git diff-tree --no-commit-id --name-only -r -m "$TRIGGER_SHA"', text)


if __name__ == "__main__":
    unittest.main()
