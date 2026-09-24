import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]


class WorkflowCleanupSemanticsTests(unittest.TestCase):
    def test_citation_schema_is_persistent_not_runtime_patched(self):
        workflow = (ROOT / ".github/workflows/citation-graph-backfill.yml").read_text(encoding="utf-8")
        self.assertNotIn("Install citation schema hooks", workflow)
        self.assertNotIn("Commit schema and graph hooks", workflow)
        self.assertNotIn("could not replace legacy _citation_counts()", workflow)

        survey = (ROOT / ".survey/scripts/survey.py").read_text(encoding="utf-8")
        template = (ROOT / ".survey/templates/paper.md").read_text(encoding="utf-8")
        self.assertIn("for family in PAPER_FAMILIES", survey)
        self.assertIn("citation_counts_from_view_records", survey)
        for key in ("references:", "references_checked_at:", "references_source:", "references_total:"):
            self.assertIn(key, template)

    def test_citation_backfill_configures_commit_identity(self):
        workflow = (ROOT / ".github/workflows/citation-graph-backfill.yml").read_text(encoding="utf-8")
        self.assertIn("git config user.name 'citation-graph[bot]'", workflow)
        self.assertIn("git config user.email 'citation-graph[bot]@users.noreply.github.com'", workflow)

    def test_update_helper_shares_background_writer_concurrency(self):
        workflow = (ROOT / ".github/workflows/update-helper.yml").read_text(encoding="utf-8")
        self.assertIn("group: survey-background-main", workflow)
        self.assertNotIn("group: survey-helper-main", workflow)

    def test_survey_helper_has_no_retired_transport_paths(self):
        workflow = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertNotIn("chat-inbox.json", workflow)
        self.assertNotIn("reusable_transport_baseline.py", workflow)
        self.assertNotIn("preflight_chat_record.py", workflow)
        self.assertNotIn("assemble_research_record.py --repo-root", workflow)
        self.assertNotIn("normalize_v10_jobs.py", workflow)
        self.assertNotIn("apply_offline_job_seed.py", workflow)
        self.assertNotIn("ensure_dashboard_history.py", workflow)
        self.assertNotIn("normalize_required_metadata.py", workflow)
        self.assertNotIn("workflow_version': 9", workflow)

        validator = (ROOT / ".survey/scripts/assemble_research_record.py").read_text(encoding="utf-8")
        self.assertIn("def validate_record(", validator)
        self.assertIn("MAX_SLOT_BYTES", validator)
        self.assertNotIn("chat-inbox.json", validator)
        self.assertNotIn("chat-payload.md", validator)
        self.assertNotIn("def assemble(", validator)

        reference_pool = (ROOT / ".survey/scripts/reference_pool.py").read_text(encoding="utf-8")
        self.assertNotIn("DEFAULT_LEDGER =", reference_pool)
        self.assertNotIn('--ledger", help="deprecated alias', reference_pool)

        worker = (ROOT / ".survey/scripts/queue_worker.py").read_text(encoding="utf-8")
        self.assertIn("workflow v10", worker)
        self.assertNotIn("Queue-oriented survey state worker (workflow v9)", worker)
        self.assertNotIn("reconcile_legacy_identity_deltas", worker)

    def test_worker_router_is_single_worker_policy(self):
        readme = (ROOT / ".survey/docs/survey-workflow/README.md").read_text(encoding="utf-8")
        router = (ROOT / ".survey/docs/survey-workflow/worker-router.md").read_text(encoding="utf-8")
        implementation_index = (ROOT / ".survey/docs/survey-workflow/implementation-index.md").read_text(encoding="utf-8")

        self.assertIn("唯一の人間向け正本", readme)
        self.assertIn("手順書ではなく入力データ", readme)
        self.assertIn("candidate_inventory >= RESEARCH_DISCOVERY_THRESHOLD", router)
        self.assertIn("candidate_inventory < RESEARCH_DISCOVERY_THRESHOLD", router)
        self.assertNotIn("overflow research mode", router)
        self.assertIn("schema_version: 3", router)
        self.assertIn("target_unseen: 20", router)
        self.assertIn("これはワーカー実行手順ではない", implementation_index)
        self.assertIn("実装の所在だけ", implementation_index)

        retired_worker_surfaces = [
            ".survey/docs/survey-workflow/always-on-worker.md",
            ".survey/docs/survey-workflow/backlog-resilience.md",
            ".survey/docs/survey-workflow/candidate-buffer-policy.md",
            ".survey/docs/survey-workflow/claim-serial-policy.md",
            ".survey/docs/survey-workflow/discovery-continuation-policy.md",
            ".survey/docs/survey-workflow/continuation-policy.json",
            ".survey/docs/survey-workflow/discovery-exhaustive-run-policy.md",
            ".survey/docs/survey-workflow/discovery-search-filter.md",
            ".survey/docs/survey-workflow/discovery-search-loop.md",
            ".survey/docs/survey-workflow/discovery-specialist-worker.md",
            ".survey/docs/survey-workflow/fallback-routing.md",
            ".survey/docs/survey-workflow/run-liveness-policy.md",
            ".github/workflows/manual-library-recovery.yml",
            ".github/workflows/manual-serverlesslora-library-recovery.yml",
            ".github/workflows/library-fallback-bundle-replay.yml",
            "docs/superpowers/plans/2026-09-14-parallel-submission-batch.md",
            "docs/superpowers/plans/2026-09-15-fallback-recovery-loop.md",
            "docs/superpowers/plans/2026-09-17-claim-fast-wait.md",
        ]
        for rel in retired_worker_surfaces:
            with self.subTest(path=rel):
                self.assertFalse((ROOT / rel).exists(), rel)

    def test_retired_compatibility_and_one_shot_repair_files_are_absent(self):
        retired = [
            ".survey/scripts/normalize_v10_jobs.py",
            ".survey/scripts/reusable_transport_baseline.py",
            ".survey/scripts/preflight_chat_record.py",
            ".survey/scripts/append_research_throughput_status.py",
            ".survey/scripts/refine_status_observability.py",
            ".survey/scripts/apply_offline_job_seed.py",
            ".survey/scripts/ensure_dashboard_history.py",
            ".survey/scripts/normalize_required_metadata.py",
            ".survey/tests/test_normalize_required_metadata.py",
            ".survey/work-queue/transport/offline-job-seed.json",
            ".survey/tests/test_reusable_transport_baseline.py",
            ".survey/tests/test_legacy_scheduled_chat_lease_cap.py",
            ".github/workflows/repair-corrupted-lineages.yml",
            ".survey/scripts/repair_corrupted_lineages.py",
            ".survey/tests/test_repair_corrupted_lineages.py",
            ".survey/work-queue/submissions/chat-inbox.json",
            ".survey/work-queue/results/chat-inbox.json",
            ".survey/docs/survey-workflow/handoff-2026-09-11-metadata-backfill.md",
            ".survey/docs/survey-workflow/queue-v10.md",
        ]
        for rel in retired:
            with self.subTest(path=rel):
                self.assertFalse((ROOT / rel).exists(), rel)

    def test_blocked_retry_has_no_retired_attempt_alias(self):
        blocked_retry = (ROOT / ".survey/scripts/blocked_retry.py").read_text(encoding="utf-8")
        self.assertIn("DORMANT_AFTER_ATTEMPTS", blocked_retry)
        self.assertNotIn("MAX_BLOCKED_ATTEMPTS", blocked_retry)
        self.assertNotIn("blocked_permanent", blocked_retry)
        self.assertNotIn("legacy_permanent", blocked_retry)
        claim_worker = (ROOT / ".survey/scripts/claim_worker.py").read_text(encoding="utf-8")
        self.assertNotIn("_normalize_legacy_scheduled_chat_leases", claim_worker)
        self.assertNotIn("scheduled-chat-llm-survey", claim_worker)
        full_gc = (ROOT / ".survey/scripts/full_gc.py").read_text(encoding="utf-8")
        self.assertNotIn("chat-inbox.json", full_gc)
        self.assertNotIn("chat-payload.md", full_gc)
        self.assertNotIn("blocked_permanent", full_gc)

    def test_survey_build_has_no_training_list_migration(self):
        survey = (ROOT / ".survey/scripts/survey.py").read_text(encoding="utf-8")
        self.assertNotIn("_migrate_legacy_training_list", survey)
        self.assertNotIn("_legacy_title", survey)
        self.assertNotIn("_legacy_summary", survey)
        self.assertNotIn("old hand-written training paper list", survey)

    def test_repository_checker_requires_only_current_worker_docs(self):
        checker = (ROOT / ".survey/scripts/check_repository.py").read_text(encoding="utf-8")
        self.assertIn(".survey/docs/survey-workflow/worker-router.md", checker)
        self.assertNotIn(".survey/docs/survey-workflow/fallback-routing.md", checker)
        self.assertNotIn(".survey/docs/survey-workflow/backlog-resilience.md", checker)

    def test_repository_checker_uses_current_daily_maintenance_contract(self):
        checker = (ROOT / ".survey/scripts/check_repository.py").read_text(encoding="utf-8")
        self.assertNotIn("cadence_runs", checker)
        self.assertNotIn("runs_since_maintenance", checker)
        self.assertIn("maintenance_pending", checker)
        self.assertIn("scheduled_chat_0830_jst_30_worker", checker)
        self.assertIn("daily_0830_jst", checker)

    def test_maintenance_refreshes_metadata_coverage_before_health(self):
        workflow = (ROOT / ".github/workflows/maintenance.yml").read_text(encoding="utf-8")
        metadata_command = (
            "python .survey/scripts/audit_metadata_coverage.py --repo-root . "
            "--json-out .survey/reports/metadata-coverage-latest.json --strict"
        )
        self.assertIn(metadata_command, workflow)
        self.assertLess(workflow.index(metadata_command), workflow.index("python .survey/scripts/maintenance_health.py"))

    def test_repository_regression_runs_live_structural_checks(self):
        workflow = (ROOT / ".github/workflows/repository-tests.yml").read_text(encoding="utf-8")
        metadata_command = (
            "python .survey/scripts/audit_metadata_coverage.py --repo-root . "
            "--json-out /tmp/metadata-coverage.json --strict"
        )
        inventory_command = "python .survey/scripts/build_repository_inventory.py"
        consistency_command = "python .survey/scripts/check_repository.py"
        self.assertIn(metadata_command, workflow)
        self.assertIn(inventory_command, workflow)
        self.assertIn(consistency_command, workflow)
        self.assertLess(workflow.index(metadata_command), workflow.index(consistency_command))
        self.assertLess(workflow.index(inventory_command), workflow.index(consistency_command))


if __name__ == "__main__":
    unittest.main()
