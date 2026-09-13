from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / ".survey" / "scripts" / "push_retry_policy.py"
WORKFLOWS = (
    ROOT / ".github" / "workflows" / "survey-claim-fast.yml",
    ROOT / ".github" / "workflows" / "survey-submission-fast.yml",
    ROOT / ".github" / "workflows" / "status-dashboard.yml",
)


def load_policy_module():
    if not POLICY_PATH.exists():
        raise AssertionError("push_retry_policy.py must exist")
    spec = importlib.util.spec_from_file_location("push_retry_policy", POLICY_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("push_retry_policy.py could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PushRetryPolicyTests(unittest.TestCase):
    def test_classifies_conflict_transient_and_unknown_failures(self) -> None:
        policy = load_policy_module()

        self.assertEqual(
            policy.classify_push_failure(
                "! [rejected] HEAD -> main (fetch first)\n"
                "error: failed to push some refs"
            ),
            "push_conflict",
        )
        self.assertEqual(
            policy.classify_push_failure(
                "remote: Internal Server Error\n"
                "fatal: unable to access 'https://github.com/example/repo/'"
            ),
            "transient_remote_error",
        )
        self.assertEqual(
            policy.classify_push_failure("fatal: authentication failed"),
            "push_failure",
        )

    def test_retry_delay_adds_bounded_deterministic_jitter(self) -> None:
        policy = load_policy_module()

        delays = {policy.retry_delay(2, f"run-{index}") for index in range(12)}

        self.assertTrue(delays.issubset({4, 5, 6}))
        self.assertGreater(len(delays), 1)
        self.assertEqual(
            policy.retry_delay(2, "run-3"),
            policy.retry_delay(2, "run-3"),
        )

    def test_main_writers_use_shared_retry_policy(self) -> None:
        for workflow in WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                text = workflow.read_text(encoding="utf-8")
                self.assertIn(".survey/scripts/push_retry_policy.py", text)
                self.assertNotIn("sleep $((attempt * 2))", text)


if __name__ == "__main__":
    unittest.main()
