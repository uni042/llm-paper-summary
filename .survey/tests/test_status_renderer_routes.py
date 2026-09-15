import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
LEGACY_RENDER_INVOCATION = re.compile(
    r"python(?:3)?\s+\.survey/scripts/build_status_dashboard\.py(?:\s|$)"
)


class StatusRendererRouteTests(unittest.TestCase):
    def test_workflows_do_not_execute_legacy_status_renderer(self):
        offenders = []
        for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if LEGACY_RENDER_INVOCATION.search(text):
                offenders.append(str(path.relative_to(ROOT)))

        self.assertEqual(
            [],
            offenders,
            "STATUS.md must only be rendered through render_status_dashboard.py; "
            f"legacy renderer invocations found in: {offenders}",
        )

    def test_legacy_cli_delegates_to_canonical_counts_first_layout(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            output = repo / "STATUS.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / ".survey/scripts/build_status_dashboard.py"),
                    "--repo-root",
                    str(repo),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("## 件数サマリー", text)
            self.assertIn("## 詳細証拠", text)
            self.assertNotIn("## 1. ここ数時間で論文読解・サーベイが成功しているか", text)


if __name__ == "__main__":
    unittest.main()
