from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import normalize_research_paper_paths as normalizer  # noqa: E402


EXPECTED = (
    "papers/inference/99-other-inference-systems/"
    "2026-2609.04875-forgetting-without-restarting-execution-state-unlearning-for-stateful-llm-agents.md"
)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class NormalizeResearchPaperPathsTests(unittest.TestCase):
    def test_apply_fills_missing_research_path_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs = root / ".survey/work-queue/jobs"
            missing = jobs / "job-r1.json"
            explicit = jobs / "job-r2.json"
            non_research = jobs / "job-d1.json"

            write_json(
                missing,
                {
                    "job_id": "job-r1",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.04875",
                    "title": "Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents",
                    "source_url": "https://arxiv.org/abs/2609.04875",
                    "paper_path": None,
                },
            )
            write_json(
                explicit,
                {
                    "job_id": "job-r2",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2609.00001",
                    "title": "Already Classified",
                    "paper_path": "papers/inference/01-kv-cache/2026-existing.md",
                },
            )
            write_json(
                non_research,
                {
                    "job_id": "job-d1",
                    "type": "discovery",
                    "status": "ready",
                    "paper_path": None,
                },
            )

            first = normalizer.normalize(root, apply=True)
            self.assertEqual(first["updated"], 1)
            self.assertEqual(first["unresolved"], 0)
            self.assertEqual(json.loads(missing.read_text(encoding="utf-8"))["paper_path"], EXPECTED)
            self.assertEqual(
                json.loads(explicit.read_text(encoding="utf-8"))["paper_path"],
                "papers/inference/01-kv-cache/2026-existing.md",
            )
            self.assertIsNone(json.loads(non_research.read_text(encoding="utf-8"))["paper_path"])

            second = normalizer.normalize(root, apply=True)
            self.assertEqual(second["updated"], 0)
            self.assertEqual(second["unresolved"], 0)

    def test_missing_identity_is_reported_without_fabricating_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job = root / ".survey/work-queue/jobs/job-r1.json"
            write_json(
                job,
                {
                    "job_id": "job-r1",
                    "type": "research",
                    "status": "ready",
                    "paper_path": None,
                },
            )

            result = normalizer.normalize(root, apply=True)
            self.assertEqual(result["updated"], 0)
            self.assertEqual(result["unresolved"], 1)
            self.assertIsNone(json.loads(job.read_text(encoding="utf-8"))["paper_path"])


if __name__ == "__main__":
    unittest.main()
