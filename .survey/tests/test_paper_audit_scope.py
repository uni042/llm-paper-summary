from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from paper_audit_scope import added_paper_paths  # noqa: E402


class AddedPaperScopeTests(unittest.TestCase):
    def test_only_papers_added_after_baseline_are_selected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Scope test"], cwd=repo, check=True)

            old = repo / "papers" / "inference" / "old.md"
            old.parent.mkdir(parents=True)
            old.write_text("old version\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            baseline = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            old.write_text("metadata-only edit; do not audit this old paper\n", encoding="utf-8")
            new = repo / "papers" / "survey" / "new.md"
            new.parent.mkdir(parents=True)
            new.write_text("new paper\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "add new paper"], cwd=repo, check=True)

            selected = added_paper_paths(repo, baseline)

        self.assertEqual(selected, {"papers/survey/new.md"})


if __name__ == "__main__":
    unittest.main()
