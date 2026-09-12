# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（97本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-12 · [TraCT: Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale](2025-2512.18194-tract-rack-scale-cxl-shared-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  CXL Type-3共有メモリをプリフィル・デコード間KV転送路とラック共有接頭辞キャッシュに兼用し、GPU–CXL直接DMAでRDMAのNICホップを除去するサービング方式。

- **2025-11 · [Continnum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](2025-2511.02230-continuum-agent-kv-cache-ttl-scheduling.md)**  
  実装：[✓](https://github.com/Hanchenli/vllm-continuum) ・ リポジトリ内被引用：6  
  ツール呼出しを挟む多ターンLLMエージェントで、ツール待ち時間・KV再構築費用・残りターンを見てKVキャッシュの保持期限を動的に決め、短い待ちではGPUに固定し長い待ちでは解放してターン間待ちを減らすスケジューラ。

- **2026-09 · [GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving](2025-2508.16449-greenllm-slo-aware-dvfs-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  GreenLLMは、プリフィルとデコードの負荷を入力長・出力TPS・P95トークン間時間から観測し、各段階のSLO内でGPU周波数を別々に選ぶ二重帰還制御により、過剰な高周波数動作とエネルギーを減らす。

- **2026-07 · [AugServe: Adaptive Request Scheduling for Augmented Large Language Model Inference Serving](2025-2512.04013-augserve-adaptive-request-scheduling-augmented-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  外部APIや検索を待つ拡張LLMで、停止・再開状態、出力長・外部呼出し時間、KV保持・退避・再計算費用を観測して要求順位と反復トークン予算を変え、先頭待ちとGPUメモリ圧迫を減らすスケジューラ。

- **2026-05 · [AlignedServe: Orchestrating Prefix-aware Batching to Build a High-throughput and Computing-efficient LLM Serving System](2026-2605.23389-alignedserve-prefix-aware-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AlignedServeは、長いKV系列を分離するため要求をCPU KVプールへ置き、接頭辞長が近い要求を四分木から密度優先で集め、次バッチのKVをGPU間へ先読みして反復内の待ちと転送待ちを減らす。

- **2026-04 · [Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter](2026-2604.15039-prefill-as-a-service-cross-datacenter-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KVキャッシュ量が小さいハイブリッド注意機構を利用し、長い未キャッシュ入力のプリフィルだけを遠隔GPU群へ振り分け、KVをデータセンター間転送して異種GPU資源の利用効率と処理能力を高める。

- **2026-02 · [DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS](2026-2602.18755-biscale-phase-aware-placement-dvfs.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DualScaleは、プリフィル・デコード分離のGPU台数・並列度・周波数・振り分け比率を数分単位で配置し、プリフィルの将来待ち行列とデコードのTPOT余裕を反復ごとに制御してSLO内の電力を減らす二段階方式。

- **2026-07 · [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル中に重要KVだけを先送りし、デコード時は不足分をローカル読出しと並列取得、残りを背景転送へ回して、全量転送の待ちと部分転送の後続停止を減らす。

- **2026-06 · [Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice](2026-2606.22327-geometry-aware-online-scheduling.md)**  
  実装：[✓](https://github.com/Aurora-Kl/Geometry-Aware-Online-Scheduling) ・ リポジトリ内被引用：1  
  出力長とプロンプト長からKVメモリ占有の時間積分を見積もり、小さいメモリ時間体積の要求を先に実行するSVFを比較して、SJFが無視するKV容量起因の先頭待ちを減らす。

- **2026-06 · [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低頻度MoEモデルの大きなFFN重みを重みGPUへ、変動するKVキャッシュを共有KV GPUへ分離し、モデル間で余剰HBMを融通して長文脈の容量不足とKV競合を減らす。

- **2026-05 · [RTP-LLM: High-Performance Alibaba LLM Inference Engine](2026-2605.29639-rtp-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  実運用LLM基盤で、要求をKV位置とGPU負荷に応じて振り分け、プリフィル/デコードを分離し、GPU〜分散ストレージのKV階層・高速読込・投機的復号を統合して待ち時間と容量負荷を減らす。

- **2026-03 · [MoEless: Efficient MoE LLM Serving via Serverless Computing](2026-2603.06350-moeless-serverless-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散MoE推論で次の層のエキスパート負荷を予測し、混雑するエキスパートだけを一時複製して複数GPUへ配置し、ルータを変えずに同期点での最遅GPU待ちを減らすサーバーレス提供システム。

- **2026-02 · [vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models](2026-2602.02204-vllm-omni-fully-disaggregated-multimodal-serving.md)**  
  実装：[✓](https://github.com/vllm-project/vllm-omni) ・ リポジトリ内被引用：1  
  複数LLM・拡散モデル・音声/画像生成器を段階グラフへ分解し、各段階を独立バッチ・独立GPU配置・共通コネクタで実行することで、any-to-any型マルチモーダル推論を単一モデル用サービング基盤から拡張する方式。

- **2026-02 · [OServe: Accelerating LLM Serving via Spatial-Temporal Workload Orchestration](2026-2602.12151-oserve-spatial-temporal-workload-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/LiveServe_Documents-1F54/) ・ リポジトリ内被引用：1  
  要求長の空間的ばらつきと時間変動を予測し、レプリカごとに異なるGPU数・並列方式と要求割当を最大流で共同最適化し、重み再利用による高速配置切替で追随するLLMサービング方式。

- **2026-02 · [Efficient Multi-round LLM Inference over Disaggregated Serving](2026-2602.14516-ampd-multi-round-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  多ラウンド推論の追加プリフィルを、実行時負荷に応じてデコード側の局所実行かプリフィル側の遠隔実行へ振り分け、待ち行列の並べ替えとGPU配備計画を組み合わせてSLO達成率を高める分離サービング方式。

- **2026-01 · [Power Aware Dynamic Reallocation For Inference](2026-2601.12241-rapid-power-aware-dynamic-reallocation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル・デコード分離環境でGPU台数だけでなく電力上限も段階間で再配分し、待ち行列とTTFT/TPOTを見ながら電力移動→GPU役割変更の順でSLO達成率を維持するRAPIDを実機評価する。

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

- **2026-09 · [Latency-Aware Orchestration for Multi-Agent LLM Workflows on Heterogeneous GPUs](2026-2609.03335-latency-aware-multi-agent-orchestration-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  依存するエージェント処理グラフから近接後続を先読みし、モデルの常駐・読込・解放と異種GPU配置・実行順を共同で決めて、モデル待ちと不要なGPU占有を減らす。

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

- **2026-09 · [Adaptive Context Parallelism for Production LLM Serving](2026-2609.04774-vertumnus-adaptive-context-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  接頭辞キャッシュ後の残計算量とワーカー混雑を測り、要求ごとの文脈並列度とクラスタのCP分割・統合を数秒単位で変えて、短文の通信費と長文の計算待ちを減らす。

- **2026-08 · [When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference](2026-2608.03741-heteropanacea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル/デコードと注意/FFNを最大4段へ分離するシミュレータで、計算性能・メモリ帯域・通信費の異なる装置配置を比較し、分離が有利な資源条件を測定する研究。

- **2026-08 · [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](2026-2608.25523-topas-workflow-aware-prefix-state-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント接頭辞KVの常駐と要求投入を共有GPUメモリ下で共同決定し、DAGの残存クリティカルパス、将来再利用、移動・プリエンプト費用を比較してタスク完了時間を短縮する。

- **2026-08 · [Pallas: A Proactive KV Cache Migration Framework for LLM Inference in AI-RAN](2026-2608.16477-pallas-proactive-kv-cache-migration-ai-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハンドオーバー時刻を予測し、古いKVは移動先で再計算しつつ新しく増えるKVだけを送信元からストリームして、切替時の全量転送待ちと遠回り生成を減らす。

- **2026-08 · [P-PAS: Prefill-Pressure Adaptive Scheduling for Long-Context LLM Serving](2026-2608.15171-p-pas-prefill-pressure-adaptive-scheduling.md)**  
  実装：[✓](https://github.com/TimoSaemann/ppas-vllm) ・ リポジトリ内被引用：0  
  プリフィルとデコードの同時圧力を観測し、vLLMの1反復トークン予算を低圧力では大きく高圧力では小さく切り替えて、固定分割の競合待ちと過剰な起動費を減らす。

- **2026-08 · [OpScale: Operator-level Provisioning and Autoscaling for LLM Serving](2026-2608.13499-opscale-operator-level-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル全体ではなく演算子単位で供給・配置・実行時伸縮を行い、負荷に応じて現在の律速演算子だけへGPU資源を追加するLLM配信基盤。

- **2026-08 · [From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems](2026-2608.15127-agentsysbench.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントのLLM呼出しだけでなくツール・検索・サンドボックス・状態・通信を含む実行を測定し、トークン速度だけでは捉えられない待ち時間と資源競合がどこで生じるかを明らかにしたベンチマーク。

- **2026-08 · [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](2026-2608.06557-cascade-slo-aware-latency-budget-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求の残りSLO遅延を実行順とKVのHBM・CPU DRAM・NVMe配置へ共通予算として配り、復元・先読み・保持・再計算を切り替えて、処理量と長文脈要求の公平性を両立するサービング。

- **2026-07 · [X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding](2026-2609.09166-x-cosd-cross-vocabulary-collaborative-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末SLMとサーバLLMの語彙が異なっても、残差分布を共通語彙・LLM専用語彙へ分け、少数の置換候補だけを通信して厳密な協調投機的デコードを行う方式。

- **2026-07 · [Towards Load-Aware Prefill Deflection for Disaggregated LLM Serving](2026-2607.02043-kairos-load-aware-prefill-deflection.md)**  
  実装：[✓](https://github.com/sudokara/Kairos) ・ リポジトリ内被引用：0  
  プリフィルGPUの混雑時にデコードGPUの余力へプリフィルを小分けで差し込み、トークン間時間のSLOを超えない範囲で要求を移して、プリフィル待ちとKV転送を減らす。

- **2026-07 · [Sangam: Efficiently Serving Diffusion LLMs with the AR Stack](2026-2607.04206-sangam-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/UT-InfraAI/sangam) ・ リポジトリ内被引用：0  
  拡散LLMの不可分な再プリフィルをデコードの残りトークン予算と繰越不足額で受け入れ、プリフィル混雑時だけデコードGPUへ溢れさせて、待ち時間と資源偏りを抑える。

- **2026-07 · [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長分布のずれを考慮し、プリエンプション損失と未使用HBM損失からKV予約量を求め、GPU構成・要求振り分け・接頭辞キャッシュを再最適化して容量浪費と追い出しを減らす。

- **2026-07 · [Online Linear Programming for Multi-Objective Routing in LLM Serving](2026-2607.03948-online-linear-programming-multi-objective-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各デコードワーカーの将来バッチ枠とKV容量へ影価格を付け、SLO報酬が資源費を上回る要求だけをルーティングして、平均・末尾遅延とスループットの優先順位を切り替える。

- **2026-07 · [ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving](2026-2607.00466-eldr-expert-locality-decode-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル時のMoEエキスパート活性化から署名を作り、似た署名の要求を同じデコードGPUへ集めて一括読込する専門家重みの種類を減らし、TPOTのばらつきを抑える。

- **2026-07 · [Akashic: A Low-Overhead LLM Inference Service with MemAttention](2026-2607.05708-akashic-memattention-memory-service.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長期エージェント履歴を1024トークン級チャンクへ共同圧縮し、関連チャンクだけを検索・再統合してNVMe上でも近接配置することで、再入力量とメモリI/Oを減らす。

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

- **2026-06 · [FlexNPU: Transparent NPU Virtualization for Dynamic LLM Prefill-Decode Co-location](2026-2606.04415-flexnpu-transparent-virtualization-dynamic-pd-colocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AscendCL操作を仮想ハンドル経由で物理NPUへ転送し、プリフィルとデコードの待機・実行時間・帯域圧力を測って実行比率を動的に変え、静的PD配置の資源偏りとTTFT待ちを減らす。

- **2026-06 · [Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs](2026-2606.30391-energy-aware-scheduling-for-serverless-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有GPU上の複数LLMについて、要求配置・SM分割・GPU周波数・低負荷時集約をSLO制約下で協調し、同居モデルの周波数不一致を避けてクラスタ全体の推論エネルギーを削減するサーバレス制御方式。

- **2026-06 · [Beyond Prediction: Tail-Aware Scheduling for LLM Inference](2026-2606.18431-tail-aware-prediction-free-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長予測を使わず、既得サービス量と末尾分布から要求優先度を調整し、KVを壊す頻繁なプリエンプトを幾何学的に制限して平均ではなくP95/P99遅延を安定化する。

- **2026-05 · [Towards Multi-Model LLM Schedulers: Empirical Insights into Offloading and Preemption](2026-2605.19593-multi-model-offloading-preemption-schedulers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  限られたGPUで複数モデルを切り替える推論について、GPUに置く層の割合を連続掃引し、KV退避・モデル解放・重み再読込・KV復元の費用を分解して、オフロード感度と切替ボトルネックを測定した研究。

- **2026-05 · [Towards Distributed Inference of LLMs on a P2P Network](2026-2606.17059-p2p-prefix-cache-aware-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散LLMサービングで各ノードの接頭辞KV基数木を交換し、キャッシュを持つノードへ要求を移すP2Pルーティングでプリフィル再計算を減らすが、転送遅延と負荷集中も測定する。

- **2026-05 · [Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference](2026-2605.02329-taming-request-imbalance-slo-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離で、各要求のTTFT/TPOT目標までの余裕を測り、余裕のない要求を先にプリフィルし、余裕内だけ短いデコード要求を選んで長い要求の先頭待ちと同期遅延を減らすSLOスケジューラ。

- **2026-05 · [STAR: Decode-Phase Rescheduling for LLM Inference](2026-2510.13668-star-decode-phase-rescheduling-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離後も変動する生成長を最終層の隠れ状態から軽量MLPで継続予測し、KV移送費を回収できる要求を過負荷GPUから低負荷GPUへ移して、長出力の負荷偏りと尾部遅延を減らす再配置機構。

- **2026-05 · [Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server](2026-2609.05425-cotail.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU制御段階のP95/P99遅延からスケジューラ競合とNUMA・キャッシュ競合を診断し、リアルタイム優先度またはCPU配置分離を選んで同居ワークロードによるLLM遅延を減らす。

- **2026-04 · [TENT: A Declarative Slice Spraying Engine for Performant and Resilient Data Movement in Disaggregated LLM Serving](2026-2604.00368-tent-declarative-slice-spraying-data-movement.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：0  
  KVキャッシュなどの大容量転送を細粒度スライスへ分け、実時間の混雑や障害に応じてRDMA・NVLink等の複数経路へ動的分散し、分離型LLMサービングの帯域利用と障害回復を改善する転送基盤。

- **2026-04 · [Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC](2026-2604.07609-blink-cpu-free-llm-inference-gpu-smartnic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  定常状態のLLM推論でCPUが行うバッチ更新・KV管理・GPU起動をGPU常駐制御へ移し、要求受付とトークン送受信をSmartNICへ分離して、CPU干渉によるGPU待ちとコピー待ちを減らす実機システム。

- **2026-03 · [Understand and Accelerate Memory Processing Pipeline for Large Language Model Inference](2026-2603.29002-memory-processing-pipeline-gpu-fpga.md)**  
  実装：[✓](https://github.com/OswaldHe/HeteroLLM) ・ リポジトリ内被引用：0  
  疎注意・RAG・圧縮メモリを4段階の共通メモリ処理へ分解し、不規則・メモリ律速部分をFPGA、密計算をGPUへ割り当てて長文推論の遅延と消費エネルギーを削減する異種実行方式。

- **2026-03 · [PrefixWall: Mitigating Prefix Caching Side Channels in Shared LLM Systems](2026-2603.10726-cachesolidarity-prefix-cache-side-channel-defense.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PrefixWallは、共有自動接頭辞キャッシュのヒット・ミス遅延から他利用者の入力を推測される副チャネルを検出し、異なる利用者間で再利用された接頭辞の先だけを再計算へ切り替えることで、完全分離よりキャッシュ再利用を残す防御。

- **2026-03 · [Multi-stage Flow Scheduling for LLM Serving](2026-2603.17456-multi-stage-flow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MFSは、遠隔KV取得・集団通信・プリフィルからデコードへの転送を依存付きの段階として追跡し、余裕のある通信を遅らせ、締切が近いフローを逆多段キューで昇格してTTFTのSLO違反を減らすネットワークスケジューラ。

- **2026-03 · [Cost-Efficient Multimodal LLM Inference via Cross-Tier GPU Heterogeneity](2026-2603.12707-cost-efficient-multimodal-llm-inference-via-cross-tier-gpu-heterogeneity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像符号化をRTX 4090、言語生成をA100へ分離し、KVキャッシュではなく数MB級の画像埋め込みだけをPCIe転送することで、異種GPUを使った低コストなマルチモーダルLLMサービングを実現する。

- **2026-03 · [CALVO: Improve Serving Efficiency for LLM Inferences with Intense Network Demands](2026-2603.21257-calvo-network-aware-kv-loading-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔KV読み込みを独立した非同期段階へ分離し、通信時間と計算時間を合わせた要求費用で順序付けすることで、長文脈の高キャッシュ再利用環境で平均最初のトークン時間を81.3%以上短縮し、期限達成率を最大61.67%改善する。

- **2026-02 · [Multi-Layer Scheduling for MoE-Based LLM Reasoning](2026-2602.21626-multi-layer-scheduling-moe-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gimbalは、MoEサービングで実測KV使用量から要求の送り先、入力長からエンジン内の実行順、専門家の活性頻度と層間依存からGPU配置を決め、容量偏り・先頭待ち・専門家集中をまとめて減らす三層スケジューラ。

- **2026-02 · [Large-Scale LLM Inference with Heterogeneous Workloads: Prefill-Decode Contention and Asymptotically Optimal Control](2026-2602.02987-prefill-decode-contention-optimal-control.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模LLM推論で異なる入力・出力長の要求を混在処理する際、実測反復時間からプリフィル混在/デコード単独のサービス率を求め、流体最適化の占有率に追従してプリフィル受入れとデコード配置をゲート・ルート制御する研究。

- **2025-10 · [From Principles to Practice: A Systematic Study of LLM Serving on Multi-core NPUs](2025-2510.05632-systematic-study-multicore-npu-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチコアNPU向け多層シミュレータで、テンソル分割・コア配置・SRAM/HBM管理・プリフィルとデコードの分離/融合をQwen3各サイズで比較し、入力長・通信競合・負荷構成ごとに有利な設計を明らかにする研究。

### 2年前（2024-10〜2025-09）

- **2025-04 · [MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism](2025-2504.02263-megascale-infer-disaggregated-expert-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  注意機構とMoE専門家FFNを別GPU群へ分離し、複数注意レプリカから専門家要求を集約して大きな専門家バッチを作り、専用多対多RDMA通信とピンポン型パイプラインで通信を隠す大規模MoEサービング方式。

- **2025-07 · [Oneiros: KV Cache Optimization through Parameter Remapping for Multi-tenant LLM Serving](2025-2507.11507-oneiros-parameter-remapping-multitenant-serving.md)**  
  実装：[✓](https://github.com/UT-SysML/Oneiros/) ・ リポジトリ内被引用：4  
  複数LLMを同じGPUで提供すると、KVキャッシュ不足をCPU退避で解決する方法は毎トークンの転送と同期でデコードを止める。Oneirosは不変なモデルパラメータをCPUへ移し、空いたGPUページをKVキャッシュへ転用し、重み読込みをGPU計算に重ねて停滞を抑える。

- **2025-04 · [Optimizing LLM Inference: Fluid-Guided Online Scheduling with Memory Constraints](2025-2504.11320-fluid-guided-online-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  流体平衡からデコード進捗区間ごとのGPU常駐構成を見積もり、WAIT/Nested WAITで制御する。未知の出力長は予測せず、生成を継続する残存要求を段階分類してKV追い出し連鎖を抑えるスケジューラ。

- **2025-01 · [Mell: Memory-Efficient Large Language Model Serving via Multi-GPU KV Cache Management](2025-2501.06709-mell-multi-gpu-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  複数GPUでLLMを提供すると、要求ごとの出力長の違いでKVキャッシュが一方のGPUだけに膨らみ、空きGPUを使えない。Mellは実行中要求をGPU間で移し、通信余力があればKV本体を転送し、演算余力があればトークンだけを送り移行先で再プリフィルして偏りを抑える。

- **2025-01 · [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  クライアントごとのサービス量を公平に保ちつつ、公平性が大きく崩れない範囲だけ実行順を入れ替えて、同じ接頭辞を持つリクエストを続けて処理しKV再利用を増やすスケジューラ。複数GPUでは負荷分散も同時に調整する。

- **2025-09 · [Parallax: Efficient LLM Inference Service over Decentralized Environment](2025-2509.26182-parallax-decentralized-heterogeneous-serving.md)**  
  実装：[✓](https://github.com/GradientHQ/parallax) ・ リポジトリ内被引用：1  
  地理的に離れた異種GPUでモデル層を地域・VRAM・計算性能に合わせて配置し、GPUごとの処理時間と通信遅延から要求ごとの層経路を選ぶことで、遅いGPU・低速回線によるパイプライン待ちを減らす分散LLMサービング。

- **2025-09 · [Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism](2025-2509.08309-hetis-heterogeneous-gpu-dynamic-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異種GPUの遅い機種を密演算経路から外し、デコード注意をヘッド単位で動的分配してKVキャッシュも部分移行することで、計算・通信・メモリの不均衡を同時に抑えるLLMサービング方式。

- **2025-01 · [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話型リクエストの遅延目標を守りながら余ったGPU容量をバッチリクエストへ使うため、各GPUで同時処理するリクエスト数を素早く増減する制御と、クラスタ全体のGPUインスタンス数を遅い周期で増減する制御を分けたLLM自動スケーラ。

### 3年前（2023-10〜2024-09）

- **2024-01 · [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)**  
  実装：[✓](https://github.com/LLMServe/DistServe) ・ リポジトリ内被引用：120  
  プリフィルとデコードを別GPU群へ分け、それぞれのGPU数・モデル分割方法・配置場所を、最初のトークンまでの時間とその後のトークン間隔の目標に合わせて別々に決めることで、両処理段階の干渉をなくす推論提供システム。

- **2023-11 · [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)**  
  実装：[✓](https://github.com/Mutinifni/splitwise-sim) ・ リポジトリ内被引用：114  
  プリフィルとデコードを別の計算機群へ分け、それぞれに向くGPU世代・電力設定・台数を使い分けて、クラスタ全体のスループット・コスト・消費電力を改善するサービング設計。

- **2023-12 · [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)**  
  実装：[✓](https://github.com/sgl-project/sglang) ・ リポジトリ内被引用：106  
  複数のLLM呼び出しや条件分岐をランタイムが1つのプログラムとして理解し、共有接頭辞のKV再利用・並列実行・構造化出力生成をまとめて効率化する推論システム。

- **2024-03 · [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)**  
  実装：[✓](https://github.com/microsoft/sarathi-serve) ・ リポジトリ内被引用：96  
  長いプリフィルを小さい分割片へ分け、毎回まず進行中要求のデコードトークンを処理し、残った総トークン枠へプリフィルを入れることで、新要求を受けながらデコードの長時間停止を防ぐ推論提供スケジューラ。

- **2024-07 · [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：63  
  プリフィルとデコードを別GPU群へ分け、クラスタ内のCPU DRAM・SSDへ過去KVを保存して別ノードからも再利用できるようにし、KV取得時間・待ち行列待ち・残りプリフィル計算を比較してリクエストの実行先を決める大規模な推論提供システム。

- **2024-03 · [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：49  
  複数ターン会話の過去KVを要求終了後もDRAM / SSDへ保存し、次ターンで使う層のKVを少し前からGPUへ戻すことで、履歴全体の再プリフィルと記憶装置待ちを減らす状態保持型推論提供手法。

- **2024-06 · [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)**  
  実装：[✓](https://github.com/AlibabaPAI/llumnix) ・ リポジトリ内被引用：32  
  実行中要求のKVキャッシュを別モデル実行単位へ段階的に移し、GPU間の混雑差・メモリ不足・優先度変更・実行単位削減が起きた後でも要求配置を修正できる複数実行単位の推論提供スケジューラ。

- **2024-05 · [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  同じプレフィックスのKVをすでに持つGPUへリクエストを送ればプリフィルを省ける一方、そのGPUだけ混むことがあるため、KV再利用で節約できる計算時間とGPUの混雑による待ち時間を比較してリクエストの送り先を決めるdistributed サービング スケジューラ。

- **2024-06 · [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  プリフィルとデコードを別実行単位へ分ける推論提供で、GPU / CPU上のKVキャッシュを実行単位横断で検索・共有・転送できる共通メモリプールを作り、過去接頭部の再利用と処理段階間KV移動を同じ仕組みで扱うシステム。

- **2024-01 · [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)**  
  実装：[✓](https://github.com/ServerlessLLM/ServerlessLLM) ・ リポジトリ内被引用：18  
  要求到着時にモデルをGPUへ読み込むサーバーレス環境で、チェックポイントをGPU近くのSSD / DRAMへキャッシュし、高速読み込み器とモデル所在地を考慮した要求配置、生成途中要求の移動を組み合わせてモデル起動待ちを短縮するシステム。

- **2024-01 · [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed-MII) ・ リポジトリ内被引用：18  
  長いプリフィルを小さく分割し、短いプロンプト・プリフィル 分割片・デコード トークンを毎回ほぼ同じ総トークン数になるよう混ぜることで、長いプリフィルがデコードを止める時間を抑えつつGPUを効率よく使うLLM 提供処理 システム。

- **2023-12 · [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)**  
  実装：[✓](https://github.com/Ying1123/VTC-artifact) ・ リポジトリ内被引用：18  
  仮想 トークン Counter（VTC）は、要求数ではなくクライアントごとに実際に処理した入力・出力トークンをサービス量として数え、累積サービス量が少ないクライアントから新しい要求を実行バッチへ入れる。空きGPUを意図的に遊ばせず、公平性と高い利用率を両立することを狙う。

- **2023-12 · [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  複数往復会話の過去KVキャッシュをリクエスト終了後もGPU / CPUへ残し、次の往復で同じ履歴を再びプリフィルする計算を避ける状態保持型LLM提供処理システム。

- **2023-11 · [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)**  
  実装：[✓](https://github.com/Hsword/SpotServe) ・ リポジトリ内被引用：16  
  安価だが突然利用できなくなるスポットGPU（spot GPU）の増減に合わせてモデルの分割方法を組み替え、既存の重み（重み）とKVキャッシュ（KV キャッシュ）をできるだけ再利用してLLMサービングを継続するシステム。

- **2024-08 · [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  最終的な出力トークン数を正確に当てる代わりに、プロンプトからどのリクエストが他より短く終わりそうかという順位だけを小型モデルで予測し、短そうなリクエストを先に処理して長いリクエストによるキュー待ちを減らすスケジューラ。

- **2024-05 · [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)**  
  実装：[✓](https://github.com/microsoft/ParrotServe) ・ リポジトリ内被引用：14  
  複数LLM呼び出しから成るアプリケーションについて、どの呼び出しの出力を次の呼び出しが使うか、どのプロンプト部分を共有するかをバックエンドへ伝え、アプリケーション全体を見て並列実行・バッチ処理・接頭部 KV再利用を調整する推論提供システム。

- **2024-02 · [INFERCEPT: Efficient Intercept Support for Augmented Large Language Model Inference](2024-2402.01869-infercept-intercept-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  外部ツールや人間応答を待つ間に生成が中断される拡張LLMで、KVキャッシュをGPUに保持する、CPUへ退避する、破棄して再計算するという三つの選択肢を、GPUメモリの時間積で表した浪費量を基準に要求ごとに切り替える推論基盤。

- **2024-06 · [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)**  
  実装：[✓](https://github.com/QLM-project/QLM) ・ リポジトリ内被引用：9  
  対話的 / バッチ要求や複数モデルを同じクラスタで扱うとき、各要求グループがあと何秒待てるかとモデルがどのGPUに載っているかを見て、待ち行列順序と実行先を組み替え、遅延目標を守れる要求数を増やすシステム。

- **2024-04 · [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LLMのストリーミング応答を単純な生成速度ではなく、最初のトークンが早く届き、その後もユーザーが読む速度に間に合うようトークンが途切れず届くかで評価し、十分先まで生成済みの要求を一時停止して、今すぐGPU時間が必要な要求へ回す推論提供システム。

- **2024-08 · [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  P/D-Serveは、事前充填と復号を別インスタンス群へ分け、シナリオごとにP/D比を調整し、混雑ノードを待たず要求を再送し、KV転送をまとめることで数万NPUクラスタの待ち行列と通信固定費を減らす商用基盤。

### 4年前（2022-10〜2023-09）

- **2023-09 · [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)**  
  実装：[✓](https://github.com/vllm-project/vllm) ・ リポジトリ内被引用：224  
  vLLMは、要求ごとに大きな連続領域を予約していたKVキャッシュを固定長ブロックへ分解し、論理的な並びとGPU上の物理配置を分離する。必要なブロックだけ動的に割り当て、同じ接頭辞のKVを共有することで、限られたGPUメモリへより多くの要求を同時に載せる。

- **2023-02 · [AlpaServe: Statistical Multiplexing with Model Parallelism for Deep Learning Serving](2023-2302.11665-alpaserve.md)**  
  実装：[✓](https://github.com/alpa-projects/mms) ・ リポジトリ内被引用：36  
  複数モデルへ届くリクエスト数が時間ごとに偏る環境で、モデルを複数GPUへ分割して置き、空いているGPUをモデル間で共有しやすくすることで、特定モデルだけ待ち行列が伸びるのを抑えるサービング配置手法。

- **2023-05 · [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)**  
  実装：[✓](https://github.com/LLMServe/FastServe) ・ リポジトリ内被引用：34  
  出力トークンを1つ生成する区切りで要求（リクエスト）を一時停止・再開できるようにし、短い要求を優先しながらKVキャッシュ（KV キャッシュ）をCPUへ退避・先読みして待ち時間を減らすLLMサービングスケジューラ（serving スケジューラ）。

### 5年前（2021-10〜2022-09）

- **2022-07 · [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：115  
  出力トークンを1個生成するたびにスケジューラへ制御を戻し、終わった要求を外して新着要求を追加する。さらに、長さの違う要求を同じバッチで処理できるよう、注意機構だけを要求ごとに分け、それ以外の演算はトークン単位でまとめて実行する分散LLMサービングシステム。
<!-- survey:auto:end -->
