import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "normalize_nullable_paper_metadata.py"


def _load_module(repo_root: Path):
    path = repo_root / ".survey/scripts/normalize_nullable_paper_metadata.py"
    spec = importlib.util.spec_from_file_location("normalize_nullable_paper_metadata", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NormalizeNullablePaperMetadataTests(unittest.TestCase):
    def _repo(self, td: str):
        repo = Path(td)
        target = repo / ".survey/scripts/normalize_nullable_paper_metadata.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
        return repo

    def test_missing_code_is_inserted_as_null_without_reformatting_body(self):
        with tempfile.TemporaryDirectory() as td:
            repo = self._repo(td)
            paper = repo / "papers/inference/x.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            original = """---\ntitle: Example\nimplementation: 公式コードURLは確認できない。\nlast_checked: '2026-09-14'\n---\n\n# Example\n\n本文はそのまま。\n"""
            paper.write_text(original, encoding="utf-8")
            module = _load_module(repo)

            changed = module.normalize_repo(repo)

            self.assertEqual(changed, ["papers/inference/x.md"])
            text = paper.read_text(encoding="utf-8")
            self.assertIn("implementation: 公式コードURLは確認できない。\ncode: null\nlast_checked:", text)
            self.assertTrue(text.endswith("# Example\n\n本文はそのまま。\n"))

    def test_existing_code_value_and_null_are_left_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            repo = self._repo(td)
            for name, value in (("url.md", "https://example.com/repo"), ("null.md", "null")):
                paper = repo / "papers" / name
                paper.parent.mkdir(parents=True, exist_ok=True)
                paper.write_text(
                    f"---\ntitle: Example\ncode: {value}\nlast_checked: '2026-09-14'\n---\n\nbody\n",
                    encoding="utf-8",
                )
            before = {p.name: p.read_text(encoding="utf-8") for p in (repo / "papers").glob("*.md")}
            module = _load_module(repo)

            self.assertEqual(module.normalize_repo(repo), [])
            after = {p.name: p.read_text(encoding="utf-8") for p in (repo / "papers").glob("*.md")}
            self.assertEqual(before, after)

    def test_normalization_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            repo = self._repo(td)
            paper = repo / "papers/x.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("---\ntitle: X\nlast_checked: null\n---\n\nbody\n", encoding="utf-8")
            module = _load_module(repo)

            self.assertEqual(module.normalize_repo(repo), ["papers/x.md"])
            first = paper.read_text(encoding="utf-8")
            self.assertEqual(module.normalize_repo(repo), [])
            self.assertEqual(first, paper.read_text(encoding="utf-8"))
            self.assertEqual(first.count("\ncode: null\n"), 1)


if __name__ == "__main__":
    unittest.main()
