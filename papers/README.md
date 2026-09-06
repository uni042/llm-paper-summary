# 論文カタログ

収録論文: **84本**。

論文はまず最終目的で **Inference（推論）** と **Training（学習）** に分け、その下を研究系統別に整理する。

## Inference / 推論 — 68本

- [Offload / Hierarchical Memory](inference/01-offload-hierarchical-memory/) — 10本
- [Adaptive Expert Computation / Compression](inference/02-adaptive-expert-computation-compression/) — 10本
- [Expert Prefetch](inference/03-expert-prefetch/) — 12本
- [Conditional Computation](inference/04-conditional-computation/) — 8本
- [Speculative Decoding × MoE](inference/05-speculative-decoding-moe/) — 6本
- [MoE Quantization / Compression](inference/06-moe-quantization-compression/) — 13本
- [KV Cache Optimization / Compression](inference/07-kv-cache-optimization-compression/) — 3本
- [Edge / On-device LLM Systems](inference/08-edge-on-device-llm-systems/) — 4本
- [Other Inference Systems](inference/09-other-inference-systems/) — 2本

→ [Inference一覧](inference/)

## Training / 学習 — 16本

- [Training Offload / Memory Systems](training/01-training-offload-memory-systems/) — 11本
- [Distributed / Heterogeneous MoE Training](training/02-distributed-heterogeneous-moe-training/) — 5本

→ [Training一覧](training/)

## 分類ルール

分類は「手法の中で何を使うか」ではなく、**最終的に何を効率化する研究か**で決める。

- 推論・serving・decodingを高速化するために、予測器の学習、蒸留、追加学習、calibrationなどを使う場合 → `inference/`
- 事前学習、fine-tuning、optimizer update、分散学習そのものを効率化する場合 → `training/`
- 学習・推論の両方へ適用できる場合 → 論文の主目的、主要評価、主要metricを優先して分類する

研究系統は固定しない。独立した問題設定・主要技術・評価軸を持つ論文群が増えた場合は、適宜新しい系統を追加・分割・統合する。
