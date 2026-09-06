# KV Cache Optimization / Compression

長いcontextや長時間のreasoningで増え続けるKV cacheを、**必要度に応じて削る・圧縮する・予算を動的に増減する**ことで、VRAM使用量を抑えながら推論品質とdecode速度を保つ研究をまとめる。

重みoffloadとは違い、この系統が対象にするのは推論中に生成されるattention用のKV cacheである。どのtokenやattention headの情報を残すか、いつcache容量を増やすか、重要度評価そのものにどれだけ計算を使うかが主要な論点となる。

## 収録論文

収録論文: 4本。公開日が新しい順。

- 2026-09-03 — [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)
  - KVの重要度を毎tokenで一から計算せず、過去のattention傾向を滑らかに蓄積して順位を長めに使い回し、cache削減判断の計算負荷を下げる。
- 2026-09-03 — [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)
  - KV cacheを最初から大きく確保せず、reasoning中に過去contextへのattention需要が増えた時だけpage単位で容量を追加する。
- 2026-09-03 — [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)
  - 長いcontextの要点を保持する能力が高いattention headへ多くのKV容量を与え、冗長なheadのcacheを強く削減する。
- 2024-03-26 — [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)
  - attentionに効きやすいtokenだけを残し、sequenceが伸びるにつれてKVをGPU保持→CPU offload→GPU再計算へ切り替えて、cache容量とPCIe trafficを減らす。
