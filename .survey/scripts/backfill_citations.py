#!/usr/bin/env python3
"""Backfill structured references from primary paper reference sections.

The durable state file records a stable source fingerprint, so completed papers are not
re-read on later runs. arXiv HTML is preferred; the official arXiv source archive is the
fallback. Unsupported primary-source formats are recorded as blocked instead of guessed
from external citation databases.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import tarfile
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml

from citation_graph import (
    alias_index,
    coverage_report,
    front,
    load_records,
    normalize_arxiv,
    normalize_doi,
    normalize_openreview,
    normalized_identifiers,
    paper_paths,
    reference_source_fingerprint,
)

STATE_SCHEMA_VERSION = 1
USER_AGENT = "llm-paper-summary-citation-backfill/1.0 (+https://github.com/uni042/llm-paper-summary)"


class ArxivReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {k: v or "" for k, v in attrs}
        classes = set(amap.get("class", "").split())
        if tag == "li" and "ltx_bibitem" in classes and self.current is None:
            self.current = {"text": [], "hrefs": []}
            self.depth = 1
            return
        if self.current is not None:
            self.depth += 1
            if tag == "a" and amap.get("href"):
                self.current["hrefs"].append(amap["href"])

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        self.depth -= 1
        if tag == "li" and self.depth <= 0:
            self.current["text"] = " ".join(self.current["text"]).strip()
            self.items.append(self.current)
            self.current = None
            self.depth = 0

    def handle_data(self, data: str) -> None:
        if self.current is not None and data.strip():
            self.current["text"].append(data.strip())


def fetch_bytes(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def extract_identifiers(text: str, hrefs: list[str] | None = None) -> dict[str, str]:
    hrefs = hrefs or []
    candidates = "\n".join([text, *hrefs])
    result: dict[str, str] = {}

    arxiv_matches = re.findall(
        r"(?:arxiv(?:\.org/(?:abs|pdf|html)/|\s*:\s*)?)(\d{4}\.\d{4,5}(?:v\d+)?|[a-z.-]+/\d{7}(?:v\d+)?)",
        candidates,
        re.I,
    )
    for match in arxiv_matches:
        aid = normalize_arxiv(match)
        if aid:
            result["arxiv_id"] = aid
            break

    doi_urls = re.findall(r"https?://(?:dx\.)?doi\.org/([^\s<>\"'}]+)", candidates, re.I)
    doi_text = re.findall(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", candidates, re.I)
    for match in [*doi_urls, *doi_text]:
        doi = normalize_doi(match)
        if doi:
            result["doi"] = doi
            break

    openreview_urls = re.findall(r"https?://openreview\.net/(?:forum|pdf)\?id=([^&#\s<>\"'}]+)", candidates, re.I)
    if openreview_urls:
        oid = normalize_openreview(openreview_urls[0])
        if oid:
            result["openreview_id"] = oid
    return result


def canonical_for_reference(ref: dict[str, str], aliases: dict[str, str]) -> str | None:
    probe = dict(ref)
    if probe.get("arxiv_id"):
        probe["canonical_id"] = "arXiv:" + probe["arxiv_id"]
    elif probe.get("doi"):
        probe["canonical_id"] = "DOI:" + probe["doi"]
    elif probe.get("openreview_id"):
        probe["canonical_id"] = "OpenReview:" + probe["openreview_id"]
    for identifier in normalized_identifiers(probe):
        if identifier in aliases:
            return aliases[identifier]
    return probe.get("canonical_id")


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def title_match(text: str, title_targets: list[tuple[str, str]]) -> str | None:
    normalized_text = normalize_title(text)
    if not normalized_text:
        return None
    matches = [canonical for title, canonical in title_targets if len(title) >= 24 and title in normalized_text]
    unique = list(dict.fromkeys(matches))
    return unique[0] if len(unique) == 1 else None


def entries_to_references(
    entries: list[dict[str, Any]],
    aliases: dict[str, str],
    title_targets: list[tuple[str, str]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        text = str(entry.get("text") or "")
        hrefs = [str(x) for x in entry.get("hrefs") or []]
        ref = extract_identifiers(text, hrefs)
        canonical = canonical_for_reference(ref, aliases) if ref else None
        matched = title_match(text, title_targets)
        if matched:
            canonical = matched
        if not canonical:
            continue
        item: dict[str, str] = {"canonical_id": canonical}
        item.update(ref)
        key = canonical.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def arxiv_html_references(arxiv_id: str) -> tuple[list[dict[str, Any]], str]:
    raw = fetch_bytes(f"https://arxiv.org/html/{arxiv_id}")
    parser = ArxivReferenceParser()
    parser.feed(raw.decode("utf-8", errors="replace"))
    if not parser.items:
        raise ValueError("arXiv HTML contained no ltx_bibitem reference entries")
    return parser.items, "arxiv-html-reference-section"


def bibliography_blocks(text: str) -> list[str]:
    blocks = re.split(r"\\bibitem(?:\[[^\]]*\])?\{[^}]+\}", text)
    return [block.strip() for block in blocks[1:] if block.strip()]


def source_archive_references(arxiv_id: str) -> tuple[list[dict[str, Any]], str]:
    errors: list[str] = []
    raw = b""
    for url in (f"https://export.arxiv.org/e-print/{arxiv_id}", f"https://arxiv.org/e-print/{arxiv_id}"):
        try:
            raw = fetch_bytes(url, timeout=60)
            if raw:
                break
        except Exception as exc:  # network/provider error is reported as blocked state
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    if not raw:
        raise ValueError("unable to download arXiv source archive: " + " | ".join(errors))

    texts: list[str] = []
    try:
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            bbl = [m for m in members if m.name.lower().endswith(".bbl")]
            selected = bbl
            if not selected:
                selected = [m for m in members if m.name.lower().endswith((".tex", ".ltx"))]
            for member in selected:
                handle = archive.extractfile(member)
                if handle:
                    texts.append(handle.read().decode("utf-8", errors="replace"))
    except tarfile.ReadError:
        try:
            texts = [gzip.decompress(raw).decode("utf-8", errors="replace")]
        except Exception:
            texts = [raw.decode("utf-8", errors="replace")]

    blocks: list[str] = []
    for text in texts:
        if "\\bibitem" in text:
            blocks.extend(bibliography_blocks(text))
        elif "\\begin{thebibliography}" in text:
            for section in re.findall(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", text, re.S):
                blocks.extend(bibliography_blocks(section))
    if not blocks:
        raise ValueError("arXiv source archive contained no compiled/reference-section bibitems")
    return [{"text": block, "hrefs": []} for block in blocks], "arxiv-source-reference-section"


def extract_primary_references(meta: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    aid = normalize_arxiv(meta.get("arxiv_id")) or normalize_arxiv(meta.get("canonical_id"))
    if not aid:
        for value in [meta.get("source"), *(meta.get("sources") or [])]:
            aid = normalize_arxiv(value)
            if aid:
                break
    if not aid:
        raise ValueError("no supported primary reference extractor for non-arXiv paper")
    html_error = None
    try:
        return arxiv_html_references(aid)
    except Exception as exc:
        html_error = f"{type(exc).__name__}: {exc}"
    try:
        return source_archive_references(aid)
    except Exception as exc:
        raise ValueError(f"arXiv HTML failed ({html_error}); source fallback failed ({type(exc).__name__}: {exc})") from exc


def replace_frontmatter(path: Path, meta: dict[str, Any]) -> None:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError("paper lacks YAML frontmatter")
    parts = raw.split("---", 2)
    yaml_text = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000).rstrip()
    path.write_text(f"---\n{yaml_text}\n---{parts[2]}", encoding="utf-8")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": STATE_SCHEMA_VERSION, "papers": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("papers"), dict):
        return {"schema_version": STATE_SCHEMA_VERSION, "papers": {}}
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["schema_version"] = STATE_SCHEMA_VERSION
    state["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backfill(repo_root: Path, limit: int, delay: float, apply: bool, retry_blocked: bool) -> dict[str, Any]:
    records = load_records(repo_root)
    aliases = alias_index(records)
    title_targets = sorted(
        [(normalize_title(str(r.meta.get("title") or "")), r.canonical_id) for r in records if r.meta.get("title")],
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    state_path = repo_root / ".survey/reports/citation-backfill-state.json"
    coverage_path = repo_root / ".survey/reports/citation-coverage-latest.json"
    state = load_state(state_path)
    paper_state: dict[str, Any] = state["papers"]

    attempted = completed = blocked = changed = 0
    for path in paper_paths(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        meta, _ = front(path)
        fingerprint = reference_source_fingerprint(meta)
        prior = paper_state.get(rel) or {}
        already_complete = (
            prior.get("status") == "complete"
            and prior.get("source_fingerprint") == fingerprint
            and isinstance(meta.get("references"), list)
            and meta.get("references_checked_at")
        )
        already_blocked = prior.get("status") == "blocked" and prior.get("source_fingerprint") == fingerprint
        if already_complete or (already_blocked and not retry_blocked):
            continue
        if limit > 0 and attempted >= limit:
            break
        attempted += 1
        try:
            entries, source_label = extract_primary_references(meta)
            references = entries_to_references(entries, aliases, title_targets)
            meta["references"] = references
            meta["references_checked_at"] = date.today().isoformat()
            meta["references_source"] = source_label
            meta["references_total"] = len(entries)
            if apply:
                replace_frontmatter(path, meta)
            paper_state[rel] = {
                "status": "complete",
                "source_fingerprint": fingerprint,
                "references_total": len(entries),
                "normalized_references": len(references),
                "source": source_label,
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            completed += 1
            changed += 1
        except Exception as exc:
            paper_state[rel] = {
                "status": "blocked",
                "source_fingerprint": fingerprint,
                "error": f"{type(exc).__name__}: {exc}",
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            blocked += 1
        save_state(state_path, state)
        if delay > 0:
            time.sleep(delay)

    coverage = coverage_report(repo_root)
    coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_state(state_path, state)
    result = {
        "attempted": attempted,
        "completed": completed,
        "blocked": blocked,
        "changed": changed,
        "coverage": coverage["summary"],
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--delay", type=float, default=0.75)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--retry-blocked", action="store_true")
    args = ap.parse_args()
    result = backfill(Path(args.root).resolve(), args.limit, args.delay, args.apply, args.retry_blocked)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
