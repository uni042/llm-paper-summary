from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_discovery_precheck  # noqa: E402
import queue_worker  # noqa: E402


class DiscoveryPrecheckProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / "discovery-identities"
        self.snapshot.mkdir(parents=True)
        (self.snapshot / "_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "source": "queue_worker.existing_candidate_keys",
                    "source_commit": "abc123",
                    "code_search_is_authority": False,
                    "shards": {"arxiv-2609.txt": 1},
                }
            ),
            encoding="utf-8",
        )
        (self.snapshot / "arxiv-2609.txt").write_text(
            "id:arXiv:2609.00001\n",
            encoding="utf-8",
        )
        self.ledger = self.root / "discovery-rejections.json"
        self.ledger.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "source": "immutable_discovery_submissions.rejected_candidates",
                    "records": {},
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_processor_only_emits_unseen_records_and_receipt(self) -> None:
        request = self.root / "request.json"
        request.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "req-1",
                    "run_key": "2026-09-20T01:00:00+09:00",
                    "axis": "memory",
                    "records": [
                        {"canonical_id": "arXiv:2609.00001", "title": "Known"},
                        {"canonical_id": "arXiv:2609.99999", "title": "New"},
                    ],
                }
            ),
            encoding="utf-8",
        )

        result = process_discovery_precheck.process_request(
            request,
            snapshot_dir=self.snapshot,
            rejection_ledger_path=self.ledger,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["retrieval_duplicate_filtered_count"], 1)
        self.assertEqual(result["unseen_result_count"], 1)
        self.assertEqual(result["results"][0]["canonical_id"], "arXiv:2609.99999")
        self.assertEqual(result["snapshot_source_commit"], "abc123")
        self.assertTrue(result["receipt"].startswith("sha256:"))
        self.assertIn("id:arXiv:2609.99999", result["allowed_records"][0]["identity_tokens"])


class DiscoveryPrecheckGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.originals = {
            name: getattr(queue_worker, name)
            for name in ("ROOT", "QUEUE", "JOBS", "SUBMISSIONS", "RESULTS", "STATE", "ARCHIVE", "DISCOVERY_STATE")
        }
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.survey = self.repo / ".survey"
        self.queue = self.survey / "work-queue"
        self.results = self.queue / "discovery-precheck" / "results"
        self.results.mkdir(parents=True)
        queue_worker.ROOT = self.survey
        queue_worker.QUEUE = self.queue
        queue_worker.JOBS = self.queue / "jobs"
        queue_worker.SUBMISSIONS = self.queue / "submissions"
        queue_worker.RESULTS = self.queue / "results"
        queue_worker.STATE = self.queue / "state.json"
        queue_worker.ARCHIVE = self.queue / "archive"
        queue_worker.DISCOVERY_STATE = self.queue / "discovery-state.json"

        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        (self.repo / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            setattr(queue_worker, name, value)
        self.tmp.cleanup()

    @staticmethod
    def _sub(run_key: str = "2026-09-20T01:00:00+09:00") -> dict:
        return {
            "operation": "submit_discovery_round",
            "candidates": [{"canonical_id": "arXiv:2609.99999", "title": "New"}],
            "discovery_stats": {
                "run_key": run_key,
                "round": "r1",
                "axis": "memory",
            },
        }

    def _commit_result(self, *, author_email: str = "survey-discovery-precheck[bot]@users.noreply.github.com") -> Path:
        path = self.results / "req-1.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "operation": "precheck_discovery_candidates",
                    "ok": True,
                    "request_id": "req-1",
                    "run_key": "2026-09-20T01:00:00+09:00",
                    "axis": "memory",
                    "snapshot_source_commit": "abc123",
                    "allowed_records": [
                        {
                            "primary_identity": "id:arXiv:2609.99999",
                            "identity_tokens": ["id:arXiv:2609.99999"],
                            "record": {"canonical_id": "arXiv:2609.99999", "title": "New"},
                        }
                    ],
                    "receipt": "sha256:receipt",
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", path.relative_to(self.repo).as_posix()], cwd=self.repo, check=True)
        env = dict(os.environ)
        env["GIT_AUTHOR_NAME"] = "survey-discovery-precheck[bot]"
        env["GIT_AUTHOR_EMAIL"] = author_email
        subprocess.run(["git", "commit", "-qm", "precheck result"], cwd=self.repo, check=True, env=env)
        return path

    def test_historical_round_remains_compatible_without_precheck(self) -> None:
        sub = self._sub("2026-09-19T23:00:00+09:00")
        self.assertIsNone(queue_worker.validate_discovery_precheck(sub))

    def test_future_round_without_precheck_returns_actionable_guidance(self) -> None:
        with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
            queue_worker.validate_discovery_precheck(self._sub())
        self.assertEqual(ctx.exception.code, "discovery_precheck_required")
        self.assertIn("NEW immutable Discovery submission", ctx.exception.next_action)
        self.assertTrue(any("precheck" in step for step in ctx.exception.recovery_steps))

    def test_workflow_produced_result_allows_only_emitted_candidate(self) -> None:
        self._commit_result()
        sub = self._sub()
        sub["discovery_precheck"] = {
            "request_id": "req-1",
            "result_path": ".survey/work-queue/discovery-precheck/results/req-1.json",
            "receipt": "sha256:receipt",
        }
        result = queue_worker.validate_discovery_precheck(sub)
        self.assertEqual(result["request_id"], "req-1")

    def test_handwritten_result_is_rejected_with_recovery_guidance(self) -> None:
        self._commit_result(author_email="worker@example.com")
        sub = self._sub()
        sub["discovery_precheck"] = {
            "request_id": "req-1",
            "result_path": ".survey/work-queue/discovery-precheck/results/req-1.json",
            "receipt": "sha256:receipt",
        }
        with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
            queue_worker.validate_discovery_precheck(sub)
        self.assertIn("workflow", str(ctx.exception))

    def test_candidate_not_emitted_by_result_is_rejected(self) -> None:
        self._commit_result()
        sub = self._sub()
        sub["candidates"] = [{"canonical_id": "arXiv:2609.88888", "title": "Bypass"}]
        sub["discovery_precheck"] = {
            "request_id": "req-1",
            "result_path": ".survey/work-queue/discovery-precheck/results/req-1.json",
            "receipt": "sha256:receipt",
        }
        with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
            queue_worker.validate_discovery_precheck(sub)
        self.assertIn("not emitted", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
