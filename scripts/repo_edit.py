#!/usr/bin/env python3
"""Safe line-oriented text editor for repository maintenance.

This is an emergency helper, not a semantic migration tool. It can read and
edit arbitrary UTF-8 text files beneath a selected root while preventing path
escape and stale overwrites.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_target(root: Path, relpath: str) -> Path:
    root = root.resolve()
    unresolved = root / relpath
    if unresolved.is_symlink():
        raise ValueError(f"Symlink targets are not editable: {relpath}")
    target = unresolved.resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Path escapes root: {relpath}")
    return target


def read_bytes(path: Path) -> bytes:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(path)
    return path.read_bytes()


def read_text(path: Path) -> tuple[str, bytes]:
    raw = read_bytes(path)
    return raw.decode("utf-8"), raw


def normalized_range(start: int, end: int | None, count: int) -> tuple[int, int]:
    if start < 1:
        raise ValueError("Line numbers are 1-based and must be >= 1")
    end = start if end is None else end
    if end < start:
        raise ValueError("end-line must be >= start-line")
    if count == 0 or start > count or end > count:
        raise ValueError(f"Line range {start}-{end} exceeds file length {count}")
    return start - 1, end


def load_payload(args) -> str:
    if getattr(args, "text", None) is not None and getattr(args, "text_file", None) is not None:
        raise ValueError("Use only one of --text or --text-file")
    if getattr(args, "text_file", None) is not None:
        return Path(args.text_file).read_text(encoding="utf-8")
    if getattr(args, "text", None) is not None:
        return args.text
    return ""


def line_chunks(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def ensure_line_ending(payload: str, reference: list[str]) -> str:
    if not payload or payload.endswith(("\n", "\r")):
        return payload
    newline = "\n"
    for line in reference:
        if line.endswith("\r\n"):
            newline = "\r\n"
            break
        if line.endswith("\n"):
            break
    return payload + newline


def render_diff(relpath: str, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{relpath}",
            tofile=f"b/{relpath}",
        )
    )


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_name, mode)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def check_precondition(raw: bytes, expected: str | None) -> str:
    actual = sha256_bytes(raw)
    if expected and expected.lower() != actual:
        raise ValueError(f"SHA-256 precondition failed: expected {expected}, actual {actual}")
    return actual


def command_read(args) -> int:
    path = resolve_target(Path(args.root), args.path)
    text, raw = read_text(path)
    lines = line_chunks(text)
    start = args.start_line or 1
    end = args.end_line if args.end_line is not None else len(lines)
    if not lines:
        selected = []
    else:
        a, b = normalized_range(start, end, len(lines))
        selected = lines[a:b]
    if args.json:
        print(json.dumps({
            "path": args.path,
            "sha256": sha256_bytes(raw),
            "line_count": len(lines),
            "start_line": start,
            "end_line": end,
            "text": "".join(selected),
        }, ensure_ascii=False, indent=2))
    elif args.number:
        for i, line in enumerate(selected, start=start):
            print(f"{i}: {line}", end="" if line.endswith(("\n", "\r")) else "\n")
    else:
        print("".join(selected), end="")
    return 0


def edit_text(before: str, args) -> str:
    lines = line_chunks(before)
    payload = load_payload(args)
    if args.command == "append":
        return before + ensure_line_ending(payload, lines)
    if args.command == "insert":
        if args.line < 1 or args.line > len(lines) + 1:
            raise ValueError(f"Insert line {args.line} exceeds valid range 1-{len(lines)+1}")
        payload = ensure_line_ending(payload, lines)
        idx = args.line - 1
        if args.position == "after":
            if args.line > len(lines):
                raise ValueError("Cannot insert after line_count + 1")
            idx = args.line
        return "".join(lines[:idx] + ([payload] if payload else []) + lines[idx:])
    a, b = normalized_range(args.start_line, args.end_line, len(lines))
    if args.command == "delete":
        return "".join(lines[:a] + lines[b:])
    if args.command == "replace":
        payload = ensure_line_ending(payload, lines)
        return "".join(lines[:a] + ([payload] if payload else []) + lines[b:])
    raise ValueError(args.command)


def command_edit(args) -> int:
    path = resolve_target(Path(args.root), args.path)
    before, raw = read_text(path)
    old_sha = check_precondition(raw, args.expect_sha256)
    after = edit_text(before, args)
    diff = render_diff(args.path, before, after)
    new_sha = sha256_bytes(after.encode("utf-8"))
    result = {
        "path": args.path,
        "old_sha256": old_sha,
        "new_sha256": new_sha,
        "changed": before != after,
        "applied": bool(args.apply and before != after),
        "diff": diff,
    }
    if args.apply and before != after:
        atomic_write(path, after)
        if sha256_bytes(read_bytes(path)) != new_sha:
            raise RuntimeError("Post-write SHA-256 verification failed")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(diff if diff else "(no change)\n", end="")
        print(json.dumps({k: v for k, v in result.items() if k != "diff"}, ensure_ascii=False))
    return 0


def add_common_path(parser):
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Allowed root; target paths may not escape it")
    parser.add_argument("--path", required=True, help="UTF-8 text file path relative to --root")
    parser.add_argument("--json", action="store_true")


def add_mutation_common(parser):
    add_common_path(parser)
    parser.add_argument("--expect-sha256", help="Abort if current file SHA-256 differs")
    parser.add_argument("--apply", action="store_true", help="Write atomically; without this only show the proposed diff")


def add_payload(parser):
    parser.add_argument("--text")
    parser.add_argument("--text-file")


def main() -> int:
    p = argparse.ArgumentParser(description="Safely read and edit line ranges beneath a root directory")
    sub = p.add_subparsers(dest="command", required=True)

    q = sub.add_parser("read")
    add_common_path(q)
    q.add_argument("--start-line", type=int)
    q.add_argument("--end-line", type=int)
    q.add_argument("--number", action="store_true")

    q = sub.add_parser("insert")
    add_mutation_common(q)
    q.add_argument("--line", required=True, type=int)
    q.add_argument("--position", choices=["before", "after"], default="before")
    add_payload(q)

    q = sub.add_parser("replace")
    add_mutation_common(q)
    q.add_argument("--start-line", required=True, type=int)
    q.add_argument("--end-line", type=int)
    add_payload(q)

    q = sub.add_parser("delete")
    add_mutation_common(q)
    q.add_argument("--start-line", required=True, type=int)
    q.add_argument("--end-line", type=int)

    q = sub.add_parser("append")
    add_mutation_common(q)
    add_payload(q)

    args = p.parse_args()
    return command_read(args) if args.command == "read" else command_edit(args)


if __name__ == "__main__":
    raise SystemExit(main())
