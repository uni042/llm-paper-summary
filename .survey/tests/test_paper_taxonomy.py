from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from paper_taxonomy import (  # noqa: E402
    CANONICAL_INFERENCE_LINEAGES,
    DEFAULT_INFERENCE_LINEAGE,
    canonical_lineage,
    canonicalize_paper_path,
)


class PaperTaxonomyTests(unittest.TestCase):
    def test_known_legacy_inference_lineages_collapse_to_canonical_taxonomy(self) -> None:
        self.assertEqual(
            canonical_lineage("inference", "03-kv-cache"),
            "07-kv-cache-optimization-compression",
        )
        self.assertEqual(
            canonical_lineage("inference", "05-kv-cache-offloading"),
            "10-kv-cache-offload-recomputation",
        )
        self.assertEqual(
            canonical_lineage("inference", "06-serving-scheduling"),
            "11-llm-serving-scheduling-disaggregation",
        )
        self.assertEqual(
            canonical_lineage("inference", "04-moe-parallelism-communication"),
            "12-moe-parallelism-communication",
        )
        self.assertEqual(
            canonical_lineage("inference", "08-quantization-kernels"),
            "16-weight-quantization-compression",
        )
        self.assertEqual(
            canonical_lineage("inference", "05-pim-near-memory"),
            "17-pim-near-data-acceleration",
        )
        self.assertEqual(
            canonical_lineage("inference", "18-pipeline-native-cpu-inference"),
            "18-pipeline-native-cpu-inference",
        )

    def test_unknown_inference_lineage_falls_back_without_creating_another_taxonomy(self) -> None:
        self.assertEqual(
            canonical_lineage("inference", "37-worker-invented-lineage"),
            DEFAULT_INFERENCE_LINEAGE,
        )

    def test_non_inference_taxonomy_is_not_rewritten(self) -> None:
        self.assertEqual(
            canonical_lineage("training", "02-distributed-heterogeneous-moe-training"),
            "02-distributed-heterogeneous-moe-training",
        )

    def test_physical_inference_directories_are_canonical(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        actual = {path.name for path in (repo_root / "papers" / "inference").iterdir() if path.is_dir()}
        self.assertEqual(actual, set(CANONICAL_INFERENCE_LINEAGES))

    def test_candidate_paper_path_is_normalized_to_canonical_directory(self) -> None:
        self.assertEqual(
            canonicalize_paper_path("papers/inference/03-kv-cache/2026-example.md"),
            "papers/inference/07-kv-cache-optimization-compression/2026-example.md",
        )
        self.assertEqual(
            canonicalize_paper_path("papers/inference/new-unregistered-topic/2026-example.md"),
            "papers/inference/99-other-inference-systems/2026-example.md",
        )


if __name__ == "__main__":
    unittest.main()
