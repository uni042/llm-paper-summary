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
## 自動生成の論文一覧（29本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-05 · [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KARAは、新しく増えたKV区間だけを一度ずつ圧縮し、重要トークンを可変長チャンクへ広げ、周期発動で再圧縮費を抑えて長い推論の同時実行数を保つ。

- **2026-04 · [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SPINは、異なる疎注意方式の選択単位を共通ページへ写し、要求ごとのKV予算とGPU局所性キャッシュを調整して、階層メモリの転送とHBM圧力を減らす。

- **2026-04 · [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md)**  
  実装：[✓](https://github.com/yuzhenmao/IceCache) ・ リポジトリ内被引用：1  
  IceCacheは、意味的に近いKVを同じ物理ページへクラスタ化し、関連ページだけをCPUから一括転送して、長文のGPU KV容量とPCIeデータ量を減らす。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SGD-KVは、要点抽出へ寄与する注意ヘッドを事前診断し、ヘッド別KV容量へ変換して、長文の意味集約に必要な履歴を優先保持する。

- **2026-09 · [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/Random-Attention) ・ リポジトリ内被引用：0  
  Random 注意機構は、入力文を必ず保持し、生成した推論過程のKVだけをヘッド別に無作為保持することで、選択器の採点計算を省き、同じ容量で強い選択法に近い正答率と高い提供スループットを得る。

- **2026-09 · [OmniKVQuant: KV Cache Quantization for Omni-LLMs](2026-2609.11582-omnikvquant-kv-cache-quantization-for-omni-llms.md)**  
  実装：[✓](https://github.com/kaistmm/OmniKVQuant) ・ リポジトリ内被引用：0  
  全モダリティ大規模言語モデルのKVキャッシュに対し、32トークン局所範囲でキー量子化を適応し、モダリティ別回転でバリューを2ビット化して品質劣化を抑える学習不要方式。

- **2026-09 · [MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference](2026-2609.07966-metakv-adaptive-kv-cache-compression-for-constrained-llm-inference.md)**  
  実装：[✓](https://github.com/MichaelWang0505/MetaKV.git) ・ リポジトリ内被引用：0  
  MetaKVは、プロンプトと遅延・KVメモリ制約から候補圧縮方式の結果を予測し、制約内で正答率を保つ設定をリクエストごとに切り替える。

- **2026-09 · [Language Models Can Control Their Own Attention](2026-2609.02737-declarative-attention-self-directed-kv-access.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル自身が思考中に注意範囲を宣言し、推論エンジンがKVブロック表を切り替えて不要な長文脈読出しを省く疎注意方式。Gemma-4-31Bで参照トークンを52.0%削減し、精度低下は1.27ポイントだった。

- **2026-09 · [KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints](2026-2609.10266-kvsharearena-cross-context-checkpoint-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVShareArenaは、文脈・チェックポイントをまたぐKV再利用で位置ずれと情報源間相互作用の欠落を分離測定し、補正・再計算・圧縮の品質と費用を共通基準で比較する。

- **2026-09 · [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jacapは、将来クエリへの注意出力感度と値方向の重複を測り、重要度だけでなく情報の多様性を持つKV集合を選んで、高圧縮時の出力情報欠落を減らす。

- **2026-09 · [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeadWiseKVは、全体注意層のKV履歴を物理KVヘッドごとに較正し、必要な窓だけGPUへ確保して、長文脈の過剰メモリと一律圧縮による品質低下を抑える。

- **2026-09 · [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GrowPageは、生成中の注意参照範囲を短期・長期信号で予測し、容量境界で圧縮継続かKVページ追加かを選んで、推論ごとの過剰予約と必要履歴の削除を抑える。

- **2026-09 · [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](2026-2609.09768-kv-concatenation-aware-recompute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV連結対応学習とCacheBlendの選択的再計算を組み合わせ、文書間相互作用の欠落を15%再計算で補い、RAG長文の品質とSSD読出し・転送待ちを両立する。

- **2026-09 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](2026-2609.04971-beaconkv.md)**  
  実装：[✓](https://github.com/aiha-lab/BeaconKV) ・ リポジトリ内被引用：0  
  長い推論で過去の計画へ再注意する問い合わせを少数のビーコンとして保持し、将来再参照されるKVを予測して残す訓練不要の圧縮方式。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：0  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-07 · [Lynx: Progressive Speculative Quantization for accelerating KV Transfer in Long-Context Inference](2026-2607.01831-lynx-progressive-kv-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LynxはKVを上位ビットのAnchorとResidualへ分割し、Anchor到着後に低精度で投機生成、Residual到着後に一括検証して、分離サービングの転送待ちを隠しつつINT8級品質を保つ。

- **2026-06 · [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md)**  
  実装：[✓](https://github.com/aiha-lab/TANGRAM) ・ リポジトリ内被引用：0  
  Tangramは、ヘッド別KV保持量を少数サンプルで事前較正し、固定予算のraggedページ化と負荷分散へ変換して、非一様圧縮の断片化・回収費・デコード不均衡を減らす。

- **2026-06 · [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AsymCacheは、非連続KV区間を一つの注意カーネルで統合し、再利用確率と再計算遅延で追い出し、負荷適応チャンク化で長文サービングのGPU計算と管理費を減らす。

- **2026-06 · [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：0  
  CompressKVは、意味的証拠を検索する注意ヘッドだけでKVトークンを選び、層ごとの追い出し感度で容量を配分して、同じKV予算で長文品質を保つ。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：0  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

### 2年前（2024-10〜2025-09）

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Preserveは、テンソル並列のGPU間集約通信中に次の重みとKVをHBMからL2へ先読みし、通信待ちとメモリ読出しを重ねて分散推論の遅延を減らす。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：3  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：2  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：2  
  非同期KV先読みは、現在の注意ブロック計算中に次のKVをHBMからL2へ運び、Hopper GPUのメモリ待ちを隠して、注意カーネルとE2Eデコードを速める。

- **2025-07 · [HCAttention: Extreme KV Cache Compression via Heterogeneous Attention Computing for LLMs](2025-2507.19823-hcattention-heterogeneous-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー量子化・値のCPU退避・層別の動的KV削除を統合し、GPU KV予算25%でLlama-3-8BのLongBench平均43.2を全注意と同値に保ち、12.5%でも42.5（0.7ポイント差）に抑える異種GPU/CPU注意方式。

### 3年前（2023-10〜2024-09）

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/hydragen) ・ リポジトリ内被引用：12  
  Hydragenは、共有接頭辞への複数系列のクエリをまとめて計算し、同じKVのHBM読出しを一度に処理して、共有プロンプトの注意帯域と実行効率を改善する。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  ALISAは、重要トークンを残す疎注意とKVのGPU・CPU・再計算配置、INT8量子化を系列長に応じて切替え、容量・PCIe転送・再計算費を抑える。
<!-- survey:auto:end -->
