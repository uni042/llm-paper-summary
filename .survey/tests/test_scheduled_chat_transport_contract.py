"""Machine-side invariants after moving human worker procedures to ChatGPT Library.

The GitHub repository intentionally contains no executable human-facing worker
router document. These tests validate only repository-owned machine contracts;
Library prose is maintained and verified through the Library workflow.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
ROUTER = ROOT / ".survey" / "docs" / "survey-workflow" / "worker-router.md"


class ScheduledChatTransportContractTests(unittest.TestCase):
    def test_worker_instructions_are_library_only(self):
        self.assertFalse(ROUTER.exists())
        self.assertFalse((ROOT / "docs/superpowers").exists())
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/LLM-paper-summary-library-first/", readme)

    def test_current_worker_quota_is_in_machine_policy(self):
        text = (ROOT / ".survey/scripts/worker_quota_policy.py").read_text(encoding="utf-8")
        self.assertIn("RESEARCH_AUDIT_MINIMUM_COMPLETIONS = 5", text)
        self.assertIn("DISCOVERY_MINIMUM_ROUNDS = 8", text)

    def test_worklists_still_exist_after_procedure_cleanup(self):
        work_queue = ROOT / ".survey/work-queue"
        for slot in ("00", "30", "45"):
            with self.subTest(slot=slot):
                self.assertTrue((work_queue / f"worker-worklist-{slot}.json").is_file())

    def test_import_processor_keeps_durable_pending_payloads(self):
        source = (ROOT / ".survey/scripts/process_library_import_inbox.py").read_text(encoding="utf-8")
        self.assertIn("retain blocked payloads in GitHub", source)
        self.assertIn("idempotent", source)
        self.assertIn("create-only", source)

    def test_no_legacy_router_is_reintroduced(self):
        self.assertFalse((ROOT / ".survey/docs").exists())
        self.assertFalse((ROOT / "docs/superpowers").exists())


if __name__ == "__main__":
    unittest.main()
