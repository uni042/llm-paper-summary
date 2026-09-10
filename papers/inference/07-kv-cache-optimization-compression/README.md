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
## 自動生成の論文一覧（17本）

| 論文 | 一文要約 |
|---|---|
| [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md) | KV tokenを個別のattention scoreだけで順位付けするのではなく、『残したtoken集合が、今後queryが少し変わった時にattention出力をどれだけ豊かに変化させられるか』を情報容量として評価する。Jacobianはqueryの微小変化がoutputへどう伝わるかを表し、softmaxの競争・keyの到達性・valueが作るoutput方向を統合する。実用版はこれをsoftmax-sensitive weightとweighted leverage scoreへ近似し、重要度だけでなく似たtokenばかり残す冗長性も避ける。高圧縮LongBench/NIAHで強いが、AIME25 8192-token budgetではCapKVに負ける条件もある。 |
| [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md) | 長いreasoning中のKV cacheを圧縮する際、attention score等で重要tokenを選ぶのではなく、system prompt・user questionを含むprefill部分は必ず残し、model自身が生成したreasoning tokenだけをKV headごとに独立ランダム保持する。reasoning traceは必要情報を文章中で繰り返し、さらにheadごとに別sampleを残すため冗長性が高いという観察を利用する。4 models・6 reasoning tasksで強いselectorと概ね同等のaccuracyを保ちながら、score計算を省くことでvLLM serving throughputを32〜43%上回る。 |
| [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md) | hybrid LLMに少数残っているglobal-attention層のKV cacheを、全headで同じ長さ保持するのではなく、物理KV headごとに8K/16K/32K/fullなど異なる履歴窓へ静的配分する。SeqCalibは下位layerですでに短縮したcacheを実際に適用した状態で次layerを較正し、最短で許容品質を満たす窓を選ぶ。runtimeはmaskで隠すだけでなく選んだ長さ分しかKVを物理確保しないため、Qwen3.6-27Bで112K context時のpeak device memoryを8.59%削減し、検証済み最大contextを114Kから161Kへ拡張した。 |
| [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md) | GQA modelの全attention headを一律に平均してtoken重要度を決めると、局所patternを見るheadが長距離の意味検索signalを薄める。CompressKVはprompt先頭・末尾だけでなく中間の意味的証拠とその周辺を正しく拾えるSemantic Retrieval Headをofflineで特定し、そのheadだけをtoken保持判定へ使う。さらにfull-cache attention outputとの差からlayerごとのeviction sensitivityを測り、同じ総KV budgetを圧縮に弱いlayerへ多く配る。 |
| [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md) | 分離型LLM推論で巨大なKV cacheをnetwork/storage境界越しに運ぶ際、圧縮方式を固定せず、workload・実効帯域・SLO・品質下限に応じて圧縮profileを選択するsystem。圧縮処理自体が通信削減より遅い状況では圧縮しない判断も含め、KV移動のend-to-end latencyを最小化する。 |
| [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md) | 長いreasoning出力で増え続けるKVを、cache長が閾値を超えるたび過去全体へ再圧縮するのではなく、直近に新しく生成されたwindowだけ一度ずつ処理する。window内では双方向attentionから重要tokenを選び、連続する候補tokenを端点として可変長semantic chunkへ拡張する。さらにPagedAttention block単位の周期的compressionへ変換したKvLLMで、batch concurrencyが増えてもcompression triggerが爆発しないようにする。 |
| [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md) | attentionが現在のKV blockを計算している間に、次に使うKV blockをHBMからGPUのL2 cacheへ先読みし、decode中のHBM待ちを減らすHopper向け最適化。 |
| [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md) | tensor parallel推論のGPU間集約通信中に、次に使うweightとKV cacheをHBMからL2 cacheへ先読みし、通信待ちとmemory readを同時に進める分散推論手法。 |
| [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md) | attentionで重要な過去tokenだけを参照し、sequenceが伸びるにつれてKVをGPU保持・CPU退避・GPU再計算へ切り替えることで、KV容量とPCIe転送を減らす手法。 |
| [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md) | 同じ長いprefixを共有する複数sequenceのqueryをまとめて処理し、共有KVをsequenceごとに何度もHBMから読み直す無駄を減らすexact attention手法。 |
| [MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference](2026-2609.07966-metakv-adaptive-kv-cache-compression-for-constrained-llm-inference.md) | 同じKVキャッシュ圧縮方式を全リクエストへ固定適用せず、入力プロンプトと利用者が指定した遅延・ピークKVメモリ上限から、各候補方式の遅延、メモリ、正答確率を軽量予測器で見積もり、制約を満たしつつ正答率を保ちやすい圧縮設定をリクエストごとに選ぶ適応型推論制御方式。 |
| [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md) | decode中のKV evictionでは重要度score式だけでなく、scoreを時間方向にどう蓄積するかが保持tokenの順位を大きく左右すると分析。attention scoreをEMAで蓄積するInertiaKVと、score更新を数stepおきに間引くInertiaKV-Lazyを提案する。 |
| [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md) | 推論中に注意参照範囲の広がりをオンライン推定し、固定KV容量の中で圧縮を続けるか、PagedAttentionの物理pageを1枚追加するかをrequestごとに動的決定するKV cache budget制御。 |
| [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md) | 長文の意味をまとめて扱うのに寄与するattention headを診断taskで特定し、そのheadへKV cache budgetを重点配分するhead-aware圧縮。25%のKV budget（75%削減）でも長文taskの精度低下を抑える。 |
| [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md) | 非一様KVキャッシュ圧縮のhead別保持量を少数サンプルで事前較正し、固定予算・head-group単位のragged paging・事前負荷分散へ落とし込むvLLMベースのserving system。動的な非一様圧縮の精度をほぼ保ちながらfragmentation、page reclaim、decode workload imbalanceを解消し、実機で最大2.6倍のthroughputを報告する。 |
| [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md) | 長文・複数ターンのLLMサービングでは、GPUメモリ不足時にKVキャッシュを追い出して後で再計算する損失なし管理が必要になるが、従来方式は再利用頻度や位置だけを見ており、どのKVブロックを残すとGPU注意計算そのものがどれだけ速くなるかを十分扱っていない。AsymCacheは、非連続に残った複数KV区間を1回のGPU注意カーネルで処理する複数区間注意（Multi-Segment Attention; MSA）、再利用確率と位置依存の再計算遅延を掛け合わせる追い出し器、負荷に応じてプリフィル分割量を変える適応チャンク化を統合する。vLLM上のH20実機評価で、最新比較対象に対し先頭トークン時間を最大1.90〜2.03倍、出力トークン当たり時間を1.62〜1.71倍改善し、出力値は近似せず保持する。 |
| [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md) | 長文LLM推論で増大するKVキャッシュをGPUとCPUの間で要求ごとに動的再配置し、転送待ちを計算へ重ねることでトークン遅延SLOとスループットを改善する推論提供システム。 |
<!-- survey:auto:end -->
