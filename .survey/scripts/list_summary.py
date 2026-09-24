#!/usr/bin/env python3
"""Audit explicit Japanese one-line summaries used in paper indexes."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from japanese_style import (
    DEFAULT_MIN_JAPANESE_RATIO,
    DEFAULT_WARN_JAPANESE_RATIO,
    find_bare_english,
    japanese_ratio,
)

DEFAULT_MIN_CHARS = 45
DEFAULT_MAX_CHARS = 180
URL_RE = re.compile(r"https?://\\S+")
CAMEL_OR_ACRONYM_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Z][A-Z0-9_-]{1,}|[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)(?:-[A-Za-z0-9]+)*(?![A-Za-z0-9])"
)
TITLECASE_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*(?![A-Za-z0-9])"
)
MULTIWORD_TITLECASE_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*(?:\s+[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*)+(?![A-Za-z0-9])"
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


