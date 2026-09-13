import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402


AT = datetime(2026, 9, 13, 0, 0, tzinfo=timezone.utc)
WORKER_ID = "scheduled-chat-failed-immutable-test"


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


def add_request(root: Path, request_id: str, requested_at: datetime):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": WORKER_ID,
        "worker_kind": "scheduled_chat",
        "requested_at": requested_at.isoformat(),
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    })


def add_descriptor_and_failed_result(root: Path, assignment: dict):
    attempt_id = assignment["attempt_id"]
    job_id = assignment["job_id"]
    write_json(root / ".survey/work-queue/submissions/research" / f"{attempt_id}.json", {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "attempt_id": attempt_id,
        "job_id": job_id,
        "record_bank": "a",
    })
    write_json(root / ".survey/work-queue/results/research" / f"{attempt_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": False,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "error": "synthetic validation failure",
    })


class FailedImmutableResultClaimSemanticsTests(unittest.TestCase):
    def test_failed_result_keeps_descriptor_pending_for_retry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
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
                "error": "synthetic validation failure",
            })

            pending = claim_worker._immutable_descriptors(root)

            self.assertEqual([(row["job_id"], row["attempt_id"]) for row in pending], [("job-a", "attempt-a")])

    def test_failed_result_does_not_hold_worker_claim_after_durable_capture(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            add_job(root, "job-a", 90)
            add_job(root, "job-b", 80)
            add_request(root, "req-a", AT)
            claim_worker.process_requests(root, at=AT)
            first = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            assignment = first["assignments"][0]
            self.assertEqual(assignment["job_id"], "job-a")
            add_descriptor_and_failed_result(root, assignment)

            later = AT + timedelta(minutes=1)
            add_request(root, "req-b", later)
            claim_worker.process_requests(root, at=later)

            second = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            self.assertEqual([row["job_id"] for row in second["assignments"]], ["job-b"])
            old_claim = json.loads((root / ".survey/work-queue/claims/job-a.json").read_text())
            self.assertIn("released_at", old_claim)


if __name__ == "__main__":
    unittest.main()
