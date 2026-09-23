#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import research_quality_selfcheck as selfcheck  # noqa: E402


class ResearchQualitySelfcheckTests(unittest.TestCase):
    def _descriptor(self):
        return {
            "paper_path": "papers/inference/example.md",
            "record_slots": [
                {"slot": "metadata", "path": "bank/metadata.json", "blob_sha": "abc"}
            ],
        }

    def test_pass_reuses_existing_render_and_quality_gates(self) -> None:
        quality = SimpleNamespace(status="PASS", failures=[], warnings=[])
        with tempfile.TemporaryDirectory() as td, \
             patch.object(selfcheck.prepare_completed_submission, "build", return_value=self._descriptor()) as build, \
             patch.object(selfcheck.process_immutable_submission, "render_descriptor", return_value="# rendered") as render, \
             patch.object(selfcheck.process_immutable_submission, "_precheck_paper") as precheck, \
             patch.object(selfcheck.paper_quality_gate, "inspect_rendered_paper", return_value=quality) as inspect:
            result = selfcheck.check(
                Path(td),
                kind="research",
                attempt_id="attempt-a",
                job_id="job-a",
                record_bank="a",
            )

        self.assertTrue(result["selfcheck_passed"])
        self.assertEqual(result["decision"], "READY_FOR_ASYNC_PREFLIGHT")
        build.assert_called_once()
        render.assert_called_once()
        precheck.assert_called_once()
        inspect.assert_called_once()

    def test_quality_fail_is_repair_before_async_preflight(self) -> None:
        quality = SimpleNamespace(
            status="FAIL",
            failures=["手法構成要素#1 の段落数 1 < 2"],
            warnings=[],
        )
        with tempfile.TemporaryDirectory() as td, \
             patch.object(selfcheck.prepare_completed_submission, "build", return_value=self._descriptor()), \
             patch.object(selfcheck.process_immutable_submission, "render_descriptor", return_value="# rendered"), \
             patch.object(selfcheck.process_immutable_submission, "_precheck_paper"), \
             patch.object(selfcheck.paper_quality_gate, "inspect_rendered_paper", return_value=quality):
            result = selfcheck.check(
                Path(td),
                kind="research",
                attempt_id="attempt-a",
                job_id="job-a",
                record_bank="a",
            )

        self.assertFalse(result["selfcheck_passed"])
        self.assertTrue(result["repair_required"])
        self.assertEqual(result["stage"], "rendered_paper_quality")
        self.assertIn("段落数", result["validation_errors"][0])


if __name__ == "__main__":
    unittest.main()
