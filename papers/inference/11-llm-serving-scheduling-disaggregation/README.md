# LLM Serving / Scheduling / Disaggregation

複数request・複数GPU / nodeを使うLLM servingで、**iteration-level batching、request scheduling、prefillとdecodeの資源配分、conversation / KV state再利用、model startup、cluster間data transfer、elastic resource管理**をまとめて設計し、latency / SLOを守りながらgoodput・throughput・cost効率・fairnessを高める研究をまとめる。

単一requestのkernel高速化や単一GPUのmemory節約ではなく、**「いつどのrequestを実行するか」「batchをどう組み替えるか」「どのinstance / phaseへ配置するか」「modelや実行中stateをどこへ動かすか」「client間でserviceをどう配分するか」**が主題となる。continuous batching、preemption、chunked prefill、prefill / decode disaggregation、request migration、stateful conversation、global KV cache、fair scheduling、admission control、serverless / elastic servingなどを含む。

KV cacheをCPU / storageへ退避すること自体が主目的なら `KV Cache Offload / Recomputation`、MoE expert placementが主目的なら各MoE系統に分類する。

## 収録論文

収録論文: 12本。公開日が新しい順。

- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefill / decode clusterを分離し、CPU DRAM・SSD・RDMAを跨ぐglobal KV cacheとcache-aware schedulerを組み合わせて、長context servingのSLO付きrequest capacityを高める。
- 2024-06-05 — [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)
  - requestとKV cacheを実行中のmodel instance間でlive migrationし、load imbalance・memory fragmentation・priority差・auto-scalingに応じてplacementをruntimeで組み替える。
- 2024-03-04 — [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)
  - 長いprefillを小さいchunkへ分け、既存decodeを毎iteration先に処理して残りtoken budgetへprefillを詰めることで、generation stallを防ぎながらserving capacityを高める。
- 2024-01-25 — [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)
  - model checkpointをlocal SSD / DRAMへcacheし、高速loader・token-based live migration・checkpoint locality-aware schedulingでserverless cold startを短縮する。
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
  - prefillとdecodeを別GPUへ分離し、各phaseのGPU数・parallelism・physical placementをTTFT / TPOT SLOとnetwork帯域に合わせて別々に最適化する。
- 2023-12-31 — [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)
  - clientごとの入力・出力tokenに基づく累積service量を追跡し、serviceが少ないclientを優先するVTCでGPUをidleにせずclient-level fairnessを保つ。
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
- **Client-level fair scheduling:** VTCはclientごとの累積serviceをtoken costでaccountingし、work-conservingなままservice差をboundedに保つ。
- **Stateful conversation serving:** Pensieveはconversation KVをrequest終了後も保持し、follow-up requestでhistoryの重複prefillを避ける。
- **Colocated stall-free scheduling:** Sarathi-ServeはP/Dを同じGPUへ残したままprefillをchunk化し、decode latencyを保護する。
- **P/D resource disaggregation:** DistServeはprefill / decodeを別resource poolとしてprovisionし、SLO付きgoodputを最大化する。
- **Hardware specialization:** SplitwiseはphaseごとにGPU世代・power budgetを変え、Perf/$・Perf/Wまでcluster designへ取り込む。
- **Serverless model startup:** ServerlessLLMはcheckpoint localityとloading timeをplacement costに含め、高速checkpoint loadingとlive migrationでcold startを抑える。
- **Elastic / preemptible serving:** SpotServeは利用可能GPU数の変動に合わせてparallel topologyを再構成し、weight / KV stateを再利用しながらspot instance上でserveする。
- **Runtime request migration:** Llumnixはrunning requestとKVをinstance間で移し、dispatch後に判明したload imbalanceやfragmentationを修正する。
- **Global KV-centric serving:** MooncakeはP/D分離の上にdistributed KV cache poolを置き、prefix reuse・replication・RDMA transferをglobal schedulerで扱う。

この系統は独立した研究群として継続し、SLO-aware fairness、serverless / autoscaling、stateful prefix reuse、heterogeneous routingなどの引用鎖も引き続き確認する。