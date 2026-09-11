#!/usr/bin/env python3
"""Build and audit compact Japanese one-line summaries for paper indexes."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from japanese_style import (
    DEFAULT_MIN_JAPANESE_RATIO,
    DEFAULT_WARN_JAPANESE_RATIO,
    PREFERRED_TERMS,
    TERM_PATTERNS,
    find_bare_english,
    japanese_ratio,
)

DEFAULT_MIN_CHARS = 45
DEFAULT_MAX_CHARS = 180
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]+\)")
URL_RE = re.compile(r"https?://\S+")
HTML_RE = re.compile(r"<[^>]+>")
SENTENCE_RE = re.compile(r".+?[。！？](?=\s|$)|.+$", re.S)


@dataclass
class ListSummaryQuality:
    status: str
    char_count: int
    japanese_ratio: float
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    bare_english_terms: list[str] = field(default_factory=list)


def _clean_markdown(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = URL_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def _extract_h2(body: str, title: str) -> str:
    collecting = False
    out: list[str] = []
    for line in body.splitlines():
        hm = H2_RE.match(line)
        if hm:
            current = re.sub(r"[`*_~]", "", hm.group(1)).strip()
            if collecting:
                break
            collecting = current == title or current.startswith(title + " ")
            continue
        if collecting:
            out.append(line)
    return _clean_markdown("\n".join(out))


def _extract_lead_blockquote(body: str) -> str:
    seen_h1 = False
    quote: list[str] = []
    started = False
    for line in body.splitlines():
        if line.startswith("# "):
            seen_h1 = True
            continue
        if not seen_h1:
            continue
        if H2_RE.match(line):
            break
        if line.lstrip().startswith(">"):
            started = True
            quote.append(re.sub(r"^\s*>\s?", "", line))
            continue
        if started and line.strip():
            break
    return _clean_markdown("\n".join(quote))


def extract_summary_source(body: str, fallback_summary: str = "") -> str:
    """Prefer the paper page overview; metadata is only a final fallback."""
    explicit = _extract_h2(body, "概要")
    if explicit:
        return explicit
    lead = _extract_lead_blockquote(body)
    if lead:
        return lead
    legacy = _extract_h2(body, "一文要約")
    if legacy:
        return legacy
    return _clean_markdown(fallback_summary)


def _normalize_terms(text: str) -> str:
    for canonical, pattern in TERM_PATTERNS.items():
        preferred = PREFERRED_TERMS[canonical][0].split("／", 1)[0]
        text = pattern.sub(preferred, text)
    return text


def _trim_long_sentence(sentence: str, max_chars: int) -> str:
    if len(sentence) <= max_chars:
        return sentence
    window = sentence[: max_chars - 1]
    candidates = [window.rfind(mark) for mark in ("、", "；", ";", "：", ":")]
    cut = max(candidates)
    if cut >= max(45, max_chars // 2):
        return window[:cut].rstrip("、；;：: ") + "。"
    return sentence[: max_chars - 1].rstrip() + "…"


def _compact(text: str, min_chars: int, max_chars: int) -> str:
    text = _normalize_terms(_clean_markdown(text))
    if not text:
        return ""
    sentences = [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()] or [text]
    chosen: list[str] = []
    for sentence in sentences:
        if not chosen and len(sentence) > max_chars:
            return _trim_long_sentence(sentence, max_chars)
        candidate = "".join(chosen + [sentence])
        if len(candidate) > max_chars:
            break
        chosen.append(sentence)
        if len(candidate) >= min_chars:
            break
    result = "".join(chosen) if chosen else _trim_long_sentence(text, max_chars)
    if len(result) > max_chars:
        result = _trim_long_sentence(result, max_chars)
    if result and result[-1] not in "。！？…":
        result = result + "。" if len(result) < max_chars else result[:-1].rstrip() + "。"
    return result


def compact_list_summary(
    body: str,
    fallback_summary: str = "",
    *,
    min_chars: int = DEFAULT_MIN_CHARS,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    return _compact(extract_summary_source(body, fallback_summary), min_chars, max_chars)


def audit_list_summary(
    text: str,
    *,
    min_chars: int = DEFAULT_MIN_CHARS,
    max_chars: int = DEFAULT_MAX_CHARS,
    min_japanese_ratio: float = DEFAULT_MIN_JAPANESE_RATIO,
    warn_japanese_ratio: float = DEFAULT_WARN_JAPANESE_RATIO,
) -> ListSummaryQuality:
    failures: list[str] = []
    warnings: list[str] = []
    plain = text.strip()
    chars = len(plain)
    if not plain:
        failures.append("一文要約が空")
    if "\n" in text or "\r" in text:
        failures.append("一文要約に改行がある")
    if chars < min_chars:
        failures.append(f"一文要約 {chars}文字 < {min_chars}文字")
    if chars > max_chars:
        failures.append(f"一文要約 {chars}文字 > {max_chars}文字")
    if URL_RE.search(plain):
        failures.append("一文要約にURLが残っている")
    if re.search(r"`|\[[^\]]+\]\([^)]+\)", plain):
        failures.append("一文要約にMarkdown断片が残っている")
    if plain and plain[-1] not in "。！？…":
        failures.append("一文要約が文末記号で終わっていない")

    ratio, _, _ = japanese_ratio(plain)
    if ratio < min_japanese_ratio:
        failures.append(f"日本語比率 {ratio:.1%} < {min_japanese_ratio:.1%}")
    elif ratio < warn_japanese_ratio:
        warnings.append(f"日本語比率 {ratio:.1%} < 警告基準 {warn_japanese_ratio:.1%}")

    bare = find_bare_english(plain)
    if bare:
        preview = ", ".join(f"{hit.term}→{hit.preferred} ×{hit.count}" for hit in bare[:8])
        failures.append(f"日本語化できる英語専門語が裸で残っている: {preview}")

    status = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return ListSummaryQuality(
        status=status,
        char_count=chars,
        japanese_ratio=ratio,
        failures=failures,
        warnings=warnings,
        bare_english_terms=[hit.term for hit in bare],
    )
