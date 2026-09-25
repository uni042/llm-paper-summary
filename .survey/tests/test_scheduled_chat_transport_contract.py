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

    def test_transport_stop_requires_health_probe_contract(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            ".survey/work-queue/transport/health-probe.json",
            text,
        )
        self.assertIn(
            "transport_health_probe_attempted=true",
            text,
        )
        self.assertIn(
            "transport_health_probe_succeeded=false",
            text,
        )
        self.assertIn(
            "既存GitHub file updateだけ",
            text,
        )
        self.assertIn(
            "新しいrun-state requestのcreateを要求しない",
            text,
        )

    def test_status_only_rejection_uses_worker_control_before_health_probe(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            ".survey/work-queue/transport/worker-control/<worker_id>.json",
            text,
        )
        self.assertIn(
            "status-only createが1回拒否されたら、同じcreateを連打せずこのupdate-only第2経路を試す。",
            text,
        )
        self.assertIn(
            "worker-control update自体もplatform safetyで拒否された場合だけ、第3経路として従来のhealth-probe update-only quarantineへ進む。",
            text,
        )
        self.assertIn("foreground_guard", text)

    def test_completed_submission_cannot_bypass_preflight(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn(
            "completed immutable descriptor writeも行わず",
            text,
        )
        self.assertIn(
            "preflight_result",
            text,
        )
        self.assertIn(
            "submission processorが拒否する",
            text,
        )

    def test_scheduled_chat_specific_relay_is_not_the_default(self):
        text = ROUTER.read_text(encoding="utf-8")
        self.assertIn("Scheduled Chat固有の別transportを設けない。", text)
        self.assertIn("Library fallback", text)


if __name__ == "__main__":
    unittest.main()
