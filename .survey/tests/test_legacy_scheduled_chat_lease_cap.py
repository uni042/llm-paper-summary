import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402
import claim_worker_with_banks  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


AT = datetime(2026, 9, 13, 3, 0, tzinfo=timezone.utc)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_job(root: Path, job_id: str, priority: int):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "lane": "research",
        "status": "ready",
        "priority": priority,
        "created_at": "2026-09-12T00:00:00+00:00",
        "title": job_id,
        "paper_path": f"papers/{job_id}.md",
        "depends_on_job_ids": [job_id],
    })


def seed_free_banks(root: Path):
    for bank_root in BANK_ROOTS.values():
        for slot in SLOT_NAMES:
            write_json(root / bank_root / f"{slot}.json", {
                "schema_version": 1,
                "transport_version": 10,
                "slot": slot,
                "attempt_id": "unused-bank-placeholder",
                "job_id": "unused-bank-placeholder",
                "data": {},
            })


def seed_legacy_claim(root: Path, *, heartbeat_at: str | None = None):
    claim = {
        "schema_version": 1,
        "workflow_version": 10,
        "claim_id": "claim-legacy",
        "job_id": "job-old",
        "worker_id": "scheduled-chat-legacy",
        "worker_kind": "scheduled_chat",
        "attempt_id": "attempt-legacy",
        "request_id": "req-legacy",
        "claimed_at": "2026-09-13T00:00:00+00:00",
        "expires_at": "2026-09-13T08:00:00+00:00",
        "kind": "research",
        "depends_on_job_ids": ["job-old"],
    }
    if heartbeat_at is not None:
        claim["heartbeat_at"] = heartbeat_at
    write_json(root / ".survey/work-queue/claims/job-old.json", claim)


def seed_request(root: Path, *, lease_seconds: int = 5400):
    write_json(root / ".survey/work-queue/claim-requests/req-new.json", {
        "schema_version": 1,
        "request_id": "req-new",
        "worker_id": "scheduled-chat-new",
        "worker_kind": "scheduled_chat",
        "requested_at": "2026-09-13T03:00:00+00:00",
        "max_jobs": 1,
        "lease_seconds": lease_seconds,
        "job_types": ["research"],
    })


class LegacyScheduledChatLeaseCapTests(unittest.TestCase):
    def test_scheduled_chat_rejects_lease_above_90_minutes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_job(root, "job-new", 100)
            seed_request(root, lease_seconds=28800)

            result = claim_worker.process_requests(root, at=AT)
            response = json.loads((root / ".survey/work-queue/claim-results/req-new.json").read_text())

            self.assertEqual(result["errors"], 1)
            self.assertFalse(response["ok"])
            self.assertIn("5400", response["error"])
            self.assertFalse((root / ".survey/work-queue/claims/job-new.json").exists())

    def test_stale_legacy_8h_claim_is_normalized_and_no_longer_fences_banks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-old", 10)
            seed_job(root, "job-new", 100)
            seed_legacy_claim(root)
            seed_request(root)

            result = claim_worker_with_banks.process_requests(root, at=AT)
            old_claim = json.loads((root / ".survey/work-queue/claims/job-old.json").read_text())
            new_claim = json.loads((root / ".survey/work-queue/claims/job-new.json").read_text())

            self.assertEqual(old_claim["expires_at"], "2026-09-13T01:30:00+00:00")
            self.assertEqual(old_claim["legacy_lease_original_expires_at"], "2026-09-13T08:00:00+00:00")
            self.assertEqual(old_claim["lease_invalidated_at"], "2026-09-13T03:00:00+00:00")
            self.assertEqual(result["banks_reserved"], 1)
            self.assertEqual(result["banks_fallback"], 0)
            self.assertIsInstance(new_claim.get("record_bank"), str)
            self.assertNotIn("record_bank_fallback", new_claim)

    def test_recent_legacy_claim_is_shortened_and_migrated_without_global_fence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-old", 10)
            seed_job(root, "job-new", 100)
            seed_legacy_claim(root, heartbeat_at="2026-09-13T02:30:00+00:00")
            seed_request(root)

            result = claim_worker_with_banks.process_requests(root, at=AT)
            old_claim = json.loads((root / ".survey/work-queue/claims/job-old.json").read_text())
            new_claim = json.loads((root / ".survey/work-queue/claims/job-new.json").read_text())

            self.assertEqual(old_claim["expires_at"], "2026-09-13T04:00:00+00:00")
            self.assertNotIn("lease_invalidated_at", old_claim)
            self.assertEqual(old_claim.get("record_bank_fallback"), "library")
            self.assertEqual(old_claim.get("record_bank_migration"), "legacy-unbanked-to-library")
            self.assertEqual(result["banks_migrated_unbanked"], 1)
            self.assertEqual(result["banks_reserved"], 1)
            self.assertEqual(result["banks_fallback"], 0)
            self.assertIsInstance(new_claim.get("record_bank"), str)
            self.assertNotIn("record_bank_fallback", new_claim)


if __name__ == "__main__":
    unittest.main()
