# 推論システム研究

収録論文: **68本**。

推論・serving・decoding・実行時memory/I/O・on-device実行など、**モデルを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

## 系統

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — 10本
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — 10本
- [Expert Prefetch](03-expert-prefetch/) — 12本
- [Conditional Computation](04-conditional-computation/) — 8本
- [Speculative Decoding × MoE](05-speculative-decoding-moe/) — 6本
- [MoE Quantization / Compression](06-moe-quantization-compression/) — 13本
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — 3本
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — 4本
- [Other Inference Systems](09-other-inference-systems/) — 2本
