#!/usr/bin/env python3
"""Build repository-internal citation counts from structured frontmatter references."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

PAPER_FAMILIES = ("inference", "training", "survey")
REFERENCE_AUDIT_VERSION = 1


def front(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        return {}, raw
    parts = raw.split("---", 2)
    return yaml.safe_load(parts[1]) or {}, parts[2]


def normalize_arxiv(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    text = re.sub(r"^(?:arxiv:|https?://arxiv\.org/(?:abs|pdf|html)/)", "", text, flags=re.I)
    text = re.sub(r"\.pdf$", "", text, flags=re.I)
    text = re.sub(r"v\d+$", "", text, flags=re.I)
    if re.fullmatch(r"\d{4}\.\d{4,5}|[a-z.-]+/\d{7}", text, re.I):
        return text
    return None


def normalize_doi(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    text = re.sub(r"^(?:doi:|https?://(?:dx\.)?doi\.org/)", "", text, flags=re.I)
    text = text.rstrip(".,;)]}")
    if re.match(r"^10\.\d{4,9}/\S+$", text, re.I):
        return text.lower()
    return None


def normalize_openreview(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    m = re.search(r"openreview\.net/(?:forum|pdf)\?id=([^&#\s]+)", text, re.I)
    if m:
        return m.group(1)
    text = re.sub(r"^OpenReview:", "", text, flags=re.I)
    return text if re.fullmatch(r"[A-Za-z0-9_.-]+", text) else None


def normalized_identifiers(meta: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    cid = meta.get("canonical_id")
    if cid:
        cid_text = str(cid).strip()
        aid = normalize_arxiv(cid_text)
        doi = normalize_doi(cid_text)
        oid = normalize_openreview(cid_text)
        if aid:
            ids.append("arXiv:" + aid)
        elif doi:
            ids.append("DOI:" + doi)
        elif oid and cid_text.lower().startswith("openreview:"):
            ids.append("OpenReview:" + oid)
        else:
            ids.append(cid_text)
    aid = normalize_arxiv(meta.get("arxiv_id"))
    doi = normalize_doi(meta.get("doi"))
    oid = normalize_openreview(meta.get("openreview_id"))
    if aid:
        ids.append("arXiv:" + aid)
    if doi:
        ids.append("DOI:" + doi)
    if oid:
        ids.append("OpenReview:" + oid)
    return list(dict.fromkeys(ids))


def reference_identifiers(ref: Any) -> list[str]:
    if isinstance(ref, str):
        ref = {"canonical_id": ref}
    if not isinstance(ref, dict):
        return []
    return normalized_identifiers(ref)


def paper_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for family in PAPER_FAMILIES:
        root = repo_root / "papers" / family
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if path.name in {"README.md", "comparison.md"}:
                continue
            paths.append(path)
    return sorted(paths)


@dataclass(frozen=True)
class PaperRecord:
    path: str
    canonical_id: str
    identifiers: tuple[str, ...]
    meta: dict[str, Any]


def load_records(repo_root: Path) -> list[PaperRecord]:
    records: list[PaperRecord] = []
    for path in paper_paths(repo_root):
        meta, _ = front(path)
        ids = normalized_identifiers(meta)
        canonical = str(meta.get("canonical_id") or "").strip()
        if not canonical:
            continue
        if ids:
            canonical = ids[0] if canonical not in ids else canonical
        records.append(PaperRecord(
            path=path.relative_to(repo_root).as_posix(),
            canonical_id=canonical,
            identifiers=tuple(ids),
            meta=meta,
        ))
    return records


def alias_index(records: Iterable[PaperRecord]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for record in records:
        for identifier in record.identifiers:
            previous = aliases.get(identifier)
            if previous and previous != record.canonical_id:
                raise ValueError(f"duplicate identifier {identifier}: {previous} vs {record.canonical_id}")
            aliases[identifier] = record.canonical_id
    return aliases


def build_graph(records: list[PaperRecord]) -> tuple[dict[str, set[str]], dict[str, int]]:
    aliases = alias_index(records)
    path_by_canonical = {record.canonical_id: record.path for record in records}
    outgoing: dict[str, set[str]] = {record.path: set() for record in records}
    counts: dict[str, int] = {record.path: 0 for record in records}

    for source in records:
        targets: set[str] = set()
        references = source.meta.get("references")
        if not isinstance(references, list):
            references = []
        for ref in references:
            target_canonical = None
            for identifier in reference_identifiers(ref):
                if identifier in aliases:
                    target_canonical = aliases[identifier]
                    break
            if target_canonical is None or target_canonical == source.canonical_id:
                continue
            target_path = path_by_canonical.get(target_canonical)
            if target_path:
                targets.add(target_path)
        outgoing[source.path] = targets
        for target_path in targets:
            counts[target_path] += 1
    return outgoing, counts


def citation_counts_from_view_records(view_records: list[dict[str, Any]]) -> dict[str, int]:
    records: list[PaperRecord] = []
    for row in view_records:
        meta = row.get("meta") or {}
        canonical = str(meta.get("canonical_id") or "").strip()
        ids = normalized_identifiers(meta)
        if not canonical or not ids:
            continue
        canonical = canonical if canonical in ids else ids[0]
        records.append(PaperRecord(
            path=str(row["path"]),
            canonical_id=canonical,
            identifiers=tuple(ids),
            meta=meta,
        ))
    _, counts = build_graph(records)
    result = {str(row["path"]): 0 for row in view_records}
    result.update(counts)
    return result


def reference_source_fingerprint(meta: dict[str, Any]) -> str:
    stable = {
        key: meta.get(key)
        for key in (
            "canonical_id", "arxiv_id", "doi", "openreview_id", "title", "source", "sources",
            "published", "publication", "publication_version",
        )
    }
    encoded = json.dumps(stable, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def coverage_report(repo_root: Path, records: list[PaperRecord] | None = None) -> dict[str, Any]:
    records = records or load_records(repo_root)
    complete: list[str] = []
    missing: list[dict[str, str]] = []
    by_family: dict[str, dict[str, int]] = {family: {"total": 0, "complete": 0} for family in PAPER_FAMILIES}
    for record in records:
        family = record.path.split("/")[1]
        by_family.setdefault(family, {"total": 0, "complete": 0})
        by_family[family]["total"] += 1
        meta = record.meta
        ok = (
            isinstance(meta.get("references"), list)
            and bool(meta.get("references_checked_at"))
            and bool(meta.get("references_source"))
            and isinstance(meta.get("references_total"), int)
        )
        if ok:
            complete.append(record.path)
            by_family[family]["complete"] += 1
        else:
            missing.append({
                "path": record.path,
                "canonical_id": record.canonical_id,
                "reason": "missing structured reference audit metadata",
            })
    return {
        "schema_version": 1,
        "reference_audit_version": REFERENCE_AUDIT_VERSION,
        "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": {
            "total": len(records),
            "complete": len(complete),
            "incomplete": len(missing),
        },
        "families": by_family,
        "incomplete": missing,
    }


def graph_report(repo_root: Path) -> dict[str, Any]:
    records = load_records(repo_root)
    outgoing, counts = build_graph(records)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "paper_count": len(records),
        "edge_count": sum(len(v) for v in outgoing.values()),
        "citation_counts": counts,
        "outgoing": {k: sorted(v) for k, v in outgoing.items()},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--graph-report")
    ap.add_argument("--coverage-report")
    ap.add_argument("--strict-coverage", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    graph = graph_report(root)
    coverage = coverage_report(root)
    if args.graph_report:
        Path(args.graph_report).write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.coverage_report:
        Path(args.coverage_report).write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"graph": {"paper_count": graph["paper_count"], "edge_count": graph["edge_count"]}, "coverage": coverage["summary"]}, ensure_ascii=False))
    return 2 if args.strict_coverage and coverage["summary"]["incomplete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
