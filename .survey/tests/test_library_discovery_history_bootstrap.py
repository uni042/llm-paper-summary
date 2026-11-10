#!/usr/bin/env python3
"""Keep the accelerated Discovery checkout provenance-safe."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/library-discovery-intake.yml"
QUEUE_WORKER = ROOT / ".survey/scripts/queue_worker.py"


class DiscoveryHistoryBootstrapTests(unittest.TestCase):
    def test_main_only_complete_ancestry_precedes_processing(self):
        content = WORKFLOW.read_text(encoding="utf-8")
        checkout = content.index("name: Checkout latest main")
        fast_checkout = content.index("fetch-depth: 1", checkout)
        history = content.index("git -c protocol.version=2 fetch --unshallow --filter=blob:none --no-tags origin main")
        quality = content.index("name: Validate Discovery scripts")
        self.assertLess(fast_checkout, history)
        self.assertLess(history, quality)
        self.assertNotIn("fetch-depth: 0", content)

    def test_enforcement_markers_still_verified_fail_closed(self):
        content = WORKFLOW.read_text(encoding="utf-8")
        script = QUEUE_WORKER.read_text(encoding="utf-8")
        for marker in (
            "ENFORCED",
            "ITERATIVE_ENFORCED",
            "FIXED_SOURCE_ENFORCED",
            "REFERENCE_POOL_FIRST_ENFORCED",
            "CITATION_FIRST_ENFORCED",
        ):
            self.assertIn(marker, content)
        self.assertIn('git rev-parse --is-shallow-repository', content)
        self.assertIn('git log --diff-filter=A --format=%H', content)
        self.assertIn('git merge-base --is-ancestor', content)
        self.assertIn('_precheck_result_has_workflow_provenance', script)
        self.assertIn('_git_introducing_commit', script)
        self.assertIn('validate_discovery_precheck', script)

    def test_no_quality_or_ingestion_shortcut(self):
        content = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            '--max-discovery-records 240',
            'discovery-precheck.yml',
            'process_reference_relevance_requests.py',
            '--library-discovery-only',
            '--max-submissions 64',
            'git rebase origin/main',
        ):
            self.assertIn(required, content)


if __name__ == "__main__":
    unittest.main()
