#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import process_library_import_inbox as inbox


class LibraryImportInboxTests(unittest.TestCase):
    def test_repo_relative_accepts_relative_and_absolute_paths(self) -> None:
        repo_root = Path("/tmp/example-repo").resolve()
        rel = Path(".survey/import-inbox/pending/research/paper.md")
        absolute = repo_root / rel

        self.assertEqual(
            inbox.repo_relative(rel, repo_root),
            ".survey/import-inbox/pending/research/paper.md",
        )
        self.assertEqual(
            inbox.repo_relative(absolute, repo_root),
            ".survey/import-inbox/pending/research/paper.md",
        )

    def test_oversized_discovery_run_is_retained_and_split_by_record_count(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                waiting = root / ".survey/import-inbox/waiting/discovery"
                waiting.mkdir(parents=True)
                source = waiting / "discovery-large.json"

                records = [
                    {
                        "classification": "accept",
                        "canonical_id": f"arXiv:2609.{index:05d}",
                        "reason": f"record {index}",
                    }
                    for index in range(40)
                ]
                payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "scheduled-chat-00-test-large",
                    "record_count": len(records),
                    "records": records,
                }
                original_bytes = (
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8")
                source.write_bytes(original_bytes)

                self.assertEqual(inbox.split_oversized_discovery_sources(20), 1)

                retained = (
                    root
                    / ".survey/import-inbox/retained/discovery-source/discovery-large.json"
                )
                self.assertEqual(retained.read_bytes(), original_bytes)

                chunks = sorted(waiting.glob("discovery-large--chunk-*.json"))
                self.assertEqual(len(chunks), 2)
                parsed = [json.loads(path.read_text(encoding="utf-8")) for path in chunks]
                self.assertEqual([item["record_count"] for item in parsed], [20, 20])
                self.assertTrue(
                    all(
                        item["parent_run_key"] == "scheduled-chat-00-test-large"
                        for item in parsed
                    )
                )
                self.assertEqual(
                    inbox.select_discovery_sources(20),
                    [chunks[0]],
                )
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
