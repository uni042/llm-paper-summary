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
        claim_result_pending=False,
        submission_result_pending=False,
        ack_result_pending=False,
        hard_stop=False,
        handoff_safe=False,
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
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("active_assignment_requires_work", result["blocking_reasons"])

    def test_each_async_pending_state_requires_30_second_wait_loop(self):
        cases = (
            ("claim_result_pending", "claim_result"),
            ("submission_result_pending", "submission_result"),
            ("ack_result_pending", "ack_result"),
        )
        for field, target in cases:
            with self.subTest(field=field):
                result = mod.decide(make_args(**{field: True}))
                self.assertEqual(result["decision"], "MUST_CONTINUE")
                self.assertEqual(result["wait_seconds"], 30)
                self.assertEqual(result["next_action"], "WAIT_30_SECONDS_AND_RECHECK")
                self.assertIn(target, result["wait_targets"])
                self.assertFalse(result["finalization_permit"]["issued"])

    def test_stop_run_without_finalization_allowed_still_cannot_finalize(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=False,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("continuation_gate_did_not_allow_finalization", result["blocking_reasons"])

    def test_clean_time_stop_run_issues_permit(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
        ))
        self.assertEqual(result["decision"], "MAY_FINALIZE")
        self.assertTrue(result["finalization_permit"]["issued"])
        self.assertEqual(result["wait_seconds"], 0)

    def test_non_time_hard_stop_remains_abnormal_even_after_safe_handoff(self):
        result = mod.decide(make_args(
            continuation_decision="STOP_RUN",
            continuation_finalization_allowed=True,
            active_assignment=True,
            active_assignment_handoff_safe=True,
            claim_result_pending=True,
            hard_stop=True,
            handoff_safe=True,
        ))
        self.assertEqual(result["decision"], "MUST_CONTINUE")
        self.assertFalse(result["finalization_permit"]["issued"])
        self.assertIn("non_time_hard_stop_is_abnormal", result["blocking_reasons"])
        self.assertEqual(result["next_action"], "REPORT_OR_RECOVER_ABNORMAL_BLOCKER_WITHOUT_NORMAL_FINALIZATION")

    def test_hard_stop_without_safe_handoff_is_abnormal_and_unsafe(self):
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
        self.assertIn("non_time_hard_stop_is_abnormal", result["blocking_reasons"])
        self.assertIn("hard_stop_handoff_not_safe", result["blocking_reasons"])


if __name__ == "__main__":
    unittest.main()
