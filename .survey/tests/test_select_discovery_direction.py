from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "select_discovery_direction.py"
spec = importlib.util.spec_from_file_location("select_discovery_direction", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class SelectDiscoveryDirectionTests(unittest.TestCase):
    def test_pair_order_starts_backward_then_forward(self):
        state = {"history": []}
        first = mod.decide(state, "run-a")
        self.assertEqual(first["next_direction"], "backward")

        state["history"].append(
            {
                "run_key": "run-a",
                "citation_direction": "backward",
                "accepted_count": 1,
                "novel_candidate_count": 1,
                "duplicate_ratio": 0.0,
            }
        )
        second = mod.decide(state, "run-a")
        self.assertEqual(second["next_direction"], "forward")

    def test_empty_pair_allows_normal_gap_fill(self):
        state = {
            "history": [
                {
                    "run_key": "run-a",
                    "citation_direction": "backward",
                    "accepted_count": 0,
                    "novel_candidate_count": 0,
                    "duplicate_ratio": 1.0,
                },
                {
                    "run_key": "run-a",
                    "citation_direction": "forward",
                    "accepted_count": 0,
                    "novel_candidate_count": 0,
                    "duplicate_ratio": 1.0,
                },
            ]
        }
        result = mod.decide(state, "run-a")
        self.assertEqual(result["next_direction"], "normal")

    def test_productive_history_prefers_direction_and_seed(self):
        state = {
            "history": [
                {
                    "run_key": "old",
                    "citation_direction": "backward",
                    "seed_canonical_id": "arXiv:0002.00002",
                    "accepted_count": 0,
                    "novel_candidate_count": 0,
                    "duplicate_ratio": 1.0,
                },
                {
                    "run_key": "old",
                    "citation_direction": "forward",
                    "seed_canonical_id": "arXiv:0001.00001",
                    "accepted_count": 2,
                    "novel_candidate_count": 3,
                    "duplicate_ratio": 0.0,
                },
                {
                    "run_key": "run-a",
                    "citation_direction": "backward",
                    "accepted_count": 1,
                    "novel_candidate_count": 1,
                    "duplicate_ratio": 0.0,
                },
                {
                    "run_key": "run-a",
                    "citation_direction": "forward",
                    "accepted_count": 1,
                    "novel_candidate_count": 1,
                    "duplicate_ratio": 0.0,
                },
            ]
        }
        result = mod.decide(state, "run-a")
        self.assertEqual(result["next_direction"], "forward")
        self.assertEqual(result["selected_seed_canonical_id"], "arXiv:0001.00001")


if __name__ == "__main__":
    unittest.main()
