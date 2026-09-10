#!/usr/bin/env python3
"""Seventh content-only batch: oldest remaining 2025 papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/03-expert-prefetch/2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md": [
        (
            "GPU上で別modelを動かさないため、予測overheadを小さくできる。",
            "この予測はnative routerを置き換えるのではなく、次layerのweight transferを早く始めるためのhintとして使う。現在layerを計算している間に次layer候補expertをCPUからGPUへ動かし、実際に次layerへ到達した時点では本来のrouter結果を使う。予測が当たれば転送待ちを隠せるが、外れた場合は不足expertをon-demandで追加loadするため、予測誤りそのものが別expertへ誤routingするわけではない。したがってprefetch部分は品質を変えず、品質差が生じるのは主に後段の低bit量子化設定である。",
        ),
        (
            "深いlayerはroutingが一部expertへ偏りやすいため、小さいcacheでもprefetchで補える。",
            "これはGPU cacheを全layerへ均等分割する方式との違いである。浅いlayerで予測精度が低いのにcacheまで小さくすると、毎回異なるexpertがmissしてPCIe待ちが露出しやすい。一方、深いlayerではrouting候補が偏り、次layer予測も当たりやすいため、常駐数を減らしても必要expertを計算前に準備しやすい。Fateは『予測が難しい場所ほどresident capacityで守り、予測しやすい場所ほどprefetchへ依存する』という形で限られたVRAMを非均等に配る。",
        ),
        (
            "FateはARC（Adaptive Replacement Cache）を使い、**最近使われたexpert用の領域と、繰り返し使われるexpert用の領域を分け、その比率をworkloadに合わせて自動調整する**。",
            "この二種類を分ける理由は、MoE routingに短期的な局所性と長期的な人気度の両方があるからである。直近requestだけで急に使われたexpertをすべて残すと、長期間頻出するexpertが追い出される可能性がある。逆に累積頻度だけを見ると、現在のrequestで急に必要になったexpertへ適応しにくい。ARCはmissの出方に応じてrecency側とfrequency側の容量比を動かし、workloadが変化したときに固定LRU/LFUより追従しやすくする。",
        ),
    ],
    "papers/inference/99-other-inference-systems/2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md": [
        (
            "モデル配置やexpert数は変えず、同じtensorを同じ精度で計算する。したがって量子化やpruningではなく、**GPU間通信とGEMMの実行順序を細かく組み替えるlossless最適化**である。",
            "従来もall-to-all通信とexpert計算をchunk単位で重ねる方法はあるが、chunkを小さくしすぎると各GEMMが小さくなりTensor Coreを十分使えず、逆にchunkを大きくすると次の計算を始めるまで通信完了を長く待つ。つまり粗いpipelineには『通信を細かく隠したい』と『GEMMは大きく保ちたい』という衝突がある。CometはGEMM全体を小kernelへ分断するのではなく、1つの大きな計算の内部でtileごとのdata依存だけを細かく追跡し、このtrade-offを緩和する。",
        ),
        (
            "これにより、あるexpert向けdataがまだ届いていなくても、すでにdataが揃った別expertや別領域の計算を進められる。",
            "tileごとのready状態を使うことで、通信の最も遅い相手GPUを待つ全体barrierを避けられる。例えば8 GPU中7 GPUから必要tokenが届いていて1 GPUだけ遅れている場合、従来のall-to-all完了待ちではGEMM全体が停止するが、Cometでは到着済みtokenに対応するtileを先に処理する。遅れているtileだけを後へ回すため、networkのばらつきやexpertごとの不均衡があってもGPU演算器を動かし続けやすい。",
        ),
        (
            "論文では `thread-block specialization` と呼ぶが、要点は**通信kernelが終わってから計算kernelを起動するのではなく、GPU内部で通信係と計算係を並行して動かす**ことである。",
            "同一kernel内へまとめることで、通信kernelとGEMM kernelの間に毎回global synchronizationを置く必要も減る。通信担当blockはremote memoryへdataを送り、到着した領域の状態を更新する。GEMM担当blockはその状態を確認してreadyなtileだけを計算し、combine段階ではreduction担当が到着済みexpert結果を順次まとめる。処理段階をkernel境界ではなくdata依存で接続することが、細粒度重畳の実装上の中心になる。",
        ),
        (
            "Cometはmodel shape、token数、expert数、top-kに応じて、通信用blockと計算用blockの比率を事前測定から選ぶ。",
            "この比率が重要なのは、両者が同じGPUのSMやmemory resourceを取り合うためである。通信担当を増やしすぎるとdataは早く届いてもGEMM blockが不足し、計算担当を増やしすぎるとGEMM側が通信待ちになる。通信量が大きいshapeではcommunication側へ、行列演算が支配的なshapeではGEMM側へ資源を寄せ、両方の完了時間が近づくようにする。したがってCometの重畳は単に同時実行を許可するだけでなく、同時実行時のresource competitionまで含めて調整する。",
        ),
    ],
    "papers/inference/04-conditional-computation/2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md": [
        (
            "論文では、生成後半ほどperplexityが下がり、中間layerの変換も冗長になりやすいという観察から、常に使うlayerとskip候補layerを分ける。",
            "発想は、すべての生成位置へ同じ深さを割り当てる必要はないというものである。生成開始直後は文脈から次の展開を決める不確実性が高く、ここで誤ると後続tokenの条件そのものが変わる。一方、文や推論過程が進んで局所的な表現が固まった後半では、次tokenが比較的予測しやすくなる場合が多い。D³はtoken内容を毎回分類するrouterを追加せず、生成位置をこの計算需要の簡易proxyとして使うためtraining-freeで実装できる。",
        ),
        (
            "これは「最後のk layerを削るearly exit」と違い、**最終layer側の出力整形能力を残したまま中間計算を削る**設計である。",
            "最初と最後のlayerをcoreとして保護するのは役割が異なる。初期layerは入力表現を後段で使える特徴へ変換する基盤になり、最終layer付近はLM headへ渡す表現を語彙予測に適した状態へ整える。中間layerに相対的な冗長性があるという観察を利用し、両端を残して中央だけを可変にすることで、単純なearly exitより元modelの入出力interfaceを保ちやすくしている。",
        ),
        (
            "D3では必要なKVをコピーして、skipしたlayerでも後続tokenが過去contextを参照できるようにする。",
            "ここで必要なのは、現在tokenをそのlayerで重く処理しないことと、将来tokenが過去位置を参照するための状態を失わないことを分離することである。途中layerを飛ばしたtokenのKVが欠けると、後で同じlayerを実行するtokenから見た過去contextの長さが位置ごとに不整合になる。そこで近傍layerの状態を利用してKV位置を埋め、将来のattentionが系列全体を参照できる形を維持する。計算削減のためにcontext自体を削除する方式ではない。",
        ),
        (
            "ただし `α` と `start` はtask長に応じてvalidationで探索するため、完全に設定不要なplug-and-playではない。",
            "また位置だけで深さを決めるため、生成後半に突然難しい計算や固有名詞選択が現れても、そのtokenだけ自動的にfull depthへ戻す判断はできない。`α`を強く設定すると平均計算量は減るが、このような後半の難しいtokenまで一律に浅くなる。逆に安全側へ設定すると品質は守りやすいがspeedupが小さくなるため、taskごとの生成長と難易度分布を見て減衰率を決める必要がある。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md": [
        (
            "論文ではこの値を `significance` と呼ぶ。",
            "複数指標を使う理由は、routing頻度だけでは量子化誤差の大きさを表せないからである。頻繁に選ばれるexpertでも低bit化して出力がほとんど変わらないなら高精度を残す優先度は下げられる。一方、選択回数が少なくても特定datasetでrouting scoreが高く、そのexpertのweightが量子化へ敏感なら、低bit化した少数回の誤差が品質へ大きく効く可能性がある。DynaMoは利用頻度・寄与の強さ・weight側の感度を合わせて、datasetごとにprecisionを残す価値を見積もる。",
        ),
        (
            "論文ではこの分類を `fuzzy clustering` と呼ぶ。境界にあるexpertを無理に最初から一群へ固定せず、最終的には容量を節約するため低bit側へ寄せる。",
            "この多段階化により、重要expertだけINT8、やや重要なexpertはINT6/4、影響の小さいexpertはINT2という連続的な容量配分ができる。二値の高bit/低bit分類では境界付近のexpertをどちらかへ丸める必要があり、容量を余計に使うか品質を余計に落とすかのどちらかになりやすい。中間bitを用意することで、総memory budgetの中でimportanceに近いprecisionを割り当てやすくなる。",
        ),
        (
            "全weightの約1%だけをFP16 cacheとして持ち、新datasetへ切り替わった際はこの部分を使って必要なbit構成だけを更新する。",
            "dataset切替で問題になるのは、expert全体のweightが変わることではなく『どのchannelの量子化誤差が新しい入力分布で目立つか』が変わる点である。変化に敏感なchannelだけ高精度copyを残しておけば、全expertのFP16 weightを別途保持したり、モデル全体を最初から再量子化したりせず、その部分を差し替えて新しいprecision構成へ適応できる。少量cacheはcross-dataset adaptationの復元材料として働く。",
        ),
        (
            "つまり、\n\n`dataset A向けbit配置 → dataset Bへ切替 → expert重要度を更新 → 変化に敏感な少数channelを使ってbit配置を更新`\n\nという運用で、decode tokenごとにINT2/INT8を動的変更する方式ではない。",
            "したがってruntime switchableという名称でも、各tokenのrouter結果に合わせて毎回weight表現を作り直すcostは負わない。workload切替時にだけ較正情報とsalient channelを使って構成を更新し、その後の多数requestでは同じ低bit weightを繰り返し使う。切替頻度が低いservingでは更新costを長い実行期間へ償却できる一方、datasetが極端に短い周期で入れ替わる環境では adaptation overheadの比率が大きくなる。",
        ),
    ],
    "papers/inference/04-conditional-computation/2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md": [
        (
            "つまりlayer自体を削除するのではなく、**tokenごとに二つの経路から選ぶ**。",
            "同じbatch内でもtokenごとに選択が異なるため、FlexiDepthは固定した浅いsubmodelを使う方式ではない。あるtokenは前のlayerをskipしても次layerではfull経路へ戻れ、逆に別tokenは複数layerを連続して軽量経路で通れる。この柔軟性によってcopyや定型句へ少ない計算を割き、計算・推論など不確実性の高いtokenへ深い経路を残せるが、GPU実行上はtokenごとの分岐が増えるというcostも生む。",
        ),
        (
            "adapterなしの評価で品質が大きく崩れるため、FlexiDepthでは**「layerを飛ばす」より「重いlayer処理を安い近似変換へ置き換える」**と理解する方が正確である。",
            "adapterはfull blockの出力を完全再現する必要はなく、skipしたtokenの表現を次の元Transformer layerが扱える分布へ近づける役割を持つ。元LLM weightは固定されているため、後段layer側をskip入力へ合わせて学習し直すことはできない。そこで軽量adapter側だけを学習し、重いattention/FFNを省いたことで生じる表現のずれを局所的に補正する。この設計により元checkpointを保ったまま動的経路を追加できる。",
        ),
        (
            "つまり削るのは主にquery側attention計算やFFNで、過去tokenとしての文脈情報を消すわけではない。",
            "これは現在tokenの計算需要と、将来tokenにとっての記憶価値を別扱いにする設計である。あるtoken自身は定型的でfull attention/FFNを必要としなくても、そのtokenが後続文脈から参照される可能性はある。K/Vまで消すと後続tokenから見えるhistoryが経路選択に依存して欠落するため、軽量経路でも将来参照用の状態だけは保存し、計算削減がcontext削除にならないようにする。",
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
    print(f"content-quality batch7: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
