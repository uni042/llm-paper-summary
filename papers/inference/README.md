# 推論システム研究

収録論文: **726本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**modelを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

## 主な系統

以下は主要系統の説明。正確な系統一覧と本数は下の自動生成表を正本とする。

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — model weightやMoE expertをCPU・peer GPU・SSD / Flash等へ置き、転送・計算を協調させてGPU memory不足を補う。
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — tokenやlayerごとに実行expert数を変えたりexpertを統合・代替したりして、MoEの計算・転送・容量を減らす。
- [Expert Prefetch](03-expert-prefetch/) — 将来使うexpertをrouting確定前に予測し、GPU cacheの保持や先読みを制御してweight転送待ち・転送量を減らす。
- [Conditional Computation](04-conditional-computation/) — layer skipping、early exit、token pruning等で入力に応じて不要なTransformer計算を実行しない。
- [Speculative Decoding / MoE](05-speculative-decoding-moe/) — draft候補を並列生成・検証して1回のtarget実行で複数tokenを確定し、MoEではexpert読込・検証costも抑える。
- [MoE Quantization / Compression](06-moe-quantization-compression/) — expert weightを低bit化・pruning・mixed precision等で小さくし、VRAM・bandwidth・計算量を削減する。
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — KV cacheを圧縮・選別・動的配分・GPU内prefetchして、容量とmemory bandwidthの負荷を減らす。
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — smartphoneや個人PCなど、memory・bandwidth・電力制約の厳しい端末でLLMを実行するsystem研究。
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — KVをCPU・peer GPU・SSD等へ置き、必要な転送・attention実行場所・再計算を最適化する。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — request順、batch、prefill / decode分離、KV再利用・移動、GPU配置を調整してserving効率とlatencyを改善する。
- [Other Inference Systems](99-other-inference-systems/) — 推論効率化が主目的だが、まだ独立lineageを作るほど同種研究が集まっていない手法を置く。

<!-- survey:auto:start -->
## 自動生成の収録状況

推論論文：**726本**。

| 系統 | 本数 |
|---|---:|
| [01-offload-hierarchical-memory](01-offload-hierarchical-memory/README.md) | 53 |
| [02-adaptive-expert-computation-compression](02-adaptive-expert-computation-compression/README.md) | 15 |
| [02-cpu-offload](02-cpu-offload/README.md) | 1 |
| [02-hardware-accelerators](02-hardware-accelerators/README.md) | 8 |
| [02-memory-offload](02-memory-offload/README.md) | 1 |
| [02-moe-expert-placement-caching](02-moe-expert-placement-caching/README.md) | 1 |
| [02-moe-inference](02-moe-inference/README.md) | 1 |
| [02-moe-offload](02-moe-offload/README.md) | 2 |
| [03-expert-prefetch](03-expert-prefetch/README.md) | 14 |
| [03-hierarchical-memory](03-hierarchical-memory/README.md) | 2 |
| [03-kv-cache](03-kv-cache/README.md) | 3 |
| [03-moe-expert-offload](03-moe-expert-offload/README.md) | 4 |
| [03-offload-hierarchical-memory](03-offload-hierarchical-memory/README.md) | 3 |
| [04-conditional-computation](04-conditional-computation/README.md) | 9 |
| [04-cpu-ssd-offload](04-cpu-ssd-offload/README.md) | 4 |
| [04-kv-prefix-cache](04-kv-prefix-cache/README.md) | 1 |
| [04-moe-expert-offload-caching](04-moe-expert-offload-caching/README.md) | 2 |
| [04-moe-offload-expert-cache](04-moe-offload-expert-cache/README.md) | 1 |
| [04-moe-offload-routing](04-moe-offload-routing/README.md) | 1 |
| [04-moe-parallelism-communication](04-moe-parallelism-communication/README.md) | 22 |
| [05-kv-cache-compression-quantization](05-kv-cache-compression-quantization/README.md) | 1 |
| [05-kv-cache-memory-management](05-kv-cache-memory-management/README.md) | 7 |
| [05-kv-cache-offloading](05-kv-cache-offloading/README.md) | 7 |
| [05-memory-architecture-near-data](05-memory-architecture-near-data/README.md) | 1 |
| [05-moe](05-moe/README.md) | 2 |
| [05-moe-expert-offload](05-moe-expert-offload/README.md) | 4 |
| [05-offload-hierarchical-memory](05-offload-hierarchical-memory/README.md) | 2 |
| [05-pim-near-memory](05-pim-near-memory/README.md) | 1 |
| [05-speculative-decoding](05-speculative-decoding/README.md) | 5 |
| [05-speculative-decoding-moe](05-speculative-decoding-moe/README.md) | 17 |
| [06-expert-offloading](06-expert-offloading/README.md) | 2 |
| [06-kv-cache-memory](06-kv-cache-memory/README.md) | 14 |
| [06-moe-expert-offloading](06-moe-expert-offloading/README.md) | 5 |
| [06-moe-inference-expert-offloading](06-moe-inference-expert-offloading/README.md) | 3 |
| [06-moe-inference-expert-placement-caching](06-moe-inference-expert-placement-caching/README.md) | 3 |
| [06-moe-quantization-compression](06-moe-quantization-compression/README.md) | 14 |
| [06-serving-scheduling](06-serving-scheduling/README.md) | 16 |
| [06-speculative-decoding](06-speculative-decoding/README.md) | 9 |
| [06-speculative-decoding-moe](06-speculative-decoding-moe/README.md) | 3 |
| [07-kv-cache-optimization-compression](07-kv-cache-optimization-compression/README.md) | 41 |
| [07-speculative-decoding](07-speculative-decoding/README.md) | 1 |
| [08-edge-on-device-llm-systems](08-edge-on-device-llm-systems/README.md) | 18 |
| [08-quantization-kernels](08-quantization-kernels/README.md) | 1 |
| [08-speculative-decoding](08-speculative-decoding/README.md) | 3 |
| [09-attention-kernel-serving-optimization](09-attention-kernel-serving-optimization/README.md) | 3 |
| [09-kernel-runtime-compilation](09-kernel-runtime-compilation/README.md) | 16 |
| [10-kv-cache-offload-recomputation](10-kv-cache-offload-recomputation/README.md) | 77 |
| [10-sparse-attention](10-sparse-attention/README.md) | 1 |
| [11-llm-serving-scheduling-disaggregation](11-llm-serving-scheduling-disaggregation/README.md) | 220 |
| [12-benchmarking-modeling-emulation](12-benchmarking-modeling-emulation/README.md) | 3 |
| [kv-cache](kv-cache/README.md) | 1 |
| [moe](moe/README.md) | 1 |
| [scheduling](scheduling/README.md) | 1 |
| [09-other-inference-systems](09-other-inference-systems/README.md) | 1 |
| [99-other-inference-systems](99-other-inference-systems/README.md) | 74 |
<!-- survey:auto:end -->