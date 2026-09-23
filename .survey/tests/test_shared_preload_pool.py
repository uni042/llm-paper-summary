from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_state
import claim_window_policy
import claim_worker_with_banks
import select_record_bank
import shared_preload_pool
from record_bank_config import BANK_ROOTS, SLOT_NAMES

AT = datetime(2026, 9, 23, 12, 0, tzinfo=timezone.utc)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_banks(root: Path):
    for relative_root in BANK_ROOTS.values():
        for slot in SLOT_NAMES:
            write_json(root / relative_root / f"{slot}.json", {
                "schema_version": 1,
                "transport_version": 10,
                "slot": slot,
                "attempt_id": select_record_bank.PLACEHOLDER_ATTEMPT,
                "job_id": select_record_bank.PLACEHOLDER_ATTEMPT,
                "data": {},
            })


def seed_job(root: Path, index: int, *, priority: int | None = None, job_id: str | None = None):
    job_id = job_id or f"job-{index:03d}"
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "priority": (1000 - index) if priority is None else priority,
        "created_at": f"2026-09-20T00:{index % 60:02d}:00+00:00",
    })
    return job_id


def seed_request(root: Path, request_id: str, worker_id: str, when: datetime, *, window: int = 12):
    write_json(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "requested_at": when.isoformat(),
        "max_jobs": 1,
        "claim_window": window,
        "lease_seconds": 5400,
        "job_types": ["research", "audit"],
    })


def active_inventory(root: Path, at: datetime):
    claims = claim_state.current_claims(root, at)
    return [
        value for value in claims.values()
        if value.get("active")
        and value.get("kind") in {"research", "audit"}
        and (
            shared_preload_pool.is_pool_claim(value)
            or value.get("worker_kind") == "scheduled_chat"
        )
    ]


class SharedPreloadPoolTests(unittest.TestCase):
    def test_maintains_144_logical_inventory_without_consuming_banks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_banks(root)
            for index in range(170):
                seed_job(root, index)

            summary = claim_worker_with_banks.process_requests(
                root,
                at=AT,
                maintain_shared_pool=True,
            )
            claims = claim_state.current_claims(root, AT)
            waiting = shared_preload_pool.waiting_claims(claims)

            self.assertEqual(summary["shared_pool_target"], 144)
            self.assertEqual(summary["shared_pool_inventory_active"], 144)
            self.assertEqual(summary["shared_pool_pool_waiting"], 144)
            self.assertEqual(len(waiting), 144)
            self.assertEqual([row["pool_order"] for row in waiting], list(range(144)))
            self.assertTrue(all("record_bank" not in row for row in waiting))

            bank_state = select_record_bank.inspect(root)
            free_or_reusable = [
                row for row in bank_state["banks"]
                if row["state"] in {"free", "reusable"}
            ]
            self.assertEqual(len(free_or_reusable), len(BANK_ROOTS))

    def test_six_workers_hold_twelve_each_but_only_four_hot_claims_use_banks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_banks(root)
            for index in range(180):
                seed_job(root, index)

            claim_worker_with_banks.process_requests(root, at=AT, maintain_shared_pool=True)
            before = shared_preload_pool.waiting_claims(claim_state.current_claims(root, AT))
            expected = [row["job_id"] for row in before[:72]]

            requests = [
                (f"req-{index}", f"worker-{index}")
                for index in range(1, 7)
            ]
            for offset, (request_id, worker_id) in enumerate(requests):
                seed_request(root, request_id, worker_id, AT + timedelta(seconds=offset + 1))

            summary = claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(minutes=1),
                maintain_shared_pool=False,
            )

            observed = []
            banked = []
            for request_id, _worker_id in sorted(requests):
                result = json.loads(
                    (root / ".survey/work-queue/claim-results" / f"{request_id}.json").read_text()
                )
                self.assertEqual(result["shared_pool_adopted_count"], 12)
                self.assertEqual(len(result["assignments"]), 12)
                hot = result["assignments"][:claim_window_policy.HOT_BANKED_CLAIMS]
                cold = result["assignments"][claim_window_policy.HOT_BANKED_CLAIMS:]
                self.assertTrue(all(isinstance(row.get("record_bank"), str) for row in hot))
                self.assertTrue(all("record_bank" not in row for row in cold))
                observed.extend(row["job_id"] for row in result["assignments"])
                banked.extend(row["record_bank"] for row in hot)

            self.assertEqual(observed, expected)
            self.assertEqual(len(set(observed)), 72)
            self.assertEqual(len(banked), 24)
            self.assertEqual(len(set(banked)), 24)
            self.assertEqual(summary["banks_hot_scheduled_claims"], 24)

            claims = claim_state.current_claims(root, AT + timedelta(minutes=1))
            waiting = shared_preload_pool.waiting_claims(claims)
            self.assertEqual(len(active_inventory(root, AT + timedelta(minutes=1))), 144)
            self.assertEqual(len(waiting), 72)

            bank_state = select_record_bank.inspect(root)
            free_or_reusable = [
                row for row in bank_state["banks"]
                if row["state"] in {"free", "reusable"}
            ]
            self.assertEqual(len(free_or_reusable), 8)

    def test_refill_promotes_cold_standby_into_four_hot_banked_claims(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_banks(root)
            for index in range(170):
                seed_job(root, index)

            claim_worker_with_banks.process_requests(root, at=AT, maintain_shared_pool=True)
            seed_request(root, "req-initial", "worker-1", AT + timedelta(seconds=1))
            claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(seconds=1),
                maintain_shared_pool=False,
            )
            initial = json.loads(
                (root / ".survey/work-queue/claim-results/req-initial.json").read_text()
            )
            first_ids = [row["job_id"] for row in initial["assignments"]]
            self.assertEqual(len(first_ids), 12)
            self.assertTrue(all(
                isinstance(row.get("record_bank"), str)
                for row in initial["assignments"][:4]
            ))
            self.assertTrue(all(
                "record_bank" not in row
                for row in initial["assignments"][4:]
            ))

            # Simulate two terminal foregrounds; the low-watermark policy refills
            # while two old hot claims are still immediately runnable.
            for job_id in first_ids[:2]:
                claim_path = root / ".survey/work-queue/claims" / f"{job_id}.json"
                claim = json.loads(claim_path.read_text())
                claim["released_at"] = (AT + timedelta(seconds=2)).isoformat()
                claim["expires_at"] = (AT + timedelta(seconds=2)).isoformat()
                write_json(claim_path, claim)
                job_path = root / ".survey/work-queue/jobs" / f"{job_id}.json"
                job = json.loads(job_path.read_text())
                job["status"] = "completed"
                write_json(job_path, job)

            seed_request(root, "req-refill", "worker-1", AT + timedelta(seconds=3))
            claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(seconds=3),
                maintain_shared_pool=False,
            )
            refill = json.loads(
                (root / ".survey/work-queue/claim-results/req-refill.json").read_text()
            )
            self.assertEqual(len(refill["assignments"]), 12)
            self.assertEqual(
                [row["job_id"] for row in refill["assignments"][:2]],
                first_ids[2:4],
            )
            hot = refill["assignments"][:claim_window_policy.HOT_BANKED_CLAIMS]
            cold = refill["assignments"][claim_window_policy.HOT_BANKED_CLAIMS:]
            self.assertTrue(all(isinstance(row.get("record_bank"), str) for row in hot))
            self.assertTrue(all("record_bank" not in row for row in cold))
            self.assertEqual(len({row["record_bank"] for row in hot}), 4)


    def test_new_high_priority_job_is_appended_behind_loaded_fifo(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_banks(root)
            for index in range(170):
                seed_job(root, index)

            claim_worker_with_banks.process_requests(root, at=AT, maintain_shared_pool=True)
            initial = shared_preload_pool.waiting_claims(claim_state.current_claims(root, AT))
            initial_ids = [row["job_id"] for row in initial]

            seed_job(root, 999, priority=100000, job_id="job-new-high")
            seed_request(root, "req-first", "worker-1", AT + timedelta(minutes=1))
            claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(minutes=1),
                maintain_shared_pool=True,
            )
            first_result = json.loads(
                (root / ".survey/work-queue/claim-results/req-first.json").read_text()
            )
            self.assertEqual(
                [row["job_id"] for row in first_result["assignments"]],
                initial_ids[:12],
            )

            completed_job = first_result["assignments"][0]["job_id"]
            job_path = root / ".survey/work-queue/jobs" / f"{completed_job}.json"
            job = json.loads(job_path.read_text())
            job["status"] = "completed"
            write_json(job_path, job)

            claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(minutes=2),
                maintain_shared_pool=True,
            )
            claims = claim_state.current_claims(root, AT + timedelta(minutes=2))
            high = claims["job-new-high"]
            self.assertTrue(shared_preload_pool.is_pool_claim(high))
            older_waiting = [
                row for row in shared_preload_pool.waiting_claims(claims)
                if row["job_id"] != "job-new-high"
            ]
            self.assertGreater(high["pool_order"], max(row["pool_order"] for row in older_waiting))
            self.assertNotIn("record_bank", high)

            seed_request(root, "req-second", "worker-2", AT + timedelta(minutes=3))
            claim_worker_with_banks.process_requests(
                root,
                at=AT + timedelta(minutes=3),
                maintain_shared_pool=True,
            )
            second = json.loads(
                (root / ".survey/work-queue/claim-results/req-second.json").read_text()
            )
            self.assertNotIn("job-new-high", [row["job_id"] for row in second["assignments"]])
            self.assertEqual(
                [row["job_id"] for row in second["assignments"]],
                initial_ids[12:24],
            )


if __name__ == "__main__":
    unittest.main()
