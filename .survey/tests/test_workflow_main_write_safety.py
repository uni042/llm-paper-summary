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

    def test_discovery_recovery_recomputes_bank_selection_after_push_race(self):
        text = (WORKFLOWS / "survey-discovery-recovery.yml").read_text(encoding="utf-8")

        # Discovery recovery may reserve the next PRECHECKED bank. A push race must
        # therefore discard the stale local selection and recompute from latest main
        # so a bank taken by another worker cannot be published as a double claim.
        self.assertIn("for attempt in $(seq 1 12)", text)
        self.assertIn("git reset --hard origin/main", text)
        self.assertIn("auto_advance_discovery.py", text)
        self.assertIn("recomputing from latest main", text)
        self.assertNotIn("git rebase origin/main", text)


if __name__ == "__main__":
    unittest.main()
