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
        claim_state_checked=False,
        claim_result_pending=False,
        claim_result_pending_age_seconds=0,
        claim_monitor_window_seconds=60,
        submission_state_checked=False,
        submission_result_pending=False,
        pipeline_ahead_count=0,
        discovery_precheck_result_pending=False,
        discovery_submission_result_pending=False,
        discovery_evaluation_pending=False,
        discovery_recovery_required=False,
        write_failed=False,
        probe="not-run",
        seconds_to_run_deadline=1800,
        seconds_to_next_scheduled_task=None,
        scheduled_handoff_guard_seconds=600,
        candidate_inventory=50,
        research_audit_completed_this_invocation=0,
        research_minimum_completions=3,
        last_terminal_job_status="none",
        discovery_rounds_completed=0,
        discovery_rounds_since_last_novel=None,
        discovery_min_rounds=4,
        discovery_exhausted=False,
        next_axis_available=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class ContinuationGateClaimWaitTests(unittest.TestCase):
    def test_unchecked_claim_state_requires_refresh(self):
        result = mod.decide(make_args())
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CHECK_CLAIM_STATE")
        self.assertFalse(result["finalization_allowed"])
        self.assertFalse(result["claim_state_checked"])
        self.assertIn("claim", result["next_action_message"].lower())

    def test_fresh_pending_claim_uses_active_monitoring_cycle(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=True,
            claim_result_pending_age_seconds=22,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "MONITOR_CLAIM_FAST_LANE")
        self.assertEqual(result["claim_wait_seconds"], 10)
        self.assertIn("inspect_survey_claim_fast_actions_run", result["claim_wait_action"])
        self.assertIn("unsettled_submissions", result["claim_wait_action"])
        self.assertTrue(result["claim_state_checked"])
        self.assertIn("60秒未満", result["next_action_message"])

    def test_old_pending_claim_keeps_same_request_and_checks_transport_health(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=True,
            claim_result_pending_age_seconds=60,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_CLAIM_RESULT")
        self.assertEqual(result["claim_wait_seconds"], 10)
        self.assertIn("keep_same_request_id", result["claim_wait_action"])
        self.assertIn("transport_health", result["claim_wait_action"])
        self.assertIn("新しいrequestは発行せず", result["next_action_message"])

    def test_unchecked_submission_state_requires_refresh(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=False,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CHECK_SUBMISSION_STATE")
        self.assertIn("submission", result["next_action_message"].lower())

    def test_pending_submission_allows_exactly_one_paper_lookahead(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
            pipeline_ahead_count=0,
            independent_work=True,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")
        self.assertFalse(result["finalization_allowed"])
        self.assertEqual(result["submission_wait_seconds"], 0)
        self.assertEqual(result["submission_wait_action"], "none")
        self.assertIn("1本だけ先送り", result["next_action_message"])

    def test_pending_submission_without_claimable_work_waits_instead(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
            pipeline_ahead_count=0,
            independent_work=False,
            spillover_work=False,
            can_discover=False,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT")
        self.assertEqual(result["submission_wait_seconds"], 10)

    def test_pending_previous_submission_blocks_after_one_paper_lookahead(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
            pipeline_ahead_count=1,
            independent_work=True,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT")
        self.assertEqual(result["submission_wait_seconds"], 10)
        self.assertIn("1本前", result["progress_notice"])
        self.assertIn("再確認", result["progress_notice"])

    def test_checked_clear_claim_state_under_quota_claims_next_paper(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=False,
            submission_state_checked=True,
            research_audit_completed_this_invocation=0,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")
        self.assertFalse(result["finalization_allowed"])
        self.assertTrue(result["claim_state_checked"])
        self.assertIn("次のResearch/Audit", result["next_action_message"])

    def test_terminal_blocked_claims_next_paper_even_after_quota_floor(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=False,
            submission_state_checked=True,
            research_audit_completed_this_invocation=3,
            last_terminal_job_status="blocked",
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")
        self.assertTrue(result["status_only_terminal"])
        self.assertFalse(result["finalization_allowed"])

    def test_completed_terminal_after_quota_floor_allows_general_continuation(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=False,
            submission_state_checked=True,
            research_audit_completed_this_invocation=3,
            last_terminal_job_status="completed",
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CONTINUE_WORK")
        self.assertFalse(result["status_only_terminal"])


if __name__ == "__main__":
    unittest.main()
