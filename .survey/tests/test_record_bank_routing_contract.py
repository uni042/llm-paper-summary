import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_worker_with_banks  # noqa: E402
import immutable_submission  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slot_payload(slot: str, attempt_id: str, job_id: str):
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "data": {"text": f"payload-{slot}"},
    }


class RecordBankRoutingContractTests(unittest.TestCase):
    def test_bank_a_legacy_slot_paths_remain_read_compatible(self):
        """Already-durable workflow-v10 descriptors using old bank-A paths must recover."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            attempt_id = "attempt-legacy-a"
            job_id = "job-legacy-a"
            legacy_root = ".survey/work-queue/records/chat-record-a"
            refs = []
            for slot in SLOT_NAMES:
                path = root / legacy_root / f"{slot}.json"
                write_json(path, slot_payload(slot, attempt_id, job_id))
                refs.append({
                    "slot": slot,
                    "path": path.relative_to(root).as_posix(),
                    "blob_sha": immutable_submission.git_blob_sha(path.read_bytes()),
                })

            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": attempt_id,
                "job_id": job_id,
                "record_bank": "a",
                "paper_path": "papers/inference/test/legacy-a.md",
                "record_slots": refs,
            }

            validated = immutable_submission.validate_descriptor(root, descriptor)
            self.assertEqual(validated["record_bank"], "a")
            self.assertEqual(
                [ref["path"] for ref in validated["record_slots"]],
                [f"{legacy_root}/{slot}.json" for slot in SLOT_NAMES],
            )

    def test_unregistered_slot_path_is_still_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            attempt_id = "attempt-invalid-path"
            job_id = "job-invalid-path"
            wrong_root = ".survey/work-queue/records/not-a-bank"
            refs = []
            for slot in SLOT_NAMES:
                path = root / wrong_root / f"{slot}.json"
                write_json(path, slot_payload(slot, attempt_id, job_id))
                refs.append({
                    "slot": slot,
                    "path": path.relative_to(root).as_posix(),
                    "blob_sha": immutable_submission.git_blob_sha(path.read_bytes()),
                })
            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": attempt_id,
                "job_id": job_id,
                "record_bank": "a",
                "paper_path": "papers/inference/test/invalid.md",
                "record_slots": refs,
            }
            with self.assertRaisesRegex(ValueError, "must use fixed path"):
                immutable_submission.validate_descriptor(root, descriptor)

    def test_claim_result_exposes_exact_canonical_bank_root_and_slot_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            claim = {
                "request_id": "req-a",
                "job_id": "job-a",
                "claim_id": "claim-a",
                "record_bank": "a",
            }
            result_path = root / ".survey/work-queue/claim-results/req-a.json"
            write_json(result_path, {
                "schema_version": 1,
                "request_id": "req-a",
                "assignments": [{
                    "job_id": "job-a",
                    "claim_id": "claim-a",
                    "record_bank": "a",
                }],
            })

            claim_worker_with_banks._persist_assignment_bank(root, claim, "a")
            assignment = json.loads(result_path.read_text(encoding="utf-8"))["assignments"][0]

            self.assertEqual(assignment["record_bank_root"], BANK_ROOTS["a"])
            self.assertEqual(
                assignment["record_slot_paths"],
                {slot: f"{BANK_ROOTS['a']}/{slot}.json" for slot in SLOT_NAMES},
            )
            self.assertNotEqual(assignment["record_bank_root"], ".survey/work-queue/records/chat-record-a")


if __name__ == "__main__":
    unittest.main()
