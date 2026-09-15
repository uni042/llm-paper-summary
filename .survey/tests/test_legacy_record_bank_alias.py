from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dispatch_fallback_inbox  # noqa: E402
import fallback_transport as ft  # noqa: E402
import replay_record_fallback as record_replay  # noqa: E402
from record_bank_config import SLOT_NAMES  # noqa: E402


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class LegacyRecordBankAliasTests(unittest.TestCase):
    def test_terminal_legacy_chat_record_a_bundle_is_acknowledged(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root / ".survey/work-queue/jobs/job-r1.json",
                {
                    "job_id": "job-r1",
                    "type": "research",
                    "status": "completed",
                    "paper_path": "papers/inference/test.md",
                    "depends_on_job_ids": ["job-r1"],
                },
            )

            writes = []
            for slot in SLOT_NAMES:
                writes.append(
                    {
                        "path": f".survey/work-queue/records/chat-record-a/{slot}.json",
                        "content": json.dumps(
                            {
                                "schema_version": 1,
                                "transport_version": 10,
                                "slot": slot,
                                "job_id": "job-r1",
                                "attempt_id": "attempt-a",
                                "data": {"slot": slot},
                            },
                            ensure_ascii=False,
                        ),
                    }
                )
            writes.append(
                {
                    "path": record_replay.CHAT_INBOX,
                    "content": json.dumps(
                        {
                            "schema_version": 1,
                            "transport_version": 10,
                            "kind": "research",
                            "job_id": "job-r1",
                            "claim_id": "claim-a",
                            "worker_id": "worker-a",
                            "attempt_id": "attempt-a",
                            "depends_on_job_ids": ["job-r1"],
                            "paper_path": "papers/inference/test.md",
                            "record_bank": "a",
                        },
                        ensure_ascii=False,
                    ),
                }
            )
            envelope = {
                "schema_version": 1,
                "id": "legacy-a-terminal",
                "origin": "claimed_worker",
                "kind": "research",
                "job_id": "job-r1",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "attempt_id": "attempt-a",
                "depends_on_job_ids": ["job-r1"],
                "paper_path": "papers/inference/test.md",
                "writes": writes,
            }
            inbox = root / ft.FALLBACK_INBOX
            inbox.mkdir(parents=True, exist_ok=True)
            (inbox / "legacy-a-terminal.json").write_text(ft.canonical_text(envelope), encoding="utf-8")

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "ack_terminal")
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "legacy-a-terminal.json").is_file())
            self.assertFalse((root / ft.FALLBACK_FAILED / "legacy-a-terminal.json").exists())


if __name__ == "__main__":
    unittest.main()
