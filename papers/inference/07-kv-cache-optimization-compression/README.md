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
## 自動生成の論文一覧（427本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/07-kv-cache-optimization-compression/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：23  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2026-07 · [Gemma 4 Technical Report](2026-2607.02770-gemma-4-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  密モデルと混合専門家モデルを含むGemma 4の技術報告。局所・大域注意の配置、キー・値キャッシュ共有、キーの値への再利用、部分回転位置符号化、量子化対応学習、複数トークン予測ドラフタ、12Bの符号化器不要構成を組み合わせ、推論時の重み容量・KV容量・復号費用をそれぞれ減らす。数値はモデル系列・量子化形式・文脈長ごとに区別して読む必要がある。

- **2025-11 · [TiDAR: Think in Diffusion, Talk in Autoregression](2025-2511.08923-tidar-think-in-diffusion-talk-in-autoregression.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  論文が対象にするのは、単に「拡散型言語モデルを速くする」ことではない。確定した接頭辞の鍵・値（KV）キャッシュは再利用でき、拡散型で問題になりやすい過去全体の再計算も避けられる。8B版の生成六課題平均正答率65.31%はQwen3-8Bの68.09%を下回り、元モデルと同じ出力分布を厳密に保存する手法ではない。

- **2025-11 · [TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection](2025-token-select.md)**  
  実装：[✓](https://github.com/pzs19/TokenSelect) ・ リポジトリ内被引用：17  
  各問い合わせで重要な鍵値をトークン単位に選び、ヘッド軟投票・選択キャッシュ・ページ化内積カーネルで長文脈注意を高精度かつ高速化する。

- **2026-01 · [Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction](2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md)**  
  実装：[✓](https://github.com/Janghyun1230/FastKVzip) ・ リポジトリ内被引用：14  
  長文脈の言語モデルは、生成のたびに過去の鍵・値（KV）を参照するため、文脈が長くなるとキャッシュがGPUメモリを圧迫する。重要でないKVを削除する方法は容量を減らせるが、何を消すかを決めるために過去の注意を再計算すると、圧縮器自体の費用が大きくなる。

- **2026-01 · [KVzap: Fast, Adaptive, and Faithful KV Cache Pruning](2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：13  
  KVzapは、大規模言語モデルの鍵・値キャッシュ（KVキャッシュ）をトークン位置方向に間引く際、重要度の計算そのものが推論を遅くしてしまう問題を解く方式である。Qwen3-8B、Llama-3.1-8B-Instruct、Qwen3-32Bにおける長文脈検索・理解・推論課題で、著者らはおおむね2〜4倍のKV圧縮と小さな精度低下を報告する。

- **2026-07 · [The Pitfalls of KV Cache Compression](2026-2510.00231-the-pitfalls-of-kv-cache-compression.md)**  
  実装：[✓](https://github.com/alexluchen/pitfalls-of-kv-cache-compression) ・ リポジトリ内被引用：12  
  KVキャッシュ圧縮の典型的な評価は、単一質問への回答、長文からの検索、コード生成といったタスクで「キャッシュを減らしても品質はほとんど落ちない」と結論しがちである。

- **2026-07 · [LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning](2026-lazyeviction.md)**  
  実装：[✓](https://github.com/Halo-949/LazyEviction) ・ リポジトリ内被引用：11  
  一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。

- **2026-06 · [STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control](2026-2606.08382-star-kv-adaptive-low-rank-cache-compression.md)**  
  実装：[✓](https://github.com/PriyanshBhatnagar/STAR-KV) ・ リポジトリ内被引用：9  
  特異値の学習可能なしきい値で層・ヘッドごとのKV低ランク次元を自動配分し、鍵/値で異なる分解と低ランク対応混合精度量子化を組み合わせ、強い圧縮を実GPU高速化へつなげる。

- **2026-04 · [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](2026-2604.04921-triattention-efficient-long-reasoning-with-trigonometric-kv-compression.md)**  
  実装：[✓](https://github.com/WeianMao/triattention) ・ リポジトリ内被引用：9  
  長い推論列で「今のクエリに強く注意されるKV」だけを残すのではなく、回転位置埋め込み（Rotary Position Embedding; RoPE）前のクエリ・キーが固定中心の周囲へ集中する性質から、将来の距離ごとの注意傾向を三角関数として予測する。

- **2025-11 · [KV Cache Transform Coding for Compact Storage in LLM Inference](2025-2511.01815-kv-cache-transform-coding-for-compact-storage-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  KVTCは共通の主成分分析基底でKVキャッシュの相関を減らし、重要度別の量子化と無損失符号化で保存量を縮める。16倍目標で多くの課題品質を概ね保ち、H100の8K文脈では復号再利用がKV再計算よりTTFTを約8倍短縮したが、処理時間と強圧縮時の品質低下も示す。

- **2026-05 · [LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents](2026-2602.01053-lragent-multilora-agent-kv-sharing.md)**  
  実装：[✓](https://github.com/jeonhye/lragent) ・ リポジトリ内被引用：8  
  multi-LoRAエージェントのKVを共有基盤成分と低ランク役割成分へ分解し、後者を全次元化せず注意計算することで、長い共有履歴のKVメモリと再プリフィルを削減する。

- **2026-05 · [KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving](2026-2605.13734-kvserve-service-aware-kv-cache-compression.md)**  
  実装：[✓](https://github.com/hpdps-group/KVServe) ・ リポジトリ内被引用：7  
  KVServeは、実効帯域・負荷・品質制約からKV圧縮プロファイルか無圧縮を選び、分離型LLMの通信待ちと圧縮処理費を同時に抑える。

- **2026-02 · [SideQuest: Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning](2026-2602.22603-sidequest-model-driven-kv-cache-management-for-long-horizon-agentic-reas.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  調査エージェントが過去に開いた文書のうち不要になったものを、別の補助推論が意味的に判定し、主推論を止めずにKVキャッシュから削除する。

- **2026-01 · [ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation](2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cac.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  従来の部分再計算法は、文書中の一部トークンだけを再計算して欠けた注意関係を補う。第二段階では層を横断して統合した重要度の上位トークンを選び、その位置のKVを全層で再計算する。原著はLlama-3.1-8B、Qwen2.5-14B、Qwen3-14Bを用い、文書トークンの20%だけを再計算する条件で、全再計算に近い平均精度を報告する。

- **2026-09 · [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](2026-2609.19969-deepseek-v4.1-flash-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  CED・CSA2の層間KV再利用・FP4 KV・SWA限定再実行を統合し、100万トークン対応552B MoEのグローバルKVを890 bytes/トークン、永続KVを前世代比約1/8へ圧縮する。

- **2026-07 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2026-ojakv.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：6  
  重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。

- **2026-06 · [Value-Aware Stochastic KV Cache Eviction for Reasoning Models](2026-2606.03928-value-aware-stochastic-kv-cache-eviction-for-reasoning-models.md)**  
  実装：[✓](https://github.com/terarachang/VaSE) ・ リポジトリ内被引用：6  
  疎注意（Sparse 注意機構）には、キャッシュ全体を保持して計算対象だけを選ぶ方式と、重要度が低い過去トークンの鍵・値を実際に破棄する方式がある。Qwen3-4BとQwen3-14Bの数学・科学課題では約4倍のKV容量圧縮でも、既存の削除方式より高い平均正答率を得た。

- **2026-05 · [Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management](2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  PBKVは、複数の言語モデルエージェントが同じ処理を分担する動的ワークフローで、次に使われる可能性が高いキー・値キャッシュ（KVキャッシュ）をGPUに残し、必要に応じてホストメモリから先読みする仕組みである。

- **2026-04 · [Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs](2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-devic.md)**  
  実装：[✓](https://github.com/SayedPedramHaeri/Dont-Waste-Bits) ・ リポジトリ内被引用：6  
  本研究は、端末上で動かす小型言語モデルのキー・値キャッシュ（KVキャッシュ）を、トークンごとの重要度に応じて異なるビット幅で保存する適応量子化方式を提案する。SmolLM-360MとHellaSwagの実機評価では、固定4ビットの正答率33.6%、遅延2.93に対して、提案方式は41.2%、2.41だった。

- **2025-12 · [MEPIC: Memory Efficient Position Independent Caching for LLM Serving](2025-2512.16822-mepic-position-independent-chunk-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  位置非依存KVをページ境界へ正規配置し、最初の1ブロックだけ再計算、RoPEを注意時に融合することで、同一チャンクのHBMページを要求間共有し、既存PICよりHBM重複と再計算を大幅に減らす。

- **2025-11 · [PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel](2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md)**  
  実装：[✓](https://github.com/flashserve/PAT) ・ リポジトリ内被引用：6  
  共有接頭辞を要求間で一度だけ読む詰込みと動的タイル選択により、復号注意の大域メモリ読出しと実行空洞を同時に削減する。

- **2026-07 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2026-2607.17715-c2kv-compressed-composable-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/s7a9/C2KV) ・ リポジトリ内被引用：5  
  文書ごとに位置非依存で直接連結できる圧縮KVを学習抽出し、非prefix再利用のプリフィル削減とKV保存・転送・デコード帯域削減を同時に狙う。

- **2026-05 · [RateQuant: Optimal Mixed-Precision KV Cache Quantization via Rate-Distortion Theory](2026-2605.06675-ratequant-optimal-mixed-precision-kv-cache-quantization-via-rate-distort.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  各ヘッドの損失勾配に基づく重要度と、量子化器固有の指数型ビット数・歪み関係を校正し、逆水充填法と整数ビットの限界利得選択で配分を決める。Qwen3/Llama3の5モデルと3種類の量子化器で評価し、平均4ビット時のTurboQuantにおける量子化劣化回復率は5モデル平均75.7%。

- **2026-05 · [OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization](2026-2605.17757-oscar-offline-spectral-covariance-aware-rotation-for-2-bit-kv-cache-quan.md)**  
  実装：[✓](https://github.com/FutureMLS-Lab/OSCAR) ・ リポジトリ内被引用：5  
  しかし2ビットには4段階の値しかなく、KV活性値の少数の大きな外れ値が量子化範囲を支配すると、通常値の区別が失われ、注意分布が崩れる。システム評価はNVIDIA H100上の著者実装であり、12GB級の民生GPUや標準配布版llama.cppで同じ結果が出ると示したものではない。

- **2025-11 · [$A^3$: Attention-Aware Accurate KV Cache Fusion for Fast Large Language Model Serving](2025-2511.17560-a-3-attention-aware-accurate-kv-cache-fusion-for-fast-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  $A^3$（注意機構-Aware Accurate KV Cache Fusion）は、複数の質問で再利用される文書断片のKVキャッシュを事前に作り、質問に関係する部分だけを再計算して、長文入力の事前充填を高速化する手法である。Mistral-7B-Instruct-v0.2では全文計算38.27、A3が36.98で、再利用系の比較手法を上回った。

- **2026-08 · [Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding](2026-2609.00097-faster-than-flash-attention-sparsity-long-context-decoding.md)**  
  実装：[✓](https://github.com/qluoluo/faster-flash-decoding) ・ リポジトリ内被引用：4  
  2ビット鍵でKV全体を低帯域走査し、局所・シンク由来の近似最大値からtop-δで必要ブロックだけを選ぶ選別・計算融合カーネルにより、長文デコードを最大11.63倍のカーネル高速化、最大2.37倍の生成スループットへ高める。

- **2026-06 · [RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention](2026-2606.06256-redknot-efficient-long-context-llm-serving-with-head-aware-kv-reuse-and-segpagedattention.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  従来のKV管理は全ヘッドを同じトークンブロックとして扱うが、RedKnotの測定では局所ヘッドが83.4〜96.8%、接頭辞変化に敏感な大域ヘッドは3.2〜16.6%に留まる。そこで大域ヘッドだけを広範囲に再計算し、局所ヘッドを再利用するElastic Sparsityと、ヘッド別のKVページを扱うSegPagedAttentionを組み合わせる。

- **2026-05 · [Dynamic-dLLM: Dynamic Cache-Budget and Adaptive Parallel Decoding for Training-Free Acceleration of Diffusion LLM](2026-2606.26120-dynamic-dllm-cache-budget-parallel-decoding.md)**  
  実装：[✓](https://github.com/TianyiWu233/DYNAMIC-DLLM) ・ リポジトリ内被引用：4  
  層別キャッシュ更新量とトークン別確定基準を動的化し、追加学習なしで最大4.48倍の拡散型LLM推論高速化を実現する。

- **2026-04 · [When Hidden States Drift: Can KV Caches Rescue Long-Range Speculative Decoding?](2026-2604.26412-when-hidden-states-drift-can-kv-caches-rescue-long-range-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  投機的復号（投機的復号）は、小さなドラフトモデルが先の複数トークンを提案し、大きな対象モデルが一括で検証することで逐次生成の遅延を減らす。Qwen3-8Bでの実験では、KV再利用は後方の投機ステップの受理率を改善し、混成方式は小規模な逐次受理評価で平均受理トークン数を2.37から2.54へ増やした。

- **2026-04 · [SAW-INT4: System-Aware 4-Bit KV-Cache Quantization for Real-World LLM Serving](2026-2604.19157-saw-int4-system-aware-4-bit-kv-cache-quantization-for-real-world-llm-ser.md)**  
  実装：[✓](https://github.com/togethercomputer/saw-int4) ・ リポジトリ内被引用：4  
  SAW-INT4は、モデルのキー・値（KV）キャッシュを4ビット整数へ縮めるとき、単に量子化誤差を小さくするのではなく、実際のサービングエンジンで高速に動くデータ配置と演算を先に制約として置く研究である。

- **2026-02 · [You Need an Encoder for Native Position-Independent Caching](2026-2602.01519-you-need-an-encoder-for-native-position-independent-caching.md)**  
  実装：[✓](https://github.com/shijuzhao/Comb) ・ リポジトリ内被引用：4  
  凍結したデコーダ専用LLMへPIC専用エンコーダを追加し、任意順序の文書KV再利用を高精度化しつつTTFTを51〜94%削減、KV容量も約75%以上削減するCOMBを提案。

- **2026-01 · [OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration](2026-2601.10729-orbitflow-slo-aware-kv-cache-reconfiguration.md)**  
  実装：[✓](https://github.com/omnia-postech/OrbitFlow) ・ リポジトリ内被引用：4  
  OrbitFlowは、要求ごとのKVのGPU常駐量とCPU退避間隔をSLOに応じて動的再配置し、退避KVの転送を層計算へ重ねて長文待ち時間を減らす。

- **2026-07 · [[AAFLOW+] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows](2026-2607.10987-aaflow-stateful-operator-abstraction-with-zero-copy-distributed-kv-cache.md)**  
  実装：[✓](https://github.com/arupcsedu/AAFLOW) ・ リポジトリ内被引用：3  
  複数エージェントで検索、計画、推論、回答の統合を進めると、異なるエージェントが同じ文書や会話履歴を読み直す。主要な定量報告では、Mistral-7Bの平均初回トークン時間（TTFT）が0.041秒で、テキストを再計算するAAFLOW-textの2.057秒に対し50.2倍の差がある。

- **2026-05 · [AgentKVShift: Efficient KV Cache Reuse for Agentic Memory Systems](2026-2607.21604-agentkvshift-agentic-memory-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  構造化エージェントメモリの一部トークンだけを再計算し、そこから推定したメモリ単位のKV残差を未再計算トークン全体へ加えて、低い再計算率で品質を回復する。

- **2026-04 · [PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference](2026-2604.24971-polykv-shared-asymmetrically-compressed-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  共通文書のKVキャッシュを一度だけ非対称量子化して共有プール化し、複数エージェントへ注入して重複メモリを削減する。

- **2026-04 · [LKV: End-to-End Learning of Head-wise Budgets and Token Selection for LLM KV Cache Eviction](2026-2605.06676-lkv-end-to-end-learning-of-head-wise-budgets-and-token-selection-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  KVキャッシュの残し方を「どのヘッドへ何トークン分を割り当てるか」と「そのヘッド内でどのトークンを残すか」に分解し、両方をタスクの品質から学習する。

- **2026-04 · [IceCache: Memory-efficient KV-cache Management for Long-Sequence LLMs](2026-2604.10539-icecache-semantic-kv-offload.md)**  
  実装：[✓](https://github.com/yuzhenmao/IceCache) ・ リポジトリ内被引用：3  
  IceCacheは、意味的に近いKVを同じ物理ページへクラスタ化し、関連ページだけをCPUから一括転送して、長文のGPU KV容量とPCIeデータ量を減らす。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

- **2026-03 · [LongFlow: Efficient KV Cache Compression for Reasoning Models](2026-2603.11504-longflow-efficient-kv-cache-compression-for-reasoning-models.md)**  
  実装：[✓](https://github.com/yisunlp/LongFLow) ・ リポジトリ内被引用：3  
  LongFlowは、長い推論過程を生成するモデルの鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）を、生成中に継続的に圧縮する方式である。

- **2026-03 · [Judge Q: Trainable Queries for Optimized Information Retention in KV Cache Eviction](2026-2509.10798-judge-q-trainable-queries-for-optimized-information-retention-in-kv-cach.md)**  
  実装：[✓](https://github.com/Mambaaaaaaaaa/Judge-Q) ・ リポジトリ内被引用：3  
  既存の注意機構重みや本体Transformerを再学習せず、削除位置の選択を改善する設計である。論文の主評価は同じKV保持数における正解率・タスクスコアであり、追加soft トークンによるプリフィル計算を含めた実機のTTFT、TPOT、メモリピークやスループットの改善を実証したものではない。

- **2026-02 · [InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache for Large Language Models](2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  InnerQは、長文脈デコードで増え続けるキー・バリューキャッシュ（KV キャッシュ）を低ビット化する際、量子化誤差だけでなく「量子化済みKVをGPU上で復号してベクトル行列積（GEMV）へ渡すときのスケール/ゼロ点読み出し」を主要ボトルネックとして設計する調整不要のKV量子化方式である。

- **2025-12 · [Efficient Low Rank Attention for Long-Context Inference in Large Language Models](2025-2510.23649-efficient-low-rank-attention-for-long-context-inference-in-large-languag.md)**  
  実装：[✓](https://github.com/tenghuilee/LRQK) ・ リポジトリ内被引用：3  
  Q・Kの共同低ランク索引で重要KVを選び、CPU上の完全精度KVから欠損分だけGPUへ取得して長文脈の容量制約を緩和する。

- **2025-11 · [Lethe: Layer- and Time-Adaptive KV Cache Pruning for Reasoning-Intensive LLM Serving](2025-2511.06029-lethe-layer-and-time-adaptive-kv-cache-pruning-for-reasoning-intensive-l.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Letheは、長い思考過程を文章として生成する大規模言語モデル（LLM）の推論時に、鍵・値キャッシュ（KVキャッシュ）を保持し続けることによるメモリ消費と注意計算の増大を抑える方式である。

- **2026-09 · [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md)**  
  実装：[✓](https://github.com/LiuTaowen-Tony/agentkv) ・ リポジトリ内被引用：2  
  思考・行動・ツール応答など段階別の問い合わせ履歴でKV重要度を評価し、エージェントの段階遷移で必要になる古い状態を残しつつ、物理ページ圧縮で最大1.80倍の出力スループットを得る。

- **2026-08 · [RestoreKV: Recovering Full-Cache Behavior Under Aggressive Query-Agnostic KV Cache Eviction](2026-2608.01247-restorekv-recovering-full-cache-behavior-under-aggressive-query-agnostic.md)**  
  実装：[✓](https://github.com/cvsp-lab/RestoreKV) ・ リポジトリ内被引用：2  
  RestoreKVは、将来の質問がまだ分からない段階で長文脈の鍵値キャッシュ（Key–Value キャッシュ、KVキャッシュ）を圧縮する推論方式に、少数の学習済み補完状態を追加する手法である。保持割合が十分なら有効だが、容量を5%程度まで削ると、選別器がどれほど優れていても消失した情報を後の質問から取り戻せない。

- **2026-08 · [Fewer Tokens, Smaller Cache: Reward-Coordinated Efficient Reasoning](2026-2608.04771-fewer-tokens-smaller-cache-reward-coordinated-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ReCo（Reward-Coordinated Compression）は、長い思考連鎖を生成する推論モデルの実行費用を、KVキャッシュの削減と、これから生成する思考トークンの削減を同時に制御する方式である。

- **2026-08 · [Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression](2026-2608.01631-does-accuracy-equal-evidence-reasoning-faithfulness-under-kv-cache-compr.md)**  
  実装：[✓](https://github.com/famous-blue-raincoat/Safe_KV_Compress) ・ リポジトリ内被引用：2  
  保持トークンを選別して捨てる方式はメモリを節約できるが、一般的な評価は最終回答の正答率を重視する。非圧縮の正答率67.4%、正答中の不完全推論率4.3%に対し、SnapKVは正答率50.0%を維持しても不完全推論率が65.5%に増えた。

- **2026-07 · [SemPIC: Learning Semantic Position-Independent KV Caches](2026-2607.28069-sempic-learning-semantic-position-independent-kv-caches.md)**  
  実装：[✓](https://github.com/jn12-29/SemPIC) ・ リポジトリ内被引用：2  
  SemPICは、検索拡張生成（Retrieval-Augmented Generation、RAG）やエージェントの長い文書文脈を、問い合わせや文書順序が変わっても再利用するための位置非依存キャッシュ（Position-Independent Caching、PIC）方式である。

- **2026-07 · [ResKV: Reconstructing Omitted Attention Contributions for Fixed-Budget KV Cache Compression](2026-2607.29591-reskv-reconstructing-omitted-attention-contributions-for-fixed-budget-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  重要トークンへ削除側の情報を混ぜ込む方式もあるが、厳密に保持したい鍵・値自体が改変され、特定箇所の検索に悪影響を与える場合がある。

- **2026-07 · [KV Cache Translation across Heterogeneous Large Language Models](2026-2607.28979-kv-cache-translation-across-heterogeneous-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の単一射影や共有潜在空間を介す方式と異なり、MoTは複数の変換器を用意し、トークンごとに適切な変換器を上位K個選択して出力を混合する。Llama-3.2 3B、Gemma-3 4B、Qwen-3 4B間の異種変換を評価し、閉集合質問応答の平均正解率57.6%、抽出型質問応答の平均F1 0.42を報告する。

- **2026-07 · [HYPIC: Accelerating Hybrid-Attention LLM Serving with Position-Independent Caching](2026-2607.01299-hypic-hybrid-attention-position-independent-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  線形注意区間の累積遷移演算子とゼロ始動状態を保存して位置非依存に合成し、完全注意層は境界窓だけ再計算、未保存区間は複数実体で並列処理することで、ハイブリッド注意言語モデルの初トークン待ち時間を平均3.25倍短縮する。

- **2026-07 · [A JoLT for the KV cache: Near-Lossless KV Cache Compression via Joint Rank-bit Allocation](2026-2607.12550-a-jolt-for-the-kv-cache-near-lossless-kv-cache-compression-via-joint-ran.md)**  
  実装：[✓](https://github.com/rahulk98/JoLT-Master-Thesis) ・ リポジトリ内被引用：2  
  従来の低ランク圧縮は保持する特異ベクトル数を決め、量子化は値のビット幅を決めるが、両者を同じメモリ予算の下で同時に配分することは一般的ではなかった。5モデル・4系列の評価では2〜3倍のKV圧縮でパープレキシティ（perplexity）の相対変化を0.2%未満に抑えた。

- **2026-06 · [Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving](2026-2606.06302-tangram-non-uniform-kv-cache.md)**  
  実装：[✓](https://github.com/aiha-lab/TANGRAM) ・ リポジトリ内被引用：2  
  Tangramは、ヘッド別KV保持量を少数サンプルで事前較正し、固定予算のraggedページ化と負荷分散へ変換して、非一様圧縮の断片化・回収費・デコード不均衡を減らす。

- **2026-06 · [ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning Models](2026-2606.11164-reasonalloc-hierarchical-decoding-time-kv-cache-budget-allocation-for-re.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ReasonAllocは、長い思考過程を逐次生成する推論モデルにおいて、復号中に増え続ける鍵・値キャッシュ（KVキャッシュ）の保持予算をどの層・どの注意頭へ割り当てるかを最適化する手法である。まずモデルごとに少数の入力を使って、各層が注意重みの93%を保持するのに必要な履歴トークン数を測り、層別の予算比率を事前校正する。

- **2026-06 · [RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference](2026-2606.31519-rabitqcache.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈大規模言語モデルでは、復号の各ステップで巨大なKVキャッシュから注意計算用データを読むことがメモリ帯域のボトルネックになる。RaBitQCacheはランダム回転と二値量子化で小型索引を作り、不偏な注意スコア推定から累積確率に応じて必要量を変える上位確率検索（Top-p）を行う。

- **2026-06 · [Multi-Segment Attention: Enabling Efficient KV-Cache Management for Faster Large Language Model Serving](2026-2606.02964-multi-segment-attention-enabling-efficient-kv-cache-management-for-faster-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AsymCacheは、非連続KV区間を一つの注意カーネルで統合し、再利用確率と再計算遅延で追い出し、負荷適応チャンク化で長文サービングのGPU計算と管理費を減らす。

- **2026-06 · [Kamera: Unified Position-Invariant Multimodal KV Cache for Training-Free Reuse](2026-2606.23581-kamera-unified-position-invariant-multimodal-kv-cache-for-training-free-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Kameraは、画像・動画・画面の断片を繰り返し参照する視覚言語モデルのエージェントで、以前に計算した鍵・値キャッシュ（KVキャッシュ）を異なる文脈位置へ移して再利用するための方式である。

- **2026-06 · [Information-Aware KV Cache Compression for Long Reasoning](2026-2606.26875-information-aware-kv-cache-compression-for-long-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の鍵値キャッシュ（KV キャッシュ）圧縮は、直近の問い合わせから大きな注意（注意機構）を受けたトークンを残す設計が多い。LongReasonでは40%・20%の鍵値キャッシュ保持率でSnapKV、PyramidKV、Expected 注意機構を上回り、長い復号でもRPCより高いタスク性能を示す。

- **2026-05 · [TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Agentic Inference Tasks](2026-2605.17170-triaxialkv-toward-extreme-low-precision-kv-cache-quantization-for-agenti.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長い対話履歴を保持するエージェント型大規模言語モデルでは、システム指示、ツール定義、過去の会話、画像、ツール実行結果が同じ鍵・値キャッシュ（KVキャッシュ）に混在する。

- **2026-05 · [ReST-KV: Robust KV Cache Eviction with Layer-wise Output Reconstruction and Spatial-Temporal Smoothing](2026-2605.08840-rest-kv-robust-kv-cache-eviction-with-layer-wise-output-reconstruction-a.md)**  
  実装：[✓](https://github.com/an-yongqi/rest-kv) ・ リポジトリ内被引用：2  
  自己回帰生成では、過去トークンのキーとバリューを各層・各ヘッドに保存する。入力文脈が伸びるとキャッシュの占有量と復号時の読み出しが増え、長文脈の同時提供でメモリ容量・帯域の制約が強くなる。従来のH2OやSnapKVなどは注意重みの累積・観測窓内の集約を重視するが、トークンを削除するとソフトマックスの分母が変わり、残されたトークンへの注意が再分配される。

- **2026-05 · [KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression](2026-2607.01237-kara-sliding-window-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KARAは、新しく増えたKV区間だけを一度ずつ圧縮し、重要トークンを可変長チャンクへ広げ、周期発動で再圧縮費を抑えて長い推論の同時実行数を保つ。

- **2026-04 · [Unifying Sparse Attention with Hierarchical Memory for Scalable Long-Context LLM Serving](2026-2604.26837-spin-sparse-attention-hierarchical-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SPINは、異なる疎注意方式の選択単位を共通ページへ写し、要求ごとのKV予算とGPU局所性キャッシュを調整して、階層メモリの転送とHBM圧力を減らす。

- **2026-04 · [The Illusion of Equivalence: Systematic FP16 Divergence in KV-Cached Autoregressive Inference](2026-2604.15409-the-illusion-of-equivalence-systematic-fp16-divergence-in-kv-cached-auto.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  数学的には、毎回すべての接頭辞を再計算する経路と同じ注意計算を実行するはずである。新しい高速化カーネルやKV圧縮方式を提案する研究ではない。さらに32ビット浮動小数点（FP32）へ切り替えると、著者らの別の対照実験ではトークン反転が0%となり、出力分布差が大幅に減った。

- **2026-04 · [Sub-Token Routing for KV Cache Compression](2026-2604.21335-sub-token-routing-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来のQuestなどの手法は「どのトークンを残すか」を決め、視覚言語モデルのFastVやVisionZipは大量の視覚トークンを減らす。

- **2026-04 · [Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing](2026-2604.22782-stochastic-kv-routing-enabling-adaptive-depth-wise-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  既存の削減手法の多くは「どの時刻のトークンを捨てるか」に着目するが、本研究は「どの層が独自のKVを持つ必要があるか」を問い直す。

- **2026-03 · [The Residual Stream Is All You Need: On the Redundancy of the KV Cache in Transformer Inference](2026-2603.19664-the-residual-stream-is-all-you-need-on-the-redundancy-of-the-kv-cache-in.md)**  
  実装：[✓](https://github.com/Kaleemullahqasim/KV-Direct) ・ リポジトリ内被引用：2  
  著者らはこの事実を残差の十分性として整理し、古いKVを破棄して残差ベクトルのチェックポイントを保持するKV-Directを提案した。原著の全系列を毎回再計算する比較では、30トークン生成が標準キャッシュ方式より1.7～3.8倍遅かった。

- **2026-03 · [KVSculpt: KV Cache Compression as Distillation](2026-2603.27819-kvsculpt-kv-cache-compression-as-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の追い出し方式は重要な元トークン位置を選び、結合方式も元の位置・ベクトルに由来する値を作る。

- **2026-03 · [Hybrid Associative Memories](2026-2603.22325-hybrid-associative-memories.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本研究は、系列全体を固定長状態へ圧縮する再帰型ニューラルネットワーク（Recurrent Neural Network; RNN）と、過去の各トークンを個別に保持する自己注意（Self-注意機構）を、単に交互に積むのではなく相補的な二つの記憶として組み合わせる。

- **2026-01 · [SONIC: Segmented Optimized Nexus for Information Compression in Key-Value Caching](2026-2601.21927-sonic-segmented-optimized-nexus-for-information-compression-in-key-value.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  多ターンの対話では、過去のユーザー発話とモデル応答が蓄積するたびに鍵値キャッシュが増え、メモリ使用量と新しいトークンの注意計算が重くなる。SONICは対話のターン境界を利用し、過去の各メッセージを少数の学習可能なNexusトークンへ集約する方式である。

- **2025-12 · [Accurate KV Cache Eviction via Anchor Direction Projection for Efficient LLM Inference](2025-fc5da84b7582-accurate-kv-cache-eviction-via-anchor-direction-projection-for-efficient.md)**  
  実装：[✓](https://github.com/MIRALab-USTC/LLM-AnDPro) ・ リポジトリ内被引用：2  
  従来のH2OやSnapKVは、注意重みの大きいトークンほど重要とみなす。だが注意出力は、注意重みと値ベクトルの積を足し合わせたベクトル和である。重みが大きくても値ベクトルが出力方向に寄与しなければ、そのトークンを残す意義は小さい。逆に重みが比較的小さくても、出力方向へ強い成分を持つ値は重要になりうる。

- **2025-11 · [FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management](2025-2511.00868-flexicache-leveraging-temporal-stability-of-attention-heads-for-efficient-kv-cache-management.md)**  
  実装：[✓](https://github.com/NazmulTakbir/FlexiCache) ・ リポジトリ内被引用：2  
  重要KVページが時間的に入れ替わりやすい注意ヘッドだけ全KVをGPUへ残し、安定ヘッドは上位ページ以外をCPUへ退避・周期再昇格することで、精度を保ちながらGPUメモリを最大70%削減する。

- **2026-10 · [Monte Carlo Estimation for KV Cache Eviction](2026-2610.07643-monte-carlo-estimation-for-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  履歴が長くなるほどメモリ容量と転送帯域を圧迫するため、限られた保持枠に重要なトークンだけを残す削除方式が研究されている。一方、同じ条件のサンプル当たり実行時間はAnDProの7.8799秒に対し17.5342秒であり、速度向上ではない。

- **2026-09 · [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](2026-2609.03430-random-attention-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/Random-Attention) ・ リポジトリ内被引用：1  
  Random 注意機構は、入力文を必ず保持し、生成した推論過程のKVだけをヘッド別に無作為保持することで、選択器の採点計算を省き、同じ容量で強い選択法に近い正答率と高い提供スループットを得る。

- **2026-09 · [PatchKV: Weight-Space Compensation of KV Cache](2026-2609.39329-patchkv-weight-space-compensation-of-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数の質問が同じ長い文書やコードベースを参照する場合、文脈を一度だけ読み込み、そのKVを再利用することで質問ごとの計算を減らせる。

- **2026-09 · [Language Models Can Control Their Own Attention](2026-2609.02737-declarative-attention-self-directed-kv-access.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル自身が思考中に注意範囲を宣言し、推論エンジンがKVブロック表を切り替えて不要な長文脈読出しを省く疎注意方式。Gemma-4-31Bで参照トークンを52.0%削減し、精度低下は1.27ポイントだった。

- **2026-09 · [EchoPress: Query-Agnostic KV Cache Pruning via Virtual Context Reconstruction](2026-2610.00412-echopress-query-agnostic-kv-cache-pruning-via-virtual-context-reconstruc.md)**  
  実装：[✓](https://github.com/ljwljwljwljw/kvpress/tree/echo-press) ・ リポジトリ内被引用：1  
  複数の質問で同じ長文を再利用したい場合、質問を受け取ってから重要なトークンを決める方法では、圧縮済みキャッシュを別の質問へ使い回すことが難しい。著者の実測では、KVzipの圧縮追加時間が対応する通常の入力処理時間の約2.1〜2.2倍になる。

- **2026-09 · [Cartridges++: KV Cache Compression without Off-Context Derailment](2026-2609.35621-cartridges-kv-cache-compression-without-off-context-derailment.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  文書を一度だけ処理し、少数の仮想KV位置へ圧縮した記憶を複数の質問で再利用できれば、デコード時に参照するKV長を減らせる。主要なQwen3長文3課題で、後者の関連性ルータは文書内質問の90%超を受理し、文書外質問の90%超を拒否した。

- **2026-09 · [ARC-KV: Amortizing Anchor Search for Reconstruction-Based KV Cache Compaction](2026-2609.36835-arc-kv-amortizing-anchor-search-for-reconstruction-based-kv-cache-compac.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  通常の削除型圧縮では、残すトークンを選んで元の鍵と値をそのまま保存する。Llama-3.1-8B-InstructとQuALITYの評価では、KV保持率10%でAMの正解率0.6409に対してARC-KVは0.6474、圧縮時間は959.8秒から37.3秒へ短縮し、25.73倍となった。

- **2026-08 · [vToken: Token-Level Virtualization for Reclaimable KV Caches](2026-2608.13263-vtoken-token-level-virtualization-for-reclaimable-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ページ化注意（PagedAttention）は固定長ブロックを非連続配置して外部断片化を抑えるが、H2OやScissorhandsなどの削除方策は「残すトークン」をブロックより細かい単位で選ぶ。

- **2026-08 · [Trust the Mass: Forced Weights in KV-Cache Eviction](2026-2608.25230-trust-the-mass-forced-weights-in-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  5系列・計168,192注意行の検査で、候補プール内の最良集合へ切り替えて埋められる差は、残存誤差の中央値で約2〜5%であった。

- **2026-08 · [TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning](2026-2608.03276-taskpress-query-agnostic-kv-cache-compression-via-task-guided-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一方、再構築を使うKVzip型の方式は複数質問への適応を狙えるが、文脈をもう一度長く処理する費用が生じる。LLaMA-3.1-8B-InstructのLongBench平均では、int4 KVを前提に75%削除時、TaskPress 43.08、KVzip 38.24、SnapKV 39.37である（表1）。

- **2026-08 · [Spend Bits Where Queries Look: KV Cache Vector Quantization with Attention-Preserving Transforms](2026-2608.04074-spend-bits-where-queries-look-kv-cache-vector-quantization-with-attentio.md)**  
  実装：[✓](https://github.com/Amir-zsh/nova-kv) ・ リポジトリ内被引用：1  
  文脈長と同時実行数に比例してキャッシュが増えるため、読み出し帯域が復号速度と同時収容数の制約になる。NOVA-KVは、このキャッシュを単に数値として再現するのではなく、照会と鍵の内積、および注意重みと値の積を保つことを量子化の目的に置く。

- **2026-08 · [ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents](2608.19662.md)**  
  実装：[✓](https://github.com/EIT-NLP/ReCache) ・ リポジトリ内被引用：1  
  ツール／スキル定義を組合せ非依存のKVブロックとして再利用し、重要な層・KVヘッド群と呼出し必須フィールドだけを残して、エージェント推論のプリフィルとKVメモリを削減する。

- **2026-08 · [GraniKV: Asymmetric Granularity KV-Cache Paging for Multi-Agent Systems with Long Shared Prefix](2026-2608.15584-granikv-asymmetric-granularity-kv-cache-paging-for-multi-agent-systems-w.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数エージェント型の大規模言語モデル推論では、システム指示、道具定義、共有メモリなどからなる長い接頭辞を複数要求が共有し、その後ろに各要求固有の生成履歴が接尾辞として伸びる。

- **2026-08 · [CommitKV: Lifecycle-Aware KV Cache Compression via Commit Transitions for Multi-Turn Agents](2026-2608.07855-commitkv-lifecycle-aware-kv-cache-compression-via-commit-transitions-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CommitKVは、工具呼出しを伴う多輪の推論・行動型エージェント（ReAct agent）で増大する鍵・値キャッシュ（KV キャッシュ）を、情報の利用状態が変化した瞬間を利用して削減する手法である。

- **2026-07 · [SpecCache: Speculative KV Cache Reuse for Efficient RAG Serving](2026-2c3e6cdc141b-speccache-speculative-kv-cache-reuse-for-efficient-rag-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  検索拡張生成（Retrieval-Augmented Generation; RAG）は検索された複数の文書片を質問へ追加するため、初回トークンの生成までに必要な事前充填（プリフィル）が長くなる。単純な全再利用は回答品質を落とし、全再計算は遅い。ただしこの倍率は特定の検索拡張生成ワークロード、GPU、キャッシュの事前作成・保持という条件に依存する。

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

- **2026-07 · [HqeKV: Towards Hybrid Quantization and Eviction for KV Cache in Long-Context LLM Inference](2026-ec9fa0b99268-hqekv-towards-hybrid-quantization-and-eviction-for-kv-cache-in-long-cont.md)**  
  実装：[✓](https://github.com/skywclouds/HqeKV) ・ リポジトリ内被引用：1  
  一方、文脈長や同時要求数が増えるほどキャッシュがGPUメモリを占め、実行可能なバッチ数を制約する。従来の低ビット量子化は多くのトークンに同じ精度を割り当て、削除方式は低重要度と判断したトークンの情報を完全に失う。著者の実機評価はRTX A6000（48GB）上のLlama-3.1-8B-InstructおよびQwen3-8Bで実施された。

- **2026-07 · [HiKV: Hierarchical Importance-Aware KV Cache with Hardware Acceleration for LLM Decoding](2026-2607.22389-hikv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HiKVは、長文脈デコードでKVキャッシュが外部メモリアクセスの大部分を占める問題に対し、トークン単位と要素単位という二つの独立した冗長性を順番に削るアルゴリズム・ハードウェア協調設計である。1%以内の精度低下という同一条件で外部メモリアクセスを平均7.17倍削減し、注意計算を平均5.70倍、最大7.95倍高速化し、エネルギーを80〜90%削減する。

- **2026-07 · [GroupKV: Hierarchical KV Cache Management for Long-Context Diffusion LLM Inference](2026-2609.17573-groupkv-hierarchical-kv-cache-diffusion-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散型LLMの長文KVを連続グループ単位で疎選択し、層間予測先読みと古さ補正を組み合わせてCPU退避時の転送量と待ち時間を削減する。

- **2026-07 · [Adaptive Filtering of the KV Cache: Diagnosing and Correcting Structural-Role Bias in LLM Inference](2026-2607.13205-adaptive-filtering-of-the-kv-cache-diagnosing-and-correcting-structural-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文推論のKVキャッシュを圧縮するとき、H2Oに代表される方式は過去のqueryから多くの注意を受けたトークンを重要とみなし、保持予算の上位へ残す。Llama-3.1-8B-Instructの合成JSONでは、区切り記号のトークン当たり平均注意量13.64に対し、回答を持つ値は0.336であり、約40倍の開きがある。

- **2026-06 · [Vortex: Efficient and Programmable Sparse Attention Serving for AI Agents](2026-2606.06453-vortex-programmable-sparse-attention-serving.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/vortex_torch) ・ リポジトリ内被引用：1  
  ページ化KVを抽象化するvFlow/vTensorと最適化バックエンドで、動的疎注意を数行のPython表現からSGLang実運用へ落とし込み、全注意比最大3.60倍のスループットを実現する。

- **2026-06 · [RoPE-Aware Bit Allocation for KV-Cache Quantization](2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/blockgtq) ・ リポジトリ内被引用：1  
  回転位置埋め込みの周波数ブロックごとのエネルギーに応じて鍵キャッシュのビット幅を配分し、圧縮した鍵・値を直接読む融合注意計算で長文脈推論の容量とメモリ帯域を同時に削減する。

- **2026-06 · [PTStore (Prefix Tensor Store): Distributed Prefix Caching and Replication for High Throughput Inference Serving](2026-2607.22648-ptstore-prefix-tensor-store-distributed-prefix-caching-and-replication-f.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同じ長文やシステムプロンプトを含む問い合わせを複数GPU・計算ノードで処理すると、共通prefixに対して入力処理で計算した注意機構のkey/value（KV）を要求ごとに再生成する。著者は長文文書 QAで、メモリを複数ノード/GPUに集約しない比較方式より5–6倍効率的と要旨で総括する。

- **2026-06 · [CompressKV: Semantic-Retrieval-Guided KV-Cache Compression for Resource-Efficient Long-Context LLM Inference](2026-2606.24467-compresskv-semantic-retrieval-guided-compression.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：1  
  CompressKVは、意味的証拠を検索する注意ヘッドだけでKVトークンを選び、層ごとの追い出し感度で容量を配分して、同じKV予算で長文品質を保つ。

- **2026-05 · [WaveFilter: Enhancing the Long-Context Capability of Diffusion LLMs via Wavelet-Guided KV Cache Filtering](2026-2606.00724-wavefilter-enhancing-the-long-context-capability-of-diffusion-llms-via-w.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  WaveFilterは、拡散型大規模言語モデル（diffusion LLM; dLLM）が長い文脈を処理するとき、鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）の重要な位置を選別して注意機構へ渡す方式である。

- **2026-05 · [Reformulating KV Cache Eviction Problem for Long-Context LLM Inference](2026-2605.07234-reformulating-kv-cache-eviction-problem-for-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  既存の追い出し手法は、過去のトークンが受けた注意重みを平均・集計し、その値の大きな位置を残すことが多い。NVIDIA H100 80GBでのLlama-3.1-8B、128K文脈、同保持予算の効率測定では、完全キャッシュ比で復号のトークン当たり遅延が2.3倍改善し、最大メモリは63.3GBから約47.5GBへ低下した。

- **2026-05 · [OCTOPUS: Optimized KV Cache for Transformers via Octahedral Parametrization Under optimal Squared error quantization](2026-2605.21226-octopus-optimized-kv-cache-for-transformers-via-octahedral-parametrizati.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  OCTOPUSは、Transformerの長文脈推論で肥大化するKVキャッシュを、回転前処理と3座標単位の幾何学的量子化によって縮小する研究である。一方、H200で測った単一クエリの融合デコードはbf16 SDPAより8.9倍遅い条件がある。

- **2026-05 · [CONF-KV: Confidence-Aware KV Cache Eviction with Mixed-Precision Storage for Long-Horizon LLM Inference](2026-2605.24786-conf-kv-confidence-aware-kv-cache-eviction-with-mixed-precision-storage-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  過去の注意重みに基づく方式は、重要そうなトークンを選別できる反面、将来どの情報が必要になるかを正確には予測できない。

- **2026-05 · [ArborKV: Structure-Aware KV Cache Management for Scaling Tree-based LLM Reasoning](2026-2605.22106-arborkv-structure-aware-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  活動経路の保護、トークン単位の選択的追い出し、後戻り時の遅延再構築を組み合わせ、単一RTX 4090上のToT評価で同一キャッシュ予算の系列方式を上回り、256展開の探索を5.6 GiBで完了した。

- **2026-04 · [Retrospective Sparse Attention for Efficient Long-Context Generation](2026-2508.09001-retrospective-sparse-attention-for-efficient-long-context-generation.md)**  
  実装：[✓](https://github.com/csh3695/RetroAttention) ・ リポジトリ内被引用：1  
  arXiv:2508.09001の2026年5月20日改訂版（v2）を一次資料とし、本文・表・付録の実験条件を確認した。目的は、長い入力を一度読むプリフィルだけでなく、数千トークンに及ぶ生成の途中で疎な注意計算の近似誤差が蓄積する問題を軽減することにある。提案名はRetrospective Sparse 注意機構、実装名はRetroAttentionである。

- **2026-04 · [DASH-KV: Accelerating Long-Context LLM Inference via Asymmetric KV Cache Hashing](2026-2604.19351-dash-kv-asymmetric-hashing-long-context.md)**  
  実装：[✓](https://github.com/Zhihan-Zh/DASH-KV) ・ リポジトリ内被引用：1  
  注意の全キー内積を学習済み非対称ハッシュ検索へ置換し、重要トークンだけ完全精度へ戻すことで、長文脈の計算量を線形化しつつLongBench品質をFull 注意機構近傍に維持する。

- **2026-03 · [EntropyCache: Decoded Token Entropy Guided KV Caching for Diffusion Language Models](2026-2603.18489-entropycache-decoded-token-entropy-guided-kv-caching-for-diffusion-langu.md)**  
  実装：[✓](https://github.com/mscheong01/EntropyCache) ・ リポジトリ内被引用：1  
  自己回帰型言語モデルの因果注意では、過去トークンの鍵・値（Key–Value; KV）表現は後続トークンの追加で変わらないため、過去KVを厳密に再利用できる。これに対して離散拡散言語モデル（discrete Diffusion Language モデル; dLLM）は双方向注意を使い、マスクされたトークンが一つ確定するだけで他の全位置の表現が変わり得る。

- **2026-03 · [ELORA: Efficient LoRA and KV Cache Management for Multi-LoRA LLM Serving](2026-d563756c245c-elora-efficient-lora-and-kv-cache-management-for-multi-lora-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数の低ランク適応（LoRA）を単一の基盤LLMで提供するサービスでは、リクエストに応じてアダプタを切り替えつつ、過去の会話のKVキャッシュを再利用する。著者らが測定したvLLMではGPU上のKVの平均42.4%がその状態だった。

- **2026-03 · [EchoKV: Efficient KV Cache Compression via Similarity-Based Reconstruction](2026-2603.22910-echokv-efficient-kv-cache-compression-via-similarity-based-reconstructio.md)**  
  実装：[✓](https://github.com/noforit/EchoKV) ・ リポジトリ内被引用：1  
  圧縮方式の一つである低ランク分解は、重み行列を変形して保存すべきKVの次元を減らすが、変形後のモデルを短文・長文の負荷に応じて元の通常推論へ戻すことが難しい。これらは圧縮率50%で精度が常に完全維持されるという結果ではなく、課題ごとの悪化もある。

- **2026-02 · [ARKV: Adaptive and Resource-Efficient KV Cache Management under Limited Memory Budget for Long-Context Inference in LLMs](2026-2603.08727-arkv-adaptive-and-resource-efficient-kv-cache-management-under-limited-m.md)**  
  実装：[✓](https://github.com/Large-scale-Sustainable-Computing-LSC/ARKV) ・ リポジトリ内被引用：1  
  ARKVは、長文脈の自己回帰言語モデルで増大するキー・値キャッシュ（KVキャッシュ）を、原精度で保持するトークン、低精度へ量子化するトークン、破棄するトークンの三種類へ動的に割り当てる推論時の管理方式である。原精度の基準モデルに対する生成速度は平均86.1%であり、圧縮が無条件に高速化をもたらすわけではない。

- **2026-01 · [Singular Proxies for Adaptive Caching in Diffusion Language Models](2026-2602.02544-singular-proxies-for-adaptive-caching-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/wenhao728/spa-cache) ・ リポジトリ内被引用：1  
  自己注意（self-注意機構）が双方向であるため、ある位置のトークンを更新すると別の位置の隠れ状態にも影響が及び、自己回帰型モデルのように過去の鍵・値（KV）を常に固定したまま再利用することはできない。LLaDA-8BのMBPPでは通常復号5.75トークン/秒に対し46.12トークン/秒（8.0倍）で、正解率は39.20から39.00へ変化した。

- **2026-01 · [HeteroCache: A Dynamic Retrieval Approach to Heterogeneous KV Cache Compression for Long-Context LLM Inference](2026-2601.13684-heterocache-dynamic-heterogeneous-kv-retrieval.md)**  
  実装：[✓](https://github.com/ponytaill/HeteroCache) ・ リポジトリ内被引用：1  
  注意ヘッドの安定性と層内冗長性に応じてKV予算を細粒度配分し、代表ヘッドの注意ドリフト検知時だけCPUから非同期取得することで、224K文脈の復号を完全注意計算比約3倍高速化する。

- **2026-01 · [ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management](2026-2601.13631-contiguouskv-accelerating-llm-prefill-with-granularity-aligned-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV 枝刈りとI/Oの粒度をContiguousChunkへ統一し、二段非同期プリフェッチでSSD KV読み込みを計算と重ねてRe-プリフィルを最大3.85倍高速化する。

- **2025-11 · [Revisiting Multimodal KV Cache Compression: A Frequency-Domain-Guided Outlier-KV-Aware Approach](2025-2511.16786-revisiting-multimodal-kv-cache-compression-a-frequency-domain-guided-out.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlashCacheは、画像・動画を扱う視覚言語モデルの長文入力で膨らむ鍵・値キャッシュ（KVキャッシュ）を、注意スコアを再計算せずに削減する方式である。著者は単一NVIDIA H200 141GBで、KV保持率20%の長文復号において最大1.69倍の速度を報告する。

- **2025-11 · [FlowMM: Cross-Modal Information Flow Guided KV Cache Merging for Efficient Multimodal Context Inference](2025-2511.05534-flowmm-cross-modal-information-flow-guided-kv-cache-merging-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlowMMは画像と文章が混在する多模態大規模言語モデル（MLLM）の推論時に、注意のキー・値キャッシュ（KVキャッシュ）を破棄ではなく結合によって圧縮する方式である。KV保持予算20%では、InternVL2.5-8Bの平均指標が全KV保持の27.97から27.85へと0.12ポイントの低下にとどまる。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](2026-2610.12060-look-back-think-ahead-visual-memory-on-demand-for-efficient-multimodal-r.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像の内容を一度だけ要約して視覚トークンを削減すると、生成する文章の最初の段階では十分でも、後の推論段階で必要な細部が削除済みという問題が起こる。固定的な重要度で一回だけ残す方式は、この変化を事前にすべて予測する必要がある。

- **2026-10 · [Efficient KV Cache Migration for Geo-Distributed LLM Inference in Collaborative Edge Computing](2026-2610.22172-efficient-kv-cache-migration-for-geo-distributed-llm-inference-in-collab.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層単位で両方式を混合して通信と再計算を重ね、さらに複数の送信元に対する移動先の選択を最適化することで、移送の完了時刻を短縮する。条件によって直接転送比で約35～45%の移送時間短縮を報告する。

- **2026-10 · [Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches](2026-2610.09827-dual-qk-sharp-queries-and-flat-keys-for-prunable-2-bit-kv-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の長文推論では、過去トークンの鍵・値キャッシュ（KV キャッシュ）がGPUメモリを圧迫し、復号のたびに大量のキーを読み直す。KVを2ビットへ量子化すれば保存容量は減るが、注意スコアに敏感な外れ値が量子化範囲を広げ、精度が崩れる。保存容量の約6.8倍削減と読出量の約8.3倍削減は形式・アクセス量の推定であり、実測速度そのものではない。

- **2026-09 · [Where Should the KV Cache Live? Placement Policies Across GPU, CPU, and SSD for Long-Lived Sessions](2026-2609.16215-where-should-the-kv-cache-live-placement-policies-across-gpu-cpu-and-ssd-for-long-lived-sessions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU・CPU・SSD間のKV配置政策を比較し、SSDの容量利得とワークロード別の最適配置・遅延境界を定量化する。

- **2026-09 · [Where Activation Sparsity and KV-Cache Sparsity Cross in LLM Decoding](2026-2609.33889-where-activation-sparsity-and-kv-cache-sparsity-cross-in-llm-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/ByteCross) ・ リポジトリ内被引用：0  
  LLMの一トークン復号では、線形層の重みをメモリから読み込む費用と、過去文脈のKVキャッシュを読み込む費用が競合する。前者はモデルの構造でほぼ固定され、後者は文脈長に比例して増える。活性化疎化は現在の入力で活性化しているニューロンに対応する射影重みだけを読み込み、KV疎化は注意で参照する過去トークンを選んでキャッシュ読出しを減らす。

- **2026-09 · [When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse](2026-2609.28870-when-fancy-eviction-fails-rethinking-cache-replacement-for-llm-prefix-re.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  接頭辞キャッシュ（prefix キャッシュ）は長文脈の事前充填（プリフィル）費用を下げる重要な機構だが、GPUの高帯域幅メモリ（HBM）には容量制限があるため、どのブロックを保持し、どれを退避するかを決める必要がある。

- **2026-09 · [What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation](2026-2609.03515-inertiakv-temporal-aggregation-ranking-preservation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  InertiaKVはデコード中の注意スコアをEMAで蓄積して保持順位を安定させ、Lazy4で更新を4ステップに1回へ間引き、KV再評価の計算費と一時的な誤追い出しを減らす。

- **2026-09 · [VestigeKV: The NoPE-MLA KV Cache Carries Its Own Eviction Signal in a Vestigial Branch](2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-eviction-signal-in-a-ves.md)**  
  実装：[✓](https://github.com/fan-wenjie/vestigekv) ・ リポジトリ内被引用：0  
  選ばれた行だけを毎回の注意計算へ送り、残りはビット列を変えずGPU内の退避領域へ保存する。著者の実装資料は、Kimi Linear 48B-A3Bを対象とした2台のRTX PRO 6000 Blackwellで、単一要求の連続復号において256K文脈で約1.28倍、496Kで約1.46倍の速度比を示す。

- **2026-09 · [Validating Hybrid-State Cache Recovery for GLM-5.3-Flash with vLLM and LMCache](2026-2609.15030-validating-hybrid-state-cache-recovery-for-glm-5-3-flash-with-vllm-and-lmcache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GLM-5.3-Flash＋vLLM＋LMCacheの完全キャッシュヒット境界ずれを厳密プレフィックス復旧で修正し、出力同一性を保ったCPUキャッシュ再ロードのTTFT短縮を実証。

- **2026-09 · [Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management](2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-mana.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Unified AI Gatewayは、複数の大規模言語モデルを使い分ける推論サービスにおいて、モデルを切り替えるたびに鍵値キャッシュ（KVキャッシュ）が使えなくなり、長い入力を最初から処理し直す問題を扱う。モデル切替確率を変えた条件で、初回トークン時間の代理指標は1.25〜13.28倍、入力費用は1.20〜6.16倍改善する余地があると報告する。

- **2026-09 · [To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems](2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-.md)**  
  実装：[✓](https://github.com/FastLM/KVLearn) ・ リポジトリ内被引用：0  
  大規模言語モデルの推論を、入力を一括処理するプリフィル（プリフィル）ノードと、生成を継続する復号（デコード）ノードへ分離すると、キー・バリューキャッシュ（KV キャッシュ）の価値は単なる「最後に使われた時刻」では決まらなくなる。

- **2026-09 · [The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems](2026-2609.27746-kv-cache-working-set-online-capacity-planning.md)**  
  実装：[✓](https://github.com/llc-kc/kv_cache_capacity_estimator) ・ リポジトリ内被引用：0  
  LRUのスタック距離をFenwick木で解析し、接頭辞KVキャッシュの目標ヒット率に必要な容量を1回の要求トレースからオンライン推定する。

- **2026-09 · [The KV Cache Is the New Memory Wall](2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しいKV圧縮器やGPUカーネルの実装ではなく、既存研究が異なる条件で報告してきた改善率を解釈するための分析枠組みを作る。例えばLlama-3-70BをBF16で扱う場合、重みは約140GB、1系列128kトークンのKVは約42GBである。

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

- **2026-09 · [Preserving Provenance in Shared KV Caches for LLM Serving](2026-2609.38706-preserving-provenance-in-shared-kv-caches-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テナント分離用のソルトを共有鍵に含めない条件では、応答時間から被害者のプロンプトを93%の正確さで識別できた。

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

- **2026-09 · [MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators](2026-2609.19207-meshkv-a-network-on-chip-kv-cache-fabric-for-scalable-transformer-decoding-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  鍵値キャッシュをオンチップ網の分散流へ変換し、8×8 FPGA実装で通信量最大58%削減、鍵値帯域利用率2.1倍、生成処理量最大1.90倍を実測する。

- **2026-09 · [KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints](2026-2609.10266-kvsharearena-cross-context-checkpoint-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVShareArenaは、文脈・チェックポイントをまたぐKV再利用で位置ずれと情報源間相互作用の欠落を分離測定し、補正・再計算・圧縮の品質と費用を共通基準で比較する。

- **2026-09 · [KVCMAS: Efficient KV cache Correction for Shared Context in Multi-Agent Systems](2026-2609.34060-kvcmas-efficient-kv-cache-correction-for-shared-context-in-multi-agent-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  完全に再計算すると入力処理が何度も必要になる。一方、先行エージェントのキャッシュを無修正で使うと、注意機構が本来と異なる内部状態を参照して回答品質が大きく落ちる。著者のvLLM実装によるA100 80GBの同時要求試験では、共有文脈32Kトークン、毎秒8要求、キャッシュ再利用率約0.8で、初回トークン待ち時間（TTFT）の中央値が61.95秒であった。

- **2026-09 · [KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation](2026-2609.24298-kv-cobra-kv-cache-compression-via-co-optimized-bit-rank-allocation.md)**  
  実装：[✓](https://github.com/seonha01/KV-COBRA) ・ リポジトリ内被引用：0  
  各トークンのKV値を保持したまま圧縮する方式では、低ランク射影で次元数を減らし、残った座標を量子化することが多い。注意演算単体は特定条件で全精度実装比1.79〜1.89倍高速だが、推論サーバ全体の処理量やP99遅延を測定した結果ではない。

- **2026-09 · [Jacap: Robust KV Cache Eviction via Jacobian-Based Nonlinear Information Capacity Preservation](2026-2609.08131-jacap.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jacapは、将来クエリへの注意出力感度と値方向の重複を測り、重要度だけでなく情報の多様性を持つKV集合を選んで、高圧縮時の出力情報欠落を減らす。

- **2026-09 · [HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrid Long-Context Language Models](2026-2609.02029-headwisekv-budgeted-per-head-cache-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeadWiseKVは、全体注意層のKV履歴を物理KVヘッドごとに較正し、必要な窓だけGPUへ確保して、長文脈の過剰メモリと一律圧縮による品質低下を抑える。

- **2026-09 · [HeadGuard: Selective Head Protection for Low-Bit VLM KV-Cache Quantization](2026-2609.35800-headguard-selective-head-protection-for-low-bit-vlm-kv-cache-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キャッシュを一様に2～3ビットへ量子化すると容量は小さくなるが、視覚情報に強く依存するヘッドの表現まで丸められ、画像質問応答や選択問題の正答率が急落する場合がある。

- **2026-09 · [H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache](2026-2609.24197-h-spec-parallel-speculative-decoding-without-a-drafter-side-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H-Specは、投機的復号（投機的復号）の軽量な候補生成器であるドラフターが、対象モデルの隠れ状態を各入力位置で別の鍵・値キャッシュ（KV キャッシュ）へ射影して保存する方式に対し、その追加キャッシュを廃止するための混成Mamba・注意ドラフターである。

- **2026-09 · [GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving](2026-2609.03494-growpage-on-demand-kv-budgeting-for-efficient-llm-reasoning-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GrowPageは、生成中の注意参照範囲を短期・長期信号で予測し、容量境界で圧縮継続かKVページ追加かを選んで、推論ごとの過剰予約と必要履歴の削除を抑える。

- **2026-09 · [Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction](2026-2609.13285-grouped-value-attention-efficient-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  値だけをKVキャッシュへ保存し、内容キーを値から再構成してクエリ側へ吸収することで、GQAに近い精度を保ちながら永続キャッシュを約45〜47%削減する注意機構。

- **2026-09 · [Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs](2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Flash-dLLM) ・ リポジトリ内被引用：0  
  拡散言語モデルの鍵・値キャッシュ更新を融合注意へ統合し、同じモデルによる下書き・検証型並列復号を重ねることで、メモリ入出力と反復回数を同時に削減する。

- **2026-09 · [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](2026-2609.09768-kv-concatenation-aware-recompute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV連結対応学習とCacheBlendの選択的再計算を組み合わせ、文書間相互作用の欠落を15%再計算で補い、RAG長文の品質とSSD読出し・転送待ちを両立する。

- **2026-09 · [Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches](2026-2609.17652-fathom-per-query-read-depth-offloaded-kv-cache.md)**  
  実装：[✓](https://github.com/vivekkalyanarangan30/fathom) ・ リポジトリ内被引用：0  
  問い合わせごとに鍵チャネルの読取深度を変え、ホスト退避した疎注意索引の転送量を減らして百万トークン復号を最大一・六七倍高速化する。

- **2026-09 · [ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics](2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コサイン類似度だけでは見落とすKV表現の大きさをユークリッド距離で補い、注意ヘッドごとの冗長度に応じて多様性と重要度を混合し、狭いKV予算で保持トークンを改善する方式。

- **2026-09 · [Dynamic Flow, Static Graph: KV Cache Reuse for Efficient LLM Serving on Mobile NPUs](2026-2609.34727-dynamic-flow-static-graph-kv-cache-reuse-for-efficient-llm-serving-on-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、固定形状の計算グラフ内で必要なトークンだけ再計算する方式、複数グラフ呼出しを統合する動的計画法、NPU・CPUメモリ・フラッシュにまたがる階層KV保存、読み込み・位置補正・保存とNPU実行の非同期重畳を組み合わせる。

- **2026-09 · [Divergence Timing and Cumulative Disagreement under KV-Cache Eviction](2026-2609.16617-divergence-timing-and-cumulative-disagreement-under-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文はKVキャッシュ削除の新しい実装を提案するのではなく、削除したときに生成結果がどのように参照モデルから離れていくかを測る理論と実験を提示する。Llama-3.1-8B-InstructとQwen2.5-7B-Instructで、SnapKVによる50%保持は同予算の直近トークン保持やSnapKV-512より遅く・少なく分岐した。

- **2026-09 · [D-Quant: Driftable Entropy Coding for KV Cache Quantization](2026-2609.19880-d-quant-driftable-entropy-coding-for-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定サイズ容器と長さ制約付きドリフトを組み合わせ、エントロピー符号化KVキャッシュを注意カーネル内で直接並列復号できる形にした低ビット量子化方式。

- **2026-09 · [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits](2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文書編集で古くなったKVは重要位置の散発再計算より編集直後を連続再計算する方が有効で、隣接依存なら13〜21倍高速にほぼ完全修復する。

- **2026-09 · [Compressing Long Context into Answer-Aligned Memory Embeddings for LLM Inference](2026-2609.25537-cmc.md)**  
  実装：[✓](https://github.com/mostafiz26/CMC) ・ リポジトリ内被引用：0  
  CMC（Context-to-Answer-Aligned メモリ Compression）は、長文を少数の連続的な文脈記憶埋め込み（Context メモリ Embeddings、CME）へ変換し、質問に関連する記憶と原文の局所窓を組み合わせて凍結したデコーダへ渡す方式である。

- **2026-09 · [CacheRepair: Learning to Repair Cross-Chunk Context in RAG for KV Cache Fusion](2026-2609.35139-cacherepair-learning-to-repair-cross-chunk-context-in-rag-for-kv-cache-f.md)**  
  実装：[✓](https://github.com/genglinWang/CacheRepair-code) ・ リポジトリ内被引用：0  
  CacheRepairは、複数の検索文書を使うRetrieval-Augmented Generation（RAG）で、文書ごとに独立に計算したKVキャッシュを再利用するときの品質劣化を、軽量な修復ネットワークで補う方式である。

- **2026-09 · [Beyond Mean Attention: Diversity-Aware, Layer-Wise Scoring for KV Cache Eviction](2026-2609.30738-beyond-mean-attention-diversity-aware-layer-wise-scoring-for-kv-cache-ev.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特に文章中の指定箇所を探すpassage-retrievalでは、層の途中から冗長性の係数を負から正へ切り替える設定で60.60から70.17へ上昇した。

- **2026-09 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](2026-2609.04971-beaconkv.md)**  
  実装：[✓](https://github.com/aiha-lab/BeaconKV) ・ リポジトリ内被引用：0  
  長い推論で過去の計画へ再注意する問い合わせを少数のビーコンとして保持し、将来再参照されるKVを予測して残す訓練不要の圧縮方式。

- **2026-09 · [ARM: Attention with Routed-Memory for Learnable Sparse Control](2026-2609.24417-arm-attention-routed-memory-learnable-sparse-control.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  増え続けるKVキャッシュを固定数256スロットの階層メモリへ置き換え、書込み先と混合率、さらに読み出すメモリ量まで学習する。Llama-3.1-8Bで128Kまで動作し、RULER平均15.12を報告する。

- **2026-09 · [ActKV: Efficient LLM Agents through Action-Guided KV Cache Management](2026-2609.31395-actkv-efficient-llm-agents-through-action-guided-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行動生成時の注意履歴で将来の操作に必要なキー・値状態を選び、生成確信度に応じて保存枠を拡張し、ページ化された実キャッシュを追加作業領域なしで圧縮する。ReAct型の長期タスクでは、無圧縮方式に対する平均タスク精度98.53%を、ピークKV容量25.98%で維持する。

- **2026-08 · [WnW: Waxing-and-Waning KV Cache for Long-Form Speech LLMs](2026-2608.22704-wnw-waxing-and-waning-kv-cache-for-long-form-speech-llms.md)**  
  実装：[✓](https://github.com/XMUDeepLIT/WnW) ・ リポジトリ内被引用：0  
  従来のKV圧縮は、プリフィル時の注意スコアで重要な音声位置を選び、残りを削除したままデコードを続ける。Voxtral-mini-3bのLibriSpeech-LongでGPU上の音声KV保持率が約22%のとき、WnWのWERはtest-clean 6.23、test-other 8.87で、無圧縮の6.79、8.86に近い。

- **2026-08 · [VisCache: Visual KV Cache Pruning for Efficient Vision Large Language Model Inference](2026-2608.24063-viscache-visual-kv-cache-pruning-for-efficient-vision-large-language-mod.md)**  
  実装：[✓](https://github.com/Wlklk/VisCache) ・ リポジトリ内被引用：0  
  前段で質問に関係する多様なフレームを残し、後段で層ごとの重要度と鍵・値の役割の違いを利用して圧縮する。論文の試作では、Qwen2.5-VLの3Bと32Bを使い、視覚KVの保持率28%で複数の動画理解課題の平均精度を比較方式より高く保ち、保持率19%でも大きく破綻しない結果を示す。

- **2026-08 · [Strong Drafts Need Compact Memories: Long-Context Speculative Decoding with Compressed KV Cache](2026-2608.30252-strong-drafts-need-compact-memories-long-context-speculative-decoding-wi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案するメモリ拡張スライディング窓（メモリ-Augmented Sliding Window、MASW）は、強い独立下書き器のKVメモリを、先頭の注意シンク、直近の正確なKV、過去を圧縮した学習可能なメモリスロットに分ける。

- **2026-08 · [Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction](2026-2608.23296-sigmoid-attention-as-a-better-substrate-for-learned-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/IsaacLi74/sigmoid-kv-eviction) ・ リポジトリ内被引用：0  
  本研究は、学習時に連続値で表現したトークン保持ゲートを、推論時に鍵・値キャッシュ（Key-Value Cache、KVキャッシュ）の実際の削除へ変換するとき、注意重みの正規化方式が結果を左右することを示す。

- **2026-08 · [SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference](2026-2608.28911-semkv-semantic-mixed-precision-kv-cache-quantization-guided-by-the-quali.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重要度の低いトークンを消す方式も、長文脈の回答に必要な証拠を失う恐れがある。SemKVは境界より安全側の2.322ビットと2.585ビットをトークンごとに混ぜ、平均2.39コードビット、充填とメタデータを含む実効2.65ビットで、FP16比6.0倍のKV保存量削減を実測した。

- **2026-08 · [RippleKV: Cross-Layer KV Cache Allocation via Perturbation Propagation](2026-2608.08684-ripplekv-cross-layer-kv-cache-allocation-via-perturbation-propagation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈長が長くなるほどKVキャッシュは大きくなり、GPUメモリを占有するだけでなく、生成時に参照するメモリ量も増える。一方で同じ数を全層に配れば、生成結果を強く左右する層が過度に圧縮され、圧縮に強い層にメモリが余る可能性がある。

- **2026-08 · [PuzzleKV: Page-Wise Low-Rank Decomposition for KV Cache Compression](2026-2608.23843-puzzlekv-page-wise-low-rank-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PagedAttentionの固定長ページごとにKVを独立低ランク分解し、密ページと因子化ページを復元なしで同時に注意計算することで、学習不要のままKV容量を約60%へ削減する。

- **2026-08 · [Practical Online KV Cache Compaction for LLM Agents: An Empirical Study](2026-2608.00902-practical-online-kv-cache-compaction-for-llm-agents-an-empirical-study.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的な長文質問では、最終質問を見た後で不要トークンを選別できるが、エージェントがまだ次に何を調べるか分からない時点で圧縮すると、後で必要になる検索結果を失い得る。大規模モデルQwen3.5-27BのBrowseComp-Plusでは、無圧縮の正答率52.50%に対し、1ターン遅延のTEが52.00%、AMが51.00%だった。

- **2026-08 · [PatchKV: Efficient KV Cache Recovery for Dynamically Edited LLM Contexts](2026-2609.26219-patchkv-efficient-kv-cache-recovery-for-dynamically-edited-llm-contexts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純な接頭辞キャッシュでは最初の不一致以降を全再計算し、無条件再利用では古い因果状態を持ち込むという二者択一になる。編集位置からの距離に基づく局所的な修復範囲、過去に収集した注意重みから見つける遠方の重要ブロック、保存時に決めたブロック別の量子化精度を組み合わせる。

- **2026-08 · [Parser Transitions Already Reveal Structural Responsibility: KV Persistence for Structured Generation](2026-2608.28276-parser-transitions-already-reveal-structural-responsibility-kv-persisten.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMエージェントが関数呼出し、JSON、SQLなどの構造化出力を生成する時、制約付きデコーダはパーサ状態を管理し、文法的に合法な次トークンだけを許可する。KVキャッシュを圧縮すると、注意スコア上は重要に見えないが構造上の役割を持つトークンの履歴が失われ、合法だが誤った出力になる可能性がある。

- **2026-08 · [PAGE: Partition-Aware Gated KV-Cache Eviction](2026-2609.22157-page-partition-aware-gated-kv-cache-eviction.md)**  
  実装：[✓](https://github.com/pankajkumar6002/PAGE) ・ リポジトリ内被引用：0  
  値が大きければ注意希釈型と見なして既存の退避器を起動し、小さければ容量律速型と見なして全キャッシュを保持する。Mistral-7Bの精密な複数鍵検索では、通常のSnapKVの正答率が99%から0%へ崩れる保持予算でも、PAGEを併用すると89%を保った。

- **2026-08 · [Output-Aware Rotation for INT2 KV-Cache Quantization](2026-2608.02691-output-aware-rotation-int2-kv-cache.md)**  
  実装：[✓](https://github.com/daniel-eai/Output-Aware-INT2-KV-Cache-Quantization) ・ リポジトリ内被引用：0  
  OptRは、長文脈推論でKVキャッシュを2ビット整数へ量子化したとき、キーや値そのものの再構成誤差が小さくても、注意重みと出力射影を通過した後のモデル内部表現には大きな誤差が残り得る問題を扱う。

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

- **2026-08 · [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](2026-2608.02515-livemem-maintaining-memory-state-continuity-in-long-running-llm-inferenc.md)**  
  実装：[✓](https://github.com/cafeii/LiveMem) ・ リポジトリ内被引用：0  
  長時間稼働する対話支援や自律エージェントでは、対話履歴がモデルの注意機構（注意機構）の文脈窓を超える。Qwen3-4Bを基盤とする制限文脈の実験では、教師あり微調整と強化学習を経たLiveMemの全課題総合スコアが0.519で、基盤モデルの0.458を上回る。

- **2026-08 · [KVDiagnosis: A Diagnostic Benchmark for KV-Cache Compression in Long-Context Language Models](2026-2608.09412-kvdiagnosis-a-diagnostic-benchmark-for-kv-cache-compression-in-long-cont.md)**  
  実装：[✓](https://github.com/ChosenQC/KVDiagnosis) ・ リポジトリ内被引用：0  
  長文脈LLMの鍵・値キャッシュ（KVキャッシュ）を圧縮する研究では、通常、圧縮後の平均正答率と保存容量が比較される。うち7,913行（63.2%）は証拠位置の測定・投影被覆が低いか部分的であった。

- **2026-08 · [KV Cache Compression Through the Lens of Transform Coding](2026-2608.14191-kv-cache-compression-through-the-lens-of-transform-coding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  保存精度を下げれば容量を削減できるが、鍵と値の数値的な再構成誤差が小さいことと、注意機構の出力が変化しないことは同義ではない。約5.82倍の鍵値キャッシュ圧縮時に、原著の標準誤差による判定では、両モデルの主要18評価セルすべてで非圧縮基準との統計的な区別がつかないと報告する。

- **2026-08 · [ImpactHO: Importance-Aware KV Cache Transfer for Multi-User Edge LLM Handover](2026-2608.10545-impactho-importance-aware-kv-cache-transfer-for-multi-user-edge-llm-hand.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  元の入力文字列だけを送れば転送量は小さいが、移動先で全履歴を再度事前処理しなければならない。一方、KVキャッシュを丸ごと転送すると再計算は避けられるが、複数利用者の移動が重なるとノード間回線が詰まる。転送が途中で切れても、届いた上位要素を使って推論を再開できる「途中再開可能性」が中心的な設計である。

- **2026-08 · [Entropy-Constrained Adaptive Stochastic Quantization](2026-2608.18147-entropy-constrained-adaptive-stochastic-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  listsummary と同じ一覧専用解説。ECASQは値ごとに適応する不偏確率量子化で、誤差と後段のエントロピー符号化後の平均ビット量を共同最適化する。実モデルのKVテンソルでも比較し、近似法は厳密法に近い誤差を保ちながら解法処理を高速化する。

- **2026-08 · [DualPath: Accelerating Agentic LLM Inference by Harvesting Disaggregated KV-Cache Storage I/O](2026-3f706ddceb51-dualpath-accelerating-agentic-llm-inference-by-harvesting-disaggregated-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の入力処理・復号分離（プリフィル–デコード disaggregation）では、過去のKVキャッシュを入力処理エンジン（プリフィル engine; PE）がストレージから読み、計算後に復号エンジン（デコード engine; DE）へ転送する。

- **2026-08 · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](2026-2608.08878-distillcache-kl-guided-adaptive-kv-cache-eviction-for-memory-efficient-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著表1によると、Mistral-7B-Instruct-v0.3のLongBenchで完全キャッシュ41.5に対して、25%予算の提案法は39.1±1.1（完全版の94.2%）を得る。

- **2026-08 · [DASC: Decay-Aware State Compression for Hybrid Linear-Attention Serving](2026-2608.30386-dasc-decay-aware-state-compression-for-hybrid-linear-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み由来の保持地平でKDA/GDN再帰状態を選別・ragged保存し、TP均衡化によりKimi-KDAで2.63倍のcheckpoint容量とTTFT 42.6%削減を実現する。

- **2026-08 · [CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG](2026-2608.07458-coinrag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongBenchのHotpotQA、2WikiMQA、MuSiQueを対象に、初回トークン時間（Time to First Token、TTFT）の99パーセンタイルを100ミリ秒以内に制限した条件で、最良比較方式TurboRAGの3課題平均F1=39.6に対して41.7を報告する。

- **2026-08 · [Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects](2026-2608.30076-budget-aware-compression-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み量子化・層削減・鍵値キャッシュ圧縮の相互作用を三予算で評価し、七百億モデルを約三十三ギガバイトへ縮小して単一A40・一万トークン入力で約五十七トークン毎秒を実現する。

- **2026-08 · [A Probabilistic Interpretation of KV Cache Eviction](2026-2608.28293-a-probabilistic-interpretation-of-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV追放を期待値推定として定式化し、確率的追放＋復号時重要度補正で既存top-kのバイアスを抑えタスク間頑健性を高める。

- **2026-07 · [When Efficiency Meets Safety: A Benchmark Security Analysis of KV Cache Compression in Large Language Models](2026-2deb03505de5-when-efficiency-meets-safety-a-benchmark-security-analysis-of-kv-cache-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈推論では、過去の鍵・値（key-value; KV）をキャッシュすることで各生成ステップの再計算を減らすが、保存するトークンが増えるとGPUメモリ容量と帯域を圧迫する。反対に、CAMのような統合では浅い層の過度な値の重畳が深い層の注意を乱し、LLaMA-2の文脈内攻撃でASRが非圧縮0%から34%へ上がった。

- **2026-07 · [VarRate: Training-Free Variable-Rate KV Cache Compression for Long-Context LLMs](2026-2607.15498-varrate-training-free-variable-rate-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを削除せず、注意顕著度に応じて各トークンの低ランク表現へ可変容量を配る学習不要KV圧縮で、20%メモリ予算でもLongBench平均を非圧縮から0.8点以内に保ち、再利用時の不可逆削除崩壊を抑える。

- **2026-07 · [Set Diffusion: Interpolating Token Orderings Between Autoregression and Diffusion for Fast and Flexible Decoding](2026-2607.01775-set-diffusion-interpolating-token-orderings-between-autoregression-and-d.md)**  
  実装：[✓](https://github.com/kuleshov-group/setdlms) ・ リポジトリ内被引用：0  
  マスクを復元する拡散モデルは多数の位置を並列に予測できるが、双方向の注意と固定長の生成領域を前提とするため、復号中に一部だけを確定して計算結果を長期再利用する設計が難しい。

- **2026-07 · [SelKV: Selective KV Cache Merging with Per-Token Merge-or-Drop and Attention Compensation](2026-2607.16213-selkv-selective-kv-cache-merging-with-per-token-merge-or-drop-and-attent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純なKV削除は必要な情報を失う一方、削除対象を保持KVへ一律に統合する方式では、似ていない値ベクトルまで混ざり、重要な表現を壊す場合がある。

- **2026-07 · [ReFreeKV: Towards Threshold-Free KV Cache Compression](2026-2502.16886-refreekv-towards-threshold-free-kv-cache-compression.md)**  
  実装：[✓](https://github.com/Patrick-Ni/ReFreeKV) ・ リポジトリ内被引用：0  
  長い入力を処理したLLMは、デコード中に過去のトークンへ注意するため、各層のKeyとValueをKVキャッシュとして保持する。H2O、SnapKV、StreamingLLMなどは重要とみなした位置だけを残すが、通常は「入力の何%を保持するか」または「何トークン残すか」を先に決める。ReFreeKVは、保持率ではなく注意行列のノルム変化を停止条件にする。

- **2026-07 · [Question Tells You Where the Answer Is: Intention-aware Long-Context KV Cache Compression](2026-3562943b0724-question-tells-you-where-the-answer-is-intention-aware-long-context-kv-c.md)**  
  実装：[✓](https://github.com/linkezh/IntentKV) ・ リポジトリ内被引用：0  
  IntentKVは、長文脈推論のプリフィル段階で作られたKey/Value（KV）を、後続の生成にとって重要な文脈に絞って保持する方式である。128K入力・保持容量2048の効率評価では、復号遅延はFullKVの16%、KVキャッシュメモリは13%と報告する。

- **2026-07 · [LOCKS: Page-Local Compact Key Summaries for Efficient Long-Context Decoding](2026-2607.24555-locks.md)**  
  実装：[✓](https://github.com/Js-Hwang1/locks) ・ リポジトリ内被引用：0  
  長文脈LLMでは復号のたびに過去トークンの鍵・値（KV）を読み、問い合わせと照合する。短文脈で小さなバッチならモデル重みの読出しが支配的だが、長文脈かつ複数要求では要求ごとのKV読出しが帯域を圧迫する。例えばLlama-3.1-8Bの128K文脈はbf16のKVだけで要求あたり約16GiBとなる。本方式はKVキャッシュの削除や容量圧縮ではない。

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

- **2026-07 · [GSRQ: Gain–Shape Residual Quantization for Sub-1-bit KV Cache](2026-2607.01065-gsrq-gain-shape-residual-quantization-for-sub-1-bit-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の残差ベクトル量子化（Residual Quantization; RQ）は、小さなコードブックで近似した誤差を次段のコードブックで繰り返し近似する。別途、独自PyTorch/Triton実装の単一A100 80GBにおけるデコード測定では、8K文脈で1.59倍、64Kで3.40倍のトークン当たり遅延短縮を報告する。

- **2026-07 · [FreqDepthKV: Frequency-Guided Depth Sharing for Robust KV Cache Compression in Long-Context LLM Inference](2026-2607.06519-freqdepthkv-frequency-guided-depth-sharing-for-robust-kv-cache-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FreqDepthKVは、長文脈LLMのKVキャッシュをトークン方向だけでなく層の深さ方向にも圧縮する推論時手法である。Peak KV メモリは24.0GBから6.2GB、デコード スループットは38.2から70.4 トークン/sとなる。

- **2026-07 · [DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation](2026-2607.24331-dynacalkv-key-value-cache-compression-via-head-grouping-and-adaptive-rank-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー投影の注意ヘッドをCKA類似度で動的に群分けし、群ごとの情報量に応じて低ランク次元を配分することでReCalKVよりキー側パラメータを減らすが、GQAの長文脈では精度低下も確認する。

- **2026-07 · [DepthWeave-KV: Token-Adaptive Cross-Layer Residual Factorization for Long-Context KV Cache Compression](2026-2607.06523-depthweave-kv-token-adaptive-cross-layer-residual-factorization-for-long.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DepthWeave-KVは、長文脈TransformerのKVキャッシュを、隣接する層間の冗長性とトークンごとの重要度の違いを同時に利用して圧縮する手法である。

- **2026-07 · [Compress the Cache, Not the Speech Embedding: KV Compression for Efficient Speech LLMs](2026-2607.06827-compress-the-cache-not-the-speech-embedding-kv-compression-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の音声アダプタによる早期間引きはこの問題を解消するが、LLMが音声とテキストを統合する前に細かな音響情報を失うおそれがある。実験では、社内固有表現認識の誤り率が14.41から13.46、OpenASRの平均単語誤り率が6.12から5.98へ改善し、A100 80GBとvLLMの復号速度は30秒音声で1.49倍、10分音声で2.02倍となった。

- **2026-07 · [Codec-Gauge: Learning Compression-Friendly Gauges for Transformer KV Caches](2026-2607.20538-codec-gauge-learning-compression-friendly-gauges-for-transformer-kv-cach.md)**  
  実装：[✓](https://huggingface.co/cccat6/Codec-Gauge) ・ リポジトリ内被引用：0  
  要求数、文脈長、層数、KVヘッド数に比例してキャッシュが増えるため、低ビット量子化や数値圧縮を行ってGPUメモリの使用量と転送量を抑える。

- **2026-06 · [Unified KV Pooling to Accelerate Long-Context LLM Serving](2026-2606.14779-unified-kv-pooling-to-accelerate-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数RAM/SSDを帯域幅比例の単一KVプールとして並列利用し、SPDK直アクセスでファイルシステムを迂回して長文脈KV再取得を高速化する。

- **2026-06 · [Rethinking LoRA Memory Through the Lens of KV Cache Compression](2026-2606.05698-rethinking-lora-memory-through-the-lens-of-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索拡張生成では、回答に必要な文書をプロンプトへ入れると、文書内容が鍵・値キャッシュ（KVキャッシュ）へ保存され、回答中に参照される。さらにLoRAを文書の事前処理（プリフィル）、KV圧縮の重要度採点、回答復号のどの段階で有効にするかを分けた。

- **2026-06 · [Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers](2026-2144aa87ce08-reimagining-llm-inference-infrastructure-with-memory-centric-kv-cache-se.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、GPUを計算能力の大きさで増設する従来のLLMデータセンター設計が、長文脈・長い推論出力・複数エージェント間の接頭辞共有という負荷に必ずしも合致しないと論じる。

- **2026-06 · [HybridThinker: Efficient Chain-of-Thought Reasoning via Compressed Memory and Transient Thought Steps](2026-2606.03768-hybridthinker-efficient-chain-of-thought-reasoning-via-compressed-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LightThinkerのような方式は、各思考段階を少数の記憶トークンへ圧縮して、元の思考トークンのKVを即座に削除する。

- **2026-06 · [High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration](2026-2607.16248-high-accuracy-low-bit-kv-cache-quantization-via-local-distribution-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  1ビットKVキャッシュを維持したまま、量子化で崩れた高確率候補の局所順位だけを検出・補正し、RULER精度を47.8%から83.2%へ回復するDGAP。

- **2026-06 · [Affix Cache for Diffusion Large Language Models](2026-2608.26140-affix-cache-for-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/sands-lab/ACache) ・ リポジトリ内被引用：0  
  ACache（Affix Cache）は、拡散型大規模言語モデル（Diffusion Large Language モデル; DLLM）において、複数の生成要求が同じ文脈を共有する際に、共有文脈の鍵・値キャッシュ（KV キャッシュ）を一度だけ保存し、要求ごとに必要な一部だけを再計算する推論基盤である。

- **2026-05 · [WindowQuant: Mixed-Precision KV Cache Quantization based on Window-Level Similarity for VLMs Inference Optimization](2026-2605.02262-windowquant-mixed-precision-kv-cache-quantization-based-on-window-level-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の量子化方式では全トークンを同じ低ビットへ変換すると品質が落ちやすく、重要度によってトークンごとにビット幅を変えると探索や計算の費用が大きくなる。

- **2026-05 · [Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles](2026-2605.19775-understanding-inference-scaling-for-llms-bottlenecks-trade-offs-and-perf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は新しい推論アルゴリズムを提案するものではなく、8Bから671Bパラメータまでの密なモデルと混合専門家モデルを、8基のNVIDIA H200を持つ実機で比較した性能特性研究である。

- **2026-05 · [SemanticKV: A Semantics-Driven KV Cache Eviction Framework for Efficient Long Prompt LLM Inference](2026-41074c82c154-semantickv-a-semantics-driven-kv-cache-eviction-framework-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SemanticKVは、長い入力プロンプトを処理するプリフィル段階で、後続の生成に必要なKVキャッシュだけを残す方式である。著者らは、元のKVキャッシュの20%だけを残す条件で、Llama3.1-8B-InstructのInfiniteBench長文脈タスクを評価した。

- **2026-05 · [Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models](2026-2605.09630-scratchpad-patching-decoupling-compute-from-patch-size-in-byte-level-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この「パッチ遅延（patch lag）」が、大きなパッチの精度劣化を招く。したがって、パッチ長が決めるKVキャッシュ圧縮率と、内部で追加実行する計算回数を別々に調整できる。約20億パラメータの実験で、固定16バイト/パッチの自然言語理解平均精度はSPなし48.0からSPあり54.2へ改善し、バイト単位基準の主幹系列短縮16倍を維持する。

- **2026-05 · [Rotation-Aligned Key Channel Pruning for Efficient Vision-Language Model Inference](2026-2605.19218-rotation-aligned-key-channel-pruning-for-efficient-vision-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来は重要度の低い視覚トークンを丸ごと削除する方式が多いが、文書の小さな文字や画像全体に散らばる情報を必要とする質問では、削除した位置の証拠を復元できない。

- **2026-05 · [QKVShare: Quantized KV-Cache Handoff for Multi-Agent On-Device LLMs](2026-2605.03884-qkvshare-quantized-kv-cache-handoff-for-multi-agent-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  送信側が既に計算した注意機構の鍵・値キャッシュ（KVキャッシュ）を、受信側がテキストから再計算する再事前充填（re-プリフィル）は無駄が大きい。

- **2026-05 · [Polynomial Context-Truncation Sensitivity in Autoregressive Language Models: Sequential Wyner-Ziv Bounds for KV Cache Compression](2026-2605.25085-polynomial-context-truncation-sensitivity-in-autoregressive-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  逐次Wyner–Ziv符号化としてKVキャッシュ圧縮を定式化し、末尾窓だけを保持する方式の必要窓長が、追加の両側リスク条件下で許容分布誤差εに対してΘ(ε^{-1/α})となることを示す。

- **2026-05 · [NIKA: Optimal KV Cache Transfer for Minimizing the Latency of Disaggregated LLM Inference](2026-96229b44d7f2-nika-optimal-kv-cache-transfer-for-minimizing-the-latency-of-disaggregat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NIKAが対象とするのは、入力プロンプトを一括処理する事前入力（プリフィル）と、出力トークンを逐次生成する復号（デコード）を別のGPUへ割り当てる分離型推論である。CLOSER 2026の8ページ論文では、vLLM 0.8.4の分離型構成を改造し、全KV転送の基準方式に対してTTFT最大54%減を報告した。

- **2026-05 · [NestedKV: Nested Memory Routing for Long-Context KV Cache Compression](2026-2605.26678-nestedkv-nested-memory-routing-for-long-context-kv-cache-compression.md)**  
  実装：[✓](https://github.com/ChenHong30/NestedKV) ・ リポジトリ内被引用：0  
  学習不要のKV圧縮では、注意重みが大きいトークン、最近のトークン、鍵ベクトルが平均から離れたトークンなどを残す方法が使われる。Qwen3-4B、RULERの4,000トークン文脈、KVの75%を削除する条件でNestedKVは79.32点、単一の全文平均方向を使うKeyDiffは60.22点だった。

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

- **2026-05 · [KV-Fold: One-Step KV-Cache Recurrence for Long-Context Inference](2026-2605.12471-kv-fold-one-step-kv-cache-recurrence-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い入力を一度に処理する大規模言語モデル（LLM）の事前処理では、全トークンに対する注意演算と、各層の鍵・値キャッシュ（KV キャッシュ）を保持するための記憶容量が問題になる。新しい注意カーネルや学習済み圧縮器の提案ではなく、既存Transformerの推論操作に対する実証的な分析が中心となる。

- **2026-05 · [Hurwitz Quaternion Multiplicative Quantization for KV Cache Compression](2026-2605.27646-hurwitz-quaternion-multiplicative-quantization-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の半精度浮動小数点（FP16）で保存すると、文脈長に比例してKVのメモリ占有量が増える。ノルムである半径は別に量子化する。これに、チャンクの半径が同一集団の中央値の3倍を超えたときだけFP16で保存する外れ値退避（Med3×）を組み合わせる。

- **2026-05 · [HeadQ: Model-Visible Distortion and Score-Space Correction for KV-Cache Quantization](2026-2605.03562-headq-model-visible-distortion-and-score-space-correction-for-kv-cache-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  保存精度を下げれば容量と読み出し帯域を削減できるが、単純に保存値の平均二乗誤差が小さい量子化方式を選んでも、生成品質が良いとは限らない。

- **2026-05 · [FastOCR: Dynamic Visual Fixation via KV Cache Pruning for Efficient Document Parsing](2026-2605.17447-fastocr-dynamic-visual-fixation-via-kv-cache-pruning-for-efficient-docum.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FastOCRは追加学習不要で、焦点層誘導型の枝刈り（Focal-Guided Pruning、FGP）とステップ間注視再利用（Cross-Step Fixation Reuse、CSFR）を組み合わせる。Qwen2.5-VLでは画像トークンの保持率5%でOmniDocBench総合スコア72.76から71.34（98.0%保持）となる。

- **2026-05 · [Discovering KV Cache Eviction Policies via LLM-Guided Program Evolution](2026-2608.14555-discovering-kv-cache-eviction-policies-via-llm-guided-program-evolution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が扱うのは、長い入力文を処理した直後に、後続の生成に必要な鍵・値キャッシュ（Key-Value Cache、以下KVキャッシュ）のどの位置を残すかという選択問題である。キャッシュを圧縮すると生成中のメモリ使用量は減るが、削除した位置へ再び注意を向けられなくなるため、根拠検索や長文理解の精度が低下する。

- **2026-05 · [Context Memorization for Efficient Long Context Generation](2026-2605.18226-context-memorization-for-efficient-long-context-generation.md)**  
  実装：[✓](https://github.com/yasu0001/AttentionMemory) ・ リポジトリ内被引用：0  
  著者らは注意状態メモリ（注意機構-state メモリ; ASM）を提案する。LLaMA 3.1-8Bを使うManyICLBenchの主要5課題では、同等のメモリ予算で1K〜8K項目の平均精度が文脈内学習基準と同等以上になり、8K予算では注意演算の遅延を1.36倍改善したと報告する。

- **2026-05 · [Benchmarking KV-Cache Optimizations across Task Quality and System Performance for Long-Context Serving](2026-2607.05399-benchmarking-kv-cache-optimizations-across-task-quality-and-system-perfo.md)**  
  実装：[✓](https://github.com/nikagrwal/Benchmarking-KV-Cache-Optimizations-across-Task-Quality-and-System-Performance) ・ リポジトリ内被引用：0  
  本研究の目的は、鍵・値キャッシュ（Key–Value キャッシュ; KVキャッシュ）の削減率だけで方式を選んだときに、実際の長文脈推論が速くなるとは限らないという問題を、同じモデル・負荷・測定指標のもとで検証することである。A100 40GBの単一GPU評価では、KIVI4が比較的安定した品質を示し、SnapKVは高い復号処理量を維持した。

- **2026-04 · [Sequential KV Cache Compression via Probabilistic Language Tries: Beyond the Per-Vector Shannon Limit](2026-2604.15356-sequential-kv-cache-compression-via-probabilistic-language-tries-beyond-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、言語モデルの鍵・値キャッシュ（KV Cache）を独立した浮動小数点ベクトルの集合として圧縮する従来の考え方を改め、元のトークン系列の確率構造に基づいてキャッシュ系列全体を圧縮する構想を示す。原著に対応するGPU実験表はなく、復号時の予測KV再計算、誤差許容、索引維持、圧縮・復元時間を含めた実用性は検証されていない。

- **2026-04 · [Probe-and-Fetch: Dynamic KV Cache Pruning for Accelerated Long-Context Inference in Web-Scale AI Search](2026-bfd3ce93bf5b-probe-and-fetch-dynamic-kv-cache-pruning-for-accelerated-long-context-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の投機的復号は軽量ドラフトが複数トークンを提案し、大型ターゲットが一度に検証する。ターゲットは転送済みの疎KVだけで候補を検証するため、転送とドラフト生成を重ね、検証のメモリ帯域を削減できる。

- **2026-04 · [MoE-nD: Per-Layer Mixture-of-Experts Routing for Multi-Axis KV Cache Compression](2026-2604.17695-moe-nd-per-layer-mixture-of-experts-routing-for-multi-axis-kv-cache-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし一つの圧縮率やビット幅を全層に一律適用すると、圧縮に弱い層まで強く削られ、圧縮に強い層に余裕を残す。非圧縮KVが1859 MB・平均11.5の条件で、提案の異種割当は136 MB・平均12.0だった。

- **2026-04 · [KV Cache Offloading for Context-Intensive Tasks](2026-2604.08426-kv-cache-offloading-for-context-intensive-tasks.md)**  
  実装：[✓](https://github.com/yandex-research/context-intensive-kv-offloading) ・ リポジトリ内被引用：0  
  文脈集約型課題でKV退避の選択誤差を分析し、低ビット量子化によるYAKVで精度とスループットを改善する。

- **2026-04 · [High Throughput and Low Latency LLM Serving via Adaptive KV Caching](2026-e8ff0256681f-high-throughput-and-low-latency-llm-serving-via-adaptive-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論のデコード（デコード）段階では、過去トークンの鍵・値（KV）キャッシュが高帯域幅メモリ（HBM）を占有する一方、演算器であるストリーミング・マルチプロセッサ（SM）は遊休しやすい。従来のvLLMの退避・再計算は、主にメモリ不足で停止した要求のKV全体を扱う。

- **2026-04 · [Graph-Guided Adaptive Channel Elimination for KV Cache Compression](2026-2604.16983-graph-guided-adaptive-channel-elimination-for-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈のLLM推論では、各層・各注意ヘッドのKeyとValueを過去トークン分保持するKVキャッシュがメモリを圧迫する。トークン単位で古いKVを捨てる方法や、低ビット化する方法とは別に、Keyベクトルのチャネル方向の冗長性を利用する圧縮がある。

- **2026-03 · [PRISM: Photonic Similarity Engine for KV Cache Block Selection in Long-Context LLM Inference](2026-2603.21576-prism-photonic-similarity-engine-for-kv-cache-block-selection-in-long-co.md)**  
  実装：[✓](https://github.com/hyoseokp/PRISM) ・ リポジトリ内被引用：0  
  PRISMは、長文脈LLMのデコード時にKVキャッシュのどのブロックを読むべきか決める候補選択段階を、薄膜ニオブ酸リチウム（TFLN）の光回路へ移す構想である。通常のブロック疎注意では、GPUが全ブロックの短い署名を読み、現在のqueryと比較して上位k個を選び、そのブロックの実際のKVを取得する。今回の読解はPDFの最新版を基準とする。

- **2026-03 · [OxyGen: Unified KV Cache Management for VLA Inference under Multi-Task Parallelism](2026-2603.14371-oxygen-unified-kv-cache-management-for-vla-inference-under-multi-task-pa.md)**  
  実装：[✓](https://github.com/air-embodied-brain/OxyGen) ・ リポジトリ内被引用：0  
  OxyGenは、この重複を「専門家間で分離されていた鍵・値キャッシュ（KV キャッシュ）の寿命と所有権」の問題と捉え、観測から得た基盤モデルのKVを共有するとともに、文章の生成状態をフレームをまたいで保存する。

- **2026-03 · [Efficient Reasoning on the Edge](2026-2603.16867-efficient-reasoning-on-the-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Efficient Reasoning on the Edge は、推論能力のあるLLMをエッジ端末へ載せる際の主な負担を、重いモデル重み、長いchain-of-thought（CoT）、不必要な推論、KVキャッシュ、並列回答の検証に分けて扱う統合研究である。

- **2026-03 · [CacheNotes: Task-Aware Key-Value Cache Compression for Reasoning-Intensive Knowledge Tasks](2026-04cca81d3e08-cachenotes-task-aware-key-value-cache-compression-for-reasoning-intensiv.md)**  
  実装：[✓](https://github.com/giulio98/cachenotes) ・ リポジトリ内被引用：0  
  コーパスに対しタスク別の圧縮計画トークン（CPTs）を生成し、CPTsからの注意を用いてコーパスKVキャッシュを一度だけ圧縮する。H100の128KコーパスでTTFT 0.13秒、RAG 0.61秒、全再入力15.88秒。

- **2026-03 · [Beyond Token Eviction: Mixed-Dimension Budget Allocation for Efficient KV Cache Compression](2026-2603.20616-beyond-token-eviction-mixed-dimension-budget-allocation-for-efficient-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixedDimKVは、長文推論の鍵・値キャッシュ（key-value キャッシュ、KVキャッシュ）を「トークンを残すか破棄するか」だけで制御する従来の方式を拡張し、各トークンに異なる保持次元数を割り当てる圧縮方式である。

- **2026-03 · [Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding](2026-2603.23914-attention-aware-inference-optimizations-large-vlm-memory-efficient-decoding.md)**  
  実装：[✓](https://github.com/git-disl/AttentionPack) ・ リポジトリ内被引用：0  
  複数ヘッドをまとめた低ランク分解で視覚言語モデルのKVを圧縮し、注意度に応じて復元精度を変えることで、動画QAのキャッシュを8.11分の1にしつつバッチ推論を60%高速化する。

- **2026-02 · [Hierarchical Adaptive Eviction for KV Cache Management in Multimodal Language Models](2026-2602.02197-hierarchical-adaptive-eviction-for-kv-cache-management-in-multimodal-lan.md)**  
  実装：[✓](https://github.com/maxindian/HAE_for_VLMs) ・ リポジトリ内被引用：0  
  視覚と言語を同じ自己注意機構で処理するマルチモーダル大規模言語モデルでは、画像から展開された視覚トークンが大量の鍵・値キャッシュ（KVキャッシュ）を消費する。

- **2026-02 · [Compiler-Assisted Speculative Sampling for Accelerated LLM Inference on Heterogeneous Edge Devices](2026-2602.08060-compiler-assisted-speculative-sampling-for-accelerated-llm-inference-on-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの逐次生成では、次のトークンを決めるたびに大型モデルを実行するため、計算資源が限られるエッジ機器では応答遅延が大きくなる。投機的サンプリングは小型草稿モデルが複数の候補トークンを先に生成し、大型検証モデルがまとめて検証することで、大型モデルの呼び出し回数を減らす。

- **2026-01 · [TableCache: Primary Foreign Key Guided KV Cache Precomputation for Low Latency Text-to-SQL](2026-2601.08743-tablecache-primary-foreign-key-guided-kv-cache-precomputation-for-low-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TableCacheは、自然言語からSQLを生成するText-to-SQLシステムで、同じデータベースの表定義を何度も長いプロンプトへ挿入するために生じるプリフィル遅延を削減する。BIRDのOmniSQL-7Bを使った追加比較では累積初回トークン待ち時間（TTFT）が291.26秒から80.53秒へ短縮し、約3.62倍の改善となる。

- **2026-01 · [PackCache: A Training-Free Acceleration Method for Unified Autoregressive Video Generation via Compact KV-Cache](2026-2601.04359-packcache-a-training-free-acceleration-method-for-unified-autoregressive.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去の鍵・値（KV）をキャッシュすれば再計算を避けられるものの、フレーム数が増えるほど保存トークンが累積し、自己注意の計算時間とGPUメモリ消費が増える。この外挿比較を「完走した二方式の実測倍率」と同一視してはならない。

- **2026-01 · [On the Limits of Learned Importance Scoring for KV Cache Compression](2026-2601.14279-on-the-limits-of-learned-importance-scoring-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/BradySteele/kv-cache-compression-limits) ・ リポジトリ内被引用：0  
  しかし、TinyLlama-1.1B-Chat-v1.0、最大2048トークンの評価では、5乱数種・4保持率・3課題のいずれでも、SIPは単純な基準方式に対する統計的に有意な優位を示さなかった。

- **2026-01 · [Multi-tier dynamic storage of KV cache for LLM inference under resource-constrained conditions](2026-e905fcb3ff0a-multi-tier-dynamic-storage-of-kv-cache-for-llm-inference-under-resource-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、複数の大規模言語モデル（LLM）要求を限られたGPUで処理するとき、過去に計算した鍵・値（KV）キャッシュをどこに保存し、いつGPUへ戻すべきかを扱う。推論の事前充填（プリフィル）段階では入力トークンから注意機構のKVを計算する。

- **2026-01 · [GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models](2026-2601.04719-gpu-accelerated-int8-quantization-for-kv-cache-compression-in-large-lang.md)**  
  実装：[✓](https://github.com/MaanasTaneja/cuda-kv-cache-compression) ・ リポジトリ内被引用：0  
  再計算を避けるため、各層・各注意ヘッドの過去の鍵と値を保持するKVキャッシュ（KV キャッシュ）が必要になる。そこで本論文は、FP32の鍵・値行列をINT8へ変換する列別量子化と、その変換処理を高速化するCUDAカーネルを実装・比較する。

- **2026-01 · [Don't be so Stief! Learning KV Cache low-rank approximation over the Stiefel manifold](2026-2601.21686-don-t-be-so-stief-learning-kv-cache-low-rank-approximation-over-the-stie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  StiefAttentionは、学習済みの大規模言語モデルを再事前学習せずに、推論時の鍵・値（KV）キャッシュを低ランク化する手法である。

- **2025-12 · [V-Rex: Real-Time Streaming Video LLM Acceleration via Dynamic KV Cache Retrieval](2025-2512.12284-v-rex-real-time-streaming-video-llm-acceleration-via-dynamic-kv-cache-re.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去の映像を後から質問される可能性があるため、不要に見えるKVを永久削除する方式は会話の整合性を損なう。論文のエッジ向けV-Rex8構成は、KV長1K〜40KのCOIN動画でフレーム当たり121〜254 ms、すなわち3.9〜8.3 FPSを報告する。

- **2025-12 · [Reconstructing KV Caches with Cross-layer Fusion For Enhanced Transformers](2025-2512.03870-reconstructing-kv-caches-with-cross-layer-fusion-for-enhanced-transforme.md)**  
  実装：[✓](https://github.com/LivingFutureLab/FusedKV) ・ リポジトリ内被引用：0  
  長い系列と同時要求の増加に伴い、層数に比例するKVキャッシュ容量と読み出しがサービングの制約となる。著者は、上位層のキーと値が異なる深さの情報を必要とすることが原因の一つと考え、上位層のキー・値を下位層から非対称に再構成するFusedKVを設計した。

- **2025-12 · [CTkvr: KV Cache Retrieval for Long-Context LLMs via Centroid then Token Indexing](2025-2512.15550-ctkvr-kv-cache-retrieval-for-long-context-llms-via-centroid-then-token-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全履歴をGPUの高帯域メモリに置くと文脈長と同時要求数に比例して容量を圧迫する。一方、CPUの主記憶へ退避すると、必要な過去トークンを効率よく特定しなければ検索と転送の費用が新たな律速になる。原著は96Kトークンの復号でLlama-3-8Bに最大3倍、Yi-9Bに最大4倍の処理量改善、GPU容量制約下で最大10倍・20倍のバッチ数を報告する。

- **2025-11 · [SWAN: Sparse Winnowed Attention for Reduced Inference Memory via Decompression-Free KV-Cache Compression](2025-2511.18936-swan-sparse-winnowed-attention-for-reduced-inference-memory-via-decompre.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SWAN（Sparse Winnowed 注意機構）は、大規模言語モデルの生成時に増え続ける鍵・値キャッシュ（key-value キャッシュ、KVキャッシュ）を、次元方向に疎な形式へ変換して保存する方式である。50～60%程度のKVメモリ削減で多くの課題の性能が保たれると報告する一方、保持次元を減らしすぎると数学推論が大きく悪化する。

### 2年前（2024-11〜2025-10）

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：94  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2025-03 · [vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention](2024-2405.04437-vattention-virtual-memory-kv-management.md)**  
  実装：[✓](https://github.com/microsoft/vattention) ・ リポジトリ内被引用：79  
  KVキャッシュの仮想アドレスを連続に保ったままCUDA仮想メモリで物理ページだけを需要時割当し、PagedAttention固有のブロック表と専用注意カーネルを不要にする方式。長文脈サービングで最大1.23倍のスループット改善を報告する。

- **2024-12 · [A Survey on Large Language Model Acceleration based on KV Cache Management](2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-manageme.md)**  
  実装：[✓](https://github.com/TreeAI-Lab/Awesome-KV-Cache-Management) ・ リポジトリ内被引用：73  
  キャッシュを減らせば容量は空くが、注意品質の低下、検索・量子化の追加計算、CPU/SSD転送、再計算など別の費用が発生する。

- **2025-05 · [KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction](2025-2505.23416-kvzip.md)**  
  実装：[✓](https://github.com/snu-mllab/KVzip) ・ リポジトリ内被引用：55  
  元文脈の再構成時に使われるKVを重要とみなし、将来クエリを知らずに再利用可能な長文脈KVキャッシュを3〜4倍圧縮する。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：54  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-10 · [Expected Attention: KV Cache Compression by Estimating Attention from Future Queries Distribution](2025-2510.00636-expected-attention-kv-cache-compression-by-estimating-attention-from-fut.md)**  
  実装：[✓](https://github.com/NVIDIA/kvpress) ・ リポジトリ内被引用：53  
  Expected 注意機構は、大規模言語モデルの推論で増大する鍵・値キャッシュ（KV キャッシュ）を、追加学習なしに選択削除する方法である。Qwen3-8BのRULER 16Kでは、キャッシュ50%削除でも無圧縮92.9に対し92.7を維持する。

- **2025-04 · [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](2025-2504.19874-turboquant-online-vector-quantization-with-near-optimal-distortion-rate.md)**  
  実装：✓ ・ リポジトリ内被引用：51  
  TurboQuantは、高次元ベクトルを入力データセットに合わせて学習し直さずに低ビット化する、オンライン量子化方式である。理論面では、復元二乗誤差と内積誤差の両方について、ビット幅bに対して概ね4のマイナスb乗で減る上界を示し、情報理論的な下限との差が最大約2.7倍の定数内であると証明する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：47  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2025-03 · [CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences](2025-2503.12491-cake-cascading-and-adaptive-kv-cache-eviction-with-layer-preferences.md)**  
  実装：[✓](https://github.com/antgroup/cakekv) ・ リポジトリ内被引用：42  
  推論中に重要度の低いトークンのKVを削除する方式は多数提案されているが、層ごとに同じ数を保持するだけでは、必要な文脈情報が層によって異なる点を反映できない。Mistral-7Bの128K文脈では、FlashAttention-2を用いた全キャッシュ実装比でピークメモリ約48.63%削減、復号遅延10倍超の改善を報告する。

- **2024-12 · [ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression](2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-com.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/ClusterKV) ・ リポジトリ内被引用：39  
  鍵値キャッシュ（KVキャッシュ）を全量GPUに置くと、文脈長に比例して必要メモリが増え、各復号ステップで読み出すデータ量も増加する。これを抑える方法には、不要なトークンのKVを永久に破棄する方法と、CPUなど低速階層に退避したKVを必要に応じて呼び戻す方法がある。GPUでの復号遅延は最大2倍、処理率は最大2.5倍改善したと報告する。

- **2025-05 · [R-KV: Redundancy-aware KV Cache Compression for Reasoning Models](2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md)**  
  実装：[✓](https://github.com/Zefan-Cai/R-KV) ・ リポジトリ内被引用：34  
  R-KVは、推論モデルが数学問題を解く際に生成する長い思考過程に含まれる重複を利用し、自己回帰復号中の鍵値キャッシュ（Key-Value キャッシュ、以下KVキャッシュ）を固定予算に抑える手法である。論文の例では8Bモデルが約32Kトークンを生成する場合、重み15.5GBに加えてKVキャッシュ約4.1GBを要する。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-01 · [RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations](2025-2501.16383-rotatekv-accurate-and-robust-2-bit-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/ZunhaiSu/RotateKV) ・ リポジトリ内被引用：28  
  RotateKVは、言語モデルの鍵・値キャッシュ（KVキャッシュ）を2ビットまで量子化するとき、少数の極端に大きい活性値が量子化範囲を広げてしまう問題を、特徴空間の回転と選択的な高精度保持によって抑える方式である。

- **2024-12 · [DynamicKV: Task-Aware Adaptive KV Cache Compression for Long Context LLMs](2024-2412.14838-dynamickv-task-aware-adaptive-kv-cache-compression-for-long-context-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  KVを一律の長さで削る方式は簡単だが、要約、文書質問応答、コード補完などでは、重要な情報が残る層とトークン位置が異なる。

- **2025-06 · [KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider](2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at.md)**  
  実装：[✓](https://github.com/vllm-project/vllm/pull/22236) ・ リポジトリ内被引用：26  
  合成トレースではなく本番サービスのトレースに基づく設計材料が不足しているという問題に対し、本研究はAliyun Tongyiの大規模serving クラスタから得た顧客向け(to-C)と企業向け(to-B)のトレースを特徴付け、観測した分布を使う追い出し 方策を提案する。

- **2025-05 · [FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion](2025-2505.21467-flashdlm-accelerating-diffusion-language-model-inference.md)**  
  実装：[✓](https://github.com/ZhanqiuHu/flash-dlm-experimental) ・ リポジトリ内被引用：25  
  FlashDLMは拡散言語モデル（Diffusion Language モデル; DLM）の遅さを、1回のノイズ除去で再計算し過ぎる問題と、何回ノイズ除去を繰り返すかという問題に分ける。FreeCacheは前者を、Guided Diffusionは後者を削り、二つを組み合わせて大きな端末間高速化を得る。

- **2025-03 · [xKV: Cross-Layer KV-Cache Compression via Aligned Singular Vector Extraction](2025-2503.18893-xkv-cross-layer-kv-cache-compression-via-aligned-singular-value-decomposition.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/xKV) ・ リポジトリ内被引用：25  
  xKVは、隣接層のキー・バリュー（Key-Value; KV）キャッシュをトークンごとに直接似ているとみなすのではなく、複数層が共有する支配的な特異ベクトルをまとめて抽出する。プリフィル時に複数層を横連結して共有低ランク基底へ因子分解し、デコード時はクエリに重要なトークンだけを選択的に再構成する。

- **2025-02 · [KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference](2025-2502.04420-kvtuner-sensitivity-aware-layer-wise-mixed-precision-kv-cache-quantizati.md)**  
  実装：[✓](https://github.com/cmd2001/KVTuner) ・ リポジトリ内被引用：24  
  KVTunerは、大規模言語モデル（LLM）の鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を、層ごとに異なるビット幅で量子化するための自動設定方式である。またKIVI-KV8を基準に、文脈長を変えた実験で最大21.25%の推論処理量改善を報告する。

- **2024-12 · [DiffKV: Differentiated Memory Management for Large Language Models with Parallel KV Compaction](2024-2412.03131-diffkv-differentiated-memory-management-for-large-language-models-with-parallel-kv-compaction.md)**  
  実装：[✓](https://github.com/zyqCSL/DiffKV) ・ リポジトリ内被引用：22  
  鍵・値・トークン・注意ヘッドを異なる粒度で圧縮し、不規則な空き容量をGPU内で並列コンパクションするDiffKV。KVを2.7〜5.7倍圧縮しスループットを1.9〜5.4倍改善する。

- **2024-11 · [DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving](2024-2411.02820-droidspeak-kv-cache-sharing-for-cross-llm-communication-and-multi-llm-se.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  DroidSpeakは、同じ基盤モデルを微調整して得た異なるLLMが、同じ会話履歴や文書を別々に処理する際の重複プリフィルを減らす分散推論システムである。著者らは8種類のモデル対で層別の感度を測定し、KV差異に敏感な層は平均約11%と報告した。

- **2025-10 · [KVComm: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems](2025-2510.12872-kvcomm-online-cross-context-kv-cache-communication-for-efficient-llm-bas.md)**  
  実装：[✓](https://github.com/FastMAS/KVCOMM) ・ リポジトリ内被引用：21  
  複数の大規模言語モデル（LLM）エージェントが役割を分担すると、各エージェントのシステム指示、直前の発言、道具から得た文章は異なる。

- **2025-10 · [Cache-to-Cache: Direct Semantic Communication Between Large Language Models](2025-2510.03215-cache-to-cache-direct-semantic-communication-between-large-language-mode.md)**  
  実装：[✓](https://github.com/thu-nics/C2C) ・ リポジトリ内被引用：19  
  複数の大規模言語モデル（LLM）が協調するシステムでは、あるモデルが推論や分析の結果を文章として生成し、別のモデルがその文章を読み込んで次の応答を作ることが多い。

- **2025-06 · [CommVQ: Commutative Vector Quantization for KV Cache Compression](2025-2506.18879-commvq-commutative-vector-quantization-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UMass-Embodied-AGI/CommVQ) ・ リポジトリ内被引用：19  
  CommVQは、長文脈の大規模言語モデル推論で鍵値キャッシュ（KVキャッシュ）が装置メモリを占有する問題に対し、ベクトル量子化（Vector Quantization; VQ）と回転位置埋め込み（Rotary Position Embedding; RoPE）の代数的性質を組み合わせて、保存容量と復号計算の両方を削減する方法である。

- **2025-02 · [Online Scheduling for LLM Inference with KV Cache Constraints](2025-2502.07115-online-scheduling-for-llm-inference-with-kv-cache-constraints.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  本研究は、大規模言語モデル（LLM）の複数要求を一つの推論ワーカーで処理する際に、生成が進むほど増える鍵・値キャッシュ（KVキャッシュ）を将来時点まで予測し、どの要求をいつ開始するかを決めるオンラインスケジューリング（online スケジューラ）を扱う。

- **2025-02 · [Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation](2025-2502.15734-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-gene.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  文書自体が同じなのに、GPUはその文書の鍵・値（KV）を再計算することになる。Cache-Craftは再利用するかどうかの判定と、どれだけ再計算して修復するかの決定を分離する。実際のRAGワークロードでは、接頭辞キャッシュ比で冗長計算を51%減らし、連続バッチ下で処理率を1.6倍、エンドツーエンド応答遅延を約半分にしたと報告する。

- **2025-10 · [Attention Is All You Need for KV Cache in Diffusion LLMs](2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Elastic-Cache) ・ リポジトリ内被引用：17  
  従来の安全な実装は、各復号段階ですべての位置と層のクエリ・キー・値を再計算するが、変化の少ない状態まで繰り返し計算するため遅い。提案方式は、左側の未確定位置を中心とする移動窓で新しいトークンを予測し、窓外MASKのKVを再利用する。

- **2025-03 · [Jenga: Effective Memory Management for Serving LLM with Heterogeneity](2025-2503.18292-jenga-heterogeneous-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  PagedAttentionは固定サイズのページでKVを割り当て、従来の連続領域確保よりメモリ断片化を減らした。論文のvLLMベース実装は、H100で要求処理量を平均1.80倍、最大4.92倍、L4で平均1.69倍、最大3.29倍へ改善した。

- **2025-07 · [Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation](2025-2507.10524-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-tok.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  共有Transformerブロックを再帰利用し、ルータがトークンごとに継続深度を決めて活動集合だけへ注意・KV保持することで、推論時の適応計算とパラメータ共有を両立する。

- **2025-02 · [TransMLA: Migrating GQA Models to MLA with Full DeepSeek Compatibility and Speedup](2025-2502.07864-transmla-migrating-gqa-models-to-mla-with-full-deepseek-compatibility-an.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  TransMLAは、すでに学習済みのグループ化問い合わせ注意（Grouped Query 注意機構、GQA）モデルを、DeepSeek系の多頭潜在注意（Multi-head Latent 注意機構、MLA）へ変換するための手法である。

- **2025-02 · [QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache](2025-2502.10424-quantspec-self-speculative-decoding-with-hierarchical-quantized-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  QuantSpecは、長い文脈を持つ大規模言語モデルの復号で、鍵値キャッシュ（KVキャッシュ）の読出しがGPU帯域と容量を圧迫する問題を、階層量子化キャッシュを共有する自己投機的復号によって改善する。

- **2025-10 · [Acon: Optimizing Context Compression for Long-horizon LLM Agents](2025-2510.00615-acon-optimizing-context-compression-for-long-horizon-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  Acon（Agent Context Optimization）は、過去の行動・観測をまとめた履歴と、新たに届いた長いツール観測の両方をLLMで圧縮する。圧縮の指針を人手で固定せず、同じ課題で非圧縮なら成功したのに圧縮後は失敗した実行軌跡を比較し、失われた重要情報を分析して自然言語の圧縮指示を改善する。

- **2025-05 · [PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs](2025-2505.18610-pm-kvq-progressive-mixed-precision-kv-cache-quantization-for-long-cot-llms.md)**  
  実装：[✓](https://github.com/thu-nics/PM-KVQ) ・ リポジトリ内被引用：12  
  KVを16→8→4→2bitと必要時だけ段階圧縮し、層感度とRoPE位置補間校正で長CoTの累積量子化誤差を抑えるPM-KVQ。

- **2025-10 · [ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models](2025-2510.01290-thinkv-thought-adaptive-kv-cache-compression-for-efficient-reasoning-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  ThinKVは、長い思考過程を出力する推論型大規模言語モデル（large reasoning モデル; LRM）のKVキャッシュを、単純なトークン年齢や注意得点だけでなく、現在どの種類の思考区間を生成しているかに応じて圧縮する方式である。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：11  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-02 · [CriticalKV: Optimizing KV Cache Eviction from an Output Perturbation Perspective](2025-2502.03805-criticalkv-optimizing-kv-cache-eviction-from-an-output-perturbation-perspective.md)**  
  実装：[✓](https://github.com/FFY0/DefensiveKV) ・ リポジトリ内被引用：11  
  KVキャッシュ追い出しを「注意出力摂動の最小化」として定式化し、注意重み×出力射影後の値状態ノルムで重要KVを選ぶ二段階方式により、既存3方式の圧縮損失を29データセット平均で半分超削減する。

- **2025-05 · [FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference](2025-2505.13109-freekv-boosting-kv-cache-retrieval-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/FreeKV) ・ リポジトリ内被引用：10  
  全KVをGPUメモリに保持すると長文脈・同時要求数の増加に耐えにくい。そこで全KVをCPUメモリに保持し、注意計算に必要なページだけGPUへ呼び戻す検索型圧縮が考えられる。原著の32K文脈・バッチ1の分析では、ArkValeの時間の約94%、ShadowKVの約73%が選択と呼び戻しに費やされる。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

- **2025-01 · [PRESERVE: Prefetching Model Weights and KV-Cache in Distributed LLM Serving](2025-2501.08192-preserve-prefetching-model-weights-and-kv-cache-in-distributed-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  PRESERVEは、複数のGPUまたはNPUに大規模言語モデルを分割して実行する際、アクセラレータ間の集合通信が生む待ち時間を、次の演算に必要なメモリ読み出しへ転用する手法である。バッチ4、最大系列長16Kなどの条件で、先読みを行わない基準方式に対し端から端までの推論時間を1.09～1.61倍短縮した。

- **2024-12 · [KunServe: Parameter-centric Memory Management for Efficient Memory Overloading Handling in LLM Serving](2024-2412.18169-kunserve-elastic-and-efficient-large-language-model-serving-with-paramet.md)**  
  実装：[✓](https://github.com/SJTU-IPADS/kunserve) ・ リポジトリ内被引用：10  
  リクエストのKVキャッシュを捨てる代わりに、複数の推論インスタンスに重複配置されたモデル重みを一時解放する。残存する層を複数GPUで協調実行し、通信とバッチ形成を調整することで、突発負荷時の待ち行列を短縮する。

- **2025-05 · [TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization](2025-2505.19586-tailorkv-layer-tailored-quantization-offloading.md)**  
  実装：[✓](https://github.com/ydyhello/TailorKV) ・ リポジトリ内被引用：9  
  TailorKVは、層ごとの注意特性に応じてKVを低ビット保持する層とCPUから動的top-k取得する層へ分け、PCIe転送と長文KV容量を削減する。

- **2025-08 · [CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation](2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-b.md)**  
  実装：[✓](https://github.com/TUDa-HWAI/CompressKV) ・ リポジトリ内被引用：8  
  文脈が長くなるほどKV容量と注意計算量が増え、GPUメモリ容量と応答遅延の制約が厳しくなる。第二に、極端に小さいKV予算で注意ブロックの出力がどれだけ変化するかをオフラインで測定し、圧縮に弱い層へ多くのKV予算を配る。

- **2025-05 · [ReCalKV: Low-Rank KV Cache Compression via Head Reordering and Offline Calibration](2025-2505.24357-recalkv-low-rank-kv-cache-compression-via-head-reordering.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/ReCalKV) ・ リポジトリ内被引用：8  
  ReCalKVは、大規模言語モデルの長文推論で増大する鍵・値キャッシュ（KVキャッシュ）を、保存する隠れ次元の低ランク化によって削減する学習後圧縮方式である。既存の低ランクKV圧縮であるPaluと比較し、LLaMA-2-7BのKVを70%圧縮したとき、6つのゼロショット質問応答課題の平均はReCalKVが59.90%、Paluが52.14%だった。

- **2025-05 · [Lookahead Q-Cache: Achieving More Consistent KV Cache Eviction via Pseudo Query](2025-2505.20334-lookahead-q-cache-achieving-more-consistent-kv-cache-eviction-via-pseudo.md)**  
  実装：[✓](https://github.com/noforit/Lookahead_Q-Cache) ・ リポジトリ内被引用：8  
  Lookahead Q-Cache（LAQ）は、大規模言語モデルの長文推論で、KVキャッシュをどの位置から削除するか決めるための観測窓を、入力末尾から仮に生成した回答の問い合わせベクトルへ変更する手法である。

- **2025-04 · [CAOTE: KV Cache Selection for LLMs via Attention Output Error-Based Token Eviction](2025-2504.14051-caote-kv-cache-selection-for-llms-via-attention-output-error-based-token.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  従来のH2O・TOVA・SnapKVなどは、主に注意重み（注意機構 score）を重要度の代理指標として利用する。

- **2025-09 · [EvolKV: Evolutionary KV Cache Compression for LLM Inference](2025-2509.08315-evolkv-evolutionary-kv-cache-compression-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  KVを削除すればメモリ容量を抑えられるが、どの層にどれだけの過去情報を残すかは回答品質に強く影響する。既存方式は全層に同じ保持数を割り当てるか、下層から上層へ単調に予算を減らすピラミッド型の規則を使うことが多い。

- **2025-09 · [EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments](2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-reso.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  一般的な事後圧縮は履歴全体を事前入力（プリフィル）してから不要なKVを削除するため、圧縮後の容量が小さくても処理途中のピークメモリを抑えられない。LongMemEval、RealTalk、LoCoMoを使った評価では、4～6倍のKV圧縮でも全KVに近い回答品質を示す条件がある。

- **2025-01 · [Cache Me If You Must: Adaptive Key-Value Quantization for Large Language Models](2025-2501.19392-cache-me-if-you-must-adaptive-key-value-quantization-for-large-language-.md)**  
  実装：[✓](https://github.com/goodevening13/aquakv) ・ リポジトリ内被引用：7  
  長文脈の大規模言語モデル（LLM）では、生成済みトークンの注意機構に使う鍵・値（KV）を各層に保存する。原著の例では、131,072トークンを保持するLlama 3.2 3Bの16ビットKVは約15 GiB、Llama 3.1 70Bでは約42.9 GB（論文の導入部における十進表記）を占める。

- **2025-10 · [Which Heads Matter for Reasoning? RL-Guided KV Cache Compression](2025-2510.08525-which-heads-matter-for-reasoning-rl-guided-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  既存のKV削除手法は、検索・要約型のタスクで重要なトークンや注意ヘッドを見つけるが、数千トークンに及ぶ推論途中の自己修正・論理的一貫性・終了判断を保つためのヘッドと必ずしも一致しない。

- **2025-06 · [InfiniPot-V: Memory-Constrained KV Cache Compression for Streaming Video Understanding](2025-2506.15745-infinipot-v-memory-constrained-kv-cache-compression-for-streaming-video-.md)**  
  実装：[✓](https://github.com/aiha-lab/InfiniPot-V) ・ リポジトリ内被引用：6  
  InfiniPot-Vは、動画を順次処理する映像言語モデルの鍵・値キャッシュ（KVキャッシュ）が、視聴時間とともに増加する問題を扱う。全映像のKVキャッシュをいったん構築してから圧縮する方式は、圧縮前の瞬間最大メモリが装置容量を超える。主要評価では、Qwen-2-VL-7Bの50Kトークン相当の動画文脈を6Kへ縮小しても、MLVU平均65.8を維持した。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-09 · [PagedEviction: Structured Block-wise KV Cache Pruning for Efficient Large Language Model Inference](2025-2509.04377-pagedeviction-structured-block-wise-kv-cache-pruning-for-efficient-large.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  PagedEvictionは、推論サーバーvLLMで用いられるページ型KVキャッシュ管理（PagedAttention）と、KVキャッシュの重要度に基づく削除を両立させる方式である。

- **2025-04 · [Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching](2025-2504.06319-asynchronous-kv-cache-prefetching.md)**  
  実装：[✓](https://github.com/alibaba/vllm_xformers_prefetch) ・ リポジトリ内被引用：5  
  本研究は、大規模言語モデルの自己回帰復号において、鍵値キャッシュ（KV キャッシュ）を高帯域メモリ（HBM）から読み込む間にGPUの実行単位が待たされる問題を対象とする。鍵値を削除・量子化・オフロードして保存容量を減らすのではなく、現在の鍵値ブロックを使った注意演算と、次に必要なブロックのHBMから二次キャッシュ（L2 キャッシュ）への転送を重ねる。

- **2025-03 · [Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs](2025-2503.00979-dialogue-without-limits-constant-sized-kv-caches-for-extended-responses-.md)**  
  実装：[✓](https://github.com/ghadiaravi13/MorphKV) ・ リポジトリ内被引用：5  
  従来のSnapKVのように入力側のキャッシュを圧縮しても、生成済みトークンをすべて残す実装では出力長に比例する増大を止められない。要旨の「52.9%節約、18.2%品質改善」は、長文応答タスクにおける比較対象H2Oとの平均比較であり、全注意に対する普遍的な改善率ではない。

- **2025-08 · [KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache](2025-2509.00579-kvcomp-a-high-performance-llm-aware-lossy-compression-framework-for-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KVCompは、大規模言語モデルの長文脈推論において、過去トークンの鍵・値（KV）キャッシュがGPUメモリを占有し、処理可能な文脈長や同時実行数を制限する問題に取り組む。既存の低ビット量子化だけでは整数符号に残る統計的偏りを使い切れず、一般的な可逆圧縮を追加すると毎トークン必要な復号が遅くなる。

- **2025-05 · [Mustafar: Promoting Unstructured Sparsity for KV Cache Pruning in LLM Inference](2025-2505.22913-mustafar-promoting-unstructured-sparsity-for-kv-cache-pruning-in-llm-inf.md)**  
  実装：[✓](https://github.com/dhjoo98/mustafar) ・ リポジトリ内被引用：4  
  Mustafarは、大規模言語モデル（LLM）の逐次生成時に蓄積する鍵・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を、トークンごと・要素ごとの非構造化枝刈り（unstructured 枝刈り）で圧縮し、その圧縮形式をGPUの注意演算へ直接渡す方式である。

- **2025-05 · [LoLA: Low-Rank Linear Attention with Sparse Caching](2025-2505.23666-lola-low-rank-linear-attention-with-sparse-caching.md)**  
  実装：[✓](https://github.com/lukemcdermotttt/LoLA-release) ・ リポジトリ内被引用：4  
  LoLA（Low-Rank Linear 注意機構 with Sparse Caching）は、線形注意（Linear 注意機構）が長い文脈を固定長の再帰状態に圧縮する際に失いやすい、個別の鍵と値の対応関係を守るための推論時キャッシュ管理方式である。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-08 · [SmallKV: Small Model Assisted Compensation of KV Cache Compression for Efficient LLM Inference](2025-2508.02751-smallkv-small-model-assisted-compensation-of-kv-cache-compression-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SmallKVは、長文脈の大規模言語モデル（LLM）の鍵・値キャッシュ（KV キャッシュ）を小さくする際、単純な重要度順位でトークンを消してしまうと必要な情報が失われる問題を、小型言語モデル（Small Language モデル; SLM）との協調で緩和する方式である。

- **2025-08 · [Selective KV-Cache Sharing to Mitigate Timing Side-Channels in LLM Inference](2025-2508.08438-selective-kv-cache-sharing-to-mitigate-timing-side-channels-in-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SafeKVは、大規模言語モデル（LLM）の複数利用者向けサービングにおいて、プレフィックスのKVキャッシュを利用者間で共有する性能上の利益と、共有によるタイミング情報漏えいを両立させるシステムである。

- **2025-08 · [KV Cache Compression for Inference Efficiency in LLMs: A Review](2025-2508.06297-kv-cache-compression-for-inference-efficiency-in-llms-a-review.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  著者はKV圧縮を、重要なトークンを選んで残す方式、K/Vのビット幅を下げる量子化、注意構造やヘッドの冗長性を利用する方式、複数の技術を組み合わせる方式に分類する。

- **2025-07 · [HCAttention: Extreme KV Cache Compression via Heterogeneous Attention Computing for LLMs](2025-2507.19823-hcattention-heterogeneous-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  キー量子化・値のCPU退避・層別の動的KV削除を統合し、GPU KV予算25%でLlama-3-8BのLongBench平均43.2を全注意と同値に保ち、12.5%でも42.5（0.7ポイント差）に抑える異種GPU/CPU注意方式。

- **2025-06 · [AnTKV: Anchor Token-Aware Sub-Bit Vector Quantization for KV Cache in Large Language Models](2025-2506.19505-antkv-anchor-token-aware-sub-bit-vector-quantization-for-kv-cache-in-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  AnTKVは、TransformerのKVキャッシュを極端に低いビット幅へ圧縮したときの品質劣化を、トークンごとの誤差感度が均一ではないという観察から抑える方式である。FP16のアンカーが全体の1%でも、1bit以下の領域で大きな品質改善が報告される。

- **2025-06 · [AhaKV: Adaptive Holistic Attention-Driven KV Cache Eviction for Efficient Inference of Large Language Models](2025-2506.03762-ahakv-adaptive-holistic-attention-driven-kv-cache-eviction-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  AhaKVは、LLM推論でKVキャッシュを固定予算へ圧縮するとき、過去トークンの重要度を累積注意スコアだけで決めることの偏りを修正する方式である。

- **2025-05 · [KVmix: Gradient-Based Layer Importance-Aware Mixed-Precision Quantization for KV Cache](2025-2506.08018-kvmix-gradient-based-layer-importance-aware-mixed-precision-quantization.md)**  
  実装：[✓](https://github.com/LfLab-AI/KVmix) ・ リポジトリ内被引用：3  
  KVmixは、長い文脈や多数の同時要求でGPUメモリを圧迫するKVキャッシュを、モデルの品質に影響しやすい層と影響しにくい層に分けて量子化する方式である。RTX 4090 24GBで入力688トークン・最大生成1024トークンの実験では、最大バッチサイズを増やせることを含めた処理率が194.06から1032.06 トークン/sへ上昇する。

- **2025-05 · [FreqKV: Key-Value Compression in Frequency Domain for Context Window Extension](2025-2505.00570-freqkv-key-value-compression-in-frequency-domain-for-context-window-exte.md)**  
  実装：[✓](https://github.com/LUMIA-Group/FreqKV) ・ リポジトリ内被引用：3  
  全履歴を保持する方式では文脈長に応じてKV容量が増え、長い事前入力では注意の計算量も増える。

- **2025-04 · [SentenceKV: Efficient LLM Inference via Sentence-Level Semantic KV Caching](2025-2504.00970-sentencekv-efficient-llm-inference-via-sentence-level-semantic-kv-cachin.md)**  
  実装：[✓](https://github.com/zzbright1998/SentenceKV) ・ リポジトリ内被引用：3  
  SentenceKVは、長い入力を文ごとのまとまりに分け、文の意味を表す小さなキー索引だけをGPUに残して、個々の鍵・値（KV）対をCPU側へ退避する長文脈推論方式である。

- **2025-03 · [Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving](2025-2503.24000-rethinking-key-value-cache-compression-techniques-for-large-language-mod.md)**  
  実装：[✓](https://github.com/LLMkvsys/rethink-kv-compression) ・ リポジトリ内被引用：3  
  鍵値キャッシュ（Key-Value Cache、KVキャッシュ）の圧縮は、大規模言語モデル（Large Language モデル、LLM）の復号で過去トークンの状態を保持するGPUメモリを減らす。

- **2025-03 · [Efficient Many-Shot In-Context Learning with Dynamic Block-Sparse Attention](2025-2503.08640-efficient-many-shot-in-context-learning-with-dynamic-block-sparse-attent.md)**  
  実装：[✓](https://github.com/millix19/dbsa) ・ リポジトリ内被引用：3  
  通常の多数例ICLは、同じモデルを複数の分類課題へ転用できる反面、数千件の入力・正解ラベル例を毎要求の文脈へ入れるため推論が高価になる。動的 Block-Sparse 注意機構（DBSA）はこの二者を分離する。第2段階では、BM25によって要求に関連するブロックを30%検索し、保存したKV断片を連結し直してから新しい要求を生成する。

- **2025-02 · [Compression Barriers in Autoregressive Transformers](2025-2502.15955-compression-barriers-in-autoregressive-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  近年のKV圧縮は重要トークンの選択、疎性、低次元表現、クラスタリング等で保存量を削減しているが、これらの成功が任意の入力でも保証できるかは別問題である。

- **2024-12 · [More Tokens, Lower Precision: Towards the Optimal Token-Precision Trade-off in KV Cache Compression](2024-2412.12706-more-tokens-lower-precision-towards-the-optimal-token-precision-trade-of.md)**  
  実装：[✓](https://github.com/zhzihao/QPruningKV) ・ リポジトリ内被引用：3  
  KVキャッシュの容量制約下で、残すトークン数と量子化精度を別々に決めず、両者の積で予算を配分する「量子化付き間引き」を検証した研究。

- **2025-10 · [VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization](2025-2510.06175-vecinfer-efficient-llm-inference-with-low-bit-kv-cache-via-outlier-suppr.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  キャッシュ量は文脈長に比例して増えるため、長い入力を扱う際にはGPUの高帯域メモリ（HBM）容量が不足し、デコード中の読み出し量も大きくなる。ベクトル量子化（VQ）は複数要素を一つの代表ベクトルへ対応付け、各小ベクトルを短い索引として保存する。長文脈192K入力・129出力のH100単一バッチでは、2ビット構成でデコード遅延が8.3倍改善した。

- **2025-10 · [TALE: Token-Adaptive Low-Rank KVCache Approximation with Reconstruction Elimination](2025-ffb681f1a4fd-tale-token-adaptive-low-rank-kvcache-approximation-with-reconstruction-e.md)**  
  実装：[✓](https://github.com/thnkinbtfly/TALE) ・ リポジトリ内被引用：2  
  TALE（トークン-適応的 Low-Rank KVCache Approximation with Reconstruction Elimination）は、既存の大規模言語モデル（LLM）の重みを再学習せずに、生成時のキー・バリューキャッシュ（KV キャッシュ）を削減する方式である。

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

- **2025-07 · [Multi-matrix Factorization Attention](2025-98e1f6bbeb53-multi-matrix-factorization-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  自己回帰型の大規模言語モデルでは、生成済みトークンの鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を保存することで、次のトークンを生成するたびに過去系列を再計算せずに済む。12個の評価指標の平均はMHA 49.0、MFA 49.9、MFA-KR 48.0で、MFAは少ないキャッシュ量でも比較対象のMHAをわずかに上回った。

- **2025-07 · [Forecasting LLM Inference Performance via Hardware-Agnostic Analytical Modeling](2025-2508.00904-forecasting-llm-inference-performance-via-hardware-agnostic-analytical-m.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  入力長、出力長、注意機構、量子化、演算融合、カーネルの効率が時間とともに変わるためである。Llama2-7Bを対象に、プレフィル（プリフィル）で入力長256から65,536へ増やすと、行列積（GEMM）の計算量構成比が99.0%から27.5%へ下がり、バッチ行列積（BMM）が1.0%から71.6%へ増えると推計した（表4）。

- **2025-02 · [CalibQuant: 1-Bit KV Cache Quantization for Multimodal LLMs](2025-2502.14882-calibquant-1-bit-kv-cache-quantization-for-multimodal-llms.md)**  
  実装：[✓](https://github.com/insuhan/calibquant) ・ リポジトリ内被引用：2  
  主張は、視覚トークンのKVキャッシュを圧縮し、限られたメモリ予算下でバッチ数を増やしてデコードスループットを上げることであり、モデル重みを1bit化する方式ではない。主結果はCOCO Caption、DocVQA、MMBench-VideoとH100 80GBでのスループット評価である。

- **2024-12 · [XKV: Personalized KV Cache Memory Reduction for Long-Context LLM Inference](2024-2412.05896-xkv-personalized-kv-cache-memory-reduction-for-long-context-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  トークンの重要度に基づいて一部のKVを捨てる方式はあるが、各Transformer層へ同じ容量を割り当てたり、層位置に応じてあらかじめ決めたピラミッド形の容量を割り当てたりすると、入力とタスクごとに変わる重要度分布を捉えきれない。

- **2024-12 · [EMS: Adaptive Evict-then-Merge Strategy for Head-wise KV Cache Compression Based on Global-Local Importance](2024-2412.08521-ems-adaptive-evict-then-merge-strategy-for-head-wise-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  EMS（適応的 Evict-then-Merge Strategy）は、重要度の計測と実際の圧縮を分離する。最大10.75倍のスループット改善も報告するが、これは実行可能な最大バッチサイズが変わる条件での比較であり、単一要求の10.75倍高速化ではない。

- **2025-10 · [Improving Model Representation and Reducing KV Cache via Skip Connections with First Value Heads](2025-2510.16807-improving-model-representation-and-reducing-kv-cache-via-skip-connection.md)**  
  実装：[✓](https://github.com/Zhoutong-Wu/SkipV1Former) ・ リポジトリ内被引用：1  
  このKVキャッシュは系列長、層数、ヘッド数、同時要求数に比例して増えるため、長文脈推論ではモデル重みと並ぶGPUメモリの制約になる。反対に、残差経路を増やして浅い情報を深い層へ伝える方式は、品質を改善してもKVキャッシュを減らさないことが多い。

- **2025-10 · [Breadcrumbs Reasoning: Memory-Efficient Reasoning with Compression Beacons](2025-2510.13797-breadcrumbs-reasoning-memory-efficient-reasoning-with-compression-beacon.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Breadcrumbs Reasoning（BR）は、生成を一定数進めるたびに専用の圧縮ビーコンをモデルへ入力し、直前の生成トークンのKVをビーコン1個のKVへ置換する。

- **2025-08 · [Spotlight Attention: Towards Efficient LLM Generation via Non-linear Hashing-based KV Cache Retrieval](2025-2508.19740-spotlight-attention-towards-efficient-llm-generation-via-non-linear-hash.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Spotlight 注意機構は、大規模言語モデル（LLM）の長文脈生成で、過去の鍵・値キャッシュ（KV キャッシュ）のうち現在の問い合わせに重要な少数トークンだけを取り出して注意計算を行う方式である。A100単体で512Kトークンに対するハッシュ検索を100マイクロ秒未満とし、通常の全注意デコードに比べ端から端まで最大約3倍のスループットを示した。

- **2025-07 · [ReasonCache: Accelerating Large Reasoning Model Serving through KV Cache Sharing](2025-2507.21433-reasoncache-accelerating-large-reasoning-model-serving-through-kv-cache-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  生成トークンが増えると、過去のトークンに対応するキー・バリュー（KV）キャッシュも伸び、GPUメモリを圧迫する。ReasonCacheは似た思考ステップに対応するKVブロックが内部表現上も似ているという観測を利用し、既に保持している物理ブロックを新しい論理位置から参照することで、KVの実体数を減らす方式である。

- **2025-07 · [Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing](2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話ごとの注意類似度から層間の鍵・値共有を動的選択し、注意類似度計算を中央処理装置と画像処理装置へ分担、圧縮後の再計算とロードを層間パイプラインで重畳してマルチターン状態復元を高速・省容量化する。

- **2025-07 · [FAEDKV: Infinite-Window Fourier Transform for Unbiased KV Cache Compression](2025-2507.20030-faedkv-infinite-window-fourier-transform-for-unbiased-kv-cache-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  H2OやSnapKVのようなトークン削除はメモリを節約する一方、直近の注意や頻出トークンを重視し、後から必要になる古い情報を消す場合がある。学習済み圧縮器は別途学習費用を要し、過去の圧縮表現を繰り返し更新すると古い情報が劣化する可能性もある。

- **2025-06 · [TaDA: Training-free recipe for Decoding with Adaptive KV Cache Compression and Mean-centering](2025-2506.04642-tada-training-free-recipe-for-decoding-with-adaptive-kv-cache-compressio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TaDAは、自己回帰型の大規模言語モデル（LLM）で生成済みトークンの鍵・値を保存するKVキャッシュを、重み再学習なしに小さくする方式である。これは容量を27%まで削減したという意味であり、「27%だけ削減」とは異なる。

- **2025-06 · [MadaKV: Adaptive Modality-Perception KV Cache Eviction for Efficient Multimodal Long-Context Inference](2025-2506.15724-madakv-adaptive-modality-perception-kv-cache-eviction-for-efficient-mult.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MadaKVは、各注意ヘッドが画像と文字のどちらへ注意を向けているかを測り、モダリティごとに異なるKV保持予算を割り当てるModality Preference Adaptation（MPA）と、層ごとの圧縮過不足を後続層へ補償するHierarchical Compression Compensation（HCC）を組み合わせる。

- **2025-05 · [EFIM: Efficient Serving of LLMs for Infilling Tasks with Improved KV Cache Reuse](2025-2505.21889-efim-infilling-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/gty111/EFIM) ・ リポジトリ内被引用：1  
  FIMの増分を末尾へ移して接頭部・接尾部KVを要求間再利用し、断片トークン化学習で語途中生成能力を補って平均遅延52%削減・スループット98%向上。

- **2025-03 · [WindowKV: Task-Adaptive Group-Wise KV Cache Window Selection for Efficient LLM Inference](2025-2503.17922-windowkv-task-adaptive-group-wise-kv-cache-window-selection-for-efficien.md)**  
  実装：[✓](https://github.com/optim996/WindowKV) ・ リポジトリ内被引用：1  
  長い入力をプリフィルした後、全トークンの鍵・値を全層で保持すると、生成中にKVキャッシュがGPUメモリを圧迫する。WindowKVは連続したレビュー窓を単位に選び、入力タスクに応じて窓のスコア付けを切り替える。著者は全KVの約12%の容量で同等に近い品質を報告する。

- **2025-02 · [CoKV: Optimizing KV Cache Allocation via Cooperative Game](2025-2502.17501-cokv-optimizing-kv-cache-allocation-via-cooperative-game.md)**  
  実装：[✓](https://github.com/nawei1010/CoKV) ・ リポジトリ内被引用：1  
  Mistral-7B-Instruct-v0.2をA100 40GBで動かした実測では、28kトークン入力の生成総時間がFullKVの半分未満、32k入力のピークGPUメモリは64%削減された。オンライン要求ごとにゲーム理論の評価をやり直す方式ではない。

- **2025-10 · [GUI-KV: Efficient GUI Agents via KV Cache with Spatio-Temporal Awareness](2025-2510.00536-gui-kv-efficient-gui-agents-via-kv-cache-with-spatio-temporal-awareness.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GUI-KV) ・ リポジトリ内被引用：0  
  論文はUI-TARS-1.5-7Bについて、5画面・最大50段階の条件でGPUメモリ消費が80GBを超え得ると説明し、単なる計算高速化ではなく、履歴を保持するためのメモリ節約を主課題とする。GUI-KVは、自然画像用の圧縮方式をそのまま転用せず、画面固有の二種類の冗長性を利用する。

- **2025-09 · [OjaKV: Context-Aware Online Low-Rank KV Cache Compression](2025-2509.21623-ojakv-context-aware-online-low-rank-kv-cache-compression.md)**  
  実装：[✓](https://github.com/zzbright1998/OjaKV) ・ リポジトリ内被引用：0  
  OjaKVは長文脈言語モデルのキー・バリュー（KV）キャッシュを低ランク射影で圧縮する際、校正データで決めた固定基底が実際の会話・コード・ニュースなどの分布変化に適合しなくなる問題を扱う。LongChat-7B-v1.5-32kの16K RULERでは、KV保存予算0.6倍の条件で静的PCAの平均正答率23.44%をOjaKVが39.99%へ改善した。

- **2025-08 · [Unifying Mixture of Experts and Multi-Head Latent Attention for Efficient Language Models](2025-2508.01261-unifying-mixture-of-experts-and-multi-head-latent-attention-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Unifying Mixture of エキスパート and Multi-Head Latent 注意機構 for Efficient Language Modelsは、小型言語モデルの計算量とKVキャッシュ量を同時に抑えるため、Mixture-of-Experts（MoE）、Multi-head Latent 注意機構（MLA）…

- **2025-05 · [NSNQuant: A Double Normalization Approach for Calibration-Free Low-Bit Vector Quantization of KV Cache](2025-2505.18231-nsnquant-a-double-normalization-approach-for-calibration-free-low-bit-ve.md)**  
  実装：[✓](https://github.com/DHdroid/NSNQuant) ・ リポジトリ内被引用：0  
  重みを低ビット化しても、生成が長くなると過去トークンの鍵・値（KV）がGPUメモリを占有し、同時に処理できる要求数が減る。NSNQuantは、このKVを1ビットまたは2ビット相当のベクトル量子化で保存する方式である。

- **2025-03 · [Time and Memory Trade-off of KV-Cache Compression in Tensor Transformer Decoding](2025-2503.11108-time-and-memory-trade-off-of-kv-cache-compression-in-tensor-transformer-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ところが、複数のキー・値を組み合わせる高次のテンソル 注意機構では、元のキー・値を保持するか、組み合わせたキー・値を事前展開して保持するかで、より極端な時間と記憶量の交換条件が現れる。

- **2025-03 · [LogQuant: Log-Distributed 2-Bit Quantization of KV Cache with Superior Accuracy Preservation](2025-2503.19950-logquant-log-distributed-2-bit-quantization-of-kv-cache-with-superior-ac.md)**  
  実装：[✓](https://github.com/Concyclics/LogQuantKV) ・ リポジトリ内被引用：0  
  LogQuantは、長文脈のLLM推論で増大する鍵・値キャッシュ（KVキャッシュ）を2bitへ圧縮しつつ、重要な位置を選択的に元の精度で残す手法である。Llama-3.1-8B-Instructでは、GSM8Kの最終回答正答率が2bit KiViの18.04%に対してLogQuantの40.41%へ改善する（論文Table 4）。

- **2025-02 · [BaKlaVa - Budgeted Allocation of KV cache for Long-context Inference](2025-2502.13176-baklava-budgeted-allocation-of-kv-cache-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BaKlaVaは、長文脈のLLM推論でKVキャッシュを削減する際、全注意ヘッドへ同じ保持容量を与えるのではなく、重要度の高いヘッドへ多く、低いヘッドへ少なく配分する方式である。

- **2025-01 · [MPCache: MPC-Friendly KV Cache Eviction for Efficient Private LLM Inference](2025-2501.06807-mpcache-mpc-friendly-kv-cache-eviction-for-efficient-private-llm-inferen.md)**  
  実装：[✓](https://github.com/zwxandy/MPCache) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）のKVキャッシュ圧縮は、通常のGPU推論では過去トークンの一部を削除・選択することで注意計算量とメモリを減らす。さらに粗いクラスタから細かいクラスタへ選択を絞り、近接Transformer層の選択インデックスを共有することで、MPC特有の比較と秘密インデックスgatherの費用を削減する。

- **2024-12 · [Batch-Max: Higher LLM Throughput using Larger Batch Sizes and KV Cache Compression](2024-2412.05693-batch-max-higher-llm-throughput-using-larger-batch-sizes-and-kv-cache-co.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存のKVキャッシュ削除は、長い入力プロンプトをすべて処理した後、生成段階のKVメモリや帯域を減らすことに主眼がある。プリフィルの全KVを一度保持しなければならないため、生成段階では大幅に圧縮していても、最初のプリフィル時のピークメモリがバッチサイズを制限する。

### 3年前（2023-11〜2024-10）

- **2024-06 · [SnapKV: LLM Knows What You are Looking for Before Generation](2024-2404.14469-snapkv.md)**  
  実装：[✓](https://github.com/FasterDecoding/SnapKV) ・ リポジトリ内被引用：461  
  プロンプト末尾の観測窓から各注意ヘッドが将来参照する位置を推定し、重要KVだけをクラスタ単位で残して長文復号を軽量化する手法。

- **2024-01 · [KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization](2024-2401.18079-kvquant.md)**  
  実装：[✓](https://github.com/SqueezeAILab/KVQuant) ・ リポジトリ内被引用：347  
  Key分布に合わせたチャネル別・RoPE前・非一様・外れ値分離量子化で、3ビットKVを約4.8倍圧縮しつつパープレキシティ悪化0.1未満を実現する。

- **2024-02 · [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](2024-2402.02750-kivi.md)**  
  実装：[✓](https://github.com/jy-yuan/KIVI) ・ リポジトリ内被引用：343  
  KIVIは、自己注意の鍵・値キャッシュ（KV キャッシュ）を追加学習なしで2ビットに圧縮する方式である。Llama-2-7Bを用いた単一A100 80GBの実機実験では、ピークメモリ（モデル重みを含む）が最大2.6分の1となり、同程度のメモリ上限で最大4倍のバッチを処理できる。

- **2024-05 · [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](2024-2405.04434-deepseek-v2-mla.md)**  
  実装：✓ ・ リポジトリ内被引用：336  
  通常の多頭注意（Multi-Head 注意機構; MHA）では、系列長が伸びるほどKVキャッシュが線形に増え、GPU高帯域メモリ（High Bandwidth メモリ; HBM）に置ける同時要求数や最大文脈長を圧迫する。

- **2024-06 · [PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling](2024-2406.02069-pyramidkv.md)**  
  実装：[✓](https://github.com/Zefan-Cai/PyramidKV) ・ リポジトリ内被引用：261  
  注意の層間集約パターンに合わせてKV予算を下層から上層へ逓減させ、同じ総メモリで固定予算型より長文脈性能を保つKVキャッシュ圧縮法。

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：161  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2024-10 · [DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads](2024-2410.10819-duoattention-efficient-long-context-llm-inference-with-retrieval-and-str.md)**  
  実装：[✓](https://github.com/mit-han-lab/duo-attention) ・ リポジトリ内被引用：145  
  デコード時には過去のKVを読み出すため遅延も長くなり、プリフィルでは注意計算が系列長の二乗に増える。DuoAttentionは、全ての注意ヘッドが遠距離の情報を必要とするわけではないという観測に基づき、ヘッドごとに全履歴を残すか、固定長の履歴だけ残すかを切り替える方式である。

- **2024-07 · [Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference](2024-2407.11550-ada-kv.md)**  
  実装：[✓](https://github.com/FFY0/AdaKV) ・ リポジトリ内被引用：141  
  注意ヘッドごとの集中度に応じて同一層内のKV保持予算を再配分し、既存Top-k圧縮の総容量を変えずに追い出し損失を下げる手法。

- **2024-03 · [GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM](2024-2403.05527-gear-an-efficient-kv-cache-compression-recipe-for-near-lossless-generati.md)**  
  実装：[✓](https://github.com/HaoKang-Timmy/GEAR) ・ リポジトリ内被引用：105  
  GEARは、自己回帰生成で増え続けるKVキャッシュを高い圧縮率で保持しつつ、単純な低ビット量子化で生じる生成品質の崩壊を抑えるための圧縮法である。

- **2024-05 · [MiniCache: KV Cache Compression in Depth Dimension for Large Language Models](2024-2405.14366-minicache-kv-cache-compression-in-depth-dimension-for-large-language-mod.md)**  
  実装：[✓](https://github.com/AkideLiu/MiniCache) ・ リポジトリ内被引用：96  
  MiniCacheは層内のトークン選別や低ビット化だけでなく、隣り合う層のあいだにも冗長性があると観察し、中層以降で同じ位置のKV状態を共有表現へ統合する。

- **2024-03 · [Jamba: A Hybrid Transformer-Mamba Language Model](2024-2403.19887-jamba-a-hybrid-transformer-mamba-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：79  
  系列が長くなると鍵値キャッシュ（KVキャッシュ）の容量と読出し量が増え、GPUのメモリ容量・帯域を圧迫する。さらに混合専門家モデル（Mixture-of-Experts、MoE）を一部の前向き全結合層へ導入し、総パラメータ容量とトークン当たりの有効計算量を分離する。

- **2024-10 · [MagicPIG: LSH Sampling for Efficient LLM Generation](2024-2410.16179-magicpig-lsh-sampling-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/MagicPIG) ・ リポジトリ内被引用：78  
  LSHの衝突確率を注意分布の提案分布として使い、CPUへ置いたKVから少数だけをサンプリングして疎注意を計算する方式。全注意の2〜5%程度の計算で精度を保ち、最大5倍のデコードスループットを示す。

- **2024-03 · [Keyformer: KV Cache reduction through key tokens selection for Efficient Generative Inference](2024-2403.09054-keyformer-kv-cache-reduction-through-key-tokens-selection-for-efficient-.md)**  
  実装：[✓](https://github.com/d-matrix-ai/keyformer-llm) ・ リポジトリ内被引用：67  
  Keyformerは、生成中に増え続ける鍵値キャッシュ（KVキャッシュ）を、重要な過去トークンだけへ圧縮する方式である。著者らは、注意重みの約90%が過去トークンの一部に集中するという観察から、すべての履歴を保持する必要はないと考える。

- **2024-02 · [No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization](2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-.md)**  
  実装：✓ ・ リポジトリ内被引用：65  
  自己回帰推論の鍵・値キャッシュ（KVキャッシュ）は、生成済みの各トークンの中間状態を再利用して再計算を避ける一方、必要容量が同時要求数と文脈長にほぼ比例して増える。提案する混合精度KVキャッシュ（MiKV）は、重要トークンを高精度で保持し、従来なら追い出すトークンも2〜4ビットで保存する。

- **2024-07 · [PQCache: Product Quantization-based KVCache for Long Context LLM Inference](2024-2407.12820-pqcache-product-quantization-based-kvcache-for-long-context-llm-inferenc.md)**  
  実装：[✓](https://github.com/HugoZHL/PQCache) ・ リポジトリ内被引用：60  
  文脈が長くなるほどKVキャッシュは大きくなり、GPUメモリへ収まらない場合にはCPUメモリへの退避と転送が必要になる。Llama-3.1-8Bの128K文脈を用いたInfiniteBenchでは、過去トークンの1/10だけを選択する条件で平均スコア46.80を報告し、比較方式に対する改善は+4.60%である。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：60  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：60  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。

- **2024-05 · [PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference](2024-2405.12532-pyramidinfer-pyramid-kv-cache-compression-for-high-throughput-llm-infere.md)**  
  実装：[✓](https://github.com/mutonix/pyramidinfer) ・ リポジトリ内被引用：60  
  PyramidInferは、大規模言語モデルの生成時にGPUメモリを占有するKVキャッシュを、層の深さに応じて段階的に減らす方式である。A100 80GBでのLLaMA 2-13B評価では、固定バッチ・固定長条件でKVメモリ24.2GBから11.0GB、スループット621から1389 トークン/sという結果を報告する。

- **2024-03 · [Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference](2024-2403.09636-dynamic-memory-compression-retrofitting-llms-for-accelerated-inference.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM/tree/DMC) ・ リポジトリ内被引用：59  
  動的メモリ圧縮（動的 メモリ Compression; DMC）は、過去トークンを「残す／捨てる」の二択にせず、各注意ヘッドが新しいキー・値（Key-Value; KV）を新規スロットへ追加するか、直前のスロットへ重み付きで結合するかを学習する。これにより、内容・層・ヘッドごとに必要な時間解像度を変えながらKVキャッシュをオンライン圧縮する。

- **2024-07 · [RazorAttention: Efficient KV Cache Compression Through Retrieval Heads](2024-2407.15891-razorattention-efficient-kv-cache-compression-through-retrieval-heads.md)**  
  実装：✓ ・ リポジトリ内被引用：58  
  RazorAttentionは、長い入力を処理する大規模言語モデルの鍵・値キャッシュ（KV キャッシュ）を、注意頭ごとの機能差に基づいて圧縮する手法である。原著の既定設定では、非検索頭に残す近傍長を max(4000,N/5)、系列先頭の保持数を4とし、誘導頭の上位14%と反復頭の上位1%を検索頭として保護する。

- **2024-05 · [ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification](2024-2405.14256-zipcache.md)**  
  実装：[✓](https://github.com/ThisisBillhe/ZipCache) ・ リポジトリ内被引用：57  
  ZipCacheは、長文脈推論で肥大化する鍵・値キャッシュ（KV キャッシュ）を、重要トークンの識別と混合精度量子化によって圧縮する手法である。そこでZipCacheは最近5%とランダム5%のプローブトークンの注意スコアだけを求め、残りのトークンは高速注意経路を維持する。

- **2024-07 · [Keep the Cost Down: A Review on Methods to Optimize LLM's KV Cache Consumption](2024-2407.18003-keep-the-cost-down-a-review-on-methods-to-optimize-llm-s-kv-cache-consum.md)**  
  実装：✓ ・ リポジトリ内被引用：53  
  本稿は、Luohe Shi、Hongyi Zhang、Yao Yao、Zuchao Li、Hai Zhaoによる鍵・値キャッシュ（Key-Value Cache、以下KVキャッシュ）の最適化手法に関する総説を、2024年11月20日の第4版を一次資料として再監査した解説である。

- **2024-10 · [Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning](2024-2410.19258-not-all-heads-matter-a-head-level-kv-cache-compression-method-with-integ.md)**  
  実装：[✓](https://github.com/FYYFU/HeadKV) ・ リポジトリ内被引用：50  
  従来の圧縮方式は、最近の注意得点を利用して残すトークンを選んだり、層ごとに予算を変えたりする。論文は文脈QAの代表条件で元キャッシュの約1.5%を保持しながら完全キャッシュ性能の97%を得たと報告するが、これは全タスク・全モデルで97%という保証ではない。

- **2024-02 · [Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference](2024-2402.09398-get-more-with-less-synthesizing-recurrence-with-kv-cache-compression-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/hdong920/LESS) ・ リポジトリ内被引用：50  
  LESSは、キー・値キャッシュ（Key-Value Cache; KVキャッシュ）の追い出しを「残すか捨てるか」の二択にしない。重要なトークンは従来どおり疎KVキャッシュへ明示的に残し、追い出すトークンは固定サイズの低ランク状態へ順次圧縮する。次の注意計算では両方を合成するため、疎キャッシュから消えたトークンにも低解像度ながら参照経路が残る。

- **2024-03 · [QAQ: Quality Adaptive Quantization for LLM KV Cache](2024-2403.04643-qaq-quality-adaptive-quantization-for-llm-kv-cache.md)**  
  実装：[✓](https://github.com/ClubieDong/KVCacheQuantization) ・ リポジトリ内被引用：49  
  QAQは、自己回帰型大規模言語モデルの鍵値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を、すべてのトークンで一律のビット幅にするのではなく、注意出力の誤差許容量に応じてキー（Key; K）と値（Value; V）を別々に量子化する方式である。

- **2024-05 · [KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization](2024-2405.03917-coupled-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：48  
  鍵値活性のチャネル間依存を利用して複数チャネルを共同量子化し、極低ビットでも品質劣化を抑える連結量子化を提案する。

- **2024-02 · [Hydragen: High-Throughput LLM Inference with Shared Prefixes](2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md)**  
  実装：[✓](https://github.com/jordan-benjamin/hydragen) ・ リポジトリ内被引用：48  
  共通のシステム指示、少数例の例示、同一問題に対する多数の候補生成などでは、異なる要求が接頭辞の鍵・値キャッシュを共有する。原著はCodeLlama-13Bを8枚のA100-40GBで実行し、大きなバッチと長い共有接頭辞でvLLMのページ注意に対して端点処理率最大32倍を報告する。

- **2024-02 · [GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding](2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：47  
  本論文は、大規模言語モデルの生成時に生じる逐次計算の待ち時間を、投機的復号（投機的復号）の二つの構成要素から短縮する研究である。投機的復号では軽量な下書きモデルが数トークンを先に提案し、大型の対象モデルが一度の前向き計算で提案を検証する。

- **2024-07 · [ThinK: Thinner Key Cache by Query-Driven Pruning](2024-2407.21018-think-thinner-key-cache-by-query-driven-pruning.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/ThinK) ・ リポジトリ内被引用：43  
  ThinKは、長文脈生成に必要な鍵・値キャッシュ（KVキャッシュ）のうち、鍵（Key）ベクトル内部のチャネルを選択的に削除する圧縮手法である。ICLR 2025の著者論文では、H2OやSnapKVへ40%のKeyチャネル削減を追加してもLongBenchの平均スコアがほぼ維持される例を示す。

- **2024-07 · [Model Tells You Where to Merge: Adaptive KV Cache Merging for LLMs on Long-Context Tasks](2024-2407.08454-model-tells-you-where-to-merge-adaptive-kv-cache-merging-for-llms-on-lon.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  既存のKV圧縮は、量子化で各要素のビット数を減らす、注意重要度の低いトークンを削除する、複数トークンを一つへ統合する、という三系統に分けられる。

- **2024-02 · [ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition](2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-t.md)**  
  実装：[✓](https://github.com/microsoft/chunk-attention) ・ リポジトリ内被引用：41  
  ChunkAttentionは、同じ言語モデルを複数の利用者・アプリケーションへ提供する際に、要求の先頭で共有されるシステム指示や少数例を計算と記憶の両面で再利用する推論用注意機構である。

- **2024-05 · [SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models](2024-2405.06219-skvq-sliding-window-key-and-value-cache-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/cat538/SKVQ) ・ リポジトリ内被引用：40  
  KVチャネルを量子化しやすい順へ並べ替え、外れ値をクリップし、直近KVだけ高精度で残すことで鍵2ビット・値1.5ビット級まで圧縮し、長文脈の容量・帯域律速を緩和する。

- **2024-03 · [ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching](2024-2403.17312-alisa-accelerating-large-language-model-inference-via-sparsity-aware-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  ALISAは、生成が進むほど増加する鍵・値キャッシュ（KVキャッシュ）の容量とCPU・GPU間転送が、単一GPUでの大規模言語モデル推論を妨げる問題を扱う。提案方式は三つの操作を組み合わせる。原著はOPT、LLaMA、Pythiaの6.7B～33B級を評価し、入力128・出力512トークンのAlpaca負荷で、80%のKV疎化を採用した際の処理量を比較する。

- **2024-02 · [WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More](2024-2402.12065-wkvquant-quantizing-weight-and-key-value-cache-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  WKVQuantは、大規模言語モデルの推論時に使うメモリを、モデル重み、鍵・値キャッシュ、一時活性化の三種類に分け、容量を長く占有する重みと鍵・値キャッシュだけを低ビット化する事後量子化（post-学習 量子化; PTQ）方式である。重みのみの量子化は比較的精度を維持しやすいが、長文脈・大バッチで増える鍵・値キャッシュを圧縮しない。

- **2024-08 · [Eigen Attention: Attention in Low-Rank Space for KV Cache Compression](2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md)**  
  実装：[✓](https://github.com/UtkarshSaxena1/EigenAttn) ・ リポジトリ内被引用：39  
  長い文脈を処理する言語モデルでは、生成時に過去のトークンの鍵と値を保存するKVキャッシュが、モデル重みと同程度かそれ以上のメモリを占めることがある。Eigen 注意機構は、保存するトークン数や一要素のビット幅を減らすのではなく、各トークンの鍵・値ベクトルの特徴次元を低ランク空間へ縮める。

- **2024-06 · [A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression](2024-2406.11430-l2-kv-compression.md)**  
  実装：[✓](https://github.com/alessiodevoto/l2compress) ・ リポジトリ内被引用：36  
  キーのL2ノルムと注意重みの逆相関を利用し、注意重みを計算せず重要KVを残す学習不要の圧縮法。FlashAttention互換のまま、長文検索では50〜90%のKV削減でも高精度を維持する。

- **2024-10 · [LoRC: Low-Rank Compression for LLMs KV Cache with a Progressive Compression Strategy](2024-2410.03111-lorc-low-rank-compression-for-llms-kv-cache-with-a-progressive-compression-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  自己回帰型の大規模言語モデル（LLM）は、過去トークンの鍵（K）と値（V）をKVキャッシュへ保存することで、次のトークン生成時に過去の注意計算をやり直さない。原著のメモリ表では、バッチ64、文脈長2048でLLaMA-2 13BのKVキャッシュが50GBから27.5GB、LLaMA-3 8Bが8GBから4.8GB、70Bが20GBから11GBになる。

- **2024-06 · [Attention Score is not All You Need for Token Importance Indicator in KV Cache Reduction: Value Also Matters](2024-2406.12335-attention-score-is-not-all-you-need-for-token-importance-indicator-in-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  注意スコアに値ベクトルのL1ノルムを組み込み、実際の注意出力寄与に近い重要度でKVトークンを削減する後付け型キャッシュ枝刈り。

- **2024-01 · [Long Context Compression with Activation Beacon](2024-2401.03462-long-context-compression-with-activation-beacon.md)**  
  実装：[✓](https://github.com/FlagOpen/FlagEmbedding) ・ リポジトリ内被引用：31  
  活性値 Beaconは、文章そのものを短く書き換えるのではなく、Transformerの各層に生じる鍵・値活性を、追加したビーコントークンの活性へ直接圧縮する。圧縮率を8倍にした128K文脈の実験では、非圧縮で同じデータにより微調整した比較モデルに対し、推論時間を約半分、KVキャッシュを約8分の1にした。

- **2024-08 · [NACL: A General and Effective KV Cache Eviction Framework for LLM at Inference Time](2024-2408.03675-nacl-a-general-and-effective-kv-cache-eviction-framework-for-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/Research/tree/master/NLP/ACL2024-NACL) ・ リポジトリ内被引用：29  
  KV追い出しで「これまで注意スコアが大きかったトークンを残す」だけでは、注意が先頭・直近位置へ偏るため、長文中央の重要情報を捨てやすい。NACLは、質問などタスク固有の代理トークン（proxy トークン）が入力全体へ向けた注意から重要度を作る決定論的な保持と、その重要度分布からヘッド・層ごとに異なるトークンを確率的に残す保持を混ぜる。

- **2024-10 · [KVSharer: Efficient Inference via Layer-Wise Dissimilar KV Cache Sharing](2024-2410.18517-kvsharer-efficient-inference-via-layer-wise-dissimilar-kv-cache-sharing.md)**  
  実装：[✓](https://github.com/yangyifei729/KVSharer) ・ リポジトリ内被引用：23  
  層ごとの鍵・値キャッシュを独立に保存する代わりに、一部の後段層で前段層のキャッシュを再利用する。直感に反して「KV表現が大きく異なる層対」から共有を試し、元モデルの最終隠れ状態を保てる組だけを採用する。

- **2024-10 · [MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection](2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md)**  
  実装：[✓](https://github.com/The-kamisato/MatryoshkaKV-cache) ・ リポジトリ内被引用：20  
  MatryoshkaKVは、事前学習済み大規模言語モデル（LLM）の鍵値キャッシュ（KVキャッシュ）について、トークン数や注意ヘッド数を減らす代わりに各ヘッドが保存する特徴次元を縮小する方式である。単純な主成分分析（PCA）による次元削減は中程度の圧縮では有効だが、元のキャッシュ容量の半分以下にすると生成品質が急落する。

- **2024-10 · [LayerKV: Optimizing Large Language Model Serving with Layer-wise KV Cache Management](2024-2410.00428-layerkv-optimizing-large-language-model-serving-with-layer-wise-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  LayerKVは、長い入力を受ける言語モデルのサービングで、初回トークンまでの時間（Time to First Token、TTFT）が急増する原因を新規要求がGPU上の鍵・値（KV）キャッシュ領域を確保できず待たされることに求めたシステムである。

- **2024-06 · [Effectively Compress KV Heads for LLM](2024-2406.07056-effectively-compress-kv-heads-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  本論文は、既に多頭注意（Multi-Head 注意機構; MHA）として学習済みの大規模言語モデルを、鍵・値（Key/Value; KV）のヘッド数が少ない構成へ後変換する研究である。LLaMA2-7BのKVヘッドを32から16へ半減すると、単一A100 80GBで復号速度が8.05から13.41トークン/秒へ増えた。

- **2024-02 · [On the Efficacy of Eviction Policy for Key-Value Constrained Generative Language Model Inference](2024-2402.06262-on-the-efficacy-of-eviction-policy-for-key-value-constrained-generative-language-model-inference.md)**  
  実装：[✓](https://github.com/DRSY/EasyKV) ・ リポジトリ内被引用：18  
  RoCoはKV トークンの重要度を累積注意機構ではなく平均注意機構で測り、注意機構標準偏差で追い出し候補を動的に選び、固定window依存を減らしながらfull-キャッシュに近い生成品質を保つ。

- **2023-12 · [Compressed Context Memory For Online Language Model Interaction](2023-2312.03414-compressed-context-memory-for-online-language-model-interaction.md)**  
  実装：[✓](https://github.com/snu-mllab/context-memory) ・ リポジトリ内被引用：18  
  オンライン対話、個人化推薦、複数課題の逐次学習では、要求を受けるたびに新しい文脈が追加される。Compressed Context メモリ（CCM）は、過去の鍵値キャッシュを、専用の圧縮トークンが生成する少数の鍵値へ繰り返し統合する。

- **2024-06 · [QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead](2024-2406.03482-qjl-1-bit-quantized-jl-transform-for-kv-cache-quantization-with-zero-ove.md)**  
  実装：[✓](https://github.com/amirzandieh/QJL) ・ リポジトリ内被引用：17  
  従来の低ビット量子化は、量子化された整数だけでなく、元の実数値へ戻すための尺度（scale）とゼロ点（zero point）をブロック単位で保持する。

- **2024-10 · [InfiniPot: Infinite Context Processing on Memory-Constrained LLMs](2024-2410.01518-infinipot-infinite-context-processing-on-memory-constrained-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  InfiniPotは、長い入力をすべて読み終わってから鍵・値キャッシュ（KVキャッシュ）を削減する方式ではなく、入力を読んでいる途中から固定容量内で何度も圧縮する長文脈処理の仕組みである。Mistral系の4K固定KV予算で最大100万トークンの検索実験も行ったが、「無限長でも全情報を損失なく保持する」ことを示したわけではない。

- **2024-04 · [SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget](2024-2404.04793-squeezeattention-2d-management-of-kv-cache-in-llm-inference-via-layer-wi.md)**  
  実装：[✓](https://github.com/hetailang/SqueezeAttention) ・ リポジトリ内被引用：16  
  SqueezeAttentionは、大規模言語モデルの推論で必要になる鍵・値キャッシュ（KVキャッシュ）を、系列中のトークン方向だけでなく、注意機構を構成する層の方向からも最適化する方式である。

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

- **2024-10 · [LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation](2024-2410.13846-lighttransfer-your-long-context-llm-is-secretly-a-hybrid-model-with-effo.md)**  
  実装：[✓](https://github.com/sail-sg/LightTrans) ・ リポジトリ内被引用：13  
  キャッシュがGPUメモリを圧迫すると、同時に処理できる要求数が減り、長文脈の生成処理量も低下する。ある層では先頭の少数トークン（注意機構 sink）と直近の窓だけに注意が集中する。

- **2024-10 · [Locret: Enhancing Eviction in Long-Context LLM Inference with Trained Retaining Heads on Consumer-Grade Devices](2024-2410.01805-locret-enhancing-eviction-in-long-context-llm-inference-with-trained-ret.md)**  
  実装：[✓](https://github.com/huangyuxiang03/Locret) ・ リポジトリ内被引用：11  
  Locretは、長文脈LLMの推論で大きくなるキー・バリューキャッシュ（KVキャッシュ）を、必要な情報だけ残して逐次削除する方式である。原著は、Phi-3-mini-128Kで最大20倍超、Llama-3.1-8B-instructで8倍超のKV圧縮を報告する。

- **2024-09 · [Small Language Models: Survey, Measurements, and Insights](2024-2409.15790-small-language-models-survey-measurements-and-insights.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/SLM_Survey) ・ リポジトリ内被引用：10  
  推論を高速化する新しいアルゴリズムを提案する論文ではない。同程度のパラメータ数でもQwen2-0.5Bの初回トークン時間はQwen1.5-0.5Bの1.46倍であり、Qwen1.5-0.5Bはパラメータが25.4%多いにもかかわらずJetson上では31.9%速い。

- **2024-09 · [Inf-MLLM: Efficient Streaming Inference of Multimodal Large Language Models on a Single GPU](2024-2409.09086-inf-mllm-efficient-streaming-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  著者らは注意得点の時間的な構造を観察し、直近トークンだけでなく、離れた過去にある重要トークンを固定容量キャッシュへ残す方法を提案する。

- **2024-06 · [Optimised Grouped-Query Attention Mechanism for Transformers](2024-2406.14963-optimised-grouped-query-attention-mechanism-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  既存の多頭注意（Multi-Head 注意機構、MHA）を、複数の質問ヘッドで鍵・値ヘッドを共有するグループ化質問注意（Grouped-Query 注意機構、GQA）へ変換すると、復号時に保存する鍵値キャッシュと鍵値投影のパラメータを減らせる。

- **2024-09 · [KVPruner: Structural Pruning for Faster and Memory-Efficient Large Language Models](2024-2409.11057-kvpruner-structural-pruning-for-faster-and-memory-efficient-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KVPrunerは、長い入力や複数の同時要求で増大する鍵・値キャッシュを、事前にモデルの注意チャネルを削除することで小さくする手法である。原著のLLaMA-7B実験では、鍵・値チャネルを50%削減した構成で鍵・値保存量が8GBから4GB、モデルパラメータ数が7Bから5.5Bになる。

- **2024-10 · [Exploring CXL-based KV Cache Storage for LLM Serving](2024-fcda582bb2a7-exploring-cxl-based-kv-cache-storage-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CPUの主記憶へ退避しても、複数の長文脈要求を保持するには容量が足りなくなる可能性がある。

- **2024-09 · [CSKV: Training-Efficient Channel Shrinking for KV Cache in Long-Context Scenarios](2024-2409.10593-cskv-training-efficient-channel-shrinking-for-kv-cache-in-long-context-s.md)**  
  実装：[✓](https://github.com/wln20/CSKV) ・ リポジトリ内被引用：1  
  過去トークンの表現を毎回計算し直さずに済む一方、保存容量は文脈長にほぼ比例して増え、長い文書の読解や検索でGPUメモリを圧迫する。量子化は保存ビット数を減らすが、高圧縮では誤差が増える。LongChat-7B-v1.5-32kでは80%のKV容量圧縮時、LongEvalの10K検索正答率が無圧縮0.98に対してCSKV0.90となる。

- **2024-06 · [Training-Free Exponential Context Extension via Cascading KV Cache](2024-2406.17808-training-free-exponential-context-extension-via-cascading-kv-cache.md)**  
  実装：[✓](https://github.com/jeffwillette/cascading_kv_cache) ・ リポジトリ内被引用：1  
  固定長の滑動窓（sliding window）を使えばメモリを抑えられるが、窓から出た過去のトークンは消え、長距離の依存関係を復元できない。StreamingLLMは冒頭の注意シンク（注意機構 sinks）を残して安定性を高めるものの、冒頭以外の過去トークンは一定の年齢になると削除する。

- **2024-07 · [QET: Enhancing Quantized LLM Parameters and KV Cache Compression through Element Substitution and Residual Clustering](2024-2407.03637-qet-enhancing-quantized-llm-parameters-and-kv-cache-compression-through-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Quantum Entanglement Trees（QET）は、量子コンピュータを用いる方式ではない。主要実験では圧縮比4のLLaMA2重み行列のMSEをPQの5.05%、KキャッシュのMSEを13.33%、VキャッシュのMSEを11.89%に減らしたと報告する。

- **2024-07 · [Let the Code LLM Edit Itself When You Edit the Code](2024-2407.03157-let-the-code-llm-edit-itself-when-you-edit-the-code.md)**  
  実装：[✓](https://github.com/zhenyuhe00/PIE) ・ リポジトリ内被引用：0  
  本研究は、開発者が既存コードの途中に行を挿入・削除した直後に、コード補完用の大規模言語モデル（LLM）が次の行を予測し直す場面を対象とする。

- **2024-03 · [Hierarchical and Dynamic Prompt Compression for Efficient Zero-shot API Usage](2024-60b566817f9b-hierarchical-and-dynamic-prompt-compression-for-efficient-zero-shot-api-.md)**  
  実装：[✓](https://github.com/jiangycTarheel/HD-Gist) ・ リポジトリ内被引用：0  
  従来のgist トークン方式は文書を固定個数の特殊トークンの隠れ状態へ圧縮できるが、API呼出しのように細かい引数名・値の正確さが必要なタスクでは情報が失われ、圧縮前より大きく精度が低下する。

### 4年前（2022-11〜2023-10）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：687  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。

- **2023-06 · [H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models](2023-2306.14048-h2o.md)**  
  実装：[✓](https://github.com/FMInference/H2O) ・ リポジトリ内被引用：654  
  累積注意のヘビーヒッターと最新トークンを動的保持し、20%程度のKV予算で品質を維持しながらメモリ・スループットを改善する。

- **2023-05 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-2305.13245-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：401  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各クエリ頭に独立した鍵頭と値頭を持つため、復号時には全KV頭のキャッシュを読み出す必要がある。

- **2023-10 · [Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs](2023-2310.01801-fastgen.md)**  
  実装：[✓](https://github.com/machilusZ/FastGen) ・ リポジトリ内被引用：262  
  FastGenは注意ヘッドごとの構造を一度だけ診断してKVキャッシュ保持方針を変え、追加学習なしでメモリ削減と長系列生成の高速化を両立する。

- **2023-05 · [Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time](2023-2305.17118-scissorhands.md)**  
  実装：✓ ・ リポジトリ内被引用：237  
  Scissorhandsは、過去の注意重みが大きかったトークンは将来の生成でも高い注意を受けやすいという「重要性の持続性仮説（Persistence of Importance Hypothesis）」を提案する。

- **2023-06 · [Augmenting Language Models with Long-Term Memory](2023-2306.07174-augmenting-language-models-with-long-term-memory.md)**  
  実装：[✓](https://github.com/Victorwz/LongMem) ・ リポジトリ内被引用：10  
  過去のキー・値（KV）を外部バンクへ保持して必要な箇所だけ取り出す方式は有望だが、モデルを学習しながら記憶を書き込むと、古いモデルが生成した記憶表現と現在のモデルの表現が食い違う問題が生じる。

### 7年前（2019-11〜2020-10）

- **2019-11 · [Fast Transformer Decoding: One Write-Head is All You Need](2019-1911.02150-multi-query-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：267  
  複数問い合わせ注意（Multi-Query 注意機構; MQA）は、問い合わせ側の8ヘッドを維持したまま、鍵と値だけを全ヘッドで1組へ共有する。長い履歴を毎生成ステップで読む増分復号のメモリ転送を減らし、TPUv2でのWMT英独翻訳のデコーダ測定を46から3.8マイクロ秒／出力トークンへ短縮した。
<!-- survey:auto:end -->
