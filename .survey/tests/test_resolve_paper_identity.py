from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import resolve_paper_identity  # noqa: E402


class ResolvePaperIdentityTests(unittest.TestCase):
    def test_existing_arxiv_identity_returns_existing_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/test/2026-2609.99991-existing.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                """---
canonical_id: "arXiv:2609.99991"
arxiv_id: "2609.99991"
title: "Existing Paper"
source: "https://arxiv.org/abs/2609.99991"
---

# Existing Paper
""",
                encoding="utf-8",
            )

            result = resolve_paper_identity.resolve(
                root,
                {"canonical_id": "arXiv:2609.99991"},
            )

            self.assertEqual(result["status"], "represented")
            self.assertEqual(
                result["paper_path"],
                "papers/inference/test/2026-2609.99991-existing.md",
            )

    def test_missing_identity_returns_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            result = resolve_paper_identity.resolve(
                root,
                {"arxiv_id": "2609.99992"},
            )
            self.assertEqual(result["status"], "not_found")
            self.assertIsNone(result["paper_path"])

    def test_stable_identity_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "stable paper identity required"):
                resolve_paper_identity.resolve(Path(td), {"title": "Only a title"})


if __name__ == "__main__":
    unittest.main()
