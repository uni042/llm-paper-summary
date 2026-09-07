# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、主に**model weightやMoE expert**をCPU memory、peer GPU HBM、SSD / Flashなどへ置き、必要な部分だけGPUへ移す、CPU/GPUで分担して計算する、storage側で計算する研究をまとめる。KV cache固有のoffloadは [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

## 収録論文

収録論文: 17本。公開日が新しい順。

- 2026-08-14 — [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)
  - 通常SSDより高帯域な将来型HBFをGPU / HBM近傍へ接続し、expert weightの直接転送とHBM buffer経由転送を並行して大容量MoEのI/O待ちを減らす。
- 2026-08-12 — [Who Should Own the Expert Cache? Kernel-Managed Tiering for Trillion-Parameter MoE Inference](2026-2608.12103-kernel-managed-expert-cache-tiering.md)
  - 1.45 TB expert poolでOS page cacheをDRAM tierとして評価し、kernel recencyと専用frequency cacheを比較する。
- 2026-06-24 — [Cache-Resident LLM Inference in GB-Scale Last-Level Caches](2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md)
  - GB級CPU LLCへweightを常駐させ、weight計算とattention/KVを別socketへ分けてcache pollutionとoperator同期costを減らす。
- 2026-05-18 — [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)
  - 複数microbatchから同じexpertへ来るtokenをまとめて大きなGEMMとして実行し、Intel AMX対応CPUとGPUへexpert計算を分担してoffloaded MoEのthroughputを高める。
- 2026-04-03 — [FluxMoE: Decoupling Expert Residency for High-Performance MoE Serving](2026-2604.02715-fluxmoe-decoupling-expert-residency.md)
  - expertを一時的なstreamed parameterとしてmaterializeし、GPU memoryをKV cacheへ優先配分する。
- 2026-01-30 — [Harvest: Opportunistic Peer-to-Peer GPU Caching for LLM Inference](2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md)
  - NVLink接続された別GPUの空きHBMを一時cacheとして使い、MoE expert weightやKV cacheをhost DRAMから戻すより速く再取得する。
- 2025-02-09 — [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)
  - 複数batchで共通利用されるexpertを先にGPUで計算し、その間に未常駐expertをCPU RAM / SSDから読み込んでI/O待ちを隠す。
- 2025-02-07 — [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)
  - iterationごとのrouting履歴とprompt類似性から次に必要なexpertを予測し、GPU cacheへの先読みで小VRAM時のweight転送待ちを減らす。
- 2024-11-18 — [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)
  - expert weightとKV cacheをCPU DRAMへ置き、weight転送・CPU attention・GPU MoE計算をmicrobatch間で重ねてI/O待ちを減らす。
- 2024-09-16 — [TwinPilots: A New Computing Paradigm for GPU-CPU Parallel LLM Inference](2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md)
  - Transformer演算ごとにCPU実行とGPU転送＋実行のcostを比較して配置を決め、CPU計算とPCIe転送を並行させる。
- 2024-05-29 — [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)
  - GPUにないexpert weightを運ばず、weightを置いた拡張memory device側でexpert計算を行って小さいactivationだけを転送する。
- 2024-03-02 — [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md)
  - GPUに載らないlinear weightの一部をCPUで直接計算し、残りのweight転送・GPU計算と並行してbatch=1のoffload latencyを減らす。
- 2024-02-10 — [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)
  - GPUに常駐しないexpertをCPUで直接計算し、重いexpert weight transferを小さいactivation転送へ置き換える。
- 2024-01-25 — [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)
  - request内で続きやすいexpert利用偏りをrouting履歴から予測し、再利用されそうなexpertをGPUへ残してprefetchする。
- 2023-12-28 — [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)
  - MoE expertをCPUへ置き、最近使ったexpertをGPUへ残すcacheと将来expertの先読みを組み合わせてPCIe待ちを減らす。
- 2023-12-12 — [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)
  - 直近tokenで使ったFFN weightをDRAMへ残し、必要なweightだけをFlashからまとまったreadで読み出してI/OとDRAM使用量を減らす。
- 2023-03-13 — [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md)
  - GPU・CPU DRAM・NVMe SSDを一つのmemory hierarchyとして扱い、weight・activation・KV cache配置と実行順を探索して単一GPUのbatch throughputを高める。
