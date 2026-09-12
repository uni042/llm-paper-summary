from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DiscoverySpecialistPolicyTest(unittest.TestCase):
    def test_specialist_policy_requires_continuation_until_hard_stop(self) -> None:
        specialist = (ROOT / ".survey/docs/survey-workflow/discovery-specialist-worker.md").read_text(encoding="utf-8")
        buffer_policy = (ROOT / ".survey/docs/survey-workflow/candidate-buffer-policy.md").read_text(encoding="utf-8")
        continuous = (ROOT / ".survey/docs/survey-workflow/continuous-discovery-policy.md").read_text(encoding="utf-8")
        combined = specialist + "\n" + buffer_policy + "\n" + continuous

        for phrase in (
            "在庫水位は停止条件ではない",
            "固定ラウンド上限を設けない",
            "空振り・全重複・低採用率は停止理由にしない",
            "単一ソースの障害・rate limitは停止理由にしない",
            "GitHubとLibraryの両方へ耐久保存できない",
            "実行上限",
            "有望な独立探索軸を合理的に使い切った",
        ):
            self.assertIn(phrase, combined)

        self.assertIn("通常論文workerのdiscoveryを停止・縮小しない", buffer_policy)


if __name__ == "__main__":
    unittest.main()
