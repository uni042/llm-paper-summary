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
    def test_batch_mode_drains_multiple_eligible_record_envelopes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox = root / ft.FALLBACK_INBOX
            write_json(inbox / "env-a.json", {"id": "env-a", "kind": "research"})
            write_json(inbox / "env-b.json", {"id": "env-b", "kind": "research"})

            def materialize(_root: Path, raw: dict) -> dict:
                return {"action": "ack_terminal", "job_id": f"job-{raw['id']}", "changed_paths": []}

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

    def test_record_wave_never_reuses_a_bank_before_it_is_pinned(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox = root / ft.FALLBACK_INBOX
            write_json(inbox / "env-a.json", {"id": "env-a", "kind": "research"})
            write_json(inbox / "env-b.json", {"id": "env-b", "kind": "research"})
            observed_exclusions: list[set[str]] = []

            def materialize(_root: Path, raw: dict, *, excluded_banks=None) -> dict:
                excluded = set(excluded_banks or ())
                observed_exclusions.append(excluded)
                bank = next(bank for bank in ("a", "b") if bank not in excluded)
                return {
                    "action": "materialized",
                    "job_id": f"job-{raw['id']}",
                    "record_bank": bank,
                    "descriptor": f".survey/work-queue/submissions/research/attempt-{raw['id']}.json",
                    "changed_paths": [],
                }

            with (
                mock.patch.object(dispatcher, "_is_record_fallback", return_value=True),
                mock.patch.object(dispatcher.record_replay, "materialize", side_effect=materialize),
            ):
                result = dispatcher.dispatch(root, max_items=50)

            self.assertEqual([row["record_bank"] for row in result["processed"]], ["a", "b"])
            self.assertEqual(observed_exclusions, [set(), {"a"}])

    def test_record_only_mode_leaves_generic_fallback_for_ordinary_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox = root / ft.FALLBACK_INBOX
            write_json(inbox / "generic.json", {"schema_version": 1, "id": "generic", "writes": []})

            with mock.patch.object(dispatcher, "_is_record_fallback", return_value=False):
                result = dispatcher.dispatch(root, max_items=50, record_only=True)

            self.assertEqual(result["processed_count"], 0)
            self.assertTrue((inbox / "generic.json").is_file())


if __name__ == "__main__":
    unittest.main()
