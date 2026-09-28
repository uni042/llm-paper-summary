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
## 自動生成の論文一覧（22本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse](2026-2603.12201-indexcache-cross-layer-index-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  各層で繰り返す疎注意のトークン選択を一部の層だけで計算し、後続層に再利用する。30B DSAモデルの200K文脈でインデクサ計算を75%削減し、プリフィルを1.82倍、デコードを1.48倍高速化した。

- **2025-12 · [Kascade: A Practical Sparse Attention Method for Long-Context LLM Inference](2025-2512.16391-kascade-a-practical-sparse-attention-method-for-long-context-inference.md)**  
  実装：[✓](https://github.com/microsoft/kascade) ・ リポジトリ内被引用：4  
  長文脈の注意を10%だけ計算すれば理論上は大きく速くなるが、「どの10%を残すか」を毎層正確に探す処理が高い。Kascadeは、高い注意重みを持つキー集合が近接層でかなり似るという性質を利用し、少数のアンカー層だけでTop-k探索をやり直す。残りの層ではそのインデックスを再利用するため、疎化の選択費用を層間で償却できる。

- **2026-07 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2026-delta.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：2  
  少数の更新層で重要KVページを動的に選び、後続層がその集合を再利用することで、完全なKV保持と推論精度を維持しつつ長文デコードを高速化する疎注意方式。

- **2026-06 · [SparDA: Sparse Decoupled Attention for Efficient Long-Context LLM Inference](2026-2606.04511-sparda.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  疎注意は実際に参照するKVだけを減らせるが、全KVキャッシュ容量は文脈長に比例して増え、GPUからCPUへ退避するとPCIe転送が律速になる。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [RouteRelay: Event-Triggered Cross-Layer Route Reuse for Efficient Dynamic Sparse Attention](2026-2609.07306-routerelay-cross-layer-route-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意の前層経路IDを監視候補付きで再利用し、変化した行だけ再ルーティングして経路スコア計算を約38～52%へ削減するが、現CPU実装は未融合処理で逆に低速。

- **2026-09 · [RBS-Attention: Radius-Bounded Sparse Prefill for Long-Context Large Language Models](2026-2609.20971-rbs-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RBS-注意機構は、長文脈の前処理注意で重要なトークンを含むブロックを安価に選び、不要なブロック間注意を省く訓練不要方式である。H100上のQwen3-30B-A3B-Instruct-2507-FP8、128K文脈では、単体の前処理注意を20.65倍、vLLM内の前処理注意を11.92倍、エンドツーエンドの初回トークン到達時間を5.97倍高速化した。

- **2026-09 · [On-Demand Attention: Language Models Know When to Recall](2026-2609.20734-on-demand-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成中の多くの位置では直近文脈だけで次トークンを決められるにもかかわらず、数万から十数万トークンの履歴を毎回読むため、注意計算とHBM帯域の費用が増える。按需注意（On-Demand 注意機構; ODA）は、まず安価な局所注意を実行し、その結果と直前状態から「この段階で全注意を使う利益」を軽量な想起ヘッドで予測する。

- **2026-04 · [HieraSparse: Hierarchical Semi-Structured Sparse KV Attention](2026-2604.16864-hierasparse.md)**  
  実装：[✓](https://github.com/psl-ntu/HieraSparse) ・ リポジトリ内被引用：0  
  HieraSparseは、長文脈推論で自己注意計算とKVキャッシュ容量が増大する問題に対し、KVを密ブロックとN:M半構造化疎ブロックへ分け、GPUの疎テンソルコアで直接処理する方式である。NVIDIA L40S実機では、同じ疎性のMUSTAFARに対して最大1.2倍高いKV圧縮率と4.57倍の注意カーネル高速化を示す。

### 2年前（2024-10〜2025-09）

- **2025-02 · [MoBA: Mixture of Block Attention for Long-Context LLMs](2025-2502.13189-moba.md)**  
  実装：[✓](https://github.com/MoonshotAI/MoBA) ・ リポジトリ内被引用：13  
  MoBAは各問い合わせが関連KVブロックを動的選択するMoE型疎注意で、1M文脈の品質を完全注意に近く保ちつつ注意層前処理を最大6.5倍高速化する。

- **2024-10 · [SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs](2024-2410.13276-seerattention.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：13  
  Q/Kからブロック単位の重要度を学習する軽量ゲートとブロック疎FlashAttentionを組み合わせ、長文プリフィルの注意計算を動的に削減する。

- **2025-02 · [FlexPrefill: A Context-Aware Sparse Attention Mechanism for Efficient Long-Sequence Inference](2025-2502.20766-flexprefill-a-context-aware-sparse-attention-mechanism-for-efficient-long-context-inference.md)**  
  実装：[✓](https://github.com/bytedance/FlexPrefill) ・ リポジトリ内被引用：6  
  要点: FlexPrefillは、長文プリフィルの注意計算を一律の疎パターンへ置き換えるのではなく、入力と注意ヘッドごとに「クエリごとに見る場所が違う多様型」か「多くのクエリが似た場所を見る構造型」かを判定し、その型に合う索引だけを累積注意量の閾値まで選ぶ。これにより、必要なヘッドには多く、簡単なヘッドには少ない計算予算を割り当てる。

- **2025-06 · [SeerAttention-R: Sparse Attention Adaptation for Long Reasoning](2025-2506.08889-seerattention-r-sparse-attention-adaptation-for-long-reasoning.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：4  
  思考連鎖が1万トークンを超える推論モデルでは、1トークン生成するたび全過去KVを読む注意が重くなる。SeerAttention-Rは、元モデルを変えずに小さなゲートだけを学習し、「今回のクエリが見るべきKVブロック」を予測してデコード注意を疎化する。

- **2025-02 · [Tactic: Adaptive Sparse Attention with Clustering and Distribution Fitting for Long-Context LLMs](2025-2502.12216-tactic-adaptive-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  累積注意質量を目標にKV数を動的決定し、K-meansと分布当てはめで選択費用を抑えて注意を最大7.29倍高速化するTactic。

- **2025-02 · [Top-Theta Attention: Sparsifying Transformers by Compensated Thresholding](2025-2502.08363-top-theta-attention.md)**  
  実装：[✓](https://github.com/huawei-csl/top-theta-attention) ・ リポジトリ内被引用：0  
  Top-Thetaは層・ヘッド・位置別の校正しきい値で注意重みを選び、行ごとの上位k選択（top-k）を避けて注意計算とV行読出しを減らす。LLaMA系評価では注意要素やV読出しを最大10分の1程度まで減らす条件を示す一方、強い疎化や実装条件によって品質・実速度の利得が変わる。

### 3年前（2023-10〜2024-09）

- **2024-06 · [Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference](2024-2406.10774-quest.md)**  
  実装：[✓](https://github.com/mit-han-lab/Quest) ・ リポジトリ内被引用：67  
  KVページのキー最小・最大値と現在クエリから重要度上界を推定し、上位ページだけを読むことで全KVを保持したまま長文脈注意の帯域を削減し最大7.03倍高速化。

- **2024-07 · [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](2024-2407.02490-minference.md)**  
  実装：[✓](https://github.com/microsoft/MInference) ・ リポジトリ内被引用：36  
  注意ヘッドを3種の疎パターンへ割り当て、入力ごとの重要位置を動的推定して長文脈プリフィルを専用GPUカーネルで高速化する。

- **2024-09 · [Block-Attention for Efficient Prefilling](2024-2409.15355-block-attention-for-efficient-prefilling.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Block-Attention) ・ リポジトリ内被引用：4  
  検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した各文書を互いに独立した注意ブロックとして事前計算し、同じ文書が別質問で再利用されたらKVキャッシュを再計算しない。

- **2024-06 · [Mixture of Attention Spans: Optimizing LLM Inference Efficiency with Heterogeneous Sliding-Window Lengths](2024-2406.14909-mixture-of-attention-spans-optimizing-llm-inference-efficiency-with-heterogeneous-sliding-window-lengths.md)**  
  実装：[✓](https://github.com/thu-nics/MoA) ・ リポジトリ内被引用：4  
  headごとの局所性と入力長への伸び方を勾配で測り、異種sliding-window規則を自動探索して静的KV maskへ落とすMoA。

- **2023-10 · [HyperAttention: Long-context Attention in Near-Linear Time](2023-2310.05869-hyperattention-long-context-attention-in-near-linear-time.md)**  
  実装：[✓](https://github.com/insuhan/hyper-attn) ・ リポジトリ内被引用：4  
  HyperAttentionは、softmax注意行列を全要素計算する代わりに、局所性鋭敏ハッシュ（Locality-Sensitive Hashing; LSH）で非常に大きな注意要素を先に見つけ、残りをサンプリングして近似する。

### 4年前（2022-10〜2023-09）

- **2023-05 · [Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers](2023-2305.15805-dynamic-context-pruning-for-efficient-and-interpretable-autoregressive-transformers.md)**  
  実装：[✓](https://github.com/sanagno/adaptively_sparse_attention) ・ リポジトリ内被引用：2  
  動的 Context 枝刈りは、生成の途中で「今後のトークンが参照する価値が低い」と学習した過去トークンを、注意対象とキー・バリュー（Key-Value; KV）キャッシュから動的に削除する。固定窓のように距離だけで落とさず、層ごとの学習可能な相互作用スコアで削除時点を決める。

### 6年前（2020-10〜2021-09）

- **2021-06 · [Memory-efficient Transformers via Top-k Attention](2021-2106.06899-top-k-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  通常注意は系列長をLとするとL×Lのスコア行列を作るため、長系列ではメモリ使用量が二次的に増える。Top-k 注意機構は、各クエリについて全キーとのスコアから上位k個だけを残し、クエリをチャンク単位で処理することでピークメモリを系列長に対して線形へ近づける。

### 7年前（2019-10〜2020-09）

- **2020-03 · [Efficient Content-Based Sparse Attention with Routing Transformers](2020-2003.05997-efficient-content-based-sparse-attention-with-routing-transformers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/routing_transformer) ・ リポジトリ内被引用：2  
  固定した近傍窓ではなく「内容が近いトークン」をクラスタリングして注意先を決める。局所注意だけでは拾いにくい遠距離依存を残しつつ、各トークンが全系列を見る密な自己注意の二乗コストを削る、初期の内容依存疎注意方式。
<!-- survey:auto:end -->
