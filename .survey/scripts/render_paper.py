#!/usr/bin/env python3
"""Render a validated workflow-v10 structured research record into repository Markdown."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def q(value: Any) -> str:
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
    out: list[str] = []
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
    details: list[str] = []
    if baseline:
        details.append(f"比較対象: {baseline}")
    if condition:
        details.append(f"条件: {condition}")
    if details:
        head += f" ({'; '.join(details)})"
    if interpretation:
        head += f" — {interpretation}"
    return f"- {head}" if head else ""


def representative_result_text(item: Any) -> str:
    """Turn the first key result into a self-contained overview sentence."""
    if not isinstance(item, dict):
        return ""
    metric = text(item.get("metric"))
    value = text(item.get("value"))
    baseline = text(item.get("baseline"))
    condition = text(item.get("condition"))
    interpretation = text(item.get("interpretation"))
    if not (metric and value):
        return ""

    sentence = "代表結果として、"
    sentence += metric
    if condition:
        sentence += f"は{condition}で"
    else:
        sentence += "は"
    if baseline:
        sentence += f"{baseline}に対して"
    sentence += value.rstrip("。") + "。"
    if interpretation:
        sentence += interpretation.rstrip("。") + "。"
    return sentence


def build_overview(meta: dict[str, Any], pm: dict[str, Any], rs: dict[str, Any]) -> str:
    """Build an overview that always exposes method intent and a headline result."""
    parts: list[str] = []
    base = text(meta.get("overview") or meta.get("summary"))
    novelty = text(pm.get("novelty"))
    key_results = rs.get("key_results") or []
    headline = representative_result_text(key_results[0]) if key_results else ""

    for value in (base, novelty, headline):
        value = value.strip()
        if not value:
            continue
        joined = "\n\n".join(parts)
        if value in joined:
            continue
        if headline and value == headline and text(key_results[0].get("value")) in joined:
            continue
        parts.append(value)
    return "\n\n".join(parts)


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

    front_order = (
        "canonical_id", "arxiv_id", "doi", "openreview_id", "arxiv_categories",
        "title", "summary", "authors", "authors_affiliations", "published",
        "publication", "publication_type", "publication_status", "publication_version",
        "lineage", "topics",
        "importance", "hardware_evaluation", "hardware_details", "quality_effect",
        "storage_targets", "bottlenecks", "evidence_locations",
        "references", "references_checked_at", "references_source", "references_total",
        "source", "sources", "code", "implementation", "implementation_status", "evaluation_type",
        "last_checked", "last_audited", "audit_version",
    )
    front_meta: dict[str, Any] = {}
    for key in front_order:
        if key in meta and meta[key] not in (None, "", []):
            front_meta[key] = meta[key]
    front_meta["canonical_id"] = canonical_id
    front_meta["title"] = title
    front_meta["summary"] = summary
    front_meta["source"] = source
    if "references" in meta:
        front_meta["references"] = meta["references"]
    front_meta.setdefault("last_audited", None)
    front_meta["audit_version"] = int(meta.get("audit_version") or 0)
    yaml_text = yaml.safe_dump(
        front_meta,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    front = [
        "---", yaml_text, "---", "", f"# {title}", "", f"> {summary}", "",
    ]

    bib: list[str] = []
    authors = meta.get("authors")
    if authors:
        if isinstance(authors, list):
            authors = ", ".join(text(x) for x in authors if text(x))
        bib.append(f"- **著者**: {text(authors)}")
    if meta.get("authors_affiliations"):
        bib.append(f"- **著者・所属**: {text(meta['authors_affiliations'])}")
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
    parts.append(section("概要", build_overview(meta, pm, rs)))
    if pm.get("problem"):
        parts.append(section("問題設定", text(pm["problem"])))
    if pm.get("novelty"):
        parts.append(section("新規性", text(pm["novelty"])))

    method_body: list[str] = []
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

    eval_lines: list[str] = []
    for label, key in [
        ("ハードウェア", "hardware"),
        ("ソフトウェア", "software"),
        ("モデル", "model"),
        ("データセット／トレース", "datasets"),
        ("比較対象", "baselines"),
        ("正確性・品質", "correctness"),
    ]:
        value = ev.get(key)
        if value:
            if isinstance(value, list):
                value = "、".join(
                    text(x) if not isinstance(x, dict)
                    else text(x.get("description") or x.get("name"))
                    for x in value
                )
            eval_lines.append(f"- **{label}**: {text(value)}")
    if ev.get("settings"):
        eval_lines.append(bullets(ev["settings"]))
    if ev.get("methodology"):
        eval_lines.append(text(ev["methodology"]))
    if ev.get("scope"):
        eval_lines.append(text(ev["scope"]))
    parts.append(section("評価条件", "\n".join(x for x in eval_lines if x)))

    result_lines: list[str] = []
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
    if pos.get("differences"):
        value = pos["differences"]
        parts.append(section("既存研究との差", bullets(value) if isinstance(value, list) else text(value)))
    if pos.get("limitations"):
        value = pos["limitations"]
        parts.append(section("限界", bullets(value) if isinstance(value, list) else text(value)))
    if pos.get("implementation_status"):
        parts.append(section("実装状態", text(pos["implementation_status"])))
    if pos.get("research_positioning"):
        parts.append(section("研究上の位置づけ", text(pos["research_positioning"])))
    if pos.get("audit_notes"):
        parts.append(section("監査メモ", text(pos["audit_notes"])))

    sources = meta.get("sources") or [source]
    src_lines: list[str] = []
    seen: set[str] = set()
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