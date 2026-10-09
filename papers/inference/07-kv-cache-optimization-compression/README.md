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
## 自動生成の論文一覧（189本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-07 · [Gemma 4 Technical Report](2026-2607.02770-gemma-4-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  密モデルと混合専門家モデルを含むGemma 4の技術報告。局所・大域注意の配置、キー・値キャッシュ共有、キーの値への再利用、部分回転位置符号化、量子化対応学習、複数トークン予測ドラフタ、12Bの符号化器不要構成を組み合わせ、推論時の重み容量・KV容量・復号費用をそれぞれ減らす。数値はモデル系列・量子化形式・文脈長ごとに区別して読む必要がある。

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：8  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2025-11 · [TiDAR: Think in Diffusion, Talk in Autoregression](2025-2511.08923-tidar-think-in-diffusion-talk-in-autoregression.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  論文が対象にするのは、単に「拡散型言語モデルを速くする」ことではない。確定した接頭辞の鍵・値（KV）キャッシュは再利用でき、拡散型で問題になりやすい過去全体の再計算も避けられる。8B版の生成六課題平均正答率65.31%はQwen3-8Bの68.09%を下回り、元モデルと同じ出力分布を厳密に保存する手法ではない。

- **2026-05 · [LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents](2026-2602.01053-lragent-multilora-agent-kv-sharing.md)**  
  実装：[✓](https://github.com/jeonhye/lragent) ・ リポジトリ内被引用：6  
  multi-LoRAエージェントのKVを共有基盤成分と低ランク役割成分へ分解し、後者を全次元化せず注意計算することで、長い共有履歴のKVメモリと再プリフィルを削減する。

- **2025-11 · [TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection](2025-token-select.md)**  
  実装：[✓](https://github.com/pzs19/TokenSelect) ・ リポジトリ内被引用：6  
  各問い合わせで重要な鍵値をトークン単位に選び、ヘッド軟投票・選択キャッシュ・ページ化内積カーネルで長文脈注意を高精度かつ高速化する。

- **2026-05 · [Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management](2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  PBKVは、複数の言語モデルエージェントが同じ処理を分担する動的ワークフローで、次に使われる可能性が高いキー・値キャッシュ（KVキャッシュ）をGPUに残し、必要に応じてホストメモリから先読みする仕組みである。

- **2026-01 · [KVzap: Fast, Adaptive, and Faithful KV Cache Pruning](2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：5  
  KVzapは、長文脈大規模言語モデル（LLM）のキー・バリューキャッシュ（KV キャッシュ）を時間軸方向に削減する手法である。Qwen3-8B/32BとLlama-3.1-8B-Instructで、長文脈検索・理解・reasoningを大きく崩さず平均63〜72%のKVを除去し、2.7〜3.5倍の実効圧縮を報告する。

- **2026-07 · [LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning](2026-lazyeviction.md)**  
  実装：[✓](https://github.com/Halo-949/LazyEviction) ・ リポジトリ内被引用：4  
  一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：4  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：[✓](https://github.com/omnia-postech/OrbitFlow) ・ リポジトリ内被引用：4  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

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

- **2026-01 · [ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation](2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cac.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  文書ごとに事前計算したキー・値キャッシュ (key-value キャッシュ; KV キャッシュ) を再利用すれば計算は省けるが、各文書を単独で計算したKVには他文書や今回のユーザー質問との交差注意 (cross-注意機構) が入っていない。こうして質問に必要な交差注意を優先的に修復し、20%程度の再計算で全プリフィルに近い品質を狙う。

- **2026-07 · [KV Cache Translation across Heterogeneous Large Language Models](2026-2607.28979-kv-cache-translation-across-heterogeneous-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の単一射影や共有潜在空間を介す方式と異なり、MoTは複数の変換器を用意し、トークンごとに適切な変換器を上位K個選択して出力を混合する。Llama-3.2 3B、Gemma-3 4B、Qwen-3 4B間の異種変換を評価し、閉集合質問応答の平均正解率57.6%、抽出型質問応答の平均F1 0.42を報告する。

- **2026-06 · [RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention](2026-2606.06256-redknot-efficient-long-context-llm-serving-with-head-aware-kv-reuse-and-segpagedattention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来のKV管理は全ヘッドを同じトークンブロックとして扱うが、RedKnotの測定では局所ヘッドが83.4〜96.8%、接頭辞変化に敏感な大域ヘッドは3.2〜16.6%に留まる。そこで大域ヘッドだけを広範囲に再計算し、局所ヘッドを再利用するElastic Sparsityと、ヘッド別のKVページを扱うSegPagedAttentionを組み合わせる。

- **2026-04 · [When Hidden States Drift: Can KV Caches Rescue Long-Range Speculative Decoding?](2026-2604.26412-when-hidden-states-drift-can-kv-caches-rescue-long-range-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は、小さなドラフトモデルが先の複数トークンを提案し、大きな対象モデルが一括で検証することで逐次生成の遅延を減らす。Qwen3-8Bでの実験では、KV再利用は後方の投機ステップの受理率を改善し、混成方式は小規模な逐次受理評価で平均受理トークン数を2.37から2.54へ増やした。

- **2026-04 · [The Illusion of Equivalence: Systematic FP16 Divergence in KV-Cached Autoregressive Inference](2026-2604.15409-the-illusion-of-equivalence-systematic-fp16-divergence-in-kv-cached-auto.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、自己回帰推論で標準的に用いられるKVキャッシュ（KV キャッシュ）が、キャッシュを無効化して各段階でprefix全体を再計算する経路と「数学的には同値だから、同じトークン列を返す」とみなされてきた前提をFP16実装で検証する分析論文である。中心的な主張は「KV キャッシュというアルゴリズム自体が近似だから違う」のではない。

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
  複数エージェント型の大規模言語モデル推論では、システム指示、道具定義、共有メモリなどからなる長い接頭辞を複数要求が共有し、その後ろに各要求固有の生成履歴が接尾辞として伸びる。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：1  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-07 · [REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression](2026-real-kv.md)**  
  実装：[✓](https://github.com/yonseicasl/REAL) ・ リポジトリ内被引用：1  
  成功例だけでなく偏り・注意散漫を含む4種の注意挙動を測り、推論に重要なヘッドへKV予算を重点配分することで、長文脈の精度を保ちながらキャッシュを圧縮する。

- **2026-07 · [MosaicKV: Serving Long-Context LLM with Dynamic Two-D KV Cache Compression](2026-2607.00760-mosaickv-serving-long-context-llm-with-dynamic-two-d-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MosaicKVは、極長文脈のKVキャッシュを系列方向とチャネル方向の両方で圧縮し、容量削減だけでなく注意計算そのものを高速化するサービングシステムである。一方、両者を単純に組み合わせると重要要素まで二重に捨ててしまい、論文のQuestベース素朴実装ではチャネル圧縮率30%で24.5%、70%で82.8%の精度低下が生じる。

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

- **2026-06 · [Kamera: Unified Position-Invariant Multimodal KV Cache for Training-Free Reuse](2026-2606.23581-kamera-unified-position-invariant-multimodal-kv-cache-for-training-free-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Kameraは、画像・動画・画面の断片を繰り返し参照する視覚言語モデルのエージェントで、以前に計算した鍵・値キャッシュ（KVキャッシュ）を異なる文脈位置へ移して再利用するための方式である。

- **2026-06 · [Information-Aware KV Cache Compression for Long Reasoning](2026-2606.26875-information-aware-kv-cache-compression-for-long-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来の鍵値キャッシュ（KV キャッシュ）圧縮は、直近の問い合わせから大きな注意（注意機構）を受けたトークンを残す設計が多い。LongReasonでは40%・20%の鍵値キャッシュ保持率でSnapKV、PyramidKV、Expected 注意機構を上回り、長い復号でもRPCより高いタスク性能を示す。

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
  実装：[✓](https://github.com/SayedPedramHaeri/Dont-Waste-Bits) ・ リポジトリ内被引用：1  
  本研究は、端末上で動かす小型言語モデルのキー・値キャッシュ（KVキャッシュ）を、トークンごとの重要度に応じて異なるビット幅で保存する適応量子化方式を提案する。SmolLM-360MとHellaSwagの実機評価では、固定4ビットの正答率33.6%、遅延2.93に対して、提案方式は41.2%、2.41だった。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

- **2026-02 · [InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache for Large Language Models](2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  InnerQは、長文脈デコードで増え続けるキー・バリューキャッシュ（KV キャッシュ）を低ビット化する際、量子化誤差だけでなく「量子化済みKVをGPU上で復号してベクトル行列積（GEMV）へ渡すときのスケール/ゼロ点読み出し」を主要ボトルネックとして設計する調整不要のKV量子化方式である。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [VestigeKV: The NoPE-MLA KV Cache Carries Its Own Eviction Signal in a Vestigial Branch](2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-eviction-signal-in-a-ves.md)**  
  実装：[✓](https://github.com/fan-wenjie/vestigekv) ・ リポジトリ内被引用：0  
  選ばれた行だけを毎回の注意計算へ送り、残りはビット列を変えずGPU内の退避領域へ保存する。著者の実装資料は、Kimi Linear 48B-A3Bを対象とした2台のRTX PRO 6000 Blackwellで、単一要求の連続復号において256K文脈で約1.28倍、496Kで約1.46倍の速度比を示す。

- **2026-09 · [Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management](2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-mana.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数LLMを品質・価格・遅延に応じて切り替えるモデルルーティングは、単一モデル固定より効率的になり得る。8種類のワークロードを使う解析シミュレーションでは、キャッシュ準備時間をTTFTの代理指標として1.25〜13.28倍、入力トークン費用を1.20〜6.16倍改善する可能性を報告する。

- **2026-09 · [To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems](2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-.md)**  
  実装：[✓](https://github.com/FastLM/KVLearn) ・ リポジトリ内被引用：0  
  KVLearnは、プリフィル（プリフィル）とデコード（デコード）を別ノード プールへ分離するLLM サービングで、KV キャッシュを「残す／捨てる」判断を単なるLRUではなく期待コスト最小化として扱う。

- **2026-09 · [The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems](2026-2609.27746-kv-cache-working-set-online-capacity-planning.md)**  
  実装：[✓](https://github.com/llc-kc/kv_cache_capacity_estimator) ・ リポジトリ内被引用：0  
  LRUのスタック距離をFenwick木で解析し、接頭辞KVキャッシュの目標ヒット率に必要な容量を1回の要求トレースからオンライン推定する。

- **2026-09 · [The KV Cache Is the New Memory Wall](2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しいKV圧縮器やGPUカーネルの実装ではなく、既存研究が異なる条件で報告してきた改善率を解釈するための分析枠組みを作る。例えばLlama-3-70BをBF16で扱う場合、重みは約140GB、1系列128kトークンのKVは約42GBである。

- **2026-09 · [StepKV: Step-Aware KV Cache Compression for LLM Agents](2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの自己回帰生成では、過去トークンの鍵と値を保存する鍵値キャッシュ（KVキャッシュ）が、次トークンの注意計算で過去の隠れ状態を再計算せずに済ませる。キャッシュ圧縮で一部のトークンを捨てると容量を減らせるが、注意重みが小さいトークンが将来も不要であるとは限らない。

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
  チャンク型KVキャッシュ圧縮（chunked KV-キャッシュ compression）は、連続するトークンを固定幅の窓へ区切り、各窓を少数のK/V表現へ要約することで長文脈推論のKV容量と注意計算を削減する。

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
  H-Specは、投機的復号（投機的復号）の軽量な候補生成器であるドラフターが、対象モデルの隠れ状態を各入力位置で別の鍵・値キャッシュ（KV キャッシュ）へ射影して保存する方式に対し、その追加キャッシュを廃止するための混成Mamba・注意ドラフターである。

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
  本研究は、固定形状の計算グラフ内で必要なトークンだけ再計算する方式、複数グラフ呼出しを統合する動的計画法、NPU・CPUメモリ・フラッシュにまたがる階層KV保存、読み込み・位置補正・保存とNPU実行の非同期重畳を組み合わせる。

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
  行動生成時の注意履歴で将来の操作に必要なキー・値状態を選び、生成確信度に応じて保存枠を拡張し、ページ化された実キャッシュを追加作業領域なしで圧縮する。ReAct型の長期タスクでは、無圧縮方式に対する平均タスク精度98.53%を、ピークKV容量25.98%で維持する。

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
  実装：[✓](https://github.com/daniel-eai/Output-Aware-INT2-KV-Cache-Quantization) ・ リポジトリ内被引用：0  
  OptRは、長文脈推論でKVキャッシュを2ビット整数へ量子化したとき、キーや値そのものの再構成誤差が小さくても、注意重みと出力射影を通過した後のモデル内部表現には大きな誤差が残り得る問題を扱う。

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

- **2026-08 · [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](2026-2608.02515-livemem-maintaining-memory-state-continuity-in-long-running-llm-inferenc.md)**  
  実装：[✓](https://github.com/cafeii/LiveMem) ・ リポジトリ内被引用：0  
  長時間稼働する対話支援や自律エージェントでは、対話履歴がモデルの注意機構（注意機構）の文脈窓を超える。Qwen3-4Bを基盤とする制限文脈の実験では、教師あり微調整と強化学習を経たLiveMemの全課題総合スコアが0.519で、基盤モデルの0.458を上回る。

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

- **2026-07 · [Set Diffusion: Interpolating Token Orderings Between Autoregression and Diffusion for Fast and Flexible Decoding](2026-2607.01775-set-diffusion-interpolating-token-orderings-between-autoregression-and-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この設計により、集合サイズ1なら自己回帰に近づき、全位置を1集合にすれば通常の順序非依存拡散に近づく。公開評価では数学推論、要約、無条件生成で従来の拡散方式より良い速度―品質交換条件を示し、同程度の尤度を持つブロック拡散とのOpenWebText比較では22%高速な復号を報告する。

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

- **2026-05 · [Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles](2026-2605.19775-understanding-inference-scaling-for-llms-bottlenecks-trade-offs-and-perf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、新しい推論アルゴリズムを提案するのではなく、推論型大規模言語モデル（reasoning LLM）の長い思考連鎖（Chain-of-Thought; CoT）が推論基盤のボトルネックをどう変えるかを、8Bから671Bまでのモデルと8基のNVIDIA H200で系統的に測定する性能特性研究である。

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
  実装：[✓](https://github.com/microsoft/vattention) ・ リポジトリ内被引用：52  
  KVキャッシュの仮想アドレスを連続に保ったままCUDA仮想メモリで物理ページだけを需要時割当し、PagedAttention固有のブロック表と専用注意カーネルを不要にする方式。長文脈サービングで最大1.23倍のスループット改善を報告する。

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：27  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2024-12 · [A Survey on Large Language Model Acceleration based on KV Cache Management](2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-manageme.md)**  
  実装：[✓](https://github.com/TreeAI-Lab/Awesome-KV-Cache-Management) ・ リポジトリ内被引用：22  
  キャッシュを減らせば容量は空くが、注意品質の低下、検索・量子化の追加計算、CPU/SSD転送、再計算など別の費用が発生する。

- **2025-10 · [Expected Attention: KV Cache Compression by Estimating Attention from Future Queries Distribution](2025-2510.00636-expected-attention-kv-cache-compression-by-estimating-attention-from-fut.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：21  
  Expected 注意機構は、大規模言語モデルの推論で増大する鍵・値キャッシュ（KV キャッシュ）を、追加学習なしに選択削除する方法である。Qwen3-8BのRULER 16Kでは、キャッシュ50%削除でも無圧縮92.9に対し92.7を維持する。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：18  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：18  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2025-05 · [KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction](2025-2505.23416-kvzip.md)**  
  実装：[✓](https://github.com/snu-mllab/KVzip) ・ リポジトリ内被引用：17  
  元文脈の再構成時に使われるKVを重要とみなし、将来クエリを知らずに再利用可能な長文脈KVキャッシュを3〜4倍圧縮する。

- **2024-11 · [DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving](2024-2411.02820-droidspeak-kv-cache-sharing-for-cross-llm-communication-and-multi-llm-se.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  DroidSpeakは、同じ基盤モデルを微調整して得た異なるLLMが、同じ会話履歴や文書を別々に処理する際の重複プリフィルを減らす分散推論システムである。著者らは8種類のモデル対で層別の感度を測定し、KV差異に敏感な層は平均約11%と報告した。

- **2025-04 · [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](2025-2504.19874-turboquant-online-vector-quantization-with-near-optimal-distortion-rate.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  TurboQuantは、高次元ベクトルを入力データセットに合わせて学習し直さずに低ビット化する、オンライン量子化方式である。理論面では、復元二乗誤差と内積誤差の両方について、ビット幅bに対して概ね4のマイナスb乗で減る上界を示し、情報理論的な下限との差が最大約2.7倍の定数内であると証明する。

- **2024-12 · [ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression](2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-com.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/ClusterKV) ・ リポジトリ内被引用：12  
  鍵値キャッシュ（KVキャッシュ）を全量GPUに置くと、文脈長に比例して必要メモリが増え、各復号ステップで読み出すデータ量も増加する。これを抑える方法には、不要なトークンのKVを永久に破棄する方法と、CPUなど低速階層に退避したKVを必要に応じて呼び戻す方法がある。GPUでの復号遅延は最大2倍、処理率は最大2.5倍改善したと報告する。

- **2025-10 · [Cache-to-Cache: Direct Semantic Communication Between Large Language Models](2025-2510.03215-cache-to-cache-direct-semantic-communication-between-large-language-mode.md)**  
  実装：[✓](https://github.com/thu-nics/C2C) ・ リポジトリ内被引用：11  
  複数の大規模言語モデル（LLM）が協調するシステムでは、あるモデルが推論や分析の結果を文章として生成し、別のモデルがその文章を読み込んで次の応答を作ることが多い。

- **2025-01 · [RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations](2025-2501.16383-rotatekv-accurate-and-robust-2-bit-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/ZunhaiSu/RotateKV) ・ リポジトリ内被引用：10  
  RotateKVは、キー・バリュー（Key-Value; KV）キャッシュを2ビットへ落とす前に、外れ値が特定チャネルへ集中しないよう適応回転する。

- **2024-12 · [DiffKV: Differentiated Memory Management for Large Language Models with Parallel KV Compaction](2024-2412.03131-diffkv-differentiated-memory-management-for-large-language-models-with-parallel-kv-compaction.md)**  
  実装：[✓](https://github.com/zyqCSL/DiffKV) ・ リポジトリ内被引用：10  
  鍵・値・トークン・注意ヘッドを異なる粒度で圧縮し、不規則な空き容量をGPU内で並列コンパクションするDiffKV。KVを2.7〜5.7倍圧縮しスループットを1.9〜5.4倍改善する。

- **2025-03 · [Jenga: Effective Memory Management for Serving LLM with Heterogeneity](2025-2503.18292-jenga-heterogeneous-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  異なる大きさ・依存関係のKV/視覚/Mamba状態を、LCM大ページと層別キャッシュAPIで統合管理し、vLLM比でスループット最大4.92倍、GPUメモリ利用を最大79.6%改善する。

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  Preserveは、テンソル並列のGPU間集約通信中に次の重みとKVをHBMからL2へ先読みし、通信待ちとメモリ読出しを重ねて分散推論の遅延を減らす。

- **2025-03 · [xKV: Cross-Layer KV-Cache Compression via Aligned Singular Vector Extraction](2025-2503.18893-xkv-cross-layer-kv-cache-compression-via-aligned-singular-value-decomposition.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/xKV) ・ リポジトリ内被引用：7  
  xKVは、隣接層のキー・バリュー（Key-Value; KV）キャッシュをトークンごとに直接似ているとみなすのではなく、複数層が共有する支配的な特異ベクトルをまとめて抽出する。プリフィル時に複数層を横連結して共有低ランク基底へ因子分解し、デコード時はクエリに重要なトークンだけを選択的に再構成する。

- **2025-02 · [QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache](2025-2502.10424-quantspec-self-speculative-decoding-with-hierarchical-quantized-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  QuantSpecは、長い文脈を持つ大規模言語モデルの復号で、鍵値キャッシュ（KVキャッシュ）の読出しがGPU帯域と容量を圧迫する問題を、階層量子化キャッシュを共有する自己投機的復号によって改善する。

- **2024-12 · [KunServe: Parameter-centric Memory Management for Efficient Memory Overloading Handling in LLM Serving](2024-2412.18169-kunserve-elastic-and-efficient-large-language-model-serving-with-paramet.md)**  
  実装：[✓](https://github.com/SJTU-IPADS/kunserve) ・ リポジトリ内被引用：7  
  リクエストのKVキャッシュを捨てる代わりに、複数の推論インスタンスに重複配置されたモデル重みを一時解放する。残存する層を複数GPUで協調実行し、通信とバッチ形成を調整することで、突発負荷時の待ち行列を短縮する。

- **2025-06 · [KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider](2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at.md)**  
  実装：[✓](https://github.com/vllm-project/vllm/pull/22236) ・ リポジトリ内被引用：6  
  合成トレースではなく本番サービスのトレースに基づく設計材料が不足しているという問題に対し、本研究はAliyun Tongyiの大規模serving クラスタから得た顧客向け(to-C)と企業向け(to-B)のトレースを特徴付け、観測した分布を使う追い出し 方策を提案する。

- **2025-08 · [KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache](2025-2509.00579-kvcomp-a-high-performance-llm-aware-lossy-compression-framework-for-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KVCompは、大規模言語モデルの長文脈推論において、過去トークンの鍵・値（KV）キャッシュがGPUメモリを占有し、処理可能な文脈長や同時実行数を制限する問題に取り組む。既存の低ビット量子化だけでは整数符号に残る統計的偏りを使い切れず、一般的な可逆圧縮を追加すると毎トークン必要な復号が遅くなる。

- **2025-07 · [Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation](2025-2507.10524-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-tok.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  共有Transformerブロックを再帰利用し、ルータがトークンごとに継続深度を決めて活動集合だけへ注意・KV保持することで、推論時の適応計算とパラメータ共有を両立する。

- **2025-06 · [CommVQ: Commutative Vector Quantization for KV Cache Compression](2025-2506.18879-commvq-commutative-vector-quantization-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UMass-Embodied-AGI/CommVQ) ・ リポジトリ内被引用：4  
  CommVQは、KVキャッシュを複数の符号帳ベクトルの和で表す加算型ベクトル量子化（additive vector 量子化）を使い、特にキー側の符号帳を回転位置埋め込み（Rotary Position Embedding; RoPE）と交換可能になるよう学習する。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：4  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-05 · [ReCalKV: Low-Rank KV Cache Compression via Head Reordering and Offline Calibration](2025-2505.24357-recalkv-low-rank-kv-cache-compression-via-head-reordering.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/ReCalKV) ・ リポジトリ内被引用：4  
  KeyとValueは注意機構で同じ役割ではない。ReCalKVは、Keyには「似たヘッドをまとめて低ランク化」、Valueには「データで低ランク因子を補正して復元行列を次の射影へ融合」という別々の圧縮を割り当て、高圧縮時の品質と実行時オーバーヘッドを両方抑える。

- **2025-05 · [R-KV: Redundancy-aware KV Cache Compression for Reasoning Models](2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md)**  
  実装：[✓](https://github.com/Zefan-Cai/R-KV) ・ リポジトリ内被引用：4  
  R-KVは、推論モデルが数学問題を解く際に生成する長い思考過程に含まれる重複を利用し、自己回帰復号中の鍵値キャッシュ（Key-Value キャッシュ、以下KVキャッシュ）を固定予算に抑える手法である。論文の例では8Bモデルが約32Kトークンを生成する場合、重み15.5GBに加えてKVキャッシュ約4.1GBを要する。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：4  
  本研究は、大規模言語モデルの自己回帰復号において、鍵値キャッシュ（KV キャッシュ）を高帯域メモリ（HBM）から読み込む間にGPUの実行単位が待たされる問題を対象とする。鍵値を削除・量子化・オフロードして保存容量を減らすのではなく、現在の鍵値ブロックを使った注意演算と、次に必要なブロックのHBMから二次キャッシュ（L2 キャッシュ）への転送を重ねる。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

- **2025-02 · [CriticalKV: Optimizing KV Cache Eviction from an Output Perturbation Perspective](2025-2502.03805-criticalkv-optimizing-kv-cache-eviction-from-an-output-perturbation-perspective.md)**  
  実装：[✓](https://github.com/FFY0/DefensiveKV) ・ リポジトリ内被引用：4  
  KVキャッシュ追い出しを「注意出力摂動の最小化」として定式化し、注意重み×出力射影後の値状態ノルムで重要KVを選ぶ二段階方式により、既存3方式の圧縮損失を29データセット平均で半分超削減する。

- **2025-10 · [Attention Is All You Need for KV Cache in Diffusion LLMs](2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Elastic-Cache) ・ リポジトリ内被引用：3  
  従来の安全な実装は、各復号段階ですべての位置と層のクエリ・キー・値を再計算するが、変化の少ない状態まで繰り返し計算するため遅い。提案方式は、左側の未確定位置を中心とする移動窓で新しいトークンを予測し、窓外MASKのKVを再利用する。

- **2025-05 · [PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs](2025-2505.18610-pm-kvq-progressive-mixed-precision-kv-cache-quantization-for-long-cot-llms.md)**  
  実装：[✓](https://github.com/thu-nics/PM-KVQ) ・ リポジトリ内被引用：3  
  KVを16→8→4→2bitと必要時だけ段階圧縮し、層感度とRoPE位置補間校正で長CoTの累積量子化誤差を抑えるPM-KVQ。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：2  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-10 · [VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization](2025-2510.06175-vecinfer-efficient-llm-inference-with-low-bit-kv-cache-via-outlier-suppr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キャッシュ量は文脈長に比例して増えるため、長い入力を扱う際にはGPUの高帯域メモリ（HBM）容量が不足し、デコード中の読み出し量も大きくなる。ベクトル量子化（VQ）は複数要素を一つの代表ベクトルへ対応付け、各小ベクトルを短い索引として保存する。長文脈192K入力・129出力のH100単一バッチでは、2ビット構成でデコード遅延が8.3倍改善した。

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
  実装：✓ ・ リポジトリ内被引用：179  
  通常の多頭注意（Multi-Head 注意機構; MHA）では、系列長が伸びるほどKVキャッシュが線形に増え、GPU高帯域メモリ（High Bandwidth メモリ; HBM）に置ける同時要求数や最大文脈長を圧迫する。

- **2024-06 · [SnapKV: LLM Knows What You are Looking for Before Generation](2024-2404.14469-snapkv.md)**  
  実装：[✓](https://github.com/FasterDecoding/SnapKV) ・ リポジトリ内被引用：149  
  プロンプト末尾の観測窓から各注意ヘッドが将来参照する位置を推定し、重要KVだけをクラスタ単位で残して長文復号を軽量化する手法。

- **2024-02 · [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](2024-2402.02750-kivi.md)**  
  実装：[✓](https://github.com/jy-yuan/KIVI) ・ リポジトリ内被引用：143  
  キーはチャネル単位、値はトークン単位で2ビット量子化し、直近KVだけ高精度保持することで追加学習なしにKVメモリと帯域を削減し最大3.47倍のスループットを得る。

- **2024-01 · [KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization](2024-2401.18079-kvquant.md)**  
  実装：[✓](https://github.com/SqueezeAILab/KVQuant) ・ リポジトリ内被引用：138  
  Key分布に合わせたチャネル別・RoPE前・非一様・外れ値分離量子化で、3ビットKVを約4.8倍圧縮しつつパープレキシティ悪化0.1未満を実現する。

- **2024-06 · [PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling](2024-2406.02069-pyramidkv.md)**  
  実装：[✓](https://github.com/Zefan-Cai/PyramidKV) ・ リポジトリ内被引用：92  
  注意の層間集約パターンに合わせてKV予算を下層から上層へ逓減させ、同じ総メモリで固定予算型より長文脈性能を保つKVキャッシュ圧縮法。

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：79  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2024-10 · [DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads](2024-2410.10819-duoattention-efficient-long-context-llm-inference-with-retrieval-and-str.md)**  
  実装：[✓](https://github.com/mit-han-lab/duo-attention) ・ リポジトリ内被引用：49  
  デコード時には過去のKVを読み出すため遅延も長くなり、プリフィルでは注意計算が系列長の二乗に増える。DuoAttentionは、全ての注意ヘッドが遠距離の情報を必要とするわけではないという観測に基づき、ヘッドごとに全履歴を残すか、固定長の履歴だけ残すかを切り替える方式である。

- **2024-07 · [Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference](2024-2407.11550-ada-kv.md)**  
  実装：[✓](https://github.com/FFY0/AdaKV) ・ リポジトリ内被引用：49  
  注意ヘッドごとの集中度に応じて同一層内のKV保持予算を再配分し、既存Top-k圧縮の総容量を変えずに追い出し損失を下げる手法。

- **2024-03 · [GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM](2024-2403.05527-gear-an-efficient-kv-cache-compression-recipe-for-near-lossless-generati.md)**  
  実装：[✓](https://github.com/HaoKang-Timmy/GEAR) ・ リポジトリ内被引用：44  
  GEARは、自己回帰生成で増え続けるKVキャッシュを高い圧縮率で保持しつつ、単純な低ビット量子化で生じる生成品質の崩壊を抑えるための圧縮法である。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：30  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/jordan-benjamin/hydragen) ・ リポジトリ内被引用：30  
  共通のシステム指示、少数例の例示、同一問題に対する多数の候補生成などでは、異なる要求が接頭辞の鍵・値キャッシュを共有する。原著はCodeLlama-13Bを8枚のA100-40GBで実行し、大きなバッチと長い共有接頭辞でvLLMのページ注意に対して端点処理率最大32倍を報告する。

- **2024-03 · [Jamba: A Hybrid Transformer-Mamba Language Model](2024-2403.19887-jamba-a-hybrid-transformer-mamba-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  系列が長くなると鍵値キャッシュ（KVキャッシュ）の容量と読出し量が増え、GPUのメモリ容量・帯域を圧迫する。さらに混合専門家モデル（Mixture-of-Experts、MoE）を一部の前向き全結合層へ導入し、総パラメータ容量とトークン当たりの有効計算量を分離する。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  ALISAは、重要トークンを残す疎注意とKVのGPU・CPU・再計算配置、INT8量子化を系列長に応じて切替え、容量・PCIe転送・再計算費を抑える。

- **2024-02 · [No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization](2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  自己回帰推論の鍵・値キャッシュ（KVキャッシュ）は、生成済みの各トークンの中間状態を再利用して再計算を避ける一方、必要容量が同時要求数と文脈長にほぼ比例して増える。提案する混合精度KVキャッシュ（MiKV）は、重要トークンを高精度で保持し、従来なら追い出すトークンも2〜4ビットで保存する。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：22  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-02 · [ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition](2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-t.md)**  
  実装：[✓](https://github.com/microsoft/chunk-attention) ・ リポジトリ内被引用：21  
  ChunkAttentionは、同じ言語モデルを複数の利用者・アプリケーションへ提供する際に、要求の先頭で共有されるシステム指示や少数例を計算と記憶の両面で再利用する推論用注意機構である。

- **2024-05 · [KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization](2024-2405.03917-coupled-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  鍵値活性のチャネル間依存を利用して複数チャネルを共同量子化し、極低ビットでも品質劣化を抑える連結量子化を提案する。

- **2024-03 · [Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference](2024-2403.09636-dynamic-memory-compression-retrofitting-llms-for-accelerated-inference.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM/tree/DMC) ・ リポジトリ内被引用：19  
  動的メモリ圧縮（動的 メモリ Compression; DMC）は、過去トークンを「残す／捨てる」の二択にせず、各注意ヘッドが新しいキー・値（Key-Value; KV）を新規スロットへ追加するか、直前のスロットへ重み付きで結合するかを学習する。これにより、内容・層・ヘッドごとに必要な時間解像度を変えながらKVキャッシュをオンライン圧縮する。

- **2024-05 · [MiniCache: KV Cache Compression in Depth Dimension for Large Language Models](2024-2405.14366-minicache-kv-cache-compression-in-depth-dimension-for-large-language-mod.md)**  
  実装：[✓](https://github.com/AkideLiu/MiniCache) ・ リポジトリ内被引用：18  
  MiniCacheは層内のトークン選別や低ビット化だけでなく、隣り合う層のあいだにも冗長性があると観察し、中層以降で同じ位置のKV状態を共有表現へ統合する。

- **2024-02 · [GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding](2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  本論文は、大規模言語モデルの生成時に生じる逐次計算の待ち時間を、投機的復号（投機的復号）の二つの構成要素から短縮する研究である。投機的復号では軽量な下書きモデルが数トークンを先に提案し、大型の対象モデルが一度の前向き計算で提案を検証する。

- **2024-07 · [Keep the Cost Down: A Review on Methods to Optimize LLM's KV Cache Consumption](2024-2407.18003-keep-the-cost-down-a-review-on-methods-to-optimize-llm-s-kv-cache-consum.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  本論文はKVキャッシュ最適化を、事前学習時のアーキテクチャ変更、配備時のメモリ管理・再利用、学習後の削除・統合・量子化という時間軸で整理する。

- **2024-05 · [ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification](2024-2405.14256-zipcache.md)**  
  実装：[✓](https://github.com/ThisisBillhe/ZipCache) ・ リポジトリ内被引用：17  
  ZipCacheは、長文脈推論で肥大化する鍵・値キャッシュ（KV キャッシュ）を、重要トークンの識別と混合精度量子化によって圧縮する手法である。そこでZipCacheは最近5%とランダム5%のプローブトークンの注意スコアだけを求め、残りのトークンは高速注意経路を維持する。

- **2024-02 · [Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference](2024-2402.09398-get-more-with-less-synthesizing-recurrence-with-kv-cache-compression-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/hdong920/LESS) ・ リポジトリ内被引用：17  
  LESSは、キー・値キャッシュ（Key-Value Cache; KVキャッシュ）の追い出しを「残すか捨てるか」の二択にしない。重要なトークンは従来どおり疎KVキャッシュへ明示的に残し、追い出すトークンは固定サイズの低ランク状態へ順次圧縮する。次の注意計算では両方を合成するため、疎キャッシュから消えたトークンにも低解像度ながら参照経路が残る。

- **2024-10 · [Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning](2024-2410.19258-not-all-heads-matter-a-head-level-kv-cache-compression-method-with-integ.md)**  
  実装：[✓](https://github.com/FYYFU/HeadKV) ・ リポジトリ内被引用：16  
  従来の圧縮方式は、最近の注意得点を利用して残すトークンを選んだり、層ごとに予算を変えたりする。論文は文脈QAの代表条件で元キャッシュの約1.5%を保持しながら完全キャッシュ性能の97%を得たと報告するが、これは全タスク・全モデルで97%という保証ではない。

- **2024-07 · [RazorAttention: Efficient KV Cache Compression Through Retrieval Heads](2024-2407.15891-razorattention-efficient-kv-cache-compression-through-retrieval-heads.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  RazorAttentionは、長い入力を処理する大規模言語モデルの鍵・値キャッシュ（KV キャッシュ）を、注意頭ごとの機能差に基づいて圧縮する手法である。原著の既定設定では、非検索頭に残す近傍長を max(4000,N/5)、系列先頭の保持数を4とし、誘導頭の上位14%と反復頭の上位1%を検索頭として保護する。

- **2024-03 · [QAQ: Quality Adaptive Quantization for LLM KV Cache](2024-2403.04643-qaq-quality-adaptive-quantization-for-llm-kv-cache.md)**  
  実装：[✓](https://github.com/ClubieDong/KVCacheQuantization) ・ リポジトリ内被引用：16  
  QAQは、自己回帰型大規模言語モデルの鍵値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を、すべてのトークンで一律のビット幅にするのではなく、注意出力の誤差許容量に応じてキー（Key; K）と値（Value; V）を別々に量子化する方式である。

- **2024-10 · [LayerKV: Optimizing Large Language Model Serving with Layer-wise KV Cache Management](2024-2410.00428-layerkv-optimizing-large-language-model-serving-with-layer-wise-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  LayerKVは、長文脈LLMの最初のトークンまでの時間（時間 to First トークン; TTFT）が増える主因を、プリフィル計算そのものだけでなく「十分なGPU KVブロックが空くまで新規リクエストを開始できない待ち行列」と捉え、KVキャッシュ管理の粒度をリクエスト単位から層単位へ細かくするサービング手法である。

- **2024-07 · [ThinK: Thinner Key Cache by Query-Driven Pruning](2024-2407.21018-think-thinner-key-cache-by-query-driven-pruning.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/ThinK) ・ リポジトリ内被引用：13  
  ThinKは、長文脈生成に必要な鍵・値キャッシュ（KVキャッシュ）のうち、鍵（Key）ベクトル内部のチャネルを選択的に削除する圧縮手法である。ICLR 2025の著者論文では、H2OやSnapKVへ40%のKeyチャネル削減を追加してもLongBenchの平均スコアがほぼ維持される例を示す。

- **2024-03 · [Keyformer: KV Cache reduction through key tokens selection for Efficient Generative Inference](2024-2403.09054-keyformer-kv-cache-reduction-through-key-tokens-selection-for-efficient-.md)**  
  実装：[✓](https://github.com/d-matrix-ai/keyformer-llm) ・ リポジトリ内被引用：12  
  Keyformerは、生成中に増え続ける鍵値キャッシュ（KVキャッシュ）を、重要な過去トークンだけへ圧縮する方式である。著者らは、注意重みの約90%が過去トークンの一部に集中するという観察から、すべての履歴を保持する必要はないと考える。

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

- **2024-05 · [SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models](2024-2405.06219-skvq-sliding-window-key-and-value-cache-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/cat538/SKVQ) ・ リポジトリ内被引用：11  
  KVチャネルを量子化しやすい順へ並べ替え、外れ値をクリップし、直近KVだけ高精度で残すことで鍵2ビット・値1.5ビット級まで圧縮し、長文脈の容量・帯域律速を緩和する。

- **2024-10 · [LoRC: Low-Rank Compression for LLMs KV Cache with a Progressive Compression Strategy](2024-2410.03111-lorc-low-rank-compression-for-llms-kv-cache-with-a-progressive-compression-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  KVキャッシュから「どのトークンを捨てるか」を決めるのではなく、キー・値を作る射影行列そのものを低ランク化する。さらに、浅い層の近似誤差ほど後段で増幅されやすいことを利用し、浅層は保守的、深層は積極的に圧縮する。

- **2024-08 · [Eigen Attention: Attention in Low-Rank Space for KV Cache Compression](2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UtkarshSaxena1/EigenAttn) ・ リポジトリ内被引用：10  
  長い文脈を処理する言語モデルでは、生成時に過去のトークンの鍵と値を保存するKVキャッシュが、モデル重みと同程度かそれ以上のメモリを占めることがある。Eigen 注意機構は、保存するトークン数や一要素のビット幅を減らすのではなく、各トークンの鍵・値ベクトルの特徴次元を低ランク空間へ縮める。

- **2024-06 · [A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression](2024-2406.11430-l2-kv-compression.md)**  
  実装：[✓](https://github.com/alessiodevoto/l2compress) ・ リポジトリ内被引用：10  
  キーのL2ノルムと注意重みの逆相関を利用し、注意重みを計算せず重要KVを残す学習不要の圧縮法。FlashAttention互換のまま、長文検索では50〜90%のKV削減でも高精度を維持する。

- **2024-08 · [NACL: A General and Effective KV Cache Eviction Framework for LLM at Inference Time](2024-2408.03675-nacl-a-general-and-effective-kv-cache-eviction-framework-for-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/Research/tree/master/NLP/ACL2024-NACL) ・ リポジトリ内被引用：9  
  KV追い出しで「これまで注意スコアが大きかったトークンを残す」だけでは、注意が先頭・直近位置へ偏るため、長文中央の重要情報を捨てやすい。NACLは、質問などタスク固有の代理トークン（proxy トークン）が入力全体へ向けた注意から重要度を作る決定論的な保持と、その重要度分布からヘッド・層ごとに異なるトークンを確率的に残す保持を混ぜる。

- **2024-06 · [Attention Score is not All You Need for Token Importance Indicator in KV Cache Reduction: Value Also Matters](2024-2406.12335-attention-score-is-not-all-you-need-for-token-importance-indicator-in-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  注意スコアに値ベクトルのL1ノルムを組み込み、実際の注意出力寄与に近い重要度でKVトークンを削減する後付け型キャッシュ枝刈り。

- **2024-10 · [KVSharer: Efficient Inference via Layer-Wise Dissimilar KV Cache Sharing](2024-2410.18517-kvsharer-efficient-inference-via-layer-wise-dissimilar-kv-cache-sharing.md)**  
  実装：[✓](https://github.com/yangyifei729/KVSharer) ・ リポジトリ内被引用：7  
  層ごとの鍵・値キャッシュを独立に保存する代わりに、一部の後段層で前段層のキャッシュを再利用する。直感に反して「KV表現が大きく異なる層対」から共有を試し、元モデルの最終隠れ状態を保てる組だけを採用する。

- **2024-06 · [Effectively Compress KV Heads for LLM](2024-2406.07056-effectively-compress-kv-heads-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、既に多頭注意（Multi-Head 注意機構; MHA）として学習済みの大規模言語モデルを、鍵・値（Key/Value; KV）のヘッド数が少ない構成へ後変換する研究である。LLaMA2-7BのKVヘッドを32から16へ半減すると、単一A100 80GBで復号速度が8.05から13.41トークン/秒へ増えた。

- **2024-02 · [On the Efficacy of Eviction Policy for Key-Value Constrained Generative Language Model Inference](2024-2402.06262-on-the-efficacy-of-eviction-policy-for-key-value-constrained-generative-language-model-inference.md)**  
  実装：[✓](https://github.com/DRSY/EasyKV) ・ リポジトリ内被引用：7  
  RoCoはKV トークンの重要度を累積注意機構ではなく平均注意機構で測り、注意機構標準偏差で追い出し候補を動的に選び、固定window依存を減らしながらfull-キャッシュに近い生成品質を保つ。

- **2024-09 · [Inf-MLLM: Efficient Streaming Inference of Multimodal Large Language Models on a Single GPU](2024-2409.09086-inf-mllm-efficient-streaming-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  注意機構 saddlesを追跡して最新・重要トークンだけを固定KVへ残し、注意機構 biasで長期ストリーム中の注意移動にも追随するInf-MLLM。

- **2024-10 · [InfiniPot: Infinite Context Processing on Memory-Constrained LLMs](2024-2410.01518-infinipot-infinite-context-processing-on-memory-constrained-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  InfiniPotは、長い入力をすべて読み終わってから鍵・値キャッシュ（KVキャッシュ）を削減する方式ではなく、入力を読んでいる途中から固定容量内で何度も圧縮する長文脈処理の仕組みである。Mistral系の4K固定KV予算で最大100万トークンの検索実験も行ったが、「無限長でも全情報を損失なく保持する」ことを示したわけではない。

- **2024-04 · [SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget](2024-2404.04793-squeezeattention-2d-management-of-kv-cache-in-llm-inference-via-layer-wi.md)**  
  実装：[✓](https://github.com/hetailang/SqueezeAttention) ・ リポジトリ内被引用：5  
  SqueezeAttentionは、KVキャッシュ圧縮を「各層の中でどのトークンを残すか」という系列方向だけでなく、「総KV予算をどの注意機構層へ配るか」という層方向まで含む二次元問題として扱う。

- **2024-09 · [Small Language Models: Survey, Measurements, and Insights](2024-2409.15790-small-language-models-survey-measurements-and-insights.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/SLM_Survey) ・ リポジトリ内被引用：3  
  推論を高速化する新しいアルゴリズムを提案する論文ではない。同程度のパラメータ数でもQwen2-0.5Bの初回トークン時間はQwen1.5-0.5Bの1.46倍であり、Qwen1.5-0.5Bはパラメータが25.4%多いにもかかわらずJetson上では31.9%速い。

### 4年前（2022-11〜2023-10）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：274  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。

- **2023-06 · [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](2023-2306.14048-h2o.md)**  
  実装：[✓](https://github.com/FMInference/H2O) ・ リポジトリ内被引用：245  
  累積注意のヘビーヒッターと最新トークンを動的保持し、20%程度のKV予算で品質を維持しながらメモリ・スループットを改善する。

- **2023-10 · [Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs](2023-2310.01801-fastgen.md)**  
  実装：[✓](https://github.com/machilusZ/FastGen) ・ リポジトリ内被引用：109  
  FastGenは注意ヘッドごとの構造を一度だけ診断してKVキャッシュ保持方針を変え、追加学習なしでメモリ削減と長系列生成の高速化を両立する。

- **2023-05 · [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](2023-2305.17118-scissorhands.md)**  
  実装：✓ ・ リポジトリ内被引用：73  
  Scissorhandsは、過去の注意重みが大きかったトークンは将来の生成でも高い注意を受けやすいという「重要性の持続性仮説（Persistence of Importance Hypothesis）」を提案する。

### 7年前（2019-11〜2020-10）

- **2019-11 · [Fast Transformer Decoding: One Write-Head is All You Need](2019-1911.02150-multi-query-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：129  
  複数問い合わせ注意（Multi-Query 注意機構; MQA）は、問い合わせ側の8ヘッドを維持したまま、鍵と値だけを全ヘッドで1組へ共有する。長い履歴を毎生成ステップで読む増分復号のメモリ転送を減らし、TPUv2でのWMT英独翻訳のデコーダ測定を46から3.8マイクロ秒／出力トークンへ短縮した。
<!-- survey:auto:end -->
