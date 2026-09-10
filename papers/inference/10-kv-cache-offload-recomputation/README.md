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
## 自動生成の論文一覧（30本）

| 論文 | 一文要約 |
|---|---|
| [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](2026-2609.04852-kvmem-virtualizing-million-token-agent-workspaces.md) | 長時間agentの履歴をtextへ戻して要約・再prefillするのではなく、計算済みKVをGPU・CPU DRAM・NVMeへpageとして保持し、現在queryに関連するblockだけをnative context内の実行viewへ戻すKV-context virtualization system。logical workspace sizeと、その時GPUがattentionするactive context sizeを分離する。 |
| [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md) | GH200でCPU DRAM上のKV cacheをGPU HBMへ一度コピーせず、GPUのattention kernelから直接読み、同じCPU側dataを何度も読まないよう計算順序とkernelを作り直すzero-copy KV offload system。 |
| [SwiftCache: Efficient LLM Serving for Multi-turn Conversations with Heterogeneous KV Cache Sharing](2026-2606.16135-swiftcache-heterogeneous-kv-cache-sharing.md) | 複数modelを同一serverへ載せる環境で、KV需要が小さいmodelの空きHBMを長文会話modelへ貸し、prefix KVをCPU/SSDではなくNVLink接続peer GPUへ置く協調cache system。さらにmaster側は現在layerのKVだけをlocal bufferへstreamし、worker側はblock-major layoutで貸出容量をO(1)に伸縮することでTTFTと最大context長を改善する。 |
| [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md) | GH200のHBMが混雑したとき、応答開始やtoken間隔の目標に遅れそうなrequestを優先してKV cacheをCPU DRAMとの間で入れ替え、小さいKV blockをまとめて双方向転送することで高速C2C linkを使い切るonline serving system。 |
| [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md) | CPUから戻すcached KVの量が、新しく計算するprefill token量に対してどれくらい増えるとPCIe転送の方がGPU計算より遅くなるかを式とH100実測で示し、prefix reuseが多いほどKV offloadが早くI/O律速になることを分析した研究。 |
| [LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference](2025-2510.09665-lmcache.md) | vLLM/SGLang内部でrequestごとに閉じていたKV cacheを独立したstorage/communication layerとして外へ取り出し、query間のprefix reuseとprefill-decode間のKV transferを同じ基盤で扱う。小pageを大粒度chunkへ束ねるCUDA data path、layer-wise compute-I/O overlap、zero-copy、標準connectorとcontrol APIでGPU・CPU・disk・networkを跨ぐKV移動を高速化する。 |
| [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md) | 頻繁に参照されるKVを高速HBM、そうでないKVを大容量DRAMへ置く配置問題をモデル化し、未来のattention参照先を完全に知る理想条件との比較から、実用schedulerにどれだけ改善余地が残るかを測るsimulation研究。 |
| [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md) | 一部requestのKV cacheとdecode attentionをCPUへ移しつつ、attention前のlinear計算はCPU/GPU向けrequestを一つのGPU batchでまとめ、CPU結果を必要になる直前まで待たないことでCPU attentionをGPU計算の裏へ隠す方式。 |
| [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md) | 長いcontextで増え続けるKV cacheの16-bit正本をCPU DRAMへ退避し、GPUには重要KVを探すための1/2-bitコピーと少数の16-bit KVだけを置く。さらに現在tokenと『次tokenの参照先を予測するための投機token』を同時に計算し、次stepで必要になりそうな16-bit KVを1 step早くCPUからGPUへ先読みすることで、VRAM削減とCPU-GPU転送待ちの隠蔽を両立する。 |
| [HeadInfer: Memory-Efficient LLM Inference by Head-wise Offloading](2025-2502.12574-headinfer-head-wise-kv-offloading.md) | 従来のlayer単位KV offloadをさらにattention head単位まで細分化し、CPU DRAMに全KV正本を保持しながらGPUには現在計算するhead groupのKVだけを置くlossless long-context inference方式。chunked prefillでactivation peakを抑え、ping-pong bufferで次headのPCIe transferを現在headのattention計算へ重ね、context長に応じてhead group数を変えて容量とkernel/transfer overheadを両立する。 |
| [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md) | 過去tokenを、すぐ使えるKVそのものと、K/Vを作る前のより小さい中間activationの2形式で混在保存し、weight転送中にactivationからKVを再生成してPCIe転送量とGPU再計算量を釣り合わせる方式。 |
| [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md) | CPU上のKV cacheを全部GPUへ戻さず、一部はより小さい中間activationだけを送りGPUでK/Vを作り直し、残りのKV転送と同時に進めてPCIe待ちを減らす方式。 |
| [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md) | 一部のKV cacheをCPU DRAMへ置き、使う数layer前にGPUへ戻して転送を現在layerの計算と重ね、GPUを待たせない範囲までoffload量を自動で増やすKV-cache offload system。 |
| [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md) | 一部requestだけKV cacheとdecode attentionをCPUへ移し、残りrequestはGPUで処理しながら、CPU/GPUが同時に終わるようoffload量を毎iteration調整してVRAM不足を緩和するonline serving system。 |
| [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md) | KV cacheを計算機能付きSSD内へ置き、decode attentionもSSD内部で実行することで、巨大なKVをSSDからGPUへ毎token読み戻す転送を避けるlong-context推論system。 |
| [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md) | 同じNVLink / NVSwitch接続内で余っている別GPUのHBMを、KV cacheなどの一時退避先として借り、CPU DRAMへ退避するより高速にrequestを入れ替えて公平なonline servingを行うmemory system。 |
| [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md) | KV cacheとそれを読むattention計算を複数CPU nodeへ置き、GPUにはmodel weightを使う計算を集中させることで、KV転送を避けながら大batchでGPU throughputを高めるheterogeneous serving system。 |
| [CacheBridge: Efficient Cross-Model KV Cache Transfer](2026-2609.00891-cachebridge.md) | 同じ長い入力を別のLLMへ引き継ぐと、通常は新しいモデルが最初からprefillして自分用のKVキャッシュを作り直す必要がある。CacheBridgeは元モデルのKVから受信モデルのKVを線形変換で近似し、この再計算を避ける。各KV headを全headから予測する従来法を対応headだけへ限定し、生成品質に効く誤差をattention感度で重く学習し、変換係数の構築もGPU上で融合することで、品質を保ちながら変換器の容量・適用時間・構築時間を削減する。 |
| [Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap](2026-2608.23658-elastic-kv-cache.md) | vLLMは大きなprefillに備えて一時activation用GPUメモリを常時予約するため、decode中はその領域が遊ぶ。Elastic KV CacheはCUDA仮想メモリを使い、decode中だけその予約領域をKV cacheへ貸し、prefill直前に返す機構を実装する。しかし実験ではprefill chunkを小さくする単純設定でもほぼ同じTTFTでより多くKVを確保でき、複雑なelastic機構の実用上の優位を見つけられなかったというnegative resultが中心。 |
| [Learning Agent Execution for KV-Cache Management in Agentic Serving](2026-2608.14624-cachescout.md) | 複数のLLMエージェントを順番に呼ぶシステムでは、各エージェント固有のsystem promptやtool定義が何度も再利用される。CacheScoutは『今のエージェントの次に誰が呼ばれやすいか』を実行履歴から軽量に学習し、近く再利用されそうなエージェントの固定prefix KVをGPUに残し、空き時間には次候補のKVを先に作ることで再prefillを減らす。 |
| [Heterogeneous LLM Serving with General-Purpose Processing-Near-Memory for Retrieval-Based Sparse Attention](2026-2608.03555-karat-pnm-retrieval-sparse-attention.md) | 100万トークン級の長文で検索型疎注意を使うLLMでは、毎ステップ読むKV量は減っても全KVキャッシュと索引キーの保存容量は減らない。KARATはKVと索引を大容量LPDDR搭載の汎用処理近傍メモリへ移し、GPUを重み・MoE計算へ専念させ、異種デバイス間をマイクロバッチでパイプライン化することで、同一電力制約下の同時実行数とデコード処理量を高める。 検索型疎注意は、各デコードステップで全履歴から重要な上位kトークンだけを選んで注意計算するため、KV読み出し量を全長Lからkへ減らせる。 |
| [DualDecoder: Accelerate Long Context LLM Inference by Predictive Prefetch](2026-2607.26475-dualdecoder-predictive-prefetch.md) | 長文LLMで疎なKVキャッシュだけをGPUへ読み込む方式は、KV本体を減らしても検索や再構成に使う補助状態を全層分GPUへ常駐させるため、実際のメモリ節約が小さくなりやすい。DualDecoderは、直前に投機生成したトークンから次トークンが参照しそうなKV位置を予測し、層ごとの計算より先にCPUメモリから必要KVを転送する。GPU側は現在計算中と次に転送する2層分だけを保持するため、補助バッファも全層常駐から定数規模へ縮小できる。ShadowKV上の8GPU実機評価で、128K文脈のQwen2.5-32BではShadowKV比2.62倍のデコードスループットを示し、GPUメモリを最大36.4%削減する。 |
| [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md) | GPU HBM・CPU DRAM・NVMe SSDの3階層へKV cacheを置き、**直近のattentionで再利用されそうなKVだけをGPUへ残すこと、必要KVの選択・転送・GPU計算を小さなbatch単位で並行実行すること、SSDから必要blockだけを疎に読むこと**を組み合わせ、長contextでKV全体を毎回転送するI/O待ちを減らす。 |
| [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md) | NVMe SSD上へ退避したKV cacheを戻す際、CPUが大量の小さなI/O要求を発行する従来方式をやめ、GPU自身がSSDへの非同期I/Oを制御してKVをまとめて転送することで、SSD容量を使いながらDRAM-backed cacheに近い推論性能を狙うsystem。 |
| [CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration](2026-2604.25080-cacheflow.md) | 以前処理した長いprefixのKVキャッシュがGPU外に退避されているとき、全部をI/Oで戻すか全部を再計算するかの二択にせず、prefixの一部はGPUで再計算し、別部分は外部メモリから読み戻して同時進行させる手法。さらにこの分担をトークン方向だけでなく層方向・複数GPU方向にも広げ、同じバッチ内の複数要求がGPU計算資源とI/O帯域を奪い合う状況までまとめてスケジュールする。 |
| [HybridGen: Efficient LLM Generative Inference via CPU-GPU Hybrid Computing](2026-2604.18529-hybridgen-efficient-llm-generative-inference-via-cpu-gpu-hybrid-computing.md) | 長文生成では巨大化したKVキャッシュをCPUへ退避すると転送量が増え、CPU側で注意機構を計算すると今度はCPU計算が律速になる。HybridGenはKVキャッシュをCPU側とGPU側へ分け、各側が手元のKVに対する注意スコアを並列計算し、GPUで結合・正規化する。さらにCPUが次層の計算を投機的に先行し、実行時フィードバックでCPU処理トークン数と選択方式を切り替え、KベクトルをDRAM、VベクトルをCXL拡張メモリへ配置することで、CPU計算・PCIe転送・GPU計算を重ね合わせる。A100/H100/RTX 5090実機で既存のKV選択・退避方式に対し平均最大1.41〜3.2倍の速度向上を報告する。 |
| [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md) | 長contextのKV cacheの大部分をCPU DRAMへ置きながら、GPUにある重要blockはGPU、CPUにしかない重要blockだけはCPUでattentionを計算し、さらに**次layerでCPUが担当するattentionを1 layer早く開始する**ことで、KV転送待ちとCPU計算待ちの両方を減らす。 |
| [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md) | attentionで一緒に参照されやすいKV cacheを事前にまとめ、そのグループ内のKVを複数SSDへ分散配置することで、1回のKV読み出しを複数SSDから並列に行い、単一SSDの帯域上限を超える実効I/O帯域を得る方式。 |
| [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md) | full-precisionのKV cacheをCPU DRAMへ置いたまま、GPU上の小さなkey要約だけで現在のqueryに重要なtokenを二段階検索し、選ばれたKVだけをGPUからCPU memoryへ直接読みに行くことで、長い生成中に検索indexが古くなる問題とCPU検索・CPU主導転送の待ち時間を同時に減らすKV retrieval system。 |
| [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md) | 長contextのKV cacheをCPU memory上の**vector storageとして検索対象にし、attentionに重要なtokenだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するmemory容量とbandwidthを減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論system。 |
<!-- survey:auto:end -->
