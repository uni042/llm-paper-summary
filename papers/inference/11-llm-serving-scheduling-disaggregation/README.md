# LLM Serving / Scheduling / Disaggregation

複数request・複数GPU / nodeを使うLLM servingで、**prefillとdecodeの資源配分、request scheduling、KV cache共有、cluster間data transfer**をまとめて設計し、TTFT / TBTなどのSLOを守りながらgoodputを高める研究をまとめる。

単一requestのkernel高速化や単一GPUのmemory節約ではなく、**serving cluster全体で「どのrequestを、どのstageで、どのinstanceに割り当てるか」**が主題となる。prefill / decode disaggregation、chunked prefill、global KV cache、load balancing、admission controlなどを含む。

KV cacheをCPU / storageへ退避すること自体が主目的なら `KV Cache Offload / Recomputation`、MoE expert placementが主目的なら各MoE系統に分類する。

## 収録論文

収録論文: 1本。公開日が新しい順。

- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefill / decode clusterを分離し、CPU DRAM・SSD・RDMAを跨ぐglobal KV cacheとcache-aware schedulerを組み合わせて、長context servingのSLO付きrequest capacityを高める。

今後はDistServe、Splitwise、Sarathi-Serveなど、同じcluster-level serving設計の引用鎖を確認しながら収録・境界調整する。