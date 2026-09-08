#!/usr/bin/env python3
"""Connector-safe identity deltas for the survey repository.

The format-3 paper identity index is a compacted snapshot. Normal paper writes
may publish a small delta with the paper and state instead of rewriting the
whole snapshot. A checkout-capable runtime can later compact all deltas.
"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import survey  # noqa: E402

ROOT = survey.ROOT
STATE = "survey-state/"
DELTA_DIR = STATE + "identity-deltas/"


def delta_path(canonical_id: str) -> str:
    cid = survey.norm_id(canonical_id)
    if ":" not in cid:
        return DELTA_DIR + "other/" + quote(cid, safe="._-") + ".json"
    kind, body = cid.split(":", 1)
    parts = [quote(part, safe="._-") for part in body.split("/")]
    return DELTA_DIR + kind.lower() + "/" + "/".join(parts) + ".json"


def paper_record(relpath: str) -> dict:
    path = ROOT / relpath
    meta, _ = survey.front(path)
    cid = survey.norm_id(meta["canonical_id"])
    ids = [cid]
    for key, prefix in [
        ("arxiv_id", "arXiv:"),
        ("doi", "DOI:"),
        ("openreview_id", "OpenReview:"),
    ]:
        if meta.get(key):
            ids.append(survey.norm_id(prefix + str(meta[key])))
    return {
        "schema_version": 1,
        "canonical_id": cid,
        "path": relpath,
        "identifiers": sorted(set(ids)),
    }


def read_delta_files() -> list[dict]:
    root = ROOT / DELTA_DIR
    if not root.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(root.rglob("*.json"))]


def logical_lookup(identifier: str):
    ident = survey.norm_id(identifier)
    for record in read_delta_files():
        if ident in record.get("identifiers", []):
            return record["canonical_id"], record["path"], "delta"
    base = survey.read(STATE + "paper-identity-index.json", {}) or {}
    cid = base.get("identifier_to_canonical", {}).get(ident)
    if cid:
        rec = base.get("papers", {}).get(cid, {})
        return cid, rec.get("path"), "snapshot"
    return None


def assert_no_conflicts(record: dict):
    cid = record["canonical_id"]
    path = record["path"]
    base = survey.read(STATE + "paper-identity-index.json", {}) or {}
    base_rec = base.get("papers", {}).get(cid)
    if base_rec and base_rec.get("path") not in (None, path):
        raise ValueError(f"Canonical ID already points to another path: {cid}")
    for other in read_delta_files():
        if other.get("canonical_id") == cid and other.get("path") != path:
            raise ValueError(f"Delta canonical ID already points to another path: {cid}")
    for ident in record["identifiers"]:
        hit = logical_lookup(ident)
        if hit and hit[0] != cid:
            raise ValueError(f"Identifier conflict: {ident} -> {hit[0]}")


def prepare(relpath: str) -> str:
    record = paper_record(relpath)
    assert_no_conflicts(record)
    target = ROOT / delta_path(record["canonical_id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return target.relative_to(ROOT).as_posix()


def validate_all() -> int:
    seen = {}
    base = survey.read(STATE + "paper-identity-index.json", {}) or {}
    records = read_delta_files()
    for record in records:
        expected = paper_record(record["path"])
        if record != expected:
            raise ValueError("Delta does not match paper frontmatter: " + record["path"])
        cid = record["canonical_id"]
        base_rec = base.get("papers", {}).get(cid)
        if base_rec and base_rec.get("path") not in (None, record["path"]):
            raise ValueError(f"Snapshot/delta path conflict: {cid}")
        for ident in record["identifiers"]:
            prev = seen.get(ident)
            if prev and prev != cid:
                raise ValueError(f"Delta identifier conflict: {ident}")
            seen[ident] = cid
            other = base.get("identifier_to_canonical", {}).get(ident)
            if other and other != cid:
                raise ValueError(f"Snapshot/delta conflict: {ident} -> {other}")
    return len(records)


def compact() -> int:
    # Rebuild format-3 snapshot from paper frontmatter, then remove applied deltas.
    survey.write(STATE + "paper-identity-index.json", survey.identity(survey.papers()))
    root = ROOT / DELTA_DIR
    removed = 0
    if root.exists():
        for p in root.rglob("*.json"):
            p.unlink()
            removed += 1
        for d in sorted([p for p in root.rglob("*") if p.is_dir()], reverse=True):
            try:
                d.rmdir()
            except OSError:
                pass
    return removed


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--paper", required=True)
    p = sub.add_parser("lookup")
    p.add_argument("identifier")
    sub.add_parser("validate")
    sub.add_parser("compact")
    args = parser.parse_args()

    if args.cmd == "prepare":
        print(prepare(args.paper))
    elif args.cmd == "lookup":
        hit = logical_lookup(args.identifier)
        print(json.dumps({"found": bool(hit), "result": hit}, ensure_ascii=False))
        raise SystemExit(0 if hit else 1)
    elif args.cmd == "validate":
        print(json.dumps({"delta_count": validate_all()}, ensure_ascii=False))
    elif args.cmd == "compact":
        print(json.dumps({"removed_deltas": compact()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
