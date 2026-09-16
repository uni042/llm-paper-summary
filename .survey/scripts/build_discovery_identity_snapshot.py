#!/usr/bin/env python3
"""Build compact Discovery duplicate-precheck shards from the final identity gate.

The Discovery worker cannot rely on GitHub code search for duplicate detection because
that search index may omit already tracked papers. This script deliberately reuses
queue_worker.existing_candidate_keys(), the same normalized identity-token set consumed
by the final Discovery materialization gate, and publishes it as small deterministic
files that Scheduled Chat can fetch exactly.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import queue_worker


README = """# Discovery identity precheck

This directory is a derived lookup surface for Discovery workers. It is generated from
`queue_worker.existing_candidate_keys()`, so it contains the same identity tokens as the final duplicate gate.

Before accepting a candidate, check the appropriate shard using the candidate's strongest
available identity in this order: canonical/arXiv ID, DOI, OpenReview ID, normalized URL,
then normalized title. Refresh the latest default-branch HEAD and repeat this check
immediately before writing an immutable Discovery submission.

Do not use GitHub code search as duplicate authority. Code search may be used only for
navigation; a code-search miss does not mean a paper is new. A candidate whose normalized
identity token is present in a shard is already represented or pending and must be filtered
before submission.

Shard naming:
- `arxiv-YYMM.txt`: normalized arXiv identity tokens for one arXiv month prefix.
- `doi.txt`, `openreview.txt`, `id-other.txt`: other stable identifier tokens.
- `url-<host>.txt`: normalized URL tokens by host.
- `title-<bucket>.txt`: normalized title tokens by first ASCII letter/digit bucket.
- `_manifest.json`: source contract, source commit, token count, and per-shard counts.

Each `.txt` file contains one exact normalized identity token per line. Do not infer
novelty from a missing GitHub search result; check the appropriate shard before accepting a candidate.
"""


def configure_queue_worker(root: Path) -> None:
    root = root.resolve()
    queue = root / "work-queue"
    queue_worker.ROOT = root
    queue_worker.QUEUE = queue
    queue_worker.JOBS = queue / "jobs"
    queue_worker.SUBMISSIONS = queue / "submissions"
    queue_worker.RESULTS = queue / "results"
    queue_worker.STATE = queue / "state.json"
    queue_worker.ARCHIVE = queue / "archive"
    queue_worker.DISCOVERY_STATE = queue / "discovery-state.json"


def _safe_component(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "other"


def shard_name(token: str) -> str:
    if token.startswith("id:arXiv:"):
        ident = token[len("id:arXiv:"):]
        match = re.match(r"(\d{4})\.\d+", ident)
        return f"arxiv-{match.group(1) if match else 'other'}.txt"
    if token.startswith("id:DOI:"):
        return "doi.txt"
    if token.startswith("id:OpenReview:"):
        return "openreview.txt"
    if token.startswith("id:"):
        return "id-other.txt"
    if token.startswith("url:"):
        try:
            host = urlparse(token[len("url:"):]).netloc
        except Exception:
            host = ""
        return f"url-{_safe_component(host)}.txt"
    if token.startswith("title:"):
        title = token[len("title:"):].lstrip()
        first = title[:1].casefold()
        if first.isascii() and first.isalpha():
            bucket = first
        elif first.isascii() and first.isdigit():
            bucket = "0-9"
        else:
            bucket = "other"
        return f"title-{bucket}.txt"
    return "other.txt"


def _write_text_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def build_snapshot(root: Path, output: Path | None = None, source_commit: str | None = None) -> bool:
    root = root.resolve()
    configure_queue_worker(root)
    output = (output or root / "work-queue" / "discovery-identities").resolve()
    output.mkdir(parents=True, exist_ok=True)

    tokens = sorted(queue_worker.existing_candidate_keys())
    shards: dict[str, list[str]] = {}
    for token in tokens:
        shards.setdefault(shard_name(token), []).append(token)

    desired_names = set(shards) | {"_manifest.json", "_README.md"}
    changed = False
    for path in output.iterdir():
        if path.is_file() and path.name not in desired_names:
            path.unlink()
            changed = True

    for name, shard_tokens in sorted(shards.items()):
        text = "".join(f"{token}\n" for token in shard_tokens)
        changed = _write_text_if_changed(output / name, text) or changed

    manifest = {
        "schema_version": 1,
        "source": "queue_worker.existing_candidate_keys",
        "source_commit": source_commit,
        "token_count": len(tokens),
        "shards": {name: len(values) for name, values in sorted(shards.items())},
        "lookup_order": ["stable_identifier", "normalized_url", "normalized_title"],
        "code_search_is_authority": False,
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    changed = _write_text_if_changed(output / "_manifest.json", manifest_text) or changed
    changed = _write_text_if_changed(output / "_README.md", README) or changed
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    changed = build_snapshot(args.root, args.output, source_commit=args.source_commit)
    print(json.dumps({"changed": changed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
