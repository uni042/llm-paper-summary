# フレームワーク更新

主要LLMフレームワークで起きた、**推論速度・学習速度・memory使用量・GPU間通信・offload方式を実質的に変える更新**を、このページから追えるように継続管理する。

- フレームワーク差分の最終確認: **2026-09-08**
- 用語・可読性の最終監査: **2026-09-07**

この2つは分けて扱う。2026-09-08の差分確認では、公式release・開発元repositoryを基準に9月5日以降の主要な性能・量子化・memory関連変更を再確認した。

## 現在の機能マップ

ここでは「直近に何が変わったか」より先に、**現在そのフレームワークで何ができるか**を整理する。更新履歴は、その能力がどの方向へ拡張・高速化されたかとして読む。

### 推論・serving

| Framework | 現在できること | 最近の更新が強化している部分 |
|---|---|---|
| [llama.cpp](inference-engines/llama-cpp/) | CPU / GPUをまたぐローカル推論、量子化、複数GPU分割、KV cache管理、投機的デコード、部分的weight offload | MoE kernel fusion、CUDA Graph、CPU offloadしたexpertのVRAM cache、multi-GPU同時実行 |
| [vLLM](inference-engines/vllm/) | continuous batching、paged / tiered KV cache、P/D分離、MoE、投機的デコード、weight offload、分散serving | KV階層化、NIXL転送、adaptive speculative decoding、E/P/D分離、MoE通信・kernel fusion |
| [SGLang](inference-engines/sglang/) | prefix cache、continuous batching、P/D分離、投機的デコード、paged attention、TP/PP/EP/DP、量子化、multi-LoRA、RL rollout | 階層cache、MTP、sparse attention、MoE負荷分散、CUDA Graph、通信同期削減 |
| [TensorRT-LLM](inference-engines/tensorrt-llm/) | NVIDIA GPU向け高性能serving、paged KV、量子化、投機的デコード、P/D分離、multi-GPU | KVCacheManagerV2、disk KV、KV圧縮、NIXL転送、CUDA Graph拡張、低bit MoE |
| [LMDeploy](inference-engines/lmdeploy/) | GPU serving、prefix / object cache、paged attention、MoE、P/D分離、外部KV connector | object cache再設計、SSM state再利用、DeepEPv2、Mooncake接続、低精度GEMM |
| [LightLLM](inference-engines/lightllm/) | GPU→CPU→diskの多段cache、P/D分離、MoE、投機的デコード、RL rollout向けonline weight更新 | Hybrid Radix Cache、量子化KV、NIXL、disk cache、MoE fusion |
| [ExLlama](inference-engines/exllama/) | 低bit GPU推論、MoE expert / KVのCPU offload、投機的デコード、複数GPU | expert単位の動的offload、CPU KV tier、draft自動調整、VRAM slab allocator |
| [KTransformers](inference-engines/ktransformers/) | CPU/GPU異種推論、CPU上の低bit MoE expert実行、full-parameter / LoRA SFT | INT4 CPU expert、FP8 LoRA、CPU activation保持、巨大MoEのhost memory削減 |
| [Mistral.rs](inference-engines/mistral-rs/) | CPU/GPU推論、量子化、MoE、LoRA、複数request serving、投機的デコード | CPU量子化kernel、GQA KV streaming、MTP / DFlash、dynamic adapter、CUDA Graph |
| [Ollama](inference-engines/ollama/) | ローカルmodel管理・API serving、Apple / NVIDIA等での推論、量子化model、MTP | Apple MTP、MoE / NVFP4高速化、metadata cache、prefill再利用 |
| [MLX LM](inference-engines/mlx-lm/) | Apple Silicon上のLLM推論、量子化、KV cache、batch generation、server | stableの大更新は少なく、MLA multi-token decode、KV量子化、recurrent rollbackをOpen PRで追跡 |
| [MLX](inference-engines/mlx/) | Apple Siliconの統一memoryを使うtensor / neural-network実行、GPU kernel、量子化 | GQA / attention / quantized MoE kernel、zero-copy import |
| [Hugging Face Transformers](inference-engines/hugging-face-transformers/) | 多数modelの標準推論・学習API、KV cache、attention backend、生成制御、投機的デコード | StaticCache prefill高速化、ensemble speculative decoding |
| [ONNX Runtime GenAI](inference-engines/onnx-runtime-genai/) | ONNX modelの生成runtime、複数Execution Provider、hardware別build、KV cache、低bit model | hardware variant同梱、QNN zero-copy KV、INT8 builder |
| [OpenVINO GenAI](inference-engines/openvino-genai/) | Intel CPU / GPU向け生成AI推論、LLM・画像/動画生成、投機的デコード | tree型speculative decoding、temporal cache、build最適化 |
| [Modular MAX](inference-engines/modular-max/) | GPU serving、低bit KV、tiered KV、MoE並列、投機的デコード、compile済みgraph実行 | VMM allocator、async KV onload、FP8 / MXint8 KV、DFlash、shared expert overlap |
| [Accelerate](inference-engines/accelerate/) | PyTorch分散学習のlaunch / device配置、FSDP / DeepSpeed連携、CPU offload | FSDP2 FP8、regional compilation、CPU offload、Intel CPU分散学習 |
| [TGI](inference-engines/tgi/) | continuous batching、tensor parallelism、量子化、streamingを備えた既存serving stack | repository archive済みで、新規機能追加は停止状態 |
| [FlexFlow Serve](inference-engines/flexflow-serve/) | speculative serving、複数GPU配置、serving schedulingを扱う既存runtime | 追跡期間内は本質的更新なし |

### 学習

| Framework | 現在できること | 最近の更新が強化している部分 |
|---|---|---|
| [DeepSpeed](training-frameworks/deepspeed/) | ZeRO、CPU / NVMe offload、MoE、分散学習、RLHF向けHybridEngine | AutoEP、TP+EP folding、grouped-GEMM、gradient / activation非同期offload |
| [Megatron-Core](training-frameworks/megatron-core/) | TP / PP / DP / EP、FSDP、MoE、activation recomputation、CUDA Graph、低精度学習 | HybridEP / DeepEP、通信と計算のoverlap、低bit parameter gather、activation / optimizer offload |
| [Megatron-LM](training-frameworks/megatron-lm/) | Megatron-Coreを使った大規模Transformer / MoE事前学習・fine-tuning | Core統合、細粒度recompute、chunked optimizer-state / master-weight CPU offload |
| [TorchTitan](training-frameworks/torchtitan/) | PyTorch-nativeなFSDP / TP / PP / EP、MoE、activation checkpointing、低精度学習 | unified token dispatcher、GraphTrainer、通信overlap、whole-step graph化 |

### Hardware runtime

| Runtime | 現在できること | 最近の更新が強化している部分 |
|---|---|---|
| [ROCm](hardware-runtimes/rocm/) | AMD GPU向けHIP runtime、RCCL集合通信、AITER / Composable KernelによるLLM kernel | low-bit MoE、paged / compressed KV、sparse MLA、Graph replay、storage→GPU direct transfer |

## 掲載方針

対象は特定の最適化方式に限定せず、**LLMの推論・serving・学習・runtime・hardware実行基盤で、そのフレームワークの能力、利用可能な構成、性能特性、memory / I/O / 通信特性、運用方法を実質的に変える主要機能**を広く扱う。

たとえば、推論・生成方式、batchingとscheduling、KV / prefix cache、memory管理、CPU・storage・peer GPUへのoffload、量子化、投機的デコード、MoE、各種parallelismと分散実行、prefill / decode分離、GPU kernelとcompiler最適化、通信・I/O、LoRAやfine-tuning、distributed training、FSDP / ZeRO、activation / optimizer管理、RL rollout連携、multimodal処理、API / serving機能、modelのload・配置・実行方式などを含む。ここに挙げたものは例示であり、**新しい種類の主要機能も、そのフレームワークで「何ができるか」を実質的に広げるなら対象とする**。

「現在できること」は、直近の更新履歴に登場した機能だけではなく、公式documentation・repository・releaseなどから確認できる主要機能全体をまとめる。更新履歴では、その主要機能が新設された場合だけでなく、適用範囲の拡大、構成自由度の向上、性能・memory効率・latency・throughput・通信量・I/O・運用性を実質的に改善する変更も扱う。

一方、単なる対応model追加、allowlist・chat template追加、軽微な互換性変更、既存機能を変えないhardware対応追加、bug / crash / correctness / security修正など、**フレームワークの主要能力を実質的に変えない変更は原則として除外する**。

情報源は公式release、公式PR、公式documentationなど一次資料を優先する。未マージPRはstable機能と分け、Open / Draft状態を明示する。

---

## 最新更新

### 2026-09-08

#### llama.cpp

- **VulkanでTQ1_0量子化weightを直接実行 — merged / release b10831**

  Vulkan backendにTQ1_0の行列積、行列ベクトル積、MoE向けID付き行列積、逆量子化、行抽出を追加した。これによりTQ1_0 weightをVulkan対応GPUでCPU fallbackせず処理できる範囲が広がる。AMD gfx1151でbackend testの対象演算が通過している。Metalは対応kernelがないため、この型の該当演算を明示的にCPU fallbackする。

  一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b10831

- **VulkanのRMSNorm周辺fusion拡張 — merged / release b10833**

  RMSNormの後に続く乗算・加算・view・row書込みなどを融合できるパターンを追加し、中間tensorの書戻しとkernel起動を減らす。release記載の開発者環境ではGemma 4で約4%の改善。環境依存の単一測定値なので一般性能値とは区別する。

  一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b10833

#### その他

- 9月5日以降の確認範囲では、単なるmodel対応、bug / correctness修正だけの変更は掲載対象から除外した。

### 2026-09-05

#### llama.cpp

- **CPUへ退避したMoE expert向けGPU常駐LRU cache — Draft / Open**

  CPU memoryへoffloadしたMoE expertのうち、最近使ったexpertだけをVRAMへ一時保持する提案。

  MoE expertをCPUへ置くとVRAM使用量は減るが、decodeのたびに選ばれたexpert weightをCPU RAMから読むためhost memory bandwidthが律速になりやすい。このPRは「直近で使ったexpertは近いtokenでも再利用されやすい」という**時間局所性（temporal locality）**を利用する。

  LRU（Least Recently Used）は、cacheが満杯になったとき最も長く使っていない項目から追い出す方式。`--moe-expert-cache N`でopt-inし、現状は通常の1-token decodeだけで動作する。

  Qwen3.8-Flash-Next UD-Q4_K_XL、2×RTX 3090で **18.4 → 24.2 tok/s（+31%）**。routing traceから推定したhit率は64 slotsで約67%、128 slotsで約81%。投機的デコードやMTP（Multi-Token Prediction; 複数token予測）のmulti-token stepでは現状cacheを使わない。

  一次資料: https://github.com/ggml-org/llama.cpp/pull/27861

#### vLLM

- **activation関数＋FP8量子化をmodel側から明示的にfusion — merged 2026-09-03**

  compilerが後から自動検出していた「SwiGLU activation → static FP8 quantization」を、model実装側から直接1つのfused kernelへ流せる経路を追加。

  **fusion（融合）**は、別kernelなら中間結果をVRAMへ書いて再読込する複数処理を1 kernelへまとめ、kernel起動回数とmemory trafficを減らす最適化。Llama MLPの`down_proj`前で利用し、manual fusionが発火した場合はcompiler側が二重にfusionしないよう制御する。

  PR本文には独立速度benchmarkがなく、現段階では「fusionを確実に適用できる実装基盤」の拡張として記録する。

  一次資料: https://github.com/vllm-project/vllm/pull/51415

#### その他

- CPU offload / SSD・NVMe offload: 前回確認以降、新規論文・重要revision・upstream統合として追加すべき差分なし。

### 2026-09-04

#### vLLM

- **PDL待機前にweightを先読みするfused Q/KV RMSNorm改善 — merged 2026-09-03**

  PDL（Programmatic Dependent Launch; GPU kernel間の依存起動をGPU側で待つ仕組み）で前処理完了を待つ前に、前処理結果へ依存しないgamma weightを先に読み始める。

  待機時間とmemory loadを重ね、さらにhidden width 2048以上では8 warp化。Kimi-K3 / DeepSeek-V4のattention前段で使うkernelを **4.02 → 3.55 µs（約12%短縮）**。

  一次資料: https://github.com/vllm-project/vllm/pull/55020

- **MLA decodeのquery連結＋KV cache書き込み短縮 — merged 2026-09-03**

  MLA（Multi-head Latent Attention; K/Vを低次元latentへ圧縮して保持するattention）のdecode前処理で、query連結と新KV cache entry書き込みを行うkernelを改善。

  token数に応じて1行を担当するwarp数を変え、依存待ち前に独立loadを進め、後続attention kernelも可能な時点で早く起動する。kernel latencyは **2.95 → 2.06 µs（30%短縮）**、安定decode時のITL（Inter-Token Latency; token間遅延）は **約0.40%短縮**。

  一次資料: https://github.com/vllm-project/vllm/pull/54896

#### その他

- 新規LLMフレームワーク: 該当なし。
- 論文と実装のギャップ: 新たに記録すべき状態変化なし。
- 注視中の未マージPR: 新規登録すべきものなし。
- CPU offload / SSD・NVMe offload: 前回確認以降に新規論文・重要revision・upstream統合として追加すべき差分なし。

---

## フレームワーク別サマリー

以下は **2026-06-03以降** に確認した主要更新の入口。詳細ページでは、略語だけでなく「何をどこへ動かすのか」「何の待ち時間やmemoryを減らすのか」まで説明する。

### 推論エンジン（inference engines）

- [llama.cpp](inference-engines/llama-cpp/) — MoE kernel fusion、DSpark投機的デコード、CUDA Graph、dense FFN CPU offload、CPUへ退避したMoE expert向けGPU LRU cache（Draft）、Vulkan TQ1_0、RMSNorm fusion
- [vLLM](inference-engines/vllm/) — multi-tier KV cache、prefill/decode分離、adaptive speculative decoding、weight offload、MoE通信、activation量子化fusion
- [SGLang](inference-engines/sglang/) — Spec V2、階層cache（HiCache）、MTP、sparse attention、MoE負荷分散、CUDA Graph
- [TensorRT-LLM](inference-engines/tensorrt-llm/) — KVCacheManagerV2、disk KV、投機的デコード、prefill/decode分離、paged attention（v1.3.0 RC群）
- [KTransformers](inference-engines/ktransformers/) — CPU/GPU異種実行、INT4 CPU expert、full-parameter / LoRA SFT、FP8 LoRA
- [Hugging Face Transformers](inference-engines/hugging-face-transformers/) — StaticCache prefill高速化、ensemble speculative decoding
- [Accelerate](inference-engines/accelerate/) — FSDP2 FP8、regional compilation、CPU offload
- [MLX](inference-engines/mlx/) — GQA / attention / quantized MoE kernel、unified memory zero-copy import
- [MLX LM](inference-engines/mlx-lm/) — stableの大きな該当更新なし。MLA multi-token decode、KV cache量子化、recurrent rollback cacheのOpen PRを追跡
- [Ollama](inference-engines/ollama/) — Apple MTP、MoE / NVFP4高速化、metadata cache、prefill restore point
- [ExLlama](inference-engines/exllama/) — ExLlamaV3のexpert / KV CPU offload、dynamic drafting、VRAM slab allocator
- [Mistral.rs](inference-engines/mistral-rs/) — CPU量子化kernel、GQA KV streaming、MTP / DFlash、CUDA Graph
- [ONNX Runtime GenAI](inference-engines/onnx-runtime-genai/) — hardware別model variant、QNN KV zero-copy、INT8 builder
- [OpenVINO GenAI](inference-engines/openvino-genai/) — Dynamic Tree Search speculative decoding、TaylorSeer temporal cache
- [TGI](inference-engines/tgi/) — repository archive済み。対象期間の本質的更新なし
- [LMDeploy](inference-engines/lmdeploy/) — object cache、SSM prefix cache、DeepEPv2、Mooncake KV connector、PDL
- [LightLLM](inference-engines/lightllm/) — Hybrid Radix Cache、GPU→CPU→disk階層、NIXL、RL online weight update
- [FlexFlow Serve](inference-engines/flexflow-serve/) — 対象期間の本質的更新なし
- [Modular MAX](inference-engines/modular-max/) — FP8 / MXint8 KV、tiered KV、VMM allocator、speculative decoding

### 学習フレームワーク（training frameworks）

- [DeepSpeed](training-frameworks/deepspeed/) — AutoEP、parallel folding、MoE grouped-GEMM、async gradient / activation offload
- [Megatron-LM](training-frameworks/megatron-lm/) — Megatron-Core統合、activation recomputation、chunked optimizer-state / master-weight CPU offload
- [Megatron-Core](training-frameworks/megatron-core/) — HybridEP / DeepEP、MoE fusion、CUDA Graph、低精度parameter gather、activation offload
- [TorchTitan](training-frameworks/torchtitan/) — unified MoE token dispatcher、GraphTrainer、FSDP / EP overlap、低精度optimizer

### Hardware runtime

- [ROCm](hardware-runtimes/rocm/) — HIP / RCCL、AITER low-bit MoE、sparse MLA、paged KV、storage→GPU direct transfer

---

## 更新方法

- 新しい重要更新を確認したら、まずこのページ上部の **「最新更新」** に日付付きで追記する。
- 同時に該当フレームワークの **「フレームワーク別サマリー」** と個別READMEを必要に応じて更新する。
- 日次・期間別の新しいMarkdownファイルは原則として作らず、このページをフレームワーク更新の入口・集約ページとして維持する。
- 同一内容の重複記録は避け、Open PRがmerge / closeされた場合など状態変化は既存項目を更新する。
- 未マージPRのbenchmarkは「提案時の測定値」であり、stable releaseの性能値とは分けて扱う。
