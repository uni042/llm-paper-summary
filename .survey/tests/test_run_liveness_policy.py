import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs" / "survey-workflow"


class RunLivenessPolicyTests(unittest.TestCase):
    def test_canonical_policy_covers_each_async_wait_with_30_second_repeat(self):
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
                start = text.index(heading)
                end = text.find("\n## ", start + len(heading))
                if end == -1:
                    end = len(text)
                body = text[start:end]
                self.assertIn("30秒待機", body)
                self.assertIn("同じ", body)
                self.assertIn("繰り返", body)

    def test_final_response_follows_deterministic_permit_and_next_action(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        self.assertIn("continuation_gate.py", text)
        self.assertIn("run_finalization_gate.py", text)
        self.assertIn("MAY_FINALIZE", text)
        self.assertIn("finalization_permit.issued=true", text)
        self.assertIn("next_action", text)
        self.assertIn("worker自身に「時間まで絶対に終わるな」という主観的な継続判断は要求しない", text)
        self.assertIn("存在しないエラー", text)
        self.assertIn("事前にそれを予測してstop理由へ変換しない", text)

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
        self.assertIn("30秒待機を新しい同期障壁にしない", text)


if __name__ == "__main__":
    unittest.main()
