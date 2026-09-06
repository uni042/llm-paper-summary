# Distributed / Heterogeneous MoE Training

収録論文: 5本。公開日が新しい順。

- 2025-08-18 — [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)
  - expert parallelism・通信・負荷分散を共同最適化してMoE trainingをHPCへ拡張する。
- 2025-04-28 — [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)
  - expert weightとoptimizer stateを分離し、動的配置変更時の状態移送を減らす。
- 2025-04-21 — [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)
  - data・tensor・expert・pipeline parallelismのmappingを柔軟に組み替える。
- 2025-04-04 — [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)
  - 性能の異なるGPUへattentionとexpertを非対称配置してtrainingを高速化する。
- 2023-04-08 — [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)
  - routing負荷に応じてexpertのGPU配置・複製数を動的変更する。
