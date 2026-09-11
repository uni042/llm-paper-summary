from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from assemble_research_record import validate_record  # noqa: E402
from render_paper import render_paper  # noqa: E402


def complete_record() -> dict:
    return {
        "metadata": {
            "canonical_id": "arXiv:2607.16473",
            "arxiv_id": "2607.16473",
            "doi": "10.48550/arXiv.2607.16473",
            "arxiv_categories": {"primary": "cs.AR", "cross_list": []},
            "title": "Example",
            "summary": "要約。" * 100,
            "source": "https://arxiv.org/abs/2607.16473",
            "sources": ["https://arxiv.org/abs/2607.16473"],
            "authors": ["A. Author"],
            "publication": "arXiv:2607.16473v1",
            "publication_type": "プレプリント",
            "published": "2026-07-17",
            "publication_status": "MICRO 2026採択",
            "topics": ["NPU"],
            "implementation": "公開実装あり。",
            "hardware_evaluation": "シミュレーション。",
            "hardware_details": "TPUv4相当。",
            "quality_effect": "品質は変更しない。",
            "storage_targets": ["モデル重み"],
            "bottlenecks": ["消費電力"],
            "evidence_locations": ["§5"],
            "references": [
                {
                    "canonical_id": "arXiv:2303.06865",
                    "arxiv_id": "2303.06865",
                    "doi": "10.48550/arXiv.2303.06865",
                }
            ],
            "references_checked_at": "2026-09-11",
            "references_source": "primary-reference-section",
            "references_total": 42,
            "code": "https://example.com/code",
            "last_checked": "2026-09-11",
        },
        "problem_method": {
            "problem": "問題。" * 100,
            "novelty": "新規性。" * 60,
            "method_overview": "全体像。" * 130,
            "components": [
                {"name": "機構1", "description": "説明。" * 90},
                {"name": "機構2", "description": "説明。" * 90},
            ],
            "system_design": "流れ。" * 100,
        },
        "evaluation": {"hardware": "機器", "scope": "評価範囲"},
        "results": {
            "overview": "結果。" * 70,
            "key_results": [{
                "metric": "エネルギー",
                "value": "25%削減",
                "baseline": "比較対象",
                "condition": "条件",
                "interpretation": "意味",
            }],
            "negative_results": ["限界"],
            "interpretation": "解釈",
            "quality_impact": "品質への影響はない。",
        },
        "positioning": {
            "limitations": ["限界"],
            "differences": ["差"],
            "implementation_status": "状態",
            "research_positioning": "位置づけ",
        },
    }


class RenderPaperMetadataTest(unittest.TestCase):
    def test_frontmatter_keeps_index_audit_and_reference_metadata(self) -> None:
        rendered = render_paper(complete_record())
        meta = yaml.safe_load(rendered.split("---", 2)[1])
        self.assertEqual(meta["arxiv_categories"], {"primary": "cs.AR", "cross_list": []})
        self.assertEqual(meta["published"], "2026-07-17")
        self.assertEqual(meta["publication_status"], "MICRO 2026採択")
        self.assertEqual(meta["code"], "https://example.com/code")
        self.assertEqual(meta["storage_targets"], ["モデル重み"])
        self.assertEqual(meta["references"][0]["canonical_id"], "arXiv:2303.06865")
        self.assertEqual(meta["references_checked_at"], "2026-09-11")
        self.assertEqual(meta["references_total"], 42)

    def test_references_are_required(self) -> None:
        record = complete_record()
        del record["metadata"]["references"]
        with self.assertRaisesRegex(ValueError, "metadata.references"):
            validate_record(record)

    def test_reference_items_require_a_normalized_identity(self) -> None:
        record = complete_record()
        record["metadata"]["references"] = [{"title": "Missing identifiers"}]
        with self.assertRaisesRegex(ValueError, "normalized identity"):
            validate_record(record)

    def test_arxiv_category_is_required(self) -> None:
        record = complete_record()
        del record["metadata"]["arxiv_categories"]
        with self.assertRaisesRegex(ValueError, "arxiv_categories.primary"):
            validate_record(record)


if __name__ == "__main__":
    unittest.main()
