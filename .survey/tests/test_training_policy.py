from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_repository  # noqa: E402


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class TrainingPolicyTest(unittest.TestCase):
    def run_check(self, root: Path, baseline_files: dict[str, str]) -> dict:
        frozen = root / ".survey/survey-state/frozen-training.json"
        frozen.parent.mkdir(parents=True, exist_ok=True)
        frozen.write_text(
            json.dumps({
                "schema_version": 2,
                "policy": "No new training paper entries; existing files may be edited.",
                "files": baseline_files,
            }),
            encoding="utf-8",
        )
        inventory_files = []
        for path in sorted(root.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                inventory_files.append({"path": path.relative_to(root).as_posix(), "sha": blob_sha(data)})
        inventory = {"source_commit": "test", "files": inventory_files}
        with patch.object(check_repository, "REQUIRED_V10_PATHS", ()):
            return check_repository.check(root, inventory)

    def test_existing_training_paper_may_change(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/training/lineage/paper.md"
            paper.parent.mkdir(parents=True)
            original = b"original\n"
            paper.write_bytes(b"edited content\n")
            result = self.run_check(
                root,
                {paper.relative_to(root).as_posix(): blob_sha(original)},
            )
            codes = [finding["code"] for finding in result["findings"]]
            self.assertNotIn("frozen_training_changed", codes)
            self.assertNotIn("frozen_training_added", codes)

    def test_new_training_paper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old_paper = root / "papers/training/lineage/old.md"
            old_paper.parent.mkdir(parents=True)
            old_paper.write_text("old\n", encoding="utf-8")
            new_paper = root / "papers/training/lineage/new.md"
            new_paper.write_text("new\n", encoding="utf-8")
            result = self.run_check(
                root,
                {old_paper.relative_to(root).as_posix(): blob_sha(b"old\n")},
            )
            added = [finding for finding in result["findings"] if finding["code"] == "frozen_training_added"]
            self.assertEqual([finding["path"] for finding in added], [new_paper.relative_to(root).as_posix()])


if __name__ == "__main__":
    unittest.main()
