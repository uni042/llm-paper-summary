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

EXCLUDED_SECTIONS = {"一次資料", "参考文献", "References", "更新履歴", "監査メモ"}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
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
    japanese_ratio: float
    japanese_chars: int
    latin_chars: int
    bare_english_terms: list[TermHit]
    failures: list[str]
    warnings: list[str]


def strip_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    if not lines or lines[0].strip() != "---":
        return lines, 0
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[idx + 1 :], idx + 1
    return lines, 0


def normalize_heading(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    return text.strip()


def is_excluded_section(title: str) -> bool:
    title = normalize_heading(title)
    return any(title == x or title.startswith(x + " ") for x in EXCLUDED_SECTIONS)


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
        if current_h2 and (current_h2 == "手法" or current_h2.startswith("手法 ")):
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
                and (current_h2 == "手法" or current_h2.startswith("手法 "))
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
    raw = path.read_text(encoding="utf-8")
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

    has_method = any(
        h2 and (h2 == "手法" or h2.startswith("手法 "))
        for _, _, h2, _ in iter_body_lines(raw_lines)
    )
    if not has_method:
        failures.append("「## 手法」節がない")
    elif len(method_blocks) < args.min_method_paragraphs:
        failures.append(f"手法段落数 {len(method_blocks)} < {args.min_method_paragraphs}")

    if len(method_components) >= 3:
        for component_id, paragraphs in sorted(method_components.items()):
            if len(paragraphs) < args.min_component_paragraphs:
                failures.append(
                    f"手法構成要素#{component_id} の段落数 {len(paragraphs)} "
                    f"< {args.min_component_paragraphs}"
                )

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
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# 論文要約の機械的品質監査",
        "",
        f"- 生成日時: {now}",
        f"- 対象: {len(results)}件",
        f"- 合格: {len(passed)}件 / 警告: {len(warned)}件 / 不合格: {len(failed)}件",
        f"- 日本語比率: 不合格 < {args.min_japanese_ratio:.0%}、警告 < {args.warn_japanese_ratio:.0%}",
        "- 英語専門語: 日本語・カタカナに置換可能な語が裸で1件でも残れば不合格",
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
            f"- 説明段落: {r.paragraphs} / 手法段落: {r.method_paragraphs}",
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
    files = sorted(papers_root.rglob("*.md"))
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
            "schema_version": 2,
            "criteria": {
                "min_bytes": args.min_bytes,
                "min_prose_chars": args.min_prose_chars,
                "min_paragraphs": args.min_paragraphs,
                "min_method_paragraphs": args.min_method_paragraphs,
                "min_component_paragraphs": args.min_component_paragraphs,
                "min_japanese_ratio": args.min_japanese_ratio,
                "warn_japanese_ratio": args.warn_japanese_ratio,
                "bare_english_terms_allowed": 0,
            },
            "results": [asdict(r) for r in results],
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed = any(r.status == "FAIL" for r in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
