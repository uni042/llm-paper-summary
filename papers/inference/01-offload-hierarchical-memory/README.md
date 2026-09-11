# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、主に**model weightやMoE expert**をCPU memory、peer GPU HBM、SSD / Flashなどへ置き、必要な部分だけGPUへ移す、CPU/GPUで分担して計算する、storage側で計算する研究をまとめる。KV cache固有のoffloadは [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（34本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-04 | [FluxMoE: Decoupling Expert Residency for High-Performance MoE Serving](2026-2604.02715-fluxmoe-decoupling-expert-residency.md) | ✓ | 3 | FluxMoEは、MoEのエキスパート重みを「モデルを読み込みしたらsession終了までGPUに居続ける静的パラメータ」とみなす前提を崩す。 |
| 2026-06 | [WiSP: A Working-Set View of Mixture-of-Experts Serving on Extremely Low-Resource Hardware](2026-2606.21868-wisp-working-set-moe-serving-low-resource-hardware.md) | [✓](https://github.com/nokia-applied-research/WiSP) | 1 | 低並列の混合専門家モデル（Mixture of エキスパート; MoE）推論では、全エキスパート重みをGPUへ常駐できない一方、各トークンが実際に使うエキスパートは一部だけである。 |
| 2026-02 | [DALI: A Workload-Aware Offloading Framework for Efficient MoE Inference on Local PCs](2026-2602.03495-dali-workload-aware-moe-offloading-local-pcs.md) | ✓ | 1 | GPUメモリに全エキスパートを置けないローカルPCで混合専門家モデル（Mixture of エキスパート; MoE）を実行すると、CPUとGPUの固定分担では入力ごとに変動するエキスパート負荷へ追随できず、PCIe転送も待ち時間になりやすい。 |
| 2025-12 | [Context-Aware Mixture-of-Experts Inference on CXL-Enabled GPU-NDP Systems](2025-2512.04476-context-aware-moe-cxl-ndp.md) | ✓ | 1 | GPUメモリに収まらない混合専門家モデル（Mixture of エキスパート; MoE）では、外部メモリから巨大なエキスパート重みを毎回GPUへ運ぶとPCIe転送が支配的になる。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [Who Should Own the Expert Cache? Kernel-Managed Tiering for Trillion-Parameter MoE Inference](2026-2608.12103-kernel-managed-expert-cache-tiering.md) | ✓ | 0 | この論文が問うのは「LRUとLFUのどちらが良いか」より一段上の問題である。巨大MoEのエキスパートキャッシュを誰が所有すべきか、すなわちLLMランタイムがエキスパート単位の専用キャッシュを自前実装するべきか、それともLinuxカーネルがすでに持つページキャッシュをDRAM階層として利用すべきかを実機で比較する。 |
| 2026-08 | [SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning](2026-2608.21614-saem-stage-aware-expert-management-cot.md) | ✓ | 0 | 長い連鎖思考（Chain-of-Thought; CoT）では同じ推論段階のあいだに似たエキスパート集合が繰り返し使われる一方、トークン単位のLRU型キャッシュは細かなルーティング変動のたびに重みを入れ替え、PCIe転送とキャッシュスラッシングを増やす。 |
| 2026-08 | [Potential Applications of HBF in LLM Serving Systems](2026-2608.13127-hbf-llm-serving.md) | ✓ | 0 | 本論文は、LLM提供でHBMの帯域だけでなく容量が主要制約になりつつあることに着目し、SanDiskが提案するHigh-帯域 Flash（HBF）をGPUメモリ階層へ追加する場合のアーキテクチャとシステム上の使い道を整理する。 |
| 2026-08 | [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md) | ✓ | 0 | DASHは、将来の HBF（High-帯域 フラッシュ） をGPU近傍の大容量メモリとして使うMoE向け構成である。 |
| 2026-06 | [Cache-Resident LLM Inference in GB-Scale Last-Level Caches](2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md) | ✓ | 0 | GB級のCPU last-レベルキャッシュへモデル重みを常駐させ、重み計算と注意機構/KV状態を別ソケットへ分離し、コア局所な配置と細粒度同期でDRAM往復と演算子バリアを減らすCPU LLM inferenceシステム。 |
| 2026-05 | [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md) | ✓ | 0 | CoX-MoEは、オフロード MoE 提供でエキスパート重み 転送だけでなく、エキスパートごとのGEMMが小さ過ぎてCPU/GPUの行列演算器を十分使えないことを問題にする。 |
| 2026-04 | [NVLLM: A 3D NAND-Centric Architecture Enabling Edge on-Device LLM Inference](2026-2604.25699-nvllm-3d-nand-centric-edge-inference.md) | ✓ | 0 | 端末上でDRAM容量を超えるLLMを動かす場合、SSDからFFN重みを毎トークン読み戻す方式はPCIe帯域とデータ移動が支配的になり、GPUやNPUの演算器を十分に使えない。 |
| 2026-04 | [DAK: Direct-Access-Enabled GPU Memory Offloading with Optimal Efficiency for LLM Inference](2026-2604.26074-dak-direct-access-gpu-memory-offloading.md) | [✓](https://github.com/shouxulin/DirectAccessKernel) | 0 | 従来のLLMメモリオフロードはCPU側の重みやKVキャッシュを一度GPU HBMへ先読みしてから計算するため、転送書き込みと計算中のHBM読み出しが競合し、先読み用バッファもHBM容量を消費する。 |
| 2026-01 | [Harvest: Opportunistic Peer-to-Peer GPU Caching for LLM Inference](2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md) | ✓ | 0 | Harvestは、GPUメモリ不足時のオフロードを「計算中GPUのHBMかホスト DRAMか」の二択にせず、NVLinkで接続された別GPUの余っているHBMを中間の一時キャッシュとして使う研究である。 |
| 2026-01 | [FlashMoE: Reducing SSD I/O Bottlenecks via ML-Based Cache Replacement for Mixture-of-Experts Inference on Edge Devices](2026-2601.17063-flashmoe-ssd-io-cache-replacement.md) | ✓ | 0 | FlashMoEが対象にするのは、GPUのVRAMだけでなくCPUのDRAMにもモデル全体を置けない個人PC級の環境で、大規模な混合専門家モデル（Mixture of 専門家; MoE）を動かすという問題である。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2023-03 | [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md) | [✓](https://github.com/FMInference/FlexGen) | 108 | FlexGenが対象にするのは、chatのように1 リクエストの応答をすぐ返す用途ではなく、ベンチマーク、情報抽出、文書処理のような多少待ってもよい代わりに、多数のリクエストをできるだけ安く処理したい生成処理である。 |
| 2024-01 | [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) | [✓](https://github.com/EfficientMoE/MoE-Infinity) | 41 | MoE-Infinityは、個人PCで典型的なバッチ=1・単一ユーザーのデコードでは、同じリクエストの中で使われるエキスパートの組み合わせに偏りが続きやすいことを利用するMoE inference システムである。 |
| 2024-02 | [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md) | [✓](https://github.com/efeslab/fiddler) | 32 | Fiddlerは、GPUキャッシュ ミスしたエキスパートについて、重みをGPUへ運ぶか、活性値だけCPUへ送りCPUでエキスパートを計算するかを実行時に選ぶMoE 推論 システムである。 |
| 2023-12 | [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md) | [✓](https://github.com/dvmazur/mixtral-offloading) | 32 | Fast Inference of MoE withオフロード（実装名 Mixtral-オフロード）は、Mixtral-8x7Bの巨大なエキスパート重みをCPU DRAMへ置き、必要なエキスパートだけGPUへ移すことで、12〜16 GB級VRAMでもMoEを動かす方式を実装した研究である。 |
| 2023-12 | [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md) | ✓ | 27 | LLM in a Flashは、DRAMにモデル全体を保持できない端末で、モデル重みをフラッシュストレージへ置き、各トークンで必要なFFN部分だけをDRAMへ読み込む重みストリーミング方式である。 |
| 2024-03 | [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md) | ✓ | 14 | HeteGenは、GPU メモリにモデル全体が収まらない状況で、CPUを単なる重み置き場にせず計算資源としても同時利用するLLM inference システムである。 |
| 2025-02 | [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md) | [✓](https://github.com/IntelliSys-Lab/FineMoE-EuroSys26) | 13 | fMoE（改訂版では FineMoE）は、エキスパート重み本体をCPU DRAMへ置き、GPU側の小さなエキスパートキャッシュを反復単位のルーティング履歴とプロンプトの意味的類似性で制御するMoE 提供 システムである。 |
| 2025-02 | [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md) | [✓](https://openi.pcl.ac.cn/fangzhy/Klotski) | 11 | Klotskiは、GPU VRAMにエキスパート重みが収まらないMoEで、複数バッチを同時に流してGPU計算時間を長くし、その間にCPU RAM / SSDから次エキスパートを読むことでGPUがI/Oを待つ時間を減らす推論engineである。 |
| 2024-09 | [TwinPilots: A New Computing Paradigm for GPU-CPU Parallel LLM Inference](2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md) | ✓ | 11 | TwinPilotsは、GPUメモリにLLM全体が収まらない環境で、CPUを単なるパラメータ置き場ではなくGPUと並列に動く計算主体として使う推論システムである。 |
| 2025-02 | [Memory Offloading for Large Language Model Inference with Latency SLO Guarantees](2025-2502.08182-select-n-slo-aware-memory-offloading.md) | ✓ | 2 | Select-Nは、GPUに残すモデル状態量とCPU側ホストメモリへの退避量を、遅延サービス水準目標（service-level objective: SLO）を守りながら動的に調整するLLM推論システムである。 |
| 2024-11 | [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md) | [✓](https://github.com/caoshiyi/artifacts/tree/asplos25) | 2 | MoE-Lightningは、低VRAM GPUで多数リクエストをまとめて処理する オフライン / バッチ-指向 提供 を主対象にする。 |
| 2025-06 | [eLLM: Elastic Memory Management Framework for Efficient LLM Serving](2025-2506.15155-ellm-elastic-memory-management.md) | ✓ | 1 | LLMサービングで活性値とKVキャッシュを別々の固定メモリ領域として管理すると、片方が空いていても他方へ融通できずGPUメモリが遊ぶ問題に対し、仮想テンソル抽象で両者を同じ物理プールへ載せ、GPU内で領域を動的に貸し借りし、さらにCPUメモリを弾性的な退避先として使う推論基盤。 |
| 2025-08 | [SSD Offloading for LLM Mixture-of-Experts Weights Considered Harmful in Energy Efficiency](2025-2508.06978-ssd-moe-offloading-energy-efficiency.md) | [✓](https://github.com/scale-snu/SSD-offloading) | 0 | MoEの専門家重みをSSDへ退避すると容量不足と転送遅延は扱いやすくなる一方、NAND Flashの読み出しエネルギーがHBMやCPU側DRAMより大幅に高い。 |
| 2025-06 | [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md) | ✓ | 0 | 一部リクエストのKV キャッシュとデコード 注意機構をCPUへ移し、CPU/GPU向けリクエストをまとめて実行しながらCPU処理をGPU計算へ重ね、メモリ制約下のonline推論スループットを高める方式。 |
| 2025-01 | [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md) | [✓](https://github.com/casys-kaist/Capture) | 0 | 過去トークンをKVそのものと、K/Vを作る前の中間活性値の2形式で混在保存し、重み転送中に活性値からKVを再生成して転送量と再計算量を釣り合わせる方式。 |
| 2024-11 | [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md) | [✓](https://github.com/NEO-MLSys25/NEO) | 0 | 一部リクエストのKV キャッシュとデコード 注意機構をCPUへ移し、残りリクエストはGPUで処理しながらCPU/GPUを非対称に重ね、VRAM不足を緩和するonline serving システム。 |
| 2024-11 | [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md) | [✓](https://github.com/chaoyij/KVPR) | 0 | CPU上のKV キャッシュを全部GPUへ戻さず、一部は中間活性値からGPUでK/Vを作り直し、残りのKV転送と同時に進めてPCIe待ちを減らす方式。 |
| 2024-09 | [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md) | ✓ | 0 | KV キャッシュを計算機能付きSSD内へ置き、デコード 注意機構もSSD内部で実行することで、巨大なKVをSSDからGPUへ毎回読み戻す転送を避ける長文脈推論システム。 |
| 2024-05 | [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md) | ✓ | 0 | MoNDEは、あまり使われないエキスパートの重みをGPUへ運ぶ代わりに、CXLでホスト/GPUへ接続した拡張メモリ デバイス側でエキスパート GEMMそのものを実行する方式である。 |
| 2024-03 | [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md) | ✓ | 0 | KV キャッシュを読む注意機構計算をCPU側へ分け、GPUにはモデル重みを使う計算を集中させることで、KV転送を避けながらGPUの処理量を高める異種LLM serving システム。 |
<!-- survey:auto:end -->
