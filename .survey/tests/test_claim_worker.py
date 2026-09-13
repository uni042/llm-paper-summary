import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_state  # noqa: E402
import claim_worker  # noqa: E402
from unittest.mock import patch  # noqa: E402


AT = datetime(2026, 9, 13, 0, 0, tzinfo=timezone.utc)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def job(root: Path, job_id: str, *, priority=50, created="2026-09-12T00:00:00+00:00", kind="research", status="ready", lane="research"):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1, "workflow_version": 10, "job_id": job_id,
        "type": kind, "lane": lane, "status": status, "priority": priority,
        "created_at": created, "title": job_id, "paper_path": f"papers/{job_id}.md",
        "depends_on_job_ids": [job_id],
    })


def request(root: Path, request_id: str, *, worker="worker-a", worker_kind="work", max_jobs=1, lease=28800, job_types=None):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1, "request_id": request_id, "worker_id": worker,
        "worker_kind": worker_kind, "requested_at": "2026-09-13T00:00:00+00:00",
        "max_jobs": max_jobs, "lease_seconds": lease,
        "job_types": job_types or ["research", "audit"],
    })


class ClaimWorkerTests(unittest.TestCase):
    def test_two_requests_allocate_one_ready_job_only_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1")
            request(root, "req-a", worker="worker-a"); request(root, "req-b", worker="worker-b")
            result = claim_worker.process_requests(root, at=AT)
            self.assertEqual(result["processed"], 2)
            a = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            b = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            assigned = [x["job_id"] for x in a["assignments"] + b["assignments"]]
            self.assertEqual(assigned, ["job-r1"])
            self.assertEqual(len(list((root / ".survey/work-queue/claims").glob("*.json"))), 1)

    def test_priority_created_and_id_order_is_stable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job(root, "job-z", priority=70, created="2026-09-12T00:00:01+00:00")
            job(root, "job-a", priority=70, created="2026-09-12T00:00:01+00:00")
            job(root, "job-low", priority=80)
            request(root, "req-a", max_jobs=3)
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual([x["job_id"] for x in result["assignments"]], ["job-low", "job-a", "job-z"])
            self.assertEqual(result["assignments"][0]["job"]["type"], "research")
            self.assertEqual(result["assignments"][0]["job"]["paper_path"], "papers/job-low.md")
            self.assertEqual(result["assignments"][0]["job"]["depends_on_job_ids"], ["job-low"])
            self.assertNotIn("_path", result["assignments"][0]["job"])

    def test_repeated_request_reuses_authoritative_result_and_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1"); request(root, "req-a")
            first = claim_worker.process_requests(root, at=AT)
            result_path = root / ".survey/work-queue/claim-results/req-a.json"
            claim_path = root / ".survey/work-queue/claims/job-r1.json"
            before = result_path.read_text(); claim_before = claim_path.read_text()
            request(root, "req-a", worker="different")
            second = claim_worker.process_requests(root, at=AT.replace(hour=1))
            self.assertEqual(second["reused"], 1)
            self.assertEqual(result_path.read_text(), before)
            self.assertEqual(claim_path.read_text(), claim_before)
            self.assertEqual(first["processed"], 1)

    def test_expired_current_claim_is_reallocated_but_active_is_not(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1")
            request(root, "req-a", worker="worker-a", lease=300)
            claim_worker.process_requests(root, at=AT)
            request(root, "req-b", worker="worker-b")
            claim_worker.process_requests(root, at=AT + timedelta(seconds=100))
            b = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            self.assertEqual(b["assignments"], [])
            request(root, "req-c", worker="worker-c")
            claim_worker.process_requests(root, at=AT + timedelta(seconds=301))
            c = json.loads((root / ".survey/work-queue/claim-results/req-c.json").read_text())
            self.assertEqual([x["job_id"] for x in c["assignments"]], ["job-r1"])
            self.assertNotEqual(c["assignments"][0]["claim_id"], json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text()).get("previous_claim_id"))

    def test_terminal_and_discovery_jobs_are_not_claimable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-d", kind="discovery", lane="discovery"); job(root, "job-done", status="completed")
            request(root, "req-a", worker_kind="scheduled_chat")
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual(result["assignments"], [])

    def test_invalid_request_writes_deterministic_error_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/claim-requests/bad.json", {"schema_version": 1, "request_id": "other"})
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/bad.json").read_text())
            self.assertFalse(result["ok"])
            self.assertEqual(result["assignments"], [])
            self.assertIn("request_id", result["error"])
            self.assertIn("processed_at", result)

    def test_claim_write_interruption_is_recovered_without_new_assignment(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1"); request(root, "req-a")
            original = claim_worker._write
            def interrupted(path, obj):
                if "claim-results" in str(path):
                    raise RuntimeError("synthetic interruption")
                return original(path, obj)
            with patch.object(claim_worker, "_write", side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError, "synthetic interruption"):
                    claim_worker.process_requests(root, at=AT)
            claim_path = root / ".survey/work-queue/claims/job-r1.json"
            self.assertTrue(claim_path.exists())
            claim_before = claim_path.read_text()
            claim_worker.process_requests(root, at=AT + timedelta(seconds=1))
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual([x["job_id"] for x in result["assignments"]], ["job-r1"])
            self.assertEqual(claim_path.read_text(), claim_before)

    def test_invalid_canonical_job_id_or_filename_is_not_claimed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/jobs/job-bad.json", {"job_id": "../bad", "type": "research", "status": "ready"})
            write_json(root / ".survey/work-queue/jobs/job-mismatch.json", {"job_id": "job-other", "type": "research", "status": "ready"})
            request(root, "req-a")
            claim_worker.process_requests(root, at=AT)
            result = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            self.assertEqual(result["assignments"], [])
            self.assertEqual(list((root / ".survey/work-queue/claims").glob("*.json")), [])

    def test_schema_and_non_utc_request_timestamps_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); write_json(root / ".survey/work-queue/claim-requests/req-a.json", {"schema_version": 2, "request_id": "req-a", "worker_id": "worker-a", "worker_kind": "work", "requested_at": "2026-09-13T00:00:00+00:00"})
            write_json(root / ".survey/work-queue/claim-requests/req-b.json", {"schema_version": 1, "request_id": "req-b", "worker_id": "worker-a", "worker_kind": "work", "requested_at": "2026-09-13T09:00:00+09:00"})
            claim_worker.process_requests(root, at=AT)
            for request_id in ("req-a", "req-b"):
                result = json.loads((root / ".survey/work-queue/claim-results" / f"{request_id}.json").read_text())
                self.assertFalse(result["ok"])

    def test_claim_is_inactive_at_exact_expiry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1"); request(root, "req-a", lease=300)
            claim_worker.process_requests(root, at=AT)
            claims = claim_state.current_claims(root, AT + timedelta(seconds=300))
            self.assertFalse(claims["job-r1"]["active"])

    def test_claim_snapshot_marks_active_and_claimable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); job(root, "job-r1"); job(root, "job-r2")
            request(root, "req-a", worker="worker-a")
            claim_worker.process_requests(root, at=AT)
            jobs = [json.loads(p.read_text()) for p in (root / ".survey/work-queue/jobs").glob("*.json")]
            self.assertEqual(claim_state.snapshot_claiming(jobs, root, AT), {
                "ready_research_audit": 2, "actively_claimed": 1, "claimable": 1,
            })

    def test_four_worker_simulation_reassigns_only_expired_current_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for index in range(4):
                job(root, f"job-r{index}", priority=100 - index)
                request(root, f"req-{index}", worker=f"worker-{index}", lease=300 if index == 0 else 28800)
            result = claim_worker.process_requests(root, at=AT)
            self.assertEqual(result["assigned"], 4)
            assigned = []
            for index in range(4):
                value = json.loads((root / ".survey/work-queue/claim-results" / f"req-{index}.json").read_text())
                assigned.extend(item["job_id"] for item in value["assignments"])
            self.assertEqual(len(set(assigned)), 4)
            request(root, "req-retry", worker="worker-retry")
            claim_worker.process_requests(root, at=AT + timedelta(seconds=299))
            before = json.loads((root / ".survey/work-queue/claim-results/req-retry.json").read_text())
            self.assertEqual(before["assignments"], [])
            request(root, "req-retry-2", worker="worker-retry-2")
            claim_worker.process_requests(root, at=AT + timedelta(seconds=301))
            after = json.loads((root / ".survey/work-queue/claim-results/req-retry-2.json").read_text())
            self.assertEqual([item["job_id"] for item in after["assignments"]], ["job-r0"])


if __name__ == "__main__":
    unittest.main()
