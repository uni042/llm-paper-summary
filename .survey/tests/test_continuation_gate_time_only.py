import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = REPO_ROOT / ".survey" / "scripts" / "continuation_gate.py"


def run_gate(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(GATE), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


class ContinuationGateTimeOnlyDiscoveryTests(unittest.TestCase):
    def test_discovery_exhaustion_cannot_finalize_outside_handoff_guard(self):
        result = run_gate(
            "--worker-kind", "discovery",
            "--seconds-to-run-deadline", "1200",
            "--independent-work", "no",
            "--can-discover", "no",
            "--discovery-rounds-completed", "12",
            "--discovery-rounds-since-last-novel", "4",
            "--discovery-exhausted", "yes",
            "--next-axis-available", "no",
        )
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertFalse(result["finalization_allowed"])
        self.assertEqual(result["required_action"], "DISCOVER_AGAIN")
        self.assertNotIn("discovery_exhausted_after_minimum_rounds", result["stop_reasons"])

    def test_run_deadline_handoff_guard_still_allows_stop(self):
        result = run_gate(
            "--worker-kind", "discovery",
            "--seconds-to-run-deadline", "600",
            "--independent-work", "no",
            "--can-discover", "no",
        )
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertIn("run_deadline_within_handoff_guard", result["stop_reasons"])

    def test_canonical_read_failure_remains_abnormal_stop(self):
        result = run_gate(
            "--worker-kind", "discovery",
            "--seconds-to-run-deadline", "1200",
            "--github-read", "no",
            "--independent-work", "no",
            "--can-discover", "no",
        )
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertIn("github_read_unavailable_for_repo_state", result["stop_reasons"])


if __name__ == "__main__":
    unittest.main()
