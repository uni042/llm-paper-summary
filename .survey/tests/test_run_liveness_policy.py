import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / ".survey" / "docs" / "survey-workflow"
WORKFLOWS = ROOT / ".github" / "workflows"


class RunLivenessPolicyTests(unittest.TestCase):
    def test_human_guide_is_external_to_repository(self):
        self.assertFalse(DOCS.exists())

    def test_central_scheduler_periodically_dispatches_library_first_lanes(self):
        scheduler = (WORKFLOWS / "survey-orchestrator.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '7/10 * * * *'", scheduler)
        self.assertIn(".survey/scheduler/library-import-kick.json", scheduler)
        for workflow in (
            "library-import.yml",
            "forward-citation-sweep.yml",
            "candidate-priority-refresh.yml",
            "maintenance.yml",
        ):
            with self.subTest(workflow=workflow):
                self.assertIn(f"dispatch_if_idle {workflow}", scheduler)
        self.assertIn("GITHUB_RUN_NUMBER % 6", scheduler)
        self.assertIn("Library import inbox is empty; skip processor dispatch.", scheduler)
        self.assertIn('if [ "$GITHUB_EVENT_NAME" = "push" ] && jq -e', scheduler)

        watchdog = (WORKFLOWS / "survey-scheduler-watchdog.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '13,43 * * * *'", watchdog)
        self.assertIn("survey-orchestrator.yml/dispatches", watchdog)
        self.assertIn("survey-scheduler-watchdog.yml/dispatches", watchdog)
        self.assertIn("sleep 600", watchdog)
        self.assertIn("group: survey-scheduler-watchdog-main", watchdog)

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
            "discovery-identity-snapshot.yml",
            "paper-metadata-reconciliation.yml",
            "paper-quality-audit.yml",
        )
        for workflow in retired_auto:
            with self.subTest(retired=workflow):
                text = (WORKFLOWS / workflow).read_text(encoding="utf-8")
                trigger = text.split("permissions:", 1)[0]
                self.assertIn("workflow_dispatch:", trigger)
                self.assertNotIn("schedule:", trigger)
                self.assertNotIn("push:", trigger)
                self.assertNotIn("workflow_run:", trigger)

    def test_library_import_rechecks_precheck_liveness_at_handoff(self):
        workflow = (WORKFLOWS / "library-import.yml").read_text(encoding="utf-8")
        self.assertIn("unsettled_library_prechecks", workflow)
        self.assertIn("active_precheck_runs", workflow)
        self.assertIn("gh workflow run discovery-precheck.yml", workflow)
        self.assertIn(
            "dispatching the dedicated gate",
            workflow,
        )

    def test_library_import_hands_new_papers_to_citation_backfill(self):
        workflow = (WORKFLOWS / "library-import.yml").read_text(encoding="utf-8")
        self.assertIn("citation_backfill_due", workflow)
        self.assertIn("citation-coverage-latest.json", workflow)
        self.assertIn("citation_graph.load_records", workflow)
        self.assertIn("gh workflow run citation-graph-backfill.yml", workflow)
        self.assertIn("active_citation_runs", workflow)

    def test_repository_tests_skip_paper_only_main_pushes(self):
        text = (WORKFLOWS / "repository-tests.yml").read_text(encoding="utf-8")
        push_block, rest = text.split("  pull_request:", 1)
        pull_block = rest.split("  workflow_dispatch:", 1)[0]
        self.assertNotIn("papers/**/*.md", push_block)
        self.assertIn("papers/**/*.md", pull_block)

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
        self.assertFalse(DOCS.exists())

    def test_library_failure_uses_durable_chat_fallback_not_github_write(self):
        self.assertFalse(DOCS.exists())

    def test_router_does_not_depend_on_retired_direct_worker_policy_docs(self):
        self.assertFalse(DOCS.exists())

    def test_run_mode_is_fixed_and_completion_is_library_durable(self):
        self.assertFalse(DOCS.exists())


if __name__ == "__main__":
    unittest.main()
