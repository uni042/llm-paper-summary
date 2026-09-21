import argparse
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "run_finalization_gate.py"
spec = importlib.util.spec_from_file_location("run_finalization_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_args(**overrides):
    data = dict(
        continuation_decision="CONTINUE",
        continuation_finalization_allowed=False,
        active_assignment=False,
        active_assignment_handoff_safe=False,
        claim_state_checked=False,
        claim_result_pending=False,
        submission_state_checked=False,
        submission_result_pending=False,
        ack_result_pending=False,
        discovery_precheck_result_pending=False,
        discovery_submission_result_pending=False,
        discovery_evaluation_pending=False,
        discovery_recovery_required=False,
        hard_stop=False,
        handoff_safe=False,
        work_mode="unknown",
        research_audit_completed_this_invocation=0,
        research_minimum_completions=3,
        discovery_rounds_completed=0,
        discovery_min_rounds=4,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class RunFinalizationGateTests(unittest.TestCase):
    def test_continue_never_issues_finalization_permit(self):
        result = mod.decide(make_args())
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("continuation_decision_is_continue", result["blocking_reasons"])

    def test_active_assignment_blocks_normal_finalization(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            active_assignment=True,
            claim_state_checked=True,
            submission_state_checked=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("active_assignment_requires_work", result["blocking_reasons"])

    def test_each_async_pending_state_requires_10_second_wait_loop(self):
        cases = (
            ("claim_result_pending", "claim_result"),
            ("submission_result_pending", "submission_result"),
            ("ack_result_pending", "ack_result"),
        )
        for field, target in cases:
            with self.subTest(field=field):
                result = mod.decide(make_args(
                    claim_state_checked=True,
                    submission_state_checked=(field != "submission_result_pending"),
                    **{field: True},
                ))
                self.assertEqual(result["decision"], "MUST_CONTINUE")
                self.assertEqual(result["wait_seconds"], 10)
                self.assertEqual(result["next_action"], "WAIT_10_SECONDS_AND_RECHECK")
                self.assertIn(target, result["wait_targets"])
                self.assertFalse(result["finalization_permit"]["issued"])
                self.assertIn("terminal", result["rule"].lower())

    def test_started_discovery_round_blocks_normal_finalization(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
            work_mode="discovery",
            discovery_rounds_completed=4,
            discovery_evaluation_pending=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertIn("discovery_round_in_progress", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "CONTINUE_DISCOVERY_ROUND")

    def test_discovery_precheck_pending_uses_fixed_wait(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
            discovery_precheck_result_pending=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertEqual(result["next_action"], "WAIT_10_SECONDS_AND_RECHECK")
        self.assertIn("discovery_precheck_result", result["wait_targets"])

    def test_stop_run_without_finalization_allowed_still_cannot_finalize(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=False,
            claim_state_checked=True,
            submission_state_checked=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("continuation_gate_did_not_allow_finalization", result["blocking_reasons"])

    def test_unchecked_claim_state_blocks_finalization(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=False,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("claim_state_not_checked", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "CHECK_CLAIM_STATE")

    def test_unchecked_submission_state_blocks_finalization(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=False,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("submission_state_not_checked", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "CHECK_SUBMISSION_STATE")
        self.assertIn("submission", result["next_action_message"].lower())
        self.assertTrue(result["next_action_message"])

    def test_pending_submission_exposes_non_finalizing_progress_notice(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertEqual(result["next_action"], "WAIT_10_SECONDS_AND_RECHECK")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("終了しません", result["progress_notice"])
        self.assertIn("待機", result["progress_notice"])
        self.assertIn("再確認", result["progress_notice"])
        self.assertEqual(result["next_action_message"], result["progress_notice"])

    def test_research_quota_shortfall_blocks_finalization_even_with_stop_run(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
            work_mode="research",
            research_audit_completed_this_invocation=0,
            research_minimum_completions=3,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("research_minimum_not_met", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "CLAIM_NEXT_RESEARCH_AUDIT")

    def test_discovery_quota_shortfall_blocks_finalization_even_with_stop_run(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
            work_mode="discovery",
            discovery_rounds_completed=2,
            discovery_min_rounds=4,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("discovery_minimum_not_met", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "DISCOVER_AGAIN")

    def test_clean_stop_run_issues_permit(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            claim_state_checked=True,
            submission_state_checked=True,
        ))
        self.assertEqual(result["decision"], "MAY_FINALIZE")
        self.assertTrue(result["finalization_permit"]["issued"])
        self.assertEqual(result["wait_seconds"], 0)

    def test_explicit_hard_stop_can_finalize_pending_wait_only_after_safe_handoff(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            active_assignment=True,
            active_assignment_handoff_safe=True,
            claim_result_pending=True,
            hard_stop=True,
            handoff_safe=True,
        ))
        self.assertEqual(result["decision"], "MAY_FINALIZE")
        self.assertTrue(result["finalization_permit"]["issued"])
        self.assertEqual(result["next_action"], "FINALIZE_AFTER_SAFE_HANDOFF")

    def test_hard_stop_without_safe_handoff_does_not_issue_permit(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            active_assignment=True,
            claim_result_pending=True,
            hard_stop=True,
            handoff_safe=False,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("hard_stop_handoff_not_safe", result["blocking_reasons"])


if __name__ == "__main__":
    unittest.main()
