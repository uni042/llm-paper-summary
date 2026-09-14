from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import retry_adopted_checkpoint_submissions as retry  # noqa: E402


class RetryAdoptedCheckpointSubmissionsTests(unittest.TestCase):
    def _write(self, root: Path, rel: str, value: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _seed(self, root: Path, *, checkpoint_name: str = "env-a.json") -> Path:
        job_id = "job-research-a"
        old_attempt = "attempt-old"
        descriptor = self._write(
            root,
            f".survey/work-queue/submissions/research/{old_attempt}.json",
            {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": old_attempt,
                "job_id": job_id,
                "claim_id": "claim-old",
                "worker_id": "worker-old",
            },
        )
        self._write(
            root,
            f".survey/work-queue/results/research/{old_attempt}.json",
            {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "attempt_id": old_attempt,
                "job_id": job_id,
                "job_type": "research",
                "job_status": None,
                "artifact": None,
                "submission": f".survey/work-queue/submissions/research/{old_attempt}.json",
                "error": "ValueError: stale attempt: current claim uses attempt-new, descriptor uses attempt-old",
            },
        )
        self._write(
            root,
            f".survey/work-queue/jobs/{job_id}.json",
            {"job_id": job_id, "type": "research", "status": "ready"},
        )
        self._write(
            root,
            f".survey/work-queue/claims/{job_id}.json",
            {
                "job_id": job_id,
                "claim_id": "claim-new",
                "worker_id": "worker-new",
                "worker_kind": "scheduled_chat",
                "attempt_id": "attempt-new",
                "released_at": "2026-09-14T21:32:05+00:00",
                "checkpoint_ref": f"/LLM-survey-outbox/pending/{checkpoint_name}",
            },
        )
        slot = {
            "schema_version": 1,
            "transport_version": 10,
            "attempt_id": old_attempt,
            "job_id": job_id,
            "slot": "metadata",
            "reservation": {
                "claim_id": "claim-old",
                "worker_id": "worker-old",
                "attempt_id": old_attempt,
            },
            "data": {"canonical_id": "arXiv:2600.00001"},
        }
        self._write(
            root,
            ".survey/work-queue/fallback-archive/env-a.json",
            {
                "schema_version": 1,
                "id": "env-a",
                "origin": "claimed_worker",
                "kind": "research",
                "job_id": job_id,
                "attempt_id": old_attempt,
                "claim_id": "claim-old",
                "worker_id": "worker-old",
                "writes": [
                    {
                        "path": ".survey/work-queue/records/chat-record/metadata.json",
                        "content": json.dumps(slot, ensure_ascii=False),
                    }
                ],
            },
        )
        return descriptor

    def test_selects_failed_stale_attempt_when_new_claim_adopted_exact_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            descriptor = self._seed(root)

            selected = retry.eligible_adoptions(root)

            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0]["source_descriptor"], descriptor)
            self.assertEqual(selected[0]["source_attempt_id"], "attempt-old")
            self.assertEqual(selected[0]["claim"]["attempt_id"], "attempt-new")

    def test_does_not_select_when_checkpoint_ref_does_not_match_archive(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed(root, checkpoint_name="different.json")

            self.assertEqual(retry.eligible_adoptions(root), [])

    def test_rebind_changes_transport_identity_but_preserves_record_data(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed(root)
            envelope = json.loads(
                (root / ".survey/work-queue/fallback-archive/env-a.json").read_text(encoding="utf-8")
            )
            claim = json.loads(
                (root / ".survey/work-queue/claims/job-research-a.json").read_text(encoding="utf-8")
            )

            rebound = retry.rebind_envelope(envelope, claim)
            payload = json.loads(rebound["writes"][0]["content"])

            self.assertEqual(rebound["attempt_id"], "attempt-new")
            self.assertEqual(rebound["claim_id"], "claim-new")
            self.assertEqual(rebound["worker_id"], "worker-new")
            self.assertEqual(payload["attempt_id"], "attempt-new")
            self.assertEqual(payload["job_id"], "job-research-a")
            self.assertEqual(payload["reservation"]["claim_id"], "claim-new")
            self.assertEqual(payload["reservation"]["worker_id"], "worker-new")
            self.assertEqual(payload["data"], {"canonical_id": "arXiv:2600.00001"})


if __name__ == "__main__":
    unittest.main()
