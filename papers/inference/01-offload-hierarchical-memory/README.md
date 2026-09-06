# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、重みやexpertをCPUメモリ、SSD / Flashなどへ置き、必要な部分だけをGPUへ移す、またはGPU外で直接計算する研究をまとめる。単純に容量を増やすだけでなく、転送とGPU計算を重ねる、アクセス頻度に応じて配置を変える、storage側で計算するなどして、**メモリ容量とI/O待ちの両方を減らす**ことが中心課題となる。

CPU offload、KV-cache offload、通常のNVMe SSD、Computational Storage Drive、High-Bandwidth Flash、near-data processingなどは、同じ階層メモリ系でも移動するdata・帯域・遅延・実行場所が異なるため区別して扱う。

## 収録論文

収録論文: 14本。公開日が新しい順。

- 2026-08-14 — [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)
  - 高帯域Flashから必要なexpertをGPU / HBMへ直接送り、通常のNVMeより大きなMoEをI/O待ちを抑えて推論する。
- 2026-05-18 — [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)
  - expertへ送られたtokenを大きなまとまりに集約し、CPUとGPUへ分担して実行することで、重みをすべてGPUへ載せずにthroughputを高める。
- 2025-02-09 — [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)
  - 複数batchのGPU計算を利用して、GPUにないexpertをCPU / SSDから読み込む時間を隠し、巨大MoEのI/O待ちを減らす。
- 2025-02-07 — [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)
  - expertをより小さなblockに分割し、必要な部分だけをGPUへ読み込むことで、VRAM使用量と転送遅延のバランスを調整する。
- 2024-11-18 — [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)
  - expertの配置、CPUからの読み出し、GPU計算をpipeline化し、重みI/Oと計算を重ねて待ち時間を隠す。
- 2024-09-08 — [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)
  - KV cacheとdecode attentionをComputational Storage Drive内へ置き、flash内部帯域で処理してstorage↔GPUの巨大なKV転送を避ける。
- 2024-05-29 — [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)
  - storageの近くでexpert計算の一部を実行し、expert重みをGPUまで運ぶ量を減らして大規模MoEを推論する。
- 2024-03-18 — [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)
  - KV cacheとattention計算を複数CPU nodeへ置き、GPUにはlinear / MLP計算を集中させてKV転送を避けながら大batch throughputを高める。
- 2024-03-02 — [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md)
  - linear weightをCPU計算分とGPU計算分へ分け、CPU計算・weight転送・GPU計算を重ねることでbatch=1のoffload latencyを下げる。
- 2024-02-10 — [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)
  - GPUにないexpertは重みを転送せずCPU上で直接計算し、CPU-GPU間では小さいactivationだけを渡して転送量を減らす。
- 2024-01-25 — [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)
  - 同じsequenceでは使うexpertが偏りやすい性質を利用し、よく使うexpertをGPUへ残しながら次に必要なexpertを先読みする。
- 2023-12-28 — [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)
  - MoE expertをCPUへ置き、実際の利用頻度に応じたGPU cacheと先読みで必要な重み転送を減らす。
- 2023-12-12 — [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)
  - Flash上の重みからその時に必要な部分だけを読み出し、DRAM容量が小さい端末でも大きなLLMを実行できるようにする。
- 2023-03-13 — [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md)
  - weight・activation・KV cacheをGPU / CPU / SSDへ分散配置し、同じlayer weightを複数batchで使い回す計算順とI/O重畳で単一GPUのoffline throughputを高める。
