#!/usr/bin/env python3
"""Central policy for Research/Audit paper inventory and hot bank buffering.

Paper ownership and record-bank capacity are intentionally separate layers:
- a worker may own a deeper logical paper inventory;
- only the leading hot slice needs record banks immediately;
- the shared paper preload pool is sized independently from record-bank count.

This keeps allocation latency low without turning every standby paper into a bank
reservation.
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
    """Trigger refill early enough to preserve the hot bank-ready slice.

    For the default 12-paper inventory with a four-paper hot slice, refill begins at
    nine remaining assignments. That means the refill/bank-promotion request starts
    while one previously hot paper is still available, rather than after all four
    hot assignments have been consumed.
    """
    window = normalize_window(window)
    hot = hot_banked_claims(window)
    if window <= 1:
        return 0
    return max(1, window - hot + 1)


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
