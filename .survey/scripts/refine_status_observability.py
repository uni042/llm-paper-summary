#!/usr/bin/env python3
"""Refine STATUS.md so durable queue state is not mistaken for live process state.

The base dashboard and throughput renderer intentionally remain the owners of
routing/throughput policy. This final pass only clarifies two observability
boundaries:

* a valid claim lease is not the same thing as a live Scheduled Chat process;
* a Research job can have a durable worker checkpoint before GitHub terminal
  state has caught up.

All values are derived from repository-persisted state. ChatGPT Library is not
queried by this script; Library checkpoints are counted only after a worker has
recorded their checkpoint_ref in durable claim-request/claim state.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

JST = timezone(timedelta(hours=9))
START = "<!-- research-throughput-status:start -->"
END = "<!-- research-throughput-status:end -->"
WORKER_RUN_RE = re.compile(r"(?P<stamp>\d{8}T\d{4})JST", re.IGNORECASE)
WORKER_SLOT_RE = re.compile(r"(?P<hour>\d{2})(?P<minute>00|30)(?:\D|$)")

PROGRESS_LABELS = {
    "全文精読完了（累計）",
    "GitHub反映済みResearch完了（job）",
    "耐久checkpoint済み・GitHub未反映（job）",
    "精読済みユニーク論文（推定）",
}
WORKER_REPLACED_LABELS = {
    "処理中（Active claims）",
    "有効claim（lease）",
    ":30 通常worker Active claims",
    ":00 補助worker Active claims",
    "その他/帰属不明 Active claims",
    "有効leaseを持つworker run",
    ":30 最新worker run",
    ":30 最新run由来の有効claim",
    ":30 旧run由来の有効claim",
    ":00 最新worker run",
    ":00 最新run由来の有効claim",
    ":00 旧run由来の有効claim",
    "その他/帰属不明の有効claim",
}
COUNT_NOTE_PREFIX = "> **精読数の数え方**:"
CLAIM_NOTE_PREFIX = "有効claimは未失効のdurable leaseであり、"


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


def _worker_lane(worker_id: Any) -> str:
    value = str(worker_id or "").lower()
    if not value:
        return "unknown"
    if "discovery" in value or "aux" in value or "specialist" in value:
        return "aux"
    if "scheduled-chat-llm-survey" in value:
        return "normal"
    if "normal" in value or "router" in value:
        return "normal"
    matches = list(WORKER_SLOT_RE.finditer(value))
    if not matches:
        return "unknown"
    return "aux" if matches[-1].group("minute") == "00" else "normal"


def _slot_from_claim_time(claim: dict[str, Any], lane: str) -> datetime | None:
    claimed = _dt(claim.get("claimed_at"))
    if claimed is None:
        return None
    local = claimed.astimezone(JST)
    if lane == "normal":
        slot = local.replace(minute=30, second=0, microsecond=0)
        return slot if local.minute >= 30 else slot - timedelta(hours=1)
    if lane == "aux":
        return local.replace(minute=0, second=0, microsecond=0)
    return None


def _claim_run_key(claim: dict[str, Any]) -> str | None:
    worker_id = str(claim.get("worker_id") or "")
    match = WORKER_RUN_RE.search(worker_id)
    if match is not None:
        try:
            local = datetime.strptime(match.group("stamp"), "%Y%m%dT%H%M").replace(tzinfo=JST)
        except ValueError:
            return None
        return local.isoformat(timespec="seconds")
    local = _slot_from_claim_time(claim, _worker_lane(worker_id))
    return local.isoformat(timespec="seconds") if local is not None else None


def _load_jobs(repo_root: Path) -> dict[str, dict[str, Any]]:
    jobs_dir = repo_root / ".survey/work-queue/jobs"
    jobs: dict[str, dict[str, Any]] = {}
    for path in sorted(jobs_dir.glob("*.json")) if jobs_dir.is_dir() else []:
        job = _load(path)
        job_id = str(job.get("job_id") or path.stem)
        if job_id:
            jobs[job_id] = job
    return jobs


def _load_claims(repo_root: Path) -> dict[str, dict[str, Any]]:
    claims_dir = repo_root / ".survey/work-queue/claims"
    claims: dict[str, dict[str, Any]] = {}
    for path in sorted(claims_dir.glob("*.json")) if claims_dir.is_dir() else []:
        claim = _load(path)
        job_id = str(claim.get("job_id") or path.stem)
        if job_id:
            claims[job_id] = claim
    return claims


def _checkpointed_job_ids(repo_root: Path) -> set[str]:
    """Return job ids with a durable worker checkpoint reference recorded in GitHub."""
    out: set[str] = set()
    request_dir = repo_root / ".survey/work-queue/claim-requests"
    for path in sorted(request_dir.glob("*.json")) if request_dir.is_dir() else []:
        request = _load(path)
        for item in request.get("checkpointed_jobs") or []:
            if not isinstance(item, dict) or not item.get("checkpoint_ref"):
                continue
            job_id = str(item.get("job_id") or "")
            if job_id:
                out.add(job_id)

    # The current/latest claim file may contain the release checkpoint before a
    # later request has copied it into checkpointed_jobs.
    for job_id, claim in _load_claims(repo_root).items():
        if claim.get("checkpoint_ref"):
            out.add(job_id)
    return out


def research_progress(repo_root: Path) -> dict[str, int]:
    jobs = _load_jobs(repo_root)
    research_jobs = {job_id: job for job_id, job in jobs.items() if job.get("type") == "research"}
    completed_ids = {job_id for job_id, job in research_jobs.items() if job.get("status") == "completed"}
    checkpointed_ids = _checkpointed_job_ids(repo_root) & set(research_jobs)
    pending_checkpoint_ids = {
        job_id for job_id in checkpointed_ids if research_jobs[job_id].get("status") != "completed"
    }

    def identity(job_id: str) -> str:
        job = research_jobs[job_id]
        return str(
            job.get("canonical_id")
            or job.get("source_url")
            or job.get("paper_path")
            or job_id
        )

    effective_ids = completed_ids | pending_checkpoint_ids
    unique_papers = {identity(job_id) for job_id in effective_ids}
    return {
        "integrated_jobs": len(completed_ids),
        "checkpoint_pending_jobs": len(pending_checkpoint_ids),
        "effective_unique_papers": len(unique_papers),
    }


def active_claim_rows(repo_root: Path, now: datetime) -> list[dict[str, Any]]:
    jobs = _load_jobs(repo_root)
    claims = _load_claims(repo_root)
    rows: list[dict[str, Any]] = []
    for job_id, claim in claims.items():
        job = jobs.get(job_id) or {}
        if job.get("status") != "ready" or job.get("type") not in {"research", "audit"}:
            continue
        expires = _dt(claim.get("expires_at"))
        if expires is None or expires <= now:
            continue
        lane = _worker_lane(claim.get("worker_id"))
        rows.append({
            "job_id": job_id,
            "lane": lane,
            "run_key": _claim_run_key(claim),
            "worker_id": str(claim.get("worker_id") or ""),
            "activity": _dt(claim.get("heartbeat_at") or claim.get("claimed_at")),
        })
    return rows


def _run_breakdown(rows: list[dict[str, Any]], lane: str) -> dict[str, Any]:
    lane_rows = [row for row in rows if row.get("lane") == lane]
    candidates: list[tuple[datetime, str]] = []
    for row in lane_rows:
        run_key = row.get("run_key")
        stamp = _dt(run_key)
        if run_key and stamp:
            candidates.append((stamp, str(run_key)))
    latest_run = max(candidates)[1] if candidates else None
    latest_count = sum(1 for row in lane_rows if latest_run and row.get("run_key") == latest_run)
    return {
        "latest_run": latest_run or "—",
        "latest_count": latest_count,
        "old_count": max(0, len(lane_rows) - latest_count),
    }


def worker_observability(repo_root: Path, now: datetime) -> dict[str, Any]:
    rows = active_claim_rows(repo_root, now)
    run_ids = {
        (str(row.get("lane")), str(row.get("run_key") or row.get("worker_id") or row.get("job_id")))
        for row in rows
    }
    unknown = sum(1 for row in rows if row.get("lane") == "unknown")
    return {
        "valid_claims": len(rows),
        "run_count": len(run_ids),
        "normal": _run_breakdown(rows, "normal"),
        "aux": _run_breakdown(rows, "aux"),
        "unknown_claims": unknown,
    }


def _table_label(line: str) -> str | None:
    if not line.startswith("|"):
        return None
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return cells[0] if cells else None


def _replace_progress(text: str, progress: dict[str, int]) -> str:
    lines = text.splitlines()
    indexes = [i for i, line in enumerate(lines) if _table_label(line) in PROGRESS_LABELS]
    if indexes:
        insert_at = min(indexes)
        lines = [line for line in lines if _table_label(line) not in PROGRESS_LABELS]
        block = [
            f"| GitHub反映済みResearch完了（job） | **{progress['integrated_jobs']}** |",
            f"| 耐久checkpoint済み・GitHub未反映（job） | **{progress['checkpoint_pending_jobs']}** |",
            f"| 精読済みユニーク論文（推定） | **{progress['effective_unique_papers']}** |",
        ]
        lines[insert_at:insert_at] = block

    # Keep the explanation adjacent to the current-state section and idempotent.
    lines = [line for line in lines if not line.startswith(COUNT_NOTE_PREFIX)]
    try:
        warning_index = lines.index("### 要注意")
    except ValueError:
        warning_index = -1
    if warning_index >= 0:
        while warning_index > 0 and not lines[warning_index - 1].strip():
            del lines[warning_index - 1]
            warning_index -= 1
        note = (
            f"{COUNT_NOTE_PREFIX} 「GitHub反映済み」はResearch jobのterminal state、"
            "「耐久checkpoint済み・GitHub未反映」はworkerがcheckpoint_refをGitHubへ記録済みだが"
            "terminal stateが未反映のjobです。「精読済みユニーク論文（推定）」は両者を"
            "canonical IDで重複排除して数えます。"
        )
        lines[warning_index:warning_index] = ["", note, ""]
    return "\n".join(lines)


def _replace_claim_explanation(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("- **Claim**:"):
            lines[i] = (
                "- **Claim**: workerが処理権を確保するdurable lease。有効claimはleaseが未失効という意味で、"
                "実際に生存しているworkerプロセス数とは一致しません。Claimableは今すぐ別workerが着手できる件数です。"
            )
    return "\n".join(lines)


def _replace_worker_section(text: str, metrics: dict[str, Any]) -> str:
    if START not in text or END not in text:
        return text
    prefix, tail = text.split(START, 1)
    body, suffix = tail.split(END, 1)
    lines = body.splitlines()

    # Remove previous/legacy rows that confuse lease count with worker count.
    lines = [line for line in lines if _table_label(line) not in WORKER_REPLACED_LABELS]
    lines = [line for line in lines if not line.startswith(CLAIM_NOTE_PREFIX)]

    ready_index = next(
        (i for i, line in enumerate(lines) if _table_label(line) == "未処理候補（Research ready）"),
        None,
    )
    if ready_index is not None:
        lines[ready_index + 1:ready_index + 1] = [
            f"| 有効claim（lease） | **{metrics['valid_claims']}** |",
        ]

    claimable_index = next(
        (i for i, line in enumerate(lines) if _table_label(line) == "今すぐ着手可能（Claimable）"),
        None,
    )
    if claimable_index is not None:
        normal = metrics["normal"]
        aux = metrics["aux"]
        run_rows = [
            f"| 有効leaseを持つworker run | **{metrics['run_count']}** |",
            f"| :30 最新worker run | **{normal['latest_run']}** |",
            f"| :30 最新run由来の有効claim | **{normal['latest_count']}** |",
            f"| :30 旧run由来の有効claim | **{normal['old_count']}** |",
            f"| :00 最新worker run | **{aux['latest_run']}** |",
            f"| :00 最新run由来の有効claim | **{aux['latest_count']}** |",
            f"| :00 旧run由来の有効claim | **{aux['old_count']}** |",
            f"| その他/帰属不明の有効claim | **{metrics['unknown_claims']}** |",
        ]
        lines[claimable_index + 1:claimable_index + 1] = run_rows

    while lines and not lines[-1].strip():
        lines.pop()
    lines += [
        "",
        CLAIM_NOTE_PREFIX
        + "Scheduled Chatプロセスの生存そのものではありません。"
        "ここではrun固有worker_idを優先して、最新run由来のleaseと旧run由来の残存leaseを分離します。",
    ]
    body = "\n".join(lines).strip("\n")
    return prefix + START + "\n" + body + "\n" + END + suffix


def refine_text(repo_root: Path, text: str, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)
    text = _replace_claim_explanation(text)
    text = _replace_progress(text, research_progress(repo_root))
    text = _replace_worker_section(text, worker_observability(repo_root, now))
    return text.rstrip() + "\n"


def refine_status(repo_root: Path, status_path: Path, now: datetime | None = None) -> None:
    text = status_path.read_text(encoding="utf-8")
    status_path.write_text(refine_text(repo_root, text, now=now), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--status", type=Path, default=Path("STATUS.md"))
    args = parser.parse_args()
    refine_status(args.repo_root.resolve(), args.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
