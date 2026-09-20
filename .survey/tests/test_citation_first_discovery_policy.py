from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


class CitationFirstDiscoveryPolicyTest(unittest.TestCase):
    def test_precheck_sources_are_classified_by_citation_direction(self) -> None:
        backward_cases = [
            {
                "provider": "repository_references",
                "source_url": "repository://structured-references",
            },
            {
                "provider": "openalex_references",
                "source_url": "https://api.openalex.org/works/W123",
            },
            {
                "provider": "semantic_scholar",
                "source_url": "https://api.semanticscholar.org/graph/v1/paper/abc/references",
            },
        ]
        forward_cases = [
            {
                "provider": "semantic_scholar",
                "source_url": "https://api.semanticscholar.org/graph/v1/paper/abc/citations",
            },
            {
                "provider": "openalex",
                "source_url": "https://api.openalex.org/works?filter=cites:W123&sort=publication_date:desc",
            },
        ]
        for result in backward_cases:
            with self.subTest(result=result):
                self.assertEqual(
                    queue_worker._citation_direction_from_precheck_result(result),
                    "backward",
                )
        for result in forward_cases:
            with self.subTest(result=result):
                self.assertEqual(
                    queue_worker._citation_direction_from_precheck_result(result),
                    "forward",
                )
        self.assertIsNone(
            queue_worker._citation_direction_from_precheck_result(
                {
                    "provider": "openalex",
                    "source_url": "https://api.openalex.org/works?search=llm+serving",
                }
            )
        )

    def test_normal_search_requires_both_citation_directions_in_same_run(self) -> None:
        original = queue_worker.DISCOVERY_STATE
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                run_key = "2026-09-20T20:00:00+09:00"
                queue_worker.DISCOVERY_STATE.write_text(
                    json.dumps(
                        {
                            "history": [
                                {
                                    "run_key": run_key,
                                    "citation_direction": "backward",
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                sub = {
                    "discovery_stats": {
                        "run_key": run_key,
                        "round": "normal-search",
                        "axis": "keyword-gap-fill",
                    }
                }
                result = {
                    "provider": "openalex",
                    "source_url": "https://api.openalex.org/works?search=moe+serving",
                }
                with self.assertRaises(queue_worker.DiscoveryPrecheckError) as ctx:
                    queue_worker._validate_citation_first_route(
                        sub,
                        result,
                        sub["discovery_stats"],
                    )
                self.assertEqual(ctx.exception.code, "citation_first_required")
                self.assertIn("forward-citation", ctx.exception.next_action)

                queue_worker.DISCOVERY_STATE.write_text(
                    json.dumps(
                        {
                            "history": [
                                {"run_key": run_key, "citation_direction": "backward"},
                                {"run_key": run_key, "citation_direction": "forward"},
                                {"run_key": "other-run", "citation_direction": "forward"},
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                self.assertIsNone(
                    queue_worker._validate_citation_first_route(
                        sub,
                        result,
                        sub["discovery_stats"],
                    )
                )
        finally:
            queue_worker.DISCOVERY_STATE = original

    def test_reference_pool_does_not_block_forward_citation(self) -> None:
        original = queue_worker.DISCOVERY_STATE
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                queue_worker.DISCOVERY_STATE.write_text(
                    json.dumps(
                        {
                            "history": [
                                {
                                    "run_key": "run-1",
                                    "citation_direction": "backward",
                                    "accepted_count": 3,
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                sub = {
                    "discovery_stats": {
                        "run_key": "run-1",
                        "round": "forward-refresh",
                        "axis": "lineage-forward-citation",
                    }
                }
                forward_result = {
                    "provider": "openalex",
                    "source_url": "https://api.openalex.org/works?filter=cites:W123&sort=publication_date:desc",
                }
                self.assertEqual(
                    queue_worker._validate_citation_first_route(
                        sub,
                        forward_result,
                        sub["discovery_stats"],
                    ),
                    "forward",
                )
        finally:
            queue_worker.DISCOVERY_STATE = original

    def test_discovery_stats_persist_provider_and_citation_direction(self) -> None:
        original = queue_worker.DISCOVERY_STATE
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                sub = {
                    "_file": "work-queue/submissions/citation-route.json",
                    "candidates": [],
                    "discovery_stats": {
                        "run_key": "run-2",
                        "round": "forward-1",
                        "axis": "forward-citation",
                    },
                }
                precheck = {
                    "provider": "semantic_scholar",
                    "source_url": "https://api.semanticscholar.org/graph/v1/paper/abc/citations",
                }
                self.assertTrue(
                    queue_worker.record_discovery_stats(
                        sub,
                        accepted_count=0,
                        precheck_result=precheck,
                    )
                )
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                row = state["history"][-1]
                self.assertEqual(row["provider"], "semantic_scholar")
                self.assertEqual(row["citation_direction"], "forward")
                self.assertTrue(row["source_url"].endswith("/citations"))
        finally:
            queue_worker.DISCOVERY_STATE = original


if __name__ == "__main__":
    unittest.main()
