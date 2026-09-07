# KV Cache Offload / Recomputation

local GPU HBMに収まらないKV cacheを**CPU DRAM・別GPUのHBM・storageなどへ置く、KVを使うattention計算をdataの近くへ移す、またはKVを運ぶ代わりに一部をGPUで作り直す**研究をまとめる。

`KV Cache Optimization / Compression` が「どのKVを残すか・どれだけ小さくするか」を主に扱うのに対し、この系統は**KVをlocal HBM以外へ置いたとき、どこから読み、どこでattentionを計算し、転送と再計算をどう使い分けるか**が中心課題である。

weightやexpert全般を含む汎用memory hierarchyは `Offload / Hierarchical Memory` に残し、KV cache固有の配置・attention実行場所・再計算を主題とする論文はこちらへ分類する。

## 収録論文

収録論文: 13本。公開日が新しい順。

- 2026-07-13 — [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md)
  - GH200の高速CPU-GPU接続を使い、KVをいったんGPUの作業用bufferへコピーせずCPU memory上に置いたままGPUから直接読み、読み出し単位やkernelを調整してremote memory accessを減らす。
- 2026-05-05 — [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md)
  - NVMe SSD上のKVを戻すI/O要求をCPUが大量に発行する構成をやめ、GPU自身が非同期SSD I/Oを制御してKVをまとめてHBMへ戻し、storage bandwidthを使い切りながらGPUのI/O待ちを減らす。
- 2026-01-28 — [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md)
  - requestごとのTTFT / TBTの遅れを見ながらKVをHBMとCPU DRAMの間で入れ替え、小さな転送をまとめて双方向のCPU-GPU帯域を使いやすくする。
- 2025-12-16 — [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md)
  - 再利用するKV量と新しくprefillするtoken量の比から「計算よりKV転送が遅くなる境界」を求め、実際のPCIe帯域では理論上の最大帯域を前提にした予測より早くI/O待ちが支配的になることを示す。
- 2025-07-01 — [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md)
  - 将来どのKVがattentionで使われるかを事前に知っている理想条件のsimulationで、KVをHBMと低速memoryへ動的に配置した場合の上限性能を測り、固定配置にどれだけ改善余地が残るかを評価する。
- 2025-06-03 — [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md)
  - CPU側でattentionするrequestとGPUだけで処理するrequestのlinear計算を一つのGPU batchへまとめ、CPU attentionの結果を待つ時点を遅らせてCPU処理とGPU計算を長く重ねる。
- 2025-01-03 — [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md)
  - 過去tokenの情報をKVそのものと、KVを再生成できる小さな中間activationの2形式で保存し、weight転送中にactivationからKVを作り直してPCIe転送量とGPU計算量のバランスを取る。
- 2024-11-26 — [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md)
  - CPU上のKVを全部GPUへ送らず、一部は小さいactivationだけを送りGPUでKVへ戻し、残りのKV転送と再計算を同時に進めてPCIe待ちを減らす。
- 2024-11-14 — [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md)
  - GH200の高速CPU-GPU接続を使い、各layerで必要になる少し前にKVをCPUからGPUへ先読みし、実行中の負荷を見ながらCPU側へ置くKV量を自動調整する。
- 2024-11-02 — [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md)
  - requestの一部だけdecode attentionとKVをCPUへ移し、GPU側requestと同時に処理しながら、その時のCPU / GPU負荷に応じてCPUへ回すrequest数を毎iteration変える。
- 2024-09-08 — [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)
  - KV cacheとdecode attentionを計算機能付きSSDの内部へ置き、flash内部でKVを読んでattentionまで処理することで、巨大なKVをstorageとGPUの間で往復させる転送を避ける。
- 2024-07-31 — [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md)
  - 同じ高速GPU間networkにつながった別GPUの空きHBMをKVの退避先として借り、CPU DRAMへ退避するより速くKVを戻せるようにして、実行中requestの一時退避を実用化する。
- 2024-03-18 — [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)
  - KV cacheとattentionを複数CPU nodeへ置き、GPUにはlinear / MLP計算を集中させることで、巨大なKVをCPUからGPUへ毎token転送する必要をなくし、大きなbatchでのthroughputを高める。

## 主な技術の分岐

- **KVのある場所でattentionする:** FastDecode / NEO / APEXはKVがあるCPUへattentionを寄せ、InstAttentionは同じ発想を計算機能付きSSDまで進める。
- **KV転送の一部を再計算へ置き換える:** KVPR / CAPTUREはKVそのものより小さいactivationを保存・転送し、GPUで必要なKVだけを作り直す。
- **別GPUの空きHBMを借りる:** Aquaは別GPUの余剰HBMを高速な退避先として使う。
- **使う直前にCPUからGPUへ先読みする:** Pieはlayerの実行順が分かっていることを利用し、必要になる前にKVをGPUへ戻して転送待ちを計算と重ねる。
- **高速memoryと低速memoryの間で置き場所を変える:** Fang et al.は、将来のKV利用を完全に知っている理想的な配置がどこまで速くなり得るかをsimulationで評価する。
- **SLOの遅れに応じてKVを入れ替える:** SuperInferはrequestごとのTTFT / TBT進捗を見て、HBMへ残すKVとCPU DRAMへ出すKVを変える。
- **CPU上のKVをコピーせず直接読む:** DirectKVは高速CPU-GPU接続を前提に、KVをCPUに置いたままGPUから読み出す。
- **SSDへのI/O制御をGPUへ移す:** TuttiはKV dataだけをdirect transferするのではなく、I/O requestの発行・管理もGPU側へ寄せ、多数の断片化したKVをNVMe SSDから戻す際のCPU bottleneckを避ける。
- **offloadが遅くなる条件を定量化する:** Meng et al.はKV量と実効CPU-GPU帯域から、計算よりKV転送待ちが支配的になる境界を求める。

実行場所やmemory tierは異なるが、共通して**KVをlocal GPU HBMだけへ固定すると容量や転送帯域が限界になる問題を避ける、またはその限界を定量化する**研究として扱う。
