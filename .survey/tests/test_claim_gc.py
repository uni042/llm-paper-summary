import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import full_gc  # noqa: E402


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj) + "\n", encoding="utf-8")


class ClaimGcTests(unittest.TestCase):
    def test_ready_job_claim_and_unprocessed_request_result_are_protected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            write(root / ".survey/work-queue/jobs/job-r1.json", {"job_id": "job-r1", "type": "research", "status": "ready", "created_at": old})
            write(root / ".survey/work-queue/claims/job-r1.json", {"job_id": "job-r1", "claim_id": "claim-a", "assigned_at": old, "expires_at": old})
            write(root / ".survey/work-queue/claim-requests/req-a.json", {"request_id": "req-a", "requested_at": old})
            write(root / ".survey/work-queue/claim-results/req-a.json", {"request_id": "req-a", "ok": True, "assignments": []})
            candidates, skipped = full_gc.collect_claim_artifacts(root, 7, datetime.now(timezone.utc))
            paths = {item["path"].relative_to(root).as_posix() for item in candidates}
            self.assertNotIn(".survey/work-queue/claims/job-r1.json", paths)
            self.assertNotIn(".survey/work-queue/claim-requests/req-a.json", paths)
            self.assertNotIn(".survey/work-queue/claim-results/req-a.json", paths)

    def test_old_terminal_claim_and_settled_request_result_are_collectable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            write(root / ".survey/work-queue/jobs/job-r1.json", {"job_id": "job-r1", "type": "research", "status": "completed", "completed_at": old})
            write(root / ".survey/work-queue/claims/job-r1.json", {"job_id": "job-r1", "claim_id": "claim-a", "assigned_at": old, "expires_at": old})
            write(root / ".survey/work-queue/claim-requests/req-a.json", {"request_id": "req-a", "requested_at": old})
            write(root / ".survey/work-queue/claim-results/req-a.json", {"request_id": "req-a", "ok": True, "processed_at": old, "assignments": []})
            candidates, _ = full_gc.collect_claim_artifacts(root, 7, datetime.now(timezone.utc))
            paths = {item["path"].relative_to(root).as_posix() for item in candidates}
            self.assertIn(".survey/work-queue/claims/job-r1.json", paths)
            self.assertIn(".survey/work-queue/claim-requests/req-a.json", paths)
            self.assertIn(".survey/work-queue/claim-results/req-a.json", paths)


if __name__ == "__main__":
    unittest.main()
