import argparse
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "continuation_gate.py"
spec = importlib.util.spec_from_file_location("continuation_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_args(**overrides):
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
        independent_work=True,
        spillover_work=False,
        can_discover=True,
        claim_state_checked=True,
        claim_result_pending=False,
        submission_state_checked=True,
        submission_result_pending=False,
        write_failed=False,
        probe="not-run",
        seconds_to_next_scheduled_task=None,
        seconds_to_run_deadline=None,
        scheduled_handoff_guard_seconds=600,
        worker_kind="normal",
        candidate_inventory=None,
        work_mode="auto",
        papers_added_this_invocation=0,
        research_minimum_papers=3,
        discovery_rounds_completed=0,
        discovery_rounds_since_last_novel=None,
        discovery_min_rounds=4,
        discovery_exhausted=False,
        next_axis_available=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class ContinuationGateScheduleTests(unittest.TestCase):
    def test_both_schedule_labels_choose_same_mode_from_inventory(self):
        for worker_kind in ("normal", "discovery"):
            with self.subTest(worker_kind=worker_kind):
                research = mod.decide(make_args(
                    worker_kind=worker_kind,
                    candidate_inventory=49,
                    seconds_to_run_deadline=3600,
                ))
                discovery = mod.decide(make_args(
                    worker_kind=worker_kind,
                    candidate_inventory=50,
                    discovery_rounds_since_last_novel=0,
                    seconds_to_run_deadline=3600,
                ))
                self.assertEqual(research["work_mode"], "research")
                self.assertEqual(research["mode_source"], "candidate_inventory")
                self.assertEqual(discovery["work_mode"], "discovery")
                self.assertEqual(discovery["mode_source"], "candidate_inventory")
                self.assertEqual(discovery["required_action"], "DISCOVER_AGAIN")

    def test_threshold_boundary_50_is_discovery(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            discovery_rounds_since_last_novel=0,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["work_mode"], "discovery")
        self.assertEqual(result["minimum_rounds_remaining"], 4)

    def test_inventory_below_50_is_research_and_exposes_three_paper_quota(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            papers_added_this_invocation=1,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["work_mode"], "research")
        self.assertEqual(result["research_minimum_papers"], 3)
        self.assertEqual(result["research_quota_remaining"], 2)
        self.assertEqual(result["required_action"], "CONTINUE_WORK")

    def test_discovery_minimum_four_rounds_is_preserved(self):
        result = mod.decide(make_args(
            candidate_inventory=100,
            discovery_rounds_completed=3,
            discovery_rounds_since_last_novel=3,
            discovery_exhausted=True,
            next_axis_available=False,
            independent_work=False,
            can_discover=False,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "DISCOVER_AGAIN")
        self.assertEqual(result["minimum_rounds_remaining"], 1)
        self.assertFalse(result["finalization_allowed"])

    def test_discovery_can_stop_after_four_rounds_if_exhausted(self):
        result = mod.decide(make_args(
            candidate_inventory=100,
            discovery_rounds_completed=4,
            discovery_rounds_since_last_novel=4,
            discovery_exhausted=True,
            next_axis_available=False,
            independent_work=False,
            can_discover=False,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertIn("discovery_exhausted_after_minimum_rounds", result["stop_reasons"])

    def test_run_deadline_guard_overrides_mode_quota(self):
        for candidate_inventory in (49, 50):
            with self.subTest(candidate_inventory=candidate_inventory):
                result = mod.decide(make_args(
                    candidate_inventory=candidate_inventory,
                    discovery_rounds_since_last_novel=0,
                    seconds_to_run_deadline=600,
                ))
                self.assertEqual(result["decision"], "STOP_RUN")
                self.assertTrue(result["finalization_allowed"])
                self.assertIn("run_deadline_within_handoff_guard", result["stop_reasons"])

    def test_schedule_boundary_is_compatibility_fallback_when_run_deadline_missing(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            seconds_to_next_scheduled_task=599,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertIn("next_scheduled_task_within_handoff_guard", result["stop_reasons"])

    def test_old_callers_without_inventory_fall_back_to_worker_kind(self):
        research = mod.decide(make_args(worker_kind="normal", candidate_inventory=None))
        discovery = mod.decide(make_args(
            worker_kind="discovery",
            candidate_inventory=None,
            discovery_rounds_since_last_novel=0,
        ))
        self.assertEqual(research["work_mode"], "research")
        self.assertEqual(research["mode_source"], "legacy_worker_kind_fallback")
        self.assertEqual(discovery["work_mode"], "discovery")
        self.assertEqual(discovery["mode_source"], "legacy_worker_kind_fallback")


if __name__ == "__main__":
    unittest.main()
