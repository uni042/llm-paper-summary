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
        for index, heading in enumerate(sections):
            with self.subTest(heading=heading):
                start = text.index(heading)
                end = text.find("\n## ", start + len(heading))
                if end == -1:
                    end = len(text)
                body = text[start:end]
                self.assertIn("30秒待機", body)
                self.assertIn("同じ", body)
                self.assertIn("繰り返", body)

    def test_final_response_requires_deterministic_permit(self):
        text = (DOCS / "run-liveness-policy.md").read_text(encoding="utf-8")
        self.assertIn("run_finalization_gate.py", text)
        self.assertIn("MAY_FINALIZE", text)
        self.assertIn("finalization_permit", text)
        self.assertIn("許可なしにfinal responseを出してはならない", text)

    def test_specialized_docs_point_to_explicit_30_second_wait_contract(self):
        paths = [
            "claim-serial-policy.md",
            "always-on-worker.md",
            "library-publication-ack.md",
            "fallback-routing.md",
        ]
        for name in paths:
            with self.subTest(name=name):
                text = (DOCS / name).read_text(encoding="utf-8")
                self.assertIn("run-liveness-policy.md", text)
                self.assertIn("30秒", text)


if __name__ == "__main__":
    unittest.main()
