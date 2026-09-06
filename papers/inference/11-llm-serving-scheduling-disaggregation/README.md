# LLM Serving / Scheduling / Disaggregation

複数request・複数GPU / nodeを使うLLM servingで、**prefillとdecodeの資源配分、request scheduling、KV cache共有、cluster間data transfer**をまとめて設計し、TTFT / TBTなどのSLOを守りながらgoodputを高める研究をまとめる。

単一requestのkernel高速化や単一GPUのmemory節約ではなく、**serving cluster全体で「どのrequestを、どのstageで、どのinstanceに割り当てるか」**が主題となる。prefill / decode disaggregation、chunked prefill、global KV cache、load balancing、admission control、phaseごとのhardware provisioningなどを含む。

KV cacheをCPU / storageへ退避すること自体が主目的なら `KV Cache Offload / Recomputation`、MoE expert placementが主目的なら各MoE系統に分類する。

## 収録論文

収録論文: 3本。公開日が新しい順。

- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefill / decode clusterを分離し、CPU DRAM・SSD・RDMAを跨ぐglobal KV cacheとcache-aware schedulerを組み合わせて、長context servingのSLO付きrequest capacityを高める。
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
  - prefillとdecodeを別GPUへ分離し、各phaseのGPU数・parallelism・physical placementをTTFT / TPOT SLOとnetwork帯域に合わせて別々に最適化する。
- 2023-11-30 — [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)
  - promptとtoken generationを別machine poolへ分け、phaseごとにA100 / H100やpower capを選んでcluster throughput・cost・powerを最適化する。

## 主な技術の分岐

- **P/D resource disaggregation:** DistServeはprefill / decodeを別resource poolとしてprovisionし、SLO付きgoodputを最大化する。
- **Hardware specialization:** SplitwiseはphaseごとにGPU世代・power budgetを変え、Perf/$・Perf/Wまでcluster designへ取り込む。
- **Global KV-centric serving:** MooncakeはP/D分離の上にdistributed KV cache poolを置き、prefix reuse・replication・RDMA transferをglobal schedulerで扱う。

この系統は3本以上の明確な研究群になったため、通常の独立系統として継続する。Sarathi-Serve等のcolocated schedulingもcluster-level serving設計として境界を確認しながら追加する。