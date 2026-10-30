# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（338本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/05-speculative-decoding-moe/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [DFlash: Block Diffusion for Flash Speculative Decoding](2026-2602.06036-dflash-block-diffusion-for-flash-speculative-decoding.md)**  
  実装：[✓](https://github.com/z-lab/dflash) ・ リポジトリ内被引用：74  
  対象 隠れ featuresで条件付けしたblock-diffusion drafterが候補列を1回で並列生成し、投機ドラフト自身の逐次待ちを除くDFlash。

- **2026-07 · [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](2026-2607.05147-dspark-confidence-scheduled-speculative-decoding.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSpec) ・ リポジトリ内被引用：35  
  並列ドラフトの後半受理率低下を軽量な逐次ヘッドで抑え、較正した接頭辞生存確率と実機処理能力から検証長を負荷適応で配分し、実トラフィックで同等処理能力時のユーザー当たり生成速度を57〜85%改善する。

- **2026-05 · [Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding](2026-2605.29707-domino-speculative-decoding.md)**  
  実装：[✓](https://github.com/jianuo-huang/Domino) ・ リポジトリ内被引用：25  
  並列ドラフトが弱めるトークン間の依存を、軽量GRUと低ランク補正で戻す投機的デコード方式。Qwen3評価では受理長と生成速度を改善したが、要旨の最大5.8倍は本文表の条件と対応づけられない。

- **2026-04 · [Accelerating Speculative Decoding with Block Diffusion Draft Trees](2026-2604.12989-accelerating-speculative-decoding-with-block-diffusion-draft-trees.md)**  
  実装：[✓](https://github.com/liranringel/ddtree) ・ リポジトリ内被引用：24  
  DFlashが1回で得た位置別確率分布から高確率な複数接頭辞をDDTreeとして組み、1回の対象モデル検証で複数経路を試して単一路径投機より受理長と速度を高める。

- **2025-11 · [SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding](2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-de.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  投機的復号は、小さなドラフターが先のトークンを提案し、大きな検証器が複数位置をまとめて評価することで自己回帰生成の待ち時間を減らす。Qwen2.5-72BのHumanEvalでは通常復号比で最大5.51倍、70B級の複数課題ではおおむね約4倍の速度改善を報告する。

- **2026-01 · [DART: Diffusion-Inspired Speculative Decoding for Fast LLM Inference](2026-2601.19278-dart-diffusion-inspired-speculative-decoding-for-fast-llm-inference.md)**  
  実装：[✓](https://github.com/fvliang/DART) ・ リポジトリ内被引用：19  
  対象LLM特徴から未来ロジットを1回で並列予測しN-gram木刈り込みを行い、EAGLE3より平均約30%高い投機デコード高速化を得る。

- **2026-01 · [TALON: Confidence-Aware Speculative Decoding with Adaptive Token Trees](2026-2601.07353-talon-confidence-aware-speculative-decoding-with-adaptive-draft-length.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  投機木の形をあらかじめ「幅10・深さ8」のように固定すると、簡単な箇所では深さが足りず、難しい箇所では大量の枝を作って捨てる。TALONは総ノード数だけを固定し、ドラフトモデルの確信度に応じて予算を深さと幅へその場で配分する。

- **2026-05 · [D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting](2026-2605.18810-d-pace.md)**  
  実装：[✓](https://github.com/Lucas-TY/D-PACE) ・ リポジトリ内被引用：13  
  並列投機ドラフタで、受理接頭辞長への位置別寄与から交差エントロピー重みを毎例動的に計算し、固定位置減衰より受理長と実測高速化を改善する。

- **2025-12 · [Speculative Decoding: Performance or Illusion?](2026-2601.11580-speculative-decoding-performance-or-illusion.md)**  
  実装：[✓](https://github.com/orgs/SpecDecode-Bench/repositories) ・ リポジトリ内被引用：13  
  実運用向けvLLMで主要投機的復号を横断評価し、検証支配・バッチ依存・受理変動と理論上限との差を定量化。

- **2026-03 · [Speculative Speculative Decoding](2026-2603.03251-speculative-speculative-decoding.md)**  
  実装：[✓](https://github.com/tanishqkumar/ssd) ・ リポジトリ内被引用：12  
  検証中に受理長と補正トークンを複数予測し、その各結果に続く次ラウンドのドラフトを別GPUで先行生成することで、投機的デコードに残るドラフト待ちを隠す方式。

- **2026-05 · [ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios](2026-2604.09603-echo.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  高同時実行時の投機的デコードを固定検証予算の配分問題として扱い、信頼度の高い深さだけで候補木を伸縮し、バッチ内要求間で予算を再配分するSGLang統合方式。

- **2026-02 · [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  MoE-Specは、候補木全体のルータ確率を層ごとに合算して専門家を予算B個へ絞り、各枝をその集合内で再選択して、木の拡大による検証重み読出しを抑える。

- **2025-11 · [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  MoE-SpeQは、対象MoEの4ビット版を下書きにして候補トークンと専門家経路を先に予測し、必要重みを検証前に読み込み、圧縮カーネルで転送と計算の待ちを減らす。

- **2026-06 · [JetSpec: Breaking the Scaling Ceiling of Speculative Decoding with Parallel Tree Drafting](2026-2606.18394-jetspec-breaking-the-scaling-ceiling-of-speculative-decoding-with-parall.md)**  
  実装：[✓](https://github.com/hao-ai-lab/JetSpec) ・ リポジトリ内被引用：9  
  自己回帰型言語モデルは次トークンを逐次生成するため、出力長が伸びるほど復号遅延が蓄積する。投機的復号は小さなドラフト器が複数トークンを提案し、対象モデルがまとめて検証することで対象モデルの逐次順伝播回数を減らす。木予算256、貪欲復号設定のMATH-500では自己回帰復号比9.64倍、平均受理長10.76を報告する。

- **2026-06 · [DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding](2026-2606.02091-dflare.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：9  
  ブロック拡散ドラフトの各層へ異なる標的層混合を注入し、ドラフト深さ・標的知識・学習データを拡張して受理長と実時間高速化を伸ばす。

- **2026-02 · [P-EAGLE: Parallel-Drafting EAGLE with Scalable Training](2026-2602.01469-p-eagle-parallel-drafting-eagle-with-scalable-training.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  投機的復号は軽いドラフトモデルが先に複数トークンを提案し、大きな対象モデルがまとめて検証することで、対象モデルの重みを読む回数を減らす。vLLMでの実測では、GPT-OSS 20B、120B、Qwen3-Coder 30Bに対し、自己回帰EAGLE-3比で代表的に1.10〜1.36倍の生成処理量改善を報告する。

- **2026-01 · [Double: Breaking the Acceleration Limit via Double Retrieval Speculative Parallelism](2026-2601.05524-double-breaking-the-acceleration-limit-via-double-retrieval-speculative-.md)**  
  実装：[✓](https://github.com/Sylvan820/Double1) ・ リポジトリ内被引用：8  
  Doubleは、並列投機的復号（Parallel 投機的復号; PSD）における二つの性能制約を同時に解く。この方式は、ドラフト用の追加学習を必要としない。原著の8基のNVIDIA A100 80GBによる実験では、LLaMA3.3-70BのHumanEvalで通常のターゲット推論に対して5.33倍、Qwen3-32Bでは2.84倍の実時間高速化を示す。

- **2026-05 · [Draft Less, Retrieve More: Hybrid Tree Construction for Speculative Decoding](2026-2605.20104-draft-less-retrieve-more-hybrid-tree-construction-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  動的剪定は投機木を速くするが、剪定した枝の中に本来受理できる候補があれば平均受理長が落ちる。Graftは剪定で空いた候補枠を捨てず、対象モデルの過去検証から得た安価な検索候補で「接ぎ木」する。対象モデルが一度に検証するノード総数は増やさず、ドラフト計算だけを安い検索へ置換する。

- **2025-11 · [SPECVLM: Enhancing Speculative Decoding of Video LLMs via Verifier-Guided Token Pruning](2025-6ac6253cc798-specvlm-enhancing-speculative-decoding-of-video-llms-via-verifier-guided.md)**  
  実装：[✓](https://github.com/zju-jiyicheng/SpecVLM) ・ リポジトリ内被引用：6  
  削るべきトークンをターゲットのlanguage-to-video 注意機構から決め、まず重要度の高いトークンを累積注意量に基づいて残し、残りを空間的に均一に間引く。

- **2025-11 · [DSD: A Distributed Speculative Decoding Solution for Edge-Cloud Agile Large Model Serving](2025-2511.21669-dsd-distributed-edge-cloud-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  端末側下書きモデルとクラウド側目標モデルによる分散投機的復号をDSD-Simでモデル化し、学習型の適応窓制御で投機窓幅を調整して処理量を最大9.7%向上する。

- **2026-07 · [LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation](2026-df65c3a3c97c-logitspec-accelerating-retrieval-based-speculative-decoding-via-next-nex.md)**  
  実装：[✓](https://github.com/smart-lty/LogitSpec) ・ リポジトリ内被引用：5  
  投機的デコードは、軽い下書き側が将来トークン候補を提案し、大きなtargetモデルが複数候補を一度の順伝播で検証する。target分布を保つ検証規則を使えば、逐次生成と同じ出力分布を維持したまま1回のtarget 順伝播で複数トークンを確定できる。

- **2026-07 · [D-cut: Adaptive Verification Depth Pruning for Batched Speculative Decoding](2026-2607.14647-d-cut-adaptive-verification-depth-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  投機的復号は小さなドラフト器が複数トークンを先に提案し、大きな対象モデルがまとめて検証することで逐次実行回数を減らす。高並行条件では長ドラフト基準の自己回帰復号比平均高速化率1.26倍を1.65倍へ引き上げ、30個のモデル・課題組合せ中29個で改善した。

- **2026-06 · [TreeFlash: Parallel AR-Approximation for Faster Speculative Decoding](2026-2606.03819-treeflash-parallel-ar-approximation-for-faster-speculative-decoding.md)**  
  実装：[✓](https://github.com/ETH-DISCO/TreeFlash) ・ リポジトリ内被引用：5  
  投機的復号（投機的復号）は、軽量なドラフター（drafter）が複数の候補トークンを先に提案し、重い対象モデル（対象モデル）がまとめて検証することで、対象モデルの逐次呼び出し回数を減らす。

- **2026-03 · [KNN-SSD: Enabling Dynamic Self-Speculative Decoding via Nearest Neighbor Layer Set Optimization](2026-4d6bf2312451-knn-ssd-enabling-dynamic-self-speculative-decoding-via-nearest-neighbor-.md)**  
  実装：[✓](https://github.com/mbsong/KNN-SSD) ・ リポジトリ内被引用：5  
  KNN-SSDは、同一LLMの一部層を飛ばす自己投機的復号で、入力ドメインが変わると固定skip-層集合の受理率・速度が悪化する問題を扱う。ドメイン別の最適skip集合をBayesian Optimizationで事前探索し、最後の隠れ状態をK-meansで代表化したアンカーへのKNN類似度から入力ごとに集合を選ぶ。

- **2026-02 · [SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding](2026-2604.09557-speed-bench-speculative-decoding-benchmark.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  投機的復号を意味多様性・入力長・エントロピー・並列度の軸で統一評価し、合成入力の平均23%過大評価やバッチ依存の最適ドラフト長など、従来ベンチマークの順位偏りを明らかにする。

- **2026-02 · [Speculative Decoding with a Speculative Vocabulary](2026-2602.13836-speculative-decoding-with-a-speculative-vocabulary.md)**  
  実装：[✓](https://github.com/SamsungLabs/SpecVocab) ・ リポジトリ内被引用：5  
  SpecVocabは、投機的復号（投機的復号）の小型ドラフトモデルが次のトークンを予測する際、語彙全体への出力射影を行わず、文脈ごとに予測した候補語だけを精密計算する手法である。Qwen3 8BのSpec-Benchでは、再現したEAGLE-3の平均受理長4.78から5.01へ、平均スループット235.1から245.2トークン/秒へ改善した。

- **2026-02 · [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)**  
  実装：[✓](https://github.com/lshAlgorithm/MoE-SpAc) ・ リポジトリ内被引用：5  
  MoE-SpAcは、投機的復号で先に見える専門家需要を集計し、VRAMに残す専門家・先読みする重み・CPUで計算する専門家を制約付きで同時に配置して、端末の転送待ちを減らす。

- **2026-07 · [Trees from Marginals: Autoregressive drafting with factorized priors](2026-2607.06763-trees-from-marginals-autoregressive-drafting-with-factorized-priors.md)**  
  実装：[✓](https://github.com/trymirai/sglang) ・ リポジトリ内被引用：4  
  Trees from Marginals（DFlash-TfM）は、未来の複数トークンを並列に予測する周辺分布型の下書き器DFlashと、直前に選択した下書きトークンに条件付ける小型自己回帰器Weaverを接続した投機的復号方式である。

- **2026-07 · [SelfJudge: Faster Speculative Decoding via Self-Supervised Judge Verification](2026-2510.02329-selfjudge-faster-speculative-decoding-via-self-supervised-judge-verifica.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  通常の投機的復号（投機的復号）は、小さな草稿モデルが複数トークンを先読みし、大きなターゲットモデルが一度の順伝播でまとめて検証する。増加率はそれぞれ23.5%と46.3%である。

- **2026-07 · [DeLS-Spec: Decoupled Long-Short Contexts for Parallel Speculative Drafting](2026-2607.07409-dels-spec-decoupled-long-short-contexts-for-parallel-speculative-draftin.md)**  
  実装：[✓](https://github.com/dt-3t/DeLS-Spec) ・ リポジトリ内被引用：4  
  投機的復号（投機的復号）は、軽量なドラフトモデルで複数の候補トークンを先に生成し、目標モデルの一度の前向き計算で並列検証することで自己回帰生成の逐次呼出しを減らす。Qwen3-4Bの温度0、8ベンチマーク平均では、DFlashの自己回帰比復号高速化4.63倍・平均受理長6.04から、DeLS-Specは4.82倍・6.35へ改善した。

- **2026-05 · [Draft-OPD: On-Policy Distillation for Speculative Draft Models](2026-2605.29343-draft-opd.md)**  
  実装：[✓](https://github.com/haodilei/Draft-OPD) ・ リポジトリ内被引用：4  
  投機的復号の検証で露出したドラフト誤り位置から提案を再生し、教師分布でオンポリシー蒸留することで受理長と無損失推論速度を高める。

- **2026-04 · [Self-Speculative Decoding for On-device MoE Acceleration](2025-self-speculative-decoding-for-on-device-moe-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  少数の経路選択専門家だけで同じMoE自身をドラフト化し、GPUを専門家キャッシュとして生成・検証間で再利用することで、CPU退避を伴う端末MoE復号を最大3.72倍高速化する。

- **2025-12 · [Towards Efficient Agents: A Co-Design of Inference Architecture and System](2025-2512.18337-towards-efficient-agents-a-co-design-of-inference-architecture-and-syste.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  AgentInferは、長い推論と外部ツール呼出しを繰り返すLLMエージェントの効率を、単一の生成呼出しのトークン/秒ではなく、目的を達成するまでの総所要時間・総トークン消費・タスク成功率で評価し、推論アーキテクチャと提供システムを共同設計する枠組みである。

- **2026-08 · [LiLiCorr: Lightweight Likelihood Correlation of Parallel Drafts for Speculative Decoding](2026-2608.20530-lilicorr-lightweight-likelihood-correlation-of-parallel-drafts-for-specu.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号（投機的復号）は、軽量なドラフト器が未来の複数トークンを予測し、大きな対象モデルがまとめて検証することで、対象モデルの逐次実行回数を減らす。競合方式に対して処理率が明確に最良だったのは63条件、測定誤差1%以内の同率が6条件、劣ったのが3条件である。

- **2026-08 · [DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees](2026-2608.13524-dartree-speculative-diffusion-decoding-with-autoregressive-draft-trees.md)**  
  実装：[✓](https://github.com/VILA-Lab/DARTree) ・ リポジトリ内被引用：3  
  投機的復号では軽量な提案器が複数の候補トークンを作り、大きな目標モデルがまとめて検証する。Qwen3-4B、温度0、GSM8Kでは平均受理長12.97トークン、同一環境で測定した通常自己回帰復号に対して9.73倍の復号速度向上を報告する。

- **2026-07 · [HeteroSpec: Leveraging Contextual Heterogeneity for Efficient Speculative Decoding](2026-2505.13254-heterospec-leveraging-contextual-heterogeneity-for-efficient-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  自己回帰型の大規模言語モデルは出力トークンを逐次生成するため、出力が長くなると毎トークンの前向き計算が遅延を支配する。投機的復号（投機的復号）は、小さなドラフトモデルが先に複数トークンを予測し、大きなターゲットモデルがまとめて検証することで逐次計算回数を減らす。

- **2026-07 · [AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding](2026-2607.25852-angelspec.md)**  
  実装：[✓](https://github.com/Tencent/AngelSpec) ・ リポジトリ内被引用：3  
  会話には短い多トークン予測、コード・数学には並列草稿DFlyを使い分け、実行時負荷に応じて検証深度も動的調整する推測デコード基盤。

- **2026-05 · [PipeSD: An Efficient Cloud-Edge Collaborative Pipeline Inference Framework with Speculative Decoding](2026-2605.13319-pipesd.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号は小型モデルが複数トークンを先に提案し、大型モデルがまとめて検証することで自己回帰生成を高速化する。

- **2026-05 · [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  一覧用要約：EVICTは混合専門家モデル（MoE）の木構造投機的復号で、下書き確率から見積もった期待確定トークン数を、事前測定した検証ステップ時間で割る効用を最大化するよう検証木の接頭部分を選び、不要な専門家起動を抑える。SGLangのCUDAグラフに統合し、出力分布を変えずに復号速度を改善する。

- **2026-04 · [Multi-Drafter Speculative Decoding with Alignment Feedback](2026-2604.05417-multi-drafter-speculative-decoding-with-alignment-feedback.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号（投機的復号）は小さなドラフトモデルが先のトークン列を予測し、対象モデルがまとめて検証することで逐次呼出し回数を減らす。

- **2026-04 · [DIVERSED: Relaxed Speculative Decoding via Dynamic Ensemble Verification](2026-2604.07622-diversed-relaxed-speculative-decoding-via-dynamic-ensemble-verification.md)**  
  実装：[✓](https://github.com/comeusr/diversed) ・ リポジトリ内被引用：3  
  投機的復号（投機的復号）は、小型のドラフトモデルが複数トークンを先読みし、大型の対象モデルがそれらをまとめて検証することで、逐次生成の待ち時間を短縮する。

- **2026-02 · [Vegas: Self-Speculative Decoding with Verification-Guided Sparse Attention](2026-2602.07223-specattn-sparse-attention-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/platformxlab/vegas) ・ リポジトリ内被引用：3  
  検証で得た注意ロジットを次の疎な候補生成へ再利用し、鍵値選択の追加走査を抑えながら損失なし自己投機復号を高速化する。

- **2026-02 · [HSD: Training-Free Acceleration for Document Parsing Vision-Language Models with Hierarchical Speculative Decoding](2026-2602.12957-hsd-training-free-acceleration-for-document-parsing-vision-language-mode.md)**  
  実装：[✓](https://github.com/whlscut/HSD) ・ リポジトリ内被引用：3  
  文書画像をMarkdownや構造化テキストへ変換する視覚言語モデルは、表・数式・本文・読順を一貫して扱えるが、長いページの結果を自己回帰的に1トークンずつ生成するため、出力が長いほど遅延が増える。著者らはこの二つの方式を競合関係とせず、軽量パイプラインの領域下書きを、強力な視覚言語モデルで段階的に検証する方式を提案する。

- **2026-01 · [Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding](2026-2601.05724-overcoming-joint-intractability-with-lossless-hierarchical-speculative-d.md)**  
  実装：[✓](https://github.com/ZhouYuxuanYX/Hierarchical-Speculative-Decoding) ・ リポジトリ内被引用：3  
  HSDは利用可能な草案の枝だけから局所的な確率質量を計算し、階層をまたいで過不足を補正することで、この問題を回避する。主要実験はQwen2.5-0.5Bを草案とし、14B・32B・72Bを目標に使った比較で、トークン単位検証に対する復号速度の平均改善は約6.7%、一部条件では11%前後に達した。

- **2025-11 · [Collaborative Large Language Model Inference via Resource-Aware Parallel Speculative Decoding](2025-2511.01695-collaborative-large-language-model-inference-via-resource-aware-parallel.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号（投機的復号）は、小さなドラフトモデルが複数トークンを先に生成し、大きなターゲットモデルがまとめて検証することで、出力品質を維持しながら生成の待機時間を短縮することを目指す。

- **2026-09 · [DFlow: Enabling Verifier Information Flow in Block Diffusion Speculative Decoding](2026-2609.06498-dflow-verifier-information-flow-block-diffusion.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  検証済みだが棄却された後続位置の対象モデル中間表現を次の投機生成回へ再利用し、対象モデルの追加計算なしでブロック拡散型投機的復号の平均受理長を約10〜13%改善する。

- **2026-08 · [Verification-Aware Training for Speculative Decoding](2026-2608.30135-verification-aware-training-for-speculative-decoding.md)**  
  実装：[✓](https://github.com/naver-ai/VAT) ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は、軽量な草案モデルが先の複数トークンを提案し、大きな目標モデルが一度の前向き計算でそれらを検証することで自己回帰生成の遅延を減らす。NVIDIA A100 80GB上で、EAGLE-3と拡散型のDFlash、目標モデルQwen3-4B、Qwen3-8B、Llama-3.1-8Bを組み合わせ、数学・コード・会話の八課題で評価した。

- **2026-08 · [S2-MoE: Enabling Efficient Self-Speculative Decoding for Mixture-of-Experts on Edge Devices](2026-2608.15018-s2-moe-self-speculative-decoding-edge.md)**  
  実装：[✓](https://github.com/angerybob/S2-MoE) ・ リポジトリ内被引用：2  
  エッジ向けMoEで、専門家再利用を考慮した投機展開・ゲーティング・文脈共有を組み合わせ、専門家読み出しを抑えながら自己投機的復号を高速化する。

- **2026-08 · [From Chains to Trees: Parent-Conditioned Drafting for Semi-Autoregressive Speculative Decoding](2026-2608.02123-from-chains-to-trees-parent-conditioned-drafting-for-semi-autoregressive.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの逐次生成は、直前のトークンを確定しなければ次を計算できないため、GPUの並列演算能力を十分に使いにくい。投機的復号（投機的復号）は小さな草案モデルに先のトークンを予測させ、目標モデルがまとめて検証する。しかし草案が一本の列だと、序盤のトークンが棄却された瞬間に後続の正しそうな候補も使えなくなる。

- **2026-08 · [Bole: Efficient Tree Speculation for Hybrid-Attention Language Models](2026-2608.01651-bole-efficient-tree-speculation-for-hybrid-attention-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  再帰型線形注意の木検証を厳密閉形式で並列化し、因子化状態とhardware-aware予算をSGLangへ統合して最大4.72倍のデコード スループットを実現。

- **2026-07 · [Speculative Verification: Exploiting Information Gain for Speculative Decoding](2026-9b451e22fa70-speculative-verification-exploiting-information-gain-for-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的 検証（SV、投機的検証） は、草稿モデルが先読み生成した複数トークンを大きな標的モデルで検証する投機的復号（投機的復号; SD）に、小さな補助モデル（companion モデル）を追加して受理確率を予測し、検証すべきトークン数を動的に選ぶ方式である。

- **2026-07 · [SpecExtend: A Drop-in Enhancement for Speculative Decoding of Long Sequences](2026-specextend.md)**  
  実装：[✓](https://github.com/jycha98/SpecExtend) ・ リポジトリ内被引用：2  
  対象モデルの注意重みでドラフト側KVキャッシュの重要文脈を動的選択し、再学習なしで長文の投機的復号を高速化する拡張。

- **2026-07 · [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は、軽量な下書きモデルが先のトークン候補を生成し、対象モデルが複数候補を一括検証することで、自己回帰生成の逐次的な待ち時間を減らす。対象モデルの検証規則は変更しないため、下書きの選び方を変えても、標準の投機的復号が持つ出力分布の保存を維持できる。

- **2026-06 · [PRESTO: Prefix-Aligned Tree Drafting for Diffusion Speculative Decoding](2026-2607.22634-presto-prefix-aligned-tree-drafting-for-diffusion-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は、軽量な草稿モデル（下書きモデル）で将来のトークン候補を生成し、大きな対象モデル（対象モデル）でまとめて検証することで、対象モデルの出力品質を維持しながら生成速度を上げる技術である。

- **2026-05 · [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)**  
  実装：[✓](https://github.com/sgl-project/sglang/pull/22272) ・ リポジトリ内被引用：2  
  SPECTREは、余った小型モデルGPUを遠隔下書き器として大型モデルの検証に再利用し、下書きと検証を直列・並列の間で切り替えて、通信待ちとロールバックを抑える。

- **2026-05 · [SpecBlock: Block-Iterative Speculative Decoding with Dynamic Tree Drafting](2026-2605.07243-specblock-block-iterative-speculative-decoding-with-dynamic-tree-draftin.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は小型の草稿モデルが複数の候補トークンを先に提案し、目標モデルがそれらを一度の前向き計算で検証する。論文の主要な速度比較は、単一NVIDIA A100-80GB、バッチ1で行われた。

- **2026-05 · [FlexDraft: Flexible Speculative Decoding via Attention Tuning and Bonus-Guided Calibration](2026-2605.20022-flexdraft-flexible-speculative-decoding-via-attention-tuning-and-bonus-g.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FlexDraftは、大規模言語モデル（LLM）の投機的復号（投機的復号）において、ドラフト生成と対象モデルの検証を重ねる並列方式と、確定結果を待ってからドラフトを生成する逐次方式を、バッチサイズに応じて使い分ける枠組みである。Qwen3-8BをA100で評価した原著表2の5タスク平均は、自己回帰生成に対して4.59倍の高速化となる。

- **2026-04 · [ToolSpec: Accelerating Tool Calling via Schema-Aware and Retrieval-Augmented Speculative Decoding](2026-2604.13519-toolspec-accelerating-tool-calling-via-schema-aware-and-retrieval-augmen.md)**  
  実装：[✓](https://github.com/hemingkx/ToolSpec) ・ リポジトリ内被引用：2  
  大規模言語モデルが検索や計算などの外部ツールを使う際には、ツール自体の処理だけでなく、関数名・引数名・引数値を含む呼び出し文字列を生成する時間もかかる。ToolBenchを用いたQwen2.5-14B-Instructの予備調査では、呼び出し文字列の生成が処理全体の遅延の約80%を占め、外部ツールの実行時間の約4倍だった。

- **2026-03 · [A Pipelined Collaborative Speculative Decoding Framework for Efficient Edge-Cloud LLM Inference](2026-2603.19133-picospec-edge-cloud-pipelined-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  端末の候補生成とクラウド検証を非同期に重ね、棄却用確率分布を疎圧縮してネットワーク往復を隠すことで、端末・クラウド協調推論を最大2.9倍高速化する。

- **2026-01 · [WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching](2026-2601.11652-wisp-distributed-speculative-serving-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  WISPは、エッジで最初の棄却位置を予測して下書きを止め、サーバーでSLO余裕と検証時間から異種要求をバッチ分離し、無駄計算と干渉を減らす。

- **2026-01 · [TABED: Test-Time Adaptive Ensemble Drafting for Robust Speculative Decoding in LVLMs](2026-2601.20357-tabed-test-time-adaptive-ensemble-drafting-for-robust-speculative-decodi.md)**  
  実装：[✓](https://github.com/furiosa-ai/TABED) ・ リポジトリ内被引用：2  
  TABED（Test-Time 適応的 Ensemble Drafting）は、画像と文章を処理する大規模視覚言語モデル（LVLM）の出力生成を速くするための、実行時適応型の投機的復号方式である。

- **2025-12 · [Parallel Token Prediction for Language Models](2025-2512.21323-parallel-token-prediction-for-language-models.md)**  
  実装：[✓](https://github.com/mandt-lab/ptp) ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は小さなモデルに先読みさせて大きなモデルでまとめて検証するが、草案モデル自身が1トークンずつ順次生成する費用は残る。Vicuna-7Bを教師として学習したPTPは、RTX A6000単体でSpecBenchの6種類の文章生成課題において、通常の自己回帰生成比で平均2.40倍の実時間高速化を報告した。

- **2025-12 · [Fail Fast, Win Big: Rethinking the Drafting Strategy in Speculative Decoding via Diffusion LLMs](2025-2512.20573-fail-fast-win-big-rethinking-the-drafting-strategy-in-speculative-decodi.md)**  
  実装：[✓](https://github.com/ruipeterpan/failfast) ・ リポジトリ内被引用：2  
  生成がメモリ帯域に制約される場面では、各トークンのために大きなモデルを繰り返し実行することが遅延の原因となる。投機的復号（投機的復号）は小さな草稿モデルが複数トークンを先に提案し、大きな対象モデルがそれらをまとめて検証することで、この反復回数を減らす。

- **2025-11 · [Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Minimization](2025-2511.15898-global-resolution-optimal-multi-draft-speculative-sampling-via-convex-mi.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Global Resolutionは、複数の草案トークンを同じ次トークン位置に提示する投機的サンプリングに対し、目標モデルの出力分布からの逸脱を制御しながら、草案のいずれかを受理できる確率を最大化する検証規則を計算する研究である。語彙数をVとすると候補n組の数はVのn乗であり、n=2でも通常の大語彙では汎用ソルバーで解けない。

- **2025-11 · [Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits](2025-2511.11346-fast-and-expressive-multi-byte-prediction-with-probabilistic-circuits.md)**  
  実装：[✓](https://github.com/april-tools/mtpc) ・ リポジトリ内被引用：2  
  本論文は、バイト単位の大規模言語モデルで複数の将来バイトを同時に予測する際、予測位置間の依存関係と候補生成の遅延を同時に制御する確率回路方式MtPCを提案する。

- **2026-09 · [RheoSampling: Resolving the One-Hot Dilemma in Stochastic Dynamic-Tree Speculative Decoding](2026-2609.21827-rheosampling-resolving-the-one-hot-dilemma-in-stochastic-dynamic-tree-sp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  木型投機的復号（tree-based 投機的復号）は、小型ドラフトモデルが複数の候補トークン列を木として用意し、大型ターゲットモデルがその木をまとめて検証することで、自己回帰復号の一段ずつの待機を減らす。

- **2026-09 · [Draft in Parallel, Condition Through Depth: Adjacent Causal Injection for Speculative Decoding](2026-2609.36173-draft-in-parallel-condition-through-depth-adjacent-causal-injection-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、軽量な下書き器が候補トークン列を提案し、対象LLMが一括検証する。Qwen3-8Bの7課題、温度0での平均受理長は、DFlashの3.77トークン/回からDSpineの4.82トークン/回へ増加し、相対改善率は27.8%となる。

- **2026-09 · [Carryover Drafting: Recycling Rejected States for Speculative Decoding](2026-2609.14717-carryover-drafting-recycling-rejected-states.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  検証済みだが棄却されたターゲット隠れ状態を次回ドラフトの一時KV文脈へ再利用し、追加投影器なしで受理長を6.5〜14.7%改善する。

- **2026-09 · [ASPIRE: Asynchronous Batched Self-Speculative Decoding for Long-Context LLM Inference](2026-2609.17943-aspire-asynchronous-batched-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/Amir-zsh/ASPIRE) ・ リポジトリ内被引用：1  
  下書き・検証混在順伝播、要求別オンライン制御、下書き内の鍵値文脈更新により長文脈自己投機復号を最大4.58倍高速化する。

- **2026-08 · [TreeSpark: Calibrated, Load-Adaptive Draft Trees for Semi-Autoregressive Speculative Decoding](2026-2609.22098-treespark-calibrated-load-adaptive-draft-trees-for-semi-autoregressive-s.md)**  
  実装：[✓](https://github.com/PopSoda2002/TreeSpark) ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さな提案モデルが複数トークンを予測し、大きな目標モデルがまとめて検証することで、目標モデルの逐次呼び出しを減らす。原著の固定ノード数実験では、Qwen3-4B/8B/14Bのいずれも同じ検証ノード数のDDTreeより目標モデル1回当たりの受理トークン数が9〜16%増えた。

- **2026-08 · [Pre-Compiled Pipeline Shards for Distributed LLM Inference on Intel AI PC Fleets](2026-2608.19147-pre-compiled-pipeline-shards-for-distributed-llm-inference-on-intel-ai-p.md)**  
  実装：[✓](https://github.com/labscommunity/pipeline-sharded-inference-paper) ・ リポジトリ内被引用：1  
  本論文は、単独のメモリ容量では700億パラメータ級の大規模言語モデルを保持できない民生用AIパソコンを、通常のネットワーク越しに束ねる分散推論方式を示す。Llama 3.1 8Bの2台構成では、単一利用者の分散実行16.33トークン/秒から、2利用者合計43.97トークン/秒へ改善する。

- **2026-08 · [CURE: Local Uncertainty Repair for Block-Parallel Speculative Decoding](2026-2608.00531-cure-local-uncertainty-repair-for-block-parallel-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CUREは、大規模言語モデルの投機的復号（投機的復号）において、草案を一度に複数トークン生成する方式の弱点を、少数の修復枝だけで補う推論時の仕組みである。Qwen3-8Bを検証器とする単一GPU実験では、通常の自己回帰復号に比べHumanEvalで3.490倍、MBPPで2.661倍、LiveCodeBench-liteで3.071倍の高速化を報告する。

- **2026-08 · [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さな下書き器が複数の候補トークンを先に生成し、対象となる大規模言語モデルがそれらを一括検証することで、逐次生成の待ち時間を短縮する。

- **2026-07 · [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DraftExpertは、各MoE層に小型の常駐専門家を追加して候補を作り、専門家展開量を予測した枝打ちと非同期先読みを行い、端末の専門家搬送待ちを減らす。

- **2026-07 · [AdaptiveSD A Stability-Aware, Runtime-Adaptive Speculative Decoding Framework with Multi-Policy Orchestration for CPU-Constrained LLM Inference](2026-2607.03876-adaptivesd-runtime-adaptive-cpu-constrained.md)**  
  実装：[✓](https://github.com/sadrasa97/adaptive-speculate-decoding) ・ リポジトリ内被引用：1  
  CPU資源・受理率・遅延・KV圧力を監視し、投機深度を閉ループ制御して資源飽和と遅延変動を抑える適応投機デコード。

- **2026-07 · [A Practical Investigation of Training-free Relaxed Speculative Decoding](2026-2607.08690-a-practical-investigation-of-training-free-relaxed-speculative-decoding.md)**  
  実装：[✓](https://github.com/graphcore-research/relaxed-spec-dec-repro) ・ リポジトリ内被引用：1  
  本論文は新しい単一の投機的復号アルゴリズムを提案するのではなく、既存の緩和型投機的復号（relaxed 投機的復号）を統一的に定式化し、実際に採用すると何が起こるかを比較する研究である。これに対し緩和型は、あえて検証モデルの分布からずらして受理率を上げ、速度や能力の改善を狙う。

- **2026-06 · [When Is a Draft Accepted? A Theory of Acceptance in Speculative Decoding](2026-2606.30265-when-is-a-draft-accepted-a-theory-of-acceptance-in-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号は、小さい草稿モデルが先のトークン列を提案し、目標モデルが複数位置を並列に検証することで目標モデルの呼び出しを節約する。枝数の増加には検証計算量の増加が伴い、証明書が大きいだけでは高速化を保証しない。

- **2026-06 · [Teaching Diffusion to Speculate Left-to-Right](2026-2606.11552-teaching-diffusion-to-speculate-left-to-right.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、軽い生成器が複数の候補トークンを先に出し、大きな対象モデルが候補列を一度の並列計算で検証することで、対象モデルを逐次実行する回数を減らす。

- **2026-06 · [Speculation at a Distance: Where Edge-Cloud Speculative Decoding Actually Pays Off](2026-2606.25091-speculation-at-a-distance-where-edge-cloud-speculative-decoding-actually.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案の中心は新しいGPUカーネルや推論基盤ではなく、比較対象を明確に分けた解析的な性能・容量の境界条件である。分散方式の論文がcloud ARとの比較で高速化を示していても、同じ下書きモデルをクラウドへ置けるなら同居型SDの方が速い場合がある。

- **2026-06 · [D^2SD: Accelerating Speculative Decoding with Dual Diffusion Draft Models](2026-2606.04446-d-2sd-accelerating-speculative-decoding-with-dual-diffusion-draft-models.md)**  
  実装：[✓](https://github.com/catnanami/D2-SD) ・ リポジトリ内被引用：1  
  通常の投機的復号では軽量なドラフトモデルが先のトークンを提案し、元の大きな対象モデルが一度の前進計算でそれらを検証する。Qwen3-8Bを対象にブロック長16、分岐数4で評価した場合、貪欲復号に対する平均壁時計速度向上はDFlashの4.16倍からD²SDの4.98倍へ増え、平均採用長は5.31から7.05トークンへ伸びた。

- **2026-06 · [AdaPLD: Adaptive Retrieval and Reuse for Efficient Model-Free Speculative Decoding](2026-2606.05742-adapld-adaptive-retrieval-and-reuse-for-efficient-model-free-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  完全一致トークンによる検索が空のときだけ埋め込み類似度検索へ退避し、候補位置を隠れ状態で再順位付けする。Vicuna-v1.3 7B/13B/33BをH20×8・FP16で評価し、入力依存生成の平均速度比2.27/1.98/1.74倍、33Bのコード編集で最大の平均3.10倍を報告。

- **2026-05 · [UniVer: A Unified Perspective for Multi-step and Multi-draft Speculative Decoding](2026-2605.04543-univer-a-unified-perspective-for-multi-step-and-multi-draft-speculative-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号は軽量な草案モデルが次の候補トークンを提案し、大きなターゲットモデルが並列に検証する。受理長のRRSw比改善はモデルと木形状により4.2～8.5%で、トークン毎秒が同じ割合で必ず増えるという意味ではない。

- **2026-05 · [PSD: Pushing the Pareto Frontier of Diffusion LLMs via Parallel Speculative Decoding](2026-2605.15609-psd-pushing-the-pareto-frontier-of-diffusion-llms-via-parallel-speculati.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PSD（Parallel 投機的復号）は、離散拡散型言語モデル（diffusion large language モデル; dLLM）がマスク位置を段階的に確定する処理を、空間方向と時間方向の二軸で短縮する推論方式である。

- **2026-05 · [Component-Aware Self-Speculative Decoding in Hybrid Language Models](2026-2605.01106-component-aware-self-speculative-decoding-in-hybrid-language-models.md)**  
  実装：[✓](https://github.com/hecboar/hybrid-speculative-decoding) ・ リポジトリ内被引用：1  
  状態空間モデル（SSM）と通常の注意を組み合わせるハイブリッドLLMで、既存モデルの内部成分だけを候補生成器に使う自己投機的復号を検証する。並列構成Falcon-H1では候補2トークンの一括受理率0.680だが、逐次構成Qwen3.5では0.038に落ちる。

- **2026-05 · [Bastion: Budget-Aware Speculative Decoding with Tree-structured Block Diffusion Drafting](2026-2605.29727-bastion-budget-aware-speculative-decoding-with-tree-structured-block-dif.md)**  
  実装：[✓](https://github.com/kaist-ai-osi-lab/BASTION) ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さい草稿モデル（drafter）が先に複数トークンを提案し、対象モデルがまとめて検証することで、対象モデルの逐次呼出し回数を減らす。

- **2026-04 · [WISV: Wireless-Informed Semantic Verification for Distributed Speculative Decoding in Device-Edge LLM Inference](2026-2604.17701-wisv-wireless-informed-semantic-verification-for-distributed-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  500 Mbps条件の比較では端から端までの推論遅延を最大31.4%削減する。本方式は近似的な意味受理である。Llama実機では通常方式80.4%に対しWISVは最低79.6%、Qwen実機では87.3%に対し最低86%となる条件がある。

- **2026-04 · [SENSE: Semantic Embedding Navigation with Soft-gated Evaluation for Retrieval-based Speculative Decoding](2026-2606.00021-sense-semantic-embedding-navigation-with-soft-gated-evaluation-for-retri.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、目標となる大規模言語モデルより安価な処理で複数の候補トークンを用意し、目標モデルが一括して検証することで逐次生成の反復回数を減らす。本文表1のQwen3-14Bでは、目標モデル自身の出力から作った索引を使う場合、4課題平均の速度倍率が3.03倍で、平均採択トークン数は4.13である。

- **2026-04 · [NanoSpec: Accelerating Speculative Decoding using Minimalist In-Context Vocabularies](2026-2605.26444-microspec-lightweight-in-context-vocabularies.md)**  
  実装：[✓](https://github.com/csAugust/NanoSpec) ・ リポジトリ内被引用：1  
  文脈と直近候補から毎ステップ3000未満の動的ドラフト語彙を作り、必要なLMヘッド重みを非同期収集して射影計算を削減する投機的デコード最適化。EAGLE-2のドラフト時間を平均51.6%削減する。

- **2026-04 · [Goose: Anisotropic Speculation Trees for Training-Free Speculative Decoding](2026-2604.02047-goose-anisotropic-speculation-trees-for-training-free-speculative-decodi.md)**  
  実装：[✓](https://github.com/2kinto/GOOSE_Speculative_Decoding) ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、安価な候補生成器が未来のトークン列を先に提案し、目標モデルが一回の前向き計算で複数候補をまとめて検証する。入力や生成済み文脈から一致するn-gramの続きをコピーする文脈照合候補は、目標モデルの過去の出力分布から予測する遷移候補よりも、測定上2〜18倍、中央値約6倍の受理率を持つ。

- **2026-04 · [FASER: Fine-Grained Phase Management for Speculative Decoding in Dynamic LLM Serving](2026-2604.20503-faser-fine-grained-phase-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  動的負荷下の投機的デコードを、リクエスト別投機長、検証途中の棄却枝刈り、ドラフトと検証のフロンティア単位重畳で細粒度化し、vLLM上で最大53%のスループット向上と最大1.92倍の遅延改善を示す。

- **2026-02 · [When RL Meets Adaptive Speculative Training: A Unified Training-Serving System](2026-2602.06932-aurora-adaptive-speculator-training-serving.md)**  
  実装：[✓](https://github.com/togethercomputer/aurora) ・ リポジトリ内被引用：1  
  実配信の採用・棄却トレースからドラフトモデルを非同期更新し、停止なしで重みを差し替える閉ループ型の投機的復号により、初日配備と分布変化への継続適応を実現する。

- **2026-02 · [Variational Speculative Decoding: Rethinking Draft Training from Token Likelihood to Sequence Acceptance](2026-2602.05774-variational-speculative-decoding-rethinking-draft-training-from-token-li.md)**  
  実装：[✓](https://github.com/LV-Lab-SMU/VSD) ・ リポジトリ内被引用：1  
  投機的復号では草案モデルが先の複数トークンをまとめて提案し、大きな目標モデルが一回の並列計算で検証する。

- **2026-02 · [PACER: Blockwise Pre-verification for Speculative Decoding with Adaptive Length](2026-2602.01274-pacer-blockwise-pre-verification-for-speculative-decoding-with-adaptive-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PACERは、投機的復号（投機的復号）において、小型の草稿モデルが何個の候補トークンを生成してから大型の目標モデルに検証を依頼するかを、復号の各段階で動的に決める方式である。Llama-2 7B/70BのHumanEvalでは自己回帰復号約9.1トークン/秒に対して24.2トークン/秒、すなわち2.66倍である。

- **2026-01 · [TriSpec: Ternary Speculative Decoding via Lightweight Proxy Verification](2026-2601.23180-trispec-ternary-speculative-decoding-via-lightweight-proxy-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さなドラフトモデルが先に複数のトークンを提案し、大きな対象モデルがまとめて検証することで、自己回帰生成の逐次的な待ち時間を削減する。

- **2025-12 · [GoodSpeed: Optimizing Fair Goodput with Adaptive Speculative Decoding in Distributed Edge Inference](2025-2512.09963-goodspeed-optimizing-fair-goodput-with-adaptive-speculative-decoding-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GoodSpeedは、複数の小型言語モデル（Small Language Models; SLM）がエッジサーバで候補トークンを作り、中央の大型言語モデル（Large Language モデル; LLM）が一括検証する分散投機的復号（投機的復号; SD）のスケジューラである。

- **2025-12 · [Fast Inference of Visual Autoregressive Model with Adjacency-Adaptive Dynamical Draft Trees](2025-2512.21857-fast-inference-of-visual-autoregressive-model-with-adjacency-adaptive-dy.md)**  
  実装：[✓](https://github.com/Haodong-Lei-Ray/ADT-Tree) ・ リポジトリ内被引用：1  
  画像自己回帰モデル（visual autoregressive モデル）は、画像を離散符号列に変換し、左から右へ順に画像トークンを生成する。言語モデルと同じ逐次生成の制約を持つが、画像では位置ごとに予測の難しさが大きく変わる。この局所差を無視して全画像へ同じ深さと幅の草稿木を使うと、検証されない枝の計算費用が膨らむ。この違いは重要である。

- **2025-12 · [AdaSD: Adaptive Speculative Decoding for Efficient Language Model Inference](2025-2512.11280-adasd-adaptive-speculative-decoding-for-efficient-language-model-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号の通常方式では、小型モデルが数トークンを先に生成し、大型モデルが一度の前向き計算で候補を並列検証する。

- **2025-12 · [Accelerate Speculative Decoding with Sparse Computation in Verification](2025-2512.21911-accelerate-speculative-decoding-with-sparse-computation-in-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さな草稿モデルが複数の候補トークンを先読みし、大きな対象モデルがそれらをまとめて検証することで、対象モデルの呼出し回数を減らす手法である。品質と平均受理長の評価はあるが、元モデルの出力分布との数学的同値性や、GPUでのエンドツーエンド実測速度向上は示されていない。

- **2025-11 · [TapOut: A Bandit-Based Approach to Dynamic Speculative Decoding](2025-2511.02017-tapout-a-bandit-based-approach-to-dynamic-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TapOutは、確率分布に基づく五つの停止規則を候補とし、多腕バンディット（multi-armed bandit）が検証結果からその時点で有利な規則を選ぶ方式である。

- **2025-11 · [Speculative Streaming: Efficient and Scalable Speculative Decoding with Multi-Stream Attention](2025-ecec79b7ef4d-speculative-streaming-efficient-and-scalable-speculative-decoding-with-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Medusaのように対象モデルへ複数予測ヘッドを付ける方式は別モデルを不要にするが、ヘッド間のトークン依存を表現しにくい。

- **2025-11 · [Speculative Decoding in Decentralized LLM Inference: Turning Communication Latency into Computation Throughput](2025-2511.11733-speculative-decoding-in-decentralized-llm-inference-turning-communicatio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散投機的復号（Decentralized 投機的復号、DSD）は、投機的復号を中央集約型GPUサーバから、複数の独立管理ノードへモデルを分割して実行する環境へ拡張した方式である。

- **2025-11 · [Scaling LLM Speculative Decoding: Non-Autoregressive Forecasting in Large-Batch Scenarios](2025-2511.20340-scaling-llm-speculative-decoding-non-autoregressive-forecasting-in-large.md)**  
  実装：[✓](https://github.com/ShiLuohe/SpecFormer) ・ リポジトリ内被引用：1  
  投機的復号は小さなモデルが複数トークンを先読みし、大きな目標モデルで一括検証することにより、目標モデルを直列に呼び出す回数を減らす。著者はQwenおよびLlama系で評価し、特定の草案予算制約下では従来のHASSやEAGLE-3より高い総トークン処理速度を示した。

- **2025-11 · [NEZHA: A Zero-sacrifice and Hyperspeed Decoding Architecture for Generative Recommendations](2025-2511.18793-nezha-a-zero-sacrifice-and-hyperspeed-decoding-architecture-for-generati.md)**  
  実装：[✓](https://github.com/Applied-Machine-Learning-Lab/WWW2026_NEZHA) ・ リポジトリ内被引用：1  
  候補を広く集めるために多数のビームを保持して逐次復号すると、出力は3トークン程度でも主モデルを何度も呼び出すため遅延が大きい。外部ドラフトモデルを必要とせず、識別子の位置を表すプレースホルダーと、選択した前トークンを反映する状態遷移によって、意味識別子の順序依存性を維持する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [SP²ec: Adaptive Self-Speculative Decoding for Vision-Language Models](2026-2610.18735-sp-ec-adaptive-self-speculative-decoding-for-vision-language-models.md)**  
  実装：[✓](https://github.com/hyuqi/sp2ec) ・ リポジトリ内被引用：0  
  Qwen2.5-VL-7B-InstructとLLaVA-NeXT-Mistral-7B、Video-MME・MMBench-Video・ARKitScenes・AIME25を使った評価では、既存の自己投機方式に制御器を追加することで最大11%の速度改善を報告する。

- **2026-10 · [Match the Distribution, Not the Compute: Post-Training Multi-Token Prediction Heads](2026-2610.00888-match-the-distribution-not-the-compute-post-training-multi-token-predict.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結したQwen3-8Bが生成する推論文を教師にMTPヘッドだけを後学習し、厳密検証で事前学習済みMiMo-7B-RLに近い平均受理長を実現する。分布ずれを制御する近似検証と、実測処理量に応じてヘッド数を変える適応制御器も評価する。

- **2026-10 · [JetSpec++: Foresight Parallel Drafting with Self Refinements](2026-2610.19792-jetspec-foresight-parallel-drafting-with-self-refinements.md)**  
  実装：[✓](https://github.com/hao-ai-lab/JetSpec) ・ リポジトリ内被引用：0  
  投機的復号は、小型のドラフトモデルが複数トークンを提案し、大型のターゲットモデルが一括検証することで、自己回帰生成の直列回数を減らす。原著のGB200上の単一要求サービング実験では、Qwen3-8Bを対象にGSM8KでDSparkの744.3 トークン/sから1148.8 トークン/s、MATH-500で902.1から1361.1 トークン/sへ改善した。

- **2026-10 · [From Positionwise Confidence to Prefix Scheduling: Verifier Skipping in Speculative Decoding](2026-2608.14787-from-positionwise-confidence-to-prefix-scheduling-verifier-skipping-in-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の投機的復号では、軽いドラフトモデルが提案した複数トークンを大きいターゲットモデルがまとめて検証する。

- **2026-10 · [From Draft-Then-Verify to Systems Co-Design: A Survey of Speculative Decoding for Autoregressive Large Language Models](2026-186df873bd7f-from-draft-then-verify-to-systems-co-design-a-survey-of-speculative-deco.md)**  
  実装：[✓](https://github.com/LifeIsSoSolong/awesome-speculative-decoding) ・ リポジトリ内被引用：0  
  候補の枝分かれ、検証規則、KVキャッシュの巻き戻し、同時要求のバッチ処理、GPU間通信まで含めると、単純な「ドラフト方式別」分類では結果を比較しきれない。ここで詳しく検証した全文は2026年8月11日公開のPreprints.org v1であり、同じ論文の査読済みIEEE Access版が10月16日に公開されたことは著者の公式補足リポジトリで確認した。

- **2026-10 · [DRelay: Global Draft Context for Prefix-Aware Parallel Speculative Decoding Repair](2026-2610.01439-drelay-global-draft-context-for-prefix-aware-parallel-speculative-decodi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DRelayは、大規模言語モデルの投機的復号（投機的復号）において、並列下書き（parallel drafting）が既に予測した複数位置の候補情報を、早い位置の誤った候補選択を修復する証拠として再利用する方式である。

- **2026-10 · [An Empirical Study of Speculative Decoding on Software Engineering Tasks](2026-2604.26469-an-empirical-study-of-speculative-decoding-on-software-engineering-tasks.md)**  
  実装：[✓](https://github.com/AltriaSetsuna/speculative-decoding-empirical) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、安価な草稿生成器が複数トークンを先読みし、大きな対象モデルが一度の前向き計算でまとめて検証することで、通常の逐次復号に必要な対象モデル呼び出し回数を減らす。一般的な対話ベンチマークでの高速化は、ソフトウェア工学の作業にそのまま当てはまらない。

- **2026-10 · [AgSpec: Pushing the Limits of Retrieval-Based Speculative Decoding in Coding Agent Pipelines](2026-2610.01108-agspec-pushing-the-limits-of-retrieval-based-speculative-decoding-in-cod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AgSpecは、コード生成エージェント（Coding Agent）が繰り返し使う文章やコードを検索し、投機的復号（投機的復号; SD）の草稿として再利用する方式である。

- **2026-09 · [UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding](2026-2609.39972-ubtree-parallel-tree-drafting-via-unigram-and-bigram-models-for-speculat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は軽いドラフトモデルが将来の候補トークンを提案し、大きなターゲットモデルが一度に検証することで自己回帰生成を高速化する。

- **2026-09 · [Tsubame: Tree Replay for Diffusion-Based Speculative Decoding](2026-2609.33652-tsubame-tree-replay-for-diffusion-based-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Tsubameは、投機的復号で複数の候補系列を木として提示する際、木の形を選ぶことと実際に検証する候補トークンを選ぶことを分離する方式である。

- **2026-09 · [TSS: Target-Side Sparsification for Speculative Decoding in Domain-Specific Large Language Models](2026-2609.26100-tss-target-side-sparsification-for-speculative-decoding-in-domain-specif.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では軽量ドラフトモデルが候補を生成し、大型ターゲットモデルが候補を並列検証する。多くの高速化研究はドラフト側の候補品質・候補木・生成速度を改善するが、ターゲット側は元の全層を実行することを前提とする。TSSは、翻訳・要約・QA・RAG・MMLUなどのドメインごとにターゲットのスキップ層集合をオフラインで探索する。

- **2026-09 · [SpecQuant: Speculative Decoding with Multi-Parent Quantization for Adaptive LLM Inference](2026-2609.21704-specquant-speculative-decoding-with-multi-parent-quantization-for-adapti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単独の高精度モデルで全要求を生成すると、短い事実質問も長い推論問題も同じ重み精度・同じ自己回帰生成経路を使う。一方、低ビット量子化だけでは出力品質が変化し、通常の投機的復号では別途草稿モデルを用意する必要がある。

- **2026-09 · [SEED: Self-Speculative Decoding via Implicit Encoder-Decoder](2026-2609.36590-seed-self-speculative-decoding-via-implicit-encoder-decoder.md)**  
  実装：[✓](https://github.com/lhk2004/SEED) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は軽い候補生成器で複数トークンを先に提案し、重い対象モデルがまとめて検証することで全層実行の回数を減らす。Qwen3-1.7B-BaseとQwen3-4B-Baseを数学・コード・一般知識・要約の4タスクで微調整し、単一NVIDIA A6000上の貪欲生成で、通常自己回帰生成に対して平均2.6倍および2.7倍の速度向上を報告した。

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

- **2026-09 · [LongSpark: Efficient speculative decoding with a fixed-cost parallel drafter](2026-2609.37029-longspark-efficient-speculative-decoding-with-a-fixed-cost-parallel-draf.md)**  
  実装：[✓](https://github.com/Hao-Yuan-He/LongSpark) ・ リポジトリ内被引用：0  
  大規模言語モデルの投機的復号（投機的復号）は、軽い下書き器（drafter）が複数の候補トークンを生成し、対象モデル（対象モデル）が一度の前向き計算でまとめて検証することで逐次生成の回数を減らす。Qwen3-4B、8B、14Bの数学・コード・対話8課題で、通常の自己回帰復号に対する平均処理量倍率はそれぞれ1.88、1.99、2.13倍だった。

- **2026-09 · [Jina-OCR-v1: Efficient Document Parsing with Speculative Decoding and Dense Verifiable Rewards](2026-2609.03181-jina-ocr-v1-efficient-document-parsing-with-speculative-decoding-and-den.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし一ページの出力が長くなりやすく、画像側のトークン圧縮だけでは自己回帰復号の時間が残る。原著はNVIDIA L4で、vLLM 0.20.1のバッチ1・通常実行（eager）において、草稿3段で通常の自己回帰復号に対して1.95倍のトークン生成速度を報告する。

- **2026-09 · [How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus](2026-2609.15504-orthrus-numerical-precision-losslessness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Orthrusの無損失投機的復号を独立再現し、BF16では生成軌跡の完全一致が43〜45%に留まる一方、FP32では1,190件すべて一致することを示した再現・評価研究。

- **2026-09 · [HAWK: Rethinking Multimodal Drafting for Speculative Decoding](2026-2610.00623-hawk-rethinking-multimodal-drafting-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HAWKは、画像と文章を処理する大規模視覚言語モデル（LVLM）の投機的復号において、軽量な草案モデル（ドラフタ）が教師モデルの視覚情報を十分に活用できず、複数トークンを連続して提案すると受理率が落ちる問題を扱う。

- **2026-09 · [GrowMTP: Can RL Grow Its Own Draft Head?](2026-2609.16648-growmtp-efficient-multi-token-prediction-via-progressive-growth.md)**  
  実装：[✓](https://growmtp.github.io/) ・ リポジトリ内被引用：0  
  強化学習ロールアウトの検証信号でドラフトヘッドをその場で育成し、事前ヘッドなしでも投機的デコードによる学習加速を実現する。

- **2026-09 · [GDN Tree-Scan: Served Tree Verification for Recurrent-Hybrid Language Models](2026-2609.23900-gdn-tree-scan-served-tree-verification-for-recurrent-hybrid-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再帰状態を持つハイブリッドLLMの木型投機検証で、枝ごとのGDN状態を親子関係どおりに走査し、受理枝だけを永続化することで、Qwen3.6-27B-FP8のデコード処理量を27.0%改善する。

- **2026-09 · [Efficient Mixture-of-Experts with Speculative Decoding via Expert Coactivation](2026-2609.22471-efficient-mixture-of-experts-with-speculative-decoding-via-expert-coacti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（mixture-of-エキスパート; MoE）は、トークンごとに少数の専門家を選択して演算することで、総パラメータ数が大きくても活性化する重み量を抑える。

- **2026-09 · [ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding](2026-2609.17241-echo-early-layer-collaborative-hierarchical-orchestration-with-bonus-logits-in-speculative-decoding.md)**  
  実装：[✓](https://github.com/whucs21Mzy/ECHO) ・ リポジトリ内被引用：0  
  対象モデルの前半層を高頻度の候補木探索、後半層を低頻度の厳密検証へ分け、中間状態再利用と補助ロジットで候補を更新し、追加ドラフトモデルなしで2.4〜2.9倍級の生成高速化を報告する。

- **2026-09 · [DScale: Scaling Block-Diffusion Speculative Decoding with Adaptive Verification](2026-2609.37532-dscale-scaling-block-diffusion-speculative-decoding-with-adaptive-verifi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DScaleは、ブロック拡散型の草案器が並列生成したトークン候補を、教師モデルが検証する際の実行効率を改善するサービング方式である。

- **2026-09 · [Diffusion Drafts, AR Verifies: Accelerating Document OCR with Self-Speculative Decoding](2026-2609.26638-diffusion-drafts-ar-verifies-accelerating-document-ocr-with-self-specula.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし同じステップで予測した位置は互いの確定値を見ていないため、各トークンが局所的にもっともらしくても、読み順が飛ぶ、語が重複する、表タグが閉じないなどの誤りが生じる。領域crop単位・SGLangのデコード-onlyでは777から3,057 トークン/s（3.94倍）である。

- **2026-09 · [DEdit: Iterative Draft Editing for Speculative Decoding](2026-2609.38510-dedit-iterative-draft-editing-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後ろの位置の予測を前の位置の修正に利用できる点が、因果方向の補正方式と異なる。著者の7課題マクロ平均では、Qwen3-4BとQwen3-8Bを対象とするgreedy復号で、自己回帰生成に対するエンドツーエンド速度倍率がそれぞれ5.72倍と5.97倍、1検証ラウンド当たりの平均前進トークン数が7.58と7.75であった。

- **2026-09 · [CAST: Cost-Aware Speculative Trees from One-Pass Block Drafters](2026-2610.00321-cast-cost-aware-speculative-trees-from-one-pass-block-drafters.md)**  
  実装：[✓](https://github.com/js-lee-AI/CAST) ・ リポジトリ内被引用：0  
  最初の方で対象モデルの選ぶトークンと異なれば、後続の候補をいくら正しく予測していても、そのラウンドで確定できるトークンは短くなる。H100 SXMのQwen3-8Bでは、逐次復号比の平均高速化がDFlashの4.38倍からCASTの5.62倍へ改善した。

- **2026-09 · [BV Loss: Block Verification-Aware Loss for Block Diffusion Speculative Decoding](2026-2609.34832-bv-loss-block-verification-aware-loss-for-block-diffusion-speculative-de.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では小さな下書き器が複数の候補トークンを提案し、対象モデル（対象モデル）が一括検証する。Qwen3-4B/8Bを対象モデルにした5層DFlash・DSparkで、7課題平均の検証1回当たり保持トークン数は、CE学習と比較して13.0～21.0%改善した。

- **2026-09 · [Adapting Tree-Structured Speculative Decoding to DeepSeek-V4 for Efficient Inference](2026-2609.24698-adapting-tree-structured-speculative-decoding-to-deepseek-v4-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では軽いドラフトが複数候補を先読みし、重いターゲットが一度の検証で連続する候補を受理する。処理量の最大改善はShareGPT、D=6、バッチ4の18.5%であり、受理長の伸びがそのまま同率の処理量改善になるわけではない。

- **2026-09 · [Acceptance-Aware Draft Model Training for Speculative Decoding](2026-2609.24150-acceptance-aware-draft-model-training-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小型の下書きモデルが生成した複数の候補トークンを、大型の目標モデルが一度に検証することで自己回帰復号の待機を減らす。

- **2026-08 · [WA-SpecDec: World-Aware Speculative Decoding for Vision-Language-Action Models](2026-2608.08725-wa-specdec-world-aware-speculative-decoding-for-vision-language-action-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  WA-SpecDecは受理しきい値自体を動的に変えるのではない。LIBERO四系列の評価では、通常の投機的復号に対し、同一の受理方式と比較条件で成功率と速度を改善した。

- **2026-08 · [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) ・ リポジトリ内被引用：0  
  GLANCEは、VLMの視覚・言語融合状態から未来トークン塊を1回で下書きし、幅広い候補木を対象モデルで一括検証して、画像根拠付き生成の逐次下書き処理を減らす。

- **2026-08 · [OoO-Spec: Out-of-Order Semantic Speculation for Fast Tool Calling](2026-2608.00814-ooo-spec-out-of-order-semantic-speculation-for-fast-tool-calling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OoO-Specは、この未解決の部分を文字列上の位置に到達する前に、意味的なスロットとして並列予測する方式である。

- **2026-08 · [Oilbird: Training-Free Speculative Decoding with Keys the Verifier Already Computes](2026-2608.03839-oilbird-training-free-speculative-decoding-with-keys-the-verifier-alread.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Oilbirdは、学習不要の投機的復号（学習不要 投機的復号）における「保存済みの正解候補を検索できない」という問題を対象とする。提案方式は、対象モデルの検証計算で既に得られた中間隠れ状態を位置ごとに保存し、次回の候補検索で意味的な近傍検索を行う。

- **2026-08 · [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MemSpecは、入力と生成履歴から有望なドラフトを予測し、上位モデルを常駐集合へ先読みして、エッジ端末のSSD読み込み待ちを隠し適応投機を高速化する。

- **2026-08 · [LibraSpec: Dynamic Diffusion-Based Speculative Decoding via Marginal-Gain-Driven Optimization](2026-2608.08721-libraspec-dynamic-diffusion-based-speculative-decoding-via-marginal-gain.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の動的投機長制御は「何トークン受理されそうか」を予測して長さを決めることが多い。LibraSpecはこの費用構造の違いに着目し、期待受理長だけでなく検証時間を分母に含む期待高速化率を最大化する。

- **2026-08 · [Is Multimodal Speculative Decoding Ready for Diffusion-Based Parallel Drafting? A Survey and Empirical Diagnosis](2026-2608.20743-is-multimodal-speculative-decoding-ready-for-diffusion-based-parallel-dr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存方式の整理と、視覚言語モデル（VLM）における実測を組み合わせたサーベイ兼実証的診断であり、新しい単一の復号アルゴリズムを提案する論文ではない。

- **2026-08 · [FOVEA: Focused On-Demand Visual Evidence Adaptation for Cache-Friendly Multimodal Speculative Decoding](2026-2608.22883-fovea-focused-on-demand-visual-evidence-adaptation-for-cache-friendly-mu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ただし、本文の「検索件数を動的に決める」という説明と付録の「16件固定」という記述は矛盾しており、可変件数機構の実験的寄与は原著だけでは完全に確証できない。

- **2026-08 · [AsymSpec: Efficient Cloud-Edge Speculative Decoding over Asymmetric Networks](2026-2608.04974-asymspec-efficient-cloud-edge-speculative-decoding-over-asymmetric-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非対称回線向けの証明付き段階補正と確認済み要求間パイプラインを組み合わせ、クラウド・エッジ投機的復号の通信待ちと無効先読みを削減する。

- **2026-08 · [Approximate Speculative Decoding](2026-2608.03447-approximate-speculative-decoding.md)**  
  実装：[✓](https://github.com/Kissmetothemoon/ASD) ・ リポジトリ内被引用：0  
  標準的なgreedy投機的復号では、小さな下書きモデルが候補トークン列を作り、大きなtargetモデルが1回の順伝播 passでそれらを検証する。下書きとtargetのgreedy トークンが一致する限り連続して受理するが、最初の不一致が生じた時点で後続候補を捨てる。Approximate 投機的復号（ASD）はこの制約を緩める。

- **2026-08 · [AdaMTP: An Adaptive Training Paradigm for Multi-Token Prediction](2026-2608.00434-adamtp-an-adaptive-training-paradigm-for-multi-token-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論では候補をまとめて検証することで逐次実行回数を減らせるが、学習では位置にかかわらず固定個数の未来を教師信号にすると、話題や文法単位の切れ目を越えた不確実な予測を強制する。代表例としてLlama-3.1-8BのGSM8Kで、通常MTPの自己回帰比1.65倍に対しAdaMTPは2.12倍、Gemma-3-12Bの同課題では2.38倍に対し2.75倍である。

- **2026-08 · [A Rigor-Matched Audit of Periodic-Step Layer Skipping for Efficient LLM Inference: ConfLayers versus SWIFT, with a Supplemental Analysis of Trained Routing Alternatives](2026-2608.28846-a-rigor-matched-audit-of-periodic-step-layer-skipping-for-efficient-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  どの層を省くかをオンラインで探索する方式は、探索自体の推論呼び出し・評価・探索状態更新が余分な計算となる。この費用を測定から除くか含めるかで、どちらの方式が速いかが逆転する。

- **2026-07 · [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](2026-2607.21535-windowed-mtp-removing-the-full-context-draft-kv-tax-at-million-token-con.md)**  
  実装：[✓](https://github.com/avalliappan-nvidia/windowed-mtp-b200) ・ リポジトリ内被引用：0  
  投機的復号は、小さなドラフトが先のトークンを提案し、大きなターゲットモデルがまとめて検証することで、生成トークン当たりの遅延を短縮する。

- **2026-07 · [Unlocking Parallelism in Autoregressive Language Models via Speculative Decoding with Progressive Tree Drafting](2026-2607.10661-unlocking-parallelism-in-autoregressive-language-models-via-speculative-.md)**  
  実装：[✓](https://github.com/MINE-USTC/PTD) ・ リポジトリ内被引用：0  
  投機的復号は複数候補を一度に検証して、正しい連続部分をまとめて確定させるが、別の小型ドラフトモデルを使う方式ではモデルのロード・通信・同期・追加学習の費用が生じる。

- **2026-07 · [Training-Free Adaptive Speculative Decoding via Linguistic Priors](2026-2ad70212cfe6-training-free-adaptive-speculative-decoding-via-linguistic-priors.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LinguaSpecは、投機的復号（投機的復号）の二つの支出先――小さい草稿モデルが次の候補をどこまで生成するか、大きい対象モデルがその候補をどこまで受理するか――を、トークンの言語的役割に応じて変える方式である。自己回帰復号に対する平均実測高速化は順に4.26倍、4.67倍、4.08倍で、同じ表のEAGLE-3は3.97倍、4.36倍、3.88倍だった。

- **2026-07 · [SPIDE: Serial and Parallel Intertwined Speculative Decoding](2026-6403c69c2ddc-spide-serial-and-parallel-intertwined-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の自己回帰復号では、ターゲットLLMを生成トークンごとに実行するため、大規模モデルの重み読み出しと逐次依存が生成遅延を支配する。標準SDは小さな草稿モデルが複数トークンを先行生成し、大きなターゲットが一度の順伝播で検証することで、この逐次依存を減らす。自己回帰生成に対する壁時計時間の高速化は平均3.25倍、最大4.56倍。

- **2026-07 · [Revisiting Lossy Verification in Speculative Decoding: Mechanisms, Trade-offs, and Failure Modes](2026-2607.26627-revisiting-lossy-verification-in-speculative-decoding-mechanisms-trade-o.md)**  
  実装：[✓](https://github.com/ZhouYuxuanYX/Fast-HSD) ・ リポジトリ内被引用：0  
  投機的復号は軽量なドラフトモデルqが候補を提案し、ターゲットモデルpがまとめて検証することで、逐次生成のターゲット順伝播 pass回数を減らす。EAGLE-3を用いたLlama-3.1-8Bの比較では、η-samplingをターゲットへ正しく適用したMATH正答率76.12%に対し、typical acceptanceは69.84%だった。

- **2026-07 · [Margins, Not Windows: Training-Free Per-Step Lossy Speculative Decoding](2026-2609.02897-margins-not-windows-training-free-per-step-lossy-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号は小さな下書きモデルに複数トークンまたは候補木を作らせ、targetモデルがまとめて検証することでこの逐次性を緩める。代表結果として、単一A100上の主評価で両軸併用方式は9条件すべてでEAGLE-3を上回り、モデル平均の高速化倍率は16–44%、最大改善は56%だった。

- **2026-07 · [HCSpec: Two-Tier Horizontal Cascade Speculative Decoding for High-Efficiency Large Language Model Inference](2026-e55859d7e526-hcspec-two-tier-horizontal-cascade-speculative-decoding-for-high-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな草稿モデルが先読みした複数トークンを標的モデルが一括検証し、標的モデルの逐次呼び出しを削減する。

- **2026-07 · [EDSD: Entropy-Driven Design for Faster Speculative Decoding](2026-90a0064fbd38-edsd-entropy-driven-design-for-faster-speculative-decoding.md)**  
  実装：[✓](https://github.com/KerwinKai/EDSD) ・ リポジトリ内被引用：0  
  EDSDは、投機的復号（投機的復号）の草稿モデルを、対象となる大規模言語モデルの不確実性に応じて学習・設計する研究である。代表例のLlama-3.1-Instruct 8B、温度0では、EAGLE-3の平均受理長6.34・通常復号比3.73倍に対してEDSDは6.56・3.92倍となる。

- **2026-07 · [Characterizing self-speculative decoding approaches for accelerating LLMs](2026-145a6256ce66-characterizing-self-speculative-decoding-approaches-for-accelerating-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では安価なドラフトが複数トークンを先に提案し、完全なモデルが一括検証する。論文はSWIFT、下書き & Verify、LayerSkip、DEL、Kangarooを比較し、層スキップ方式のHumanEvalにおける通常生成比高速化が1.04〜1.48倍に留まる一方、早期終了方式は平均1.49〜2.67倍を達成したと報告する。

- **2026-07 · [Beyond KV Reconstruction: Functional Reconstruction for MLA Draft Models in Speculative Decoding](2026-2607.27269-beyond-kv-reconstruction-functional-reconstruction-for-mla-draft-models-.md)**  
  実装：[✓](https://github.com/swyhahaha/FunctionalMLA) ・ リポジトリ内被引用：0  
  本論文は、多頭注意（Multi-Head 注意機構; MHA）またはグループ化クエリ注意（Grouped-Query 注意機構; GQA）で事前学習した小型言語モデルを、多頭潜在注意（Multi-head Latent 注意機構; MLA）へ変換して投機的復号（投機的復号）のドラフトモデルとして使う際の受理率低下を扱う。

- **2026-07 · [A Sparse Glimpse of the Whole: Train-Free Self-Speculative Decoding](2026-2607.27735-a-sparse-glimpse-of-the-whole-train-free-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  完全KVでの検証と正しい受理・補正を行うため、近似drafterの出力をそのまま採用する方式とは異なり、元の対象モデルの出力分布を維持する設計である。

- **2026-06 · [WhiFlash: Accelerating Speculative Decoding with Token-Level Cross-Paradigm Routing](2026-2606.07710-whiflash-accelerating-speculative-decoding-with-token-level-cross-paradi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では小型草稿器が次のトークン候補を提案し、大型目標モデルが候補をまとめて検証する。原著はこの切替処理の費用を検証ラウンド遅延の7%未満に抑えたと報告する。

- **2026-06 · [SimSD: Simple Speculative Decoding in Diffusion Language Models](2026-2606.02544-simsd-simple-speculative-decoding-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/airevo2/SimSD-release) ・ リポジトリ内被引用：0  
  自己回帰言語モデルの投機的復号では、小型モデルが先に複数トークンを提案し、大型モデルが一度の前向き計算で各提案の確率を評価する。2枚のRTX PRO 6000 Blackwell、バッチ1、KVキャッシュ有効の条件で、基本のVanilla TP2比最大7.46倍のデコード処理量を報告する。

- **2026-06 · [GRAFT: Adaptive DLM-Based Draft Tree Construction with Target-Distilled Edge Scoring](2026-2608.20375-graft-adaptive-dlm-based-draft-tree-construction-with-target-distilled-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GRAFTは、拡散言語モデル（diffusion language モデル; DLM）を草稿器に使う投機的復号（投機的復号）で、候補トークンをどの親につなぐかと各復号回で何個の候補節点を検証するかを同時に最適化する研究である。従来のDDTreeは、各位置のトークン確率の積で経路を評価するため、親が変わっても子の評価値が同じである。

- **2026-06 · [Diffusion Language Model Parallel Decoding via Product-of-Experts Bridge](2026-2606.08048-diffusion-language-model-parallel-decoding-via-product-of-experts-bridge.md)**  
  実装：[✓](https://github.com/juntongshi48/poe-bridge) ・ リポジトリ内被引用：0  
  PoE-Bridgeは、拡散言語モデル（Diffusion Language モデル、DLM）の複数トークン並列生成と、自己回帰モデル（Autoregressive モデル、AR）の高い文章品質を両立させるための復号方式である。

- **2026-05 · [TreeGraft: Adaptive Multi-Drafter Grafting for Tree-Based Speculative Decoding](2026-2608.26112-treegraft-adaptive-multi-drafter-grafting-for-tree-based-speculative-dec.md)**  
  実装：[✓](https://anonymous.4open.science/r/TreeGraft-E983) ・ リポジトリ内被引用：0  
  通常の投機的復号は、小さい草稿モデルが将来のトークンを提案し、大きい対象モデルが候補を一度に検証する。対象モデルの通常の自己回帰復号に対する平均高速化はTreeGraftが1.60倍、全段階を小草稿器にするAll Smallが1.32倍、全段階を中草稿器にするAll Midが1.39倍だった。

- **2026-05 · [SpecKV: Adaptive Speculative Decoding with Compression-Aware Gamma Selection](2026-2605.02888-speckv-adaptive-speculative-decoding-with-compression-aware-gamma-select.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量なドラフトモデルが複数の次トークン候補を提案し、大型の対象モデルが一度の順伝播で候補を検証することで生成を高速化する。

- **2026-05 · [SlimSpec: Low-Rank Draft LM-Head for Accelerated Speculative Decoding](2026-2605.10453-slimspec-low-rank-draft-lm-head-for-accelerated-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さなドラフトモデルが先に複数トークンを提案し、大きな対象モデルが一括して検証することで生成を高速化する。

- **2026-05 · [RAC: Request-adaptive Configuration for Efficient Speculative Decoding](2026-2ebee891fde4-rac-request-adaptive-configuration-for-efficient-speculative-decoding.md)**  
  実装：[✓](https://github.com/JhSheng/RAC-) ・ リポジトリ内被引用：0  
  RAC（リクエスト-適応的 Configuration selection）は、投機的復号（投機的復号）で使う草稿モデルと草稿長を要求ごとに同時選択する方式である。表1ではVicuna-33B-v1.3を目標モデルとし、HumanEvalの生成速度を通常の自己回帰復号29.369 トークン/sからRACの59.343 トークン/sへ改善した（2.021倍）。

- **2026-05 · [Performance-Driven Policy Optimization for Speculative Decoding with Adaptive Windowing](2026-2605.14978-performance-driven-policy-optimization-for-speculative-decoding-with-ada.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PPOW（Performance-Driven Policy Optimization with 適応的 Windowing）は、投機的復号（投機的復号）で用いる軽量な草稿モデル（下書きモデル、drafter）を、推論時の受理効率に合わせて追加学習する方式である。

- **2026-05 · [Hybrid Verified Decoding: Learning to Allocate Verification in Speculative Decoding](2026-2606.01019-hybrid-verified-decoding-learning-to-allocate-verification-in-speculativ.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量な草稿器が複数の候補トークンを提案し、最終的な対象LLMが一括検証して受理できる接頭部分を確定する。平均高速化はそれぞれ2.97倍、2.64倍。

- **2026-05 · [DREAM-S: Speculative Decoding with Searchable Drafting and Target-Aware Refinement for Multimodal Generation](2026-2606.00535-dream-s-speculative-decoding-with-searchable-drafting-and-target-aware-r.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/DREAM-S) ・ リポジトリ内被引用：0  
  DREAM-Sは、画像を含む入力を処理する視覚言語モデル（VLM）のトークン生成を速くするため、投機的復号の草稿モデルそのものを実行環境に合わせて選ぶ方式である。LLaVA-v1.6-Vicuna-13Bでは、温度0の6ベンチマーク平均で自己回帰生成に対する速度比が3.16倍となり、同条件のEAGLE-3の2.89倍を上回る。

- **2026-05 · [DREAM-R: Multimodal Speculative Reasoning with RL-Based Refined Drafting, Precise Verification, and Fully Parallel Execution](2026-2605.28678-dream-r-multimodal-speculative-reasoning-with-rl-based-refined-drafting-.md)**  
  実装：[✓](https://github.com/HuYunhai-Alex/DREAM-R) ・ リポジトリ内被引用：0  
  生成の各ステップで大きな目標モデルを実行すると、この長い推論部分が待ち時間を支配する。目標モデルの品質を必ず数学的に保存する厳密なトークン投機復号とは異なり、推論ステップの意味的妥当性を判定する近似的な方式であることが重要である。

- **2026-05 · [Cassandra: Enabling Reasoning LLMs at Edge via Self-Speculative Decoding](2026-2605.26558-cassandra-enabling-reasoning-llms-at-edge-via-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非構造化の重要値選別、仮数部切詰め、指数部の圧縮を併用し、ビット表現の復号を支援する専用回路とメモリ管理まで設計している。

- **2026-05 · [Beyond the Target: From Imitation to Collaboration in Speculative Decoding](2026-2605.24793-beyond-the-target-from-imitation-to-collaboration-in-speculative-decodin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推測復号（投機的復号）は、小さな草稿モデルが複数トークンを先読みし、ターゲットが一度の並列計算で検証することで、ターゲットの呼び出し回数を減らす。

- **2026-05 · [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、投機的復号（投機的復号）が単独要求では速くても、実際の大規模言語モデル配備で要求数が増えると高速化倍率が縮小し、場合によっては通常復号より遅くなる現象を説明する遅延モデルを提案する。

- **2026-04 · [SpecTr-GBV: Multi-Draft Block Verification Accelerating Speculative Decoding](2026-2604.25925-spectr-gbv-multi-draft-block-verification-accelerating-speculative-decod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SpecTr-GBVは、小型の草稿モデルが作った複数の候補列を大きな対象モデルでまとめて検証し、対象モデルの出力分布を保ちながら一反復で確定できるトークン数を増やす方式である。提案法は複数草稿とブロック検証を同時に扱い、独立同分布で草稿を生成するという実現可能な制約の下で期待受理長の上限を達成することを理論的に示す。

- **2026-04 · [Position-Aware Drafting for Inference Acceleration in LLM-Based Generative List-Wise Recommendation](2026-2604.27747-position-aware-drafting-for-inference-acceleration-in-llm-based-generati.md)**  
  実装：[✓](https://github.com/Jiaju-Chen/PAD-Rec) ・ リポジトリ内被引用：0  
  各アイテムを単なる自然言語の名前として出力するのではなく、残差量子化変分オートエンコーダ（RQ-VAE）から得た4個の意味識別子と区切りトークンへ変換し、それらを順次生成する。

- **2026-04 · [From Tokens to Steps: Verification-Aware Speculative Decoding for Efficient Multi-Step Reasoning](2026-2604.15244-from-tokens-to-steps-verification-aware-speculative-decoding-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SpecGuardは、通常の推測復号がトークン単位の確率分布を基準に下書き候補を受理するのに対し、意味のまとまりを持つ推論ステップ単位で候補を選び、モデル内部の二種類の信号から妥当性を検証する。小型下書きモデルで複数の推論ステップを生成し、その中で他候補との意味的一致が最も高いものを代表として選ぶ。

- **2026-04 · [EvoSpec: Evolving Speculative Decoding via Real-Time Vocabulary and Parameter Adaptation](2026-2605.27390-evospec-evolving-speculative-decoding-via-real-time-vocabulary-and-param.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号は、小さな草稿モデルが先行して候補トークンを生成し、大きなターゲットモデルがまとめて検証することで自己回帰生成を高速化する。

- **2026-04 · [Calibrated Speculative Decoding: Frequency-Guided Candidate Selection for Efficient Inference](2026-2604.13634-calibrated-speculative-decoding-frequency-guided-candidate-selection-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  途中のトークンが棄却されると、それ以降に先読みしたトークンも使えなくなる。Llama-3-70Bと1Bの組では、4課題の平均生成速度がターゲット単独比2.02倍となり、標準投機的復号の1.75倍を上回る。

- **2026-04 · [AHASD: Asynchronous Heterogeneous Architecture for LLM Adaptive Drafting Speculative Decoding on Mobile Devices](2026-2604.25326-ahasd-asynchronous-heterogeneous-architecture-for-llm-adaptive-drafting-.md)**  
  実装：[✓](https://github.com/MAdrid1011/AHASD) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さな草稿モデル（下書き language モデル, DLM）が複数の候補トークンを生成し、大きな目標モデル（target language モデル, TLM）がまとめて検証することで、高価な目標モデルの逐次実行回数を減らす。

- **2026-03 · [EAGLE-Pangu: Accelerator-Safe Tree Speculative Decoding on Ascend NPUs](2026-2603.08088-eagle-pangu-accelerator-safe-tree-speculative-decoding-on-ascend-npus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は小さな草稿モデルで複数候補を先に生成し、教師モデルがまとめて検証することで教師モデルの呼び出し回数を減らす。240ターンの単一要求評価で、教師単独の平均17.65トークン/秒から22.42トークン/秒へ改善し、平均速度比1.27倍を報告する（原著表1）。

- **2026-03 · [Cross-Family Speculative Decoding for Polish Language Models on Apple Silicon: An Empirical Evaluation of Bielik 11B with UAG-Extended MLX-LM](2026-2604.16368-cross-family-speculative-decoding-for-polish-language-models-on-apple-si.md)**  
  実装：[✓](https://github.com/krzysiekfonal/mlx-lm/tree/feature/slem-with-context-aware) ・ リポジトリ内被引用：0  
  投機的復号は、小さな草稿モデルが複数の候補トークンを先行生成し、大きなターゲットモデルがまとめて検証することで生成速度を上げる。一般的な速度モデルでは、ターゲットがk個の候補をまとめて検証する費用は1トークンの自己回帰生成に近く、草稿が十分に安くて受理率が高ければ高速化できる。

- **2026-03 · [Accelerating PayPal's Commerce Agent with Speculative Decoding: An Empirical Study on EAGLE3 with Fine-Tuned Nemotron Models](2026-2604.19767-accelerating-paypal-s-commerce-agent-with-speculative-decoding-an-empiri.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、新しい投機的復号アルゴリズムそのものの提案ではなく、商取引向けに微調整された8B級言語モデルの構造化出力に、既存のEAGLE3を導入したときの運用上の利益と限界を測定する実証論文である。草稿長3の構成では、要求処理量は基準の1.22〜1.49倍、平均要求遅延は18〜33%短縮された。

- **2026-02 · [WANSpec: Leveraging Global Compute Capacity for LLM Inference](2026-2602.18931-wanspec-leveraging-global-compute-capacity-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のリクエスト転送は遠距離ネットワークの往復遅延を増やし、対話生成には不利である。高性能拠点ではtargetモデルを引き続き動かし、別拠点のworkerが先読み候補を送ることで、主拠点のGPU負荷を軽減する。著者らのAWS実機検証では、近距離の別拠点間でcontrollerが実行する下書き 順伝播 passを減らしながら生成時間をほぼ維持した。

- **2026-02 · [Training-free Dropout Sampling for Semantic Token Acceptance in Speculative Decoding](2026-2603.03333-training-free-dropout-sampling-for-semantic-token-acceptance-in-speculat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さい草稿モデルが複数トークンを先読みし、大きい検証モデルがまとめて検証することで、自己回帰生成の逐次計算を減らす。A100を4基使ったテンソル並列（テンソル Parallelism; TP=4）構成で、標準投機的復号に対して条件により1.09～1.33倍程度の処理量改善を報告する。

- **2026-02 · [Speculative Decoding Scaling Laws (SDSL): Throughput Optimization Made Simple](2026-2603.11053-speculative-decoding-scaling-laws-sdsl-throughput-optimization-made-simp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量な草稿モデルが複数の次トークン候補を作り、大きな検証モデルがまとめて確認することで生成の逐次的な費用を減らす。結果は「大きい草稿ほど採択率が高い」だけでなく、採択率の改善と草稿費用の競合が中間規模に最適点を作ることを示す。

- **2026-02 · [SDFP: Speculative Decoding with FIT-Pruned Models for Training-Free and Plug-and-Play LLM Acceleration](2026-2602.05499-sdfp-speculative-decoding-with-fit-pruned-models-for-training-free-and-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量な草稿モデルが候補トークンを先に生成し、元の大きな検証モデルがまとめて採否を判定することで、自己回帰生成の遅延を削減する。

- **2026-02 · [Privacy-Aware Split Inference with Speculative Decoding for Large Language Models over Wide-Area Networks](2026-2602.16760-privacy-aware-split-inference-with-speculative-decoding-for-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  問題は、生成の各トークンでローカル→クラウド→ローカルの往復通信が必要になることだ。著者はヤコビ反復（Jacobi Iteration）から得たn-gram候補を使う先読み復号（Lookahead Decoding）を組み込み、1回の往復で複数トークンを確定させることで遅延を償却する。

- **2026-02 · [Dynamic Delayed Tree Expansion For Improved Multi-Path Speculative Decoding](2026-2602.16994-dynamic-delayed-tree-expansion-for-improved-multi-path-speculative-decod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数候補を木状に展開する多経路方式では、同じ対象モデル呼び出しで複数の分岐を評価できる一方、木を大きくすると下書き計算と対象モデルの検証計算が増える。比較した既存方式では木走査検証が3モデル系統平均15.89 トークン/sで最良だったが、NDEを組み込んだSpecInferは16.69 トークン/sとなり約5.0%上回った。

- **2026-02 · [Benchmarking the Energy Savings with Speculative Decoding Strategies](2026-2602.09113-benchmarking-the-energy-savings-with-speculative-decoding-strategies.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  論文は、一定長の草案を生成するCOGA、草案長を動的に変えるDYGA、EAGLE-2、EAGLE-3、Medusaを、Vicuna、Llama、Flan-T5、Qwen3などのモデル系列と、コード生成、数学推論、要約の課題で比較する。

- **2026-01 · [StarSD: One-for-Many Speculative Decoding](2026-2601.21622-starsd-one-for-many-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  StarSDは、複数の大型言語モデルの推論要求が一つの軽量下書きモデルを共有する、星型の分散投機的復号（投機的復号）システムである。原著の2サーバ・計7 GPUの構成では、対象モデル1個で総処理量79.9トークン/秒、6個で288.7トークン/秒に増えた。

- **2026-01 · [JuDi: Revisiting Judge Decoding from First Principles via Training-Free Distributional Divergence](2026-2601.04766-judi-revisiting-judge-decoding-from-first-principles-via-training-free-d.md)**  
  実装：[✓](https://github.com/sunshy-1/JuDi) ・ リポジトリ内被引用：0  
  著者らは学習済み判定器の「重要トークン」スコアが、二つのモデルのカルバック・ライブラー発散（Kullback–Leibler divergence; KL発散）と相関することを確認し、KL値が閾値を下回る候補を受理する学習不要の方式JuDiを提案する。

- **2026-01 · [ConfSpec: Efficient Step-Level Speculative Reasoning via Confidence-Gated Verification](2026-2602.18447-confspec-efficient-step-level-speculative-reasoning-via-confidence-gated.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型の草稿モデルが作った途中の推論を大型の対象モデルで検証する既存方式は、単語列が異なっていても意味が同じである推論を扱える一方、すべてのステップを高価な検証器へ送ると加速効果が弱くなる。論文の表2では、DeepSeek-R1-Distill 1.5B/32B構成で5課題平均の高速化が1.68倍、平均正答率が対象モデル81.99%に対して81.51%である。

- **2026-01 · [ButterflyMoE: Compression-Scalable Ternary Experts via Structured Butterfly Orbits](2026-2601.13563-butterflymoe-compression-scalable-ternary-experts-via-structured-butterf.md)**  
  実装：[✓](https://github.com/aryan331277/butterfly_moe) ・ リポジトリ内被引用：0  
  低ビット量子化や枝刈りは係数を小さくできるが、独立した行列を $N$ 個保存する構造は残る。専門家部分の容量は標準MoEの32.00 MBから0.40 MBへ減少するが、検証困惑度（perplexity、低いほど良い）は標準MoEの71.75に対してButterflyMoEは81.19であり、無損失の圧縮ではない。

- **2025-11 · [Towards Efficient LLM Inference via Collective and Adaptive Speculative Decoding](2025-b830988a571f-towards-efficient-llm-inference-via-collective-and-adaptive-speculative-.md)**  
  実装：[✓](https://github.com/kiki632/Smurfs) ・ リポジトリ内被引用：0  
  Smurfsは、大規模言語モデルの投機的復号を、単一の小型モデルによる先読みから、複数の小型モデルが協調するサービス実行方式へ拡張する研究である。複数のドラフトモデルを同時に使えば候補の多様性は得られるが、それぞれの候補を大型モデルで検証すると、検証費用が増えて高速化が相殺される。

- **2025-11 · [Striking the Right Balance between Compute and Copy: Improving LLM Inferencing Under Speculative Decoding](2025-2511.12031-striking-the-right-balance-between-compute-and-copy-improving-llm-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BMC（Balancing メモリ and Compute）は、LLMの復号時にキー・値キャッシュ（key-value キャッシュ; KVキャッシュ）を拡張する際のメモリ再確保・コピー費用と、未使用のキャッシュ領域を含む余分な注意計算を交換する方式である。

- **2025-11 · [FractalLLM: Lossless Self-Speculative Decoding with Layer Embedded Self-Compression](2025-2d13577b2303-fractalllm-lossless-self-speculative-decoding-with-layer-embedded-self-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FractalLLMは、自己回帰言語モデルのトークン逐次生成を減らすため、元のデコーダの途中に小さな圧縮モデルを挿入する自己投機的復号（自己投機的復号）の方式である。論文のRTX 3090実験では、CodeLlama-13BのHumanEvalで基準の1.79トークン/秒が4.43トークン/秒となり、2.47倍の高速化を報告する。

- **2025-11 · [Democratizing LLM Efficiency: From Hyperscale Optimizations to Universal Deployability](2025-2511.20662-democratizing-llm-efficiency-from-hyperscale-optimizations-to-universal-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLM推論効率を「演算量・トークン毎秒・GPUのピーク処理率」だけで測る研究慣行に対し、導入する組織の規模と運用条件を含めて効率を評価すべきだと提案する立場表明である。

### 2年前（2024-11〜2025-10）

- **2025-03 · [EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](2025-2503.01840-eagle-3.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：220  
  特徴回帰制約を外して直接トークン予測し、訓練時に自己生成入力を再投入することでドラフト学習のデータ規模拡大を有効化したEAGLE系投機的復号。

- **2025-04 · [Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion](2025-speculative-diffusion-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  自己回帰型の下書き器を離散拡散型へ置換し、候補列の生成と目標モデルによる検証の双方を並列化して投機的復号を高速化する方式。

- **2025-09 · [DiffuSpec: Unlocking Diffusion Language Models for Speculative Decoding](2025-2510.02358-diffuspec-unlocking-diffusion-language-models-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  投機的復号は小さいドラフト器が数トークンを先に作り、大きい対象モデルがまとめて検証することで逐次実行を減らす。論文の主実験では、Qwen2.5-32Bを対象モデル、Dream-7Bをドラフト器とし、単一NVIDIA A100 80GBで六つの課題群を評価した。

- **2025-01 · [Judge Decoding: Faster Speculative Sampling Requires Going Beyond Model Alignment](2025-2501.19309-judge-decoding-faster-speculative-sampling-requires-going-beyond-model-a.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  Llama-3.1-8Bをドラフト、Llama-3.1-405Bを目標にした実験では、平均受理長が標準方式の6.3から19.7トークンへ伸び、最適化されたgpt-fast上で129.3トークン/秒に達した。

- **2025-07 · [Your LLM Knows the Future: Uncovering Its Multi-Token Prediction Potential](2025-2507.11851-your-llm-knows-the-future-uncovering-its-multi-token-prediction-potentia.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  長い出力ではモデルの実行回数が多くなり、復号の逐次性が遅延の原因になる。提案方式は、入力末尾へ複数のマスク位置を追加し、同一の接頭辞から未来のトークンを予測させる。ただしこの数値は受理トークン数を生成反復数で割った指標であり、壁時計時間で5.35倍高速になったという実測ではない。

- **2025-04 · [PARD: Accelerating LLM Inference with Low-Cost PARallel Draft Model Adaptation](2025-2504.18583-pard-accelerating-llm-inference-with-low-cost-parallel-draft-model-adaptation.md)**  
  実装：[✓](https://github.com/AMD-AIG-AIMA/PARD) ・ リポジトリ内被引用：23  
  PARDは、高精度な小型自己回帰モデルを、1回の順伝播で複数の候補トークンを出す並列下書きモデルへ低コストで適応し、同一モデル系列の複数の対象モデルへ再利用できるようにする投機的復号（投機的復号）方式である。

- **2024-11 · [SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications](2024-2411.04975-suffixdecoding-extreme-speculative-decoding-for-emerging-ai-applications.md)**  
  実装：[✓](https://github.com/snowflakedb/ArcticInference) ・ リポジトリ内被引用：23  
  SuffixDecodingは、大規模言語モデルの生成結果が過去の生成と繰り返し似た文字列になる場面を利用し、追加の草稿モデルを使わずに投機的復号（投機的復号）を高速化する推論基盤技術である。この方式が狙うのは、プログラム修正エージェントの反復試行、複数エージェントによる同形式の応答、SQL生成の定型構造など、同じ接頭辞・後続列が繰り返される作業である。

- **2025-02 · [LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification](2025-2502.17421-longspec-long-context-lossless-speculative-decoding-with-efficient-draft.md)**  
  実装：[✓](https://github.com/sail-sg/LongSpec) ・ リポジトリ内被引用：22  
  投機的復号（投機的復号）は、小さいドラフトモデルが次の候補トークンを先に作り、大きな対象モデルがまとめて検証することで、最終的な出力分布を変えずに生成を高速化する。

- **2025-01 · [Reward-Guided Speculative Decoding for Efficient LLM Reasoning](2025-2501.19324-reward-guided-speculative-decoding-for-efficient-llm-reasoning.md)**  
  実装：[✓](https://github.com/BaohaoLiao/RSD) ・ リポジトリ内被引用：20  
  複雑な数学問題に大規模言語モデルを使うと、最終回答に至るまで何十もの途中式や判断を順番に生成する。高性能な大型モデルだけに全段階を担当させると、簡単な計算の確認にも高価なモデルの演算を費やす。一方、小型モデルだけでは途中の誤りが連鎖して最終回答を損なう。報酬が閾値以上なら草稿を採用し、低ければ草稿を棄却して目標モデルに同じ文脈から次段階を生成させる。

- **2024-11 · [Draft Model Knows When to Stop: Self-Verification Speculative Decoding for Long-Form Generation](2024-2411.18462-draft-model-knows-when-to-stop-a-self-verification-length-policy-for-spe.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  投機的復号は、小型のドラフトモデルが先に数トークンを生成し、大型の対象モデルがまとめて検証することで、対象モデルの逐次実行回数を減らす方式である。著者らはQwen2.5を用いたMT-Benchの最大8K文脈で、固定長より最大17%の高速化を報告する。

- **2025-02 · [Speculative Decoding and Beyond: An In-Depth Survey of Techniques](2025-2502.19732-speculative-decoding-and-beyond-an-in-depth-survey-of-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  本稿は、大規模言語モデル（LLM）の自己回帰復号に伴う逐次依存を、候補列の生成（generation）と修正・検証（refinement）に分離して整理した技術サーベイである。

- **2025-05 · [SpecBranch: Speculative Decoding via Hybrid Drafting and Rollback-Aware Branch Parallelism](2025-2506.01979-specbranch-speculative-decoding-via-hybrid-drafting-and-rollback-aware-branching.md)**  
  実装：[✓](https://github.com/Sylvan820/Specbranch) ・ リポジトリ内被引用：14  
  投機的復号は、この逐次依存を小型のドラフトモデルが候補を先行生成し、大型の対象モデルが複数候補をまとめて検証する方式で緩和する。ICLR 2026掲載版の評価では、複数のドラフト・対象モデル組合せと課題に対し、通常の自己回帰生成比でおおむね1.8〜4.5倍の高速化を報告する。

- **2025-05 · [MoESD: Unveil Speculative Decoding's Potential for Accelerating Sparse MoE](2025-2505.19645-moesd-unveiling-speculative-decodings-potential-for-accelerating-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  投機的復号（投機的復号; SD）は、小型の下書きモデルが複数トークンを先行提案し、大型の対象モデルが一括検証することで、対象モデルの逐次呼び出し回数を減らす。通常の密モデルでは、対象モデルの重みを一度読み込んで複数候補を検証できるため高速化しやすい。

- **2024-12 · [Dovetail: A CPU/GPU Heterogeneous Speculative Decoding for LLM inference](2024-2412.18934-dovetail-cpu-gpu-heterogeneous-speculative-decoding.md)**  
  実装：[✓](https://github.com/ddInference/Dovetail) ・ リポジトリ内被引用：13  
  ターゲットLLMをCPU、深くした小型ドラフトをGPUへ分離し、候補数削減・動的ゲート融合・複数Transformerブロックで低VRAM環境の投機的デコードを高速化する。

- **2025-02 · [GRIFFIN: Effective Token Alignment for Faster Speculative Decoding](2025-2502.11018-griffin-effective-token-alignment-for-faster-speculative-decoding.md)**  
  実装：[✓](https://github.com/hsj576/GRIFFIN) ・ リポジトリ内被引用：12  
  投機的復号（投機的復号）は、小さなドラフトモデルが複数トークンを先に生成し、大きな対象モデルがそれらをまとめて検証することで、対象モデルの順伝播回数を減らす。

- **2025-10 · [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  本論文は、混合専門家（Mixture-of-Experts、MoE）モデルの重みを中央処理装置メモリへ退避する環境で、投機的復号（投機的復号）を併用すると検証段階に多数の専門家が必要となり、中央処理装置から画像処理装置への重み転送が競合する問題を扱う。

- **2025-06 · [Utility-Driven Speculative Decoding for Mixture-of-Experts](2025-2506.20675-cascade.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  MoEでは投機長が増やす専門家読出し費用まで含めた効用を実測し、投機の無効化とK選択を動的に行って最悪減速を5%へ抑える。

- **2025-05 · [Fast and Cost-effective Speculative Edge-Cloud Decoding with Early Exits](2025-2505.21594-fast-and-cost-effective-speculative-edge-cloud-decoding-with-early-exits.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  Cloud 対象の早期出口から暫定トークンを返し、エッジ ドラフトを最終検証と並行して先行生成することで待ち時間を隠し、Jetson Nano＋A100でpre-drafting単体最大11%級の追加改善を示す。

- **2025-02 · [Accelerating LLM Inference with Lossless Speculative Decoding Algorithms for Heterogeneous Vocabularies](2025-2502.05202-accelerating-llm-inference-with-lossless-speculative-decoding-algorithms-for-heterogeneous-vocabularies.md)**  
  実装：[✓](https://github.com/keyboardAnt/hf-bench) ・ リポジトリ内被引用：11  
  対象モデルと提案モデルの語彙が異なっても損失なし投機的復号を可能にし、既製モデルの自由な組合せで自己回帰復号比最大2.8倍高速化する。

- **2025-09 · [SpecVLM: Fast Speculative Decoding in Vision-Language Models](2025-2509.11815-specvlm-fast-speculative-decoding-in-vision-language-models.md)**  
  実装：[✓](https://github.com/haiduo/SpecVLM) ・ リポジトリ内被引用：10  
  SpecVLMは、この視覚特有の律速に対して、EAGLE-2型の軽量候補生成器EagleVLM、質問内容に応じて視覚圧縮方式を選ぶ弾力的視覚圧縮器、対象モデルのロジットと最終直前特徴をその場で教師にするオンライン蒸留を組み合わせる。対象モデルによる並列検証と投機的サンプリングを維持するため、正しい受理・棄却処理を行う限り対象モデルの出力分布を保つ。

- **2025-09 · [FastMTP: Accelerating LLM Inference with Enhanced Multi-Token Prediction](2025-2509.18362-fastmtp-accelerating-llm-inference-with-enhanced-multi-token-prediction.md)**  
  実装：[✓](https://github.com/Tencent-BAC/FastMTP) ・ リポジトリ内被引用：10  
  FastMTPは、複数トークン予測（multi-トークン prediction、MTP）モジュールを推論時の投機的復号に再利用するための学習・実行方式である。

- **2025-07 · [TETRIS: Optimal Draft Token Selection for Batch Speculative Decoding](2025-2502.15197-tetris-optimal-draft-token-selection-for-batch-speculative-decoding.md)**  
  実装：[✓](https://github.com/ZhaoxuanWu/Tetris) ・ リポジトリ内被引用：10  
  投機的復号（投機的復号; SD）で速いドラフトモデルが多めの候補を作り、遅い対象モデルが並列検証する構造はそのままに、対象モデルへ送る候補を要求ごとではなくバッチ全体で選び直す。各要求の連続候補について「そこまで全部受理される確率」を計算し、限られた検証容量 (C) を確率の高い前方トークンへ配る。

- **2025-05 · [DREAM: Drafting with Refined Target Features and Entropy-Adaptive Cross-Attention Fusion for Multimodal Speculative Decoding](2025-2505.19201-dream-drafting-with-refined-target-features-and-entropy-adaptive-cross-a.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/DREAM) ・ リポジトリ内被引用：10  
  投機的復号（投機的復号）は小さな下書きモデルが複数の候補トークンを生成し、大きな検証モデルがまとめて受理判定することで逐次生成の反復回数を減らす。NeurIPS 2025版の評価ではLLaVA-v1.6-Vicuna、Pixtral、SmolVLM、Gemma3を対象とし、A100で通常の自己回帰復号比1.5～3.6倍程度の高速化を報告する。

- **2025-02 · [Fuzzy Speculative Decoding for a Tunable Accuracy-Runtime Tradeoff](2025-2502.20704-fuzzy-speculative-decoding-for-a-tunable-accuracy-runtime-tradeoff.md)**  
  実装：[✓](https://github.com/maxholsman/fsd) ・ リポジトリ内被引用：9  
  標準的な投機的復号（投機的復号; SD）は、小さいドラフトモデルが複数トークンを先に生成し、大きいターゲットモデルがそれらを一括検証することで、ターゲットモデルの逐次実行回数を減らす。たとえばQwen 2.5 7B/32BのGSM8Kでは、標準SDの95.1%・17.4トークン/秒に対し、低閾値FSDは94.7%・21.4トークン/秒となる。

- **2025-10 · [Self Speculative Decoding for Diffusion Large Language Models](2025-2510.04147-self-speculative-decoding-for-diffusion-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  別のモデル重みを載せず、複数位置の候補を一度に予測し、その候補を階層的な検証木としてまとめて実行する。原著はLLaDA系列3モデル、Dream系列2モデルを単一NVIDIA A100 80GBで評価した。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  ドラフトGPU群と対象GPU群を分離して候補木生成と検証を同時実行し、検証済み接頭辞と未検証枝のKVを分けて再利用し、低バッチの同期・起動待ちを減らす投機的デコード。

- **2025-04 · [DEL: Context-Aware Dynamic Exit Layer for Efficient Self-Speculative Decoding](2025-2504.05598-del-context-aware-dynamic-exit-layer-for-efficient-self-speculative-deco.md)**  
  実装：[✓](https://github.com/hoenza/DEL) ・ リポジトリ内被引用：8  
  一般的な投機的復号は、軽い下書きモデルが複数トークンを予測し、重い目標モデルが一括検証する。実測ではLLaMA3-8Bで通常復号比2.62倍、LLaMA2-7Bで2.50倍、LLaMA2-70Bで2.41倍の全体高速化を報告する。

- **2025-04 · [Adaptive Draft-Verification for Efficient Large Language Model Decoding](2025-2407.12021-adaptive-draft-verification-for-efficient-large-language-model-decoding.md)**  
  実装：[✓](https://github.com/liuxukun2000/Adaptix) ・ リポジトリ内被引用：7  
  単一トークンずつの逐次処理は、モデル重みの読み込みやメモリ帯域の費用が大きい。投機的復号（投機的復号）は軽量な提案器で複数の候補トークンを先に作り、対象モデルの一括検証で正しい接頭辞を確定することで、この逐次実行回数を減らす。論文図3は自己回帰比で約1.8〜2.5倍の処理量向上を示す。

- **2024-11 · [Draft on the Fly: Adaptive Self-Speculative Decoding using Cosine Similarity](2024-2410.01028-draft-on-the-fly-adaptive-self-speculative-decoding-using-cosine-similar.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  投機的復号（投機的復号）は、安価なドラフトモデルで候補を数トークン生成し、完全な目標モデルで一括検証することで、この逐次性を緩和する。

- **2025-09 · [Set Block Decoding is a Language Model Inference Accelerator](2025-2509.04185-set-block-decoding-is-a-language-model-inference-accelerator.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  次トークン予測とマスク位置予測を同一Transformerへ統合し、未来ブロックの非連続位置をEB-Samplerで並列確定するSBD。8Bモデルで品質を概ね維持しながら前向き計算回数を約3〜5倍削減し、H100屋根線モデルで実時間化の可能性を分析する。

- **2025-09 · [Bridging Draft Policy Misalignment: Group Tree Optimization for Speculative Decoding](2025-2509.22134-bridging-draft-policy-misalignment-group-tree-optimization-for-speculati.md)**  
  実装：[✓](https://github.com/hsj576/GTO) ・ リポジトリ内被引用：6  
  投機的復号では小型草稿モデルが複数の次トークン候補を先に予測し、大型の対象モデルがまとめて検証する。LLaMA-3.1-8B、Vicuna-13B、DeepSeek-R1-Distill-LLaMA-8B、LLaMA-3.3-70Bなどの対話・コード・数学評価で、EAGLE-3比の平均追加高速化は温度0で7.7%、温度1で5.6%と報告される。

- **2025-06 · [Scaling Speculative Decoding with Lookahead Reasoning](2025-2506.19830-scaling-speculative-decoding-with-lookahead-reasoning.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadReasoning) ・ リポジトリ内被引用：6  
  従来の投機的復号（投機的復号）は小型モデルが未来のトークンを先行提案し、大型目標モデルが複数位置をまとめて検証する。しかし草稿長を増やすほど全トークンが連続して受理される確率が下がり、目標モデルの検証計算も増えるため、速度向上が頭打ちになる。

- **2025-03 · [SPIN: Accelerating Large Language Model Inference with Heterogeneous Speculative Models](2025-2503.15921-spin-heterogeneous-speculative-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  要求難度に応じて異種の小型下書きモデルを選択し、検証バッチのゼロ埋めを要求分解で減らし、下書き生成と標的検証を小バッチ単位で重ねて投機的デコードを高速化する。

- **2025-03 · [Collaborative Speculative Inference for Efficient LLM Inference Serving](2025-2503.10325-collaborative-speculative-inference-for-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  異種GPUへドラフト生成と検証を分離し、専門ドラフタ協調と動的パイプライン制御で投機推論の資源利用と受理率を改善する。

- **2025-04 · [Dynamic-Width Speculative Beam Decoding for LLM Inference](2025-2409.16560-dynamic-width-speculative-beam-decoding-for-llm-inference.md)**  
  実装：[✓](https://github.com/ZongyueQin/DSBD) ・ リポジトリ内被引用：5  
  動的幅投機的ビーム復号（Dynamic-Width 投機的 Beam Decoding; DSBD）は、単一系列の投機的復号（投機的復号）の速度利得と、複数候補系列を保持するビームサンプリング（beam sampling）の品質利得を両立するための方式である。

- **2025-03 · [ML-SpecQD: Multi-Level Speculative Decoding with Quantized Drafts](2025-2503.13565-ml-specqd-multi-level-speculative-decoding-quantized-drafts.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  BF16対象の直接MXFP4版を第一段ドラフトにし、その生成を小型ドラフトで再び投機して、専用ドラフト学習なしに最大2.72倍高速化する。

- **2025-03 · [Gumiho: A Hybrid Architecture to Prioritize Early Tokens in Speculative Decoding](2025-2503.10135-gumiho-a-hybrid-architecture-to-prioritize-early-tokens-in-speculative-decoding.md)**  
  実装：[✓](https://github.com/AMD-AIG-AIMA/Gumiho) ・ リポジトリ内被引用：5  
  したがって、すべての候補位置へ同じ計算量を割り当てるのは必ずしも最善ではない。先頭には過去の未検証トークンの依存関係を使える表現力を割り当て、後続は待ち時間を短縮する。

- **2025-03 · [A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models](2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-la.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  HATは、端末で利用する大規模言語モデルの応答速度と、入力・出力トークンをクラウドへ直接送らない配置を両立するための協調推論方式である。論文全体では比較方式に対して初回応答遅延41～54%、トークン間遅延41～77%の削減を報告する。

- **2025-10 · [HiSpec: Hierarchical Speculative Decoding for LLMs](2025-2510.01336-hispec-hierarchical-speculative-decoding-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HiSpecは、投機的復号の律速が候補トークンの作成ではなく巨大な対象モデルによる検証に移っていることを踏まえ、同じ早期退出モデルの浅い層・中間層・最終層をそれぞれドラフト生成・中間検証・最終検証へ割り当てる階層型の復号方式である。

- **2025-06 · [AdaDecode: Accelerating LLM Decoding with Adaptive Layer Parallelism](2025-2506.03700-adadecode-accelerating-llm-decoding-with-adaptive-layer-parallelism.md)**  
  実装：[✓](https://github.com/weizhepei/AdaDecode) ・ リポジトリ内被引用：4  
  自己回帰型の大規模言語モデル（LLM）は、次トークンを確定するまで次のトークンの入力を処理できない。通常は各トークンを全Transformer層へ順に通し、最終層の語彙分布から出力を決める。長文生成や長い思考過程ではこの直列依存が繰り返される。別の小さなモデルが候補トークンを作る投機的復号（投機的復号）は有力だが、追加モデルの重み・実行費用を要する。

- **2025-05 · [Scaling Laws for Speculative Decoding](2025-2505.07858-scaling-laws-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  投機的復号の速度はドラフトの受理率だけでは決まらない。ドラフト事前学習、層数、対象モデルの検証幅を別々に測り、GPUのメモリ帯域と演算能力の境界に合わせて検証候補を絞る設計を示す。

- **2025-07 · [OmniDraft: A Cross-vocabulary, Online Adaptive Drafter for On-device Speculative Decoding](2025-2507.02659-omnidraft-a-cross-vocabulary-online-adaptive-drafter-for-on-device-specu.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号（投機的復号）は、小型の下書きモデルが提案した複数トークンを大きな対象モデルが一括検証することで、対象モデルの逐次呼出しを減らす。

- **2025-04 · [Token-Driven GammaTune: Adaptive Calibration for Enhanced Speculative Decoding](2025-2504.00030-token-driven-gammatune-adaptive-calibration-for-enhanced-speculative-dec.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  投機的復号では小型ドラフトモデルが先の複数トークンを提案し、大型ターゲットモデルがまとめて検証する。〔原著§3–4〕 SpecBenchの4組のターゲット/ドラフトモデルをH100 80GBで評価した結果、固定長SpecDecodeを基準にした平均処理率はGammaTuneが1.15±0.05倍、GammaTune+が1.16±0.03倍である。

- **2025-10 · [Mirror Speculative Decoding: Breaking the Serial Barrier in LLM Inference](2025-2510.13161-mirror-speculative-decoding-breaking-the-serial-barrier-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ドラフト側は複数の先読み位置を1回の前向き計算で予測する投機ストリーミングを使い、ドラフト自身の逐次依存も短縮する。8台のApple M2 UltraのGPU/NPUを使うSpecBench実験で、Qwen3-32Bの数学推論・温度0では自己回帰基準比5.84倍、EAGLE3は同条件で3.77倍であった。

- **2025-10 · [Correctness Forensics for Batch Speculative Decoding: Diagnosing the Ragged Tensor Problem](2025-2510.22876-correctness-forensics-for-batch-speculative-decoding-diagnosing-the-ragg.md)**  
  実装：[✓](https://github.com/eBay/spec_dec) ・ リポジトリ内被引用：2  
  著者らは、既存のBSPとDSDに重大な同期不良があることを具体的な出力で示し、正当性の検査指標を設計する。論文のA100実験ではEXSpecはバッチサイズ8で最大約3倍の処理量を示す。

- **2025-10 · [CAS-Spec: Cascade Adaptive Self-Speculative Decoding for On-the-Fly Lossless Inference Acceleration of LLMs](2025-2510.26843-cas-spec-cascade-adaptive-self-speculative-decoding-for-on-the-fly-lossl.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号は、安価な草案器が未来のトークンを先に提案し、ターゲットLLMが複数位置を一度に検証することで逐次実行回数を減らす。原著のH100 80GB、Vicuna-7B/13B/33B、Spec-Benchでは、訓練不要のCAS-Specが自己回帰復号比でそれぞれ平均1.578/1.524/1.481倍となる。

- **2025-10 · [Accelerating Mobile Language Model via Speculative Decoding and NPU-Coordinated Execution](2025-2510.15312-accelerating-mobile-language-model-via-speculative-decoding-and-npu-coor.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  sd.npuは、スマートフォン上で検索拡張生成（retrieval-augmented generation; RAG）を動かすとき、モバイル神経処理装置（neural processing unit; NPU）の演算器を使い切れない問題を、実行時制御と推測復号（投機的復号）の両側から解決するシステムである。

- **2025-09 · [Speculative Verification: Exploiting Information Gain to Refine Speculative Decoding](2025-2509.24328-speculative-verification-exploiting-information-gain-to-refine-speculati.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的 検証（SV）は、下書きモデルが生成した候補トークンをtargetモデルへ何個渡すかを、候補が受理される見込みと検証に要するGPU時間から選択する投機的復号の拡張方式である。

- **2025-09 · [Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding](2025-2509.04576-communication-efficient-distributed-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  分散投機的デコードの上り通信を語彙全体分布から上位K疎ロジットへ圧縮し、出力分布を維持したまま通信量と最適ドラフト長を共同最適化する。

- **2025-07 · [Quantize-Sample-and-Verify: LLM Acceleration via Adaptive Edge-Cloud Speculative Decoding](2025-2507.00605-quantize-sample-and-verify-llm-acceleration-via-adaptive-edge-cloud-spec.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  しかし端末とクラウドがネットワークで離れていると、下書きトークンだけでなく検証に必要な確率分布を毎反復で送る必要があり、通信遅延が利点を打ち消す。本論文は、送信確率を量子化する際の処理順序に着目する。評価では、クラウドOPT-13Bと端末側OPT-125M、CNN/DailyMail要約、上り平均350 kbpsと4 Mbpsの二条件を使う。

- **2025-06 · [POSS: Position Specialist Generates Better Draft for Speculative Decoding](2025-2506.03566-poss-position-specialist-generates-better-draft-for-speculative-decoding.md)**  
  実装：[✓](https://github.com/shrango/PosS) ・ リポジトリ内被引用：2  
  PosS（Position Specialists）は、投機的デコードのドラフトモデルが後半の投機位置ほど予測に失敗しやすい問題を、位置別に学習した複数のドラフト層で改善する研究である。最初の位置では対象LLMの正確な隠れ状態を利用できるが、後半の位置では前のドラフトが予測した不完全な特徴を入力にするため、誤差が累積する。

- **2025-06 · [Out-of-Vocabulary Sampling Boosts Speculative Decoding](2025-2506.03206-out-of-vocabulary-sampling-boosts-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、ドラフトモデルと検証対象モデルの語彙が異なる投機的復号に対して、ドラフト側の語彙に存在しないトークンも候補として出せるようにする確率再配分手法RDK（Redistributing Drafter Kernels）を提案する。原著§6では語彙の75%超を削った設定でも、従来の共通語彙だけの方式より受理率が改善することを報告する。

- **2025-05 · [Sparse-to-Dense: A Free Lunch for Lossless Acceleration of Video Understanding in LLMs](2025-2505.19155-sparse-to-dense-a-free-lunch-for-lossless-acceleration-of-video-understa.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  動画を扱う大規模言語モデルでは、数百フレームの映像が数万から十数万の視覚トークンへ展開される。例えば原著が挙げるVILAの設定では、1時間の映像を5秒間隔で720フレーム抽出すると141,120視覚トークンになる。この小さいKV集合で同じモデルを繰り返し実行して候補トークンを作り、元の全KVを使うモデルが候補列をまとめて検証する。

- **2025-05 · [Semi-Clairvoyant Scheduling of Speculative Decoding Requests to Minimize LLM Inference Latency](2025-2505.17074-semi-clairvoyant-scheduling-of-speculative-decoding-requests-to-minimize.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  これは単一リクエストの生成方法の最適化だが、複数リクエストが同じGPUを共有するときには別の問題が残る。従来のスケジューラは、プロンプトから予測した出力長を仕事量の代理変数として使うことが多い。公式会議録は、NVIDIA L20 48GBで3種類のワークロードを用いた評価において、平均推論遅延を既存手法より約39%削減したと報告する。

- **2025-10 · [Polybasic Speculative Decoding Through a Theoretical Perspective](2025-2510.26527-polybasic-speculative-decoding-through-a-theoretical-perspective.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さく速いモデルが将来のトークンを先に提案し、大きなモデルがまとめて検証することで、最終モデルを毎トークン逐次実行する回数を減らす技術である。一方、ドラフト器を大きくすると提案自体の費用が増え、検証回数削減の利得を失う。

- **2025-10 · [FastVLM: Self-Speculative Decoding for Fast Vision-Language Model Inference](2025-2510.22641-fastvlm-self-speculative-decoding-for-fast-vision-language-model-inferen.md)**  
  実装：[✓](https://anonymous.4open.science/r/SSD-575E/README.md) ・ リポジトリ内被引用：1  
  自己回帰デコードでは1トークンごとに大きなデコーダを呼び出す。投機的復号では小さい候補生成器が数トークンを先に作り、大きい本体が一度に検証して、受理した連続トークンを確定する。しかし視覚言語タスクでは、デコーダの浅い層だけを通った特徴から正しいキャプションや回答を予測するのが難しい。

- **2025-09 · [Pipeline Parallelism is All You Need for Optimized Early-Exit Based Self-Speculative Decoding](2025-2509.19368-pipeline-parallelism-is-all-you-need-for-optimized-early-exit-based-self.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己投機的復号では、大規模言語モデルの一部の層だけで次トークンを予測し、同じモデルの残りの層でその候補を検証できる。通常復号比で、PPSDの各構成は平均2.01〜3.08倍、個別の最大値は3.81倍を報告する。

- **2025-09 · [DSDE: Dynamic Speculative Decoding with KLD Stability for Real-World Serving](2025-2509.01083-dsde-dynamic-speculative-decoding-with-kld-stability-for-real-world-serv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  候補長（Speculation Length, SL）を大きくすると受理が続く局面ではtarget呼出しを節約できるが、棄却が多い局面では不要な下書き計算と検証負荷が増える。特にコード生成・対話・要約など異種要求を同じバッチに入れると、全要求に同じSLを固定する方式は一部の要求にとって不利になる。

- **2025-07 · [SpecASR: Accelerating LLM-based Automatic Speech Recognition via Speculative Decoding](2025-2507.18181-specasr-accelerating-llm-based-automatic-speech-recognition-via-speculat.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SpecASRは、大規模言語モデルを復号器に用いる自動音声認識（ASR）の逐次生成を短縮する投機的復号方式である。

- **2025-06 · [Guided Speculative Inference for Efficient Test-Time Alignment of LLMs](2025-2506.04118-guided-speculative-inference-for-efficient-test-time-alignment-of-llms.md)**  
  実装：[✓](https://github.com/j-geuter/GSI) ・ リポジトリ内被引用：1  
  Guided 投機的 Inference（GSI）は、大規模言語モデル（LLM）の推論時に、小型モデルが生成する複数の思考ステップを、大型モデルの確率と報酬モデルの評価で選び直す手法である。Qwen3の候補数16・A100環境では、対象モデルだけでS-BoNを行う方式に対して思考ステップ処理量が約51%高い。

- **2025-05 · [Speculative Decoding Meets Quantization: Compatibility Evaluation and Hierarchical Framework Design](2025-2505.22179-speculative-decoding-meets-quantization-compatibility-evaluation-and-hie.md)**  
  実装：[✓](https://github.com/AI9Stars/SpecMQuant) ・ リポジトリ内被引用：1  
  投機的デコードと量子化は、どちらもLLMの生成を高速化する代表的な方法である。W4A16のLlama-3-70Bを単一A100 80GBで動かしたSpecBenchの六種類の生成タスクでは、HierSpecの最良構成が平均98.19トークン/秒を達成した。

- **2025-05 · [SpecMemo: Speculative Decoding is in Your Pocket](2025-2506.01986-specmemo-memory-aware-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的デコードの候補木・KVキャッシュ・デコードヘッドをGPUメモリ予算に合わせて自動調整し、Titan RTXで生成メモリ65%削減・スループット96%維持、8×MI250のLlama-2-70Bでは通常分散復号比2倍を示す。

- **2025-04 · [Hierarchical Speculative Decoding with Dynamic Windows for Efficient Language Model Inference](2025-d38a1bd0beb3-hierarchical-speculative-decoding-with-dynamic-windows-for-efficient-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの逐次生成では、巨大な対象モデルをトークンごとに呼ぶ費用が大きい。投機的復号（投機的復号）は小型のドラフトモデルに複数の候補を作らせ、対象モデルで一括検証する。これらは対象モデル単独の自己回帰生成を1とした速度倍率であり、別の投機的復号方式に対して常に同じ倍率で勝つという意味ではない。

- **2025-02 · [EasySpec: Layer-Parallel Speculative Decoding for Efficient Multi-GPU Utilization](2025-2502.02493-easyspec-layer-parallel-speculative-decoding-for-efficient-multi-gpu-uti.md)**  
  実装：[✓](https://github.com/Yize-Wu/EasyInfra) ・ リポジトリ内被引用：1  
  EasySpecはこの問題を、ドラフトの「層は必ず下から上へ逐次実行する」という制約を緩めることで解く。学習やモデルの再訓練を必要とせず、層の実行方式とKV管理を変更する。通常の逐次生成に対する最大4.17倍の高速化、ドラフト段階で最大1.62倍の短縮を報告する。

- **2025-10 · [TokenTiming: A Dynamic Alignment Method for Universal Speculative Decoding Model Pairs](2025-2510.15545-tokentiming-a-dynamic-alignment-method-for-universal-speculative-decodin.md)**  
  実装：[✓](https://github.com/SeabirdShore/TokenTiming) ・ リポジトリ内被引用：0  
  投機的復号は小型ドラフトモデルが複数の次トークンを提案し、大型ターゲットモデルがまとめて検証することで自己回帰生成の逐次計算を減らす。

- **2025-10 · [OWL: Overcoming Window Length-Dependence in Speculative Decoding for Long-Context Inputs](2025-2510.07535-owl-overcoming-window-length-dependence-in-speculative-decoding-for-long.md)**  
  実装：[✓](https://anonymous.4open.science/r/owl-BFB8) ・ リポジトリ内被引用：0  
  OWLは、投機的復号（投機的復号）において、入力文脈がドラフトモデルの学習時の長さを超えると候補トークンの受理数が急減する問題を扱う。投機的復号は、小型のドラフトモデルが将来の複数トークンを予測し、大型の対象モデルがそれらをまとめて検証することで、対象モデルの逐次実行回数を減らす。

- **2025-10 · [3-Model Speculative Decoding](2025-2510.12966-3-model-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準的な投機的デコードでは、小さなドラフトモデルが先のトークンを複数予測し、大きなターゲットモデルがまとめて検証する。ドラフトが速くてもターゲットと予測分布が大きく異なれば、検証時に多くの候補が棄却され、期待した高速化が得られない。

- **2025-09 · [Speculate Deep and Accurate: Lossless and Training-Free Acceleration for Offloaded LLMs via Substitute Speculative Decoding](2025-2509.18344-speculate-deep-and-accurate-lossless-and-training-free-acceleration-for-.md)**  
  実装：[✓](https://github.com/NYCU-EDgeAi/subspec) ・ リポジトリ内被引用：0  
  この研究は、GPUメモリにモデル全体が収まらず、一部の層の重みをCPUメモリへ退避するパラメータオフロード（パラメータ オフロード）環境で、生成を高速化する。RTX 4090でGPUメモリを8GBへ制限したQwen2.5-7Bの貪欲生成では、5課題平均で2.68トークン/秒から27.09トークン/秒（10.10倍）へ改善した。

- **2025-09 · [FastEagle: Cascaded Drafting for Accelerating Speculative Decoding](2025-2509.20416-fasteagle-cascaded-drafting-for-accelerating-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  時間方向の逐次生成をモデル内部の層方向のカスケードへ移す設計である。原著Table 1のgreedy生成では、LLaMA3.1-8BのEAGLE-3平均高速化3.94倍に対してFastEagle4.74倍、Vicuna-13Bでは5.01倍から5.67倍となる。

- **2025-08 · [Reward-Shifted Speculative Sampling Is An Efficient Test-Time Weak-to-Strong Aligner](2025-2508.15044-reward-shifted-speculative-sampling-is-an-efficient-test-time-weak-to-st.md)**  
  実装：[✓](https://github.com/lblaoke/CARDS) ・ リポジトリ内被引用：0  
  本論文は、投機的標本化（投機的 sampling）の目的を「大型対象モデルと同じ分布を保って高速化する」ことから、「大型対象モデルを追加学習せず、人間の選好に整合した理想的な大型モデルの分布を生成する」ことへ変更する。従来の投機的標本化では、小型ドラフトモデルが候補トークンを生成し、大型対象モデルの確率との比率で候補を受理する。

- **2025-08 · [CARD: A Cache-Assisted Parallel Speculative Decoding Framework via Query-and-Correct Paradigm for Accelerating LLM Inference](2025-2508.04462-card-cache-assisted-parallel-speculative-decoding-for-efficient-large-la.md)**  
  実装：[✓](https://github.com/hunzhizi/CARD) ・ リポジトリ内被引用：0  
  CARDは、大規模言語モデル（LLM）の投機的復号（投機的復号）で、ドラフトモデルが候補を作り終わるまで対象モデルが待ち、対象モデルが検証している間ドラフトモデルが待つという相互待機を減らす方式である。

- **2025-07 · [FlowSpec: Continuous Pipelined Speculative Decoding for Efficient Distributed LLM Inference](2025-2507.02620-flowspec-continuous-pipelined-speculative-decoding-for-efficient-distrib.md)**  
  実装：[✓](https://github.com/Leosang-lx/FlowSpec) ・ リポジトリ内被引用：0  
  提案法はEAGLE系列の文脈依存投機的復号を基礎に、(1)高い受理見込みを持つ候補を優先して検証するスコア順分割、(2)棄却された投機木の枝を早期に剪定して因果関係を維持する管理、(3)最新の検証結果に基づく継続的な木拡張を組み合わせる。

- **2025-06 · [PredGen: Accelerated Inference of Large Language Models through Input-Time Speculation for Real-Time Speech Interaction](2025-2506.15556-predgen-accelerated-inference-of-large-language-models-through-input-tim.md)**  
  実装：[✓](https://github.com/jacklishufan/PredGen) ・ リポジトリ内被引用：0  
  テキストをトークン単位で逐次出力できても、自然なイントネーションを持つ音声を文単位で合成するなら、第一文が完成するまでの時間（time to first sentence; TTFS）が遅延の主要部分になる。LiとGroverのPredGenは、利用者がまだ発話している時間を、LLM応答の先行計算へ転用することでこの待ち時間を削る。

- **2025-06 · [List-Level Distribution Coupling with Applications to Speculative Decoding and Lossy Compression](2025-2506.05632-list-level-distribution-coupling-with-applications-to-speculative-decodi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小さいドラフトモデルが候補トークンを先に作り、大きい目標モデルがまとめて検証することで、目標モデルの出力分布を変えずに生成を高速化する。

- **2025-05 · [Ghidorah: Fast LLM Inference on Edge with Speculative Decoding and Hetero-Core Parallelism](2025-2505.23219-ghidorah-fast-llm-inference-on-edge-with-speculative-decoding-and-hetero.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Ghidorahは、端末側の単一要求LLMデコードを対象に、投機的復号で増やしたトークン並列性をCPUとGPUの両方で使う推論システムである。著者らはNVIDIA Jetson Xavier NXでVicuna-7BとMedusaを評価し、逐次デコードに対して最大7.6倍の正規化デコード速度を報告する。

- **2025-05 · [Automatic Task Detection and Heterogeneous LLM Speculative Decoding](2025-2505.08600-automatic-task-detection-and-heterogeneous-llm-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一般目的のドラフト1個をすべての問い合わせに使用する代わりに、既存の生成要求からタスク群を自動抽出し、各群に適応したドラフトを用意する TaskSpec を提案する。

- **2025-04 · [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大バッチ投機的デコードの受理率とKV読出し量を実測し、浅くKVを制限したドラフトの性能モデルを構築して、重み読出しよりKV帯域が支配する条件の処理量を比較する研究。

- **2025-03 · [Speculative Decoding for Multi-Sample Inference](2025-2503.05330-speculative-decoding-for-multi-sample-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号 for Multi-サンプル Inferenceは、数学的推論でよく使う自己整合性（自己整合性）やBest-of-N標本化において、同じ大規模言語モデル（LLM）から並列生成している複数の回答候補を、互いの投機的復号（投機的復号）のドラフト供給源として利用する方式である。

- **2024-12 · [A Unified Framework for Speculative Decoding with Multiple Drafters as a Bandit](2024-64007ea4d2a1-a-unified-framework-for-speculative-decoding-with-multiple-drafters-as-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号では、小型のドラフトモデルが先行して複数トークンを予測し、大型のターゲットモデルが一括で検証する。黒箱のコードでは自己回帰比2.300倍、Mathでは2.280倍、白箱のコードでは3.724倍だった。

- **2024-11 · [SAM Decoding: Speculative Decoding via Suffix Automaton](2024-2411.10666-sam-decoding-speculative-decoding-via-suffix-automaton.md)**  
  実装：[✓](https://github.com/hyx1999/SAM-Decoding) ・ リポジトリ内被引用：0  
  投機的デコードは、軽い手段で複数の候補トークンを先に提案し、元の大きなモデルがまとめて検証することで生成時間を減らす。Vicuna-7B-v1.3、RTX A6000、バッチ1、貪欲生成のSpec-Benchで、通常生成比の速度倍率はPLDの1.56倍に対しSAM-Decodingが1.84倍だった。

### 3年前（2023-11〜2024-10）

- **2024-01 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)**  
  実装：[✓](https://github.com/FasterDecoding/Medusa) ・ リポジトリ内被引用：434  
  Medusaは、対象LLMの隠れ状態に未来位置ごとの小型予測ヘッドを追加し、上位候補を木構造へまとめて一括検証することで、別ドラフトモデルを置かず対象モデルの逐次呼出しを減らす。

- **2024-01 · [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：365  
  EAGLEは、対象LLMの上位層特徴量と直前に標本化したトークンを小型デコーダへ与えて未来特徴量を予測し、元の言語モデル出力ヘッドと木構造検証で重み読出し回数を減らす。

- **2024-06 · [EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](2024-2406.16858-eagle-2.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：210  
  EAGLE-2は、既存のEAGLEで用いる小型の下書きモデルをそのまま使いながら、投機的復号（投機的復号）で検証する候補木の形を入力文脈に応じて変える手法である。代表的な温度0のVicuna 7B・MT-benchでは通常生成比3.62倍、既存EAGLEは2.90倍であり、平均受理長はそれぞれ4.98と3.94トークンである。

- **2024-02 · [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadDecoding) ・ リポジトリ内被引用：175  
  先読みデコードは、対象LLMを未来位置へ並列反復して途中の正しい短いトークン列を蓄積し、現在接頭辞に合う候補を一括検証して、追加モデルなしに逐次ステップとメモリ帯域待ちを減らす。

- **2023-11 · [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)**  
  実装：[✓](https://github.com/FasterDecoding/REST) ・ リポジトリ内被引用：130  
  RESTは、現在文脈末尾と一致する過去トークン列を接尾辞索引から検索し、その続き候補を木構造へ集約して対象LLMで一括検証し、ドラフトモデルなしで反復的なコードの対象重み読出しを減らす。

- **2024-07 · [Online Speculative Decoding](2023-2310.07177-online-speculative-decoding.md)**  
  実装：[✓](https://github.com/LiuXiaoxuanPKU/OSD) ・ リポジトリ内被引用：103  
  投機的復号で得られる目標モデルの確率分布を教師信号として下書きモデルをオンライン更新し、問い合わせ分布の変化に追従して受理率と推論速度を高める方式。

- **2024-04 · [Better & Faster Large Language Models via Multi-token Prediction](2024-2404.19737-better-faster-large-language-models-via-multi-token-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：93  
  一般的な自己回帰言語モデルは、各位置までの文脈から直後の一つのトークンを予測する。これに対して複数トークン予測（Multi-トークン Prediction; MTP）は、同じ位置の共有表現から、1個先だけでなく2個先、3個先、4個先など複数の未来トークンを別々の出力ヘッドで予測するよう学習する。この研究には二つの独立した成果がある。

- **2024-02 · [Hydra: Sequentially-Dependent Draft Heads for Medusa Decoding](2024-2402.05109-hydra-sequentially-dependent-draft-heads-for-medusa-decoding.md)**  
  実装：[✓](https://github.com/zankner/Hydra) ・ リポジトリ内被引用：92  
  投機的復号（投機的復号）は、安価な下書きモデルが複数の将来トークンを予測し、元の大きな言語モデルが候補をまとめて検証することで、1回の高価な順伝播で複数トークンを確定させる。単一要求のVicuna 7B/13B/33Bで通常の自己回帰生成に対しそれぞれ2.70/2.50/2.53倍、Medusaに対し1.27/1.27/1.31倍の処理率を報告する。

- **2024-02 · [Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding](2024-2402.12374-sequoia-scalable-robust-and-hardware-aware-speculative-decoding.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/Sequoia) ・ リポジトリ内被引用：81  
  自己回帰型の大規模言語モデル（LLM）は、1 トークンを確定するたびに大きな対象モデルを1回実行するため、生成の逐次依存が遅延の下限になる。また、標本化温度が変わるとドラフト分布と対象分布の重なり方が変わり、固定的な木構造・検証方式は性能が不安定になる。

- **2024-08 · [MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding](2025-2408.11049-magicdec-breaking-the-latency-throughput-tradeoff-for-long-context-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：64  
  長文脈と大きなバッチを同時に扱うと、KVキャッシュの転送が推論を律速し、投機的復号の検証費用が相対的に小さくなる。MagicDecは疎KVドラフトと受理率・計算費用の解析を組み合わせ、従来の「大バッチでは投機が不利」という通説の成立範囲を明確にする。

- **2024-04 · [TriForce: Lossless Acceleration of Long Sequence Generation with Hierarchical Speculative Decoding](2024-2404.11912-triforce-lossless-acceleration-of-long-sequence-generation-with-hierarch.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/TriForce) ・ リポジトリ内被引用：64  
  長文脈のKVキャッシュ読込を減らす近似的な中間検証と、完全KVによる厳密な最終検証を分離することで、長系列の投機的復号を高速化する。

- **2024-05 · [SpecDec++: Boosting Speculative Decoding via Adaptive Candidate Lengths](2024-2405.19715-specdec-boosting-speculative-decoding-via-adaptive-candidate-lengths.md)**  
  実装：[✓](https://github.com/Kaffaljidhmah2/SpecDec_pp) ・ リポジトリ内被引用：60  
  SpecDec++は、大きな対象モデルの出力分布を保持する投機的復号（投機的復号）において、小さなドラフトモデルが何トークン先まで候補を作ってから対象モデルに検証させるかを、生成の途中で動的に決める手法である。

- **2024-08 · [PEARL: Parallel Speculative Decoding with Adaptive Draft Length](2024-2408.11850-pearl-parallel-speculative-decoding-with-adaptive-draft-length.md)**  
  実装：[✓](https://github.com/smart-lty/ParallelSpeculativeDecoding) ・ リポジトリ内被引用：53  
  投機的復号は、小さなドラフトモデルが先の複数トークンを予測し、大きな対象モデルがそれらを一回の順伝播でまとめて検証する。一次論文の2024年9月版では、コード生成、算術推論、複数ターン対話の実験で、自己回帰生成比最大3.79倍、通常の投機的復号比最大1.52倍の高速化を報告する。

- **2024-02 · [Decoding Speculative Decoding](2024-2402.01528-decoding-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：52  
  350件超の投機的デコード実験からドラフト遅延と層深度を主要因と特定し、浅く広いドラフトモデルへ再設計して最大111%のスループット向上を示す。

- **2024-04 · [Kangaroo: Lossless Self-Speculative Decoding for Accelerating LLMs via Double Early Exiting](2024-2404.18911-kangaroo-lossless-self-speculative-decoding-via-double-early-exiting.md)**  
  実装：[✓](https://github.com/Equationliu/Kangaroo) ・ リポジトリ内被引用：51  
  一般的な方式では、対象モデルとよく似た予測を出す小型ドラフトモデルを別途学習・配置する必要がある。NeurIPS 2024最終版では単一系列検証だけでなく動的な木状候補にもこの二段目の早期終了を拡張し、Spec-BenchでVicuna-7B平均1.72倍、Vicuna-13B平均1.65倍、最大2.04倍の壁時計高速化を報告する。

- **2024-08 · [Learning Harmonized Representations for Speculative Sampling](2024-2408.15766-learning-harmonized-representations-for-speculative-sampling.md)**  
  実装：[✓](https://github.com/HArmonizedSS/HASS) ・ リポジトリ内被引用：50  
  HASSはEAGLE-2の投機的復号で、下書きモデルの学習時には正しい対象モデルの隠れ状態が見えるが、生成時には自己予測した不正確な状態を使うという文脈不一致を解消する。H800・バッチ1の四種類のLLaMAと三課題で自己回帰比2.81〜4.05倍の実時間高速化を示す一方、学習時間はEAGLE-2比平均66.34%増加する。

- **2024-06 · [OPT-Tree: Speculative Decoding with Adaptive Draft Tree Structure](2024-2406.17276-opt-tree-speculative-decoding-with-adaptive-draft-tree-structure.md)**  
  実装：[✓](https://github.com/Jikai0Wang/OPT-Tree) ・ リポジトリ内被引用：49  
  OPT-Treeは、投機的復号（投機的復号）で草稿モデルが作る候補の木構造を、各生成ステップの予測確率に応じて変える方式である。実験では対象モデルと草稿モデルの組合せによって最大約3.2倍の生成処理率改善を報告する。

- **2023-12 · [Cascade Speculative Drafting for Even Faster LLM Inference](2023-2312.11462-cascade-speculative-drafting-for-even-faster-llm-inference.md)**  
  実装：[✓](https://github.com/lfsszd/CS-Drafting) ・ リポジトリ内被引用：48  
  ChenらのCascade 投機的 Drafting（CS Drafting）は、下書きモデルの生成をさらに小さなモデルによる投機で加速する縦方向の連鎖（Vertical Cascade）と、候補列の位置ごとに異なる計算費の下書きモデルを割り当てる横方向の連鎖（Horizontal Cascade）を組み合わせる。

- **2024-10 · [SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration](2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleratio.md)**  
  実装：[✓](https://github.com/hemingkx/SWIFT) ・ リポジトリ内被引用：47  
  したがって本研究は「精度を下げて速くする層削減」ではなく、「一時的な近似ドラフトで正確な検証を少ない回数にする」方式である。LLaMA-2-13Bでは通常自己回帰の20.10トークン/秒に対して28.26トークン/秒、全体1.41倍、LLaMA-2-70Bでは4.32に対して6.41トークン/秒、1.48倍を報告する。

- **2024-01 · [Multi-Candidate Speculative Decoding](2024-2401.06706-multi-candidate-speculative-decoding.md)**  
  実装：[✓](https://github.com/NJUNLP/MCSD) ・ リポジトリ内被引用：35  
  標準方式では各深さに一つの候補しかない。したがって、研究の核は「候補幅による受理率向上」「分布保存の検証」「共有接頭辞による検証費用削減」の三点である。

- **2024-03 · [Recurrent Drafter for Fast Speculative Decoding in Large Language Models](2024-2403.09919-recurrent-drafter-for-fast-speculative-decoding-in-large-language-models.md)**  
  実装：[✓](https://github.com/apple/ml-recurrent-drafter) ・ リポジトリ内被引用：34  
  軽量再帰型の下書きモデル、ビーム探索、動的な共有接頭辞除去、対象モデルからの知識蒸留を組み合わせる。受理トークン数が多くても処理率が上がるとは限らないことを、実測の正負両結果から検証する。

- **2024-06 · [SpecExec: Massively Parallel Speculative Decoding for Interactive LLM Inference on Consumer Devices](2024-2406.02532-specexec-massively-parallel-speculative-decoding-for-interactive-llm-inference-on-consumer-devices.md)**  
  実装：[✓](https://github.com/yandex-research/specexec) ・ リポジトリ内被引用：33  
  RAMオフロードでは「対象モデルを1トークン通す時間」と「数百〜数千トークンをまとめて通す時間」の差が小さくなる。SpecExecはその余剰バッチ幅で将来分布を事前計算し、70B級モデルを消費者GPUでも数トークン/sで対話可能にする。

- **2024-05 · [Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models](2024-2405.04304-dynamic-speculation-lookahead-accelerates-speculative-decoding-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  投機的復号（投機的復号）は、安価な下書きモデルが将来トークンを自己回帰的に生成し、対象モデルが複数候補を一括検証することで推論時間を短縮する。

- **2024-03 · [Block Verification Accelerates Speculative Decoding](2024-2403.10444-block-verification-accelerates-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  各接頭辞の受理確率を適切に設計し、受理された中で最も長い接頭辞を確定させる。PaLM-2-Sを対象、PaLM-2-XXSを下書きとし、候補長8、8種類のデータセットで測った結果、対象モデル一回当たりの生成量を示すブロック効率は平均3.41から3.70へ増え、標準検証に対して8.30%改善した。

- **2024-02 · [Speculative Streaming: Fast LLM Inference without Auxiliary Models](2024-2402.11131-speculative-streaming-fast-llm-inference-without-auxiliary-models.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  本論文の課題は、大規模言語モデルの自己回帰復号が一トークンずつ重みを読み込むため、演算器の能力を使い切れないことにある。投機的復号では小さな下書きモデルが将来トークンを先読みし、大きな対象モデルが候補をまとめて検証する。

- **2024-10 · [DySpec: Faster Speculative Decoding with Dynamic Token Tree Structure](2024-2410.11744-dyspec-faster-speculative-decoding-with-dynamic-token-tree-structure.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  一覧用要約：DySpecは下書きモデルの確率分布から候補の受理見込みを近似し、受理後の子候補と拒否後の兄弟候補を優先度付きキューで動的に展開する。閾値付き層単位生成で下書き呼出しを抑え、Llama2-70BのCPUオフロード条件では対象モデル呼出し回数の削減により大きな速度改善を得る。

- **2024-04 · [On Speculative Decoding for Multimodal Large Language Models](2024-2404.08856-on-speculative-decoding-for-multimodal-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  この部分は小バッチ時にメモリ帯域が律速になりやすく、画像理解モデルであっても文章LLMと同じ問題を抱える。従来の投機的復号では、小型モデルが数トークンを予測し、大型モデルがその候補を一括検証する。論文の最大2.37倍は、メモリ律速を仮定して計算した高速化指標（MBSU）であり、実際に計測したトークン率の倍率と混同してはならない。

- **2023-12 · [Lookahead: An Inference Acceleration Framework for Large Language Model with Lossless Generation Accuracy](2023-2312.12728-lookahead-an-inference-acceleration-framework-for-large-language-model-w.md)**  
  実装：[✓](https://github.com/alipay/PainlessInferenceAcceleration) ・ リポジトリ内被引用：23  
  Lookaheadは、この空きを利用して過去の生成履歴から複数の継続候補を構成し、一回の対象モデル計算で複数トークンを確定する推論高速化方式である。

- **2024-10 · [AdaEDL: Early Draft Stopping for Speculative Decoding of Large Language Models via an Entropy-based Lower Bound on Token Acceptance Probability](2024-2410.18351-adaedl-early-draft-stopping-for-speculative-decoding-of-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  追加の停止予測ネットワークを学習しない点が、学習型の適応長方式との主要な違いである。単一NVIDIA A100 80GB・FP32で、Llama2-7Bを対象、直接整合済みの115M下書きを用いたCNN-DM要約では、最大下書き長16の固定方式36.30 トークン/sに対し54.10 トークン/sを報告する。

- **2024-02 · [Ouroboros: Generating Longer Drafts Phrase by Phrase for Faster Speculative Decoding](2024-2402.13720-ouroboros-generating-longer-drafts-phrase-by-phrase-for-faster-speculati.md)**  
  実装：[✓](https://github.com/thunlp/Ouroboros) ・ リポジトリ内被引用：22  
  通常の投機的復号（投機的復号）では、対象となる大規模言語モデル（対象モデル）より小さい下書きモデル（下書きモデル）が数トークンを先読み生成し、対象モデルがそれらを一度に検証する。

- **2024-02 · [Recursive Speculative Decoding: Accelerating LLM Inference via Sampling Without Replacement](2024-2402.14160-recursive-speculative-decoding-accelerating-llm-inference-via-sampling-w.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  投機的復号は小さいドラフトモデルで先のトークンを予測し、大きい対象モデルにまとめて検証させることで、対象モデルの逐次実行回数を減らす。Llama 2-7Bと115Mドラフトを使ったXSumの評価では、通常の逐次復号37.269トークン/秒に対し、RSD-Cの2-2分岐は56.609トークン/秒を報告する。

- **2024-10 · [ParallelSpec: Parallel Drafter for Efficient Speculative Decoding](2024-2410.05589-parallelspec-parallel-drafter-for-efficient-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  投機的復号（投機的復号）は、小さな下書きモデルが複数トークンの候補を作り、大きな対象モデルがまとめて検証することで、大きなモデルを毎トークン実行する費用を減らす。

- **2024-02 · [Generation Meets Verification: Accelerating Large Language Model Inference with Smart Parallel Auto-Correct Decoding](2024-2402.11809-generation-meets-verification-accelerating-large-language-models-with-speculative-decoding.md)**  
  実装：[✓](https://github.com/cteant/SPACE) ・ リポジトリ内被引用：19  
  SPACE（Smart Parallel Auto-Correct デコード）は、自己回帰（autoregressive）型の大規模言語モデルを、別の小型下書きモデルを使わずに高速化する投機的復号方式である。論文は6B～70B級の複数モデルを評価し、HumanEval-Xのコード生成では2.71～4.04倍の高速化を報告する。

- **2024-10 · [A Theoretical Perspective for Speculative Decoding Algorithm](2024-2411.00841-a-theoretical-perspective-for-speculative-decoding-algorithm.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  小型モデルが候補トークンを提案し、大型モデルが並列に検証する方式では、候補が多く受理されるほど大型モデルの逐次呼出しが減る。定理3は複数のドラフト列を同時に検証するバッチ方式の不偏性と改善量を与える。

- **2024-08 · [Dynamic Depth Decoding: Faster Speculative Decoding for LLMs](2024-2409.00142-dynamic-depth-decoding-faster-speculative-decoding-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  投機的復号では軽量なドラフトモデルが複数候補を先に提案し、目標モデルがまとめて検証することで目標モデルの呼び出し当たりの確定トークン数を増やす。論文の単一NVIDIA A40での実験では、4モデルで自己回帰比3.09〜3.22倍の高速化、EAGLE-2比平均約4%の改善を報告する。

- **2024-04 · [Lossless Acceleration of Large Language Model via Adaptive N-gram Parallel Decoding](2024-2404.08698-lossless-acceleration-of-large-language-model-via-adaptive-n-gram-parall.md)**  
  実装：[✓](https://github.com/oujieww/ANPD) ・ リポジトリ内被引用：11  
  適応的N-gram並列復号（適応的 N-gram Parallel Decoding; ANPD）は、大規模言語モデル（LLM）を自己回帰で1トークンずつ実行する代わりに、安価なN-gram表で数トークンの候補を先に作り、元のLLMでまとめて検証する手法である。

- **2024-10 · [Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution](2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  複数小型モデルの重み付き多数決、オンライン投機長調整、SSM/LLM非同期パイプラインを統合した投機的復号サービング。

- **2024-04 · [BASS: Batched Attention-optimized Speculative Sampling](2024-2404.15778-bass.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  系列ごとに異なる投機受理長を保ったまま注意計算をバッチ化し、動的ドラフト長調整で複数応答の遅延とGPU利用率を改善する方式。

- **2024-10 · [AMUSD: Asynchronous Multi-Device Speculative Decoding for LLM Acceleration](2024-2410.17375-amusd-asynchronous-multi-device-speculative-decoding-for-llm-acceleratio.md)**  
  実装：[✓](https://github.com/BradMcDanel/AMUSD) ・ リポジトリ内被引用：9  
  二つのモデルを別々のGPUへ配置しても、この実行順序を変えなければGPUを同時に使い切れない。平均トークン時間は、自己回帰生成に対してHumanEvalで1.57倍、MT-Benchで1.31倍、RefactorChatで1.96倍の高速化となった。

- **2024-02 · [Guiding LLMs The Right Way: Fast, Non-Invasive Constrained Generation](2024-2403.06988-guiding-llms-the-right-way-fast-non-invasive-constrained-generation.md)**  
  実装：[✓](https://github.com/eth-sri/domino) ・ リポジトリ内被引用：8  
  制約付き復号（constrained デコード）は、各生成段階で許される次トークンを文法で絞り、出力の構文的な妥当性を保証する。これが単なる書式上の違いにとどまらず、推論問題の正解率を損なうことを本論文は実験で示した。提案するDOMINOは、文法を解釈する字句解析器（scanner）と構文解析器（parser）を分ける。

- **2024-10 · [QSpec: Speculative Decoding with Complementary Quantization Schemes](2024-2410.11305-qspec-speculative-decoding-with-complementary-quantization-schemes.md)**  
  実装：[✓](https://github.com/hku-netexplo-lab/QSpec) ・ リポジトリ内被引用：7  
  QSPECが解決するのは、4ビット重みの言語モデルを動かす際に、活性化も4ビットへ落とすと演算は軽くなるものの、複数段階の推論やコード生成の正確さが損なわれるという問題である。著者は活性化まで4ビットにした実行経路を候補トークンの提案に限定し、同じ重みを活性化16ビットで計算する経路に採否の最終決定を任せる。

- **2024-05 · [Clover: Regressive Lightweight Speculative Decoding with Sequential Knowledge](2024-2405.00263-clover-regressive-lightweight-speculative-decoding-with-sequential-knowl.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  特に要求数が少ないと計算器よりメモリ転送が支配的になり、GPUの演算能力を十分に使えない。投機的復号（投機的復号）は、軽量な予測器が複数トークンを先に推測し、元の大規模モデルでまとめて検証することで、重み読出し当たりの確定トークン数を増やす。

- **2024-05 · [Nearest Neighbor Speculative Decoding for LLM Generation and Attribution](2024-2405.19325-nearest-neighbor-speculative-decoding-for-llm-generation-and-attribution.md)**  
  実装：[✓](https://github.com/facebookresearch/NEST) ・ リポジトリ内被引用：6  
  対象：外部コーパスの根拠に基づく生成と複数トークンの投機的復号を統合する半パラメトリック推論。一次資料はNeurIPS 2024掲載論文のarXiv第3版（2025年4月25日）。標準的な分布保存型の投機的復号と区別する。

- **2024-10 · [Temperature-Centric Investigation of Speculative Decoding with Knowledge Distillation](2024-2410.10141-temperature-centric-investigation-of-speculative-decoding-with-knowledge-distillation.md)**  
  実装：[✓](https://github.com/ozyyshr/TempSpec) ・ リポジトリ内被引用：2  
  対象モデルの重みや注意機構を変えるのではなく、下書きモデルと対象モデルの出力分布の整合を、蒸留データの生成条件から改善する研究である。さらに、目的の復号温度に近い複数温度で生成した蒸留データを混合する方式を提案し、温度0.8のGSM8Kではオフライン蒸留の通常復号比4.93倍を5.62倍へ改善した。

- **2024-08 · [CREST: Effectively Compacting a Datastore For Retrieval-Based Speculative Decoding](2024-2408.04678-crest-effectively-compacting-a-datastore-for-retrieval-based-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CREST（Compact Retrieval-Based 投機的復号）は、RESTの全文保存方式を改め、短くて頻出するn-gramをキー、そこから生成した候補トークン木を値とする辞書を保持する。原著は、RESTと同等の受理長を10.6〜13.5倍小さな容量で達成し、同じ容量では受理長を16.5〜17.1%改善したと報告する。

- **2024-08 · [Context-Aware Assistant Selection for Improved Inference Acceleration with Large Language Models](2024-2408.08470-context-aware-assistant-selection-for-improved-inference-acceleration-wi.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号（投機的復号）は小さなドラフトモデルが複数トークンを先読みし、大きな対象モデルがまとめて検証することで逐次生成の遅延を削減する。

- **2024-10 · [Cerberus: Efficient Inference with Adaptive Parallel Decoding and Sequential Knowledge Enhancement](2024-2410.13344-cerberus-efficient-inference-with-adaptive-parallel-decoding-and-sequent.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  また、受理候補が少ない難しいステップでも木構造の検証を行うと、予測ヘッド・木検証の追加費用だけが残る。Cerberusは、各予測ヘッドの残差ブロック同士を接続するCerberus Headsと、エントロピーに応じて並列復号と通常復号を切り替えるゲートを組み合わせる。木候補63では通常復号比2.12倍の高速化を報告する。

- **2024-05 · [EMS-SD: Efficient Multi-sample Speculative Decoding for Accelerating Large Language Models](2024-2405.07542-ems-sd-efficient-multi-sample-speculative-decoding-for-accelerating-larg.md)**  
  実装：[✓](https://github.com/niyunsheng/EMS-SD) ・ リポジトリ内被引用：1  
  EMS-SDは、複数要求を一度に処理する投機的復号（投機的復号）で、要求ごとに草稿の受理数や予測長が違うために生じる無駄な埋め草トークン（padding）を除く実装方式である。非投機的な貪欲復号468.89との比較では、従来1.37倍、提案2.17倍である。

- **2024-07 · [S2D: Sorted Speculative Decoding For More Efficient Deployment of Nested Large Language Models](2024-2407.01955-s2d-sorted-speculative-decoding-for-more-efficient-deployment-of-nested-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号は、小さなドラフトモデルが先の複数トークンを予測し、大きな対象モデルがそれらを一括検証することで、逐次デコードに必要な対象モデルの実行回数を減らす。Spec-BenchのMT-Bench評価では、3対象×greedy/非greedyの6条件における自己回帰生成比の単純平均高速化が1.55倍であった（Table 2）。

- **2024-03 · [SDSAT: Accelerating LLM Inference through Speculative Decoding with Semantic Adaptive Tokens](2024-2403.18647-sdsat-accelerating-llm-inference-through-speculative-decoding-with-seman.md)**  
  実装：[✓](https://github.com/ainergy-ml/SDSAT) ・ リポジトリ内被引用：0  
  単一要求・小バッチではメモリ帯域に律速されやすく、GPUの演算能力が十分でもトークンを逐次確定する依存関係が残る。投機的復号は複数の候補トークンを先読みし、検証をまとめることで逐次処理の回数を減らす。

### 4年前（2022-11〜2023-10）

- **2022-11 · [Fast Inference from Transformers via Speculative Decoding](2022-2211.17192-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：624  
  軽量モデルの複数トークン提案を対象モデルで並列検証し、出力分布を変えずに直列復号回数を削減する投機的復号の基礎研究。

- **2023-02 · [Accelerating Large Language Model Decoding with Speculative Sampling](2023-2302.01318-speculative-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：457  
  小型モデルの複数候補を大型モデルで並列検証し、出力分布を変えず700億パラメータモデルのデコードを最大約2.5倍高速化。

- **2023-05 · [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)**  
  実装：[✓](https://github.com/flexflow/FlexFlow) ・ リポジトリ内被引用：208  
  SpecInferは、小型モデル群が先に作る複数候補を共通接頭辞の木へまとめ、対象LLMを1回で木構造検証することで、逐次デコードの対象重み読出しとGPU間通信を減らし、複数トークンを確定する。

- **2023-09 · [Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding](2023-2309.08168-draft-verify.md)**  
  実装：[✓](https://openreview.net/attachment?id=ACC2nQYzPYS&name=software) ・ リポジトリ内被引用：157  
  元モデルの中間層を一時的に飛ばして下書きを生成し、完全モデルで一括検証することで、追加下書きモデルなしに最大約2倍の損失なしデコード高速化を実現する。

- **2023-10 · [DistillSpec: Improving Speculative Decoding via Knowledge Distillation](2023-2310.08461-distillspec-improving-speculative-decoding-via-knowledge-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：142  
  ドラフト自身の生成データと課題別の分布間距離でターゲットとの整合を蒸留し、投機的デコードの候補受理率を上げる手法。

- **2023-02 · [Speculative Decoding with Big Little Decoder](2023-2302.07863-speculative-decoding-with-big-little-decoder.md)**  
  実装：[✓](https://github.com/kssteven418/BigLittleDecoder) ・ リポジトリ内被引用：87  
  Big Little Decoder（BiLD）は、小型モデルに自己回帰生成を任せ、予測が難しいときだけ大型モデルへフォールバックする。大型モデルは小型モデルが直前まで作った区間をまとめて評価し、不一致が大きい位置までロールバックして修正する。mT5/T5の翻訳・要約でNVIDIA T4上最大2.12倍高速化する。

- **2023-08 · [Accelerating LLM Inference with Staged Speculative Decoding](2023-2308.04623-accelerating-llm-inference-with-staged-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：84  
  本研究は投機的復号（投機的復号）の候補を一本の直線ではなく木構造へ広げ、さらに小型のドラフトモデルも別の極小モデルで投機実行する「段階投機的復号」を提案する。段階投機は通常比3.16倍、標準投機比1.36倍である。

- **2023-10 · [SpecTr: Fast Speculative Decoding via Optimal Transport](2023-2310.15141-spectr-fast-speculative-decoding-via-optimal-transport.md)**  
  実装：✓ ・ リポジトリ内被引用：80  
  大規模言語モデルの通常の自己回帰復号は、次のトークンを一つ出すたびに大きなモデルの前向き計算を必要とする。投機的復号（投機的復号）は小さな下書きモデルで将来のトークン列を先に作り、大きな検証モデルでまとめて採否を調べる。採択されたトークンを一度の検証で複数確定できれば、利用者が一つの回答を受け取るまでの時間を短縮できる。

- **2023-10 · [SPEED: Speculative Pipelined Execution for Efficient Decoding](2023-2310.12072-speed-speculative-pipelined-execution-for-efficient-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  周期的に同じ重みを繰り返し使用する復号器で、途中層から未来トークンを先読みし、複数の系列位置を同一の重み行列で並行処理する。投機予測が変わったときは後続処理と鍵・値キャッシュを巻き戻し、深い共有モデルの出力を維持する。

- **2023-07 · [Predictive Pipelined Decoding: A Compute-Latency Trade-off for Exact LLM Decoding](2023-2307.05908-predictive-pipelined-decoding-a-compute-latency-trade-off-for-exact-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  予測パイプライン復号（Predictive Pipelined Decoding; PPD）は、自己回帰型の大規模言語モデルが次のトークンを確定するまで、その次のトークンの計算を開始できないという逐次依存を緩める方式である。

### 5年前（2021-11〜2022-10）

- **2022-03 · [Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation](2022-2203.16487-speculative-decoding-exploiting-speculative-execution-for-accelerating-s.md)**  
  実装：[✓](https://github.com/hemingkx/SpecDec) ・ リポジトリ内被引用：74  
  提案の中核は、入力を読むエンコーダを深く、反復生成するデコーダを浅くした独立の候補生成モデル「Spec-Drafter」と、候補を対象モデルでまとめて確かめる「Spec-検証」である。
<!-- survey:auto:end -->
