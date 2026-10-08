#!/usr/bin/env python3
"""Lossless sharded priority cache, preserving the original load_cache interface.

Never discard provider observations or failed-lookup provenance to fit GitHub's
per-file size cap. A compact manifest references 32 hash-partitioned files.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from forward_citation_state import _encode, _encode_bounded, _write_text

PARTS = 32
INLINE_LIMIT = 64 * 1024 * 1024
MAPPINGS = ("records", "aliases", "lookup_failures")


def _shard_dir(path: Path) -> Path:
    return path.parent / (path.stem + "-shards")


def _part(key: str) -> int:
    return hashlib.sha256(str(key).encode("utf-8")).digest()[0] % PARTS


def load(path: Path, default: Any = None) -> Any:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    if not isinstance(data, dict) or "cache_shards" not in data:
        return data
    names = data["cache_shards"]
    if not isinstance(names, list) or len(names) != PARTS or len(set(names)) != PARTS:
        raise ValueError("malformed candidate-priority shard manifest")
    merged: dict[str, Any] = {k: v for k, v in data.items() if k not in ("cache_shards", "cache_record_count")}
    for key in MAPPINGS:
        merged[key] = {}
    for name in names:
        if not isinstance(name, str) or not name.startswith("part-") or not name.endswith(".json") or "/" in name:
            raise ValueError(f"invalid candidate-priority shard name: {name!r}")
        payload = json.loads((_shard_dir(path) / name).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"malformed candidate-priority shard: {name}")
        for mapping in MAPPINGS:
            part = payload.get(mapping)
            if not isinstance(part, dict):
                raise ValueError(f"missing {mapping} in candidate-priority shard: {name}")
            if merged[mapping].keys() & part.keys():
                raise ValueError(f"duplicate candidate-priority mapping keys: {mapping} {name}")
            merged[mapping].update(part)
    if len(merged["records"]) != data.get("cache_record_count"):
        raise ValueError("candidate-priority cache record count does not match shards")
    return merged


def write(path: Path, value: dict[str, Any]) -> bool:
    path = Path(path)
    encoded = _encode(value)
    try:
        old = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        old = {}
    sharded = isinstance(old, dict) and "cache_shards" in old
    if len(encoded.encode("utf-8")) < INLINE_LIMIT and not sharded:
        return _write_text(path, _encode_bounded(value))

    if not isinstance(value, dict) or any(not isinstance(value.get(k), dict) for k in MAPPINGS):
        raise ValueError("cannot shard priority cache without records, aliases, lookup_failures")
    parts = [{key: {} for key in MAPPINGS} for _ in range(PARTS)]
    for mapping in MAPPINGS:
        for key, row in value[mapping].items():
            parts[_part(key)][mapping][key] = row
    encoded_parts = [_encode_bounded(part) for part in parts]
    names = [f"part-{i:02d}.json" for i in range(PARTS)]
    manifest = {k: v for k, v in value.items() if k not in MAPPINGS and k != "cache_shards"}
    manifest["cache_shards"] = names
    manifest["cache_record_count"] = len(value["records"])
    encoded_manifest = _encode_bounded(manifest)
    changed = False
    directory = _shard_dir(path)
    for name, raw in zip(names, encoded_parts):
        changed = _write_text(directory / name, raw) or changed
    changed = _write_text(path, encoded_manifest) or changed
    return changed
