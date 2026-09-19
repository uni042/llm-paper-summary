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
        self.ledger = self.root / ".survey" / "work-queue" / "reference-curation" / "unrelated-papers.json"
        self.ledger.parent.mkdir(parents=True)

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

    def test_pool_aggregates_relation_count_and_excludes_represented_and_unrelated(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [
                {"canonical_id": "arXiv:2609.90001"},
                {"canonical_id": "arXiv:2609.90002"},
                {"canonical_id": "arXiv:2609.00002"},
            ],
        )
        self._write_paper(
            "b.md",
            "arXiv:2609.00002",
            "B",
            [{"canonical_id": "arXiv:2609.90001"}],
        )
        self.ledger.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "records": {
                        "arXiv:2609.90002": {
                            "canonical_id": "arXiv:2609.90002",
                            "identity_tokens": ["arXiv:2609.90002"],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

        pool = reference_pool.build_reference_pool(
            self.root,
            unrelated_ledger_path=self.ledger,
        )
        self.assertEqual(pool["candidate_count"], 1)
        candidate = pool["candidates"][0]
        self.assertEqual(candidate["canonical_id"], "arXiv:2609.90001")
        self.assertEqual(candidate["relation_count"], 2)
        self.assertEqual(len(candidate["linked_from"]), 2)

    def test_unrelated_ledger_is_idempotent_and_provider_skips_saved_candidate(self) -> None:
        self._write_paper(
            "a.md",
            "arXiv:2609.00001",
            "A",
            [
                {"canonical_id": "arXiv:2609.90001"},
                {"canonical_id": "arXiv:2609.90002"},
            ],
        )
        reference_relevance_ledger.mark_unrelated(
            self.ledger,
            canonical_id="arXiv:2609.90001",
            title="Noise",
            reason="outside scope",
        )
        reference_relevance_ledger.mark_unrelated(
            self.ledger,
            canonical_id="arXiv:2609.90001",
            title="Noise",
            reason="outside scope",
        )
        saved = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(saved["record_count"], 1)

        fetch = discovery_provider_adapter.repository_reference_pool_fetcher(
            reference_pool.SOURCE_URL,
            page_size=1,
            repo_root=self.root,
            unrelated_ledger_path=self.ledger,
        )
        page = fetch(None)
        self.assertEqual([r["canonical_id"] for r in page["records"]], ["arXiv:2609.90002"])
        self.assertIsNone(page["next_cursor"])


if __name__ == "__main__":
    unittest.main()
