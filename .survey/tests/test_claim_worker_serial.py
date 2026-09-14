import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402

AT = datetime(2026, 9, 13, 0, 0, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_job(root: Path, job_id: str, priority: int):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "priority": priority,
        "created_at": "2026-09-12T00:00:00+00:00",
        "depends_on_job_ids": [job_id],
    })


def add_request(root: Path, request_id: str, *, max_jobs=1):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": "scheduled-chat-20260913-1530",
        "worker_kind": "scheduled_chat",
        "requested_at": "2026-09-13T00:00:00+00:00",
        "max_jobs": max_jobs,
        "job_types": ["research", "audit"],
    })


class SerialScheduledChatClaimTests(unittest.TestCase):
    def test_second_request_resumes_same_unsubmitted_claim_for_same_worker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            add_job(root, "job-b", 80)
            add_request(root, "req-a")
            claim_worker.process_requests(root, at=AT)
            first = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            first_assignment = first["assignments"][0]
            claim_path = root / ".survey/work-queue/claims/job-a.json"
            current_claim = json.loads(claim_path.read_text())
            current_claim["record_bank"] = None
            current_claim["record_bank_fallback"] = "library"
            write_json(claim_path, current_claim)

            add_request(root, "req-b")
            claim_worker.process_requests(root, at=AT)
            second = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())

            self.assertEqual(len(second["assignments"]), 1)
            resumed = second["assignments"][0]
            self.assertEqual(resumed["job_id"], "job-a")
            self.assertEqual(resumed["claim_id"], first_assignment["claim_id"])
            self.assertEqual(resumed["attempt_id"], first_assignment["attempt_id"])
            self.assertEqual(resumed["claimed_at"], first_assignment["claimed_at"])
            self.assertEqual(resumed["worker_id"], "scheduled-chat-20260913-1530")
            self.assertEqual(resumed["record_bank_fallback"], "library")
            self.assertEqual(second.get("reason"), "resumed active unsubmitted claim")

            job_b_claim = root / ".survey/work-queue/claims/job-b.json"
            self.assertFalse(job_b_claim.exists())

    def test_durable_descriptor_releases_previous_worker_slot_and_next_job_can_be_claimed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            add_job(root, "job-b", 80)
            add_request(root, "req-a")
            claim_worker.process_requests(root, at=AT)
            first = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            assignment = first["assignments"][0]
            write_json(root / ".survey/work-queue/submissions/research" / f"{assignment['attempt_id']}.json", {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": assignment["attempt_id"],
                "job_id": "job-a",
                "record_bank": "a",
            })
            add_request(root, "req-b")
            claim_worker.process_requests(root, at=AT)
            second = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            self.assertEqual([row["job_id"] for row in second["assignments"]], ["job-b"])
            old_claim = json.loads((root / ".survey/work-queue/claims/job-a.json").read_text())
            self.assertIn("released_at", old_claim)
            self.assertEqual(old_claim["expires_at"], "2026-09-13T00:00:00+00:00")

    def test_descriptor_pending_job_is_not_reclaimed_by_other_worker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            write_json(root / ".survey/work-queue/submissions/research/attempt-a.json", {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
            })
            write_json(root / ".survey/work-queue/claim-requests/req-other.json", {
                "schema_version": 1,
                "request_id": "req-other",
                "worker_id": "scheduled-chat-other",
                "worker_kind": "scheduled_chat",
                "requested_at": "2026-09-13T00:00:00+00:00",
                "max_jobs": 1,
                "job_types": ["research"],
            })
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-other.json").read_text())
            self.assertEqual(result["assignments"], [])

    def test_failed_descriptor_stays_pending_and_job_is_not_reclaimed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            write_json(root / ".survey/work-queue/submissions/research/attempt-a.json", {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
            })
            write_json(root / ".survey/work-queue/results/research/attempt-a.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "error": "validation failed",
            })
            write_json(root / ".survey/work-queue/claim-requests/req-other.json", {
                "schema_version": 1,
                "request_id": "req-other",
                "worker_id": "scheduled-chat-other",
                "worker_kind": "scheduled_chat",
                "requested_at": "2026-09-13T00:00:00+00:00",
                "max_jobs": 1,
                "job_types": ["research"],
            })
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-other.json").read_text())
            self.assertEqual(result["assignments"], [])

    def test_scheduled_chat_cannot_request_multiple_jobs_in_one_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            add_request(root, "req-a", max_jobs=2)
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertFalse(result["ok"])
            self.assertEqual(result["assignments"], [])
            self.assertIn("scheduled_chat", result["error"])


if __name__ == "__main__":
    unittest.main()
