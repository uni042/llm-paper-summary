#!/usr/bin/env python3
"""Generate STATUS.md from durable survey state.

The dashboard is deliberately read-only: queue/state files remain owned by the
existing survey workflows. This script only renders their current contents.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
LOW_WATERMARK = 25
CRITICAL_WATERMARK = 15


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _in_window(item: dict[str, Any], cutoff: datetime, now: datetime) -> bool:
    dt = _parse_dt(item.get("run_key") or item.get("last_recorded_at") or item.get("recorded_at"))
    if dt is None:
        return False
    return cutoff <= dt.astimezone(timezone.utc) <= now.astimezone(timezone.utc)


def _run_minute(item: dict[str, Any]) -> int | None:
    dt = _parse_dt(item.get("run_key"))
    return None if dt is None else dt.astimezone(JST).minute


def _fmt_pct(num: int, den: int) -> str:
    return "—" if den <= 0 else f"{100.0 * num / den:.1f}%"


def _sum_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    keys = (
        "research_completed",
        "audit_completed",
        "discovery_completed",
        "blocked",
        "new_jobs",
        "new_papers",
        "fallback_archived",
    )
    out = {key: 0 for key in keys}
    for entry in entries:
        counts = entry.get("counts") or {}
        for key in keys:
            out[key] += int(counts.get(key) or 0)
    return out


def _recent_completed(entries: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for entry in reversed(entries):
        for transition in reversed(entry.get("terminal_transitions") or []):
            if transition.get("type") != "research" or transition.get("to") != "completed":
                continue
            key = transition.get("canonical_id") or transition.get("title") or transition.get("job_id")
            if not key or key in seen:
                continue
            seen.add(str(key))
            result.append(transition)
            if len(result) >= limit:
                return result
    return result


def _axis_rows(history: list[dict[str, Any]]) -> list[tuple[str, int, int, int]]:
    agg: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for row in history:
        axis = str(row.get("axis") or "未分類")
        agg[axis][0] += int(row.get("candidate_count") or 0)
        agg[axis][1] += int(row.get("duplicate_filtered_count") or 0)
        agg[axis][2] += int(row.get("accepted_count") or 0)
    return sorted(
        ((axis, vals[0], vals[1], vals[2]) for axis, vals in agg.items()),
        key=lambda x: (-x[1], x[0]),
    )


def _group_discovery_runs(
    history: list[dict[str, Any]],
    *,
    minute: int | None = None,
) -> list[dict[str, Any]]:
    """Aggregate discovery rounds by Scheduled Chat run_key.

    The specialist Scheduled Chat runs at :00 JST and the normal worker at :30
    JST. discovery-state.json carries the original Scheduled Chat run_key, so it
    is the authoritative source for worker attribution. The run ledger is not:
    helper events can be merged into the latest normal-worker maintenance bucket.
    """
    grouped: dict[str, dict[str, Any]] = {}
    for row in history:
        if minute is not None and _run_minute(row) != minute:
            continue
        run_key = str(row.get("run_key") or "")
        if not run_key:
            continue
        item = grouped.setdefault(
            run_key,
            {
                "run_key": run_key,
                "round_count": 0,
                "axes": [],
                "candidate_count": 0,
                "duplicate_filtered_count": 0,
                "novel_candidate_count": 0,
                "accepted_count": 0,
            },
        )
        item["round_count"] += 1
        axis = str(row.get("axis") or "未分類")
        if axis not in item["axes"]:
            item["axes"].append(axis)
        item["candidate_count"] += int(row.get("candidate_count") or 0)
        item["duplicate_filtered_count"] += int(row.get("duplicate_filtered_count") or 0)
        item["novel_candidate_count"] += int(row.get("novel_candidate_count") or 0)
        item["accepted_count"] += int(row.get("accepted_count") or 0)

    def sort_key(item: dict[str, Any]):
        return _parse_dt(item.get("run_key")) or datetime.min.replace(tzinfo=timezone.utc)

    return sorted(grouped.values(), key=sort_key)


def _normal_blocked(entry: dict[str, Any]) -> int:
    return sum(
        1
        for transition in (entry.get("terminal_transitions") or [])
        if transition.get("to") == "blocked" and transition.get("type") in {"research", "audit"}
    )


def build_dashboard(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now_utc = now.astimezone(timezone.utc)
    now_jst = now_utc.astimezone(JST)
    cutoff_24h = now_utc - timedelta(hours=24)
    cutoff_7d = now_utc - timedelta(days=7)

    queue = _load_json(repo_root / ".survey/work-queue/next-jobs.json")
    ledger = _load_json(repo_root / ".survey/work-queue/run-ledger.json")
    discovery = _load_json(repo_root / ".survey/work-queue/discovery-state.json")
    maintenance = _load_json(repo_root / ".survey/work-queue/maintenance-cycle.json")

    research_counts = ((queue.get("counts") or {}).get("research") or {})
    ready = int(research_counts.get("ready") or 0)
    blocked_now = int(research_counts.get("blocked") or 0)
    deferred_now = int(research_counts.get("deferred") or 0)
    completed_total = int(research_counts.get("completed") or 0)

    ledger_entries = [e for e in (ledger.get("entries") or []) if isinstance(e, dict)]
    discovery_history = [e for e in (discovery.get("history") or []) if isinstance(e, dict)]
    ledger_24 = [e for e in ledger_entries if _in_window(e, cutoff_24h, now_utc)]
    counts_24 = _sum_counts(ledger_24)

    # Attribution is based on the run_key stored in discovery-state, not on the
    # run-ledger bucket. The ledger intentionally merges helper events under the
    # latest maintenance-cycle run key and therefore can mix specialist events
    # into a :30 normal-worker bucket.
    specialist_history = [row for row in discovery_history if _run_minute(row) == 0]
    normal_discovery_history = [row for row in discovery_history if _run_minute(row) == 30]
    specialist_24 = [row for row in specialist_history if _in_window(row, cutoff_24h, now_utc)]
    specialist_runs = _group_discovery_runs(specialist_history, minute=0)
    specialist_runs_24 = _group_discovery_runs(specialist_24, minute=0)
    normal_discovery_runs = _group_discovery_runs(normal_discovery_history, minute=30)
    normal_discovery_by_key = {row["run_key"]: row for row in normal_discovery_runs}

    evaluated_24 = sum(int(e.get("candidate_count") or 0) for e in specialist_24)
    duplicate_24 = sum(int(e.get("duplicate_filtered_count") or 0) for e in specialist_24)
    accepted_24 = sum(int(e.get("accepted_count") or 0) for e in specialist_24)
    novel_24 = sum(int(e.get("novel_candidate_count") or 0) for e in specialist_24)

    latest_run = ledger_entries[-1] if ledger_entries else {}
    latest_run_counts = latest_run.get("counts") or {}
    latest_run_key = str(latest_run.get("run_key") or "")
    latest_normal_discovery = normal_discovery_by_key.get(latest_run_key, {
        "round_count": 0,
        "candidate_count": 0,
        "duplicate_filtered_count": 0,
        "novel_candidate_count": 0,
        "accepted_count": 0,
        "axes": [],
    })
    latest_specialist = specialist_runs[-1] if specialist_runs else {}

    warnings: list[str] = []
    if ready < CRITICAL_WATERMARK:
        warnings.append(f"**CRITICAL**: candidate在庫が15未満（現在 {ready}）。探索を最優先で継続。")
    elif ready < LOW_WATERMARK:
        warnings.append(f"**LOW**: candidate在庫が25未満（現在 {ready}）。能動的な補充が必要。")
    if blocked_now:
        warnings.append(f"Research blocked が **{blocked_now}件** 残っています。")
    if maintenance.get("maintenance_pending"):
        warnings.append("Maintenance が pending です。")
    if maintenance.get("last_consistency_status") not in {None, "passed"}:
        warnings.append(f"Consistency check: **{maintenance.get('last_consistency_status')}**")
    if evaluated_24 and duplicate_24 / evaluated_24 >= 0.70:
        warnings.append(f"直近24hの探索専用worker重複率が **{_fmt_pct(duplicate_24, evaluated_24)}** と高めです。探索軸の変更を優先。")
    if accepted_24 > 0 and counts_24["research_completed"] > accepted_24 * 1.5:
        warnings.append("Research消化が探索専用workerの候補補充を上回っています。candidate枯渇に注意。")
    if accepted_24 > counts_24["research_completed"] * 2 and accepted_24 >= 5:
        warnings.append("候補補充がResearch消化を大きく上回っています。ready在庫の増加を監視。")

    hist_limit = int(discovery.get("history_limit") or 0)
    if hist_limit and len(discovery_history) >= hist_limit:
        oldest = _parse_dt(discovery_history[0].get("run_key"))
        if oldest and oldest.astimezone(timezone.utc) > cutoff_24h:
            warnings.append("探索履歴bufferが24h全域を覆っていない可能性があります。24h探索値は保持済み範囲の下限値です。")

    lines: list[str] = [
        "# 運用ダッシュボード",
        "",
        f"> 自動生成: **{now_jst.strftime('%Y-%m-%d %H:%M JST')}**。正本は `.survey/work-queue/` のdurable stateです。",
        "",
        "## 現在",
        "",
        "| 指標 | 状態 |",
        "|---|---:|",
        f"| Candidate在庫（Research ready） | **{ready}** |",
        f"| Research ready | **{ready}** |",
        f"| Research blocked | **{blocked_now}** |",
        f"| Research deferred | **{deferred_now}** |",
        f"| Research completed（累計） | **{completed_total}** |",
        f"| Maintenance | **{'pending' if maintenance.get('maintenance_pending') else maintenance.get('last_maintenance_status', '—')}** |",
        f"| Consistency | **{maintenance.get('last_consistency_status', '—')}** |",
        f"| Maintenance counter | **{maintenance.get('runs_since_maintenance', '—')} / {maintenance.get('cadence_runs', '—')}** |",
        "",
        "### 注意事項",
        "",
    ]
    lines.extend([f"- {w}" for w in warnings] or ["- 現在、集計stateから重大な警告は検出されていません。"])

    lines += [
        "",
        "## 直近の通常worker",
        "",
        f"Run: **{latest_run.get('run_key', '—')}**",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| Research完了 | **{int(latest_run_counts.get('research_completed') or 0)}** |",
        f"| Audit完了 | **{int(latest_run_counts.get('audit_completed') or 0)}** |",
        f"| 通常worker Discovery round | **{int(latest_normal_discovery.get('round_count') or 0)}** |",
        f"| 通常worker Discovery採用 | **{int(latest_normal_discovery.get('accepted_count') or 0)}** |",
        f"| Repo収録 | **{int(latest_run_counts.get('new_papers') or 0)}** |",
        f"| Research/Audit blocked遷移 | **{_normal_blocked(latest_run)}** |",
        "",
        "> Discoveryは `discovery-state.json` のrun_keyで帰属しています。run-ledgerのDiscovery/new_jobsは探索専用workerのhelper処理が混ざり得るため、この欄では使用しません。",
        "",
        "## 直近の探索専用worker",
        "",
        f"Run: **{latest_specialist.get('run_key', '—')}**",
        "",
        "| 指標 | 値 |",
        "|---|---:|",
        f"| 探索round | **{int(latest_specialist.get('round_count') or 0)}** |",
        f"| 探索軸 | {' / '.join(latest_specialist.get('axes') or []) or '—'} |",
        f"| 評価候補 | **{int(latest_specialist.get('candidate_count') or 0)}** |",
        f"| 重複除外 | **{int(latest_specialist.get('duplicate_filtered_count') or 0)}** |",
        f"| Novel候補 | **{int(latest_specialist.get('novel_candidate_count') or 0)}** |",
        f"| Research候補採用 | **{int(latest_specialist.get('accepted_count') or 0)}** |",
        f"| 重複率 | **{_fmt_pct(int(latest_specialist.get('duplicate_filtered_count') or 0), int(latest_specialist.get('candidate_count') or 0))}** |",
        "",
        "## 直近24時間",
        "",
        "| 指標 | 件数 / 率 |",
        "|---|---:|",
        f"| 通常worker run（ledger観測） | **{len(ledger_24)}** |",
        f"| 探索専用worker run（stats観測） | **{len(specialist_runs_24)}** |",
        f"| 探索専用worker round（stats観測） | **{len(specialist_24)}** |",
        f"| 探索評価候補 | **{evaluated_24}** |",
        f"| 重複除外 | **{duplicate_24}** |",
        f"| 重複率 | **{_fmt_pct(duplicate_24, evaluated_24)}** |",
        f"| Novel候補 | **{novel_24}** |",
        f"| Research候補採用 | **{accepted_24}** |",
        f"| Research完了 | **{counts_24['research_completed']}** |",
        f"| Repo収録 | **{counts_24['new_papers']}** |",
        f"| Audit完了 | **{counts_24['audit_completed']}** |",
        f"| Fallback archive（全helper） | **{counts_24['fallback_archived']}** |",
        "",
        "### 24時間ファネル",
        "",
        f"**探索専用worker評価 {evaluated_24} → 重複除外後 {max(evaluated_24 - duplicate_24, 0)} → Research候補採用 {accepted_24} → Research完了 {counts_24['research_completed']} → Repo収録 {counts_24['new_papers']}**",
        "",
        "## 探索専用workerの探索効率（直近24時間）",
        "",
        "| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    axis_rows = _axis_rows(specialist_24)
    if axis_rows:
        for axis, cand, dup, accepted in axis_rows:
            lines.append(f"| {axis} | {cand} | {dup} | {accepted} | {_fmt_pct(dup, cand)} | {_fmt_pct(accepted, cand)} |")
    else:
        lines.append("| — | 0 | 0 | 0 | — | — |")

    lines += ["", "### 直近5探索専用worker run", ""]
    for run in specialist_runs[-5:][::-1]:
        axes = " / ".join(run.get("axes") or []) or "未分類"
        lines.append(
            f"- {run.get('run_key', '—')} — {int(run.get('round_count') or 0)} round: "
            f"評価 {int(run.get('candidate_count') or 0)} / 重複 {int(run.get('duplicate_filtered_count') or 0)} / "
            f"採用 {int(run.get('accepted_count') or 0)} / 軸 {axes}"
        )
    if not specialist_runs:
        lines.append("- 履歴なし")

    lines += ["", "## 最近処理した論文", "", "### Research完了", ""]
    completed = _recent_completed(ledger_24)
    for paper in completed:
        lines.append(f"- `{paper.get('canonical_id', '—')}` — {paper.get('title') or 'title不明'}")
    if not completed:
        lines.append("- 直近24hの完了記録なし")

    lines += ["", "### 次に処理する候補", ""]
    next_research = [j for j in (queue.get("next_jobs") or []) if j.get("type") == "research"][:5]
    for job in next_research:
        lines.append(f"- P{job.get('priority', '—')} `{job.get('canonical_id', '—')}` — {job.get('title') or 'title不明'}")
    if not next_research:
        lines.append("- ready候補なし")

    earliest_ledger = _parse_dt(ledger_entries[0].get("run_key")) if ledger_entries else None
    lines += ["", "## 7日比較", ""]
    if earliest_ledger is None or earliest_ledger.astimezone(timezone.utc) > cutoff_7d:
        lines.append("**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。")
    else:
        ledger_7d = [e for e in ledger_entries if _in_window(e, cutoff_7d, now_utc)]
        counts_7d = _sum_counts(ledger_7d)
        lines += [
            "| 指標 | 直近24h | 7日平均/日 |",
            "|---|---:|---:|",
            f"| Research完了 | {counts_24['research_completed']} | {counts_7d['research_completed'] / 7:.1f} |",
            f"| Repo収録 | {counts_24['new_papers']} | {counts_7d['new_papers'] / 7:.1f} |",
            f"| Audit完了 | {counts_24['audit_completed']} | {counts_7d['audit_completed'] / 7:.1f} |",
        ]

    lines += [
        "",
        "---",
        "",
        "このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="STATUS.md")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    text = build_dashboard(root)
    (root / args.output).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
