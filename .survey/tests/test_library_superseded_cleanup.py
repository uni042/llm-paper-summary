from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import library_ack_manifest as ack  # noqa: E402


class LibrarySupersededCleanupTests(unittest.TestCase):
    def _write_json(self, root: Path, rel: str, payload: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_failed_fallback_is_superseded_after_same_job_publishes_via_new_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-research-a"
            old_attempt = "attempt-old"
            new_attempt = "attempt-new"
            envelope_id = "env-old"
            paper_path = "papers/inference/99-other-inference-systems/paper-a.md"
            old_submission = f".survey/work-queue/submissions/research/{old_attempt}.json"
            new_submission = f".survey/work-queue/submissions/research/{new_attempt}.json"

            self._write_json(
                root,
                f".survey/work-queue/fallback-archive/{envelope_id}.json",
                {
                    "schema_version": 1,
                    "id": envelope_id,
                    "kind": "research",
                    "job_id": job_id,
                    "attempt_id": old_attempt,
                    "paper_path": paper_path,
                },
            )
            self._write_json(
                root,
                old_submission,
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "job_id": job_id,
                    "attempt_id": old_attempt,
                    "paper_path": paper_path,
                },
            )
            self._write_json(
                root,
                f".survey/work-queue/results/research/{old_attempt}.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "ok": False,
                    "job_id": job_id,
                    "attempt_id": old_attempt,
                    "job_type": "research",
                    "job_status": None,
                    "artifact": None,
                    "submission": old_submission,
                    "error": "ValueError: stale attempt",
                },
            )
            self._write_json(
                root,
                new_submission,
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "job_id": job_id,
                    "attempt_id": new_attempt,
                    "paper_path": paper_path,
                },
            )
            self._write_json(
                root,
                f".survey/work-queue/results/research/{new_attempt}.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "ok": True,
                    "job_id": job_id,
                    "attempt_id": new_attempt,
                    "job_type": "research",
                    "job_status": "completed",
                    "artifact": {"paper": paper_path},
                    "submission": new_submission,
                },
            )
            self._write_json(
                root,
                f".survey/work-queue/jobs/{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "research",
                    "status": "completed",
                    "paper_path": paper_path,
                    "artifact_submission": new_submission,
                },
            )
            paper = root / paper_path
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("# published paper\n", encoding="utf-8")

            manifest = ack.build_manifest(root)

            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"], [])
            self.assertEqual(len(manifest["superseded"]), 1)
            row = manifest["superseded"][0]
            self.assertEqual(row["envelope_id"], envelope_id)
            self.assertEqual(row["attempt_id"], old_attempt)
            self.assertEqual(row["canonical_attempt_id"], new_attempt)
            self.assertEqual(row["status"], "superseded")
            self.assertEqual(row["pending_path"], f"/LLM-survey-outbox/pending/{envelope_id}.json")
            self.assertEqual(row["superseded_path"], f"/LLM-survey-outbox/superseded/{envelope_id}.json")

    def test_failed_fallback_stays_waiting_while_job_is_not_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_json(
                root,
                ".survey/work-queue/fallback-archive/env-old.json",
                {
                    "schema_version": 1,
                    "id": "env-old",
                    "kind": "research",
                    "job_id": "job-research-a",
                    "attempt_id": "attempt-old",
                    "paper_path": "papers/inference/99-other-inference-systems/paper-a.md",
                },
            )
            self._write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-old.json",
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "job_id": "job-research-a",
                    "attempt_id": "attempt-old",
                    "paper_path": "papers/inference/99-other-inference-systems/paper-a.md",
                },
            )
            self._write_json(
                root,
                ".survey/work-queue/results/research/attempt-old.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "ok": False,
                    "job_id": "job-research-a",
                    "attempt_id": "attempt-old",
                    "job_type": "research",
                    "job_status": None,
                    "artifact": None,
                    "submission": ".survey/work-queue/submissions/research/attempt-old.json",
                },
            )
            self._write_json(
                root,
                ".survey/work-queue/jobs/job-research-a.json",
                {
                    "job_id": "job-research-a",
                    "type": "research",
                    "status": "ready",
                    "paper_path": "papers/inference/99-other-inference-systems/paper-a.md",
                },
            )

            manifest = ack.build_manifest(root)

            self.assertEqual(manifest.get("superseded", []), [])
            self.assertEqual(manifest["waiting"][0]["reason"], "result_not_successful")


if __name__ == "__main__":
    unittest.main()
