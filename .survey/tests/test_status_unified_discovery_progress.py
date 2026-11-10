from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import reference_relevance_ledger  # noqa: E402
import render_status_dashboard_core as status_core  # noqa: E402


class UnifiedDiscoveryProgressTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        paper_dir = self.root / "papers" / "inference" / "01-test"
        paper_dir.mkdir(parents=True)
        meta = {
            "canonical_id": "arXiv:2609.00001",
            "title": "Collected Seed",
            "references": [
                {"canonical_id": "arXiv:2609.00002", "title": "Backward Pending"},
                {"canonical_id": "arXiv:2609.00003", "title": "Already Unrelated"},
                {"canonical_id": "arXiv:2609.00004", "title": "Promoted Research"},
            ],
        }
        (paper_dir / "seed.md").write_text(
            "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\nbody\n",
            encoding="utf-8",
        )

        cur = self.root / ".survey" / "work-queue" / "reference-curation"
        cur.mkdir(parents=True)
        reference_relevance_ledger.mark_unrelated(
            cur / "unrelated-papers.json",
            canonical_id="arXiv:2609.00003",
            reason="outside scope",
        )
        reference_relevance_ledger.mark_borderline(
            cur / "borderline-papers.json",
            canonical_id="arXiv:2609.00006",
            reason="weak fit",
        )

        jobs = self.root / ".survey" / "work-queue" / "jobs"
        jobs.mkdir(parents=True)
        (jobs / "job-r.json").write_text(
            json.dumps({
                "job_id": "job-r",
                "type": "research",
                "status": "ready",
                "canonical_id": "arXiv:2609.00004",
                "title": "Promoted Research",
                "source_url": "https://arxiv.org/abs/2609.00004",
            }),
            encoding="utf-8",
        )

        forward = self.root / ".survey" / "work-queue" / "forward-citation-sweep.json"
        forward.write_text(
            json.dumps({
                "schema_version": 1,
                "candidates": {
                    "same-backward": {
                        "canonical_id": "DOI:10.48550/arxiv.2609.00002",
                        "identity_tokens": [
                            "DOI:10.48550/arxiv.2609.00002",
                            "arXiv:2609.00002",
                        ],
                        "title": "Backward Pending",
                    },
                    "forward-only": {
                        "canonical_id": "arXiv:2609.00005",
                        "identity_tokens": ["arXiv:2609.00005"],
                        "title": "Forward Pending",
                    },
                    "research-alias": {
                        "canonical_id": "arXiv:2609.00004",
                        "identity_tokens": ["arXiv:2609.00004"],
                        "title": "Promoted Research",
                    },
                },
            }),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_progress_unifies_forward_backward_and_processed_states(self) -> None:
        progress = status_core._structured_reference_progress(self.root)

        self.assertTrue(progress["available"])
        self.assertEqual(progress["represented"], 1)
        self.assertEqual(progress["research"], 1)
        self.assertEqual(progress["unrelated"], 1)
        self.assertEqual(progress["borderline"], 1)
        self.assertEqual(progress["remaining"], 2)
        self.assertEqual(progress["processed"], 4)
        self.assertEqual(progress["total"], 6)
        self.assertEqual(progress["backward_pending_raw"], 2)
        self.assertEqual(progress["forward_pending_raw"], 3)
        self.assertEqual(progress["combined_pending_before_research_exclusion"], 3)

        rendered = "\n".join(status_core._render_structured_reference_progress(progress))
        self.assertIn("## 探索候補の処理状況", rendered)
        self.assertIn("| 探索候補総数 | **6** |", rendered)
        self.assertIn("| 未処理Discovery候補 | **2** |", rendered)
        self.assertNotIn("構造化references総候補", rendered)


if __name__ == "__main__":
    unittest.main()
