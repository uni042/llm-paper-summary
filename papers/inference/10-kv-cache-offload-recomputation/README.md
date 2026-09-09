# KV Cache Offload / Recomputation

local GPU HBMに収まらないKV cacheを**CPU DRAM・別GPUのHBM・storageなどへ置く、KVを使うattention計算をdataの近くへ移す、またはKVを運ぶ代わりに一部をGPUで作り直す**研究をまとめる。

`KV Cache Optimization / Compression` が「どのKVを残すか・どれだけ小さくするか」を主に扱うのに対し、この系統は**KVをlocal HBM以外へ置いたとき、どこから読み、どこでattentionを計算し、転送と再計算をどう使い分けるか**が中心課題である。

weightやexpert全般を含む汎用memory hierarchyは `Offload / Hierarchical Memory` に残し、KV cache固有の配置・attention実行場所・再計算を主題とする論文はこちらへ分類する。

## 主な技術の分岐

- **KVのある場所でattentionする:** FastDecode / NEO / APEXはKVがあるCPUへattentionを寄せ、InstAttentionは同じ発想を計算機能付きSSDまで進める。
- **CPU attentionを前倒ししてGPU待ちを隠す:** ScoutAttentionは次layerのCPU attentionを予測queryで早く開始する。
- **KV転送の一部を再計算へ置き換える:** KVPR / CAPTUREは小さいactivationからGPUでKVを作り直す。
- **別GPUの空きHBMを借りる:** Aquaは別GPUの余剰HBMを高速な退避先として使う。
- **使う直前にCPUからGPUへ先読みする:** Pieはlayer順、SpeCacheは次tokenのattention予測を使ってKV転送を計算と重ねる。
- **CPU上のKVを検索する:** RetroInfer / ParisKVは全KVを戻さず必要subsetだけを選択する。
- **SSDへのI/O制御をGPUへ移す:** TuttiはI/O request発行・管理をGPU側へ寄せる。
- **複数SSDの帯域を束ねる:** Swarmは同時参照KVを複数SSDへ分散する。
- **attention sparsityと3階層storageを協調させる:** KVDriveはHBM/DRAM/SSDの配置とselection/fetch/computeをpipeline化する。

実行場所やmemory tierは異なるが、共通して**KVをlocal GPU HBMだけへ固定すると容量や転送帯域が限界になる問題を避ける、またはその限界を定量化する**研究として扱う。

<!-- survey:auto:start -->
## 自動生成の論文一覧（25本）

| 論文 | 一文要約 |
|---|---|
| [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](2026-2609.04852-kvmem-virtualizing-million-token-agent-workspaces.md) | GPU・CPU DRAM・NVMeへ退避した過去のKV状態をattention空間の索引で検索し、必要blockだけを現在のcontextへ再構成することで、consumer GPU上でnative contextを超えるagent workspaceを扱うKV virtualization system。 |
| [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md) | GH200でCPU DRAM上のKV cacheをGPU HBMへ一度コピーせず、GPUのattention kernelから直接読み、同じCPU側dataを何度も読まないよう計算順序とkernelを作り直すzero-copy KV offload system。 |
| [SwiftCache: Efficient LLM Serving for Multi-turn Conversations with Heterogeneous KV Cache Sharing](2026-2606.16135-swiftcache-heterogeneous-kv-cache-sharing.md) | 同一serverでKV需要が低い別modelの空きHBMへprefix KVをNVLink経由で退避し、local GPUには実行中layerのKVだけを流し込んで、multi-turn servingの再読込待ちと文脈長制約を減らす。 |
| [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md) | GH200のHBMが混雑したとき、応答開始やtoken間隔の目標に遅れそうなrequestを優先してKV cacheをCPU DRAMとの間で入れ替え、小さいKV blockをまとめて双方向転送することで高速C2C linkを使い切るonline serving system。 |
| [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md) | CPUから戻すcached KVの量が、新しく計算するprefill token量に対してどれくらい増えるとPCIe転送の方がGPU計算より遅くなるかを式とH100実測で示し、prefix reuseが多いほどKV offloadが早くI/O律速になることを分析した研究。 |
| [LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference](lmcache.md) | 未記録 |
| [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md) | 頻繁に参照されるKVを高速HBM、そうでないKVを大容量DRAMへ置く配置問題をモデル化し、未来のattention参照先を完全に知る理想条件との比較から、実用schedulerにどれだけ改善余地が残るかを測るsimulation研究。 |
| [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md) | 一部requestのKV cacheとdecode attentionをCPUへ移しつつ、attention前のlinear計算はCPU/GPU向けrequestを一つのGPU batchでまとめ、CPU結果を必要になる直前まで待たないことでCPU attentionをGPU計算の裏へ隠す方式。 |
| [HeadInfer: Memory-Efficient LLM Inference by Head-wise Offloading](2025-2502.12574-headinfer-head-wise-kv-offloading.md) | KVキャッシュをlayer単位より細かいattention head単位でCPU RAMへ退避し、GPUには同時に使うheadだけを置いて、近似なしの超長文脈推論を小容量GPUで可能にする。 |
| [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md) | 過去tokenを、すぐ使えるKVそのものと、K/Vを作る前のより小さい中間activationの2形式で混在保存し、weight転送中にactivationからKVを再生成してPCIe転送量とGPU再計算量を釣り合わせる方式。 |
| [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md) | CPU上のKV cacheを全部GPUへ戻さず、一部はより小さい中間activationだけを送りGPUでK/Vを作り直し、残りのKV転送と同時に進めてPCIe待ちを減らす方式。 |
| [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md) | 一部のKV cacheをCPU DRAMへ置き、使う数layer前にGPUへ戻して転送を現在layerの計算と重ね、GPUを待たせない範囲までoffload量を自動で増やすKV-cache offload system。 |
| [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md) | 一部requestだけKV cacheとdecode attentionをCPUへ移し、残りrequestはGPUで処理しながら、CPU/GPUが同時に終わるようoffload量を毎iteration調整してVRAM不足を緩和するonline serving system。 |
| [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md) | KV cacheを計算機能付きSSD内へ置き、decode attentionもSSD内部で実行することで、巨大なKVをSSDからGPUへ毎token読み戻す転送を避けるlong-context推論system。 |
| [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md) | 同じNVLink / NVSwitch接続内で余っている別GPUのHBMを、KV cacheなどの一時退避先として借り、CPU DRAMへ退避するより高速にrequestを入れ替えて公平なonline servingを行うmemory system。 |
| [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md) | KV cacheとそれを読むattention計算を複数CPU nodeへ置き、GPUにはmodel weightを使う計算を集中させることで、KV転送を避けながら大batchでGPU throughputを高めるheterogeneous serving system。 |
| [Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap](elastic-kv-cache.md) | prefill activation reserveをdecode中だけKVへ貸すCUDA VMM機構を実装しつつ、small chunkでもTTFTがほぼ悪化せず単純なchunk縮小の方が有利というnegative resultを示す。 |
| [Learning Agent Execution for KV-Cache Management in Agentic Serving](cachescout.md) | CacheScoutはagent実行遷移をオンライン学習し、再利用されやすい固定文脈KVを予測的に保持・事前取得するvLLM上のruntime。 |
| [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md) | GPU HBM・CPU DRAM・NVMe SSDの3階層へKV cacheを置き、**直近のattentionで再利用されそうなKVだけをGPUへ残すこと、必要KVの選択・転送・GPU計算を小さなbatch単位で並行実行すること、SSDから必要blockだけを疎に読むこと**を組み合わせ、長contextでKV全体を毎回転送するI/O待ちを減らす。 |
| [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md) | NVMe SSD上へ退避したKV cacheを戻す際、CPUが大量の小さなI/O要求を発行する従来方式をやめ、GPU自身がSSDへの非同期I/Oを制御してKVをまとめて転送することで、SSD容量を使いながらDRAM-backed cacheに近い推論性能を狙うsystem。 |
| [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md) | 長contextのKV cacheの大部分をCPU DRAMへ置きながら、GPUにある重要blockはGPU、CPUにしかない重要blockだけはCPUでattentionを計算し、さらに**次layerでCPUが担当するattentionを1 layer早く開始する**ことで、KV転送待ちとCPU計算待ちの両方を減らす。 |
| [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md) | attentionで一緒に参照されやすいKV cacheを事前にまとめ、そのグループ内のKVを複数SSDへ分散配置することで、1回のKV読み出しを複数SSDから並列に行い、単一SSDの帯域上限を超える実効I/O帯域を得る方式。 |
| [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md) | full-precisionのKV cacheをCPU DRAMへ置いたまま、GPU上の小さなkey要約だけで現在のqueryに重要なtokenを二段階検索し、選ばれたKVだけをGPUからCPU memoryへ直接読みに行くことで、長い生成中に検索indexが古くなる問題とCPU検索・CPU主導転送の待ち時間を同時に減らすKV retrieval system。 |
| [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md) | 長contextのKV cacheをCPU memory上の**vector storageとして検索対象にし、attentionに重要なtokenだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するmemory容量とbandwidthを減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論system。 |
| [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md) | full-precision KV cacheをCPU DRAMへ保持し、GPUには低bitのKV要約を置いて毎decode stepで重要KVだけを選び、**次tokenで必要になりそうなKVを1 step先読みしてCPU→GPU転送と現在の計算を重ねる**ことで、情報を捨てずに長contextのVRAM使用量を減らす。 |
<!-- survey:auto:end -->
