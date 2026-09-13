#!/usr/bin/env python3
"""Append research-throughput and claim-health metrics to STATUS.md."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

START = "<!-- research-throughput-status:start -->"
END = "<!-- research-throughput-status:end -->"
HIGH_BACKLOG = 25
LOW_COMPLETIONS = 2
TARGET_COMPLETIONS = 3


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _latest_run(entries: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [entry for entry in entries if isinstance(entry, dict)]
    if not valid:
        return {}
    return max(
        valid,
        key=lambda entry: _dt(entry.get("run_key") or entry.get("last_recorded_at"))
        or datetime.min.replace(tzinfo=timezone.utc),
    )


def _research_completed_24h(entries: list[dict[str, Any]], now: datetime) -> int:
    cutoff = now - timedelta(hours=24)
    total = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        when = _dt(entry.get("run_key") or entry.get("last_recorded_at"))
        if when is None or when < cutoff or when > now:
            continue
        total += int((entry.get("counts") or {}).get("research_completed") or 0)
    return total


def _oldest_active_claim_age(repo_root: Path, now: datetime) -> int | None:
    claims_dir = repo_root / ".survey/work-queue/claims"
    ages: list[int] = []
    for path in sorted(claims_dir.glob("*.json")) if claims_dir.is_dir() else []:
        claim = _load(path)
        expires = _dt(claim.get("expires_at"))
        if expires is None or expires <= now:
            continue
        activity = _dt(claim.get("heartbeat_at") or claim.get("claimed_at"))
        if activity is None or activity > now:
            continue
        ages.append(max(0, int((now - activity).total_seconds() // 60)))
    return max(ages) if ages else None


def render_section(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    queue = _load(repo_root / ".survey/work-queue/next-jobs.json")
    ledger = _load(repo_root / ".survey/work-queue/run-ledger.json")
    research = ((queue.get("counts") or {}).get("research") or {})
    claiming = queue.get("claiming") or {}
    entries = [entry for entry in (ledger.get("entries") or []) if isinstance(entry, dict)]
    latest = _latest_run(entries)

    ready = int(research.get("ready") or 0)
    active = int(claiming.get("actively_claimed") or 0)
    claimable = int(claiming.get("claimable") or 0)
    latest_completed = int((latest.get("counts") or {}).get("research_completed") or 0)
    completed_24h = _research_completed_24h(entries, now)
    oldest_age = _oldest_active_claim_age(repo_root, now)
    high_backlog = ready >= HIGH_BACKLOG and (active + claimable) > 0

    mode = "HIGH-BACKLOG RESEARCH-ONLY" if high_backlog else "NORMAL"
    health = "OK"
    warning = ""
    if high_backlog and latest and latest_completed < LOW_COMPLETIONS:
        health = "LOW"
        warning = (
            f"- **Research throughput LOW**: ready={ready} の高在庫状態で、"
            f"最新runのresearch完了は {latest_completed} 件です。探索へ逃げずresearchを継続してください。\n"
        )

    age_text = "—" if oldest_age is None else f"{oldest_age} min"
    run_key = str(latest.get("run_key") or "—")
    return (
        f"{START}\n"
        "## Research throughput health\n\n"
        f"Mode: **{mode}** / Health: **{health}**\n\n"
        "| 指標 | 値 |\n"
        "|---|---:|\n"
        f"| Research ready | **{ready}** |\n"
        f"| Active claims | **{active}** |\n"
        f"| Claimable | **{claimable}** |\n"
        f"| Latest normal run | **{run_key}** |\n"
        f"| Latest research completed | **{latest_completed}** |\n"
        f"| Research completed (24h) | **{completed_24h}** |\n"
        f"| Oldest active claim age | **{age_text}** |\n\n"
        f"高在庫モードでは、hard stopに達しない限り通常runの下限目標は **最低{TARGET_COMPLETIONS}件**。"
        "3件は上限・終了条件ではありません。\n\n"
        f"{warning}"
        f"{END}\n"
    )


def append_section(repo_root: Path, status_path: Path, now: datetime | None = None) -> None:
    section = render_section(repo_root, now=now)
    try:
        text = status_path.read_text(encoding="utf-8")
    except OSError:
        text = ""

    if START in text and END in text:
        prefix, rest = text.split(START, 1)
        _, suffix = rest.split(END, 1)
        text = prefix.rstrip() + "\n\n" + section + suffix.lstrip("\n")
    else:
        text = text.rstrip() + "\n\n" + section
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--status", type=Path, default=Path("STATUS.md"))
    args = parser.parse_args()
    append_section(args.repo_root, args.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
