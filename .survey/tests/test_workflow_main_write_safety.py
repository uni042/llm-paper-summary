import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class MainWriterWorkflowSafetyTests(unittest.TestCase):
    def test_push_triggered_workflows_that_write_main_are_main_only(self):
        offenders = []
        for path in sorted(WORKFLOWS.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if "git push origin HEAD:main" not in text:
                continue
            data = yaml.load(text, Loader=yaml.BaseLoader) or {}
            trigger = data.get("on") or {}
            push = trigger.get("push") if isinstance(trigger, dict) else None
            if push is None:
                continue
            branches = push.get("branches") if isinstance(push, dict) else None
            if branches != ["main"]:
                offenders.append(path.name)

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
