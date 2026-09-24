from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_window_policy


class ClaimWindowPolicyTests(unittest.TestCase):
    def test_default_inventory_hot_slice_and_refill_lead(self):
        self.assertEqual(claim_window_policy.DEFAULT_CLAIM_WINDOW, 12)
        self.assertEqual(claim_window_policy.HOT_BANKED_CLAIMS, 4)
        self.assertEqual(claim_window_policy.hot_banked_claims(12), 4)
        self.assertEqual(claim_window_policy.refill_threshold(12), 10)
        self.assertFalse(claim_window_policy.should_refill(11, 12))
        self.assertTrue(claim_window_policy.should_refill(10, 12))
        self.assertTrue(claim_window_policy.should_refill(1, 12))

    def test_refill_generalizes_with_window(self):
        self.assertEqual(claim_window_policy.refill_threshold(4), 2)
        self.assertEqual(claim_window_policy.refill_threshold(6), 4)
        self.assertEqual(claim_window_policy.refill_threshold(10), 8)
        self.assertFalse(claim_window_policy.should_refill(9, 10))
        self.assertTrue(claim_window_policy.should_refill(8, 10))

    def test_shared_stock_and_route_threshold_are_bank_independent(self):
        self.assertEqual(claim_window_policy.EXPECTED_PARALLEL_WORKERS, 6)
        self.assertEqual(claim_window_policy.shared_pool_target(), 144)
        self.assertEqual(claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD, 288)


if __name__ == "__main__":
    unittest.main()
