import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "append_research_throughput_status.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("append_research_throughput_status", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NormalRunSelectionTests(unittest.TestCase):
    def test_excludes_0830_special_slot(self):
        module = _load_module()
        entries = [
            {"run_key": "2026-09-14T07:30:00+09:00", "counts": {"research_completed": 3}},
            {"run_key": "2026-09-14T08:30:00+09:00", "counts": {"research_completed": 0}},
        ]
        latest = module._latest_normal_run(entries, {})
        self.assertEqual(latest["run_key"], "2026-09-14T07:30:00+09:00")
        self.assertEqual(latest["counts"]["research_completed"], 3)

    def test_excludes_current_maintenance_slot_at_any_hour(self):
        module = _load_module()
        entries = [
            {"run_key": "2026-09-14T05:30:00+09:00", "counts": {"research_completed": 4}},
            {"run_key": "2026-09-14T06:30:00+09:00", "counts": {"research_completed": 0}},
        ]
        maintenance = {
            "runs_since_maintenance": 0,
            "last_counted_run_key": "2026-09-14T06:30:00+09:00",
            "maintenance_pending": True,
        }
        latest = module._latest_normal_run(entries, maintenance)
        self.assertEqual(latest["run_key"], "2026-09-14T05:30:00+09:00")
        self.assertEqual(latest["counts"]["research_completed"], 4)

    def test_keeps_latest_ordinary_30_slot(self):
        module = _load_module()
        entries = [
            {"run_key": "2026-09-14T09:30:00+09:00", "counts": {"research_completed": 2}},
            {"run_key": "2026-09-14T10:30:00+09:00", "counts": {"research_completed": 5}},
        ]
        latest = module._latest_normal_run(entries, {"runs_since_maintenance": 1})
        self.assertEqual(latest["run_key"], "2026-09-14T10:30:00+09:00")
        self.assertEqual(latest["counts"]["research_completed"], 5)


if __name__ == "__main__":
    unittest.main()
