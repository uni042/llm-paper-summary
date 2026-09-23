from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import continuation_gate


def args(active_claim_count: int) -> argparse.Namespace:
    return argparse.Namespace(
        github_read=True,
        github_write=True,
        library_writable=True,
        result_durable=True,
        seed_durable=True,
        unpublished_completed_result=False,
        offline_seed_required=False,
        platform_limit=False,
        global_dependency=False,
        independent_work=True,
        spillover_work=False,
        can_discover=False,
        write_failed=False,
        probe="not-run",
        work_mode="research",
        candidate_inventory=100,
        active_assignment=True,
        active_claim_count=active_claim_count,
        claim_window=8,
        claim_refill_threshold=4,
        claim_window_remaining=max(8 - active_claim_count, 0),
        claim_state_checked=True,
        claim_result_pending=False,
        submission_state_checked=True,
        submission_result_pending=False,
        seconds_to_run_deadline=3000,
    )


class ContinuationGateClaimWindowTests(unittest.TestCase):
    def test_above_low_watermark_keeps_processing_without_refill(self):
        result = continuation_gate.decide(args(5))
        self.assertEqual(result["required_action"], "CONTINUE_ASSIGNED_WORK")
        self.assertFalse(result["claim_refill_needed"])

    def test_at_low_watermark_refills_asynchronously(self):
        result = continuation_gate.decide(args(4))
        self.assertEqual(
            result["required_action"],
            "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY",
        )
        self.assertTrue(result["claim_refill_needed"])
        self.assertEqual(result["claim_refill_threshold"], 4)


if __name__ == "__main__":
    unittest.main()
