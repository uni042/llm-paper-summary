import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402


AT = datetime(2026, 9, 15, 0, 0, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_job(root: Path, job_id: str, priority: int):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "priority": priority,
        "created_at": "2026-09-14T00:00:00+00:00",
        "title": job_id,
        "paper_path": f"papers/{job_id}.md",
        "depends_on_job_ids": [job_id],
    })


def seed_request(root: Path, request_id: str):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": "scheduled-chat-llm-survey-20260915T0030JST",
        "worker_kind": "scheduled_chat",
        "requested_at": AT.isoformat().replace("+00:00", "Z"),
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    })


class LibraryCheckpointRegistryTests(unittest.TestCase):
    def test_persisted_checkpoint_ref_blocks_reclaim_without_request_echo(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_job(root, "job-checkpointed", 100)
            seed_job(root, "job-next", 90)
            write_json(root / ".survey/work-queue/claims/job-checkpointed.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "claim_id": "claim-old",
                "job_id": "job-checkpointed",
                "worker_id": "scheduled-chat-llm-survey-20260914T2330JST",
                "worker_kind": "scheduled_chat",
                "attempt_id": "attempt-old",
                "request_id": "req-old",
                "claimed_at": (AT - timedelta(minutes=5)).isoformat(),
                "expires_at": (AT - timedelta(minutes=1)).isoformat(),
                "released_at": (AT - timedelta(minutes=1)).isoformat(),
                "kind": "research",
                "depends_on_job_ids": ["job-checkpointed"],
                "checkpoint_ref": "/LLM-survey-outbox/pending/job-checkpointed.json",
            })
            seed_request(root, "req-new")

            claim_worker.process_requests(root, at=AT)

            result = json.loads((root / ".survey/work-queue/claim-results/req-new.json").read_text())
            self.assertEqual([item["job_id"] for item in result["assignments"]], ["job-next"])
            job = json.loads((root / ".survey/work-queue/jobs/job-checkpointed.json").read_text())
            self.assertEqual(job["status"], "ready")


if __name__ == "__main__":
    unittest.main()
