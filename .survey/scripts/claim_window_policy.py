#!/usr/bin/env python3
"""Central policy for Research/Audit inventory and dual-mode bank buffering.

Each canonical bank has two independent stock lanes:
- Research lane: logical preloaded paper ownership, sharded round-robin by pool order;
- Discovery lane: a prechecked search window, maintained independently.

The five writable Research record slots are a third, hot staging resource inside
the same bank identity. Cold Research stock does not reserve those slots. A worker
may own a deeper logical paper inventory while only the leading hot slice consumes
record-slot capacity.
"""
from __future__ import annotations

EXPECTED_PARALLEL_WORKERS = 6

# Logical paper inventory held by each worker. Only the foreground is read at once.
DEFAULT_CLAIM_WINDOW = 12
MAX_CLAIM_WINDOW = 24

# Leading assignments kept bank-ready. Six workers therefore use at most 24 of the
# current 32 banks for ordinary hot work, leaving the rest for repair/exception use.
HOT_BANKED_CLAIMS = 4

# Keep a second complete six-worker inventory in the shared pool. In Research mode
# the routing threshold guarantees enough candidate depth for this without coupling
# the paper stock to record-bank capacity.
SHARED_PRELOAD_TARGET = (
    DEFAULT_CLAIM_WINDOW * EXPECTED_PARALLEL_WORKERS * 2
)

# Switch to Discovery before Research stock gets close to one full six-worker load.
# User policy: four times the inventory six workers can comfortably hold.
RESEARCH_DISCOVERY_THRESHOLD = (
    DEFAULT_CLAIM_WINDOW * EXPECTED_PARALLEL_WORKERS * 4
)


def normalize_window(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("claim window must be an integer")
    if not 1 <= value <= MAX_CLAIM_WINDOW:
        raise ValueError(f"claim window must be between 1 and {MAX_CLAIM_WINDOW}")
    return value


def hot_banked_claims(window: int) -> int:
    """Return how many leading assignments should be immediately bank-ready."""
    window = normalize_window(window)
    return min(HOT_BANKED_CLAIMS, window)


def refill_threshold(window: int) -> int:
    """Trigger refill while half of the hot bank-ready slice is still available.

    With the default 12-paper inventory and four hot banked claims, refill begins at
    ten remaining assignments: two hot papers are still immediately runnable while
    the asynchronous claim/bank promotion catches up.
    """
    window = normalize_window(window)
    hot = hot_banked_claims(window)
    if window <= 1:
        return 0
    refill_after = max(1, hot // 2)
    return max(1, window - refill_after)


def should_refill(
    active_claim_count: int,
    window: int,
    *,
    threshold: int | None = None,
) -> bool:
    window = normalize_window(window)
    count = max(int(active_claim_count), 0)
    mark = refill_threshold(window) if threshold is None else max(
        0, min(int(threshold), window - 1)
    )
    return 0 < count < window and count <= mark


def shared_pool_target() -> int:
    """Return the logical preload target; this is deliberately bank-independent."""
    return SHARED_PRELOAD_TARGET
