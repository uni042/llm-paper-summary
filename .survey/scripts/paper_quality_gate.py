#!/usr/bin/env python3
"""Apply publication-integrity checks to one rendered paper before publication.

In addition to the existing language/integrity checks, this gate rejects obvious
cross-paper boilerplate reuse: long prose paragraphs copied across multiple
Research summaries.  It intentionally avoids trying to replace semantic review.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import audit_paper_quality as quality


def _default_args() -> argparse.Namespace:
    """Compatibility namespace for callers.

    Only the Japanese-ratio thresholds are active quality thresholds.  The
    retired quantity/depth thresholds are neutral zeros.
    """
    return argparse.Namespace(
        min_bytes=quality.DEFAULT_MIN_BYTES,
        min_prose_chars=quality.DEFAULT_MIN_PROSE_CHARS,
        min_paragraphs=quality.DEFAULT_MIN_PARAGRAPHS,
        min_method_paragraphs=quality.DEFAULT_MIN_METHOD_PARAGRAPHS,
        min_component_paragraphs=quality.DEFAULT_MIN_COMPONENT_PARAGRAPHS,
        min_japanese_ratio=quality.DEFAULT_MIN_JAPANESE_RATIO,
        warn_japanese_ratio=quality.DEFAULT_WARN_JAPANESE_RATIO,
    )


REUSE_MIN_PARAGRAPH_CHARS = 180
REUSE_MIN_SHARED_CHARS = 500
REUSE_MIN_SHARED_RATIO = 0.15
REUSE_MIN_PARAGRAPHS = 2


def _normalize_prose_paragraphs(text: str) -> list[str]:
    """Return long prose paragraphs suitable for cross-paper reuse checks."""
    lines = text.splitlines()
    body, _ = quality.strip_frontmatter(lines)
    paragraphs: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if not current:
            return
        raw = " ".join(part.strip() for part in current if part.strip())
        current.clear()
        normalized = re.sub(r"\\s+", " ", raw).strip()
        if len(normalized) >= REUSE_MIN_PARAGRAPH_CHARS:
            paragraphs.append(normalized)

    in_fence = False
    for line in body:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            flush()
            continue
        if (
            stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("- ")
            or stripped.startswith("* ")
            or stripped.startswith("> ")
        ):
            flush()
            continue
        current.append(stripped)
    flush()
    return paragraphs


def _reuse_search_paths(repo_root: Path, paper_path: str) -> list[Path]:
    roots = [
        repo_root / "papers/inference",
        repo_root / "papers/training",
        repo_root / "papers/survey",
    ]
    paths: list[Path] = []
    for root in roots:
        if root.is_dir():
            paths.extend(root.rglob("*.md"))

    if paper_path.startswith(".survey/import-inbox/pending/research/"):
        pending = repo_root / ".survey/import-inbox/pending/research"
        if pending.is_dir():
            paths.extend(pending.glob("*.md"))
    return paths


def _boilerplate_reuse_failures(repo_root: Path, paper_path: str, content: str) -> list[str]:
    candidate = _normalize_prose_paragraphs(content)
    if not candidate:
        return []

    candidate_set = set(candidate)
    total_chars = sum(len(p) for p in candidate)
    current = (repo_root / paper_path).resolve()
    shared_by_source: dict[str, list[str]] = {}

    for other in _reuse_search_paths(repo_root, paper_path):
        try:
            if other.resolve() == current:
                continue
            rel = other.relative_to(repo_root).as_posix()
            if other.name.casefold() in {"readme.md", "comparison.md"}:
                continue
            other_text = other.read_text(encoding="utf-8", errors="strict")
            if quality.is_moved_stub(other_text.splitlines()):
                continue
        except (OSError, UnicodeError, ValueError):
            continue
        overlap = candidate_set.intersection(_normalize_prose_paragraphs(other_text))
        if overlap:
            shared_by_source[rel] = sorted(overlap, key=len, reverse=True)

    failures: list[str] = []
    for source, shared in shared_by_source.items():
        shared_chars = sum(len(p) for p in shared)
        ratio = shared_chars / max(total_chars, 1)
        if (
            len(shared) >= REUSE_MIN_PARAGRAPHS
            and shared_chars >= REUSE_MIN_SHARED_CHARS
            and ratio >= REUSE_MIN_SHARED_RATIO
        ):
            failures.append(
                "長文定型文の再利用を検出: "
                f"{source} と {len(shared)} 段落 / {shared_chars}文字 "
                f"({ratio:.1%}) が完全一致"
            )
    return failures


def inspect_rendered_paper(repo_root: Path, paper_path: str, content: str) -> quality.PaperResult:
    repo_root = Path(repo_root).resolve()
    tmp_root = repo_root / ".survey" / ".quality-gate-tmp"
    tmp_path = tmp_root / paper_path
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        tmp_path.write_text(content.rstrip() + "\n", encoding="utf-8")
        result = quality.audit_file(tmp_path, tmp_root, _default_args())
        reuse_failures = _boilerplate_reuse_failures(repo_root, paper_path, content)
        if reuse_failures:
            result.failures.extend(reuse_failures)
            result.status = "FAIL"
        return result
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        finally:
            # Remove only directories created by this compatibility gate.
            parent = tmp_path.parent
            while parent != tmp_root.parent and parent.exists():
                try:
                    parent.rmdir()
                except OSError:
                    break
                if parent == tmp_root:
                    break
                parent = parent.parent


def validate_rendered_paper(repo_root: Path, paper_path: str, content: str) -> quality.PaperResult:
    result = inspect_rendered_paper(repo_root, paper_path, content)
    if result.status == "FAIL":
        raise ValueError("paper quality gate failed (publication integrity/Japanese ratio): " + "; ".join(result.failures))
    return result
