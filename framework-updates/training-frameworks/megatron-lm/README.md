# Megatron-LM

Megatron-LM repository全体の主要なsystem更新を継続的に記録する集約ページ。Megatron-Core固有のrelease内容やkernel・parallelism詳細は [Megatron-Core](../megatron-core/) を参照する。

## 現在できること

- **大規模pretraining / fine-tuning**: Megatron-Coreを基盤に、巨大なdense TransformerとMoEをmulti-GPU / multi-nodeで事前学習・追加学習できる。model sizeだけでなく長sequenceや多数expertにも対応する。
- **多次元parallelism**: tensor / pipeline / data / context / expert parallelismを組み合わせ、modelのどの軸をどのGPUへ分けるかをcluster topologyに合わせて設計できる。
- **学習stateの分割とoffload**: distributed optimizer、FSDP系sharding、CPU offloadでparameter・gradient・optimizer stateのGPU常駐量を減らせる。optimizer stateやmaster weightをCPU正本として保持する構成も取れる。
- **activation memory削減**: activation checkpointing / recomputationでforward中間値を保持せずbackward時に再計算し、長sequence trainingのpeak VRAMを削減できる。layer / segment単位で適用範囲も調整できる。
- **MoE training**: expert parallelism、token dispatcher、DeepEP / NCCL系通信、grouped-GEMM、shared expertを組み合わせ、routing後のtoken交換とexpert計算を最適化できる。
- **通信と計算のoverlap**: parameter gather、gradient reduction、pipeline通信、MoE All-to-All等をcomputeと重ね、network待ちを隠せる。
- **低精度training**: FP8 / FP4等でmatrix計算・parameter通信・checkpoint loadを低bit化し、HBM trafficとnetwork transferを削減できる。
- **CUDA Graph / fused kernel**: 繰り返すtraining stepやMoE MLPをGraph / fused kernelへまとめ、CPU launchと中間tensor書き戻しを減らせる。
- **distributed checkpoint / resume**: 大規模jobのcheckpoint save / load、shard変換、再開を行え、cluster構成変更を伴う運用にも対応する。

このページでは、Megatron-Core単体のkernel詳細よりも、**Megatron-LM全体としてtraining workflowで何が使えるか、Core側の新機能が上位trainingへどう反映されるか**を追う。

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
