# フレームワーク更新

主要LLMフレームワークの、本質的な機能・性能更新を**この1ページで継続管理**する。

最終更新: **2026-09-04**

## 掲載方針

offload、MoE、expert cache／prefetch、dynamic routing、speculative decoding、quantization、kernel、parallelism、memory management、I/O方式、実質的なhardware性能改善を対象とする。

単なる新モデル対応、allowlist・chat template追加、軽微な互換性変更、bug／crash／correctness／security fixのみの変更は原則として除外する。

情報源は公式release、公式PR、公式documentationなど一次資料を優先する。

---

## 最新更新

### 2026-09-04

#### vLLM

- **[Perf] Prefetch the weight before the PDL wait in fused_q_kv_rmsnorm — merged 2026-09-03**  
  Programmatic Dependent Launch (PDL; プログラム依存起動) の待機前に依存しないgamma weight loadを先行させ、さらに幅2048以上では8 warp化することで、Kimi-K3 / DeepSeek-V4のattention frontendで使うfused Q/KV RMSNorm kernelを **4.02 → 3.55 µs（約12%短縮）**。演算順序・出力は不変。weight prefetchとGPU依存待ちのオーバーラップというruntime/kernel-levelの性能前進として収録。  
  一次資料: https://github.com/vllm-project/vllm/pull/55020

- **[Perf][Kimi-K3] Cut MLA decode concat/cache epilogue latency — merged 2026-09-03**  
  Multi-head Latent Attention (MLA; 潜在表現型Attention) decodeのquery concat + KV cache insert kernelで、token数に応じたwarp-per-row分割、依存待ち前の独立load、consumer FMHAのearly triggerを組み合わせた。kernel latencyは **2.95 → 2.06 µs（30%短縮）**、stable decode ITLは **約0.40%短縮**。モデル固有kernelではあるが、PDLとcache writeのcritical pathを縮める実装技法として記録。  
  一次資料: https://github.com/vllm-project/vllm/pull/54896

#### その他

- 新規LLMフレームワーク: 該当なし。
- 論文と実装のギャップ: 新たに記録すべき状態変化なし。
- 注視中の未マージPR: 新規登録すべきものなし。
- CPU offload / SSD・NVMe offload: 前回確認以降に新規論文・重要revision・upstream統合として追加すべき差分なし。

---

## フレームワーク別サマリー

以下は **2026-06-03以降** に確認した主要な更新を集約したもの。詳細ページがあるものはリンク先に個別の一次資料・更新内容を残す。

### Inference engines

- [llama.cpp](inference-engines/llama-cpp/) — MoE fusion、DSpark、CUDA Graph、CPU FFN offload
- [vLLM](inference-engines/vllm/) — multi-tier KV、P/D分離、adaptive speculative decoding、weight offload、PDL待機とweight loadのoverlap、MLA decode cache epilogue短縮
- [SGLang](inference-engines/sglang/) — Spec V2、HiCache、DSpark、MoE／通信kernel
- [TensorRT-LLM](inference-engines/tensorrt-llm/) — KVCacheManagerV2、disk KV、DFlash／DSpark、disaggregated serving（pre-release）
- [KTransformers](inference-engines/ktransformers/) — RAWINT4 CPU expert、heterogeneous SFT、FP8 LoRA
- [Hugging Face Transformers](inference-engines/hugging-face-transformers/) — StaticCache prefill高速化、ensemble speculative decoding
- [Accelerate](inference-engines/accelerate/) — FSDP2 FP8、regional compilation、CPU offload
- [MLX](inference-engines/mlx/) — GQA／attention／quantized MoE kernel、zero-copy import
- [MLX LM](inference-engines/mlx-lm/) — stableでの大きな該当更新なし。MLA decodeとKV量子化のOpen PRを継続確認
- [Ollama](inference-engines/ollama/) — Apple MTP、MoE／NVFP4高速化、metadata／prefill cache
- [ExLlama](inference-engines/exllama/) — ExLlamaV3のexpert／KV CPU offload、dynamic drafting
- [Mistral.rs](inference-engines/mistral-rs/) — CPU kernel、MTP／DFlash、CUDA Graph
- [ONNX Runtime GenAI](inference-engines/onnx-runtime-genai/) — model variant package、QNN KV zero-copy、INT8 builder
- [OpenVINO GenAI](inference-engines/openvino-genai/) — Dynamic Tree Search、TaylorSeer cache
- [TGI](inference-engines/tgi/) — 本質的な新規更新なし（archive済み）
- [LMDeploy](inference-engines/lmdeploy/) — object cache、SSM prefix cache、DeepEPv2、Mooncake KV
- [LightLLM](inference-engines/lightllm/) — Hybrid Radix Cache、GPU→CPU→disk階層、NIXL
- [FlexFlow Serve](inference-engines/flexflow-serve/) — 本質的な新規更新なし
- [Modular MAX](inference-engines/modular-max/) — FP8／MXint8 KV、tiered KV、VMM allocator、speculative decoding

### Training frameworks

- [DeepSpeed](training-frameworks/deepspeed/) — AutoEP、MoE grouped-GEMM、async gradient／activation offload
- [Megatron-LM](training-frameworks/megatron-lm/) — Megatron-Core更新、CPU optimizer offload
- [Megatron-Core](training-frameworks/megatron-core/) — HybridEP／DeepEP、MoE fusion、CUDA Graph、低精度学習
- [TorchTitan](training-frameworks/torchtitan/) — unified MoE dispatcher、GraphTrainer、低精度optimizer

### Hardware runtimes

- [ROCm](hardware-runtimes/rocm/) — HIP／RCCL、AITER low-bit MoE、sparse MLA、paged KV

---

## 更新方法

- 新しい重要更新を確認したら、まずこのページ上部の **「最新更新」** に日付付きで追記する。
- 同時に該当フレームワークの **「フレームワーク別サマリー」** を必要に応じて更新する。
- 日次・期間別の新しいMarkdownファイルは原則として作らず、このページをフレームワーク更新の入口・集約ページとして維持する。
- 同一内容の重複記録は避け、既存項目の状態変化は同じ項目を更新する。
