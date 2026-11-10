import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_immutable_submission as processor  # noqa: E402
import queue_worker  # noqa: E402


class ImmutableReplayReconciliationTests(unittest.TestCase):
    def test_precheck_accepts_expected_blob_mismatch_when_current_file_is_exact_render(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            paper = repo / "papers/inference/test/exact.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            rendered = ("exact rendered record\n" * 40).rstrip() + "\n"
            paper.write_text(rendered, encoding="utf-8")
            descriptor = {
                "paper_path": "papers/inference/test/exact.md",
                "expected_blob_sha": "0" * 40,
            }

            processor._precheck_paper(repo, descriptor, rendered_content=rendered)

    def test_precheck_rejects_expected_blob_mismatch_when_current_file_differs(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            paper = repo / "papers/inference/test/conflict.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("different current content\n", encoding="utf-8")
            descriptor = {
                "paper_path": "papers/inference/test/conflict.md",
                "expected_blob_sha": "0" * 40,
            }

            with self.assertRaisesRegex(ValueError, "paper blob changed"):
                processor._precheck_paper(
                    repo,
                    descriptor,
                    rendered_content=("desired rendered record\n" * 40),
                )

    def test_precheck_still_requires_expected_blob_for_existing_paper(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            paper = repo / "papers/inference/test/no-expected.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            rendered = ("exact rendered record\n" * 40).rstrip() + "\n"
            paper.write_text(rendered, encoding="utf-8")
            descriptor = {"paper_path": "papers/inference/test/no-expected.md"}

            with self.assertRaisesRegex(ValueError, "expected_blob_sha is required"):
                processor._precheck_paper(repo, descriptor, rendered_content=rendered)

    def test_apply_artifact_accepts_exact_already_applied_content(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            survey_root = repo / ".survey"
            survey_root.mkdir(parents=True, exist_ok=True)
            queue_worker.ROOT = survey_root
            paper_rel = "papers/inference/test/exact.md"
            paper = repo / paper_rel
            paper.parent.mkdir(parents=True, exist_ok=True)
            content = ("already applied immutable content\n" * 30).rstrip() + "\n"
            paper.write_text(content, encoding="utf-8")
            sub = {
                "status": "completed",
                "paper_path": paper_rel,
                "content": content,
                "expected_blob_sha": "1" * 40,
            }
            job = {"type": "research", "paper_path": paper_rel}
            calls = [
                SimpleNamespace(returncode=0, stdout="2" * 40 + "\n", stderr=""),
                SimpleNamespace(returncode=0, stdout="delta.json\n", stderr=""),
            ]

            with patch("subprocess.run", side_effect=calls):
                artifact = queue_worker.apply_artifact(sub, job)

            self.assertEqual(artifact["paper"], paper_rel)
            self.assertEqual(paper.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
