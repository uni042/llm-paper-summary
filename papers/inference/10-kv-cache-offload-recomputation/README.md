# KV Cache Offload / Recomputation

GPU HBMに収まらないKV cacheを**CPU DRAM・storageなどへ置く、KVを使うattention計算をdataの近くへ移す、またはKV転送の一部をGPU再計算へ置き換える**研究をまとめる。

`KV Cache Optimization / Compression` が「どのKVを残すか・どれだけ小さくするか」を主に扱うのに対し、この系統は**KVをGPU外へ置いたときのdata movementと実行場所**が中心課題である。CPU attention、in-storage attention、partial recomputation、activation checkpoint、zero-copy remote accessなど、KVを毎token HBMへ戻すcostを避ける手法を含む。

weight / expert全般のCPU・SSD offloadは `Offload / Hierarchical Memory` に残し、KV cache固有のplacement・attention execution・recomputationを主題とする論文はこちらへ分類する。

## 収録論文

収録論文: 8本。公開日が新しい順。

- 2026-07-13 — [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md)
  - GH200のNVLink-C2Cを使い、GPU kernelがCPU pinned memory上のKVをstaging bufferなしで直接読み、専用tilingとkernel fusionでremote-memory trafficを抑える。
- 2025-06-03 — [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md)
  - CPU/GPU requestのlinear計算を一つのGPU batchへまとめ、CPU attention結果の同期を遅らせてGPU処理と長く重ね、KV-cache offload時のCPU待ちを減らす。
- 2025-01-03 — [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md)
  - 過去tokenをKVと中間activationの2形式で混在保存し、weight転送中にactivationからKVを再生成してPCIe transferとGPU computeを釣り合わせる。
- 2024-11-26 — [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md)
  - CPU上のKVの一部を小さいactivationからGPUで再計算し、残りのKV転送と同時実行することでPCIe待ちをGPU computeへ置き換える。
- 2024-11-14 — [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md)
  - GH200の高速CPU-GPU接続を使い、KV cacheをlayer単位で先回りswapしながらGPU計算と重ね、online監視でCPU側へ拡張する容量を自動調整する。
- 2024-11-02 — [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md)
  - requestの一部だけdecode attentionとKV cacheをCPUへ移し、GPU側sub-batchと並行実行しながら毎iterationの負荷に応じてoffload量を変える。
- 2024-09-08 — [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)
  - KV cacheとdecode attentionをComputational Storage Drive内へ置き、flash内部帯域で処理してstorage↔GPUの巨大なKV転送を避ける。
- 2024-03-18 — [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)
  - KV cacheとattentionを複数CPU nodeへ置き、GPUにはlinear / MLP計算を集中させてKV転送を避けながら大batch throughputを高める。

## 主な技術の分岐

- **Compute-to-data:** FastDecode / NEO / APEXはKVがあるCPUへattentionを寄せる。InstAttentionは同じ発想をstorage内部へ進める。
- **Recompute instead of transfer:** KVPR / CAPTUREは、KVそのものを運ぶ代わりに小さいactivationを保持・転送しGPUで一部KVを再生成する。
- **Prefetch before use:** Pieはlayer access順序を利用し、CPU上のKVを必要になる前にGPUへswapして転送をcomputeで隠す。
- **Zero-copy remote access:** DirectKVは高速CPU-GPU interconnectを前提に、KVをCPUに置いたままGPU kernelから直接読む。

これらは実行場所こそ異なるが、共通して**KVを毎decode stepでGPU HBMへ完全にstageするcostを避ける**ことを目的とする。
