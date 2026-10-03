import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / ".survey" / "docs" / "survey-workflow"
WORKFLOWS = ROOT / ".github" / "workflows"


class RunLivenessPolicyTests(unittest.TestCase):
    def test_scheduled_worker_has_no_direct_github_wait_protocol(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("Scheduled workerはGitHubへのclaim、reservation、submission、result", router)
        self.assertIn("Library保存不能でも完成成果を破棄しない", router)
        self.assertIn("GitHub writeをLibrary失敗回避手段として使わない", router)
        self.assertNotIn("MONITOR_CLAIM_FAST_LANE", router)
        self.assertNotIn("continuation_gate.py", router)
        self.assertNotIn("run_finalization_gate.py", router)

    def test_central_scheduler_periodically_dispatches_library_first_lanes(self):
        scheduler = (WORKFLOWS / "survey-orchestrator.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '7/10 * * * *'", scheduler)
        self.assertIn(".survey/scheduler/library-import-kick.json", scheduler)
        for workflow in (
            "library-import.yml",
            "forward-citation-sweep.yml",
            "candidate-priority-refresh.yml",
        ):
            with self.subTest(workflow=workflow):
                self.assertIn(f"dispatch_if_idle {workflow}", scheduler)

        retired_auto = (
            "survey-claim-fast.yml",
            "survey-run-state.yml",
            "survey-submission-fast.yml",
            "survey-research-quality-preflight.yml",
            "survey-completed-builder-fast.yml",
            "survey-discovery-recovery.yml",
            "survey-helper.yml",
            "survey-reference-relevance-fast.yml",
            "retry-adopted-library-checkpoints.yml",
            "library-publication-ack.yml",
            "discovery-preload-local-fast.yml",
            "discovery-preload-warm.yml",
        )
        for workflow in retired_auto:
            with self.subTest(retired=workflow):
                text = (WORKFLOWS / workflow).read_text(encoding="utf-8")
                trigger = text.split("permissions:", 1)[0]
                self.assertIn("workflow_dispatch:", trigger)
                self.assertNotIn("schedule:", trigger)
                self.assertNotIn("push:", trigger)
                self.assertNotIn("workflow_run:", trigger)

    def test_event_driven_fallbacks_are_freshness_gated(self):
        for workflow_name, state_path in (
            ("forward-citation-sweep.yml", ".survey/work-queue/forward-citation-sweep.json"),
            ("candidate-priority-refresh.yml", ".survey/work-queue/candidate-priority-cache.json"),
        ):
            with self.subTest(workflow=workflow_name):
                text = (WORKFLOWS / workflow_name).read_text(encoding="utf-8")
                self.assertNotIn("- 'STATUS.md'", text)
                self.assertIn(".survey/scripts/refresh_due.py", text)
                self.assertIn(state_path, text)
                self.assertIn("--max-age-seconds 3000", text)
                self.assertIn("steps.due.outputs.run == 'true'", text)

    def test_scheduled_task_is_not_disabled_by_worker_failure(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("ユーザーの明示指示なしにScheduled Taskを停止・無効化・削除せず", router)

    def test_library_failure_uses_durable_chat_fallback_not_github_write(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("Research: 完成MarkdownをScheduled Chatへ完全添付", router)
        self.assertIn("Discovery: 10件全件を含む完成JSONをScheduled Chatへ完全添付", router)
        self.assertIn("GitHub writeをLibrary失敗回避手段として使わない", router)

    def test_router_does_not_depend_on_retired_direct_worker_policy_docs(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        retired = (
            "always-on-worker.md",
            "claim-serial-policy.md",
            "fallback-routing.md",
            "candidate-buffer-policy.md",
            "discovery-specialist-worker.md",
            "run-liveness-policy.md",
            "queue-v10.md",
        )
        for name in retired:
            with self.subTest(name=name):
                self.assertNotIn(name, router)
        self.assertIn("旧direct-GitHub worker運用は履歴資料", router)
        self.assertIn("新規通常runへ復活させない", router)

    def test_run_mode_is_fixed_and_completion_is_library_durable(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("run中に在庫が変化してもモードは固定する", router)
        self.assertIn("保存後はLibraryから再取得", router)
        self.assertIn("Researchは**1ラウンドにつき**新規完成Research Markdownを5件Libraryへ保存する", router)


if __name__ == "__main__":
    unittest.main()
