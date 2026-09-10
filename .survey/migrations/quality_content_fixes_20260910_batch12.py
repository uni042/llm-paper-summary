#!/usr/bin/env python3
"""Twelfth content-only batch: April-June 2026 papers."""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
"papers/inference/02-adaptive-expert-computation-compression/2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md": [
("Alloc-MoEの新規性はlayerとtokenを別々に最適化せず、**同じexpert実行予算の配分問題として結合したこと**にある。",
"この結合が重要なのは、layer-level配分だけでは同じlayer内の簡単なtokenと難しいtokenへ同じKを使い、token-level配分だけでは全layerへ同じ平均budgetを残してしまうためである。Alloc-Lで『どのlayerへ予算を置く価値が高いか』を決め、そのlayer内でAlloc-Tがrouter uncertaintyに応じて再配分することで、二種類の不均一性を順番に吸収する。"),
("選択するnative expert数だけを変え、weightの置き場所やPCIe transferは最適化しない。",
"このため実機speedupの解釈には注意が必要である。all-GPU環境ではactive expert数を減らせば主にGEMM量が減るが、offload環境では同じK削減でも『GPU resident expertを省いたか』『CPU側expertのtransferを省いたか』でI/O効果が大きく違う。Alloc-MoE自身はそこをcost modelへ入れないので、heterogeneous memory systemへ載せる場合はexpert residencyとactivation budgetをsystem側で共同最適化する余地が残る。")],
"papers/inference/05-speculative-decoding-moe/2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md": [
("高確率nodeは検証する価値が高く、低確率nodeはそのために新しいexpertを追加起動する価値が低い。",
"ただしacceptance probabilityだけで順位を付けるとMoE特有のcostを見落とす。ほぼ同じ受理確率の2 nodeでも、一方がすでにverification batchで使うexpertだけを再利用し、もう一方が新しいexpert集合を追加activateするなら後者の限界costは大きい。EVICTは候補benefitをtarget側の実測costと組み合わせることで、単なるhigh-confidence pruningではなく『受理される見込みに対してverification resourceを使う価値があるか』を評価する。"),
("論文ではこの性質を `ancestor-closed prefix` と呼ぶ。",
"この制約によりtree pruningは任意nodeのknapsackではなく、prefix構造を保つ選択になる。深いnodeのacceptanceが高くても、その祖先のどこかが低確率ならそこまで検証するcostを全て支払わなければ深いnodeへ到達できない。したがってEVICTは局所node scoreだけでなくrootからの累積benefit/costを見て、途中で枝を切る方が得な場合はそのdescendantもまとめて除外する。"),
("このためdecode stepごとにtree sizeが変わる。",
"適応tree sizeは、draft品質が時間とともに変化する場合にも効く。easy spanでは同じdraft branchが長くacceptされやすく、少し広いtreeへtarget computeを使う価値が高い。一方、難しいtoken付近ではbranchが分岐してexpert coverageも広がりやすく、同じ固定tree sizeを使うとrejectされる候補のために多数expertを起動する。stepごとにprefixを縮めることで、この局所的なacceptanceとMoE activationの変動へ追従する。")],
"papers/inference/05-speculative-decoding-moe/2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md": [
("MoEではbatchや1回のverification token数が増えると、一度に触れるexpert集合が広がる。そのためdense modelと同じparameter scalingだけでは低負荷側のcostを説明しにくい。論文はexpert coverageを使う補正を加え、sparse activationによる低負荷時のずれを説明する。",
"expert coverageが効く理由は、MoEの1 cycleのcostがtoken数へ線形に比例しないからである。少数requestではactive expert集合が疎で、verification tokenを増やすと新しいexpert weightやkernel workが増えやすい。一方batchが十分大きいと多くのexpertがすでにcoverageされ、追加tokenの限界costが変わる。モデルへcoverage項を入れることで、dense parameter countだけでは表せないこのactivation saturationを低次元cost modelへ取り込む。")],
"papers/inference/10-kv-cache-offload-recomputation/2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md": [
("KVをchunk化し、各pageの代表keyと上位centroidからなる階層indexをGPUに置く。全keyをそのままindexにする方式よりGPU memoryを減らしつつ、queryに関連するKV blockを絞り込む。論文では比較するspatial chunking系indexと同等のretrieval precisionを保ちながらindex footprintを50%削減し、lookupを最大2倍高速化したと報告している。",
"このindexはKV本体を置き換える圧縮ではなく、低速tierから何をfetchするかを決めるmetadataである。index自体が大きすぎるとKVを節約して空けたHBMを検索構造が消費し、lookupが遅ければI/O開始も遅れる。page代表とcentroidの二段階にすることで、まず粗くcandidate pageを絞り、詳細KVは必要pageだけDRAM/SSDから読む。したがってindex footprint・selection latency・retrieval recallの3者を同時に抑えることがpipeline成立の条件になる。")],
"papers/inference/06-moe-quantization-compression/2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md": [
("論文ではこれを `progressive quantization` と呼ぶ。",
"段階化にはrouter tuningとの相互作用もある。あるexpertを低bit化するとrouter再学習後のtraffic分布が変わり、その結果、次にどのexpertをさらに圧縮してよいかという重要度も変化する。高精度modelで一度だけ重要度を測って最終2bit配置まで決めるのではなく、各budget段階でquantized expertとrouterを新しい基準点として再評価することで、このfeedbackを近似的に追跡する。")],
"papers/inference/07-kv-cache-optimization-compression/2026-2606.06302-tangram-non-uniform-kv-cache.md": [
("underlying compressorのtoken選択誤りはTangramでは修正しない。",
"この設計は、圧縮algorithmとserving systemの責任を分ける。onlineでもimportance score自体は元compressorが計算し、Tangramが固定するのは各headで保持できる個数の上限である。したがって『どのtokenを残すか』の品質特性は既存compressorに従い、『その不均一な保持量をどう事前予約・page化・GPUへ割り当てるか』だけをstatic profileで安定化する。"),
("評価ではα=2。",
"安全係数αはdynamic compressorの揺らぎを固定budgetへ吸収する余裕である。αを小さくするとmemoryを強く節約できる反面、実入力でcalibration平均を超える保持需要が出たときbudget不足になりやすい。大きくするとprofile外入力へ頑健になるが、各headへ未使用capacityを予約してnon-uniform compressionのmemory利得を失う。つまりdeterministic allocationは完全な平均値固定ではなく、観測分散に応じたguard bandを持つ。"),
("adjacent groupingよりfull KVの12–25%を追加回収する。",
"budgetが近いheadを同groupへ入れる理由は、group page内のphysical allocationがそのgroupで最も長いheadに引っ張られるためである。保持率30%のheadと90%のheadを同じgroupにすると短いheadの空きが再び内部fragmentationとして残る。offline sort/clusteringで似た長さをまとめれば、group数を無限に増やさなくてもmax-minus-actualの差を小さくでき、page table overheadとmemory reclamationの中間点を作れる。"),
("fragmentation削減とCPU管理overheadのtrade-offを改善する。",
"head-groupごとに独立tableを持つと、schedulerが更新・参照するblock-table entry数とpointer操作が増える。Vectorized Block Tableはこの管理処理を複数groupまとめて連続配列として処理し、OpenMPでcore間、SIMDでentry間を並列化する。これによりH_pを小さくしてmemoryを細粒度回収したときも、host-side bookkeepingがprefill/decodeの新しいbottleneckになりにくくする。"),
("decode時はmapを読み、static heuristicのstragglerとdynamic planner costを避ける。",
"AOT mapはhead-groupの相対KV長がcontext成長後もほぼ同じ比率で伸びるという観察を利用する。runtime plannerなら毎stepの実長からCTA配分を最適化できるが、CPU planning costが発生する。固定equal splitならcostはないが長いgroupがstragglerになる。calibration比率から事前にwork shareを決めれば、runtimeではlookupだけで長いgroupへ多くCTAを配り、この二つの失敗を同時に避ける。"),
("underlying compressorのtoken選択誤りはTangramでは修正しない。\n\nこの設計は、圧縮algorithmとserving systemの責任を分ける。onlineでもimportance score自体は元compressorが計算し、Tangramが固定するのは各headで保持できる個数の上限である。したがって『どのtokenを残すか』の品質特性は既存compressorに従い、『その不均一な保持量をどう事前予約・page化・GPUへ割り当てるか』だけをstatic profileで安定化する。",
"同じretention profileをallocation・paging・load balancingの3層で共有することも重要である。memory allocatorだけ固定budgetを知っていてkernel schedulerが実長を知らなければ、容量は回収できてもdecode imbalanceが残る。逆にkernelだけ静的配分してもpage layoutがmonolithicならmemoryが返らない。Tangramはoffline calibration結果をcontrol plane全体の共通blueprintとして使い、各最適化が同じhead-length予測に基づいて噛み合うようにしている。")],
"papers/inference/01-offload-hierarchical-memory/2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md": [
("rack node間ではInfiniBand RDMAを使い、固定pipeline topologyとpre-registered bufferでkernel network stackやconnection setupを避ける。weight自体をnode間で毎token移すのではなく、stage間の小さいactivationを送る。",
"この通信設計が成立するのは、weight shardを各stageのLLCへ固定常駐させるからである。tokenごとに移動するdataを大きなparameterではなくembedding/activationへ限定すれば、node間pipelineを深くしてもnetwork byteはmodel sizeへ比例しない。pre-registered bufferと固定peerを使うことでRDMA setupもhot pathから外し、cache-resident operatorを短くした後にnetwork control overheadが相対的に目立つのを防ぐ。")],
"papers/inference/02-adaptive-expert-computation-compression/2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md": [
("が小さいexpertを省く候補にする。",
"benefit/cost比を使うことで、router scoreだけを見るdynamic Top-kとは異なる選択になる。例えばscore 0.08のexpertがGPU residentなら追加costは小さく実行した方がよい一方、score 0.10でも別deviceへのtransferと同期を発生させ、そのdeviceがcritical pathなら省く価値が高い場合がある。CAEEはsemantic contributionとhardware latencyを別軸で測り、同じTop-k集合の中からsystem上の限界費用が大きいexpertを探す。"),
("追加predictorや再学習は不要。ただしnative Top-kの一部を実際に省くため、losslessなprefetch/cache最適化ではない。",
"training-freeである代わりに、補正は元router scoreと実行済みexpertの範囲で行う。省いたexpertのweightを新しいexpertへ振り直す際、追加loadを必要とする候補は選ばないためI/O削減を相殺しない。これは精度回復の自由度を制限するが、runtime latencyを確実に減らすための制約である。品質低下を1%未満へ抑えたという結果は、この限定的なrenormalizationとthreshold設定の範囲での実測であり、完全同値ではない。"),
("論文ではこの考え方を`straggler-aware`と呼ぶ。ここでstragglerは「他deviceより遅く、全体を待たせているdevice」を意味する。",
"makespanを短くするには、最遅device以外の仕事を減らしても意味がない。例えばdevice Aが8 ms、Bが12 msで終わるlayerでAから2 ms削ってもlayer完了は12 msのままであるが、B側のlow-benefit expertを2 ms分省けば10 msへ短縮できる。CAEEはこのcritical-path性をcostへ入れ、同じ総FLOPs削減でもend-to-end latencyへ反映される場所を優先する。")],
}

def apply(path, anchor, addition):
    text=path.read_text(encoding='utf-8')
    if addition in text: return False
    if anchor not in text: raise RuntimeError(f'anchor not found: {path}\n{anchor}')
    path.write_text(text.replace(anchor, anchor+'\n\n'+addition,1),encoding='utf-8'); return True

def mark(path):
    t=path.read_text(encoding='utf-8').replace('last_audited: null','last_audited: "2026-09-10"',1).replace('audit_version: 0','audit_version: 1',1)
    path.write_text(t,encoding='utf-8')

def main():
    n=0
    for rel, ps in PATCHES.items():
        p=ROOT/rel; ch=False
        for a,b in ps: ch |= apply(p,a,b)
        if ch: mark(p); n+=1
    print(f'content-quality batch12: {n} paper(s) changed')
if __name__=='__main__': main()
