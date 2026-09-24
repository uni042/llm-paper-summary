#!/usr/bin/env python3
"""Backfill blocked citation audits from primary-source PDF reference sections.

This is deliberately a fallback after backfill_citations.py. It only uses PDFs
linked by the paper's own primary sources (plus the canonical arXiv PDF URL) and
matches references by explicit identifiers or repository paper titles.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import time
from datetime import date, datetime, timezone
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from pypdf import PdfReader

from backfill_citations import (
    extract_identifiers,
    fetch_bytes,
    load_state,
    normalize_title,
    replace_frontmatter,
    save_state,
)
from citation_graph import (
    alias_index,
    coverage_report,
    front,
    load_records,
    normalize_arxiv,
    normalized_identifiers,
    paper_paths,
    reference_source_fingerprint,
)


def primary_source_urls(meta: dict) -> list[str]:
    urls: list[str] = []
    for value in [meta.get("source"), *(meta.get("sources") or [])]:
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            urls.append(value)
    aid = normalize_arxiv(meta.get("arxiv_id")) or normalize_arxiv(meta.get("canonical_id"))
    if aid:
        urls.append(f"https://arxiv.org/pdf/{aid}.pdf")
    # ACL Anthology has a stable primary PDF URL derived from the landing page.
    for value in list(urls):
        parsed = urlsplit(value)
        if parsed.netloc.lower() == "aclanthology.org":
            slug = parsed.path.strip("/")
            if slug and not slug.endswith(".pdf"):
                urls.append(f"https://aclanthology.org/{slug}.pdf")
    return list(dict.fromkeys(urls))


def discover_pdf_urls(page_url: str) -> list[str]:
    try:
        raw = fetch_bytes(page_url, timeout=45)
    except Exception:
        return []
    text = raw.decode("utf-8", errors="replace")
    hrefs = re.findall(r"href\s*=\s*[\"']([^\"']+)[\"']", text, re.I)
    found: list[str] = []
    for href in hrefs:
        href = unescape(href)
        low = href.lower()
        if low.endswith(".pdf") or "/pdf/" in low or "/article/download/" in low or "download" in low and "pdf" in low:
            found.append(urljoin(page_url, href))
    return list(dict.fromkeys(found))


def candidate_pdf_urls(meta: dict) -> list[str]:
    primary = primary_source_urls(meta)
    direct = [url for url in primary if urlsplit(url).path.lower().endswith(".pdf")]
    discovered: list[str] = []
    for url in primary:
        if url in direct:
            continue
        discovered.extend(discover_pdf_urls(url))
    return list(dict.fromkeys([*direct, *discovered]))


def pdf_text(url: str) -> str:
    raw = fetch_bytes(url, timeout=75)
    if not raw.startswith(b"%PDF"):
        raise ValueError("primary PDF URL did not return a PDF")
    reader = PdfReader(io.BytesIO(raw))
    pages = [(page.extract_text() or "") for page in reader.pages]
    text = "\n".join(pages)
    if len(text.strip()) < 500:
        raise ValueError("primary PDF text extraction produced too little text")
    return text


def reference_section(text: str) -> str:
    matches = list(re.finditer(r"(?im)^\s*(?:references|bibliography)\s*$", text))
    if not matches:
        # Common numbered heading variants such as "9 References".
        matches = list(re.finditer(r"(?im)^\s*\d+(?:\.\d+)*\.?\s+(?:references|bibliography)\s*$", text))
    if not matches:
        raise ValueError("PDF text contained no recognizable References/Bibliography heading")
    section = text[matches[-1].end():]
    # Remove appendices if they clearly start after the references section.
    appendix = re.search(r"(?im)^\s*(?:appendix|appendices)(?:\s+[A-Z0-9].*)?\s*$", section)
    if appendix:
        section = section[:appendix.start()]
    if len(section.strip()) < 100:
        raise ValueError("PDF reference section was unexpectedly short")
    return section


def split_reference_entries(section: str) -> list[str]:
    patterns = [
        r"(?m)^\s*\[(\d{1,3})\]\s*",
        r"(?m)^\s*(\d{1,3})[.)]\s+",
    ]
    for pattern in patterns:
        matches = list(re.finditer(pattern, section))
        if len(matches) >= 2:
            entries: list[str] = []
            for idx, match in enumerate(matches):
                end = matches[idx + 1].start() if idx + 1 < len(matches) else len(section)
                item = section[match.end():end].strip()
                if item:
                    entries.append(item)
            if entries:
                return entries
    blocks = [re.sub(r"\s+", " ", block).strip() for block in re.split(r"\n\s*\n", section)]
    return [block for block in blocks if len(block) >= 20]


def canonical_from_ids(ref: dict[str, str], aliases: dict[str, str]) -> str | None:
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


def references_from_section(
    section: str,
    aliases: dict[str, str],
    title_targets: list[tuple[str, str]],
) -> tuple[list[dict[str, str]], int]:
    entries = split_reference_entries(section)
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        ref = extract_identifiers(entry)
        canonical = canonical_from_ids(ref, aliases) if ref else None
        normalized_entry = normalize_title(entry)
        title_matches = [canonical_id for title, canonical_id in title_targets if len(title) >= 24 and title in normalized_entry]
        title_matches = list(dict.fromkeys(title_matches))
        if len(title_matches) == 1:
            canonical = title_matches[0]
        if canonical and canonical.lower() not in seen:
            item: dict[str, str] = {"canonical_id": canonical}
            item.update(ref)
            output.append(item)
            seen.add(canonical.lower())

    # PDF text extraction can merge numbered entries. A second exact-title pass over
    # the whole reference section preserves repository-internal edges without using
    # an external citation database.
    normalized_section = normalize_title(section)
    for title, canonical in title_targets:
        if len(title) < 24 or title not in normalized_section or canonical.lower() in seen:
            continue
        output.append({"canonical_id": canonical})
        seen.add(canonical.lower())
    return output, len(entries)


def backfill(repo_root: Path, limit: int, delay: float, apply: bool, retry_blocked: bool) -> dict:
    records = load_records(repo_root)
    aliases = alias_index(records)
    title_targets = sorted(
        [(normalize_title(str(record.meta.get("title") or "")), record.canonical_id) for record in records if record.meta.get("title")],
        key=lambda pair: len(pair[0]),
        reverse=True,
    )
    state_path = repo_root / ".survey/reports/citation-backfill-state.json"
    coverage_path = repo_root / ".survey/reports/citation-coverage-latest.json"
    state = load_state(state_path)
    paper_state = state["papers"]

    attempted = completed = blocked = changed = 0
    for path in paper_paths(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        meta, _ = front(path)
        if isinstance(meta.get("references"), list) and meta.get("references_checked_at"):
            continue
        prior = paper_state.get(rel) or {}
        if prior.get("status") != "blocked" and not retry_blocked:
            continue
        if limit > 0 and attempted >= limit:
            break
        attempted += 1
        fingerprint = reference_source_fingerprint(meta)
        errors: list[str] = []
        success = False
        for url in candidate_pdf_urls(meta):
            try:
                section = reference_section(pdf_text(url))
                references, total = references_from_section(section, aliases, title_targets)
                meta["references"] = references
                meta["references_checked_at"] = date.today().isoformat()
                meta["references_source"] = "primary-pdf-reference-section"
                meta["references_total"] = total
                if apply:
                    replace_frontmatter(path, meta)
                paper_state[rel] = {
                    "status": "complete",
                    "source_fingerprint": fingerprint,
                    "references_total": total,
                    "normalized_references": len(references),
                    "source": "primary-pdf-reference-section",
                    "source_url": url,
                    "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                }
                completed += 1
                changed += 1
                success = True
                break
            except Exception as exc:
                errors.append(f"{url}: {type(exc).__name__}: {exc}")
        if not success:
            paper_state[rel] = {
                "status": "blocked",
                "source_fingerprint": fingerprint,
                "error": "PDF fallback failed: " + " | ".join(errors or ["no primary PDF URL discovered"]),
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            blocked += 1
        save_state(state_path, state)
        if delay > 0:
            time.sleep(delay)

    coverage = coverage_report(repo_root)
    coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_state(state_path, state)
    return {
        "attempted": attempted,
        "completed": completed,
        "blocked": blocked,
        "changed": changed,
        "coverage": coverage["summary"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--delay", type=float, default=0.75)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--retry-blocked", action="store_true")
    args = ap.parse_args()
    result = backfill(Path(args.root).resolve(), args.limit, args.delay, args.apply, args.retry_blocked)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
