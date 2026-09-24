from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lineage_proposal  # noqa: E402
import paper_taxonomy  # noqa: E402


class LineageProposalTests(unittest.TestCase):
    def _repo(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
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
            json.dumps(
                {
                    "schema_version": 3,
                    "active_count": 4,
                    "papers": papers,
                    "identifier_to_canonical": {key: key for key in papers},
                    "ignored_moved_stubs": [],
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return tmp, root

    def _proposal(self):
        return {
            "slug_tail": "distinct-runtime-cluster",
            "title": "Distinct Runtime Cluster",
            "description": "既存近傍系統とは最適化対象と主要機構が異なる実行時システム研究をまとめる独立系統。",
            "distinctness_reason": "近傍系統がメモリ退避そのものを主目的とするのに対し、このクラスタは別の実行時制御機構を主要貢献とし、同じ分類では差分が失われる。",
            "boundary_rule": "主要貢献がこの実行時制御機構そのものの場合だけ含め、補助利用だけなら近傍系統へ残す。",
            "scope_includes": ["実行時制御機構を主要貢献とする研究"],
            "scope_excludes": ["単なるオフロード実装"],
            "neighbor_lineages": ["01-offload-hierarchical-memory"],
            "confidence": "high",
            "supporting_papers": [
                {"canonical_id": f"arXiv:2601.0000{i}", "reason": "同一の主要機構"}
                for i in range(1, 5)
            ],
        }

    def test_clear_multi_paper_cluster_is_promoted(self):
        tmp, root = self._repo()
        self.addCleanup(tmp.cleanup)
        result = lineage_proposal.consider_lineage_proposal(
            root, self._proposal(), round_candidates=[], source_submission="test.json"
        )
        self.assertEqual(result["status"], "promoted")
        self.assertIn(result["lineage"], paper_taxonomy.canonical_inference_lineages(root))
        self.assertTrue((root / "papers/inference" / result["lineage"] / "README.md").is_file())

    def test_weak_cluster_is_deferred(self):
        tmp, root = self._repo()
        self.addCleanup(tmp.cleanup)
        proposal = self._proposal()
        proposal["supporting_papers"] = proposal["supporting_papers"][:1]
        result = lineage_proposal.consider_lineage_proposal(
            root, proposal, round_candidates=[], source_submission="test.json"
        )
        self.assertEqual(result["status"], "deferred")
        self.assertIsNone(result["lineage"])


if __name__ == "__main__":
    unittest.main()
