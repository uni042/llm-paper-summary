# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（160本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [DFlash: Block Diffusion for Flash Speculative Decoding](2026-2602.06036-dflash-block-diffusion-for-flash-speculative-decoding.md)**  
  実装：[✓](https://github.com/z-lab/dflash) ・ リポジトリ内被引用：41  
  対象 隠れ featuresで条件付けしたblock-diffusion drafterが候補列を1回で並列生成し、投機ドラフト自身の逐次待ちを除くDFlash。

- **2026-07 · [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](2026-2607.05147-dspark-confidence-scheduled-speculative-decoding.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSpec) ・ リポジトリ内被引用：16  
  並列ドラフトの後半受理率低下を軽量な逐次ヘッドで抑え、較正した接頭辞生存確率と実機処理能力から検証長を負荷適応で配分し、実トラフィックで同等処理能力時のユーザー当たり生成速度を57〜85%改善する。

- **2026-04 · [Accelerating Speculative Decoding with Block Diffusion Draft Trees](2026-2604.12989-accelerating-speculative-decoding-with-block-diffusion-draft-trees.md)**  
  実装：[✓](https://github.com/liranringel/ddtree) ・ リポジトリ内被引用：14  
  DFlashが1回で得た位置別確率分布から高確率な複数接頭辞をDDTreeとして組み、1回の対象モデル検証で複数経路を試して単一路径投機より受理長と速度を高める。

- **2026-05 · [Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding](2026-2605.29707-domino-speculative-decoding.md)**  
  実装：[✓](https://github.com/jianuo-huang/Domino) ・ リポジトリ内被引用：13  
  並列ドラフトが弱めるトークン間の依存を、軽量GRUと低ランク補正で戻す投機的デコード方式。Qwen3評価では受理長と生成速度を改善したが、要旨の最大5.8倍は本文表の条件と対応づけられない。

- **2025-11 · [SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding](2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-de.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  投機的復号は、小さなドラフターが先のトークンを提案し、大きな検証器が複数位置をまとめて評価することで自己回帰生成の待ち時間を減らす。Qwen2.5-72BのHumanEvalでは通常復号比で最大5.51倍、70B級の複数課題ではおおむね約4倍の速度改善を報告する。

- **2026-01 · [TALON: Confidence-Aware Speculative Decoding with Adaptive Token Trees](2026-2601.07353-talon-confidence-aware-speculative-decoding-with-adaptive-draft-length.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  投機木の形をあらかじめ「幅10・深さ8」のように固定すると、簡単な箇所では深さが足りず、難しい箇所では大量の枝を作って捨てる。TALONは総ノード数だけを固定し、ドラフトモデルの確信度に応じて予算を深さと幅へその場で配分する。

- **2025-11 · [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  MoE-SpeQは、対象MoEの4ビット版を下書きにして候補トークンと専門家経路を先に予測し、必要重みを検証前に読み込み、圧縮カーネルで転送と計算の待ちを減らす。

- **2026-02 · [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoE-Specは、候補木全体のルータ確率を層ごとに合算して専門家を予算B個へ絞り、各枝をその集合内で再選択して、木の拡大による検証重み読出しを抑える。

- **2026-05 · [D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting](2026-2605.18810-d-pace.md)**  
  実装：[✓](https://github.com/Lucas-TY/D-PACE) ・ リポジトリ内被引用：7  
  並列投機ドラフタで、受理接頭辞長への位置別寄与から交差エントロピー重みを毎例動的に計算し、固定位置減衰より受理長と実測高速化を改善する。

- **2026-05 · [ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios](2026-2604.09603-echo.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  高同時実行時の投機的デコードを固定検証予算の配分問題として扱い、信頼度の高い深さだけで候補木を伸縮し、バッチ内要求間で予算を再配分するSGLang統合方式。

- **2025-12 · [Speculative Decoding: Performance or Illusion?](2026-2601.11580-speculative-decoding-performance-or-illusion.md)**  
  実装：[✓](https://github.com/orgs/SpecDecode-Bench/repositories) ・ リポジトリ内被引用：6  
  実運用向けvLLMで主要投機的復号を横断評価し、検証支配・バッチ依存・受理変動と理論上限との差を定量化。

- **2025-11 · [DSD: A Distributed Speculative Decoding Solution for Edge-Cloud Agile Large Model Serving](2025-2511.21669-dsd-distributed-edge-cloud-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  端末側下書きモデルとクラウド側目標モデルによる分散投機的復号をDSD-Simでモデル化し、学習型の適応窓制御で投機窓幅を調整して処理量を最大9.7%向上する。

- **2026-06 · [TreeFlash: Parallel AR-Approximation for Faster Speculative Decoding](2026-2606.03819-treeflash-parallel-ar-approximation-for-faster-speculative-decoding.md)**  
  実装：[✓](https://github.com/ETH-DISCO/TreeFlash) ・ リポジトリ内被引用：4  
  投機的復号（投機的復号）は、軽量なドラフター（drafter）が複数の候補トークンを先に提案し、重い対象モデル（対象モデル）がまとめて検証することで、対象モデルの逐次呼び出し回数を減らす。

- **2026-06 · [DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding](2026-2606.02091-dflare.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：4  
  ブロック拡散ドラフトの各層へ異なる標的層混合を注入し、ドラフト深さ・標的知識・学習データを拡張して受理長と実時間高速化を伸ばす。

- **2026-05 · [Draft Less, Retrieve More: Hybrid Tree Construction for Speculative Decoding](2026-2605.20104-draft-less-retrieve-more-hybrid-tree-construction-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  動的剪定は投機木を速くするが、剪定した枝の中に本来受理できる候補があれば平均受理長が落ちる。Graftは剪定で空いた候補枠を捨てず、対象モデルの過去検証から得た安価な検索候補で「接ぎ木」する。対象モデルが一度に検証するノード総数は増やさず、ドラフト計算だけを安い検索へ置換する。

- **2026-04 · [Self-Speculative Decoding for On-device MoE Acceleration](2025-self-speculative-decoding-for-on-device-moe-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  少数の経路選択専門家だけで同じMoE自身をドラフト化し、GPUを専門家キャッシュとして生成・検証間で再利用することで、CPU退避を伴う端末MoE復号を最大3.72倍高速化する。

- **2026-02 · [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)**  
  実装：[✓](https://github.com/lshAlgorithm/MoE-SpAc) ・ リポジトリ内被引用：4  
  MoE-SpAcは、投機的復号で先に見える専門家需要を集計し、VRAMに残す専門家・先読みする重み・CPUで計算する専門家を制約付きで同時に配置して、端末の転送待ちを減らす。

- **2026-06 · [JetSpec: Breaking the Scaling Ceiling of Speculative Decoding with Parallel Tree Drafting](2026-2606.18394-jetspec-breaking-the-scaling-ceiling-of-speculative-decoding-with-parall.md)**  
  実装：[✓](https://github.com/hao-ai-lab/JetSpec) ・ リポジトリ内被引用：3  
  自己回帰型言語モデルは次トークンを逐次生成するため、出力長が伸びるほど復号遅延が蓄積する。投機的復号は小さなドラフト器が複数トークンを提案し、対象モデルがまとめて検証することで対象モデルの逐次順伝播回数を減らす。木予算256、貪欲復号設定のMATH-500では自己回帰復号比9.64倍、平均受理長10.76を報告する。

- **2026-02 · [SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding](2026-2604.09557-speed-bench-speculative-decoding-benchmark.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号を意味多様性・入力長・エントロピー・並列度の軸で統一評価し、合成入力の平均23%過大評価やバッチ依存の最適ドラフト長など、従来ベンチマークの順位偏りを明らかにする。

- **2026-07 · [D-cut: Adaptive Verification Depth Pruning for Batched Speculative Decoding](2026-2607.14647-d-cut-adaptive-verification-depth-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号は小さなドラフト器が複数トークンを先に提案し、大きな対象モデルがまとめて検証することで逐次実行回数を減らす。高並行条件では長ドラフト基準の自己回帰復号比平均高速化率1.26倍を1.65倍へ引き上げ、30個のモデル・課題組合せ中29個で改善した。

- **2026-07 · [AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding](2026-2607.25852-angelspec.md)**  
  実装：[✓](https://github.com/Tencent/AngelSpec) ・ リポジトリ内被引用：2  
  会話には短い多トークン予測、コード・数学には並列草稿DFlyを使い分け、実行時負荷に応じて検証深度も動的調整する推測デコード基盤。

- **2026-05 · [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)**  
  実装：[✓](https://github.com/sgl-project/sglang/pull/22272) ・ リポジトリ内被引用：2  
  SPECTREは、余った小型モデルGPUを遠隔下書き器として大型モデルの検証に再利用し、下書きと検証を直列・並列の間で切り替えて、通信待ちとロールバックを抑える。

- **2026-05 · [SpecBlock: Block-Iterative Speculative Decoding with Dynamic Tree Drafting](2026-2605.07243-specblock-block-iterative-speculative-decoding-with-dynamic-tree-draftin.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は小型の草稿モデルが複数の候補トークンを先に提案し、目標モデルがそれらを一度の前向き計算で検証する。論文の主要な速度比較は、単一NVIDIA A100-80GB、バッチ1で行われた。

- **2026-05 · [PipeSD: An Efficient Cloud-Edge Collaborative Pipeline Inference Framework with Speculative Decoding](2026-2605.13319-pipesd.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号は小型モデルが複数トークンを先に提案し、大型モデルがまとめて検証することで自己回帰生成を高速化する。

- **2026-05 · [Draft-OPD: On-Policy Distillation for Speculative Draft Models](2026-2605.29343-draft-opd.md)**  
  実装：[✓](https://github.com/haodilei/Draft-OPD) ・ リポジトリ内被引用：2  
  投機的復号の検証で露出したドラフト誤り位置から提案を再生し、教師分布でオンポリシー蒸留することで受理長と無損失推論速度を高める。

- **2026-03 · [Speculative Speculative Decoding](2026-2603.03251-speculative-speculative-decoding.md)**  
  実装：[✓](https://github.com/tanishqkumar/ssd) ・ リポジトリ内被引用：2  
  検証中に受理長と補正トークンを複数予測し、その各結果に続く次ラウンドのドラフトを別GPUで先行生成することで、投機的デコードに残るドラフト待ちを隠す方式。

- **2026-02 · [Speculative Decoding with a Speculative Vocabulary](2026-2602.13836-speculative-decoding-with-a-speculative-vocabulary.md)**  
  実装：[✓](https://github.com/SamsungLabs/SpecVocab) ・ リポジトリ内被引用：2  
  SpecVocabは、投機的復号（投機的復号）の小型ドラフトモデルが次のトークンを予測する際、語彙全体への出力射影を行わず、文脈ごとに予測した候補語だけを精密計算する手法である。Qwen3 8BのSpec-Benchでは、再現したEAGLE-3の平均受理長4.78から5.01へ、平均スループット235.1から245.2トークン/秒へ改善した。

- **2026-01 · [WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching](2026-2601.11652-wisp-distributed-speculative-serving-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  WISPは、エッジで最初の棄却位置を予測して下書きを止め、サーバーでSLO余裕と検証時間から異種要求をバッチ分離し、無駄計算と干渉を減らす。

- **2025-12 · [Towards Efficient Agents: A Co-Design of Inference Architecture and System](2025-2512.18337-towards-efficient-agents-a-co-design-of-inference-architecture-and-syste.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AgentInferは、長い推論と外部ツール呼出しを繰り返すLLMエージェントの効率を、単一の生成呼出しのトークン/秒ではなく、目的を達成するまでの総所要時間・総トークン消費・タスク成功率で評価し、推論アーキテクチャと提供システムを共同設計する枠組みである。

- **2026-08 · [S2-MoE: Enabling Efficient Self-Speculative Decoding for Mixture-of-Experts on Edge Devices](2026-2608.15018-s2-moe-self-speculative-decoding-edge.md)**  
  実装：[✓](https://github.com/angerybob/S2-MoE) ・ リポジトリ内被引用：1  
  エッジ向けMoEで、専門家再利用を考慮した投機展開・ゲーティング・文脈共有を組み合わせ、専門家読み出しを抑えながら自己投機的復号を高速化する。

- **2026-07 · [SpecExtend: A Drop-in Enhancement for Speculative Decoding of Long Sequences](2026-specextend.md)**  
  実装：[✓](https://github.com/jycha98/SpecExtend) ・ リポジトリ内被引用：1  
  対象モデルの注意重みでドラフト側KVキャッシュの重要文脈を動的選択し、再学習なしで長文の投機的復号を高速化する拡張。

- **2026-07 · [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、軽量な下書きモデルが先のトークン候補を生成し、対象モデルが複数候補を一括検証することで、自己回帰生成の逐次的な待ち時間を減らす。対象モデルの検証規則は変更しないため、下書きの選び方を変えても、標準の投機的復号が持つ出力分布の保存を維持できる。

- **2026-07 · [HeteroSpec: Leveraging Contextual Heterogeneity for Efficient Speculative Decoding](2026-2505.13254-heterospec-leveraging-contextual-heterogeneity-for-efficient-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己回帰型の大規模言語モデルは出力トークンを逐次生成するため、出力が長くなると毎トークンの前向き計算が遅延を支配する。投機的復号（投機的復号）は、小さなドラフトモデルが先に複数トークンを予測し、大きなターゲットモデルがまとめて検証することで逐次計算回数を減らす。

- **2026-05 · [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一覧用要約：EVICTは混合専門家モデル（MoE）の木構造投機的復号で、下書き確率から見積もった期待確定トークン数を、事前測定した検証ステップ時間で割る効用を最大化するよう検証木の接頭部分を選び、不要な専門家起動を抑える。SGLangのCUDAグラフに統合し、出力分布を変えずに復号速度を改善する。

- **2026-05 · [FlexDraft: Flexible Speculative Decoding via Attention Tuning and Bonus-Guided Calibration](2026-2605.20022-flexdraft-flexible-speculative-decoding-via-attention-tuning-and-bonus-g.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlexDraftは、大規模言語モデル（LLM）の投機的復号（投機的復号）において、ドラフト生成と対象モデルの検証を重ねる並列方式と、確定結果を待ってからドラフトを生成する逐次方式を、バッチサイズに応じて使い分ける枠組みである。Qwen3-8BをA100で評価した原著表2の5タスク平均は、自己回帰生成に対して4.59倍の高速化となる。

- **2026-05 · [Component-Aware Self-Speculative Decoding in Hybrid Language Models](2026-2605.01106-component-aware-self-speculative-decoding-in-hybrid-language-models.md)**  
  実装：[✓](https://github.com/hecboar/hybrid-speculative-decoding) ・ リポジトリ内被引用：1  
  状態空間モデル（SSM）と通常の注意を組み合わせるハイブリッドLLMで、既存モデルの内部成分だけを候補生成器に使う自己投機的復号を検証する。並列構成Falcon-H1では候補2トークンの一括受理率0.680だが、逐次構成Qwen3.5では0.038に落ちる。

- **2026-04 · [WISV: Wireless-Informed Semantic Verification for Distributed Speculative Decoding in Device-Edge LLM Inference](2026-2604.17701-wisv-wireless-informed-semantic-verification-for-distributed-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  500 Mbps条件の比較では端から端までの推論遅延を最大31.4%削減する。本方式は近似的な意味受理である。Llama実機では通常方式80.4%に対しWISVは最低79.6%、Qwen実機では87.3%に対し最低86%となる条件がある。

- **2026-04 · [ToolSpec: Accelerating Tool Calling via Schema-Aware and Retrieval-Augmented Speculative Decoding](2026-2604.13519-toolspec-accelerating-tool-calling-via-schema-aware-and-retrieval-augmen.md)**  
  実装：[✓](https://github.com/hemingkx/ToolSpec) ・ リポジトリ内被引用：1  
  大規模言語モデルが検索や計算などの外部ツールを使う際には、ツール自体の処理だけでなく、関数名・引数名・引数値を含む呼び出し文字列を生成する時間もかかる。ToolBenchを用いたQwen2.5-14B-Instructの予備調査では、呼び出し文字列の生成が処理全体の遅延の約80%を占め、外部ツールの実行時間の約4倍だった。

- **2026-03 · [A Pipelined Collaborative Speculative Decoding Framework for Efficient Edge-Cloud LLM Inference](2026-2603.19133-picospec-edge-cloud-pipelined-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  端末の候補生成とクラウド検証を非同期に重ね、棄却用確率分布を疎圧縮してネットワーク往復を隠すことで、端末・クラウド協調推論を最大2.9倍高速化する。

- **2026-02 · [When RL Meets Adaptive Speculative Training: A Unified Training-Serving System](2026-2602.06932-aurora-adaptive-speculator-training-serving.md)**  
  実装：[✓](https://github.com/togethercomputer/aurora) ・ リポジトリ内被引用：1  
  実配信の採用・棄却トレースからドラフトモデルを非同期更新し、停止なしで重みを差し替える閉ループ型の投機的復号により、初日配備と分布変化への継続適応を実現する。

- **2026-02 · [PACER: Blockwise Pre-verification for Speculative Decoding with Adaptive Length](2026-2602.01274-pacer-blockwise-pre-verification-for-speculative-decoding-with-adaptive-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PACERは、投機的復号（投機的復号）において、小型の草稿モデルが何個の候補トークンを生成してから大型の目標モデルに検証を依頼するかを、復号の各段階で動的に決める方式である。Llama-2 7B/70BのHumanEvalでは自己回帰復号約9.1トークン/秒に対して24.2トークン/秒、すなわち2.66倍である。

- **2026-02 · [HSD: Training-Free Acceleration for Document Parsing Vision-Language Models with Hierarchical Speculative Decoding](2026-2602.12957-hsd-training-free-acceleration-for-document-parsing-vision-language-mode.md)**  
  実装：[✓](https://github.com/whlscut/HSD) ・ リポジトリ内被引用：1  
  文書画像をMarkdownや構造化テキストへ変換する視覚言語モデルは、表・数式・本文・読順を一貫して扱えるが、長いページの結果を自己回帰的に1トークンずつ生成するため、出力が長いほど遅延が増える。著者らはこの二つの方式を競合関係とせず、軽量パイプラインの領域下書きを、強力な視覚言語モデルで段階的に検証する方式を提案する。

- **2026-01 · [TriSpec: Ternary Speculative Decoding via Lightweight Proxy Verification](2026-2601.23180-trispec-ternary-speculative-decoding-via-lightweight-proxy-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さなドラフトモデルが先に複数のトークンを提案し、大きな対象モデルがまとめて検証することで、自己回帰生成の逐次的な待ち時間を削減する。

- **2026-01 · [Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding](2026-2601.05724-overcoming-joint-intractability-with-lossless-hierarchical-speculative-d.md)**  
  実装：[✓](https://github.com/ZhouYuxuanYX/Hierarchical-Speculative-Decoding) ・ リポジトリ内被引用：1  
  HSDは利用可能な草案の枝だけから局所的な確率質量を計算し、階層をまたいで過不足を補正することで、この問題を回避する。主要実験はQwen2.5-0.5Bを草案とし、14B・32B・72Bを目標に使った比較で、トークン単位検証に対する復号速度の平均改善は約6.7%、一部条件では11%前後に達した。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [Match the Distribution, Not the Compute: Post-Training Multi-Token Prediction Heads](2026-2610.00888-match-the-distribution-not-the-compute-post-training-multi-token-predict.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結したQwen3-8Bが生成する推論文を教師にMTPヘッドだけを後学習し、厳密検証で事前学習済みMiMo-7B-RLに近い平均受理長を実現する。分布ずれを制御する近似検証と、実測処理量に応じてヘッド数を変える適応制御器も評価する。

- **2026-09 · [RheoSampling: Resolving the One-Hot Dilemma in Stochastic Dynamic-Tree Speculative Decoding](2026-2609.21827-rheosampling-resolving-the-one-hot-dilemma-in-stochastic-dynamic-tree-sp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  木型投機的復号（tree-based 投機的復号）は、小型ドラフトモデルが複数の候補トークン列を木として用意し、大型ターゲットモデルがその木をまとめて検証することで、自己回帰復号の一段ずつの待機を減らす。

- **2026-09 · [Resource-Efficient Speculative Decoding for Long-Context LLM Serving](2026-2609.33184-resource-efficient-speculative-decoding-for-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈でCPUに退避したKVキャッシュを検証の途中から使い、対象モデルの待ち時間に草案モデルを実行するSpecStreamの設計と評価。

- **2026-09 · [Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding](2026-2609.09338-osprey-target-agnostic-pretraining-speculative-decoding.md)**  
  実装：[✓](https://github.com/LeanModels/Osprey) ・ リポジトリ内被引用：0  
  Ospreyは、汎用ウェブで事前学習した浅いドラフト骨格を複数ターゲットへ転用し、ターゲット固有蒸留の初期値を改善して分野外でも受理トークンを増やし、検証回数を減らす。

- **2026-09 · [NebulaSD: Many-for-Many Speculative Decoding](2026-2609.29364-nebulasd.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NebulaSDは、投機的復号（投機的復号）のドラフト生成と対象モデル検証を固定した一対一の組から切り離し、M個のドラフトワーカーとN個の対象ワーカーを独立した共有資源プールとして運用する推論システムである。物理分離方式比で50.4%、同居方式比で72.6%高く、時間重み付きストリーミングマルチプロセッサ活動率も約29〜30%から47.3%へ上昇した。

- **2026-09 · [LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers](2026-2609.17184-loopspec-pipelined-self-speculative-looped-transformers.md)**  
  実装：[✓](https://github.com/kaist-flexml-lab/loopspec) ・ リポジトリ内被引用：0  
  ループ型Transformerの中間再帰状態を投機提案に使い、未来ドラフトと現在検証をパイプライン化して最大6.83倍高速化する。

- **2026-09 · [How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus](2026-2609.15504-orthrus-numerical-precision-losslessness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Orthrusの無損失投機的復号を独立再現し、BF16では生成軌跡の完全一致が43〜45%に留まる一方、FP32では1,190件すべて一致することを示した再現・評価研究。

- **2026-09 · [ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding](2026-2609.17241-echo-early-layer-collaborative-hierarchical-orchestration-with-bonus-logits-in-speculative-decoding.md)**  
  実装：[✓](https://github.com/whucs21Mzy/ECHO) ・ リポジトリ内被引用：0  
  対象モデルの前半層を高頻度の候補木探索、後半層を低頻度の厳密検証へ分け、中間状態再利用と補助ロジットで候補を更新し、追加ドラフトモデルなしで2.4〜2.9倍級の生成高速化を報告する。

- **2026-09 · [DFlow: Enabling Verifier Information Flow in Block Diffusion Speculative Decoding](2026-2609.06498-dflow-verifier-information-flow-block-diffusion.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却された後続位置の対象モデル中間表現を次の投機生成回へ再利用し、対象モデルの追加計算なしでブロック拡散型投機的復号の平均受理長を約10〜13%改善する。

- **2026-09 · [Carryover Drafting: Recycling Rejected States for Speculative Decoding](2026-2609.14717-carryover-drafting-recycling-rejected-states.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却されたターゲット隠れ状態を次回ドラフトの一時KV文脈へ再利用し、追加投影器なしで受理長を6.5〜14.7%改善する。

- **2026-08 · [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) ・ リポジトリ内被引用：0  
  GLANCEは、VLMの視覚・言語融合状態から未来トークン塊を1回で下書きし、幅広い候補木を対象モデルで一括検証して、画像根拠付き生成の逐次下書き処理を減らす。

- **2026-08 · [Verification-Aware Training for Speculative Decoding](2026-2608.30135-verification-aware-training-for-speculative-decoding.md)**  
  実装：[✓](https://github.com/naver-ai/VAT) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量な草案モデルが先の複数トークンを提案し、大きな目標モデルが一度の前向き計算でそれらを検証することで自己回帰生成の遅延を減らす。NVIDIA A100 80GB上で、EAGLE-3と拡散型のDFlash、目標モデルQwen3-4B、Qwen3-8B、Llama-3.1-8Bを組み合わせ、数学・コード・会話の八課題で評価した。

- **2026-08 · [TreeSpark: Calibrated, Load-Adaptive Draft Trees for Semi-Autoregressive Speculative Decoding](2026-2609.22098-treespark-calibrated-load-adaptive-draft-trees-for-semi-autoregressive-s.md)**  
  実装：[✓](https://github.com/PopSoda2002/TreeSpark) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな提案モデルが複数トークンを予測し、大きな目標モデルがまとめて検証することで、目標モデルの逐次呼び出しを減らす。原著の固定ノード数実験では、Qwen3-4B/8B/14Bのいずれも同じ検証ノード数のDDTreeより目標モデル1回当たりの受理トークン数が9〜16%増えた。

- **2026-08 · [Pre-Compiled Pipeline Shards for Distributed LLM Inference on Intel AI PC Fleets](2026-2608.19147-pre-compiled-pipeline-shards-for-distributed-llm-inference-on-intel-ai-p.md)**  
  実装：[✓](https://github.com/labscommunity/pipeline-sharded-inference-paper) ・ リポジトリ内被引用：0  
  本論文は、単独のメモリ容量では700億パラメータ級の大規模言語モデルを保持できない民生用AIパソコンを、通常のネットワーク越しに束ねる分散推論方式を示す。Llama 3.1 8Bの2台構成では、単一利用者の分散実行16.33トークン/秒から、2利用者合計43.97トークン/秒へ改善する。

- **2026-08 · [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MemSpecは、入力と生成履歴から有望なドラフトを予測し、上位モデルを常駐集合へ先読みして、エッジ端末のSSD読み込み待ちを隠し適応投機を高速化する。

- **2026-08 · [LiLiCorr: Lightweight Likelihood Correlation of Parallel Drafts for Speculative Decoding](2026-2608.20530-lilicorr-lightweight-likelihood-correlation-of-parallel-drafts-for-specu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量なドラフト器が未来の複数トークンを予測し、大きな対象モデルがまとめて検証することで、対象モデルの逐次実行回数を減らす。競合方式に対して処理率が明確に最良だったのは63条件、測定誤差1%以内の同率が6条件、劣ったのが3条件である。

- **2026-08 · [From Chains to Trees: Parent-Conditioned Drafting for Semi-Autoregressive Speculative Decoding](2026-2608.02123-from-chains-to-trees-parent-conditioned-drafting-for-semi-autoregressive.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの逐次生成は、直前のトークンを確定しなければ次を計算できないため、GPUの並列演算能力を十分に使いにくい。投機的復号（投機的復号）は小さな草案モデルに先のトークンを予測させ、目標モデルがまとめて検証する。しかし草案が一本の列だと、序盤のトークンが棄却された瞬間に後続の正しそうな候補も使えなくなる。

- **2026-08 · [CURE: Local Uncertainty Repair for Block-Parallel Speculative Decoding](2026-2608.00531-cure-local-uncertainty-repair-for-block-parallel-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CUREは、大規模言語モデルの投機的復号（投機的復号）において、草案を一度に複数トークン生成する方式の弱点を、少数の修復枝だけで補う推論時の仕組みである。Qwen3-8Bを検証器とする単一GPU実験では、通常の自己回帰復号に比べHumanEvalで3.490倍、MBPPで2.661倍、LiveCodeBench-liteで3.071倍の高速化を報告する。

- **2026-08 · [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな下書き器が複数の候補トークンを先に生成し、対象となる大規模言語モデルがそれらを一括検証することで、逐次生成の待ち時間を短縮する。

- **2026-07 · [Margins, Not Windows: Training-Free Per-Step Lossy Speculative Decoding](2026-2609.02897-margins-not-windows-training-free-per-step-lossy-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号は小さな下書きモデルに複数トークンまたは候補木を作らせ、targetモデルがまとめて検証することでこの逐次性を緩める。代表結果として、単一A100上の主評価で両軸併用方式は9条件すべてでEAGLE-3を上回り、モデル平均の高速化倍率は16–44%、最大改善は56%だった。

- **2026-07 · [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DraftExpertは、各MoE層に小型の常駐専門家を追加して候補を作り、専門家展開量を予測した枝打ちと非同期先読みを行い、端末の専門家搬送待ちを減らす。

- **2026-07 · [AdaptiveSD A Stability-Aware, Runtime-Adaptive Speculative Decoding Framework with Multi-Policy Orchestration for CPU-Constrained LLM Inference](2026-2607.03876-adaptivesd-runtime-adaptive-cpu-constrained.md)**  
  実装：[✓](https://github.com/sadrasa97/adaptive-speculate-decoding) ・ リポジトリ内被引用：0  
  CPU資源・受理率・遅延・KV圧力を監視し、投機深度を閉ループ制御して資源飽和と遅延変動を抑える適応投機デコード。

- **2026-06 · [PRESTO: Prefix-Aligned Tree Drafting for Diffusion Speculative Decoding](2026-2607.22634-presto-prefix-aligned-tree-drafting-for-diffusion-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量な草稿モデル（下書きモデル）で将来のトークン候補を生成し、大きな対象モデル（対象モデル）でまとめて検証することで、対象モデルの出力品質を維持しながら生成速度を上げる技術である。

- **2026-05 · [Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding](2026-2605.26558-cassandra-enabling-reasoning-llms-at-edge-via-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非構造化の重要値選別、仮数部切詰め、指数部の圧縮を併用し、ビット表現の復号を支援する専用回路とメモリ管理まで設計している。

- **2026-05 · [Bastion: Budget-Aware Speculative Decoding with Tree-structured Block Diffusion Drafting](2026-2605.29727-bastion-budget-aware-speculative-decoding-with-tree-structured-block-dif.md)**  
  実装：[✓](https://github.com/kaist-ai-osi-lab/BASTION) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さい草稿モデル（drafter）が先に複数トークンを提案し、対象モデルがまとめて検証することで、対象モデルの逐次呼出し回数を減らす。

- **2026-05 · [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、投機的復号（投機的復号）が単独要求では速くても、実際の大規模言語モデル配備で要求数が増えると高速化倍率が縮小し、場合によっては通常復号より遅くなる現象を説明する遅延モデルを提案する。

- **2026-04 · [NanoSpec: Accelerating Speculative Decoding using Minimalist In-Context Vocabularies](2026-2605.26444-microspec-lightweight-in-context-vocabularies.md)**  
  実装：[✓](https://github.com/csAugust/NanoSpec) ・ リポジトリ内被引用：0  
  文脈と直近候補から毎ステップ3000未満の動的ドラフト語彙を作り、必要なLMヘッド重みを非同期収集して射影計算を削減する投機的デコード最適化。EAGLE-2のドラフト時間を平均51.6%削減する。

- **2026-04 · [Multi-Drafter Speculative Decoding with Alignment Feedback](2026-2604.05417-multi-drafter-speculative-decoding-with-alignment-feedback.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は小さなドラフトモデルが先のトークン列を予測し、対象モデルがまとめて検証することで逐次呼出し回数を減らす。

- **2026-04 · [Goose: Anisotropic Speculation Trees for Training-Free Speculative Decoding](2026-2604.02047-goose-anisotropic-speculation-trees-for-training-free-speculative-decodi.md)**  
  実装：[✓](https://github.com/2kinto/GOOSE_Speculative_Decoding) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、安価な候補生成器が未来のトークン列を先に提案し、目標モデルが一回の前向き計算で複数候補をまとめて検証する。入力や生成済み文脈から一致するn-gramの続きをコピーする文脈照合候補は、目標モデルの過去の出力分布から予測する遷移候補よりも、測定上2〜18倍、中央値約6倍の受理率を持つ。

- **2026-04 · [FASER: Fine-Grained Phase Management for Speculative Decoding in Dynamic LLM Serving](2026-2604.20503-faser-fine-grained-phase-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的負荷下の投機的デコードを、リクエスト別投機長、検証途中の棄却枝刈り、ドラフトと検証のフロンティア単位重畳で細粒度化し、vLLM上で最大53%のスループット向上と最大1.92倍の遅延改善を示す。

- **2026-04 · [DIVERSED: Relaxed Speculative Decoding via Dynamic Ensemble Verification](2026-2604.07622-diversed-relaxed-speculative-decoding-via-dynamic-ensemble-verification.md)**  
  実装：[✓](https://github.com/comeusr/diversed) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小型のドラフトモデルが複数トークンを先読みし、大型の対象モデルがそれらをまとめて検証することで、逐次生成の待ち時間を短縮する。

- **2026-04 · [AHASD: Asynchronous Heterogeneous Architecture for LLM Adaptive Drafting Speculative Decoding on Mobile Devices](2026-2604.25326-ahasd-asynchronous-heterogeneous-architecture-for-llm-adaptive-drafting-.md)**  
  実装：[✓](https://github.com/MAdrid1011/AHASD) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな草稿モデル（下書き language モデル, DLM）が複数の候補トークンを生成し、大きな目標モデル（target language モデル, TLM）がまとめて検証することで、高価な目標モデルの逐次実行回数を減らす。

- **2026-02 · [Vegas: Self-Speculative Decoding with Verification-Guided Sparse Attention](2026-2602.07223-specattn-sparse-attention-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/platformxlab/vegas) ・ リポジトリ内被引用：0  
  検証で得た注意ロジットを次の疎な候補生成へ再利用し、鍵値選択の追加走査を抑えながら損失なし自己投機復号を高速化する。

- **2026-02 · [Variational Speculative Decoding: Rethinking Draft Training from Token Likelihood to Sequence Acceptance](2026-2602.05774-variational-speculative-decoding-rethinking-draft-training-from-token-li.md)**  
  実装：[✓](https://github.com/LV-Lab-SMU/VSD) ・ リポジトリ内被引用：0  
  投機的復号では草案モデルが先の複数トークンをまとめて提案し、大きな目標モデルが一回の並列計算で検証する。

- **2026-01 · [StarSD: One-for-Many Speculative Decoding](2026-2601.21622-starsd-one-for-many-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  StarSDは、複数の大型言語モデルの推論要求が一つの軽量下書きモデルを共有する、星型の分散投機的復号（投機的復号）システムである。原著の2サーバ・計7 GPUの構成では、対象モデル1個で総処理量79.9トークン/秒、6個で288.7トークン/秒に増えた。

- **2025-12 · [GoodSpeed: Optimizing Fair Goodput with Adaptive Speculative Decoding in Distributed Edge Inference](2025-2512.09963-goodspeed-optimizing-fair-goodput-with-adaptive-speculative-decoding-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GoodSpeedは、複数の小型言語モデル（Small Language Models; SLM）がエッジサーバで候補トークンを作り、中央の大型言語モデル（Large Language モデル; LLM）が一括検証する分散投機的復号（投機的復号; SD）のスケジューラである。

- **2025-12 · [Fail Fast, Win Big: Rethinking the Drafting Strategy in Speculative Decoding via Diffusion LLMs](2025-2512.20573-fail-fast-win-big-rethinking-the-drafting-strategy-in-speculative-decodi.md)**  
  実装：[✓](https://github.com/ruipeterpan/failfast) ・ リポジトリ内被引用：0  
  生成がメモリ帯域に制約される場面では、各トークンのために大きなモデルを繰り返し実行することが遅延の原因となる。投機的復号（投機的復号）は小さな草稿モデルが複数トークンを先に提案し、大きな対象モデルがそれらをまとめて検証することで、この反復回数を減らす。

- **2025-12 · [AdaSD: Adaptive Speculative Decoding for Efficient Language Model Inference](2025-2512.11280-adasd-adaptive-speculative-decoding-for-efficient-language-model-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の通常方式では、小型モデルが数トークンを先に生成し、大型モデルが一度の前向き計算で候補を並列検証する。

- **2025-12 · [Accelerate Speculative Decoding with Sparse Computation in Verification](2025-2512.21911-accelerate-speculative-decoding-with-sparse-computation-in-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな草稿モデルが複数の候補トークンを先読みし、大きな対象モデルがそれらをまとめて検証することで、対象モデルの呼出し回数を減らす手法である。品質と平均受理長の評価はあるが、元モデルの出力分布との数学的同値性や、GPUでのエンドツーエンド実測速度向上は示されていない。

- **2025-11 · [TapOut: A Bandit-Based Approach to Dynamic Speculative Decoding](2025-2511.02017-tapout-a-bandit-based-approach-to-dynamic-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TapOutは、確率分布に基づく五つの停止規則を候補とし、多腕バンディット（multi-armed bandit）が検証結果からその時点で有利な規則を選ぶ方式である。

- **2025-11 · [Speculative Streaming: Efficient and Scalable Speculative Decoding with Multi-Stream Attention](2025-ecec79b7ef4d-speculative-streaming-efficient-and-scalable-speculative-decoding-with-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Medusaのように対象モデルへ複数予測ヘッドを付ける方式は別モデルを不要にするが、ヘッド間のトークン依存を表現しにくい。

- **2025-11 · [Speculative Decoding in Decentralized LLM Inference: Turning Communication Latency into Computation Throughput](2025-2511.11733-speculative-decoding-in-decentralized-llm-inference-turning-communicatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散投機的復号（Decentralized 投機的復号、DSD）は、投機的復号を中央集約型GPUサーバから、複数の独立管理ノードへモデルを分割して実行する環境へ拡張した方式である。

- **2025-11 · [Scaling LLM Speculative Decoding: Non-Autoregressive Forecasting in Large-Batch Scenarios](2025-2511.20340-scaling-llm-speculative-decoding-non-autoregressive-forecasting-in-large.md)**  
  実装：[✓](https://github.com/ShiLuohe/SpecFormer) ・ リポジトリ内被引用：0  
  投機的復号は小さなモデルが複数トークンを先読みし、大きな目標モデルで一括検証することにより、目標モデルを直列に呼び出す回数を減らす。著者はQwenおよびLlama系で評価し、特定の草案予算制約下では従来のHASSやEAGLE-3より高い総トークン処理速度を示した。

- **2025-11 · [Collaborative Large Language Model Inference via Resource-Aware Parallel Speculative Decoding](2025-2511.01695-collaborative-large-language-model-inference-via-resource-aware-parallel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さなドラフトモデルが複数トークンを先に生成し、大きなターゲットモデルがまとめて検証することで、出力品質を維持しながら生成の待機時間を短縮することを目指す。

### 2年前（2024-11〜2025-10）

- **2025-03 · [EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](2025-2503.01840-eagle-3.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：117  
  特徴回帰制約を外して直接トークン予測し、訓練時に自己生成入力を再投入することでドラフト学習のデータ規模拡大を有効化したEAGLE系投機的復号。

- **2025-09 · [DiffuSpec: Unlocking Diffusion Language Models for Speculative Decoding](2025-2510.02358-diffuspec-unlocking-diffusion-language-models-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  投機的復号は小さいドラフト器が数トークンを先に作り、大きい対象モデルがまとめて検証することで逐次実行を減らす。論文の主実験では、Qwen2.5-32Bを対象モデル、Dream-7Bをドラフト器とし、単一NVIDIA A100 80GBで六つの課題群を評価した。

- **2025-04 · [Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion](2025-speculative-diffusion-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  自己回帰型の下書き器を離散拡散型へ置換し、候補列の生成と目標モデルによる検証の双方を並列化して投機的復号を高速化する方式。

- **2025-04 · [PARD: Accelerating LLM Inference with Low-Cost PARallel Draft Model Adaptation](2025-2504.18583-pard-accelerating-llm-inference-with-low-cost-parallel-draft-model-adaptation.md)**  
  実装：[✓](https://github.com/AMD-AIG-AIMA/PARD) ・ リポジトリ内被引用：13  
  PARDは、高精度な小型自己回帰モデルを、1回の順伝播で複数の候補トークンを出す並列下書きモデルへ低コストで適応し、同一モデル系列の複数の対象モデルへ再利用できるようにする投機的復号（投機的復号）方式である。

- **2025-02 · [LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification](2025-2502.17421-longspec-long-context-lossless-speculative-decoding-with-efficient-draft.md)**  
  実装：[✓](https://github.com/sail-sg/LongSpec) ・ リポジトリ内被引用：13  
  投機的復号（投機的復号）は、小さいドラフトモデルが次の候補トークンを先に作り、大きな対象モデルがまとめて検証することで、最終的な出力分布を変えずに生成を高速化する。

- **2025-10 · [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  本論文は、混合専門家（Mixture-of-Experts、MoE）モデルの重みを中央処理装置メモリへ退避する環境で、投機的復号（投機的復号）を併用すると検証段階に多数の専門家が必要となり、中央処理装置から画像処理装置への重み転送が競合する問題を扱う。

- **2025-05 · [SpecBranch: Speculative Decoding via Hybrid Drafting and Rollback-Aware Branch Parallelism](2025-2506.01979-specbranch-speculative-decoding-via-hybrid-drafting-and-rollback-aware-branching.md)**  
  実装：[✓](https://github.com/Sylvan820/Specbranch) ・ リポジトリ内被引用：11  
  投機的復号は、この逐次依存を小型のドラフトモデルが候補を先行生成し、大型の対象モデルが複数候補をまとめて検証する方式で緩和する。ICLR 2026掲載版の評価では、複数のドラフト・対象モデル組合せと課題に対し、通常の自己回帰生成比でおおむね1.8〜4.5倍の高速化を報告する。

- **2024-11 · [SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications](2024-2411.04975-suffixdecoding-extreme-speculative-decoding-for-emerging-ai-applications.md)**  
  実装：[✓](https://github.com/snowflakedb/ArcticInference) ・ リポジトリ内被引用：11  
  SuffixDecodingは、大規模言語モデルの生成結果が過去の生成と繰り返し似た文字列になる場面を利用し、追加の草稿モデルを使わずに投機的復号（投機的復号）を高速化する推論基盤技術である。この方式が狙うのは、プログラム修正エージェントの反復試行、複数エージェントによる同形式の応答、SQL生成の定型構造など、同じ接頭辞・後続列が繰り返される作業である。

- **2025-05 · [MoESD: Unveil Speculative Decoding's Potential for Accelerating Sparse MoE](2025-2505.19645-moesd-unveiling-speculative-decodings-potential-for-accelerating-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  投機的復号（投機的復号; SD）は、小型の下書きモデルが複数トークンを先行提案し、大型の対象モデルが一括検証することで、対象モデルの逐次呼び出し回数を減らす。通常の密モデルでは、対象モデルの重みを一度読み込んで複数候補を検証できるため高速化しやすい。

- **2024-11 · [Draft Model Knows When to Stop: Self-Verification Speculative Decoding for Long-Form Generation](2024-2411.18462-draft-model-knows-when-to-stop-a-self-verification-length-policy-for-spe.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  投機的復号は、小型のドラフトモデルが先に数トークンを生成し、大型の対象モデルがまとめて検証することで、対象モデルの逐次実行回数を減らす方式である。著者らはQwen2.5を用いたMT-Benchの最大8K文脈で、固定長より最大17%の高速化を報告する。

- **2025-06 · [Utility-Driven Speculative Decoding for Mixture-of-Experts](2025-2506.20675-cascade.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoEでは投機長が増やす専門家読出し費用まで含めた効用を実測し、投機の無効化とK選択を動的に行って最悪減速を5%へ抑える。

- **2025-01 · [Reward-Guided Speculative Decoding for Efficient LLM Reasoning](2025-2501.19324-reward-guided-speculative-decoding-for-efficient-llm-reasoning.md)**  
  実装：[✓](https://github.com/BaohaoLiao/RSD) ・ リポジトリ内被引用：7  
  複雑な数学問題に大規模言語モデルを使うと、最終回答に至るまで何十もの途中式や判断を順番に生成する。高性能な大型モデルだけに全段階を担当させると、簡単な計算の確認にも高価なモデルの演算を費やす。一方、小型モデルだけでは途中の誤りが連鎖して最終回答を損なう。報酬が閾値以上なら草稿を採用し、低ければ草稿を棄却して目標モデルに同じ文脈から次段階を生成させる。

- **2025-09 · [Set Block Decoding is a Language Model Inference Accelerator](2025-2509.04185-set-block-decoding-is-a-language-model-inference-accelerator.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  次トークン予測とマスク位置予測を同一Transformerへ統合し、未来ブロックの非連続位置をEB-Samplerで並列確定するSBD。8Bモデルで品質を概ね維持しながら前向き計算回数を約3〜5倍削減し、H100屋根線モデルで実時間化の可能性を分析する。

- **2025-05 · [Fast and Cost-effective Speculative Edge-Cloud Decoding with Early Exits](2025-2505.21594-fast-and-cost-effective-speculative-edge-cloud-decoding-with-early-exits.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Cloud 対象の早期出口から暫定トークンを返し、edge ドラフトを最終検証と並行して先行生成することで待ち時間を隠し、Jetson Nano＋A100でpre-drafting単体最大11%級の追加改善を示す。

- **2025-09 · [SpecVLM: Fast Speculative Decoding in Vision-Language Models](2025-2509.11815-specvlm-fast-speculative-decoding-in-vision-language-models.md)**  
  実装：[✓](https://github.com/haiduo/SpecVLM) ・ リポジトリ内被引用：5  
  SpecVLMは、この視覚特有の律速に対して、EAGLE-2型の軽量候補生成器EagleVLM、質問内容に応じて視覚圧縮方式を選ぶ弾力的視覚圧縮器、対象モデルのロジットと最終直前特徴をその場で教師にするオンライン蒸留を組み合わせる。対象モデルによる並列検証と投機的サンプリングを維持するため、正しい受理・棄却処理を行う限り対象モデルの出力分布を保つ。

- **2024-12 · [Dovetail: A CPU/GPU Heterogeneous Speculative Decoding for LLM inference](2024-2412.18934-dovetail-cpu-gpu-heterogeneous-speculative-decoding.md)**  
  実装：[✓](https://github.com/ddInference/Dovetail) ・ リポジトリ内被引用：5  
  ターゲットLLMをCPU、深くした小型ドラフトをGPUへ分離し、候補数削減・動的ゲート融合・複数Transformerブロックで低VRAM環境の投機的デコードを高速化する。

- **2025-07 · [TETRIS: Optimal Draft Token Selection for Batch Speculative Decoding](2025-2502.15197-tetris-optimal-draft-token-selection-for-batch-speculative-decoding.md)**  
  実装：[✓](https://github.com/ZhaoxuanWu/Tetris) ・ リポジトリ内被引用：4  
  投機的復号（投機的復号; SD）で速いドラフトモデルが多めの候補を作り、遅い対象モデルが並列検証する構造はそのままに、対象モデルへ送る候補を要求ごとではなくバッチ全体で選び直す。各要求の連続候補について「そこまで全部受理される確率」を計算し、限られた検証容量 (C) を確率の高い前方トークンへ配る。

- **2025-02 · [Speculative Decoding and Beyond: An In-Depth Survey of Techniques](2025-2502.19732-speculative-decoding-and-beyond-an-in-depth-survey-of-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本稿は、大規模言語モデル（LLM）の自己回帰復号に伴う逐次依存を、候補列の生成（generation）と修正・検証（refinement）に分離して整理した技術サーベイである。

- **2025-03 · [ML-SpecQD: Multi-Level Speculative Decoding with Quantized Drafts](2025-2503.13565-ml-specqd-multi-level-speculative-decoding-quantized-drafts.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BF16対象の直接MXFP4版を第一段ドラフトにし、その生成を小型ドラフトで再び投機して、専用ドラフト学習なしに最大2.72倍高速化する。

- **2025-10 · [HiSpec: Hierarchical Speculative Decoding for LLMs](2025-2510.01336-hispec-hierarchical-speculative-decoding-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  HiSpecは、投機的復号の律速が候補トークンの作成ではなく巨大な対象モデルによる検証に移っていることを踏まえ、同じ早期退出モデルの浅い層・中間層・最終層をそれぞれドラフト生成・中間検証・最終検証へ割り当てる階層型の復号方式である。

- **2025-10 · [Accelerating Mobile Language Model via Speculative Decoding and NPU-Coordinated Execution](2025-2510.15312-accelerating-mobile-language-model-via-speculative-decoding-and-npu-coor.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  sd.npuは、スマートフォン上で検索拡張生成（retrieval-augmented generation; RAG）を動かすとき、モバイル神経処理装置（neural processing unit; NPU）の演算器を使い切れない問題を、実行時制御と推測復号（投機的復号）の両側から解決するシステムである。

- **2025-09 · [Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding](2025-2509.04576-communication-efficient-distributed-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  分散投機的デコードの上り通信を語彙全体分布から上位K疎ロジットへ圧縮し、出力分布を維持したまま通信量と最適ドラフト長を共同最適化する。

- **2025-07 · [Quantize-Sample-and-Verify: LLM Acceleration via Adaptive Edge-Cloud Speculative Decoding](2025-2507.00605-quantize-sample-and-verify-llm-acceleration-via-adaptive-edge-cloud-spec.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  しかし端末とクラウドがネットワークで離れていると、下書きトークンだけでなく検証に必要な確率分布を毎反復で送る必要があり、通信遅延が利点を打ち消す。本論文は、送信確率を量子化する際の処理順序に着目する。評価では、クラウドOPT-13Bと端末側OPT-125M、CNN/DailyMail要約、上り平均350 kbpsと4 Mbpsの二条件を使う。

- **2025-06 · [Scaling Speculative Decoding with Lookahead Reasoning](2025-2506.19830-scaling-speculative-decoding-with-lookahead-reasoning.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadReasoning) ・ リポジトリ内被引用：2  
  従来の投機的復号（投機的復号）は小型モデルが未来のトークンを先行提案し、大型目標モデルが複数位置をまとめて検証する。しかし草稿長を増やすほど全トークンが連続して受理される確率が下がり、目標モデルの検証計算も増えるため、速度向上が頭打ちになる。

- **2025-05 · [Scaling Laws for Speculative Decoding](2025-2505.07858-scaling-laws-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号の速度はドラフトの受理率だけでは決まらない。ドラフト事前学習、層数、対象モデルの検証幅を別々に測り、GPUのメモリ帯域と演算能力の境界に合わせて検証候補を絞る設計を示す。

- **2025-03 · [SPIN: Accelerating Large Language Model Inference with Heterogeneous Speculative Models](2025-2503.15921-spin-heterogeneous-speculative-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  要求難度に応じて異種の小型下書きモデルを選択し、検証バッチのゼロ埋めを要求分解で減らし、下書き生成と標的検証を小バッチ単位で重ねて投機的デコードを高速化する。

- **2025-05 · [SpecMemo: Speculative Decoding is in Your Pocket](2025-2506.01986-specmemo-memory-aware-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的デコードの候補木・KVキャッシュ・デコードヘッドをGPUメモリ予算に合わせて自動調整し、Titan RTXで生成メモリ65%削減・スループット96%維持、8×MI250のLlama-2-70Bでは通常分散復号比2倍を示す。

- **2025-04 · [Hierarchical Speculative Decoding with Dynamic Windows for Efficient Language Model Inference](2025-d38a1bd0beb3-hierarchical-speculative-decoding-with-dynamic-windows-for-efficient-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの逐次生成では、巨大な対象モデルをトークンごとに呼ぶ費用が大きい。投機的復号（投機的復号）は小型のドラフトモデルに複数の候補を作らせ、対象モデルで一括検証する。これらは対象モデル単独の自己回帰生成を1とした速度倍率であり、別の投機的復号方式に対して常に同じ倍率で勝つという意味ではない。

- **2025-02 · [Fuzzy Speculative Decoding for a Tunable Accuracy-Runtime Tradeoff](2025-2502.20704-fuzzy-speculative-decoding-for-a-tunable-accuracy-runtime-tradeoff.md)**  
  実装：[✓](https://github.com/maxholsman/fsd) ・ リポジトリ内被引用：1  
  標準的な投機的復号（投機的復号; SD）は、小さいドラフトモデルが複数トークンを先に生成し、大きいターゲットモデルがそれらを一括検証することで、ターゲットモデルの逐次実行回数を減らす。たとえばQwen 2.5 7B/32BのGSM8Kでは、標準SDの95.1%・17.4トークン/秒に対し、低閾値FSDは94.7%・21.4トークン/秒となる。

- **2025-08 · [CARD: A Cache-Assisted Parallel Speculative Decoding Framework via Query-and-Correct Paradigm for Accelerating LLM Inference](2025-2508.04462-card-cache-assisted-parallel-speculative-decoding-for-efficient-large-la.md)**  
  実装：[✓](https://github.com/hunzhizi/CARD) ・ リポジトリ内被引用：0  
  CARDは、大規模言語モデル（LLM）の投機的復号（投機的復号）で、ドラフトモデルが候補を作り終わるまで対象モデルが待ち、対象モデルが検証している間ドラフトモデルが待つという相互待機を減らす方式である。

### 3年前（2023-11〜2024-10）

- **2024-01 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)**  
  実装：[✓](https://github.com/FasterDecoding/Medusa) ・ リポジトリ内被引用：244  
  Medusaは、対象LLMの隠れ状態に未来位置ごとの小型予測ヘッドを追加し、上位候補を木構造へまとめて一括検証することで、別ドラフトモデルを置かず対象モデルの逐次呼出しを減らす。

- **2024-01 · [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：198  
  EAGLEは、対象LLMの上位層特徴量と直前に標本化したトークンを小型デコーダへ与えて未来特徴量を予測し、元の言語モデル出力ヘッドと木構造検証で重み読出し回数を減らす。

- **2024-06 · [EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](2024-2406.16858-eagle-2.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：100  
  EAGLE-2は、既存のEAGLEで用いる小型の下書きモデルをそのまま使いながら、投機的復号（投機的復号）で検証する候補木の形を入力文脈に応じて変える手法である。代表的な温度0のVicuna 7B・MT-benchでは通常生成比3.62倍、既存EAGLEは2.90倍であり、平均受理長はそれぞれ4.98と3.94トークンである。

- **2024-02 · [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadDecoding) ・ リポジトリ内被引用：93  
  先読みデコードは、対象LLMを未来位置へ並列反復して途中の正しい短いトークン列を蓄積し、現在接頭辞に合う候補を一括検証して、追加モデルなしに逐次ステップとメモリ帯域待ちを減らす。

- **2023-11 · [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)**  
  実装：[✓](https://github.com/FasterDecoding/REST) ・ リポジトリ内被引用：68  
  RESTは、現在文脈末尾と一致する過去トークン列を接尾辞索引から検索し、その続き候補を木構造へ集約して対象LLMで一括検証し、ドラフトモデルなしで反復的なコードの対象重み読出しを減らす。

- **2024-07 · [Online Speculative Decoding](2023-2310.07177-online-speculative-decoding.md)**  
  実装：[✓](https://github.com/LiuXiaoxuanPKU/OSD) ・ リポジトリ内被引用：59  
  投機的復号で得られる目標モデルの確率分布を教師信号として下書きモデルをオンライン更新し、問い合わせ分布の変化に追従して受理率と推論速度を高める方式。

- **2024-02 · [Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding](2024-2402.12374-sequoia-scalable-robust-and-hardware-aware-speculative-decoding.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/Sequoia) ・ リポジトリ内被引用：47  
  自己回帰型の大規模言語モデル（LLM）は、1 トークンを確定するたびに大きな対象モデルを1回実行するため、生成の逐次依存が遅延の下限になる。また、標本化温度が変わるとドラフト分布と対象分布の重なり方が変わり、固定的な木構造・検証方式は性能が不安定になる。

- **2024-04 · [TriForce: Lossless Acceleration of Long Sequence Generation with Hierarchical Speculative Decoding](2024-2404.11912-triforce-lossless-acceleration-of-long-sequence-generation-with-hierarch.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/TriForce) ・ リポジトリ内被引用：40  
  長文脈のKVキャッシュ読込を減らす近似的な中間検証と、完全KVによる厳密な最終検証を分離することで、長系列の投機的復号を高速化する。

- **2024-05 · [SpecDec++: Boosting Speculative Decoding via Adaptive Candidate Lengths](2024-2405.19715-specdec-boosting-speculative-decoding-via-adaptive-candidate-lengths.md)**  
  実装：[✓](https://github.com/Kaffaljidhmah2/SpecDec_pp) ・ リポジトリ内被引用：35  
  SpecDec++は、大きな対象モデルの出力分布を保持する投機的復号（投機的復号）において、小さなドラフトモデルが何トークン先まで候補を作ってから対象モデルに検証させるかを、生成の途中で動的に決める手法である。

- **2024-08 · [MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding](2025-2408.11049-magicdec-breaking-the-latency-throughput-tradeoff-for-long-context-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：34  
  長文脈と大きなバッチを同時に扱うと、KVキャッシュの転送が推論を律速し、投機的復号の検証費用が相対的に小さくなる。MagicDecは疎KVドラフトと受理率・計算費用の解析を組み合わせ、従来の「大バッチでは投機が不利」という通説の成立範囲を明確にする。

- **2024-08 · [PEARL: Parallel Speculative Decoding with Adaptive Draft Length](2024-2408.11850-pearl-parallel-speculative-decoding-with-adaptive-draft-length.md)**  
  実装：[✓](https://github.com/smart-lty/ParallelSpeculativeDecoding) ・ リポジトリ内被引用：31  
  投機的復号は、小さなドラフトモデルが先の複数トークンを予測し、大きな対象モデルがそれらを一回の順伝播でまとめて検証する。一次論文の2024年9月版では、コード生成、算術推論、複数ターン対話の実験で、自己回帰生成比最大3.79倍、通常の投機的復号比最大1.52倍の高速化を報告する。

- **2024-06 · [OPT-Tree: Speculative Decoding with Adaptive Draft Tree Structure](2024-2406.17276-opt-tree-speculative-decoding-with-adaptive-draft-tree-structure.md)**  
  実装：[✓](https://github.com/Jikai0Wang/OPT-Tree) ・ リポジトリ内被引用：29  
  OPT-Treeは、投機的復号（投機的復号）で草稿モデルが作る候補の木構造を、各生成ステップの予測確率に応じて変える方式である。実験では対象モデルと草稿モデルの組合せによって最大約3.2倍の生成処理率改善を報告する。

- **2024-04 · [Kangaroo: Lossless Self-Speculative Decoding for Accelerating LLMs via Double Early Exiting](2024-2404.18911-kangaroo-lossless-self-speculative-decoding-via-double-early-exiting.md)**  
  実装：[✓](https://github.com/Equationliu/Kangaroo) ・ リポジトリ内被引用：24  
  一般的な方式では、対象モデルとよく似た予測を出す小型ドラフトモデルを別途学習・配置する必要がある。NeurIPS 2024最終版では単一系列検証だけでなく動的な木状候補にもこの二段目の早期終了を拡張し、Spec-BenchでVicuna-7B平均1.72倍、Vicuna-13B平均1.65倍、最大2.04倍の壁時計高速化を報告する。

- **2024-08 · [Learning Harmonized Representations for Speculative Sampling](2024-2408.15766-learning-harmonized-representations-for-speculative-sampling.md)**  
  実装：[✓](https://github.com/HArmonizedSS/HASS) ・ リポジトリ内被引用：21  
  HASSはEAGLE-2の投機的復号で、下書きモデルの学習時には正しい対象モデルの隠れ状態が見えるが、生成時には自己予測した不正確な状態を使うという文脈不一致を解消する。H800・バッチ1の四種類のLLaMAと三課題で自己回帰比2.81〜4.05倍の実時間高速化を示す一方、学習時間はEAGLE-2比平均66.34%増加する。

- **2024-10 · [SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration](2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleratio.md)**  
  実装：[✓](https://github.com/hemingkx/SWIFT) ・ リポジトリ内被引用：20  
  したがって本研究は「精度を下げて速くする層削減」ではなく、「一時的な近似ドラフトで正確な検証を少ない回数にする」方式である。LLaMA-2-13Bでは通常自己回帰の20.10トークン/秒に対して28.26トークン/秒、全体1.41倍、LLaMA-2-70Bでは4.32に対して6.41トークン/秒、1.48倍を報告する。

- **2024-03 · [Recurrent Drafter for Fast Speculative Decoding in Large Language Models](2024-2403.09919-recurrent-drafter-for-fast-speculative-decoding-in-large-language-models.md)**  
  実装：[✓](https://github.com/apple/ml-recurrent-drafter) ・ リポジトリ内被引用：20  
  軽量再帰型の下書きモデル、ビーム探索、動的な共有接頭辞除去、対象モデルからの知識蒸留を組み合わせる。受理トークン数が多くても処理率が上がるとは限らないことを、実測の正負両結果から検証する。

- **2023-12 · [Cascade Speculative Drafting for Even Faster LLM Inference](2023-2312.11462-cascade-speculative-drafting-for-even-faster-llm-inference.md)**  
  実装：[✓](https://github.com/lfsszd/CS-Drafting) ・ リポジトリ内被引用：20  
  ChenらのCascade 投機的 Drafting（CS Drafting）は、下書きモデルの生成をさらに小さなモデルによる投機で加速する縦方向の連鎖（Vertical Cascade）と、候補列の位置ごとに異なる計算費の下書きモデルを割り当てる横方向の連鎖（Horizontal Cascade）を組み合わせる。

- **2024-05 · [Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models](2024-2405.04304-dynamic-speculation-lookahead-accelerates-speculative-decoding-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  投機的復号（投機的復号）は、安価な下書きモデルが将来トークンを自己回帰的に生成し、対象モデルが複数候補を一括検証することで推論時間を短縮する。

- **2024-06 · [SpecExec: Massively Parallel Speculative Decoding for Interactive LLM Inference on Consumer Devices](2024-2406.02532-specexec-massively-parallel-speculative-decoding-for-interactive-llm-inference-on-consumer-devices.md)**  
  実装：[✓](https://github.com/yandex-research/specexec) ・ リポジトリ内被引用：17  
  RAMオフロードでは「対象モデルを1トークン通す時間」と「数百〜数千トークンをまとめて通す時間」の差が小さくなる。SpecExecはその余剰バッチ幅で将来分布を事前計算し、70B級モデルを消費者GPUでも数トークン/sで対話可能にする。

- **2024-02 · [Speculative Streaming: Fast LLM Inference without Auxiliary Models](2024-2402.11131-speculative-streaming-fast-llm-inference-without-auxiliary-models.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  本論文の課題は、大規模言語モデルの自己回帰復号が一トークンずつ重みを読み込むため、演算器の能力を使い切れないことにある。投機的復号では小さな下書きモデルが将来トークンを先読みし、大きな対象モデルが候補をまとめて検証する。

- **2024-03 · [Block Verification Accelerates Speculative Decoding](2024-2403.10444-block-verification-accelerates-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  各接頭辞の受理確率を適切に設計し、受理された中で最も長い接頭辞を確定させる。PaLM-2-Sを対象、PaLM-2-XXSを下書きとし、候補長8、8種類のデータセットで測った結果、対象モデル一回当たりの生成量を示すブロック効率は平均3.41から3.70へ増え、標準検証に対して8.30%改善した。

- **2024-10 · [DySpec: Faster Speculative Decoding with Dynamic Token Tree Structure](2024-2410.11744-dyspec-faster-speculative-decoding-with-dynamic-token-tree-structure.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  一覧用要約：DySpecは下書きモデルの確率分布から候補の受理見込みを近似し、受理後の子候補と拒否後の兄弟候補を優先度付きキューで動的に展開する。閾値付き層単位生成で下書き呼出しを抑え、Llama2-70BのCPUオフロード条件では対象モデル呼出し回数の削減により大きな速度改善を得る。

- **2024-02 · [Ouroboros: Generating Longer Drafts Phrase by Phrase for Faster Speculative Decoding](2024-2402.13720-ouroboros-generating-longer-drafts-phrase-by-phrase-for-faster-speculati.md)**  
  実装：[✓](https://github.com/thunlp/Ouroboros) ・ リポジトリ内被引用：12  
  通常の投機的復号（投機的復号）では、対象となる大規模言語モデル（対象モデル）より小さい下書きモデル（下書きモデル）が数トークンを先読み生成し、対象モデルがそれらを一度に検証する。

- **2024-02 · [Generation Meets Verification: Accelerating Large Language Model Inference with Smart Parallel Auto-Correct Decoding](2024-2402.11809-generation-meets-verification-accelerating-large-language-models-with-speculative-decoding.md)**  
  実装：[✓](https://github.com/cteant/SPACE) ・ リポジトリ内被引用：12  
  SPACE（Smart Parallel Auto-Correct デコード）は、自己回帰（autoregressive）型の大規模言語モデルを、別の小型下書きモデルを使わずに高速化する投機的復号方式である。論文は6B～70B級の複数モデルを評価し、HumanEval-Xのコード生成では2.71～4.04倍の高速化を報告する。

- **2024-10 · [AdaEDL: Early Draft Stopping for Speculative Decoding of Large Language Models via an Entropy-based Lower Bound on Token Acceptance Probability](2024-2410.18351-adaedl-early-draft-stopping-for-speculative-decoding-of-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  追加の停止予測ネットワークを学習しない点が、学習型の適応長方式との主要な違いである。単一NVIDIA A100 80GB・FP32で、Llama2-7Bを対象、直接整合済みの115M下書きを用いたCNN-DM要約では、最大下書き長16の固定方式36.30 トークン/sに対し54.10 トークン/sを報告する。

- **2024-04 · [On Speculative Decoding for Multimodal Large Language Models](2024-2404.08856-on-speculative-decoding-for-multimodal-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  この部分は小バッチ時にメモリ帯域が律速になりやすく、画像理解モデルであっても文章LLMと同じ問題を抱える。従来の投機的復号では、小型モデルが数トークンを予測し、大型モデルがその候補を一括検証する。論文の最大2.37倍は、メモリ律速を仮定して計算した高速化指標（MBSU）であり、実際に計測したトークン率の倍率と混同してはならない。

- **2024-02 · [Recursive Speculative Decoding: Accelerating LLM Inference via Sampling Without Replacement](2024-2402.14160-recursive-speculative-decoding-accelerating-llm-inference-via-sampling-w.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  投機的復号は小さいドラフトモデルで先のトークンを予測し、大きい対象モデルにまとめて検証させることで、対象モデルの逐次実行回数を減らす。Llama 2-7Bと115Mドラフトを使ったXSumの評価では、通常の逐次復号37.269トークン/秒に対し、RSD-Cの2-2分岐は56.609トークン/秒を報告する。

- **2024-10 · [ParallelSpec: Parallel Drafter for Efficient Speculative Decoding](2024-2410.05589-parallelspec-parallel-drafter-for-efficient-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  投機的復号（投機的復号）は、小さな下書きモデルが複数トークンの候補を作り、大きな対象モデルがまとめて検証することで、大きなモデルを毎トークン実行する費用を減らす。

- **2024-10 · [A Theoretical Perspective for Speculative Decoding Algorithm](2024-2411.00841-a-theoretical-perspective-for-speculative-decoding-algorithm.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  小型モデルが候補トークンを提案し、大型モデルが並列に検証する方式では、候補が多く受理されるほど大型モデルの逐次呼出しが減る。定理3は複数のドラフト列を同時に検証するバッチ方式の不偏性と改善量を与える。

- **2024-10 · [AMUSD: Asynchronous Multi-Device Speculative Decoding for LLM Acceleration](2024-2410.17375-amusd-asynchronous-multi-device-speculative-decoding-for-llm-acceleratio.md)**  
  実装：[✓](https://github.com/BradMcDanel/AMUSD) ・ リポジトリ内被引用：6  
  二つのモデルを別々のGPUへ配置しても、この実行順序を変えなければGPUを同時に使い切れない。平均トークン時間は、自己回帰生成に対してHumanEvalで1.57倍、MT-Benchで1.31倍、RefactorChatで1.96倍の高速化となった。

- **2024-04 · [BASS: Batched Attention-optimized Speculative Sampling](2024-2404.15778-bass.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  系列ごとに異なる投機受理長を保ったまま注意計算をバッチ化し、動的ドラフト長調整で複数応答の遅延とGPU利用率を改善する方式。

- **2024-05 · [Nearest Neighbor Speculative Decoding for LLM Generation and Attribution](2024-2405.19325-nearest-neighbor-speculative-decoding-for-llm-generation-and-attribution.md)**  
  実装：[✓](https://github.com/facebookresearch/NEST) ・ リポジトリ内被引用：4  
  対象：外部コーパスの根拠に基づく生成と複数トークンの投機的復号を統合する半パラメトリック推論。一次資料はNeurIPS 2024掲載論文のarXiv第3版（2025年4月25日）。標準的な分布保存型の投機的復号と区別する。

- **2024-10 · [QSpec: Speculative Decoding with Complementary Quantization Schemes](2024-2410.11305-qspec-speculative-decoding-with-complementary-quantization-schemes.md)**  
  実装：[✓](https://github.com/hku-netexplo-lab/QSpec) ・ リポジトリ内被引用：3  
  QSPECが解決するのは、4ビット重みの言語モデルを動かす際に、活性化も4ビットへ落とすと演算は軽くなるものの、複数段階の推論やコード生成の正確さが損なわれるという問題である。著者は活性化まで4ビットにした実行経路を候補トークンの提案に限定し、同じ重みを活性化16ビットで計算する経路に採否の最終決定を任せる。

### 4年前（2022-11〜2023-10）

- **2022-11 · [Fast Inference from Transformers via Speculative Decoding](2022-2211.17192-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：348  
  軽量モデルの複数トークン提案を対象モデルで並列検証し、出力分布を変えずに直列復号回数を削減する投機的復号の基礎研究。

- **2023-02 · [Accelerating Large Language Model Decoding with Speculative Sampling](2023-2302.01318-speculative-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：265  
  小型モデルの複数候補を大型モデルで並列検証し、出力分布を変えず700億パラメータモデルのデコードを最大約2.5倍高速化。

- **2023-05 · [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)**  
  実装：[✓](https://github.com/flexflow/FlexFlow) ・ リポジトリ内被引用：131  
  SpecInferは、小型モデル群が先に作る複数候補を共通接頭辞の木へまとめ、対象LLMを1回で木構造検証することで、逐次デコードの対象重み読出しとGPU間通信を減らし、複数トークンを確定する。

- **2023-09 · [Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding](2023-2309.08168-draft-verify.md)**  
  実装：[✓](https://openreview.net/attachment?id=ACC2nQYzPYS&name=software) ・ リポジトリ内被引用：90  
  元モデルの中間層を一時的に飛ばして下書きを生成し、完全モデルで一括検証することで、追加下書きモデルなしに最大約2倍の損失なしデコード高速化を実現する。

- **2023-08 · [Accelerating LLM Inference with Staged Speculative Decoding](2023-2308.04623-accelerating-llm-inference-with-staged-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：51  
  本研究は投機的復号（投機的復号）の候補を一本の直線ではなく木構造へ広げ、さらに小型のドラフトモデルも別の極小モデルで投機実行する「段階投機的復号」を提案する。段階投機は通常比3.16倍、標準投機比1.36倍である。

- **2023-02 · [Speculative Decoding with Big Little Decoder](2023-2302.07863-speculative-decoding-with-big-little-decoder.md)**  
  実装：[✓](https://github.com/kssteven418/BigLittleDecoder) ・ リポジトリ内被引用：46  
  Big Little Decoder（BiLD）は、小型モデルに自己回帰生成を任せ、予測が難しいときだけ大型モデルへフォールバックする。大型モデルは小型モデルが直前まで作った区間をまとめて評価し、不一致が大きい位置までロールバックして修正する。mT5/T5の翻訳・要約でNVIDIA T4上最大2.12倍高速化する。

- **2023-10 · [SpecTr: Fast Speculative Decoding via Optimal Transport](2023-2310.15141-spectr-fast-speculative-decoding-via-optimal-transport.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  大規模言語モデルの通常の自己回帰復号は、次のトークンを一つ出すたびに大きなモデルの前向き計算を必要とする。投機的復号（投機的復号）は小さな下書きモデルで将来のトークン列を先に作り、大きな検証モデルでまとめて採否を調べる。採択されたトークンを一度の検証で複数確定できれば、利用者が一つの回答を受け取るまでの時間を短縮できる。

- **2023-10 · [SPEED: Speculative Pipelined Execution for Efficient Decoding](2023-2310.12072-speed-speculative-pipelined-execution-for-efficient-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  周期的に同じ重みを繰り返し使用する復号器で、途中層から未来トークンを先読みし、複数の系列位置を同一の重み行列で並行処理する。投機予測が変わったときは後続処理と鍵・値キャッシュを巻き戻し、深い共有モデルの出力を維持する。

### 5年前（2021-11〜2022-10）

- **2022-03 · [Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation](2022-2203.16487-speculative-decoding-exploiting-speculative-execution-for-accelerating-s.md)**  
  実装：[✓](https://github.com/hemingkx/SpecDec) ・ リポジトリ内被引用：37  
  提案の中核は、入力を読むエンコーダを深く、反復生成するデコーダを浅くした独立の候補生成モデル「Spec-Drafter」と、候補を対象モデルでまとめて確かめる「Spec-検証」である。
<!-- survey:auto:end -->
