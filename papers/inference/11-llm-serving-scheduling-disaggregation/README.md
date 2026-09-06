# LLM Serving / Scheduling / Disaggregation

複数request・複数GPU / nodeを使うLLM servingで、**iteration-level batching、token-budget / chunked-prefill scheduling、request scheduling、prefillとdecodeの資源配分、conversation / KV state再利用、application-level dependency、model startup、cluster間data transfer、elastic resource管理、user-perceived streaming QoE**をまとめて設計し、latency / SLOを守りながらgoodput・throughput・cost効率・fairness・体感品質を高める研究をまとめる。

単一requestのkernel高速化や単一GPUのmemory節約ではなく、**「いつどのrequestを実行するか」「batchをどう組み替えるか」「どのinstance / phaseへ配置するか」「modelや実行中stateをどこへ動かすか」「複数LLM callの依存関係や共有contextをどう使うか」「どのrequestへ次のtokenを与えるとuser experienceが改善するか」**が主題となる。continuous batching、preemption、chunked prefill、SLO-aware queueing、prefill / decode disaggregation、request migration、stateful conversation、application-aware scheduling、global KV cache、prefix-locality-aware routing、fair scheduling、predictive job-size scheduling、QoE-aware streaming、serverless / elastic servingなどを含む。

KV cacheをCPU / storageへ退避すること自体が主目的なら `KV Cache Offload / Recomputation`、MoE expert placementが主目的なら各MoE系統に分類する。

## 収録論文

収録論文: 22本。公開日が新しい順。

- 2025-01-24 — [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)
  - client間のservice deficitをboundedに保ちながら、その許容範囲でshared prefixが長いrequestをまとめるDLPMと、複数GPUでfairness・prefix locality・load balanceを両立するD²LPMを提案する。
- 2024-08-28 — [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)
  - promptから出力長の絶対値ではなくrequest間の相対順位を小型予測器で学習し、短いrequestを優先してSJF / SRTFへ近づけることでHOL blockingを減らす。
- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefill / decode clusterを分離し、CPU DRAM・SSD・RDMAを跨ぐglobal KV cacheとcache-aware schedulerを組み合わせて、長context servingのSLO付きrequest capacityを高める。
- 2024-06-25 — [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)
  - GPU HBM・CPU DRAM上のKVをinstance横断で管理・検索・転送するMemPoolを導入し、context cachingとP/D分離を同じmemory substrate上で組み合わせる。
- 2024-06-05 — [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)
  - batch / interactive request、複数model、異なるSLOを同じqueueで扱い、待ち時間予測を使ってrequest groupの順序とinstance割当を組み替える。
- 2024-06-05 — [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)
  - requestとKV cacheを実行中のmodel instance間でlive migrationし、load imbalance・memory fragmentation・priority差・auto-scalingに応じてplacementをruntimeで組み替える。
- 2024-05-30 — [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)
  - 複数LLM callのprompt構造・依存関係・共有prefixをbackendへ伝え、request DAG全体を見ながら並列化・batching・prefix reuse・schedulingを共同最適化する。
- 2024-05-08 — [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)
  - shared prefixを持つrequestのKV再利用量とGPU負荷を同じ計算costで比較するE2 schedulerにより、cluster-level prefix localityとload balanceを共同最適化する。
- 2024-04-25 — [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)
  - streaming responseのuser consumption timelineをQoEとして定式化し、token-level preemptionとclient-side pacingで、先行生成に使うGPUをTTFT待ちやtoken不足が近いrequestへ振り替える。
- 2024-03-23 — [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)
  - multi-turn history KVをDRAM / SSDへ階層保存し、scheduler-awareなlayer-wise preloadと非同期saveで次turnのhistory再prefillとslow-tier待ちを減らす。
- 2024-03-04 — [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)
  - 長いprefillを小さいchunkへ分け、既存decodeを毎iteration先に処理して残りtoken budgetへprefillを詰めることで、generation stallを防ぎながらserving capacityを高める。
- 2024-01-25 — [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)
  - model checkpointをlocal SSD / DRAMへcacheし、高速loader・token-based live migration・checkpoint locality-aware schedulingでserverless cold startを短縮する。
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
  - prefillとdecodeを別GPUへ分離し、各phaseのGPU数・parallelism・physical placementをTTFT / TPOT SLOとnetwork帯域に合わせて別々に最適化する。
- 2024-01-09 — [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)
  - 長promptをchunkへ分割し、短prompt・prefill・decodeをtarget token budgetへ融合するDynamic SplitFuseでforward work量を均し、generation stallとtail latencyを抑える。
- 2023-12-31 — [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)
  - clientごとの入力・出力tokenに基づく累積service量を追跡し、serviceが少ないclientを優先するVTCでGPUをidleにせずclient-level fairnessを保つ。
- 2023-12-12 — [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)
  - 複数generation callやcontrol flowを含むLM programをruntimeが理解し、RadixAttentionによるprefix KV reuse、cache-aware scheduling、structured decodingをまとめて最適化する。
- 2023-12-09 — [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)
  - multi-turn conversationの過去history KVをrequest間で保持し、GPU / CPU tiered cacheと非連続KV対応attentionで毎turnのhistory再prefillを避ける。
- 2023-11-30 — [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)
  - promptとtoken generationを別machine poolへ分け、phaseごとにA100 / H100やpower capを選んでcluster throughput・cost・powerを最適化する。
- 2023-11-27 — [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)
  - spot GPUの増減に合わせてmodel parallel構成を動的に組み替え、既存weight・KVを再利用するmigrationとtoken単位のstate recoveryで安価なpreemptible instanceを活用する。
- 2023-09-12 — [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)
  - KV cacheを固定長blockへ分けて必要な分だけ非連続memoryへ配置・共有し、fragmentationと過剰予約を減らしてcontinuous batchへ載せられるrequest数を増やす。
- 2023-05-10 — [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)
  - output tokenごとにrequestをpreemptし、入力長を使ったpriority schedulingと先回りKV swapで長いrequestによるqueueing delayを抑える。
- 2022-07-11 — [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)
  - 1 token generationごとにbatchを組み替え、attention以外をtoken単位でまとめて実行することで、異なる長さ・進行位置のrequestを同じbatchへ柔軟に混在させる。

## 主な技術の分岐

- **Iteration-level flexible batching:** Orcaはrequest全体ではなく1 token generationをscheduling boundaryとし、continuous batchingの基礎を作る。
- **Paged KV memory:** vLLMはKV cacheをpage-like blockで管理・共有し、continuous batchingをmemory側から大きくする。
- **Preemptive priority scheduling:** FastServeはiteration boundaryでrunning requestをpreemptし、priorityとproactive KV swappingでhead-of-line blockingを抑える。
- **Predictive job-size scheduling:** Efficient LLM Scheduling by Learning to Rankはpromptからgeneration lengthの相対順位を予測し、実行前から短いrequestを優先してSJF / SRTFへ近づける。
- **Token-budget / chunked-prefill scheduling:** DeepSpeed-FastGenは長promptをsplitし短promptをfuseしてforwardの総token数をtargetへ揃え、Sarathi-Serveはdecodeを保護した上で残りtoken budgetへprefill chunkを詰めてgeneration stallを抑える。
- **SLO-aware queue management:** QLMはrequest waiting time、SLO slack、model locality、instance loadを見てmulti-model queue順序と割当を最適化する。
- **QoE-aware text streaming:** Andesは人間がtokenを消費するtimelineを目的関数へ入れ、十分先まで生成済みのrequestをpreemptして、そのGPU時間をTTFT待ちやstream starvationが近いrequestへ回す。
- **Prefix-locality-aware cluster routing:** Prebleはprefix reuseで節約できるprefill計算とGPU load / KV eviction costを共同評価し、shared-prefix requestを同じGPUへ集める利得とhotspot回避を両立する。
- **Client-level fair scheduling:** VTCはclientごとの累積serviceをtoken costでaccountingし、work-conservingなままservice差をboundedに保つ。DLPM / D²LPMはそのfairness boundを緩めた範囲でprefix localityを優先し、distributed settingではload balanceも同時に扱う。
- **Application / program-aware serving:** Parrotはrequest DAGとSemantic Variableを使ってapplication全体をscheduleし、SGLangはLM program構造とpersistent prefix cacheをruntime最適化へ利用する。
- **Stateful conversation serving:** PensieveはGPU / CPU cacheでconversation KVをrequest間保持し、CachedAttentionはDRAM / SSD hierarchyとscheduler hintまで使って同じreuseを大規模化する。
- **P/D resource disaggregation:** DistServeはprefill / decodeを別resource poolとしてprovisionし、SLO付きgoodputを最大化する。
- **Distributed stateful P/D serving:** MemServeはGPU HBM・CPU DRAMを跨ぐMemPoolでhistorical KVをinstance横断管理し、context cachingとP/D分離を同時に成立させる。
- **Hardware specialization:** SplitwiseはphaseごとにGPU世代・power budgetを変え、Perf/$・Perf/Wまでcluster designへ取り込む。
- **Serverless model startup:** ServerlessLLMはcheckpoint localityとloading timeをplacement costに含め、高速checkpoint loadingとlive migrationでcold startを抑える。
- **Elastic / preemptible serving:** SpotServeは利用可能GPU数の変動に合わせてparallel topologyを再構成し、weight / KV stateを再利用しながらspot instance上でserveする。
- **Runtime request migration:** Llumnixはrunning requestとKVをinstance間で移し、dispatch後に判明したload imbalanceやfragmentationを修正する。
- **Global KV-centric serving:** MooncakeはP/D分離の上にdistributed KV cache poolを置き、prefix reuse・replication・RDMA transferをglobal schedulerで扱う。

この系統は独立した研究群として継続し、SLO-aware fairness、QoE / deadline-aware streaming、agent / program-aware serving、serverless / autoscaling、stateful prefix reuse、heterogeneous routing、predictive schedulingなどの引用鎖も引き続き確認する。