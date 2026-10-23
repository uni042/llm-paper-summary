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
## 自動生成の論文一覧（18本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/20-linear-recurrent-language-models/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Kalman Delta Networks: Uncertainty-aware Associative Memory](2026-2609.07816-kalman-delta-networks-associative-memory.md)**  
  実装：[✓](https://github.com/ngocbh/kalman-delta-networks) ・ リポジトリ内被引用：0  
  固定サイズの線形注意メモリに推定不確実性を持たせ、蓄積証拠に応じて上書き強度をカルマン利得から決めることで、長文脈検索と生成精度を改善する。

- **2026-05 · [Interdomain Attention: Beyond Token-Level Key-Value Memory](2026-2605.24330-interdomain-attention-beyond-token-level-key-value-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この方式は必要な過去情報を内容に基づいて選べるが、復号が進むほどKVキャッシュ容量と参照帯域が増える。FineWeb-Eduを用いて125M〜1.3Bパラメータの復号型モデルを学習した結果、同じ再帰状態予算のS4Dだけのモデルより検証パープレキシティが13〜16%低い。

- **2026-05 · [Blurry Window Attention](2026-2606.09862-blurry-window-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Blurry Window 注意機構（BLA）は、長い系列の全トークンに注意を向ける通常の自己注意の代わりに、有限サイズの状態から過去の鍵・値情報を補間して読み出す注意機構である。規則学習課題RegBenchでは、比較した線形注意系の中でBLAとSWAが状態量の増加に応じて精度を改善し、BLAは小さな状態でも優位な条件があった。

- **2026-04 · [FG^2-GDN: Enhancing Long-Context Gated Delta Networks with Doubly Fine-Grained Control](2026-2604.19021-fg-2-gdn-enhancing-long-context-gated-delta-networks-with-doubly-fine-gr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い文脈の自己回帰推論では、通常のソフトマックス注意（softmax 注意機構）が鍵・値キャッシュ（Key-Value Cache、KV Cache）を系列長に応じて保持し、入力一括処理の計算も系列長の二乗で増える。

### 2年前（2024-11〜2025-10）

- **2024-12 · [Gated Delta Networks: Improving Mamba2 with Delta Rule](2024-2412.06464-gated-delta-networks-improving-mamba2-with-delta-rule.md)**  
  実装：[✓](https://github.com/NVlabs/GatedDeltaNet) ・ リポジトリ内被引用：79  
  本論文は、長文脈を固定容量の状態へ圧縮する線形再帰言語モデルが、記憶の保持と更新を両立しにくい問題を扱う。

### 3年前（2023-11〜2024-10）

- **2023-12 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](2023-2312.00752-mamba-selective-state-space-linear-time-inference.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：181  
  入力依存の選択的状態空間層とGPU向け融合走査を統合し、注意機構なしでTransformer級品質と4〜5倍の生成スループットを両立する。

- **2023-12 · [Gated Linear Attention Transformers with Hardware-Efficient Training](2024-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md)**  
  実装：[✓](https://github.com/sustcsonglin/flash-linear-attention) ・ リポジトリ内被引用：63  
  また再帰式を素朴にGPUへ実装すると、逐次依存や高帯域メモリへの状態書き込みが律速となる。著者らは二つの仕組みを提案する。

- **2024-02 · [Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models](2024-2402.19427-griffin-mixing-gated-linear-recurrences-with-local-attention-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  Griffinは、自己回帰言語モデルの推論において、文脈が伸びるたびに増える鍵・値キャッシュ（KVキャッシュ）の読み出し費用を抑えるため、固定長の再帰状態と有限窓の注意機構を組み合わせたモデル構造である。

- **2024-02 · [Simple linear attention language models balance the recall-throughput tradeoff](2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tr.md)**  
  実装：[✓](https://github.com/HazyResearch/based) ・ リポジトリ内被引用：29  
  通常のソフトマックス注意（softmax 注意機構）は、入力文脈に含まれる特定の情報を後から正確に参照する再取得（recall）に強い。モデル規模360M～1.3B、最大50Bトークンの学習、単一NVIDIA H100での実行測定を行い、1.3B・バッチ128・1024トークン生成でFlashAttention-2比最大24倍の処理量を報告する。

- **2024-06 · [Samba: Simple Hybrid State Space Models for Efficient Unlimited Context Language Modeling](2024-2406.07522-samba-simple-hybrid-state-space-models-for-efficient-unlimited-context-language-modeling.md)**  
  実装：[✓](https://github.com/microsoft/Samba) ・ リポジトリ内被引用：25  
  Sambaは、選択的状態空間モデル（Selective State Space モデル; SSM）で遠い過去を固定サイズ状態へ畳み込み、スライディング窓注意（Sliding Window 注意機構; SWA）で直近トークンを正確に参照する。

- **2024-04 · [Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence](2024-2404.05892-eagle-and-finch-rwkv-with-matrix-valued-states-and-dynamic-recurrence.md)**  
  実装：[✓](https://github.com/RWKV/RWKV-LM) ・ リポジトリ内被引用：22  
  過去の鍵・値をトークン単位で保持する代わりに、複数ヘッドの固定サイズ行列状態を更新する。Eagleは行列状態とゲートを、Finchは内容依存の補間・時間減衰を導入し、長文脈での情報保持を改善する。

- **2024-04 · [HGRN2: Gated Linear RNNs with State Expansion](2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md)**  
  実装：[✓](https://github.com/OpenNLPLab/HGRN2) ・ リポジトリ内被引用：17  
  これに対し、線形再帰モデルは固定サイズの状態へ履歴を圧縮して次のトークンを生成できるため、推論時の状態保存量を系列長に依存させない。

- **2023-11 · [GateLoop: Fully Data-Controlled Linear Recurrence for Sequence Modeling](2023-2311.01927-gateloop-fully-data-controlled-linear-recurrence-for-sequence-modeling.md)**  
  実装：[✓](https://github.com/tobiaskatsch/GatedLinearRNN) ・ リポジトリ内被引用：7  
  一方、状態空間モデルや線形再帰モデルは、過去を有限の隠れ状態へ圧縮して逐次更新できるが、保持・忘却の速度を固定の状態遷移係数に依存させる方式では、入力内容に応じて重要な情報だけを残す操作が難しい。

- **2024-02 · [BlackMamba: Mixture of Experts for State-Space Models](2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md)**  
  実装：[✓](https://github.com/Zyphra/BlackMamba) ・ リポジトリ内被引用：4  
  選択的状態空間モデルの固定状態生成と、混合専門家層の疎な全結合計算を一つの言語モデルに組み込み、長系列生成・学習計算量・専門家の割当てを同時に評価した。

### 4年前（2022-11〜2023-10）

- **2023-05 · [RWKV: Reinventing RNNs for the Transformer Era](2023-2305.13048-rwkv-reinventing-rnns-for-the-transformer-era.md)**  
  実装：[✓](https://github.com/BlinkDL/RWKV-LM) ・ リポジトリ内被引用：91  
  RWKVの大きな特徴は、単に注意を近似して軽量化することではなく、同じ重みと演算を訓練時の並列形式と推論時の再帰形式の双方で扱うことである。論文自身も長文脈評価の一部で弱点を示し、指示の順序を変えるだけで下流評価が大きく改善する例を報告している。

- **2023-07 · [Retentive Network: A Successor to Transformer for Large Language Models](2023-2307.08621-retentive-network-a-successor-to-transformer-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：81  
  RetNetは、指数減衰付き保持演算を並列・再帰・チャンク再帰の三形式で同じ重みのまま実行する。6.7Bモデルの8K入力ではTransformerのKVキャッシュ方式に対し復号8.4倍、メモリ約70%削減を報告し、学習の並列性と固定状態復号を両立する。

- **2022-12 · [Hungry Hungry Hippos: Towards Language Modeling with State Space Models](2022-2212.14052-hungry-hungry-hippos-towards-language-modeling-with-state-space-models.md)**  
  実装：[✓](https://github.com/HazyResearch/H3) ・ リポジトリ内被引用：40  
  本論文は、状態空間モデル（state space モデル; SSM）が長系列を効率的に処理できるにもかかわらず、言語モデリングでは注意機構（注意機構）を使う変換器（Transformer）に劣る理由を二つの観点から調べる。

### 5年前（2021-11〜2022-10）

- **2022-06 · [Long Range Language Modeling via Gated State Spaces](2022-2206.13947-long-range-language-modeling-via-gated-state-spaces.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  対象：自己回帰言語モデルの状態空間層をTPUで効率よく学習し、学習系列長を超える長距離依存を扱う研究。学習速度と推論速度の主張を分けて読む。一次論文は2022年7月2日改訂の第3版。
<!-- survey:auto:end -->
