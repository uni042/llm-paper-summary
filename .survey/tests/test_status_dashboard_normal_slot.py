import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _load(repo: Path):
    dst = repo / ".survey/scripts/build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("build_status_dashboard_normal_slot", dst)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StatusDashboardNormalSlotTests(unittest.TestCase):
    def test_base_dashboard_does_not_render_ledger_based_normal_run_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 10, "ready": 100, "blocked": 0, "deferred": 0}},
                "next_jobs": [],
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "cadence_runs": 24,
                "runs_since_maintenance": 7,
                "maintenance_pending": False,
                "last_maintenance_status": "passed",
                "last_consistency_status": "passed",
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {
                    "run_key": "2026-09-14T07:30:00+09:00",
                    "counts": {"research_completed": 3, "audit_completed": 0, "discovery_completed": 0, "blocked": 0, "new_jobs": 0, "new_papers": 3, "fallback_archived": 0},
                    "terminal_transitions": [],
                    "new_jobs": [],
                    "new_paper_ids": ["a", "b", "c"],
                },
                {
                    "run_key": "2026-09-14T08:30:00+09:00",
                    "counts": {"research_completed": 5, "audit_completed": 0, "discovery_completed": 0, "blocked": 0, "new_jobs": 0, "new_papers": 5, "fallback_archived": 0},
                    "terminal_transitions": [],
                    "new_jobs": [],
                    "new_paper_ids": ["d", "e", "f", "g", "h"],
                },
            ]})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": []})

            module = _load(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 14, 2, 0, tzinfo=timezone.utc))

            self.assertNotIn("## 直近の通常worker", text)
            self.assertIn("## 直近24時間の処理量", text)
            self.assertIn("Research完了 | **8**", text)
            self.assertIn("## 次に処理する候補", text)


if __name__ == "__main__":
    unittest.main()
