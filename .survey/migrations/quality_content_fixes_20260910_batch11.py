#!/usr/bin/env python3
"""Eleventh content-only batch: oldest remaining 2026 papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/99-other-inference-systems/2026-2601.15013-radixmlp-intra-batch-deduplication.md": [
        (
            "位置独立部分の主要計算量は概ね `O(N d²)` から `O(N' d²)` へ減る。トークンを集めたり戻したりする処理は追加されるが、モデル次元が大きくMLP等の計算が重いほど削減効果が上回りやすい。",
            "この重複排除で結果が変わらないのは、共有プレフィックス内の同じトークン位置が同じ入力表現と同じ因果履歴を持つためである。MLP・LayerNorm・線形射影のような位置ごとの演算は、その入力が同一なら出力も同一なので1回だけ計算して複数系列へ複製できる。一方、suffixへ分岐した後の位置や、系列内の他トークンとの関係を使うattentionは同じ扱いにできない。この境界を守ることで近似を入れずに計算だけを減らす。",
        ),
    ],
    "papers/inference/10-kv-cache-offload-recomputation/2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md": [
        (
            "iteration tでGPUがmodelを実行している間に、host側では次iterationのschedulingとKV rotationを進める。transferとscheduler overheadをGPU executionの裏へ隠すことで、frequent rotationによるstallを抑える。",
            "このpipelineでは、現在iterationが使うKV配置を途中で変更せず、次iterationで有効にする入替えをhost側で先に準備する。GPU計算終了の境界で必要なtransfer完了とscheduleを同期してから次iterationへ進むため、制御処理を重ねても現在計算が不完全なKVを読む必要はない。高速C2CとDuplexKVでrotation時間を短くし、その大部分を現在iterationのcompute内へ収めることが、requestを頻繁に入れ替えてもthroughputを落としにくくする条件になる。",
        ),
    ],
    "papers/inference/01-offload-hierarchical-memory/2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md": [
        (
            "local HBMから追い出したdataを別GPU HBMへ置ければ、次回必要になった時はPCIeではなくGPU間copyで戻す。別GPUに空きがなければ従来どおりhost DRAMを使う。",
            "この3階層化の要点は、peer HBMを新しい永続保存先として扱うのではなく、hostより速くlocalへ戻せるvictim cacheとして挟むことである。local HBMに保持できないexpertやKVでも、近隣GPUに空きがある間だけ複製しておけば次回missの復旧経路をPCIeからNVLinkへ変えられる。peer側の空きがなくなった場合は階層を1段飛ばしてhostへ戻るため、peer cacheの有無で正しさが変わらない。",
        ),
        (
            "重要なのは、**別GPU cacheは性能改善のためだけに使い、それを失っても推論を継続できるようにする**ことにある。",
            "weightとKVで復旧方法を分けるのは再生成costが違うためである。expert weightは元parameterから毎回再構築するよりhost DRAMの正式copyを残す方が安い。一方KVはrequest stateから再計算可能な場合があり、host copyを必ず二重保持するか再計算へ戻すかをruntimeが選べる。どちらの場合もpeer HBM上のcopyを唯一の正本にしないため、貸出GPUが突然memoryを取り戻してもmodel stateを失わず、性能だけがhost/recompute経路へ戻る。",
        ),
    ],
    "papers/inference/05-speculative-decoding-moe/2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md": [
        (
            "MoE-SpAcでは同じ優先度を使い、\n\n- 近く使う可能性が高いexpert → GPUに残す、または先に転送する\n- 近く使う可能性が低いexpert → GPUから追い出す、またはCPUで実行する\n\nと判断する。",
            "同じutilityを共有することで、cache policyとprefetch policyが互いに打ち消すのを防げる。例えば近い将来何度も使うと予測したexpertをprefetchした直後に、過去利用だけを見るLRUが追い出してしまえば転送が無駄になる。逆に将来需要が低いexpertをcacheへ残すために、必要expertのprefetch領域を圧迫する可能性もある。将来のactivation回数を共通の価値尺度にすることで、resident容量とPCIe帯域を同じexpert需要へ向けられる。",
        ),
        (
            "目的は、CPUかGPUの一方だけを忙しくするのではなく、**両方の処理ができるだけ同じ頃に終わるように仕事を分け、遅い側の待ち時間を減らすこと**である。",
            "ここでGPU実行が常に最善とは限らない。GPUにないexpertはweight全体をPCIeで転送してからGEMMする必要があり、token数が少ないexpertではそのtransfer costがCPU上で直接計算する時間を上回る場合がある。反対に多くのtokenが集まるexpertではCPU GEMMが長くなり、転送を払ってもGPUで処理した方が早い。MoE-SpAcはspeculative windowから将来のtoken数も見積もり、expertごとのCPU計算・GPU計算・転送時間を同じ配置問題へ入れる。",
        ),
        (
            "MoE-SpAcはこれを単純な順位順ではなく、**限られたmemoryと帯域の中で全expertの配置・実行場所をまとめて選ぶ問題**として解く。",
            "この組み合わせは、あるexpertをGPUへ載せる判断が他expertのVRAMとPCIe機会を奪うため独立には決められない。論文はonline integer optimizationで全体の完了時間を小さくする配置を選び、speculative utilityの高いexpertへ優先的に高速資源を割り当てる。毎expertを個別のthresholdで処理するより、GPU capacityを超えないこととCPU/GPU workload balanceを同時に保証しやすい。",
        ),
        (
            "将来需要の予測だけ良くても、各処理を順番に待つ実装では効果が小さいため、**転送待ちを別の計算の裏へ隠す実行engine**が重要になる。",
            "非同期engineは、draftが次のexpert需要を示した時点でtransferを発行し、現在のtarget/draft計算やCPU expert computeと並行させる。native routingが確定するまで何もしない方式では、せっかくspeculative decodingで得たlookahead時間を使えない。予測miss時には正しいexpertの追加transferが必要になるが、hitしたexpertについてはそのI/Oの大部分を前段computeへ重ねられるため、utility predictionを実際のlatency削減へ変換できる。",
        ),
    ],
    "papers/inference/10-kv-cache-offload-recomputation/2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md": [
        (
            "同じKVが複数SSDへ複製されている場合、どのcopyから読むかでSSDごとの負荷が偏る。Swarmはruntimeで各SSDのloadを見て読み出し先を選び、複数SSDが同時に働くようにする。またdecodeが進んで新しいKVが増えると参照傾向も変わるため、cluster membershipとDRAM cacheを更新する。",
            "静的配置だけでは、同じhot clusterへのrequestが集中したとき特定SSDだけqueueが伸び、理論上は複数deviceへ分散していてもaggregate bandwidthを使えないことがある。複製されたentryについて現在queueの短いSSDを選び、必要に応じてcluster配置を更新することで、共活性に基づく並列性をruntimeの実負荷へ合わせる。つまりoffline profilingは『一緒に読む集合』を作り、online schedulingは『その集合を今どのdeviceから読むか』を調整する役割分担になっている。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md": [
        (
            "追加predictorを学習せず元routerを利用できる一方、router自体の計算costは残る。論文では`Router-PF`と呼ぶ。",
            "Router-PFはnative gateと同じdecision boundaryを使えるため、軽量estimatorより予測精度を得やすい。一方、次layer routerを通常より早く追加実行するため、その計算とquasi-hidden state生成がprefetchで隠す時間を一部消費する。予測しやすいlayerではより安いestimatorへ切り替え、誤りやすいlayerだけRouter-PFを使うHybrid-PFが必要になる理由は、このaccuracyとprediction overheadのtrade-offにある。",
        ),
        (
            "prefetchのみなら隠せるのはtransfer時間だけだが、この方式では**transfer + expert compute**の両方を次layer到達前へ押し出せる。",
            "先行FFNが有効なのは、現在layerの残り計算と次layer到達までのslackが、weight transferだけでなくexpert GEMMの一部も重ねられる場合である。GPUがすでに飽和していて別queueのspeculative GEMMがnative computeを遅らせる場合や、次layerまでの距離が短い場合はprefetch-onlyの方が安全になる。そのため投機実行は予測精度だけでなくGPU resource contentionも含めて使うlayerを選ぶ必要がある。",
        ),
        (
            "予測expertを最終出力の代用品として使わないためlosslessである。",
            "hit時にはnative routerが選んだexpert IDと投機実行したIDが一致することを確認してから、その先行FFN結果をcommitする。miss時は投機結果を捨て、native expertを改めてtransfer・computeするため数学的には通常実行へ戻る。このcommit/fallback境界が、誤expertをそのまま代用してI/Oを省く近似手法との違いである。代償はmiss時に誤transferと誤GEMMの両方を二重に払うことであり、予測困難layerでは無効化する必要がある。",
        ),
        (
            "そのためlayerごとに、**現在layerの状態と次layer routingのずれや予測確信度**を測り、先行計算を使うか調整する。",
            "この選択は『すべてのlayerで最大限speculateすればよい』という設計を避ける。隣接layer間でrepresentationがよく似る区間はquasi-hidden stateからroutingを当てやすく、投機の期待利益が正になりやすい。一方router driftが大きい区間はmiss costが期待利益を上回るため、通常のon-demand loadへ戻す。layer-wise gatingによって投機を利益が見込める場所だけへ限定する。",
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
    print(f"content-quality batch11: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
