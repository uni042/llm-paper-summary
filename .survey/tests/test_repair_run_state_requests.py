from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import repair_run_state_requests  # noqa: E402


class RepairRunStateRequestsTests(unittest.TestCase):
    def test_yaml_object_with_json_suffix_is_rewritten_as_json(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/work-queue/run-state/requests/example.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                """schema_version: 1
request_id: example
run_key: run-example
worker_id: scheduled-chat-30
scheduled_slot: "30"
actual_invocation_start: "2026-09-26T05:28:21+09:00"
runtime_condition: none
""",
                encoding="utf-8",
            )

            result = repair_run_state_requests.repair(root, apply=True)

            self.assertEqual(result["repaired"], [
                ".survey/work-queue/run-state/requests/example.json"
            ])
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value["request_id"], "example")
            self.assertEqual(value["scheduled_slot"], "30")

    def test_valid_json_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/work-queue/run-state/requests/example.json"
            path.parent.mkdir(parents=True)
            raw = '{"schema_version":1,"request_id":"example"}\n'
            path.write_text(raw, encoding="utf-8")

            result = repair_run_state_requests.repair(root, apply=True)

            self.assertEqual(result["repaired"], [])
            self.assertEqual(path.read_text(encoding="utf-8"), raw)


if __name__ == "__main__":
    unittest.main()
