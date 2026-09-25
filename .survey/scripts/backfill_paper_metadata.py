#!/usr/bin/env python3
"""Backfill canonical paper frontmatter from existing body text and arXiv metadata.

Rules:
- Never overwrite a non-empty existing frontmatter value.
- Reuse already researched bibliographic/implementation details from the Markdown body.
- Use arXiv API only for stable bibliographic facts (authors, dates, categories, abs URL).
- Keep code=null when no official code URL is evidenced in the repository content.
- Derive implementation status only from existing code/evaluation metadata; do not invent a code URL.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
URL_RE = re.compile(r"https?://[^\s）)】>]+")
REQUIRED_METADATA = (
    "canonical_id", "title", "summary", "authors", "published", "publication",
    "publication_type", "publication_status", "source", "sources", "implementation",
    "code", "last_checked",
)



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


def body_one_line_summary(body: str) -> str | None:
    """Reuse an already-authored one-line explanation; never invent prose."""
    patterns = (
        r"##\s+一文解説\s*\n+\s*([^\n]+)",
        r"^>\s*([^\n]+)$",
    )
    for pattern in patterns:
        match = re.search(pattern, body, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if value:
                return value
    return None


def metadata_needs_backfill(meta: dict[str, Any], body: str) -> bool:
    for key in REQUIRED_METADATA:
        if key == "code":
            if key not in meta:
                return True
            continue
        if key not in meta or empty(meta.get(key)):
            return True
    if meta.get("arxiv_id"):
        categories = meta.get("arxiv_categories")
        if not isinstance(categories, dict) or not categories.get("primary"):
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
    return [x.strip() for x in re.split(r"\s*(?:,|、|；|;)\s*", value) if x.strip()]


def authors_from_affiliations(value: Any) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    # Existing legacy field usually has "A, B（University）". Only consume the
    # author segment before the first affiliation parenthesis.
    head = re.split(r"[（(]", value, maxsplit=1)[0].strip()
    return split_authors(head)


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


class _ArxivMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: dict[str, list[str]] = {}
        self._primary_subject_depth = 0
        self.primary_subject_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {str(k).lower(): (v or "") for k, v in attrs}
        classes = set(amap.get("class", "").split())
        if self._primary_subject_depth:
            self._primary_subject_depth += 1
        elif "primary-subject" in classes:
            self._primary_subject_depth = 1

        if tag.lower() != "meta":
            return
        name = amap.get("name", "").lower()
        content = amap.get("content", "").strip()
        if name and content:
            self.values.setdefault(name, []).append(content)

    def handle_endtag(self, tag: str) -> None:
        if self._primary_subject_depth:
            self._primary_subject_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._primary_subject_depth and data.strip():
            self.primary_subject_text.append(data.strip())


def _parse_arxiv_html_metadata(arxiv_id: str, raw: bytes) -> dict[str, Any] | None:
    parser = _ArxivMetaParser()
    parser.feed(raw.decode("utf-8", errors="replace"))
    meta = parser.values
    authors = [x.strip() for x in meta.get("citation_author", []) if x.strip()]
    dates = meta.get("citation_date", []) or meta.get("citation_publication_date", [])
    published = ""
    if dates:
        date_match = re.search(r"(\d{4})[-/](\d{2})(?:[-/](\d{2}))?", dates[0])
        if date_match:
            published = "-".join(part for part in date_match.groups() if part)
    keyword_values = meta.get("citation_keywords", [])
    category_codes: list[str] = []
    category_sources = [*keyword_values, *parser.primary_subject_text]
    for value in category_sources:
        for code in re.findall(r"\(([A-Za-z][A-Za-z0-9.-]*[.-][A-Za-z0-9-]+)\)", value):
            if code not in category_codes:
                category_codes.append(code)
        for code in re.findall(r"\b([A-Za-z][A-Za-z0-9-]*\.[A-Za-z0-9.-]+)\b", value):
            if code not in category_codes:
                category_codes.append(code)
    if not authors and not published and not category_codes:
        return None
    primary = category_codes[0] if category_codes else ""
    return {
        "authors": authors,
        "published": published,
        "arxiv_categories": (
            {"primary": primary, "cross_list": category_codes[1:]}
            if primary
            else None
        ),
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
    }


def _fetch_arxiv_html(arxiv_id: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": "llm-paper-summary-metadata-backfill/1.1 (https://github.com/uni042/llm-paper-summary)",
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
    }
    errors: list[str] = []
    best: dict[str, Any] | None = None
    for url in (
        f"https://arxiv.org/html/{arxiv_id}",
        f"https://arxiv.org/abs/{arxiv_id}",
    ):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=60) as response:
                raw = response.read()
            parsed = _parse_arxiv_html_metadata(arxiv_id, raw)
            if parsed:
                if best is None:
                    best = parsed
                else:
                    for key, value in parsed.items():
                        if value and not best.get(key):
                            best[key] = value
                categories = best.get("arxiv_categories")
                if isinstance(categories, dict) and categories.get("primary"):
                    return best
            else:
                errors.append(f"{url}: no citation metadata")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    if best is not None:
        return best
    print(
        f"WARNING arXiv HTML metadata unavailable for {arxiv_id}: "
        + " | ".join(errors),
        file=sys.stderr,
    )
    return None


def _fetch_arxiv_batch(batch: list[str]) -> ET.Element:
    query = urlencode({"id_list": ",".join(batch), "max_results": str(len(batch))})
    headers = {
        "User-Agent": "llm-paper-summary-metadata-backfill/1.1 (citation metadata maintenance)",
        "Accept": "application/atom+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.1",
    }
    endpoints = (
        "https://export.arxiv.org/api/query?",
        "https://arxiv.org/api/query?",
    )
    errors: list[str] = []
    for endpoint in endpoints:
        for attempt in range(3):
            req = Request(endpoint + query, headers=headers)
            try:
                with urlopen(req, timeout=60) as response:
                    payload = response.read()
                return ET.fromstring(payload)
            except Exception as exc:
                errors.append(f"{endpoint} attempt={attempt + 1}: {type(exc).__name__}: {exc}")
                if attempt < 2:
                    time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(
        "arXiv metadata fetch failed after endpoint fallbacks: " + " | ".join(errors)
    )


def fetch_arxiv(ids: list[str], batch_size: int = 25) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for offset in range(0, len(ids), batch_size):
        batch = ids[offset : offset + batch_size]
        try:
            root = _fetch_arxiv_batch(batch)
        except Exception as exc:
            print(
                f"WARNING arXiv Atom API unavailable for batch {batch}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            root = None
        if root is not None:
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
        for arxiv_id in batch:
            if arxiv_id not in result:
                parsed = _fetch_arxiv_html(arxiv_id)
                if parsed:
                    result[arxiv_id] = parsed
        if offset + batch_size < len(ids):
            time.sleep(3.1)
    return result


def paper_paths(root: Path) -> list[Path]:
    out: list[Path] = []
    for family in ("inference", "training", "survey"):
        for path in sorted((root / "papers" / family).rglob("*.md")):
            if path.name in {"README.md", "comparison.md"}:
                continue
            _, body = parse_frontmatter(path)
            if body.lstrip().startswith("# Moved"):
                continue
            out.append(path)
    return out


def ensure_sources(meta: dict[str, Any], *extra: Any) -> bool:
    current = meta.get("sources")
    if isinstance(current, list) and current:
        return False
    sources: list[str] = []
    for candidate in (meta.get("source"), *extra, meta.get("code")):
        if isinstance(candidate, str) and candidate and candidate not in sources:
            sources.append(candidate)
    if sources:
        meta["sources"] = sources
        return True
    return False


def synthesize_implementation(meta: dict[str, Any]) -> tuple[str, str]:
    code = meta.get("code")
    evaluation = meta.get("hardware_evaluation") or meta.get("evaluation_type")
    if isinstance(code, str) and code.strip():
        prefix = f"公式コード公開あり（{code.strip()}）。"
        status = "official-code-available"
    else:
        prefix = "公式コードURLはメタデータ確認時点で確認できず。"
        status = "official-code-not-confirmed"
    if isinstance(evaluation, str) and evaluation.strip():
        detail = f"論文では{evaluation.strip()}による提案手法の実装・評価を報告。"
    else:
        detail = "実装形態の詳細は既存本文の手法・評価記述を参照。"
    return detail + prefix, status


def backfill(path: Path, arxiv: dict[str, dict[str, Any]], checked: str) -> tuple[bool, list[str]]:
    meta, body = parse_frontmatter(path)
    before = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    bib = body_bibliography(body)
    added: list[str] = []

    authored_one_line = body_one_line_summary(body)
    if set_missing(meta, "list_summary", authored_one_line):
        added.append("list_summary(body)")
    if set_missing(meta, "summary", meta.get("list_summary") or authored_one_line):
        added.append("summary(existing-one-line)")

    if "authors" in bib and set_missing(meta, "authors", split_authors(bib["authors"])):
        added.append("authors(body)")
    if ("authors" not in meta or empty(meta.get("authors"))) and meta.get("authors_affiliations"):
        authors = authors_from_affiliations(meta.get("authors_affiliations"))
        if authors:
            meta["authors"] = authors
            added.append("authors(authors_affiliations)")

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
        incoming_categories = info.get("arxiv_categories")
        categories = meta.get("arxiv_categories")
        if incoming_categories and (not isinstance(categories, dict) or empty(categories.get("primary"))):
            meta["arxiv_categories"] = incoming_categories
            added.append("arxiv_categories")
        if set_missing(meta, "source", info.get("abs_url")):
            added.append("source(arxiv)")
        if set_missing(meta, "publication", "arXiv"):
            added.append("publication(arxiv)")
        if set_missing(meta, "publication_type", "プレプリント"):
            added.append("publication_type(arxiv)")
        if set_missing(meta, "publication_status", "arXiv preprint"):
            added.append("publication_status(arxiv)")
        if ensure_sources(meta, info.get("abs_url"), info.get("pdf_url")):
            added.append("sources")

    # Non-arXiv legacy conference pages can usually be reconstructed from existing fields.
    source = str(meta.get("source") or "")
    if set_missing(meta, "publication", meta.get("publication_status")):
        added.append("publication(publication_status)")
    if ("publication_type" not in meta or empty(meta.get("publication_type"))) and "usenix.org/" in source:
        meta["publication_type"] = "査読付き国際会議論文"
        added.append("publication_type(usenix)")
    if ensure_sources(meta):
        added.append("sources")

    # Empty legacy code strings are normalized to explicit null: do not infer a URL.
    if "code" not in meta or meta.get("code") == "":
        meta["code"] = None
        added.append("code=null")

    if "implementation" not in meta or empty(meta.get("implementation")):
        implementation, status = synthesize_implementation(meta)
        meta["implementation"] = implementation
        added.append("implementation(evidence)")
        if "implementation_status" not in meta or empty(meta.get("implementation_status")):
            meta["implementation_status"] = status
            added.append("implementation_status")
    elif "implementation_status" not in meta or empty(meta.get("implementation_status")):
        code = meta.get("code")
        meta["implementation_status"] = (
            "official-code-available"
            if isinstance(code, str) and code.strip()
            else "official-code-not-confirmed"
        )
        added.append("implementation_status")

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
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Process only papers with incomplete canonical metadata.",
    )
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    paths = paper_paths(root)
    if args.missing_only:
        paths = [
            path
            for path in paths
            if metadata_needs_backfill(*parse_frontmatter(path))
        ]
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
