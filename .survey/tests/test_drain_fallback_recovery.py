from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import drain_fallback_recovery as recovery  # noqa: E402


class DrainFallbackRecoveryTests(unittest.TestCase):
    def test_materialized_record_is_pinned_and_settled_before_next_replay(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            events: list[str] = []
            records = [
                {
                    "action": "materialized",
                    "envelope_id": "env-a",
                    "descriptor": ".survey/work-queue/submissions/research/attempt-a.json",
                    "archived": ".survey/work-queue/fallback-archive/env-a.json",
                    "source": ".survey/work-queue/fallback-inbox/env-a.json",
                    "changed_paths": [
                        ".survey/work-queue/records/chat-record-c/metadata.json",
                        ".survey/work-queue/submissions/research/attempt-a.json",
                    ],
                },
                {
                    "action": "materialized",
                    "envelope_id": "env-b",
                    "descriptor": ".survey/work-queue/submissions/research/attempt-b.json",
                    "archived": ".survey/work-queue/fallback-archive/env-b.json",
                    "source": ".survey/work-queue/fallback-inbox/env-b.json",
                    "changed_paths": [
                        ".survey/work-queue/records/chat-record-c/metadata.json",
                        ".survey/work-queue/submissions/research/attempt-b.json",
                    ],
                },
                {"action": "idle", "deferred": []},
            ]

            def dispatch_one(_root: Path) -> dict:
                value = records.pop(0)
                events.append(f"dispatch:{value.get('envelope_id', 'idle')}")
                return value

            def pin(_root: Path, row: dict) -> None:
                events.append(f"pin:{row['envelope_id']}")

            def settle(_root: Path, descriptor: str, *, parallelism: int) -> dict:
                events.append(f"settle:{Path(descriptor).stem}")
                return {"failures": 0}

            with (
                mock.patch.object(recovery, "dispatch_one_record", side_effect=dispatch_one),
                mock.patch.object(recovery, "pin_materialized_record", side_effect=pin),
                mock.patch.object(recovery, "settle_descriptor", side_effect=settle),
            ):
                result = recovery.drain(root, max_records=10, parallelism=4)

            self.assertEqual(
                events,
                [
                    "dispatch:env-a",
                    "pin:env-a",
                    "settle:attempt-a",
                    "dispatch:env-b",
                    "pin:env-b",
                    "settle:attempt-b",
                    "dispatch:idle",
                ],
            )
            self.assertEqual(result["materialized"], 2)
            self.assertEqual(result["settled"], 2)
            self.assertEqual(result["failures"], 0)

    def test_terminal_ack_does_not_require_a_pin_commit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            records = [
                {"action": "ack_terminal", "envelope_id": "env-old"},
                {"action": "idle", "deferred": []},
            ]
            with (
                mock.patch.object(recovery, "dispatch_one_record", side_effect=lambda _root: records.pop(0)),
                mock.patch.object(recovery, "pin_materialized_record") as pin,
                mock.patch.object(recovery, "settle_descriptor") as settle,
            ):
                result = recovery.drain(root, max_records=10)

            pin.assert_not_called()
            settle.assert_not_called()
            self.assertEqual(result["ack_terminal"], 1)


if __name__ == "__main__":
    unittest.main()
