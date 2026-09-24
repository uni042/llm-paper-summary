from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class DiscoveryIdentityDedupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.originals = {
            name: getattr(queue_worker, name)
            for name in ("ROOT", "QUEUE", "JOBS", "SUBMISSIONS", "RESULTS", "STATE", "ARCHIVE", "DISCOVERY_STATE")
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
        queue_worker.JOBS.mkdir(parents=True)

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            setattr(queue_worker, name, value)
        self.tmp.cleanup()

    def _write_existing_paper(self) -> None:
        paper = self.repo_root / "papers" / "inference" / "kv-cache" / "existing.md"
        paper.parent.mkdir(parents=True)
        paper.write_text(
            """---
canonical_id: arXiv:2605.12345
arxiv_id: 2605.12345
doi: 10.1234/example
title: "Fast KV Cache: A Practical System"
summary: Existing paper used for identity-dedup regression coverage.
---
# Fast KV Cache: A Practical System
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
                        "arXiv:2605.12345": {
                            "path": "papers/inference/kv-cache/existing.md",
                            "identifiers": ["arXiv:2605.12345", "DOI:10.1234/example"],
                        }
                    },
                    "identifier_to_canonical": {
                        "arXiv:2605.12345": "arXiv:2605.12345",
                        "DOI:10.1234/example": "arXiv:2605.12345",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def test_process_discovery_uses_normalized_identity_before_materializing_research(self) -> None:
        self._write_existing_paper()
        sub = {
            "candidates": [
                {
                    "source_url": "https://arxiv.org/pdf/2605.12345v2.pdf",
                    "title": "Fast KV Cache: A Practical System",
                    "priority": 80,
                },
                {
                    "source_url": "https://doi.org/10.1234/example",
                    "title": "DOI-form duplicate",
                    "priority": 79,
                },
                {
                    "title": "Fast KV Cache - A Practical System",
                    "priority": 78,
                },
                {
                    "canonical_id": "arXiv:2609.99999",
                    "source_url": "https://arxiv.org/abs/2609.99999",
                    "title": "Actually New Paper",
                    "priority": 77,
                },
            ]
        }
        job = {"job_id": "job-discovery-test", "status": "processing"}
        state = {
            "stats": {
                "discovered": 0,
                "selected": 0,
                "research_completed": 0,
                "audit_completed": 0,
                "rejected": 0,
            }
        }

        queue_worker.process_discovery(sub, job, state)

        research_jobs = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in queue_worker.JOBS.glob("*.json")
        ]
        self.assertEqual(job["result_summary"]["research_jobs_added"], 1)
        self.assertEqual(len(research_jobs), 1)
        self.assertEqual(research_jobs[0]["canonical_id"], "arXiv:2609.99999")

    def test_same_candidate_with_versioned_id_and_url_materializes_only_once(self) -> None:
        sub = {
            "candidates": [
                {
                    "canonical_id": "arXiv:2609.88888v2",
                    "source_url": "https://arxiv.org/pdf/2609.88888v2.pdf",
                    "title": "One Paper",
                    "priority": 80,
                },
                {
                    "source_url": "https://arxiv.org/abs/2609.88888",
                    "title": "One Paper",
                    "priority": 79,
                },
            ]
        }
        job = {"job_id": "job-discovery-test", "status": "processing"}
        state = {
            "stats": {
                "discovered": 0,
                "selected": 0,
                "research_completed": 0,
                "audit_completed": 0,
                "rejected": 0,
            }
        }

        queue_worker.process_discovery(sub, job, state)

        research_jobs = list(queue_worker.JOBS.glob("*.json"))
        self.assertEqual(job["result_summary"]["research_jobs_added"], 1)
        self.assertEqual(len(research_jobs), 1)


if __name__ == "__main__":
    unittest.main()
