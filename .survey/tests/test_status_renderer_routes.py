import re
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


if __name__ == "__main__":
    unittest.main()
