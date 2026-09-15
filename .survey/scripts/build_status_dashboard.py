#!/usr/bin/env python3
"""Build STATUS.md only from direct, durable survey evidence.

Accepted evidence:
- .survey/work-queue/jobs/*.json
- .survey/work-queue/results/**/*.json
- .survey/work-queue/submissions/**/*.json
- .survey/work-queue/claims/*.json
- paper files explicitly referenced by those records

Deliberately excluded:
- run-ledger.json and other aggregate counters
- next-jobs.json queue snapshots
- discovery-state.json summaries
- previous STATUS.md contents
- inferred Scheduled Chat process liveness
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
RECENT_HEARTBEAT_MINUTES = 15
TERMINAL_STATUSES = {
    "completed",
    "blocked",
    "blocked_permanent",
    "deferred",
    "rejected",
    "superseded",
    "cancelled",
}
RUN_STAMP_RE = re.compile(r"(?P<date>\d{8})T(?P<hm>\d{4})JST", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _iter_json(directory: Path) -> Iterable[tuple[Path, dict[str, Any]]]:
    if not directory.is_dir():
        return []
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(directory.rglob("*.json")):
        payload = _load_json(path)
        if payload:
            rows.append((path, payload))
    return rows


def _parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        value = value.replace("Z", "+00:00")
        stamp = datetime.fromisoformat(value)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def _fmt_time(value: datetime | None) -> str:
    if value is None:
        return "—"
    return value.astimezone(JST).strftime("%m-%d %H:%M:%S JST")


def _fmt_age(now: datetime, value: datetime | None) -> str:
    if value is None:
        return "—"
    seconds = max(0, int((now - value).total_seconds()))
    if seconds < 60:
        return f"{seconds}秒前"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}分前"
    hours, rem = divmod(minutes, 60)
    return f"{hours}時間{rem}分前"


def _rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return "—"
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _resolve_repo_path(repo_root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip().replace("\\", "/").lstrip("/")
    candidates = [raw]
    if raw.startswith("work-queue/") or raw.startswith("survey-state/"):
        candidates.insert(0, f".survey/{raw}")
    for candidate in candidates:
        path = repo_root / candidate
        if path.is_file():
            return path
    return repo_root / candidates[0]


def _job_id(path: Path, payload: dict[str, Any]) -> str:
    return str(payload.get("job_id") or payload.get("id") or path.stem)


def _kind(path: Path, payload: dict[str, Any]) -> str:
    explicit = str(payload.get("job_type") or payload.get("type") or payload.get("kind") or "").lower()
    if explicit:
        return explicit
    parts = {part.lower() for part in path.parts}
    if "research" in parts:
        return "research"
    if "audit" in parts:
        return "audit"
    if "discovery" in path.name.lower():
        return "discovery"
    return "unknown"


def _label(payload: dict[str, Any], job_id: str) -> str:
    canonical = str(payload.get("canonical_id") or "")
    title = str(payload.get("title") or "")
    if canonical and title:
        return f"`{canonical}` — {title}"
    if title:
        return title
    if canonical:
        return f"`{canonical}`"
    return f"`{job_id}`"


def _run_time_from_worker(worker_id: Any) -> datetime | None:
    text = str(worker_id or "")
    match = RUN_STAMP_RE.search(text)
    if match is None:
        return None
    try:
        local = datetime.strptime(
            match.group("date") + match.group("hm"),
            "%Y%m%d%H%M",
        ).replace(tzinfo=JST)
    except ValueError:
        return None
    return local.astimezone(timezone.utc)


def _collect_jobs(repo_root: Path) -> dict[str, dict[str, Any]]:
    jobs: dict[str, dict[str, Any]] = {}
    for path, payload in _iter_json(repo_root / ".survey/work-queue/jobs"):
        job_id = _job_id(path, payload)
        jobs[job_id] = {
            "path": path,
            "payload": payload,
            "kind": _kind(path, payload),
            "completed_at": _parse_dt(payload.get("completed_at")),
        }
    return jobs


def _collect_submissions(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, payload in _iter_json(repo_root / ".survey/work-queue/submissions"):
        rows.append(
            {
                "path": path,
                "payload": payload,
                "job_id": str(payload.get("job_id") or ""),
                "kind": _kind(path, payload),
                "worker_id": str(payload.get("worker_id") or ""),
                "worker_run_time": _run_time_from_worker(payload.get("worker_id")),
                "discovery_run_time": _parse_dt(
                    (payload.get("discovery_stats") or {}).get("run_key")
                    if isinstance(payload.get("discovery_stats"), dict)
                    else None
                ),
            }
        )
    return rows


def _collect_results(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, payload in _iter_json(repo_root / ".survey/work-queue/results"):
        rows.append(
            {
                "path": path,
                "payload": payload,
                "job_id": str(payload.get("job_id") or ""),
                "kind": _kind(path, payload),
                "processed_at": _parse_dt(payload.get("processed_at")),
            }
        )
    return rows


def _submission_for_result(
    repo_root: Path,
    result: dict[str, Any],
    submissions: list[dict[str, Any]],
) -> dict[str, Any] | None:
    payload = result["payload"]
    explicit = _resolve_repo_path(repo_root, payload.get("submission"))
    if explicit is not None and explicit.is_file():
        for submission in submissions:
            if submission["path"] == explicit:
                return submission

    attempt_id = str(payload.get("attempt_id") or "")
    job_id = result["job_id"]
    candidates = [
        row
        for row in submissions
        if row["job_id"] == job_id
        and (not attempt_id or str(row["payload"].get("attempt_id") or "") == attempt_id)
    ]
    return candidates[0] if len(candidates) == 1 else None


def _paper_path(
    repo_root: Path,
    result_payload: dict[str, Any],
    submission_payload: dict[str, Any],
    job_payload: dict[str, Any],
) -> Path | None:
    artifact = result_payload.get("artifact")
    values: list[Any] = []
    if isinstance(artifact, dict):
        values.append(artifact.get("paper"))
    values.extend([submission_payload.get("paper_path"), job_payload.get("paper_path")])
    for value in values:
        path = _resolve_repo_path(repo_root, value)
        if path is not None and path.is_file():
            return path
    return None


def _verified_completions(
    repo_root: Path,
    jobs: dict[str, dict[str, Any]],
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    verified: list[dict[str, Any]] = []
    seen_jobs: set[str] = set()
    for result in results:
        result_payload = result["payload"]
        kind = result["kind"]
        if kind not in {"research", "audit"}:
            continue
        if result_payload.get("ok") is not True:
            continue
        if str(result_payload.get("job_status") or "").lower() != "completed":
            continue

        job_id = result["job_id"]
        if not job_id or job_id in seen_jobs:
            continue
        job = jobs.get(job_id)
        if job is None:
            continue
        job_payload = job["payload"]
        if str(job_payload.get("status") or "").lower() != "completed":
            continue
        if job["kind"] not in {kind, "unknown"}:
            continue

        submission = _submission_for_result(repo_root, result, submissions)
        if submission is None or submission["job_id"] != job_id:
            continue

        paper = _paper_path(
            repo_root,
            result_payload,
            submission["payload"],
            job_payload,
        )
        if kind == "research" and paper is None:
            continue

        completed_at = result["processed_at"] or job["completed_at"]
        if completed_at is None:
            continue

        verified.append(
            {
                "job_id": job_id,
                "kind": kind,
                "job": job,
                "submission": submission,
                "result": result,
                "paper": paper,
                "completed_at": completed_at,
            }
        )
        seen_jobs.add(job_id)

    return sorted(verified, key=lambda row: row["completed_at"], reverse=True)


def _verified_by_submission(verified: list[dict[str, Any]]) -> dict[Path, dict[str, Any]]:
    return {row["submission"]["path"]: row for row in verified}


def _verified_discovery_rows(
    repo_root: Path,
    jobs: dict[str, dict[str, Any]],
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    discovery_submissions = {
        row["path"]: row
        for row in submissions
        if row["kind"] == "discovery"
        or isinstance(row["payload"].get("discovery_stats"), dict)
    }

    for result in results:
        payload = result["payload"]
        if result["kind"] != "discovery":
            continue
        if payload.get("ok") is not True:
            continue
        if str(payload.get("job_status") or "").lower() != "completed":
            continue
        job_id = result["job_id"]
        job = jobs.get(job_id)
        if job is None or str(job["payload"].get("status") or "").lower() != "completed":
            continue

        explicit = _resolve_repo_path(repo_root, payload.get("submission"))
        submission = discovery_submissions.get(explicit) if explicit is not None else None
        if submission is None:
            candidates = [row for row in discovery_submissions.values() if row["job_id"] == job_id]
            submission = candidates[0] if len(candidates) == 1 else None
        if submission is None or submission["job_id"] != job_id:
            continue

        run_time = submission["discovery_run_time"]
        if run_time is None:
            continue
        rows.append(
            {
                "job_id": job_id,
                "job": job,
                "submission": submission,
                "result": result,
                "run_time": run_time,
                "completed_at": result["processed_at"] or job["completed_at"],
            }
        )
    return sorted(rows, key=lambda row: row["run_time"], reverse=True)


def _latest_paper_run(
    submissions: list[dict[str, Any]],
) -> tuple[datetime | None, str | None, list[dict[str, Any]]]:
    rows = [
        row
        for row in submissions
        if row["kind"] in {"research", "audit"}
        and row["worker_run_time"] is not None
        and row["worker_id"]
    ]
    if not rows:
        return None, None, []
    latest = max(row["worker_run_time"] for row in rows)
    selected = [row for row in rows if row["worker_run_time"] == latest]
    return latest, selected[0]["worker_id"], selected


def _latest_discovery_run(
    submissions: list[dict[str, Any]],
) -> tuple[datetime | None, list[dict[str, Any]]]:
    rows = [
        row
        for row in submissions
        if row["discovery_run_time"] is not None
        and (
            row["kind"] == "discovery"
            or isinstance(row["payload"].get("discovery_stats"), dict)
        )
    ]
    if not rows:
        return None, []
    latest = max(row["discovery_run_time"] for row in rows)
    return latest, [row for row in rows if row["discovery_run_time"] == latest]


def _active_claims(
    repo_root: Path,
    jobs: dict[str, dict[str, Any]],
    now: datetime,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, claim in _iter_json(repo_root / ".survey/work-queue/claims"):
        job_id = str(claim.get("job_id") or path.stem)
        job = jobs.get(job_id)
        if job is None:
            continue
        status = str(job["payload"].get("status") or "").lower()
        if status in TERMINAL_STATUSES:
            continue
        expires_at = _parse_dt(claim.get("expires_at"))
        if expires_at is None or expires_at <= now:
            continue
        rows.append(
            {
                "job_id": job_id,
                "job": job,
                "claim_path": path,
                "claim": claim,
                "worker_id": str(claim.get("worker_id") or "—"),
                "claimed_at": _parse_dt(claim.get("claimed_at")),
                "heartbeat_at": _parse_dt(claim.get("heartbeat_at")),
                "expires_at": expires_at,
            }
        )
    return sorted(
        rows,
        key=lambda row: row["heartbeat_at"]
        or row["claimed_at"]
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )


def _render_verified_evidence(repo_root: Path, row: dict[str, Any]) -> list[str]:
    job = row["job"]
    lines = [
        f"- **{_fmt_time(row['completed_at'])}** [{row['kind']}] "
        f"{_label(job['payload'], row['job_id'])}",
        f"  - job: `{_rel(repo_root, job['path'])}`",
        f"  - result: `{_rel(repo_root, row['result']['path'])}` (`ok=true`)",
        f"  - submission: `{_rel(repo_root, row['submission']['path'])}`",
    ]
    if row["paper"] is not None:
        lines.append(f"  - paper: `{_rel(repo_root, row['paper'])}`")
    return lines


def build_dashboard(repo_root: Path, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    jobs = _collect_jobs(repo_root)
    submissions = _collect_submissions(repo_root)
    results = _collect_results(repo_root)
    verified = _verified_completions(repo_root, jobs, submissions, results)
    verified_by_submission = _verified_by_submission(verified)
    verified_discovery = _verified_discovery_rows(repo_root, jobs, submissions, results)
    active = _active_claims(repo_root, jobs, now)

    cutoff = now - timedelta(hours=RECENT_HOURS)
    recent = [row for row in verified if cutoff <= row["completed_at"] <= now]
    recent_research = [row for row in recent if row["kind"] == "research"]
    recent_audit = [row for row in recent if row["kind"] == "audit"]
    last_completed = recent[0]["completed_at"] if recent else (verified[0]["completed_at"] if verified else None)

    paper_run_time, paper_worker_id, latest_paper_submissions = _latest_paper_run(submissions)
    discovery_run_time, latest_discovery_submissions = _latest_discovery_run(submissions)
    discovery_verified_by_submission = {
        row["submission"]["path"]: row for row in verified_discovery
    }

    heartbeat_cutoff = now - timedelta(minutes=RECENT_HEARTBEAT_MINUTES)
    heartbeat_recent = [
        row
        for row in active
        if row["heartbeat_at"] is not None and heartbeat_cutoff <= row["heartbeat_at"] <= now
    ]

    lines: list[str] = [
        "# LLM論文サーベイ 稼働状況",
        "",
        f"> 自動生成: **{now.astimezone(JST).strftime('%Y-%m-%d %H:%M:%S JST')}**",
        "",
        "このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。",
        "`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。",
        "",
        "## 1. ここ数時間で論文読解・サーベイが成功しているか",
        "",
        "| 指標 | 検証済み実績 |",
        "|---|---:|",
        f"| 直近{RECENT_HOURS}時間 Research完了 | **{len(recent_research)}** |",
        f"| 直近{RECENT_HOURS}時間 Audit完了 | **{len(recent_audit)}** |",
        f"| 直近{RECENT_HOURS}時間 検証済み完了合計 | **{len(recent)}** |",
        f"| 最終検証済み完了 | **{_fmt_time(last_completed)}** |",
        f"| 最終完了から | **{_fmt_age(now, last_completed)}** |",
        "",
        "成功として数えるのは、対応する **job=completed / result.ok=true / immutable submission** が一致し、"
        "Researchではさらにpaper実体が存在するものだけです。",
        "",
    ]

    if recent:
        lines += ["### 直近の検証済み完了", ""]
        for row in recent[:10]:
            lines.extend(_render_verified_evidence(repo_root, row))
    else:
        lines.append(f"- 直近{RECENT_HOURS}時間に、上記条件を満たすResearch/Audit完了は確認できません。")

    lines += [
        "",
        "## 2. 直近タスクが実際に処理成功している証拠",
        "",
        "### :30 論文worker",
        "",
    ]
    if paper_run_time is None:
        lines.append("- worker時刻を復元できるimmutable Research/Audit submissionは確認できません。")
    else:
        succeeded = [
            row for row in latest_paper_submissions if row["path"] in verified_by_submission
        ]
        lines.append(
            f"- 最新観測run: **{paper_run_time.astimezone(JST).strftime('%Y-%m-%d %H:%M JST')}**"
            f" / worker `{paper_worker_id}`"
        )
        lines.append(
            f"- immutable submission: **{len(latest_paper_submissions)}件** / "
            f"検証済み成功: **{len(succeeded)}件**"
        )
        for submission in latest_paper_submissions[:10]:
            verified_row = verified_by_submission.get(submission["path"])
            if verified_row is None:
                lines.append(
                    f"  - **未完了または未検証** `{_rel(repo_root, submission['path'])}` "
                    f"(job `{submission['job_id'] or '—'}`)"
                )
            else:
                lines.append(
                    f"  - **成功** {_label(verified_row['job']['payload'], verified_row['job_id'])} "
                    f"/ result `{_rel(repo_root, verified_row['result']['path'])}` "
                    f"/ paper `{_rel(repo_root, verified_row['paper']) if verified_row['paper'] else '—'}`"
                )

    lines += ["", "### :00 探索worker", ""]
    if discovery_run_time is None:
        lines.append("- `discovery_stats.run_key` を持つimmutable discovery submissionは確認できません。")
    else:
        succeeded = [
            row
            for row in latest_discovery_submissions
            if row["path"] in discovery_verified_by_submission
        ]
        candidate_count = 0
        axes: list[str] = []
        for submission in latest_discovery_submissions:
            payload = submission["payload"]
            stats = payload.get("discovery_stats")
            candidates = payload.get("candidates")
            if isinstance(candidates, list):
                candidate_count += len(candidates)
            elif isinstance(stats, dict):
                candidate_count += int(stats.get("candidate_count") or 0)
            if isinstance(stats, dict):
                axis = str(stats.get("axis") or "")
                if axis and axis not in axes:
                    axes.append(axis)
        lines.append(
            f"- 最新観測run: **{discovery_run_time.astimezone(JST).strftime('%Y-%m-%d %H:%M JST')}**"
        )
        lines.append(
            f"- immutable submission: **{len(latest_discovery_submissions)}件** / "
            f"検証済み成功result: **{len(succeeded)}件** / 候補: **{candidate_count}件**"
        )
        if axes:
            lines.append(f"- 探索軸: {' / '.join(axes)}")
        for submission in latest_discovery_submissions[:10]:
            verified_row = discovery_verified_by_submission.get(submission["path"])
            if verified_row is None:
                lines.append(
                    f"  - **未完了または未検証** `{_rel(repo_root, submission['path'])}` "
                    f"(job `{submission['job_id'] or '—'}`)"
                )
            else:
                lines.append(
                    f"  - **成功** job `{verified_row['job_id']}` "
                    f"/ result `{_rel(repo_root, verified_row['result']['path'])}` "
                    f"/ submission `{_rel(repo_root, submission['path'])}`"
                )

    lines += [
        "",
        "## 3. 今何をやっているか",
        "",
        f"- 未失効かつ非terminal jobのclaim: **{len(active)}件**",
        f"- うち直近{RECENT_HEARTBEAT_MINUTES}分にheartbeat記録あり: **{len(heartbeat_recent)}件**",
        "",
    ]
    if active:
        for row in active[:10]:
            job_payload = row["job"]["payload"]
            lines.append(
                f"- {_label(job_payload, row['job_id'])} [{row['job']['kind']}] "
                f"/ worker `{row['worker_id']}`"
            )
            lines.append(
                f"  - claim: **{_fmt_time(row['claimed_at'])}** / "
                f"heartbeat: **{_fmt_time(row['heartbeat_at'])}** / "
                f"lease expiry: **{_fmt_time(row['expires_at'])}**"
            )
            lines.append(f"  - evidence: `{_rel(repo_root, row['claim_path'])}`")
    else:
        lines.append("- 現在処理中と判定できる有効claimはありません。")

    lines += [
        "",
        "> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。"
        "Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。",
        "",
        "## このSTATUSが採用する証拠",
        "",
        "- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。",
        "- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。",
        "- **探索成功**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合します。",
        "- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。",
        "- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。",
        "",
        "---",
        "",
        "生成ロジック: `.survey/scripts/build_status_dashboard.py`",
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
