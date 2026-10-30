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
## 自動生成の論文一覧（164本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/13-sparse-attention/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-04 · [DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](2026-2606.19348-deepseek-v4-towards-highly-efficient-million-token-context-intelligence.md)**  
  実装：[✓](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/tree/main/inference) ・ リポジトリ内被引用：49  
  長いコンテキストのデコードでは、各生成トークンが過去の大量のKey/Valueを参照するため、KVのメモリ占有量と注意演算が制約になる。DeepSeek-V4は一様な密注意を用いず、圧縮疎注意（Compressed Sparse 注意機構、CSA）と高圧縮注意（Heavily Compressed 注意機構、HCA）を交互に配置する。

- **2026-02 · [GLM-5: from Vibe Coding to Agentic Engineering](2026-2602.15763-glm-5-from-vibe-coding-to-agentic-engineering.md)**  
  実装：[✓](https://github.com/zai-org/GLM-5) ・ リポジトリ内被引用：42  
  前世代GLM-4.5の3550億/320億活性と比較すると、総容量を増やしながら毎トークンの計算増加を限定する設計である。論文は長系列の注意計算で約1.5〜2倍の削減効果を述べるが、これは全システムの要求処理率が一律2倍になるという意味ではない。

- **2026-03 · [IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse](2026-2603.12201-indexcache-cross-layer-index-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  各層で繰り返す疎注意のトークン選択を一部の層だけで計算し、後続層に再利用する。30B DSAモデルの200K文脈でインデクサ計算を75%削減し、プリフィルを1.82倍、デコードを1.48倍高速化した。

- **2026-03 · [HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention](2026-2603.28458-hisa-efficient-hierarchical-indexing-for-fine-grained-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  HISA（階層型索引付き疎注意、Hierarchical Indexed Sparse 注意機構）は、長文脈大規模言語モデルの疎注意（sparse 注意機構）において、注意本体を計算する前に「どの過去トークンを参照するか」を探す索引器が律速になるという問題を扱う。

- **2026-02 · [HySparse: A Hybrid Sparse Attention Architecture with Oracle Token Selection and KV Cache Sharing](2026-2602.03560-hysparse-a-hybrid-sparse-attention-architecture-with-oracle-token-select.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  HySparseは、長文脈言語モデルの注意計算と鍵・値キャッシュ（KVキャッシュ）を同時に削減するため、少数の全体注意層を後続の疎注意層の情報供給源として再利用する混合注意アーキテクチャである。従来の動的疎注意は、重要なトークンを予測する補助選択器が必要になり、選択誤差と計算費用が生じる。HySparseでは一つの全体注意層の後ろに複数の疎注意層を配置する。

- **2025-12 · [Kascade: A Practical Sparse Attention Method for Long-Context LLM Inference](2025-2512.16391-kascade-a-practical-sparse-attention-method-for-long-context-inference.md)**  
  実装：[✓](https://github.com/microsoft/kascade) ・ リポジトリ内被引用：7  
  長文脈の注意を10%だけ計算すれば理論上は大きく速くなるが、「どの10%を残すか」を毎層正確に探す処理が高い。Kascadeは、高い注意重みを持つキー集合が近接層でかなり似るという性質を利用し、少数のアンカー層だけでTop-k探索をやり直す。残りの層ではそのインデックスを再利用するため、疎化の選択費用を層間で償却できる。

- **2026-07 · [Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling](2026-2607.0298-hierarchical-sparse-attention-done-right-toward-infinite-context-modelin.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/HiLS-Attention) ・ リポジトリ内被引用：6  
  本論文の階層ランドマーク疎注意（Hierarchical Landmark Sparse 注意機構、HiLS-注意機構）は、全注意であるチャンクが受ける指数化注意重みの合計を近似するため、各チャンク末尾のランドマークトークンから「圧縮鍵」と「エントロピーバイアス」を作る。

- **2026-08 · [On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability](2026-2608.30320-on-the-design-of-qwen3-8-next-architecture-evaluation-efficiency-and-tra.md)**  
  実装：[✓](https://github.com/QwenLM/FlashQLA) ・ リポジトリ内被引用：5  
  Qwen3.8-Flash-Nextは履歴を再帰状態へ要約し、圧縮した疎注意機構で長文脈を検索する。論文は1M文脈で注意機構の計算時間を短縮し、検索品質も比較する。

- **2026-06 · [MiniMax Sparse Attention](2026-2606.13392-minimax-sparse-attention.md)**  
  実装：[✓](https://github.com/MiniMax-AI/MSA) ・ リポジトリ内被引用：5  
  対象：100万トークン級の長文脈推論・学習における、GQA対応の学習可能なブロック疎注意。一次論文は2026年6月12日改訂の第2版。速度の値は「モデル全体の推論速度」ではなく、論文の注意演算実装をH800で測った値として読む。

- **2026-02 · [Double-P: Hierarchical Top-P Sparse Attention for Long-Context LLMs](2026-2602.05191-double-p-hierarchical-top-p-sparse-attention-for-long-context-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  固定トークン数だけを選ぶ上位k方式は単純だが、必要な注意質量が層・ヘッド・入力・復号時点ごとに変わるため、同じ予算でも精度が安定しない。RetroInfer比の注意演算単体は最大1.78倍、出力1トークン当たりの復号は最大1.26倍の高速化であり、両者は異なる測定単位である。

- **2026-01 · [From Prefix Cache to Fusion RAG Cache: Accelerating LLM Inference in Retrieval-Augmented Generation](2026-2601.12904-from-prefix-cache-to-fusion-rag-cache-accelerating-llm-inference-in-retr.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  検索拡張生成（Retrieval-Augmented Generation; RAG）では、質問に関連する文書片を多数連結して言語モデルへ渡す。通常の全文注意では文書片を一度に事前入力処理するため、互いの文脈を利用できる反面、検索片が増えると初回トークン待ち時間（Time to First Token; TTFT）が長くなる。

- **2026-03 · [FlashPrefill: Instantaneous Pattern Discovery and Thresholding for Ultra-Fast Long-Context Prefilling](2026-2603.06199-flashprefill-instantaneous-pattern-discovery-and-thresholding-for-ultra-.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefill) ・ リポジトリ内被引用：4  
  FlashPrefillは、長文脈の大規模言語モデル（LLM）が入力全体を一度に処理するプリフィル段階を高速化する、動的な疎注意（sparse 注意機構）の方式である。原著のQwen3-30B-A3B-Instruct-2507を用いた注意演算子比較では、密なFlashAttentionに対して4Kで1.71倍、256Kで27.78倍の高速化を報告する。

- **2026-07 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2026-delta.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：3  
  少数の更新層で重要KVページを動的に選び、後続層がその集合を再利用することで、完全なKV保持と推論精度を維持しつつ長文デコードを高速化する疎注意方式。

- **2026-06 · [SpotAttention: Plug-In Block-Sparse Routing for Pretrained Long-Context Transformers](2026-2606.22874-spotattention-plug-in-block-sparse-routing-for-pretrained-long-context-t.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SpotAttentionは、既存の学習済みモデルの重みを固定し、全注意層ごとに小さな鍵・質問の選択器を追加する方式である。著者はQwen3-8B、128K文脈、NVIDIA B200単体で70トークン/秒を報告し、FlashAttention比3.9倍、Twilight比1.8倍とする。

- **2026-05 · [DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention](2026-2605.18753-dashattention-differentiable-and-adaptive-sparse-hierarchical-attention.md)**  
  実装：[✓](https://github.com/fasa-org/dash-attention) ・ リポジトリ内被引用：3  
  DashAttentionは、長文脈の大規模言語モデル（Large Language モデル, LLM）で、問い合わせごとに必要な過去トークン数が異なるにもかかわらず、固定個数のブロックを選ぶ階層的疎注意（hierarchical sparse 注意機構）が使われる問題に対処する。

- **2026-05 · [An Efficient Hybrid Sparse Attention with CPU-GPU Parallelism for Long-Context Inference](2026-2605.07719-an-efficient-hybrid-sparse-attention-with-cpu-gpu-parallelism-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  CPU常駐KV向けに出力寄与ベース予算配分とCPU・GPU協調疎注意を統合し、長文復号を最大3.7倍高速化する。

- **2026-04 · [Guess-Verify-Refine: Data-Aware Top-K for Sparse-Attention Decoding on Blackwell via Temporal Correlation](2026-2604.22312-guess-verify-refine-data-aware-top-k-for-sparse-attention-decoding-on-bl.md)**  
  実装：[✓](https://github.com/longcheng-nv/GVR_TopK_supplementaty_materials) ・ リポジトリ内被引用：3  
  Guess-Verify-Refine（GVR）は、長文脈の疎注意を使う言語モデルが次のトークンを生成するとき、過去の全トークンから重要度上位の位置を選ぶ処理を高速化するGPUアルゴリズムである。

- **2026-02 · [LycheeDecode: Accelerating Long-Context LLM Inference via Hybrid-Head Sparse Decoding](2026-2602.04541-lycheedecode-accelerating-long-context-llm-inference-via-hybrid-head-spa.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  文脈長が128Kトークンに達すると、注意計算とKVキャッシュの読み出しが遅延を増やす。LycheeDecodeはこの問題を、少数の「検索ヘッド（retrieval heads）」と多数の「疎ヘッド（sparse heads）」へ役割を分ける混合ヘッド方式で解く。

- **2026-02 · [FASA: Frequency-aware Sparse Attention](2026-2602.03152-fasa-frequency-aware-sparse-attention.md)**  
  実装：[✓](https://github.com/wangyifei0047/FASA-ICLR2026) ・ リポジトリ内被引用：3  
  そこで過去トークンを間引く方式が使われるが、固定位置の保存や事前段階での一度限りの選別では、生成途中に変わる重要性を追跡できない。

- **2026-08 · [LongCat Sparse Attention: Taming the Lightning via Streaming-aware Hierarchical Cross-Layer Indexing](2026-2608.01662-longcat-sparse-attention-taming-the-lightning-via-streaming-aware-hierar.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LongCat Sparse 注意機構（LSA）は、長文脈モデルにおける疎注意の「選ぶための計算」と「選んだ鍵・値をGPUが読むための計算」の両方を減らす研究である。

- **2026-08 · [FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving](2026-2608.19758-flashprefill-v2-block-sparse-prefill-attention-for-long-context-llm-serving.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefillv2) ・ リポジトリ内被引用：2  
  平均補正付きブロック疎注意をHopper向けに再設計し、SGLangの長文事前充填を128Kで最大4.8倍高速化する。

- **2026-04 · [AsyncTLS: Efficient Generative LLM Inference with Asynchronous Two-level Sparse Attention](2026-2604.07815-asynctls-efficient-generative-llm-inference-with-asynchronous-two-level-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  必要な過去トークンだけを読む疎注意（sparse 注意機構）は計算を減らすが、重要トークンを毎回全体から探す索引処理が重い。Qwen3とGLM-4.7-Flashの長文脈評価では、全注意に近い品質を保ち、注意演算子単体で最大10.0倍、96K文脈でオフロードを含む要求処理率は最大4.70倍の改善を報告した。

- **2026-03 · [Stem: Rethinking Causal Information Flow in Sparse Attention](2026-2603.06274-stem-rethinking-causal-information-flow-in-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Stemは、長文脈Transformerの事前充填（プリフィル）段階で行う注意演算を、因果的な情報の流れに合わせて間引く方式である。Qwen3-8BのLongBenchでは、全注意方式の平均32.01に対してStemは31.64を維持しながら、注意ブロック予算を25%に抑えた。

- **2026-02 · [QUOKA: Query-Oriented KV Selection For Efficient LLM Prefill](2026-2602.08722-quoka-query-oriented-kv-selection-for-efficient-llm-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  選択したKVだけを通常の密注意カーネルへ渡すため、専用の疎行列GPUカーネルを必須としない。主な検証はNVIDIA A100上のQwen3-4Bなどで、分割プリフィル時の初回トークンまでの時間（TTFT）を長文条件で最大約3倍改善し、注意演算単体では約5倍の高速化を示した。

- **2026-01 · [Elastic Attention: Test-time Adaptive Sparsity Ratios for Efficient Transformers](2026-2601.17367-elastic-attention-test-time-adaptive-sparsity-ratios-for-efficient-trans.md)**  
  実装：[✓](https://github.com/LCM-Lab/Elastic-Attention) ・ リポジトリ内被引用：2  
  既存の混合注意方式は、どのヘッドを全注意に残すかを学習後に固定しがちで、同じモデルへ異なる種類の依頼が来たときの配分変更が難しい。

- **2025-12 · [InfiniteVL: Synergizing Linear and Sparse Attention for Highly-Efficient, Unlimited-Input Vision-Language Models](2025-2512.08829-infinitevl-synergizing-linear-and-sparse-attention-for-highly-efficient-.md)**  
  実装：[✓](https://github.com/hustvl/InfiniteVL) ・ リポジトリ内被引用：2  
  従来の全注意（full 注意機構）型Transformerは、事前充填（プリフィル）で系列長の二乗に比例する計算を要し、復号（デコード）では生成が進むほどKVキャッシュが増える。RTX 4090での実測では、基本型は約450K文脈でQwen2.5-VL-3B比のトークン当たり復号遅延を1.7倍改善し、256K文脈の事前充填を2.8倍高速化した。

- **2026-09 · [Elastic Threshold Attention: Learned Contextual Sparsity for Long-Context Decoding](2026-2609.20888-elastic-threshold-attention-learned-contextual-sparsity-for-long-context.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Elastic Threshold 注意機構（ETA）は、注意ヘッドごとに現在のクエリから動的な閾値を予測する機構をモデルに組み込み、訓練時から疎化しやすい注意分布を学習する。

- **2026-09 · [CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference](2026-2609.26300-compkv-compensation-aware-kv-selection-for-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  平均補償後に残る注意誤差を注意質量とブロック内得点分散の積で推定し、厳密に読む鍵・値ブロックを選ぶことで、長文脈の疎な注意計算の精度と中央処理装置退避効率を改善する。

- **2026-08 · [RouteSparse: Input-Conditional Pattern Routing for Budgeted Long-Context Prefilling](2026-2608.29058-routesparse-input-conditional-pattern-routing-for-budgeted-long-context-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RouteSparseは、長文脈LLMの事前充填（プリフィル）で必要な注意演算の組を減らす動的な疎注意（sparse 注意機構）手法である。

- **2026-08 · [Prefix Sliding for efficient test-time scaling](2026-2608.26070-prefix-sliding-for-efficient-test-time-scaling.md)**  
  実装：[✓](https://github.com/Muennighoff/prefix-sliding) ・ リポジトリ内被引用：1  
  推論時間拡張（test-time scaling）では、言語モデルが問題を解くために生成する思考トークン数を増やし、難問の正答率を改善する。しかし、通常の全注意（full 注意機構）では、生成済みの全トークンに対する鍵・値キャッシュ（KV キャッシュ）を保持し、次のトークンを生成するたびに全履歴を読む。

- **2026-07 · [CoSA: Accelerating Long-Context Inference via Proxy-Kernel Co-Designed Sparse Attention](2026-2607.25291-cosa-accelerating-long-context-inference-via-proxy-kernel-co-designed-sp.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：1  
  長文脈のプレフィルで密な自己注意を実行すると、クエリとキーの全組合せを計算する負荷が入力長の二乗で増える。逆にカーネル内で実際の注意logitを見て省略する方式は、判定前のQK内積を減らせず、訪問順が悪いと省略が保守的になる。NVIDIA H20の128K文脈では密注意比で注意演算4.93倍、最初のトークンまでの時間（TTFT）2.53倍を報告した。

- **2026-06 · [SparDA: Sparse Decoupled Attention for Efficient Long-Context LLM Inference](2026-2606.04511-sparda.md)**  
  実装：[✓](https://github.com/NVlabs/SparDA) ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデルでは、事前入力処理の注意計算、復号時のKVキャッシュ読出し帯域、KVキャッシュのGPU容量という三つの資源が制約になる。疎注意（Sparse 注意機構）は実際に参照するトークンやブロックを減らし、注意計算と読出し帯域を削減する。

- **2026-06 · [From Rigid to Dynamic: Entropy-Guided Adaptive Inference for Long-Context LLMs](2026-2606.09508-from-rigid-to-dynamic-entropy-guided-adaptive-inference-for-long-context.md)**  
  実装：[✓](https://github.com/SHA-4096/EntropyInfer) ・ リポジトリ内被引用：1  
  長い入力を処理するLLMでは、入力文脈全体の注意機構計算がプリフィル 遅延を押し上げ、生成中は過去トークンのキー/値 (KV) が蓄積してGPU メモリを圧迫する。

- **2026-05 · [Sparse Attention as a Range Searching Problem: Towards an Inference-Efficient Index for KV Cache](2026-2605.06763-sparse-attention-as-a-range-searching-problem-towards-an-inference-effic.md)**  
  実装：[✓](https://github.com/UIC-InDeXLab/Louver) ・ リポジトリ内被引用：1  
  著者らは、必要な鍵の数が質問と時刻によって変わることを実験で示し、固定個数の検索ではなく、問い合わせとの内積が指定閾値以上の鍵を全て返す問題へ置き換える。提案方式Louverは、KVキャッシュの鍵を幾何学的な点集合と見なし、問い合わせベクトルと閾値から定まる半空間に含まれる点を検索する。

- **2026-05 · [AB-Sparse: Sparse Attention with Adaptive Block Size for Accurate and Efficient Long-Context Inference](2026-2605.12110-ab-sparse-sparse-attention-with-adaptive-block-size-for-accurate-and-eff.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ブロック疎注意（block sparse 注意機構）は、過去トークンを一定長のブロックへ区切り、各ブロックの代表ベクトルと現在の問い合わせの類似度から重要なブロックだけを読み込む。Llama-3.1-8B、Qwen3-8B、Qwen3-32BのRULERとLongBenchで、Quest・ArkValeを同じKV予算4%、平均ブロック長32の条件で比較した。

- **2026-04 · [LoSA: Locality Aware Sparse Attention for Block-Wise Diffusion Language Models](2026-2604.12056-losa-locality-aware-sparse-attention-for-block-wise-diffusion-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LoSA（Locality-Aware Sparse 注意機構）は、ブロック単位の拡散言語モデル（Block-Wise Diffusion Language モデル, DLM）の長文脈推論に特有のメモリ帯域問題を扱う。

- **2026-03 · [Dynamic Sparse Attention: Access Patterns and Architecture](2026-2603.13430-dynamic-sparse-attention-access-patterns-and-architecture.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、大規模言語モデル（LLM）の復号時に動的疎注意（動的 Sparse 注意機構; DSA）を採用すると、読み込む鍵・値（KV）の個数を減らしてもGPUが速くなるとは限らない理由を、アクセス履歴とGPU計数器から明らかにするシステム研究である。

- **2026-02 · [Scout Before You Attend: Sketch-and-Walk Sparse Attention for Efficient LLM Inference](2026-2602.07397-scout-before-you-attend-sketch-and-walk-sparse-attention-for-efficient-l.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Sketch&Walkは、長文脈LLM推論の自己注意を疎にする際、その層で直接似ている鍵だけを残すと、複数層を経由して重要になる情報経路を切断してしまう問題を扱う。提案方式はトークンをブロックにまとめて平均し、Hadamard変換で特徴次元を縮めてブロック間の注意を推定する。

- **2026-02 · [RRAttention: Dynamic Block Sparse Attention via Per-Head Round-Robin Shifts for Long-Context Inference](2026-2602.05853-rrattention-dynamic-block-sparse-attention-via-per-head-round-robin-shif.md)**  
  実装：[✓](https://github.com/PaddlePaddle/PaddleFleet) ・ リポジトリ内被引用：1  
  提案法は各 S トークン区間からヘッドごとに異なる問い合わせを一つ選び、鍵を区間単位で集約して重要度を計算する。Llama-3.1-8BとQwen2.5-7BのHELMETでは、注意ブロックの約半分を省略しながら全注意の平均性能の99%以上を再現した。

- **2025-12 · [Training-free Context-adaptive Attention for Efficient Long Context Modeling](2025-2512.09238-training-free-context-adaptive-attention-for-efficient-long-context-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  別の方式では、注意ヘッドごとの疎性を学習で獲得するため、既存モデルへ適用する際の追加学習が必要になる。LLaMA3.1-8B-Instructの128Kトークン文脈では、全注意との比較で前処理遅延を2.8倍改善し、生成速度を2.1倍にし、KV容量を8.00GBから3.12GBへ61%削減したと報告する。

- **2025-12 · [A Unified Sparse Attention via Multi-Granularity Compression](2025-2512.14082-a-unified-sparse-attention-via-multi-granularity-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  疎注意（sparse 注意機構）は重要なブロックだけを計算して演算数を減らす一方、「重要なブロックを決めるための計算」が重くなると、疎化で節約した時間が消えてしまう。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [HHR: Hierarchical Hash Retrieval for Efficient LLM Generation](2026-2610.01230-hhr-hierarchical-hash-retrieval-for-efficient-llm-generation.md)**  
  実装：[✓](https://github.com/lianjunl13-sudo/HHR) ・ リポジトリ内被引用：0  
  品質ではLongBenchのLlama-3.1-8B平均が密注意47.51、HHR46.96と僅かに低下する一方、ハッシュ型の比較方式HATA45.86より高い。

- **2026-09 · [SparseEngine: Sparse-First Inference Engine](2026-2609.39068-sparseengine-sparse-first-inference-engine.md)**  
  実装：[✓](https://github.com/CURRENTF/SparseEngine) ・ リポジトリ内被引用：0  
  SparseEngineの貢献は、新しい疎注意スコアそのものではなく、疎方式が持つ異なる物理KV表現と状態更新の規則を共通サービング基盤へ接続する抽象化である。

- **2026-09 · [SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking](2026-2609.13141-sas-simple-attention-sparsification-via-end-to-end-optimization-of-context-ranking.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/Simple-Attention-Sparsification) ・ リポジトリ内被引用：0  
  言語モデル損失を注意ソフトマックス内の連続ゲートへ直接流してコンテキスト順位を学習し、固定Top-K疎注意の精度と長文脈デコード効率を改善する。

- **2026-09 · [SANTA++: Sampling Attention through Representative Keys](2026-2609.35629-santa-sampling-attention-through-representative-keys.md)**  
  実装：[✓](https://github.com/OPUSLab/santapp-kernel-demo) ・ リポジトリ内被引用：0  
  代表キーを使う確率的な疎注意。長文脈の全キー走査を避けつつ、選ばれたチームの注意寄与を包含確率で補正する。

- **2026-09 · [Sample-Guided Exact Top-K Selection for Long-Context Sparse Attention](2026-2609.08450-sample-guided-exact-topk-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HPC-Ops Top-Kは、標本で上位候補境界を予測し、全行の一回走査で十分性を証明、足りない時だけ回復して正確なK個を選び、長文疎注意の再走査を減らす。

- **2026-09 · [RouteRelay: Event-Triggered Cross-Layer Route Reuse for Efficient Dynamic Sparse Attention](2026-2609.07306-routerelay-cross-layer-route-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意の前層経路IDを監視候補付きで再利用し、変化した行だけ再ルーティングして経路スコア計算を約38～52%へ削減するが、現CPU実装は未融合処理で逆に低速。

- **2026-09 · [RBS-Attention: Radius-Bounded Sparse Prefill for Long-Context Large Language Models](2026-2609.20971-rbs-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RBS-注意機構は、長い入力文を処理して最初の出力トークンを返すまでの事前入力処理（プリフィル）を高速化する方式である。

- **2026-09 · [On-Demand Attention: Language Models Know When to Recall](2026-2609.20734-on-demand-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成中の多くの位置では直近文脈だけで次トークンを決められるにもかかわらず、数万から十数万トークンの履歴を毎回読むため、注意計算とHBM帯域の費用が増える。按需注意（On-Demand 注意機構; ODA）は、まず安価な局所注意を実行し、その結果と直前状態から「この段階で全注意を使う利益」を軽量な想起ヘッドで予測する。

- **2026-09 · [HySparse2: Hybrid Sparse Attention with Two-Level KV Sharing](2026-2609.26368-hysparse2-hybrid-sparse-attention-with-two-level-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この負荷は、長い入力を一度だけ読んで長い回答を生成する通常のチャットとは異なる。HySparse2は、先行HySparseの「全注意層が後続の疎注意層へKVと選択索引を供給する」設計を拡張し、YOCO型のself-decoderとcross-decoderの間にもKVを橋渡しする。

- **2026-09 · [Efficient Agentic LLM Serving over SSD-based Sparse KV Storage](2026-2609.36938-efficient-agentic-llm-serving-over-ssd-based-sparse-kv-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去の履歴を再計算しないためには鍵・値キャッシュを保持する必要があるが、全履歴を計算装置の高帯域メモリに置くと容量が不足する。後で正確な選択結果が得られた時点で予測漏れを補正するため、予測を外したトークンを黙って捨てる近似手法ではない。

- **2026-09 · [CoWindow Attention: Full Causal Coverage Is a Collective Property](2026-2609.32704-cowindow-attention-full-causal-coverage-is-a-collective-property.md)**  
  実装：[✓](https://github.com/HKUSTDial/flash-sparse-attention) ・ リポジトリ内被引用：0  
  一方、全headを同じ局所窓へ制限するSliding Window 注意機構は、長距離情報へ直接アクセスできなくなる。8Kの連想記憶実験では、全注意89.97%に対しCoWAは89.73%であり、同じ一head当たり窓幅でも長距離窓を重複させる方式より良い。

- **2026-09 · [CommunityKV: Efficient Long-Context Decoding via Graph Partitioning](2026-2610.00418-communitykv-efficient-long-context-decoding-via-graph-partitioning.md)**  
  実装：[✓](https://github.com/amazon-science/community-kv) ・ リポジトリ内被引用：0  
  CommunityKVは、長文脈の自己回帰生成で過去トークンの鍵・値キャッシュ（key-value キャッシュ; KV キャッシュ）を毎回すべて読み込む代わりに、入力文脈中で意味的にまとまったトークン群だけを検索して正確な注意計算を行う学習不要の疎注意方式である。

- **2026-09 · [CEDAR: Error-Bounded Residual Routing for Efficient Long-Context Attention](2026-2609.07237-cedar-error-bounded-residual-routing-for-efficient-long-context-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  選外チャンクも要約経路で全域可視性を残し、鍵・値分散に基づく誤差上界で必要なチャンクだけ正確注意へ展開して、128Kで約3倍のカーネル高速化と品質回復を両立する疎注意方式。

- **2026-09 · [Block-Sparse Attention with Semantic-Geometric Decoupled Routing](2026-2609.22884-block-sparse-attention-with-semantic-geometric-decoupled-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己注意は、入力系列の全トークン対を比較する密注意の計算量とメモリアクセスが大きい。そこで、問い合わせと鍵をブロック単位に平均して近似スコアを出す方式が用いられる。単一NVIDIA H100 80GBでの128Kトークン注意処理では、FlashAttentionの451.03 msに対してSGDRは89.59 ms（5.03倍）であった。

- **2026-09 · [Block Sparse Attention with Log-Linear Complexity](2026-2609.31093-block-sparse-attention-with-log-linear-complexity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の注意計算を高速化する際、過去のすべての鍵・値に注意を計算する代わりに、重要と判断した鍵ブロックだけを参照するブロック疎注意（block-sparse 注意機構）が用いられる。Tritonによる選択処理単体の実験では、256KトークンでBSAの312.96ミリ秒に対しPISAの31.44ミリ秒で、約9.95倍高速だった。

- **2026-09 · [Attention Routing Stabilizes Early: Working-Set Inference for Recurrent Language Models](2026-2609.27373-attention-routing-stabilizes-early-working-set-inference-for-recurrent-language-models.md)**  
  実装：[✓](https://github.com/tbn5pj/WISE_code) ・ リポジトリ内被引用：0  
  再帰型言語モデルは、同じネットワークブロックを何度も通して潜在表現を更新することで、固定パラメータ数のまま推論時計算量を増やせる。4K文脈では、後半20段の注意をネイティブFlashAttention比で1.758倍、探索段を含む32段の注意軌跡全体でも1.355倍高速化した。

- **2026-08 · [Self-Indexing Attention for Compression-Compatible Sparse Long-Context LLM Inference](2026-2609.13205-self-indexing-attention-for-compression-compatible-sparse-long-context-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要点：鍵の直交変換後の符号を、追加の検索器を保存せずに、事前入力処理（プリフィル）と逐次復号（デコード）の双方で利用する。検索の近似性、注意計算そのものの正確性、鍵・値の量子化誤差は別の問題として扱う。

- **2026-08 · [Learning how to Forget: Fine-tuning for Long-Context Sparse Attention](2026-2608.19920-learning-how-to-forget-fine-tuning-for-long-context-sparse-attention.md)**  
  実装：[✓](https://github.com/awslabs/keys_values) ・ リポジトリ内被引用：0  
  任意のKVキャッシュ方策を学習中に再現し、二重チェックポイントとKV差分符号化で推論級メモリの長文脈疎注意微調整を実現する。

- **2026-08 · [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](2026-2608.06849-autonomy-of-heads-data-free-sparse-attention-from-frozen-query-key-geome.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後者のheadに対して過去全トークンのKVを保持すると、メモリ容量と注意計算が無駄になる。特異値が少数の方向へ集中した低ER headは、内容に応じた遠距離の照合に重要であり、full 注意機構を維持する。

- **2026-07 · [Scaling Attention Beyond GPUs for LLM Inference](2026-c3c79f91845d-scaling-attention-beyond-gpus-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Beyondは、長文脈の大規模言語モデル（LLM）でキー・値キャッシュ（KVキャッシュ）が画像処理装置（GPU）の高帯域メモリ（HBM）からあふれた際、中央処理装置（CPU）の主記憶を単なる退避場所にせず、CPU側でも注意計算を実行する仕組みである。

- **2026-07 · [RoBSA: RoPE-based Blockwise Sparse Multi-head Latent Attention](2026-2a77ad945c5e-robsa-rope-based-blockwise-sparse-multi-head-latent-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RoBSAは、DeepSeek-V3やDeepSeek-R1が採用する多頭潜在注意（Multi-head Latent 注意機構; MLA）の復号段階を対象とする、学習不要のブロック単位疎注意方式である。入力が128Kトークン程度まで伸びると、論文の測定条件では注意計算が復号時間の90%以上を占める。

- **2026-07 · [RIS-Kernel: A Model-Agnostic Architecture for Long-Context LLM Inference via Sparse Attention](2026-2607.21927-ris-kernel-a-model-agnostic-architecture-for-long-context-llm-inference-.md)**  
  実装：[✓](https://github.com/santosardr/riskernel) ・ リポジトリ内被引用：0  
  RIS-Kernelは、長文脈の自己注意（self-注意機構）が全トークン対を評価することで計算量・メモリ量が急増する問題に対し、推論時だけ注意相互作用を疎化するReduced Interaction Sampling（RIS）を実装した推論層である。

- **2026-07 · [From Logical to Computational Sparsity: Structure-Aware Block-Sparse Attention for Long Code Completion](2026-a55ddcf36e91-from-logical-to-computational-sparsity-structure-aware-block-sparse-atte.md)**  
  実装：[✓](https://github.com/DeepSoftwareAnalytics/SabreCoder) ・ リポジトリ内被引用：0  
  長いコードを補完する言語モデルでは、入力コードを一度に処理する事前計算（プリフィル）の注意演算が入力長の二乗に応じて増える。コード特有の関数・識別子・import文を考慮しない疎注意は重要な依存を失って補完精度が落ちやすい。次に同一チャンク内、明示的依存、埋め込み類似、グローバル参照という四つの規則を合成して注意マスクを作る。

- **2026-07 · [BOSCH: Black-Box Binary Optimization for Short-Context Attention-Head Selection in LLMs](2026-fa80222132dc-bosch-black-box-binary-optimization-for-short-context-attention-head-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BOSCH（Black-Box Binary Optimization for Short-Context 注意機構-Head Selection）は、すでに学習された大規模言語モデル（LLM）を、全域因果注意（global causal self-注意機構）とスライディングウィンドウ注意（Sliding Window 注意機構…

- **2026-06 · [Memory-Efficient KV Cache Optimization for Large Language Model Inference at the Edge](2026-c5217a359f97-memory-efficient-kv-cache-optimization-for-large-language-model-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存のクエリ依存疎注意（query-aware sparse 注意機構）は、現在のトークンに必要な過去のKVの一部だけを計算に使う。Llama系モデルの実験では、メモリ削減率最大75%の条件で非制限基準の復号効率の95%を維持し、容量制限下の比較で復号遅延を最大54.84%低減したと報告する。

- **2026-05 · [VisionPulse: Dynamic Visual Sparsity for Efficient Multimodal Reasoning](2026-2605.31457-visionpulse-dynamic-visual-sparsity-for-efficient-multimodal-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚言語モデル（Vision-Language モデル）は画像を多数の視覚トークンへ変換し、テキストとともに自己注意（self-注意機構）へ入力する。

- **2026-05 · [Stochastic Sparse Attention for Memory-Bound Inference](2026-2605.01910-stochastic-sparse-attention-for-memory-bound-inference.md)**  
  実装：[✓](https://github.com/OPUSLab/SANTA) ・ リポジトリ内被引用：0  
  SANTA（Stochastic Additive No-mulT 注意機構）は、注意確率を使って少数の値ベクトルだけを抽出し、その平均で密な注意出力を近似する。RTX 6000 Ada上の32K文脈では、精度が密注意と統計的に同等な設定で注意カーネルが約1.5倍高速化した。

- **2026-05 · [PulseCol: Periodically Refreshed Column-Sparse Attention for Accelerating Diffusion Language Models](2026-2605.20813-pulsecol-periodically-refreshed-column-sparse-attention-for-accelerating.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PulseColは、拡散言語モデル（diffusion language モデル、dLLM）の生成で同じ系列に対する双方向の自己注意を何度も計算する費用を減らす方式である。

- **2026-05 · [Position: LLM Inference Should Be Evaluated as Energy-to-Token Production](2026-2605.11733-position-llm-inference-should-be-evaluated-as-energy-to-token-production.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の推論評価では精度、応答遅延、トークン毎秒、GPU利用率、モデル浮動小数点演算利用率（モデル FLOPs Utilization、MFU）を測る。KVキャッシュ圧縮、量子化、疎注意、ルーティング、バッチ化、スケジューリングなどは、トークン当たりの計算量と消費エネルギーを減らすことで、この上限を引き上げる介入として位置づけられる。

- **2026-05 · [Inference Time Context Sparsity: Illusion or Opportunity?](2026-2605.24168-inference-time-context-sparsity-illusion-or-opportunity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単なる疎化方式の提案ではなく、何を選ぶと品質が保たれ、選択器の計算費用を含めても高速化できるかを分離して調べた点が重要である。疎化の基準は通常の密な注意であり、例えば「50倍疎化」は各問い合わせ頭が文脈トークンの約1/50を参照する設定を意味する。

- **2026-05 · [Efficient Long-Context Modeling in Diffusion Language Models via Block Approximate Sparse Attention](2026-2605.19726-efficient-long-context-modeling-in-diffusion-language-models-via-block-a.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/Block-Approximate-Sparse-Attention) ・ リポジトリ内被引用：0  
  既存の学習不要な疎注意には、系列先頭、末尾、対角線などの位置パターンを優先して候補ブロックを探す方式がある。実験では、A100上でFlashAttention-2を使った密な注意と比較し、注意演算で最大6.95倍の高速化を報告する。

- **2026-05 · [CompactAttention: Accelerating Chunked Prefill with Block-Union KV Selection](2026-2605.16839-compactattention-accelerating-chunked-prefill-with-block-union-kv-select.md)**  
  実装：[✓](https://github.com/jiwonsong-dev/CompactAttention) ・ リポジトリ内被引用：0  
  CompactAttentionは、長文脈の大規模言語モデル（LLM）の分割入力処理（chunked プリフィル）を高速化するため、疎注意（sparse 注意機構）の「どのKVブロックを選ぶか」と「選んだKVをどのカーネルで計算するか」を切り離す方式である。

- **2026-04 · [SpikingBrain2.0: Brain-Inspired Foundation Models for Efficient Long-Context and Cross-Platform Inference](2026-2604.22575-spikingbrain2-0-brain-inspired-foundation-models-for-efficient-long-cont.md)**  
  実装：[✓](https://github.com/BICLab/SpikingBrain2.0) ・ リポジトリ内被引用：0  
  長い文章を扱う大規模言語モデルでは、全注意（Full 注意機構; FA）を用いると、事前充填（プリフィル）時の注意計算が系列長に対して二次的に増える。

- **2026-04 · [SAS: Sparse Attention Synthesizer for Efficient Language Model Inference](2026-35256164722e-sas-sparse-attention-synthesizer-for-efficient-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAS（Sparse 注意機構 Synthesizer）は、大規模言語モデルの疎注意を、マスクの記述だけでなく鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）の配置・寿命管理と低水準カーネルの生成まで一体化するシステムである。

- **2026-04 · [Salca: A Sparsity-Aware Hardware Accelerator for Efficient Long-Context Attention Decoding](2026-2604.24820-salca-a-sparsity-aware-hardware-accelerator-for-efficient-long-context-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Salcaは、数万トークンの長い文脈を保持したまま一語ずつ生成する際の注意計算に特化した、疎注意アルゴリズムとASIC構成の共同設計である。著者らのChatGLM3の解析では、注意確率の95%を保持する条件で平均94.6%の疎性を観測した。

- **2026-04 · [HubRouter: A Pluggable Sub-Quadratic Routing Primitive for Hybrid Sequence Models](2026-2604.22442-hubrouter-a-pluggable-sub-quadratic-routing-primitive-for-hybrid-sequenc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HubRouterは、全トークン同士を比較する通常の自己注意を、少数の学習可能なハブを介したルーティングと、重要トークンだけを対象とする小規模な注意計算に置き換える系列モデル用の機構である。

- **2026-04 · [HieraSparse: Hierarchical Semi-Structured Sparse KV Attention](2026-2604.16864-hierasparse.md)**  
  実装：[✓](https://github.com/psl-ntu/HieraSparse) ・ リポジトリ内被引用：0  
  HieraSparseは、長文脈推論で自己注意計算とKVキャッシュ容量が増大する問題に対し、KVを密ブロックとN:M半構造化疎ブロックへ分け、GPUの疎テンソルコアで直接処理する方式である。NVIDIA L40S実機では、同じ疎性のMUSTAFARに対して最大1.2倍高いKV圧縮率と4.57倍の注意カーネル高速化を示す。

- **2026-04 · [Flux Attention: Context-Aware Hybrid Attention for Efficient LLMs Inference](2026-2604.07394-flux-attention-context-aware-hybrid-attention-for-efficient-llms-inferen.md)**  
  実装：[✓](https://github.com/qqtang-code/FluxAttention) ・ リポジトリ内被引用：0  
  Flux 注意機構は、長文LLMの各Transformer層で完全注意（Full 注意機構; FA）を維持するか、疎注意（Sparse 注意機構; SA）へ切り替えるかを、入力プロンプトの文脈に応じて学習した軽量ルータで決める方式である。

- **2026-04 · [Composing Sparse Attention via Learned Grouping](2026-2604.03260-composing-sparse-attention-via-learned-grouping.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerのsoftmax注意は、長さnの系列に対してトークン対をほぼ全て評価するため、長文では演算量とメモリアクセスが二次的に増える。GPT-2 124MのPG-19では、全注意を微調整した場合のPPL31.4に対しFocusは30.3で改善する。

- **2026-02 · [Token Sparse Attention: Efficient Long-Context Inference with Interleaved Token Selection](2026-2602.03216-token-sparse-attention-efficient-long-context-inference-with-interleaved.md)**  
  実装：[✓](https://github.com/dongwonjo/Token-Sparse-Attention) ・ リポジトリ内被引用：0  
  トークン Sparse 注意機構は、長文脈のプリフィルで注意計算の対象トークンを減らすが、元の系列からトークンを永久に捨てない方式である。LLaMA-3.1-8B-InstructのRULERでは、FlashAttentionの128K注意処理を基準とする速度が1.00倍から1.36倍となり、平均正答率は87.01%から87.02%とほぼ不変だった。

- **2026-02 · [S2O: Early Stopping for Sparse Attention via Online Permutation](2026-2602.22575-s2o-early-stopping-for-sparse-attention-via-online-permutation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これは単にTop-Kブロックを固定数選ぶ方式ではなく、実行中の寄与を見て処理を止める方式である。Llama-3.1-8Bの128K入力では、著者は注意演算約7.5倍、事前充填のエンドツーエンド3.81倍の高速化を報告する。

- **2026-02 · [Light Forcing: Accelerating Autoregressive Video Diffusion via Sparse Attention](2026-2602.04789-light-forcing-accelerating-autoregressive-video-diffusion-via-sparse-att.md)**  
  実装：[✓](https://github.com/chengtao-lv/LightForcing) ・ リポジトリ内被引用：0  
  Light Forcingは、自己回帰型動画拡散モデルの注意演算を疎化するとき、動画の後半に画質劣化が蓄積する問題と、長い履歴の重要フレームを捨ててしまう問題を同時に扱う推論高速化方式である。

- **2026-01 · [Sparse Attention as Compact Kernel Regression](2026-2601.22766-sparse-attention-as-compact-kernel-regression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、sparsemaxやα-entmaxなどの疎注意は、関連性の低いトークンへ正確にゼロの重みを割り当てる。

- **2026-01 · [Mixture of Distributions Matters: Dynamic Sparse Attention for Efficient Video Diffusion Transformers](2026-2601.11641-mixture-of-distributions-matters-dynamic-sparse-attention-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎注意は一部の問い合わせ・鍵の組を省くが、あらかじめ固定した疎パターンは生成途中で変わる注意分布を十分に表せず、動的に重要位置を再探索する方式は探索自体が重くなる。

- **2025-12 · [Leveraging KV Similarity for Online Structured Pruning in LLMs](2025-2512.07090-leveraging-kv-similarity-for-online-structured-pruning-in-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事前学習済み言語モデルの構造化枝刈りは、重みや注意ヘッドを削ることで推論費用を下げるが、較正用の入力分布が実際の生成入力と異なる場合、精度低下が大きい。著者のLLaMA-2-13B実験では50%省略条件の常識推論7課題平均が無省略69.51%から65.90%となり、バッチ128では遅延を46.6%、メモリを33.6%削減した。

- **2025-11 · [Optimizing Native Sparse Attention with Latent Attention and Local Global Alternating Strategies](2025-2511.00819-optimizing-native-sparse-attention-with-latent-attention-and-local-globa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の言語モデルでは、すべての過去トークンへ注意を計算する密な注意は計算・メモリ転送とも高価である。Native Sparse 注意機構（NSA）は、直近の窓、圧縮した過去ブロック、重要ブロックの選択という三つの枝を同じ注意層に置き、それらの出力をゲートで混ぜる。

- **2025-11 · [OmniSparse: Training-Aware Fine-Grained Sparse Attention for Long-Video MLLMs](2025-2511.12201-omnisparse-training-aware-fine-grained-sparse-attention-for-long-video-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の疎注意は推論時に重要そうな鍵だけを残す方式が多く、全注意で学習したモデルへ疎化を後付けすると、学習時と推論時の注意分布の不一致が生じる。論文の表1では、256フレーム・約65,600トークン条件で注意演算量を72.6%、鍵・値キャッシュ容量を53.4%削減しながら、動画質問応答の精度を概ね維持した。

### 2年前（2024-11〜2025-10）

- **2025-02 · [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](2025-2502.11089-native-sparse-attention-hardware-aligned-and-natively-trainable-sparse-a.md)**  
  実装：✓ ・ リポジトリ内被引用：149  
  Native Sparse 注意機構（NSA）は、長文脈Transformerの注意演算を、圧縮した長距離文脈、入力依存で選んだ重要ブロック、直近の局所窓という三つの枝に分ける疎注意方式である。注意カーネルは64K文脈で順伝播最大9.0倍、逆伝播最大6.0倍の実測高速化を報告する。

- **2025-02 · [MoBA: Mixture of Block Attention for Long-Context LLMs](2025-2502.13189-moba.md)**  
  実装：[✓](https://github.com/MoonshotAI/MoBA) ・ リポジトリ内被引用：101  
  MoBAは各問い合わせが関連KVブロックを動的選択するMoE型疎注意で、1M文脈の品質を完全注意に近く保ちつつ注意層前処理を最大6.5倍高速化する。

- **2025-02 · [FlexPrefill: A Context-Aware Sparse Attention Mechanism for Efficient Long-Sequence Inference](2025-2502.20766-flexprefill-a-context-aware-sparse-attention-mechanism-for-efficient-long-context-inference.md)**  
  実装：[✓](https://github.com/bytedance/FlexPrefill) ・ リポジトリ内被引用：67  
  要点: FlexPrefillは、長文プリフィルの注意計算を一律の疎パターンへ置き換えるのではなく、入力と注意ヘッドごとに「クエリごとに見る場所が違う多様型」か「多くのクエリが似た場所を見る構造型」かを判定し、その型に合う索引だけを累積注意量の閾値まで選ぶ。これにより、必要なヘッドには多く、簡単なヘッドには少ない計算予算を割り当てる。

- **2025-03 · [XAttention: Block Sparse Attention with Antidiagonal Scoring](2025-2503.16428-xattention-block-sparse-attention-with-antidiagonal-scoring.md)**  
  実装：[✓](https://github.com/mit-han-lab/x-attention) ・ リポジトリ内被引用：52  
  すべての過去トークンが同じように重要とは限らないため、注意行列の重要な領域だけを計算するブロック疎注意（block-sparse 注意機構）が提案されてきた。RULERやLongBenchでは全注意に近い精度を保ち、注意演算部分では最大13.5倍の高速化を報告する。

- **2025-02 · [SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference](2025-2502.18137-spargeattn-accurate-sparse-attention-accelerating-any-model-inference.md)**  
  実装：[✓](https://github.com/thu-ml/SpargeAttn) ・ リポジトリ内被引用：38  
  自己類似度を使って重要ブロックを予測し、残ったブロックにもGPUワープ単位のsoftmax判定を適用する学習不要の疎注意演算子。近似誤差の許容範囲を層ごとに調整し、言語・画像・動画で実測性能と品質を比較する。

- **2024-12 · [SCBench: A KV Cache-Centric Analysis of Long-Context Methods](2024-2412.10319-scbench-a-kv-cache-centric-analysis-of-long-context-methods.md)**  
  実装：✓ ・ リポジトリ内被引用：36  
  共有長文脈を複数ターンで再利用する12タスクを用い、KV生成・圧縮・検索・読み込みの各方式が初回だけでなく後続要求でどう崩れるかを比較する。

- **2024-11 · [Squeezed Attention: Accelerating Long Context Length LLM Inference](2024-2411.09688-squeezed-attention-accelerating-long-context-length-llm-inference.md)**  
  実装：[✓](https://github.com/SqueezeAILab/SqueezedAttention) ・ リポジトリ内被引用：27  
  中心的な前提：入力の大部分が、複数リクエスト間で変化しない固定文書・指示・例示である。前処理で固定文脈の鍵をクラスタ化し、オンラインの問い合わせに関連する元の鍵・値だけを読出す。

- **2025-02 · [Twilight: Adaptive Attention Sparsity with Hierarchical Top-p Pruning](2025-2502.02770-twilight-adaptive-attention-sparsity-with-hierarchical-top-p-pruning.md)**  
  実装：[✓](https://github.com/tsinghua-ideal/Twilight) ・ リポジトリ内被引用：24  
  疎注意（sparse 注意機構）は参照対象を重要トークンへ限定して帯域を節約するが、従来の多くの方式は選択数を固定した上位k件（top-k）方式である。

- **2025-09 · [InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation](2025-2509.24663-infllm-v2-dense-sparse-switchable-attention-for-seamless-short-to-long-a.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  すべての過去トークンを見る密注意は安定した品質を持つが、長い入力を処理すると計算量とGPUメモリ帯域の双方が制約になる。第一に、元モデルの問い合わせ・鍵・値射影をそのまま共有し、短い系列では密注意、長い系列では疎注意へ切り替える。

- **2025-06 · [SeerAttention-R: Sparse Attention Adaptation for Long Reasoning](2025-2506.08889-seerattention-r-sparse-attention-adaptation-for-long-reasoning.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：18  
  思考連鎖が1万トークンを超える推論モデルでは、1トークン生成するたび全過去KVを読む注意が重くなる。SeerAttention-Rは、元モデルを変えずに小さなゲートだけを学習し、「今回のクエリが見るべきKVブロック」を予測してデコード注意を疎化する。

- **2025-02 · [RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression](2025-2502.14051-rocketkv-accelerating-long-context-llm-inference-via-two-stage-kv-cache-.md)**  
  実装：[✓](https://github.com/NVlabs/RocketKV) ・ リポジトリ内被引用：18  
  大規模言語モデルの復号では、過去トークンの鍵・値（KV）を保存することで、同じ過去文脈の線形層を繰り返し計算することを避けられる。論文はLlama3.1-70B-Instruct、バッチ32、32K文脈のFP16 KVが約320 GBに達する例を挙げる。

- **2025-07 · [Compactor: Calibrated Query-Agnostic KV Cache Compression with Approximate Leverage Scores](2025-2507.08143-compactor-calibrated-query-agnostic-kv-cache-compression-with-approximat.md)**  
  実装：[✓](https://github.com/vnchari/compactor-vllm) ・ リポジトリ内被引用：11  
  近似レバレッジスコアで質問非依存にKVを選別し、文脈別の圧縮耐性を校正してLongBenchで完全KV相当の性能を保ちながら平均68%のKVメモリを削減する。

- **2025-02 · [Tactic: Adaptive Sparse Attention with Clustering and Distribution Fitting for Long-Context LLMs](2025-2502.12216-tactic-adaptive-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  既存の疎注意は重要なトークンだけを読むが、各注意ヘッドに同数のトークンを割り当てると、注意が集中するヘッドでは読み過ぎ、広く分散するヘッドでは読み足りない。

- **2025-07 · [RefreshKV: Updating Small KV Cache During Long-form Generation](2025-a2b748353aae-refreshkv-updating-small-kv-cache-during-long-form-generation.md)**  
  実装：[✓](https://github.com/carriex/refreshkv) ・ リポジトリ内被引用：10  
  従来のKVキャッシュ削除方式は、プリフィル直後や過去の注意得点から残すトークンを選び、それ以外の鍵値を捨てる。

- **2025-07 · [Efficient Attention Mechanisms for Large Language Models: A Survey](2025-2507.19595-efficient-attention-mechanisms-for-large-language-models-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  独自の統一実験ではなく既存研究の概念・設計制約を統合し、理論計算量と実測速度、疎演算とKV容量削減の違いを強調する。

- **2025-04 · [MMInference: Accelerating Pre-filling for Long-Context VLMs via Modality-Aware Permutation Sparse Attention](2025-2504.16083-mminference-accelerating-pre-filling-for-long-context-vlms-via-modality-.md)**  
  実装：[✓](https://aka.ms/MMInference) ・ リポジトリ内被引用：9  
  MMInferenceは、長い動画や動画とテキストが混在する視覚言語モデル（Vision-Language モデル; VLM）の入力処理段階を、モダリティごとの疎注意パターンに合わせて高速化する。報告される8.3倍は1Mトークンでのプリフィル時間に関する値であり、生成段階の一トークン時間ではない。

- **2025-10 · [NOSA: Native and Offloadable Sparse Attention](2025-2510.13602-nosa-native-and-offloadable-sparse-attention.md)**  
  実装：[✓](https://github.com/thunlp/NOSA) ・ リポジトリ内被引用：7  
  NOSAは、学習可能な疎注意（trainable sparse 注意機構）とCPUへのKVキャッシュ退避を両立させるために、注意先の選択パターンを学習段階から転送局所性の高いものへ制約する手法である。

- **2025-08 · [TinyServe: Query-Aware Cache Selection for Efficient LLM Serving](2025-2509.12211-tinyserve-query-aware-cache-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  QueryごとにKVページの関連度を軽量メタデータで推定し、必要ページだけを融合CUDAカーネルで読むことで小型LLMサービングの復号とメモリ移動を削減する。

- **2025-07 · [Accelerating Prefilling via Decoding-time Contribution Sparsity](2025-2507.21526-accelerating-prefilling-via-decoding-time-contribution-sparsity.md)**  
  実装：[✓](https://aka.ms/TriangleMix) ・ リポジトリ内被引用：5  
  TriangleMixは、長文脈言語モデルのプリフィルを高速化するために、注意スコアが大きいことと、最終的なデコード予測へ大きく寄与することは同じではないという性質を利用する。従来の動的疎注意は、注意スコアが大きそうなブロックを入力から推定し、それらだけを計算する。その層だけを単純な三角形状の静的注意へ置き換え、他の層は密注意または動的疎注意を維持する。

- **2025-03 · [Progressive Sparse Attention: Algorithm and System Co-design for Efficient Attention in LLM Serving](2025-2503.00392-progressive-sparse-attention-algorithm-and-system-co-design-for-efficien.md)**  
  実装：[✓](https://github.com/ASISys/PSAttention) ・ リポジトリ内被引用：5  
  Progressive Sparse 注意機構（PSA）は、長文脈大規模言語モデルの推論サービングで、必要なKVキャッシュのブロックを要求ごと・層ごとに動的に選ぶ方式である。

- **2025-08 · [Sparse Attention across Multiple-context KV Cache](2025-2508.11661-sparse-attention-across-multiple-context-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  一般の単一文書KV圧縮とは異なり、文書ごとのKVキャッシュはそれぞれ独立した位置関係のもとで作られている。原著表1の系列保持率は14.9%、再計算率は14.3%である。

- **2025-06 · [Kinetics: Rethinking Test-Time Scaling Laws](2025-2506.05333-kinetics-rethinking-test-time-scaling-laws.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/Kinetics) ・ リポジトリ内被引用：4  
  Sadhukhanらは、モデルパラメータ演算・注意演算・KVメモリアクセスをまとめた等価演算量（equivalent FLOPs、eFLOPs）を導入し、モデル規模、生成長、試行回数をどのように選ぶべきか再分析した。提案するKineticsでは、長い思考過程のKV読出しが増えるため、単純に小さなモデルで長く考える戦略が過大評価される。

- **2025-10 · [VideoNSA: Native Sparse Attention Scales Video Understanding](2025-2510.02295-videonsa-native-sparse-attention-scales-video-understanding.md)**  
  実装：[✓](https://github.com/Espere-1119-Song/VideoNSA) ・ リポジトリ内被引用：3  
  視覚トークンを事前にまとめて削る方式は計算量を抑えられるが、削った後に質問に必要な細部を復元できないという問題がある。ただし長動画ベンチマークすべてで最良ではなく、推論の理論演算量削減がそのまま実測高速化になっていない。

- **2025-08 · [Trainable Dynamic Mask Sparse Attention](2025-2508.02124-trainable-dynamic-mask-sparse-attention.md)**  
  実装：[✓](https://github.com/flash-algo/flash-sparse-attention) ・ リポジトリ内被引用：3  
  動的 Mask 注意機構（DMA）は、長文脈Transformerの注意機構で「どの過去位置を参照するか」を入力内容から学習しつつ、GPUで効率的に実行できる疎な注意演算へ変換する方式である。

- **2025-04 · [RWKV-X: A Linear Complexity Hybrid Language Model](2025-2504.21463-rwkv-x-a-linear-complexity-hybrid-language-model.md)**  
  実装：[✓](https://github.com/howardhou/RWKV-X) ・ リポジトリ内被引用：3  
  RWKV-Xは、RWKV-7の線形再帰モデルに、長距離の証拠を選択して参照するTop-k Chunk Sparse 注意機構を周期的に挿入するハイブリッド言語モデルである。128K プリフィルではFlashAttention-3を使う密なTransformerとの比較で1.37倍の速度改善を報告する。

- **2025-10 · [PureKV: Plug-and-Play KV Cache Optimization with Spatial-Temporal Sparse Attention for Vision-Language Large Models](2025-2510.25600-purekv-plug-and-play-kv-cache-optimization-with-spatial-temporal-sparse-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長い動画はフレームごとに多数の視覚トークンを持つため、事前入力（プリフィル）では注意計算量が増え、生成（デコード）では過去のKVを保持するメモリが増える。従来の重要度に基づくKV削除は、各層の注意スコアを集計して重要トークンを残す方式が多い。

- **2025-10 · [Long-Context Modeling with Dynamic Hierarchical Sparse Attention for Memory-Constrained LLM Inference](2025-2510.24606-long-context-modeling-with-dynamic-hierarchical-sparse-attention-for-mem.md)**  
  実装：[✓](https://github.com/xiongsiheng/DHSA) ・ リポジトリ内被引用：2  
  動的 Hierarchical Sparse 注意機構（DHSA）は、長い入力に対する自己注意の計算を削減するため、注意行列のどこを残すかを入力内容に応じて予測する方式である。128K文脈で最大10.66倍という値はFlashAttention-2と比較した注意カーネル単体の速度である。

- **2025-05 · [AnchorAttention: Difference-Aware Sparse Attention with Stripe Granularity](2025-2505.23520-anchorattention-difference-aware-sparse-attention-with-stripe-granularit.md)**  
  実装：[✓](https://github.com/yuzhouzhang9/Anchor-Attention) ・ リポジトリ内被引用：2  
  疎注意（sparse 注意機構）は重要な位置だけを選べるが、従来の動的方式は重要位置の探索自体に時間がかかり、128×128などの粗いブロック単位で残すと重要でない列まで計算する。

- **2025-04 · [Hardware-aligned Hierarchical Sparse Attention for Efficient Long-term Memory Access](2025-2504.16795-hardware-aligned-hierarchical-sparse-attention-for-efficient-long-term-m.md)**  
  実装：[✓](https://github.com/ant-research/long-context-modeling) ・ リポジトリ内被引用：2  
  再帰型ニューラルネットワーク（Recurrent Neural Network; RNN）や状態空間モデル（State Space モデル; SSM）は、過去を固定次元の状態に圧縮するため、文脈が伸びても注意機構のような二乗計算や増大するKVキャッシュを必要としない。

- **2025-02 · [InfiniteHiP: Extending Language Model Context Up to 3 Million Tokens on a Single GPU](2025-2502.08910-infinitehip-extending-language-model-context-up-to-3-million-tokens-on-a.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈の大規模言語モデル推論には三つの問題がある。第一に、注意機構が参照する過去トークンが増えると演算量とメモリアクセスが増える。原著は単一L40S 48GBで最大約300万トークンの文脈を扱えるとし、同条件でSGLangの比較対象に対して復号処理量が約7.25倍と報告する。

- **2025-02 · [APB: Accelerating Distributed Long-Context Inference by Passing Compressed Context Blocks across GPUs](2025-2502.12085-apb-accelerating-distributed-long-context-inference-by-passing-compresse.md)**  
  実装：[✓](https://github.com/thunlp/APB) ・ リポジトリ内被引用：2  
  系列並列化（sequence parallelism）は入力を複数GPUへ分けることで計算を並列に進めるが、完全な注意計算を維持する方式ではGPU間で大量の情報を交換し、計算総量も大きい。原著は最大速度改善をFlashAttention比9.2倍、RingAttention比4.2倍、StarAttention比1.6倍と報告する。

- **2025-10 · [Understanding and Improving Length Generalization in Hierarchical Sparse Attention Models](2025-2510.17196-understanding-and-improving-length-generalization-in-hierarchical-sparse.md)**  
  実装：[✓](https://github.com/jacky-leng/length-generalizable-sparse-attention) ・ リポジトリ内被引用：1  
  長いコンテキストを扱うTransformerは、過去トークンの全KVを参照できる一方、文脈長の増加とともに注意計算・メモリ参照の費用が大きくなる。Sliding Window 注意機構（SWA）は局所窓へ制限することで負荷を抑えるが、窓の外にある事実を直接検索できない。

- **2025-10 · [Alleviating Forgetfulness of Linear Attention by Hybrid Sparse Attention and Contextualized Learnable Token Eviction](2025-2510.20787-alleviating-forgetfulness-of-linear-attention-by-hybrid-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  線形注意（linear 注意機構）やGated DeltaNetのような再帰的トークン混合器は、過去の全履歴を固定サイズの状態へ畳み込むことで、復号1ステップあたりの時間と記憶量を入力長に依存させない。

- **2025-08 · [Efficient Attention Methods: Hardware-efficient, Sparse, Compact, and Linear Attention](2025-483ca98d7491-efficient-attention-methods-hardware-efficient-sparse-compact-and-linear.md)**  
  実装：[✓](https://github.com/attention-survey/Efficient_Attention_Survey) ・ リポジトリ内被引用：1  
  原著は20ページで、注意計算の数式、GPUの演算性能とメモリ帯域、事前入力処理と復号の律速差を説明したうえで、ハードウェア効率化、コンパクト注意（Compact 注意機構）、疎注意（Sparse 注意機構）、線形注意（Linear 注意機構）の四系統を共通の記法で比較する。

- **2025-02 · [Top-Theta Attention: Sparsifying Transformers by Compensated Thresholding](2025-2502.08363-top-theta-attention.md)**  
  実装：[✓](https://github.com/huawei-csl/top-theta-attention) ・ リポジトリ内被引用：1  
  Top-Thetaは層・ヘッド・位置別の校正しきい値で注意重みを選び、行ごとの上位k選択（top-k）を避けて注意計算とV行読出しを減らす。LLaMA系評価では注意要素やV読出しを最大10分の1程度まで減らす条件を示す一方、強い疎化や実装条件によって品質・実速度の利得が変わる。

- **2025-10 · [The End of Transformers? On Challenging Attention and the Rise of Sub-Quadratic Architectures](2025-2510.05364-the-end-of-transformers-on-challenging-attention-and-the-rise-of-sub-qua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意やRNN、SSMは履歴を固定サイズの状態へ圧縮するため、長い履歴を一定のメモリで処理できる一方、任意の過去トークンを厳密に検索する能力に制約が生じる。

- **2025-10 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2025-2510.09883-delta-dynamic-layer-aware-token-attention-for-efficient-long-context-rea.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：0  
  推論特化のLLMは数学・科学問題で長いChain-of-Thoughtを生成する。古いKVを削除する方式は容量と計算の両方を減らせるが、思考過程の後半で以前の中間結論が再び重要になったとき、削除済みのKVを取り戻せない。DS-Qwen-1.5Bの合成18kデコードでは403秒から261秒へ短縮し、スループット2921から4517 トークン/sへ増加する。

- **2025-10 · [Adamas: Hadamard Sparse Attention for Efficient Long-Context Inference](2025-2510.18413-adamas-hadamard-sparse-attention-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Adamasは、長文脈LLMの復号時に、過去のすべてのKey/Value（KV）を読み込んで正確な注意を計算する代わりに、現在のQueryに関連する過去トークンだけを選択する疎注意方式である。

- **2025-06 · [Lag-Relative Sparse Attention In Long Context Training](2025-2506.11498-lag-relative-sparse-attention-in-long-context-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文の対象は、長文脈の事後学習で使用する注意機構を、推論時のKVキャッシュ圧縮と整合させる方法である。

- **2025-06 · [Accelerating Sparse Transformer Inference on GPU](2025-2506.06095-accelerating-sparse-transformer-inference-on-gpu.md)**  
  実装：[✓](https://github.com/HeyDavid633/PPoPP26-pap161-AE) ・ リポジトリ内被引用：0  
  STOF（Sparse Transformer with Operator Fusion）は、Transformerの疎な注意マスクをGPU上で実際の計算削減へ結び付けることと、注意演算の後に続く行列積・正規化・加算などの融合境界を入力形状に応じて選ぶことを、ひとつの推論実行基盤として扱う。主張は二層に分けて読む必要がある。

- **2025-02 · [Neural Attention Search](2025-2502.13251-neural-attention-search.md)**  
  実装：[✓](https://github.com/automl/NeuralAttentionSearch) ・ リポジトリ内被引用：0  
  Neural 注意機構 Search（NAtS）は、長い系列を扱うTransformerで、各トークンの鍵・値キャッシュをいつまで残すべきかを学習する疎注意方式である。

### 3年前（2023-11〜2024-10）

- **2024-06 · [Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference](2024-2406.10774-quest.md)**  
  実装：[✓](https://github.com/mit-han-lab/Quest) ・ リポジトリ内被引用：295  
  KVページのキー最小・最大値と現在クエリから重要度上界を推定し、上位ページだけを読むことで全KVを保持したまま長文脈注意の帯域を削減し最大7.03倍高速化。

- **2024-07 · [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](2024-2407.02490-minference.md)**  
  実装：[✓](https://github.com/microsoft/MInference) ・ リポジトリ内被引用：198  
  注意ヘッドを3種の疎パターンへ割り当て、入力ごとの重要位置を動的推定して長文脈プリフィルを専用GPUカーネルで高速化する。

- **2024-09 · [RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval](2024-2409.10516-retrievalattention-accelerating-long-context-llm-inference-via-vector-re.md)**  
  実装：✓ ・ リポジトリ内被引用：79  
  RetrievalAttentionは、長文脈の大規模言語モデルが自己回帰復号で過去のすべての鍵値を走査する負担を、現在の質問に重要なトークンだけを動的に検索することで減らす手法である。しかし注意の質問と鍵は異なる重み行列で射影され、ベクトル分布がずれるため、一般的な索引をそのまま使うと高い再現率を得るために鍵の30～50%を走査しなければならない。

- **2024-10 · [SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs](2024-2410.13276-seerattention.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：78  
  Q/Kからブロック単位の重要度を学習する軽量ゲートとブロック疎FlashAttentionを組み合わせ、長文プリフィルの注意計算を動的に削減する。

- **2024-06 · [Loki: Low-Rank Keys for Efficient Sparse Attention](2024-2406.02542-loki-low-rank-keys-for-efficient-sparse-attention.md)**  
  実装：[✓](https://github.com/hpcgroup/loki) ・ リポジトリ内被引用：52  
  キーの低ランク性を使い、低次元スコアで候補KVを選んでから全次元注意を計算し、品質を保ちながら注意計算を最大約45%短縮する疎注意法。

- **2024-08 · [Post-Training Sparse Attention with Double Sparsity](2024-2408.07092-post-training-sparse-attention-with-double-sparsity.md)**  
  実装：[✓](https://github.com/andy-yang-1/DoubleSparse) ・ リポジトリ内被引用：27  
  長文脈の自己回帰生成では、各新規トークンの問い合わせに対して過去の鍵・値キャッシュ（KVキャッシュ）を読み出すため、注意計算がGPUのメモリ帯域に律速されやすい。注意スコアへ大きく寄与する特徴チャネルを学習後の少量データで層別に校正し、そのチャネルだけを連続配置した小さなラベルキャッシュを作る。

- **2024-06 · [SampleAttention: Near-Lossless Acceleration of Long Context LLM Inference with Adaptive Structured Sparse Attention](2024-2406.15486-sampleattention-near-lossless-acceleration-of-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  SampleAttentionは、長い入力文脈を持つ大規模言語モデル（Large Language モデル、LLM）の事前計算（プリフィル）を高速化するため、注意（注意機構）行列の重要な位置だけを実行時に選ぶ構造化疎注意方式である。

- **2024-09 · [Block-Attention for Efficient Prefilling](2024-2409.15355-block-attention-for-efficient-prefilling.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Block-Attention) ・ リポジトリ内被引用：18  
  検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した各文書を互いに独立した注意ブロックとして事前計算し、同じ文書が別質問で再利用されたらKVキャッシュを再計算しない。

- **2024-10 · [TidalDecode: Fast and Accurate LLM Decoding with Position Persistent Sparse Attention](2024-2410.05076-tidaldecode-fast-and-accurate-llm-decoding-with-position-persistent-spar.md)**  
  実装：[✓](https://github.com/DerrickYLJ/TidalDecode) ・ リポジトリ内被引用：17  
  系列が長くなるほど鍵値キャッシュは線形に増えるため、1トークンずつ生成する復号では演算より高帯域メモリからの読出しが律速になりやすい。論文の例ではLLaMA-2-7Bを半精度、128K文脈で使うと鍵値キャッシュだけで64GBになる。疎注意（sparse 注意機構）は全過去トークンの一部だけを注意計算へ入れることで、この読出し量を減らす。

- **2024-06 · [Mixture of Attention Spans: Optimizing LLM Inference Efficiency with Heterogeneous Sliding-Window Lengths](2024-2406.14909-mixture-of-attention-spans-optimizing-llm-inference-efficiency-with-heterogeneous-sliding-window-lengths.md)**  
  実装：[✓](https://github.com/thu-nics/MoA) ・ リポジトリ内被引用：16  
  ヘッドごとの局所性と入力長への伸び方を勾配で測り、異種sliding-ウィンドウ規則を自動探索して静的KV マスクへ落とすMoA。

- **2024-10 · [ZipVL: Accelerating Vision-Language Models Through Dynamic Token Sparsity](2024-2410.08584-zipvl-accelerating-vision-language-models-through-dynamic-token-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  入力全体を処理するプリフィル段階では注意計算が長い系列に対して重くなり、続くデコード段階では生成トークンが過去のKey/Value（KV）を繰り返し読み出すためメモリ帯域が問題になる。ただし、前者はバッチ1の最初のトークンまでの時間、後者は各方式が単一GPUで収容できる最大バッチを使った生成処理率であり、同じ測定条件の速度指標ではない。

- **2024-10 · [HSR-Enhanced Sparse Attention Acceleration](2024-2410.10165-hsr-enhanced-sparse-attention-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  最新版v2の付録Aには、提案HSRアルゴリズム自体を実装していないことが明記されている。実験で確認したのはSoftmax近似の品質側である。

- **2023-11 · [One Pass Streaming Algorithm for Super Long Token Attention Approximation in Sublinear Space](2023-2311.14652-one-pass-streaming-algorithm-for-super-long-token-attention-approximatio.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長大な文脈を扱う注意機構では、問い合わせ、鍵、値の各行列から計算される注意重みが系列長に伴って大きくなる。主結果は実験的な高速化ではなく、厳密な入力条件の下での確率的な誤差・空間・復元時間の保証である。

- **2024-08 · [X-former Elucidator: Reviving Efficient Attention for Long Context Language Modeling](2024-16427914d16d-x-former-elucidator-reviving-efficient-attention-for-long-context-langua.md)**  
  実装：[✓](https://github.com/Hsword/X-former-Elucidator) ・ リポジトリ内被引用：1  
  大規模言語モデル（Large Language モデル; LLM）の長文脈処理では、標準の自己注意（self-注意機構）が系列長nに対して概ね二乗の計算を必要とし、特に学習や長い入力のプリフィル（プリフィル）でメモリ・演算の負担が増える。著者らはNVIDIA Titan RTX 24GB群で計21,114 GPU時間を費やしたと報告する。

- **2024-07 · [S2-Attention: Hardware-Aware Context Sharding Among Attention Heads](2024-2407.17678-s2-attention-hardware-aware-context-sharding-among-attention-heads.md)**  
  実装：[✓](https://github.com/linxihui/dkernel) ・ リポジトリ内被引用：0  
  しかし実GPUでは、疎な位置を飛ばすための分岐、細かなタイル、共有メモリ（SRAM）への同じKVの再読込が増え、密注意を高度に融合したFlashAttention-2より遅くなることがある。また、推論中に不要なKVを削除する方式では、PagedAttentionのページ管理との不整合や将来再参照されるKVの保持が問題となる。

### 4年前（2022-11〜2023-10）

- **2023-08 · [LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models](2023-2308.16137-lm-infinite-zero-shot-extreme-length-generalization-for-large-language-m.md)**  
  実装：[✓](https://github.com/Glaciohound/LM-Infinite) ・ リポジトリ内被引用：64  
  LM-Infiniteは、短い系列で学習した大規模言語モデルを追加学習なしで長文脈へ外挿するため、推論時の注意範囲と位置距離の扱いだけを変更する方式である。論文は元の完全注意に対してデコードを約2.7倍高速化し、GPUメモリを最大7.5倍削減したと報告する。

- **2023-07 · [LongNet: Scaling Transformers to 1,000,000,000 Tokens](2023-2307.02486-longnet-scaling-transformers-to-1-000-000-000-tokens.md)**  
  実装：[✓](https://aka.ms/LongNet) ・ リポジトリ内被引用：43  
  LongNetは、自己注意の計算量が系列長Nの二乗で増える問題を、拡張注意（dilated 注意機構）で解くTransformer変種である。

- **2023-05 · [Landmark Attention: Random-Access Infinite Context Length for Transformers](2023-2305.16300-landmark-attention-random-access-infinite-context-length-for-transformer.md)**  
  実装：[✓](https://github.com/epfml/landmark-attention) ・ リポジトリ内被引用：41  
  目印注意（Landmark 注意機構）は、長い文章を一定長のブロックに分け、それぞれの末尾へ特別な目印トークンを挿入し、注意機構そのものに「どの過去ブロックを読み戻すべきか」を学習させる方式である。また、LLaMA-7Bを長さ512の文脈で15,000ステップ微調整した実験では、32Kを超える入力から埋め込んだ合言葉を検索できることを示した。

- **2023-05 · [Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers](2023-2305.15805-dynamic-context-pruning-for-efficient-and-interpretable-autoregressive-transformers.md)**  
  実装：[✓](https://github.com/sanagno/adaptively_sparse_attention) ・ リポジトリ内被引用：31  
  動的 Context 枝刈りは、生成の途中で「今後のトークンが参照する価値が低い」と学習した過去トークンを、注意対象とキー・バリュー（Key-Value; KV）キャッシュから動的に削除する。固定窓のように距離だけで落とさず、層ごとの学習可能な相互作用スコアで削除時点を決める。

- **2023-10 · [HyperAttention: Long-context Attention in Near-Linear Time](2023-2310.05869-hyperattention-long-context-attention-in-near-linear-time.md)**  
  実装：[✓](https://github.com/insuhan/hyper-attn) ・ リポジトリ内被引用：22  
  局所性鋭敏ハッシュで注意行列の大きな要素を効率的に見つけ、残りの小さい成分をサンプリングで近似する。全注意行列を作らずに正規化と値の加重和を計算し、長文脈での計算量を削減する。

- **2023-05 · [Unlimiformer: Long-Range Transformers with Unlimited Length Input](2023-2305.01625-unlimiformer-long-range-transformers-with-unlimited-length-input.md)**  
  実装：[✓](https://github.com/abertsch72/unlimiformer) ・ リポジトリ内被引用：15  
  文書が長いほど参照すべきキーと値の数が増え、推論時のメモリ使用量と注意計算が膨らむ。長文専用の注意構造へモデルを変更する方式は再事前学習や追加の位置埋め込み学習を要する場合がある。

- **2023-10 · [Context Compression for Auto-regressive Transformers with Sentinel Tokens](2023-2310.08152-context-compression-for-auto-regressive-transformers-with-sentinel-token.md)**  
  実装：[✓](https://github.com/DRSY/KV_Compression) ・ リポジトリ内被引用：3  
  Ren・Jia・Zhuの研究は、自己回帰型の大規模言語モデル（Large Language モデル; LLM）で、長い入力に伴って増える鍵・値キャッシュ（Key–Value キャッシュ; KVキャッシュ）を、捨てる前に情報を短い表現へ移すことで削減する方式を提案する。

### 5年前（2021-11〜2022-10）

- **2021-12 · [LongT5: Efficient Text-To-Text Transformer for Long Sequences](2021-2112.07916-longt5-efficient-text-to-text-transformer-for-long-sequences.md)**  
  実装：[✓](https://github.com/google-research/longt5) ・ リポジトリ内被引用：13  
  T5のエンコーダを長文向けに置き換え、各層でブロック集約した大域トークンを一時的に作る注意機構を提案する。重要文生成による事前学習と組み合わせ、要約・質問応答で長い入力の情報を利用する。論文の主な評価はモデル品質と学習時の計算費用であり、デコード専用の推論サービング実験とは区別する。

- **2021-11 · [Memory-efficient Transformers via Top-k Attention](2021-c7730f7e7292-memory-efficient-transformers-via-top-k-attention.md)**  
  実装：[✓](https://github.com/ag1988/top_k_attention) ・ リポジトリ内被引用：7  
  既存の効率的注意には、ハッシュや局所窓で計算する組合せを制限する方式と、注意関数自体を近似する線形注意がある。

### 6年前（2020-11〜2021-10）

- **2020-12 · [SpAtten: Efficient Sparse Attention Architecture with Cascade Token and Head Pruning](2020-2012.09852-spatten-efficient-sparse-attention-architecture-with-cascade-token-and-head-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：70  
  累積注意確率とヘッド出力から重要トークン・ヘッドを動的にカスケード枝刈りし、確率分布に応じた段階的量子化と専用top-k回路で注意の計算・DRAM転送を同時に削減する。

- **2021-10 · [Sanger: A Co-Design Framework for Enabling Sparse Attention using Reconfigurable Architecture](2021-0aaecf5ce8bb-sanger-a-co-design-framework-for-enabling-sparse-attention-using-reconfi.md)**  
  実装：[✓](https://github.com/pku-liang/Sanger) ・ リポジトリ内被引用：16  
  Sangerは、Transformerの注意演算に含まれる重要度の低い接続を入力ごとに選別し、専用ハードウェア上で実際に計算を省くための協調設計である。

- **2021-06 · [Memory-efficient Transformers via Top-k Attention](2021-2106.06899-top-k-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  通常注意は系列長をLとするとL×Lのスコア行列を作るため、長系列ではメモリ使用量が二次的に増える。Top-k 注意機構は、各クエリについて全キーとのスコアから上位k個だけを残し、クエリをチャンク単位で処理することでピークメモリを系列長に対して線形へ近づける。

- **2021-10 · [Transformer Acceleration with Dynamic Sparse Attention](2021-2110.11299-transformer-acceleration-with-dynamic-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  DSAは、入力ごとに異なる重要な注意位置を安価に予測し、残した位置に限り通常の注意計算を行うことで、密な注意の表現力を可能な限り維持しつつ計算を減らす。90%の注意重みを除く設定で、最初から学習したDSAの三課題平均精度は57.48%、同条件の密なTransformerは56.79%だった。

- **2021-10 · [Scatterbrain: Unifying Sparse and Low-rank Attention Approximation](2021-2110.15343-scatterbrain-unifying-sparse-and-low-rank-attention-approximation.md)**  
  実装：[✓](https://github.com/HazyResearch/scatterbrain) ・ リポジトリ内被引用：4  
  Scatterbrainは、長い系列を処理するTransformerの注意機構を近似する際、疎な重要位置だけを計算する方法と、注意行列を低ランク構造で近似する方法を競合する選択肢ではなく、相補的な成分として同時利用する研究である。

- **2021-05 · [Poolingformer: Long Document Modeling with Pooling Attention](2021-2105.04371-poolingformer-long-document-modeling-with-pooling-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本論文は、長文を処理する変換器（Transformer）の自己注意を、近い単語を精密に参照する第一段と、遠い単語を圧縮して参照する第二段に分ける「Poolingformer」を提案する。

- **2021-03 · [A Practical Survey on Faster and Lighter Transformers](2021-2103.14636-a-practical-survey-on-faster-and-lighter-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  本論文は、Transformerの注意機構が系列長に対して二次の計算・記憶費用を持つという問題を起点に、モデル一般に使える効率化とTransformer固有の構造を変更する効率化を区別して、研究成果を整理した文献調査である。

### 7年前（2019-11〜2020-10）

- **2020-07 · [Big Bird: Transformers for Longer Sequences](2020-2007.14062-big-bird-transformers-for-longer-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：230  
  Big Birdは、系列長に対して二次の計算・メモリ費用が生じる完全自己注意を、局所窓、ランダム接続、少数の大域トークンからなる疎注意へ置き換える長文処理モデルである。各位置が全位置を直接参照する代わりに、近傍の限られた位置、ランダムに選んだ遠距離位置、全体と接続する大域位置だけを見る。論文は同程度のハードウェアで従来より最大8倍長い系列を扱えると報告する。

- **2020-01 · [Reformer: The Efficient Transformer](2020-2001.04451-reformer-the-efficient-transformer.md)**  
  実装：[✓](https://github.com/google/trax/tree/master/trax/models/reformer) ・ リポジトリ内被引用：178  
  第一の制約は、全トークン対の内積を求める標準自己注意が系列長の二乗に比例する計算を要することである。

- **2020-03 · [Efficient Content-Based Sparse Attention with Routing Transformers](2020-2003.05997-efficient-content-based-sparse-attention-with-routing-transformers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/routing_transformer) ・ リポジトリ内被引用：87  
  固定した近傍窓ではなく「内容が近いトークン」をクラスタリングして注意先を決める。局所注意だけでは拾いにくい遠距離依存を残しつつ、各トークンが全系列を見る密な自己注意の二乗コストを削る、初期の内容依存疎注意方式。

- **2019-11 · [Blockwise Self-Attention for Long Document Understanding](2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md)**  
  実装：[✓](https://github.com/xptree/BlockBERT) ・ リポジトリ内被引用：34  
  BlockBERTは、長文の読解に使う双方向エンコーダBERTで、自己注意の計算と活性値保存が系列長の二乗に増える問題を、注意を計算するブロックの組合せを注意頭ごとに限定することで軽減する方式である。系列長1024の事前学習ではRoBERTa-1seq比で最大36.1%のGPUメモリ削減、25.1%の学習時間短縮を示す。
<!-- survey:auto:end -->
