#!/usr/bin/env python3
"""Recover citation audits that normal primary-source extraction cannot reach.

The normal backfill prefers arXiv HTML/source and then publisher-linked PDFs. This
module handles two remaining primary-source edge cases without guessing from
citation databases:

* publisher pages whose official PDF URL is not discoverable reliably from CI;
* withdrawn arXiv papers whose PDF/HTML is unavailable but whose source archive
  still contains a BibTeX bibliography.

Only verified primary-source URLs are hard-coded. The resulting references are
normalized against the repository identity index in the same way as the regular
backfill.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import tarfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from backfill_citations import (
    entries_to_references,
    fetch_bytes,
    load_state,
    normalize_title,
    replace_frontmatter,
    save_state,
)
from backfill_citation_pdfs import pdf_text, reference_section, references_from_section
from citation_graph import (
    alias_index,
    coverage_report,
    front,
    load_records,
    normalize_arxiv,
    paper_paths,
    reference_source_fingerprint,
)

# Official publisher PDFs verified from the primary publication pages. OJS and
# ACM do not consistently expose these links to GitHub Actions through the
# landing-page HTML, so keep the small exception table explicit and auditable.
PRIMARY_PDF_OVERRIDES = {
    "DOI:10.1145/3688351.3689164": "https://dl.acm.org/doi/pdf/10.1145/3688351.3689164",
    "AAAI:39816": "https://ojs.aaai.org/index.php/AAAI/article/download/39816/43777",
    "AAAI:39454": "https://ojs.aaai.org/index.php/AAAI/article/download/39454/43415",
    "AAAI:39106": "https://ojs.aaai.org/index.php/AAAI/article/download/39106/43068",
}

# Author-hosted copies are used only after the official publisher PDF fails.
# The TwinPilots copy is hosted on co-author Song Jiang's university site and
# carries the same title, authors and DOI as the ACM version.
PRIMARY_PDF_FALLBACKS = {
    "DOI:10.1145/3688351.3689164": [
        "https://jiangs.utasites.cloud/pubs/papers/Yu24-TwinPilots.pdf",
    ],
}


def primary_pdf_urls(canonical_id: str) -> list[str]:
    urls: list[str] = []
    official = PRIMARY_PDF_OVERRIDES.get(canonical_id)
    if official:
        urls.append(official)
    urls.extend(PRIMARY_PDF_FALLBACKS.get(canonical_id, []))
    return list(dict.fromkeys(urls))


def bibtex_blocks(text: str) -> list[str]:
    """Split a BibTeX database into complete entry-sized text blocks."""
    starts = list(re.finditer(r"(?im)^\s*@[A-Za-z]+\s*\{", text))
    blocks: list[str] = []
    for idx, match in enumerate(starts):
        end = starts[idx + 1].start() if idx + 1 < len(starts) else len(text)
        block = text[match.start():end].strip()
        if len(block) >= 20:
            blocks.append(block)
    return blocks


def arxiv_source_urls(arxiv_id: str) -> list[str]:
    """Return official source endpoints, including version fallbacks for withdrawals."""
    variants = [arxiv_id, f"{arxiv_id}v3", f"{arxiv_id}v2", f"{arxiv_id}v1"]
    urls: list[str] = []
    for variant in variants:
        urls.extend([
            f"https://export.arxiv.org/e-print/{variant}",
            f"https://arxiv.org/e-print/{variant}",
        ])
    return list(dict.fromkeys(urls))


def arxiv_bibtex_entries(arxiv_id: str) -> tuple[list[dict[str, Any]], str]:
    """Read .bib entries from the official arXiv source archive."""
    errors: list[str] = []
    for url in arxiv_source_urls(arxiv_id):
        try:
            raw = fetch_bytes(url, timeout=60)
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
            continue
        if not raw:
            errors.append(f"{url}: empty response")
            continue

        texts: list[str] = []
        try:
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as archive:
                members = [m for m in archive.getmembers() if m.isfile() and m.name.lower().endswith(".bib")]
                for member in members:
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
            blocks.extend(bibtex_blocks(text))
        if blocks:
            return [{"text": block, "hrefs": []} for block in blocks], url
        errors.append(f"{url}: source archive contained no parseable .bib entries")

    raise ValueError("unable to recover arXiv source bibliography: " + " | ".join(errors))


def backfill(repo_root: Path, limit: int, apply: bool) -> dict[str, Any]:
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

        canonical = str(meta.get("canonical_id") or "").strip()
        aid = normalize_arxiv(meta.get("arxiv_id")) or normalize_arxiv(canonical)
        pdf_urls = primary_pdf_urls(canonical)
        if not pdf_urls and not aid:
            continue
        if limit > 0 and attempted >= limit:
            break

        attempted += 1
        fingerprint = reference_source_fingerprint(meta)
        errors: list[str] = []
        success = False
        references: list[dict[str, str]] = []
        total = 0
        source_label = ""
        source_url = ""

        for candidate in pdf_urls:
            source_url = candidate
            try:
                section = reference_section(pdf_text(source_url))
                references, total = references_from_section(section, aliases, title_targets)
                source_label = "primary-pdf-reference-section"
                success = True
                break
            except Exception as exc:
                errors.append(f"{source_url}: {type(exc).__name__}: {exc}")

        # A withdrawn arXiv record may return 404 for HTML/PDF while retaining an
        # official source archive for an explicit version. BibTeX remains the
        # paper's own bibliography and is acceptable as the primary source.
        if not success and aid:
            try:
                entries, source_url = arxiv_bibtex_entries(aid)
                references = entries_to_references(entries, aliases, title_targets)
                total = len(entries)
                source_label = "arxiv-source-bibtex"
                success = True
            except Exception as exc:
                errors.append(f"arXiv source BibTeX: {type(exc).__name__}: {exc}")

        if success:
            meta["references"] = references
            meta["references_checked_at"] = date.today().isoformat()
            meta["references_source"] = source_label
            meta["references_total"] = total
            if apply:
                replace_frontmatter(path, meta)
            paper_state[rel] = {
                "status": "complete",
                "source_fingerprint": fingerprint,
                "references_total": total,
                "normalized_references": len(references),
                "source": source_label,
                "source_url": source_url,
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            completed += 1
            changed += 1
        else:
            paper_state[rel] = {
                "status": "blocked",
                "source_fingerprint": fingerprint,
                "error": "primary-source recovery failed: " + " | ".join(errors),
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            blocked += 1
        save_state(state_path, state)

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
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    result = backfill(Path(args.root).resolve(), args.limit, args.apply)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
