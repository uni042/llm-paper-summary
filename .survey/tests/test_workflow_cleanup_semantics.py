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
        queue = (ROOT / ".survey/docs/survey-workflow/queue-v10.md").read_text(encoding="utf-8")
        self.assertIn("for family in PAPER_FAMILIES", survey)
        self.assertIn("citation_counts_from_view_records", survey)
        for key in ("references:", "references_checked_at:", "references_source:", "references_total:"):
            self.assertIn(key, template)
            self.assertIn(key.rstrip(":"), queue)

    def test_citation_backfill_configures_commit_identity(self):
        workflow = (ROOT / ".github/workflows/citation-graph-backfill.yml").read_text(encoding="utf-8")
        self.assertIn("git config user.name 'citation-graph[bot]'", workflow)
        self.assertIn("git config user.email 'citation-graph[bot]@users.noreply.github.com'", workflow)

    def test_update_helper_shares_background_writer_concurrency(self):
        workflow = (ROOT / ".github/workflows/update-helper.yml").read_text(encoding="utf-8")
        self.assertIn("group: survey-background-main", workflow)
        self.assertNotIn("group: survey-helper-main", workflow)

    def test_survey_helper_has_no_reusable_chat_or_v10_normalizer_path(self):
        workflow = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertNotIn("chat-inbox.json", workflow)
        self.assertNotIn("reusable_transport_baseline.py", workflow)
        self.assertNotIn("preflight_chat_record.py", workflow)
        self.assertNotIn("assemble_research_record.py --repo-root", workflow)
        self.assertNotIn("normalize_v10_jobs.py", workflow)
        self.assertNotIn("workflow_version': 9", workflow)

        worker = (ROOT / ".survey/scripts/queue_worker.py").read_text(encoding="utf-8")
        self.assertIn("workflow v10", worker)
        self.assertNotIn("Queue-oriented survey state worker (workflow v9)", worker)

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
