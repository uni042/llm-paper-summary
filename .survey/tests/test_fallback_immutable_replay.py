from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dispatch_fallback_inbox  # noqa: E402
import fallback_transport as ft  # noqa: E402
import replay_record_fallback as record_replay  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402

LEGACY_CHAT_INBOX = record_replay.CHAT_INBOX


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_repo(root: Path) -> None:
    write_json(
        root / ".survey/work-queue/jobs/job-r1.json",
        {
            "job_id": "job-r1",
            "type": "research",
            "status": "ready",
            "paper_path": "papers/inference/test.md",
            "depends_on_job_ids": ["job-r1"],
        },
    )
    write_json(
        root / ".survey/work-queue/claims/job-r1.json",
        {
            "schema_version": 1,
            "workflow_version": 10,
            "job_id": "job-r1",
            "claim_id": "claim-a",
            "worker_id": "worker-a",
            "attempt_id": "attempt-a",
            "claimed_at": "2026-09-13T00:00:00+00:00",
            "expires_at": "2999-01-01T00:00:00+00:00",
        },
    )
    for bank_root in BANK_ROOTS.values():
        for slot in SLOT_NAMES:
            write_json(
                root / bank_root / f"{slot}.json",
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": "unused-bank-placeholder",
                    "data": {},
                },
            )


def slot_writes() -> list[dict[str, str]]:
    writes: list[dict[str, str]] = []
    for slot in SLOT_NAMES:
        writes.append(
            {
                "path": f".survey/work-queue/records/chat-record/{slot}.json",
                "content": json.dumps(
                    {
                        "schema_version": 1,
                        "transport_version": 10,
                        "slot": slot,
                        "job_id": "job-r1",
                        "attempt_id": "attempt-a",
                        "data": {"slot": slot},
                    },
                    ensure_ascii=False,
                ),
            }
        )
    return writes


def root_fields() -> dict:
    return {
        "schema_version": 1,
        "id": "env-a",
        "origin": "claimed_worker",
        "kind": "research",
        "job_id": "job-r1",
        "claim_id": "claim-a",
        "worker_id": "worker-a",
        "attempt_id": "attempt-a",
        "depends_on_job_ids": ["job-r1"],
        "paper_path": "papers/inference/test.md",
    }


def put(root: Path, envelope: dict) -> None:
    inbox = root / ft.FALLBACK_INBOX
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / f"{envelope['id']}.json").write_text(
        ft.canonical_text(envelope), encoding="utf-8"
    )


class FallbackImmutableReplayTests(unittest.TestCase):
    def assert_descriptor(self, root: Path) -> dict:
        path = root / ".survey/work-queue/submissions/research/attempt-a.json"
        self.assertTrue(path.is_file())
        descriptor = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(descriptor["transport_version"], 10)
        self.assertEqual(descriptor["kind"], "research")
        self.assertEqual(descriptor["job_id"], "job-r1")
        self.assertEqual(descriptor["claim_id"], "claim-a")
        self.assertEqual(descriptor["attempt_id"], "attempt-a")
        self.assertEqual(descriptor["paper_path"], "papers/inference/test.md")
        self.assertEqual(len(descriptor["record_slots"]), len(SLOT_NAMES))
        self.assertTrue(all(ref.get("blob_sha") for ref in descriptor["record_slots"]))
        return descriptor

    def test_legacy_chat_bundle_is_converted_to_immutable_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root)
            envelope = root_fields()
            envelope["writes"] = slot_writes() + [
                {
                    "path": LEGACY_CHAT_INBOX,
                    "content": json.dumps(
                        {
                            "schema_version": 1,
                            "transport_version": 10,
                            "job_id": "job-r1",
                            "claim_id": "claim-a",
                            "worker_id": "worker-a",
                            "attempt_id": "attempt-a",
                            "kind": "research",
                            "depends_on_job_ids": ["job-r1"],
                            "paper_path": "papers/inference/test.md",
                            "record_bank": "a",
                        },
                        ensure_ascii=False,
                    ),
                }
            ]
            put(root, envelope)

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "dispatched")
            self.assertFalse((root / LEGACY_CHAT_INBOX).exists())
            self.assert_descriptor(root)
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").is_file())

    def test_current_bundle_needs_no_chat_inbox_to_replay(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root)
            envelope = root_fields()
            envelope["writes"] = slot_writes()
            put(root, envelope)

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "dispatched")
            self.assertFalse((root / LEGACY_CHAT_INBOX).exists())
            self.assert_descriptor(root)
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").is_file())

    def test_connector_safe_bundle_materializes_slots_then_reenters_quality_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root)
            envelope = root_fields()
            envelope.update({
                "record_bundle_mode": "quality_preflight_v1",
                "run_key": "worker-a-20260925T060000Z-test",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": "2026-09-24T21:00:00+00:00",
                "requested_at": "2026-09-24T21:05:00+00:00",
                "self_review": {
                    "primary_source_read_to_end": True,
                    "no_unverified_inference": True,
                    "summary_and_list_summary_specific": True,
                    "headline_result_grounded": True,
                    "method_end_to_end_explained": True,
                    "evaluation_conditions_and_baselines_explicit": True,
                    "results_conditions_and_interpretation_explicit": True,
                    "limitations_and_positioning_specific": True,
                },
            })
            envelope["writes"] = slot_writes()
            put(root, envelope)

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "dispatched")
            self.assertEqual(result["record_bank"], "a")
            self.assertIn("preflight_request", result)
            self.assertNotIn("descriptor", result)
            self.assertFalse(
                (root / ".survey/work-queue/submissions/research/attempt-a.json").exists()
            )

            request_path = root / result["preflight_request"]
            self.assertTrue(request_path.is_file())
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["operation"], "research_quality_preflight")
            self.assertEqual(request["attempt_id"], "attempt-a")
            self.assertEqual(request["job_id"], "job-r1")
            self.assertEqual(request["record_bank"], "a")
            self.assertEqual(request["worker_id"], "worker-a")
            self.assertEqual(request["run_key"], envelope["run_key"])
            self.assertEqual(request["scheduled_slot"], "adhoc")
            self.assertTrue(all(request["self_review"].values()))
            self.assertTrue((root / ft.FALLBACK_ARCHIVE / "env-a.json").is_file())

    def test_offline_record_waits_for_canonical_job_instead_of_quarantine(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            envelope = root_fields()
            envelope["origin"] = "offline_worker"
            envelope.pop("claim_id")
            envelope.pop("worker_id")
            envelope["writes"] = slot_writes()
            put(root, envelope)

            result = dispatch_fallback_inbox.dispatch(root)

            self.assertEqual(result["action"], "idle")
            self.assertTrue((root / ft.FALLBACK_INBOX / "env-a.json").is_file())
            self.assertFalse((root / ft.FALLBACK_FAILED / "env-a.json").exists())
            self.assertTrue(result["deferred"])
            self.assertIn("canonical", result["deferred"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
