#!/usr/bin/env python3
"""Shared Japanese-first prose policy for survey paper summaries."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

DEFAULT_MIN_JAPANESE_RATIO = 0.70
DEFAULT_WARN_JAPANESE_RATIO = 0.80

# English prose terms that should normally be written in Japanese or katakana.
# English is allowed in code/URLs, proper names/acronyms, and the first
# parenthetical formal-name annotation after a Japanese explanation.
PREFERRED_TERMS: dict[str, tuple[str, tuple[str, ...]]] = {
    "request": ("リクエスト／要求", ("request", "requests", "request-wise")),
    "token": ("トークン", ("token", "tokens", "token-level", "per-token")),
    "layer": ("層／レイヤー", ("layer", "layers", "layer-wise", "per-layer")),
    "batch": ("バッチ", ("batch", "batches")),
    "decode": ("デコード", ("decode", "decoding")),
    "prefill": ("プリフィル／入力処理", ("prefill",)),
    "offload": ("オフロード／退避", ("offload", "offloading", "offloaded")),
    "cache": ("キャッシュ", ("cache", "caching")),
    "prefetch": ("プリフェッチ／先読み", ("prefetch", "prefetching")),
    "eviction": ("追い出し", ("eviction", "evict", "evicted")),
    "scheduler": ("スケジューラ", ("scheduler", "scheduling")),
    "placement": ("配置", ("placement",)),
    "runtime": ("ランタイム／実行時", ("runtime",)),
    "latency": ("遅延", ("latency", "latencies")),
    "throughput": ("スループット", ("throughput",)),
    "bandwidth": ("帯域", ("bandwidth",)),
    "memory": ("メモリ", ("memory",)),
    "stream": ("ストリーム", ("stream", "streams")),
    "buffer": ("バッファ", ("buffer", "buffers")),
    "solver": ("ソルバー／最適化器", ("solver",)),
    "pipeline": ("パイプライン", ("pipeline",)),
    "routing": ("ルーティング", ("routing", "router")),
    "expert": ("エキスパート／専門家", ("expert", "experts")),
    "kernel": ("カーネル", ("kernel", "kernels")),
    "fusion": ("融合", ("fusion",)),
    "quantization": ("量子化", ("quantization", "quantized")),
    "pruning": ("枝刈り", ("pruning", "pruned")),
    "activation": ("活性値", ("activation", "activations")),
    "weight": ("重み", ("weight", "weights")),
    "benchmark": ("ベンチマーク", ("benchmark", "benchmarks")),
    "baseline": ("比較対象", ("baseline", "baselines")),
    "trace": ("トレース", ("trace", "traces")),
    "workload": ("ワークロード", ("workload", "workloads")),
    "bottleneck": ("ボトルネック", ("bottleneck", "bottlenecks")),
    "overhead": ("オーバーヘッド", ("overhead",)),
    "speedup": ("高速化倍率", ("speedup",)),
    "goodput": ("有効スループット", ("goodput",)),
    "stall": ("待ち／停止", ("stall", "stalls", "stalled")),
    "lossless": ("無損失", ("lossless",)),
    "synthetic": ("合成", ("synthetic",)),
    "adaptive": ("適応型", ("adaptive",)),
    "dynamic": ("動的", ("dynamic",)),
    "static": ("静的", ("static",)),
    "host": ("ホスト", ("host",)),
    "resident": ("常駐", ("resident",)),
    "infeasible": ("実行不能", ("infeasible",)),
    "end-to-end": ("エンドツーエンド", ("end-to-end",)),
    "component": ("構成要素", ("component", "components")),
    "condition": ("条件", ("condition", "conditions")),
    "metric": ("指標", ("metric", "metrics")),
    "simulation": ("シミュレーション", ("simulation", "simulated")),
}

JP_CLASS = r"\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff々〆ヶ"
JP_RE = re.compile(f"[{JP_CLASS}]")
LATIN_RE = re.compile(r"[A-Za-z]")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MD_LINK_DEST_RE = re.compile(r"\]\((?:https?://|[^)]*/)[^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z][A-Z0-9.+/-]{1,15}(?![A-Za-z0-9])")
MODELISH_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Za-z]*\d+[A-Za-z0-9.+/-]*|"
    r"[A-Z][A-Za-z0-9-]*[A-Z][A-Za-z0-9-]*)(?![A-Za-z0-9])"
)


def _term_patterns() -> dict[str, re.Pattern[str]]:
    out: dict[str, re.Pattern[str]] = {}
    for canonical, (_, variants) in PREFERRED_TERMS.items():
        alt = "|".join(re.escape(v) for v in sorted(variants, key=len, reverse=True))
        out[canonical] = re.compile(
            rf"(?<![A-Za-z0-9])(?:{alt})(?![A-Za-z0-9])", re.I
        )
    return out


TERM_PATTERNS = _term_patterns()


@dataclass(frozen=True)
class BareEnglishHit:
    term: str
    preferred: str
    count: int


def clean_for_language_ratio(text: str) -> str:
    text = URL_RE.sub(" ", text)
    text = MD_LINK_DEST_RE.sub("]", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = re.sub(rf"(?<=[{JP_CLASS}])（[^（）]*）", " ", text)
    text = re.sub(rf"(?<=[{JP_CLASS}])\([^()]*\)", " ", text)
    text = ACRONYM_RE.sub(" ", text)
    text = MODELISH_RE.sub(" ", text)
    return text


def japanese_ratio(text: str) -> tuple[float, int, int]:
    cleaned = clean_for_language_ratio(text)
    jp = len(JP_RE.findall(cleaned))
    latin = len(LATIN_RE.findall(cleaned))
    denom = jp + latin
    return (jp / denom if denom else 1.0), jp, latin


def find_bare_english(text: str) -> list[BareEnglishHit]:
    cleaned = clean_for_language_ratio(text)
    hits: list[BareEnglishHit] = []
    for canonical, pattern in TERM_PATTERNS.items():
        count = len(pattern.findall(cleaned))
        if count:
            hits.append(BareEnglishHit(canonical, PREFERRED_TERMS[canonical][0], count))
    return sorted(hits, key=lambda x: (-x.count, x.term))


def iter_prose_strings(value: Any) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        if value.strip():
            yield value
        return
    if isinstance(value, list):
        for item in value:
            yield from iter_prose_strings(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {
                "canonical_id", "arxiv_id", "doi", "openreview_id", "source", "sources",
                "code", "paper_path", "attempt_id", "job_id", "published",
            }:
                continue
            yield from iter_prose_strings(item)


def record_prose_text(record: dict[str, Any]) -> str:
    chunks: list[str] = []
    meta = record.get("metadata") or {}
    for key in ("summary", "overview", "hardware_details", "quality_effect"):
        chunks.extend(iter_prose_strings(meta.get(key)))
    for section in ("problem_method", "evaluation", "results", "positioning"):
        chunks.extend(iter_prose_strings(record.get(section) or {}))
    return "\n".join(chunks)
