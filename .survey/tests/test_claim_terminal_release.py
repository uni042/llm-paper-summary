import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_state  # noqa: E402
import claim_worker  # noqa: E402


AT = datetime(2026, 9, 13, 19, 8, tzinfo=timezone.utc)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ClaimTerminalReleaseTests(unittest.TestCase):
    def test_completed_legacy_job_does_not_block_same_worker_next_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            queue = root / ".survey/work-queue"

            write_json(queue / "jobs/job-done.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-done",
                "type": "research",
                "status": "completed",
                "priority": 90,
                "created_at": "2026-09-13T18:00:00+00:00",
                "artifact_submission": "work-queue/submissions/chat-inbox.json",
                "depends_on_job_ids": ["job-done"],
            })
            write_json(queue / "claims/job-done.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "claim_id": "claim-done",
                "job_id": "job-done",
                "worker_id": "scheduled-chat-llm-survey",
                "worker_kind": "scheduled_chat",
                "attempt_id": "attempt-done",
                "request_id": "req-old",
                "claimed_at": "2026-09-13T18:54:54+00:00",
                "expires_at": (AT + timedelta(minutes=70)).replace(microsecond=0).isoformat(),
                "kind": "research",
                "depends_on_job_ids": ["job-done"],
            })
            write_json(queue / "jobs/job-next.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-next",
                "type": "research",
                "status": "ready",
                "priority": 80,
                "created_at": "2026-09-13T18:30:00+00:00",
                "title": "next",
                "paper_path": "papers/next.md",
                "depends_on_job_ids": ["job-next"],
            })
            write_json(queue / "claim-requests/req-next.json", {
                "schema_version": 1,
                "request_id": "req-next",
                "worker_id": "scheduled-chat-llm-survey",
                "worker_kind": "scheduled_chat",
                "requested_at": AT.replace(microsecond=0).isoformat(),
                "max_jobs": 1,
                "lease_seconds": 5400,
                "job_types": ["research"],
            })

            claim_worker.process_requests(root, at=AT)

            result = json.loads((queue / "claim-results/req-next.json").read_text(encoding="utf-8"))
            self.assertEqual([item["job_id"] for item in result["assignments"]], ["job-next"])
            current = claim_state.current_claims(root, AT)
            self.assertFalse(current["job-done"]["active"])
            self.assertEqual(current["job-done"].get("terminal_job_status"), "completed")

    def test_missing_result_recovery_does_not_reassign_terminal_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            queue = root / ".survey/work-queue"
            write_json(queue / "jobs/job-r1.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-r1",
                "type": "research",
                "status": "ready",
                "priority": 80,
                "created_at": "2026-09-13T18:00:00+00:00",
                "title": "job-r1",
                "paper_path": "papers/job-r1.md",
                "depends_on_job_ids": ["job-r1"],
            })
            write_json(queue / "claim-requests/req-r1.json", {
                "schema_version": 1,
                "request_id": "req-r1",
                "worker_id": "scheduled-chat-llm-survey",
                "worker_kind": "scheduled_chat",
                "requested_at": AT.replace(microsecond=0).isoformat(),
                "max_jobs": 1,
                "lease_seconds": 5400,
                "job_types": ["research"],
            })

            original_write = claim_worker._write

            def interrupt_result(path, obj):
                if "claim-results" in str(path):
                    raise RuntimeError("synthetic result write interruption")
                return original_write(path, obj)

            with patch.object(claim_worker, "_write", side_effect=interrupt_result):
                with self.assertRaisesRegex(RuntimeError, "synthetic result write interruption"):
                    claim_worker.process_requests(root, at=AT)

            job = json.loads((queue / "jobs/job-r1.json").read_text(encoding="utf-8"))
            job["status"] = "completed"
            job["completed_at"] = (AT + timedelta(seconds=1)).isoformat()
            write_json(queue / "jobs/job-r1.json", job)

            claim_worker.process_requests(root, at=AT + timedelta(seconds=2))

            result = json.loads((queue / "claim-results/req-r1.json").read_text(encoding="utf-8"))
            self.assertEqual(result["assignments"], [])


if __name__ == "__main__":
    unittest.main()
