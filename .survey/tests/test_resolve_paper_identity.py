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


    def test_generic_source_url_is_a_stable_identity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/test/2026-existing-project-paper.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                """---
canonical_id: "OpenReview:project-paper"
openreview_id: "project-paper"
title: "Project Paper"
source: "https://example.org/papers/project-paper"
---

# Project Paper
""",
                encoding="utf-8",
            )

            result = resolve_paper_identity.resolve(
                root,
                {"source_url": "https://example.org/papers/project-paper?tracking=ignored"},
            )

            self.assertEqual(result["status"], "represented")
            self.assertEqual(
                result["paper_path"],
                "papers/inference/test/2026-existing-project-paper.md",
            )
            self.assertIn(
                "url:https://example.org/papers/project-paper",
                result["query_identity_tokens"],
            )

    def test_unrelated_duplicate_identifier_does_not_block_unique_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / "papers/inference/test"
            folder.mkdir(parents=True)
            for name in ("duplicate-a.md", "duplicate-b.md"):
                (folder / name).write_text(
                    """---
canonical_id: "arXiv:2609.77777"
arxiv_id: "2609.77777"
title: "Duplicate Paper"
source: "https://arxiv.org/abs/2609.77777"
---

# Duplicate Paper
""",
                    encoding="utf-8",
                )
            (folder / "unique.md").write_text(
                """---
canonical_id: "arXiv:2609.88888"
arxiv_id: "2609.88888"
title: "Unique Paper"
source: "https://arxiv.org/abs/2609.88888"
---

# Unique Paper
""",
                encoding="utf-8",
            )

            result = resolve_paper_identity.resolve(
                root,
                {"canonical_id": "arXiv:2609.88888"},
            )

            self.assertEqual(result["status"], "represented")
            self.assertEqual(
                result["paper_path"],
                "papers/inference/test/unique.md",
            )

    def test_queried_duplicate_identifier_remains_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            folder = root / "papers/inference/test"
            folder.mkdir(parents=True)
            for name in ("duplicate-a.md", "duplicate-b.md"):
                (folder / name).write_text(
                    """---
canonical_id: "arXiv:2609.77777"
arxiv_id: "2609.77777"
title: "Duplicate Paper"
source: "https://arxiv.org/abs/2609.77777"
---

# Duplicate Paper
""",
                    encoding="utf-8",
                )

            with self.assertRaisesRegex(
                ValueError,
                "identity resolves to multiple represented paper paths",
            ):
                resolve_paper_identity.resolve(
                    root,
                    {"canonical_id": "arXiv:2609.77777"},
                )


if __name__ == "__main__":
    unittest.main()
