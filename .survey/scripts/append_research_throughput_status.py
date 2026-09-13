#!/usr/bin/env python3
"""Append research-throughput, worker-routing, and claim-health metrics to STATUS.md."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

START = "<!-- research-throughput-status:start -->"
END = "<!-- research-throughput-status:end -->"
HIGH_BACKLOG = 25
CRITICAL_WATERMARK = 15
SPECIALIST_RESEARCH_SWITCH = 50
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
    auxiliary_mode = (
        "NORMAL-WORKER ASSIST (RESEARCH/AUDIT)"
        if ready > SPECIALIST_RESEARCH_SWITCH
        else "DISCOVERY SPECIALIST"
    )
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
        f"| :00補助worker mode | **{auxiliary_mode}** |\n"
        f"| :00切替閾値 | **ready > {SPECIALIST_RESEARCH_SWITCH} → 通常worker補助 / ready ≤ {SPECIALIST_RESEARCH_SWITCH} → 探索専用** |\n"
        f"| Latest normal run | **{run_key}** |\n"
        f"| Latest research completed | **{latest_completed}** |\n"
        f"| Research completed (24h) | **{completed_24h}** |\n"
        f"| Oldest active claim age | **{age_text}** |\n\n"
        "### Worker routing snapshot\n\n"
        f"- 毎時`:30`の通常論文workerは、readyが **{HIGH_BACKLOG}本以上** かつactionable researchがある間はresearch / auditを優先し、通常worker側の広範なdiscoveryを止めます。\n"
        f"- readyが **{CRITICAL_WATERMARK}〜{HIGH_BACKLOG - 1}本** ではresearchを継続しつつdiscovery補充を積極化し、**0〜{CRITICAL_WATERMARK - 1}本** では候補枯渇防止のためdiscovery比重を上げます。\n"
        f"- 毎時`:00`の補助workerはreadyが **{SPECIALIST_RESEARCH_SWITCH}本を超える** と通常workerと同じresearch / audit優先動作へ切り替わり、**{SPECIALIST_RESEARCH_SWITCH}本以下** で探索専用へ戻ります。\n"
        "- `.survey/work-queue/next-jobs.json` は優先スナップショットであり、表示件数を処理量上限として扱いません。表示外readyもpriority順に処理対象です。\n"
        "- discoveryのcandidate最大5本は **1探索軸・1 submissionのtransport batch上限** であり、1run全体の候補数・round数・batch数の上限ではありません。\n"
        "- `:00`補助worker由来の実行は、research補助モード時も通常workerの24-run maintenance counterへ加算しません。\n"
        "- 上段の「探索専用worker」統計は実際にdiscoveryを行った履歴だけを集計します。`:00`補助workerがresearch補助モードの回は、探索roundとしては増えません。\n\n"
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
