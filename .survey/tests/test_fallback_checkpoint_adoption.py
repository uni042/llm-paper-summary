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
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class FallbackCheckpointAdoptionTests(unittest.TestCase):
    def test_newer_released_claim_may_adopt_exact_older_library_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/jobs/job-r1.json", {
                "job_id": "job-r1",
                "type": "research",
                "status": "ready",
                "paper_path": "papers/inference/test.md",
                "depends_on_job_ids": ["job-r1"],
            })
            # This is the historical bad state: a duplicate claim was allocated after
            # the paper had already been checkpointed, then that newer claim was released
            # while explicitly pointing back at the original Library payload.
            write_json(root / ".survey/work-queue/claims/job-r1.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-r1",
                "claim_id": "claim-new",
                "worker_id": "worker-new",
                "attempt_id": "attempt-new",
                "claimed_at": "2026-09-15T00:10:00+00:00",
                "expires_at": "2026-09-15T00:11:00+00:00",
                "released_at": "2026-09-15T00:11:00+00:00",
                "previous_claim_id": "claim-old",
                "checkpoint_ref": "/LLM-survey-outbox/pending/env-old.json",
            })
            for bank_root in BANK_ROOTS.values():
                for slot in SLOT_NAMES:
                    write_json(root / bank_root / f"{slot}.json", {
                        "schema_version": 1,
                        "transport_version": 10,
                        "slot": slot,
                        "job_id": "unused-bank-placeholder",
                        "attempt_id": "unused-bank-placeholder",
                        "data": {},
                    })

            writes = []
            for slot in SLOT_NAMES:
                writes.append({
                    "path": f".survey/work-queue/records/chat-record/{slot}.json",
                    "content": json.dumps({
                        "schema_version": 1,
                        "transport_version": 10,
                        "slot": slot,
                        "job_id": "job-r1",
                        "attempt_id": "attempt-old",
                        "data": {"slot": slot},
                    }, ensure_ascii=False),
                })
            envelope = {
                "schema_version": 1,
                "id": "env-old",
                "origin": "claimed_worker",
                "kind": "research",
                "job_id": "job-r1",
                "claim_id": "claim-old",
                "worker_id": "worker-old",
                "attempt_id": "attempt-old",
                "depends_on_job_ids": ["job-r1"],
                "paper_path": "papers/inference/test.md",
                "writes": writes,
            }
            inbox = root / ft.FALLBACK_INBOX
            inbox.mkdir(parents=True, exist_ok=True)
            (inbox / "env-old.json").write_text(ft.canonical_text(envelope), encoding="utf-8")

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "dispatched")
            self.assertTrue((root / ".survey/work-queue/submissions/research/attempt-old.json").is_file())
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-old.json").is_file())
            self.assertFalse((root / ft.FALLBACK_FAILED / "env-old.json").exists())


if __name__ == "__main__":
    unittest.main()
