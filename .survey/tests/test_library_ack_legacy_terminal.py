from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import library_ack_manifest as ack  # noqa: E402


class LibraryAckLegacyTerminalTests(unittest.TestCase):
    def _write_json(self, root: Path, rel: str, payload: dict) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _archive(self, root: Path, canonical_id: str = "arXiv:2512.14946") -> None:
        metadata = {
            "schema_version": 1,
            "transport_version": 10,
            "slot": "metadata",
            "attempt_id": "attempt-old",
            "job_id": "job-legacy",
            "data": {"canonical_id": canonical_id},
        }
        self._write_json(
            root,
            ".survey/work-queue/fallback-archive/env-old.json",
            {
                "schema_version": 1,
                "id": "env-old",
                "kind": "research",
                "job_id": "job-legacy",
                "attempt_id": "attempt-old",
                "writes": [
                    {
                        "path": ".survey/work-queue/records/chat-record/metadata.json",
                        "content": json.dumps(metadata, ensure_ascii=False) + "\n",
                    }
                ],
            },
        )

    def _job_and_paper(self, root: Path, paper_canonical_id: str = "arXiv:2512.14946") -> None:
        paper_path = "papers/inference/10-kv-cache-offload-recomputation/legacy.md"
        self._write_json(
            root,
            ".survey/work-queue/jobs/job-legacy.json",
            {
                "job_id": "job-legacy",
                "type": "research",
                "status": "completed",
                "canonical_id": "arXiv:2512.14946",
                "paper_path": paper_path,
                "artifact_submission": "work-queue/submissions/chat-inbox.json",
                "completed_at": "2026-09-13T13:32:57+00:00",
            },
        )
        paper = root / paper_path
        paper.parent.mkdir(parents=True, exist_ok=True)
        paper.write_text(
            "---\n"
            f"canonical_id: {paper_canonical_id}\n"
            "title: Legacy terminal paper\n"
            "---\n\n# Legacy terminal paper\n",
            encoding="utf-8",
        )

    def test_completed_legacy_chat_inbox_job_supersedes_unattributed_old_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._archive(root)
            self._job_and_paper(root)

            manifest = ack.build_manifest(root)

            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"], [])
            self.assertEqual(len(manifest["superseded"]), 1)
            row = manifest["superseded"][0]
            self.assertEqual(row["envelope_id"], "env-old")
            self.assertEqual(row["job_id"], "job-legacy")
            self.assertEqual(row["reason"], "legacy_terminal_job_without_immutable_attempt")
            self.assertEqual(row["paper_path"], "papers/inference/10-kv-cache-offload-recomputation/legacy.md")
            self.assertTrue(row["legacy_terminal_evidence"])
            self.assertNotIn("canonical_attempt_id", row)

    def test_legacy_terminal_rule_rejects_canonical_id_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._archive(root)
            self._job_and_paper(root, paper_canonical_id="arXiv:9999.99999")

            manifest = ack.build_manifest(root)

            self.assertEqual(manifest["superseded"], [])
            self.assertEqual(len(manifest["waiting"]), 1)
            self.assertEqual(manifest["waiting"][0]["reason"], "descriptor_missing")


if __name__ == "__main__":
    unittest.main()
