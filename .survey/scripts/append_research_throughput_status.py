#!/usr/bin/env python3
"""Insert concise worker-routing and claim-health metrics near the top of STATUS.md."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

START = "<!-- research-throughput-status:start -->"
END = "<!-- research-throughput-status:end -->"
HIGH_BACKLOG = 25
SPECIALIST_RESEARCH_SWITCH = 50
LOW_COMPLETIONS = 2
TARGET_COMPLETIONS = 3
WORKER_SLOT_RE = re.compile(r"(?P<hour>\d{2})(?P<minute>00|30)(?:\D|$)")
WORKER_RUN_RE = re.compile(r"(?P<date>\d{8})T(?P<time>\d{4})JST", re.IGNORECASE)
JST = timezone(timedelta(hours=9))
DASHBOARD_LABEL_REPLACEMENTS = (
    ("次回保守までの通常run", "保守カウンタ（通常run）"),
    ("探索専用worker run（毎時枠）", ":00 補助worker Discovery run（毎時枠）"),
    ("探索専用worker round（stats観測）", ":00 補助worker Discovery round（stats観測）"),
    ("### 直近の探索専用worker", "### 直近の:00 補助worker Discovery"),
    ("### 探索専用workerの探索効率（直近24時間）", "### :00 補助workerのDiscovery効率（直近24時間）"),
    ("### 直近5探索専用worker run", "### 直近5件の:00 補助worker Discovery run"),
    ("直近24hの探索専用worker重複率", "直近24hの:00 補助worker Discovery重複率"),
    ("Research消化が探索専用workerの候補補充", "Research消化が:00 補助workerのDiscovery候補補充"),
)


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _modernize_dashboard_labels(text: str) -> str:
    """Normalize generated STATUS labels to the current dual-mode :00 worker model."""
    for old, new in DASHBOARD_LABEL_REPLACEMENTS:
        text = text.replace(old, new)
    return text


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


def _is_ordinary_research_run(entry: dict[str, Any], maintenance: dict[str, Any]) -> bool:
    """Return whether a ledger entry can represent an ordinary :30 paper-worker run."""
    stamp = _dt(entry.get("run_key") or entry.get("last_recorded_at"))
    if stamp is None:
        return False
    jst = stamp.astimezone(JST)
    if jst.minute != 30:
        return False
    if jst.hour == 8:
        return False
    if int(maintenance.get("runs_since_maintenance") or 0) == 0:
        maintenance_key = str(maintenance.get("last_counted_run_key") or "")
        if maintenance_key and str(entry.get("run_key") or "") == maintenance_key:
            return False
    return True


def _latest_normal_run(
    entries: list[dict[str, Any]],
    maintenance: dict[str, Any],
) -> dict[str, Any]:
    valid = [
        entry
        for entry in entries
        if isinstance(entry, dict) and _is_ordinary_research_run(entry, maintenance)
    ]
    if not valid:
        return {}
    return max(
        valid,
        key=lambda entry: _dt(entry.get("run_key") or entry.get("last_recorded_at"))
        or datetime.min.replace(tzinfo=timezone.utc),
    )


def _load_claims(repo_root: Path) -> dict[str, dict[str, Any]]:
    claims_dir = repo_root / ".survey/work-queue/claims"
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(claims_dir.glob("*.json")) if claims_dir.is_dir() else []:
        claim = _load(path)
        job_id = str(claim.get("job_id") or path.stem)
        if job_id:
            out[job_id] = claim
    return out


def _ready_claimable_job_ids(repo_root: Path) -> set[str]:
    jobs_dir = repo_root / ".survey/work-queue/jobs"
    out: set[str] = set()
    for path in sorted(jobs_dir.glob("*.json")) if jobs_dir.is_dir() else []:
        job = _load(path)
        if job.get("status") != "ready" or job.get("type") not in {"research", "audit"}:
            continue
        job_id = str(job.get("job_id") or path.stem)
        if job_id:
            out.add(job_id)
    return out


def _worker_lane(worker_id: Any) -> str:
    """Classify research claim ownership into the :30 or :00 Scheduled Chat lane."""
    value = str(worker_id or "").lower()
    if not value:
        return "unknown"
    if "aux" in value or "specialist" in value:
        return "aux"
    if "normal" in value or "router" in value:
        return "normal"

    matches = list(WORKER_SLOT_RE.finditer(value))
    if not matches:
        return "unknown"
    minute = matches[-1].group("minute")
    return "aux" if minute == "00" else "normal"


def _worker_run_time(worker_id: Any) -> datetime | None:
    """Recover the Scheduled Chat run start encoded in a durable worker_id."""
    value = str(worker_id or "")
    matches = list(WORKER_RUN_RE.finditer(value))
    if not matches:
        return None
    match = matches[-1]
    try:
        parsed = datetime.strptime(match.group("date") + match.group("time"), "%Y%m%d%H%M")
    except ValueError:
        return None
    return parsed.replace(tzinfo=JST)


def _is_normal_worker_run(stamp: datetime, maintenance: dict[str, Any]) -> bool:
    jst = stamp.astimezone(JST)
    if jst.minute != 30 or jst.hour == 8:
        return False
    if int(maintenance.get("runs_since_maintenance") or 0) == 0:
        maintenance_stamp = _dt(maintenance.get("last_counted_run_key"))
        if maintenance_stamp is not None and jst == maintenance_stamp.astimezone(JST):
            return False
    return True


def _completed_research_job_ids(entries: list[dict[str, Any]]) -> set[str]:
    completed: set[str] = set()
    for entry in entries:
        for transition in entry.get("terminal_transitions") or []:
            if not isinstance(transition, dict):
                continue
            if transition.get("type") == "research" and transition.get("to") == "completed":
                job_id = str(transition.get("job_id") or "")
                if job_id:
                    completed.add(job_id)
    return completed


def _latest_normal_worker_run_metrics(
    entries: list[dict[str, Any]],
    claims: dict[str, dict[str, Any]],
    maintenance: dict[str, Any],
) -> tuple[str, int]:
    """Return the latest actual normal worker run and its completed research count.

    The run-ledger bucket is keyed by maintenance.last_counted_run_key, which is
    the state-observation slot rather than the originating Scheduled Chat run.
    Durable claim worker_ids encode the actual worker run and therefore take
    precedence for per-run throughput attribution.
    """
    run_times: list[datetime] = []
    for claim in claims.values():
        stamp = _worker_run_time(claim.get("worker_id"))
        if stamp is not None and _worker_lane(claim.get("worker_id")) == "normal" and _is_normal_worker_run(stamp, maintenance):
            run_times.append(stamp)

    if not run_times:
        latest = _latest_normal_run(entries, maintenance)
        return (
            str(latest.get("run_key") or "—"),
            int((latest.get("counts") or {}).get("research_completed") or 0),
        )

    latest_stamp = max(run_times)
    completed_ids = _completed_research_job_ids(entries)
    completed = 0
    for job_id, claim in claims.items():
        stamp = _worker_run_time(claim.get("worker_id"))
        if stamp == latest_stamp and job_id in completed_ids and claim.get("worker_id"):
            completed += 1
    return latest_stamp.isoformat(), completed


def _completion_attribution(
    entries: list[dict[str, Any]],
    claims: dict[str, dict[str, Any]],
    now: datetime,
) -> Counter[str]:
    """Attribute recent research completions using the durable final claim per job."""
    cutoff = now - timedelta(hours=24)
    counts: Counter[str] = Counter()
    seen: set[str] = set()
    for entry in entries:
        recorded = _dt(entry.get("run_key") or entry.get("last_recorded_at"))
        if recorded is None or recorded < cutoff or recorded > now:
            continue
        for transition in entry.get("terminal_transitions") or []:
            if not isinstance(transition, dict):
                continue
            if transition.get("type") != "research" or transition.get("to") != "completed":
                continue
            job_id = str(transition.get("job_id") or "")
            if not job_id or job_id in seen:
                continue
            seen.add(job_id)
            claim = claims.get(job_id) or {}
            counts[_worker_lane(claim.get("worker_id"))] += 1
    return counts


def _active_claim_counts(
    repo_root: Path,
    claims: dict[str, dict[str, Any]],
    now: datetime,
) -> Counter[str]:
    """Count active leases only for jobs still ready and claimable."""
    ready_ids = _ready_claimable_job_ids(repo_root)
    counts: Counter[str] = Counter()
    for job_id, claim in claims.items():
        if job_id not in ready_ids:
            continue
        expires = _dt(claim.get("expires_at"))
        if expires is None or expires <= now:
            continue
        counts[_worker_lane(claim.get("worker_id"))] += 1
    return counts


def _latest_claim_time(
    claims: dict[str, dict[str, Any]],
    lane: str,
) -> datetime | None:
    values: list[datetime] = []
    for claim in claims.values():
        if _worker_lane(claim.get("worker_id")) != lane:
            continue
        stamp = _dt(claim.get("heartbeat_at") or claim.get("claimed_at"))
        if stamp is not None:
            values.append(stamp)
    return max(values) if values else None


def _oldest_active_claim_age(repo_root: Path, now: datetime) -> int | None:
    claims = _load_claims(repo_root)
    ready_ids = _ready_claimable_job_ids(repo_root)
    ages: list[int] = []
    for job_id, claim in claims.items():
        if job_id not in ready_ids:
            continue
        expires = _dt(claim.get("expires_at"))
        if expires is None or expires <= now:
            continue
        activity = _dt(claim.get("heartbeat_at") or claim.get("claimed_at"))
        if activity is None or activity > now:
            continue
        ages.append(max(0, int((now - activity).total_seconds() // 60)))
    return max(ages) if ages else None


def _fmt_time(value: datetime | None) -> str:
    if value is None:
        return "—"
    return value.astimezone(JST).strftime("%m-%d %H:%M JST")


def render_section(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    queue = _load(repo_root / ".survey/work-queue/next-jobs.json")
    ledger = _load(repo_root / ".survey/work-queue/run-ledger.json")
    maintenance = _load(repo_root / ".survey/work-queue/maintenance-cycle.json")
    claims = _load_claims(repo_root)
    research = ((queue.get("counts") or {}).get("research") or {})
    claiming = queue.get("claiming") or {}
    entries = [entry for entry in (ledger.get("entries") or []) if isinstance(entry, dict)]
    run_key, latest_completed = _latest_normal_worker_run_metrics(entries, claims, maintenance)

    ready = int(research.get("ready") or 0)
    active = int(claiming.get("actively_claimed") or 0)
    claimable = int(claiming.get("claimable") or 0)
    oldest_age = _oldest_active_claim_age(repo_root, now)
    high_backlog = ready >= HIGH_BACKLOG and (active + claimable) > 0

    attributed = _completion_attribution(entries, claims, now)
    active_by_lane = _active_claim_counts(repo_root, claims, now)
    latest_aux_claim = _latest_claim_time(claims, "aux")
    latest_normal_claim = _latest_claim_time(claims, "normal")

    normal_mode = "Research/Audit優先（高在庫）" if high_backlog else "通常"
    auxiliary_mode = "通常worker補助（Research/Audit）" if ready > SPECIALIST_RESEARCH_SWITCH else "Discovery優先"
    health = "OK"
    warning = ""
    if high_backlog and run_key != "—" and latest_completed < LOW_COMPLETIONS:
        health = "LOW"
        warning = (
            f"- **処理速度 LOW**: ready={ready} の高在庫状態で、最新通常runのResearch完了は "
            f"{latest_completed} 件です。DiscoveryよりResearch消化を優先します。\n"
        )

    unknown_completed = attributed["unknown"]
    attribution_note = ""
    if unknown_completed:
        attribution_note = (
            f"- 直近24hのResearch完了のうち **{unknown_completed}件** はclaim workerを復元できず、"
            "worker別集計では「帰属不明」としています。\n"
        )

    age_text = "—" if oldest_age is None else f"{oldest_age} min"
    return (
        f"{START}\n"
        "## ワーカー稼働状況\n\n"
        "| 指標 | 状態 |\n"
        "|---|---:|\n"
        f"| :30 通常worker | **{normal_mode}** |\n"
        f"| :00 補助worker | **{auxiliary_mode}** |\n"
        f"| 処理速度 | **{health}** |\n"
        f"| 未処理候補（Research ready） | **{ready}** |\n"
        f"| 処理中（Active claims） | **{active}** |\n"
        f"| 今すぐ着手可能（Claimable） | **{claimable}** |\n"
        f"| :30 通常worker Active claims | **{active_by_lane['normal']}** |\n"
        f"| :00 補助worker Active claims | **{active_by_lane['aux']}** |\n"
        f"| その他/帰属不明 Active claims | **{active_by_lane['unknown']}** |\n"
        f"| :30 通常worker 直近claim | **{_fmt_time(latest_normal_claim)}** |\n"
        f"| :00 補助worker 直近claim | **{_fmt_time(latest_aux_claim)}** |\n"
        f"| 直近24h Research完了（:30 通常worker） | **{attributed['normal']}** |\n"
        f"| 直近24h Research完了（:00 補助worker） | **{attributed['aux']}** |\n"
        f"| 直近24h Research完了（帰属不明） | **{unknown_completed}** |\n"
        f"| 最新通常run | **{run_key}** |\n"
        f"| 最新通常runのResearch完了 | **{latest_completed}** |\n"
        f"| 最古の有効claimの経過時間 | **{age_text}** |\n\n"
        f"Research readyが **{SPECIALIST_RESEARCH_SWITCH}本を超える間は`:00` workerも論文精読側** に回り、"
        f"**{SPECIALIST_RESEARCH_SWITCH}本以下になるとDiscovery優先へ戻ります**。`:30`通常workerは、"
        f"readyが **{HIGH_BACKLOG}本以上** で処理可能なResearchがある間はResearch/Auditを優先します。\n\n"
        f"高在庫時の通常runは、hard stopに達しない限り **最低{TARGET_COMPLETIONS}件** のResearch完了を下限目標にします。"
        "3件は上限・終了条件ではありません。\n\n"
        "Research/Auditの通常配送は **claim-fast → 予約bank → attempt固有immutable descriptor → submission-fast** です。"
        "Actionsは **claim-fast / submission-fast / background** の3レーンです。"
        "旧固定 `chat-inbox.json` は通常経路では使いません。Library fallbackは復旧時にattempt固有immutable descriptorへ変換します。\n\n"
        f"{warning}"
        f"{attribution_note}"
        f"{END}\n"
    )


def append_section(repo_root: Path, status_path: Path, now: datetime | None = None) -> None:
    section = render_section(repo_root, now=now).rstrip()
    try:
        text = status_path.read_text(encoding="utf-8")
    except OSError:
        text = ""
    text = _modernize_dashboard_labels(text)

    if START in text and END in text:
        prefix, rest = text.split(START, 1)
        _, suffix = rest.split(END, 1)
        text = prefix.rstrip() + "\n\n" + section + "\n\n" + suffix.lstrip("\n")
    elif "## 直近24時間の処理量" in text:
        prefix, suffix = text.split("## 直近24時間の処理量", 1)
        text = prefix.rstrip() + "\n\n" + section + "\n\n## 直近24時間の処理量" + suffix
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