from __future__ import annotations

import json
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_search_filter  # noqa: E402
import paper_identity  # noqa: E402
from build_discovery_identity_snapshot import shard_name  # noqa: E402


class DiscoveryCandidateIdFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / "discovery-identities"
        self.rejections = self.root / "discovery-rejections.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_snapshot(self, *, tokens=(), represented=()) -> None:
        self.snapshot.mkdir(parents=True, exist_ok=True)
        shards: dict[str, list[str]] = defaultdict(list)
        for token in tokens:
            shards[shard_name(token)].append(token)
        for name, values in shards.items():
            (self.snapshot / name).write_text("".join(value + "\n" for value in values), encoding="utf-8")
        (self.snapshot / "_represented_papers.json").write_text(
            json.dumps(paper_identity.build_represented_resolver(list(represented))),
            encoding="utf-8",
        )
        (self.snapshot / "_manifest.json").write_text(
            json.dumps({
                "schema_version": 2,
                "source": "queue_worker.existing_candidate_keys",
                "source_commit": "test-main",
                "code_search_is_authority": False,
                "shards": {name: len(values) for name, values in shards.items()},
                "represented_resolver_file": "_represented_papers.json",
            }),
            encoding="utf-8",
        )

    def _write_rejections(self, records: dict) -> None:
        self.rejections.write_text(
            json.dumps({
                "source": "immutable_discovery_submissions.rejected_candidates",
                "records": records,
            }),
            encoding="utf-8",
        )

    def _classify(self, rows, *, reconsider_identifiers=None):
        classify = getattr(discovery_search_filter, "classify_explicit_identifier_lookups", None)
        self.assertTrue(callable(classify), "explicit identifier classifier is missing")
        if not callable(classify):
            return None
        return classify(
            rows,
            snapshot_dir=self.snapshot,
            rejection_ledger_path=self.rejections,
            reconsider_identifiers=set(reconsider_identifiers or []),
        )

    @staticmethod
    def _found(canonical_id: str, title: str, **extra):
        record = {"canonical_id": canonical_id, "title": title, **extra}
        return {"requested_id": canonical_id, "status": "found", "record": record}

    def test_existing_canonical_identity_is_reported_for_its_input_id(self) -> None:
        identity = "arXiv:2609.20001"
        self._write_snapshot(tokens={"id:" + identity})

        outcomes = self._classify([self._found(identity, "Already represented")])
        if outcomes is None:
            return

        self.assertEqual(outcomes[0]["requested_id"], identity)
        self.assertEqual(outcomes[0]["status"], "filtered_by_snapshot")
        self.assertEqual(outcomes[0]["filter_reason"], "identity_token")

    def test_alias_identity_is_reported_as_snapshot_filtered(self) -> None:
        arxiv_id = "arXiv:2609.20002"
        doi_id = "DOI:10.48550/arxiv.2609.20002"
        represented = [{"canonical_id": arxiv_id, "title": "Existing alias paper"}]
        self._write_snapshot(represented=represented)

        outcomes = self._classify([self._found(doi_id, "Provider alias title", doi="10.48550/arxiv.2609.20002")])
        if outcomes is None:
            return

        self.assertEqual(outcomes[0]["requested_id"], doi_id)
        self.assertEqual(outcomes[0]["status"], "filtered_by_snapshot")
        self.assertEqual(outcomes[0]["filter_reason"], "represented_paper_match")
        self.assertTrue(outcomes[0]["matched_paper_key"].startswith("paper:"))

    def test_rejection_ledger_match_is_distinctly_reported(self) -> None:
        identity = "arXiv:2609.20003"
        self._write_snapshot()
        self._write_rejections({"id:" + identity: {"identity_tokens": ["id:" + identity]}})

        outcomes = self._classify([self._found(identity, "Previously rejected")])
        if outcomes is None:
            return

        self.assertEqual(outcomes[0]["status"], "filtered_by_snapshot")
        self.assertEqual(outcomes[0]["filter_reason"], "rejection_ledger")

    def test_reconsidered_identifier_bypasses_rejection_ledger_only(self) -> None:
        identity = "arXiv:2609.20033"
        self._write_snapshot()
        self._write_rejections({"id:" + identity: {"identity_tokens": ["id:" + identity]}})

        outcomes = self._classify(
            [self._found(identity, "Previously borderline")],
            reconsider_identifiers={identity},
        )
        if outcomes is None:
            return
        self.assertEqual(outcomes[0]["status"], "allowed")

        self._write_snapshot(tokens={"id:" + identity})
        outcomes = self._classify(
            [self._found(identity, "Now represented")],
            reconsider_identifiers={identity},
        )
        self.assertEqual(outcomes[0]["status"], "filtered_by_snapshot")
        self.assertEqual(outcomes[0]["filter_reason"], "identity_token")

    def test_unseen_identity_remains_allowed(self) -> None:
        identity = "arXiv:2609.20004"
        self._write_snapshot()

        outcomes = self._classify([self._found(identity, "New paper")])
        if outcomes is None:
            return

        self.assertEqual(outcomes[0]["status"], "allowed")
        self.assertEqual(outcomes[0]["record"]["canonical_id"], identity)

    def test_two_ids_resolving_to_one_paper_preserve_both_status_rows(self) -> None:
        arxiv_id = "arXiv:2609.20005"
        doi_id = "DOI:10.48550/arxiv.2609.20005"
        self._write_snapshot()
        rows = [
            self._found(arxiv_id, "Same paper"),
            self._found(doi_id, "Same paper alias", doi="10.48550/arxiv.2609.20005"),
        ]

        outcomes = self._classify(rows)
        if outcomes is None:
            return

        self.assertEqual([row["requested_id"] for row in outcomes], [arxiv_id, doi_id])
        self.assertEqual([row["status"] for row in outcomes], ["allowed", "intra_batch_duplicate"])
        self.assertEqual(outcomes[1]["filter_reason"], "represented_paper_alias_within_batch")


if __name__ == "__main__":
    unittest.main()
