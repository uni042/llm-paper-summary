import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
ROUTER = ROOT / ".survey" / "docs" / "survey-workflow" / "worker-router.md"


class ScheduledChatTransportContractTests(unittest.TestCase):
    def test_direct_github_connector_remains_canonical_transport(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            "このGitHub connector直結方式をScheduled Chatの既定・継続transportとする。",
            text,
        )
        self.assertIn(
            "通常のGitHub file create/update → GitHub Actions fast lane → result読取",
            text,
        )
        self.assertIn(
            "明示的なユーザー指示がない限り、正規transportの変更ではなく既存経路の修復を優先する。",
            text,
        )

    def test_scheduled_chat_specific_relay_is_not_the_default(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("Scheduled Chat固有の別transportを設けない。", text)
        self.assertIn("Library fallback", text)


if __name__ == "__main__":
    unittest.main()
