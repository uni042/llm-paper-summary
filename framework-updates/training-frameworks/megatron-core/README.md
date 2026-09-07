# Megatron-Core

Megatron-Coreの主要な機能・性能更新を継続的に記録する集約ページ。大規模Transformer / MoE学習のparallelism、GPU間通信、CUDA Graph、activation recomputation、CPU offload、低精度parameter通信などを扱う。

## 現在できること

- tensor / pipeline / data / context / expert parallelismを組み合わせ、大規模dense TransformerとMoEをmulti-GPU / multi-nodeで学習できる。
- FSDP系parameter sharding、sequence parallelism、distributed optimizerを使い、parameter・gradient・optimizer stateのmemory複製を減らせる。
- MoEではexpert parallelism、token dispatcher、DeepEP / NCCL等の通信backend、shared expertを組み合わせてrouting後のtoken交換を制御できる。
- communication overlapでparameter gather、gradient reduction、MoE All-to-All等をcomputeと重ね、network待ちを隠せる。
- activation checkpointing / recomputation / CPU offloadとoptimizer-state offloadを使い、GPU memoryと追加計算・host transferをtrade-offできる。
- FP8 / FP4等の低精度training、低bit parameter通信、fused kernel、CUDA Graphを利用し、演算・通信・launch overheadを削減できる。

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
