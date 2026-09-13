import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dispatch_fallback_inbox  # noqa: E402
import fallback_transport as ft  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def claim(root: Path, job_id="job-r1", claim_id="claim-a", worker_id="worker-a", attempt_id="attempt-a", *, expires="2026-09-13T01:00:00+00:00"):
    write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", {
        "schema_version": 1, "workflow_version": 10, "job_id": job_id,
        "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id,
        "expires_at": expires,
    })


def envelope(job_id="job-r1", claim_id="claim-a", worker_id="worker-a", attempt_id="attempt-a", *, origin="claimed_worker", envelope_id="env-a"):
    writes = []
    for slot in SLOT_NAMES:
        writes.append({"path": f".survey/work-queue/records/chat-record/{slot}.json", "content": json.dumps({"schema_version": 1, "transport_version": 10, "slot": slot, "job_id": job_id, "attempt_id": attempt_id, "data": {"slot": slot}})})
    writes.append({"path": ft.CHAT_INBOX, "content": json.dumps({"schema_version": 1, "transport_version": 10, "job_id": job_id, "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id, "paper_path": "papers/test.md", "record_bank": "a"})})
    return {"schema_version": 1, "id": envelope_id, "origin": origin, "job_id": job_id, "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id, "writes": writes}


def seed_job(root: Path, job_id="job-r1", status="ready"):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {"job_id": job_id, "type": "research", "status": status, "paper_path": "papers/test.md"})


class ClaimedDispatchTests(unittest.TestCase):
    def put(self, root, value):
        raw = ft.canonical_text(value)
        (root / ft.FALLBACK_INBOX).mkdir(parents=True, exist_ok=True)
        (root / ft.FALLBACK_INBOX / f"{value['id']}.json").write_text(raw, encoding="utf-8")

    def seed_free_banks(self, root):
        for bank_root in BANK_ROOTS.values():
            for slot in SLOT_NAMES:
                write_json(root / bank_root / f"{slot}.json", {
                    "schema_version": 1, "transport_version": 10,
                    "slot": slot, "attempt_id": "unused-bank-placeholder", "data": {},
                })

    def test_expired_but_current_claim_is_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root, expires="2026-09-12T23:00:00+00:00")
            self.put(root, envelope())
            self.assertEqual(ft.claimed_envelope_state(root, envelope()), (True, None))

    def test_current_claim_is_remapped_to_a_safe_bank_before_apply(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root); self.seed_free_banks(root)
            self.put(root, envelope())
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "dispatched")
            inbox = json.loads((root / ft.CHAT_INBOX).read_text(encoding="utf-8"))
            self.assertEqual(inbox["record_bank"], "a")
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").exists())

    def test_superseded_claim_is_quarantined_without_transport_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root, claim_id="claim-new", attempt_id="attempt-new")
            value = envelope(claim_id="claim-old", attempt_id="attempt-old")
            self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())
            self.assertFalse((root / ft.CHAT_INBOX).exists())

    def test_missing_claim_is_quarantined(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); value = envelope(); self.put(root, value)
            dispatch_fallback_inbox.dispatch(root)
            error = next((root / ft.FALLBACK_FAILED).glob("*.error.json"))
            self.assertIn("claim", error.read_text(encoding="utf-8"))

    def test_terminal_claimed_envelope_is_archived_without_apply(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root, status="completed"); claim(root); value = envelope(); self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "ack_terminal")
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").exists())
            self.assertFalse((root / ft.CHAT_INBOX).exists())

    def test_legacy_envelope_keeps_dispatch_behavior(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = {"schema_version": 1, "id": "legacy-a", "writes": [{"path": ".survey/work-queue/transport/legacy.json", "content": "{}"}]}
            self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "dispatched")
            self.assertTrue((root / ".survey/work-queue/transport/legacy.json").exists())


if __name__ == "__main__":
    unittest.main()
