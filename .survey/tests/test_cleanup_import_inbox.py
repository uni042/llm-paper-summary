#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cleanup_import_inbox as cleanup


class CleanupImportInboxTests(unittest.TestCase):
    def test_deletes_non_markdown_pending_research_junk(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / ".survey/import-inbox/pending/research"
            pending.mkdir(parents=True)
            junk = pending / "undefined--undefined"
            junk.write_text("The requested file reference is not currently visible.", encoding="utf-8")

            self.assertEqual(cleanup.cleanup_pending_research_junk(root), 1)
            self.assertFalse(junk.exists())
            receipts = list((root / ".survey/import-inbox/results/cleanup").glob("*.json"))
            self.assertEqual(len(receipts), 1)
            payload = json.loads(receipts[0].read_text(encoding="utf-8"))
            self.assertEqual(
                payload["events"][-1]["status"],
                "discarded_pending_research_junk",
            )

    def test_deletes_blocked_research_when_success_result_exists(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            blocked = root / ".survey/import-inbox/blocked/research"
            blocked.mkdir(parents=True)
            source = blocked / "paper.md"
            source.write_text(
                """---
canonical_id: arXiv:2609.00001
title: Example
---
# Example
""",
                encoding="utf-8",
            )
            results = root / ".survey/import-inbox/results/research"
            results.mkdir(parents=True)
            (results / "done.json").write_text(
                json.dumps(
                    {
                        "status": "imported",
                        "canonical_id": "arXiv:2609.00001",
                    }
                ),
                encoding="utf-8",
            )

            counts = cleanup.recover_blocked_research(root)
            self.assertEqual(counts["stale_deleted"], 1)
            self.assertFalse(source.exists())

    def test_requeues_complete_blocked_research_once(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            blocked = root / ".survey/import-inbox/blocked/research"
            blocked.mkdir(parents=True)
            source = blocked / "paper.md"
            source.write_text(
                """---
canonical_id: arXiv:2609.00002
title: Example
---
# Example
""",
                encoding="utf-8",
            )
            audit = SimpleNamespace(status="PASS", failures=[], japanese_ratio=1.0)
            with mock.patch.object(cleanup.inbox, "research_metadata_failures", return_value=[]), \
                 mock.patch.object(cleanup.inbox.resolve_paper_identity, "resolve", return_value={"status": "missing"}), \
                 mock.patch.object(cleanup.inbox.paper_quality_gate, "inspect_rendered_paper", return_value=audit):
                counts = cleanup.recover_blocked_research(root)

            self.assertEqual(counts["requeued"], 1)
            retries = list((root / ".survey/import-inbox/pending/research").glob("retry-research-*.md"))
            self.assertEqual(len(retries), 1)
            self.assertFalse(source.exists())

    def test_defers_conflicting_research_retry_without_data_loss(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            blocked = root / ".survey/import-inbox/blocked/research"
            pending = root / ".survey/import-inbox/pending/research"
            blocked.mkdir(parents=True)
            pending.mkdir(parents=True)
            source = blocked / "losparse.md"
            blocked_bytes = b"---\\ncanonical_id: arXiv:2306.11222\\ntitle: LoSparse\\n---\\n# Original blocked revision\\n"
            # Use real newlines, not escaped backslash sequences.
            blocked_bytes = blocked_bytes.replace(b"\\\\n", b"\\n")
            source.write_bytes(blocked_bytes)
            retry = pending / cleanup._safe_retry_name(cleanup.RESEARCH_RETRY_PREFIX, source)
            new_revision = b"---\\ncanonical_id: arXiv:2306.11222\\n---\\n# Newer pending revision\\n"
            new_revision = new_revision.replace(b"\\\\n", b"\\n")
            retry.write_bytes(new_revision)

            with mock.patch.object(cleanup.inbox, "research_metadata_failures", return_value=[]):
                counts = cleanup.recover_blocked_research(root)

            self.assertEqual(counts["collision_deferred"], 1)
            self.assertEqual(counts["requeued"], 0)
            self.assertEqual(source.read_bytes(), blocked_bytes)
            self.assertEqual(retry.read_bytes(), new_revision)
            receipt = root / ".survey/import-inbox/results/cleanup/latest.json"
            events = json.loads(receipt.read_text(encoding="utf-8"))["events"]
            self.assertEqual(events[-1]["status"], "deferred_blocked_research_retry_collision")
            self.assertEqual(events[-1]["canonical_id"], "arXiv:2306.11222")

    def test_requeues_legacy_blocked_discovery(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            try:
                os.chdir(root)
                blocked = root / ".survey/import-inbox/blocked/discovery"
                blocked.mkdir(parents=True)
                source = blocked / "legacy.json"
                source.write_text(
                    json.dumps(
                        {
                            "schema_version": 2,
                            "artifact_type": "discovery_run",
                            "run_key": "legacy-run",
                            "record_count": 1,
                            "records": [
                                {
                                    "classification": "unrelated",
                                    "canonical_id": "arXiv:2609.00003",
                                    "reason": "not relevant",
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )

                counts = cleanup.recover_blocked_discovery(root)
                self.assertEqual(counts["legacy_requeued"], 1)
                retries = list(
                    (root / ".survey/import-inbox/pending/discovery").glob(
                        "retry-legacy-block-*.json"
                    )
                )
                self.assertEqual(len(retries), 1)
                self.assertFalse(source.exists())
            finally:
                os.chdir(original_cwd)

    def test_discards_provider_only_gap_with_tombstone(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            try:
                os.chdir(root)
                blocked = root / ".survey/import-inbox/blocked/discovery-provider"
                blocked.mkdir(parents=True)
                source = blocked / "provider.json"
                source.write_text(
                    json.dumps(
                        {
                            "schema_version": 2,
                            "artifact_type": "discovery_run",
                            "run_key": "provider-gap",
                            "provider_gap_ids": ["OpenReview:abcdefghij"],
                            "record_count": 1,
                            "records": [
                                {
                                    "classification": "accept",
                                    "canonical_id": "OpenReview:abcdefghij",
                                    "identity_tokens": ["OpenReview:abcdefghij"],
                                    "title": "Hard provider-only paper",
                                    "reason": "provider unavailable",
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )

                counts = cleanup.recover_blocked_discovery(root)
                self.assertEqual(counts["hard_deleted"], 1)
                self.assertFalse(source.exists())
                tomb = root / ".survey/import-inbox/results/discovery-provider/provider.json"
                self.assertTrue(tomb.exists())
                payload = json.loads(tomb.read_text(encoding="utf-8"))
                self.assertEqual(payload["status"], "discarded_unresolved_provider")
                self.assertEqual(payload["canonical_ids"], ["OpenReview:abcdefghij"])
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
