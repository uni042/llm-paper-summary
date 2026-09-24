#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

ALLOWED_PREFIXES = ("framework-updates/", "llm-releases/")
ALLOWED_EDIT_OPS = {"replace_once", "insert_after_once", "insert_before_once"}
REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


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
            f"target outside allowed update areas: {normalized}; allowed={ALLOWED_PREFIXES}"
        )
    return normalized


def apply_edits(original: str, edits: list[Any], target: str) -> str:
    text = original
    for edit_idx, edit in enumerate(edits):
        if not isinstance(edit, dict):
            raise ValueError(f"{target} edit[{edit_idx}] must be an object")
        op = edit.get("op")
        if op not in ALLOWED_EDIT_OPS:
            raise ValueError(f"unsupported edit op for {target}: {op}")

        if op == "replace_once":
            old = edit.get("old")
            new = edit.get("new")
            if not isinstance(old, str) or not old:
                raise ValueError(f"replace_once.old must be non-empty for {target}")
            if not isinstance(new, str):
                raise ValueError(f"replace_once.new must be a string for {target}")
            count = text.count(old)
            if count != 1:
                raise ValueError(
                    f"replace_once expected exactly one match in {target}, found {count}"
                )
            text = text.replace(old, new, 1)

        elif op == "insert_after_once":
            anchor = edit.get("anchor")
            insertion = edit.get("text")
            if not isinstance(anchor, str) or not anchor:
                raise ValueError(f"insert_after_once.anchor must be non-empty for {target}")
            if not isinstance(insertion, str):
                raise ValueError(f"insert_after_once.text must be a string for {target}")
            count = text.count(anchor)
            if count != 1:
                raise ValueError(
                    f"insert_after_once expected exactly one anchor in {target}, found {count}"
                )
            text = text.replace(anchor, anchor + insertion, 1)

        elif op == "insert_before_once":
            anchor = edit.get("anchor")
            insertion = edit.get("text")
            if not isinstance(anchor, str) or not anchor:
                raise ValueError(f"insert_before_once.anchor must be non-empty for {target}")
            if not isinstance(insertion, str):
                raise ValueError(f"insert_before_once.text must be a string for {target}")
            count = text.count(anchor)
            if count != 1:
                raise ValueError(
                    f"insert_before_once expected exactly one anchor in {target}, found {count}"
                )
            text = text.replace(anchor, insertion + anchor, 1)

    return text


def write_result(result_path: Path, payload: dict[str, Any]) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def validate_and_apply(repo_root: Path, request: dict[str, Any]) -> dict[str, Any]:
    if request.get("schema_version") != 1:
        raise ValueError("unsupported request schema_version")

    attempt_id = request.get("attempt_id")
    if not isinstance(attempt_id, str) or not attempt_id.strip():
        raise ValueError("attempt_id must be a non-empty string")
    if not REQUEST_ID_RE.fullmatch(attempt_id):
        raise ValueError("attempt_id contains unsafe characters")
    if request.get("kind") != "framework_llm_update":
        raise ValueError("unsupported request kind")

    artifacts = request.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("artifacts must be a list")
    if len(artifacts) > 40:
        raise ValueError("too many artifacts in one update")

    validated: list[tuple[str, str, bool]] = []
    seen: set[str] = set()
    for idx, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"artifact[{idx}] must be an object")

        target_raw = artifact.get("path")
        expected = artifact.get("expected_blob_sha")
        if not isinstance(target_raw, str) or not target_raw.strip():
            raise ValueError(f"artifact[{idx}].path must be non-empty")
        if expected is not None and not isinstance(expected, str):
            raise ValueError(f"artifact[{idx}].expected_blob_sha must be string/null")

        target = normalize_target(target_raw)
        if target in seen:
            raise ValueError(f"duplicate target path: {target}")
        seen.add(target)

        target_path = repo_root / target
        exists = target_path.exists()
        if exists:
            current_bytes = target_path.read_bytes()
            current = git_blob_sha(current_bytes)
            if not expected:
                raise ValueError(f"expected_blob_sha required for existing file: {target}")
            if current != expected:
                raise ValueError(
                    f"blob SHA mismatch for {target}: expected {expected}, current {current}"
                )

            has_content = "content" in artifact
            has_edits = "edits" in artifact
            if has_content == has_edits:
                raise ValueError(
                    f"existing file {target} must specify exactly one of content or edits"
                )
            if has_content:
                content = artifact.get("content")
                if not isinstance(content, str):
                    raise ValueError(f"artifact[{idx}].content must be a string")
                new_content = content
            else:
                edits = artifact.get("edits")
                if not isinstance(edits, list) or not edits:
                    raise ValueError(f"artifact[{idx}].edits must be a non-empty list")
                new_content = apply_edits(current_bytes.decode("utf-8"), edits, target)
        else:
            if expected:
                raise ValueError(
                    f"expected_blob_sha must be null/omitted for new file: {target}"
                )
            content = artifact.get("content")
            if not isinstance(content, str):
                raise ValueError(f"new file {target} requires string content")
            if "edits" in artifact:
                raise ValueError(f"new file {target} cannot use edits")
            new_content = content

        validated.append((target, new_content, exists))

    # Validate every artifact before writing any target.
    for target, content, _exists in validated:
        target_path = repo_root / target
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")

    return {
        "schema_version": 1,
        "ok": True,
        "attempt_id": attempt_id,
        "kind": "framework_llm_update",
        "updated_paths": [v[0] for v in validated],
        "created_paths": [v[0] for v in validated if not v[2]],
        "updated_existing_paths": [v[0] for v in validated if v[2]],
        "summary": request.get("summary"),
    }


def process_request(survey_root: Path, request_path: Path) -> dict[str, Any]:
    repo_root = survey_root.parent
    result_path = survey_root / "update-worker" / "results" / request_path.name
    attempt_hint = request_path.stem

    try:
        request = load_json(request_path)
        attempt_id = request.get("attempt_id")
        if attempt_id != request_path.stem:
            raise ValueError(
                f"request filename/attempt_id mismatch: {request_path.stem} != {attempt_id}"
            )
        result = validate_and_apply(repo_root, request)
    except Exception as exc:
        result = {
            "schema_version": 1,
            "ok": False,
            "attempt_id": attempt_hint,
            "error": f"{type(exc).__name__}: {exc}",
        }

    write_result(result_path, result)
    # Keep the old single-result surface only as a compatibility pointer.
    write_result(survey_root / "update-worker" / "result.json", result)
    return result


def pending_requests(survey_root: Path) -> list[Path]:
    request_dir = survey_root / "update-worker" / "requests"
    result_dir = survey_root / "update-worker" / "results"
    if not request_dir.is_dir():
        return []
    return [
        path
        for path in sorted(request_dir.glob("*.json"))
        if not (result_dir / path.name).is_file()
    ]


def normalize_explicit_request(repo_root: Path, survey_root: Path, raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    request_dir = (survey_root / "update-worker" / "requests").resolve()
    if path.parent != request_dir or path.suffix != ".json":
        raise ValueError("request must be under .survey/update-worker/requests/*.json")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".survey")
    parser.add_argument("--request")
    args = parser.parse_args()

    survey_root = Path(args.root).resolve()
    repo_root = survey_root.parent

    if args.request:
        request_path = normalize_explicit_request(repo_root, survey_root, args.request)
        results = [process_request(survey_root, request_path)]
    else:
        requests = pending_requests(survey_root)
        if not requests:
            print(json.dumps({
                "action": "noop",
                "reason": "no_pending_immutable_update_requests",
            }))
            return 0
        results = [process_request(survey_root, path) for path in requests]

    print(json.dumps({
        "action": "processed",
        "request_count": len(results),
        "ok_count": sum(1 for item in results if item.get("ok") is True),
        "failed_count": sum(1 for item in results if item.get("ok") is not True),
        "attempt_ids": [item.get("attempt_id") for item in results],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
