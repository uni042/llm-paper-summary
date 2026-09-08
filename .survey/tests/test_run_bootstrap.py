import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "run_bootstrap", Path(__file__).resolve().parents[1] / "scripts/run_bootstrap.py"
)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

AT = "2026-09-08T10:30:00+09:00"
START = "2026-09-08T10:30:02+09:00"
COMMIT = "a" * 40


class BootstrapTests(unittest.TestCase):
    def make_root(self, tmp, plan_status="ready"):
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "survey-state/daily-plans").mkdir(parents=True)
        source_survey = Path(__file__).resolve().parents[1] / "scripts/survey.py"
        (root / "scripts/survey.py").write_text(source_survey.read_text())
        layout = {
            "schema_version": 1,
            "workflow_version": 7,
            "paths": {
                "runtime": "survey-state/runtime.json",
                "leases": "survey-state/leases.json",
                "runs_dir": "survey-state/runs/",
            },
        }
        (root / "survey-state/state-layout.json").write_text(json.dumps(layout))
        plan_path = "survey-state/daily-plans/2026-09-08.json"
        runtime = {"current_plan_id": "day", "current_plan_path": plan_path}
        (root / "survey-state/runtime.json").write_text(json.dumps(runtime))
        plan = {
            "plan_id": "day",
            "period_start": "2026-09-08T09:30:00+09:00",
            "status": plan_status,
        }
        (root / plan_path).write_text(json.dumps(plan))
        (root / "survey-state/leases.json").write_text(
            json.dumps({"schema_version": 1, "items": {}})
        )
        return root

    def call(self, root, **overrides):
        args = dict(
            root=root,
            run_id="r1",
            scheduled_at=AT,
            started_at=START,
            workflow_commit=COMMIT,
            nightly_hour=0,
            morning_hour=8,
            morning_minute=30,
            planning_hour=9,
            planning_minute=30,
            period_start="2026-09-08T09:30:00+09:00",
            github_read="true",
            github_write="true",
            apply=True,
        )
        args.update(overrides)
        return b.prepare_bootstrap(**args)

    def test_reading_run_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            result = self.call(root)
            self.assertEqual(result["mode"], "reading")
            self.assertEqual(result["route"], "reading")
            run = json.loads((root / "survey-state/runs/r1.json").read_text())
            self.assertEqual(run["workflow_version"], 7)
            self.assertEqual(run["status"], "running")
            self.assertTrue(run["capabilities"]["github_write"])

    def test_nightly_auto_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            result = self.call(
                root,
                scheduled_at="2026-09-09T00:30:00+09:00",
                started_at="2026-09-09T00:30:01+09:00",
                period_start=None,
                auto_lease=True,
            )
            self.assertEqual(result["mode"], "nightly")
            self.assertEqual(result["lease_resource"], "maintenance")
            leases = json.loads((root / "survey-state/leases.json").read_text())
            self.assertEqual(leases["items"]["maintenance"]["run_id"], "r1")

    def test_recovery_auto_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, plan_status="selecting")
            result = self.call(root, auto_lease=True)
            self.assertEqual(result["route"], "recover_planning")
            self.assertEqual(
                result["lease_resource"],
                "planning:2026-09-08T09:30:00+09:00",
            )

    def test_existing_run_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            self.call(root)
            with self.assertRaisesRegex(ValueError, "Run ID already exists"):
                self.call(root)

    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            result = self.call(root, apply=False)
            self.assertEqual(result["result"], "preview")
            self.assertFalse((root / "survey-state/runs/r1.json").exists())


if __name__ == "__main__":
    unittest.main()
