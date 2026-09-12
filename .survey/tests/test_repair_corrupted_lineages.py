from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from repair_corrupted_lineages import expected_lineage_repair, repair_text  # noqa: E402


class RepairCorruptedLineagesTest(unittest.TestCase):
    def test_detects_normalizer_corruption_from_parent_lineage_slug(self) -> None:
        path = Path("papers/inference/01-offload-hierarchical-memory/paper.md")
        self.assertEqual(
            expected_lineage_repair(path, "オフロード-hierarchical-メモリ"),
            "offload-hierarchical-memory",
        )

    def test_detects_scheduling_corruption(self) -> None:
        path = Path("papers/inference/11-llm-serving-scheduling-disaggregation/paper.md")
        self.assertEqual(
            expected_lineage_repair(path, "llm-serving-スケジューラ-disaggregation"),
            "llm-serving-scheduling-disaggregation",
        )

    def test_does_not_rewrite_legacy_human_readable_lineage(self) -> None:
        path = Path("papers/inference/11-llm-serving-scheduling-disaggregation/paper.md")
        self.assertIsNone(
            expected_lineage_repair(path, "LLM Serving / Scheduling / Disaggregation")
        )

    def test_repair_text_changes_only_corrupted_frontmatter_lineage(self) -> None:
        path = Path("papers/inference/01-offload-hierarchical-memory/paper.md")
        source = "---\ntitle: Example\nlineage: オフロード-hierarchical-メモリ\n---\n\n# Example\n"
        repaired, changed = repair_text(path, source)
        self.assertTrue(changed)
        self.assertIn("lineage: offload-hierarchical-memory", repaired)
        self.assertIn("# Example", repaired)


if __name__ == "__main__":
    unittest.main()
