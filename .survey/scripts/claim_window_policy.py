#!/usr/bin/env python3
"""Central policy for Research/Audit claim-window buffering.

Only one paper is read at a time. The claim window controls how many assignments
are reserved ahead of foreground work. Refill uses a low-watermark so a burst of
quick blocked/deferred papers can be absorbed without making claim-result latency
a foreground barrier.
"""
from __future__ import annotations

DEFAULT_CLAIM_WINDOW = 8
MAX_CLAIM_WINDOW = 10
REFILL_NUMERATOR = 1
REFILL_DENOMINATOR = 2
SHARED_POOL_HEADROOM_NUMERATOR = 1
SHARED_POOL_HEADROOM_DENOMINATOR = 4


def normalize_window(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("claim window must be an integer")
    if not 1 <= value <= MAX_CLAIM_WINDOW:
        raise ValueError(f"claim window must be between 1 and {MAX_CLAIM_WINDOW}")
    return value


def refill_threshold(window: int) -> int:
    """Return the active-claim low-watermark that triggers one asynchronous refill."""
    window = normalize_window(window)
    if window <= 1:
        return 0
    threshold = (window * REFILL_NUMERATOR) // REFILL_DENOMINATOR
    return max(1, min(threshold, window - 1))


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


def shared_pool_target(bank_count: int) -> int:
    """Derive normal preload capacity while retaining proportional repair headroom."""
    count = max(int(bank_count), 0)
    if count <= 1:
        return 0
    headroom = max(
        1,
        (count * SHARED_POOL_HEADROOM_NUMERATOR + SHARED_POOL_HEADROOM_DENOMINATOR - 1)
        // SHARED_POOL_HEADROOM_DENOMINATOR,
    )
    return max(count - headroom, 0)
