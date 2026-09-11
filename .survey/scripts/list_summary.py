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
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]+\)")
URL_RE = re.compile(r"https?://\S+")
HTML_RE = re.compile(r"<[^>]+>")
SENTENCE_RE = re.compile(r"[^。！？]+[。！？]?")
CAMEL_OR_ACRONYM_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Z][A-Z0-9_-]{1,}|[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)(?:-[A-Za-z0-9]+)*(?![A-Za-z0-9])"
)
TITLECASE_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*(?![A-Za-z0-9])"
)
MULTIWORD_TITLECASE_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*(?:\s+[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*)+(?![A-Za-z0-9])"
)

METHOD_SIGNAL_RE = re.compile(
    r"(?:提案|手法|方式|機構|システム|設計|スケジューラ|アルゴリズム|"
    r"予測して|予測し|配置して|配置し|選択して|選択し|割り当て|切り替え|"
    r"先読み|オフロード|退避|圧縮|量子化|枝刈り|再計算|分離|統合|調整し|"
    r"動的に[^。！？]{0,30}(?:変え|変更|決め|選ぶ|配置)|することで|によって[^。！？]{0,40}(?:減ら|抑え|改善))"
)
RESULT_SIGNAL_RE = re.compile(
    r"(?:評価|実験|測定|比較|解析|分析|検証|ベンチマーク|結果)[^。！？]{0,90}"
    r"(?:示した|確認した|分かった|達成|短縮|削減|低減|改善|向上|高速化|上回|維持|同等|支配的|逆転)"
    r"|(?:\d+(?:\.\d+)?\s*(?:%|％|倍|x|×|ms|秒|GB|MB|TB|W|J|トークン/秒|tokens?/s))",
    re.I,
)
PROBLEM_SIGNAL_RE = re.compile(
    r"(?:問題|課題|ボトルネック|不足|制約|限られ|待ち時間|遅延|帯域|メモリ|転送|競合|再計算|負荷|難しい|高コスト)"
)

LIST_TERM_REPLACEMENTS = (
    ("self-speculative decoding", "自己投機的復号"),
    ("speculative decoding", "投機的復号"),
    ("adaptive verification", "適応的検証"),
    ("expert weight load", "専門家重みの読み込み"),
    ("verification cost", "検証コスト"),
    ("storage architecture", "ストレージ構成"),
    ("storage cost", "保存コスト"),
    ("model parameter", "モデルパラメータ"),
    ("optimizer state", "オプティマイザ状態"),
    ("update matrix", "更新行列"),
    ("system benchmark", "システムベンチマーク"),
    ("long-context chatbot", "長文脈チャットボット"),
    ("few-shot prompt", "少数例プロンプト"),
    ("draft branch", "下書き分岐"),
    ("draft tree", "下書き木"),
    ("draft model", "下書きモデル"),
    ("target model", "対象モデル"),
    ("full model", "完全なモデル"),
    ("all-to-all", "全対全"),
    ("fine-tuning", "微調整"),
    ("training-free", "学習不要"),
    ("depth decay", "深度減衰"),
    ("self-consistency", "自己整合性"),
    ("self-ensemble", "自己アンサンブル"),
    ("consumer gpu", "民生GPU"),
    ("dnn training", "DNN学習"),
    ("bp-free", "逆伝播不要"),
    ("self-speculative", "自己投機的"),
    ("verification", "検証"),
    ("chatbot", "チャットボット"),
    ("few-shot", "少数例"),
    ("training", "学習"),
    ("forward", "順伝播"),
    ("backward", "逆伝播"),
    ("gradient", "勾配"),
    ("parameter", "パラメータ"),
    ("momentum", "モーメンタム"),
    ("variance", "分散"),
    ("dispatch", "分配"),
    ("combine", "結合"),
    ("tensor", "テンソル"),
    ("communication", "通信"),
    ("architecture", "構成"),
    ("compiler", "コンパイラ"),
    ("consumer", "民生"),
    ("freezing", "凍結"),
    ("storage", "ストレージ"),
    ("memory", "メモリ"),
    ("system", "システム"),
    ("benchmark", "ベンチマーク"),
    ("toolkit", "ツールキット"),
    ("framework", "フレームワーク"),
    ("sample", "サンプル"),
    ("prompt", "プロンプト"),
    ("weight", "重み"),
    ("load", "読み込み"),
    ("model", "モデル"),
    ("draft", "下書き"),
    ("expert", "専門家"),
    ("cost", "コスト"),
    ("code", "コード"),
    ("layer", "層"),
    ("attention", "注意機構"),
    ("speculative", "投機的"),
    ("adaptive", "適応的"),
)
LIST_TERM_PATTERNS = tuple(
    (
        term,
        replacement,
        re.compile(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", re.I),
    )
    for term, replacement in sorted(LIST_TERM_REPLACEMENTS, key=lambda x: len(x[0]), reverse=True)
)


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
    """Prefer the worker-authored lead summary; use overview compaction only for legacy pages."""
    lead = _extract_lead_blockquote(body)
    if lead:
        return lead
    explicit = _extract_h2(body, "概要")
    if explicit:
        return explicit
    legacy = _extract_h2(body, "一文要約")
    if legacy:
        return legacy
    return _clean_markdown(fallback_summary)


def _title_method_names(body: str) -> list[str]:
    match = H1_RE.search(body)
    if not match:
        return []
    title = _clean_markdown(match.group(1))
    names: list[str] = []
    if ":" in title or "：" in title:
        prefix = re.split(r"[:：]", title, maxsplit=1)[0].strip()
        if 1 <= len(prefix.split()) <= 4 and re.search(r"[A-Za-z]", prefix):
            names.append(prefix)
    for token in CAMEL_OR_ACRONYM_RE.findall(title):
        names.append(token)
    return list(dict.fromkeys(names))


def _replace_list_terms(text: str) -> str:
    for _, replacement, pattern in LIST_TERM_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _is_generic_english(text: str) -> bool:
    if find_bare_english(text):
        return True
    return any(pattern.fullmatch(text) for _, _, pattern in LIST_TERM_PATTERNS)


def _proper_name_candidates(text: str, explicit_names: tuple[str, ...] = ()) -> list[str]:
    candidates: list[str] = [name for name in explicit_names if name and name in text]
    for match in MULTIWORD_TITLECASE_RE.finditer(text):
        phrase = match.group(0)
        first = phrase.split()[0]
        if not _is_generic_english(first):
            candidates.append(phrase)
    for match in CAMEL_OR_ACRONYM_RE.finditer(text):
        candidates.append(match.group(0))
    for match in TITLECASE_RE.finditer(text):
        token = match.group(0)
        if not _is_generic_english(token):
            candidates.append(token)
    return sorted(set(candidates), key=len, reverse=True)


def _protect_proper_names(text: str, explicit_names: tuple[str, ...] = ()) -> tuple[str, list[tuple[str, str]]]:
    protected: list[tuple[str, str]] = []
    for value in _proper_name_candidates(text, explicit_names):
        placeholder = f"固有名詞{len(protected)}号"
        pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(value)}(?![A-Za-z0-9])")
        updated, count = pattern.subn(placeholder, text)
        if count:
            protected.append((placeholder, value))
            text = updated
    return text, protected


def _restore_proper_names(text: str, protected: list[tuple[str, str]]) -> str:
    for placeholder, value in protected:
        text = text.replace(placeholder, value)
    return text


def _mask_proper_names(text: str) -> str:
    masked, protected = _protect_proper_names(text)
    for placeholder, _ in protected:
        masked = masked.replace(placeholder, " ")
    return re.sub(r"\s+", " ", masked).strip()


def _normalize_terms(text: str, explicit_names: tuple[str, ...] = ()) -> str:
    text = _replace_list_terms(text)
    text, protected = _protect_proper_names(text, explicit_names)
    for canonical, pattern in TERM_PATTERNS.items():
        preferred = PREFERRED_TERMS[canonical][0].split("／", 1)[0]
        text = pattern.sub(preferred, text)
    return _restore_proper_names(text, protected)


def _trim_long_sentence(sentence: str, max_chars: int) -> str:
    if len(sentence) <= max_chars:
        return sentence
    window = sentence[: max_chars - 1]
    candidates = [window.rfind(mark) for mark in ("、", "；", ";", "：", ":")]
    cut = max(candidates)
    if cut >= max(45, max_chars // 2):
        return window[:cut].rstrip("、；;：: ") + "…"
    return sentence[: max_chars - 1].rstrip() + "…"


def _find_sentence(sentences: list[str], pattern: re.Pattern[str], *, start: int = 0) -> int | None:
    for index in range(start, len(sentences)):
        if pattern.search(sentences[index]):
            return index
    return None


def _semantic_sentence_order(sentences: list[str]) -> list[int]:
    """Legacy fallback: reserve budget for the method, then add problem/result if they fit."""
    method = _find_sentence(sentences, METHOD_SIGNAL_RE)
    if method is None:
        return list(range(len(sentences)))

    problem: int | None = None
    for index in range(method + 1):
        if index != method and PROBLEM_SIGNAL_RE.search(sentences[index]):
            problem = index
            break

    result = _find_sentence(sentences, RESULT_SIGNAL_RE, start=method + 1)
    selected = [method]
    if problem is not None:
        selected.append(problem)
    if result is not None:
        selected.append(result)
    selected_set = set(selected)
    selected.extend(index for index in range(len(sentences)) if index not in selected_set)
    return selected


def _compact(
    text: str,
    min_chars: int,
    max_chars: int,
    explicit_names: tuple[str, ...] = (),
) -> str:
    text = _normalize_terms(_clean_markdown(text), explicit_names)
    if not text:
        return ""
    sentences = [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()] or [text]
    order = _semantic_sentence_order(sentences)
    chosen_indices: list[int] = []

    for index in order:
        sentence = sentences[index]
        if not chosen_indices and len(sentence) > max_chars:
            return _trim_long_sentence(sentence, max_chars)
        candidate_indices = sorted(chosen_indices + [index])
        candidate = "".join(sentences[i] for i in candidate_indices)
        if len(candidate) > max_chars:
            continue
        chosen_indices.append(index)

        chosen_text = "".join(sentences[i] for i in sorted(chosen_indices))
        has_method = any(METHOD_SIGNAL_RE.search(sentences[i]) for i in chosen_indices)
        if len(chosen_text) >= min_chars and has_method:
            result_index = _find_sentence(sentences, RESULT_SIGNAL_RE)
            if result_index is None or result_index in chosen_indices:
                break
            with_result = "".join(sentences[i] for i in sorted(set(chosen_indices + [result_index])))
            if len(with_result) > max_chars:
                break

    if not chosen_indices:
        result = _trim_long_sentence(text, max_chars)
    else:
        result = "".join(sentences[i] for i in sorted(chosen_indices))

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
    source = extract_summary_source(body, fallback_summary)
    return _compact(source, min_chars, max_chars, tuple(_title_method_names(body)))


def _list_specific_bare_terms(text: str) -> list[str]:
    return [term for term, _, pattern in LIST_TERM_PATTERNS if pattern.search(text)]


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

    audit_text = _mask_proper_names(plain)
    ratio, _, _ = japanese_ratio(audit_text)
    if ratio < min_japanese_ratio:
        failures.append(f"日本語比率 {ratio:.1%} < {min_japanese_ratio:.1%}")
    elif ratio < warn_japanese_ratio:
        warnings.append(f"日本語比率 {ratio:.1%} < 警告基準 {warn_japanese_ratio:.1%}")

    shared_hits = find_bare_english(audit_text)
    list_hits = _list_specific_bare_terms(audit_text)
    if shared_hits or list_hits:
        preview_parts = [f"{hit.term}→{hit.preferred} ×{hit.count}" for hit in shared_hits[:8]]
        preview_parts.extend(list_hits[:8 - len(preview_parts)])
        failures.append("日本語化できる英語専門語が裸で残っている: " + ", ".join(preview_parts))

    status = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return ListSummaryQuality(
        status=status,
        char_count=chars,
        japanese_ratio=ratio,
        failures=failures,
        warnings=warnings,
        bare_english_terms=[hit.term for hit in shared_hits] + list_hits,
    )
