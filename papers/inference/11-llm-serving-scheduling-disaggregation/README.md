# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

## 収録論文

収録論文: 36本。公開日が新しい順。

- 2026-09-04 — [Adaptive Context Parallelism for Production LLM Serving](2026-2609.04774-vertumnus-adaptive-context-parallelism.md)
  - requestごとにcontext parallelism（文脈並列）のdegreeを選び、workload変化に合わせてGPU群のCP構成をsplit / mergeしつつprefix cacheも配置・複製して、長context servingのTTFTとSLO達成率を改善する。
- 2026-09-01 — [OUTLETS: Output-Length Prediction from Speculative Decoding Backbones](2026-2609.01068-outlets-output-length-prediction-speculative-decoding.md)
  - speculative decodingで既に計算されるdraft表現へ軽量な回帰headを付けて出力長を予測し、短いrequestの優先処理とdecode instance間の負荷分散へ使うことでtail latencyを下げる。
- 2026-08-17 — [Pallas: A Proactive KV Cache Migration Framework for LLM Inference in AI-RAN](2026-2608.16477-pallas-proactive-kv-cache-migration-ai-ran.md)
  - handover前に安定prefixを移行先で再計算し、生成中suffix KVを移行元から転送して、切替後の生成停止と遠隔経路のITLを減らす。
- 2026-08-15 — [P-PAS: Prefill-Pressure Adaptive Scheduling for Long-Context LLM Serving](2026-2608.15171-p-pas-prefill-pressure-adaptive-scheduling.md)
  - concurrent prefillとactive decodeからtoken budgetを動的に切り替え、長prefillの効率とdecode interferenceを調整する。
- 2026-08-06 — [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](2026-2608.06557-cascade-slo-aware-latency-budget-serving.md)
  - requestごとの残りlatency budgetを継続推定し、実行順とHBM / CPU DRAM / NVMe間のKV復元・先読み・保持・再計算を同じbudgetで決めて、SLO達成量と長context requestへの公平性を両立する。
- 2026-07-30 — [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)
  - prefill / decode分離でKV全体を転送せず、使われやすいKVを先送りし、不足分のremote取得とlocal読出しを並列化してstage切替待ちを減らす。
- 2026-07-18 — [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)
  - 未知の出力長に対するKV予約量、GPU構成、routing、prefix cachingを分布変化まで考慮して共同最適化し、過剰予約とpreemptionを抑える。
- 2026-07-04 — [Online Linear Programming for Multi-Objective Routing in LLM Serving](2026-2607.03948-online-linear-programming-multi-objective-routing.md)
  - batch枠とKV cacheをresource budgetとして価格付けし、SLO便益とshadow priceを比較してworker routingを決め、latency・TTFT・throughput・tail SLOを同じonline最適化で調整する。
- 2026-06-23 — [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)
  - 低頻度な複数MoEでFFN weight用GPU poolとKV / attention用GPU poolを分離し、model間で変動するKV需要を共有してHBM利用率を上げる。
- 2026-06-21 — [Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice](2026-2606.22327-geometry-aware-online-scheduling.md)
  - requestの処理時間だけでなく生成中に増えるKV cacheの占有量を含む時空間volumeで優先順位を決め、memory pressure下の平均・tail latencyを下げる。
- 2026-03-06 — [MoEless: Efficient MoE LLM Serving via Serverless Computing](2026-2603.06350-moeless-serverless-moe-serving.md)
  - hot expertを予測しserverless replicaを動的にscale・配置してexpert stragglerを減らす。
- 2025-01-24 — [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)
  - client間のGPU利用公平性を保ちながら、許容範囲だけ実行順を変えて同じprefixを持つrequestを続け、KV再利用を増やす。
- 2025-01-14 — [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)
  - GPU内のconcurrencyを速い周期、cluster全体のinstance数を遅い周期で制御し、interactive SLOを守りつつ余剰capacityをbatch処理へ使う。
- 2024-08 — [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)
  - 大規模prefill / decode分離clusterでP/D比をworkloadごとに調整し、request再転送とblock-free KV transferで固定構成のmismatchを減らす。
- 2024-08-28 — [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)
  - 出力token数の絶対値ではなくrequest同士の長さ順位を小型modelで予測し、短く終わりそうなrequestを先に処理してqueue待ちを減らす。
- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefill / decodeを別poolへ分け、CPU DRAM・SSDへ保存したKVをcluster全体で再利用し、KV取得・queue待ち・再計算costを見てrequest配置を決める。
- 2024-06-25 — [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)
  - GPU / CPU上のKVをinstance横断で検索・共有・転送できるmemory poolを作り、prefix reuseとprefill→decode KV移動を同じ仕組みで扱う。
- 2024-06-05 — [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)
  - request groupのSLO残余時間とmodel配置を見てqueue順序と実行先を調整し、interactive / batch・複数model混在時のSLO達成率を上げる。
- 2024-06-05 — [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)
  - 実行中requestのKVを別instanceへ段階移動し、load imbalance・memory不足・priority変更後でも配置をruntimeで修正する。
- 2024-05-30 — [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)
  - 複数LLM callのdataflowと共有promptをbackendへ伝え、application全体を見て並列実行・batching・prefix KV reuseを最適化する。
- 2024-05-08 — [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)
  - prefix KV再利用で節約できるprefill計算とGPU混雑による待ち時間を比較し、distributed servingでrequestの送り先を決める。
- 2024-04-25 — [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)
  - token生成速度だけでなく人間の読解速度に対するstreaming QoEを見て、十分先行生成済みのrequestからGPU時間を必要なrequestへ回す。
- 2024-03-23 — [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)
  - multi-turn会話のKVをrequest終了後もDRAM / SSDへ保存し、次turnでprefetchしてhistoryの再prefillとstorage待ちを減らす。
- 2024-03-04 — [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)
  - 長いprefillをchunk化し、毎iterationでdecodeを先に処理して残りtoken budgetへprefillを入れ、generation stallを防ぐ。
- 2024-01-25 — [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)
  - local SSD / DRAMにmodel checkpointをcacheし、model localityを考慮したrequest配置とrunning request移動でserverless cold startを短縮する。
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
  - prefillとdecodeを別GPU群へ分け、各phaseのGPU数・parallelism・物理配置をTTFT / TPOT SLOに合わせて独立最適化する。
- 2024-01-09 — [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)
  - 長promptを小分けにし、prefill chunk・短prompt・decode tokenを総token数が揃うよう混ぜてGPU利用率とtail latencyを両立する。
- 2023-12-31 — [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)
  - clientごとの累積input / output token処理量を重み付きで追跡し、service量が少ないclientを優先してGPUを遊ばせず公平性を保つ。
- 2023-12-12 — [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)
  - 複数LLM callや条件分岐を一つのprogramとしてruntimeが理解し、共有prefix KV、並列実行、structured output生成をまとめて効率化する。
- 2023-12-09 — [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)
  - multi-turn conversationの過去KVをrequest終了後もGPU / CPUへ保持し、次turnでhistory全体を再prefillする重複計算を避ける。
- 2023-11-30 — [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)
  - prefillとdecodeを別machine poolへ分け、各phaseに向くGPU世代・power setting・台数を使い分けてcostとthroughputを改善する。
- 2023-11-27 — [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)
  - spot GPUの増減に合わせてmodel parallel構成を組み替え、既存weightとKVを再利用してpreemption下でもservingを継続する。
- 2023-09-12 — [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)
  - KV cacheを固定長blockへ分けて必要分だけ割り当て・共有し、memory fragmentationと予約浪費を減らして同時request数を増やす。
- 2023-05-10 — [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)
  - token生成iterationごとにrequestをpreempt / resumeし、短いrequestを優先しながらKVのCPU退避とprefetchで待ち時間を減らす。
- 2023-02-22 — [AlpaServe: Statistical Multiplexing with Model Parallelism for Deep Learning Serving](2023-2302.11665-alpaserve.md)
  - modelを複数GPUへ分割して配置し、model間で偏るtrafficを共有GPU poolへ統計的に多重化して、特定modelだけqueueが伸びるのを抑える。
- 2022-07-11 — [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)
  - output tokenを1つ生成するたびbatchを組み替え、進行位置や長さが異なるrequestを途中から出し入れできるcontinuous batchingの基礎を示す。