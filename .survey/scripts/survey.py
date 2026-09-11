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
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

# ROOT is the .survey working root in production. Tests may point it at a
# temporary repository root directly. Keep state beneath ROOT, but resolve
# repository artifacts (papers/ and top-level READMEs) from repository_root().
ROOT = Path(__file__).resolve().parents[1]
STATE = "survey-state/"
PAPER_FAMILIES = ("inference", "training", "survey")


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
    """All repository paper families used by the canonical identity index.

    Citation matching must cross Inference, Training, and Survey without
    creating duplicate identities for papers that expose multiple identifiers.
    """
    repo = repository_root()
    old = read(STATE + "paper-identity-index.json", {}) or {}
    moved = set(old.get("ignored_moved_stubs", []))
    records = []
    paper_paths = []
    for family in PAPER_FAMILIES:
        paper_paths += list((repo / "papers" / family).glob("*/*.md"))
    for p in sorted(paper_paths):
        rel = p.relative_to(repo).as_posix()
        relative_family_path = rel.split("/", 2)[-1]
        if p.name == "README.md" or relative_family_path in moved:
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


def _extract_arxiv_id(meta, path):
    for value in (meta.get("arxiv_id"), meta.get("canonical_id"), meta.get("source"), meta.get("canonical_url")):
        if not value:
            continue
        m = re.search(r"(?:arxiv:|arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?", str(value), re.I)
        if m:
            return m.group(1)
        m = re.search(r"(?:arxiv:)?([a-z.-]+/(\d{4})\d{3})(?:v\d+)?", str(value), re.I)
        if m:
            return m.group(1)
    m = re.search(r"(?<!\d)(\d{4}\.\d{4,5})(?!\d)", path.name)
    return m.group(1) if m else None


def _publication_month(meta, path):
    published = str(meta.get("published") or "")
    m = re.match(r"^(\d{4})-(\d{2})", published)
    if m and 1 <= int(m.group(2)) <= 12:
        return int(m.group(1)), int(m.group(2))
    aid = _extract_arxiv_id(meta, path)
    if aid:
        if re.fullmatch(r"\d{4}\.\d{4,5}", aid):
            yy, mm = int(aid[:2]), int(aid[2:4])
            if 1 <= mm <= 12:
                return 2000 + yy, mm
        old = re.search(r"/(\d{2})(\d{2})\d{3}$", aid)
        if old and 1 <= int(old.group(2)) <= 12:
            yy = int(old.group(1))
            return (1900 + yy if yy >= 91 else 2000 + yy), int(old.group(2))
    year = meta.get("year")
    if str(year).isdigit():
        return int(year), None
    m = re.match(r"^(\d{4})-", path.name)
    return (int(m.group(1)), None) if m else (None, None)


def _month_number(year, month):
    return year * 12 + month - 1


def _recent_window(now=None):
    now = now or datetime.now(ZoneInfo("Asia/Tokyo"))
    end = (now.year, now.month)
    start_num = _month_number(*end) - 11
    start = (start_num // 12, start_num % 12 + 1)
    return start, end


def _legacy_title(body, path):
    m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    return m.group(1).strip() if m else path.stem


def _legacy_summary(body):
    m = re.search(r"^##\s+一文要約\s*$\n+(.*?)(?=\n##\s|\Z)", body, re.M | re.S)
    if not m:
        return ""
    value = m.group(1).strip()
    return re.sub(r"\s*\n\s*", " ", value)


def _explicit_implementation(meta, body=""):
    for key in ("code", "code_url", "implementation", "implementation_url", "repository", "repo"):
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            value = value.strip()
            if value.lower() not in {"none", "n/a", "na", "unknown", "未記録", "なし"}:
                return value
        elif value is True:
            return True
    status = str(meta.get("implementation_status") or "").strip().lower()
    if status and any(token in status for token in ("available", "released", "public", "official-code")):
        return True
    m = re.search(r"^[-*]\s*\*\*(?:実装|コード)\*\*:\s*(.+)$", body, re.M)
    if m:
        value = m.group(1).strip()
        url = re.search(r"https?://[^\s)>]+", value)
        return url.group(0) if url else True
    return None


def _view_identifiers(meta, path):
    ids = []
    aid = _extract_arxiv_id(meta, path)
    if aid:
        ids.append(("arxiv", re.sub(r"v\d+$", "", aid).lower()))
    doi = meta.get("doi")
    if doi:
        ids.append(("doi", re.sub(r"^(?:doi:|https?://doi.org/)", "", str(doi), flags=re.I).lower()))
    return ids


def paper_views():
    """Return render-only records for inference, training, and survey papers."""
    repo = repository_root()
    records = []
    for family in PAPER_FAMILIES:
        root = repo / "papers" / family
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.md")):
            if p.name == "README.md" or p.name == "comparison.md":
                continue
            rel = p.relative_to(repo).as_posix()
            meta, body = front(p)
            year, month = _publication_month(meta, p)
            records.append({
                "family": family,
                "lineage": p.parent.name,
                "path": rel,
                "file": p,
                "title": meta.get("title") or _legacy_title(body, p),
                "summary": meta.get("summary") or _legacy_summary(body),
                "year": year,
                "month": month,
                "identifiers": _view_identifiers(meta, p),
                "implementation": _explicit_implementation(meta, body),
                "meta": meta,
                "text": body,
            })
    return records


def _citation_counts(records):
    from citation_graph import citation_counts_from_view_records
    return citation_counts_from_view_records(records)

def _month_label(record):
    if record["year"] and record["month"]:
        return f"{record['year']:04d}-{record['month']:02d}"
    if record["year"]:
        return str(record["year"])
    return "未記録"


def _implementation_cell(value):
    if isinstance(value, str):
        if re.match(r"^https?://", value, re.I):
            return f"[✓]({value})"
        return "✓"
    return "✓" if value is True else "—"


def _sort_recent(record):
    return (record["year"] or 0, record["month"] or 0, record["title"].lower())


def _render_table(rows, citations, base_dir):
    if not rows:
        return ["該当なし。"]
    lines = [
        "| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |",
        "|---|---|:---:|---:|---|",
    ]
    for r in rows:
        link = Path(r["path"]).relative_to(base_dir).as_posix()
        lines.append(
            f"| {_month_label(r)} | [{cell(r['title'])}]({link}) | "
            f"{_implementation_cell(r['implementation'])} | {citations.get(r['path'], 0)} | {cell(r['summary'])} |"
        )
    return lines


def _render_taxonomy_list(rows, citations, base_dir, now=None):
    start, end = _recent_window(now)
    start_num, end_num = _month_number(*start), _month_number(*end)

    recent, cited, other = [], [], []
    for r in rows:
        is_recent = False
        if r["year"] and r["month"]:
            num = _month_number(r["year"], r["month"])
            is_recent = start_num <= num <= end_num
        if is_recent:
            recent.append(r)
        elif citations.get(r["path"], 0) > 0:
            cited.append(r)
        else:
            other.append(r)

    recent.sort(key=_sort_recent, reverse=True)
    cited.sort(key=lambda r: (citations.get(r["path"], 0),) + _sort_recent(r), reverse=True)
    other.sort(key=_sort_recent, reverse=True)

    period = f"{start[0]:04d}-{start[1]:02d}〜{end[0]:04d}-{end[1]:02d}"
    lines = [
        f"## 自動生成の論文一覧（{len(rows)}本）",
        "",
        f"分類は相互排他的。直近12か月は公開年月ベース（現在は **{period}**）。"
        "「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。",
        "「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。",
        "",
        f"### 直近12か月（{period}）",
        "",
    ]
    lines += _render_table(recent, citations, base_dir)
    lines += ["", "### 直近12か月より前・リポジトリ内で被引用", ""]
    lines += _render_table(cited, citations, base_dir)
    lines += ["", "### その他", ""]
    lines += _render_table(other, citations, base_dir)
    return "\n".join(lines)


def _migrate_legacy_training_list(path):
    """Remove the old hand-written training paper list before adding auto markers."""
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if "<!-- survey:auto:start -->" in content:
        return
    stripped = re.sub(r"\n## 収録論文\s*\n.*\Z", "\n", content, flags=re.S)
    if stripped != content:
        path.write_text(stripped.rstrip() + "\n", encoding="utf-8")


def _lineage_sort_key(item):
    name = item[0]
    return (1 if "other" in name.lower() else 0, name)


def _render_family_overview(family, rows):
    grouped = {}
    for r in rows:
        grouped.setdefault(r["lineage"], []).append(r)
    label = {"inference": "推論", "training": "学習", "survey": "サーベイ"}[family]
    lines = [
        "## 自動生成の収録状況",
        "",
        f"{label}論文：**{len(rows)}本**。",
        "",
        "| 系統 | 本数 |",
        "|---|---:|",
    ]
    lines += [f"| [{k}]({k}/README.md) | {len(v)} |" for k, v in sorted(grouped.items(), key=_lineage_sort_key)]
    if not grouped:
        lines.append("| — | 0 |")
    family_readme = repository_root() / "papers" / family / "README.md"
    if family_readme.exists():
        content = family_readme.read_text(encoding="utf-8")
        content = re.sub(r"収録論文: \*\*\d+本\*\*", f"収録論文: **{len(rows)}本**", content)
        family_readme.write_text(content, encoding="utf-8")
    block(f"papers/{family}/README.md", "\n".join(lines))


def render_indexes(records, now=None):
    repo = repository_root()
    citations = _citation_counts(records)
    by_family = {family: [] for family in PAPER_FAMILIES}
    by_taxonomy = {}
    for r in records:
        by_family.setdefault(r["family"], []).append(r)
        by_taxonomy.setdefault((r["family"], r["lineage"]), []).append(r)

    for (family, lineage), rows in sorted(by_taxonomy.items()):
        readme = repo / "papers" / family / lineage / "README.md"
        if family == "training":
            _migrate_legacy_training_list(readme)
        base_dir = Path("papers") / family / lineage
        block(f"papers/{family}/{lineage}/README.md", _render_taxonomy_list(rows, citations, base_dir, now=now))

    for family in PAPER_FAMILIES:
        if (repo / "papers" / family).exists():
            _render_family_overview(family, by_family.get(family, []))
    return by_family


def _update_catalog_counts(by_family):
    repo = repository_root()
    counts = {family: len(by_family.get(family, [])) for family in PAPER_FAMILIES}
    total = sum(counts.values())
    p = repo / "papers/README.md"
    if p.exists():
        content = p.read_text(encoding="utf-8")
        content = re.sub(r"収録論文: \*\*\d+本\*\*。", f"収録論文: **{total}本**。", content)
        content = re.sub(r"## Inference / 推論 — \d+本", f"## Inference / 推論 — {counts['inference']}本", content)
        content = re.sub(r"## Training / 学習 — \d+本", f"## Training / 学習 — {counts['training']}本", content)
        content = re.sub(r"## Survey / サーベイ — \d+本", f"## Survey / サーベイ — {counts['survey']}本", content)
        for family, rows in by_family.items():
            lineage_counts = {}
            for row in rows:
                lineage_counts[row["lineage"]] = lineage_counts.get(row["lineage"], 0) + 1
            for lineage, count in lineage_counts.items():
                pattern = r"(\]\(" + re.escape(f"{family}/{lineage}/") + r"\)\s*—\s*)\d+本"
                content = re.sub(pattern, lambda m, count=count: m.group(1) + str(count) + "本", content)
        p.write_text(content, encoding="utf-8")
        block("papers/README.md", f"推論：**{counts['inference']}本** ／ 学習：**{counts['training']}本** ／ サーベイ：**{counts['survey']}本**。 [推論一覧](inference/README.md) ／ [学習一覧](training/README.md) ／ [サーベイ一覧](survey/README.md) ／ [研究比較](inference/comparison.md)")
    root = repo / "README.md"
    if root.exists():
        content = root.read_text(encoding="utf-8")
        content = re.sub(r"現在の論文収録数: .*", f"現在の論文収録数: **{total}本**（推論{counts['inference']}本 + 学習{counts['training']}本 + サーベイ{counts['survey']}本）", content)
        content = re.sub(r"- \[Inference / 推論\]\(papers/inference/\) — \*\*\d+本\*\*", f"- [Inference / 推論](papers/inference/) — **{counts['inference']}本**", content)
        content = re.sub(r"- \[Training / 学習\]\(papers/training/\) — \*\*\d+本（凍結）\*\*", f"- [Training / 学習](papers/training/) — **{counts['training']}本（凍結）**", content)
        survey_line = f"  - [Survey / サーベイ](papers/survey/) — **{counts['survey']}本**"
        if "[Survey / サーベイ](papers/survey/)" not in content:
            training_line = re.search(r"^  - \[Training / 学習\].*$", content, flags=re.M)
            if training_line:
                content = content[:training_line.end()] + "\n" + survey_line + content[training_line.end():]
        else:
            content = re.sub(r"^  - \[Survey / サーベイ\]\(papers/survey/\) — \*\*\d+本\*\*$", survey_line, content, flags=re.M)
        root.write_text(content, encoding="utf-8")
        block("README.md", f"推論：**{counts['inference']}本** ／ 学習：**{counts['training']}本** ／ サーベイ：**{counts['survey']}本**。 [推論一覧](papers/inference/README.md) ／ [学習一覧](papers/training/README.md) ／ [サーベイ一覧](papers/survey/README.md) ／ [研究比較](papers/inference/comparison.md)")


def _comparison_link(path):
    if path.startswith("papers/inference/"):
        return path.removeprefix("papers/inference/")
    if path.startswith("papers/"):
        return "../" + path.removeprefix("papers/")
    return path


def render_comparison(records):
    cols = [("summary", "一文要約"), ("topics", "主題"), ("storage_targets", "保存・転送対象"), ("bottlenecks", "改善対象"), ("hardware_evaluation", "評価方式"), ("hardware_details", "評価機器"), ("quality_effect", "品質への影響"), ("code", "実装"), ("evidence_locations", "主要結果の出典")]
    lines = ["# 推論研究の横断比較", "", "既存の明示属性だけを表示する。未記録は未確認であり、非対応・実装なしを意味しない。本文の数値から自動推測しない。", "", "| 論文 | " + " | ".join(v for _, v in cols) + " |", "|---|" + "---|" * len(cols)]
    lines += ["| [" + cell(r["title"]) + "](" + _comparison_link(r["path"]) + ") | " + " | ".join(cell(r["meta"].get(k)) for k, _ in cols) + " |" for r in records]
    put_text("papers/inference/comparison.md", "\n".join(lines) + "\n")


def render():
    inference_records = papers()
    write(STATE + "paper-identity-index.json", identity(inference_records))
    view_records = paper_views()
    by_family = render_indexes(view_records)
    _update_catalog_counts(by_family)
    render_comparison(inference_records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    args = parser.parse_args()
    global ROOT
    if args.root:
        candidate = args.root.resolve()
        ROOT = candidate / ".survey" if (candidate / ".survey").is_dir() else candidate
    if args.cmd == "build":
        render()


if __name__ == "__main__":
    main()
