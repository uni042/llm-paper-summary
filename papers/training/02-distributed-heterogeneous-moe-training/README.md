# Distributed / Heterogeneous MoE Training

MoEを多数GPUへ分散して学習するときの**expert配置、複製数、通信、parallelism、GPU性能差による負荷偏り**を扱う研究をまとめる。MoEではtokenごとに使うexpertが変わるため、dense modelよりもGPU間通信とload imbalanceが大きくなりやすい。

そのため、routing負荷に応じてexpertを移動・複製する、dense部分とexpert部分で異なるparallelismを使う、性能の違うGPUへ役割を分けるなどして、大規模MoE trainingのthroughputとhardware利用率を高める。

## 収録論文

収録論文: 5本。公開日が新しい順。

- 2025-08-18 — [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)
  - 新しいMoE構造をHPC clusterへ載せるため、expertの分散方法、GPU間通信、負荷分散をまとめて最適化する。
- 2025-04-28 — [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)
  - expert weightとoptimizer stateの置き場所を切り離し、expertを別GPUへ移動・複製しても大きなoptimizer stateまで一緒に移さずに済むようにする。
- 2025-04-21 — [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)
  - dense部分とMoE部分でdata / tensor / expert / pipeline parallelismの組み合わせを変え、通信量とmemory使用量を抑える。
- 2025-04-04 — [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)
  - 高速GPUへattention、低速GPUへexpertを多めに割り当てるなど、性能の異なるGPUへ非対称に仕事を配置して全体の待ち時間を減らす。
- 2023-04-08 — [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)
  - routingで混雑したexpertを別GPUへ移したり複製したりして、特定GPUへtoken処理が偏るのを動的に緩和する。
