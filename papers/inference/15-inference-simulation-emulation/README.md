# Inference Simulation / Emulation

LLM推論・サービング基盤を実GPU実行の代わりに離散事象、仮想時間、プロファイル標本化、カーネル性能モデルなどで再現し、構成探索や性能評価を高速化する研究をまとめる。

## 分類境界

主要貢献がLLM推論の性能・資源挙動を実機の代替として予測・模擬するsimulator、emulator、time-warp、profile-driven modelである研究を含め、実測benchmarkだけの研究や実serving policyそのものは含めない。

### 含める研究

- LLM serving離散事象シミュレータ
- 実runtimeを残したGPUエミュレーション
- カーネルからservingまでの性能モデル

### 含めない研究

- 実測値を列挙するだけのbenchmark
- 本番serving schedulerそのもの

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [09-kernel-runtime-compilation](../09-kernel-runtime-compilation/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（74本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/15-inference-simulation-emulation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure](2026-2602.23036-llmservingsim-2-heterogeneous-disaggregated-simulator.md)**  
  実装：[✓](https://github.com/casys-kaist/LLMServingSim) ・ リポジトリ内被引用：12  
  異種GPU/TPU/PIMと分離サービング・多階層鍵値メモリ・MoE・電力を要求駆動ループで統合模擬するLLMサービングシミュレータ。

- **2026-01 · [AIConfigurator: Lightning-Fast Configuration Optimization for Multi-Framework LLM Serving](2026-2601.06288-aiconfigurator-multi-framework-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  実GPUで測った演算・通信性能から複数のLLMサービング構成をCPU上で予測し、並列化やバッチ、プリフィル・デコード分離を探索して遅延目標を満たす候補を選ぶ。

- **2026-01 · [Revati: Transparent GPU-Free Time-Warp Emulation for LLM Serving](2026-2601.00397-revati-transparent-gpu-free-time-warp-emulation.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  実LLMサーバ制御コードをそのまま走らせ、GPU計算だけ仮想時間へ置換して5%未満の誤差と約5〜17倍の評価高速化を狙うGPU不要エミュレータ。

- **2026-06 · [Frontier: Towards Comprehensive and Accurate LLM Inference Simulation](2026-2605.21312-frontier-comprehensive-accurate-llm-inference-simulation.md)**  
  実装：[✓](https://github.com/NetX-lab/Frontier) ・ リポジトリ内被引用：5  
  分離プリフィル/デコードや注意-FFN分離を役割別イベントグラフとして再現し、演算・通信・KVメモリを実測校正して、現代LLMサービング構成の性能を高精度に予測する。

- **2026-01 · [ScaleSim: Serving Large-Scale Multi-Agent Simulation with Invocation Distance-Based Memory Management](2026-2601.21473-scalesim-serving-large-scale-multi-agent-simulation-with-invocation-dist.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  ScaleSimは、多数の大規模言語モデル利用エージェントを同時に動かすシミュレーションにおいて、GPUメモリ上のエージェント固有状態を、次にどのエージェントが言語モデルを呼び出すかというアプリケーション側の予測に基づいて管理する配信システムである。

- **2026-03 · [DyQ-VLA: Dynamic Quantization and Compensation for VLA models with Runtime Error Awareness](2026-2603.07904-dyq-vla-temporal-dynamic-aware-quantization-for-embodied-vision-language.md)**  
  実装：[✓](https://anonymous.4open.science/r/DyQ-VLA-7F51/) ・ リポジトリ内被引用：2  
  DyQ-VLAの2026年10月4日公開の第3版は、量子化によって変わる実行時の行動と誤差の相関を明示的に測り、並進と回転で異なる制御を行う。LIBEROおよびRoboTwin 2.0の評価では、BF16に対する推論単位の速度改善が1.74〜1.81倍、成功した実行全体にわたるモデル推論時間の改善が1.88〜1.93倍となった。

- **2026-06 · [KernelSight-LM: A Kernel-Level LLM Inference Simulator](2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUカーネル予測と実運用サービングの離散事象モデルを統合し、未計測GPUでもカーネル誤差12.1%、対象計測ありで3.8%を達成。

- **2026-06 · [Characterizing How Complex Agentic AI Systems Handle General Tasks: A Trace-Based Simulation Study](2026-2606.01725-characterizing-how-complex-agentic-ai-systems-handle-general-tasks-a-tra.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.22133686) ・ リポジトリ内被引用：1  
  さらに既存のLLMサービングシミュレータVidurを拡張したVidur-Agentへトレースを入力し、GPU配分、接頭辞キャッシュ（prefix キャッシュ）、事前充填と復号の分離、要求の処理順を変えてタスク完了時間を比較する。

- **2026-05 · [LLM-Emu: Native Runtime Emulation of LLM Inference via Profile-Driven Sampling](2026-2605.00616-llm-emu-native-runtime-emulation.md)**  
  実装：[✓](https://github.com/AKafakA/llm-emu) ・ リポジトリ内被引用：1  
  vLLMの本番HTTP・スケジューラ・KV管理を実コードのまま動かし、GPU順伝播だけを二次元遅延プロファイルからの標本化へ置換して、実GPU比の出力トークン当たり時間・反復時間を4.8%、エンドツーエンド遅延を5.3%、出力スループットを1.9%以内で再現する（初回トークン時間は最大10.41%ずれる）実時間エミュレータ。

- **2026-05 · [EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture](2026-2605.24144-eva-accelerating-llm-decoding-via-an-efficient-vector-quantization-archi.md)**  
  実装：[✓](https://github.com/dbw6/Eva) ・ リポジトリ内被引用：1  
  ベクトル量子化は複数重みを一つの索引にまとめるため2ビット級の圧縮品質に優れる一方、従来の実装では重み索引から符号帳の値を不規則に読み出す。

- **2026-02 · [Asynchronous Verified Semantic Caching for Tiered LLM Architectures](2026-2602.13165-asynchronous-verified-semantic-caching-for-tiered-llm-architectures.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  著者は、事前に人手や大規模モデルで検証した回答を持つ静的キャッシュと、通常の要求を処理しながら生成回答を保存する動的キャッシュを分離する構成を前提とする。原著のトレース駆動シミュレーションでは、会話要求における静的由来回答の割合が8.2%から19.4%、検索要求では2.2%から8.6%へ増えた。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [ePACT: Energy-Performance-Aware Commitment Tracking for LLM Serving](2026-2610.01784-epact-energy-performance-aware-commitment-tracking-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMサービングの電力を単純に減らすのではなく、事前に契約した時間単位の電力量へ実消費を近づける。要求ごとのサービス期限を予測し、レプリカ数とGPUクロックをオンラインで調整する。

- **2026-09 · [Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash](2026-2609.15636-trillion-parameter-moe-in-a-box-decoupling-memory-provisioning-with-high.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、総パラメータ数が1兆を超える混合専門家モデル（Mixture-of-Experts、MoE）を、多数の要求で負荷を平準化するクラスタではなく、同時要求数1〜8程度の単一装置で動かす場合のメモリ設計を検討する。

- **2026-09 · [RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems](2026-2609.12551-rooflang-ai-driven-llm-inference-architecting.md)**  
  実装：[✓](https://github.com/yzygitzh/rooflang) ・ リポジトリ内被引用：0  
  RoofLangはLLM推論を計算・ハードウェアグラフと意味保存変換で表し、実装非依存のシミュレーションを評価器としてAIに配置・並列化・通信構成を探索させる設計基盤である。

- **2026-09 · [Hot–Cold Tiering of HBM and High Bandwidth Flash for Agentic LLM Serving](2026-2609.25782-hot-cold-tiering-of-hbm-and-high-bandwidth-flash-for-agentic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全セッションのKVを高帯域メモリ（High Bandwidth メモリ; HBM）に残せば容量が不足し、CPUメモリなどへ退避すると復帰時の転送待ちが増える。Qwen3-Coder-30B-A3Bを用いたエージェント作業のトレースで、HBM単独の165セッションに対してHBF追加構成は3900セッションを保持する（約23.6倍）。

- **2026-09 · [FlashGPU-sim: Enabling GPU Modeling for Modern Architectures and AI Workloads](2026-2609.15311-flashgpu-sim-enabling-gpu-modeling-for-modern-architectures-and-ai-workloads.md)**  
  実装：[✓](https://github.com/FlashGPU-Sim/FlashGPU-Sim) ・ リポジトリ内被引用：0  
  Hopper/Blackwellの非同期GPU機構とTriton AIカーネルを実行駆動で再現し、131構成でサイクル誤差5.24%、16スレッドで7.86倍高速化した現代GPUシミュレータ。

- **2026-09 · [Decomposing Predictive Kubernetes Autoscaling for Large Language Model Serving Under Long Startup Delays](2026-2609.20874-decomposing-predictive-kubernetes-autoscaling-for-large-language-model-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）をオンライン配信するKubernetes環境では、レプリカ（同じモデルを提供する推論プロセス）を新しく起動するだけで数分かかる。すなわち、要求件数でなく入力・出力トークン量を測ること、起動遅延 $\Delta$ だけ将来を予測すること、予測誤差の上側余裕を設けること、待ち行列とKVキャッシュ圧迫度を状態として観測することである。

- **2026-09 · [Characterizing High Bandwidth Flash for LLM Serving](2026-2609.39131-characterizing-high-bandwidth-flash-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らはHBM、HBF、ホストDRAM、SSDの四階層にまたがる配置方針と、キャッシュ再利用を優先しながら新規要求の受入れを制限するスケジューラを設計する。B200相当の計算モデルとHBFの仮定仕様を用いた結果、評価した負荷条件で処理完了時間を36.1〜87.7%短縮する構成があり、モデル化したエネルギー削減率は最大59.1%に達する。

- **2026-08 · [Unified Lookup-Table Inference with Signed-Digit K/V Caches for Ternary LLMs](2026-2608.03229-unified-lookup-table-inference-with-signed-digit-k-v-caches-for-ternary-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SALUTは三値重みの線形演算を高速化する参照表（LUT）演算器と、動的に生成される高精度KVキャッシュを処理する注意演算器が分離してしまう問題を解く。

- **2026-08 · [The Joule Point: an Energy-Optimal Operating Point for AI Inference](2026-2609.27926-the-joule-point-an-energy-optimal-operating-point-for-ai-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし、GPUにはアイドルに近い状態でも必要な固定電力があり、高負荷領域では電力が処理速度より急激に増える。GPUを「A100を何枚割り当てるか」というハードウェア単位だけで扱うのではなく、(GPU種類、power cap) の組を動作点として扱う。

- **2026-08 · [Spatial Prefix Caching for Wireless Edge LLM Inference: A Stochastic-Geometry and Queueing Framework](2026-2608.01126-spatial-prefix-caching-for-wireless-edge-llm-inference-a-stochastic-geom.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案はこの四つの費用を一つの最初のトークンまでの時間（TTFT）へ統合する。正規化した数値実験では、空間要求強度4件/(km²・秒)、TTFT閾値0.8秒における達成率が、提案法約0.63、接頭辞一致だけを優先してキューを無視する方式約0.23、最近傍ノード選択約0.52だった。

- **2026-08 · [Simthesizer: An Agent-Driven Simulation Framework for LLM Serving Systems](2026-2608.24650-simthesizer-an-agent-driven-simulation-framework-for-llm-serving-systems.md)**  
  実装：[✓](https://github.com/casys-kaist/Simthesizer) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論提供では、連続的なバッチ形成、入力処理と生成の分離、KVキャッシュの退避、投機的復号、専門家混合（MoE）、複数回のモデル呼出しを含むエージェント処理など、複雑な機構が急速に増えている。

- **2026-08 · [LLM Inference Under Bursty Workload Distribution: Modifying the WAIT Algorithm](2026-2608.06135-llm-inference-under-bursty-workload-distribution-modifying-the-wait-algo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMサービングでは、GPUに投入するバッチを大きくすれば1回の演算で多くの要求を処理できる一方、十分な要求が集まるまで待つと応答遅延が増える。既存のWAIT（Waiting for Accumulated Inference Threshold）スケジューラは、要求種別ごとの到着率を事前に知っている前提でバッチ投入の閾値を決める。

- **2026-08 · [HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads](2026-2608.19395-hydra-a-heterogeneous-chiplet-dse-framework-for-serving-dynamic-hybrid-l.md)**  
  実装：[✓](https://github.com/ONQLin/hydra-cases-2026-artifact) ・ リポジトリ内被引用：0  
  HYDRAは、注意機構（注意機構）と状態空間モデル（State Space モデル、SSM）を混在させた大規模言語モデルの推論サービスに向けて、複数種類の計算・メモリチップレットをどう組み合わせ、配置し、実行時に使い分けるかを探索する設計空間探索（Design Space Exploration、DSE）基盤である。

- **2026-08 · [Beyond Binary Priorities: Multi-Tier SLA Scheduling for Large Language Model Serving](2026-2608.16336-beyond-binary-priorities-multi-tier-sla-scheduling-for-large-language-mo.md)**  
  実装：[✓](https://github.com/andersvestrum/llumnix_sim) ・ リポジトリ内被引用：0  
  本論文は、Llumnixの二段階（高優先度・通常）の優先度管理を任意のK段階へ拡張し、LLMサービングにおけるSLA階層とKVキャッシュ容量の予約を同時に扱うスケジューラを提案する。均等分布1万リクエストではK=4がINFaaS+vLLM比でプリフィル平均8.23倍、エンドツーエンド P99 3.13倍、コスト-per-遅延 68%改善を示す。

- **2026-08 · [BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge](2026-2608.05926-balance-hybrid-autoregressive-speculative-llm-inference-at-the-network-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（SD）は小規模言語モデル（SLM）が複数トークンを提案し、LLMがまとめて検証するため遅延を下げられる一方、LLMとSLM双方の重み、両方式のKVキャッシュ、複数トークンの検証に必要なメモリがGPUに載る。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMETは、LLMのタイル配置とメモリ階層転送を回路レベルのSRAM・M3D特性へ接続し、L2容量を増やす利益とアクセス費が釣り合う省エネ設計点を探索する。

- **2026-07 · [ELiTeFormer: An Efficient Transformer for FPGAs](2026-2607.03652-eliteformer-an-efficient-transformer-for-fpgas.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ELiTeFormerは、言語モデルの注意機構と全結合層を個別に高速化するだけでは、再構成可能な論理回路（Field-Programmable Gate Array; FPGA）の特性を十分に利用できないという問題に取り組む。

- **2026-07 · [Auto-Scaling Heterogeneous Neural Processing Units for Energy and Cost-Efficient LLM Serving](2026-2607.16488-auto-scaling-heterogeneous-neural-processing-units-for-energy-and-cost-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NeuScaleは、世代ごとに計算性能、メモリ帯域、メモリ容量、チップ間通信性能が異なるニューラル処理装置（NPU）を、LLM推論サービスに効率よく割り当てる制御方式である。複数モデルと複数要求系列にわたる均質構成の従来型自動伸縮方式との比較で、平均エネルギー効率1.13倍、金銭的費用効率1.43倍、サービス水準目標（SLO）達成率1.36倍を報告する。

- **2026-05 · [MoE-Hub: Taming Software Complexity for Seamless MoE Overlap with Hardware-Accelerated Communication on Multi-GPU Systems](2026-2605.05888-moe-hub-taming-software-complexity-for-seamless-moe-overlap-with-hardwar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案方式は、ルータが決めた論理宛先だけでトークン行を送信できるst.rowsp命令と、受信側で実際の格納行を割り当てるアドレス割当装置（Address Allocation Unit; AAU）を導入する。

- **2026-05 · [GAPS: Global-Aware Prediction-driven Scheduling for Large-Scale LLM Inference](2026-334dba8993b3-gaps-global-aware-prediction-driven-scheduling-for-large-scale-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GAPS（Global-Aware Prediction-driven Scheduling）は、複数GPUで大規模言語モデル（Large Language モデル; LLM）の推論要求を受け付けるとき、全インスタンスの負荷を監視し、要求の処理時間を予測して割当と再配置を決めるスケジューラである。

- **2026-05 · [Dooly: Configuration-Agnostic, Redundancy-Aware Profiling for LLM Inference Simulation](2026-2605.07985-dooly-configuration-agnostic-redundancy-aware-profiling-for-llm-inferenc.md)**  
  実装：[✓](https://github.com/dooly-project) ・ リポジトリ内被引用：0  
  しかし従来方式は演算の種類や呼び出し引数を特定のモデル・エンジン向けに手作業で定義し、異なるモデルでも同じ演算を繰り返し測定する。

- **2026-05 · [BAGEN: Are LLM Agents Budget-Aware?](2026-2606.00198-bagen-are-llm-agents-budget-aware.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の評価では、タスクの成否と終了後の消費トークン数を記録するが、実行途中のエージェント自身が残りの必要予算を理解していたかは別問題である。BAGEN（Budget-Aware Agent）は、残予算の自己推定を独立した能力として定義し、途中状態ごとに「完了に必要な資源の下限・上限」または「完了不可能」を回答させる評価枠組みを提案する。

- **2026-04 · [RouteNLP: Closed-Loop LLM Routing with Conformal Cascading and Distillation Co-Optimization](2026-2604.23577-routenlp-closed-loop-llm-routing-with-conformal-cascading-and-distillati.md)**  
  実装：[✓](https://github.com/bettyguo/RouteNLP) ・ リポジトリ内被引用：0  
  提案方式は、タスク条件付きの難易度予測器、共形リスク制御で初期化した品質確認付きの段階的移行、失敗した問い合わせを分類して小型モデルを再蒸留する閉ループという三つの機構を連結する。8週間・1日約5,000件の顧客サービス試験運用では、費用58%削減、専門家による応答受理率91%を報告した。

- **2026-04 · [DeepStack: Facilitating Co-Design Exploration of 3D DRAM-Stacked Accelerators for Distributed LLM Inference](2026-2604.04750-deepstack-facilitating-co-design-exploration-of-3d-dram-stacked-accelera.md)**  
  実装：[✓](https://github.com/tile-ai/DeepStack/tree/ae) ・ リポジトリ内被引用：0  
  本論文は、3D積層DRAMを計算ダイの近傍に接続したAIアクセラレータを複数台組み合わせる際、チップ設計とLLMの分散実行計画を別々に最適化すると誤った設計を選ぶという問題に取り組む。重要なのは「高速な新GPUを実際に製造して推論が9.5倍になった」研究ではない点である。

- **2026-04 · [CodeQuant: Unified Clustering and Quantization for Enhanced Outlier Smoothing in Low-Precision Mixture-of-Experts](2026-2604.10496-codequant-unified-clustering-and-quantization-for-enhanced-outlier-smoot.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/CodeQuant) ・ リポジトリ内被引用：0  
  これを低ビット化するとGPUメモリ使用量を減らせるものの、活性値や重みに少数の大きな外れ値があると、均一な量子化の刻み幅が粗くなり、特に4ビット級で精度が悪化する。主要評価はPhi-mini-MoE-Instruct、DeepSeek-V2-Lite、Qwen3-30B-A3B、Mixtral 8×7Bを対象とする。

- **2026-04 · [Adaptive Load Balancing for Multi-Tier LLM Inference with Dynamic Model Routing](2026-cedb2b11ea50-adaptive-load-balancing-for-multi-tier-llm-inference-with-dynamic-model-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  論文の代表結果は、5,000件の合成要求を使ったシミュレーションで、ラウンドロビン方式に対して平均応答時間を101.36 msから49.48 msへ51.18%短縮し、総費用を4.3322米ドルから1.2964米ドルへ70.08%削減したというものである。

- **2026-04 · [A Case for a Simulation-Driven Exploration of Distributed GenAI Platforms](2026-7f1241155fa8-a-case-for-a-simulation-driven-exploration-of-distributed-genai-platform.md)**  
  実装：[✓](https://github.com/IBM/opal-sim) ・ リポジトリ内被引用：0  
  リクエストの到着率、入力・出力長、プリフィルとデコードの資源配分、ルーティング、KVキャッシュの再利用、階層ストレージへの退避、ネットワーク輻輳、オートスケールが相互作用する。1万GPUワーカーを模擬するMoonshotAIのトレース再生は38～144秒で完了するが、これはGPU実機のLLM推論が高速化したという結果ではない。

- **2026-03 · [Temperature-Aware Scheduling of LLM Inference in Large-Scale Geo-Distributed Edge Data Centers with Distributed Optimization](2026-2603.07810-temperature-aware-scheduling-of-llm-inference-in-large-scale-geo-distrib.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  地理的に離れた複数のデータセンターへ大規模言語モデル（LLM）の推論要求を割り振るとき、要求の到着場所、GPUの処理能力、通信遅延だけでなく、各拠点の外気温も運用費を左右する。本論文は、これらをLLM推論要求の配置問題に統合する。ただし原著は主要結果をSplitwise比で正規化した図として示し、本文中に個別指標の絶対値・改善率・信頼区間を列挙していない。

- **2026-03 · [FleetOpt: Analytical Fleet Provisioning for LLM Inference with Compress-and-Route as Implementation Mechanism](2026-2603.16514-fleetopt-analytical-fleet-provisioning-for-llm-inference-with-compress-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FleetOptは、長文脈LLM推論のGPUをすべて最大入力長に合わせて確保すると、多くの短い要求に対してKVキャッシュ枠が過大になる問題を扱う。境界をわずかに超えた要求は、推論エンジンへ入れる前にゲートウェイで文章を抽出圧縮し、短文脈プールへ移せるようにする。

- **2026-02 · [TriGen: NPU Architecture for End-to-End Acceleration of Large Language Models based on SW-HW Co-Design](2026-2602.12962-trigen-npu-architecture-for-end-to-end-acceleration-of-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TriGenは、モバイルや組込み機器のようにSRAM容量とDRAM帯域が厳しく制限される環境で、Transformer型LLMの線形演算だけでなくRMSNorm、softmax、SiLUなどの非線形演算を含むモデル全体を一つのNPU設計で実行する研究である。

- **2026-02 · [TOM: A Ternary Read-only Memory Accelerator for LLM-powered Edge Intelligence](2026-2602.20662-tom-a-ternary-read-only-memory-accelerator-for-llm-powered-edge-intellig.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TOMは、三値重み（ternary 重み）を持つ大規模言語モデル（LLM）をエッジ端末で低遅延・低消費電力に動かすための、読出し専用メモリ（ROM）と静的ランダムアクセスメモリ（SRAM）の混合専用回路である。重みを毎トークン外部メモリから転送する方式と異なり、固定ベースモデルの重みをROMとしてオンチップへ焼き込み、各演算器の近くに分散配置する。

- **2026-02 · [Harmonia: Algorithm-Hardware Co-Design for Memory- and Compute-Efficient BFP-based LLM Inference](2026-2602.04595-harmonia-algorithm-hardware-co-design-for-memory-and-compute-efficient-b.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論ではモデル重みだけでなく、各層で生じる活性化と、長い入力履歴を保持する鍵・値キャッシュ（KVキャッシュ）がメモリ容量・帯域・演算器の面積を消費する。重みだけを4ビット整数へ量子化しても、活性化がFP16のままでは浮動小数点と整数の混合積和演算を処理する回路が必要になる。

- **2026-01 · [Mugi: Value Level Parallelism For Efficient LLMs](2026-2601.10823-mugi-value-level-parallelism-for-efficient-llms.md)**  
  実装：[✓](https://zenodo.org/records/18063514) ・ リポジトリ内被引用：0  
  Mugiは、値レベル並列性（Value Level Parallelism; VLP）という、数値が一致する複数の演算に対して中間結果を共有するハードウェア方式を、LLMの推論へ適用した研究である。

- **2025-12 · [SQ-format: A Unified Sparse-Quantized Hardware-friendly Data Format for LLMs](2025-2512.05409-sq-format-a-unified-sparse-quantized-hardware-friendly-data-format-for-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非構造的な任意位置の疎性より、ハードウェアが扱う要素数を予測しやすく、低精度の密な経路と高精度の疎な経路を組み合わせやすい。Llama-3-70Bの入力処理（プリフィル）では、W4A8基準の10分8秒に対し、静的活性SQ方式の疎性0.875で5分55秒となり、1.71倍の高速化を報告する。

- **2025-12 · [RAPID-LLM: Runtime Analysis of Parallel Infrastructure for Distributed LLM Training and Inference](2025-2512.19606-rapid-llm-runtime-analysis-of-parallel-infrastructure-for-distributed-ll.md)**  
  実装：[✓](https://github.com/nanocad-lab/Rapid-LLM) ・ リポジトリ内被引用：0  
  RAPID-LLMは、大規模言語モデル（LLM）の分散学習と推論について、モデル構造、並列化方式、GPU仕様、通信網構成を与えると実行時間を予測する基盤である。A100とH100における学習・推論124条件の実測値に対し、全体の平均絶対百分率誤差（Mean Absolute Percentage Error; MAPE）は10.0%である。

- **2025-12 · [DCO: Dynamic Cache Orchestration for LLM Accelerators through Predictive Management](2025-2512.07312-dco-dynamic-cache-orchestration-for-llm-accelerators-through-predictive-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DCOは、複数の人工知能演算コアが共有する最終段キャッシュ（last-level キャッシュ、LLC）を、単なる過去のアクセス時刻ではなく、演算グラフから分かるテンソルの参照予定回数とデータフローに従って管理する提案である。論文v2のHTML本文は従来LRUに対する最大1.90倍の速度向上を記す。

- **2025-11 · [Multiplexed Heterogeneous LLM Serving via Stage-Aligned Parallelism](2025-832f2fc32711-multiplexed-heterogeneous-llm-serving-via-stage-aligned-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ParaFlexは、規模や必要メモリが異なる複数の大規模言語モデル（LLM）を、同じGPU群上で効率よく同時提供するための推論サービングシステムである。原著は異種モデルの混合負荷で、テンソル並列型の多重化と比べ中央値遅延を最大63%削減、処理量を最大4.7倍に改善し、共有パイプライン型の既存方式に対して処理量を最大1.6倍に改善したと報告する。

- **2025-11 · [From Models to Operators: Rethinking Autoscaling Granularity for Large Generative Models](2025-2511.02248-from-models-to-operators-rethinking-autoscaling-granularity-for-large-ge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの推論基盤では、負荷に応じてモデル全体の複製を増減することが一般的である。各演算子に異なる複製数、バッチ、並列度を割り当て、最後にGPUへ配置する。

### 2年前（2024-11〜2025-10）

- **2024-11 · [APEX: An Extensible and Dynamism-Aware Simulator for Automated Parallel Execution in LLM Serving](2024-2411.17651-apex-an-extensible-and-dynamism-aware-simulator-for-automated-parallel-e.md)**  
  実装：[✓](https://github.com/microsoft/apex_plus) ・ リポジトリ内被引用：13  
  APEXは、大規模言語モデル（LLM）を複数GPUで提供する際に、どの並列化方式を組み合わせるべきかを実機へ総当たりで配備せず、CPU上のシミュレーションで比較するシステムである。

- **2025-07 · [Rethinking LLM Inference Bottlenecks: Insights from Latent Attention and Mixture-of-Experts](2025-2507.15465-rethinking-llm-inference-bottlenecks-insights-from-latent-attention-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  従来の大規模言語モデルでは、多頭注意（multi-head 注意機構、MHA）の復号時演算は過去の鍵・値キャッシュを大量に読み出すため、メモリ帯域が主要な制約と考えられてきた。

- **2025-07 · [Efficient and Scalable Agentic AI with Heterogeneous Systems](2025-2507.19635-efficient-and-scalable-agentic-ai-with-heterogeneous-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  本研究は、一つの大規模言語モデル（LLM）を高速化するのではなく、複数のモデル推論・外部検索・ツール実行を含むエージェント全体を、異なる計算特性を持つ装置へ配置することを目的とする。音声対話エージェントを例にすると、音声認識、文脈検索、LLMによる応答生成、検索API、音声合成は互いに依存するが、同じGPUを使う必要はない。

- **2025-07 · [Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations](2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference.md)**  
  実装：[✓](https://github.com/ozcanmiraay/vidur-energy) ・ リポジトリ内被引用：4  
  LLMの推論基盤は、要求到着率、入力と出力の長さ、バッチ編成、モデル並列方式によってGPUの使用状況が大きく変わる。A100上のCodeLlama-34Bの並列構成比較では、平均GPU電力213.2～355.3W、総エネルギー0.16～0.56kWhと構成によって大きく変わる。

- **2025-03 · [Improving the End-to-End Efficiency of Offline Inference for Multi-LLM Applications Based on Sampling and Simulation](2025-2503.16893-improving-the-end-to-end-efficiency-of-offline-inference-for-multi-llm-a.md)**  
  実装：[✓](https://github.com/puddingfjz/vllm) ・ リポジトリ内被引用：3  
  本研究が対象とするのは、あらかじめ処理する要求集合が分かっているオフライン推論であり、複数の大規模言語モデル（LLM）を一つのアプリケーション内で使う状況である。単一モデルの要求順序を最適化するだけでは、モデル間のGPU分配を決められない。SamuLLMはこれらを一つの計画問題として扱う。

- **2024-11 · [DeeR-VLA: Dynamic Inference of Multimodal Large Language Models for Efficient Robot Execution](2024-2411.02359-deer-vla-dynamic-inference-of-multimodal-large-language-models-for-effic.md)**  
  実装：[✓](https://github.com/yueyang130/DeeR-VLA) ・ リポジトリ内被引用：3  
  DeeR-VLA（動的 Early-Exit for Robotic Multimodal Large Language Models）は、画像と自然言語の指示からロボットの行動を決める視覚・言語・行動モデルに、複数の中間出口（early exit）を設ける推論時の計算資源配分方式である。

- **2025-10 · [LLM.265: Video Codecs are Secretly Tensor Codecs](2025-5a2b2924d4e3-llm-265-video-codecs-are-secretly-tensor-codecs.md)**  
  実装：[✓](https://github.com/Entropy-xcy/llm.265) ・ リポジトリ内被引用：2  
  大規模言語モデル（LLM）の推論では、重み、鍵・値キャッシュ（KV キャッシュ）、パイプライン並列（パイプライン parallelism）の段間活性値を保持・転送する費用が大きい。従来の低ビット量子化は重みやKVキャッシュなど個別の対象に特化し、校正データや量子化方式の選択を必要とする場合が多い。

- **2025-04 · [SplitReason: Learning To Offload Reasoning](2025-2504.16379-splitreason-learning-to-offload-reasoning.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/SplitReason) ・ リポジトリ内被引用：1  
  大規模推論モデルは、数学問題などで長い思考連鎖（Chain-of-Thought; CoT）を生成する。思考の各トークンを高価な大型モデルで生成すると、逐次復号（デコード）の費用が大きくなる。一方、途中の式変形や説明のすべてが大型モデルを必要とするわけではない。基本構成は1.5Bパラメータの小型推論モデルと、8B・14B・32Bなどの大型推論モデルである。

- **2025-04 · [MIST: A Co-Design Framework for Heterogeneous, Multi-Stage LLM Inference](2025-2504.09775-mist-a-co-design-framework-for-heterogeneous-multi-stage-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMサービングの性能は、モデルのプリフィルとデコードだけでなく、RAGの検索、KVキャッシュの再利用、ネットワーク転送、スケジューリング、異なるモデルを使う複数クライアントなどの組合せで決まる。しかし異なるベンダーを跨いだプリフィル/デコード（PD）分離を、実際の統一サービングスタックで検証できないことが多い。

- **2024-11 · [Anda: Unlocking Efficient LLM Inference with a Variable-Length Grouped Activation Data Format](2024-2411.15982-anda-unlocking-efficient-llm-inference-with-a-variable-length-grouped-ac.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AndaはこのFP-INT行列積を対象に、活性値の格納形式、各演算モジュールへ割り当てる精度、専用回路の三つを共同最適化する研究である。

- **2025-09 · [SAIL: SRAM-Accelerated LLM Inference System with Lookup-Table-based GEMV](2025-2509.25853-sail-sram-accelerated-llm-inference-system-with-lookup-table-based-gemv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAIL（SRAM-Accelerated Inference of LLMs）は、量子化されたLLMをCPUベースのサーバで効率的に推論するため、CPUのLast-Level Cache（LLC）の各sliceの近傍に演算可能なSRAM（C-SRAM）を追加し…

- **2025-08 · [COMET: A Framework for Modeling Compound Operation Dataflows with Explicit Collectives](2025-2509.00599-comet-a-framework-for-modeling-compound-operation-dataflows-with-explici.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著はLlama-3とGPT-2由来の演算形状を使い、GEMM-Softmax、GEMM-LayerNorm、self-注意機構を、edge/cloudの二つの仮想アクセラレータ構成で評価する。非融合のデータフローを基準に、最適化したマッピングの幾何平均速度比は順に1.42倍、3.46倍、1.82倍と報告する。

- **2025-07 · [Temporal-Aware GPU Resource Allocation for Distributed LLM Inference via Reinforcement Learning](2025-2507.10259-temporal-aware-gpu-resource-allocation-for-distributed-llm-inference-via.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の地域に分散したGPUサーバーへ推論要求を割り当てるとき、現在の空き容量だけを見て最も速そうなサーバーを選ぶと、需要の増加に遅れて起動するサーバーや、短時間で頻繁に移動する要求が生まれる。

- **2025-06 · [Semantic Scheduling for LLM Inference](2025-2506.12204-semantic-scheduling-for-llm-inference.md)**  
  実装：[✓](https://github.com/Wenyueh/latency_optimization_with_priority_constraints) ・ リポジトリ内被引用：0  
  本論文は、LLMのオンライン推論に到着する要求を単なる先着順や予測実行時間順ではなく、要求文面から推定される緊急度を第一の優先基準として実行するスケジューラを提案する。実データ条件で最も緊急な要求の正規化待ち時間がFCFS比最大167.3倍短縮した条件がある。

- **2025-05 · [Serve Programs, Not Prompts](2025-2510.25412-serve-programs-not-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLMサービングの基本単位を「プロンプトを受け取ってトークン列を返すリクエスト」から、LLM推論プログラム（LLM Inference Program, LIP）へ変えるというシステム設計を提案する。

- **2024-11 · [MAS-Attention: Memory-Aware Stream Processing for Attention Acceleration on Resource-Constrained Edge Devices](2024-2411.17720-mas-attention-memory-aware-stream-processing-for-attention-acceleration-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MAS-注意機構は、演算資源とオンチップ記憶容量が限られる端末向けニューラル演算器において、正確な注意機構を高速化する計算配置方式である。著者らは、改変TileFlow・Timeloop・Accelergyによる端末向け演算器のシミュレーションで、FLATに対する注意演算サイクルの最大2.75倍の高速化、最大54.03%の推定消費エネルギー削減を報告した。

### 3年前（2023-11〜2024-10）

- **2024-05 · [Vidur: A Large-Scale Simulation Framework For LLM Inference](2024-2405.05465-vidur-a-large-scale-simulation-framework-for-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/vidur) ・ リポジトリ内被引用：59  
  Vidurは、大規模言語モデル（LLM）をどのGPUに何台配置し、どの並列化方式・バッチ化方式で処理するかを、候補ごとに実機で運転せず比較するためのシミュレータである。LLaMA2-7B/70B、InternLM-20B、Qwen-72Bを使った実機比較では、オンライン負荷での正規化要求遅延の誤差は最大でも9%未満と報告される。

- **2023-12 · [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](2023-2312.03134-llmcompass-enabling-efficient-hardware-design-for-large-language-model-i.md)**  
  実装：[✓](https://github.com/PrincetonUniversity/LLMCompass) ・ リポジトリ内被引用：19  
  入力はモデルの計算グラフと装置構成であり、出力は演算子別・推論段階別の遅延、チップ面積、製造費用の推定値である。性能推定と面積・費用推定を同一の設計空間で組み合わせるため、最速のチップだけでなく、価格に見合った推論性能を評価できる。

- **2024-08 · [LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale](2024-2408.05499-llmservingsim-a-hw-sw-co-simulation-infrastructure-for-llm-inference-ser.md)**  
  実装：[✓](https://github.com/casys-kaist/llmservingsim) ・ リポジトリ内被引用：14  
  大規模言語モデルの推論基盤では、GPUや専用演算器の設計だけでなく、到着する要求の分布、バッチ化、KVキャッシュ管理、複数装置へのモデル分割が性能を左右する。論文は実GPU上の推論基盤に対する性能傾向の誤差を平均14.7%程度に抑え、既存の演算器シミュレータに対して34.7〜491倍の高速化を報告する。

- **2024-06 · [Demystifying AI Platform Design for Distributed Inference of Next-Generation LLM models](2024-2406.01698-demystifying-ai-platform-design-for-distributed-inference-of-next-generation-llm-models.md)**  
  実装：[✓](https://github.com/abhibambhaniya/GenZ-LLM-Analyzer) ・ リポジトリ内被引用：9  
  演算子-階層 ルーフラインと集合通信通信モデルでLLM構造・推論提供最適化・分散方式から計算/メモリ/ネットワーク要件を逆算するGenZ。

- **2024-09 · [TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation](2024-2409.12514-tinyvla-towards-fast-data-efficient-vision-language-action-models-for-ro.md)**  
  実装：[✓](https://github.com/liyaxuanliyaxuan/TinyVLA) ・ リポジトリ内被引用：6  
  提案手法は、画像・言語の意味理解を約4.2億〜13億パラメータの小型マルチモーダル基盤モデルへ、連続行動の生成を拡散方策（diffusion policy）復号器へ分担させる。実機のFranka単腕ロボット5タスクでは、最大構成TinyVLA-Hの平均成功率が94.0%、OpenVLAが68.3%であり、差は25.7パーセントポイントだった。

- **2024-08 · [LUT Tensor Core: A Software-Hardware Co-Design for LUT-Based Low-Bit LLM Inference](2024-2408.06003-lut-tensor-core-a-software-hardware-co-design-for-lut-based-low-bit-llm-.md)**  
  実装：[✓](https://github.com/microsoft/T-MAC/tree/LUTTensorCore_ISCA25) ・ リポジトリ内被引用：6  
  重みを1〜4ビットに量子化した大規模言語モデル（LLM）では、重みの転送量は小さくなる一方、活性化はFP16やINT8など比較的高い精度で保持される。ISCA 2025の原著は、従来のLUTアクセラレータに比べて計算密度とエネルギー効率を1.44倍改善し、低ビットLLMの推論をモデル単位のシミュレーションで2.06〜5.51倍高速化したと報告する。

### 4年前（2022-11〜2023-10）

- **2023-10 · [Sia: Heterogeneity-aware, goodput-optimized ML-cluster scheduling](2023-2c2071afa90d-sia-heterogeneity-aware-goodput-optimized-ml-cluster-scheduling.md)**  
  実装：[✓](https://github.com/siasosp23/artifacts) ・ リポジトリ内被引用：4  
  Siaは、GPUの種類が混在する深層学習訓練クラスタで、各ジョブへ割り当てるGPUの種類・台数・バッチサイズを同時に決めるスケジューラである。原著は、44GPUの実機クラスタで既存のPolluxより平均ジョブ完了時間を約35〜50%、Gavelより約50%短縮したと報告する。

### 7年前（2019-11〜2020-10）

- **2020-02 · [A3: Accelerating Attention Mechanisms in Neural Networks with Approximation](2020-2002.10941-a3-accelerating-attention-mechanisms-in-neural-networks-with-approximati.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  通常の注意機構は、クエリベクトルと全キー行の内積を求め、softmaxで正規化し、値ベクトルを重み付き合成する。保守的設定は近似によるタスク精度の低下をおおむね1%に抑える一方、積極的設定はおおむね8%の精度低下を伴う。

### 9年前（2017-11〜2018-10）

- **2017-12 · [Ray: A Distributed Framework for Emerging AI Applications](2017-1712.05889-ray-a-distributed-framework-for-emerging-ai-applications.md)**  
  実装：[✓](https://github.com/ray-project/ray) ・ リポジトリ内被引用：20  
  Rayは、強化学習で頻繁に現れる「多数の環境を並列に動かす」「学習器で方策を更新する」「更新した方策を低遅延で実行する」という異質な仕事を、別々の分散基盤へ切り分けずに一つの実行系へ載せるための研究である。提案の中核は、状態を持たない遠隔関数を「タスク」、状態を保持する遠隔オブジェクトを「アクター」として同じ動的依存グラフへ埋め込むことである。
<!-- survey:auto:end -->
