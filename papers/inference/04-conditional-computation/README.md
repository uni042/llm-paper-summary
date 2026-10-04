# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference](2026-2609.08189-hero-history-aware-routing-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の局所状態だけでなく過去のゲート選択と残差変化を線形注意メモリへ蓄積し、Llama 3.1-8Bで26.87%のパラメータ計算を回避しつつ密モデル比100.24%の性能を保つ動的FFNルーティング。

### 2年前（2024-11〜2025-10）

- **2025-04 · [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)**  
  実装：[✓](https://github.com/iie-ycx/DEER) ・ リポジトリ内被引用：5  
  DEERは推論途中で最終回答を試し、自己評価の確信度が高ければ思考連鎖を終了し、低ければ元地点から続行する。追加学習なしで過剰な再検討を減らす。

- **2024-11 · [SparseInfer: Training-free Prediction of Activation Sparsity for Fast LLM Inference](2024-2411.12692-sparseinfer-training-free-prediction-of-activation-sparsity-for-fast-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ReLU化FFNのzero行を入力・重みの符号bit XORだけで学習なし予測し、行単位GEMV スキップへつなぐSparseInfer。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：2  
  FlexiDepthはトークン・層ごとに通常の注意機構とFFNか小型adapterかを選び、skipしたトークンのKVは残す。簡単な入力の計算を減らしつつ後続文脈を保つ。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：2  
  D-LLMは各トークン・各層に小型判断器を置き、実行かskipかを学習する。skipしたトークンのKVも後続注意から外し、計算量とKV使用量を同時に減らす。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DiffSkipはFFN前後の状態差が小さいトークン・層だけを小型adapterへ置換し、元FFNを残したまま固定層削除より品質を保って計算量を減らす。

- **2025-03 · [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  D3は生成後半ほど実行する層数を減らし、最初と最後の層を残して中間層だけを段階的にskipする。KVキャッシュを保ちながら、学習なしでデコード計算を減らす。

### 3年前（2023-11〜2024-10）

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：46  
  LayerSkipは同じLLMの前半層を下書き器、後半層を検証器に分け、追加モデルなしで自己投機的デコードを行う。学習で中間層の予測力を高め、検証済み結果だけを採用する。

- **2024-08 · [Training-Free Activation Sparsity in Large Language Models](2024-2408.14690-training-free-activation-sparsity-in-large-language-models.md)**  
  実装：[✓](https://github.com/FasterDecoding/TEAL) ・ リポジトリ内被引用：12  
  隠れ状態の小振幅成分を層別にゼロ化し、対応重みチャネルを読まない専用カーネルで、追加学習なしに40〜50%のモデル全体活性疎性と最大1.8倍のデコード高速化を実現する。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  LazyLLMは長文入力で重要なトークンだけを後続層へ通し、外したトークンの途中層状態を補助キャッシュに保存して、後で必要になれば再活性化する。

- **2024-06 · [D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models](2024-2406.13035-d2o-dynamic-discriminative-operations-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  全層へ同じKVキャッシュ量を与えず、プリフィル時の注意密度から浅い層へ大きく、深い層へ小さく予算を配る。さらに追い出し候補を永久削除せず、保持トークンとの類似度を再判定して情報を重み付き統合する。学習なしで長文品質を保ちつつ、フルKVキャッシュ比で最大3.04倍のスループットを示す。

- **2024-06 · [Turbo Sparse: Achieving LLM SOTA Performance with Minimal Activated Parameters](2024-2406.05955-turbo-sparse-achieving-llm-sota-performance-with-minimal-activated-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  SwiGLUのゲート側だけでなくup射影側にもReLUを掛ける二重ReLU（dReLU）へ置換し、継続事前学習で性能を回復する。Mistral-7BはFFNの約90%、Mixtral-47Bは専門家ルーティング込みで約97%を非活性化し、PowerInfer系の疎実行で2〜5倍のデコード高速化を報告する。

- **2024-10 · [MoH: Multi-Head Attention as Mixture-of-Head Attention](2024-2410.11842-moh-mixture-of-head-attention.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoH) ・ リポジトリ内被引用：4  
  注意ヘッドを共有ヘッドとTop-Kルーティングヘッドに分け、トークンごとに必要なヘッドだけ使うMoH。LLaMA3-8Bで75%利用・14評価平均64.0%を達成。

- **2024-03 · [Not All Layers of LLMs Are Necessary During Inference](2024-2403.02181-not-all-layers-of-llms-are-necessary-during-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  「簡単な入力にも全層を使う」固定深さをやめ、中間層の出力が最終層と一致しそうならそこで止める。平均17.8%の層を省ける一方、壁時計高速化は最大1.30倍であり、層削減率と実時間短縮を分けて読む必要がある。

### 4年前（2022-11〜2023-10）

- **2023-07 · [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  Skipデコードは生成位置が後ろへ進むほど実行するTransformer層数を段階的に減らし、同じ位置ではバッチ全体で同じ深度を使って、バッチ処理とKVキャッシュを保ちながら計算を減らす。

- **2023-03 · [CoLT5: Faster Long-Range Transformers with Conditional Computation](2023-2303.09752-colt5-faster-long-range-transformers-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  軽量経路を全トークン、高容量の注意・MLPを学習ルータが選ぶ少数トークンだけへ適用し、16k入力でLongT5比35〜75%の学習高速化・50〜100%の推論高速化を示す。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Magic Pyramid: Accelerating Inference with Early Exiting and Token Pruning](2021-2111.00230-magic-pyramid-accelerating-inference-with-early-exiting-and-token-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  BERT系推論で「何個のトークンを後段へ残すか」と「何層まで進むか」を同時に削る。トークン枝刈りは長文、早期終了は短く容易な入力で効きやすいという相補性を使い、片方だけの方式より広い入力長で計算量を落とす。
<!-- survey:auto:end -->
