#!/usr/bin/env python3
"""Render STATUS.md from direct, durable survey evidence.

The dashboard answers only three operational questions:
1. Have paper-reading / survey tasks actually completed in the last few hours?
2. What direct durable evidence proves the latest scheduled workers succeeded?
3. What work is actively claimed right now?

Unlike the previous dashboard, recent completion counts are derived directly from
terminal job files. Aggregate ledgers are not used as the source of truth for
throughput, so attribution errors cannot turn real completed work into zero.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
RECENT_HOURS = 6
TERMINAL_STATUSES = {
    "completed",
    "blocked",
    "blocked_permanent",
    "deferred",
    "rejected",
    "superseded",
    "cancelled",
}
WORKER_RE = re.compile(r"scheduled-chat-paper-(\d{8})T(\d{4})JST")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _iter_json(directory: Path) -> Iterable[tuple[Path, dict[str, Any]]]:
    if not directory.exists():
        return []
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(directory.rglob("*.json")):
        payload = _load_json(path)
        if payload:
            rows.append((path, payload))
    return rows


def _parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _fmt_time(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.astimezone(JST).strftime("%m-%d %H:%M:%S JST")


def _job_id(path: Path, job: dict[str, Any]) -> str:
    return str(job.get("id") or job.get("job_id") or path.stem)


def _job_kind(path: Path, job: dict[str, Any]) -> str:
    explicit = str(job.get("type") or job.get("kind") or "").lower()
    if explicit:
        return explicit
    name = path.stem.lower()
    if "research" in name:
        return "research"
    if "audit" in name:
        return "audit"
    return "unknown"


def _job_label(job: dict[str, Any], job_id: str) -> str:
    canonical = str(job.get("canonical_id") or "")
    title = str(job.get("title") or "")
    if canonical and title:
        return f"`{canonical}` — {title}"
    if title:
        return title
    if canonical:
        return f"`{canonical}`"
    return f"`{job_id}`"


def _worker_run_time(worker_id: Any) -> datetime | None:
    if not isinstance(worker_id, str):
        return None
    match = WORKER_RE.fullmatch(worker_id)
    if not match:
        return None
    try:
        local = datetime.strptime("".join(match.groups()), "%Y%m%d%H%M").replace(tzinfo=JST)
    except ValueError:
        return None
    return local.astimezone(timezone.utc)


def _path_exists(repo_root: Path, rel: Any) -> bool:
    return isinstance(rel, str) and bool(rel) and (repo_root / rel).is_file()


def _completed_proof(repo_root: Path, job: dict[str, Any]) -> str:
    submission_ok = _path_exists(repo_root, job.get("artifact_submission"))
    paper_ok = _path_exists(repo_root, job.get("paper_path"))
    return (
        "job=completed / "
        f"submission={'存在' if submission_ok else '未確認'} / "
        f"paper={'存在' if paper_ok else '未確認'}"
    )


def _collect_jobs(repo_root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    by_id: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for path, payload in _iter_json(repo_root / ".survey/work-queue/jobs"):
        job_id = _job_id(path, payload)
        row = {
            "path": path,
            "job_id": job_id,
            "kind": _job_kind(path, payload),
            "payload": payload,
            "completed_at": _parse_dt(payload.get("completed_at")),
        }
        by_id[job_id] = row
        rows.append(row)
    return by_id, rows


def _recent_completed(job_rows: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    cutoff = now - timedelta(hours=RECENT_HOURS)
    rows = [
        row
        for row in job_rows
        if str(row["payload"].get("status") or "").lower() == "completed"
        and row["completed_at"] is not None
        and cutoff <= row["completed_at"] <= now
        and row["kind"] in {"research", "audit"}
    ]
    return sorted(rows, key=lambda row: row["completed_at"], reverse=True)


def _collect_submissions(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    root = repo_root / ".survey/work-queue/submissions"
    for path, payload in _iter_json(root):
        worker_id = payload.get("worker_id")
        worker_time = _worker_run_time(worker_id)
        stats = payload.get("discovery_stats") if isinstance(payload.get("discovery_stats"), dict) else None
        run_time = _parse_dt(stats.get("run_key")) if stats else worker_time
        rows.append({
            "path": path,
            "payload": payload,
            "worker_id": worker_id,
            "worker_time": worker_time,
            "discovery_stats": stats,
            "run_time": run_time,
        })
    return rows


def _latest_paper_worker(submissions: list[dict[str, Any]]) -> tuple[str | None, datetime | None, list[dict[str, Any]]]:
    paper_rows = [row for row in submissions if row["worker_time"] is not None]
    if not paper_rows:
        return None, None, []
    latest_time = max(row["worker_time"] for row in paper_rows)
    latest_rows = [row for row in paper_rows if row["worker_time"] == latest_time]
    worker_id = str(latest_rows[0]["worker_id"])
    return worker_id, latest_time, latest_rows


def _latest_discovery(submissions: list[dict[str, Any]]) -> tuple[datetime | None, list[dict[str, Any]]]:
    rows = [row for row in submissions if row["discovery_stats"] is not None and row["run_time"] is not None]
    if not rows:
        return None, []
    latest_time = max(row["run_time"] for row in rows)
    return latest_time, [row for row in rows if row["run_time"] == latest_time]


def _active_claims(repo_root: Path, jobs_by_id: dict[str, dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
    active: list[dict[str, Any]] = []
    for path, claim in _iter_json(repo_root / ".survey/work-queue/claims"):
        expires = _parse_dt(claim.get("expires_at"))
        if expires is None or expires <= now:
            continue
        job_id = str(claim.get("job_id") or path.stem)
        job_row = jobs_by_id.get(job_id)
        if job_row is None:
            continue
        status = str(job_row["payload"].get("status") or "").lower()
        if status in TERMINAL_STATUSES:
            continue
        active.append({
            "job_id": job_id,
            "job": job_row["payload"],
            "kind": str(claim.get("kind") or job_row["kind"]),
            "worker_id": str(claim.get("worker_id") or "—"),
            "claimed_at": _parse_dt(claim.get("claimed_at")),
            "expires_at": expires,
        })
    return sorted(active, key=lambda row: row["claimed_at"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)


def build_dashboard(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    jobs_by_id, job_rows = _collect_jobs(repo_root)
    submissions = _collect_submissions(repo_root)
    recent = _recent_completed(job_rows, now)
    active = _active_claims(repo_root, jobs_by_id, now)
    worker_id, worker_time, latest_worker_submissions = _latest_paper_worker(submissions)
    discovery_time, latest_discovery_rows = _latest_discovery(submissions)
    queue = _load_json(repo_root / ".survey/work-queue/next-jobs.json")

    recent_research = [row for row in recent if row["kind"] == "research"]
    recent_audit = [row for row in recent if row["kind"] == "audit"]

    lines: list[str] = [
        "# LLM論文サーベイ 稼働状況",
        "",
        f"> 自動生成: **{now.astimezone(JST).strftime('%Y-%m-%d %H:%M:%S JST')}**",
        "",
        "このページは、集計済みカウンタではなく **terminal job / immutable submission / claim / 実在するpaperファイル** を直接確認して現状を算出します。",
        "run-ledger等の二次集計値は、直近の成功件数を決める根拠には使いません。",
        "",
        "## 1. ここ数時間で論文読解・サーベイができているか",
        "",
        "| 指標 | 実績 |",
        "|---|---:|",
        f"| 直近{RECENT_HOURS}時間 Research完了 | **{len(recent_research)}** |",
        f"| 直近{RECENT_HOURS}時間 Audit完了 | **{len(recent_audit)}** |",
        f"| 直近{RECENT_HOURS}時間 合計terminal成功 | **{len(recent)}** |",
        "",
    ]

    if recent:
        lines += ["### 直近の完了証拠", ""]
        for row in recent[:10]:
            job = row["payload"]
            lines.append(
                f"- **{_fmt_time(row['completed_at'])}** [{row['kind']}] {_job_label(job, row['job_id'])} — "
                f"{_completed_proof(repo_root, job)}"
            )
    else:
        lines.append(f"- 直近{RECENT_HOURS}時間に `completed_at` を持つResearch/Audit terminal jobはありません。")

    lines += [
        "",
        "## 2. 直近タスクが成功している証拠",
        "",
        "### 通常worker（:30）",
        "",
    ]

    if worker_id is None:
        lines.append("- scheduled paper worker由来のimmutable submissionが見つかりません。")
    else:
        completed_evidence: list[dict[str, Any]] = []
        submitted_jobs: list[dict[str, Any]] = []
        for row in latest_worker_submissions:
            payload = row["payload"]
            job_id = str(payload.get("job_id") or "")
            job_row = jobs_by_id.get(job_id)
            if job_row:
                submitted_jobs.append(job_row)
                job = job_row["payload"]
                if str(job.get("status") or "").lower() == "completed":
                    completed_evidence.append(job_row)
        lines.append(f"- **{worker_time.astimezone(JST).strftime('%H:%M')} 通常worker**: `{worker_id}`")
        if completed_evidence:
            for row in completed_evidence[:5]:
                job = row["payload"]
                paper_exists = _path_exists(repo_root, job.get("paper_path"))
                submission_exists = _path_exists(repo_root, job.get("artifact_submission"))
                proof = "完了job + immutable submission + paper" if paper_exists and submission_exists else _completed_proof(repo_root, job)
                lines.append(
                    f"  - **成功** {_job_label(job, row['job_id'])} — {proof} / completed {_fmt_time(row['completed_at'])}"
                )
        elif submitted_jobs:
            lines.append("  - immutable submissionは存在しますが、対応jobのterminal完了はまだ確認できません。")
        else:
            lines.append("  - submissionは存在しますが、対応jobを直接照合できません。")

    lines += ["", "### 探索worker（:00）", ""]
    if discovery_time is None:
        lines.append("- immutable discovery submissionが見つかりません。")
    else:
        candidate_count = 0
        axes: list[str] = []
        files: list[str] = []
        for row in latest_discovery_rows:
            stats = row["discovery_stats"] or {}
            candidate_count += int(stats.get("candidate_count") or 0)
            axis = str(stats.get("axis") or "未分類")
            if axis not in axes:
                axes.append(axis)
            files.append(str(row["path"].relative_to(repo_root)))
        lines.append(
            f"- **{discovery_time.astimezone(JST).strftime('%H:%M')} 探索worker**: **成功証拠あり** — immutable discovery submission {len(files)}件"
        )
        lines.append(f"  - 探索軸: {' / '.join(axes) or '—'}")
        lines.append(f"  - 評価候補: **{candidate_count}**")
        for path in files[:3]:
            lines.append(f"  - evidence: `{path}`")

    lines += [
        "",
        "## 3. 今何をやっているか",
        "",
    ]
    if active:
        lines.append(f"現在、非terminal jobに対する有効claimが **{len(active)}件** あります。")
        lines.append("")
        for row in active[:10]:
            lines.append(
                f"- [{row['kind']}] {_job_label(row['job'], row['job_id'])} — worker `{row['worker_id']}` / "
                f"claim {_fmt_time(row['claimed_at'])} / lease expiry {_fmt_time(row['expires_at'])}"
            )
    else:
        lines.append("- **現在処理中と断定できる有効claimはありません。** 直近runが完了済みなら正常な待機状態です。")

    next_jobs = [job for job in (queue.get("next_jobs") or []) if isinstance(job, dict)][:3]
    lines += ["", "### 次に着手可能な候補", ""]
    if next_jobs:
        for job in next_jobs:
            job_id = str(job.get("id") or job.get("job_id") or "—")
            lines.append(f"- [{job.get('type', 'unknown')}] {_job_label(job, job_id)}")
    else:
        lines.append("- `next-jobs.json` に表示候補なし")

    lines += [
        "",
        "### 判定ルール",
        "",
        "- Research/Auditの『成功』は `jobs/*.json` の `status=completed` と `completed_at` を直接使用します。",
        "- 通常workerの直近成功証拠は、同一jobについて terminal job・immutable submission・paperファイルを相互照合します。",
        "- 『今やっている』は、lease未失効かつ対応jobが非terminalのclaimだけを表示します。完了jobに残った未失効claimは除外します。",
        "- 探索workerはclaimを持たないため、最後に耐久保存されたimmutable discovery submissionを成功証拠として表示します。submission保存前のブラウズ中状態までは推測しません。",
        "",
        "---",
        "",
        "自動生成物です。集計ロジックは `.survey/scripts/build_status_dashboard.py` にあります。",
        "",
    ]
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
    output.write_text(build_dashboard(root), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
