# Diffusion Language Model Decoding Efficiency

離散・masked diffusion言語モデルの生成token commit順序・並列幅、denoising回数、単一request内のrefinement/advancement依存、候補軌道の分岐・剪定・計算配分を制御し、NFEやlatency/throughputと品質の関係を改善する研究をまとめる。

## 分類境界

Include inference-time methods whose primary mechanism schedules, selects, branches, prunes, or verifies denoising states or token commitments within a discrete/masked diffusion-LM request, with direct evidence on denoising rounds/NFE, latency/throughput, or quality-efficiency. Include per-request lane scheduling only when it changes diffusion refinement/advancement dependency. Exclude new model/backbone architecture or training-only gains; general conditional layer/token skipping independent of the diffusion denoising process; external target-model draft verification (05); primary KV/cache management (07); primary kernel/runtime work (09); cross-request admission/batching/resource scheduling (11); sparse query-key computation (13); and methods whose primary evidence shows quality gains without inference-efficiency evidence.

### 含める研究

- masked位置のunmask/commit順序と同時更新幅の制御
- denoising round/NFE予算の適応的配分
- diffusion refinement/advancementを分離する単一request内の依存制御
- denoising軌道の探索・remask・剪定による品質対計算量改善

### 含めない研究

- 一般model/backbone設計、training-only、効率評価のない品質改善
- 通常の入力token/layer skipping04、外部target-modelによるdraft verification05
- 主貢献がKV/cache07またはkernel/runtime09の研究
- cross-request admission/batching/resource scheduling11、sparse query-key13

## 近傍系統

- [04-conditional-computation](../04-conditional-computation/)
- [05-speculative-decoding-moe](../05-speculative-decoding-moe/)
- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（11本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/22-diffusion-decoding-efficiency/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2025-12 · [Learning Unmasking Policies for Diffusion Language Models](2025-2512.09106-learning-unmasking-policies-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/apple/ml-rl-dllm) ・ リポジトリ内被引用：3  
  拡散言語モデル（diffusion language モデル）は、左から右へ一語ずつ出力する自己回帰型モデルと異なり、未確定位置をマスクした系列全体を繰り返し予測し、複数位置を同じ前向き計算で確定できる。

- **2026-04 · [Dependency-Guided Parallel Decoding in Discrete Diffusion Language Models](2026-2604.02560-dependency-guided-parallel-decoding-in-discrete-diffusion-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  依存推定は拡散モデルの1回の前向き計算で得た状態を利用し、正確な依存行列を作るためにマスク位置ごとに追加推論する方式を避ける。

- **2026-03 · [DAPD: Dependency-Aware Parallel Decoding via Attention for Diffusion LLMs](2026-2603.12996-dapd-dependency-aware-parallel-decoding-via-attention-for-diffusion-llms.md)**  
  実装：[✓](https://github.com/quasar529/DAPD) ・ リポジトリ内被引用：2  
  またLLaDAの主表では比較方式とDAPDのブロック構成が異なるため、速度差の全てを位置選択アルゴリズム単独の効果とみなせない。

- **2025-12 · [LoPA: Scaling dLLM Inference via Lookahead Parallel Decoding](2025-2512.16229-lopa-scaling-dllm-inference-via-lookahead-parallel-decoding.md)**  
  実装：[✓](https://github.com/SJTU-DENG-Lab/LoPA) ・ リポジトリ内被引用：2  
  しかし実際には、確信度が閾値を超える位置だけを確定する方式では、難しい位置が残ってしまい、1回当たり1〜3トークン程度しか進まない場合が多い。

- **2026-08 · [Speculative Correction: Draft-then-Refine Decoding for Diffusion Language Models](2026-2608.02625-speculative-correction-draft-then-refine-decoding-for-diffusion-language.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的 Correctionは、拡散言語モデル（Diffusion Language モデル、DLM）が持つ双方向の修正能力を、実際の文章生成へ生かすための二段階復号方式である。flash–flashではGSM8Kの正答率を0.848から0.899へ改善し、同じ問題集合のモデル実行時間を18.77秒から15.96秒へ短縮した。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-09 · [Early-Bird Decoding: Accelerating Diffusion LLMs with Learnable Block Sizes and Parallel Sampling](2026-2609.16450-early-bird-decoding-accelerating-diffusion-llms-with-learnable-block-siz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型大規模言語モデル（diffusion LLM、dLLM）は、未確定位置をマスクした系列に対し、双方向Transformerで各位置の語彙分布を同時に予測し、確信できる位置を確定して再び推論する。

- **2026-06 · [AsyncLane: Decoupling Refinement from Advancement in Diffusion Language Model Decoding](2026-2606.08411-asynclane-decoupling-refinement-from-advancement-in-diffusion-language-m.md)**  
  実装：[✓](https://github.com/renyingxuan/AsyncLane) ・ リポジトリ内被引用：0  
  AsyncLaneは、マスク拡散言語モデル（diffusion language モデル、DLM）のブロック単位生成に存在するブロック完了待ちを緩和する、再学習不要の復号スケジューラである。単一H100・バッチ1でLLaDAとDreamを対象に評価した結果、数学的推論とコード生成のすべての報告した長さ設定で比較方式中の最大TPSを示した。

- **2026-02 · [Prism: Efficient Test-Time Scaling via Hierarchical Search and Self-Verification for Discrete Diffusion Language Models](2026-2602.01842-prism-efficient-test-time-scaling-via-hierarchical-search-and-self-verif.md)**  
  実装：[✓](https://github.com/viiika/Prism) ・ リポジトリ内被引用：0  
  Prismは、階層的軌跡探索（Hierarchical Trajectory Search; HTS）、部分再マスクによる局所分岐（Local Branching via Partial Remasking）、自己検証フィードバック（Self-Verified Feedback; SVF）を統合する。

### 2年前（2024-12〜2025-11）

- **2025-06 · [Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles](2025-2506.10848-accelerating-diffusion-large-language-models-with-slowfast-sampling-the-three-golden-principles.md)**  
  実装：[✓](https://github.com/LiangrunFlora/Slow-Fast-Sampling) ・ リポジトリ内被引用：17  
  単独の信頼度閾値だけではなく、連続区間の終端が最近の複数反復で安定したかを検査し、探索段階（Slow）から高速段階（Fast）へ切り替える。原著図2のGPQA・8-shot・生成長1024という特定条件では、LLaDAの通常復号が1.60トークン/秒、SlowFast単独が25.00トークン/秒で15.63倍となる。

- **2025-11 · [From Bits to Rounds: Parallel Decoding with Exploration for Diffusion Language Models](2025-2511.21103-from-bits-to-rounds-parallel-decoding-with-exploration-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  通常の自己回帰モデルとは異なり、左から一語ずつ確定する必要がないため、並列復号によって生成の反復回数を減らせる可能性がある。実験ではGSM8K、MATH、HumanEval、MMLU-Proを対象に、同程度の正答率で必要なモデル順伝播回数を26〜61%削減する代表結果を示す。

- **2025-11 · [Beyond Confidence: Adaptive and Coherent Decoding for Diffusion Language Models](2025-2512.02044-beyond-confidence-adaptive-and-coherent-decoding-for-diffusion-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、整合的文脈復号（coherent contextual デコード; CCD）を提案する。ステップ数の比は3.48倍で、得点差は3.91ポイントである。
<!-- survey:auto:end -->
