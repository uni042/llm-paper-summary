# KV Cache Optimization / Compression

長いcontextやreasoningで増えるKV cacheについて、**残す量を減らす・圧縮する・必要に応じて容量を変える・GPU内で使う直前に高速cacheへ先読みする・shared prefixへの重複accessをまとめる**ことで、VRAM使用量やHBMからの読み出し待ちを抑えながら推論品質とdecode速度を保つ研究をまとめる。

weight offloadとは違い、この系統が対象にするのは推論中に生成・参照されるKV cacheそのものの管理と読み出し効率である。どのtoken / headのKVを残すかだけでなく、HBM上のKVをいつL2 cacheへ運ぶか、shared prefixを複数sequenceでどう効率よく読むか、同じKVを何度も読み直す無駄をどう減らすかも含む。

CPU DRAM・別GPUのHBM・storageへKVを置く方法や、attention計算をGPU外へ移す研究は [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

## 主な技術の分岐

- **KVを減らす:** InertiaKV、Random Attention、SGD-KV、CompressKV、KARA、ALISAはKVを選別して保存や読み出しを減らす。Random Attentionは重要度score自体を使わない点が異なる。
- **必要な時だけ容量を増やす:** GrowPageはreasoning中のattention需要が増えた時だけKV容量を追加する。
- **GPU内で先読みする:** Asynchronous KV Cache PrefetchingとPRESERVEは、HBM上のKVを使う直前にL2 cacheへ運び、HBMから読み出す待ち時間を別の計算や通信と重ねる。
- **shared prefixの重複計算を減らす:** Hydragenは共有KVを保存するだけでなく、複数sequenceのattentionをまとめて計算し、同じprefix KVの重複読み出しを減らす。

方向は異なるが、いずれも**KV cacheがdecode時のmemory容量やmemory bandwidthのボトルネックになることを直接緩和する**研究として扱う。

<!-- survey:auto:start -->
## 自動生成の論文一覧（12本）

| 論文 | 一文要約 |
|---|---|
| [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md) | ハイブリッド長文脈モデルで全域注意（global attention）の物理KV headごとに異なる履歴窓を静的配分し、品質を保ちながらGPU上のKVキャッシュ量を減らす学習不要の方式。 |
| [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md) | 意味検索に強いattention headを選び、そのheadが重要と判断したtokenを優先保持しつつ、圧縮誤差が大きいlayerへ多くのKV budgetを配るlong-context KV圧縮手法。 |
| [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md) | 分離型LLM推論で帯域・品質条件・サービス水準目標を観測し、KVキャッシュの圧縮構成を動的に選んでKV転送待ちを減らす。 |
| [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md) | reasoning中に新しく増えたKVだけを周期的なsliding windowで圧縮し、重要tokenから可変長chunkへ拡張して保持することで、圧縮overheadと意味情報の欠落を抑える。 |
| [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md) | attentionが現在のKV blockを計算している間に、次に使うKV blockをHBMからGPUのL2 cacheへ先読みし、decode中のHBM待ちを減らすHopper向け最適化。 |
| [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md) | tensor parallel推論のGPU間集約通信中に、次に使うweightとKV cacheをHBMからL2 cacheへ先読みし、通信待ちとmemory readを同時に進める分散推論手法。 |
| [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md) | attentionで重要な過去tokenだけを参照し、sequenceが伸びるにつれてKVをGPU保持・CPU退避・GPU再計算へ切り替えることで、KV容量とPCIe転送を減らす手法。 |
| [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md) | 同じ長いprefixを共有する複数sequenceのqueryをまとめて処理し、共有KVをsequenceごとに何度もHBMから読み直す無駄を減らすexact attention手法。 |
| [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md) | KVの重要度を毎tokenで一から計算し直さず、過去のattention傾向を滑らかに蓄積して重要tokenの順位を数step使い回すことで、90%級のKV圧縮でもdecode時の管理costを減らす手法。 |
| [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md) | reasoning中に「過去contextをどれだけ広く参照し始めたか」を追跡し、必要な時だけKV cache容量をpage単位で少しずつ増やすserving方式。 |
| [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md) | promptを固定保護したうえで生成済みreasoning tokenのKVをattention headごとにランダム保持し、重要度score計算なしで高い品質とserving throughputを両立する。 |
| [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md) | 長いcontextの要点を保持しやすいattention headへ多くのKV容量を配り、重要度の低いheadでは強くKVを削ることで、最大75%のKV cache削減でも品質を保つ手法。 |
<!-- survey:auto:end -->
