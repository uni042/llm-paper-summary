"""Prefilter denominator must match canonical STATUS pending candidate count."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import build_worker_worklist as worklist
import citation_graph
import reference_pool
import forward_citation_state

spec = importlib.util.spec_from_file_location("render_status_dashboard_prefilter_counts", SCRIPTS / "render_status_dashboard_core.py")
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class PrefilterCountsTests(unittest.TestCase):
    def test_alias_of_existing_paper_does_not_inflate_filter_pool(self):
        paper = SimpleNamespace(
            canonical_id="arXiv:2501.00001",
            identifiers=["arXiv:2501.00001"],
            meta={"title": "Already Collected Study"},
        )
        rows = [
            {"canonical_id": "DOI:10.1111/example", "title": "Already Collected Study"},
            {"canonical_id": "arXiv:2601.00002", "title": "New Study on GPU Inference"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(citation_graph, "load_records", return_value=[paper]), \
                 patch.object(worklist, "_jobs", return_value=[]), \
                 patch.object(worklist, "_discovery_candidates", return_value=(rows, 2)), \
                 patch.object(reference_pool, "build_reference_pool", return_value={"candidate_count": 2}), \
                 patch.object(forward_citation_state, "load", return_value={"candidates": {}}):
                result = mod._structured_reference_progress(root)
        self.assertTrue(result["available"], result.get("error"))
        self.assertEqual(result["remaining"], 1)
        self.assertEqual(result["prefilter"]["unfiltered_count"], 1)
        self.assertEqual(result["prefilter"]["reviewable_count"], 1)
        self.assertEqual(result["prefilter"]["quota_eligible_count"], 1)
