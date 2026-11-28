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
## 自動生成の論文一覧（734本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/07-kv-cache-optimization-compression/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-07 · [Gemma 4 Technical Report](2026-2607.02770-gemma-4-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：54  
  密モデルと混合専門家モデルを含むGemma 4の技術報告。局所・大域注意の配置、キー・値キャッシュ共有、キーの値への再利用、部分回転位置符号化、量子化対応学習、複数トークン予測ドラフタ、12Bの符号化器不要構成を組み合わせ、推論時の重み容量・KV容量・復号費用をそれぞれ減らす。数値はモデル系列・量子化形式・文脈長ごとに区別して読む必要がある。

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：35  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2026-09 · [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](2026-2609.19969-deepseek-v4.1-flash-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  CED・CSA2の層間KV再利用・FP4 KV・SWA限定再実行を統合し、100万トークン対応552B MoEのグローバルKVを890 bytes/トークン、永続KVを前世代比約1/8へ圧縮する。

- **2026-02 · [Fast KV Compaction via Attention Matching](2026-2602.16284-fast-kv-compaction-via-attention-matching.md)**  
  実装：[✓](https://github.com/adamzweiger/compaction) ・ リポジトリ内被引用：24  
  長文脈のKVキャッシュを、将来の問い合わせで元の注意挙動を再現する短い鍵・値・バイアスへ置き換える。参照問い合わせの生成、鍵選択、非負最小二乗による注意質量合わせ、値の最小二乗推定を組み合わせる。

- **2026-01 · [Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction](2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md)**  
  実装：[✓](https://github.com/Janghyun1230/FastKVzip) ・ リポジトリ内被引用：19  
  長文脈の言語モデルは、生成のたびに過去の鍵・値（KV）を参照するため、文脈が長くなるとキャッシュがGPUメモリを圧迫する。重要でないKVを削除する方法は容量を減らせるが、何を消すかを決めるために過去の注意を再計算すると、圧縮器自体の費用が大きくなる。

- **2026-01 · [ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation](2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cac.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  従来の部分再計算法は、文書中の一部トークンだけを再計算して欠けた注意関係を補う。第二段階では層を横断して統合した重要度の上位トークンを選び、その位置のKVを全層で再計算する。原著はLlama-3.1-8B、Qwen2.5-14B、Qwen3-14Bを用い、文書トークンの20%だけを再計算する条件で、全再計算に近い平均精度を報告する。

- **2026-01 · [KVzap: Fast, Adaptive, and Faithful KV Cache Pruning](2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：18  
  KVzapは、大規模言語モデルの鍵・値キャッシュ（KVキャッシュ）をトークン位置方向に間引く際、重要度の計算そのものが推論を遅くしてしまう問題を解く方式である。Qwen3-8B、Llama-3.1-8B-Instruct、Qwen3-32Bにおける長文脈検索・理解・推論課題で、著者らはおおむね2〜4倍のKV圧縮と小さな精度低下を報告する。

- **2026-04 · [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](2026-2604.04921-triattention-efficient-long-reasoning-with-trigonometric-kv-compression.md)**  
  実装：[✓](https://github.com/WeianMao/triattention) ・ リポジトリ内被引用：15  
  長い推論列で「今のクエリに強く注意されるKV」だけを残すのではなく、回転位置埋め込み（Rotary Position Embedding; RoPE）前のクエリ・キーが固定中心の周囲へ集中する性質から、将来の距離ごとの注意傾向を三角関数として予測する。

- **2026-07 · [The Pitfalls of KV Cache Compression](2026-2510.00231-the-pitfalls-of-kv-cache-compression.md)**  
  実装：[✓](https://github.com/alexluchen/pitfalls-of-kv-cache-compression) ・ リポジトリ内被引用：14  
  KVキャッシュ圧縮の典型的な評価は、単一質問への回答、長文からの検索、コード生成といったタスクで「キャッシュを減らしても品質はほとんど落ちない」と結論しがちである。

- **2026-06 · [STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control](2026-2606.08382-star-kv-adaptive-low-rank-cache-compression.md)**  
  実装：[✓](https://github.com/PriyanshBhatnagar/STAR-KV) ・ リポジトリ内被引用：14  
  特異値の学習可能なしきい値で層・ヘッドごとのKV低ランク次元を自動配分し、鍵/値で異なる分解と低ランク対応混合精度量子化を組み合わせ、強い圧縮を実GPU高速化へつなげる。

- **2026-07 · [LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning](2026-lazyeviction.md)**  
  実装：[✓](https://github.com/Halo-949/LazyEviction) ・ リポジトリ内被引用：13  
  一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。

- **2026-05 · [OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization](2026-2605.17757-oscar-offline-spectral-covariance-aware-rotation-for-2-bit-kv-cache-quan.md)**  
  実装：[✓](https://github.com/FutureMLS-Lab/OSCAR) ・ リポジトリ内被引用：13  
  しかし2ビットには4段階の値しかなく、KV活性値の少数の大きな外れ値が量子化範囲を支配すると、通常値の区別が失われ、注意分布が崩れる。システム評価はNVIDIA H100上の著者実装であり、12GB級の民生GPUや標準配布版llama.cppで同じ結果が出ると示したものではない。

- **2026-05 · [Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management](2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  PBKVは、複数の言語モデルエージェントが同じ処理を分担する動的ワークフローで、次に使われる可能性が高いキー・値キャッシュ（KVキャッシュ）をGPUに残し、必要に応じてホストメモリから先読みする仕組みである。

- **2026-05 · [LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents](2026-2602.01053-lragent-multilora-agent-kv-sharing.md)**  
  実装：[✓](https://github.com/jeonhye/lragent) ・ リポジトリ内被引用：11  
  multi-LoRAエージェントのKVを共有基盤成分と低ランク役割成分へ分解し、後者を全次元化せず注意計算することで、長い共有履歴のKVメモリと再プリフィルを削減する。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：11  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

- **2026-02 · [SideQuest: Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning](2026-2602.22603-sidequest-model-driven-kv-cache-management-for-long-horizon-agentic-reas.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  調査エージェントが過去に開いた文書のうち不要になったものを、別の補助推論が意味的に判定し、主推論を止めずにKVキャッシュから削除する。

- **2026-02 · [Learning to Evict from Key-Value Cache](2026-2602.10238-learning-to-evict-from-key-value-cache.md)**  
  実装：[✓](https://github.com/apple/ml-learning-to-evict) ・ リポジトリ内被引用：10  
  キーと値だけから将来の有用さを予測する順位付けを、ヘッドごとの小さな方策として強化学習で学ぶ追い出し方式で、手作り指標を上回り128K文脈へも一般化した。

- **2025-12 · [MEPIC: Memory Efficient Position Independent Caching for LLM Serving](2025-2512.16822-mepic-position-independent-chunk-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  位置非依存KVをページ境界へ正規配置し、最初の1ブロックだけ再計算、RoPEを注意時に融合することで、同一チャンクのHBMページを要求間共有し、既存PICよりHBM重複と再計算を大幅に減らす。

- **2026-05 · [RateQuant: Optimal Mixed-Precision KV Cache Quantization via Rate-Distortion Theory](2026-2605.06675-ratequant-optimal-mixed-precision-kv-cache-quantization-via-rate-distort.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  各ヘッドの損失勾配に基づく重要度と、量子化器固有の指数型ビット数・歪み関係を校正し、逆水充填法と整数ビットの限界利得選択で配分を決める。Qwen3/Llama3の5モデルと3種類の量子化器で評価し、平均4ビット時のTurboQuantにおける量子化劣化回復率は5モデル平均75.7%。

- **2026-07 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2026-ojakv.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：8  
  重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。

- **2026-07 · [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](2026-2607.15456-looped-latent-attention-cross-loop-kv-compression-for-looped-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  ループ型Transformerは、同じTransformerブロックを何度も適用することで、モデルの深さに相当する反復計算を少ない重みで実現する。Ouro-1.4Bを用いた同一キャッシュ容量比較では、4倍圧縮のLLAはGSM8K厳密正解率0.800を記録し、教師の0.794とほぼ同等だった。

- **2026-07 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2026-2607.17715-c2kv-compressed-composable-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/s7a9/C2KV) ・ リポジトリ内被引用：8  
  文書ごとに位置非依存で直接連結できる圧縮KVを学習抽出し、非prefix再利用のプリフィル削減とKV保存・転送・デコード帯域削減を同時に狙う。

- **2026-06 · [RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention](2026-2606.06256-redknot-efficient-long-context-llm-serving-with-head-aware-kv-reuse-and-segpagedattention.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  従来のKV管理は全ヘッドを同じトークンブロックとして扱うが、RedKnotの測定では局所ヘッドが83.4〜96.8%、接頭辞変化に敏感な大域ヘッドは3.2〜16.6%に留まる。そこで大域ヘッドだけを広範囲に再計算し、局所ヘッドを再利用するElastic Sparsityと、ヘッド別のKVページを扱うSegPagedAttentionを組み合わせる。

- **2026-04 · [SAW-INT4: System-Aware 4-Bit KV-Cache Quantization for Real-World LLM Serving](2026-2604.19157-saw-int4-system-aware-4-bit-kv-cache-quantization-for-real-world-llm-ser.md)**  
  実装：[✓](https://github.com/togethercomputer/saw-int4) ・ リポジトリ内被引用：8  
  SAW-INT4は、モデルのキー・値（KV）キャッシュを4ビット整数へ縮めるとき、単に量子化誤差を小さくするのではなく、実際のサービングエンジンで高速に動くデータ配置と演算を先に制約として置く研究である。

- **2026-07 · [HYPIC: Accelerating Hybrid-Attention LLM Serving with Position-Independent Caching](2026-2607.01299-hypic-hybrid-attention-position-independent-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  線形注意区間の累積遷移演算子とゼロ始動状態を保存して位置非依存に合成し、完全注意層は境界窓だけ再計算、未保存区間は複数実体で並列処理することで、ハイブリッド注意言語モデルの初トークン待ち時間を平均3.25倍短縮する。

- **2026-04 · [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md)**  
  実装：[✓](https://github.com/yuzhenmao/IceCache) ・ リポジトリ内被引用：7  
  IceCacheは、意味的に近いKVを同じ物理ページへクラスタ化し、関連ページだけをCPUから一括転送して、長文のGPU KV容量とPCIeデータ量を減らす。

- **2026-08 · [Output-Aware Rotation for INT2 KV-Cache Quantization](2026-2608.02691-output-aware-rotation-int2-kv-cache.md)**  
  実装：[✓](https://github.com/daniel-eai/Output-Aware-INT2-KV-Cache-Quantization) ・ リポジトリ内被引用：6  
  OptRは、長文脈推論でKVキャッシュを2ビット整数へ量子化したとき、キーや値そのものの再構成誤差が小さくても、注意重みと出力射影を通過した後のモデル内部表現には大きな誤差が残り得る問題を扱う。

- **2026-06 · [Value-Aware Stochastic KV Cache Eviction for Reasoning Models](2026-2606.03928-value-aware-stochastic-kv-cache-eviction-for-reasoning-models.md)**  
  実装：[✓](https://github.com/terarachang/VaSE) ・ リポジトリ内被引用：6  
  疎注意（Sparse 注意機構）には、キャッシュ全体を保持して計算対象だけを選ぶ方式と、重要度が低い過去トークンの鍵・値を実際に破棄する方式がある。Qwen3-4BとQwen3-14Bの数学・科学課題では約4倍のKV容量圧縮でも、既存の削除方式より高い平均正答率を得た。

- **2026-06 · [MiniPIC: Flexible Position-Independent Caching in <100LOC](2026-2606.13126-minipic-flexible-position-independent-caching-in-100loc.md)**  
  実装：[✓](https://github.com/IBM/vllm) ・ リポジトリ内被引用：6  
  例えばシステム指示や文書の並び順が異なる二つの要求は、同じ文書の事前充填を繰り返すことになる。H100単体・2Wikiの12,576サンプルでは、文書の事前充填と最終要求を交互に投入する方式により48.01サンプル/秒を達成し、通常vLLMの32.21サンプル/秒に対して49%増加した。

- **2026-04 · [Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs](2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-devic.md)**  
  実装：[✓](https://github.com/SayedPedramHaeri/Dont-Waste-Bits) ・ リポジトリ内被引用：6  
  本研究は、端末上で動かす小型言語モデルのキー・値キャッシュ（KVキャッシュ）を、トークンごとの重要度に応じて異なるビット幅で保存する適応量子化方式を提案する。SmolLM-360MとHellaSwagの実機評価では、固定4ビットの正答率33.6%、遅延2.93に対して、提案方式は41.2%、2.41だった。

- **2026-03 · [The Residual Stream Is All You Need: On the Redundancy of the KV Cache in Transformer Inference](2026-2603.19664-the-residual-stream-is-all-you-need-on-the-redundancy-of-the-kv-cache-in.md)**  
  実装：[✓](https://github.com/Kaleemullahqasim/KV-Direct) ・ リポジトリ内被引用：6  
  著者らはこの事実を残差の十分性として整理し、古いKVを破棄して残差ベクトルのチェックポイントを保持するKV-Directを提案した。原著の全系列を毎回再計算する比較では、30トークン生成が標準キャッシュ方式より1.7～3.8倍遅かった。

- **2026-02 · [You Need an Encoder for Native Position-Independent Caching](2026-2602.01519-you-need-an-encoder-for-native-position-independent-caching.md)**  
  実装：[✓](https://github.com/shijuzhao/Comb) ・ リポジトリ内被引用：6  
  凍結したデコーダ専用LLMへPIC専用エンコーダを追加し、任意順序の文書KV再利用を高精度化しつつTTFTを51〜94%削減、KV容量も約75%以上削減するCOMBを提案。

- **2026-08 · [Spend Bits Where Queries Look: KV Cache Vector Quantization with Attention-Preserving Transforms](2026-2608.04074-spend-bits-where-queries-look-kv-cache-vector-quantization-with-attentio.md)**  
  実装：[✓](https://github.com/Amir-zsh/nova-kv) ・ リポジトリ内被引用：5  
  文脈長と同時実行数に比例してキャッシュが増えるため、読み出し帯域が復号速度と同時収容数の制約になる。NOVA-KVは、このキャッシュを単に数値として再現するのではなく、照会と鍵の内積、および注意重みと値の積を保つことを量子化の目的に置く。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：5  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-07 · [SemPIC: Learning Semantic Position-Independent KV Caches](2026-2607.28069-sempic-learning-semantic-position-independent-kv-caches.md)**  
  実装：[✓](https://github.com/jn12-29/SemPIC) ・ リポジトリ内被引用：5  
  SemPICは、検索拡張生成（Retrieval-Augmented Generation、RAG）やエージェントの長い文書文脈を、問い合わせや文書順序が変わっても再利用するための位置非依存キャッシュ（Position-Independent Caching、PIC）方式である。

- **2026-06 · [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  AsymCacheは、非連続KV区間を一つの注意カーネルで統合し、再利用確率と再計算遅延で追い出し、負荷適応チャンク化で長文サービングのGPU計算と管理費を減らす。

- **2026-06 · [MomentKV: Closing the Directional Gap in KV Cache Eviction for Long-Context Inference](2026-2606.01563-momentkv-closing-the-directional-gap-in-kv-cache-eviction-for-long-conte.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  捨てたトークンの要約統計を保持し、その統計で追い出し先を選び、捨てた側の注意出力を近似で戻すことで、方向のずれによる誤差を抑えて全てのキャッシュ予算で先行方式を上回った。

- **2026-06 · [Kamera: Unified Position-Invariant Multimodal KV Cache for Training-Free Reuse](2026-2606.23581-kamera-unified-position-invariant-multimodal-kv-cache-for-training-free-.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Kameraは、画像・動画・画面の断片を繰り返し参照する視覚言語モデルのエージェントで、以前に計算した鍵・値キャッシュ（KVキャッシュ）を異なる文脈位置へ移して再利用するための方式である。

- **2026-05 · [Dynamic-dLLM: Dynamic Cache-Budget and Adaptive Parallel Decoding for Training-Free Acceleration of Diffusion LLM](2026-2606.26120-dynamic-dllm-cache-budget-parallel-decoding.md)**  
  実装：[✓](https://github.com/TianyiWu233/DYNAMIC-DLLM) ・ リポジトリ内被引用：5  
  層別キャッシュ更新量とトークン別確定基準を動的化し、追加学習なしで最大4.48倍の拡散型LLM推論高速化を実現する。

- **2026-04 · [When Hidden States Drift: Can KV Caches Rescue Long-Range Speculative Decoding?](2026-2604.26412-when-hidden-states-drift-can-kv-caches-rescue-long-range-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  投機的復号（投機的復号）は、小さなドラフトモデルが先の複数トークンを提案し、大きな対象モデルが一括で検証することで逐次生成の遅延を減らす。Qwen3-8Bでの実験では、KV再利用は後方の投機ステップの受理率を改善し、混成方式は小規模な逐次受理評価で平均受理トークン数を2.37から2.54へ増やした。

- **2026-04 · [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  SPINは、異なる疎注意方式の選択単位を共通ページへ写し、要求ごとのKV予算とGPU局所性キャッシュを調整して、階層メモリの転送とHBM圧力を減らす。

- **2026-03 · [LookaheadKV: Fast and Accurate KV Cache Eviction by Glimpsing into the Future without Generation](2026-2603.10899-lookaheadkv-fast-and-accurate-kv-cache-eviction-by-glimpsing-into-the-fu.md)**  
  実装：[✓](https://github.com/SamsungLabs/LookaheadKV) ・ リポジトリ内被引用：5  
  先読みトークンと専用LoRAで将来応答の注意パターンを生成なしに予測してKVキャッシュを追い出す方式で、下書き型より最大14.5倍安い追い出し費用と低予算での品質維持を両立した。

- **2026-03 · [LongFlow: Efficient KV Cache Compression for Reasoning Models](2026-2603.11504-longflow-efficient-kv-cache-compression-for-reasoning-models.md)**  
  実装：[✓](https://github.com/yisunlp/LongFLow) ・ リポジトリ内被引用：5  
  LongFlowは、長い推論過程を生成するモデルの鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）を、生成中に継続的に圧縮する方式である。

- **2026-03 · [Judge Q: Trainable Queries for Optimized Information Retention in KV Cache Eviction](2026-2509.10798-judge-q-trainable-queries-for-optimized-information-retention-in-kv-cach.md)**  
  実装：[✓](https://github.com/Mambaaaaaaaaa/Judge-Q) ・ リポジトリ内被引用：5  
  既存の注意機構重みや本体Transformerを再学習せず、削除位置の選択を改善する設計である。論文の主評価は同じKV保持数における正解率・タスクスコアであり、追加soft トークンによるプリフィル計算を含めた実機のTTFT、TPOT、メモリピークやスループットの改善を実証したものではない。

- **2026-02 · [IVC-Prune: Revealing the Implicit Visual Coordinates in LVLMs for Vision Token Pruning](2026-2602.03060-ivc-prune-revealing-the-implicit-visual-coordinates-in-lvlms-for-vision-.md)**  
  実装：[✓](https://github.com/FireRedTeam/IVC-Prune) ・ リポジトリ内被引用：5  
  回転位置埋め込みが生む座標役の視覚トークンと意味的に重要な前景トークンを両方残す学習不要の枝刈りで、視覚トークンを約半分にしながら空間推論の精度をほぼ落とさない方式である。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：[✓](https://github.com/omnia-postech/OrbitFlow) ・ リポジトリ内被引用：5  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

- **2026-01 · [Don't be so Stief! Learning KV Cache low-rank approximation over the Stiefel manifold](2026-2601.21686-don-t-be-so-stief-learning-kv-cache-low-rank-approximation-over-the-stie.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  StiefAttentionは、学習済みの大規模言語モデルを再事前学習せずに、推論時の鍵・値（KV）キャッシュを低ランク化する手法である。

- **2025-12 · [Accurate KV Cache Eviction via Anchor Direction Projection for Efficient LLM Inference](2025-fc5da84b7582-accurate-kv-cache-eviction-via-anchor-direction-projection-for-efficient.md)**  
  実装：[✓](https://github.com/MIRALab-USTC/LLM-AnDPro) ・ リポジトリ内被引用：5  
  従来のH2OやSnapKVは、注意重みの大きいトークンほど重要とみなす。だが注意出力は、注意重みと値ベクトルの積を足し合わせたベクトル和である。重みが大きくても値ベクトルが出力方向に寄与しなければ、そのトークンを残す意義は小さい。逆に重みが比較的小さくても、出力方向へ強い成分を持つ値は重要になりうる。

- **2026-10 · [ResidualQuant: KV Cache Quantization for Looped Transformers with 2-Bit Residuals](2026-2610.10381-residualquant-kv-cache-quantization-for-looped-transformers-with-2-bit-r.md)**  
  実装：[✓](https://github.com/heejunkim00/ResidualQuant) ・ リポジトリ内被引用：4  
  最終ループのKVを参照に残し他ループの差分だけを2ビットで保存する残差量子化で、KV保存量を80.7パーセント減らしながらBF16に近い精度を保った。

- **2026-09 · [When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse](2026-2609.28870-when-fancy-eviction-fails-rethinking-cache-replacement-for-llm-prefix-re.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  接頭辞キャッシュ（prefix キャッシュ）は長文脈の事前充填（プリフィル）費用を下げる重要な機構だが、GPUの高帯域幅メモリ（HBM）には容量制限があるため、どのブロックを保持し、どれを退避するかを決める必要がある。

- **2026-09 · [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md)**  
  実装：[✓](https://github.com/LiuTaowen-Tony/agentkv) ・ リポジトリ内被引用：4  
  思考・行動・ツール応答など段階別の問い合わせ履歴でKV重要度を評価し、エージェントの段階遷移で必要になる古い状態を残しつつ、物理ページ圧縮で最大1.80倍の出力スループットを得る。

- **2026-08 · [Practical Online KV Cache Compaction for LLM Agents: An Empirical Study](2026-2608.00902-practical-online-kv-cache-compaction-for-llm-agents-an-empirical-study.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  静的な長文質問では、最終質問を見た後で不要トークンを選別できるが、エージェントがまだ次に何を調べるか分からない時点で圧縮すると、後で必要になる検索結果を失い得る。大規模モデルQwen3.5-27BのBrowseComp-Plusでは、無圧縮の正答率52.50%に対し、1ターン遅延のTEが52.00%、AMが51.00%だった。

- **2026-08 · [KV Cache Compression Through the Lens of Transform Coding](2026-2608.14191-kv-cache-compression-through-the-lens-of-transform-coding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  保存精度を下げれば容量を削減できるが、鍵と値の数値的な再構成誤差が小さいことと、注意機構の出力が変化しないことは同義ではない。約5.82倍の鍵値キャッシュ圧縮時に、原著の標準誤差による判定では、両モデルの主要18評価セルすべてで非圧縮基準との統計的な区別がつかないと報告する。

- **2026-08 · [DASC: Decay-Aware State Compression for Hybrid Linear-Attention Serving](2026-2608.30386-dasc-decay-aware-state-compression-for-hybrid-linear-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重み由来の保持地平でKDA/GDN再帰状態を選別・ragged保存し、TP均衡化によりKimi-KDAで2.63倍のcheckpoint容量とTTFT 42.6%削減を実現する。

- **2026-07 · [KV Cache Translation across Heterogeneous Large Language Models](2026-2607.28979-kv-cache-translation-across-heterogeneous-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  従来の単一射影や共有潜在空間を介す方式と異なり、MoTは複数の変換器を用意し、トークンごとに適切な変換器を上位K個選択して出力を混合する。Llama-3.2 3B、Gemma-3 4B、Qwen-3 4B間の異種変換を評価し、閉集合質問応答の平均正解率57.6%、抽出型質問応答の平均F1 0.42を報告する。

- **2026-06 · [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](2026-2606.17107-models-take-notes-at-prefill-kv-cache-can-be-editable-and-composable.md)**  
  実装：[✓](https://github.com/19PINE-AI/programmable-kv) ・ リポジトリ内被引用：4  
  プリフィル済みKVキャッシュを結論メモとして捉え、追記訂正による編集とRoPE再配置による部品合成で再プリフィルを回避する。

- **2026-05 · [MuKV: Multi-Grained KV Cache Compression for Long Streaming Video Question-Answering](2026-2605.22269-mukv-multi-grained-kv-cache-compression-for-long-streaming-video-questio.md)**  
  実装：[✓](https://github.com/IMBALDY/MuKV) ・ リポジトリ内被引用：4  
  動画を区間・フレーム・パッチの3粒度のKVキャッシュで保持し、自己注意と周波数の二信号で圧縮して半階層検索する方式で、保存量を増やさずにストリーミング動画質問応答の精度を代表方式から数ポイント引き上げた。

- **2026-05 · [AgentKVShift: Efficient KV Cache Reuse for Agentic Memory Systems](2026-2607.21604-agentkvshift-agentic-memory-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  構造化エージェントメモリの一部トークンだけを再計算し、そこから推定したメモリ単位のKV残差を未再計算トークン全体へ加えて、低い再計算率で品質を回復する。

- **2026-04 · [Swift-SVD: Theoretical Optimality Meets Practical Efficiency in Low-Rank LLM Compression](2026-2604.01609-swift-svd-theoretical-optimality-meets-practical-efficiency-in-low-rank-.md)**  
  実装：[✓](https://github.com/hiahei/Swift-SVD) ・ リポジトリ内被引用：4  
  出力活性値の共分散を逐次集約して固有値分解を1回だけ行い、活性値を考慮した理論最適な低ランク圧縮を高速かつ数値安定に実現し、再構成損失と層重要度を組み合わせた動的ランク配分まで備えた学習不要の圧縮手法。

- **2026-04 · [PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference](2026-2604.24971-polykv-shared-asymmetrically-compressed-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  共通文書のKVキャッシュを一度だけ非対称量子化して共有プール化し、複数エージェントへ注入して重複メモリを削減する。

- **2026-04 · [HybridKV: Hybrid KV Cache Compression for Efficient Multimodal Large Language Model Inference](2026-2604.05887-hybridkv-hybrid-kv-cache-compression-for-efficient-multimodal-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  注意ヘッドを静的型と動的型へ分類し、枝刈りと検索を使い分ける混合型KVキャッシュ圧縮で、メモリを最大7.9分の1にしながら性能をほぼ維持した。

- **2026-03 · [EchoKV: Efficient KV Cache Compression via Similarity-Based Reconstruction](2026-2603.22910-echokv-efficient-kv-cache-compression-via-similarity-based-reconstructio.md)**  
  実装：[✓](https://github.com/noforit/EchoKV) ・ リポジトリ内被引用：4  
  圧縮方式の一つである低ランク分解は、重み行列を変形して保存すべきKVの次元を減らすが、変形後のモデルを短文・長文の負荷に応じて元の通常推論へ戻すことが難しい。これらは圧縮率50%で精度が常に完全維持されるという結果ではなく、課題ごとの悪化もある。

- **2025-12 · [Reconstructing KV Caches with Cross-layer Fusion For Enhanced Transformers](2025-2512.03870-reconstructing-kv-caches-with-cross-layer-fusion-for-enhanced-transforme.md)**  
  実装：[✓](https://github.com/LivingFutureLab/FusedKV) ・ リポジトリ内被引用：4  
  長い系列と同時要求の増加に伴い、層数に比例するKVキャッシュ容量と読み出しがサービングの制約となる。著者は、上位層のキーと値が異なる深さの情報を必要とすることが原因の一つと考え、上位層のキー・値を下位層から非対称に再構成するFusedKVを設計した。

- **2025-12 · [Efficient Low Rank Attention for Long-Context Inference in Large Language Models](2025-2510.23649-efficient-low-rank-attention-for-long-context-inference-in-large-languag.md)**  
  実装：[✓](https://github.com/tenghuilee/LRQK) ・ リポジトリ内被引用：4  
  Q・Kの共同低ランク索引で重要KVを選び、CPU上の完全精度KVから欠損分だけGPUへ取得して長文脈の容量制約を緩和する。

- **2026-10 · [Hybrid Latent Attention for Looped Language Models](2026-2610.07940-hybrid-latent-attention-for-looped-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  古いトークンを全ループ共有の潜在として保存し再構成せず直接読み、直近分だけ正確なKVを残す注意機構で、キャッシュを10.7倍圧縮し16K文脈の復号を最大7.4倍高速化した。

- **2026-10 · [Cache Engineering for Agents](2026-2610.28577-cache-engineering-for-agents.md)**  
  実装：[✓](https://github.com/thu-nics/AKV) ・ リポジトリ内被引用：3  
  履歴テキストを書き換えずにKVキャッシュ自体を削除・再配置して有効文脈を制御する方式と、その履歴依存性に対応する提供基盤で、要約方式より成績を上げながら費用を27.7パーセント削減した。

- **2026-09 · [Where Activation Sparsity and KV-Cache Sparsity Cross in LLM Decoding](2026-2609.33889-where-activation-sparsity-and-kv-cache-sparsity-cross-in-llm-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/ByteCross) ・ リポジトリ内被引用：3  
  LLMの一トークン復号では、線形層の重みをメモリから読み込む費用と、過去文脈のKVキャッシュを読み込む費用が競合する。前者はモデルの構造でほぼ固定され、後者は文脈長に比例して増える。活性化疎化は現在の入力で活性化しているニューロンに対応する射影重みだけを読み込み、KV疎化は注意で参照する過去トークンを選んでキャッシュ読出しを減らす。

- **2026-09 · [KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints](2026-2609.10266-kvsharearena-cross-context-checkpoint-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  KVShareArenaは、文脈・チェックポイントをまたぐKV再利用で位置ずれと情報源間相互作用の欠落を分離測定し、補正・再計算・圧縮の品質と費用を共通基準で比較する。

- **2026-09 · [H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache](2026-2609.24197-h-spec-parallel-speculative-decoding-without-a-drafter-side-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  H-Specは、投機的復号（投機的復号）の軽量な候補生成器であるドラフターが、対象モデルの隠れ状態を各入力位置で別の鍵・値キャッシュ（KV キャッシュ）へ射影して保存する方式に対し、その追加キャッシュを廃止するための混成Mamba・注意ドラフターである。

- **2026-08 · [ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents](2608.19662.md)**  
  実装：[✓](https://github.com/EIT-NLP/ReCache) ・ リポジトリ内被引用：3  
  ツール／スキル定義を組合せ非依存のKVブロックとして再利用し、重要な層・KVヘッド群と呼出し必須フィールドだけを残して、エージェント推論のプリフィルとKVメモリを削減する。

- **2026-07 · [Set Diffusion: Interpolating Token Orderings Between Autoregression and Diffusion for Fast and Flexible Decoding](2026-2607.01775-set-diffusion-interpolating-token-orderings-between-autoregression-and-d.md)**  
  実装：[✓](https://github.com/kuleshov-group/setdlms) ・ リポジトリ内被引用：3  
  マスクを復元する拡散モデルは多数の位置を並列に予測できるが、双方向の注意と固定長の生成領域を前提とするため、復号中に一部だけを確定して計算結果を長期再利用する設計が難しい。

- **2026-07 · [ResKV: Reconstructing Omitted Attention Contributions for Fixed-Budget KV Cache Compression](2026-2607.29591-reskv-reconstructing-omitted-attention-contributions-for-fixed-budget-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  重要トークンへ削除側の情報を混ぜ込む方式もあるが、厳密に保持したい鍵・値自体が改変され、特定箇所の検索に悪影響を与える場合がある。

- **2026-07 · [[AAFLOW+] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows](2026-2607.10987-aaflow-stateful-operator-abstraction-with-zero-copy-distributed-kv-cache.md)**  
  実装：[✓](https://github.com/arupcsedu/AAFLOW) ・ リポジトリ内被引用：3  
  複数エージェントで検索、計画、推論、回答の統合を進めると、異なるエージェントが同じ文書や会話履歴を読み直す。主要な定量報告では、Mistral-7Bの平均初回トークン時間（TTFT）が0.041秒で、テキストを再計算するAAFLOW-textの2.057秒に対し50.2倍の差がある。

- **2026-06 · [ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning Models](2026-2606.11164-reasonalloc-hierarchical-decoding-time-kv-cache-budget-allocation-for-re.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ReasonAllocは、長い思考過程を逐次生成する推論モデルにおいて、復号中に増え続ける鍵・値キャッシュ（KVキャッシュ）の保持予算をどの層・どの注意頭へ割り当てるかを最適化する手法である。まずモデルごとに少数の入力を使って、各層が注意重みの93%を保持するのに必要な履歴トークン数を測り、層別の予算比率を事前校正する。

- **2026-06 · [RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference](2026-2606.31519-rabitqcache.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  長文脈大規模言語モデルでは、復号の各ステップで巨大なKVキャッシュから注意計算用データを読むことがメモリ帯域のボトルネックになる。RaBitQCacheはランダム回転と二値量子化で小型索引を作り、不偏な注意スコア推定から累積確率に応じて必要量を変える上位確率検索（Top-p）を行う。

- **2026-06 · [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：3  
  CompressKVは、意味的証拠を検索する注意ヘッドだけでKVトークンを選び、層ごとの追い出し感度で容量を配分して、同じKV予算で長文品質を保つ。

- **2026-05 · [TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Agentic Inference Tasks](2026-2605.17170-triaxialkv-toward-extreme-low-precision-kv-cache-quantization-for-agenti.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  長い対話履歴を保持するエージェント型大規模言語モデルでは、システム指示、ツール定義、過去の会話、画像、ツール実行結果が同じ鍵・値キャッシュ（KVキャッシュ）に混在する。

- **2026-05 · [ReST-KV: Robust KV Cache Eviction with Layer-wise Output Reconstruction and Spatial-Temporal Smoothing](2026-2605.08840-rest-kv-robust-kv-cache-eviction-with-layer-wise-output-reconstruction-a.md)**  
  実装：[✓](https://github.com/an-yongqi/rest-kv) ・ リポジトリ内被引用：3  
  自己回帰生成では、過去トークンのキーとバリューを各層・各ヘッドに保存する。入力文脈が伸びるとキャッシュの占有量と復号時の読み出しが増え、長文脈の同時提供でメモリ容量・帯域の制約が強くなる。従来のH2OやSnapKVなどは注意重みの累積・観測窓内の集約を重視するが、トークンを削除するとソフトマックスの分母が変わり、残されたトークンへの注意が再分配される。

- **2026-05 · [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  KARAは、新しく増えたKV区間だけを一度ずつ圧縮し、重要トークンを可変長チャンクへ広げ、周期発動で再圧縮費を抑えて長い推論の同時実行数を保つ。

- **2026-04 · [WSVD: Weighted Low-Rank Approximation for Fast and Efficient Execution of Low-Precision Vision-Language Models](2026-2604.02570-wsvd-weighted-low-rank-approximation-for-fast-and-efficient-execution-of.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/WSVD) ・ リポジトリ内被引用：3  
  SVDを注意ヘッドごとに適用し再構成をフラッシュデコードへ融合することで、視覚言語モデルのデコードを1.8倍超高速化し、量子化込みでも精度低下を約1ポイントに抑えた。

- **2026-04 · [The Illusion of Equivalence: Systematic FP16 Divergence in KV-Cached Autoregressive Inference](2026-2604.15409-the-illusion-of-equivalence-systematic-fp16-divergence-in-kv-cached-auto.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  数学的には、毎回すべての接頭辞を再計算する経路と同じ注意計算を実行するはずである。新しい高速化カーネルやKV圧縮方式を提案する研究ではない。さらに32ビット浮動小数点（FP32）へ切り替えると、著者らの別の対照実験ではトークン反転が0%となり、出力分布差が大幅に減った。

- **2026-04 · [Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing](2026-2604.22782-stochastic-kv-routing-enabling-adaptive-depth-wise-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  既存の削減手法の多くは「どの時刻のトークンを捨てるか」に着目するが、本研究は「どの層が独自のKVを持つ必要があるか」を問い直す。

- **2026-04 · [LKV: End-to-End Learning of Head-wise Budgets and Token Selection for LLM KV Cache Eviction](2026-2605.06676-lkv-end-to-end-learning-of-head-wise-budgets-and-token-selection-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  KVキャッシュの残し方を「どのヘッドへ何トークン分を割り当てるか」と「そのヘッド内でどのトークンを残すか」に分解し、両方をタスクの品質から学習する。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

- **2026-03 · [KVSculpt: KV Cache Compression as Distillation](2026-2603.27819-kvsculpt-kv-cache-compression-as-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  従来の追い出し方式は重要な元トークン位置を選び、結合方式も元の位置・ベクトルに由来する値を作る。

- **2026-02 · [InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache for Large Language Models](2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  InnerQは、長文脈デコードで増え続けるキー・バリューキャッシュ（KV キャッシュ）を低ビット化する際、量子化誤差だけでなく「量子化済みKVをGPU上で復号してベクトル行列積（GEMV）へ渡すときのスケール/ゼロ点読み出し」を主要ボトルネックとして設計する調整不要のKV量子化方式である。

- **2026-01 · [SONIC: Segmented Optimized Nexus for Information Compression in Key-Value Caching](2026-2601.21927-sonic-segmented-optimized-nexus-for-information-compression-in-key-value.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多ターンの対話では、過去のユーザー発話とモデル応答が蓄積するたびに鍵値キャッシュが増え、メモリ使用量と新しいトークンの注意計算が重くなる。SONICは対話のターン境界を利用し、過去の各メッセージを少数の学習可能なNexusトークンへ集約する方式である。

- **2026-11 · [BitDecoding-FP4: Native FP4 KV Cache Decoding via Algorithm-System Co-Design](2026-2611.09825-bitdecoding-fp4-native-fp4-kv-cache-decoding-via-algorithm-system-co-des.md)**  
  実装：[✓](https://github.com/OpenBitSys/BitDecoding-FP4) ・ リポジトリ内被引用：2  
  クエリの二重残差表現、確率のアンダーフロー対策、キーの外れ値対策と転置ソフトマックスを組み合わせ、FP4テンソルコアで直接デコードしながらBF16並みの精度と2.4倍から3.0倍のサービングスループットを得るFP4 KVキャッシュ方式。

- **2026-10 · [Understanding KV Residency in Production-Scale Agentic LLM Workloads](2026-2610.22863-understanding-kv-residency-in-production-scale-agentic-llm-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  1億2100万回超の本番呼出しを分析し、エージェントのKV保持がセッション規模と配置の両面で律速すること、休止上限と低精度複製の保持が再計算を大きく減らすことを示した。

- **2026-10 · [The Surprising Effectiveness of Shared Memory in Looped Transformers](2026-2610.02383-the-surprising-effectiveness-of-shared-memory-in-looped-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ループTransformerのKVキャッシュを最初の再帰だけが書き、後続は共有キャッシュと短い自前ウィンドウを読むよう事前学習すると、コンテキストメモリを最大で約5分の1にしながらパープレキシティと下流精度がむしろ改善することを示した研究。

- **2026-10 · [RaReCache: Bridging the Gap in Cross-Model KV Cache Reuse via Rank disagreement-based Selective Recomputation](2026-2610.11358-rarecache-bridging-the-gap-in-cross-model-kv-cache-reuse-via-rank-disagr.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  小さいモデルのKVキャッシュを線形写像で大きいモデルへ移し、較正データの部分空間の外側へ漏れる量が大きい位置だけを再計算させることで、23倍の規模差でも3割の再計算で本来の正解率の95から99パーセントを保つ方式である。

- **2026-10 · [Lachesis: Lifetime-Aware KV Cache Placement for Agent Serving across HBM and High-Bandwidth Flash](2026-2610.08378-lachesis-lifetime-aware-kv-cache-placement-for-agent-serving-across-hbm-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  文脈区間の寿命を書込み前に判定し、短命な区間を高速メモリ、長命な区間をフラッシュへ配置することで、フラッシュの書換え寿命を最大3.13倍に延ばした配置層の提案。

- **2026-10 · [HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs](2026-2610.23503-hbfsim-a-simulator-for-exploring-hbf-in-memory-hierarchies-for-llms.md)**  
  実装：[✓](https://github.com/FlashLabAE/HBFSim) ・ リポジトリ内被引用：2  
  実機のない高帯域フラッシュを含むメモリ階層を、較正済みの提供スケジューラとフラッシュ内部モデルを閉ループでつないで模擬する器を作り、配置はKV優先、変換は並列性を保つ範囲マッピング、寿命はKV書き込み量で決まるという設計指針を引き出した。

- **2026-10 · [Behavior-Preserving KV Cache Compression](2026-2610.06479-behavior-preserving-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  キャッシュ削除の採点を注意量などの代理信号から、全キャッシュモデルの次トークン分布とのずれへ置き換え、圧縮前の統計だけでそのずれを推定することで、除去率90パーセントの長文脈検索でも注意型の41点台に対し61から68点を保った。

- **2026-09 · [The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems](2026-2609.27746-kv-cache-working-set-online-capacity-planning.md)**  
  実装：[✓](https://github.com/llc-kc/kv_cache_capacity_estimator) ・ リポジトリ内被引用：2  
  LRUのスタック距離をFenwick木で解析し、接頭辞KVキャッシュの目標ヒット率に必要な容量を1回の要求トレースからオンライン推定する。

- **2026-09 · [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/Random-Attention) ・ リポジトリ内被引用：2  
  Random 注意機構は、入力文を必ず保持し、生成した推論過程のKVだけをヘッド別に無作為保持することで、選択器の採点計算を省き、同じ容量で強い選択法に近い正答率と高い提供スループットを得る。

- **2026-09 · [Multi-Turn LLM Conversations under the Least-Recently-Used Policy: Mean-Field Asymptotics and Hit Ratio Approximation](2026-2609.02027-multi-turn-lru-hit-ratio-mean-field.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  多ターン会話の最終使用時刻型鍵値キャッシュを確率モデル化し、メモリ容量と会話到着率からヒット率を推定する平均場式を導出。Qwen3-8B実機評価で到着率0.5〜2.0毎秒の条件において絶対誤差0.015未満・相対誤差7%未満を確認する。

- **2026-09 · [MpFA: Hardware-Efficient Train-Free QK4V8 FlashAttention Kernels on Blackwell GPUs](2026-2609.33135-mpfa-hardware-efficient-train-free-qk4v8-flashattention-kernels-on-black.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  BlackwellのFP4行列演算をそのまま注意へ使うとsoftmax側の処理が律速になることを突き止め、QK積だけをFP4化し、精度補償を行列演算へ逃がすことで、長文脈推論の注意を学習不要で高速化したカーネル。

- **2026-09 · [EchoPress: Query-Agnostic KV Cache Pruning via Virtual Context Reconstruction](2026-2610.00412-echopress-query-agnostic-kv-cache-pruning-via-virtual-context-reconstruc.md)**  
  実装：[✓](https://github.com/ljwljwljwljw/kvpress/tree/echo-press) ・ リポジトリ内被引用：2  
  複数の質問で同じ長文を再利用したい場合、質問を受け取ってから重要なトークンを決める方法では、圧縮済みキャッシュを別の質問へ使い回すことが難しい。著者の実測では、KVzipの圧縮追加時間が対応する通常の入力処理時間の約2.1〜2.2倍になる。

- **2026-09 · [ARC-KV: Amortizing Anchor Search for Reconstruction-Based KV Cache Compaction](2026-2609.36835-arc-kv-amortizing-anchor-search-for-reconstruction-based-kv-cache-compac.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  通常の削除型圧縮では、残すトークンを選んで元の鍵と値をそのまま保存する。Llama-3.1-8B-InstructとQuALITYの評価では、KV保持率10%でAMの正解率0.6409に対してARC-KVは0.6474、圧縮時間は959.8秒から37.3秒へ短縮し、25.73倍となった。

- **2026-08 · [Trust the Mass: Forced Weights in KV-Cache Eviction](2026-2608.25230-trust-the-mass-forced-weights-in-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  5系列・計168,192注意行の検査で、候補プール内の最良集合へ切り替えて埋められる差は、残存誤差の中央値で約2〜5%であった。

- **2026-08 · [TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning](2026-2608.03276-taskpress-query-agnostic-kv-cache-compression-via-task-guided-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  一方、再構築を使うKVzip型の方式は複数質問への適応を狙えるが、文脈をもう一度長く処理する費用が生じる。LLaMA-3.1-8B-InstructのLongBench平均では、int4 KVを前提に75%削除時、TaskPress 43.08、KVzip 38.24、SnapKV 39.37である（表1）。

- **2026-08 · [RestoreKV: Recovering Full-Cache Behavior Under Aggressive Query-Agnostic KV Cache Eviction](2026-2608.01247-restorekv-recovering-full-cache-behavior-under-aggressive-query-agnostic.md)**  
  実装：[✓](https://github.com/cvsp-lab/RestoreKV) ・ リポジトリ内被引用：2  
  RestoreKVは、将来の質問がまだ分からない段階で長文脈の鍵値キャッシュ（Key–Value キャッシュ、KVキャッシュ）を圧縮する推論方式に、少数の学習済み補完状態を追加する手法である。保持割合が十分なら有効だが、容量を5%程度まで削ると、選別器がどれほど優れていても消失した情報を後の質問から取り戻せない。

- **2026-08 · [Fewer Tokens, Smaller Cache: Reward-Coordinated Efficient Reasoning](2026-2608.04771-fewer-tokens-smaller-cache-reward-coordinated-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ReCo（Reward-Coordinated Compression）は、長い思考連鎖を生成する推論モデルの実行費用を、KVキャッシュの削減と、これから生成する思考トークンの削減を同時に制御する方式である。

- **2026-08 · [Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression](2026-2608.01631-does-accuracy-equal-evidence-reasoning-faithfulness-under-kv-cache-compr.md)**  
  実装：[✓](https://github.com/famous-blue-raincoat/Safe_KV_Compress) ・ リポジトリ内被引用：2  
  保持トークンを選別して捨てる方式はメモリを節約できるが、一般的な評価は最終回答の正答率を重視する。非圧縮の正答率67.4%、正答中の不完全推論率4.3%に対し、SnapKVは正答率50.0%を維持しても不完全推論率が65.5%に増えた。

- **2026-08 · [Benchmarking Composable Compression Techniques in Mixture-of-Experts LLMs](2026-2608.21693-benchmarking-composable-compression-techniques-in-mixture-of-experts-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  専門家枝刈り、量子化、KV圧縮を重ねる配備を10モデルと7ワークロードで一貫評価するベンチマークを構築し、圧縮率では品質も速度も予測できず専門家軸が劣化を支配すること、KV圧縮が長文脈の復号を遅くし得ることを示した。

- **2026-08 · [Archer: Adaptive Reuse of Cached Hidden States for Efficient Rollback in Diffusion Language Models](2026-2608.08086-archer-adaptive-reuse-of-cached-hidden-states-for-efficient-rollback-in-.md)**  
  実装：[✓](https://github.com/Hxnng/Archer) ・ リポジトリ内被引用：2  
  本研究は、拡散言語モデル（Diffusion Language モデル; DLM）が一度生成したトークンを後から置換・再マスクできる「巻き戻し（rollback）」を保持しながら、繰り返しの全系列再計算を減らす推論時のキャッシュ制御を扱う。ただし応答を再計算することと、元の全再計算方式と同じ出力分布・復号経路を保証することは異なる。

- **2026-07 · [When Efficiency Meets Safety: A Benchmark Security Analysis of KV Cache Compression in Large Language Models](2026-2deb03505de5-when-efficiency-meets-safety-a-benchmark-security-analysis-of-kv-cache-c.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈推論では、過去の鍵・値（key-value; KV）をキャッシュすることで各生成ステップの再計算を減らすが、保存するトークンが増えるとGPUメモリ容量と帯域を圧迫する。反対に、CAMのような統合では浅い層の過度な値の重畳が深い層の注意を乱し、LLaMA-2の文脈内攻撃でASRが非圧縮0%から34%へ上がった。

- **2026-07 · [SpecCache: Speculative KV Cache Reuse for Efficient RAG Serving](2026-2c3e6cdc141b-speccache-speculative-kv-cache-reuse-for-efficient-rag-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  検索拡張生成（Retrieval-Augmented Generation; RAG）は検索された複数の文書片を質問へ追加するため、初回トークンの生成までに必要な事前充填（プリフィル）が長くなる。単純な全再利用は回答品質を落とし、全再計算は遅い。ただしこの倍率は特定の検索拡張生成ワークロード、GPU、キャッシュの事前作成・保持という条件に依存する。

- **2026-07 · [LOCKS: Page-Local Compact Key Summaries for Efficient Long-Context Decoding](2026-2607.24555-locks.md)**  
  実装：[✓](https://github.com/Js-Hwang1/locks) ・ リポジトリ内被引用：2  
  長文脈LLMでは復号のたびに過去トークンの鍵・値（KV）を読み、問い合わせと照合する。短文脈で小さなバッチならモデル重みの読出しが支配的だが、長文脈かつ複数要求では要求ごとのKV読出しが帯域を圧迫する。例えばLlama-3.1-8Bの128K文脈はbf16のKVだけで要求あたり約16GiBとなる。本方式はKVキャッシュの削除や容量圧縮ではない。

- **2026-07 · [HqeKV: Towards Hybrid Quantization and Eviction for KV Cache in Long-Context LLM Inference](2026-ec9fa0b99268-hqekv-towards-hybrid-quantization-and-eviction-for-kv-cache-in-long-cont.md)**  
  実装：[✓](https://github.com/skywclouds/HqeKV) ・ リポジトリ内被引用：2  
  一方、文脈長や同時要求数が増えるほどキャッシュがGPUメモリを占め、実行可能なバッチ数を制約する。従来の低ビット量子化は多くのトークンに同じ精度を割り当て、削除方式は低重要度と判断したトークンの情報を完全に失う。著者の実機評価はRTX A6000（48GB）上のLlama-3.1-8B-InstructおよびQwen3-8Bで実施された。

- **2026-07 · [A JoLT for the KV cache: Near-Lossless KV Cache Compression via Joint Rank-bit Allocation](2026-2607.12550-a-jolt-for-the-kv-cache-near-lossless-kv-cache-compression-via-joint-ran.md)**  
  実装：[✓](https://github.com/rahulk98/JoLT-Master-Thesis) ・ リポジトリ内被引用：2  
  従来の低ランク圧縮は保持する特異ベクトル数を決め、量子化は値のビット幅を決めるが、両者を同じメモリ予算の下で同時に配分することは一般的ではなかった。5モデル・4系列の評価では2〜3倍のKV圧縮でパープレキシティ（perplexity）の相対変化を0.2%未満に抑えた。

- **2026-06 · [TGV-KV: Text-Grounded KV Eviction for Vision-Language Models](2026-2606.03075-tgv-kv-text-grounded-kv-eviction-for-vision-language-models.md)**  
  実装：[✓](https://github.com/Danielement321/TGV-KV) ・ リポジトリ内被引用：2  
  TGV-KVは、画像と文章を同時に入力する視覚言語モデル（Vision-Language モデル; VLM）の鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）を、文章の意味を優先して削減する手法である。

- **2026-06 · [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md)**  
  実装：[✓](https://github.com/aiha-lab/TANGRAM) ・ リポジトリ内被引用：2  
  Tangramは、ヘッド別KV保持量を少数サンプルで事前較正し、固定予算のraggedページ化と負荷分散へ変換して、非一様圧縮の断片化・回収費・デコード不均衡を減らす。

- **2026-06 · [Information-Aware KV Cache Compression for Long Reasoning](2026-2606.26875-information-aware-kv-cache-compression-for-long-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の鍵値キャッシュ（KV キャッシュ）圧縮は、直近の問い合わせから大きな注意（注意機構）を受けたトークンを残す設計が多い。LongReasonでは40%・20%の鍵値キャッシュ保持率でSnapKV、PyramidKV、Expected 注意機構を上回り、長い復号でもRPCより高いタスク性能を示す。

- **2026-05 · [OmniRefine: Alignment-Aware Cooperative Compression for Efficient Omnimodal Large Language Models](2026-2605.12056-omnirefine-alignment-aware-cooperative-compression-for-efficient-omnimod.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  固定した時間区切りをフレームと音声の対応に合わせて作り替えてから、映像と音声をそれぞれの冗長構造に合う方式で協調圧縮し、保持率44パーセントで全トークン並みの正解率を保った学習不要の圧縮方式。

- **2026-04 · [When Less Latent Leads to Better Relay: Information-Preserving Compression for Latent Multi-Agent LLM Collaboration](2026-2604.13349-when-less-latent-leads-to-better-relay-information-preserving-compressio.md)**  
  実装：[✓](https://github.com/markli404/When-Less-Latent-Leads-to-Better-Relay) ・ リポジトリ内被引用：2  
  エージェント間の潜在受け渡しでプロンプトのKVを32トークンへ絞り、消した値の直交残差を保持側へ戻す方式で、通信量を約4.7分の1にしながら全受け渡しに近い精度を保った。

- **2026-04 · [Universal YOCO for Efficient Depth Scaling](2026-2604.01220-universal-yoco-for-efficient-depth-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  YOCOの自己デコーダだけをパラメータ共有で再帰化し、全体KVキャッシュを一定に保ちながら深さ方向の計算スケーリングを実現したアーキテクチャ研究。

- **2026-04 · [Sub-Token Routing for KV Cache Compression](2026-2604.21335-sub-token-routing-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来のQuestなどの手法は「どのトークンを残すか」を決め、視覚言語モデルのFastVやVisionZipは大量の視覚トークンを減らす。

- **2026-03 · [Hybrid Associative Memories](2026-2603.22325-hybrid-associative-memories.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本研究は、系列全体を固定長状態へ圧縮する再帰型ニューラルネットワーク（Recurrent Neural Network; RNN）と、過去の各トークンを個別に保持する自己注意（Self-注意機構）を、単に交互に積むのではなく相補的な二つの記憶として組み合わせる。

- **2026-03 · [CARE: Covariance-Aware and Rank-Enhanced Decomposition for Enabling Multi-Head Latent Attention](2026-2603.17946-care-covariance-aware-and-rank-enhanced-decomposition-for-enabling-multi.md)**  
  実装：[✓](https://github.com/FutureMLS-Lab/CARE) ・ リポジトリ内被引用：2  
  活性の共分散で白色化したSVDと層ごとのランク再配分で、GQAからMLAへの変換初期化を改善し、同じKV予算で一括変換のパープレキシティを最大約215倍下げた。

- **2026-02 · [ST-Lite: Training-Free KV Cache Compression with Spatio-Trajectory Guidance for Long-Horizon GUI Agents](2026-2603.00188-st-lite-training-free-kv-cache-compression-with-spatio-trajectory-guidan.md)**  
  実装：[✓](https://github.com/94wen94/ST-Lite) ・ リポジトリ内被引用：2  
  GUI画面の冗長な履歴を類似度で落とし、小さなUI要素の境界を近傍の不一致で守る学習不要のKVキャッシュ圧縮で、5分の1の予算でも全キャッシュ並みの精度と最大2.35倍のデコード高速化を得た。

- **2026-02 · [ARKV: Adaptive and Resource-Efficient KV Cache Management under Limited Memory Budget for Long-Context Inference in LLMs](2026-2603.08727-arkv-adaptive-and-resource-efficient-kv-cache-management-under-limited-m.md)**  
  実装：[✓](https://github.com/Large-scale-Sustainable-Computing-LSC/ARKV) ・ リポジトリ内被引用：2  
  ARKVは、長文脈の自己回帰言語モデルで増大するキー・値キャッシュ（KVキャッシュ）を、原精度で保持するトークン、低精度へ量子化するトークン、破棄するトークンの三種類へ動的に割り当てる推論時の管理方式である。原精度の基準モデルに対する生成速度は平均86.1%であり、圧縮が無条件に高速化をもたらすわけではない。

- **2026-01 · [PackCache: A Training-Free Acceleration Method for Unified Autoregressive Video Generation via Compact KV-Cache](2026-2601.04359-packcache-a-training-free-acceleration-method-for-unified-autoregressive.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  過去の鍵・値（KV）をキャッシュすれば再計算を避けられるものの、フレーム数が増えるほど保存トークンが累積し、自己注意の計算時間とGPUメモリ消費が増える。この外挿比較を「完走した二方式の実測倍率」と同一視してはならない。

- **2026-01 · [HeteroCache: A Dynamic Retrieval Approach to Heterogeneous KV Cache Compression for Long-Context LLM Inference](2026-2601.13684-heterocache-dynamic-heterogeneous-kv-retrieval.md)**  
  実装：[✓](https://github.com/ponytaill/HeteroCache) ・ リポジトリ内被引用：2  
  注意ヘッドの安定性と層内冗長性に応じてKV予算を細粒度配分し、代表ヘッドの注意ドリフト検知時だけCPUから非同期取得することで、224K文脈の復号を完全注意計算比約3倍高速化する。

- **2026-01 · [Beyond Speedup -- Utilizing KV Cache for Sampling and Reasoning](2026-2601.20326-beyond-speedup-utilizing-kv-cache-for-sampling-and-reasoning.md)**  
  実装：[✓](https://github.com/cmd2001/ICLR2026_KV-Embedding) ・ リポジトリ内被引用：2  
  保持済みのKVキャッシュを表現として再利用し、自己評価と難易度予測による思考切替を行い、追加計算ほぼなしで生成トークンを最大5.7倍削減した。

- **2025-12 · [V-Rex: Real-Time Streaming Video LLM Acceleration via Dynamic KV Cache Retrieval](2025-2512.12284-v-rex-real-time-streaming-video-llm-acceleration-via-dynamic-kv-cache-re.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  過去の映像を後から質問される可能性があるため、不要に見えるKVを永久削除する方式は会話の整合性を損なう。論文のエッジ向けV-Rex8構成は、KV長1K〜40KのCOIN動画でフレーム当たり121〜254 ms、すなわち3.9〜8.3 FPSを報告する。

- **2025-12 · [ReFusion: A Diffusion Large Language Model with Parallel Autoregressive Decoding](2025-2512.13586-refusion-a-diffusion-large-language-model-with-parallel-autoregressive-d.md)**  
  実装：[✓](https://github.com/ML-GSAI/ReFusion) ・ リポジトリ内被引用：2  
  応答をスロットへ分割し、スロット間は拡散的に選んでスロット内は自己回帰で埋め、並べ替えでKVキャッシュを全面再利用することで、拡散モデルの並列性と自己回帰モデルの一貫性を両立させた生成方式。

- **2026-11 · [LowRAM: Low-Rank Keys and Amortised Values for Composable KV Cache Compression at Test-Time](2026-2611.07025-lowram-low-rank-keys-and-amortised-values-for-composable-kv-cache-compre.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ヘッド内で値がキーから予測できる冗長性を使い、文脈適応した予測器と誤差上位の残差で値を償却し、キーは層間低ランクで圧縮する非対称なキャッシュ圧縮で、四倍圧縮のほぼ無損失化と、量子化・追い出しとの重ね合わせによる二六・九倍圧縮での性能九四・五パーセント保持を報告した。

- **2026-11 · [FlagRot: Selective Rotation for Low-Bit KV Caches](2026-2611.03992-flagrot-selective-rotation-for-low-bit-kv-caches.md)**  
  実装：[✓](https://github.com/KunmingSHAO/FlagRot_releaser) ・ リポジトリ内被引用：1  
  回転が平らな部分をかえって悪化させる観測から、部分ごとに回すか否かを注意誤差で選んで旗を符号の符号ビットへ隠す方式で、二・五ビットでの発散度を一八・七から一二・四へ下げ、長文脈課題を二・九ポイント回復したと報告した。

- **2026-10 · [Vesta: Queueing-Aware LLM Scheduling for Real-World Workloads](2026-2610.14686-vesta-queueing-aware-llm-scheduling-for-real-world-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  セッションのKVキャッシュ所有先を固定し、実行先だけを待ち行列理論に基づく混雑価格付き目的関数でリクエストごとに選ぶことで、キャッシュ再利用と負荷分散を両立させる分散スケジューラ。

- **2026-10 · [Tailoring the Quantization Space for 1-Bit KV Cache Compression](2026-2610.03027-tailoring-the-quantization-space-for-1-bit-kv-cache-compression.md)**  
  実装：[✓](https://github.com/mscheong01/tasq) ・ リポジトリ内被引用：1  
  クエリ感度によるチャネル重み付け、ヘッド共有スケール、共分散対応のグループ化でベクトル量子化の対象空間を整え、1ビット級KVキャッシュ圧縮の品質劣化を既存方式より大幅に抑えた。

- **2026-10 · [SARIA: Persistence-Aware KV Caching with Coordinated DRAM--SSD Reload for LLM Agents](2026-2610.31169-saria-persistence-aware-kv-caching-with-coordinated-dram-ssd-reload-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェント向け階層KVキャッシュで、繰り返しエビクションと再利用履歴を証拠にDRAM滞在を超える再利用が見込めるブロックだけをSSDへ永続化し、SSDヒットの一部をDRAMへ遅延複製して協調再読込で帯域を分け合うことで、SSD書き込みを全複製比57.1から58.9パーセント減らし平均TTFTをDRAMのみ比42.3から79.7パーセント下げる手法。

- **2026-10 · [RoLaQ: Joint Rotation and Range Calibration for 2-Bit KV Caches in Multi-Head Latent Attention](2026-2610.20686-rolaq-joint-rotation-and-range-calibration-for-2-bit-kv-caches-in-multi-.md)**  
  実装：[✓](https://github.com/noforit/RoLaQ) ・ リポジトリ内被引用：1  
  MLAの共有潜在に対する2ビット量子化で、キー・バリュー射影が定める部分空間での回転学習と、閾値とゲインを結び付けたレンジ較正を合同で行い、保護なしでも最強の比較対象を平均1.1から3.8ポイント上回る精度と容量3.96倍を両立させる。

- **2026-10 · [Rethinking KV Cache Eviction for Agentic LLM Serving](2026-2611.00391-rethinking-kv-cache-eviction-for-agentic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVキャッシュの追い出しを末尾からではなく共有接頭辞の直後から行い、再計算の高い接尾辞を残すことで、実エージェントトレースで初回トークン時間を最大76パーセント削減するサービング方式。

- **2026-10 · [Read What Matters: Query-Adaptive Quantization for KV Caches](2026-2610.11245-read-what-matters-query-adaptive-quantization-for-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVキャッシュの保持精度と読出し量を分離し、漸進符号の接頭辞をクエリごとに2段階（キー側チャネル配分→再構成注意によるバリュー側トークン配分）で配分して、保持したまま読む量だけを削る量子化方式。

- **2026-10 · [Monte Carlo Estimation for KV Cache Eviction](2026-2610.07643-monte-carlo-estimation-for-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  履歴が長くなるほどメモリ容量と転送帯域を圧迫するため、限られた保持枠に重要なトークンだけを残す削除方式が研究されている。一方、同じ条件のサンプル当たり実行時間はAnDProの7.8799秒に対し17.5342秒であり、速度向上ではない。

- **2026-10 · [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](2026-2610.12060-look-back-think-ahead-visual-memory-on-demand-for-efficient-multimodal-r.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  画像の内容を一度だけ要約して視覚トークンを削減すると、生成する文章の最初の段階では十分でも、後の推論段階で必要な細部が削除済みという問題が起こる。固定的な重要度で一回だけ残す方式は、この変化を事前にすべて予測する必要がある。

- **2026-10 · [LatentRemedy: Efficient Remedy For Non-Prefix KV Cache Reuse in Multi-Agent Systems](2026-2610.18014-latentremedy-efficient-remedy-for-non-prefix-kv-cache-reuse-in-multi-age.md)**  
  実装：[✓](https://github.com/chenzhwsysu57/kvreuse) ・ リポジトリ内被引用：1  
  競合課題間の非接頭辞KV再利用で崩れる解釈を、接頭辞から作る16個の潜在トークンを再利用ブロックの後ろへ置いて立て直し、再計算なしに正解率を大きく回復させた。

- **2026-10 · [KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization](2026-2610.14448-kv4-rl-unlocking-faster-asynchronous-rollouts-for-rlvr-with-int4-kv-cach.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  非同期ロールアウトで集中するKV処理をINT4量子化し、シンクと直近文脈だけをINT8で守ることで、RLVRのロールアウトを累積1.80倍速くしながら最終精度の差を0.5ポイント以内に抑える方式。

- **2026-10 · [KV2: A Self-Refining KV Cache](2026-2610.03198-kv2-a-self-refining-kv-cache.md)**  
  実装：[✓](https://anonymous.4open.science/r/KVsquared-0B97/) ・ リポジトリ内被引用：1  
  再利用型KV圧縮で、軽量な代理スコアが選んだ少数の文脈トークンだけを再構成クエリに使い、最終エビクションスコアを決める2段方式。予算2パーセントの極端な圧縮で比較対象との差が最大になる。

- **2026-10 · [KV-Repurpose: A Testbed for Evaluating Non-Prefix KV-Cache Reuse](2026-2610.13060-kv-repurpose-a-testbed-for-evaluating-non-prefix-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/taiga333/eval-kv-repurpose) ・ リポジトリ内被引用：1  
  接頭辞一致に縛られない区間単位のKV再利用をvLLM上で測るテストベッドを構築し、単純な位置補正だけの再利用が単一文書課題では品質を保ち、偏った負荷では同じ容量でヒット率63.9パーセント対3.3パーセントと大きく効く一方、複数文書推論では劣化することを示した。

- **2026-10 · [iS-KV: Online Low-Rank KV Cache Compression via Block-Incremental SVD](2026-2610.02815-is-kv-online-low-rank-kv-cache-compression-via-block-incremental-svd.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  直近を正確に残し古い履歴を低ランク化するオンライン圧縮で、基底更新時に過去の係数も同期させることでドリフトを防ぎ、MATH-500で4.06倍圧縮しながら元モデルの83.6パーセントに対し82.6パーセントを保つ。

- **2026-10 · [FuTransformer: FP8 Prefill and INT4 Decode for Llama-Style Inference on Hopper](2026-2610.23796-futransformer-fp8-prefill-and-int4-decode-for-llama-style-inference-on-h.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィルとデコードで律速が違うことに合わせ、プリフィルはFP8のGEMM後処理融合で中間転送を消し、デコードは重みとKVキャッシュをフラグメント配置のINT4で保持してその場で逆量子化する、Hopper向けの推論ブロック実装。

- **2026-10 · [Folding Attention Biases into Keys Makes Compacted KV Caches Run on Standard Kernels](2026-2610.36520-folding-attention-biases-into-keys-makes-compacted-kv-caches-run-on-stan.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  圧縮KVキャッシュのロジットバイアスを、ヘッドごとに閉形式で求めた1方向へのキー移動で吸収し、標準カーネルと未改変vLLMでそのまま動く通常キャッシュへ変換する手法。

- **2026-10 · [Efficient KV Cache Migration for Geo-Distributed LLM Inference in Collaborative Edge Computing](2026-2610.22172-efficient-kv-cache-migration-for-geo-distributed-llm-inference-in-collab.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  層単位で両方式を混合して通信と再計算を重ね、さらに複数の送信元に対する移動先の選択を最適化することで、移送の完了時刻を短縮する。条件によって直接転送比で約35～45%の移送時間短縮を報告する。

- **2026-10 · [Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches](2026-2610.09827-dual-qk-sharp-queries-and-flat-keys-for-prunable-2-bit-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の長文推論では、過去トークンの鍵・値キャッシュ（KV キャッシュ）がGPUメモリを圧迫し、復号のたびに大量のキーを読み直す。KVを2ビットへ量子化すれば保存容量は減るが、注意スコアに敏感な外れ値が量子化範囲を広げ、精度が崩れる。保存容量の約6.8倍削減と読出量の約8.3倍削減は形式・アクセス量の推定であり、実測速度そのものではない。

- **2026-10 · [Drift Says When, Budget Says How Much: Rate-Controlled KV Re-selection for Long-Form Multimodal Generation](2026-2610.31433-drift-says-when-budget-says-how-much-rate-controlled-kv-re-selection-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文マルチモーダル生成の再選択型KVキャッシュで、除外済みプリフィックスへのアテンション質量をドリフトとして測り、再選択の時期をドリフト、量をリフレッシュ率の制御で決めることで、固定予算64エントリでInfiniGenをROUGE-Lで最大3.8ポイント上回る手法。

- **2026-10 · [Coda: Exploiting Admission Flexibility for Coding-Agent Serving](2026-2610.03088-coda-exploiting-admission-flexibility-for-coding-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  コーディングエージェント向けサービングで、KV状態の準備費用と待ち時間による受付順の並べ替え、文脈長の近い集団への注意分割、多ワーカーでの文脈適合ルーティングを組み合わせ、進行を保ちながらスループットを上げる方式。

- **2026-10 · [BELT: BEhavior-Aligned Low-Rank KV Cache Compression with Learned Top-k Rank Allocation](2026-2610.17966-belt-behavior-aligned-low-rank-kv-cache-compression-with-learned-top-k-r.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意分布と注意出力に目的関数を合わせた低ランクKV圧縮と、全ヘッド横断の学習型ランク配分により、70パーセント圧縮でも長文脈品質を保ち、量子化併用で最大17.8倍の削減と最大3.3倍のデコード高速化を得た。

- **2026-10 · [AlignPred: Error-Controlled KV Cache Compression via Alignment and Predictive Coding](2026-2610.17970-alignpred-error-controlled-kv-cache-compression-via-alignment-and-predic.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  永続KVキャッシュを、ヘッドや層の局所整列と予測符号化で、利用者が指定した再構成誤差の上限内に収めながら圧縮し、階層キャッシュの永続容量を42から72パーセント削減した。

- **2026-10 · [Accelerating CPU Speculative Decoding via Unified Graph Execution and Transactional KV Isolation](2026-2610.28671-accelerating-cpu-speculative-decoding-via-unified-graph-execution-and-tr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  下書きと検証の計算図を単一領域と常駐スレッド群へ統合し、投機キャッシュを静的作業領域へ隔離して巻き戻しを位置初期化だけにすることで、プロセッサ上の投機的デコードを公開基盤比1.35倍、自己回帰比3.99倍に高速化する実行基盤。

- **2026-09 · [WUSH-KV: KV Cache Quantization with Data-Adaptive Transforms](2026-2609.38121-wush-kv-kv-cache-quantization-with-data-adaptive-transforms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キーと値の二階統計と、クエリ側・出力射影側の感度の両方から閉形式で作るデータ適応変換を量子化前に挟むKVキャッシュ量子化で、2ビットでも再構成誤差とパープレキシティを既存変換より小さく保った。

- **2026-09 · [Where Should the KV Cache Live? Placement Policies Across GPU, CPU, and SSD for Long-Lived Sessions](2026-2609.16215-where-should-the-kv-cache-live-placement-policies-across-gpu-cpu-and-ssd-for-long-lived-sessions.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU・CPU・SSD間のKV配置政策を比較し、SSDの容量利得とワークロード別の最適配置・遅延境界を定量化する。

- **2026-09 · [UniCache: Task- and Type-Aware KV Cache Compression for Unified Multimodal Models](2026-2609.32831-unicache-task-and-type-aware-kv-cache-compression-for-unified-multimodal.md)**  
  実装：[✓](https://github.com/Superone77/UniCache) ・ リポジトリ内被引用：1  
  課題ごとに変わるKVキャッシュの種類構成と種類ごとの圧縮の好みを、オフライン較正による方針割当てと注意誘導型の予算配分で扱う学習不要の圧縮枠組みで、理解と編集で5倍の圧縮と最大1.78倍の高速化を得た。

- **2026-09 · [Preserving Provenance in Shared KV Caches for LLM Serving](2026-2609.38706-preserving-provenance-in-shared-kv-caches-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  テナント分離用のソルトを共有鍵に含めない条件では、応答時間から被害者のプロンプトを93%の正確さで識別できた。

- **2026-09 · [Prefill-Free Cross-Family KV Cache Transfer for Heterogeneous Multi-Agent LLMs](2026-2609.32259-prefill-free-cross-family-kv-cache-transfer-for-heterogeneous-multi-agen.md)**  
  実装：[✓](https://github.com/daniel-eai/Prefill-Free-Multi-Agent-LLMs) ・ リポジトリ内被引用：1  
  ファミリーの違うモデル間で、文字境界のトークン対応、3層集約と統計量合わせの写像、注意と出力に合わせた較正の畳み込みにより、受信側プリフィルなしでキーと値のキャッシュを渡せるようにした転送方式。

- **2026-09 · [Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression](2026-2609.36322-periodic-weak-spots-phase-sensitivity-from-chunked-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  チャンク型KVキャッシュ圧縮（chunked KV-キャッシュ compression）は、連続するトークンを固定幅の窓へ区切り、各窓を少数のK/V表現へ要約することで長文脈推論のKV容量と注意計算を削減する。

- **2026-09 · [PatchKV: Weight-Space Compensation of KV Cache](2026-2609.39329-patchkv-weight-space-compensation-of-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数の質問が同じ長い文書やコードベースを参照する場合、文脈を一度だけ読み込み、そのKVを再利用することで質問ごとの計算を減らせる。

- **2026-09 · [MoSE: Mode-Switching Expander for Mixed LLM Training and Inference](2026-2609.39138-mose-mode-switching-expander-for-mixed-llm-training-and-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  推論と訓練が混在するクラスタで、固定した辺予算の配分を時期ごとに切り替える再構成可能なネットワークトポロジにより、KV転送と訓練通信の両方の費用を下げた研究。

- **2026-09 · [Language Models Can Control Their Own Attention](2026-2609.02737-declarative-attention-self-directed-kv-access.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル自身が思考中に注意範囲を宣言し、推論エンジンがKVブロック表を切り替えて不要な長文脈読出しを省く疎注意方式。Gemma-4-31Bで参照トークンを52.0%削減し、精度低下は1.27ポイントだった。

- **2026-09 · [KVCMAS: Efficient KV cache Correction for Shared Context in Multi-Agent Systems](2026-2609.34060-kvcmas-efficient-kv-cache-correction-for-shared-context-in-multi-agent-s.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  完全に再計算すると入力処理が何度も必要になる。一方、先行エージェントのキャッシュを無修正で使うと、注意機構が本来と異なる内部状態を参照して回答品質が大きく落ちる。著者のvLLM実装によるA100 80GBの同時要求試験では、共有文脈32Kトークン、毎秒8要求、キャッシュ再利用率約0.8で、初回トークン待ち時間（TTFT）の中央値が61.95秒であった。

- **2026-09 · [KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation](2026-2609.24298-kv-cobra-kv-cache-compression-via-co-optimized-bit-rank-allocation.md)**  
  実装：[✓](https://github.com/seonha01/KV-COBRA) ・ リポジトリ内被引用：1  
  各トークンのKV値を保持したまま圧縮する方式では、低ランク射影で次元数を減らし、残った座標を量子化することが多い。注意演算単体は特定条件で全精度実装比1.79〜1.89倍高速だが、推論サーバ全体の処理量やP99遅延を測定した結果ではない。

- **2026-09 · [Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction](2026-2609.13285-grouped-value-attention-efficient-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  値だけをKVキャッシュへ保存し、内容キーを値から再構成してクエリ側へ吸収することで、GQAに近い精度を保ちながら永続キャッシュを約45〜47%削減する注意機構。

- **2026-09 · [Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches](2026-2609.17652-fathom-per-query-read-depth-offloaded-kv-cache.md)**  
  実装：[✓](https://github.com/vivekkalyanarangan30/fathom) ・ リポジトリ内被引用：1  
  問い合わせごとに鍵チャネルの読取深度を変え、ホスト退避した疎注意索引の転送量を減らして百万トークン復号を最大一・六七倍高速化する。

- **2026-09 · [Dynamic Flow, Static Graph: KV Cache Reuse for Efficient LLM Serving on Mobile NPUs](2026-2609.34727-dynamic-flow-static-graph-kv-cache-reuse-for-efficient-llm-serving-on-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、固定形状の計算グラフ内で必要なトークンだけ再計算する方式、複数グラフ呼出しを統合する動的計画法、NPU・CPUメモリ・フラッシュにまたがる階層KV保存、読み込み・位置補正・保存とNPU実行の非同期重畳を組み合わせる。

- **2026-09 · [D-Quant: Driftable Entropy Coding for KV Cache Quantization](2026-2609.19880-d-quant-driftable-entropy-coding-for-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  固定サイズ容器と長さ制約付きドリフトを組み合わせ、エントロピー符号化KVキャッシュを注意カーネル内で直接並列復号できる形にした低ビット量子化方式。

- **2026-09 · [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits](2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  文書編集で古くなったKVは重要位置の散発再計算より編集直後を連続再計算する方が有効で、隣接依存なら13〜21倍高速にほぼ完全修復する。

- **2026-09 · [CONDUIT: A Unified Residual-Stream Restoration Framework for KV Cache Reuse in Vision-Language Models](2026-2609.05821-conduit-a-unified-residual-stream-restoration-framework-for-kv-cache-reu.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  画像や文書を一度読み込んだ視覚言語モデルに別の質問を投げるとき、以前の視覚トークンのキー・値（KV）キャッシュを再利用できれば、画像の再処理を減らせる。しかし接頭辞に質問や指示が追加・変更されると、同じ画像であっても以前の計算結果は新しい文脈に対して古くなる。単純な全再計算は正確だが遅く、古いKVをそのまま使うと回答品質が下がる。

- **2026-09 · [Cartridges++: KV Cache Compression without Off-Context Derailment](2026-2609.35621-cartridges-kv-cache-compression-without-off-context-derailment.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  文書を一度だけ処理し、少数の仮想KV位置へ圧縮した記憶を複数の質問で再利用できれば、デコード時に参照するKV長を減らせる。主要なQwen3長文3課題で、後者の関連性ルータは文書内質問の90%超を受理し、文書外質問の90%超を拒否した。

- **2026-09 · [CacheReforge: Bounded Recovery for Stale KV Caches under Evolving Adapters](2026-2609.30884-cachereforge-bounded-recovery-for-stale-kv-caches-under-evolving-adapter.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  アダプターの更新で古くなったKVキャッシュを、層ごとの版の記録と感度とずれの積による危険度で判定し、直接再利用、範囲を絞った再計算、影響サフィックス全体の再計算の三つから選んで回復させることで、KLを92.4パーセント減らしながら再計算を層の5.44パーセントに抑えた研究。

- **2026-09 · [Budgeted Cache Repair for Cross-Context KV-Cache Reuse](2026-2610.02233-budgeted-cache-repair-for-cross-context-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  文脈横断キャッシュ再利用の精度損失はゲートや呼び出し選択では消えず、2トークンのドラフトで注意の集まる行を選び固定予算だけ正確に再計算することでGSM8Kの精度を稠密水準へ回復させる方式。

- **2026-09 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](2026-2609.04971-beaconkv.md)**  
  実装：[✓](https://github.com/aiha-lab/BeaconKV) ・ リポジトリ内被引用：1  
  長い推論で過去の計画へ再注意する問い合わせを少数のビーコンとして保持し、将来再参照されるKVを予測して残す訓練不要の圧縮方式。

- **2026-09 · [ActKV: Efficient LLM Agents through Action-Guided KV Cache Management](2026-2609.31395-actkv-efficient-llm-agents-through-action-guided-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  行動生成時の注意履歴で将来の操作に必要なキー・値状態を選び、生成確信度に応じて保存枠を拡張し、ページ化された実キャッシュを追加作業領域なしで圧縮する。ReAct型の長期タスクでは、無圧縮方式に対する平均タスク精度98.53%を、ピークKV容量25.98%で維持する。

- **2026-08 · [vToken: Token-Level Virtualization for Reclaimable KV Caches](2026-2608.13263-vtoken-token-level-virtualization-for-reclaimable-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ページ化注意（PagedAttention）は固定長ブロックを非連続配置して外部断片化を抑えるが、H2OやScissorhandsなどの削除方策は「残すトークン」をブロックより細かい単位で選ぶ。

- **2026-08 · [Strong Drafts Need Compact Memories: Long-Context Speculative Decoding with Compressed KV Cache](2026-2608.30252-strong-drafts-need-compact-memories-long-context-speculative-decoding-wi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案するメモリ拡張スライディング窓（メモリ-Augmented Sliding Window、MASW）は、強い独立下書き器のKVメモリを、先頭の注意シンク、直近の正確なKV、過去を圧縮した学習可能なメモリスロットに分ける。

- **2026-08 · [Small Frequency Corrections Can Change What Survives KV Cache Compression](2026-2608.27128-small-frequency-corrections-can-change-what-survives-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  バリューの強さを、似たキーが離れた場所に何個あるかという頻度で割り引いて保持要素を選び直し、質問が来る前のキャッシュ圧縮で冗長な要素より例外的な要素を残りやすくする学習なしの方式。

- **2026-08 · [KVDiagnosis: A Diagnostic Benchmark for KV-Cache Compression in Long-Context Language Models](2026-2608.09412-kvdiagnosis-a-diagnostic-benchmark-for-kv-cache-compression-in-long-cont.md)**  
  実装：[✓](https://github.com/ChosenQC/KVDiagnosis) ・ リポジトリ内被引用：1  
  長文脈LLMの鍵・値キャッシュ（KVキャッシュ）を圧縮する研究では、通常、圧縮後の平均正答率と保存容量が比較される。うち7,913行（63.2%）は証拠位置の測定・投影被覆が低いか部分的であった。

- **2026-08 · [GraniKV: Asymmetric Granularity KV-Cache Paging for Multi-Agent Systems with Long Shared Prefix](2026-2608.15584-granikv-asymmetric-granularity-kv-cache-paging-for-multi-agent-systems-w.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数エージェント型の大規模言語モデル推論では、システム指示、道具定義、共有メモリなどからなる長い接頭辞を複数要求が共有し、その後ろに各要求固有の生成履歴が接尾辞として伸びる。

- **2026-08 · [DualPath: Accelerating Agentic LLM Inference by Harvesting Disaggregated KV-Cache Storage I/O](2026-3f706ddceb51-dualpath-accelerating-agentic-llm-inference-by-harvesting-disaggregated-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来の入力処理・復号分離（プリフィル–デコード disaggregation）では、過去のKVキャッシュを入力処理エンジン（プリフィル engine; PE）がストレージから読み、計算後に復号エンジン（デコード engine; DE）へ転送する。

- **2026-08 · [CommitKV: Lifecycle-Aware KV Cache Compression via Commit Transitions for Multi-Turn Agents](2026-2608.07855-commitkv-lifecycle-aware-kv-cache-compression-via-commit-transitions-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CommitKVは、工具呼出しを伴う多輪の推論・行動型エージェント（ReAct agent）で増大する鍵・値キャッシュ（KV キャッシュ）を、情報の利用状態が変化した瞬間を利用して削減する手法である。

- **2026-08 · [Beyond Sparse Weights: When Is Attention Compressible?](2026-2608.21541-beyond-sparse-weights-when-is-attention-compressible.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  疎な注意マップだけではKV圧縮を正当化できないことを理論化し、値分散配分と末尾要約を厳密な物理予算で実装するCertKVを提案。

- **2026-07 · [SelKV: Selective KV Cache Merging with Per-Token Merge-or-Drop and Attention Compensation](2026-2607.16213-selkv-selective-kv-cache-merging-with-per-token-merge-or-drop-and-attent.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  単純なKV削除は必要な情報を失う一方、削除対象を保持KVへ一律に統合する方式では、似ていない値ベクトルまで混ざり、重要な表現を壊す場合がある。

- **2026-07 · [REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression](2026-real-kv.md)**  
  実装：[✓](https://github.com/yonseicasl/REAL) ・ リポジトリ内被引用：1  
  成功例だけでなく偏り・注意散漫を含む4種の注意挙動を測り、推論に重要なヘッドへKV予算を重点配分することで、長文脈の精度を保ちながらキャッシュを圧縮する。

- **2026-07 · [MosaicKV: Serving Long-Context LLM with Dynamic Two-D KV Cache Compression](2026-2607.00760-mosaickv-serving-long-context-llm-with-dynamic-two-d-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MosaicKVは、極長文脈のKVキャッシュを系列方向とチャネル方向の両方で圧縮し、容量削減だけでなく注意計算そのものを高速化するサービングシステムである。一方、両者を単純に組み合わせると重要要素まで二重に捨ててしまい、論文のQuestベース素朴実装ではチャネル圧縮率30%で24.5%、70%で82.8%の精度低下が生じる。

- **2026-07 · [Lynx: Progressive Speculative Quantization for accelerating KV Transfer in Long-Context Inference](2026-2607.01831-lynx-progressive-kv-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LynxはKVを上位ビットのAnchorとResidualへ分割し、Anchor到着後に低精度で投機生成、Residual到着後に一括検証して、分離サービングの転送待ちを隠しつつINT8級品質を保つ。

- **2026-07 · [KVpop — Key-Value Cache Compression with Predictive Online Pruning](2026-2607.05061-kvpop-key-value-cache-compression-with-predictive-online-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVpopは、長文脈の自己回帰推論でキー・値（KV）キャッシュが文脈長とともに増大する問題に対し、将来参照される見込みのあるトークンを、限られた保存枠に残すための学習型追い出し方式である。

- **2026-07 · [HiKV: Hierarchical Importance-Aware KV Cache with Hardware Acceleration for LLM Decoding](2026-2607.22389-hikv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HiKVは、長文脈デコードでKVキャッシュが外部メモリアクセスの大部分を占める問題に対し、トークン単位と要素単位という二つの独立した冗長性を順番に削るアルゴリズム・ハードウェア協調設計である。1%以内の精度低下という同一条件で外部メモリアクセスを平均7.17倍削減し、注意計算を平均5.70倍、最大7.95倍高速化し、エネルギーを80〜90%削減する。

- **2026-07 · [GSRQ: Gain–Shape Residual Quantization for Sub-1-bit KV Cache](2026-2607.01065-gsrq-gain-shape-residual-quantization-for-sub-1-bit-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  通常の残差ベクトル量子化（Residual Quantization; RQ）は、小さなコードブックで近似した誤差を次段のコードブックで繰り返し近似する。別途、独自PyTorch/Triton実装の単一A100 80GBにおけるデコード測定では、8K文脈で1.59倍、64Kで3.40倍のトークン当たり遅延短縮を報告する。

- **2026-07 · [GroupKV: Hierarchical KV Cache Management for Long-Context Diffusion LLM Inference](2026-2609.17573-groupkv-hierarchical-kv-cache-diffusion-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散型LLMの長文KVを連続グループ単位で疎選択し、層間予測先読みと古さ補正を組み合わせてCPU退避時の転送量と待ち時間を削減する。

- **2026-07 · [Codec-Gauge: Learning Compression-Friendly Gauges for Transformer KV Caches](2026-2607.20538-codec-gauge-learning-compression-friendly-gauges-for-transformer-kv-cach.md)**  
  実装：[✓](https://huggingface.co/cccat6/Codec-Gauge) ・ リポジトリ内被引用：1  
  要求数、文脈長、層数、KVヘッド数に比例してキャッシュが増えるため、低ビット量子化や数値圧縮を行ってGPUメモリの使用量と転送量を抑える。

- **2026-07 · [Back from the Future: Key-Value Cache Management by Counter-Causal Surprise](2026-2607.27600-back-from-the-future-key-value-cache-management-by-counter-causal-surpri.md)**  
  実装：[✓](https://github.com/metacognitionai/counter_causal) ・ リポジトリ内被引用：1  
  従来のスライディングウィンドウは古いトークンを機械的に捨て、H2Oなどのheavy-hitter方式は過去に多く注意されたトークンを残す。Qwen2.5-7B、RTX4090のキャッシュ更新1回では、KV長512で54msから7.9ms、4096で496msから52.6msとなり、更新処理単体で7～9倍速くなる。

- **2026-07 · [Adaptive Filtering of the KV Cache: Diagnosing and Correcting Structural-Role Bias in LLM Inference](2026-2607.13205-adaptive-filtering-of-the-kv-cache-diagnosing-and-correcting-structural-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文推論のKVキャッシュを圧縮するとき、H2Oに代表される方式は過去のqueryから多くの注意を受けたトークンを重要とみなし、保持予算の上位へ残す。Llama-3.1-8B-Instructの合成JSONでは、区切り記号のトークン当たり平均注意量13.64に対し、回答を持つ値は0.336であり、約40倍の開きがある。

- **2026-06 · [Vortex: Efficient and Programmable Sparse Attention Serving for AI Agents](2026-2606.06453-vortex-programmable-sparse-attention-serving.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/vortex_torch) ・ リポジトリ内被引用：1  
  ページ化KVを抽象化するvFlow/vTensorと最適化バックエンドで、動的疎注意を数行のPython表現からSGLang実運用へ落とし込み、全注意比最大3.60倍のスループットを実現する。

- **2026-06 · [Unified KV Pooling to Accelerate Long-Context LLM Serving](2026-2606.14779-unified-kv-pooling-to-accelerate-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数RAM/SSDを帯域幅比例の単一KVプールとして並列利用し、SPDK直アクセスでファイルシステムを迂回して長文脈KV再取得を高速化する。

- **2026-06 · [UltraQuant: 4-bit KV Caching for Context-Heavy Agents](2026-2606.20474-ultraquant-4-bit-kv-caching-for-context-heavy-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キー・バリューキャッシュを浮動小数点四ビットと二の冪の尺度で保持し逆量子化を行列コアの命令へ畳み込むことで、本番由来のエージェントトレース再生で十六ビット基準の二・七一倍と四・三八倍の適格要求処理能力を、八ビット方式の半分のバイト数で達成したと報告した。

- **2026-06 · [STaR-KV: Spatio-Temporal Adaptive Re-weighting for KV Cache Compression in GUI Vision-Language Models](2026-2606.01790-star-kv-spatio-temporal-adaptive-re-weighting-for-kv-cache-compression-i.md)**  
  実装：[✓](https://github.com/kawhiiiileo/STaR-KV) ・ リポジトリ内被引用：1  
  注意の部分空間ごとの空間特化、履歴の時間的安定度、点数分布のエントロピーという三軸でキャッシュの点数を較正する学習不要の圧縮で、同予算の比較方式中最も高い精度と約4割のメモリ削減を両立させた。

- **2026-06 · [RoPE-Aware Bit Allocation for KV-Cache Quantization](2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/blockgtq) ・ リポジトリ内被引用：1  
  回転位置埋め込みの周波数ブロックごとのエネルギーに応じて鍵キャッシュのビット幅を配分し、圧縮した鍵・値を直接読む融合注意計算で長文脈推論の容量とメモリ帯域を同時に削減する。

- **2026-06 · [PTStore (Prefix Tensor Store): Distributed Prefix Caching and Replication for High Throughput Inference Serving](2026-2607.22648-ptstore-prefix-tensor-store-distributed-prefix-caching-and-replication-f.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同じ長文やシステムプロンプトを含む問い合わせを複数GPU・計算ノードで処理すると、共通prefixに対して入力処理で計算した注意機構のkey/value（KV）を要求ごとに再生成する。著者は長文文書 QAで、メモリを複数ノード/GPUに集約しない比較方式より5–6倍効率的と要旨で総括する。

- **2026-06 · [MM-ShiftKV: Decode-Aware Prefill-Stage KV Selection for Multimodal Large Language Models](2026-2607.22586-mm-shiftkv-decode-aware-prefill-stage-kv-selection-for-multimodal-large-.md)**  
  実装：[✓](https://github.com/zjuDBxAI/MM-ShiftKV) ・ リポジトリ内被引用：1  
  生成段階のクエリの分散の大きさを模した代理クエリを入力処理中に作り、注意の質量に基づく群ごとの投票で残すキーを選ぶことで、予算六十四でも六課題の平均得点六九・三を保ち、入力長三万二千で生成遅延を最大一・九倍、最大メモリを約四十三パーセント削減したと報告した。

- **2026-06 · [Last But Not Least: Boundary Attention CalibratiON for Multimodal KV Cache Compression](2026-2606.14782-last-but-not-least-boundary-attention-calibration-for-multimodal-kv-cach.md)**  
  実装：[✓](https://github.com/ryu1ion/official_BACON) ・ リポジトリ内被引用：1  
  最終クエリの注意が観測窓を上回る差分を境界証拠として抽出し、層内の広がりと層間の持続で雑音を除いてから観測窓の点数へ較正して加える方式で、強い圧縮ほどキャッシュ圧縮の精度を大きく改善した。

- **2026-05 · [WaveFilter: Enhancing the Long-Context Capability of Diffusion LLMs via Wavelet-Guided KV Cache Filtering](2026-2606.00724-wavefilter-enhancing-the-long-context-capability-of-diffusion-llms-via-w.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  WaveFilterは、拡散型大規模言語モデル（diffusion LLM; dLLM）が長い文脈を処理するとき、鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）の重要な位置を選別して注意機構へ渡す方式である。

- **2026-05 · [Towards Generalization of Block Attention via Automatic Segmentation and Block Distillation](2026-2605.15913-towards-generalization-of-block-attention-via-automatic-segmentation-and.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  意味のある分割を学ぶセグメンタと、凍結した全アテンション教師から学ぶブロック蒸留で、ブロックアテンションを一般領域へ広げ、KVキャッシュの使い回しで長文の最初のトークンまでの時間を大幅に下げた研究。

- **2026-05 · [Reformulating KV Cache Eviction Problem for Long-Context LLM Inference](2026-2605.07234-reformulating-kv-cache-eviction-problem-for-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  既存の追い出し手法は、過去のトークンが受けた注意重みを平均・集計し、その値の大きな位置を残すことが多い。NVIDIA H100 80GBでのLlama-3.1-8B、128K文脈、同保持予算の効率測定では、完全キャッシュ比で復号のトークン当たり遅延が2.3倍改善し、最大メモリは63.3GBから約47.5GBへ低下した。

- **2026-05 · [RcLLM: Accelerating Generative Recommendation via Beyond-Prefix KV Caching](2026-2605.07443-rcllm-accelerating-generative-recommendation-via-beyond-prefix-kv-cachin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  接頭辞にならない履歴とアイテムのKVを意味複製とグラフ分割の2層で分散保持し、親和性のある台へ寄せて重みトークンだけ再計算することで、推薦の最初の応答を最大9.51倍速くした分散推論系。

- **2026-05 · [QKVShare: Quantized KV-Cache Handoff for Multi-Agent On-Device LLMs](2026-2605.03884-qkvshare-quantized-kv-cache-handoff-for-multi-agent-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  送信側が既に計算した注意機構の鍵・値キャッシュ（KVキャッシュ）を、受信側がテキストから再計算する再事前充填（re-プリフィル）は無駄が大きい。

- **2026-05 · [OCTOPUS: Optimized KV Cache for Transformers via Octahedral Parametrization Under optimal Squared error quantization](2026-2605.21226-octopus-optimized-kv-cache-for-transformers-via-octahedral-parametrizati.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  OCTOPUSは、Transformerの長文脈推論で肥大化するKVキャッシュを、回転前処理と3座標単位の幾何学的量子化によって縮小する研究である。一方、H200で測った単一クエリの融合デコードはbf16 SDPAより8.9倍遅い条件がある。

- **2026-05 · [NestedKV: Nested Memory Routing for Long-Context KV Cache Compression](2026-2605.26678-nestedkv-nested-memory-routing-for-long-context-kv-cache-compression.md)**  
  実装：[✓](https://github.com/ChenHong30/NestedKV) ・ リポジトリ内被引用：1  
  学習不要のKV圧縮では、注意重みが大きいトークン、最近のトークン、鍵ベクトルが平均から離れたトークンなどを残す方法が使われる。Qwen3-4B、RULERの4,000トークン文脈、KVの75%を削除する条件でNestedKVは79.32点、単一の全文平均方向を使うKeyDiffは60.22点だった。

- **2026-05 · [Efficient Cooperation-Aware Key and Value Management for LLM Inference](2026-3089a0084f72-efficient-cooperation-aware-key-and-value-management-for-llm-inference.md)**  
  実装：[✓](https://github.com/ZJU-DIVER/CoKV) ・ リポジトリ内被引用：1  
  得られたSSVは事前にモデルと検証データから計算し、実行時にはヘッド群別の保持トークン数やKV量子化ビット数の重みとして使う。Qwen3-32Bで平均128組のKVを保持する設定では、GSM8Kの正答率82.10%、MATH 46.17%を報告し、比較した圧縮方式を上回る。

- **2026-05 · [CONF-KV: Confidence-Aware KV Cache Eviction with Mixed-Precision Storage for Long-Horizon LLM Inference](2026-2605.24786-conf-kv-confidence-aware-kv-cache-eviction-with-mixed-precision-storage-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  過去の注意重みに基づく方式は、重要そうなトークンを選別できる反面、将来どの情報が必要になるかを正確には予測できない。

- **2026-05 · [ArborKV: Structure-Aware KV Cache Management for Scaling Tree-based LLM Reasoning](2026-2605.22106-arborkv-structure-aware-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  活動経路の保護、トークン単位の選択的追い出し、後戻り時の遅延再構築を組み合わせ、単一RTX 4090上のToT評価で同一キャッシュ予算の系列方式を上回り、256展開の探索を5.6 GiBで完了した。

- **2026-04 · [ZoomR: Memory Efficient Reasoning through Multi-Granularity Key Value Retrieval](2026-2604.10898-zoomr-memory-efficient-reasoning-through-multi-granularity-key-value-ret.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  推論の段落要約を索引にして、注意ヘッドの合意が取れた区間だけ原文をCPUから読み戻すKV管理で、全キャッシュ退避比でもメモリを4倍超削りながら同予算の圧縮方式を正解率で大きく上回った。

- **2026-04 · [YOCO++: Enhancing YOCO with KV Residual Connections for Efficient LLM Inference](2026-2604.13556-yoco-enhancing-yoco-with-kv-residual-connections-for-efficient-llm-infer.md)**  
  実装：[✓](https://github.com/wuyou2002/YOCO-plus) ・ リポジトリ内被引用：1  
  下半分の各層で最下層のキーと値を重み付きで混ぜてからキャッシュすることで、キャッシュ半減の効率を保ったままYOCOの品質低下を回復し標準モデルも上回った。

- **2026-04 · [Retrospective Sparse Attention for Efficient Long-Context Generation](2026-2508.09001-retrospective-sparse-attention-for-efficient-long-context-generation.md)**  
  実装：[✓](https://github.com/csh3695/RetroAttention) ・ リポジトリ内被引用：1  
  arXiv:2508.09001の2026年5月20日改訂版（v2）を一次資料とし、本文・表・付録の実験条件を確認した。目的は、長い入力を一度読むプリフィルだけでなく、数千トークンに及ぶ生成の途中で疎な注意計算の近似誤差が蓄積する問題を軽減することにある。提案名はRetrospective Sparse 注意機構、実装名はRetroAttentionである。

- **2026-04 · [RetentiveKV: State-Space Memory for Uncertainty-Aware Multimodal KV Cache Eviction](2026-2605.04075-retentivekv-state-space-memory-for-uncertainty-aware-multimodal-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  捨てられる視覚KVを削除せず、注意のエントロピーで重み付けした状態空間の連続状態へ吸収して必要時に想起する圧縮で、遅れて重要になる視覚情報を守りながらキャッシュを大幅に減らした。

- **2026-04 · [MoE-nD: Per-Layer Mixture-of-Experts Routing for Multi-Axis KV Cache Compression](2026-2604.17695-moe-nd-per-layer-mixture-of-experts-routing-for-multi-axis-kv-cache-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし一つの圧縮率やビット幅を全層に一律適用すると、圧縮に弱い層まで強く削られ、圧縮に強い層に余裕を残す。非圧縮KVが1859 MB・平均11.5の条件で、提案の異種割当は136 MB・平均12.0だった。

- **2026-04 · [KV Cache Offloading for Context-Intensive Tasks](2026-2604.08426-kv-cache-offloading-for-context-intensive-tasks.md)**  
  実装：[✓](https://github.com/yandex-research/context-intensive-kv-offloading) ・ リポジトリ内被引用：1  
  文脈集約型課題でKV退避の選択誤差を分析し、低ビット量子化によるYAKVで精度とスループットを改善する。

- **2026-04 · [DASH-KV: Accelerating Long-Context LLM Inference via Asymmetric KV Cache Hashing](2026-2604.19351-dash-kv-asymmetric-hashing-long-context.md)**  
  実装：[✓](https://github.com/Zhihan-Zh/DASH-KV) ・ リポジトリ内被引用：1  
  注意の全キー内積を学習済み非対称ハッシュ検索へ置換し、重要トークンだけ完全精度へ戻すことで、長文脈の計算量を線形化しつつLongBench品質をFull 注意機構近傍に維持する。

- **2026-03 · [Ouroboros: Wafer-Scale SRAM CIM with Token-Grained Pipelining for Large Language Model Inference](2026-2603.02737-ouroboros-wafer-scale-sram-cim-with-token-grained-pipelining-for-large-l.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全演算をウェハ上のSRAM内で実行するメモリ内計算の設計に、トークン粒度パイプライン・分散動的KV管理・通信認識配置を組み合わせ、シミュレーションで平均スループット4.1倍とエネルギー効率4.2倍を示した。

- **2026-03 · [EntropyCache: Decoded Token Entropy Guided KV Caching for Diffusion Language Models](2026-2603.18489-entropycache-decoded-token-entropy-guided-kv-caching-for-diffusion-langu.md)**  
  実装：[✓](https://github.com/mscheong01/EntropyCache) ・ リポジトリ内被引用：1  
  自己回帰型言語モデルの因果注意では、過去トークンの鍵・値（Key–Value; KV）表現は後続トークンの追加で変わらないため、過去KVを厳密に再利用できる。これに対して離散拡散言語モデル（discrete Diffusion Language モデル; dLLM）は双方向注意を使い、マスクされたトークンが一つ確定するだけで他の全位置の表現が変わり得る。

- **2026-03 · [ELORA: Efficient LoRA and KV Cache Management for Multi-LoRA LLM Serving](2026-d563756c245c-elora-efficient-lora-and-kv-cache-management-for-multi-lora-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ELORAは、複数のLoRAアダプタを一つの基盤LLMへ切り替えて提供するサービング環境で、GPUメモリのLoRAと履歴KVキャッシュを別々に管理することによる無駄を減らす方式である。著者らの観測では、vLLMのGPU内KVの平均42.4%が、対応LoRAが存在しないため直ちに利用できない「invalid KV」になる。

- **2026-03 · [CacheNotes: Task-Aware Key-Value Cache Compression for Reasoning-Intensive Knowledge Tasks](2026-04cca81d3e08-cachenotes-task-aware-key-value-cache-compression-for-reasoning-intensiv.md)**  
  実装：[✓](https://github.com/giulio98/cachenotes) ・ リポジトリ内被引用：1  
  コーパスに対しタスク別の圧縮計画トークン（CPTs）を生成し、CPTsからの注意を用いてコーパスKVキャッシュを一度だけ圧縮する。H100の128KコーパスでTTFT 0.13秒、RAG 0.61秒、全再入力15.88秒。

- **2026-03 · [Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding](2026-2603.23914-attention-aware-inference-optimizations-large-vlm-memory-efficient-decoding.md)**  
  実装：[✓](https://github.com/git-disl/AttentionPack) ・ リポジトリ内被引用：1  
  複数ヘッドをまとめた低ランク分解で視覚言語モデルのKVを圧縮し、注意度に応じて復元精度を変えることで、動画QAのキャッシュを8.11分の1にしつつバッチ推論を60%高速化する。

- **2026-02 · [Stopping Computation for Converged Tokens in Masked Diffusion-LM Decoding](2026-2602.06412-stopping-computation-for-converged-tokens-in-masked-diffusion-lm-decodin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  マスク拡散デコードで事後分布が安定した位置をロックして以降の計算を止め、キーとバリューはキャッシュから読ませることで理論計算量を30から50パーセント減らした研究。

- **2026-02 · [Q Cache: Visual Attention is Valuable in Less than Half of Decode Layers for Multimodal Large Language Model](2026-2602.01901-q-cache-visual-attention-is-valuable-in-less-than-half-of-decode-layers-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MLLMで隣接デコード層のアテンションが半数以上の層で類似する観測に基づき、層をまたいでクエリとキーを共有するレイジーアテンションとQキャッシュでKVキャッシュを35パーセント以上削減しスループットを1.5倍にした研究。

- **2026-02 · [Dynamic Mixed-Precision Routing for Efficient Multi-step LLM Interaction](2026-2602.02711-dynamic-mixed-precision-routing-for-efficient-multi-step-llm-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェントの臨界ステップが約1パーセントしかないという観測に基づき、最高精度のKVキャッシュを共有しながらステップごとにデコード精度を切り替えるDMRの研究。

- **2026-02 · [CryptoGen: Secure Transformer Generation with Encrypted KV-Cache Reuse](2026-2602.08798-cryptogen-secure-transformer-generation-with-encrypted-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  暗号化したまま再利用できるKVキャッシュと、プリフィルとデコードで使い分ける異種符号化により、安全な自己回帰生成のスケーリングを2次からほぼ線形へ変えた研究。

- **2026-02 · [Compiler-Assisted Speculative Sampling for Accelerated LLM Inference on Heterogeneous Edge Devices](2026-2602.08060-compiler-assisted-speculative-sampling-for-accelerated-llm-inference-on-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMの逐次生成では、次のトークンを決めるたびに大型モデルを実行するため、計算資源が限られるエッジ機器では応答遅延が大きくなる。投機的サンプリングは小型草稿モデルが複数の候補トークンを先に生成し、大型検証モデルがまとめて検証することで、大型モデルの呼び出し回数を減らす。

- **2026-01 · [Singular Proxies for Adaptive Caching in Diffusion Language Models](2026-2602.02544-singular-proxies-for-adaptive-caching-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/wenhao728/spa-cache) ・ リポジトリ内被引用：1  
  自己注意（self-注意機構）が双方向であるため、ある位置のトークンを更新すると別の位置の隠れ状態にも影響が及び、自己回帰型モデルのように過去の鍵・値（KV）を常に固定したまま再利用することはできない。LLaDA-8BのMBPPでは通常復号5.75トークン/秒に対し46.12トークン/秒（8.0倍）で、正解率は39.20から39.00へ変化した。

- **2026-01 · [NPU Design for Diffusion Language Model Inference](2026-2601.20706-npu-design-for-diffusion-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  双方向注意の全系列計算、ブロック更新型の鍵値キャッシュ、縮約中心のサンプリングに専用命令と分離メモリで対応する拡散言語モデル専用NPUで、GPU比で最大4.91倍の速度と23.3倍の電力効率を得た。

- **2026-01 · [Joint Encoding of KV-Cache Blocks for Scalable LLM Serving](2026-2601.03067-joint-encoding-of-kv-cache-blocks-for-scalable-llm-serving.md)**  
  実装：[✓](https://github.com/sef1/kv_fast_fusion) ・ リポジトリ内被引用：1  
  余弦類似度がしきい値を超えたキー・バリューキャッシュのブロックを方向の平均で共有表現へ融合し大きさだけを個別に残すことで、七百二十億級モデルで圧縮率四・三八倍を達成し、提供基盤の測定でトークン処理能力が約四割向上したと報告した。

- **2026-01 · [Dynamic Thinking-Token Selection for Efficient Reasoning in Large Reasoning Models](2026-2601.18383-dynamic-thinking-token-selection-for-efficient-reasoning-in-large-reason.md)**  
  実装：[✓](https://github.com/Robin930/DynTS) ・ リポジトリ内被引用：1  
  DynTS（動的 Thinking-Token Selection）は、長い思考列を生成する大規模推論モデル（Large Reasoning モデル; LRM）で、最終回答に必要な思考トークンのキー・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を残し、その他を推論途中に削除する方式である。

- **2026-01 · [ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management](2026-2601.13631-contiguouskv-accelerating-llm-prefill-with-granularity-aligned-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV 枝刈りとI/Oの粒度をContiguousChunkへ統一し、二段非同期プリフェッチでSSD KV読み込みを計算と重ねてRe-プリフィルを最大3.85倍高速化する。

- **2026-01 · [Adaptive Layer Selection for Layer-Wise Token Pruning in LLM Inference](2026-2601.07667-adaptive-layer-selection-for-layer-wise-token-pruning-in-llm-inference.md)**  
  実装：[✓](https://github.com/TANIGUCHIREI/ASL) ・ リポジトリ内被引用：1  
  ASL（適応的選別層）は、長い入力を処理するTransformerのどの層でトークンを間引くべきかを、実行時の注意分布から判断する方式である。

- **2025-12 · [SmartCache: Context-aware Semantic Cache for Efficient Multi-turn LLM Inference](2025-f88744e972d2-smartcache-context-aware-semantic-cache-for-efficient-multi-turn-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数ターン対話の意味的な重複に対し、会話を階層索引する意味フォレストと注意による話題転換検出とKVキャッシュ共有・追い出しを協調設計し、再計算とメモリ重複を減らすSmartCache。

- **2025-12 · [KV-CAR: KV Cache Compression using Autoencoders and KV Reuse in Large Language Models](2025-2512.06727-kv-car-kv-cache-compression-using-autoencoders-and-kv-reuse-in-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVベクトルを埋め込み次元のオートエンコーダで圧縮保存し、隣接層の類似ヘッドはKVを再利用する圧縮手法。量子化や枝刈りと直交する次元の軸を削り、最大47.85パーセントのKV削減を小規模モデルで示す。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [Where Should a KV-Cache Repair Budget Go? Distractor Structure and Contextual Compatibility in Non-Prefix Reuse](2026-2611.06397-where-should-a-kv-cache-repair-budget-go-distractor-structure-and-contex.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非プリフィックスKV再利用の損失をディストラクタの出所を変えて分解し、損傷が多数のディストラクタへ分散すること、質問アテンションではターゲットをほとんど見つけられないこと、小さい修復予算は検索器の最上位チャンクを質問の直前へ移して再計算する使い方が有効であることを示した分析論文。

- **2026-11 · [TripleKV: Predict, Prefetch, Protect -- KV Cache Management for AI Agents](2026-2611.25112-triplekv-predict-prefetch-protect-kv-cache-management-for-ai-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ツール実行中に追い出されたエージェントのKVキャッシュについて、完了時刻をツール固有に予測してSSDからホストDRAMへだけ先読みし、保護付き置換で再利用まで残すことで、クリティカルパス上のSSD読みを要するリクエストを45から76パーセントから10パーセント未満へ減らす3階層KV管理。

- **2026-11 · [Transformer-FSQ: Discrete Latents for Extreme KV-Cache Compression](2026-2611.09598-transformer-fsq-discrete-latents-for-extreme-kv-cache-compression.md)**  
  実装：[✓](https://github.com/ASzecsenyi/transformer-fsq) ・ リポジトリ内被引用：0  
  残差状態を有限スカラー量子化の広い低ビット格子へ写して整数コードだけをメタデータなしで保持することで、圧縮率12倍から97.5倍の極端なKVキャッシュ圧縮でも長文脈検索の精度を比較手法中最高に保ち、デコード速度も非圧縮並み以上を実測したKVキャッシュ圧縮。

- **2026-11 · [TraceKV: Policy-Preserving Low-Rank KV Cache Compression for Reasoning Vision-Language Models](2026-2611.15569-tracekv-policy-preserving-low-rank-kv-cache-compression-for-reasoning-vi.md)**  
  実装：[✓](https://github.com/AK-DREAM/TraceKV) ・ リポジトリ内被引用：0  
  自己生成した推論トレースでの較正、フィッシャー感度で重み付けした特異値分解、全層でのランク配分により、方策のKL乖離を抑える無訓練の低ランクKV圧縮TraceKVを提案し、量子化併用で5.64倍圧縮しながら正解率を密モデルの73.58%に対し73.41%に保った。

- **2026-11 · [The Storage View of KV Cache: Characterizing Cache Behavior Across LLM Workloads](2026-2611.10178-the-storage-view-of-kv-cache-characterizing-cache-behavior-across-llm-wo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  11トレースをKVブロック単位で横断測定し、KV状態が単一セッション状態と多セッション状態の2形態を取ること、保持・回収・配置にはワークロードID・セッションID・セッション完了信号の3つの汎用信号で足りることを定量化した、多層KVストレージ設計のための分析研究。

- **2026-11 · [Testing Quantized KV-Cache Maintenance: Encoding Layout and Historical Restoration](2026-2611.30720-testing-quantized-kv-cache-maintenance-encoding-layout-and-historical-re.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化KVキャッシュの保守について、符号化回数を揃えてもレイアウトでドリフトが変わることと、現在状態の合格が履歴復元を保証しないことを対照実験で示し、検査が保証する契約の明示を求めるテスト研究。

- **2026-11 · [State Space Attention: Learning Context-Dependent Memory Retention](2026-2611.33625-state-space-attention-learning-context-dependent-memory-retention.md)**  
  実装：[✓](https://github.com/Ege-Cakar/State-Space-Attention) ・ リポジトリ内被引用：0  
  学習済みスコアラがチャンク単位で保持する過去表現を選び直し、捨てた情報が必要だった学習誤りをスコアラへ返す回復で学習することで、読み取り予算576トークンでも8K文脈の検索課題で全注意に数ポイント差まで迫る、推論メモリ一定の注意機構。

- **2026-11 · [RoCoKV: Accelerating LLM Inference Serving through Uncertainty and Redundancy Aware KV Cache Compression](2026-2611.25433-rocokv-accelerating-llm-inference-serving-through-uncertainty-and-redund.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論モデルの冗長な推論トレースでKV予算が奪われる問題に対し、モデルの不確実性で枝刈り強度を変え、直近内容と似たトークンを割り引くRoCoKVを提案し、制約付き予算で既存圧縮法より高い精度と、vLLM実測でFull-KV比最大1.43倍の高速化を示した圧縮法。

- **2026-11 · [RES: Accelerating Diffusion Language Models with Rolling Entropy Sampling](2026-2611.29066-res-accelerating-diffusion-language-models-with-rolling-entropy-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルで受理とKVキャッシュへの確定を分離し、受理済み連続プレフィックスが最小長に達した時点でだけ確定するローリング型サンプラーRESを提案し、DiffusionGemmaの7ベンチマークでパスあたりトークン数を19.3から25.5へ増やした（マクロ精度は80.7%から78.8%）。

- **2026-11 · [ReKV: Overlapping Quantized KV Transfer and Suffix Recomputation](2026-2611.08770-rekv-overlapping-quantized-kv-transfer-and-suffix-recomputation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離のKV受け渡しで、層境界より前を量子化転送し、境界状態から後ろをデコード側で再計算して転送と重ねることで、8K受け渡し遅延をBF16全転送の最大3.65倍まで短縮した、品質ゲート付きの結合方針。

- **2026-11 · [PackLoop: Row-Packed Self-Speculative Decoding for Looped Language Models under Concurrency](2026-2611.30205-packloop-row-packed-self-speculative-decoding-for-looped-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ループ型モデルの自己投機が同時実行で効かなくなる原因を行単位のKV読込みと特定し、投機位置を行へ詰め込む配置とEOQによる入場規則で、164負荷点中161点で最良の既存スケジュールを上回った厳密なデコード方式。

- **2026-11 · [OPSERVE: Opportunistic LLM Inference over Fragmented GPU Capacity in HPC Systems](2026-de7f1d0908f4-opserve-opportunistic-llm-inference-over-fragmented-gpu-capacity-in-hpc-.md)**  
  実装：[✓](https://github.com/sc26-submission/aionhpc-26-adsubmission) ・ リポジトリ内被引用：0  
  HPCで一時的に遊ぶGPU断片の上に過渡ワーカーを起動し、プリフィルとデコードの遅延比率に応じてワーカーの役割を動的に配り直し、完了済みプリフィルのKV状態を共有層で回収後も生かすことで、固定配分比で95パーセンタイル遅延を最大15.4倍短くした機会的推論基盤。

- **2026-11 · [One Million Tokens in 20GB: Calibration-Free 2-Bit SRFT KV-Cache Compression for Looped MoE Inference on Apple Silicon](2026-2611.29092-one-million-tokens-in-20gb-calibration-free-2-bit-srft-kv-cache-compress.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NoPE型モデルの値の単位RMS正規化を使い、SRFT回転後のKVキャッシュを較正なしで実効2.06ビットへ圧縮し、32GB Apple M6上でInkling-2-Miniの100万トークン推論を19.49GiB・9.52トークン毎秒で動かしたKV圧縮とMetalカーネル。

- **2026-11 · [Norn: Context-Length-Aware Optimization of Weight and KV Cache Placement for Offloaded LLM Inference](2026-2611.32295-norn-context-length-aware-optimization-of-weight-and-kv-cache-placement-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフロード推論の計算割当てと重み・KVキャッシュ配置を文脈長ごとに最適化した複数計画を事前に作り、デコードの進行に合わせて切り替えることで、静的配置が将来のKVキャッシュ予約で払う性能損失を消し、実機で最大16.8倍のエンドツーエンド高速化を示した動的配置方式。

- **2026-11 · [NoHairCache: Calibrate-Once KV Cache Eviction with One Power-Law Exponent](2026-2611.29006-nohaircache-calibrate-once-kv-cache-eviction-with-one-power-law-exponent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  累積注意型と直近ウィンドウ型のエビクションを単一の冪乗スコア族の両端として統一し、その減衰指数をモデル固有の量として1回だけ校正して使い回すことで、3データセット全てで両方式を上回るパープレキシティを示したKVキャッシュ・エビクションのスコアラ。

- **2026-11 · [Nebula: Distributed Position-Independent Caching for LLM Serving](2026-2611.09474-nebula-distributed-position-independent-caching-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  位置に依存しないキャッシュのセグメントをクラスタ全体の一級対象として遠隔再利用と並列プリフィルを可能にし、ビュー同期・容量自己調整・完了時刻モデルによる配置の3機構で、中央値TTFTを最強比較対象比で平均61.4%削減した分散LLMサービング基盤。

- **2026-11 · [Native Block-Quantized Matrix Multiplication and Explicit K/V Residency with Dual-View Access for LLM Inference on RISC-V Vector Processors](2026-2611.31937-native-block-quantized-matrix-multiplication-and-explicit-k-v-residency-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RVVの汎用性を保ちながら、ブロック量子化行列積をネイティブブロック実行にまとめるQBSと、K/V常駐と多ビュー供給を行うAKVで、射影を幾何平均35.68〜51.34倍、デコード注意を1.45倍高速化し、面積増12.65%でエネルギー効率19.78倍を得た。

- **2026-11 · [Mayfly: Lifecycle-Aware High-Bandwidth Flash for Recursive Self-Improvement](2026-2611.32264-mayfly-lifecycle-aware-high-bandwidth-flash-for-recursive-self-improveme.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再帰的自己改善のKVバーストに対し、実行中KVの高帯域フラッシュからの読み出しをステップ単位で制限し、空いたHBMへの復帰とセッション終了通知による書き込み制御を組み合わせ、世代の完了時間を置き戻し方式より最大55%短縮した階層メモリ管理。

- **2026-11 · [Looping Deeper Without Growing the KV Cache: Recurrent Depth for Causal Encoder-Decoders](2026-2611.13378-looping-deeper-without-growing-the-kv-cache-recurrent-depth-for-causal-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ループを因果エンコーダ側に置いて大域KV源を反復精緻化し、確率的深さ学習による固定点で最終ラウンドだけのKV共有を無損失化することで、ループなしと同量の常駐KVのまま再帰深度の利得の86から93パーセントを得て、552BサービングでKV 36.8分の1とスループット3.6倍を示したループ型アーキテクチャ。

- **2026-11 · [LooM: Loop-Invariant Memory for Causal Encoder-Decoder Language Models](2026-2611.06835-loom-loop-invariant-memory-for-causal-encoder-decoder-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  メモリを書く層と読む層を因果エンコーダ・デコーダで分け、読む層はKVエントリを初回訪問時だけ公開することで、キャッシュ量をループ回数から切り離し、3回から21回までの計算予算をルータなしの1モデルで担えるようにしたループ型言語モデルの実行規則。

- **2026-11 · [LiveLoRA: Exact KV Cache Migration Across LoRA Updates for LLM Agents](2026-2611.31105-livelora-exact-kv-cache-migration-across-lora-updates-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  最終ブロック限定のアダプタと固定した下向き射影で履歴の低ランク座標を版不変にし、KVキャッシュを閉形式で移行することで、8K履歴32セッションの公開を再プリフィル比68.98倍に速めた、エージェント向けの版整合なアダプタ公開方式。

- **2026-11 · [HiPerfCC-KVCache: Accelerating Confidential LLM Serving with Hierarchical KV Caching](2026-2611.28702-hiperfcc-kvcache-accelerating-confidential-llm-serving-with-hierarchical.md)**  
  実装：[✓](https://github.com/sept-usc/HiPerfCC-KVCache) ・ リポジトリ内被引用：0  
  機密コンピューティング下の階層KV転送がドライバロックで無関係な処理を止める問題を特定し、資源寿命・バックアップ順序・補助コンテキスト復元の3調整で、H200実機で幾何平均1.74倍のスループットと平均36パーセントのTTFT削減を示したSGLangランタイム。

- **2026-11 · [Gossamer: A Utility-Driven Architecture for Constant-Budget KV Cache Compression in Reasoning LLMs](2026-2611.29497-gossamer-a-utility-driven-architecture-for-constant-budget-kv-cache-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化・マージ・エビクションを効用で選ぶ枠組みと、類似度計算を注意へ融合して空き演算で済ませる仕組みでKVキャッシュを一定予算に保ち、未圧縮比最大16.7倍のスループットと未圧縮に最も近い推論精度をシミュレーションで示した推論LLM向けKV圧縮アーキテクチャ。

- **2026-11 · [Fast 4-bit KV-Cache Decoding on Hopper GPUs: Why Existing Kernels Are Slow and How to Fix Them](2026-2611.30027-fast-4-bit-kv-cache-decoding-on-hopper-gpus-why-existing-kernels-are-slo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Hopperで4ビットKVが遅い原因を命令発行予算の超過と処理の直列化と特定し、書込み時レイアウトとワープ特化で帯域の67〜75%を使うデコードカーネルを作り、vLLM内でFP8比最大1.64倍のデコードと1.63倍のキャッシュ容量を実現した研究。

- **2026-11 · [Fairway: Load-Aware KV Cache Reuse for LLM Prefill Scheduling](2026-2611.02082-fairway-load-aware-kv-cache-reuse-for-llm-prefill-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再利用率と自分の処理時間で割った相対待ちで並べる速い車線と、作業量の課金で最も古い要求の前の作業を抑える公平な車線を組み合わせ、調整なしで尾の初回トークン時間を先行方式より最大八・六倍下げ、過負荷でも中央値を犠牲にせず飢餓を起こさなかったと報告した。

- **2026-11 · [Exact on Paper: Which LLM Serving Shortcuts Flip Graded Answers, Measured Against the Noise of Reordering the Same Requests](2026-2611.29663-exact-on-paper-which-llm-serving-shortcuts-flip-graded-answers-measured-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  正確とされるサービング機能がどのリクエストの正誤を入れ替えるかを、再起動と到着順変更の2つのノイズ床とバッチ不変カーネルの対照で測り、精度確認だけではFP8 KVキャッシュ級の反転を見逃すことを示した検証研究。

- **2026-11 · [Coordinated Mixed-Precision KV Cache Quantization for Efficient LLM-based Multi-agent Systems](2026-2611.10096-coordinated-mixed-precision-kv-cache-quantization-for-efficient-llm-base.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同時に常駐する複数エージェントのキャッシュへ、直近のクエリ・キー・バリューから推定した感度に基づき共有予算の下でビット幅を協調配分する量子化で、平均三ビットの平均正解率六八・三五パーセントと最強の比較対象比プラス〇・五九ポイント、別条件でキャッシュ最大容量の三二・〇八パーセント削減と一・三八倍の高速化を報告した。

- **2026-11 · [CarrierKV: An Edge LLM Accelerator with Positional Carrier Decomposition for Low-Bit KV Cache](2026-2611.26857-carrierkv-an-edge-llm-accelerator-with-positional-carrier-decomposition-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キーのエネルギーの大半を占める位置依存成分を回転位置埋め込みの前で取り除き、内容残差だけを4ビットで保存して、取り除いた成分のスコア寄与は位置から再生成することで、NVFP4と同じ容量のまま低ビットKVキャッシュの精度損失をほぼ消すエッジ向けアクセラレータ。

- **2026-11 · [Can KV Cache Be Reused Across Model Updates? A DeepSeek-V4-Flash Case Study](2026-2611.14051-can-kv-cache-be-reused-across-model-updates-a-deepseek-v4-flash-case-stu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  旧モデルのKVキャッシュを更新後のモデルへ直接渡す再利用を四つの更新で測り、検索の保持、質問応答の高速化と品質低下、分布の発散の増え方がタスクで異なることを明らかにする分析。

- **2026-11 · [CALFA-KV: Joint Calibration and Fisher-Guided Anchors for 1-Bit KV Cache Compression](2026-2611.10511-calfa-kv-joint-calibration-and-fisher-guided-anchors-for-1-bit-kv-cache-.md)**  
  実装：[✓](https://github.com/XiancaiTian/CALFA-KV) ・ リポジトリ内被引用：0  
  注意出力に合わせた量子化器の共同較正と、フィッシャー型感度で重み付けした再構成誤差による高精度アンカー選択を組み合わせ、1ビット級のKVキャッシュでBF16との平均差を最小で0.90点まで縮める圧縮法。

- **2026-11 · [BasisKV: Value Latents for Communication and Key Routing](2026-2611.02583-basiskv-value-latents-for-communication-and-key-routing.md)**  
  実装：[✓](https://github.com/alexz949/BasisKV) ・ リポジトリ内被引用：0  
  バリューの低ランク潜在表現を一つ作り、KVキャッシュ幅、テンソル並列の通信、キーのページ選択の三つに共有することで、8GPUテンソル並列で最大1.42倍の高速化を得る低ランク圧縮法。

- **2026-11 · [Anchor: Augmented Cross-Layer Recurrent State for Long-Context Retrieval in Test-Time Training](2026-2611.04327-anchor-augmented-cross-layer-recurrent-state-for-long-context-retrieval-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈検索を担う層が少数のアンカー層に限られ他層の再帰状態は基底違いの重複だという観測を使い、テスト時学習の状態をアンカー層だけに置いて1つの共有状態を層固有の読み写像で読むことで、状態量を10倍小さくしながら検索精度をLoLCATsの2.3〜3.1倍にし、遅延を最大4.3倍下げた線形化手法。

- **2026-11 · [Aggron: Aggressive Compression of Agentic KV Caches during Head-of-Line Stalls in the Request Queue](2026-2611.26435-aggron-aggressive-compression-of-agentic-kv-caches-during-head-of-line-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントのKVキャッシュ圧縮を、文脈が大きくなってから一括で行うのではなく、リクエストが待ち行列でヘッド・オブ・ライン停滞に止まる時間へ埋め込むサービング方式。要約できる散文だけを別キューで小さく何度も圧縮し、高負荷でP99遅延を27〜31パーセント削減、スループットを1.34〜1.40倍にしながら精度を無圧縮と同等に保つ。

- **2026-10 · [ZipFusion: Fusing Lossless KV Decompression with Attention for Efficient LLM Decoding](2026-2610.33719-zipfusion-fusing-lossless-kv-decompression-with-attention-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  無損失圧縮したKVキャッシュを注意カーネルが直接読み、レジスタ内の簡単なビット演算で値を再構成することで、復元の受け渡しを消してデコードの帯域を下げ、空いたメモリを同時実行数の増加へ回す仕組み。

- **2026-10 · [WIRE: Weight Space Implicit Representation Encoding of Frozen Video LLMs](2026-2610.17355-wire-weight-space-implicit-representation-encoding-of-frozen-video-llms.md)**  
  実装：[✓](https://github.com/AmeenAli/WIRE) ・ リポジトリ内被引用：0  
  凍結した動画言語モデルの視覚入力を質問条件付き走査でキャリアトークンへ圧縮して列を物理的に短くし、圧縮で失われた情報をハイパーネットワーク生成の一時的な低ランク重み更新へ移すことで、プリフィルとKVキャッシュを削減する方式。

- **2026-10 · [Where KV-Cache Error Lives in Looped Language Models: A Diagnostic Study of Ouro and Huginn](2026-2610.41825-where-kv-cache-error-lives-in-looped-language-models-a-diagnostic-study-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ループ型モデルのキー・値キャッシュで、感度は値が九十四パーセントを担うのに実測の分布のずれはキーが八十九パーセントを担う逆転と、二次の予測が典型列では当たるが少数の自信の強い行で集計が崩れることを同一行の測定で示し、共有重みの増幅が三十二回繰り返しで誤差の向きにより一・六五倍から四・〇九倍まで変わると報告した診断研究である。

- **2026-10 · [When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill](2026-2610.21500-when-the-kv-cache-is-slower-than-the-gpu-scaling-remote-kv-tiers-for-con.md)**  
  実装：[✓](https://github.com/LMCache/LMCache) ・ リポジトリ内被引用：0  
  遠隔KVティアが再計算より遅くなる条件を帯域下限と固定費の2項モデルで示し、MLA KVストアのランク間シャーディングと遠隔ティアのランク分割で帯域を6.3倍にして、ヒット過多時のp99を83.32秒から0.67秒へ戻した実運用の分析と対策。

- **2026-10 · [WAKMan: Workload Aware KVCache Manager](2026-2610.36355-wakman-workload-aware-kvcache-manager.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  直近のトラフィックを影のLRUと影のS3FIFOで再生し、模擬ヒット率の高い方へ追い出し方策を切り替える管理方式で、種別情報なしにLRU比で平均5ポイントのヒット率改善と最小の後悔を得た。

- **2026-10 · [WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds](2026-2610.02713-wakekv-reactive-reversible-kv-residency-for-heads-that-change-their-mind.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ヘッド分類を固定せず、冷えたKVページをCPU側の貯留庫へ可逆に降格し、必要になった瞬間に正確な状態を取り戻す反応型の常駐方針で、変わり続けるヘッドの読み方へ追随する手法。

- **2026-10 · [Visual Cache Reuse for Efficient Multimodal Inference](2026-2610.25136-visual-cache-reuse-for-efficient-multimodal-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  似た画像のKVキャッシュを、エントロピーの低いパッチは再利用し、注意の高い非一様パッチは再計算し、残りをマスクする近似再利用で活かし、完全一致と近似で階層管理を分けることで、視覚言語モデルのプリフィルを品質を保ちながら減らすサービング系。

- **2026-10 · [Virtual Head Attention](2026-2610.17959-virtual-head-attention.md)**  
  実装：[✓](https://github.com/PaddlePaddle/VHA) ・ リポジトリ内被引用：0  
  物理クエリヘッド半減とKVヘッド2本化で生じる多様性の損失を、学習時だけの線形な仮想展開と低ランク出力混合で回復し、推論時には標準のグループ化注意へ吸収してキャッシュと計算量と品質を同時に改善する注意機構。

- **2026-10 · [Video-MemComp: Taylor-Guided Sensitivity-Aware Memory Management for Streaming Video Understanding](2026-2610.32784-video-memcomp-taylor-guided-sensitivity-aware-memory-management-for-stre.md)**  
  実装：[✓](https://github.com/hhnk666/videomemorycompress) ・ リポジトリ内被引用：0  
  誤差を層の感度と局所誤差へ分解し、位置回転前の集約と感度に応じた予算配分でKVキャッシュを定数へ抑え、全保持を超える精度を出した動画向けメモリ管理方式。

- **2026-10 · [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](2026-2610.12338-vfold-symmetry-aware-cross-layer-value-cache-compression.md)**  
  実装：[✓](https://github.com/nverma1/vfold) ・ リポジトリ内被引用：0  
  注意の対称性で整列写像を重みへ畳み込み、関数を変えずに隣接層のバリューキャッシュを平均共有する層間圧縮。注意計算は無改変で、誤差はマージの瞬間だけに生じる。

- **2026-10 · [TwinPrune: Density-Aware Two-Phase Token Pruning for Vision-Language Models](2026-2610.17530-twinprune-density-aware-two-phase-token-pruning-for-vision-language-mode.md)**  
  実装：[✓](https://github.com/Kai-Liu001/TwinPrune) ・ リポジトリ内被引用：0  
  視覚トークンの空間密度を一度だけ測り、プリフィルではマージによる計算削減へ、デコードではキー・バリュー追い出しによるメモリ削減へ使い回す二相圧縮で、あわせて最初のトークンだけで採点するベンチマークではデコード圧縮を測れないことも実証した研究。

- **2026-10 · [To Cache or Not to Cache: Understanding and Mitigating Safety Incompatibility in Cross-Model KV Cache Reuse](2026-2610.15721-to-cache-or-not-to-cache-understanding-and-mitigating-safety-incompatibi.md)**  
  実装：[✓](https://github.com/Snakinya/VReparo) ・ リポジトリ内被引用：0  
  別モデルのKVキャッシュ再利用が受け手の安全行動を変える現象を体系的に測り、バリューが主因であることを示したうえで、層とヘッドごとのアフィン補正で攻撃成功率を平均57.28パーセントから39.21パーセントへ下げつつ時間短縮を保った研究。

- **2026-10 · [Titan-Llama: Retrofitting Pre-trained LLMs with External Neural Memory Modules](2026-2610.19210-titan-llama-retrofitting-pre-trained-llms-with-external-neural-memory-mo.md)**  
  実装：[✓](https://github.com/sarahpannn/titans-pytorch) ・ リポジトリ内被引用：0  
  事前学習済みモデルの初期層をブロック注意へ換え、遠い履歴をテスト時学習で更新する固定サイズのニューラルメモリへ圧縮することで、土台を凍結したまま長文脈の正解率を分割注意から大きく回復し、デコードの速度とメモリも改善した研究。

- **2026-10 · [TideKV: Delayed KV eviction via layer-wise chunked prefill for memory-efficient long-context LLM inference](2026-2610.24499-tidekv-delayed-kv-eviction-via-layer-wise-chunked-prefill-for-memory-eff.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルを層優先に並べ替えて各層の完了まで追い出しを遅らせ、層末圧縮を二度走査で省メモリに実行することで、選択の質と最終キャッシュを保ったまま構築ピークを最大83.89パーセント削減する方式。

- **2026-10 · [Think Before You Speak: Enabling Training-Free Latent Communication Between Language Models](2026-2610.16165-think-before-you-speak-enabling-training-free-latent-communication-betwe.md)**  
  実装：[✓](https://github.com/rishiskhare/CacheFuse) ・ リポジトリ内被引用：0  
  KV形状が一致する異サイズモデル間で、送信側と受信側のKVキャッシュをスカラー重みで線形補間する学習不要の潜在通信CacheFuseを提案し、精度の向上とテキスト通信に対する大幅なTTFT短縮を示した研究。

- **2026-10 · [The Token-Energy Law of LLM Decode: Active Bytes and Realized Time Account for Joules per Token](2026-2610.28576-the-token-energy-law-of-llm-decode-active-bytes-and-realized-time-accoun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有重みバイト、固有KVバイト、実現時間の3座標でデコードのトークンあたりエネルギーを表す法則を立て、係数固定のまま未観測条件・別装置・離脱条件へ当てて最大誤差3.73パーセントで検証した計測研究。

- **2026-10 · [The Price of Precision: A Calibrated Cost Model for Mixed-Precision LLM Serving](2026-2610.15629-the-price-of-precision-a-calibrated-cost-model-for-mixed-precision-llm-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  律速資源を見分ける較正つきコストモデルで混合精度構成の遅延を予測し、精度割当てと文脈依存スケジュールに使う手法。

- **2026-10 · [The Optimization Landscape of Learning Compacted Context Models](2026-2610.05885-the-optimization-landscape-of-learning-compacted-context-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結モデルを通してKVキャッシュ圧縮を学習する際の損失景観を、恒等写像が大域解になる線形写像で可視化して鋭い盆地と平らな停滞域を特定し、密な損失・自己学習・重み緩和が圧縮時と反復時に効かない理由を示した上で、単一ヘッドのクロスアテンションだけに簡素化した書き込み器が圧縮品質と速度で比較対象を上回ることを示した研究。

- **2026-10 · [TempoKV: Predictive KV Cache Quantization for Autoregressive Video Generation](2026-2610.15324-tempokv-predictive-kv-cache-quantization-for-autoregressive-video-genera.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動画KVキャッシュの時間予測可能性の非対称性を使い、キーはキー履歴から、値は現在のキーと値履歴から予測して残差だけを低ビット保存することで、学習なしで最大6.71倍の圧縮と最良の品質効率均衡を達成する。

- **2026-10 · [TDLM: Adaptive Temporal Integration for Diffusion Language Models](2026-2610.36940-tdlm-adaptive-temporal-integration-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの未確定位置が過去ステップの自位置表現を時間的注意で再利用できるようにし、少ないデノイザー評価で同等の回答品質を得る、凍結基盤への軽量な追加モジュールと自己蒸留学習。

- **2026-10 · [TAO: Tool-Aware Joint Scheduling for LLM-Based Agentic Serving](2026-2610.37230-tao-tool-aware-joint-scheduling-for-llm-based-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  道具の戻り時刻、時間で減衰する節点別キャッシュ価値、文脈量を辞書式に評価し、待機セッションの受入れと配置を動的計画法で一括最適化することで、エージェント型サービスの遅延を最大26.8パーセント下げた。

- **2026-10 · [Swarm Telepathy: Prefill-Free KV-Cache Transfer Across Families](2026-2610.15095-swarm-telepathy-prefill-free-kv-cache-transfer-across-families.md)**  
  実装：[✓](https://github.com/Ar-Kareem/SwaT) ・ リポジトリ内被引用：0  
  異なるモデルファミリー間で送信側のKVキャッシュを学習済みマッパーで受信側のキャッシュへ変換し、受信側のプリフィルなしにエージェント間通信を行う方式で、テキスト通信より高精度かつ高速であることを示した研究。

- **2026-10 · [Spend Bytes on Breadth: Precision–Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning](2026-2610.05685-spend-bytes-on-breadth-precision-count-trade-offs-for-decode-time-kv-com.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  古いデコード KVをKIVI形式で2、3、4ビット量子化し、直近128トークンはfp16に残す。3モデル、複数の数学・科学ベンチマーク、2予算の計18条件では、BreadthKVがfp16のSnapKV-D 追い出しより17条件で正答率が高く、16条件で95%信頼区間が0を除く。

- **2026-10 · [SoloQ: Calibration-Free Quantization for Diffusion Language Models](2026-2610.07121-soloq-calibration-free-quantization-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Panda/SoloQ) ・ リポジトリ内被引用：0  
  拡散言語モデルの活性値分布の揺れを追わず、K-RPBH回転で分布が予測可能な空間へ写して較正なしに重み・活性値・KVキャッシュを4ビット量子化し、精度とメモリ削減を両立させる手法。

- **2026-10 · [SlimKV: Joint Token-Feature KV Cache Compression with Reconstruction-Free Beacon Attention](2026-2610.02953-slimkv-joint-token-feature-kv-cache-compression-with-reconstruction-free.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ビーコンの鍵と値を低ランク潜在として学習し層適応に配分するトークンと特徴の同時圧縮に、ビーコン鍵だけ位置埋め込みを外して再構成なしの潜在注意を組み合わせ、32倍圧縮でも長文性能で首位を保ち、文脈128Kで復号を最大3.38倍速くした。

- **2026-10 · [SIEVE: Preserving Cross-Image Evidence via Depth-Aware Token Compression](2026-2611.00351-sieve-preserving-cross-image-evidence-via-depth-aware-token-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数画像の視覚トークンを、画像ごとの等量クォータとデコーダ深さ方向の漸進的選択・同一画像内集約で圧縮し、保持率12.5%でプリフィル計算量を6.6倍削減し遅延を1.9倍高速化しながら未圧縮の平均精度を上回った、学習不要のVLM推論圧縮方式。

- **2026-10 · [Serving a Revisable World: Versioned Execution for Interruptible Agents](2026-2610.01160-serving-a-revisable-world-versioned-execution-for-interruptible-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントの計画差し替えを版付き実行で扱い、旧版の権限取消し・残り実行の有界化・有効プリフィックスの認証継承を1つの遷移に統一して、陳腐化出力の漏れと再計算の無駄を同時に消す制御面の再設計。

- **2026-10 · [ServeTwin: A Benchmark-Validated Simulator for Distributed LLM Architecture Exploration](2026-2610.02732-servetwin-a-benchmark-validated-simulator-for-distributed-llm-architectu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  仕様駆動の解析時刻計算を、KVライフサイクルと多ターンセッションを追う閉ループのサービング状態へ組み込み、実測プロファイルなしで未改変ベンチマークを回して実機と照合できる分散推論シミュレータ。

- **2026-10 · [Selective and Hybrid-State Communication for Latent Multi-Agent Systems](2026-2610.37779-selective-and-hybrid-state-communication-for-latent-multi-agent-systems.md)**  
  実装：[✓](https://github.com/mliao2710/SelectKV) ・ リポジトリ内被引用：0  
  潜在マルチエージェントの引き継ぎで、継承した文脈を保護しつつ新しいKVだけを選んで送る選択的通信と、全注意のKVと線形注意の再帰状態を併せて渡すハイブリッド状態通信の二方式。

- **2026-10 · [SARP: An On-SSD Index for KVCache with Fast Prefix Matching and Recovery](2026-2610.26849-sarp-an-on-ssd-index-for-kvcache-with-fast-prefix-matching-and-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVブロックの識別子とメタデータをSSD上のセグメントへ詰め、メモリには疎なルーティング点と候補フィルタだけを置くことで、再起動時の復旧を速くしながらプリフィックス照合のストレージ読み取りを抑える永続KV索引。

- **2026-10 · [RISK-KV: Quality-Aware Selective KV Cache Reconstruction for Distributed LLM Inference](2026-2610.29544-risk-kv-quality-aware-selective-kv-cache-reconstruction-for-distributed-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴KVの一部を両側の正確なKVからの回帰で再構成し、残りを正確に保持する方式。再構成の可否は数値誤差ではなく実際に測った予測損失で層ごとに決め、品質予算のゲートで選ぶことで、履歴KVを最大で約3分の1省きながら品質変化を小さく抑える。

- **2026-10 · [RIFT: KV Cache Compression for Draft Models with Complementary Compressibility Training](2026-2610.31098-rift-kv-cache-compression-for-draft-models-with-complementary-compressib.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドラフトモデルのKV圧縮で、プリフィル選択が生成中に陳腐化する問題に対し、直近ウィンドウとの予算併用、デコード中の再採点、適応的な更新間隔、圧縮マスク付き蒸留学習を段階的に組み合わせ、固定予算で受理長をほぼ維持する手法群。

- **2026-10 · [Rehearse Everything, Remember Nothing: Attic-KV Rehearses What Will Be Read](2026-2610.12133-rehearse-everything-remember-nothing-attic-kv-rehearses-what-will-be-rea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Attic-KV（Attic）は、長い文書を一度だけプリフィルしてKVキャッシュを保存し、将来の多数の質問に使い回す環境で、質問がまだ分からない段階でKVを圧縮する方式である。最終的なKV位置の重要度は再読時の注意機構・出力寄与から決め、保持率3～5%という厳しい条件でも事実を残しやすくする。

- **2026-10 · [Recency Is the Wrong Axis: A Negative Result on Windowed Deepest-Plane KV Caching in Looped Language Models](2026-2610.34436-recency-is-the-wrong-axis-a-negative-result-on-windowed-deepest-plane-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  最深プレーンだけのKV共有への最近窓修復は、効くかどうかが新しさではなくプレーンの収束度と共有される位置で決まることを、3モデルと事前登録実験で示した否定的結果。窓の採用前に熟成度テストとプロンプト側確認が必要になる。

- **2026-10 · [Real Long-Term Memory for AI: A 50-Million-Token Window That Is Faster and Cheaper Than Recompute](2026-2610.10845-real-long-term-memory-for-ai-a-50-million-token-window-that-is-faster-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック単位のKV状態を暗号化してNVMeへ永続化し再計算なしに復元するメモリ層で、5,000万トークンの範囲を一定のGPUメモリのまま扱い、復元が再計算より速く省エネルギーになることを実測した研究。

- **2026-10 · [Range: Decoupling KV-Cache Reuse Granularity from Storage Work](2026-2610.21241-range-decoupling-kv-cache-reuse-granularity-from-storage-work.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  保存経路の費用を項目数ではなくバイト数と物理バッチで数える原則の下で、区間チケット、固定バイトストライプ、完了所有の転送バンクにより、6ギガバイト復元のTTFTを項目数32倍の範囲と層ごと配送でも1.79から1.80秒に保つKV保存エンジン。

- **2026-10 · [Queuing for Inference: Dynamic Memory Footprints and Costly Preemption](2026-2610.33923-queuing-for-inference-dynamic-memory-footprints-and-costly-preemption.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成とともに増えるKVキャッシュ、容量超過時の速度低下、状態退避を伴う高価なプリエンプションを待ち行列モデルへ組み込み、古典的最適方針が崩れる理由と、プリエンプション回数を制限しながら短いジョブを優先する方針の平均応答時間を解析した理論研究。

- **2026-10 · [PriorityFEC: Deadline-Aware Streaming FEC for KV-Cache Handoff in Edge Multi-Agent Systems](2026-2610.21390-priorityfec-deadline-aware-streaming-fec-for-kv-cache-handoff-in-edge-mu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層と位置ごとの感度で測ったKVの効用順に送信し、確認応答で滑るストリーミング前方誤り訂正と二重DQNの修復配分で、締切までに届く有用なKVを最大化するエッジ間引き継ぎ方式で、厳しい締切で課題F1を比較対象比で大きく保った。

- **2026-10 · [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](2026-2610.19605-pn-mix-pair-norm-guided-mixed-precision-key-cache-quantization-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クエリとキーの対ノルム積で重要な回転位置埋め込みチャネル対を入力処理時に一度だけ選び、3ビットと1ビットを配る混合精度キー量子化により、平均2.26ビットで従来方式以上の精度保持と、単一装置での実行可能範囲の拡大を示した。

- **2026-10 · [Persistent Memory in Multi-Agent LLM Inference: What It Costs, What It Buys, and When You Can Tell](2026-2610.07782-persistent-memory-in-multi-agent-llm-inference-what-it-costs-what-it-buy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント分解は最大KVを約6割減らすが、軌跡を保存する永続層は費用だけが測れて正解率の効果は検出できないことを実測し、その無効果がベンチマークの構造に由来することと消去実験の成立条件を示した測定研究。

- **2026-10 · [PeekKV: The First Content Token Already Knows Which Heads Matter](2026-2610.23939-peekkv-the-first-content-token-already-knows-which-heads-matter.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル直後の最初の内容トークン1つを観測して、ヘッドグループへの予算配分とトークン保持を入力ごとに決めるKVエビクション。プロファイルも学習も不要で、信号をプリフィルではなくデコード経路から取る。

- **2026-10 · [MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization](2026-2610.18642-multialloc-budget-aware-precision-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/RL-MIND/MultiAlloc) ・ リポジトリ内被引用：0  
  固定KVメモリ予算を層ごとのビット幅向上とトークンごとの高精度保持へ、オフラインプロファイルで測った需要に基づいて配分し、推論時は探索なしで静的方針を適用するKVキャッシュ量子化の配分枠組み。

- **2026-10 · [MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs](2026-2610.30206-moezip-routing-aware-kv-cache-compression-for-sparse-mixture-of-experts-.md)**  
  実装：[✓](https://github.com/kmswin1/MoEZip) ・ リポジトリ内被引用：0  
  KV削減でエキスパート選択が反転するMoE固有の失敗に対し、ルータのFisherトレースで脆さを測って保持予算の一部を保護用アンカーへ割り当て、強い圧縮でも品質を保つKV圧縮方式。

- **2026-10 · [MLAfication: Efficiently Enabling High-Fidelity MLA for Modern LLMs](2026-2610.17202-mlafication-efficiently-enabling-high-fidelity-mla-for-modern-llms.md)**  
  実装：[✓](https://github.com/JT-Ushio/MLAfication) ・ リポジトリ内被引用：0  
  多ヘッド潜在注意への変換を、キーの正規化の平均による較正と、触る射影だけの蒸留で、正規化つきモデルと混合専門家モデルへ広げ、品質を保ったままキャッシュ圧縮とサービング高速化を得る変換法。

- **2026-10 · [MemLLM: End-to-end In-Storage Acceleration of On-device Retrieval-Augmented Generation using Precomputed KV Caches](2026-2610.22579-memllm-end-to-end-in-storage-acceleration-of-on-device-retrieval-augment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事前計算ケーブイキャッシュの入出力の壁を、再計算から注意計算までをストレージ内で完結させる計算型ストレージで解き、端末の検索拡張生成をジーピーユー比で平均4.06倍に高速化した研究。

- **2026-10 · [MCF: A Memory- and Communication-Aware Co-Designed Framework for Long-Context LLM Inference](2026-2610.34731-mcf-a-memory-and-communication-aware-co-designed-framework-for-long-cont.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈並列のKV配置をプリフィルの段階に合わせて動的に変え、序盤は再利用の多いKVを複製して転送待ちを隠し、終盤は所有者だけの配置へ戻してデコードへそのまま渡すことで、長文脈プリフィルの遅延を下げる枠組みとそのFPGA実装。

- **2026-10 · [Low-Bit GDN Recurrent-State Quantization: Global Gradient-aware Allocation and Pure-Write Sliding Windows](2026-2610.39931-low-bit-gdn-recurrent-state-quantization-global-gradient-aware-allocatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  将来損失への勾配でヘッドへビットを配り直す配分と、直近の書き込みを高精度に別保持する窓の組合せで、再帰状態の平均4ビット量子化の課題平均を既存方式から最大41.2ポイント回復した。

- **2026-10 · [Local Inference of LLMs on Long Contexts: A Data Systems Perspective](2026-2610.28223-local-inference-of-llms-on-long-contexts-a-data-systems-perspective.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一ブロックのカーネル単位計測で、長文脈ローカル推論では注意が時間を支配するのにGPUを使い切れず最新GPUほど恩恵が薄いことを示し、並列化・ページング・融合・ストール削減の4提言を出した分析研究。

- **2026-10 · [Linear-Time Context Compression with State-Space Encoding](2026-2610.33006-linear-time-context-compression-with-state-space-encoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  状態空間モデルで文脈を線形時間に読みKVキャッシュへ注入するオンライン圧縮器で、従来のオフライン圧縮と同等以上の忠実度を、圧縮率16倍でもほぼ保ちながら、圧縮自体の遅延を1桁下げる手法。

- **2026-10 · [LearnPrunerV2: Learnable Progressive Token Pruning for Vision-Language Models](2026-2610.36986-learnprunerv2-learnable-progressive-token-pruning-for-vision-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全層に学習可能な枝刈りモジュールを入れ、シャドウトークンで集めたクエリ関連度と視覚的な顕著さを融合して視覚トークンを段階的に落とす方式で、77.8パーセント削減でも元の性能の99.8パーセントを保ち、層別予算を固定して遅延を決定論的にする。

- **2026-10 · [LatLM: Line-Parallel Language Models with Deferred Commitment](2026-2610.23951-latlm-line-parallel-language-models-with-deferred-commitment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テキストを2次元格子に置き、確定可能なフロンティアの中からエントロピーの低いセルだけを毎ラウンド確定し、前提が未生成のセルは待たせることで、行並列デコードの速度と依存箇所での正確さを両立させる方式。

- **2026-10 · [KVStream: Adaptive Parallel Storage Management for KV Caching in Large-Scale LLM Serving](2026-2610.31827-kvstream-adaptive-parallel-storage-management-for-kv-caching-in-large-sc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィックスKVの読み出しをNVMeと並列ファイルシステムの合計帯域で賄うため、各チャンクを全階層へ複製し、書き込みを遅延させ、空いた階層が未読チャンクを引き取る完了駆動ルーティングで静的分割の限界を回避し、上限の5パーセント以内で読み出すKVキャッシュエンジン。

- **2026-10 · [KVCompass: A Discovery Plane for Internet-Scale Prefix Cache Sharing in LLM Serving](2026-2610.24179-kvcompass-a-discovery-plane-for-internet-scale-prefix-cache-sharing-in-l.md)**  
  実装：[✓](https://github.com/011shiyiLing/KVCompass) ・ リポジトリ内被引用：0  
  KVキャッシュの同一性と配置を切り離し、鍵なし多段索引を全エッジへ複製してローカル参照し、遅延由来の一致長と負荷と距離の共同スコアで転送先を決める地域間接頭辞共有の発見プレーンで、99パーセンタイルの最初のトークンまでの時間を比較対象比1.3から14倍下げた。

- **2026-10 · [KV Cache Quantization for Diffusion Language Models](2026-2610.39853-kv-cache-quantization-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルのキャッシュ再利用では量子化前から誤差があることを示し、出現軌跡で較正してキー側の高精度枠を層ごとに選ぶことで、4ビットと2ビットの全設定で量子化比較法中最高の4課題平均を得た。

- **2026-10 · [Kernel-based Interpolatory Methods for Context Compression of Attention Mechanisms](2026-2610.40943-kernel-based-interpolatory-methods-for-context-compression-of-attention-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アテンションをカーネルのヒルベルト空間で線形写像の比として補間し、文脈を少数のノードと重みへ圧縮する2方式を提案した研究。25パーセント圧縮で無圧縮比87.1パーセントのタスク性能を保ったが、再構成誤差とタスク性能の不一致も明らかになった。

- **2026-10 · [JointServe: Serving Multi-Model Agents on Memory-Constrained GPUs](2026-2610.19822-jointserve-serving-multi-model-agents-on-memory-constrained-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの断片とKVブロックを1つのメモリ予算で競わせ、呼び出し意図の先読みと層単位の流し込みで複数モデルエージェントをメモリ制約GPUに載せるサービング基盤。

- **2026-10 · [InferOpt: Constrained Multi-Objective Search for LLM Inference Configurations](2026-2610.04473-inferopt-constrained-multi-objective-search-for-llm-inference-configurat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層ごとのKV保持率と専門家数を同じ探索の枠組みで扱い、固定した代理評価、予算超過の事前棄却、予算の段階的な引き締めで、品質と資源のパレートな設定群を効率よく探す手法。

- **2026-10 · [HAWK: Heterogeneity-Aware KV Cache Transfer for Efficient GPU-NPU Phase-Disaggregated LLM Inference](2026-2610.29873-hawk-heterogeneity-aware-kv-cache-transfer-for-efficient-gpu-npu-phase-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルをGPU、デコードをNPUに分ける異種分離型サービングのためのKV転送機構。共通のRDMA経路で直接転送し、テンソル配置の違いを転送前の部分変換とチャネル別バッファで転送中に吸収することで、GPU単独に迫る性能と高い電力・コスト効率を実機で示す。

- **2026-10 · [HaloBlock: Faster and Better Decoding for Diffusion Large Language Models](2026-2610.17948-haloblock-faster-and-better-decoding-for-diffusion-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルのブロック右側の難しさと境界の文脈不連続を、双方向累積エントロピーで測ってブロック両側へハローを適応的に足すことで緩和し、学習なしで正解率とスループットの両方を改善した研究。

- **2026-10 · [GAAC: Lossless KV Compression for Bandwidth-Efficient LLM Inference on Personal Devices](2026-2610.38210-gaac-lossless-kv-compression-for-bandwidth-efficient-llm-inference-on-pe.md)**  
  実装：[✓](https://github.com/Intelligent-Microsystems-Lab/GAAC) ・ リポジトリ内被引用：0  
  BF16の指数部が短い連続区間へ集中する性質を使い、KVをビット単位で無損失に約1.41倍圧縮し、復元を注意カーネルへ融合して読み出し帯域を減らすことで、個人向けデバイスの長文脈デコード注意とサービングを速める方式。

- **2026-10 · [FORGE: Procedural Weight Generation for Sparse MoE Inference](2026-2610.16890-forge-procedural-weight-generation-for-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎な混合専門家モデルのエキスパート重みを高帯域メモリから読む代わりに、ローターの種から専用回路でチップ上に再生成し、帯域律速の解消と容量の解放を精度との交換で得るハードウェア手法。

- **2026-10 · [FlatCake: A Flat KVCache Storage Architecture for LLM Serving](2026-2610.38355-flatcake-a-flat-kvcache-storage-architecture-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DRAMとSSDを階層でなく対等な媒体として扱い、KVブロックを生成時に最終媒体へ直接置いて移動させず、セッション連続・層優先の配置と直接読み込みで復元を連続化することで、階層型KV保存のヒット率崩壊とTTFT悪化を防ぐ方式。

- **2026-10 · [Few Bits, One Law: Toward W2A4KV2](2026-2610.09202-few-bits-one-law-toward-w2a4kv2.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定回転とエネルギー正規化で重み・活性値・KVキャッシュを正準座標へそろえ、凍結したガウス参照コードブックを使い回しながら共同で量子化認識学習するCanonQにより、W2A4KV2でパープレキシティを最大14.28倍下げた研究。

- **2026-10 · [FAD-KV: Adaptive Dictionary KV Caching for Efficient Reasoning Decoding](2026-2610.37921-fad-kv-adaptive-dictionary-kv-caching-for-efficient-reasoning-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVを学習済み辞書のアトムの疎な組合せで表す圧縮について、相関スコアで候補を絞る高速な符号化と、不活性アトムの置換だけで辞書を大きくしない適応を組み合わせ、符号化費用と辞書の際限ない増加を同時に抑える方式。

- **2026-10 · [Expanding Attention: A Taylor-Series Route to Linear-Time Transformers with a Fixed Number of Recurrent States](2026-2610.20637-expanding-attention-a-taylor-series-route-to-linear-time-transformers-wi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の指数カーネルをテイラー展開で打ち切りテンソル冪へ分解し、文脈長に依らない固定個数の再帰状態で線形時間の注意を構成する方式と、次数・状態幅・正規化のトレードオフの実測。

- **2026-10 · [Evaluating the Applicability of LLM Inference Optimizations on Apple Silicon](2026-2610.31479-evaluating-the-applicability-of-llm-inference-optimizations-on-apple-sil.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サーバーGPU向け推論最適化4群をApple Siliconへ移植して実測した評価。KVプルーニングは長文脈で最大1.75倍、投機的デコードは主要条件で全方式が悪化、量子化はデコードで最大74.9パーセント向上と、移植可能性が実行条件で大きく分かれることを示す。

- **2026-10 · [E8 Lattice Key Quantization for Low-Bit KV-Cache Compression](2026-2610.15384-e8-lattice-key-quantization-for-low-bit-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュのキーをE8格子の固定コードブックでベクトル量子化し、クエリとコードブックの内積表による非対称スコアリングで復号なしに注意を計算することで、キー2ビットでも品質を保ちKVを約6倍に圧縮する方式。

- **2026-10 · [DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction](2026-2610.22130-dropkv-decoupling-residual-output-perturbation-for-near-optimal-kv-cache.md)**  
  実装：[✓](https://github.com/AozhongZhang/DropKV) ・ リポジトリ内被引用：0  
  捨てたときの注意出力のずれをトークンごとに分離して測る採点でKVを追い出し、近似の保証と融合カーネルを備えて、予算5パーセントでも最高精度と最低遅延を両立した。

- **2026-10 · [Double KV Cache Optimization on Apple Silicon: Block-FP4, Radial Quantization, and Fused Metal Kernels](2026-2610.33076-double-kv-cache-optimization-on-apple-silicon-block-fp4-radial-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Apple Silicon上でKVキャッシュの4ビット表現とラジアル量子化とその逐次合成を実測比較し、融合カーネル化で中規模文脈の順位が逆転すること、合成の非加算性、長文脈での全量復元による崩壊を明らかにした研究。

- **2026-10 · [DeferKV: Rethinking Eviction Timing for One-Shot KV Cache Compression](2026-2610.06286-deferkv-rethinking-eviction-timing-for-one-shot-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVの一括エビクションをプリフィル直後から初回デコードの直後へ遅らせ、初回の実デコードクエリと直近のプロンプトクエリを時間重み付きで統合して残すトークンを決めることで、追加学習や将来予測なしに圧縮時の生成品質を高める方式。

- **2026-10 · [DCKV: Learned Transform Coding of the Prompt KV Cache in Hybrid Language Models](2026-2610.36950-dckv-learned-transform-coding-of-the-prompt-kv-cache-in-hybrid-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハイブリッドモデルの保存用プロンプトKVキャッシュを、共同基底の変換・学習した量子化・条件付きエントロピーモデルで符号化し、モデルの出力変化を歪みに学習することで、同等品質のバイト数を従来の変換符号化から6割以上削減した学習型コーデック。

- **2026-10 · [Context-Aware Precision Scheduling for Small Language Models](2026-2610.15640-context-aware-precision-scheduling-for-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈の伸びに合わせて重み精度を切り替えるスケジュールを事前計算し、KVキャッシュを保持したまま実行する手法。

- **2026-10 · [Context Is Not Free: Carbon-Aware LLM Routing for Multi-Turn LLM Web Services across Geo-Distributed Data Centers](2026-2610.35230-context-is-not-free-carbon-aware-llm-routing-for-multi-turn-llm-web-serv.md)**  
  実装：[✓](https://anonymous.4open.science/r/carbonrouter-artifact-00C6/) ・ リポジトリ内被引用：0  
  複数ターン会話の振り分けで、候補のモデル・GPU・地域のすべてに履歴再計算の炭素を課金し、次ターンで逆戻りしそうな切替をゲートで止めることで、キャッシュを壊す移動を避けて排出を減らす炭素配慮ルーティング方式。

- **2026-10 · [Compositional Performance Modeling of LLM Inference Clusters with Hierarchical KV Caching](2026-2610.15366-compositional-performance-modeling-of-llm-inference-clusters-with-hierar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  局所的な計算・転送費用とKVの所在・容量・準備状態を分離して離散イベントで合成する推論クラスタのシミュレータで、1P1D較正のモデルを他構成へ再利用し、階層型KVキャッシュ下の遅延と再利用を高精度に予測する研究。

- **2026-10 · [Can Agent Harnesses and Inference Engines Hear Each Other? The HEAR Protocol for Agentic LLM Serving](2026-2610.06597-can-agent-harnesses-and-inference-engines-hear-each-other-the-hear-proto.md)**  
  実装：[✓](https://anonymous.4open.science/r/hear-3D1E/) ・ リポジトリ内被引用：0  
  ハーネスのワークフロー意図とエンジンのキャッシュ・キュー状態を4分類メッセージで双方向に交換するHEARプロトコルを定め、同じ契約でキャッシュ協調スケジューリングと役割別実行モード選択を行い、対話と研究エージェントで高速化を得る研究。

- **2026-10 · [CacheSmith: Accurate RAG Serving under Latency SLOs with Adaptive KV Reuse](2026-2610.18925-cachesmith-accurate-rag-serving-under-latency-slos-with-adaptive-kv-reus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAGのKV再利用で失われる文書片間注意の再計算を、ウォームアップ・プローブ・パッチの3相で構成可能にし、品質ゲート付きSLO到達率を最大化するようバッチごとに信号と被覆率を適応させるサービング方式。

- **2026-10 · [Cache the Encoder Within:Compact, Reusable Memory across LLM Queries](2026-2610.10058-cache-the-encoder-within-compact-reusable-memory-across-llm-queries.md)**  
  実装：[✓](https://anonymous.4open.science/r/EncBank-1E15/) ・ リポジトリ内被引用：0  
  LLMの下位層を文書エンコーダーとして再利用し、分割境界の残差状態を低ビットで永続保存して適応済み上位層が読み直す方式を提案した研究。

- **2026-10 · [Budgeted KV-Cache Repair for Evolving Contexts](2026-2610.17338-budgeted-kv-cache-repair-for-evolving-contexts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  削除後に汚れたKVを、凍結埋め込みで選んだクエリ関連のテキスト領域だけ予算内で再計算して直す意味単位リフレッシュと、分散した修復を一回の走行で処理する層詰め実行器の提案。

- **2026-10 · [Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration](2026-2610.11214-bridging-kv-cache-quantization-and-linear-attention-from-theory-to-pretr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  離散アドレスへの軟割当がKV量子化と線形注意を一つの機構でつなぐことを証明し、その理論を足場に軟量子化中間モデル経由で事前学習済みTransformerの重みをRAM-Netへ移す移行手順を9モデルで実証した研究。

- **2026-10 · [BitNest: Bit-Nested Speculative Decoding for Memory-Efficient LLM Inference Acceleration](2026-2610.02800-bitnest-bit-nested-speculative-decoding-for-memory-efficient-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  強いW4ベースを先に固定し残差だけを4ビットで足してW8ターゲットを復元する入れ子表現により、別コピーなしでW4ドラフトとW8検証を単一の重みとKVキャッシュから読み分ける自己投機的デコード手法。

- **2026-10 · [Beyond Hotness: High-Resolution Memory Characterization of Cloud and LLM Workloads for Tiered Memory with ARM SPE](2026-2610.32711-beyond-hotness-high-resolution-memory-characterization-of-cloud-and-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プロセッサのサンプリング拡張でLLM推論を含む8ワークロードのメモリ挙動を細かく測り、遅延の集中とアイドル期間で階層メモリへの適性を判定した計測研究。

- **2026-10 · [BellowsKV: One Latent for Many Layers, Expanded on Demand](2026-2610.35023-bellowskv-one-latent-for-many-layers-expanded-on-demand.md)**  
  実装：[✓](https://github.com/MorrisZJ/BellowsKV) ・ リポジトリ内被引用：0  
  隣接層のキャッシュではなく隠れ状態を共有対象とし、n層ぶんの隠れ状態をトークンごとに1つの潜在へ畳んで次元を削らずに低ビット量子化とブロック単位エビクションで圧縮することで、13倍超でも精度保持率97パーセント台を保つ学習不要のKVキャッシュ圧縮方式。

- **2026-10 · [AvoKV-E: Payload-Aware KV Cache Eviction for Long Reasoning](2026-2610.03007-avokv-e-payload-aware-kv-cache-eviction-for-long-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長推論向けKVエビクションで、最近の状態は判定を遅らせて守り、古い候補は読み圧・キー冗長性・バリュー量を候補内順位で正規化して残す学習不要の方針。最も小さい予算で既存方針との差が最大になる。

- **2026-10 · [AttSVD: Prompt-Adaptive Low-Rank KV Cache Compression via Attention-Guided SVD](2026-2610.06927-attsvd-prompt-adaptive-low-rank-kv-cache-compression-via-attention-guide.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを捨てず、プロンプトごとにクエリ共分散と注意質量で重み付けした特異値分解の因子だけを保持し、生成の長さに応じて蓄積型とストリーミング型のデコードを使い分ける低ランクKVキャッシュ圧縮。

- **2026-10 · [Approximation Algorithms for Dual-Memory Request Scheduling in Disaggregated LLM Inference](2026-2610.15579-approximation-algorithms-for-dual-memory-request-scheduling-in-disaggreg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型推論のプリフィル側とデコード側の2つのメモリ容量を同時に扱う受付スケジューリング問題を定式化し、近似保証つきアルゴリズムを2つ与えた理論研究。

- **2026-10 · [AnchorKV: Lossless Key-Value Cache Reconstruction from Layer-Sparse Residual Anchors](2026-2611.00117-anchorkv-lossless-key-value-cache-reconstruction-from-layer-sparse-resid.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層方向に疎な残差アンカーだけを保存し、カスケード再生でKVキャッシュをビット単位で無損失に再構成することで、4k文脈の再構成を最大16.3倍高速化し、32k文脈で再活性化可能なセッション容量を全KVの5.78〜54.0倍にした、保存量と再生費用のスペクトラムを設計する方式。

- **2026-10 · [An Optical KV Cache Network for Disaggregated LLM Serving](2026-2610.18444-an-optical-kv-cache-network-for-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離サービングのKV転送専用に光回線交換網を用い、プリフィル中に回線を予約して機械式スイッチの再構成遅延を隠すことで、過剰予約パケット網より安く同等の応答性を得る網設計と予約方式。

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [vSkipper: Translating Dynamic Layer Skipping into LLM Serving Gains](2026-2609.37062-vskipper-translating-dynamic-layer-skipping-into-llm-serving-gains.md)**  
  実装：[✓](https://github.com/AKafakA/sglang-vskipper/tree/vskipper-ref) ・ リポジトリ内被引用：0  
  トークンごとの層スキップを、層ごとのKV書込みを保つ実行と射影のみの実行の2値インターフェースと、判断ごとのコホート実行、収益性による経路切替で、現代的なサービング基盤の利得へ変換する仮想化層。

- **2026-09 · [VestigeKV: The NoPE-MLA KV Cache Carries Its Own Eviction Signal in a Vestigial Branch](2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-eviction-signal-in-a-ves.md)**  
  実装：[✓](https://github.com/fan-wenjie/vestigekv) ・ リポジトリ内被引用：0  
  選ばれた行だけを毎回の注意計算へ送り、残りはビット列を変えずGPU内の退避領域へ保存する。著者の実装資料は、Kimi Linear 48B-A3Bを対象とした2台のRTX PRO 6000 Blackwellで、単一要求の連続復号において256K文脈で約1.28倍、496Kで約1.46倍の速度比を示す。

- **2026-09 · [ValueDiff: Value-Geometric KV Cache Eviction for Sink-Suppressed LLMs](2026-2609.23314-valuediff-value-geometric-kv-cache-eviction-for-sink-suppressed-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意シンクが弱い近年のモデルではバリュー側の幾何が安定した保持信号になるという観測に基づき、バリューベクトルとキャッシュ平均との距離でトークンを順位付ける、クエリ非依存のKVキャッシュエビクション方式。

- **2026-09 · [Validating Hybrid-State Cache Recovery for GLM-5.3-Flash with vLLM and LMCache](2026-2609.15030-validating-hybrid-state-cache-recovery-for-glm-5-3-flash-with-vllm-and-lmcache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GLM-5.3-Flash＋vLLM＋LMCacheの完全キャッシュヒット境界ずれを厳密プレフィックス復旧で修正し、出力同一性を保ったCPUキャッシュ再ロードのTTFT短縮を実証。

- **2026-09 · [Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management](2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-mana.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Unified AI Gatewayは、複数の大規模言語モデルを使い分ける推論サービスにおいて、モデルを切り替えるたびに鍵値キャッシュ（KVキャッシュ）が使えなくなり、長い入力を最初から処理し直す問題を扱う。モデル切替確率を変えた条件で、初回トークン時間の代理指標は1.25〜13.28倍、入力費用は1.20〜6.16倍改善する余地があると報告する。

- **2026-09 · [TRACE: Trajectory-robust Admission with Evidence Ordering for Efficient GUI Agents](2026-2609.10297-trace-trajectory-robust-admission-with-evidence-ordering-for-efficient-g.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キャッシュ再利用下の視覚枝刈りを不可逆な受入れと捉え、レイアウト事前分布・指示関連度・特徴新規性を入れ子順序へ統合し、被覆修復と単調なKV縮約を組み合わせて、厳しい予算でもGUIエージェントの精度と初回応答を両立した。

- **2026-09 · [To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems](2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-.md)**  
  実装：[✓](https://github.com/FastLM/KVLearn) ・ リポジトリ内被引用：0  
  大規模言語モデルの推論を、入力を一括処理するプリフィル（プリフィル）ノードと、生成を継続する復号（デコード）ノードへ分離すると、キー・バリューキャッシュ（KV キャッシュ）の価値は単なる「最後に使われた時刻」では決まらなくなる。

- **2026-09 · [The KV Cache Is the New Memory Wall](2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しいKV圧縮器やGPUカーネルの実装ではなく、既存研究が異なる条件で報告してきた改善率を解釈するための分析枠組みを作る。例えばLlama-3-70BをBF16で扱う場合、重みは約140GB、1系列128kトークンのKVは約42GBである。

- **2026-09 · [The Extender: A Log-Structured Transformer](2026-2609.32759-the-extender-a-log-structured-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  次のトークン予測用の残差とは別に、各層が32次元だけを末尾へ連結する追加専用の経路を注意専用に設け、全層で共有する1本のキャッシュへ注意入力を集約して、持続注意メモリを最大104倍削減した変換器の変種。

- **2026-09 · [Tessera: Demand-Driven KV Cache Management for Retrieval-Augmented LLM Serving](2026-2609.32999-tessera-demand-driven-kv-cache-management-for-retrieval-augmented-llm-se.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索結果を単なるLLMへの入力ではなく、キャッシュの将来需要を示す制御信号として扱い、検索履歴、KV配置、生成ノード負荷を一体で用いてキャッシュ採否・退避・要求ルーティングを計画する。

- **2026-09 · [TempoKV: Timely Staging of LLM KV Caches for Memory-Semantic Flash](2026-2609.35065-tempokv-timely-staging-of-llm-kv-caches-for-memory-semantic-flash.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TempoKVは、過去の要求で計算済みの接頭辞キー・バリュー（KV）キャッシュを、SSDを背後に持つ大容量メモリ階層から再利用する際、再利用が分かった時点で高速メモリを確保しないという設計を導入する。vLLMとLMCacheを拡張したH100実機評価では、即時予約と比べて保護容量時間を63～91%削減した。

- **2026-09 · [StepKV: Step-Aware KV Cache Compression for LLM Agents](2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの自己回帰生成では、過去トークンの鍵と値を保存する鍵値キャッシュ（KVキャッシュ）が、次トークンの注意計算で過去の隠れ状態を再計算せずに済ませる。キャッシュ圧縮で一部のトークンを捨てると容量を減らせるが、注意重みが小さいトークンが将来も不要であるとは限らない。

- **2026-09 · [Shared-Prefix KV Reuse Across Standard LoRA Adapters: Quality and Serving Tradeoffs](2026-2609.17109-shared-prefix-kv-reuse-across-standard-lora-adapters-quality-and-serving-tradeoffs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既学習の標準LoRA間で基盤モデル接頭辞KVを直接再利用し、8K暖機済み初回トークン時間約16倍と小さいが不確実な品質低下、物理共有未実装という実運用上の境界を測定する。

- **2026-09 · [Shared KV Caching for Replicated 27B Inference: Correctness Failures and Performance Boundaries](2026-2609.15021-shared-kv-caching-replicated-27b-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュのページ表現・CUDAストリーム順序・全容量ピン留めを段階検証し、レプリカ移動時だけ大きな長文プリフィル再利用効果が得られる境界を実測する。

- **2026-09 · [SGD-KV: Summarization Guided KV Cache Compression](2026-2609.03235-sgd-kv-summarization-guided-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SGD-KVは、要点抽出へ寄与する注意ヘッドを事前診断し、ヘッド別KV容量へ変換して、長文の意味集約に必要な履歴を優先保持する。

- **2026-09 · [Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context Window Size](2026-2609.12686-residual-vector-long-context-recall.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文書を事実単位の外部残差ベクトルへ変換し、質問時にFFN活性で選択注入して元トークン/KVなしに事実を再構成することで、文書長にほぼ依存しないGPU記憶量で長文脈recallを実現する。

- **2026-09 · [Quality Recovery for Quantized KV Caches via Low-Rank Attention Adaptation](2026-2609.04263-quality-recovery-for-quantized-kv-caches-via-low-rank-attention-adaptati.md)**  
  実装：[✓](https://github.com/saifmb0/kvlora) ・ リポジトリ内被引用：0  
  キャッシュを4ビットや2ビットに量子化すれば保存量を減らせるが、量子化誤差が注意出力を変え、パープレキシティや長文脈検索の品質を落とす。

- **2026-09 · [Prefix Sharing Is a Sorting Problem](2026-2609.13692-prefix-sharing-sorting-problem.md)**  
  実装：[✓](https://github.com/Darrenus/prefix-sharing-is-sorting) ・ リポジトリ内被引用：0  
  入力部品の並びと要求処理順を階層的に最適化し、既存の先頭キャッシュを変更せず実検索データで先頭共有を増やして事前計算量を17〜36%削減する。

- **2026-09 · [PReCache: Efficient KV Cache Sharing for Multi-LoRA Agents via Low-Rank Precomputation and Neutral Reconstruction](2026-2609.34054-precache-efficient-kv-cache-sharing-for-multi-lora-agents-via-low-rank-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有軌跡が初めて処理される時点で全エージェント分の低ランクキャッシュを事前計算し、さらにアダプターなしの隠れ状態から基底キャッシュを再構成することで、繰り返しプリフィルを消しながら精度低下を平均1.1ポイントに抑える学習不要のKVキャッシュ共有方式。

- **2026-09 · [One Distribution, Two Channels: Coverage-Calibrated KV Retention and Compensation](2026-2610.02235-one-distribution-two-channels-coverage-calibrated-kv-retention-and-compe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈推論ではKVキャッシュがメモリ容量と読み出し帯域を圧迫する。トークンを単純に重要度順で保持する方式では、重要度の高いトークンが互いに似ている場合に貴重な保持枠を浪費する。RULERでは90% KV圧縮時に最良比較方式を平均2.25ポイント、最大3.78ポイント上回り、複数回の再圧縮やLongBenchでも優位性を報告する。

- **2026-09 · [OmniKVQuant: KV Cache Quantization for Omni-LLMs](2026-2609.11582-omnikvquant-kv-cache-quantization-for-omni-llms.md)**  
  実装：[✓](https://github.com/kaistmm/OmniKVQuant) ・ リポジトリ内被引用：0  
  全モダリティ大規模言語モデルのKVキャッシュに対し、32トークン局所範囲でキー量子化を適応し、モダリティ別回転でバリューを2ビット化して品質劣化を抑える学習不要方式。

- **2026-09 · [MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference](2026-2609.07966-metakv-adaptive-kv-cache-compression-for-constrained-llm-inference.md)**  
  実装：[✓](https://github.com/MichaelWang0505/MetaKV.git) ・ リポジトリ内被引用：0  
  MetaKVは、プロンプトと遅延・KVメモリ制約から候補圧縮方式の結果を予測し、制約内で正答率を保つ設定をリクエストごとに切り替える。

- **2026-09 · [MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators](2026-2609.19207-meshkv-a-network-on-chip-kv-cache-fabric-for-scalable-transformer-decoding-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  鍵値キャッシュをオンチップ網の分散流へ変換し、8×8 FPGA実装で通信量最大58%削減、鍵値帯域利用率2.1倍、生成処理量最大1.90倍を実測する。

- **2026-09 · [Memory as a Cache: Exact Context Reuse and Deletion by Construction](2026-2609.32395-memory-as-a-cache-exact-context-reuse-and-deletion-by-construction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈をブロックごとに独立符号化したメモリ行の集合として保持し、生成はその和集合へのクロスアテンションで条件付けることで、接頭辞共有に限られていたKV再利用を任意のブロックの厳密な合成と削除へ広げるアーキテクチャ。

- **2026-09 · [MCPO: Modality-Contrastive Preference Optimization for Multimodal Chain-of-Thought Compression](2026-2609.04947-mcpo-modality-contrastive-preference-optimization-for-multimodal-chain-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考連鎖の各ステップの視覚依存度を画像ありと画像なしの尤度差で測って視覚に依存しないステップを枝刈りし、画像ありと画像なしで勾配の急さが異なる非対称な選好損失で短く視覚に根ざした推論様式を学習させる、マルチモーダル思考連鎖の二段階圧縮手法。

- **2026-09 · [Learning to Predict Middle-Layer Attention in MLLMs for Visual Token Pruning](2026-2608.06411-learning-to-predict-middle-layer-attention-in-mllms-for-visual-token-pru.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問に最も応答する中間層はサンプルごとに異なるため、質問対照で選んだ教師層の注意を言語モデル処理前に動く軽量予測器へ蒸留し、注意マップなしで視覚トークンの5.56%まで削って性能の97.5%を保持した研究。

- **2026-09 · [Learning Functional Subspaces for Neural Network Compression](2026-2609.40127-learning-functional-subspaces-for-neural-network-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  捨てる部分空間を層ごとの閉形式基準ではなく、出力分布へのKLで全層の直交射影をエンドツーエンドに学習して決める低ランク圧縮法で、注意では共有潜在だけをキャッシュしてKVキャッシュも細らせる。

- **2026-09 · [LatentPort: Beyond KV Cache - Cross-Model Transfer of Recurrent Memory in Hybrid Language Models: A 4B-to-9B Hybrid-State Handoff Without Target Prefix Replay](2026-2609.25053-latentport-beyond-kv-cache-cross-model-transfer-of-recurrent-memory-in-h.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意KVに加えて再帰層の持続状態パッケージまでを4Bから9Bへ移し、接頭辞を再処理せずに本来の9Bの文脈利益の91.8パーセントを回復した、ハイブリッドモデル間の状態引継ぎの実証研究。

- **2026-09 · [KVFetch: Temporal Prefetching for the Missing Half of KV Cache Compression](2026-2610.08811-kvfetch-temporal-prefetching-for-the-missing-half-of-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  内容ではなく位置で思い出す低温層と読みポインタによる先読みで、KV圧縮で途切れる逐語複写を同一予算のまま0.8から78.4へ回復させる学習不要の枠組み。

- **2026-09 · [KV-Lingo: Learning KV-Cache Translators with Distillation](2026-2609.32610-kv-lingo-learning-kv-cache-translators-with-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル間で互換性のないKVキャッシュを、層ごとの線形写像と自己蒸留で学んだ変換器で翻訳し、モデル切替時の再プリフィルを不要にして最初のトークンまでの時間を最大29倍短縮した。

- **2026-09 · [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jacapは、将来クエリへの注意出力感度と値方向の重複を測り、重要度だけでなく情報の多様性を持つKV集合を選んで、高圧縮時の出力情報欠落を減らす。

- **2026-09 · [Intra-Prompt Parallel Decoding for Common-Context Question Answering](2026-2609.05707-intra-prompt-parallel-decoding-for-common-context-question-answering.md)**  
  実装：[✓](https://github.com/networkslab/IPPD) ・ リポジトリ内被引用：0  
  共通文脈と複数質問を一つのプロンプトへ積み重ね、仮想位置とマスクで分離したまま全質問の次トークンを並行生成する推論方式で、品質を保ったまま標準バッチ推論の最大7倍級のスループットを得た。

- **2026-09 · [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeadWiseKVは、全体注意層のKV履歴を物理KVヘッドごとに較正し、必要な窓だけGPUへ確保して、長文脈の過剰メモリと一律圧縮による品質低下を抑える。

- **2026-09 · [HeadGuard: Selective Head Protection for Low-Bit VLM KV-Cache Quantization](2026-2609.35800-headguard-selective-head-protection-for-low-bit-vlm-kv-cache-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キャッシュを一様に2～3ビットへ量子化すると容量は小さくなるが、視覚情報に強く依存するヘッドの表現まで丸められ、画像質問応答や選択問題の正答率が急落する場合がある。

- **2026-09 · [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GrowPageは、生成中の注意参照範囲を短期・長期信号で予測し、容量境界で圧縮継続かKVページ追加かを選んで、推論ごとの過剰予約と必要履歴の削除を抑える。

- **2026-09 · [Freeze the Decoder, Heal the Encoder: Parameter-Efficient Adaptation for SVD-Based KV-Cache Compression](2026-2610.10552-freeze-the-decoder-heal-the-encoder-parameter-efficient-adaptation-for-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SVDによるKVキャッシュ圧縮の回復学習で、デコーダーを凍結しエンコーダーだけを学習しても、学習率を条件ごとに調整すれば全学習と同精度になることを示し、学習可能パラメータと最適化器メモリを3分の1にする実証と、共有学習率比較の落とし穴の記録。

- **2026-09 · [Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs](2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Flash-dLLM) ・ リポジトリ内被引用：0  
  拡散言語モデルの鍵・値キャッシュ更新を融合注意へ統合し、同じモデルによる下書き・検証型並列復号を重ねることで、メモリ入出力と反復回数を同時に削減する。

- **2026-09 · [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](2026-2609.09768-kv-concatenation-aware-recompute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV連結対応学習とCacheBlendの選択的再計算を組み合わせ、文書間相互作用の欠落を15%再計算で補い、RAG長文の品質とSSD読出し・転送待ちを両立する。

- **2026-09 · [FastGuide: Accelerating Reward Guidance for Diffusion Large Language Models](2026-2609.36202-fastguide-accelerating-reward-guidance-for-diffusion-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  報酬ガイダンスのベクトルは候補群で使い回し、拡散モデルのロジットは疎な再計算で開示ごとに更新し、低信頼の候補は保留することで、逐次ガイダンスを最大4.4倍高速化するハイブリッドデコード。

- **2026-09 · [ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics](2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コサイン類似度だけでは見落とすKV表現の大きさをユークリッド距離で補い、注意ヘッドごとの冗長度に応じて多様性と重要度を混合し、狭いKV予算で保持トークンを改善する方式。

- **2026-09 · [DPS: Dual-Mode Precision LLM Serving with Semi-Unified Memory](2026-2609.34380-dps-dual-mode-precision-llm-serving-with-semi-unified-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV圧力が高いときだけ入れ子型の低精度実行へ切り替え、残差の重みメモリをKVブロックへ転用することで、バースト時のプリエンプションとSLO違反を抑える二重精度サービング方式。

- **2026-09 · [Divergence Timing and Cumulative Disagreement under KV-Cache Eviction](2026-2609.16617-divergence-timing-and-cumulative-disagreement-under-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文はKVキャッシュ削除の新しい実装を提案するのではなく、削除したときに生成結果がどのように参照モデルから離れていくかを測る理論と実験を提示する。Llama-3.1-8B-InstructとQwen2.5-7B-Instructで、SnapKVによる50%保持は同予算の直近トークン保持やSnapKV-512より遅く・少なく分岐した。

- **2026-09 · [Distance-KV: Exploiting Relative Distance for Efficient Long-Context Inference](2026-2609.32663-distance-kv-exploiting-relative-distance-for-efficient-long-context-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  復号時の注意演算は過去のKVを繰り返し参照するため、メモリ容量と帯域がボトルネックになる。既存の圧縮方式には、最近のトークンだけを残す方式、注意重みで重要トークンを選ぶ方式、層や注意ヘッドごとに異なる保持予算を割り当てる方式がある。

- **2026-09 · [CoVeR: Coverage-Based Token Pruning for Multi-View 3D Reasoning in VLMs](2026-2609.08345-cover-coverage-based-token-pruning-for-multi-view-3d-reasoning-in-vlms.md)**  
  実装：[✓](https://humansensinglab.github.io/CoVeR) ・ リポジトリ内被引用：0  
  多視点3D推論の視覚トークンを、注意や特徴を使わず3次元座標の空間被覆だけで選ぶ学習不要の枝刈り。場面適応ボクセル化で粗い被覆を作り、最遠点サンプリングで予算ちょうどまで埋めることで、ボクセル化の飽和と学習型重要度の重複選択を同時に解く。

- **2026-09 · [Compressing Long Context into Answer-Aligned Memory Embeddings for LLM Inference](2026-2609.25537-cmc.md)**  
  実装：[✓](https://github.com/mostafiz26/CMC) ・ リポジトリ内被引用：0  
  CMC（Context-to-Answer-Aligned メモリ Compression）は、長文を少数の連続的な文脈記憶埋め込み（Context メモリ Embeddings、CME）へ変換し、質問に関連する記憶と原文の局所窓を組み合わせて凍結したデコーダへ渡す方式である。

- **2026-09 · [Capture the lifecycle: KV Cache management in ReAct Agents with KVTether](2026-2609.39819-capture-the-lifecycle-kv-cache-management-in-react-agents-with-kvtether.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント実行基盤のメッセージ操作から文脈のライフサイクルを捉えてKVの状態管理へ変換し、死んだKVの即時回収と待機中KVの保護で、ReActエージェントの遅延と費用を大きく下げた。

- **2026-09 · [CacheRepair: Learning to Repair Cross-Chunk Context in RAG for KV Cache Fusion](2026-2609.35139-cacherepair-learning-to-repair-cross-chunk-context-in-rag-for-kv-cache-f.md)**  
  実装：[✓](https://github.com/genglinWang/CacheRepair-code) ・ リポジトリ内被引用：0  
  CacheRepairは、複数の検索文書を使うRetrieval-Augmented Generation（RAG）で、文書ごとに独立に計算したKVキャッシュを再利用するときの品質劣化を、軽量な修復ネットワークで補う方式である。

- **2026-09 · [Beyond Mean Attention: Diversity-Aware, Layer-Wise Scoring for KV Cache Eviction](2026-2609.30738-beyond-mean-attention-diversity-aware-layer-wise-scoring-for-kv-cache-ev.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特に文章中の指定箇所を探すpassage-retrievalでは、層の途中から冗長性の係数を負から正へ切り替える設定で60.60から70.17へ上昇した。

- **2026-09 · [ARM: Attention with Routed-Memory for Learnable Sparse Control](2026-2609.24417-arm-attention-routed-memory-learnable-sparse-control.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  増え続けるKVキャッシュを固定数256スロットの階層メモリへ置き換え、書込み先と混合率、さらに読み出すメモリ量まで学習する。Llama-3.1-8Bで128Kまで動作し、RULER平均15.12を報告する。

- **2026-09 · [A Survey of Inference Processing Units for Large Language Model Inference: Chips, Systems, Algorithms, and Paradigms (2024–2026)](2026-f8b8eb9da2fe-a-survey-of-inference-processing-units-for-large-language-model-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  21ページのサーベイは、(1)チップ層、(2)サービングシステム層、(3)アルゴリズム層、(4)推論パラダイム層の四つを区別し、2024～2026年の主要研究・製品・ベンチマークを配置する。

- **2026-08 · [WnW: Waxing-and-Waning KV Cache for Long-Form Speech LLMs](2026-2608.22704-wnw-waxing-and-waning-kv-cache-for-long-form-speech-llms.md)**  
  実装：[✓](https://github.com/XMUDeepLIT/WnW) ・ リポジトリ内被引用：0  
  従来のKV圧縮は、プリフィル時の注意スコアで重要な音声位置を選び、残りを削除したままデコードを続ける。Voxtral-mini-3bのLibriSpeech-LongでGPU上の音声KV保持率が約22%のとき、WnWのWERはtest-clean 6.23、test-other 8.87で、無圧縮の6.79、8.86に近い。

- **2026-08 · [VisCache: Visual KV Cache Pruning for Efficient Vision Large Language Model Inference](2026-2608.24063-viscache-visual-kv-cache-pruning-for-efficient-vision-large-language-mod.md)**  
  実装：[✓](https://github.com/Wlklk/VisCache) ・ リポジトリ内被引用：0  
  前段で質問に関係する多様なフレームを残し、後段で層ごとの重要度と鍵・値の役割の違いを利用して圧縮する。論文の試作では、Qwen2.5-VLの3Bと32Bを使い、視覚KVの保持率28%で複数の動画理解課題の平均精度を比較方式より高く保ち、保持率19%でも大きく破綻しない結果を示す。

- **2026-08 · [Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction](2026-2608.23296-sigmoid-attention-as-a-better-substrate-for-learned-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/IsaacLi74/sigmoid-kv-eviction) ・ リポジトリ内被引用：0  
  本研究は、学習時に連続値で表現したトークン保持ゲートを、推論時に鍵・値キャッシュ（Key-Value Cache、KVキャッシュ）の実際の削除へ変換するとき、注意重みの正規化方式が結果を左右することを示す。

- **2026-08 · [SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference](2026-2608.28911-semkv-semantic-mixed-precision-kv-cache-quantization-guided-by-the-quali.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重要度の低いトークンを消す方式も、長文脈の回答に必要な証拠を失う恐れがある。SemKVは境界より安全側の2.322ビットと2.585ビットをトークンごとに混ぜ、平均2.39コードビット、充填とメタデータを含む実効2.65ビットで、FP16比6.0倍のKV保存量削減を実測した。

- **2026-08 · [S$^4$R: Selective Sampling, Subspaces, and Sparse Reconstruction for Compressed Long-Context KV Caching](2026-2608.00528-s-4-r-selective-sampling-subspaces-and-sparse-reconstruction-for-compres.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  S4R（Selective Sampling, Subspaces, and Sparse Reconstruction）は、長文脈言語モデルのキー・値（KV）キャッシュを低ランク係数として保持し、復号時には注意計算に重要な位置だけを元の次元へ戻す方式である。RULERで2.5倍圧縮時の平均は93.61、非圧縮93.97、xKV 93.47である。

- **2026-08 · [RippleKV: Cross-Layer KV Cache Allocation via Perturbation Propagation](2026-2608.08684-ripplekv-cross-layer-kv-cache-allocation-via-perturbation-propagation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈長が長くなるほどKVキャッシュは大きくなり、GPUメモリを占有するだけでなく、生成時に参照するメモリ量も増える。一方で同じ数を全層に配れば、生成結果を強く左右する層が過度に圧縮され、圧縮に強い層にメモリが余る可能性がある。

- **2026-08 · [Retrofitting Linear Attention into Diffusion Language Models](2026-2608.06628-retrofitting-linear-attention-into-diffusion-language-models.md)**  
  実装：[✓](https://github.com/Diuven/LLaDA-Hybrid) ・ リポジトリ内被引用：0  
  拡散言語モデルの確定済みブロックへの注意を固定サイズの再帰状態で読むブロックハイブリッド注意を提案し、学習済みモデルの6層だけを2段階の軽量な追加学習で線形注意化して、品質を概ね保ちながらデコードを最大1.73倍高速化した研究。

- **2026-08 · [PuzzleKV: Page-Wise Low-Rank Decomposition for KV Cache Compression](2026-2608.23843-puzzlekv-page-wise-low-rank-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PagedAttentionの固定長ページごとにKVを独立低ランク分解し、密ページと因子化ページを復元なしで同時に注意計算することで、学習不要のままKV容量を約60%へ削減する。

- **2026-08 · [PatchKV: Efficient KV Cache Recovery for Dynamically Edited LLM Contexts](2026-2609.26219-patchkv-efficient-kv-cache-recovery-for-dynamically-edited-llm-contexts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純な接頭辞キャッシュでは最初の不一致以降を全再計算し、無条件再利用では古い因果状態を持ち込むという二者択一になる。編集位置からの距離に基づく局所的な修復範囲、過去に収集した注意重みから見つける遠方の重要ブロック、保存時に決めたブロック別の量子化精度を組み合わせる。

- **2026-08 · [Parser Transitions Already Reveal Structural Responsibility: KV Persistence for Structured Generation](2026-2608.28276-parser-transitions-already-reveal-structural-responsibility-kv-persisten.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMエージェントが関数呼出し、JSON、SQLなどの構造化出力を生成する時、制約付きデコーダはパーサ状態を管理し、文法的に合法な次トークンだけを許可する。KVキャッシュを圧縮すると、注意スコア上は重要に見えないが構造上の役割を持つトークンの履歴が失われ、合法だが誤った出力になる可能性がある。

- **2026-08 · [PAGE: Partition-Aware Gated KV-Cache Eviction](2026-2609.22157-page-partition-aware-gated-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/pankajkumar6002/PAGE) ・ リポジトリ内被引用：0  
  値が大きければ注意希釈型と見なして既存の退避器を起動し、小さければ容量律速型と見なして全キャッシュを保持する。Mistral-7Bの精密な複数鍵検索では、通常のSnapKVの正答率が99%から0%へ崩れる保持予算でも、PAGEを併用すると89%を保った。

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

- **2026-08 · [MoNe: Modular Neural Memory for Efficient Long Context Inference](2026-2608.17616-mone-modular-neural-memory-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結したトランスフォーマーの各層へ高速重みニューラルメモリを付け、文脈を固定長セグメントごとにテスト時学習で書き込み、推論時は質問だけからメモリトークンを生成して文脈を読み直さないことで、128K文脈の計算とピークGPUメモリを文脈内学習比で約80パーセント削減した研究。

- **2026-08 · [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](2026-2608.02515-livemem-maintaining-memory-state-continuity-in-long-running-llm-inferenc.md)**  
  実装：[✓](https://github.com/cafeii/LiveMem) ・ リポジトリ内被引用：0  
  長時間稼働する対話支援や自律エージェントでは、対話履歴がモデルの注意機構（注意機構）の文脈窓を超える。Qwen3-4Bを基盤とする制限文脈の実験では、教師あり微調整と強化学習を経たLiveMemの全課題総合スコアが0.519で、基盤モデルの0.458を上回る。

- **2026-08 · [ImpactHO: Importance-Aware KV Cache Transfer for Multi-User Edge LLM Handover](2026-2608.10545-impactho-importance-aware-kv-cache-transfer-for-multi-user-edge-llm-hand.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  元の入力文字列だけを送れば転送量は小さいが、移動先で全履歴を再度事前処理しなければならない。一方、KVキャッシュを丸ごと転送すると再計算は避けられるが、複数利用者の移動が重なるとノード間回線が詰まる。転送が途中で切れても、届いた上位要素を使って推論を再開できる「途中再開可能性」が中心的な設計である。

- **2026-08 · [HyQuant: Hybrid-Precision Quantization for LLM Attention](2026-2608.27875-hyquant-hybrid-precision-quantization-for-llm-attention.md)**  
  実装：[✓](https://github.com/jerrysfls/HyQuant) ・ リポジトリ内被引用：0  
  注意質量が集中する縦線位置と直近窓だけを全精度に残し残りを4ビット化する混合精度量子化を提案し、長さ32768で生成核3.58倍・生成全体1.17倍の高速化と全精度に近い長文脈精度を示した。

- **2026-08 · [Faithfulness Is Not Free: Auditing Offline KV-Cache Quantization in Retrieval-Augmented Generation](2026-2608.30996-faithfulness-is-not-free-auditing-offline-kv-cache-quantization-in-retri.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインKVキャッシュ量子化を正確さと忠実さの両面で監査し、4ビットでは正解のまま根拠への裏付けが静かに失われ、正確さだけの評価では検出できないことを示す研究。

- **2026-08 · [Entropy-Constrained Adaptive Stochastic Quantization](2026-2608.18147-entropy-constrained-adaptive-stochastic-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  listsummary と同じ一覧専用解説。ECASQは値ごとに適応する不偏確率量子化で、誤差と後段のエントロピー符号化後の平均ビット量を共同最適化する。実モデルのKVテンソルでも比較し、近似法は厳密法に近い誤差を保ちながら解法処理を高速化する。

- **2026-08 · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](2026-2608.08878-distillcache-kl-guided-adaptive-kv-cache-eviction-for-memory-efficient-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著表1によると、Mistral-7B-Instruct-v0.3のLongBenchで完全キャッシュ41.5に対して、25%予算の提案法は39.1±1.1（完全版の94.2%）を得る。

- **2026-08 · [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](2026-2608.07458-coinrag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongBenchのHotpotQA、2WikiMQA、MuSiQueを対象に、初回トークン時間（Time to First Token、TTFT）の99パーセンタイルを100ミリ秒以内に制限した条件で、最良比較方式TurboRAGの3課題平均F1=39.6に対して41.7を報告する。

- **2026-08 · [CHIPSMORE: Compute-in-Interconnect and -Memory Chiplets for Multi-Mode Multi-Request LLM Inference Acceleration](2026-2608.30509-chipsmore-compute-in-interconnect-and-memory-chiplets-for-multi-mode-mul.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの持続性で計算場所を分け、キー・バリュー保存を三層で組み替え、重みを複製せず複数リクエストを層パイプラインへ流すことで、適応あり・長文脈・多重実行を1つの計算インメモリ加速器で支える方式。

- **2026-08 · [Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects](2026-2608.30076-budget-aware-compression-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み量子化・層削減・鍵値キャッシュ圧縮の相互作用を三予算で評価し、七百億モデルを約三十三ギガバイトへ縮小して単一A40・一万トークン入力で約五十七トークン毎秒を実現する。

- **2026-08 · [A Probabilistic Interpretation of KV Cache Eviction](2026-2608.28293-a-probabilistic-interpretation-of-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV追放を期待値推定として定式化し、確率的追放＋復号時重要度補正で既存top-kのバイアスを抑えタスク間頑健性を高める。

- **2026-07 · [VarRate: Training-Free Variable-Rate KV Cache Compression for Long-Context LLMs](2026-2607.15498-varrate-training-free-variable-rate-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを削除せず、注意顕著度に応じて各トークンの低ランク表現へ可変容量を配る学習不要KV圧縮で、20%メモリ予算でもLongBench平均を非圧縮から0.8点以内に保ち、再利用時の不可逆削除崩壊を抑える。

- **2026-07 · [SLIM: Saturation-Aware Lightweight Performance Modeling for LLM Serving](2026-2607.29575-slim-saturation-aware-lightweight-performance-modeling-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スループット飽和の原因がデコード注意の帯域飽和であることを実測で特定し、半解析の予測モデルとバッチ構成の助言器で、予測誤差の大幅削減と最大55ギガバイトのメモリ削減余地を示した。

- **2026-07 · [SALT: Salience-Aware Lexical Trie for Long-Context Compression](2026-2607.17486-salt-salience-aware-lexical-trie-for-long-context-compression.md)**  
  実装：[✓](https://github.com/oteomamo/SALT) ・ リポジトリ内被引用：0  
  長文脈圧縮で文のスカラー順位付けをやめ、文頻度順のキーワードトライへ予算を主題枝ごとに配分する方式を提案し、主題の潰れを防ぎながら前処理方式最良の精度と複数ターンでの費用削減を示した研究。

- **2026-07 · [Remembering Distinct Items, Not Tokens: A Learnable Dirichlet-Process Cache Between State-Space Models and Attention](2026-2607.09889-remembering-distinct-items-not-tokens-a-learnable-dirichlet-process-cach.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新規な入力にだけスロットを開くDP-means型の割当をキーとバリューのキャッシュ自体にし、キャッシュ量をトークン数ではなく相異なる項目数へ比例させることで、全注意と同じ想起を冗長度4で4分の1のスロットで達成し、固定状態モデルと全注意の中間領域を機構実験で示した研究。

- **2026-07 · [ReFreeKV: Towards Threshold-Free KV Cache Compression](2026-2502.16886-refreekv-towards-threshold-free-kv-cache-compression.md)**  
  実装：[✓](https://github.com/Patrick-Ni/ReFreeKV) ・ リポジトリ内被引用：0  
  長い入力を処理したLLMは、デコード中に過去のトークンへ注意するため、各層のKeyとValueをKVキャッシュとして保持する。H2O、SnapKV、StreamingLLMなどは重要とみなした位置だけを残すが、通常は「入力の何%を保持するか」または「何トークン残すか」を先に決める。ReFreeKVは、保持率ではなく注意行列のノルム変化を停止条件にする。

- **2026-07 · [Question Tells You Where the Answer Is: Intention-aware Long-Context KV Cache Compression](2026-3562943b0724-question-tells-you-where-the-answer-is-intention-aware-long-context-kv-c.md)**  
  実装：[✓](https://github.com/linkezh/IntentKV) ・ リポジトリ内被引用：0  
  IntentKVは、長文脈推論のプリフィル段階で作られたKey/Value（KV）を、後続の生成にとって重要な文脈に絞って保持する方式である。128K入力・保持容量2048の効率評価では、復号遅延はFullKVの16%、KVキャッシュメモリは13%と報告する。

- **2026-07 · [PReM: Learning What to Preserve and When to Refresh for Context Compression](2026-2607.14327-prem-learning-what-to-preserve-and-when-to-refresh-for-context-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈を層別KV記憶として内部に持ち、専用記憶層による塊選択と記憶トークンによる更新で段階ごとに証拠を差し替え、32K文脈の16倍・32倍圧縮で最強の比較対象を平均完全一致で最大10.23点上回った。

- **2026-07 · [Octopus: Gated Selective Attention for Memory-Bounded Long-Context Inference in Large Language Models](2026-28d0e3a1162b-octopus-gated-selective-attention-for-memory-bounded-long-context-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事前学習済みモデルの各層へ学習可能なゲートを付け、トークンごとの効用をKVヘッド単位で予測して高効用のKV状態だけを固定予算へ残すことで、履歴を一つの状態へ圧縮せずにメモリ有界な長文脈推論を実現する方式。

- **2026-07 · [Nexus: Depth-Adaptive KV-Cache Splicing and Retrieval-Decoupled Tool Routing for Agentic LLMs on Unified Memory](2026-2608.20397-nexus-depth-adaptive-kv-cache-splicing-and-retrieval-decoupled-tool-rout.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ツール選択をスキーマプリフィルから検索で切り離し、引数生成は圧縮署名上で行うエージェント向けサービング試作。KV移植はRoPE位相ずれの境界つきで、深さ適応型再計算により出力の完全一致を保証する。

- **2026-07 · [MOSAIC: Adaptive Inter-layer Composition for Efficient Heterogeneous Vision-Language Models](2026-2607.09029-mosaic-adaptive-inter-layer-composition-for-efficient-heterogeneous-visi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層ごとに注意機構とFFN幅を選ぶ探索を多目的混合整数計画で解き、2段階蒸留で品質を回復して、視覚言語モデルを教師とほぼ同品質のままプリフィル1.76倍・デコード2.54倍へ高速化する自動異種化の手法。

- **2026-07 · [MoA-Structured Decode Attention DNF Derivation, KV-Cache Accumulation, GQA/MQA, and OpenACC Kernel](2026-2607.19456-moa-structured-decode-attention-dnf-derivation-kv-cache-accumulation-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習時の注意の標準形へデコードの添字を固定し、転置バッファを代数的に消したデコード式、合体アクセスを証明したOpenACCカーネル、定数コストのKVキャッシュ追加、GQA／MQAを、メモリ交通の定理付きで導く形式導出。

- **2026-07 · [LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models](2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの反復生成で不変なトークン状態とFlashAttention中間状態を無損失再利用し、第2層以降をFP8化して、既存の生成ステップ削減法と組み合わせ可能な推論高速化を実現する。

- **2026-07 · [KAP: Bridging the Knowledge Selection-Runtime Consumption Gap in LLM Systems](2026-2607.24260-kap-knowledge-access-planning-kv-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索・グラフなど上流の知識選択情報を実行時アクセス計画へコンパイルし、論理プロンプトを変えず物理KV参照を選択化する。GraphSpecは128Kで提案時KVアクセスを元状態の5.5%まで減らす。

- **2026-07 · [InferScale: GPU-Native KV Injection for Personalized LLM Serving](2026-2607.27090-inferscale-gpu-native-kv-injection.md)**  
  実装：[✓](https://github.com/saltsystemslab/InferScale) ・ リポジトリ内被引用：0  
  検索メモリのRoPE適用前KVをGPU上で再利用・位置再配置してvLLMへ直接注入し、k=50でTTFTを72〜79%削減する。

- **2026-07 · [How Query Visibility Changes KV-Cache Compression Rankings: A Matched-Budget Audit](2026-2607.11942-how-query-visibility-changes-kv-cache-compression-rankings-a-matched-bud.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文書を一度プリフィルしてKVキャッシュを保存し、後から多数の質問に答える運用では、キャッシュ圧縮時点で将来の質問文は存在しない。RULER-8192で3モデル・6既存方式・3単純基準・4圧縮率を比較した結果、質問を見ずに圧縮する条件では、KeyDiffが単純基準3方式の最高値を36条件中31条件で上回り、平均差は+0.171だった。

- **2026-07 · [FreqDepthKV: Frequency-Guided Depth Sharing for Robust KV Cache Compression in Long-Context LLM Inference](2026-2607.06519-freqdepthkv-frequency-guided-depth-sharing-for-robust-kv-cache-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FreqDepthKVは、長文脈LLMのKVキャッシュをトークン方向だけでなく層の深さ方向にも圧縮する推論時手法である。Peak KV メモリは24.0GBから6.2GB、デコード スループットは38.2から70.4 トークン/sとなる。

- **2026-07 · [FastTPS: An Optimized Method for LLM Token Phase for AI accelerators](2026-2607.11211-fasttps-an-optimized-method-for-llm-token-phase-for-ai-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン生成段階のKV連結を静的キャッシュへの直接書き込みで消し、注意とMLPを深く融合して演算強度を上げるデータフロー最適化。NPU実機で最大6.0倍の高速化と帯域利用率93パーセントを達成。

- **2026-07 · [DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation](2026-2607.24331-dynacalkv-key-value-cache-compression-via-head-grouping-and-adaptive-rank-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー投影の注意ヘッドをCKA類似度で動的に群分けし、群ごとの情報量に応じて低ランク次元を配分することでReCalKVよりキー側パラメータを減らすが、GQAの長文脈では精度低下も確認する。

- **2026-07 · [DepthWeave-KV: Token-Adaptive Cross-Layer Residual Factorization for Long-Context KV Cache Compression](2026-2607.06523-depthweave-kv-token-adaptive-cross-layer-residual-factorization-for-long.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DepthWeave-KVは、長文脈TransformerのKVキャッシュを、隣接する層間の冗長性とトークンごとの重要度の違いを同時に利用して圧縮する手法である。

- **2026-07 · [Compress the Cache, Not the Speech Embedding: KV Compression for Efficient Speech LLMs](2026-2607.06827-compress-the-cache-not-the-speech-embedding-kv-compression-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の音声アダプタによる早期間引きはこの問題を解消するが、LLMが音声とテキストを統合する前に細かな音響情報を失うおそれがある。実験では、社内固有表現認識の誤り率が14.41から13.46、OpenASRの平均単語誤り率が6.12から5.98へ改善し、A100 80GBとvLLMの復号速度は30秒音声で1.49倍、10分音声で2.02倍となった。

- **2026-07 · [Cache Merging as a Convergent Replicated State for Multi-Agent Latent Reasoning](2026-2607.01308-cache-merging-as-a-convergent-replicated-state-for-multi-agent-latent-re.md)**  
  実装：[✓](https://anonymous.4open.science/r/cache-merge-artifact-2F54) ・ リポジトリ内被引用：0  
  エージェント間のKVキャッシュ交換を、内容で順序を決める正準マージと集合和による収束型複製状態に作り替え、入力順序や重複配達に依存しない潜在推論の合成を、精度をほぼ落とさず実現した。

- **2026-07 · [Anchoring the Cache: Mitigating Contextual Hallucination in KV-Compressed Long-Context Summarization](2026-07a1c74f044c-anchoring-the-cache-mitigating-contextual-hallucination-in-kv-compressed.md)**  
  実装：[✓](https://github.com/FYYFU/HeadKV) ・ リポジトリ内被引用：0  
  KVキャッシュ圧縮が長文要約の幻覚を最大3.36倍に悪化させることと、その原因が検索ヘッドの注意の原文から生成文への移行であることを示し、デコード時に検索ヘッドの生成済みキャッシュだけを除くHalluKVで、Llama-3-8Bでは幻覚を平均5.48ポイント下げつつ要約品質も保った。

- **2026-07 · [A Comparative Study of KV-Cache Quantisation Methods for Large Language Model Inference](2026-7076e1d844a5-a-comparative-study-of-kv-cache-quantisation-methods-for-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュ量子化の5手法と無圧縮基準を、ビット予算・キャリブレーション要否・キー再構成の有無など5基準で並べ、圧縮率の差がメタデータ費用で説明できることと、データ無依存型の2手法だけがキャリブレーションも再構成も不要であることを整理した比較サーベイ。

- **2026-06 · [RKSC: Reasoning-Aware KV Cache Sharing and Confident Early Exit for Multi-Step LLM Inference](2026-2606.09937-rksc-reasoning-aware-kv-cache-sharing-and-confident-early-exit-for-multi.md)**  
  実装：[✓](https://github.com/AnirudhSekar/RKSC) ・ リポジトリ内被引用：0  
  意味的類似度でプリフィックスKVをブランチ間共有し、確信が高いとき検証を省くか中間層で検証を終える学習不要の枠組みで、多ブランチ推論をKVなし基準の約3倍に高速化する方式。

- **2026-06 · [Rethinking LoRA Memory Through the Lens of KV Cache Compression](2026-2606.05698-rethinking-lora-memory-through-the-lens-of-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索拡張生成では、回答に必要な文書をプロンプトへ入れると、文書内容が鍵・値キャッシュ（KVキャッシュ）へ保存され、回答中に参照される。さらにLoRAを文書の事前処理（プリフィル）、KV圧縮の重要度採点、回答復号のどの段階で有効にするかを分けた。

- **2026-06 · [Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers](2026-2144aa87ce08-reimagining-llm-inference-infrastructure-with-memory-centric-kv-cache-se.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、GPUを計算能力の大きさで増設する従来のLLMデータセンター設計が、長文脈・長い推論出力・複数エージェント間の接頭辞共有という負荷に必ずしも合致しないと論じる。

- **2026-06 · [ProtoKV: Streaming Video Understanding under Delayed Query with Summary-State Memory](2026-2606.26762-protokv-streaming-video-understanding-under-delayed-query-with-summary-s.md)**  
  実装：[✓](https://github.com/kaist-ina/ProtoKV) ・ リポジトリ内被引用：0  
  視覚言語モデル（Vision-Language モデル; VLM）は新しいフレームを取り込むたびに注意機構のキー・値（Key/Value; KV）キャッシュを増やす。主実験のLLaVA-OV-7Bでは、RVS-Egoの正答率が固定窓方式55.7%、オンラインのトークン保持方式InfiniPot-V 57.8%、ProtoKV 58.6%となる。

- **2026-06 · [Plug-and-Play KV Cache Reuse for Low-Latency Retrieval-Augmented Generation](2026-61064d66f56b-plug-and-play-kv-cache-reuse-for-low-latency-retrieval-augmented-generat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデルもプロンプトも変えない条件で、システム指示をアンカーとして文書ブロックを事前計算し、位置埋め込みを直して連結することでKVキャッシュを再利用し、最初のトークンまでの時間を約5.9倍短くする代わりに正解率の一部を失う交換関係を実測した研究。

- **2026-06 · [Myopia Rectification: KV Cache Pruning for MLLMs via Dynamic Attention Subsidy and Token Reclamation](2026-1b586a81703a-myopia-rectification-kv-cache-pruning-for-mllms-via-dynamic-attention-su.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数画像MLLMで後ろの画像が注意されにくい「注意機構 Myopia」を発見し、画像単位の動的注意補助（DAS）と捨てトークンの回収箱（Recycling Bin）で、KVキャッシュ20%でも精度を保つ学習不要のプルーニング手法を提案した論文。

- **2026-06 · [HybridThinker: Efficient Chain-of-Thought Reasoning via Compressed Memory and Transient Thought Steps](2026-2606.03768-hybridthinker-efficient-chain-of-thought-reasoning-via-compressed-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LightThinkerのような方式は、各思考段階を少数の記憶トークンへ圧縮して、元の思考トークンのKVを即座に削除する。

- **2026-06 · [High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration](2026-2607.16248-high-accuracy-low-bit-kv-cache-quantization-via-local-distribution-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  1ビットKVキャッシュを維持したまま、量子化で崩れた高確率候補の局所順位だけを検出・補正し、RULER精度を47.8%から83.2%へ回復するDGAP。

- **2026-06 · [CompRank: Efficient LLM Reranking via Token-Level Compression and Decoding-Free Scoring](2026-2606.11700-comprank-efficient-llm-reranking-via-token-level-compression-and-decodin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMリランカーの文書表現を候補順序から切り離して再利用可能にし、文書トークンを区間圧縮で10.2パーセントまで減らし、識別子生成の代わりに注意質量のスコアで生成なしに順位付けることで、BEIR平均の品質をほぼ保ちながら生成型方式より最大9.5倍速く、候補500件まで安定する枠組み。

- **2026-06 · [Can I Buy Your KV Cache?](2026-2606.13361-can-i-buy-your-kv-cache.md)**  
  実装：[✓](https://github.com/zly-idleness/kvstore) ・ リポジトリ内被引用：0  
  文書のKVキャッシュを発行者が事前計算して成果物化し、利用側が読み込んでプリフィルを省略する再利用を検証した研究。トークン完全一致を確認し、再利用はプリフィルの9〜50倍安く、配送より提供者側ホスティングが経済的に成り立つことを示す。

- **2026-06 · [Affix Cache for Diffusion Large Language Models](2026-2608.26140-affix-cache-for-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/sands-lab/ACache) ・ リポジトリ内被引用：0  
  ACache（Affix Cache）は、拡散型大規模言語モデル（Diffusion Large Language モデル; DLLM）において、複数の生成要求が同じ文脈を共有する際に、共有文脈の鍵・値キャッシュ（KV キャッシュ）を一度だけ保存し、要求ごとに必要な一部だけを再計算する推論基盤である。

- **2026-06 · [Adaptive Visual KV Cache Reuse for Efficient Multi-Turn Iterative Multimodal Reasoning](2026-2606.26631-adaptive-visual-kv-cache-reuse-for-efficient-multi-turn-iterative-multim.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  切り取りの面積比で再エンコードと視覚KV再利用を切り替え、キーの位置を掛け直し、推論の意図で値を強調することで、多ターン視覚推論の重複処理を削りながら正解率を保つ適応型再利用。

- **2026-05 · [WindowQuant: Mixed-Precision KV Cache Quantization based on Window-Level Similarity for VLMs Inference Optimization](2026-2605.02262-windowquant-mixed-precision-kv-cache-quantization-based-on-window-level-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の量子化方式では全トークンを同じ低ビットへ変換すると品質が落ちやすく、重要度によってトークンごとにビット幅を変えると探索や計算の費用が大きくなる。

- **2026-05 · [When Quantization Is Free: An int4 KV Cache That Outruns fp16 on Apple Silicon](2026-2605.05699-when-quantization-is-free-an-int4-kv-cache-that-outruns-fp16-on-apple-si.md)**  
  実装：[✓](https://github.com/aminems/AppleSiliconFFT) ・ リポジトリ内被引用：0  
  統一メモリでは鍵値の転送が生成を支配するため、回転と尺度と四ビット詰め込みを一回の融合カーネルにまとめれば、量子化の追加費用より転送の節約が大きくなり、十六ビットより速く約三倍の圧縮が同時に得られることを実機で示した。

- **2026-05 · [When KV Meets Embeddings: Dynamic GPU Memory Allocation for Accelerating Generative Recommender Serving](2026-2605.04450-when-kv-meets-embeddings-dynamic-gpu-memory-allocation-for-accelerating-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成レコメンダのGPU HBMを埋め込みキャッシュとKVキャッシュへ実行時に再配分する問題を定式化し、3層PPO制御器による配分決定、在駐状態を動かさない配分適用、両キャッシュの局所性を併せ見たルーティングを備えるRACERで、静的配分比の限界を実測とともに示した研究。

- **2026-05 · [Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles](2026-2605.19775-understanding-inference-scaling-for-llms-bottlenecks-trade-offs-and-perf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は新しい推論アルゴリズムを提案するものではなく、8Bから671Bパラメータまでの密なモデルと混合専門家モデルを、8基のNVIDIA H200を持つ実機で比較した性能特性研究である。

- **2026-05 · [SemanticKV: A Semantics-Driven KV Cache Eviction Framework for Efficient Long Prompt LLM Inference](2026-41074c82c154-semantickv-a-semantics-driven-kv-cache-eviction-framework-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力が数万から十万トークン規模になると、KV保存量だけでなく、各生成トークンで過去文脈へ注意を計算する時間が問題になる。単純な直近窓だけを残す方式では、文書の中盤にある重要な条件や事実が失われる。

- **2026-05 · [Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models](2026-2605.09630-scratchpad-patching-decoupling-compute-from-patch-size-in-byte-level-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この「パッチ遅延（patch lag）」が、大きなパッチの精度劣化を招く。したがって、パッチ長が決めるKVキャッシュ圧縮率と、内部で追加実行する計算回数を別々に調整できる。約20億パラメータの実験で、固定16バイト/パッチの自然言語理解平均精度はSPなし48.0からSPあり54.2へ改善し、バイト単位基準の主幹系列短縮16倍を維持する。

- **2026-05 · [SATORU: Proactive Length-Aware Scheduling for High-Throughput Batch LLM Serving](2026-77c905c22830-satoru-proactive-length-aware-scheduling-for-high-throughput-batch-llm-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長予測で将来のKV増加と残り作業量を見積もり、インスタンス内では先読み受付でプリエンプションの再計算を防ぎ、クラスタでは接頭辞の共有と作業量均等化で振り分ける、一括処理向けの先回り型スケジューリング枠組み。

- **2026-05 · [Rotation-Aligned Key Channel Pruning for Efficient Vision-Language Model Inference](2026-2605.19218-rotation-aligned-key-channel-pruning-for-efficient-vision-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来は重要度の低い視覚トークンを丸ごと削除する方式が多いが、文書の小さな文字や画像全体に散らばる情報を必要とする質問では、削除した位置の証拠を復元できない。

- **2026-05 · [ProxyKV: Cross-Model Proxy Pruning for Efficient Long-Context LLM Inference](2026-2605.16360-proxykv-cross-model-proxy-pruning-for-efficient-long-context-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ProxyKVは、長文脈LLMのKVキャッシュを圧縮するとき、どのトークンを残すかを高精度に決める計算を大型モデル自身にさせず、同じモデル系列の小型モデルへ委譲する方式である。Llama-3.1-8Bではdual-GPU構成で最大3.21倍のプレフィル高速化、同一GPU上でCUDA ストリームを共有する構成では約1.5倍を報告する。

- **2026-05 · [Probing the Prompt KV Cache: Where It Becomes Dispensable](2026-2605.30574-probing-the-prompt-kv-cache-where-it-becomes-dispensable.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層・時点・ドナー内容を振る接続介入で、プロンプトKVは上層では形式だけあれば置換可能で、下層では内容が効くことを示した分析。圧縮は上層では削除より構造的な代用品への置換、下層では内容保持が要るという指針を与える。

- **2026-05 · [Polynomial Context-Truncation Sensitivity in Autoregressive Language Models: Sequential Wyner-Ziv Bounds for KV Cache Compression](2026-2605.25085-polynomial-context-truncation-sensitivity-in-autoregressive-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  逐次Wyner–Ziv符号化としてKVキャッシュ圧縮を定式化し、末尾窓だけを保持する方式の必要窓長が、追加の両側リスク条件下で許容分布誤差εに対してΘ(ε^{-1/α})となることを示す。

- **2026-05 · [Non-Monotonic Latency in Apple MPS Decoding: KV Cache Interactions and Execution Regimes](2026-2605.08913-non-monotonic-latency-in-apple-mps-decoding-kv-cache-interactions-and-ex.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Apple MPSバックエンドの自己回帰デコードで、特定のデコード予算区間にだけ遅延が最大21倍へ跳ねる非単調な実行レジームが存在し、KVキャッシュの利得がその区間で崩壊することを、複数モデルと統制実験で示した測定研究。

- **2026-05 · [NIKA: Optimal KV Cache Transfer for Minimizing the Latency of Disaggregated LLM Inference](2026-96229b44d7f2-nika-optimal-kv-cache-transfer-for-minimizing-the-latency-of-disaggregat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NIKAが対象とするのは、入力プロンプトを一括処理する事前入力（プリフィル）と、出力トークンを逐次生成する復号（デコード）を別のGPUへ割り当てる分離型推論である。CLOSER 2026の8ページ論文では、vLLM 0.8.4の分離型構成を改造し、全KV転送の基準方式に対してTTFT最大54%減を報告した。

- **2026-05 · [Moment-KV: Momentum-Based Decode-Time KV Cache Compression for Long Generation](2026-2605.29873-moment-kv-momentum-based-decode-time-kv-cache-compression-for-long-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルを凍結し、デコード側KVだけをモメンタム付き注意集約の累積重要度で管理する圧縮法。瞬時注意の見落としと固定直近ウィンドウの無駄を同時に避け、長生成ベンチマークで比較対象を上回る。

- **2026-05 · [Minimal-Intervention KV Retention via Set-Conditioned Diversity](2026-2605.14292-minimal-intervention-kv-retention-via-set-conditioned-diversity.md)**  
  実装：[✓](https://github.com/libophd/minimal-kv-retention) ・ リポジトリ内被引用：0  
  基準方式TriAttentionの保持重要度を変更せず、既に選んだトークンの値ベクトル（value vector; V）と重複する候補を次の選択で減点する、集合条件付き（set-conditioned）の保持選択器αを提案する。

- **2026-05 · [Meta-Soft: Leveraging Composable Meta-Tokens for Context-Preserving KV Cache Compression](2026-2605.22337-meta-soft-leveraging-composable-meta-tokens-for-context-preserving-kv-ca.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈LLMの生成では、過去トークンの鍵・値（KV）キャッシュが入力長にほぼ比例して増え、GPUメモリと注意計算の負担になる。Meta-Softは二つの機構を組み合わせる。生成1万トークンの別実験では、完全KVより大きなバッチと高い処理量を達成するが、SnapKVより生成処理量は低い。

- **2026-05 · [Make Your LVLM KV Cache More Lightweight](2026-2605.00789-make-your-lvlm-kv-cache-more-lightweight.md)**  
  実装：[✓](https://github.com/howtoosee/LightKV) ・ リポジトリ内被引用：0  
  自己回帰復号では過去のキー・値（KV）を保存するため、視覚トークンが多いほどGPUメモリを消費する。LightKVが速度でも品質でもすべての比較方式に勝つわけではない。

- **2026-05 · [KVCapsule: Efficient Sequential KV Cache Compression for Vision-Language Models with Asymmetric Redundancy](2026-2605.16439-kvcapsule-efficient-sequential-kv-cache-compression-for-vision-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVCapsuleは、視覚言語モデルの画像トークンが作る鍵・値キャッシュを、単に重要度の低いトークンから削除するのではなく、後で復元できる表現へ圧縮する手法である。五つの視覚言語モデルと画像・動画評価で、視覚KVを平均約60%削減しながら多くの品質指標を保つ。

- **2026-05 · [KVBoost: Chunk-Level Key-Value Cache Reuse with Deviation-Guided Recomputation for Efficient Large Language Model Inference](2026-2608.21362-kvboost-chunk-level-key-value-cache-reuse-with-deviation-guided-recomput.md)**  
  実装：[✓](https://github.com/pythongiant/kvboost) ・ リポジトリ内被引用：0  
  プロンプトをチャンクに切り二重ハッシュでKVを引くことで任意位置の共通部分を再利用し、継ぎ目の誤差をずれの大きいトークンだけの再計算で直すことで、最初のトークンまでの時間を4.49倍短縮し前置きキャッシュも上回った研究。

- **2026-05 · [KV-Fold: One-Step KV-Cache Recurrence for Long-Context Inference](2026-2605.12471-kv-fold-one-step-kv-cache-recurrence-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い入力を一度に処理する大規模言語モデル（LLM）の事前処理では、全トークンに対する注意演算と、各層の鍵・値キャッシュ（KV キャッシュ）を保持するための記憶容量が問題になる。新しい注意カーネルや学習済み圧縮器の提案ではなく、既存Transformerの推論操作に対する実証的な分析が中心となる。

- **2026-05 · [Hurwitz Quaternion Multiplicative Quantization for KV Cache Compression](2026-2605.27646-hurwitz-quaternion-multiplicative-quantization-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の半精度浮動小数点（FP16）で保存すると、文脈長に比例してKVのメモリ占有量が増える。ノルムである半径は別に量子化する。これに、チャンクの半径が同一集団の中央値の3倍を超えたときだけFP16で保存する外れ値退避（Med3×）を組み合わせる。

- **2026-05 · [How to Compress KV Cache in RL Post-Training? Shadow Mask Distillation for Memory-Efficient Alignment](2026-2605.06850-how-to-compress-kv-cache-in-rl-post-training-shadow-mask-distillation-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成時に残したトークンの記録である影マスクを学習側の注意へ注入して生成と評価の条件を一致させ、密な文脈からの蒸留を併用することで、強化学習の生成段階の鍵と値のキャッシュを半分にしても学習を崩さないと第1版で主張した方式。ただし論文自体は実験結果の誤りを理由に撤回済みである。

- **2026-05 · [HeadQ: Model-Visible Distortion and Score-Space Correction for KV-Cache Quantization](2026-2605.03562-headq-model-visible-distortion-and-score-space-correction-for-kv-cache-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  保存精度を下げれば容量と読み出し帯域を削減できるが、単純に保存値の平均二乗誤差が小さい量子化方式を選んでも、生成品質が良いとは限らない。

- **2026-05 · [FastOCR: Dynamic Visual Fixation via KV Cache Pruning for Efficient Document Parsing](2026-2605.17447-fastocr-dynamic-visual-fixation-via-kv-cache-pruning-for-efficient-docum.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FastOCRは追加学習不要で、焦点層誘導型の枝刈り（Focal-Guided Pruning、FGP）とステップ間注視再利用（Cross-Step Fixation Reuse、CSFR）を組み合わせる。Qwen2.5-VLでは画像トークンの保持率5%でOmniDocBench総合スコア72.76から71.34（98.0%保持）となる。

- **2026-05 · [Discovering KV Cache Eviction Policies via LLM-Guided Program Evolution](2026-2608.14555-discovering-kv-cache-eviction-policies-via-llm-guided-program-evolution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が扱うのは、長い入力文を処理した直後に、後続の生成に必要な鍵・値キャッシュ（Key-Value Cache、以下KVキャッシュ）のどの位置を残すかという選択問題である。キャッシュを圧縮すると生成中のメモリ使用量は減るが、削除した位置へ再び注意を向けられなくなるため、根拠検索や長文理解の精度が低下する。

- **2026-05 · [Decouple and Cache: KV Cache Construction for Streaming Video Understanding](2026-2605.01858-decouple-and-cache-kv-cache-construction-for-streaming-video-understandi.md)**  
  実装：[✓](https://github.com/pangzhan27/DSCache) ・ リポジトリ内被引用：0  
  過去の累積キャッシュと直近の即時キャッシュの構築を分離し、位置非依存の符号化で長さの壁を外すことで、学習済みのオフライン動画モデルを無限の流れへ学習不要で適応させ、正解率を平均2.5ポイント押し上げた研究である。

- **2026-05 · [CoRDS: Coreset-based Representative and Diverse Selection for Streaming Video Understanding](2026-2605.14310-cords-coreset-based-representative-and-diverse-selection-for-streaming-v.md)**  
  実装：[✓](https://github.com/ailarmhz/CoRDS.git) ・ リポジトリ内被引用：0  
  KVキャッシュ圧縮を履歴全体を覆うコアセット選択として定式化し、キーとバリューの両空間での被覆と直交性による多様さで選ぶことで、同一予算の既存圧縮を上回り、全保持を超える条件も示した。

- **2026-05 · [Context Memorization for Efficient Long Context Generation](2026-2605.18226-context-memorization-for-efficient-long-context-generation.md)**  
  実装：[✓](https://github.com/yasu0001/AttentionMemory) ・ リポジトリ内被引用：0  
  著者らは注意状態メモリ（注意機構-state メモリ; ASM）を提案する。LLaMA 3.1-8Bを使うManyICLBenchの主要5課題では、同等のメモリ予算で1K〜8K項目の平均精度が文脈内学習基準と同等以上になり、8K予算では注意演算の遅延を1.36倍改善したと報告する。

- **2026-05 · [Benchmarking KV-Cache Optimizations across Task Quality and System Performance for Long-Context Serving](2026-2607.05399-benchmarking-kv-cache-optimizations-across-task-quality-and-system-perfo.md)**  
  実装：[✓](https://github.com/nikagrwal/Benchmarking-KV-Cache-Optimizations-across-Task-Quality-and-System-Performance) ・ リポジトリ内被引用：0  
  本研究の目的は、鍵・値キャッシュ（Key–Value キャッシュ; KVキャッシュ）の削減率だけで方式を選んだときに、実際の長文脈推論が速くなるとは限らないという問題を、同じモデル・負荷・測定指標のもとで検証することである。A100 40GBの単一GPU評価では、KIVI4が比較的安定した品質を示し、SnapKVは高い復号処理量を維持した。

- **2026-05 · [Augmenting Attention with Exponentially Decaying Memory Improves Query-Aware KV Sparsity](2026-2605.28640-augmenting-attention-with-exponentially-decaying-memory-improves-query-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キーとバリューへ指数減衰メモリを混ぜるバックボーンを使うと、Quest・MoBA・SnapKVのスパース推論が同じKV予算でも正解率を大きく保てることを、干し草タスク8種と選択命中率・ランダム選択の分析実験で示した研究。

- **2026-04 · [Sequential KV Cache Compression via Probabilistic Language Tries: Beyond the Per-Vector Shannon Limit](2026-2604.15356-sequential-kv-cache-compression-via-probabilistic-language-tries-beyond-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、言語モデルの鍵・値キャッシュ（KV Cache）を独立した浮動小数点ベクトルの集合として圧縮する従来の考え方を改め、元のトークン系列の確率構造に基づいてキャッシュ系列全体を圧縮する構想を示す。原著に対応するGPU実験表はなく、復号時の予測KV再計算、誤差許容、索引維持、圧縮・復元時間を含めた実用性は検証されていない。

- **2026-04 · [Reducing Peak Memory Usage for Modern Multimodal Large Language Model Pipelines](2026-2604.16734-reducing-peak-memory-usage-for-modern-multimodal-large-language-model-pi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力をブロック単位に処理し各ブロック直後に固定予算を超えた分を追い出す前処理中の圧縮で、約九割削っても平均正解率の低下を〇・七八ポイントに抑えた条件があり、タイルを増やしてもピークメモリがほぼ一定に保たれたと報告した。

- **2026-04 · [Probe-and-Fetch: Dynamic KV Cache Pruning for Accelerated Long-Context Inference in Web-Scale AI Search](2026-bfd3ce93bf5b-probe-and-fetch-dynamic-kv-cache-pruning-for-accelerated-long-context-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の投機的復号は軽量ドラフトが複数トークンを提案し、大型ターゲットが一度に検証する。ターゲットは転送済みの疎KVだけで候補を検証するため、転送とドラフト生成を重ね、検証のメモリ帯域を削減できる。

- **2026-04 · [Latent-Condensed Transformer for Efficient Long Context Modeling](2026-2604.12452-latent-condensed-transformer-for-efficient-long-context-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（multi-head latent 注意機構、MLA）はトークンごとのKVを低次元潜在へ圧縮するが、文脈の全トークンを保持し、注意計算も全長に対して行う。

- **2026-04 · [High Throughput and Low Latency LLM Serving via Adaptive KV Caching](2026-e8ff0256681f-high-throughput-and-low-latency-llm-serving-via-adaptive-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論のデコード（デコード）段階では、過去トークンの鍵・値（KV）キャッシュが高帯域幅メモリ（HBM）を占有する一方、演算器であるストリーミング・マルチプロセッサ（SM）は遊休しやすい。従来のvLLMの退避・再計算は、主にメモリ不足で停止した要求のKV全体を扱う。

- **2026-04 · [Graph-Guided Adaptive Channel Elimination for KV Cache Compression](2026-2604.16983-graph-guided-adaptive-channel-elimination-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈のLLM推論では、各層・各注意ヘッドのKeyとValueを過去トークン分保持するKVキャッシュがメモリを圧迫する。トークン単位で古いKVを捨てる方法や、低ビット化する方法とは別に、Keyベクトルのチャネル方向の冗長性を利用する圧縮がある。

- **2026-03 · [TurboESM: Ultra-Efficient 3-Bit KV Cache Quantization for Protein Language Models with Orthogonal Rotation and QJL Correction](2026-2603.26110-turboesm-ultra-efficient-3-bit-kv-cache-quantization-for-protein-languag.md)**  
  実装：[✓](https://github.com/YueHuLab/TurboESM) ・ リポジトリ内被引用：0  
  タンパク質言語モデルの鋭い外れ値に対し、RoPEの後に直交回転を掛ける順序、ヘッドごとの特異値分解較正、二重ルックアップテーブルと1ビット残差補正で3ビットKVキャッシュ量子化を成立させ、ESM-2 650Mでメモリを7.1倍圧縮しながら類似度0.96超を保つ手法。

- **2026-03 · [Think-as-You-See: Streaming Chain-of-Thought Reasoning for Large Vision-Language Models](2026-2603.02872-think-as-you-see-streaming-chain-of-thought-reasoning-for-large-vision-l.md)**  
  実装：[✓](https://github.com/EIT-NLP/StreamingLLM/tree/main/TaYS) ・ リポジトリ内被引用：0  
  動画を全て受け取ってから推論するバッチ型に対し、フレーム到着と並行して推論を進めるストリーミング推論を、ストリーミング注意マスク、分離型の位置符号化、視覚と推論を分離したデュアルKVキャッシュで実現し、初回トークンまでの時間をほぼゼロにした研究。

- **2026-03 · [Stream2LLM: Overlap Context Streaming and Prefill for Reduced Time-to-First-Token (TTFT)](2026-2604.16395-stream2llm-overlap-context-streaming-and-prefill-for-reduced-time-to-fir.md)**  
  実装：[✓](https://github.com/rajveerb/stream2llm/) ・ リポジトリ内被引用：0  
  文脈の断片が届くたびにプリフィルを進めるストリーミング基盤で、費用考慮のスケジューリングと接頭辞一致による無効化削減を組み合わせ、TTFTを最大11倍改善しつつスループットを維持した。

- **2026-03 · [SPAR-K: Scheduled Periodic Alternating Early Exit for Spoken Language Models](2026-2603.09215-spar-k-scheduled-periodic-alternating-early-exit-for-spoken-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  交互生成型の音声言語モデルで、音声位置だけを周期スケジュールで早期終了させ、全深さステップで分布ずれの回復と上位KVキャッシュの一括補完を行う方式を提案し、精度をほぼ保って音声の平均深さを削減した研究。

- **2026-03 · [PRISM: Photonic Similarity Engine for KV Cache Block Selection in Long-Context LLM Inference](2026-2603.21576-prism-photonic-similarity-engine-for-kv-cache-block-selection-in-long-co.md)**  
  実装：[✓](https://github.com/hyoseokp/PRISM) ・ リポジトリ内被引用：0  
  PRISMは、長文脈LLMのデコード時にKVキャッシュのどのブロックを読むべきか決める候補選択段階を、薄膜ニオブ酸リチウム（TFLN）の光回路へ移す構想である。通常のブロック疎注意では、GPUが全ブロックの短い署名を読み、現在のqueryと比較して上位k個を選び、そのブロックの実際のKVを取得する。今回の読解はPDFの最新版を基準とする。

- **2026-03 · [OxyGen: Unified KV Cache Management for VLA Inference under Multi-Task Parallelism](2026-2603.14371-oxygen-unified-kv-cache-management-for-vla-inference-under-multi-task-pa.md)**  
  実装：[✓](https://github.com/air-embodied-brain/OxyGen) ・ リポジトリ内被引用：0  
  OxyGenは、この重複を「専門家間で分離されていた鍵・値キャッシュ（KV キャッシュ）の寿命と所有権」の問題と捉え、観測から得た基盤モデルのKVを共有するとともに、文章の生成状態をフレームをまたいで保存する。

- **2026-03 · [KVSlimmer: Theoretical Insights and Practical Optimizations for Asymmetric KV Merging](2026-2603.00907-kvslimmer-theoretical-insights-and-practical-optimizations-for-asymmetri.md)**  
  実装：[✓](https://github.com/lianjunl13-sudo/KVSlimmer) ・ リポジトリ内被引用：0  
  古いトークンを単に捨てる方式は将来必要になる情報を回復できないため、近接したトークンの表現を統合して残す方法が検討されている。A100上ではAsymKV比で平均実行時間28%削減、チャンク512のピークGPUメモリ約29%削減を報告する。

- **2026-03 · [Knowledge Packs: Zero-Token Knowledge Delivery via KV Cache Injection](2026-2604.03270-knowledge-packs-zero-token-knowledge-delivery-via-kv-cache-injection.md)**  
  実装：[✓](https://github.com/cnails/kv-knowledge-packs) ・ リポジトリ内被引用：0  
  事実文のKVキャッシュを事前計算して接頭辞として注入し、検索拡張生成とバイト単位で同じ出力をトークン消費ゼロで得る方式を、等価性の証明とチャットテンプレート整形の必須条件つきで示した研究。

- **2026-03 · [Efficient Reasoning on the Edge](2026-2603.16867-efficient-reasoning-on-the-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Efficient Reasoning on the Edge は、推論能力のあるLLMをエッジ端末へ載せる際の主な負担を、重いモデル重み、長いchain-of-thought（CoT）、不必要な推論、KVキャッシュ、並列回答の検証に分けて扱う統合研究である。

- **2026-03 · [Beyond Token Eviction: Mixed-Dimension Budget Allocation for Efficient KV Cache Compression](2026-2603.20616-beyond-token-eviction-mixed-dimension-budget-allocation-for-efficient-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixedDimKVは、長文推論の鍵・値キャッシュ（key-value キャッシュ、KVキャッシュ）を「トークンを残すか破棄するか」だけで制御する従来の方式を拡張し、各トークンに異なる保持次元数を割り当てる圧縮方式である。

- **2026-02 · [More Than a Quick Glance: Overcoming the Greedy Bias in KV-Cache Compression](2026-2602.02199-more-than-a-quick-glance-overcoming-the-greedy-bias-in-kv-cache-compress.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意スコア単独の貪欲なKV圧縮に対し、蓄積型予算と保護除数とハッシュ想起を組み合わせ、128k文脈でも崩壊しないKVキャッシュ圧縮を示す。

- **2026-02 · [Hierarchical Adaptive Eviction for KV Cache Management in Multimodal Language Models](2026-2602.02197-hierarchical-adaptive-eviction-for-kv-cache-management-in-multimodal-lan.md)**  
  実装：[✓](https://github.com/maxindian/HAE_for_VLMs) ・ リポジトリ内被引用：0  
  視覚と言語を同じ自己注意機構で処理するマルチモーダル大規模言語モデルでは、画像から展開された視覚トークンが大量の鍵・値キャッシュ（KVキャッシュ）を消費する。

- **2026-01 · [TableCache: Primary Foreign Key Guided KV Cache Precomputation for Low Latency Text-to-SQL](2026-2601.08743-tablecache-primary-foreign-key-guided-kv-cache-precomputation-for-low-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TableCacheは、自然言語からSQLを生成するText-to-SQLシステムで、同じデータベースの表定義を何度も長いプロンプトへ挿入するために生じるプリフィル遅延を削減する。BIRDのOmniSQL-7Bを使った追加比較では累積初回トークン待ち時間（TTFT）が291.26秒から80.53秒へ短縮し、約3.62倍の改善となる。

- **2026-01 · [Parallel Context-of-Experts Decoding for Retrieval Augmented Generation](2026-2601.08670-parallel-context-of-experts-decoding-for-retrieval-augmented-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索文書を文書単位のKVキャッシュのまま並列エキスパートとして走らせ、検索スコアを事前重みに変換したコントラスティブデコードでトークンごとに証拠を縫い合わせることで、長い連結プロンプトのプリフィルなしに多文書推論を回復する学習不要の方式。

- **2026-01 · [On the Limits of Learned Importance Scoring for KV Cache Compression](2026-2601.14279-on-the-limits-of-learned-importance-scoring-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/BradySteele/kv-cache-compression-limits) ・ リポジトリ内被引用：0  
  しかし、TinyLlama-1.1B-Chat-v1.0、最大2048トークンの評価では、5乱数種・4保持率・3課題のいずれでも、SIPは単純な基準方式に対する統計的に有意な優位を示さなかった。

- **2026-01 · [Multi-tier dynamic storage of KV cache for LLM inference under resource-constrained conditions](2026-e905fcb3ff0a-multi-tier-dynamic-storage-of-kv-cache-for-llm-inference-under-resource-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、複数の大規模言語モデル（LLM）要求を限られたGPUで処理するとき、過去に計算した鍵・値（KV）キャッシュをどこに保存し、いつGPUへ戻すべきかを扱う。推論の事前充填（プリフィル）段階では入力トークンから注意機構のKVを計算する。

- **2026-01 · [GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models](2026-2601.04719-gpu-accelerated-int8-quantization-for-kv-cache-compression-in-large-lang.md)**  
  実装：[✓](https://github.com/MaanasTaneja/cuda-kv-cache-compression) ・ リポジトリ内被引用：0  
  再計算を避けるため、各層・各注意ヘッドの過去の鍵と値を保持するKVキャッシュ（KV キャッシュ）が必要になる。そこで本論文は、FP32の鍵・値行列をINT8へ変換する列別量子化と、その変換処理を高速化するCUDAカーネルを実装・比較する。

- **2025-12 · [CTkvr: KV Cache Retrieval for Long-Context LLMs via Centroid then Token Indexing](2025-2512.15550-ctkvr-kv-cache-retrieval-for-long-context-llms-via-centroid-then-token-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全履歴をGPUの高帯域メモリに置くと文脈長と同時要求数に比例して容量を圧迫する。一方、CPUの主記憶へ退避すると、必要な過去トークンを効率よく特定しなければ検索と転送の費用が新たな律速になる。原著は96Kトークンの復号でLlama-3-8Bに最大3倍、Yi-9Bに最大4倍の処理量改善、GPU容量制約下で最大10倍・20倍のバッチ数を報告する。

### 2年前（2024-12〜2025-11）

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：156  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2025-03 · [vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention](2024-2405.04437-vattention-virtual-memory-kv-management.md)**  
  実装：[✓](https://github.com/microsoft/vattention) ・ リポジトリ内被引用：97  
  KVキャッシュの仮想アドレスを連続に保ったままCUDA仮想メモリで物理ページだけを需要時割当し、PagedAttention固有のブロック表と専用注意カーネルを不要にする方式。長文脈サービングで最大1.23倍のスループット改善を報告する。

- **2025-04 · [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](2025-2504.19874-turboquant-online-vector-quantization-with-near-optimal-distortion-rate.md)**  
  実装：✓ ・ リポジトリ内被引用：89  
  TurboQuantは、高次元ベクトルを入力データセットに合わせて学習し直さずに低ビット化する、オンライン量子化方式である。理論面では、復元二乗誤差と内積誤差の両方について、ビット幅bに対して概ね4のマイナスb乗で減る上界を示し、情報理論的な下限との差が最大約2.7倍の定数内であると証明する。

- **2025-05 · [KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction](2025-2505.23416-kvzip.md)**  
  実装：[✓](https://github.com/snu-mllab/KVzip) ・ リポジトリ内被引用：84  
  元文脈の再構成時に使われるKVを重要とみなし、将来クエリを知らずに再利用可能な長文脈KVキャッシュを3〜4倍圧縮する。

- **2024-12 · [A Survey on Large Language Model Acceleration based on KV Cache Management](2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-manageme.md)**  
  実装：[✓](https://github.com/TreeAI-Lab/Awesome-KV-Cache-Management) ・ リポジトリ内被引用：82  
  キャッシュを減らせば容量は空くが、注意品質の低下、検索・量子化の追加計算、CPU/SSD転送、再計算など別の費用が発生する。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：78  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：71  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2025-10 · [Expected Attention: KV Cache Compression by Estimating Attention from Future Queries Distribution](2025-2510.00636-expected-attention-kv-cache-compression-by-estimating-attention-from-fut.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：62  
  Expected 注意機構は、大規模言語モデルの推論で増大する鍵・値キャッシュ（KV キャッシュ）を、追加学習なしに選択削除する方法である。Qwen3-8BのRULER 16Kでは、キャッシュ50%削除でも無圧縮92.9に対し92.7を維持する。

- **2025-05 · [R-KV: Redundancy-aware KV Cache Compression for Reasoning Models](2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md)**  
  実装：[✓](https://github.com/Zefan-Cai/R-KV) ・ リポジトリ内被引用：52  
  R-KVは、推論モデルが数学問題を解く際に生成する長い思考過程に含まれる重複を利用し、自己回帰復号中の鍵値キャッシュ（Key-Value キャッシュ、以下KVキャッシュ）を固定予算に抑える手法である。論文の例では8Bモデルが約32Kトークンを生成する場合、重み15.5GBに加えてKVキャッシュ約4.1GBを要する。

- **2025-03 · [CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences](2025-2503.12491-cake-cascading-and-adaptive-kv-cache-eviction-with-layer-preferences.md)**  
  実装：[✓](https://github.com/antgroup/cakekv) ・ リポジトリ内被引用：49  
  推論中に重要度の低いトークンのKVを削除する方式は多数提案されているが、層ごとに同じ数を保持するだけでは、必要な文脈情報が層によって異なる点を反映できない。Mistral-7Bの128K文脈では、FlashAttention-2を用いた全キャッシュ実装比でピークメモリ約48.63%削減、復号遅延10倍超の改善を報告する。

- **2024-12 · [ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression](2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-com.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/ClusterKV) ・ リポジトリ内被引用：48  
  鍵値キャッシュ（KVキャッシュ）を全量GPUに置くと、文脈長に比例して必要メモリが増え、各復号ステップで読み出すデータ量も増加する。これを抑える方法には、不要なトークンのKVを永久に破棄する方法と、CPUなど低速階層に退避したKVを必要に応じて呼び戻す方法がある。GPUでの復号遅延は最大2倍、処理率は最大2.5倍改善したと報告する。

- **2025-06 · [KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider](2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at.md)**  
  実装：[✓](https://github.com/vllm-project/vllm/pull/22236) ・ リポジトリ内被引用：44  
  合成トレースではなく本番サービスのトレースに基づく設計材料が不足しているという問題に対し、本研究はAliyun Tongyiの大規模serving クラスタから得た顧客向け(to-C)と企業向け(to-B)のトレースを特徴付け、観測した分布を使う追い出し 方策を提案する。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：42  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-01 · [RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations](2025-2501.16383-rotatekv-accurate-and-robust-2-bit-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/ZunhaiSu/RotateKV) ・ リポジトリ内被引用：42  
  RotateKVは、言語モデルの鍵・値キャッシュ（KVキャッシュ）を2ビットまで量子化するとき、少数の極端に大きい活性値が量子化範囲を広げてしまう問題を、特徴空間の回転と選択的な高精度保持によって抑える方式である。

- **2025-03 · [xKV: Cross-Layer KV-Cache Compression via Aligned Singular Vector Extraction](2025-2503.18893-xkv-cross-layer-kv-cache-compression-via-aligned-singular-value-decomposition.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/xKV) ・ リポジトリ内被引用：39  
  xKVは、隣接層のキー・バリュー（Key-Value; KV）キャッシュをトークンごとに直接似ているとみなすのではなく、複数層が共有する支配的な特異ベクトルをまとめて抽出する。プリフィル時に複数層を横連結して共有低ランク基底へ因子分解し、デコード時はクエリに重要なトークンだけを選択的に再構成する。

- **2025-10 · [Cache-to-Cache: Direct Semantic Communication Between Large Language Models](2025-2510.03215-cache-to-cache-direct-semantic-communication-between-large-language-mode.md)**  
  実装：[✓](https://github.com/thu-nics/C2C) ・ リポジトリ内被引用：38  
  複数の大規模言語モデル（LLM）が協調するシステムでは、あるモデルが推論や分析の結果を文章として生成し、別のモデルがその文章を読み込んで次の応答を作ることが多い。

- **2025-02 · [KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference](2025-2502.04420-kvtuner-sensitivity-aware-layer-wise-mixed-precision-kv-cache-quantizati.md)**  
  実装：[✓](https://github.com/cmd2001/KVTuner) ・ リポジトリ内被引用：38  
  KVTunerは、大規模言語モデル（LLM）の鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を、層ごとに異なるビット幅で量子化するための自動設定方式である。またKIVI-KV8を基準に、文脈長を変えた実験で最大21.25%の推論処理量改善を報告する。

- **2025-05 · [FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion](2025-2505.21467-flashdlm-accelerating-diffusion-language-model-inference.md)**  
  実装：[✓](https://github.com/ZhanqiuHu/flash-dlm-experimental) ・ リポジトリ内被引用：34  
  FlashDLMは拡散言語モデル（Diffusion Language モデル; DLM）の遅さを、1回のノイズ除去で再計算し過ぎる問題と、何回ノイズ除去を繰り返すかという問題に分ける。FreeCacheは前者を、Guided Diffusionは後者を削り、二つを組み合わせて大きな端末間高速化を得る。

- **2025-10 · [KVComm: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems](2025-2510.12872-kvcomm-online-cross-context-kv-cache-communication-for-efficient-llm-bas.md)**  
  実装：[✓](https://github.com/FastMAS/KVCOMM) ・ リポジトリ内被引用：33  
  複数の大規模言語モデル（LLM）エージェントが役割を分担すると、各エージェントのシステム指示、直前の発言、道具から得た文章は異なる。

- **2024-12 · [DynamicKV: Task-Aware Adaptive KV Cache Compression for Long Context LLMs](2024-2412.14838-dynamickv-task-aware-adaptive-kv-cache-compression-for-long-context-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  KVを一律の長さで削る方式は簡単だが、要約、文書質問応答、コード補完などでは、重要な情報が残る層とトークン位置が異なる。

- **2025-07 · [Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation](2025-2507.10524-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-tok.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  共有Transformerブロックを再帰利用し、ルータがトークンごとに継続深度を決めて活動集合だけへ注意・KV保持することで、推論時の適応計算とパラメータ共有を両立する。

- **2025-02 · [Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation](2025-2502.15734-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-gene.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  文書自体が同じなのに、GPUはその文書の鍵・値（KV）を再計算することになる。Cache-Craftは再利用するかどうかの判定と、どれだけ再計算して修復するかの決定を分離する。実際のRAGワークロードでは、接頭辞キャッシュ比で冗長計算を51%減らし、連続バッチ下で処理率を1.6倍、エンドツーエンド応答遅延を約半分にしたと報告する。

- **2024-12 · [DiffKV: Differentiated Memory Management for Large Language Models with Parallel KV Compaction](2024-2412.03131-diffkv-differentiated-memory-management-for-large-language-models-with-parallel-kv-compaction.md)**  
  実装：[✓](https://github.com/zyqCSL/DiffKV) ・ リポジトリ内被引用：28  
  鍵・値・トークン・注意ヘッドを異なる粒度で圧縮し、不規則な空き容量をGPU内で並列コンパクションするDiffKV。KVを2.7〜5.7倍圧縮しスループットを1.9〜5.4倍改善する。

- **2025-06 · [CommVQ: Commutative Vector Quantization for KV Cache Compression](2025-2506.18879-commvq-commutative-vector-quantization-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UMass-Embodied-AGI/CommVQ) ・ リポジトリ内被引用：26  
  CommVQは、長文脈の大規模言語モデル推論で鍵値キャッシュ（KVキャッシュ）が装置メモリを占有する問題に対し、ベクトル量子化（Vector Quantization; VQ）と回転位置埋め込み（Rotary Position Embedding; RoPE）の代数的性質を組み合わせて、保存容量と復号計算の両方を削減する方法である。

- **2025-11 · [TiDAR: Think in Diffusion, Talk in Autoregression](2025-2511.08923-tidar-think-in-diffusion-talk-in-autoregression.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  論文が対象にするのは、単に「拡散型言語モデルを速くする」ことではない。確定した接頭辞の鍵・値（KV）キャッシュは再利用でき、拡散型で問題になりやすい過去全体の再計算も避けられる。8B版の生成六課題平均正答率65.31%はQwen3-8Bの68.09%を下回り、元モデルと同じ出力分布を厳密に保存する手法ではない。

- **2025-10 · [Acon: Optimizing Context Compression for Long-horizon LLM Agents](2025-2510.00615-acon-optimizing-context-compression-for-long-horizon-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  Acon（Agent Context Optimization）は、過去の行動・観測をまとめた履歴と、新たに届いた長いツール観測の両方をLLMで圧縮する。圧縮の指針を人手で固定せず、同じ課題で非圧縮なら成功したのに圧縮後は失敗した実行軌跡を比較し、失われた重要情報を分析して自然言語の圧縮指示を改善する。

- **2025-03 · [Jenga: Effective Memory Management for Serving LLM with Heterogeneity](2025-2503.18292-jenga-heterogeneous-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  PagedAttentionは固定サイズのページでKVを割り当て、従来の連続領域確保よりメモリ断片化を減らした。論文のvLLMベース実装は、H100で要求処理量を平均1.80倍、最大4.92倍、L4で平均1.69倍、最大3.29倍へ改善した。

- **2025-02 · [QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache](2025-2502.10424-quantspec-self-speculative-decoding-with-hierarchical-quantized-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  QuantSpecは、長い文脈を持つ大規模言語モデルの復号で、鍵値キャッシュ（KVキャッシュ）の読出しがGPU帯域と容量を圧迫する問題を、階層量子化キャッシュを共有する自己投機的復号によって改善する。

- **2025-10 · [Attention Is All You Need for KV Cache in Diffusion LLMs](2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Elastic-Cache) ・ リポジトリ内被引用：23  
  従来の安全な実装は、各復号段階ですべての位置と層のクエリ・キー・値を再計算するが、変化の少ない状態まで繰り返し計算するため遅い。提案方式は、左側の未確定位置を中心とする移動窓で新しいトークンを予測し、窓外MASKのKVを再利用する。

- **2025-02 · [TransMLA: Migrating GQA Models to MLA with Full DeepSeek Compatibility and Speedup](2025-2502.07864-transmla-migrating-gqa-models-to-mla-with-full-deepseek-compatibility-an.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  TransMLAは、すでに学習済みのグループ化問い合わせ注意（Grouped Query 注意機構、GQA）モデルを、DeepSeek系の多頭潜在注意（Multi-head Latent 注意機構、MLA）へ変換するための手法である。

- **2025-05 · [PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs](2025-2505.18610-pm-kvq-progressive-mixed-precision-kv-cache-quantization-for-long-cot-llms.md)**  
  実装：[✓](https://github.com/thu-nics/PM-KVQ) ・ リポジトリ内被引用：22  
  KVを16→8→4→2bitと必要時だけ段階圧縮し、層感度とRoPE位置補間校正で長CoTの累積量子化誤差を抑えるPM-KVQ。

- **2025-11 · [TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection](2025-token-select.md)**  
  実装：[✓](https://github.com/pzs19/TokenSelect) ・ リポジトリ内被引用：21  
  各問い合わせで重要な鍵値をトークン単位に選び、ヘッド軟投票・選択キャッシュ・ページ化内積カーネルで長文脈注意を高精度かつ高速化する。

- **2025-06 · [InfiniPot-V: Memory-Constrained KV Cache Compression for Streaming Video Understanding](2025-2506.15745-infinipot-v-memory-constrained-kv-cache-compression-for-streaming-video-.md)**  
  実装：[✓](https://github.com/aiha-lab/InfiniPot-V) ・ リポジトリ内被引用：20  
  InfiniPot-Vは、動画を順次処理する映像言語モデルの鍵・値キャッシュ（KVキャッシュ）が、視聴時間とともに増加する問題を扱う。全映像のKVキャッシュをいったん構築してから圧縮する方式は、圧縮前の瞬間最大メモリが装置容量を超える。主要評価では、Qwen-2-VL-7Bの50Kトークン相当の動画文脈を6Kへ縮小しても、MLVU平均65.8を維持した。

- **2025-02 · [Online Scheduling for LLM Inference with KV Cache Constraints](2025-2502.07115-online-scheduling-for-llm-inference-with-kv-cache-constraints.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  本研究は、大規模言語モデル（LLM）の複数要求を一つの推論ワーカーで処理する際に、生成が進むほど増える鍵・値キャッシュ（KVキャッシュ）を将来時点まで予測し、どの要求をいつ開始するかを決めるオンラインスケジューリング（online スケジューラ）を扱う。

- **2025-11 · [KV Cache Transform Coding for Compact Storage in LLM Inference](2025-2511.01815-kv-cache-transform-coding-for-compact-storage-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  KVTCは共通の主成分分析基底でKVキャッシュの相関を減らし、重要度別の量子化と無損失符号化で保存量を縮める。16倍目標で多くの課題品質を概ね保ち、H100の8K文脈では復号再利用がKV再計算よりTTFTを約8倍短縮したが、処理時間と強圧縮時の品質低下も示す。

- **2025-02 · [CriticalKV: Optimizing KV Cache Eviction from an Output Perturbation Perspective](2025-2502.03805-criticalkv-optimizing-kv-cache-eviction-from-an-output-perturbation-perspective.md)**  
  実装：[✓](https://github.com/FFY0/DefensiveKV) ・ リポジトリ内被引用：18  
  KVキャッシュ追い出しを「注意出力摂動の最小化」として定式化し、注意重み×出力射影後の値状態ノルムで重要KVを選ぶ二段階方式により、既存3方式の圧縮損失を29データセット平均で半分超削減する。

- **2025-10 · [ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models](2025-2510.01290-thinkv-thought-adaptive-kv-cache-compression-for-efficient-reasoning-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  ThinKVは、長い思考過程を出力する推論型大規模言語モデル（large reasoning モデル; LRM）のKVキャッシュを、単純なトークン年齢や注意得点だけでなく、現在どの種類の思考区間を生成しているかに応じて圧縮する方式である。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：16  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-05 · [FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference](2025-2505.13109-freekv-boosting-kv-cache-retrieval-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/FreeKV) ・ リポジトリ内被引用：16  
  全KVをGPUメモリに保持すると長文脈・同時要求数の増加に耐えにくい。そこで全KVをCPUメモリに保持し、注意計算に必要なページだけGPUへ呼び戻す検索型圧縮が考えられる。原著の32K文脈・バッチ1の分析では、ArkValeの時間の約94%、ShadowKVの約73%が選択と呼び戻しに費やされる。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

- **2025-01 · [Cache Me If You Must: Adaptive Key-Value Quantization for Large Language Models](2025-2501.19392-cache-me-if-you-must-adaptive-key-value-quantization-for-large-language-.md)**  
  実装：[✓](https://github.com/goodevening13/aquakv) ・ リポジトリ内被引用：16  
  長文脈の大規模言語モデル（LLM）では、生成済みトークンの注意機構に使う鍵・値（KV）を各層に保存する。原著の例では、131,072トークンを保持するLlama 3.2 3Bの16ビットKVは約15 GiB、Llama 3.1 70Bでは約42.9 GB（論文の導入部における十進表記）を占める。

- **2025-05 · [Lookahead Q-Cache: Achieving More Consistent KV Cache Eviction via Pseudo Query](2025-2505.20334-lookahead-q-cache-achieving-more-consistent-kv-cache-eviction-via-pseudo.md)**  
  実装：[✓](https://github.com/noforit/Lookahead_Q-Cache) ・ リポジトリ内被引用：13  
  Lookahead Q-Cache（LAQ）は、大規模言語モデルの長文推論で、KVキャッシュをどの位置から削除するか決めるための観測窓を、入力末尾から仮に生成した回答の問い合わせベクトルへ変更する手法である。

- **2024-12 · [KunServe: Parameter-centric Memory Management for Efficient Memory Overloading Handling in LLM Serving](2024-2412.18169-kunserve-elastic-and-efficient-large-language-model-serving-with-paramet.md)**  
  実装：[✓](https://github.com/SJTU-IPADS/kunserve) ・ リポジトリ内被引用：13  
  リクエストのKVキャッシュを捨てる代わりに、複数の推論インスタンスに重複配置されたモデル重みを一時解放する。残存する層を複数GPUで協調実行し、通信とバッチ形成を調整することで、突発負荷時の待ち行列を短縮する。

- **2025-05 · [ReCalKV: Low-Rank KV Cache Compression via Head Reordering and Offline Calibration](2025-2505.24357-recalkv-low-rank-kv-cache-compression-via-head-reordering.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/ReCalKV) ・ リポジトリ内被引用：12  
  ReCalKVは、大規模言語モデルの長文推論で増大する鍵・値キャッシュ（KVキャッシュ）を、保存する隠れ次元の低ランク化によって削減する学習後圧縮方式である。既存の低ランクKV圧縮であるPaluと比較し、LLaMA-2-7BのKVを70%圧縮したとき、6つのゼロショット質問応答課題の平均はReCalKVが59.90%、Paluが52.14%だった。

- **2025-04 · [CAOTE: KV Cache Selection for LLMs via Attention Output Error-Based Token Eviction](2025-2504.14051-caote-kv-cache-selection-for-llms-via-attention-output-error-based-token.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  従来のH2O・TOVA・SnapKVなどは、主に注意重み（注意機構 score）を重要度の代理指標として利用する。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：10  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-03 · [Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving](2025-2503.24000-rethinking-key-value-cache-compression-techniques-for-large-language-mod.md)**  
  実装：[✓](https://github.com/LLMkvsys/rethink-kv-compression) ・ リポジトリ内被引用：10  
  鍵値キャッシュ（Key-Value Cache、KVキャッシュ）の圧縮は、大規模言語モデル（Large Language モデル、LLM）の復号で過去トークンの状態を保持するGPUメモリを減らす。

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  PRESERVEは、複数のGPUまたはNPUに大規模言語モデルを分割して実行する際、アクセラレータ間の集合通信が生む待ち時間を、次の演算に必要なメモリ読み出しへ転用する手法である。バッチ4、最大系列長16Kなどの条件で、先読みを行わない基準方式に対し端から端までの推論時間を1.09～1.61倍短縮した。

- **2025-09 · [EvolKV: Evolutionary KV Cache Compression for LLM Inference](2025-2509.08315-evolkv-evolutionary-kv-cache-compression-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  KVを削除すればメモリ容量を抑えられるが、どの層にどれだけの過去情報を残すかは回答品質に強く影響する。既存方式は全層に同じ保持数を割り当てるか、下層から上層へ単調に予算を減らすピラミッド型の規則を使うことが多い。

- **2025-09 · [EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments](2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-reso.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  一般的な事後圧縮は履歴全体を事前入力（プリフィル）してから不要なKVを削除するため、圧縮後の容量が小さくても処理途中のピークメモリを抑えられない。LongMemEval、RealTalk、LoCoMoを使った評価では、4～6倍のKV圧縮でも全KVに近い回答品質を示す条件がある。

- **2025-08 · [CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation](2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-b.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：8  
  文脈が長くなるほどKV容量と注意計算量が増え、GPUメモリ容量と応答遅延の制約が厳しくなる。第二に、極端に小さいKV予算で注意ブロックの出力がどれだけ変化するかをオフラインで測定し、圧縮に弱い層へ多くのKV予算を配る。

- **2025-11 · [PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel](2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md)**  
  実装：[✓](https://github.com/flashserve/PAT) ・ リポジトリ内被引用：7  
  共有接頭辞を要求間で一度だけ読む詰込みと動的タイル選択により、復号注意の大域メモリ読出しと実行空洞を同時に削減する。

- **2025-11 · [$A^3$: Attention-Aware Accurate KV Cache Fusion for Fast Large Language Model Serving](2025-2511.17560-a-3-attention-aware-accurate-kv-cache-fusion-for-fast-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  $A^3$（注意機構-Aware Accurate KV Cache Fusion）は、複数の質問で再利用される文書断片のKVキャッシュを事前に作り、質問に関係する部分だけを再計算して、長文入力の事前充填を高速化する手法である。Mistral-7B-Instruct-v0.2では全文計算38.27、A3が36.98で、再利用系の比較手法を上回った。

- **2025-09 · [PagedEviction: Structured Block-wise KV Cache Pruning for Efficient Large Language Model Inference](2025-2509.04377-pagedeviction-structured-block-wise-kv-cache-pruning-for-efficient-large.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  PagedEvictionは、推論サーバーvLLMで用いられるページ型KVキャッシュ管理（PagedAttention）と、KVキャッシュの重要度に基づく削除を両立させる方式である。

- **2025-08 · [KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache](2025-2509.00579-kvcomp-a-high-performance-llm-aware-lossy-compression-framework-for-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  KVCompは、大規模言語モデルの長文脈推論において、過去トークンの鍵・値（KV）キャッシュがGPUメモリを占有し、処理可能な文脈長や同時実行数を制限する問題に取り組む。既存の低ビット量子化だけでは整数符号に残る統計的偏りを使い切れず、一般的な可逆圧縮を追加すると毎トークン必要な復号が遅くなる。

- **2025-08 · [KV Cache Compression for Inference Efficiency in LLMs: A Review](2025-2508.06297-kv-cache-compression-for-inference-efficiency-in-llms-a-review.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  著者はKV圧縮を、重要なトークンを選んで残す方式、K/Vのビット幅を下げる量子化、注意構造やヘッドの冗長性を利用する方式、複数の技術を組み合わせる方式に分類する。

- **2025-04 · [SentenceKV: Efficient LLM Inference via Sentence-Level Semantic KV Caching](2025-2504.00970-sentencekv-efficient-llm-inference-via-sentence-level-semantic-kv-cachin.md)**  
  実装：[✓](https://github.com/zzbright1998/SentenceKV) ・ リポジトリ内被引用：7  
  SentenceKVは、長い入力を文ごとのまとまりに分け、文の意味を表す小さなキー索引だけをGPUに残して、個々の鍵・値（KV）対をCPU側へ退避する長文脈推論方式である。

- **2025-03 · [Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs](2025-2503.00979-dialogue-without-limits-constant-sized-kv-caches-for-extended-responses-.md)**  
  実装：[✓](https://github.com/ghadiaravi13/MorphKV) ・ リポジトリ内被引用：7  
  従来のSnapKVのように入力側のキャッシュを圧縮しても、生成済みトークンをすべて残す実装では出力長に比例する増大を止められない。要旨の「52.9%節約、18.2%品質改善」は、長文応答タスクにおける比較対象H2Oとの平均比較であり、全注意に対する普遍的な改善率ではない。

- **2025-02 · [Quantize What Counts: More for Keys, Less for Values](2025-2502.15075-quantize-what-counts-more-for-keys-less-for-values.md)**  
  実装：[✓](https://github.com/mohsenhariri/spectral-kv) ・ リポジトリ内被引用：7  
  キー射影のノルムがバリュー射影より大きいという定理と、キー優先のビット配分が量子化誤差を最小化するという定理で、KVキャッシュ量子化のビット配分を理論づけた研究。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-10 · [Which Heads Matter for Reasoning? RL-Guided KV Cache Compression](2025-2510.08525-which-heads-matter-for-reasoning-rl-guided-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  既存のKV削除手法は、検索・要約型のタスクで重要なトークンや注意ヘッドを見つけるが、数千トークンに及ぶ推論途中の自己修正・論理的一貫性・終了判断を保つためのヘッドと必ずしも一致しない。

- **2025-07 · [OracleKV: Oracle Guidance for Question-Independent KV Cache Eviction](2025-598fc6b87732-oraclekv-oracle-guidance-for-question-independent-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  質問が来る前に文脈だけを削らなければならない場面で、将来の質問の型と必要情報の統計を文章化したガイダンスを文脈末尾へ付け、その注意スコアで残す鍵値項目を選ぶことで、予算10パーセントでも検索系課題の精度を大きく保つ追い出し方式。

- **2025-06 · [MadaKV: Adaptive Modality-Perception KV Cache Eviction for Efficient Multimodal Long-Context Inference](2025-2506.15724-madakv-adaptive-modality-perception-kv-cache-eviction-for-efficient-mult.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  MadaKVは、各注意ヘッドが画像と文字のどちらへ注意を向けているかを測り、モダリティごとに異なるKV保持予算を割り当てるModality Preference Adaptation（MPA）と、層ごとの圧縮過不足を後続層へ補償するHierarchical Compression Compensation（HCC）を組み合わせる。

- **2025-05 · [Mustafar: Promoting Unstructured Sparsity for KV Cache Pruning in LLM Inference](2025-2505.22913-mustafar-promoting-unstructured-sparsity-for-kv-cache-pruning-in-llm-inf.md)**  
  実装：[✓](https://github.com/dhjoo98/mustafar) ・ リポジトリ内被引用：6  
  Mustafarは、大規模言語モデル（LLM）の逐次生成時に蓄積する鍵・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を、トークンごと・要素ごとの非構造化枝刈り（unstructured 枝刈り）で圧縮し、その圧縮形式をGPUの注意演算へ直接渡す方式である。

- **2025-11 · [Lethe: Layer- and Time-Adaptive KV Cache Pruning for Reasoning-Intensive LLM Serving](2025-2511.06029-lethe-layer-and-time-adaptive-kv-cache-pruning-for-reasoning-intensive-l.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Letheは、長い思考過程を文章として生成する大規模言語モデル（LLM）の推論時に、鍵・値キャッシュ（KVキャッシュ）を保持し続けることによるメモリ消費と注意計算の増大を抑える方式である。

- **2025-10 · [TALE: Token-Adaptive Low-Rank KVCache Approximation with Reconstruction Elimination](2025-ffb681f1a4fd-tale-token-adaptive-low-rank-kvcache-approximation-with-reconstruction-e.md)**  
  実装：[✓](https://github.com/thnkinbtfly/TALE) ・ リポジトリ内被引用：5  
  TALE（トークン-適応的 Low-Rank KVCache Approximation with Reconstruction Elimination）は、既存の大規模言語モデル（LLM）の重みを再学習せずに、生成時のキー・バリューキャッシュ（KV キャッシュ）を削減する方式である。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-07 · [Forecasting LLM Inference Performance via Hardware-Agnostic Analytical Modeling](2025-2508.00904-forecasting-llm-inference-performance-via-hardware-agnostic-analytical-m.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  入力長、出力長、注意機構、量子化、演算融合、カーネルの効率が時間とともに変わるためである。Llama2-7Bを対象に、プレフィル（プリフィル）で入力長256から65,536へ増やすと、行列積（GEMM）の計算量構成比が99.0%から27.5%へ下がり、バッチ行列積（BMM）が1.0%から71.6%へ増えると推計した（表4）。

- **2025-05 · [NSNQuant: A Double Normalization Approach for Calibration-Free Low-Bit Vector Quantization of KV Cache](2025-2505.18231-nsnquant-a-double-normalization-approach-for-calibration-free-low-bit-ve.md)**  
  実装：[✓](https://github.com/DHdroid/NSNQuant) ・ リポジトリ内被引用：5  
  重みを低ビット化しても、生成が長くなると過去トークンの鍵・値（KV）がGPUメモリを占有し、同時に処理できる要求数が減る。NSNQuantは、このKVを1ビットまたは2ビット相当のベクトル量子化で保存する方式である。

- **2025-05 · [LoLA: Low-Rank Linear Attention with Sparse Caching](2025-2505.23666-lola-low-rank-linear-attention-with-sparse-caching.md)**  
  実装：[✓](https://github.com/lukemcdermotttt/LoLA-release) ・ リポジトリ内被引用：5  
  LoLA（Low-Rank Linear 注意機構 with Sparse Caching）は、線形注意（Linear 注意機構）が長い文脈を固定長の再帰状態に圧縮する際に失いやすい、個別の鍵と値の対応関係を守るための推論時キャッシュ管理方式である。

- **2025-05 · [FreqKV: Key-Value Compression in Frequency Domain for Context Window Extension](2025-2505.00570-freqkv-key-value-compression-in-frequency-domain-for-context-window-exte.md)**  
  実装：[✓](https://github.com/LUMIA-Group/FreqKV) ・ リポジトリ内被引用：5  
  全履歴を保持する方式では文脈長に応じてKV容量が増え、長い事前入力では注意の計算量も増える。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：5  
  本研究は、大規模言語モデルの自己回帰復号において、鍵値キャッシュ（KV キャッシュ）を高帯域メモリ（HBM）から読み込む間にGPUの実行単位が待たされる問題を対象とする。鍵値を削除・量子化・オフロードして保存容量を減らすのではなく、現在の鍵値ブロックを使った注意演算と、次に必要なブロックのHBMから二次キャッシュ（L2 キャッシュ）への転送を重ねる。

- **2024-12 · [More Tokens, Lower Precision: Towards the Optimal Token-Precision Trade-off in KV Cache Compression](2024-2412.12706-more-tokens-lower-precision-towards-the-optimal-token-precision-trade-of.md)**  
  実装：[✓](https://github.com/zhzihao/QPruningKV) ・ リポジトリ内被引用：5  
  KVキャッシュの容量制約下で、残すトークン数と量子化精度を別々に決めず、両者の積で予算を配分する「量子化付き間引き」を検証した研究。

- **2025-10 · [VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization](2025-2510.06175-vecinfer-efficient-llm-inference-with-low-bit-kv-cache-via-outlier-suppr.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  キャッシュ量は文脈長に比例して増えるため、長い入力を扱う際にはGPUの高帯域メモリ（HBM）容量が不足し、デコード中の読み出し量も大きくなる。ベクトル量子化（VQ）は複数要素を一つの代表ベクトルへ対応付け、各小ベクトルを短い索引として保存する。長文脈192K入力・129出力のH100単一バッチでは、2ビット構成でデコード遅延が8.3倍改善した。

- **2025-10 · [GUI-KV: Efficient GUI Agents via KV Cache with Spatio-Temporal Awareness](2025-2510.00536-gui-kv-efficient-gui-agents-via-kv-cache-with-spatio-temporal-awareness.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GUI-KV) ・ リポジトリ内被引用：4  
  論文はUI-TARS-1.5-7Bについて、5画面・最大50段階の条件でGPUメモリ消費が80GBを超え得ると説明し、単なる計算高速化ではなく、履歴を保持するためのメモリ節約を主課題とする。GUI-KVは、自然画像用の圧縮方式をそのまま転用せず、画面固有の二種類の冗長性を利用する。

- **2025-08 · [SmallKV: Small Model Assisted Compensation of KV Cache Compression for Efficient LLM Inference](2025-2508.02751-smallkv-small-model-assisted-compensation-of-kv-cache-compression-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  SmallKVは、長文脈の大規模言語モデル（LLM）の鍵・値キャッシュ（KV キャッシュ）を小さくする際、単純な重要度順位でトークンを消してしまうと必要な情報が失われる問題を、小型言語モデル（Small Language モデル; SLM）との協調で緩和する方式である。

- **2025-08 · [Selective KV-Cache Sharing to Mitigate Timing Side-Channels in LLM Inference](2025-2508.08438-selective-kv-cache-sharing-to-mitigate-timing-side-channels-in-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  SafeKVは、大規模言語モデル（LLM）の複数利用者向けサービングにおいて、プレフィックスのKVキャッシュを利用者間で共有する性能上の利益と、共有によるタイミング情報漏えいを両立させるシステムである。

- **2025-06 · [AnTKV: Anchor Token-Aware Sub-Bit Vector Quantization for KV Cache in Large Language Models](2025-2506.19505-antkv-anchor-token-aware-sub-bit-vector-quantization-for-kv-cache-in-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  AnTKVは、TransformerのKVキャッシュを極端に低いビット幅へ圧縮したときの品質劣化を、トークンごとの誤差感度が均一ではないという観察から抑える方式である。FP16のアンカーが全体の1%でも、1bit以下の領域で大きな品質改善が報告される。

- **2025-05 · [KVmix: Gradient-Based Layer Importance-Aware Mixed-Precision Quantization for KV Cache](2025-2506.08018-kvmix-gradient-based-layer-importance-aware-mixed-precision-quantization.md)**  
  実装：[✓](https://github.com/LfLab-AI/KVmix) ・ リポジトリ内被引用：4  
  KVmixは、長い文脈や多数の同時要求でGPUメモリを圧迫するKVキャッシュを、モデルの品質に影響しやすい層と影響しにくい層に分けて量子化する方式である。RTX 4090 24GBで入力688トークン・最大生成1024トークンの実験では、最大バッチサイズを増やせることを含めた処理率が194.06から1032.06 トークン/sへ上昇する。

- **2025-03 · [Efficient Many-Shot In-Context Learning with Dynamic Block-Sparse Attention](2025-2503.08640-efficient-many-shot-in-context-learning-with-dynamic-block-sparse-attent.md)**  
  実装：[✓](https://github.com/millix19/dbsa) ・ リポジトリ内被引用：4  
  通常の多数例ICLは、同じモデルを複数の分類課題へ転用できる反面、数千件の入力・正解ラベル例を毎要求の文脈へ入れるため推論が高価になる。動的 Block-Sparse 注意機構（DBSA）はこの二者を分離する。第2段階では、BM25によって要求に関連するブロックを30%検索し、保存したKV断片を連結し直してから新しい要求を生成する。

- **2025-11 · [FlowMM: Cross-Modal Information Flow Guided KV Cache Merging for Efficient Multimodal Context Inference](2025-2511.05534-flowmm-cross-modal-information-flow-guided-kv-cache-merging-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FlowMMは画像と文章が混在する多模態大規模言語モデル（MLLM）の推論時に、注意のキー・値キャッシュ（KVキャッシュ）を破棄ではなく結合によって圧縮する方式である。KV保持予算20%では、InternVL2.5-8Bの平均指標が全KV保持の27.97から27.85へと0.12ポイントの低下にとどまる。

- **2025-11 · [FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management](2025-2511.00868-flexicache-leveraging-temporal-stability-of-attention-heads-for-efficient-kv-cache-management.md)**  
  実装：[✓](https://github.com/NazmulTakbir/FlexiCache) ・ リポジトリ内被引用：3  
  重要KVページが時間的に入れ替わりやすい注意ヘッドだけ全KVをGPUへ残し、安定ヘッドは上位ページ以外をCPUへ退避・周期再昇格することで、精度を保ちながらGPUメモリを最大70%削減する。

- **2025-10 · [Improving Model Representation and Reducing KV Cache via Skip Connections with First Value Heads](2025-2510.16807-improving-model-representation-and-reducing-kv-cache-via-skip-connection.md)**  
  実装：[✓](https://github.com/Zhoutong-Wu/SkipV1Former) ・ リポジトリ内被引用：3  
  このKVキャッシュは系列長、層数、ヘッド数、同時要求数に比例して増えるため、長文脈推論ではモデル重みと並ぶGPUメモリの制約になる。反対に、残差経路を増やして浅い情報を深い層へ伝える方式は、品質を改善してもKVキャッシュを減らさないことが多い。

- **2025-09 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2025-2509.21623-ojakv-context-aware-online-low-rank-kv-cache-compression.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：3  
  OjaKVは長文脈言語モデルのキー・バリュー（KV）キャッシュを低ランク射影で圧縮する際、校正データで決めた固定基底が実際の会話・コード・ニュースなどの分布変化に適合しなくなる問題を扱う。LongChat-7B-v1.5-32kの16K RULERでは、KV保存予算0.6倍の条件で静的PCAの平均正答率23.44%をOjaKVが39.99%へ改善した。

- **2025-07 · [Multi-matrix Factorization Attention](2025-98e1f6bbeb53-multi-matrix-factorization-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  自己回帰型の大規模言語モデルでは、生成済みトークンの鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を保存することで、次のトークンを生成するたびに過去系列を再計算せずに済む。12個の評価指標の平均はMHA 49.0、MFA 49.9、MFA-KR 48.0で、MFAは少ないキャッシュ量でも比較対象のMHAをわずかに上回った。

- **2025-07 · [HCAttention: Extreme KV Cache Compression via Heterogeneous Attention Computing for LLMs](2025-2507.19823-hcattention-heterogeneous-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  キー量子化・値のCPU退避・層別の動的KV削除を統合し、GPU KV予算25%でLlama-3-8BのLongBench平均43.2を全注意と同値に保ち、12.5%でも42.5（0.7ポイント差）に抑える異種GPU/CPU注意方式。

- **2025-06 · [AhaKV: Adaptive Holistic Attention-Driven KV Cache Eviction for Efficient Inference of Large Language Models](2025-2506.03762-ahakv-adaptive-holistic-attention-driven-kv-cache-eviction-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  AhaKVは、LLM推論でKVキャッシュを固定予算へ圧縮するとき、過去トークンの重要度を累積注意スコアだけで決めることの偏りを修正する方式である。

- **2025-03 · [Slim attention: cut your context memory in half without loss – K-cache is all you need for MHA](2025-2503.05840-slim-attention-cut-your-context-memory-in-half-without-loss-k-cache-is-a.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  値射影をキー射影の逆行列で変換し、値をキーキャッシュから等価に復元して文脈メモリを半分にする無損失狙いの注意機構。長文脈の生成を最大2倍速くする。

- **2025-02 · [Compression Barriers in Autoregressive Transformers](2025-2502.15955-compression-barriers-in-autoregressive-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  近年のKV圧縮は重要トークンの選択、疎性、低次元表現、クラスタリング等で保存量を削減しているが、これらの成功が任意の入力でも保証できるかは別問題である。

- **2025-01 · [MPCache: MPC-Friendly KV Cache Eviction for Efficient Private LLM Inference](2025-2501.06807-mpcache-mpc-friendly-kv-cache-eviction-for-efficient-private-llm-inferen.md)**  
  実装：[✓](https://github.com/zwxandy/MPCache) ・ リポジトリ内被引用：3  
  大規模言語モデル（LLM）のKVキャッシュ圧縮は、通常のGPU推論では過去トークンの一部を削除・選択することで注意計算量とメモリを減らす。さらに粗いクラスタから細かいクラスタへ選択を絞り、近接Transformer層の選択インデックスを共有することで、MPC特有の比較と秘密インデックスgatherの費用を削減する。

- **2024-12 · [XKV: Personalized KV Cache Memory Reduction for Long-Context LLM Inference](2024-2412.05896-xkv-personalized-kv-cache-memory-reduction-for-long-context-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  トークンの重要度に基づいて一部のKVを捨てる方式はあるが、各Transformer層へ同じ容量を割り当てたり、層位置に応じてあらかじめ決めたピラミッド形の容量を割り当てたりすると、入力とタスクごとに変わる重要度分布を捉えきれない。

- **2025-11 · [Revisiting Multimodal KV Cache Compression: A Frequency-Domain-Guided Outlier-KV-Aware Approach](2025-2511.16786-revisiting-multimodal-kv-cache-compression-a-frequency-domain-guided-out.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FlashCacheは、画像・動画を扱う視覚言語モデルの長文入力で膨らむ鍵・値キャッシュ（KVキャッシュ）を、注意スコアを再計算せずに削減する方式である。著者は単一NVIDIA H200 141GBで、KV保持率20%の長文復号において最大1.69倍の速度を報告する。

- **2025-10 · [LouisKV: Efficient KV Cache Retrieval for Long Input-Output Sequences](2025-2510.11292-louiskv-efficient-kv-cache-retrieval-for-long-input-output-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈LLMでは、過去トークンのKeyとValueをKVキャッシュに保存することで自己回帰生成時の再計算を避ける。単一NVIDIA A6000上でArkvaleと比較したエンドツーエンド遅延の最大高速化は、長入力・短出力1.9倍、短入力・長出力2.9倍、長入力・長出力4.7倍である。

- **2025-09 · [Adaptive KV-Cache Compression without Manually Setting Budget](2025-2509.03136-adaptive-kv-cache-compression-without-manually-setting-budget.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  提案の核は、現在のqueryだけに高い注意を払われたキーを残すのではなく、将来の複数queryが必要としそうなキーの和集合を近似することにある。

- **2025-08 · [PiKV: KV Cache Management System for Mixture of Experts](2025-2508.06526-pikv-kv-cache-management-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/NoakLiu/PiKV) ・ リポジトリ内被引用：2  
  混合専門家モデルのKVを専門家単位に分散し、選択・圧縮・保持判断を統合する設計。第3版本文には独立した実測評価節がない。

- **2025-08 · [GraphKV: Breaking the Static Selection Paradigm with Graph-Based KV Cache Eviction](2025-2509.00388-graphkv-breaking-the-static-selection-paradigm-with-graph-based-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GraphKVは、長文脈のKVキャッシュ削減で「注意スコアの上位をそのまま残すと、互いに似た情報を持つトークンが重複して選ばれる」という問題を扱う。一方、QMSumのデコード遅延はPyramidKV単独5.133秒に対して併用5.265秒と2.5%悪化しており、すべての既存方式を高速化するという主張は成立しない。

- **2025-07 · [ReasonCache: Accelerating Large Reasoning Model Serving through KV Cache Sharing](2025-2507.21433-reasoncache-accelerating-large-reasoning-model-serving-through-kv-cache-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  生成トークンが増えると、過去のトークンに対応するキー・バリュー（KV）キャッシュも伸び、GPUメモリを圧迫する。ReasonCacheは似た思考ステップに対応するKVブロックが内部表現上も似ているという観測を利用し、既に保持している物理ブロックを新しい論理位置から参照することで、KVの実体数を減らす方式である。

- **2025-07 · [Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing](2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  対話ごとの注意類似度から層間の鍵・値共有を動的選択し、注意類似度計算を中央処理装置と画像処理装置へ分担、圧縮後の再計算とロードを層間パイプラインで重畳してマルチターン状態復元を高速・省容量化する。

- **2025-05 · [Addressing Activation Outliers in LLMs: A Systematic Review of Post-Training Quantization Techniques](2025-26c8fc4003ac-addressing-activation-outliers-in-llms-a-systematic-review-of-post-train.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  活性値の外れ値に絞った学習後量子化の系統的レビュー。PRISMAで選んだ52件を等価変換・混合精度・細粒度化・非線形データ型の4群へ分類し、どのビット幅でどの対策が要るかを困惑度の横断比較で示した。

- **2025-02 · [CalibQuant: 1-Bit KV Cache Quantization for Multimodal LLMs](2025-2502.14882-calibquant-1-bit-kv-cache-quantization-for-multimodal-llms.md)**  
  実装：[✓](https://github.com/insuhan/calibquant) ・ リポジトリ内被引用：2  
  主張は、視覚トークンのKVキャッシュを圧縮し、限られたメモリ予算下でバッチ数を増やしてデコードスループットを上げることであり、モデル重みを1bit化する方式ではない。主結果はCOCO Caption、DocVQA、MMBench-VideoとH100 80GBでのスループット評価である。

- **2024-12 · [EMS: Adaptive Evict-then-Merge Strategy for Head-wise KV Cache Compression Based on Global-Local Importance](2024-2412.08521-ems-adaptive-evict-then-merge-strategy-for-head-wise-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  EMS（適応的 Evict-then-Merge Strategy）は、重要度の計測と実際の圧縮を分離する。最大10.75倍のスループット改善も報告するが、これは実行可能な最大バッチサイズが変わる条件での比較であり、単一要求の10.75倍高速化ではない。

- **2025-11 · [SWAN: Sparse Winnowed Attention for Reduced Inference Memory via Decompression-Free KV-Cache Compression](2025-2511.18936-swan-sparse-winnowed-attention-for-reduced-inference-memory-via-decompre.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SWAN（Sparse Winnowed 注意機構）は、大規模言語モデルの生成時に増え続ける鍵・値キャッシュ（key-value キャッシュ、KVキャッシュ）を、次元方向に疎な形式へ変換して保存する方式である。50～60%程度のKVメモリ削減で多くの課題の性能が保たれると報告する一方、保持次元を減らしすぎると数学推論が大きく悪化する。

- **2025-10 · [PatternKV: Flattening KV Representation Expands Quantization Headroom](2025-2510.05176-patternkv-flattening-kv-representation-expands-quantization-headroom.md)**  
  実装：[✓](https://github.com/HCOOOH/PatternKV) ・ リポジトリ内被引用：1  
  KVキャッシュを保持することで過去トークンの注意計算を省ける一方、文脈長、同時リクエスト数、複数回答を生成する推論時スケーリングに比例してキャッシュが膨らむ。著者は複数モデル平均でFP16との差が0.08%と要約するが、これは個別モデルの全タスクで差がゼロという意味ではない。

- **2025-10 · [Breadcrumbs Reasoning: Memory-Efficient Reasoning with Compression Beacons](2025-2510.13797-breadcrumbs-reasoning-memory-efficient-reasoning-with-compression-beacon.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Breadcrumbs Reasoning（BR）は、生成を一定数進めるたびに専用の圧縮ビーコンをモデルへ入力し、直前の生成トークンのKVをビーコン1個のKVへ置換する。

- **2025-08 · [Spotlight Attention: Towards Efficient LLM Generation via Non-linear Hashing-based KV Cache Retrieval](2025-2508.19740-spotlight-attention-towards-efficient-llm-generation-via-non-linear-hash.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Spotlight 注意機構は、大規模言語モデル（LLM）の長文脈生成で、過去の鍵・値キャッシュ（KV キャッシュ）のうち現在の問い合わせに重要な少数トークンだけを取り出して注意計算を行う方式である。A100単体で512Kトークンに対するハッシュ検索を100マイクロ秒未満とし、通常の全注意デコードに比べ端から端まで最大約3倍のスループットを示した。

- **2025-07 · [FAEDKV: Infinite-Window Fourier Transform for Unbiased KV Cache Compression](2025-2507.20030-faedkv-infinite-window-fourier-transform-for-unbiased-kv-cache-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  H2OやSnapKVのようなトークン削除はメモリを節約する一方、直近の注意や頻出トークンを重視し、後から必要になる古い情報を消す場合がある。学習済み圧縮器は別途学習費用を要し、過去の圧縮表現を繰り返し更新すると古い情報が劣化する可能性もある。

- **2025-07 · [ClusterAttn: KV Cache Compression under Intrinsic Attention Clustering](2025-2af879bf02e3-clusterattn-kv-cache-compression-under-intrinsic-attention-clustering.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  デコード中に注意がプロンプト内の安定したクラスタへ集まる現象を利用し、観測ウィンドウで集約した注意重要度を密度ベースにクラスタリングしてプロンプトのKVキャッシュを圧縮する学習不要の方式ClusterAttn。

- **2025-06 · [TaDA: Training-free recipe for Decoding with Adaptive KV Cache Compression and Mean-centering](2025-2506.04642-tada-training-free-recipe-for-decoding-with-adaptive-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TaDAは、自己回帰型の大規模言語モデル（LLM）で生成済みトークンの鍵・値を保存するKVキャッシュを、重み再学習なしに小さくする方式である。これは容量を27%まで削減したという意味であり、「27%だけ削減」とは異なる。

- **2025-05 · [SubGCache: Accelerating Graph-based RAG with Subgraph-level KV Cache](2025-2505.10951-subgcache-accelerating-graph-based-rag-with-subgraph-level-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  バッチ内のクエリを検索部分グラフの埋め込みでクラスタリングし、クラスタ代表部分グラフのKVキャッシュを共有することで、グラフ型検索拡張生成の初回トークン時間を最大6.68倍短縮するサブグラフ単位のキャッシュ。

- **2025-05 · [EFIM: Efficient Serving of LLMs for Infilling Tasks with Improved KV Cache Reuse](2025-2505.21889-efim-infilling-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/gty111/EFIM) ・ リポジトリ内被引用：1  
  FIMの増分を末尾へ移して接頭部・接尾部KVを要求間再利用し、断片トークン化学習で語途中生成能力を補って平均遅延52%削減・スループット98%向上。

- **2025-03 · [WindowKV: Task-Adaptive Group-Wise KV Cache Window Selection for Efficient LLM Inference](2025-2503.17922-windowkv-task-adaptive-group-wise-kv-cache-window-selection-for-efficien.md)**  
  実装：[✓](https://github.com/optim996/WindowKV) ・ リポジトリ内被引用：1  
  長い入力をプリフィルした後、全トークンの鍵・値を全層で保持すると、生成中にKVキャッシュがGPUメモリを圧迫する。WindowKVは連続したレビュー窓を単位に選び、入力タスクに応じて窓のスコア付けを切り替える。著者は全KVの約12%の容量で同等に近い品質を報告する。

- **2025-02 · [CoKV: Optimizing KV Cache Allocation via Cooperative Game](2025-2502.17501-cokv-optimizing-kv-cache-allocation-via-cooperative-game.md)**  
  実装：[✓](https://github.com/nawei1010/CoKV) ・ リポジトリ内被引用：1  
  Mistral-7B-Instruct-v0.2をA100 40GBで動かした実測では、28kトークン入力の生成総時間がFullKVの半分未満、32k入力のピークGPUメモリは64%削減された。オンライン要求ごとにゲーム理論の評価をやり直す方式ではない。

- **2025-01 · [TreeKV: Smooth Key-Value Cache Compression with Tree Structures](2025-2501.04987-treekv-smooth-key-value-cache-compression-with-tree-structures.md)**  
  実装：[✓](https://github.com/ZiweiHe/TreeKV) ・ リポジトリ内被引用：1  
  過去KVの一部だけを残す方法は以前からあるが、単純な「先頭と末尾の固定窓」は中間の重要情報を落とし、注意重みが大きいものを全履歴から貪欲に選ぶ方式は特定領域へ保持位置が偏りやすい。

- **2025-01 · [StagFormer: Time Staggering Transformer Decoding for RunningLayers In Parallel](2025-2501.15665-stagformer-time-staggering-transformer-decoding-for-runninglayers-in-par.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  層をスタックに分け、上位スタックの依存を1時刻前へずらすことでデコード時に深さ方向の並列実行を可能にするアーキテクチャStagFormerを提案し、品質維持と引き換えにKVキャッシュ増加と追加計算を伴うことを示した研究。

- **2024-12 · [CSR: Achieving 1 Bit Key-Value Cache via Sparse Representation](2024-2412.11741-csr-achieving-1-bit-key-value-cache-via-sparse-representation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVキャッシュを学習済み辞書による疎表現へ変換し、インデックスと係数だけを保存して1ビット相当まで圧縮する手法。量子化が届かない2ビット未満でも長文脈タスクの性能を大きく保つ。

- **2025-11 · [End-to-End Transformer Acceleration Through Processing-in-Memory Architectures](2025-2601.14260-end-to-end-transformer-acceleration-through-processing-in-memory-archite.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  抵抗変化メモリ型のメモリ内計算でTransformerを丸ごと速くするため、中間結果の再書込みを行列分解で消し、KVキャッシュを枝刈りと量子化の直列圧縮で生成中に縮め、注意を最近傍検索へ読み替える三点セットの統合設計。

- **2025-10 · [Position-Adaptive Temporal Sparsity for KV Caches in Long-Context LLMs](2025-65a0133f5916-position-adaptive-temporal-sparsity-for-kv-caches-in-long-context-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュの各エントリの仮数下位ビットをトークン位置に応じて切り捨て、全トークンを残したままキャッシュを最大42パーセント削減し、最適スケジュールではパープレキシティ増加0.9パーセントで35.9パーセント削減を達成する位置適応型の圧縮。

- **2025-10 · [Cortex: Workflow-Aware Resource Pooling and Scheduling for Agentic Serving](2025-2510.14126-cortex-workflow-aware-resource-pooling-and-scheduling-for-agentic-servin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントワークフローの段階ごとに専用エンジンプールを割り当てる段階分離で、段階間の干渉とKVキャッシュの重複保持を断ち、段階単位の増強と優先度付けを可能にするワークフロー認識型サービング基盤のプロトタイプ（定量評価は未報告）。

- **2025-09 · [ChunkLLM: A Lightweight Pluggable Framework for Accelerating LLMs Inference](2025-2510.02361-chunkllm-a-lightweight-pluggable-framework-for-accelerating-llms-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ChunkLLMは、既存Transformerのbackboneを固定したまま軽量なadapterを付加し、長文のどのchunkのKVを保持するかを学習する方式である。Qwen2.5-7BのLongBenchでは、通常モデルの平均44.13に対してChunkLLMは43.53、KV保持率は48.58%である。

- **2025-08 · [Unifying Mixture of Experts and Multi-Head Latent Attention for Efficient Language Models](2025-2508.01261-unifying-mixture-of-experts-and-multi-head-latent-attention-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Unifying Mixture of エキスパート and Multi-Head Latent 注意機構 for Efficient Language Modelsは、小型言語モデルの計算量とKVキャッシュ量を同時に抑えるため、Mixture-of-Experts（MoE）、Multi-head Latent 注意機構（MLA）…

- **2025-07 · [EARN: Efficient Inference Acceleration for LLM-based Generative Recommendation by Register Tokens](2025-2507.00715-earn-efficient-inference-acceleration-for-llm-based-generative-recommend.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.15553291) ・ リポジトリ内被引用：0  
  入力の両端に置いたレジスタトークンへ浅い層で履歴情報を集約し、深い層ではプロンプトを捨ててレジスタだけを処理することで、生成推薦の推論を最大3.79倍速くしKVキャッシュを最大80.8パーセント削りながら推薦精度を保ち向上させる方式。

- **2025-07 · [CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration](2026-2608.30295-catekv-on-sequential-consistency-for-long-context-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/haoyun-jiang/CateKV) ・ リポジトリ内被引用：0  
  プリフィルからデコードまで注意先が安定するヘッドだけKVを強く削減し、動的ヘッドは大半を保持するハイブリッドKVキャッシュで、精度を保ちながら長文推論のメモリ・デコード・バッチ性能を改善する。

- **2025-06 · [VEDA: Efficient LLM Generation Through Voting-based KV Cache Eviction and Dataflow-flexible Accelerator](2025-2507.00797-veda-efficient-llm-generation-through-voting-based-kv-cache-eviction-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各トークンの適応しきい値による投票でKVキャッシュを追い出し、内積・外積切替可能なデータフローと要素直列スケジューリングで生成フェーズを高速化するエッジ向けアクセラレータ。エビクションで注意が最大10倍高速になる。

- **2025-05 · [Efficient Multi-modal Long Context Learning for Training-free Adaptation](2025-2505.19812-efficient-multi-modal-long-context-learning-for-training-free-adaptation.md)**  
  実装：[✓](https://github.com/Zehong-Ma/EMLoC) ・ リポジトリ内被引用：0  
  実演例の文脈を塊ごとに分け、各層で出力分布の発散が上限以下になる最小の保持率を探して鍵値キャッシュを圧縮することで、文脈を約四・四倍に縮めながら精度を素の長文脈方式以上に保った。

- **2025-04 · [UniCAIM: A Unified CAM/CIM Architecture with Static-Dynamic KV Cache Pruning for Efficient Long-Context LLM Inference](2025-2504.07479-unicaim-a-unified-cam-cim-architecture-with-static-dynamic-kv-cache-prun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FeFETの統一アレイで動的枝刈り・静的枝刈り・厳密注意計算を3モード切替で実行するCIMアクセラレータ。定数時間の上位k選択と同一サイクルの累積で、AEDPを最大831倍改善する。

- **2025-04 · [SubKV: Quantizing Long Context KV Cache for Sub-billion Parameter Language Models on Edge Devices](2025-cf4ae1fdc15a-subkv-quantizing-long-context-kv-cache-for-sub-billion-parameter-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  10億パラメータ前後の小型言語モデルは重み容量が比較的小さいが、生成が長くなると過去トークンの鍵・値（KV）キャッシュが増え、端末側のメモリを圧迫する。ZengらのSubKVは、鍵をチャネル別、値をトークン別に量子化する非対称な粒度を採用し、直近の重要なトークンと先頭の注意集中領域を高精度で残す。

- **2025-04 · [EdgePrompt: A Distributed Key-Value Inference Framework for LLMs in 6G Networks](2025-2504.11729-edgeprompt-a-distributed-key-value-inference-framework-for-llms-in-6g-ne.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プロンプトをクラウド側とエッジ側へ分け、KVペア同期で層ごとに注意を融合することで個人情報をエッジに残したままクラウドの計算を使う分散KV推論枠組みで、エッジ配置のスループットでPagedAttention比最大約50パーセントの優位を図上で示した。

- **2025-03 · [Time and Memory Trade-off of KV-Cache Compression in Tensor Transformer Decoding](2025-2503.11108-time-and-memory-trade-off-of-kv-cache-compression-in-tensor-transformer-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ところが、複数のキー・値を組み合わせる高次のテンソル 注意機構では、元のキー・値を保持するか、組み合わせたキー・値を事前展開して保持するかで、より極端な時間と記憶量の交換条件が現れる。

- **2025-03 · [LogQuant: Log-Distributed 2-Bit Quantization of KV Cache with Superior Accuracy Preservation](2025-2503.19950-logquant-log-distributed-2-bit-quantization-of-kv-cache-with-superior-ac.md)**  
  実装：[✓](https://github.com/Concyclics/LogQuantKV) ・ リポジトリ内被引用：0  
  LogQuantは、長文脈のLLM推論で増大する鍵・値キャッシュ（KVキャッシュ）を2bitへ圧縮しつつ、重要な位置を選択的に元の精度で残す手法である。Llama-3.1-8B-Instructでは、GSM8Kの最終回答正答率が2bit KiViの18.04%に対してLogQuantの40.41%へ改善する（論文Table 4）。

- **2025-02 · [BaKlaVa - Budgeted Allocation of KV cache for Long-context Inference](2025-2502.13176-baklava-budgeted-allocation-of-kv-cache-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BaKlaVaは、長文脈のLLM推論でKVキャッシュを削減する際、全注意ヘッドへ同じ保持容量を与えるのではなく、重要度の高いヘッドへ多く、低いヘッドへ少なく配分する方式である。

- **2024-12 · [Boosting Long-Context Management via Query-Guided Activation Refilling](2024-2412.12486-boosting-long-context-management-via-query-guided-activation-refilling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュを全体要約のL1と詳細のL2の2層に分け、クエリに応じて必要な詳細だけをL1へ補充する長文脈処理手法。要約だけ・検索だけの方式より幅広い情報ニーズへ対応し、窓を超える文脈でも動く。

- **2024-12 · [Batch-Max: Higher LLM Throughput using Larger Batch Sizes and KV Cache Compression](2024-2412.05693-batch-max-higher-llm-throughput-using-larger-batch-sizes-and-kv-cache-co.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存のKVキャッシュ削除は、長い入力プロンプトをすべて処理した後、生成段階のKVメモリや帯域を減らすことに主眼がある。プリフィルの全KVを一度保持しなければならないため、生成段階では大幅に圧縮していても、最初のプリフィル時のピークメモリがバッチサイズを制限する。

### 3年前（2023-12〜2024-11）

- **2024-06 · [SnapKV: LLM Knows What You are Looking for Before Generation](2024-2404.14469-snapkv.md)**  
  実装：[✓](https://github.com/FasterDecoding/SnapKV) ・ リポジトリ内被引用：620  
  プロンプト末尾の観測窓から各注意ヘッドが将来参照する位置を推定し、重要KVだけをクラスタ単位で残して長文復号を軽量化する手法。

- **2024-02 · [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](2024-2402.02750-kivi.md)**  
  実装：[✓](https://github.com/jy-yuan/KIVI) ・ リポジトリ内被引用：478  
  KIVIは、自己注意の鍵・値キャッシュ（KV キャッシュ）を追加学習なしで2ビットに圧縮する方式である。Llama-2-7Bを用いた単一A100 80GBの実機実験では、ピークメモリ（モデル重みを含む）が最大2.6分の1となり、同程度のメモリ上限で最大4倍のバッチを処理できる。

- **2024-01 · [KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization](2024-2401.18079-kvquant.md)**  
  実装：[✓](https://github.com/SqueezeAILab/KVQuant) ・ リポジトリ内被引用：449  
  Key分布に合わせたチャネル別・RoPE前・非一様・外れ値分離量子化で、3ビットKVを約4.8倍圧縮しつつパープレキシティ悪化0.1未満を実現する。

- **2024-05 · [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](2024-2405.04434-deepseek-v2-mla.md)**  
  実装：✓ ・ リポジトリ内被引用：432  
  通常の多頭注意（Multi-Head 注意機構; MHA）では、系列長が伸びるほどKVキャッシュが線形に増え、GPU高帯域メモリ（High Bandwidth メモリ; HBM）に置ける同時要求数や最大文脈長を圧迫する。

- **2024-06 · [PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling](2024-2406.02069-pyramidkv.md)**  
  実装：[✓](https://github.com/Zefan-Cai/PyramidKV) ・ リポジトリ内被引用：335  
  注意の層間集約パターンに合わせてKV予算を下層から上層へ逓減させ、同じ総メモリで固定予算型より長文脈性能を保つKVキャッシュ圧縮法。

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：202  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2024-07 · [Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference](2024-2407.11550-ada-kv.md)**  
  実装：[✓](https://github.com/FFY0/AdaKV) ・ リポジトリ内被引用：177  
  注意ヘッドごとの集中度に応じて同一層内のKV保持予算を再配分し、既存Top-k圧縮の総容量を変えずに追い出し損失を下げる手法。

- **2024-10 · [DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads](2024-2410.10819-duoattention-efficient-long-context-llm-inference-with-retrieval-and-str.md)**  
  実装：[✓](https://github.com/mit-han-lab/duo-attention) ・ リポジトリ内被引用：172  
  デコード時には過去のKVを読み出すため遅延も長くなり、プリフィルでは注意計算が系列長の二乗に増える。DuoAttentionは、全ての注意ヘッドが遠距離の情報を必要とするわけではないという観測に基づき、ヘッドごとに全履歴を残すか、固定長の履歴だけ残すかを切り替える方式である。

- **2024-03 · [GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM](2024-2403.05527-gear-an-efficient-kv-cache-compression-recipe-for-near-lossless-generati.md)**  
  実装：[✓](https://github.com/HaoKang-Timmy/GEAR) ・ リポジトリ内被引用：119  
  GEARは、自己回帰生成で増え続けるKVキャッシュを高い圧縮率で保持しつつ、単純な低ビット量子化で生じる生成品質の崩壊を抑えるための圧縮法である。

- **2024-05 · [MiniCache: KV Cache Compression in Depth Dimension for Large Language Models](2024-2405.14366-minicache-kv-cache-compression-in-depth-dimension-for-large-language-mod.md)**  
  実装：[✓](https://github.com/AkideLiu/MiniCache) ・ リポジトリ内被引用：112  
  MiniCacheは層内のトークン選別や低ビット化だけでなく、隣り合う層のあいだにも冗長性があると観察し、中層以降で同じ位置のKV状態を共有表現へ統合する。

- **2024-03 · [Jamba: A Hybrid Transformer-Mamba Language Model](2024-2403.19887-jamba-a-hybrid-transformer-mamba-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：105  
  系列が長くなると鍵値キャッシュ（KVキャッシュ）の容量と読出し量が増え、GPUのメモリ容量・帯域を圧迫する。さらに混合専門家モデル（Mixture-of-Experts、MoE）を一部の前向き全結合層へ導入し、総パラメータ容量とトークン当たりの有効計算量を分離する。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：95  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：86  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：83  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。

- **2024-05 · [ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification](2024-2405.14256-zipcache.md)**  
  実装：[✓](https://github.com/ThisisBillhe/ZipCache) ・ リポジトリ内被引用：78  
  ZipCacheは、長文脈推論で肥大化する鍵・値キャッシュ（KV キャッシュ）を、重要トークンの識別と混合精度量子化によって圧縮する手法である。そこでZipCacheは最近5%とランダム5%のプローブトークンの注意スコアだけを求め、残りのトークンは高速注意経路を維持する。

- **2024-07 · [PQCache: Product Quantization-based KVCache for Long Context LLM Inference](2024-2407.12820-pqcache-product-quantization-based-kvcache-for-long-context-llm-inferenc.md)**  
  実装：[✓](https://github.com/HugoZHL/PQCache) ・ リポジトリ内被引用：77  
  文脈が長くなるほどKVキャッシュは大きくなり、GPUメモリへ収まらない場合にはCPUメモリへの退避と転送が必要になる。Llama-3.1-8Bの128K文脈を用いたInfiniteBenchでは、過去トークンの1/10だけを選択する条件で平均スコア46.80を報告し、比較方式に対する改善は+4.60%である。

- **2024-02 · [No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization](2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-.md)**  
  実装：✓ ・ リポジトリ内被引用：76  
  自己回帰推論の鍵・値キャッシュ（KVキャッシュ）は、生成済みの各トークンの中間状態を再利用して再計算を避ける一方、必要容量が同時要求数と文脈長にほぼ比例して増える。提案する混合精度KVキャッシュ（MiKV）は、重要トークンを高精度で保持し、従来なら追い出すトークンも2〜4ビットで保存する。

- **2024-05 · [PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference](2024-2405.12532-pyramidinfer-pyramid-kv-cache-compression-for-high-throughput-llm-infere.md)**  
  実装：[✓](https://github.com/mutonix/pyramidinfer) ・ リポジトリ内被引用：75  
  PyramidInferは、大規模言語モデルの生成時にGPUメモリを占有するKVキャッシュを、層の深さに応じて段階的に減らす方式である。A100 80GBでのLLaMA 2-13B評価では、固定バッチ・固定長条件でKVメモリ24.2GBから11.0GB、スループット621から1389 トークン/sという結果を報告する。

- **2024-03 · [Keyformer: KV Cache reduction through key tokens selection for Efficient Generative Inference](2024-2403.09054-keyformer-kv-cache-reduction-through-key-tokens-selection-for-efficient-.md)**  
  実装：[✓](https://github.com/d-matrix-ai/keyformer-llm) ・ リポジトリ内被引用：74  
  Keyformerは、生成中に増え続ける鍵値キャッシュ（KVキャッシュ）を、重要な過去トークンだけへ圧縮する方式である。著者らは、注意重みの約90%が過去トークンの一部に集中するという観察から、すべての履歴を保持する必要はないと考える。

- **2024-07 · [RazorAttention: Efficient KV Cache Compression Through Retrieval Heads](2024-2407.15891-razorattention-efficient-kv-cache-compression-through-retrieval-heads.md)**  
  実装：✓ ・ リポジトリ内被引用：70  
  RazorAttentionは、長い入力を処理する大規模言語モデルの鍵・値キャッシュ（KV キャッシュ）を、注意頭ごとの機能差に基づいて圧縮する手法である。原著の既定設定では、非検索頭に残す近傍長を max(4000,N/5)、系列先頭の保持数を4とし、誘導頭の上位14%と反復頭の上位1%を検索頭として保護する。

- **2024-03 · [Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference](2024-2403.09636-dynamic-memory-compression-retrofitting-llms-for-accelerated-inference.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM/tree/DMC) ・ リポジトリ内被引用：70  
  動的メモリ圧縮（動的 メモリ Compression; DMC）は、過去トークンを「残す／捨てる」の二択にせず、各注意ヘッドが新しいキー・値（Key-Value; KV）を新規スロットへ追加するか、直前のスロットへ重み付きで結合するかを学習する。これにより、内容・層・ヘッドごとに必要な時間解像度を変えながらKVキャッシュをオンライン圧縮する。

- **2023-12 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-.md)**  
  実装：✓ ・ リポジトリ内被引用：62  
  本論文は、既に学習済みの多頭注意（MHA）モデルを破棄せず、復号時に読み出すKey/Value（KV）ヘッド数を減らすためのチェックポイント変換と追加学習を提案する。著者らはMHAのKV投影重みをグループ内で平均して初期化し、元の事前学習手順の5%相当を追加実行する。

- **2024-10 · [Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning](2024-2410.19258-not-all-heads-matter-a-head-level-kv-cache-compression-method-with-integ.md)**  
  実装：[✓](https://github.com/FYYFU/HeadKV) ・ リポジトリ内被引用：61  
  従来の圧縮方式は、最近の注意得点を利用して残すトークンを選んだり、層ごとに予算を変えたりする。論文は文脈QAの代表条件で元キャッシュの約1.5%を保持しながら完全キャッシュ性能の97%を得たと報告するが、これは全タスク・全モデルで97%という保証ではない。

- **2024-07 · [Keep the Cost Down: A Review on Methods to Optimize LLM's KV Cache Consumption](2024-2407.18003-keep-the-cost-down-a-review-on-methods-to-optimize-llm-s-kv-cache-consum.md)**  
  実装：✓ ・ リポジトリ内被引用：61  
  本稿は、Luohe Shi、Hongyi Zhang、Yao Yao、Zuchao Li、Hai Zhaoによる鍵・値キャッシュ（Key-Value Cache、以下KVキャッシュ）の最適化手法に関する総説を、2024年11月20日の第4版を一次資料として再監査した解説である。

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/jordan-benjamin/hydragen) ・ リポジトリ内被引用：60  
  共通のシステム指示、少数例の例示、同一問題に対する多数の候補生成などでは、異なる要求が接頭辞の鍵・値キャッシュを共有する。原著はCodeLlama-13Bを8枚のA100-40GBで実行し、大きなバッチと長い共有接頭辞でvLLMのページ注意に対して端点処理率最大32倍を報告する。

- **2024-08 · [Eigen Attention: Attention in Low-Rank Space for KV Cache Compression](2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UtkarshSaxena1/EigenAttn) ・ リポジトリ内被引用：58  
  長い文脈を処理する言語モデルでは、生成時に過去のトークンの鍵と値を保存するKVキャッシュが、モデル重みと同程度かそれ以上のメモリを占めることがある。Eigen 注意機構は、保存するトークン数や一要素のビット幅を減らすのではなく、各トークンの鍵・値ベクトルの特徴次元を低ランク空間へ縮める。

- **2024-03 · [QAQ: Quality Adaptive Quantization for LLM KV Cache](2024-2403.04643-qaq-quality-adaptive-quantization-for-llm-kv-cache.md)**  
  実装：[✓](https://github.com/ClubieDong/KVCacheQuantization) ・ リポジトリ内被引用：58  
  QAQは、自己回帰型大規模言語モデルの鍵値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を、すべてのトークンで一律のビット幅にするのではなく、注意出力の誤差許容量に応じてキー（Key; K）と値（Value; V）を別々に量子化する方式である。

- **2024-05 · [KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization](2024-2405.03917-coupled-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：57  
  鍵値活性のチャネル間依存を利用して複数チャネルを共同量子化し、極低ビットでも品質劣化を抑える連結量子化を提案する。

- **2024-07 · [ThinK: Thinner Key Cache by Query-Driven Pruning](2024-2407.21018-think-thinner-key-cache-by-query-driven-pruning.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/ThinK) ・ リポジトリ内被引用：56  
  ThinKは、長文脈生成に必要な鍵・値キャッシュ（KVキャッシュ）のうち、鍵（Key）ベクトル内部のチャネルを選択的に削除する圧縮手法である。ICLR 2025の著者論文では、H2OやSnapKVへ40%のKeyチャネル削減を追加してもLongBenchの平均スコアがほぼ維持される例を示す。

- **2024-02 · [Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference](2024-2402.09398-get-more-with-less-synthesizing-recurrence-with-kv-cache-compression-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/hdong920/LESS) ・ リポジトリ内被引用：54  
  LESSは、キー・値キャッシュ（Key-Value Cache; KVキャッシュ）の追い出しを「残すか捨てるか」の二択にしない。重要なトークンは従来どおり疎KVキャッシュへ明示的に残し、追い出すトークンは固定サイズの低ランク状態へ順次圧縮する。次の注意計算では両方を合成するため、疎キャッシュから消えたトークンにも低解像度ながら参照経路が残る。

- **2024-02 · [GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding](2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：53  
  本論文は、大規模言語モデルの生成時に生じる逐次計算の待ち時間を、投機的復号（投機的復号）の二つの構成要素から短縮する研究である。投機的復号では軽量な下書きモデルが数トークンを先に提案し、大型の対象モデルが一度の前向き計算で提案を検証する。

- **2024-07 · [Model Tells You Where to Merge: Adaptive KV Cache Merging for LLMs on Long-Context Tasks](2024-2407.08454-model-tells-you-where-to-merge-adaptive-kv-cache-merging-for-llms-on-lon.md)**  
  実装：✓ ・ リポジトリ内被引用：51  
  既存のKV圧縮は、量子化で各要素のビット数を減らす、注意重要度の低いトークンを削除する、複数トークンを一つへ統合する、という三系統に分けられる。

- **2024-02 · [ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition](2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-t.md)**  
  実装：[✓](https://github.com/microsoft/chunk-attention) ・ リポジトリ内被引用：51  
  ChunkAttentionは、同じ言語モデルを複数の利用者・アプリケーションへ提供する際に、要求の先頭で共有されるシステム指示や少数例を計算と記憶の両面で再利用する推論用注意機構である。

- **2024-05 · [SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models](2024-2405.06219-skvq-sliding-window-key-and-value-cache-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/cat538/SKVQ) ・ リポジトリ内被引用：50  
  KVチャネルを量子化しやすい順へ並べ替え、外れ値をクリップし、直近KVだけ高精度で残すことで鍵2ビット・値1.5ビット級まで圧縮し、長文脈の容量・帯域律速を緩和する。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：47  
  ALISAは、生成が進むほど増加する鍵・値キャッシュ（KVキャッシュ）の容量とCPU・GPU間転送が、単一GPUでの大規模言語モデル推論を妨げる問題を扱う。提案方式は三つの操作を組み合わせる。原著はOPT、LLaMA、Pythiaの6.7B～33B級を評価し、入力128・出力512トークンのAlpaca負荷で、80%のKV疎化を採用した際の処理量を比較する。

- **2024-06 · [A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression](2024-2406.11430-l2-kv-compression.md)**  
  実装：[✓](https://github.com/alessiodevoto/l2compress) ・ リポジトリ内被引用：45  
  キーのL2ノルムと注意重みの逆相関を利用し、注意重みを計算せず重要KVを残す学習不要の圧縮法。FlashAttention互換のまま、長文検索では50〜90%のKV削減でも高精度を維持する。

- **2024-02 · [WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More](2024-2402.12065-wkvquant-quantizing-weight-and-key-value-cache-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：45  
  WKVQuantは、大規模言語モデルの推論時に使うメモリを、モデル重み、鍵・値キャッシュ、一時活性化の三種類に分け、容量を長く占有する重みと鍵・値キャッシュだけを低ビット化する事後量子化（post-学習 量子化; PTQ）方式である。重みのみの量子化は比較的精度を維持しやすいが、長文脈・大バッチで増える鍵・値キャッシュを圧縮しない。

- **2024-01 · [Long Context Compression with Activation Beacon](2024-2401.03462-long-context-compression-with-activation-beacon.md)**  
  実装：[✓](https://github.com/FlagOpen/FlagEmbedding) ・ リポジトリ内被引用：43  
  活性値 Beaconは、文章そのものを短く書き換えるのではなく、Transformerの各層に生じる鍵・値活性を、追加したビーコントークンの活性へ直接圧縮する。圧縮率を8倍にした128K文脈の実験では、非圧縮で同じデータにより微調整した比較モデルに対し、推論時間を約半分、KVキャッシュを約8分の1にした。

- **2024-10 · [LoRC: Low-Rank Compression for LLMs KV Cache with a Progressive Compression Strategy](2024-2410.03111-lorc-low-rank-compression-for-llms-kv-cache-with-a-progressive-compression-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  自己回帰型の大規模言語モデル（LLM）は、過去トークンの鍵（K）と値（V）をKVキャッシュへ保存することで、次のトークン生成時に過去の注意計算をやり直さない。原著のメモリ表では、バッチ64、文脈長2048でLLaMA-2 13BのKVキャッシュが50GBから27.5GB、LLaMA-3 8Bが8GBから4.8GB、70Bが20GBから11GBになる。

- **2024-06 · [Attention Score is not All You Need for Token Importance Indicator in KV Cache Reduction: Value Also Matters](2024-2406.12335-attention-score-is-not-all-you-need-for-token-importance-indicator-in-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  注意スコアに値ベクトルのL1ノルムを組み込み、実際の注意出力寄与に近い重要度でKVトークンを削減する後付け型キャッシュ枝刈り。

- **2024-11 · [DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving](2024-2411.02820-droidspeak-kv-cache-sharing-for-cross-llm-communication-and-multi-llm-se.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  DroidSpeakは、同じ基盤モデルを微調整して得た異なるLLMが、同じ会話履歴や文書を別々に処理する際の重複プリフィルを減らす分散推論システムである。著者らは8種類のモデル対で層別の感度を測定し、KV差異に敏感な層は平均約11%と報告した。

- **2024-08 · [NACL: A General and Effective KV Cache Eviction Framework for LLM at Inference Time](2024-2408.03675-nacl-a-general-and-effective-kv-cache-eviction-framework-for-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/Research/tree/master/NLP/ACL2024-NACL) ・ リポジトリ内被引用：32  
  KV追い出しで「これまで注意スコアが大きかったトークンを残す」だけでは、注意が先頭・直近位置へ偏るため、長文中央の重要情報を捨てやすい。NACLは、質問などタスク固有の代理トークン（proxy トークン）が入力全体へ向けた注意から重要度を作る決定論的な保持と、その重要度分布からヘッド・層ごとに異なるトークンを確率的に残す保持を混ぜる。

- **2024-10 · [KVSharer: Efficient Inference via Layer-Wise Dissimilar KV Cache Sharing](2024-2410.18517-kvsharer-efficient-inference-via-layer-wise-dissimilar-kv-cache-sharing.md)**  
  実装：[✓](https://github.com/yangyifei729/KVSharer) ・ リポジトリ内被引用：29  
  層ごとの鍵・値キャッシュを独立に保存する代わりに、一部の後段層で前段層のキャッシュを再利用する。直感に反して「KV表現が大きく異なる層対」から共有を試し、元モデルの最終隠れ状態を保てる組だけを採用する。

- **2024-10 · [MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection](2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md)**  
  実装：[✓](https://github.com/The-kamisato/MatryoshkaKV-cache) ・ リポジトリ内被引用：27  
  MatryoshkaKVは、事前学習済み大規模言語モデル（LLM）の鍵値キャッシュ（KVキャッシュ）について、トークン数や注意ヘッド数を減らす代わりに各ヘッドが保存する特徴次元を縮小する方式である。単純な主成分分析（PCA）による次元削減は中程度の圧縮では有効だが、元のキャッシュ容量の半分以下にすると生成品質が急落する。

- **2024-06 · [QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead](2024-2406.03482-qjl-1-bit-quantized-jl-transform-for-kv-cache-quantization-with-zero-ove.md)**  
  実装：[✓](https://github.com/amirzandieh/QJL) ・ リポジトリ内被引用：23  
  従来の低ビット量子化は、量子化された整数だけでなく、元の実数値へ戻すための尺度（scale）とゼロ点（zero point）をブロック単位で保持する。

- **2024-10 · [LayerKV: Optimizing Large Language Model Serving with Layer-wise KV Cache Management](2024-2410.00428-layerkv-optimizing-large-language-model-serving-with-layer-wise-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  LayerKVは、長い入力を受ける言語モデルのサービングで、初回トークンまでの時間（Time to First Token、TTFT）が急増する原因を新規要求がGPU上の鍵・値（KV）キャッシュ領域を確保できず待たされることに求めたシステムである。

- **2024-06 · [Effectively Compress KV Heads for LLM](2024-2406.07056-effectively-compress-kv-heads-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  本論文は、既に多頭注意（Multi-Head 注意機構; MHA）として学習済みの大規模言語モデルを、鍵・値（Key/Value; KV）のヘッド数が少ない構成へ後変換する研究である。LLaMA2-7BのKVヘッドを32から16へ半減すると、単一A100 80GBで復号速度が8.05から13.41トークン/秒へ増えた。

- **2024-02 · [On the Efficacy of Eviction Policy for Key-Value Constrained Generative Language Model Inference](2024-2402.06262-on-the-efficacy-of-eviction-policy-for-key-value-constrained-generative-language-model-inference.md)**  
  実装：[✓](https://github.com/DRSY/EasyKV) ・ リポジトリ内被引用：20  
  RoCoはKV トークンの重要度を累積注意機構ではなく平均注意機構で測り、注意機構標準偏差で追い出し候補を動的に選び、固定window依存を減らしながらfull-キャッシュに近い生成品質を保つ。

- **2024-10 · [InfiniPot: Infinite Context Processing on Memory-Constrained LLMs](2024-2410.01518-infinipot-infinite-context-processing-on-memory-constrained-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  InfiniPotは、長い入力をすべて読み終わってから鍵・値キャッシュ（KVキャッシュ）を削減する方式ではなく、入力を読んでいる途中から固定容量内で何度も圧縮する長文脈処理の仕組みである。Mistral系の4K固定KV予算で最大100万トークンの検索実験も行ったが、「無限長でも全情報を損失なく保持する」ことを示したわけではない。

- **2023-12 · [Compressed Context Memory For Online Language Model Interaction](2023-2312.03414-compressed-context-memory-for-online-language-model-interaction.md)**  
  実装：[✓](https://github.com/snu-mllab/context-memory) ・ リポジトリ内被引用：19  
  オンライン対話、個人化推薦、複数課題の逐次学習では、要求を受けるたびに新しい文脈が追加される。Compressed Context メモリ（CCM）は、過去の鍵値キャッシュを、専用の圧縮トークンが生成する少数の鍵値へ繰り返し統合する。

- **2024-09 · [Small Language Models: Survey, Measurements, and Insights](2024-2409.15790-small-language-models-survey-measurements-and-insights.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/SLM_Survey) ・ リポジトリ内被引用：18  
  推論を高速化する新しいアルゴリズムを提案する論文ではない。同程度のパラメータ数でもQwen2-0.5Bの初回トークン時間はQwen1.5-0.5Bの1.46倍であり、Qwen1.5-0.5Bはパラメータが25.4%多いにもかかわらずJetson上では31.9%速い。

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

- **2024-04 · [SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget](2024-2404.04793-squeezeattention-2d-management-of-kv-cache-in-llm-inference-via-layer-wi.md)**  
  実装：[✓](https://github.com/hetailang/SqueezeAttention) ・ リポジトリ内被引用：17  
  SqueezeAttentionは、大規模言語モデルの推論で必要になる鍵・値キャッシュ（KVキャッシュ）を、系列中のトークン方向だけでなく、注意機構を構成する層の方向からも最適化する方式である。

- **2024-10 · [LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation](2024-2410.13846-lighttransfer-your-long-context-llm-is-secretly-a-hybrid-model-with-effo.md)**  
  実装：[✓](https://github.com/sail-sg/LightTrans) ・ リポジトリ内被引用：14  
  キャッシュがGPUメモリを圧迫すると、同時に処理できる要求数が減り、長文脈の生成処理量も低下する。ある層では先頭の少数トークン（注意機構 sink）と直近の窓だけに注意が集中する。

- **2024-10 · [Locret: Enhancing Eviction in Long-Context LLM Inference with Trained Retaining Heads on Consumer-Grade Devices](2024-2410.01805-locret-enhancing-eviction-in-long-context-llm-inference-with-trained-ret.md)**  
  実装：[✓](https://github.com/huangyuxiang03/Locret) ・ リポジトリ内被引用：13  
  Locretは、長文脈LLMの推論で大きくなるキー・バリューキャッシュ（KVキャッシュ）を、必要な情報だけ残して逐次削除する方式である。原著は、Phi-3-mini-128Kで最大20倍超、Llama-3.1-8B-instructで8倍超のKV圧縮を報告する。

- **2024-09 · [Inf-MLLM: Efficient Streaming Inference of Multimodal Large Language Models on a Single GPU](2024-2409.09086-inf-mllm-efficient-streaming-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  著者らは注意得点の時間的な構造を観察し、直近トークンだけでなく、離れた過去にある重要トークンを固定容量キャッシュへ残す方法を提案する。

- **2024-06 · [Optimised Grouped-Query Attention Mechanism for Transformers](2024-2406.14963-optimised-grouped-query-attention-mechanism-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  既存の多頭注意（Multi-Head 注意機構、MHA）を、複数の質問ヘッドで鍵・値ヘッドを共有するグループ化質問注意（Grouped-Query 注意機構、GQA）へ変換すると、復号時に保存する鍵値キャッシュと鍵値投影のパラメータを減らせる。

- **2024-10 · [Exploring CXL-based KV Cache Storage for LLM Serving](2024-fcda582bb2a7-exploring-cxl-based-kv-cache-storage-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CPUの主記憶へ退避しても、複数の長文脈要求を保持するには容量が足りなくなる可能性がある。

- **2024-09 · [KVPruner: Structural Pruning for Faster and Memory-Efficient Large Language Models](2024-2409.11057-kvpruner-structural-pruning-for-faster-and-memory-efficient-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KVPrunerは、長い入力や複数の同時要求で増大する鍵・値キャッシュを、事前にモデルの注意チャネルを削除することで小さくする手法である。原著のLLaMA-7B実験では、鍵・値チャネルを50%削減した構成で鍵・値保存量が8GBから4GB、モデルパラメータ数が7Bから5.5Bになる。

- **2024-09 · [CSKV: Training-Efficient Channel Shrinking for KV Cache in Long-Context Scenarios](2024-2409.10593-cskv-training-efficient-channel-shrinking-for-kv-cache-in-long-context-s.md)**  
  実装：[✓](https://github.com/wln20/CSKV) ・ リポジトリ内被引用：2  
  過去トークンの表現を毎回計算し直さずに済む一方、保存容量は文脈長にほぼ比例して増え、長い文書の読解や検索でGPUメモリを圧迫する。量子化は保存ビット数を減らすが、高圧縮では誤差が増える。LongChat-7B-v1.5-32kでは80%のKV容量圧縮時、LongEvalの10K検索正答率が無圧縮0.98に対してCSKV0.90となる。

- **2024-06 · [Training-Free Exponential Context Extension via Cascading KV Cache](2024-2406.17808-training-free-exponential-context-extension-via-cascading-kv-cache.md)**  
  実装：[✓](https://github.com/jeffwillette/cascading_kv_cache) ・ リポジトリ内被引用：2  
  固定長の滑動窓（sliding window）を使えばメモリを抑えられるが、窓から出た過去のトークンは消え、長距離の依存関係を復元できない。StreamingLLMは冒頭の注意シンク（注意機構 sinks）を残して安定性を高めるものの、冒頭以外の過去トークンは一定の年齢になると削除する。

- **2024-04 · [XC-Cache: Cross-Attending to Cached Context for Efficient LLM Inference](2024-2404.15420-xc-cache-cross-attending-to-cached-context-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  文脈を符号器の最終表現だけでキャッシュし交差注意で読む形へ復号器を作り替え、KVキャッシュを約30分の1にしながらプロンプト方式より高い質問応答精度を出した方式。

- **2024-03 · [Accurate Block Quantization in LLMs with Outliers](2024-2403.20137-accurate-block-quantization-in-llms-with-outliers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈LLMのKVキャッシュは系列長に比例して大きくなるため、重み量子化とは別にKVの保存精度を下げる必要がある。

- **2024-10 · [BATON: Enhancing Batch-wise Inference Efficiency for Large Language Models via Dynamic Re-Batching](2024-2410.18701-baton-enhancing-batch-wise-inference-efficiency-for-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  完了したクエリの枠へ新規クエリを差し込む動的リバッチを、ベクトル整形とプリフィル済みKVの埋め込みで実現し、追加パラメータなしにアイドル計算をほぼゼロにした研究。

- **2024-10 · [ALISE: Accelerating Large Language Model Serving with Speculative Scheduling](2024-2410.23537-alise-accelerating-large-language-model-serving-with-speculative-schedul.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  出力長を検索型予測器で推定し、残り時間の短いジョブを優先するプリエンプティブなスケジューリングと、待ち時間に応じたKVキャッシュのスワップで、ヘッドオブライン・ブロッキングを解くサービング方式。vLLM比で最大2.1倍のスループット。

- **2024-07 · [Let the Code LLM Edit Itself When You Edit the Code](2024-2407.03157-let-the-code-llm-edit-itself-when-you-edit-the-code.md)**  
  実装：[✓](https://github.com/zhenyuhe00/PIE) ・ リポジトリ内被引用：1  
  本研究は、開発者が既存コードの途中に行を挿入・削除した直後に、コード補完用の大規模言語モデル（LLM）が次の行を予測し直す場面を対象とする。

- **2024-06 · [CaR: An Efficient KV Cache Reuse System for Large Language Model Inference](2024-e4d953294da1-car-an-efficient-kv-cache-reuse-system-for-large-language-model-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  破棄されていた履歴の鍵値キャッシュをHBMとCXLメモリの二層に残し、スケジューラと協調した先読み・退避・層別疎化で要求をまたいで再利用し、最初のトークンまでの時間を約30パーセント、長い文脈では60パーセント超短くした多層キャッシュ基盤。

- **2024-05 · [BiSup: Bidirectional Quantization Error Suppression for Large Language Models](2024-2405.15346-bisup-bidirectional-quantization-error-suppression-for-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  量子化誤差の縦の蓄積と横の拡散を分けて抑える誤差抑制手法。学習可能な量子化パラメータの層別微調整と、システムプロンプトの高精度キャッシュ保持で、3ビット量子化のパープレキシティを大きく改善する。

- **2024-11 · [StreamAdapter: Efficient Test Time Adaptation from Contextual Streams](2024-2411.09289-streamadapter-efficient-test-time-adaptation-from-contextual-streams.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  デモンストレーションのKVキャッシュを一定サイズの文脈状態へ圧縮し、低ランク更新として重みへ吸収させるテスト時適応StreamAdapter。文脈を残さないため生成遅延が文脈長に依存せず、LLaMA-3-8Bの学習済みタスク平均92.75で10ショットICLの86.11を上回った。

- **2024-11 · [SCA: Selective Compression Attention for Efficiently Extending the Context Window of Large Language Models](2024-b9a679571edc-sca-selective-compression-attention-for-efficiently-extending-the-contex.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュの冗長度が最も増えないベクトルを貪欲に選んで代表だけを残す学習不要の圧縮で、文脈窓を3倍へ広げてもパスキー検索100パーセントを保ち、微調整済み長文脈モデルを実課題で上回る。

- **2024-11 · [A Method for Building Large Language Models with Predefined KV Cache Capacity](2024-2411.15785-a-method-for-building-large-language-models-with-predefined-kv-cache-cap.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意層のKVキャッシュを固定長Mの列へ置き換え、新しい入力を書き込み重み付きの加算で既存の列へ畳み込むことで、文脈が伸びてもメモリが増えないモデル構築法。容量2048の実験ではメモリと速度が一定に保たれ、BLEUの差は従来方式比3%以内とされる。

- **2024-07 · [Token-Picker: Accelerating Attention in Text Generation with Minimized Memory Transfer via Probability Estimation](2024-2407.15131-token-picker-accelerating-attention-in-text-generation-with-minimized-me.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キーの部分ビットから注意確率の上限を保守的に見積もり、確率が無視できるトークンの転送を省くToken-Pickerと専用ハードウェアToPickを提案し、メモリアクセス2.57倍削減、生成で2.28倍の高速化と2.41倍のエネルギー効率を達成した。

- **2024-07 · [QET: Enhancing Quantized LLM Parameters and KV Cache Compression through Element Substitution and Residual Clustering](2024-2407.03637-qet-enhancing-quantized-llm-parameters-and-kv-cache-compression-through-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Quantum Entanglement Trees（QET）は、量子コンピュータを用いる方式ではない。主要実験では圧縮比4のLLaMA2重み行列のMSEをPQの5.05%、KキャッシュのMSEを13.33%、VキャッシュのMSEを11.89%に減らしたと報告する。

- **2024-06 · [SUBLLM: A Novel Efficient Architecture with Token Sequence Subsampling for LLM](2024-2406.06571-subllm-a-novel-efficient-architecture-with-token-sequence-subsampling-fo.md)**  
  実装：[✓](https://github.com/XiaoMi/subllm) ・ リポジトリ内被引用：0  
  重要度の低いトークンを中間層で間引いて系列を40パーセントまで短縮し、スコア重み付き補間で復元するデコーダ型アーキテクチャ。LLaMA同規模で学習26パーセント、推論最大37パーセントの高速化とメモリ削減を、検証損失を保ったまま達成する。

- **2024-06 · [CItruS: Chunked Instruction-aware State Eviction for Long Sequence Modeling](2024-2406.12018-citrus-chunked-instruction-aware-state-eviction-for-long-sequence-modeli.md)**  
  実装：[✓](https://github.com/ybai-nlp/CItruS) ・ リポジトリ内被引用：0  
  文書文脈の注意だけで状態を追い出すと課題に要る情報が落ちる問題を示し、最終の指示文の注意で選ぶ専用または共有のキャッシュを併設することで、百万トークン文書の合言葉検索を全件成功させ、針探し課題のルージ一を標準方式の十五・二から六十三・五へ改善したと報告した。

- **2024-03 · [Hierarchical and Dynamic Prompt Compression for Efficient Zero-shot API Usage](2024-60b566817f9b-hierarchical-and-dynamic-prompt-compression-for-efficient-zero-shot-api-.md)**  
  実装：[✓](https://github.com/jiangycTarheel/HD-Gist) ・ リポジトリ内被引用：0  
  従来のgist トークン方式は文書を固定個数の特殊トークンの隠れ状態へ圧縮できるが、API呼出しのように細かい引数名・値の正確さが必要なタスクでは情報が失われ、圧縮前より大きく精度が低下する。

### 4年前（2022-12〜2023-11）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：908  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。

- **2023-06 · [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](2023-2306.14048-h2o.md)**  
  実装：[✓](https://github.com/FMInference/H2O) ・ リポジトリ内被引用：833  
  累積注意のヘビーヒッターと最新トークンを動的保持し、20%程度のKV予算で品質を維持しながらメモリ・スループットを改善する。

- **2023-05 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-2305.13245-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：437  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各クエリ頭に独立した鍵頭と値頭を持つため、復号時には全KV頭のキャッシュを読み出す必要がある。

- **2023-10 · [Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs](2023-2310.01801-fastgen.md)**  
  実装：[✓](https://github.com/machilusZ/FastGen) ・ リポジトリ内被引用：295  
  FastGenは注意ヘッドごとの構造を一度だけ診断してKVキャッシュ保持方針を変え、追加学習なしでメモリ削減と長系列生成の高速化を両立する。

- **2023-05 · [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](2023-2305.17118-scissorhands.md)**  
  実装：✓ ・ リポジトリ内被引用：281  
  Scissorhandsは、過去の注意重みが大きかったトークンは将来の生成でも高い注意を受けやすいという「重要性の持続性仮説（Persistence of Importance Hypothesis）」を提案する。

- **2023-06 · [Augmenting Language Models with Long-Term Memory](2023-2306.07174-augmenting-language-models-with-long-term-memory.md)**  
  実装：[✓](https://github.com/Victorwz/LongMem) ・ リポジトリ内被引用：15  
  過去のキー・値（KV）を外部バンクへ保持して必要な箇所だけ取り出す方式は有望だが、モデルを学習しながら記憶を書き込むと、古いモデルが生成した記憶表現と現在のモデルの表現が食い違う問題が生じる。

### 8年前（2018-12〜2019-11）

- **2019-11 · [Fast Transformer Decoding: One Write-Head is All You Need](2019-1911.02150-multi-query-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：319  
  複数問い合わせ注意（Multi-Query 注意機構; MQA）は、問い合わせ側の8ヘッドを維持したまま、鍵と値だけを全ヘッドで1組へ共有する。長い履歴を毎生成ステップで読む増分復号のメモリ転送を減らし、TPUv2でのWMT英独翻訳のデコーダ測定を46から3.8マイクロ秒／出力トークンへ短縮した。
<!-- survey:auto:end -->
