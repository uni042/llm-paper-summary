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
## 自動生成の論文一覧（87本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/21-static-structured-pruning/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-05 · [Locality-Aware Redundancy Pruning for LLM Depth Compression](2026-2605.27786-locality-aware-redundancy-pruning-for-llm-depth-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LoRP（Locality-Aware Redundancy Pruning）は、事前学習済み大規模言語モデルのTransformerブロックを、追加学習なしに削除する深さ枝刈り（depth 枝刈り）方式である。

- **2026-02 · [Pruning as a Cooperative Game: Surrogate-Assisted Layer Contribution Estimation for Large Language Models](2026-2602.07804-pruning-as-a-cooperative-game-surrogate-assisted-layer-contribution-esti.md)**  
  実装：[✓](https://github.com/920927/Pruning_As_A_Cooperative_Game) ・ リポジトリ内被引用：2  
  本論文は、推論時に実行するTransformer層を丸ごと減らす深さ方向の構造化枝刈り（depth-wise structured 枝刈り）を対象とする。

- **2026-04 · [Structural Pruning of Large Vision Language Models: A Comprehensive Study on Pruning Dynamics, Recovery, and Data Efficiency](2026-2604.24380-structural-pruning-of-large-vision-language-models-a-comprehensive-study.md)**  
  実装：[✓](https://github.com/YiranHuangIrene/VLMCompression) ・ リポジトリ内被引用：1  
  本論文は新しい単一の枝刈りアルゴリズムを提案するというより、何を削るか、何を再学習するか、どれだけのデータを使うかの組合せを、異なる視覚言語モデルで統制して比較する研究である。

- **2026-03 · [Task-aware Block Pruning with Output Distribution Signals for Large Language Models](2026-7c4a0355f923-task-aware-block-pruning-with-output-distribution-signals-for-large-lang.md)**  
  実装：[✓](https://github.com/Song-haJo/TaBP) ・ リポジトリ内被引用：1  
  各ブロック前後の出力分布の統計的変化を複数選択式質問応答の較正データで集約して重要度を測るブロック枝刈りTaBPを提案し、LLaMA-3-8Bで25%のブロックを削除しても平均正解率60.93%を保ち、感度分析型の比較対象56.6%前後を上回った。

- **2026-03 · [Deterministic Differentiable Structured Pruning for Large Language Models](2026-2603.08065-deterministic-differentiable-structured-pruning-for-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  重みを凍結してマスクだけを学ぶ構造化枝刈りで、確率的な緩和を決定的なゲートと焼きなましの代理写像へ置き換え、二値化の損失と拡張ラグランジュ法で目標の削減率を正確に満たしながら、従来方式を大きく上回る品質と実測の高速化を得た。

- **2026-01 · [Iterative Structured Pruning for Large Language Models with Multi-Domain Calibration](2026-2601.02674-iterative-structured-pruning-for-large-language-models-with-multi-domain.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は大規模言語モデル（LLM）の構造化枝刈り（structured 枝刈り）で、削除すべきチャネルの選択をより正確にするため、多領域の較正データと反復的な重要度の再計算を組み合わせる。Qwen2.5-32Bを50%構造化枝刈りした6課題ゼロショット評価では、FLAPの平均36.59点に対して提案法は46.65点となる。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-09 · [Output-aware Residual Stream Pruning for Large Language Models](2026-2609.35579-output-aware-residual-stream-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  残差ストリーム枝刈りで残す方向の選び方を、活性値の再構成誤差だけでなく出力KLへの感度で重み付けする基準へ変え、感度重み付き共分散の固有分解で解くことで、SliceGPTより全モデル・全疎性でパープレキシティと下流精度を改善する研究。

- **2026-09 · [LILA: Data-Free Structured Pruning of LLMs via Latent Spectral Geometry](2026-2609.11163-lila-data-free-structured-pruning-of-llms-via-latent-spectral-geometry.md)**  
  実装：[✓](https://anonymous.4open.science/r/LILA-33CB) ・ リポジトリ内被引用：0  
  重みの非負行列因子分解と特異値分布のコルモゴロフ・スミルノフ距離だけで全結合ニューロンの重要度を決めるデータ不要の構造化枝刈りで、キャリブレーション済み手法を上回る精度と最大1.64倍の推論高速化を示す。

- **2026-08 · [Unifying Depth and Width Pruning for LLMs via Binary Knapsack Optimization](2026-2608.12953-unifying-depth-and-width-pruning-for-llms-via-binary-knapsack-optimizati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの構造化枝刈りは、注意ブロック、MLP、層、チャネルなど、行列の形状を維持できるまとまった単位を取り除く。

- **2026-08 · [SlimVLM: Sensitivity-aware Dynamic Structured Pruning with Adaptive Visual Token Selection for Efficient Vision-Language Models](2026-2608.03580-slimvlm-sensitivity-aware-dynamic-structured-pruning-with-adaptive-visua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚言語モデル（Vision-Language モデル; VLM）を小型化するとき、単に言語モデル向けの重み枝刈りを適用しても、画像由来の多数の視覚トークンがモジュールの重要度推定を歪める。一次論文のLLaVA-1.5-7Bの20%枝刈りでは、8種類の評価群における元モデルに対する平均相対性能93.80%を維持した。

- **2026-08 · [SHIFT-LLM: Distribution Shift Correction in Depth-Pruned LLMs](2026-2608.25068-shift-llm-distribution-shift-correction-in-depth-pruned-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  深さ枝刈りで欠けた残差の更新だけを、恒等経路を残した線形補正で閉形式に較正して埋め戻し、微調整なしで枝刈り後の精度低下を大きく回復する方式。

- **2026-08 · [Magnitude Profile Pruning: Calibration-Free Structured Attention Head Removal for Transformer Compression](2026-2609.26177-magnitude-profile-pruning-calibration-free-structured-attention-head-rem.md)**  
  実装：[✓](https://github.com/Kasun-Dewage/Magnitude-Profile-Pruning-2026) ・ リポジトリ内被引用：0  
  重みの行ノルムが統計的な外れ値であるヘッドだけを残し、通常の大きさのヘッドを先に削る較正不要の枝刈り基準を作り、グループ化クエリ注意への配分も加えたことで、大規模デコーダで較正を使う比較対象をパープレキシティで上回った。

- **2026-08 · [COEC: Calibrated Orthogonal-Equivalence Compensation for Structured Pruning of Large Language Models](2026-2608.21142-coec-calibrated-orthogonal-equivalence-compensation-for-structured-pruni.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  列を落とした保持重みへ左右両側の直交回転と特異値ごとの再調整で学習不要の補償を行うCOECを提案し、疎性30パーセントで全モデルの困惑度を既存補償より改善し、利得が疎さとともに大きくなることを示した。

- **2026-07 · [CausalGate: Causal Importance Distillation for Transformer Module Pruning](2026-2607.22720-causalgate-causal-importance-distillation-for-transformer-module-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サブ層をゼロ化する介入で測った因果的重要度を静的ゲートへ蒸留し、実行時オーバーヘッドなしでモジュールを飛ばす枝刈り手法。観測的指標より大きな削除率まで品質を保つ。

- **2026-06 · [TriSP: Tri-Signal Structured Pruning for Large Language Models](2026-2607.22587-trisp-tri-signal-structured-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み・勾配・活性の3信号を幾何平均した重要度でヘッドとニューロンを構造的に落とし、適応配分とLoRA回復を組み合わせた枝刈り手法。全枝刈り率と4モデルで最良のパープレキシティとゼロショット精度を達成する。

- **2026-06 · [From Layers to Submodules: Rethinking Granularity in Replacement-Based LLM Compression](2026-2606.02559-from-layers-to-submodules-rethinking-granularity-in-replacement-based-ll.md)**  
  実装：[✓](https://github.com/eliacunegatti/SubFit) ・ リポジトリ内被引用：0  
  層単位で連続範囲を置換する従来の圧縮を、注意とフィードフォワードのサブモジュール単位で非連続に選び分ける方式へ変え、疎性25パーセントで精度保持84.6パーセントとパープレキシティ悪化2.42倍を両立する置換型圧縮。

- **2026-05 · [Relative Kinetic Utility: Calibrating Cross-Layer Credit for Global Structured LLM Pruning](2026-2605.09008-relative-kinetic-utility-calibrating-cross-layer-credit-for-global-struc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Global RKU（Global Relative Kinetic Utility）は、大規模言語モデル（LLM）のフィードフォワード層（Feed-順伝播 Network; FFN）からチャネルを削る構造化枝刈りにおいて、同じ層内で重要なチャネルを選ぶ問題と、異なる層のチャネルを共通予算で比較する問題を分離する方式である。

- **2026-05 · [Prune, Update and Trim: Robust Structured Pruning for Large Language Models](2026-2605.18331-prune-update-and-trim-robust-structured-pruning-for-large-language-model.md)**  
  実装：[✓](https://github.com/Coello-dev/Putri) ・ リポジトリ内被引用：0  
  残したFFN重みの最小二乗更新、FFNの逐次枝刈り、KVヘッド単位の除去によるGQA対応を組み合わせ、高疎性でも他手法より崩れにくい学習後構造化枝刈りPutriを提案した研究。

- **2026-05 · [Ghosted Layers: Unconstrained Activation Alignment for Recovering Layer-Pruned LLMs](2026-2605.15491-ghosted-layers-unconstrained-activation-alignment-for-recovering-layer-p.md)**  
  実装：[✓](https://github.com/daniel-eai/ghosted_layers_official_repository) ・ リポジトリ内被引用：0  
  大規模言語モデルの深さ方向の構造的枝刈りは、トランスフォーマーの復号層を丸ごと削除し、特殊な疎行列カーネルを必要とせずにモデルの演算と重みを減らせる。LLaMA-3.1-8Bで32層中7層をLLM-Streamlineにより削除した場合、9課題平均正答率は無補正の42.60%から60.01%へ回復する。

- **2026-04 · [SimDiff: Depth Pruning via Similarity and Difference](2026-2604.19520-simdiff-depth-pruning-via-similarity-and-difference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SimDiffは、隣接層の隠れ状態について方向の違いと変化の大きさを別々に計算し、重み付きの重要度へ統合する。一次論文は25%剪定したLLaMA2-7Bで元モデルの10課題平均の91.44%を維持し、LLaMA3.1-8Bで12層を削った場合にA40上の生成スループット1.49倍を報告する。

- **2026-04 · [GRASPrune: Global Gating for Budgeted Structured Pruning of Large Language Models](2026-2604.19398-grasprune-global-gating-for-budgeted-structured-pruning-of-large-languag.md)**  
  実装：[✓](https://github.com/ZiY-Wang/GRASPrune) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）の推論時に重みメモリと鍵・値キャッシュ（KV キャッシュ）がともに大きな資源を消費する点を背景に、フィードフォワードネットワーク（Feed-順伝播 Network; FFN）の中間チャネルと、注意機構のKVヘッド群を一つの予算で選ぶ構造化枝刈り（structured 枝刈り）を提案する。

- **2026-03 · [Understanding Pruning Regimes in Vision-Language Models Through Domain-Aware Layer Selection](2026-2603.20275-understanding-pruning-regimes-in-vision-language-models-through-domain-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の入出力の活性の類似度を数学と非数学の探査で別々に測って冗長な層を順位付けする領域配慮の削除を提案し、削除率が小さい様相では層の選択が最も効くこと、率が上がると方式が収束し、高い率では削除の間隔という構造が支配すること、そして絶対精度の低下自体は一割削除でも大きいことを二モデル・七評価で示した。

- **2026-03 · [Bielik-Minitron-7B: Compressing Large Language Models via Structured Pruning and Knowledge Distillation for the Polish Language](2026-2603.11881-bielik-minitron-7b-compressing-large-language-models-via-structured-prun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重み容量と計算費用を下げる方法には、数値精度を落とす量子化と、モデル構造自体を小さくする枝刈りがある。パラメータ削減率は33.4%である。

- **2026-02 · [TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation](2026-2602.02891-tracenas-zero-shot-llm-pruning-via-gradient-trace-correlation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TraceNASは、事前学習済み大規模言語モデル（Large Language モデル、LLM）から層と内部チャネルを削除する構造的枝刈り（structured 枝刈り）において、候補構造を逐一学習させずに選ぶための探索方式である。

- **2026-02 · [GradMAP: Faster Layer Pruning with Gradient Metric and Projection Compensation](2026-2602.14649-gradmap-faster-layer-pruning-with-gradient-metric-and-projection-compens.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  勾配の大きさで層の重要度を1回の逆伝播で測り、枝刈り後に最もずれた1層だけへ射影補償行列を掛けて回復させることで、枝刈り自体を平均約4倍速くし性能も上回る2段階の層枝刈り。

- **2026-02 · [FlattenGPT: Depth Compression for Transformer with Layer Flattening](2026-2602.08858-flattengpt-depth-compression-for-transformer-with-layer-flattening.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlattenGPTは、変換器（Transformer）の隣接層が似た隠れ状態を受け取ることに着目し、層全体を削除するのではなく、隣接2層を幅の広い1層へ平坦化し、その内部の冗長な注意頭と多層パーセプトロン（MLP）チャネルを削る方式である。

- **2026-02 · [Compressing LLMs with MoP: Mixture of Pruners](2026-2602.06127-compressing-llms-with-mop-mixture-of-pruners.md)**  
  実装：[✓](https://github.com/c2d-usp/Efficient-LLMs-with-MoP) ・ リポジトリ内被引用：0  
  深さ枝刈りと幅枝刈りの候補を毎回同じ圧縮量で競わせ、短い回復微調整後の品質で経路を選ぶ反復により、二つの次元の強みを交互に使う構造化枝刈り。

- **2026-01 · [MI-PRUN: Optimize Large Language Model Pruning via Mutual Information](2026-2601.07212-mi-prun-optimize-large-language-model-pruning-via-mutual-information.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック前後の隠れ状態の相互情報量で冗長な層を見分け、連続ブロック単位の反復入れ替えで削除組合せを大域的に磨く枝刈り方式で、従来法より小さい品質低下で層を削減した。

- **2025-12 · [SAP: Syntactic Attention Pruning for Transformer-based Language Models](2025-2512.19125-sap-syntactic-attention-pruning-for-transformer-based-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAP（Syntactic 注意機構 枝刈り）は、Transformerの複数頭注意（multi-head 注意機構）に含まれる各注意頭（注意機構 head）が、文の構文依存関係をどの程度捉えているかを調べ、言語理解にとって重要でないと判定した頭を再学習なしで削除する構造的枝刈り（structured 枝刈り）手法である。

- **2025-12 · [Data-Free Pruning of Self-Attention Layers in LLMs](2025-2512.20636-data-free-pruning-of-self-attention-layers-in-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  深い注意層が自らの更新を消すという抑制仮説に基づき、クエリとキー重みの結合の強さだけで注意層を順位付けて外す、データ不要で1秒未満に終わる深さ方向の枝刈り。

### 2年前（2024-12〜2025-11）

- **2025-06 · [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](2025-2506.01844-smolvla-a-vision-language-action-model-for-affordable-and-efficient-robo.md)**  
  実装：[✓](https://github.com/huggingface/lerobot) ・ リポジトリ内被引用：10  
  中核は、SmolVLM-2を使う視覚言語部の上位層を省略し、1画像の視覚トークンを64個に抑え、行動専門家（action 専門家）に交差注意と自己注意を交互に配置する設計である。実機のPick-Placeでは同期推論の平均完了時間13.75秒に対し、非同期推論は9.70秒、固定時間内の成功した物体移動数は9個から19個へ増えた。

- **2025-03 · [Týr-the-Pruner: Structural Pruning LLMs via Global Sparsity Distribution Optimization](2025-2503.09657-t-r-the-pruner-structural-pruning-llms-via-global-sparsity-distribution-.md)**  
  実装：[✓](https://github.com/AMD-AGI/Tyr-the-Pruner) ・ リポジトリ内被引用：5  
  各層を複数の疎率で切った複製の束から全体の疎率配分を進化的探索で選ぶ全体枝刈りで、七百億級モデルを半分切っても下流の平均正解率を元の九十七パーセントに保ち、八十億級の三十七・五パーセント枝刈りでは従来の最良手法より困惑度が三・四五低く正解率が十・二六ポイント高かったと報告した。

- **2024-12 · [TrimLLM: Progressive Layer Dropping for Domain-Specific LLMs](2024-2412.11242-trimllm-progressive-layer-dropping-for-domain-specific-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  対象領域に要らない層を微調整の途中で一層ずつ落とす漸進的な深さ削減で、七十億級モデルを半分ほどに圧縮しても医療の正解率を五四・六パーセントから五三・一パーセントに保ち、消費者向け装置で量子化や枝刈りの二・一倍から五・七倍の処理量を得て、併用時は記憶量八分の一で四・五倍になったと報告した。

- **2025-11 · [Towards Efficient VLMs: Information-Theoretic Driven Compression via Adaptive Structural Pruning](2025-2511.19518-towards-efficient-vlms-information-theoretic-driven-compression-via-adap.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚言語モデルの視覚モジュールへ、情報ボトルネック原理に基づくヘッド枝刈り（eRankとKS距離）と、誤差上限からランクを決める訓練なしFFN低ランク圧縮を組み合わせたInfoPruneを提案した研究。

- **2025-11 · [INTERLACE: Interleaved Layer Pruning and Efficient Adaptation in Large Vision-Language Models](2025-2511.19676-interlace-interleaved-layer-pruning-and-efficient-adaptation-in-large-vi.md)**  
  実装：[✓](https://github.com/pmadinei/Interlace) ・ リポジトリ内被引用：1  
  3層組は重複しないよう選択し、同じ層が複数の役割を持たないようにする。原著の表1では、Qwen3-VL-8Bの言語デコーダ層を25%削除し、FineVisionの1%を1エポック微調整すると、12課題平均の元モデルに対する性能保持率は86.1%だった。

- **2025-09 · [COMPACT: Common-token Optimized Model Pruning Across Channels and Tokens](2025-2509.06836-compact-common-token-optimized-model-pruning-across-channels-and-tokens.md)**  
  実装：[✓](https://github.com/ekwek1/COMPACT) ・ リポジトリ内被引用：1  
  COMPACTは、推論用の大規模言語モデルを圧縮するとき、Transformerの層数や隠れ次元を一律に削るのでなく、語彙表に結び付くパラメータとフィードフォワード網（FFN）の中間チャネルを別々に制御する手法である。

- **2025-05 · [One-for-All Pruning: A Universal Model for Customized Compression of Large Language Models](2025-2505.12216-one-for-all-pruning-a-universal-model-for-customized-compression-of-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この論文の主眼は、枝刈り済み大規模言語モデルを一つだけ作ることではなく、利用者ごとに異なる圧縮率・品質の希望を受け、適切な枝刈り構成を何度も短時間で作ることである。UniCuCoは多数の要求から一度学習した写像を再利用し、要求に応じた層別の枝刈り率を1秒未満で出力する。

- **2025-04 · [Entropy-Based Block Pruning for Efficient Large Language Models](2025-2504.03794-entropy-based-block-pruning-for-efficient-large-language-models.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/EntroDrop) ・ リポジトリ内被引用：1  
  Transformerの構造化剪定では、隣接する層や注意機構 blockの入出力のcosine similarityを冗長度の指標として使うことが多い。

- **2025-04 · [Efficient LLMs with AMP: Attention Heads and MLP Pruning](2025-2504.21174-efficient-llms-with-amp-attention-heads-and-mlp-pruning.md)**  
  実装：[✓](https://github.com/c2d-usp/Efficient-LLMs-with-AMP) ・ リポジトリ内被引用：1  
  入力を重みへ射影して測る寄与の大きさで、注意ヘッドとMLPニューロンを同時に削る構造化枝刈り。ノルム基準より精度を保ち、実測の高速化も得る。

- **2025-01 · [DReSS: Data-driven Regularized Structured Streamlining for Large Language Models](2025-2501.17905-dress-data-driven-regularized-structured-streamlining-for-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし従来の「重要度を測ってチャネルを直接削除し、その後に回復微調整する」方式では、削除予定チャネルに残っていた有用な情報まで失われる。

- **2025-10 · [The Structural Scalpel: Automated Contiguous Layer Pruning for Large Language Models](2025-2510.23652-the-structural-scalpel-automated-contiguous-layer-pruning-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連続層区間を微分可能なゲートとKL最小化で自動探索して切り取り、切り口の両端2層だけを微調整して回復する層枝刈り手法。70Bモデルでも枝刈り率30パーセントで性能保持率91パーセント超を維持する。

- **2025-10 · [TELL-TALE: Task Efficient LLMs with Task Aware Layer Elimination](2025-2510.22767-tell-tale-task-efficient-llms-with-task-aware-layer-elimination.md)**  
  実装：[✓](https://github.com/omyokun/tale) ・ リポジトリ内被引用：0  
  本研究は、ある層を除去するとモデルが小さくなるだけでなく、対象タスクの正答率がむしろ上がる場合があることに着目し、タスク認識型層除去（Task-Aware 層 Elimination、TALE）を提案する。著者はゼロショット（zero-shot）と少数例提示（少数例）、通常の選択肢評価と生成文を読む評価を使い分け、削減層の選択がタスクに依存することを示す。

- **2025-10 · [Entropy Meets Importance: A Unified Head Importance-Entropy Score for Stable and Efficient Transformer Pruning](2025-2510.13832-entropy-meets-importance-a-unified-head-importance-entropy-score-for-sta.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭注意の構造化枝刈りでは、学習済みTransformerの注意ヘッドを削除し、演算とKVキャッシュの潜在的な負担を減らす。一次論文の主実験はBERT-baseのGLUEであり、50%枝刈り時の平均品質・安定性の改善を示す。

- **2025-07 · [High-Layer Attention Pruning with Rescaling](2025-2507.01900-high-layer-attention-pruning-with-rescaling.md)**  
  実装：[✓](https://github.com/SongtaoLiu0823/HARP) ・ リポジトリ内被引用：0  
  下位層と上位層で同じ割合の注意を削ると、表現形成の早い段階にある重要なトークン間依存まで失われ、特に生成・推論課題で品質が大幅に悪化する。HARP（High-層 注意機構 枝刈り with Rescaling）は、高い層ほどトークン表現が類似し、注意によるトークンの識別が弱くなるという仮説を設計の出発点にする。

- **2025-06 · [SDMPrune: Self-Distillation MLP Pruning for Efficient Large Language Models](2025-2506.11120-sdmprune-self-distillation-mlp-pruning-for-efficient-large-language-mode.md)**  
  実装：[✓](https://github.com/visresearch/SDMPrune) ・ リポジトリ内被引用：0  
  枝刈りの重要度測定へ自己蒸留損失を組み込み、元のモデルの予測分布を保ちながらMLPの中間ニューロンだけを構造的に刈る手法。ラベルだけの勾配より正確に感度の低いニューロンを選べる。

- **2025-06 · [Pruning General Large Language Models into Customized Expert Models](2025-2506.02561-pruning-general-large-language-models-into-customized-expert-models.md)**  
  実装：[✓](https://github.com/zhaoyiran924/Custom-Prune) ・ リポジトリ内被引用：0  
  言語・分野・タスクの各コーパスで無関係なニューロンを測り、その共通部分だけを後学習なしで除去することで、特定用途に合わせた軽量な専門家モデルを作る枝刈り手法。

- **2025-06 · [Olica: Efficient Structured Pruning of Large Language Models without Retraining](2025-2506.08436-olica-efficient-structured-pruning-of-large-language-models-without-retr.md)**  
  実装：[✓](https://github.com/BetterTMrR/LLM-Olica) ・ リポジトリ内被引用：0  
  注意機構の二つの行列積を一体として主成分分析で圧縮し、フィードフォワードの残差誤差を低ランク線形較正で戻すことで、再学習なしに大規模言語モデルを構造化枝刈りする方式。

- **2025-06 · [Hopscotch: Discovering and Skipping Redundancies in Language Models](2025-2506.03303-hopscotch-discovering-and-skipping-redundancies-in-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Hopscotchは、Transformerの注意ブロックを丸ごと除去しながら、残る層の出力を少数のスカラーで再調整する構造圧縮法である。Llama-3.1-8B-InstructとQwen2.5-7B-Instructで検証し、Llamaでは四つの注意ブロックを削除しても平均性能保持率98.65%、七つ削除した場合も97.08%と報告する。

- **2025-06 · [GPTailor: Large Language Model Pruning Through Layer Cutting and Stitching](2025-2506.20480-gptailor-large-language-model-pruning-through-layer-cutting-and-stitchin.md)**  
  実装：[✓](https://github.com/Guinan-Su/auto-merge-llm) ・ リポジトリ内被引用：0  
  単一モデルではなく同族の微調整モデルの層を除去・選択・統合する切り貼りを零次最適化で探索する枝刈りで、一百三十億級モデルの約二十五パーセント除去時に能力の九十七・三パーセント、七十億級で九十二・二パーセントを後訓練なしで保った。

- **2025-06 · [Accurate Sublayer Pruning for Large Language Models by Exploiting Latency and Tunability Information](2025-2506.03510-accurate-sublayer-pruning-for-large-language-models-by-exploiting-latenc.md)**  
  実装：[✓](https://github.com/snudm-starlab/SPRINT) ・ リポジトリ内被引用：0  
  しかし注意とMLPは遅延への寄与が違い、削除後に残った層を補正することで回復できる誤差も異なる。Llama-2/3系モデルで、同程度の推論高速化を達成する従来方式と比較し、ゼロショット常識推論の正答率を最大23.88パーセントポイント改善したと報告する。

- **2025-05 · [Two-Stage Regularization-Based Structured Pruning for LLMs](2025-2505.18232-two-stage-regularization-based-structured-pruning-for-llms.md)**  
  実装：[✓](https://github.com/fmk345/TRSP) ・ リポジトリ内被引用：0  
  削除前に層重みを貪欲に学習して候補を決め、候補層の入出力差への正則化で知識を残存層へ移してから層を削除する再学習不要の枝刈りで、七十億級モデルの二十五パーセント削除時に困惑度を次点より約二十パーセント下げ平均正解率六十・五七パーセントを保った。

- **2025-05 · [SPAP: Structured Pruning via Alternating Optimization and Penalty Methods](2025-2505.03373-spap-structured-pruning-via-alternating-optimization-and-penalty-methods.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MLPの構造枝刈りを混合整数最適化として定式化し、緩和の最適性を証明したうえでペナルティ法と交互最小化で解く手法。経験的指標に頼らず枝刈り先と重みの回復を決め、疎性30パーセントで約1.29倍の高速化を得た。

- **2025-03 · [Sample-aware Adaptive Structured Pruning for Large Language Models](2025-2503.06184-sample-aware-adaptive-structured-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/JunKong5/AdaPruner) ・ リポジトリ内被引用：0  
  構造化枝刈りの成否を分けるキャリブレーションデータと重要度指標の組み合わせを、ベイズ最適化でサンプルを意識して自動探索するAdaPrunerで、枝刈り率20%で未枝刈りモデルの97%の性能を保つ。

- **2025-02 · [MaskPrune: Mask-based LLM Pruning for Layer-wise Uniform Structures](2025-2502.14008-maskprune-mask-based-llm-pruning-for-layer-wise-uniform-structures.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マスクと層共通の削減数をミニマックス最適化で同時学習し、全層で同じ形を保ったまま構造化枝刈りを行うことで、推論配置しやすい均一な圧縮モデルを得る方式。

- **2025-02 · [Forget the Data and Fine-Tuning! Just Fold the Network to Compress](2025-2502.10216-forget-the-data-and-fine-tuning-just-fold-the-network-to-compress.md)**  
  実装：[✓](https://github.com/nanguoyu/model-folding-universal) ・ リポジトリ内被引用：0  
  同一ネットワーク内の似たニューロンを重みだけのk平均クラスタリングで統合し、統合で潰れる活性値の分散をデータなしの近似補正で直すことで、学習データもファインチューニングもなしにモデルを構造的に圧縮する方式。

- **2024-12 · [Extracting Interpretable Task-Specific Circuits from Large Language Models for Faster Inference](2024-2412.15750-extracting-interpretable-task-specific-circuits-from-large-language-mode.md)**  
  実装：[✓](https://github.com/jgcarrasco/circuit-extraction) ・ リポジトリ内被引用：0  
  注意ヘッドと多層パーセプトロンをKLダイバージェンスの増分で判定して実際に除去し、タスク専用の小さく高速な部分モデルを抽出する枝刈り手法。

- **2024-12 · [Adaptive Pruning for Large Language Models with Structural Importance Awareness](2024-2412.15127-adaptive-pruning-for-large-language-models-with-structural-importance-aw.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重要度の融合指標と揺らぎに基づく構造探索で不安定な結合構造から消し、グループ量子化つき微調整で回復する構造化枝刈り手法。大きな枝刈り率でも比較対象より精度を保つ。

### 3年前（2023-12〜2024-11）

- **2024-03 · [ShortGPT: Layers in Large Language Models are More Redundant Than You Expect](2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-exp.md)**  
  実装：[✓](https://github.com/icip-cas/ShortGPT) ・ リポジトリ内被引用：127  
  本論文は、大規模言語モデルの全ての変換層が同程度に必要とは限らないという観察から、計算の一部を省略する二種類の方式を提案する。ACL 2025掲載版の代表例では、Llama2-13Bの40層から10層を対象とする条件で、多肢選択指標の平均値は58.49から53.57となり、元の約91.59%を維持した。

- **2023-12 · [Fluctuation-based Adaptive Structured Pruning for Large Language Models](2023-2312.11983-fluctuation-based-adaptive-structured-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/CASIA-IVA-Lab/FLAP) ・ リポジトリ内被引用：65  
  FLAP（FLuctuation-based 適応的 Structured Pruning）は、大規模言語モデル（LLM）の重みを再学習せずに構造化枝刈りする手法である。

- **2024-09 · [CFSP: An Efficient Structured Pruning Framework for LLMs with Coarse-to-Fine Activation Information](2024-2409.13199-cfsp-an-efficient-structured-pruning-framework-for-llms-with-coarse-to-f.md)**  
  実装：[✓](https://github.com/wyxscir/CFSP) ・ リポジトリ内被引用：6  
  CFSPは、大規模言語モデル（LLM）から推論に不要な重み構造を除去する構造化枝刈り（structured 枝刈り）の手法である。50%という論文上の枝刈り設定では、LLaMA3-8Bのパラメータ数が8.03Bから5.21B、表記メモリ量が16.06GBから10.42GB、積和演算量（MAC）が3.64Tから2.19Tに減少した。

- **2024-08 · [Pruning Large Language Models to Intra-module Low-rank Architecture with Transitional Activations](2024-2407.05690-pruning-large-language-models-to-intra-module-low-rank-architecture-with.md)**  
  実装：[✓](https://github.com/sbwww/TransAct-pruning) ・ リポジトリ内被引用：3  
  本論文の対象は、大規模言語モデル（LLM）を端末に配置する際に必要となる重みの格納容量、推論中の計算量、そして鍵・値キャッシュ（KV キャッシュ）のメモリ使用量である。重みだけを低ビット化しても、注意機構の過去トークンの鍵・値を保持する領域は高精度のまま残る。

- **2024-06 · [MoreauPruner: Robust Pruning of Large Language Models against Weight Perturbations](2024-2406.07017-moreaupruner-robust-pruning-of-large-language-models-against-weight-pert.md)**  
  実装：[✓](https://github.com/ShiningSord/MoreauPruner) ・ リポジトリ内被引用：3  
  LLaMA-13Bでは回復微調整後の7課題平均が元64.97に対しMoreauPruner-GSで64.94まで近づく。一方、LLaMA3-8Bでは元70.33に対し同方式の20%剪定後が65.37で、性能損失が残る。

- **2024-05 · [STAT: Shrinking Transformers After Training](2024-2406.00061-stat-shrinking-transformers-after-training.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  STATは、学習済みTransformerを再学習せずに小さくするため、フィードフォワードネットワーク（FFN）のニューロンと自己注意ヘッドを構造ごと除去する事後剪定手法である。いずれもA6000 48GBを1枚使った剪定計算が約2時間半で、これはモデル圧縮の処理時間である。

- **2024-02 · [Why Lift so Heavy? Slimming Large Language Models by Cutting Off the Layers](2024-2402.11700-why-lift-so-heavy-slimming-large-language-models-by-cutting-off-the-laye.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデル（LLM）は多数のTransformer層を積み重ねることで表現能力を獲得する。重要な限定条件は、すべて分類タスク向けに再微調整した後の結果である。

- **2023-12 · [Mini-GPTs: Efficient Large Language Models through Contextual Pruning](2023-2312.12682-mini-gpts-efficient-large-language-models-through-contextual-pruning.md)**  
  実装：[✓](https://github.com/tval2/contextual-pruning) ・ リポジトリ内被引用：2  
  Mini-GPTsは、汎用言語モデルが保持する知識や計算経路の全てを個別業務で必要とするわけではないという仮説から、用途に応じて不要なニューロンを取り除く研究である。削除後には分野別データで微調整し、困惑度の回復を試みる。

- **2024-11 · [AmoebaLLM: Constructing Any-Shape Large Language Models for Efficient and Instant Deployment](2024-2411.10606-amoeballm-constructing-any-shape-large-language-models-for-efficient-and.md)**  
  実装：[✓](https://github.com/GATECH-EIC/AmoebaLLM) ・ リポジトリ内被引用：1  
  動的計画法の層選択と形状連動のLoRA混合で、一回の微調整から深さと幅の任意形状のモデルを即時抽出できるようにし、個別圧縮より高い精度を出した枠組み。

- **2024-02 · [NutePrune: Efficient Progressive Pruning with Numerous Teachers for Large Language Models](2024-2402.09773-nuteprune-efficient-progressive-pruning-with-numerous-teachers-for-large.md)**  
  実装：[✓](https://github.com/Lucius-lsr/NutePrune) ・ リポジトリ内被引用：1  
  無傷のモデル1個にマスクとLoRAを取り替えて多数の教師を演じさせることで、メモリ追加なしに漸進的蒸留を構造化プルーニングへ適用したNutePruneの研究。教師と生徒のスパース率の差を一定に保ち、能力差による蒸留の難化を抑える。

- **2024-09 · [PASS: Pruning Attention Heads with Almost-sure Sparsity Targets](2024-1a2ee8dce5b4-pass-pruning-attention-heads-with-almost-sure-sparsity-targets.md)**  
  実装：[✓](https://github.com/DujianDing/PASS) ・ リポジトリ内被引用：0  
  ゲートの閉じ・開き確率を確率1へ二極化させる「ほぼ確実な疎さ」で、閾値調整なしに指定本数どおり注意ヘッドを枝刈りし、残すヘッドを少数層へ集中させて層ごと省略できるようにした枝刈り方式。

- **2024-07 · [Efficient LLM Pruning with Global Token-Dependency Awareness and Hardware-Adapted Inference](2024-614ce03da14c-efficient-llm-pruning-with-global-token-dependency-awareness-and-hardwar.md)**  
  実装：[✓](https://github.com/oshindutta/TVAprune) ・ リポジトリ内被引用：0  
  TVA-Pruneは、大規模言語モデルの注意ヘッド、フィードフォワード層の中間次元、トークン表現の隠れ次元を構造的に削除する圧縮方式である。A100 40GBでLLaMA-2-7Bを枝刈りした条件では、無圧縮のWikiText2困惑度5.11に対し、TVA-Pruneの困惑度は14.15へ悪化するが、推論速度は1.8倍となる。

- **2024-07 · [Attention Is All You Need But You Don't Need All Of It For Inference of Large Language Models](2024-2407.15516-attention-is-all-you-need-but-you-don-t-need-all-of-it-for-inference-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TransformerベースのLLMでは、各層に注意機構サブレイヤとMLPサブレイヤがあり、推論時にもすべての層を通すのが通常である。主要な結果として、Llama2-13Bで後段注意機構の約33%を省くと、OpenLLMのARC、HellaSwag、TruthfulQA、MMLUの平均スコアは58.5から56.8へ低下する。

- **2024-06 · [VTrans: Accelerating Transformer Compression with Variational Information Bottleneck based Pruning](2024-2406.05276-vtrans-accelerating-transformer-compression-with-variational-information.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来は残差接続などの整合性が難しく埋め込みを温存する方式が多かったが、埋め込みが全パラメータの相当部分を占める小・中規模モデルでは、そこを残すことが極端な圧縮の障害となる。「剪定を25倍高速化」は生成TPSが25倍になる意味ではない。

- **2024-05 · [OpenBA-V2: Reaching 77.3% High Compression Ratio with Fast Multi-Stage Pruning](2024-2405.05957-openba-v2-reaching-77-3-high-compression-ratio-with-fast-multi-stage-pru.md)**  
  実装：[✓](https://github.com/OpenNLG/OpenBA-v2) ・ リポジトリ内被引用：0  
  OpenBA-V2は、中国語・英語を中心に学習したencoder-decoder型のOpenBA（15Bパラメータ）を、3.4Bへ縮小するための多段階圧縮・継続事前学習の研究である。元モデルから約77.3%のパラメータを削除しながら、層単位、行列の幅方向、語彙埋め込みという異なる削減対象を順番に処理する。

- **2024-03 · [Toward Adaptive Large Language Models Structured Pruning via Hybrid-grained Weight Importance Assessment](2024-2403.10799-toward-adaptive-large-language-models-structured-pruning-via-hybrid-grai.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  粗い粒度と細かい粒度のテイラー重要度推定を層の役割に応じて適応的に融合する構造化枝刈りで、LLaMA-7Bを20パーセント削っても単一粒度方式より平均正解率を保ち、遅延を約1.82倍速くする。

### 4年前（2022-12〜2023-11）

- **2023-05 · [LLM-Pruner: On the Structural Pruning of Large Language Models](2023-2305.11627-llm-pruner-on-the-structural-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/horseee/LLM-Pruner) ・ リポジトリ内被引用：325  
  LLM-Prunerは、大規模言語モデルのパラメータを実際に削除して小さい密行列モデルへ変換する構造枝刈り手法である。LLaMA-7B、Vicuna-7B、ChatGLM-6Bを評価し、LLaMA-7Bでは20%の構造削減でゼロショット七課題平均が63.25から56.82へ下がり、低ランク適応後60.07まで回復した。

- **2023-10 · [Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning](2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pr.md)**  
  実装：[✓](https://github.com/princeton-nlp/LLM-Shearing) ・ リポジトリ内被引用：123  
  枝刈り直後に失われた能力は継続事前学習で回復するが、その際にも学習データを元の比率で使い続けず、領域別の損失回復状況に応じて再配分する。A100 80GB上の単一生成で、13億パラメータの均一形状は毎秒58トークン、非均一形状は51トークン、27億では43対37トークンであった。

- **2023-05 · [LoRAPrune: Structured Pruning Meets Low-Rank Parameter-Efficient Fine-Tuning](2023-2305.18403-loraprune-structured-pruning-meets-low-rank-parameter-efficient-fine-tun.md)**  
  実装：[✓](https://github.com/aim-uofa/LoRAPrune) ・ リポジトリ内被引用：40  
  LoRAPruneは、事前学習済み大規模言語モデルを配備しやすい小型の密モデルへ変えるために、低ランク適応（Low-Rank Adaptation、LoRA）と構造化枝刈り（structured 枝刈り）を一体化する方式である。

- **2023-10 · [Compresso: Structured Pruning with Collaborative Prompting Learns Compact Large Language Models](2023-2310.05015-compresso-structured-pruning-with-collaborative-prompting-learns-compact.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  Compressoは、大規模言語モデルの注意ヘッド、中間層のチャネル、隠れ次元をまとめて削除する構造化枝刈りの手法である。評価の中心はモデル規模と正答率であり、実機のトークン毎秒や消費電力の改善倍率は示されていない。

- **2023-09 · [Pruning Large Language Models via Accuracy Predictor](2023-2309.09507-pruning-large-language-models-via-accuracy-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  大規模言語モデルの枝刈りを「どの重みを削るか」だけでなく「どの層を何割削るか」という探索問題として扱い、少数の実測品質から決定木型予測器を学習する。推論速度の測定ではなく、圧縮率とタスク品質の交換条件を改善する研究である。

- **2023-10 · [NASH: A Simple Unified Framework of Structured Pruning for Accelerating Encoder-Decoder Language Models](2023-2310.10054-nash-a-simple-unified-framework-of-structured-pruning-for-accelerating-e.md)**  
  実装：[✓](https://github.com/jongwooko/NASH-Pruning-Official) ・ リポジトリ内被引用：0  
  復号器は層を均等に間引いて浅くし、符号化器は幅を低い疎さで徐々に狭める非対称な枝刈りで、T5-baseの要約で品質をほぼ保ちながら実時間2.5倍から4.2倍の高速化を示した。

- **2022-12 · [Gradient-based Intra-attention Pruning on Pre-trained Language Models](2022-2212.07634-gradient-based-intra-attention-pruning-on-pre-trained-language-models.md)**  
  実装：[✓](https://github.com/airaria/GRAIN) ・ リポジトリ内被引用：0  
  注意ヘッド内部の次元を勾配重要度で反復的に落とし、構造正則化と勾配分離つき知識蒸留、埋め込み因数分解を組み合わせて、密度5%で教師の93〜99%の性能と6〜7倍の高速化を得る事前学習言語モデルの構造化枝刈り。

### 5年前（2021-12〜2022-11）

- **2022-04 · [Structured Pruning Learns Compact and Accurate Models](2022-2204.00408-structured-pruning-learns-compact-and-accurate-models.md)**  
  実装：[✓](https://github.com/princeton-nlp/CoFiPruning) ・ リポジトリ内被引用：51  
  一方、あらかじめ小型の学生モデルを定めて知識蒸留する方式は、推論しやすい構造を得られるが、大量の未ラベル文章で一般蒸留を行う費用が大きい。MNLIの約95%剪定条件ではBERT-base比12.1倍の推論高速化と精度80.6を報告し、QNLIでも12.1倍・86.1を報告する。

- **2022-04 · [A Fast Post-Training Pruning Framework for Transformers](2022-2204.09656-a-fast-post-training-pruning-framework-for-transformers.md)**  
  実装：[✓](https://github.com/WoosukKwon/retraining-free-pruning) ・ リポジトリ内被引用：45  
  Transformerの計算量と推論遅延を減らすために、不要な注意頭や順伝播層のフィルタを削る構造化枝刈りが使われる。品質低下を1%以内に抑えながら、BERT Baseでは元の演算量の60〜70%程度まで、DistilBERTでは条件により50%まで減らした。

- **2021-12 · [DAP-BERT: Differentiable Architecture Pruning of BERT](2021-0028045aea9f-dap-bert-differentiable-architecture-pruning-of-bert.md)**  
  実装：[✓](https://github.com/OscarYau525/DAP-BERT) ・ リポジトリ内被引用：0  
  DAP-BERTは、既存のBERTモデルから、実行装置の演算制約に応じて不要な注意ヘッドとFeed-順伝播 Network（FFN）の中間次元を選択的に除去する、微分可能な構造化枝刈り方式である。

### 7年前（2019-12〜2020-11）

- **2020-04 · [On the Effect of Dropping Layers of Pre-trained Transformer Models](2020-2004.03844-on-the-effect-of-dropping-layers-of-pre-trained-transformer-models.md)**  
  実装：[✓](https://github.com/hsajjad/transformers/) ・ リポジトリ内被引用：28  
  事前学習済みBERT系モデルの上位層を削除して推論時間を約半減し、モデル・タスクごとの精度低下と下位層の重要性を比較した構造的圧縮研究。

### 8年前（2018-12〜2019-11）

- **2019-05 · [Are Sixteen Heads Really Better than One?](2019-1905.10650-are-sixteen-heads-really-better-than-one.md)**  
  実装：[✓](https://github.com/pmichel31415/are-16-heads-really-better-than-1) ・ リポジトリ内被引用：112  
  Michelらは、学習済みの翻訳用TransformerとBERTの各注意ヘッドを無効化して、品質の変化、ヘッド重要度の推定、構造的な枝刈り後の推論速度を実験した。WMT14英仏翻訳のTransformerでは全ヘッドの約20%、MultiNLIに微調整したBERTでは約40%を重要度順に削っても顕著な品質低下が生じなかった。

- **2019-05 · [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](2019-1905.09418-analyzing-multi-head-self-attention-specialized-heads-do-the-heavy-lifti.md)**  
  実装：[✓](https://github.com/lena-voita/the-story-of-heads) ・ リポジトリ内被引用：97  
  本論文は、翻訳用Transformerの多頭注意機構において、各ヘッドの計算が同じだけ必要なのかを、予測への寄与と実際の削除耐性の両側面から調べた研究である。一方、これは2019年の機械翻訳Transformerにおける品質評価であり、現代の生成専用LLMで実際に同じ割合の実行時間や鍵・値キャッシュ容量を削減できると証明した結果ではない。

- **2019-09 · [Reducing Transformer Depth on Demand with Structured Dropout](2019-1909.11556-reducing-transformer-depth-on-demand-with-structured-dropout.md)**  
  実装：✓ ・ リポジトリ内被引用：89  
  深いTransformerは学習時に層をすべて使用する前提で最適化されるため、学習後に連続した層を削ると、残った層が想定しない中間表現を受け取り品質が悪化する。深度ごとに新しいモデルを一から学習したり知識蒸留を繰り返したりする方法では、必要な配備構成が増えるほど学習費用が増える。深度削減は品質低下を完全に取り除くわけではない。
<!-- survey:auto:end -->
