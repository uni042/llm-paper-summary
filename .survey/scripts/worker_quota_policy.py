#!/usr/bin/env python3
"""Canonical per-run work quotas for survey workers.

These values are execution-policy constants, not scheduling-capacity limits.
Keep the Research/Audit completion floor and Discovery round floor separate from
the Audit starvation block size: the latter controls mix/fairness, not run
completion.
"""
from __future__ import annotations

RESEARCH_AUDIT_MINIMUM_COMPLETIONS = 5
DISCOVERY_MINIMUM_ROUNDS = 8

# Fairness policy only. This is intentionally independent of the five-completion
# Research/Audit run floor.
AUDIT_STARVATION_BLOCK_SIZE = 3

def order_with_audit_fairness(
    rows: list[dict],
    *,
    starting_position: int = 0,
    prior_kinds: tuple[str, ...] | list[str] = (),
    kind_field: str = "kind",
    limit: int | None = None,
    reserve_missing_audit_slot: bool = False,
) -> list[dict]:
    """Preserve source order except when the closing slot of a 3-item block needs Audit.

    starting_position is zero-based in the worker pipeline. prior_kinds contains
    the already-owned kinds in the current block before that position. If an Audit is
    available among rows, the earliest one is pulled forward into the block-closing
    slot. When reserve_missing_audit_slot is true and no Audit exists in this source,
    selection stops before filling that slot so a later source can supply an Audit.
    """
    remaining = list(rows)
    selected: list[dict] = []
    cap = len(remaining) if limit is None else max(int(limit), 0)
    block_size = AUDIT_STARVATION_BLOCK_SIZE
    position_in_block = max(int(starting_position), 0) % block_size
    audit_seen = any(str(kind).lower() == "audit" for kind in prior_kinds)

    while remaining and len(selected) < cap:
        closes_block = position_in_block == block_size - 1
        chosen_index = 0
        if closes_block and not audit_seen:
            audit_index = next(
                (
                    index
                    for index, row in enumerate(remaining)
                    if str(row.get(kind_field) or "").lower() == "audit"
                ),
                None,
            )
            if audit_index is None:
                if reserve_missing_audit_slot:
                    break
            else:
                chosen_index = audit_index

        row = remaining.pop(chosen_index)
        selected.append(row)
        if str(row.get(kind_field) or "").lower() == "audit":
            audit_seen = True

        position_in_block += 1
        if position_in_block >= block_size:
            position_in_block = 0
            audit_seen = False

    return selected
