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
## 自動生成の論文一覧（23本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-05 | [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md) | ✓ | 1 | 推論 モデルは、通常chat モデルより非常に長い出力を生成することがある。数学問題やコード 推論では数千〜数万トークンの思考連鎖（CoT）を出し続けるため、プロンプトが短くてもデコード中にKV キャッシュが大きく成長する。 |
| 2026-04 | [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md) | ✓ | 1 | 動的疎注意は各デコード段で重要な少数KVだけをGPUへ読み込めば長文注意計算を減らせるが、選択粒度が方式ごとに異なり、CPU上の完全KVから細粒度・不連続なデータをPCIeで取り出す費用が利得を打ち消しやすい。 |
| 2026-04 | [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md) | [✓](https://github.com/yuzhenmao/IceCache) | 1 | IceCacheは、長文推論でGPUに載り切らないKVキャッシュをCPUへ退避する際、重要トークンだけを戻そうとしても元の時系列順ページ配置では意味的に関連するトークンが多数のページへ散らばり、不要トークンまでPCIe転送してしまう問題を、意味的クラスタリングとページ化注意機構を一体化して解く。 |
| 2026-01 | [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md) | ✓ | 1 | 長文生成ではKVキャッシュが生成トークン数に応じて増え、同時実行中の要求数も変化するため、GPUメモリ需要は実行中に継続して変わる。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md) | ✓ | 0 | KV キャッシュ圧縮では「各トークンの重要度をどう採点するか」ばかりが注目されやすい。本論文は、そのスコアをデコード ステップ間でどう蓄積し、保持／削除順位をどれだけ安定させるかも同じくらい重要だと示す。 |
| 2026-09 | [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md) | ✓ | 0 | すべての注意機構 ヘッドを同じように圧縮するのではなく、長文の各部分から重要情報を拾い、それらをまとめて扱うのに強く関与するヘッドへ多くのKV容量を残す。 |
| 2026-09 | [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md) | [✓](https://github.com/SalesforceAIResearch/Random-Attention) | 0 | 推論過程 モデルは、最終回答を出す前に何千〜何万トークンもの思考過程を生成することがある。 |
| 2026-09 | [MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference](2026-2609.07966-metakv-adaptive-kv-cache-compression-for-constrained-llm-inference.md) | [✓](https://github.com/MichaelWang0505/MetaKV.git) | 0 | 同じKVキャッシュ圧縮方式を全リクエストへ固定適用せず、入力プロンプトと利用者が指定した遅延・ピークKVメモリ上限から、各候補方式の遅延、メモリ、正答確率を軽量予測器で見積もり、制約を満たしつつ正答率を保ちやすい圧縮設定をリクエストごとに選ぶ適応型推論制御方式。 |
| 2026-09 | [KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints](2026-2609.10266-kvsharearena-cross-context-checkpoint-reuse.md) | ✓ | 0 | 本論文は、検索拡張生成や複数エージェント連携で、別々に作ったKVキャッシュを新しい文脈へ組み込むと、位置のずれだけでなく、各情報源が互いを見ずに符号化されたため必要な相互作用が欠ける問題を、共通条件で測るベンチマークを提案する。 |
| 2026-09 | [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md) | ✓ | 0 | 長い文脈を持つLLMでは、過去トークンごとのキー/値をKV キャッシュへ保存する。デコードが進むたびにKV キャッシュは増えるため、GPU メモリが足りなくなる。 |
| 2026-09 | [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md) | ✓ | 0 | 最近の長文脈 モデルには、すべての層で通常の全域注意機構を行うのではなく、局所注意機構、recurrent 層、線形-注意機構系層などを混ぜるハイブリッド アーキテクチャが増えている。 |
| 2026-09 | [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md) | ✓ | 0 | 長い推論でKV キャッシュが増え続ける問題に対し、最初から大きな容量を予約するのではなく、そのリクエストが本当に広い過去文脈を必要とし始めた時だけKV用ページを追加する。 |
| 2026-09 | [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](2026-2609.09768-kv-concatenation-aware-recompute.md) | ✓ | 0 | 本論文は、RAGで文書ごとに事前計算したKVキャッシュを連結すると、文書間の相互参照を欠くことと位置の不整合により、長文脈ほど品質が大きく低下する問題を扱う。 |
| 2026-07 | [Lynx: Progressive Speculative Quantization for accelerating KV Transfer in Long-Context Inference](2026-2607.01831-lynx-progressive-kv-transfer.md) | ✓ | 0 | Lynxは、プリフィル・デコード分離型の長文LLM推論で巨大なKVキャッシュをネットワーク転送し終えるまでデコードを開始できない直列化障壁を、KVの重要ビットを段階的に送ることで取り除く。 |
| 2026-06 | [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md) | [✓](https://github.com/aiha-lab/TANGRAM) | 0 | 非一様KVキャッシュ圧縮のヘッド別保持量を少数サンプルで事前較正し、固定予算・ヘッド-グループ単位のragged ページ化・事前負荷分散へ落とし込むvLLMベースのサービング システム。 |
| 2026-06 | [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md) | ✓ | 0 | 長文・複数ターンのLLMサービングでは、GPUメモリ不足時にKVキャッシュを追い出して後で再計算する損失なし管理が必要になるが、従来方式は再利用頻度や位置だけを見ており、どのKVブロックを残すとGPU注意計算そのものがどれだけ速くなるかを十分扱っていない。 |
| 2026-06 | [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md) | [✓](https://github.com/TUDa-HWAI/CompressKV) | 0 | Transformerは生成済みトークンのkey/値をKV キャッシュへ保存することで、次トークンを作るたびに過去トークンを最初から再計算する必要をなくしている。 |
| 2026-05 | [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md) | [✓](https://github.com/hpdps-group/KVServe) | 0 | KVServeは「KVキャッシュ（KV キャッシュ）をどう圧縮するか」だけではなく、今の回線速度・処理負荷・品質条件なら、そもそもどの圧縮方式を使うべきか、あるいは圧縮しない方が速いかを実行時に選ぶ仕組みである。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-03 | [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md) | ✓ | 9 | KVキャッシュは過去トークンのK/Vを再利用することで、自己回帰デコードで過去系列全体を毎回計算し直す必要をなくす。 |
| 2024-02 | [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md) | [✓](https://github.com/ScalingIntelligence/hydragen) | 9 | 少数例 プロンプト、同じシステム プロンプトを使うチャットボット、多数サンプルを生成する自己整合性などでは、バッチ内の複数系列が長い接頭辞を共有する。 |
| 2025-01 | [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md) | ✓ | 3 | 保持するは、distributed LLM 推論で発生するcollective 通信を単なる待ち時間にせず、その間に次に使う重みとKV キャッシュをHBMからon-chip L2 キャッシュへプリフェッチする研究である。 |
| 2025-04 | [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md) | [✓](https://github.com/alibaba/vllm_xformers_prefetch) | 2 | 本研究は、KV キャッシュの容量を減らすのではなく、HBMにあるKVを注意機構 カーネルが使う少し前にGPU L2 キャッシュへ運んでおくことでデコード スループットを高める。 |
| 2025-05 | [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md) | [✓](https://github.com/ydyhello/TailorKV) | 1 | TailorKVは、長文LLMのKVキャッシュを一律に量子化すると重要な外れ値を持つ層で精度が落ち、一律にCPUへオフロードするとPCIe転送が遅すぎる問題を扱う。 |
<!-- survey:auto:end -->
