from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dispatch_fallback_inbox as dispatcher  # noqa: E402
import fallback_transport as ft  # noqa: E402


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


class FallbackDispatchBatchTests(unittest.TestCase):
    def test_dispatch_drains_multiple_eligible_record_envelopes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox = root / ft.FALLBACK_INBOX
            write_json(inbox / "env-a.json", {"id": "env-a", "kind": "research"})
            write_json(inbox / "env-b.json", {"id": "env-b", "kind": "research"})

            def materialize(_root: Path, raw: dict) -> dict:
                return {
                    "action": "ack_terminal",
                    "job_id": f"job-{raw['id']}",
                    "changed_paths": [],
                }

            with (
                mock.patch.object(dispatcher, "_is_record_fallback", return_value=True),
                mock.patch.object(dispatcher.record_replay, "materialize", side_effect=materialize),
            ):
                result = dispatcher.dispatch(root, max_items=50)

            self.assertEqual(result["processed_count"], 2)
            self.assertEqual([row["envelope_id"] for row in result["processed"]], ["env-a", "env-b"])
            self.assertEqual(list(inbox.glob("*.json")), [])
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").is_file())
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-b.json").is_file())

    def test_deferred_envelope_does_not_block_later_dispatchable_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox = root / ft.FALLBACK_INBOX
            write_json(inbox / "env-a.json", {"id": "env-a", "kind": "research"})
            write_json(inbox / "env-b.json", {"id": "env-b", "kind": "research"})

            def materialize(_root: Path, raw: dict) -> dict:
                if raw["id"] == "env-a":
                    return {"action": "deferred", "reason": "canonical job not available"}
                return {"action": "ack_terminal", "job_id": "job-b", "changed_paths": []}

            with (
                mock.patch.object(dispatcher, "_is_record_fallback", return_value=True),
                mock.patch.object(dispatcher.record_replay, "materialize", side_effect=materialize),
            ):
                result = dispatcher.dispatch(root, max_items=50)

            self.assertEqual(result["processed_count"], 1)
            self.assertEqual(result["processed"][0]["envelope_id"], "env-b")
            self.assertTrue((inbox / "env-a.json").is_file())
            self.assertFalse((inbox / "env-b.json").exists())
            self.assertEqual(result["deferred"][0]["id"], "env-a")


if __name__ == "__main__":
    unittest.main()
