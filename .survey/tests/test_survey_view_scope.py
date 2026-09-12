from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import survey  # noqa: E402


class ComparisonScopeTest(unittest.TestCase):
    def test_render_passes_only_inference_records_to_comparison(self) -> None:
        records = [
            {"path": "papers/inference/01-lineage/inference.md"},
            {"path": "papers/training/01-lineage/training.md"},
            {"path": "papers/survey/01-lineage/survey.md"},
        ]
        received: list[dict] = []

        with (
            mock.patch.object(survey, "papers", return_value=records),
            mock.patch.object(survey, "identity", return_value={}),
            mock.patch.object(survey, "write"),
            mock.patch.object(survey, "paper_views", return_value=[]),
            mock.patch.object(survey, "render_indexes", return_value={}),
            mock.patch.object(survey, "_update_catalog_counts"),
            mock.patch.object(survey, "render_comparison", side_effect=lambda rows: received.extend(rows)),
        ):
            survey.render()

        self.assertEqual(
            [record["path"] for record in received],
            ["papers/inference/01-lineage/inference.md"],
        )


if __name__ == "__main__":
    unittest.main()
