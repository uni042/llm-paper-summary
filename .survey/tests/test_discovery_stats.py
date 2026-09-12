from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class DiscoveryStatsTest(unittest.TestCase):
    def test_discovery_submission_updates_axis_stats_and_is_idempotent(self) -> None:
        original_root = queue_worker.ROOT
        original_state = getattr(queue_worker, "DISCOVERY_STATE", None)
        try:
            with tempfile.TemporaryDirectory() as td:
                survey_root = Path(td) / ".survey"
                queue_worker.ROOT = survey_root
                queue_worker.DISCOVERY_STATE = survey_root / "work-queue" / "discovery-state.json"
                queue_worker.DISCOVERY_STATE.parent.mkdir(parents=True)
                queue_worker.DISCOVERY_STATE.write_text(
                    json.dumps({
                        "schema_version": 2,
                        "history_limit": 24,
                        "history": [],
                        "axes": {},
                    }, ensure_ascii=False),
                    encoding="utf-8",
                )

                sub = {
                    "_file": "work-queue/submissions/test-discovery.json",
                    "candidates": [{"canonical_id": "arXiv:2609.00001"}] * 3,
                    "discovery_stats": {
                        "run_key": "2026-09-12T14:00:00+09:00",
                        "round": "specialist-new-2609-1",
                        "axis": "2609新着・分離サービング・動的ルーティング",
                        "query_summary": "2609新着を複数軸で探索",
                        "candidate_count": 4,
                        "duplicate_filtered_count": 1,
                        "duplicate_canonical_ids": ["arxiv:2609.11133"],
                        "next_axis_hint": "次回はSSD expert I/O schedulingへ移る",
                    },
                }

                self.assertTrue(queue_worker.record_discovery_stats(sub, accepted_count=3))
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(state["last_run_key"], "2026-09-12T14:00:00+09:00")
                self.assertEqual(state["last_round"], "specialist-new-2609-1")
                self.assertEqual(len(state["history"]), 1)
                row = state["history"][0]
                self.assertEqual(row["candidate_count"], 4)
                self.assertEqual(row["duplicate_filtered_count"], 1)
                self.assertEqual(row["novel_candidate_count"], 3)
                self.assertEqual(row["accepted_count"], 3)
                self.assertAlmostEqual(row["duplicate_ratio"], 0.25)
                axis = state["axes"]["2609新着・分離サービング・動的ルーティング"]
                self.assertEqual(axis["rounds"], 1)
                self.assertEqual(axis["candidate_count"], 4)
                self.assertEqual(axis["duplicate_filtered_count"], 1)
                self.assertEqual(axis["accepted_count"], 3)

                self.assertFalse(queue_worker.record_discovery_stats(sub, accepted_count=3))
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(len(state["history"]), 1)
                self.assertEqual(state["axes"]["2609新着・分離サービング・動的ルーティング"]["rounds"], 1)
        finally:
            queue_worker.ROOT = original_root
            if original_state is not None:
                queue_worker.DISCOVERY_STATE = original_state


if __name__ == "__main__":
    unittest.main()
