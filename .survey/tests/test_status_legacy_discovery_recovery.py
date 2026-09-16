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
    spec = importlib.util.spec_from_file_location("render_status_dashboard_legacy_discovery_recovery", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_legacy_invalid_discovery(repo: Path) -> None:
    submission = "work-queue/submissions/discovery-specialist-legacy.json"
    _write_json(repo / ".survey" / submission, {
        "operation": "submit_discovery_round",
        "run_key": "2026-09-16T21:00:00+09:00",
        "candidates": [
            {
                "canonical_id": "arXiv:2606.24957",
                "title": "Dustin",
                "source_url": "https://arxiv.org/abs/2606.24957",
                "priority": 88,
                "reason": "legacy candidate",
            },
            {
                "canonical_id": "arXiv:2608.25062",
                "title": "FLINT",
                "source_url": "https://arxiv.org/abs/2608.25062",
                "priority": 90,
                "reason": "legacy candidate",
            },
        ],
        "discovery_stats": {
            "round": 2,
            "axis": "legacy-axis",
            "evaluated": 4,
            "submitted": 2,
        },
    })
    _write_json(repo / ".survey/work-queue/results/discovery-specialist-legacy.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "submission": submission,
        "ok": False,
        "error": "ValueError: invalid submit_discovery_round payload",
    })


def _write_research_job(repo: Path, canonical_id: str, suffix: str) -> None:
    _write_json(repo / f".survey/work-queue/jobs/job-research-{suffix}.json", {
        "job_id": f"job-research-{suffix}",
        "type": "research",
        "canonical_id": canonical_id,
        "title": suffix,
        "source_url": f"https://arxiv.org/abs/{canonical_id.split(':', 1)[1]}",
        "status": "ready",
    })


class StatusLegacyDiscoveryRecoveryTests(unittest.TestCase):
    def test_partially_recovered_invalid_legacy_round_remains_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_legacy_invalid_discovery(repo)
            _write_research_job(repo, "arXiv:2606.24957", "dustin")

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 17, 0, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **1** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **1** |", text)

    def test_fully_recovered_invalid_legacy_round_is_history_not_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_legacy_invalid_discovery(repo)
            _write_research_job(repo, "arXiv:2606.24957", "dustin")
            _write_research_job(repo, "arXiv:2608.25062", "flint")

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 17, 0, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **0** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **0** |", text)


if __name__ == "__main__":
    unittest.main()
