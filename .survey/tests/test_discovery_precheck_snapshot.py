from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class DiscoveryPrecheckSnapshotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.originals = {
            name: getattr(queue_worker, name, None)
            for name in (
                "ROOT",
                "QUEUE",
                "JOBS",
                "SUBMISSIONS",
                "RESULTS",
                "STATE",
                "ARCHIVE",
                "DISCOVERY_STATE",
                "DISCOVERY_IDENTITY_DIR",
            )
        }
        self.tmp = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.tmp.name)
        self.root = self.repo_root / ".survey"
        self.queue = self.root / "work-queue"
        queue_worker.ROOT = self.root
        queue_worker.QUEUE = self.queue
        queue_worker.JOBS = self.queue / "jobs"
        queue_worker.SUBMISSIONS = self.queue / "submissions"
        queue_worker.RESULTS = self.queue / "results"
        queue_worker.STATE = self.queue / "state.json"
        queue_worker.ARCHIVE = self.queue / "archive"
        queue_worker.DISCOVERY_STATE = self.queue / "discovery-state.json"
        queue_worker.DISCOVERY_IDENTITY_DIR = self.queue / "discovery-identities"
        queue_worker.JOBS.mkdir(parents=True)

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            if value is None and hasattr(queue_worker, name):
                delattr(queue_worker, name)
            else:
                setattr(queue_worker, name, value)
        self.tmp.cleanup()

    def _write_existing_identity(self) -> None:
        paper = self.repo_root / "papers" / "inference" / "kv-cache" / "crosspool.md"
        paper.parent.mkdir(parents=True)
        paper.write_text(
            """---
canonical_id: arXiv:2606.24506
arxiv_id: 2606.24506
title: "CrossPool: Efficient Multi-LLM Serving for Cold MoE Models"
summary: Existing paper used for discovery precheck regression coverage.
---
# CrossPool
""",
            encoding="utf-8",
        )
        state = self.root / "survey-state"
        state.mkdir(parents=True)
        (state / "paper-identity-index.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "papers": {
                        "arXiv:2606.24506": {
                            "path": "papers/inference/kv-cache/crosspool.md",
                            "identifiers": ["arXiv:2606.24506"],
                        }
                    },
                    "identifier_to_canonical": {
                        "arXiv:2606.24506": "arXiv:2606.24506",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (queue_worker.JOBS / "job-research-pending.json").write_text(
            json.dumps(
                {
                    "job_id": "job-research-pending",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.11294",
                    "source_url": "https://arxiv.org/abs/2609.11294",
                    "title": "Memory Compression for High-Fanout Agent Sandboxes",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def test_snapshot_exposes_same_existing_ids_as_final_duplicate_guard(self) -> None:
        self._write_existing_identity()

        changed = queue_worker.write_discovery_identity_snapshot()

        self.assertTrue(changed)
        arxiv_2606 = (queue_worker.DISCOVERY_IDENTITY_DIR / "arxiv-2606.txt").read_text(encoding="utf-8")
        arxiv_2609 = (queue_worker.DISCOVERY_IDENTITY_DIR / "arxiv-2609.txt").read_text(encoding="utf-8")
        self.assertIn("id:arXiv:2606.24506\n", arxiv_2606)
        self.assertIn("id:arXiv:2609.11294\n", arxiv_2609)

        manifest = json.loads(
            (queue_worker.DISCOVERY_IDENTITY_DIR / "_manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["source"], "queue_worker.existing_candidate_keys")
        self.assertGreaterEqual(manifest["token_count"], 4)

    def test_discovery_job_requires_snapshot_precheck_instead_of_code_search(self) -> None:
        instructions = queue_worker.DISCOVERY_INSTRUCTIONS

        self.assertIn(".survey/work-queue/discovery-identities/_manifest.json", instructions)
        self.assertIn("same identity tokens as the final duplicate gate", instructions)
        self.assertIn("Do not use GitHub code search as duplicate authority", instructions)


if __name__ == "__main__":
    unittest.main()
