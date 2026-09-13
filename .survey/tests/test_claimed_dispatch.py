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
import select_record_bank  # noqa: E402
import claim_worker  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def claim(root: Path, job_id="job-r1", claim_id="claim-a", worker_id="worker-a", attempt_id="attempt-a", *, expires="2026-09-13T01:00:00+00:00"):
    write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", {
        "schema_version": 1, "workflow_version": 10, "job_id": job_id,
        "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id,
        "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": expires,
    })


def envelope(job_id="job-r1", claim_id="claim-a", worker_id="worker-a", attempt_id="attempt-a", *, origin="claimed_worker", envelope_id="env-a"):
    writes = []
    for slot in SLOT_NAMES:
        writes.append({"path": f".survey/work-queue/records/chat-record/{slot}.json", "content": json.dumps({"schema_version": 1, "transport_version": 10, "slot": slot, "job_id": job_id, "attempt_id": attempt_id, "data": {"slot": slot}})})
    writes.append({"path": ft.CHAT_INBOX, "content": json.dumps({"schema_version": 1, "transport_version": 10, "job_id": job_id, "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id, "kind": "research", "depends_on_job_ids": [job_id], "paper_path": "papers/test.md", "record_bank": "a"})})
    return {"schema_version": 1, "id": envelope_id, "origin": origin, "job_id": job_id, "claim_id": claim_id, "worker_id": worker_id, "attempt_id": attempt_id, "kind": "research", "depends_on_job_ids": [job_id], "writes": writes}


def seed_job(root: Path, job_id="job-r1", status="ready"):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {"job_id": job_id, "type": "research", "status": status, "paper_path": "papers/test.md", "depends_on_job_ids": [job_id]})


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

    def test_claimed_envelope_without_all_five_slots_is_quarantined_before_apply(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root); value = envelope(); value["writes"] = [value["writes"][-1]]; self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())
            self.assertFalse((root / ft.CHAT_INBOX).exists())

    def test_claimed_envelope_with_one_missing_slot_is_quarantined(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root); value = envelope(); value["writes"].pop(1); self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())

    def test_slot_internal_identity_mismatch_is_quarantined_without_bank_or_chat_change(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root); self.seed_free_banks(root); value = envelope()
            before = {path.relative_to(root).as_posix(): path.read_bytes() for path in (root / ".survey/work-queue/records").rglob("*.json")}
            payload = json.loads(value["writes"][0]["content"]); payload["job_id"] = "job-other"; value["writes"][0]["content"] = json.dumps(payload); self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())
            self.assertFalse((root / ft.CHAT_INBOX).exists())
            after = {path.relative_to(root).as_posix(): path.read_bytes() for path in (root / ".survey/work-queue/records").rglob("*.json")}
            self.assertEqual(after, before)

    def test_slot_name_or_transport_version_mismatch_is_quarantined(self):
        for field, value in (("slot", "results"), ("transport_version", 9)):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as td:
                root = Path(td); seed_job(root); claim(root); self.seed_free_banks(root); envelope_value = envelope()
                payload = json.loads(envelope_value["writes"][0]["content"]); payload[field] = value; envelope_value["writes"][0]["content"] = json.dumps(payload); self.put(root, envelope_value)
                result = dispatch_fallback_inbox.dispatch(root)
                self.assertEqual(result["action"], "idle")
                self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())

    def test_dependency_order_extra_or_duplicate_mismatch_is_quarantined(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); claim(root); self.seed_free_banks(root); value = envelope()
            value["depends_on_job_ids"] = ["job-r1", "job-extra", "job-r1"]
            chat = json.loads(value["writes"][-1]["content"]); chat["depends_on_job_ids"] = list(value["depends_on_job_ids"]); value["writes"][-1]["content"] = json.dumps(chat); self.put(root, value)
            result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())

    def test_two_claimed_envelopes_do_not_overwrite_unsettled_bank_or_chat(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); seed_job(root, "job-r2"); claim(root); claim(root, "job-r2", "claim-b", "worker-b", "attempt-b"); self.seed_free_banks(root)
            first = envelope(); second = envelope("job-r2", "claim-b", "worker-b", "attempt-b", envelope_id="env-b")
            self.put(root, first); self.put(root, second)
            self.assertEqual(dispatch_fallback_inbox.dispatch(root)["action"], "dispatched")
            first_inbox = (root / ft.CHAT_INBOX).read_text(encoding="utf-8")
            second_result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(second_result["action"], "idle")
            self.assertEqual((root / ft.CHAT_INBOX).read_text(encoding="utf-8"), first_inbox)
            self.assertTrue((root / ft.FALLBACK_INBOX / "env-b.json").exists())

    def test_selector_reads_all_canonical_ready_job_files_not_truncated_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs = root / ".survey/work-queue/jobs"
            jobs.mkdir(parents=True)
            for index in range(10):
                write_json(jobs / f"job-r{index}.json", {"job_id": f"job-r{index}", "type": "research", "status": "ready"})
            write_json(root / ".survey/work-queue/next-jobs.json", {"next_jobs": [{"job_id": "job-r0"}]})
            self.assertEqual(len(select_record_bank.ready_job_ids(root)), 10)

    def test_allocator_expiry_reassignment_fences_old_envelope_and_dispatches_current(self):
        from datetime import datetime, timedelta, timezone
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); seed_job(root); self.seed_free_banks(root)
            request_root = root / ".survey/work-queue/claim-requests"
            write_json(request_root / "req-a.json", {"schema_version": 1, "request_id": "req-a", "worker_id": "worker-a", "worker_kind": "work", "requested_at": "2026-09-13T00:00:00+00:00", "max_jobs": 1, "lease_seconds": 300, "job_types": ["research"]})
            claim_worker.process_requests(root, at=datetime(2026, 9, 13, tzinfo=timezone.utc))
            first = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())["assignments"][0]
            old = envelope(claim_id=first["claim_id"], worker_id=first["worker_id"], attempt_id=first["attempt_id"])
            (root / ".survey/work-queue/claim-requests/req-b.json").write_text(json.dumps({"schema_version": 1, "request_id": "req-b", "worker_id": "worker-b", "worker_kind": "work", "requested_at": "2026-09-13T00:00:00+00:00", "max_jobs": 1, "lease_seconds": 300, "job_types": ["research"]}), encoding="utf-8")
            claim_worker.process_requests(root, at=datetime(2026, 9, 13, tzinfo=timezone.utc) + timedelta(seconds=301))
            second = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())["assignments"][0]
            current = envelope(claim_id=second["claim_id"], worker_id=second["worker_id"], attempt_id=second["attempt_id"], envelope_id="env-b")
            self.put(root, old); self.put(root, current)
            first_result = dispatch_fallback_inbox.dispatch(root)
            self.assertEqual(first_result["action"], "dispatched")
            self.assertTrue((root / ft.FALLBACK_FAILED / "env-a.json").exists())
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-b.json").exists())

    def test_failed_and_cancelled_claimed_jobs_are_archived_without_apply(self):
        for status in ("failed", "cancelled"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as td:
                root = Path(td); seed_job(root, status=status); claim(root); value = envelope(); self.put(root, value)
                result = dispatch_fallback_inbox.dispatch(root)
                self.assertEqual(result["action"], "ack_terminal")
                self.assertFalse((root / ft.CHAT_INBOX).exists())

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
