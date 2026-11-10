from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import library_ack_manifest as ack  # noqa: E402


class LibraryAckReboundTests(unittest.TestCase):
    def _write(self, root: Path, rel: str, value: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_failed_source_attempt_is_acknowledged_when_canonical_success_proves_rebound_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-research-a"
            old_attempt = "attempt-old"
            new_attempt = "attempt-new"
            envelope_id = "env-a"
            paper = "papers/inference/99-other-inference-systems/paper-a.md"
            old_submission = f".survey/work-queue/submissions/research/{old_attempt}.json"
            new_submission = f".survey/work-queue/submissions/research/{new_attempt}.json"

            self._write(root, f".survey/work-queue/fallback-archive/{envelope_id}.json", {
                "schema_version": 1,
                "id": envelope_id,
                "kind": "research",
                "job_id": job_id,
                "attempt_id": old_attempt,
                "paper_path": paper,
            })
            self._write(root, old_submission, {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "job_id": job_id,
                "attempt_id": old_attempt,
                "paper_path": paper,
            })
            self._write(root, f".survey/work-queue/results/research/{old_attempt}.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "job_id": job_id,
                "attempt_id": old_attempt,
                "submission": old_submission,
                "error": "ValueError: stale attempt: current claim differs",
            })
            self._write(root, new_submission, {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "job_id": job_id,
                "attempt_id": new_attempt,
                "paper_path": paper,
                "source_fallback_envelope_id": envelope_id,
                "source_attempt_id": old_attempt,
            })
            self._write(root, f".survey/work-queue/results/research/{new_attempt}.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": True,
                "job_id": job_id,
                "attempt_id": new_attempt,
                "job_type": "research",
                "job_status": "completed",
                "artifact": {"paper": paper},
                "submission": new_submission,
            })
            self._write(root, f".survey/work-queue/jobs/{job_id}.json", {
                "job_id": job_id,
                "type": "research",
                "status": "completed",
                "paper_path": paper,
                "artifact_submission": new_submission,
            })
            paper_path = root / paper
            paper_path.parent.mkdir(parents=True, exist_ok=True)
            paper_path.write_text("# published\n", encoding="utf-8")

            manifest = ack.build_manifest(root)

            self.assertEqual(len(manifest["acknowledgements"]), 1)
            row = manifest["acknowledgements"][0]
            self.assertEqual(row["envelope_id"], envelope_id)
            self.assertEqual(row["attempt_id"], old_attempt)
            self.assertEqual(row["published_attempt_id"], new_attempt)
            self.assertEqual(row["status"], "reflected")
            self.assertEqual(manifest["waiting"], [])


if __name__ == "__main__":
    unittest.main()
