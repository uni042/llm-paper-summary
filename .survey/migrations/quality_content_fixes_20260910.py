#!/usr/bin/env python3
"""Idempotent content-only fixes for summaries selected by the quality audit.

This migration intentionally does not perform terminology/Japanese-ratio cleanup.
It only inserts missing explanatory prose needed to understand the mechanisms.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/01-offload-hierarchical-memory/2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md": [
        (
            "model全体はVRAMに収まらなくても、ある瞬間の計算で本当に必要なtensorはmodel sizeよりはるかに小さい。TwinPilotsは残ったVRAMへ再利用価値の高いweightやKV dataを保持し、不要なtransferを減らす。",
            "このキャッシュ領域が効くのは、直後の層や次の生成反復で同じ重み・KV状態を再利用できる場合である。CPUで計算する処理を増やしてGPUへ送る重みを減らしても、GPU側に残したデータがすぐ追い出されればPCIe転送は再発する。そこで計算に必須な作業領域を確保した残りだけを再利用用へ回し、保持できたデータについては次回のCPU→GPU転送を丸ごと省く。つまりTwinPilotsのGPUメモリ利用は、単なる容量不足対策ではなく、CPU実行で削った転送量とGPU側再利用を組み合わせて転送待ちをさらに減らす役割を持つ。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md": [
        (
            "両方を併用できるが、skipを追加するほどquality trade-offも増える。",
            "二つを併用したときは誤差の入り方も異なる。恒久的なエキスパート削除は、以後すべての入力で選択可能な候補集合そのものを狭めるため、較正データ（calibration data）と実運用入力の分布がずれると回復できない。一方、動的スキップは重みを残したまま、そのトークンで第2エキスパートの寄与が小さいと判断したときだけ計算を省く。そのため後者だけなら別トークンでは同じエキスパートを再び使える。併用時には、まず削減済み候補から上位2個を選び、その第2候補をさらに省くので近似が重なる。速度だけでなく、削除率・スキップ閾値・較正領域を一組の運用設定として評価する必要がある。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md": [
        (
            "そのため理論FLOPsが同じでもwall-clockが必ず速いわけではなく、XMoE自身もexpert粒度の選択を課題として挙げる。",
            "細粒度化の利得が実時間へつながるには、選ばれた小エキスパートへトークンをまとめ、十分大きな行列積として実行できることも必要になる。閾値ルーティングではトークンごとに選択数が異なるため、あるエキスパートには多数のトークン、別のエキスパートには数個しか来ない状況が生じる。後者を小さなGPUカーネルとして個別実行すると、演算量を減らしても起動固定費やメモリアクセス効率の悪化が支配的になり得る。したがってXMoEの計算量削減は、細かい計算単位を効率よく束ねる実行系と組み合わせて初めて、同程度の壁時計時間（wall-clock time）削減として現れる。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md": [
        (
            "論文は主にload / FLOPsを報告し、optimized inference kernelでのend-to-end speedupは示していない。",
            "可変計算量になる理由は、通常エキスパートの上位順位を直接打ち切るのではなく、ルータ自身に『この選択枠は計算しなくてよい』というnullエキスパートを選ばせる点にある。簡単なトークンでは複数のnullがTop-kへ入り、難しいトークンでは通常エキスパートが多く残るので、同じTop-kインターフェースのまま実FFN数だけが変わる。補助損失は平均null利用量を制御するが、個々のトークンに同じnull数を強制しないため、このばらつきが残る。逆に補助損失が強すぎれば全トークンの構成が似通い、弱すぎればnullへ過度に集中し得るため、計算予算と品質の両方を学習時に調整する必要がある。",
        ),
    ],
}


def apply_patch(path: Path, anchor: str, addition: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if addition in text:
        return False
    if anchor not in text:
        raise RuntimeError(f"anchor not found: {path}\n{anchor}")
    text = text.replace(anchor, anchor + "\n\n" + addition, 1)
    path.write_text(text, encoding="utf-8")
    return True


def mark_audited(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace('last_audited: null', 'last_audited: "2026-09-10"', 1)
    text = text.replace('audit_version: 0', 'audit_version: 1', 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    changed = 0
    for rel, patches in PATCHES.items():
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(path)
        paper_changed = False
        for anchor, addition in patches:
            paper_changed |= apply_patch(path, anchor, addition)
        if paper_changed:
            mark_audited(path)
            changed += 1
    print(f"content-quality migration: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
