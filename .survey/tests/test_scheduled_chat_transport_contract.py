import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
ROUTER = ROOT / ".survey" / "docs" / "survey-workflow" / "worker-router.md"


class ScheduledChatTransportContractTests(unittest.TestCase):
    def test_scheduled_worker_is_library_first_and_github_read_only(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("scheduled-chat-00", text)
        self.assertIn("scheduled-chat-30", text)
        self.assertIn("scheduled-chat-45", text)
        self.assertIn("scheduled-chat-45", text)
        self.assertIn("read-only | read/write", text)
        self.assertIn("Scheduled workerはGitHubへのclaim、reservation、submission、result", text)
        self.assertIn("Library保存不能でも完成成果を破棄しない", text)
        self.assertIn("GitHub writeをLibrary失敗回避手段として使わない", text)

    def test_current_inventory_and_quota_contract(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("収録候補論文数 > 600", text)
        self.assertIn("収録候補論文数 <= 600", text)
        self.assertIn("Research runでは新規完成Research Markdownを5件Libraryへ保存する", text)
        self.assertIn("新規canonical identity 10件を本文確認まで行い", text)
        self.assertNotIn("E = G + D - R", text)

    def test_worklist_order_is_highest_priority_first(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("rank 1がその生成時点で最も重要度スコアの高い候補", text)
        self.assertIn("rank 1から上から下へ", text)
        self.assertNotIn("候補はリスト末尾から上方向", text)

    def test_import_verifies_durable_handoff_before_library_cleanup(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("byte-preserving転送", text)
        self.assertIn("source_sha256", text)
        self.assertIn("そのLibrary成果を削除してよい", text)

    def test_legacy_direct_transport_is_not_a_current_worker_path(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("旧direct-GitHub worker運用は履歴資料", text)
        self.assertIn("新規通常runへ復活させない", text)


if __name__ == "__main__":
    unittest.main()
