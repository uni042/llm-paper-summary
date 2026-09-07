# Megatron-LM

Megatron-LM repository全体の主要なsystem更新を継続的に記録する集約ページ。Megatron-Core固有のrelease内容やkernel・parallelism詳細は [Megatron-Core](../megatron-core/) を参照する。

## 現在できること

- **大規模LLM pretraining**: Megatron-Coreを基盤に、数十億〜さらに大きいparameter規模のdense TransformerやMoEをmulti-GPU / multi-nodeで事前学習できる。model definitionだけでなくdata loading、optimizer、parallelism、checkpointまでtraining job全体を構成する上位stack。
- **fine-tuning / continued pretraining**: pretrained checkpointから追加学習し、domain adaptationやinstruction tuning等へつなげられる。大規模pretrainingと同じparallelism / memory機能を利用できるため、modelが単一GPUに収まらない場合でもfine-tuningできる。
- **tensor parallelism**: 1 layer内のmatrixを複数GPUへ分割し、hidden size / FFNが大きいmodelを学習できる。layerごとにcollective通信が必要になるため、node内の高速interconnectを活用する構成に向く。
- **pipeline parallelism**: layer群を複数stageへ分け、異なるmicrobatchをpipelineへ流せる。model depthを複数GPUへ分散しつつ、microbatch schedulingでpipeline bubbleを減らす。
- **data parallelism / FSDP系sharding**: batchをGPU間へ分けると同時に、parameter・gradient・optimizer stateのshardingを利用できる。全GPUがmodel stateを完全複製するmemory costを減らせる。
- **context parallelism**: 長いsequenceを複数GPUへ分け、activationやattentionの1 GPU当たりmemoryを減らせる。長context pretrainingでsequence lengthがmemory制約になる場合に使う。
- **expert parallelism**: MoE expertをGPU間へ分散し、token routing後に必要expertだけ計算する。expert数を増やして総parameter数を大きくしつつ、token当たりactive computeを抑えるMoE学習をclusterへ展開できる。
- **複数parallelismの同時利用**: tensor / pipeline / data / context / expert parallelismを組み合わせ、node内高速linkとnode間networkに合わせてparallel groupを作れる。model size、sequence、expert数のどこが主制約かに応じて構成を変えられる。
- **distributed optimizer**: optimizer stateやgradientをdata-parallel rank間へshardし、Adam等が持つ大きなstateのVRAM重複を減らせる。大規模modelではparameter本体以上にoptimizer stateがmemoryを占めるため重要。
- **activation checkpointing / recomputation**: forward中間値をすべて保存せずbackwardで再計算し、activation memoryを削減できる。layer / segment単位で再計算範囲を調整し、追加computeとVRAM節約のtrade-offを選べる。
- **activation CPU offload**: activationの一部をCPU DRAMへ移し、backward前にGPUへ戻す構成を取れる。長sequence時のpeak VRAMをさらに下げられるが、host-device bandwidthがstep timeへ効く。
- **optimizer-state / master-weight CPU offload**: optimizer stateと高精度master weightをCPU pinned memoryに正本として保持し、updateするchunkだけGPUへ戻せる。GPUへ全optimizer stateを常駐させずに済む。
- **MoE token dispatch**: routingされたtokenをexpertが置かれたGPUへ送って戻すAll-to-All通信をDeepEP / NCCL系backendで実行できる。通信とexpert計算をoverlapし、network待ちを隠すこともできる。
- **MoE load balancing / shared expert**: expertへのtoken偏りを減らすrouter調整や、全tokenが通るshared expertを組み合わせられる。特定expertの混雑によるstragglerを減らしながらmodel capacityを利用する。
- **grouped / fused MoE kernel**: 複数expertのGEMM、activation、quantization等をまとめ、小さなkernelをexpertごとに起動するoverheadと中間HBM trafficを減らせる。
- **communication overlap**: parameter gather、gradient reduce-scatter、pipeline send / recv、MoE All-to-All等をcomputeと重ね、GPUがnetwork完了だけを待つ時間を減らせる。
- **FP8 / FP4等の低精度training**: matrix計算、parameter / activation、場合によっては通信を低bit化し、Tensor Core throughput、HBM使用量、network trafficを削減できる。scale管理と収束精度の検証が必要。
- **低bit parameter gather**: sharded parameterをGPU間で集める際にMXFP8 / NVFP4等へ圧縮し、通信量を減らせる。compute precisionとcommunication precisionを分けて最適化する。
- **CUDA Graph**: 繰り返すtraining step / model区間をcaptureし、Python / CPUが毎step大量のGPU kernelをlaunchするoverheadを減らせる。固定bufferやoffload pathとの互換性が実用範囲を左右する。
- **distributed checkpoint**: model / optimizerをrankごとのshardとして保存・復元し、巨大stateを1 processへ集約せずcheckpointできる。job再開やparallelism構成の変更へ対応するための変換も行える。
- **quantized checkpointのstreaming load**: checkpoint全体を一度CPU RAMへ展開せず、blockごとに読み込んでtarget precision / GPUへ送れる。巨大modelのstartup時host memory peakを抑えられる。
- **training recipe / data pipeline**: Megatron-Coreの低level building blockに加え、実際のpretraining jobとしてmodel config、dataset、optimizer、scheduler、checkpoint cadence等をまとめて実行できる。
- **性能計測と大規模job運用**: throughput、loss、memory、parallelism設定を大規模training jobとして管理し、研究用kernel単体ではなくend-to-end pretraining systemとして使える。

このページでは、Megatron-Core単体のkernel詳細よりも、**Megatron-LM全体としてtraining workflowで何が使えるか、Core側の新機能が実際のpretraining / fine-tuningへどう組み込まれるか**を追う。

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
