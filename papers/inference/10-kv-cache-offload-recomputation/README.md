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
## 自動生成の論文一覧（59本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-10 · [LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference](2025-2510.09665-lmcache.md)**  
  実装：[✓](https://github.com/LMCache/LMCache) ・ リポジトリ内被引用：34  
  LMCacheはKVを独立オブジェクトとしてページ集約し、複数要求・推論エンジン・保存階層間で検索／転送し、接頭辞再計算とGPU・I/O待ちを減らす基盤。

- **2026-05 · [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  TuttiはGPU主導の非同期SSD読込みでKV要求をまとめ、CPU発行の小I/Oを排してGPUへ直接転送し、SSD容量を使いながらKV復元待ちを減らす方式。

- **2026-05 · [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KVDriveはHBM・DRAM・NVMeの三層でKVを管理し、再利用度に応じた選択・転送・注意計算を小バッチで重ね、SSDから必要ブロックだけを読み長文I/Oを減らす方式。

- **2025-12 · [CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving](2025-2512.11920-cxl-speckv-fpga-disaggregated-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CXL-SpecKVは低温KVをCXLメモリへ置き、FPGAで圧縮・展開とDMAを処理し、将来トークンを予測し、予測トークンに対応すると論文が説明する将来位置のKVを先読みすることで容量と転送待ちを減らす方式。論文は投機先読みを報告するが、公開実装ではLSTM重み読込・実DMA・予測トークン別address生成を確認できず性能寄与未検証。

- **2025-11 · [LiteCache: A Query Similarity-Driven, GPU-Centric KVCache Subsystem for Efficient LLM Inference](2025-2511.14510-litecache-gpu-centric-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LiteCacheはクエリ類似度で再利用価値の高いKVヘッドを選び、CPUの索引処理をGPU中心の一括取得へ置き換えて、細粒度管理・同期・カーネル起動のオーバーヘッドを減らす方式。

- **2026-08 · [HiSparse: Scaling Sparse-Attention Decoding with Hierarchical KV Cache Management](2026-2608.07009-hisparse-hierarchical-kv-sparse-attention.md)**  
  実装：[✓](https://github.com/sgl-project/sglang) ・ リポジトリ内被引用：1  
  疎注意が実際に読むtop-k KVだけを固定サイズHBMキャッシュへ置き、全履歴はホストDRAMに保持してLRU・融合CUDA取得・共有選択の正確な先読みで補うことで、出力を変えず長文デコードのHBM容量壁を外す方式。

- **2026-08 · [Heterogeneous LLM Serving with General-Purpose Processing-Near-Memory for Retrieval-Based Sparse Attention](2026-2608.03555-karat-pnm-retrieval-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KARATはKVと索引をLPDDR搭載の汎用処理近傍メモリへ移し、GPUを重み計算へ専念させ、検索型疎注意をマイクロバッチ化して大容量KVの転送とGPU容量制約を減らす方式。

- **2026-08 · [Cross-Model KV Cache Transfer in LLM Families: A Closed-Form Linear Mapping for Prefill Reuse](2026-2608.03893-cross-model-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大小モデル間でKVを内容空間のヘッド単位線形写像へ変換し、受信モデルの長文再プリフィルを省く方式。対応層を選びRoPEを付け直して形状差による誤差を抑える。

- **2026-07 · [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md)**  
  実装：[✓](https://github.com/shutianluo/DirectKV) ・ リポジトリ内被引用：1  
  DirectKVはCPU DRAM上のKVをGPUカーネルから直接読み、CPUデータを再利用するタイル化と融合カーネルで中継HBMバッファ・往復転送・帯域浪費を減らすゼロコピー方式。

- **2026-07 · [Learning Agent Execution for KV-Cache Management in Agentic Serving](2026-2608.14624-cachescout.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CacheScoutはエージェント遷移をオンライン学習し、次に呼ばれそうな固定プレフィックスKVをGPUへ残し、空き時間に先読みして再プリフィルと追い出しを減らす方式。

- **2026-07 · [A CXL Memory Rack for Multi-Turn LLM Serving](2026-2607.18141-hymcache-cxl-hybrid-memory-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HyMCacheはCXL背後の小容量DRAMと大容量SSDを一体化し、接頭辞KVをリクエスト単位でDRAMへ先読み、読出しを優先してSSD容量と再利用遅延を両立する方式。

- **2026-05 · [VeriCache: Turning Lossy KV Cache into Lossless LLM Inference](2026-2605.17613-vericache-lossless-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  VeriCacheは圧縮KVで候補を生成し、完全KVをCPU／共有ストアから読み込んで最初の不一致を検証・訂正し、品質を保ったまま復元帯域とGPU計算を要求間で重ねる方式。

- **2026-04 · [HybridGen: Efficient LLM Generative Inference via CPU-GPU Hybrid Computing](2026-2604.18529-hybridgen-efficient-llm-generative-inference-via-cpu-gpu-hybrid-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HybridGenはKVをCPU/GPUへ分けて各側で注意を計算しGPUで正規化し、次層CPU計算・PCIe転送・GPU計算も重ねて長文デコードの転送／CPU律速を減らす方式。

- **2026-04 · [DUAL-BLADE: Dual-Path NVMe-Direct KV-Cache Offloading for Edge LLM Inference](2026-2604.26557-dual-blade-nvme-direct-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DUAL-BLADEはKVをページキャッシュとNVMe直接経路へ分け、連続論理ブロックとGPU DMAを使い、mmapのスラッシングとファイル層処理によるSSD待ちを減らす方式。

- **2026-04 · [CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration](2026-2604.25080-cacheflow.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CacheFlowは退避接頭辞KVをトークン・層・GPU方向に分割し、一部を再計算し残りをI/O復元して同時進行させ、復元待ちを減らす3次元スケジューラ。

- **2026-03 · [TTKV: Temporal-Tiered KV Cache for Long-Context LLM Inference](2026-2604.19769-ttkv-temporal-tiered-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TTKVは最近KVをHBM、古いKVを差分量子化してDRAMへ置き、重要ブロックを非同期先読みしながら注意を計算して転送量と長文遅延を減らす方式。

- **2026-03 · [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Swarmは共に参照されるKVを事前にグループ化し、複数SSDへ分散して並列読込みすることで、単一SSDの帯域上限と長文KVのI/O待ちを減らす方式。

- **2026-01 · [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/SuperInfer) ・ リポジトリ内被引用：1  
  SuperInferはTTFT/TBTのSLO遅れを監視し、要求KVをGH200のHBMとCPU DRAM間で入れ替え、KVブロックを集約転送してヘッドオブライン待ちとC2C帯域浪費を抑える方式。

- **2025-12 · [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV再利用で省いたプリフィル計算と、CPUから戻すKV転送をH100実測・式で比較し、キャッシュ量が増えるといつPCIeが律速へ逆転するかを明らかにする分析。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents](2026-2609.09643-unison-agent-session-kv-residency.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントのツール待ち間隔と終了しやすさからセッション単位のKV再利用順位を作り、追い出しとSRAM/HBM間移動を同じ近メモリ制御器で決めることで、再プリフィルと階層アクセス遅延を減らす方式。

- **2026-09 · [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](2026-2609.04852-kvmem-virtualizing-million-token-agent-workspaces.md)**  
  実装：[✓](https://github.com/kvmem/kvmem-qw3) ・ リポジトリ内被引用：0  
  KVMemは百万トークン級の履歴KVをGPU・CPU・NVMeの論理ワークスペースに保持し、質問に必要なブロックだけをモデル文脈窓へ戻すことで、全履歴の再プリフィルとGPU容量制約を減らす方式。

- **2026-09 · [Enabling High-Bandwidth Flash for Generative Recommendation Serving with Write-Aware KV Cache Policy](2026-2609.07175-high-bandwidth-flash-write-aware-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成推薦の利用者KVキャッシュをHBFへ置く際、LRU-Kで低再利用利用者のキャッシュ書込みを抑え、HBMのみより3.8〜4.7倍のスループットを得つつフラッシュ寿命を約1年から6年以上へ延ばす方式を分析した。

- **2026-09 · [CacheBridge: Efficient Cross-Model KV Cache Transfer](2026-2609.00891-cachebridge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CacheBridgeは出典モデルのKVを受信モデルのヘッド局所表現へ線形変換し、注意感度で係数を学習・GPU融合して、モデル切替時の再プリフィル計算と変換器容量を減らす方式。

- **2026-08 · [Preserving Admission Responsibility in Multi-Tenant Large Language Model Prefix Caches](2026-2608.01657-prefixshield-admission-responsibility.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュで新規ブロックを作った利用者に持続的な回収責任を持たせ、負債中の再利用昇格を抑えつつ、その利用者の低価値ブロックから追い出すことで、固定分割なしに他利用者の接頭辞再利用を守る方式。

- **2026-08 · [OasisKV: Scaling In-Decode KV Cache Beyond HBM with Lookahead Sparse Prefetching](2026-2608.08097-oasiskv-lookahead-sparse-prefetching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OasisKVは投機トークンと圧縮キー要約で次に必要なKVブロックを予測し、GPUへ疎な作業集合だけを非同期先読みして、CPU／遠隔メモリ転送とHBM容量を抑える方式。

- **2026-08 · [Minima-KV: Retention-Preserving KV Cache Compression with Mixed-Format Paged Attention](2026-2608.23834-minima-kv-mixed-format-paged-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Minima-KVは最近・保護ページをFP8、古い非保護ページを3ビット級へ変換し、形式別注意カーネルを共通softmaxで統合して、KV削除と高精度影コピーを避ける方式。

- **2026-08 · [Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap](2026-2608.23658-elastic-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Elastic KVキャッシュはCUDA仮想メモリでデコード中だけ活性値予約領域をKVへ貸し、プリフィル直前に返す。単純な小分割とTTFT・容量を比較し、機構の実用優位の範囲を測る分析。

- **2026-07 · [DualDecoder: Accelerate Long Context LLM Inference by Predictive Prefetch](2026-2607.26475-dualdecoder-predictive-prefetch.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DualDecoderは投機トークンから次の疎KV位置を予測し、層計算より先にCPUから必要KVを転送する。GPUには現在・次層の二層だけを保持し補助状態の容量を減らす方式。

- **2026-07 · [A Photonic-CXL Memory Appliance for Scalable KV Cache Management in LLM Inference](2026-2607.27187-photonic-cxl-memory-appliance-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フォトニックCXL装置は共有KVを受動光網で16ホストへ接続し、電気スイッチの多段遅延を避けて共有容量を2TBから32TBへ広げ、再計算と転送待ちを減らす方式。

- **2026-06 · [SwiftCache: Efficient LLM Serving for Multi-turn Conversations with Heterogeneous KV Cache Sharing](2026-2606.16135-swiftcache-heterogeneous-kv-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SwiftCacheはKV需要の小さいモデルの空きHBMを借り、主モデルの接頭辞KVをNVLinkで共有し、層単位でストリーム転送してCPU／SSD退避のTTFTを減らす方式。

- **2026-06 · [PolyKV: Heterogeneous Retention and Allocation for KV Cache Compression](2026-2606.15157-polykv-heterogeneous-kv-retention-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PolyKVは層・プリフィル／デコード段階ごとに追い出し方式と容量を校正評価で選び、感度の高い層へKV予算を再配分して固定規則の品質低下を減らす方式。

- **2026-05 · [ObjectCache: Layerwise Object-Storage Retrieval for KV Cache Reuse](2026-2605.22850-objectcache-layerwise-object-storage-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  細粒度KVチャンクをS3互換ストレージへ保存したまま、複数物体の同一層範囲をサーバ側で集約して層順にRDMA転送し、GPU計算とI/Oを重ね、計算窓に応じて共有帯域も配分する大容量接頭辞キャッシュ方式。

- **2026-05 · [Adaptive KV Cache Reuse for Fast Long-Context LLM Serving](2026-2605.24022-cachetune-adaptive-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CacheTuneは文書断片KVを周波数成分で選別し、重要部分だけ全体文脈で再計算、残りをストレージから再利用して、品質と再計算・転送時間を両立する方式。

- **2026-03 · [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ScoutAttentionはGPUにない重要KVの注意をCPUで計算し、次層のCPU注意を一層先に開始して、KV転送とCPU計算をGPU層処理へ重ねる方式。

- **2026-02 · [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ParisKVはGPUにキー要約だけを残し、古くなる検索索引を再構成しながら重要KVを二段選択してCPU DRAMから直接取得し、長文検索のCPU処理・転送待ちを減らす方式。

- **2026-02 · [PAM: Processing Across Memory Hierarchy for Efficient KV-centric LLM Serving System](2026-2602.11521-pam-processing-across-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PAMはHBM・DDR・SSD各層にメモリ内処理を置き、重要KVを上位へ寄せつつ各層で注意を局所計算し、全KVをGPUへ戻す帯域と下位層集中を減らす方式。

- **2026-02 · [KEEP: A KV-Cache-Centric Memory Management System for Efficient Embodied Planning](2026-2602.23592-keep-kv-cache-centric-embodied-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KEEPは更新頻度で具身記憶を群分けし、文脈依存の重要度伝播で必要KVだけを再計算し、層をまたぐ先読みでCPU→GPU読込み待ちを減らす方式。

- **2026-02 · [HillInfer: Efficient Long-Context LLM Inference on the Edge with Hierarchical KV Eviction using SmartSSD](2026-2602.18750-hillinfer-smartssd-hierarchical-kv-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HillInferはSmartSSD内FPGAでKV全体ではなく重要度内積だけを評価し、CPUの高温KVとSSDの低温KVを選択転送・GPU計算と重ねてI/O待ちを減らす方式。

- **2026-02 · [ForesightKV: Optimizing KV Cache Eviction for Reasoning Models by Learning Long-Term Contribution](2026-2602.03203-foresightkv-long-term-contribution-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ForesightKVは将来の注意履歴から数百〜数千トークン後に参照されるKVを教師化し、軽量評価器で長期寄与を予測して追い出し、早すぎる削除を減らす方式。

- **2026-02 · [Efficient Remote KV Cache Reuse with GPU-native Video Codec](2026-2602.09725-kvfetcher-gpu-native-media-asic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVFetcherは遠隔KVの取得・展開・逆量子化をGPU近傍メディアASICで処理し、推論GPUとの資源競合を分離してネットワーク転送と復元待ちを減らす方式。

- **2026-02 · [CHESS: Context-aware Hierarchical Efficient Semantic Selection for Long-Context LLM Inference](2026-2602.20732-chess-context-aware-hierarchical-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CHESSはKVをGrid・Chunk・Pageの三階層で要約し、生成文脈との類似度で必要ページだけを再構成し、不確実時だけ修復して全KV走査と容量を減らす方式。

### 2年前（2024-10〜2025-09）

- **2024-11 · [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md)**  
  実装：[✓](https://github.com/NEO-MLSys25/NEO) ・ リポジトリ内被引用：20  
  NEOは一部要求のKVとデコード注意をCPUへ移し、GPU要求と同時に進めてCPU/GPUの完了時刻を反復ごとに揃え、VRAM不足と待ち時間を抑える方式。

- **2024-10 · [ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference](2024-2410.21465-shadowkv-low-rank-key-value-offload.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/ShadowKV) ・ リポジトリ内被引用：19  
  ShadowKVはキーを低ランク要約と代表値としてGPUに残し、値だけCPUへ置いて重要チャンクの値を選択転送し、長文KVの容量とPCIe転送量を減らす方式。

- **2024-11 · [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md)**  
  実装：[✓](https://github.com/chaoyij/KVPR) ・ リポジトリ内被引用：11  
  KVPRはCPU上のKVの一部を小さい中間活性値からGPUで再計算し、残りのKV転送と並行してPCIe待ちを減らす無損失方式。

- **2025-05 · [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  RetroInferはCPU上のKVをベクトル索引で検索し、注意に重要なトークンだけGPUへ取り出して、全KV走査の容量・帯域を減らしつつ検索近似誤差を抑える方式。

- **2024-11 · [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Pieは数層先で必要なKVをCPU DRAMからGPUへ先読みし、現在層の計算と転送を重ね、転送が律速する直前まで退避量を動的に増やす方式。

- **2025-03 · [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SpeCacheは16-bit KV正本をCPUに残し、GPUには重要位置の低ビット索引と少数の正確KVだけを置く。次トークンの参照先を予測して一段先読みし、容量と転送待ちを減らす方式。

- **2025-09 · [ShadowServe: Interference-Free KV Cache Fetching for Distributed Prefix Caching](2025-2509.16857-shadowserve-smartnic-kv-fetching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ShadowServeは遠隔圧縮KVの展開・逆量子化をSmartNICへ移し、GPUを推論計算に専念させて、KV取得時のGPU競合とCPU処理待ちを減らす方式。

- **2025-08 · [TokenLake: A Unified Segment-level Prefix Cache Pool for Fine-grained Elastic Long-Context LLM Serving](2025-2508.17219-tokenlake-segment-prefix-cache-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  TokenLakeは接頭辞KVを独立セグメントへ分割して全GPUの共有プールへ置き、頻出セグメントだけ複製し、負荷偏り・重複保存・断片化と通信量を減らす方式。

- **2025-02 · [HeadInfer: Memory-Efficient LLM Inference by Head-wise Offloading](2025-2502.12574-headinfer-head-wise-kv-offloading.md)**  
  実装：[✓](https://github.com/wdlctc/headinfer) ・ リポジトリ内被引用：2  
  HeadInferはKVをヘッド単位でCPU DRAMからGPUへ読み、次ヘッドの転送を現在ヘッドの注意計算へ重ねることで、層単位転送より必要VRAMと長文容量を抑える方式。

- **2024-10 · [Compute Or Load KV Cache? Why Not Both?](2024-2410.03065-cake-compute-or-load-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Cakeは保存済み接頭辞KVの先頭をGPUで再計算し末尾をストレージから逆順読込みし、両方をチャンク並行化してTTFTを支配する計算・I/O待ちを減らす方式。

- **2025-07 · [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  高速HBMと大容量DRAMへのKV配置を将来の注意参照まで既知とする理想条件で比較し、頻繁に読むKVをHBMへ移すことの性能上限と予測配置の余地を測る分析。

- **2025-06 · [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  APEXはCPU担当要求とGPU担当要求の線形計算を一つのGPUバッチにまとめ、注意結果の同期を必要直前まで遅らせてCPU計算をGPU処理の裏へ隠す方式。

- **2025-09 · [TRACE: Unlocking Effective CXL Bandwidth via Lossless Compression and Precision Scaling](2025-2509.03377-cxl-ndp-transparent-near-data-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TRACEはCXLメモリ装置内で重み・KVをビット面再配置して無損失圧縮し、精度別別名で不要ビット面を読まず、CXL帯域・DRAM読出し・エネルギーを減らす方式。

- **2025-09 · [SparseServe: Unlocking Parallelism for Dynamic Sparse Attention in Long-Context LLM Serving](2025-2509.24626-sparseserve-dynamic-sparse-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意で未使用KVをDRAMへ逃がし、断片化転送・HBM競合・長文プリフィルを専用機構で抑えることで、vLLM比で初回トークン時間を最大9.26倍短縮し生成スループットを最大3.14倍高めた長文LLMサービング基盤。

- **2025-01 · [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md)**  
  実装：[✓](https://github.com/casys-kaist/Capture) ・ リポジトリ内被引用：0  
  過去トークンをKVまたは小さい中間活性値で混在保存し、重み転送中に活性値からKVを再生成して、PCIe転送量とGPU再計算量の大きい方を抑える方式。

### 3年前（2023-10〜2024-09）

- **2024-03 · [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  FastDecodeはKVと注意計算を複数CPUノードへ置き、GPUは重み計算を大バッチで進め、巨大KVのGPU転送とHBM容量制約を減らす異種パイプライン。

- **2024-09 · [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  InstAttentionはKVを計算機能付きSSDへ置き、SSD内部でデコード注意を計算して、毎トークンのKV読戻しによるPCIe転送を削減する方式。

- **2024-07 · [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md)**  
  実装：[✓](https://github.com/aquaml/aqua) ・ リポジトリ内被引用：6  
  AquaはNVLink/NVSwitch内の空きGPU HBMを別要求のKV退避先として貸し、CPU DRAM・PCIeへの退避より高速に要求を切り替えて待ち時間を抑える方式。
<!-- survey:auto:end -->
