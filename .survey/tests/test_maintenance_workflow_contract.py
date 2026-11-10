import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "maintenance.yml"


class MaintenanceWorkflowContractTests(unittest.TestCase):
    def test_metadata_coverage_findings_do_not_abort_remaining_maintenance(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        start = text.index("      - name: Refresh metadata coverage")
        end = text.index("      - name: Audit queue, state, quality regressions, and report freshness", start)
        step = text[start:end]
        self.assertIn("--strict", step)
        self.assertIn("continue-on-error: true", step)


if __name__ == "__main__":
    unittest.main()
