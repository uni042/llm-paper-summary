#!/usr/bin/env python3
"""Guarded promotion of clearly distinct neighboring Inference lineages."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import paper_taxonomy

MIN_SUPPORTING_PAPERS = 4
MIN_COLLECTED_SUPPORTS = 2
MAX_NEIGHBOR_LINEAGES = 3
MAX_NEW_LINEAGES_PER_ROUND = 1
_SLUG_TAIL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _norm_identity(value: Any, prefix: str | None = None) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if prefix == "arXiv:" and not raw.lower().startswith("arxiv:"):
        raw = prefix + raw
    elif prefix == "DOI:" and not raw.lower().startswith(("doi:", "https://doi.org/", "http://doi.org/")):
        raw = prefix + raw
    elif prefix == "OpenReview:" and not raw.lower().startswith("openreview:"):
        raw = prefix + raw
    if raw.lower().startswith("arxiv:"):
        return "arXiv:" + re.sub(r"v\d+$", "", raw.split(":", 1)[1], flags=re.I)
    if raw.lower().startswith(("doi:", "https://doi.org/", "http://doi.org/")):
        return "DOI:" + re.sub(r"^(?:doi:|https?://doi.org/)", "", raw, flags=re.I).lower()
    if raw.lower().startswith("openreview:"):
        return "OpenReview:" + raw.split(":", 1)[1]
    return raw


def _record_identities(record: dict[str, Any]) -> set[str]:
    values = {
        _norm_identity(record.get("canonical_id")),
        _norm_identity(record.get("arxiv_id"), "arXiv:"),
        _norm_identity(record.get("doi"), "DOI:"),
        _norm_identity(record.get("openreview_id"), "OpenReview:"),
    }
    return {value for value in values if value}


def _available_identity_sets(repo_root: Path, round_candidates: Iterable[dict[str, Any]]) -> tuple[set[str], set[str]]:
    index = _read_json(repo_root / ".survey/survey-state/paper-identity-index.json", {}) or {}
    collected: set[str] = set()
    if isinstance(index, dict):
        papers = index.get("papers")
        if isinstance(papers, dict):
            for canonical, record in papers.items():
                normalized = _norm_identity(canonical)
                if normalized:
                    collected.add(normalized)
                if isinstance(record, dict):
                    for identity in record.get("identifiers") or []:
                        normalized = _norm_identity(identity)
                        if normalized:
                            collected.add(normalized)
        aliases = index.get("identifier_to_canonical")
        if isinstance(aliases, dict):
            for identity, canonical in aliases.items():
                for value in (identity, canonical):
                    normalized = _norm_identity(value)
                    if normalized:
                        collected.add(normalized)
    available = set(collected)
    for candidate in round_candidates:
        if isinstance(candidate, dict):
            available.update(_record_identities(candidate))
    return available, collected


def _support_identity(value: Any) -> str | None:
    if isinstance(value, str):
        return _norm_identity(value)
    if not isinstance(value, dict):
        return None
    for key, prefix in (
        ("canonical_id", None),
        ("arxiv_id", "arXiv:"),
        ("doi", "DOI:"),
        ("openreview_id", "OpenReview:"),
    ):
        normalized = _norm_identity(value.get(key), prefix)
        if normalized:
            return normalized
    return None


def _slug_tail(value: Any) -> str:
    return re.sub(r"^\d{2}-", "", str(value or "").strip().lower())


def _existing_by_tail(repo_root: Path, tail: str) -> str | None:
    for slug in paper_taxonomy.canonical_inference_lineages(repo_root):
        if re.sub(r"^\d{2}-", "", slug) == tail:
            return slug
    return None


def _allocate_slug(repo_root: Path, tail: str) -> str:
    used = set()
    for slug in paper_taxonomy.canonical_inference_lineages(repo_root):
        match = re.match(r"^(\d{2})-", slug)
        if match and match.group(1) != "99":
            used.add(int(match.group(1)))
    for number in range(1, 99):
        if number not in used:
            return f"{number:02d}-{tail}"
    raise ValueError("no free inference lineage number remains")


def _proposal_id(proposal: dict[str, Any], supports: list[str]) -> str:
    seed = json.dumps(
        {
            "slug_tail": _slug_tail(proposal.get("slug_tail") or proposal.get("slug")),
            "title": str(proposal.get("title") or "").strip(),
            "supports": sorted(supports),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return "lineage-proposal-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def _readme(entry: dict[str, Any]) -> str:
    includes = "\n".join(f"- {value}" for value in entry["scope_includes"])
    excludes = "\n".join(f"- {value}" for value in entry["scope_excludes"])
    neighbors = "\n".join(
        f"- [{value}](../{value}/)" for value in entry["neighbor_lineages"]
    )
    return (
        f"# {entry['title']}\n\n{entry['description']}\n\n"
        f"## 分類境界\n\n{entry['boundary_rule']}\n\n"
        f"### 含める研究\n\n{includes}\n\n"
        f"### 含めない研究\n\n{excludes}\n\n"
        f"## 近傍系統\n\n{neighbors}\n\n"
        "この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。"
        "単一論文だけを理由に細分化せず、上記の分類境界を維持する。\n"
    )


def consider_lineage_proposal(
    repo_root: Path,
    proposal: Any,
    *,
    round_candidates: Iterable[dict[str, Any]],
    source_submission: str | None = None,
    allow_new: bool = True,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if not isinstance(proposal, dict):
        return {"status": "none", "lineage": None, "reasons": []}

    tail = _slug_tail(proposal.get("slug_tail") or proposal.get("slug"))
    title = str(proposal.get("title") or "").strip()
    description = str(proposal.get("description") or "").strip()
    distinctness = str(proposal.get("distinctness_reason") or "").strip()
    boundary = str(proposal.get("boundary_rule") or "").strip()
    confidence = str(proposal.get("confidence") or "").strip().lower()
    includes = [str(v).strip() for v in proposal.get("scope_includes") or [] if str(v).strip()]
    excludes = [str(v).strip() for v in proposal.get("scope_excludes") or [] if str(v).strip()]
    neighbors = list(dict.fromkeys(
        str(v).strip() for v in proposal.get("neighbor_lineages") or [] if str(v).strip()
    ))
    support_values = proposal.get("supporting_papers") or []
    supports = list(dict.fromkeys(
        identity for identity in (_support_identity(v) for v in support_values) if identity
    ))

    available, collected = _available_identity_sets(repo_root, round_candidates)
    verified = [value for value in supports if value in available]
    collected_verified = [value for value in supports if value in collected]
    canonical = set(paper_taxonomy.canonical_inference_lineages(repo_root))
    reasons: list[str] = []

    if not _SLUG_TAIL_RE.fullmatch(tail):
        reasons.append("slug_tail must be lowercase ASCII words joined by hyphens")
    if len(title) < 4:
        reasons.append("title is too short")
    if len(description) < 40:
        reasons.append("description must explain the lineage scope")
    if len(distinctness) < 60:
        reasons.append("distinctness_reason must explain why neighboring lineages are insufficient")
    if len(boundary) < 40:
        reasons.append("boundary_rule must state an operational classification boundary")
    if confidence != "high":
        reasons.append("confidence must be high")
    if not includes or not excludes:
        reasons.append("scope_includes and scope_excludes must both be non-empty")
    if not (1 <= len(neighbors) <= MAX_NEIGHBOR_LINEAGES):
        reasons.append("neighbor_lineages must contain 1-3 canonical neighbors")
    bad_neighbors = [
        value for value in neighbors
        if value not in canonical or value == paper_taxonomy.DEFAULT_INFERENCE_LINEAGE
    ]
    if bad_neighbors:
        reasons.append("neighbor_lineages contains unknown/default lineage: " + ", ".join(bad_neighbors))
    if len(verified) < MIN_SUPPORTING_PAPERS:
        reasons.append(f"need at least {MIN_SUPPORTING_PAPERS} verified supporting papers")
    if len(collected_verified) < MIN_COLLECTED_SUPPORTS:
        reasons.append(f"need at least {MIN_COLLECTED_SUPPORTS} supporting papers already collected")

    proposal_id = _proposal_id(proposal, supports)
    ledger_path = repo_root / ".survey/work-queue/lineage-proposals" / f"{proposal_id}.json"
    ledger = {
        "schema_version": 1,
        "proposal_id": proposal_id,
        "source_submission": source_submission,
        "evaluated_at": _now(),
        "slug_tail": tail,
        "title": title,
        "description": description,
        "distinctness_reason": distinctness,
        "boundary_rule": boundary,
        "scope_includes": includes,
        "scope_excludes": excludes,
        "neighbor_lineages": neighbors,
        "confidence": confidence,
        "supporting_papers": supports,
        "verified_supporting_papers": verified,
        "collected_supporting_papers": collected_verified,
    }

    existing = _existing_by_tail(repo_root, tail) if tail else None
    if existing:
        ledger.update({"status": "existing", "lineage": existing, "reasons": []})
        _write_json(ledger_path, ledger)
        return {"status": "existing", "lineage": existing, "proposal_id": proposal_id, "reasons": []}

    if not allow_new and not reasons:
        reasons.append("one new lineage has already been promoted in this Discovery round")

    if reasons:
        ledger.update({"status": "deferred", "lineage": None, "reasons": reasons})
        _write_json(ledger_path, ledger)
        return {"status": "deferred", "lineage": None, "proposal_id": proposal_id, "reasons": reasons}

    slug = _allocate_slug(repo_root, tail)
    registry_path = repo_root / paper_taxonomy.PROMOTED_INFERENCE_LINEAGES_RELATIVE_PATH
    registry = _read_json(registry_path, {}) or {}
    rows = [row for row in registry.get("lineages") or [] if isinstance(row, dict)]
    entry = {
        "slug": slug,
        "title": title,
        "description": description,
        "distinctness_reason": distinctness,
        "boundary_rule": boundary,
        "scope_includes": includes,
        "scope_excludes": excludes,
        "neighbor_lineages": neighbors,
        "supporting_papers": supports,
        "created_at": _now(),
        "created_from_proposal": proposal_id,
    }
    rows.append(entry)
    rows.sort(key=lambda row: str(row.get("slug") or ""))
    _write_json(registry_path, {"schema_version": 1, "lineages": rows})

    readme = repo_root / "papers/inference" / slug / "README.md"
    if not readme.exists():
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(_readme(entry), encoding="utf-8")

    ledger.update({"status": "promoted", "lineage": slug, "reasons": []})
    _write_json(ledger_path, ledger)
    return {"status": "promoted", "lineage": slug, "proposal_id": proposal_id, "reasons": []}


def route_candidate_to_lineage(candidate: dict[str, Any], lineage: str) -> dict[str, Any]:
    routed = dict(candidate)
    routed["lineage"] = lineage
    paper_path = routed.get("paper_path")
    if isinstance(paper_path, str):
        parts = paper_path.split("/")
        if len(parts) >= 4 and parts[:2] == ["papers", "inference"]:
            parts[2] = lineage
            routed["paper_path"] = "/".join(parts)
    return routed
