import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reconcile_maintenance_state.py"


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ReconcileMaintenanceStateTests(unittest.TestCase):
    def test_health_error_prevents_newer_consistency_pass_from_marking_overall_passed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/maintenance-cycle.json", {
                "schema_version": 1,
                "last_maintenance_status": "issues_found",
                "last_maintenance_status_source": "maintenance_workflow",
                "last_consistency_status": "issues_found",
                "last_consistency_checked_at": "2026-09-13T00:00:00+00:00",
                "last_health_status": "issues_found",
                "last_health_checked_at": "2026-09-13T00:05:00+00:00",
                "last_health_errors": 1,
                "last_health_warnings": 0,
            })
            write_json(root / ".survey/reports/consistency-latest.json", {
                "schema_version": 3,
                "checked_at": "2026-09-13T01:00:00+00:00",
                "status": "passed",
            })
            write_json(root / ".survey/reports/maintenance-health-latest.json", {
                "schema_version": 1,
                "checked_at": "2026-09-13T00:30:00+00:00",
                "status": "issues_found",
                "error_count": 2,
                "warning_count": 3,
            })

            subprocess.run(
                [sys.executable, str(SCRIPT), "--repo-root", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            state = json.loads((root / ".survey/work-queue/maintenance-cycle.json").read_text())

            self.assertEqual(state["last_consistency_status"], "passed")
            self.assertEqual(state["last_health_status"], "issues_found")
            self.assertEqual(state["last_health_errors"], 2)
            self.assertEqual(state["last_health_warnings"], 3)
            self.assertEqual(state["last_maintenance_status"], "issues_found")
            self.assertEqual(state["last_maintenance_status_source"], "reconciled_reports")

    def test_overall_status_returns_to_passed_only_when_consistency_and_health_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/maintenance-cycle.json", {
                "schema_version": 1,
                "last_maintenance_status": "issues_found",
                "last_consistency_status": "passed",
                "last_consistency_checked_at": "2026-09-13T01:00:00+00:00",
                "last_health_status": "issues_found",
                "last_health_checked_at": "2026-09-13T00:30:00+00:00",
                "last_health_errors": 2,
                "last_health_warnings": 3,
            })
            write_json(root / ".survey/reports/maintenance-health-latest.json", {
                "schema_version": 1,
                "checked_at": "2026-09-13T01:30:00+00:00",
                "status": "passed",
                "error_count": 0,
                "warning_count": 0,
            })

            subprocess.run(
                [sys.executable, str(SCRIPT), "--repo-root", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            state = json.loads((root / ".survey/work-queue/maintenance-cycle.json").read_text())

            self.assertEqual(state["last_health_status"], "passed")
            self.assertEqual(state["last_maintenance_status"], "passed")
            self.assertEqual(state["last_maintenance_status_source"], "reconciled_reports")


if __name__ == "__main__":
    unittest.main()
