#!/usr/bin/env python3
"""Render STATUS.md from the direct-evidence collector with a counts-first layout."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_status_dashboard as evidence


KINDS = ("research", "audit", "discovery")
LABELS = {
    "research": "Research",
    "audit": "Audit",
    "discovery": "Discovery",
    "other": "Other/Unknown",
}


def _active_kind(row: dict[str, Any]) -> str:
    kind = row["job"]["kind"]
    return kind if kind in KINDS else "other"


def _candidate_count(submissions: list[dict[str, Any]]) -> int:
    count = 0
    for submission in submissions:
        payload = submission["payload"]
        candidates = payload.get("candidates")
        stats = payload.get("discovery_stats")
        if isinstance(candidates, list):
            count += len(candidates)
        elif isinstance(stats, dict):
            count += int(stats.get("candidate_count") or 0)
    return count


def _axes(submissions: list[dict[str, Any]]) -> list[str]:
    axes: list[str] = []
    for submission in submissions:
        stats = submission["payload"].get("discovery_stats")
        if not isinstance(stats, dict):
            continue
        axis = str(stats.get("axis") or "")
        if axis and axis not in axes:
            axes.append(axis)
    return axes


def _render_active_row(repo_root: Path, row: dict[str, Any]) -> list[str]:
    job_payload = row["job"]["payload"]
    return [
        f"- {evidence._label(job_payload, row['job_id'])} / worker `{row['worker_id']}`",
        f"  - claim: **{evidence._fmt_time(row['claimed_at'])}** / "
        f"heartbeat: **{evidence._fmt_time(row['heartbeat_at'])}** / "
        f"lease expiry: **{evidence._fmt_time(row['expires_at'])}**",
        f"  - evidence: `{evidence._rel(repo_root, row['claim_path'])}`",
    ]


def _render_discovery_evidence(repo_root: Path, row: dict[str, Any]) -> list[str]:
    submission = row["submission"]
    stamp = row["completed_at"] or row["run_time"]
    candidates = _candidate_count([submission])
    axes = _axes([submission])
    lines = [
        f"- **{evidence._fmt_time(stamp)}** job `{row['job_id']}` / 候補 **{candidates}件**",
        f"  - result: `{evidence._rel(repo_root, row['result']['path'])}` (`ok=true`)",
        f"  - submission: `{evidence._rel(repo_root, submission['path'])}`",
    ]
    if axes:
        lines.append(f"  - 探索軸: {' / '.join(axes)}")
    return lines


def _render_latest_paper_kind(
    repo_root: Path,
    *,
    kind: str,
    paper_run_time: datetime | None,
    paper_worker_id: str | None,
    submissions: list[dict[str, Any]],
    verified_by_submission: dict[Path, dict[str, Any]],
) -> list[str]:
    label = LABELS[kind]
    lines = [f"#### {label} (:30)", ""]
    selected = [row for row in submissions if row["kind"] == kind]
    if paper_run_time is None:
        lines.append("- worker時刻を復元できるimmutable submissionは確認できません。")
        return lines

    lines.append(
        f"- 最新観測run: **{paper_run_time.astimezone(evidence.JST).strftime('%Y-%m-%d %H:%M JST')}**"
        f" / worker `{paper_worker_id or '—'}`"
    )
    succeeded = [row for row in selected if row["path"] in verified_by_submission]
    lines.append(
        f"- immutable submission: **{len(selected)}件** / 検証済み成功: **{len(succeeded)}件** / "
        f"未完了・未検証: **{len(selected) - len(succeeded)}件**"
    )
    if not selected:
        lines.append(f"- このrunに{label} submissionはありません。")
        return lines

    for submission in selected[:10]:
        verified_row = verified_by_submission.get(submission["path"])
        if verified_row is None:
            lines.append(
                f"- **未完了または未検証** `{evidence._rel(repo_root, submission['path'])}` "
                f"(job `{submission['job_id'] or '—'}`)"
            )
            continue
        lines.append(
            f"- **成功** {evidence._label(verified_row['job']['payload'], verified_row['job_id'])}"
        )
        lines.append(f"  - job: `{evidence._rel(repo_root, verified_row['job']['path'])}`")
        lines.append(f"  - result: `{evidence._rel(repo_root, verified_row['result']['path'])}` (`ok=true`)")
        lines.append(f"  - submission: `{evidence._rel(repo_root, submission['path'])}`")
        if verified_row["paper"] is not None:
            lines.append(f"  - paper: `{evidence._rel(repo_root, verified_row['paper'])}`")
    return lines


def build_dashboard(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    jobs = evidence._collect_jobs(repo_root)
    submissions = evidence._collect_submissions(repo_root)
    results = evidence._collect_results(repo_root)
    verified = evidence._verified_completions(repo_root, jobs, submissions, results)
    verified_by_submission = evidence._verified_by_submission(verified)
    verified_discovery = evidence._verified_discovery_rows(repo_root, jobs, submissions, results)
    active = evidence._active_claims(repo_root, jobs, now)

    cutoff = now - timedelta(hours=evidence.RECENT_HOURS)
    recent_verified = [row for row in verified if cutoff <= row["completed_at"] <= now]
    recent_by_kind = {
        kind: [row for row in recent_verified if row["kind"] == kind]
        for kind in ("research", "audit")
    }
    recent_discovery = [
        row
        for row in verified_discovery
        if row["completed_at"] is not None and cutoff <= row["completed_at"] <= now
    ]

    paper_run_time, paper_worker_id, latest_paper_submissions = evidence._latest_paper_run(submissions)
    discovery_run_time, latest_discovery_submissions = evidence._latest_discovery_run(submissions)
    discovery_verified_by_submission = {
        row["submission"]["path"]: row for row in verified_discovery
    }

    latest_by_kind: dict[str, list[dict[str, Any]]] = {
        "research": [row for row in latest_paper_submissions if row["kind"] == "research"],
        "audit": [row for row in latest_paper_submissions if row["kind"] == "audit"],
        "discovery": latest_discovery_submissions,
    }
    latest_success = {
        "research": sum(row["path"] in verified_by_submission for row in latest_by_kind["research"]),
        "audit": sum(row["path"] in verified_by_submission for row in latest_by_kind["audit"]),
        "discovery": sum(
            row["path"] in discovery_verified_by_submission for row in latest_by_kind["discovery"]
        ),
    }

    heartbeat_cutoff = now - timedelta(minutes=evidence.RECENT_HEARTBEAT_MINUTES)
    active_by_kind: dict[str, list[dict[str, Any]]] = {
        kind: [row for row in active if _active_kind(row) == kind]
        for kind in (*KINDS, "other")
    }
    heartbeat_by_kind = {
        kind: [
            row
            for row in rows
            if row["heartbeat_at"] is not None and heartbeat_cutoff <= row["heartbeat_at"] <= now
        ]
        for kind, rows in active_by_kind.items()
    }

    recent_counts = {
        "research": len(recent_by_kind["research"]),
        "audit": len(recent_by_kind["audit"]),
        "discovery": len(recent_discovery),
        "other": 0,
    }
    latest_submission_counts = {
        kind: len(latest_by_kind[kind]) for kind in KINDS
    } | {"other": 0}
    latest_success_counts = latest_success | {"other": 0}
    latest_unverified_counts = {
        kind: latest_submission_counts[kind] - latest_success_counts[kind]
        for kind in (*KINDS, "other")
    }
    candidate_count = _candidate_count(latest_discovery_submissions)

    lines: list[str] = [
        "# LLM論文サーベイ 稼働状況",
        "",
        f"> 自動生成: **{now.astimezone(evidence.JST).strftime('%Y-%m-%d %H:%M:%S JST')}**",
        "",
        "このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。",
        "`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。",
        "",
        "## 件数サマリー",
        "",
        f"直近{evidence.RECENT_HOURS}時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。",
        "",
        f"| 区分 | 直近{evidence.RECENT_HOURS}h成功 | 最新run submission | 最新run成功 | 最新run未完了/未検証 | 現在claim | 直近{evidence.RECENT_HEARTBEAT_MINUTES}分heartbeat | 最新run候補 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for kind in KINDS:
        candidate_cell = f"**{candidate_count}**" if kind == "discovery" else "—"
        lines.append(
            f"| {LABELS[kind]} | **{recent_counts[kind]}** | **{latest_submission_counts[kind]}** | "
            f"**{latest_success_counts[kind]}** | **{latest_unverified_counts[kind]}** | "
            f"**{len(active_by_kind[kind])}** | **{len(heartbeat_by_kind[kind])}** | {candidate_cell} |"
        )

    if active_by_kind["other"]:
        lines.append(
            f"| {LABELS['other']} | **0** | **0** | **0** | **0** | "
            f"**{len(active_by_kind['other'])}** | **{len(heartbeat_by_kind['other'])}** | — |"
        )

    total_recent = sum(recent_counts[kind] for kind in KINDS)
    total_submissions = sum(latest_submission_counts[kind] for kind in KINDS)
    total_success = sum(latest_success_counts[kind] for kind in KINDS)
    total_unverified = sum(latest_unverified_counts[kind] for kind in KINDS)
    total_active = len(active)
    total_heartbeat = sum(len(rows) for rows in heartbeat_by_kind.values())
    lines.append(
        f"| 合計 | **{total_recent}** | **{total_submissions}** | **{total_success}** | "
        f"**{total_unverified}** | **{total_active}** | **{total_heartbeat}** | **{candidate_count}** |"
    )

    lines += [
        "",
        "## 詳細証拠",
        "",
        f"### 直近{evidence.RECENT_HOURS}時間の検証済み完了",
        "",
        "### Research",
        "",
    ]
    if recent_by_kind["research"]:
        for row in recent_by_kind["research"][:10]:
            lines.extend(evidence._render_verified_evidence(repo_root, row))
    else:
        lines.append("- 検証済み完了なし。")

    lines += ["", "### Audit", ""]
    if recent_by_kind["audit"]:
        for row in recent_by_kind["audit"][:10]:
            lines.extend(evidence._render_verified_evidence(repo_root, row))
    else:
        lines.append("- 検証済み完了なし。")

    lines += ["", "### Discovery", ""]
    if recent_discovery:
        for row in recent_discovery[:10]:
            lines.extend(_render_discovery_evidence(repo_root, row))
    else:
        lines.append("- 検証済み成功なし。")

    lines += ["", "### 直近タスク", ""]
    lines.extend(
        _render_latest_paper_kind(
            repo_root,
            kind="research",
            paper_run_time=paper_run_time,
            paper_worker_id=paper_worker_id,
            submissions=latest_paper_submissions,
            verified_by_submission=verified_by_submission,
        )
    )
    lines += [""]
    lines.extend(
        _render_latest_paper_kind(
            repo_root,
            kind="audit",
            paper_run_time=paper_run_time,
            paper_worker_id=paper_worker_id,
            submissions=latest_paper_submissions,
            verified_by_submission=verified_by_submission,
        )
    )

    lines += ["", "#### Discovery (:00)", ""]
    if discovery_run_time is None:
        lines.append("- `discovery_stats.run_key` を持つimmutable discovery submissionは確認できません。")
    else:
        discovery_succeeded = [
            row
            for row in latest_discovery_submissions
            if row["path"] in discovery_verified_by_submission
        ]
        lines.append(
            f"- 最新観測run: **{discovery_run_time.astimezone(evidence.JST).strftime('%Y-%m-%d %H:%M JST')}**"
        )
        lines.append(
            f"- immutable submission: **{len(latest_discovery_submissions)}件** / "
            f"検証済み成功result: **{len(discovery_succeeded)}件** / "
            f"未完了・未検証: **{len(latest_discovery_submissions) - len(discovery_succeeded)}件** / "
            f"候補: **{candidate_count}件**"
        )
        axes = _axes(latest_discovery_submissions)
        if axes:
            lines.append(f"- 探索軸: {' / '.join(axes)}")
        for submission in latest_discovery_submissions[:10]:
            verified_row = discovery_verified_by_submission.get(submission["path"])
            if verified_row is None:
                lines.append(
                    f"- **未完了または未検証** `{evidence._rel(repo_root, submission['path'])}` "
                    f"(job `{submission['job_id'] or '—'}`)"
                )
            else:
                lines.extend(_render_discovery_evidence(repo_root, verified_row))

    lines += ["", "### 現在処理中", ""]
    for kind in (*KINDS, "other"):
        if kind == "other" and not active_by_kind[kind]:
            continue
        lines += [f"#### {LABELS[kind]}", ""]
        rows = active_by_kind[kind]
        lines.append(
            f"- 未失効かつ非terminal jobのclaim: **{len(rows)}件** / "
            f"直近{evidence.RECENT_HEARTBEAT_MINUTES}分heartbeat: **{len(heartbeat_by_kind[kind])}件**"
        )
        if rows:
            for row in rows[:10]:
                lines.extend(_render_active_row(repo_root, row))
        else:
            lines.append("- 現在処理中と判定できる有効claimはありません。")
        lines.append("")

    lines += [
        "> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。"
        "Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。",
        "",
        "### このSTATUSが採用する証拠",
        "",
        "- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。",
        "- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。",
        "- **Audit完了**: job/result/submissionの対応と成功状態を照合します。",
        "- **Discovery成功**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合します。",
        "- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。",
        "- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。",
        "",
        "---",
        "",
        "証拠収集: `.survey/scripts/build_status_dashboard.py`",
        "",
        "表示生成: `.survey/scripts/render_status_dashboard.py`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="STATUS.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.write_text(build_dashboard(repo_root), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
