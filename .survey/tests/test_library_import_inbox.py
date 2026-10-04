#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import process_library_import_inbox as inbox


class LibraryImportInboxTests(unittest.TestCase):
    def test_research_metadata_gate_rejects_incomplete_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ".survey/import-inbox/pending/research/paper.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                """---
canonical_id: arXiv:2609.99999
title: Incomplete
summary: 不足メタデータの検査用。
list_summary: 不足メタデータの検査用。
source: https://arxiv.org/abs/2609.99999
worker_completed_at: '2026-10-03T16:00:00+09:00'
worker_run_key: 20261003-1600-scheduled-chat-00
---
# Incomplete
""",
                encoding="utf-8",
            )
            meta = inbox.parse_frontmatter(source.read_text(encoding="utf-8"))
            failures = inbox.research_metadata_failures(source, meta, root)
            self.assertIn("authors", failures)
            self.assertIn("published", failures)
            self.assertIn("publication", failures)
            self.assertIn("publication_type", failures)
            self.assertIn("publication_status", failures)
            self.assertIn("sources", failures)
            self.assertIn("implementation", failures)
            self.assertIn("code", failures)
            self.assertIn("last_checked", failures)
            self.assertIn("arxiv_id", failures)
            self.assertIn("arxiv_categories.primary", failures)
            self.assertIn("arxiv_categories.cross_list", failures)

    def test_research_metadata_gate_rejects_invalid_published_format(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ".survey/import-inbox/pending/research/paper.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                """---
canonical_id: DOI:10.1000/example
title: Example
summary: 完成原稿。
list_summary: 完成原稿の一文要約。
authors:
- Example Author
published: '2026'
publication: Example Venue
publication_type: 査読付き学術論文
publication_status: Published
source: https://doi.org/10.1000/example
sources:
- https://doi.org/10.1000/example
implementation: 論文中で実装・評価済み。
code: null
last_checked: '2026-10-03'
worker_completed_at: '2026-10-03T16:00:00+09:00'
worker_run_key: 20261003-1600-scheduled-chat-00
---
# Example
""",
                encoding="utf-8",
            )
            meta = inbox.parse_frontmatter(source.read_text(encoding="utf-8"))
            failures = inbox.research_metadata_failures(source, meta, root)
            self.assertIn("published:format", failures)

    def test_research_metadata_gate_accepts_complete_library_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ".survey/import-inbox/pending/research/paper.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                """---
canonical_id: arXiv:2609.99999
arxiv_id: '2609.99999'
arxiv_categories:
  primary: cs.LG
  cross_list: []
title: Complete
summary: 必須メタデータが揃ったResearch原稿。
list_summary: 必須メタデータが揃ったResearch原稿を取り込み前に検証する。
authors:
- Example Author
published: '2026-09-01'
publication: arXiv
publication_type: プレプリント
publication_status: arXiv preprint
source: https://arxiv.org/abs/2609.99999
sources:
- https://arxiv.org/abs/2609.99999
implementation: 論文中で実装・評価済み。公式コードURLは確認できない。
code: null
last_checked: '2026-10-03'
worker_completed_at: '2026-10-03T16:00:00+09:00'
worker_run_key: 20261003-1600-scheduled-chat-00
---
# Complete
""",
                encoding="utf-8",
            )
            meta = inbox.parse_frontmatter(source.read_text(encoding="utf-8"))
            self.assertEqual(inbox.research_metadata_failures(source, meta, root), [])

    def test_research_import_adds_structural_audit_placeholders_without_claiming_audit(self) -> None:
        raw = """---
canonical_id: arXiv:2609.99999
title: Complete
last_checked: '2026-10-03'
---
# Complete
"""
        meta = inbox.parse_frontmatter(raw)
        normalized_raw, normalized_meta = inbox.normalize_research_audit_metadata(raw, meta)
        self.assertIsNone(normalized_meta["last_audited"])
        self.assertEqual(normalized_meta["audit_version"], 0)
        self.assertIn("last_audited: null", normalized_raw)
        self.assertIn("audit_version: 0", normalized_raw)

        unchanged_raw, unchanged_meta = inbox.normalize_research_audit_metadata(
            normalized_raw, normalized_meta
        )
        self.assertEqual(unchanged_raw, normalized_raw)
        self.assertEqual(unchanged_meta, normalized_meta)

    def test_library_research_japanese_normalizer_repairs_generic_terms(self) -> None:
        raw = """---
canonical_id: DOI:10.1000/example
title: Example
list_summary: "cache and memory model for serving"
---
# Example

This cache stores model state in memory for serving.
URL https://example.com/cache and `cache` code must remain unchanged.
"""
        normalized, changed = inbox.normalize_library_research_japanese(raw)
        self.assertTrue(changed)
        self.assertIn("キャッシュ", normalized)
        self.assertIn("メモリ", normalized)
        self.assertIn("モデル", normalized)
        self.assertIn("推論提供", normalized)
        self.assertIn("https://example.com/cache", normalized)
        self.assertIn("`cache`", normalized)

    def test_repo_relative_accepts_relative_and_absolute_paths(self) -> None:
        repo_root = Path("/tmp/example-repo").resolve()
        rel = Path(".survey/import-inbox/pending/research/paper.md")
        absolute = repo_root / rel

        self.assertEqual(
            inbox.repo_relative(rel, repo_root),
            ".survey/import-inbox/pending/research/paper.md",
        )
        self.assertEqual(
            inbox.repo_relative(absolute, repo_root),
            ".survey/import-inbox/pending/research/paper.md",
        )

    def test_requeues_discovery_blocked_only_by_precheck_provenance(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                blocked = root / ".survey/import-inbox/blocked/discovery/source.json"
                blocked.parent.mkdir(parents=True)
                blocked_payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "20261002T120000JST-scheduled-chat-00",
                    "record_count": 1,
                    "records": [
                        {
                            "classification": "accept",
                            "canonical_id": "arXiv:2609.00001",
                            "reason": "test",
                        }
                    ],
                }
                blocked.write_text(
                    json.dumps(blocked_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

                failure_id = "libimp-deadbeef-pre01-sub01"
                queue_result = root / f".survey/work-queue/results/{failure_id}.json"
                queue_result.parent.mkdir(parents=True)
                queue_result.write_text(
                    json.dumps(
                        {
                            "ok": False,
                            "retryable": True,
                            "error_code": "discovery_precheck_required",
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                import_result = root / ".survey/import-inbox/results/discovery/source.json"
                import_result.parent.mkdir(parents=True)
                import_result.write_text(
                    json.dumps(
                        {
                            "status": "blocked_downstream",
                            "retained_payload": ".survey/import-inbox/blocked/discovery/source.json",
                            "failures": [failure_id],
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                self.assertEqual(
                    inbox.recover_retryable_precheck_provenance_blocks(root), 1
                )
                retry_files = list(
                    (root / ".survey/import-inbox/pending/discovery").glob(
                        "retry-precheck-*--source.json"
                    )
                )
                self.assertEqual(len(retry_files), 1)
                self.assertEqual(retry_files[0].read_bytes(), blocked.read_bytes())
                self.assertEqual(
                    inbox.recover_retryable_precheck_provenance_blocks(root), 0
                )
            finally:
                os.chdir(original_cwd)

    def test_requeues_historical_provider_only_discovery_block_once(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                blocked = root / ".survey/import-inbox/blocked/discovery/source.json"
                blocked.parent.mkdir(parents=True)
                blocked_payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "20261002T120000JST-scheduled-chat-00",
                    "record_count": 2,
                    "records": [
                        {
                            "classification": "accept",
                            "canonical_id": "OpenReview:abcdefghij",
                            "identity_tokens": ["OpenReview:abcdefghij"],
                            "reason": "provider gap",
                        },
                        {
                            "classification": "unrelated",
                            "canonical_id": "arXiv:2609.00002",
                            "reason": "irrelevant",
                        },
                    ],
                }
                blocked.write_text(
                    json.dumps(blocked_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                result = root / ".survey/import-inbox/results/discovery/source.json"
                result.parent.mkdir(parents=True)
                result.write_text(
                    json.dumps(
                        {
                            "status": "blocked_downstream",
                            "retained_payload": ".survey/import-inbox/blocked/discovery/source.json",
                            "failures": ["OpenReview:abcdefghij"],
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                self.assertEqual(inbox.recover_candidate_provider_gap_blocks(root), 1)
                retries = list(
                    (root / ".survey/import-inbox/pending/discovery").glob(
                        "retry-provider-gap-*--source.json"
                    )
                )
                self.assertEqual(len(retries), 1)
                self.assertEqual(retries[0].read_bytes(), blocked.read_bytes())
                self.assertEqual(inbox.recover_candidate_provider_gap_blocks(root), 0)
            finally:
                os.chdir(original_cwd)

    def test_preferred_candidate_id_uses_stable_alias_before_openreview(self) -> None:
        record = {
            "canonical_id": "OpenReview:abcdefghij",
            "identity_tokens": [
                "OpenReview:abcdefghij",
                "arXiv:2402.15220",
                "DOI:10.18653/v1/2024.acl-long.623",
            ],
        }
        self.assertEqual(inbox.preferred_candidate_id(record), "arXiv:2402.15220")

    def test_provider_gap_alias_is_requeued_as_reduced_retry(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                blocked = root / ".survey/import-inbox/blocked/discovery-provider/gap.json"
                blocked.parent.mkdir(parents=True)
                payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "provider-gap-parent::provider-gap",
                    "provider_gap_ids": ["OpenReview:abcdefghij"],
                    "record_count": 1,
                    "records": [
                        {
                            "classification": "accept",
                            "canonical_id": "OpenReview:abcdefghij",
                            "identity_tokens": [
                                "OpenReview:abcdefghij",
                                "arXiv:2402.15220",
                            ],
                            "reason": "provider gap",
                        }
                    ],
                }
                blocked.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

                self.assertEqual(inbox.recover_provider_gap_alias_blocks(root), 1)
                retries = list(
                    (root / ".survey/import-inbox/pending/discovery").glob(
                        "retry-provider-alias-*--gap.json"
                    )
                )
                self.assertEqual(len(retries), 1)
                retry = json.loads(retries[0].read_text(encoding="utf-8"))
                self.assertEqual(retry["record_count"], 1)
                self.assertEqual(
                    inbox.preferred_candidate_id(retry["records"][0]),
                    "arXiv:2402.15220",
                )
                self.assertEqual(inbox.recover_provider_gap_alias_blocks(root), 0)
            finally:
                os.chdir(original_cwd)

    def test_provider_error_is_candidate_gap_not_whole_run_failure(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                token = "provider-gap-test"
                record = {
                    "classification": "accept",
                    "canonical_id": "OpenReview:abcdefghij",
                    "identity_tokens": ["OpenReview:abcdefghij"],
                    "reason": "provider gap",
                }
                request_id = inbox.candidate_request_id(token, 1)
                result_path = root / inbox.PRECHECK_RESULTS / f"{request_id}.json"
                result_path.parent.mkdir(parents=True)
                result_path.write_text(
                    json.dumps(
                        {
                            "ok": True,
                            "evaluation_allowed": True,
                            "candidate_statuses": [
                                {
                                    "requested_id": "OpenReview:abcdefghij",
                                    "status": "provider_error",
                                    "lookup_route": "openreview_notes",
                                    "error": "HTTP Error 403: Forbidden",
                                }
                            ],
                            "allowed_records": [],
                            "receipt": "sha256:test",
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                waiting, submission_waiting, failures, gaps, counts = (
                    inbox.create_accept_pipeline(root, token, [record])
                )
                self.assertEqual(waiting, [])
                self.assertEqual(submission_waiting, [])
                self.assertEqual(failures, [])
                self.assertEqual(gaps, ["OpenReview:abcdefghij"])
                self.assertEqual(counts["submitted"], 0)

                source = root / ".survey/import-inbox/waiting/discovery/source.json"
                source.parent.mkdir(parents=True)
                payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "provider-gap-parent",
                    "record_count": 1,
                    "records": [record],
                }
                source.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                gap_path = inbox.retain_provider_gap_payload(
                    root, source, payload, gaps
                )
                self.assertIsNotNone(gap_path)
                retained = json.loads((root / gap_path).read_text(encoding="utf-8"))
                self.assertEqual(retained["record_count"], 1)
                self.assertEqual(retained["provider_gap_ids"], gaps)
            finally:
                os.chdir(original_cwd)

    def test_oversized_discovery_run_is_retained_and_split_by_record_count(self) -> None:
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            try:
                os.chdir(root)
                waiting = root / ".survey/import-inbox/waiting/discovery"
                waiting.mkdir(parents=True)
                source = waiting / "discovery-large.json"

                records = [
                    {
                        "classification": "accept",
                        "canonical_id": f"arXiv:2609.{index:05d}",
                        "reason": f"record {index}",
                    }
                    for index in range(40)
                ]
                payload = {
                    "schema_version": 2,
                    "artifact_type": "discovery_run",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "scheduled-chat-00-test-large",
                    "record_count": len(records),
                    "records": records,
                }
                original_bytes = (
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
                ).encode("utf-8")
                source.write_bytes(original_bytes)

                self.assertEqual(inbox.split_oversized_discovery_sources(20), 1)

                retained = (
                    root
                    / ".survey/import-inbox/retained/discovery-source/discovery-large.json"
                )
                self.assertEqual(retained.read_bytes(), original_bytes)

                chunks = sorted(waiting.glob("discovery-large--chunk-*.json"))
                self.assertEqual(len(chunks), 2)
                parsed = [json.loads(path.read_text(encoding="utf-8")) for path in chunks]
                self.assertEqual([item["record_count"] for item in parsed], [20, 20])
                self.assertTrue(
                    all(
                        item["parent_run_key"] == "scheduled-chat-00-test-large"
                        for item in parsed
                    )
                )
                selected = inbox.select_discovery_sources(20)
                self.assertEqual(len(selected), 1)
                self.assertEqual(selected[0].name, chunks[0].name)
                self.assertEqual(
                    len(inbox.discovery_records(inbox.read_json(selected[0]))),
                    20,
                )
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
