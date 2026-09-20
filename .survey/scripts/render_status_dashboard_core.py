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




def _structured_reference_progress(repo_root: Path) -> dict[str, Any]:
    """Read the latest durable repository-reference precheck progress snapshot."""
    rows: list[tuple[datetime, dict[str, Any]]] = []
    root = repo_root / ".survey/work-queue/discovery-precheck/results"
    for _, payload in evidence._iter_json(root):
        if payload.get("ok") is not True:
            continue
        if str(payload.get("provider") or "") not in {"repository_references", "repository_reference_pool"}:
            continue
        progress = payload.get("provider_progress")
        if not isinstance(progress, dict):
            continue
        observed_at = evidence._parse_dt(payload.get("progress_observed_at"))
        if observed_at is None:
            observed_at = datetime.min.replace(tzinfo=timezone.utc)
        rows.append((observed_at, progress))

    if not rows:
        return {
            "available": False,
            "error": "repository-reference progress snapshot has not been generated yet",
        }

    _, progress = max(rows, key=lambda row: row[0])
    required = (
        "reference_total_count",
        "reference_processed_count",
        "reference_remaining_count",
        "reference_represented_count",
        "reference_unrelated_count",
        "reference_borderline_count",
    )
    if any(key not in progress for key in required):
        return {
            "available": False,
            "error": "latest repository-reference progress snapshot is incomplete",
        }
    return {
        "available": True,
        "total": int(progress["reference_total_count"]),
        "processed": int(progress["reference_processed_count"]),
        "remaining": int(progress["reference_remaining_count"]),
        "represented": int(progress["reference_represented_count"]),
        "unrelated": int(progress["reference_unrelated_count"]),
        "borderline": int(progress["reference_borderline_count"]),
    }


def _render_structured_reference_progress(progress: dict[str, Any]) -> list[str]:
    lines = ["## 構造化references探索状況", ""]
    if progress.get("available") is not True:
        lines.extend([
            "- 構造化references探索の進捗スナップショットはまだありません。",
            f"- 診断: {progress.get('error') or 'unknown error'}",
            "",
        ])
        return lines

    total = int(progress["total"])
    processed = int(progress["processed"])
    remaining = int(progress["remaining"])
    ratio = (processed / total * 100.0) if total else 100.0
    lines.extend([
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| 構造化references総候補 | **{total}** |",
        f"| 処理済み | **{processed}** |",
        f"| 未処理 | **{remaining}** |",
        f"| 収録済みとして除外 | **{progress['represented']}** |",
        f"| 無関係として除外 | **{progress['unrelated']}** |",
        f"| 微妙として除外 | **{progress['borderline']}** |",
        "",
        f"- 消化率: **{ratio:.1f}%**",
        "- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。",
        "- 探索時にpaper実体と無関係/微妙台帳から再計算した値を、schema-v3 precheck resultへ耐久保存して表示します。",
        "",
    ])
    return lines

def _durable_candidate_backlog(jobs: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Count current research candidates only from durable job records.

    The number of papers is only asserted for rows with a durable canonical_id.
    Nonterminal research jobs without canonical_id are reported separately rather
    than guessed to be distinct papers.
    """
    canonical_ids: set[str] = set()
    nonterminal_jobs = 0
    missing_canonical = 0

    for job in jobs.values():
        if job["kind"] != "research":
            continue
        payload = job["payload"]
        status = str(payload.get("status") or "").strip().lower()
        if status in evidence.TERMINAL_STATUSES:
            continue

        nonterminal_jobs += 1
        canonical_id = str(payload.get("canonical_id") or "").strip()
        if canonical_id:
            canonical_ids.add(canonical_id.casefold())
        else:
            missing_canonical += 1

    return {
        "canonical_candidates": len(canonical_ids),
        "missing_canonical": missing_canonical,
        "nonterminal_jobs": nonterminal_jobs,
    }


def _source_url(payload: dict[str, Any]) -> str:
    for key in ("url", "source_url", "paper_url", "primary_url", "arxiv_url", "pdf_url"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    source = payload.get("source")
    if isinstance(source, dict):
        for key in ("url", "source_url", "paper_url"):
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def _is_moved_stub(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as handle:
            prefix = handle.read(256).lstrip()
    except (OSError, UnicodeError):
        return False
    first_line = prefix.splitlines()[0].strip().casefold() if prefix else ""
    return first_line in {"#moved", "# moved"} or first_line.startswith("# moved ")


def _paper_markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for area in ("inference", "training", "survey"):
        root = repo_root / "papers" / area
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            name = path.name.casefold()
            stem = path.stem.casefold()
            if name == "readme.md" or stem == "comparison" or stem.startswith("comparison-"):
                continue
            if _is_moved_stub(path):
                continue
            files.append(path)
    return sorted(files)


def _discovery_round_identity(submission: dict[str, Any]) -> tuple[str, str] | None:
    stats = submission["payload"].get("discovery_stats")
    if not isinstance(stats, dict):
        return None
    run_key = str(stats.get("run_key") or "").strip()
    round_id = str(stats.get("round") or "").strip()
    if not run_key or not round_id:
        return None
    return run_key, round_id


def _terminally_rejected_submission_paths(
    repo_root: Path,
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> set[Path]:
    """Return submissions whose exact attempt has a durable terminal rejection.

    These immutable submissions remain useful failure history. They are not a
    current queue-consistency anomaly once the processor has durably rejected
    the exact attempt as non-retryable content validation.
    """
    rejected: set[Path] = set()
    for result in results:
        payload = result["payload"]
        if payload.get("ok") is not False:
            continue
        if payload.get("retryable") is not False:
            continue
        if str(payload.get("failure_class") or "").strip() != "content_validation":
            continue

        submission = evidence._submission_for_result(repo_root, result, submissions)
        if submission is None:
            continue
        result_attempt = str(payload.get("attempt_id") or "").strip()
        submission_attempt = str(submission["payload"].get("attempt_id") or "").strip()
        if not result_attempt or result_attempt != submission_attempt:
            continue
        if result["job_id"] != submission["job_id"]:
            continue
        rejected.add(submission["path"])
    return rejected


def _direct_evidence_metrics(
    repo_root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    verified: list[dict[str, Any]],
    verified_discovery: list[dict[str, Any]],
    active: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    nonterminal: list[tuple[str, dict[str, Any]]] = []
    status_counts: dict[str, int] = {}
    canonical_counts: dict[str, int] = {}
    missing_canonical = 0
    missing_title = 0
    missing_source_url = 0

    for job_id, job in jobs.items():
        if job["kind"] != "research":
            continue
        payload = job["payload"]
        status = str(payload.get("status") or "").strip().lower()
        if status in evidence.TERMINAL_STATUSES:
            continue
        nonterminal.append((job_id, job))
        status_key = status or "(未設定)"
        status_counts[status_key] = status_counts.get(status_key, 0) + 1

        canonical = str(payload.get("canonical_id") or "").strip()
        if canonical:
            key = canonical.casefold()
            canonical_counts[key] = canonical_counts.get(key, 0) + 1
        else:
            missing_canonical += 1
        if not str(payload.get("title") or "").strip():
            missing_title += 1
        if not _source_url(payload):
            missing_source_url += 1

    duplicate_groups = sum(count > 1 for count in canonical_counts.values())
    duplicate_jobs = sum(max(0, count - 1) for count in canonical_counts.values())
    active_research_ids = {
        str(row["job_id"])
        for row in active
        if _active_kind(row) == "research"
    }
    unclaimed_jobs = sum(job_id not in active_research_ids for job_id, _ in nonterminal)

    verified_research = [row for row in verified if row["kind"] == "research"]
    cutoff_24h = now - timedelta(hours=24)
    recent_research_24h = [
        row for row in verified_research if cutoff_24h <= row["completed_at"] <= now
    ]
    last_research_completed_at = max(
        (row["completed_at"] for row in verified_research if row["completed_at"] <= now),
        default=None,
    )

    verified_submission_paths = {row["submission"]["path"] for row in verified}
    verified_submission_paths.update(
        row["submission"]["path"] for row in verified_discovery
    )
    unmatched_submissions = [
        row for row in submissions if row["path"] not in verified_submission_paths
    ]
    unmatched_by_kind: dict[str, int] = {}
    for row in unmatched_submissions:
        kind = row["kind"] if row["kind"] in KINDS else "other"
        unmatched_by_kind[kind] = unmatched_by_kind.get(kind, 0) + 1

    verified_job_ids = {row["job_id"] for row in verified}
    completed_without_verified = 0
    completed_research_missing_paper_paths: set[Path] = set()
    for job_id, job in jobs.items():
        if job["kind"] not in {"research", "audit"}:
            continue
        payload = job["payload"]
        status = str(payload.get("status") or "").strip().lower()
        if status != "completed":
            continue
        if job_id not in verified_job_ids:
            completed_without_verified += 1
        if job["kind"] != "research":
            continue
        paper_value = payload.get("paper_path")
        if not isinstance(paper_value, str) or not paper_value.strip():
            continue
        declared_paper = evidence._resolve_repo_path(repo_root, paper_value)
        if declared_paper is None or not declared_paper.is_file():
            completed_research_missing_paper_paths.add(job["path"])

    terminally_rejected_submission_paths = _terminally_rejected_submission_paths(
        repo_root,
        submissions,
        results,
    )
    orphan_submission_paths = {
        row["path"]
        for row in submissions
        if (not row["job_id"] or row["job_id"] not in jobs)
        and row["path"] not in terminally_rejected_submission_paths
        and not (
            row["kind"] == "discovery"
            and _discovery_round_identity(row) is not None
        )
    }
    success_results = [
        row
        for row in results
        if row["payload"].get("ok") is True
        and str(row["payload"].get("job_status") or "").strip().lower() == "completed"
    ]
    orphan_success_result_paths = {
        row["path"]
        for row in success_results
        if not row["job_id"] or row["job_id"] not in jobs
    }
    success_result_without_submission_paths = {
        row["path"]
        for row in success_results
        if evidence._submission_for_result(repo_root, row, submissions) is None
    }
    malformed_success_result_paths = (
        orphan_success_result_paths | success_result_without_submission_paths
    )
    anomalous_record_paths = (
        completed_research_missing_paper_paths
        | orphan_submission_paths
        | malformed_success_result_paths
    )
    consistency = {
        "completed_without_verified": completed_without_verified,
        "completed_research_missing_paper": len(completed_research_missing_paper_paths),
        "orphan_submissions": len(orphan_submission_paths),
        "orphan_success_results": len(orphan_success_result_paths),
        "success_results_without_submission": len(success_result_without_submission_paths),
    }
    consistency_total = len(anomalous_record_paths)

    return {
        "candidate_papers": len(canonical_counts),
        "nonterminal_jobs": len(nonterminal),
        "unclaimed_jobs": unclaimed_jobs,
        "status_counts": status_counts,
        "duplicate_groups": duplicate_groups,
        "duplicate_jobs": duplicate_jobs,
        "missing_canonical": missing_canonical,
        "missing_title": missing_title,
        "missing_source_url": missing_source_url,
        "paper_markdown_count": len(_paper_markdown_files(repo_root)),
        "research_24h": len(recent_research_24h),
        "last_research_completed_at": last_research_completed_at,
        "unmatched_submissions": len(unmatched_submissions),
        "unmatched_by_kind": unmatched_by_kind,
        "consistency": consistency,
        "consistency_total": consistency_total,
    }


def _render_top_metrics(metrics: dict[str, Any], now: datetime) -> list[str]:
    last = metrics["last_research_completed_at"]
    if last is None:
        last_text = "—"
    else:
        last_text = f"{evidence._fmt_time(last)}（{evidence._fmt_age(now, last)}）"
    return [
        "## 重要指標",
        "",
        "すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。",
        "",
        "| 指標 | 現在値 |",
        "|---|---:|",
        f"| 収録候補論文 | **{metrics['candidate_papers']}** |",
        f"| 未claim Research job | **{metrics['unclaimed_jobs']}** |",
        f"| 直近24hの検証済みResearch収録 | **{metrics['research_24h']}** |",
        f"| 最終検証済みResearch収録 | **{last_text}** |",
        f"| 整合性異常 | **{metrics['consistency_total']}** |",
        "",
    ]


def _render_direct_metric_details(metrics: dict[str, Any]) -> list[str]:
    lines = [
        "",
        "## 耐久証拠の詳細集計",
        "",
        "### 未処理Research jobの状態内訳",
        "",
        "| status | 件数 |",
        "|---|---:|",
    ]
    if metrics["status_counts"]:
        for status, count in sorted(metrics["status_counts"].items()):
            lines.append(f"| {status} | **{count}** |")
    else:
        lines.append("| （なし） | **0** |")

    lines += [
        "",
        "### 候補の重複・識別情報欠損",
        "",
        "非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| 重複canonical_idグループ | **{metrics['duplicate_groups']}** |",
        f"| 重複分のResearch job | **{metrics['duplicate_jobs']}** |",
        f"| canonical_id欠損 | **{metrics['missing_canonical']}** |",
        f"| title欠損 | **{metrics['missing_title']}** |",
        f"| source URL欠損 | **{metrics['missing_source_url']}** |",
        "",
        "### 収録済み論文実体",
        "",
        "`papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README、comparison系、Movedスタブを除外します。",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| inference/training/survey配下の論文Markdown実体 | **{metrics['paper_markdown_count']}** |",
        "",
        "### immutable submissionの未照合",
        "",
        "検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| 成功result未照合のimmutable submission | **{metrics['unmatched_submissions']}** |",
    ]
    for kind in (*KINDS, "other"):
        count = metrics["unmatched_by_kind"].get(kind, 0)
        if count:
            lines.append(f"| └ {LABELS.get(kind, kind)} | **{count}** |")

    consistency = metrics["consistency"]
    lines += [
        "",
        "### 厳格検証が未成立のcompleted job",
        "",
        "completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| completed Research/Audit jobで厳格検証未成立 | **{consistency['completed_without_verified']}** |",
        "",
        "### 整合性異常",
        "",
        "直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。",
        "",
        "| 検出項目 | 件数 |",
        "|---|---:|",
        f"| completed Research jobで指定paper実体なし | **{consistency['completed_research_missing_paper']}** |",
        f"| 対応jobなしsubmission（有効Discovery round除外） | **{consistency['orphan_submissions']}** |",
        f"| 対応jobなし成功result | **{consistency['orphan_success_results']}** |",
        f"| 対応submissionなし成功result | **{consistency['success_results_without_submission']}** |",
        f"| 異常レコード合計（重複排除） | **{metrics['consistency_total']}** |",
        "",
    ]
    return lines


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


def _durable_discovery_rounds(
    submissions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, int]:
    """Return unique immutable round records and anomaly counts.

    A round is proven only by a durable discovery submission containing both
    ``discovery_stats.run_key`` and ``discovery_stats.round``. Aggregate state,
    filenames, and result count are deliberately not used to infer round count.
    """
    rounds: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    duplicate_identities = 0
    missing_identities = 0

    for submission in sorted(submissions, key=lambda row: str(row["path"])):
        identity = _discovery_round_identity(submission)
        if identity is None:
            missing_identities += 1
            continue
        if identity in seen:
            duplicate_identities += 1
            continue
        seen.add(identity)
        rounds.append(submission)

    return rounds, duplicate_identities, missing_identities


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


def _render_discovery_round(
    repo_root: Path,
    submission: dict[str, Any],
    verified_row: dict[str, Any] | None,
) -> list[str]:
    stats = submission["payload"].get("discovery_stats")
    assert isinstance(stats, dict)
    round_id = str(stats.get("round") or "").strip()
    axis = str(stats.get("axis") or "").strip()
    candidates = _candidate_count([submission])
    lines = [
        f"- round `{round_id}` / 候補 **{candidates}件**",
        f"  - submission: `{evidence._rel(repo_root, submission['path'])}`",
    ]
    if axis:
        lines.append(f"  - 探索軸: {axis}")
    if verified_row is None:
        lines.append("  - 個別result照合: なし（immutable round記録は確認済み）")
    else:
        lines.append(
            f"  - 個別result照合: あり / "
            f"`{evidence._rel(repo_root, verified_row['result']['path'])}` (`ok=true`)"
        )
    return lines


def _render_latest_paper_kind(
    repo_root: Path,
    *,
    kind: str,
    paper_run_time: datetime | None,
    paper_worker_id: str | None,
    submissions: list[dict[str, Any]],
    verified_by_submission: dict[Path, dict[str, Any]],
    result_by_submission: dict[Path, dict[str, Any]],
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
    matched_non_success = [row for row in selected if row["path"] in result_by_submission and row["path"] not in verified_by_submission]
    missing_result = [row for row in selected if row["path"] not in result_by_submission]
    lines.append(f"- immutable submission: **{len(selected)}件** / 検証済み成功: **{len(succeeded)}件** / result照合済み非成功: **{len(matched_non_success)}件** / 個別result未照合: **{len(missing_result)}件**")
    if not selected:
        lines.append(f"- このrunに{label} submissionはありません。")
        return lines

    for submission in selected[:10]:
        verified_row = verified_by_submission.get(submission["path"])
        if verified_row is None:
            matched_result = result_by_submission.get(submission["path"])
            if matched_result is not None:
                failure_class = str(matched_result["payload"].get("failure_class") or "non_success")
                lines.append(f"- **result照合済み非成功** `{evidence._rel(repo_root, submission['path'])}` (job `{submission['job_id'] or '—'}`, failure_class `{failure_class}`)")
                lines.append(f"  - result: `{evidence._rel(repo_root, matched_result['path'])}` (`ok={str(matched_result['payload'].get('ok')).lower()}`)")
            else:
                lines.append(f"- **個別result未照合** `{evidence._rel(repo_root, submission['path'])}` (job `{submission['job_id'] or '—'}`)")
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
    result_by_submission: dict[Path, dict[str, Any]] = {}
    for result in results:
        submission = evidence._submission_for_result(repo_root, result, submissions)
        if submission is not None:
            result_by_submission[submission["path"]] = result
    verified_discovery = evidence._verified_discovery_rows(repo_root, jobs, submissions, results)
    active = evidence._active_claims(repo_root, jobs, now)
    candidate_backlog = _durable_candidate_backlog(jobs)
    reference_progress = _structured_reference_progress(repo_root)
    direct_metrics = _direct_evidence_metrics(
        repo_root,
        jobs=jobs,
        submissions=submissions,
        results=results,
        verified=verified,
        verified_discovery=verified_discovery,
        active=active,
        now=now,
    )

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
    latest_discovery_rounds, duplicate_round_submissions, missing_round_submissions = (
        _durable_discovery_rounds(latest_discovery_submissions)
    )

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
    latest_result_counts = {kind: sum(row["path"] in result_by_submission for row in latest_by_kind[kind]) for kind in KINDS} | {"other": 0}
    latest_unverified_counts = {kind: latest_submission_counts[kind] - latest_result_counts[kind] for kind in (*KINDS, "other")}
    candidate_count = _candidate_count(latest_discovery_submissions)

    lines: list[str] = [
        "# LLM論文サーベイ 稼働状況",
        "",
        f"> 自動生成: **{now.astimezone(evidence.JST).strftime('%Y-%m-%d %H:%M:%S JST')}**",
        "",
        "このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。",
        "`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。",
        "",
    ]
    lines.extend(_render_top_metrics(direct_metrics, now))
    lines += [
        "## 現在の収録候補",
        "",
        "`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。",
        "",
        "| 指標 | 件数 |",
        "|---|---:|",
        f"| canonical_id確認済みの一意な候補論文 | **{candidate_backlog['canonical_candidates']}** |",
        f"| canonical_idなしの候補Research job | **{candidate_backlog['missing_canonical']}** |",
        f"| 非終端Research job合計 | **{candidate_backlog['nonterminal_jobs']}** |",
        "",
        "`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。",
        "",
        *_render_structured_reference_progress(reference_progress),
        "## 件数サマリー",
        "",
        f"直近{evidence.RECENT_HOURS}時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。",
        "",
        f"| 区分 | 直近{evidence.RECENT_HOURS}h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近{evidence.RECENT_HEARTBEAT_MINUTES}分heartbeat | 最新run候補 |",
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
    if discovery_run_time is not None:
        lines.append("")
        lines.append(
            f"- 最新Discovery runの耐久探索round: **{len(latest_discovery_rounds)}件** "
            "（immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）"
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
            result_by_submission=result_by_submission,
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
            result_by_submission=result_by_submission,
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
            f"- 耐久探索round: **{len(latest_discovery_rounds)}件** / "
            f"immutable submission: **{len(latest_discovery_submissions)}件** / "
            f"検証済み成功result: **{len(discovery_succeeded)}件** / "
            f"個別result照合: **{len(discovery_succeeded)}件** / "
            f"個別result未照合: **{len(latest_discovery_submissions) - len(discovery_succeeded)}件** / "
            f"候補: **{candidate_count}件**"
        )
        if duplicate_round_submissions or missing_round_submissions:
            lines.append(
                f"- round識別子重複submission: **{duplicate_round_submissions}件** / "
                f"round識別子なしsubmission: **{missing_round_submissions}件**"
            )
        axes = _axes(latest_discovery_rounds)
        if axes:
            lines.append(f"- 探索軸: {' / '.join(axes)}")
        for submission in latest_discovery_rounds[:10]:
            verified_row = discovery_verified_by_submission.get(submission["path"])
            lines.extend(_render_discovery_round(repo_root, submission, verified_row))
        if missing_round_submissions:
            lines.append(
                "- `discovery_stats.run_key + round` が揃わないsubmissionはround数へ推定加算しません。"
            )

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
    ]
    lines.extend(_render_direct_metric_details(direct_metrics))
    lines += [
        "### このSTATUSが採用する証拠",
        "",
        "- **重要指標**: 候補・未claim・24h収録・最終収録・整合性異常を、jobs/submissions/results/claims/paper実体から直接再計算します。",
        "- **収録候補**: `jobs/*.json` の非終端Research jobだけを対象にし、`canonical_id` の一意数を候補論文数として数えます。`canonical_id` 欠損jobは別件数で表示し、論文数へ推定加算しません。",
        "- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。",
        "- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。",
        "- **Audit完了**: job/result/submissionの対応と成功状態を照合します。",
        "- **論文実体数**: `papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README/comparison系/Movedスタブを除外します。",
        "- **immutable submission未照合**: 検証済み成功に結びつかないsubmission実体を数え、処理待ちや失敗済みを含み得るため整合性異常とは分離します。",
        "- **completed未検証**: completedでも現行の厳格な照合条件が成立しないjobを別計上し、過去形式や移行履歴を含み得るため異常とは断定しません。",
        "- **整合性異常**: completed Research jobが宣言したpaper実体の欠損、未解決の対応jobなしsubmission、対応jobなし成功result、対応submissionなし成功resultを直接検出し、レコードpathで重複排除します。`discovery_stats.run_key + round` が揃ったDiscovery submission、および同一attempt/job/submissionへ対応する `content_validation` の再試行不可終端却下resultがあるsubmissionは、対応job欠損だけでは現在の異常にしません。",
        "- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。",
        "- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。",
        "- **構造化references探索状況**: schema-v3 repository-reference precheck resultに耐久保存されたprovider進捗を表示します。値自体は探索時にpaper実体と無関係/微妙台帳から再計算されます。",
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
