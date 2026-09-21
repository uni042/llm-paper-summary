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
        pipeline_ahead_count=0,
        discovery_precheck_result_pending=False,
        discovery_submission_result_pending=False,
        discovery_evaluation_pending=False,
        discovery_recovery_required=False,
        write_failed=False,
        probe="not-run",
        seconds_to_next_scheduled_task=None,
        seconds_to_run_deadline=None,
        scheduled_handoff_guard_seconds=600,
        candidate_inventory=None,
        work_mode="auto",
        research_audit_completed_this_invocation=0,
        research_minimum_completions=3,
        discovery_rounds_completed=0,
        discovery_min_rounds=4,
        discovery_exhausted=False,
        next_axis_available=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class ContinuationGateScheduleTests(unittest.TestCase):
    def test_inventory_alone_selects_mode(self):
        discovery = mod.decide(make_args(
            candidate_inventory=49,
            seconds_to_run_deadline=3600,
        ))
        research = mod.decide(make_args(
            candidate_inventory=50,
            seconds_to_run_deadline=3600,
        ))
        self.assertEqual(discovery["work_mode"], "discovery")
        self.assertEqual(discovery["mode_source"], "candidate_inventory")
        self.assertEqual(discovery["required_action"], "DISCOVER_AGAIN")
        self.assertEqual(research["work_mode"], "research")
        self.assertEqual(research["mode_source"], "candidate_inventory")

    def test_threshold_boundary_50_is_research(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["work_mode"], "research")
        self.assertEqual(result["research_quota_remaining"], 3)

    def test_inventory_at_least_50_is_research_and_exposes_combined_quota(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            research_audit_completed_this_invocation=1,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["work_mode"], "research")
        self.assertEqual(result["research_minimum_completions"], 3)
        self.assertEqual(result["research_audit_completed_this_invocation"], 1)
        self.assertEqual(result["research_quota_remaining"], 2)
        self.assertEqual(result["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")

    def test_discovery_minimum_four_rounds_is_preserved(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_rounds_completed=3,
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

    def test_discovery_exhaustion_does_not_end_run_early(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_rounds_completed=4,
            discovery_exhausted=True,
            next_axis_available=False,
            independent_work=False,
            can_discover=False,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertFalse(result["finalization_allowed"])
        self.assertEqual(result["required_action"], "REFRESH_AND_CONTINUE")


    def test_explicit_mode_locks_routing_for_the_run(self):
        result = mod.decide(make_args(
            candidate_inventory=0,
            work_mode="research",
            research_audit_completed_this_invocation=2,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["work_mode"], "research")
        self.assertEqual(result["mode_source"], "explicit_work_mode")
        self.assertEqual(result["research_quota_remaining"], 1)

    def test_four_round_floor_uses_total_completed_prechecks(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_rounds_completed=4,
            discovery_exhausted=True,
            next_axis_available=False,
            independent_work=False,
            can_discover=False,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["minimum_rounds_remaining"], 0)

    def test_research_runwide_write_failure_checkpoints_without_next_paper(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            work_mode="research",
            write_failed=True,
            probe="failure",
            github_write=False,
            library_writable=True,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["write_failure_scope"], "run_wide_github_write_unavailable")
        self.assertIn("checkpoint_current_assignment_to_library", result["write_action"])
        self.assertIn("do_not_start_next_paper", result["write_action"])
        self.assertIn("keep_scheduled_task_enabled", result["write_action"])

    def test_research_mode_does_not_treat_discovery_as_fallback_independent_work(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            work_mode="research",
            global_dependency=True,
            independent_work=False,
            spillover_work=False,
            can_discover=True,
            claim_state_checked=True,
            submission_state_checked=True,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertIn("all_remaining_work_blocked_after_fallback_consideration", result["stop_reasons"])

    def test_run_deadline_guard_overrides_mode_quota(self):
        for candidate_inventory in (49, 50):
            with self.subTest(candidate_inventory=candidate_inventory):
                result = mod.decide(make_args(
                    candidate_inventory=candidate_inventory,
                            seconds_to_run_deadline=600,
                ))
                self.assertEqual(result["decision"], "STOP_RUN")
                self.assertTrue(result["finalization_allowed"])
                self.assertTrue(result["hard_stop"])
                self.assertIn("run_deadline_within_handoff_guard", result["stop_reasons"])

    def test_schedule_boundary_is_compatibility_fallback_when_run_deadline_missing(self):
        result = mod.decide(make_args(
            candidate_inventory=50,
            seconds_to_next_scheduled_task=599,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertIn("next_scheduled_task_within_handoff_guard", result["stop_reasons"])

    def test_discovery_pending_precheck_survives_600_second_start_prohibition_window(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_precheck_result_pending=True,
            seconds_to_run_deadline=600,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_DISCOVERY_PRECHECK_RESULT")
        self.assertFalse(result["finalization_allowed"])

    def test_discovery_pending_submission_survives_600_second_start_prohibition_window(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_submission_result_pending=True,
            seconds_to_run_deadline=599,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT")

    def test_final_180_second_guard_can_handoff_started_discovery(self):
        result = mod.decide(make_args(
            candidate_inventory=49,
            discovery_precheck_result_pending=True,
            seconds_to_run_deadline=180,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertIn("run_deadline_within_final_180_second_handoff_guard", result["stop_reasons"])

    def test_auto_mode_requires_candidate_inventory(self):
        with self.assertRaises(ValueError):
            mod.decide(make_args(candidate_inventory=None))


if __name__ == "__main__":
    unittest.main()
