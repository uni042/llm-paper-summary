# KV Cache Optimization / Compression

長いcontextやreasoningで増えるKV cacheについて、**残す量を減らす・圧縮する・budgetを動的に変える・GPU内部のmemory hierarchyで先読みする・shared prefixへのaccessをまとめる**ことで、VRAM使用量やHBM access待ちを抑えながら推論品質とdecode速度を保つ研究をまとめる。

weight offloadとは違い、この系統が対象にするのは推論中に生成・参照されるKV cacheそのものの管理とaccess efficiencyである。どのtoken / headを残すかだけでなく、HBM上のKVをいつL2へ運ぶか、shared prefixを複数sequenceでどう効率よく読むか、cache localityをどう改善するかも含む。

CPU DRAM・peer GPU HBM・storageへKVを置くplacementや、attention computeをGPU外へ移す研究は [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

## 収録論文

収録論文: 7本。公開日が新しい順。

- 2026-09-03 — [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)
  - KVの重要度を毎tokenで一から計算せず、過去のattention傾向を滑らかに蓄積して順位を長めに使い回し、cache削減判断の計算負荷を下げる。
- 2026-09-03 — [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)
  - KV cacheを最初から大きく確保せず、reasoning中に過去contextへのattention需要が増えた時だけpage単位で容量を追加する。
- 2026-09-03 — [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)
  - 長いcontextの要点を保持する能力が高いattention headへ多くのKV容量を与え、冗長なheadのcacheを強く削減する。
- 2025-04-08 — [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)
  - attentionが現在のKV blockを計算している間に次のK/V blockをHBMからGPU L2へ非同期prefetchし、cache missによるwarp stallを計算と重ねて隠す。
- 2025-01-14 — [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)
  - tensor-parallel推論のAllreduce中に次のweightとKVをHBMからL2へ先読みし、communication待ち時間をmemory readへ利用する。
- 2024-03-26 — [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)
  - attentionに効きやすいtokenだけを残し、sequenceが伸びるにつれてKVをGPU保持→CPU offload→GPU再計算へ切り替えて、cache容量とPCIe trafficを減らす。
- 2024-02-07 — [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)
  - shared prefixと各sequence固有suffixのattentionを分離し、共有prefixへの複数queryをまとめてmatrix-matrix計算することで同じKVの重複readを減らす。

## 主な技術の分岐

- **Eviction / compression:** InertiaKV、SGD-KV、ALISAは重要なKVだけを残す、またはbudgetを偏らせる。
- **Dynamic capacity:** GrowPageはreasoning中の需要変化に応じてKV budget自体を増やす。
- **Intra-GPU prefetch:** Asynchronous KV Cache PrefetchingとPRESERVEは、HBM上のKVを使う直前にL2へ運び、HBM latencyを別処理とoverlapする。
- **Shared-prefix attention:** Hydragenは共有KVを保存するだけでなく、複数sequenceのqueryをまとめて同じprefix KVへattentionし、重複memory readとmatrix-vector計算を減らす。

容量削減・access locality改善・shared-prefix access最適化は異なる方向だが、いずれも**KV cacheがdecode時のmemory bottleneckになることを直接緩和する**研究として扱う。