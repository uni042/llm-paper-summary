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
## 自動生成の論文一覧（54本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [GLM-5: from Vibe Coding to Agentic Engineering](2026-2602.15763-glm-5-from-vibe-coding-to-agentic-engineering.md)**  
  実装：[✓](https://github.com/zai-org/GLM-5) ・ リポジトリ内被引用：26  
  前世代GLM-4.5の3550億/320億活性と比較すると、総容量を増やしながら毎トークンの計算増加を限定する設計である。論文は長系列の注意計算で約1.5〜2倍の削減効果を述べるが、これは全システムの要求処理率が一律2倍になるという意味ではない。

- **2026-03 · [IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse](2026-2603.12201-indexcache-cross-layer-index-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  各層で繰り返す疎注意のトークン選択を一部の層だけで計算し、後続層に再利用する。30B DSAモデルの200K文脈でインデクサ計算を75%削減し、プリフィルを1.82倍、デコードを1.48倍高速化した。

- **2025-12 · [Kascade: A Practical Sparse Attention Method for Long-Context LLM Inference](2025-2512.16391-kascade-a-practical-sparse-attention-method-for-long-context-inference.md)**  
  実装：[✓](https://github.com/microsoft/kascade) ・ リポジトリ内被引用：6  
  長文脈の注意を10%だけ計算すれば理論上は大きく速くなるが、「どの10%を残すか」を毎層正確に探す処理が高い。Kascadeは、高い注意重みを持つキー集合が近接層でかなり似るという性質を利用し、少数のアンカー層だけでTop-k探索をやり直す。残りの層ではそのインデックスを再利用するため、疎化の選択費用を層間で償却できる。

- **2026-03 · [HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention](2026-2603.28458-hisa-efficient-hierarchical-indexing-for-fine-grained-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  狙いはブロック疎 注意へ変更することではなく、ブロックを検索用の粗い索引としてだけ使い、最終的な注意対象はトークン粒度のまま維持することにある。

- **2026-06 · [MiniMax Sparse Attention](2026-2606.13392-minimax-sparse-attention.md)**  
  実装：[✓](https://github.com/MiniMax-AI/MSA) ・ リポジトリ内被引用：4  
  対象：100万トークン級の長文脈推論・学習における、GQA対応の学習可能なブロック疎注意。一次論文は2026年6月12日改訂の第2版。速度の値は「モデル全体の推論速度」ではなく、論文の注意演算実装をH800で測った値として読む。

- **2026-02 · [HySparse: A Hybrid Sparse Attention Architecture with Oracle Token Selection and KV Cache Sharing](2026-2602.03560-hysparse-a-hybrid-sparse-attention-architecture-with-oracle-token-select.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HySparseは、長文脈言語モデルの注意計算と鍵・値キャッシュ（KVキャッシュ）を同時に削減するため、少数の全体注意層を後続の疎注意層の情報供給源として再利用する混合注意アーキテクチャである。従来の動的疎注意は、重要なトークンを予測する補助選択器が必要になり、選択誤差と計算費用が生じる。HySparseでは一つの全体注意層の後ろに複数の疎注意層を配置する。

- **2026-07 · [Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling](2026-2607.0298-hierarchical-sparse-attention-done-right-toward-infinite-context-modelin.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/HiLS-Attention) ・ リポジトリ内被引用：3  
  本論文の階層ランドマーク疎注意（Hierarchical Landmark Sparse 注意機構、HiLS-注意機構）は、全注意であるチャンクが受ける指数化注意重みの合計を近似するため、各チャンク末尾のランドマークトークンから「圧縮鍵」と「エントロピーバイアス」を作る。

- **2026-07 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2026-delta.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：3  
  少数の更新層で重要KVページを動的に選び、後続層がその集合を再利用することで、完全なKV保持と推論精度を維持しつつ長文デコードを高速化する疎注意方式。

- **2026-04 · [Guess-Verify-Refine: Data-Aware Top-K for Sparse-Attention Decoding on Blackwell via Temporal Correlation](2026-2604.22312-guess-verify-refine-data-aware-top-k-for-sparse-attention-decoding-on-bl.md)**  
  実装：[✓](https://github.com/longcheng-nv/GVR_TopK_supplementaty_materials) ・ リポジトリ内被引用：3  
  Guess-Verify-Refine（GVR）は、DeepSeek Sparse 注意機構（DSA）の復号時に毎トークン実行される正確な上位K選択（exact Top-K）を高速化するGPUアルゴリズムである。

- **2026-07 · [dLLM-Serve: Bridging the Memory Gap in Diffusion Language Model Serving](2026-2512.17077-dllm-serve-bridging-the-memory-gap-in-diffusion-language-model-serving.md)**  
  実装：[✓](https://github.com/chosen-ox/dLLM-Serve) ・ リポジトリ内被引用：2  
  本論文のdLLM-Serveは、出力語彙の計算を小分けにして一時活性値の上限を固定する仕組み、更新局面と再利用局面を同じ実行回に詰め合わせるスケジューラ、注意ヘッドごとに重要なトークンを選びながら鍵・値を物理的に連続配置するキャッシュ管理を統合した。

- **2026-04 · [AsyncTLS: Efficient Generative LLM Inference with Asynchronous Two-level Sparse Attention](2026-2604.07815-asynctls-efficient-generative-llm-inference-with-asynchronous-two-level-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  必要な過去トークンだけを読む疎注意（sparse 注意機構）は計算を減らすが、重要トークンを毎回全体から探す索引処理が重い。Qwen3とGLM-4.7-Flashの長文脈評価では、全注意に近い品質を保ち、注意演算子単体で最大10.0倍、96K文脈でオフロードを含む要求処理率は最大4.70倍の改善を報告した。

- **2026-03 · [FlashPrefill: Instantaneous Pattern Discovery and Thresholding for Ultra-Fast Long-Context Prefilling](2026-2603.06199-flashprefill-instantaneous-pattern-discovery-and-thresholding-for-ultra-.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefill) ・ リポジトリ内被引用：2  
  FlashPrefillは、長文脈大規模言語モデル（LLM）のプリフィル（プリフィル）で支配的になる二次複雑度の自己注意を、入力ごとに発見したブロック-疎 注意へ置換する手法である。

- **2026-08 · [On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability](2026-2608.30320-on-the-design-of-qwen3-8-next-architecture-evaluation-efficiency-and-tra.md)**  
  実装：[✓](https://github.com/QwenLM/FlashQLA) ・ リポジトリ内被引用：1  
  Qwen3.8-Flash-Nextは履歴を再帰状態へ要約し、圧縮した疎注意機構で長文脈を検索する。論文は1M文脈で注意機構の計算時間を短縮し、検索品質も比較する。

- **2026-08 · [LongCat Sparse Attention: Taming the Lightning via Streaming-aware Hierarchical Cross-Layer Indexing](2026-2608.01662-longcat-sparse-attention-taming-the-lightning-via-streaming-aware-hierar.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LongCat Sparse 注意機構（LSA）は、長文脈モデルにおける疎注意の「選ぶための計算」と「選んだ鍵・値をGPUが読むための計算」の両方を減らす研究である。

- **2026-06 · [SparDA: Sparse Decoupled Attention for Efficient Long-Context LLM Inference](2026-2606.04511-sparda.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  疎注意は実際に参照するKVだけを減らせるが、全KVキャッシュ容量は文脈長に比例して増え、GPUからCPUへ退避するとPCIe転送が律速になる。

- **2026-06 · [From Rigid to Dynamic: Entropy-Guided Adaptive Inference for Long-Context LLMs](2026-2606.09508-from-rigid-to-dynamic-entropy-guided-adaptive-inference-for-long-context.md)**  
  実装：[✓](https://github.com/SHA-4096/EntropyInfer) ・ リポジトリ内被引用：1  
  長い入力を処理するLLMでは、入力文脈全体の注意機構計算がプリフィル 遅延を押し上げ、生成中は過去トークンのキー/値 (KV) が蓄積してGPU メモリを圧迫する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [SANTA++: Sampling Attention through Representative Keys](2026-2609.35629-santa-sampling-attention-through-representative-keys.md)**  
  実装：[✓](https://github.com/OPUSLab/santapp-kernel-demo) ・ リポジトリ内被引用：0  
  代表キーを使う確率的な疎注意。長文脈の全キー走査を避けつつ、選ばれたチームの注意寄与を包含確率で補正する。

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

- **2026-07 · [Scaling Attention Beyond GPUs for LLM Inference](2026-c3c79f91845d-scaling-attention-beyond-gpus-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Beyondは、長文脈・多要求の大規模言語モデル（LLM）推論でキー・値キャッシュ（KV キャッシュ）がGPUの高帯域メモリ（HBM）を超えたとき、CPU DRAMを単なる退避先として使うのではなく、CPU側のメモリ帯域と演算能力も注意計算へ参加させるCPU–GPU協調ランタイムである。

- **2026-07 · [RIS-Kernel: A Model-Agnostic Architecture for Long-Context LLM Inference via Sparse Attention](2026-2607.21927-ris-kernel-a-model-agnostic-architecture-for-long-context-llm-inference-.md)**  
  実装：[✓](https://github.com/santosardr/riskernel) ・ リポジトリ内被引用：0  
  RIS-Kernelは、長文脈の自己注意（self-注意機構）が全トークン対を評価することで計算量・メモリ量が急増する問題に対し、推論時だけ注意相互作用を疎化するReduced Interaction Sampling（RIS）を実装した推論層である。

- **2026-04 · [HieraSparse: Hierarchical Semi-Structured Sparse KV Attention](2026-2604.16864-hierasparse.md)**  
  実装：[✓](https://github.com/psl-ntu/HieraSparse) ・ リポジトリ内被引用：0  
  HieraSparseは、長文脈推論で自己注意計算とKVキャッシュ容量が増大する問題に対し、KVを密ブロックとN:M半構造化疎ブロックへ分け、GPUの疎テンソルコアで直接処理する方式である。NVIDIA L40S実機では、同じ疎性のMUSTAFARに対して最大1.2倍高いKV圧縮率と4.57倍の注意カーネル高速化を示す。

### 2年前（2024-11〜2025-10）

- **2025-02 · [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](2025-2502.11089-native-sparse-attention-hardware-aligned-and-natively-trainable-sparse-a.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  Native Sparse 注意機構（NSA）は、長文脈Transformerの注意演算を、圧縮した長距離文脈、入力依存で選んだ重要ブロック、直近の局所窓という三つの枝に分ける疎注意方式である。注意カーネルは64K文脈で順伝播最大9.0倍、逆伝播最大6.0倍の実測高速化を報告する。

- **2025-02 · [MoBA: Mixture of Block Attention for Long-Context LLMs](2025-2502.13189-moba.md)**  
  実装：[✓](https://github.com/MoonshotAI/MoBA) ・ リポジトリ内被引用：37  
  MoBAは各問い合わせが関連KVブロックを動的選択するMoE型疎注意で、1M文脈の品質を完全注意に近く保ちつつ注意層前処理を最大6.5倍高速化する。

- **2025-02 · [FlexPrefill: A Context-Aware Sparse Attention Mechanism for Efficient Long-Sequence Inference](2025-2502.20766-flexprefill-a-context-aware-sparse-attention-mechanism-for-efficient-long-context-inference.md)**  
  実装：[✓](https://github.com/bytedance/FlexPrefill) ・ リポジトリ内被引用：17  
  要点: FlexPrefillは、長文プリフィルの注意計算を一律の疎パターンへ置き換えるのではなく、入力と注意ヘッドごとに「クエリごとに見る場所が違う多様型」か「多くのクエリが似た場所を見る構造型」かを判定し、その型に合う索引だけを累積注意量の閾値まで選ぶ。これにより、必要なヘッドには多く、簡単なヘッドには少ない計算予算を割り当てる。

- **2024-12 · [SCBench: A KV Cache-Centric Analysis of Long-Context Methods](2024-2412.10319-scbench-a-kv-cache-centric-analysis-of-long-context-methods.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  共有長文脈を複数ターンで再利用する12タスクを用い、KV生成・圧縮・検索・読み込みの各方式が初回だけでなく後続要求でどう崩れるかを比較する。

- **2025-02 · [Twilight: Adaptive Attention Sparsity with Hierarchical Top-p Pruning](2025-2502.02770-twilight-adaptive-attention-sparsity-with-hierarchical-top-p-pruning.md)**  
  実装：[✓](https://github.com/tsinghua-ideal/Twilight) ・ リポジトリ内被引用：10  
  疎注意（sparse 注意機構）は参照対象を重要トークンへ限定して帯域を節約するが、従来の多くの方式は選択数を固定した上位k件（top-k）方式である。

- **2025-09 · [InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation](2025-2509.24663-infllm-v2-dense-sparse-switchable-attention-for-seamless-short-to-long-a.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  すべての過去トークンを見る密注意は安定した品質を持つが、長い入力を処理すると計算量とGPUメモリ帯域の双方が制約になる。第一に、元モデルの問い合わせ・鍵・値射影をそのまま共有し、短い系列では密注意、長い系列では疎注意へ切り替える。

- **2025-03 · [XAttention: Block Sparse Attention with Antidiagonal Scoring](2025-2503.16428-xattention-block-sparse-attention-with-antidiagonal-scoring.md)**  
  実装：[✓](https://github.com/mit-han-lab/x-attention) ・ リポジトリ内被引用：9  
  すべての過去トークンが同じように重要とは限らないため、注意行列の重要な領域だけを計算するブロック疎注意（block-sparse 注意機構）が提案されてきた。RULERやLongBenchでは全注意に近い精度を保ち、注意演算部分では最大13.5倍の高速化を報告する。

- **2025-07 · [RefreshKV: Updating Small KV Cache During Long-form Generation](2025-a2b748353aae-refreshkv-updating-small-kv-cache-during-long-form-generation.md)**  
  実装：[✓](https://github.com/carriex/refreshkv) ・ リポジトリ内被引用：7  
  従来のKVキャッシュ削除方式は、プリフィル直後や過去の注意得点から残すトークンを選び、それ以外の鍵値を捨てる。

- **2025-06 · [SeerAttention-R: Sparse Attention Adaptation for Long Reasoning](2025-2506.08889-seerattention-r-sparse-attention-adaptation-for-long-reasoning.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：7  
  思考連鎖が1万トークンを超える推論モデルでは、1トークン生成するたび全過去KVを読む注意が重くなる。SeerAttention-Rは、元モデルを変えずに小さなゲートだけを学習し、「今回のクエリが見るべきKVブロック」を予測してデコード注意を疎化する。

- **2024-11 · [Squeezed Attention: Accelerating Long Context Length LLM Inference](2024-2411.09688-squeezed-attention-accelerating-long-context-length-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  固定長文脈のキーをオフラインで意味クラスタ化し、実行時クエリに関連するクラスタの元KVだけを読み込んで正確な注意を計算し、長文脈の帯域と演算を削減する。

- **2025-02 · [Tactic: Adaptive Sparse Attention with Clustering and Distribution Fitting for Long-Context LLMs](2025-2502.12216-tactic-adaptive-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  累積注意質量を目標にKV数を動的決定し、K-meansと分布当てはめで選択費用を抑えて注意を最大7.29倍高速化するTactic。

- **2025-02 · [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](2025-2502.18137-spargeattn-accurate-sparse-attention-accelerating-any-model-inference.md)**  
  実装：[✓](https://github.com/thu-ml/SpargeAttn) ・ リポジトリ内被引用：5  
  自己類似度を使って重要ブロックを予測し、残ったブロックにもGPUワープ単位のsoftmax判定を適用する学習不要の疎注意演算子。近似誤差の許容範囲を層ごとに調整し、言語・画像・動画で実測性能と品質を比較する。

- **2025-10 · [NOSA: Native and Offloadable Sparse Attention](2025-2510.13602-nosa-native-and-offloadable-sparse-attention.md)**  
  実装：[✓](https://github.com/thunlp/NOSA) ・ リポジトリ内被引用：4  
  NOSAは、学習可能な疎注意（trainable sparse 注意機構）とCPUへのKVキャッシュ退避を両立させるために、注意先の選択パターンを学習段階から転送局所性の高いものへ制約する手法である。

- **2025-07 · [Compactor: Calibrated Query-Agnostic KV Cache Compression with Approximate Leverage Scores](2025-2507.08143-compactor-calibrated-query-agnostic-kv-cache-compression-with-approximat.md)**  
  実装：[✓](https://github.com/vnchari/compactor-vllm) ・ リポジトリ内被引用：4  
  近似レバレッジスコアで質問非依存にKVを選別し、文脈別の圧縮耐性を校正してLongBenchで完全KV相当の性能を保ちながら平均68%のKVメモリを削減する。

- **2025-04 · [MMInference: Accelerating Pre-filling for Long-Context VLMs via Modality-Aware Permutation Sparse Attention](2025-2504.16083-mminference-accelerating-pre-filling-for-long-context-vlms-via-modality-.md)**  
  実装：[✓](https://aka.ms/MMInference) ・ リポジトリ内被引用：4  
  MMInferenceは、長い動画や動画とテキストが混在する視覚言語モデル（Vision-Language モデル; VLM）の入力処理段階を、モダリティごとの疎注意パターンに合わせて高速化する。報告される8.3倍は1Mトークンでのプリフィル時間に関する値であり、生成段階の一トークン時間ではない。

- **2025-02 · [Top-Theta Attention: Sparsifying Transformers by Compensated Thresholding](2025-2502.08363-top-theta-attention.md)**  
  実装：[✓](https://github.com/huawei-csl/top-theta-attention) ・ リポジトリ内被引用：0  
  Top-Thetaは層・ヘッド・位置別の校正しきい値で注意重みを選び、行ごとの上位k選択（top-k）を避けて注意計算とV行読出しを減らす。LLaMA系評価では注意要素やV読出しを最大10分の1程度まで減らす条件を示す一方、強い疎化や実装条件によって品質・実速度の利得が変わる。

### 3年前（2023-11〜2024-10）

- **2024-06 · [Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference](2024-2406.10774-quest.md)**  
  実装：[✓](https://github.com/mit-han-lab/Quest) ・ リポジトリ内被引用：121  
  KVページのキー最小・最大値と現在クエリから重要度上界を推定し、上位ページだけを読むことで全KVを保持したまま長文脈注意の帯域を削減し最大7.03倍高速化。

- **2024-07 · [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](2024-2407.02490-minference.md)**  
  実装：[✓](https://github.com/microsoft/MInference) ・ リポジトリ内被引用：74  
  注意ヘッドを3種の疎パターンへ割り当て、入力ごとの重要位置を動的推定して長文脈プリフィルを専用GPUカーネルで高速化する。

- **2024-10 · [SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs](2024-2410.13276-seerattention.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：25  
  Q/Kからブロック単位の重要度を学習する軽量ゲートとブロック疎FlashAttentionを組み合わせ、長文プリフィルの注意計算を動的に削減する。

- **2024-06 · [Loki: Low-Rank Keys for Efficient Sparse Attention](2024-2406.02542-loki-low-rank-keys-for-efficient-sparse-attention.md)**  
  実装：[✓](https://github.com/hpcgroup/loki) ・ リポジトリ内被引用：16  
  キーの低ランク性を使い、低次元スコアで候補KVを選んでから全次元注意を計算し、品質を保ちながら注意計算を最大約45%短縮する疎注意法。

- **2024-08 · [Post-Training Sparse Attention with Double Sparsity](2024-2408.07092-post-training-sparse-attention-with-double-sparsity.md)**  
  実装：[✓](https://github.com/andy-yang-1/DoubleSparse) ・ リポジトリ内被引用：15  
  長文脈の自己回帰生成では、各新規トークンの問い合わせに対して過去の鍵・値キャッシュ（KVキャッシュ）を読み出すため、注意計算がGPUのメモリ帯域に律速されやすい。注意スコアへ大きく寄与する特徴チャネルを学習後の少量データで層別に校正し、そのチャネルだけを連続配置した小さなラベルキャッシュを作る。

- **2024-06 · [Mixture of Attention Spans: Optimizing LLM Inference Efficiency with Heterogeneous Sliding-Window Lengths](2024-2406.14909-mixture-of-attention-spans-optimizing-llm-inference-efficiency-with-heterogeneous-sliding-window-lengths.md)**  
  実装：[✓](https://github.com/thu-nics/MoA) ・ リポジトリ内被引用：10  
  ヘッドごとの局所性と入力長への伸び方を勾配で測り、異種sliding-window規則を自動探索して静的KV maskへ落とすMoA。

- **2024-10 · [TidalDecode: Fast and Accurate LLM Decoding with Position Persistent Sparse Attention](2024-2410.05076-tidaldecode-fast-and-accurate-llm-decoding-with-position-persistent-spar.md)**  
  実装：[✓](https://github.com/DerrickYLJ/TidalDecode) ・ リポジトリ内被引用：7  
  系列が長くなるほど鍵値キャッシュは線形に増えるため、1トークンずつ生成する復号では演算より高帯域メモリからの読出しが律速になりやすい。論文の例ではLLaMA-2-7Bを半精度、128K文脈で使うと鍵値キャッシュだけで64GBになる。疎注意（sparse 注意機構）は全過去トークンの一部だけを注意計算へ入れることで、この読出し量を減らす。

- **2024-09 · [Block-Attention for Efficient Prefilling](2024-2409.15355-block-attention-for-efficient-prefilling.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Block-Attention) ・ リポジトリ内被引用：7  
  検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した各文書を互いに独立した注意ブロックとして事前計算し、同じ文書が別質問で再利用されたらKVキャッシュを再計算しない。

### 4年前（2022-11〜2023-10）

- **2023-05 · [Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers](2023-2305.15805-dynamic-context-pruning-for-efficient-and-interpretable-autoregressive-transformers.md)**  
  実装：[✓](https://github.com/sanagno/adaptively_sparse_attention) ・ リポジトリ内被引用：10  
  動的 Context 枝刈りは、生成の途中で「今後のトークンが参照する価値が低い」と学習した過去トークンを、注意対象とキー・バリュー（Key-Value; KV）キャッシュから動的に削除する。固定窓のように距離だけで落とさず、層ごとの学習可能な相互作用スコアで削除時点を決める。

- **2023-10 · [HyperAttention: Long-context Attention in Near-Linear Time](2023-2310.05869-hyperattention-long-context-attention-in-near-linear-time.md)**  
  実装：[✓](https://github.com/insuhan/hyper-attn) ・ リポジトリ内被引用：4  
  局所性鋭敏ハッシュで注意行列の大きな要素を効率的に見つけ、残りの小さい成分をサンプリングで近似する。全注意行列を作らずに正規化と値の加重和を計算し、長文脈での計算量を削減する。

### 6年前（2020-11〜2021-10）

- **2020-12 · [SpAtten: Efficient Sparse Attention Architecture with Cascade Token and Head Pruning](2020-2012.09852-spatten-efficient-sparse-attention-architecture-with-cascade-token-and-head-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  累積注意確率とヘッド出力から重要トークン・ヘッドを動的にカスケード枝刈りし、確率分布に応じた段階的量子化と専用top-k回路で注意の計算・DRAM転送を同時に削減する。

- **2021-06 · [Memory-efficient Transformers via Top-k Attention](2021-2106.06899-top-k-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  通常注意は系列長をLとするとL×Lのスコア行列を作るため、長系列ではメモリ使用量が二次的に増える。Top-k 注意機構は、各クエリについて全キーとのスコアから上位k個だけを残し、クエリをチャンク単位で処理することでピークメモリを系列長に対して線形へ近づける。

### 7年前（2019-11〜2020-10）

- **2020-07 · [Big Bird: Transformers for Longer Sequences](2020-2007.14062-big-bird-transformers-for-longer-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：58  
  Big Birdは、系列長に対して二次の計算・メモリ費用が生じる完全自己注意を、局所窓、ランダム接続、少数の大域トークンからなる疎注意へ置き換える長文処理モデルである。各位置が全位置を直接参照する代わりに、近傍の限られた位置、ランダムに選んだ遠距離位置、全体と接続する大域位置だけを見る。論文は同程度のハードウェアで従来より最大8倍長い系列を扱えると報告する。

- **2020-03 · [Efficient Content-Based Sparse Attention with Routing Transformers](2020-2003.05997-efficient-content-based-sparse-attention-with-routing-transformers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/routing_transformer) ・ リポジトリ内被引用：19  
  固定した近傍窓ではなく「内容が近いトークン」をクラスタリングして注意先を決める。局所注意だけでは拾いにくい遠距離依存を残しつつ、各トークンが全系列を見る密な自己注意の二乗コストを削る、初期の内容依存疎注意方式。
<!-- survey:auto:end -->
