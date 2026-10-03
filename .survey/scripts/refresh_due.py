#!/usr/bin/env python3
"""Small durable freshness gate for event-driven workflow fallbacks."""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def _parse(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def is_due(path: Path, *, max_age_seconds: int, now: dt.datetime | None = None) -> bool:
    if max_age_seconds < 0:
        raise ValueError("max_age_seconds must be >= 0")
    now = now or dt.datetime.now(dt.timezone.utc)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return True
    if not isinstance(payload, dict):
        return True
    updated = _parse(payload.get("updated_at"))
    if updated is None:
        return True
    return (now - updated).total_seconds() >= max_age_seconds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--max-age-seconds", type=int, required=True)
    args = parser.parse_args()
    print("true" if is_due(args.state, max_age_seconds=args.max_age_seconds) else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
