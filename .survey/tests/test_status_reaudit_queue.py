"""Regression coverage for the STATUS re-audit figures derived from queue entries."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".survey/scripts"))
import render_status_dashboard_core as status  # noqa: E402


class StatusReauditQueueTests(unittest.TestCase):
    def _queue(self, root: Path, entries, **overrides):
        target = root / status.REAUDIT_QUEUE_PATH
        target.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "queue_kind": "under_16kb_semantic_reaudit",
            "queue_version": "2026-10-07-v1",
            "generated_at": "2026-10-08T00:00:00+09:00",
            "count": 9999,  # intentionally stale; must never drive STATUS
            "worker_counts": {"scheduled-chat-00": 9999},
            "entries": entries,
        }
        data.update(overrides)
        target.write_text(json.dumps(data), encoding="utf-8")

    @staticmethod
    def _item(n, worker="scheduled-chat-00", mechanical="FAIL"):
        return {
            "path": f"papers/inference/paper-{n}.md",
            "semantic_status": "pending",
            "mechanical_status": mechanical,
            "assigned_worker": worker,
        }

    def test_counts_are_computed_from_entries_not_queue_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._queue(root, [
                self._item(1),
                self._item(2, "scheduled-chat-30", "PASS"),
                self._item(3, "scheduled-chat-45", "WARN"),
            ])
            result = status._reaudit_queue_summary(root)
            self.assertTrue(result["available"])
            self.assertEqual(result["remaining"], 3)
            self.assertEqual(result["by_worker"], {
                "scheduled-chat-00": 1,
                "scheduled-chat-30": 1,
                "scheduled-chat-45": 1,
            })
            self.assertEqual(result["by_mechanical"], {
                "FAIL": 1, "PASS": 1, "WARN": 1
            })
            self.assertTrue(result["cached_count_mismatch"])
            rendered = "\n".join(status._render_reaudit_queue(result))
            self.assertIn("| **再監査残件数** | **3** |", rendered)
            self.assertIn("| 機械検査適合・警告のみ（PASS/WARN） | **2** |", rendered)
            self.assertIn("| :45ワーカー担当残 | **1** |", rendered)
            self.assertIn("待機リスト単独では算出できません", rendered)

    def test_unavailable_queue_does_not_report_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = status._reaudit_queue_summary(Path(tmp))
            self.assertFalse(result["available"])
            section = "\n".join(status._render_reaudit_queue(result))
            self.assertIn("残件数を取得できません", section)
            self.assertNotIn("| **再監査残件数** | **0** |", section)

    def test_duplicate_or_nonpending_rows_refuse_unreliable_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = self._item(1)
            self._queue(root, [entry, dict(entry)])
            self.assertFalse(status._reaudit_queue_summary(root)["available"])
            self._queue(root, [dict(entry, semantic_status="passed")])
            self.assertFalse(status._reaudit_queue_summary(root)["available"])

    def test_queue_changes_trigger_dashboard_workflow(self):
        workflow = (ROOT / ".github/workflows/status-dashboard.yml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            workflow.count("'.survey/repair-queue/under-16kb-reaudit.json'"), 2
        )


if __name__ == "__main__":
    unittest.main()
