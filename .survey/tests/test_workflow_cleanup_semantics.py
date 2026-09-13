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

    def test_reusable_chat_success_is_bound_to_exact_attempt(self):
        workflow = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertIn("attempt_id = inbox.get('attempt_id')", workflow)
        self.assertIn("result.get('attempt_id') == attempt_id", workflow)
        self.assertIn("'attempt_id': attempt_id", workflow)

        worker = (ROOT / ".survey/scripts/queue_worker.py").read_text(encoding="utf-8")
        self.assertIn('result["attempt_id"] = attempt_id', worker)


if __name__ == "__main__":
    unittest.main()
