# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（85本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/04-conditional-computation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-09 · [LayerRoute: Adaptive Layer-Skipping with LoRA-Preserved Quality for Efficient LLM Inference](2026-2609.13682-layerroute-adaptive-layer-skipping-with-lora-preserved-quality-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同時にランク-8 LoRAを注意機構 射影へ入れ、層を飛ばすことで失われる表現能力をパラメータ-efficientに補償する。壁時計速度は全試行で改善し1.02〜1.06倍、平均1.04倍。

- **2026-08 · [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](2026-2608.07088-rora-role-oriented-regional-allocation-for-visual-token-pruning-in-mllms.md)**  
  実装：[✓](https://github.com/LukieLuu/RoRA) ・ リポジトリ内被引用：1  
  高解像度画像や複数画像では、画像に由来するトークンが入力系列の多くを占め、事前計算（プリフィル）の演算、注意機構のキー・バリュー（KV）キャッシュ、応答開始までの時間を増加させる。LLaVA-1.5-7Bの視覚576トークンを64個へ減らす条件（88.9%削減）では、九つの評価課題の正規化平均が非削減時の96.5%に相当した。

- **2026-08 · [DiffPrune: Differentiable Information Throttling for Token Pruning in Vision-Language Models](2026-2608.01985-diffprune-differentiable-information-throttling-for-token-pruning-in-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚言語モデル（Vision-Language モデル; VLM）では、画像エンコーダが数百〜数千の視覚トークンを生成する。言語モデルへ渡す視覚トークンを減らせば事前処理（プリフィル）の計算量と遅延を削減できるが、「どのトークンを残すか」を学習する段階で問題が生じる。この演算子不一致が重要度学習を不安定にする。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-09 · [FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference](2026-2609.17008-flexee-self-speculative-and-kv-compatible-early-exiting-for-offloading-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Top-K自己投機による軽量な早期退出と隠れ状態の持越しでKV整合性を保ち、重みオフロード時に後段層の計算と転送をまとめて省く。

- **2026-09 · [Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference](2026-2609.08189-hero-history-aware-routing-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の局所状態だけでなく過去のゲート選択と残差変化を線形注意メモリへ蓄積し、Llama 3.1-8Bで26.87%のパラメータ計算を回避しつつ密モデル比100.24%の性能を保つ動的FFNルーティング。

- **2026-08 · [Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching](2026-2608.09444-depth-adaptive-inference-of-looped-language-models-via-continuous-depth-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  論文はCDBを端から端まで実装し、深度が不揃いになる鍵値キャッシュ（KV キャッシュ）、CPU側スケジューラとGPU側反復の同期、前段・後段をどの頻度で実行するかまで扱う。

- **2026-05 · [VideoRouter: Query-Adaptive Dual Routing for Efficient Long-Video Understanding](2026-2605.05848-videorouter-query-adaptive-dual-routing-for-efficient-long-video-underst.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VideoRouterは、固定の視覚トークン予算を「広く浅く」か「重要な場面へ厚く」かに配分する方式を質問ごとに決める。

- **2026-02 · [WiSparse: Boosting LLM Inference Efficiency with Weight-Aware Mixed Activation Sparsity](2026-2602.14452-wisparse-boosting-llm-inference-efficiency-with-weight-aware-mixed-activ.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論では、各層の線形射影が多数の乗算と重み読出を必要とする。WiSparseは、活性と重みの両方からチャネル重要度を推定し、モデル全体の疎性率をブロック・層の二段階で割り当てる学習不要の活性疎化（学習不要 活性値 sparsity）方式である。

- **2026-02 · [ConsensusDrop: Fusing Visual and Cross-Modal Saliency for Efficient Vision Language Models](2026-2602.00946-consensusdrop-fusing-visual-and-cross-modal-saliency-for-efficient-visio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ConsensusDropは、言語モデルに入る前に質問依存の画像顕著性を近似して取得し、視覚エンコーダ由来の顕著性と統合する。原著Table 1では、LLaVA-1.5-7Bの視覚トークン576個を32個へ削減したとき、九つの画像ベンチマークの集計精度が基準モデルの90.5%となり、TTFTは106.4msから60.0ms（1.77倍）へ短縮された。

- **2026-02 · [CLAA: Cross-Layer Attention Aggregation for Accelerating LLM Prefill](2026-2602.16054-claa-cross-layer-attention-aggregation-for-accelerating-llm-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CLAA（Cross-層 注意機構 Aggregation）は、層ごとに重要度順位が大きく変わるという現象を先に検証し、選別層の直前の複数層の重要度を各トークンについて最大値で集約する。

- **2026-01 · [ChunkWise LoRA: Adaptive Sequence Partitioning for Memory-Efficient Low-Rank Adaptation and Accelerated LLM Inference](2026-2601.21109-chunkwise-lora-adaptive-sequence-partitioning-for-memory-efficient-low-r.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク適応（LoRA）は、事前学習済みの重みを固定し、少数の低ランク行列を追加学習することで、モデルの更新費用を抑える。原著表Iでは、LLaMA-7Bを用いた比較で、通常のモデルが22.5ms/トークン、ピークGPUメモリ14.6GBに対し、提案方式は14.9ms/トークン、9.1GBを報告する。

- **2025-12 · [Mixture of Attention Schemes (MoAS): Learning to Route Between MHA, GQA, and MQA](2025-2512.20650-mixture-of-attention-schemes-moas-learning-to-route-between-mha-gqa-and-.md)**  
  実装：[✓](https://github.com/Esmail-ibraheem/Mixture-of-Attention-Schemes-MoAS) ・ リポジトリ内被引用：0  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各問い合わせ頭に独立したキー・バリュー（Key-Value; KV）頭を持ち、表現力が高い一方、生成時のKVキャッシュが大きくなる。これは条件付き計算の可能性を示す探索的結果であって、LLM推論の実用的高速化を実証した結果ではない。

### 2年前（2024-12〜2025-11）

- **2025-03 · [DivPrune: Diversity-based Visual Token Pruning for Large Multimodal Models](2025-2503.02175-divprune-diversity-based-visual-token-pruning-for-large-multimodal-model.md)**  
  実装：[✓](https://github.com/vbdi/divprune) ・ リポジトリ内被引用：60  
  提案方式は、情報量が高そうな個々のトークンを選ぶのではなく、選んだトークン同士が似過ぎないようにすることで、短い視覚列に異なる意味的領域を残そうとする。提案された距離選択を、言語モデルの最初の層より前、または途中層の視覚対応隠れ状態へ挿入できるが、主要な実験で最も良好だったのは最初の層の前に削減する構成である。

- **2025-02 · [Stop Looking for Important Tokens in Multimodal Language Models: Duplication Matters More](2025-2502.11494-stop-looking-for-important-tokens-in-multimodal-language-models-duplicat.md)**  
  実装：[✓](https://github.com/ZichenWen1/DART) ・ リポジトリ内被引用：45  
  従来は注意重みを使って重要そうなトークンを残す方式が多かった。LLaVA-Next-7Bの画像トークンを2880から320へ削減した条件では、総推論時間が36分16秒から18分13秒、事前充填時間が22分51秒から7分38秒へ短縮し、鍵値キャッシュは1512.1MBから168.0MBへ減少した。

- **2025-04 · [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)**  
  実装：[✓](https://github.com/iie-ycx/DEER) ・ リポジトリ内被引用：31  
  DEERは推論途中で最終回答を試し、自己評価の確信度が高ければ思考連鎖を終了し、低ければ元地点から続行する。追加学習なしで過剰な再検討を減らす。

- **2025-06 · [Beyond Attention or Similarity: Maximizing Conditional Diversity for Token Pruning in MLLMs](2025-2506.10967-beyond-attention-or-similarity-maximizing-conditional-diversity-for-toke.md)**  
  実装：[✓](https://github.com/Theia-4869/CDPruner) ・ リポジトリ内被引用：24  
  本論文は、質問に必要な画像情報を残しながら視覚トークンを減らすCDPrunerを提案する。LLaVA-1.5-7Bで視覚トークン576個から128個へ減らすと、10種類の評価指標の平均相対性能は99.0%である。

- **2024-12 · [Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification](2024-2412.00876-dynamic-llava-efficient-multimodal-large-language-models-via-dynamic-vis.md)**  
  実装：[✓](https://github.com/Osilly/dynamic_llava) ・ リポジトリ内被引用：22  
  動的-LLaVAは、マルチモーダル大規模言語モデル（マルチモーダル Large Language モデル; MLLM）の高速化を、画像トークンだけの削減ではなく「画像文脈と生成済み言語文脈の両方を、推論段階に応じて動的に疎化する」問題として扱う。予測は一度だけ行い、その保持/削除決定を後続層すべてで共有する。

- **2025-05 · [AdaptThink: Reasoning Models Can Learn When to Think](2025-2505.13417-adaptthink-reasoning-models-can-learn-when-to-think.md)**  
  実装：[✓](https://github.com/THU-KEG/AdaptThink) ・ リポジトリ内被引用：14  
  AdaptThinkは、問題ごとに「思考あり（Thinking）」と「思考なし（NoThinking）」のどちらで回答するかをモデル自身が選択できるよう、強化学習（Reinforcement Learning; RL）で訓練する方式である。

- **2025-04 · [Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification](2025-2504.05419-reasoning-models-know-when-they-re-right-probing-hidden-states-for-self-.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  長い思考連鎖（Chain of Thought; CoT）を生成する推論モデルは、最初に正解へ到達しても別の推論経路を探索し、同じ問題を何度も検証することがある。オンラインで検証器を挿入したサービングシステムの最初のトークン遅延、処理率、VRAM消費、GPU時間を直接測定した結果ではない。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：9  
  D-LLMは、大規模言語モデルのすべてのトークンに同じ層数の計算を行う必要はないという観点から、各トークン・各Transformer層でその層を実行するか省略するかを学習する動的深度方式である。代表的な設定では、完全な層を実行するLoRA基準の約52～59%の浮動小数点演算量で、多くの課題の品質を維持した。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：8  
  FlexiDepthは、すでに学習された大規模言語モデルの重みを変更せず、出力トークンごとに必要な層の計算量を変える手法である。原著のLlama-3-8B-Instruct（32層）では、平均8層を省いても6つの評価課題における平均性能保持率が100.7%となり、固定層省略方式より高い品質を示す。

- **2025-10 · [VisionSelector: End-to-End Learnable Visual Token Compression for Efficient Multimodal LLMs](2025-2510.16598-visionselector-end-to-end-learnable-visual-token-compression-for-efficie.md)**  
  実装：[✓](https://github.com/JulietChoo/VisionSelector) ・ リポジトリ内被引用：6  
  言語モデル側はそれらを文章トークンとともに入力として処理するため、画像の情報量が増えるほど初期入力計算（プリフィル）の時間と中間状態のメモリが増える。視覚トークンを一部だけ残せば高速になるが、単純に注意スコアが大きい位置を選ぶと、内容上重要でない先頭トークンへ注意が集中する「注意の吸い込み（注意機構 sink）」や、文字・図表の細部が欠落する問題が起きる。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  大規模言語モデルは、次の単語を推測するたびに、難しい計算を要する単語にも文脈からほぼ写すだけの単語にも同じ数の変換層を適用する。DiffSkipは、トークンと層の組ごとに、後続のフィードフォワードネットワーク（FFN）を実行するか、軽量な補正器で代替するかを判断する手法である。

- **2025-05 · [WINA: Weight Informed Neuron Activation for Accelerating Large Language Model Inference](2025-2505.19427-wina-weight-informed-neuron-activation-for-accelerating-large-language-m.md)**  
  実装：[✓](https://github.com/microsoft/wina) ・ リポジトリ内被引用：5  
  WINAは、既存の大規模言語モデル（LLM）を再学習せず、各層で計算に参加させる活性成分を選択する疎活性化方式である。代表例としてLlama-2-7Bの常識推論8課題平均では、65%の活性疎性でWINAが65.14、TEALが61.07、R-Sparseが59.37となった。

- **2025-10 · [Learning to Inference Adaptively for Multimodal Large Language Models](2025-2503.10905-learning-to-inference-adaptively-for-multimodal-large-language-models.md)**  
  実装：[✓](https://github.com/zhuoyan-xu/AdaLLaVA) ・ リポジトリ内被引用：3  
  一般的な軽量化方式では、視覚トークン削除数や層構成が推論開始前に固定され、要求ごとの計算予算や画像・質問の難しさに合わせて変更できない。LLaVA-1.5の7B構成で層単位版を60%予算にすると、論文のMME計測ではプリフィル計算量が8.6兆から5.1兆浮動小数点演算へ、時間が81msから49msへ減り、VQAv2正解率は78.5から75.0へ下がる。

- **2025-03 · [AdaReTaKe: Adaptive Redundancy Reduction to Perceive Longer for Video-language Understanding](2025-2503.12559-adaretake-adaptive-redundancy-reduction-to-perceive-longer-for-video-lan.md)**  
  実装：[✓](https://github.com/SCZwangxiao/video-FlexReduc) ・ リポジトリ内被引用：3  
  動画を長くするほど事前充填で扱う系列が増え、言語モデルの鍵・値キャッシュ（KVキャッシュ）がGPUメモリを圧迫する。すべてのフレームを同じ割合で圧縮すると、静止区間へ不要な容量を割り当てる一方、質問に必要な短い場面の情報を失う。これは処理可能な動画情報量と理解精度の結果であり、トークン生成速度が同倍率で向上するという主張ではない。

- **2025-05 · [ToDRE: Effective Visual Token Pruning via Token Diversity and Task Relevance](2025-2505.18757-todre-effective-visual-token-pruning-via-token-diversity-and-task-releva.md)**  
  実装：[✓](https://github.com/Yrdal3910/ToDRE) ・ リポジトリ内被引用：2  
  既存の削減方式は、視覚トークン同士の類似度か、テキストと視覚の注意スコアのどちらか一方を重複の指標として使うことが多い。

- **2025-03 · [Position-Aware Depth Decay Decoding (D³): Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  位置考慮型深さ減衰復号（Position-Aware 深度減衰 デコード; D³）は、大規模言語モデルの自己回帰生成で、出力トークンの位置に応じて実行するTransformer層数を減らす方式である。

- **2025-01 · [Instruction-Following Pruning for Large Language Models](2025-2501.02086-instruction-following-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  指示追従枝刈り（Instruction-Following Pruning、IFPruning）は、利用者の指示文から小型の疎性予測器が必要なフィードフォワード層（FFN）の中間次元を選び、その指示に対する応答の復号中は同じ部分ネットワークを固定して実行する手法である。

- **2025-11 · [Conv-Basis: A New Paradigm for Efficient Attention Inference and Gradient Computation in Transformers](2025-a7d4659aa00f-conv-basis-a-new-paradigm-for-efficient-attention-inference-and-gradient.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案方式は、相対位置差に沿った対角線状の反復パターンを「畳み込み基底（conv basis）」として表し、各基底に対応する畳み込みとVの積を高速フーリエ変換（Fast Fourier Transform; FFT）で計算する。

- **2025-08 · [ILRe: Intermediate Layer Retrieval for Context Compression in Causal Language Models](2025-2508.17892-ilre-intermediate-layer-retrieval-for-context-compression-in-causal-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Intermediate 層 Retrieval（ILRe）は、長大な入力を全層へそのまま通す代わりに、選択した中間デコーダ層までの処理で原文から重要トークンを選び直し、短いプロンプトとして再投入する文脈圧縮方式である。

- **2025-07 · [La RoSA: Enhancing LLM Efficiency via Layerwise Rotated Sparse Activation](2025-2507.01299-la-rosa-enhancing-llm-efficiency-via-layerwise-rotated-sparse-activation.md)**  
  実装：[✓](https://github.com/alibaba/EfficientAI) ・ リポジトリ内被引用：1  
  重みの量子化や枝刈りとは別に、入力活性の多くをゼロにできれば、ゼロに対応する重み列を読み込まずに済む。論文の代表例では、LLaMA2-7Bのモデル全体の活性疎性40%で困惑度の悪化が5.47から5.64への0.17にとどまり、7種のゼロ例示タスクの平均得点は66.69から66.15への0.54ポイント低下である。

- **2025-05 · [Scalable LLM Reasoning Acceleration with Low-rank Distillation](2025-2505.07861-scalable-llm-reasoning-acceleration-with-low-rank-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Capreseは、大規模言語モデルのフィードフォワードネットワーク（FFN）を疎化したとき、長い数学的推論で顕著になる精度低下を、小さな低ランク補正で回復する手法である。

- **2025-05 · [Beyond Hard and Soft: Hybrid Context Compression for Balancing Local and Global Information Retention](2025-2505.15774-beyond-hard-and-soft-hybrid-context-compression-for-balancing-local-and-.md)**  
  実装：[✓](https://github.com/Xnhyacinth/HyCo2) ・ リポジトリ内被引用：1  
  HyCo2（Hybrid Context Compression）は、長文脈の検索拡張生成（Retrieval-Augmented Generation; RAG）で、必要な情報を保持しながら入力トークン数を減らす圧縮方式である。デフォルトでは16個の潜在クエリと、原文トークンの上位10%を保持する設定である。

- **2025-09 · [EfficientUICoder: Efficient MLLM-based UI Code Generation via Input and Output Token Compression](2025-2509.12159-efficientuicoder-efficient-mllm-based-ui-code-generation-via-input-and-o.md)**  
  実装：[✓](https://github.com/WebPAI/EfficientUICoder) ・ リポジトリ内被引用：0  
  本研究は、ウェブ画面の画像を入力してHTMLとCSSを生成するUI-to-コードの推論費用を、画像側とコード側の両方から削減する方式である。

- **2025-02 · [Infinite Retrieval: Attention Enhanced LLMs in Long-Context Processing](2025-2502.12962-infinite-retrieval-attention-enhanced-llms-in-long-context-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純な窓移動では古い区間を忘れ、KVキャッシュ圧縮では過去情報の一部を固定された埋め込み表現として保存するため、質問に必要な文を失うことがある。

### 3年前（2023-12〜2024-11）

- **2024-03 · [An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models](2024-2403.06764-an-image-is-worth-1-2-tokens-after-layer-2-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/pkunlp-icler/FastV) ・ リポジトリ内被引用：146  
  LLaVA-1.5では一枚の336×336画像が576トークンになり、高解像度化や動画の複数フレーム処理では数千トークンへ増える。初期層では画像情報が広く注意される一方、深い層では少数のシステム指示や文章トークンへ注意が集中し、画像トークン一個当たりの注意効率が非常に低くなる。代表設定は二層後に視覚トークンの50%を削除する方式である。

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：141  
  LayerSkipは、大規模言語モデルの全ての層を毎トークン実行する代わりに、浅い層から次トークンを予測できるよう学習し、その予測を同じモデルの残りの層で検証する方式である。下書きモデルの生成結果を大きなモデルで一括検証することで生成時間を短縮できるが、二つのモデルの重みや鍵・値キャッシュを管理する必要がある。

- **2024-03 · [LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models](2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-m.md)**  
  実装：[✓](https://github.com/42Shawn/LLaVA-PruMerge) ・ リポジトリ内被引用：107  
  LLaVA-PruMergeは、画像を大規模言語モデルへ渡す際の視覚トークン数を削減する方式である。LLaVA-1.5は336×336画素の画像から24×24個、すなわち576個の視覚トークンを生成する。

- **2024-10 · [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](2024-2410.04417-sparsevlm-visual-token-sparsification-for-efficient-vision-language-mode.md)**  
  実装：[✓](https://github.com/Gumpest/SparseVLMs) ・ リポジトリ内被引用：96  
  SparseVLMは、視覚言語モデル（VLM）の入力画像から生じる大量の視覚トークンを、現在の質問に必要な情報をできるだけ残しながら削減する追加学習不要の方式である。

- **2024-10 · [PyramidDrop: Accelerating Your Large Vision-Language Models via Pyramid Visual Redundancy Reduction](2024-2410.17247-pyramiddrop-accelerating-your-large-vision-language-models-via-pyramid-v.md)**  
  実装：[✓](https://github.com/Cooperx521/PyramidDrop) ・ リポジトリ内被引用：75  
  大規模視覚言語モデル（Large Vision-Language モデル; LVLM）は、画像を数百から数千の画像トークンへ変換して、文章の質問と一緒に言語モデルへ入力する。画像解像度が上がると画像トークンが増え、注意計算と全結合層の演算量が大きくなる。複数の視覚言語ベンチマークで品質は概ね維持されるが、個別の高解像度課題では小さな低下もある。

- **2024-04 · [Mixture-of-Depths: Dynamically allocating compute in transformer-based language models](2024-2404.02258-mixture-of-depths-dynamically-allocating-compute-in-transformer-based-la.md)**  
  実装：✓ ・ リポジトリ内被引用：67  
  そのため、簡単な予測位置も難しい予測位置も同じ計算を受ける。方式の要点は、処理するトークンの「個数」kを事前に固定し、「どのトークンか」だけを学習済みルータが動的に選ぶ点にある。論文の代表構成では系列長2048に対し、一つおきの層で上位256トークン、すなわち12.5%だけを自己注意とMLPへ通す。

- **2024-06 · [D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models](2024-2406.13035-d2o-dynamic-discriminative-operations-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：45  
  全層へ同じKVキャッシュ量を与えず、プリフィル時の注意密度から浅い層へ大きく、深い層へ小さく予算を配る。さらに追い出し候補を永久削除せず、保持トークンとの類似度を再判定して情報を重み付き統合する。学習なしで長文品質を保ちつつ、フルKVキャッシュ比で最大3.04倍のスループットを示す。

- **2024-05 · [Boosting Multimodal Large Language Models with Visual Tokens Withdrawal for Rapid Inference](2024-2405.05803-boosting-multimodal-large-language-models-with-visual-tokens-withdrawal-.md)**  
  実装：[✓](https://github.com/lzhxmu/VTW) ・ リポジトリ内被引用：36  
  例えばLLaVAでは336×336画像を576個の視覚トークンに変換し、システム指示、ユーザー質問、生成済みのテキストトークンとともにデコーダへ流す。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：35  
  LazyLLMは、長い入力文のすべてのトークンを全変換層で計算する慣行を改め、現在予測しようとしている次のトークンに重要な入力部分だけを深い層へ進める推論時の計算削減法である。

- **2024-11 · [DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models](2024-2411.15024-dycoke-dynamic-compression-of-tokens-for-fast-video-large-language-model.md)**  
  実装：[✓](https://github.com/KD-TAO/DyCoke) ・ リポジトリ内被引用：32  
  DyCokeは、動画を入力とする大規模言語モデルが多数のフレームを視覚トークンへ変換する際に生じる、注意計算と鍵・値（KV）キャッシュの増大を抑える学習不要の圧縮方式である。原著のLLaVA-OneVision 7Bによる32フレーム評価では、基準方式の一例当たり遅延2.30秒・メモリ34GBに対し、DyCokeは1.49秒・24GBとなった。

- **2024-10 · [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](2024-2410.17434-longvu-spatiotemporal-adaptive-compression-for-long-video-language-under.md)**  
  実装：[✓](https://github.com/Vision-CAIR/LongVU) ・ リポジトリ内被引用：29  
  LongVUは、長時間動画を多模態大規模言語モデルへ入力するとき、視覚トークン数が文脈長を超える問題に対して、時間方向の冗長なフレーム削除、質問に応じた空間解像度の配分、フレーム間で重複する空間トークンの削除を段階的に組み合わせる方式である。

- **2024-08 · [Training-Free Activation Sparsity in Large Language Models](2024-2408.14690-training-free-activation-sparsity-in-large-language-models.md)**  
  実装：[✓](https://github.com/FasterDecoding/TEAL) ・ リポジトリ内被引用：27  
  隠れ状態の小振幅成分を層別にゼロ化し、対応重みチャネルを読まない専用カーネルで、追加学習なしに40〜50%のモデル全体活性疎性と最大1.8倍のデコード高速化を実現する。

- **2024-03 · [Not All Layers of LLMs Are Necessary During Inference](2024-2403.02181-not-all-layers-of-llms-are-necessary-during-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  本論文は、デコーダ専用大規模言語モデルの各入力を必ず最終層まで通すことによる過剰計算を、入力単位の早期終了で減らすAdaInferを提案する。原著第3版の主評価では、Llama 2の7B・13BとOPT-13Bで層削減率は課題により約9〜43%、平均17.8%となる。

- **2024-09 · [Discovering the Gems in Early Layers: Accelerating Long-Context LLMs with 1000x Input Token Reduction](2024-2409.17422-discovering-the-gems-in-early-layers-accelerating-long-context-llms-with.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GemFilter) ・ リポジトリ内被引用：16  
  GemFilterは、長い入力文脈を持つ大規模言語モデル（LLM）の推論を高速化するため、回答に関係する入力トークンをモデルの比較的早い層で選び、その短い部分列だけを全層で再処理する手法である。

- **2024-06 · [Turbo Sparse: Achieving LLM SOTA Performance with Minimal Activated Parameters](2024-2406.05955-turbo-sparse-achieving-llm-sota-performance-with-minimal-activated-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  SwiGLUのゲート側だけでなくup射影側にもReLUを掛ける二重ReLU（dReLU）へ置換し、継続事前学習で性能を回復する。Mistral-7BはFFNの約90%、Mixtral-47Bは専門家ルーティング込みで約97%を非活性化し、PowerInfer系の疎実行で2〜5倍のデコード高速化を報告する。

- **2024-11 · [FFN-SkipLLM: A Hidden Gem for Autoregressive Decoding with Adaptive Feed Forward Skipping](2024-2404.03865-ffn-skipllm-a-hidden-gem-for-autoregressive-decoding-with-adaptive-feed-.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  将来トークンが参照するキャッシュに穴が生じるため、過去状態をコピーしたり鍵・値を再計算したりする追加対策が必要となる。提案法は各層の自己注意を維持し、FFNに入る状態とFFN残差更新後の状態のコサイン類似度（cosine similarity）から、中間層の冗長なFFNを検出する。

- **2024-09 · [Oryx MLLM: On-Demand Spatial-Temporal Understanding at Arbitrary Resolution](2024-2409.12961-oryx-mllm-on-demand-spatial-temporal-understanding-at-arbitrary-resoluti.md)**  
  実装：[✓](https://github.com/Oryx-mllm/Oryx) ・ リポジトリ内被引用：7  
  主要な設計要素は、入力画像の縦横比と解像度を維持して視覚特徴を抽出するOryxViTと、画像・短動画・長動画の用途に応じて視覚トークン数を1倍から最大16倍まで圧縮する動的圧縮器（動的 compressor）である。

- **2024-04 · [Accelerating Inference in Large Language Models with a Unified Layer Skipping Strategy](2024-2404.06954-accelerating-inference-in-large-language-models-with-a-unified-layer-ski.md)**  
  実装：[✓](https://github.com/Adaxry/Unified_Layer_Skipping) ・ リポジトリ内被引用：7  
  大規模言語モデル（LLM）の自動回帰生成では、次トークンを作るたびに多数のTransformer層を通る。したがって、論文は無劣化の高速化ではなく、実行層数・生成処理量・翻訳や要約の品質の交換関係を改善する方式を提案している。

- **2024-10 · [MoH: Multi-Head Attention as Mixture-of-Head Attention](2024-2410.11842-moh-mixture-of-head-attention.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoH) ・ リポジトリ内被引用：6  
  注意ヘッドを共有ヘッドとTop-Kルーティングヘッドに分け、トークンごとに必要なヘッドだけ使うMoH。LLaMA3-8Bで75%利用・14評価平均64.0%を達成。

- **2024-11 · [SparseInfer: Training-free Prediction of Activation Sparsity for Fast LLM Inference](2024-2411.12692-sparseinfer-training-free-prediction-of-activation-sparsity-for-fast-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  大規模言語モデルの逐次生成では、要求ごとの同時処理数が小さいと、フィードフォワード網の大きな重み行列をGPUメモリから読み出す費用が律速になる。入力によってゼロになる中間活性を事前に予測できれば、その活性に対応する行の重み読込みと行列ベクトル積を省略できる。しかし、一般的なLLaMAの滑らかな活性化関数であるSiLUでは、負の値も厳密にはゼロになりにくい。

- **2024-11 · [Accelerating Multimodal Large Language Models by Searching Optimal Vision Token Reduction](2024-2412.00556-accelerating-multimodal-large-language-models-by-searching-optimal-visio.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  この観察に「深い層で必要になる重要トークンは浅い層でも必要である」という仮定を加え、層別の保持率を浅い側から決める貪欲探索（Greedy Search、G-Search）を提案する。

- **2024-10 · [CoreInfer: Accelerating Large Language Model Inference with Semantics-Inspired Adaptive Sparse Activation](2024-2410.18311-coreinfer-accelerating-large-language-model-inference-with-semantics-ins.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  文の意味が安定している間は、生成トークンが変わっても必要なFFNニューロンの集合は大きく変わらない。プリフィル時に文単位の重要ニューロンを決めて生成中に固定し、トークンごとの予測器と頻繁な重み配置変更を避ける。

- **2024-06 · [DEED: Dynamic Early Exit on Decoder for Accelerating Encoder-Decoder Transformer Models](2024-2311.08623-deed-dynamic-early-exit-on-decoder-for-accelerating-encoder-decoder-tran.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  浅い層の表現を深い層の状態としてそのままコピーする従来の停止・コピー方式は、層間の意味表現の違いを無視して精度を損なう。正式版のT5-large・SQuADでは、総遅延が221.9msから57.6ms（約74.0%短縮）、F1が92.1から91.6となった。

- **2024-02 · [HiRE: High Recall Approximate Top-k Estimation for Efficient LLM Inference](2024-2402.09360-hire-high-recall-approximate-top-k-estimation-for-efficient-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  HiRE（High Recall Approximate Top-k Estimation）は、自己回帰型の大規模言語モデル（LLM）で次トークンを生成するとき、必要な重み行・列を入力に応じて少数だけ読み込む方式である。

- **2024-05 · [VideoTree: Adaptive Tree-based Video Representation for LLM Reasoning on Long Videos](2024-2405.19209-videotree-adaptive-tree-based-video-representation-for-llm-reasoning-on-.md)**  
  実装：[✓](https://github.com/Ziyang412/VideoTree) ・ リポジトリ内被引用：2  
  高関連クラスタだけを再分割して細部を調べるため、動画全体を均一に密な説明文へ変換する方式より、不要なフレーム説明や冗長な言語入力を減らせる。原著の主な根拠は、EgoSchema検証部分集合で66.2%の正答率、LLoVi-bestの61.2%に対して20.1秒対24.8秒という比較である。

- **2024-02 · [EE-Tuning: An Economical yet Scalable Solution for Tuning Early-Exit Large Language Models](2024-2402.00518-ee-tuning-an-economical-yet-scalable-solution-for-tuning-early-exit-larg.md)**  
  実装：[✓](https://github.com/pan-x-c/EE-LLM) ・ リポジトリ内被引用：2  
  EE-Tuningは、既存の大規模言語モデル（Large Language モデル; LLM）を、全パラメータの再学習なしに早期終了（early exit）できるモデルへ変換する手法である。論文本文では13Bの追加学習を4基のA800 GPUで約5時間、ピークGPUメモリ約20GB、70Bを約30時間、ピーク約78GBと報告する。

- **2024-11 · [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](2024-2411.17465-showui-one-vision-language-action-model-for-gui-visual-agent.md)**  
  実装：[✓](https://github.com/showlab/ShowUI) ・ リポジトリ内被引用：1  
  一方、画像を粗く統合してしまうと、クリック対象の小さな部品の座標を失いやすい。Qwen2-VL-2Bを基盤に、25.6万件の指示データで学習したモデルは、ScreenSpotのゼロショット画面要素特定で75.1%を報告した。

- **2024-10 · [FiRST: Finetuning Router-Selective Transformers for Input-Adaptive Latency Reduction](2024-2410.12513-first-finetuning-router-selective-transformers-for-input-adaptive-latenc.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FiRST（Finetuning Router-Selective Transformers）は、入力系列によって必要なTransformer層が異なるという観察に基づき、各層の前へ軽量ルータを挿入して推論時に通過層を選択する方式である。

- **2024-10 · [MoDification: Mixture of Depths Made Easy](2024-2410.14268-modification-mixture-of-depths-made-easy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoDificationは、既存の大規模言語モデル（Large Language モデル; LLM）を、各トークンに必要な層の計算だけを実行する深さの混合（Mixture of Depths; MoD）方式へ変換する研究である。

- **2024-05 · [Switchable Decision: Dynamic Neural Generation Networks](2024-2405.04513-switchable-decision-dynamic-neural-generation-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  問題設定。事前学習したTransformerを軽量化する一般的な方法は、枝刈り、量子化、知識蒸留などによって固定された小型モデルを作る。

### 4年前（2022-12〜2023-11）

- **2023-10 · [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-.md)**  
  実装：[✓](https://aka.ms/LongLLMLingua) ・ リポジトリ内被引用：65  
  LongLLMLinguaは、長いプロンプトを単に一律に切り詰めるのではなく、「質問に対してどの文書・トークンが有用か」を小型言語モデルで推定し、重要部分へトークン予算を集中させる長文脈プロンプト圧縮法である。

- **2023-10 · [Compressing Context to Enhance Inference Efficiency of Large Language Models](2023-2310.06201-compressing-context-to-enhance-inference-efficiency-of-large-language-mo.md)**  
  実装：[✓](https://github.com/liyucheng09/Selective_Context) ・ リポジトリ内被引用：61  
  長い文書や会話を大規模言語モデル（LLM）へ入力すると、初回入力処理と鍵・値キャッシュに多くの時間・メモリが必要になる。Selective Contextは、下流モデルの構造や重みを変更する代わりに、入力文脈に含まれる予測しやすい語句を事前に削り、残った自然言語テキストだけを渡す。

- **2023-07 · [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：37  
  トークンごとに途中で処理を終了する早期終了（early exit）は計算を減らせるが、従来の方式をそのまま実際の配信へ持ち込むと、二つの問題が生じる。原著は2023年のプレプリントで、OPT-1.3BとOPT-6.7Bを使い、構造化情報からの文章生成、短文要約、ニュース要約で目標2～5倍の高速化設定を比較した。

- **2023-10 · [ReLU Strikes Back: Exploiting Activation Sparsity in Large Language Models](2024-2310.04564-relu-strikes-back-exploiting-activation-sparsity-in-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  大規模言語モデルは推論時に膨大な重みを読み出す。特に小さなバッチでの一トークンずつの生成では、演算器のピーク性能より高帯域メモリからの重み移動が制約になることが多い。滑らかな活性化関数であるSiLUやGELUは、負の入力でも通常は厳密なゼロを出さないため、出力が小さくても対応する重みの読み出しを機械的に省略しにくい。

- **2023-07 · [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](2023-2307.16449-moviechat-from-dense-token-to-sparse-memory-for-long-video-understanding.md)**  
  実装：[✓](https://github.com/rese1f/MovieChat) ・ リポジトリ内被引用：18  
  MovieChatは、固定長の短期記憶を逐次更新し、古いフレームを類似度に応じて統合した長期記憶へ送ることで、この問題を扱う。原著図1は、224×224画素のフレームを標本抽出なしで処理する視覚側の条件で、24GB GPU上で10,000フレーム超を扱えると報告する。

- **2023-03 · [CoLT5: Faster Long-Range Transformers with Conditional Computation](2023-2303.09752-colt5-faster-long-range-transformers-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  軽量経路を全トークン、高容量の注意・MLPを学習ルータが選ぶ少数トークンだけへ適用し、16k入力でLongT5比35〜75%の学習高速化・50〜100%の推論高速化を示す。

- **2023-05 · [Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs](2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-a.md)**  
  実装：[✓](https://sample-step-by-step.info) ・ リポジトリ内被引用：14  
  大規模言語モデル（LLM）で多段階推論の精度を上げる自己整合性（自己整合性）は、同じ質問に対して複数の思考連鎖を標本化し、最終回答を多数決する方式である。最大7.9倍の節約は個別条件の値であり、全条件平均ではない。

- **2023-11 · [Learning to Skip for Language Modeling](2023-2311.15436-learning-to-skip-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  モデルを深くすれば表現容量は増えるが、トークン当たりの行列演算と復号遅延も増える。提案するSkipLayerは各層を二値ルータで包み、トークンの現在の隠れ表現から「この層を実行する」か「入力をそのまま次層へ渡す」かを選ぶ。

- **2023-10 · [Sparse Universal Transformer](2023-2310.07096-sparse-universal-transformer.md)**  
  実装：[✓](https://github.com/shawntan/SUT) ・ リポジトリ内被引用：10  
  Sparse Universal Transformer（SUT）は、同じTransformerブロックを複数回反復するユニバーサルTransformer（Universal Transformer; UT）の長所を残しながら、反復計算を疎な専門家選択と動的停止で削減するモデルである。通常のTransformerは各層に別の重みを持つ。

### 5年前（2021-12〜2022-11）

- **2022-08 · [Learned Token Pruning for Transformers](2022-2107.00910-learned-token-pruning-for-transformers.md)**  
  実装：[✓](https://github.com/kssteven418/LTP) ・ リポジトリ内被引用：22  
  この論文の対象は、入力文の全トークンを全Transformer層で処理するために生じる推論計算量である。一次資料としてKDD 2022の原論文に加え、筆頭著者が2023年に公表した同方式の31ページの学位論文（UC Berkeley EECS-2023-119）の方法・評価・議論を参照した。

- **2022-03 · [Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space](2022-2203.14680-transformer-feed-forward-layers-build-predictions-by-promoting-concepts-.md)**  
  実装：[✓](https://github.com/aviclu/ffn-values) ・ リポジトリ内被引用：7  
  Transformerの順伝播層（feed-順伝播 network、FFN）は、自己注意層で得た表現を更新するが、どのような内部操作が次トークンの予測を形作るかは分かりにくい。本論文は、FFNが出力するベクトルを、個々の値ベクトルに入力依存の係数を掛けた小さな加算成分の和として分解し、各成分が語彙中のどのトークンを押し上げるかを調べる。

- **2022-03 · [Pyramid-BERT: Reducing Complexity via Successive Core-set based Token Selection](2022-2203.14380-pyramid-bert-reducing-complexity-via-successive-core-set-based-token-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案するPyramid-BERTは、各エンコーダ層の間で代表的なトークン表現の部分集合を選び、層が深くなるにつれて系列長を減らす。BERT-baseを用いたGLUEの開発集合では、推論時間を約3倍高速化する系列長構成で、原型の平均81.5に対して提案手法の最良設定が80.0を記録した。

### 6年前（2020-12〜2021-11）

- **2021-04 · [BERxiT: Early Exiting for BERT with Better Fine-Tuning and Extension to Regression](2021-3c0f54f14532-berxit-early-exiting-for-bert-with-better-fine-tuning-and-extension-to-r.md)**  
  実装：[✓](https://github.com/castorini/berxit) ・ リポジトリ内被引用：17  
  従来の早期終了では、最後の層で良い予測を得ることと、中間層でも十分に良い予測を得ることの学習目標が競合しやすい。BERxiTはこの二つを別々の機構で解決する。例えばBERTBASEのSST-2試験集合では、交互微調整によって元モデルの得点の98%を保ちながら実行層数を65%減らす条件があり、より強い早期終了では96%の得点に対して79%の層削減を得る。

- **2021-06 · [TR-BERT: Dynamic Token Reduction for Accelerating BERT Inference](2021-00c8b8f9f90e-tr-bert-dynamic-token-reduction-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/thunlp/TR-BERT) ・ リポジトリ内被引用：9  
  選択しなかったトークンの表現はその層で凍結し、最終予測時には終了時の表現を回収する。表2の代表条件では、SQuAD 2.0でBERTのF1 77.12に対しTR-BERT12は75.66、演算回数の比で2.08倍の削減である。

- **2021-10 · [Magic Pyramid: Accelerating Inference with Early Exiting and Token Pruning](2021-2111.00230-magic-pyramid-accelerating-inference-with-early-exiting-and-token-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  文章分類器BERTの推論で、後続層へ運ぶトークン数を減らす枝刈りと、十分に確信できた入力の層処理を途中終了する機構を組み合わせる。入力長により得意条件が異なる二つの削減方法を重ね、五つの分類課題で演算量と精度の交換条件を評価した研究。表に示す4.95倍や8.25倍は浮動小数点演算量から計算した削減倍率であり、GPUの実時間高速化をそのまま意味しない。

### 7年前（2019-12〜2020-11）

- **2020-04 · [DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference](2020-2004.12993-deebert-dynamic-early-exiting-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/castorini/DeeBERT) ・ リポジトリ内被引用：56  
  DeeBERTは、BERT系の分類モデルで入力ごとに必要なTransformer層数が異なることを利用し、浅い層ですでに十分確信度の高い予測が得られた例を途中で返す動的早期終了（動的 early exiting）方式である。

- **2020-06 · [BERT Loses Patience: Fast and Robust Inference with Early Exit](2020-2006.04152-bert-loses-patience-fast-and-robust-inference-with-early-exit.md)**  
  実装：✓ ・ リポジトリ内被引用：42  
  浅い層で正しい分類がほぼ確定している入力にも後段層の計算を続けるため、不要な遅延が生じる。従来の早期終了方式は中間分類器の最大確率やエントロピーなど、一つの層での自信の強さを停止信号にすることが多かった。

- **2020-04 · [FastBERT: a Self-distilling BERT with Adaptive Inference Time](2020-2004.02178-fastbert-a-self-distilling-bert-with-adaptive-inference-time.md)**  
  実装：[✓](https://github.com/autoliuweijie/FastBERT) ・ リポジトリ内被引用：42  
  この設計は文章生成の各トークンを省略する方式ではなく、主に文章分類と文対照合に適用される。例えば中国語THUCNewsでは閾値0.1で分類精度96.71%を維持しつつ計算量が約6.05分の1、英語DBpediaでは同閾値で99.31%から99.28%への微小な低下と引き換えに約10.57分の1となる。

- **2020-01 · [PoWER-BERT: Accelerating BERT Inference via Progressive Word-vector Elimination](2020-2001.08950-power-bert-accelerating-bert-inference-via-progressive-word-vector-elimi.md)**  
  実装：[✓](https://github.com/IBM/PoWER-BERT) ・ リポジトリ内被引用：17  
  方式は二つの判断を分離する。原著のK80 GPU、Keras、バッチ128（RACEのみ32）の評価では、BERTBASE比で各課題2.0～4.5倍の推論時間短縮を報告する。
<!-- survey:auto:end -->
