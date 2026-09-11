#!/usr/bin/env python3
"""Backfill canonical paper frontmatter from existing body text and arXiv metadata.

Rules:
- Never overwrite a non-empty existing frontmatter value.
- Reuse already researched bibliographic/implementation details from the Markdown body.
- Use arXiv API only for stable bibliographic facts (authors, dates, categories, abs URL).
- Keep code=null when no official code URL is already evidenced in the repository content.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import time
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
URL_RE = re.compile(r"https?://[^\s）)】>]+")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2].lstrip("\n")


def write_frontmatter(path: Path, meta: dict[str, Any], body: str) -> None:
    front = yaml.safe_dump(
        meta,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    text = f"---\n{front}\n---\n\n{body.lstrip()}"
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def set_missing(meta: dict[str, Any], key: str, value: Any) -> bool:
    if key not in meta or empty(meta.get(key)):
        if value is not None and value != "" and value != []:
            meta[key] = value
            return True
    return False


def body_bibliography(body: str) -> dict[str, str]:
    values: dict[str, str] = {}
    labels = {
        "著者": "authors",
        "公開": "publication",
        "種別": "publication_type",
        "公開状態": "publication_status",
        "実装": "implementation",
        "コード": "implementation",
    }
    for line in body.splitlines():
        m = re.match(r"^-\s+\*\*([^*]+)\*\*:\s*(.+?)\s*$", line)
        if not m:
            continue
        label = m.group(1).strip()
        value = m.group(2).strip()
        if label in labels and value:
            values.setdefault(labels[label], value)
    return values


def split_authors(value: str) -> list[str]:
    parts = [x.strip() for x in re.split(r"\s*(?:,|、|；|;)\s*", value) if x.strip()]
    return parts


def official_code_from_text(text: str) -> str | None:
    lowered = text.lower()
    if not any(token in lowered for token in ("公式", "official", "公開コード", "code")):
        return None
    for url in URL_RE.findall(text):
        host = url.lower()
        if "github.com/" in host or "gitlab.com/" in host or "huggingface.co/" in host:
            return url.rstrip(".,;:")
    return None


def arxiv_ids(paths: list[Path]) -> list[str]:
    ids: list[str] = []
    for path in paths:
        meta, _ = parse_frontmatter(path)
        aid = str(meta.get("arxiv_id") or "").strip()
        if aid and aid not in ids:
            ids.append(aid)
    return ids


def fetch_arxiv(ids: list[str], batch_size: int = 25) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for offset in range(0, len(ids), batch_size):
        batch = ids[offset : offset + batch_size]
        query = urlencode({"id_list": ",".join(batch), "max_results": str(len(batch))})
        req = Request(
            "https://export.arxiv.org/api/query?" + query,
            headers={"User-Agent": "llm-paper-summary-metadata-backfill/1.0"},
        )
        with urlopen(req, timeout=60) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall(ATOM + "entry"):
            raw_id = (entry.findtext(ATOM + "id") or "").rstrip("/").split("/")[-1]
            raw_id = re.sub(r"v\d+$", "", raw_id)
            if not raw_id:
                continue
            authors = [
                (a.findtext(ATOM + "name") or "").strip()
                for a in entry.findall(ATOM + "author")
                if (a.findtext(ATOM + "name") or "").strip()
            ]
            published = (entry.findtext(ATOM + "published") or "").strip()
            primary_node = entry.find(ARXIV + "primary_category")
            primary = primary_node.attrib.get("term", "").strip() if primary_node is not None else ""
            categories = [
                node.attrib.get("term", "").strip()
                for node in entry.findall(ATOM + "category")
                if node.attrib.get("term", "").strip()
            ]
            cross = [cat for cat in categories if cat != primary]
            result[raw_id] = {
                "authors": authors,
                "published": published[:10] if published else "",
                "arxiv_categories": {"primary": primary, "cross_list": cross} if primary else None,
                "abs_url": f"https://arxiv.org/abs/{raw_id}",
                "pdf_url": f"https://arxiv.org/pdf/{raw_id}",
            }
        if offset + batch_size < len(ids):
            time.sleep(3.1)
    return result


def paper_paths(root: Path) -> list[Path]:
    out: list[Path] = []
    for family in ("inference", "training", "survey"):
        for path in sorted((root / "papers" / family).rglob("*.md")):
            if path.name in {"README.md", "comparison.md"}:
                continue
            meta, body = parse_frontmatter(path)
            if body.lstrip().startswith("# Moved"):
                continue
            out.append(path)
    return out


def backfill(path: Path, arxiv: dict[str, dict[str, Any]], checked: str) -> tuple[bool, list[str]]:
    meta, body = parse_frontmatter(path)
    before = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    bib = body_bibliography(body)
    added: list[str] = []

    if "authors" in bib and set_missing(meta, "authors", split_authors(bib["authors"])):
        added.append("authors(body)")
    for key in ("publication", "publication_type", "publication_status", "implementation"):
        if key in bib and set_missing(meta, key, bib[key]):
            added.append(f"{key}(body)")

    if "implementation" in bib and ("code" not in meta or empty(meta.get("code"))):
        code = official_code_from_text(bib["implementation"])
        if code:
            meta["code"] = code
            added.append("code(body)")

    aid = str(meta.get("arxiv_id") or "").strip()
    info = arxiv.get(aid) if aid else None
    if info:
        if set_missing(meta, "authors", info.get("authors")):
            added.append("authors(arxiv)")
        if set_missing(meta, "published", info.get("published")):
            added.append("published(arxiv)")
        if set_missing(meta, "arxiv_categories", info.get("arxiv_categories")):
            added.append("arxiv_categories")
        if set_missing(meta, "source", info.get("abs_url")):
            added.append("source(arxiv)")
        if set_missing(meta, "publication", "arXiv"):
            added.append("publication(arxiv)")
        if set_missing(meta, "publication_type", "プレプリント"):
            added.append("publication_type(arxiv)")
        if set_missing(meta, "publication_status", "arXiv preprint"):
            added.append("publication_status(arxiv)")

        sources = meta.get("sources")
        if not isinstance(sources, list) or not sources:
            sources = []
            for candidate in (meta.get("source"), info.get("abs_url"), info.get("pdf_url"), meta.get("code")):
                if isinstance(candidate, str) and candidate and candidate not in sources:
                    sources.append(candidate)
            if sources:
                meta["sources"] = sources
                added.append("sources")

    # A missing code key means "unknown field"; explicit null means checked/no URL recorded.
    if "code" not in meta:
        meta["code"] = None
        added.append("code=null")

    # Reuse a body implementation description when possible. Otherwise keep it incomplete;
    # this prevents the audit from falsely declaring implementation evidence complete.
    if "last_checked" not in meta or empty(meta.get("last_checked")):
        meta["last_checked"] = checked
        added.append("last_checked")

    after = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    changed = before != after
    if changed:
        write_frontmatter(path, meta, body)
    return changed, added


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--no-network", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    paths = paper_paths(root)
    ids = arxiv_ids(paths)
    arxiv = {} if args.no_network else fetch_arxiv(ids)
    checked = datetime.now(timezone.utc).date().isoformat()

    changed_count = 0
    for path in paths:
        changed, added = backfill(path, arxiv, checked)
        if changed:
            changed_count += 1
            print(f"UPDATED {path.relative_to(root).as_posix()}: {', '.join(added)}")
    print(f"metadata_backfill_changed={changed_count} papers={len(paths)} arxiv_entries={len(arxiv)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
