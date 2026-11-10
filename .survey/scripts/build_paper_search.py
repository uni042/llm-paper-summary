#!/usr/bin/env python3
"""Build static Japanese paper search pages from the canonical survey views."""
from __future__ import annotations

import argparse
import gzip
import html
import io
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import survey  # noqa: E402

MANIFEST = ".paper-search-manifest.json"
DEFAULT_SITE = "https://uni042.github.io/llm-paper-summary/"
DEFAULT_REPO = "https://github.com/uni042/llm-paper-summary/blob/main/"
FAMILIES = (("inference", "推論"), ("training", "学習"), ("survey", "サーベイ"))


def visible_text(markdown: str) -> str:
    """Return visible markdown text, excluding frontmatter, comments, and URLs."""
    text = markdown.replace("\r\n", "\n")
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[`*_>#~|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _clean_summary(value: str) -> str:
    return visible_text(value or "")


def overview_section(markdown: str) -> str:
    """Extract the Markdown section headed exactly ``##... 概要``."""
    headers = list(re.finditer(r"(?m)^(#{1,6})[ \t]+概要[ \t]*#*[ \t]*$", markdown))
    if not headers:
        return ""
    header = headers[0]
    level = len(header.group(1))
    next_header = re.search(rf"(?m)^#{{1,{level}}}[ \t]+", markdown[header.end():])
    end = header.end() + next_header.start() if next_header else len(markdown)
    return markdown[header.end():end].strip()


def _paper_record(row: dict, citations: dict, repo_url: str, now) -> dict:
    month = row.get("month")
    year = row.get("year")
    date = f"{year:04d}-{month:02d}" if year and month else (str(year) if year else "")
    start, end = survey._recent_window(now)
    cited = int(citations.get(row["path"], 0) or 0)
    recent = bool(year and month and (start <= (year, month) <= end))
    repo_path = "/".join(quote(part, safe="-._~") for part in row["path"].split("/"))
    meta = row.get("meta") or {}
    summary_sources = [meta.get("summary"), meta.get("list_summary"), row.get("summary"), overview_section(str(row.get("text") or ""))]
    summaries = []
    for source in summary_sources:
        cleaned = _clean_summary(str(source or ""))
        if cleaned and cleaned not in summaries:
            summaries.append(cleaned)
    return {
        "path": row["path"], "family": row["family"], "lineage": row["lineage"],
        "title": _clean_summary(str(row.get("title") or "")),
        "summary": " ".join(summaries),
        "summary_display": _clean_summary(str(row.get("summary") or "")),
        "body": unicodedata.normalize("NFKC", visible_text(str(row.get("text") or ""))),
        "year": year, "date": date, "citations": cited,
        "attention": bool(recent and cited >= 1),
        "implementation": row.get("implementation"),
        "source_url": repo_url.rstrip("/") + "/" + repo_path,
    }


def _safe_scope(scope: str) -> str:
    if scope in ("", "all"):
        return ""
    parts = scope.split("/")
    if len(parts) not in (1, 2) or parts[0] not in {f[0] for f in FAMILIES}:
        raise ValueError(f"Invalid search scope: {scope}")
    if len(parts) == 2 and (not parts[1] or parts[1] in {".", ".."} or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", parts[1])):
        raise ValueError(f"Invalid lineage scope: {scope}")
    return "/".join(parts)


def _page_html(scope: str, label: str, base: str, lineages: list[str] | None = None) -> str:
    scope = _safe_scope(scope)
    depth = 0 if not scope else len(scope.split("/"))
    asset = "../" * depth
    escaped_scope = html.escape(scope, quote=True)
    nav = [f'<a href="{asset}index.html">全体検索</a>'] if depth else []
    nav += [f'<a href="{html.escape(asset + family + "/index.html", quote=True)}">{name}検索</a>' for family, name in FAMILIES]
    if depth == 2:
        nav.append(f'<a href="{html.escape(asset + scope.split("/")[0] + "/index.html", quote=True)}">区分へ戻る</a>')
    breadcrumb = "<nav aria-label=\"パンくず\">" + " / ".join(nav) + "</nav>"
    lineage_links = ""
    if depth == 1 and lineages:
        links = " ".join(f'<a href="{html.escape(lineage, quote=True)}/index.html">{html.escape(lineage)}</a>' for lineage in sorted(lineages))
        lineage_links = f'<nav aria-label="系統">系統検索: {links}</nav>'
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(label)} | 日本語論文解説検索</title><link rel="stylesheet" href="{asset}assets/style.css">
<script defer src="{asset}assets/search.js"></script></head>
<body><main id="app" data-scope="{escaped_scope}" data-site-base="{html.escape(base, quote=True)}">
<h1>{html.escape(label)}の論文解説を検索</h1>{breadcrumb}{lineage_links}
<p>収録した日本語論文解説を、タイトル・概要・本文から検索できます。</p>
<form id="search-form"><label for="query">検索語</label><input id="query" name="q" type="search" autocomplete="off" placeholder="例: KV cache &quot;メモリ帯域&quot;">
<div class="filters"><label>検索対象<select name="field" id="field"><option value="all">すべて</option><option value="title">タイトル</option><option value="summary">概要</option><option value="body">本文</option></select></label>
<label>公開年<select name="year" id="year"><option value="">すべて</option></select></label>
<label>並び順<select name="sort" id="sort"><option value="recommend">おすすめ</option><option value="citations">引用数順</option><option value="newest">新しい順</option></select></label>
<label class="check"><input type="checkbox" name="attention" id="attention">注目のみ</label><label class="check"><input type="checkbox" name="implementation" id="implementation">実装情報あり</label></div>
<button type="submit">検索</button></form><p id="status" role="status" aria-live="polite">検索データを読み込んでいます。</p><ol id="results"></ol><button id="more" type="button" hidden>さらに表示</button>
<footer><a href="{html.escape(base, quote=True)}">検索トップ</a></footer></main></body></html>'''


def _scope_items(records):
    scopes = [("", "all", "全体")]
    for family, label in FAMILIES:
        scopes.append((family, family, label))
        lineages = sorted({r["lineage"] for r in records if r["family"] == family})
        scopes.extend((f"{family}/{lineage}", f"{family}/{lineage}", f"{label} / {lineage}") for lineage in lineages)
    return scopes


def _write_scope_gzip(path: Path, scope: str, papers: list[dict]) -> int:
    """Stream one deterministic gzip JSON payload and return its plain byte size."""
    plain_bytes = 0
    with path.open("wb") as raw_file:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=raw_file, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as output:
                prefix = json.dumps({"scope": scope or "all", "body_normalization": "NFKC", "papers": []}, ensure_ascii=False, separators=(",", ":"))[:-2]
                output.write(prefix)
                plain_bytes += len(prefix.encode("utf-8"))
                for index, paper in enumerate(papers):
                    if index:
                        output.write(",")
                        plain_bytes += 1
                    encoded = json.dumps(paper, ensure_ascii=False, separators=(",", ":"))
                    output.write(encoded)
                    plain_bytes += len(encoded.encode("utf-8"))
                output.write("]}\n")
                plain_bytes += 3
    return plain_bytes


def build(repo_root: Path, out_dir: Path, site_base: str = DEFAULT_SITE, repo_url: str = DEFAULT_REPO, now=None):
    repo_root, out_dir = Path(repo_root).resolve(), Path(out_dir).resolve()
    if out_dir == repo_root or out_dir in repo_root.parents or repo_root not in out_dir.parents:
        raise ValueError("Output must be a dedicated directory inside the repository")
    old_root = survey.ROOT
    survey.ROOT = repo_root / ".survey" if (repo_root / ".survey").is_dir() else repo_root
    try:
        rows = survey.paper_views()
        citations = survey._citation_counts(rows)
        built = [_paper_record(row, citations, repo_url, now) for row in rows]
        previous = []
        manifest_path = out_dir / MANIFEST
        if out_dir.exists() and not manifest_path.exists() and any(out_dir.iterdir()):
            raise ValueError("Output directory is non-empty and has no paper-search manifest")
        if manifest_path.is_file():
            try:
                previous = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                previous = []
        if not isinstance(previous, list) or any(not isinstance(p, str) for p in previous):
            previous = []
        current = []
        raw_json_bytes = 0
        full_json_bytes = 0
        for scope, route, label in _scope_items(rows):
            page_scope = "" if route == "all" else scope
            target = out_dir if route == "all" else out_dir.joinpath(*route.split("/")) if route else out_dir
            route_parts = [] if route == "all" else route.split("/") if route else []
            scoped = [p for p in built if not route_parts or [p["family"]] + ([p["lineage"]] if len(route_parts) == 2 else []) == route_parts]
            target.mkdir(parents=True, exist_ok=True)
            data_rel = (Path(route) / "papers.json.gz").as_posix() if route and route != "all" else "papers.json.gz"
            page_rel = (Path(route) / "index.html").as_posix() if route and route != "all" else "index.html"
            data_path = out_dir / data_rel
            page_path = out_dir / page_rel
            plain_size = _write_scope_gzip(data_path, scope, scoped)
            raw_json_bytes += plain_size
            if route == "all":
                full_json_bytes = plain_size
            family_lineages = sorted({p["lineage"] for p in built if p["family"] == scope}) if len(scope.split("/")) == 1 else None
            page_path.write_text(_page_html(page_scope, label, site_base, family_lineages), encoding="utf-8")
            current.extend((data_rel, page_rel))
        asset_dir = out_dir / "assets"
        asset_dir.mkdir(parents=True, exist_ok=True)
        for name in ("search.js", "style.css"):
            source = SCRIPTS.parent.parent / "web" / "paper-search" / name
            target = asset_dir / name
            target.write_bytes(source.read_bytes())
            current.append(target.relative_to(out_dir).as_posix())
        for stale in previous:
            path = (out_dir / stale).resolve()
            if path != out_dir and out_dir in path.parents and path.is_file() and stale not in current:
                path.unlink()
                parent = path.parent
                while parent != out_dir:
                    try:
                        parent.rmdir()
                    except OSError:
                        break
                    parent = parent.parent
        manifest_path.write_text(json.dumps(sorted(current), indent=2) + "\n", encoding="utf-8")
        return {"papers": len(built), "scopes": len(_scope_items(rows)), "json_bytes": raw_json_bytes, "compressed_json_bytes": sum((out_dir / p).stat().st_size for p in current if p.endswith("papers.json.gz")), "full_scope_json_bytes": full_json_bytes, "full_scope_gzip_bytes": (out_dir / "papers.json.gz").stat().st_size, "files": len(current)}
    finally:
        survey.ROOT = old_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--site-base", default=DEFAULT_SITE)
    parser.add_argument("--repo-url", default=DEFAULT_REPO)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    out = args.out or repo / "_site"
    print(json.dumps(build(repo, out, args.site_base, args.repo_url), ensure_ascii=False))


if __name__ == "__main__":
    main()
