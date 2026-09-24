# Megatron-Core

Megatron-Coreの主要な機能・性能更新を継続的に記録する集約ページ。大規模Transformer / MoE学習のparallelism、GPU間通信、CUDA Graph、activation recomputation、CPU offload、低精度parameter通信などを扱う。

## 現在できること

- **tensor parallelism**: 1 layer内の大きなmatrix計算を複数GPUへ分割し、単一GPUに収まらないhidden sizeやFFNを学習できる。各layerでGPU間collective通信が入るため、NVLink / high-bandwidth interconnectが重要。
- **pipeline parallelism**: model layerを複数stageへ分け、異なるmicrobatchをstage間でpipeline実行できる。model depthを複数GPUへ分散できる一方、stageが仕事をしていないpipeline bubbleを減らすschedule設計が性能を左右する。
- **data parallelism / FSDP**: batchをGPU間へ分けるdata parallelismに加え、parameter・gradient・optimizer stateをGPU間へshardするFSDP系実行を使える。model stateの重複を減らし、data parallel replicaごとのVRAM使用量を下げられる。
- **context / sequence parallelism**: 長いsequenceのactivationやattention計算をGPU間へ分割し、1 GPU当たりのactivation / KV相当stateを減らせる。長context trainingでsequence length由来のmemory増加を抑えるために使う。
- **expert parallelism**: MoE expertをGPU間へ分散し、routingされたtokenだけを対応expertへ送る。全GPUが全expertを持つ必要をなくし、expert数が大きいmodelをmulti-GPUへ拡張できる。
- **複数parallelismの合成**: tensor / pipeline / data / context / expert parallelismを同時に組み合わせられる。model size、sequence長、expert数、GPU topologyのどれが主制約かに応じて分割軸を変えられることがMegatron-Coreの中心機能。
- **distributed optimizer**: optimizer stateやgradientをGPU間で分割し、data parallel replicaごとの重複memoryを減らせる。計算に必要なstateだけを集め、update後に再びshardする。
- **MoE token dispatcher**: routing結果を見てtokenをexpertが置かれたGPUへ送り、expert計算後に元のtoken順へ戻す通信層を持つ。NCCL、DeepEP、HybridEP等をcluster構成に応じて選べる。
- **MoE load balancing**: expertごとのtoken負荷を観測し、特定expertだけが混雑してlayer全体を待たせる状況を減らすrouter調整を利用できる。平均だけでなくtail側の偏りを抑える方式も扱う。
- **shared expert**: routed expertとは別に全tokenが通るshared expertをMoE layerへ組み込み、routed expertと並行 / fused実行する構成を取れる。shared expertが追加するcomputeをcritical pathへ載せすぎないことが重要。
- **grouped GEMM / fused MoE MLP**: 複数expertの小さいmatrix multiply、SwiGLU、quantization等をまとめて実行し、expertごとのkernel launchと中間tensorのHBM書き戻しを減らせる。
- **communication overlap**: parameter gather、gradient reduction、pipeline通信、MoE All-to-All等をcomputeと別stream / chunkで進め、network完了を待つ時間をGPU計算の裏へ隠せる。
- **FSDPとMoE通信のoverlap**: parameter sharding通信とexpert token交換を直列に待たず、可能な部分を同時進行できる。FSDPとEPを組み合わせたときのnetwork serializationを減らす。
- **activation checkpointing / recomputation**: forward中間値をすべて保持せず、backward時に必要部分を再計算してVRAMを節約できる。layer / segment単位で保持と再計算を選び、追加computeとmemory削減を調整できる。
- **activation CPU offload**: backwardまで必要なactivationの一部をCPU DRAMへ退避し、GPU memoryを空けられる。CUDA Graph対応pathでは固定buffer等を使い、offloadを有効にしてもGraph captureを壊しにくくする。
- **optimizer-state / master-weight offload**: optimizer stateと高精度master weightの正本をCPU pinned memoryへ置き、update対象chunkだけGPUへ戻せる。optimizer stepで全stateを同時にVRAMへ載せる必要をなくす。
- **FP8 / FP4 training**: weight / activation / matrix計算を低精度化し、Tensor Core throughputとHBM trafficを改善できる。低bit化による数値誤差・scale管理と収束への影響を確認する必要がある。
- **低bit parameter communication**: sharded parameterをGPU間でgatherするときMXFP8 / NVFP4等へ圧縮し、network trafficを減らせる。通信後に必要precisionへ戻すcostと精度がtrade-offになる。
- **CUDA Graph**: 繰り返すtraining stepやmodel区間をcaptureし、Python / CPUから大量のGPU kernelを毎step launchするoverheadを減らせる。full-model Graphへ適用範囲を広げることもできる。
- **streaming checkpoint load**: quantized checkpoint全体をCPU RAMへ展開せず、必要blockを順に読み込んでtarget format / GPUへ送れる。巨大modelの起動時host-memory peakを抑えられる。
- **distributed checkpoint**: multi-GPUにshardされたmodel / optimizer stateを保存・復元し、parallelism構成やjob再開へ使える。大規模trainingで1 processに全stateを集めて保存する必要を減らす。
- **上位training stack向けbuilding block**: transformer layer、parallel linear、MoE、distributed optimizer等をlibraryとして提供し、Megatron-LM等がmodel recipe / data pipelineを載せる基盤になる。

以下の更新履歴は、**MoE通信とfusion、CUDA Graph、低精度parameter gather、activation / optimizer offload**が最近どう拡張されたかを記録している。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-23 — Core 0.18.0（released）

- **Megatron-FSDP A2A overlap**: FSDPでparameterを分割保持しながら、MoE tokenの全対全通信（All-to-All）とexpert計算を同時進行させる。network待ちをexpert computeの裏へ隠す狙い。

- **HybridEP fusion**: expert parallelism（EP）を複数通信backend / parallel groupと組み合わせるHybridEPで、routing・token並べ替え・通信前後処理などをfusionして小kernelとmemory trafficを削減。

- **GroupGEMM + SwiGLU + quantize fused MLP**: 複数expertのGEMM、SwiGLU activation、次工程向けquantizationを別kernelへ分けず1つの処理系列へまとめる。中間tensorのVRAM書き戻しを減らす。

- **full-model CUDA Graph**: layer単位ではなくmodelのより広い実行区間をCUDA Graphへcaptureし、CPUからのkernel launch overheadを削減。

- **MXFP8 / NVFP4 parameter gather**: GPU間で分割されているparameterを集めるとき、BF16 / FP16より小さい低bit形式で通信し、network trafficを減らす。

[release](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.18.0)

### 2026-08-19 — Core 0.19.0（released）

- **Quantile Balancing router**: MoE expertごとのtoken負荷を単純平均だけでなく分位点（quantile）ベースで見て、極端に混雑するexpertを減らすrouting調整。

- **fused shared-expert MLP**: routed expertとは別に全tokenが通るshared expert計算を、周辺activation処理とまとめて実行しkernel overheadを減らす。

- **DeepEP / HybridEP THD dispatch**: token layoutをTHD（Total tokens × Heads/Hidden × Dimension系の可変token表現）として扱い、paddingを減らしながらDeepEP / HybridEP通信へ流す。

- **NCCL EP dispatcher**: DeepEP専用pathだけでなくNCCLを使うexpert token dispatchを正式なdispatcherとして追加し、cluster構成に応じて通信backendを選べるようにする。

- **per-sequence All-to-All fusion**: sequenceごとに個別発行していたtoken交換をまとめ、集合通信の起動回数を減らす。

- **CUDA-Graph-compatible activation offload**: activationをCPUへ退避する際にも、固定bufferや実行shapeを使ってCUDA Graph captureを壊しにくいpathを追加。

- **streaming quantized checkpoint load**: quantized checkpoint全体を一度CPU RAMへ展開せず、必要部分を順に読み込みながらGPU / target formatへ変換する。model load時のhost memory peakを下げる。

[release](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.19.0)

### 2026-08-02〜08-19 — activation recompute（merged into `dev`）

GPU memoryを節約するため、forward中間結果を保持せずbackward時に再計算するactivation recomputationを、MoE通信overlapと両立できるよう改善した。

従来の大きなpipeline stage単位だけでなく、**layer / segment単位で「この区間は保持、この区間は再計算」**を選べるよう細分化している。

これにより、

- memoryを多く使うlayerだけrecomputeする
- communication overlapを壊しやすいlayerは保持する

といった調整が可能になる。

[#5869](https://github.com/NVIDIA/Megatron-LM/pull/5869) [#6311](https://github.com/NVIDIA/Megatron-LM/pull/6311)

### 2026-08-18 — chunked optimizer-state offload（merged into `dev`）

optimizer stateとmaster weightの正本をCPU pinned memoryへ置き、GPUへは一度に全stateを戻さず**一定サイズのchunkだけ**restoreする。

処理は概ね、

`CPU canonical state → GPUへchunk restore → optimizer update → CPUへoffload`

をchunkごとに繰り返す。

GPUに同時常駐するoptimizer stateを上限付きにできるためpeak VRAMを抑えられる。代わりにPCIe / NVLink-C2C等のhost-device bandwidthが性能へ効く。[PR #6244](https://github.com/NVIDIA/Megatron-LM/pull/6244)

## 注視すべきPR

- **#5745（Open、2026-09-07確認）**: inference-only DeepEP v2 dispatcher。通常decode用とchunked prefill用に別サイズのElasticBufferを初期化時に確保し、step中の再allocationを避ける。固定layoutにすることでCUDA Graph capture可能なMoE token dispatchを目指す。[PR #5745](https://github.com/NVIDIA/Megatron-LM/pull/5745)

### 用語メモ

- **FSDP（Fully Sharded Data Parallel; 完全分割データ並列）**: parameter、gradient、optimizer stateをGPU間へ分割し、各GPUの常駐memoryを減らす方式。
- **EP（Expert Parallelism; エキスパート並列）**: MoE expertをGPU間へ分散する方式。
- **parameter gather**: 分割保持しているweightを、計算に必要なタイミングでGPU間から集める通信。
- **canonical storage**: 正本として扱うstateの保存場所。offloadではCPU側を正本にし、GPU側を一時working copyにする場合がある。
