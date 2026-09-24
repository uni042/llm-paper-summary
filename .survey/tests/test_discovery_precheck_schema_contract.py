from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_discovery_precheck as precheck  # noqa: E402


def request(schema_version: int) -> dict:
    return {
        "schema_version": schema_version,
        "operation": "precheck_discovery_candidates",
        "request_id": "schema-contract-test",
        "collector_id": "schema-contract",
        "run_key": "schema-contract-run",
        "axis": "schema-contract",
        "provider": "repository_references",
        "source_url": "repository://structured-references",
        "target_unseen": 20,
    }


class DiscoveryPrecheckSchemaContractTests(unittest.TestCase):
    def test_schema_v3_is_the_only_executable_request_schema(self) -> None:
        normalized = precheck._validate_request(request(3))
        self.assertEqual(normalized["schema_version"], 3)
        self.assertEqual(normalized["provider"], "repository_references")

    def test_legacy_schema_v2_request_is_rejected_with_migration_guidance(self) -> None:
        payload = request(2)
        payload["records"] = []
        payload["provider_has_more"] = False
        with self.assertRaises(precheck.DiscoveryPrecheckRequestError) as ctx:
            precheck._validate_request(payload)
        self.assertIn("exactly 3", str(ctx.exception))
        self.assertIn("legacy", str(ctx.exception).lower())

    def test_unknown_future_schema_is_not_silently_treated_as_v3(self) -> None:
        with self.assertRaises(precheck.DiscoveryPrecheckRequestError) as ctx:
            precheck._validate_request(request(4))
        self.assertIn("exactly 3", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
