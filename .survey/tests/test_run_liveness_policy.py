import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs" / "survey-workflow"


class RunLivenessPolicyTests(unittest.TestCase):
    @staticmethod
    def _section(text: str, heading: str) -> str:
        start = text.index(heading)
        end = text.find("\n## ", start + len(heading))
        if end == -1:
            end = len(text)
        return text[start:end]

    def test_each_required_async_wait_uses_10_second_real_time_polling_until_terminal(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        sections = [
            "## 2. Claim result待機",
            "## 3. Research / Audit submission result待機",
            "## 4. Library publication ACK待機",
            "## 5. Fallback replay / materialization待機",
            "## 6. GitHub Actions / その他の非同期結果待機",
        ]
        for heading in sections:
            with self.subTest(heading=heading):
                body = self._section(text, heading)
                self.assertIn("10秒", body)
                self.assertIn("実時間", body)
                self.assertIn("同じ", body)
                self.assertIn("terminal", body)
                self.assertIn("繰り返", body)

    def test_runtime_wait_cannot_be_replaced_by_immediate_rechecks(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        body = self._section(text, "## 7. 10秒wait loopの共通形")
        self.assertIn("runtime wait", body)
        self.assertIn("即時再取得", body)
        self.assertIn("代替", body)
        self.assertIn("10秒", body)

    def test_old_30_second_contract_is_absent(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        self.assertNotIn("30秒", text)

    def test_final_response_requires_deterministic_permit(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        self.assertIn("run_finalization_gate.py", text)
        self.assertIn("MAY_FINALIZE", text)
        self.assertIn("finalization_permit", text)
        self.assertIn("許可なしにfinal responseを出してはならない", text)

    def test_policy_preserves_specialized_contracts_without_adding_blocking_waits(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        for name in (
            "worker-router.md",
            "always-on-worker.md",
            "claim-serial-policy.md",
            "fallback-routing.md",
            "library-publication-ack.md",
        ):
            with self.subTest(name=name):
                self.assertIn(name, text)
        self.assertIn("新しい同期障壁にしない", text)


if __name__ == "__main__":
    unittest.main()
