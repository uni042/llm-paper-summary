import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
ROUTER = ROOT / ".survey" / "docs" / "survey-workflow" / "worker-router.md"


class ScheduledChatTransportContractTests(unittest.TestCase):
    def test_scheduled_worker_is_library_first_and_github_read_only(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("Scheduled workerがGitHubをread-onlyで参照", text)
        self.assertIn("GitHub writeを試してLibrary失敗を回避することは禁止する。", text)
        self.assertIn("Survey GitHub ImportのWorkタスク", text)
        self.assertIn("Scheduled workerはGitHubへの `write`、`claim`", text)

    def test_current_inventory_and_quota_contract(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("E = G + D - R", text)
        self.assertIn("E > 500", text)
        self.assertIn("E <= 500", text)
        self.assertIn("完成論文を10件", text)
        self.assertIn("新規canonical identity 40件", text)

    def test_worklist_order_is_tail_first(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("専用リストの末尾から上方向", text)

    def test_work_task_verifies_before_library_cleanup(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("再取得確認できた後だけ対応Library原本を削除する", text)
        self.assertIn("1件の失敗で他の独立成果を止めない", text)

    def test_legacy_direct_transport_is_archived_not_active(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("worker-router-legacy-v10.22-direct-github.md", text)
        self.assertIn("新規Scheduled worker runの実行手順として旧資料を補完利用しない", text)


if __name__ == "__main__":
    unittest.main()
