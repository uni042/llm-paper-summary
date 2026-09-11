#!/usr/bin/env python3
"""Repository-wide structural consistency checks for the current v10 layout."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

REQUIRED_V10_PATHS = (
    ".survey/docs/survey-workflow/worker-router.md",
    ".survey/docs/survey-workflow/queue-v10.md",
    ".survey/docs/survey-workflow/continuation-policy.json",
    ".survey/docs/survey-workflow/fallback-routing.md",
    ".survey/docs/survey-workflow/backlog-resilience.md",
    ".survey/docs/survey-workflow/suggestion-box.md",
    ".survey/survey-state/paper-identity-index.json",
    ".survey/survey-state/frozen-training.json",
    ".survey/work-queue/next-jobs.json",
    ".survey/work-queue/state.json",
    ".survey/work-queue/maintenance-cycle.json",
    ".survey/work-queue/discovery-state.json",
    ".survey/work-queue/run-ledger.json",
    ".survey/work-queue/records/bank-registry.json",
    ".survey/update-worker/update-inbox.json",
    ".survey/update-worker/update-payload.json",
)

REQUIRED_PAPER_METADATA = (
    "canonical_id", "title", "summary", "authors", "published", "publication",
    "publication_type", "publication_status", "source", "sources", "implementation",
    "code", "last_checked", "last_audited", "audit_version",
)


def raw_path_bytes(path):
    if path.is_symlink():
        return os.readlink(path).encode("utf-8")
    return path.read_bytes()


def blob_hash(path):
    data = raw_path_bytes(path)
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def local_files(root):
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if (p.is_symlink() or p.is_file()) and not any(x in (".git", "__pycache__", ".venv") for x in p.relative_to(root).parts) and not p.name.endswith((".pyc", ".tmp"))}


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1]) or {}, parts[2]


def check(root, inventory):
    root = root.resolve()
    files = local_files(root)
    findings = []
    external = set()
    def issue(code, path, detail):
        findings.append({"code": code, "path": path, "detail": detail})
    expected = {x["path"]: x["sha"] for x in inventory.get("files", [])}
    if not inventory.get("source_commit") or not expected:
        issue("inventory_missing", "", "A complete tracked-file inventory is required")
    for path in expected:
        if path not in files:
            issue("missing_file", path, "Present in inventory but unavailable locally")
    for path in REQUIRED_V10_PATHS:
        if path not in files:
            issue("required_v10_path_missing", path, "Required by the current workflow v10")
    json_objects = {}
    canonical_ids = {}
    scanned = []
    for name, path in sorted(files.items()):
        scanned.append(name)
        if path.is_symlink():
            try:
                destination = path.resolve(strict=True)
                if not destination.is_relative_to(root):
                    issue("symlink_outside_repository", name, os.readlink(path))
            except (OSError, RuntimeError):
                issue("broken_symlink", name, os.readlink(path))
            continue
        if path.suffix not in (".md", ".json", ".yaml", ".yml"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            issue("invalid_encoding", name, "Expected UTF-8 text")
            continue
        if path.suffix == ".json":
            try:
                json_objects[name] = json.loads(text)
            except ValueError as error:
                issue("invalid_json", name, str(error))
        if path.suffix in (".yaml", ".yml") or (path.suffix == ".md" and text.startswith("---\n")):
            try:
                yaml.safe_load(text if path.suffix != ".md" else text.split("---", 2)[1])
            except (ValueError, yaml.YAMLError) as error:
                issue("invalid_yaml", name, str(error))
        if path.suffix != ".md":
            continue
        prose = re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)
        links = re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", prose)
        links += re.findall(r"^\s*\[[^\]]+\]:\s*(\S+)", prose, re.M)
        for link in links:
            target = link.strip("<>")
            try:
                parsed = urlsplit(target)
            except ValueError:
                issue("invalid_link", name, target)
                continue
            if parsed.scheme or parsed.netloc:
                if parsed.scheme in ("http", "https"):
                    external.add(target)
                continue
            if not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                issue("link_outside_repository", name, target)
            elif not destination.exists():
                issue("broken_local_link", name, target)
        parts = Path(name).parts
        is_identity_paper = len(parts) == 4 and parts[0] == "papers" and parts[1] in ("inference", "survey") and path.name != "README.md"
        if is_identity_paper:
            meta, body = frontmatter(path)
            if body.lstrip().startswith("# Moved") or text.lstrip().startswith("# Moved"):
                continue
            cid = meta.get("canonical_id")
            if not cid:
                issue("paper_missing_canonical_id", name, "Active inference paper requires canonical_id")
            elif cid in canonical_ids:
                issue("duplicate_canonical_id", name, f"Also used by {canonical_ids[cid]}")
            else:
                canonical_ids[cid] = name
            for key in REQUIRED_PAPER_METADATA:
                if key not in meta:
                    issue("paper_missing_metadata", name, key)
            authors = meta.get("authors")
            if "authors" in meta and (not isinstance(authors, list) or not authors):
                issue("paper_invalid_metadata", name, "authors must be a non-empty list")
            sources = meta.get("sources")
            if "sources" in meta and (not isinstance(sources, list) or not sources):
                issue("paper_invalid_metadata", name, "sources must be a non-empty list")
            published = meta.get("published")
            if "published" in meta and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(published)):
                issue("paper_invalid_metadata", name, "published must use YYYY-MM-DD")
            if meta.get("arxiv_id"):
                categories = meta.get("arxiv_categories")
                if not isinstance(categories, dict) or not categories.get("primary"):
                    issue("paper_missing_metadata", name, "arxiv_categories.primary")
                elif not isinstance(categories.get("cross_list", []), list):
                    issue("paper_invalid_metadata", name, "arxiv_categories.cross_list must be a list")
    frozen_name = ".survey/survey-state/frozen-training.json"
    frozen = json_objects.get(frozen_name, {})
    if not isinstance(frozen, dict) or not frozen.get("files"):
        issue("frozen_baseline_missing", frozen_name, "Cannot verify training freeze without a baseline")
    else:
        actual_training = {n for n in files if n.startswith("papers/training/")}
        baseline = frozen["files"]
        for name, sha in baseline.items():
            if name not in files:
                issue("frozen_training_missing", name, "Baseline file is missing")
            elif blob_hash(files[name]) != sha:
                issue("frozen_training_changed", name, "Read-only baseline differs; do not rewrite automatically")
        for name in actual_training - set(baseline):
            issue("frozen_training_added", name, "Unreviewed addition in frozen training area")
    maintenance_name = ".survey/work-queue/maintenance-cycle.json"
    maintenance = json_objects.get(maintenance_name, {})
    if isinstance(maintenance, dict):
        cadence = maintenance.get("cadence_runs")
        count = maintenance.get("runs_since_maintenance")
        if cadence != 24:
            issue("maintenance_cadence", maintenance_name, f"Expected cadence_runs=24, got {cadence!r}")
        if not isinstance(count, int) or count < 0 or count >= 24:
            issue("maintenance_counter", maintenance_name, f"Invalid runs_since_maintenance={count!r}")
    return {
        "schema_version": 3,
        "source_commit": inventory.get("source_commit"),
        "checked_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "status": "passed" if not findings else "issues_found",
        "scope": "repository-wide structural consistency",
        "inventory_file_count": len(expected),
        "checked_file_count": len(scanned),
        "missing_files": sorted(set(expected) - set(files)),
        "working_changes": sorted(n for n, p in files.items() if n not in expected or blob_hash(p) != expected[n]),
        "checks": ["inventory_coverage", "required_v10_paths", "all_json_yaml", "markdown_file_links", "symlink_targets", "frozen_training", "paper_metadata_and_identity", "maintenance_cycle"],
        "not_checked": ["External URL reachability", "Fragment anchors", "Scientific validity / full paper audits", "Scheduler startup guarantees", "Runtime execution of arbitrary repository code"],
        "external_url_count": len(external),
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.root, json.loads(args.inventory.read_text(encoding="utf-8")))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checked_files": result["checked_file_count"], "findings": len(result["findings"])}))
    raise SystemExit(0 if result["status"] == "passed" else 1)


if __name__ == "__main__":
    main()
