#!/usr/bin/env python3
"""Normalize bare generic English terms in Japanese survey prose.

This is a conservative legacy-repair pass. It does not translate proper method
names, URLs, inline/code-fence content, frontmatter other than list_summary, or
source/reference sections. Replacements are case-sensitive and therefore target
lower-case generic prose terms while preserving capitalized named systems.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import yaml

from japanese_style import PREFERRED_TERMS
from list_summary import LIST_TERM_REPLACEMENTS, audit_list_summary

PAPER_FAMILIES = ("inference", "training", "survey")
EXCLUDED_H2 = {"書誌情報", "一次資料", "参考文献", "References", "更新履歴", "監査メモ"}

EXTRA_REPLACEMENTS = (
    ("compute-bound", "計算律速"),
    ("memory-bound", "メモリ律速"),
    ("load-aware", "負荷認識"),
    ("end-to-end", "エンドツーエンド"),
    ("all-to-all", "全対全通信"),
    ("allreduce", "全削減通信"),
    ("roofline", "ルーフライン"),
    ("parallelism", "並列化"),
    ("microbenchmark", "マイクロベンチマーク"),
    ("optimizer", "最適化器"),
    ("checkpoint", "チェックポイント"),
    ("dependency", "依存関係"),
    ("acceptance", "受理率"),
    ("requirement", "要件"),
    ("collective", "集合通信"),
    ("communication", "通信"),
    ("operator", "演算子"),
    ("hardware", "ハードウェア"),
    ("platform", "基盤"),
    ("efficiency", "効率"),
    ("profiling", "プロファイリング"),
    ("parallel", "並列"),
    ("strategy", "戦略"),
    ("sequence", "系列"),
    ("resource", "資源"),
    ("recovery", "回復"),
    ("failure", "障害"),
    ("objective", "目的関数"),
    ("upstream", "上流"),
    ("downstream", "下流"),
    ("readout", "読み出し"),
    ("message", "メッセージ"),
    ("network", "ネットワーク"),
    ("serving", "推論提供"),
    ("speculative", "投機的"),
    ("decoding", "復号"),
    ("prefill", "プリフィル"),
    ("decode", "デコード"),
    ("draft", "ドラフト"),
    ("target", "対象"),
    ("hidden", "隠れ"),
    ("forward", "順伝播"),
    ("backward", "逆伝播"),
    ("gradient", "勾配"),
    ("training", "学習"),
    ("fine-tuning", "微調整"),
    ("activation", "活性値"),
    ("parameter", "パラメータ"),
    ("model", "モデル"),
    ("memory", "メモリ"),
    ("bandwidth", "帯域"),
    ("weight", "重み"),
    ("token", "トークン"),
    ("tokens", "トークン"),
    ("cache", "キャッシュ"),
    ("batch", "バッチ"),
    ("expert", "専門家"),
    ("pipeline", "パイプライン"),
    ("kernel", "カーネル"),
    ("attention", "注意機構"),
    ("tensor", "テンソル"),
    ("dispatch", "分配"),
    ("combine", "結合"),
    ("throughput", "スループット"),
    ("latency", "遅延"),
    ("overlap", "重畳"),
    ("horizontal", "水平"),
    ("vertical", "垂直"),
    ("split", "分割"),
    ("group", "グループ"),
    ("stage", "段"),
    ("state", "状態"),
    ("local", "局所"),
    ("global", "大域"),
    ("update", "更新"),
    ("bubble", "バブル"),
    ("baseline", "比較対象"),
    ("input", "入力"),
    ("output", "出力"),
    ("dense", "密"),
    ("active", "活性"),
    ("shape", "形状"),
    ("size", "サイズ"),
    ("link", "リンク"),
    ("head", "ヘッド"),
    ("task", "タスク"),
    ("load", "読み込み"),
)


def replacement_pairs() -> list[tuple[str, str]]:
    pairs: dict[str, str] = {}
    for _, (preferred, variants) in PREFERRED_TERMS.items():
        jp = preferred.split("／", 1)[0]
        for variant in variants:
            pairs.setdefault(variant, jp)
    for english, japanese in LIST_TERM_REPLACEMENTS:
        pairs.setdefault(english, japanese)
    for english, japanese in EXTRA_REPLACEMENTS:
        pairs[english] = japanese
    return sorted(pairs.items(), key=lambda item: len(item[0]), reverse=True)


PAIRS = replacement_pairs()


def replace_generic_terms(text: str) -> str:
    placeholders: list[str] = []

    def protect(match: re.Match[str]) -> str:
        placeholders.append(match.group(0))
        return f"\uFFF0{len(placeholders)-1}\uFFF1"

    text = re.sub(r"https?://\S+|\x60[^\x60]*\x60", protect, text)
    for english, japanese in PAIRS:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9]){re.escape(english)}(?![A-Za-z0-9])"
        )
        text = pattern.sub(japanese, text)
    for index, value in enumerate(placeholders):
        text = text.replace(f"\uFFF0{index}\uFFF1", value)
    return text


def split_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---\n"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    return yaml.safe_load(parts[1]) or {}, parts[2]


def render(meta: dict, body: str) -> str:
    front = yaml.safe_dump(
        meta, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000
    ).rstrip()
    return f"---\n{front}\n---{body}"


def normalize_body(body: str) -> str:
    out: list[str] = []
    in_fence = False
    excluded = False
    for line in body.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        newline = line[len(stripped):]
        if re.match(r"^\s*\x60\x60\x60", stripped):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if heading:
            if len(heading.group(1)) == 2:
                title = re.sub(r"[\x60*_~]", "", heading.group(2)).strip()
                excluded = any(title == name or title.startswith(name + " ") for name in EXCLUDED_H2)
            out.append(line)
            continue
        if excluded:
            out.append(line)
            continue
        out.append(replace_generic_terms(stripped) + newline)
    return "".join(out)


def iter_papers(root: Path) -> Iterable[Path]:
    for family in PAPER_FAMILIES:
        base = root / "papers" / family
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.casefold() in {"readme.md", "comparison.md"}:
                continue
            yield path


def normalize_file(path: Path, apply: bool) -> tuple[bool, bool]:
    raw = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw)
    if not meta or body.lstrip().startswith("# Moved"):
        return False, False

    body_new = normalize_body(body)
    body_changed = body_new != body

    list_changed = False
    current = meta.get("list_summary")
    if isinstance(current, str) and current.strip():
        candidate = replace_generic_terms(current)
        old_audit = audit_list_summary(current)
        new_audit = audit_list_summary(candidate)
        if candidate != current and (
            new_audit.japanese_ratio > old_audit.japanese_ratio
            or (old_audit.status == "FAIL" and new_audit.status != "FAIL")
        ):
            meta["list_summary"] = candidate
            list_changed = True

    changed = body_changed or list_changed
    if changed and apply:
        path.write_text(render(meta, body_new), encoding="utf-8")
    return changed, list_changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    changed: list[str] = []
    list_changed: list[str] = []
    for path in iter_papers(root):
        did_change, did_list = normalize_file(path, args.apply)
        if did_change:
            rel = path.relative_to(root).as_posix()
            changed.append(rel)
            if did_list:
                list_changed.append(rel)
    print(f"normalized_paper_prose={len(changed)}")
    print(f"normalized_list_summary={len(list_changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
