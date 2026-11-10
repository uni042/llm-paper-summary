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


def write_job(root: Path, job_id: str, *, priority: int):
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


class TargetedClaimTests(unittest.TestCase):
    def test_job_ids_limits_claim_to_explicit_jobs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root, "job-high-priority", priority=100)
            write_job(root, "job-target", priority=10)
            write_json(root / ".survey/work-queue/claim-requests/req-targeted.json", {
                "schema_version": 1,
                "request_id": "req-targeted",
                "worker_id": "worker-repair",
                "worker_kind": "work",
                "requested_at": "2026-09-13T00:00:00+00:00",
                "max_jobs": 1,
                "lease_seconds": 28800,
                "job_types": ["research"],
                "job_ids": ["job-target"],
            })

            claim_worker.process_requests(root, at=AT)

            result = json.loads(
                (root / ".survey/work-queue/claim-results/req-targeted.json").read_text(encoding="utf-8")
            )
            self.assertTrue(result["ok"])
            self.assertEqual([item["job_id"] for item in result["assignments"]], ["job-target"])
            self.assertFalse((root / ".survey/work-queue/claims/job-high-priority.json").exists())


if __name__ == "__main__":
    unittest.main()
