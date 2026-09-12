#!/usr/bin/env python3
"""Build a deterministic Markdown dashboard from canonical survey state.

The dashboard intentionally uses repository-owned state only. ChatGPT Library
pending items are not visible from GitHub Actions and are therefore reported as
unavailable instead of inferred.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

JST = timezone(timedelta(hours=9))
TARGET_INVENTORY = 50
LOW_WATERMARK = 25
CRITICAL_WATERMARK = 15


def read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        out = datetime.fromisoformat(text)
    except ValueError:
        return None
    if out.tzinfo is None:
        out = out.replace(tzinfo=timezone.utc)
    return out.astimezone(timezone.utc)


def format_jst(value: datetime | None) -> str:
    if value is None:
        return "集計不能"
    return value.astimezone(JST).strftime("%Y-%m-%d %H:%M JST")


def newest_timestamp(values: Iterable[Any]) -> datetime | None:
    parsed = [p for p in (parse_time(v) for v in values) if p is not None]
    return max(parsed) if parsed else None


def entry_time(entry: dict[str, Any]) -> datetime | None:
    return parse_time(entry.get("last_recorded_at")) or parse_time(entry.get("run_key"))


def discovery_time(row: dict[str, Any]) -> datetime | None:
    return parse_time(row.get("run_key"))


def in_window(ts: datetime | None, start: datetime, end: datetime) -> bool:
    return ts is not None and start <= ts <= end


def unique_strings(values: Iterable[Any]) -> list[str]:
    return list(dict.fromkeys(str(v) for v in values if v))


def load_jobs(root: Path) -> list[dict[str, Any]]:
    jobs_dir = root / ".survey/work-queue/jobs"
    out: list[dict[str, Any]] = []
    if not jobs_dir.is_dir():
        return out
    for path in sorted(jobs_dir.glob("*.json")):
        data = read_json(path, {})
        if isinstance(data, dict):
            out.append(data)
    return out


def source_worker(row: dict[str, Any]) -> str:
    explicit = str(row.get("source_worker") or "").strip().lower()
    if explicit:
        return explicit
    ts = discovery_time(row)
    if ts is not None:
        local = ts.astimezone(JST)
        if local.minute == 0:
            return "specialist"
        if local.minute == 30:
            return "normal"
    round_name = str(row.get("round") or "").lower()
    if "specialist" in round_name:
        return "specialist"
    return "unknown"


def aggregate_runs(entries: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "research_completed": 0,
        "audit_completed": 0,
        "discovery_completed": 0,
        "blocked": 0,
        "new_jobs": 0,
        "fallback_archived": 0,
    }
    paper_ids: list[str] = []
    completed_papers: list[dict[str, Any]] = []
    for entry in entries:
        raw = entry.get("counts") if isinstance(entry.get("counts"), dict) else {}
        for key in counts:
            counts[key] += int(raw.get(key, 0) or 0)
        paper_ids.extend(str(x) for x in (entry.get("new_paper_ids") or []) if x)
        for transition in entry.get("terminal_transitions") or []:
            if not isinstance(transition, dict):
                continue
            if transition.get("type") == "research" and transition.get("to") == "completed":
                completed_papers.append({
                    "canonical_id": transition.get("canonical_id"),
                    "title": transition.get("title"),
                    "time": entry_time(entry),
                })
    counts["repo_papers"] = len(set(paper_ids))
    counts["completed_papers"] = completed_papers
    counts["normal_runs"] = len(entries)
    return counts


def aggregate_discovery(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out = {
        "rounds": len(rows),
        "candidate_count": 0,
        "duplicate_filtered_count": 0,
        "novel_candidate_count": 0,
        "accepted_count": 0,
        "specialist_runs": 0,
        "normal_runs": 0,
    }
    specialist_keys: set[str] = set()
    normal_keys: set[str] = set()
    for row in rows:
        out["candidate_count"] += int(row.get("candidate_count", 0) or 0)
        out["duplicate_filtered_count"] += int(row.get("duplicate_filtered_count", 0) or 0)
        out["novel_candidate_count"] += int(row.get("novel_candidate_count", 0) or 0)
        out["accepted_count"] += int(row.get("accepted_count", 0) or 0)
        worker = source_worker(row)
        key = str(row.get("run_key") or row.get("round") or "")
        if worker == "specialist":
            specialist_keys.add(key)
        elif worker == "normal":
            normal_keys.add(key)
    out["specialist_runs"] = len(specialist_keys)
    out["normal_runs"] = len(normal_keys)
    return out


def latest_by_time(rows: list[dict[str, Any]], getter) -> dict[str, Any] | None:
    candidates = [(getter(row), row) for row in rows if isinstance(row, dict)]
    candidates = [(ts, row) for ts, row in candidates if ts is not None]
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def count_json_files(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for p in path.glob("*.json") if p.is_file())


def warning_lines(
    inventory: int,
    repair_count: int,
    blocked_count: int,
    fallback_inbox: int,
    maintenance: dict[str, Any],
    consistency: dict[str, Any],
    discovery_24h: dict[str, Any],
    runs_24h: dict[str, Any],
    recent_discovery: list[dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    if inventory < CRITICAL_WATERMARK:
        warnings.append(f"candidate在庫がcritical watermark未満（{inventory} < {CRITICAL_WATERMARK}）。探索補充を最優先。")
    elif inventory < LOW_WATERMARK:
        warnings.append(f"candidate在庫がlow watermark未満（{inventory} < {LOW_WATERMARK}）。探索補充を強化。")
    if repair_count:
        warnings.append(f"validation repair待ちが{repair_count}件。通常researchと独立に修整可能。")
    if blocked_count:
        warnings.append(f"blocked researchが{blocked_count}件。独立jobは止めず、blocker単位で回復を試行。")
    if fallback_inbox:
        warnings.append(f"GitHub fallback inboxに{fallback_inbox}件滞留。replay可能性を確認。")
    if maintenance.get("maintenance_pending"):
        warnings.append("maintenance_pending=true。後続runは止めず、maintenance結果を別途確認。")
    consistency_status = str(consistency.get("status") or consistency.get("result") or "").lower()
    if consistency and consistency_status not in {"passed", "pass", "success", "ok"}:
        warnings.append(f"repository consistencyが正常終了扱いではない（{consistency_status or 'unknown'}）。")

    recent = recent_discovery[-3:]
    cand = sum(int(r.get("candidate_count", 0) or 0) for r in recent)
    dup = sum(int(r.get("duplicate_filtered_count", 0) or 0) for r in recent)
    if cand >= 5 and dup / cand >= 0.7:
        warnings.append(f"直近{len(recent)}探索ラウンドの重複率が{dup / cand:.0%}。同じ軸を反復せず探索空間を広げる。")

    accepted = int(discovery_24h.get("accepted_count", 0) or 0)
    completed = int(runs_24h.get("research_completed", 0) or 0)
    if accepted >= 6 and accepted > completed * 2:
        warnings.append("24時間のcandidate供給がresearch消化を大きく上回っている。priority順の消化を維持。")
    if completed >= 6 and completed > accepted * 2 and inventory < LOW_WATERMARK:
        warnings.append("24時間のresearch消化がcandidate補充を大きく上回っている。在庫枯渇リスクあり。")
    return warnings


def axis_rows(axes: dict[str, Any], *, high_duplicate: bool) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for name, raw in axes.items():
        if not isinstance(raw, dict):
            continue
        candidates = int(raw.get("candidate_count", 0) or 0)
        if candidates <= 0:
            continue
        accepted = int(raw.get("accepted_count", 0) or 0)
        duplicates = int(raw.get("duplicate_filtered_count", 0) or 0)
        row = dict(raw)
        row["acceptance_ratio"] = accepted / candidates
        row["duplicate_ratio_calc"] = duplicates / candidates
        rows.append((name, row))
    if high_duplicate:
        rows.sort(key=lambda item: (item[1]["duplicate_ratio_calc"], item[1].get("candidate_count", 0)), reverse=True)
    else:
        rows.sort(key=lambda item: (item[1]["acceptance_ratio"], item[1].get("candidate_count", 0)), reverse=True)
    return rows[:5]


def seven_day_available(as_of: datetime, run_entries: list[dict[str, Any]], discovery_rows: list[dict[str, Any]]) -> bool:
    threshold = as_of - timedelta(days=7)
    run_times = [entry_time(e) for e in run_entries]
    discovery_times = [discovery_time(r) for r in discovery_rows]
    run_times = [t for t in run_times if t]
    discovery_times = [t for t in discovery_times if t]
    return bool(run_times and discovery_times and min(run_times) <= threshold and min(discovery_times) <= threshold)


def build_dashboard(repo_root: Path) -> str:
    repo_root = Path(repo_root)
    survey = repo_root / ".survey"
    ledger = read_json(survey / "work-queue/run-ledger.json", {}) or {}
    discovery = read_json(survey / "work-queue/discovery-state.json", {}) or {}
    next_jobs = read_json(survey / "work-queue/next-jobs.json", {}) or {}
    maintenance = read_json(survey / "work-queue/maintenance-cycle.json", {}) or {}
    consistency = read_json(survey / "reports/consistency-latest.json", {}) or {}
    jobs = load_jobs(repo_root)

    run_entries = [e for e in (ledger.get("entries") or []) if isinstance(e, dict)]
    discovery_rows = [r for r in (discovery.get("history") or []) if isinstance(r, dict)]
    as_of = newest_timestamp([
        ledger.get("updated_at"),
        discovery.get("updated_at"),
        next_jobs.get("generated_at"),
        consistency.get("generated_at"),
        *(e.get("last_recorded_at") for e in run_entries),
        *(r.get("run_key") for r in discovery_rows),
    ]) or datetime(1970, 1, 1, tzinfo=timezone.utc)
    start_24h = as_of - timedelta(hours=24)
    entries_24h = [e for e in run_entries if in_window(entry_time(e), start_24h, as_of)]
    discovery_24h_rows = [r for r in discovery_rows if in_window(discovery_time(r), start_24h, as_of)]
    run_stats = aggregate_runs(entries_24h)
    discovery_stats = aggregate_discovery(discovery_24h_rows)

    latest_run = latest_by_time(run_entries, entry_time)
    latest_discovery = latest_by_time(discovery_rows, discovery_time)

    ready_research = [j for j in jobs if j.get("type") == "research" and j.get("status") == "ready"]
    if not jobs:
        ready_research = [j for j in (next_jobs.get("next_jobs") or []) if isinstance(j, dict) and j.get("type") == "research"]
    inventory = len(ready_research)
    repair_count = sum(1 for j in jobs if j.get("type") == "research" and j.get("repair_required") and j.get("status") not in {"completed", "superseded", "rejected"})
    blocked_count = sum(1 for j in jobs if j.get("type") == "research" and j.get("status") == "blocked")
    deferred_count = sum(1 for j in jobs if j.get("type") == "research" and j.get("status") == "deferred")
    if not jobs:
        research_counts = ((next_jobs.get("counts") or {}).get("research") or {})
        blocked_count = int(research_counts.get("blocked", 0) or 0)
        deferred_count = int(research_counts.get("deferred", 0) or 0)

    fallback_inbox = count_json_files(survey / "work-queue/fallback-inbox")
    warnings = warning_lines(
        inventory,
        repair_count,
        blocked_count,
        fallback_inbox,
        maintenance,
        consistency,
        discovery_stats,
        run_stats,
        discovery_24h_rows,
    )

    lines: list[str] = [
        "# LLM研究サーベイ 運用ダッシュボード",
        "",
        "> このページはGitHub Actionsが正本stateから自動生成します。手動編集しないでください。",
        "",
        f"**集計時点:** {format_jst(as_of)}",
        "",
        "## 現在",
        "",
        "| 指標 | 状態 |",
        "| --- | ---: |",
        f"| candidate在庫 | **{inventory} / {TARGET_INVENTORY}** |",
        f"| low / critical watermark | {LOW_WATERMARK} / {CRITICAL_WATERMARK} |",
        f"| blocked research | **{blocked_count}** |",
        f"| deferred research | **{deferred_count}** |",
        f"| repair待ち | **{repair_count}** |",
        f"| GitHub fallback inbox | **{fallback_inbox}** |",
        "| Library pending | **集計不能**（GitHub Actionsから不可視） |",
        f"| maintenance | {maintenance.get('runs_since_maintenance', '不明')} / {maintenance.get('cadence_runs', '不明')} runs; pending={str(bool(maintenance.get('maintenance_pending'))).lower()} |",
        f"| consistency | {consistency.get('status') or consistency.get('result') or '集計不能'} |",
        "",
        "## 直近の通常worker",
        "",
    ]

    if latest_run:
        counts = latest_run.get("counts") if isinstance(latest_run.get("counts"), dict) else {}
        lines.extend([
            f"実行枠: **{latest_run.get('run_key', '不明')}**",
            "",
            "| 指標 | 件数 |",
            "| --- | ---: |",
            f"| research完了 | {int(counts.get('research_completed', 0) or 0)} |",
            f"| audit完了 | {int(counts.get('audit_completed', 0) or 0)} |",
            f"| discovery完了 | {int(counts.get('discovery_completed', 0) or 0)} |",
            f"| 新規job | {int(counts.get('new_jobs', 0) or 0)} |",
            f"| repo収録 | {len(set(latest_run.get('new_paper_ids') or []))} |",
            f"| blocked遷移 | {int(counts.get('blocked', 0) or 0)} |",
            "",
        ])
        completed = [t for t in (latest_run.get("terminal_transitions") or []) if isinstance(t, dict) and t.get("type") == "research" and t.get("to") == "completed"]
        if completed:
            lines.append("完了論文: " + " / ".join(str(t.get("title") or t.get("canonical_id") or "unknown") for t in completed[-8:]))
            lines.append("")
    else:
        lines.extend(["集計可能な通常worker履歴がありません。", ""])

    lines.extend(["## 直近の探索", ""])
    if latest_discovery:
        lines.extend([
            f"**{latest_discovery.get('axis') or '軸不明'}** — {int(latest_discovery.get('candidate_count', 0) or 0)}候補 / 重複{int(latest_discovery.get('duplicate_filtered_count', 0) or 0)} / 採用{int(latest_discovery.get('accepted_count', 0) or 0)}",
            "",
            f"- 実行: {latest_discovery.get('run_key') or '不明'} / worker: {source_worker(latest_discovery)}",
            f"- round: `{latest_discovery.get('round') or '不明'}`",
            f"- 次回ヒント: {latest_discovery.get('next_axis_hint') or 'なし'}",
            "",
        ])
    else:
        lines.extend(["集計可能な探索履歴がありません。", ""])

    lines.extend([
        "## 直近24時間",
        "",
        "| 指標 | 件数 |",
        "| --- | ---: |",
        f"| 通常worker実行 | **{run_stats['normal_runs']}** |",
        f"| 探索ラウンド | **{discovery_stats['rounds']}** |",
        f"| 探索評価候補 | **{discovery_stats['candidate_count']}** |",
        f"| 重複除外 | **{discovery_stats['duplicate_filtered_count']}** |",
        f"| 新規候補 | **{discovery_stats['novel_candidate_count']}** |",
        f"| candidate採用 | **{discovery_stats['accepted_count']}** |",
        f"| research完了 | **{run_stats['research_completed']}** |",
        f"| audit完了 | **{run_stats['audit_completed']}** |",
        f"| repo収録 | **{run_stats['repo_papers']}** |",
        f"| blocked遷移 | **{run_stats['blocked']}** |",
        f"| fallback archive | **{run_stats['fallback_archived']}** |",
        "",
        "### 24時間ファネル",
        "",
        f"探索候補 **{discovery_stats['candidate_count']}** → 重複除外後 **{discovery_stats['novel_candidate_count']}** → candidate採用 **{discovery_stats['accepted_count']}** → research完了 **{run_stats['research_completed']}** → repo収録 **{run_stats['repo_papers']}**",
        "",
        "※ research完了は24時間より前に発見された在庫も含むため、同一コホートの変換率ではありません。",
        "",
        "## 探索効率",
        "",
        "### 採用率が高い探索軸",
        "",
        "| 探索軸 | 候補 | 採用 | 採用率 | 重複率 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    axes = discovery.get("axes") if isinstance(discovery.get("axes"), dict) else {}
    top_yield = axis_rows(axes, high_duplicate=False)
    if top_yield:
        for name, row in top_yield:
            lines.append(f"| {name} | {int(row.get('candidate_count', 0) or 0)} | {int(row.get('accepted_count', 0) or 0)} | {row['acceptance_ratio']:.0%} | {row['duplicate_ratio_calc']:.0%} |")
    else:
        lines.append("| 集計不能 | 0 | 0 | - | - |")

    lines.extend([
        "",
        "### 重複率が高い探索軸",
        "",
        "| 探索軸 | 候補 | 重複 | 重複率 |",
        "| --- | ---: | ---: | ---: |",
    ])
    high_dup = axis_rows(axes, high_duplicate=True)
    if high_dup:
        for name, row in high_dup:
            lines.append(f"| {name} | {int(row.get('candidate_count', 0) or 0)} | {int(row.get('duplicate_filtered_count', 0) or 0)} | {row['duplicate_ratio_calc']:.0%} |")
    else:
        lines.append("| 集計不能 | 0 | 0 | - |")

    lines.extend(["", "## 次に処理する候補", ""])
    queued = [j for j in (next_jobs.get("next_jobs") or []) if isinstance(j, dict) and j.get("type") == "research"]
    if queued:
        for job in queued[:8]:
            repair = " / repair" if job.get("repair_required") else ""
            lines.append(f"- P{job.get('priority', '?')} — {job.get('title') or job.get('canonical_id') or job.get('job_id')}{repair}")
    else:
        lines.append("- actionable research candidateなし")

    completed_recent = run_stats.get("completed_papers") or []
    lines.extend(["", "## 24時間以内に完了した論文", ""])
    seen: set[str] = set()
    rendered = 0
    for paper in sorted(completed_recent, key=lambda x: x.get("time") or datetime.min.replace(tzinfo=timezone.utc), reverse=True):
        key = str(paper.get("canonical_id") or paper.get("title") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        lines.append(f"- {paper.get('title') or paper.get('canonical_id')} ({paper.get('canonical_id') or 'ID不明'})")
        rendered += 1
        if rendered >= 12:
            break
    if rendered == 0:
        lines.append("- なし")

    lines.extend(["", "## 気になる状態", ""])
    if warnings:
        lines.extend(f"- {w}" for w in warnings)
    else:
        lines.append("- 現在、主要な運用警告はありません。")

    lines.extend(["", "## 7日比較", ""])
    if seven_day_available(as_of, run_entries, discovery_rows):
        start_7d = as_of - timedelta(days=7)
        run_7d = aggregate_runs([e for e in run_entries if in_window(entry_time(e), start_7d, as_of)])
        disc_7d = aggregate_discovery([r for r in discovery_rows if in_window(discovery_time(r), start_7d, as_of)])
        lines.extend([
            "| 指標 | 7日平均/日 | 直近24時間 |",
            "| --- | ---: | ---: |",
            f"| research完了 | {run_7d['research_completed'] / 7:.1f} | {run_stats['research_completed']} |",
            f"| repo収録 | {run_7d['repo_papers'] / 7:.1f} | {run_stats['repo_papers']} |",
            f"| 探索評価候補 | {disc_7d['candidate_count'] / 7:.1f} | {discovery_stats['candidate_count']} |",
            f"| candidate採用 | {disc_7d['accepted_count'] / 7:.1f} | {discovery_stats['accepted_count']} |",
        ])
    else:
        lines.append("**履歴不足** — 7日分のrun/discovery履歴が蓄積した後に自動表示します。")

    lines.extend([
        "",
        "---",
        "データ源: `run-ledger.json`, `discovery-state.json`, `next-jobs.json`, job state, maintenance/consistency reports。Library pendingのみGitHub側から直接集計できません。",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="STATUS.md")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    text = build_dashboard(root)
    if output.exists() and output.read_text(encoding="utf-8") == text:
        print(json.dumps({"action": "noop", "output": str(output)}, ensure_ascii=False))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(json.dumps({"action": "updated", "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
