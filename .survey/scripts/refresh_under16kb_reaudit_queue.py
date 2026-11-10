#!/usr/bin/env python3
"""Build the durable semantic re-audit queue for paper summaries below 16,000 bytes.

The queue is intentionally broader than the normal publication gate.  File size is
only the entry trigger; leaving the queue requires a current-version semantic
attestation plus deterministic explanation/language checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

import audit_paper_quality as quality

QUEUE_PATH = Path(".survey/repair-queue/under-16kb-reaudit.json")
REAUDIT_VERSION = "2026-10-07-v1"
MAX_FILE_BYTES = 16_000
MIN_JAPANESE_RATIO = 0.80
MIN_BODY_CHARS = 2_200
MIN_METHOD_CHARS = 700
MIN_EVALUATION_CHARS = 500
WORKERS = ("scheduled-chat-00", "scheduled-chat-30", "scheduled-chat-45")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}".encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}
    try:
        value = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def assigned_worker(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).digest()
    return WORKERS[digest[0] % len(WORKERS)]


def previous_queue_assignments(repo_root: Path) -> dict[str, str]:
    """Preserve existing ownership to avoid reshuffling running workers."""
    target = repo_root.resolve() / QUEUE_PATH
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(payload, dict) or (
        payload.get("queue_kind") != "under_16kb_semantic_reaudit"
        or payload.get("queue_version") != REAUDIT_VERSION
    ):
        return {}
    entries = payload.get("entries")
    if not isinstance(entries, list):
        return {}
    result: dict[str, str] = {}
    for row in entries:
        if not isinstance(row, dict):
            continue
        paper_path = str(row.get("path") or "")
        owner = row.get("assigned_worker")
        if paper_path.startswith("papers/") and owner in WORKERS:
            result[paper_path] = owner
    return result


def rebalance_workers(
    entries: list[dict[str, Any]],
    previous: dict[str, str] | None = None,
    protected_each_end: int = 5,
) -> None:
    """Balance *remaining* papers with minimal ownership changes.

    Existing owners take precedence over the hash fallback. Protect the first
    and last few tasks of each worker because a scheduled chat might already
    be using either end of its prior queue snapshot. No paper is duplicated.
    """
    previous = previous or {}
    for row in entries:
        path = str(row["path"])
        row["assigned_worker"] = previous.get(path, row.get("assigned_worker"))
        if row["assigned_worker"] not in WORKERS:
            row["assigned_worker"] = assigned_worker(path)

    total = len(entries)
    counts = {worker: 0 for worker in WORKERS}
    for row in entries:
        counts[row["assigned_worker"]] += 1

    target = {worker: total // len(WORKERS) for worker in WORKERS}
    # Give surplus slots to the current largest owners, reducing migrations
    # when total is not a multiple of the number of workers.
    for worker in sorted(WORKERS, key=lambda w: (-counts[w], WORKERS.index(w)))[:total % len(WORKERS)]:
        target[worker] += 1

    for donor in sorted(WORKERS, key=lambda w: (-counts[w], WORKERS.index(w))):
        surplus = counts[donor] - target[donor]
        if surplus <= 0:
            continue
        owned = [row for row in entries if row["assigned_worker"] == donor]
        # Middle tasks are safest to transfer. Preserve both live work fronts.
        protected = {
            id(row)
            for row in owned[:protected_each_end] + (
                owned[-protected_each_end:] if protected_each_end else []
            )
        }
        candidates = [row for row in owned if id(row) not in protected]
        candidates += [row for row in owned if id(row) in protected]
        for row in candidates[:surplus]:
            recipient = min(
                (w for w in WORKERS if counts[w] < target[w]),
                key=lambda w: (counts[w] - target[w], WORKERS.index(w)),
            )
            row["assigned_worker"] = recipient
            counts[donor] -= 1
            counts[recipient] += 1


def is_survey_path(path: str) -> bool:
    return path.startswith("papers/survey/")


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def previous_queue_paths(repo_root: Path) -> set[str]:
    """Return current-version pending paths already admitted to the durable lane.

    A paper enters this lane because it was below the size trigger at some point.
    Once admitted, growing above 16KB must not make it disappear before a current
    semantic attestation and all deterministic checks pass.
    """
    target = repo_root.resolve() / QUEUE_PATH
    if not target.is_file():
        return set()
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        return set()
    if (
        payload.get("queue_kind") != "under_16kb_semantic_reaudit"
        or payload.get("queue_version") != REAUDIT_VERSION
    ):
        return set()
    entries = payload.get("entries")
    if not isinstance(entries, list):
        return set()
    paths: set[str] = set()
    for row in entries:
        if not isinstance(row, dict):
            continue
        value = str(row.get("path") or "").strip()
        if value.startswith("papers/"):
            paths.add(Path(value).as_posix())
    return paths


def reaudit_failures(audit: quality.PaperResult, path: str) -> list[str]:
    """Return the deterministic failures for the under-16KB semantic re-audit lane.

    The generic Research gate's explanation-floor messages are recomputed here so
    survey/review papers are not forced into an experimental-paper evaluation shape.
    Publication-integrity failures (frontmatter, UTF-8, >=70% Japanese baseline, ...)
    remain failures.  The re-audit lane then tightens Japanese prose to >=80%.
    """
    failures = [
        reason
        for reason in audit.failures
        if not str(reason).startswith("説明不足トリガー:")
    ]
    if audit.prose_chars < MIN_BODY_CHARS:
        failures.append(
            f"16KB未満再監査: 本文説明量 {audit.prose_chars} < {MIN_BODY_CHARS}"
        )
    if audit.method_chars < MIN_METHOD_CHARS:
        failures.append(
            f"16KB未満再監査: 手法説明量 {audit.method_chars} < {MIN_METHOD_CHARS}"
        )
    if not is_survey_path(path) and audit.evaluation_chars < MIN_EVALUATION_CHARS:
        failures.append(
            "16KB未満再監査: "
            f"評価説明量 {audit.evaluation_chars} < {MIN_EVALUATION_CHARS}"
        )
    if audit.japanese_ratio < MIN_JAPANESE_RATIO:
        failures.append(
            "16KB未満再監査: "
            f"日本語比率 {audit.japanese_ratio:.1%} < {MIN_JAPANESE_RATIO:.0%}"
        )
    return _dedupe(failures)


def semantic_attestation_present(meta: dict[str, Any]) -> bool:
    return (
        str(meta.get("under16kb_reaudit_version") or "").strip() == REAUDIT_VERSION
        and meta.get("under16kb_reaudit_passed") is True
    )


def completed(meta: dict[str, Any], audit: quality.PaperResult, path: str) -> bool:
    return semantic_attestation_present(meta) and not reaudit_failures(audit, path)


def audit_one(path: Path, repo_root: Path) -> tuple[quality.PaperResult, dict[str, Any]]:
    # Repository-wide audit keeps explanation floors as metrics; this queue applies
    # its own paper-type-aware floor below.
    args = argparse.Namespace(enforce_explanation_floor=False)
    audit = quality.audit_file(path, repo_root, args)
    meta = parse_frontmatter(path.read_text(encoding="utf-8", errors="strict"))
    return audit, meta


def build_queue(repo_root: Path, max_file_bytes: int = MAX_FILE_BYTES) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    entries: list[dict[str, Any]] = []
    previously_admitted = previous_queue_paths(repo_root)

    for path in quality.iter_papers(repo_root):
        raw = path.read_bytes()
        size = len(raw)
        rel = path.relative_to(repo_root).as_posix()
        if size >= max_file_bytes and rel not in previously_admitted:
            continue
        audit, meta = audit_one(path, repo_root)
        if completed(meta, audit, rel):
            continue

        failures = reaudit_failures(audit, rel)
        entries.append(
            {
                "path": rel,
                "canonical_id": meta.get("canonical_id"),
                "title": meta.get("title"),
                "file_bytes": size,
                "source_sha256": sha256_bytes(raw),
                "source_git_blob_sha": git_blob_sha(raw),
                "assigned_worker": assigned_worker(rel),
                "semantic_status": "pending",
                "mechanical_status": "FAIL" if failures else (
                    "WARN" if audit.warnings else "PASS"
                ),
                "japanese_ratio": round(float(audit.japanese_ratio), 6),
                "quality_metrics": {
                    "body_chars": audit.prose_chars,
                    "method_chars": audit.method_chars,
                    "evaluation_chars": audit.evaluation_chars,
                    "limitation_chars": audit.limitation_chars,
                },
                "mechanical_failures": failures,
                "warnings": list(audit.warnings),
            }
        )

    entries.sort(key=lambda row: (int(row["file_bytes"]), str(row["path"])))
    rebalance_workers(entries, previous_queue_assignments(repo_root))
    worker_counts = {
        worker: sum(1 for row in entries if row["assigned_worker"] == worker)
        for worker in WORKERS
    }
    return {
        "schema_version": 1,
        "queue_kind": "under_16kb_semantic_reaudit",
        "queue_version": REAUDIT_VERSION,
        "threshold_bytes_exclusive": max_file_bytes,
        "minimum_japanese_ratio": MIN_JAPANESE_RATIO,
        "count": len(entries),
        "worker_counts": worker_counts,
        "entries": entries,
    }


def write_queue(repo_root: Path, queue: dict[str, Any]) -> bool:
    target = repo_root.resolve() / QUEUE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    stable = dict(queue)
    old_stable: dict[str, Any] | None = None
    if target.exists():
        try:
            old = json.loads(target.read_text(encoding="utf-8"))
            old_stable = dict(old)
            old_stable.pop("generated_at", None)
        except (OSError, json.JSONDecodeError, TypeError):
            old_stable = None

    if old_stable == stable:
        return False

    payload = {"generated_at": now(), **queue}
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-file-bytes", type=int, default=MAX_FILE_BYTES)
    args = parser.parse_args()

    queue = build_queue(args.repo_root, args.max_file_bytes)
    if args.apply:
        changed = write_queue(args.repo_root, queue)
        print(
            json.dumps(
                {
                    "changed": changed,
                    "count": queue["count"],
                    "worker_counts": queue["worker_counts"],
                },
                ensure_ascii=False,
            )
        )
        return 0

    rendered = json.dumps({"generated_at": now(), **queue}, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
