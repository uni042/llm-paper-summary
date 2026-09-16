from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SURVEY = Path(__file__).resolve().parents[1]
SCRIPTS = SURVEY / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


continuation_gate = load_module("continuation_gate_time_only", "continuation_gate.py")
run_finalization_gate = load_module("run_finalization_gate_time_only", "run_finalization_gate.py")
import queue_worker  # noqa: E402


def continuation_args(**overrides):
    data = dict(
        github_read=True,
        github_write=True,
        library_writable=False,
        result_durable=True,
        seed_durable=True,
        unpublished_completed_result=False,
        offline_seed_required=False,
        platform_limit=False,
        global_dependency=False,
        independent_work=False,
        spillover_work=False,
        can_discover=False,
        claim_result_pending=False,
        write_failed=False,
        probe="not-run",
        seconds_to_next_scheduled_task=None,
        seconds_to_run_deadline=2500,
        scheduled_handoff_guard_seconds=600,
        worker_kind="discovery",
        discovery_rounds_completed=99,
        discovery_rounds_since_last_novel=99,
        discovery_min_rounds=4,
        discovery_exhausted=True,
        next_axis_available=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


def finalization_args(**overrides):
    data = dict(
        continuation_decision="STOP_RUN",
        continuation_finalization_allowed=True,
        active_assignment=False,
        active_assignment_handoff_safe=False,
        claim_result_pending=False,
        submission_result_pending=False,
        ack_result_pending=False,
        hard_stop=False,
        handoff_safe=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class DiscoveryTimeOnlyLivenessTests(unittest.TestCase):
    GLOBALS = ("ROOT", "QUEUE", "JOBS", "SUBMISSIONS", "RESULTS", "STATE", "ARCHIVE", "DISCOVERY_STATE")

    def setUp(self) -> None:
        self.originals = {name: getattr(queue_worker, name) for name in self.GLOBALS}
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / ".survey"
        queue_worker.ROOT = root
        queue_worker.QUEUE = root / "work-queue"
        queue_worker.JOBS = queue_worker.QUEUE / "jobs"
        queue_worker.SUBMISSIONS = queue_worker.QUEUE / "submissions"
        queue_worker.RESULTS = queue_worker.QUEUE / "results"
        queue_worker.STATE = queue_worker.QUEUE / "state.json"
        queue_worker.ARCHIVE = queue_worker.QUEUE / "archive"
        queue_worker.DISCOVERY_STATE = queue_worker.QUEUE / "discovery-state.json"
        queue_worker.JOBS.mkdir(parents=True)
        queue_worker.SUBMISSIONS.mkdir(parents=True)
        queue_worker.DISCOVERY_STATE.write_text(
            json.dumps({"schema_version": 2, "history_limit": 24, "history": [], "axes": {}}),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            setattr(queue_worker, name, value)
        self.tmp.cleanup()

    def test_discovery_exhaustion_and_round_counts_cannot_stop_before_time_guard(self) -> None:
        result = continuation_gate.decide(continuation_args())
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertFalse(result["finalization_allowed"])
        self.assertNotIn("discovery_exhausted_after_minimum_rounds", result["stop_reasons"])

    def test_non_time_hard_stop_cannot_receive_normal_finalization_permit(self) -> None:
        result = run_finalization_gate.decide(finalization_args(hard_stop=True, handoff_safe=True))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("non_time_hard_stop_is_abnormal", result["blocking_reasons"])

    def test_discovery_round_accepts_more_than_five_candidates_without_truncation(self) -> None:
        candidates = [
            {
                "canonical_id": f"arXiv:2609.{91000 + i}",
                "title": f"Unlimited discovery candidate {i}",
                "source_url": f"https://arxiv.org/abs/2609.{91000 + i}",
                "paper_path": f"papers/inference/99-test/2609.{91000 + i}.md",
                "priority": 90,
                "reason": "unbounded discovery regression fixture",
            }
            for i in range(12)
        ]
        payload = {
            "schema_version": 1,
            "workflow_version": 10,
            "operation": "submit_discovery_round",
            "_file": "work-queue/submissions/unbounded-round.json",
            "candidates": candidates,
            "discovery_stats": {
                "run_key": "2026-09-16T20:00:00+09:00",
                "round": "unbounded-regression",
                "axis": "unbounded-regression-axis",
                "query_summary": "verify arbitrary candidate counts are accepted",
                "candidate_count": len(candidates),
                "duplicate_filtered_count": 0,
            },
        }
        state = {
            "stats": {
                "discovered": 0,
                "selected": 0,
                "research_completed": 0,
                "audit_completed": 0,
                "rejected": 0,
            }
        }

        job = queue_worker.process_discovery_round_submission(payload, state)

        self.assertEqual(job["result_summary"]["submitted_candidates"], 12)
        self.assertEqual(job["result_summary"]["research_jobs_added"], 12)
        research_jobs = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in queue_worker.JOBS.glob("*.json")
            if json.loads(path.read_text(encoding="utf-8")).get("type") == "research"
        ]
        self.assertEqual(len(research_jobs), 12)
        self.assertEqual(state["stats"]["discovered"], 12)
        self.assertEqual(state["stats"]["selected"], 12)


if __name__ == "__main__":
    unittest.main()
