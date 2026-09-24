import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"
SCRIPT_DIR = SCRIPT.parent


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _load_renderer():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location("render_status_dashboard_self_describing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _self_describing_round(repo: Path, *, include_explicit_submission: bool = True) -> str:
    job_id = "job-discovery-ingest-self-describing"
    submission = ".survey/work-queue/submissions/discovery-specialist-20260917T0001-self-describing.json"
    result = ".survey/work-queue/results/discovery/discovery-specialist-20260917T0001-self-describing.json"

    _write_json(repo / f".survey/work-queue/jobs/{job_id}.json", {
        "job_id": job_id,
        "type": "discovery",
        "status": "completed",
        "completed_at": "2026-09-16T15:05:00+00:00",
    })
    _write_json(repo / submission, {
        "operation": "submit_discovery_round",
        "worker_id": "scheduled-chat-discovery-20260917T0000JST",
        "candidates": [{"canonical_id": "arXiv:2609.99999"}],
        "discovery_stats": {
            "run_key": "2026-09-17T00:00:00+09:00",
            "round": "specialist-self-describing-1",
            "axis": "self-describing discovery",
            "candidate_count": 1,
        },
    })
    result_payload = {
        "ok": True,
        "job_id": job_id,
        "job_type": "discovery",
        "job_status": "completed",
        "processed_at": "2026-09-16T15:05:00+00:00",
    }
    if include_explicit_submission:
        result_payload["submission"] = "work-queue/submissions/discovery-specialist-20260917T0001-self-describing.json"
    _write_json(repo / result, result_payload)
    return submission


class StatusSelfDescribingDiscoveryTests(unittest.TestCase):
    def test_explicit_self_describing_round_is_verified_without_submission_job_id(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _self_describing_round(repo)

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 15, 10, tzinfo=timezone.utc),
            )

            self.assertIn("検証済み成功result: **1件**", text)
            self.assertIn("個別result未照合: **0件**", text)

    def test_self_describing_round_without_explicit_submission_is_not_guessed_from_internal_job(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _self_describing_round(repo, include_explicit_submission=False)

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 15, 10, tzinfo=timezone.utc),
            )

            self.assertIn("検証済み成功result: **0件**", text)
            self.assertIn("個別result未照合: **1件**", text)


if __name__ == "__main__":
    unittest.main()
