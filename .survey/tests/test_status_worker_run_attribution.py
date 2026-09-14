import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "append_research_throughput_status.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("append_research_throughput_status", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkerRunAttributionTests(unittest.TestCase):
    def test_prefers_actual_worker_run_over_ledger_bucket(self):
        module = _load_module()
        claims = {
            "job-a": {"job_id": "job-a", "worker_id": "scheduled-chat-paper-20260914T0330JST"},
            "job-b": {"job_id": "job-b", "worker_id": "scheduled-chat-paper-20260914T0330JST"},
            "job-c": {"job_id": "job-c", "worker_id": "scheduled-chat-paper-20260914T0400JST"},
        }
        entries = [
            {
                "run_key": "2026-09-14T05:30:00+09:00",
                "counts": {"research_completed": 0},
                "terminal_transitions": [
                    {"job_id": "job-a", "type": "research", "to": "completed"},
                    {"job_id": "job-b", "type": "research", "to": "completed"},
                    {"job_id": "job-c", "type": "research", "to": "completed"},
                ],
            }
        ]
        run_key, completed = module._latest_normal_worker_run_metrics(entries, claims, {})
        self.assertEqual(run_key, "2026-09-14T03:30:00+09:00")
        self.assertEqual(completed, 2)

    def test_latest_normal_worker_run_can_have_zero_completions(self):
        module = _load_module()
        claims = {
            "job-old": {"job_id": "job-old", "worker_id": "scheduled-chat-paper-20260914T0330JST"},
            "job-new": {"job_id": "job-new", "worker_id": "scheduled-chat-paper-20260914T0430JST"},
        }
        entries = [
            {
                "run_key": "2026-09-14T05:30:00+09:00",
                "terminal_transitions": [
                    {"job_id": "job-old", "type": "research", "to": "completed"},
                ],
            }
        ]
        run_key, completed = module._latest_normal_worker_run_metrics(entries, claims, {})
        self.assertEqual(run_key, "2026-09-14T04:30:00+09:00")
        self.assertEqual(completed, 0)

    def test_0830_and_current_maintenance_slot_are_not_normal_runs(self):
        module = _load_module()
        claims = {
            "job-a": {"job_id": "job-a", "worker_id": "scheduled-chat-paper-20260914T0730JST"},
            "job-b": {"job_id": "job-b", "worker_id": "scheduled-chat-paper-20260914T0830JST"},
            "job-c": {"job_id": "job-c", "worker_id": "scheduled-chat-paper-20260914T0930JST"},
        }
        maintenance = {
            "runs_since_maintenance": 0,
            "last_counted_run_key": "2026-09-14T09:30:00+09:00",
        }
        run_key, completed = module._latest_normal_worker_run_metrics([], claims, maintenance)
        self.assertEqual(run_key, "2026-09-14T07:30:00+09:00")
        self.assertEqual(completed, 0)


if __name__ == "__main__":
    unittest.main()
