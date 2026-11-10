from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import recover_discovery_provider_failures as mod


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class DiscoveryProviderFailoverTests(unittest.TestCase):
    def test_semantic_scholar_normal_failure_creates_openalex_replacement_and_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_id = "normal-s2-failed"
            request_path = root / mod.REQUEST_ROOT / f"{request_id}.json"
            write_json(
                request_path,
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": request_id,
                    "collector_id": "normal-gapfill",
                    "run_key": "run-1",
                    "axis": "normal gap-fill",
                    "provider": "semantic_scholar",
                    "source_url": (
                        "https://api.semanticscholar.org/graph/v1/paper/search/match"
                        "?query=LLM%20inference%20offloading%20memory&fields=paperId,title"
                    ),
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 2,
                    "worker_id": "scheduled-chat-00",
                    "scheduled_slot": "00",
                },
            )
            write_json(
                root / mod.RESULT_ROOT / f"{request_id}.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "ok": False,
                    "request_id": request_id,
                    "decision": "FIX_REQUEST",
                    "evaluation_allowed": False,
                    "error": "DiscoveryProviderError: unsupported Semantic Scholar paper endpoint",
                },
            )

            first = mod.recover(
                root,
                [Path(mod.REQUEST_ROOT) / f"{request_id}.json"],
                create=True,
            )
            self.assertEqual(first["unresolved_count"], 0)
            self.assertEqual(first["pending_failover_count"], 1)
            self.assertEqual(len(first["retry_request_paths"]), 1)

            child_path = root / first["retry_request_paths"][0]
            child = json.loads(child_path.read_text(encoding="utf-8"))
            self.assertEqual(child["provider"], "openalex")
            self.assertIn("https://api.openalex.org/works?search=", child["source_url"])
            self.assertIn("LLM+inference+offloading+memory", child["source_url"])
            self.assertEqual(child["provider_failover_parent_request_id"], request_id)
            self.assertEqual(child["run_key"], "run-1")
            self.assertEqual(child["worker_id"], "scheduled-chat-00")

            write_json(
                root / mod.RESULT_ROOT / f"{child['request_id']}.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "ok": True,
                    "request_id": child["request_id"],
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                },
            )
            verified = mod.recover(
                root,
                [Path(mod.REQUEST_ROOT) / f"{request_id}.json"],
                create=False,
            )
            self.assertEqual(verified["unresolved_count"], 0)
            self.assertEqual(verified["pending_failover_count"], 0)
            self.assertEqual(verified["rows"][0]["status"], "recovered_by_provider_failover")

    def test_citation_failure_is_not_rerouted_to_normal_provider(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_id = "citation-failed"
            write_json(
                root / mod.REQUEST_ROOT / f"{request_id}.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": request_id,
                    "collector_id": "forward-citation",
                    "run_key": "run-2",
                    "axis": "forward citations",
                    "provider": "semantic_scholar",
                    "source_url": (
                        "https://api.semanticscholar.org/graph/v1/paper/"
                        + "a" * 40
                        + "/citations"
                    ),
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 2,
                },
            )
            write_json(
                root / mod.RESULT_ROOT / f"{request_id}.json",
                {
                    "ok": False,
                    "request_id": request_id,
                    "decision": "FIX_REQUEST",
                    "error": "DiscoveryProviderError: Semantic Scholar page fetch failed at offset 0: HTTP Error 429",
                },
            )
            result = mod.recover(
                root,
                [Path(mod.REQUEST_ROOT) / f"{request_id}.json"],
                create=True,
            )
            self.assertEqual(result["pending_failover_count"], 0)
            self.assertEqual(result["unresolved_count"], 1)
            self.assertEqual(list((root / mod.REQUEST_ROOT).glob("auto-provider-failover-*.json")), [])


if __name__ == "__main__":
    unittest.main()
