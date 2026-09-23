from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_window_policy


class ClaimWindowPolicyTests(unittest.TestCase):
    def test_default_window_and_low_watermark(self):
        self.assertEqual(claim_window_policy.DEFAULT_CLAIM_WINDOW, 8)
        self.assertEqual(claim_window_policy.refill_threshold(8), 4)
        self.assertFalse(claim_window_policy.should_refill(5, 8))
        self.assertTrue(claim_window_policy.should_refill(4, 8))
        self.assertTrue(claim_window_policy.should_refill(1, 8))

    def test_low_watermark_generalizes_with_window(self):
        self.assertEqual(claim_window_policy.refill_threshold(4), 2)
        self.assertEqual(claim_window_policy.refill_threshold(6), 3)
        self.assertEqual(claim_window_policy.refill_threshold(10), 5)
        self.assertFalse(claim_window_policy.should_refill(4, 6))
        self.assertTrue(claim_window_policy.should_refill(3, 6))

    def test_shared_pool_target_scales_with_bank_count(self):
        self.assertEqual(claim_window_policy.shared_pool_target(32), 24)
        self.assertEqual(claim_window_policy.shared_pool_target(40), 30)
        self.assertEqual(claim_window_policy.shared_pool_target(16), 12)


if __name__ == "__main__":
    unittest.main()
