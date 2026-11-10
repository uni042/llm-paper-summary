#!/usr/bin/env python3
"""Read and validate the inert-by-default paper retirement registry."""
from __future__ import annotations

import json
import re
import hashlib
import subprocess
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

import paper_identity


REGISTRY_RELATIVE_PATH = Path(".survey/survey-state/paper-retirements.json")


def load_registry(root: Path) -> dict[str, Any]:
    path = Path(root) / REGISTRY_RELATIVE_PATH
    if not path.exists():
        return {"schema_version": 1, "records": {}}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid paper retirement registry: {path}") from exc
    return validate_registry(payload)


def validate_registry(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError("unsupported paper retirement registry schema")
    records = payload.get("records")
    if not isinstance(records, dict):
        raise ValueError("paper retirement registry records must be an object")
    owners: dict[str, str] = {}
    for key, row in records.items():
        if not isinstance(key, str) or not isinstance(row, dict):
            raise ValueError("paper retirement registry contains an invalid record")
        canonical = row.get("canonical_id")
        retirement_id = row.get("retirement_id")
        aliases = row.get("verified_aliases")
        if not isinstance(canonical, str) or not canonical or row.get("classification") != "unrelated":
            raise ValueError(f"invalid retirement identity/classification for {key}")
        if key != canonical or not isinstance(retirement_id, str) or not retirement_id:
            raise ValueError(f"invalid retirement key/id for {key}")
        if not isinstance(aliases, list) or not aliases:
            raise ValueError(f"retirement aliases missing for {key}")
        normalized_aliases = set()
        for alias in aliases:
            normalized = paper_identity.safe_norm_id(alias)
            if not normalized:
                raise ValueError(f"invalid retirement alias for {key}")
            normalized_aliases.add(normalized)
        if paper_identity.safe_norm_id(canonical) not in normalized_aliases:
            raise ValueError(f"canonical identity missing from retirement aliases for {key}")
        if not isinstance(row.get("original_path"), str) or not row["original_path"].startswith("papers/"):
            raise ValueError(f"retirement original_path invalid for {key}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("source_sha256") or "")):
            raise ValueError(f"retirement source_sha256 invalid for {key}")
        if not re.fullmatch(r"[0-9a-f]{40}", str(row.get("source_git_blob_sha") or "")):
            raise ValueError(f"retirement source Git blob invalid for {key}")
        if not re.fullmatch(r"[0-9a-f]{40}", str(row.get("source_commit") or "")):
            raise ValueError(f"retirement source commit invalid for {key}")
        if not str(row.get("reason") or "").strip() or not str(row.get("retirement_id") or "").strip() or not str(row.get("evidence") or "").strip():
            raise ValueError(f"retirement reason/evidence/id missing for {key}")
        if not str(row.get("relevance_request_id") or "").strip() or not str(row.get("relevance_result_id") or "").strip():
            raise ValueError(f"official relevance request/result lineage missing for {key}")
        for token in paper_identity.stable_identity_tokens({"identifiers": aliases}):
            owner = owners.setdefault(token, key)
            if owner != key:
                raise ValueError(f"conflicting retired identity alias: {token}")
    return payload


def find_retirement(root: Path, record: dict[str, Any]) -> dict[str, Any] | None:
    query_tokens = paper_identity.stable_identity_tokens(record)
    if not query_tokens:
        return None
    registry = load_registry(root)
    matches: dict[str, dict[str, Any]] = {}
    for key, row in registry["records"].items():
        aliases = paper_identity.stable_identity_tokens({"identifiers": row["verified_aliases"]})
        if query_tokens & aliases:
            matches[key] = row
    if len(matches) > 1:
        raise ValueError("query resolves to multiple retired papers")
    return next(iter(matches.values()), None)


def validate_source_pin(root: Path, row: dict[str, Any]) -> bool:
    """Prove that a retirement SHA and path are bound to the pinned Git object."""
    root = Path(root).resolve()
    relative = row.get("original_path")
    if not isinstance(relative, str) or "\\" in relative:
        return False
    path = PurePosixPath(relative)
    if path.is_absolute() or not path.is_relative_to(PurePosixPath("papers")) or ".." in path.parts:
        return False
    commit = str(row.get("source_commit") or "")
    expected_blob = str(row.get("source_git_blob_sha") or "")
    expected_sha = str(row.get("source_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", expected_blob) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
        return False
    try:
        resolved = subprocess.run(["git", "rev-parse", f"{commit}:{path.as_posix()}"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
        content = subprocess.run(["git", "show", f"{commit}:{path.as_posix()}"], cwd=root, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    return resolved == expected_blob and hashlib.sha256(content).hexdigest() == expected_sha
