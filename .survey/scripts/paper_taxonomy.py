#!/usr/bin/env python3
"""Canonical paper-taxonomy helpers shared by queue ingestion and derived indexes.

Historical Inference lineage names are accepted only as compatibility aliases
for stale jobs and references. Physical repository storage uses the canonical
taxonomy, and new Discovery candidates are normalized before Research jobs are
created so directory fragmentation does not grow again.
"""
from __future__ import annotations

from pathlib import PurePosixPath


DEFAULT_INFERENCE_LINEAGE = "99-other-inference-systems"

CANONICAL_INFERENCE_LINEAGES = (
    "01-offload-hierarchical-memory",
    "02-adaptive-expert-computation-compression",
    "03-expert-prefetch",
    "04-conditional-computation",
    "05-speculative-decoding-moe",
    "06-moe-quantization-compression",
    "07-kv-cache-optimization-compression",
    "08-edge-on-device-llm-systems",
    "10-kv-cache-offload-recomputation",
    "11-llm-serving-scheduling-disaggregation",
    DEFAULT_INFERENCE_LINEAGE,
)

INFERENCE_LINEAGE_ALIASES = {
    "02-cpu-offload": "01-offload-hierarchical-memory",
    "02-memory-offload": "01-offload-hierarchical-memory",
    "02-moe-expert-placement-caching": "01-offload-hierarchical-memory",
    "02-moe-offload": "01-offload-hierarchical-memory",
    "03-hierarchical-memory": "01-offload-hierarchical-memory",
    "03-moe-expert-offload": "01-offload-hierarchical-memory",
    "03-offload-hierarchical-memory": "01-offload-hierarchical-memory",
    "04-cpu-ssd-offload": "01-offload-hierarchical-memory",
    "04-moe-expert-offload-caching": "01-offload-hierarchical-memory",
    "04-moe-offload-expert-cache": "01-offload-hierarchical-memory",
    "04-moe-offload-routing": "01-offload-hierarchical-memory",
    "04-offload-heterogeneous": "01-offload-hierarchical-memory",
    "05-moe-expert-offload": "01-offload-hierarchical-memory",
    "05-offload-hierarchical-memory": "01-offload-hierarchical-memory",
    "06-expert-offloading": "01-offload-hierarchical-memory",
    "06-moe-expert-offloading": "01-offload-hierarchical-memory",
    "06-moe-inference-expert-offloading": "01-offload-hierarchical-memory",
    "06-moe-inference-expert-placement-caching": "01-offload-hierarchical-memory",

    "05-speculative-decoding": "05-speculative-decoding-moe",
    "06-speculative-decoding": "05-speculative-decoding-moe",
    "06-speculative-decoding-moe": "05-speculative-decoding-moe",
    "07-speculative-decoding": "05-speculative-decoding-moe",
    "08-speculative-decoding": "05-speculative-decoding-moe",

    "03-kv-cache": "07-kv-cache-optimization-compression",
    "04-kv-cache": "07-kv-cache-optimization-compression",
    "05-kv-cache": "07-kv-cache-optimization-compression",
    "05-kv-cache-compression-quantization": "07-kv-cache-optimization-compression",
    "05-kv-cache-memory-management": "07-kv-cache-optimization-compression",
    "06-kv-cache-memory": "07-kv-cache-optimization-compression",
    "kv-cache": "07-kv-cache-optimization-compression",

    "05-kv-cache-offloading": "10-kv-cache-offload-recomputation",

    "04-kv-prefix-cache": "11-llm-serving-scheduling-disaggregation",
    "06-serving-scheduling": "11-llm-serving-scheduling-disaggregation",
    "scheduling": "11-llm-serving-scheduling-disaggregation",

    # These historical topics do not match one canonical lineage precisely.
    "02-hardware-accelerators": DEFAULT_INFERENCE_LINEAGE,
    "02-moe-inference": DEFAULT_INFERENCE_LINEAGE,
    "04-moe-parallelism-communication": DEFAULT_INFERENCE_LINEAGE,
    "05-memory-architecture-near-data": DEFAULT_INFERENCE_LINEAGE,
    "05-moe": DEFAULT_INFERENCE_LINEAGE,
    "05-pim-near-memory": DEFAULT_INFERENCE_LINEAGE,
    "08-quantization-kernels": DEFAULT_INFERENCE_LINEAGE,
    "09-attention-kernel-serving-optimization": DEFAULT_INFERENCE_LINEAGE,
    "09-kernel-runtime-compilation": DEFAULT_INFERENCE_LINEAGE,
    "10-sparse-attention": DEFAULT_INFERENCE_LINEAGE,
    "12-benchmarking-modeling-emulation": DEFAULT_INFERENCE_LINEAGE,
    "moe": DEFAULT_INFERENCE_LINEAGE,
    "09-other-inference-systems": DEFAULT_INFERENCE_LINEAGE,
}


def canonical_lineage(family: str, lineage: str) -> str:
    """Return the stable user-facing lineage for one physical paper directory."""
    name = str(lineage or "").strip()
    if family != "inference":
        return name
    if name in CANONICAL_INFERENCE_LINEAGES:
        return name
    return INFERENCE_LINEAGE_ALIASES.get(name, DEFAULT_INFERENCE_LINEAGE)


def canonicalize_paper_path(value: str) -> str:
    """Normalize only the lineage segment of an Inference paper path."""
    path = PurePosixPath(str(value))
    parts = list(path.parts)
    if len(parts) >= 4 and tuple(parts[:2]) == ("papers", "inference"):
        parts[2] = canonical_lineage("inference", parts[2])
        return PurePosixPath(*parts).as_posix()
    return path.as_posix()
