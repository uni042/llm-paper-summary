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
## 自動生成の論文一覧（174本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：7  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2025-11 · [TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection](2025-token-select.md)**  
  実装：[✓](https://github.com/pzs19/TokenSelect) ・ リポジトリ内被引用：6  
  各問い合わせで重要な鍵値をトークン単位に選び、ヘッド軟投票・選択キャッシュ・ページ化内積カーネルで長文脈注意を高精度かつ高速化する。

- **2026-05 · [LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents](2026-2602.01053-lragent-multilora-agent-kv-sharing.md)**  
  実装：[✓](https://github.com/jeonhye/lragent) ・ リポジトリ内被引用：5  
  multi-LoRAエージェントのKVを共有基盤成分と低ランク役割成分へ分解し、後者を全次元化せず注意計算することで、長い共有履歴のKVメモリと再プリフィルを削減する。

- **2026-05 · [Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management](2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  PBKVは履歴workflowと現在のタスク 文脈から数段階先のagent呼出しを予測し、その予測から各KV entryの将来再利用可能性を算出する。

- **2026-07 · [LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning](2026-lazyeviction.md)**  
  実装：[✓](https://github.com/Halo-949/LazyEviction) ・ リポジトリ内被引用：4  
  一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：4  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

- **2025-11 · [TiDAR: Think in Diffusion, Talk in Autoregression](2025-2511.08923-tidar-think-in-diffusion-talk-in-autoregression.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  拡散による並列下書きと自己回帰による因果的確定を構造化注意マスクで同一前向き計算へ統合し、正確なKVキャッシュと高い生成スループットを両立する。

- **2025-11 · [KV Cache Transform Coding for Compact Storage in LLM Inference](2025-2511.01815-kv-cache-transform-coding-for-compact-storage-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KVTCは共通の主成分分析基底でKVキャッシュの相関を減らし、重要度別の量子化と無損失符号化で保存量を縮める。16倍目標で多くの課題品質を概ね保ち、H100の8K文脈では復号再利用がKV再計算よりTTFTを約8倍短縮したが、処理時間と強圧縮時の品質低下も示す。

- **2026-07 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2026-ojakv.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：3  
  重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。

- **2026-07 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2026-2607.17715-c2kv-compressed-composable-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/s7a9/C2KV) ・ リポジトリ内被引用：3  
  文書ごとに位置非依存で直接連結できる圧縮KVを学習抽出し、非prefix再利用のプリフィル削減とKV保存・転送・デコード帯域削減を同時に狙う。

- **2026-06 · [STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control](2026-2606.08382-star-kv-adaptive-low-rank-cache-compression.md)**  
  実装：[✓](https://github.com/PriyanshBhatnagar/STAR-KV) ・ リポジトリ内被引用：3  
  特異値の学習可能なしきい値で層・ヘッドごとのKV低ランク次元を自動配分し、鍵/値で異なる分解と低ランク対応混合精度量子化を組み合わせ、強い圧縮を実GPU高速化へつなげる。

- **2026-04 · [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](2026-2604.04921-triattention-efficient-long-reasoning-with-trigonometric-kv-compression.md)**  
  実装：[✓](https://github.com/WeianMao/triattention) ・ リポジトリ内被引用：3  
  長い推論列で「今のクエリに強く注意されるKV」だけを残すのではなく、回転位置埋め込み（Rotary Position Embedding; RoPE）前のクエリ・キーが固定中心の周囲へ集中する性質から、将来の距離ごとの注意傾向を三角関数として予測する。

- **2026-06 · [RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention](2026-2606.06256-redknot-efficient-long-context-llm-serving-with-head-aware-kv-reuse-and-segpagedattention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来のKV管理は全ヘッドを同じトークンブロックとして扱うが、RedKnotの測定では局所ヘッドが83.4〜96.8%、接頭辞変化に敏感な大域ヘッドは3.2〜16.6%に留まる。そこで大域ヘッドだけを広範囲に再計算し、局所ヘッドを再利用するElastic Sparsityと、ヘッド別のKVページを扱うSegPagedAttentionを組み合わせる。

- **2026-04 · [When Hidden States Drift: Can KV Caches Rescue Long-Range Speculative Decoding?](2026-2604.26412-when-hidden-states-drift-can-kv-caches-rescue-long-range-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号では小さなドラフト器が複数トークンを先に提案し、大きな対象モデルがまとめて検証する。診断基盤KVShotでQwen3-8Bを対象に隠れ状態のみ、KVのみ、混成を比較すると、KV再利用は遠いstepの受理率を改善する。

- **2026-04 · [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md)**  
  実装：[✓](https://github.com/yuzhenmao/IceCache) ・ リポジトリ内被引用：2  
  IceCacheは、意味的に近いKVを同じ物理ページへクラスタ化し、関連ページだけをCPUから一括転送して、長文のGPU KV容量とPCIeデータ量を減らす。

- **2026-03 · [LongFlow: Efficient KV Cache Compression for Reasoning Models](2026-2603.11504-longflow-efficient-kv-cache-compression-for-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  現在クエリと注意の寄与ベクトルからKV重要度をほぼ追加状態なしで求め、融合カーネル内で追い出して長い推論出力のKV帯域・容量を削減する。

- **2026-02 · [You Need an Encoder for Native Position-Independent Caching](2026-2602.01519-you-need-an-encoder-for-native-position-independent-caching.md)**  
  実装：[✓](https://github.com/shijuzhao/Comb) ・ リポジトリ内被引用：2  
  凍結したデコーダ専用LLMへPIC専用エンコーダを追加し、任意順序の文書KV再利用を高精度化しつつTTFTを51〜94%削減、KV容量も約75%以上削減するCOMBを提案。

- **2025-12 · [MEPIC: Memory Efficient Position Independent Caching for LLM Serving](2025-2512.16822-mepic-position-independent-chunk-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  位置非依存KVをページ境界へ正規配置し、最初の1ブロックだけ再計算、RoPEを注意時に融合することで、同一チャンクのHBMページを要求間共有し、既存PICよりHBM重複と再計算を大幅に減らす。

- **2025-12 · [Efficient Low Rank Attention for Long-Context Inference in Large Language Models](2025-2510.23649-efficient-low-rank-attention-for-long-context-inference-in-large-languag.md)**  
  実装：[✓](https://github.com/tenghuilee/LRQK) ・ リポジトリ内被引用：2  
  Q・Kを共同低ランク化した代理注意でtop-k KVを選び、必要な完全精度KVだけCPUから戻すことで、長文脈のGPUメモリと転送量を抑える。

- **2025-11 · [PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel](2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md)**  
  実装：[✓](https://github.com/flashserve/PAT) ・ リポジトリ内被引用：2  
  共有接頭辞を要求間で一度だけ読む詰込みと動的タイル選択により、復号注意の大域メモリ読出しと実行空洞を同時に削減する。

- **2026-09 · [Language Models Can Control Their Own Attention](2026-2609.02737-declarative-attention-self-directed-kv-access.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル自身が思考中に注意範囲を宣言し、推論エンジンがKVブロック表を切り替えて不要な長文脈読出しを省く疎注意方式。Gemma-4-31Bで参照トークンを52.0%削減し、精度低下は1.27ポイントだった。

- **2026-09 · [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](2026-2609.19969-deepseek-v4.1-flash-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CED・CSA2の層間KV再利用・FP4 KV・SWA限定再実行を統合し、100万トークン対応552B MoEのグローバルKVを890 bytes/トークン、永続KVを前世代比約1/8へ圧縮する。

- **2026-08 · [GraniKV: Asymmetric Granularity KV-Cache Paging for Multi-Agent Systems with Long Shared Prefix](2026-2608.15584-granikv-asymmetric-granularity-kv-cache-paging-for-multi-agent-systems-w.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  multi-agent LLMではシステム プロンプト、tool定義、共有メモリなど非常に長い接頭辞を複数リクエストが共有する一方、各agentが生成するsuffixは長さも寿命も異なる。16K共有接頭辞ではproduction 比較対象比で出力-トークン スループットを2.16倍、1.98倍、1.57倍へ改善する。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：1  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-07 · [REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression](2026-real-kv.md)**  
  実装：[✓](https://github.com/yonseicasl/REAL) ・ リポジトリ内被引用：1  
  成功例だけでなく偏り・注意散漫を含む4種の注意挙動を測り、推論に重要なヘッドへKV予算を重点配分することで、長文脈の精度を保ちながらキャッシュを圧縮する。

- **2026-07 · [KVpop：将来注意を用いた予測型オンラインKVキャッシュ枝刈り](2026-2607.05061-kvpop-key-value-cache-compression-with-predictive-online-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己回帰生成では過去トークンのキー・値状態をKVキャッシュへ保持するため、文脈長に比例してメモリ容量と読出し帯域が増える。既存の追い出し方式は累積注意量などの代理指標を使うことが多いが、「今まで重要だったトークン」が今後も重要とは限らず、推論途中で関連性が変わると誤った追い出しが起きる。

- **2026-07 · [HYPIC: Accelerating Hybrid-Attention LLM Serving with Position-Independent Caching](2026-2607.01299-hypic-hybrid-attention-position-independent-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  線形注意区間の累積遷移演算子とゼロ始動状態を保存して位置非依存に合成し、完全注意層は境界窓だけ再計算、未保存区間は複数実体で並列処理することで、ハイブリッド注意言語モデルの初トークン待ち時間を平均3.25倍短縮する。

- **2026-07 · [HiKV: Hierarchical Importance-Aware KV Cache with Hardware Acceleration for LLM Decoding](2026-2607.22389-hikv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HiKVは、長文脈デコードでKVキャッシュが外部メモリアクセスの大部分を占める問題に対し、トークン単位と要素単位という二つの独立した冗長性を順番に削るアルゴリズム・ハードウェア協調設計である。1%以内の精度低下という同一条件で外部メモリアクセスを平均7.17倍削減し、注意計算を平均5.70倍、最大7.95倍高速化し、エネルギーを80〜90%削減する。

- **2026-06 · [RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference](2026-2606.31519-rabitqcache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈大規模言語モデルでは、復号の各ステップで巨大なKVキャッシュから注意計算用データを読むことがメモリ帯域のボトルネックになる。RaBitQCacheはランダム回転と二値量子化で小型索引を作り、不偏な注意スコア推定から累積確率に応じて必要量を変える上位確率検索（Top-p）を行う。

- **2026-06 · [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AsymCacheは、非連続KV区間を一つの注意カーネルで統合し、再利用確率と再計算遅延で追い出し、負荷適応チャンク化で長文サービングのGPU計算と管理費を減らす。

- **2026-06 · [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：1  
  CompressKVは、意味的証拠を検索する注意ヘッドだけでKVトークンを選び、層ごとの追い出し感度で容量を配分して、同じKV予算で長文品質を保つ。

- **2026-05 · [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KARAは、新しく増えたKV区間だけを一度ずつ圧縮し、重要トークンを可変長チャンクへ広げ、周期発動で再圧縮費を抑えて長い推論の同時実行数を保つ。

- **2026-05 · [Dynamic-dLLM: Dynamic Cache-Budget and Adaptive Parallel Decoding for Training-Free Acceleration of Diffusion LLM](2026-2606.26120-dynamic-dllm-cache-budget-parallel-decoding.md)**  
  実装：[✓](https://github.com/TianyiWu233/DYNAMIC-DLLM) ・ リポジトリ内被引用：1  
  層別キャッシュ更新量とトークン別確定基準を動的化し、追加学習なしで最大4.48倍の拡散型LLM推論高速化を実現する。

- **2026-05 · [AgentKVShift: Efficient KV Cache Reuse for Agentic Memory Systems](2026-2607.21604-agentkvshift-agentic-memory-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  構造化エージェントメモリの一部トークンだけを再計算し、そこから推定したメモリ単位のKV残差を未再計算トークン全体へ加えて、低い再計算率で品質を回復する。

- **2026-04 · [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SPINは、異なる疎注意方式の選択単位を共通ページへ写し、要求ごとのKV予算とGPU局所性キャッシュを調整して、階層メモリの転送とHBM圧力を減らす。

- **2026-04 · [Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs](2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-devic.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全トークンを同じ低bitへ量子化すると重要トークンまで強く圧縮し、逆に高bit固定では重要でないトークンへbitを浪費する。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [VestigeKV: The NoPE-MLA KV Cache Carries Its Own Eviction Signal in a Vestigial Branch](2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-eviction-signal-in-a-ves.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈のKVキャッシュ圧縮では、H2OやSnapKVのように「これまで高い注意重みを受けたトークン」を重要とみなす方法が一般的である。論文はNoPE-MLA上でこの不一致が顕著で、8倍圧縮時の探索対象 検索がH2Oで0.00、SnapKVで0.33まで崩れると報告する。

- **2026-09 · [Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management](2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-mana.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数LLMを品質・価格・遅延に応じて切り替えるモデルルーティングは、単一モデル固定より効率的になり得る。8種類のワークロードを使う解析シミュレーションでは、キャッシュ準備時間をTTFTの代理指標として1.25〜13.28倍、入力トークン費用を1.20〜6.16倍改善する可能性を報告する。

- **2026-09 · [To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems](2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-.md)**  
  実装：[✓](https://github.com/FastLM/KVLearn) ・ リポジトリ内被引用：0  
  プリフィルとデコードを別ノード群へ分離するLLMサービングでは、KVキャッシュを残すか捨てるかの費用構造が単一GPUのLRUと異なる。

- **2026-09 · [The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems](2026-2609.27746-kv-cache-working-set-online-capacity-planning.md)**  
  実装：[✓](https://github.com/llc-kc/kv_cache_capacity_estimator) ・ リポジトリ内被引用：0  
  LRUのスタック距離をFenwick木で解析し、接頭辞KVキャッシュの目標ヒット率に必要な容量を1回の要求トレースからオンライン推定する。

- **2026-09 · [StepKV: Step-Aware KV Cache Compression for LLM Agents](2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H2OやTOVAのような既存圧縮は各トークンの注意量や直近性から重要度を決めるが、複数段階のLLMエージェントでは「情報を生成した単位」が推論段階であるため、トークン単位の局所重要度だけでは後から再利用される観測や中間判断を早期に捨てることがある。

- **2026-09 · [Shared KV Caching for Replicated 27B Inference: Correctness Failures and Performance Boundaries](2026-2609.15021-shared-kv-caching-replicated-27b-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュのページ表現・CUDAストリーム順序・全容量ピン留めを段階検証し、レプリカ移動時だけ大きな長文プリフィル再利用効果が得られる境界を実測する。

- **2026-09 · [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SGD-KVは、要点抽出へ寄与する注意ヘッドを事前診断し、ヘッド別KV容量へ変換して、長文の意味集約に必要な履歴を優先保持する。

- **2026-09 · [Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context Window Size](2026-2609.12686-residual-vector-long-context-recall.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文書を事実単位の外部残差ベクトルへ変換し、質問時にFFN活性で選択注入して元トークン/KVなしに事実を再構成することで、文書長にほぼ依存しないGPU記憶量で長文脈recallを実現する。

- **2026-09 · [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/Random-Attention) ・ リポジトリ内被引用：0  
  Random 注意機構は、入力文を必ず保持し、生成した推論過程のKVだけをヘッド別に無作為保持することで、選択器の採点計算を省き、同じ容量で強い選択法に近い正答率と高い提供スループットを得る。

- **2026-09 · [Prefix Sharing Is a Sorting Problem](2026-2609.13692-prefix-sharing-sorting-problem.md)**  
  実装：[✓](https://github.com/Darrenus/prefix-sharing-is-sorting) ・ リポジトリ内被引用：0  
  入力部品の並びと要求処理順を階層的に最適化し、既存の先頭キャッシュを変更せず実検索データで先頭共有を増やして事前計算量を17〜36%削減する。

- **2026-09 · [Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression](2026-2609.36322-periodic-weak-spots-phase-sensitivity-from-chunked-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  チャンク型KV圧縮が窓境界に対する位置位相を新たに作り、同じ情報の検索精度を最大40ポイント変動させる周期的弱点を生むことを実証する。

- **2026-09 · [OmniKVQuant: KV Cache Quantization for Omni-LLMs](2026-2609.11582-omnikvquant-kv-cache-quantization-for-omni-llms.md)**  
  実装：[✓](https://github.com/kaistmm/OmniKVQuant) ・ リポジトリ内被引用：0  
  全モダリティ大規模言語モデルのKVキャッシュに対し、32トークン局所範囲でキー量子化を適応し、モダリティ別回転でバリューを2ビット化して品質劣化を抑える学習不要方式。

- **2026-09 · [Multi-Turn LLM Conversations under the Least-Recently-Used Policy: Mean-Field Asymptotics and Hit Ratio Approximation](2026-2609.02027-multi-turn-lru-hit-ratio-mean-field.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多ターン会話の最終使用時刻型鍵値キャッシュを確率モデル化し、メモリ容量と会話到着率からヒット率を推定する平均場式を導出。Qwen3-8B実機評価で到着率0.5〜2.0毎秒の条件において絶対誤差0.015未満・相対誤差7%未満を確認する。

- **2026-09 · [MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference](2026-2609.07966-metakv-adaptive-kv-cache-compression-for-constrained-llm-inference.md)**  
  実装：[✓](https://github.com/MichaelWang0505/MetaKV.git) ・ リポジトリ内被引用：0  
  MetaKVは、プロンプトと遅延・KVメモリ制約から候補圧縮方式の結果を予測し、制約内で正答率を保つ設定をリクエストごとに切り替える。

- **2026-09 · [KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints](2026-2609.10266-kvsharearena-cross-context-checkpoint-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVShareArenaは、文脈・チェックポイントをまたぐKV再利用で位置ずれと情報源間相互作用の欠落を分離測定し、補正・再計算・圧縮の品質と費用を共通基準で比較する。

- **2026-09 · [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jacapは、将来クエリへの注意出力感度と値方向の重複を測り、重要度だけでなく情報の多様性を持つKV集合を選んで、高圧縮時の出力情報欠落を減らす。

- **2026-09 · [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeadWiseKVは、全体注意層のKV履歴を物理KVヘッドごとに較正し、必要な窓だけGPUへ確保して、長文脈の過剰メモリと一律圧縮による品質低下を抑える。

- **2026-09 · [H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache](2026-2609.24197-h-spec-parallel-speculative-decoding-without-a-drafter-side-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象モデルのKVを注意層で直接再利用し、最後の対象隠れ状態だけをMambaへ注入することで、専用ドラフターKVなしのブロック並列投機復号を実現する。

- **2026-09 · [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GrowPageは、生成中の注意参照範囲を短期・長期信号で予測し、容量境界で圧縮継続かKVページ追加かを選んで、推論ごとの過剰予約と必要履歴の削除を抑える。

- **2026-09 · [Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction](2026-2609.13285-grouped-value-attention-efficient-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  値だけをKVキャッシュへ保存し、内容キーを値から再構成してクエリ側へ吸収することで、GQAに近い精度を保ちながら永続キャッシュを約45〜47%削減する注意機構。

- **2026-09 · [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](2026-2609.09768-kv-concatenation-aware-recompute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV連結対応学習とCacheBlendの選択的再計算を組み合わせ、文書間相互作用の欠落を15%再計算で補い、RAG長文の品質とSSD読出し・転送待ちを両立する。

- **2026-09 · [Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches](2026-2609.17652-fathom-per-query-read-depth-offloaded-kv-cache.md)**  
  実装：[✓](https://github.com/vivekkalyanarangan30/fathom) ・ リポジトリ内被引用：0  
  問い合わせごとに鍵チャネルの読取深度を変え、ホスト退避した疎注意索引の転送量を減らして百万トークン復号を最大一・六七倍高速化する。

- **2026-09 · [Dynamic Flow, Static Graph: KV Cache Reuse for Efficient LLM Serving on Mobile NPUs](2026-2609.34727-dynamic-flow-static-graph-kv-cache-reuse-for-efficient-llm-serving-on-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的グラフ制約下のモバイルNPUで選択的KV再計算、階層KV管理、I/O重畳を協調させ、prefix・非prefix双方の再利用を実現する。

- **2026-09 · [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits](2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文書編集で古くなったKVは重要位置の散発再計算より編集直後を連続再計算する方が有効で、隣接依存なら13〜21倍高速にほぼ完全修復する。

- **2026-09 · [Compressing Long Context into Answer-Aligned Memory Embeddings for LLM Inference](2026-2609.25537-cmc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈推論では自己注意の計算量が文脈長に対して二次的に増え、KVキャッシュは線形に増える。CMCは長文を少数の文脈記憶埋め込みへ変換し、質問に関係する記憶と直近の原文だけをデコーダへ与える。

- **2026-09 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](2026-2609.04971-beaconkv.md)**  
  実装：[✓](https://github.com/aiha-lab/BeaconKV) ・ リポジトリ内被引用：0  
  長い推論で過去の計画へ再注意する問い合わせを少数のビーコンとして保持し、将来再参照されるKVを予測して残す訓練不要の圧縮方式。

- **2026-09 · [ARM: Attention with Routed-Memory for Learnable Sparse Control](2026-2609.24417-arm-attention-routed-memory-learnable-sparse-control.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  増え続けるKVキャッシュを固定数256スロットの階層メモリへ置き換え、書込み先と混合率、さらに読み出すメモリ量まで学習する。Llama-3.1-8Bで128Kまで動作し、RULER平均15.12を報告する。

- **2026-09 · [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md)**  
  実装：[✓](https://github.com/LiuTaowen-Tony/agentkv) ・ リポジトリ内被引用：0  
  思考・行動・ツール応答など段階別の問い合わせ履歴でKV重要度を評価し、エージェントの段階遷移で必要になる古い状態を残しつつ、物理ページ圧縮で最大1.80倍の出力スループットを得る。

- **2026-09 · [ActKV: Efficient LLM Agents through Action-Guided KV Cache Management](2026-2609.31395-actkv-efficient-llm-agents-through-action-guided-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行動生成に効くKVを注意履歴と確信度で選別し、ページ対応カーネルで圧縮するエージェント向けKV管理。FullKV比25.98%のKVメモリで平均98.53%精度を維持し、処理量を最大3.97倍にする。

- **2026-08 · [vToken: Token-Level Virtualization for Reclaimable KV Caches](2026-2608.13263-vtoken-token-level-virtualization-for-reclaimable-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vToken は論理トークンと物理配置を分離するトークン表を導入し、生存トークンを非同期に詰め直す。

- **2026-08 · [ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents](2608.19662.md)**  
  実装：[✓](https://github.com/EIT-NLP/ReCache) ・ リポジトリ内被引用：0  
  ツール／スキル定義を組合せ非依存のKVブロックとして再利用し、重要な層・KVヘッド群と呼出し必須フィールドだけを残して、エージェント推論のプリフィルとKVメモリを削減する。

- **2026-08 · [PuzzleKV: Page-Wise Low-Rank Decomposition for KV Cache Compression](2026-2608.23843-puzzlekv-page-wise-low-rank-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PagedAttentionの固定長ページごとにKVを独立低ランク分解し、密ページと因子化ページを復元なしで同時に注意計算することで、学習不要のままKV容量を約60%へ削減する。

- **2026-08 · [PAGE: Partition-Aware Gated KV-Cache Eviction](2026-2609.22157-page-partition-aware-gated-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル注意の層間ヘッド一致度低下から入力ごとのKV退避安全性を判定し、危険な入力だけ全キャッシュ保持へ戻す学習不要の安全ゲート。

- **2026-08 · [Output-Aware Rotation for INT2 KV-Cache Quantization](2026-2608.02691-output-aware-rotation-int2-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OptRは、長文脈推論でKVキャッシュを2ビット整数へ量子化したとき、キーや値そのものの再構成誤差が小さくても、注意重みと出力射影を通過した後のモデル内部表現には大きな誤差が残り得る問題を扱う。

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

- **2026-08 · [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](2026-2608.02515-livemem-maintaining-memory-state-continuity-in-long-running-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  有界KV窓とは別に固定容量の再帰状態を各層へ持たせ、退避済み履歴の影響を長時間エージェント推論へ継続させる内在メモリ方式。

- **2026-08 · [Entropy-Constrained Adaptive Stochastic Quantization](2026-2608.18147-entropy-constrained-adaptive-stochastic-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  listsummary と同じ一覧専用解説。ECASQは値ごとに適応する不偏確率量子化で、誤差と後段のエントロピー符号化後の平均ビット量を共同最適化する。実モデルのKVテンソルでも比較し、近似法は厳密法に近い誤差を保ちながら解法処理を高速化する。

- **2026-08 · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](2026-2608.08878-distillcache-kl-guided-adaptive-kv-cache-eviction-for-memory-efficient-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自己回帰型LLMは過去トークンの鍵・値をKVキャッシュへ保持することで再計算を避けるが、キャッシュ容量は文脈長に比例して増える。Mistral-7B-Instruct-v0.3では25%キャッシュ予算でLongBench 39.1、完全キャッシュ41.5に対して94.2%を維持する。

- **2026-08 · [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](2026-2608.07458-coinrag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoinRAGは、検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した長い文書チャンクを毎回前処理する費用と、チャンク単位のKVキャッシュ再利用に残る冗長情報を同時に減らす方式である。

- **2026-08 · [Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects](2026-2608.30076-budget-aware-compression-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み量子化・層削減・鍵値キャッシュ圧縮の相互作用を三予算で評価し、七百億モデルを約三十三ギガバイトへ縮小して単一A40・一万トークン入力で約五十七トークン毎秒を実現する。

- **2026-07 · [VarRate: Training-Free Variable-Rate KV Cache Compression for Long-Context LLMs](2026-2607.15498-varrate-training-free-variable-rate-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを削除せず、注意顕著度に応じて各トークンの低ランク表現へ可変容量を配る学習不要KV圧縮で、20%メモリ予算でもLongBench平均を非圧縮から0.8点以内に保ち、再利用時の不可逆削除崩壊を抑える。

- **2026-07 · [Lynx: Progressive Speculative Quantization for accelerating KV Transfer in Long-Context Inference](2026-2607.01831-lynx-progressive-kv-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LynxはKVを上位ビットのAnchorとResidualへ分割し、Anchor到着後に低精度で投機生成、Residual到着後に一括検証して、分離サービングの転送待ちを隠しつつINT8級品質を保つ。

- **2026-07 · [LOCKS: Page-Local Compact Key Summaries for Efficient Long-Context Decoding](2026-2607.24555-locks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LOCKSは、長文脈デコードで毎トークンごとに巨大なKVキャッシュ全体を読み直す帯域問題に対し、各ページ固有の低ランク要約だけを常駐させ、問い合わせごとに読むページを選ぶ方式である。ランク8では要約は元KVページのおよそ10%で、選択時には候補ページの完全なキーも値も読まない。

- **2026-07 · [KAP: Bridging the Knowledge Selection-Runtime Consumption Gap in LLM Systems](2026-2607.24260-kap-knowledge-access-planning-kv-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索・グラフなど上流の知識選択情報を実行時アクセス計画へコンパイルし、論理プロンプトを変えず物理KV参照を選択化する。GraphSpecは128Kで提案時KVアクセスを元状態の5.5%まで減らす。

- **2026-07 · [InferScale: GPU-Native KV Injection for Personalized LLM Serving](2026-2607.27090-inferscale-gpu-native-kv-injection.md)**  
  実装：[✓](https://github.com/saltsystemslab/InferScale) ・ リポジトリ内被引用：0  
  検索メモリのRoPE適用前KVをGPU上で再利用・位置再配置してvLLMへ直接注入し、k=50でTTFTを72〜79%削減する。

- **2026-07 · [GroupKV: Hierarchical KV Cache Management for Long-Context Diffusion LLM Inference](2026-2609.17573-groupkv-hierarchical-kv-cache-diffusion-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの長文KVを連続グループ単位で疎選択し、層間予測先読みと古さ補正を組み合わせてCPU退避時の転送量と待ち時間を削減する。

- **2026-06 · [Vortex: Efficient and Programmable Sparse Attention Serving for AI Agents](2026-2606.06453-vortex-programmable-sparse-attention-serving.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/vortex_torch) ・ リポジトリ内被引用：0  
  ページ化KVを抽象化するvFlow/vTensorと最適化バックエンドで、動的疎注意を数行のPython表現からSGLang実運用へ落とし込み、全注意比最大3.60倍のスループットを実現する。

- **2026-06 · [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md)**  
  実装：[✓](https://github.com/aiha-lab/TANGRAM) ・ リポジトリ内被引用：0  
  Tangramは、ヘッド別KV保持量を少数サンプルで事前較正し、固定予算のraggedページ化と負荷分散へ変換して、非一様圧縮の断片化・回収費・デコード不均衡を減らす。

- **2026-06 · [PTStore (Prefix Tensor Store): Distributed Prefix Caching and Replication for High Throughput Inference Serving](2026-2607.22648-ptstore-prefix-tensor-store-distributed-prefix-caching-and-replication-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ長文やシステムプロンプトを含む問い合わせを複数GPU・計算ノードで処理すると、共通prefixに対して入力処理で計算した注意機構のkey/value（KV）を要求ごとに再生成する。著者は長文文書 QAで、メモリを複数ノード/GPUに集約しない比較方式より5–6倍効率的と要旨で総括する。

- **2026-05 · [ArborKV: Structure-Aware KV Cache Management for Scaling Tree-based LLM Reasoning](2026-2605.22106-arborkv-structure-aware-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活動経路の保護、トークン単位の選択的追い出し、後戻り時の遅延再構築を組み合わせ、単一RTX 4090上のToT評価で同一キャッシュ予算の系列方式を上回り、256展開の探索を5.6 GiBで完了した。

- **2026-04 · [PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference](2026-2604.24971-polykv-shared-asymmetrically-compressed-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共通文書のKVキャッシュを一度だけ非対称量子化して共有プール化し、複数エージェントへ注入して重複メモリを削減する。

- **2026-04 · [DASH-KV: Accelerating Long-Context LLM Inference via Asymmetric KV Cache Hashing](2026-2604.19351-dash-kv-asymmetric-hashing-long-context.md)**  
  実装：[✓](https://github.com/Zhihan-Zh/DASH-KV) ・ リポジトリ内被引用：0  
  注意の全キー内積を学習済み非対称ハッシュ検索へ置換し、重要トークンだけ完全精度へ戻すことで、長文脈の計算量を線形化しつつLongBench品質をFull 注意機構近傍に維持する。

- **2026-03 · [Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding](2026-2603.23914-attention-aware-inference-optimizations-large-vlm-memory-efficient-decoding.md)**  
  実装：[✓](https://github.com/git-disl/AttentionPack) ・ リポジトリ内被引用：0  
  複数ヘッドをまとめた低ランク分解で視覚言語モデルのKVを圧縮し、注意度に応じて復元精度を変えることで、動画QAのキャッシュを8.11分の1にしつつバッチ推論を60%高速化する。

- **2026-01 · [HeteroCache: A Dynamic Retrieval Approach to Heterogeneous KV Cache Compression for Long-Context LLM Inference](2026-2601.13684-heterocache-dynamic-heterogeneous-kv-retrieval.md)**  
  実装：[✓](https://github.com/ponytaill/HeteroCache) ・ リポジトリ内被引用：0  
  注意ヘッドの安定性と層内冗長性に応じてKV予算を細粒度配分し、代表ヘッドの注意ドリフト検知時だけCPUから非同期取得することで、224K文脈の復号を完全注意計算比約3倍高速化する。

### 2年前（2024-11〜2025-10）

- **2025-03 · [vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention](2024-2405.04437-vattention-virtual-memory-kv-management.md)**  
  実装：[✓](https://github.com/microsoft/vattention) ・ リポジトリ内被引用：51  
  KVキャッシュの仮想アドレスを連続に保ったままCUDA仮想メモリで物理ページだけを需要時割当し、PagedAttention固有のブロック表と専用注意カーネルを不要にする方式。長文脈サービングで最大1.23倍のスループット改善を報告する。

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：23  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2024-12 · [A Survey on Large Language Model Acceleration based on KV Cache Management](2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-manageme.md)**  
  実装：[✓](https://github.com/TreeAI-Lab/Awesome-KV-Cache-Management) ・ リポジトリ内被引用：19  
  キャッシュを減らせば容量は空くが、注意品質の低下、検索・量子化の追加計算、CPU/SSD転送、再計算など別の費用が発生する。

- **2025-10 · [Expected Attention: KV Cache Compression by Estimating Attention from Future Queries Distribution](2025-2510.00636-expected-attention-kv-cache-compression-by-estimating-attention-from-fut.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  未来クエリの分布から各KV対が受ける期待注意量を閉形式で推定し、FlashAttentionのように注意行列を保持しない実装でも学習なしでKVを順位付け・削除する。プリフィルとデコードの双方へ適用し、LongBench、RULER、Needle-in-a-Haystack、AIME25、MATH-500でTOVA、SnapKV、KeyDiff等を上回る。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：16  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：15  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2024-11 · [DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving](2024-2411.02820-droidspeak-kv-cache-sharing-for-cross-llm-communication-and-multi-llm-se.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  複数の専門LLMを組み合わせるワークフローでは、同じ長い文書や会話履歴を別々のモデルが読むことが多い。各モデルが独立にプリフィルを行うと、内容が同一でもTransformer各層でキー・バリュー（KV）を再生成するため、計算と最初のトークンまでの時間（TTFT）が重複する。ただし全層のKVをそのまま共有すると、微調整によって表現が変わった層で誤差が累積する。

- **2025-05 · [KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction](2025-2505.23416-kvzip.md)**  
  実装：[✓](https://github.com/snu-mllab/KVzip) ・ リポジトリ内被引用：14  
  元文脈の再構成時に使われるKVを重要とみなし、将来クエリを知らずに再利用可能な長文脈KVキャッシュを3〜4倍圧縮する。

- **2025-04 · [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](2025-2504.19874-turboquant-online-vector-quantization-with-near-optimal-distortion-rate.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  ランダム回転と1-bit残差補正でKVキャッシュをオンライン量子化し、Llama-3.1-8B-InstructのLongBench平均を3.5 bit/channelでもFull Cacheと同じ50.06に保つ。

- **2025-10 · [Cache-to-Cache: Direct Semantic Communication Between Large Language Models](2025-2510.03215-cache-to-cache-direct-semantic-communication-between-large-language-mode.md)**  
  実装：[✓](https://github.com/thu-nics/C2C) ・ リポジトリ内被引用：10  
  異種LLM間で中間テキストを生成せずKVキャッシュを投影・融合し、層選択ゲートで有用な意味表現だけを受信モデルへ注入する直接通信方式。

- **2025-01 · [RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations](2025-2501.16383-rotatekv-accurate-and-robust-2-bit-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/ZunhaiSu/RotateKV) ・ リポジトリ内被引用：10  
  RotateKVは、キー・バリュー（Key-Value; KV）キャッシュを2ビットへ落とす前に、外れ値が特定チャネルへ集中しないよう適応回転する。

- **2024-12 · [ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression](2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-com.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/ClusterKV) ・ リポジトリ内被引用：10  
  文脈が32K、128Kと伸びるとKV容量はほぼ線形に増え、復号時には過去KVを大量に読み込むためメモリ帯域も律速になる。既存圧縮には、不要と判断したトークンを永久削除する方式と、GPU外へ退避したKVを固定ページ単位で呼び戻す方式がある。

- **2024-12 · [DiffKV: Differentiated Memory Management for Large Language Models with Parallel KV Compaction](2024-2412.03131-diffkv-differentiated-memory-management-for-large-language-models-with-parallel-kv-compaction.md)**  
  実装：[✓](https://github.com/zyqCSL/DiffKV) ・ リポジトリ内被引用：9  
  鍵・値・トークン・注意ヘッドを異なる粒度で圧縮し、不規則な空き容量をGPU内で並列コンパクションするDiffKV。KVを2.7〜5.7倍圧縮しスループットを1.9〜5.4倍改善する。

- **2025-03 · [Jenga: Effective Memory Management for Serving LLM with Heterogeneity](2025-2503.18292-jenga-heterogeneous-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  異なる大きさ・依存関係のKV/視覚/Mamba状態を、LCM大ページと層別キャッシュAPIで統合管理し、vLLM比でスループット最大4.92倍、GPUメモリ利用を最大79.6%改善する。

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  Preserveは、テンソル並列のGPU間集約通信中に次の重みとKVをHBMからL2へ先読みし、通信待ちとメモリ読出しを重ねて分散推論の遅延を減らす。

- **2025-03 · [xKV: Cross-Layer KV-Cache Compression via Aligned Singular Vector Extraction](2025-2503.18893-xkv-cross-layer-kv-cache-compression-via-aligned-singular-value-decomposition.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/xKV) ・ リポジトリ内被引用：6  
  xKVは、隣接層のキー・バリュー（Key-Value; KV）キャッシュをトークンごとに直接似ているとみなすのではなく、複数層が共有する支配的な特異ベクトルをまとめて抽出する。プリフィル時に複数層を横連結して共有低ランク基底へ因子分解し、デコード時はクエリに重要なトークンだけを選択的に再構成する。

- **2025-02 · [QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache](2025-2502.10424-quantspec-self-speculative-decoding-with-hierarchical-quantized-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  文脈が伸びると注意計算の算術強度が下がり、GPU演算能力よりメモリ帯域とKV容量が律速になる。通常の投機的復号は小型ドラフトモデルで複数トークンを先読みするが、対象モデルとの分布差が大きいと受理率が落ち、長文脈ではドラフト側KVも追加メモリになる。

- **2024-12 · [KunServe: Elastic and Efficient Large Language Model Serving with Parameter-centric Memory Management](2024-2412.18169-kunserve-elastic-and-efficient-large-language-model-serving-with-paramet.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  負荷急増時にリクエスト固有KVではなく複製パラメータを選択的に解放し、注意演算を他GPUへ遠隔実行してKV空間を確保するパラメータ中心のLLMサービング方式。

- **2025-08 · [KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache](2025-2509.00579-kvcomp-a-high-performance-llm-aware-lossy-compression-framework-for-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  誤差制御量子化＋Huffman符号化と、復号・行列ベクトル積のGPU融合でKVを高圧縮する。既存方式比で平均47%・最大83%高いメモリ削減率を示し、長文脈では復号込みカーネルがcuBLASを上回る。

- **2025-06 · [KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider](2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at.md)**  
  実装：[✓](https://github.com/vllm-project/vllm/pull/22236) ・ リポジトリ内被引用：4  
  合成トレースではなく本番サービスのトレースに基づく設計材料が不足しているという問題に対し、本研究はAliyun Tongyiの大規模serving クラスタから得た顧客向け(to-C)と企業向け(to-B)のトレースを特徴付け、観測した分布を使う追い出し 方策を提案する。

- **2025-06 · [CommVQ: Commutative Vector Quantization for KV Cache Compression](2025-2506.18879-commvq-commutative-vector-quantization-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UMass-Embodied-AGI/CommVQ) ・ リポジトリ内被引用：4  
  CommVQは、KVキャッシュを複数の符号帳ベクトルの和で表す加算型ベクトル量子化（additive vector 量子化）を使い、特にキー側の符号帳を回転位置埋め込み（Rotary Position Embedding; RoPE）と交換可能になるよう学習する。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：4  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-05 · [ReCalKV: Low-Rank KV Cache Compression via Head Reordering and Offline Calibration](2025-2505.24357-recalkv-low-rank-kv-cache-compression-via-head-reordering.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/ReCalKV) ・ リポジトリ内被引用：4  
  KeyとValueは注意機構で同じ役割ではない。ReCalKVは、Keyには「似たヘッドをまとめて低ランク化」、Valueには「データで低ランク因子を補正して復元行列を次の射影へ融合」という別々の圧縮を割り当て、高圧縮時の品質と実行時オーバーヘッドを両方抑える。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

- **2025-02 · [CriticalKV: Optimizing KV Cache Eviction from an Output Perturbation Perspective](2025-2502.03805-criticalkv-optimizing-kv-cache-eviction-from-an-output-perturbation-perspective.md)**  
  実装：[✓](https://github.com/FFY0/DefensiveKV) ・ リポジトリ内被引用：4  
  KVキャッシュ追い出しを「注意出力摂動の最小化」として定式化し、注意重み×出力射影後の値状態ノルムで重要KVを選ぶ二段階方式により、既存3方式の圧縮損失を29データセット平均で半分超削減する。

- **2025-07 · [Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation](2025-2507.10524-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-tok.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  共有Transformerブロックを再帰利用し、ルータがトークンごとに継続深度を決めて活動集合だけへ注意・KV保持することで、推論時の適応計算とパラメータ共有を両立する。

- **2025-05 · [PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs](2025-2505.18610-pm-kvq-progressive-mixed-precision-kv-cache-quantization-for-long-cot-llms.md)**  
  実装：[✓](https://github.com/thu-nics/PM-KVQ) ・ リポジトリ内被引用：3  
  KVを16→8→4→2bitと必要時だけ段階圧縮し、層感度とRoPE位置補間校正で長CoTの累積量子化誤差を抑えるPM-KVQ。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：3  
  非同期KV先読みは、現在の注意ブロック計算中に次のKVをHBMからL2へ運び、Hopper GPUのメモリ待ちを隠して、注意カーネルとE2Eデコードを速める。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：2  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-10 · [VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization](2025-2510.06175-vecinfer-efficient-llm-inference-with-low-bit-kv-cache-via-outlier-suppr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  平滑化とHadamard回転でkey外れ値を抑えてベクトル量子化のコードブック利用を改善し、融合CUDAカーネルで低ビットKVを直接注意計算へ供給する。

- **2025-07 · [Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing](2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話ごとの注意類似度から層間の鍵・値共有を動的選択し、注意類似度計算を中央処理装置と画像処理装置へ分担、圧縮後の再計算とロードを層間パイプラインで重畳してマルチターン状態復元を高速・省容量化する。

- **2025-07 · [HCAttention: Extreme KV Cache Compression via Heterogeneous Attention Computing for LLMs](2025-2507.19823-hcattention-heterogeneous-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キー量子化・値のCPU退避・層別の動的KV削除を統合し、GPU KV予算25%でLlama-3-8BのLongBench平均43.2を全注意と同値に保ち、12.5%でも42.5（0.7ポイント差）に抑える異種GPU/CPU注意方式。

- **2025-05 · [EFIM: Efficient Serving of LLMs for Infilling Tasks with Improved KV Cache Reuse](2025-2505.21889-efim-infilling-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/gty111/EFIM) ・ リポジトリ内被引用：1  
  FIMの増分を末尾へ移して接頭部・接尾部KVを要求間再利用し、断片トークン化学習で語途中生成能力を補って平均遅延52%削減・スループット98%向上。

### 3年前（2023-11〜2024-10）

- **2024-05 · [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](2024-2405.04434-deepseek-v2-mla.md)**  
  実装：✓ ・ リポジトリ内被引用：162  
  通常の多頭注意（Multi-Head 注意機構; MHA）では、系列長が伸びるほどKVキャッシュが線形に増え、GPU高帯域メモリ（High Bandwidth メモリ; HBM）に置ける同時要求数や最大文脈長を圧迫する。

- **2024-06 · [SnapKV: LLM Knows What You are Looking for Before Generation](2024-2404.14469-snapkv.md)**  
  実装：[✓](https://github.com/FasterDecoding/SnapKV) ・ リポジトリ内被引用：137  
  プロンプト末尾の観測窓から各注意ヘッドが将来参照する位置を推定し、重要KVだけをクラスタ単位で残して長文復号を軽量化する手法。

- **2024-02 · [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](2024-2402.02750-kivi.md)**  
  実装：[✓](https://github.com/jy-yuan/KIVI) ・ リポジトリ内被引用：130  
  キーはチャネル単位、値はトークン単位で2ビット量子化し、直近KVだけ高精度保持することで追加学習なしにKVメモリと帯域を削減し最大3.47倍のスループットを得る。

- **2024-01 · [KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization](2024-2401.18079-kvquant.md)**  
  実装：[✓](https://github.com/SqueezeAILab/KVQuant) ・ リポジトリ内被引用：129  
  Key分布に合わせたチャネル別・RoPE前・非一様・外れ値分離量子化で、3ビットKVを約4.8倍圧縮しつつパープレキシティ悪化0.1未満を実現する。

- **2024-06 · [PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling](2024-2406.02069-pyramidkv.md)**  
  実装：[✓](https://github.com/Zefan-Cai/PyramidKV) ・ リポジトリ内被引用：85  
  注意の層間集約パターンに合わせてKV予算を下層から上層へ逓減させ、同じ総メモリで固定予算型より長文脈性能を保つKVキャッシュ圧縮法。

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：68  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2024-07 · [Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference](2024-2407.11550-ada-kv.md)**  
  実装：[✓](https://github.com/FFY0/AdaKV) ・ リポジトリ内被引用：45  
  注意ヘッドごとの集中度に応じて同一層内のKV保持予算を再配分し、既存Top-k圧縮の総容量を変えずに追い出し損失を下げる手法。

- **2024-03 · [GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM](2024-2403.05527-gear-an-efficient-kv-cache-compression-recipe-for-near-lossless-generati.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  KV行列を一様量子化すると外れ値と構造化誤差が自己回帰生成で蓄積する問題に対し、通常成分の低ビット量子化、量子化誤差の低ランク近似、外れ値誤差の疎行列補正を組み合わせる。4ビットKVで近損失品質を保ち、最大2.38倍のスループット、最大2.29倍のピークメモリ削減を報告する。

- **2024-10 · [DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads](2024-2410.10819-duoattention-efficient-long-context-llm-inference-with-retrieval-and-str.md)**  
  実装：[✓](https://github.com/mit-han-lab/duo-attention) ・ リポジトリ内被引用：34  
  長文脈LLMでは全注意機構 ヘッドが全トークン分のKV キャッシュを保持するのが標準だが、実際に遠い過去から情報を取り出すヘッドは一部しかない。MHA モデルではメモリを最大2.55倍削減し、デコードを最大2.18倍、プリフィルを最大1.73倍高速化する。

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/hydragen) ・ リポジトリ内被引用：29  
  Hydragenは、共有接頭辞への複数系列のクエリをまとめて計算し、同じKVのHBM読出しを一度に処理して、共有プロンプトの注意帯域と実行効率を改善する。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：28  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  ALISAは、重要トークンを残す疎注意とKVのGPU・CPU・再計算配置、INT8量子化を系列長に応じて切替え、容量・PCIe転送・再計算費を抑える。

- **2024-03 · [Jamba: A Hybrid Transformer-Mamba Language Model](2024-2403.19887-jamba-a-hybrid-transformer-mamba-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  Jambaは、Transformerの自己注意が持つ高い文脈参照能力と、Mambaの状態空間モデル（state-space モデル; SSM）が持つ固定サイズ状態・線形時間処理を同一デコーダへ組み合わせる。さらに混合専門家モデル（mixture-of-エキスパート; MoE）をMLPへ入れ、毎トークンで使う計算量を増やさず総モデル容量を増やす。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：20  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-05 · [KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization](2024-2405.03917-coupled-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  鍵値活性のチャネル間依存を利用して複数チャネルを共同量子化し、極低ビットでも品質劣化を抑える連結量子化を提案する。

- **2024-03 · [Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference](2024-2403.09636-dynamic-memory-compression-retrofitting-llms-for-accelerated-inference.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM/tree/DMC) ・ リポジトリ内被引用：18  
  動的メモリ圧縮（動的 メモリ Compression; DMC）は、過去トークンを「残す／捨てる」の二択にせず、各注意ヘッドが新しいキー・値（Key-Value; KV）を新規スロットへ追加するか、直前のスロットへ重み付きで結合するかを学習する。これにより、内容・層・ヘッドごとに必要な時間解像度を変えながらKVキャッシュをオンライン圧縮する。

- **2024-02 · [Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference](2024-2402.09398-get-more-with-less-synthesizing-recurrence-with-kv-cache-compression-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/hdong920/LESS) ・ リポジトリ内被引用：17  
  LESSは、キー・値キャッシュ（Key-Value Cache; KVキャッシュ）の追い出しを「残すか捨てるか」の二択にしない。重要なトークンは従来どおり疎KVキャッシュへ明示的に残し、追い出すトークンは固定サイズの低ランク状態へ順次圧縮する。次の注意計算では両方を合成するため、疎キャッシュから消えたトークンにも低解像度ながら参照経路が残る。

- **2024-05 · [ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification](2024-2405.14256-zipcache.md)**  
  実装：[✓](https://github.com/ThisisBillhe/ZipCache) ・ リポジトリ内被引用：16  
  因果マスクで偏る累積注意スコアを正規化し、少数プローブで重要トークンを推定してKVキャッシュを混合精度量子化し、約5倍圧縮と高速化を両立する。

- **2024-03 · [QAQ: Quality Adaptive Quantization for LLM KV Cache](2024-2403.04643-qaq-quality-adaptive-quantization-for-llm-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  KとVで異なる量子化誤差伝播を理論化し、注意重要度・外れ値・直近窓からトークン別ビット幅を割り当てるKV量子化。LLaMA2-7B/13Bで1%未満の精度低下時に約6〜9倍圧縮。

- **2024-02 · [ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition](2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-t.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  複数利用者へ同じ大規模言語モデル（LLM）を提供すると、システム プロンプトや少数例例のような長い接頭辞が要求間で重複することが多い。A100 80GB、CUDA 11.8の評価では、共有システム プロンプトが1024〜4096トークンの場合、PagedAttention系カーネルに対して注意機構 カーネル スループットを3.2〜4.8倍へ高める。

- **2024-10 · [Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning](2024-2410.19258-not-all-heads-matter-a-head-level-kv-cache-compression-method-with-integ.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  KVキャッシュ圧縮の多くは、各層でどのトークンを残すか、あるいは層ごとにどれだけ予算を与えるかを決める。代表結果では元KVの約1.5%だけを保持しながら文脈QAで完全KVの97%の性能を維持する。

- **2024-07 · [RazorAttention: Efficient KV Cache Compression Through Retrieval Heads](2024-2407.15891-razorattention-efficient-kv-cache-compression-through-retrieval-heads.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  検索ヘッドは全KVを保持し非検索ヘッドだけ遠方KVを削るヘッド別圧縮と補償トークンにより、長文脈LLMのKVキャッシュを70%以上削減する。

- **2024-07 · [Keep the Cost Down: A Review on Methods to Optimize LLM's KV Cache Consumption](2024-2407.18003-keep-the-cost-down-a-review-on-methods-to-optimize-llm-s-kv-cache-consum.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  本論文はKVキャッシュ最適化を、事前学習時のアーキテクチャ変更、配備時のメモリ管理・再利用、学習後の削除・統合・量子化という時間軸で整理する。

- **2024-02 · [GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding](2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  投機的復号は小さい下書きモデルが複数トークンを先に提案し、大きい対象モデルがまとめて検証する。実時間評価ではGliDe最大2.17倍、CaPE併用最大2.61倍の高速化を報告する。

- **2024-10 · [LayerKV: Optimizing Large Language Model Serving with Layer-wise KV Cache Management](2024-2410.00428-layerkv-optimizing-large-language-model-serving-with-layer-wise-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  さらにサービス水準目標（Service Level Objective; SLO）認識スケジューラが、既存デコード要求の出力トークン時間（Time Per Output Token; TPOT）を破らない範囲だけ新規プリフィルを投入する。

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

- **2024-07 · [ThinK: Thinner Key Cache by Query-Driven Pruning](2024-2407.21018-think-thinner-key-cache-by-query-driven-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  Query–Key相互作用から重要なKeyチャネルだけを残し、トークン削減や量子化と直交するチャネル方向のKVキャッシュ圧縮を追加する。

- **2024-05 · [MiniCache: KV Cache Compression in Depth Dimension for Large Language Models](2024-2405.14366-minicache-kv-cache-compression-in-depth-dimension-for-large-language-mod.md)**  
  実装：[✓](https://github.com/AkideLiu/MiniCache) ・ リポジトリ内被引用：11  
  MiniCacheは層内のトークン選別や低ビット化だけでなく、隣り合う層のあいだにも冗長性があると観察し、中層以降で同じ位置のKV状態を共有表現へ統合する。

- **2024-05 · [SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models](2024-2405.06219-skvq-sliding-window-key-and-value-cache-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/cat538/SKVQ) ・ リポジトリ内被引用：10  
  KVチャネルを量子化しやすい順へ並べ替え、外れ値をクリップし、直近KVだけ高精度で残すことで鍵2ビット・値1.5ビット級まで圧縮し、長文脈の容量・帯域律速を緩和する。

- **2024-10 · [LoRC: Low-Rank Compression for LLMs KV Cache with a Progressive Compression Strategy](2024-2410.03111-lorc-low-rank-compression-for-llms-kv-cache-with-a-progressive-compression-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  KVキャッシュから「どのトークンを捨てるか」を決めるのではなく、キー・値を作る射影行列そのものを低ランク化する。さらに、浅い層の近似誤差ほど後段で増幅されやすいことを利用し、浅層は保守的、深層は積極的に圧縮する。

- **2024-06 · [A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression](2024-2406.11430-l2-kv-compression.md)**  
  実装：[✓](https://github.com/alessiodevoto/l2compress) ・ リポジトリ内被引用：9  
  キーのL2ノルムと注意重みの逆相関を利用し、注意重みを計算せず重要KVを残す学習不要の圧縮法。FlashAttention互換のまま、長文検索では50〜90%のKV削減でも高精度を維持する。

- **2024-06 · [Attention Score is not All You Need for Token Importance Indicator in KV Cache Reduction: Value Also Matters](2024-2406.12335-attention-score-is-not-all-you-need-for-token-importance-indicator-in-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  注意スコアに値ベクトルのL1ノルムを組み込み、実際の注意出力寄与に近い重要度でKVトークンを削減する後付け型キャッシュ枝刈り。

- **2024-10 · [KVSharer: Efficient Inference via Layer-Wise Dissimilar KV Cache Sharing](2024-2410.18517-kvsharer-efficient-inference-via-layer-wise-dissimilar-kv-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  層間KVの非類似度を校正データで探索し、後段層のKVを前段層から共有して深さ方向のKV計算・保存を削減する追加学習不要の圧縮法。

- **2024-08 · [NACL: A General and Effective KV Cache Eviction Framework for LLM at Inference Time](2024-2408.03675-nacl-a-general-and-effective-kv-cache-eviction-framework-for-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/Research/tree/master/NLP/ACL2024-NACL) ・ リポジトリ内被引用：7  
  KV追い出しで「これまで注意スコアが大きかったトークンを残す」だけでは、注意が先頭・直近位置へ偏るため、長文中央の重要情報を捨てやすい。NACLは、質問などタスク固有の代理トークン（proxy トークン）が入力全体へ向けた注意から重要度を作る決定論的な保持と、その重要度分布からヘッド・層ごとに異なるトークンを確率的に残す保持を混ぜる。

- **2024-02 · [On the Efficacy of Eviction Policy for Key-Value Constrained Generative Language Model Inference](2024-2402.06262-on-the-efficacy-of-eviction-policy-for-key-value-constrained-generative-language-model-inference.md)**  
  実装：[✓](https://github.com/DRSY/EasyKV) ・ リポジトリ内被引用：7  
  RoCoはKV トークンの重要度を累積注意機構ではなく平均注意機構で測り、注意機構標準偏差で追い出し候補を動的に選び、固定window依存を減らしながらfull-キャッシュに近い生成品質を保つ。

- **2024-09 · [Inf-MLLM: Efficient Streaming Inference of Multimodal Large Language Models on a Single GPU](2024-2409.09086-inf-mllm-efficient-streaming-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  注意機構 saddlesを追跡して最新・重要トークンだけを固定KVへ残し、注意機構 biasで長期ストリーム中の注意移動にも追随するInf-MLLM。

- **2024-08 · [Eigen Attention: Attention in Low-Rank Space for KV Cache Compression](2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UtkarshSaxena1/EigenAttn) ・ リポジトリ内被引用：6  
  各層のキー・値をSVD由来の低ランク部分空間へ射影してKVキャッシュの特徴次元を縮め、トークン枝刈りや量子化と直交する形で長文脈推論のメモリと注意遅延を削減する。

- **2024-06 · [Effectively Compress KV Heads for LLM](2024-2406.07056-effectively-compress-kv-heads-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  実KV活性の低ランク構造をSVDで利用してMHAのKV headを圧縮し、RoPE互換変換とLoRA回復でGQA相当の省メモリ・高速デコードを実現する。

- **2024-03 · [Keyformer: KV Cache Reduction through Key Tokens Selection for Efficient Generative Inference](2024-2403.09054-keyformer-kv-cache-reduction-through-key-tokens-selection-for-efficient-.md)**  
  実装：[✓](https://github.com/d-matrix-ai/keyformer-llm) ・ リポジトリ内被引用：6  
  Keyformerは注意機構重みのおよそ90%が一部トークンへ集中するという観察を使い、重要トークンだけを残す。

- **2024-04 · [SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget](2024-2404.04793-squeezeattention-2d-management-of-kv-cache-in-llm-inference-via-layer-wi.md)**  
  実装：[✓](https://github.com/hetailang/SqueezeAttention) ・ リポジトリ内被引用：4  
  KVキャッシュ圧縮の多くは、各層の中で重要トークンを選び、古い・低注意機構 トークンを捨てる「系列方向」の最適化を行う。論文は約30〜70%のKV メモリ削減と最大2.2倍スループット改善を報告する。

- **2024-10 · [InfiniPot: Infinite Context Processing on Memory-Constrained LLMs](2024-2410.01518-infinipot-infinite-context-processing-on-memory-constrained-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多くのKV圧縮法は長い入力全体を一度処理してから不要KVを捨てる。この方式では最終キャッシュは小さくても、プリフィル途中には全入力分のKVを保持する必要があり、厳しい端末メモリ制約では入力自体を処理できない。

- **2024-09 · [Small Language Models: Survey, Measurements, and Insights](2024-2409.15790-small-language-models-survey-measurements-and-insights.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  100M〜5B級小型言語モデルを端末上で統一測定し、プリフィルは構造依存、デコードは規模依存が強く、長文脈ではKVと計算バッファがメモリ支配になると示す。

### 4年前（2022-11〜2023-10）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：245  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。

- **2023-06 · [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](2023-2306.14048-h2o.md)**  
  実装：[✓](https://github.com/FMInference/H2O) ・ リポジトリ内被引用：224  
  累積注意のヘビーヒッターと最新トークンを動的保持し、20%程度のKV予算で品質を維持しながらメモリ・スループットを改善する。

- **2023-10 · [Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs](2023-2310.01801-fastgen.md)**  
  実装：[✓](https://github.com/machilusZ/FastGen) ・ リポジトリ内被引用：99  
  FastGenは注意ヘッドごとの構造を一度だけ診断してKVキャッシュ保持方針を変え、追加学習なしでメモリ削減と長系列生成の高速化を両立する。

- **2023-05 · [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](2023-2305.17118-scissorhands.md)**  
  実装：✓ ・ リポジトリ内被引用：64  
  代表結果として、OPT系列の言語モデル評価と少数例学習評価で品質を大きく損なわずKVキャッシュを最大5倍圧縮した。

### 7年前（2019-11〜2020-10）

- **2019-11 · [Fast Transformer Decoding: One Write-Head is All You Need](2019-1911.02150-multi-query-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：115  
  複数クエリ注意（Multi-Query 注意機構; MQA）は、通常の複数ヘッド注意（Multi-Head 注意機構; MHA）が各ヘッドごとに持つキー（Key; K）とバリュー（Value; V）を1組だけに共有し、クエリ（Query; Q）は複数ヘッドのまま残す。
<!-- survey:auto:end -->
