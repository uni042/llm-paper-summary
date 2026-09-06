# Training Offload / Memory Systems

収録論文: 11本。公開日が新しい順。

- 2026-04-29 — [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)
  - consumer GPU群をstateless worker poolとして使い、pipeline bubbleとoffload待ちを減らす。
- 2025-12-19 — [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)
  - NVMe-offloaded trainingでI/O回数とoptimizer待ちを減らす。
- 2025-11-18 — [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)
  - GPU・CPU・SSD間のtensor cache配置とmigrationを動的最適化する。
- 2025-09-02 — [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)
  - optimizer stateをGPU・DRAM・NVMe・並列ファイルシステムへ多階層配置する。
- 2025-06-06 — [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)
  - tensor lifetimeに基づきNVMeへのoffload timingを決める。
- 2025-05-29 — [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)
  - direct NVMe I/O、buffer管理、低精度optimizerでSSD-offloaded fine-tuningを改善する。
- 2025-05-18 — [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)
  - CPU側の非同期更新でoffload stallを抑える。
- 2024-08-19 — [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)
  - activationをNVMe SSDへ非同期退避・先読みする。
- 2024-06-14 — [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)
  - sparse projected updateをCPUへoffloadしてcommodity GPUでfine-tuningする。
- 2024-03-11 — [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)
  - SmartSSD上でoptimizer更新をnear-storage処理する。
- 2023-10-13 — [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)
  - GPU memory、host memory、storage間のtensor migrationを自動化する学習システム。
