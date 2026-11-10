import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


SCRIPTS = Path(__file__).parents[1] / "scripts"
SCRIPT = SCRIPTS / "build_worker_worklist.py"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load():
    spec = importlib.util.spec_from_file_location("build_worker_worklist_identity_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WorkerWorklistIdentityTests(unittest.TestCase):
    def test_research_reservation_excludes_discovery_arxiv_doi_alias(self):
        module = _load()
        reserved = [
            {
                "canonical_id": "arXiv:2401.01234",
                "title": "Reserved Paper",
                "source_url": "https://arxiv.org/abs/2401.01234",
            }
        ]
        discovery = [
            {
                "canonical_id": "DOI:10.48550/arxiv.2401.01234",
                "identity_tokens": ["DOI:10.48550/arxiv.2401.01234"],
                "source_url": "https://doi.org/10.48550/arxiv.2401.01234",
            },
            {
                "canonical_id": "arXiv:2401.99999",
                "identity_tokens": ["arXiv:2401.99999"],
                "title": "Unique Discovery Paper",
            },
        ]

        remaining = module._exclude_reserved_identities(
            discovery,
            reserved_rows=reserved,
        )

        self.assertEqual(
            [row["canonical_id"] for row in remaining],
            ["arXiv:2401.99999"],
        )

    def test_research_rows_are_deduped_before_worker_split(self):
        module = _load()
        rows = [
            {
                "canonical_id": "DOI:10.48550/arxiv.2502.01234",
                "source_url": "https://doi.org/10.48550/arxiv.2502.01234",
            },
            {
                "canonical_id": "arXiv:2502.01234",
                "source_url": "https://arxiv.org/abs/2502.01234",
            },
            {
                "canonical_id": "arXiv:2502.09999",
                "source_url": "https://arxiv.org/abs/2502.09999",
            },
        ]

        deduped = module._dedupe_rows_by_identity(rows)
        assigned = module._split(deduped, limit=10)

        all_ids = [
            row["canonical_id"]
            for worker in ("00", "30", "45")
            for row in assigned[worker]
        ]
        self.assertEqual(len(all_ids), 2)
        self.assertIn("arXiv:2502.09999", all_ids)
        self.assertEqual(
            sum(
                ident in {
                    "DOI:10.48550/arxiv.2502.01234",
                    "arXiv:2502.01234",
                }
                for ident in all_ids
            ),
            1,
        )


    def test_empty_discovery_pool_refills_from_borderline_with_repeat_penalty(self):
        module = _load()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config_path = root / ".survey/config/candidate-priority.json"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "policy_name": "test",
                    "freshness": {"enabled": False},
                    "prestigious_venue": {"enabled": False},
                    "citations": {"enabled": True, "score_per_citation": 1, "max_score": None},
                    "borderline_reconsideration": {"refill_target": 2, "repeat_penalty": 100000000},
                    "fallback_priority": 0,
                }),
                encoding="utf-8",
            )
            ledger_path = root / ".survey/work-queue/reference-curation/borderline-papers.json"
            ledger_path.parent.mkdir(parents=True)
            ledger_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "classification": "borderline",
                    "records": {
                        "arXiv:2001.00001": {
                            "canonical_id": "arXiv:2001.00001",
                            "identity_tokens": ["arXiv:2001.00001"],
                            "title": "A",
                            "citation_count": 5,
                            "borderline_recheck_count": 0,
                        },
                        "arXiv:2001.00002": {
                            "canonical_id": "arXiv:2001.00002",
                            "identity_tokens": ["arXiv:2001.00002"],
                            "title": "B",
                            "citation_count": 1000,
                            "borderline_recheck_count": 1,
                        },
                        "arXiv:2001.00003": {
                            "canonical_id": "arXiv:2001.00003",
                            "identity_tokens": ["arXiv:2001.00003"],
                            "title": "C",
                            "citation_count": 1,
                            "borderline_recheck_count": 0,
                        },
                    },
                }),
                encoding="utf-8",
            )

            rows, pending = module._discovery_candidates(root)
            self.assertEqual(pending, 2)
            self.assertEqual([row["canonical_id"] for row in rows], [
                "arXiv:2001.00001",
                "arXiv:2001.00003",
            ])
            self.assertTrue(all(row["source_kind"] == "borderline_reconsideration" for row in rows))
            self.assertEqual(rows[0]["priority_breakdown"]["borderline_recheck_penalty"], 0)

            penalized = module._borderline_reconsideration_candidates(
                root, cache={}, config=json.loads(config_path.read_text(encoding="utf-8"))
            )
            by_id = {row["canonical_id"]: row for row in penalized}
            self.assertEqual(by_id["arXiv:2001.00002"]["priority"], 1000 - 100000000)
            self.assertEqual(by_id["arXiv:2001.00002"]["priority_breakdown"]["borderline_recheck_count"], 1)

    def test_research_worklist_keeps_job_bibliography_when_priority_cache_alias_is_wrong(self):
        module = _load()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = root / ".survey/config/candidate-priority.json"
            config.parent.mkdir(parents=True)
            config.write_text(
                json.dumps({
                    "schema_version": 1,
                    "policy_name": "test",
                    "freshness": {"enabled": False},
                    "prestigious_venue": {"enabled": False},
                    "citations": {"enabled": True, "score_per_citation": 1, "max_score": None},
                    "fallback_priority": 0,
                }),
                encoding="utf-8",
            )
            cache = root / ".survey/work-queue/candidate-priority-cache.json"
            cache.parent.mkdir(parents=True)
            cache.write_text(
                json.dumps({
                    "schema_version": 1,
                    "records": {
                        "arXiv:2405.21060": {
                            "title": "Sovereign Byte Firewall: wrong provider alias",
                            "source_url": "https://example.invalid/wrong",
                            "published": "2026-01-01",
                            "citation_count": 78,
                            "citation_count_source": "openalex",
                        }
                    },
                    "aliases": {},
                    "lookup_failures": {},
                }),
                encoding="utf-8",
            )
            job_dir = root / ".survey/work-queue/jobs"
            job_dir.mkdir(parents=True)
            (job_dir / "job-research-mamba2.json").write_text(
                json.dumps({
                    "job_id": "job-research-mamba2",
                    "type": "research",
                    "status": "ready",
                    "canonical_id": "arXiv:2405.21060",
                    "arxiv_id": "2405.21060",
                    "title": "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality",
                    "source_url": "https://arxiv.org/abs/2405.21060",
                    "published": "2024-05-31",
                    "citation_count": 70,
                    "paper_path": "papers/inference/20-linear-recurrent-language-models/2024-2405.21060-transformers-are-ssms-generalized-models-and-efficient-algorithms-through-structured-state-space-duality.md",
                }),
                encoding="utf-8",
            )

            rows, ready_total, _reserved = module._research_candidates(root)
            self.assertEqual(ready_total, 1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(
                rows[0]["title"],
                "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality",
            )
            self.assertEqual(rows[0]["source_url"], "https://arxiv.org/abs/2405.21060")
            self.assertEqual(rows[0]["published"], "2024-05-31")
            self.assertEqual(rows[0]["citation_count"], 78)

    def test_split_uses_three_disjoint_workers(self):
        module = _load()
        rows = [
            {"canonical_id": f"arXiv:2601.{index:05d}"}
            for index in range(9)
        ]

        assigned = module._split(rows, limit=10)

        self.assertEqual(tuple(assigned), ("00", "30", "45"))
        self.assertEqual([len(assigned[key]) for key in ("00", "30", "45")], [3, 3, 3])
        identities = [
            row["canonical_id"]
            for key in ("00", "30", "45")
            for row in assigned[key]
        ]
        self.assertEqual(len(identities), len(set(identities)))


    def test_large_worklist_is_fetchable_and_lossless(self):
        module = _load()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / ".survey/work-queue"
            payloads = {}
            for slot in ("00", "30", "45"):
                rows = [
                    {
                        "rank": i + 1,
                        "source_rank": i * 3 + 1,
                        "assigned_worker": f"scheduled-chat-{slot}",
                        "canonical_id": f"arXiv:2501.{i:05d}",
                        "title": f"LLM serving candidate {i}",
                        "priority": 30,
                        "source_url": f"https://arxiv.org/abs/2501.{i:05d}",
                        "linked_from": [f"papers/inference/long-lineage/{j:03d}/" + ("x" * 40) for j in range(40)],
                    }
                    for i in range(500)
                ]
                payloads[slot] = {
                    "schema_version": 2, "worker_id": f"scheduled-chat-{slot}",
                    "research_audit": {
                        "ready_total": 0, "claimable_total": 0, "displayed": 0, "rows": [],
                    },
                    "discovery_review": {
                        "pending_total": 500, "prefilter": {}, "displayed": 500, "rows": rows,
                    },
                }
            results = module.write_outputs(root, payloads, output_dir=output)
            for slot in ("00", "30", "45"):
                main_path = output / f"worker-worklist-{slot}.json"
                self.assertLess(main_path.stat().st_size, 1024 * 1024)
                view = json.loads(main_path.read_text(encoding="utf-8"))
                self.assertEqual(view["discovery_review"]["displayed"], 500)
                self.assertEqual(len(view["discovery_review"]["rows"]), 500)
                self.assertEqual(len(view["discovery_review"]["rows"][0]["linked_from"]), 4)
                self.assertEqual(view["discovery_review"]["rows"][0]["linked_from_count"], 40)
                restored = []
                for relpath in view["discovery_review"]["full_row_shards"]:
                    shard = json.loads((output / relpath).read_text(encoding="utf-8"))
                    self.assertEqual(shard["record_count"], len(shard["rows"]))
                    restored.extend(shard["rows"])
                self.assertEqual(restored, payloads[slot]["discovery_review"]["rows"])
                self.assertEqual(len(restored), 500)
                self.assertEqual(
                    results[slot]["discovery_review"]["full_rows_sha256"],
                    view["discovery_review"]["full_rows_sha256"],
                )
            before = (output / "worker-worklist-45.json").read_bytes()
            module.write_outputs(root, payloads, output_dir=output)
            self.assertEqual(before, (output / "worker-worklist-45.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
