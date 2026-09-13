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


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def request(root: Path, request_id: str, worker_id: str):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": worker_id,
        "worker_kind": "work",
        "requested_at": "2026-09-13T00:00:00Z",
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    })


class ClaimTelemetryTests(unittest.TestCase):
    def test_new_assignments_are_not_inflated_by_reused_history(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request(root, "req-old", "old-worker")
            write_json(root / ".survey/work-queue/claim-results/req-old.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "request_id": "req-old",
                "worker_id": "old-worker",
                "worker_kind": "work",
                "ok": True,
                "assignments": [{"job_id": "job-old", "claim_id": "claim-old"}],
                "processed_at": "2026-09-12T00:00:00+00:00",
            })
            request(root, "req-new", "new-worker")
            write_json(root / ".survey/work-queue/jobs/job-new.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-new",
                "type": "research",
                "status": "ready",
                "priority": 100,
                "created_at": "2026-09-12T00:00:00+00:00",
                "depends_on_job_ids": ["job-new"],
            })

            result = claim_worker.process_requests(root, at=AT)

            self.assertEqual(result["assigned"], 1)
            self.assertEqual(result["assigned_new"], 1)
            self.assertEqual(result["assigned_reused"], 1)
            self.assertEqual(result["reused"], 1)


if __name__ == "__main__":
    unittest.main()
