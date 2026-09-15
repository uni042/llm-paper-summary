import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import repair_claim_bank_recovery  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class RepairClaimBankRecoveryTests(unittest.TestCase):
    def test_repeated_repair_restores_latest_failed_record_into_empty_reserved_bank(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-repair"
            claim_id = "claim-new"
            attempt_id = "attempt-new"
            bank = "b"
            write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
                "job_id": job_id,
                "type": "research",
                "status": "ready",
                "repair_required": True,
                "last_validation_failed_at": "2026-09-15T00:34:45+00:00",
            })
            claim = {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": job_id,
                "kind": "research",
                "claim_id": claim_id,
                "attempt_id": attempt_id,
                "request_id": "req-new",
                "worker_id": "worker",
                "worker_kind": "scheduled_chat",
                "claimed_at": "2026-09-15T00:34:52+00:00",
                "expires_at": "2026-09-15T02:04:52+00:00",
                "depends_on_job_ids": [job_id],
                "record_bank": bank,
            }
            write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
            write_json(root / ".survey/work-queue/claim-results/req-new.json", {
                "request_id": "req-new",
                "assignments": [{**claim}],
            })
            for slot in SLOT_NAMES:
                write_json(root / BANK_ROOTS[bank] / f"{slot}.json", {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": attempt_id,
                    "job_id": job_id,
                    "data": {},
                    "reservation": {"claim_id": claim_id, "worker_id": "worker", "worker_kind": "scheduled_chat"},
                })

            old_attempt = "attempt-previous-failed"
            payloads = {
                slot: {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": old_attempt,
                    "job_id": job_id,
                    "data": {"preserved": slot, "text": "expensive research survives repeated repair"},
                }
                for slot in SLOT_NAMES
            }
            candidate = (
                None,
                f".survey/work-queue/submissions/research/{old_attempt}.json",
                {"attempt_id": old_attempt},
                payloads,
            )
            with patch.object(repair_claim_bank_recovery, "_latest_failed_descriptor", return_value=candidate):
                result = repair_claim_bank_recovery.repair_allocated_claims(
                    root, at="2026-09-15T00:35:00+00:00"
                )

            self.assertEqual(result["repaired"], 1)
            repaired_claim = json.loads((root / ".survey/work-queue/claims" / f"{job_id}.json").read_text())
            self.assertEqual(repaired_claim["record_bank_recovery"], "repair-required-latest-immutable-descriptor")
            self.assertEqual(repaired_claim["record_bank_recovery_attempt_ids"], [old_attempt])
            for slot in SLOT_NAMES:
                payload = json.loads((root / BANK_ROOTS[bank] / f"{slot}.json").read_text())
                self.assertEqual(payload["attempt_id"], attempt_id)
                self.assertEqual(payload["data"], payloads[slot]["data"])
                self.assertEqual(payload["reservation"]["claim_id"], claim_id)


if __name__ == "__main__":
    unittest.main()
