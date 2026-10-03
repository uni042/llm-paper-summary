import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import assemble_research_record as assemble  # noqa: E402


class ValidationIssueCollectionTests(unittest.TestCase):
    def _record(self):
        jp = "日本語で十分な説明を行い、機構と条件と意味を具体的に記述する。" * 50
        return {
            "metadata": {
                "canonical_id": "arXiv:0000.00000",
                "title": "test",
                "summary": jp,
                "source": "https://arxiv.org/abs/0000.00000",
                "sources": ["https://arxiv.org/abs/0000.00000"],
                "authors": ["A"],
                "publication": "arXiv",
                "publication_type": "preprint",
                "published": "2026-01-01",
                "publication_status": "preprint",
                "topics": ["inference"],
                "implementation": "not confirmed",
                "code": None,
                "last_checked": "2026-09-13",
                "hardware_evaluation": "実機評価あり",
                "quality_effect": "品質影響を評価",
                "references": [],
                "references_checked_at": "2026-09-13",
                "references_source": "paper",
                "references_total": 0,
            },
            "problem_method": {
                "problem": jp,
                "novelty": jp,
                "method_overview": jp,
                "components": [
                    {"name": "c1", "description": jp},
                    {"name": "c2", "description": jp},
                ],
                "system_design": jp,
            },
            "evaluation": {"hardware": "GPU", "scope": jp},
            "results": {
                "key_results": [{
                    "metric": "遅延",
                    "value": "10 ms",
                    "baseline": "baseline",
                    "condition": "condition",
                    "interpretation": "改善を確認",
                }],
                "overview": jp,
                "negative_results": "境界条件では改善が縮小する。",
                "interpretation": "条件依存性を確認する。",
                "quality_impact": "品質影響を別途確認する。",
            },
            "positioning": {
                "limitations": ["l1", "l2", "l3"],
                "differences": jp,
                "implementation_status": "公開実装は未確認",
                "research_positioning": jp,
            },
        }

    def test_semantic_depth_is_not_a_github_publication_gate(self):
        record = self._record()
        record["problem_method"]["method_overview"] = "short"
        record["problem_method"]["components"][0]["description"] = "short"
        record["problem_method"]["components"][1]["description"] = "short"

        issues = assemble.collect_validation_issues(record)
        self.assertEqual(issues, [])

    def test_validate_record_rejects_publication_integrity_failure(self):
        record = self._record()
        record["metadata"]["canonical_id"] = ""
        with self.assertRaisesRegex(
            ValueError,
            "metadata.canonical_id is required for rendering/publication",
        ):
            assemble.validate_record(record)


if __name__ == "__main__":
    unittest.main()
