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
  大規模言語モデルの逐次生成では、要求ごとの同時処理数が小さいと、フィードフォワード網の大きな重み行列をGPUメモリから読み出す費用が律速になる。入力によってゼロになる中間活性を事前に予測できれば、その活性に対応する行の重み読込みと行列ベクトル積を省略できる。しかし、一般的なLLaMAの滑らかな活性化関数であるSiLUでは、負の値も厳密にはゼロになりにくい。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：2  
  FlexiDepthは、すでに学習された大規模言語モデルの重みを変更せず、出力トークンごとに必要な層の計算量を変える手法である。原著のLlama-3-8B-Instruct（32層）では、平均8層を省いても6つの評価課題における平均性能保持率が100.7%となり、固定層省略方式より高い品質を示す。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：2  
  D-LLMは、大規模言語モデルのすべてのトークンに同じ層数の計算を行う必要はないという観点から、各トークン・各Transformer層でその層を実行するか省略するかを学習する動的深度方式である。代表的な設定では、完全な層を実行するLoRA基準の約52～59%の浮動小数点演算量で、多くの課題の品質を維持した。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルは、次の単語を推測するたびに、難しい計算を要する単語にも文脈からほぼ写すだけの単語にも同じ数の変換層を適用する。DiffSkipは、トークンと層の組ごとに、後続のフィードフォワードネットワーク（FFN）を実行するか、軽量な補正器で代替するかを判断する手法である。

- **2025-03 · [Position-Aware Depth Decay Decoding (D³): Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  位置考慮型深さ減衰復号（Position-Aware 深度減衰 デコード; D³）は、大規模言語モデルの自己回帰生成で、出力トークンの位置に応じて実行するTransformer層数を減らす方式である。

### 3年前（2023-11〜2024-10）

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：50  
  LayerSkipは、大規模言語モデルの全ての層を毎トークン実行する代わりに、浅い層から次トークンを予測できるよう学習し、その予測を同じモデルの残りの層で検証する方式である。下書きモデルの生成結果を大きなモデルで一括検証することで生成時間を短縮できるが、二つのモデルの重みや鍵・値キャッシュを管理する必要がある。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  LazyLLMは、長い入力文のすべてのトークンを全変換層で計算する慣行を改め、現在予測しようとしている次のトークンに重要な入力部分だけを深い層へ進める推論時の計算削減法である。

- **2024-06 · [D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models](2024-2406.13035-d2o-dynamic-discriminative-operations-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  全層へ同じKVキャッシュ量を与えず、プリフィル時の注意密度から浅い層へ大きく、深い層へ小さく予算を配る。さらに追い出し候補を永久削除せず、保持トークンとの類似度を再判定して情報を重み付き統合する。学習なしで長文品質を保ちつつ、フルKVキャッシュ比で最大3.04倍のスループットを示す。

- **2024-08 · [Training-Free Activation Sparsity in Large Language Models](2024-2408.14690-training-free-activation-sparsity-in-large-language-models.md)**  
  実装：[✓](https://github.com/FasterDecoding/TEAL) ・ リポジトリ内被引用：12  
  隠れ状態の小振幅成分を層別にゼロ化し、対応重みチャネルを読まない専用カーネルで、追加学習なしに40〜50%のモデル全体活性疎性と最大1.8倍のデコード高速化を実現する。

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
  トークンごとに途中で処理を終了する早期終了（early exit）は計算を減らせるが、従来の方式をそのまま実際の配信へ持ち込むと、二つの問題が生じる。原著は2023年のプレプリントで、OPT-1.3BとOPT-6.7Bを使い、構造化情報からの文章生成、短文要約、ニュース要約で目標2～5倍の高速化設定を比較した。

- **2023-03 · [CoLT5: Faster Long-Range Transformers with Conditional Computation](2023-2303.09752-colt5-faster-long-range-transformers-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  軽量経路を全トークン、高容量の注意・MLPを学習ルータが選ぶ少数トークンだけへ適用し、16k入力でLongT5比35〜75%の学習高速化・50〜100%の推論高速化を示す。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Magic Pyramid: Accelerating Inference with Early Exiting and Token Pruning](2021-2111.00230-magic-pyramid-accelerating-inference-with-early-exiting-and-token-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  文章分類器BERTの推論で、後続層へ運ぶトークン数を減らす枝刈りと、十分に確信できた入力の層処理を途中終了する機構を組み合わせる。入力長により得意条件が異なる二つの削減方法を重ね、五つの分類課題で演算量と精度の交換条件を評価した研究。表に示す4.95倍や8.25倍は浮動小数点演算量から計算した削減倍率であり、GPUの実時間高速化をそのまま意味しない。
<!-- survey:auto:end -->
