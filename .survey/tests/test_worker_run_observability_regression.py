import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402


def _load_refiner():
    path = SCRIPTS / "refine_status_observability.py"
    spec = importlib.util.spec_from_file_location("status_refiner_run_regression", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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

    def test_new_scheduled_chat_claim_persists_run_key_from_requested_at(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/jobs/job-r1.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-r1",
                "type": "research",
                "lane": "research",
                "status": "ready",
                "priority": 50,
                "created_at": "2026-09-15T00:00:00+00:00",
                "title": "job-r1",
                "paper_path": "papers/job-r1.md",
                "depends_on_job_ids": ["job-r1"],
            })
            _write(repo / ".survey/work-queue/claim-requests/req-r1.json", {
                "schema_version": 1,
                "request_id": "req-r1",
                "worker_id": "scheduled-chat-llm-survey-20260915T1830JST",
                "worker_kind": "scheduled_chat",
                "requested_at": "2026-09-15T00:34:00+00:00",
                "max_jobs": 1,
                "lease_seconds": 5400,
                "job_types": ["research", "audit"],
            })
            claim_worker.process_requests(
                repo,
                at=datetime(2026, 9, 15, 0, 34, tzinfo=timezone.utc),
            )
            claim = json.loads(
                (repo / ".survey/work-queue/claims/job-r1.json").read_text(encoding="utf-8")
            )
            self.assertEqual(claim["run_key"], "2026-09-15T09:30:00+09:00")


if __name__ == "__main__":
    unittest.main()
