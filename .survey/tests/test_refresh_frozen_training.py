from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "refresh_frozen_training.py"


class FrozenTrainingRefreshTest(unittest.TestCase):
    def test_refresh_keeps_membership_only_freeze_policy(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/training/01-lineage/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text("# example\n", encoding="utf-8")
            (root / ".survey/survey-state").mkdir(parents=True)

            subprocess.run(
                [sys.executable, str(SCRIPT), "--repo-root", str(root), "--source", "test-source"],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(
                (root / ".survey/survey-state/frozen-training.json").read_text(encoding="utf-8")
            )
            self.assertEqual(payload["schema_version"], 2)
            self.assertIn("No new training paper entries", payload["policy"])
            self.assertIn("may be edited", payload["policy"])
            self.assertIn("historical baseline references only", payload["policy"])
            self.assertIn("papers/training/01-lineage/example.md", payload["files"])


if __name__ == "__main__":
    unittest.main()
