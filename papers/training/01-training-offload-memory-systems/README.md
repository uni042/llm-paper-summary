# Training Offload / Memory Systems

LLMの学習・fine-tuningでGPUメモリに収まりにくいactivation、optimizer state、parameter、その他tensorを**CPUメモリやNVMe SSDへ逃がし、必要な時だけ戻す**ことで、より大きなmodelやbatchを限られたGPUで学習する研究をまとめる。

単なるmemory節約だけでなく、GPU計算とI/Oを重ねる、tensorの寿命に合わせてoffload対象を選ぶ、storage側でoptimizer更新するなどして、offloadによるstallをどこまで隠せるかが主要な課題となる。

## 収録論文

収録論文: 11本。公開日が新しい順。

- 2026-04-29 — [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)
  - 複数のconsumer GPUを固定stageではなく使い回せるworkerとして扱い、layer計算を順番に割り振ってGPUの遊休時間と転送待ちを減らす。
- 2025-12-19 — [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)
  - 同じlayerのmicrobatchをまとめて処理してSSDとの往復回数を減らし、optimizer更新も次のiterationと重ねてI/O待ちを隠す。
- 2025-11-18 — [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)
  - tensorを再び使う価値と移動コストを見積もり、GPU・CPU・SSDのどこへ残すかを実行中に決める。
- 2025-09-02 — [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)
  - optimizer stateをGPU、DRAM、NVMe、並列file systemへ分散配置し、複数のI/O経路を同時に使って大規模pre-trainingのoffloadを高速化する。
- 2025-06-06 — [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)
  - 各tensorが次に必要になるまでの時間を見て、十分な猶予があるtensorだけをNVMeへ退避し、GPUとstorageを直接つないで転送する。
- 2025-05-29 — [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)
  - CPU側bufferの無駄を減らし、NVMeへ直接I/Oし、optimizerも低精度化することでSSD-offloaded fine-tuningのmemory使用量と速度を改善する。
- 2025-05-18 — [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)
  - 重要なgradientはGPUですぐ反映し、残りはCPU側で遅れて更新することで、optimizer stateのoffload待ちでGPUが止まる時間を減らす。
- 2024-08-19 — [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)
  - forwardで作ったactivationをNVMe SSDへ非同期に退避し、backwardで必要になる前に先読みしてGPU memoryを節約する。
- 2024-06-14 — [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)
  - CPUへ渡す更新情報を学習済みの疎な低次元表現へ圧縮し、転送量を減らしながらcommodity GPUでfine-tuningする。
- 2024-03-11 — [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)
  - optimizer stateをstorageからCPU / GPUへ毎回運ばず、SmartSSD側でoptimizer更新を行ってdata移動を減らす。
- 2023-10-13 — [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)
  - tensorがいつ使われ、どれだけ再利用されるかを基に、GPU memory・host memory・storage間の配置と移動を自動で決める。
