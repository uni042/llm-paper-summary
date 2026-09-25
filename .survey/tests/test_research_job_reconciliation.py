from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey/scripts"
sys.path.insert(0, str(SCRIPTS))

import build_worker_worklist  # noqa: E402
import refresh_queue_snapshot  # noqa: E402
import research_job_reconciliation  # noqa: E402


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_paper(repo: Path, canonical_id: str = "arXiv:2609.99991") -> str:
    path = (
        repo
        / "papers/inference/99-other-inference-systems"
        / "2026-2609.99991-represented-paper.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
canonical_id: "arXiv:2609.99991"
arxiv_id: "2609.99991"
title: "Represented Paper"
lineage: "99-other-inference-systems"
source: "https://arxiv.org/abs/2609.99991"
---

# Represented Paper

本文。
""",
        encoding="utf-8",
    )
    return path.relative_to(repo).as_posix()


class ResearchJobReconciliationTests(unittest.TestCase):
    def test_ready_research_job_is_superseded_without_fake_completion(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            represented_path = _write_paper(repo)
            job_path = repo / ".survey/work-queue/jobs/job-research-stale.json"
            _write_json(
                job_path,
                {
                    "job_id": "job-research-stale",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.99991",
                    "paper_path": represented_path,
                    "title": "Represented Paper",
                },
            )
            audit_path = repo / ".survey/work-queue/jobs/job-audit-still-needed.json"
            _write_json(
                audit_path,
                {
                    "job_id": "job-audit-still-needed",
                    "type": "audit",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.99991",
                    "paper_path": represented_path,
                },
            )

            result = research_job_reconciliation.reconcile(
                repo,
                timestamp="2026-09-26T00:00:00+00:00",
            )

            self.assertEqual(result["changed"], 1)
            research = json.loads(job_path.read_text(encoding="utf-8"))
            self.assertEqual(research["status"], "superseded")
            self.assertEqual(
                research["superseded_reason"], "paper_already_represented"
            )
            self.assertEqual(research["represented_paper_path"], represented_path)
            self.assertNotIn("completed_at", research)
            self.assertNotIn("result", research)

            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            self.assertEqual(audit["status"], "ready")

    def test_snapshot_and_worklist_defensively_hide_stale_ready_job(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            represented_path = _write_paper(repo)
            _write_json(
                repo / ".survey/work-queue/jobs/job-research-stale.json",
                {
                    "job_id": "job-research-stale",
                    "type": "research",
                    "status": "ready",
                    "priority": 99,
                    "canonical_id": "arXiv:2609.99991",
                    "paper_path": represented_path,
                    "title": "Represented Paper",
                    "source_url": "https://arxiv.org/abs/2609.99991",
                },
            )
            _write_json(
                repo / ".survey/work-queue/jobs/job-research-fresh.json",
                {
                    "job_id": "job-research-fresh",
                    "type": "research",
                    "status": "ready",
                    "priority": 98,
                    "canonical_id": "arXiv:2609.99992",
                    "paper_path": (
                        "papers/inference/99-other-inference-systems/"
                        "2026-2609.99992-fresh.md"
                    ),
                    "title": "Fresh Paper",
                    "source_url": "https://arxiv.org/abs/2609.99992",
                },
            )

            snapshot = refresh_queue_snapshot.build_snapshot(repo)
            self.assertEqual(snapshot["counts"]["research"]["ready"], 1)
            self.assertEqual(snapshot["counts"]["research"]["superseded"], 1)
            self.assertEqual(
                [row["job_id"] for row in snapshot["next_jobs"]],
                ["job-research-fresh"],
            )

            payloads = build_worker_worklist.build(repo, limit=100)
            rows = (
                payloads["00"]["research_audit"]["rows"]
                + payloads["30"]["research_audit"]["rows"]
            )
            self.assertEqual(
                [row["job_id"] for row in rows],
                ["job-research-fresh"],
            )
            self.assertEqual(payloads["00"]["research_audit"]["ready_total"], 1)
            self.assertEqual(payloads["30"]["research_audit"]["ready_total"], 1)

    def test_reconcile_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            represented_path = _write_paper(repo)
            _write_json(
                repo / ".survey/work-queue/jobs/job-research-stale.json",
                {
                    "job_id": "job-research-stale",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.99991",
                    "paper_path": represented_path,
                },
            )

            first = research_job_reconciliation.reconcile(repo)
            second = research_job_reconciliation.reconcile(repo)

            self.assertEqual(first["changed"], 1)
            self.assertEqual(second["changed"], 0)


if __name__ == "__main__":
    unittest.main()
