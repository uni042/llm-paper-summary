#!/usr/bin/env python3
"""Repository-wide mechanical quality audit for Japanese paper summaries."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from japanese_style import (  # noqa: E402
    DEFAULT_MIN_JAPANESE_RATIO,
    DEFAULT_WARN_JAPANESE_RATIO,
    JP_RE,
    LATIN_RE,
    PREFERRED_TERMS,
    TERM_PATTERNS,
    clean_for_language_ratio,
)

DEFAULT_MIN_BYTES = 4500
DEFAULT_MIN_PROSE_CHARS = 2200
DEFAULT_MIN_PARAGRAPHS = 10
DEFAULT_MIN_METHOD_PARAGRAPHS = 4
DEFAULT_MIN_COMPONENT_PARAGRAPHS = 2

# A long, well-structured summary may explain the mechanism through several
# descriptive H2 sections instead of placing all prose below one literal
# ``## 手法`` heading. Treat such documents as a structural equivalent rather
# than reporting a false content failure.
STRUCTURED_METHOD_MIN_PROSE_CHARS = 4000
STRUCTURED_METHOD_MIN_PARAGRAPHS = 20
STRUCTURED_METHOD_MIN_H2_SECTIONS = 3

EXCLUDED_SECTIONS = {"一次資料", "参考文献", "References", "更新履歴", "監査メモ"}
NON_METHOD_H2_PREFIXES = (
    "概要",
    "背景",
    "動機",
    "問題",
    "まず",
    "なぜ",
    "新規性",
    "評価",
    "結果",
    "主要結果",
    "評価条件",
    "既存研究",
    "関連研究",
    "限界",
    "一般的",
    "実装状況",
    "コード",
    "引用",
    "一次資料",
    "参考文献",
    "更新履歴",
    "登録履歴",
    "監査",
    "比較",
    "まとめ",
    "結論",
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
# Existing summaries use variants such as ``手法のあらまし``, ``提案手法``
# and numbered sections such as ``手法1: ...``.
METHOD_HEADING_RE = re.compile(r"^(?:提案)?手法(?:$|[\sの：:（(・]|\d)")
MOVED_HEADING_RE = re.compile(r"^#\s+Moved(?:\s|$)", re.I)
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
DETAILS_RE = re.compile(r"^\s*</?(?:details|summary)[^>]*>\s*$", re.I)
FENCE_RE = re.compile(r"^\s*```")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MD_LINK_DEST_RE = re.compile(r"\]\((?:https?://|[^)]*/)[^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")


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
    prose_chars: int
    paragraphs: int
    method_paragraphs: int
    method_components: int
    method_detection: str
    japanese_ratio: float
    japanese_chars: int
    latin_chars: int
    bare_english_terms: list[TermHit]
    failures: list[str]
    warnings: list[str]


def strip_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    """Return body lines and the original-line offset of a valid YAML front matter."""
    if not lines or lines[0].strip() != "---":
        return lines, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[idx + 1 :], idx + 1
    # Malformed front matter must not hide the file from the audit.
    return lines, 0


def normalize_heading(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    return text.strip()


def is_method_heading(title: str) -> bool:
    """Accept the current heading and legacy/numbered equivalents."""
    return bool(METHOD_HEADING_RE.match(normalize_heading(title)))


def is_excluded_section(title: str) -> bool:
    title = normalize_heading(title)
    return any(title == x or title.startswith(x + " ") for x in EXCLUDED_SECTIONS)


def is_non_method_h2(title: str) -> bool:
    title = normalize_heading(title)
    return any(title.startswith(prefix) for prefix in NON_METHOD_H2_PREFIXES)


def is_moved_stub(raw_lines: list[str]) -> bool:
    """Detect migration stubs even when they retain YAML front matter."""
    body, _ = strip_frontmatter(raw_lines)
    for line in body:
        stripped = line.strip()
        if not stripped:
            continue
        return bool(MOVED_HEADING_RE.match(stripped))
    return False


def is_paper_summary(path: Path) -> bool:
    """Return whether *path* should be audited as an individual paper summary.

    Inclusion deliberately does not depend on front-matter validity or
    ``canonical_id``. Broken metadata must not make a real paper silently
    disappear from the repository-wide quality audit. Repository navigation
    pages, the generated cross-paper comparison page and migration stubs are
    explicitly excluded instead.
    """
    if path.name.casefold() in {"readme.md", "comparison.md"}:
        return False
    raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return not is_moved_stub(raw_lines)


def iter_body_lines(raw_lines: list[str]) -> Iterable[tuple[int, str, str | None, int | None]]:
    lines, offset = strip_frontmatter(raw_lines)
    in_fence = False
    current_h2: str | None = None
    current_h3_index: int | None = None
    h3_counter = 0
    excluded = False

    for local_idx, line in enumerate(lines, start=1):
        lineno = local_idx + offset
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        hm = HEADING_RE.match(line)
        if hm:
            level = len(hm.group(1))
            title = normalize_heading(hm.group(2))
            if level == 2:
                current_h2 = title
                excluded = is_excluded_section(title)
                current_h3_index = None
                h3_counter = 0
            elif level == 3:
                h3_counter += 1
                current_h3_index = h3_counter
            if not excluded:
                yield lineno, line, current_h2, current_h3_index
            continue

        if not excluded:
            yield lineno, line, current_h2, current_h3_index


def clean_inline(text: str) -> str:
    text = URL_RE.sub(" ", text)
    text = MD_LINK_DEST_RE.sub("]", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = re.sub(r"!\[[^\]]*\]", " ", text)
    text = re.sub(r"\[([^\]]+)\]", r"\1", text)
    text = re.sub(r"[*_~>#]", " ", text)
    return text


def prose_blocks(raw_lines: list[str]) -> tuple[list[str], list[str], dict[int, list[str]]]:
    all_blocks: list[str] = []
    method_blocks: list[str] = []
    method_components: dict[int, list[str]] = {}
    current: list[str] = []
    current_h2: str | None = None
    current_h3: int | None = None

    def flush() -> None:
        nonlocal current
        if not current:
            return
        block = " ".join(s.strip() for s in current if s.strip()).strip()
        current = []
        if len(block) < 20:
            return
        all_blocks.append(block)
        if current_h2 and is_method_heading(current_h2):
            method_blocks.append(block)
            if current_h3 is not None:
                method_components.setdefault(current_h3, []).append(block)

    for _, line, h2, h3 in iter_body_lines(raw_lines):
        hm = HEADING_RE.match(line)
        if hm:
            flush()
            current_h2, current_h3 = h2, h3
            if (
                len(hm.group(1)) == 3
                and current_h2
                and is_method_heading(current_h2)
                and current_h3 is not None
            ):
                method_components.setdefault(current_h3, [])
            continue

        if not line.strip() or TABLE_RE.match(line) or DETAILS_RE.match(line) or LIST_RE.match(line):
            flush()
            continue
        cleaned = clean_inline(line)
        if not cleaned.strip():
            flush()
            continue
        current_h2, current_h3 = h2, h3
        current.append(cleaned)

    flush()
    return all_blocks, method_blocks, method_components


def prose_text_for_ratio(raw_lines: list[str]) -> str:
    parts: list[str] = []
    for _, line, _, _ in iter_body_lines(raw_lines):
        if HEADING_RE.match(line) or TABLE_RE.match(line) or DETAILS_RE.match(line):
            continue
        if not line.strip():
            continue
        cleaned = clean_inline(line)
        if cleaned.strip():
            parts.append(cleaned)
    return "\n".join(parts)


def structured_method_equivalent(
    raw_lines: list[str], prose_chars: int, paragraph_count: int
) -> bool:
    """Return whether a detailed multi-section document is method-equivalent.

    This is intentionally conservative. It is only a fallback when no explicit
    method heading exists, and requires substantially more prose than the normal
    minimum plus at least three descriptive H2 sections that are not obviously
    background/evaluation/reference sections.
    """
    if prose_chars < STRUCTURED_METHOD_MIN_PROSE_CHARS:
        return False
    if paragraph_count < STRUCTURED_METHOD_MIN_PARAGRAPHS:
        return False

    method_like_h2: list[str] = []
    seen: set[str] = set()
    for _, line, _, _ in iter_body_lines(raw_lines):
        hm = HEADING_RE.match(line)
        if not hm or len(hm.group(1)) != 2:
            continue
        title = normalize_heading(hm.group(2))
        if is_excluded_section(title) or is_non_method_h2(title):
            continue
        if title not in seen:
            seen.add(title)
            method_like_h2.append(title)
    return len(method_like_h2) >= STRUCTURED_METHOD_MIN_H2_SECTIONS


def find_bare_english_terms(raw_lines: list[str]) -> list[TermHit]:
    hits: dict[str, list[int]] = {}
    for lineno, line, _, _ in iter_body_lines(raw_lines):
        if HEADING_RE.match(line) or TABLE_RE.match(line):
            continue
        cleaned = clean_for_language_ratio(clean_inline(line))
        for canonical, pattern in TERM_PATTERNS.items():
            count = len(pattern.findall(cleaned))
            if count:
                hits.setdefault(canonical, []).extend([lineno] * count)
    return [
        TermHit(
            term=term,
            preferred=PREFERRED_TERMS[term][0],
            count=len(lines),
            lines=sorted(set(lines))[:8],
        )
        for term, lines in sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]


def audit_file(path: Path, repo_root: Path, args: argparse.Namespace) -> PaperResult:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    raw_lines = raw.splitlines()
    blocks, method_blocks, method_components = prose_blocks(raw_lines)
    prose = clean_for_language_ratio(prose_text_for_ratio(raw_lines))
    jp_chars = len(JP_RE.findall(prose))
    latin_chars = len(LATIN_RE.findall(prose))
    denominator = jp_chars + latin_chars
    jp_ratio = jp_chars / denominator if denominator else 1.0
    bare_terms = find_bare_english_terms(raw_lines)

    failures: list[str] = []
    warnings: list[str] = []
    size = len(raw.encode("utf-8"))
    prose_chars = sum(len(b) for b in blocks)

    if size < args.min_bytes:
        failures.append(f"ファイルサイズ {size} < {args.min_bytes} bytes")
    if prose_chars < args.min_prose_chars:
        failures.append(f"説明文文字数 {prose_chars} < {args.min_prose_chars}")
    if len(blocks) < args.min_paragraphs:
        failures.append(f"説明段落数 {len(blocks)} < {args.min_paragraphs}")

    has_explicit_method = any(
        h2 and is_method_heading(h2)
        for _, _, h2, _ in iter_body_lines(raw_lines)
    )
    has_structured_equivalent = (
        not has_explicit_method
        and structured_method_equivalent(raw_lines, prose_chars, len(blocks))
    )
    if has_explicit_method:
        method_detection = "explicit"
        if len(method_blocks) < args.min_method_paragraphs:
            failures.append(f"手法段落数 {len(method_blocks)} < {args.min_method_paragraphs}")
        if len(method_components) >= 3:
            for component_id, paragraphs in sorted(method_components.items()):
                if len(paragraphs) < args.min_component_paragraphs:
                    failures.append(
                        f"手法構成要素#{component_id} の段落数 {len(paragraphs)} "
                        f"< {args.min_component_paragraphs}"
                    )
    elif has_structured_equivalent:
        method_detection = "structured-equivalent"
    else:
        method_detection = "missing"
        failures.append("手法説明が不足（明示的な手法節も十分な構造化手法説明もない）")

    if jp_ratio < args.min_japanese_ratio:
        failures.append(f"日本語比率 {jp_ratio:.1%} < {args.min_japanese_ratio:.1%}")
    elif jp_ratio < args.warn_japanese_ratio:
        warnings.append(f"日本語比率 {jp_ratio:.1%} < 警告基準 {args.warn_japanese_ratio:.1%}")

    if bare_terms:
        preview = ", ".join(
            f"{x.term}→{x.preferred} ×{x.count}" for x in bare_terms[:8]
        )
        failures.append(f"日本語化できる英語専門語が裸で残っている: {preview}")

    status = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return PaperResult(
        path=path.relative_to(repo_root).as_posix(),
        status=status,
        file_bytes=size,
        prose_chars=prose_chars,
        paragraphs=len(blocks),
        method_paragraphs=len(method_blocks),
        method_components=len(method_components),
        method_detection=method_detection,
        japanese_ratio=jp_ratio,
        japanese_chars=jp_chars,
        latin_chars=latin_chars,
        bare_english_terms=bare_terms,
        failures=failures,
        warnings=warnings,
    )


def markdown_report(results: list[PaperResult], args: argparse.Namespace) -> str:
    failed = [r for r in results if r.status == "FAIL"]
    warned = [r for r in results if r.status == "WARN"]
    passed = [r for r in results if r.status == "PASS"]
    structured = [r for r in results if r.method_detection == "structured-equivalent"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# 論文要約の機械的品質監査",
        "",
        f"- 生成日時: {now}",
        f"- 対象: {len(results)}件",
        f"- 合格: {len(passed)}件 / 警告: {len(warned)}件 / 不合格: {len(failed)}件",
        f"- 構造化手法相当として認識: {len(structured)}件",
        f"- 日本語比率: 不合格 < {args.min_japanese_ratio:.0%}、警告 < {args.warn_japanese_ratio:.0%}",
        "- 英語専門語: 日本語・カタカナに置換可能な語が裸で1件でも残れば不合格",
        "- 対象判定: papers/inference 配下の Markdown から README、comparison.md、# Moved 移動元を除外",
        "- 手法見出し: 「手法」「手法のあらまし」「提案手法」「手法1: ...」などを同一扱い",
        "- 明示的な手法見出しがない長文要約は、十分な説明量と複数の機構別H2があれば構造化手法相当として扱う",
        "",
        "## 基準未達",
        "",
    ]
    if not failed:
        lines.append("なし")
    for r in failed:
        lines += [
            f"### `{r.path}`",
            "",
            f"- 日本語比率: {r.japanese_ratio:.1%}",
            f"- 説明段落: {r.paragraphs} / 手法段落: {r.method_paragraphs} / 手法判定: {r.method_detection}",
            f"- ファイルサイズ: {r.file_bytes} bytes / 説明文: {r.prose_chars}文字",
        ]
        for reason in r.failures:
            lines.append(f"- **不合格理由:** {reason}")
        for hit in r.bare_english_terms:
            loc = ", ".join(f"L{x}" for x in hit.lines)
            lines.append(
                f"- 用語: `{hit.term}` → **{hit.preferred}** "
                f"（{hit.count}件; {loc or '行番号なし'}）"
            )
        lines.append("")
    if warned:
        lines += ["## 警告のみ", ""]
        for r in warned:
            lines.append(f"- `{r.path}` — " + "; ".join(r.warnings))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--papers-root", default="papers/inference")
    ap.add_argument("--markdown-out")
    ap.add_argument("--json-out")
    ap.add_argument("--min-bytes", type=int, default=DEFAULT_MIN_BYTES)
    ap.add_argument("--min-prose-chars", type=int, default=DEFAULT_MIN_PROSE_CHARS)
    ap.add_argument("--min-paragraphs", type=int, default=DEFAULT_MIN_PARAGRAPHS)
    ap.add_argument("--min-method-paragraphs", type=int, default=DEFAULT_MIN_METHOD_PARAGRAPHS)
    ap.add_argument("--min-component-paragraphs", type=int, default=DEFAULT_MIN_COMPONENT_PARAGRAPHS)
    ap.add_argument("--min-japanese-ratio", type=float, default=DEFAULT_MIN_JAPANESE_RATIO)
    ap.add_argument("--warn-japanese-ratio", type=float, default=DEFAULT_WARN_JAPANESE_RATIO)
    ap.add_argument("--no-fail-exit", action="store_true")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    papers_root = (repo_root / args.papers_root).resolve()
    files = sorted(path for path in papers_root.rglob("*.md") if is_paper_summary(path))
    results = [audit_file(path, repo_root, args) for path in files]
    report = markdown_report(results, args)

    if args.markdown_out:
        out = repo_root / args.markdown_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    if args.json_out:
        out = repo_root / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 4,
            "criteria": {
                "min_bytes": args.min_bytes,
                "min_prose_chars": args.min_prose_chars,
                "min_paragraphs": args.min_paragraphs,
                "min_method_paragraphs": args.min_method_paragraphs,
                "min_component_paragraphs": args.min_component_paragraphs,
                "min_japanese_ratio": args.min_japanese_ratio,
                "warn_japanese_ratio": args.warn_japanese_ratio,
                "bare_english_terms_allowed": 0,
                "paper_target_policy": "all Markdown under papers/inference except README, comparison.md and # Moved stubs",
                "method_heading_compatibility": ["手法", "手法の…", "提案手法", "手法N: …"],
                "structured_method_fallback": {
                    "min_prose_chars": STRUCTURED_METHOD_MIN_PROSE_CHARS,
                    "min_paragraphs": STRUCTURED_METHOD_MIN_PARAGRAPHS,
                    "min_method_like_h2_sections": STRUCTURED_METHOD_MIN_H2_SECTIONS,
                },
            },
            "results": [asdict(r) for r in results],
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed = any(r.status == "FAIL" for r in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
