# Static Structured Model Pruning

事前学習済みdense Transformerから入力に依存しない固定のchannel/neuron、attention head、layerなどの構造単位を削除し、推論時のparameter・演算量を小さくする研究をまとめる。importance推定、mask学習、calibration、LoRA/fine-tuning/continued-pretraining/distillationによる削除後の回復工程を許容する。

## 分類境界

推論時の主要ボトルネック削減を目的に、事前学習済みdense Transformerから固定のchannel/neuron、attention head、layerなどを物理削除し、requestごとに変わらない小型dense architectureを作る研究を含める。入力token依存のpruning/skip/early exit、unstructured/N:M/block weight sparsity、quantization/encodingだけ、MoE expertだけのpruning、model topologyを変えないkernel/compiler最適化は除く。

### 含める研究

- 固定channel/neuron/hidden-dimension pruning
- 固定attention-head pruning
- 固定layer/depth pruning
- 削除後modelを作るためのcalibration、mask learning、軽量な回復学習

### 含めない研究

- input/token依存のtoken pruning、layer skipping、early exit（04）
- unstructured/N:M/block weight sparsity、weight quantization、encoding（16または別該当family）
- MoE expert固有のpruning（02/06）
- parameter topologyを変えないkernel/compiler最適化

## 近傍系統

- [04-conditional-computation](../04-conditional-computation/)
- [16-weight-quantization-compression](../16-weight-quantization-compression/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（25本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/21-static-structured-pruning/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-08 · [SlimVLM: Sensitivity-aware Dynamic Structured Pruning with Adaptive Visual Token Selection for Efficient Vision-Language Models](2026-2608.03580-slimvlm-sensitivity-aware-dynamic-structured-pruning-with-adaptive-visua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚言語モデル（Vision-Language モデル; VLM）を小型化するとき、単に言語モデル向けの重み枝刈りを適用しても、画像由来の多数の視覚トークンがモジュールの重要度推定を歪める。一次論文のLLaVA-1.5-7Bの20%枝刈りでは、8種類の評価群における元モデルに対する平均相対性能93.80%を維持した。

- **2026-05 · [Relative Kinetic Utility: Calibrating Cross-Layer Credit for Global Structured LLM Pruning](2026-2605.09008-relative-kinetic-utility-calibrating-cross-layer-credit-for-global-struc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Global RKU（Global Relative Kinetic Utility）は、大規模言語モデル（LLM）のフィードフォワード層（Feed-順伝播 Network; FFN）からチャネルを削る構造化枝刈りにおいて、同じ層内で重要なチャネルを選ぶ問題と、異なる層のチャネルを共通予算で比較する問題を分離する方式である。

- **2026-04 · [GRASPrune: Global Gating for Budgeted Structured Pruning of Large Language Models](2026-2604.19398-grasprune-global-gating-for-budgeted-structured-pruning-of-large-languag.md)**  
  実装：[✓](https://github.com/ZiY-Wang/GRASPrune) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）の推論時に重みメモリと鍵・値キャッシュ（KV キャッシュ）がともに大きな資源を消費する点を背景に、フィードフォワードネットワーク（Feed-順伝播 Network; FFN）の中間チャネルと、注意機構のKVヘッド群を一つの予算で選ぶ構造化枝刈り（structured 枝刈り）を提案する。

- **2026-02 · [FlattenGPT: Depth Compression for Transformer with Layer Flattening](2026-2602.08858-flattengpt-depth-compression-for-transformer-with-layer-flattening.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlattenGPTは、変換器（Transformer）の隣接層が似た隠れ状態を受け取ることに着目し、層全体を削除するのではなく、隣接2層を幅の広い1層へ平坦化し、その内部の冗長な注意頭と多層パーセプトロン（MLP）チャネルを削る方式である。

- **2026-01 · [Iterative Structured Pruning for Large Language Models with Multi-Domain Calibration](2026-2601.02674-iterative-structured-pruning-for-large-language-models-with-multi-domain.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は大規模言語モデル（LLM）の構造化枝刈り（structured 枝刈り）で、削除すべきチャネルの選択をより正確にするため、多領域の較正データと反復的な重要度の再計算を組み合わせる。Qwen2.5-32Bを50%構造化枝刈りした6課題ゼロショット評価では、FLAPの平均36.59点に対して提案法は46.65点となる。

- **2025-12 · [SAP: Syntactic Attention Pruning for Transformer-based Language Models](2025-2512.19125-sap-syntactic-attention-pruning-for-transformer-based-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAP（Syntactic 注意機構 枝刈り）は、Transformerの複数頭注意（multi-head 注意機構）に含まれる各注意頭（注意機構 head）が、文の構文依存関係をどの程度捉えているかを調べ、言語理解にとって重要でないと判定した頭を再学習なしで削除する構造的枝刈り（structured 枝刈り）手法である。

- **2025-11 · [INTERLACE: Interleaved Layer Pruning and Efficient Adaptation in Large Vision-Language Models](2025-2511.19676-interlace-interleaved-layer-pruning-and-efficient-adaptation-in-large-vi.md)**  
  実装：[✓](https://github.com/pmadinei/Interlace) ・ リポジトリ内被引用：0  
  3層組は重複しないよう選択し、同じ層が複数の役割を持たないようにする。原著の表1では、Qwen3-VL-8Bの言語デコーダ層を25%削除し、FineVisionの1%を1エポック微調整すると、12課題平均の元モデルに対する性能保持率は86.1%だった。

### 2年前（2024-11〜2025-10）

- **2025-06 · [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](2025-2506.01844-smolvla-a-vision-language-action-model-for-affordable-and-efficient-robo.md)**  
  実装：[✓](https://github.com/huggingface/lerobot) ・ リポジトリ内被引用：6  
  中核は、SmolVLM-2を使う視覚言語部の上位層を省略し、1画像の視覚トークンを64個に抑え、行動専門家（action 専門家）に交差注意と自己注意を交互に配置する設計である。実機のPick-Placeでは同期推論の平均完了時間13.75秒に対し、非同期推論は9.70秒、固定時間内の成功した物体移動数は9個から19個へ増えた。

- **2025-05 · [One-for-All Pruning: A Universal Model for Customized Compression of Large Language Models](2025-2505.12216-one-for-all-pruning-a-universal-model-for-customized-compression-of-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この論文の主眼は、枝刈り済み大規模言語モデルを一つだけ作ることではなく、利用者ごとに異なる圧縮率・品質の希望を受け、適切な枝刈り構成を何度も短時間で作ることである。UniCuCoは多数の要求から一度学習した写像を再利用し、要求に応じた層別の枝刈り率を1秒未満で出力する。

- **2025-10 · [TELL-TALE: Task Efficient LLMs with Task Aware Layer Elimination](2025-2510.22767-tell-tale-task-efficient-llms-with-task-aware-layer-elimination.md)**  
  実装：[✓](https://github.com/omyokun/tale) ・ リポジトリ内被引用：0  
  本研究は、ある層を除去するとモデルが小さくなるだけでなく、対象タスクの正答率がむしろ上がる場合があることに着目し、タスク認識型層除去（Task-Aware 層 Elimination、TALE）を提案する。著者はゼロショット（zero-shot）と少数例提示（少数例）、通常の選択肢評価と生成文を読む評価を使い分け、削減層の選択がタスクに依存することを示す。

### 3年前（2023-11〜2024-10）

- **2024-03 · [ShortGPT: Layers in Large Language Models are More Redundant Than You Expect](2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-exp.md)**  
  実装：[✓](https://github.com/icip-cas/ShortGPT) ・ リポジトリ内被引用：85  
  本論文は、大規模言語モデルの全ての変換層が同程度に必要とは限らないという観察から、計算の一部を省略する二種類の方式を提案する。ACL 2025掲載版の代表例では、Llama2-13Bの40層から10層を対象とする条件で、多肢選択指標の平均値は58.49から53.57となり、元の約91.59%を維持した。

- **2023-12 · [Fluctuation-based Adaptive Structured Pruning for Large Language Models](2023-2312.11983-fluctuation-based-adaptive-structured-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/CASIA-IVA-Lab/FLAP) ・ リポジトリ内被引用：31  
  FLAP（FLuctuation-based 適応的 Structured Pruning）は、大規模言語モデル（LLM）の重みを再学習せずに構造化枝刈りする手法である。

- **2024-09 · [CFSP: An Efficient Structured Pruning Framework for LLMs with Coarse-to-Fine Activation Information](2024-2409.13199-cfsp-an-efficient-structured-pruning-framework-for-llms-with-coarse-to-f.md)**  
  実装：[✓](https://github.com/wyxscir/CFSP) ・ リポジトリ内被引用：2  
  CFSPは、大規模言語モデル（LLM）から推論に不要な重み構造を除去する構造化枝刈り（structured 枝刈り）の手法である。50%という論文上の枝刈り設定では、LLaMA3-8Bのパラメータ数が8.03Bから5.21B、表記メモリ量が16.06GBから10.42GB、積和演算量（MAC）が3.64Tから2.19Tに減少した。

- **2024-08 · [Pruning Large Language Models to Intra-module Low-rank Architecture with Transitional Activations](2024-2407.05690-pruning-large-language-models-to-intra-module-low-rank-architecture-with.md)**  
  実装：[✓](https://github.com/sbwww/TransAct-pruning) ・ リポジトリ内被引用：2  
  本論文の対象は、大規模言語モデル（LLM）を端末に配置する際に必要となる重みの格納容量、推論中の計算量、そして鍵・値キャッシュ（KV キャッシュ）のメモリ使用量である。重みだけを低ビット化しても、注意機構の過去トークンの鍵・値を保持する領域は高精度のまま残る。

### 4年前（2022-11〜2023-10）

- **2023-05 · [LLM-Pruner: On the Structural Pruning of Large Language Models](2023-2305.11627-llm-pruner-on-the-structural-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/horseee/LLM-Pruner) ・ リポジトリ内被引用：209  
  LLM-Prunerは、大規模言語モデルのパラメータを実際に削除して小さい密行列モデルへ変換する構造枝刈り手法である。LLaMA-7B、Vicuna-7B、ChatGLM-6Bを評価し、LLaMA-7Bでは20%の構造削減でゼロショット七課題平均が63.25から56.82へ下がり、低ランク適応後60.07まで回復した。

- **2023-10 · [Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning](2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pr.md)**  
  実装：[✓](https://github.com/princeton-nlp/LLM-Shearing) ・ リポジトリ内被引用：84  
  枝刈り直後に失われた能力は継続事前学習で回復するが、その際にも学習データを元の比率で使い続けず、領域別の損失回復状況に応じて再配分する。A100 80GB上の単一生成で、13億パラメータの均一形状は毎秒58トークン、非均一形状は51トークン、27億では43対37トークンであった。

- **2023-05 · [LoRAPrune: Structured Pruning Meets Low-Rank Parameter-Efficient Fine-Tuning](2023-2305.18403-loraprune-structured-pruning-meets-low-rank-parameter-efficient-fine-tun.md)**  
  実装：[✓](https://github.com/aim-uofa/LoRAPrune) ・ リポジトリ内被引用：19  
  LoRAPruneは、事前学習済み大規模言語モデルを配備しやすい小型の密モデルへ変えるために、低ランク適応（Low-Rank Adaptation、LoRA）と構造化枝刈り（structured 枝刈り）を一体化する方式である。

- **2023-10 · [Compresso: Structured Pruning with Collaborative Prompting Learns Compact Large Language Models](2023-2310.05015-compresso-structured-pruning-with-collaborative-prompting-learns-compact.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  Compressoは、大規模言語モデルの注意ヘッド、中間層のチャネル、隠れ次元をまとめて削除する構造化枝刈りの手法である。評価の中心はモデル規模と正答率であり、実機のトークン毎秒や消費電力の改善倍率は示されていない。

- **2023-09 · [Pruning Large Language Models via Accuracy Predictor](2023-2309.09507-pruning-large-language-models-via-accuracy-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデルの枝刈りを「どの重みを削るか」だけでなく「どの層を何割削るか」という探索問題として扱い、少数の実測品質から決定木型予測器を学習する。推論速度の測定ではなく、圧縮率とタスク品質の交換条件を改善する研究である。

### 5年前（2021-11〜2022-10）

- **2022-04 · [Structured Pruning Learns Compact and Accurate Models](2022-2204.00408-structured-pruning-learns-compact-and-accurate-models.md)**  
  実装：[✓](https://github.com/princeton-nlp/CoFiPruning) ・ リポジトリ内被引用：33  
  一方、あらかじめ小型の学生モデルを定めて知識蒸留する方式は、推論しやすい構造を得られるが、大量の未ラベル文章で一般蒸留を行う費用が大きい。MNLIの約95%剪定条件ではBERT-base比12.1倍の推論高速化と精度80.6を報告し、QNLIでも12.1倍・86.1を報告する。

- **2022-04 · [A Fast Post-Training Pruning Framework for Transformers](2022-2204.09656-a-fast-post-training-pruning-framework-for-transformers.md)**  
  実装：[✓](https://github.com/WoosukKwon/retraining-free-pruning) ・ リポジトリ内被引用：29  
  Transformerの計算量と推論遅延を減らすために、不要な注意頭や順伝播層のフィルタを削る構造化枝刈りが使われる。品質低下を1%以内に抑えながら、BERT Baseでは元の演算量の60〜70%程度まで、DistilBERTでは条件により50%まで減らした。

### 7年前（2019-11〜2020-10）

- **2020-04 · [On the Effect of Dropping Layers of Pre-trained Transformer Models](2020-2004.03844-on-the-effect-of-dropping-layers-of-pre-trained-transformer-models.md)**  
  実装：[✓](https://github.com/hsajjad/transformers/) ・ リポジトリ内被引用：22  
  事前学習済みBERT系モデルの上位層を削除して推論時間を約半減し、モデル・タスクごとの精度低下と下位層の重要性を比較した構造的圧縮研究。

### 8年前（2018-11〜2019-10）

- **2019-05 · [Are Sixteen Heads Really Better than One?](2019-1905.10650-are-sixteen-heads-really-better-than-one.md)**  
  実装：[✓](https://github.com/pmichel31415/are-16-heads-really-better-than-1) ・ リポジトリ内被引用：86  
  Michelらは、学習済みの翻訳用TransformerとBERTの各注意ヘッドを無効化して、品質の変化、ヘッド重要度の推定、構造的な枝刈り後の推論速度を実験した。WMT14英仏翻訳のTransformerでは全ヘッドの約20%、MultiNLIに微調整したBERTでは約40%を重要度順に削っても顕著な品質低下が生じなかった。

- **2019-05 · [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](2019-1905.09418-analyzing-multi-head-self-attention-specialized-heads-do-the-heavy-lifti.md)**  
  実装：[✓](https://github.com/lena-voita/the-story-of-heads) ・ リポジトリ内被引用：75  
  本論文は、翻訳用Transformerの多頭注意機構において、各ヘッドの計算が同じだけ必要なのかを、予測への寄与と実際の削除耐性の両側面から調べた研究である。一方、これは2019年の機械翻訳Transformerにおける品質評価であり、現代の生成専用LLMで実際に同じ割合の実行時間や鍵・値キャッシュ容量を削減できると証明した結果ではない。

- **2019-09 · [Reducing Transformer Depth on Demand with Structured Dropout](2019-1909.11556-reducing-transformer-depth-on-demand-with-structured-dropout.md)**  
  実装：✓ ・ リポジトリ内被引用：74  
  深いTransformerは学習時に層をすべて使用する前提で最適化されるため、学習後に連続した層を削ると、残った層が想定しない中間表現を受け取り品質が悪化する。深度ごとに新しいモデルを一から学習したり知識蒸留を繰り返したりする方法では、必要な配備構成が増えるほど学習費用が増える。深度削減は品質低下を完全に取り除くわけではない。
<!-- survey:auto:end -->
