import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs" / "survey-workflow"
SCRIPTS = ROOT / "scripts"


class RunLivenessPolicyTests(unittest.TestCase):
    def test_router_and_gates_use_10_second_real_time_polling_until_terminal(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")

        self.assertIn("10秒", router)
        self.assertIn("実時間", router)
        self.assertIn("同一target", router)
        self.assertIn("ASYNC_WAIT_POLL_SECONDS = 10", continuation)
        self.assertIn("repeat_until_result_or_terminal_hard_stop", continuation)
        self.assertIn("ASYNC_WAIT_POLL_SECONDS = 10", finalization)
        self.assertIn("repeated until the", finalization)
        self.assertIn("terminal state", finalization)

    def test_waiting_is_not_an_unnecessary_synchronization_barrier(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        self.assertIn("不要な同期障壁にしない", router)
        self.assertIn("wait_10_real_seconds", continuation)

    def test_old_30_second_contract_is_absent(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")
        self.assertNotIn("30秒", router)
        self.assertNotIn("30-second", continuation)
        self.assertNotIn("30-second", finalization)

    def test_final_response_requires_deterministic_permit(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")
        self.assertIn("run_finalization_gate.py", router)
        self.assertIn("final response", router)
        self.assertIn("MAY_FINALIZE", finalization)
        self.assertIn("finalization_permit", finalization)
        self.assertIn("Final response is forbidden without an issued permit", finalization)

    def test_router_does_not_depend_on_retired_worker_policy_docs(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        retired = (
            "always-on-worker.md",
            "claim-serial-policy.md",
            "fallback-routing.md",
            "candidate-buffer-policy.md",
            "discovery-specialist-worker.md",
            "run-liveness-policy.md",
        )
        for name in retired:
            with self.subTest(name=name):
                self.assertNotIn(name, router)
        self.assertIn("queue-v10.md", router)
        self.assertIn("continuation_gate.py", router)


if __name__ == "__main__":
    unittest.main()
