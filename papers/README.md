# 論文カタログ

収録論文: **147本**。

論文は最終目的で **Inference（推論）** と **Training（学習）** に分け、その下を研究系統別に整理する。Training側は既存19本を保持したまま更新を凍結している。

## Inference / 推論 — 128本

- [Offload / Hierarchical Memory](inference/01-offload-hierarchical-memory/) — 14本
- [Adaptive Expert Computation / Compression](inference/02-adaptive-expert-computation-compression/) — 10本
- [Expert Prefetch](inference/03-expert-prefetch/) — 13本
- [Conditional Computation](inference/04-conditional-computation/) — 8本
- [Speculative Decoding × MoE](inference/05-speculative-decoding-moe/) — 6本
- [MoE Quantization / Compression](inference/06-moe-quantization-compression/) — 13本
- [KV Cache Optimization / Compression](inference/07-kv-cache-optimization-compression/) — 7本
- [Edge / On-device LLM Systems](inference/08-edge-on-device-llm-systems/) — 5本
- [KV Cache Offload / Recomputation](inference/10-kv-cache-offload-recomputation/) — 19本
- [LLM Serving / Scheduling / Disaggregation](inference/11-llm-serving-scheduling-disaggregation/) — 25本
- [Other Inference Systems](inference/99-other-inference-systems/) — 6本

→ [Inference一覧](inference/)

## Training / 学習 — 19本（凍結）

既存内容を参照用として保持するが、通常サーベイでは新規追加・監査・本文更新を行わない。

→ [Training一覧](training/)

## 分類ルール

収集対象は最終目的が推論・serving・decoding・runtime・実行時memory / I/O・on-device inferenceの効率化にある研究。推論高速化のために予測器学習、蒸留、calibration等を内部手段として使う場合もInferenceへ分類する。
