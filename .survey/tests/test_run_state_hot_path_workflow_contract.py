from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class RunStateHotPathWorkflowContractTests(unittest.TestCase):
    def _trigger(self, name: str) -> str:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        return text.split("permissions:", 1)[0]

    def test_submission_lane_is_manual_recovery_only(self):
        text = (WORKFLOWS / "survey-submission-fast.yml").read_text(encoding="utf-8")
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("list_unsettled_immutable_submissions.py", text)
        trigger = self._trigger("survey-submission-fast.yml")
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("push:", trigger)
        self.assertNotIn("schedule:", trigger)

    def test_run_state_lane_is_manual_recovery_only(self):
        text = (WORKFLOWS / "survey-run-state.yml").read_text(encoding="utf-8")
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("auto_claim_from_run_state.py", text)
        self.assertIn("auto_discovery_from_run_state.py", text)
        trigger = self._trigger("survey-run-state.yml")
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("push:", trigger)
        self.assertNotIn("schedule:", trigger)

    def test_discovery_precheck_repairs_missing_run_state_before_publication(self):
        text = (WORKFLOWS / "discovery-precheck.yml").read_text(encoding="utf-8")
        self.assertIn("ensure_discovery_run_state.py", text)
        self.assertIn("derive_worker_run_state.py --repo-root .", text)
        self.assertIn(".survey/work-queue/run-state", text)
        self.assertIn("group: discovery-precheck-main", text)

    def test_discovery_precheck_recovers_normal_provider_failure_in_same_lane(self):
        text = (WORKFLOWS / "discovery-precheck.yml").read_text(encoding="utf-8")
        self.assertIn("recover_discovery_provider_failures.py", text)
        self.assertIn("discovery-provider-failover-requests.txt", text)
        self.assertIn("--verify-only", text)
        self.assertIn("provider-failover batch", text)

    def test_legacy_direct_worker_lanes_are_not_periodically_dispatched(self):
        orchestrator = (WORKFLOWS / "survey-orchestrator.yml").read_text(encoding="utf-8")
        for retired in (
            "survey-run-state.yml",
            "survey-submission-fast.yml",
            "survey-research-quality-preflight.yml",
            "survey-completed-builder-fast.yml",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(f"dispatch_if_idle {retired}", orchestrator)
                trigger = self._trigger(retired)
                self.assertNotIn("push:", trigger)
                self.assertNotIn("schedule:", trigger)

    def test_dedicated_orchestrator_owns_periodic_schedule(self):
        text = (WORKFLOWS / "survey-orchestrator.yml").read_text(encoding="utf-8")
        claim = (WORKFLOWS / "survey-claim-fast.yml").read_text(encoding="utf-8")
        self.assertIn("group: survey-orchestrator-main", text)
        self.assertIn("cron: '7/10 * * * *'", text)
        self.assertIn(".survey/scheduler/library-import-kick.json", text)
        self.assertIn("dispatch_if_idle library-import.yml", text)
        self.assertNotIn("schedule:", self._trigger("survey-claim-fast.yml"))
        self.assertIn("claim_fast_path.py", claim)


if __name__ == "__main__":
    unittest.main()
