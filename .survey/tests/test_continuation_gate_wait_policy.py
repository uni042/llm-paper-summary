import argparse
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "continuation_gate.py"
spec = importlib.util.spec_from_file_location("continuation_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ContinuationGateWaitPolicyTests(unittest.TestCase):
    def test_pending_claim_exposes_fixed_10_second_recheck_contract(self):
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
            candidate_inventory=50,
            discovery_rounds_completed=0,
            discovery_min_rounds=4,
            discovery_exhausted=False,
            next_axis_available=False,
        )
        result = mod.decide(args)
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["claim_wait_seconds"], 10)
        self.assertIn("wait_10_real_seconds", result["claim_wait_action"])
        self.assertIn("repeat_until_result_or_terminal_hard_stop", result["claim_wait_action"])


if __name__ == "__main__":
    unittest.main()
