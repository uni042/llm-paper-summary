#!/usr/bin/env python3
"""Deterministic helpers used by the current queue worker.

This module intentionally contains only the identity and derived-view functions
needed by workflow v10. Runtime scheduling, leases, retries, and daily planning
live in the v10 work queue and are not duplicated here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml

# ROOT is the .survey working root in production. Tests may point it at a
# temporary repository root directly. Keep state beneath ROOT, but resolve
# repository artifacts (papers/ and top-level READMEs) from repository_root().
ROOT = Path(__file__).resolve().parents[1]
STATE = "survey-state/"


def repository_root() -> Path:
    root = ROOT.resolve()
    return root.parent if root.name == ".survey" else root


def read(path, default=None):
    p = ROOT / path
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str) + "\n"
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(p)


def front(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1]) or {}, parts[2]


def norm_id(value):
    value = str(value).strip()
    if value.lower().startswith("arxiv:"):
        basic = re.sub(r"v\d+$", "", value.split(":", 1)[1])
        if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})", basic, re.I):
            raise ValueError("Invalid arXiv ID: " + value)
        return "arXiv:" + basic
    if value.lower().startswith(("doi:", "https://doi.org/", "http://doi.org/")):
        return "DOI:" + re.sub(r"^(?:doi:|https?://doi.org/)", "", value, flags=re.I).lower()
    return value


def papers():
    repo = repository_root()
    old = read(STATE + "paper-identity-index.json", {}) or {}
    moved = set(old.get("ignored_moved_stubs", []))
    records = []
    for p in sorted((repo / "papers/inference").glob("*/*.md")):
        rel = p.relative_to(repo).as_posix()
        if p.name == "README.md" or rel.removeprefix("papers/inference/") in moved:
            continue
        meta, _ = front(p)
        cid = meta.get("canonical_id")
        if not cid:
            raise ValueError("Missing canonical_id: " + rel)
        ids = [norm_id(cid)]
        for key, prefix in [("arxiv_id", "arXiv:"), ("doi", "DOI:"), ("openreview_id", "OpenReview:")]:
            if meta.get(key):
                ids.append(norm_id(prefix + str(meta[key])))
        records.append({
            "canonical_id": norm_id(cid),
            "path": rel,
            "identifiers": sorted(set(ids)),
            "title": meta.get("title", ""),
            "summary": meta.get("summary", ""),
            "lineage": p.parent.name,
            "source_hash": hashlib.sha256(p.read_bytes()).hexdigest(),
            "meta": meta,
        })
    return records


def identity(records):
    result = {}
    aliases = {}
    for r in records:
        for key in r["identifiers"]:
            if key in aliases and aliases[key] != r["canonical_id"]:
                raise ValueError("Duplicate identifier: " + key)
            aliases[key] = r["canonical_id"]
        if r["canonical_id"] in result:
            raise ValueError("Duplicate paper: " + r["canonical_id"])
        result[r["canonical_id"]] = {k: v for k, v in r.items() if k in ("path", "identifiers", "source_hash")}
    old = read(STATE + "paper-identity-index.json", {}) or {}
    return {
        "schema_version": 3,
        "active_count": len(result),
        "papers": result,
        "identifier_to_canonical": aliases,
        "ignored_moved_stubs": old.get("ignored_moved_stubs", []),
    }


def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, default=str)
    return str(value if value not in (None, "", []) else "未記録").replace("|", "\\|").replace("\n", " ")


def put_text(path, text):
    p = repository_root() / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def block(path, text):
    p = repository_root() / path
    p.parent.mkdir(parents=True, exist_ok=True)
    content = p.read_text(encoding="utf-8") if p.exists() else ""
    start, end = "<!-- survey:auto:start -->", "<!-- survey:auto:end -->"
    replacement = start + "\n" + text + "\n" + end
    if start in content:
        content = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: replacement, content, flags=re.S)
    else:
        content = (content.rstrip() + "\n\n" if content.strip() else "") + replacement + "\n"
    p.write_text(content, encoding="utf-8")


def render():
    repo = repository_root()
    records = papers()
    write(STATE + "paper-identity-index.json", identity(records))
    grouped = {}
    for r in records:
        grouped.setdefault(r["lineage"], []).append(r)
    for lineage, rows in grouped.items():
        rows.sort(key=lambda r: (str(r["meta"].get("published", "")), r["canonical_id"]), reverse=True)
        lines = [f"## 自動生成の論文一覧（{len(rows)}本）", "", "| 論文 | 一文要約 |", "|---|---|"]
        lines += [f"| [{cell(r['title'])}]({Path(r['path']).name}) | {cell(r['summary'])} |" for r in rows]
        block(f"papers/inference/{lineage}/README.md", "\n".join(lines))
    overview = ["## 自動生成の収録状況", "", f"推論論文：**{len(records)}本**（移動案内を除く）。", "", "| 系統 | 本数 |", "|---|---:|"]
    overview += [f"| [{k}]({k}/README.md) | {len(v)} |" for k, v in sorted(grouped.items())]
    block("papers/inference/README.md", "\n".join(overview))
    for path in ["papers/inference/README.md", "papers/README.md", "README.md"]:
        p = repo / path
        content = p.read_text(encoding="utf-8")
        for lineage, rows in grouped.items():
            content = re.sub(r"(\]\((?:inference/)?" + re.escape(lineage) + r"/\) — )\d+本", lambda m: m[1] + str(len(rows)) + "本", content)
        if path == "papers/inference/README.md":
            content = re.sub(r"収録論文: \*\*\d+本\*\*", f"収録論文: **{len(records)}本**", content)
        elif path == "papers/README.md":
            training = len(list((repo / "papers/training").glob("*/*.md"))) - len(list((repo / "papers/training").glob("*/README.md")))
            content = re.sub(r"収録論文: \*\*\d+本\*\*", f"収録論文: **{len(records) + training}本**", content)
            content = re.sub(r"## Inference / 推論 — \d+本", f"## Inference / 推論 — {len(records)}本", content)
        else:
            training = len(list((repo / "papers/training").glob("*/*.md"))) - len(list((repo / "papers/training").glob("*/README.md")))
            content = re.sub(r"(\[Inference / 推論\]\(papers/inference/\) — \*\*)\d+本", lambda m: m[1] + str(len(records)) + "本", content)
            content = re.sub(r"現在の論文収録数: .*", f"現在の論文収録数: **{len(records) + training}本**（推論{len(records)}本 + 学習{training}本）", content)
        p.write_text(content, encoding="utf-8")
    for path, prefix in [("papers/README.md", "inference/"), ("README.md", "papers/inference/")]:
        block(path, f"推論論文：**{len(records)}本**。 [全一覧]({prefix}README.md) ／ [研究比較]({prefix}comparison.md)")
    cols = [("summary", "一文要約"), ("topics", "主題"), ("storage_targets", "保存・転送対象"), ("bottlenecks", "改善対象"), ("hardware_evaluation", "評価方式"), ("hardware_details", "評価機器"), ("quality_effect", "品質への影響"), ("code", "実装"), ("evidence_locations", "主要結果の出典")]
    lines = ["# 推論研究の横断比較", "", "既存の明示属性だけを表示する。未記録は未確認であり、非対応・実装なしを意味しない。本文の数値から自動推測しない。", "", "| 論文 | " + " | ".join(v for _, v in cols) + " |", "|---|" + "---|" * len(cols)]
    lines += ["| [" + cell(r["title"]) + "](" + r["path"].removeprefix("papers/inference/") + ") | " + " | ".join(cell(r["meta"].get(k)) for k, _ in cols) + " |" for r in records]
    put_text("papers/inference/comparison.md", "\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    args = parser.parse_args()
    global ROOT
    if args.root:
        ROOT = args.root.resolve()
    if args.cmd == "build":
        render()


if __name__ == "__main__":
    main()
