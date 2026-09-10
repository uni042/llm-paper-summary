#!/usr/bin/env python3
"""Eighth content-only batch: finish residual Feb-Mar gaps and expand Apr-May 2025."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/99-other-inference-systems/2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md": [
        (
            "したがって、どのhardware・shapeでも同じ固定設定を使えるkernelではない。",
            "また通信路がNVLink中心かPCIe bridgeを跨ぐかでもcommunication側の必要資源が変わるため、別clusterへ移植するときは同じmodelでもprofileを取り直す必要がある。",
        ),
    ],
    "papers/inference/04-conditional-computation/2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md": [
        (
            "D3は、**layer skippingで理論計算量の削減がそのままGPU速度にならない理由まで実測した研究**として重要である。",
            "この差はD³の評価を読むうえで重要である。layerを飛ばしてFLOPsが減っても、tokenごとに実行layer数が変われば通常の固定depth Transformerほど大きな連続kernelへまとめにくい。さらにKV整合性を保つcopyや条件分岐が残るため、algorithm上の省計算量とruntimeの実時間短縮量は別指標として扱う必要がある。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md": [
        (
            "ここから、DynaMoの利点は「常に動的にbitを変えること」ではなく、**dataset変化へ対応するためにモデル全体を再量子化し直さなくてよい**ことにある。",
            "逆に、一つの固定domainだけを長期間処理するdeploymentではcross-dataset切替機構の価値は小さく、通常の静的mixed precisionでも十分な場合がある。DynaMoは入力分布が切り替わるservingで、再較正costと追加FP16 cacheを払って適応性を得る設計である。",
        ),
    ],
    "papers/inference/08-edge-on-device-llm-systems/2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md": [
        (
            "論文ではこの入れ子構造を `nested residual` と呼ぶ。狙いは、**複数precisionを切り替えられる状態を保ちながら保存量とSSD I/Oを三重化しないこと**である。",
            "例えばINT4版を完全copyとして別保存すると、INT2で十分なtokenでもINT4全体を読み込むか、precisionごとに重複weightを持つ必要がある。MWQではまず共通する低bit部分だけを読み、必要なtokenでだけ追加bitを足してINT3/4へ拡張できる。そのためprecisionを上げるcostも『別expert全体を読み直す』のではなく追加residual分のI/Oとして表現でき、bit-width routerの動的判断をstorage側で実現しやすい。",
        ),
        (
            "RTX 3060のようなPCIe＋SSD構成と、Jetsonの共有memory構成では最適なprecisionや転送量が違うため、**同じpolicyを全deviceへ固定しない**。",
            "profiling結果は、どのexpert-bitを先にloadすればGPU計算とI/Oの終了時刻を近づけられるかを決める材料になる。SSD読出しが遅いdeviceでは低bit化でtransfer byteを減らす価値が高く、計算が相対的に遅いdeviceでは追加bitを読み込んでもそのI/Oを現在のGEMM裏へ隠せる場合がある。つまりprecisionは品質だけでなく、その端末のI/O時間とcompute時間の比率を変えるschedule変数でもある。",
        ),
        (
            "### 3. DeviceごとにSSD読込時間と計算時間を実測する",
            "### 3. DeviceごとにSSD読込時間と計算時間を実測する\n\nこの実測は単なるbenchmark表作成ではなく、後段のruntime schedulerが使うcost modelになる。各precisionについてload時間とcompute時間が分かれば、現在expertの計算が終わるまでに次expertのどのbitまで先読みできるかを見積もれる。余分な高bit residualを読んで品質を上げてもpipelineを止めない条件と、低bitへ落とさないとI/O bubbleが生じる条件をdeviceごとに区別できる。",
        ),
        (
            "memoryに余裕があるならhot expertを高bitで保持し、厳しいときは低bit版だけを残すため、**expert単位ではなくbit単位でmemory budgetを配れる**。",
            "この粒度なら『expert Aを残すか捨てるか』の二択より柔軟である。頻出expertはINT2のbaseを常駐させ、追加bitだけ必要に応じて保持すれば、最低限のhit率を確保しながら空きmemoryを品質改善へ使える。逆に低頻度expertへ高bit residualを常駐させると、ほとんど使わないbyteが貴重なedge memoryを占有するため、HEBFは利用頻度とprecisionの両方をcache価値へ反映する。",
        ),
    ],
    "papers/inference/04-conditional-computation/2025-2504.15895-dynamic-early-exit-in-reasoning-models.md": [
        (
            "追加学習や別verifierを必要とせず、既存reasoning modelの出力制御だけで成立する。",
            "重要なのは、DEERがreasoning途中のhidden stateから正誤を直接分類する別modelを作らない点である。同じreasoning model自身に『今ここでfinal answerを要求したら何を答え、どの程度確信しているか』を問い合わせる。そのため新しいcheckpointは不要だが、model自身のconfidence calibrationが悪ければ誤ったtrial answerにも高い確率を与え、早期終了してしまう。この自己評価能力が手法の主要な成立条件になる。",
        ),
        (
            "ここで生成される答えは最終確定ではなく、**「今止めても十分答えられるか」を測る試行回答**として使う。",
            "trialを毎reasoning tokenで行わずtransition pointだけに限定するのは、確認自体にもgeneration costがあるためである。まだ途中である可能性が高い地点で何度もfinal answerを生成すると、削減したCoTよりtrial側の追加tokenが多くなり得る。『考え直しへ移る兆候』のある地点だけを候補にすることで、すでに解法がまとまっている可能性が高い場所へ確認計算を集中する。",
        ),
        (
            "これにより「試しに答えを出したこと」が後続CoTへ影響しないようにする。",
            "rollbackが必要なのは、低confidence trialをhistoryへ残すとmodelがその仮回答を前提に次のreasoningを続け、元の推論軌道を変えてしまうためである。trialは判定専用のbranchとして扱い、reject時にはそのbranchのKVも破棄して、分岐前のKV cacheから本線を再開する。したがって失敗したearly-exit判定は主に余分な計算costとなり、reasoning内容そのものへ混入しにくい。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md": [
        (
            "MoEQuantではこれを `inter-expert imbalance` と呼ぶ。GPTQなどはexpertへ実際に入ったtokenから「どの重みを変えると出力誤差が増えやすいか」を推定するため、sample数が極端に少ないexpertでは量子化補正が不安定になる。",
            "これはdense modelのcalibrationと違う点である。dense FFNならcalibration tokenのほぼ全てが同じweightを通るが、MoEではrouterがtokenを分散するため、全体で数千token用意しても特定expertには数十tokenしか届かないことがある。その少数例だけでHessianやactivation rangeを推定すると、本番で別種類のtokenがそのexpertへ来たときに量子化誤差が急増し得る。したがってcalibration set全体の大きさより、各expertが十分多様な入力を実際に受け取ったかが重要になる。",
        ),
        (
            "全語彙から全ての続きを試すと候補数が急増するため、**次token確率が高い少数候補だけを残して探索を続ける**。論文ではこの絞り込みを `probability-guided path pruning` と呼ぶ。",
            "この探索は『低頻度expertを使わせるためなら不自然なtoken列でもよい』とはしない。model確率の高いbranchを優先することで、元modelが実際に生成し得る系列の範囲を保ち、その中でexpert利用分布が均されるpathを選ぶ。結果としてrare expertのcalibration sampleを増やしつつ、実運用から大きく外れた人工入力だけで量子化parameterを決める危険を抑える。",
        ),
        (
            "これにより、**そのexpertが本来重要視している入力で量子化誤差を小さくする**。",
            "router scoreを重みとして使うのは、同じexpertへrouteされたという事実だけでは最終出力への寄与量が同じとは限らないためである。Top-k末尾で小さなweightを与えられたtokenの再構成誤差を、routerがほぼ主担当として選んだtokenと同じ重さで最小化すると、量子化budgetを重要度の低い入力へ使ってしまう。AGQはrouting affinityをcalibration lossへ入れ、expert出力が最終token表現へ強く混ざるsampleを優先して保護する。",
        ),
        (
            "MoEQuant++ではさらに、重みの極端に大きい値が特定方向へ偏らないよう、**量子化前に重みを回転させて値の分布を均しやすくする変換**も使う。",
            "この回転はexpert routingを変える操作ではなく、同じ線形変換を低bitで表現しやすい数値分布へ写す前処理である。外れ値が一部channelへ集中したまま低bit化するとscaleを大きく取る必要があり、通常値に使える量子化段階が粗くなる。値を複数channelへ分散させれば同じbit数でもrounding errorを抑えやすくなり、EBSS/AGQで改善したcalibration情報をさらに低bit表現へ反映しやすくする。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md": [
        (
            "ここで `W4A16` はweight 4 bit / activation 16 bitを意味する。つまりMxMoEは、**weight bitだけでなくactivation precisionも選択肢に含める**。",
            "この粒度が効くのは、同じexpertの3つのprojectionでも出力誤差への感度とruntime上の律速が異なるからである。あるmatrixは4 bitへ落としても誤差が小さい一方、別matrixは同じbit幅で大きく品質を落とす場合がある。expert全体へ一つのprecisionを与えると、敏感なmatrixに合わせて全体を高bitにするか、鈍感なmatrixまで含めて低bit化するかの二択になる。linear-block単位なら高精度を必要な場所だけへ残せる。",
        ),
        (
            "これにより、単純な「bit数が低いほど速い」という仮定を置かず、**そのhardwareでその行列サイズを実行した実時間**をcostとして使う。",
            "低bitほど常に高速とは限らない理由は、GPU kernelの効率がmatrix shapeとprecisionに依存するためである。token数が少ない小GEMMではpacking / dequantizationやkernel起動の固定費が支配し、理論演算量が減っても速くならない場合がある。逆に大きなGEMMでは低bit Tensor Coreのthroughput利得が出やすい。routingから実際のexpert token数を再現して測ることで、このshape依存性をprecision選択へ入れる。",
        ),
        (
            "論文ではこの組み合わせ問題を整数線形計画（ILP）として解く。係数 `r` により品質を重く見るか速度を重く見るかを調整でき、通常設定はr=0.75で品質をやや重く見る。",
            "したがってMxMoEが求めるのは単一の『最良bit配置』ではなく、memory budgetと品質・latencyの重み付けごとに異なるoperating pointである。GPU memoryが厳しければ低bit候補を増やし、品質制約が厳しければ感度の高いblockを高bitへ戻す。hardwareを変更してprofile時間が変われば同じaccuracy sensitivityでも最適配置が変わるため、algorithm側の誤差情報とsystem側の実時間情報を再度組み合わせて解く必要がある。",
        ),
        (
            "このkernelまで含める点が、bit配置だけを提案するmixed-precision研究との大きな違いになる。",
            "mixed precisionでは、異なるbit-widthのGEMMを別々に順番実行すると、小さいexpertごとにkernel launchが増えて最適化で得た理論latencyを失いやすい。MxMoEのGroupGEMMは複数precisionのtileを同じ実行枠へ詰め、各tileに対応するmicro-kernelを選ぶことで、異なる形式を持つexpertでもGPU全体の占有率を保つ。つまりprecision searchとruntime kernelを共同設計し、探索時に想定した速度を実機で再現する。",
        ),
    ],
}


def apply_patch(path: Path, anchor: str, addition: str) -> bool:
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
    for rel, patches in PATCHES.items():
        path = ROOT / rel
        paper_changed = False
        for anchor, addition in patches:
            paper_changed |= apply_patch(path, anchor, addition)
        if paper_changed:
            mark_audited(path)
            changed += 1
    print(f"content-quality batch8: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
