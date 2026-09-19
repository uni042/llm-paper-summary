#!/usr/bin/env python3
"""Maintain the durable exclusion ledger for unrelated structured-reference candidates."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import citation_graph

DEFAULT_LEDGER = Path(".survey/work-queue/reference-curation/unrelated-papers.json")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": 1,
            "purpose": "Durable exclusions for papers judged unrelated during structured-reference Discovery curation.",
            "records": {},
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"unsupported unrelated-paper ledger schema: {path}")
    if not isinstance(payload.get("records"), dict):
        raise ValueError(f"unrelated-paper ledger is missing records: {path}")
    return payload


def mark_unrelated(
    path: Path,
    *,
    canonical_id: str,
    title: str | None = None,
    reason: str = "outside survey scope",
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
) -> dict[str, Any]:
    normalized = citation_graph.normalized_identifiers({"canonical_id": canonical_id})
    canonical = normalized[0] if normalized else str(canonical_id).strip()
    if not canonical:
        raise ValueError("canonical_id is required")

    tokens = set(normalized)
    for token in identity_tokens or []:
        token_ids = citation_graph.normalized_identifiers({"canonical_id": token})
        tokens.update(token_ids or ([token.strip()] if token.strip() else []))
    tokens.add(canonical)

    payload = _load(path)
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
        "canonical_id": canonical,
        "identity_tokens": sorted(tokens | set(old.get("identity_tokens") or [])),
        "reason": str(reason or "outside survey scope").strip(),
        "first_checked_at": first_checked,
        "last_checked_at": _now(),
        "linked_from": sorted(str(v) for v in source_paths if str(v).strip()),
    }
    if title or old.get("title"):
        row["title"] = str(title or old.get("title")).strip()

    if existing_key != canonical:
        records.pop(existing_key, None)
    records[canonical] = row
    payload["updated_at"] = _now()
    payload["record_count"] = len(records)

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    mark = sub.add_parser("mark-unrelated")
    mark.add_argument("--root", default=".")
    mark.add_argument("--ledger")
    mark.add_argument("--canonical-id", required=True)
    mark.add_argument("--identity-token", action="append", default=[])
    mark.add_argument("--title")
    mark.add_argument("--reason", default="outside survey scope")
    mark.add_argument("--source-path", action="append", default=[])
    args = ap.parse_args()

    if args.command != "mark-unrelated":
        return 2
    root = Path(args.root).resolve()
    ledger = Path(args.ledger).resolve() if args.ledger else root / DEFAULT_LEDGER
    row = mark_unrelated(
        ledger,
        canonical_id=args.canonical_id,
        title=args.title,
        reason=args.reason,
        identity_tokens=args.identity_token,
        linked_from=args.source_path,
    )
    print(json.dumps({"ok": True, "ledger": str(ledger), "record": row}, ensure_ascii=False))
    print(
        f"[WORKER-GUIDE][完了] {row['canonical_id']} を無関係論文台帳へ永続保存しました。",
        file=sys.stderr,
    )
    print(
        "[WORKER-GUIDE][次] 同じ識別子は repository_references 探索から以後除外されます。"
        "次の候補の評価へ進んでください。",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
