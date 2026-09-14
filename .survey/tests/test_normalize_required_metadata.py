import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "normalize_required_metadata.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("normalize_required_metadata", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class NormalizeRequiredMetadataTests(unittest.TestCase):
    def test_adds_explicit_null_code_before_implementation_without_reformatting(self):
        module = _load_module()
        original = (
            "---\n"
            "canonical_id: arXiv:2601.00001\n"
            "title: Example\n"
            "source: https://arxiv.org/abs/2601.00001\n"
            "implementation: 公式コードURLは確認できない。\n"
            "last_checked: '2026-09-14'\n"
            "---\n"
            "# Example\n"
        )
        normalized, fields = module.normalize_text(original)
        self.assertEqual(fields, ["code"])
        self.assertIn(
            "source: https://arxiv.org/abs/2601.00001\n"
            "code: null\n"
            "implementation: 公式コードURLは確認できない。",
            normalized,
        )
        self.assertTrue(normalized.endswith("---\n# Example\n"))

    def test_existing_null_code_is_idempotent(self):
        module = _load_module()
        original = (
            "---\ncanonical_id: arXiv:2601.00001\ncode: null\n"
            "implementation: none\n---\n# Example\n"
        )
        normalized, fields = module.normalize_text(original)
        self.assertEqual(normalized, original)
        self.assertEqual(fields, [])

    def test_apply_repairs_only_paper_files(self):
        module = _load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers" / "inference" / "x.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                "---\ncanonical_id: x\nimplementation: none\n---\n# X\n",
                encoding="utf-8",
            )
            readme = paper.parent / "README.md"
            readme.write_text("---\ncanonical_id: readme\n---\n", encoding="utf-8")
            changed = module.normalize_repo(root, apply=True)
            self.assertEqual(len(changed), 1)
            self.assertIn("code: null", paper.read_text(encoding="utf-8"))
            self.assertNotIn("code: null", readme.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
