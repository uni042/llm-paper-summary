#!/usr/bin/env python3
"""Deterministic selector for the next Discovery citation direction and known seed.

This helper intentionally decides only *where to search next*. Candidate relevance,
importance and priority remain research judgement.

Policy:
1. Within one run, complete backward citation before forward citation.
2. After both directions are durably represented, compare recent yield.
3. Penalize duplicate-heavy and consecutive empty windows.
4. If both latest same-run citation windows produced no novel/accepted papers, permit
   normal/new search as a gap-filling round.
5. For a direction, select the highest-yield seed among rows that durably record a
   seed identity; ties are canonical-id lexical order. If no seed history exists,
   callers choose the first canonical id from their current eligible seed pool.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DIRECTIONS = ("backward", "forward")


def _read(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _direction(row: dict[str, Any]) -> str | None:
    explicit = str(row.get("citation_direction") or "").strip().lower()
    if explicit in DIRECTIONS:
        return explicit
    text = " ".join(
        str(row.get(key) or "")
        for key in ("round", "axis", "query_summary", "source_submission")
    ).lower()
    if any(token in text for token in ("backward", "reference", "references", "後方引用")):
        return "backward"
    if any(token in text for token in ("forward", "citation", "citations", "被引用", "前方引用")):
        return "forward"
    return None


def _seed(row: dict[str, Any]) -> str | None:
    for key in ("seed_canonical_id", "seed_id", "seed"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    stats = row.get("search_window")
    if isinstance(stats, dict):
        for key in ("seed_canonical_id", "seed_id", "seed"):
            value = stats.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _accepted(row: dict[str, Any]) -> int:
    value = row.get("accepted_count", 0)
    return max(int(value), 0) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


def _novel(row: dict[str, Any]) -> int:
    for key in ("novel_candidate_count", "unseen_result_count"):
        value = row.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return max(int(value), 0)
    return 0


def _duplicate_ratio(row: dict[str, Any]) -> float:
    for key in ("final_duplicate_ratio", "duplicate_ratio"):
        value = row.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return min(max(float(value), 0.0), 1.0)
    return 0.0


def _row_score(row: dict[str, Any]) -> float:
    # Route-selection score only. This is deliberately separate from Candidate priority.
    return (4.0 * _accepted(row)) + (1.0 * _novel(row)) - (2.0 * _duplicate_ratio(row))


def _empty_streak(rows: list[dict[str, Any]], direction: str) -> int:
    streak = 0
    for row in reversed(rows):
        if _direction(row) != direction:
            continue
        if _accepted(row) == 0 and _novel(row) == 0:
            streak += 1
            continue
        break
    return streak


def _direction_score(rows: list[dict[str, Any]], direction: str) -> float:
    recent = [row for row in rows if _direction(row) == direction][-8:]
    if not recent:
        return 0.0
    score = sum(_row_score(row) for row in recent) / len(recent)
    return score - (2.0 * min(_empty_streak(rows, direction), 3))


def _best_seed(rows: list[dict[str, Any]], direction: str) -> str | None:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if _direction(row) != direction:
            continue
        seed = _seed(row)
        if seed:
            grouped.setdefault(seed, []).append(row)
    if not grouped:
        return None

    scored: list[tuple[float, str]] = []
    for seed, seed_rows in grouped.items():
        base = sum(_row_score(row) for row in seed_rows[-6:]) / min(len(seed_rows), 6)
        empty = 0
        for row in reversed(seed_rows):
            if _accepted(row) == 0 and _novel(row) == 0:
                empty += 1
            else:
                break
        scored.append((base - (2.0 * min(empty, 3)), seed))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored[0][1]


def decide(state: dict[str, Any], run_key: str) -> dict[str, Any]:
    history = state.get("history")
    rows = [row for row in history if isinstance(row, dict)] if isinstance(history, list) else []
    same_run = [row for row in rows if str(row.get("run_key") or "") == run_key]
    attempted = {_direction(row) for row in same_run}
    attempted.discard(None)

    if "backward" not in attempted:
        direction = "backward"
        reason = "same_run_backward_missing"
    elif "forward" not in attempted:
        direction = "forward"
        reason = "same_run_forward_missing"
    else:
        latest_by_direction: dict[str, dict[str, Any] | None] = {
            direction: next((row for row in reversed(same_run) if _direction(row) == direction), None)
            for direction in DIRECTIONS
        }
        both_empty = all(
            row is not None and _accepted(row) == 0 and _novel(row) == 0
            for row in latest_by_direction.values()
        )
        if both_empty:
            direction = "normal"
            reason = "citation_pair_latest_windows_empty_gap_fill_allowed"
        else:
            scores = {d: _direction_score(rows, d) for d in DIRECTIONS}
            if scores["backward"] > scores["forward"]:
                direction = "backward"
                reason = "historical_yield_score"
            elif scores["forward"] > scores["backward"]:
                direction = "forward"
                reason = "historical_yield_score"
            else:
                last = next((_direction(row) for row in reversed(same_run) if _direction(row) in DIRECTIONS), None)
                direction = "forward" if last == "backward" else "backward"
                reason = "yield_tie_alternate_direction"

    seed = _best_seed(rows, direction) if direction in DIRECTIONS else None
    return {
        "schema_version": 1,
        "run_key": run_key,
        "next_direction": direction,
        "reason": reason,
        "same_run_attempted_directions": sorted(attempted),
        "historical_direction_scores": {d: _direction_score(rows, d) for d in DIRECTIONS},
        "selected_seed_canonical_id": seed,
        "seed_fallback": (
            None if seed is not None or direction == "normal"
            else "Use the lexicographically first canonical_id from the current eligible seed pool."
        ),
        "rule": (
            "This selector controls Discovery route order only. It does not score Candidate quality. "
            "Candidate base/lineage/recency/venue judgement remains governed by worker-router.md."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=Path(".survey/work-queue/discovery-state.json"))
    parser.add_argument("--run-key", required=True)
    args = parser.parse_args()
    print(json.dumps(decide(_read(args.state), args.run_key), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided
    raise SystemExit(run_guided(main, script=__file__))
