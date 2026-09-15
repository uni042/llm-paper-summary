import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_refiner():
    return _load(SCRIPTS / "refine_status_observability.py", "status_refiner_run_regression")


def _load_throughput():
    return _load(SCRIPTS / "append_research_throughput_status.py", "status_throughput_run_regression")


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class WorkerRunObservabilityRegressionTests(unittest.TestCase):
    def test_future_embedded_worker_stamp_falls_back_to_claim_slot(self):
        refiner = _load_refiner()
        claim = {
            "worker_id": "scheduled-chat-llm-survey-20260915T1830JST",
            "worker_kind": "scheduled_chat",
            "claimed_at": "2026-09-15T00:34:00+00:00",
        }
        self.assertEqual(
            refiner._claim_run_key(claim),
            "2026-09-15T09:30:00+09:00",
        )

    def test_throughput_attribution_rejects_same_future_worker_stamp(self):
        throughput = _load_throughput()
        claim = {
            "worker_id": "scheduled-chat-llm-survey-20260915T1830JST",
            "worker_kind": "scheduled_chat",
            "claimed_at": "2026-09-15T00:34:00+00:00",
        }
        self.assertEqual(
            throughput._claim_run_key(claim),
            "2026-09-15T09:30:00+09:00",
        )

    def test_aux_latest_run_comes_from_discovery_state_without_active_research_lease(self):
        refiner = _load_refiner()
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/discovery-state.json", {
                "last_run_key": "2026-09-15T10:00:00+09:00",
                "history": [],
            })
            metrics = refiner.worker_observability(
                repo,
                now=datetime(2026, 9, 15, 1, 27, tzinfo=timezone.utc),
            )
            self.assertEqual(metrics["aux"]["latest_run"], "2026-09-15T10:00:00+09:00")
            self.assertEqual(metrics["aux"]["latest_count"], 0)
            self.assertEqual(metrics["aux"]["old_count"], 0)


if __name__ == "__main__":
    unittest.main()
