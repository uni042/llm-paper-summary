from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class RunStateHotPathWorkflowContractTests(unittest.TestCase):
    def test_submission_lane_recomputes_after_push_races_and_auto_state_is_fallback_safe(self):
        text = (WORKFLOWS / "survey-submission-fast.yml").read_text(encoding="utf-8")
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("git fetch origin main", text)
        self.assertIn("git reset --hard origin/main", text)
        self.assertIn("--auto-from-descriptors-file /tmp/immutable-submissions.txt", text)
        self.assertIn("request fast lane will recover", text)
        self.assertIn("cron: '7/10 * * * *'", text)

    def test_run_state_lane_recomputes_and_auto_allocates_only_the_initial_claim(self):
        text = (WORKFLOWS / "survey-run-state.yml").read_text(encoding="utf-8")
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("git fetch origin main", text)
        self.assertIn("git reset --hard origin/main", text)
        self.assertIn("auto_claim_from_run_state.py", text)
        self.assertIn("auto_discovery_from_run_state.py", text)
        self.assertIn("changed-run-state-results.txt", text)
        self.assertIn(".survey/work-queue/discovery-precheck", text)
        self.assertIn(".survey/work-queue/discovery-preload", text)
        self.assertIn(".survey/work-queue/direct-take-results", text)
        self.assertIn(".survey/work-queue/hot-dispatch.json", text)
        self.assertIn("group: survey-claim-main", text)
        self.assertIn("recomputing unsettled requests from latest main", text)
        self.assertIn("periodic recovery will retry unsettled requests", text)
        self.assertIn("cron: '4/10 * * * *'", text)

    def test_discovery_precheck_repairs_missing_run_state_before_publication(self):
        text = (WORKFLOWS / "discovery-precheck.yml").read_text(encoding="utf-8")
        self.assertIn("ensure_discovery_run_state.py", text)
        self.assertIn("ensure_discovery_run_state.py --repo-root .", text)
        self.assertIn("derive_worker_run_state.py --repo-root .", text)
        self.assertIn(".survey/work-queue/run-state", text)

    def test_discovery_recovery_auto_advances_prepared_bank_with_push_race_recompute(self):
        text = (WORKFLOWS / "survey-discovery-recovery.yml").read_text(encoding="utf-8")
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("git reset --hard origin/main", text)
        self.assertIn("auto_advance_discovery.py", text)
        self.assertIn("--recovery-report /tmp/discovery-recovery.json", text)
        self.assertIn(".survey/work-queue/discovery-precheck", text)
        self.assertIn(".survey/work-queue/run-state", text)
        self.assertIn(".survey/work-queue/direct-take-results/discovery", text)
        self.assertIn("recomputing from latest main", text)
        self.assertNotIn("git rebase origin/main", text)

    def test_preflight_and_descriptor_materialization_keep_periodic_recovery(self):
        preflight = (WORKFLOWS / "survey-research-quality-preflight.yml").read_text(encoding="utf-8")
        builder = (WORKFLOWS / "survey-completed-builder-fast.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '8/10 * * * *'", preflight)
        self.assertIn("cron: '9/10 * * * *'", builder)
        self.assertIn("for attempt in $(seq 1 12)", preflight)
        self.assertIn("for attempt in $(seq 1 12)", builder)

    def test_claim_lane_uses_shared_fast_path_without_schedule_change(self):
        text = (WORKFLOWS / "survey-claim-fast.yml").read_text(encoding="utf-8")
        self.assertIn("claim_fast_path.py", text)
        self.assertNotIn("py_compile", text)
        self.assertIn(".survey/work-queue/run-state", text)
        self.assertIn("group: survey-claim-main", text)
        self.assertIn("cron: '3/10 * * * *'", text)
        self.assertIn("for attempt in $(seq 1 12)", text)


if __name__ == "__main__":
    unittest.main()
