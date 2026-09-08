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

COMMIT = "a" * 40


class BootstrapTests(unittest.TestCase):
    def make_root(self, tmp, next_run_index=2, active_claim=None):
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "survey-state/runs").mkdir(parents=True)
        source_cycle = Path(__file__).resolve().parents[1] / "scripts/cycle_state.py"
        (root / "scripts/cycle_state.py").write_text(source_cycle.read_text())
        state = {
            "schema_version": 1,
            "workflow_version": 8,
            "cycle_number": 1,
            "cycle_id": "cycle-000001",
            "max_runs": 24,
            "next_run_index": next_run_index,
            "active_claim": active_claim,
            "targets": {"research": 10, "audit": 10},
            "current_plan_id": None,
            "current_plan_path": None,
            "previous_cycle_id": None,
            "previous_plan_path": None,
        }
        (root / "survey-state/cycle-state.json").write_text(json.dumps(state))
        return root

    def call(self, root, run_id="r1", scheduled_at=None, morning_overlay=False, apply=True):
        mod = b.load_cycle(root)
        out = mod.claim(
            root,
            run_id,
            COMMIT,
            scheduled_at=scheduled_at,
            morning_overlay=morning_overlay,
            apply=apply,
        )
        out["control_source"] = "survey-state/cycle-state.json"
        out["time_controls_mode"] = False
        return out

    def test_run_1_is_planning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=1)
            result = self.call(root)
            self.assertEqual(result["mode"], "planning")
            self.assertEqual(result["run_index"], 1)

    def test_run_2_is_reading_and_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=2)
            result = self.call(root)
            self.assertEqual(result["mode"], "reading")
            run = json.loads((root / "survey-state/runs/r1.json").read_text())
            self.assertEqual(run["workflow_version"], 8)
            self.assertEqual(run["status"], "running")
            self.assertEqual(run["run_index"], 2)

    def test_run_24_is_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=24)
            result = self.call(root)
            self.assertEqual(result["mode"], "integrity")
            self.assertEqual(result["run_index"], 24)

    def test_scheduled_time_does_not_change_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=3)
            result = self.call(root, scheduled_at="2026-09-09T00:30:00+09:00")
            self.assertEqual(result["mode"], "reading")
            run = json.loads((root / "survey-state/runs/r1.json").read_text())
            self.assertEqual(run["scheduled_at"], "2026-09-09T00:30:00+09:00")

    def test_morning_overlay_does_not_change_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=5)
            result = self.call(root, morning_overlay=True)
            self.assertEqual(result["mode"], "reading")
            run = json.loads((root / "survey-state/runs/r1.json").read_text())
            self.assertEqual(run["overlays"], ["morning"])

    def test_active_claim_is_recovered_same_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = {
                "cycle_id": "cycle-000001",
                "run_index": 7,
                "run_id": "old-run",
                "claim_token": "old-token",
                "workflow_commit": "b" * 40,
            }
            root = self.make_root(tmp, next_run_index=8, active_claim=old)
            result = self.call(root, run_id="recovery")
            self.assertEqual(result["run_index"], 7)
            self.assertEqual(result["recovery_of"], "old-run")
            self.assertEqual(result["mode"], "reading")

    def test_existing_run_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=2)
            self.call(root)
            with self.assertRaisesRegex(ValueError, "run_id already exists"):
                self.call(root)

    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, next_run_index=2)
            result = self.call(root, apply=False)
            self.assertEqual(result["mode"], "reading")
            self.assertFalse((root / "survey-state/runs/r1.json").exists())
            state = json.loads((root / "survey-state/cycle-state.json").read_text())
            self.assertIsNone(state["active_claim"])


if __name__ == "__main__":
    unittest.main()
