#!/usr/bin/env python3
"""Repository-wide publication-integrity audit for paper Markdown.

Semantic correctness still belongs to the reading worker.  This module also
measures a conservative explanation floor so newly completed Research can be
sent back for rereading when the body is obviously too short.  Passing the
floor never proves semantic quality.
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
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

EXCLUDED_LANGUAGE_SECTIONS = {
    "書誌情報", "一次資料", "参考文献", "References", "更新履歴", "監査メモ"
}
EXCLUDED_QUALITY_SECTIONS = EXCLUDED_LANGUAGE_SECTIONS | {
    "引用", "登録履歴"
}
# Compatibility alias for callers/tests that previously referenced this name.
EXCLUDED_SECTIONS = EXCLUDED_LANGUAGE_SECTIONS

# Publication-integrity compatibility values.  The repository-wide audit does
# not turn these into semantic PASS criteria.
DEFAULT_MIN_BYTES = 0
DEFAULT_MIN_PROSE_CHARS = 0
DEFAULT_MIN_PARAGRAPHS = 0
DEFAULT_MIN_METHOD_PARAGRAPHS = 0
DEFAULT_MIN_COMPONENT_PARAGRAPHS = 0
DEFAULT_MIN_JAPANESE_RATIO = 0.70
DEFAULT_WARN_JAPANESE_RATIO = 0.80
STRUCTURED_METHOD_MIN_PROSE_CHARS = 0
STRUCTURED_METHOD_MIN_PARAGRAPHS = 0

# Conservative "too short to call complete" trigger used by Research preflight
# and the Library import gate.  These are one-way lower bounds: meeting them
# does not establish semantic quality.
QUALITY_GATE_VERSION = "2026-10-07-v1"
QUALITY_MIN_BODY_CHARS = 2200
QUALITY_MIN_METHOD_CHARS = 700
QUALITY_MIN_EVALUATION_CHARS = 500
QUALITY_WARN_LIMITATION_CHARS = 120

METHOD_H2_PREFIXES = (
    "手法", "提案手法", "方法", "アルゴリズム", "システム設計", "設計",
    "アーキテクチャ", "調査方法", "分析方法", "分類", "体系化",
    "method", "approach", "methodology", "algorithm", "architecture", "taxonomy",
)
EVALUATION_H2_PREFIXES = (
    "評価", "実験", "結果", "主要結果", "性能", "ベンチマーク",
    "evaluation", "experiment", "result", "benchmark",
)
LIMITATION_H2_PREFIXES = (
    "限界", "制約", "適用範囲", "評価上の制約",
    "limitation", "constraint", "scope",
)

# Japanese section titles often join 評価/実験/性能 directly with a noun
# (評価条件と結果, 評価結果と解釈, 実験結果).  Whitespace/punctuation-only
# matching incorrectly measures such sections as zero characters.
# Restrict the accepted compounds to evaluation-related nouns rather than
# using startswith("評価"), which would count 評価上の制約 as evaluation.
EVALUATION_H2_COMPOUND_SUFFIXES = (
    "条件", "結果", "指標", "設定", "方法", "実験", "環境",
    "分析", "比較", "考察", "測定", "概要", "検証",
)
EVALUATION_H2_COMPOUND_PREFIXES = ("評価", "実験", "性能", "ベンチマーク")


@dataclass
class TermHit:
    term: str
    preferred: str
    count: int
    lines: list[int] = field(default_factory=list)


@dataclass
class PaperResult:
    path: str
    status: str
    file_bytes: int
    prose_chars: int = 0
    paragraphs: int = 0
    method_paragraphs: int = 0
    method_components: int = 0
    method_detection: str = "not-evaluated"
    method_chars: int = 0
    evaluation_chars: int = 0
    limitation_chars: int = 0
    quality_gate_version: str = QUALITY_GATE_VERSION
    insufficiency_flags: list[str] = field(default_factory=list)
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


def _heading_matches(title: str, prefixes: tuple[str, ...]) -> bool:
    normalized = _normalize_heading(title).casefold()
    return any(
        normalized == prefix.casefold()
        or normalized.startswith(prefix.casefold() + " ")
        or normalized.startswith(prefix.casefold() + "：")
        or normalized.startswith(prefix.casefold() + ":")
        or normalized.startswith(prefix.casefold() + "の")
        or normalized.startswith(prefix.casefold() + "・")
        or normalized.startswith(prefix.casefold() + "／")
        or normalized.startswith(prefix.casefold() + "/")
        or normalized.startswith(prefix.casefold() + "（")
        or normalized.startswith(prefix.casefold() + "(")
        for prefix in prefixes
    )


def _evaluation_heading_matches(title: str) -> bool:
    if _heading_matches(title, EVALUATION_H2_PREFIXES):
        return True
    normalized = _normalize_heading(title)
    return any(
        normalized.startswith(prefix + suffix)
        for prefix in EVALUATION_H2_COMPOUND_PREFIXES
        for suffix in EVALUATION_H2_COMPOUND_SUFFIXES
    )


def _excluded_quality_section(title: str) -> bool:
    normalized = _normalize_heading(title)
    return any(
        normalized == name or normalized.startswith(name + " ")
        for name in EXCLUDED_QUALITY_SECTIONS
    )


def _clean_metric_line(line: str) -> str:
    cleaned = URL_RE.sub(" ", line)
    cleaned = INLINE_CODE_RE.sub(" ", cleaned)
    cleaned = HTML_TAG_RE.sub(" ", cleaned)
    cleaned = re.sub(r"!\[[^\]]*\]", " ", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = LIST_RE.sub("", cleaned)
    cleaned = re.sub(r"[*_~>#]", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _quality_metrics(text: str) -> dict[str, int | str | list[str]]:
    """Measure explanation prose while excluding frontmatter/references/tables.

    The metric is intentionally simple and reproducible.  It is a shortness
    detector, not a semantic grader.
    """
    lines, _ = strip_frontmatter(text.splitlines())
    in_fence = False
    section = "other"
    excluded = False

    chars = {"body": 0, "method": 0, "evaluation": 0, "limitation": 0}
    paragraphs = {"body": 0, "method": 0}
    pending = {"body": 0, "method": 0}

    def flush() -> None:
        if pending["body"] >= 20:
            paragraphs["body"] += 1
        if pending["method"] >= 20:
            paragraphs["method"] += 1
        pending["body"] = 0
        pending["method"] = 0

    for line in lines:
        if FENCE_RE.match(line):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        hm = HEADING_RE.match(line)
        if hm:
            flush()
            if len(hm.group(1)) == 2:
                title = _normalize_heading(hm.group(2))
                excluded = _excluded_quality_section(title)
                if excluded:
                    section = "excluded"
                elif _heading_matches(title, METHOD_H2_PREFIXES):
                    section = "method"
                elif _evaluation_heading_matches(title):
                    section = "evaluation"
                elif _heading_matches(title, LIMITATION_H2_PREFIXES):
                    section = "limitation"
                else:
                    section = "other"
            continue

        stripped = line.strip()
        if excluded or not stripped or TABLE_RE.match(line):
            flush()
            continue

        cleaned = _clean_metric_line(line)
        if not cleaned:
            flush()
            continue
        count = len(re.sub(r"\s+", "", cleaned))
        if count == 0:
            continue

        chars["body"] += count
        pending["body"] += count
        if section == "method":
            chars["method"] += count
            pending["method"] += count
        elif section == "evaluation":
            chars["evaluation"] += count
        elif section == "limitation":
            chars["limitation"] += count

        # Each list item is semantically separate even without a blank line.
        if LIST_RE.match(line):
            flush()

    flush()

    flags: list[str] = []
    if chars["body"] < QUALITY_MIN_BODY_CHARS:
        flags.append(f"本文説明量 {chars['body']} < {QUALITY_MIN_BODY_CHARS}")
    if chars["method"] < QUALITY_MIN_METHOD_CHARS:
        flags.append(f"手法説明量 {chars['method']} < {QUALITY_MIN_METHOD_CHARS}")
    if chars["evaluation"] < QUALITY_MIN_EVALUATION_CHARS:
        flags.append(f"評価説明量 {chars['evaluation']} < {QUALITY_MIN_EVALUATION_CHARS}")
    if chars["limitation"] < QUALITY_WARN_LIMITATION_CHARS:
        flags.append(f"限界説明量 {chars['limitation']} < 推奨 {QUALITY_WARN_LIMITATION_CHARS}")

    return {
        "body_chars": chars["body"],
        "body_paragraphs": paragraphs["body"],
        "method_chars": chars["method"],
        "method_paragraphs": paragraphs["method"],
        "evaluation_chars": chars["evaluation"],
        "limitation_chars": chars["limitation"],
        "flags": flags,
    }


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
    metrics = _quality_metrics(text)

    meta, fm_failures = _frontmatter(text)
    failures.extend(fm_failures)
    if meta:
        for key in ("canonical_id", "title", "source", "summary", "list_summary"):
            value = meta.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                failures.append(f"frontmatter.{key} が空")

        # New templates carry an explicit semantic self-review attestation.
        # Legacy papers without these fields are grandfathered; a present but
        # unfinished attestation is never accepted.
        if "quality_self_review_version" in meta or "quality_self_review_passed" in meta:
            if meta.get("quality_self_review_passed") is not True:
                failures.append("quality_self_review_passed が true ではない")
            version = str(meta.get("quality_self_review_version") or "").strip()
            if not version:
                failures.append("quality_self_review_version が空")

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

    enforce_floor = bool(getattr(args, "enforce_explanation_floor", False))
    if enforce_floor:
        if int(metrics["body_chars"]) < QUALITY_MIN_BODY_CHARS:
            failures.append(
                f"説明不足トリガー: 本文説明量 {metrics['body_chars']} < {QUALITY_MIN_BODY_CHARS}"
            )
        if int(metrics["method_chars"]) < QUALITY_MIN_METHOD_CHARS:
            failures.append(
                f"説明不足トリガー: 手法説明量 {metrics['method_chars']} < {QUALITY_MIN_METHOD_CHARS}"
            )
        if int(metrics["evaluation_chars"]) < QUALITY_MIN_EVALUATION_CHARS:
            failures.append(
                f"説明不足トリガー: 評価説明量 {metrics['evaluation_chars']} < {QUALITY_MIN_EVALUATION_CHARS}"
            )
        if int(metrics["limitation_chars"]) < QUALITY_WARN_LIMITATION_CHARS:
            warnings.append(
                f"限界説明量 {metrics['limitation_chars']} < 推奨 {QUALITY_WARN_LIMITATION_CHARS}; "
                "一次資料と照合して具体性を確認"
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
        prose_chars=int(metrics["body_chars"]),
        paragraphs=int(metrics["body_paragraphs"]),
        method_paragraphs=int(metrics["method_paragraphs"]),
        method_detection="measured",
        method_chars=int(metrics["method_chars"]),
        evaluation_chars=int(metrics["evaluation_chars"]),
        limitation_chars=int(metrics["limitation_chars"]),
        insufficiency_flags=list(metrics["flags"]),
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
    suspicious = [x for x in results if x.insufficiency_flags]
    lines = [
        "# Paper publication-integrity audit",
        "",
        f"- 対象: {len(results)}件",
        f"- PASS/WARN: {len(results) - len(failed)}件",
        f"- FAIL: {len(failed)}件",
        f"- 説明不足トリガー該当: {len(suspicious)}件（repository-wide監査では自動FAILにしない）",
        "- 意味品質は読解ワーカーの責務。本文/手法/評価量は極端な短文化を検知する補助指標",
        "",
    ]
    if suspicious:
        lines += ["## 説明不足トリガー候補", ""]
        for item in suspicious:
            lines.append(
                f"- `{item.path}` — 本文 {item.prose_chars} / 手法 {item.method_chars} / "
                f"評価 {item.evaluation_chars} / 限界 {item.limitation_chars}文字"
            )
        lines.append("")
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
    args.enforce_explanation_floor = False
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
            "schema_version": 3,
            "audit_kind": "publication_integrity_with_explanation_metrics",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "criteria": {
                "utf8": True,
                "parseable_frontmatter": True,
                "required_frontmatter_keys": ["canonical_id", "title", "source", "summary", "list_summary"],
                "balanced_markdown_fences": True,
                "japanese_ratio_fail_below": DEFAULT_MIN_JAPANESE_RATIO,
                "japanese_ratio_warn_below": DEFAULT_WARN_JAPANESE_RATIO,
                "semantic_quality_checked": False,
                "explanation_floor_measured": True,
                "explanation_floor_enforced_in_repository_audit": False,
                "explanation_floor_version": QUALITY_GATE_VERSION,
                "explanation_floor": {
                    "body_chars": QUALITY_MIN_BODY_CHARS,
                    "method_chars": QUALITY_MIN_METHOD_CHARS,
                    "evaluation_chars": QUALITY_MIN_EVALUATION_CHARS,
                    "limitation_chars_warning": QUALITY_WARN_LIMITATION_CHARS,
                },
            },
            "results": [asdict(x) for x in results],
        }
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed = any(x.status == "FAIL" for x in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
