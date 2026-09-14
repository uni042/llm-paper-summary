import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "append_research_throughput_status.py"


def _load_module(repo_root: Path):
    path = repo_root / ".survey" / "scripts" / "append_research_throughput_status.py"
    spec = importlib.util.spec_from_file_location("append_research_throughput_status", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


class ResearchRunDashboardAttributionTests(unittest.TestCase):
    def test_async_completion_is_attributed_to_claim_worker_run(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            dst = repo / ".survey/scripts/append_research_throughput_status.py"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")

            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 100}},
                "claiming": {"actively_claimed": 0, "claimable": 100},
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "runs_since_maintenance": 4,
                "last_counted_run_key": "2026-09-14T08:30:00+09:00",
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {
                    "run_key": "2026-09-14T08:30:00+09:00",
                    "counts": {"research_completed": 1},
                    "terminal_transitions": [
                        {"job_id": "job-r1", "type": "research", "to": "completed"},
                    ],
                },
            ]})
            _write(repo / ".survey/work-queue/claims/job-r1.json", {
                "job_id": "job-r1",
                "worker_id": "scheduled-chat-paper-20260914T0730JST",
                "claimed_at": "2026-09-13T22:36:00+00:00",
                "expires_at": "2026-09-13T22:50:00+00:00",
            })

            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 14, 0, 40, tzinfo=timezone.utc))

            self.assertIn("最新通常run | **2026-09-14T07:30:00+09:00**", text)
            self.assertIn("最新通常runのResearch完了 | **1**", text)
            self.assertNotIn("最新通常run | **2026-09-14T08:30:00+09:00**", text)


if __name__ == "__main__":
    unittest.main()
