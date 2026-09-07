# Megatron-LM

Megatron-LM repository全体の主要なsystem更新を継続的に記録する集約ページ。Megatron-Core固有のrelease内容やkernel・parallelism詳細は [Megatron-Core](../megatron-core/) を参照する。

## 初期収録期間

2026-06-03〜2026-09-03

この期間の主要system更新は、Megatron-Core 0.18.0 / 0.19.0 releaseと、Megatron-LM `dev` branchへmergeされたoffload / recompute関連PRとして提供された。

## 要点

### MoE通信とparallelism

Core 0.18.0 / 0.19.0では、MoE tokenをexpert GPUへ送る全対全通信（All-to-All）とexpert計算を重ねる仕組み、HybridEP / DeepEP、MoE MLP fusionなどが追加された。

つまり、

1. routing結果に従ってtokenを別GPUへ送る
2. network通信が終わるのを完全に待たず、到着済みtokenからexpert計算を進める
3. expert計算内部のactivation / quantizationなどを1 kernelへまとめる

ことで、MoE layerの通信待ちとkernel overheadを減らす方向の更新である。

### CUDA Graphと低精度通信

full-model CUDA Graph対応や、MXFP8 / NVFP4形式でparameterをGPU間収集する低精度parameter gatherが入った。

低bit形式でparameterを通信すればnetwork転送量を減らせるが、scale管理や数値精度とのtrade-offがある。

### activation recompute

`dev` branchでは、GPU memory節約のためforward時のactivationをすべて保持せず、backward時に一部を再計算する**活性値再計算（activation recomputation）**が細粒度化された。

従来のstage単位だけでなくlayer / segment単位で「保持するか再計算するか」を選び、MoE All-to-All overlapと併用できるようにした。

### optimizer-state / master-weight CPU offload

optimizer stateと高精度master weightをCPUのpinned memoryへ正本として置き、GPUには現在更新する小さいchunkだけ戻す方式が`dev`へmergeされた。

全optimizer stateをGPUへ載せないためpeak VRAMを下げられる一方、CPU↔GPU転送量とhost RAM bandwidthが新しい制約になる。

## 注視中

- **DeepEP v2 inference dispatcher — PR #5745（Open、2026-09-07確認）**: inference-onlyのMoE token dispatcher。decode用とchunked-prefill用に固定shape bufferを別々に事前確保し、stepごとに再allocationせずCUDA Graph capture可能なlayoutを使う提案。

  **dispatcher**はrouting済みtokenを対応expert GPUへ送信し、expert計算後に元token順へ戻す通信層。DeepEP v2ではElasticBufferを用い、decodeの小さい固定shapeとprefillの大きいchunk shapeを分けて管理する。

  stable / merged機能ではないため、正式release項目とは分離して扱う。[PR #5745](https://github.com/NVIDIA/Megatron-LM/pull/5745)

- [Megatron-LM releases](https://github.com/NVIDIA/Megatron-LM/releases)

### 用語メモ

- **master weight**: mixed-precision学習で、forward/backward用低精度weightとは別にoptimizer更新用として保持する高精度weight。
- **activation recomputation**: forward結果をmemoryへ残さず、backwardで必要なとき再計算してVRAMを節約する方式。
- **All-to-All overlap**: GPU間token通信とexpert計算を同時進行させ、network待ちを隠す方式。
