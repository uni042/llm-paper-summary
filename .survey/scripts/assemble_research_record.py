#!/usr/bin/env python3
"""Assemble workflow-v10 fixed structured research slots and render transient Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from japanese_style import (  # noqa: E402
    DEFAULT_MIN_JAPANESE_RATIO,
    PREFERRED_TERMS,
    TERM_PATTERNS,
    find_bare_english,
    japanese_ratio,
    record_prose_text,
)
from render_paper import render_paper  # noqa: E402

TRANSPORT_VERSION = 10
MAX_SLOT_BYTES = {
    "metadata": 8192,
    "problem_method": 16384,
    "evaluation": 12288,
    "results": 12288,
    "positioning": 8192,
}
FIXED_INBOX = ".survey/work-queue/submissions/chat-inbox.json"
LEGACY_PAYLOAD = ".survey/work-queue/payloads/chat-payload.md"
SLOT_NAMES = ["metadata", "problem_method", "evaluation", "results", "positioning"]
BANK_ROOTS = {
    "a": ".survey/work-queue/records/chat-record",
    "b": ".survey/work-queue/records/chat-record-b",
}


def slots_for_bank(bank: str) -> list[tuple[str, str]]:
    root = BANK_ROOTS[bank]
    return [(name, f"{root}/{name}.json") for name in SLOT_NAMES]


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validated_rel(path_text: str) -> str:
    p = PurePosixPath(path_text)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"path must be repository-relative without parent traversal: {path_text}")
    return p.as_posix()


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def prose_chars(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value.strip())
    if isinstance(value, list):
        total = 0
        for item in value:
            if isinstance(item, dict):
                total += prose_chars(item.get("description"))
                total += prose_chars(item.get("interpretation"))
                total += prose_chars(item.get("text"))
            else:
                total += prose_chars(item)
        return total
    if isinstance(value, dict):
        return sum(prose_chars(v) for v in value.values())
    return 0


def normalize_preferred_terms(value: Any, key: str | None = None) -> Any:
    """Normalize ordinary English prose terms before final validation/rendering.

    Transport slots remain immutable and blob-verified.  This operates only on the
    in-memory render record, so a mechanically fixable terminology miss does not
    strand an otherwise complete fallback payload.  Identifiers, URLs, titles,
    names, and source metadata are intentionally left untouched.
    """
    protected_keys = {
        "canonical_id", "arxiv_id", "doi", "openreview_id", "source", "sources",
        "code", "paper_path", "attempt_id", "job_id", "published", "title",
        "authors", "publication", "publication_type", "publication_status",
    }
    if key in protected_keys:
        return value
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            return value
        text = value
        for canonical, pattern in TERM_PATTERNS.items():
            preferred = PREFERRED_TERMS[canonical][0].split("／", 1)[0]
            text = pattern.sub(preferred, text)
        return text
    if isinstance(value, list):
        return [normalize_preferred_terms(item, key=key) for item in value]
    if isinstance(value, dict):
        return {k: normalize_preferred_terms(v, key=k) for k, v in value.items()}
    return value


def validate_record(record: dict[str, Any]) -> None:
    meta = record.get("metadata") or {}
    pm = record.get("problem_method") or {}
    ev = record.get("evaluation") or {}
    rs = record.get("results") or {}
    pos = record.get("positioning") or {}

    for key in ("canonical_id", "title", "summary", "source", "authors", "publication", "topics", "implementation"):
        if not nonempty(meta.get(key)):
            raise ValueError(f"metadata.{key} is required")
    if prose_chars(meta.get("summary")) < 180:
        raise ValueError("metadata.summary must be explanatory, not a one-line abstract")
    if not nonempty(meta.get("publication_type")):
        raise ValueError("metadata.publication_type is required")
    if not nonempty(meta.get("hardware_evaluation")):
        raise ValueError("metadata.hardware_evaluation is required")
    if not nonempty(meta.get("quality_effect")):
        raise ValueError("metadata.quality_effect is required")

    for key in ("problem", "novelty", "method_overview", "components", "system_design"):
        if not nonempty(pm.get(key)):
            raise ValueError(f"problem_method.{key} is required")
    if prose_chars(pm.get("problem")) < 250:
        raise ValueError("problem_method.problem must explain the bottleneck and why prior approaches are insufficient")
    if prose_chars(pm.get("novelty")) < 180:
        raise ValueError("problem_method.novelty must explain the paper-specific idea")
    if prose_chars(pm.get("method_overview")) < 500:
        raise ValueError("problem_method.method_overview must explain the end-to-end mechanism")
    components = pm.get("components")
    if not isinstance(components, list) or len(components) < 2:
        raise ValueError("problem_method.components requires at least two major mechanisms")
    for index, item in enumerate(components):
        if not isinstance(item, dict) or not nonempty(item.get("name")) or not nonempty(item.get("description")):
            raise ValueError(f"problem_method.components[{index}] requires name and description")
        if prose_chars(item.get("description")) < 240:
            raise ValueError(f"problem_method.components[{index}].description is too short")

    if not (nonempty(ev.get("hardware")) or nonempty(ev.get("software")) or nonempty(ev.get("methodology"))):
        raise ValueError("evaluation requires hardware/software/methodology evidence")
    if not nonempty(ev.get("scope")):
        raise ValueError("evaluation.scope is required to distinguish real-hardware/simulation and generalization limits")

    key_results = rs.get("key_results")
    if not isinstance(key_results, list) or not key_results:
        raise ValueError("results.key_results requires at least one quantitative result")
    if not nonempty(rs.get("overview")) or prose_chars(rs.get("overview")) < 180:
        raise ValueError("results.overview must explain the main result and its practical meaning")
    for index, item in enumerate(key_results):
        if not isinstance(item, dict):
            raise ValueError(f"results.key_results[{index}] must be an object")
        missing = [k for k in ("metric", "value", "baseline", "condition", "interpretation") if not nonempty(item.get(k))]
        if missing:
            raise ValueError(f"results.key_results[{index}] missing: " + ", ".join(missing))
    if not nonempty(rs.get("negative_results")):
        raise ValueError("results.negative_results is required; record degradation and boundary conditions")
    if not nonempty(rs.get("interpretation")):
        raise ValueError("results.interpretation is required; explain why gains change across conditions")
    if not nonempty(rs.get("quality_impact")):
        raise ValueError("results.quality_impact is required; distinguish lossless from approximate methods")

    for key in ("limitations", "differences", "implementation_status", "research_positioning"):
        if not nonempty(pos.get(key)):
            raise ValueError(f"positioning.{key} is required")

    prose = record_prose_text(record)
    ratio, jp_chars, latin_chars = japanese_ratio(prose)
    if ratio < DEFAULT_MIN_JAPANESE_RATIO:
        raise ValueError(
            f"Japanese-first prose ratio is too low: {ratio:.1%} "
            f"< {DEFAULT_MIN_JAPANESE_RATIO:.0%} (Japanese={jp_chars}, Latin={latin_chars})"
        )
    bare = find_bare_english(prose)
    if bare:
        preview = ", ".join(
            f"{hit.term}->{hit.preferred} x{hit.count}" for hit in bare[:12]
        )
        raise ValueError(
            "Japanese-first terminology violation; replace ordinary English prose "
            f"with Japanese/katakana or put the formal English name only in the first parentheses: {preview}"
        )


def assemble(repo_root: Path) -> bool:
    inbox_path = repo_root / FIXED_INBOX
    inbox = read_json(inbox_path)
    refs = inbox.get("record_slots")
    if refs is None:
        return False
    if inbox.get("payload_chunks") is not None or inbox.get("payload_path") is not None:
        raise ValueError("record_slots cannot be combined with legacy payload fields")
    bank = str(inbox.get("record_bank") or "a").lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be a registered bank")
    slots = slots_for_bank(bank)
    if not isinstance(refs, list) or len(refs) != len(slots):
        raise ValueError(f"record_slots must contain exactly {len(slots)} entries")

    attempt_id = inbox.get("attempt_id")
    job_id = inbox.get("job_id")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ValueError("attempt_id is required")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError("job_id is required")

    record: dict[str, Any] = {}
    total_bytes = 0
    for index, ((slot_name, expected_path), ref) in enumerate(zip(slots, refs), start=1):
        if not isinstance(ref, dict):
            raise ValueError(f"record_slots[{index - 1}] must be an object")
        if ref.get("slot") != slot_name:
            raise ValueError(f"record_slots[{index - 1}] must declare slot={slot_name}")
        path_text = validated_rel(str(ref.get("path") or ""))
        if path_text != expected_path:
            raise ValueError(f"slot {slot_name} must use fixed path {expected_path}")
        expected_sha = ref.get("blob_sha")
        if not isinstance(expected_sha, str) or not expected_sha:
            raise ValueError(f"slot {slot_name} requires blob_sha")

        path = repo_root / path_text
        if not path.is_file():
            raise ValueError(f"missing record slot: {path_text}")
        raw = path.read_bytes()
        limit = MAX_SLOT_BYTES[slot_name]
        if len(raw) > limit:
            raise ValueError(f"record slot too large: {path_text} ({len(raw)} bytes > {limit})")
        if git_blob_sha(raw) != expected_sha:
            raise ValueError(f"record slot blob mismatch: {path_text}")

        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"{path_text} must contain an object")
        if int(payload.get("transport_version") or 0) != TRANSPORT_VERSION:
            raise ValueError(f"{path_text} transport_version must be {TRANSPORT_VERSION}")
        if payload.get("slot") != slot_name:
            raise ValueError(f"{path_text} slot mismatch")
        if payload.get("attempt_id") != attempt_id or payload.get("job_id") != job_id:
            raise ValueError(f"{path_text} attempt_id/job_id mismatch")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError(f"{path_text} data must be an object")
        record[slot_name] = data
        total_bytes += len(raw)

    record = normalize_preferred_terms(record)
    validate_record(record)
    markdown = render_paper(record)
    (repo_root / LEGACY_PAYLOAD).write_text(markdown, encoding="utf-8")

    local_inbox = dict(inbox)
    local_inbox.pop("record_slots", None)
    local_inbox["payload_path"] = LEGACY_PAYLOAD
    local_inbox["transport_version"] = TRANSPORT_VERSION
    inbox_path.write_text(json.dumps(local_inbox, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "assembled": True,
        "transport_version": TRANSPORT_VERSION,
        "bank": bank,
        "slots": len(slots),
        "structured_bytes": total_bytes,
        "rendered_bytes": len(markdown.encode("utf-8")),
    }, ensure_ascii=False))
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()
    assemble(Path(args.repo_root).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
