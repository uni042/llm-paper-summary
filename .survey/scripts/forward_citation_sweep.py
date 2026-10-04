#!/usr/bin/env python3
"""Fair, low-frequency forward-citation coverage sweep over all collected papers.

This is intentionally separate from the hot Discovery preload lane. Every collected
paper with a Semantic Scholar-compatible stable ID or resolvable primary URL eventually
receives a complete /citations scan. Long citation lists resume from their saved cursor;
after a complete
cycle, the next due cycle starts again at page 1 so newly added citations are seen.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import candidate_priority
import citation_graph
import discovery_provider_adapter
import paper_identity
import reference_pool

CONFIG_PATH = Path(".survey/config/forward-citation-sweep.json")
STATE_PATH = Path(".survey/work-queue/forward-citation-sweep.json")
S2_URL_DOMAINS = ("semanticscholar.org", "arxiv.org", "aclweb.org", "acm.org", "biorxiv.org")


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        name = tmp.name
    Path(name).replace(path)
    return True


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _paper_date(meta: dict[str, Any]) -> dt.date | None:
    raw = meta.get("published")
    if isinstance(raw, dt.datetime):
        return raw.date()
    if isinstance(raw, dt.date):
        return raw
    text = str(raw or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            parsed = dt.datetime.strptime(text, fmt).date()
            if fmt == "%Y-%m":
                parsed = parsed.replace(day=15)
            return parsed
        except ValueError:
            pass
    return None


def _rescan_days(meta: dict[str, Any], config: dict[str, Any], today: dt.date) -> int:
    published = _paper_date(meta)
    age = (today - published).days if published is not None else None
    cadence = config.get("cadence") if isinstance(config.get("cadence"), list) else []
    for row in cadence:
        if not isinstance(row, dict):
            continue
        maximum = row.get("max_paper_age_days")
        days = int(row.get("rescan_days", 90) or 90)
        if maximum is None or (age is not None and age <= int(maximum)):
            return max(days, 1)
    return 90


def _seed_identifier(record: citation_graph.PaperRecord) -> str | None:
    for prefix in ("arXiv:", "DOI:", "SemanticScholar:"):
        matches = sorted(value for value in record.identifiers if value.startswith(prefix))
        if matches:
            return matches[0]
    cid = str(record.canonical_id or "")
    if cid.startswith("SemanticScholar:"):
        return cid
    # Semantic Scholar accepts URL:<paper-url> only for a documented set
    # of scholarly hosts. Unsupported primary URLs stay visible as unsupported
    # rather than entering a permanent 404 retry loop.
    for field in ("source", "source_url", "canonical_url"):
        value = record.meta.get(field)
        if not isinstance(value, str) or not value.startswith(("https://", "http://")):
            continue
        try:
            host = urlparse(value).netloc.casefold().split(":", 1)[0]
        except ValueError:
            continue
        if any(host == domain or host.endswith("." + domain) for domain in S2_URL_DOMAINS):
            return "URL:" + value
    return None


def _s2_api_id(identifier: str) -> str:
    if identifier.startswith("arXiv:"):
        return "ARXIV:" + identifier.split(":", 1)[1]
    if identifier.startswith("SemanticScholar:"):
        return identifier.split(":", 1)[1]
    if identifier.startswith("URL:"):
        return identifier
    return "DOI:" + identifier.split(":", 1)[1]


def _source_url(identifier: str, page_size: int) -> str:
    api_id = quote(_s2_api_id(identifier), safe="")
    fields = discovery_provider_adapter.DEFAULT_FIELDS
    return (
        "https://api.semanticscholar.org/graph/v1/paper/"
        + api_id
        + "/citations?fields="
        + quote(fields, safe=",")
        + f"&limit={page_size}"
    )


def _candidate_alias_index(state: dict[str, Any]) -> dict[str, str]:
    aliases = state.get("candidate_aliases")
    if isinstance(aliases, dict):
        return {str(k): str(v) for k, v in aliases.items()}
    out: dict[str, str] = {}
    candidates = state.get("candidates") if isinstance(state.get("candidates"), dict) else {}
    for key, row in candidates.items():
        if not isinstance(row, dict):
            continue
        for ident in paper_identity.record_identifiers(row):
            out[ident] = str(key)
    return out


def _merge_candidate(
    state: dict[str, Any],
    record: dict[str, Any],
    *,
    source: citation_graph.PaperRecord,
    observed_at: str,
) -> bool:
    identifiers = paper_identity.record_identifiers(record)
    if not identifiers:
        return False
    candidates = state.setdefault("candidates", {})
    aliases = _candidate_alias_index(state)
    matched = {aliases[ident] for ident in identifiers if ident in aliases}
    key = sorted(matched)[0] if matched else (paper_identity.safe_norm_id(record.get("canonical_id")) or sorted(identifiers)[0])
    existing = candidates.get(key, {})
    merged = dict(existing) if isinstance(existing, dict) else {}
    for field, value in record.items():
        if value not in (None, "", [], {}):
            merged[field] = value

    linked_from = set(merged.get("linked_from") or [])
    linked_from.add(source.path)
    merged["linked_from"] = sorted(linked_from)
    titles = set(merged.get("linked_from_titles") or [])
    source_title = str(source.meta.get("title") or "").strip()
    if source_title:
        titles.add(source_title)
    merged["linked_from_titles"] = sorted(titles)
    lineages = set(merged.get("linked_from_lineages") or [])
    lineage = str(source.meta.get("lineage") or "").strip()
    if lineage:
        lineages.add(lineage)
    merged["linked_from_lineages"] = sorted(lineages)
    seeds = set(merged.get("forward_seed_ids") or [])
    seeds.add(source.canonical_id)
    merged["forward_seed_ids"] = sorted(seeds)
    merged["relation_count"] = len(merged["linked_from"])
    merged["discovery_routes"] = sorted(set(merged.get("discovery_routes") or []) | {"forward_citation_sweep"})
    merged.setdefault("first_seen_at", observed_at)
    merged["last_seen_at"] = observed_at
    candidates[key] = merged

    all_ids = set(paper_identity.record_identifiers(merged)) | identifiers
    aliases = state.setdefault("candidate_aliases", {})
    for ident in all_ids:
        aliases[ident] = key
    return True


def _drop_candidates_matching_tokens(state: dict[str, Any], blocked: set[str]) -> int:
    candidates = state.get("candidates") if isinstance(state.get("candidates"), dict) else {}
    remove = [
        key for key, row in candidates.items()
        if isinstance(row, dict) and paper_identity.record_identifiers(row) & blocked
    ]
    for key in remove:
        candidates.pop(key, None)
    if remove:
        live_keys = set(candidates)
        aliases = state.get("candidate_aliases") if isinstance(state.get("candidate_aliases"), dict) else {}
        state["candidate_aliases"] = {alias: key for alias, key in aliases.items() if key in live_keys}
    return len(remove)


def _drop_represented_candidates(state: dict[str, Any], represented: set[str]) -> int:
    return _drop_candidates_matching_tokens(state, represented)


def sweep(root: Path, *, now: dt.datetime | None = None, sleep_fn=time.sleep) -> dict[str, Any]:
    root = Path(root).resolve()
    config = _read(root / CONFIG_PATH, {})
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError(f"invalid forward citation sweep config: {CONFIG_PATH}")
    now = now or _now()
    today = now.date()
    now_text = now.replace(microsecond=0).isoformat()
    max_seeds = int(config.get("max_seeds_per_run", 20) or 20)
    max_pages = int(config.get("max_pages_per_seed_per_run", 2) or 2)
    page_size = int(config.get("page_size", 100) or 100)
    max_provider_errors = max(int(config.get("max_provider_errors_per_run", 1) or 1), 1)
    rate_limit_retries = max(int(config.get("rate_limit_retries_per_request", 0) or 0), 0)
    spacing = max(float(config.get("request_spacing_seconds", 2) or 0), 0.0)

    papers = citation_graph.load_records(root)
    represented = {ident for paper in papers for ident in paper.identifiers}

    # Forward citations are a complementary source, not a second copy of the
    # structured backward-reference queue. If a paper is already present in the
    # live backward pool, keep it only there and never retain a duplicate in the
    # forward-citation state.
    backward_pool = reference_pool.build_reference_pool(root)
    backward_candidates = (
        backward_pool.get("candidates")
        if isinstance(backward_pool, dict)
        else None
    )
    backward_identities: set[str] = set()
    if isinstance(backward_candidates, list):
        for candidate in backward_candidates:
            if isinstance(candidate, dict):
                backward_identities.update(paper_identity.record_identifiers(candidate))

    state = _read(root / STATE_PATH, {})
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        state = {"schema_version": 1, "seeds": {}, "candidates": {}, "candidate_aliases": {}}
    seeds = state.setdefault("seeds", {})

    paper_by_canonical = {paper.canonical_id: paper for paper in papers}
    for paper in papers:
        ident = _seed_identifier(paper)
        row = seeds.get(paper.canonical_id, {})
        row = dict(row) if isinstance(row, dict) else {}
        row.update({
            "canonical_id": paper.canonical_id,
            "paper_path": paper.path,
            "title": paper.meta.get("title"),
            "published": str(paper.meta.get("published") or "") or None,
            "seed_identifier": ident,
            "supported": ident is not None,
            "rescan_days": _rescan_days(paper.meta, config, today),
        })
        row.setdefault("next_cursor", None)
        row.setdefault("last_completed_at", None)
        row.setdefault("cycle_started_at", None)
        seeds[paper.canonical_id] = row

    # Remove seeds for papers no longer represented while keeping candidate evidence.
    for canonical in list(seeds):
        if canonical not in paper_by_canonical:
            seeds.pop(canonical, None)

    def due_key(item: tuple[str, dict[str, Any]]) -> tuple[Any, ...]:
        canonical, row = item
        # Fairness first: an in-progress high-citation seed keeps its cursor but
        # does not monopolize every run. Seeds least recently touched are selected
        # first, so the initial all-paper sweep converges across the whole corpus.
        touches = [
            value
            for value in (
                _parse_time(row.get("last_page_at")),
                _parse_time(row.get("last_attempt_at")),
                _parse_time(row.get("last_completed_at")),
            )
            if value is not None
        ]
        touched = max(touches) if touches else None
        return (0 if touched is None else 1, touched.isoformat() if touched else "", canonical)

    due: list[tuple[str, dict[str, Any]]] = []
    for canonical, row in seeds.items():
        if not isinstance(row, dict) or row.get("supported") is not True:
            continue
        if row.get("cycle_started_at") is not None:
            due.append((canonical, row))
            continue
        completed = _parse_time(row.get("last_completed_at"))
        interval = dt.timedelta(days=max(int(row.get("rescan_days") or 90), 1))
        if completed is None or now - completed >= interval:
            due.append((canonical, row))
    due.sort(key=due_key)
    selected = due[:max(max_seeds, 0)]

    pages_fetched = new_observations = completed_cycles = errors = attempted_seeds = 0
    provider_errors = seed_errors = 0
    provider_error_budget_exhausted = False
    for index, (canonical, seed_state) in enumerate(selected):
        paper = paper_by_canonical[canonical]
        identifier = str(seed_state["seed_identifier"])
        attempted_seeds += 1
        seed_state["last_attempt_at"] = now_text
        fetch = discovery_provider_adapter.semantic_scholar_fetcher(
            _source_url(identifier, page_size),
            page_size=page_size,
            max_rate_limit_retries=rate_limit_retries,
        )
        cursor = seed_state.get("next_cursor")
        if seed_state.get("cycle_started_at") is None:
            seed_state["cycle_started_at"] = now_text
            cursor = None
            seed_state["next_cursor"] = None
        try:
            for page_index in range(max_pages):
                page = fetch(cursor)
                pages_fetched += 1
                records = page.get("records") if isinstance(page, dict) else None
                for candidate in records if isinstance(records, list) else []:
                    if not isinstance(candidate, dict):
                        continue
                    candidate_ids = paper_identity.record_identifiers(candidate)
                    if candidate_ids & represented:
                        continue
                    if candidate_ids & backward_identities:
                        continue
                    if _merge_candidate(state, candidate, source=paper, observed_at=now_text):
                        new_observations += 1
                cursor = page.get("next_cursor") if isinstance(page, dict) else None
                seed_state["next_cursor"] = cursor
                seed_state["last_page_at"] = now_text
                seed_state["last_error"] = None
                if cursor is None:
                    seed_state["last_completed_at"] = now_text
                    seed_state["cycle_started_at"] = None
                    seed_state["next_cursor"] = None
                    seed_state["completed_cycles"] = int(seed_state.get("completed_cycles") or 0) + 1
                    completed_cycles += 1
                    break
                if spacing and page_index + 1 < max_pages:
                    sleep_fn(spacing)
        except Exception as exc:
            errors += 1
            status_code = getattr(exc, "status_code", None)
            seed_state["last_error"] = f"{type(exc).__name__}: {exc}"
            seed_state["last_error_at"] = now_text
            # A paper-specific lookup failure (notably 404) must not abort the
            # corpus-wide sweep. It is rotated to the back by last_attempt_at
            # and retried after other never-scanned/older seeds get a turn.
            # Provider-wide throttling/outage/network failures consume the
            # bounded run-level error budget instead.
            if isinstance(status_code, int) and 400 <= status_code < 500 and status_code != 429:
                seed_errors += 1
                seed_state["coverage_status"] = "seed_error"
            else:
                provider_errors += 1
                seed_state["coverage_status"] = "provider_error"
        seeds[canonical] = seed_state
        if provider_errors >= max_provider_errors:
            provider_error_budget_exhausted = True
            break
        if spacing and index + 1 < len(selected):
            sleep_fn(spacing)

    represented_removed = _drop_represented_candidates(state, represented)
    backward_reference_removed = _drop_candidates_matching_tokens(
        state, backward_identities
    )

    # Candidates already durably classified as unrelated/borderline no longer
    # need to stay in the sweep candidate surface. Their exclusion evidence
    # remains in the canonical ledgers and future sightings will be filtered.
    unrelated = reference_pool._load_ledger_tokens(
        root / reference_pool.DEFAULT_UNRELATED_LEDGER,
        label="unrelated-paper",
    )
    borderline = reference_pool._load_ledger_tokens(
        root / reference_pool.DEFAULT_BORDERLINE_LEDGER,
        label="borderline-paper",
    )
    rejected = unrelated | borderline
    candidates = state.get("candidates") if isinstance(state.get("candidates"), dict) else {}
    rejected_keys = [
        key for key, row in candidates.items()
        if isinstance(row, dict) and paper_identity.record_identifiers(row).intersection(rejected)
    ]
    for key in rejected_keys:
        candidates.pop(key, None)
    if rejected_keys:
        live_keys = set(candidates)
        aliases = state.get("candidate_aliases") if isinstance(state.get("candidate_aliases"), dict) else {}
        state["candidate_aliases"] = {
            alias: key for alias, key in aliases.items() if key in live_keys
        }

    state["schema_version"] = 1
    state["policy"] = config.get("policy_name")
    state["updated_at"] = now_text
    state["paper_count"] = len(papers)
    state["supported_seed_count"] = sum(1 for row in seeds.values() if isinstance(row, dict) and row.get("supported") is True)
    state["unsupported_seed_count"] = sum(1 for row in seeds.values() if isinstance(row, dict) and row.get("supported") is not True)
    state["due_seed_count_before_run"] = len(due)
    state["candidate_count"] = len(state.get("candidates") or {})
    changed = _write(root / STATE_PATH, state)
    return {
        "paper_count": len(papers),
        "supported_seed_count": state["supported_seed_count"],
        "unsupported_seed_count": state["unsupported_seed_count"],
        "due_seed_count_before_run": len(due),
        "selected_seed_count": len(selected),
        "attempted_seed_count": attempted_seeds,
        "pages_fetched": pages_fetched,
        "candidate_observations": new_observations,
        "completed_cycles": completed_cycles,
        "errors": errors,
        "seed_errors": seed_errors,
        "provider_errors": provider_errors,
        "max_provider_errors_per_run": max_provider_errors,
        "rate_limit_retries_per_request": rate_limit_retries,
        "provider_error_budget_exhausted": provider_error_budget_exhausted,
        "represented_candidates_removed": represented_removed,
        "backward_reference_candidates_removed": backward_reference_removed,
        "classified_candidates_removed": len(rejected_keys),
        "candidate_count": state["candidate_count"],
        "state_changed": changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(sweep(args.repo_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
