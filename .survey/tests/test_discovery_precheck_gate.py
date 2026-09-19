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
                    "schema_version": 2,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "req-1",
                    "collector_id": "collector-1",
                    "run_key": "validation-round",
                    "axis": "memory",
                    "provider_has_more": False,
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
        self.assertTrue(result["evaluation_allowed"])
        self.assertEqual(result["decision"], "READY_FOR_EVALUATION")
        self.assertEqual(result["stop_reason"], "PROVIDER_EXHAUSTED")
        self.assertIn("id:arXiv:2609.99999", result["allowed_records"][0]["identity_tokens"])

    def test_iterative_processor_forces_next_page_and_collapses_cross_page_duplicate(self) -> None:
        request1 = self.root / "request-1.json"
        request1.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "req-page-1",
                    "collector_id": "collector-pages",
                    "run_key": "validation-round",
                    "axis": "citations",
                    "target_unseen": 2,
                    "provider_has_more": True,
                    "records": [
                        {"canonical_id": "arXiv:2609.90001", "title": "New A"},
                        {"canonical_id": "arXiv:2609.00001", "title": "Known"},
                    ],
                }
            ),
            encoding="utf-8",
        )

        first = process_discovery_precheck.process_request(
            request1,
            snapshot_dir=self.snapshot,
            rejection_ledger_path=self.ledger,
        )
        self.assertFalse(first["evaluation_allowed"])
        self.assertEqual(first["decision"], "CONTINUE_FETCH")
        self.assertEqual(first["unseen_result_count"], 1)
        self.assertEqual(first["pages_processed"], 1)

        results_dir = self.root / "results"
        results_dir.mkdir()
        (results_dir / "req-page-1.json").write_text(
            json.dumps(first),
            encoding="utf-8",
        )

        request2 = self.root / "request-2.json"
        request2.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "req-page-2",
                    "collector_id": "collector-pages",
                    "run_key": "validation-round",
                    "axis": "citations",
                    "target_unseen": 2,
                    "provider_has_more": True,
                    "previous_request_id": "req-page-1",
                    "previous_receipt": first["receipt"],
                    "records": [
                        {
                            "source_url": "https://arxiv.org/abs/2609.90001",
                            "title": "New A",
                        },
                        {"canonical_id": "arXiv:2609.90002", "title": "New B"},
                    ],
                }
            ),
            encoding="utf-8",
        )

        second = process_discovery_precheck.process_request(
            request2,
            snapshot_dir=self.snapshot,
            rejection_ledger_path=self.ledger,
        )
        self.assertTrue(second["evaluation_allowed"])
        self.assertEqual(second["decision"], "READY_FOR_EVALUATION")
        self.assertEqual(second["stop_reason"], "TARGET_REACHED")
        self.assertEqual(second["pages_processed"], 2)
        self.assertEqual(second["cross_page_duplicate_filtered_count"], 1)
        self.assertEqual(
            [row["title"] for row in second["results"]],
            ["New A", "New B"],
        )

    def test_iterative_request_requires_explicit_provider_has_more(self) -> None:
        request = self.root / "request-missing-more.json"
        request.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "req-missing-more",
                    "collector_id": "collector-missing-more",
                    "run_key": "validation-round",
                    "axis": "references",
                    "records": [],
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(process_discovery_precheck.DiscoveryPrecheckRequestError):
            process_discovery_precheck.process_request(
                request,
                snapshot_dir=self.snapshot,
                rejection_ledger_path=self.ledger,
            )


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
        self.submissions = self.queue / "submissions"
        self.results = self.queue / "discovery-precheck" / "results"
        self.submissions.mkdir(parents=True)
        self.results.mkdir(parents=True)
        queue_worker.ROOT = self.survey
        queue_worker.QUEUE = self.queue
        queue_worker.JOBS = self.queue / "jobs"
        queue_worker.SUBMISSIONS = self.submissions
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

        self.old_submission = self.submissions / "old-round.json"
        self.old_submission.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", self.old_submission.relative_to(self.repo).as_posix()], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "historical discovery submission"], cwd=self.repo, check=True)

        marker = self.queue / "discovery-precheck" / "ENFORCED"
        marker.write_text("enforced\n", encoding="utf-8")
        subprocess.run(["git", "add", marker.relative_to(self.repo).as_posix()], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "enable discovery precheck"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        for name, value in self.originals.items():
            setattr(queue_worker, name, value)
        self.tmp.cleanup()

    @staticmethod
    def _base_sub() -> dict:
        return {
            "operation": "submit_discovery_round",
            "candidates": [{"canonical_id": "arXiv:2609.99999", "title": "New"}],
            "discovery_stats": {
                "run_key": "validation-round",
                "round": "r1",
                "axis": "memory",
            },
        }

    def _commit_submission(self, name: str = "new-round.json") -> str:
        path = self.submissions / name
        path.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", path.relative_to(self.repo).as_posix()], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", f"add {name}"], cwd=self.repo, check=True)
        return f"work-queue/submissions/{name}"

    def _commit_result(
        self,
        *,
        author_email: str = "survey-discovery-precheck[bot]@users.noreply.github.com",
        schema_version: int = 1,
        evaluation_allowed: bool = True,
    ) -> Path:
        path = self.results / "req-1.json"
        payload = {
            "schema_version": schema_version,
            "operation": "precheck_discovery_candidates",
            "ok": True,
            "request_id": "req-1",
            "run_key": "validation-round",
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
        if schema_version >= 2:
            payload.update(
                {
                    "collector_id": "collector-1",
                    "target_unseen": 10,
                    "pages_processed": 1,
                    "evaluation_allowed": evaluation_allowed,
                    "decision": "READY_FOR_EVALUATION" if evaluation_allowed else "CONTINUE_FETCH",
                }
            )
        path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        subprocess.run(["git", "add", path.relative_to(self.repo).as_posix()], cwd=self.repo, check=True)
        env = dict(os.environ)
        env["GIT_AUTHOR_NAME"] = "survey-discovery-precheck[bot]"
        env["GIT_AUTHOR_EMAIL"] = author_email
        subprocess.run(["git", "commit", "-qm", "precheck result"], cwd=self.repo, check=True, env=env)
        return path

    def test_historical_submission_predating_marker_remains_compatible(self) -> None:
        sub = self._base_sub()
        sub["_file"] = "work-queue/submissions/old-round.json"
        self.assertIsNone(queue_worker.validate_discovery_precheck(sub))

    def test_new_submission_without_precheck_returns_actionable_guidance(self) -> None:
        sub = self._base_sub()
        sub["_file"] = self._commit_submission()
        with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
            queue_worker.validate_discovery_precheck(sub)
        self.assertEqual(ctx.exception.code, "discovery_precheck_required")
        self.assertIn("NEW immutable Discovery submission", ctx.exception.next_action)
        self.assertTrue(any("precheck" in step for step in ctx.exception.recovery_steps))

    def test_bypass_rejection_does_not_create_ingest_job(self) -> None:
        sub = self._base_sub()
        sub["_file"] = self._commit_submission("bypass-round.json")
        queue_worker.JOBS.mkdir(parents=True, exist_ok=True)
        state = {"stats": {"discovered": 0, "selected": 0}}

        with self.assertRaises(queue_worker.DiscoveryPrecheckError):
            queue_worker.process_discovery_round_submission(sub, state)

        self.assertEqual(list(queue_worker.JOBS.glob("*.json")), [])

    def test_workflow_produced_result_allows_only_emitted_candidate(self) -> None:
        self._commit_result()
        sub = self._base_sub()
        sub["_file"] = self._commit_submission()
        sub["discovery_precheck"] = {
            "request_id": "req-1",
            "result_path": ".survey/work-queue/discovery-precheck/results/req-1.json",
            "receipt": "sha256:receipt",
        }
        result = queue_worker.validate_discovery_precheck(sub)
        self.assertEqual(result["request_id"], "req-1")

    def test_intermediate_iterative_result_cannot_authorize_submission(self) -> None:
        self._commit_result(schema_version=2, evaluation_allowed=False)
        sub = self._base_sub()
        sub["_file"] = self._commit_submission()
        sub["discovery_precheck"] = {
            "request_id": "req-1",
            "result_path": ".survey/work-queue/discovery-precheck/results/req-1.json",
            "receipt": "sha256:receipt",
        }
        with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
            queue_worker.validate_discovery_precheck(sub)
        self.assertIn("not final", str(ctx.exception))

    def test_handwritten_result_is_rejected_with_recovery_guidance(self) -> None:
        self._commit_result(author_email="worker@example.com")
        sub = self._base_sub()
        sub["_file"] = self._commit_submission()
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
        sub = self._base_sub()
        sub["_file"] = self._commit_submission()
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
