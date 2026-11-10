#!/usr/bin/env python3
"""Contracts for the independent Library Discovery intake lane."""
from __future__ import annotations

import json
import re
import sys
import subprocess
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
import lineage_proposal


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

    def test_lineage_promotion_outputs_are_all_staged_by_publish(self) -> None:
        workflow = (ROOT / ".github/workflows/library-discovery-intake.yml").read_text(encoding="utf-8")
        match = re.search(
            r"publish 'library-discovery: register verified candidates' \\\n(?P<paths>.*?)\s*; then break; fi",
            workflow,
            re.DOTALL,
        )
        self.assertIsNotNone(match, "register verified candidates publish command must remain parseable")
        publish_paths = match.group("paths").replace("\\\n", " ").split()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Synthetic Test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "synthetic@example.invalid"], check=True)
            (root / ".survey/survey-state").mkdir(parents=True)
            papers = {
                f"arXiv:2601.0000{i}": {
                    "path": f"papers/inference/99-other-inference-systems/2026-{i}.md",
                    "identifiers": [f"arXiv:2601.0000{i}"],
                    "source_hash": str(i),
                }
                for i in range(1, 5)
            }
            (root / ".survey/survey-state/paper-identity-index.json").write_text(
                json.dumps({"papers": papers, "identifier_to_canonical": {key: key for key in papers}}) + "\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text("Synthetic repository\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "synthetic base"], check=True)

            proposal = {
                "slug_tail": "synthetic-runtime-cluster",
                "title": "Synthetic Runtime Cluster",
                "description": "独立した実行時制御を主題とする複数論文の研究系統。" * 2,
                "distinctness_reason": "既存の近傍分類とは中心となる制御機構と評価対象が異なる。" * 3,
                "boundary_rule": "中心貢献が実行時制御機構の場合だけ含める。" * 2,
                "scope_includes": ["実行時制御機構"],
                "scope_excludes": ["単なるオフロード"],
                "neighbor_lineages": ["01-offload-hierarchical-memory"],
                "confidence": "high",
                "supporting_papers": [
                    {"canonical_id": f"arXiv:2601.0000{i}", "reason": "同一の主要機構"}
                    for i in range(1, 5)
                ],
            }
            promoted = lineage_proposal.consider_lineage_proposal(root, proposal, round_candidates=[])
            self.assertEqual(promoted["status"], "promoted")
            expected = {
                ".survey/config/promoted-inference-lineages.json",
                f".survey/work-queue/lineage-proposals/{promoted['proposal_id']}.json",
                f"papers/inference/{promoted['lineage']}/README.md",
            }
            self.assertTrue(all((root / path).is_file() for path in expected))

            subprocess.run(["git", "-C", str(root), "add", "-A", "--", *publish_paths], check=True)
            staged = set(subprocess.run(
                ["git", "-C", str(root), "diff", "--cached", "--name-only"],
                check=True, capture_output=True, text=True,
            ).stdout.splitlines())
            unstaged = set(subprocess.run(
                ["git", "-C", str(root), "diff", "--name-only"],
                check=True, capture_output=True, text=True,
            ).stdout.splitlines())
            self.assertTrue(expected <= staged, f"promotion outputs missing from publish staging: {expected - staged}")
            self.assertFalse(expected & unstaged, f"promotion outputs remain unstaged: {expected & unstaged}")


if __name__ == "__main__":
    unittest.main()
