import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import assemble_research_record as assemble  # noqa: E402


class ValidationIssueCollectionTests(unittest.TestCase):
    def _record(self):
        jp = "日本語で十分な説明を行う。" * 80
        return {
            "metadata": {
                "title": "test",
                "canonical_id": "arXiv:0000.00000",
                "publication_date": "2026-01-01",
                "status": "preprint",
                "arxiv_primary_category": "cs.LG",
                "source_url": "https://arxiv.org/abs/0000.00000",
                "authors": ["A"],
                "arxiv_categories": ["cs.LG"],
            },
            "problem_method": {
                "problem_statement": jp,
                "novelty": jp,
                "method_overview": jp,
                "components": [
                    {"name": "c1", "description": jp},
                    {"name": "c2", "description": jp},
                ],
            },
            "evaluation": {"evaluation_summary": jp, "conditions": ["cond"]},
            "results": {
                "quantitative": [{"metric": "latency", "value": "10 ms"}],
                "result_summary": jp,
            },
            "positioning": {
                "limitations": ["l1", "l2", "l3"],
                "related_work": ["r1", "r2", "r3"],
                "implementation_notes": jp,
            },
        }

    def test_collects_all_current_issues_in_one_preflight(self):
        record = self._record()
        record["problem_method"]["method_overview"] = "short"
        record["problem_method"]["components"][0]["description"] = "short"
        record["problem_method"]["components"][1]["description"] = "short"

        issues = assemble.collect_validation_issues(record)

        self.assertIn("problem_method.method_overview must be at least 500 characters", issues)
        self.assertIn("problem_method.components[0].description must be at least 240 characters", issues)
        self.assertIn("problem_method.components[1].description must be at least 240 characters", issues)
        self.assertGreaterEqual(len(issues), 3)

    def test_validate_record_keeps_first_error_compatibility(self):
        record = self._record()
        record["problem_method"]["method_overview"] = "short"
        record["problem_method"]["components"][0]["description"] = "short"
        with self.assertRaisesRegex(
            ValueError,
            "problem_method.method_overview must be at least 500 characters",
        ):
            assemble.validate_record(record)


if __name__ == "__main__":
    unittest.main()
