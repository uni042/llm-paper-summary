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
## 自動生成の論文一覧（103本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：5  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2026-05 · [LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents](2026-2602.01053-lragent-multilora-agent-kv-sharing.md)**  
  実装：[✓](https://github.com/jeonhye/lragent) ・ リポジトリ内被引用：4  
  multi-LoRAエージェントのKVを共有基盤成分と低ランク役割成分へ分解し、後者を全次元化せず注意計算することで、長い共有履歴のKVメモリと再プリフィルを削減する。

- **2026-07 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2026-ojakv.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：3  
  重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。

- **2026-07 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2026-2607.17715-c2kv-compressed-composable-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/s7a9/C2KV) ・ リポジトリ内被引用：3  
  文書ごとに位置非依存で直接連結できる圧縮KVを学習抽出し、非prefix再利用のプリフィル削減とKV保存・転送・デコード帯域削減を同時に狙う。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：3  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

- **2025-11 · [TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection](2025-token-select.md)**  
  実装：[✓](https://github.com/pzs19/TokenSelect) ・ リポジトリ内被引用：3  
  各問い合わせで重要な鍵値をトークン単位に選び、ヘッド軟投票・選択キャッシュ・ページ化内積カーネルで長文脈注意を高精度かつ高速化する。

- **2026-07 · [LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning](2026-lazyeviction.md)**  
  実装：[✓](https://github.com/Halo-949/LazyEviction) ・ リポジトリ内被引用：2  
  一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。

- **2026-06 · [STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control](2026-2606.08382-star-kv-adaptive-low-rank-cache-compression.md)**  
  実装：[✓](https://github.com/PriyanshBhatnagar/STAR-KV) ・ リポジトリ内被引用：2  
  特異値の学習可能なしきい値で層・ヘッドごとのKV低ランク次元を自動配分し、鍵/値で異なる分解と低ランク対応混合精度量子化を組み合わせ、強い圧縮を実GPU高速化へつなげる。

- **2026-04 · [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md)**  
  実装：[✓](https://github.com/yuzhenmao/IceCache) ・ リポジトリ内被引用：2  
  IceCacheは、意味的に近いKVを同じ物理ページへクラスタ化し、関連ページだけをCPUから一括転送して、長文のGPU KV容量とPCIeデータ量を減らす。

- **2025-12 · [MEPIC: Memory Efficient Position Independent Caching for LLM Serving](2025-2512.16822-mepic-position-independent-chunk-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  位置非依存KVをページ境界へ正規配置し、最初の1ブロックだけ再計算、RoPEを注意時に融合することで、同一チャンクのHBMページを要求間共有し、既存PICよりHBM重複と再計算を大幅に減らす。

- **2026-09 · [Language Models Can Control Their Own Attention](2026-2609.02737-declarative-attention-self-directed-kv-access.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル自身が思考中に注意範囲を宣言し、推論エンジンがKVブロック表を切り替えて不要な長文脈読出しを省く疎注意方式。Gemma-4-31Bで参照トークンを52.0%削減し、精度低下は1.27ポイントだった。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：1  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-07 · [REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression](2026-real-kv.md)**  
  実装：[✓](https://github.com/yonseicasl/REAL) ・ リポジトリ内被引用：1  
  成功例だけでなく偏り・注意散漫を含む4種の注意挙動を測り、推論に重要なヘッドへKV予算を重点配分することで、長文脈の精度を保ちながらキャッシュを圧縮する。

- **2026-07 · [HYPIC: Accelerating Hybrid-Attention LLM Serving with Position-Independent Caching](2026-2607.01299-hypic-hybrid-attention-position-independent-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  線形注意区間の累積遷移演算子とゼロ始動状態を保存して位置非依存に合成し、完全注意層は境界窓だけ再計算、未保存区間は複数実体で並列処理することで、ハイブリッド注意言語モデルの初トークン待ち時間を平均3.25倍短縮する。

- **2026-07 · [HiKV: Hierarchical Importance-Aware KV Cache with Hardware Acceleration for LLM Decoding](2026-2607.22389-hikv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HiKVは、長文脈デコードでKVキャッシュが外部メモリアクセスの大部分を占める問題に対し、トークン単位と要素単位という二つの独立した冗長性を順番に削るアルゴリズム・ハードウェア協調設計である。1%以内の精度低下という同一条件で外部メモリアクセスを平均7.17倍削減し、注意計算を平均5.70倍、最大7.95倍高速化し、エネルギーを80〜90%削減する。

- **2026-07 · [2026-2607.05061-kvpop-key-value-cache-compression-with-predictive-online-pruning](2026-2607.05061-kvpop-key-value-cache-compression-with-predictive-online-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己回帰生成では過去トークンのキー・値状態をKVキャッシュへ保持するため、文脈長に比例してメモリ容量と読出し帯域が増える。既存の追い出し方式は累積注意量などの代理指標を使うことが多いが、「今まで重要だったトークン」が今後も重要とは限らず、推論途中で関連性が変わると誤った追い出しが起きる。

- **2026-06 · [RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention](2026-2606.06256-redknot-efficient-long-context-llm-serving-with-head-aware-kv-reuse-and-segpagedattention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来のKV管理は全ヘッドを同じトークンブロックとして扱うが、RedKnotの測定では局所ヘッドが83.4〜96.8%、接頭辞変化に敏感な大域ヘッドは3.2〜16.6%に留まる。そこで大域ヘッドだけを広範囲に再計算し、局所ヘッドを再利用するElastic Sparsityと、ヘッド別のKVページを扱うSegPagedAttentionを組み合わせる。

- **2026-06 · [RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference](2026-2606.31519-rabitqcache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈大規模言語モデルでは、復号の各ステップで巨大なKVキャッシュから注意計算用データを読むことがメモリ帯域のボトルネックになる。RaBitQCacheはランダム回転と二値量子化で小型索引を作り、不偏な注意スコア推定から累積確率に応じて必要量を変える上位確率検索（Top-p）を行う。

- **2026-06 · [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AsymCacheは、非連続KV区間を一つの注意カーネルで統合し、再利用確率と再計算遅延で追い出し、負荷適応チャンク化で長文サービングのGPU計算と管理費を減らす。

- **2026-05 · [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KARAは、新しく増えたKV区間だけを一度ずつ圧縮し、重要トークンを可変長チャンクへ広げ、周期発動で再圧縮費を抑えて長い推論の同時実行数を保つ。

- **2026-05 · [Dynamic-dLLM: Dynamic Cache-Budget and Adaptive Parallel Decoding for Training-Free Acceleration of Diffusion LLM](2026-2606.26120-dynamic-dllm-cache-budget-parallel-decoding.md)**  
  実装：[✓](https://github.com/TianyiWu233/DYNAMIC-DLLM) ・ リポジトリ内被引用：1  
  層別キャッシュ更新量とトークン別確定基準を動的化し、追加学習なしで最大4.48倍の拡散型LLM推論高速化を実現する。

- **2026-04 · [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SPINは、異なる疎注意方式の選択単位を共通ページへ写し、要求ごとのKV予算とGPU局所性キャッシュを調整して、階層メモリの転送とHBM圧力を減らす。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

- **2025-11 · [PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel](2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md)**  
  実装：[✓](https://github.com/flashserve/PAT) ・ リポジトリ内被引用：1  
  共有接頭辞を要求間で一度だけ読む詰込みと動的タイル選択により、復号注意の大域メモリ読出しと実行空洞を同時に削減する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems](2026-2609.27746-kv-cache-working-set-online-capacity-planning.md)**  
  実装：[✓](https://github.com/llc-kc/kv_cache_capacity_estimator) ・ リポジトリ内被引用：0  
  LRUのスタック距離をFenwick木で解析し、接頭辞KVキャッシュの目標ヒット率に必要な容量を1回の要求トレースからオンライン推定する。

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

- **2026-09 · [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](2026-2609.19969-deepseek-v4.1-flash-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CED・CSA2の層間KV再利用・FP4 KV・SWA限定再実行を統合し、100万トークン対応552B MoEのグローバルKVを890 bytes/トークン、永続KVを前世代比約1/8へ圧縮する。

- **2026-09 · [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits](2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文書編集で古くなったKVは重要位置の散発再計算より編集直後を連続再計算する方が有効で、隣接依存なら13〜21倍高速にほぼ完全修復する。

- **2026-09 · [Compressing Long Context into Answer-Aligned Memory Embeddings for LLM Inference](2026-2609.25537-cmc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈推論では自己注意の計算量が文脈長に対して二次的に増え、KVキャッシュは線形に増える。CMCは長文を少数の文脈記憶埋め込みへ変換し、質問に関係する記憶と直近の原文だけをデコーダへ与える。

- **2026-09 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](2026-2609.04971-beaconkv.md)**  
  実装：[✓](https://github.com/aiha-lab/BeaconKV) ・ リポジトリ内被引用：0  
  長い推論で過去の計画へ再注意する問い合わせを少数のビーコンとして保持し、将来再参照されるKVを予測して残す訓練不要の圧縮方式。

- **2026-09 · [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md)**  
  実装：[✓](https://github.com/LiuTaowen-Tony/agentkv) ・ リポジトリ内被引用：0  
  思考・行動・ツール応答など段階別の問い合わせ履歴でKV重要度を評価し、エージェントの段階遷移で必要になる古い状態を残しつつ、物理ページ圧縮で最大1.80倍の出力スループットを得る。

- **2026-08 · [vToken: Token-Level Virtualization for Reclaimable KV Caches](2026-2608.13263-vtoken-token-level-virtualization-for-reclaimable-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vToken は論理トークンと物理配置を分離するトークン表を導入し、生存トークンを非同期に詰め直す。

- **2026-08 · [ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents](2608.19662.md)**  
  実装：[✓](https://github.com/EIT-NLP/ReCache) ・ リポジトリ内被引用：0  
  ツール／スキル定義を組合せ非依存のKVブロックとして再利用し、重要な層・KVヘッド群と呼出し必須フィールドだけを残して、エージェント推論のプリフィルとKVメモリを削減する。

- **2026-08 · [PuzzleKV: Page-Wise Low-Rank Decomposition for KV Cache Compression](2026-2608.23843-puzzlekv-page-wise-low-rank-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PagedAttentionの固定長ページごとにKVを独立低ランク分解し、密ページと因子化ページを復元なしで同時に注意計算することで、学習不要のままKV容量を約60%へ削減する。

- **2026-08 · [Output-Aware Rotation for INT2 KV-Cache Quantization](2026-2608.02691-output-aware-rotation-int2-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OptRは、長文脈推論でKVキャッシュを2ビット整数へ量子化したとき、キーや値そのものの再構成誤差が小さくても、注意重みと出力射影を通過した後のモデル内部表現には大きな誤差が残り得る問題を扱う。

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

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
  GraphSpec実装では論理プロンプト、モデル重み、学習手順を変えず、4K〜128Kの長文脈質問応答で全文脈方式と同等の回答品質を維持しつつ、128K時の提案段階KVアクセスを元状態の5.5%まで減らした。

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

- **2026-06 · [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：0  
  CompressKVは、意味的証拠を検索する注意ヘッドだけでKVトークンを選び、層ごとの追い出し感度で容量を配分して、同じKV予算で長文品質を保つ。

- **2026-05 · [ArborKV: Structure-Aware KV Cache Management for Scaling Tree-based LLM Reasoning](2026-2605.22106-arborkv-structure-aware-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活動経路の保護、トークン単位の選択的追い出し、後戻り時の遅延再構築を組み合わせ、単一RTX 4090上のToT評価で同一キャッシュ予算の系列方式を上回り、256展開の探索を5.6 GiBで完了した。

- **2026-05 · [AgentKVShift: Efficient KV Cache Reuse for Agentic Memory Systems](2026-2607.21604-agentkvshift-agentic-memory-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  構造化エージェントメモリの一部トークンだけを再計算し、そこから推定したメモリ単位のKV残差を未再計算トークン全体へ加えて、低い再計算率で品質を回復する。

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

### 2年前（2024-10〜2025-09）

- **2025-03 · [vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention](2024-2405.04437-vattention-virtual-memory-kv-management.md)**  
  実装：[✓](https://github.com/microsoft/vattention) ・ リポジトリ内被引用：39  
  KVキャッシュの仮想アドレスを連続に保ったままCUDA仮想メモリで物理ページだけを需要時割当し、PagedAttention固有のブロック表と専用注意カーネルを不要にする方式。長文脈サービングで最大1.23倍のスループット改善を報告する。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：20  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：16  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2025-05 · [KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction](2025-2505.23416-kvzip.md)**  
  実装：[✓](https://github.com/snu-mllab/KVzip) ・ リポジトリ内被引用：11  
  元文脈の再構成時に使われるKVを重要とみなし、将来クエリを知らずに再利用可能な長文脈KVキャッシュを3〜4倍圧縮する。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：11  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：10  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2025-03 · [Jenga: Effective Memory Management for Serving LLM with Heterogeneity](2025-2503.18292-jenga-heterogeneous-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  異なる大きさ・依存関係のKV/視覚/Mamba状態を、LCM大ページと層別キャッシュAPIで統合管理し、vLLM比でスループット最大4.92倍、GPUメモリ利用を最大79.6%改善する。

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  Preserveは、テンソル並列のGPU間集約通信中に次の重みとKVをHBMからL2へ先読みし、通信待ちとメモリ読出しを重ねて分散推論の遅延を減らす。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：3  
  非同期KV先読みは、現在の注意ブロック計算中に次のKVをHBMからL2へ運び、Hopper GPUのメモリ待ちを隠して、注意カーネルとE2Eデコードを速める。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：2  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：2  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-07 · [Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing](2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話ごとの注意類似度から層間の鍵・値共有を動的選択し、注意類似度計算を中央処理装置と画像処理装置へ分担、圧縮後の再計算とロードを層間パイプラインで重畳してマルチターン状態復元を高速・省容量化する。

- **2025-07 · [HCAttention: Extreme KV Cache Compression via Heterogeneous Attention Computing for LLMs](2025-2507.19823-hcattention-heterogeneous-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キー量子化・値のCPU退避・層別の動的KV削除を統合し、GPU KV予算25%でLlama-3-8BのLongBench平均43.2を全注意と同値に保ち、12.5%でも42.5（0.7ポイント差）に抑える異種GPU/CPU注意方式。

- **2025-05 · [EFIM: Efficient Serving of LLMs for Infilling Tasks with Improved KV Cache Reuse](2025-2505.21889-efim-infilling-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/gty111/EFIM) ・ リポジトリ内被引用：0  
  FIMの増分を末尾へ移して接頭部・接尾部KVを要求間再利用し、断片トークン化学習で語途中生成能力を補って平均遅延52%削減・スループット98%向上。

### 3年前（2023-10〜2024-09）

- **2024-05 · [2024-2405.04434-deepseek-v2-mla](2024-2405.04434-deepseek-v2-mla.md)**  
  実装：✓ ・ リポジトリ内被引用：114  
  長文脈LLMでは注意のキー・値キャッシュが系列長に比例して増え、巨大モデルの同時処理数と生成速度を制約する。DeepSeek-V2はキーと値をそのまま全ヘッド分保存せず、入力隠れ状態を低次元潜在ベクトルへ圧縮して保存し、注意計算時に必要な表現へ復元するMLAを導入する。

- **2024-06 · [SnapKV: LLM Knows What You are Looking for Before Generation](2024-2404.14469-snapkv.md)**  
  実装：[✓](https://github.com/FasterDecoding/SnapKV) ・ リポジトリ内被引用：80  
  プロンプト末尾の観測窓から各注意ヘッドが将来参照する位置を推定し、重要KVだけをクラスタ単位で残して長文復号を軽量化する手法。

- **2024-02 · [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](2024-2402.02750-kivi.md)**  
  実装：[✓](https://github.com/jy-yuan/KIVI) ・ リポジトリ内被引用：79  
  キーはチャネル単位、値はトークン単位で2ビット量子化し、直近KVだけ高精度保持することで追加学習なしにKVメモリと帯域を削減し最大3.47倍のスループットを得る。

- **2024-01 · [KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization](2024-2401.18079-kvquant.md)**  
  実装：[✓](https://github.com/SqueezeAILab/KVQuant) ・ リポジトリ内被引用：69  
  Key分布に合わせたチャネル別・RoPE前・非一様・外れ値分離量子化で、3ビットKVを約4.8倍圧縮しつつパープレキシティ悪化0.1未満を実現する。

- **2024-06 · [PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling](2024-2406.02069-pyramidkv.md)**  
  実装：[✓](https://github.com/Zefan-Cai/PyramidKV) ・ リポジトリ内被引用：56  
  注意の層間集約パターンに合わせてKV予算を下層から上層へ逓減させ、同じ総メモリで固定予算型より長文脈性能を保つKVキャッシュ圧縮法。

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：47  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2023-10 · [Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs](2023-2310.01801-fastgen.md)**  
  実装：[✓](https://github.com/machilusZ/FastGen) ・ リポジトリ内被引用：42  
  FastGenは注意ヘッドごとの構造を一度だけ診断してKVキャッシュ保持方針を変え、追加学習なしでメモリ削減と長系列生成の高速化を両立する。

- **2024-07 · [Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference](2024-2407.11550-ada-kv.md)**  
  実装：[✓](https://github.com/FFY0/AdaKV) ・ リポジトリ内被引用：28  
  注意ヘッドごとの集中度に応じて同一層内のKV保持予算を再配分し、既存Top-k圧縮の総容量を変えずに追い出し損失を下げる手法。

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/hydragen) ・ リポジトリ内被引用：22  
  Hydragenは、共有接頭辞への複数系列のクエリをまとめて計算し、同じKVのHBM読出しを一度に処理して、共有プロンプトの注意帯域と実行効率を改善する。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  ALISAは、重要トークンを残す疎注意とKVのGPU・CPU・再計算配置、INT8量子化を系列長に応じて切替え、容量・PCIe転送・再計算費を抑える。

- **2024-05 · [KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization](2024-2405.03917-coupled-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  鍵値活性のチャネル間依存を利用して複数チャネルを共同量子化し、極低ビットでも品質劣化を抑える連結量子化を提案する。

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：8  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-06 · [A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression](2024-2406.11430-l2-kv-compression.md)**  
  実装：[✓](https://github.com/alessiodevoto/l2compress) ・ リポジトリ内被引用：6  
  キーのL2ノルムと注意重みの逆相関を利用し、注意重みを計算せず重要KVを残す学習不要の圧縮法。FlashAttention互換のまま、長文検索では50〜90%のKV削減でも高精度を維持する。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。

### 4年前（2022-10〜2023-09）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：153  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。

- **2023-06 · [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](2023-2306.14048-h2o.md)**  
  実装：[✓](https://github.com/FMInference/H2O) ・ リポジトリ内被引用：115  
  累積注意のヘビーヒッターと最新トークンを動的保持し、20%程度のKV予算で品質を維持しながらメモリ・スループットを改善する。

- **2023-05 · [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](2023-2305.17118-scissorhands.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  代表結果として、OPT系列の言語モデル評価と少数例学習評価で品質を大きく損なわずKVキャッシュを最大5倍圧縮した。

### 7年前（2019-10〜2020-09）

- **2019-11 · [Fast Transformer Decoding: One Write-Head is All You Need](2019-1911.02150-multi-query-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：60  
  クエリの複数ヘッドは維持しつつキーと値だけを全ヘッドで共有する複数クエリ注意を導入し、増分復号のKV読込み量をヘッド数分削減して、TPUv2上の復号を46µs/トークンから3.8µsへ短縮する。
<!-- survey:auto:end -->
