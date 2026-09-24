import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker_with_banks  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


AT = datetime(2026, 9, 13, 0, 0, tzinfo=timezone.utc)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_free_banks(root: Path):
    for bank_root in BANK_ROOTS.values():
        for slot in SLOT_NAMES:
            write_json(root / bank_root / f"{slot}.json", {
                "schema_version": 1,
                "transport_version": 10,
                "slot": slot,
                "attempt_id": "unused-bank-placeholder",
                "job_id": "unused-bank-placeholder",
                "data": {},
            })


def seed_job(root: Path, job_id: str):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "lane": "research",
        "status": "ready",
        "priority": 100,
        "created_at": "2026-09-12T00:00:00+00:00",
        "title": job_id,
        "paper_path": f"papers/{job_id}.md",
        "depends_on_job_ids": [job_id],
    })


def seed_request(root: Path, request_id: str, worker_id: str, requested_at: datetime):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": worker_id,
        "worker_kind": "work",
        "requested_at": requested_at.replace(microsecond=0).isoformat(),
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    })


class ExpiredDatafulBankReuseTests(unittest.TestCase):
    def test_same_ready_job_reuses_coherent_dataful_bank_after_claim_expiry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-r1")
            seed_request(root, "req-a", "worker-a", AT)

            claim_worker_with_banks.process_requests(root, at=AT)
            first = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            first_assignment = first["assignments"][0]
            first_bank = first_assignment["record_bank"]
            old_data = {}
            for index, slot in enumerate(SLOT_NAMES):
                data = {"preserved": f"{slot}-{index}"}
                old_data[slot] = data
                write_json(root / BANK_ROOTS[first_bank] / f"{slot}.json", {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": first_assignment["attempt_id"],
                    "job_id": "job-r1",
                    "data": data,
                    "reservation": {
                        "claim_id": first_assignment["claim_id"],
                        "worker_id": "worker-a",
                        "worker_kind": "work",
                    },
                })

            second_at = AT + timedelta(hours=2)
            seed_request(root, "req-b", "worker-b", second_at)
            result = claim_worker_with_banks.process_requests(root, at=second_at)
            second = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            second_assignment = second["assignments"][0]

            self.assertEqual(second_assignment["record_bank"], first_bank)
            self.assertEqual(second_assignment.get("record_bank_recovery"), "expired-same-job")
            self.assertGreaterEqual(result.get("banks_recovered_expired", 0), 1)
            for slot in SLOT_NAMES:
                payload = json.loads((root / BANK_ROOTS[first_bank] / f"{slot}.json").read_text())
                self.assertEqual(payload["job_id"], "job-r1")
                self.assertEqual(payload["attempt_id"], second_assignment["attempt_id"])
                self.assertEqual(payload["data"], old_data[slot])
                self.assertEqual(payload["reservation"]["claim_id"], second_assignment["claim_id"])

    def test_inactive_mixed_bank_is_reclaimed_before_new_allocation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            mixed_root = root / BANK_ROOTS["c"]
            for index, slot in enumerate(SLOT_NAMES):
                owner = "job-old-a" if index == 0 else "job-old-b"
                attempt = "attempt-old-a" if index == 0 else "attempt-old-b"
                claim_id = "claim-old-a" if index == 0 else "claim-old-b"
                write_json(mixed_root / f"{slot}.json", {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": attempt,
                    "job_id": owner,
                    "data": {"stale": slot},
                    "reservation": {
                        "claim_id": claim_id,
                        "worker_id": "old-worker",
                        "worker_kind": "scheduled_chat",
                    },
                })

            seed_job(root, "job-r1")
            seed_request(root, "req-a", "worker-a", AT)
            result = claim_worker_with_banks.process_requests(root, at=AT)

            self.assertGreaterEqual(result.get("banks_reclaimed_inactive_dirty", 0), 1)
            payloads = [
                json.loads((mixed_root / f"{slot}.json").read_text())
                for slot in SLOT_NAMES
            ]
            owners = {(payload["job_id"], payload["attempt_id"]) for payload in payloads}
            self.assertEqual(len(owners), 1)
            self.assertNotIn(("job-old-a", "attempt-old-a"), owners)
            self.assertNotIn(("job-old-b", "attempt-old-b"), owners)


if __name__ == "__main__":
    unittest.main()
