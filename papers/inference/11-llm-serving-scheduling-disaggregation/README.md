# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（526本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/11-llm-serving-scheduling-disaggregation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：269  
  Mooncakeは、大規模言語モデル（Large Language モデル、LLM）の推論サービスで、GPUの計算能力とメモリを同時に効率よく使うための分散サービング基盤である。中心にあるのは、KVの所在と移動費用を知る全体スケジューラ（Global Scheduler）であるConductorである。

- **2025-11 · [Continnum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](2025-2511.02230-continuum-agent-kv-cache-ttl-scheduling.md)**  
  実装：[✓](https://github.com/Hanchenli/vllm-continuum) ・ リポジトリ内被引用：48  
  ツール呼出しを挟む多ターンLLMエージェントで、ツール待ち時間・KV再構築費用・残りターンを見てKVキャッシュの保持期限を動的に決め、短い待ちではGPUに固定し長い待ちでは解放してターン間待ちを減らすスケジューラ。

- **2026-07 · [Kimi K3: Open Frontier Intelligence](2026-2607.24653-kimi-k3-open-frontier-intelligence.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  KDA状態とMLAのKVを統合する接頭辞キャッシュ、512トークン境界の再利用、クラスタ親和ルーティングを記述するKimi K3技術報告。配信機構は具体的だが、節内に比較測定はない。

- **2025-12 · [TraCT: Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale](2025-2512.18194-tract-rack-scale-cxl-shared-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  CXL Type-3共有メモリをプリフィル・デコード間KV転送路とラック共有接頭辞キャッシュに兼用し、GPU–CXL直接DMAでRDMAのNICホップを除去するサービング方式。

- **2026-09 · [GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving](2025-2508.16449-greenllm-slo-aware-dvfs-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  GreenLLMは、プリフィルとデコードの負荷を入力長・出力TPS・P95トークン間時間から観測し、各段階のSLO内でGPU周波数を別々に選ぶ二重帰還制御により、過剰な高周波数動作とエネルギーを減らす。

- **2026-04 · [SkyWalker: A Locality-Aware Cross-Region Load Balancer for LLM Inference](2026-2505.24095-skywalker-cross-region-load-balancer.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  地域ごとに異なるLLM推論需要を別地域へ逃がしつつ、接頭辞木でKVキャッシュ共有と要求待ち行列を見て経路を選び、同等処理量を9台で達成して費用を25%削減する。

- **2026-04 · [Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter](2026-2604.15039-prefill-as-a-service-cross-datacenter-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  KVキャッシュ量が小さいハイブリッド注意機構を利用し、長い未キャッシュ入力のプリフィルだけを遠隔GPU群へ振り分け、KVをデータセンター間転送して異種GPU資源の利用効率と処理能力を高める。

- **2026-01 · [Concur: Proactive Agent-Level Admission Control for Efficient Agentic Batch Inference](2026-2601.22705-concur-agentic-admission-control.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  非同期エージェントのKV接頭辞がLRU追い出しと再計算を繰り返す中盤スラッシングを、KV使用率・ヒット率を混雑信号にしたエージェント単位の加算増加・乗算減少型受入れ制御で未然に抑える方式。

- **2025-12 · [TokenScale: Timely and Accurate Autoscaling for Disaggregated LLM Serving with Token Velocity](2025-2512.03416-tokenscale-token-velocity-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  プリフィル・通信・デコードを共通の「トークン速度」で観測し、突発負荷では既存デコードGPUを一時的なプリフィル処理へ転用して、新規GPU起動の遅れを埋める自動スケーリング方式。

- **2026-02 · [DualMap: Enabling Both Cache Affinity and Load Balancing for Distributed LLM Serving](2026-2602.06502-dualmap-enabling-both-cache-affinity-and-load-balancing-for-distributed-.md)**  
  実装：[✓](https://github.com/ASISys/DualMap) ・ リポジトリ内被引用：9  
  DualMapは、分散LLM推論でプロンプト接頭辞のKVキャッシュを再利用したいという要求と、各推論インスタンスへ負荷を均等に分けたいという要求の衝突を解く配車方式である。ICLR 2026の論文は、vLLMを用いた分散推論クラスタで実際の会話・ツール利用負荷を評価し、同じTTFT目標を満たす有効要求容量を既存方式比で最大2.25倍に改善したと報告する。

- **2026-04 · [Introspective Diffusion Language Models](2026-2604.11035-introspective-diffusion-language-models.md)**  
  実装：[✓](https://github.com/Introspective-Diffusion/I-DLM) ・ リポジトリ内被引用：8  
  本論文は、拡散言語モデル（diffusion language モデル; DLM）が複数トークンを同時に提案できるにもかかわらず、同規模の自己回帰言語モデル（autoregressive language モデル; ARモデル）より推論品質が低く、複数要求を処理する実運用で期待ほど高速化しない原因を、生成アルゴリズムと推論エンジンの双方から調べる。

- **2026-03 · [Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving](2026-2603.18897-paste-pattern-aware-speculative-tool-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  反復する道具系列と引数依存から次の具体的な道具呼出しを先行実行し、言語モデル側の混雑も共同制御して平均タスク完了時間を最大43.5%削減する。

- **2026-02 · [vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models](2026-2602.02204-vllm-omni-fully-disaggregated-multimodal-serving.md)**  
  実装：[✓](https://github.com/vllm-project/vllm-omni) ・ リポジトリ内被引用：8  
  複数LLM・拡散モデル・音声/画像生成器を段階グラフへ分解し、各段階を独立バッチ・独立GPU配置・共通コネクタで実行することで、any-to-any型マルチモーダル推論を単一モデル用サービング基盤から拡張する方式。

- **2026-01 · [LLM-42: Enabling Determinism in LLM Inference with Verified Speculation](2026-2601.17768-llm42-verified-speculation-deterministic-inference.md)**  
  実装：[✓](https://github.com/microsoft/llm-42) ・ リポジトリ内被引用：8  
  動的バッチの高速カーネルで先に生成し、固定形状の再実行でトークンとKVを検証・巻き戻すことで、要求単位の決定性をカーネル全面書換えなしに保証する。

- **2026-02 · [Efficient Multi-round LLM Inference over Disaggregated Serving](2026-2602.14516-ampd-multi-round-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  多ラウンド推論の追加プリフィルを、実行時負荷に応じてデコード側の局所実行かプリフィル側の遠隔実行へ振り分け、待ち行列の並べ替えとGPU配備計画を組み合わせてSLO達成率を高める分離サービング方式。

- **2025-11 · [Chameleon: Adaptive Caching and Scheduling for Many-Adapter LLM Inference Environments](2024-2411.17741-chameleon-adapter-caching-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  多数LoRA提供で生じるアダプタ転送競合と要求時間のばらつきを、動的GPUアダプタキャッシュとサイズ認識型複数キュースケジューリングの協調で抑え、高負荷時のP99初回トークン時間を80.7%削減する。

- **2026-04 · [fabric-lib: RDMA Point-to-Point Communication for LLM Systems](2026-2510.27656-fabric-lib-rdma-point-to-point-communication-for-llm-systems.md)**  
  実装：[✓](https://github.com/perplexityai/pplx-garden) ・ リポジトリ内被引用：6  
  fabric-libは、大規模言語モデルの分離推論、混合専門家モデルのトークン配送、非同期強化学習における重み更新を、異なるネットワーク機器でも共通の遠隔直接メモリアクセス（Remote Direct メモリ Access、RDMA）操作で実行する通信基盤である。

- **2026-02 · [Predicting LLM Output Length via Entropy-Guided Representations](2026-2602.11812-predicting-llm-output-length-via-entropy-guided-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  生成長を事前に予測して近い長さの要求をまとめればこの無駄を減らせるが、既存法はDistilBERTのような補助モデルを別途動かすため、追加遅延とGPUメモリを消費する。

- **2026-02 · [FLYING SERVING: On-the-Fly Parallelism Switching for Large Language Model Serving](2026-2602.22593-flying-serving-online-dp-tp-switching.md)**  
  実装：[✓](https://github.com/Picomp-lab/Flying-Serving) ・ リポジトリ内被引用：6  
  同じGPU常駐重みとKV物理プールをゼロコピーの論理ビューでDP↔TP切替し、15msのオンライン再構成で高負荷時のDP処理量と低負荷・長文時のTP遅延/容量を使い分ける方式。

- **2026-01 · [A Universal Load Balancing Principle and Its Application to Large Language Model Serving](2026-2601.17855-universal-load-balancing-principle-llm-serving.md)**  
  実装：[✓](https://github.com/Echoscd/Load-Balancing-Release) ・ リポジトリ内被引用：6  
  同期障壁で最遅GPUに全体が律速されるデータ並列デコードを、短期先読み付き整数最適化BF-IOで割り当て直し、256基A100相当のシミュレーションでFCFS比スループット約92%向上・エネルギー約29%削減を示す。

- **2026-07 · [SMetric: Rethink LLM Scheduling for Serving Agents with Balanced Session-centric Scheduling](2026-2607.08565-smetric-session-centric-agent-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  セッションの初回だけ負荷分散し、後続要求はKV局所性を優先しつつ過負荷・キャッシュ消失時だけ再配置することで、エージェント配信のクラスタTPSを10〜16%改善する。

- **2026-07 · [dLLM-Serve: Bridging the Memory Gap in Diffusion Language Model Serving](2026-2512.17077-dllm-serve-bridging-the-memory-gap-in-diffusion-language-model-serving.md)**  
  実装：[✓](https://github.com/chosen-ox/dLLM-Serve) ・ リポジトリ内被引用：5  
  本論文のdLLM-Serveは、出力語彙の計算を小分けにして一時活性値の上限を固定する仕組み、更新局面と再利用局面を同じ実行回に詰め合わせるスケジューラ、注意ヘッドごとに重要なトークンを選びながら鍵・値を物理的に連続配置するキャッシュ管理を統合した。

- **2026-05 · [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](2026-2605.00528-saga.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  エージェントの全ワークフローを単位にKV保持・セッション親和性・公平性を共同制御し、64基A100でタスク完了時間を幾何平均1.64倍短縮する。

- **2026-04 · [Cascadia: An Efficient Cascade Serving System for Large Language Models](2025-2506.04203-cascadia-cascade-serving-routing-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  モデルカスケードの経路選択、GPU資源配分、並列構成を二段階最適化で共同設計し、品質維持下で遅延SLOと処理性能を改善する。

- **2026-03 · [Not All Prefills Are Equal: PPD Disaggregation for Multi-turn LLM Serving](2026-2603.13358-ppd-disaggregation-multiturn-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  複数ターン会話の2ターン目以降について、既存鍵値キャッシュを持つデコードGPUで追加プリフィルするか従来どおりプリフィルGPUへ送るかを遅延目標ごとに動的選択し、後続ターンの初トークン待ち時間と鍵値転送量を大幅に削減する。

- **2026-02 · [OServe: Accelerating LLM Serving via Spatial-Temporal Workload Orchestration](2026-2602.12151-oserve-spatial-temporal-workload-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/LiveServe_Documents-1F54/) ・ リポジトリ内被引用：5  
  要求長の空間的ばらつきと時間変動を予測し、レプリカごとに異なるGPU数・並列方式と要求割当を最大流で共同最適化し、重み再利用による高速配置切替で追随するLLMサービング方式。

- **2026-02 · [DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS](2026-2602.18755-biscale-phase-aware-placement-dvfs.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  DualScaleは、プリフィル・デコード分離のGPU台数・並列度・周波数・振り分け比率を数分単位で配置し、プリフィルの将来待ち行列とデコードのTPOT余裕を反復ごとに制御してSLO内の電力を減らす二段階方式。

- **2025-11 · [DuetServe: Harmonizing Prefill and Decode for LLM Serving via Adaptive GPU Multiplexing](2025-2511.04791-duetserve-adaptive-gpu-multiplexing.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  TBT違反が予測される時だけ単一GPUのSMをプリフィル/デコードへ動的分割し、集約方式のスループットと分離方式のisolationを両立する。

- **2025-11 · [DOPD: A Dynamic PD-Disaggregation Architecture for Maximizing Goodput in LLM Inference Serving](2025-2511.20982-dopd-dynamic-pd-disaggregation.md)**  
  実装：[✓](https://github.com/liao4s/DOPD) ・ リポジトリ内被引用：5  
  負荷予測と解析的な最適P/D比でプリフィル/デコード instanceを動的再構成し、8x H100実機で有効スループット最大1.5倍・SLO達成99.4%を報告。

- **2026-08 · [From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems](2026-2608.15127-agentsysbench.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  エージェントのLLM呼出しだけでなくツール・検索・サンドボックス・状態・通信を含む実行を測定し、トークン速度だけでは捉えられない待ち時間と資源競合がどこで生じるかを明らかにしたベンチマーク。

- **2026-07 · [AugServe: Adaptive Request Scheduling for Augmented Large Language Model Inference Serving](2025-2512.04013-augserve-adaptive-request-scheduling-augmented-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  外部APIや検索を待つ拡張LLMで、停止・再開状態、出力長・外部呼出し時間、KV保持・退避・再計算費用を観測して要求順位と反復トークン予算を変え、先頭待ちとGPUメモリ圧迫を減らすスケジューラ。

- **2026-04 · [PipeLive: Efficient Live In-place Pipeline Parallelism Reconfiguration for Dynamic LLM Serving](2026-2604.12171-pipelive.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  実行中のKVキャッシュ容量とレイヤー配置を動的に組み替え、差分KV同期で停止を約10msに抑えながら、ワークロードに応じたパイプライン並列構成へ切り替えるLLMサービング方式。

- **2026-02 · [Revealing the Challenges of Attention-FFN Disaggregation for Modern MoE Models and Hardware Systems](2026-2602.09721-revealing-the-challenges-of-attention-ffn-disaggregation-for-modern-moe-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  注意計算と専門家FFNを別のGPU群へ配置すると、計算とメモリの資源配分を独立に調整できる。しかしトークンの往復通信が新しい上限を作り、専門家側のGPUを増やすほど全体の演算利用率が下がる場合がある。本研究はその成立条件を数式と実測に基づいて整理する。

- **2026-02 · [BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective Bayesian Optimization](2026-2602.10729-boute-heterogeneous-model-gpu-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  問い合わせごとのモデル振り分けと異種GPU上のモデル配置・並列化を多目的ベイズ最適化で同時に探索し、品質制約下の遅延と運用費を削減する。

- **2025-11 · [ContextPilot: Fast Long-Context Inference via Context Reuse](2025-2511.03475-contextpilot-fast-long-context-inference-via-context-reuse.md)**  
  実装：[✓](https://github.com/EfficientContext/ContextPilot) ・ リポジトリ内被引用：4  
  ContextPilotは、検索拡張生成（Retrieval-Augmented Generation; RAG）、会話記憶、複数エージェントが同じ資料を繰り返し参照する状況で、長文脈の前処理（プリフィル）を減らす推論前段システムである。主要なRAG条件では既存方式比でプリフィル処理率が最大約3倍に改善する。

- **2026-09 · [Astrolabe: Balancing Load in LLM Serving with Randomized Prediction-Guided Scheduling](2025-2508.03611-block-predictive-load-balancing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  出力長予測とインスタンス局所シミュレーションを2択無作為配送へ統合し、KV移送なしでLLMクラスタの負荷分散を改善する。

- **2026-06 · [ReMP: Low-Downtime Runtime Model-Parallelism Reconfiguration for LLM Serving](2026-2606.18741-remp-runtime-model-parallelism-reconfiguration.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  TP/PP切替で重み・KV・通信群・ワーカーを作り直す代わりに、CPU共有重み、二次元KV移送、事前生成通信状態、待機ワーカーを再利用し、数秒で並列構成を変更できるLLMサービング方式。

- **2026-05 · [STAR: Decode-Phase Rescheduling for LLM Inference](2026-2510.13668-star-decode-phase-rescheduling-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  プリフィル・デコード分離後も変動する生成長を最終層の隠れ状態から軽量MLPで継続予測し、KV移送費を回収できる要求を過負荷GPUから低負荷GPUへ移して、長出力の負荷偏りと尾部遅延を減らす再配置機構。

- **2026-05 · [Nitsum: Serving Tiered LLM Requests with Adaptive Tensor Parallelism](2026-2605.05467-nitsum-adaptive-tensor-parallelism-tiered-slo.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多階層SLOの負荷変動に応じてテンソル並列度、プリフィル/デコードGPU配分、要求スケジューリングを同時に切り替え、重み再読込不要化と高速KV移行で再構成をミリ秒級に抑えるLLMサービング方式。

- **2026-05 · [AlignedServe: Orchestrating Prefix-aware Batching to Build a High-throughput and Computing-efficient LLM Serving System](2026-2605.23389-alignedserve-prefix-aware-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  AlignedServeは、長いKV系列を分離するため要求をCPU KVプールへ置き、接頭辞長が近い要求を四分木から密度優先で集め、次バッチのKVをGPU間へ先読みして反復内の待ちと転送待ちを減らす。

- **2026-04 · [StructKV: Preserving the Structural Skeleton for Scalable Long-Context Inference](2026-2604.06746-structkv-preserving-the-structural-skeleton-for-scalable-long-context-in.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案の中心は、全層入次数中心性（Global In-Degree Centrality）、動的転換層検出（動的 Pivot Detection）、構造的伝播と保存予算の分離（Structural Propagation and Decoupling）の三機構である。

- **2026-04 · [Scheduling LLM Inference with Uncertainty-Aware Output Length Predictions](2026-2604.00499-scheduling-llm-inference-with-uncertainty-aware-output-length-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  本論文は、出力長を単一値ではなく確率分布として扱うTIE（Tail Inflated Expectation）スケジューラを提案する。

- **2026-04 · [Foundry: Template-Based CUDA Graph Context Materialization for Fast LLM Serving Cold Start](2026-2604.06664-foundry-cuda-graph-context-materialization.md)**  
  実装：[✓](https://github.com/foundry-org/foundry) ・ リポジトリ内被引用：3  
  CUDAグラフの仮想アドレス配置とカーネルバイナリまで保存し、少数の構造テンプレートから再構築することで、LLMサービングの起動時グラフ捕捉を数分から数秒へ短縮する方式。

- **2026-03 · [Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference](2026-2603.22774-characterizing-cpu-induced-slowdowns-multi-gpu-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多GPU LLM推論でCPUコア不足がトークン化・カーネル発行・NCCL同期・共有メモリ放送を遅らせGPUを遊休させる経路を実機分解し、CPU増強だけでTTFTを最大7.11倍改善できることを示す。

- **2026-01 · [Towards Resiliency in Large Language Model Serving with KevlarFlow](2026-2601.22438-kevlarflow-resilient-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  故障したパイプライン段だけを健全ノードへ動的に差し替え、KVキャッシュを背景複製して処理中要求を継続するLLM配信耐障害化。A10の8/16台クラスタで復旧時間を約30秒まで短縮し、故障時TTFTを最大574.6倍改善。

- **2026-01 · [Power Aware Dynamic Reallocation For Inference](2026-2601.12241-rapid-power-aware-dynamic-reallocation.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  プリフィル・デコード分離環境でGPU台数だけでなく電力上限も段階間で再配分し、待ち行列とTTFT/TPOTを見ながら電力移動→GPU役割変更の順でSLO達成率を維持するRAPIDを実機評価する。

- **2025-12 · [WarmServe: Enabling One-for-Many GPU Prewarming for Multi-LLM Serving](2025-2512.09472-warmserve-one-for-many-gpu-prewarming.md)**  
  実装：[✓](https://github.com/LLMServe/WarmServe) ・ リポジトリ内被引用：3  
  将来負荷を予測して複数モデル重みを同じGPU群へ先行配置し、解放前GPUの未使用KV領域とCUDA仮想メモリ再対応付けを使って、冷間起動を隠しながら本番推論時はGPUを専有させる複数LLM配信方式。

- **2025-12 · [Tangram: Accelerating Serverless LLM Loading through GPU Memory Reuse and Affinity](2025-2512.01357-tangram-serverless-llm-loading-gpu-memory-reuse.md)**  
  実装：[✓](https://anonymous.4open.science/r/Tangram) ・ リポジトリ内被引用：3  
  未使用GPUメモリにモデルのテンソルを残し、KVキャッシュの動的確保とGPU親和性スケジューリングを組み合わせ、サーバレスLLMの再読み込み量とコールドスタート遅延を削減する。

- **2025-12 · [Cornfigurator: Automated Planning for Any-to-Any Multimodal Model Serving](2025-2512.14098-cornserve-efficiently-serving-any-to-any-multimodal-models.md)**  
  実装：[✓](https://github.com/cornserve-ai/cornfigurator) ・ リポジトリ内被引用：3  
  これらを一つのGPU集合へ固定すると遅い構成要素が全体を止め、逆にすべてを分離すると使われないGPUや通信費が増える。実機評価ではQwen 3 Omni、InternVL 3、Qwen 3 VL、Qwen-Imageなどを対象に、既存方式や専門家調整配置と同等または最大6.32倍の有効スループットを報告する。

- **2025-11 · [Pre-Attention Expert Prediction and Prefetching for Mixture-of-Experts Large Language Models](2025-2511.10676-pre-attention-expert-prediction-and-prefetching-for-mixture-of-experts-l.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  そのため演算量を抑えられるが、選択後に必要な重みがGPUに載っていない場合はストレージまたはホストメモリから転送する必要がある。従来の予測方式は前層の状態から次層の選択を予測するため、層をまたぐ変化が誤りになり、最初の層では参照できる前層出力もない。

- **2025-11 · [Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment](2025-6987e5a4e5ec-cauchy-a-cost-efficient-llm-serving-system-through-adaptive-heterogeneou.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  前者は行列積が多く演算性能に依存しやすい一方、後者はモデル重みと鍵値キャッシュ（Key-Value キャッシュ; KVキャッシュ）の読み出しが支配的になり、メモリ帯域に依存しやすい。Cauchyは、計算能力とメモリ帯域が異なるGPUを、プリフィルとデコードへ適切に割り当てる大規模言語モデル配信基盤である。

- **2026-08 · [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](2026-2608.25523-topas-workflow-aware-prefix-state-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  エージェント接頭辞KVの常駐と要求投入を共有GPUメモリ下で共同決定し、DAGの残存クリティカルパス、将来再利用、移動・プリエンプト費用を比較してタスク完了時間を短縮する。

- **2026-08 · [PowerSlider: Exploiting Phase Asymmetry for LLM Serving under Demand Response](2026-2608.21719-powerslider-phase-asymmetry-demand-response.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  入力処理・思考・回答生成の電力感度とKV容量の非対称性を段階別周波数制御、KV予約、GPU割当に利用し、時間変動する電力上限の下でもLLM提供の達成要求率を維持する。

- **2026-07 · [SPORK: Self-Speculative Forking to Accelerate Agentic LLM Inference](2026-2607.03333-spork-self-speculative-forking-agentic-llm.md)**  
  実装：[✓](https://github.com/baihuajun24/spork) ・ リポジトリ内被引用：2  
  主LLM自身をprobeとして分岐し、思考生成中に将来のツール呼出しを先行実行することで外部ツール待ちを隠す。GAIAのQwen3-32BでP95遅延を18%削減し、誤予測時は一致した呼出し接頭辞を再利用する。

- **2026-07 · [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  プリフィル中に重要KVだけを先送りし、デコード時は不足分をローカル読出しと並列取得、残りを背景転送へ回して、全量転送の待ちと部分転送の後続停止を減らす。

- **2026-07 · [Sangam: Efficiently Serving Diffusion LLMs with the AR Stack](2026-2607.04206-sangam-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/UT-InfraAI/sangam) ・ リポジトリ内被引用：2  
  拡散LLMの不可分な再プリフィルをデコードの残りトークン予算と繰越不足額で受け入れ、プリフィル混雑時だけデコードGPUへ溢れさせて、待ち時間と資源偏りを抑える。

- **2026-07 · [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  出力長分布のずれを考慮し、プリエンプション損失と未使用HBM損失からKV予約量を求め、GPU構成・要求振り分け・接頭辞キャッシュを再最適化して容量浪費と追い出しを減らす。

- **2026-07 · [ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving](2026-2607.00466-eldr-expert-locality-decode-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  プリフィル時のMoEエキスパート活性化から署名を作り、似た署名の要求を同じデコードGPUへ集めて一括読込する専門家重みの種類を減らし、TPOTのばらつきを抑える。

- **2026-06 · [SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving with Lookahead Context Engineering](2026-2607.00151-smoothagent-lookahead-context-engineering.md)**  
  実装：[✓](https://github.com/PanZaifeng/SmoothAgent) ・ リポジトリ内被引用：2  
  文脈要約・オフロード・分離を前倒し実行し変換後KVを先に作るlookahead ランタイム。SGLangのSLO-aware スケジューラと組み合わせ、長時間agentの変換点TTFTを最大11.9倍改善。

- **2026-06 · [Observation, Not Prediction: Conversation-Level Disaggregated Scheduling for Agentic Serving](2026-2606.01839-conserve-conversation-level-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  エージェント会話をターン単位で再配置せず、初回プリフィルのKVを一度だけデコードGPUへ移して後続ターンを同じGPUに固定し、再移送と将来長予測の誤差を減らす。

- **2026-06 · [M*: A Modular, Extensible, Serving System for Multimodal Models](2026-2606.12688-mstar-modular-composite-model-serving.md)**  
  実装：[✓](https://github.com/mstar-project/mstar) ・ リポジトリ内被引用：2  
  複合マルチモーダルモデルを構成要素グラフと要求別の『Walk』で宣言し、ループ・並列分岐・ストリーミング・GPU配置を共通実行時へ落とし込むことで、モデルごとの専用配線なしに高性能化する汎用サービング基盤。

- **2026-06 · [Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice](2026-2606.22327-geometry-aware-online-scheduling.md)**  
  実装：[✓](https://github.com/Aurora-Kl/Geometry-Aware-Online-Scheduling) ・ リポジトリ内被引用：2  
  出力長とプロンプト長からKVメモリ占有の時間積分を見積もり、小さいメモリ時間体積の要求を先に実行するSVFを比較して、SJFが無視するKV容量起因の先頭待ちを減らす。

- **2026-06 · [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低頻度MoEモデルの大きなFFN重みを重みGPUへ、変動するKVキャッシュを共有KV GPUへ分離し、モデル間で余剰HBMを融通して長文脈の容量不足とKV競合を減らす。

- **2026-05 · [Towards Distributed Inference of LLMs on a P2P Network](2026-2606.17059-p2p-prefix-cache-aware-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  分散LLMサービングで各ノードの接頭辞KV基数木を交換し、キャッシュを持つノードへ要求を移すP2Pルーティングでプリフィル再計算を減らすが、転送遅延と負荷集中も測定する。

- **2026-05 · [RTP-LLM: High-Performance Alibaba LLM Inference Engine](2026-2605.29639-rtp-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  実運用LLM基盤で、要求をKV位置とGPU負荷に応じて振り分け、プリフィル/デコードを分離し、GPU〜分散ストレージのKV階層・高速読込・投機的復号を統合して待ち時間と容量負荷を減らす。

- **2026-05 · [Coral: Cost-Efficient Multi-LLM Serving over Heterogeneous Cloud GPUs](2026-2605.04357-coral-multi-llm-heterogeneous-cloud-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異種GPU上のモデル内部配置をオフラインの配信テンプレートへ落とし、オンラインでは全モデルの需要・価格・在庫を共同割当することで、費用を最大2.79倍削減し資源逼迫時の有効スループットを最大2.39倍高める。

- **2026-05 · [A Policy-Driven Runtime Layer for Agentic LLM Serving](2026-2605.27744-policy-driven-runtime-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  エージェント識別子を共通座標に観測・採点・予測・作用を推論基盤へ挿入し、オンライン遷移学習を鍵値追い出しと先読みに使ってヒット率と遅延を改善する。

- **2026-04 · [Pythia: Exploiting Workflow Predictability for Efficient Agent-Native LLM Serving](2026-2604.25899-pythia-predictability-driven-agent-native-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  エージェントのワークフロー構造を予測し、接頭辞キャッシュ、要求配置、優先度、モデル複製数を先回り制御して平均完了時間を最大2.9倍短縮。

- **2026-03 · [SLO-Aware Compute Resource Allocation for Prefill-Decode Disaggregated LLM Inference](2026-2603.04716-slo-aware-compute-resource-allocation-for-prefill-decode-disaggregated-l.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LLM推論の事前処理（プリフィル）と逐次生成（デコード）を分離した配備で、要求総トークン量、入力・出力長、初回トークン遅延TTFT、生成トークン間隔TPOTから必要なP/Dインスタンス数を求める方法。

- **2026-03 · [PrefixWall: Mitigating Prefix Caching Side Channels in Shared LLM Systems](2026-2603.10726-cachesolidarity-prefix-cache-side-channel-defense.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  PrefixWallは、共有自動接頭辞キャッシュのヒット・ミス遅延から他利用者の入力を推測される副チャネルを検出し、異なる利用者間で再利用された接頭辞の先だけを再計算へ切り替えることで、完全分離よりキャッシュ再利用を残す防御。

- **2026-03 · [Chimera: Latency- and Performance-Aware Multi-agent Serving for Heterogeneous LLMs](2026-2603.22206-chimera-latency-performance-aware-multi-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異種LLM群で要求難易度、残りワークフロー長、実行中トークン量を同時予測し、モデル選択と待ち行列順序を共同制御して遅延とタスク性能のPareto前線を改善する。

- **2026-02 · [Pancake: Hierarchical Memory System for Multi-Agent LLM Serving](2026-2602.21477-pancake-hierarchical-agentic-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  動的なエージェント記憶向けに多段インデックスキャッシュ、複数エージェント協調インデックス、CPU-GPU協調を統合し、既存メモリ基盤比で端から端まで平均4.29倍超の性能向上を示す。

- **2026-02 · [Large-Scale LLM Inference with Heterogeneous Workloads: Prefill-Decode Contention and Asymptotically Optimal Control](2026-2602.02987-prefill-decode-contention-optimal-control.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模LLM推論で異なる入力・出力長の要求を混在処理する際、実測反復時間からプリフィル混在/デコード単独のサービス率を求め、流体最適化の占有率に追従してプリフィル受入れとデコード配置をゲート・ルート制御する研究。

- **2026-02 · [GORGO: Online Tuning for Cross-Region Network-Aware LLM Serving](2026-2602.11688-gorgo-online-tuning-for-cross-region-network-aware-llm-serving.md)**  
  実装：[✓](https://github.com/atoniolo76/GORGO) ・ リポジトリ内被引用：2  
  接頭辞再利用率だけを最大化すると負荷が一部のサーバーへ集中し、空いているサーバーを選ぶだけでは長い接頭辞を再計算してしまう。地域間の通信遅延が数十〜数百ミリ秒以上変動する場合、二つの指標だけを考慮する方式では、最初のトークンが返るまでの時間を適切に見積もれない。

- **2026-02 · [FlowPrefill: Decoupling Preemption from Prefill Scheduling Granularity to Mitigate Head-of-Line Blocking in LLM Serving](2026-2602.16603-flowprefill-operator-level-preemption.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  演算子境界で事前充填を協調的に割り込み、イベント駆動のSLOスケジューリングと組み合わせて長い要求の先頭待ちを抑え、有効処理量を高める。

- **2026-01 · [EPD-Serve: A Flexible Multimodal EPD Disaggregation Inference Serving System On Ascend](2026-2601.11590-epd-serve-ascend-multimodal-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  マルチモーダル推論をエンコード・事前充填・復号へ三分離し、段階間の非同期特徴量/KV転送、モダリティ別ルーティング、物理同居を組み合わせて、異種段階の干渉を抑えながらSLOと資源効率を改善する。

- **2025-12 · [Reliable and Resilient Collective Communication Library for LLM Training and Serving](2025-2512.25059-r2ccl-resilient-collective-serving.md)**  
  実装：[✓](https://github.com/r2cc-project/R-2CCL) ・ リポジトリ内被引用：2  
  NIC障害時に通信器を再起動せず接続を別NICへ移し、残存帯域に合わせてcollectiveを再配置する耐障害通信ライブラリ。学習1%未満・推論3%未満の障害時オーバーヘッドを報告。

- **2025-12 · [Learned Prefix Caching for Efficient LLM Inference](2025-dac9d9c660d5-learned-prefix-caching-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/yangdsh/LPC) ・ リポジトリ内被引用：2  
  特に複数ターンの会話では、それまでの会話履歴が次の質問にも含まれるため、同じ履歴を再計算しない価値が大きい。一方、GPUメモリは有限で、実行中の要求がKV領域を増やすと保存済みの接頭辞を退避しなければならない。原著のH100・Qwen3-32B-FP8評価では、LRUと同等のヒット率に必要なキャッシュ容量を18〜47%削減した。

- **2025-12 · [CascadeInfer: Length-Aware Scheduling of LLM Serving with Low Latency and Load Balancing](2025-2512.19179-l4-length-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  系列長が近い要求を同じGPU段へ集め、生成で長くなった要求をKVごと後段へ移すスケジューラ。実行時の境界補正と分散負荷再均衡で偏りも抑え、16 GPU評価で主要比較対象より処理率とSLO達成率を改善する。

- **2026-10 · [Characterizing Parallelism Strategies in LLM Inference: Fundamental Compute-Communication Trade-offs](2026-2610.05305-characterizing-parallelism-strategies-in-llm-inference-fundamental-compu.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一方、同じ8基をPP8、PP4TP2、PP2TP4、TP8として割り当てると、長い入力を処理するプレフィルではPP寄りが速く、逐次生成ではTP寄りが速いという反対の傾向が現れる（図8〜9）。

- **2026-09 · [Deadline-Aware Adaptive Prefill Chunking for Efficient Large Language Model Serving](2026-2609.07883-deadline-aware-adaptive-prefill-chunking.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  デコード要求の次トークン期限から残り時間を求め、期限内に入る最大プリフィル塊を反復ごとに二分探索して、固定分割の起動費と一括処理のデコード停止を減らす。

- **2026-09 · [Adaptive Context Parallelism for Production LLM Serving](2026-2609.04774-vertumnus-adaptive-context-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  接頭辞キャッシュ後の残計算量とワーカー混雑を測り、要求ごとの文脈並列度とクラスタのCP分割・統合を数秒単位で変えて、短文の通信費と長文の計算待ちを減らす。

- **2026-08 · [When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference](2026-2608.03741-heteropanacea.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル/デコードと注意/FFNを最大4段へ分離するシミュレータで、計算性能・メモリ帯域・通信費の異なる装置配置を比較し、分離が有利な資源条件を測定する研究。

- **2026-08 · [TokTier: Exact Stateful CPU+GPU Tokenization for Agentic LLM Serving](2026-2607.29678-toktier-stateful-agentic-tokenization.md)**  
  実装：[✓](https://github.com/asu-idi/toktier) ・ リポジトリ内被引用：1  
  長いエージェント会話の追記境界だけを安全検証付きで再トークン化し、再利用不能な大規模入力は厳密GPU経路へ送る方式。参照トークン列との一致を保ちつつ、vLLM統合で中央値TTFTを16〜34%削減する。

- **2026-08 · [Routing LLM Inference to the Cleanest Grid in Real Time](2026-2608.06188-carbon-aware-realtime-inference-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本番の負荷圧力ルータへ絶対MOER由来の可逆な配置補正を重ね、実機二地域で配送失敗なく負荷を移動できることを確認し、19地域・1年再生では仮定依存ながら約23〜51%のGPU運用排出削減余地を示す。

- **2026-08 · [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](2026-2608.06557-cascade-slo-aware-latency-budget-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  要求の残りSLO遅延を実行順とKVのHBM・CPU DRAM・NVMe配置へ共通予算として配り、復元・先読み・保持・再計算を切り替えて、処理量と長文脈要求の公平性を両立するサービング。

- **2026-08 · [CacheRoute: Planned Prefix-Affinity Routing for Large-Scale LLM Serving](2026-2608.19677-cacheroute-prefix-affinity-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キー別要求率から温存対象と安定配置を周期計画し、プレフィックス局所性と負荷均衡を両立して、60基H100の70B評価で3.5秒p99 SLO容量をPreble比2.3倍へ高めるが、親和性が効かない負荷では逆効果になる。

- **2026-07 · [Towards Load-Aware Prefill Deflection for Disaggregated LLM Serving](2026-2607.02043-kairos-load-aware-prefill-deflection.md)**  
  実装：[✓](https://github.com/sudokara/Kairos) ・ リポジトリ内被引用：1  
  プリフィルGPUの混雑時にデコードGPUの余力へプリフィルを小分けで差し込み、トークン間時間のSLOを超えない範囲で要求を移して、プリフィル待ちとKV転送を減らす。

- **2026-07 · [Serving Agentic Workflows with a Physical-Plan Compiler and Adaptive Runtime](2026-2607.02942-dyserve-agentic-physical-plan-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル・検証・実行先をワークフロー全体で共同選択し、混雑度別の事前計画を未送信部分だけ切り替えることで、品質を保ちながらエージェント処理の遅延と有効スループットを改善する。

- **2026-07 · [KV-PRM: Efficient Process Reward Modeling via KV-Cache Transfer for Multi-Agent Test-Time Scaling](2026-2607.09153-kv-prm-efficient-process-reward-modeling-via-kv-cache-transfer-for-multi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ここで$d$は隠れ次元であり、KVの生成自体を省く方式ではない。NVIDIA GH200 120GBで8B・4096トークンの採点は172.0ミリ秒から4.6ミリ秒へ短縮した。

- **2026-07 · [BlockServe: Block-Grained Continuous Batching for High-Throughput Diffusion LLM Serving](2026-2607.08930-blockserve-diffusion-llm-continuous-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散型LLMの要求ごとの収束速度差を、ブロック境界での即時追い出し・異なる拡散状態の混在実行・トークン予算補充で吸収する連続バッチング。Dream/LLaDAでFast-dLLM比1.9〜10.6倍のスループットを報告。

- **2026-06 · [The Price of Anarchy in Disaggregated Inference](2026-2606.17081-price-of-anarchy-disaggregated-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル／デコード分離型サーバーのGPU配分・KV配置・要求経路を三つの相互依存ゲームとして分析し、負荷飽和による効率悪化を実機で測定。TTFTから飽和を検出してルーティングを切り替える制御器をDynamoで評価する。

- **2026-06 · [Solyx AI Grid: Hardware-Telemetry-Aware Routing Across Geographically Distributed GPU Clusters: An Empirical Study of Multi-Site LLM Inference](2026-2606.15050-solyx-hardware-telemetry-geo-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DCGM・vLLM・WANの10信号を圧力値へ統合し、地理分散GPUへの要求重みをxDSで更新する。障害・能力差・ネットワーク揺らぎを単一制御面で扱う。

- **2026-06 · [Service-Induced Congestion in Memory-Constrained LLM Serving](2026-2606.15555-service-induced-congestion-memory-constrained-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  生成中にKVキャッシュが増えるため現時点で安全な受入れが将来の追い出し連鎖を作ることを力学系で示し、要求長の非同期化と受入れ率制限を安定化原理として導く。

- **2026-06 · [RouteBalance: Fused Model Routing and Load Balancing for Heterogeneous LLM Serving](2026-2606.17949-routebalance-fused-routing-load-balancing.md)**  
  実装：[✓](https://github.com/AKafakA/route-balance) ・ リポジトリ内被引用：1  
  モデル選択と実体負荷分散を統合し、要求ごとの品質・予測遅延・費用を同時評価して具体的なモデル実体へ割り当て、異種GPU上の多モデルクラスタで品質と負荷集中を両立して抑える方式。

- **2026-06 · [QCFuse: Query-Aware Cache Fusion via Compressed View for Efficient RAG Serving](2026-2606.05875-qcfuse-query-aware-cache-fusion-via-compressed-view-for-efficient-rag-se.md)**  
  実装：[✓](https://github.com/uYanJX/QCFuse) ・ リポジトリ内被引用：1  
  キャッシュ融合（キャッシュ 融合）は、チャンクごとに事前構築した位置独立キャッシュ（Position-Independent Cache; PIC）を再利用し、重要なトークン位置だけ現在の質問とチャンク順序に合わせて再計算する折衷方式である。

- **2026-06 · [LUMEN: Coordinated Failure Recovery for Distributed LLM Serving](2026-2606.17787-lumen-coordinated-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  障害前の負荷認識キャッシュ保存、障害時の保存局所性と負荷を両立する再配分、モデル再読込中の小型下書きモデルによる投機補助を協調させ、分散大規模言語モデル提供基盤の復旧遅延を縮める方式。

- **2026-06 · [HBM Is Not All You Need: Efficient Disaggregated LLM Serving across Memory-heterogeneous Accelerators](2026-2606.29986-hma-serve-memory-heterogeneous-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  計算律速のプリフィルを安価なGDDR搭載アクセラレータ、メモリ律速のデコードをHBM GPUへ分担し、低精度KVの層別転送と遅延復元で異ベンダー間の形式差と通信待ちを隠す分離配信方式。

- **2026-06 · [Fairness-Aware and Latency-Controllable Scheduling for Chunked-Prefill LLM Serving](2026-2606.09061-fairness-latency-chunked-prefill-scheduling.md)**  
  実装：[✓](https://github.com/Charmstok/Chunked_Prefill_Serving) ・ リポジトリ内被引用：1  
  待ち時間と残りプリフィル量で処理順を更新し、遅延予測でチャンク量を目標時間へ合わせ、同時プリフィル数も制限することで、分割プリフィル配信の公平性と裾遅延を改善する。

- **2026-06 · [Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs](2026-2606.30391-energy-aware-scheduling-for-serverless-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共有GPU上の複数LLMについて、要求配置・SM分割・GPU周波数・低負荷時集約をSLO制約下で協調し、同居モデルの周波数不一致を避けてクラスタ全体の推論エネルギーを削減するサーバレス制御方式。

- **2026-06 · [Enabling Low-Latency, GPU-Efficient Serverless Inference with Model Swapping](2026-7ca899e20e0a-enabling-low-latency-gpu-efficient-serverless-inference-with-model-swapp.md)**  
  実装：[✓](https://github.com/s4-lab-cuhksz/torpor) ・ リポジトリ内被引用：1  
  GPUで機械学習モデルをサーバーレス提供するとき、従来は推論関数を起動時に特定GPUへ結び付け、モデル重みをGPUメモリに保持し続ける方式が一般的だった。実運用パイロット導入では、利用者側の費用が平均70%、事業者側のGPU調達費用が65%削減された。

- **2026-06 · [Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference](2026-2606.23521-concordia-persistent-kernel-checkpointing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU常駐の永続カーネルでKVキャッシュ等の差分を検出・追記保存し、NCCL境界でのチェックポイントとGPU故障復旧をホストCPU依存なしに高速化する耐障害LLM推論基盤。

- **2026-05 · [VibeServe: Can AI Agents Build Bespoke LLM Serving Systems?](2026-2605.06068-vibeserve-agent-generated-bespoke-serving-systems.md)**  
  実装：[✓](https://github.com/uw-syfi/vibe-serve) ・ リポジトリ内被引用：1  
  モデル・ワークロード・ハードウェアごとに複数AIエージェントがLLMサービング基盤を生成し、標準条件ではvLLM相当、特殊条件では予測出力・ハイブリッドキャッシュ・Apple Silicon特化などを自動実装して最大6.27倍高速化する。

- **2026-05 · [Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference](2026-2605.02329-taming-request-imbalance-slo-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル・デコード分離で、各要求のTTFT/TPOT目標までの余裕を測り、余裕のない要求を先にプリフィルし、余裕内だけ短いデコード要求を選んで長い要求の先頭待ちと同期遅延を減らすSLOスケジューラ。

- **2026-05 · [Tackling the Data-Parallel Load Balancing Bottleneck in LLM Serving: Practical Online Routing at Scale](2026-2605.06113-balanceroute-data-parallel-online-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同期障壁を持つデータ並列デコードで、各ワーカーの安全余裕をFスコアで評価して新規要求を割り当て、KV負荷の偏りと障壁待ちを抑えるオンラインルータBalanceRouteを提案する。

- **2026-05 · [PRISM: Fast Online LLM Serving via Scheduling-Memory Co-design](2026-2605.08581-prism-fast-online-llm-serving-via-scheduling-memory-co-design.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共通のシステム指示、同じ検索文書、ツール定義などの区間が何度も現れ、末尾だけが要求ごとに変わる。著者らは単一NVIDIA A800 80GB上のSGLangで実装し、Qwen3-4B-Instruct-2507およびLlama2-13Bを評価した。

- **2026-05 · [Optimus: Elastic Decoding for Efficient Diffusion LLM Serving](2026-2605.24832-optimus-elastic-decoding-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/dubcyfor3/Optimus) ・ リポジトリ内被引用：1  
  拡散LLMのブロックを再学習なしでチャンク化し、GPU飽和と有効トークン率を見ながら復号粒度を動的変更して負荷変動へ追従する。

- **2026-05 · [GoodServe: Towards High-Goodput Serving of Agentic LLM Inferences over Heterogeneous Resources](2026-2605.16867-goodserve-agentic-heterogeneous-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  出力長と各GPUの実効処理能力を予測し、SLOを満たす必要十分なGPUへ割り当て、実行中の違反リスクを軽量移行で補正してグッドプットを最大27.4%改善する。

- **2026-05 · [FATE: Future-State-Aware Scheduling for Heterogeneous LLM Workflows](2026-2605.07238-fate-future-state-aware-workflow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  現在のGPU負荷だけでなく、配置後に残るモデル常駐・親出力局所性・接頭辞再利用を有限先読みで評価し、ワークフローDAGの次段階に有利な状態を残すスケジューラ。

- **2026-05 · [Elastic-dLLM: Position Preserving Context Compression and Augmentation of Diffusion LLMs](2026-2605.18165-elastic-dllm-position-preserving-context-compression-and-augmentation-of.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Elastic-dLLMは、この計算を削減する一方で、各[MASK]の位置情報と終端位置が持つ意味を維持する、追加学習不要の推論時方式である。LLaDA-1.5でElastic単独1.52倍、Fast-dLLMとの併用7.28倍という速度倍率を報告する。

- **2026-05 · [DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Checkpoint/Rollback](2026-2605.22781-deltabox-agent-sandbox-checkpoint-rollback.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ファイルとプロセスの連続状態差分だけを保存し、動的overlay層切替と凍結テンプレートforkを組み合わせて、状態を持つAIエージェントのチェックポイント・ロールバックをミリ秒級にする。

- **2026-04 · [The Energy Cost of Execution-Idle in GPU Clusters](2026-2604.04745-the-energy-cost-of-execution-idle-in-gpu-clusters.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  省電力の試作として、負荷を少数GPUへ集め、残りを深いアイドルへ移す方式を試すと、8 GPUのAzure コードトレース再生でエネルギーを均等分散時の56%まで下げられた。

- **2026-04 · [TENT: A Declarative Slice Spraying Engine for Performant and Resilient Data Movement in Disaggregated LLM Serving](2026-2604.00368-tent-declarative-slice-spraying-data-movement.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：1  
  KVキャッシュなどの大容量転送を細粒度スライスへ分け、実時間の混雑や障害に応じてRDMA・NVLink等の複数経路へ動的分散し、分離型LLMサービングの帯域利用と障害回復を改善する転送基盤。

- **2026-04 · [Sparse Prefix Caching for Hybrid and Recurrent LLM Serving](2026-2605.05219-sparse-prefix-caching-hybrid-recurrent.md)**  
  実装：[✓](https://github.com/arabel1a/sparse-prefix-caching) ・ リポジトリ内被引用：1  
  再帰型・ハイブリッドLLMの共有接頭辞へ内部状態検査点を疎配置し、O(NM)動的計画法でメモリと正確な再計算の交換関係を最適化する。

- **2026-04 · [RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving](2026-2604.10907-routerwise-resource-allocation-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU割当とプロンプト振り分けを構成別遅延モデルと双対価格で共同最適化し、同一クラスタでも配備構成がSLO下の達成品質を最大87%変えることを示す。

- **2026-04 · [Dual-Pool Token-Budget Routing for Cost-Efficient and Reliable LLM Serving](2026-2604.08075-dual-pool-token-budget-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  短文が大半なのに全GPUを最長文脈向けに設定する無駄を、短文・長文の2群と自己較正する総トークン予算ルーティングで解き、KV容量の過剰予約、要求追い出し、GPU費用を同時に削減する。

- **2026-03 · [Token-Budget-Aware Pool Routing for Cost-Efficient LLM Inference](2026-2604.09613-token-budget-aware-pool-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  短文・長文でvLLMプールを分離し、自己校正した総トークン予算で振り分けてGPU台数を約17〜39%削減するフリート経路制御。

- **2026-03 · [TetriServe: Efficiently Serving Mixed DiT Workloads](2026-2510.01565-tetriserve-efficiently-serving-mixed-dit-workloads.md)**  
  実装：[✓](https://github.com/DiT-Serving/TetriServe) ・ リポジトリ内被引用：1  
  TetriServeは、要求のdenoising stepごとにGPU並列度を変えられるスケジューラを設計する。FLUX.1-devを8枚のH100、SD3 Mediumを4枚のA40で実測し、固定SP方式に対してSLO達成率を最大32%改善したと報告する。

- **2026-03 · [TCM-Serve: Modality-aware Scheduling for Multimodal Large Language Model Inference](2026-2603.26498-rps-serve-modality-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル遅延とKV占有量からマルチモーダル要求を3資源クラスへ分け、クラス別キューとエージング付き優先制御で巨大動画による先頭待ちを抑え、平均TTFTを54%、遅延重視要求で78.5%削減する。

- **2026-03 · [SUN: Shared Use of Next-token Prediction for Efficient Multi-LLM Disaggregated Serving](2026-2603.02599-sun-shared-use-of-next-token-prediction-for-efficient-multi-llm-disaggre.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  通常の分離配信（disaggregated serving）は、入力を一括処理するプリフィル（プリフィル）と、出力を1トークンずつ生成するデコード（デコード）を異なるGPUへ割り当てる。

- **2026-03 · [Simple is Better: Multiplication May Be All You Need for LLM Request Scheduling](2026-2603.15202-simple-is-better-multiplication-may-be-all-you-need-for-llm-request-sche.md)**  
  実装：[✓](https://github.com/blitz-serving/blitz-router) ・ リポジトリ内被引用：1  
  複数の推論インスタンスを持つLLMサービスでは、到着した要求をどのインスタンスへ割り当てるかで、初回トークン遅延（Time To First Token、TTFT）と出力トークン当たり遅延（Time Per Output Token、TPOT）が変わる。

- **2026-03 · [SageSched: Efficient LLM Scheduling Confronting Demand Uncertainty and Hybridity](2026-2603.07917-sagesched-demand-uncertainty-hybrid-cost-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  類似プロンプトの履歴から出力長分布を学習なしで推定し、入力長と出力長から計算・KVキャッシュ費用を統合、Gittins指数で不確実性込みの優先順位を決めるLLMスケジューラ。平均TTLTを最大28.7%以上改善する。

- **2026-03 · [MoEless: Efficient MoE LLM Serving via Serverless Computing](2026-2603.06350-moeless-serverless-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散MoE推論で次の層のエキスパート負荷を予測し、混雑するエキスパートだけを一時複製して複数GPUへ配置し、ルータを変えずに同期点での最遅GPU待ちを減らすサーバーレス提供システム。

- **2026-03 · [GhostServe: A Lightweight Checkpointing System in the Shadow for Fault-Tolerant LLM Serving](2026-2605.00831-ghostserve-shadow-checkpointing-fault-tolerant-serving.md)**  
  実装：[✓](https://github.com/project-ghostserve/26mlsys-AE-GhostServe) ・ リポジトリ内被引用：1  
  KVキャッシュ全体ではなく消失訂正符号パリティをホストメモリへ退避し、長文脈LLMの障害復旧を低メモリ・低遅延化する。

- **2026-03 · [Cost-Efficient Multimodal LLM Inference via Cross-Tier GPU Heterogeneity](2026-2603.12707-cost-efficient-multimodal-llm-inference-via-cross-tier-gpu-heterogeneity.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  画像符号化をRTX 4090、言語生成をA100へ分離し、KVキャッシュではなく数MB級の画像埋め込みだけをPCIe転送することで、異種GPUを使った低コストなマルチモーダルLLMサービングを実現する。

- **2026-02 · [TIDE: Temporal Incremental Draft Engine for Self-Improving LLM Inference](2026-2602.05145-tide-temporal-incremental-draft-engine-for-self-improving-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TIDE（Temporal Incremental 下書き Engine、時間的増分草稿エンジン）は、投機的復号（投機的復号）を「静的な草稿モデルを使う復号手法」から「実際の入力分布に合わせて草稿モデルを更新し、必要な場合だけ投機するサービングシステム」へ拡張する研究である。

- **2026-02 · [PrefillShare: A Shared Prefill Module for KV Reuse in Multi-LLM Disaggregated Serving](2026-2602.12029-prefillshare-shared-prefill-multi-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数LLMが同じ文脈を別々にプリフィルする重複を、凍結共有プリフィル＋KV条件付き追加学習でモデル横断共有し、エージェント処理の尾遅延とKVメモリを削減する。

- **2026-02 · [PASCAL: A Phase-Aware Scheduling Algorithm for Serving Reasoning-based Large Language Models](2026-2602.11530-pascal-phase-aware-reasoning-llm-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  推論型大規模言語モデルの非表示推論と表示回答を別の利用者目標として扱い、優先度待ち行列・出力平滑化・フェーズ境界での鍵値キャッシュ移行により、最初の回答が見えるまでの裾の待ち時間を最大七十二パーセント削減する。

- **2026-02 · [InfMem: Learning System-2 Memory Control for Long-Context Agent](2026-2602.02704-infmem-learning-system-2-memory-control-for-long-context-agent.md)**  
  実装：[✓](https://github.com/UCMP13753/InfMem) ・ リポジトリ内被引用：1  
  100万トークン級の文書から複数箇所の証拠を集めて質問に答える場合、全文を一度に言語モデルへ入力する方式は文脈長と注意計算に制約される。推論時間は平均3.9倍、最大5.1倍短縮した。

- **2026-01 · [Competitive Non-Clairvoyant KV-Cache Scheduling for LLM Inference](2026-2601.22996-competitive-non-clairvoyant-kv-cache-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  未知の生成長に対し、幾何級数的な時間片ごとの再開始と開始時刻をずらすKVメモリ平滑化を組み合わせ、一般条件で初の定数競合比を与える非先見的KVスケジューリング理論。

- **2025-12 · [Predictive-LoRA: A Proactive and Fragmentation-Aware Serverless Inference System for LLMs](2025-2512.20210-predictive-lora-serverless-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LoRA要求の時系列から次に必要なアダプタを先読みし、重みを2MB固定ページへ分割して異種rankの断片化を抑えることで、1000アダプタ時にS-LoRA比1.52倍のスループットと高負荷TTFT 35%短縮を達成する。

- **2025-12 · [DynaPipe: Dynamic Layer Redistribution for Efficient Serving of LLMs with Pipeline Parallelism](2025-600ed7f01044-dynapipe-dynamic-layer-redistribution-for-efficient-serving-of-llms-with.md)**  
  実装：[✓](https://github.com/xhx1022/DynaPipe) ・ リポジトリ内被引用：1  
  そのため最終段だけ負荷が重くなり、前段のGPUが待つ「パイプラインの空隙（パイプライン bubble）」が生じる。予測器、空隙認識スケジューラ、移行調整器の三要素で構成される。

- **2025-11 · [SIMPLE: Disaggregating Sampling from GPU Inference into a Decision Plane for Faster Distributed LLM Serving](2025-2512.00719-simple-disaggregating-sampling-from-gpu-inference-into-a-decision-plane-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  単にCPUへ処理を移すだけではCPUメモリー走査が遅くなるため、バッチ方向の並列化、履歴の増分更新、頻出語彙への確率質量集中を組み合わせ、GPUが次の計算を行う時間へ抽出を重ねる。提案方式の実機評価では、比較対象のvLLMに対して生成スループットが最大96%増加し、出力トークン時間の95パーセンタイル（P95）が20〜65%短縮したと報告する。

- **2025-11 · [Serving Heterogeneous LoRA Adapters in Distributed LLM Inference Systems](2025-2511.22880-loraserve-heterogeneous-adapter-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LoRAのランクと需要を同時に見て動的配置・確率ルーティングし、不在アダプタはGPUDirect RDMAで遠隔取得して分散アダプタプールを構成する。

- **2025-11 · [Optimal Self-Consistency for Efficient Reasoning with Large Language Models](2025-2511.12309-optimal-self-consistency-for-efficient-reasoning-with-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし、全問題へ同じ回数だけ生成を繰り返すと、少数の試行で答えが安定する簡単な問題にも計算を使い続け、回答が割れる難しい問題に十分な予算を残せない。固定回数の生成、回答の信頼度に応じて停止する方式、問題間で生成回数を再配分する方式の違いを整理し、予算が少ない段階で有効な方法と、予算が大きい段階で有効な方法を組み合わせるBlend-ASCを提案する。

- **2025-11 · [FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs](2025-2511.00807-freesh-fair-resource-energy-efficient-scheduling.md)**  
  実装：[✓](https://github.com/AndrewFangZequan/LLM_Serving_FREESH) ・ リポジトリ内被引用：1  
  地域別炭素強度と異種GPU特性を使った30分単位の資源配置、1秒単位の動的周波数制御、要求単位の最小余裕時間優先を組み合わせ、エネルギー28.6%・炭素排出45.45%を削減する分散LLMサービング方式。

- **2025-11 · [Fast LLM Post-training via Decoupled and Fastest-of-N Speculation](2025-2511.16193-fast-llm-post-training-via-decoupled-and-fastest-of-n-speculation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの強化学習による後学習では、各学習ステップの前半で多数の問題に対する応答を生成し、報酬を計算してからパラメータを更新する。ChengらのSpecActorは、この待ち時間を単に他の学習処理で埋めるのではなく、ロールアウトそのものを投機的復号で高速化するシステムである。

- **2025-11 · [FailSafe: High-performance Resilient Serving](2025-2511.14116-failsafe-resilient-tensor-parallel-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU障害後も任意数のGPUでテンソル並列推論を継続し、KVキャッシュ配置・注意計算・要求割当を均衡化しながら状態復旧を高速化する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [Unlocking Structured Pruning for Reasoning Language Models via Attention-Preserving MLP Trimming](2026-2610.19121-unlocking-structured-pruning-for-reasoning-language-models-via-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論型言語モデル（Reasoning Language モデル; RLM）は、数学やプログラミング問題を解くために長い思考過程（Chain-of-Thought; CoT）を生成する。重みを構造的に枝刈り（Structured Pruning）すると、行列の幅や層数が減るため、特殊な疎行列カーネルがなくても演算量とメモリ量を削減できる。

- **2026-09 · [Unlocking Software-defined GPU Fabric Scheduling in the LLM Era](2026-a43ed4b300bf-unlocking-software-defined-gpu-fabric-scheduling-in-the-llm-era.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUファブリック競合を監視・通信注入制御し、vLLM+MooncakeでPD KV転送を19.4–34.4%短縮する。

- **2026-09 · [Topology-Aware Data Movement for Disaggregated GPU Inference](2026-2607.28633-topology-aware-data-movement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間のNVLink・PCIe・RDMA・TCP接続を調べてKV転送経路を選び、層計算へ重ねる方式とCXL容量階層を解析し、分離推論の転送待ちとHBM容量制約を減らす。

- **2026-09 · [Token Latency Fairness: Performance Isolation for Multi-Tenant LLM Serving](2026-2609.18112-fairinference-token-latency-fairness-multitenant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離実行比δ以内のトークン遅延を保証するdeadline スケジューラとKV予約を統合し、高需要テナント下のp99 遅延 isolationを実現する。

- **2026-09 · [SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving](2026-2609.37626-splash-switching-parallel-layouts-of-attention-with-seamless-handoff-for.md)**  
  実装：[✓](https://github.com/ict-agent/SPLASH-sglang) ・ リポジトリ内被引用：0  
  SPLASHは、LLM推論配信中に注意演算のGPU間並列配置を切り替えるシステムである。B200でGLM-5.3を配信する評価では、固定配置に対する端から端までの総処理量が1.3～1.73倍となる。

- **2026-09 · [Spatial LLM Workload Shifting Needs Foresight: Model Commitment for AI Data Center Operation under Power Grid Constraints](2026-2609.09787-model-commitment-spatial-llm-workload-shifting.md)**  
  実装：[✓](https://github.com/EilabDBJ/Model-Commitment) ・ リポジトリ内被引用：0  
  モデル読込の先行時間とTTFT/TPOT制約をモデル配置・拠点間配送・電力制約へ統合し、3拠点事例で100%サービス率と総運用費29.0%削減を示す。

- **2026-09 · [SlimWise: Decoupling Expert Pruning Across Prefill and Decode for Efficient MoE Serving](2026-2609.34117-slimwise-decoupling-expert-pruning-across-prefill-and-decode-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート、MoE）は、各トークンに対して全エキスパートのうち少数だけを実行することで、モデル全体のパラメータ規模に比べた演算量を抑える。

- **2026-09 · [Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM Serving](2026-2609.04748-cache-induced-divergence-quantization-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  接頭辞キャッシュは要求外のサーバ状態を出力へ持ち込み、エージェント軌跡差を16ビット36.2%から4ビット75.0%へ増幅することを制御実験で確認。

- **2026-09 · [REVA: Reusable Evidence View Aggregation for Context-Efficient RAG Serving](2026-2609.11209-reva-reusable-evidence-view-rag-serving.md)**  
  実装：[✓](https://github.com/UIUC-MLSys/REVA) ・ リポジトリ内被引用：0  
  過去のRAG要求で対象LLMが文書のどこへ注意したかを文書単位で蓄積し、次回は保存済み重要度から普通のテキスト証拠を数十msで再構成して要求ごとの重い圧縮を避ける。

- **2026-09 · [Rethinking Heterogeneous System Disaggregation for Subquadratic Attention](2026-2609.13134-subquadratic-attention-heterogeneous-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SQDは劣二次注意LLMを状態の文脈依存性で分割し、増大KV処理をDRAM GPU、固定状態の劣二次注意+FFNをSRAM専用ASICへ置いて低遅延推論の電力効率を高める。

- **2026-09 · [QuantMLA: Function-Aligned Dual-Path Quantization for Low-Bit MLA KV Caching](2026-2609.36760-quantmla-function-aligned-dual-path-quantization-for-low-bit-mla-kv-cach.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（Multi-Head Latent 注意機構、MLA）は、通常の注意機構のように各ヘッドの鍵と値をすべて保存せず、複数ヘッドで共有する低次元の内容潜在と、位置情報を表す回転位置埋め込み（Rotary Position Embedding、RoPE）の鍵を保持する。

- **2026-09 · [Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances](2026-2609.12550-quality-constrained-routing-over-a-fixed-pool-of-quantized-mixture-of-experts-instances.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定常駐したW2・W3・W4量子化MoEインスタンス間で、入力時の脆弱性重み付きパープレキシティから要求別の量子化リスクを推定し、品質予算付き線形計画で高処理量側へ配分する要求ルーティング。

- **2026-09 · [Phase-Decoupled, Model-Calibrated Power Control for Disaggregated LLM Serving](2026-2609.11133-phase-decoupled-model-calibrated-power-control-for-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離サービングのプリフィルには校正済みSMクロック窓、デコードには性能崖直上の電力上限を使い分け、B200実機でMax-Qより高いエネルギー効率と良好な遅延を両立する。

- **2026-09 · [PEEK: Predictive Queue-Informed KV Cache Management for LLM Serving](2607.02525.md)**  
  実装：[✓](https://github.com/xiexbing/peek) ・ リポジトリ内被引用：0  
  待機列の接頭辞共有を増分基数木で可視化し、要求順序とKV追い出しを同じ将来需要信号で協調させ、キャッシュ圧迫下のスラッシングを抑える。

- **2026-09 · [OUTLETS: Output-Length Prediction from Speculative Decoding Backbones](2026-2609.01068-outlets-output-length-prediction-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的デコードのドラフト表現から残り出力長を予測し、短く終わる要求をキュー順序とワーカー割当で先に進めて、長い要求による先頭待ちとP99遅延を減らす。

- **2026-09 · [OpWeave: Flexible Operator Disaggregation for Heterogeneous LLM Serving](2026-2609.14237-opweave-flexible-operator-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定分離境界を外し、演算子境界と異種GPU配置を共同探索して費用を同種GPUで最大1.78倍、異種GPUで最大1.89倍改善する。

- **2026-09 · [MeanField Surrogate Modeling for Scalable Runtime Scheduling of Concurrent Heterogeneous AI Inference on Shared GPUs](2026-2609.02109-meanfield-surrogate-runtime-scheduling-shared-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有GPU上の異種LLM/視覚推論で、各モデルの局所構成＋集約GPU状態から性能を予測する平均場代理モデルにより、プロファイル数を実測で約20Nへ抑えつつ5モデル78,732構成を26msで近似探索する。

- **2026-09 · [MAPS: Memory-Aware Predictive Scheduling Framework for Large Language Model Serving](2026-2609.15359-maps-memory-aware-predictive-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末側の出力長予測を共形校正し、必要KV容量と待ち行列を同時に見て分離型LLMのデコード先と実行順を決める。

- **2026-09 · [Latency-Aware Orchestration for Multi-Agent LLM Workflows on Heterogeneous GPUs](2026-2609.03335-latency-aware-multi-agent-orchestration-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  依存するエージェント処理グラフから近接後続を先読みし、モデルの常駐・読込・解放と異種GPU配置・実行順を共同で決めて、モデル待ちと不要なGPU占有を減らす。

- **2026-09 · [Janus: Multi-LLM Serving at Production Scale](2026-922addb5dfb2-janus-multi-llm-serving-at-production-scale.md)**  
  実装：[✓](https://github.com/Janus2026/Janus) ・ リポジトリ内被引用：0  
  単一モデルの推論エンジンを速くしても、多数の異なるLLMを同時提供するサービスでは設備効率と応答期限の両立が難しい。Janusはサービス層（Service）と推論エンジン層（Engine）を協調設計した、多モデル向けサービングシステムである。

- **2026-09 · [HoneyRoute: Honeypot-Model Routing for Adversarial LLM Serving](2026-2609.08306-honeyroute-adversarial-llm-serving-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  悪意要求を安価なハニーポットへ分流し、本番GPU保護と攻撃指紋収集を両立するサービング層ルータ。

- **2026-09 · [HeatCache: Thermal-aware Energy-efficient LLM Inference Scheduling for Chassis-level Liquid Cooling in Sustainable Edge Server Rooms](2026-2609.12449-heatcache-thermal-aware-energy-efficient-llm-inference-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeatCacheはAIO液冷ループの残存熱容量を熱予算として推定し、ジョブ別の発熱予測とTTFT/TPOT制約を使ってvLLMのバッチ・GPU割当・周波数を再順位付けする。48℃級の実機環境で計算エネルギーを最大18.0%削減し、熱スロットリング曝露を大幅に抑える。

- **2026-09 · [Fast Recovery for LLM Serving via Decoupled Device Memory Lifetime in Dynamo](2026-2609.25451-fast-recovery-for-llm-serving-via-decoupled-device-memory-lifetime-in-dy.md)**  
  実装：[✓](https://github.com/ai-dynamo/dynamo) ・ リポジトリ内被引用：0  
  本研究の問題意識は、推論サービスで障害が発生した際に最も高価なのは、失敗した個別要求の計算途中状態を失うことよりも、新しい要求を受け付けられる準備完了済みレプリカの能力が失われることだという点にある。著者はGPU上に残る重みをプロセスと独立に保持し、初期化済みの予備エンジンを切り替える設計をNVIDIA Dynamoに実装する。

- **2026-09 · [ExaServe: Large-Scale LLM Serving on Exascale HPC Systems](2026-2609.10812-exaserve-large-scale-llm-serving-exascale-hpc-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エクサスケールHPC向けLLM推論展開を設定ファイルから自動化し、Aurora 256ノード・3072レプリカまで拡張して、中央ストリーミング配信とRay制御面が先に限界へ達することを実測した。

- **2026-09 · [ETCInfer: An Energy-efficient Thermal-aware Cooling-joint Scheduler for LLM Inference in AI Datacenters](2026-2609.15230-etcinfer-thermal-aware-cooling-joint-scheduler.md)**  
  実装：[✓](https://anonymous.4open.science/r/ETCInfer-2761/) ・ リポジトリ内被引用：0  
  GPU周波数・マイクロバッチと空調設定温度を熱モデル付きで共同制御し、LLM推論の総エネルギーを最大33.1%削減しつつ高温環境でもSLOと熱安全性を維持する。

- **2026-09 · [Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs](2026-2609.11562-entwine-tiled-computation-fine-grained-gpu-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力タイルの生成順序・タイル単位通信・共有SM上の通信並列度を協調し、テンソル並列GEMMとReduceScatterの通信尾を抑える計算通信重畳方式。

- **2026-09 · [Energy-Efficient LLM Serving via Disaggregated Attention--FFN and Flexible Frequency Scaling](2026-2608.01891-aflex-attention-ffn-disaggregation-frequency-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構とFFNを別GPU群へ分け、遅延・エネルギー予測から数分単位の配置と要求ごとの周波数を選び、適応バッチ化と増分再配置でSLO内の電力と分離空きを減らす。

- **2026-09 · [EMMI: Edge Multi-Modal Intelligence for Communication-Efficient MLLM Inference via Fused Representation Compression](2026-2609.11058-emmi-edge-multimodal-representation-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末側でモダリティ別特徴を先に融合してから64次元へ学習圧縮し、固定長潜在表現だけをサーバへ送ることで通信量を32分の1、帯域制約下の推定総遅延を最大3.4倍改善する。

- **2026-09 · [Efficient Iterative Retrieval with Heterogeneous Batching](2026-2609.25405-orthrus.md)**  
  実装：[✓](https://github.com/illinoisdata/Orthrus) ・ リポジトリ内被引用：0  
  従来の推論サーバでは埋め込みモデルと生成モデルを別GPU群へ割り当てるか、同じGPU上で別プロセスとして実行することが多い。4基のA100 40GBで、固定GPU分割に対して制御ワークロードの処理率を1.28〜4.52倍に高め、反復RAGの99パーセンタイル遅延を最大55.8%減らした。

- **2026-09 · [EAServe: Encode-Aware Disaggregated Serving for Multimodal Large Language Models](2026-2609.31551-easerve-encode-aware-disaggregated-serving-for-multimodal-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テキスト専用の事前充填–復号分離では二段のGPU配分を調整すればよいが、マルチモーダル推論では入口の符号化が下流への要求供給を支配する。サービス水準目標（SLO）を満たす要求処理量（有効スループット）は、NVIDIA Dynamo比で最大4.3倍、vLLM比で最大1.7倍だった。

- **2026-09 · [DLB: Distributed Load Balancing at Scale for Generative AI Inference](2026-2609.21079-dlb-distributed-load-balancing-at-scale-for-generative-ai-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  セルを相互プローブし、推論負荷から予測する遅延と通信遅延を基に、生成AI要求を地理的に分散したサーバーへ配る本番ロードバランサー。

- **2026-09 · [Disaggregated Quantization: Specializing LLM Prefill and Decode](2026-2609.26333-disaggregated-quantization-prefill-decode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離量子化（Disaggregated Quantization; DQ）は、両段階に同じ量子化形式を強制せず、プリフィルには演算器が高速に扱えるNVFP4等、復号には2〜3ビット級の重みのみ量子化を割り当てる。

- **2026-09 · [Denoising Surface: Modeling and Predicting Inference Cost for Diffusion LLM Serving](2026-2610.00499-denoising-surface-modeling-and-predicting-inference-cost-for-diffusion-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは、各ブロック・ステップが実行される確率を表すDenoising Workload Surface（DWS）をプロンプトから予測し、GPU構成に応じて計測した一ステップ当たり費用と合成する。LLaDA2.0-miniでの予測費用MAEは355.24msで、出力長ベース887.97ms、総denoisingステップ数ベース517.04msより小さい。

- **2026-09 · [Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows](2026-2609.10964-decoupling-readiness-from-release-tail-aware-agentic-llm-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント型LLMワークフローで準備完了ターンの即時投入をやめ、尾部リスク/推定仕事量による優先度と適応投入予算でP95完了時間を最大3.50倍改善するスケジューリング方式。

- **2026-09 · [Crossflow: Prefill-Decode Elasticity for Agentic LLM Serving](2026-2609.27085-crossflow-prefill-decode-elasticity-for-agentic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定P/D分離は各段階を専用化できる一方、実運用では未キャッシュ入力と出力の比率が短時間に変動する。大規模フリートでは分単位のピーク対平均比が最大4.7倍、公開エージェント型トレースでは同日内の時間別比率幅が中央値24.5倍だった。

- **2026-09 · [Cross-Model Autoscaling for Shared LLM Serving](2026-2609.29160-cross-model-autoscaling-for-shared-llm-serving.md)**  
  実装：[✓](https://github.com/zxzx9898/Token-service-share_Rebalancing_Engine) ・ リポジトリ内被引用：0  
  著者らは、要求1件当たりに供給される実効トークン処理能力を測り、モデルとSLOごとに定めた「健全なサービスの最低境界」で正規化するトークンサービス分配率（トークン Service Share: TSS）を設計する。二台の各4基A100 40 GBを備えた評価基盤で、AIBrixとvLLMのホット切替を利用し、3モデル・7種類の負荷トレースを測定した。

- **2026-09 · [Cascadia: A Control-Plane-Free Alternative to Hyperconverged AI Infrastructure](2026-2609.38697-cascadia-a-control-plane-free-alternative-to-hyperconverged-ai-infrastru.md)**  
  実装：[✓](https://github.com/labscommunity/cascadia-architecture-paper) ・ リポジトリ内被引用：0  
  設計の核心は、要求ごとの専用ルータを不要にすることと、単一ノードに収まるモデルの複製と、収まらないモデルの層分割を同じ認証済みネットワーク上で扱うことである。

- **2026-09 · [Calibrate, Then Route: A Measured Study of Learned Request Routing for Disaggregated LLM Serving](2026-2609.16206-calibrate-then-route-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力長・予測出力長・KV圧力・SLOから配置後の追加完了時間を見積もり、実機校正したコストでプリフィル／デコード先を選ぶルータをA40分離サービング上で評価し、利得と失敗領域を定量化した。

- **2026-09 · [Ask the Tool, Don't Guess: Agent Tool Calls Hold Their Progress, and the Serving System Should Read It](2026-2609.18849-ask-the-tool-progress-aware-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ツール実行中の進捗を副経路でKV管理へ伝え、vLLM上でLRU比p90ツール後TTFTを約21%削減する。

- **2026-09 · [Analytical Resource Management for Fine-grained MoE Computation-Communication Overlap](2026-2609.07536-moe-overlap-resource-manager.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力長とMoE専門家へのトークン偏りから通信タイルへ予約するGPU資源を解析的に選び、計算と通信の重なりを調整して固定配分よりプリフィル待ちを減らす。

- **2026-09 · [Analytical Power-Aware Provisioning for Prefill-Decode Disaggregated AI Inference](2026-2609.24639-analytical-power-aware-provisioning-for-prefill-decode-disaggregated-ai-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、入力処理（プリフィル）と復号（デコード）を別々のGPU群に割り当てる分離型サービング（プリフィル–デコード Disaggregation、PD分離）で、何台の入力処理インスタンスと復号インスタンスを稼働させれば、要求処理容量を満たしながらGPU電力を最小化できるかを扱う。

- **2026-09 · [An Open-Source End-to-End FHE Implementation for Privacy-Preserving Llama 3 8B Inference](2026-2609.12378-an-open-source-end-to-end-fhe-implementation-for-privacy-preserving-llam.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  問題は単一演算を高速化するだけではなく、各演算の入出力の暗号文配置を接続できるようにすることにある。arXiv:2609.12378の2026年10月14日改訂v3本文は、提案方式をThemisと呼ぶ。

- **2026-09 · [An Approximate Queueing Model of LLM Inference Serving for SLO-Driven Autoscaling](2026-2609.20957-an-approximate-queueing-model-of-llm-inference-serving-for-slo-driven-au.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RamaniとTantawiは、連続バッチ処理（Continuous Batching）を行う大規模言語モデル（Large Language モデル、LLM）サーバについて、初回トークン時間（Time to First Token、TTFT）と出力トークン間遅延（Inter-Token Latency、ITL）を要求到着率とGPUレプリカ数から予測し…

- **2026-09 · [AInfer-PD: Communication-Safe In-Place Prefill-Decode Multiplexing for Distributed MoE Rollouts](2026-2609.00993-ainfer-pd-communication-safe-prefill-decode-multiplexing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散MoEロールアウトでプリフィルとデコードを同一GPU群へ安全に同居させ、競合する集合通信だけを順序付ける方式。8×H20-3Eで通常AInfer比の総処理時間を最大22.5%、16GPUで最大35.3%削減した。

- **2026-09 · [A Year in LLM Serving: Workload Evolution, Caching and Load-Balancing](2026-2608.13573-year-llm-serving-workload-evolution.md)**  
  実装：[✓](https://github.com/HarvardMadSys/chutes_workload) ・ リポジトリ内被引用：0  
  61.2億件・9,174モデルの1年実運用記録を解析し、LLM需要の非定常性、短時間の接頭辞再利用、キャッシュ局所性と負荷分散の競合を定量化して公開評価記録を提供する。

- **2026-08 · [Towards Efficient Serving of Network-intensive LLM Inferences](2026-5c9bc68e3beb-towards-efficient-serving-of-network-intensive-llm-inferences.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い共通コンテキストを持つ要求では、過去に計算した接頭辞のKVキャッシュを別サーバから再利用することでプリフィル再計算を減らせる。実機構成を用いた評価では、読込みが単一リクエストのTTFTの90%超になるケース、ICLを1.2 QPSで処理するときの平均TTFT 81.3%超の短縮、同条件でのSLO達成率61.67%向上などを報告する。

- **2026-08 · [TensorCast: The Missing Tensor Management Layer in Large Language Model Infrastructure](2026-2608.06007-tensorcast-tensor-as-a-service.md)**  
  実装：[✓](https://github.com/tensorcast-ai/tensorcast) ・ リポジトリ内被引用：0  
  モデル重み・KV・チェックポイントをArtifact/Operation/Planとして統一管理し、配置・移動・変換・実体化を実行エンジンから分離することで、個別専用基盤に近い性能と横断的な状態管理方針の合成を両立する分散テンソル基盤。

- **2026-08 · [Squeezing the Cache, Preserving the Truth: Monotonic Equipotential Allocation with Geodesia-KV](2026-2608.23599-squeezing-the-cache-preserving-the-truth-monotonic-equipotential-allocat.md)**  
  実装：[✓](https://github.com/geodesia-ai/geodesia-kv) ・ リポジトリ内被引用：0  
  Geodesia-KVは、長文脈LLM推論のKVキャッシュを単に一律4ビット化するのでなく、64トークン単位のブロックごとに異なる精度を割り当て、不要になった高精度表現を保持せず低精度側へ単調に移す方式である。しかしこの差は0.39%程度で、別コーパスPG-19の11冊では同一の優位は統計的に確立されない。

- **2026-08 · [SplitScaling: Adaptive Scaling for Disaggregated LLM Serving Against Traffic Bursts via DRL](2026-92b65c48d388-splitscaling-adaptive-scaling-for-disaggregated-llm-serving-against-traffic-bursts-via-drl.md)**  
  実装：[✓](https://github.com/Onlytonight/SplitScaling) ・ リポジトリ内被引用：0  
  プリフィル／デコード各プールを深層強化学習で独立伸縮し、新規ノードへ待機要求を即時再割当して、バースト負荷下でSLOを守りながら静的構成比25.2%の計算コストを削減する。

- **2026-08 · [SkillZip: Contract-Preserving Graph Compression for Scalable Agent Skill Libraries](2026-2608.05604-skillzip-contract-preserving-graph-compression-for-scalable-agent-skill-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一般のプロンプト圧縮と違い、文書の語数を減らすこと自体を最適化の終点としない。原著のSkillsBench、1,000スキル、MiniMax-M2.7という条件では、最も強い比較対象のSkillDAGに対して、タスク報酬27.3から33.3、最初の正解スキル検索率66.7から73.6、最終提示手順の平均トークン数3,103から1,941へ改善する。

- **2026-08 · [SAGE: SLO-Aware Adaptive Retrieval for Production RAG Systems](2026-2608.08237-sage-slo-aware-adaptive-retrieval-for-production-rag-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索拡張生成（Retrieval-Augmented Generation、RAG）は、外部文書を検索してから大規模言語モデル（LLM）に回答させる。実運用では、検索文書数を一律に20件などへ固定すると、単純な質問に過剰な文書を渡して時間と費用を浪費する一方、複雑な質問では検索量が足りず正答率を落とす。

- **2026-08 · [RAC: Reference-Aware Activation Compression for Communication-Efficient Split LLM Inference](2026-2608.04991-rac-reference-aware-activation-compression-for-communication-efficient-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末からクラウドへ送る境界活性と、クラウドから端末へ返す境界活性を、そのまま低ビット量子化するのではなく、送受信側で共有可能な参照状態との差分として符号化する。原著が評価した3モデルと9種類のモデル・回線条件では、無圧縮との比較で平均初回トークン時間（TTFT）の比が1.24～2.72倍、平均出力トークン時間（TPOT）の比が1.01～2.79倍である。

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

- **2026-08 · [M-LoRA: Efficient Serving for Concurrent LoRA Adapters with Memory-Aware Speculative Scheduler on Single GPU](2026-bbf40b71b5e2-m-lora-efficient-serving-for-concurrent-lora-adapters-with-memory-aware-speculative-scheduler-on-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとの生成長をモデル別LoRA予測器で見積もり、鍵値キャッシュとアダプタのピークメモリを同時制約する整数線形計画で、単一GPUの複数LoRA要求を高並行に割り当てるサービング方式。

- **2026-08 · [LOCAL: Enabling Learning On-device Contiguously for Agent LLMs](2026-2608.15241-local-contiguous-on-device-agent-learning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一24 GB GPUで前景推論を止めずにLoRA学習を進め、アダプタ版を考慮したKV再利用・再計算・退避をスケジューラと協調させる端末向け継続学習ランタイム。

- **2026-08 · [LLMVisor: A Real-Time Latency Attribution Model for Multi-Tenant LLM Serving](2026-2608.08382-llmvisor-realtime-latency-attribution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  処理トークン、文脈長、自己注意の二次項、バッチ規模を使う加法的な区分線形モデルで、共バッチ処理のGPU時間を要求・テナント別へマイクロ秒級で帰属し、VTCより裾誤差を最大4.4倍改善する。

- **2026-08 · [Janus: Joint Prefill/Decode Disaggregation with KV-Cache-Aware Multi-Cloud Routing for Edge-Adjacent LLM Serving](2026-98d01325c44c-janus-joint-prefill-decode-disaggregation-with-kv-cache-aware-multi-cloud-routing-for-edge-adjacent-llm-serving.md)**  
  実装：[✓](https://github.com/arunakbofficial-tech/Janus) ・ リポジトリ内被引用：0  
  プリフィル/デコード配置とKV輸送方式を共同最適化し、異種マルチクラウドLLMサービングのTTFT・有効スループット・コストを同時改善する。

- **2026-08 · [HorizonServe: Coordinating Request Scheduling with GPU Sharing for Omni-Model Serving](2026-2608.01785-horizonserve-coordinating-request-scheduling-with-gpu-sharing-for-omni-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一GPU上のオムニモデルで、締切余裕に基づく経路入場制御と帯域圧力に応じたSM配分を連携し、異種出力要求のSLO達成率を高めるサービング方式。

- **2026-08 · [FleetSieve: Decision-Critical Profiling for SLO-Aware LLM Fleet Configuration](2026-2608.19659-fleetsieve-decision-critical-profiling-for-slo-aware-llm-fleet-configura.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  チャット、コード補完など異なる要求系列へ有限のGPUを配分するとき、テンソル並列度（テンソル parallelism; TP）、モデル複製数、要求負荷を変えると、処理容量と遅延の関係が複雑に変化する。ただしコード補完用途では無作為計測などの方が安く、すべての用途で優位な探索方式ではない。

- **2026-08 · [Efficiency and Cost Alignment in Batched LLM Serving via Resource-Fair Scheduling](2026-2608.02244-resource-fair-batched-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長短要求を同居させたバッチで短い要求まで最大KV量相当の費用を負担する外部性を定式化し、デコード進捗差を制限するISJLを提案。一般のバッチ幅で競争比3/4を保証し、LMSYS再生ではLJFより最大17%高いスループットと21%低い平均遅延を示す。

- **2026-08 · [Connex: Endpoint Mobility Primitives for Dynamic LLM Serving](2026-04a3072fd610-connex-endpoint-mobility-primitives-for-dynamic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Connexは、分離型プリフィル・デコードやパイプライン並列化を使う大規模言語モデル（LLM）のオンライン推論で、GPUワーカーの追加・離脱・故障・移動を通信経路を全面再構築せずに扱うための通信基盤である。構成変更中の中負荷では要求完了率100%を保ち、比較対象は条件によって0～28%まで低下する。

- **2026-08 · [AFD-Ledger: Deployment Provisioning for Attention--FFN Disaggregation](2026-2608.04502-afd-ledger-deployment-provisioning-for-attention-ffn-disaggregation.md)**  
  実装：[✓](https://github.com/kvcache-ai/AFD-Ledger) ・ リポジトリ内被引用：0  
  AFDと同居配置を同一予算・TPOT SLOで独立最適化し、少数のハードウェア組だけを完全評価して最適配置を探索する分析プロビジョニング系。

- **2026-07 · [X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding](2026-2609.09166-x-cosd-cross-vocabulary-collaborative-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末SLMとサーバLLMの語彙が異なっても、残差分布を共通語彙・LLM専用語彙へ分け、少数の置換候補だけを通信して厳密な協調投機的デコードを行う方式。

- **2026-07 · [Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs](2026-2607.17181-talaria-session-aware-serverless-serving-of-hundred-billion-parameter-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単発要求の待ち時間やGPU利用率だけを最適化する方式は、ツールを使うエージェントの連続呼出しには必ずしも適さない。機構を無効化したラウンド型基準と比較し、セッション完了時間の中央値を1000秒から189秒、95パーセンタイルを2296秒から867秒へ短縮した。

- **2026-07 · [SpecBox: Speculative Sandbox Scheduling for Efficient LLM Agent Serving](2026-2607.23933-specbox-speculative-sandbox-scheduling-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SpecBoxはLLM生成中に将来のツール利用を推測して隔離実行環境を投機起動し、依存グラフ先読み・結果キャッシュ・共有メモリ転送を組み合わせてエージェントサービングの初回起動遅延と常時予約メモリを両立改善する。

- **2026-07 · [QUARTZ: Quantile-Aware Routing and Queueing for TTFT SLOs in LLM Serving](2026-925996defd10-quartz-quantile-aware-routing-and-queueing-for-ttft-slos-in-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）のオンライン推論では、初回トークン時間（Time To First Token; TTFT）が対話の応答性を左右する。平均遅延が小さくても、長い検索拡張生成（Retrieval-Augmented Generation; RAG）の要求が先頭に並ぶと、短い対話要求まで待たされ、99パーセンタイル（P99）の遅延が悪化する。

- **2026-07 · [PDD: Unleashing Economical and Flexible Heterogeneous LLM Inference via Cross-Datacenter Prefill-Decode Disaggregation](2026-2609.13161-pdd-cross-datacenter-prefill-decode-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  広域KV転送中だけ近傍の中継GPUでデコードを先行し、遠隔GPUへトークンIDで引き継ぐ三段PD分離により、データセンター間異種推論のTTFTと費用効率を改善する。

- **2026-07 · [OpenTela: Unifying Decentralized Computing Resources for Heterogeneous LLM Serving (Operational Systems)](2026-a3ac377502ac-opentela-unifying-decentralized-computing-resources-for-heterogeneous-ll.md)**  
  実装：[✓](https://github.com/eth-easl/opentela) ・ リポジトリ内被引用：0  
  中央の特権的なクラスタ管理者を置かず、既存のHPCジョブ管理方式を変えずに導入できることが設計目標である。GH200でQwen3-1.7Bを提供した実験では、入口での認証・選択・転送等の制御面による追加TTFTが到着率1/4/16 RPSで約1.69/1.68/1.42msであり、制御面が存在する代償を実測している。

- **2026-07 · [Online Linear Programming for Multi-Objective Routing in LLM Serving](2026-2607.03948-online-linear-programming-multi-objective-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各デコードワーカーの将来バッチ枠とKV容量へ影価格を付け、SLO報酬が資源費を上回る要求だけをルーティングして、平均・末尾遅延とスループットの優先順位を切り替える。

- **2026-07 · [On the Limitations of Non-GPU AI Accelerators for Large-Model Inference: A Field Study of MoE and Multimodal Serving on Huawei Ascend](2026-2607.08215-on-the-limitations-of-non-gpu-ai-accelerators-for-large-model-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は新しい高速化アルゴリズムを提案する研究ではない。対象は約300 GBの8ビット重み・8ビット活性化（W8A8）混合専門家モデルによる判定サービスと、約540 GBのbfloat16画像言語モデルによる画像質問応答の評価サービスである。

- **2026-07 · [OmniPilot: An Uncertainty-Aware LLM Inference Advisor for Heterogeneous GPU Clusters](2026-2607.01579-omnipilot-uncertainty-aware-inference-advisor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU種類・テンソル並列度・精度を実測ベースの不確実性付き費用モデルで順位付けし、未知領域では推薦を控える起動助言器。460実測でスループット誤差6.2%、上位1位正解率95%を示す。

- **2026-07 · [Metronome: Bound the Cache, Keep the Beat for Real-Time Interaction Model Serving](2026-2607.02640-metronome.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、自由生成の品質維持に重要な冒頭の注意シンク（注意機構 sink）トークンは固定保持する。

- **2026-07 · [Kalypso: Relational LLM Serving](2026-2607.23815-kalypso-relational-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは、段階ごとのメモリ予算、待機列の飢餓・飽和の検知、出力トークン数の予測、明示的または仮想的なKV保持を組み合わせる。利得はLLMの重みや注意機構を変更したためではなく、意味演算子の処理順とKV寿命を連動させたためである。

- **2026-07 · [InstantInfer: Enabling Fast LLM Cold Start with Communicating Finite Automata](2026-2607.18957-instantinfer-enabling-fast-llm-cold-start-with-communicating-finite-auto.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数モデルをオンデマンドで起動するサーバーレス環境では、通常の推論速度が速くても、起動だけで数十秒から数分かかると初トークン遅延（TTFT）を支配する。InstantInferは、モデルの演算を近似したり量子化したりするのではなく、起動プログラムの実行依存関係とI/O粒度を改善する。

- **2026-07 · [General Non-Clairvoyant KV-Cache Scheduling via Regime-Aware Routing](2026-2607.09248-regime-aware-non-clairvoyant-kv-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  応答長未知で成長するKVキャッシュを、メモリ成長形状ごとの三領域へ実行時ルーティングし、領域別スケジューラを時分割して任意長でも定数競合保証を与える。

- **2026-07 · [Full-Pipeline Inference Optimization for MiMo-V2.5 Series: Pushing Hybrid SWA Efficiency to the Limit](2026-2607.13095-mimo-hybrid-swa-full-pipeline-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Hybrid SWAの理論的KV削減を本番へ落とすため、Full/SWA二重KVプール、層単位先読み、分散GCache、KV親和ルーティング、プリフィル・デコード・マルチモーダル処理を一体最適化する。

- **2026-07 · [Efficient and Privacy Aware Edge Cloud Collaborative Inference for Large Language Models](2026-2607.13093-privacy-aware-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原文を送らず、端末にKV認可・軽量投機・低次元出力層を残し、クラウドの重いデコーダと協調する分割推論。H20＋3種端末で素朴な分割推論比の遅延最大46.1%、下り通信最大67.4%削減を報告する。

- **2026-07 · [DeltaServe: Host-Agnostic Co-Serving of Inference and Fine-Tuning for LLMs](2026-2607.28848-deltaserve-inference-finetuning-coserving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRA微調整の順伝播を既存推論バッチへSLO予算内で混ぜ、逆伝播を層境界でプリエンプト可能な別プロセスへ分離することで、推論GPUの空き計算資源を微調整へ転用する外付け共存実行方式。

- **2026-07 · [CoCoScale: Leveraging Layer-wise Scaling to Unlock the Potential of Online LLM Serving](2026-2607.04181-cocoscale-leveraging-layer-wise-scaling-to-unlock-the-potential-of-onlin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数のモデルを提供するクラスタでは、人気モデルへの要求が急増しても、別のモデルに割り当てたGPUが遊休に近いことがある。4基のNVIDIA H20上で実負荷トレースを再生した評価では、従来のインスタンス単位の増設に比べ拡張遅延を97.9〜99.3%短縮し、比較した全モデル・トレースでSLO達成率100%を示した。

- **2026-07 · [Beyond Static RAG: An Adaptive, Tri-Metric Routing Framework for Efficient Long-Context Inference on Commodity GPUs](2026-2609.17564-adaptive-rag-routing-commodity-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文RAGの各要求を文書長・キーワード密度・異なり語率で未圧縮、ニューラル圧縮、BM25へ振り分け、T4のVRAM競合とOOMを抑える。

- **2026-07 · [Akashic: A Low-Overhead LLM Inference Service with MemAttention](2026-2607.05708-akashic-memattention-memory-service.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長期エージェント履歴を1024トークン級チャンクへ共同圧縮し、関連チャンクだけを検索・再統合してNVMe上でも近接配置することで、再入力量とメモリI/Oを減らす。

- **2026-06 · [The Serialized Bridge: Understanding and Recovering LLM Serving Performance under Blackwell GPU Confidential Computing](2026-2606.23969-serialized-bridge-blackwell-gpu-confidential-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU機密計算でLLM推論が遅くなる主因をGPU演算ではなく機密VM–GPU間の直列化された転送路と特定し、スケジューリング・モデルロード・KV退避を転送特性に合わせて変えることで大半の性能差を回復する。

- **2026-06 · [Scaling LLM Inference Beyond Amdahl's Limits via Eliminating Non-Scalable Overheads](2026-2606.01927-scaling-llm-inference-beyond-amdahl-s-limits-via-eliminating-non-scalabl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Albireoは、推論エンジンの各イテレーションに含まれるスケジューリング、入力準備、出力処理、samplingを、順伝播と並行して実行できるようにするシステムである。

- **2026-06 · [Recency/Frequency Adaptive KV Caching for Large Language Model Serving](2026-2606.21238-recency-frequency-adaptive-kv-caching-for-large-language-model-serving.md)**  
  実装：[✓](https://github.com/Y-aang/vllm-ARC) ・ リポジトリ内被引用：0  
  LLMのprefix KV キャッシュは、過去の要求の入力表現を再利用することで、同じ文書や会話履歴を再度プリフィルする計算を省く。著者らはQwen3-14Bを単一NVIDIA H100 PCIe 80GB GPUで評価した。

- **2026-06 · [PersistentKV: Page-Aware Decode Scheduling for Long-Context LLM Serving on Commodity GPUs](2026-2606.26666-persistentkv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ページ化KV表を作り直さず長い系列を区間へ分割し、必要な区間だけ作業キューへ詰めてGPUを埋め、長文デコードの遊休と不要なカーネル起動を減らす。

- **2026-06 · [NetKV: Network-Aware Decode Instance Selection for Disaggregated LLM Inference](2026-2606.03910-netkv-network-aware-decode-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離推論のデコード先選択へネットワーク階層・帯域・混雑を加え、KV転送・キュー・初回デコード時間の合計が最小のGPUを要求ごとに選ぶ。

- **2026-06 · [LiveServe: Interaction-Aware Serving for Real-Time Omni-Modal LLMs](2026-2606.22983-liveserve-interaction-aware-serving-for-real-time-omni-modal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話の再生進捗・発話・割込みをスケジューリングとKV配置へ反映し、不要な先行生成を抑えながら次ターンのKVを発話中に先読みし、P90初回音声遅延と無駄計算を同時に減らす。

- **2026-06 · [KernelFlume: Elastic Core-Attention Scaling for Agentic Long-Context Decoding](2026-2606.29207-kernelflume-elastic-core-attention-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル重みを固定した重みノードとKV保持・注意計算だけの重みなしノードへデコードを分離し、長文要求のKV増加に合わせて注意側だけを増設することで、完全モデル複製なしに低遅延で容量を拡張するサービング方式。

- **2026-06 · [HW-Router: Hardware-Aware Routing for Scalable Multi-LLM Serving](2026-2608.14575-hw-router-hardware-aware-multi-llm-serving.md)**  
  実装：[✓](https://github.com/UCF-ML-Research/HW-Router) ・ リポジトリ内被引用：0  
  実時間のキュー・KVキャッシュ・TTFT/TPOTを遅延予測へ統合し、複数LLMルーティングのSLOとGPU負荷均衡を改善する。

- **2026-06 · [HeraSys: Collaborative Serving of Multiple LLM Workflows via Fine-Grained End-to-End Optimization](2026-2607.22578-herasys-collaborative-serving-of-multiple-llm-workflows-via-fine-grained.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HeraSysは、複数利用者が同時に検索拡張生成（retrieval-augmented generation; RAG）や検索エージェントを実行する際の、アプリケーション全体の処理遅延を改善するサービング基盤である。提案は二層で構成される。

- **2026-06 · [FlexNPU: Transparent NPU Virtualization for Dynamic LLM Prefill-Decode Co-location](2026-2606.04415-flexnpu-transparent-virtualization-dynamic-pd-colocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AscendCL操作を仮想ハンドル経由で物理NPUへ転送し、プリフィルとデコードの待機・実行時間・帯域圧力を測って実行比率を動的に変え、静的PD配置の資源偏りとTTFT待ちを減らす。

- **2026-06 · [Energy-Efficient Multimodal Inference Serving with Tri-serve](2026-2606.29629-energy-efficient-multimodal-inference-serving-with-tri-serve.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen2.5-Omni-7Bを代表例として、Thinker（理解・推論）、Talker（音声生成の中間表現）、Vocoder/Code2Wav（波形生成）をvLLM-Omniの別プロセス・別GPUへ割り当てると、後段は前段の出力待ちで停止する。

- **2026-06 · [DriftSched: Adaptive QoS-Aware Scheduling under Runtime Token Drift for Multi-Tenant GPU Inference](2026-2606.02982-driftsched-adaptive-qos-aware-scheduling-under-runtime-token-drift-for-m.md)**  
  実装：[✓](https://github.com/kpalania1/driftsched) ・ リポジトリ内被引用：0  
  DriftSchedは、複数利用者が共有するGPUで大規模言語モデル（LLM）の生成要求を処理するとき、要求を受け付けた時点の予想トークン数と、実際に生成されたトークン数のずれが待ち行列の順序と遅延に及ぼす影響を検証するシステムである。

- **2026-06 · [Demystifying the Design Space and Best Practices for Heterogeneous LLM Inference and Serving](2026-2606.29708-demystifying-the-design-space-and-best-practices-for-heterogeneous-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論を事前充填（プリフィル）と逐次復号（デコード）に分離すると、各段階を異なるアクセラレータで実行できる。ただしこれは制約下で処理可能な到着率の変化であり、すべての推論処理が一律10倍速くなったという意味ではない。

- **2026-06 · [Beyond Prediction: Tail-Aware Scheduling for LLM Inference](2026-2606.18431-tail-aware-prediction-free-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力長予測を使わず、既得サービス量と末尾分布から要求優先度を調整し、KVを壊す頻繁なプリエンプトを幾何学的に制限して平均ではなくP95/P99遅延を安定化する。

- **2026-06 · [Beyond Greedy Chunking: SLO-Aware Sliding-Window Scheduling for LLM Inference](2026-2606.05933-beyond-greedy-chunking-slo-aware-sliding-window-scheduling-for-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、対話型大規模言語モデル（LLM）のオンライン配信で、利用者が要求する最初のトークンまでの時間（TTFT）と、以降のトークン間隔（TBT）の期限を守りつつ、単位時間に処理できる要求数を増やすスケジューリング方式「SlidingServe」を提案する。

- **2026-06 · [AgentServeSim: Serving-System Simulation and Policy Search for LLM Agent Programs](2026-2606.09613-agentservesim-multiturn-agent-serving-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多輪エージェントを要求列ではなく因果的なプログラムとして模擬し、ツール待ちをまたぐKV保持・セッション配置・プログラム単位スケジューリングを同一評価基盤で比較する。実vLLMとの20条件で平均完了時間誤差を約5.5%以内に抑える。

- **2026-05 · [Trading Complexity for Expressivity Through Structured Generalized Linear Token Mixing](2026-2605.31367-trading-complexity-for-expressivity-through-structured-generalized-linea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルの長文脈処理で使う「過去のどの位置から情報を受け取るか」という接続構造を、注意機構と状態空間モデルの二者択一ではなく、一般化された線形再帰の設計問題として扱う。合成コピー課題では二次間隔型が99.66%、指数間隔型が92.63%、密な再帰型が100%である。

- **2026-05 · [Towards Multi-Model LLM Schedulers: Empirical Insights into Offloading and Preemption](2026-2605.19593-multi-model-offloading-preemption-schedulers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  限られたGPUで複数モデルを切り替える推論について、GPUに置く層の割合を連続掃引し、KV退避・モデル解放・重み再読込・KV復元の費用を分解して、オフロード感度と切替ボトルネックを測定した研究。

- **2026-05 · [RW-TTT: Batched Serving for Request-Owned Test-Time Training State](2026-2605.28053-rw-ttt-batched-serving-for-request-owned-test-time-training-state.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RW-TTTはTTTの新しい学習規則ではなく、READとWRITEを区別し、要求の所有権と状態versionを保持して合法な遷移だけをまとめるサービング契約を提案する。

- **2026-05 · [Requests of a Feather Must Flock Together: Batch Size vs. Prefix Homogeneity in LLM Inference](2026-2605.06046-requests-of-a-feather-must-flock-together-batch-size-vs-prefix-homogenei.md)**  
  実装：[✓](https://github.com/networkedsystemsIITB/Feather) ・ リポジトリ内被引用：0  
  例えば共通のシステム指示や長い文書を前置きした多数の要求を同時に扱うと、複数要求の注意計算は同じキー・値キャッシュ（KV キャッシュ）を読む。著者は接頭辞を共有する負荷で、既存方式に対して最大2〜10倍のエンドツーエンド処理量を報告する。

- **2026-05 · [Regulating Branch Parallelism in LLM Serving](2026-2605.06914-taper-regulating-branch-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各デコードステップの残余SLO余裕から追加分岐の遅延予算を作り、予算内だけを動的に実行することで、分岐並列化による他要求の遅延悪化を防ぎつつQwen3-32Bで有効スループットを最大1.77倍へ高める。

- **2026-05 · [MinT: Managed Infrastructure for Training and Serving Millions of LLMs](2026-2605.13779-mint-managed-infrastructure-for-training-and-serving-millions-of-llms.md)**  
  実装：[✓](https://github.com/MindLab-Research/mindlab-toolkit) ・ リポジトリ内被引用：0  
  低ランク適応（LoRA）は更新パラメータを小さくできるが、学習後に基盤モデルへ統合して全量チェックポイントを再配布してしまうと、この利点を運用全体で失う。

- **2026-05 · [Mind the Delay: Latency-aware Query Routing for Heterogeneous LLM pools](2026-2607.18253-mind-the-delay-latency-aware-query-routing-for-heterogeneous-llm-pools.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のモデルルータは入力質問の難しさを見て品質と費用を比較し、負荷分散器はモデルが決まった後にキュー長などからインスタンスを選ぶことが多い。しかし、この二段階の分離では、能力が高くても現在混雑しているモデルへ要求を送り、初回トークン遅延（Time To First Token、TTFT）の期限を破る場合がある。

- **2026-05 · [Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server](2026-2609.05425-cotail.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU制御段階のP95/P99遅延からスケジューラ競合とNUMA・キャッシュ競合を診断し、リアルタイム優先度またはCPU配置分離を選んで同居ワークロードによるLLM遅延を減らす。

- **2026-05 · [Lodestar：オンライン学習によるLLM推論リクエストルータ](2026-2606.00946-lodestar-an-online-learning-llm-inference-router.md)**  
  実装：[✓](https://github.com/gangmuk/Lodestar) ・ リポジトリ内被引用：0  
  公開クラウドの同種8基A30クラスタと、A30 8基＋V100 8基の異種クラスタで評価し、強い接頭辞・負荷認識ヒューリスティックに対して平均TTFTを平均1.41倍、P99 TTFTを1.47倍改善し、条件によって異種クラスタでは4倍超の改善を示す。

- **2026-05 · [Libra: Flexible Request Partitioning and Scheduling for Serving Unbalanced and Dynamic LLM Workloads](2026-a0647c9f2100-libra-flexible-request-partitioning-and-scheduling-for-serving-unbalance.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両者を別々のGPU群へ固定分離すると、入力長と出力長の比率が変化したとき、一方が過負荷でも他方のGPUが遊んでしまう。実機評価では、A100で固定同居方式より最大1.91倍、固定分離方式より最大1.61倍の有効処理量（有効スループット）を達成した。

- **2026-05 · [Keep What Audio Cannot Say: Context-Preserving Token Pruning for Omni-LLMs](2026-2605.11605-keep-what-audio-cannot-say-context-preserving-token-pruning-for-omni-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声は短い特徴系列に圧縮されることが多い一方、映像はフレーム数と空間パッチ数に比例して長くなり、事前充填の計算、注意用メモリ、入力長の制限に影響する。Qwen2.5-Omni 7Bの6つの音声映像課題では、入力トークンを平均55%減らして、無圧縮を100とする正規化平均性能100.0を得た。

- **2026-05 · [JacQuant: STE-Free Quantization-Aware Training via Learned Jacobian Surrogates](2026-2605.25469-jacquant-ste-free-quantization-aware-training-via-learned-jacobian-surro.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  JacQuantは、大規模言語モデル（LLM）を重み1〜2ビットまで圧縮する際の量子化考慮学習（量子化-aware 学習、QAT）を改善する。

- **2026-05 · [Human-Less LLM Serving: Quantifying the Human Tax on Throughput](2026-2606.20577-human-less-llm-serving-human-tax-throughput.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  人間が逐次トークン表示を待たないエージェント処理に、対話向けの先頭トークン遅延（Time to First Token; TTFT）・出力トークン間隔（Time Per Output Token; TPOT）制約をそのまま課すと、長文脈・高並列ではGPUを小さな処理単位へ分割する費用が大きくなる。

- **2026-05 · [HexAGenT: Efficient Agentic LLM Serving via Workflow- and Heterogeneity-Aware Scheduling](2026-2605.16637-hexagent-workflow-heterogeneity-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HexAGenTは逐次公開されるエージェントワークフローの完了危険度を追跡し、異種GPU上のプリフィル・デコード配置とキュー優先度を共同決定して、ワークフロー全体のSLO達成を改善する。

- **2026-05 · [Fine-Tuning and Serving Gemma 4 31B on Google Cloud TPU: A Technical Comparison with GPU Baselines](2026-2605.25645-fine-tuning-and-serving-gemma-4-31b-on-google-cloud-tpu-a-technical-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Gemma 4 31BをTPU v5p-8上で低ランク適応（LoRA）によって教師あり微調整し、TPU v6e-8上のvLLMで推論提供するための具体的な移植手順と、2基のNVIDIA H100 GPUとの実測比較をまとめる。学習ではTPU v5p-8が3.34時間、2×H100が5.39時間で、時間比は1.61倍。

- **2026-05 · [Fail-Closed Lowering of Resident KV Claims onto LLM Serving Runtimes](2026-2606.01387-fail-closed-lowering-of-resident-kv-claims-onto-llm-serving-runtimes.md)**  
  実装：[✓](https://github.com/gustavgauge/resident-kv-lowering-artifact) ・ リポジトリ内被引用：0  
  大規模言語モデルの推論基盤には、鍵・値キャッシュ（KVキャッシュ）の保持優先度、期限、CPU・ストレージへの退避、ブロックの保存・削除イベント、退避禁止、キャッシュ状態を考慮した経路選択などがある。

- **2026-05 · [Enabling Performant and Flexible Model-Internal Observability for LLM Inference](2026-2605.11093-enabling-performant-and-flexible-model-internal-observability-for-llm-in.md)**  
  実装：[✓](https://github.com/ProjectDMX/DMI) ・ リポジトリ内被引用：0  
  本論文が対象とするのは、大規模言語モデル（LLM）の出力やGPU使用率だけでなく、推論中に生成される残差流、注意機構の射影、隠れ状態、全結合層の活性値などを継続的に取り出すシステムである。H100 80GBを使うオフライン推論では、観測点を多数設置しても、元の推論に対する追加時間は0.4～6.8%（柔軟な観測点を使う条件の平均3.6%）だった。

- **2026-05 · [DisagFusion: Asynchronous Pipeline Parallelism and Elastic Scheduling for Disaggregated Diffusion Serving](2026-2605.25550-disagfusion-asynchronous-pipeline-parallelism-and-elastic-scheduling-for.md)**  
  実装：[✓](https://github.com/ModelTC/LightX2V) ・ リポジトリ内被引用：0  
  DisagFusionは、画像・動画を生成する拡散モデル（diffusion モデル）の配信を、符号化器（Encoder）、拡散Transformer（Diffusion Transformer、DiT）、復号器（Decoder）の三段階に分離するシステムである。

- **2026-05 · [DarkForest: Less Talk, Higher Accuracy for Multi-Agent LLMs](2026-2605.25188-darkforest-less-talk-higher-accuracy-for-multi-agent-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の大規模言語モデル（LLM）エージェントに同じ質問を解かせ、討論や相互修正を通じて回答を統合する方法は、単一モデルの誤りを発見できる可能性がある。論文は数学、コード生成、一般知識、科学、金融、法律の6ベンチマークで評価し、通信量の多い方式と比較して最大6.5倍のトークン使用量削減を報告する。

- **2026-05 · [C2CServe: Leveraging NVLink-C2C for Elastic Serverless LLM Serving on MIG](2026-2605.19481-c2cserve-serverless-mig-nvlink-c2c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GH200のCPUメモリをNVLink-C2C経由の能動的な重み格納層として使い、MIGごとのHBM不足を回避するサーバレスLLM基盤。HybridGEMMと競合対応スケジューラで密モデルのコールドスタートを最大7.1倍短縮する。

- **2026-05 · [BIRDS: Characterizing and Understanding Biodiversity Impact of Large Language Model Serving](2026-2605.27480-birds-characterizing-and-understanding-biodiversity-impact-of-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  炭素排出量または水消費量だけでGPU配置先を選ぶと、酸性化、富栄養化、光化学オゾン生成等を経由する生態系損失を取りこぼす。原著の特徴は、電力1 kWh当たりの地域係数を直接比べるだけでなく、GPU電力／SLOを満たした単位時間当たりの完了リクエスト数を経由する点にある。推論時のトークン長、GPU世代、バッチ効率、MoEの稼働GPU数が環境影響へ反映される。

- **2026-05 · [Adaptive Memory Decay for Log-Linear Attention](2026-2605.06946-adaptive-memory-decay-for-log-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意や状態空間モデルは過去を固定長の状態へ圧縮することで生成時の記憶量を一定にできるが、長い文脈の細かな情報を再び取り出すのが難しい。追加パラメータは全モデルの0.007%未満と報告する。

- **2026-04 · [UCCL-Zip: Lossless Compression Supercharged GPU Communication](2026-2604.17172-cccl-compression-coupled-collective-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU通信へ無損失圧縮を融合し、点対点通信の分割送信とNCCL内融合によって通信量と余分なメモリアクセスを減らす方式。

- **2026-04 · [Flow-Controlled Scheduling for LLM Inference with Provable Stability Guarantees](2026-2604.11001-flow-controlled-scheduling-stability.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求の実行開始率を流量制御し、出力長未知時は先入れ先出し受付と後入れ先出し追い出しを組み合わせ、KV容量超過確率を理論的に抑えながら処理量と尾部遅延を改善する。

- **2026-04 · [Fast Heterogeneous Serving: Scalable Mixed-Scale LLM Allocation for SLO-Constrained Inference](2026-2604.07472-fast-heterogeneous-serving-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種GPU・モデル・TP/PP・ルーティングを制約認識型貪欲法で共同配置し、Azure トレース較正の大規模問題で1秒未満・厳密ソルバー比260倍超高速に実行可能解を得る。

- **2026-04 · [Distributed Generative Inference of LLM at Internet Scales with Multi-Dimensional Communication Optimization](2026-2604.21072-bloombee-internet-scale-distributed-inference.md)**  
  実装：[✓](https://github.com/ai-decentralized/BloomBee) ・ リポジトリ内被引用：0  
  一般インターネット上の異種GPU推論で、層配置・KV退避・マイクロバッチ・無損失活性値圧縮・帯域適応型投機デコードを組み合わせ、通信ホップ数・転送量・生成段数を共同削減する。

- **2026-04 · [Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC](2026-2604.07609-blink-cpu-free-llm-inference-gpu-smartnic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  定常状態のLLM推論でCPUが行うバッチ更新・KV管理・GPU起動をGPU常駐制御へ移し、要求受付とトークン送受信をSmartNICへ分離して、CPU干渉によるGPU待ちとコピー待ちを減らす実機システム。

- **2026-04 · [AUTOPOIESIS: A Self-Evolving System Paradigm for LLM Serving Under Runtime Dynamics](2026-2604.07144-autopoiesis-a-self-evolving-system-paradigm-for-llm-serving-under-runtim.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存のシステムは負荷に応じて配置計画を更新できても、その計画を作るアルゴリズム自体は事前に人間が設計した固定方針であることが多い。実行完了時間はそれぞれ平均27%、30%、44%短縮し、全体では平均34%、最大53%の改善を報告する。

- **2026-03 · [WWW.Serve: Interconnecting Global LLM Services through Decentralization](2026-2603.20661-www-serve-decentralized-global-llm-serving.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/WWW.Serve) ・ リポジトリ内被引用：0  
  信用量・持分証明・対戦評価・ゴシップ同期を組み合わせ、独立したLLM提供者が中央管理なしで要求を相互委譲しつつ、単一ノード比でSLO達成率最大1.5倍・遅延最大27.6%改善する。

- **2026-03 · [Understand and Accelerate Memory Processing Pipeline for Large Language Model Inference](2026-2603.29002-memory-processing-pipeline-gpu-fpga.md)**  
  実装：[✓](https://github.com/OswaldHe/HeteroLLM) ・ リポジトリ内被引用：0  
  疎注意・RAG・圧縮メモリを4段階の共通メモリ処理へ分解し、不規則・メモリ律速部分をFPGA、密計算をGPUへ割り当てて長文推論の遅延と消費エネルギーを削減する異種実行方式。

- **2026-03 · [StreamWise: Serving Multi-Modal Generation in Real-Time at Scale](2026-2603.05800-streamwise-serving-multi-modal-generation-in-real-time-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM単体の推論高速化が進んでも、音声・画像・動画を含む生成アプリケーションのエンドツーエンド遅延が同じ割合で短縮するわけではない。ポッドキャスト動画のように、ユーザーが再生を開始した直後から映像を継続供給するには、全動画の生成完了を待つバッチ方式では不十分である。

- **2026-03 · [Serving Hybrid LLM Loads with SLO Guarantees Using CPU-GPU Attention Piggybacking](2026-2603.12831-serving-hybrid-llm-loads-with-slo-guarantees-using-cpu-gpu-attention-piggybacking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUへ逃がした低優先度要求の注意計算を非同期化し、後続GPU密計算へ層単位で相乗りさせることで、SLOを守りながら低優先度スループットを最大9.85倍にする。

- **2026-03 · [S-HPLB: Efficient LLM Attention Serving via Sparsity-Aware Head Parallelism Load Balance](2026-2603.10353-s-hplb-efficient-llm-attention-serving-via-sparsity-aware-head-paralleli.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意行列の全要素を計算せず重要なトークンだけを残す疎注意（sparse 注意機構）は有効だが、各注意ヘッドに同じトークン数を割り当てると、少数のトークンで十分なヘッドには過剰計算を与え、多くのトークンを必要とするヘッドでは重要な情報を捨てる。

- **2026-03 · [Parallelization Strategies for Dense LLM Deployment: Navigating Through Application-Specific Tradeoffs and Bottlenecks](2026-2603.05692-parallelization-strategies-for-dense-llm-deployment-navigating-through-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  どのように分割するかは、単にメモリに載るかだけでなく、最初のトークンが出るまでの時間（TTFT）、出力トークン間隔（TPOT）、システム全体の出力トークン毎秒（TPS）の関係を決める。MI325x実機との相関を検証しているが、405BのTP8ではプリフィル平均誤差17.25%が報告され、デコードの予測精度はさらに低い。

- **2026-03 · [Parallel In-context Learning for Large Vision Language Models](2026-2603.16092-parallel-in-context-learning-for-large-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLaVA-OV-7BのMI-Bench-ICLで、例示数8→16→32に増やすと入力長は23,318→44,027→84,959トークン、平均遅延は1.004→2.376→3.479秒へ増加する。各群の予測を重み付き専門家積（weighted product of エキスパート、PoE）で統合し、全例示を一度に読んだときの分布を近似する。

- **2026-03 · [Multi-stage Flow Scheduling for LLM Serving](2026-2603.17456-multi-stage-flow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MFSは、遠隔KV取得・集団通信・プリフィルからデコードへの転送を依存付きの段階として追跡し、余裕のある通信を遅らせ、締切が近いフローを逆多段キューで昇格してTTFTのSLO違反を減らすネットワークスケジューラ。

- **2026-03 · [Duration Aware Scheduling for ASR Serving Under Workload Drift](2026-2603.11273-duration-aware-scheduling-for-asr-serving-under-workload-drift.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案するのは、短い要求を先に処理する最短仕事優先（Shortest Job First、SJF）と、待ち時間に応じて長い要求の優先度を上げる最高応答比率優先（Highest Response Ratio Next、HRRN）である。

- **2026-03 · [Compute-Optimal Resource Allocation for Distributed Large Language Model Inference in Cloud-Scale Intelligent Systems](2026-bbf3ba61cdaa-compute-optimal-resource-allocation-for-distributed-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論時に、複数の候補回答を生成して最良の回答を選ぶ手法は、単一の貪欲復号より高い正答率を得られる場合がある。Mistral-7B-v0.1とNVIDIA A4000を使った評価では、GSM8K正答率が固定best-of-16の65.1%から67.2%へ上がり、1,000要求当たり費用は0.85ドルから0.52ドルへ下がった。

- **2026-03 · [CoLLM: Continuous Adaptation for SLO-Aware LLM Serving on Shared GPU Clusters](2026-2604.16400-collm-continuous-adaptation-for-slo-aware-llm-serving-on-shared-gpu-clus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoLLMは、低ランク適応（Low-Rank Adaptation; LoRA）を利用するLLMサービスにおいて、推論専用に確保したGPUの遊休時間を、同じモデルの追加学習に再利用する共同実行システムである。

- **2026-03 · [CALVO: Improve Serving Efficiency for LLM Inferences with Intense Network Demands](2026-2603.21257-calvo-network-aware-kv-loading-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔KV読み込みを独立した非同期段階へ分離し、通信時間と計算時間を合わせた要求費用で順序付けすることで、長文脈の高キャッシュ再利用環境で平均最初のトークン時間を81.3%以上短縮し、期限達成率を最大61.67%改善する。

- **2026-03 · [AgentServe: Algorithm-System Co-Design for Efficient Agentic AI Serving on a Consumer-Grade GPU](2026-2603.10342-agentserve-consumer-gpu-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント処理を初回・再開プリフィルと短いデコードへ分け、TPOTフィードバックとGPU内SM予約で民生GPU上の相互干渉を抑える。

- **2026-02 · [RAM-Net: Linear-Time Sequence Modeling with Sparsely Addressable State](2026-2602.11958-ram-net-linear-time-sequence-modeling-with-sparsely-addressable-state.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全注意型Transformerは、過去トークンを独立したkey/valueとして保存し、現在のqueryに適合する位置へ集中してアクセスできる。一方でKVキャッシュは系列長に比例して増え、長文推論のメモリ容量と帯域を圧迫する。アドレスが重ならないトークン同士は同じ状態を汚さない。1.3Bでも実文書検索の全注意との差は残る。< の表1～3を参照した。

- **2026-02 · [QuRL: Efficient Reinforcement Learning with Quantized Rollout](2026-2602.13953-qurl-efficient-reinforcement-learning-with-quantized-rollout.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い思考系列では前者が学習時間の最大約70%を占める。生成用モデルだけを8ビットに量子化すれば行列積を高速化できるが、生成したトークンの確率分布が学習更新に使う高精度モデルと一致しなくなり、単純な置換は学習を不安定にする。INT8とFP8で検証し、量子化推論の要求処理量はモデル・GPUに応じて改善する。

- **2026-02 · [Multi-Layer Scheduling for MoE-Based LLM Reasoning](2026-2602.21626-multi-layer-scheduling-moe-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gimbalは、MoEサービングで実測KV使用量から要求の送り先、入力長からエンジン内の実行順、専門家の活性頻度と層間依存からGPU配置を決め、容量偏り・先頭待ち・専門家集中をまとめて減らす三層スケジューラ。

- **2026-02 · [Dynamic Micro-Batch and Token-Budget Scheduling for IoT-Scale Pipeline-Parallel LLM Inference](2026-4b60583e1d6f-dynamic-micro-batch-and-token-budget-scheduling-for-iot-scale-pipeline-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  4ノードのパイプライン並列LLM推論で、入力処理と逐次生成の負荷不均衡・通信待ちを減らすため、トークン予算とマイクロバッチ数を同時に動的調整するスケジューラを提案。RTX 4070 12GB×4、Llama-2-13BとQwen2.5-14B、100/1000Mbpsのネットワークで評価。

- **2026-02 · [Bit-serial Acceleration of LLM Inference with Mixture-of-Datatype Quantization](2026-be8124062d48-bit-serial-acceleration-of-llm-inference-with-mixture-of-datatype-quanti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、言語モデルの重みと鍵・値キャッシュ（KVキャッシュ）の双方を3〜4ビット程度に圧縮しても推論品質を保ち、その圧縮表現を16ビット浮動小数点へ全面展開せず計算できる専用ハードウェアを設計する研究である。端末向け単一バッチでは、損失なしの設定でFP16専用アクセラレータに対し識別課題2.1倍、生成課題2.4倍の平均高速化を報告する。

- **2026-02 · [A State-Transition Framework for Efficient LLM Reasoning](2026-2602.01198-a-state-transition-framework-for-efficient-llm-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、長い思考連鎖（Chain-of-Thought; CoT）を生成する言語モデルで、思考トークンを短く削ることなく、過去の推論を保持するためのKVキャッシュと注意計算を減らす方式を提案する。Qwen2.5-1.5Bの数学5課題平均正答率は基盤モデルの51.5%から56.2%、平均推論遅延は300.0秒から253.0秒となった。

- **2026-01 · [RelServe: Fast LLM Inference Serving on Relational Data](2026-2601.11546-relserve-fast-llm-inference-serving-on-relational-data.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RelServeは、表の各行へ同じテンプレートのLLM処理を適用する問い合わせ（relQuery）を、オンラインで低遅延に実行するための推論基盤である。静的な短い仕事優先方式は開始前の待ち時間を減らせても、処理が進んだ後の残作業や共有接頭辞キャッシュの利用状況を反映しない。

- **2026-01 · [RelayGR: Scaling Long-Sequence Generative Recommendation via Cross-Stage Relay-Race Inference](2026-2601.01712-relaygr-scaling-long-sequence-generative-recommendation-via-cross-stage-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  そこでRelayGRは、選択的な先行実行、利用者IDによる同一インスタンスへの振分け、ホストメモリへの短期退避を一体で設計する。

- **2026-01 · [RAPID-Serve: Resource-efficient and Accelerated P/D Intra-GPU Disaggregation](2026-2601.11822-rapid-serve-intra-gpu-pd-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同一GPU内でプリフィル/デコードを非lockstep並行実行し、共有KVとCU maskingでSLOと利用率を両立、MI300X実機で有効スループット平均4.9倍を報告。

- **2026-01 · [Mico: efficient query scheduling for multi-cloud deployed LLM inference service](2026-e363df893fb4-mico-efficient-query-scheduling-for-multi-cloud-deployed-llm-inference-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求数だけを均等に複数クラウドへ振り分けても、長い応答が特定クラウドへ集中すると他のクラウドが先に空き、システム全体の完了時刻とスループットが悪化する。GPT-2/GPT-Neoを使ったA6000の評価では、3クラウド・200要求・バッチ3の条件で累積KVキャッシュ長が44.89%減少し、要求処理スループットが1.79倍になった。

- **2025-12 · [xGR: Efficient Generative Recommendation Serving at Scale](2025-2512.11529-xgr-efficient-generative-recommendation-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の対話型LLMとは異なり、入力は数百〜数千トークンと長い一方、出力は商品を表す数個のトークンに限られる。著者は注意演算子xAttention、探索アルゴリズムxBeam、実行管理xScheduleの三つをxLLM上に統合する。

- **2025-12 · [SpaceServe: Spatial Multiplexing of Complementary Encoders and Decoders for Multimodal LLMs](2025-b801ff7cdf66-spaceserve-spatial-multiplexing-of-complementary-encoders-and-decoders-f.md)**  
  実装：[✓](https://github.com/gofreelee/SpaceServe) ・ リポジトリ内被引用：0  
  画像エンコーダは大きな行列演算を行う計算律速、デコーダの1トークン生成は重み・KVキャッシュの読み込みが支配的なメモリ律速になりやすい。SMを何基ずつ割り当てるかはオフラインの演算子プロファイルから作る資源効用曲線に基づき、要求の画像解像度・入力長・負荷に応じてオンラインで変える。

- **2025-12 · [ProServe: Unified Multi-Priority Request Scheduling for LLM Serving](2025-2512.12928-proserve-unified-multi-priority-request-scheduling-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  局所ではSlideBatchingが負荷に応じて期限順と利得密度順を切り替え、割り込みで必要になるKVキャッシュの退避・復元を計算と重ねる。Qwen2-7B・Qwen3-32BとAscend 910B上の評価で、比較スケジューラに対しシステム利得最大35%、SLO達成率最大52%の改善を報告した。

- **2025-12 · [MultiPath Transfer Engine: Breaking GPU and Host-Memory Bandwidth Bottlenecks in LLM Services](2025-2512.16056-multipath-transfer-engine-gpu-host-memory-bandwidth.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数GPUのホスト接続とGPU間リンクを透過的に束ね、ホスト・GPU間帯域を最大245GB/s、標準比4.62倍へ高め、初回トークン時間とモデル切替を最大2.38倍、2.48倍高速化。

- **2025-12 · [MS-SSM: A Multi-Scale State Space Model for Efficient Sequence Modeling](2025-2512.23824-ms-ssm-a-multi-scale-state-space-model-for-efficient-sequence-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  状態空間モデル（state space モデル; SSM）は、過去の情報を有限次元の内部状態へ圧縮し、入力を逐次取り込むことで長い系列を効率よく処理する。ListOpsの階層演算予測ではMambaの38.02%に対してMS-SSM(S6)は63.04%、MS-SSM(S4)は62.83%を報告する。

- **2025-12 · [Efficient Mixture-of-Agents Serving via Tree-Structured Routing, Adaptive Pruning, and Dependency-Aware Prefill-Decode Overlap](2025-2512.18126-efficient-mixture-of-agents-serving-via-tree-structured-routing-adaptive.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FaSTeR-MoAは、複数の大規模言語モデル（large language モデル、LLM）が候補回答を生成し、別のモデルが統合するエージェント混合（mixture of agents、MoA）の推論処理を高速化する方式である。

- **2025-11 · [Seer Self-Consistency: Advance Budget Estimation for Adaptive Test-Time Scaling](2025-2511.09345-seer-self-consistency-advance-budget-estimation-for-adaptive-test-time-s.md)**  
  実装：[✓](https://github.com/noforit/SeerSC) ・ リポジトリ内被引用：0  
  複数の推論経路を生成して最頻回答を選ぶ自己整合（自己整合性; SC）は、数学問題などで単一路線の思考連鎖より正解率を上げられる。各問題へ一律に $N$ 経路を割り当てると、容易な問題へも大量のトークンを使う。

- **2025-11 · [Safety-Preserving PTQ via Contrastive Alignment Loss](2025-2511.07842-safety-preserving-ptq-via-contrastive-alignment-loss.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、大規模言語モデル（Large Language モデル、LLM）の学習後量子化（Post-学習 量子化、PTQ）における目的関数の不足を扱う。LLaMA3.1-8B-Instructの重み4ビット・活性値4ビット（W4A4）条件で、安全性評価SafetyBenchは比較方式OSTQuantの57.5からCAQの60.1へ2.6ポイント改善した。

- **2025-11 · [Parallel Vision Token Scheduling for Fast and Accurate Multimodal LMMs Inference](2025-2511.18875-parallel-vision-token-scheduling-for-fast-and-accurate-multimodal-lmms-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ParVTS（Parallel Vision Token Scheduling）は、高解像度画像を入力するマルチモーダル大規模言語モデル（MLLM）において、視覚トークンを一律に残すか捨てるかという二者択一を避ける推論時手法である。

- **2025-11 · [Optimizing Long-context LLM Serving via Fine-grained Sequence Parallelism](2025-2511.06247-optimizing-long-context-llm-serving-via-fine-grained-sequence-parallelis.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  系列並列化（sequence parallelism、SP）は一つの入力系列を複数GPUへ分けて注意計算を実行する技術だが、要求全体に固定のSP数を割り当てると、先に空いたGPUだけでは開始できず、同期相手を待つ時間が生じる。

- **2025-11 · [MoSKA: Mixture of Shared KV Attention for Efficient Long-Sequence LLM Inference](2025-2511.06010-moska-mixture-of-shared-kv-attention-for-efficient-long-sequence-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoSKA（Mixture of Shared KV 注意機構）は、複数のLLM要求が共通の長大な文書・知識ベースを参照する状況で、KVキャッシュを共有して容量を節約するだけではメモリ帯域の負荷が解消しないという問題を扱う。

- **2025-11 · [MaverIQ: Fingerprint-Guided Extrapolation and Fragmentation-Aware Layering for Intent-Based LLM Serving](2025-ef9c70168212-maveriq-fingerprint-guided-extrapolation-and-fragmentation-aware-layerin.md)**  
  実装：[✓](https://github.com/UT-SysML/MaverIQ) ・ リポジトリ内被引用：0  
  MaverIQは、大規模言語モデル（Large Language モデル; LLM）の推論サービスを配備する際、利用者が「遅延を最小化したい」「費用上限を守りたい」「精度を落とせない」といった目的を指定するだけで、モデル圧縮、テンソル並列（テンソル Parallelism; TP）、パイプライン並列（パイプライン Parallelism…

- **2025-11 · [C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning](2025-2511.07396-c3po-optimized-large-language-model-cascades-with-probabilistic-cost-con.md)**  
  実装：[✓](https://github.com/AntonValk/C3PO-LLM) ・ リポジトリ内被引用：0  
  すべての質問を最も高価なモデルへ送るのではなく、小型モデルが容易な質問へ回答し、難しい質問だけを高性能モデルへ順に送る方式をカスケード推論（cascaded inference）という。

- **2025-11 · [A Scalable NorthPole System with End-to-End Vertical Integration for Low-Latency and Energy-Efficient LLM Inference](2025-2511.15950-a-scalable-northpole-system-with-end-to-end-vertical-integration-for-low.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はIBMの専用ニューラル推論アクセラレータNorthPoleを288枚組み合わせ、18台の2Uサーバからなるラックへ実装した大規模言語モデル推論システムである。2,048トークン文脈、28同時利用者の一インスタンスで、最初のトークンまでの時間64.8ミリ秒、トークン間遅延2.8ミリ秒、出力処理量10,341トークン/秒を報告する。

### 2年前（2024-11〜2025-10）

- **2025-02 · [Autellix: An Efficient Serving Engine for LLM Agents as General Programs](2025-2502.13965-autellix-agent-program-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：57  
  エージェントのLLM呼び出しをプログラム単位で追跡し、累積サービス時間と動的DAGの重要経路近似で優先順位を付け、KV局所性を保つ複数GPUルーティングまで組み合わせてプログラム全体の待ち時間を削減する。

- **2025-04 · [MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism](2025-2504.02263-megascale-infer-disaggregated-expert-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：46  
  注意機構とMoE専門家FFNを別GPU群へ分離し、複数注意レプリカから専門家要求を集約して大きな専門家バッチを作り、専用多対多RDMA通信とピンポン型パイプラインで通信を隠す大規模MoEサービング方式。

- **2025-02 · [LServe: Efficient Long-sequence LLM Serving with Unified Sparse Attention](2025-2502.14866-lserve-efficient-long-sequence-llm-serving-with-unified-sparse-attention.md)**  
  実装：[✓](https://github.com/mit-han-lab/omniserve) ・ リポジトリ内被引用：32  
  長文LLMでは、プリフィルでは系列長に対して二乗で増える注意計算、デコードでは過去KVを毎トークン読み直すメモリ帯域が別々の律速になる。LServeは両者をブロック疎注意（block-sparse 注意機構）という共通の実行形式へ落とし、オフラインで決めるストリーミングヘッドと、実行時に選ぶ重要KVページを同じカーネル群で処理する。

- **2025-05 · [Prism: Unleashing GPU Sharing for Cost-Efficient Multi-LLM Serving](2025-2505.04021-prism-gpu-sharing-multi-llm-serving.md)**  
  実装：[✓](https://github.com/ovg-project/kvcached) ・ リポジトリ内被引用：31  
  GPU物理メモリをモデル横断で動的再配分し、空間共有と時間共有を負荷に応じて切り替える多モデル提供基盤。

- **2025-08 · [InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency](2025-2508.18265-internvl3-5-advancing-open-source-multimodal-models-in-versatility-reaso.md)**  
  実装：[✓](https://github.com/OpenGVLab/InternVL) ・ リポジトリ内被引用：30  
  推論効率に直接関係する二つの提案は、視覚解像度ルータ（Visual Resolution Router; ViR）と視覚・言語分離配置（Decoupled Vision-Language Deployment; DvD）である。最後の値は通常配置の4.05倍である。

- **2025-10 · [Aegaeon: Effective GPU Pooling for Concurrent LLM Serving on the Market](2025-3731569.3764815-aegaeon-gpu-pooling.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  トークン単位の先取り自動スケーリングと高速モデル切替で多数LLMをGPUプールへ集約し、実運用でGPU数を82%削減したマルチモデル推論基盤。

- **2025-01 · [AdaServe: Accelerating Multi-SLO LLM Serving with SLO-Customized Speculative Decoding](2025-2501.12162-adaserve-multi-slo-speculative-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  GPU検証予算を各リクエストのSLO達成用トークンへ優先配分し、残余をスループット向上へ回す投機的デコード配信で、SLO違反を最大4.3倍削減する。

- **2025-08 · [Strata: Hierarchical Context Caching for Long Context Language Model Serving](2025-2508.18572-strata-hierarchical-context-caching-for-long-context-language-model-serv.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  GPUに載りきらない接頭辞KVをCPUやSSDへ置くだけでは、復帰時の小ページ転送とロード待ちが性能を支配する。StrataはGPU支援転送、階層別メモリ配置、I/Oを資源として扱う要求スケジューリングを一体化する。

- **2025-04 · [SLOs-Serve: Optimized Serving of Multi-SLO LLMs](2025-2504.08784-slos-serve-multi-slo-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  段階別SLOを動的計画法で扱い、チャンク化プリフィル・投機的デコード・入場制御・レプリカルーティングを統合してGPU当たり容量を平均2.2倍改善する。

- **2024-11 · [BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching](2024-2412.03594-batchllm-optimizing-large-batched-llm-inference-with-global-prefix-shari.md)**  
  実装：[✓](https://github.com/microsoft/MixLLM/tree/batchllm_vllm_064) ・ リポジトリ内被引用：27  
  BatchLLMは、検索結果の説明文生成、広告文書の変換、推薦候補の採点など、数千件以上のプロンプトをまとめて処理する大規模言語モデル（LLM）の一括推論を対象とするシステムである。原著のMLSys 2026産業部門版は、NVIDIA A100とAMD MI200上で、vLLMやSGLangに対して1.3～10.8倍の端点処理率改善を報告する。

- **2025-02 · [SageServe: Optimizing LLM Serving on Cloud Data Centers with Forecast Aware Auto-Scaling](2025-2502.14617-sageserve-multi-timescale-cloud-autoscaling.md)**  
  実装：[✓](https://github.com/shashwatj07/SageServe) ・ リポジトリ内被引用：25  
  対話型と非対話型の要求を統合GPUプールで共有し、地域間ルーティング、需要予測、整数線形計画、遅延実行を異なる時間尺度で連携させる。Office 365の本番トレースでSLOを維持しつつGPU時間を最大25%削減した。

- **2024-11 · [Marconi: Prefix Caching for the Era of Hybrid LLMs](2024-2411.19379-marconi-prefix-caching-for-the-era-of-hybrid-llms.md)**  
  実装：[✓](https://github.com/ruipeterpan/marconi) ・ リポジトリ内被引用：25  
  言語モデルの接頭辞キャッシュ（Prefix Caching）は、複数要求が共有するシステム指示や会話履歴の前半部分について、過去に計算した内部状態を再利用して初回トークン生成までの時間を短縮する。主要評価では、拡張vLLMに対するトークン命中率がLMSysで平均4.5倍、ShareGPTで7.3倍、SWEBenchで34.4倍となる。

- **2025-04 · [JITServe: SLO-aware LLM Serving with Imprecise Request Information](2025-2504.20068-jitserve-slo-aware-llm-serving-with-imprecise-request-information.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  不確かな出力長と依存関係を逐次更新し、期限達成に必要な最小帯域で要求を選ぶことで、サービス有効処理量を1.4〜6.3倍へ改善する。

- **2025-04 · [semi-PD: Towards Efficient LLM Serving via Phase-Wise Disaggregated Computation and Unified Storage](2025-2504.19867-semi-pd-phase-wise-disaggregated-unified-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  入力処理と逐次生成の計算をSM単位で分離しつつ高帯域メモリを共有し、完全分離方式のKV転送と保存容量の偏りを除いてエンドツーエンド遅延を最大2.58倍改善する。

- **2025-02 · [HexGen-2: Disaggregated Generative Inference of LLMs in Heterogeneous Environment](2025-2502.07903-hexgen-2.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  異種GPU上の事前充填・復号分離を、グラフ分割と最大流で段階別並列化・資源配置・KV転送まで共同最適化するLLMサービング方式。

- **2025-08 · [Prefill-Decode Aggregation or Disaggregation? Unifying Both for Goodput-Optimized LLM Serving](2025-2508.01989-taichi-unified-prefill-decode-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  プリフィル重視/デコード重視インスタンスを混在させ、要求ごとのTTFT・TPOT余裕を別要求へ移すことで集約型と分離型を統一するLLM配信基盤。既存集約型比9〜47%、分離型比29〜77%グッドプットを改善する。

- **2025-01 · [Efficiently Serving Large Multimodal Models Using EPD Disaggregation](2025-2501.05460-efficiently-serving-large-multimodal-models-using-epd-disaggregation.md)**  
  実装：[✓](https://github.com/vbdi/epdserve) ・ リポジトリ内被引用：20  
  本論文は大規模マルチモーダルモデル（Large Multimodal モデル、LMM）の推論を、マルチモーダル符号化（Encode、E）、事前入力処理（プリフィル、P）、逐次復号（デコード、D）の三段階に分離するEPD分離（EPD Disaggregation）を提案する。

- **2025-04 · [Optimizing LLM Inference: Fluid-Guided Online Scheduling with Memory Constraints](2025-2504.11320-fluid-guided-online-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  流体平衡からデコード進捗区間ごとのGPU常駐構成を見積もり、WAIT/Nested WAITで制御する。未知の出力長は予測せず、生成を継続する残存要求を段階分類してKV追い出し連鎖を抑えるスケジューラ。

- **2025-02 · [ModServe: Modality- and Stage-Aware Resource Disaggregation for Scalable Multimodal Model Serving](2025-2502.00937-modserve.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  画像処理・画像符号化とテキスト生成を独立プールへ分離し、モダリティ別ルーティングと自動拡縮でLMMの末尾遅延とGPU費用を削減する。

- **2025-02 · [Demystifying Cost-Efficiency in LLM Serving over Heterogeneous GPUs](2025-2502.00722-demystifying-cost-efficiency-in-llm-serving-over-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  次に、どのGPUを何台借りるか、各GPU群にモデルを何個複製しどの並列方式で載せるか、要求種別をどの複製へ何割ずつ振り分けるかを、価格上限と実際のGPU在庫を制約にした混合整数線形計画（Mixed-Integer Linear Programming; MILP）として表す。

- **2025-01 · [DeepServe: Serverless Large Language Model Serving at Scale](2025-2501.14417-deepflow-serverless-llm-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  要求・ジョブ・タスク抽象、NPU中心FlowServe、KV局所性とPD構成を統合した分散スケジューラ、NPU-fork等の高速スケールを組み合わせたHuawei Cloud本番サーバーレスLLM基盤。

- **2024-12 · [BLITZSCALE: Fast and Live Large Model Autoscaling with O(1) Host Caching](2024-2412.17246-blitzscale-fast-and-live-large-model-autoscaling-with-o-1-host-caching.md)**  
  実装：[✓](https://github.com/blitz-serving/blitz-scale) ・ リポジトリ内被引用：18  
  一方、需要を観測してから新しい提供インスタンスを起動する従来方式では、数十GBから数百GBの重みをストレージやホストメモリからGPUへロードする時間が長く、急な要求増加に追いつけない。

- **2024-11 · [BlendServe: Optimizing Offline Inference for Auto-regressive Large Models with Resource-aware Batching](2024-2411.16102-blendserve-optimizing-offline-inference-for-auto-regressive-large-models.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  本論文は、応答を即時返す必要のないオフライン大規模言語モデル推論で、要求の並べ替えによってGPUの計算器とメモリ帯域を同時に使う方式を提案する。一次論文v1のA100・Llama 3.1 8B実機評価では、最良の比較対象NanoFlow-DFSに対して19.34〜22.65%の処理量改善、vLLMに対して最大1.44倍の改善を報告する。

- **2025-05 · [AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning](2025-2505.24298-areal-a-large-scale-asynchronous-reinforcement-learning-system-for-langu.md)**  
  実装：[✓](https://github.com/inclusionAI/AReaL) ・ リポジトリ内被引用：17  
  AReaLは、長い推論列を生成する大規模推論モデル（大規模推論モデル（Large Reasoning モデル; LRM））の強化学習（強化学習（reinforcement learning; RL））で、ロールアウト生成とパラメータ更新を同じバッチ障壁で交互実行する同期方式をやめ、生成GPU群と学習GPU群を完全に分離する学習システムである。

- **2025-07 · [Nexus: Proactive Intra-GPU Disaggregation of Prefill and Decode in LLM Serving](2025-2507.06608-nexus-proactive-intra-gpu-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  同一GPU内でプリフィル/デコードをproactiveにSM分割し、計算飽和とメモリ帯域競合をモデル化してvLLM比最大2.2倍スループット・20倍TTFT改善を達成する。

- **2025-02 · [AIBrix: Towards Scalable, Cost-Effective Large Language Model Inference Infrastructure](2025-2504.03648-aibrix-towards-scalable-cost-effective-large-language-model-inference-in.md)**  
  実装：[✓](https://github.com/vllm-project/aibrix) ・ リポジトリ内被引用：16  
  GPU利用率のみで自動スケーリングすれば、入力長と出力長の差、復号負荷、KV容量圧迫を適切に反映できない。提案は、Kubernetesによる粗粒度資源管理を残しつつ、LLMのトークン処理量・接頭辞一致・KV使用量・アダプター配置・GPU別費用を観測する仕組みを導入する。

- **2024-12 · [Efficiently Scaling LLM Reasoning with Certaindex](2024-2412.20993-efficiently-scaling-llm-reasoning-with-certaindex.md)**  
  実装：[✓](https://github.com/hao-ai-lab/Dynasor) ・ リポジトリ内被引用：16  
  複雑な問題に対して大規模言語モデル（LLM）が長い思考過程を生成したり、複数経路を探索したりする場合、計算を増やすほど正答率が上がるとは限らない。本研究の焦点は、難度を入力問題の外見から事前に予測するのではなく、推論を実際に進めた結果、回答がどこまで安定したかを観測することである。

- **2025-02 · [HydraServe: Minimizing Cold Start Latency for Serverless LLM Serving in Public Clouds](2025-2502.15524-hydraserve-serverless-cold-start.md)**  
  実装：[✓](https://github.com/LLMServe/hydraserve) ・ リポジトリ内被引用：15  
  起動時だけモデル層を複数サーバーへ分散して帯域を束ね、重み取得・GPU転送・実行環境初期化を重ね、起動後にワーカーを集約することでサーバーレスLLMのコールドスタートを1.7〜4.7倍短縮する。

- **2024-12 · [KVDirect: Distributed Disaggregated LLM Inference](2024-2501.14743-kvdirect-distributed-disaggregated-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  分離型推論（disaggregated inference）は、長い入力列を処理する入力処理（プリフィル）と、一トークンずつ出力する復号（デコード）を別のGPUワーカーに担当させる。最大4台のH100サーバを使った実験では、vLLMの一体型推論に対してarXiv論文要約負荷で要求遅延55%減、ShareGPT対話負荷で24%減を報告した。

- **2024-11 · [Context Parallelism for Scalable Million-Token Inference](2024-2411.01783-context-parallelism-for-scalable-million-token-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  本研究は、巨大な言語モデルの推論において、長い入力を処理する最初の一回の待ち時間を短縮する文脈並列（context parallelism）の実装を扱う。提案の中心は、リング状の通信で鍵・値を巡回させるpass-KVと、逆に問い合わせを巡回させるpass-Qを、推論段階と既存キャッシュの割合に応じて切り替えることである。

- **2025-08 · [LLM Serving Optimization with Variable Prefill and Decode Lengths](2025-2508.06133-llm-serving-optimization-variable-prefill-decode-lengths.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  要求ごとのプリフィル長とデコード長を考慮し、KV容量を守るバッチをF指標で選ぶスケジューラ。Vidur時間モデルでは混合2000要求の平均遅延をFCFS比4.87倍改善した。

- **2025-04 · [LLM推論とAIエージェント向けスループット最適スケジューリング](2025-2504.07347-throughput-optimal-scheduling-llm-inference-ai-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  混合バッチを仕事で埋める方式がいつ最大処理量を達成するかを待ち行列理論で証明し、AIエージェントの分岐処理網への拡張と、成立しない経路構造・運用制約も示す。

- **2025-01 · [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  クライアントごとのサービス量を公平に保ちつつ、公平性が大きく崩れない範囲だけ実行順を入れ替えて、同じ接頭辞を持つリクエストを続けて処理しKV再利用を増やすスケジューラ。複数GPUでは負荷分散も同時に調整する。

- **2025-10 · [Pie: A Programmable Serving System for Emerging LLM Applications](2025-2510.24051-pie-a-programmable-serving-system-for-emerging-llm-applications.md)**  
  実装：[✓](https://github.com/pie-project/pie) ・ リポジトリ内被引用：13  
  生成ループを細粒度APIへ分解し、Wasm inferletがKV・復号・入出力を直接制御しつつ適応一括処理でGPU効率を維持するプログラマブルLLMサービング基盤。

- **2025-09 · [Parallax: Efficient LLM Inference Service over Decentralized Environment](2025-2509.26182-parallax-decentralized-heterogeneous-serving.md)**  
  実装：[✓](https://github.com/GradientHQ/parallax) ・ リポジトリ内被引用：13  
  地理的に離れた異種GPUでモデル層を地域・VRAM・計算性能に合わせて配置し、GPUごとの処理時間と通信遅延から要求ごとの層経路を選ぶことで、遅いGPU・低速回線によるパイプライン待ちを減らす分散LLMサービング。

- **2025-07 · [PolyServe: Efficient Multi-SLO Serving at Scale](2025-2507.17769-polyserve-efficient-multi-slo-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  PolyServeは、LLM配信サービスに複数の遅延保証階層がある場合に、要求をどのサーバへ送るか、各階層へ何台のサーバを割り当てるかを共同で制御する方式である。SLO達成率90%の点で、既存方式に対する有効処理量（有効スループット）はプリフィル・デコード分離構成で平均1.23倍、同居構成で平均1.18倍である。

- **2025-03 · [Injecting Adrenaline into LLM Serving: Boosting Resource Utilization and Throughput via Attention Disaggregation](2025-2503.20552-adrenaline.md)**  
  実装：[✓](https://github.com/ASISys/Adrenaline) ・ リポジトリ内被引用：13  
  デコード注意をプリフィルGPUの余剰HBMへ動的に移し、低遅延同期・GPU資源分割・負荷連動制御で分離配信の資源偏りを解消する。

- **2025-01 · [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  対話型リクエストの遅延目標を守りながら余ったGPU容量をバッチリクエストへ使うため、各GPUで同時処理するリクエスト数を素早く増減する制御と、クラスタ全体のGPUインスタンス数を遅い周期で増減する制御を分けたLLM自動スケーラ。

- **2025-05 · [PrefillOnly: An Inference Engine for Prefill-only Workloads in Large Language Model Applications](2025-2505.07203-prefillonly-an-inference-engine-for-prefill-only-workloads-in-large-language-model-applications.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  PrefillOnlyはこの出力が一トークンで終了する要求を別の負荷クラスとして定義し、通常の生成要求と同じエンジンで処理する無駄を削減する。提案は大きく二つある。結果として、比較方式より1.4～4.0倍の要求到着率を、平均遅延と99パーセンタイル遅延を悪化させずに処理できる領域があった。

- **2025-05 · [HydraInfer: Hybrid Disaggregated Scheduling for Multimodal Large Language Model Serving](2025-2505.12658-hydrainfer-hybrid-epd-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  画像符号化・入力処理・デコードを異種段階として扱い、負荷とSLOに応じてE+P+D、EP+D、ED+Pを選ぶ混成分離と段階別バッチ・二重ストリームを組み合わせ、マルチモーダル配信のグッドプットを高める。

- **2025-04 · [Towards High-Goodput LLM Serving with Prefill-decode Multiplexing](2025-2504.14489-towards-high-goodput-llm-serving-with-prefill-decode-multiplexing.md)**  
  実装：[✓](https://github.com/ykcombat/sglang/tree/slo_config) ・ リポジトリ内被引用：12  
  前者は大きな行列積を実行しやすい一方、後者は各反復で重みとキャッシュを読み出すためメモリ帯域の制約を受けやすい。両段階を別々のGPUへ割り当てる分離配信は干渉を避けられるが、要求が片方に偏ると計算資源が遊休し、キャッシュの保存先も分かれる。

- **2025-02 · [λScale: Enabling Fast Scaling for Serverless Large Language Model Inference](2025-2502.09922-lambdascale-serverless-fast-scaling.md)**  
  実装：[✓](https://github.com/lambda-scale/lambda-scale) ・ リポジトリ内被引用：12  
  モデル重みをRDMAで多段配信し、全重みの到着を待たず受信済み層から分散推論を始めるサーバレス拡張方式。実負荷トレースで末尾TTFTを最大5倍改善し、累積GPU資源を最大31.3%削減する。

- **2025-06 · [Beyond the Buzz: A Pragmatic Take on Inference Disaggregation](2025-2506.05508-beyond-the-buzz-a-pragmatic-take-on-inference-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  二つの段階を同じGPU群で混在させる同居方式は、片方を最適化するともう片方が悪化しやすい。

- **2025-04 · [FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling](2025-2504.03775-flowkv-low-latency-transfer-load-aware.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  KVキャッシュを連続セグメントへ寄せてNCCL転送をまとめ、全体負荷に応じてプリフィル／デコード役割も切り替える分離推論基盤。転送遅延を最大96.8%削減し、LongBenchで15.2〜48.9%短縮。

- **2025-04 · [Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving](2025-2504.07494-apt-serve-hybrid-cache-adaptive-scheduling.md)**  
  実装：[✓](https://github.com/eddiegaoo/Apt-Serve) ・ リポジトリ内被引用：11  
  KVキャッシュと半分の容量で済む隠れ状態キャッシュを反復ごとに切り替え、待機時間・メモリ量に基づく近似比2の適応バッチ編成でTTFTのSLO崩壊を抑え、有効スループットをvLLM比最大8.8倍へ高める。

- **2025-03 · [throttLL’eM: Predictive GPU Throttling for Energy Efficient LLM Inference Serving](2025-778bb2a31fb4-throttll-em-predictive-gpu-throttling-for-energy-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/WilliamBlaskowicz/throttLL-eM) ・ リポジトリ内被引用：11  
  固定した最大周波数でGPUを動かすと低負荷時に余分な電力を使うが、単純に周波数を下げると同時要求数やKVキャッシュ量が増えたとき遅延が悪化する。著者らは、要求の生成長を予測し、将来の各復号反復におけるバッチサイズとKVキャッシュ使用量を推定する。

- **2025-02 · [ThunderServe: High-performance and Cost-efficient LLM Serving in Cloud Environments](2025-2502.09334-thunderserve-high-performance-and-cost-efficient-llm-serving-in-cloud-en.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  ThunderServeは、同種の高性能GPUを大量に確保できない環境で、大規模言語モデル（LLM）の推論を低コストかつ高いサービス水準で提供する分散サービング方式である。

- **2025-08 · [Kairos: Low-latency Multi-Agent Serving with Shared LLMs and Excessive Loads in the Public Cloud](2025-2508.06948-kairos-multi-agent-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  動的ワークフローから残り遅延分布を学習して短く完了しやすいエージェントを優先し、将来KVメモリ需要を時間枠で予測してLLM実体へ配置するマルチエージェント配信基盤。

- **2025-06 · [WindServe: Efficient Phase-Disaggregated LLM Serving with Stream-based Dynamic Scheduling](2025-8e0fd88d7ddc-windserve-efficient-phase-disaggregated-llm-serving-with-stream-based-dy.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  DistServeやSplitwiseのように別GPUへ二段階を分離すれば互いの干渉を抑えられるが、プリフィル GPUが混雑しデコード GPUが遊休になる場合、あるいは逆にデコード GPUがKVキャッシュで満杯なのにプリフィル GPUが空く場合、固定役割は資源を無駄にする。

- **2025-03 · [Seesaw: High-throughput LLM Inference via Model Re-sharding](2025-2503.06433-seesaw-high-throughput-llm-inference-via-model-re-sharding.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  プリフィルとデコードでモデルの並列分割を動的に切り替え、CPU階層KVバッファと遷移最小化で再配置費用を償却し、vLLM比最大1.78倍・平均1.36倍のスループットを達成する。

- **2025-02 · [EcoServe: Designing Carbon-Aware AI Inference Systems](2025-2502.05043-ecoserve-carbon-aware-ai-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  運用時炭素と製造由来炭素を同時最適化し、4Rと整数線形計画でLLM配信の総炭素をSLO維持のまま最大47%削減するEcoServe。

- **2025-09 · [Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism](2025-2509.08309-hetis-heterogeneous-gpu-dynamic-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  異種GPUの遅い機種を密演算経路から外し、デコード注意をヘッド単位で動的分配してKVキャッシュも部分移行することで、計算・通信・メモリの不均衡を同時に抑えるLLMサービング方式。

- **2025-06 · [SLED: A Speculative LLM Decoding Framework for Efficient Edge Serving](2025-2506.09397-sled-a-speculative-llm-decoding-framework-for-efficient-edge-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  通常の投機的復号（投機的復号）は、小型モデルが複数候補を提案し、大型モデルが一回の前向き計算で受理・棄却を判定する。

- **2025-04 · [SLO-Aware Scheduling for Large Language Model Inferences](2025-2504.14966-slo-aware-scheduling-for-large-language-model-inferences.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  チャットとコード生成のように異なるサービス品質目標（Service Level Objective; SLO）を持つ要求を一つの先着順で処理せず、入力長・予想出力長・要求ごとのSLOから「どの順序・どのバッチなら何件が期限内に終わるか」を推定し、焼きなまし法（シミュレーション Annealing）で優先順を探索する。

- **2025-03 · [Teola: Towards End-to-End Optimization of LLM-based Applications](2024-2407.00326-teola.md)**  
  実装：[✓](https://github.com/NetX-lab/Ayo) ・ リポジトリ内被引用：9  
  LLMアプリをプリミティブ依存グラフへ分解し、モジュール横断の並列化・パイプライン化とトポロジ認識バッチングでエンドツーエンド遅延を短縮する。

- **2025-01 · [Mell: Memory-Efficient Large Language Model Serving via Multi-GPU KV Cache Management](2025-2501.06709-mell-multi-gpu-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  複数GPUでLLMを提供すると、要求ごとの出力長の違いでKVキャッシュが一方のGPUだけに膨らみ、空きGPUを使えない。Mellは実行中要求をGPU間で移し、通信余力があればKV本体を転送し、演算余力があればトークンだけを送り移行先で再プリフィルして偏りを抑える。

- **2025-09 · [VoltanaLLM: Feedback-Driven Frequency Control and State-Space Routing for Energy-Efficient LLM Serving](2025-2509.04827-voltanallm-feedback-driven-frequency-control-and-state-space-routing-for-energy-efficient-llm-serving.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/VoltanaLLM) ・ リポジトリ内被引用：8  
  P/D分離配信で周波数制御・遅延予測・状態空間ルーティングを連動し、SLOを保ちながら最大36.3%省エネするVoltanaLLM。

- **2025-04 · [Efficient LLM Serving on Hybrid Real-time and Best-effort Requests](2025-2504.09590-bros-hybrid-real-time-best-effort-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  RTのTTFT/TPOT締切を動的優先度にした反復単位スケジューリングと、RT/BEが同じKVブロックを逆方向から共有する双方向KV管理で、混在負荷の遅延と処理量を両立する。

- **2025-03 · [Niyama: Breaking the Silos of LLM Inference Serving](2025-2503.22562-niyama-breaking-the-silos-of-llm-inference-serving.md)**  
  実装：[✓](https://github.com/microsoft/sarathi-serve/tree/niyama_asplos2026) ・ リポジトリ内被引用：8  
  対話・コード補完・要約などを「対話型」「バッチ型」の別GPU群へ固定せず、要求ごとの細かなサービス品質（Quality of Service; QoS）期限を同じGPUプールで扱う配信系。Niyamaはデコード要求の締切余裕を見ながらプリフィルの分割サイズを動的に変え、期限優先と残り仕事量優先を混ぜ、過負荷時には少数要求だけを低優先度へ降格する。

- **2025-02 · [Universal Model Routing for Efficient LLM Inference](2025-2502.08773-universal-model-routing-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  新LLMを代表プロンプト群へのクラスタ別誤差ベクトルで表現し、ルータ再学習なしで動的モデルプールへ追加するUniRouteが、30超の未観測LLMを含む評価でK-NN/ZeroRouterを上回る。

- **2025-02 · [TeleRAG: Efficient Retrieval-Augmented Generation Inference with Lookahead Retrieval](2025-2502.20969-telerag-efficient-retrieval-augmented-generation-inference-with-lookahead-retrieval.md)**  
  実装：[✓](https://github.com/uw-syfi/TeleRAG) ・ リポジトリ内被引用：8  
  RAGの前段生成から次のIVF検索クラスタを予測し、LLM生成とCPU→GPU先読みを重ねつつ外れクラスタをCPU検索で補完して、大規模索引をGPU常駐せず検索待ちを隠す。

- **2025-10 · [MX+: Pushing the Limits of Microscaling Formats for Efficient Large Language Model Serving](2025-2510.14557-mx-pushing-the-limits-of-microscaling-formats-for-efficient-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  しかし4ビットの浮動小数点形式では、活性の一部に現れる極端に大きな値が量子化尺度を押し上げ、他の値がゼロへ丸められることがある。

- **2025-10 · [FlexPipe: Adapting Dynamic LLM Serving Through Inflight Pipeline Refactoring in Fragmented Serverless Clusters](2025-2510.11938-flexpipe-adapting-dynamic-llm-serving-through-inflight-pipeline-refactoring-in-fragmented-serverless-clusters.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  断片化したserverless GPU上でパイプライン 段を実行中に細分化・統合し、KV整合性を保ちながら負荷変動へ追随するFlexPipe。

- **2025-10 · [FairBatching: Fairness-Aware Batch Formation for LLM Inference](2025-2510.14392-fairbatching-fairness-aware-batch-formation-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  FairBatching-vanilla単体の有効要求処理量（有効スループット）改善は、最良の比較方式に対する幾何平均で20.0%である。

- **2025-09 · [Amoeba: Runtime Tensor Parallel Transformation for LLM Inference Services](2025-2509.19729-gyges-cross-instance-parallelism-transformation.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  要求長に応じて稼働中インスタンスをTP1↔TP2↔TP4へ変換し、KVページ配置と重み境界を事前整列して再計算なしで並列度を変えることで、短文時の高処理量と長文対応を両立する方式。

- **2025-07 · [Oneiros: KV Cache Optimization through Parameter Remapping for Multi-tenant LLM Serving](2025-2507.11507-oneiros-parameter-remapping-multitenant-serving.md)**  
  実装：[✓](https://github.com/UT-SysML/Oneiros/) ・ リポジトリ内被引用：7  
  複数LLMを同じGPUで提供すると、KVキャッシュ不足をCPU退避で解決する方法は毎トークンの転送と同期でデコードを止める。Oneirosは不変なモデルパラメータをCPUへ移し、空いたGPUページをKVキャッシュへ転用し、重み読込みをGPU計算に重ねて停滞を抑える。

- **2025-04 · [Taming the Titans: A Survey of Efficient LLM Inference Serving](2025-2504.19720-taming-the-titans-a-survey-of-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、これらを個別の高速化手法として列挙するだけでなく、単一インスタンス・クラスタ・新興用途・補助領域の四層に配置する。

- **2024-11 · [FastSwitch: Optimizing Context Switching Efficiency in Fairness-aware Large Language Model Serving](2024-2411.18424-fastswitch-optimizing-context-switching-efficiency-in-fairness-aware-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  初回トークンまでの時間（time to first トークン; TTFT）や連続するトークン間隔（time between トークン; TBT）について利用者ごとのサービス水準目標（service-level objective; SLO）を満たすには、実行中の要求の優先度を調整し、低優先度の要求を一時停止して高優先度の要求へGPUメモリを譲る必要がある。

- **2025-10 · [TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling](2025-2510.02758-tokenflow-responsive-llm-text-streaming-serving-under-request-burst-via-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  TokenFlowが扱うのは、生成済みトークンを逐次ユーザーへ渡すストリーミング配信である。通常の推論器はできるだけ多くのトークンを生成するが、人が文章を読む速度はモデルの生成速度より遅い場合が多い。既に多くのトークンを生成した利用者の要求をGPU上で走らせ続ける一方、新しい利用者を長く待たせることは、総生成トークン数が高くても体感応答性を悪化させる。

- **2025-07 · [On Evaluating Performance of LLM Inference Serving Systems](2025-2507.09019-on-evaluating-performance-of-llm-inference-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  本論文は、大規模言語モデル（LLM）の推論配信システムにおける性能評価の落とし穴を体系化した方法論研究である。

- **2025-06 · [TD-Pipe: Temporally-Disaggregated Pipeline Parallelism Architecture for High-Throughput LLM Inference](2025-2506.10470-td-pipe-temporally-disaggregated-pipeline-parallelism-architecture-for-h.md)**  
  実装：[✓](https://github.com/MLSysU/TD-Pipe) ・ リポジトリ内被引用：6  
  PCIeのみで接続されたGPUのパイプライン並列推論において、プリフィルとデコードを時間分離し、予測型KVメモリ管理と負荷移送で遊休時間を削減する。

- **2025-05 · [SpecEdge: Scalable Edge-Assisted Serving Framework for Interactive LLMs](2025-2505.17052-specedge-edge-assisted-speculative-serving.md)**  
  実装：[✓](https://github.com/kaist-ina/specedge) ・ リポジトリ内被引用：6  
  消費者GPUをエッジ側ドラフト生成へ使い、先行ドラフトと複数要求の検証パイプラインでWAN遅延を隠しつつ、A100サーバの処理量を平均2.22倍へ高めるエッジ支援投機的配信。

- **2025-05 · [ELIS: Efficient LLM Iterative Scheduling System with Response Length Predictor](2025-2505.09142-elis-efficient-llm-iterative-scheduling-system-with-response-length-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  応答長を50トークンごとに再予測して短い残作業を優先し、LLM servingの先頭待ちを減らすKubernetes/vLLMスケジューラ。

- **2024-12 · [Multi-Bin Batching for Increasing LLM Inference Throughput](2024-2412.04504-multi-bin-batching-for-increasing-llm-inference-throughput.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  しかし固定バッチ方式では、バッチに含まれる要求のうち最も長い生成が終わるまで、そのバッチ全体が実行資源を占有する。2026年改訂版の実測では、単一A100 80GB上のllama.cppでDollyワークロードを処理し、推定長8ビンが固定バッチの273.53生成トークン/秒から684.02生成トークン/秒へ改善する。

- **2025-10 · [Accelerating Diffusion LLM Inference via Local Determinism Propagation](2025-2510.07081-accelerating-diffusion-llm-inference-via-local-determinism-propagation.md)**  
  実装：[✓](https://github.com/friedrichor/LocalLeap) ・ リポジトリ内被引用：5  
  マスクを順に外す標準的な復号では、各反復で最も確信度の高い一位置だけを確定する保守的方式が品質維持のために用いられる。LLaDA-8B-InstructのGSM8K・生成長512では、逐次確定の7.76トークン/秒を53.82トークン/秒へ、反復512回を73回へ削減し、正答率は78.24%から78.54%であった。

- **2025-09 · [Ranking Before Serving: Low-Latency LLM Serving via Pairwise Learning-to-Rank](2025-2510.03243-ranking-before-serving-low-latency-llm-serving-via-pairwise-ranking.md)**  
  実装：[✓](https://github.com/SPEAR-UIC/PARS) ・ リポジトリ内被引用：5  
  PARSの要点は「出力長を正確に当てる」ことではない。SJF型スケジューリングに必要なのは、待機中の要求についてどちらを先に流すべきかという相対順序である。絶対長回帰を捨て、長さ差が十分ある要求対だけから順位を学ぶことで、生成長のノイズを避けながらHOL blockingを減らす。

- **2025-07 · [BucketServe: Bucket-Based Dynamic Batching for Smart and Efficient LLM Inference Serving](2025-2507.17120-bucketserve-dynamic-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  系列長バケットを負荷に応じて分割・統合し、KV容量から安全なバッチ数を動的計算して、パディング・OOM・SLO違反を抑えるLLMサービング方式。

- **2025-03 · [Optimizing LLM Inference Throughput via Memory-aware and SLA-constrained Dynamic Batching](2025-2503.05248-optimizing-llm-inference-throughput-via-memory-aware-and-sla-constrained.md)**  
  実装：[✓](https://github.com/KevinLee1110/dynamic-batching) ・ リポジトリ内被引用：5  
  ただし各要求の入力長・生成長に応じてKVキャッシュが増えるため、バッチを大きくし過ぎるとメモリ不足（OOM）、KV退避、再計算が発生する。飽和要求負荷での実験では、静的バッチ上限に比べて生成処理量が6.5〜28.2%改善した。

- **2024-12 · [METIS: Fast Quality-Aware RAG Systems with Configuration Adaptation](2024-2412.10543-metis-fast-quality-aware-rag-systems-with-configuration-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  検索数を増やすと根拠が集まりやすい反面、入力長が増え、最初のトークン生成までの処理やGPUメモリ占有が大きくなる。METISは、質問ごとに必要な検索件数、文章片の統合方法、中間要約長を変えることと、同時にGPUで処理する要求を選ぶことを、一つの制御器で行う。

- **2025-10 · [BanaServe: Unified KV Cache and Dynamic Module Migration for Balancing Disaggregated LLM Serving in AI Infrastructure](2025-2510.13223-banaserve-dynamic-module-migration.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  分離サービングの固定GPU配分と接頭辞キャッシュ偏在を、層単位の重み移動・注意ヘッド単位のKV移動・CPU/SSD共有KVストアで切り離し、負荷だけを見た再配置とルーティングを可能にする。

- **2025-08 · [Taming the Chaos: Coordinated Autoscaling for Heterogeneous and Disaggregated LLM Inference](2025-2508.19559-heteroscale-coordinated-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  異種GPUとRDMAネットワーク階層を考慮してプリフィル／デコードを配置し、デコードTPSを主信号に両プールを協調増減することで、P/D分離サービングの資源浪費と比率崩れを抑える。

- **2025-08 · [Optimal Scheduling Algorithms for LLM Inference: Theory and Practice](2025-2508.01002-optimal-scheduling-algorithms-for-llm-inference-theory-and-practice.md)**  
  実装：[✓](https://github.com/agrimUT/SLAI) ・ リポジトリ内被引用：4  
  理論部分の資源認識型動的スケジューラ（Resource-Aware Dynamic; RAD）は、最適な行列積タイル配置と入力・復号への動的な演算配分を組み合わせ、同質な推論ノード、確率的到着、十分なGPUメモリなどの仮定下で処理量最適性を証明する。

- **2025-08 · [HFX: Joint Design of Algorithms and Systems for Multi-SLO Serving and Fast Scaling](2025-2508.15919-hfx-joint-design-of-algorithms-and-systems-for-multi-slo-serving-and-fas.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HFX（後続版ではHyperFlexisとも表記）は、異なる遅延目標を持つLLM推論要求が同じクラスタに流入する状況で、既に処理中の要求を遅延目標違反に追い込まず、緊急な新規要求を早く投入し、必要な実行器を迅速に増やすためのシステムである。

- **2025-07 · [ElasticMM: Efficient Multimodal LLMs Serving with Elastic Multimodal Parallelism](2025-2507.10069-elasticmm-elastic-multimodal-parallelism.md)**  
  実装：[✓](https://github.com/hpdps-group/ElasticMM) ・ リポジトリ内被引用：4  
  テキスト要求とマルチモーダル要求を分離し、符号化・事前充填・復号ごとにGPU配分と並列度を動的変更することで、TTFTを最大4.2倍短縮しSLO内スループットを3.2〜4.5倍にする。

- **2025-06 · [PecSched: Preemptive and Efficient Cluster Scheduling for LLM Inference](2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  長入力事前計算を短入力事前計算で選択的に横取りし、事前計算・復号の分離同居と高速系列並列を組み合わせて、短入力の待ち時間と長入力の飢餓を両立して抑える。

- **2025-05 · [Arrow: Adaptive Scheduling Mechanisms for Disaggregated LLM Inference Architecture](2025-2505.11916-arrow-adaptive-scheduling-mechanisms-for-disaggregated-llm-inference-arc.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  LLMサービングでは、入力全体を処理する入力処理と、次トークンを逐次生成する逐次生成とで、計算密度、メモリ帯域要求、許容遅延が異なる。これらを別のGPU群へ分離する構成は相互干渉を減らすが、固定のGPU配分比では、長い入力が集中した時間帯には入力処理が詰まり、長い出力が増えた時間帯には逐次生成が詰まる。

- **2025-04 · [HELIOS: Adaptive Model And Early-Exit Selection for Efficient LLM Inference Serving](2025-2504.10724-helios-adaptive-model-and-early-exit-selection-for-efficient-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  早期終了方式は、Transformerの途中層に置いた出力ヘッドで十分に確信できる次トークンが得られれば、残りの層を実行せずに生成する。4基のNVIDIA A100 40GBを使う評価で、OPT-1.3B単独の早期終了方式に比べバッチ1条件のトークンスループットは平均1.48倍、OPT-6.7B単独比は2.13倍となった。

- **2025-04 · [Compass: SLO-aware Query Planner for Compound AI Serving at Scale](2025-2504.16397-compass-slo-aware-query-planner-for-compound-ai-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  各演算器にはモデル規模やサンプリング率の選択肢があり、端末、近傍エッジ、クラウドのどこで実行するか、どれだけGPUを割り当てるかで、品質・遅延・費用が変わる。原著の評価は5種類の複合AI応用を対象とし、強化した既存計画器と比べて、同じ計画期限でSLOを満たす要求数を2.4〜5.1倍、全要求を処理するための配備費を3.8〜4.5分の1に改善したと報告する。

- **2024-12 · [GreenLLM: Disaggregating Large Language Model Serving on Heterogeneous GPUs for Lower Carbon Emissions](2024-2412.20322-greenllm-disaggregating-large-language-model-serving-on-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  GreenLLMは、新型A100と旧世代T4/V100を組み合わせ、要求の種類と負荷に応じて推論処理の一部を旧GPUへ割り当てる配信基盤である。

- **2024-11 · [Saving GPU Hours in LLM Inference System Development and Online Workloads with Simulation and DBMS-Inspired Cache Replacement Policies](2024-2411.07447-dbms-inspired-cache-replacement-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  単純なコストモデルによる推論シミュレーションから、短い要求を先にプリエンプトするSRFを導出。vLLM/SGLang/Dynamoへ数行で実装し、オンライン負荷で遅延を最大15〜20%改善する。

- **2024-11 · [Ensuring Fair LLM Serving Amid Diverse Applications](2024-2411.15997-ensuring-fair-llm-serving-amid-diverse-applications.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本論文はMicrosoft Copilotの34アプリ、数千利用者、数百万件のLLM要求から利用パターンを調べ、要求回数による制限と一律なトークン受益量に基づく配分が、アプリの負荷特性や多段対話を十分に反映できないことを示した。提案するFairServeは二つの機構を組み合わせる。

- **2025-10 · [When to Reason: Semantic Router for vLLM](2025-2510.08731-when-to-reason-semantic-router-for-vllm.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  問い合わせの処理をGPU上で実行するモデル内部へ直接埋め込むのではなく、HTTP要求の経路に配置できる点が設計上の特徴である。

- **2025-09 · [RServe: Overlapping Encoding and Prefill for Efficient LMM Inference](2025-2509.24381-rserve-overlapping-encoding-and-prefill-for-efficient-lmm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  マルチモーダル入力の符号化が全件終わるまで言語モデルを待機させる依存を解消する。要求内では準備済み埋め込みだけを順にプリフィルへ渡し、要求間では処理可能トークンを複数要求から集めて分割パイプラインの空きを減らす。Qwen2.5-VLの評価で初回トークン遅延最大66%削減、入力トークン処理量最大109%増加を報告する。

- **2025-09 · [FineServe: Precision-Aware KV Slab and Two-Level Scheduling for Heterogeneous Precision LLM Serving](2025-2509.06261-fineserve-precision-aware-kv-slab-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  混合精度モデル間で共有できるKVスラブと、精度別の限界メモリ効率・TTFT期限を使う二段スケジューリングにより、Prism相当方式比でSLO達成率最大2.2倍、生成スループット最大1.8倍を実現する。

- **2025-08 · [Equinox: Holistic Fair Scheduling in Serving Large Language Models](2025-2508.16646-equinox-holistic-fair-scheduling-in-serving-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  利用者QoSとGPU効率を別カウンタで追い、MoPEで未知の実行コストを予測して統一公平性スコア順に要求を組むEquinox。

- **2025-06 · [Efficient Serving of LLM Applications with Probabilistic Demand Modeling](2025-2506.14851-efficient-serving-of-llm-applications-with-probabilistic-demand-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Hermesは、一回のLLM生成要求ではなく、複数の生成、検索、コード実行、画像処理が連鎖するアプリケーション全体の終了時間を最適化する。既存のvLLMの要求単位の先着順や、アプリ単位でも処理量を推定しない先着順では、短いアプリが長いアプリの後ろに並ぶ。推定した分布からGittins指標でアプリの優先度を決め、次のバックエンドの事前準備を行う。

- **2025-05 · [Thinking Short and Right Over Thinking Long: Serving LLM Reasoning Efficiently and Accurately](2025-2505.13326-thinking-short-and-right-over-thinking-long-serving-llm-reasoning-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SARTは、推論分岐を必要数より多く開始し、必要な本数が完成したら残りを停止する冗長サンプリング（redundant sampling with early stopping）と、過程報酬モデル（process reward モデル、PRM）で低品質の分岐を段階的に削る動的枝刈りを組み合わせる。

- **2025-05 · [Scorpio: Serving Right Requests at the Right Time for Heterogeneous SLOs in LLM Inference](2025-2505.23022-scorpio-heterogeneous-slo-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  要求ごとに異なるTTFT/TPOTのSLOを、締切順の並べ替え・達成不能要求の拒否・SLO比例の処理機会配分で共同制御し、高負荷時の有効スループットを最大14.4倍にする。

- **2025-05 · [MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized Layer Swapping and KV Cache Resizing](2025-2506.02006-efficient-and-workload-aware-llm-serving-via-runtime-layer-swapping-and-kv-cache-resizing.md)**  
  実装：[✓](https://github.com/ds2-lab/MorphServe) ・ リポジトリ内被引用：3  
  負荷ピーク時だけ低影響層を低ビット版へ非同期交換し、空いたGPUメモリをKVキャッシュへ振り替えることで、平均SLO違反を92.45%削減しP95初回トークン遅延を2.2〜3.9倍改善する。

- **2025-05 · [MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models](2025-2505.22101-memos-an-operating-system-for-memory-augmented-generation-mag-in-large-l.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  2025年5月の短縮版は設計と処理経路を詳述するが、推論速度、GPUメモリ削減、検索正答率、実行スループットの定量比較表を提示しないため、性能改善は未実証と区別する。

- **2025-04 · [SeaLLM: Service-Aware and Latency-Optimized Resource Sharing for Large Language Model Inference](2025-2504.15720-seallm-service-aware-and-latency-optimized-resource-sharing-for-large-la.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SeaLLMは、GPUクラスタ上で複数のLLMサービスを同居させる際、正規化応答遅延とSLO達成率を優先して配置・要求順序・KVキャッシュを共同設計するシステムである。4ノード・32枚のNVIDIA A800 80GBによる実機評価で、MuxServeに対し正規化遅延を最大13.60倍、99パーセンタイル遅延を最大18.69倍改善する。

- **2025-03 · [PipeBoost: Resilient Pipelined Architecture for Fast Serverless LLM Scaling](2025-2503.17707-pipeboost-resilient-pipelined-serverless-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  同一基盤モデルのサーバーレス立上げをGPU間のパイプライン読込・早期分散推論・障害復旧で高速化し、既存低遅延基盤比で推論遅延を31〜49.8%削減する。

- **2025-02 · [OmniRouter: Budget and Performance Controllable Multi-LLM Routing](2025-2502.20576-omnirouter-budget-and-performance-controllable-multi-llm-routing.md)**  
  実装：[✓](https://github.com/dongyuanjushi/OmniRouter) ・ リポジトリ内被引用：3  
  評価では、MMLU、GPQA-Diamond、Math-500、GSM8Kの合計2,698問（本文では約2.7千問）を10モデルに割り当て、OmniRouterが正答率75.19%、一問当たりの金銭費用0.0515ドルを報告した。

- **2025-01 · [HyGen: Efficient LLM Serving via Elastic Online-Offline Request Co-location](2025-2501.14808-hygen-efficient-llm-serving-via-elastic-online-offline-request-co-locati.md)**  
  実装：[✓](https://github.com/UIUC-MLSys/HyGen) ・ リポジトリ内被引用：3  
  本研究は、オンライン要求を先にバッチへ配置し、そのバッチが消費しない遅延・トークン・KVキャッシュメモリの予算内でオフライン要求を追加する二段階スケジューラを設計した。原著の主要実機評価では、純オンラインのSarathi比で総処理量最大3.87倍、SLOを考慮してオフライン到着率を制御するHyGen比でオフライン処理量最大5.84倍を報告する。

- **2025-09 · [Cannikin: No Lagger of SLO in Concurrent Multiple LoRA LLM Serving](2020-fa2b92104549-cannikin-no-lagger-of-slo-in-concurrent-multiple-lora-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低ランク適応（Low-Rank Adaptation; LoRA）では大きな基盤モデルを共有し、サービスごとに小さなアダプタだけを切り替えられる。実トレース評価では、各LoRAサービスのSLO達成率を90%超に維持したまま、既存multi-LoRAサービング基盤に対して最大3.6倍高い要求到着率、または2.8倍大きいバースト性を処理できると報告する。

- **2025-07 · [StreamVLN: Streaming Vision-and-Language Navigation via SlowFast Context Modeling](2025-2507.05240-streamvln-streaming-vision-and-language-navigation-via-slowfast-context-.md)**  
  実装：[✓](https://streamvln.github.io/) ・ リポジトリ内被引用：2  
  StreamVLNは、視覚・言語・行動を連続して扱うロボット誘導システムにおいて、動画言語モデルの文脈長と鍵・値キャッシュ（KVキャッシュ）が際限なく増える問題を解決しようとする。

- **2025-07 · [LeMix: Unified Scheduling for LLM Training and Inference on Multi-GPU Systems](2025-2507.21276-lemix-unified-training-inference-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LeMixは継続学習と推論を同一GPU群へ共置し、事前予測した空き時間・応答遅延・メモリ量でタスク配置と実行順を調整する。固定分離比でスループット最大3.53倍、SLO達成率最大2.12倍を報告。

- **2025-05 · [ServerlessLoRA: Minimizing Latency and Cost in Serverless Inference for LoRA-Based LLMs](2025-2505.14468-serverlesslora-latency-cost-lora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LoRAサーバレス推論で基盤重みだけを独立関数間でゼロコピー共有し、到着予測に基づく事前読み込み、SLO適応バッチ、動的退避を組み合わせ、コールドスタートとGPU重複保持を同時に削減する。

- **2025-03 · [AccelGen: Heterogeneous SLO-Guaranteed High-Throughput LLM Inference Serving for Diverse Applications](2025-2503.13737-accelgen-heterogeneous-slo-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SLOから各反復のトークン予算を決める動的分割、残り猶予順の優先付け、GPU計算とKVキャッシュを同時に詰める処理群選択を組み合わせ、長短入力混在で有効処理量とSLO達成率を改善する。

- **2025-10 · [Preserving LLM Capabilities through Calibration Data Curation: From Analysis to Optimization](2025-2510.10618-preserving-llm-capabilities-through-calibration-data-curation-from-analy.md)**  
  実装：[✓](https://github.com/BokwaiHo/COLA) ・ リポジトリ内被引用：1  
  量子化・剪定はLLMの重み容量や演算量を減らすが、圧縮前の校正データの選び方で、残る能力の種類が変わる。LLaMA3-8B-InstructのSparseGPT 50%剪定では、WikiTextのランダム校正による常識推論41.85%に対しCOLAは44.23%を報告する。

- **2025-10 · [From Tokens to Layers: Redefining Stall-Free Scheduling for MoE Serving with Layered Prefill](2025-2510.08055-layered-prefill-stall-free-moe-serving.md)**  
  実装：[✓](https://github.com/scale-snu/layered-prefill) ・ リポジトリ内被引用：1  
  長い入力をトークンではなくモデル層群へ分け、各反復で一群だけに入力処理を進めながら全群のデコードを続けることで、MoE重みの再読込を減らしTTFT・電力を改善する。

- **2025-09 · [A Predictive and Synergistic Two-Layer Scheduling Framework for LLM Serving](2025-2509.23384-synergysched-predictive-two-layer-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  オンライン性能モデルをエンジン内SLO対応処理群形成とクラスタ先読み配送の共通信号にし、二層間の情報断絶を閉じて動的・異種LLM配信の遅延とSLO達成率を改善する。

- **2025-08 · [Semantic Caching for Low-Cost LLM Serving: From Offline Learning to Online Adaptation](2025-2508.07675-semantic-caching-for-low-cost-llm-serving-from-offline-learning-to-onlin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMサービングでは、同じ質問への回答を保存する通常の応答キャッシュによって再計算を減らせる。原著の評価は合成データ上の費用・後悔・切替回数が中心であり、実際の生成品質やGPU推論速度の実測改善と混同してはならない。

- **2025-07 · [A Thermal-aware Workload Scheduler for High-performance LLM Inference in Cooling-regulated Datacenters](2025-a06f210bac8b-a-thermal-aware-workload-scheduler-for-high-performance-llm-inference-in.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、データセンターの冷却設定温度を高めることで冷却電力を節約しようとすると、GPUの熱保護動作（thermal throttling）が逆に推論処理量を低下させる、という運用上の競合を扱う。従来の推論スケジューラはGPU利用率とトークン処理量を最適化しても、この熱的な履歴状態を明示的には考慮しない。

- **2025-06 · [PCDVQ: Enhancing Vector Quantization for Large Language Models via Polar Coordinate Decoupling](2025-2506.05432-pcdvq-enhancing-vector-quantization-for-large-language-models-via-polar-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PCDVQは、大規模言語モデルの重みを2ビット前後まで圧縮する重み専用のベクトル量子化を扱う。著者らの観測では、LLaMA-2-7Bの重みベクトルを方向と長さへ分けて片方ずつ量子化した際、方向の量子化によるゼロショット課題の正答率低下は46.5%、長さの量子化では2.3%だった。

- **2025-05 · [QoS-Efficient Serving of Multiple Mixture-of-Expert LLMs Using Partial Runtime Reconfiguration](2025-2505.06481-qos-efficient-serving-of-multiple-mixture-of-expert-llms-using-partial-r.md)**  
  実装：[✓](https://github.com/hamid-74/Multi-MoE) ・ リポジトリ内被引用：1  
  混合専門家モデル（Mixture-of-Experts; MoE）は、入力ごとに少数の専門家だけを選択して計算するため、全パラメータ数が大きくても演算量を抑えられる。

- **2025-04 · [NoWag: A Unified Framework for Shape Preserving Compression of Large Language Models](2025-2504.14569-nowag-a-unified-framework-for-shape-preserving-compression-of-large-lang.md)**  
  実装：[✓](https://github.com/LawrenceRLiu/NoWag) ・ リポジトリ内被引用：1  
  NoWag（Normalized 重み and 活性値 Guided Compression）は、学習済みLLMの重み行列を入出力形状を保ったまま低ビット量子化または疎化するための共通枠組みである。NoWag-Pも50%非構造剪定ではWandaより低いperplexityを示す。

- **2025-02 · [Hybrid Offline-online Scheduling Method for Large Language Model Inference Optimization](2025-2502.15763-hybrid-offline-online-scheduling-method-for-large-language-model-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLaMA-65B、GSM8Kの1319要求、8基のAscend計算ユニットで、ベースラインの総完了時間201.00秒・利用率80.2%を、全方式併用で190.58秒・89.06%へ改善した（原著§V、図6–9）。

- **2025-01 · [iServe: An Intent-based Serving System for LLMs](2025-2501.13111-iserve-intent-based-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  軽量なモデル・フィンガープリントで多数の並列化・圧縮構成の遅延とメモリを推定し、利用者の遅延・費用意図とGPU空き状況に合わせて配備構成を自動選択することで、遅延77.62%削減、SLO達成3.03〜7.09倍、GPUスループット4.72倍を示す。

- **2025-10 · [Loquetier: A Virtualized Multi-LoRA Framework for Unified LLM Fine-tuning and Serving](2025-2511.00101-loquetier-virtualized-multilora-serving.md)**  
  実装：[✓](https://github.com/NJUDeepEngine/Loquetier) ・ リポジトリ内被引用：0  
  共有基盤LLM上でLoRAごとの仮想モデルを隔離し、SMLMカーネルで微調整・評価・プリフィル・デコードを同一実行系へ統合する多数LoRA基盤。推論でFlexLLM比最大3.0倍、統一負荷でPEFT比46.4倍のSLO達成率を報告する。

- **2025-10 · [Kelle: Co-design KV Caching and eDRAM for Efficient LLM Serving in Edge Computing](2025-2510.16040-kelle-co-design-kv-caching-and-edram-for-efficient-llm-serving-in-edge-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Kelleは、端末上で大規模言語モデル（LLM）を推論する際、鍵・値の中間表現（KVキャッシュ）を面積効率の高い組込みDRAM（eDRAM）へ置き、記憶内容の削除・再計算・リフレッシュ頻度・演算順序まで一体で最適化する方式である。原著の合成・モデル評価では、元のSRAM構成に対し平均3.94倍の遅延改善と4.46倍のエネルギー効率改善を報告する。

- **2025-10 · [From Principles to Practice: A Systematic Study of LLM Serving on Multi-core NPUs](2025-2510.05632-systematic-study-multicore-npu-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチコアNPU向け多層シミュレータで、テンソル分割・コア配置・SRAM/HBM管理・プリフィルとデコードの分離/融合をQwen3各サイズで比較し、入力長・通信競合・負荷構成ごとに有利な設計を明らかにする研究。

- **2025-10 · [Best of mini-N in-loop Sampling: A Contextual Quality Reward Model for Reliable and Efficient Best-of-N Sampling](2025-2510.04087-best-of-mini-n-in-loop-sampling-a-contextual-quality-reward-model-for-re.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Best-of-N（BoN）は、同じプロンプトに対してN個の回答候補を生成し、報酬モデルで最も高いものを採用する。多数の候補を生成すれば高品質な回答に出会いやすくなるが、生成費用が増え、さらに候補がすべて不適切でも相対順位の1位を出力してしまう。安全性と速度を同時に無償で改善する手法ではなく、明確な閾値・品質交換関係を持つ。

- **2025-10 · [A Survey on Collaborating Small and Large Language Models for Performance, Cost-effectiveness, Cloud-edge Privacy, and Trustworthiness](2025-2510.13890-a-survey-on-collaborating-small-and-large-language-models-for-performanc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両者を単純に比較するのではなく、どの処理をどちらに割り当て、いつ結果を交換するかを設計対象とするのが協調方式である。

- **2025-09 · [SplitQuant: Resource-Efficient LLM Offline Serving on Heterogeneous GPUs via Phase-Aware Model Partition and Adaptive Quantization](2025-a2e6bfa9ec8a-splitquant-resource-efficient-llm-offline-serving-on-heterogeneous-gpus-.md)**  
  実装：[✓](https://github.com/tonyzhao-jt/LLM-PQ) ・ リポジトリ内被引用：0  
  SplitQuantは、計算能力・メモリ容量・対応する低精度演算が異なるGPUを組み合わせたクラスタで、LLMのオフラインバッチ推論を効率化するシステムである。10種類のクラスタを用いた評価では最大2.34倍、平均1.61倍のスループット向上を報告する。

- **2025-09 · [MACE: A Hybrid LLM Serving System with Colocated SLO-aware Continuous Retraining Alignment](2025-2510.03283-mace-a-hybrid-llm-serving-system-with-colocated-slo-aware-continuous-ret.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一定時間ごとに再学習する方式はモデル更新が遅れ、更新を最優先する方式は利用者への応答を待たせる。A6000 AdaではAdaInf比で10%再学習率の推論スループット最大1.46倍、入力事前計算遅延最大63%削減を報告する。

- **2025-09 · [Intra-request branch orchestration for efficient LLM reasoning](2025-2509.24957-intra-request-branch-orchestration-for-efficient-llm-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、推論時に複数のChain-of-Thought（CoT）枝を生成して多数決を取る自己整合性（SC）のトークン費用とリクエスト完了遅延を同時に削減するDUCHESSを提案する。

- **2025-08 · [Rethinking Caching for LLM Serving Systems: Beyond Traditional Heuristics](2025-2508.18736-rethinking-caching-for-llm-serving-systems-beyond-traditional-heuristics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  さらに高負荷でも同じ類似度しきい値を維持すると、モデル本体へ送られる要求が多すぎて遅延目標を守れない場合がある。SISO（Similar Input? Similar Output!）は、意味クラスタの重心をキャッシュする方式、意味的な局所性に基づく置換、要求負荷に応じた検索しきい値の動的制御を組み合わせる。

- **2025-08 · [Pruning Long Chain-of-Thought of Large Reasoning Models via Small-Scale Preference Optimization](2025-2508.10164-pruning-long-chain-of-thought-of-large-reasoning-models-via-small-scale-.md)**  
  実装：[✓](https://github.com/SleepyWithoutCoffee/Small_Scale) ・ リポジトリ内被引用：0  
  大規模推論モデル（LRM）は、複雑な数学問題や知識問題に答えるために長いChain-of-Thought（CoT）を生成する。大規模なオンライン強化学習で長さ報酬を最適化する方式は、学習用の大量生成と複雑な実行基盤を要する。

- **2025-07 · [Towards Resource-Efficient Serverless LLM Inference with SLINFER](2025-2507.00507-towards-resource-efficient-serverless-llm-inference-with-slinfer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SLINFERは、個別モデルへの要求が少なく断続的に発生する私設大規模言語モデル（LLM）サービスを対象に、CPUとGPUの両方を推論実行先として扱い、同一ノードで複数モデルを弾力的に共有するシステムである。論文の事前調査では、ServerlessLLMで各インスタンスへGPU全体を割り当てたときの平均GPUメモリ利用率が23%にとどまる条件が示される。

- **2025-07 · [MoLink: Distributed and Efficient Serving Framework for Large Models](2025-2507.05043-molink-distributed-and-efficient-serving-framework-for-large-models.md)**  
  実装：[✓](https://github.com/oldcpple/MoLink) ・ リポジトリ内被引用：0  
  MoLinkは、専用の高速相互接続を持たないGPUを複数台集め、大きな言語モデルをパイプライン並列で提供するシステムである。100 Mbps・往復遅延10 ms・毎秒1要求のとき、MoLinkは196.142 トークン/sで、Petals 45.343、vLLM 135.86を上回る。

- **2025-06 · [Optimizing MoE Routers: Design, Implementation, and Evaluation in Transformer Models](2025-2506.16419-optimizing-moe-routers-design-implementation-and-evaluation-in-transform.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本稿は新しい分散MoEサービング基盤を提案するのではなく、ルーティングの設計選択がパラメータ数、トークン処理遅延、選択分布の集中度、既存モデルへの組込み難度にどう効くかを実装比較する研究である。

- **2025-06 · [On-the-Fly Adaptive Distillation of Transformer to Dual-State Linear Attention for Long-Context LLM Serving](2025-2506.09316-on-the-fly-adaptive-distillation-of-transformer-to-dual-state-linear-att.md)**  
  実装：[✓](https://github.com/utnslab/DSLA-Serve) ・ リポジトリ内被引用：0  
  DSLA-Serveは、大規模言語モデル（LLM）の長文推論で増大する自己注意（self-注意機構）の計算量とKVキャッシュ容量を、自己注意層の一部を線形注意へ置き換えることで削減する方式である。報告された代表値は、元のLlama2-7Bに対して約2.29倍、ハイブリッドモデルZamba-7Bに対して約3.0倍の推論高速化である。

- **2025-06 · [Diagonal Batching Unlocks Parallelism in Recurrent Memory Transformers for Long Contexts](2025-2506.05229-diagonal-batching-unlocks-parallelism-in-recurrent-memory-transformers-f.md)**  
  実装：[✓](https://github.com/svtdanny/diagonal-batching) ・ リポジトリ内被引用：0  
  Recurrent メモリ Transformer（RMT）は入力を短いセグメントに分け、固定サイズのメモリ状態を次のセグメントへ引き継ぐことで、文脈全体を一度に注意へ載せずに処理できる。この手法は重みを削る、近似注意へ変える、再帰状態を近似する方法ではなく、既存モデルの計算順序を依存関係の許す範囲で入れ替えるランタイムスケジューリングである。

- **2025-06 · [Adaptive Request Scheduling for CodeLLM Serving with SLA Guarantees](2025-2506.19677-adaptive-request-scheduling-for-codellm-serving-with-sla-guarantees.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SABERは、各要求の期限と現在実行中の要求を見ながら、新しい要求をバッチへ入れてよいかを予測するSLA-awareスケジューラである。

- **2025-05 · [Recursive Offloading for LLM Serving in Multi-tier Networks](2025-2505.16502-recursive-offloading-for-llm-serving-in-multi-tier-networks.md)**  
  実装：[✓](https://github.com/wuzhiyuan2000/RecServe) ・ リポジトリ内被引用：0  
  端末→エッジ→クラウドを信頼度で再帰的に上げ、履歴分位点から閾値を自動適応してCloudServe比50%以上の通信削減を狙う多層LLMサービング。

- **2025-05 · [How Many Parameters Does Your Task Really Need? Task Specific Pruning with LLM-Sieve](2025-2505.18350-how-many-parameters-does-your-task-really-need-task-specific-pruning-wit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、用途と関係の薄い行列を強く圧縮できれば、同じ品質許容差のもとで大幅な容量削減が期待できる。70Bの感情分類では品質差1%以内で55%、5%以内で75%のパラメータを削減できたと報告する。

- **2025-05 · [Harmonia: End-to-End RAG Serving Optimization](2025-2505.07833-harmonia-end-to-end-rag-serving-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Harmoniaは開発者のPythonワークフローからコンポーネント依存関係を抽出し、CPU/GPUとメモリを配置して、実行中の負荷や分岐頻度に応じて再配分する。

- **2025-03 · [Alchemist: Towards the Design of Efficient Online Continual Learning System](2025-2503.01066-alchemist-towards-the-design-of-efficient-online-continual-learning-syst.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Alchemistは、LLMのサービングとオンライン継続学習を別々のGPUやプロセスで実行すると、サービングのプリフィルで既に計算した中間活性を学習側が再計算してしまうことに着目したシステムである。著者らの分析では、この重複した順伝播計算がオンライン学習時間の30～42%を占める。

- **2025-01 · [Mixed-Precision Graph Neural Quantization for Low Bit Large Language Models](2025-2501.18154-mixed-precision-graph-neural-quantization-for-low-bit-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、学習済み大規模言語モデルの重みを平均2ビット前後へ事後量子化する際、すべての重み列に同じビット幅を割り当てると重要な列の誤差が大きくなり、困惑度が急激に悪化する問題を扱う。原著の効率評価はRTX 4090上の量子化前処理時間であり、生成トークン/sやエンドツーエンド推論時間の改善は示していない。

- **2024-11 · [EconoServe: Maximizing Multi-Resource Utilization with SLO Guarantees in LLM Serving](2024-2411.06364-econoserve-maximizing-multi-resource-utilization-with-slo-guarantees-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  EconoServeはLLMサービングでGPUの演算能力とKVキャッシュ（KVC）容量を同時に活用するための、プリフィルとgenerationの責任分離・時間同期バッチ・KVCの時間的再利用を組み合わせたスケジューラである。

### 3年前（2023-11〜2024-10）

- **2023-12 · [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)**  
  実装：[✓](https://github.com/sgl-project/sglang) ・ リポジトリ内被引用：660  
  複数のLLM呼び出しや条件分岐をランタイムが1つのプログラムとして理解し、共有接頭辞のKV再利用・並列実行・構造化出力生成をまとめて効率化する推論システム。

- **2024-07 · [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)**  
  実装：[✓](https://github.com/LLMServe/DistServe) ・ リポジトリ内被引用：609  
  DistServeは、二段階を異なるGPU群へ分離し、事前入力処理側と逐次復号側の装置配分、モデル並列化、要求の束ね方を独立に決める。OSDI 2024の論文は、四ノード・計32台のA100 80GBを用い、OPT-13B、OPT-66B、OPT-175Bと三種のアプリケーションを評価した。

- **2023-11 · [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)**  
  実装：[✓](https://github.com/Mutinifni/splitwise-sim) ・ リポジトリ内被引用：508  
  プリフィルとデコードを別の計算機群へ分け、それぞれに向くGPU世代・電力設定・台数を使い分けて、クラスタ全体のスループット・コスト・消費電力を改善するサービング設計。

- **2024-03 · [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)**  
  実装：[✓](https://github.com/microsoft/sarathi-serve) ・ リポジトリ内被引用：473  
  本論文の重要な点は、単純に事前入力を分割するだけでなく、デコードと事前入力を同じ反復へ混ぜるスケジューリング規則、反復あたりの総トークン予算、パイプライン並列化での仕事量の均等化を一体で設計したことである。

- **2024-06 · [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)**  
  実装：[✓](https://github.com/AlibabaPAI/llumnix) ・ リポジトリ内被引用：184  
  Llumnixは、複数のGPU実行単位で大規模言語モデルを提供するとき、要求を最初に振り分けて終わりにせず、生成途中でも別の実行単位へ移動するスケジューラである。

- **2024-03 · [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：171  
  本研究は、対話型の大規模言語モデル（LLM）において、利用者が同じ会話を再開するたびに過去の文章を読み直して注意機構の鍵・値（KV）を作り直す無駄を、会話状態の耐久保存で削減する。原著が調べたShareGPT会話では73%が複数ターンで、長く続いた会話の新規ターンでは過去の内容に由来する再計算が事前計算時間の最大99%に達する。

- **2024-01 · [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](2024-2401.11181-tetriinfer.md)**  
  実装：✓ ・ リポジトリ内被引用：120  
  事前充填を固定長チャンク化して復号インスタンスから分離し、生成長予測付き二段階配置で混合LLM要求の干渉を抑える配信システム。

- **2024-01 · [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)**  
  実装：[✓](https://github.com/ServerlessLLM/ServerlessLLM) ・ リポジトリ内被引用：113  
  要求到着時にモデルをGPUへ読み込むサーバーレス環境で、チェックポイントをGPU近くのSSD / DRAMへキャッシュし、高速読み込み器とモデル所在地を考慮した要求配置、生成途中要求の移動を組み合わせてモデル起動待ちを短縮するシステム。

- **2024-01 · [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed-MII) ・ リポジトリ内被引用：105  
  長いプリフィルを小さく分割し、短いプロンプト・プリフィル 分割片・デコード トークンを毎回ほぼ同じ総トークン数になるよう混ぜることで、長いプリフィルがデコードを止める時間を抑えつつGPUを効率よく使うLLM 提供処理 システム。

- **2024-08 · [DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency](2024-2408.00741-dynamollm.md)**  
  実装：✓ ・ リポジトリ内被引用：104  
  要求種別ごとのプールと階層制御でGPU数・並列度・周波数を動的最適化し、SLO維持下で推論クラスタのエネルギーを約52%削減する。

- **2023-12 · [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)**  
  実装：[✓](https://github.com/Ying1123/VTC-artifact) ・ リポジトリ内被引用：93  
  仮想 トークン Counter（VTC）は、要求数ではなくクライアントごとに実際に処理した入力・出力トークンをサービス量として数え、累積サービス量が少ないクライアントから新しい要求を実行バッチへ入れる。空きGPUを意図的に遊ばせず、公平性と高い利用率を両立することを狙う。

- **2024-05 · [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)**  
  実装：[✓](https://github.com/microsoft/ParrotServe) ・ リポジトリ内被引用：92  
  複数の言語モデル呼出しから成るアプリケーションの入力・出力の関係を、意味変数という抽象化で推論提供側へ公開する。これにより要求間の依存関係、同一接頭部の再利用、アプリケーション全体の完了時間を考慮した要求配置を可能にする。単一要求の速度ではなく、複数要求を組み合わせた作業の完了時間を最適化する研究である。

- **2023-11 · [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)**  
  実装：[✓](https://github.com/Hsword/SpotServe) ・ リポジトリ内被引用：88  
  一覧用要約：スポットGPUの回収・獲得に合わせて並列構成を再最適化し、既存の重みとKVキャッシュを最大限再利用する配置・移行と、トークン単位の状態付き途中再開によって分散LLMの長尾遅延と運用費を抑える。

- **2024-08 · [NanoFlow: Towards Optimal Large Language Model Serving Throughput](2024-2408.12757-nanoflow.md)**  
  実装：[✓](https://github.com/efeslab/Nanoflow) ・ リポジトリ内被引用：87  
  異種GPU資源を使う演算をナノバッチ化して同一装置内で重畳し、自動探索で高スループットな推論パイプラインを構成する。

- **2024-06 · [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：79  
  プリフィルとデコードを別実行単位へ分ける推論提供で、GPU / CPU上のKVキャッシュを実行単位横断で検索・共有・転送できる共通メモリプールを作り、過去接頭部の再利用と処理段階間KV移動を同じ仕組みで扱うシステム。

- **2024-04 · [LoongServe: Efficiently Serving Long-Context Large Language Models with Elastic Sequence Parallelism](2024-2404.09526-loongserve-efficiently-serving-long-context-large-language-models-with-e.md)**  
  実装：[✓](https://github.com/LoongServe/LoongServe) ・ リポジトリ内被引用：77  
  従来の固定テンソル並列は事前充填に必要な多数のGPUを復号中にも占有し、逆に固定の事前充填・復号分離は各GPU群の遊休容量を相互利用できない。著者のSOSP 2024論文では、8基のNVIDIA A800を用いた長文脈モデルの評価で、最大処理率がチャンク化事前充填方式比で最大3.85倍、事前充填・復号分離方式比で最大5.81倍となった。

- **2024-08 · [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)**  
  実装：[✓](https://github.com/hao-ai-lab/vllm-ltr) ・ リポジトリ内被引用：75  
  正確な生成長を当てる代わりに「どの要求が相対的に短いか」を学習し、その順位で連続バッチ処理を並べ替える。OPT-125M級の補助予測器、ListMLE、要求飢餓を防ぐ優先度昇格を組み合わせ、先着順より最短ジョブ優先に近い配信を実現する。

- **2024-05 · [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：75  
  同じプレフィックスのKVをすでに持つGPUへリクエストを送ればプリフィルを省ける一方、そのGPUだけ混むことがあるため、KV再利用で節約できる計算時間とGPUの混雑による待ち時間を比較してリクエストの送り先を決めるdistributed サービング スケジューラ。

- **2024-04 · [A Survey on Efficient Inference for Large Language Models](2024-2404.14294-a-survey-on-efficient-inference-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：70  
  根本原因を巨大なモデルサイズ、系列長に対して二乗に増える自己注意、逐次的な自己回帰復号へ分け、それぞれが計算量、メモリアクセス量、メモリ容量を通じて遅延、スループット、ストレージ、energyへ波及すると整理する。対策taxonomyはデータ層、モデル層、システム層の3階層である。

- **2024-04 · [Efficient Interactive LLM Serving with Proxy Model-based Sequence Length Prediction](2024-2404.08509-ssjf.md)**  
  実装：[✓](https://github.com/James-QiuHaoran/LLM-serving-with-proxy-models) ・ リポジトリ内被引用：60  
  SSJFはBERT-base代理モデルでLLMの出力長を予測して短い要求を先に処理し、FCFS比で平均完了時間を30.5〜39.6%削減する。

- **2024-01 · [Infinite-LLM: Efficient LLM Service for Long Context with DistAttention and Distributed KVCache](2024-2401.02669-infinite-llm-distattention-distributed-kvcache.md)**  
  実装：✓ ・ リポジトリ内被引用：60  
  注意計算とKVを系列方向に分散し、クラスタ全体のGPUメモリを共有して最大200万トークンを処理し、提供スループットを1.35〜3.4倍改善する。

- **2023-12 · [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：59  
  Pensieveは、会話型の大規模言語モデルを複数往復にわたって提供するとき、前回までの履歴を毎回最初から入力処理する重複計算を減らす状態保持型の推論提供システムである。

- **2024-04 · [RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation](2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：55  
  RAGCacheは、検索拡張生成（Retrieval-Augmented Generation; RAG）で同じ知識文書が何度も検索されることに着目し、その文書を言語モデルが処理したときの鍵・値キャッシュ（KVキャッシュ）を複数要求で再利用する推論提供システムである。

- **2024-02 · [INFERCEPT: Efficient Intercept Support for Augmented Large Language Model Inference](2024-2402.01869-infercept-intercept-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：54  
  外部ツールや人間応答を待つ間に生成が中断される拡張LLMで、KVキャッシュをGPUに保持する、CPUへ退避する、破棄して再計算するという三つの選択肢を、GPUメモリの時間積で表した浪費量を基準に要求ごとに切り替える推論基盤。

- **2024-07 · [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)**  
  実装：[✓](https://github.com/QLM-project/QLM) ・ リポジトリ内被引用：47  
  QLMは、対話型の低遅延要求と、数分から数時間待てる一括処理要求を、複数の言語モデルが稼働するGPU群で混在させるための待ち行列管理システムである。ShareGPTの入出力長分布を使った実験では、到着率や比較方式によって期限達成率が40～90%改善し、単一モデルでは要求処理能力が約20%、複数モデルでは最大数倍改善したと報告する。

- **2023-12 · [Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems](2023-2312.15234-towards-efficient-generative-large-language-model-serving-a-survey-from-.md)**  
  実装：✓ ・ リポジトリ内被引用：43  
  本論文はこの問題を機械学習システム（MLSys）の観点から整理し、アルゴリズム側のモデル圧縮・効率的復号と、システム側のメモリ管理・バッチ化・並列化・スケジューリングを同じサービング設計空間に置く。

- **2024-06 · [TurboSpec: Closed-loop Speculation Control System for Optimizing LLM Serving Goodput](2024-2406.14066-turbospec-closed-loop-speculation-control-system-for-optimizing-llm-serv.md)**  
  実装：✓ ・ リポジトリ内被引用：38  
  TurboSpecは、大規模言語モデル（LLM）の複数要求をまとめる連続バッチ処理と、単一要求内で複数候補を先読みする投機的復号（投機的復号）を、現在の負荷に応じて切り替える制御システムである。

- **2024-04 · [MuxServe: Flexible Spatial-Temporal Multiplexing for Multiple LLM Serving](2024-2404.02015-muxserve-flexible-spatial-temporal-multiplexing-for-multiple-llm-serving.md)**  
  実装：[✓](https://github.com/hao-ai-lab/MuxServe) ・ リポジトリ内被引用：38  
  LLM人気度を考慮した配置と事前充填・復号の動的共配置、共有KVキャッシュ管理を組み合わせ、複数LLM配信のGPU計算・メモリ利用率を同時に高める。

- **2024-04 · [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：38  
  提案は、理想的なトークン消費時系列と実際の消費時系列の差から体感品質（Quality of Experience、QoE）を定義し、各要求に今GPU時間を割り当てた場合のQoE改善量を予測してトークン単位で実行要求を入れ替えるもの。

- **2024-06 · [Helix: Distributed Serving of Large Language Models via Max-Flow on Heterogeneous GPUs](2024-2406.01566-helix-maxflow-heterogeneous-gpu-serving.md)**  
  実装：[✓](https://github.com/Thesys-lab/Helix-ASPLOS25) ・ リポジトリ内被引用：37  
  異種GPUとネットワークを容量付き有向グラフへ写像し、最大流を目的に層配置をMILPで決め、最大流比率に沿って要求ごとの経路を選ぶことで、固定パイプラインの遊休GPUと通信混雑を減らすLLMサービング方式。

- **2024-04 · [Mélange: Cost Efficient Large Language Model Serving by Exploiting GPU Heterogeneity](2024-2404.14527-m-lange-cost-efficient-large-language-model-serving-by-exploiting-gpu-he.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  本研究が最適化するのは、同じGPUでモデルを何倍速く動かせるかではなく、所定の要求量と遅延目標を満たすために、どのGPUを何台借りるかである。大規模言語モデル（LLM）のオンライン配信では、安価なGPUを多数用意する構成と高性能GPUを少数用意する構成のどちらが得かは一意に決まらない。さらに要求到着率が小さいと高性能GPUを借りても空き時間が多い。

- **2024-08 · [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  P/D-Serveは、事前充填と復号を別インスタンス群へ分け、シナリオごとにP/D比を調整し、混雑ノードを待たず要求を再送し、KV転送をまとめることで数万NPUクラスタの待ち行列と通信固定費を減らす商用基盤。

- **2024-10 · [Don't Stop Me Now: Embedding Based Scheduling for LLMs](2024-2410.01035-embedding-based-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  TRAILはLLM内部層埋め込みで残り出力長を逐次予測し、KVキャッシュ増加前だけプリエンプトする制限付きSPRPTでvLLMの待ち時間を削減する。

- **2024-09 · [No Request Left Behind: Tackling Heterogeneity in Long-Context LLM Inference with Medha](2024-2409.17264-no-request-left-behind-tackling-heterogeneity-in-long-context-llm-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  これはオペレーティングシステムでいう隊列詰まり（convoy effect）に相当し、GPUが高い総計算量を処理していても利用者の初回応答待ち時間が極端に悪化する。非割込みの長文推論配信基盤と比べて、ある混合負荷ではスループット5.7倍、初回トークン遅延の中央値30分の1、上位側の遅延174分の1という大きな差を報告する。

- **2024-07 · [LLM Inference Serving: Survey of Recent Advances and Opportunities](2024-2407.12391-llm-inference-serving-survey-of-recent-advances-and-opportunities.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  本論文は、大規模言語モデル（Large Language モデル、LLM）の推論サービスを効率化するシステム研究を整理した総説である。

- **2024-03 · [Towards Greener LLMs: Bringing Energy-Efficiency to the Forefront of LLM Inference](2024-2403.20306-towards-greener-llms-bringing-energy-efficiency-to-the-forefront-of-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  最も速い設定を常用すると、利用者の遅延制約に余裕がある時間帯でも電力を浪費する可能性がある。新しいGPUカーネルや省電力推論アルゴリズムを提案する論文ではなく、既存基盤の運用設定が作る性能・エネルギーの交換条件を定量化する研究である。

- **2024-03 · [DéjàVu：KVキャッシュ・ストリーミングによる高速・耐障害LLM配信](2024-2403.01876-dejavu-kv-cache-streaming-for-fast-fault-tolerant-generative-llm-serving.md)**  
  実装：[✓](https://github.com/msr-fiddle/dejavu) ・ リポジトリ内被引用：21  
  また各マイクロバッチのKVキャッシュをGPUに保持し続けるとメモリを過剰確保し、障害時には失われたKV状態を再計算するため復旧が遅い。DéjàVuはこれらをKVキャッシュの高速な非同期転送という一つの機構で扱う。

- **2023-11 · [HexGen: Generative Inference of Large Language Model over Heterogeneous Environment](2023-2311.11514-hexgen-generative-inference-of-large-language-model-over-heterogeneous-devices.md)**  
  実装：[✓](https://github.com/Relaxed-System-Lab/HexGen) ・ リポジトリ内被引用：21  
  HexGenは、性能もメモリ容量も異なるGPUが複数のデータセンターに分散し、拠点間ネットワークの帯域と遅延も不均一な環境で、大規模言語モデル（LLM）の生成推論を提供する分散実行システムである。

- **2024-10 · [ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving](2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  SLO予測付きトークン調整・層単位プリエンプション・増分KV退避で、オンライン遅延を守りながら遊休GPUをオフライン推論へ回す共同サービング方式。

- **2024-10 · [GraphRouter: A Graph-based Router for LLM Selections](2024-2410.03834-graphrouter-a-graph-based-router-for-llm-selections.md)**  
  実装：[✓](https://github.com/ulab-uiuc/GraphRouter) ・ リポジトリ内被引用：13  
  常に最大モデルを使うと費用が高く、常に最小モデルを使うと精度が不足する。従来の二択ルータやモデル名だけを埋め込む方式では、候補モデルが増えた場合や新しいモデルが登場した場合に適切な選択が難しい。原著の主表では、品質と費用を同等に重視した条件の報酬が0.209となり、比較対象の最高0.196を上回った。

- **2024-08 · [Intelligent Router for LLM Workloads: Improving Performance Through Workload-Aware Load Balancing](2024-2408.13510-intelligent-router-for-llm-workloads-improving-performance-through-workload-aware-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  要点: この研究は、vLLMのような各GPU内スケジューラを改良するのではなく、その一段手前の「どのLLMインスタンスへ要求を送るか」を最適化する。

- **2024-06 · [Enabling Efficient Batch Serving for LMaaS via Generation Length Prediction](2024-2406.04785-enabling-efficient-batch-serving-for-lmaas-via-generation-length-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  入力長・アプリ・利用者特徴から生成長を予測し、近い長さを適応バッチ化してHRRNで順序付けするMagnusにより、スループット最大234%向上・応答時間最大89.7%削減を達成する。

- **2024-01 · [CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference](2024-2401.11240-caraserve-cpu-assisted-lora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  LoRA読込中にCPUでプリフィル計算を先行し、ランク依存のバッチ遅延を予測してSLO違反が少ないサーバへ配分することで、多数アダプタ提供のコールドスタートを隠す。

- **2024-10 · [Fast Inference for Augmented Large Language Models](2024-2410.18248-lamps.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  API待機時のKV処理方式を予測してメモリ時間積で要求を順位付けし、拡張LLM推論の遅延をINFERCEPT比27〜85%削減する。

- **2024-07 · [SLO-Aware GPU DVFS for Energy-Efficient LLM Inference Serving](2024-slo-aware-gpu-dvfs-for-energy-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  RPSとGPU周波数からp95/p99遅延を予測し、25生成反復ごとにSLOを満たす最低周波数へDVFSする方式。GPT-J-6B＋A100/A30の実機配信で、最大周波数運用比22.8〜45.5%のエネルギー削減を示す。

- **2024-03 · [LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Aware Partition and Adaptive Quantization](2024-2403.01136-llm-pq-serving-llm-on-heterogeneous-clusters-with-phase-aware-partition-.md)**  
  実装：[✓](https://github.com/tonyzhao-jt/LLM-PQ) ・ リポジトリ内被引用：11  
  LLM-PQは、性能とメモリ容量が異なるGPUを組み合わせたクラスタで、大規模言語モデル（LLM）の一括推論を高速化するシステムである。異種構成でPipeEdgeを基準にした生成処理量の改善は平均2.26倍、最大2.88倍である。

- **2024-06 · [VideoLLM-online: Online Video Large Language Model for Streaming Video](2024-2406.11816-videollm-online-online-video-large-language-model-for-streaming-video.md)**  
  実装：[✓](https://github.com/showlab/videollm-online) ・ リポジトリ内被引用：10  
  VideoLLM-onlineは、動画が流れている最中に発話すべき瞬間だけ応答する仕組みを、動画ストリーム内学習（Learning-In-Video-strEam、LIVE）として設計した。

- **2024-05 · [Aladdin: Joint Placement and Scaling for SLO-Aware LLM Serving](2024-2405.06856-aladdin-joint-placement-and-scaling-for-slo-aware-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  Aladdinは、複数GPUで大規模言語モデルの推論要求を処理するとき、各要求をどのワーカーへ配置するかと、ワーカーを何台・何GPU構成で用意するかを共同で決めるクラスタスケジューラである。

- **2024-03 · [Optimizing LLM Queries in Relational Data Analytics Workloads](2024-2403.05821-optimizing-llm-queries-in-relational-data-analytics-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  理論上の最適解を探す最適接頭辞ヒット再帰（Optimal Prefix Hit Recursion、OPHR）は組合せ爆発を起こすため、実用方式として貪欲群再帰（Greedy Group Recursion、GGR）を設計する。

- **2024-06 · [Slice-Level Scheduling for High-Throughput and Load-Balanced LLM Serving](2024-2406.13511-slice-level-scheduling-for-high-throughput-and-load-balanced-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  SCLS（スライス単位スケジューリング）は、LLMの応答長が要求到着時に分からないことから生じる二つの資源浪費を解消するサービング手法である。著者らはAnt GroupのCodeFuse実運用要求記録を用い、8台のNVIDIA A100 80GBでLLaMA2-13Bを動かした。

- **2024-03 · [PipeRAG: Fast Retrieval-Augmented Generation via Algorithm-System Co-design](2024-2403.05676-piperag-fast-retrieval-augmented-generation-via-algorithm-system-co-desi.md)**  
  実装：[✓](https://github.com/amazon-science/piperag) ・ リポジトリ内被引用：9  
  検索拡張生成（Retrieval-Augmented Generation、RAG）では、生成開始前に一度だけ外部情報を検索する方式に加え、生成文が伸びる途中でも検索を繰り返す方式がある。1024トークン生成の端から端の遅延では、同等以上の困惑度を維持しながらRETRO比最大2.6倍の短縮を示す。

- **2024-02 · [FlexLLM: Token-Level Co-Serving of LLM Inference and Finetuning with SLO Guarantees](2024-2402.18789-flexllm-token-level-co-serving-of-llm-inference-and-finetuning.md)**  
  実装：[✓](https://github.com/FlexLLM/artifact) ・ リポジトリ内被引用：8  
  推論要求を優先しながら、パラメータ効率微調整（PEFT）の順伝播と逆伝播をトークン窓へ分解し、同じ基盤モデルを使うGPU反復へ混載する。推論の遅延制約を満たす範囲で学習トークン数を動的に選び、分離クラスタ方式より学習処理量を増やすシステムである。

- **2024-04 · [ALTO: An Efficient Network Orchestrator for Compound AI Systems](2024-01aa9dc12834-alto-an-efficient-network-orchestrator-for-compound-ai-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  ALTO（Automatic Language Token Orchestrator）は、言語モデルの生成結果を複数の検索・再順位付け・追加生成段へ渡す複合AIシステムの実行基盤である。論文の実機評価では、応答遅延4秒を目標とする条件で、非逐次転送の比較方式より最大3倍の要求到着負荷を処理し、低負荷での99パーセンタイル遅延を1.8分の1にした。

- **2024-05 · [PerLLM: Personalized Inference Scheduling with Edge-Cloud Collaboration for Diverse LLM Services](2024-2405.14636-perllm-personalized-inference-scheduling-with-edge-cloud-collaboration-f.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LLMの推論要求をすべてクラウドへ送ると、集中するネットワーク転送とGPU待ち行列が遅延・エネルギーを増やす。PerLLMは、要求をエッジとクラウドのどのサーバーへ割り当てるかを、処理期限・利用可能帯域・計算能力の制約の下で決める。

- **2024-04 · [Prepacking: A Simple Method for Fast Prefilling and Increased Throughput in Large Language Models](2024-2404.09529-prepacking-a-simple-method-for-fast-prefilling-and-increased-throughput-in-large-language-models.md)**  
  実装：[✓](https://github.com/siyan-zhao/prepacking) ・ リポジトリ内被引用：6  
  Prepackingは、長さの異なる複数の入力プロンプトを一括処理する際、短いプロンプトを最長プロンプトまでパディングすることで発生する無駄な計算とGPUメモリ消費を減らす方式である。論文は単一のNVIDIA A6000-48GBで、1.3Bから13Bまでのモデルを使って検証する。

- **2024-08 · [SLO-aware GPU Frequency Scaling for Energy Efficient LLM Inference Serving](2024-2408.05235-slo-aware-gpu-frequency-scaling-for-energy-efficient-llm-inference-serving.md)**  
  実装：[✓](https://github.com/WilliamBlaskowicz/throttLL-eM) ・ リポジトリ内被引用：5  
  推論中に変動するバッチサイズとKVキャッシュ量から次の必要性能を予測し、サービス品質目標（service-level objective, SLO）を破らない範囲までGPU周波数を下げる。さらに負荷に合わせてテンソル並列度の異なるエンジンを切り替え、LLM配信の「使っていない性能余裕」をエネルギー削減へ変える。

- **2024-05 · [ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving](2024-2407.09486-enova-autoscaling-towards-cost-effective-and-stable-serverless-llm-servi.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  ENOVAは、LLMを複数GPU・複数クラスタで提供する際、サービングの設定を観測データから選び、性能悪化を検出したら再設定するデプロイ・監視・オートスケーリングの統合システムである。

- **2024-04 · [Deferred Continuous Batching in Resource-Efficient Large Language Model Serving](2024-cd0254f5f44d-deferred-continuous-batching-in-resource-efficient-large-language-model-.md)**  
  実装：[✓](https://github.com/llm-db/FineInfer) ・ リポジトリ内被引用：4  
  前者では微調整の処理率が低下し、後者では利用者の応答遅延が増える。FineInferは、凍結済みの基盤モデル重みを両仕事で共有し、微調整・推論の各反復を細粒度に切り替える。

- **2023-12 · [Unicron: Economizing Self-Healing LLM Training at Scale](2023-2401.00134-unicron-economizing-self-healing-llm-training-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  しかし、通常時の学習速度を犠牲にする方式や、障害を受けた一つのジョブだけを回復させる方式では、複数ジョブが共存するクラスタの長期的な総計算量が最適になるとは限らない。論文が示す最大1.9倍という値は、128枚のA800 GPUを用いた高頻度障害シナリオでの累積重み付き有効演算量のMegatron比である。

- **2024-10 · [SplitLLM: Collaborative Inference of LLMs for Model Placement and Throughput Optimization](2024-2410.10759-splitllm-collaborative-inference-of-llms-for-model-placement-and-through.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式は、層ごとの端末推論時間、端末からサーバーへの上り転送時間、サーバーから端末への下り転送時間、サーバー資源消費量を測定し、モデルの順方向の依存関係を守りながら配置する。

- **2024-01 · [Inferflow: an Efficient and Highly Configurable Inference Engine for Large Language Models](2024-2401.08294-inferflow-an-efficient-and-highly-configurable-inference-engine-for-larg.md)**  
  実装：[✓](https://github.com/inferflow/inferflow) ・ リポジトリ内被引用：3  
  Inferflowは、言語モデルの構造が頻繁に変化する状況で、モデルごとに推論エンジンのソースコードを書き足す負担を減らすことを主目的とした推論基盤である。この拡張性に加え、低ビット量子化と複数GPU分割による実行効率を追求する。

- **2024-02 · [Efficient Prompt Caching via Embedding Similarity](2024-2402.01173-efficient-prompt-caching-via-embedding-similarity.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、言語モデルの生成済み応答そのものを再利用するプロンプトキャッシュの判定精度を改善する研究である。以前の質問に対する回答がキャッシュにあれば、新しい質問を言語モデルへ送らず、その回答を返すことができる。ただし、質問文の意味が近いことと、同じ回答で両方の質問に正しく答えられることは一致しない。

- **2024-04 · [Performance Characterization of Expert Router for Scalable LLM Inference](2024-2404.15153-performance-characterization-of-expert-router-for-scalable-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MoE層内部で複数のFFNエキスパートをtop-k選択する方式とは異なり、リクエスト全体を一つの独立したLLMへルーティングする。評価には8基のNVIDIA H100（各80GB）を搭載したDGX H100を用い、Llama 3 70Bと8Bの量子化・非量子化構成を比較する。

- **2023-12 · [Linear Attention via Orthogonal Memory](2023-2312.11135-linear-attention-via-orthogonal-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意はその費用を下げる有力な手段だが、双方向の文脈全体を一度に圧縮する設計を、そのまま因果的な次トークン予測へ移すと、問い合わせごとに圧縮を作り直すことになり得る。A100 80GBの測定では、16,384トークン時のLAVOメモリは9,337MB、相対速度は通常注意比22.0倍と記載されている。

### 4年前（2022-11〜2023-10）

- **2023-09 · [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)**  
  実装：[✓](https://github.com/vllm-project/vllm) ・ リポジトリ内被引用：1510  
  vLLMは、要求ごとに大きな連続領域を予約していたKVキャッシュを固定長ブロックへ分解し、論理的な並びとGPU上の物理配置を分離する。必要なブロックだけ動的に割り当て、同じ接頭辞のKVを共有することで、限られたGPUメモリへより多くの要求を同時に載せる。

- **2023-08 · [SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills](2023-2308.16369-sarathi.md)**  
  実装：✓ ・ リポジトリ内被引用：180  
  プリフィル分割とデコード最大化混合バッチでデコードを重み読込みへ相乗りさせ、単一GPUとパイプライン並列の双方で推論スループットを改善する。

- **2023-02 · [AlpaServe: Statistical Multiplexing with Model Parallelism for Deep Learning Serving](2023-2302.11665-alpaserve.md)**  
  実装：[✓](https://github.com/alpa-projects/mms) ・ リポジトリ内被引用：172  
  複数モデルへ届くリクエスト数が時間ごとに偏る環境で、モデルを複数GPUへ分割して置き、空いているGPUをモデル間で共有しやすくすることで、特定モデルだけ待ち行列が伸びるのを抑えるサービング配置手法。

- **2023-05 · [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)**  
  実装：[✓](https://github.com/LLMServe/FastServe) ・ リポジトリ内被引用：139  
  出力トークンを1つ生成する区切りで要求（リクエスト）を一時停止・再開できるようにし、短い要求を優先しながらKVキャッシュ（KV キャッシュ）をCPUへ退避・先読みして待ち時間を減らすLLMサービングスケジューラ（serving スケジューラ）。

- **2023-10 · [Punica: Multi-Tenant LoRA Serving](2023-2310.18547-punica-multitenant-lora-serving.md)**  
  実装：[✓](https://github.com/punica-ai/punica) ・ リポジトリ内被引用：46  
  異なるLoRAアダプタの要求をSGMVカーネルで同一バッチ処理し、基盤LLMを共有したまま多テナント推論を集約するサービング基盤。固定GPU資源で最大12倍のスループットを報告。

- **2023-05 · [Response Length Perception and Sequence Scheduling: An LLM-Empowered LLM Inference Pipeline](2023-2305.13144-response-length-perception-and-sequence-scheduling-an-llm-empowered-llm-inference-pipeline.md)**  
  実装：✓ ・ リポジトリ内被引用：44  
  Vicuna自身を軽量な応答長予測器として使い、生成前に要求を長さ別へ並べ替える。予測外れを失敗回収・再計算で隔離し、短い要求には大きなバッチを使うことで、可変長生成に特有のバッチ内遊休を減らす。

- **2023-09 · [LLMCarbon: Modeling the End-To-End Carbon Footprint of Large Language Models](2023-2309.14393-llmcarbon-modeling-the-end-to-end-carbon-footprint-of-large-language-mod.md)**  
  実装：[✓](https://github.com/SotaroKaneda/MLCarbon) ・ リポジトリ内被引用：15  
  LLMCarbonは、大規模言語モデル（LLM）を設計・運用する前に、モデル構造とハードウェア、データセンター条件から二酸化炭素換算排出量（CO2eq）を推定するシステムである。T5、GPT-3、GShard、Switch、XLMの5モデルで既報の学習運用排出量と比較すると、LLMCarbonの推定誤差は-3.54%～+8.2%の範囲だった。

- **2023-05 · [Large Language Models as Tool Makers](2023-2305.17126-large-language-models-as-tool-makers.md)**  
  実装：[✓](https://github.com/ctlllll/LLM-ToolMaker) ・ リポジトリ内被引用：1  
  大規模言語モデルへ複雑な推論を毎回直接依頼すると、同じ種類の問題に対して高価な推論を繰り返すことになる。Large Language Models as Tool Makers（LATM）は、問題の解き方をPython関数として保存する機能キャッシュ（functional キャッシュ）を提案する。

- **2023-05 · [PruMUX: Augmenting Data Multiplexing with Model Compression](2023-2305.14706-prumux-augmenting-data-multiplexing-with-model-compression.md)**  
  実装：[✓](https://github.com/yushansu/PruMUX) ・ リポジトリ内被引用：0  
  PruMUXは、Transformerを使う文章分類・照合の推論で、入力多重化（data multiplexing）と構造化枝刈り（structured 枝刈り）を組み合わせて処理量を高める研究である。MNLIの正解率下限を80%から74%の範囲で変えたとき、BERT-base比7.5～29.5倍の処理量を報告する。

### 5年前（2021-11〜2022-10）

- **2022-07 · [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：615  
  出力トークンを1個生成するたびにスケジューラへ制御を戻し、終わった要求を外して新着要求を追加する。さらに、長さの違う要求を同じバッチで処理できるよう、注意機構だけを要求ごとに分け、それ以外の演算はトークン単位でまとめて実行する分散LLMサービングシステム。

- **2022-04 · [Accelerating Attention through Gradient-Based Learned Runtime Pruning](2022-2204.03227-accelerating-attention-through-gradient-based-learned-runtime-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、Transformerの自己注意における「どの単語対の関連度が小さいかは入力が来るまで分からない」という制約を、学習可能な層別閾値と専用演算器の共同設計で解く。

### 6年前（2020-11〜2021-10）

- **2020-11 · [Serving DNNs like Clockwork: Performance Predictability from the Bottom Up](2020-2006.02464-serving-dnns-like-clockwork-performance-predictability-from-the-bottom-u.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  Clockworkは、深層ニューラルネットワーク（DNN）のオンライン推論で、平均速度ではなく要求ごとの締切と尾部遅延を中心に設計した分散モデル提供システムである。

- **2021-07 · [Long-Short Transformer: Efficient Transformers for Language and Vision](2021-2107.02192-long-short-transformer-efficient-transformers-for-language-and-vision.md)**  
  実装：[✓](https://github.com/NVIDIA/transformer-ls) ・ リポジトリ内被引用：13  
  Transformer-LSは、系列長を長くしたときの自己注意の二乗計算量を減らしながら、近傍の細部と遠方の関係を同じ層で扱うための注意機構である。ただし実験の中心は2021年当時の文字単位言語モデルと画像分類モデルであり、現代の数十億パラメータ級LLMサービングにおける鍵・値キャッシュ削減や連続バッチ処理を直接評価したものではない。

- **2021-10 · [OneFlow: Redesign the Distributed Deep Learning Framework from Scratch](2021-2110.15032-oneflow-redesign-the-distributed-deep-learning-framework-from-scratch.md)**  
  実装：[✓](https://github.com/Oneflow-Inc/oneflow) ・ リポジトリ内被引用：3  
  論文は分散学習を二つの問題に分解する。OneFlowはコンパイラと実行系を一体で設計し、これらを明示的に扱う。

- **2021-09 · [Multi-model Machine Learning Inference Serving with GPU Spatial Partitioning](2021-2109.01611-multi-model-machine-learning-inference-serving-with-gpu-spatial-partitio.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  複数モデルを時間順に切り替えるだけでは、この遊休部分を他モデルへ同時に渡せない。提案の干渉考慮版「gpulet+int」は、同一4 GPU実機で既存の時間共有方式SBPに対し、5種類の複数モデル推論シナリオにおける最大処理量を平均102.6%改善した。

- **2021-10 · [DCT: Dynamic Compressive Transformer for Modeling Unbounded Sequence](2021-2110.04821-dct-dynamic-compressive-transformer-for-modeling-unbounded-sequence.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DCTは、系列が長くなっても古い情報を保持したい言語モデルに対し、記憶から押し出される過去の隠れ状態を必ず保存するのではなく、必要性を判定してから圧縮記憶へ追加する仕組みを提案した研究である。この改善は予測品質の比較であり、GPU推論スループット、TTFT、TPOT、メモリ消費量が実測で何倍改善したという結果ではない。

### 7年前（2019-11〜2020-10）

- **2020-08 · [Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning](2020-2008.12260-pollux-co-adaptive-cluster-scheduling-for-goodput-optimized-deep-learnin.md)**  
  実装：[✓](https://github.com/petuum/adaptdl) ・ リポジトリ内被引用：5  
  共有GPUクラスタで深層学習ジョブを実行するとき、割り当てたGPUを多く使うことと、目標精度へ早く到達することは同じではない。OSDI 2021の実験では、16ノード64基のNVIDIA T4 GPUを用い、十分に手作業調整されたOptimus+OracleとTiresiasに対して平均ジョブ完了時間をそれぞれ50%と37%短縮した。

### 8年前（2018-11〜2019-10）

- **2019-01 · [Pay Less Attention with Lightweight and Dynamic Convolutions](2019-1901.10430-pay-less-attention-with-lightweight-and-dynamic-convolutions.md)**  
  実装：[✓](https://github.com/pytorch/fairseq) ・ リポジトリ内被引用：14  
  自己注意（self-注意機構）は各時刻の問い合わせと文脈中の鍵を比較して重みを求めるため、系列長に対して二次の計算費用が生じる。速度面でも高度に最適化された自己注意方式より約20%速い実行を報告するが、この倍率は特定の実験設定の結果であり、全ての系列長やGPUで保証されない。
<!-- survey:auto:end -->
