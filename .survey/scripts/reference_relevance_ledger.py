#!/usr/bin/env python3
"""Maintain durable relevance ledgers for structured-reference Discovery candidates."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import citation_graph

DEFAULT_UNRELATED_LEDGER = Path(".survey/work-queue/reference-curation/unrelated-papers.json")
DEFAULT_BORDERLINE_LEDGER = Path(".survey/work-queue/reference-curation/borderline-papers.json")
DEFAULT_LEDGER = DEFAULT_UNRELATED_LEDGER


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _purpose(classification: str) -> str:
    if classification == "unrelated":
        return "Durable exclusions for papers judged unrelated during structured-reference Discovery curation."
    if classification == "borderline":
        return "Default exclusions for papers judged borderline during structured-reference Discovery curation; entries may be explicitly reconsidered later."
    raise ValueError(f"unsupported classification: {classification}")


def _load(path: Path, *, classification: str) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": 1,
            "classification": classification,
            "purpose": _purpose(classification),
            "records": {},
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"unsupported relevance-ledger schema: {path}")
    if not isinstance(payload.get("records"), dict):
        raise ValueError(f"relevance ledger is missing records: {path}")
    return payload


def _identity_set(canonical_id: str, identity_tokens: list[str] | None = None) -> tuple[str, set[str]]:
    normalized = citation_graph.normalized_identifiers({"canonical_id": canonical_id})
    canonical = normalized[0] if normalized else str(canonical_id).strip()
    if not canonical:
        raise ValueError("canonical_id is required")
    tokens = set(normalized)
    for token in identity_tokens or []:
        token_ids = citation_graph.normalized_identifiers({"canonical_id": token})
        tokens.update(token_ids or ([token.strip()] if token.strip() else []))
    tokens.add(canonical)
    return canonical, tokens


def _write(path: Path, payload: dict[str, Any]) -> None:
    payload["updated_at"] = _now()
    payload["record_count"] = len(payload["records"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _remove_matching(path: Path, *, classification: str, tokens: set[str]) -> bool:
    if not path.exists():
        return False
    payload = _load(path, classification=classification)
    records = payload["records"]
    removed = False
    for key, row in list(records.items()):
        row_tokens = {str(key)}
        if isinstance(row, dict):
            row_tokens.update(str(v) for v in (row.get("identity_tokens") or []) if str(v))
            row_tokens.update(citation_graph.normalized_identifiers(row))
        if tokens.intersection(row_tokens):
            records.pop(key, None)
            removed = True
    if removed:
        _write(path, payload)
    return removed


def mark(
    path: Path,
    *,
    classification: str,
    canonical_id: str,
    title: str | None = None,
    reason: str,
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    opposite_path: Path | None = None,
    opposite_classification: str | None = None,
) -> dict[str, Any]:
    canonical, tokens = _identity_set(canonical_id, identity_tokens)
    payload = _load(path, classification=classification)
    records = payload["records"]

    existing_key = next(
        (
            key
            for key, row in records.items()
            if isinstance(row, dict)
            and tokens.intersection(set(row.get("identity_tokens") or []) | {str(key)})
        ),
        canonical,
    )
    old = records.get(existing_key) if isinstance(records.get(existing_key), dict) else {}
    first_checked = old.get("first_checked_at") or _now()
    source_paths = set(old.get("linked_from") or [])
    source_paths.update(linked_from or [])

    row = {
        "classification": classification,
        "canonical_id": canonical,
        "identity_tokens": sorted(tokens | set(old.get("identity_tokens") or [])),
        "reason": str(reason).strip(),
        "first_checked_at": first_checked,
        "last_checked_at": _now(),
        "linked_from": sorted(str(v) for v in source_paths if str(v).strip()),
    }
    if title or old.get("title"):
        row["title"] = str(title or old.get("title")).strip()

    if existing_key != canonical:
        records.pop(existing_key, None)
    records[canonical] = row
    payload["classification"] = classification
    payload["purpose"] = _purpose(classification)
    _write(path, payload)

    if opposite_path is not None and opposite_classification is not None:
        _remove_matching(
            opposite_path,
            classification=opposite_classification,
            tokens=set(row["identity_tokens"]),
        )
    return row


def mark_unrelated(
    path: Path,
    *,
    canonical_id: str,
    title: str | None = None,
    reason: str = "outside survey scope",
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    borderline_path: Path | None = None,
) -> dict[str, Any]:
    return mark(
        path,
        classification="unrelated",
        canonical_id=canonical_id,
        title=title,
        reason=reason,
        identity_tokens=identity_tokens,
        linked_from=linked_from,
        opposite_path=borderline_path,
        opposite_classification="borderline" if borderline_path is not None else None,
    )


def mark_borderline(
    path: Path,
    *,
    canonical_id: str,
    title: str | None = None,
    reason: str = "borderline relevance or expected survey value",
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    unrelated_path: Path | None = None,
) -> dict[str, Any]:
    return mark(
        path,
        classification="borderline",
        canonical_id=canonical_id,
        title=title,
        reason=reason,
        identity_tokens=identity_tokens,
        linked_from=linked_from,
        opposite_path=unrelated_path,
        opposite_classification="unrelated" if unrelated_path is not None else None,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    for name, default_reason in (
        ("mark-unrelated", "outside survey scope"),
        ("mark-borderline", "borderline relevance or expected survey value"),
    ):
        cmd = sub.add_parser(name)
        cmd.add_argument("--root", default=".")
        cmd.add_argument("--ledger")
        cmd.add_argument("--canonical-id", required=True)
        cmd.add_argument("--identity-token", action="append", default=[])
        cmd.add_argument("--title")
        cmd.add_argument("--reason", default=default_reason)
        cmd.add_argument("--source-path", action="append", default=[])
    args = ap.parse_args()

    root = Path(args.root).resolve()
    unrelated_path = root / DEFAULT_UNRELATED_LEDGER
    borderline_path = root / DEFAULT_BORDERLINE_LEDGER

    if args.command == "mark-unrelated":
        ledger = Path(args.ledger).resolve() if args.ledger else unrelated_path
        row = mark_unrelated(
            ledger,
            canonical_id=args.canonical_id,
            title=args.title,
            reason=args.reason,
            identity_tokens=args.identity_token,
            linked_from=args.source_path,
            borderline_path=borderline_path if ledger == unrelated_path else None,
        )
        label = "無関係"
    elif args.command == "mark-borderline":
        ledger = Path(args.ledger).resolve() if args.ledger else borderline_path
        row = mark_borderline(
            ledger,
            canonical_id=args.canonical_id,
            title=args.title,
            reason=args.reason,
            identity_tokens=args.identity_token,
            linked_from=args.source_path,
            unrelated_path=unrelated_path if ledger == borderline_path else None,
        )
        label = "微妙"
    else:
        return 2

    print(json.dumps({"ok": True, "ledger": str(ledger), "record": row}, ensure_ascii=False))
    print(
        f"[WORKER-GUIDE][完了] {row['canonical_id']} を{label}論文台帳へ保存しました。",
        file=sys.stderr,
    )
    print(
        "[WORKER-GUIDE][次] 同じ識別子は通常の repository_references 探索から除外されます。"
        "次の候補の評価へ進んでください。",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
