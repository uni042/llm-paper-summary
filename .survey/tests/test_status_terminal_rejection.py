import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_status_dashboard_terminal_rejection", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_orphan_submission(repo: Path, *, retryable: bool, failure_class: str = "content_validation", error: str = "ValueError: unknown job_id: job-never-existed") -> None:
    submission = ".survey/work-queue/submissions/research/attempt-orphan.json"
    _write_json(repo / submission, {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "attempt_id": "attempt-orphan",
        "job_id": "job-never-existed",
        "worker_id": "scheduled-chat-paper-20260916T173214JST",
    })
    _write_json(repo / ".survey/work-queue/results/research/attempt-orphan.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": False,
        "attempt_id": "attempt-orphan",
        "job_id": "job-never-existed",
        "job_type": "research",
        "job_status": None,
        "artifact": None,
        "submission": submission,
        "error": error,
        "processed_at": "2026-09-16T08:38:13+00:00",
        "failure_class": failure_class,
        "retryable": retryable,
    })


class StatusTerminalRejectionTests(unittest.TestCase):
    def test_terminally_rejected_orphan_submission_is_history_not_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_orphan_submission(repo, retryable=False)

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **0** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **0** |", text)

    def test_terminal_stale_job_guard_is_history_not_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_orphan_submission(
                repo,
                retryable=False,
                failure_class="state_or_transport_guard",
            )

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **0** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **0** |", text)

    def test_nonmatching_transport_guard_remains_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_orphan_submission(
                repo,
                retryable=False,
                failure_class="state_or_transport_guard",
                error="ValueError: stale attempt: claim mismatch",
            )

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **1** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **1** |", text)

    def test_retryable_orphan_submission_remains_current_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_orphan_submission(repo, retryable=True)

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 整合性異常 | **1** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **1** |", text)


if __name__ == "__main__":
    unittest.main()
