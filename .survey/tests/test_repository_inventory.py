from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_repository_inventory.py"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class RepositoryInventoryTest(unittest.TestCase):
    def run_inventory(self, root: Path) -> dict:
        output = root / "inventory.json"
        subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(output.read_text(encoding="utf-8"))

    def test_symlink_hashes_link_text_like_git(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "target.txt").write_text("payload", encoding="utf-8")
            try:
                (root / "link.txt").symlink_to("target.txt")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unsupported: {exc}")

            inventory = self.run_inventory(root)
            rows = {row["path"]: row["sha"] for row in inventory["files"]}
            self.assertEqual(rows["link.txt"], git_blob_sha(b"target.txt"))

    def test_broken_symlink_is_still_in_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            try:
                (root / "broken-link").symlink_to("missing-target")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unsupported: {exc}")

            inventory = self.run_inventory(root)
            rows = {row["path"]: row["sha"] for row in inventory["files"]}
            self.assertIn("broken-link", rows)
            self.assertEqual(rows["broken-link"], git_blob_sha(b"missing-target"))


if __name__ == "__main__":
    unittest.main()
