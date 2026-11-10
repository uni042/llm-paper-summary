#!/usr/bin/env python3
"""Durable six-dimensional Discovery search-window history helpers."""
from __future__ import annotations

import hashlib
import json
from typing import Any


WINDOW_DIMENSIONS = (
    "topic",
    "source",
    "date_range",
    "category",
    "citation_direction",
    "query_family",
)
DEFAULT_DIMENSION = "*"
DEFAULT_RECENT_LIMIT = 96
HIGH_DUPLICATE_COOLDOWN_THRESHOLD = 0.80


def _norm_dimension(value: Any) -> str:
    if value is None:
        return DEFAULT_DIMENSION
    if isinstance(value, (list, tuple, set)):
        values = sorted({str(item).strip().casefold() for item in value if str(item).strip()})
        return ",".join(values) or DEFAULT_DIMENSION
    text = str(value).strip().casefold()
    return text or DEFAULT_DIMENSION


def _count(value: Any) -> int:
    try:
        return max(int(value or 0), 0)
    except (TypeError, ValueError):
        return 0


def _last_position(window: dict[str, Any]) -> Any:
    if window.get("position") is not None:
        return window.get("position")
    position = {
        field: window.get(field)
        for field in ("cursor", "next_cursor", "offset", "page")
        if window.get(field) is not None
    }
    return position or None


def normalize_search_window(window: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(window, dict):
        raise TypeError("search window must be an object")
    normalized = {field: _norm_dimension(window.get(field)) for field in WINDOW_DIMENSIONS}
    raw = _count(window.get("raw_result_count"))
    unseen = min(_count(window.get("unseen_result_count")), raw) if raw else 0
    duplicate = min(_count(window.get("duplicate_filtered_count")), raw) if raw else 0
    rejection = min(_count(window.get("rejection_filtered_count")), raw) if raw else 0
    evaluated = _count(window.get("candidate_evaluation_count"))
    accepted = min(_count(window.get("candidate_accepted_count")), evaluated) if evaluated else 0
    normalized.update(
        {
            "raw_result_count": raw,
            "unseen_result_count": unseen,
            "duplicate_filtered_count": duplicate,
            "rejection_filtered_count": rejection,
            "candidate_evaluation_count": evaluated,
            "candidate_accepted_count": accepted,
            "last_position": _last_position(window),
        }
    )
    return normalized


def search_window_key(window: dict[str, Any]) -> str:
    normalized = normalize_search_window(window)
    payload = {field: normalized[field] for field in WINDOW_DIMENSIONS}
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:20]
    return "window-" + digest


def _refresh_rates(row: dict[str, Any]) -> None:
    raw_total = _count(row.get("raw_result_count"))
    evaluated_total = _count(row.get("candidate_evaluation_count"))
    row["unseen_rate"] = (_count(row.get("unseen_result_count")) / raw_total) if raw_total else 0.0
    row["duplicate_rate"] = (_count(row.get("duplicate_filtered_count")) / raw_total) if raw_total else 0.0
    row["candidate_acceptance_rate"] = (
        _count(row.get("candidate_accepted_count")) / evaluated_total
        if evaluated_total else 0.0
    )
    row["cooldown"] = bool(
        raw_total > 0
        and row["duplicate_rate"] >= HIGH_DUPLICATE_COOLDOWN_THRESHOLD
    )


def record_search_windows(
    state: dict[str, Any],
    windows: list[dict[str, Any]],
    *,
    run_key: str | None,
    round_name: str | None,
    recent_limit: int = DEFAULT_RECENT_LIMIT,
) -> bool:
    """Aggregate observed search windows into the durable Discovery state."""
    if not isinstance(state, dict):
        raise TypeError("state must be an object")
    if not isinstance(windows, list) or any(not isinstance(window, dict) for window in windows):
        raise TypeError("windows must be a list of objects")
    if recent_limit < 1:
        raise ValueError("recent_limit must be positive")
    if not windows:
        return False

    aggregate = state.get("search_windows") if isinstance(state.get("search_windows"), dict) else {}
    recent = state.get("recent_search_windows") if isinstance(state.get("recent_search_windows"), list) else []

    for raw_window in windows:
        window = normalize_search_window(raw_window)
        key = search_window_key(window)
        row = aggregate.get(key) if isinstance(aggregate.get(key), dict) else {}
        if not row:
            row = {field: window[field] for field in WINDOW_DIMENSIONS}
            row.update(
                {
                    "search_window_key": key,
                    "scan_count": 0,
                    "raw_result_count": 0,
                    "unseen_result_count": 0,
                    "duplicate_filtered_count": 0,
                    "rejection_filtered_count": 0,
                    "candidate_evaluation_count": 0,
                    "candidate_accepted_count": 0,
                    "last_position": None,
                }
            )
        row["scan_count"] = _count(row.get("scan_count")) + 1
        for field in (
            "raw_result_count",
            "unseen_result_count",
            "duplicate_filtered_count",
            "rejection_filtered_count",
            "candidate_evaluation_count",
            "candidate_accepted_count",
        ):
            row[field] = _count(row.get(field)) + window[field]
        if window["last_position"] is not None:
            row["last_position"] = window["last_position"]
        _refresh_rates(row)
        row["last_run_key"] = run_key
        row["last_round"] = round_name
        aggregate[key] = row

        event = {field: window[field] for field in WINDOW_DIMENSIONS}
        event.update(
            {
                "search_window_key": key,
                "run_key": run_key,
                "round": round_name,
                "raw_result_count": window["raw_result_count"],
                "unseen_result_count": window["unseen_result_count"],
                "duplicate_filtered_count": window["duplicate_filtered_count"],
                "rejection_filtered_count": window["rejection_filtered_count"],
                "candidate_evaluation_count": window["candidate_evaluation_count"],
                "candidate_accepted_count": window["candidate_accepted_count"],
                "unseen_rate": (
                    window["unseen_result_count"] / window["raw_result_count"]
                    if window["raw_result_count"] else 0.0
                ),
                "duplicate_rate": (
                    window["duplicate_filtered_count"] / window["raw_result_count"]
                    if window["raw_result_count"] else 0.0
                ),
                "candidate_acceptance_rate": (
                    window["candidate_accepted_count"] / window["candidate_evaluation_count"]
                    if window["candidate_evaluation_count"] else 0.0
                ),
                "last_position": window["last_position"],
            }
        )
        recent.append(event)

    state["search_windows"] = aggregate
    state["recent_search_windows"] = recent[-recent_limit:]
    state["search_window_history_limit"] = recent_limit
    state["high_duplicate_cooldown_threshold"] = HIGH_DUPLICATE_COOLDOWN_THRESHOLD
    return True


def rank_search_windows(
    windows: list[dict[str, Any]],
    state: dict[str, Any],
) -> list[dict[str, Any]]:
    """Rank windows: unscanned first, then productive, high-duplicate windows last."""
    if not isinstance(windows, list) or any(not isinstance(window, dict) for window in windows):
        raise TypeError("windows must be a list of objects")
    aggregate = state.get("search_windows") if isinstance(state, dict) and isinstance(state.get("search_windows"), dict) else {}
    ranked: list[dict[str, Any]] = []
    for candidate in windows:
        normalized = normalize_search_window(candidate)
        key = search_window_key(normalized)
        saved = aggregate.get(key) if isinstance(aggregate.get(key), dict) else None
        scanned = saved is not None and _count(saved.get("scan_count")) > 0
        history = {
            "scanned": scanned,
            "scan_count": _count(saved.get("scan_count")) if saved else 0,
            "unseen_rate": float(saved.get("unseen_rate") or 0.0) if saved else None,
            "duplicate_rate": float(saved.get("duplicate_rate") or 0.0) if saved else None,
            "candidate_acceptance_rate": float(saved.get("candidate_acceptance_rate") or 0.0) if saved else None,
            "cooldown": bool(saved.get("cooldown")) if saved else False,
            "last_position": saved.get("last_position") if saved else None,
            "last_run_key": saved.get("last_run_key") if saved else None,
            "last_round": saved.get("last_round") if saved else None,
        }
        row = dict(candidate)
        for field in WINDOW_DIMENSIONS:
            row[field] = normalized[field]
        row["search_window_key"] = key
        row["history"] = history
        ranked.append(row)

    def priority(row: dict[str, Any]) -> tuple[Any, ...]:
        history = row["history"]
        if not history["scanned"]:
            return (0, 0.0, 0.0, 0.0, 0, row["search_window_key"])
        return (
            2 if history["cooldown"] else 1,
            -float(history["unseen_rate"] or 0.0),
            -float(history["candidate_acceptance_rate"] or 0.0),
            float(history["duplicate_rate"] or 0.0),
            int(history["scan_count"] or 0),
            row["search_window_key"],
        )

    return sorted(ranked, key=priority)
