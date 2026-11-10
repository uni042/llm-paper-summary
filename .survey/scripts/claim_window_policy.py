#!/usr/bin/env python3
"""Central policy for Research/Audit inventory on dual-purpose banks.

Each canonical bank can simultaneously hold a Research preload sidecar, a Discovery
preload sidecar, and the five writable Research/Audit record slots. The sidecars are
independent derived stock indexes; only the leading hot Research slice reserves the
five record slots. This keeps allocation latency low without turning every standby
paper into a record-slot reservation.
"""
from __future__ import annotations

# Capacity-sizing baseline only; this is not a worker-count admission limit.
# Additional worker-N identities remain valid and share the same canonical pool.
EXPECTED_PARALLEL_WORKERS = 6

# Logical paper inventory held by each worker. Only the foreground is read at once.
DEFAULT_CLAIM_WINDOW = 12
MAX_CLAIM_WINDOW = 24

# Leading assignments kept bank-ready. Six workers therefore use at most 24 of the
# current 32 banks for ordinary hot work, leaving the rest for repair/exception use.
HOT_BANKED_CLAIMS = 4

# Keep a second complete six-worker Research inventory in the shared pool.
# This stock is maintained independently of the current Research/Discovery route;
# dual-purpose banks can hold Research and Discovery preload state simultaneously.
SHARED_PRELOAD_TARGET = (
    DEFAULT_CLAIM_WINDOW * EXPECTED_PARALLEL_WORKERS * 2
)

# Switch to Discovery before Research stock gets close to one full six-worker load.
# User policy: four times the inventory six workers can comfortably hold.
RESEARCH_DISCOVERY_THRESHOLD = (
    DEFAULT_CLAIM_WINDOW * EXPECTED_PARALLEL_WORKERS * 4
)

# Do not let a continuously healthy Research backlog starve Discovery forever.
# Once a verified Discovery round is this old, one new invocation may route to
# Discovery while Research stock remains within one extra six-worker window above
# the ordinary threshold. A very large Research backlog still wins.
DISCOVERY_REFRESH_INTERVAL_SECONDS = 2 * 60 * 60
DISCOVERY_REFRESH_MAX_INVENTORY = (
    RESEARCH_DISCOVERY_THRESHOLD
    + DEFAULT_CLAIM_WINDOW * EXPECTED_PARALLEL_WORKERS
)


def discovery_refresh_due(
    candidate_inventory: int,
    *,
    discovery_age_seconds: int | float | None,
) -> bool:
    if isinstance(candidate_inventory, bool) or not isinstance(candidate_inventory, int):
        raise ValueError("candidate inventory must be an integer")
    inventory = max(candidate_inventory, 0)
    if discovery_age_seconds is None:
        return False
    age = max(float(discovery_age_seconds), 0.0)
    return (
        age >= DISCOVERY_REFRESH_INTERVAL_SECONDS
        and inventory <= DISCOVERY_REFRESH_MAX_INVENTORY
    )


def select_work_mode(
    candidate_inventory: int,
    *,
    discovery_age_seconds: int | float | None = None,
) -> str:
    """Choose Research or Discovery with a bounded Discovery freshness override."""
    if isinstance(candidate_inventory, bool) or not isinstance(candidate_inventory, int):
        raise ValueError("candidate inventory must be an integer")
    inventory = max(candidate_inventory, 0)
    if inventory < RESEARCH_DISCOVERY_THRESHOLD:
        return "discovery"
    if discovery_refresh_due(
        inventory,
        discovery_age_seconds=discovery_age_seconds,
    ):
        return "discovery"
    return "research"


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
    """Return the logical Research preload target sharded across all bank identities."""
    return SHARED_PRELOAD_TARGET
