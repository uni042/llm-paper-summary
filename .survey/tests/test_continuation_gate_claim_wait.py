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
        submission_state_checked=False,
        submission_result_pending=False,
        write_failed=False,
        probe="not-run",
        seconds_to_run_deadline=1800,
        seconds_to_next_scheduled_task=None,
        scheduled_handoff_guard_seconds=600,
        worker_kind="normal",
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

    def test_checked_pending_claim_requires_wait_loop(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=True,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_CLAIM_RESULT")
        self.assertEqual(result["claim_wait_seconds"], 10)
        self.assertIn("keep_same_request_id", result["claim_wait_action"])
        self.assertTrue(result["claim_state_checked"])
        self.assertIn("終了しません", result["next_action_message"])

    def test_unchecked_submission_state_requires_refresh(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=False,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CHECK_SUBMISSION_STATE")
        self.assertIn("submission", result["next_action_message"].lower())

    def test_pending_submission_with_independent_work_continues_without_finalizing(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
            independent_work=True,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CONTINUE_WORK")
        self.assertFalse(result["finalization_allowed"])
        self.assertIn("終了しません", result["next_action_message"])
        self.assertIn("次", result["next_action_message"])

    def test_pending_submission_without_independent_work_waits(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            submission_state_checked=True,
            submission_result_pending=True,
            independent_work=False,
            spillover_work=False,
            can_discover=False,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "WAIT_FOR_SUBMISSION_RESULT")
        self.assertEqual(result["submission_wait_seconds"], 10)
        self.assertIn("終了しません", result["progress_notice"])
        self.assertIn("再確認", result["progress_notice"])

    def test_checked_clear_claim_state_allows_normal_work(self):
        result = mod.decide(make_args(
            claim_state_checked=True,
            claim_result_pending=False,
            submission_state_checked=True,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "CONTINUE_WORK")
        self.assertTrue(result["claim_state_checked"])


if __name__ == "__main__":
    unittest.main()
