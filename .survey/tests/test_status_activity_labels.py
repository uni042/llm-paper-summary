import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).parents[2]
THROUGHPUT_SCRIPT = ROOT / ".survey" / "scripts" / "append_research_throughput_status.py"
REFINER_SCRIPT = ROOT / ".survey" / "scripts" / "refine_status_observability.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


class StatusActivityLabelTests(unittest.TestCase):
    def test_heartbeat_activity_is_not_labeled_as_a_new_claim(self):
        throughput = _load(THROUGHPUT_SCRIPT, "status_throughput_activity_label")
        refiner = _load(REFINER_SCRIPT, "status_refiner_activity_label")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 1}},
                "claiming": {"ready_research_audit": 1, "actively_claimed": 1, "claimable": 0},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            _write(repo / ".survey/work-queue/jobs/job-normal.json", {
                "job_id": "job-normal",
                "type": "research",
                "status": "ready",
            })
            _write(repo / ".survey/work-queue/claims/job-normal.json", {
                "job_id": "job-normal",
                "worker_id": "scheduled-chat-llm-survey-20260914T1730JST",
                "claimed_at": "2026-09-14T08:35:00+00:00",
                "heartbeat_at": "2026-09-14T09:33:00+00:00",
                "expires_at": "2026-09-14T10:30:00+00:00",
            })

            now = datetime(2026, 9, 14, 10, 0, tzinfo=timezone.utc)
            text = refiner.refine_text(repo, throughput.render_section(repo, now=now), now=now)

            self.assertIn(":30 最新worker run | **2026-09-14T17:30:00+09:00**", text)
            self.assertIn(":30 通常worker 直近lease活動 | **09-14 18:33 JST**", text)
            self.assertNotIn(":30 通常worker 直近claim |", text)

    def test_consistency_result_shows_when_it_was_last_checked(self):
        refiner = _load(REFINER_SCRIPT, "status_refiner_consistency_timestamp")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "last_consistency_status": "passed",
                "last_consistency_checked_at": "2026-09-14T00:53:22+00:00",
            })
            text = (
                "## 現在の状態\n\n"
                "| 指標 | 状態 |\n"
                "|---|---:|\n"
                "| 整合性チェック（Consistency） | **passed** |\n"
            )

            refined = refiner.refine_text(
                repo,
                text,
                now=datetime(2026, 9, 14, 10, 0, tzinfo=timezone.utc),
            )

            self.assertIn("直近整合性チェック結果 | **passed**", refined)
            self.assertIn("直近整合性チェック時刻 | **09-14 09:53 JST**", refined)
            self.assertNotIn("整合性チェック（Consistency）", refined)


if __name__ == "__main__":
    unittest.main()
