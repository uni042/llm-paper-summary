import argparse
import hashlib
import importlib
import sys
import tempfile
import unittest
from pathlib import Path


class RepoEditTests(unittest.TestCase):
    def setUp(self):
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        sys.path.insert(0, str(scripts))
        self.mod = importlib.import_module("repo_edit")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / "a.txt"
        self.path.write_text("one\ntwo\nthree\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def ns(self, command, **kwargs):
        base = dict(command=command, text=None, text_file=None)
        base.update(kwargs)
        return argparse.Namespace(**base)

    def test_replace_insert_delete_append(self):
        before = self.path.read_text()
        after = self.mod.edit_text(before, self.ns("replace", start_line=2, end_line=2, text="TWO"))
        self.assertEqual(after, "one\nTWO\nthree\n")
        after = self.mod.edit_text(after, self.ns("insert", line=2, position="before", text="middle"))
        self.assertEqual(after, "one\nmiddle\nTWO\nthree\n")
        after = self.mod.edit_text(after, self.ns("delete", start_line=3, end_line=3))
        self.assertEqual(after, "one\nmiddle\nthree\n")
        after = self.mod.edit_text(after, self.ns("append", text="four"))
        self.assertEqual(after, "one\nmiddle\nthree\nfour\n")

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            self.mod.resolve_target(self.root, "../outside.txt")

    def test_sha_precondition(self):
        raw = self.path.read_bytes()
        good = hashlib.sha256(raw).hexdigest()
        self.assertEqual(self.mod.check_precondition(raw, good), good)
        with self.assertRaises(ValueError):
            self.mod.check_precondition(raw, "0" * 64)


if __name__ == "__main__":
    unittest.main()
