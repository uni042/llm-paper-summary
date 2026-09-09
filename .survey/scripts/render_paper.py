#!/usr/bin/env python3
"""Render a validated workflow-v10 structured research record into repository Markdown."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def q(value: Any) -> str:
    """YAML-safe double-quoted scalar via JSON string encoding."""
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(x).strip() for x in value if str(x).strip())
    return str(value).strip()


def bullets(items: Any) -> str:
    if not items:
        return ""
    if not isinstance(items, list):
        items = [items]
    out = []
    for item in items:
        if isinstance(item, dict):
            name = text(item.get("name") or item.get("label") or item.get("metric"))
            desc = text(item.get("description") or item.get("value") or item.get("text"))
            if name and desc:
                out.append(f"- **{name}**: {desc}")
            elif desc:
                out.append(f"- {desc}")
            elif name:
                out.append(f"- {name}")
        else:
            s = text(item)
            if s:
                out.append(f"- {s}")
    return "\n".join(out)


def render_result(item: dict[str, Any]) -> str:
    metric = text(item.get("metric"))
    value = text(item.get("value"))
    baseline = text(item.get("baseline"))
    condition = text(item.get("condition"))
    interpretation = text(item.get("interpretation"))
    head = " / ".join(x for x in [metric, value] if x)
    details = []
    if baseline:
        details.append(f"比較対象: {baseline}")
    if condition:
        details.append(f"条件: {condition}")
    if details:
        head += f" ({'; '.join(details)})"
    if interpretation:
        head += f" — {interpretation}"
    return f"- {head}" if head else ""


def section(title: str, body: str) -> str:
    body = body.strip()
    return f"## {title}\n{body}\n\n" if body else ""


def render_paper(record: dict[str, Any]) -> str:
    meta = record.get("metadata") or {}
    pm = record.get("problem_method") or {}
    ev = record.get("evaluation") or {}
    rs = record.get("results") or {}
    pos = record.get("positioning") or {}

    title = text(meta.get("title"))
    canonical_id = text(meta.get("canonical_id"))
    source = text(meta.get("source"))
    summary = text(meta.get("summary"))
    if not title or not canonical_id or not source or not summary:
        raise ValueError("metadata requires title, canonical_id, source, and summary")

    front = ["---", f"canonical_id: {q(canonical_id)}"]
    for key in ("arxiv_id", "doi", "openreview_id"):
        if meta.get(key):
            front.append(f"{key}: {q(meta[key])}")
    front += [
        f"title: {q(title)}",
        f"summary: {q(summary)}",
        f"source: {q(source)}",
        f"last_audited: {q(meta.get('last_audited')) if meta.get('last_audited') else 'null'}",
        f"audit_version: {int(meta.get('audit_version') or 0)}",
        "---",
        "",
        f"# {title}",
        "",
        f"> {summary}",
        "",
    ]

    bib = []
    authors = meta.get("authors")
    if authors:
        if isinstance(authors, list):
            authors = ", ".join(text(x) for x in authors if text(x))
        bib.append(f"- **著者**: {text(authors)}")
    if meta.get("publication"):
        bib.append(f"- **公開**: {text(meta['publication'])}")
    if meta.get("publication_type"):
        bib.append(f"- **種別**: {text(meta['publication_type'])}")
    if meta.get("topics"):
        topics = meta["topics"]
        if isinstance(topics, list):
            topics = "、".join(text(x) for x in topics if text(x))
        bib.append(f"- **対象**: {text(topics)}")
    if meta.get("implementation"):
        bib.append(f"- **実装**: {text(meta['implementation'])}")

    parts = ["\n".join(front)]
    parts.append(section("書誌情報", "\n".join(bib)))
    problem = text(pm.get("problem"))
    novelty = text(pm.get("novelty"))
    if problem:
        parts.append(section("問題設定", problem))
    if novelty:
        parts.append(section("新規性", novelty))

    method_body = []
    if pm.get("method_overview"):
        method_body.append("### 手法のあらまし\n" + text(pm["method_overview"]))
    for comp in pm.get("components") or []:
        if isinstance(comp, dict):
            name = text(comp.get("name"))
            desc = text(comp.get("description"))
            if name:
                method_body.append(f"### {name}\n{desc}" if desc else f"### {name}")
            elif desc:
                method_body.append(desc)
        else:
            s = text(comp)
            if s:
                method_body.append(s)
    if pm.get("system_design"):
        method_body.append("### 全体のデータ／制御の流れ\n" + text(pm["system_design"]))
    parts.append(section("手法", "\n\n".join(method_body)))

    eval_lines = []
    for label, key in [
        ("Hardware", "hardware"), ("Software", "software"), ("Model", "model"),
        ("Dataset / Trace", "datasets"), ("Baseline", "baselines"), ("Correctness", "correctness"),
    ]:
        value = ev.get(key)
        if value:
            if isinstance(value, list):
                value = "、".join(text(x) if not isinstance(x, dict) else text(x.get("description") or x.get("name")) for x in value)
            eval_lines.append(f"- **{label}**: {text(value)}")
    if ev.get("settings"):
        eval_lines.append(bullets(ev["settings"]))
    if ev.get("methodology"):
        eval_lines.append(text(ev["methodology"]))
    if ev.get("scope"):
        eval_lines.append(text(ev["scope"]))
    parts.append(section("評価条件", "\n".join(x for x in eval_lines if x)))

    result_lines = []
    if rs.get("overview"):
        result_lines.append(text(rs["overview"]))
    for item in rs.get("key_results") or []:
        if isinstance(item, dict):
            line = render_result(item)
            if line:
                result_lines.append(line)
    if rs.get("negative_results"):
        result_lines.append("### 負の結果・境界条件\n" + bullets(rs["negative_results"]))
    if rs.get("interpretation"):
        result_lines.append("### 結果の読み方\n" + text(rs["interpretation"]))
    parts.append(section("主要結果", "\n\n".join(result_lines)))

    if rs.get("quality_impact"):
        parts.append(section("品質への影響", text(rs["quality_impact"])))
    differences = pos.get("differences")
    if differences:
        parts.append(section("既存研究との差", bullets(differences) if isinstance(differences, list) else text(differences)))
    limitations = pos.get("limitations")
    if limitations:
        parts.append(section("限界", bullets(limitations) if isinstance(limitations, list) else text(limitations)))
    if pos.get("implementation_status"):
        parts.append(section("実装状態", text(pos["implementation_status"])))
    if pos.get("research_positioning"):
        parts.append(section("研究上の位置づけ", text(pos["research_positioning"])))
    if pos.get("audit_notes"):
        parts.append(section("監査メモ", text(pos["audit_notes"])))

    sources = meta.get("sources") or [source]
    src_lines, seen = [], set()
    for s in sources:
        u = text(s)
        if u and u not in seen:
            seen.add(u)
            src_lines.append(f"- {u}")
    parts.append(section("一次資料", "\n".join(src_lines)))

    rendered = "\n".join(p.rstrip() for p in parts if p).rstrip() + "\n"
    if len(rendered.encode("utf-8")) < 500:
        raise ValueError("rendered paper is unexpectedly short")
    return rendered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    record = json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(render_paper(record), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
