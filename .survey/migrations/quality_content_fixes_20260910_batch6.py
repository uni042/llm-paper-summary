#!/usr/bin/env python3
"""Sixth content-only batch: repair batch5 heading and start oldest 2025 papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return False
        raise RuntimeError(f"anchor not found: {path}\n{old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def append_after(path: Path, anchor: str, addition: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if addition in text:
        return False
    if anchor not in text:
        raise RuntimeError(f"anchor not found: {path}\n{anchor}")
    path.write_text(text.replace(anchor, anchor + "\n\n" + addition, 1), encoding="utf-8")
    return True


def mark_audited(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace('last_audited: null', 'last_audited: "2026-09-10"', 1)
    text = text.replace('audit_version: 0', 'audit_version: 1', 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    changed = 0

    # batch5 inserted the H3 title twice. Collapse it back to one title while
    # keeping the explanatory paragraph that follows it.
    mc = ROOT / "papers/inference/06-moe-quantization-compression/2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md"
    duplicated = "### 3. 二つの圧縮率は意味が違う\n\n### 3. 二つの圧縮率は意味が違う"
    if duplicated in mc.read_text(encoding="utf-8"):
        replace_once(mc, duplicated, "### 3. 二つの圧縮率は意味が違う")
        mark_audited(mc)
        changed += 1

    chiron = ROOT / "papers/inference/11-llm-serving-scheduling-disaggregation/2025-2501.08090-chiron-hierarchical-autoscaling.md"
    if append_after(
        chiron,
        "Chironはresource調整を、**すぐ変えられるlocal control**と**反応が遅いglobal control**の二段階へ分ける。",
        "二段階に分ける理由は、操作ごとの反応時間が大きく違うからである。1 GPU内の同時処理数は次のbatchから変えられる一方、新しいGPU instanceはmodel loadや初期化を伴うため即座には増やせない。短いtraffic変動をinstance増減だけで追うと、追加GPUが使える頃にはburstが終わっている可能性がある。そこでlocal controlを高速な一次応答、global controlを持続的なcapacity不足へ対処する二次応答として使い分ける。",
    ):
        mark_audited(chiron)
        changed += 1

    dlpm = ROOT / "papers/inference/11-llm-serving-scheduling-disaggregation/2025-2501.14312-locality-aware-fair-scheduling-dlpm.md"
    if append_after(
        dlpm,
        "これによりKV再利用を増やしつつ、特定クライアントが無制限に先行するのを防ぐ。",
        "ここで公平性の許容幅を明示的に持つことが重要である。prefix局所性だけを見れば、同じ長いprefixを繰り返すclientを連続処理するほど効率は上がるが、そのままでは別clientの待ち時間に上限がない。DLPMはまずservice deficitで『今このclientを追加で進めても公平性の境界内か』を判定し、その候補集合の中だけでprefix matchを最大化する。この順序により、局所性最適化が公平性制約を上書きしない。",
    ):
        mark_audited(dlpm)
        changed += 1

    print(f"content-quality batch6: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
