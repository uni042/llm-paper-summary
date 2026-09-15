# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（182本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [Continnum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](2025-2511.02230-continuum-agent-kv-cache-ttl-scheduling.md)**  
  実装：[✓](https://github.com/Hanchenli/vllm-continuum) ・ リポジトリ内被引用：17  
  ツール呼出しを挟む多ターンLLMエージェントで、ツール待ち時間・KV再構築費用・残りターンを見てKVキャッシュの保持期限を動的に決め、短い待ちではGPUに固定し長い待ちでは解放してターン間待ちを減らすスケジューラ。

- **2025-12 · [TraCT: Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale](2025-2512.18194-tract-rack-scale-cxl-shared-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  CXL Type-3共有メモリをプリフィル・デコード間KV転送路とラック共有接頭辞キャッシュに兼用し、GPU–CXL直接DMAでRDMAのNICホップを除去するサービング方式。

- **2026-09 · [GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving](2025-2508.16449-greenllm-slo-aware-dvfs-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  GreenLLMは、プリフィルとデコードの負荷を入力長・出力TPS・P95トークン間時間から観測し、各段階のSLO内でGPU周波数を別々に選ぶ二重帰還制御により、過剰な高周波数動作とエネルギーを減らす。

- **2026-07 · [AugServe: Adaptive Request Scheduling for Augmented Large Language Model Inference Serving](2025-2512.04013-augserve-adaptive-request-scheduling-augmented-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  外部APIや検索を待つ拡張LLMで、停止・再開状態、出力長・外部呼出し時間、KV保持・退避・再計算費用を観測して要求順位と反復トークン予算を変え、先頭待ちとGPUメモリ圧迫を減らすスケジューラ。

- **2026-04 · [Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter](2026-2604.15039-prefill-as-a-service-cross-datacenter-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KVキャッシュ量が小さいハイブリッド注意機構を利用し、長い未キャッシュ入力のプリフィルだけを遠隔GPU群へ振り分け、KVをデータセンター間転送して異種GPU資源の利用効率と処理能力を高める。

- **2026-03 · [Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving](2026-2603.18897-paste-pattern-aware-speculative-tool-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  反復する道具系列と引数依存から次の具体的な道具呼出しを先行実行し、言語モデル側の混雑も共同制御して平均タスク完了時間を最大43.5%削減する。

- **2026-03 · [Not All Prefills Are Equal: PPD Disaggregation for Multi-turn LLM Serving](2026-2603.13358-ppd-disaggregation-multiturn-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  複数ターン会話の2ターン目以降について、既存鍵値キャッシュを持つデコードGPUで追加プリフィルするか従来どおりプリフィルGPUへ送るかを遅延目標ごとに動的選択し、後続ターンの初トークン待ち時間と鍵値転送量を大幅に削減する。

- **2026-01 · [Concur: Proactive Agent-Level Admission Control for Efficient Agentic Batch Inference](2026-2601.22705-concur-agentic-admission-control.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  非同期エージェントのKV接頭辞がLRU追い出しと再計算を繰り返す中盤スラッシングを、KV使用率・ヒット率を混雑信号にしたエージェント単位の加算増加・乗算減少型受入れ制御で未然に抑える方式。

- **2026-02 · [Efficient Multi-round LLM Inference over Disaggregated Serving](2026-2602.14516-ampd-multi-round-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多ラウンド推論の追加プリフィルを、実行時負荷に応じてデコード側の局所実行かプリフィル側の遠隔実行へ振り分け、待ち行列の並べ替えとGPU配備計画を組み合わせてSLO達成率を高める分離サービング方式。

- **2026-01 · [A Universal Load Balancing Principle and Its Application to Large Language Model Serving](2026-2601.17855-universal-load-balancing-principle-llm-serving.md)**  
  実装：[✓](https://github.com/Echoscd/Load-Balancing-Release) ・ リポジトリ内被引用：3  
  同期障壁で最遅GPUに全体が律速されるデータ並列デコードを、短期先読み付き整数最適化BF-IOで割り当て直し、256基A100相当のシミュレーションでFCFS比スループット約92%向上・エネルギー約29%削減を示す。

- **2026-05 · [AlignedServe: Orchestrating Prefix-aware Batching to Build a High-throughput and Computing-efficient LLM Serving System](2026-2605.23389-alignedserve-prefix-aware-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AlignedServeは、長いKV系列を分離するため要求をCPU KVプールへ置き、接頭辞長が近い要求を四分木から密度優先で集め、次バッチのKVをGPU間へ先読みして反復内の待ちと転送待ちを減らす。

- **2026-02 · [vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models](2026-2602.02204-vllm-omni-fully-disaggregated-multimodal-serving.md)**  
  実装：[✓](https://github.com/vllm-project/vllm-omni) ・ リポジトリ内被引用：2  
  複数LLM・拡散モデル・音声/画像生成器を段階グラフへ分解し、各段階を独立バッチ・独立GPU配置・共通コネクタで実行することで、any-to-any型マルチモーダル推論を単一モデル用サービング基盤から拡張する方式。

- **2026-02 · [OServe: Accelerating LLM Serving via Spatial-Temporal Workload Orchestration](2026-2602.12151-oserve-spatial-temporal-workload-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/LiveServe_Documents-1F54/) ・ リポジトリ内被引用：2  
  要求長の空間的ばらつきと時間変動を予測し、レプリカごとに異なるGPU数・並列方式と要求割当を最大流で共同最適化し、重み再利用による高速配置切替で追随するLLMサービング方式。

- **2026-02 · [DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS](2026-2602.18755-biscale-phase-aware-placement-dvfs.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DualScaleは、プリフィル・デコード分離のGPU台数・並列度・周波数・振り分け比率を数分単位で配置し、プリフィルの将来待ち行列とデコードのTPOT余裕を反復ごとに制御してSLO内の電力を減らす二段階方式。

- **2026-08 · [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](2026-2608.25523-topas-workflow-aware-prefix-state-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェント接頭辞KVの常駐と要求投入を共有GPUメモリ下で共同決定し、DAGの残存クリティカルパス、将来再利用、移動・プリエンプト費用を比較してタスク完了時間を短縮する。

- **2026-07 · [SMetric: Rethink LLM Scheduling for Serving Agents with Balanced Session-centric Scheduling](2026-2607.08565-smetric-session-centric-agent-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  セッションの初回だけ負荷分散し、後続要求はKV局所性を優先しつつ過負荷・キャッシュ消失時だけ再配置することで、エージェント配信のクラスタTPSを10〜16%改善する。

- **2026-07 · [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル中に重要KVだけを先送りし、デコード時は不足分をローカル読出しと並列取得、残りを背景転送へ回して、全量転送の待ちと部分転送の後続停止を減らす。

- **2026-07 · [ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving](2026-2607.00466-eldr-expert-locality-decode-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル時のMoEエキスパート活性化から署名を作り、似た署名の要求を同じデコードGPUへ集めて一括読込する専門家重みの種類を減らし、TPOTのばらつきを抑える。

- **2026-06 · [ReMP: Low-Downtime Runtime Model-Parallelism Reconfiguration for LLM Serving](2026-2606.18741-remp-runtime-model-parallelism-reconfiguration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TP/PP切替で重み・KV・通信群・ワーカーを作り直す代わりに、CPU共有重み、二次元KV移送、事前生成通信状態、待機ワーカーを再利用し、数秒で並列構成を変更できるLLMサービング方式。

- **2026-06 · [Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice](2026-2606.22327-geometry-aware-online-scheduling.md)**  
  実装：[✓](https://github.com/Aurora-Kl/Geometry-Aware-Online-Scheduling) ・ リポジトリ内被引用：1  
  出力長とプロンプト長からKVメモリ占有の時間積分を見積もり、小さいメモリ時間体積の要求を先に実行するSVFを比較して、SJFが無視するKV容量起因の先頭待ちを減らす。

- **2026-06 · [Fairness-Aware and Latency-Controllable Scheduling for Chunked-Prefill LLM Serving](2026-2606.09061-fairness-latency-chunked-prefill-scheduling.md)**  
  実装：[✓](https://github.com/Charmstok/Chunked_Prefill_Serving) ・ リポジトリ内被引用：1  
  待ち時間と残りプリフィル量で処理順を更新し、遅延予測でチャンク量を目標時間へ合わせ、同時プリフィル数も制限することで、分割プリフィル配信の公平性と裾遅延を改善する。

- **2026-06 · [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低頻度MoEモデルの大きなFFN重みを重みGPUへ、変動するKVキャッシュを共有KV GPUへ分離し、モデル間で余剰HBMを融通して長文脈の容量不足とKV競合を減らす。

- **2026-05 · [STAR: Decode-Phase Rescheduling for LLM Inference](2026-2510.13668-star-decode-phase-rescheduling-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル・デコード分離後も変動する生成長を最終層の隠れ状態から軽量MLPで継続予測し、KV移送費を回収できる要求を過負荷GPUから低負荷GPUへ移して、長出力の負荷偏りと尾部遅延を減らす再配置機構。

- **2026-05 · [RTP-LLM: High-Performance Alibaba LLM Inference Engine](2026-2605.29639-rtp-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  実運用LLM基盤で、要求をKV位置とGPU負荷に応じて振り分け、プリフィル/デコードを分離し、GPU〜分散ストレージのKV階層・高速読込・投機的復号を統合して待ち時間と容量負荷を減らす。

- **2026-05 · [Nitsum: Serving Tiered LLM Requests with Adaptive Tensor Parallelism](2026-2605.05467-nitsum-adaptive-tensor-parallelism-tiered-slo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  多階層SLOの負荷変動に応じてテンソル並列度、プリフィル/デコードGPU配分、要求スケジューリングを同時に切り替え、重み再読込不要化と高速KV移行で再構成をミリ秒級に抑えるLLMサービング方式。

- **2026-05 · [FATE: Future-State-Aware Scheduling for Heterogeneous LLM Workflows](2026-2605.07238-fate-future-state-aware-workflow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  現在のGPU負荷だけでなく、配置後に残るモデル常駐・親出力局所性・接頭辞再利用を有限先読みで評価し、ワークフローDAGの次段階に有利な状態を残すスケジューラ。

- **2026-05 · [Coral: Cost-Efficient Multi-LLM Serving over Heterogeneous Cloud GPUs](2026-2605.04357-coral-multi-llm-heterogeneous-cloud-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異種GPU上のモデル内部配置をオフラインの配信テンプレートへ落とし、オンラインでは全モデルの需要・価格・在庫を共同割当することで、費用を最大2.79倍削減し資源逼迫時の有効スループットを最大2.39倍高める。

- **2026-05 · [A Policy-Driven Runtime Layer for Agentic LLM Serving](2026-2605.27744-policy-driven-runtime-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェント識別子を共通座標に観測・採点・予測・作用を推論基盤へ挿入し、オンライン遷移学習を鍵値追い出しと先読みに使ってヒット率と遅延を改善する。

- **2026-04 · [TENT: A Declarative Slice Spraying Engine for Performant and Resilient Data Movement in Disaggregated LLM Serving](2026-2604.00368-tent-declarative-slice-spraying-data-movement.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：1  
  KVキャッシュなどの大容量転送を細粒度スライスへ分け、実時間の混雑や障害に応じてRDMA・NVLink等の複数経路へ動的分散し、分離型LLMサービングの帯域利用と障害回復を改善する転送基盤。

- **2026-04 · [Foundry: Template-Based CUDA Graph Context Materialization for Fast LLM Serving Cold Start](2026-2604.06664-foundry-cuda-graph-context-materialization.md)**  
  実装：[✓](https://github.com/foundry-org/foundry) ・ リポジトリ内被引用：1  
  CUDAグラフの仮想アドレス配置とカーネルバイナリまで保存し、少数の構造テンプレートから再構築することで、LLMサービングの起動時グラフ捕捉を数分から数秒へ短縮する方式。

- **2026-03 · [SageSched: Efficient LLM Scheduling Confronting Demand Uncertainty and Hybridity](2026-2603.07917-sagesched-demand-uncertainty-hybrid-cost-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  類似プロンプトの履歴から出力長分布を学習なしで推定し、入力長と出力長から計算・KVキャッシュ費用を統合、Gittins指数で不確実性込みの優先順位を決めるLLMスケジューラ。平均TTLTを最大28.7%以上改善する。

- **2026-03 · [MoEless: Efficient MoE LLM Serving via Serverless Computing](2026-2603.06350-moeless-serverless-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散MoE推論で次の層のエキスパート負荷を予測し、混雑するエキスパートだけを一時複製して複数GPUへ配置し、ルータを変えずに同期点での最遅GPU待ちを減らすサーバーレス提供システム。

- **2026-03 · [Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective](2026-2603.16104-helium-workflow-aware-agent-serving.md)**  
  実装：[✓](https://github.com/mlsys-io/helium_demo) ・ リポジトリ内被引用：1  
  エージェントワークフローを問い合わせ計画として解析し、共通部分削除、結果・KVの先行キャッシュ、接頭辞構造を見た費用認識スケジューリングを統合して、KVFlow比最大1.56倍、複合Tradingで最大1.34倍高速化する。

- **2026-02 · [PrefillShare: A Shared Prefill Module for KV Reuse in Multi-LLM Disaggregated Serving](2026-2602.12029-prefillshare-shared-prefill-multi-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数LLMが同じ文脈を別々にプリフィルする重複を、凍結共有プリフィル＋KV条件付き追加学習でモデル横断共有し、エージェント処理の尾遅延とKVメモリを削減する。

- **2026-02 · [Large-Scale LLM Inference with Heterogeneous Workloads: Prefill-Decode Contention and Asymptotically Optimal Control](2026-2602.02987-prefill-decode-contention-optimal-control.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模LLM推論で異なる入力・出力長の要求を混在処理する際、実測反復時間からプリフィル混在/デコード単独のサービス率を求め、流体最適化の占有率に追従してプリフィル受入れとデコード配置をゲート・ルート制御する研究。

- **2026-02 · [FLYING SERVING: On-the-Fly Parallelism Switching for Large Language Model Serving](2026-2602.22593-flying-serving-online-dp-tp-switching.md)**  
  実装：[✓](https://github.com/Picomp-lab/Flying-Serving) ・ リポジトリ内被引用：1  
  同じGPU常駐重みとKV物理プールをゼロコピーの論理ビューでDP↔TP切替し、15msのオンライン再構成で高負荷時のDP処理量と低負荷・長文時のTP遅延/容量を使い分ける方式。

- **2026-02 · [FlowPrefill: Decoupling Preemption from Prefill Scheduling Granularity to Mitigate Head-of-Line Blocking in LLM Serving](2026-2602.16603-flowprefill-operator-level-preemption.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  演算子境界で事前充填を協調的に割り込み、イベント駆動のSLOスケジューリングと組み合わせて長い要求の先頭待ちを抑え、有効処理量を高める。

- **2026-01 · [Towards Resiliency in Large Language Model Serving with KevlarFlow](2026-2601.22438-kevlarflow-resilient-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  故障したパイプライン段だけを健全ノードへ動的に差し替え、KVキャッシュを背景複製して処理中要求を継続するLLM配信耐障害化。A10の8/16台クラスタで復旧時間を約30秒まで短縮し、故障時TTFTを最大574.6倍改善。

- **2026-01 · [Power Aware Dynamic Reallocation For Inference](2026-2601.12241-rapid-power-aware-dynamic-reallocation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル・デコード分離環境でGPU台数だけでなく電力上限も段階間で再配分し、待ち行列とTTFT/TPOTを見ながら電力移動→GPU役割変更の順でSLO達成率を維持するRAPIDを実機評価する。

- **2025-12 · [WarmServe: Enabling One-for-Many GPU Prewarming for Multi-LLM Serving](2025-2512.09472-warmserve-one-for-many-gpu-prewarming.md)**  
  実装：[✓](https://github.com/LLMServe/WarmServe) ・ リポジトリ内被引用：1  
  将来負荷を予測して複数モデル重みを同じGPU群へ先行配置し、解放前GPUの未使用KV領域とCUDA仮想メモリ再対応付けを使って、冷間起動を隠しながら本番推論時はGPUを専有させる複数LLM配信方式。

- **2025-12 · [Reliable and Resilient Collective Communication Library for LLM Training and Serving](2025-2512.25059-r2ccl-resilient-collective-serving.md)**  
  実装：[✓](https://github.com/r2cc-project/R-2CCL) ・ リポジトリ内被引用：1  
  NIC障害時に通信器を再起動せず接続を別NICへ移し、残存帯域に合わせてcollectiveを再配置する耐障害通信ライブラリ。学習1%未満・推論3%未満の障害時オーバーヘッドを報告。

- **2025-12 · [CascadeInfer: Length-Aware Scheduling of LLM Serving with Low Latency and Load Balancing](2025-2512.19179-l4-length-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  系列長が近い要求を同じGPU段へ集め、生成で長くなった要求をKVごと後段へ移すスケジューラ。実行時の境界補正と分散負荷再均衡で偏りも抑え、16 GPU評価で主要比較対象より処理率とSLO達成率を改善する。

- **2025-11 · [FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs](2025-2511.00807-freesh-fair-resource-energy-efficient-scheduling.md)**  
  実装：[✓](https://github.com/AndrewFangZequan/LLM_Serving_FREESH) ・ リポジトリ内被引用：1  
  地域別炭素強度と異種GPU特性を使った30分単位の資源配置、1秒単位の動的周波数制御、要求単位の最小余裕時間優先を組み合わせ、エネルギー28.6%・炭素排出45.45%を削減する分散LLMサービング方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Topology-Aware Data Movement for Disaggregated GPU Inference](2026-2607.28633-topology-aware-data-movement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間のNVLink・PCIe・RDMA・TCP接続を調べてKV転送経路を選び、層計算へ重ねる方式とCXL容量階層を解析し、分離推論の転送待ちとHBM容量制約を減らす。

- **2026-09 · [Phase-Decoupled, Model-Calibrated Power Control for Disaggregated LLM Serving](2026-2609.11133-phase-decoupled-model-calibrated-power-control-for-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離サービングのプリフィルには校正済みSMクロック窓、デコードには性能崖直上の電力上限を使い分け、B200実機でMax-Qより高いエネルギー効率と良好な遅延を両立する。

- **2026-09 · [OUTLETS: Output-Length Prediction from Speculative Decoding Backbones](2026-2609.01068-outlets-output-length-prediction-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的デコードのドラフト表現から残り出力長を予測し、短く終わる要求をキュー順序とワーカー割当で先に進めて、長い要求による先頭待ちとP99遅延を減らす。

- **2026-09 · [MeanField Surrogate Modeling for Scalable Runtime Scheduling of Concurrent Heterogeneous AI Inference on Shared GPUs](2026-2609.02109-meanfield-surrogate-runtime-scheduling-shared-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有GPU上の異種LLM/視覚推論で、各モデルの局所構成＋集約GPU状態から性能を予測する平均場代理モデルにより、プロファイル数を実測で約20Nへ抑えつつ5モデル78,732構成を26msで近似探索する。

- **2026-09 · [Latency-Aware Orchestration for Multi-Agent LLM Workflows on Heterogeneous GPUs](2026-2609.03335-latency-aware-multi-agent-orchestration-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  依存するエージェント処理グラフから近接後続を先読みし、モデルの常駐・読込・解放と異種GPU配置・実行順を共同で決めて、モデル待ちと不要なGPU占有を減らす。

- **2026-09 · [HeatCache: Thermal-aware Energy-efficient LLM Inference Scheduling for Chassis-level Liquid Cooling in Sustainable Edge Server Rooms](2026-2609.12449-heatcache-thermal-aware-energy-efficient-llm-inference-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeatCacheはAIO液冷ループの残存熱容量を熱予算として推定し、ジョブ別の発熱予測とTTFT/TPOT制約を使ってvLLMのバッチ・GPU割当・周波数を再順位付けする。48℃級の実機環境で計算エネルギーを最大18.0%削減し、熱スロットリング曝露を大幅に抑える。

- **2026-09 · [ExaServe: Large-Scale LLM Serving on Exascale HPC Systems](2026-2609.10812-exaserve-large-scale-llm-serving-exascale-hpc-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エクサスケールHPC向けLLM推論展開を設定ファイルから自動化し、Aurora 256ノード・3072レプリカまで拡張して、中央ストリーミング配信とRay制御面が先に限界へ達することを実測した。

- **2026-09 · [Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs](2026-2609.11562-entwine-tiled-computation-fine-grained-gpu-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力タイルの生成順序・タイル単位通信・共有SM上の通信並列度を協調し、テンソル並列GEMMとReduceScatterの通信尾を抑える計算通信重畳方式。

- **2026-09 · [Energy-Efficient LLM Serving via Disaggregated Attention--FFN and Flexible Frequency Scaling](2026-2608.01891-aflex-attention-ffn-disaggregation-frequency-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構とFFNを別GPU群へ分け、遅延・エネルギー予測から数分単位の配置と要求ごとの周波数を選び、適応バッチ化と増分再配置でSLO内の電力と分離空きを減らす。

- **2026-09 · [Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows](2026-2609.10964-decoupling-readiness-from-release-tail-aware-agentic-llm-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント型LLMワークフローで準備完了ターンの即時投入をやめ、尾部リスク/推定仕事量による優先度と適応投入予算でP95完了時間を最大3.50倍改善するスケジューリング方式。

- **2026-09 · [Deadline-Aware Adaptive Prefill Chunking for Efficient Large Language Model Serving](2026-2609.07883-deadline-aware-adaptive-prefill-chunking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  デコード要求の次トークン期限から残り時間を求め、期限内に入る最大プリフィル塊を反復ごとに二分探索して、固定分割の起動費と一括処理のデコード停止を減らす。

- **2026-09 · [Analytical Resource Management for Fine-grained MoE Computation-Communication Overlap](2026-2609.07536-moe-overlap-resource-manager.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力長とMoE専門家へのトークン偏りから通信タイルへ予約するGPU資源を解析的に選び、計算と通信の重なりを調整して固定配分よりプリフィル待ちを減らす。

- **2026-09 · [AInfer-PD: Communication-Safe In-Place Prefill-Decode Multiplexing for Distributed MoE Rollouts](2026-2609.00993-ainfer-pd-communication-safe-prefill-decode-multiplexing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散MoEロールアウトでプリフィルとデコードを同一GPU群へ安全に同居させ、競合する集合通信だけを順序付ける方式。8×H20-3Eで通常AInfer比の総処理時間を最大22.5%、16GPUで最大35.3%削減した。

- **2026-09 · [Adaptive Context Parallelism for Production LLM Serving](2026-2609.04774-vertumnus-adaptive-context-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  接頭辞キャッシュ後の残計算量とワーカー混雑を測り、要求ごとの文脈並列度とクラスタのCP分割・統合を数秒単位で変えて、短文の通信費と長文の計算待ちを減らす。

- **2026-08 · [When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference](2026-2608.03741-heteropanacea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル/デコードと注意/FFNを最大4段へ分離するシミュレータで、計算性能・メモリ帯域・通信費の異なる装置配置を比較し、分離が有利な資源条件を測定する研究。

- **2026-08 · [TokTier: Exact Stateful CPU+GPU Tokenization for Agentic LLM Serving](2026-2607.29678-toktier-stateful-agentic-tokenization.md)**  
  実装：[✓](https://github.com/asu-idi/toktier) ・ リポジトリ内被引用：0  
  長いエージェント会話の追記境界だけを安全検証付きで再トークン化し、再利用不能な大規模入力は厳密GPU経路へ送る方式。参照トークン列との一致を保ちつつ、vLLM統合で中央値TTFTを16〜34%削減する。

- **2026-08 · [TensorCast: The Missing Tensor Management Layer in Large Language Model Infrastructure](2026-2608.06007-tensorcast-tensor-as-a-service.md)**  
  実装：[✓](https://github.com/tensorcast-ai/tensorcast) ・ リポジトリ内被引用：0  
  モデル重み・KV・チェックポイントをArtifact/Operation/Planとして統一管理し、配置・移動・変換・実体化を実行エンジンから分離することで、個別専用基盤に近い性能と横断的な状態管理方針の合成を両立する分散テンソル基盤。

- **2026-08 · [Q-First: Most of Attention Needs Only the Query in Disaggregated LLM Decoding](2026-2608.15473-q-first-disaggregated-decoding.md)**  
  実装：[✓](https://github.com/fan-wenjie/qfirst) ・ リポジトリ内被引用：0  
  KV走査に必要なのはクエリだけだと利用し、クエリを半層早く送ってKV走査と全結合処理を重ねる。既存カーネルで厳密合成でき、Qwen3では学習時の攪乱が測定分解能以下だった。

- **2026-08 · [Pallas: A Proactive KV Cache Migration Framework for LLM Inference in AI-RAN](2026-2608.16477-pallas-proactive-kv-cache-migration-ai-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハンドオーバー時刻を予測し、古いKVは移動先で再計算しつつ新しく増えるKVだけを送信元からストリームして、切替時の全量転送待ちと遠回り生成を減らす。

- **2026-08 · [P-PAS: Prefill-Pressure Adaptive Scheduling for Long-Context LLM Serving](2026-2608.15171-p-pas-prefill-pressure-adaptive-scheduling.md)**  
  実装：[✓](https://github.com/TimoSaemann/ppas-vllm) ・ リポジトリ内被引用：0  
  プリフィルとデコードの同時圧力を観測し、vLLMの1反復トークン予算を低圧力では大きく高圧力では小さく切り替えて、固定分割の競合待ちと過剰な起動費を減らす。

- **2026-08 · [OpScale: Operator-level Provisioning and Autoscaling for LLM Serving](2026-2608.13499-opscale-operator-level-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル全体ではなく演算子単位で供給・配置・実行時伸縮を行い、負荷に応じて現在の律速演算子だけへGPU資源を追加するLLM配信基盤。

- **2026-08 · [LOCAL: Enabling Learning On-device Contiguously for Agent LLMs](2026-2608.15241-local-contiguous-on-device-agent-learning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一24 GB GPUで前景推論を止めずにLoRA学習を進め、アダプタ版を考慮したKV再利用・再計算・退避をスケジューラと協調させる端末向け継続学習ランタイム。

- **2026-08 · [LLMVisor: A Real-Time Latency Attribution Model for Multi-Tenant LLM Serving](2026-2608.08382-llmvisor-realtime-latency-attribution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  処理トークン、文脈長、自己注意の二次項、バッチ規模を使う加法的な区分線形モデルで、共バッチ処理のGPU時間を要求・テナント別へマイクロ秒級で帰属し、VTCより裾誤差を最大4.4倍改善する。

- **2026-08 · [From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems](2026-2608.15127-agentsysbench.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントのLLM呼出しだけでなくツール・検索・サンドボックス・状態・通信を含む実行を測定し、トークン速度だけでは捉えられない待ち時間と資源競合がどこで生じるかを明らかにしたベンチマーク。

- **2026-08 · [Efficiency and Cost Alignment in Batched LLM Serving via Resource-Fair Scheduling](2026-2608.02244-resource-fair-batched-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長短要求を同居させたバッチで短い要求まで最大KV量相当の費用を負担する外部性を定式化し、デコード進捗差を制限するISJLを提案。一般のバッチ幅で競争比3/4を保証し、LMSYS再生ではLJFより最大17%高いスループットと21%低い平均遅延を示す。

- **2026-08 · [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](2026-2608.06557-cascade-slo-aware-latency-budget-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求の残りSLO遅延を実行順とKVのHBM・CPU DRAM・NVMe配置へ共通予算として配り、復元・先読み・保持・再計算を切り替えて、処理量と長文脈要求の公平性を両立するサービング。

- **2026-07 · [X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding](2026-2609.09166-x-cosd-cross-vocabulary-collaborative-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末SLMとサーバLLMの語彙が異なっても、残差分布を共通語彙・LLM専用語彙へ分け、少数の置換候補だけを通信して厳密な協調投機的デコードを行う方式。

- **2026-07 · [Towards Load-Aware Prefill Deflection for Disaggregated LLM Serving](2026-2607.02043-kairos-load-aware-prefill-deflection.md)**  
  実装：[✓](https://github.com/sudokara/Kairos) ・ リポジトリ内被引用：0  
  プリフィルGPUの混雑時にデコードGPUの余力へプリフィルを小分けで差し込み、トークン間時間のSLOを超えない範囲で要求を移して、プリフィル待ちとKV転送を減らす。

- **2026-07 · [SPORK: Self-Speculative Forking to Accelerate Agentic LLM Inference](2026-2607.03333-spork-self-speculative-forking-agentic-llm.md)**  
  実装：[✓](https://github.com/baihuajun24/spork) ・ リポジトリ内被引用：0  
  主LLM自身をprobeとして分岐し、思考生成中に将来のツール呼出しを先行実行することで外部ツール待ちを隠す。GAIAのQwen3-32BでP95遅延を18%削減し、誤予測時は一致した呼出し接頭辞を再利用する。

- **2026-07 · [Sangam: Efficiently Serving Diffusion LLMs with the AR Stack](2026-2607.04206-sangam-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/UT-InfraAI/sangam) ・ リポジトリ内被引用：0  
  拡散LLMの不可分な再プリフィルをデコードの残りトークン予算と繰越不足額で受け入れ、プリフィル混雑時だけデコードGPUへ溢れさせて、待ち時間と資源偏りを抑える。

- **2026-07 · [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長分布のずれを考慮し、プリエンプション損失と未使用HBM損失からKV予約量を求め、GPU構成・要求振り分け・接頭辞キャッシュを再最適化して容量浪費と追い出しを減らす。

- **2026-07 · [Online Linear Programming for Multi-Objective Routing in LLM Serving](2026-2607.03948-online-linear-programming-multi-objective-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各デコードワーカーの将来バッチ枠とKV容量へ影価格を付け、SLO報酬が資源費を上回る要求だけをルーティングして、平均・末尾遅延とスループットの優先順位を切り替える。

- **2026-07 · [OmniPilot: An Uncertainty-Aware LLM Inference Advisor for Heterogeneous GPU Clusters](2026-2607.01579-omnipilot-uncertainty-aware-inference-advisor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU種類・テンソル並列度・精度を実測ベースの不確実性付き費用モデルで順位付けし、未知領域では推薦を控える起動助言器。460実測でスループット誤差6.2%、上位1位正解率95%を示す。

- **2026-07 · [Full-Pipeline Inference Optimization for MiMo-V2.5 Series: Pushing Hybrid SWA Efficiency to the Limit](2026-2607.13095-mimo-hybrid-swa-full-pipeline-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Hybrid SWAの理論的KV削減を本番へ落とすため、Full/SWA二重KVプール、層単位先読み、分散GCache、KV親和ルーティング、プリフィル・デコード・マルチモーダル処理を一体最適化する。

- **2026-07 · [Efficient and Privacy Aware Edge Cloud Collaborative Inference for Large Language Models](2026-2607.13093-privacy-aware-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原文を送らず、端末にKV認可・軽量投機・低次元出力層を残し、クラウドの重いデコーダと協調する分割推論。H20＋3種端末で素朴な分割推論比の遅延最大46.1%、下り通信最大67.4%削減を報告する。

- **2026-07 · [DeltaServe: Host-Agnostic Co-Serving of Inference and Fine-Tuning for LLMs](2026-2607.28848-deltaserve-inference-finetuning-coserving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRA微調整の順伝播を既存推論バッチへSLO予算内で混ぜ、逆伝播を層境界でプリエンプト可能な別プロセスへ分離することで、推論GPUの空き計算資源を微調整へ転用する外付け共存実行方式。

- **2026-07 · [BlockServe: Block-Grained Continuous Batching for High-Throughput Diffusion LLM Serving](2026-2607.08930-blockserve-diffusion-llm-continuous-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの要求ごとの収束速度差を、ブロック境界での即時追い出し・異なる拡散状態の混在実行・トークン予算補充で吸収する連続バッチング。Dream/LLaDAでFast-dLLM比1.9〜10.6倍のスループットを報告。

- **2026-07 · [Akashic: A Low-Overhead LLM Inference Service with MemAttention](2026-2607.05708-akashic-memattention-memory-service.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長期エージェント履歴を1024トークン級チャンクへ共同圧縮し、関連チャンクだけを検索・再統合してNVMe上でも近接配置することで、再入力量とメモリI/Oを減らす。

- **2026-06 · [The Serialized Bridge: Understanding and Recovering LLM Serving Performance under Blackwell GPU Confidential Computing](2026-2606.23969-serialized-bridge-blackwell-gpu-confidential-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU機密計算でLLM推論が遅くなる主因をGPU演算ではなく機密VM–GPU間の直列化された転送路と特定し、スケジューリング・モデルロード・KV退避を転送特性に合わせて変えることで大半の性能差を回復する。

- **2026-06 · [Solyx AI Grid: Hardware-Telemetry-Aware Routing Across Geographically Distributed GPU Clusters: An Empirical Study of Multi-Site LLM Inference](2026-2606.15050-solyx-hardware-telemetry-geo-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DCGM・vLLM・WANの10信号を圧力値へ統合し、地理分散GPUへの要求重みをxDSで更新する。障害・能力差・ネットワーク揺らぎを単一制御面で扱う。

- **2026-06 · [SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving with Lookahead Context Engineering](2026-2607.00151-smoothagent-lookahead-context-engineering.md)**  
  実装：[✓](https://github.com/PanZaifeng/SmoothAgent) ・ リポジトリ内被引用：0  
  文脈要約・オフロード・分離を前倒し実行し変換後KVを先に作るlookahead ランタイム。SGLangのSLO-aware スケジューラと組み合わせ、長時間agentの変換点TTFTを最大11.9倍改善。

- **2026-06 · [Service-Induced Congestion in Memory-Constrained LLM Serving](2026-2606.15555-service-induced-congestion-memory-constrained-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成中にKVキャッシュが増えるため現時点で安全な受入れが将来の追い出し連鎖を作ることを力学系で示し、要求長の非同期化と受入れ率制限を安定化原理として導く。

- **2026-06 · [RouteBalance: Fused Model Routing and Load Balancing for Heterogeneous LLM Serving](2026-2606.17949-routebalance-fused-routing-load-balancing.md)**  
  実装：[✓](https://github.com/AKafakA/route-balance) ・ リポジトリ内被引用：0  
  モデル選択と実体負荷分散を統合し、要求ごとの品質・予測遅延・費用を同時評価して具体的なモデル実体へ割り当て、異種GPU上の多モデルクラスタで品質と負荷集中を両立して抑える方式。

- **2026-06 · [PersistentKV: Page-Aware Decode Scheduling for Long-Context LLM Serving on Commodity GPUs](2026-2606.26666-persistentkv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ページ化KV表を作り直さず長い系列を区間へ分割し、必要な区間だけ作業キューへ詰めてGPUを埋め、長文デコードの遊休と不要なカーネル起動を減らす。

- **2026-06 · [Observation, Not Prediction: Conversation-Level Disaggregated Scheduling for Agentic Serving](2026-2606.01839-conserve-conversation-level-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント会話をターン単位で再配置せず、初回プリフィルのKVを一度だけデコードGPUへ移して後続ターンを同じGPUに固定し、再移送と将来長予測の誤差を減らす。

- **2026-06 · [M*: A Modular, Extensible, Serving System for Multimodal Models](2026-2606.12688-mstar-modular-composite-model-serving.md)**  
  実装：[✓](https://github.com/mstar-project/mstar) ・ リポジトリ内被引用：0  
  複合マルチモーダルモデルを構成要素グラフと要求別の『Walk』で宣言し、ループ・並列分岐・ストリーミング・GPU配置を共通実行時へ落とし込むことで、モデルごとの専用配線なしに高性能化する汎用サービング基盤。

- **2026-06 · [LUMEN: Coordinated Failure Recovery for Distributed LLM Serving](2026-2606.17787-lumen-coordinated-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  障害前の負荷認識キャッシュ保存、障害時の保存局所性と負荷を両立する再配分、モデル再読込中の小型下書きモデルによる投機補助を協調させ、分散大規模言語モデル提供基盤の復旧遅延を縮める方式。

- **2026-06 · [KernelFlume: Elastic Core-Attention Scaling for Agentic Long-Context Decoding](2026-2606.29207-kernelflume-elastic-core-attention-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル重みを固定した重みノードとKV保持・注意計算だけの重みなしノードへデコードを分離し、長文要求のKV増加に合わせて注意側だけを増設することで、完全モデル複製なしに低遅延で容量を拡張するサービング方式。

- **2026-06 · [HBM Is Not All You Need: Efficient Disaggregated LLM Serving across Memory-heterogeneous Accelerators](2026-2606.29986-hma-serve-memory-heterogeneous-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  計算律速のプリフィルを安価なGDDR搭載アクセラレータ、メモリ律速のデコードをHBM GPUへ分担し、低精度KVの層別転送と遅延復元で異ベンダー間の形式差と通信待ちを隠す分離配信方式。

- **2026-06 · [FlexNPU: Transparent NPU Virtualization for Dynamic LLM Prefill-Decode Co-location](2026-2606.04415-flexnpu-transparent-virtualization-dynamic-pd-colocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AscendCL操作を仮想ハンドル経由で物理NPUへ転送し、プリフィルとデコードの待機・実行時間・帯域圧力を測って実行比率を動的に変え、静的PD配置の資源偏りとTTFT待ちを減らす。

- **2026-06 · [Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs](2026-2606.30391-energy-aware-scheduling-for-serverless-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有GPU上の複数LLMについて、要求配置・SM分割・GPU周波数・低負荷時集約をSLO制約下で協調し、同居モデルの周波数不一致を避けてクラスタ全体の推論エネルギーを削減するサーバレス制御方式。

- **2026-06 · [Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference](2026-2606.23521-concordia-persistent-kernel-checkpointing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU常駐の永続カーネルでKVキャッシュ等の差分を検出・追記保存し、NCCL境界でのチェックポイントとGPU故障復旧をホストCPU依存なしに高速化する耐障害LLM推論基盤。

- **2026-06 · [Beyond Prediction: Tail-Aware Scheduling for LLM Inference](2026-2606.18431-tail-aware-prediction-free-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長予測を使わず、既得サービス量と末尾分布から要求優先度を調整し、KVを壊す頻繁なプリエンプトを幾何学的に制限して平均ではなくP95/P99遅延を安定化する。

- **2026-06 · [AgentServeSim: Serving-System Simulation and Policy Search for LLM Agent Programs](2026-2606.09613-agentservesim-multiturn-agent-serving-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多輪エージェントを要求列ではなく因果的なプログラムとして模擬し、ツール待ちをまたぐKV保持・セッション配置・プログラム単位スケジューリングを同一評価基盤で比較する。実vLLMとの20条件で平均完了時間誤差を約5.5%以内に抑える。

- **2026-05 · [VibeServe: Can AI Agents Build Bespoke LLM Serving Systems?](2026-2605.06068-vibeserve-agent-generated-bespoke-serving-systems.md)**  
  実装：[✓](https://github.com/uw-syfi/vibe-serve) ・ リポジトリ内被引用：0  
  モデル・ワークロード・ハードウェアごとに複数AIエージェントがLLMサービング基盤を生成し、標準条件ではvLLM相当、特殊条件では予測出力・ハイブリッドキャッシュ・Apple Silicon特化などを自動実装して最大6.27倍高速化する。

- **2026-05 · [Towards Multi-Model LLM Schedulers: Empirical Insights into Offloading and Preemption](2026-2605.19593-multi-model-offloading-preemption-schedulers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  限られたGPUで複数モデルを切り替える推論について、GPUに置く層の割合を連続掃引し、KV退避・モデル解放・重み再読込・KV復元の費用を分解して、オフロード感度と切替ボトルネックを測定した研究。

- **2026-05 · [Towards Distributed Inference of LLMs on a P2P Network](2026-2606.17059-p2p-prefix-cache-aware-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散LLMサービングで各ノードの接頭辞KV基数木を交換し、キャッシュを持つノードへ要求を移すP2Pルーティングでプリフィル再計算を減らすが、転送遅延と負荷集中も測定する。

- **2026-05 · [Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference](2026-2605.02329-taming-request-imbalance-slo-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離で、各要求のTTFT/TPOT目標までの余裕を測り、余裕のない要求を先にプリフィルし、余裕内だけ短いデコード要求を選んで長い要求の先頭待ちと同期遅延を減らすSLOスケジューラ。

- **2026-05 · [Regulating Branch Parallelism in LLM Serving](2026-2605.06914-taper-regulating-branch-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各デコードステップの残余SLO余裕から追加分岐の遅延予算を作り、予算内だけを動的に実行することで、分岐並列化による他要求の遅延悪化を防ぎつつQwen3-32Bで有効スループットを最大1.77倍へ高める。

- **2026-05 · [Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server](2026-2609.05425-cotail.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU制御段階のP95/P99遅延からスケジューラ競合とNUMA・キャッシュ競合を診断し、リアルタイム優先度またはCPU配置分離を選んで同居ワークロードによるLLM遅延を減らす。

- **2026-05 · [HexAGenT: Efficient Agentic LLM Serving via Workflow- and Heterogeneity-Aware Scheduling](2026-2605.16637-hexagent-workflow-heterogeneity-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HexAGenTは逐次公開されるエージェントワークフローの完了危険度を追跡し、異種GPU上のプリフィル・デコード配置とキュー優先度を共同決定して、ワークフロー全体のSLO達成を改善する。

- **2026-05 · [GoodServe: Towards High-Goodput Serving of Agentic LLM Inferences over Heterogeneous Resources](2026-2605.16867-goodserve-agentic-heterogeneous-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長と各GPUの実効処理能力を予測し、SLOを満たす必要十分なGPUへ割り当て、実行中の違反リスクを軽量移行で補正してグッドプットを最大27.4%改善する。

- **2026-05 · [DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Checkpoint/Rollback](2026-2605.22781-deltabox-agent-sandbox-checkpoint-rollback.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ファイルとプロセスの連続状態差分だけを保存し、動的overlay層切替と凍結テンプレートforkを組み合わせて、状態を持つAIエージェントのチェックポイント・ロールバックをミリ秒級にする。

- **2026-05 · [C2CServe: Leveraging NVLink-C2C for Elastic Serverless LLM Serving on MIG](2026-2605.19481-c2cserve-serverless-mig-nvlink-c2c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GH200のCPUメモリをNVLink-C2C経由の能動的な重み格納層として使い、MIGごとのHBM不足を回避するサーバレスLLM基盤。HybridGEMMと競合対応スケジューラで密モデルのコールドスタートを最大7.1倍短縮する。

- **2026-04 · [Dual-Pool Token-Budget Routing for Cost-Efficient and Reliable LLM Serving](2026-2604.08075-dual-pool-token-budget-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  短文が大半なのに全GPUを最長文脈向けに設定する無駄を、短文・長文の2群と自己較正する総トークン予算ルーティングで解き、KV容量の過剰予約、要求追い出し、GPU費用を同時に削減する。

- **2026-04 · [Distributed Generative Inference of LLM at Internet Scales with Multi-Dimensional Communication Optimization](2026-2604.21072-bloombee-internet-scale-distributed-inference.md)**  
  実装：[✓](https://github.com/ai-decentralized/BloomBee) ・ リポジトリ内被引用：0  
  一般インターネット上の異種GPU推論で、層配置・KV退避・マイクロバッチ・無損失活性値圧縮・帯域適応型投機デコードを組み合わせ、通信ホップ数・転送量・生成段数を共同削減する。

- **2026-04 · [Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC](2026-2604.07609-blink-cpu-free-llm-inference-gpu-smartnic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  定常状態のLLM推論でCPUが行うバッチ更新・KV管理・GPU起動をGPU常駐制御へ移し、要求受付とトークン送受信をSmartNICへ分離して、CPU干渉によるGPU待ちとコピー待ちを減らす実機システム。

- **2026-03 · [Understand and Accelerate Memory Processing Pipeline for Large Language Model Inference](2026-2603.29002-memory-processing-pipeline-gpu-fpga.md)**  
  実装：[✓](https://github.com/OswaldHe/HeteroLLM) ・ リポジトリ内被引用：0  
  疎注意・RAG・圧縮メモリを4段階の共通メモリ処理へ分解し、不規則・メモリ律速部分をFPGA、密計算をGPUへ割り当てて長文推論の遅延と消費エネルギーを削減する異種実行方式。

- **2026-03 · [TCM-Serve: Modality-aware Scheduling for Multimodal Large Language Model Inference](2026-2603.26498-rps-serve-modality-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル遅延とKV占有量からマルチモーダル要求を3資源クラスへ分け、クラス別キューとエージング付き優先制御で巨大動画による先頭待ちを抑え、平均TTFTを54%、遅延重視要求で78.5%削減する。

- **2026-03 · [PrefixWall: Mitigating Prefix Caching Side Channels in Shared LLM Systems](2026-2603.10726-cachesolidarity-prefix-cache-side-channel-defense.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PrefixWallは、共有自動接頭辞キャッシュのヒット・ミス遅延から他利用者の入力を推測される副チャネルを検出し、異なる利用者間で再利用された接頭辞の先だけを再計算へ切り替えることで、完全分離よりキャッシュ再利用を残す防御。

- **2026-03 · [Multi-stage Flow Scheduling for LLM Serving](2026-2603.17456-multi-stage-flow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MFSは、遠隔KV取得・集団通信・プリフィルからデコードへの転送を依存付きの段階として追跡し、余裕のある通信を遅らせ、締切が近いフローを逆多段キューで昇格してTTFTのSLO違反を減らすネットワークスケジューラ。

- **2026-03 · [Cost-Efficient Multimodal LLM Inference via Cross-Tier GPU Heterogeneity](2026-2603.12707-cost-efficient-multimodal-llm-inference-via-cross-tier-gpu-heterogeneity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像符号化をRTX 4090、言語生成をA100へ分離し、KVキャッシュではなく数MB級の画像埋め込みだけをPCIe転送することで、異種GPUを使った低コストなマルチモーダルLLMサービングを実現する。

- **2026-03 · [Chimera: Latency- and Performance-Aware Multi-agent Serving for Heterogeneous LLMs](2026-2603.22206-chimera-latency-performance-aware-multi-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種LLM群で要求難易度、残りワークフロー長、実行中トークン量を同時予測し、モデル選択と待ち行列順序を共同制御して遅延とタスク性能のPareto前線を改善する。

- **2026-03 · [CALVO: Improve Serving Efficiency for LLM Inferences with Intense Network Demands](2026-2603.21257-calvo-network-aware-kv-loading-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔KV読み込みを独立した非同期段階へ分離し、通信時間と計算時間を合わせた要求費用で順序付けすることで、長文脈の高キャッシュ再利用環境で平均最初のトークン時間を81.3%以上短縮し、期限達成率を最大61.67%改善する。

- **2026-03 · [AgentServe: Algorithm-System Co-Design for Efficient Agentic AI Serving on a Consumer-Grade GPU](2026-2603.10342-agentserve-consumer-gpu-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント処理を初回・再開プリフィルと短いデコードへ分け、TPOTフィードバックとGPU内SM予約で民生GPU上の相互干渉を抑える。

- **2026-02 · [Multi-Layer Scheduling for MoE-Based LLM Reasoning](2026-2602.21626-multi-layer-scheduling-moe-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gimbalは、MoEサービングで実測KV使用量から要求の送り先、入力長からエンジン内の実行順、専門家の活性頻度と層間依存からGPU配置を決め、容量偏り・先頭待ち・専門家集中をまとめて減らす三層スケジューラ。

- **2026-01 · [EPD-Serve: A Flexible Multimodal EPD Disaggregation Inference Serving System On Ascend](2026-2601.11590-epd-serve-ascend-multimodal-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチモーダル推論をエンコード・事前充填・復号へ三分離し、段階間の非同期特徴量/KV転送、モダリティ別ルーティング、物理同居を組み合わせて、異種段階の干渉を抑えながらSLOと資源効率を改善する。

- **2026-01 · [Competitive Non-Clairvoyant KV-Cache Scheduling for LLM Inference](2026-2601.22996-competitive-non-clairvoyant-kv-cache-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  未知の生成長に対し、幾何級数的な時間片ごとの再開始と開始時刻をずらすKVメモリ平滑化を組み合わせ、一般条件で初の定数競合比を与える非先見的KVスケジューリング理論。

- **2025-11 · [Serving Heterogeneous LoRA Adapters in Distributed LLM Inference Systems](2025-2511.22880-loraserve-heterogeneous-adapter-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRAのランクと需要を同時に見て動的配置・確率ルーティングし、不在アダプタはGPUDirect RDMAで遠隔取得して分散アダプタプールを構成する。

- **2025-11 · [FailSafe: High-performance Resilient Serving](2025-2511.14116-failsafe-resilient-tensor-parallel-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU障害後も任意数のGPUでテンソル並列推論を継続し、KVキャッシュ配置・注意計算・要求割当を均衡化しながら状態復旧を高速化する。

- **2025-10 · [Loquetier: A Virtualized Multi-LoRA Framework for Unified LLM Fine-tuning and Serving](2025-2511.00101-loquetier-virtualized-multilora-serving.md)**  
  実装：[✓](https://github.com/NJUDeepEngine/Loquetier) ・ リポジトリ内被引用：0  
  共有基盤LLM上でLoRAごとの仮想モデルを隔離し、SMLMカーネルで微調整・評価・プリフィル・デコードを同一実行系へ統合する多数LoRA基盤。推論でFlexLLM比最大3.0倍、統一負荷でPEFT比46.4倍のSLO達成率を報告する。

- **2025-10 · [From Principles to Practice: A Systematic Study of LLM Serving on Multi-core NPUs](2025-2510.05632-systematic-study-multicore-npu-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチコアNPU向け多層シミュレータで、テンソル分割・コア配置・SRAM/HBM管理・プリフィルとデコードの分離/融合をQwen3各サイズで比較し、入力長・通信競合・負荷構成ごとに有利な設計を明らかにする研究。

- **2025-10 · [BanaServe: Unified KV Cache and Dynamic Module Migration for Balancing Disaggregated LLM Serving in AI Infrastructure](2025-2510.13223-banaserve-dynamic-module-migration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離サービングの固定GPU配分と接頭辞キャッシュ偏在を、層単位の重み移動・注意ヘッド単位のKV移動・CPU/SSD共有KVストアで切り離し、負荷だけを見た再配置とルーティングを可能にする。

### 2年前（2024-10〜2025-09）

- **2025-02 · [Autellix: An Efficient Serving Engine for LLM Agents as General Programs](2025-2502.13965-autellix-agent-program-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  エージェントのLLM呼び出しをプログラム単位で追跡し、累積サービス時間と動的DAGの重要経路近似で優先順位を付け、KV局所性を保つ複数GPUルーティングまで組み合わせてプログラム全体の待ち時間を削減する。

- **2025-04 · [MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism](2025-2504.02263-megascale-infer-disaggregated-expert-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  注意機構とMoE専門家FFNを別GPU群へ分離し、複数注意レプリカから専門家要求を集約して大きな専門家バッチを作り、専用多対多RDMA通信とピンポン型パイプラインで通信を隠す大規模MoEサービング方式。

- **2025-02 · [SageServe: Optimizing LLM Serving on Cloud Data Centers with Forecast Aware Auto-Scaling](2025-2502.14617-sageserve-multi-timescale-cloud-autoscaling.md)**  
  実装：[✓](https://github.com/shashwatj07/SageServe) ・ リポジトリ内被引用：13  
  対話型と非対話型の要求を統合GPUプールで共有し、地域間ルーティング、需要予測、整数線形計画、遅延実行を異なる時間尺度で連携させる。Office 365の本番トレースでSLOを維持しつつGPU時間を最大25%削減した。

- **2025-04 · [Optimizing LLM Inference: Fluid-Guided Online Scheduling with Memory Constraints](2025-2504.11320-fluid-guided-online-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  流体平衡からデコード進捗区間ごとのGPU常駐構成を見積もり、WAIT/Nested WAITで制御する。未知の出力長は予測せず、生成を継続する残存要求を段階分類してKV追い出し連鎖を抑えるスケジューラ。

- **2025-08 · [Prefill-Decode Aggregation or Disaggregation? Unifying Both for Goodput-Optimized LLM Serving](2025-2508.01989-taichi-unified-prefill-decode-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  プリフィル重視/デコード重視インスタンスを混在させ、要求ごとのTTFT・TPOT余裕を別要求へ移すことで集約型と分離型を統一するLLM配信基盤。既存集約型比9〜47%、分離型比29〜77%グッドプットを改善する。

- **2025-08 · [Kairos: Low-latency Multi-Agent Serving with Shared LLMs and Excessive Loads in the Public Cloud](2025-2508.06948-kairos-multi-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  動的ワークフローから残り遅延分布を学習して短く完了しやすいエージェントを優先し、将来KVメモリ需要を時間枠で予測してLLM実体へ配置するマルチエージェント配信基盤。

- **2025-07 · [Oneiros: KV Cache Optimization through Parameter Remapping for Multi-tenant LLM Serving](2025-2507.11507-oneiros-parameter-remapping-multitenant-serving.md)**  
  実装：[✓](https://github.com/UT-SysML/Oneiros/) ・ リポジトリ内被引用：5  
  複数LLMを同じGPUで提供すると、KVキャッシュ不足をCPU退避で解決する方法は毎トークンの転送と同期でデコードを止める。Oneirosは不変なモデルパラメータをCPUへ移し、空いたGPUページをKVキャッシュへ転用し、重み読込みをGPU計算に重ねて停滞を抑える。

- **2025-01 · [Mell: Memory-Efficient Large Language Model Serving via Multi-GPU KV Cache Management](2025-2501.06709-mell-multi-gpu-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  複数GPUでLLMを提供すると、要求ごとの出力長の違いでKVキャッシュが一方のGPUだけに膨らみ、空きGPUを使えない。Mellは実行中要求をGPU間で移し、通信余力があればKV本体を転送し、演算余力があればトークンだけを送り移行先で再プリフィルして偏りを抑える。

- **2025-01 · [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  対話型リクエストの遅延目標を守りながら余ったGPU容量をバッチリクエストへ使うため、各GPUで同時処理するリクエスト数を素早く増減する制御と、クラスタ全体のGPUインスタンス数を遅い周期で増減する制御を分けたLLM自動スケーラ。

- **2025-01 · [DeepServe: Serverless Large Language Model Serving at Scale](2025-2501.14417-deepflow-serverless-llm-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  要求・ジョブ・タスク抽象、NPU中心FlowServe、KV局所性とPD構成を統合した分散スケジューラ、NPU-fork等の高速スケールを組み合わせたHuawei Cloud本番サーバーレスLLM基盤。

- **2025-09 · [Parallax: Efficient LLM Inference Service over Decentralized Environment](2025-2509.26182-parallax-decentralized-heterogeneous-serving.md)**  
  実装：[✓](https://github.com/GradientHQ/parallax) ・ リポジトリ内被引用：4  
  地理的に離れた異種GPUでモデル層を地域・VRAM・計算性能に合わせて配置し、GPUごとの処理時間と通信遅延から要求ごとの層経路を選ぶことで、遅いGPU・低速回線によるパイプライン待ちを減らす分散LLMサービング。

- **2025-09 · [Amoeba: Runtime Tensor Parallel Transformation for LLM Inference Services](2025-2509.19729-gyges-cross-instance-parallelism-transformation.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  要求長に応じて稼働中インスタンスをTP1↔TP2↔TP4へ変換し、KVページ配置と重み境界を事前整列して再計算なしで並列度を変えることで、短文時の高処理量と長文対応を両立する方式。

- **2025-05 · [HydraInfer: Hybrid Disaggregated Scheduling for Multimodal Large Language Model Serving](2025-2505.12658-hydrainfer-hybrid-epd-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  画像符号化・入力処理・デコードを異種段階として扱い、負荷とSLOに応じてE+P+D、EP+D、ED+Pを選ぶ混成分離と段階別バッチ・二重ストリームを組み合わせ、マルチモーダル配信のグッドプットを高める。

- **2025-04 · [FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling](2025-2504.03775-flowkv-low-latency-transfer-load-aware.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KVキャッシュを連続セグメントへ寄せてNCCL転送をまとめ、全体負荷に応じてプリフィル／デコード役割も切り替える分離推論基盤。転送遅延を最大96.8%削減し、LongBenchで15.2〜48.9%短縮。

- **2025-02 · [λScale: Enabling Fast Scaling for Serverless Large Language Model Inference](2025-2502.09922-lambdascale-serverless-fast-scaling.md)**  
  実装：[✓](https://github.com/lambda-scale/lambda-scale) ・ リポジトリ内被引用：4  
  モデル重みをRDMAで多段配信し、全重みの到着を待たず受信済み層から分散推論を始めるサーバレス拡張方式。実負荷トレースで末尾TTFTを最大5倍改善し、累積GPU資源を最大31.3%削減する。

- **2025-01 · [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  クライアントごとのサービス量を公平に保ちつつ、公平性が大きく崩れない範囲だけ実行順を入れ替えて、同じ接頭辞を持つリクエストを続けて処理しKV再利用を増やすスケジューラ。複数GPUでは負荷分散も同時に調整する。

- **2025-04 · [Efficient LLM Serving on Hybrid Real-time and Best-effort Requests](2025-2504.09590-bros-hybrid-real-time-best-effort-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  RTのTTFT/TPOT締切を動的優先度にした反復単位スケジューリングと、RT/BEが同じKVブロックを逆方向から共有する双方向KV管理で、混在負荷の遅延と処理量を両立する。

- **2025-02 · [HydraServe: Minimizing Cold Start Latency for Serverless LLM Serving in Public Clouds](2025-2502.15524-hydraserve-serverless-cold-start.md)**  
  実装：[✓](https://github.com/LLMServe/hydraserve) ・ リポジトリ内被引用：3  
  起動時だけモデル層を複数サーバーへ分散して帯域を束ね、重み取得・GPU転送・実行環境初期化を重ね、起動後にワーカーを集約することでサーバーレスLLMのコールドスタートを1.7〜4.7倍短縮する。

- **2025-09 · [Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism](2025-2509.08309-hetis-heterogeneous-gpu-dynamic-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異種GPUの遅い機種を密演算経路から外し、デコード注意をヘッド単位で動的分配してKVキャッシュも部分移行することで、計算・通信・メモリの不均衡を同時に抑えるLLMサービング方式。

- **2025-09 · [FineServe: Precision-Aware KV Slab and Two-Level Scheduling for Heterogeneous Precision LLM Serving](2025-2509.06261-fineserve-precision-aware-kv-slab-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  混合精度モデル間で共有できるKVスラブと、精度別の限界メモリ効率・TTFT期限を使う二段スケジューリングにより、Prism相当方式比でSLO達成率最大2.2倍、生成スループット最大1.8倍を実現する。

- **2025-09 · [A Predictive and Synergistic Two-Layer Scheduling Framework for LLM Serving](2025-2509.23384-synergysched-predictive-two-layer-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  オンライン性能モデルをエンジン内SLO対応処理群形成とクラスタ先読み配送の共通信号にし、二層間の情報断絶を閉じて動的・異種LLM配信の遅延とSLO達成率を改善する。

- **2025-07 · [ElasticMM: Efficient Multimodal LLMs Serving with Elastic Multimodal Parallelism](2025-2507.10069-elasticmm-elastic-multimodal-parallelism.md)**  
  実装：[✓](https://github.com/hpdps-group/ElasticMM) ・ リポジトリ内被引用：1  
  テキスト要求とマルチモーダル要求を分離し、符号化・事前充填・復号ごとにGPU配分と並列度を動的変更することで、TTFTを最大4.2倍短縮しSLO内スループットを3.2〜4.5倍にする。

- **2025-03 · [PipeBoost: Resilient Pipelined Architecture for Fast Serverless LLM Scaling](2025-2503.17707-pipeboost-resilient-pipelined-serverless-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同一基盤モデルのサーバーレス立上げをGPU間のパイプライン読込・早期分散推論・障害復旧で高速化し、既存低遅延基盤比で推論遅延を31〜49.8%削減する。

- **2025-03 · [AccelGen: Heterogeneous SLO-Guaranteed High-Throughput LLM Inference Serving for Diverse Applications](2025-2503.13737-accelgen-heterogeneous-slo-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SLOから各反復のトークン予算を決める動的分割、残り猶予順の優先付け、GPU計算とKVキャッシュを同時に詰める処理群選択を組み合わせ、長短入力混在で有効処理量とSLO達成率を改善する。

- **2024-11 · [Saving GPU Hours in LLM Inference System Development and Online Workloads with Simulation and DBMS-Inspired Cache Replacement Policies](2024-2411.07447-dbms-inspired-cache-replacement-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  単純なコストモデルによる推論シミュレーションから、短い要求を先にプリエンプトするSRFを導出。vLLM/SGLang/Dynamoへ数行で実装し、オンライン負荷で遅延を最大15〜20%改善する。

- **2025-08 · [Taming the Chaos: Coordinated Autoscaling for Heterogeneous and Disaggregated LLM Inference](2025-2508.19559-heteroscale-coordinated-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種GPUとRDMAネットワーク階層を考慮してプリフィル／デコードを配置し、デコードTPSを主信号に両プールを協調増減することで、P/D分離サービングの資源浪費と比率崩れを抑える。

- **2025-07 · [LeMix: Unified Scheduling for LLM Training and Inference on Multi-GPU Systems](2025-2507.21276-lemix-unified-training-inference-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LeMixは継続学習と推論を同一GPU群へ共置し、事前予測した空き時間・応答遅延・メモリ量でタスク配置と実行順を調整する。固定分離比でスループット最大3.53倍、SLO達成率最大2.12倍を報告。

- **2025-05 · [SpecEdge: Scalable Edge-Assisted Serving Framework for Interactive LLMs](2025-2505.17052-specedge-edge-assisted-speculative-serving.md)**  
  実装：[✓](https://github.com/kaist-ina/specedge) ・ リポジトリ内被引用：0  
  消費者GPUをエッジ側ドラフト生成へ使い、先行ドラフトと複数要求の検証パイプラインでWAN遅延を隠しつつ、A100サーバの処理量を平均2.22倍へ高めるエッジ支援投機的配信。

- **2025-05 · [Scorpio: Serving Right Requests at the Right Time for Heterogeneous SLOs in LLM Inference](2025-2505.23022-scorpio-heterogeneous-slo-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとに異なるTTFT/TPOTのSLOを、締切順の並べ替え・達成不能要求の拒否・SLO比例の処理機会配分で共同制御し、高負荷時の有効スループットを最大14.4倍にする。

- **2025-01 · [iServe: An Intent-based Serving System for LLMs](2025-2501.13111-iserve-intent-based-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  軽量なモデル・フィンガープリントで多数の並列化・圧縮構成の遅延とメモリを推定し、利用者の遅延・費用意図とGPU空き状況に合わせて配備構成を自動選択することで、遅延77.62%削減、SLO達成3.03〜7.09倍、GPUスループット4.72倍を示す。

### 3年前（2023-10〜2024-09）

- **2024-01 · [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)**  
  実装：[✓](https://github.com/LLMServe/DistServe) ・ リポジトリ内被引用：199  
  プリフィルとデコードを別GPU群へ分け、それぞれのGPU数・モデル分割方法・配置場所を、最初のトークンまでの時間とその後のトークン間隔の目標に合わせて別々に決めることで、両処理段階の干渉をなくす推論提供システム。

- **2023-12 · [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)**  
  実装：[✓](https://github.com/sgl-project/sglang) ・ リポジトリ内被引用：180  
  複数のLLM呼び出しや条件分岐をランタイムが1つのプログラムとして理解し、共有接頭辞のKV再利用・並列実行・構造化出力生成をまとめて効率化する推論システム。

- **2023-11 · [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)**  
  実装：[✓](https://github.com/Mutinifni/splitwise-sim) ・ リポジトリ内被引用：177  
  プリフィルとデコードを別の計算機群へ分け、それぞれに向くGPU世代・電力設定・台数を使い分けて、クラスタ全体のスループット・コスト・消費電力を改善するサービング設計。

- **2024-03 · [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)**  
  実装：[✓](https://github.com/microsoft/sarathi-serve) ・ リポジトリ内被引用：158  
  長いプリフィルを小さい分割片へ分け、毎回まず進行中要求のデコードトークンを処理し、残った総トークン枠へプリフィルを入れることで、新要求を受けながらデコードの長時間停止を防ぐ推論提供スケジューラ。

- **2024-07 · [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：103  
  プリフィルとデコードを別GPU群へ分け、クラスタ内のCPU DRAM・SSDへ過去KVを保存して別ノードからも再利用できるようにし、KV取得時間・待ち行列待ち・残りプリフィル計算を比較してリクエストの実行先を決める大規模な推論提供システム。

- **2024-03 · [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：72  
  複数ターン会話の過去KVを要求終了後もDRAM / SSDへ保存し、次ターンで使う層のKVを少し前からGPUへ戻すことで、履歴全体の再プリフィルと記憶装置待ちを減らす状態保持型推論提供手法。

- **2024-06 · [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)**  
  実装：[✓](https://github.com/AlibabaPAI/llumnix) ・ リポジトリ内被引用：66  
  実行中要求のKVキャッシュを別モデル実行単位へ段階的に移し、GPU間の混雑差・メモリ不足・優先度変更・実行単位削減が起きた後でも要求配置を修正できる複数実行単位の推論提供スケジューラ。

- **2024-05 · [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：35  
  同じプレフィックスのKVをすでに持つGPUへリクエストを送ればプリフィルを省ける一方、そのGPUだけ混むことがあるため、KV再利用で節約できる計算時間とGPUの混雑による待ち時間を比較してリクエストの送り先を決めるdistributed サービング スケジューラ。

- **2024-01 · [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed-MII) ・ リポジトリ内被引用：35  
  長いプリフィルを小さく分割し、短いプロンプト・プリフィル 分割片・デコード トークンを毎回ほぼ同じ総トークン数になるよう混ぜることで、長いプリフィルがデコードを止める時間を抑えつつGPUを効率よく使うLLM 提供処理 システム。

- **2024-01 · [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)**  
  実装：[✓](https://github.com/ServerlessLLM/ServerlessLLM) ・ リポジトリ内被引用：34  
  要求到着時にモデルをGPUへ読み込むサーバーレス環境で、チェックポイントをGPU近くのSSD / DRAMへキャッシュし、高速読み込み器とモデル所在地を考慮した要求配置、生成途中要求の移動を組み合わせてモデル起動待ちを短縮するシステム。

- **2023-12 · [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)**  
  実装：[✓](https://github.com/Ying1123/VTC-artifact) ・ リポジトリ内被引用：32  
  仮想 トークン Counter（VTC）は、要求数ではなくクライアントごとに実際に処理した入力・出力トークンをサービス量として数え、累積サービス量が少ないクライアントから新しい要求を実行バッチへ入れる。空きGPUを意図的に遊ばせず、公平性と高い利用率を両立することを狙う。

- **2024-06 · [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  プリフィルとデコードを別実行単位へ分ける推論提供で、GPU / CPU上のKVキャッシュを実行単位横断で検索・共有・転送できる共通メモリプールを作り、過去接頭部の再利用と処理段階間KV移動を同じ仕組みで扱うシステム。

- **2024-05 · [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)**  
  実装：[✓](https://github.com/microsoft/ParrotServe) ・ リポジトリ内被引用：31  
  複数LLM呼び出しから成るアプリケーションについて、どの呼び出しの出力を次の呼び出しが使うか、どのプロンプト部分を共有するかをバックエンドへ伝え、アプリケーション全体を見て並列実行・バッチ処理・接頭部 KV再利用を調整する推論提供システム。

- **2023-11 · [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)**  
  実装：[✓](https://github.com/Hsword/SpotServe) ・ リポジトリ内被引用：30  
  安価だが突然利用できなくなるスポットGPU（spot GPU）の増減に合わせてモデルの分割方法を組み替え、既存の重み（重み）とKVキャッシュ（KV キャッシュ）をできるだけ再利用してLLMサービングを継続するシステム。

- **2024-08 · [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  最終的な出力トークン数を正確に当てる代わりに、プロンプトからどのリクエストが他より短く終わりそうかという順位だけを小型モデルで予測し、短そうなリクエストを先に処理して長いリクエストによるキュー待ちを減らすスケジューラ。

- **2023-12 · [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  複数往復会話の過去KVキャッシュをリクエスト終了後もGPU / CPUへ残し、次の往復で同じ履歴を再びプリフィルする計算を避ける状態保持型LLM提供処理システム。

- **2024-02 · [INFERCEPT: Efficient Intercept Support for Augmented Large Language Model Inference](2024-2402.01869-infercept-intercept-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  外部ツールや人間応答を待つ間に生成が中断される拡張LLMで、KVキャッシュをGPUに保持する、CPUへ退避する、破棄して再計算するという三つの選択肢を、GPUメモリの時間積で表した浪費量を基準に要求ごとに切り替える推論基盤。

- **2024-06 · [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)**  
  実装：[✓](https://github.com/QLM-project/QLM) ・ リポジトリ内被引用：18  
  対話的 / バッチ要求や複数モデルを同じクラスタで扱うとき、各要求グループがあと何秒待てるかとモデルがどのGPUに載っているかを見て、待ち行列順序と実行先を組み替え、遅延目標を守れる要求数を増やすシステム。

- **2024-06 · [Helix: Distributed Serving of Large Language Models via Max-Flow on Heterogeneous GPUs](2024-2406.01566-helix-maxflow-heterogeneous-gpu-serving.md)**  
  実装：[✓](https://github.com/Thesys-lab/Helix-ASPLOS25) ・ リポジトリ内被引用：12  
  異種GPUとネットワークを容量付き有向グラフへ写像し、最大流を目的に層配置をMILPで決め、最大流比率に沿って要求ごとの経路を選ぶことで、固定パイプラインの遊休GPUと通信混雑を減らすLLMサービング方式。

- **2024-04 · [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  LLMのストリーミング応答を単純な生成速度ではなく、最初のトークンが早く届き、その後もユーザーが読む速度に間に合うようトークンが途切れず届くかで評価し、十分先まで生成済みの要求を一時停止して、今すぐGPU時間が必要な要求へ回す推論提供システム。

- **2024-08 · [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  P/D-Serveは、事前充填と復号を別インスタンス群へ分け、シナリオごとにP/D比を調整し、混雑ノードを待たず要求を再送し、KV転送をまとめることで数万NPUクラスタの待ち行列と通信固定費を減らす商用基盤。

- **2023-10 · [Punica: Multi-Tenant LoRA Serving](2023-2310.18547-punica-multitenant-lora-serving.md)**  
  実装：[✓](https://github.com/punica-ai/punica) ・ リポジトリ内被引用：4  
  異なるLoRAアダプタの要求をSGMVカーネルで同一バッチ処理し、基盤LLMを共有したまま多テナント推論を集約するサービング基盤。固定GPU資源で最大12倍のスループットを報告。

### 4年前（2022-10〜2023-09）

- **2023-09 · [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)**  
  実装：[✓](https://github.com/vllm-project/vllm) ・ リポジトリ内被引用：362  
  vLLMは、要求ごとに大きな連続領域を予約していたKVキャッシュを固定長ブロックへ分解し、論理的な並びとGPU上の物理配置を分離する。必要なブロックだけ動的に割り当て、同じ接頭辞のKVを共有することで、限られたGPUメモリへより多くの要求を同時に載せる。

- **2023-02 · [AlpaServe: Statistical Multiplexing with Model Parallelism for Deep Learning Serving](2023-2302.11665-alpaserve.md)**  
  実装：[✓](https://github.com/alpa-projects/mms) ・ リポジトリ内被引用：60  
  複数モデルへ届くリクエスト数が時間ごとに偏る環境で、モデルを複数GPUへ分割して置き、空いているGPUをモデル間で共有しやすくすることで、特定モデルだけ待ち行列が伸びるのを抑えるサービング配置手法。

- **2023-05 · [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)**  
  実装：[✓](https://github.com/LLMServe/FastServe) ・ リポジトリ内被引用：58  
  出力トークンを1つ生成する区切りで要求（リクエスト）を一時停止・再開できるようにし、短い要求を優先しながらKVキャッシュ（KV キャッシュ）をCPUへ退避・先読みして待ち時間を減らすLLMサービングスケジューラ（serving スケジューラ）。

### 5年前（2021-10〜2022-09）

- **2022-07 · [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：188  
  出力トークンを1個生成するたびにスケジューラへ制御を戻し、終わった要求を外して新着要求を追加する。さらに、長さの違う要求を同じバッチで処理できるよう、注意機構だけを要求ごとに分け、それ以外の演算はトークン単位でまとめて実行する分散LLMサービングシステム。
<!-- survey:auto:end -->
