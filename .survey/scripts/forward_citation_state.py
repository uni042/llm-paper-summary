#!/usr/bin/env python3
"""Backward-compatible durable, sharded forward-citation state.

Small test fixtures retain the original monolithic JSON schema. Once the live
candidate inventory outgrows the inline threshold, the manifest stores seed
cursors and points to fixed hash-partitioned candidate/alias shards. Reading
reconstructs the exact legacy schema; missing/corrupt shards are fatal rather
than silently treating previously discovered citations as absent.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

INLINE_MAX_BYTES = 64 * 1024 * 1024
SHARD_MAX_BYTES = 90 * 1024 * 1024
SHARD_COUNT = 32


def _encode(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"


def _write_text(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)
    return True


def _encode_bounded(value: Any) -> str:
    text = _encode(value)
    size = len(text.encode("utf-8"))
    if size >= SHARD_MAX_BYTES:
        raise ValueError(
            f"forward citation state is {size} bytes; "
            "refusing to create an unpublishable git blob (90 MiB safety limit)"
        )
    return text


def _shard_dir(path: Path) -> Path:
    return path.parent / (path.stem + "-shards")


def _bucket(key: str) -> int:
    return hashlib.sha256(key.encode("utf-8")).digest()[0] % SHARD_COUNT


def load(path: Path, default: Any = None) -> Any:
    path = Path(path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    if not isinstance(raw, dict):
        return raw
    shards = raw.get("candidate_shards")
    if shards is None:
        return raw
    if not isinstance(shards, list) or not shards:
        raise ValueError("invalid forward citation candidate-shard manifest")

    state = dict(raw)
    state.pop("candidate_shards", None)
    candidates: dict[str, Any] = {}
    aliases: dict[str, str] = {}
    for name in shards:
        if not isinstance(name, str) or not name.startswith("part-") or not name.endswith(".json") or "/" in name:
            raise ValueError(f"unsafe candidate-shard filename: {name!r}")
        file = _shard_dir(path) / name
        # Do not silently recover to {} if one committed shard is absent.
        data = json.loads(file.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("candidates"), dict) or not isinstance(data.get("candidate_aliases"), dict):
            raise ValueError(f"malformed forward citation shard: {name}")
        for key, row in data["candidates"].items():
            if key in candidates:
                raise ValueError(f"duplicate candidate key in shards: {key}")
            candidates[key] = row
        for key, target in data["candidate_aliases"].items():
            if key in aliases:
                raise ValueError(f"duplicate alias key in shards: {key}")
            aliases[key] = target
    state["candidates"] = candidates
    state["candidate_aliases"] = aliases
    recorded_count = raw.get("candidate_count")
    if recorded_count is not None and int(recorded_count) != len(candidates):
        raise ValueError(
            f"forward citation shard count mismatch: {len(candidates)} vs {recorded_count}"
        )
    return state


def write(path: Path, value: Any) -> bool:
    path = Path(path)
    # Always enforce the hard guard before constructing a git commit.
    monolithic = _encode(value)
    size = len(monolithic.encode("utf-8"))
    old_manifest = False
    if path.is_file():
        try:
            old_manifest = isinstance(json.loads(path.read_text(encoding="utf-8")).get("candidate_shards"), list)
        except (ValueError, AttributeError):
            pass

    if size < INLINE_MAX_BYTES and not old_manifest:
        return _write_text(path, _encode_bounded(value))
    if not isinstance(value, dict):
        raise ValueError("sharded forward citation state requires an object")
    candidates = value.get("candidates")
    aliases = value.get("candidate_aliases")
    if not isinstance(candidates, dict) or not isinstance(aliases, dict):
        raise ValueError("sharded forward citation state is missing candidates or aliases")

    pieces: list[dict[str, Any]] = [
        {"candidates": {}, "candidate_aliases": {}} for _ in range(SHARD_COUNT)
    ]
    for key, row in candidates.items():
        pieces[_bucket(str(key))]["candidates"][key] = row
    for key, target in aliases.items():
        pieces[_bucket(str(key))]["candidate_aliases"][key] = target

    # Check every output size before touching any file.
    encoded_shards = [_encode_bounded(piece) for piece in pieces]
    manifest = {k: v for k, v in value.items() if k not in ("candidates", "candidate_aliases", "candidate_shards")}
    names = [f"part-{i:02d}.json" for i in range(SHARD_COUNT)]
    manifest["candidate_shards"] = names
    manifest["candidate_count"] = len(candidates)
    encoded_manifest = _encode_bounded(manifest)

    # All changes are local until the containing workflow commits them as
    # one atomic Git revision. A failed push cannot publish a partial manifest.
    changed = False
    directory = _shard_dir(path)
    for name, data in zip(names, encoded_shards):
        changed = _write_text(directory / name, data) or changed
    changed = _write_text(path, encoded_manifest) or changed
    return changed
