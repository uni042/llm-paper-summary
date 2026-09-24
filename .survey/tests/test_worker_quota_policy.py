from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey/scripts"
sys.path.insert(0, str(SCRIPTS))

import worker_quota_policy  # noqa: E402


class WorkerQuotaPolicyTests(unittest.TestCase):
    def test_canonical_quota_values_are_distinct_from_audit_fairness(self):
        self.assertEqual(worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS, 5)
        self.assertEqual(worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS, 8)
        self.assertEqual(worker_quota_policy.AUDIT_STARVATION_BLOCK_SIZE, 3)

    def test_audit_fairness_pulls_audit_into_each_closing_block_slot(self):
        rows = [
            {"id": "r1", "kind": "research"},
            {"id": "r2", "kind": "research"},
            {"id": "r3", "kind": "research"},
            {"id": "a1", "kind": "audit"},
            {"id": "r4", "kind": "research"},
            {"id": "r5", "kind": "research"},
            {"id": "a2", "kind": "audit"},
        ]
        ordered = worker_quota_policy.order_with_audit_fairness(rows, limit=6)
        self.assertEqual([row["kind"] for row in ordered], [
            "research", "research", "audit",
            "research", "research", "audit",
        ])

    def test_canonical_sources_do_not_reintroduce_old_run_quota_language(self):
        router = (ROOT / ".survey/docs/survey-workflow/worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")
        derived = (SCRIPTS / "derive_worker_run_state.py").read_text(encoding="utf-8")

        self.assertNotIn("Research / Audit 合計3件ノルマ", router)
        self.assertNotIn("research_audit_completed_this_invocation < 3", router)
        self.assertNotIn("three-completion quota", continuation)
        self.assertNotIn("three-completion floor", continuation)
        self.assertNotIn("four-round floor", continuation)
        self.assertNotIn("three-success floor", finalization)
        self.assertNotIn("four-round floor", finalization)
        self.assertIn("worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS", derived)
        self.assertIn("worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS", derived)


if __name__ == "__main__":
    unittest.main()
