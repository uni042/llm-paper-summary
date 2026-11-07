import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker  # noqa: E402

AT = datetime(2026, 9, 15, 16, 15, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_job(root: Path, job_id: str, priority: int):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "priority": priority,
        "created_at": "2026-09-12T00:00:00+00:00",
        "paper_path": f"papers/{job_id}.md",
        "depends_on_job_ids": [job_id],
    })


class TargetedClaimTests(unittest.TestCase):
    def test_target_job_ids_restrict_claim_selection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root, "job-unrelated-high", 100)
            write_job(root, "job-repair-target", 10)
            request_id = "req-targeted-repair"
            write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
                "schema_version": 1,
                "request_id": request_id,
                "worker_id": "work-repair-controller",
                "worker_kind": "work",
                "requested_at": "2026-09-15T16:15:00+00:00",
                "max_jobs": 1,
                "lease_seconds": 5400,
                "job_types": ["research"],
                "target_job_ids": ["job-repair-target"],
            })

            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results" / f"{request_id}.json").read_text())

            self.assertTrue(result["ok"])
            self.assertEqual([row["job_id"] for row in result["assignments"]], ["job-repair-target"])
            self.assertFalse((root / ".survey/work-queue/claims/job-unrelated-high.json").exists())

    def test_target_job_ids_reject_unknown_or_duplicate_targets(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_job(root, "job-repair-target", 10)
            for request_id, targets in (
                ("req-duplicate", ["job-repair-target", "job-repair-target"]),
                ("req-too-many", ["job-a", "job-b"]),
            ):
                write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
                    "schema_version": 1,
                    "request_id": request_id,
                    "worker_id": "work-repair-controller",
                    "worker_kind": "work",
                    "requested_at": "2026-09-15T16:15:00+00:00",
                    "max_jobs": 1,
                    "lease_seconds": 5400,
                    "job_types": ["research"],
                    "target_job_ids": targets,
                })
            claim_worker.process_requests(root, at=AT)
            for request_id in ("req-duplicate", "req-too-many"):
                result = json.loads((root / ".survey/work-queue/claim-results" / f"{request_id}.json").read_text())
                self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
