#!/usr/bin/env python3
"""Repository-wide mechanical quality audit for paper summaries.

This script complements the semantic paper.md review. It intentionally checks
only properties that can be measured reliably: document size, explanatory
paragraph density, Japanese-vs-Latin character balance, required section
presence, and bare English technical terms that violate the repository's
Japanese-first terminology rule.
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

DEFAULT_MIN_BYTES = 4500
DEFAULT_MIN_PROSE_CHARS = 2200
DEFAULT_MIN_PARAGRAPHS = 10
DEFAULT_MIN_METHOD_PARAGRAPHS = 4
DEFAULT_MIN_JAPANESE_RATIO = 0.50
DEFAULT_WARN_JAPANESE_RATIO = 0.60
DEFAULT_MIN_COMPONENT_PARAGRAPHS = 2

EXCLUDED_SECTIONS = {
    "一次資料",
    "参考文献",
    "References",
    "更新履歴",
    "監査メモ",
}

# English terms that should normally be introduced as
# "日本語（English term）" and then written in Japanese or as an established acronym.
# Proper names, model names, framework names, acronyms, units, and URLs are not
# covered here.
TERM_RULES: dict[str, tuple[str, ...]] = {
    "request": ("request", "requests", "request-wise"),
    "token": ("token", "tokens", "token-level", "per-token"),
    "layer": ("layer", "layers", "layer-wise", "per-layer"),
    "batch": ("batch", "batches"),
    "decode": ("decode", "decoding"),
    "prefill": ("prefill",),
    "offload": ("offload", "offloading", "offloaded"),
    "cache": ("cache", "caching"),
    "prefetch": ("prefetch", "prefetching"),
    "eviction": ("eviction", "evict", "evicted"),
    "scheduler": ("scheduler", "scheduling"),
    "placement": ("placement",),
    "runtime": ("runtime",),
    "latency": ("latency", "latencies"),
    "throughput": ("throughput",),
    "bandwidth": ("bandwidth",),
    "memory": ("memory",),
    "stream": ("stream", "streams"),
    "buffer": ("buffer", "buffers"),
    "solver": ("solver",),
    "pipeline": ("pipeline",),
    "routing": ("routing", "router"),
    "expert": ("expert", "experts"),
    "kernel": ("kernel", "kernels"),
    "fusion": ("fusion",),
    "quantization": ("quantization", "quantized"),
    "pruning": ("pruning", "pruned"),
    "activation": ("activation", "activations"),
    "weight": ("weight", "weights"),
    "benchmark": ("benchmark", "benchmarks"),
    "baseline": ("baseline", "baselines"),
    "trace": ("trace", "traces"),
    "workload": ("workload", "workloads"),
    "bottleneck": ("bottleneck", "bottlenecks"),
    "overhead": ("overhead",),
    "speedup": ("speedup",),
    "goodput": ("goodput",),
    "stall": ("stall", "stalls", "stalled"),
    "lossless": ("lossless",),
    "synthetic": ("synthetic",),
    "adaptive": ("adaptive",),
    "dynamic": ("dynamic",),
    "static": ("static",),
    "host": ("host",),
    "resident": ("resident",),
    "infeasible": ("infeasible",),
    "end-to-end": ("end-to-end",),
}

URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MD_LINK_DEST_RE = re.compile(r"\]\((?:https?://|[^)]*/)[^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
JP_CLASS = r"\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff々〆ヶ"
JP_RE = re.compile(f"[{JP_CLASS}]")
LATIN_RE = re.compile(r"[A-Za-z]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
DETAILS_RE = re.compile(r"^\s*</?(?:details|summary)[^>]*>\s*$", re.I)
FENCE_RE = re.compile(r"^\s*```")


@dataclass
class TermHit:
    term: str
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
    """Yield line number, line, current H2 title, current H3 ordinal marker."""
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
            if excluded:
                continue
            yield lineno, line, current_h2, current_h3_index
            continue

        if excluded:
            continue
        yield lineno, line, current_h2, current_h3_index


def clean_inline(text: str, *, mask_parentheses: bool = False) -> str:
    text = URL_RE.sub(" ", text)
    text = MD_LINK_DEST_RE.sub("]", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    if mask_parentheses:
        # Only parenthetical English immediately following Japanese is considered
        # compliant with the repository's "日本語（English）" rule. Parentheses
        # appearing without a Japanese lead-in remain visible to the term linter.
        text = re.sub(rf"(?<=[{JP_CLASS}])（[^（）]*）", " ", text)
        text = re.sub(rf"(?<=[{JP_CLASS}])\([^()]*\)", " ", text)
    text = re.sub(r"!\[[^\]]*\]", " ", text)
    text = re.sub(r"\[([^\]]+)\]", r"\1", text)
    text = re.sub(r"[*_~>#]", " ", text)
    return text


def prose_blocks(raw_lines: list[str]) -> tuple[list[str], list[str], dict[int, list[str]]]:
    """Return all prose paragraphs, method paragraphs, and per-H3 method paragraphs."""
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
            current_h2 = h2
            current_h3 = h3
            if (
                len(hm.group(1)) == 3
                and current_h2
                and (current_h2 == "手法" or current_h2.startswith("手法 "))
                and current_h3 is not None
            ):
                method_components.setdefault(current_h3, [])
            continue
        if not line.strip():
            flush()
            continue
        if TABLE_RE.match(line) or DETAILS_RE.match(line):
            flush()
            continue
        if LIST_RE.match(line):
            # Bullets/tables are useful evidence but are not explanatory paragraphs.
            flush()
            continue
        cleaned = clean_inline(line)
        if not cleaned.strip():
            flush()
            continue
        current_h2 = h2
        current_h3 = h3
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


def term_patterns() -> dict[str, re.Pattern[str]]:
    patterns: dict[str, re.Pattern[str]] = {}
    for canonical, variants in TERM_RULES.items():
        alt = "|".join(re.escape(v) for v in sorted(variants, key=len, reverse=True))
        patterns[canonical] = re.compile(
            rf"(?<![A-Za-z0-9])(?:{alt})(?![A-Za-z0-9])", re.I
        )
    return patterns


TERM_PATTERNS = term_patterns()


def find_bare_english_terms(raw_lines: list[str]) -> list[TermHit]:
    hits: dict[str, list[int]] = {}
    for lineno, line, _, _ in iter_body_lines(raw_lines):
        if HEADING_RE.match(line) or TABLE_RE.match(line):
            continue
        cleaned = clean_inline(line, mask_parentheses=True)
        for canonical, pattern in TERM_PATTERNS.items():
            if pattern.search(cleaned):
                count = len(pattern.findall(cleaned))
                hits.setdefault(canonical, []).extend([lineno] * count)
    return [
        TermHit(term=term, count=len(lines), lines=sorted(set(lines))[:8])
        for term, lines in sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]


def audit_file(path: Path, repo_root: Path, args: argparse.Namespace) -> PaperResult:
    raw = path.read_text(encoding="utf-8")
    raw_lines = raw.splitlines()
    blocks, method_blocks, method_components = prose_blocks(raw_lines)
    prose = prose_text_for_ratio(raw_lines)
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
        failures.append(f"file_bytes {size} < {args.min_bytes}")
    if prose_chars < args.min_prose_chars:
        failures.append(f"prose_chars {prose_chars} < {args.min_prose_chars}")
    if len(blocks) < args.min_paragraphs:
        failures.append(f"paragraphs {len(blocks)} < {args.min_paragraphs}")

    has_method = any(
        h2 and (h2 == "手法" or h2.startswith("手法 "))
        for _, _, h2, _ in iter_body_lines(raw_lines)
    )
    if not has_method:
        failures.append("missing ## 手法 section")
    elif len(method_blocks) < args.min_method_paragraphs:
        failures.append(
            f"method_paragraphs {len(method_blocks)} < {args.min_method_paragraphs}"
        )

    if len(method_components) >= 3:
        for component_id, paragraphs in sorted(method_components.items()):
            if len(paragraphs) < args.min_component_paragraphs:
                failures.append(
                    f"method_component#{component_id} paragraphs {len(paragraphs)} "
                    f"< {args.min_component_paragraphs}"
                )

    if jp_ratio < args.min_japanese_ratio:
        failures.append(
            f"japanese_ratio {jp_ratio:.1%} < {args.min_japanese_ratio:.1%}"
        )
    elif jp_ratio < args.warn_japanese_ratio:
        warnings.append(
            f"japanese_ratio {jp_ratio:.1%} < warning {args.warn_japanese_ratio:.1%}"
        )

    if bare_terms:
        preview = ", ".join(f"{x.term}×{x.count}" for x in bare_terms[:8])
        failures.append(f"bare English technical terms: {preview}")

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
        "# Paper mechanical quality audit",
        "",
        f"- Generated: {now}",
        f"- Scanned: {len(results)}",
        f"- FAIL: {len(failed)}",
        f"- WARN: {len(warned)}",
        f"- PASS: {len(passed)}",
        "",
        "## Criteria",
        "",
        f"- Minimum UTF-8 file size: {args.min_bytes} bytes",
        f"- Minimum explanatory prose: {args.min_prose_chars} characters",
        f"- Minimum prose paragraphs: {args.min_paragraphs}",
        f"- Minimum method paragraphs: {args.min_method_paragraphs}",
        f"- Minimum paragraphs per method component when 3+ components exist: {args.min_component_paragraphs}",
        f"- Minimum Japanese character ratio: {args.min_japanese_ratio:.0%}",
        f"- Japanese ratio warning threshold: {args.warn_japanese_ratio:.0%}",
        "- Bare English technical terms listed in TERM_RULES are failures unless they are in a compliant Japanese-led parenthetical, inline code, URLs, headings, or tables.",
        "",
        "The Japanese ratio is diagnostic only: URLs, frontmatter, fenced/inline code, "
        "Markdown link destinations, headings, tables, and source/history sections are excluded. "
        "The terminology check is the stronger enforcement for the Japanese-first rule.",
        "",
        "## Non-conforming papers",
        "",
    ]
    nonconforming = failed + warned
    if not nonconforming:
        lines.append("No failures or warnings.")
    else:
        lines += [
            "| Status | Paper | Bytes | Prose chars | Paras | Method paras | JP ratio | Bare terms |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
        for r in nonconforming:
            lines.append(
                f"| {r.status} | `{r.path}` | {r.file_bytes} | {r.prose_chars} | "
                f"{r.paragraphs} | {r.method_paragraphs} | {r.japanese_ratio:.1%} | "
                f"{sum(x.count for x in r.bare_english_terms)} |"
            )

        lines += ["", "## Details", ""]
        for r in nonconforming:
            lines += [f"### {r.status}: `{r.path}`", ""]
            for item in r.failures:
                lines.append(f"- FAIL: {item}")
            for item in r.warnings:
                lines.append(f"- WARN: {item}")
            if r.bare_english_terms:
                lines.append("- Bare English term locations:")
                for hit in r.bare_english_terms:
                    loc = ", ".join(str(x) for x in hit.lines)
                    lines.append(f"  - `{hit.term}` × {hit.count}: lines {loc}")
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
    ap.add_argument(
        "--min-method-paragraphs", type=int, default=DEFAULT_MIN_METHOD_PARAGRAPHS
    )
    ap.add_argument(
        "--min-component-paragraphs",
        type=int,
        default=DEFAULT_MIN_COMPONENT_PARAGRAPHS,
    )
    ap.add_argument(
        "--min-japanese-ratio", type=float, default=DEFAULT_MIN_JAPANESE_RATIO
    )
    ap.add_argument(
        "--warn-japanese-ratio", type=float, default=DEFAULT_WARN_JAPANESE_RATIO
    )
    ap.add_argument(
        "--no-fail-exit",
        action="store_true",
        help="Always exit 0 even when FAIL papers exist.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    papers_root = repo_root / args.papers_root
    if not papers_root.is_dir():
        raise SystemExit(f"papers root not found: {papers_root}")

    paths = sorted(p for p in papers_root.rglob("*.md") if p.is_file())
    results = [audit_file(p, repo_root, args) for p in paths]
    results.sort(
        key=lambda r: (
            0 if r.status == "FAIL" else 1 if r.status == "WARN" else 2,
            r.japanese_ratio,
            r.path,
        )
    )

    report = markdown_report(results, args)
    print(report, end="")

    if args.markdown_out:
        out = repo_root / args.markdown_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")

    if args.json_out:
        out = repo_root / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "criteria": {
                "min_bytes": args.min_bytes,
                "min_prose_chars": args.min_prose_chars,
                "min_paragraphs": args.min_paragraphs,
                "min_method_paragraphs": args.min_method_paragraphs,
                "min_component_paragraphs": args.min_component_paragraphs,
                "min_japanese_ratio": args.min_japanese_ratio,
                "warn_japanese_ratio": args.warn_japanese_ratio,
            },
            "summary": {
                "scanned": len(results),
                "fail": sum(r.status == "FAIL" for r in results),
                "warn": sum(r.status == "WARN" for r in results),
                "pass": sum(r.status == "PASS" for r in results),
            },
            "papers": [asdict(r) for r in results],
        }
        out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    has_fail = any(r.status == "FAIL" for r in results)
    return 0 if args.no_fail_exit or not has_fail else 1


if __name__ == "__main__":
    sys.exit(main())
