#!/usr/bin/env python3
"""Build the shared top/bottom worklist used by scheduled survey workers.

The output is a rebuildable selection surface only. Canonical job/claim state and
reference relevance ledgers remain authoritative. A worker must re-check canonical
state immediately before doing content work.
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

DEFAULT_LIMIT = 100
DEFAULT_JSON = Path(".survey/work-queue/worker-worklist.json")
DEFAULT_MARKDOWN = Path(".survey/work-queue/WORKLIST.md")


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


def _research_rows(root: Path, *, limit: int) -> tuple[list[dict[str, Any]], int, int]:
    jobs = _jobs(root)
    claims = claim_state.current_claims(root)
    ready = [
        row
        for row in jobs
        if row.get("status") == "ready"
        and row.get("type") in {"research", "audit"}
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
    selected: list[dict[str, Any]] = []
    for rank, row in enumerate(claimable[:limit], start=1):
        selected.append(
            {
                "rank": rank,
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
    return selected, len(ready), len(claimable)


def _discovery_rows(root: Path, *, limit: int) -> tuple[list[dict[str, Any]], int]:
    pool = reference_pool.build_reference_pool(root)
    source = pool.get("candidates")
    candidates = source if isinstance(source, list) else []
    selected: list[dict[str, Any]] = []
    for rank, row in enumerate(candidates[:limit], start=1):
        if not isinstance(row, dict):
            continue
        selected.append(
            {
                "rank": rank,
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
    return selected, int(pool.get("candidate_count") or len(candidates))


def build(root: Path, *, limit: int) -> dict[str, Any]:
    research, research_ready, research_claimable = _research_rows(root, limit=limit)
    discovery, discovery_pending = _discovery_rows(root, limit=limit)
    return {
        "schema_version": 1,
        "purpose": "scheduled-worker-selection-surface",
        "limits": {
            "research_audit": limit,
            "discovery_review": limit,
        },
        "worker_directions": {
            "scheduled-chat-00": {
                "direction": "top_to_bottom",
                "rank_order": "ascending",
            },
            "scheduled-chat-30": {
                "direction": "bottom_to_top",
                "rank_order": "descending",
            },
        },
        "selection_rules": [
            "This file is a rebuildable index; canonical jobs, claims, papers, and relevance ledgers remain authoritative.",
            "Re-check canonical state immediately before work and skip rows that are no longer pending or are actively claimed.",
            "For Library-first runs, skip a paper identity already saved in ChatGPT Library as a completed pending GitHub import.",
            "scheduled-chat-00 scans from rank 1 upward; scheduled-chat-30 scans from the largest displayed rank downward.",
        ],
        "research_audit": {
            "ready_total": research_ready,
            "claimable_total": research_claimable,
            "displayed": len(research),
            "rows": research,
        },
        "discovery_review": {
            "pending_total": discovery_pending,
            "displayed": len(discovery),
            "rows": discovery,
        },
    }


def _esc(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _link(label: Any, url: Any) -> str:
    label_s = _esc(label) or "source"
    url_s = str(url or "").strip()
    return f"[{label_s}]({url_s})" if url_s else label_s


def render_markdown(payload: dict[str, Any]) -> str:
    generated = str(payload.get("generated_at") or "")
    research = payload["research_audit"]
    discovery = payload["discovery_review"]
    out = [
        "# Scheduled worker shared worklist",
        "",
        f"Generated: `{generated}`",
        "",
        "このページは再構築可能な選択索引です。正本は `.survey/work-queue/jobs/`、claim、論文実体、"
        "およびrelevance ledgerです。処理直前に最新正本を再確認してください。",
        "",
        "- `scheduled-chat-00`: **上から下**へ処理する。",
        "- `scheduled-chat-30`: **下から上**へ処理する。",
        "- Library-first runでは、同じidentityの完成原稿・探索結果がすでにChatGPT Libraryへ保存済みならskipする。",
        "- 行が最新状態で処理済み・claim済み・対象外になっていればskipし、次の行へ進む。",
        "",
        "## 未処理 Research / Audit",
        "",
        f"ready総数: **{research['ready_total']}** / 未claim総数: **{research['claimable_total']}** / 表示: **{research['displayed']}**",
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
            f"未判定総数: **{discovery['pending_total']}** / 表示: **{discovery['displayed']}**",
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
            "同じ内容は [worker-worklist.json](worker-worklist.json) にあります。Scheduled workerはMarkdownの表を解析せず、可能ならJSONを使用します。",
            "",
        ]
    )
    return "\n".join(out)


def write_outputs(
    root: Path,
    payload: dict[str, Any],
    *,
    json_output: Path,
    markdown_output: Path,
) -> dict[str, Any]:
    json_path = json_output if json_output.is_absolute() else root / json_output
    markdown_path = markdown_output if markdown_output.is_absolute() else root / markdown_output

    old = _read(json_path, {})
    old_cmp = dict(old) if isinstance(old, dict) else {}
    old_cmp.pop("generated_at", None)
    if old_cmp == payload:
        generated = str(old.get("generated_at") or _now())
    else:
        generated = _now()

    final = {"generated_at": generated, **payload}
    _write_text(
        json_path,
        json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    _write_text(markdown_path, render_markdown(final) + "\n")
    return final


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()
    if args.limit <= 0:
        parser.error("--limit must be > 0")
    root = args.repo_root.resolve()
    payload = build(root, limit=args.limit)
    final = write_outputs(
        root,
        payload,
        json_output=args.json_output,
        markdown_output=args.markdown_output,
    )
    print(
        json.dumps(
            {
                "generated_at": final["generated_at"],
                "research_displayed": final["research_audit"]["displayed"],
                "research_claimable_total": final["research_audit"]["claimable_total"],
                "discovery_displayed": final["discovery_review"]["displayed"],
                "discovery_pending_total": final["discovery_review"]["pending_total"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
