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
    "papers/inference/02-adaptive-expert-computation-compression/2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md": [
        (
            "したがって既存Mixtralへruntimeだけ差し込むcache / pruning手法ではなく、**architectureとtraining方法を一緒に変えるadaptive computation**である。",
            "この学習が必要なのは、zero / copy / constantのどれを選べば表現を壊さずFFN計算を省けるかが、トークンと層によって異なるためである。zeroはMoE出力を加えない、copyは入力情報をそのまま残す、constantは入力に依存しない補正を加えるので、三者は同じ『計算しない経路』でも機能が違う。学習時から通常FFNと同じルータ候補へ置くことで、単純なトークンには軽量経路、変換が必要なトークンには通常FFNを割り当てる役割分担をモデル側に形成させる。推論時だけ通常FFNを軽量経路へ置き換える方式では、この役割分担を学んでいないため同じ品質は期待できない。",
        ),
        (
            "そのため軽量expertを選んだtokenは、別GPUへtokenを送ってremote FFNを実行する通信を減らせる可能性がある。",
            "軽量エキスパートは巨大なFFN重みを持たないため、エキスパート並列で通常FFNのようにGPUごとへ分散配置する必要が小さい。各GPUへ複製しておけば、その経路を選んだトークンはローカルでzero / copy / constant処理を完了でき、全対全通信（all-to-all communication）へ参加するトークン数も減らせる。したがってMoE++の利得はFFN FLOPs削減だけではなく、分散MoEで通信と特定FFNへの負荷集中を減らせる点にもある。ただし実際のエンドツーエンド利得は、軽量経路を選ぶ割合と通常FFN側の通信パターンに依存する。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md": [
        (
            "ため、3つを一体で使うことが重要になる。",
            "三要素は同じ転送待ちを別の段階から減らす。RPPは『何が必要になるか』を早めに知らせ、TSは『同じ重みを使うトークンをいつ一緒に処理するか』を変え、ECEは『限られたGPUメモリをどの層のエキスパートへ使うか』を変える。RPPが正しくても各バッチの経路がばらばらなら多数の重みを同時に保持する必要があり、TSだけで経路を揃えても必要重みを直前までCPUに置いたままでは待ち時間が残る。ECEも予測なしでは将来どの層へ容量を貸すべきか判断しにくい。このため三者を直列の独立最適化ではなく、同じ将来ルーティング情報を共有する一つの制御系として扱うことが性能向上の中心になる。",
        ),
        (
            "RPPはnative routerを置き換えず、先読みと実行順調整のhintとして使う。予測ミス時は正しいexpertを追加transferするため品質は変わらない。",
            "したがって予測器の誤りは、モデル出力の誤りではなく資源利用の誤りとして現れる。外れたエキスパートを先に載せればGPUメモリとPCIe帯域を一時的に浪費し、必要なエキスパートを見落とせば正規ルータ判定後の追加転送を待つ。一方で正しいエキスパート計算へフォールバックするため、予測精度が低い条件でも推論結果そのものを近似する必要はない。これは予測ルーティングをそのまま実経路に使う方式と異なり、予測器を速度最適化の補助情報として安全に使える理由である。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md": [
        (
            "浅いblockでは次layer routing予測が不安定なため、最初の4 blockは先行計算を使わずnative gateに従う。\n\nその後だけ予測を有効化する。",
            "浅い層で予測を無理に使わないことは、正確性だけでなく無駄なCPU計算を抑える意味もある。次層予測が外れると、本来使わないCPUエキスパートを先に計算したうえで、正しい経路の計算を改めて行う必要があり、重畳による利得より投機失敗の費用が大きくなる。そこで相関が安定しにくい先頭部分は通常ルーティングへ残し、予測が有効な後段だけでCPU計算をGPU処理の裏へ重ねる。DAOPは全層へ一律に投機を適用するのではなく、予測の当たりやすさが十分な区間だけを高速経路にすることで、誤予測時の追加仕事を制限している。",
        ),
        (
            "論文ではこの仕組みを`Graceful Degradation`と呼ぶが、実際には**遅いCPU expertを一つ省いて、少し品質を犠牲にGPU上のexpertへ置き換える**処理である。",
            "この置換は、CPU実行が間に合わないときにだけ使う遅延上限側の逃げ道である。Top-2の両方をCPUで処理すると二つの大きなFFN計算が直列または資源競合し、GPU側が長く待つ可能性がある。そこで寄与の小さい方を、すでにGPUへ常駐している次善候補へ変えると、新しい重み転送や追加CPU計算なしで層を完了できる。代わりに元ルータが選んだエキスパート集合を変更するため、この経路だけは無損失ではない。したがってDAOPでは通常時の先行計算による無損失な待ち時間削減と、混雑時の品質・遅延交換を分けて評価する必要がある。",
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
