import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"


def _load():
    spec = importlib.util.spec_from_file_location("render_status_dashboard_round_identity", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DiscoveryRoundIdentityTests(unittest.TestCase):
    def test_current_identity_uses_discovery_stats_run_key(self):
        module = _load()
        row = {"payload": {"discovery_stats": {"run_key": "current", "round": 2}}}
        self.assertEqual(module._discovery_round_identity(row), ("current", "2"))

    def test_durable_legacy_identity_uses_top_level_run_key(self):
        module = _load()
        row = {
            "payload": {
                "run_key": "2026-09-16T21:00:00+09:00",
                "discovery_stats": {"round": 1, "axis": "fresh-2609-serving-memory-kv"},
            }
        }
        self.assertEqual(
            module._discovery_round_identity(row),
            ("2026-09-16T21:00:00+09:00", "1"),
        )

    def test_missing_run_key_is_not_a_round_identity(self):
        module = _load()
        row = {"payload": {"discovery_stats": {"round": 1}}}
        self.assertIsNone(module._discovery_round_identity(row))


if __name__ == "__main__":
    unittest.main()
