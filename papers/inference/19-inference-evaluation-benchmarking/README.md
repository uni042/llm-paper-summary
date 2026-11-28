<!-- survey:auto:start -->
## 自動生成の論文一覧（284本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/19-inference-evaluation-benchmarking/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-03 · [AIMER: Calibration-Free Task-Agnostic MoE Expert Pruning](2026-2603.18492-aimer-calibration-free-task-agnostic-moe-expert-pruning.md)**  
  実装：[✓](https://github.com/ZongfangLiu/AIMER) ・ リポジトリ内被引用：10  
  特にGPUメモリが限られる場合、未使用時間の長い専門家であっても保存・読込み費用がかかる。この方式は代表入力の分布に依存し、校正用入力の収集・推論・統計保存が必要となる。Qwen3-30Bの専門家50%削減ではコード評価平均がAIMERで0.361、REAPで0.046となった。

- **2025-12 · [Less Is More, but Where? Dynamic Token Compression via LLM-Guided Keyframe Prior](2025-2512.06866-less-is-more-but-where-dynamic-token-compression-via-llm-guided-keyframe.md)**  
  実装：[✓](https://github.com/yu-lin-li/DyToK) ・ リポジトリ内被引用：6  
  映像が長くなると入力トークン数が増え、自己注意と全結合層の計算費用、入力事前充填の遅延、メモリ消費が増える。既存の視覚トークン圧縮は、各フレームに同じ保持率を適用する場合が多い。

- **2026-05 · [Stop When Reasoning Converges: Semantic-Preserving Early Exit for Reasoning Models](2026-2605.17672-stop-when-reasoning-converges-semantic-preserving-early-exit-for-reasoni.md)**  
  実装：[✓](https://github.com/giovanni-vaccarino/PUMA) ・ リポジトリ内被引用：4  
  PUMAは、推論モデルが問題を解き終えた後も思考を繰り返す「過剰思考」を減らすための推論時早期終了方式である。

- **2026-04 · [Watt Counts: Energy-Aware Benchmark for Sustainable LLM Inference on Heterogeneous GPU Architectures](2026-2604.09048-watt-counts-energy-aware-benchmark-for-sustainable-llm-inference-on-hete.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  逆に常時待機する低負荷サーバでは、ピーク処理能力よりアイドル時の消費電力が支配的になり、別のGPUが有利になり得る。Watt Countsは、こうしたモデル、GPU、運用負荷の三者の相互作用を比較するための公開データセットと測定基盤を提案する。

- **2026-03 · [Characterizing Performance-Energy Trade-offs of Large Language Models in Multi-Request Workflows](2026-2604.09611-characterizing-performance-energy-trade-offs-of-large-language-models-in.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  新しい推論カーネルの提案ではなく、既存の推論基盤をどの条件でどう設定すると効率が変わるかを調べる。A100 40GB上でLlama-2-7Bを使い、入力長、出力長、バッチサイズ、GPU電力上限を変える。

- **2026-02 · [Parallel-Probe: Towards Efficient Parallel Thinking via 2D Probing](2026-2602.03845-parallel-probe-towards-efficient-parallel-thinking-via-2d-probing.md)**  
  実装：[✓](https://github.com/zhengkid/Parallel-Probe) ・ リポジトリ内被引用：4  
  多数派の答えが途中で既に確定していても、最後まで生成する方式では長い少数経路の完了待ちと総生成トークンが残る。論文の表1では、Qwen3-0.6Bの数学3ベンチマーク平均で、固定64経路の多数決に比べ正答率22.8%から23.3%へ変化しつつ、逐次トークン31.6千個から20.3千個、総トークン945.7千個から735.3千個へ減少した。

- **2026-05 · [EarlyTom: Early Token Compression Completes Fast Video Understanding](2026-2605.30010-earlytom-early-token-compression-completes-fast-video-understanding.md)**  
  実装：[✓](https://github.com/viridisGreen/EarlyTom) ・ リポジトリ内被引用：3  
  既存の圧縮方式の多くは、視覚符号化器が全トークンを処理し終えた後に間引く。単一NVIDIA A100上のLLaVA-OneVision-7Bでは、言語モデルへ入る視覚トークンを元の10%に保つ条件で、最初のトークンまでの時間（Time to First Token; TTFT）が889.9ミリ秒から336.2ミリ秒へ短縮し、約2.65倍の逆数比となる。

- **2026-03 · [Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention](2026-2603.21957-unified-spatiotemporal-token-compression-for-video-llms-at-ultra-low-ret.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  既存の手法はフレーム内の空間圧縮とフレーム間の時間圧縮を順番に適用するものが多いが、保持率を5%以下まで下げると、先に決めた各段階の予算配分が適切でなくなり、質問に必要な短い出来事や小さな物体を落としやすい。

- **2026-03 · [QMoP: Query Guided Mixture-of-Projector for Efficient Visual Token Compression](2026-2603.21232-qmop-query-guided-mixture-of-projector-for-efficient-visual-token-compre.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  QMoP（Query Guided Mixture-of-Projector）は、マルチモーダル大規模言語モデル（Multimodal Large Language モデル、MLLM）の画像トークン数を減らす際に、一つの固定圧縮法では画像と質問の組合せによって必要な情報を失うという問題を扱う。

- **2026-09 · [Predict, Don't Iterate: Efficient Adaptive-Length Infilling for Diffusion Language Models](2026-2609.02108-predict-don-t-iterate-efficient-adaptive-length-infilling-for-diffusion-.md)**  
  実装：[✓](https://github.com/Hsu1023/PILL) ・ リポジトリ内被引用：2  
  PILLは、拡散言語モデル（diffusion language モデル）が文章やプログラムの既知の前半と後半の間を補完する課題（infilling）において、欠落部分の長さをあらかじめ固定しなければならない制約を扱う。既存の可変長方式は長さを反復探索したり生成途中に伸縮操作を挿入したりするため、推論回数が増える。

- **2026-06 · [Beyond tokens: a unified framework for latent communication in LLM-based multi-agent systems](2026-2606.05711-beyond-tokens-a-unified-framework-for-latent-communication-in-llm-based-.md)**  
  実装：[✓](https://github.com/enochliu98/Awesome-Latent-Communication) ・ リポジトリ内被引用：2  
  2026年7月15日を調査打切りとして、2024～2026年の代表的な18研究を選び、送る情報の種類（WHAT）、送受信間の表現・層の整合（WHICH）、受信モデルへの統合方法（HOW）という3軸で比較する。

- **2026-05 · [When NPUs Are Not Always Faster: A Stage-Level Analysis of Mobile LLM Inference](2026-2605.27435-when-npus-are-not-always-faster-a-stage-level-analysis-of-mobile-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  携帯端末でニューラル処理装置が常に速いわけではないことを段階別に実測し、入力処理では中央処理装置が最大1.6倍速く、逐次生成の実効加速も1.05から1.20倍にとどまり、全面任せでは電力が最大51パーセント増えることを示した。

- **2026-04 · [Early Stopping for Large Reasoning Models via Confidence Dynamics](2026-2604.04930-early-stopping-for-large-reasoning-models-via-confidence-dynamics.md)**  
  実装：[✓](https://github.com/sudoparsa/CoDE-Stop) ・ リポジトリ内被引用：2  
  中間回答の確信度の時系列から、届いた推論は閾値で、不発な推論は不安定さの蓄積で止める学習不要の早期終了で、トークン量を25から50パーセント削りながら釣り合いを最も良くした。

- **2026-03 · [DyLLM: Efficient Diffusion LLM Inference via Saliency-based Token Selection and Partial Attention](2026-2603.08026-dyllm-efficient-diffusion-llm-inference-via-saliency-based-token-selecti.md)**  
  実装：[✓](https://github.com/scale-snu/DyLLM) ・ リポジトリ内被引用：2  
  マスク拡散型の言語モデルは、応答系列をマスクから始め、複数トークンを並列に埋めながら反復的に復号する。salient位置ではFFNを再計算し、注意も正確に更新する。DyLLMは速度だけでなく品質を維持する運用点を探す方式である。

- **2026-03 · [Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing](2026-2603.12254-attend-before-attention-efficient-and-scalable-video-understanding-via-a.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  視覚トランスフォーマーの手前で再構成可能な最小の複数尺度パッチを自己回帰的に選ぶ軽量な注視モジュールにより、視覚トークンを最大100分の1へ減らし、長尺・4K動画への拡張と精度向上を両立する。

- **2026-10 · [Measuring the Energy Cost of Completing Tasks with Quantized Language-Model Agents](2026-2610.32417-measuring-the-energy-cost-of-completing-tasks-with-quantized-language-mo.md)**  
  実装：[✓](https://github.com/stephen122204/mantra-energy/tree/paper-1) ・ リポジトリ内被引用：1  
  量子化エージェントのエネルギーをトークン単位ではなく完了タスク単位で測り直し、4ビットがトークン当たりでは安くても課題によっては完了当たり最大3.5倍高くなることと、その主因が余分なトークンであることを実機測定で示した。

- **2026-09 · [Dissecting GPU Utilization for LLM Inference on Nvidia Hopper](2026-2609.12923-dissecting-gpu-utilization-llm-inference-hopper.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  H100上のLLM推論を8種類のNsight指標で分解し、デコードでは帯域待ちに加えGMMA m64固定断片の1.56～12.5%充填やwave損失が単一SM利用率に隠れることを示す。

- **2026-09 · [AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines](2026-2609.18123-autotunebench-trustworthy-serving-engine-measurement.md)**  
  実装：[✓](https://github.com/li-ch/autotunebench) ・ リポジトリ内被引用：1  
  自動チューニングの測定規約を凍結コード・DB投入検証・不正隔離・事前登録比較・外部アンカーで強制し、エージェントが評価欠陥を最適化するのを防ぐ。

- **2026-09 · [A Calibrated Instrument for Measuring How Inference Optimizations Affect Output Quality](2026-2609.18005-a-calibrated-instrument-for-measuring-how-inference-optimizations-affect.md)**  
  実装：[✓](https://github.com/jerrykaplan/Calibrated-Instrument) ・ リポジトリ内被引用：1  
  判定器の偏りと雑音を帰無条件で較正し、同等性境界プラスマイナス0.3点の単一の物差しで量子化と早期終了と投機的復号の品質費用を分野別に比べ、費用が分野とモデルで大きく変わることを示した。

- **2026-08 · [The Halt Vector: Internalizing a Causal Steering Intervention for Efficient Reasoning](2026-2608.28859-the-halt-vector-internalizing-a-causal-steering-intervention-for-efficie.md)**  
  実装：[✓](https://github.com/dylanjayabahu/halt-vector) ・ リポジトリ内被引用：1  
  答え確定前後の活性差から作った停止ベクトルへのステアリングを、軸外次元を固定した全ベクトル再構成で重みへ内在化し、24問の適合だけで未見ベンチマークの思考を約24パーセント、問題適応的に削減した研究。

- **2026-08 · [Sliding-window beats linear attention](2026-2608.28444-sliding-window-beats-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  線形注意は固定サイズの再帰状態に集約することで、この増加を抑える。窓64・先頭シンク4の方式は、一般知識6課題平均で元モデルの99.0%を回復し、11の比較例のうち9例で元モデルを除く最高の平均値を得た。

- **2026-08 · [SABER: Stability-Aware Early Exit for LLM Reasoning via Adversarial Branch Probing](2026-2608.27963-saber-stability-aware-early-exit-for-llm-reasoning-via-adversarial-branc.md)**  
  実装：[✓](https://github.com/Bl1nding/SABER) ・ リポジトリ内被引用：1  
  推論の途中で「前の推論は間違い」と揺さぶる短い分岐を伸ばし、答えが揺らがなければ収束したとみなして早期終了する方式で、推論トークンを3から4割削りながら正解率を保った。

- **2026-08 · [LLMRouter: Unified Infrastructure for Developing, Evaluating, and Deploying LLM Routers](2026-2608.06867-llmrouter-unified-infrastructure-for-developing-evaluating-and-deploying.md)**  
  実装：[✓](https://github.com/ulab-uiuc/LLMRouter) ・ リポジトリ内被引用：1  
  LLMルーティングを5部品の逐次意思決定として統一し、18モデルを全クエリへ流して教師を作る評価基盤xRouteBenchと16種以上のルータ実装で、固定モデルより相対14.6パーセント良いルーティングと予算による順位逆転を示す基盤論文。

- **2026-08 · [Dependency-Aware Revocable Decoding for Efficient Diffusion Large Language Model Inference](2026-2608.26574-dependency-aware-revocable-decoding-for-efficient-diffusion-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  復号済みトークンを候補と確定へ分け、候補を信頼度の高い文脈だけで検証して検証文脈の汚染を断つ取消可能復号で、Saber比2.71倍の高速化と品質改善を両立した。

- **2026-07 · [HiFA4: Training-Free 4-bit FlashAttention on Ascend HIF4 NPUs for LLM Inference](2026-2607.04302-hifa4-training-free-4-bit-flashattention-on-ascend-hif4-npus-for-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意の行列積を4ビット化する際に、較正固定の等価な拡大・縮小でキーの外れ値をクエリ側へ移し、正規化子を実際に使う量子化済み重みから求めることで、判断のずれを大幅に減らした学習不要の方式である。

- **2026-06 · [Spectral Evolution-Guided Token Pruning in Multimodal Large Language Models](2026-2606.24165-spectral-evolution-guided-token-pruning-in-multimodal-large-language-mod.md)**  
  実装：[✓](https://github.com/zjubinchen/CLSE) ・ リポジトリ内被引用：1  
  層をまたぐ周波数成分の変化量を重要度にして視覚トークンを第2層の前に落とす学習不要の枝刈りで、88.9パーセント削減でも全トークン性能の94.8パーセントを保持した。

- **2026-06 · [NLL-Guided Full-Attention Layer Selection for Training-Free Sliding-Window Adaptation](2026-2606.27791-nll-guided-full-attention-layer-selection-for-training-free-sliding-wind.md)**  
  実装：[✓](https://gitlab.com/fars-a/nll-guided-swaa-layer-selection) ・ リポジトリ内被引用：1  
  長文脈LLMの事前充填（プリフィル）では、通常の全注意（full 注意機構; FA）の計算量が入力長に対して二乗で増える。36層のQwen3-4B-Thinking-2507とLongMemEval24kの評価では、9層（1/4）を全注意としたNLL-guidedが64.6%の正解率を得た。

- **2026-06 · [Does Mixture-of-Experts Actually Help Inference on Consumer and Edge Hardware? An Empirical Study](2026-2606.21428-does-mixture-of-experts-actually-help-inference-on-consumer-and-edge-har.md)**  
  実装：[✓](https://github.com/Analytics-Everywhere-Lab/edge-moe) ・ リポジトリ内被引用：1  
  専門家モデルの疎な活性化が辺縁実機で効くかを同一条件で実測し、Jetsonでは同じ有効規模の密モデルより約31パーセント遅く電力2.1倍・メモリ天井到達となり、費用は有効ではなく総パラメータに追随すること、経路選択は計算の9パーセント未満で主因でないことを示した。

- **2026-06 · [Benchmarking LLM Serving Systems for Agentic AI Workloads with XPerf](2026-2608.20370-xperf-benchmarking-llm-serving-agentic-ai-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェント実行を呼出し依存グラフとして記録・再生し、8種類の実アプリでサービング負荷とハードウェア指標を再現可能に測る評価基盤を提示する。

- **2026-05 · [Silicon Showdown: Performance, Efficiency, and Ecosystem Barriers in Consumer-Grade LLM Inference](2026-2605.00519-silicon-showdown-performance-efficiency-and-ecosystem-barriers-in-consum.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  消費者向けNvidia GPUとApple Siliconを70B級モデルとNVFP4まで含めて実測比較した分析。Nvidiaは収まる範囲で計算密度が最高だがVRAMの壁とバックエンド摩擦があり、Appleは統合メモリで大規模モデルを実用精度のまま載せ効率でも勝るという二分構造を示した。

- **2026-05 · [PARCEL: Pool-Anchored Resampling with Conditioned Elastic Queries for Efficient Vision-Language Understanding](2026-2605.30126-parcel-pool-anchored-resampling-with-conditioned-elastic-queries-for-eff.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PARCELは、視覚トークンの数を16、64、256など異なる予算へ縮めても、空間的な位置関係と画像の細部を両立して保つための、可変予算の視覚表現設計である。27種類の評価課題を横断した全体平均の性能保持率は、視覚トークン256個で95.6%、64個で95.3%、16個で88.3%と報告された。

- **2026-05 · [Evading Visual Aphasia: Contrastive Adaptive Semantic Token Pruning for Vision-Language Models](2026-2605.09429-evading-visual-aphasia-contrastive-adaptive-semantic-token-pruning-for-v.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  たとえば、画像内で目立つ動物より周辺の店名看板を尋ねているのに、初期層の注意が動物へ集中した結果、看板のトークンが枝刈りされ、モデルが架空の店名を答える。LLaVA-v1.5-7Bで画像トークンを576個から128個へ77.8%削減した条件では、七つの評価セットを正規化した平均性能を98.64%保持し、遅延を167.50ミリ秒から77.94ミリ秒へ短縮した。

- **2026-05 · [AsymVLM: Asymmetric Token Pruning for Efficient Vision-Language Model Inference](2026-2605.29535-asymvlm-asymmetric-token-pruning-for-efficient-vision-language-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚トークンはプリフィル前に学習済みスコアラーで強く枝刈りし、テキストトークンは予算超過時だけエビクションするという非対称な圧縮で、最大54%のFLOPs削減と文書・図表理解での精度向上を両立する視覚言語モデルの推論方式。

- **2026-05 · [Agentic Kernel Optimization: Generating State-of-the-Art GPU Kernels Without Hand-Written CUDA](2026-2608.14560-agentic-kernel-optimization-generating-state-of-the-art-gpu-kernels-with.md)**  
  実装：[✓](https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda) ・ リポジトリ内被引用：1  
  正しさを門番とする評価とハッキング禁止の下で複数コードエージェントが計画・実装・プロファイル・統合を分担し、人手のCUDAなしでMoEと疎注意のカーネルを参照実装比最大1101倍まで高速化した事例研究。

- **2026-04 · [The Detection-Extraction Gap: Models Know the Answer Before They Can Say It](2026-2604.06613-the-detection-extraction-gap-models-know-the-answer-before-they-can-say-.md)**  
  実装：[✓](https://github.com/EdWangLoDaSc/know2say) ・ リポジトリ内被引用：1  
  答えが回収可能になる時点と強制抽出できる時点のずれを分布のずれとして定式化し、自由継続だけで検出と抽出を行う早期終了BAEEで直列生成を約7割減らしながら正解率も上げる、推論時計算の分析と手法。

- **2026-04 · [Reasoning Language Model Inference Serving Unveiled: An Empirical Study](2025-2510.18672-reasoning-language-model-inference-serving-unveiled.md)**  
  実装：[✓](https://github.com/lqinfdim/RLMServing) ・ リポジトリ内被引用：1  
  推論大規模言語モデルは通常の言語モデルと異なり、キャッシュ使用量が大きく変動し、少数の遅い要求が処理全体を引き延ばす。著者らは評価枠組みASUとベンチマークASU-Perfを導入し、複数のサービング最適化がモデル規模や負荷によって効いたり逆効果になったりすることを、実機評価と到着負荷の再現で示す。

- **2026-04 · [NeuReasoner: Towards Explainable, Controllable, and Unified Reasoning via Mixture-of-Neurons](2026-2604.02972-neureasoner-towards-explainable-controllable-and-unified-reasoning-via-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  失敗を、単一推論段階内の計算・論理誤り、複数段階間で同じ考えを繰り返す停滞、問題の難易度に対して考え過ぎる過剰思考の三つに分類する。原著付録のA100実測では、監視と介入を加えた方式の実行時間が元モデルより増えている。

- **2026-04 · [MoEITS: A Green AI approach for simplifying MoE-LLMs](2026-2604.10603-moeits-a-green-ai-approach-for-simplifying-moe-llms.md)**  
  実装：[✓](https://github.com/luisbalru/MoEITS) ・ リポジトリ内被引用：1  
  一方、推論時に毎回使わないエキスパートも重みとして保持する必要があり、GPUやホスト側のメモリ容量、モデル配備コスト、エネルギー消費が大きくなる。方式は単純な利用頻度ベースの削除ではない。

- **2026-04 · [KiToke: Distribution-Aware Token Compression for Video Large Language Models](2026-2604.03414-kitoke-distribution-aware-token-compression-for-video-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  特に保持率1%など極端な条件では、複雑な既存手法が一様ランダム抽出より低い精度になることもある。

- **2026-04 · [EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling](2026-2604.17087-evocomp-learning-visual-token-compression-for-multimodal-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル時の注意演算、鍵・値（KV）キャッシュ、入力列の読み込みが増え、初回応答の待ち時間が長くなる。EvoCompは、視覚トークンのうち質問への回答に必要なものだけを選び、下流LLMへ渡す系列長を減らす方式である。LLaVA-1.5-7Bでは576トークンを192に削減したとき、6ベンチマークの平均成績を元モデルの99.3%に保つ。

- **2026-03 · [Wattchmen: Watching the Wattchers -- High Fidelity, Flexible GPU Energy Modeling](2026-2603.26435-wattchmen-watching-the-wattchers-high-fidelity-flexible-gpu-energy-model.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一方、従来の細粒度モデルは一部の命令だけを対象にするか、別のGPU・冷却条件への移植性が不足していた。これはLLM専用推論の速度を改善する方式ではなく、GPUを使う学習・推論・科学計算のエネルギーを分析し最適化箇所を見つける基盤である。

- **2026-03 · [Token Reduction via Local and Global Contexts Optimization for Efficient Video Large Language Models](2026-2603.01400-token-reduction-via-local-and-global-contexts-optimization-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AOT（local-global Anchor Optimal Transport）は、動画対応の大規模言語モデル（Video LLM）の入力に含まれる視覚トークンを、追加学習なしで削減する方式である。LLaVA-OneVision-7Bの無圧縮平均58.4に対し、視覚トークン10%保持のAOTは平均57.0で、元性能の97.6%を維持した。

- **2026-03 · [Diagnosing FP4 Inference: A Layer-Wise and Block-Wise Sensitivity Analysis of NVFP4 and MXFP4](2026-2603.08747-diagnosing-fp4-inference-a-layer-wise-and-block-wise-sensitivity-analysi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FP4の感度を射影の種類とブロックの深さで切り分けた診断研究で、MLPの上向き・下向き射影が全規模・両形式で最も敏感であり、感度は最終ブロックだけに集中しないことを示した。

- **2025-12 · [Vision Token Reduction via Attention-Driven Self-Compression for Efficient Multimodal Large Language Models](2025-2602.12618-vision-token-reduction-via-attention-driven-self-compression-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  決まった層で視覚トークンを一様に間引く詰め込み口を作り、注意の働きで情報を残るトークンへ移す自己圧縮を学習させる方式で、LLaVA-1.5-7Bの計算量を53.7%、キー値キャッシュを56.7%減らしながら性能の98.2%を保持した。

- **2025-12 · [ELANA: A Simple Energy and Latency Analyzer for LLMs](2025-2512.09946-elana-a-simple-energy-and-latency-analyzer-for-llms.md)**  
  実装：[✓](https://github.com/enyac-group/Elana) ・ リポジトリ内被引用：1  
  本論文は新しい推論アルゴリズムの高速化倍率を主張するものではなく、計測方法と計測例を提示する研究である。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [Understanding the Energy Cost of Quantized Agents on Shared GPUs](2026-2610.41672-understanding-the-energy-cost-of-quantized-agents-on-shared-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  失敗分も含めた検証済み完了当たりのエネルギーで量子化を測り直し、固定した呼び出しでは10〜25%安い4ビット形式が実実行では余分な作業と未完了で49%高くなる一方、キャッシュ競合のある40GB配置では空きメモリの効果で安くなり、最安の精度は同時実行数と配置で変わることを実機で示した。

- **2026-11 · [SHADOWPREFILL: Keeping Your Next Model Warm for Per-Step Model Routing in Agentic LLM Serving](2026-2611.13176-shadowprefill-keeping-your-next-model-warm-for-per-step-model-routing-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル切り替えで失われるプリフィックス再利用を、選ばれていないモデルの余裕容量で文脈を影プリフィルして先回りすることで回復する方式。切り替え遅延を最大21.4パーセント、トークン費用を最大46.1パーセント削減する。

- **2026-11 · [SafeStart: Mitigating the Overlooked Safety Cost of Active Expert Reduction in MoE LLM Serving](2026-2611.06147-safestart-mitigating-the-overlooked-safety-cost-of-active-expert-reducti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパート削減によるMoE高速化が精度をほぼ保ったまま拒否だけを弱めることを実測で示し、原因が応答の冒頭にあることを特定して、冒頭だけ全エキスパートで計算するSafeStartで高速化の大半と拒否の両方を保つ対策を与えた研究。

- **2026-11 · [R^2-Omni: Reducing Structural and Precision Redundancy in Omni-LLMs for Long-Form Generation](2026-2611.03247-r-2-omni-reducing-structural-and-precision-redundancy-in-omni-llms-for-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問への注意ではなく時空間類似と局所連続性でマルチモーダルトークンを統合し、残したKVキャッシュの値の精度を注意出力誤差と音声映像の整合で配分することで、長文生成の品質を保ちながらメモリを約5倍削減する手法。

- **2026-11 · [MultiTurnRoute: A Platform for Building and Evaluating Multi-Turn LLM Routers](2026-2611.10848-multiturnroute-a-platform-for-building-and-evaluating-multi-turn-llm-rou.md)**  
  実装：[✓](https://github.com/loopleap-lab/MultiTurnRoute) ・ リポジトリ内被引用：0  
  複数ターン会話向けに、対話状態と各モデルのキャッシュ済みプレフィックスをルーターへ渡す基盤と評価Arenaを構築し、ゲート付き対話状態とキャッシュ割引で品質と費用を別々に見積もるルーターが最強モデルの品質に届く費用を最大20.3パーセント削減する。

- **2026-11 · [Matching Workloads to Blackwell: Power-Resolved Benchmarking of NVIDIA B200 and B300 across HPC and AI Workloads](2026-2610.41919-matching-workloads-to-blackwell-power-resolved-benchmarking-of-nvidia-b2.md)**  
  実装：[✓](https://github.com/MohsenZand/GPUBenchmarking) ・ リポジトリ内被引用：0  
  新旧のデータセンター向け図形処理装置を二つの独立クラスタで横断測定し、新装置が畳み込みで最大五・六倍、七百億の言語モデル推論で二十四から二十七パーセント遅い一方で大きな行列積の負荷では速いこと、遅さは基板電力の低さからカーネルごとの費用に帰着すること、同一半導体でも提供基盤の版で最初のトークンまでの時間が二・一倍変わることを示した。

- **2026-11 · [Direct GPU Energy Measurements of Batch-Level Sharing in Mixture-of-Experts and Recurrent Models](2026-2611.11696-direct-gpu-energy-measurements-of-batch-level-sharing-in-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算回数ではなくGPUエネルギーを直接測り、再帰方策ではバッチ共有が成立しないこと、専門家モデルではバッチ配慮型ルーティングが重み読みを25から31パーセント減らしトークンあたりエネルギーを12から18パーセント減らすことを示す実測研究。

- **2026-11 · [CoPyro: Feeding Copy Proposals to Parallel Drafters](2026-2611.27217-copyro-feeding-copy-proposals-to-parallel-drafters.md)**  
  実装：[✓](https://github.com/dt-3t/CoPyro) ・ リポジトリ内被引用：0  
  文脈中の過去の出現からコピーした続きをマスクの代わりに並列ドラフターへ入力し、信頼性特徴とともに残す部分と直す部分を学ばせることで、受理長を最大5.08パーセント伸ばす投機的デコードの改良。

- **2026-11 · [AutoEMatic: Runtime-Adaptive Mixed-Precision LLM Inference via Automatic Exponent-Mantissa Refinement](2026-2611.10165-autoematic-runtime-adaptive-mixed-precision-llm-inference-via-automatic-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  次トークンの不確かさと層の更新量を実行時に観測して層ごとの精度を2、4、6ビットから選び、単一のNVFP4表現から全精度を導く形式とカーネルで、精度と速度を両立させる実行時適応型の混合精度推論。

- **2026-10 · [VLA-HWBench: Where the Time Goes When VLA Models Run on Edge Hardware](2026-2610.34717-vla-hwbench-where-the-time-goes-when-vla-models-run-on-edge-hardware.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  開放モデル18種を2種の縁端計算機で7段階に分解して測り、遅延はモデル規模ではなく行動生成の反復回数で決まること、融合と4ビット化が最大の利得だが適用範囲が狭いこと、最適化後はソフトウェア律速が残ることを明らかにした。

- **2026-10 · [VisionWeave: Weaving Elastic Visual Representations as a Native Capability of MLLMs](2026-2610.07987-visionweave-weaving-elastic-visual-representations-as-a-native-capabilit.md)**  
  実装：[✓](https://github.com/FFY0/VisionWeave) ・ リポジトリ内被引用：0  
  視覚ブロックごとに細粒度4トークンと粗粒度1トークンを学習済みルーターで織り替える弾性表現を自己蒸留で基盤モデルに植え付け、Qwen3.8-27Bで平均43.0パーセントのトークン削減と本来性能の98.9パーセント維持、SGLangで2.30倍のスループットを両立する。

- **2026-10 · [Towards Green AI: Evaluating Energy Efficiency for Quantized LLM Inference](2026-2610.17531-towards-green-ai-evaluating-energy-efficiency-for-quantized-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みのみ量子化10構成のエネルギー・速度・精度・メモリを5モデル・4タスク・4種のGPUで統一実測し、融合カーネル型の8ビット量子化が最大約4倍省エネルギーであることと、長入力・短出力で利得が最大になり実行時間がエネルギーの代理指標になることを明らかにした評価論文。

- **2026-10 · [The Cost of Context: Profiling the Energy Footprint of Input Tokens in Large Language Models](2026-2610.19819-the-cost-of-context-profiling-the-energy-footprint-of-input-tokens-in-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルだけを1ミリ秒刻みの電力計測で切り分け、入力トークンのエネルギー原単位が文脈長とエンジン最適化でどう変わるかをA100実機で示した計測研究。

- **2026-10 · [Reproducible LLM Inference Benchmarking: A Sequential Isolation Protocol for Regression Testing](2026-2610.09778-reproducible-llm-inference-benchmarking-a-sequential-isolation-protocol-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ベンチマークの実行順序・再起動・ウォームアップ・間隔を統制する順次分離プロトコルで、推論測定のrun間変動係数を15.2パーセントから2.2パーセントへ下げ、回帰テストに使える再現性を得る方法と実測。

- **2026-10 · [ReFold: Training-Free Reversible Inter-Turn Context Folding for Long-Horizon Agents](2026-2610.07863-refold-training-free-reversible-inter-turn-context-folding-for-long-hori.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  土台の履歴を残したまま見せる文脈だけを畳み、表示済みの重複と読み終えたターンを可逆に除くことで、トークンを最大2.5倍減らしKVキャッシュを半減させるエージェントの文脈管理。

- **2026-10 · [Raincheck: Deferred Multimodal Prefill for Efficient Multi-Turn MLLM Inference](2026-2610.39562-raincheck-deferred-multimodal-prefill-for-efficient-multi-turn-mllm-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  間引きで外れたマルチモーダルトークンを捨てず、生成中の空き計算と応答後の隙間で元の順序に処理し直し、可視性制御と状態写像で生成中の文脈へ差し込むことで、失われた品質の平均七七・七パーセントを回復しつつ最初の応答を最大二四・一パーセント速くし、出力間隔の悪化を〇・五パーセント未満に抑えたと報告した。

- **2026-10 · [Prefetch-Steered Routing: Deterministic Cache-Aware Expert Selection for Offloaded Mixture-of-Experts Decoding](2026-2610.34721-prefetch-steered-routing-deterministic-cache-aware-expert-selection-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEのエキスパート選択を、転送タイミングで変わる物理キャッシュではなく決定的な論理キャッシュに基づいて行い、プリフェッチで選ばれるエキスパート自体をルーティングへ織り込むことで、評価と配備の一致を保ったままオフロードデコードを速める方式。

- **2026-10 · [PACE: Pareto-Adaptive Compression for Efficient Native MLLMs](2026-2610.24005-pace-pareto-adaptive-compression-for-efficient-native-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ネイティブ型マルチモーダルモデルの視覚トークンを、高さと幅へ分けた重要度とパレート最適な段階別保持率で圧縮し、保持率25パーセントでもほぼ無損失のまま計算量を2.0倍分減らした研究。

- **2026-10 · [Operon-S1: a fast decision controller for long-horizon biomedical agents](2026-2610.41350-operon-s1-a-fast-decision-controller-for-long-horizon-biomedical-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントの反復判断を13の決定点の閉じた質問として切り出し、答えを含まない固定メッセージだけで介入する高速決定層により、判断を測定・交換・学習できる層として分離した。

- **2026-10 · [On the Fundamental Limits of Prefill-Based Decoding Length Prediction](2026-2610.40541-on-the-fundamental-limits-of-prefill-based-decoding-length-prediction.md)**  
  実装：[✓](https://github.com/ShwStone/DecodingPredict) ・ リポジトリ内被引用：0  
  デコード長を停止時刻と更新過程でモデル化し、プリフィル予測の誤差下限が生成の標準偏差だけで決まることを理論と実測で示した研究。下限は平均絶対誤差で標準偏差の0.798倍であり、単純な予測器でもほぼ到達できる。

- **2026-10 · [Offline AI Modules: Voice-First Offline Architecture, Hardware Reference Stack, Quantization and Benchmarking](2026-2610.07026-offline-ai-modules-voice-first-offline-architecture-hardware-reference-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話を完全オフラインで動かすモジュール式スタックと安価な部品表を提示し、2層の実機で量子化形式を比べ、4ビット形式が大きさと品質の釣り合いで最適であることを実測で示した研究。

- **2026-10 · [Measuring the Inference Energy Efficiency of Open-Weight LLMs across Benchmarks, Reasoning Modes, and Hardware](2026-2610.14389-measuring-the-inference-energy-efficiency-of-open-weight-llms-across-ben.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  86チェックポイントを7ベンチマークと6基盤で飽和サービングしながらGPUエネルギーを直接測り、能力とエネルギーのパレートフロンティア、推論モードと出力予算の費用、トークン数という代理指標の限界、FP8とハードウェア変更の効果を明らかにした大規模実測研究。

- **2026-10 · [MAServeBench: Benchmarking Multi-Agent LLM Serving Systems with Hierarchical Collaboration Workloads](2026-2610.40293-maservebench-benchmarking-multi-agent-llm-serving-systems-with-hierarchi.md)**  
  実装：[✓](https://github.com/ShengxuanQiu/MAServeBench) ・ リポジトリ内被引用：0  
  複数エージェントの協調を負荷の生成規則として組み立て、実現した作業を固定して解放と資源だけを変える比較を可能にしたベンチマークで、解放の順序付けが根の遅延を最大五十四パーセント増やし、期限達成は百パーセント対四パーセントに分かれることを示した。

- **2026-10 · [Lightweight Scheduling Policies for Continuously Batched LLM Serving Across GPU Architectures](2026-2610.15899-lightweight-scheduling-policies-for-continuously-batched-llm-serving-acr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連続バッチングのデコードスケジューラ8方針を6モデルと3種のGPUで実機比較し、優劣がハードウェアで入れ替わることを示した評価研究。

- **2026-10 · [Just Respect the Semantics: Image-Token Compression via Pre-LLM Semantic Variable-Resolution Tokenization and In-LLM Relevance Pruning](2026-2610.18690-just-respect-the-semantics-image-token-compression-via-pre-llm-semantic-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  物体境界と文字らしさで解像度を配る前段の可変解像度トークン化と、中盤の学習型関連性枝刈りを組み合わせ、画像トークンを5.56パーセントまで減らしても性能を86から92パーセント保持する視覚トークン圧縮方式。

- **2026-10 · [JOVE: Joint Execution and Verification for Resource-Aware LLM Task Graphs](2026-2610.03296-jove-joint-execution-and-verification-for-resource-aware-llm-task-graphs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  タスクグラフの各ノードへの実行モデルの割当てと、有料検証を行うノードの選択を、予算と遅延の制約の下でクエリごとの混合整数計画として同時に決め、検証結果で品質推定をオンラインに学ぶ枠組み。

- **2026-10 · [ixi-sLM: On-Device sLM for AI Call Agent Service](2026-2610.19382-ixi-slm-on-device-slm-for-ai-call-agent-service.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通話ドメインへの語彙削減とトークナイザー再適合、実通話校正の混合精度量子化で、1.2ビーモデルを803メガバイトに収めてモバイルエヌピーユーで動かし、クラウド級品質の94パーセントを保った実サービス報告。

- **2026-10 · [How Far Are We From On-Device VLM Inference? A Measurement Study on Edge NPUs](2026-2610.40039-how-far-are-we-from-on-device-vlm-inference-a-measurement-study-on-edge-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末の神経処理装置で六つの視覚言語モデルをカーネル単位で測り、注意はソフトマックスが支配して行列装置が空転すること、線形注意の利得は配置変換で消えること、逐次生成の勝敗は注意の行列並列度で決まることを示し、課題ごとの甘い解像度を提案した測定研究である。

- **2026-10 · [Fewer Bits, More Tries: Recovering Capability Under Memory Constraints](2026-2610.15372-fewer-bits-more-tries-recovering-capability-under-memory-constraints.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小さい・低ビットのモデルを並列に複数回試行しテストで検証して選ぶことで、失われた一発正解率の多くを回復できることを示し、7Bの8回試行が32Bの1回にメモリ約4分の1で匹敵・上回ることを実測する分析研究。

- **2026-10 · [DoubtLess: Training-Free Contrastive Decoding for Efficient Reasoning](2026-2610.18862-doubtless-training-free-contrastive-decoding-for-efficient-reasoning.md)**  
  実装：[✓](https://github.com/leoluolol/DoubtLess) ・ リポジトリ内被引用：0  
  小さい推論モデルに簡潔な読みと冗長な読みの二通りで途中経過を読ませ、そのロジット差で大きいモデルを毎ステップ誘導し、学習なしで思考連鎖を31%短縮しながら正解率を保つ対照デコード。

- **2026-10 · [CALM: Consistency-Aware Logit Masking in Decoding Space for Mitigating Overthinking of Large Reasoning Models](2026-2610.25908-calm-consistency-aware-logit-masking-in-decoding-space-for-mitigating-ov.md)**  
  実装：[✓](https://github.com/szu-tera/CALM.git) ・ リポジトリ内被引用：0  
  試行回答の連続一致を検出した後も生成を打ち切らず、行動遷移点トークンのロジットを抑えることで冗長な再検討を減らし、トークンを約2割削減しながら精度を保つ学習不要のデコード手法。

- **2026-10 · [A Case Study of a Multi-Agent Kernel-Optimization Loop That Learns a New AI Accelerator](2026-2610.38329-a-case-study-of-a-multi-agent-kernel-optimization-loop-that-learns-a-new.md)**  
  実装：[✓](https://github.com/bgchun-fs/multi-agent-kernel-gen-loop) ・ リポジトリ内被引用：0  
  未知のNPUとそのRust製ドメイン特化言語について、文書要約と実測とコンパイラ規則から知識基盤を自作して再検証し、設計木と役割分担の探索でGemma-4-12Bのカーネル3本を公式比で幾何平均9.293倍へ高速化したエージェントループの事例研究。

- **2026-09 · [Who Speaks for the Pruned? Visual Token Pruning as Coverage Optimization](2026-2609.03158-who-speaks-for-the-pruned-visual-token-pruning-as-coverage-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークン枝刈りを、残すトークンの順位付けではなく、捨てるトークンを誰が代表するかという被覆最適化として定式化し、強い圧縮ほど既存方式を引き離した学習不要の枝刈り研究。

- **2026-09 · [Where Should a Document Live: Context, Representations, or Parameters?](2026-2609.17346-where-should-a-document-live-context-representations-or-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文書知識の置き場として文脈、KV表現、パラメータを保存量を揃えて統制比較し、KV型のCartridgesが単一文書と複数文書の両方で最も正確だが忘却も伴うこと、Compactionとパラメータ型は複数文書の合成で崩れることを明らかにした比較研究。

- **2026-09 · [Visual Jev: Accurate and Efficient Decisions from Shared Visual Context](2026-2609.25845-visual-jev-accurate-and-efficient-decisions-from-shared-visual-context.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ画像への複数の選択式質問で、視覚プリフィックスを一度だけ計算して共有し質問接尾辞を隔離バッチ実行することで、再計算を消して8.9倍の処理効率を得る視覚判断システム。

- **2026-09 · [The Inference Engineering Pareto Atlas: Which Optimizations Dominate the Cost, Quality, and Latency Frontier?](2026-2609.17863-inference-engineering-pareto-atlas.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  54実測点と校正シミュレータで推論最適化の組合せを品質・遅延・費用の同一Pareto面へ置き、制約別の支配構成を示す。

- **2026-09 · [STAR-Pro: Stage-Wise Token Adaptive Reduction with Progressive Refinement for Efficient Large Vision-Language Models](2026-2609.05916-star-pro-stage-wise-token-adaptive-reduction-with-progressive-refinement.md)**  
  実装：[✓](https://github.com/EasonAI-5589/starpro) ・ リポジトリ内被引用：0  
  融合前はピボット付きQRで特徴被覆を保つ候補プールを作り、デコーダ内では深さで変わる注意に合わせて段階的に絞る2段階の視覚トークン削減で、90.5パーセント削減でも性能の92.7パーセント保持と2.24倍高速化を両立した。

- **2026-09 · [Stable Answers, Unfinished Reasoning: Why Self-Consensus Is Not a Safe Early-Exit Signal](2026-2609.09989-stable-answers-unfinished-reasoning-why-self-consensus-is-not-a-safe-ear.md)**  
  実装：[✓](https://github.com/Antony-zdh/stable-answers-unfinished-reasoning) ・ リポジトリ内被引用：0  
  単一軌跡への繰り返しプローブの一致を早期終了信号にする自己合意について、一致は推論の終了ではなく回答の持続しか示さない合意・終了ギャップを測定し、事前登録した3,520ルールの走査で安全かつ節約になる合意ルールが存在しない一方、境界確信度の対照は全ゲートを通過することを示した分析研究。

- **2026-09 · [SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops](2026-2609.19169-siliconbench-speed-memory-and-fidelity-for-llm-serving-on-unified-memory-desktops.md)**  
  実装：[✓](https://github.com/WindChimeRan/SiliconBench) ・ リポジトリ内被引用：0  
  Apple Siliconの九推論基盤を速度・共有メモリ・忠実度・新モデル対応・複数機で横断監査し、vllm-metalの並行処理と遠隔直接メモリアクセスを使うテンソル並列の優位を示す。

- **2026-09 · [Separating Stream Stability from Long-Term Recall in Language Models](2026-2609.07282-stream-stability-long-term-recall-threeh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間生成の安定性・過去情報への因果アクセス・タスク効用をThreeHの3到達距離へ分離し、注意シンクの安定生成を長期記憶と誤認しない評価契約を示す。

- **2026-09 · [PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving](2026-2609.19657-prefixbench-h100-prefix-reuse-ttft.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21725505) ・ リポジトリ内被引用：0  
  単一H100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞キャッシュそのものの効果、容量超過、要求スケジューリングの差を切り分ける実測ベンチマーク。

- **2026-09 · [PC-SubMax: Efficient Prompt Compression via Regularized Submodular Maximization](2026-2609.32474-pc-submax-efficient-prompt-compression-via-regularized-submodular-maximi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文選択を被覆・関連性・多様性の劣モジュラ効用とトークン費用の差として定式化し、近似保証付きの貪欲法で解くことで、自己回帰モデルによる採点なしに速く冗長さの少ないプロンプト圧縮を行う。

- **2026-09 · [P4Q: Co-designing Token Pruning and Quantization for Vision-Language Model Acceleration](2026-2609.34867-p4q-co-designing-token-pruning-and-quantization-for-vision-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疑似量子化した射影特徴で視覚トークンを選び、同じ選択で量子化調整を行う共同設計により、4ビット化と88.9パーセント枝刈りを併用しても性能を保ちながら推論を2.8倍速くする方式。

- **2026-09 · [Measured Joules, Learned Routes: Learning to Route for Energy-Efficient LLM Serving](2026-2609.23085-measured-joules-learned-routes-learning-to-route-for-energy-efficient-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  9モデルの全候補に全クエリを解かせた実測エネルギー記録からゲート付き順位報酬を作り、小型言語モデルルーターを教師あり微調整とGRPOで学習して、精度をほぼ保ちながら回答エネルギーを約23パーセント下げるルーティング手法。

- **2026-09 · [MassAlloc Attention: Let Attention Allocate Its Own Compute](2026-2609.32712-massalloc-attention-let-attention-allocate-its-own-compute.md)**  
  実装：[✓](https://github.com/HKUSTDial/flash-sparse-attention) ・ リポジトリ内被引用：0  
  MassAlloc 注意機構（MALA）は、長文脈で計算負荷が大きくなる自己注意のうち、クエリとキーの内積スコアを求めた後の処理を削減する方式である。原著は8基のH100を用いた128K系列の注意演算子ベンチマークで、全注意（Full 注意機構; FullAttn）に対し順伝播の遅延を2.2倍、逆伝播を3.0倍、復号を1.6倍改善したと報告する。

- **2026-09 · [MaskCoFT: Masked Co-Adaptive Fine-Tuning for Memory-Efficient MoE Inference](2026-2609.34077-maskcoft-masked-co-adaptive-fine-tuning-for-memory-efficient-moe-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUメモリが不足する場合は専門家をCPUへオフロードし、必要時にGPUへロードする。原著はMoE-OffloadingにおけるMixtral-8×7Bのデコード時間で、専門家ロードが86%、専門家計算が3%という分析を示す。

- **2026-09 · [LazyAgent: Demand-Driven Materialization and Physical Optimization of Agentic Programs](2026-2609.23058-lazyagent-demand-driven-materialization-and-physical-optimization-of-age.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントプログラムについて、実行可能なステップと要求が必要なステップを区別し、プログラム全体から計算した需要集合に入る仕事だけを実行する需要駆動の実体化と、LLMステップの出力を必要分だけに絞る射影などの物理最適化を定式化し、証明と実測で効果の範囲を示した研究。

- **2026-09 · [KREX: Concurrent Kernel Benchmarking on Shared GPUs via Region-Granular Exclusivity](2026-2609.30057-krex-concurrent-kernel-benchmarking-on-shared-gpus-via-region-granular-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時間のわずかな差が候補順位を変えるため、他の処理が同じGPUへ負荷をかけると測定が歪み、エージェントは遅い候補を良いものと誤認する。さらにGPUコンテキストを毎回作り直さず、長寿命のコンテキスト保持プロセスを再利用することで、GPU初期化時のノード全体の直列化を避ける。

- **2026-09 · [HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications](2026-2609.12412-holibench-a-cross-platform-benchmarking-and-deployment-toolkit-for-foundation-models-in-cps-iot-applications.md)**  
  実装：[✓](https://github.com/beesfleas/HoliBench) ・ リポジトリ内被引用：0  
  20モデル×7デバイス×3量子化×8推論系を精度・遅延・電力・メモリで統一測定し、実測プロファイルから制約付き配備構成まで選ぶ基盤。

- **2026-09 · [Green AI: Cost of LLM-Based Code Completion](2026-2609.33918-green-ai-cost-of-llm-based-code-completion.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21971227) ・ リポジトリ内被引用：0  
  コード補完のためにLLMをローカル実行する場合、モデルの正答率や生成速度だけでなく、入力文脈を処理するためのGPUエネルギーと、出力を逐次生成するためのGPUエネルギーを分けて評価する必要がある。量子化モデル、とくにQ4は同一モデル系のFP16に比べて省エネルギーな傾向があり、品質とエネルギーのPareto前線へ頻繁に現れる。

- **2026-09 · [GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems](2026-2609.14864-gguf-metadata-prediction-of-single-sequence-llama-cpp-throughput-across-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ローカル大規模言語モデルを選ぶとき、GGUF形式の複数の量子化モデルを実際に読み込み、同じ入力長で速度を比較する作業は重い。

- **2026-09 · [From Inference Engine to Inference Control Plane: Connecting vLLM, llm-d, and the Evolution of Efficient Distributed LLM Serving](2026-2609.23130-from-inference-engine-to-inference-control-plane-connecting-vllm-llm-d-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM推論最適化の単位が単一推論エンジンのバッチ処理・KV管理から、分散したGPU群のルーティング、KV転送、プリフィル/デコード分離、入場制御、拡縮と耐障害性を束ねる制御面へ移行していることを整理したシステム統合レビュー。

- **2026-09 · [FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents](2026-2609.37590-focus-training-free-decision-preserving-context-compression-for-llm-agen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント履歴を推論・行動・観測の単位に分け、下書きモデルの将来計画が各単位をどれだけ頻繁に依存先として挙げるかで将来有用性を測り、学習なしでテスト時に残す単位を選ぶ圧縮方式を提案し、文脈量を減らしながら成功率を上げた研究。

- **2026-09 · [FaultSense: Fault Localization in Large-Scale Mixture-of-Experts Model Serving Infrastructure](2026-a08c1f9c632d-faultsense-fault-localization-in-large-scale-mixture-of-experts-model-serving-infrastructure.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一MoE層の選択可能プローブと二段階グループ検査で、特権監視なしにグレー障害GPU・通信経路をアプリ層から局所化し、診断プローブを約20倍削減する。

- **2026-09 · [Efficient FlashAttention on Blackwell via Fixed-Shift Softmax and Persistent Scheduling](2026-2610.02229-efficient-flashattention-on-blackwell-via-fixed-shift-softmax-and-persis.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行最大値の逐次補正を固定シフトで消し、逆方向の正規化を逆数分母の保存で前処理へ移し、持続型スケジューリングと重ねることで、新世代GPU向け注意カーネルのスループットを24条件の幾何平均で7.3パーセント高めた実装研究。

- **2026-09 · [Constraints Are Graphs, Not Chains: Exact Decoding for Diffusion Language Models](2026-2609.32900-constraints-are-graphs-not-chains-exact-decoding-for-diffusion-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの制約付きデコードで、制約を逐次状態ではなく因子グラフとして保持し変数消去で厳密に解く方式を提案し、全制約充足を小さな追加遅延で達成した研究。

- **2026-09 · [Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs](2026-2609.07664-accuracy-is-not-enough-a-divergence-based-approach-to-evaluate-fidelity-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）を低ビット量子化して端末へ載せるとき、一般的には困惑度（perplexity）や選択式問題の正答率がどれだけ落ちるかを確認する。例えばLLaMA-3.1-8BのMMLUでは、Q4KとQ40の正答率はそれぞれ32.2%と32.1%でほぼ等しいのに、BF16に対するTVDは0.055と0.221で約4倍異なる。

- **2026-08 · [Total Recall at What Cost? Benchmarking the Serving Cost of Agentic Memory Systems](2026-2608.11879-total-recall-at-what-cost-benchmarking-the-serving-cost-of-agentic-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント向けメモリ3方式と参照2方式を同一バックボーン・同一料金で最大400ターンまで測り、メモリ方式のコストは会話長とメッセージサイズだけでは予測できず保持外誤差が18〜69パーセントに達すること、全履歴より安くなる損益分岐ターンが方式とバックボーンで即時から400ターン超まで大きく散ることを示した計測研究。

- **2026-08 · [To Think or Not to Think: Allocating Reasoning Where It Helps](2026-2609.29664-to-think-or-not-to-think-allocating-reasoning-where-it-helps.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論長の効果が部分的に解ける問題へ集中することを示し、サンプリングした応答群の短半分と長半分の正解率比較から長さ調整の方向だけを推定してGRPOの報酬へ入れるCAREにより、精度を上げながら推論トークンを最大で約37パーセント減らした学習手法の研究。

- **2026-08 · [Thinking Hard, Not Smart: Reasoning Models Fail to Ration Test-Time Compute Across Questions](2026-2608.07968-thinking-hard-not-smart-reasoning-models-fail-to-ration-test-time-comput.md)**  
  実装：[✓](https://github.com/Fcr09/thinking-hard-not-smart) ・ リポジトリ内被引用：0  
  長い思考を許す推論言語モデルは、一問ごとの数学・コード問題で精度を高められる。しかし現実の計算資源は有限であり、複数の依頼を同時に処理する場合には「どの問題へ何トークン使うか」「いつ諦めて別の問題へ進むか」という別の判断が必要になる。この論文は新しい高速化カーネルや推論サービング基盤を提案するものではない。

- **2026-08 · [Task-Aware Spectral Pruning: A Mixture-of-Masks Framework for Efficient LLM Inference](2026-2609.29499-task-aware-spectral-pruning-a-mixture-of-masks-framework-for-efficient-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スペクトル記述子が課題別除去損害を予測できるかを事前に判定し、通過時だけ課題族ごとの依存閉鎖マスクを構築してターン単位で振り分ける枝刈りで、70Bの計算量43パーセント削減時に保持率97.7パーセントとデコード1.44倍を両立する。

- **2026-08 · [RUTA: Principled Visual Token Allocation via Rate-Utility Optimization](2026-2608.04132-ruta-principled-visual-token-allocation-via-rate-utility-optimization.md)**  
  実装：[✓](https://github.com/Multimedia-Analytics-Laboratory/RUTA) ・ リポジトリ内被引用：0  
  視覚トークンの削減を率と効用の最適化として定式化し、質問に合わせて候補を絞り、保持確率の合計への罰則で入力ごとに個数を学ばせ、落とした分の情報を錨へ吸収させることで、全トークンの数パーセントで性能の9割前後を保つ削減方式。

- **2026-08 · [RLCascadeRouter: Quality-Estimator-Free Cascade Routing via Reinforcement Learning](2026-2608.15817-rlcascaderouter-quality-estimator-free-cascade-routing-via-reinforcement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  品質推定器を使わず、停止とモデル選択を強化学習の方策として直接学ぶカスケードルーティングで、予測誤差と決定損失のずれを解消し、性能とコストの釣り合いを改善する。

- **2026-08 · [Ripple-Pivot Search: Active Parallel Decoding for Diffusion Large Language Models](2026-2608.11742-ripple-pivot-search-active-parallel-decoding-for-diffusion-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中エントロピーの位置を先に確定する波及効果を使い、ピボット位置と置くトークンの両方を先読みで探す学習不要の探索で、拡散言語モデルの並列デコードを4〜10倍速くする方式。

- **2026-08 · [Pro-Router: Token-Aware Progressive Model Routing with Adaptive Edge-Cloud Collaboration for Efficient Multimodal LLM Inference](2026-2608.28726-pro-router-token-aware-progressive-model-routing-with-adaptive-edge-clou.md)**  
  実装：[✓](https://github.com/xinyuangui2/pro-router) ・ リポジトリ内被引用：0  
  プロンプトの事前スコアと小モデル自身のトークン分布から読む自信で二段に振り分け、実測レートで配分を決めるエッジ・クラウド協調により、最高のルーティング精度と既存比75パーセント超のスループット向上を両立する研究。

- **2026-08 · [PaDoc: Layout-Grounded Parallel Decoding for Document Parsing](2026-2608.06146-padoc-layout-grounded-parallel-decoding-for-document-parsing.md)**  
  実装：[✓](https://github.com/Longin-Yu/Padoc) ・ リポジトリ内被引用：0  
  配置を枝分かれ構造とみなし、ページ画像を共有したまま領域ごとの内容生成を同時に進める因数分解で、逐次生成の深さを最長の配置と内容の経路まで縮め、品質を保ったまま処理量を最大2倍超にした文書解析方式。

- **2026-08 · [LowRankArena: A Standardized Evaluation Platform for SVD-Based LLM Compression](2026-2608.26389-lowrankarena-a-standardized-evaluation-platform-for-svd-based-llm-compre.md)**  
  実装：[✓](https://github.com/Zishan-Shao/lowrankarena) ・ リポジトリ内被引用：0  
  特異値分解（Singular Value Decomposition; SVD）を使う低ランク圧縮は、重み行列を二つの小さな行列の積に分解し、保存するパラメータと演算量を減らす。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの融合カーネル・4/8ビット量子化・グラフコンパイルを単体とE2Eで測定し、局所高速化が起動律速や品質へどう波及するかを分解して、置換可能な最適化の限界を明らかにする研究。

- **2026-08 · [Dynamic Resolution Routing for Efficient Egocentric Grounding](2026-2608.01638-dynamic-resolution-routing-for-efficient-egocentric-grounding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低解像度画像で対象らしい場所を予測し、選ばれたパッチだけを高解像度で符号化して低解像度文脈へ順序を保って差し込む解像度ルーティングで、視覚トークンを最大67パーセント減らしながら全解像度性能の86.4パーセントを保ち、枝刈り方式より最大1.66倍速くする。

- **2026-08 · [DRLM: Deep Reinforcement Learning-Based LLM Query Orchestration in Edge Environments](2026-2609.00442-drlm-deep-reinforcement-learning-based-llm-query-orchestration-in-edge-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クエリの意味分類に基づく品質推定と特徴ベースの遅延予測を、装置の負荷状態とともに因子化PPOへ入力し、エッジ上のモデル・装置・量子化の割当てをクエリごとに決めるLLMオーケストレーション。遅延最大51パーセント減と引き換えに正解率は最大8パーセント低下する。

- **2026-08 · [Diagnose Before You Compress: Prediction-Independent Bottleneck Witness Refinement for LLM Serving Traces](2026-2608.00423-bottleneck-preserving-witnessing.md)**  
  実装：[✓](https://github.com/llmllmllm/BPW) ・ リポジトリ内被引用：0  
  スケジューリング・入力処理・生成・KVキャッシュの各ボトルネックを実機測定で独立確認し、四要素すべてに複数の証拠を残す小さなLLMサービング再生用トレースを選ぶ。

- **2026-08 · [DeaMoE: Efficient MoE Structure for Fast Small-Batch Decoding](2026-2608.14385-deamoe-efficient-moe-structure-for-fast-small-batch-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパートを部門へまとめ大きな射影を共有させ、私有の小さな変換だけで分化させるMoE構造と部門先行の2段ルーティングで、小バッチデコードのエキスパート重み読み込みを最大約半分にし、品質を保ったままTPOTを最大1.33倍高速化した。

- **2026-08 · [Beyond Tokens: A Survey on Decoding Methods for Large Language and Vision-Language Models](2026-2608.14797-beyond-tokens-a-survey-on-decoding-methods-for-large-language-and-vision.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象はモデルの重みを更新する学習ではなく、既存モデルが出力した確率分布を、推論時にどのようなトークン列へ変換するかという復号（デコード）の設計である。表1の年代と分類は文献整理の結果であり、速度・品質の絶対値や改善倍率を示す統一ベンチマークではない。

- **2026-08 · [Beyond Accuracy: Auditing Spatial Provenance in Visual Token Pruning for OCR-Critical MLLM Inference](2026-2608.00077-beyond-accuracy-auditing-spatial-provenance-in-visual-token-pruning-for-.md)**  
  実装：[✓](https://github.com/SouthWinter/spatial-provenance-audit) ・ リポジトリ内被引用：0  
  視覚トークンを間引けば言語モデル側の事前計算（プリフィル）とその作業用メモリを削減できるが、単に「保持率30%で正答率がほぼ同じ」という評価には穴がある。さらにトークンを統合する手法については、統合出力の出自集合と、代表位置で局所的に追跡できる範囲を区別する。

- **2026-07 · [WaveZip: Wavelet-Driven Space-Time Decoupling for Video Token Condensation](2026-2607.23265-wavezip-wavelet-driven-space-time-decoupling-for-video-token-condensatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ウェーブレット変換で時間の傾向と空間の細部を周波数で分離し、場面変化で関連度の揺れを整え、質問に合う高周波だけを強めてから予算配分する学習不要の動画トークン圧縮で、10倍圧縮でも全入力の99.6パーセントの性能を保った。

- **2026-07 · [Seeing the End at Step Zero: Accelerating Diffusion MLLMs via MLP Sparsity-Aware Truncation](2026-2607.14557-seeing-the-end-at-step-zero-accelerating-diffusion-mllms-via-mlp-sparsit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型マルチモーダルモデルの初回ステップでMLP活性の疎さから応答の終わりを検出して冗長な末尾を一括切り捨てる学習不要の方式で、精度を保ちながらスループットを最大約31倍にした。

- **2026-07 · [SeDeM: Selective Decompression of Hidden-State Memories for Long-Context Question Answering](2026-2608.00311-sedem-selective-decompression-of-hidden-state-memories-for-long-context-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈を隠れ状態メモリに圧縮保存し、質問に合う区間だけを復元してデコーダ中間層へ注入する選択的復元方式で、圧縮手法群を上回り3Bでは全長処理の参照も3データセットで超えた。

- **2026-07 · [Rethinking the Generation Order of Block Diffusion Language Models](2026-2607.24306-rethinking-the-generation-order-of-block-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック内の位置は任意順で確定できるように見えるが、既存の並列サンプリング方式をそのまま移植すると、先の位置だけを確定して前方の未確定位置を残し、コードや推論の構造を壊す場合がある。

- **2026-07 · [PartRep: Learning What to Repeat for Decoder-only LLMs](2026-2607.01792-partrep-learning-what-to-repeat-for-decoder-only-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プロンプトを全部繰り返す代わりに、負の対数尤度が高い情報密度の高いトークンだけを初期層ゲートで選んで繰り返し、全繰り返しの精度利得をKVキャッシュ59.4パーセントで近似する選択的拡張。

- **2026-07 · [From Static Inference to Dynamic Interaction: A Survey of Streaming Large Language Models](2026-73c7c240d868-from-static-inference-to-dynamic-interaction-a-survey-of-streaming-large.md)**  
  実装：[✓](https://github.com/EIT-NLP/Awesome-Streaming-LLMs) ・ リポジトリ内被引用：0  
  さらに同時入出力で生じる注意依存の競合、位置IDの衝突、読み書きタイミングの決定を、アーキテクチャと制御ポリシーの独立した設計軸として比較する。

- **2026-07 · [From Expert Reduction to Behavioral Divergence: Tracing Numerical State through Sparse MoE Inference](2026-2607.28097-from-expert-reduction-to-behavioral-divergence-tracing-numerical-state-through-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎MoEの専門家加算順序だけで内部状態と生成文が分岐しうることを全順列・状態再構成で実証し、BF16項＋FP32累算を評価範囲の安定な互換契約として特定する。

- **2026-07 · [CORVUS: Context Optimization and Reduction Via Underlying Synchronization for LLM Coding Agents](2026-2607.22711-corvus-context-optimization-and-reduction-via-underlying-synchronization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コード編集を行う大規模言語モデル（LLM）エージェントは、ファイル読込み、編集、試験、再読込みを何度も繰り返す。従来の追記専用履歴では、読込み時のファイル本文が道具の観測結果として永久に残り、後で同じファイルが変更されても古い本文は削除されない。エージェントがその古い記述を使って修正すると、適用位置の不一致や失敗が起こり、さらに再読込みと再試行を繰り返す。

- **2026-07 · [ConvX: A Lightweight Converter to Bridge Indexed Dense Representations and Large Language Models for Retrieval-Augmented Generation](2026-2812aba9b42f-convx-a-lightweight-converter-to-bridge-indexed-dense-representations-an.md)**  
  実装：[✓](https://github.com/NLPlab-skku/ConvX) ・ リポジトリ内被引用：0  
  検索器が索引時に作った密ベクトルを、語彙復元で学習した軽量コンバータで固定個数のメモリスロットへ展開して生成モデルへ渡し、文書本文の再入力なしに16倍から128倍の圧縮率で検索付き生成を行う方式。

- **2026-07 · [Conformal Cascade: Distribution-Free Accuracy Guarantees for Multi-Tier LLM Inference](2026-2607.25018-conformal-cascade-distribution-free-accuracy-guarantees-for-multi-tier-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  カスケードの振り分けを信頼度閾値から適合予測集合の大きさへ替え、誤り予算から閾値を決めて分布に依らない精度保証を与え、72組の評価で49組で最良ヒューリスティクスを上回る方式。

- **2026-07 · [C-PTQ: Fisher-weighted Channel-wise Sensitivity for Post-training Quantization of MLLMs](2026-2607.21076-c-ptq-fisher-weighted-channel-wise-sensitivity-for-post-training-quantiz.md)**  
  実装：[✓](https://github.com/renaissanceee/cptq) ・ リポジトリ内被引用：0  
  対角フィッシャー情報でチャネルごとの量子化残差を重み付け、感度の粒度とスケーリングの粒度を揃えるマルチモーダルモデルの学習後量子化C-PTQ。補助モジュールなしで最良水準の精度を保つ。

- **2026-07 · [Benchmarking Confidential GPU Inference on NVIDIA H100 under Intel TDX](2026-2607.19353-benchmarking-confidential-gpu-inference-on-nvidia-h100-under-intel-tdx.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著はサービス指標の比較研究であり、GPU内部の暗号化処理、PCIe転送、HBM帯域、スケジューラのどれが何%の原因かまで分解したマイクロアーキテクチャ解析ではない。

- **2026-07 · [AdaMix: Adaptive Mixing for Short and Long Reasoning Adapters](2026-812fc13a8ba3-adamix-adaptive-mixing-for-short-and-long-reasoning-adapters.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論の長さと深さを担う2つのLoRAアダプタを別々に強化学習で鍛え、問題の難しさに応じて重みを線形補間することで、考えすぎを削りながら難しい問題の精度も伸ばす適応型推論の枠組み。

- **2026-06 · [Unveiling the Entropy Dynamics of Chain-of-Thought Reasoning](2026-2606.02020-unveiling-the-entropy-dynamics-of-chain-of-thought-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoTの予測エントロピーが探索局面から収束局面へ急峻に遷移することを示し、その遷移をCUSUM変化点検出で学習なしに捉えて早期終了と重み付き投票に使うことで、精度を保ちながらトークンを11.1%削減した研究。

- **2026-06 · [Understanding Evaluation Illusion in Diffusion Large Language Models](2026-2606.29228-understanding-evaluation-illusion-in-diffusion-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は新しい復号器の提案ではなく、既存の復号方式を同じ条件で比較するための評価方法論の研究である。結果は、少し異なるテンプレートを使うだけで方式間の優劣が逆転し、単一テンプレートで測った「品質を維持した高速化」が再現しない場合があるというものだった。

- **2026-06 · [The Language-Energy Divide: Measuring Energy Costs of Multilingual LLM Inference](2026-2606.21869-the-language-energy-divide-measuring-energy-costs-of-multilingual-llm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一二二言語で推論エネルギーを実機計測し、トークン当たりで最大八・三倍、応答当たり総量で英語比一七九倍の言語間格差があること、その主因が低資源言語でのトークン単価上昇と出力トークン数膨張の掛け算であり、格差がモデル・ハードウェア・課題を変えても残ることを明らかにした。

- **2026-06 · [MARS: Margin-Adversarial Risk-controlled Stopping for Parallel LLM Test-time Scaling](2026-2606.12935-mars-margin-adversarial-risk-controlled-stopping-for-parallel-llm-test-t.md)**  
  実装：[✓](https://github.com/Wenbo11/MARS) ・ リポジトリ内被引用：0  
  途中回答の投票の票差が、将来の変更による敵対的な損害を上回ることを証明してから並列生成を止める停止規則で、精度を保ったまま自己整合性のトークンを25から47パーセント削減する。

- **2026-06 · [Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention](2026-2606.26560-erase-then-delta-attention-decoupling-erase-and-write-addresses-in-delta.md)**  
  実装：[✓](https://github.com/QwenLM/FlashQLA) ・ リポジトリ内被引用：0  
  デルタルール線形注意の能動的な修正が書き込みアドレスに固定される問題に対し、学習された別の消去アドレスで古い連想を先に消してから通常のデルタ書き込みを行う更新規則を提案し、2.5Bと25B-A2.8Bの事前学習と4k〜128kの長文脈評価で比較対象を上回る平均スコアを示した研究。

- **2026-06 · [Differentiable Efficient Operator Search](2026-2606.05232-differentiable-efficient-operator-search.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈り・マージ・プーリング・リウェイティングを単一の連続演算子空間に統一し、層選択・保持予算・演算子パラメータを微分可能に探索することで、厳しい視覚トークン予算ほど人手設計を上回る削減構成を見つける枠組み。

- **2026-06 · [DeepLook: Uncertainty-Guided Branching with Lookahead Confidence for Efficient Reasoning](2026-2607.22602-deeplook-uncertainty-guided-branching-with-lookahead-confidence-for-effi.md)**  
  実装：[✓](https://github.com/txyang1/deeplook) ・ リポジトリ内被引用：0  
  推論トレースをセグメント単位で監視し、不確実性が集中する地点でのみ分岐して、先読み区間の平均信頼度で候補を順位付けし枝刈りする学習不要のデコーディング法を提案し、数学で精度を保ちながら生成トークンを大きく減らせることと、知識集約型課題では効かなくなる境界を示した研究。

- **2026-06 · [Cold Start Latency of Quantized Small Language Models on Serverless CPU Infrastructure](2026-9a95feba0c73-cold-start-latency-of-quantized-small-language-models-on-serverless-cpu-.md)**  
  実装：[✓](https://github.com/mingwho/slm-research) ・ リポジトリ内被引用：0  
  本論文は、アクセス頻度の低い小型言語モデル（Small Language モデル; SLM）を、要求が来たときだけ起動するサーバーレス基盤で提供する際の遅延を測る研究である。利用者の要求がないときに実行環境をゼロへ縮退させられる反面、次の要求時にはコンテナを起こし、量子化重みを読み込み、トークンを生成する必要がある。

- **2026-06 · [Characterizing Software Aging in GPU-Based LLM Serving Systems](2026-2606.11916-characterizing-software-aging-in-gpu-based-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  6種類のGPU LLMサービング構成を計216時間連続運転し、全構成でホスト側のメモリ経年劣化を検出。リーク率はvLLM V1単体+1.8KB/時からTriton+V0の+157KB/時まで大差があり、配置・ランタイム選択が長期信頼性を左右することを示す。

- **2026-06 · [Breaking the Ice: Analyzing Cold Start Latency in vLLM](2026-2606.07362-breaking-the-ice-analyzing-cold-start-latency-in-vllm.md)**  
  実装：[✓](https://github.com/upb-cn/vllm-startup-profiler) ・ リポジトリ内被引用：0  
  vLLMの起動を6段階へ分解して初めて体系的に量り、全体が主にCPU律速で各段階が特定の量へほぼ線形に従うことを示し、段階別回帰の予測器で平均二乗誤差2.42秒の予測を達成した。

- **2026-06 · [Beyond Per-Token Pricing: A Concurrency-Aware Methodology for LLM Infrastructure Cost Estimation](2026-2606.11690-beyond-per-token-pricing-a-concurrency-aware-methodology-for-llm-infrast.md)**  
  実装：[✓](https://github.com/pChitral/vllm-cost-meter) ・ リポジトリ内被引用：0  
  本研究はこの差を、要求到着率を明示した費用測定問題として定式化する。ハードウェア、モデル構造、量子化精度、要求到着率、遅延目標を分け、同じGPUでも負荷によって費用がどの程度変わるかを実機で測る。H100 NVLの主実験では、3種類のモデルと2種類の精度の計6構成を7段階の要求率で測定し、同じ構成内で17.5～36.3倍の出力トークン単価差を観測した。

- **2026-06 · [Benchmarking Large Language Model Inference on Limited-Resource Edge Systems](2026-1b6cd9d3f031-benchmarking-large-language-model-inference-on-limited-resource-edge-sys.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  12件の小型・中型モデルについて生成型精度とJetson実機のスループット・電力を二重測定で結び付け、GPU実行が電力増にもかかわらずエネルギー効率を0.453から0.823トークン毎ジュールへ上げることと、精度と効率の交換がモデル規模で決まることを示すベンチマーク。

- **2026-06 · [AVIS: Adaptive Test-Time Scaling for Vision-Language Models](2026-2606.11576-avis-adaptive-test-time-scaling-for-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンを減らして浮いた計算を、難しい問いの追加推論へ回せれば、計算を減らしつつ精度を維持・改善できる可能性がある。推論探索量を制御するVisual Reasoning Scaling（VRS）では、視覚埋め込みから問題の解答可能性を予測し、自己整合性多数決の試行数Kを1、3、5、7から選ぶ。

- **2026-06 · [Agentic Chain-of-Thought Steering for Efficient and Controllable LLM Reasoning](2026-2606.03965-agentic-chain-of-thought-steering-for-efficient-and-controllable-llm-rea.md)**  
  実装：[✓](https://github.com/Andree-9/ACTS) ・ リポジトリ内被引用：0  
  凍結した推論モデルの思考を、別に学習した制御エージェントが戦略と誘導句でステップごとに操舵する方式で、正解率を保ちながら思考トークンを3割から6割削り、予算による制御も可能にした。

- **2026-06 · [Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads](2026-2606.06448-agent-memory-characterization-and-system-implications-of-stateful-long-h.md)**  
  実装：[✓](https://github.com/Tambe-Lab/agent-memory-profiling) ・ リポジトリ内被引用：0  
  本研究は、長期にわたり複数のセッションをまたいで稼働する大規模言語モデル（LLM）エージェントの「記憶」を、回答品質を高める機能としてだけでなく、計算・メモリ・入出力・スケジューリングの対象となる実行時システムとして捉え直す。後者は前者の約26.5倍である。

- **2026-05 · [Switchcraft: AI Model Router for Agentic Tool Calling](2026-2605.07112-switchcraft-ai-model-router-for-agentic-tool-calling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  道具呼出しごとの厳密な正しさを予測する較正済みDistilBERT分類器で、予算内で最も安い正解見込みモデルを選び不可能な要求は棄却することで、単一最良モデルより59パーセント安く高い正解率を出すエージェント向けモデルルーター。

- **2026-05 · [MindFusion: Communication-Efficient Mobile-Cloud Orchestration for MLLMs](2026-43a5561dce36-mindfusion-communication-efficient-mobile-cloud-orchestration-for-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生データを端末に残すモバイルとクラウドの分割実行で、デコードをクラウド内に閉じさせる近道と画像特徴だけの8分の1圧縮により、最初のトークンまでの遅延を87パーセント減らしデコードを最大25倍速くしながら転送量を70パーセント以上削る方式。

- **2026-05 · [Measuring Maximum Activations in Open Large Language Models](2026-2605.15572-measuring-maximum-activations-in-open-large-language-models.md)**  
  実装：[✓](https://github.com/clx1415926/Max_act_llm) ・ リポジトリ内被引用：0  
  低ビット推論では、活性値を少数の離散水準へ写すときに、値の最大絶対値が量子化尺度の決定を左右する。近い規模のMoEモデルは密モデルより14.0〜23.4倍低い極大値を示す。

- **2026-05 · [Mapping text to multiplex graph: Prompt compression as Lévy walk-guided graph pruning](2026-2607.01241-mapping-text-to-multiplex-graph-prompt-compression-as-l-vy-walk-guided-g.md)**  
  実装：[✓](https://anonymous.4open.science/r/RAGP-B0CB) ・ リポジトリ内被引用：0  
  テキストを注意の局所層と意味の大域層からなる多重グラフへ写し、レヴィ歩行の訪問頻度で冗長でないノードを選ぶことで、構造を保ったままプロンプトを圧縮する。

- **2026-05 · [Linear Scaling Video VLMs for Long Video Understanding](2026-2605.31598-linear-scaling-video-vlms-for-long-video-understanding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い動画を視覚言語モデル（Vision-Language モデル; VLM）へ入力すると、映像から得られる視覚トークンが時間とともに増え、各フレームが過去の全フレームへ自己注意（self-注意機構）を計算する通常の実装では、全映像を処理する事前充填（プリフィル）の計算量がフレーム数 N に対して二次的に増える。

- **2026-05 · [LensVLM: Selective Context Expansion for Compressed Visual Representation of Text](2026-2605.07019-lensvlm-selective-context-expansion-for-compressed-visual-representation.md)**  
  実装：[✓](https://github.com/apple-aiml-research/ml-lensvlm) ・ リポジトリ内被引用：0  
  テキストを画像化して圧縮し、根拠画像だけを未圧縮へ展開する道具使用を教師あり学習と強化学習で教え、実効圧縮4.3倍で全文並みの精度を保つ視覚言語モデルの推論枠組み。

- **2026-05 · [LEAP: Layer-wise Exit-Aware Pretraining for Efficient Transformer Inference](2026-2605.01058-leap-layer-wise-exit-aware-pretraining-for-efficient-transformer-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層対応の蒸留が早期終了の前提である表現の収束を潰す非両立性を特定し、中間層を最終層へ近づける制約を蒸留へ加えたLEAPで、蒸留モデルでも収束ベースの早期終了により1.61倍の実測高速化を得た研究。

- **2026-05 · [LEAD: Length-Efficient Adaptive and Dynamic Reasoning for Large Language Models](2026-2605.09806-lead-length-efficient-adaptive-and-dynamic-reasoning-for-large-language-.md)**  
  実装：[✓](https://github.com/CrazyMint/LEAD) ・ リポジトリ内被引用：0  
  推論モデルの冗長な思考を削る強化学習法。正しさと長さの報酬を分離正規化し、重みを信号の不安定さと改善余地でオンライン調整、目標長を問題ごとの正解出力の平均から自動較正することで、1.5Bモデルで正解率を上げながら平均長を約6割削減した。

- **2026-05 · [KernelBrain: Coarse-to-Fine, Budget-Aware Search for Agentic GPU Kernel Optimization](2026-2608.02611-kernelbrain-coarse-to-fine-budget-aware-search-for-agentic-gpu-kernel-op.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Tritonカーネルの自動最適化を、専門家誘導の多様な候補生成と多忠実度のふるいとプロファイラ診断付き変異で回し、PyTorch比最大6.72倍と最先端エージェント比最大1.4倍を最適化時間最大48%減で得るエージェント研究。

- **2026-05 · [INAR-VL: Input-Aware Routing for Edge–Cloud Vision–Language Inference](2026-2605.18853-inar-vl-input-aware-routing-for-edge-cloud-vision-language-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像品質とテキスト複雑さの軽い事前信号からモデルと配置と解像度をリクエストごとに選ぶ端末・クラウド振り分けシステムで、36パーセントを端末処理しながらクラウドのみ比で遅延24パーセント・エネルギー26パーセント削減と精度の97パーセント維持を実機で示した研究。

- **2026-05 · [Identifying and Mitigating Systemic Measurement Bias in Production LLM Inference Benchmarks](2026-2605.24217-identifying-and-mitigating-systemic-measurement-bias-in-production-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ベンチマーク用クライアントの単一プロセス構造が待ち行列となり遅延を水増しする測定バイアスを、待ち行列理論とシミュレータ相手の実測で示し、複数プロセスへの負荷分散と複合指標NTPOTによる是正策を提示した研究。

- **2026-05 · [HEED: Density-Weighted Residual Alignment for Hybrid Vision-Language Model Distillation](2026-2605.17093-heed-density-weighted-residual-alignment-for-hybrid-vision-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハイブリッドVLMへの蒸留で細部の視覚情報だけが落ちる失敗を、残差のずれが高密度パッチへ集中する現象として診断し、整列損失の重みをパッチ密度で配り直すHEEDで、推論費用を変えずにOCR系の成績を回復させる研究。

- **2026-05 · [CSR: Infinite-Horizon Real-Time Policies With Massive Cached State Representations](2026-2605.07325-csr-infinite-horizon-real-time-policies-with-massive-cached-state-repres.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ロボットの状態履歴を書き換えない静的プリフィックスと小さな動的末尾へ分け、追い出しは別資源で裏側に再計算して差し替えることで、235Bモデルと12万トークン文脈の応答開始遅延を14.67秒から0.56秒へ26倍下げ、想起率でも検索型を上回る枠組み。

- **2026-04 · [TRACES: Tagging Reasoning Steps for Adaptive Cost-Efficient Early-Stopping](2026-2604.21057-traces-tagging-reasoning-steps-for-adaptive-cost-efficient-early-stoppin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論ステップの役割を生成中にタグ付けし、正解到達後に起きる「構成から評価へ」の種類の移行を検出して生成を止めることで、精度を保ちながらトークンを2割から5割減らす解釈可能な早期停止。

- **2026-04 · [SMoES: Soft Modality-Guided Expert Specialization in MoE-VLMs](2026-2604.23996-smoes-soft-modality-guided-expert-specialization-in-moe-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SMoES（Soft Modality-guided 専門家 Specialization）は、視覚・言語モデル（Vision-Language モデル, VLM）の専門家混合（Mixture of エキスパート, MoE）層で、画像由来トークンと文章由来トークンが各層でどの程度混合しているかを推定し、専門家の配置と学習を調整する方式である。

- **2026-04 · [Quantized Transformers in Practice: Benchmarking Full- and Low-Precision LLMs across Two Processors](2026-f22ed3216fa9-quantized-transformers-in-practice-benchmarking-full-and-low-precision-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は新規の量子化アルゴリズムを提案するものではなく、既存の8ビット学習後量子化を一般的なノートPC向けGPUに適用した場合、モデルの収容可否、生成時間、生成文の一致度がどのように変化するかを実測する。著者の要旨はCPUオフロードの影響を受けた条件を除外した平均高速化を3.4倍と記すが、個別の表3は非常に不均一である。

- **2026-04 · [On the Quantization Robustness of Diffusion Language Models in Coding Benchmarks](2026-2604.20079-on-the-quantization-robustness-of-diffusion-language-models-in-coding-be.md)**  
  実装：[✓](https://github.com/zinichakraborty/Diffusion-LLM-Quantization-Robustness) ・ リポジトリ内被引用：0  
  推論用重みを低ビットで表す学習後量子化（post-学習 量子化; PTQ）はこの費用を減らす有力な方法だが、自己回帰型で得られた量子化の知見を拡散型へそのまま適用できるとは限らない。重要な留保として、混合精度実験は量子化を模擬しても重みを浮動小数点形式で保存する方式であり、低ビットの実物理容量削減を実測した結果ではない。

- **2026-04 · [Multi-objective Evolutionary Merging Enables Efficient Reasoning Models](2026-2604.06465-multi-objective-evolutionary-merging-enables-efficient-reasoning-models.md)**  
  実装：[✓](https://github.com/iacobellimario/L2S-MultiObjective-Evolutionary-Merging) ・ リポジトリ内被引用：0  
  速い思考モデルと遅い思考モデルの重み補間係数を精度と出力長の2目的で進化探索し、パレートフロントを求める学習不要のLong-to-Shortマージ手法。

- **2026-04 · [LayerBoost: Layer-Aware Attention Reduction for Efficient LLMs](2026-2604.22050-layerboost-layer-aware-attention-reduction-for-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層ごとの感度測定に基づいて注意を残す層・窓注意にする層・外す層を決め、軽い蒸留で回復する注意削減手法。一律線形化より性能低下を小さく抑え、高同時実行で大きく速くなる。

- **2026-04 · [IWP: Token Pruning as Implicit Weight Pruning in Large Vision Language Models](2026-2604.00757-iwp-token-pruning-as-implicit-weight-pruning-in-large-vision-language-mo.md)**  
  実装：[✓](https://github.com/jhtwosun/IWP) ・ リポジトリ内被引用：0  
  視覚トークンを削る従来方式は、注意重みの大きいトークンを残す、埋込み表現が似たトークンをまとめるなどの経験的基準を使うことが多い。LLaVA-OneVision-7Bの88.9%削減条件では、全トークン時1.37秒から0.64秒へ実測レイテンシを短縮する一方、品質指標は95.9%から89.5%へ下がる。

- **2026-04 · [ID-Selection: Importance-Diversity Based Visual Token Selection for Efficient LVLM Inference](2026-2604.05601-id-selection-importance-diversity-based-visual-token-selection-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  候補N個からT個を残す計算量は概ねO(NT)であり、TがNより十分小さい強い圧縮で実用的とされる。LLaVA-1.5-7Bでは576個の視覚トークンを16個へ削減しても、9課題の集計で元モデルの91.8%の性能を維持する。

- **2026-04 · [Efficient Multimodal Spatial Reasoning via Dynamic and Asymmetric Routing](2026-22e11514f14e-efficient-multimodal-spatial-reasoning-via-dynamic-and-asymmetric-routin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これにより複雑な空間関係を段階的に処理できるが、過去の中間トークンが自己回帰的に蓄積し、注意計算・KVキャッシュ・推論遅延を押し上げる。既存の固定率圧縮では、初期段階で必要な画像細部を落としたり、深い層ですでに冗長な視覚トークンを残したりする。

- **2026-04 · [Comparative Characterization of KV Cache Management Strategies for LLM Inference](2026-2604.05012-comparative-characterization-kv-cache-management-strategies-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLM、H2O、InfiniGenをH100実機で比較し、GPUメモリを最大約70%減らすH2O、初期事実を保ちやすいInfiniGen、速度に優れるvLLMの条件別の使い分けを明らかにする。

- **2026-04 · [Caracal: Causal Architecture via Spectral Mixing](2026-2605.00292-caracal-causal-architecture-via-spectral-mixing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Caracalは、Transformerの全域注意（global 注意機構）を多頭フーリエ混合（Multi-Head Fourier、MHF）で置き換える言語モデルの設計である。ただし、論文の主要な高速化評価は文脈長を変えた訓練処理であり、一般的なLLM配信での1トークンずつの逐次生成が同率で高速化することを示したものではない。

- **2026-04 · [Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning](2026-2604.05404-beyond-accuracy-unveiling-inefficiency-patterns-in-tool-integrated-reaso.md)**  
  実装：[✓](https://github.com/sqs-ustc/tool-reasoning-framework-PTE) ・ リポジトリ内被引用：0  
  本論文は、推論と外部ツール利用を交互に行うツール統合推論（tool-integrated reasoning; TIR）の計算費用の測り方を提案する。

- **2026-04 · [Awakening Dormant Experts: Counterfactual Routing to Mitigate MoE Hallucinations](2026-2604.14246-awakening-dormant-experts-counterfactual-routing-to-mitigate-moe-halluci.md)**  
  実装：[✓](https://github.com/ZhaiYanbo/CoR) ・ リポジトリ内被引用：0  
  眠った専門エキスパートを反事実影響で起こし、総活性数を変えずに層間予算を知識層へ移すことで、事実性平均を約2ポイント上げ静的増量を上回る学習なしのルーティング是正。

- **2026-03 · [Towards Efficient Large Vision-Language Models: A Comprehensive Survey on Inference Strategies](2026-2603.27960-towards-efficient-large-vision-language-models-a-comprehensive-survey-on.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Surendra PathakとBo Hanによる本サーベイは、大規模視覚言語モデル（LVLM）の推論を高速化・省メモリ化する既存研究を、①視覚トークン圧縮、②KVキャッシュ管理とサービング、③モデル構造と注意計算の最適化、④高度な復号戦略という四つの層に整理する。

- **2026-03 · [SVD Contextual Sparsity Predictors for Fast LLM Inference](2026-2603.14110-svd-contextual-sparsity-predictors-for-fast-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ゲート行列のデータ重み付き特異値分解による低ランク近似を学習不要のスパース性予測器とし、ニューロン別閾値の貪欲較正と逐次実行で、平均90パーセントのスパース性のもとデコードを最大1.8倍高速化する。

- **2026-03 · [Sustainability Is Not Linear: Quantifying Performance, Energy, and Privacy Trade-offs in On-Device Intelligence](2026-2603.26603-sustainability-is-not-linear-quantifying-performance-energy-and-privacy-.md)**  
  実装：[✓](https://github.com/eziyoo/LLMs-on-Devices) ・ リポジトリ内被引用：0  
  無改造の旗艦スマートフォンで8モデルと2種類の4ビット量子化を速度・エネルギー・品質で実測し、重要度配慮型量子化はメモリを減らしても電池を節約せず、混合専門家モデルは7B級の容量を持ちながら1Bから2B級のエネルギーで動くことを示した計測研究。

- **2026-03 · [Spend Less, Reason Better: Budget-Aware Value Tree Search for LLM Agents](2026-2603.12634-spend-less-reason-better-budget-aware-value-tree-search-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実サービスではツール呼び出し回数、生成トークン数、API料金に上限があるため、単に推論を長くする方式は適さない。原著はgpt-oss-20bとQwen3-30B-A3B-Instruct-2507を用い、HotpotQA、2WikiMultihopQA、MuSiQue、Bamboogleで評価した。

- **2026-03 · [AE-LLM: Adaptive Efficiency Optimization for Large Language Models](2026-2603.20492-ae-llm-adaptive-efficiency-optimization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  効率化手法の組合せを多目的最適化として自動探索する枠組み。代理モデルの予測と進化探索で、精度・遅延・メモリ・エネルギーのバランスが取れた構成を配備条件ごとに見つける。

- **2026-02 · [On the Optimal Reasoning Length for RL-Trained Language Models](2026-2602.09591-on-the-optimal-reasoning-length-for-rl-trained-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長くすることで最頻回答が正解になる問題は増えるが、その正解周辺に個々の標本が集中しなくなるため、単発回答の成功率が下がり得る。

- **2026-02 · [Just on Time: Token-Level Early Stopping for Diffusion Language Models](2026-2602.11133-just-on-time-token-level-early-stopping-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの各位置で上位2確率の比を確信度として測り、確定済み近傍に近い位置ほど閾値を下げる空間変調付きの学習不要なトークン単位早期終了で、生成ステップを大幅に減らす方式。

- **2026-02 · [CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute](2026-2602.08948-corefine-confidence-guided-self-refinement-for-adaptive-test-time-comput.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論トレース全体の信頼度の動態を小さなConv1Dコントローラで読み、停止・再検討・別方針を選ぶ適応型の自己洗練により、512サンプルの多数決と同等以上の精度を約190分の1のトークンで達成した研究。

- **2026-02 · [Architecture-Aware LLM Inference Optimization on AMD Instinct GPUs: A Comprehensive Benchmark and Deployment Study](2026-2603.10031-architecture-aware-llm-inference-optimization-on-amd-instinct-gpus-a-com.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MI325X 8台で2350億から1兆パラメータの4モデルを実測し、注意機構ごとにブロック大きさ・カーネル・KV方針・並列度を変える必要があること、テキストでは密モデル毎秒15,944トークンと活性37億の専門家混合モデル毎秒15,343トークンがほぼ並ぶこと、全モデルが同時約500件で帯域律速に飽和することを示した。

- **2026-02 · [Adaptive Test-Time Compute Allocation for Block Diffusion Language Models in Complex Reasoning](2026-2602.09555-adaptive-test-time-compute-allocation-for-block-diffusion-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック拡散言語モデルのテスト時計算配分として、信頼度の平均で閾値を上下限つきで適応させるデコードと、探索は大きいブロック・推敲は小さいブロックで生成する2段階方式を提案し、高速化と精度向上を両立させた研究。

- **2026-02 · [1-Bit Wonder: Improving QAT Performance in the Low-Bit Regime through K-Means Quantization](2026-2602.15563-1-bit-wonder-improving-qat-performance-in-the-low-bit-regime-through-k-m.md)**  
  実装：[✓](https://github.com/Aleph-Alpha-Research/1-Bit-Wonder) ・ リポジトリ内被引用：0  
  固定した推論メモリ予算の下でビット幅とパラメータ数の配分をスケーリング則で分析し、k-means量子化とQATにより1ビット重みが生成系下流タスクで最良になることを示した研究。

- **2026-01 · [Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct](2026-2601.14277-which-quantization-should-i-use-a-unified-evaluation-of-llama-cpp-quanti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ80億パラメータモデルを半精度から13形式へ変換し、五つの下流課題と困惑度と速度を統一条件で比べ、5ビットと調整のよい4ビットが容量を約3分の2減らしても品質をほぼ保ち、最も強い3ビットだけが推論課題で大きく崩れることを示した実務指針。

- **2026-01 · [Tensor Program Superoptimization through Cost-Guided Symbolic Program Synthesis](2026-5223769ccd56-tensor-program-superoptimization-through-cost-guided-symbolic-program-sy.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.17638076) ・ リポジトリ内被引用：0  
  テンソルプログラムを記号実行で数式化し、スケッチ合成と実測コストモデルの分枝限定法で等価な高速プログラムを自動発見する超最適化器STENSO。NumPyで幾何平均3.8倍、JAXとPyTorchで1.6倍の高速化を報告する。

- **2026-01 · [ProfInfer: An eBPF-based Fine-Grained LLM Inference Profiler](2026-2601.20755-profinfer-an-ebpf-based-fine-grained-llm-inference-profiler.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡張バークレーパケットフィルタの動的プローブで推論エンジンを書き換えずに四つの粒度で計測し、演算子・時系列・統計の三つの図へ変換する、速度低下4パーセント未満の細粒度プロファイラ。

- **2026-01 · [Pay for Hints, Not Answers: LLM Shepherding for Cost-Efficient Inference](2026-2601.22132-pay-for-hints-not-answers-llm-shepherding-for-cost-efficient-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模モデルの応答全体ではなく先頭の接頭辞だけをヒントとして買い、小規模モデルに最終応答を書かせる費用配分で、目標精度を保ちながら推論費用を33から65パーセント削減した。

- **2026-01 · [L³: Large Lookup Layers](2026-2601.21461-l-large-lookup-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  このため、CPUに退避した専門家をGPUへ移す場合は、選択後の転送が計算の待ち時間になりやすい。推論速度はL³の配置に依存し、2.6B稼働モデルで最初のL³を第5層後に置くと、原著表2のバッチ1速度は密モデル776に対して772トークン/秒/系列だった。

- **2026-01 · [FROST: Filtering Reasoning Outliers with Attention for Efficient Reasoning](2026-2601.19001-frost-filtering-reasoning-outliers-with-attention-for-efficient-reasonin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意関数をSoftmax1へ替えて寄与の小さい推論文を生成されにくくする微調整方式で、トークンを約7割削りながら正解率を平均で改善した。

- **2026-01 · [Forest Before Trees: Latent Superposition for Efficient Visual Reasoning](2026-2601.06803-forest-before-trees-latent-superposition-for-efficient-visual-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  残りの視覚推論経路全体を有効窓とし、隠れ状態を窓内の未来意味の重ね合わせへ合わせる学習で、早すぎる意味の収束を防ぎながら推論トークンを97パーセント超減らす潜在視覚推論方式。

- **2026-01 · [EntroCut: Entropy-Guided Adaptive Truncation for Efficient Chain-of-Thought Reasoning in Small-scale Large Reasoning Models](2026-2601.22617-entrocut-entropy-guided-adaptive-truncation-for-efficient-chain-of-thoug.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  反省トークンの地点で探査文字列への続きのエントロピーを測り、確信が十分なら思考を打ち切って応答段階へ移す学習不要の適応的打ち切りで、小規模な推論モデルのトークンを最大約40%削りながら精度をほぼ保つ方式。

- **2025-12 · [Viability and Performance of a Private LLM Server for SMBs: A Benchmark Analysis of Qwen3-30B on Consumer-Grade Hardware](2025-2512.23029-viability-and-performance-of-a-private-llm-server-for-smbs-a-benchmark-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RTX 5090を1基使う自社サーバーで量子化Qwen3-30Bを実測した分析研究。品質はMMLU83パーセントでクラウドに近い一方、同時利用が増えると1人あたり効率が急落し、実用範囲は軽い同時利用に限られることを示す。

- **2025-12 · [Understanding and Harnessing Sparsity in Unified Multimodal Models](2025-2512.02351-understanding-and-harnessing-sparsity-in-unified-multimodal-models.md)**  
  実装：[✓](https://github.com/Shwai-He/SparseUnifiedModel) ・ リポジトリ内被引用：0  
  統合マルチモーダルモデルの部品ごとの圧縮耐性を学習なし枝刈りで測り分け、弱い生成部品はニューロンをエキスパートへ分けて半分だけ活性化するMoE適応で、BAGELのGenEvalを無圧縮以上へ回復させる分析と適応法。

- **2025-12 · [Sliced ReLU attention: Quasi-linear contextual expressivity via sorting](2025-2512.11411-sliced-relu-attention-quasi-linear-contextual-expressivity-via-sorting.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クエリとキーの差の一次元射影へReLUを適用し、ソートと累積和で注意をO(n log n)で厳密計算する注意機構で、普遍近似の理論保証を保ちながらLRA平均正解率をソフトマックスの59.8パーセントから62.9パーセントへ上げる。

- **2025-12 · [Quantization Methods for Energy Efficient LLM Deployments](2025-b174259d82b3-quantization-methods-for-energy-efficient-llm-deployments.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3の6規模に6つの量子化方式を適用し精度保持率とエネルギーとスループットを実測した研究。原生対応のFP8とINT8が省エネと高速化で優れ、32BのFP8はFP16比で1トークンあたりエネルギーが半分以下になる一方、GPTQ 4ビットはエネルギーが基準超えになることを示す。

- **2025-12 · [Modality Inflation: Energy Characterization and Optimization Opportunities for MLLM Inference](2025-2512.22695-modality-inflation-energy-characterization-and-optimization-opportunitie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像入力を追加すると、視覚符号化器（vision encoder）が必要になるだけでなく、符号化結果が多数の視覚トークンとして言語モデルへ渡される。モデルはおおむね7B～8Bの言語モデル本体を持つが、視覚符号化器と画像のトークン化方式が異なる。代表的な条件では、画像入力によるエネルギー上乗せは17～94%の範囲だったと報告する。

- **2025-12 · [HyperVL: An Efficient and Dynamic Multimodal Large Language Model for Edge Devices](2025-2512.14052-hypervl-an-efficient-and-dynamic-multimodal-large-language-model-for-edg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚解像度圧縮器で入力ごとに縮小率を予測して視覚トークンを減らし、二重整合学習で大小二つの視覚エンコーダを一つの言語モデルへそろえて切替可能にした、端末向けマルチモーダルモデル。

### 2年前（2024-12〜2025-11）

- **2025-03 · [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](2025-2503.16419-stop-overthinking-a-survey-on-efficient-reasoning-for-large-language-mod.md)**  
  実装：[✓](https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs) ・ リポジトリ内被引用：55  
  本論文は、推論に特化した大規模言語モデルが長い思考連鎖（Chain-of-Thought; CoT）を生成することで正答率を高める一方、単純な質問にも冗長な検証や反復を行ってしまう「過剰思考」を減らす研究を整理したサーベイである。

- **2025-02 · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](2025-2502.05171-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-app.md)**  
  実装：[✓](https://github.com/seal-rg/recurrent-pretraining) ・ リポジトリ内被引用：44  
  この研究は、推論時の計算量を思考連鎖（chain-of-thought; CoT）の出力トークン数ではなく、モデル内部の反復深さで増やす。入力を処理するprelude、共有されるrecurrent core、出力を作るcodaにTransformerを分け、coreを推論時に何回でも反復する。

- **2025-05 · [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](2026-2505.09999-servegen-workload-characterization-and-generation-of-large-language-mode.md)**  
  実装：[✓](https://github.com/alibaba/ServeGen) ・ リポジトリ内被引用：38  
  4か月・12モデル・35.4億要求の本番記録から、到着率、バースト、入力・出力長、画像・音声・動画、推論過程の分布を分析する。顧客ごとの比較的安定した特性と時間変動する到着率を合成し、現実的な推論ベンチマークを作る。

- **2025-01 · [LLaVA-Mini: Efficient Image and Video Large Multimodal Models with One Vision Token](2025-2501.03895-llava-mini-efficient-image-and-video-large-multimodal-models-with-one-vi.md)**  
  実装：[✓](https://github.com/ictnlp/LLaVA-Mini) ・ リポジトリ内被引用：37  
  画像を1枚だけ扱う場合でも自己注意と中間活性の負荷が増え、動画ではフレーム数にほぼ比例して言語モデルの文脈が膨らむ。別の学習可能なクエリを使った圧縮器が、言語モデルへ渡す視覚トークンを最少1個にする。

- **2025-02 · [KernelBench: Can LLMs Write Efficient GPU Kernels?](2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/KernelBench) ・ リポジトリ内被引用：28  
  一般的なプログラム合成では単体試験に通ることを重視するが、GPUカーネルの実用性は入力形状、メモリ階層、並列実行、命令セットに左右される。正しくても遅い実装を成功とみなさないことが設計の中心にある。例えばDeepSeek-R1の fast1 は単一演算12%、複合演算36%、モデル全体2%である。

- **2025-04 · [Energy Considerations of Large Language Model Inference and Efficiency Optimizations](2025-2504.17674-energy-considerations-of-large-language-model-inference-and-efficiency-o.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  LLM推論の電力量を、入力長・出力長・バッチ数・GPU・推論基盤・復号方式・モデル並列の組合せで実測し、実トラフィックの入出力長分布を区間化して総消費量を推定する。適切なソフトウェア最適化で未最適化PyTorch比最大73%削減できる一方、投機的復号や複数GPUは条件によって逆に電力量を増やす。

- **2025-11 · [Latent Collaboration in Multi-Agent Systems](2025-2511.20639-latent-collaboration-in-multi-agent-systems.md)**  
  実装：[✓](https://github.com/Gen-Verse/LatentMAS) ・ リポジトリ内被引用：18  
  LatentMASはこの境界を変え、エージェントが最終層の隠れ状態を連続表現のまま自己回帰生成し、層ごとの鍵・値キャッシュ（KVキャッシュ）を共有作業メモリとして次のエージェントへ渡す。著者は既存モデルを追加学習しない訓練不要方式として設計し、入力埋め込みと最終層隠れ状態の分布の違いを補正する線形写像を組み込む。

- **2025-07 · [LIMINAL: Exploring The Frontiers of LLM Decode Performance](2025-2507.14397-liminal-exploring-the-frontiers-of-llm-decode-performance.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  LIMINALは、自己回帰デコードの上限を、モデル側の演算・重み・キー・バリュー（Key-Value; KV）キャッシュ需要と、加速器側の演算性能・メモリ容量・帯域・集合通信性能へ分解する解析性能モデルである。

- **2024-12 · [Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](2024-2412.15605-don-t-do-rag-when-cache-augmented-generation-is-all-you-need-for-knowled.md)**  
  実装：[✓](https://github.com/hhhuang/CAG) ・ リポジトリ内被引用：17  
  著者らはキャッシュ拡張生成（Cache-Augmented Generation、CAG）を提案する。Llama 3.1 8BをV100×8で評価した結果、SQuADとHotPotQAの多くの知識集合でCAGの回答品質は疎検索・密検索を用いるRAGと同等以上である。

- **2025-10 · [Growing a Twig to Accelerate Large Vision-Language Models](2025-2503.14075-growing-a-twig-to-accelerate-large-vision-language-models.md)**  
  実装：[✓](https://github.com/MILVLG/twigvlm) ・ リポジトリ内被引用：16  
  初期の視覚トークン枝刈り方式は、入力処理（プリフィル）の計算量を減らす一方、初期層の注意得点が質問内容を十分反映しないため、削除してはいけない視覚トークンを捨てやすい。ICCV 2025論文の主結果では、LLaVA-1.5-7Bの平均視覚トークンを576から64へ減らした設定（88.9%削減）で、6課題の平均相対性能96.0%を維持した。

- **2025-06 · [Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](2025-2506.09501-understanding-and-mitigating-numerical-sources-of-nondeterminism-in-llm-inference.md)**  
  実装：[✓](https://github.com/nanomaoli/llm_reproducibility) ・ リポジトリ内被引用：16  
  「温度0の貪欲復号なら同じモデルは同じ答えを返す」という前提が、GPU数・GPU種類・バッチサイズによる浮動小数点演算順序の変化だけでも崩れることを系統的に示し、重みの保存精度と計算精度を分離するLayerCastで再現性を改善する研究。

- **2025-07 · [ShortGPT: Layers in Large Language Models are More Redundant Than You Expect](2025-bdec19301b9e-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-exp.md)**  
  実装：[✓](https://github.com/icip-cas/ShortGPT) ・ リポジトリ内被引用：8  
  層の入出力の類似度から重要度を測る指標BIで冗長な層を見つけ、層を丸ごと削除するShortGPTと、生成トークンだけ全層を通すShortGPT-genで、約25%の層を削っても多肢選択で約9割、生成で97%の性能を保つ枝刈り手法。

- **2025-07 · [Collaborative Inference and Learning between Edge SLMs and Cloud LLMs: A Survey of Algorithms, Execution, and Open Challenges](2025-2507.16731-collaborative-inference-and-learning-between-edge-slms-and-cloud-llms-a-.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  端末で簡単な要求を処理し、必要な時だけクラウドを呼ぶ方式は自然だが、呼出し回数が増えれば往復遅延が支配的になる。

- **2025-11 · [From Prompts to Power: Measuring the Energy Footprint of LLM Inference](2025-2511.05597-from-prompts-to-power-measuring-the-energy-footprint-of-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本サーベイとの接点は、LLM推論サービング（serving）の省エネルギー化、モデル・GPUの配置選択、バッチ処理、KVキャッシュ容量、量子化・実行方式の設計判断である。

- **2025-10 · [Not All Bits Are Equal: Scale-Dependent Memory Optimization Strategies for Reasoning Models](2025-2510.10964-not-all-bits-are-equal-scale-dependent-memory-optimization-strategies-fo.md)**  
  実装：[✓](https://github.com/krafton-ai/not-all-bits-are-equal) ・ リポジトリ内被引用：4  
  長い思考列を出力する推論モデルでは、量子化してモデル重みを小さくすれば常に省メモリで高性能になる、という通常の指針が成立しない。原著のQwen3-4Bでは、4bit重みが2.49 GBであるのに対し、32kトークン相当のKVキャッシュは4.42 GBと約1.8倍に達する（原著§1）。

- **2025-09 · [MCBP: A Memory-Compute Efficient LLM Inference Accelerator Leveraging Bit-Slice-enabled Sparsity and Repetitiveness](2025-2509.10372-mcbp-a-memory-compute-efficient-llm-inference-accelerator-leveraging-bit.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みをビットの層へ分解して見える重複と疎さを3つの滞留へ効かせる専用加速器で、A100比9.43倍の高速化と31.1倍のエネルギー効率をシミュレーション評価で示した。

- **2025-06 · [Towards Efficient Multi-LLM Inference: Characterization and Analysis of LLM Routing and Hierarchical Techniques](2025-2506.06579-towards-efficient-multi-llm-inference-characterization-and-analysis-of-l.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  このサーベイは、複数の独立した大規模言語モデル（LLM）を一つのサービスで使い分ける際、どの要求をどのモデルへ送り、どの条件で上位モデルへ再実行するかを推論システムの最適化問題として整理する。本文中の最大98%費用削減などの値は引用した個別研究の結果であり、このサーベイの独立した再現実験ではない。

- **2025-01 · [Resource-efficient Algorithms and Systems of Foundation Models: A Survey](2025-f103beecee83-resource-efficient-algorithms-and-systems-of-foundation-models-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  Xu・Cai・Yin・Wang・Jin・Liuによる39ページの査読付きサーベイは、基盤モデルの「効率」を単一のモデル圧縮率やGPU演算速度として扱わず、モデル構造、学習・圧縮・推論アルゴリズム、実行システムという異なる介入点に分解する。

- **2025-11 · [Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications](2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  公平な2-GPU基準と複数KV転送階層・DVFSでプリフィル/デコード分離を再評価し、性能・省電力の優位が条件依存であることを示す。

- **2025-09 · [Training Matryoshka Mixture-of-Experts for Elastic Inference-Time Expert Utilization](2025-2509.26520-training-matryoshka-mixture-of-experts-for-elastic-inference-time-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  1T トークンをk=1で事前学習したcheckpointから、各方式でさらに80B トークンを継続学習する。

- **2025-11 · [OckBench: Measuring the Efficiency of LLM Reasoning](2025-2511.05722-ockbench-measuring-the-efficiency-of-llm-reasoning.md)**  
  実装：[✓](https://github.com/OckBench/OckBench) ・ リポジトリ内被引用：2  
  従来の正答率だけではこの差が見えず、ハードウェアの処理量だけではモデル自身がどれほど冗長に推論するかを分離できない。

- **2024-12 · [A Survey of RWKV](2024-2412.14847-a-survey-of-rwkv.md)**  
  実装：[✓](https://github.com/MLGroupJLU/RWKV-Survey) ・ リポジトリ内被引用：2  
  RWKVは、過去の情報を固定形状の再帰状態へ畳み込むことで、生成時に全トークンのKVを保持しない設計を取る。

- **2025-11 · [TimeViper: A Hybrid Mamba-Transformer Vision-Language Model for Efficient Long Video Understanding](2025-2511.16595-timeviper-a-hybrid-mamba-transformer-vision-language-model-for-efficient.md)**  
  実装：[✓](https://github.com/xiaomi-research/timeviper) ・ リポジトリ内被引用：1  
  1時間の動画を毎秒1枚、1フレーム768トークンで表現すると約276万トークンになり、通常の全注意では処理費用とメモリが大きい。TimeViperは、状態空間モデル（State Space モデル; SSM）のMamba-2とTransformerの注意層を混ぜた基盤を使い、さらに言語モデルの途中で視覚トークンを圧縮する。

- **2025-11 · [MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning](2025-2511.02805-memsearcher-training-llms-to-reason-search-and-manage-memory-via-end-to-.md)**  
  実装：[✓](https://github.com/icip-cas/MemSearcher) ・ リポジトリ内被引用：1  
  検索エージェント（search agent）が外部検索を何度も行うと、思考、検索クエリ、検索結果を全て会話履歴に追記する従来のReAct方式では、ターンが増えるにつれて入力文脈が長くなる。検索エージェントの入力文脈はほぼ一定長で、論文の評価条件では4,000トークン未満を維持する。

- **2025-09 · [Motivating Next-Gen Accelerators with Flexible N:M Activation Sparsity via Benchmarking Lightweight Post-Training Sparsification Approaches](2025-2509.22166-motivating-next-gen-accelerators-with-flexible-n-m-activation-sparsity-v.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  半構造化N:M疎性は、各M要素のうちN要素を残す制約を設ける。2:4、4:8、8:16、16:32はいずれも50%の要素をゼロ化するが、ブロックが大きいほど、どの要素を残すかの組合せが増える。したがって本研究は「半構造化活性疎性が現時点で実用上安全」と結論するより、将来ハードウェアの設計選択を促す精度とコストの基礎ベンチマークとして読むべきである。

- **2025-05 · [ResDecode: Accelerating Large Language Models Inference via Residual Decoding Heads](2025-098116cbc05e-resdecode-accelerating-large-language-models-inference-via-residual-deco.md)**  
  実装：[✓](https://github.com/ZeroNLP/ResDecode) ・ リポジトリ内被引用：1  
  投機的復号では軽いドラフト側が複数の未来トークンを先読みし、対象の大きな言語モデルが候補をまとめて検証する。対象モデルの検証を通った候補だけを採用するため、単にドラフトを高速化するだけでなく、候補の採択長と検証費用の均衡が重要になる。

- **2025-05 · [Quantitative Analysis of Performance Drop in DeepSeek Model Quantization](2025-2505.02390-quantitative-analysis-of-performance-drop-in-deepseek-model-quantization.md)**  
  実装：[✓](https://github.com/UnicomAI/DeepSeek-Eval) ・ リポジトリ内被引用：1  
  671BのDeepSeek-R1/V3を含む系列全体で2から8ビット量子化の性能低下を実測し、重要モジュールへ高精度を配る動的3ビット量子化DQ3KMが4ビット級の精度を281GBで達成することを示した評価報告。

- **2025-04 · [LLMPi: Optimizing LLMs for High-Throughput on Raspberry Pi](2025-2504.02118-llmpi-optimizing-llms-for-high-throughput-on-raspberry-pi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ラズベリーパイ五の実機で、二ビットから八ビットの学習後量子化と三値の学習済みモデルを速度・電力効率・意味品質で比べ、最小モデルは二ビットで三・八八倍速く四・三倍効率化する一方、八十億級は七十一倍速くなっても対話の下限に届かず、二ビットでは意味品質が急落することを示した。

- **2025-02 · [Binary Neural Networks for Large Language Model: A Survey](2025-2502.19008-binary-neural-networks-for-large-language-model-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  中心となるのは、BitNet、BitNet b1.58、BitNet a4.8、FBI-LLM、Bi-Mambaなど、重みの二値化・三値化を学習時から組み込む方式である。

- **2025-11 · [Iris: First-Class Multi-GPU Programming Experience in Triton](2025-2511.12500-iris-first-class-multi-gpu-programming-experience-in-triton.md)**  
  実装：[✓](https://github.com/ROCm/iris) ・ リポジトリ内被引用：0  
  対称メモリをTritonのタイル抽象へ持ち込み、計算と通信をタイル単位で重ねる融合カーネルを純粋なPythonとTritonで書ける複数GPU通信ライブラリ。集合通信比で平均1.21倍の高速化。

- **2025-11 · [Firewall Routing: Blocking Leads to Better Hybrid Inference for LLMs](2025-73146b754a26-firewall-routing-blocking-leads-to-better-hybrid-inference-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両モデルを複数回サンプリングして勝率をソフトなラベル化し、強いモデルでも解けないロングテールクエリを弱いモデル側へ遮断するルーター学習。APGRで最大5.29ポイント改善。

- **2025-11 · [CoEdge-RAG: Optimizing Hierarchical Scheduling for Retrieval-Augmented LLMs in Collaborative Edge Computing](2025-2511.05915-coedge-rag-optimizing-hierarchical-scheduling-for-retrieval-augmented-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散した私的コーパスを持つエッジノード群について、方策学習でクエリのドメインを推定し、ノード間とノード内の二層で負荷とメモリを配分することで、遅延制約の下で検索拡張生成の品質を上げる階層スケジューリング。

- **2025-11 · [Analyzing and Modeling LLM Response Lengths with Extreme Value Theory: Anchoring Effects and Hybrid Distributions](2025-a08ef62fbe5d-analyzing-and-modeling-llm-response-lengths-with-extreme-value-theory-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとの出力長がばらつくと、短い応答と非常に長い応答が混在し、GPUの連続バッチングやスケジューラの資源配分が難しくなる。

- **2025-10 · [Sparse Query Attention (SQA): A Computationally Efficient Attention Mechanism with Query Heads Reduction](2025-2510.01817-sparse-query-attention-sqa-a-computationally-efficient-attention-mechani.md)**  
  実装：[✓](https://github.com/RxAI-dev/rxnn-Attention) ・ リポジトリ内被引用：0  
  キー・バリューではなくクエリヘッドを減らすことで注意スコア計算の演算量そのものをHq/H倍へ削り、計算律速な学習・長文処理で最大約3.4倍の高速化を示した注意アーキテクチャ。

- **2025-10 · [RECON: Reasoning with Condensation for Efficient Retrieval-Augmented Generation](2025-2510.10448-recon-reasoning-with-condensation-for-efficient-retrieval-augmented-gene.md)**  
  実装：[✓](https://github.com/allfornancy/RECON) ・ リポジトリ内被引用：0  
  RL型RAGの推論ループ内に、関連性事前学習と多観点蒸留で訓練した専用要約器を挟み、文脈長を35%・推論時間を30.9%削減しながらQA精度も上げた文脈圧縮の枠組み。

- **2025-10 · [RCPU: Rotation-Constrained Error Compensation for Structured Pruning of a Large Language Model](2025-2510.07782-rcpu-rotation-constrained-error-compensation-for-structured-pruning-of-a.md)**  
  実装：[✓](https://github.com/harutaro/rcpu) ・ リポジトリ内被引用：0  
  構造化枝刈りの出力誤差を、ノルムと内積を保つ回転だけの閉形式更新で補正し、入力分散を掛けた列スコアで主方向の列を残す RCPU を提案し、Llama系で枝刈り率30パーセントまで Wanda-sp と FLAP をパープレキシティと平均精度で上回った研究。

- **2025-10 · [LLM Routing with Dueling Feedback](2025-2510.00841-llm-routing-with-dueling-feedback.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ルーティングを文脈付き決闘バンディットとして定式化し、カテゴリ校正ファインチューニングで作ったモデル埋め込みとFeel-Good Thompson Samplingを組み合わせ、pairwise選好だけから性能とコストを両立するモデル選択をオンライン学習する方式。

- **2025-10 · [Higher-order Linear Attention](2025-2510.27258-higher-order-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Higher-order Linear 注意機構（HLA）は、より高次の相互作用を、低次のモーメントと補正統計の組合せへ因数分解する。

- **2025-10 · [Finish First, Perfect Later: Test-Time Token-Level Cross-Validation for Diffusion Large Language Models](2025-2510.05090-finish-first-perfect-later-test-time-token-level-cross-validation-for-di.md)**  
  実装：[✓](https://github.com/Rachum-thu/tolerator) ・ リポジトリ内被引用：0  
  拡散言語モデルの確定済みトークンを直せない問題に対し、まず全体を埋めてから部分集合を再マスクして予測し直す相互検証リファインメントを後段に置く、学習不要の2段階デコードToleratorを提案し、同一計算予算で2モデル・5ベンチマークの品質改善を示した研究。

- **2025-10 · [CARES: Context-Aware Resolution Selector for VLMs](2025-2510.19496-cares-context-aware-resolution-selector-for-vlms.md)**  
  実装：[✓](https://github.com/mkimhi/CARES) ・ リポジトリ内被引用：0  
  小型の代理モデルで画像と質問を見て必要最小限の入力解像度を予測し、対象の視覚言語モデルを無改造のまま前段で振り分けるCARESにより、9ベンチマークで精度をほぼ保ちながらプリフィル計算を最大で平均78パーセント削減した解像度選択の研究。

- **2025-09 · [PLaMo 2 Technical Report](2025-2509.04897-plamo-2-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PLaMo 2 Technical Reportは、Preferred Networksが開発した日本語向け大規模言語モデル系列のアーキテクチャ、学習・蒸留、長文脈対応、推論実装と量子化をまとめた技術報告である。推論側では、31BモデルのBF16重みが約63GB、KVキャッシュが約110KB/トークンであり、32K文脈だけで約3.6GBのKVを使う。

- **2025-09 · [HIVTP: A Training-Free Method to Improve VLMs Efficiency via Hierarchical Visual Token Pruning Using Middle-Layer-Based Importance Score](2025-2509.23663-hivtp-a-training-free-method-to-improve-vlms-efficiency-via-hierarchical.md)**  
  実装：[✓](https://github.com/Blacktower27/HIVTP) ・ リポジトリ内被引用：0  
  視覚エンコーダ中間層の注意で視覚トークンの重要度を測り、領域単位の大域保持と窓単位の局所保持の二段で間引く学習不要の枝刈りで、LLaVA系の初回トークン時間を最大で約半分にしスループットを最大6割上げる。

- **2025-09 · [Efficient Fine-Grained GPU Performance Modeling for Distributed Deep Learning of LLM](2025-2509.22832-efficient-fine-grained-gpu-performance-modeling-for-distributed-deep-lea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、こうした複雑さをブラックボックスの「モデルサイズから学習時間を推定する式」だけで扱うのではなく、演算・通信プリミティブの実測回帰器と、実行依存関係を反映した時間軸モデルを組み合わせることで、実際の学習反復時間を予測する手法を提案する。

- **2025-09 · [Certainty-Guided Reasoning in Large Language Models: A Dynamic Thinking Budget Approach](2025-2509.07820-certainty-guided-reasoning-in-large-language-models-a-dynamic-thinking-b.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考途中で最終回答を試行生成し、回答トークン確率の最小値が閾値を超えたら早期終了する確実性誘導推論で、固定予算の正解率をほぼ保ちながら思考トークンを削減する方式。

- **2025-09 · [Accelerating RAG Systems: A Performance-Oriented Systematic Mapping](2025-d9e213765995-accelerating-rag-systems-a-performance-oriented-systematic-mapping.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAG高速化研究147件を性能志向のシステマティックマッピングで34件へ絞って分類し、焦点が検索精度からプリフィックス対応KV再利用やGPU加速などのサービング効率へ移る一方、評価指標の不統一と多言語対応の不足が残ることを示したサーベイ。

- **2025-08 · [TPLA: Tensor Parallel Latent Attention for Efficient Disaggregated Prefill and Decode Inference](2025-2508.15881-tpla-tensor-parallel-latent-attention-for-efficient-disaggregated-prefil.md)**  
  実装：[✓](https://github.com/fxmeng/TransMLA) ・ リポジトリ内被引用：0  
  TPLA（テンソル-Parallel Latent 注意機構）は、DeepSeek系列などで使われるMulti-Head Latent 注意機構（MLA）のKVキャッシュをGPUごとに複製する問題を解消するテンソル parallel（TP）方式である。

- **2025-08 · [Meta-Metrics and Best Practices for System-Level Inference Performance Benchmarking](2025-2508.10251-meta-metrics-and-best-practices-for-system-level-inference-performance-b.md)**  
  実装：[✓](https://github.com/IBM/fmwork) ・ リポジトリ内被引用：0  
  入力トークン長、出力トークン長、同時実行数、重み精度、テンソル並列数、推論エンジン、スケジューラ設定を変えると、初回トークン遅延（TTFT）、トークン間遅延（ITL）、総スループット（THP）は異なる。

- **2025-08 · [MagicVL-2B: Empowering Vision-Language Models on Mobile Devices with Lightweight Visual Encoders via Curriculum Learning](2025-2508.01540-magicvl-2b-empowering-vision-language-models-on-mobile-devices-with-ligh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  93Mの軽量視覚エンコーダとトークン単位の動的解像度でスマホ上の視覚処理を軽くし、複雑さで段階化したカリキュラム学習で精度を補う、モバイル向け視覚言語モデルの設計と実機評価。

- **2025-08 · [DRQA: Dynamic Reasoning Quota Allocation for Controlling Overthinking in Reasoning Large Language Models](2025-2508.17803-drqa-dynamic-reasoning-quota-allocation-for-controlling-overthinking-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  バッチ推論で生じる資源競合による推論圧縮を、A/B/C判定の選好データとGRPOで単一質問推論へ移植し、正解率を上げながらトークンを約31%削減した過剰思考の制御手法。

- **2025-07 · [Characterizing State Space Model and Hybrid Language Model Performance with Long Context](2025-2507.12442-characterizing-state-space-model-and-hybrid-language-model-performance-w.md)**  
  実装：[✓](https://github.com/sapmitra/ssm-scope) ・ リポジトリ内被引用：0  
  近年はSSMと注意機構を組み合わせたHybridモデルも登場した。本論文は、RTX 4090（24GB）とJetson Orin Nano（8GB共有メモリ）を対象に、Transformer・SSM・Hybridの文脈長による性能逆転、メモリ上限、消費エネルギー、演算子別のボトルネックを計測したシステム特性評価である。

- **2025-05 · [Towards Efficient Key-Value Cache Management for Prefix Prefilling in LLM Inference](2025-2505.21919-towards-efficient-key-value-cache-management-for-prefix-prefilling-in-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実運用トレースでKVキャッシュの再利用率と逐次・ランダムの混合アクセスを実証し、RedisとRDMA系キーバリューストアのメタデータ性能を実トレースで測って、接頭辞プリフィル専用のメタデータ管理が要ることを示した分析研究。

- **2025-05 · [Resource-Efficient Language Models: Quantization for Fast and Accessible Inference](2025-2505.08620-resource-efficient-language-models-quantization-for-fast-and-accessible-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルを一般利用者の限られた計算資源で動かすための後学習量子化を解説する文献レビューである。

- **2025-05 · [LightRouter: Towards Efficient LLM Collaboration with Minimal Overhead](2025-2505.16221-lightrouter-towards-efficient-llm-collaboration-with-minimal-overhead.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全候補へ短いブートトークンだけを生成させて見込みを判定し、有望なモデルだけに続きを生成させて統合する適応型ルーティングLightRouterを提案し、集成方式より低い推論コストで高い精度を示した研究。

- **2025-04 · [Efficient LLaMA-3.2-Vision by Trimming Cross-attended Visual Features](2025-2504.00557-efficient-llama-3-2-vision-by-trimming-cross-attended-visual-features.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  交差注意の重みが一部の画像特徴へ偏り層間でも変わらない観測に基づき、最初の層で注意頭ごとの上位特徴の和集合だけを残して残り層のキャッシュと計算を減らす追加学習なしの方式で、特徴を約半分にしても性能同等を保ちバッチ三二の遅延を二六パーセント減らした。

- **2025-03 · [Dynamic Pyramid Network for Efficient Multimodal Large Language Models](2025-2503.20322-dynamic-pyramid-network-for-efficient-multimodal-large-language-models.md)**  
  実装：[✓](https://github.com/aihao2000/DPN-LLaVA) ・ リポジトリ内被引用：0  
  視覚トークンの圧縮を言語モデルの外から内側の階層構造へ移し、深さとともに段階的に圧縮しながら、サンプルごとにプーリング率を動的に選ぶことで、LLaVAの演算量を最大56%削りつつ性能を保つマルチモーダル推論の高速化。

- **2025-02 · [Task-agnostic Prompt Compression with Context-aware Sentence Embedding and Reward-guided Task Descriptor](2025-2502.13374-task-agnostic-prompt-compression-with-context-aware-sentence-embedding-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問や手作りテンプレートなしで長いプロンプトを文単位に圧縮するため、プロンプトからタスク記述を生成するモデルを応答分布の近さを報酬に磨き、その記述と各文の文脈対応埋め込みの類似度で文を選ぶ方式で、質問なし設定でも従来方式を大きく上回る。

- **2025-02 · [Leveraging the true depth of LLMs](2025-2502.02790-leveraging-the-true-depth-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連続する2層を同じ入力から並列に計算させてテンソル並列の同期回数を半減させるレイヤー並列化を提案し、再学習なしでLlama 2 7Bのスループットを1.19倍にしつつ、精度低下とファインチューニングによる回復の範囲を実測した研究。

- **2025-02 · [KVCrush: Key value cache size-reduction using similarity in head-behaviour](2025-2503.00022-kvcrush-key-value-cache-size-reduction-using-similarity-in-head-behaviou.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVCrushは、長文脈のLLM推論でKVキャッシュを縮小する際に、重要度の高いトークンだけを残す既存方式の弱点を補う手法である。平均KV削減率約4倍の条件でも精度低下を小さく抑えられる一方、すべての個別課題でFullKVに勝つわけではない。

- **2024-12 · [Pruning All-Rounder: Rethinking and Improving Inference Efficiency for Large Vision Language Models](2024-2412.06458-pruning-all-rounder-rethinking-and-improving-inference-efficiency-for-la.md)**  
  実装：[✓](https://github.com/ASGO-MM/Pruning-All-Rounder) ・ リポジトリ内被引用：0  
  層の冗長性とトークンの冗長性が連動する実証に基づき、軽量メタ・ルーターが落とす視覚トークンと飛ばす層を入力適応に決め、本体を再学習せず計算量をほぼ半減する視覚言語モデルの枝刈り方式。

### 3年前（2023-12〜2024-11）

- **2024-01 · [BurstGPT: A Real-world Workload Dataset to Optimize LLM Serving Systems](2024-2401.17644-burstgpt-real-world-llm-serving-workload-dataset.md)**  
  実装：[✓](https://github.com/HPMLL/BurstGPT) ・ リポジトリ内被引用：87  
  Azure OpenAI GPTサービスの1031万件・213日分の実トレースと再生基盤BurstGPT-Perfを公開し、平均RPSだけを揃えた合成負荷では見えないバースト、会話間隔、応答長、失敗がサービング評価の結論を変えることを示す。

- **2024-03 · [The Unreasonable Ineffectiveness of the Deeper Layers](2024-2403.17887-the-unreasonable-ineffectiveness-of-the-deeper-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：64  
  削除したい層数を決め、入力・出力間の角距離が最小の連続ブロックを選択し、実際に層を除去する。Llama-2系列の5-shot MMLUでは削除率45〜55%付近で急落するが、Qwen系列では約20%付近で急落する。

- **2024-04 · [Characterizing Power Management Opportunities for LLMs in the Cloud](2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md)**  
  実装：✓ ・ リポジトリ内被引用：36  
  この観測を使い、優先度別の二段階電力制御を行うPOLCAを提案する。著者らは本番トレースから生成した合成負荷を用いた離散事象シミュレーションで、既存の電力予算のままサーバーを30%多く配置しても、設定した遅延SLOを満たし、通常条件で電力ブレーキを起こさない結果を示した。

- **2024-02 · [A Comprehensive Evaluation of Quantization Strategies for Large Language Models](2024-2402.16775-a-comprehensive-evaluation-of-quantization-strategies-for-large-language.md)**  
  実装：[✓](https://github.com/cordercorder/quant_eval) ・ リポジトリ内被引用：24  
  本論文は、新しい量子化器を提案するものではなく、既存の量子化方式をモデル能力、指示追従・整合性、推論効率という異なる観点で測り直す比較実験である。論文のSpQR実装は低ビットの値域を模擬しながら高精度形式で重みを保持しており、品質の比較には使えても実メモリ削減を実証しない。

- **2024-01 · [Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning](2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reas.md)**  
  実装：[✓](https://github.com/Yiwei98/ESC) ・ リポジトリ内被引用：24  
  多段階推論では、単一の思考連鎖（Chain-of-Thought、CoT）だけで回答すると、途中の偶然の誤りがそのまま最終回答に伝わる。自己整合性（自己整合性、SC）は同一問題から複数の思考連鎖を独立に標本化し、最終回答を多数決してこの変動を抑える。しかしSCは難しい問題にも簡単な問題にも、事前に決めた最大標本数を一律に使う。

- **2024-11 · [Lynx: Enabling Efficient MoE Inference through Dynamic Batch-Aware Expert Selection](2024-2411.08982-lynx-enabling-efficient-moe-inference-through-dynamic-batch-aware-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  演算の疎性が、専門家重みを高帯域メモリから読み出す量の削減につながらなくなる。Lynxはこの矛盾を、モデルの重みを恒久的に枝刈りするのでなく、現在のバッチのルーター出力を再配置することで緩和する。通常の同居配置で出力トークン間隔の中央値を1.09～1.30倍短縮し、精度変化を概ね1ポイント以内に抑える。

- **2024-02 · [Benchmarking and Dissecting the Nvidia Hopper GPU Architecture](2024-2402.13499-benchmarking-and-dissecting-the-nvidia-hopper-gpu-architecture.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  Hopper世代のGPUは第4世代テンソル Core、8ビット浮動小数点（FP8）、ワープグループ行列積（wgmma）、動的計画法命令（DPX）、テンソルメモリアクセラレータ（TMA）、分散共有メモリ（DSM）を備える。しかし仕様表のピーク演算量や帯域だけでは、行列形状、オペランド配置、電力、精度変換、カーネル起動の費用を含む実性能は分からない。

- **2024-06 · [Measuring and Improving the Energy Efficiency of Large Language Models Inference](2024-f40d5b5275ad-measuring-and-improving-the-energy-efficiency-of-large-language-models-i.md)**  
  実装：[✓](https://github.com/maufadel/EnergyMeter) ・ リポジトリ内被引用：10  
  著者らは推論をモデルパラメータ数だけで比較する慣習にも疑問を投げかけ、層の深さ、注意・フィードフォワードの並列化、バッチ数、量子化形式の実行実装を分けて検証した。

- **2024-04 · [Toward Inference-optimal Mixture-of-Expert Large Language Models](2024-2404.02852-toward-inference-optimal-mixture-of-expert-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoEのスケーリング則へ推論費用を組み込み、専門家数を増やした「損失最適」構成より、小さなMoEを多くのデータで学習する構成が配信費用まで含めて有利になる領域を示す。

- **2024-06 · [Divergent Token Metrics: Measuring degradation to prune away LLM components -- and optimize quantization](2024-2311.01544-divergent-token-metrics-measuring-degradation-to-prune-away-llm-componen.md)**  
  実装：[✓](https://github.com/Aleph-Alpha/Divergent_Tokens) ・ リポジトリ内被引用：3  
  大規模言語モデルの圧縮では、重みを0にする枝刈りや、浮動小数点数を整数へ変換する量子化が、生成文をどの時点から変えてしまうかを把握する必要がある。この指標を使って行列ごとの枝刈り率を配分すると、Llama-2-13Bを全体75%疎化したとき、同じ平均疎化率の一様な大きさ基準の枝刈りより、WikiText2のPPLを13.512から8.101へ抑えられる。

- **2024-10 · [LLMCBench: Benchmarking Large Language Model Compression for Efficient Deployment](2024-2410.21352-llmcbench-benchmarking-large-language-model-compression-for-efficient-de.md)**  
  実装：[✓](https://github.com/AboveParadise/LLMCBench) ・ リポジトリ内被引用：1  
  圧縮性能から信頼性までの6軸で疎化と量子化の代表7手法を統一測定し、量子化が性能保持で優れること、重みのみ量子化が汎化で安定すること、疎化は学習が軽いが配布基盤の対応が未熟なことを明らかにした。

- **2024-09 · [AVG-LLaVA: An Efficient Large Multimodal Model with Adaptive Visual Granularity](2024-2410.02745-avg-llava-an-efficient-large-multimodal-model-with-adaptive-visual-granu.md)**  
  実装：[✓](https://github.com/DeepLearnXMU/AVG-LLaVA) ・ リポジトリ内被引用：1  
  画像と指示に応じて視覚トークンの粒度を5段階から選ぶルータを、言語モデル自身の回答の対数確率を教師にするRGLFで学習し、AI2Dで視覚トークン85.3パーセント削減と2.53倍の高速化を性能向上と両立させる。

- **2024-09 · [Art and Science of Quantizing Large-Scale Models: A Comprehensive Overview](2024-2409.11650-art-and-science-of-quantizing-large-scale-models-a-comprehensive-overvie.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、大規模モデルの量子化（量子化）を、重みと活性値の数値表現、学習後量子化（post-学習 量子化; PTQ）、量子化認識学習（量子化-aware 学習; QAT）、知識蒸留（knowledge distillation）、鍵・値キャッシュ（key-value キャッシュ; KV キャッシュ）の圧縮という複数の切り口から整理した概説論文である。

- **2024-11 · [PPLLaVA: Varied Video Sequence Understanding With Prompt Guidance](2024-2411.02327-ppllava-varied-video-sequence-understanding-with-prompt-guidance.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  指示文と各視覚トークンの関連度を重みに使う三次元畳み込み型プーリングで動画トークンを十八倍まで圧縮し、大規模動画ベンチマークで元モデルを上回る正解率と約三分の一の処理時間を両立した。テキスト符号器の文脈拡張が長い指示への対応を担う。

- **2024-11 · [Efficient Multi-modal Large Language Models via Visual Token Grouping](2024-2411.17773-efficient-multi-modal-large-language-models-via-visual-token-grouping.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事前学習済みViTの中で意味トークンへ画像領域を集約させ、Gumbel-Softmaxの割り当てで視覚トークンを意味グループごとに統合し、LLaVA-1.5の視覚トークンを576から128へ減らして性能維持率97.5パーセントと推論時間27パーセント超削減を両立する手法。

- **2024-10 · [LLMProxy: Reducing Cost to Access Large Language Models](2024-2410.11857-llmproxy-reducing-cost-to-access-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル選択・文脈管理・意味キャッシュの3つのLLMコスト最適化を、双方向APIを持つプロキシLLMProxyへ集約する設計を提案し、WhatsApp実サービス運用と評価で文脈コスト30〜50%減などを示した研究。

- **2024-09 · [EchoAtt: Attend, Copy, then Adjust for More Efficient Large Language Models](2024-2409.14595-echoatt-attend-copy-then-adjust-for-more-efficient-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  内側の層同士で注意行列が似るという観測に基づき、似た層の注意計算を共有する生徒モデルを知識蒸留と継続学習で作り、パラメータ削減と推論・学習の高速化を品質維持と両立させた研究。

- **2024-09 · [Archon: An Architecture Search Framework for Inference-Time Techniques](2024-2409.15254-archon-an-architecture-search-framework-for-inference-time-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成・融合・順位付け・批判・検証などの推論時技法の部品とモデルの組み合わせをベイズ最適化で自動探索し、課題と計算予算に合わせた推論アーキテクチャを組むことで、フロンティアモデルを平均15.1パーセント上回りながら推論呼び出しを20パーセント減らした構成探索フレームワーク。

- **2024-04 · [Softmax Attention with Constant Cost per Token](2024-2404.05843-softmax-attention-with-constant-cost-per-token.md)**  
  実装：[✓](https://github.com/glassroom/heinsen_attention) ・ リポジトリ内被引用：0  
  クエリとキーの類似度を指数の内積の対数へ変えて注意を線形化し、固定サイズの隠れ状態の更新だけでトークンあたり定数費用の注意を実現する方式。

### 4年前（2022-12〜2023-11）

- **2023-10 · [From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference](2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  対象は初代LLaMAの7B、13B、65Bで、NVIDIA V100とA100、自然言語指示のAlpaca、算術問題のGSM8Kを用いる。この研究は新しい注意演算や復号アルゴリズムを提案するものではない。

- **2023-10 · [Compressing LLMs: The Truth is Rarely Pure and Never Simple](2023-2310.01382-compressing-llms-the-truth-is-rarely-pure-and-never-simple.md)**  
  実装：[✓](https://github.com/VITA-Group/llm-kick) ・ リポジトリ内被引用：26  
  困惑度（perplexity）がほぼ維持されても、圧縮モデルの事実知識や指示追従は失われ得る。知識をモデル内部から答える課題と、外部文脈を与える検索・要約を分けて評価することで、枝刈りと量子化の能力別の弱点を可視化する。

- **2023-09 · [Large Language Model Routing with Benchmark Datasets](2023-2309.15789-large-language-model-routing-with-benchmark-datasets.md)**  
  実装：[✓](https://github.com/UMich-FATML/llm-routing) ・ リポジトリ内被引用：24  
  しかし実際のサービスでは、数学問題、法務文書、要約、常識質問など、タスクごとに得意なモデルが異なる。常に最も大きいモデルを呼ぶ方式は品質を得やすい反面、必要以上の推論計算を消費する。これらは品質と必要なモデル呼出し回数の評価であり、実際のGPU実行時間・請求金額の削減倍率を測定したものではない（原著§5、表1・2）。

- **2023-05 · [A Quantitative Review on Language Model Efficiency Research](2023-2306.01768-a-quantitative-review-on-language-model-efficiency-research.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、新しい高速化アルゴリズムや推論カーネルを提案する研究ではなく、既存の効率的言語モデル研究が公開した評価表を出典とともに集め直し、論文間で比較できる範囲と比較できない範囲を調べるメタ分析である。

### 5年前（2021-12〜2022-11）

- **2022-02 · [A Survey on Model Compression and Acceleration for Pretrained Language Models](2022-2202.07105-a-survey-on-model-compression-and-acceleration-for-pretrained-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  著者らは推論段階を対象に、重み共有、低ランク分解、枝刈り、量子化、知識蒸留、早期終了、トークン省略の七系統を比較する。

- **2022-08 · [Momentum Transformer: Closing the Performance Gap Between Self-attention and Its Linearization](2022-2208.00579-momentum-transformer-closing-the-performance-gap-between-self-attention-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モーメンタム Transformerは、通常のソフトマックス注意を線形化した際に失われる表現力を、最適化アルゴリズムのモーメンタムに着想を得た状態更新で補おうとする研究である。だが、LRAの平均正答率は標準ソフトマックスの58.70%を下回る56.04%であり、翻訳の生成速度も標準ソフトマックスの方が大きい。

### 6年前（2020-12〜2021-11）

- **2021-10 · [Efficiently Modeling Long Sequences with Structured State Spaces](2021-2111.00396-efficiently-modeling-long-sequences-with-structured-state-spaces.md)**  
  実装：[✓](https://github.com/HazyResearch/state-spaces) ・ リポジトリ内被引用：141  
  自己注意（self-注意機構）は系列長Lに対して二次の注意行列を作るため、1万〜数万ステップの系列では計算・メモリ負荷が大きくなる。論文はLong Range Arena（LRA）の全課題で当時の最良水準を更新し、長さ16,384のPath-Xで88%正解率を達成した。

- **2021-11 · [You Only Sample (Almost) Once: Linear Cost Self-Attention Via Bernoulli Sampling](2021-2111.09714-you-only-sample-almost-once-linear-cost-self-attention-via-bernoulli-sam.md)**  
  実装：[✓](https://github.com/mlpen/YOSO) ・ リポジトリ内被引用：1  
  ソフトマックス注意を、局所性鋭敏ハッシュの衝突によるベルヌーイサンプリングへ置き換え、系列長に比例する費用で長系列を学習できる注意機構YOSOを提案する。
<!-- survey:auto:end -->
