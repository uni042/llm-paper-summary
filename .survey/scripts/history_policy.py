#!/usr/bin/env python3
"""Shared retention policy for durable survey dashboard histories."""
from __future__ import annotations

from typing import Any

MIN_HISTORY_LIMIT = 384


def normalize_history_limit(value: Any) -> int:
    """Preserve larger explicit limits while enforcing the dashboard minimum."""
    if isinstance(value, int) and not isinstance(value, bool) and value >= MIN_HISTORY_LIMIT:
        return value
    return MIN_HISTORY_LIMIT
