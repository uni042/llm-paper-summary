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


def write_job(root: Path):
    write_json(root / ".survey/work-queue/jobs/job-r1.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": "job-r1",
        "type": "research",
        "lane": "research",
        "status": "ready",
        "priority": 100,
        "created_at": "2026-09-12T00:00:00+00:00",
        "title": "paper",
        "paper_path": "papers/job-r1.md",
        "depends_on_job_ids": ["job-r1"],
    })


def write_request(root: Path, *, requested_at: str, worker: str = "worker-a", lease_seconds=None):
    value = {
        "schema_version": 1,
        "request_id": "req-a",
        "worker_id": worker,
        "worker_kind": "work",
        "requested_at": requested_at,
        "max_jobs": 1,
        "job_types": ["research"],
    }
    if lease_seconds is not None:
        value["lease_seconds"] = lease_seconds
    write_json(root / ".survey/work-queue/claim-requests/req-a.json", value)


class ClaimHeartbeatTests(unittest.TestCase):
    def test_default_claim_lease_is_90_minutes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_request(root, requested_at="2026-09-13T00:00:00+00:00")
            claim_worker.process_requests(root, at=AT)
            claim = json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text())
            self.assertEqual(claim["expires_at"], "2026-09-13T01:30:00+00:00")

    def test_same_worker_replay_renews_existing_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_request(root, requested_at="2026-09-13T00:00:00+00:00")
            claim_worker.process_requests(root, at=AT)

            heartbeat_at = AT + timedelta(hours=1)
            write_request(root, requested_at="2026-09-13T01:00:00+00:00")
            result = claim_worker.process_requests(root, at=heartbeat_at)

            self.assertEqual(result["renewed"], 1)
            claim = json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text())
            self.assertEqual(claim["expires_at"], "2026-09-13T02:30:00+00:00")
            response = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual(response["assignments"][0]["expires_at"], "2026-09-13T02:30:00+00:00")

    def test_different_worker_replay_does_not_renew_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root)
            write_request(root, requested_at="2026-09-13T00:00:00+00:00")
            claim_worker.process_requests(root, at=AT)
            before = (root / ".survey/work-queue/claims/job-r1.json").read_text()

            write_request(root, requested_at="2026-09-13T01:00:00+00:00", worker="worker-b")
            result = claim_worker.process_requests(root, at=AT + timedelta(hours=1))

            self.assertEqual(result["renewed"], 0)
            self.assertEqual((root / ".survey/work-queue/claims/job-r1.json").read_text(), before)


if __name__ == "__main__":
    unittest.main()
