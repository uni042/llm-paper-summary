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
    spec = importlib.util.spec_from_file_location("status_library_first_activity", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LibraryFirstStatusTests(unittest.TestCase):
    def test_current_compact_run_keys_drive_status_and_current_activity_section(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_json(
                repo / ".survey/import-inbox/results/research/research.json",
                {
                    "artifact_type": "research",
                    "status": "imported",
                    "canonical_id": "arXiv:2609.99999",
                    "worker_completed_at": "2026-10-03T14:40:00+09:00",
                    "worker_run_key": "20261003-1440-scheduled-chat-30",
                    "processed_at": "2026-10-03T05:45:00+00:00",
                },
            )
            _write_json(
                repo / ".survey/import-inbox/results/discovery/discovery.json",
                {
                    "artifact_type": "discovery",
                    "status": "imported",
                    "processed_at": "2026-10-03T05:50:00+00:00",
                    "record_count": 10,
                    "run_key": "20261003-1445-scheduled-chat-45",
                    "worker_id": "scheduled-chat-45",
                    "accept_count": 2,
                    "relevance_count": 8,
                },
            )

            text = _load_renderer().build_dashboard(
                repo,
                now=datetime(2026, 10, 3, 6, 0, tzinfo=timezone.utc),
            )

            self.assertIn("| 最終Research処理完了 | **10-03 14:40:00 JST** |", text)
            self.assertIn("| 最終Discovery探索完了 | **10-03 14:45:00 JST** |", text)
            self.assertIn("## Library-first稼働状況", text)
            self.assertIn("| 直近6hのResearch完了 | **1** |", text)
            self.assertIn("| 直近6hのDiscovery run | **1** |", text)
            self.assertIn("| 直近6hのDiscovery本文確認・分類 | **10** |", text)
            self.assertIn("run 20261003-1445-scheduled-chat-45", text)
            self.assertIn("## 件数サマリー（旧immutable transport診断）", text)
            self.assertIn("## 詳細証拠（旧immutable transport）", text)


if __name__ == "__main__":
    unittest.main()
