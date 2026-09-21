#!/usr/bin/env python3
"""Apply the repository paper-quality criteria to one rendered artifact before publication."""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import audit_paper_quality as quality


def _default_args() -> argparse.Namespace:
    return argparse.Namespace(
        min_bytes=quality.DEFAULT_MIN_BYTES,
        min_prose_chars=quality.DEFAULT_MIN_PROSE_CHARS,
        min_paragraphs=quality.DEFAULT_MIN_PARAGRAPHS,
        min_method_paragraphs=quality.DEFAULT_MIN_METHOD_PARAGRAPHS,
        min_component_paragraphs=quality.DEFAULT_MIN_COMPONENT_PARAGRAPHS,
        min_japanese_ratio=quality.DEFAULT_MIN_JAPANESE_RATIO,
        warn_japanese_ratio=quality.DEFAULT_WARN_JAPANESE_RATIO,
    )


def validate_rendered_paper(repo_root: Path, paper_path: str, content: str) -> quality.PaperResult:
    """Validate one not-yet-published Markdown artifact with maintenance criteria.

    The candidate is written only to a temporary file under the repository so
    ``audit_file`` can reuse the exact maintenance implementation. The target
    paper is never touched here.
    """
    repo_root = Path(repo_root).resolve()
    tmp_root = repo_root / ".survey" / ".quality-gate-tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".md",
            prefix="candidate-",
            dir=tmp_root,
            delete=False,
        ) as fh:
            fh.write(content.rstrip() + "\n")
            tmp_path = Path(fh.name)
        result = quality.audit_file(tmp_path, repo_root, _default_args())
        result.path = paper_path
        if result.status == "FAIL":
            raise ValueError("paper quality gate failed: " + "; ".join(result.failures))
        return result
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        try:
            tmp_root.rmdir()
        except OSError:
            pass
