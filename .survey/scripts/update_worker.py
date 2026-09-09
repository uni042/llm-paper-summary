#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

ALLOWED_PREFIXES = ("framework-updates/", "llm-releases/")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def normalize_target(path_text: str) -> str:
    p = PurePosixPath(path_text)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe target path: {path_text}")
    normalized = p.as_posix()
    if not normalized.startswith(ALLOWED_PREFIXES):
        raise ValueError(
            f"target outside allowed update areas: {normalized}; "
            f"allowed={ALLOWED_PREFIXES}"
        )
    return normalized


def write_result(result_path: Path, payload: dict[str, Any]) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".survey")
    args = parser.parse_args()

    survey_root = Path(args.root).resolve()
    repo_root = survey_root.parent
    inbox_path = survey_root / "update-worker" / "update-inbox.json"
    result_path = survey_root / "update-worker" / "result.json"

    attempt_id: str | None = None
    try:
        inbox = load_json(inbox_path)
        if inbox.get("schema_version") != 1:
            raise ValueError("unsupported inbox schema_version")
        attempt_id = inbox.get("attempt_id")
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            raise ValueError("inbox attempt_id must be a non-empty string")

        payload_path_text = inbox.get("payload_path")
        if not isinstance(payload_path_text, str) or not payload_path_text.strip():
            raise ValueError("payload_path must be a non-empty string")
        payload_rel = PurePosixPath(payload_path_text)
        if payload_rel.is_absolute() or ".." in payload_rel.parts:
            raise ValueError("unsafe payload_path")
        if payload_rel.as_posix() != ".survey/update-worker/update-payload.json":
            raise ValueError("only the fixed reusable update payload is accepted")

        payload = load_json(repo_root / payload_rel.as_posix())
        if payload.get("schema_version") != 1:
            raise ValueError("unsupported payload schema_version")
        if payload.get("attempt_id") != attempt_id:
            raise ValueError("inbox/payload attempt_id mismatch")
        if payload.get("kind") != "framework_llm_update":
            raise ValueError("unsupported payload kind")

        artifacts = payload.get("artifacts")
        if not isinstance(artifacts, list):
            raise ValueError("artifacts must be a list")
        if len(artifacts) > 40:
            raise ValueError("too many artifacts in one update")

        validated: list[tuple[str, str, str | None, bool]] = []
        seen: set[str] = set()
        for idx, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                raise ValueError(f"artifact[{idx}] must be an object")
            target_raw = artifact.get("path")
            content = artifact.get("content")
            expected = artifact.get("expected_blob_sha")
            if not isinstance(target_raw, str) or not target_raw.strip():
                raise ValueError(f"artifact[{idx}].path must be non-empty")
            if not isinstance(content, str):
                raise ValueError(f"artifact[{idx}].content must be a string")
            if expected is not None and not isinstance(expected, str):
                raise ValueError(f"artifact[{idx}].expected_blob_sha must be string/null")

            target = normalize_target(target_raw)
            if target in seen:
                raise ValueError(f"duplicate target path: {target}")
            seen.add(target)

            target_path = repo_root / target
            exists = target_path.exists()
            if exists:
                current = git_blob_sha(target_path.read_bytes())
                if not expected:
                    raise ValueError(f"expected_blob_sha required for existing file: {target}")
                if current != expected:
                    raise ValueError(
                        f"blob SHA mismatch for {target}: expected {expected}, current {current}"
                    )
            elif expected:
                raise ValueError(f"expected_blob_sha must be null/omitted for new file: {target}")

            validated.append((target, content, expected, exists))

        # All validation completes before any target is modified.
        for target, content, _expected, _exists in validated:
            target_path = repo_root / target
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")

        write_result(
            result_path,
            {
                "schema_version": 1,
                "ok": True,
                "attempt_id": attempt_id,
                "kind": "framework_llm_update",
                "updated_paths": [v[0] for v in validated],
                "created_paths": [v[0] for v in validated if not v[3]],
                "updated_existing_paths": [v[0] for v in validated if v[3]],
                "summary": payload.get("summary"),
            },
        )
        return 0

    except Exception as exc:
        write_result(
            result_path,
            {
                "schema_version": 1,
                "ok": False,
                "attempt_id": attempt_id,
                "error": f"{type(exc).__name__}: {exc}",
            },
        )
        # Handled validation/application errors are persisted as result.json.
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
