import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_lease_policy  # noqa: E402
import claim_state  # noqa: E402
import claim_worker  # noqa: E402

AT = datetime(2026, 9, 13, 0, 0, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_job(root: Path, job_id: str = "job-r1"):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1, "workflow_version": 10, "job_id": job_id,
        "type": "research", "status": "ready", "priority": 50,
        "created_at": "2026-09-12T00:00:00+00:00", "title": job_id,
        "paper_path": f"papers/{job_id}.md", "depends_on_job_ids": [job_id],
    })


class ScheduledChatLeaseMigrationTests(unittest.TestCase):
    def test_scheduled_chat_cannot_request_eight_hour_lease(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_json(root / ".survey/work-queue/claim-requests/req-a.json", {
                "schema_version": 1, "request_id": "req-a", "worker_id": "scheduled-chat-test",
                "worker_kind": "scheduled_chat", "requested_at": "2026-09-13T00:00:00+00:00",
                "max_jobs": 1, "lease_seconds": 28800, "job_types": ["research"],
            })
            claim_lease_policy.normalize(root, AT)
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertFalse(result["ok"])
            self.assertIn("5400", result["error"])
            self.assertFalse((root / ".survey/work-queue/claims/job-r1.json").exists())

    def test_shorter_scheduled_chat_lease_remains_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_json(root / ".survey/work-queue/claim-requests/req-a.json", {
                "schema_version": 1, "request_id": "req-a", "worker_id": "scheduled-chat-test",
                "worker_kind": "scheduled_chat", "requested_at": "2026-09-13T00:00:00+00:00",
                "max_jobs": 1, "lease_seconds": 300, "job_types": ["research"],
            })
            claim_lease_policy.normalize(root, AT)
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertTrue(result["ok"])
            self.assertEqual(len(result["assignments"]), 1)

    def test_active_legacy_scheduled_chat_lease_is_capped_and_invalidated_after_90_minutes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_json(root / ".survey/work-queue/claims/job-r1.json", {
                "schema_version": 1, "workflow_version": 10, "job_id": "job-r1",
                "claim_id": "claim-old", "request_id": "req-old", "worker_id": "scheduled-chat-old",
                "worker_kind": "scheduled_chat", "attempt_id": "attempt-old", "kind": "research",
                "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": "2026-09-13T08:00:00+00:00",
            })
            claim_lease_policy.normalize(root, AT + timedelta(hours=2))
            claim = json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text())
            self.assertEqual(claim["expires_at"], "2026-09-13T01:30:00+00:00")
            self.assertEqual(claim["invalidation_reason"], "legacy_scheduled_chat_lease_exceeded_90m")
            self.assertFalse(claim_state.current_claims(root, AT + timedelta(hours=2))["job-r1"]["active"])

    def test_work_claim_keeps_explicit_long_lease(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_json(root / ".survey/work-queue/claims/job-r1.json", {
                "schema_version": 1, "workflow_version": 10, "job_id": "job-r1",
                "claim_id": "claim-work", "request_id": "req-work", "worker_id": "work-agent",
                "worker_kind": "work", "attempt_id": "attempt-work", "kind": "research",
                "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": "2026-09-13T08:00:00+00:00",
            })
            claim_lease_policy.normalize(root, AT + timedelta(hours=2))
            claim = json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text())
            self.assertEqual(claim["expires_at"], "2026-09-13T08:00:00+00:00")
            self.assertNotIn("invalidation_reason", claim)

    def test_expired_or_migrated_claim_is_rejected_but_descriptor_release_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            claim_path = root / ".survey/work-queue/claims/job-r1.json"
            descriptor = {"job_id": "job-r1", "attempt_id": "attempt-a", "claim_id": "claim-a", "worker_id": "scheduled-chat-a"}
            write_json(claim_path, {
                "job_id": "job-r1", "claim_id": "claim-a", "worker_id": "scheduled-chat-a",
                "worker_kind": "scheduled_chat", "attempt_id": "attempt-a",
                "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": "2026-09-13T01:30:00+00:00",
                "invalidated_at": "2026-09-13T02:00:00+00:00",
                "invalidation_reason": "legacy_scheduled_chat_lease_exceeded_90m",
            })
            with self.assertRaisesRegex(ValueError, "invalidated"):
                claim_lease_policy.verify_descriptor_claim(root, descriptor, AT + timedelta(hours=2))
            write_json(claim_path, {
                "job_id": "job-r1", "claim_id": "claim-a", "worker_id": "scheduled-chat-a",
                "worker_kind": "scheduled_chat", "attempt_id": "attempt-a",
                "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": "2026-09-13T02:00:00+00:00",
                "released_at": "2026-09-13T02:00:00+00:00",
            })
            claim_lease_policy.verify_descriptor_claim(root, descriptor, AT + timedelta(hours=2, minutes=1))

    def test_plain_expired_claim_without_descriptor_release_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            descriptor = {"job_id": "job-r1", "attempt_id": "attempt-a", "claim_id": "claim-a", "worker_id": "scheduled-chat-a"}
            write_json(root / ".survey/work-queue/claims/job-r1.json", {
                "job_id": "job-r1", "claim_id": "claim-a", "worker_id": "scheduled-chat-a",
                "worker_kind": "scheduled_chat", "attempt_id": "attempt-a",
                "claimed_at": "2026-09-13T00:00:00+00:00", "expires_at": "2026-09-13T01:30:00+00:00",
            })
            with self.assertRaisesRegex(ValueError, "expired"):
                claim_lease_policy.verify_descriptor_claim(root, descriptor, AT + timedelta(hours=2))


if __name__ == "__main__":
    unittest.main()
