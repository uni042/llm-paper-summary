import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402


AT = datetime(2026, 9, 15, 3, 0, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class RepairCheckpointDeadlockTests(unittest.TestCase):
    def test_durable_validation_failure_can_be_reclaimed_even_with_library_checkpoint_barrier(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-repair"
            old_attempt = "attempt-old-failed"
            checkpoint_ref = "/LLM-survey-outbox/pending/repair.json"

            write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": job_id,
                "type": "research",
                "status": "ready",
                "priority": 100,
                "created_at": "2026-09-14T00:00:00+00:00",
                "title": "repair me",
                "paper_path": "papers/repair-me.md",
                "depends_on_job_ids": [job_id],
                "repair_required": True,
                "validation_error": "RecordValidationError: repair required",
            })
            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "status": "completed",
                "attempt_id": old_attempt,
                "job_id": job_id,
            }
            write_json(
                root / ".survey/work-queue/submissions/research" / f"{old_attempt}.json",
                descriptor,
            )
            write_json(root / ".survey/work-queue/results/research" / f"{old_attempt}.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "attempt_id": old_attempt,
                "job_id": job_id,
                "error": "RecordValidationError: repair required",
            })
            request_id = "req-repair"
            write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
                "schema_version": 1,
                "request_id": request_id,
                "worker_id": "scheduled-chat-llm-survey-20260915T1200JST",
                "worker_kind": "scheduled_chat",
                "requested_at": AT.isoformat().replace("+00:00", "Z"),
                "max_jobs": 1,
                "lease_seconds": 5400,
                "job_types": ["research"],
                "checkpointed_jobs": [{"job_id": job_id, "checkpoint_ref": checkpoint_ref}],
            })

            claim_worker.process_requests(root, at=AT)

            result = json.loads(
                (root / ".survey/work-queue/claim-results" / f"{request_id}.json").read_text()
            )
            self.assertEqual([row["job_id"] for row in result["assignments"]], [job_id])
            self.assertNotEqual(result["assignments"][0]["attempt_id"], old_attempt)


if __name__ == "__main__":
    unittest.main()
