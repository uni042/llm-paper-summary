#!/usr/bin/env python3
"""Build dedicated 100-item worklists for scheduled-chat-00 and scheduled-chat-30.

The worklists are rebuildable selection indexes only. Canonical job/claim state,
paper files, and reference relevance ledgers remain authoritative. The two worker
pages are deterministically disjoint whenever at least 200 eligible rows exist.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import claim_state
import reference_pool
import research_job_reconciliation

DEFAULT_LIMIT = 100
WORKERS = ("00", "30")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as tmp:
        tmp.write(text)
        temp = Path(tmp.name)
    temp.replace(path)


def _jobs(root: Path) -> list[dict[str, Any]]:
    folder = root / ".survey/work-queue/jobs"
    rows: list[dict[str, Any]] = []
    if not folder.is_dir():
        return rows
    for path in folder.glob("*.json"):
        value = _read(path, {})
        if not isinstance(value, dict):
            continue
        row = dict(value)
        row.setdefault("job_id", path.stem)
        rows.append(row)
    return rows


def _research_candidates(root: Path) -> tuple[list[dict[str, Any]], int]:
    jobs = _jobs(root)
    claims = claim_state.current_claims(root)
    paper_index = research_job_reconciliation.build_paper_index(root)
    ready = [
        row
        for row in jobs
        if row.get("status") == "ready"
        and row.get("type") in {"research", "audit"}
        and not (
            row.get("type") == "research"
            and research_job_reconciliation.match_represented_research_job(
                row, paper_index
            ) is not None
        )
    ]
    claimable = [
        row
        for row in ready
        if not claims.get(str(row.get("job_id") or ""), {}).get("active")
    ]
    claimable.sort(
        key=lambda row: (
            -int(row.get("priority") or 0),
            str(row.get("created_at") or ""),
            str(row.get("job_id") or ""),
        )
    )
    out: list[dict[str, Any]] = []
    for source_rank, row in enumerate(claimable, start=1):
        out.append(
            {
                "source_rank": source_rank,
                "source_kind": "research_job",
                "job_id": row.get("job_id"),
                "type": row.get("type"),
                "priority": row.get("priority"),
                "canonical_id": row.get("canonical_id"),
                "title": row.get("title"),
                "source_url": row.get("source_url"),
                "paper_path": row.get("paper_path"),
                "created_at": row.get("created_at"),
            }
        )
    return out, len(ready)


def _discovery_candidates(root: Path) -> tuple[list[dict[str, Any]], int]:
    pool = reference_pool.build_reference_pool(root)
    source = pool.get("candidates")
    candidates = source if isinstance(source, list) else []
    out: list[dict[str, Any]] = []
    for source_rank, row in enumerate(candidates, start=1):
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "source_rank": source_rank,
                "source_kind": "reference_review_candidate",
                "canonical_id": row.get("canonical_id"),
                "identity_tokens": row.get("identity_tokens"),
                "title": row.get("title"),
                "source_url": row.get("source_url"),
                "year": row.get("year"),
                "published": row.get("published"),
                "relation_count": row.get("relation_count"),
                "linked_from_lineages": row.get("linked_from_lineages"),
                "linked_from": row.get("linked_from"),
            }
        )
    return out, int(pool.get("candidate_count") or len(candidates))


def _split(rows: list[dict[str, Any]], *, limit: int) -> dict[str, list[dict[str, Any]]]:
    """Assign alternating canonical rows to 00/30, with no overlap."""
    assigned = {"00": [], "30": []}
    for index, source in enumerate(rows):
        worker = WORKERS[index % 2]
        if len(assigned[worker]) >= limit:
            other = "30" if worker == "00" else "00"
            if len(assigned[other]) >= limit:
                break
            worker = other
        row = dict(source)
        row["rank"] = len(assigned[worker]) + 1
        row["assigned_worker"] = f"scheduled-chat-{worker}"
        assigned[worker].append(row)
        if all(len(assigned[key]) >= limit for key in WORKERS):
            break
    return assigned


def build(root: Path, *, limit: int) -> dict[str, dict[str, Any]]:
    research_all, research_ready = _research_candidates(root)
    discovery_all, discovery_pending = _discovery_candidates(root)
    research = _split(research_all, limit=limit)
    discovery = _split(discovery_all, limit=limit)

    result: dict[str, dict[str, Any]] = {}
    for worker in WORKERS:
        worker_id = f"scheduled-chat-{worker}"
        result[worker] = {
            "schema_version": 2,
            "purpose": "dedicated-scheduled-worker-selection-surface",
            "worker_id": worker_id,
            "assignment_policy": "deterministic_disjoint_round_robin",
            "selection_rules": [
                "Use only this worker's dedicated page/index; do not consume the other scheduled worker's page.",
                "This is a rebuildable index; canonical jobs, claims, papers, and relevance ledgers remain authoritative.",
                "Re-check canonical state immediately before work and skip rows that are no longer pending or are actively claimed.",
                "For Library-first runs, skip an identity already saved in ChatGPT Library as a completed pending GitHub import.",
            ],
            "research_audit": {
                "ready_total": research_ready,
                "claimable_total": len(research_all),
                "displayed": len(research[worker]),
                "rows": research[worker],
            },
            "discovery_review": {
                "pending_total": discovery_pending,
                "displayed": len(discovery[worker]),
                "rows": discovery[worker],
            },
        }
    return result


def _esc(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _link(label: Any, url: Any) -> str:
    label_s = _esc(label) or "source"
    url_s = str(url or "").strip()
    return f"[{label_s}]({url_s})" if url_s else label_s


def render_markdown(payload: dict[str, Any], worker: str) -> str:
    generated = str(payload.get("generated_at") or "")
    research = payload["research_audit"]
    discovery = payload["discovery_review"]
    out = [
        f"# Scheduled worker :{worker} worklist",
        "",
        f"Worker: `scheduled-chat-{worker}`  ",
        f"Generated: `{generated}`",
        "",
        "このページはこのworker専用の再構築可能な選択索引です。もう一方のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。",
        "正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。",
        "",
        "- このページに割り当てられた候補だけを使用する。",
        "- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。",
        "- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。",
        "",
        "## 未処理 Research / Audit",
        "",
        f"ready総数: **{research['ready_total']}** / 未claim総数: **{research['claimable_total']}** / このworker向け: **{research['displayed']}**",
        "",
        "| # | 種別 | identity | title | source | 想定配置先 |",
        "|---:|---|---|---|---|---|",
    ]
    for row in research["rows"]:
        out.append(
            "| {rank} | {kind} | {identity} | {title} | {source} | {path} |".format(
                rank=row["rank"],
                kind=_esc(row.get("type")),
                identity=_esc(row.get("canonical_id")),
                title=_esc(row.get("title")),
                source=_link("primary", row.get("source_url")),
                path=f"`{_esc(row.get('paper_path'))}`" if row.get("paper_path") else "",
            )
        )

    out.extend(
        [
            "",
            "## リスト入り判定待ち Discovery候補",
            "",
            f"未判定総数: **{discovery['pending_total']}** / このworker向け: **{discovery['displayed']}**",
            "",
            "| # | identity | title | year | 関連数 | 系統候補 | source |",
            "|---:|---|---|---:|---:|---|---|",
        ]
    )
    for row in discovery["rows"]:
        lineages = ", ".join(row.get("linked_from_lineages") or [])
        out.append(
            "| {rank} | {identity} | {title} | {year} | {relations} | {lineages} | {source} |".format(
                rank=row["rank"],
                identity=_esc(row.get("canonical_id")),
                title=_esc(row.get("title")),
                year=_esc(row.get("year") or row.get("published")),
                relations=_esc(row.get("relation_count")),
                lineages=_esc(lineages),
                source=_link("source", row.get("source_url")),
            )
        )
    out.extend(
        [
            "",
            "## Machine-readable",
            "",
            f"同じ割当は [worker-worklist-{worker}.json](worker-worklist-{worker}.json) にあります。",
            "",
        ]
    )
    return "\n".join(out)


def _paths(output_dir: Path, worker: str) -> tuple[Path, Path]:
    return (
        output_dir / f"worker-worklist-{worker}.json",
        output_dir / f"WORKLIST-{worker}.md",
    )


def write_outputs(root: Path, payloads: dict[str, dict[str, Any]], *, output_dir: Path) -> dict[str, dict[str, Any]]:
    base = output_dir if output_dir.is_absolute() else root / output_dir
    final: dict[str, dict[str, Any]] = {}
    for worker in WORKERS:
        json_path, markdown_path = _paths(base, worker)
        payload = payloads[worker]
        old = _read(json_path, {})
        old_cmp = dict(old) if isinstance(old, dict) else {}
        old_cmp.pop("generated_at", None)
        generated = (
            str(old.get("generated_at") or _now())
            if old_cmp == payload
            else _now()
        )
        worker_payload = {"generated_at": generated, **payload}
        _write_text(
            json_path,
            json.dumps(worker_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        _write_text(markdown_path, render_markdown(worker_payload, worker) + "\n")
        final[worker] = worker_payload
    return final


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".survey/work-queue"),
    )
    args = parser.parse_args()
    if args.limit <= 0:
        parser.error("--limit must be > 0")
    root = args.repo_root.resolve()
    payloads = build(root, limit=args.limit)
    final = write_outputs(root, payloads, output_dir=args.output_dir)
    print(
        json.dumps(
            {
                worker: {
                    "research_displayed": final[worker]["research_audit"]["displayed"],
                    "discovery_displayed": final[worker]["discovery_review"]["displayed"],
                }
                for worker in WORKERS
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
