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


def seed_job(root: Path, job_id: str, priority: int):
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


def seed_request(root: Path, request_id: str, worker_id: str):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": worker_id,
        "worker_kind": "work",
        "requested_at": "2026-09-13T00:00:00+00:00",
        "max_jobs": 1,
        "lease_seconds": 5400,
        "job_types": ["research"],
    })


def seed_active_claim(root: Path, job_id: str, request_id: str = "req-old"):
    write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "kind": "research",
        "claim_id": "claim-old",
        "attempt_id": "attempt-old",
        "request_id": request_id,
        "worker_id": "legacy-worker",
        "worker_kind": "work",
        "claimed_at": "2026-09-12T23:30:00+00:00",
        "expires_at": "2026-09-13T01:00:00+00:00",
        "depends_on_job_ids": [job_id],
    })


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


class ClaimBankReservationTests(unittest.TestCase):
    def test_parallel_workers_receive_distinct_record_banks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-r1", 100)
            seed_job(root, "job-r2", 90)
            seed_request(root, "req-a", "worker-a")
            seed_request(root, "req-b", "worker-b")

            claim_worker_with_banks.process_requests(root, at=AT)

            result_a = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            result_b = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            bank_a = result_a["assignments"][0]["record_bank"]
            bank_b = result_b["assignments"][0]["record_bank"]

            self.assertIsInstance(bank_a, str)
            self.assertIsInstance(bank_b, str)
            self.assertNotEqual(bank_a, bank_b)

            claim_a = json.loads((root / ".survey/work-queue/claims/job-r1.json").read_text())
            claim_b = json.loads((root / ".survey/work-queue/claims/job-r2.json").read_text())
            self.assertEqual(claim_a["record_bank"], bank_a)
            self.assertEqual(claim_b["record_bank"], bank_b)

    def test_existing_unbanked_active_claim_is_migrated_to_library_without_global_fence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-old", 100)
            seed_active_claim(root, "job-old")
            seed_job(root, "job-new", 90)
            seed_request(root, "req-new", "worker-new")

            result = claim_worker_with_banks.process_requests(root, at=AT)

            old_claim = json.loads((root / ".survey/work-queue/claims/job-old.json").read_text())
            new_claim = json.loads((root / ".survey/work-queue/claims/job-new.json").read_text())
            new_result = json.loads((root / ".survey/work-queue/claim-results/req-new.json").read_text())
            assignment = new_result["assignments"][0]

            self.assertIsNone(old_claim.get("record_bank"))
            self.assertEqual(old_claim.get("record_bank_fallback"), "library")
            self.assertEqual(old_claim.get("record_bank_migration"), "legacy-unbanked-to-library")
            self.assertEqual(result["banks_migrated_unbanked"], 1)
            self.assertEqual(result["banks_reserved"], 1)
            self.assertEqual(result["banks_fallback"], 0)
            self.assertIsInstance(new_claim.get("record_bank"), str)
            self.assertNotIn("record_bank_fallback", new_claim)
            self.assertEqual(assignment.get("record_bank"), new_claim["record_bank"])

    def test_explicit_library_fallback_does_not_fence_new_bank_use(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-old", 100)
            seed_active_claim(root, "job-old")
            old_claim_path = root / ".survey/work-queue/claims/job-old.json"
            old_claim = json.loads(old_claim_path.read_text())
            old_claim["record_bank"] = None
            old_claim["record_bank_fallback"] = "library"
            write_json(old_claim_path, old_claim)

            seed_job(root, "job-new", 90)
            seed_request(root, "req-new", "worker-new")

            result = claim_worker_with_banks.process_requests(root, at=AT)

            new_claim = json.loads((root / ".survey/work-queue/claims/job-new.json").read_text())
            new_result = json.loads((root / ".survey/work-queue/claim-results/req-new.json").read_text())
            assignment = new_result["assignments"][0]

            self.assertEqual(result["banks_reserved"], 1)
            self.assertEqual(result["banks_fallback"], 0)
            self.assertIsInstance(new_claim.get("record_bank"), str)
            self.assertNotIn("record_bank_fallback", new_claim)
            self.assertEqual(assignment.get("record_bank"), new_claim["record_bank"])
            self.assertNotIn("record_bank_fallback", assignment)

    def test_expired_reservation_is_reused_when_same_ready_job_is_reclaimed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-r1", 100)
            seed_request(root, "req-a", "worker-a")

            claim_worker_with_banks.process_requests(root, at=AT)
            result_a = json.loads((root / ".survey/work-queue/claim-results/req-a.json").read_text())
            first_bank = result_a["assignments"][0]["record_bank"]

            seed_request(root, "req-b", "worker-b")
            claim_worker_with_banks.process_requests(root, at=AT + timedelta(hours=2))
            result_b = json.loads((root / ".survey/work-queue/claim-results/req-b.json").read_text())
            second_bank = result_b["assignments"][0]["record_bank"]

            self.assertEqual(second_bank, first_bank)

    def test_repair_claim_reuses_nonempty_bank_for_same_job_without_losing_data(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            seed_job(root, "job-repair", 100)
            job_path = root / ".survey/work-queue/jobs/job-repair.json"
            job = json.loads(job_path.read_text())
            job["repair_required"] = True
            job["validation_error"] = "ValueError: problem_method.components[0].description is too short"
            write_json(job_path, job)

            recovery_bank = "h"
            original_data = {}
            for index, slot in enumerate(SLOT_NAMES):
                data = {"preserved": f"{slot}-{index}", "text": "already researched content"}
                original_data[slot] = data
                write_json(root / BANK_ROOTS[recovery_bank] / f"{slot}.json", {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": "attempt-old-research",
                    "job_id": "job-repair",
                    "data": data,
                })

            seed_request(root, "req-repair", "worker-repair")
            result = claim_worker_with_banks.process_requests(root, at=AT)

            assignment = json.loads(
                (root / ".survey/work-queue/claim-results/req-repair.json").read_text()
            )["assignments"][0]
            self.assertEqual(assignment["record_bank"], recovery_bank)
            self.assertEqual(result["banks_recovered"], 1)

            for slot in SLOT_NAMES:
                payload = json.loads(
                    (root / BANK_ROOTS[recovery_bank] / f"{slot}.json").read_text()
                )
                self.assertEqual(payload["job_id"], "job-repair")
                self.assertEqual(payload["attempt_id"], assignment["attempt_id"])
                self.assertEqual(payload["data"], original_data[slot])
                self.assertEqual(payload["reservation"]["claim_id"], assignment["claim_id"])


if __name__ == "__main__":
    unittest.main()
