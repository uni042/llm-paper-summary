#!/usr/bin/env python3
"""Repository-wide structural checks for workflow v8."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
STATE = REPO / ".survey/survey-state"


def git_blob_hash_bytes(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def tracked_local(root: Path):
    out = {}
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(x in (".git", "__pycache__", ".venv") for x in rel.parts):
            continue
        if p.is_symlink():
            out[rel.as_posix()] = (p, os.readlink(p).encode("utf-8"))
        elif p.is_file() and not p.name.endswith((".pyc", ".tmp")):
            out[rel.as_posix()] = (p, p.read_bytes())
    return out


def check(root: Path, inventory: dict):
    root = root.resolve()
    local = tracked_local(root)
    expected = {x["path"]: x["sha"] for x in inventory.get("files", [])}
    findings = []
    def issue(code, path, detail): findings.append({"code": code, "path": path, "detail": detail})

    if not inventory.get("source_commit") or not expected:
        issue("inventory_missing", "", "Complete tracked-file inventory and source_commit are required")
    for path, sha in expected.items():
        if path not in local:
            issue("missing_file", path, "Tracked file unavailable locally")
        elif git_blob_hash_bytes(local[path][1]) != sha:
            issue("working_change", path, "Local content differs from fixed inventory")

    json_objects = {}
    for name, (path, raw) in sorted(local.items()):
        if path.is_symlink():
            continue
        if path.suffix == ".json":
            try: json_objects[name] = json.loads(raw.decode("utf-8"))
            except Exception as exc: issue("invalid_json", name, str(exc))
        if path.suffix != ".md":
            continue
        try: text = raw.decode("utf-8")
        except UnicodeError:
            issue("invalid_encoding", name, "Expected UTF-8")
            continue
        prose = re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)
        links = re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", prose)
        for link in links:
            target = link.strip("<>")
            try: parsed = urlsplit(target)
            except ValueError:
                issue("invalid_link", name, target); continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root):
                issue("link_outside_repository", name, target)
            elif not dest.exists():
                issue("broken_local_link", name, target)

    layout = json_objects.get(".survey/survey-state/state-layout.json", {})
    for key, value in layout.get("paths", {}).items():
        if not (root / value).exists():
            issue("state_path_missing", ".survey/survey-state/state-layout.json", f"{key}: {value}")

    frozen = json_objects.get(".survey/survey-state/frozen-training.json", {})
    for name, sha in frozen.get("files", {}).items():
        p = root / name
        if not p.exists() or git_blob_hash_bytes(p.read_bytes()) != sha:
            issue("frozen_training_changed", name, "Frozen training baseline differs")

    validator = root / ".survey/scripts/survey_v8.py"
    try:
        proc = subprocess.run(["python", str(validator), "validate"], cwd=root, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        if proc.returncode != 0:
            issue("survey_v8_validate_failed", str(validator.relative_to(root)), proc.stderr[-2000:] or proc.stdout[-2000:])
    except Exception as exc:
        issue("survey_v8_validate_unavailable", str(validator.relative_to(root)), str(exc))

    missing = sorted(set(expected) - set(local))
    return {
        "schema_version": 1,
        "workflow_version": 8,
        "source_commit": inventory.get("source_commit"),
        "status": "passed" if not findings else "issues_found",
        "inventory_file_count": len(expected),
        "checked_file_count": len(local),
        "missing_files": missing,
        "findings": findings,
        "not_checked": ["External URL reachability", "Fragment anchors", "Scientific validity/full paper audit", "Scheduler startup guarantees"]
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=REPO)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    result = check(a.root, json.loads(a.inventory.read_text(encoding="utf-8")))
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "findings": len(result["findings"])}))
    raise SystemExit(0 if result["status"] == "passed" else 1)

if __name__ == "__main__": main()
