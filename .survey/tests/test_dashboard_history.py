import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]


def _load_policy():
    path = ROOT / ".survey/scripts/history_policy.py"
    spec = importlib.util.spec_from_file_location("history_policy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DashboardHistoryTests(unittest.TestCase):
    def test_history_policy_enforces_dashboard_minimum(self):
        policy = _load_policy()
        for value in (None, 0, 24, 48, 383, True, "384"):
            with self.subTest(value=value):
                self.assertEqual(policy.normalize_history_limit(value), 384)

    def test_history_policy_preserves_larger_explicit_limits(self):
        policy = _load_policy()
        self.assertEqual(policy.normalize_history_limit(384), 384)
        self.assertEqual(policy.normalize_history_limit(500), 500)

    def test_durable_history_writers_use_shared_policy(self):
        ledger = (ROOT / ".survey/scripts/record_run_ledger.py").read_text(encoding="utf-8")
        queue = (ROOT / ".survey/scripts/queue_worker.py").read_text(encoding="utf-8")
        self.assertIn("DEFAULT_HISTORY_LIMIT = history_policy.MIN_HISTORY_LIMIT", ledger)
        self.assertIn("history_policy.normalize_history_limit(ledger.get(\"history_limit\"))", ledger)
        self.assertIn("history_policy.normalize_history_limit(state.get(\"history_limit\"))", queue)
        self.assertNotIn("DEFAULT_HISTORY_LIMIT = 48", ledger)
        self.assertNotIn('state.get("history_limit", 24)', queue)


if __name__ == "__main__":
    unittest.main()
