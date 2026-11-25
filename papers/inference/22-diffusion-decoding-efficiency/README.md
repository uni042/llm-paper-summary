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
## 自動生成の論文一覧（44本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/22-diffusion-decoding-efficiency/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2025-12 · [Learning Unmasking Policies for Diffusion Language Models](2025-2512.09106-learning-unmasking-policies-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/apple/ml-rl-dllm) ・ リポジトリ内被引用：9  
  拡散言語モデル（diffusion language モデル）は、左から右へ一語ずつ出力する自己回帰型モデルと異なり、未確定位置をマスクした系列全体を繰り返し予測し、複数位置を同じ前向き計算で確定できる。

- **2026-03 · [DAPD: Dependency-Aware Parallel Decoding via Attention for Diffusion LLMs](2026-2603.12996-dapd-dependency-aware-parallel-decoding-via-attention-for-diffusion-llms.md)**  
  実装：[✓](https://github.com/quasar529/DAPD) ・ リポジトリ内被引用：8  
  またLLaDAの主表では比較方式とDAPDのブロック構成が異なるため、速度差の全てを位置選択アルゴリズム単独の効果とみなせない。

- **2026-04 · [Dependency-Guided Parallel Decoding in Discrete Diffusion Language Models](2026-2604.02560-dependency-guided-parallel-decoding-in-discrete-diffusion-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  依存推定は拡散モデルの1回の前向き計算で得た状態を利用し、正確な依存行列を作るためにマスク位置ごとに追加推論する方式を避ける。

- **2025-12 · [LoPA: Scaling dLLM Inference via Lookahead Parallel Decoding](2025-2512.16229-lopa-scaling-dllm-inference-via-lookahead-parallel-decoding.md)**  
  実装：[✓](https://github.com/SJTU-DENG-Lab/LoPA) ・ リポジトリ内被引用：6  
  しかし実際には、確信度が閾値を超える位置だけを確定する方式では、難しい位置が残ってしまい、1回当たり1〜3トークン程度しか進まない場合が多い。

- **2026-02 · [Swordsman: Entropy-Driven Adaptive Block Partition for Efficient Diffusion Language Models](2026-2602.04399-swordsman-entropy-driven-adaptive-block-partition-for-efficient-diffusio.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  Swordsmanは、拡散言語モデル（Diffusion Language モデル、DLM）の生成速度と品質を改善するため、出力列を固定長で区切るブロック復号を、モデルの予測エントロピーに応じて動的に区切る方式へ変更する。

- **2026-06 · [Mean-Field Parallel Decoding for Discrete Diffusion Language Models](2026-2606.15805-mean-field-parallel-decoding-for-discrete-diffusion-language-models.md)**  
  実装：[✓](https://github.com/AmeenAli/MDP) ・ リポジトリ内被引用：2  
  予測分布どうしの重なりで同時確定の衝突を抑える平均場の選択規則により、離散拡散モデルの並列復号をエントロピー基準比で平均5.12倍まで速め、正解率の低下を小さく抑えた。

- **2026-04 · [R2-dLLM: Accelerating Diffusion Large Language Models via Spatio-Temporal Redundancy Reduction](2026-2604.18995-r2-dllm-accelerating-diffusion-large-language-models-via-spatio-temporal.md)**  
  実装：[✓](https://github.com/GATECH-EIC/R2-dLLM) ・ リポジトリ内被引用：2  
  拡散型モデルの復号に残る空間と時間の冗長さを、塊ごとの一括確定と安定トークンの早期確定、さらに冗長さの小さい軌跡での微調整で削り、歩数を最大88パーセント減らした。

- **2026-02 · [Search or Accelerate: Confidence-Switched Position Beam Search for Diffusion Language Models](2026-2602.10953-search-or-accelerate-confidence-switched-position-beam-search-for-diffus.md)**  
  実装：[✓](https://github.com/duterscmy/SOAR) ・ リポジトリ内被引用：2  
  拡散言語モデルのマスク解除順序を位置空間で探索し、信頼度が高いステップでは並列確定へ畳む切替型復号で、正解率を貪欲復号より上げながら1.4から1.6倍の高速化を両立した。

- **2026-08 · [Speculative Correction: Draft-then-Refine Decoding for Diffusion Language Models](2026-2608.02625-speculative-correction-draft-then-refine-decoding-for-diffusion-language.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的 Correctionは、拡散言語モデル（Diffusion Language モデル、DLM）が持つ双方向の修正能力を、実際の文章生成へ生かすための二段階復号方式である。flash–flashではGSM8Kの正答率を0.848から0.899へ改善し、同じ問題集合のモデル実行時間を18.77秒から15.96秒へ短縮した。

- **2026-06 · [Multi-Token Residual Prediction](2026-2605.18817-multi-token-residual-prediction.md)**  
  実装：[✓](https://github.com/heavyball-research/multi-token-residual-prediction) ・ リポジトリ内被引用：1  
  拡散言語モデルは、マスクされたトークン列を何度も予測し直して文章を生成する。品質を維持する静的ノイズ除去では、MRPが複数トークンを先行提案し、大型モデルが検証することで1.17〜1.40倍のスループット改善を得る。

- **2026-05 · [Efficient Diffusion LLMs via Temporal-Spatial Parallel Decoding and Confidence Extrapolation](2026-2605.30753-efficient-diffusion-llms-via-temporal-spatial-parallel-decoding-and-conf.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己回帰型モデルは基本的に次の一語を順番に生成するのに対し、マスク型dLLMは多数の未確定位置を同時に予測し、確信度の低い位置を再びマスクして次の反復で修正する。

- **2026-04 · [STDec: Spatio-Temporal Stability Guided Decoding for dLLMs](2026-2604.06330-stdec-spatio-temporal-stability-guided-decoding-for-dllms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散言語モデルの確定済み近傍と予測識別子の跨ステップ一貫性から位置ごとの閾値を動的に作る学習不要のデコードで、LLaDAのMBPPで14.17倍まで高速化しながらスコアをほぼ保った。

- **2026-04 · [Breaking Block Boundaries: Anchor-based History-stable Decoding for Diffusion Large Language Models](2026-2604.08964-breaking-block-boundaries-anchor-based-history-stable-decoding-for-diffu.md)**  
  実装：[✓](https://github.com/zs1314/AHD) ・ リポジトリ内被引用：1  
  履歴バッファと動的アンカーでトークンの安定化の軌跡を捉え、安定したトークンをブロック境界を越えて早期確定することで、拡散言語モデルのデコードステップ削減と性能向上を両立する学習不要の方式。

- **2026-03 · [Attention-Based Sampler for Diffusion Language Models](2026-2604.08564-attention-based-sampler-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、マスク拡散型大規模言語モデル（dLLM）の生成時に、どの位置のマスクを先に確定するかを注意行列から決める学習不要の復号法Attn-Samplerを提案する。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-10 · [TIPS: A Tiny Inference-time Policy for Scaling in Diffusion Language Models](2026-2610.22099-tips-a-tiny-inference-time-policy-for-scaling-in-diffusion-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルのデコードで、どのトークンを見せ、どのトークンを再び隠すかを、デコーダ凍結のまま約60万パラメータの方策が学習して決める方式を提案し、呼出し32回で最強の比較対象を12ポイント上回る正解率を示した研究。

- **2026-09 · [Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation](2026-2609.37924-time-anchored-diffusion-language-models-latent-space-caching-for-fast-ge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの潜在表現が近傍の拡散時刻で再利用できる性質を使い、高価なアンカーネットワークの出力をキャッシュして軽いデノイザーと融合する潜在空間キャッシングで、DiffusionGemmaのスループットを最大1.79倍にし、事前学習版では層計算を最大38%削減する研究。

- **2026-09 · [From Position Risks to Block Survival: Faster Generation for Diffusion Language Models](2026-2609.33390-from-position-risks-to-block-survival-faster-generation-for-diffusion-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデル（DLM）は複数の将来トークンを並列に提案できるため、自己回帰生成より少ないモデル評価回数で長い出力を作れる可能性がある。arXiv:2609.33390の原著ではI-DLM 8B/32Bを対象に、H200上の18条件で同規模I-DLM比の生成スループットを8Bで幾何平均22.7%、32Bで29.8%改善する。

- **2026-09 · [Fork-dLLM: Avoiding the Flexibility Trap in Diffusion Language Models](2026-2609.39859-fork-dllm-avoiding-the-flexibility-trap-in-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの信頼度型サンプラが分岐位置を後回しにして多様性を失う問題に対し、不確かなフォールバックステップでのみ左端確定の自己回帰順序へ切り替える混成サンプラで、自己回帰型と同等のpass@kを2〜3倍少ないモデル評価で達成し、同じ原理をGRPO後学習にも広げる研究。

- **2026-09 · [Early-Bird Decoding: Accelerating Diffusion LLMs with Learnable Block Sizes and Parallel Sampling](2026-2609.16450-early-bird-decoding-accelerating-diffusion-llms-with-learnable-block-siz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型大規模言語モデル（diffusion LLM、dLLM）は、未確定位置をマスクした系列に対し、双方向Transformerで各位置の語彙分布を同時に予測し、確信できる位置を確定して再び推論する。

- **2026-07 · [Towards Efficient and Effective Diffusion Language Model Inference via Semantic-Aware Adaptive Denoising](2026-e69ef400b29d-towards-efficient-and-effective-diffusion-language-model-inference-via-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの無駄な再計算を、固定しきい値ではなく直近3ステップの信頼度軌跡のクラスタリングで意味的に安定したトークンを検出して凍結することで削り、品質を保ちながら短文脈で平均約4倍、長文脈で平均41倍高速化する方式Ada-DLM。

- **2026-07 · [CORA-Diff: Confidence-Oriented Residual Acceptance for Efficient Diffusion Language Model Inference](2026-2608.11235-cora-diff-confidence-oriented-residual-acceptance-for-efficient-diffusio.md)**  
  実装：[✓](https://github.com/wyffffff/cora-diff-llada) ・ リポジトリ内被引用：0  
  拡散言語モデルの未確定位置を信頼度と持続性だけで早期確定しブロックを早く終える学習なしの規則を提案し、全条件最速と配備条件で2.70から3.32倍の高速化を示した。

- **2026-07 · [Commit Locally, Exit Globally: Coordinating Adaptive Sampling and Early Exit in Diffusion Language Models](2026-2607.28166-commit-locally-exit-globally-coordinating-adaptive-sampling-and-early-ex.md)**  
  実装：[✓](https://ming053l.github.io/c4-dllm.github.io/) ・ リポジトリ内被引用：0  
  拡散言語モデルの局所確定加速と大域早期終了を、改訂履歴に適応する停止規則で協調させる学習不要の枠組み。ステップを最大95パーセント削り、実測で最大18.6倍高速化する。

- **2026-06 · [Walk fast but be careful: Understanding Parallel Sampling in Masked Diffusion](2026-2606.22976-walk-fast-but-be-careful-understanding-parallel-sampling-in-masked-diffu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  グラフ上のランダムウォークで並列開示の誤差を条件付き依存として分離測定し、エントロピー基準が構造依存で一様に最適でないことを示した上で、分離子を開示する二分サンプラーで対数ステップの厳密な並列生成を実現するマスク拡散の研究。

- **2026-06 · [AsyncLane: Decoupling Refinement from Advancement in Diffusion Language Model Decoding](2026-2606.08411-asynclane-decoupling-refinement-from-advancement-in-diffusion-language-m.md)**  
  実装：[✓](https://github.com/renyingxuan/AsyncLane) ・ リポジトリ内被引用：0  
  AsyncLaneは、マスク拡散言語モデル（diffusion language モデル、DLM）のブロック単位生成に存在するブロック完了待ちを緩和する、再学習不要の復号スケジューラである。単一H100・バッチ1でLLaDAとDreamを対象に評価した結果、数学的推論とコード生成のすべての報告した長さ設定で比較方式中の最大TPSを示した。

- **2026-05 · [Roll Out and Roll Back: Diffusion LLMs are Their Own Efficiency Teachers](2026-2605.16941-roll-out-and-roll-back-diffusion-llms-are-their-own-efficiency-teachers.md)**  
  実装：[✓](https://github.com/Feng-Hong/WINO-DLLM/tree/WINO-plus) ・ リポジトリ内被引用：0  
  拡散言語モデルの並列デコードを取り消し可能にし、検証で得た確定順序を学習へ戻すことで、GSM8Kで正解率を上げながらデコードステップを約7分の1へ減らす二段の効率化。

- **2026-05 · [LEAP: Unlocking dLLM Parallelism via Lookahead Early-Convergence Token Detection](2026-2605.10980-leap-unlocking-dllm-parallelism-via-lookahead-early-convergence-token-de.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルで、将来文脈の候補による摂動前後で予測が変わらないトークンを早期収束として検出し、信頼度閾値未満の中信頼度トークンまで安全に並列確定することでステップ数と遅延を減らした学習不要の手法。

- **2026-05 · [Cluster-Level Attention-Guided Parallel Decoding for Masked Diffusion Language Models](2026-2605.29607-cluster-level-attention-guided-parallel-decoding-for-masked-diffusion-la.md)**  
  実装：[✓](https://github.com/ziyigu2004/CLAD) ・ リポジトリ内被引用：0  
  マスク拡散言語モデルの確定単位を1トークンから高信頼度の連続区間へ広げ、注意由来の衝突グラフで両立する区間だけを並列確定することで、標準デコード比最大8.47倍の高速化と精度維持を両立する学習不要デコーダ。

- **2026-05 · [BlockBatch: Multi-Scale Consensus Decoding for Efficient Diffusion Language Model Inference](2026-2605.29233-blockbatch-multi-scale-consensus-decoding-for-efficient-diffusion-langua.md)**  
  実装：[✓](https://github.com/Laurence-Wu/BlockBatch) ・ リポジトリ内被引用：0  
  局所更新で古くなったKVキャッシュは定期的な全系列再計算で補正する。学習済みモデルの重みを変更しない推論時方式である。著者はLLaDA系2モデルとDream系1モデル、算数・数学・コード生成の4課題を用い、Fast-dLLMの二重キャッシュ方式と比較して、モデル呼出し回数（NFE）を平均26.6%削減し、実測生成時間を平均1.33倍高速化したと報告する。

- **2026-04 · [Stability-Weighted Decoding for Diffusion Language Models](2026-2604.17068-stability-weighted-decoding-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連続ステップ間の予測の揺れでトークンの確定を遅らせる学習不要の調整器により、拡散言語モデルの並列復号で正解率を大きく上げながら関数評価回数も減らした。

- **2026-04 · [NI Sampling: Accelerating Discrete Diffusion Sampling by Token Order Optimization](2026-2604.18471-ni-sampling-accelerating-discrete-diffusion-sampling-by-token-order-opti.md)**  
  実装：[✓](https://github.com/imagination-research/NI-Sampling) ・ リポジトリ内被引用：0  
  そのため従来の全段階方式は一回のモデル実行で一位置だけを確定し、長さ512の出力では原則512回の推論が必要となる。ICLR 2026の論文に記載された単一GPU評価では、LLaDA-8B-InstructのMBPP、生成長512で全段階方式19.1トークン/秒に対し273.8トークン/秒（14.3倍）を報告する。

- **2026-04 · [Early Decisions Matter: Proximity Bias and Initial Trajectory Shaping in Non-Autoregressive Diffusion Language Models](2026-2604.10567-early-decisions-matter-proximity-bias-and-initial-trajectory-shaping-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの完全非自己回帰デコードで、文末トークンの早期選択と隣接位置への信頼度伝播という近接バイアスが生成を崩すことを示し、初回ステップだけに軽量プランナーと文末トークンの温度アニーリングで介入して推論タスク精度を改善した研究。

- **2026-04 · [DepCap: Adaptive Block-Wise Parallel Decoding for Efficient Diffusion LM Inference](2026-2604.15750-depcap-adaptive-block-wise-parallel-decoding-for-efficient-diffusion-lm-.md)**  
  実装：[✓](https://github.com/X-Xia0828/DepCap) ・ リポジトリ内被引用：0  
  DepCapは、拡散言語モデル（DLM）が文章をブロック単位で生成する際の二つの判断、すなわち「次のブロックをどこまで伸ばすか」と「そのブロック内のどの位置を同時に確定するか」を、異なる予測信号から決める学習不要の推論方式である。

- **2026-03 · [Progressive Refinement Regulation for Accelerating Diffusion Language Model Decoding](2026-2603.04514-progressive-refinement-regulation-for-accelerating-diffusion-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散デコードの軌跡から作った収束進捗を軽量コントローラに予測させ、トークンごとの温度整形で前方計算回数を減らす制御手法。

- **2026-03 · [Locally Coherent Parallel Decoding in Diffusion Language Models](2026-2603.20216-locally-coherent-parallel-decoding-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/IBM/coherent-diffusion-local-autoregression) ・ リポジトリ内被引用：0  
  マスク拡散型の言語モデル（DLM）は、未確定トークンを一度に複数予測して反復的に確定できる。Dream-Coder-Instruct-7BとQwen3-0.6Bの組合せでは、HumanEvalのコード抽出失敗率が、1反復に8トークン確定する条件で基準DLMの70%からCoDiLAの16%へ低下した。

- **2026-03 · [Beyond Scattered Acceptance: Fast and Coherent Inference for DLMs via Longest Stable Prefixes](2026-2603.05454-beyond-scattered-acceptance-fast-and-coherent-inference-for-dlms-via-lon.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルで飛び飛びの確定をやめ、候補の差で測った安定さが続く最長の連続接頭辞だけを区切りへ吸着させて一度に確定する方式で、最大三・四倍の高速化と成績の維持を両立したと報告した。

- **2026-02 · [Prism: Efficient Test-Time Scaling via Hierarchical Search and Self-Verification for Discrete Diffusion Language Models](2026-2602.01842-prism-efficient-test-time-scaling-via-hierarchical-search-and-self-verif.md)**  
  実装：[✓](https://github.com/viiika/Prism) ・ リポジトリ内被引用：0  
  Prismは、階層的軌跡探索（Hierarchical Trajectory Search; HTS）、部分再マスクによる局所分岐（Local Branching via Partial Remasking）、自己検証フィードバック（Self-Verified Feedback; SVF）を統合する。

- **2026-01 · [Plan, Verify and Fill: A Structured Parallel Decoding Approach for Diffusion Language Models](2026-2601.12247-plan-verify-and-fill-a-structured-parallel-decoding-approach-for-diffusi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルで構造的な計画トークンを検証付きで先に確定し、詰まれば自己回帰的な穴埋めへ切り替える学習不要の復号で、前向き計算回数を最大65パーセント削減した。

- **2026-01 · [dLLM-ASR: A Faster Diffusion LLM-based Framework for Speech Recognition](2026-2601.17902-dllm-asr-a-faster-diffusion-llm-based-framework-for-speech-recognition.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CTCの事前認識で拡散デコーダの開始点と生成長を与え、パディングの早期除去と信頼度によるトークン単位の早期退出で、音声認識の拡散デコードの冗長計算を削る枠組み。

### 2年前（2024-12〜2025-11）

- **2025-08 · [Diffusion LLMs Can Do Faster-Than-AR Inference via Discrete Diffusion Forcing](2025-2508.09192-diffusion-llms-can-do-faster-than-ar-inference-via-discrete-diffusion-fo.md)**  
  実装：[✓](https://github.com/zhijie-group/Discrete-Diffusion-Forcing) ・ リポジトリ内被引用：39  
  離散拡散型の大規模言語モデル（diffusion LLM、dLLM）は、マスクされた複数トークンを一度の推論で同時に予測できる。しかし従来の双方向注意を使う拡散モデルでは、マスクの状態が反復ごとに変わるため、過去の鍵・値（KV）を自己回帰型モデルのように正確にキャッシュしにくい。確定済みのブロックのKVは変更されないため正確に再利用できる。

- **2025-06 · [Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles](2025-2506.10848-accelerating-diffusion-large-language-models-with-slowfast-sampling-the-three-golden-principles.md)**  
  実装：[✓](https://github.com/LiangrunFlora/Slow-Fast-Sampling) ・ リポジトリ内被引用：30  
  単独の信頼度閾値だけではなく、連続区間の終端が最近の複数反復で安定したかを検査し、探索段階（Slow）から高速段階（Fast）へ切り替える。原著図2のGPQA・8-shot・生成長1024という特定条件では、LLaDAの通常復号が1.60トークン/秒、SlowFast単独が25.00トークン/秒で15.63倍となる。

- **2025-10 · [dInfer: An Efficient Inference Framework for Diffusion Language Models](2025-2510.08666-dinfer-an-efficient-inference-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/inclusionAI/dInfer) ・ リポジトリ内被引用：23  
  拡散型LLM（dLLM）の反復的な雑音除去（denoising）・並列トークン確定・更新され続けるKVをモジュール化し、デコーダ/KV管理とGPU実行系を同時最適化するdInfer。

- **2025-09 · [Learning to Parallel: Accelerating Diffusion Large Language Models via Learnable Parallel Decoding](2025-2509.25188-learning-to-parallel-accelerating-diffusion-large-language-models-via-le.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  これに対してマスク型拡散言語モデルは、あるブロック内の複数トークンを一度に予測し、まだ不確かな位置だけを再びマスクして次の反復で更新する。

- **2025-11 · [From Bits to Rounds: Parallel Decoding with Exploration for Diffusion Language Models](2025-2511.21103-from-bits-to-rounds-parallel-decoding-with-exploration-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  通常の自己回帰モデルとは異なり、左から一語ずつ確定する必要がないため、並列復号によって生成の反復回数を減らせる可能性がある。実験ではGSM8K、MATH、HumanEval、MMLU-Proを対象に、同程度の正答率で必要なモデル順伝播回数を26〜61%削減する代表結果を示す。

- **2025-11 · [Beyond Confidence: Adaptive and Coherent Decoding for Diffusion Language Models](2025-2512.02044-beyond-confidence-adaptive-and-coherent-decoding-for-diffusion-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本論文は、整合的文脈復号（coherent contextual デコード; CCD）を提案する。ステップ数の比は3.48倍で、得点差は3.91ポイントである。
<!-- survey:auto:end -->
