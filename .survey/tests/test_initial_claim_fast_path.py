from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_window_policy
import initial_claim_fast_path
import select_record_bank
from record_bank_config import BANK_ROOTS, SLOT_NAMES

AT = datetime(2026, 9, 23, 13, 0, tzinfo=timezone.utc)


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
                "attempt_id": select_record_bank.PLACEHOLDER_ATTEMPT,
                "job_id": select_record_bank.PLACEHOLDER_ATTEMPT,
                "data": {},
            })


def seed_pool_claim(root: Path, index: int):
    job_id = f"job-{index}"
    claim_id = f"claim-preload-{index}"
    attempt_id = f"attempt-preload-{index}"
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "priority": 100 - index,
        "created_at": f"2026-09-23T12:{index:02d}:00+00:00",
    })
    write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "claim_id": claim_id,
        "job_id": job_id,
        "worker_id": "shared-preload-pool",
        "worker_kind": "work",
        "attempt_id": attempt_id,
        "claimed_at": "2026-09-23T12:00:00+00:00",
        "preloaded_at": "2026-09-23T12:00:00+00:00",
        "expires_at": "2026-09-24T00:00:00+00:00",
        "kind": "research",
        "depends_on_job_ids": [job_id],
        "preload_pool": True,
        "pool_order": index,
        "claim_source": "shared_preload_pool",
    })


def seed_request(root: Path, window: int):
    request_id = "auto-initial-claim-test"
    path = root / ".survey/work-queue/claim-requests" / f"{request_id}.json"
    write_json(path, {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": "worker-7",
        "worker_kind": "scheduled_chat",
        "requested_at": "2026-09-23T13:00:00+00:00",
        "max_jobs": 1,
        "claim_window": window,
        "job_types": ["research", "audit"],
        "run_key": "run-fast",
        "scheduled_slot": "adhoc",
        "actual_invocation_start": "2026-09-23T13:00:00+00:00",
        "auto_initial_claim": True,
    })
    return path


class InitialClaimPoolFastPathTests(unittest.TestCase):
    def test_adopts_deep_inventory_but_banks_only_hot_slice(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_free_banks(root)
            for index in range(6):
                seed_pool_claim(root, index)
            request = seed_request(root, 6)

            with mock.patch.object(
                initial_claim_fast_path.derive_worker_run_state,
                "apply_claim_result_deltas",
                return_value={"generated_results": []},
            ) as state:
                summary = initial_claim_fast_path.process(root, request, at=AT)

            self.assertEqual(summary["assigned"], 6)
            self.assertEqual(summary["claim_window"], 6)
            self.assertEqual(summary["bank_reconciliation"]["reserved"], 4)
            result = json.loads(
                (root / ".survey/work-queue/claim-results/auto-initial-claim-test.json").read_text()
            )
            self.assertEqual(len(result["assignments"]), 6)
            self.assertEqual(result["claim_window_remaining"], 0)
            self.assertEqual(result["hot_banked_claim_target"], 4)
            self.assertEqual(result["assignments"][0]["pipeline_role"], "foreground")
            self.assertTrue(all(
                row["pipeline_role"] == "standby"
                for row in result["assignments"][1:]
            ))

            hot = result["assignments"][:claim_window_policy.HOT_BANKED_CLAIMS]
            cold = result["assignments"][claim_window_policy.HOT_BANKED_CLAIMS:]
            self.assertEqual(len({row["record_bank"] for row in hot}), 4)
            self.assertTrue(all("record_bank" not in row for row in cold))
            for row in hot:
                payload = json.loads(
                    (root / BANK_ROOTS[row["record_bank"]] / "metadata.json").read_text()
                )
                self.assertEqual(payload["reservation"]["claim_id"], row["claim_id"])
                self.assertEqual(payload["reservation"]["worker_id"], "worker-7")
            state.assert_called_once()

    def test_pool_shortfall_declines_before_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_pool_claim(root, 0)
            request = seed_request(root, 2)

            with self.assertRaises(initial_claim_fast_path.InitialClaimFastPathUnavailable):
                initial_claim_fast_path.process(root, request, at=AT)

            self.assertFalse(
                (root / ".survey/work-queue/claim-results/auto-initial-claim-test.json").exists()
            )
            claim = json.loads((root / ".survey/work-queue/claims/job-0.json").read_text())
            self.assertTrue(claim["preload_pool"])
            self.assertEqual(claim["worker_id"], "shared-preload-pool")
            self.assertNotIn("record_bank", claim)


if __name__ == "__main__":
    unittest.main()
