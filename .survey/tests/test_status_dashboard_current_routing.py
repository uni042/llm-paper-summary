import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"


def _load_module(repo_root: Path):
    path = repo_root / ".survey" / "scripts" / "build_status_dashboard.py"
    spec = importlib.util.spec_from_file_location("build_status_dashboard_current", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


class StatusDashboardCurrentRoutingTests(unittest.TestCase):
    def test_dashboard_uses_dual_mode_auxiliary_worker_labels(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            script = repo / ".survey/scripts/build_status_dashboard.py"
            script.parent.mkdir(parents=True, exist_ok=True)
            script.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 10, "ready": 60, "blocked": 0, "deferred": 0}},
                "next_jobs": [],
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "cadence_runs": 24,
                "runs_since_maintenance": 3,
                "maintenance_pending": False,
                "last_maintenance_status": "passed",
                "last_consistency_status": "passed",
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": [
                {"run_key": "2026-09-14T08:00:00+09:00", "round": "specialist-r1", "axis": "SSD", "candidate_count": 3, "duplicate_filtered_count": 1, "novel_candidate_count": 2, "accepted_count": 2},
            ]})

            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 13, 23, 30, tzinfo=timezone.utc))

            self.assertIn("保守カウンタ（通常run） | **3 / 24**", text)
            self.assertIn(":00 補助worker Discovery run（毎時枠）", text)
            self.assertIn(":00 補助worker Discovery round（stats観測）", text)
            self.assertIn("### 直近の:00 補助worker Discovery", text)
            self.assertIn("### :00 補助workerのDiscovery効率（直近24時間）", text)
            self.assertIn("### 直近5件の:00 補助worker Discovery run", text)
            self.assertNotIn("探索専用worker", text)


if __name__ == "__main__":
    unittest.main()
