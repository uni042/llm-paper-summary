# KV Cache Offload / Recomputation

local GPU HBMに収まらないKV cacheを**CPU DRAM・別GPUのHBM・storageなどへ置く、KVを使うattention計算をdataの近くへ移す、またはKVを運ぶ代わりに一部をGPUで作り直す**研究をまとめる。

`KV Cache Optimization / Compression` が「どのKVを残すか・どれだけ小さくするか」を主に扱うのに対し、この系統は**KVをlocal HBM以外へ置いたとき、どこから読み、どこでattentionを計算し、転送と再計算をどう使い分けるか**が中心課題である。

weightやexpert全般を含む汎用memory hierarchyは `Offload / Hierarchical Memory` に残し、KV cache固有の配置・attention実行場所・再計算を主題とする論文はこちらへ分類する。

## 収録論文

収録論文: 19本。公開日が新しい順。

- 2026-07-13 — [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md)
- 2026-05-18 — [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md)
- 2026-05-05 — [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md)
- 2026-05-05 — [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md)
- 2026-03-28 — [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md)
- 2026-03-18 — [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md)
- 2026-02-07 — [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md)
- 2026-01-28 — [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md)
- 2025-12-16 — [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md)
- 2025-07-01 — [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md)
- 2025-06-03 — [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md)
- 2025-03-20 — [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md)
  - full-precision KVをCPU DRAMへ保持し、GPU上のlow-bit KV要約で重要KVを選び、次stepのKVを先読みしてCPU→GPU転送とdecode計算を重ねる。
- 2025-01-03 — [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md)
- 2024-11-26 — [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md)
- 2024-11-14 — [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md)
- 2024-11-02 — [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md)
- 2024-09-08 — [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)
- 2024-07-31 — [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md)
- 2024-03-18 — [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)

## 主な技術の分岐

- **KVのある場所でattentionする:** FastDecode / NEO / APEXはKVがあるCPUへattentionを寄せ、InstAttentionは同じ発想を計算機能付きSSDまで進める。
- **CPU attentionを前倒ししてGPU待ちを隠す:** ScoutAttentionは次layerのCPU attentionを予測queryで早く開始する。
- **KV転送の一部を再計算へ置き換える:** KVPR / CAPTUREは小さいactivationからGPUでKVを作り直す。
- **別GPUの空きHBMを借りる:** Aquaは別GPUの余剰HBMを高速な退避先として使う。
- **使う直前にCPUからGPUへ先読みする:** Pieはlayer順、SpeCacheは次tokenのattention予測を使ってKV転送を計算と重ねる。
- **CPU上のKVを検索する:** RetroInfer / ParisKVは全KVを戻さず必要subsetだけを選択する。
- **SSDへのI/O制御をGPUへ移す:** TuttiはI/O request発行・管理をGPU側へ寄せる。
- **複数SSDの帯域を束ねる:** Swarmは同時参照KVを複数SSDへ分散する。
- **attention sparsityと3階層storageを協調させる:** KVDriveはHBM/DRAM/SSDの配置とselection/fetch/computeをpipeline化する。

実行場所やmemory tierは異なるが、共通して**KVをlocal GPU HBMだけへ固定すると容量や転送帯域が限界になる問題を避ける、またはその限界を定量化する**研究として扱う。
