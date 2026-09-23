import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import enrich_claim_record_routes  # noqa: E402
import immutable_submission  # noqa: E402
import list_unsettled_immutable_submissions  # noqa: E402
from record_bank_config import (  # noqa: E402
    BANK_ROOTS,
    DISCOVERY_SLOT_NAME,
    SLOT_NAMES,
    discovery_slot_path,
)


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


def legacy_bank_a_descriptor(root: Path, attempt_id: str, job_id: str):
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
    return {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "attempt_id": attempt_id,
        "job_id": job_id,
        "record_bank": "a",
        "paper_path": "papers/inference/test/legacy-a.md",
        "record_slots": refs,
    }


def write_current_claim(root: Path, attempt_id: str, job_id: str):
    write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
        "schema_version": 1,
        "workflow_version": 10,
        "job_id": job_id,
        "type": "research",
        "status": "claimed",
    })
    write_json(root / ".survey/work-queue/claims" / f"{job_id}.json", {
        "schema_version": 1,
        "job_id": job_id,
        "claim_id": "claim-current",
        "request_id": "req-current",
        "attempt_id": attempt_id,
        "record_bank": "a",
        "expires_at": "2099-01-01T00:00:00+00:00",
    })


class RecordBankRoutingContractTests(unittest.TestCase):
    def test_registry_exposes_32_canonical_banks(self):
        expected = tuple("abcdefghijklmnopqrstuvwxyz") + ("aa", "ab", "ac", "ad", "ae", "af")
        self.assertEqual(len(BANK_ROOTS), 32)
        self.assertEqual(tuple(BANK_ROOTS), expected)
        self.assertEqual(BANK_ROOTS["a"], ".survey/work-queue/records/chat-record")
        self.assertEqual(BANK_ROOTS["z"], ".survey/work-queue/records/chat-record-z")
        self.assertEqual(BANK_ROOTS["aa"], ".survey/work-queue/records/chat-record-aa")
        self.assertEqual(BANK_ROOTS["af"], ".survey/work-queue/records/chat-record-af")
        self.assertEqual(len(set(BANK_ROOTS.values())), 32)
        self.assertEqual(DISCOVERY_SLOT_NAME, "discovery-preload")
        self.assertEqual(
            discovery_slot_path("a"),
            ".survey/work-queue/records/chat-record/discovery-preload.json",
        )
        self.assertEqual(
            discovery_slot_path("af"),
            ".survey/work-queue/records/chat-record-af/discovery-preload.json",
        )

    def test_bank_a_legacy_slot_paths_remain_read_compatible(self):
        """Already-durable workflow-v10 descriptors using old bank-A paths must recover."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            attempt_id = "attempt-legacy-a"
            job_id = "job-legacy-a"
            descriptor = legacy_bank_a_descriptor(root, attempt_id, job_id)
            legacy_root = ".survey/work-queue/records/chat-record-a"

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
            claim_path = root / ".survey/work-queue/claims/job-a.json"
            result_path = root / ".survey/work-queue/claim-results/req-a.json"
            write_json(claim_path, {
                "schema_version": 1,
                "job_id": "job-a",
                "claim_id": "claim-a",
                "request_id": "req-a",
                "record_bank": "a",
                "expires_at": "2026-09-17T00:00:00+00:00",
            })
            write_json(result_path, {
                "schema_version": 1,
                "request_id": "req-a",
                "assignments": [{
                    "job_id": "job-a",
                    "claim_id": "claim-a",
                    "record_bank": "a",
                }],
            })

            stats = enrich_claim_record_routes.enrich_routes(
                root,
                at=datetime(2026, 9, 16, 14, 0, tzinfo=timezone.utc),
            )
            claim = json.loads(claim_path.read_text(encoding="utf-8"))
            assignment = json.loads(result_path.read_text(encoding="utf-8"))["assignments"][0]

            expected_paths = {slot: f"{BANK_ROOTS['a']}/{slot}.json" for slot in SLOT_NAMES}
            self.assertEqual(stats["claims_changed"], 1)
            self.assertEqual(stats["claim_results_changed"], 1)
            self.assertEqual(assignment["record_bank_root"], BANK_ROOTS["a"])
            self.assertEqual(assignment["record_slot_paths"], expected_paths)
            self.assertEqual(claim["record_bank_root"], BANK_ROOTS["a"])
            self.assertEqual(claim["record_slot_paths"], expected_paths)
            self.assertNotEqual(assignment["record_bank_root"], ".survey/work-queue/records/chat-record-a")

    def test_legacy_path_failure_is_reopened_only_for_current_attempt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            attempt_id = "attempt-legacy-retry"
            job_id = "job-legacy-retry"
            descriptor = legacy_bank_a_descriptor(root, attempt_id, job_id)
            descriptor_path = root / ".survey/work-queue/submissions/research" / f"{attempt_id}.json"
            result_path = root / ".survey/work-queue/results/research" / f"{attempt_id}.json"
            write_json(descriptor_path, descriptor)
            write_json(result_path, {
                "schema_version": 1,
                "attempt_id": attempt_id,
                "job_id": job_id,
                "ok": False,
                "retryable": False,
                "error": "ValueError: slot metadata must use fixed path .survey/work-queue/records/chat-record/metadata.json",
            })
            write_current_claim(root, attempt_id, job_id)

            self.assertEqual(
                list_unsettled_immutable_submissions.unsettled_paths(root),
                [descriptor_path.relative_to(root).as_posix()],
            )

            claim_path = root / ".survey/work-queue/claims" / f"{job_id}.json"
            claim = json.loads(claim_path.read_text(encoding="utf-8"))
            claim["attempt_id"] = "attempt-new-owner"
            write_json(claim_path, claim)
            self.assertEqual(list_unsettled_immutable_submissions.unsettled_paths(root), [])

    def test_legacy_path_failure_is_not_reopened_after_job_completed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            attempt_id = "attempt-old"
            job_id = "job-completed"
            descriptor = legacy_bank_a_descriptor(root, attempt_id, job_id)
            descriptor_path = root / ".survey/work-queue/submissions/research" / f"{attempt_id}.json"
            result_path = root / ".survey/work-queue/results/research" / f"{attempt_id}.json"
            write_json(descriptor_path, descriptor)
            write_json(result_path, {
                "schema_version": 1,
                "attempt_id": attempt_id,
                "job_id": job_id,
                "ok": False,
                "retryable": False,
                "error": "ValueError: slot metadata must use fixed path .survey/work-queue/records/chat-record/metadata.json",
            })
            write_json(root / ".survey/work-queue/jobs" / f"{job_id}.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": job_id,
                "type": "research",
                "status": "completed",
                "artifact_submission": ".survey/work-queue/submissions/research/attempt-new.json",
            })

            self.assertEqual(list_unsettled_immutable_submissions.unsettled_paths(root), [])


if __name__ == "__main__":
    unittest.main()
