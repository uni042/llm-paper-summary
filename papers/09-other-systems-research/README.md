# その他システム研究

収録論文: 13本。公開日が新しい順。

- 2025-11-18 — [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)
  - GPU・CPU・SSD間でtensorの再利用価値と移動コストを見積もり、LLM学習のcache配置とmigrationを動的に最適化する方式。
- 2025-08-18 — [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)
  - 新しいMoE構造をHPCクラスタへ拡張するため、expert parallelism・通信・負荷分散を共同最適化する分散学習システム。
- 2025-06-06 — [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)
  - tensorの生存期間を基にNVMeオフロード対象とI/O時機を決め、GPUDirect StorageでLLM学習の転送待ちを抑える方式。
- 2025-05-29 — [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)
  - buffer fragmentation削減・direct NVMe I/O・低精度optimizerを組み合わせ、SSD-offloaded LLM fine-tuningの容量と速度を改善する方式。
- 2025-05-18 — [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)
  - 重要な勾配だけをGPUで即時更新し残りをCPUで非同期蓄積・更新して、LLM fine-tuningのoffload stallを抑える方式。
- 2025-04-28 — [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)
  - expert重みとoptimizer stateを分離し、動的なexpert複製・再配置時の状態移送を避けてMoE学習を効率化するシステム。
- 2025-04-21 — [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)
  - data・tensor・expert・pipeline parallelismを層や段階ごとにfoldし、通信量とメモリ制約へ柔軟に適応するMoE学習方式。
- 2025-04-04 — [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)
  - 高速GPUへattention、旧GPUへexpertを分離配置し、非対称割当てとpipelineで異種GPUのMoE学習を高速化する方式。
- 2025-02-27 — [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)
  - MoEのall-to-all通信をtile単位のGEMMと融合・重畳し、複数GPU学習／推論の通信待ちを隠すkernelランタイム。
- 2024-08-19 — [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)
  - 学習時activationをNVMe SSDへ非同期退避・先読みし、GPUDirect StorageでGPUメモリと再計算を減らすシステム。
- 2024-06-14 — [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)
  - 疎な低次元projected updateをCPUへオフロードし、layer-wise転送とGPU計算を重ねてconsumer GPUでLLM学習を可能にする手法。
- 2024-03-11 — [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)
  - SmartSSD上でoptimizer更新をnear-storage処理し、LLM学習のSSD–CPU／GPU間データ移動を削減する実機システム。
- 2023-04-08 — [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)
  - routing負荷に応じてexpertのGPU配置・複製数を動的に変え、token dropなしで分散MoE学習の不均衡を緩和するシステム。
