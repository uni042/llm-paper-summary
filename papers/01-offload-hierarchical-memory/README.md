# オフロード／階層メモリ

収録論文: 14本。公開日が新しい順。

- 2026-08-14 — [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)
  - High-Bandwidth FlashからexpertをGPU／HBMへ直接供給し、従来NVMeを超える大容量MoE推論を狙う階層メモリ設計。
- 2026-05-18 — [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)
  - expert tokenを大きなcoalesced batchに集約し、AMX対応CPUとGPUへ処理を分担して、メモリ制約下のMoE serving throughputを高める。
- 2026-04-29 — [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)
  - consumer GPU群をstateless worker poolとしてlayer stageをround-robin dispatchし、非対称分割と優先転送でpipeline bubbleとoffload待ちを減らす。
- 2025-12-19 — [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)
  - 同一layerの全microbatchをまとめる垂直スケジューリングと次iterationへのoptimizer重畳で、NVMeオフロード学習のI/O回数と待ち時間を減らす。
- 2025-09-02 — [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)
  - optimizer stateをGPU・DRAM・NVMe・並列ファイルシステムへ多階層・多経路配置し、汎用HPC環境でLLM事前学習のI/Oを並列化する。
- 2025-02-09 — [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)
  - 複数batchのhot expert計算でcold expertのCPU／SSD I/Oを隠し、巨大MoEを単一GPUで動かすexpert-aware pipeline。
- 2025-02-07 — [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)
  - expertを細粒度blockへ分割して必要部分だけをロードし、MoE servingのメモリ削減と転送遅延を調整する方式。
- 2024-11-18 — [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)
  - expertの配置・ロード・GPU計算をデータ中心にpipeline化し、メモリ制約GPUでMoEのI/O待ちを隠す推論システム。
- 2024-05-29 — [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)
  - computational storage上でexpert計算を行うnear-data executionにより、巨大MoEのストレージ帯域とGPU転送を削減する方式。
- 2024-02-10 — [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)
  - GPUに常駐しないexpertをCPUで直接計算し、重いweight transferをactivation転送へ置き換えるCPU–GPU協調MoE推論方式。
- 2024-01-25 — [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)
  - sequenceごとのexpert活性局所性を使うsparsity-aware cacheと先読みで、個人PC上の階層メモリMoE推論を高速化するシステム。
- 2023-12-28 — [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)
  - MoE expertをCPUへ置き、activation-awareなcacheと先読みでGPUメモリ制約下の重み転送を抑える推論手法。
- 2023-12-12 — [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)
  - Flashから必要な重み行列部分だけを読み、windowingとrow-column bundlingで端末上LLMのI/OとDRAM使用量を減らす手法。
- 2023-10-13 — [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)
  - GPU memoryとhost memory・storageを統合し、tensorの生存期間と再利用を基に階層間migrationを自動化する学習システム。
