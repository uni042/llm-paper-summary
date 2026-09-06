# Adaptive Resource / Quality-Cost Optimization

収録論文: 4本。公開日が新しい順。

- 2026-09-03 — [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)
  - decode-time KV evictionでEMAによる時間集約とranking保持を利用し、score refresh頻度を下げながら品質とthroughputを両立する。
- 2026-09-03 — [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)
  - reasoning中のattention需要変化をonline signalから推定し、KV cache予算をpage単位で必要時だけ増やす。
- 2026-09-03 — [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)
  - summarization能力の高いattention headへKV budgetを重点配分し、long-context品質を保ちながらKV memoryを削減する。
- 2026-06-29 — [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)
  - router寄与が小さく転送・実行コストが高いexpertをstraggler-awareに省き、既存active expertへ寄与を再配分して多デバイスMoEを高速化する。
