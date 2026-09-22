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

    def test_claim_wait_is_productive_fast_lane_monitoring(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        guidance = (SCRIPTS / "worker_guidance.py").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")

        self.assertIn("MONITOR_CLAIM_FAST_LANE", router)
        self.assertIn("request commitから60秒未満", router)
        self.assertIn("Actions run", router)
        self.assertIn("MONITOR_CLAIM_FAST_LANE", continuation)
        self.assertIn("claim_result_pending_age_seconds", continuation)
        self.assertIn("inspect_survey_claim_fast_actions_run_for_request_commit", continuation)
        self.assertIn("MONITOR_CLAIM_FAST_LANE", guidance)
        self.assertIn("Pending claim results also require productive fast-lane monitoring", finalization)

    def test_submission_wait_uses_one_paper_delayed_barrier(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        self.assertIn("submission result待ちは**直後の1本には同期障壁ではなく、その次の論文へ進むための同期障壁**", router)
        self.assertIn("--pipeline-ahead-count", router)
        self.assertIn("WAIT_FOR_PREVIOUS_SUBMISSION_RESULT", continuation)
        self.assertIn("CLAIM_NEXT_RESEARCH_AUDIT", continuation)
        self.assertIn("wait_10_real_seconds", continuation)
        self.assertNotIn("submission result待ちは**次論文へ進むための同期障壁**", router)

    def test_old_30_second_contract_is_absent(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        continuation = (SCRIPTS / "continuation_gate.py").read_text(encoding="utf-8")
        finalization = (SCRIPTS / "run_finalization_gate.py").read_text(encoding="utf-8")
        self.assertNotIn("30秒", router)
        self.assertNotIn("30-second", continuation)
        self.assertNotIn("30-second", finalization)

    def test_async_fast_lanes_have_periodic_orphan_recovery(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        workflows = Path(__file__).resolve().parents[2] / ".github" / "workflows"
        claim = (workflows / "survey-claim-fast.yml").read_text(encoding="utf-8")
        run_state = (workflows / "survey-run-state.yml").read_text(encoding="utf-8")
        precheck = (workflows / "discovery-precheck.yml").read_text(encoding="utf-8")
        self.assertIn("3/10", claim)
        self.assertIn("4/10", run_state)
        self.assertIn("6/10", precheck)
        self.assertIn("10分周期", router)

    def test_run_state_snapshots_require_unique_request_ids(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        guidance = (SCRIPTS / "worker_guidance.py").read_text(encoding="utf-8")
        self.assertIn("各再判定snapshotでは新しい一意な `request_id`", router)
        self.assertIn("resultが既に存在するrequest_idを再利用", guidance)
        self.assertIn("同じrequest_idを待機", guidance)

    def test_worker_manual_forbids_disabling_scheduled_task_on_failure(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("Scheduled Task自体を一時停止・無効化してはならない", router)
        self.assertIn("enabled状態は維持", router)
        self.assertIn("将来runのスケジュール停止を意味しない", router)

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
        self.assertNotIn("queue-v10.md", router)
        self.assertIn("実装リファレンス", router)
        self.assertIn("補完しない", router)
        self.assertIn("continuation_gate.py", router)


if __name__ == "__main__":
    unittest.main()
