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
## 自動生成の論文一覧（34本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure](2026-2602.23036-llmservingsim-2-heterogeneous-disaggregated-simulator.md)**  
  実装：[✓](https://github.com/casys-kaist/LLMServingSim) ・ リポジトリ内被引用：9  
  異種GPU/TPU/PIMと分離サービング・多階層鍵値メモリ・MoE・電力を要求駆動ループで統合模擬するLLMサービングシミュレータ。

- **2026-01 · [AIConfigurator: Lightning-Fast Configuration Optimization for Multi-Framework LLM Serving](2026-2601.06288-aiconfigurator-multi-framework-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  実GPUで測った演算・通信性能から複数のLLMサービング構成をCPU上で予測し、並列化やバッチ、プリフィル・デコード分離を探索して遅延目標を満たす候補を選ぶ。

- **2026-01 · [Revati: Transparent GPU-Free Time-Warp Emulation for LLM Serving](2026-2601.00397-revati-transparent-gpu-free-time-warp-emulation.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  実LLMサーバ制御コードをそのまま走らせ、GPU計算だけ仮想時間へ置換して5%未満の誤差と約5〜17倍の評価高速化を狙うGPU不要エミュレータ。

- **2026-06 · [Frontier: Towards Comprehensive and Accurate LLM Inference Simulation](2026-2605.21312-frontier-comprehensive-accurate-llm-inference-simulation.md)**  
  実装：[✓](https://github.com/NetX-lab/Frontier) ・ リポジトリ内被引用：4  
  分離プリフィル/デコードや注意-FFN分離を役割別イベントグラフとして再現し、演算・通信・KVメモリを実測校正して、現代LLMサービング構成の性能を高精度に予測する。

- **2026-01 · [ScaleSim: Serving Large-Scale Multi-Agent Simulation with Invocation Distance-Based Memory Management](2026-2601.21473-scalesim-serving-large-scale-multi-agent-simulation-with-invocation-dist.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ScaleSimは、多数の大規模言語モデル利用エージェントを同時に動かすシミュレーションにおいて、GPUメモリ上のエージェント固有状態を、次にどのエージェントが言語モデルを呼び出すかというアプリケーション側の予測に基づいて管理する配信システムである。

- **2026-03 · [DyQ-VLA: Dynamic Quantization and Compensation for VLA models with Runtime Error Awareness](2026-2603.07904-dyq-vla-temporal-dynamic-aware-quantization-for-embodied-vision-language.md)**  
  実装：[✓](https://anonymous.4open.science/r/DyQ-VLA-7F51/) ・ リポジトリ内被引用：2  
  DyQ-VLAの2026年10月4日公開の第3版は、量子化によって変わる実行時の行動と誤差の相関を明示的に測り、並進と回転で異なる制御を行う。LIBEROおよびRoboTwin 2.0の評価では、BF16に対する推論単位の速度改善が1.74〜1.81倍、成功した実行全体にわたるモデル推論時間の改善が1.88〜1.93倍となった。

- **2026-06 · [KernelSight-LM: A Kernel-Level LLM Inference Simulator](2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUカーネル予測と実運用サービングの離散事象モデルを統合し、未計測GPUでもカーネル誤差12.1%、対象計測ありで3.8%を達成。

- **2026-05 · [LLM-Emu: Native Runtime Emulation of LLM Inference via Profile-Driven Sampling](2026-2605.00616-llm-emu-native-runtime-emulation.md)**  
  実装：[✓](https://github.com/AKafakA/llm-emu) ・ リポジトリ内被引用：1  
  vLLMの本番HTTP・スケジューラ・KV管理を実コードのまま動かし、GPU順伝播だけを二次元遅延プロファイルからの標本化へ置換して、実GPU比の出力トークン当たり時間・反復時間を4.8%、エンドツーエンド遅延を5.3%、出力スループットを1.9%以内で再現する（初回トークン時間は最大10.41%ずれる）実時間エミュレータ。

- **2026-05 · [EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture](2026-2605.24144-eva-accelerating-llm-decoding-via-an-efficient-vector-quantization-archi.md)**  
  実装：[✓](https://github.com/dbw6/Eva) ・ リポジトリ内被引用：1  
  ベクトル量子化は複数重みを一つの索引にまとめるため2ビット級の圧縮品質に優れる一方、従来の実装では重み索引から符号帳の値を不規則に読み出す。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [ePACT: Energy-Performance-Aware Commitment Tracking for LLM Serving](2026-2610.01784-epact-energy-performance-aware-commitment-tracking-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMサービングの電力を単純に減らすのではなく、事前に契約した時間単位の電力量へ実消費を近づける。要求ごとのサービス期限を予測し、レプリカ数とGPUクロックをオンラインで調整する。

- **2026-09 · [Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash](2026-2609.15636-trillion-parameter-moe-in-a-box-decoupling-memory-provisioning-with-high.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、総パラメータ数が1兆を超える混合専門家モデル（Mixture-of-Experts、MoE）を、多数の要求で負荷を平準化するクラスタではなく、同時要求数1〜8程度の単一装置で動かす場合のメモリ設計を検討する。

- **2026-09 · [Characterizing High Bandwidth Flash for LLM Serving](2026-2609.39131-characterizing-high-bandwidth-flash-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らはHBM、HBF、ホストDRAM、SSDの四階層にまたがる配置方針と、キャッシュ再利用を優先しながら新規要求の受入れを制限するスケジューラを設計する。B200相当の計算モデルとHBFの仮定仕様を用いた結果、評価した負荷条件で処理完了時間を36.1〜87.7%短縮する構成があり、モデル化したエネルギー削減率は最大59.1%に達する。

- **2026-08 · [Simthesizer: An Agent-Driven Simulation Framework for LLM Serving Systems](2026-2608.24650-simthesizer-an-agent-driven-simulation-framework-for-llm-serving-systems.md)**  
  実装：[✓](https://github.com/casys-kaist/Simthesizer) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論提供では、連続的なバッチ形成、入力処理と生成の分離、KVキャッシュの退避、投機的復号、専門家混合（MoE）、複数回のモデル呼出しを含むエージェント処理など、複雑な機構が急速に増えている。

- **2026-08 · [BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge](2026-2608.05926-balance-hybrid-autoregressive-speculative-llm-inference-at-the-network-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（SD）は小規模言語モデル（SLM）が複数トークンを提案し、LLMがまとめて検証するため遅延を下げられる一方、LLMとSLM双方の重み、両方式のKVキャッシュ、複数トークンの検証に必要なメモリがGPUに載る。

- **2026-06 · [Characterizing How Complex Agentic AI Systems Handle General Tasks: A Trace-Based Simulation Study](2026-2606.01725-characterizing-how-complex-agentic-ai-systems-handle-general-tasks-a-tra.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.22133686) ・ リポジトリ内被引用：0  
  さらに既存のLLMサービングシミュレータVidurを拡張したVidur-Agentへトレースを入力し、GPU配分、接頭辞キャッシュ（prefix キャッシュ）、事前充填と復号の分離、要求の処理順を変えてタスク完了時間を比較する。

- **2026-05 · [BAGEN: Are LLM Agents Budget-Aware?](2026-2606.00198-bagen-are-llm-agents-budget-aware.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の評価では、タスクの成否と終了後の消費トークン数を記録するが、実行途中のエージェント自身が残りの必要予算を理解していたかは別問題である。BAGEN（Budget-Aware Agent）は、残予算の自己推定を独立した能力として定義し、途中状態ごとに「完了に必要な資源の下限・上限」または「完了不可能」を回答させる評価枠組みを提案する。

- **2026-04 · [RouteNLP: Closed-Loop LLM Routing with Conformal Cascading and Distillation Co-Optimization](2026-2604.23577-routenlp-closed-loop-llm-routing-with-conformal-cascading-and-distillati.md)**  
  実装：[✓](https://github.com/bettyguo/RouteNLP) ・ リポジトリ内被引用：0  
  提案方式は、タスク条件付きの難易度予測器、共形リスク制御で初期化した品質確認付きの段階的移行、失敗した問い合わせを分類して小型モデルを再蒸留する閉ループという三つの機構を連結する。8週間・1日約5,000件の顧客サービス試験運用では、費用58%削減、専門家による応答受理率91%を報告した。

- **2026-02 · [TOM: A Ternary Read-only Memory Accelerator for LLM-powered Edge Intelligence](2026-2602.20662-tom-a-ternary-read-only-memory-accelerator-for-llm-powered-edge-intellig.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TOMは、三値重み（ternary 重み）を持つ大規模言語モデル（LLM）をエッジ端末で低遅延・低消費電力に動かすための、読出し専用メモリ（ROM）と静的ランダムアクセスメモリ（SRAM）の混合専用回路である。重みを毎トークン外部メモリから転送する方式と異なり、固定ベースモデルの重みをROMとしてオンチップへ焼き込み、各演算器の近くに分散配置する。

- **2026-02 · [Harmonia: Algorithm-Hardware Co-Design for Memory- and Compute-Efficient BFP-based LLM Inference](2026-2602.04595-harmonia-algorithm-hardware-co-design-for-memory-and-compute-efficient-b.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論ではモデル重みだけでなく、各層で生じる活性化と、長い入力履歴を保持する鍵・値キャッシュ（KVキャッシュ）がメモリ容量・帯域・演算器の面積を消費する。重みだけを4ビット整数へ量子化しても、活性化がFP16のままでは浮動小数点と整数の混合積和演算を処理する回路が必要になる。

- **2026-02 · [Asynchronous Verified Semantic Caching for Tiered LLM Architectures](2026-2602.13165-asynchronous-verified-semantic-caching-for-tiered-llm-architectures.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者は、事前に人手や大規模モデルで検証した回答を持つ静的キャッシュと、通常の要求を処理しながら生成回答を保存する動的キャッシュを分離する構成を前提とする。原著のトレース駆動シミュレーションでは、会話要求における静的由来回答の割合が8.2%から19.4%、検索要求では2.2%から8.6%へ増えた。

- **2026-01 · [Mugi: Value Level Parallelism For Efficient LLMs](2026-2601.10823-mugi-value-level-parallelism-for-efficient-llms.md)**  
  実装：[✓](https://zenodo.org/records/18063514) ・ リポジトリ内被引用：0  
  Mugiは、値レベル並列性（Value Level Parallelism; VLP）という、数値が一致する複数の演算に対して中間結果を共有するハードウェア方式を、LLMの推論へ適用した研究である。

- **2025-11 · [Multiplexed Heterogeneous LLM Serving via Stage-Aligned Parallelism](2025-832f2fc32711-multiplexed-heterogeneous-llm-serving-via-stage-aligned-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ParaFlexは、規模や必要メモリが異なる複数の大規模言語モデル（LLM）を、同じGPU群上で効率よく同時提供するための推論サービングシステムである。原著は異種モデルの混合負荷で、テンソル並列型の多重化と比べ中央値遅延を最大63%削減、処理量を最大4.7倍に改善し、共有パイプライン型の既存方式に対して処理量を最大1.6倍に改善したと報告する。

### 2年前（2024-11〜2025-10）

- **2024-11 · [APEX: An Extensible and Dynamism-Aware Simulator for Automated Parallel Execution in LLM Serving](2024-2411.17651-apex-an-extensible-and-dynamism-aware-simulator-for-automated-parallel-e.md)**  
  実装：[✓](https://github.com/microsoft/apex_plus) ・ リポジトリ内被引用：10  
  APEXは、大規模言語モデル（LLM）を複数GPUで提供する際に、どの並列化方式を組み合わせるべきかを実機へ総当たりで配備せず、CPU上のシミュレーションで比較するシステムである。

- **2025-07 · [Rethinking LLM Inference Bottlenecks: Insights from Latent Attention and Mixture-of-Experts](2025-2507.15465-rethinking-llm-inference-bottlenecks-insights-from-latent-attention-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  従来の大規模言語モデルでは、多頭注意（multi-head 注意機構、MHA）の復号時演算は過去の鍵・値キャッシュを大量に読み出すため、メモリ帯域が主要な制約と考えられてきた。

- **2025-07 · [Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations](2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference.md)**  
  実装：[✓](https://github.com/ozcanmiraay/vidur-energy) ・ リポジトリ内被引用：3  
  LLMの推論基盤は、要求到着率、入力と出力の長さ、バッチ編成、モデル並列方式によってGPUの使用状況が大きく変わる。A100上のCodeLlama-34Bの並列構成比較では、平均GPU電力213.2～355.3W、総エネルギー0.16～0.56kWhと構成によって大きく変わる。

- **2025-03 · [Improving the End-to-End Efficiency of Offline Inference for Multi-LLM Applications Based on Sampling and Simulation](2025-2503.16893-improving-the-end-to-end-efficiency-of-offline-inference-for-multi-llm-a.md)**  
  実装：[✓](https://github.com/puddingfjz/vllm) ・ リポジトリ内被引用：3  
  本研究が対象とするのは、あらかじめ処理する要求集合が分かっているオフライン推論であり、複数の大規模言語モデル（LLM）を一つのアプリケーション内で使う状況である。単一モデルの要求順序を最適化するだけでは、モデル間のGPU分配を決められない。SamuLLMはこれらを一つの計画問題として扱う。

- **2024-11 · [DeeR-VLA: Dynamic Inference of Multimodal Large Language Models for Efficient Robot Execution](2024-2411.02359-deer-vla-dynamic-inference-of-multimodal-large-language-models-for-effic.md)**  
  実装：[✓](https://github.com/yueyang130/DeeR-VLA) ・ リポジトリ内被引用：3  
  DeeR-VLA（動的 Early-Exit for Robotic Multimodal Large Language Models）は、画像と自然言語の指示からロボットの行動を決める視覚・言語・行動モデルに、複数の中間出口（early exit）を設ける推論時の計算資源配分方式である。

### 3年前（2023-11〜2024-10）

- **2024-05 · [Vidur: A Large-Scale Simulation Framework For LLM Inference](2024-2405.05465-vidur-a-large-scale-simulation-framework-for-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/vidur) ・ リポジトリ内被引用：31  
  Vidurは、大規模言語モデル（LLM）をどのGPUに何台配置し、どの並列化方式・バッチ化方式で処理するかを、候補ごとに実機で運転せず比較するためのシミュレータである。LLaMA2-7B/70B、InternLM-20B、Qwen-72Bを使った実機比較では、オンライン負荷での正規化要求遅延の誤差は最大でも9%未満と報告される。

- **2024-08 · [LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale](2024-2408.05499-llmservingsim-a-hw-sw-co-simulation-infrastructure-for-llm-inference-ser.md)**  
  実装：[✓](https://github.com/casys-kaist/llmservingsim) ・ リポジトリ内被引用：10  
  大規模言語モデルの推論基盤では、GPUや専用演算器の設計だけでなく、到着する要求の分布、バッチ化、KVキャッシュ管理、複数装置へのモデル分割が性能を左右する。論文は実GPU上の推論基盤に対する性能傾向の誤差を平均14.7%程度に抑え、既存の演算器シミュレータに対して34.7〜491倍の高速化を報告する。

- **2024-09 · [TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation](2024-2409.12514-tinyvla-towards-fast-data-efficient-vision-language-action-models-for-ro.md)**  
  実装：[✓](https://github.com/liyaxuanliyaxuan/TinyVLA) ・ リポジトリ内被引用：5  
  提案手法は、画像・言語の意味理解を約4.2億〜13億パラメータの小型マルチモーダル基盤モデルへ、連続行動の生成を拡散方策（diffusion policy）復号器へ分担させる。実機のFranka単腕ロボット5タスクでは、最大構成TinyVLA-Hの平均成功率が94.0%、OpenVLAが68.3%であり、差は25.7パーセントポイントだった。

- **2024-06 · [Demystifying AI Platform Design for Distributed Inference of Next-Generation LLM models](2024-2406.01698-demystifying-ai-platform-design-for-distributed-inference-of-next-generation-llm-models.md)**  
  実装：[✓](https://github.com/abhibambhaniya/GenZ-LLM-Analyzer) ・ リポジトリ内被引用：4  
  演算子-level ルーフラインと集合通信通信モデルでLLM構造・推論提供最適化・分散方式からcompute/メモリ/ネットワーク要件を逆算するGenZ。

### 4年前（2022-11〜2023-10）

- **2023-10 · [Sia: Heterogeneity-aware, goodput-optimized ML-cluster scheduling](2023-2c2071afa90d-sia-heterogeneity-aware-goodput-optimized-ml-cluster-scheduling.md)**  
  実装：[✓](https://github.com/siasosp23/artifacts) ・ リポジトリ内被引用：2  
  Siaは、GPUの種類が混在する深層学習訓練クラスタで、各ジョブへ割り当てるGPUの種類・台数・バッチサイズを同時に決めるスケジューラである。原著は、44GPUの実機クラスタで既存のPolluxより平均ジョブ完了時間を約35〜50%、Gavelより約50%短縮したと報告する。

### 7年前（2019-11〜2020-10）

- **2020-02 · [A3: Accelerating Attention Mechanisms in Neural Networks with Approximation](2020-2002.10941-a3-accelerating-attention-mechanisms-in-neural-networks-with-approximati.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  通常の注意機構は、クエリベクトルと全キー行の内積を求め、softmaxで正規化し、値ベクトルを重み付き合成する。保守的設定は近似によるタスク精度の低下をおおむね1%に抑える一方、積極的設定はおおむね8%の精度低下を伴う。

### 9年前（2017-11〜2018-10）

- **2017-12 · [Ray: A Distributed Framework for Emerging AI Applications](2017-1712.05889-ray-a-distributed-framework-for-emerging-ai-applications.md)**  
  実装：[✓](https://github.com/ray-project/ray) ・ リポジトリ内被引用：8  
  Rayは、強化学習で頻繁に現れる「多数の環境を並列に動かす」「学習器で方策を更新する」「更新した方策を低遅延で実行する」という異質な仕事を、別々の分散基盤へ切り分けずに一つの実行系へ載せるための研究である。提案の中核は、状態を持たない遠隔関数を「タスク」、状態を保持する遠隔オブジェクトを「アクター」として同じ動的依存グラフへ埋め込むことである。
<!-- survey:auto:end -->
