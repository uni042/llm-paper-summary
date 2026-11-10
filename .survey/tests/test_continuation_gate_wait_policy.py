import argparse
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "continuation_gate.py"
spec = importlib.util.spec_from_file_location("continuation_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ContinuationGateWaitPolicyTests(unittest.TestCase):
    def test_pending_claim_exposes_productive_recheck_contract(self):
        args = argparse.Namespace(
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
            claim_result_pending=True,
            write_failed=False,
            probe="not-run",
            seconds_to_next_scheduled_task=None,
            seconds_to_run_deadline=3000,
            scheduled_handoff_guard_seconds=600,
            candidate_inventory=300,
            discovery_rounds_completed=0,
            discovery_min_rounds=8,
            discovery_exhausted=False,
            next_axis_available=False,
        )
        result = mod.decide(args)
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["claim_wait_seconds"], 0)
        self.assertTrue(result["productive_wait_required"])
        self.assertFalse(result["productive_wait_polling"])
        self.assertIn("run_one_wait_microtask", result["claim_wait_action"])
        self.assertIn("repeat_until_result_or_terminal_hard_stop", result["claim_wait_action"])


    def test_pending_discovery_prefers_prepared_pipeline_work(self):
        args = argparse.Namespace(
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
            claim_result_pending=False,
            write_failed=False,
            probe="not-run",
            seconds_to_next_scheduled_task=None,
            seconds_to_run_deadline=3000,
            scheduled_handoff_guard_seconds=600,
            candidate_inventory=0,
            work_mode="discovery",
            discovery_rounds_completed=0,
            discovery_min_rounds=8,
            discovery_exhausted=False,
            next_axis_available=True,
            discovery_precheck_result_pending=True,
            discovery_submission_result_pending=False,
            discovery_evaluation_pending=False,
            discovery_recovery_required=False,
            discovery_pipeline_work_available=True,
        )
        result = mod.decide(args)
        self.assertEqual(result["required_action"], "CONTINUE_DISCOVERY_PIPELINE")
        self.assertFalse(result["productive_wait_required"])
        self.assertTrue(result["discovery_pipeline_work_available"])
        self.assertIn("cached候補", result["next_action_message"])



if __name__ == "__main__":
    unittest.main()
