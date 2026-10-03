# Sparse Attention

長文脈LLMで全KVへ密に注意を計算せず、重要token・block・page・routeだけを選択してattention演算量とメモリ帯域を減らす疎注意方式をまとめる。

## 分類境界

主要貢献がattention対象token/block/pageの選択、疎なquery-key接続、top-k/route型attention計算削減である論文を含め、KVの圧縮・退避・量子化だけでattention接続を疎化しない研究は含めない。

### 含める研究

- token/block/page選択型の疎attention
- top-k・threshold・route型attention
- 長文脈向けattention計算削減

### 含めない研究

- KV cache圧縮だけを主題とする研究
- KV offloadだけでattention自体は密な研究

## 近傍系統

- [07-kv-cache-optimization-compression](../07-kv-cache-optimization-compression/)
- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（42本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [GLM-5: from Vibe Coding to Agentic Engineering](2026-2602.15763-glm-5-from-vibe-coding-to-agentic-engineering.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  そこでモデルは混合専門家（MoE）構成に加えてDeepSeek Sparse 注意機構（DSA）を採用し、長文脈で参照するキー・値を絞る。

- **2026-03 · [IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse](2026-2603.12201-indexcache-cross-layer-index-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  各層で繰り返す疎注意のトークン選択を一部の層だけで計算し、後続層に再利用する。30B DSAモデルの200K文脈でインデクサ計算を75%削減し、プリフィルを1.82倍、デコードを1.48倍高速化した。

- **2025-12 · [Kascade: A Practical Sparse Attention Method for Long-Context LLM Inference](2025-2512.16391-kascade-a-practical-sparse-attention-method-for-long-context-inference.md)**  
  実装：[✓](https://github.com/microsoft/kascade) ・ リポジトリ内被引用：4  
  長文脈の注意を10%だけ計算すれば理論上は大きく速くなるが、「どの10%を残すか」を毎層正確に探す処理が高い。Kascadeは、高い注意重みを持つキー集合が近接層でかなり似るという性質を利用し、少数のアンカー層だけでTop-k探索をやり直す。残りの層ではそのインデックスを再利用するため、疎化の選択費用を層間で償却できる。

- **2026-07 · [Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling](2026-2607.0298-hierarchical-sparse-attention-done-right-toward-infinite-context-modelin.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/HiLS-Attention) ・ リポジトリ内被引用：2  
  チャンク注意質量を学習可能なlandmark要約で近似し、検索スコアを階層softmaxへ直接組み込んで、疎注意の選択精度と超長文脈推論効率を両立する。

- **2026-07 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2026-delta.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：2  
  少数の更新層で重要KVページを動的に選び、後続層がその集合を再利用することで、完全なKV保持と推論精度を維持しつつ長文デコードを高速化する疎注意方式。

- **2026-06 · [MiniMax Sparse Attention](2026-2606.13392-minimax-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  索引分岐でGQAグループ別にKVブロックを選び、専用GPUカーネルと組み合わせて1M文脈の注意計算28.4倍削減、H800でプリフィル14.2倍・デコード7.6倍高速化。

- **2026-03 · [FlashPrefill: Instantaneous Pattern Discovery and Thresholding for Ultra-Fast Long-Context Prefilling](2026-2603.06199-flashprefill-instantaneous-pattern-discovery-and-thresholding-for-ultra-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  注意パターンを高速ブロック検索し、並べ替え不要の動的しきい値で疎化することで、プリフィルを256Kで最大27.78倍、4Kでも1.71倍高速化。

- **2026-06 · [SparDA: Sparse Decoupled Attention for Efficient Long-Context LLM Inference](2026-2606.04511-sparda.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  疎注意は実際に参照するKVだけを減らせるが、全KVキャッシュ容量は文脈長に比例して増え、GPUからCPUへ退避するとPCIe転送が律速になる。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [SANTA++: Sampling Attention through Representative Keys](2026-2609.35629-santa-sampling-attention-through-representative-keys.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全キー走査を避け、代表キーでチームを確率選択して包含確率補正する学習不要疎注意。32K文脈でKV読み出し16〜22%に抑え、Triton実装はFlash SDPA比1.69倍高速。

- **2026-09 · [RouteRelay: Event-Triggered Cross-Layer Route Reuse for Efficient Dynamic Sparse Attention](2026-2609.07306-routerelay-cross-layer-route-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意の前層経路IDを監視候補付きで再利用し、変化した行だけ再ルーティングして経路スコア計算を約38～52%へ削減するが、現CPU実装は未融合処理で逆に低速。

- **2026-09 · [RBS-Attention: Radius-Bounded Sparse Prefill for Long-Context Large Language Models](2026-2609.20971-rbs-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RBS-注意機構は、長文脈の前処理注意で重要なトークンを含むブロックを安価に選び、不要なブロック間注意を省く訓練不要方式である。H100上のQwen3-30B-A3B-Instruct-2507-FP8、128K文脈では、単体の前処理注意を20.65倍、vLLM内の前処理注意を11.92倍、エンドツーエンドの初回トークン到達時間を5.97倍高速化した。

- **2026-09 · [On-Demand Attention: Language Models Know When to Recall](2026-2609.20734-on-demand-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成中の多くの位置では直近文脈だけで次トークンを決められるにもかかわらず、数万から十数万トークンの履歴を毎回読むため、注意計算とHBM帯域の費用が増える。按需注意（On-Demand 注意機構; ODA）は、まず安価な局所注意を実行し、その結果と直前状態から「この段階で全注意を使う利益」を軽量な想起ヘッドで予測する。

- **2026-08 · [Self-Indexing Attention for Compression-Compatible Sparse Long-Context LLM Inference](2026-2609.13205-self-indexing-attention-for-compression-compatible-sparse-long-context-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  変換領域keyの符号1-bitをプリフィル・デコード共通の自己索引として使い、追加indexerなしで疎注意検索と低ビットKV圧縮を同居させる。

- **2026-07 · [RIS-Kernel: A Model-Agnostic Architecture for Long-Context LLM Inference via Sparse Attention](2026-2607.21927-ris-kernel-a-model-agnostic-architecture-for-long-context-llm-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特徴は単一の決定的疎パターンだけに依存せず、確率的サンプリングを複数シードで繰り返して予測を統合する点にある。

- **2026-04 · [HieraSparse: Hierarchical Semi-Structured Sparse KV Attention](2026-2604.16864-hierasparse.md)**  
  実装：[✓](https://github.com/psl-ntu/HieraSparse) ・ リポジトリ内被引用：0  
  HieraSparseは、長文脈推論で自己注意計算とKVキャッシュ容量が増大する問題に対し、KVを密ブロックとN:M半構造化疎ブロックへ分け、GPUの疎テンソルコアで直接処理する方式である。NVIDIA L40S実機では、同じ疎性のMUSTAFARに対して最大1.2倍高いKV圧縮率と4.57倍の注意カーネル高速化を示す。

### 2年前（2024-11〜2025-10）

- **2025-02 · [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](2025-2502.11089-native-sparse-attention-hardware-aligned-and-natively-trainable-sparse-a.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  完全注意は文脈長に対して二乗の注意機構計算を必要とし、長文脈では事前充填だけでなく復号時のKV読出し量も大きくなる。64K文脈では完全注意に対し順伝播最大9.0倍、逆伝播最大6.0倍、デコード最大11.6倍を報告し、品質も完全注意と同等以上を示す。

- **2025-02 · [MoBA: Mixture of Block Attention for Long-Context LLMs](2025-2502.13189-moba.md)**  
  実装：[✓](https://github.com/MoonshotAI/MoBA) ・ リポジトリ内被引用：22  
  MoBAは各問い合わせが関連KVブロックを動的選択するMoE型疎注意で、1M文脈の品質を完全注意に近く保ちつつ注意層前処理を最大6.5倍高速化する。

- **2025-02 · [FlexPrefill: A Context-Aware Sparse Attention Mechanism for Efficient Long-Sequence Inference](2025-2502.20766-flexprefill-a-context-aware-sparse-attention-mechanism-for-efficient-long-context-inference.md)**  
  実装：[✓](https://github.com/bytedance/FlexPrefill) ・ リポジトリ内被引用：10  
  要点: FlexPrefillは、長文プリフィルの注意計算を一律の疎パターンへ置き換えるのではなく、入力と注意ヘッドごとに「クエリごとに見る場所が違う多様型」か「多くのクエリが似た場所を見る構造型」かを判定し、その型に合う索引だけを累積注意量の閾値まで選ぶ。これにより、必要なヘッドには多く、簡単なヘッドには少ない計算予算を割り当てる。

- **2024-12 · [SCBench: A KV Cache-Centric Analysis of Long-Context Methods](2024-2412.10319-scbench-a-kv-cache-centric-analysis-of-long-context-methods.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  共有長文脈を複数ターンで再利用する12タスクを用い、KV生成・圧縮・検索・読み込みの各方式が初回だけでなく後続要求でどう崩れるかを比較する。

- **2025-02 · [Twilight: Adaptive Attention Sparsity with Hierarchical Top-p Pruning](2025-2502.02770-twilight-adaptive-attention-sparsity-with-hierarchical-top-p-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  長文脈復号では、過去トークンのKey/Value（KV）キャッシュを毎ステップ参照するため、文脈長とともにメモリ読出し量が増える。疎注意は全KVを読む代わりに重要トークンだけを選ぶが、多くの方式は「上位k件」という固定予算を使う。

- **2025-02 · [Tactic: Adaptive Sparse Attention with Clustering and Distribution Fitting for Long-Context LLMs](2025-2502.12216-tactic-adaptive-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  累積注意質量を目標にKV数を動的決定し、K-meansと分布当てはめで選択費用を抑えて注意を最大7.29倍高速化するTactic。

- **2025-07 · [RefreshKV: Updating Small KV Cache During Long-form Generation](2025-a2b748353aae-refreshkv-updating-small-kv-cache-during-long-form-generation.md)**  
  実装：[✓](https://github.com/carriex/refreshkv) ・ リポジトリ内被引用：4  
  完全KVを保持したまま通常は小さな部分KVへ注意し、クエリ類似度低下時だけ完全注意して重要トークン集合を更新することで長文生成の固定削除失敗を避ける。

- **2025-06 · [SeerAttention-R: Sparse Attention Adaptation for Long Reasoning](2025-2506.08889-seerattention-r-sparse-attention-adaptation-for-long-reasoning.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：4  
  思考連鎖が1万トークンを超える推論モデルでは、1トークン生成するたび全過去KVを読む注意が重くなる。SeerAttention-Rは、元モデルを変えずに小さなゲートだけを学習し、「今回のクエリが見るべきKVブロック」を予測してデコード注意を疎化する。

- **2024-11 · [Squeezed Attention: Accelerating Long Context Length LLM Inference](2024-2411.09688-squeezed-attention-accelerating-long-context-length-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  固定長文脈のキーをオフラインで意味クラスタ化し、実行時クエリに関連するクラスタの元KVだけを読み込んで正確な注意を計算し、長文脈の帯域と演算を削減する。

- **2025-09 · [InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation](2025-2509.24663-infllm-v2-dense-sparse-switchable-attention-for-seamless-short-to-long-a.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  密注意のK/V射影を再利用し、短文脈は密、長文脈はパラメータ追加なしのブロック疎注意へ切替えて、長文脈性能をほぼ保ちながら実推論を高速化する。

- **2025-04 · [MMInference: Accelerating Pre-filling for Long-Context VLMs via Modality-Aware Permutation Sparse Attention](2025-2504.16083-mminference-accelerating-pre-filling-for-long-context-vlms-via-modality-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  長動画や画像列を扱う視覚言語モデル（Vision-Language モデル; VLM）では、最初の出力を生成する前のプリフィルで全入力トークン間の注意を計算するため、入力長が100万トークン級になると二乗計算量が支配的になる。テキストLLM向け疎注意をそのまま使うと、動画トークンの時空間構造や、テキストと映像の境界で注意パターンが変わる性質を取り逃す。

- **2025-07 · [Compactor: Calibrated Query-Agnostic KV Cache Compression with Approximate Leverage Scores](2025-2507.08143-compactor-calibrated-query-agnostic-kv-cache-compression-with-approximat.md)**  
  実装：[✓](https://github.com/vnchari/compactor-vllm) ・ リポジトリ内被引用：2  
  近似レバレッジスコアで質問非依存にKVを選別し、文脈別の圧縮耐性を校正してLongBenchで完全KV相当の性能を保ちながら平均68%のKVメモリを削減する。

- **2025-02 · [Top-Theta Attention: Sparsifying Transformers by Compensated Thresholding](2025-2502.08363-top-theta-attention.md)**  
  実装：[✓](https://github.com/huawei-csl/top-theta-attention) ・ リポジトリ内被引用：0  
  Top-Thetaは層・ヘッド・位置別の校正しきい値で注意重みを選び、行ごとの上位k選択（top-k）を避けて注意計算とV行読出しを減らす。LLaMA系評価では注意要素やV読出しを最大10分の1程度まで減らす条件を示す一方、強い疎化や実装条件によって品質・実速度の利得が変わる。

### 3年前（2023-11〜2024-10）

- **2024-06 · [Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference](2024-2406.10774-quest.md)**  
  実装：[✓](https://github.com/mit-han-lab/Quest) ・ リポジトリ内被引用：95  
  KVページのキー最小・最大値と現在クエリから重要度上界を推定し、上位ページだけを読むことで全KVを保持したまま長文脈注意の帯域を削減し最大7.03倍高速化。

- **2024-07 · [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](2024-2407.02490-minference.md)**  
  実装：[✓](https://github.com/microsoft/MInference) ・ リポジトリ内被引用：53  
  注意ヘッドを3種の疎パターンへ割り当て、入力ごとの重要位置を動的推定して長文脈プリフィルを専用GPUカーネルで高速化する。

- **2024-10 · [SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs](2024-2410.13276-seerattention.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：16  
  Q/Kからブロック単位の重要度を学習する軽量ゲートとブロック疎FlashAttentionを組み合わせ、長文プリフィルの注意計算を動的に削減する。

- **2024-08 · [Post-Training Sparse Attention with Double Sparsity](2024-2408.07092-post-training-sparse-attention-with-double-sparsity.md)**  
  実装：[✓](https://github.com/andy-yang-1/DoubleSparse) ・ リポジトリ内被引用：12  
  重要トークン選択自体を重要チャネルだけで近似し、選ばれた完全KVだけを読む二重疎性で、長文脈デコードのKV帯域とGPU容量を同時に削る。

- **2024-06 · [Loki: Low-Rank Keys for Efficient Sparse Attention](2024-2406.02542-loki-low-rank-keys-for-efficient-sparse-attention.md)**  
  実装：[✓](https://github.com/hpcgroup/loki) ・ リポジトリ内被引用：11  
  キーの低ランク性を使い、低次元スコアで候補KVを選んでから全次元注意を計算し、品質を保ちながら注意計算を最大約45%短縮する疎注意法。

- **2024-06 · [Mixture of Attention Spans: Optimizing LLM Inference Efficiency with Heterogeneous Sliding-Window Lengths](2024-2406.14909-mixture-of-attention-spans-optimizing-llm-inference-efficiency-with-heterogeneous-sliding-window-lengths.md)**  
  実装：[✓](https://github.com/thu-nics/MoA) ・ リポジトリ内被引用：9  
  headごとの局所性と入力長への伸び方を勾配で測り、異種sliding-window規則を自動探索して静的KV maskへ落とすMoA。

- **2024-09 · [Block-Attention for Efficient Prefilling](2024-2409.15355-block-attention-for-efficient-prefilling.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Block-Attention) ・ リポジトリ内被引用：5  
  検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した各文書を互いに独立した注意ブロックとして事前計算し、同じ文書が別質問で再利用されたらKVキャッシュを再計算しない。

- **2024-10 · [TidalDecode: Fast and Accurate LLM Decoding with Position Persistent Sparse Attention](2024-2410.05076-tidaldecode-fast-and-accurate-llm-decoding-with-position-persistent-spar.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  系列長に比例してKVが増えるため、演算量だけでなく高帯域メモリからの読み出しが支配的になる。選択型疎注意は重要トークンだけを読むが、従来方式では各層で重要度を推定し直す費用と、近似選択の誤りが問題になる。

### 4年前（2022-11〜2023-10）

- **2023-05 · [Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers](2023-2305.15805-dynamic-context-pruning-for-efficient-and-interpretable-autoregressive-transformers.md)**  
  実装：[✓](https://github.com/sanagno/adaptively_sparse_attention) ・ リポジトリ内被引用：6  
  動的 Context 枝刈りは、生成の途中で「今後のトークンが参照する価値が低い」と学習した過去トークンを、注意対象とキー・バリュー（Key-Value; KV）キャッシュから動的に削除する。固定窓のように距離だけで落とさず、層ごとの学習可能な相互作用スコアで削除時点を決める。

- **2023-10 · [HyperAttention: Long-context Attention in Near-Linear Time](2023-2310.05869-hyperattention-long-context-attention-in-near-linear-time.md)**  
  実装：[✓](https://github.com/insuhan/hyper-attn) ・ リポジトリ内被引用：4  
  HyperAttentionは、softmax注意行列を全要素計算する代わりに、局所性鋭敏ハッシュ（Locality-Sensitive Hashing; LSH）で非常に大きな注意要素を先に見つけ、残りをサンプリングして近似する。

### 6年前（2020-11〜2021-10）

- **2020-12 · [SpAtten: Efficient Sparse Attention Architecture with Cascade Token and Head Pruning](2020-2012.09852-spatten-efficient-sparse-attention-architecture-with-cascade-token-and-head-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  累積注意確率とヘッド出力から重要トークン・ヘッドを動的にカスケード枝刈りし、確率分布に応じた段階的量子化と専用top-k回路で注意の計算・DRAM転送を同時に削減する。

- **2021-06 · [Memory-efficient Transformers via Top-k Attention](2021-2106.06899-top-k-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  通常注意は系列長をLとするとL×Lのスコア行列を作るため、長系列ではメモリ使用量が二次的に増える。Top-k 注意機構は、各クエリについて全キーとのスコアから上位k個だけを残し、クエリをチャンク単位で処理することでピークメモリを系列長に対して線形へ近づける。

### 7年前（2019-11〜2020-10）

- **2020-07 · [Big Bird: Transformers for Longer Sequences](2020-2007.14062-big-bird-transformers-for-longer-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  標準Transformerの自己注意は、長さnの系列で全トークン対の注意得点を作るため、計算・メモリが概ねn²で増える。長文書、複数段落QA、ゲノム配列では入力長を増やしたくても、注意行列がGPUメモリを急速に消費する。1トークン当たりの接続数を系列長に対して定数に保つことで、注意の計算・メモリ依存を線形へ落とす。

- **2020-03 · [Efficient Content-Based Sparse Attention with Routing Transformers](2020-2003.05997-efficient-content-based-sparse-attention-with-routing-transformers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/routing_transformer) ・ リポジトリ内被引用：5  
  固定した近傍窓ではなく「内容が近いトークン」をクラスタリングして注意先を決める。局所注意だけでは拾いにくい遠距離依存を残しつつ、各トークンが全系列を見る密な自己注意の二乗コストを削る、初期の内容依存疎注意方式。
<!-- survey:auto:end -->
