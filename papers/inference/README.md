# 推論システム研究

収録論文: **332本**。

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

推論論文：**332本**。

| 系統 | 本数 |
|---|---:|
| [01-offload-hierarchical-memory](01-offload-hierarchical-memory/README.md) | 34 |
| [02-adaptive-expert-computation-compression](02-adaptive-expert-computation-compression/README.md) | 14 |
| [02-hardware-accelerators](02-hardware-accelerators/README.md) | 1 |
| [02-moe-expert-placement-caching](02-moe-expert-placement-caching/README.md) | 1 |
| [03-expert-prefetch](03-expert-prefetch/README.md) | 14 |
| [04-conditional-computation](04-conditional-computation/README.md) | 9 |
| [04-moe-expert-offload-caching](04-moe-expert-offload-caching/README.md) | 2 |
| [04-moe-parallelism-communication](04-moe-parallelism-communication/README.md) | 11 |
| [05-kv-cache-memory-management](05-kv-cache-memory-management/README.md) | 1 |
| [05-kv-cache-offloading](05-kv-cache-offloading/README.md) | 6 |
| [05-speculative-decoding-moe](05-speculative-decoding-moe/README.md) | 17 |
| [06-moe-expert-offloading](06-moe-expert-offloading/README.md) | 5 |
| [06-moe-quantization-compression](06-moe-quantization-compression/README.md) | 14 |
| [06-speculative-decoding-moe](06-speculative-decoding-moe/README.md) | 2 |
| [07-kv-cache-optimization-compression](07-kv-cache-optimization-compression/README.md) | 26 |
| [08-edge-on-device-llm-systems](08-edge-on-device-llm-systems/README.md) | 14 |
| [09-attention-kernel-serving-optimization](09-attention-kernel-serving-optimization/README.md) | 3 |
| [10-kv-cache-offload-recomputation](10-kv-cache-offload-recomputation/README.md) | 55 |
| [11-llm-serving-scheduling-disaggregation](11-llm-serving-scheduling-disaggregation/README.md) | 92 |
| [12-benchmarking-modeling-emulation](12-benchmarking-modeling-emulation/README.md) | 1 |
| [09-other-inference-systems](09-other-inference-systems/README.md) | 1 |
| [99-other-inference-systems](99-other-inference-systems/README.md) | 9 |
<!-- survey:auto:end -->