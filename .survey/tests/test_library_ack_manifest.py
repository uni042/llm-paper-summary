from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import library_ack_manifest as ack  # noqa: E402


class LibraryAckManifestTests(unittest.TestCase):
    def _write_json(self, root: Path, rel: str, payload: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _seed_research(
        self,
        root: Path,
        *,
        envelope_id: str = "env-a",
        job_status: str = "completed",
        result_ok: bool = True,
        paper_exists: bool = True,
    ) -> None:
        job_id = "job-research-a"
        attempt_id = "attempt-a"
        paper_path = "papers/inference/99-other-inference-systems/paper-a.md"
        submission = f".survey/work-queue/submissions/research/{attempt_id}.json"

        self._write_json(
            root,
            f".survey/work-queue/fallback-archive/{envelope_id}.json",
            {
                "schema_version": 1,
                "id": envelope_id,
                "kind": "research",
                "job_id": job_id,
                "attempt_id": attempt_id,
                "paper_path": paper_path,
            },
        )
        self._write_json(
            root,
            submission,
            {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "job_id": job_id,
                "attempt_id": attempt_id,
                "paper_path": paper_path,
            },
        )
        self._write_json(
            root,
            f".survey/work-queue/results/research/{attempt_id}.json",
            {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": result_ok,
                "job_id": job_id,
                "attempt_id": attempt_id,
                "job_type": "research",
                "job_status": job_status if result_ok else None,
                "artifact": {"paper": paper_path} if result_ok else None,
                "submission": submission,
            },
        )
        self._write_json(
            root,
            f".survey/work-queue/jobs/{job_id}.json",
            {
                "job_id": job_id,
                "type": "research",
                "status": job_status,
                "paper_path": paper_path,
                "artifact_submission": submission if job_status == "completed" else None,
            },
        )
        if paper_exists:
            paper = root / paper_path
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("# paper\n", encoding="utf-8")

    def test_acknowledges_only_exact_successful_published_research_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_research(root)

            manifest = ack.build_manifest(root)

            self.assertEqual(len(manifest["acknowledgements"]), 1)
            row = manifest["acknowledgements"][0]
            self.assertEqual(row["envelope_id"], "env-a")
            self.assertEqual(row["job_id"], "job-research-a")
            self.assertEqual(row["attempt_id"], "attempt-a")
            self.assertEqual(row["status"], "reflected")
            self.assertEqual(row["pending_path"], "/LLM-survey-outbox/pending/env-a.json")
            self.assertEqual(row["processed_path"], "/LLM-survey-outbox/processed/env-a.json")

    def test_does_not_acknowledge_ready_job_even_with_success_result(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_research(root, job_status="ready")
            manifest = ack.build_manifest(root)
            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"][0]["reason"], "job_not_terminal")

    def test_does_not_acknowledge_failed_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_research(root, result_ok=False)
            manifest = ack.build_manifest(root)
            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"][0]["reason"], "result_not_successful")

    def test_does_not_acknowledge_research_when_paper_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_research(root, paper_exists=False)
            manifest = ack.build_manifest(root)
            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"][0]["reason"], "paper_missing")

    def test_write_manifest_is_deterministic_when_state_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_research(root)
            target = root / ".survey/work-queue/library-ack-manifest.json"

            changed_first = ack.write_manifest(root, target)
            first = target.read_text(encoding="utf-8")
            changed_second = ack.write_manifest(root, target)
            second = target.read_text(encoding="utf-8")

            self.assertTrue(changed_first)
            self.assertFalse(changed_second)
            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
