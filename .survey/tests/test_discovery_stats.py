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

    def test_split_submissions_from_one_precheck_count_as_one_round(self) -> None:
        original_state = getattr(queue_worker, "DISCOVERY_STATE", None)
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                base_stats = {
                    "run_key": "2026-09-21T22:00:00+09:00",
                    "round": "precheck-split-round",
                    "axis": "split-round-regression",
                    "seed_canonical_id": "arXiv:2501.00001",
                    "candidate_count": 8,
                    "duplicate_filtered_count": 0,
                    "round_submission_count": 2,
                }
                precheck = {
                    "request_id": "precheck-split-1",
                    "provider": "openalex",
                    "source_url": "https://api.openalex.org/works?example=1",
                    "allowed_records": [{} for _ in range(8)],
                    "unseen_result_count": 8,
                }
                first = {
                    "_file": "work-queue/submissions/split-01.json",
                    "candidates": [{} for _ in range(5)],
                    "discovery_stats": dict(base_stats, round_submission_index=1),
                }
                second = {
                    "_file": "work-queue/submissions/split-02.json",
                    "candidates": [{} for _ in range(3)],
                    "discovery_stats": dict(base_stats, round_submission_index=2),
                }

                self.assertTrue(queue_worker.record_discovery_stats(
                    first, accepted_count=5, precheck_result=precheck
                ))
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(len(state["history"]), 1)
                self.assertFalse(state["history"][0]["round_complete"])
                self.assertEqual(state.get("axes", {}).get("split-round-regression"), None)

                self.assertTrue(queue_worker.record_discovery_stats(
                    second, accepted_count=3, precheck_result=precheck
                ))
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(len(state["history"]), 1)
                row = state["history"][0]
                self.assertTrue(row["round_complete"])
                self.assertEqual(row["precheck_request_id"], "precheck-split-1")
                self.assertEqual(row["seed_canonical_id"], "arXiv:2501.00001")
                self.assertEqual(len(row["source_submissions"]), 2)
                self.assertEqual(row["accepted_count"], 8)
                self.assertEqual(state["axes"]["split-round-regression"]["rounds"], 1)
                self.assertEqual(state["axes"]["split-round-regression"]["accepted_count"], 8)
        finally:
            if original_state is not None:
                queue_worker.DISCOVERY_STATE = original_state

    def test_final_duplicate_filtering_is_recorded_separately(self) -> None:
        original_state = getattr(queue_worker, "DISCOVERY_STATE", None)
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                sub = {
                    "_file": "work-queue/submissions/final-dedupe.json",
                    "candidates": [
                        {"canonical_id": "arXiv:2609.00001"},
                        {"canonical_id": "arXiv:2609.00002"},
                        {"canonical_id": "arXiv:2609.00003"},
                    ],
                    "discovery_stats": {
                        "run_key": "2026-09-16T20:00:00+09:00",
                        "round": "final-dedupe-visibility",
                        "axis": "identity-dedup-regression",
                        "candidate_count": 5,
                        "duplicate_filtered_count": 2,
                    },
                }

                self.assertTrue(
                    queue_worker.record_discovery_stats(
                        sub,
                        accepted_count=1,
                        final_duplicate_filtered_count=2,
                    )
                )
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                row = state["history"][-1]
                self.assertEqual(row["duplicate_filtered_count"], 2)
                self.assertEqual(row["novel_candidate_count"], 3)
                self.assertEqual(row["final_duplicate_filtered_count"], 2)
                self.assertEqual(row["post_final_dedupe_count"], 1)
                self.assertEqual(row["accepted_count"], 1)
                self.assertAlmostEqual(row["final_duplicate_ratio"], 2 / 3)
                axis = state["axes"]["identity-dedup-regression"]
                self.assertEqual(axis["final_duplicate_filtered_count"], 2)
        finally:
            if original_state is not None:
                queue_worker.DISCOVERY_STATE = original_state

    def test_stats_repair_submission_does_not_require_live_discovery_job(self) -> None:
        originals = {
            name: getattr(queue_worker, name)
            for name in ("ROOT", "QUEUE", "JOBS", "SUBMISSIONS", "RESULTS", "STATE", "ARCHIVE", "DISCOVERY_STATE")
        }
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td) / ".survey"
                queue = root / "work-queue"
                queue_worker.ROOT = root
                queue_worker.QUEUE = queue
                queue_worker.JOBS = queue / "jobs"
                queue_worker.SUBMISSIONS = queue / "submissions"
                queue_worker.RESULTS = queue / "results"
                queue_worker.STATE = queue / "state.json"
                queue_worker.ARCHIVE = queue / "archive"
                queue_worker.DISCOVERY_STATE = queue / "discovery-state.json"
                queue_worker.SUBMISSIONS.mkdir(parents=True)
                queue_worker.DISCOVERY_STATE.write_text(
                    json.dumps({"schema_version": 2, "history_limit": 24, "history": [], "axes": {}}),
                    encoding="utf-8",
                )
                submission = {
                    "schema_version": 1,
                    "operation": "record_discovery_stats",
                    "accepted_count": 3,
                    "discovery_stats": {
                        "run_key": "2026-09-12T14:22:56+09:00",
                        "round": "specialist-2609-serving-routing-1",
                        "axis": "2609新着・分離サービング・動的ルーティング",
                        "query_summary": "手動試運転の探索結果を補完",
                        "candidate_count": 4,
                        "duplicate_filtered_count": 1,
                        "duplicate_canonical_ids": ["arxiv:2609.11133"],
                        "next_axis_hint": "SSD expert I/O schedulingへ展開",
                    },
                }
                source = queue_worker.SUBMISSIONS / "manual-stats-repair.json"
                source.write_text(json.dumps(submission, ensure_ascii=False), encoding="utf-8")

                st = {"stats": {"discovered": 0, "selected": 0, "research_completed": 0, "audit_completed": 0, "rejected": 0}}
                queue_worker.process_submissions(st)

                result = json.loads((queue_worker.RESULTS / source.name).read_text(encoding="utf-8"))
                self.assertTrue(result["ok"])
                self.assertEqual(result["operation"], "record_discovery_stats")
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(state["history"][-1]["accepted_count"], 3)
                self.assertEqual(state["history"][-1]["source_submission"], "work-queue/submissions/manual-stats-repair.json")
        finally:
            for name, value in originals.items():
                setattr(queue_worker, name, value)


if __name__ == "__main__":
    unittest.main()
