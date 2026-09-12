from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dispatch_fallback_inbox  # noqa: E402
import record_bank_config  # noqa: E402
import select_record_bank  # noqa: E402


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slot_payload(slot: str, attempt_id: str, job_id: str) -> dict:
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "data": {},
    }


def seed_bank(repo_root: Path, bank: str, attempt_id: str, job_id: str) -> None:
    root = repo_root / record_bank_config.BANK_ROOTS[bank]
    for slot in record_bank_config.SLOT_NAMES:
        write_json(root / f"{slot}.json", slot_payload(slot, attempt_id, job_id))


class RecordBankVisibilityTest(unittest.TestCase):
    def test_hidden_ready_job_keeps_its_bank_occupied(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            write_json(
                repo_root / ".survey/work-queue/next-jobs.json",
                {
                    "counts": {"research": {"ready": 1}},
                    "next_jobs": [],
                },
            )
            write_json(
                repo_root / ".survey/work-queue/jobs/job-hidden.json",
                {
                    "job_id": "job-hidden",
                    "type": "research",
                    "status": "ready",
                    "priority": 10,
                },
            )
            seed_bank(repo_root, "a", "attempt-hidden", "job-hidden")
            seed_bank(repo_root, "b", select_record_bank.PLACEHOLDER_ATTEMPT, "")

            state = select_record_bank.inspect(repo_root)
            by_bank = {row["bank"]: row for row in state["banks"]}

            self.assertEqual(by_bank["a"]["state"], "occupied")
            self.assertEqual(state["selected_bank"], "b")


class FallbackDispatchBankSafetyTest(unittest.TestCase):
    def test_dispatch_remaps_replayed_bundle_away_from_occupied_bank(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            write_json(
                repo_root / ".survey/work-queue/next-jobs.json",
                {
                    "counts": {"research": {"ready": 2}},
                    "next_jobs": [
                        {"job_id": "job-old", "type": "research", "status": "ready"},
                        {"job_id": "job-new", "type": "research", "status": "ready"},
                    ],
                },
            )
            for job_id in ("job-old", "job-new"):
                write_json(
                    repo_root / f".survey/work-queue/jobs/{job_id}.json",
                    {"job_id": job_id, "type": "research", "status": "ready"},
                )

            seed_bank(repo_root, "a", "attempt-old", "job-old")
            seed_bank(repo_root, "b", select_record_bank.PLACEHOLDER_ATTEMPT, "")

            bank_a = record_bank_config.BANK_ROOTS["a"]
            writes = []
            for slot in record_bank_config.SLOT_NAMES:
                payload = slot_payload(slot, "attempt-new", "job-new")
                writes.append(
                    {
                        "path": f"{bank_a}/{slot}.json",
                        "content": json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    }
                )
            writes.append(
                {
                    "path": ".survey/work-queue/submissions/chat-inbox.json",
                    "content": json.dumps(
                        {
                            "schema_version": 1,
                            "transport_version": 10,
                            "job_id": "job-new",
                            "attempt_id": "attempt-new",
                            "record_bank": "a",
                            "record_slots": [],
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                    + "\n",
                }
            )
            envelope = {
                "schema_version": 1,
                "id": "fallback-attempt-new",
                "kind": "research",
                "job_id": "job-new",
                "attempt_id": "attempt-new",
                "depends_on_job_ids": ["job-new"],
                "writes": writes,
            }
            write_json(
                repo_root / ".survey/work-queue/fallback-inbox/fallback-attempt-new.json",
                envelope,
            )

            result = dispatch_fallback_inbox.dispatch(repo_root)

            self.assertEqual(result["action"], "dispatched")
            old_a = json.loads(
                (repo_root / record_bank_config.BANK_ROOTS["a"] / "metadata.json").read_text(encoding="utf-8")
            )
            new_b = json.loads(
                (repo_root / record_bank_config.BANK_ROOTS["b"] / "metadata.json").read_text(encoding="utf-8")
            )
            inbox = json.loads(
                (repo_root / ".survey/work-queue/submissions/chat-inbox.json").read_text(encoding="utf-8")
            )

            self.assertEqual(old_a["job_id"], "job-old")
            self.assertEqual(new_b["job_id"], "job-new")
            self.assertEqual(inbox["record_bank"], "b")


if __name__ == "__main__":
    unittest.main()
