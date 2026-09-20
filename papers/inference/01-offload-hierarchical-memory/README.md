# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、主に**model weightやMoE expert**をCPU memory、peer GPU HBM、SSD / Flashなどへ置き、必要な部分だけGPUへ移す、CPU/GPUで分担して計算する、storage側で計算する研究をまとめる。KV cache固有のoffloadは [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（54本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [A Cost-Effective Near-Storage Processing Solution for Offline Inference of Long-Context LLMs](2025-2502.09921-hilos-near-storage-processing.md)**  
  実装：[✓](https://github.com/hongsunjang/HILOS/tree/asplos26) ・ リポジトリ内被引用：5  
  市販SmartSSD上で自己注意をKVの近くへ移し、X-キャッシュと遅延KV書戻しを組み合わせることで、長文脈オフライン推論を通常SSD型オフロード比で最大7.86倍高速化する。

- **2025-11 · [Beluga: A CXL-Based Memory Architecture for Scalable and Efficient LLM KVCache Management](2025-2511.20172-beluga-cxl-memory-kvcache.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  CXL 2.0スイッチでGPU/CPUから共有KVメモリを直接ロード／ストア可能にし、細粒度KV転送・共有メモリRPC・局所性不要の配置をvLLMへ統合してRDMA型プールのコピーと同期を削減する。

- **2026-04 · [FluxMoE: Decoupling Expert Residency for High-Performance MoE Serving](2026-2604.02715-fluxmoe-decoupling-expert-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  FluxMoEは層の実行直前だけ必要な専門家重みをGPUへ実体化し、直後に解放するPagedTensorと帯域比例のストリーミングで、KVキャッシュを圧迫する常駐重みを減らす。

- **2026-08 · [Potential Applications of HBF in LLM Serving Systems](2026-2608.13127-hbf-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究はHigh-Bandwidth FlashをHBMの代替でなく容量階層としてMoE専門家の複製と複数モデル重みの常駐を増やし、遠隔通信・読み込み・負荷偏りを減らせるか検討する。

- **2026-06 · [WiSP: A Working-Set View of Mixture-of-Experts Serving on Extremely Low-Resource Hardware](2026-2606.21868-wisp-working-set-moe-serving-low-resource-hardware.md)**  
  実装：[✓](https://github.com/nokia-applied-research/WiSP) ・ リポジトリ内被引用：1  
  WiSPはルーティング履歴から再利用される専門家をGPUワーキングセットとしてLRU保持し、限られたVRAMを専門家とKVキャッシュの限界便益で配分して、PCIe転送とKV不足を抑える。

- **2026-06 · [ITME: Inference Tiered Memory Expansion with Disaggregated CXL-Hybrid Memories](2026-2606.12556-itme-cxl-hybrid-tiered-memory-expansion.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CXLハイブリッドメモリ内のDRAM+NVMeをTB級の遠隔メモリとして公開し、重みと長文KVの予測可能なアクセスを多段DMA先読み・読出し優先I/Oで隠して、CPU DRAMを超える推論状態を保持する階層メモリ方式。

- **2026-02 · [DALI: A Workload-Aware Offloading Framework for Efficient MoE Inference on Local PCs](2026-2602.03495-dali-workload-aware-moe-offloading-local-pcs.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DALIは入力ごとの専門家負荷を測ってCPU/GPU配置を各層で動的に変え、残差から次層を先読みし負荷履歴でGPUキャッシュを交換して、ローカルPCのPCIe待ちを減らす。

- **2026-01 · [Harvest: Opportunistic Peer-to-Peer GPU Caching for LLM Inference](2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HarvestはNVLink接続された別GPUの空きHBMを一時キャッシュに使い、MoE重みやKVをホストDRAMから再取得する遅延を減らす。正本はCPUや再計算に残し、キャッシュ喪失にも耐える。

- **2026-01 · [FlashMoE: Reducing SSD I/O Bottlenecks via ML-Based Cache Replacement for Mixture-of-Experts Inference on Edge Devices](2026-2601.17063-flashmoe-ssd-io-cache-replacement.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlashMoEはMoEの専門家重みをNVMe SSDへ置き、VRAMには必要なものだけを読み込む。最近度と利用頻度から次回利用の遠さを予測してキャッシュを置換し、SSD読み出し待ちを減らす。

- **2025-12 · [SliceMoE: Bit-Sliced Expert Caching under Miss-Rate Constraints for Efficient MoE Inference](2025-2512.12990-slicemoe-bit-sliced-expert-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MoEエキスパートを上位・下位ビットのスライス単位でキャッシュし、重要度に応じて精度を動的再構成することで、フラッシュ転送を抑えながら高精度を保つ端末向け推論方式。

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

- **2026-09 · [HBFSim: Fast and Faithful Simulation of High-Bandwidth Flash Under Real GPU Execution](2026-2609.09800-hbfsim-high-bandwidth-flash-real-gpu-execution.md)**  
  実装：[✓](https://github.com/SlugLab/HBFSim) ・ リポジトリ内被引用：0  
  実GPU上のLLMをPTX計装し、未実機化のHBFについて遅延・容量・熱・保持・リフレッシュを閉ループで差し込むシミュレータ。110GiB論理容量やvLLMの同一出力を実データで検証する。

- **2026-09 · [Building py-kvcache: A Performance Characterization of External KV Caching for vLLM with NVMe SSDs](2026-2609.11744-building-py-kvcache-a-performance-characterization-of-external-kv-caching-for-vllm-with-nvme-ssds.md)**  
  実装：[✓](https://github.com/atlarge-research/py-kvcache) ・ リポジトリ内被引用：0  
  GPU・CPU・NVMe間のKV再利用を実測し、非同期直接I/O、固定容量ステージング、待機列先読み、再計算との損益分岐判定を組み合わせたvLLM外部KVキャッシュを実装・評価する。

- **2026-08 · [Who Should Own the Expert Cache? Kernel-Managed Tiering for Trillion-Parameter MoE Inference](2026-2608.12103-kernel-managed-expert-cache-tiering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は1兆パラメータ級の混合専門家モデルの重みを専用管理器でなくLinuxカーネルのページキャッシュに任せ、再利用性と先読み助言を比較してDRAM不足時の管理負担を減らす。

- **2026-08 · [SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning](2026-2608.21614-saem-stage-aware-expert-management-cot.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAEMはCoTの遷移語から推論段階を検出し、段階ごとの活性化頻度でGPU専門家キャッシュを更新する。非常駐専門家はCPU計算に回し、トークン再配置で小カーネルの管理費も減らす。

- **2026-08 · [NeuroPrefetcher: Storage-Aware Sparse LLM Inference via Delta Prefetching](2026-2608.22643-neuroprefetcher-storage-aware-delta-prefetching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  隣接トークンで82〜85%再利用できるMLP活性行をGPUに残し、新規行だけNVMeから先読みすることで、モデルが常駐不能なJetson上でllama.cpp比7.9〜12.0倍を実現する行単位ストレージ推論。

- **2026-08 · [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DASHは将来型High-Bandwidth FlashをGPU/HBM近傍へ接続し、専門家重みをGPUへ直送する経路とHBM経由経路を並行利用して、大容量MoEのフラッシュ転送待ちを減らす。

- **2026-08 · [Cacheable by Design? Training Mixture-of-Experts Routers for Locality Against the Edge Memory-Bandwidth Wall: A Pre-Registered Negative Result with a Systems Measurement Study](2026-2608.18261-cacheable-by-design-expert-locality.md)**  
  実装：[✓](https://github.com/Shriniwas410/cacheable-by-design) ・ リポジトリ内被引用：0  
  SSDオフロードMoEでは自然な専門家局所性だけで帯域壁を越えられず、局所性学習も品質低下なしには成立しないことを事前登録で示し、学習＋キャッシュ認識再ルーティングなら約80%のミス削減を得る境界を測定した。

- **2026-07 · [TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models](2026-2607.07388-tf-engram-ssd-backed-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フレーズ専用意味記憶を訓練なしで構築し、GPU・DRAM・NVMe SSDへ階層配置、中間層の早期予測でSSD読出しを先読みする外部記憶。100Mエントリで平均精度59.4、GPU使用3.06GBを報告。

- **2026-07 · [NELSSA: A GPU–PNM Heterogeneous System for Mixed-Length LLM Serving via Length–based Request Placement](2026-2607.26633-nelssa-gpu-pnm-mixed-length-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求長に応じて短い注意機構をGPU、長い疎注意を実機PNMへ配置し、文脈成長時はキー・バリュー状態を背景移送して一方向に実行先を切り替え、混在長負荷のGPUメモリ圧迫と先頭待ちを抑える異種実行基盤。

- **2026-06 · [RH+: Row-Hit-Optimized Scheduling for PIM-based LLM Inference](2026-2606.05511-rh-plus-pim-row-hit-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBM3-PIM復号の真の律速をDRAM行サイクルと特定し、同一行32連続MACへ並べ替えるRH+で8.25〜11.88倍高速化する。

- **2026-06 · [Cache-Resident LLM Inference in GB-Scale Last-Level Caches](2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はCPUのGB級LLCへ重みを常駐させ、重み計算と注意/KVをソケット分離し、コア局所配置と細粒度同期でDRAM往復と演算子バリアを減らす。

- **2026-05 · [TokenStack: A Heterogeneous HBM-PIM Architecture and Runtime for Efficient LLM Inference](2026-2605.05639-tokenstack-heterogeneous-hbm-pim-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBM4の同一スタック内を高密度容量層とPIM計算層へ分け、高頻度KVだけを演算近傍へ動的配置することで、AttAcc比で処理量1.62倍・SLO処理容量1.70倍を達成する。

- **2026-05 · [TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload](2026-2605.20179-tide-io-aware-expert-offload.md)**  
  実装：[✓](https://github.com/ims-kdks/TIDE) ・ リポジトリ内被引用：0  
  拡散MoEで近接デノイズ段階の専門家活性が安定する性質を使い、専門家配置を数ステップごとだけ更新してCPU計算とPCIe転送を両方抑え、出力を変えず単一GPU推論を高速化する。

- **2026-05 · [PipeMax: Enhancing Offline LLM Inference on Commodity GPU Servers](2026-2605.02189-pipemax-offline-llm-inference-commodity-gpu-servers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  パイプライン並列で今使わないバッチのKVキャッシュをCPUへ退避し、現在の計算時間に収まる量だけ次バッチ用に先読みすることで、GPUメモリとPCIe帯域を有効活用しオフラインLLM推論を高速化する。

- **2026-05 · [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoX-MoEは複数マイクロバッチの同一専門家向けトークンを集約して大きなGEMMにし、Intel AMX CPUとGPUへ分担実行して小規模GEMMとオフロード転送の非効率を減らす。

- **2026-05 · [Asymmetric Virtual Memory Paging for Hybrid Mamba-Transformer Inference](2026-2605.22416-asymmetric-virtual-memory-paging-hybrid-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュと固定長SSM状態を別物理プール・統一仮想アドレスで扱い、割当失敗時だけ容量を移してハイブリッドLLMのメモリ不足と処理性能を改善する。

- **2026-04 · [NVLLM: A 3D NAND-Centric Architecture Enabling Edge on-Device LLM Inference](2026-2604.25699-nvllm-3d-nand-centric-edge-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NVLLMは静的なFFN重みを3D NAND側に置いてその場で計算し、注意機構とKVをDRAM/NPU側で処理する。NAND面の並列読出しと誤り訂正を重ね、SSD経由のデータ移動を減らす。

- **2026-04 · [DAK: Direct-Access-Enabled GPU Memory Offloading with Optimal Efficiency for LLM Inference](2026-2604.26074-dak-direct-access-gpu-memory-offloading.md)**  
  実装：[✓](https://github.com/shouxulin/DirectAccessKernel) ・ リポジトリ内被引用：0  
  DAKはCPUメモリの重み・KVをGPU HBMへ先読みせずTMAで共有メモリへ直接運び、演算別オフロード率・輻輳制御・マルチキャストでHBM中継と帯域競合を減らす。

- **2025-12 · [ODMA: On-Demand Memory Allocation Framework for LLM Serving on LPDDR-Class Accelerators](2025-2512.09427-odma-on-demand-memory-allocation-lpddr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LPDDR系アクセラレータで長さ予測と動的連続バケットによりKVキャッシュをオンデマンド確保し、メモリ利用率とRPS/TPSを改善する方式。

### 2年前（2024-10〜2025-09）

- **2025-02 · [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)**  
  実装：[✓](https://github.com/IntelliSys-Lab/FineMoE-EuroSys26) ・ リポジトリ内被引用：21  
  FineMoEは反復ごとのルーティング履歴とプロンプト類似性から次に使う専門家を予測し、GPUキャッシュへ先読みしてMoE重み転送待ちを減らす。

- **2025-02 · [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)**  
  実装：[✓](https://openi.pcl.ac.cn/fangzhy/Klotski) ・ リポジトリ内被引用：18  
  Klotskiは複数バッチで共通する専門家を先に計算し、その間にCPU RAMやSSDから次の専門家を読み込んで巨大MoEのI/O待ちを隠す。

- **2025-04 · [HybriMoE: Hybrid CPU-GPU Scheduling and Cache Management for Efficient MoE Inference](2025-2504.05897-hybrimoe-hybrid-cpu-gpu-scheduling-cache-management.md)**  
  実装：[✓](https://github.com/PKU-SEC-Lab/HybriMoE) ・ リポジトリ内被引用：11  
  MoEの実負荷に応じCPU・GPU・PCIeを動的配分し、影響度駆動プリフェッチとスコア認識キャッシュを統合してkTransformers比プリフィル1.33倍、デコード1.70倍を達成する。

- **2024-11 · [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)**  
  実装：[✓](https://github.com/caoshiyi/artifacts/tree/asplos25) ・ リポジトリ内被引用：6  
  MoE-Lightningは専門家重みとKVをCPU DRAMへ置き、マイクロバッチ間で次の重み転送・CPU注意・GPU計算を重ねて低VRAMのI/O待ちを減らす。

- **2025-08 · [Accelerating Mixture-of-Experts Inference by Hiding Offloading Latency with Speculative Decoding](2025-2508.21706-specmoeoff-speculative-decoding-offload.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  専門家重み転送でGPUが遊ぶMoEオフロードに投機的デコードを組み合わせ、1回の重み転送で複数トークンを検証する。CPU向け注意検証と自動設定選択も加え、MoE-Lightning比でスループットを平均2.1倍、最大2.9倍へ改善する。

- **2025-03 · [Fast On-device LLM Inference with NPUs](2024-2407.05858-fast-on-device-llm-inference-with-npus.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/mllm) ・ リポジトリ内被引用：5  
  可変長入力の固定長分割、量子化外れ値のCPU/GPU分離、ブロック単位の異種プロセッサ配置を組み合わせ、スマートフォンNPUでLLMプリフィルを高速化する。

- **2025-08 · [SSD Offloading for LLM Mixture-of-Experts Weights Considered Harmful in Energy Efficiency](2025-2508.06978-ssd-moe-offloading-energy-efficiency.md)**  
  実装：[✓](https://github.com/scale-snu/SSD-offloading) ・ リポジトリ内被引用：4  
  MoE専門家重みをHBM・CPUメモリ・SSDに置いたときのデコードエネルギーを比較し、SSD退避では1トークン当たりMixtralが3.8〜12.5倍、DeepSeek-R1が4.7〜9.8倍増えると示す。

- **2025-06 · [eLLM: Elastic Memory Management Framework for Efficient LLM Serving](2025-2506.15155-ellm-elastic-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  eLLMは活性値とKVキャッシュを同じ物理メモリプールで動的に融通し、SLO違反に応じてCPU退避量も調整して長文脈サービングの待ち行列とバッチ容量を両立する。

- **2025-05 · [Not All Models Suit Expert Offloading: On Local Routing Consistency of Mixture-of-Expert Models](2025-2505.16056-local-routing-consistency-expert-offloading.md)**  
  実装：[✓](https://github.com/ljcleo/moe-lrc) ・ リポジトリ内被引用：3  
  20種MoEをSRP/SCHで比較し、エキスパートオフロード適性を左右する局所ルーティング一貫性とキャッシュ比率約2の設計指針を示す。

- **2025-04 · [MoE-Lens: Towards the Hardware Limit of High-Throughput MoE LLM Serving Under Resource Constraints](2025-2504.09345-moe-lens-hardware-limit-resource-constrained-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  CPUメモリ容量と要求長まで含む性能上限モデルから、プリフィル・デコード重畳と重み転送を設計し、資源制約下MoE推論をハードウェア限界へ近づける。

- **2025-02 · [Memory Offloading for Large Language Model Inference with Latency SLO Guarantees](2025-2502.08182-select-n-slo-aware-memory-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Select-NはSLO・系列長・バッチサイズに応じてGPUに残す層とCPUへ退避する層の間隔を動的に調整し、オフロード量とスループットを両立する。

- **2025-09 · [Accelerating Mixture-of-Expert Inference with Adaptive Expert Split Mechanism](2025-2509.08342-moepic-adaptive-expert-split.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  専門家を上部・下部へ分割し、頻出専門家の上部だけをGPUへ広く常駐させ、下部を次層予測で先読みするMoEオフロード方式。層別VRAM・分割比も適応設定し、TPOTを37.51〜65.73%削減する。

- **2025-03 · [FlexInfer: Breaking Memory Constraint via Flexible and Efficient Offloading for On-Device LLM Inference](2025-2503.03777-flexinfer-flexible-efficient-on-device-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  重み読出しを計算と非同期化し、各層へ固定メモリを均等配分し、容量に応じて保持テンソルを切り替えることで、端末向けCPU推論をmmap比最大12.5倍高速化する。

### 3年前（2023-10〜2024-09）

- **2024-01 · [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Infinity) ・ リポジトリ内被引用：63  
  MoE-Infinityはルーティング履歴から次に再利用される専門家を予測し、GPUキャッシュへ先読みして個人PCのMoEオフロード転送待ちを減らす。

- **2023-12 · [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：52  
  LLM in a Flashは直近で使ったFFN重みをDRAMに残し、ニューロン単位でFlash上の重みをまとめて必要部分だけ読み出して大規模モデルを限られたメモリで生成する。

- **2024-02 · [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)**  
  実装：[✓](https://github.com/efeslab/fiddler) ・ リポジトリ内被引用：48  
  Fiddlerはキャッシュミスした専門家をGPUへ転送するか、活性値だけCPUへ送りCPUで計算するかを実行時に選び、MoEの重み転送待ちを減らす。

- **2023-12 · [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)**  
  実装：[✓](https://github.com/dvmazur/mixtral-offloading) ・ リポジトリ内被引用：48  
  Mixtralの専門家重みをCPUに置き、LRUキャッシュと投機的先読みで必要な専門家だけGPUへ移して、12〜16GB級VRAMでの転送待ちを減らす。

- **2024-03 · [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  HeteGenは線形層の重みをCPU計算分とGPU計算分へ分割し、CPU計算・重み転送・GPU計算を重ねてバッチ1のオフロード遅延を抑える。

- **2024-09 · [TwinPilots: A New Computing Paradigm for GPU-CPU Parallel LLM Inference](2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  TwinPilotsはTransformer処理ごとにCPU計算とGPU転送・計算の速さを比較し、CPU計算とPCIe転送を並行させてGPUオフロードの生成待ちを減らす。

- **2024-05 · [Efficient Heterogeneous Large Language Model Decoding with Model-Attention Disaggregation](2024-2405.01814-attention-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  注意演算とその他をH20/H100へ分離し、CPU非介在通信と自動分割・パイプラインで層間通信を隠して、同費用vLLM比16.1〜90.1%高いデコードスループットを得る。

- **2024-05 · [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MoNDEは低頻度専門家の重みを拡張メモリ側に置き、デバイス上でGEMMを実行して小さな活性値だけをGPUへ転送し、MoEのデータ移動を減らす。

### 4年前（2022-10〜2023-09）

- **2023-03 · [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md)**  
  実装：[✓](https://github.com/FMInference/FlexGen) ・ リポジトリ内被引用：194  
  FlexGenは巨大LLMの重み・中間活性・KVキャッシュをGPU・CPU・SSDへ分け、計算順序とバッチでI/Oを使い回して単一GPUの生成スループットを高める。
<!-- survey:auto:end -->
