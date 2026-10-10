#!/usr/bin/env python3
"""Contracts for the independent Library Discovery intake lane."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import process_library_import_inbox as inbox
import queue_worker


class DedicatedLibraryDiscoveryIntakeTests(unittest.TestCase):
    def test_library_discovery_only_does_not_touch_research(self) -> None:
        with (
            mock.patch.object(sys, "argv", ["process_library_import_inbox.py", "--skip-research"]),
            mock.patch.object(inbox, "process_research") as research,
            mock.patch.object(inbox, "sync_returned_research_queue") as returned,
            mock.patch.object(inbox, "process_discovery", return_value=(2, 1)) as discovery,
        ):
            self.assertEqual(inbox.main(), 0)
            research.assert_not_called()
            returned.assert_not_called()
            discovery.assert_called_once()

    def test_library_research_only_does_not_touch_discovery(self) -> None:
        with (
            mock.patch.object(sys, "argv", ["process_library_import_inbox.py", "--skip-discovery"]),
            mock.patch.object(inbox, "process_research", return_value=(1, 0)) as research,
            mock.patch.object(inbox, "sync_returned_research_queue", return_value={"count": 4}),
            mock.patch.object(inbox, "process_discovery") as discovery,
        ):
            self.assertEqual(inbox.main(), 0)
            research.assert_called_once()
            discovery.assert_not_called()

    def test_library_submission_filter_precedes_bounded_budget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            submissions, results = root / "submissions", root / "results"
            submissions.mkdir()
            # Both intentionally invalid payloads produce a durable error result.
            # The filter must leave the other lane untouched, even with budget=1.
            (submissions / "a-legacy.json").write_text("{}", encoding="utf-8")
            (submissions / "libimp-test-pre01-sub01.json").write_text("{}", encoding="utf-8")
            with (
                mock.patch.object(queue_worker, "ROOT", root),
                mock.patch.object(queue_worker, "SUBMISSIONS", submissions),
                mock.patch.object(queue_worker, "RESULTS", results),
            ):
                queue_worker.process_submissions({}, 1, library_discovery_only=True)
                self.assertTrue((results / "libimp-test-pre01-sub01.json").exists())
                self.assertFalse((results / "a-legacy.json").exists())
                queue_worker.process_submissions({}, 1, exclude_library_discovery=True)
                self.assertTrue((results / "a-legacy.json").exists())

    def test_workflow_preserves_existing_uploader_paths_and_precheck(self) -> None:
        fast = (ROOT / ".github/workflows/library-discovery-intake.yml").read_text(encoding="utf-8")
        research = (ROOT / ".github/workflows/library-import.yml").read_text(encoding="utf-8")
        for part in ("pending/discovery/**", "waiting/discovery/**", "--skip-research",
                     "discovery-precheck.yml", "--library-discovery-only"):
            self.assertIn(part, fast)
        self.assertNotIn("render_status_dashboard.py", fast)
        self.assertNotIn("refresh_under16kb_reaudit_queue.py", fast)
        self.assertIn("--skip-discovery", research)
        self.assertIn("--exclude-library-discovery", research)
        self.assertNotIn("'pending/discovery/**'", research)


if __name__ == "__main__":
    unittest.main()
