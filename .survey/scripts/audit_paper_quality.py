#!/usr/bin/env python3
"""Repository-wide publication-integrity audit for paper Markdown.

Semantic paper quality belongs to the reading worker's self-review.
This module intentionally checks only properties that can be verified
without rereading the paper.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from japanese_style import JP_RE, LATIN_RE, clean_for_language_ratio

MOVED_HEADING_RE = re.compile(r"^#\s+Moved(?:\s|$)", re.I)
FENCE_RE = re.compile(r"^\s*\x60\x60\x60")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HTML_TAG_RE = re.compile(r"<[^>]+>")
EXCLUDED_LANGUAGE_SECTIONS = {
    "書誌情報", "一次資料", "参考文献", "References", "更新履歴", "監査メモ"
}
# Compatibility alias for callers/tests that previously referenced this name.
EXCLUDED_SECTIONS = EXCLUDED_LANGUAGE_SECTIONS

# Retired v10 thresholds are preserved under .survey/legacy/quality-v10/.
# They remain defined as neutral compatibility values for old callers only.
DEFAULT_MIN_BYTES = 0
DEFAULT_MIN_PROSE_CHARS = 0
DEFAULT_MIN_PARAGRAPHS = 0
DEFAULT_MIN_METHOD_PARAGRAPHS = 0
DEFAULT_MIN_COMPONENT_PARAGRAPHS = 0
DEFAULT_MIN_JAPANESE_RATIO = 0.70
DEFAULT_WARN_JAPANESE_RATIO = 0.80
STRUCTURED_METHOD_MIN_PROSE_CHARS = 0
STRUCTURED_METHOD_MIN_PARAGRAPHS = 0


@dataclass
class TermHit:
    term: str
    preferred: str
    count: int
    lines: list[int] = field(default_factory=list)


@dataclass
class PaperResult:
    # Historical fields stay in the payload for compatibility, but retired
    # semantic measurements are neutral and never determine PASS/FAIL.
    path: str
    status: str
    file_bytes: int
    prose_chars: int = 0
    paragraphs: int = 0
    method_paragraphs: int = 0
    method_components: int = 0
    method_detection: str = "not-evaluated"
    japanese_ratio: float = 1.0
    japanese_chars: int = 0
    latin_chars: int = 0
    bare_english_terms: list[TermHit] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def strip_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    if not lines or lines[0].strip() != "---":
        return lines, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[idx + 1 :], idx + 1
    return lines, 0


def is_moved_stub(raw_lines: list[str]) -> bool:
    body, _ = strip_frontmatter(raw_lines)
    for line in body:
        stripped = line.strip()
        if stripped:
            return bool(MOVED_HEADING_RE.match(stripped))
    return False


def is_paper_summary(path: Path) -> bool:
    if path.name.casefold() in {"readme.md", "comparison.md"}:
        return False
    try:
        raw_lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    except UnicodeError:
        return True
    return not is_moved_stub(raw_lines)


def _frontmatter(text: str) -> tuple[dict, list[str]]:
    failures: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["YAML前付けがない"]
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}, ["YAML前付けの終端がない"]
    try:
        value = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return {}, [f"YAML前付けを解析できない: {exc}"]
    if not isinstance(value, dict):
        failures.append("YAML前付けはmappingでなければならない")
        return {}, failures
    return value, failures


def _balanced_fences(text: str) -> bool:
    return sum(1 for line in text.splitlines() if FENCE_RE.match(line)) % 2 == 0



def _normalize_heading(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    return text.strip()


def _language_prose(text: str) -> str:
    """Extract prose for Japanese-ratio measurement without metadata/source noise."""
    lines, _ = strip_frontmatter(text.splitlines())
    parts: list[str] = []
    in_fence = False
    excluded = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        hm = HEADING_RE.match(line)
        if hm:
            if len(hm.group(1)) == 2:
                title = _normalize_heading(hm.group(2))
                excluded = any(
                    title == name or title.startswith(name + " ")
                    for name in EXCLUDED_LANGUAGE_SECTIONS
                )
            continue
        if excluded or not line.strip():
            continue
        cleaned = URL_RE.sub(" ", line)
        cleaned = INLINE_CODE_RE.sub(" ", cleaned)
        cleaned = HTML_TAG_RE.sub(" ", cleaned)
        cleaned = re.sub(r"!\[[^\]]*\]", " ", cleaned)
        cleaned = re.sub(r"\[([^\]]+)\]", r"\1", cleaned)
        cleaned = re.sub(r"[*_~>#|]", " ", cleaned)
        if cleaned.strip():
            parts.append(cleaned)
    return clean_for_language_ratio("\n".join(parts))


def _japanese_ratio(text: str) -> tuple[float, int, int]:
    prose = _language_prose(text)
    jp = len(JP_RE.findall(prose))
    latin = len(LATIN_RE.findall(prose))
    denom = jp + latin
    return (jp / denom if denom else 1.0), jp, latin


def audit_file(path: Path, repo_root: Path, args: argparse.Namespace | None = None) -> PaperResult:
    path = Path(path)
    repo_root = Path(repo_root)
    raw = path.read_bytes()
    failures: list[str] = []
    warnings: list[str] = []
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        try:
            relative = path.relative_to(repo_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        return PaperResult(
            path=relative,
            status="FAIL",
            file_bytes=len(raw),
            failures=[f"UTF-8として読めない: {exc}"],
        )

    jp_ratio, jp_chars, latin_chars = _japanese_ratio(text)

    meta, fm_failures = _frontmatter(text)
    failures.extend(fm_failures)
    if meta:
        for key in ("canonical_id", "title", "source", "summary", "list_summary"):
            value = meta.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                failures.append(f"frontmatter.{key} が空")
    if not _balanced_fences(text):
        failures.append("Markdownコードフェンスが閉じていない")
    if jp_ratio < DEFAULT_MIN_JAPANESE_RATIO:
        failures.append(
            f"日本語比率 {jp_ratio:.1%} < {DEFAULT_MIN_JAPANESE_RATIO:.0%}"
        )
    elif jp_ratio < DEFAULT_WARN_JAPANESE_RATIO:
        warnings.append(
            f"日本語比率 {jp_ratio:.1%} < 警告基準 {DEFAULT_WARN_JAPANESE_RATIO:.0%}"
        )

    try:
        relative = path.relative_to(repo_root).as_posix()
    except ValueError:
        relative = path.as_posix()
    status = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return PaperResult(
        path=relative,
        status=status,
        file_bytes=len(raw),
        japanese_ratio=jp_ratio,
        japanese_chars=jp_chars,
        latin_chars=latin_chars,
        failures=failures,
        warnings=warnings,
    )


def iter_papers(repo_root: Path) -> Iterable[Path]:
    for root in ("papers/inference", "papers/training", "papers/survey"):
        base = repo_root / root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if is_paper_summary(path):
                yield path


def markdown_report(results: list[PaperResult]) -> str:
    failed = [x for x in results if x.status == "FAIL"]
    lines = [
        "# Paper publication-integrity audit",
        "",
        f"- 対象: {len(results)}件",
        f"- PASS: {len(results) - len(failed)}件",
        f"- FAIL: {len(failed)}件",
        "- 意味品質・説明量は対象外。日本語率のみ文体上の機械ゲートとして維持",
        "",
    ]
    if failed:
        lines += ["## FAIL", ""]
        for item in failed:
            lines.append(f"### `{item.path}`")
            for reason in item.failures:
                lines.append(f"- {reason}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--markdown-out", type=Path)
    ap.add_argument("--json-out", type=Path)
    ap.add_argument("--no-fail-exit", action="store_true")
    # Retired options are accepted for invocation compatibility and ignored.
    for flag in (
        "--min-bytes", "--min-prose-chars", "--min-paragraphs",
        "--min-method-paragraphs", "--min-component-paragraphs",
        "--min-japanese-ratio", "--warn-japanese-ratio",
    ):
        ap.add_argument(flag, default=None, help=argparse.SUPPRESS)
    args = ap.parse_args()
    repo_root = args.repo_root.resolve()
    results = [audit_file(path, repo_root, args) for path in iter_papers(repo_root)]

    report = markdown_report(results)
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2,
            "audit_kind": "publication_integrity",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "criteria": {
                "utf8": True,
                "parseable_frontmatter": True,
                "required_frontmatter_keys": ["canonical_id", "title", "source", "summary", "list_summary"],
                "balanced_markdown_fences": True,
                "japanese_ratio_fail_below": DEFAULT_MIN_JAPANESE_RATIO,
                "japanese_ratio_warn_below": DEFAULT_WARN_JAPANESE_RATIO,
                "semantic_quality_checked": False,
            },
            "results": [asdict(x) for x in results],
        }
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed = any(x.status == "FAIL" for x in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
