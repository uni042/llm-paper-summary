from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_provider_adapter  # noqa: E402
import reference_pool  # noqa: E402
import reference_relevance_ledger  # noqa: E402


class ReferencePoolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.paper_dir = self.root / "papers" / "inference" / "01-test"
        self.paper_dir.mkdir(parents=True)
        base = self.root / ".survey" / "work-queue" / "reference-curation"
        base.mkdir(parents=True)
        self.unrelated = base / "unrelated-papers.json"
        self.borderline = base / "borderline-papers.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_paper(self, name: str, canonical_id: str, title: str, references: list[dict]) -> None:
        meta = {
            "canonical_id": canonical_id,
            "title": title,
            "lineage": "Offload / Hierarchical Memory",
            "references": references,
        }
        (self.paper_dir / name).write_text(
            "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\nbody\n",
            encoding="utf-8",
        )

    def test_pool_aggregates_relation_count_and_excludes_saved_classes(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [
                {"canonical_id": "arXiv:2609.90001"},
                {"canonical_id": "arXiv:2609.90002"},
                {"canonical_id": "arXiv:2609.90003"},
                {"canonical_id": "arXiv:2609.00002"},
            ],
        )
        self._write_paper(
            "b.md",
            "arXiv:2609.00002",
            "B",
            [{"canonical_id": "arXiv:2609.90001"}],
        )
        reference_relevance_ledger.mark_unrelated(
            self.unrelated,
            canonical_id="arXiv:2609.90002",
        )
        reference_relevance_ledger.mark_borderline(
            self.borderline,
            canonical_id="arXiv:2609.90003",
        )

        pool = reference_pool.build_reference_pool(
            self.root,
            unrelated_ledger_path=self.unrelated,
            borderline_ledger_path=self.borderline,
        )
        self.assertEqual(pool["candidate_count"], 1)
        candidate = pool["candidates"][0]
        self.assertEqual(candidate["canonical_id"], "arXiv:2609.90001")
        self.assertEqual(candidate["relation_count"], 2)
        self.assertEqual(len(candidate["linked_from"]), 2)
        self.assertTrue(pool["borderline_excluded"])

    def test_arxiv_doi_alias_is_excluded_by_borderline_ledger(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [{"canonical_id": "arXiv:2505.09388"}],
        )
        reference_relevance_ledger.mark_borderline(
            self.borderline,
            canonical_id="DOI:10.48550/arxiv.2505.09388",
            reason="broad model report",
        )

        pool = reference_pool.build_reference_pool(
            self.root,
            borderline_ledger_path=self.borderline,
        )
        self.assertEqual(pool["candidate_count"], 0)

    def test_borderline_is_default_exclusion_but_can_be_reconsidered(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [
                {"canonical_id": "arXiv:2609.90001"},
                {"canonical_id": "arXiv:2609.90002"},
            ],
        )
        reference_relevance_ledger.mark_borderline(
            self.borderline,
            canonical_id="arXiv:2609.90001",
            reason="weak survey value",
        )

        default_pool = reference_pool.build_reference_pool(
            self.root,
            borderline_ledger_path=self.borderline,
        )
        self.assertEqual(
            [r["canonical_id"] for r in default_pool["candidates"]],
            ["arXiv:2609.90002"],
        )

        reconsidered = reference_pool.build_reference_pool(
            self.root,
            borderline_ledger_path=self.borderline,
            include_borderline=True,
        )
        self.assertEqual(
            [r["canonical_id"] for r in reconsidered["candidates"]],
            ["arXiv:2609.90001", "arXiv:2609.90002"],
        )
        self.assertFalse(reconsidered["borderline_excluded"])

    def test_ledger_is_idempotent_and_classification_moves_between_ledgers(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [
                {"canonical_id": "arXiv:2609.90001"},
                {"canonical_id": "arXiv:2609.90002"},
            ],
        )
        reference_relevance_ledger.mark_borderline(
            self.borderline,
            canonical_id="arXiv:2609.90001",
            title="Maybe",
            unrelated_path=self.unrelated,
        )
        reference_relevance_ledger.mark_borderline(
            self.borderline,
            canonical_id="arXiv:2609.90001",
            title="Maybe",
            unrelated_path=self.unrelated,
        )
        saved = json.loads(self.borderline.read_text(encoding="utf-8"))
        self.assertEqual(saved["record_count"], 1)

        reference_relevance_ledger.mark_unrelated(
            self.unrelated,
            canonical_id="arXiv:2609.90001",
            title="Noise",
            borderline_path=self.borderline,
        )
        unrelated = json.loads(self.unrelated.read_text(encoding="utf-8"))
        borderline = json.loads(self.borderline.read_text(encoding="utf-8"))
        self.assertEqual(unrelated["record_count"], 1)
        self.assertEqual(borderline["record_count"], 0)

        fetch = discovery_provider_adapter.repository_reference_pool_fetcher(
            reference_pool.SOURCE_URL,
            page_size=1,
            repo_root=self.root,
            unrelated_ledger_path=self.unrelated,
            borderline_ledger_path=self.borderline,
        )
        page = fetch(None)
        self.assertEqual([r["canonical_id"] for r in page["records"]], ["arXiv:2609.90002"])
        self.assertIsNone(page["next_cursor"])


if __name__ == "__main__":
    unittest.main()
