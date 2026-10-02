#!/usr/bin/env python3
"""Render STATUS.md with current durable-evidence normalization and diagnostics."""
from __future__ import annotations

import importlib.util
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import render_status_dashboard_core as _core
except ModuleNotFoundError as exc:
    if exc.name != "render_status_dashboard_core":
        raise
    core_path = Path.cwd() / ".survey" / "scripts" / "render_status_dashboard_core.py"
    if not core_path.is_file():
        raise
    spec = importlib.util.spec_from_file_location("render_status_dashboard_core", core_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load status renderer core from {core_path}") from exc
    _core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_core)

import paper_taxonomy


_GENERIC_SURVEY_WORKERS = {"scheduled-chat-llm-survey"}
_CURRENT_SCHEDULED_WORKERS = {"scheduled-chat-00": "00", "scheduled-chat-30": "30", "scheduled-chat-45": "45"}
_CURRENT_RUN_KEY_RE = re.compile(
    r"(?P<stamp>\d{8}T\d{6})(?P<zone>Z|JST|[+-]\d{4})(?:-|$)"
)
_ORIGINAL_COLLECT_SUBMISSIONS = _core.evidence._collect_submissions
_ORIGINAL_DIRECT_EVIDENCE_METRICS = _core._direct_evidence_metrics
_ORIGINAL_RENDER_DIRECT_METRIC_DETAILS = _core._render_direct_metric_details
_ORIGINAL_DISCOVERY_ROUND_IDENTITY = _core._discovery_round_identity


def __getattr__(name: str) -> Any:
    return getattr(_core, name)


def _scheduled_half_hour_from_claimed_at(value: Any):
    claimed_at = _core.evidence._parse_dt(value)
    if claimed_at is None:
        return None
    local = claimed_at.astimezone(_core.evidence.JST)
    if local.minute < 30:
        local = (local - timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
    else:
        local = local.replace(minute=30, second=0, microsecond=0)
    return local.astimezone(claimed_at.tzinfo)


def _scheduled_slot_from_claimed_at(value: Any, worker_id: str):
    """Map a current fixed worker claim to the scheduled invocation slot.

    A :00 worker may claim repeatedly throughout HH:00-HH:59. A :30 worker may
    continue past the hour boundary, so claims before :30 belong to the previous
    HH:30 invocation. This groups all submissions from one invocation together
    without pretending each claim is a new run.
    """
    claimed_at = _core.evidence._parse_dt(value)
    if claimed_at is None:
        return None
    local = claimed_at.astimezone(_core.evidence.JST)
    slot = _CURRENT_SCHEDULED_WORKERS.get(worker_id)
    if slot == "00":
        local = local.replace(minute=0, second=0, microsecond=0)
    elif slot == "30":
        if local.minute < 30:
            local = (local - timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
        else:
            local = local.replace(minute=30, second=0, microsecond=0)
    elif slot == "45":
        if local.minute < 45:
            local = (local - timedelta(hours=1)).replace(minute=45, second=0, microsecond=0)
        else:
            local = local.replace(minute=45, second=0, microsecond=0)
    else:
        return None
    return local.astimezone(claimed_at.tzinfo)


def _discovery_run_time_from_key(value: Any):
    """Parse both ISO legacy run keys and current scheduled-chat run keys."""
    parsed = _core.evidence._parse_dt(value)
    if parsed is not None:
        return parsed
    match = _CURRENT_RUN_KEY_RE.search(str(value or "").strip())
    if match is None:
        return None
    try:
        zone = match.group("zone")
        if zone == "Z":
            zone = "+0000"
        elif zone == "JST":
            zone = "+0900"
        return datetime.strptime(
            match.group("stamp") + zone,
            "%Y%m%dT%H%M%S%z",
        ).astimezone(timezone.utc)
    except ValueError:
        return None


def _explicit_worker_run_time(payload: dict[str, Any]):
    """Read the workflow-v10 run identity carried by the immutable submission."""
    actual_start = _core.evidence._parse_dt(payload.get("actual_invocation_start"))
    if actual_start is not None:
        return actual_start
    return _discovery_run_time_from_key(payload.get("run_key"))


def _discovery_round_identity(submission: dict[str, Any]) -> tuple[str, str] | None:
    """Accept both current and durable pre-v10 Discovery round identities."""
    identity = _ORIGINAL_DISCOVERY_ROUND_IDENTITY(submission)
    if identity is not None:
        return identity
    payload = submission["payload"]
    stats = payload.get("discovery_stats")
    if not isinstance(stats, dict):
        return None
    run_key = str(payload.get("run_key") or "").strip()
    round_id = str(stats.get("round") or "").strip()
    if not run_key or not round_id:
        return None
    return run_key, round_id


def _collect_submissions(repo_root: Path) -> list[dict[str, Any]]:
    """Normalize current workflow-v10 worker/run evidence.

    Current Scheduled Chat worker IDs are stable across invocations, so run time
    cannot be recovered from worker_id itself. Match each submission to its
    durable claim (or claim-result assignment when the claim file was compacted)
    and group it into the worker's scheduled invocation slot.
    """
    rows = _ORIGINAL_COLLECT_SUBMISSIONS(repo_root)
    claims_by_id: dict[str, dict[str, Any]] = {}
    for _, claim in _core.evidence._iter_json(repo_root / ".survey/work-queue/claims"):
        claim_id = str(claim.get("claim_id") or "").strip()
        if claim_id:
            claims_by_id[claim_id] = claim

    for _, result in _core.evidence._iter_json(repo_root / ".survey/work-queue/claim-results"):
        assignments = result.get("assignments")
        if not isinstance(assignments, list):
            continue
        for assignment in assignments:
            if not isinstance(assignment, dict):
                continue
            claim_id = str(assignment.get("claim_id") or "").strip()
            if claim_id and claim_id not in claims_by_id:
                claims_by_id[claim_id] = assignment

    for row in rows:
        parts = {part.lower() for part in row["path"].parts}
        if row.get("kind") == "unknown" and "discovery" in parts:
            row["kind"] = "discovery"

        stats = row["payload"].get("discovery_stats")
        if isinstance(stats, dict):
            run_key = stats.get("run_key") or row["payload"].get("run_key")
            parsed_run = _discovery_run_time_from_key(run_key)
            if parsed_run is not None:
                row["discovery_run_time"] = parsed_run

        explicit_run_time = _explicit_worker_run_time(row["payload"])
        if explicit_run_time is not None:
            row["worker_run_time"] = explicit_run_time

        if row.get("worker_run_time") is not None:
            continue

        worker_id = str(row.get("worker_id") or "")
        if worker_id not in _GENERIC_SURVEY_WORKERS and worker_id not in _CURRENT_SCHEDULED_WORKERS:
            continue

        claim_id = str(row["payload"].get("claim_id") or "").strip()
        claim = claims_by_id.get(claim_id)
        if claim is None:
            continue
        if str(claim.get("worker_id") or "") != worker_id:
            continue
        claim_attempt = str(claim.get("attempt_id") or "")
        submission_attempt = str(row["payload"].get("attempt_id") or "")
        if claim_attempt and submission_attempt and claim_attempt != submission_attempt:
            continue

        if worker_id in _CURRENT_SCHEDULED_WORKERS:
            row["worker_run_time"] = _scheduled_slot_from_claimed_at(
                claim.get("claimed_at"), worker_id
            )
        else:
            row["worker_run_time"] = _scheduled_half_hour_from_claimed_at(
                claim.get("claimed_at")
            )
    return rows


def _current_orphan_submission_paths(
    repo_root: Path,
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    jobs: dict[str, dict[str, Any]],
) -> set[Path]:
    terminally_rejected = _core._terminally_rejected_submission_paths(repo_root, submissions, results)
    return {
        row["path"]
        for row in submissions
        if (not row["job_id"] or row["job_id"] not in jobs)
        and row["path"] not in terminally_rejected
        and _core._discovery_round_identity(row) is None
    }


def _canonicalized_historical_paper_job_paths(
    repo_root: Path, jobs: dict[str, dict[str, Any]]
) -> set[Path]:
    """Return completed jobs whose stale paper_path resolves to a canonical moved paper."""
    recovered: set[Path] = set()
    for job in jobs.values():
        if job["kind"] != "research":
            continue
        payload = job["payload"]
        if str(payload.get("status") or "").strip().lower() != "completed":
            continue
        paper_value = payload.get("paper_path")
        if not isinstance(paper_value, str) or not paper_value.strip():
            continue
        declared = _core.evidence._resolve_repo_path(repo_root, paper_value)
        if declared is not None and declared.is_file():
            continue
        canonical_value = paper_taxonomy.canonicalize_paper_path(
            paper_value, repo_root=repo_root
        )
        if canonical_value == paper_value:
            continue
        canonical = _core.evidence._resolve_repo_path(repo_root, canonical_value)
        if canonical is not None and canonical.is_file():
            recovered.add(job["path"])
    return recovered


def _unresolved_missing_paper_job_paths(
    repo_root: Path, jobs: dict[str, dict[str, Any]]
) -> set[Path]:
    """Expose the exact completed Research jobs still missing their declared paper."""
    recovered = _canonicalized_historical_paper_job_paths(repo_root, jobs)
    unresolved: set[Path] = set()
    for job in jobs.values():
        if job["kind"] != "research":
            continue
        payload = job["payload"]
        if str(payload.get("status") or "").strip().lower() != "completed":
            continue
        paper_value = payload.get("paper_path")
        if not isinstance(paper_value, str) or not paper_value.strip():
            continue
        declared = _core.evidence._resolve_repo_path(repo_root, paper_value)
        if (declared is None or not declared.is_file()) and job["path"] not in recovered:
            unresolved.add(job["path"])
    return unresolved


def _direct_evidence_metrics(
    repo_root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    verified: list[dict[str, Any]],
    verified_discovery: list[dict[str, Any]],
    active: list[dict[str, Any]],
    now,
) -> dict[str, Any]:
    metrics = _ORIGINAL_DIRECT_EVIDENCE_METRICS(
        repo_root,
        jobs=jobs,
        submissions=submissions,
        results=results,
        verified=verified,
        verified_discovery=verified_discovery,
        active=active,
        now=now,
    )
    orphan_paths = _current_orphan_submission_paths(repo_root, submissions, results, jobs)
    old_orphan_count = metrics["consistency"]["orphan_submissions"]
    metrics["consistency"]["orphan_submissions"] = len(orphan_paths)
    metrics["consistency_total"] -= old_orphan_count - len(orphan_paths)
    metrics["orphan_submission_paths"] = sorted(
        str(path.relative_to(repo_root)) for path in orphan_paths
    )

    recovered_paths = _canonicalized_historical_paper_job_paths(repo_root, jobs)
    old_missing = metrics["consistency"]["completed_research_missing_paper"]
    recovered_papers = min(len(recovered_paths), old_missing)
    metrics["consistency"]["completed_research_missing_paper"] = old_missing - recovered_papers
    metrics["consistency_total"] = max(0, metrics["consistency_total"] - recovered_papers)
    metrics["missing_paper_job_paths"] = sorted(
        str(path.relative_to(repo_root))
        for path in _unresolved_missing_paper_job_paths(repo_root, jobs)
    )

    # Current normal workers publish through Library-first import rather than
    # the legacy immutable submission lane. Use durable import results for the
    # top-line Research/Discovery completion timestamps when that evidence exists.
    research_events, discovery_events = _import_progress_events(repo_root, now)
    cutoff_24h = now - timedelta(hours=24)
    if research_events:
        metrics["research_24h"] = sum(
            cutoff_24h <= stamp <= now for stamp in research_events
        )
        metrics["last_research_completed_at"] = max(research_events)
    if discovery_events:
        metrics["last_discovery_completed_at"] = max(
            stamp for stamp, _ in discovery_events
        )
    return metrics


def _render_direct_metric_details(metrics: dict[str, Any]) -> list[str]:
    lines = _ORIGINAL_RENDER_DIRECT_METRIC_DETAILS(metrics)
    missing_paper_paths = metrics.get("missing_paper_job_paths") or []
    if missing_paper_paths:
        lines.extend([
            "### completed Researchのpaper欠損診断対象",
            "",
            "上の欠損件数と同じ判定で残ったjob pathです。履歴jobを推測で書き換えず、対応submission/result/paperを一次証拠で照合するための診断一覧です。",
            "",
        ])
        lines.extend(f"- `{path}`" for path in missing_paper_paths)
        lines.append("")
    orphan_paths = metrics.get("orphan_submission_paths") or []
    if orphan_paths:
        lines.extend([
            "### 対応jobなしsubmissionの診断対象",
            "",
            "上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。",
            "",
        ])
        lines.extend(f"- `{path}`" for path in orphan_paths)
        lines.append("")
    return lines


_core.evidence._collect_submissions = _collect_submissions
_core._discovery_round_identity = _discovery_round_identity
_core._direct_evidence_metrics = _direct_evidence_metrics
_core._render_direct_metric_details = _render_direct_metric_details

def _import_progress_events(repo_root: Path, now):
    """Read only GitHub-resident Library import evidence; never access ChatGPT Library."""
    research_events = []
    discovery_events = []

    # Research terminal results persist after pending payload cleanup.
    for _, payload in _core.evidence._iter_json(repo_root / ".survey/import-inbox/results/research"):
        if str(payload.get("status") or "") not in {"imported", "already_represented"}:
            continue
        stamp = _core.evidence._parse_dt(payload.get("worker_completed_at"))
        if stamp is None:
            stamp = _core.evidence._parse_dt(payload.get("processed_at"))
        if stamp is not None and stamp <= now:
            research_events.append(stamp)

    # Discovery: count each immutable Library run once. Active payloads retain
    # the original run_key; terminal results preserve it for future imports.
    seen = set()
    roots = [
        repo_root / ".survey/import-inbox/pending/discovery",
        repo_root / ".survey/import-inbox/waiting/discovery",
        repo_root / ".survey/import-inbox/blocked/discovery",
        repo_root / ".survey/import-inbox/results/discovery",
    ]
    for root in roots:
        for path, payload in _core.evidence._iter_json(root):
            run_key = str(payload.get("run_key") or "").strip()
            stamp = _discovery_run_time_from_key(run_key)
            count = int(payload.get("record_count") or 0)
            if not run_key:
                # Legacy terminal results did not retain run_key. They are still
                # GitHub evidence, but can only be assigned to import time.
                stamp = _core.evidence._parse_dt(payload.get("processed_at"))
                run_key = "legacy:" + str(path)
            if count <= 0:
                records = payload.get("records")
                if isinstance(records, list):
                    count = len(records)
            if stamp is None or stamp > now or count <= 0 or run_key in seen:
                continue
            seen.add(run_key)
            discovery_events.append((stamp, count))
    return research_events, discovery_events


def _library_first_status(repo_root: Path, now=None) -> str:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    reference_progress = _core._structured_reference_progress(repo_root)
    paper_count = len(_core._paper_markdown_files(repo_root))
    jobs = _core.evidence._collect_jobs(repo_root)
    candidate_backlog = _core._durable_candidate_backlog(jobs)
    research_events, discovery_events = _import_progress_events(repo_root, now)

    local_now = now.astimezone(_core.evidence.JST)
    today = local_now.date()
    daily = []
    for days_ago in range(6, -1, -1):
        day = today - timedelta(days=days_ago)
        research_n = sum(1 for stamp in research_events if stamp.astimezone(_core.evidence.JST).date() == day)
        discovery_n = sum(count for stamp, count in discovery_events if stamp.astimezone(_core.evidence.JST).date() == day)
        daily.append((day, research_n, discovery_n))

    cutoff_24h = now - timedelta(hours=24)
    research_24h = sum(cutoff_24h <= stamp <= now for stamp in research_events)
    discovery_24h = sum(count for stamp, count in discovery_events if cutoff_24h <= stamp <= now)
    last_research = max(research_events, default=None)
    last_discovery = max((stamp for stamp, _ in discovery_events), default=None)

    research_7d = sum(row[1] for row in daily)
    discovery_7d = sum(row[2] for row in daily)
    research_daily_avg = research_7d / 7.0
    discovery_daily_avg = discovery_7d / 7.0
    ref_remaining = int(reference_progress.get("remaining") or 0) if reference_progress.get("available") is True else 0
    ref_days_remaining = ref_remaining / discovery_daily_avg if discovery_daily_avg > 0 else None

    lines = [
        "# LLM論文サーベイ STATUS", "",
        f"> 自動生成: **{local_now.strftime('%Y-%m-%d %H:%M:%S JST')}**", "",
        "GitHubへ到達済みのLibrary-first成果だけから再構成します。ChatGPT Libraryへはアクセスしません。", "",
        "## サマリー", "",
        "| 指標 | 現在値 |", "|---|---:|",
        f"| 収録論文 | **{paper_count}** |",
        f"| 収録候補論文数 | **{candidate_backlog['canonical_candidates']}** |",
        f"| 直近24時間のResearch完了 | **{research_24h}** |",
        f"| 直近24時間のDiscovery本文確認・分類 | **{discovery_24h}** |",
        f"| 最終Research完了 | **{_core.evidence._fmt_time(last_research)}** |",
        f"| 最終Discovery完了 | **{_core.evidence._fmt_time(last_discovery)}** |",
        f"| Research 7日平均 | **{research_daily_avg:.1f}件/日** |",
        f"| Discovery 7日平均 | **{discovery_daily_avg:.1f}件/日** |",
        f"| references推定残日数 | **{f'{ref_days_remaining:.1f}日' if ref_days_remaining is not None else '算出不可'}** |",
        "",
        f"収録候補論文数は `.survey/work-queue/jobs/*.json` の非終端Research jobを対象に、`canonical_id` で一意化できる論文だけを数えます。`canonical_id` なしの非終端Research jobは **{candidate_backlog['missing_canonical']}件**で、この数には推定加算しません。", "",
        "日次進捗はImport日時ではなく元worker実行日時を優先します。旧Research成果にworker時刻がない場合だけImport処理日時へフォールバックします。", "",
        "## 直近7日の日次進捗", "",
        "| 日付 (JST) | Research完了 | Discovery本文確認・分類 |", "|---|---:|---:|",
    ]
    for day, research_n, discovery_n in daily:
        lines.append(f"| {day.isoformat()} | **{research_n}** | **{discovery_n}** |")
    lines += ["", "## 収録論文", "", f"- 現在の論文Markdown実体: **{paper_count}件**",
              "- 対象: `papers/inference/**`、`papers/training/**`、`papers/survey/**`。",
              "- README、comparison系、Movedスタブは除外します。", ""]
    lines.extend(_core._render_structured_reference_progress(reference_progress))
    lines += ["## 集計方針", "",
              "- GitHub checkoutだけを入力にし、ChatGPT Library未転送成果は数えません。",
              "- Discoveryはimmutable runの `run_key` と `record_count` を使用し、同一run_keyを一度だけ数えます。",
              "- Researchはimport resultの `worker_completed_at` を使用します。旧成果だけ `processed_at` を代用します。",
              "- Library未転送分は次回Survey GitHub Import後に反映されます。",
              "- references推定残日数は未処理references ÷ Discovery 7日平均です。", "",
              "---", "", "表示生成: `.survey/scripts/render_status_dashboard.py`", ""]
    return "\n".join(lines)

build_dashboard = _core.build_dashboard


def main() -> int:
    import argparse
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
