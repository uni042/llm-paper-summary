from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import library_ack_manifest as ack  # noqa: E402


class LibraryAckRetryResultPathTests(unittest.TestCase):
    def _write_json(self, root: Path, rel: str, payload: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_superseded_uses_result_sibling_of_retry_suffixed_canonical_submission(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-research-smoothagent"
            source_attempt = "attempt-old-library"
            canonical_attempt = "attempt-new"
            envelope_id = "env-old-library"
            paper_path = "papers/inference/11-llm-serving-scheduling-disaggregation/paper.md"
            canonical_submission = (
                ".survey/work-queue/submissions/research/attempt-new-retry2.json"
            )

            self._write_json(
                root,
                f".survey/work-queue/fallback-archive/{envelope_id}.json",
                {
                    "schema_version": 1,
                    "id": envelope_id,
                    "kind": "research",
                    "job_id": job_id,
                    "attempt_id": source_attempt,
                    "paper_path": paper_path,
                },
            )
            self._write_json(
                root,
                canonical_submission,
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "status": "completed",
                    "job_id": job_id,
                    "attempt_id": canonical_attempt,
                    "paper_path": paper_path,
                },
            )
            # The base result is an earlier failed processing of the same attempt identity.
            self._write_json(
                root,
                ".survey/work-queue/results/research/attempt-new.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "ok": False,
                    "job_id": job_id,
                    "attempt_id": canonical_attempt,
                    "job_status": None,
                    "artifact": None,
                    "submission": ".survey/work-queue/submissions/research/attempt-new.json",
                },
            )
            self._write_json(
                root,
                ".survey/work-queue/results/research/attempt-new-retry2.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "ok": True,
                    "job_id": job_id,
                    "attempt_id": canonical_attempt,
                    "job_status": "completed",
                    "artifact": {"paper": paper_path},
                    "submission": canonical_submission,
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
                    "artifact_submission": canonical_submission,
                },
            )
            paper = root / paper_path
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("# published\n", encoding="utf-8")

            manifest = ack.build_manifest(root)

            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"], [])
            self.assertEqual(len(manifest["superseded"]), 1)
            row = manifest["superseded"][0]
            self.assertEqual(row["envelope_id"], envelope_id)
            self.assertEqual(row["canonical_attempt_id"], canonical_attempt)
            self.assertEqual(row["canonical_submission_path"], canonical_submission)
            self.assertEqual(
                row["canonical_result_path"],
                ".survey/work-queue/results/research/attempt-new-retry2.json",
            )


if __name__ == "__main__":
    unittest.main()
