# Offload / Hierarchical Memory

GPUメモリに収まらないLLMを動かすため、主に**model weightやMoE expert**をCPU memory、peer GPU HBM、SSD / Flashなどへ置き、必要な部分だけGPUへ移す、CPU/GPUで分担して計算する、storage側で計算する研究をまとめる。KV cache固有のoffloadは [KV Cache Offload / Recomputation](../10-kv-cache-offload-recomputation/) に分離する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（28本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-04 · [FluxMoE: Decoupling Expert Residency for High-Performance MoE Serving](2026-2604.02715-fluxmoe-decoupling-expert-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FluxMoEは、MoEのエキスパート重みを「モデルを読み込みしたらsession終了までGPUに居続ける静的パラメータ」とみなす前提を崩す。各層を実行する直前だけその層のエキスパートをGPUへ実体化（materialize）し、使い終えたら物理メモリを解放する。

- **2026-06 · [WiSP: A Working-Set View of Mixture-of-Experts Serving on Extremely Low-Resource Hardware](2026-2606.21868-wisp-working-set-moe-serving-low-resource-hardware.md)**  
  実装：[✓](https://github.com/nokia-applied-research/WiSP) ・ リポジトリ内被引用：1  
  低並列の混合専門家モデル（Mixture of エキスパート; MoE）推論では、全エキスパート重みをGPUへ常駐できない一方、各トークンが実際に使うエキスパートは一部だけである。従来の層単位CPUオフロードは層内の全エキスパートをPCIe越しに転送するため、この疎性を生かせず、さらにエキスパート用VRAMを増やすとKVキャッシュが減って同時処理能力を失う。

- **2026-02 · [DALI: A Workload-Aware Offloading Framework for Efficient MoE Inference on Local PCs](2026-2602.03495-dali-workload-aware-moe-offloading-local-pcs.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUメモリに全エキスパートを置けないローカルPCで混合専門家モデル（Mixture of エキスパート; MoE）を実行すると、CPUとGPUの固定分担では入力ごとに変動するエキスパート負荷へ追随できず、PCIe転送も待ち時間になりやすい。

- **2025-12 · [Context-Aware Mixture-of-Experts Inference on CXL-Enabled GPU-NDP Systems](2025-2512.04476-context-aware-moe-cxl-ndp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUメモリに収まらない混合専門家モデル（Mixture of エキスパート; MoE）では、外部メモリから巨大なエキスパート重みを毎回GPUへ運ぶとPCIe転送が支配的になる。本研究はCXL接続のデータ近傍処理（Near-Data Processing; NDP）側に低頻度エキスパートを置いてその場で計算し、重み転送を小さな活性値転送へ置き換える。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [Who Should Own the Expert Cache? Kernel-Managed Tiering for Trillion-Parameter MoE Inference](2026-2608.12103-kernel-managed-expert-cache-tiering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が問うのは「LRUとLFUのどちらが良いか」より一段上の問題である。巨大MoEのエキスパートキャッシュを誰が所有すべきか、すなわちLLMランタイムがエキスパート単位の専用キャッシュを自前実装するべきか、それともLinuxカーネルがすでに持つページキャッシュをDRAM階層として利用すべきかを実機で比較する。

- **2026-08 · [SAEM: Stage-Aware Expert Management for Memory-Efficient MoE Inference in Chain-of-Thought Reasoning](2026-2608.21614-saem-stage-aware-expert-management-cot.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い連鎖思考（Chain-of-Thought; CoT）では同じ推論段階のあいだに似たエキスパート集合が繰り返し使われる一方、トークン単位のLRU型キャッシュは細かなルーティング変動のたびに重みを入れ替え、PCIe転送とキャッシュスラッシングを増やす。

- **2026-08 · [Potential Applications of HBF in LLM Serving Systems](2026-2608.13127-hbf-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  High-帯域 Flash（HBF）をHBMの直接代替にせず、HBMに収まりきらない読み出し主体なモデル状態を保持する容量階層として追加することで、MoEエキスパートの複製、複数モデル重み常駐、読み込み均衡化を改善できるかを検討する。主結果は実HBFハードウェアではなく、HBM側の実効帯域を維持できるという前提を置いたサービング・シミュレーションである。

- **2026-08 · [DASH: Beyond Capacity: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths](2026-2608.14333-dash-beyond-capacity-scalable-moe-llm-inference-via-high-bandwidth-flash-with-di.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常SSDよりはるかに高帯域な将来型フラッシュをGPU/HBMの近くへ接続し、エキスパート重みをGPUへ直接送る経路とHBMをバッファにする経路を同時利用して、大容量MoEの重み転送待ちを減らす設計。

- **2026-06 · [Cache-Resident LLM Inference in GB-Scale Last-Level Caches](2026-2606.25353-cache-resident-llm-inference-gb-scale-last-level-caches.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GB級のCPU last-レベルキャッシュへモデル重みを常駐させ、重み計算と注意機構/KV状態を別ソケットへ分離し、コア局所な配置と細粒度同期でDRAM往復と演算子バリアを減らすCPU LLM inferenceシステム。

- **2026-05 · [CoX-MoE: Coalesced Expert Execution for High-Throughput MoE Inference with AMX-Enabled CPU-GPU Co-Execution](2026-2605.17889-cox-moe-coalesced-expert-execution-for-high-throughput-moe-inference-with-amx-en.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数マイクロバッチから同じエキスパートへ送られるトークンをまとめて大きな行列 乗算として実行し、Intel AMX対応CPUとGPUへエキスパート計算を分担して、オフロード MoEのスループットを高める。

- **2026-04 · [NVLLM: A 3D NAND-Centric Architecture Enabling Edge on-Device LLM Inference](2026-2604.25699-nvllm-3d-nand-centric-edge-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末上でDRAM容量を超えるLLMを動かす場合、SSDからFFN重みを毎トークン読み戻す方式はPCIe帯域とデータ移動が支配的になり、GPUやNPUの演算器を十分に使えない。NVLLMは3D NANDを単なる保存先ではなくFFN重みの計算場所として扱い、静的で大容量なFFNをNAND側、動的な注意機構とKVキャッシュをDRAM・NPU側へ分離する。

- **2026-04 · [DAK: Direct-Access-Enabled GPU Memory Offloading with Optimal Efficiency for LLM Inference](2026-2604.26074-dak-direct-access-gpu-memory-offloading.md)**  
  実装：[✓](https://github.com/shouxulin/DirectAccessKernel) ・ リポジトリ内被引用：0  
  従来のLLMメモリオフロードはCPU側の重みやKVキャッシュを一度GPU HBMへ先読みしてから計算するため、転送書き込みと計算中のHBM読み出しが競合し、先読み用バッファもHBM容量を消費する。

- **2026-01 · [Harvest: Opportunistic Peer-to-Peer GPU Caching for LLM Inference](2026-2602.00328-harvest-opportunistic-peer-to-peer-gpu-caching-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NVLinkで接続された別GPUの空きHBMを、失ってもCPU コピーや再計算から復旧できる一時キャッシュとして使い、MoEエキスパート重みやKVキャッシュをホスト DRAMから戻すより高速に再取得するオフロード 枠組み。

- **2026-01 · [FlashMoE: Reducing SSD I/O Bottlenecks via ML-Based Cache Replacement for Mixture-of-Experts Inference on Edge Devices](2026-2601.17063-flashmoe-ssd-io-cache-replacement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全専門家重みをDRAMにも載せられない個人PC級環境で、MoEの専門家をNVMe SSDへ置き、実際に使う専門家だけをVRAMへ読み込む推論システム。SSD読出し回数を減らすため、単純なLRU/LFUではなく、各専門家の「最後に使ってからの時間」と「これまでの使用頻度」から次回利用までの遠さを小型ニューラルネットで予測し、将来使われにくい専門家から追い出す。

### 1年以上前

- **2023-03 · [FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU](2023-2303.06865-flexgen-high-throughput-generative-inference-of-large-language-models-with-a-single-gpu.md)**  
  実装：[✓](https://github.com/FMInference/FlexGen) ・ リポジトリ内被引用：104  
  FlexGenは、巨大LLMを単一GPUで動かすときに「GPUへ載らない重みをCPUやSSDへ逃がす」だけでなく、重み・中間活性・KV キャッシュの保存先と、計算順序そのものを一緒に設計することで、遅いI/Oを大きなバッチへ分散し、offline スループットを上げるシステムである。

- **2024-01 · [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Infinity) ・ リポジトリ内被引用：41  
  同じリクエストでは使われるエキスパートに偏りが続きやすい性質を利用し、過去のルーティング履歴から再利用されそうなエキスパートをGPUへ残して先読みすることで、個人PC上のMoEオフロード待ちを減らすシステム。

- **2024-02 · [Fiddler: CPU-GPU Orchestration for Fast Inference of Mixture-of-Experts Models](2024-2402.07033-fiddler-cpu-gpu-orchestration-for-fast-inference-of-mixture-of-experts-models.md)**  
  実装：[✓](https://github.com/efeslab/fiddler) ・ リポジトリ内被引用：32  
  GPUに常駐しないエキスパートをCPUで直接計算し、重い重み 転送を活性値転送へ置き換えるCPU–GPU協調MoE推論方式。

- **2023-12 · [Fast Inference of Mixture-of-Experts Language Models with Offloading](2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md)**  
  実装：[✓](https://github.com/dvmazur/mixtral-offloading) ・ リポジトリ内被引用：32  
  MoEエキスパートをCPUへ置き、最近使ったエキスパートをGPUへ残すLRUキャッシュと、将来使いそうなエキスパートの投機的先読みを組み合わせて、GPUメモリ制約下の重み転送待ちを減らす推論手法。

- **2023-12 · [LLM in a Flash: Efficient Large Language Model Inference with Limited Memory](2023-2312.11514-llm-in-a-flash-efficient-large-language-model-inference-with-limited-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  直近トークンで使ったFFN重みをDRAMへ残し、同じニューロンに必要な重みをFlash上でまとめて配置して、必要部分だけを少ない読み出し回数で読み出すことでI/OとDRAM使用量を減らす手法。

- **2025-02 · [Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading](2025-2502.05370-taming-latency-memory-trade-off-in-moe-based-llm-serving-via-fine-grained-expert.md)**  
  実装：[✓](https://github.com/IntelliSys-Lab/FineMoE-EuroSys26) ・ リポジトリ内被引用：13  
  生成反復ごとのルーティング履歴とプロンプトの類似性から近い過去リクエストを探し、次に使われそうなエキスパートだけを先読み・GPUキャッシュへ保持して、小さいVRAMでもエキスパート転送待ちを減らす無損失オフロード方式。

- **2025-02 · [Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline](2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md)**  
  実装：[✓](https://openi.pcl.ac.cn/fangzhy/Klotski) ・ リポジトリ内被引用：11  
  複数バッチで共通して使われるエキスパートを先にGPUで計算し、その計算中にまだGPUにないエキスパートをCPU RAM / SSDから読み込むことで、巨大MoEのI/O待ちを隠す単一GPU向け推論システム。

- **2024-03 · [HeteGen: Efficient Heterogeneous Parallel Inference for Large Language Models on Resource-Constrained Devices](2024-2403.01164-hetegen-efficient-heterogeneous-parallel-inference-for-large-language-models-on-resource-constrained-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  GPUに載らない線形 重みの一部をCPUで直接計算し、残りの重み転送・GPU計算と並行実行することで、バッチ=1の低遅延オフロード推論を高速化するCPU-GPU協調システム。

- **2024-09 · [TwinPilots: A New Computing Paradigm for GPU-CPU Parallel LLM Inference](2024-3688351.3689164-twinpilots-a-new-computing-paradigm-for-gpu-cpu-parallel-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  Transformer層をQ/K/V・注意機構・MLPなどへ分け、各処理をCPUで直接計算する時間とGPUへデータを運んで計算する時間を比較して実行先を決め、CPU計算とPCIe転送を同時進行させる推論システム。

- **2025-02 · [Memory Offloading for Large Language Model Inference with Latency SLO Guarantees](2025-2502.08182-select-n-slo-aware-memory-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Select-Nは、GPUに残すモデル状態量とCPU側ホストメモリへの退避量を、遅延サービス水準目標（service-level objective: SLO）を守りながら動的に調整するLLM推論システムである。中心概念はオフロード間隔（オフロード interval）で、何層ごとに1層をホストへ退避するかを整数値で表す。

- **2024-11 · [MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)**  
  実装：[✓](https://github.com/caoshiyi/artifacts/tree/asplos25) ・ リポジトリ内被引用：2  
  エキスパート重みとKVキャッシュをCPU DRAMへ置き、次の重み転送・CPU 注意機構・GPU MoE計算をマイクロバッチ間で同時進行させて、低VRAM GPUのI/O待ちを減らす推論システム。

- **2025-06 · [eLLM: Elastic Memory Management Framework for Efficient LLM Serving](2025-2506.15155-ellm-elastic-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMサービングで活性値とKVキャッシュを別々の固定メモリ領域として管理すると、片方が空いていても他方へ融通できずGPUメモリが遊ぶ問題に対し、仮想テンソル抽象で両者を同じ物理プールへ載せ、GPU内で領域を動的に貸し借りし、さらにCPUメモリを弾性的な退避先として使う推論基盤。

- **2025-08 · [SSD Offloading for LLM Mixture-of-Experts Weights Considered Harmful in Energy Efficiency](2025-2508.06978-ssd-moe-offloading-energy-efficiency.md)**  
  実装：[✓](https://github.com/scale-snu/SSD-offloading) ・ リポジトリ内被引用：0  
  MoEの専門家重みをSSDへ退避すると容量不足と転送遅延は扱いやすくなる一方、NAND Flashの読み出しエネルギーがHBMやCPU側DRAMより大幅に高い。

- **2024-05 · [MoNDE: Mixture-of-Experts Neural Network Inference with Near-Data Processing](2024-2405.18832-monde-mixture-of-experts-neural-network-inference-with-near-data-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUにないエキスパート重みを毎回GPUへ運ばず、重みを置いた拡張メモリ デバイス側でエキスパート計算を行い、小さい活性値だけを転送することでMoEのデータ 移動を減らす方式。
<!-- survey:auto:end -->
