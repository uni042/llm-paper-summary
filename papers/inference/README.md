# 推論システム研究

収録論文: **133本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**modelを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

## 系統

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — 14本
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — 10本
- [Expert Prefetch](03-expert-prefetch/) — 13本
- [Conditional Computation](04-conditional-computation/) — 8本
- [Speculative Decoding × MoE](05-speculative-decoding-moe/) — 6本
- [MoE Quantization / Compression](06-moe-quantization-compression/) — 13本
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — 9本
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — 5本
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — 19本
  - KVをCPU DRAM・別GPU HBM・storageへ置く、必要subsetだけを検索する、attentionをKVの近くへ移す、先読みや再計算を使うなどしてlocal HBM容量と転送待ちを減らす。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — 27本
  - request順、batch、P/D GPU配分、KV再利用・stage間転送、request移動を調整してlatency・SLO・resource効率を改善する。
- [Other Inference Systems](99-other-inference-systems/) — 7本
  - 推論効率化を主目的とするが、まだ独立系統を作るほど同種研究が集まっていない手法を一時的に収録する。
