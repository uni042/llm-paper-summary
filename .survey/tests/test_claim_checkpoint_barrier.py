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


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def seed_request(
    root: Path,
    request_id: str,
    *,
    worker_id: str = "scheduled-worker",
    requested_at: datetime = AT,
    checkpointed_jobs=None,
):
    body = {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "requested_at": requested_at.isoformat().replace("+00:00", "Z"),
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    }
    if checkpointed_jobs is not None:
        body["checkpointed_jobs"] = checkpointed_jobs
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", body)


class ClaimCheckpointBarrierTests(unittest.TestCase):
    def test_checkpointed_job_is_skipped_for_that_worker_without_changing_job_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_job(root, "job-checkpointed", 100)
            seed_job(root, "job-next", 90)
            seed_request(root, "req-a", checkpointed_jobs=[{
                "job_id": "job-checkpointed",
                "checkpoint_ref": "/LLM-survey-outbox/pending/punica.json",
            }])

            claim_worker.process_requests(root, at=AT)

            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual([item["job_id"] for item in result["assignments"]], ["job-next"])
            checkpointed = json.loads((root / ".survey/work-queue/jobs/job-checkpointed.json").read_text())
            self.assertEqual(checkpointed["status"], "ready")

    def test_checkpointed_current_claim_is_released_so_same_worker_can_claim_next_job(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_job(root, "job-checkpointed", 100)
            seed_job(root, "job-next", 90)
            seed_request(root, "req-first")
            claim_worker.process_requests(root, at=AT)
            first = json.loads((root / ".survey/work-queue/claim-results/req-first.json").read_text())
            self.assertEqual([item["job_id"] for item in first["assignments"]], ["job-checkpointed"])

            checkpoint_ref = "/LLM-survey-outbox/pending/punica.json"
            seed_request(
                root,
                "req-next",
                requested_at=AT + timedelta(minutes=1),
                checkpointed_jobs=[{
                    "job_id": "job-checkpointed",
                    "checkpoint_ref": checkpoint_ref,
                }],
            )
            claim_worker.process_requests(root, at=AT + timedelta(minutes=1))

            second = json.loads((root / ".survey/work-queue/claim-results/req-next.json").read_text())
            self.assertEqual([item["job_id"] for item in second["assignments"]], ["job-next"])
            released = json.loads((root / ".survey/work-queue/claims/job-checkpointed.json").read_text())
            self.assertEqual(released["checkpoint_ref"], checkpoint_ref)
            self.assertEqual(released["checkpoint_release_request_id"], "req-next")
            self.assertIn("released_at", released)
            checkpointed = json.loads((root / ".survey/work-queue/jobs/job-checkpointed.json").read_text())
            self.assertEqual(checkpointed["status"], "ready")


if __name__ == "__main__":
    unittest.main()
