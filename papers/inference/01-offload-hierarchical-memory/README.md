# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、主に**model weightやMoE expert**をCPU memory、peer GPU HBM、SSD / Flashなどへ置き、必要な部分だけGPUへ移す、CPU/GPUで分担して計算する、storage側で計算する研究をまとめる。KV cache固有のoffloadは [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（35本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-04 · [FluxMoE: Decoupling Expert Residency for High-Performance MoE Serving](2026-2604.02715-fluxmoe-decoupling-expert-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FluxMoEは層の実行直前だけ必要な専門家重みをGPUへ実体化し、直後に解放するPagedTensorと帯域比例のストリーミングで、KVキャッシュを圧迫する常駐重みを減らす。

- **2026-06 · [WiSP: A Working-Set View of Mixture-of-Experts Serving on Extremely Low-Resource Hardware](2026-2606.21868-wisp-working-set-moe-serving-low-resource-hardware.md)**  
  実装：[✓](https://github.com/nokia-applied-research/WiSP) ・ リポジトリ内被引用：1  
  WiSPはルーティング履歴から再利用される専門家をGPUワーキングセットとしてLRU保持し、限られたVRAMを専門家とKVキャッシュの限界便益で配分して、PCIe転送とKV不足を抑える。

- **2026-06 · [ITME: Inference Tiered Memory Expansion with Disaggregated CXL-Hybrid Memories](2026-2606.12556-itme-cxl-hybrid-tiered-memory-expansion.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CXLハイブリッドメモリ内のDRAM+NVMeをTB級の遠隔メモリとして公開し、重みと長文KVの予測可能なアクセスを多段DMA先読み・読出し優先I/Oで隠して、CPU DRAMを超える推論状態を保持する階層メモリ方式。

- **2026-02 · [DALI: A Workload-Aware Offloading Framework for Efficient MoE Inference on Local PCs](2026-2602.03495-dali-workload-aware-moe-offloading-local-pcs.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DALIは入力ごとの専門家負荷を測ってCPU/GPU配置を各層で動的に変え、残差から次層を先読みし負荷履歴でGPUキャッシュを交換して、ローカルPCのPCIe待ちを減らす。

- **2025-12 · [Context-Aware Mixture-of-Experts Inference on CXL-Enabled GPU-NDP Systems](2025-2512.04476-context-aware-moe-cxl-ndp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Context-Aware MoEは低頻度専門家をCXL接続NDP側で計算し、重要度に応じたGPU配置と1〜4ビット量子化で重み転送を減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [PATTON: Enabling Commodity PIM for Production LLM Serving](2026-2609.11392-patton-commodity-pim-production-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMの論理KVブロックを汎用PIMの物理配置・命令へ変換し、階層グラニュール割当とCommit Zoneで動的キャッシュ管理・GEMV効率・毎トークン書き込み効率を両立するPIMランタイム。

- **2026-09 · [LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism](2026-2609.00857-imc-noc-balanced-dataflow-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的重み用のメモリ内計算、動的データ用のメモリ近傍計算、部分結果集約用のネットワーク内計算を統合し、細粒度データ配置とプリフィル・デコード分離で通信とメモリ帯域の偏りを抑えるLLM推論アクセラレータ。

- **2026-09 · [Building py-kvcache: A Performance Characterization of External KV Caching for vLLM with NVMe SSDs](2026-2609.11744-building-py-kvcache-a-performance-characterization-of-external-kv-caching-for-vllm-with-nvme-ssds.md)**  
  実装：[✓](https://github.com/atlarge-research/py-kvcache) ・ リポジトリ内被引用：0  
  GPU・CPU・NVMe間のKV再利用を実測し、非同期直接I/O、固定容量ステージング、待機列先読み、再計算との損益分岐判定を組み合わせたvLLM外部KVキャッシュを実装・評価する。

- **2026-08 · [Who Should Own the Expert Cache? Kernel-Managed Tiering for Trillion-Parameter MoE Inference](2026-2608.12103-kernel-managed-expert-cache-tiering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は1兆パラメータ級の混合専門家モデルの重みを専用管理器でなくLinuxカーネルのページキャッシュに任せ、再利用性と先読み助言を比較してDRAM不足時の管理負担を減らす。

- **2026-08 · [SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning](2026-2608.21614-saem-stage-aware-expert-management-cot.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAEMはCoTの遷移語から推論段階を検出し、段階ごとの活性化頻度でGPU専門家キャッシュを更新する。非常駐専門家はCPU計算に回し、トークン再配置で小カーネルの管理費も減らす。

- **2026-08 · [Potential Applications of HBF in LLM Serving Systems](2026-2608.13127-hbf-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はHigh-Bandwidth FlashをHBMの代替でなく容量階層としてMoE専門家の複製と複数モデル重みの常駐を増やし、遠隔通信・読み込み・負荷偏りを減らせるか検討する。

- **2026-08 · [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DASHは将来型High-Bandwidth FlashをGPU/HBM近傍へ接続し、専門家重みをGPUへ直送する経路とHBM経由経路を並行利用して、大容量MoEのフラッシュ転送待ちを減らす。

- **2026-07 · [NELSSA: A GPU–PNM Heterogeneous System for Mixed-Length LLM Serving via Length–based Request Placement](2026-2607.26633-nelssa-gpu-pnm-mixed-length-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求長に応じて短い注意機構をGPU、長い疎注意を実機PNMへ配置し、文脈成長時はキー・バリュー状態を背景移送して一方向に実行先を切り替え、混在長負荷のGPUメモリ圧迫と先頭待ちを抑える異種実行基盤。

- **2026-06 · [Cache-Resident LLM Inference in GB-Scale Last-Level Caches](2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はCPUのGB級LLCへ重みを常駐させ、重み計算と注意/KVをソケット分離し、コア局所配置と細粒度同期でDRAM往復と演算子バリアを減らす。

- **2026-05 · [TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload](2026-2605.20179-tide-io-aware-expert-offload.md)**  
  実装：[✓](https://github.com/ims-kdks/TIDE) ・ リポジトリ内被引用：0  
  拡散MoEで近接デノイズ段階の専門家活性が安定する性質を使い、専門家配置を数ステップごとだけ更新してCPU計算とPCIe転送を両方抑え、出力を変えず単一GPU推論を高速化する。

- **2026-05 · [PipeMax: Enhancing Offline LLM Inference on Commodity GPU Servers](2026-2605.02189-pipemax-offline-llm-inference-commodity-gpu-servers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  パイプライン並列で今使わないバッチのKVキャッシュをCPUへ退避し、現在の計算時間に収まる量だけ次バッチ用に先読みすることで、GPUメモリとPCIe帯域を有効活用しオフラインLLM推論を高速化する。

- **2026-05 · [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoX-MoEは複数マイクロバッチの同一専門家向けトークンを集約して大きなGEMMにし、Intel AMX CPUとGPUへ分担実行して小規模GEMMとオフロード転送の非効率を減らす。

- **2026-04 · [NVLLM: A 3D NAND-Centric Architecture Enabling Edge on-Device LLM Inference](2026-2604.25699-nvllm-3d-nand-centric-edge-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NVLLMは静的なFFN重みを3D NAND側に置いてその場で計算し、注意機構とKVをDRAM/NPU側で処理する。NAND面の並列読出しと誤り訂正を重ね、SSD経由のデータ移動を減らす。

- **2026-04 · [DAK: Direct-Access-Enabled GPU Memory Offloading with Optimal Efficiency for LLM Inference](2026-2604.26074-dak-direct-access-gpu-memory-offloading.md)**  
  実装：[✓](https://github.com/shouxulin/DirectAccessKernel) ・ リポジトリ内被引用：0  
  DAKはCPUメモリの重み・KVをGPU HBMへ先読みせずTMAで共有メモリへ直接運び、演算別オフロード率・輻輳制御・マルチキャストでHBM中継と帯域競合を減らす。

- **2026-01 · [Harvest: Opportunistic Peer-to-Peer GPU Caching for LLM Inference](2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HarvestはNVLink接続された別GPUの空きHBMを一時キャッシュに使い、MoE重みやKVをホストDRAMから再取得する遅延を減らす。正本はCPUや再計算に残し、キャッシュ喪失にも耐える。

- **2026-01 · [FlashMoE: Reducing SSD I/O Bottlenecks via ML-Based Cache Replacement for Mixture-of-Experts Inference on Edge Devices](2026-2601.17063-flashmoe-ssd-io-cache-replacement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashMoEはMoEの専門家重みをNVMe SSDへ置き、VRAMには必要なものだけを読み込む。最近度と利用頻度から次回利用の遠さを予測してキャッシュを置換し、SSD読み出し待ちを減らす。

### 2年前（2024-10〜2025-09）

- **2025-02 · [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)**  
  実装：[✓](https://github.com/IntelliSys-Lab/FineMoE-EuroSys26) ・ リポジトリ内被引用：13  
  FineMoEは反復ごとのルーティング履歴とプロンプト類似性から次に使う専門家を予測し、GPUキャッシュへ先読みしてMoE重み転送待ちを減らす。

- **2025-02 · [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)**  
  実装：[✓](https://openi.pcl.ac.cn/fangzhy/Klotski) ・ リポジトリ内被引用：11  
  Klotskiは複数バッチで共通する専門家を先に計算し、その間にCPU RAMやSSDから次の専門家を読み込んで巨大MoEのI/O待ちを隠す。

- **2024-11 · [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)**  
  実装：[✓](https://github.com/caoshiyi/artifacts/tree/asplos25) ・ リポジトリ内被引用：3  
  MoE-Lightningは専門家重みとKVをCPU DRAMへ置き、マイクロバッチ間で次の重み転送・CPU注意・GPU計算を重ねて低VRAMのI/O待ちを減らす。

- **2025-02 · [Memory Offloading for Large Language Model Inference with Latency SLO Guarantees](2025-2502.08182-select-n-slo-aware-memory-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Select-NはSLO・系列長・バッチサイズに応じてGPUに残す層とCPUへ退避する層の間隔を動的に調整し、オフロード量とスループットを両立する。

- **2025-06 · [eLLM: Elastic Memory Management Framework for Efficient LLM Serving](2025-2506.15155-ellm-elastic-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  eLLMは活性値とKVキャッシュを同じ物理メモリプールで動的に融通し、SLO違反に応じてCPU退避量も調整して長文脈サービングの待ち行列とバッチ容量を両立する。

- **2025-08 · [SSD Offloading for LLM Mixture-of-Experts Weights Considered Harmful in Energy Efficiency](2025-2508.06978-ssd-moe-offloading-energy-efficiency.md)**  
  実装：[✓](https://github.com/scale-snu/SSD-offloading) ・ リポジトリ内被引用：0  
  MoE専門家重みをHBM・CPUメモリ・SSDに置いたときのデコードエネルギーを比較し、SSD退避では1トークン当たりMixtralが3.8〜12.5倍、DeepSeek-R1が4.7〜9.8倍増えると示す。

### 3年前（2023-10〜2024-09）

- **2024-01 · [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Infinity) ・ リポジトリ内被引用：41  
  MoE-Infinityはルーティング履歴から次に再利用される専門家を予測し、GPUキャッシュへ先読みして個人PCのMoEオフロード転送待ちを減らす。

- **2024-02 · [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)**  
  実装：[✓](https://github.com/efeslab/fiddler) ・ リポジトリ内被引用：33  
  Fiddlerはキャッシュミスした専門家をGPUへ転送するか、活性値だけCPUへ送りCPUで計算するかを実行時に選び、MoEの重み転送待ちを減らす。

- **2023-12 · [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)**  
  実装：[✓](https://github.com/dvmazur/mixtral-offloading) ・ リポジトリ内被引用：33  
  Mixtralの専門家重みをCPUに置き、LRUキャッシュと投機的先読みで必要な専門家だけGPUへ移して、12〜16GB級VRAMでの転送待ちを減らす。

- **2023-12 · [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  LLM in a Flashは直近で使ったFFN重みをDRAMに残し、ニューロン単位でFlash上の重みをまとめて必要部分だけ読み出して大規模モデルを限られたメモリで生成する。

- **2024-03 · [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  HeteGenは線形層の重みをCPU計算分とGPU計算分へ分割し、CPU計算・重み転送・GPU計算を重ねてバッチ1のオフロード遅延を抑える。

- **2024-09 · [TwinPilots: A New Computing Paradigm for GPU-CPU Parallel LLM Inference](2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  TwinPilotsはTransformer処理ごとにCPU計算とGPU転送・計算の速さを比較し、CPU計算とPCIe転送を並行させてGPUオフロードの生成待ちを減らす。

- **2024-05 · [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoNDEは低頻度専門家の重みを拡張メモリ側に置き、デバイス上でGEMMを実行して小さな活性値だけをGPUへ転送し、MoEのデータ移動を減らす。

### 4年前（2022-10〜2023-09）

- **2023-03 · [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md)**  
  実装：[✓](https://github.com/FMInference/FlexGen) ・ リポジトリ内被引用：120  
  FlexGenは巨大LLMの重み・中間活性・KVキャッシュをGPU・CPU・SSDへ分け、計算順序とバッチでI/Oを使い回して単一GPUの生成スループットを高める。
<!-- survey:auto:end -->
