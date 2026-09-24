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

    def test_legacy_workflow_chain_is_upgraded_to_canonical_layout(self):
        """A stale workflow YAML may still call old builder + compatibility shim."""
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            output = repo / "STATUS.md"
            commands = [
                [
                    sys.executable,
                    str(ROOT / ".survey/scripts/build_status_dashboard.py"),
                    "--repo-root",
                    str(repo),
                    "--output",
                    str(output),
                ],
                [
                    sys.executable,
                    str(ROOT / ".survey/scripts/append_research_throughput_status.py"),
                    "--repo-root",
                    str(repo),
                    "--status",
                    str(output),
                ],
            ]
            for command in commands:
                proc = subprocess.run(command, text=True, capture_output=True, check=False)
                self.assertEqual(proc.returncode, 0, proc.stderr)

            text = output.read_text(encoding="utf-8")
            self.assertIn("## 件数サマリー", text)
            self.assertIn("## 詳細証拠", text)
            self.assertNotIn("## 1. ここ数時間で論文読解・サーベイが成功しているか", text)


if __name__ == "__main__":
    unittest.main()
