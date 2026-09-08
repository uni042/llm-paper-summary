# KV Cache Optimization / Compression

長いcontextやreasoningで増えるKV cacheについて、**残す量を減らす・圧縮する・必要に応じて容量を変える・GPU内で使う直前に高速cacheへ先読みする・shared prefixへの重複accessをまとめる**ことで、VRAM使用量やHBMからの読み出し待ちを抑えながら推論品質とdecode速度を保つ研究をまとめる。

weight offloadとは違い、この系統が対象にするのは推論中に生成・参照されるKV cacheそのものの管理と読み出し効率である。どのtoken / headのKVを残すかだけでなく、HBM上のKVをいつL2 cacheへ運ぶか、shared prefixを複数sequenceでどう効率よく読むか、同じKVを何度も読み直す無駄をどう減らすかも含む。

CPU DRAM・別GPUのHBM・storageへKVを置く方法や、attention計算をGPU外へ移す研究は [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

## 収録論文

収録論文: 11本。公開日が新しい順。

- 2026-09-02 — [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md)
  - hybrid long-context modelのglobal-attention KV headごとに異なる履歴窓を物理割当し、品質を保ちながらGPU上のKV常駐量を減らす。

- 2026-09-03 — [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)
  - KVの重要度を毎tokenで一から計算せず、過去のattention傾向を少しずつ平均して重要度順位を長めに使い回し、どのKVを捨てるか決める計算負荷を下げる。
- 2026-09-03 — [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)
  - KV cacheを最初から大きく確保せず、reasoning中に過去contextへのattention需要が増えた時だけpage単位で容量を追加する。
- 2026-09-03 — [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md)
  - promptを固定保護したうえで生成済みreasoning tokenのKVをheadごとにランダム保持し、重要度score計算なしで品質とserving throughputを両立する。
- 2026-09-03 — [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)
  - 長いcontextの要点を保持する能力が高いattention headへ多くのKV容量を与え、冗長なheadのcacheを強く削減する。
- 2026-06-23 — [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)
  - 意味検索に強いattention headで重要tokenを選び、圧縮誤差が大きいlayerへ多くのKV budgetを配ってlong-context品質を保つ。
- 2026-05-01 — [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)
  - reasoning中に新しく増えたKVだけをwindow単位で周期圧縮し、重要token周辺を可変長chunkとして残してcompression overheadと情報欠落を抑える。
- 2025-04-08 — [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)
  - attentionが現在のKV blockを計算している間に次のK/V blockをHBMからGPUのL2 cacheへ先読みし、次のblockを読む時にGPUがHBM待ちで止まる時間を減らす。
- 2025-01-14 — [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)
  - tensor parallelismでGPU間の結果を集約している待ち時間中に、次に使うweightとKVをHBMからL2 cacheへ先読みし、通信待ちを次のmemory readの準備に使う。
- 2024-03-26 — [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)
  - attentionに効きやすいtokenのKVを優先して残し、sequenceが伸びたら一部をCPUへ退避し、転送より再計算が安い部分はGPUで作り直してKV容量とPCIe転送量を減らす。
- 2024-02-07 — [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)
  - shared prefixと各sequence固有部分のattentionを分け、複数sequenceから同じprefixへ向かうattentionをまとめて計算することで、同じKVをHBMから何度も読む無駄を減らす。

## 主な技術の分岐

- **KVを減らす:** InertiaKV、Random Attention、SGD-KV、CompressKV、KARA、ALISAはKVを選別して保存や読み出しを減らす。Random Attentionは重要度score自体を使わない点が異なる。
- **必要な時だけ容量を増やす:** GrowPageはreasoning中のattention需要が増えた時だけKV容量を追加する。
- **GPU内で先読みする:** Asynchronous KV Cache PrefetchingとPRESERVEは、HBM上のKVを使う直前にL2 cacheへ運び、HBMから読み出す待ち時間を別の計算や通信と重ねる。
- **shared prefixの重複計算を減らす:** Hydragenは共有KVを保存するだけでなく、複数sequenceのattentionをまとめて計算し、同じprefix KVの重複読み出しを減らす。

方向は異なるが、いずれも**KV cacheがdecode時のmemory容量やmemory bandwidthのボトルネックになることを直接緩和する**研究として扱う。
