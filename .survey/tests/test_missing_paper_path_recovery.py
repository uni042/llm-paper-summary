from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import immutable_submission  # noqa: E402
import replay_record_fallback as record_replay  # noqa: E402
from paper_path_resolver import resolve_paper_path  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402

EXPECTED = (
    "papers/inference/99-other-inference-systems/"
    "2026-2609.04875-forgetting-without-restarting-execution-state-unlearning-for-stateful-llm-agents.md"
)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def missing_path_job(job_id: str = "job-r1") -> dict:
    return {
        "job_id": job_id,
        "type": "research",
        "status": "ready",
        "canonical_id": "arXiv:2609.04875",
        "title": "Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents",
        "source_url": "https://arxiv.org/abs/2609.04875",
        "paper_path": None,
        "depends_on_job_ids": [job_id],
    }


class MissingPaperPathRecoveryTests(unittest.TestCase):
    def test_resolver_builds_deterministic_fallback(self) -> None:
        self.assertEqual(resolve_paper_path(missing_path_job()), EXPECTED)

    def test_immutable_descriptor_recovers_path_from_canonical_job(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job = missing_path_job()
            write_json(root / ".survey/work-queue/jobs/job-r1.json", job)

            refs = []
            bank_root = BANK_ROOTS["a"]
            for slot in SLOT_NAMES:
                path = root / bank_root / f"{slot}.json"
                payload = {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "job_id": "job-r1",
                    "attempt_id": "attempt-a",
                    "data": {},
                }
                text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                refs.append(
                    {
                        "slot": slot,
                        "path": f"{bank_root}/{slot}.json",
                        "blob_sha": immutable_submission.git_blob_sha(text.encode("utf-8")),
                    }
                )

            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-r1",
                "record_bank": "a",
                "paper_path": None,
                "record_slots": refs,
            }
            normalized = immutable_submission.validate_descriptor(root, descriptor)
            self.assertEqual(normalized["paper_path"], EXPECTED)

    def test_library_replay_recovers_path_when_job_and_envelope_are_missing_it(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(root / ".survey/work-queue/jobs/job-r1.json", missing_path_job())
            write_json(
                root / ".survey/work-queue/claims/job-r1.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "job_id": "job-r1",
                    "claim_id": "claim-a",
                    "worker_id": "worker-a",
                    "attempt_id": "attempt-a",
                    "claimed_at": "2026-09-14T00:00:00+00:00",
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
                            "job_id": "unused-bank-placeholder",
                            "data": {},
                        },
                    )

            writes = []
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
            envelope = {
                "schema_version": 1,
                "id": "env-r1",
                "origin": "claimed_worker",
                "kind": "research",
                "job_id": "job-r1",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "attempt_id": "attempt-a",
                "depends_on_job_ids": ["job-r1"],
                "writes": writes,
            }

            result = record_replay.materialize(root, envelope)
            self.assertEqual(result["action"], "materialized")
            descriptor = json.loads(
                (root / ".survey/work-queue/submissions/research/attempt-a.json").read_text(encoding="utf-8")
            )
            self.assertEqual(descriptor["paper_path"], EXPECTED)
            persisted_job = json.loads((root / ".survey/work-queue/jobs/job-r1.json").read_text(encoding="utf-8"))
            self.assertEqual(persisted_job["paper_path"], EXPECTED)


if __name__ == "__main__":
    unittest.main()
