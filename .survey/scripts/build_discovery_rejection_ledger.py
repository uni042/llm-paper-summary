#!/usr/bin/env python3
"""Build the durable Discovery candidate-evaluation rejection ledger.

The immutable Discovery submission remains the source of truth. Scheduled Chat records
papers that reached candidate evaluation but were not selected in ``rejected_candidates``.
This builder folds those immutable observations into a compact identity-indexed ledger
that retrieval-stage filtering can consult before showing search results to a worker.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import paper_identity


SOURCE = "immutable_discovery_submissions.rejected_candidates"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _source_label(root: Path, path: Path) -> str:
    try:
        return (Path(".survey") / path.relative_to(root)).as_posix()
    except ValueError:
        return path.as_posix()


def _timestamp(payload: dict[str, Any]) -> str:
    value = payload.get("submitted_at")
    if isinstance(value, str) and value.strip():
        return value.strip()
    meta = payload.get("discovery_stats")
    if isinstance(meta, dict):
        value = meta.get("run_key")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _merge_timestamp(current: str | None, incoming: str, *, earliest: bool) -> str | None:
    values = [value for value in (current, incoming) if isinstance(value, str) and value]
    if not values:
        return None
    return min(values) if earliest else max(values)


def build_ledger(root: Path, output: Path | None = None) -> dict[str, Any]:
    root = Path(root)
    queue = root / "work-queue"
    submissions = queue / "submissions"
    output = Path(output) if output is not None else queue / "discovery-rejections.json"

    records: dict[str, dict[str, Any]] = {}
    submission_count = 0
    rejection_observation_count = 0
    ignored_without_identity = 0

    if submissions.exists():
        for path in sorted(submissions.rglob("*.json")):
            payload = _read_json(path)
            if not isinstance(payload, dict):
                continue
            rejected = payload.get("rejected_candidates")
            if not isinstance(rejected, list) or not rejected:
                continue
            submission_count += 1
            meta = payload.get("discovery_stats") if isinstance(payload.get("discovery_stats"), dict) else {}
            axis = str(meta.get("axis") or "").strip() or None
            run_key = str(meta.get("run_key") or "").strip() or None
            rejected_at = _timestamp(payload)
            source_submission = _source_label(root, path)

            for candidate in rejected:
                if not isinstance(candidate, dict):
                    continue
                tokens = sorted(paper_identity.identity_tokens(candidate))
                primary = paper_identity.primary_identity_key(candidate)
                if not primary:
                    ignored_without_identity += 1
                    continue
                rejection_observation_count += 1
                reason = str(
                    candidate.get("rejection_reason")
                    or candidate.get("reason")
                    or "candidate evaluation rejected"
                ).strip()
                existing = records.get(primary)
                if existing is None:
                    records[primary] = {
                        "primary_identity": primary,
                        "identity_tokens": tokens,
                        "canonical_id": candidate.get("canonical_id"),
                        "arxiv_id": candidate.get("arxiv_id"),
                        "doi": candidate.get("doi"),
                        "openreview_id": candidate.get("openreview_id"),
                        "title": candidate.get("title"),
                        "source_url": candidate.get("source_url"),
                        "rejection_reason": reason,
                        "rejection_count": 1,
                        "first_rejected_at": rejected_at or None,
                        "last_rejected_at": rejected_at or None,
                        "axis": axis,
                        "run_key": run_key,
                        "source_submission": source_submission,
                    }
                    continue

                existing["rejection_count"] = int(existing.get("rejection_count", 0) or 0) + 1
                existing["identity_tokens"] = sorted(set(existing.get("identity_tokens") or []) | set(tokens))
                existing["first_rejected_at"] = _merge_timestamp(
                    existing.get("first_rejected_at"), rejected_at, earliest=True
                )
                previous_last = existing.get("last_rejected_at")
                incoming_is_latest = not previous_last or not rejected_at or rejected_at >= previous_last
                existing["last_rejected_at"] = _merge_timestamp(previous_last, rejected_at, earliest=False)
                if incoming_is_latest:
                    for field in ("canonical_id", "arxiv_id", "doi", "openreview_id", "title", "source_url"):
                        if candidate.get(field) is not None:
                            existing[field] = candidate.get(field)
                    existing["rejection_reason"] = reason
                    existing["axis"] = axis
                    existing["run_key"] = run_key
                    existing["source_submission"] = source_submission

    latest_rejected_at = max(
        (str(record.get("last_rejected_at")) for record in records.values() if record.get("last_rejected_at")),
        default=None,
    )
    ledger = {
        "schema_version": 1,
        "source": SOURCE,
        "updated_at": latest_rejected_at,
        "submission_count": submission_count,
        "rejection_observation_count": rejection_observation_count,
        "rejection_record_count": len(records),
        "ignored_without_identity": ignored_without_identity,
        "records": {key: records[key] for key in sorted(records)},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "output": output.as_posix(),
        "submission_count": submission_count,
        "rejection_observation_count": rejection_observation_count,
        "rejection_record_count": len(records),
        "ignored_without_identity": ignored_without_identity,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = build_ledger(args.root, args.output)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
