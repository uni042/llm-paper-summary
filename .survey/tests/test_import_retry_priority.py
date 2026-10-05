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


class ImportRetryPriorityTests(unittest.TestCase):
    def test_recovery_discovery_is_selected_before_fresh_backlog(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            try:
                os.chdir(root)
                waiting = root / ".survey/import-inbox/waiting/discovery"
                waiting.mkdir(parents=True)
                fresh = waiting / "20261005-r20-screen-999.json"
                retry = waiting / "retry-legacy-block-deadbeef--old.json"

                for path, canonical in (
                    (fresh, "arXiv:2609.99998"),
                    (retry, "arXiv:2609.99999"),
                ):
                    path.write_text(
                        json.dumps(
                            {
                                "records": [
                                    {
                                        "classification": "unrelated",
                                        "canonical_id": canonical,
                                        "reason": "test",
                                    }
                                ]
                            }
                        ),
                        encoding="utf-8",
                    )

                selected = inbox.select_discovery_sources(1)
                self.assertEqual([path.name for path in selected], [retry.name])
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
