# Linear-Recurrent Language Model Architectures

生成時に文脈長へ比例しない再帰状態で履歴を表す言語モデルのSSM、retention、linear attention、動的状態更新則と有界局所attentionとの混成を扱う。モデルの状態表現・更新則自体の設計を中心に、推論メモリ、速度、想起精度の関係を比較する。

## 分類境界

主要貢献が、生成時に文脈長へ比例しない再帰状態へ履歴を集約するSSM・retention・linear attention・data-dependent recurrenceのモデル構造または状態更新則である言語モデルを含む。有界局所attentionとの混成も含む。通常TransformerのKV保持/圧縮/offload、純kernel/runtime、固定再帰decodeを主要機構としないFFT長畳み込み、test-time gradient updateによるneural memory、recurrenceを部品として使うだけの研究は除く。

### 含める研究

- Selective state-space and linear-time sequence-model architectures
- Recurrent or matrix-state linear-attention update rules
- Retention and dynamic recurrence language-model architectures
- Recurrent plus local-attention hybrids with recurrent sequence modeling as the core

### 含めない研究

- Kernel, compiler, or runtime optimization without a model-operator contribution
- KV cache, checkpoint, or recurrent-state storage/compression policy
- Request-level serving, scheduling, or disaggregation
- Speculative decoding and verification methods
- General-purpose RNN theory with no language-model architecture contribution
- Fixed-state decodingを主要機構としないFFT長畳み込み
- Test-time gradient updateを主機構とするneural memory

## 近傍系統

- [07-kv-cache-optimization-compression](../07-kv-cache-optimization-compression/)
- [09-kernel-runtime-compilation](../09-kernel-runtime-compilation/)
- [13-sparse-attention](../13-sparse-attention/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（46本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/20-linear-recurrent-language-models/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-03 · [M²RNN: Non-Linear RNNs with Matrix-Valued States for Scalable Language Modeling](2026-2603.14360-m-rnn-non-linear-rnns-with-matrix-valued-states-for-scalable-language-mo.md)**  
  実装：[✓](https://github.com/open-lm-engine/lm-engine) ・ リポジトリ内被引用：1  
  線形注意やMamba-2、Gated DeltaNetなどの再帰型方式は固定サイズの状態へ過去を畳み込み、生成時のメモリを一定に保ちやすい。

- **2025-11 · [DiffuMamba: High-Throughput Diffusion LMs with Mamba Backbone](2025-2511.15927-diffumamba-high-throughput-diffusion-lms-with-mamba-backbone.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし拡散Transformerは各ステップで系列全体の注意を再計算し、系列長Lが長くなると注意演算の二乗計算量と中間状態の読み書きが負担になる。一方、過去ブロックの状態を再利用する方式では純Mamba版が2.3倍、混合版が1.9倍と報告され、倍率は復号方式ごとに異なる。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Switching Linear Attention](2026-2609.39034-switching-linear-attention.md)**  
  実装：[✓](https://github.com/lindermanlab/switching-linear-attention) ・ リポジトリ内被引用：0  
  ソフトマックス注意（softmax 注意機構）は過去の各トークンの鍵と値を保持し、現在の問い合わせとの類似度に応じて必要な値を取り出す。1.3Bモデルの単一H100上の生成ではTransformer基準に対して全体スループットが4〜5倍になる一方、より単純なゲート付きDeltaNetより推論で1.25〜1.5倍遅く、学習では約2倍遅い。

- **2026-09 · [Kalman Delta Networks: Uncertainty-aware Associative Memory](2026-2609.07816-kalman-delta-networks-associative-memory.md)**  
  実装：[✓](https://github.com/ngocbh/kalman-delta-networks) ・ リポジトリ内被引用：0  
  固定サイズの線形注意メモリに推定不確実性を持たせ、蓄積証拠に応じて上書き強度をカルマン利得から決めることで、長文脈検索と生成精度を改善する。

- **2026-08 · [SANE: State Anomaly Neutralization for Stable Extreme-Context Delta-Rule Models](2026-2608.22354-sane-state-anomaly-neutralization-for-stable-extreme-context-delta-rule-.md)**  
  実装：[✓](https://github.com/pass-lin/rwkv_ops) ・ リポジトリ内被引用：0  
  SANEはこの形状に合わせ、各チャンク末尾の状態行列を、入力に応じたヘッド別のしきい値で滑らかに圧縮する。

- **2026-06 · [Do Language Models Need Sleep? Offline Recurrence for Improved Online Inference](2026-2605.26099-do-language-models-need-sleep-offline-recurrence-for-improved-online-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの注意機構は過去トークンをキー・値（KV）キャッシュとして保持する。

- **2026-05 · [Interdomain Attention: Beyond Token-Level Key-Value Memory](2026-2605.24330-interdomain-attention-beyond-token-level-key-value-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この方式は必要な過去情報を内容に基づいて選べるが、復号が進むほどKVキャッシュ容量と参照帯域が増える。FineWeb-Eduを用いて125M〜1.3Bパラメータの復号型モデルを学習した結果、同じ再帰状態予算のS4Dだけのモデルより検証パープレキシティが13〜16%低い。

- **2026-05 · [Don't Read Everything: A Curvature-Conditioned Query for Linear Attention](2026-2606.01294-don-t-read-everything-a-curvature-conditioned-query-for-linear-attention.md)**  
  実装：[✓](https://github.com/ledong0110/ccq) ・ リポジトリ内被引用：0  
  線形注意（Linear 注意機構）は、通常のsoftmax注意のように過去トークン全体との注意行列を毎回計算する代わりに、過去の鍵・値の情報を固定サイズの再帰状態へ蓄積する。

- **2026-05 · [Blurry Window Attention](2026-2606.09862-blurry-window-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Blurry Window 注意機構（BLA）は、長い系列の全トークンに注意を向ける通常の自己注意の代わりに、有限サイズの状態から過去の鍵・値情報を補間して読み出す注意機構である。規則学習課題RegBenchでは、比較した線形注意系の中でBLAとSWAが状態量の増加に応じて精度を改善し、BLAは小さな状態でも優位な条件があった。

- **2026-04 · [Long-Context Aware Upcycling: A New Frontier for Hybrid LLM Scaling](2026-2604.24715-long-context-aware-upcycling-a-new-frontier-for-hybrid-llm-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを長文脈で使う場合、通常の全注意機構は過去のキーと値をトークン数に応じて保存し続けるため、GPUメモリが推論可能な文脈長を制約する。実行基盤側も改修し、8基のAMD MI300Xを使って最大約200万トークンの推論を実行した。

- **2026-04 · [FG^2-GDN: Enhancing Long-Context Gated Delta Networks with Doubly Fine-Grained Control](2026-2604.19021-fg-2-gdn-enhancing-long-context-gated-delta-networks-with-doubly-fine-gr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い文脈の自己回帰推論では、通常のソフトマックス注意（softmax 注意機構）が鍵・値キャッシュ（Key-Value Cache、KV Cache）を系列長に応じて保持し、入力一括処理の計算も系列長の二乗で増える。

- **2026-02 · [Online Vector Quantized Attention](2026-2602.03922-online-vector-quantized-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オンラインベクトル量子化注意（Online Vector Quantized 注意機構、OVQ-注意機構）は、長い系列の情報を比較的大きな固定上限の記憶状態へ圧縮しながら、自己注意（self-注意機構）の長距離検索能力に近づける系列混合層である。

- **2026-01 · [MHLA: Restoring Expressivity of Linear Attention via Token-Level Multi-Head](2026-2601.07832-mhla-restoring-expressivity-of-linear-attention-via-token-level-multi-he.md)**  
  実装：[✓](https://github.com/DAGroup-PKU/MHLA) ・ リポジトリ内被引用：0  
  MHLA（Multi-Head Linear 注意機構）は、系列長に対して計算量が線形に増える注意機構を維持しながら、従来の線形注意（linear 注意機構）で失われるトークン間の選択性を回復する構造である。DeiT-TのImageNet-1K正答率は通常の線形注意69.8%からMHLA75.8%へ、通常のソフトマックス注意72.2%も上回った。

- **2026-01 · [Gecko: An Efficient Neural Architecture Inherently Processing Sequences with Arbitrary Lengths](2026-2601.06463-gecko-an-efficient-neural-architecture-inherently-processing-sequences-w.md)**  
  実装：[✓](https://github.com/XuezheMax/gecko-llm) ・ リポジトリ内被引用：0  
  Geckoは、従来のTransformerで長い系列を扱う際の二乗注意計算と、固定窓に分割する方式で過去の情報が失われる問題を、モデル構造そのものから扱う研究である。

### 2年前（2024-11〜2025-10）

- **2024-12 · [Gated Delta Networks: Improving Mamba2 with Delta Rule](2024-2412.06464-gated-delta-networks-improving-mamba2-with-delta-rule.md)**  
  実装：[✓](https://github.com/NVlabs/GatedDeltaNet) ・ リポジトリ内被引用：113  
  本論文は、長文脈を固定容量の状態へ圧縮する線形再帰言語モデルが、記憶の保持と更新を両立しにくい問題を扱う。

- **2024-11 · [MetaLA: Unified Optimal Linear Approximation to Softmax Attention Map](2024-2411.10741-metala-unified-optimal-linear-approximation-to-softmax-attention-map.md)**  
  実装：[✓](https://github.com/BICLab/MetaLA) ・ リポジトリ内被引用：3  
  MetaLAは、従来別々の系列モデルとして説明される線形Transformer、状態空間モデル（State Space モデル; SSM）、線形再帰ニューラルネット（Linear RNN）を、有限サイズの隠れ状態を更新する線形注意（linear 注意機構）の共通形式で扱う研究である。

- **2025-10 · [AuroraLong: Bringing RNNs Back to Efficient Open-Ended Video Understanding](2025-2507.02591-auroralong-bringing-rnns-back-to-efficient-open-ended-video-understandin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AuroraLongは、動画質問応答や詳細な動画字幕生成で問題となる、画像フレーム数に比例して増える視覚トークンを低メモリで処理する多模態言語モデルである。学習済みRWKVの4,096トークンという文脈長と、多数の画像を入力する動画処理との隔たりを埋める設計である。

- **2025-02 · [PICASO: Permutation-Invariant Context Composition with State Space Models](2025-2502.17605-picaso-permutation-invariant-context-composition-with-state-space-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PICASOは、状態空間モデル（State Space モデル、SSM）で検索拡張生成を行うとき、検索された文章を毎回トークン列として読み直す費用を削減する方式である。後者は文章の個数に線形な計算量を持ち、実験では全順列版と近い予測品質を示した。

- **2025-10 · [MeSH: Memory-as-State-Highways for Recursive Transformers](2025-2510.07739-mesh-memory-as-state-highways-for-recursive-transformers.md)**  
  実装：[✓](https://github.com/LivingFutureLab/MeSH/) ・ リポジトリ内被引用：0  
  MeSH（メモリ-as-State-Highways）は、同じTransformerブロックを複数回適用する再帰Transformer（recursive transformer）の性能低下を抑えるため、反復ごとに読み書きを制御する状態メモリを導入する手法である。

- **2025-07 · [Scaling up the State Size of RNN LLMs for Long-Context Scenarios](2025-21fc56600ade-scaling-up-the-state-size-of-rnn-llms-for-long-context-scenarios.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの自己注意（self-注意機構）は、過去の鍵・値（KV）を系列長に比例して保持し、特定位置の情報を取り出せる。400M級Gated DeltaNetの状態を8倍にすると、FDA・SWDE・SQuADの検索課題平均が28.03から37.39へ改善した。

### 3年前（2023-11〜2024-10）

- **2023-12 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](2023-2312.00752-mamba-selective-state-space-linear-time-inference.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：261  
  入力依存の選択的状態空間層とGPU向け融合走査を統合し、注意機構なしでTransformer級品質と4〜5倍の生成スループットを両立する。

- **2023-12 · [Gated Linear Attention Transformers with Hardware-Efficient Training](2024-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md)**  
  実装：[✓](https://github.com/sustcsonglin/flash-linear-attention) ・ リポジトリ内被引用：95  
  また再帰式を素朴にGPUへ実装すると、逐次依存や高帯域メモリへの状態書き込みが律速となる。著者らは二つの仕組みを提案する。

- **2024-02 · [Simple linear attention language models balance the recall-throughput tradeoff](2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tr.md)**  
  実装：[✓](https://github.com/HazyResearch/based) ・ リポジトリ内被引用：50  
  通常のソフトマックス注意（softmax 注意機構）は、入力文脈に含まれる特定の情報を後から正確に参照する再取得（recall）に強い。モデル規模360M～1.3B、最大50Bトークンの学習、単一NVIDIA H100での実行測定を行い、1.3B・バッチ128・1024トークン生成でFlashAttention-2比最大24倍の処理量を報告する。

- **2024-02 · [Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models](2024-2402.19427-griffin-mixing-gated-linear-recurrences-with-local-attention-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：48  
  Griffinは、自己回帰言語モデルの推論において、文脈が伸びるたびに増える鍵・値キャッシュ（KVキャッシュ）の読み出し費用を抑えるため、固定長の再帰状態と有限窓の注意機構を組み合わせたモデル構造である。

- **2024-04 · [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](2024-2404.07143-leave-no-context-behind-efficient-infinite-context-transformers-with-infini-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：47  
  Infini-注意機構は、入力文脈が数十万から100万トークンに達しても、過去の全トークンに対応する鍵・値（KV）を保存し続けずに情報を参照するための注意機構である。

- **2024-06 · [Samba: Simple Hybrid State Space Models for Efficient Unlimited Context Language Modeling](2024-2406.07522-samba-simple-hybrid-state-space-models-for-efficient-unlimited-context-language-modeling.md)**  
  実装：[✓](https://github.com/microsoft/Samba) ・ リポジトリ内被引用：41  
  Sambaは、選択的状態空間モデル（Selective State Space モデル; SSM）で遠い過去を固定サイズ状態へ畳み込み、スライディング窓注意（Sliding Window 注意機構; SWA）で直近トークンを正確に参照する。

- **2024-04 · [Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence](2024-2404.05892-eagle-and-finch-rwkv-with-matrix-valued-states-and-dynamic-recurrence.md)**  
  実装：[✓](https://github.com/RWKV/RWKV-LM) ・ リポジトリ内被引用：35  
  過去の鍵・値をトークン単位で保持する代わりに、複数ヘッドの固定サイズ行列状態を更新する。Eagleは行列状態とゲートを、Finchは内容依存の補間・時間減衰を導入し、長文脈での情報保持を改善する。

- **2024-04 · [HGRN2: Gated Linear RNNs with State Expansion](2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md)**  
  実装：[✓](https://github.com/OpenNLPLab/HGRN2) ・ リポジトリ内被引用：26  
  これに対し、線形再帰モデルは固定サイズの状態へ履歴を圧縮して次のトークンを生成できるため、推論時の状態保存量を系列長に依存させない。

- **2024-01 · [Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models](2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengt.md)**  
  実装：[✓](https://github.com/OpenNLPLab/lightning-attention) ・ リポジトリ内被引用：16  
  一覧用要約：Lightning 注意機構-2は因果線形注意を現在のタイル内と過去タイルからの寄与に分解し、タイル内を因果マスク付き通常行列積、タイル間を固定サイズの累積KV状態による右積で計算する。前向き・逆向きの両方をTritonで入出力認識型に実装し、長系列でも学習速度と作業メモリを安定させる。

- **2023-11 · [GateLoop: Fully Data-Controlled Linear Recurrence for Sequence Modeling](2023-2311.01927-gateloop-fully-data-controlled-linear-recurrence-for-sequence-modeling.md)**  
  実装：[✓](https://github.com/tobiaskatsch/GatedLinearRNN) ・ リポジトリ内被引用：11  
  一方、状態空間モデルや線形再帰モデルは、過去を有限の隠れ状態へ圧縮して逐次更新できるが、保持・忘却の速度を固定の状態遷移係数に依存させる方式では、入力内容に応じて重要な情報だけを残す操作が難しい。

- **2024-02 · [BlackMamba: Mixture of Experts for State-Space Models](2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md)**  
  実装：[✓](https://github.com/Zyphra/BlackMamba) ・ リポジトリ内被引用：5  
  選択的状態空間モデルの固定状態生成と、混合専門家層の疎な全結合計算を一つの言語モデルに組み込み、長系列生成・学習計算量・専門家の割当てを同時に評価した。

- **2024-03 · [Cobra: Extending Mamba to Multi-Modal Large Language Model for Efficient Inference](2024-2403.14520-cobra-extending-mamba-to-multi-modal-large-language-model-for-efficient-.md)**  
  実装：[✓](https://github.com/h-zhao1997/cobra) ・ リポジトリ内被引用：3  
  提案の中心は、既存のMamba言語モデルへ視覚情報を接続する設計と学習方法を評価した点にある。単一のNVIDIA A100 PCIe 80GBで、画像1枚と同じ質問を入力し256トークンを生成する実験では、Cobra-3.5Bが1.54秒・166.47トークン/秒、MobileVLM v2-3Bが5.17秒・49.50トークン/秒である。

- **2023-11 · [Linear Log-Normal Attention with Unbiased Concentration](2023-2311.13541-linear-log-normal-attention-with-unbiased-concentration.md)**  
  実装：[✓](https://github.com/ynahshan/linear-lognormal-attention) ・ リポジトリ内被引用：1  
  本研究が扱う問題は、系列長が伸びると通常の自己注意（self-注意機構）のスコア行列が二次的に増大する一方、その行列を単に線形化した方式では言語理解の精度が落ちやすいことである。系列長4096での学習反復時間は標準方式6.8秒に対しLLN単独3.2秒、メモリは32.1GBに対し7.5GBだった。

### 4年前（2022-11〜2023-10）

- **2023-05 · [RWKV: Reinventing RNNs for the Transformer Era](2023-2305.13048-rwkv-reinventing-rnns-for-the-transformer-era.md)**  
  実装：[✓](https://github.com/BlinkDL/RWKV-LM) ・ リポジトリ内被引用：131  
  RWKVの大きな特徴は、単に注意を近似して軽量化することではなく、同じ重みと演算を訓練時の並列形式と推論時の再帰形式の双方で扱うことである。論文自身も長文脈評価の一部で弱点を示し、指示の順序を変えるだけで下流評価が大きく改善する例を報告している。

- **2023-07 · [Retentive Network: A Successor to Transformer for Large Language Models](2023-2307.08621-retentive-network-a-successor-to-transformer-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：114  
  RetNetは、指数減衰付き保持演算を並列・再帰・チャンク再帰の三形式で同じ重みのまま実行する。6.7Bモデルの8K入力ではTransformerのKVキャッシュ方式に対し復号8.4倍、メモリ約70%削減を報告し、学習の並列性と固定状態復号を両立する。

- **2022-12 · [Hungry Hungry Hippos: Towards Language Modeling with State Space Models](2022-2212.14052-hungry-hungry-hippos-towards-language-modeling-with-state-space-models.md)**  
  実装：[✓](https://github.com/HazyResearch/H3) ・ リポジトリ内被引用：53  
  本論文は、状態空間モデル（state space モデル; SSM）が長系列を効率的に処理できるにもかかわらず、言語モデリングでは注意機構（注意機構）を使う変換器（Transformer）に劣る理由を二つの観点から調べる。

- **2023-03 · [Resurrecting Recurrent Neural Networks for Long Sequences](2023-2303.06349-resurrecting-recurrent-neural-networks-for-long-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  連続時間状態空間モデルの特殊な離散化を出発点とせず、古典的な再帰型ニューラルネットワークを線形化・複素対角化・安定化・正規化することで、長距離依存の精度と並列学習速度を回復できることを、段階的な除去実験で示した研究。論文が測ったのは主として長系列ベンチマークの分類精度と学習速度であり、大規模言語モデルの実運用推論性能ではない。

- **2023-04 · [Scaling Transformer to 1M tokens and beyond with RMT](2023-2304.11062-scaling-transformer-to-1m-tokens-and-beyond-with-rmt.md)**  
  実装：[✓](https://github.com/booydar/t5-experiments/tree/aaai24) ・ リポジトリ内被引用：12  
  再帰メモリトランスフォーマー（Recurrent メモリ Transformer; RMT）は、長い入力を固定長の区間に分け、直前の区間から受け取った少数のメモリトークンを次の区間に引き渡す方式である。自然言語の実験は、主に履歴区間の追加によってパープレキシティ（perplexity、正解系列の予測の難しさを表す指標）が改善するかを測っている。

- **2023-09 · [Transformer-VQ: Linear-Time Transformers via Vector Quantization](2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md)**  
  実装：[✓](https://github.com/transformer-vq/transformer_vq) ・ リポジトリ内被引用：10  
  基本の着想は、過去の鍵ベクトルを学習可能なコードブックの少数の代表ベクトルへ量子化すると、異なるトークン位置でも同じコードを持つ鍵は同じ注意得点になる、という性質にある。TPU v3での訓練処理率は同規模の二次注意モデルと比べ、系列長8192で3倍超、32768で12倍超となり、131072トークンまで大きな処理率低下なく動作した。

- **2023-06 · [Block-State Transformers](2023-2306.09539-block-state-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUで測った層単体の順方向計算は、ブロック再帰方式に対して単一頭BSTが6〜11倍速い。

- **2023-02 · [SpikeGPT: Generative Pre-trained Language Model with Spiking Neural Networks](2023-2302.13939-spikegpt-generative-pre-trained-language-model-with-spiking-neural-netwo.md)**  
  実装：[✓](https://github.com/ridgerchu/SpikeGPT) ・ リポジトリ内被引用：1  
  従来のスパイク型ネットワークは画像分類などでは有効だったが、語彙数が大きく長距離依存を必要とする言語生成では、二値活性による情報の欠落と訓練の不安定性が課題だった。SpikeGPTは再帰的な言語モデルRWKVのトークン混合をスパイク型ニューロンと組み合わせ、時系列の情報を内部状態へ蓄積することで、二値発火を用いながら自己回帰的な文章生成を行う。

### 5年前（2021-11〜2022-10）

- **2022-02 · [Transformer Quality in Linear Time](2022-2202.10447-transformer-quality-in-linear-time.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  FLASHは、注意計算を系列長に対して線形に近づける方式が、理論計算量を減らしても実機で速くならず、強いTransformerを比較対象にすると品質が落ちるという問題に取り組む。

- **2022-02 · [cosFormer: Rethinking Softmax in Attention](2022-2202.08791-cosformer-rethinking-softmax-in-attention.md)**  
  実装：[✓](https://github.com/OpenNLPLab/cosFormer) ・ リポジトリ内被引用：33  
  cosFormerはソフトマックスの関数形をそのまま近似するのでなく、注意係数が非負であることと、関連性の高い位置へ重みを集中させることを抽出して設計する。

- **2022-06 · [Long Range Language Modeling via Gated State Spaces](2022-2206.13947-long-range-language-modeling-via-gated-state-spaces.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  対象：自己回帰言語モデルの状態空間層をTPUで効率よく学習し、学習系列長を超える長距離依存を扱う研究。学習速度と推論速度の主張を分けて読む。一次論文は2022年7月2日改訂の第3版。

- **2022-02 · [Flowformer: Linearizing Transformers with Conservation Flows](2022-2202.06258-flowformer-linearizing-transformers-with-conservation-flows.md)**  
  実装：[✓](https://github.com/thuml/Flowformer) ・ リポジトリ内被引用：2  
  Flowformerは、自己注意（Self-注意機構）の計算量を系列長に対して線形に抑えつつ、通常のsoftmax注意が持つ「重要な位置を選んで重みを集中させる」性質を残そうとする研究である。

### 7年前（2019-11〜2020-10）

- **2020-09 · [Rethinking Attention with Performers](2020-2009.14794-rethinking-attention-with-performers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/performer) ・ リポジトリ内被引用：171  
  Performerは、通常の全ランクのソフトマックス注意を正の直交ランダム特徴で近似するFAVOR+を提案し、注意行列を明示的に保持しない線形時間・線形空間の実行を可能にする。
<!-- survey:auto:end -->
