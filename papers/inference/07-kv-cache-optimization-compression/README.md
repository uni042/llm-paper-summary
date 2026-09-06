# KV Cache Optimization / Compression

収録論文: 3本。公開日が新しい順。

- 2026-09-03 — [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)
  - decode-time KV evictionでEMAによる時間集約とranking保持を使い、score refresh頻度を下げる。
- 2026-09-03 — [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)
  - reasoning中のattention需要に応じてKV cache予算をpage単位で増やす。
- 2026-09-03 — [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)
  - summarization能力の高いattention headへKV budgetを重点配分する。
