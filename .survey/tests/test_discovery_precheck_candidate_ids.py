from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_discovery_precheck as precheck  # noqa: E402


class DiscoveryPrecheckCandidateIdTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / "discovery-identities"
        self.snapshot.mkdir()
        (self.snapshot / "_manifest.json").write_text(json.dumps({
            "schema_version": 2,
            "source": "queue_worker.existing_candidate_keys",
            "source_commit": "main-snapshot-abc123",
            "code_search_is_authority": False,
            "shards": {},
            "represented_resolver_file": "_represented_papers.json",
        }), encoding="utf-8")
        (self.snapshot / "_represented_papers.json").write_text(json.dumps({
            "papers": {}, "alias_to_paper": {}, "title_hash_to_paper": {},
        }), encoding="utf-8")
        self.rejections = self.root / "discovery-rejections.json"
        self.rejections.write_text(json.dumps({
            "source": "immutable_discovery_submissions.rejected_candidates", "records": {},
        }), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _request(self, identifiers: list[str]) -> Path:
        path = self.root / "request.json"
        path.write_text(json.dumps({
            "schema_version": 3,
            "operation": "precheck_discovery_candidates",
            "request_id": "candidate-id-run-1",
            "collector_id": "candidate-id-tests",
            "run_key": "candidate-id-run-1",
            "axis": "library-candidate-intake",
            "provider": "candidate_id_lookup",
            "source_url": "identifier://approved-public-apis",
            "identifiers": identifiers,
        }), encoding="utf-8")
        return path

    def test_mixed_batch_preserves_per_id_results_and_only_allows_verified_records(self) -> None:
        ids = ["arXiv:2407.21018", "DOI:10.1000/notfound", "OpenReview:abcdefghij"]
        lookups = [
            {"requested_id": ids[0], "status": "found", "lookup_route": "semantic_scholar_single", "record": {
                "canonical_id": ids[0], "arxiv_id": "2407.21018", "title": "New paper", "source_url": "https://arxiv.org/abs/2407.21018",
            }},
            {"requested_id": ids[1], "status": "error", "lookup_route": "semantic_scholar_single", "error": "temporary outage"},
            {"requested_id": ids[2], "status": "unresolved", "lookup_route": "openreview_notes", "record": None},
        ]
        with patch.object(precheck.discovery_provider_adapter, "lookup_identifiers", return_value=lookups) as lookup:
            result = precheck.process_request(
                self._request(ids), snapshot_dir=self.snapshot,
                rejection_ledger_path=self.rejections, repo_root=self.root,
            )

        lookup.assert_called_once_with(ids)
        self.assertTrue(result["evaluation_allowed"])
        self.assertEqual([row["status"] for row in result["candidate_statuses"]], [
            "allowed", "provider_error", "provider_unresolved",
        ])
        self.assertEqual([row["canonical_id"] for row in result["results"]], [ids[0]])
        self.assertEqual(len(result["allowed_records"]), 1)
        self.assertEqual(result["snapshot_source_commit"], "main-snapshot-abc123")
        self.assertTrue(result["provider_exhausted"])
        self.assertEqual(result["stop_reason"], "EXPLICIT_IDENTIFIERS_PROCESSED")

    def test_snapshot_duplicate_is_statused_but_excluded_from_allowed_records(self) -> None:
        ids = ["arXiv:2407.21018"]
        record = {"canonical_id": ids[0], "arxiv_id": "2407.21018", "title": "Existing paper"}
        # Add the exact stable token to the authoritative snapshot.
        (self.snapshot / "arxiv-2407.txt").write_text("id:arXiv:2407.21018\n", encoding="utf-8")
        manifest = json.loads((self.snapshot / "_manifest.json").read_text(encoding="utf-8"))
        manifest["shards"] = {"arxiv-2407.txt": 1}
        (self.snapshot / "_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with patch.object(precheck.discovery_provider_adapter, "lookup_identifiers", return_value=[{
            "requested_id": ids[0], "status": "found", "record": record, "lookup_route": "semantic_scholar_batch",
        }]):
            result = precheck.process_request(
                self._request(ids), snapshot_dir=self.snapshot,
                rejection_ledger_path=self.rejections, repo_root=self.root,
            )
        self.assertEqual(result["candidate_statuses"][0]["status"], "filtered_by_snapshot")
        self.assertEqual(result["allowed_records"], [])

    def test_receipt_binds_requested_ids_statuses_allowed_records_and_snapshot(self) -> None:
        ids = ["arXiv:2407.21018"]
        lookup = [{
            "requested_id": ids[0], "status": "found", "record": {
                "canonical_id": ids[0], "arxiv_id": "2407.21018", "title": "New paper",
            }, "lookup_route": "semantic_scholar_batch",
        }]

        def run(current_ids: list[str], row: dict) -> dict:
            with patch.object(precheck.discovery_provider_adapter, "lookup_identifiers", return_value=[row]):
                return precheck.process_request(
                    self._request(current_ids), snapshot_dir=self.snapshot,
                    rejection_ledger_path=self.rejections, repo_root=self.root,
                )

        baseline = run(ids, lookup[0])
        changed_status = run(ids, {**lookup[0], "status": "unresolved", "record": None})
        changed_id = run(["arXiv:2407.21019"], {**lookup[0], "requested_id": "arXiv:2407.21019"})
        changed_record = run(ids, {**lookup[0], "record": {**lookup[0]["record"], "title": "Changed title"}})
        manifest = json.loads((self.snapshot / "_manifest.json").read_text(encoding="utf-8"))
        manifest["source_commit"] = "main-snapshot-def456"
        (self.snapshot / "_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        changed_snapshot = run(ids, lookup[0])
        self.assertNotEqual(baseline["receipt"], changed_status["receipt"])
        self.assertNotEqual(baseline["receipt"], changed_id["receipt"])
        self.assertNotEqual(baseline["receipt"], changed_record["receipt"])
        self.assertNotEqual(baseline["receipt"], changed_snapshot["receipt"])


if __name__ == "__main__":
    unittest.main()
