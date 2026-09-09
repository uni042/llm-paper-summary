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
    return len(str(value))


def paragraph_count(value: Any) -> int:
    if not isinstance(value, str):
        return 0
    return len([p for p in re.split(r"\n\s*\n", value.strip()) if p.strip()])


def validate_record(record: dict[str, Any]) -> None:
    """Reject completed artifacts that are structurally complete but below paper.md quality."""
    meta = record.get("metadata") or {}
    pm = record.get("problem_method") or {}
    ev = record.get("evaluation") or {}
    rs = record.get("results") or {}
    pos = record.get("positioning") or {}

    required_meta = ("canonical_id", "title", "summary", "source")
    missing_meta = [k for k in required_meta if not nonempty(meta.get(k))]
    if missing_meta:
        raise ValueError("metadata missing required fields: " + ", ".join(missing_meta))
    if not nonempty(meta.get("sources")):
        raise ValueError("metadata.sources requires at least one primary-source URL")

    for key in ("problem", "novelty"):
        if not nonempty(pm.get(key)):
            raise ValueError(f"problem_method.{key} is required")
    overview = pm.get("method_overview")
    components = pm.get("components")
    system_design = pm.get("system_design")
    if not nonempty(overview):
        raise ValueError("problem_method.method_overview is required for reader-first explanation")
    if prose_chars(overview) < 300:
        raise ValueError("problem_method.method_overview is too terse; explain the processing order and data flow")
    if not isinstance(components, list) or not components:
        raise ValueError("problem_method.components is required")
    if not nonempty(system_design) or prose_chars(system_design) < 250:
        raise ValueError("problem_method.system_design must explain the end-to-end data/control flow")

    complex_paper = len(components) >= 3
    for index, comp in enumerate(components):
        if not isinstance(comp, dict) or not nonempty(comp.get("name")) or not nonempty(comp.get("description")):
            raise ValueError(f"problem_method.components[{index}] requires name and description")
        desc = comp.get("description")
        if complex_paper and prose_chars(desc) < 220:
            raise ValueError(f"problem_method.components[{index}] is too terse for a multi-stage system paper")
        if complex_paper and paragraph_count(desc) < 2:
            raise ValueError(f"problem_method.components[{index}] should use at least two explanatory paragraphs")

    method_chars = prose_chars(overview) + prose_chars(components) + prose_chars(system_design)
    method_floor = 1800 if complex_paper else 1000
    if method_chars < method_floor:
        raise ValueError(
            "problem_method is too terse for repository publication; explain component roles, "
            "data/control flow, why each mechanism helps, and failure/boundary conditions"
        )

    if not nonempty(ev.get("baselines")):
        raise ValueError("evaluation.baselines is required")
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
        raise ValueError("record_bank must be a or b")
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
