#!/usr/bin/env python3
"""Apply publication-integrity checks to one rendered paper before publication.

Semantic quality is owned by the reading worker's self-review.  This gate is
intentionally limited to checks that do not require rereading the paper.
"""
from __future__ import annotations

import argparse
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


def inspect_rendered_paper(repo_root: Path, paper_path: str, content: str) -> quality.PaperResult:
    repo_root = Path(repo_root).resolve()
    tmp_root = repo_root / ".survey" / ".quality-gate-tmp"
    tmp_path = tmp_root / paper_path
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        tmp_path.write_text(content.rstrip() + "\n", encoding="utf-8")
        return quality.audit_file(tmp_path, tmp_root, _default_args())
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
