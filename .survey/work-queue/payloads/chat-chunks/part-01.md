---
canonical_id: "arXiv:2609.00891"
arxiv_id: "2609.00891"
title: "CacheBridge: Efficient Cross-Model KV Cache Transfer"
summary: "モデル間KVキャッシュ転送の全head回帰をarchitecture対応headへ局所化し、attention感度重み付けとfused GPU fittingを組み合わせ、Qwen3 14B→32Bで99.83%のtarget retentionを維持しつつmapperを8分の1、適用を最大3.0×高速化する。"
source: "https://arxiv.org/abs/2609.00891"
last_audited: null
audit_version: 0
---

# CacheBridge: Efficient Cross-Model KV Cache Transfer

## 書誌情報
- **著者**: Xingyu Qu, Siyuan Lu, Zhiyu Chen, Sheng Wang, Tao Lin
- **所属**: Westlake University, Wuhan University, Amazon（論文記載）
- **公開日**: 2026-09-01
- **状態**: arXiv preprint v1
- **コード**: arXiv本文・著者公開ページから公式実装repositoryは確認できず。

## 問題設定
複数LLMをrouting、cost-quality cascade、agent pipelineなどで切り替える場合、同じprefixを引き継いでもKVキャッシュはモデル固有表現なので受信側モデルが再prefillしなければならない。長文になるほどこの再計算がhandoff latencyを支配する。

直前研究のFull-Head Mappingは、source/targetのaligned KV traceからtraining-freeなaffine ridge mapperをclosed formで作り、target側prefillを省く。しかし各target KV headを、選択したsource layer内の**全source KV head**から予測するため、(1) architecture差に弱い、(2) coordinate-wiseなKV再構成誤差と実際のcontinuation品質が一致しない、(3) mapper容量とonline affine計算量がsupport幅に比例する、(4) target layerごとに異なるtop-k source layerを使うためoffline fitting時のgather/materializationが重い、という問題がある。

## 手法
CacheBridgeはオンライン時のinterfaceをaffine mappingのまま維持しつつ、mapper support、calibration objective、construction pathの3点を同時に変える。

### Head-Local
Full-Head Mappingではtarget headごとに、選択された各source layerの全KV headをfeatureへ連結する。Head-Localは各target KV headをarchitecture metadataから決めた**対応source KV head 1個**だけに制約し、cross-layer aggregationだけを残す。評価した3方向はいずれもsource/targetが8 KV headsなので対応はidentity assignmentを使う。

source KV head数を `H_s` とすると、K/V両方の非bias係数数はfull-headに対して理論上 `1/H_s` となる。今回の評価では `H_s=8` なのでmapper係数・storageと主要affine workを8分の1へ削減する。これは単なる圧縮ではなく、GQAのquery-to-KV ownershipに沿わないcross-head相関を回帰から排除する構造的制約でもある。

### Attn-Repair
通常のridge fittingはすべてのKV coordinate誤差を同等に扱うが、実際のdecode出力への影響はreceiver側のquery・attention mass・downstream layerによって異なる。Attn-Repairはtarget modelのcausal attentionからK/V誤差の一次近似感度を求め、tokenごとのsample weightとしてridge regressionへ入れる。

KとVで別々の感度を計算し、32個の対数間隔prefix boundaryでfirst-future-queryを観測する。極端な重み集中でeffective sample sizeが崩れないよう、raw weightを一様重みへshrinkし、Kish effective sample sizeがfeature widthに応じたfloor以上になる最大係数を使う。オンライン時のmapper supportや適用コードは変わらず、変化するのはofflineで得られる係数値だけである。
