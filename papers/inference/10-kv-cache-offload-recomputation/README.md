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
## 自動生成の論文一覧（55本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-10 · [LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference](2025-2510.09665-lmcache.md)**  
  実装：[✓](https://github.com/LMCache/LMCache) ・ リポジトリ内被引用：25  
  LMCacheの本質は、KVキャッシュ（KV キャッシュ）を「1台のGPU上で1 リクエストのデコードを速くする一時バッファ」から、複数リクエスト・複数推論エンジン・複数保存 階層の間で保存・検索・転送できる独立データ オブジェクトへ昇格させることにある。

- **2026-05 · [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈のデコードではKV キャッシュがGPU HBMに収まらないため、CPU DRAMへ退避し、注意機構に必要なKVだけをGPUへ戻す方式が使われる。

- **2025-11 · [LiteCache: A Query Similarity-Driven, GPU-Centric KVCache Subsystem for Efficient LLM Inference](2025-2511.14510-litecache-gpu-centric-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LiteCacheは、長文LLMでKVキャッシュをCPUへ退避し必要なtop-kだけGPUへ戻す方式が、細粒度キャッシュ管理をCPUで行うためCPU処理・同期・カーネル起動がボトルネックとなり、CUDAグラフも使いにくい問題を扱う。

- **2026-08 · [Heterogeneous LLM Serving with General-Purpose Processing-Near-Memory for Retrieval-Based Sparse Attention](2026-2608.03555-karat-pnm-retrieval-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  100万トークン級の長文で検索型疎注意を使うLLMでは、毎ステップ読むKV量は減っても全KVキャッシュと索引キーの保存容量は減らない。KARATはKVと索引を大容量LPDDR搭載の汎用処理近傍メモリへ移し、GPUを重み・MoE計算へ専念させ、異種デバイス間をマイクロバッチでパイプライン化することで、同一電力制約下の同時実行数とデコード処理量を高める。

- **2026-08 · [Cross-Model KV Cache Transfer in LLM Families: A Closed-Form Linear Mapping for Prefill Reuse](2026-2608.03893-cross-model-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同一モデル系列の大小モデルを途中で切り替える運用では、受信側モデルが蓄積済み文脈を最初からプリフィルし直すため、長い会話ほど切替コストが大きくなる。本論文は送信元モデルのKVキャッシュを受信先のKV表現へ直接写像し、再プリフィルを省く。

- **2026-05 · [VeriCache: Turning Lossy KV Cache into Lossless LLM Inference](2026-2605.17613-vericache-lossless-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文LLM推論ではKVキャッシュを間引き・量子化するとGPUメモリ使用量と転送量を減らせる一方、各トークンで生じる小さな分布差が生成列全体で累積し、コード生成や関数呼び出しでは形式上自然でも機能的に誤った出力へ崩れる。

- **2026-05 · [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVMe SSD上へ退避したKVキャッシュを戻す際、CPUが大量の小さなI/O要求を発行する従来方式をやめ、GPU自身がSSDへの非同期I/Oを制御してKVをまとめて転送することで、SSD容量を使いながらDRAM基盤の キャッシュに近い推論性能を狙うシステム。

- **2026-04 · [HybridGen: Efficient LLM Generative Inference via CPU-GPU Hybrid Computing](2026-2604.18529-hybridgen-efficient-llm-generative-inference-via-cpu-gpu-hybrid-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文生成では巨大化したKVキャッシュをCPUへ退避すると転送量が増え、CPU側で注意機構を計算すると今度はCPU計算が律速になる。HybridGenはKVキャッシュをCPU側とGPU側へ分け、各側が手元のKVに対する注意スコアを並列計算し、GPUで結合・正規化する。

- **2026-03 · [TTKV: Temporal-Tiered KV Cache for Long-Context LLM Inference](2026-2604.19769-ttkv-temporal-tiered-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TTKVは、長文推論で増え続けるKVキャッシュを、最近のトークンを置くGPU HBMの高速階層と、古いトークンを圧縮して置くホストDRAMの低速階層に分ける。単なる退避ではなく、キーを8ビット、値を4ビットで差分量子化し、低速階層を128トークン単位のブロックに整理する。

- **2026-01 · [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/SuperInfer) ・ リポジトリ内被引用：1  
  GH200のHBMが混雑したとき、応答開始やトークン間隔の目標に遅れそうなリクエストを優先してKV キャッシュをCPU DRAMとの間で入れ替え、小さいKV ブロックをまとめて双方向転送することで高速C2C linkを使い切るオンライン 提供 システム。

- **2025-12 · [CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving](2025-2512.11920-cxl-speckv-fpga-disaggregated-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈LLMのKVキャッシュをGPU HBMだけに保持できない問題に対し、CXL接続メモリへ低温KVを退避し、FPGAで圧縮・展開とDMA制御を行う階層メモリ方式である。論文はさらに小型LSTMで将来トークンを予測し、将来位置のKVをGPU側へ投機的に先読みすると説明する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](2026-2609.04852-kvmem-virtualizing-million-token-agent-workspaces.md)**  
  実装：[✓](https://github.com/kvmem/kvmem-qw3) ・ リポジトリ内被引用：0  
  KVMemは「100万トークンをGPUで一度に注意機構する」仕組みではない。エージェントが過去に処理した100万トークン規模の履歴を検索可能な論理ワークスペースとして保持し、その時の質問に必要な一部だけをモデル本来の文脈 窓へ戻して推論する仕組みである。

- **2026-09 · [Enabling High-Bandwidth Flash for Generative Recommendation Serving with Write-Aware KV Cache Policy](2026-2609.07175-high-bandwidth-flash-write-aware-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成推薦の利用者KVキャッシュをHBFへ置く際、LRU-Kで低再利用利用者のキャッシュ書込みを抑え、HBMのみより3.8〜4.7倍のスループットを得つつフラッシュ寿命を約1年から6年以上へ延ばす方式を分析した。

- **2026-09 · [CacheBridge: Efficient Cross-Model KV Cache Transfer](2026-2609.00891-cachebridge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ長い入力を別のLLMへ引き継ぐと、通常は新しいモデルが最初からプリフィルして自分用のKVキャッシュを作り直す必要がある。CacheBridgeは元モデルのKVから受信モデルのKVを線形変換で近似し、この再計算を避ける。

- **2026-08 · [OasisKV: Scaling In-Decode KV Cache Beyond HBM with Lookahead Sparse Prefetching](2026-2608.08097-oasiskv-lookahead-sparse-prefetching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OasisKVは、長文LLMのデコードで完全KVキャッシュをGPU HBMへ保持するとバッチ数が制限され、CPU・遠隔メモリへ置いて必要時に取得するとPCIeやネットワーク転送がクリティカルパスになる問題を扱う。投機的デコードのドラフトトークンを一段先の注意予測信号として再利用し、圧縮キー要約から次に必要なKVブロックを予測して非同期先読みする。

- **2026-08 · [Minima-KV: Retention-Preserving KV Cache Compression with Mixed-Format Paged Attention](2026-2608.23834-minima-kv-mixed-format-paged-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文推論のKVキャッシュを一律の精度で保持するとHBM容量と帯域を消費する一方、重要度が低いと判断した過去トークンを削除する方式は、後から注意が戻った位置を参照できない。Minima-KVは稼働中要求の論理KVページを削除せず、最近のページと保護対象の古いページをFP8、その他の古いページを3ビット級のTQ3へ移す三階層方式である。

- **2026-08 · [Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap](2026-2608.23658-elastic-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMは大きなプリフィルに備えて一時活性値用GPUメモリを常時予約するため、デコード中はその領域が遊ぶ。Elastic KVキャッシュはCUDA仮想メモリを使い、デコード中だけその予約領域をKVキャッシュへ貸し、プリフィル直前に返す機構を実装する。

- **2026-07 · [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md)**  
  実装：[✓](https://github.com/shutianluo/DirectKV) ・ リポジトリ内被引用：0  
  GH200でCPU DRAM上のKVキャッシュをGPU HBMへ一度コピーせず、GPUの注意機構 カーネルから直接読み、同じCPU側データを何度も読まないよう計算順序とカーネルを作り直すゼロコピー KV オフロード システム。

- **2026-07 · [Learning Agent Execution for KV-Cache Management in Agentic Serving](2026-2608.14624-cachescout.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数のLLMエージェントを順番に呼ぶシステムでは、各エージェント固有のシステム プロンプトやツール定義が何度も再利用される。CacheScoutは「今のエージェントの次に誰が呼ばれやすいか」を実行履歴から軽量に学習し、近く再利用されそうなエージェントの固定プレフィックス KVをGPUに残し、空き時間には次候補のKVを先に作ることで再プリフィルを減らす。

- **2026-07 · [DualDecoder: Accelerate Long Context LLM Inference by Predictive Prefetch](2026-2607.26475-dualdecoder-predictive-prefetch.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文LLMで疎なKVキャッシュだけをGPUへ読み込む方式は、KV本体を減らしても検索や再構成に使う補助状態を全層分GPUへ常駐させるため、実際のメモリ節約が小さくなりやすい。DualDecoderは、直前に投機生成したトークンから次トークンが参照しそうなKV位置を予測し、層ごとの計算より先にCPUメモリから必要KVを転送する。

- **2026-07 · [A Photonic-CXL Memory Appliance for Scalable KV Cache Management in LLM Inference](2026-2607.27187-photonic-cxl-memory-appliance-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模LLM配信では、長文・複数ターン会話のKVキャッシュをGPU HBMだけに保持できず、CPU側DRAMやSSDへ階層化すると容量は増えるが、再利用時の転送帯域と遅延が新たなボトルネックになる。

- **2026-07 · [A CXL Memory Rack for Multi-Turn LLM Serving](2026-2607.18141-hymcache-cxl-hybrid-memory-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数ターンLLMでは過去の接頭辞から得たKVキャッシュを再利用するとプリフィル計算を省ける一方、共有KVをTB級まで蓄えるとGPU HBMや通常DRAMの容量単価が問題になる。

- **2026-06 · [SwiftCache: Efficient LLM Serving for Multi-turn Conversations with Heterogeneous KV Cache Sharing](2026-2606.16135-swiftcache-heterogeneous-kv-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SwiftCacheの発想は、CPUやSSDへKV キャッシュを逃がす前に、同じserver内で別モデルが使っていないGPU メモリを借りられないかというものだ。長い会話を処理するモデルを主モデル（マスター）、KV需要が小さいモデルを作業モデル（ワーカー）として、ワーカーの空きHBMへマスターの接頭部 KVを保存する。

- **2026-06 · [PolyKV: Heterogeneous Retention and Allocation for KV Cache Compression](2026-2606.15157-polykv-heterogeneous-kv-retention-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈LLMのKVキャッシュ圧縮では、従来は全Transformer層へ同じ追い出し規則とほぼ同じ容量を適用することが多い。PolyKVは、層ごと・プリフィル/デコード段階ごとに『どの既存追い出し方式を使うか』と『何トークン分のKV容量を与えるか』を別々に選べる設計空間へ拡張する。

- **2026-05 · [Adaptive KV Cache Reuse for Fast Long-Context LLM Serving](2026-2605.24022-cachetune-adaptive-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CacheTuneは、検索拡張生成や複数文書質問応答のように、再利用したい文書断片が最終入力の先頭に固定されない長文推論を対象とするKVキャッシュ再利用方式である。断片を個別に計算したKVを単純連結すると、本来は前方の別断片を参照して形成される層内表現が欠け、生成品質が落ちる。

- **2026-04 · [DUAL-BLADE: Dual-Path NVMe-Direct KV-Cache Offloading for Edge LLM Inference](2026-2604.26557-dual-blade-nvme-direct-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  メモリ制約の強い単一GPUエッジ環境でKVキャッシュをNVMe SSDへ退避すると、通常のmmap経路はOSページキャッシュが作業集合より小さい領域で激しくスラッシングし、さらにVFS・ファイルシステム・ブロック層の処理がSSD帯域を使い切れない。

- **2026-04 · [CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration](2026-2604.25080-cacheflow.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  以前処理した長いプレフィックスのKVキャッシュがGPU外に退避されているとき、全部をI/Oで戻すか全部を再計算するかの二択にせず、プレフィックスの一部はGPUで再計算し、別部分は外部メモリから読み戻して同時進行させる手法。

- **2026-03 · [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構で一緒に参照されやすいKV キャッシュを事前にまとめ、そのグループ内のKVを複数SSDへ分散配置することで、1回のKV読み出しを複数SSDから並列に行い、単一SSDの帯域上限を超える実効I/O帯域を得る方式。

- **2026-03 · [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈のKVキャッシュの大部分をCPU DRAMへ置きながら、GPUにある重要ブロックはGPU、CPUにしかない重要ブロックだけはCPUで注意機構を計算し、さらに次層でCPUが担当する注意機構を1層早く開始することで、KV転送待ちとCPU計算待ちの両方を減らす。

- **2026-02 · [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  完全精度のKV キャッシュをCPU DRAMへ置いたまま、GPU上の小さなキー要約だけで現在のクエリに重要なトークンを二段階検索し、選ばれたKVだけをGPUからCPU メモリへ直接読みに行くことで、長い生成中に検索indexが古くなる問題とCPU検索・CPU主導転送の待ち時間を同時に減らすKV 検索 システム。

- **2026-02 · [PAM: Processing Across Memory Hierarchy for Efficient KV-centric LLM Serving System](2026-2602.11521-pam-processing-across-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの逐次生成では、KVキャッシュの容量と注意計算に必要なメモリ帯域が同時に増える。安価なDDRやSSDへKVを置くだけでは、最下層に多数のKVが集中して低帯域側が新たな律速になる。

- **2026-02 · [KEEP: A KV-Cache-Centric Memory Management System for Efficient Embodied Planning](2026-2602.23592-keep-kv-cache-centric-embodied-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  具身計画で頻繁に更新される長い記憶をKVキャッシュとして再利用する際、更新箇所以降のキャッシュ無効化とCPUからGPUへの読み込み待ちが増える問題に対し、更新頻度に応じた記憶グループ化、文脈依存の多段重要度伝播による選択的再計算、層をまたぐ先読み読み込みを組み合わせて、精度を保ちながら初回トークン時間を短縮するシステム。

- **2026-02 · [HillInfer: Efficient Long-Context LLM Inference on the Edge with Hierarchical KV Eviction using SmartSSD](2026-2602.18750-hillinfer-smartssd-hierarchical-kv-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文LLMをメモリ制約の厳しいPCで動かす際、GPU・CPUだけではKVキャッシュを保持しきれずSSDへ退避すると、毎デコード段で重要度評価のため大量KVを読み戻す入出力が支配的になる。

- **2026-02 · [ForesightKV: Optimizing KV Cache Eviction for Reasoning Models by Learning Long-Term Contribution](2026-2602.03203-foresightkv-long-term-contribution-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い推論連鎖ではKVキャッシュが生成長に比例して増えるが、現在の注意だけで重要度を決める追い出し方式は、今は目立たなくても数百〜数千トークン後に再利用される意味依存KVを捨てやすい。ForesightKVは完全な推論軌跡の将来注意を使うGolden 追い出しで『将来一度でも強く参照されるKV』を教師化し、軽量MLP評価器を順位学習する。

- **2026-02 · [Efficient Remote KV Cache Reuse with GPU-native Video Codec](2026-2602.09725-kvfetcher-gpu-native-media-asic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔KVキャッシュ再利用では、同じ接頭辞のKVキャッシュを別ノードやストレージから取得して長いプリフィル計算を省ける一方、一般的なクラウドの数十Gbps以下のネットワークでは転送時間が利益を打ち消す。既存の圧縮方式は転送量を減らせても、CUDAコアを使う展開処理が推論と競合したり、高価なSmartNICを必要としたりする。

- **2026-02 · [CHESS: Context-aware Hierarchical Efficient Semantic Selection for Long-Context LLM Inference](2026-2602.20732-chess-context-aware-hierarchical-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CHESSは長文推論のKVキャッシュを単純に削るのではなく、現在の生成文脈に意味的に関連するページを毎段階で再構成するアルゴリズム・システム協調設計である。KVをGrid→Chunk→Pageの三階層の論理表現で要約し、最近のKey状態から作った問い合わせアンカーとのKey-Key意味類似度を使って粗い階層から細かい階層へ絞り込む。

- **2025-12 · [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUから戻すcached KVの量が、新しく計算するプリフィル トークン量に対してどれくらい増えるとPCIe転送の方がGPU計算より遅くなるかを式とH100実測で示し、prefix 再利用が多いほどKV オフロードが早くI/O律速になることを分析した研究。

### 1年以上前

- **2024-11 · [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md)**  
  実装：[✓](https://github.com/NEO-MLSys25/NEO) ・ リポジトリ内被引用：19  
  一部リクエストだけKV キャッシュとデコード 注意機構をCPUへ移し、残りリクエストはGPUで処理しながら、CPU/GPUが同時に終わるようオフロード量を毎iteration調整してVRAM不足を緩和するオンライン 提供 システム。

- **2024-10 · [ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference](2024-2410.21465-shadowkv-low-rank-key-value-offload.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/ShadowKV) ・ リポジトリ内被引用：17  
  ShadowKVは、長文LLMでKVキャッシュをGPUへ全保持するとバッチ数が制限され、CPUへ全退避すると疎なKVを毎トークン取得するPCIe遅延が大きい問題を扱う。回転位置埋め込み適用前のキーが系列ごとに強い低ランク構造を持つことを利用し、キーの低ランク表現・チャンク代表値・少数の外れ値だけGPUへ残し、低ランクでない値キャッシュをCPUへ退避する。

- **2024-03 · [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  KV キャッシュとそれを読むアテンション計算を複数CPU nodeへ置き、GPUにはモデル 重みを使う計算を集中させることで、KV転送を避けながら大バッチでGPU スループットを高める異種 推論提供 システム。

- **2024-11 · [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md)**  
  実装：[✓](https://github.com/chaoyij/KVPR) ・ リポジトリ内被引用：10  
  CPU上のKV キャッシュを全部GPUへ戻さず、一部はより小さい中間活性値だけを送りGPUでK/Vを作り直し、残りのKV転送と同時に進めてPCIe待ちを減らす方式。

- **2025-05 · [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  長文脈のKV キャッシュをCPU メモリ上のベクトル 保存として検索対象にし、注意機構に重要なトークンだけをGPUへ取り出すことで、全KVをGPUへ保持・走査するメモリ容量と帯域を減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論システム。

- **2024-09 · [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  KV キャッシュを計算機能付きSSD内へ置き、デコード アテンションもSSD内部で実行することで、巨大なKVをSSDからGPUへ毎トークン読み戻す転送を避ける長文脈推論システム。

- **2024-11 · [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  一部のKV キャッシュをCPU DRAMへ置き、使う数層前にGPUへ戻して転送を現在層の計算と重ね、GPUを待たせない範囲までオフロード量を自動で増やすKVキャッシュ オフロード システム。

- **2024-07 · [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md)**  
  実装：[✓](https://github.com/aquaml/aqua) ・ リポジトリ内被引用：6  
  同じNVLink / NVSwitch接続内で余っている別GPUのHBMを、KV キャッシュなどの一時退避先として借り、CPU DRAMへ退避するより高速に要求を入れ替えて公平なonline 推論提供を行うメモリ システム。

- **2025-03 · [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SpeCacheは、KV キャッシュを消してVRAMを空けるのではなく、16-bitの完全な正本をCPUに残したまま、今のトークンが実際に強く参照する少数のKVだけをGPUへ戻す方式である。

- **2025-09 · [ShadowServe: Interference-Free KV Cache Fetching for Distributed Prefix Caching](2025-2509.16857-shadowserve-smartnic-kv-fetching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ShadowServeは、分散接頭辞キャッシュで圧縮KVキャッシュを遠隔保存先から取得するとき、GPU上の復号・逆量子化がLLMのデコード計算と同じ演算資源・メモリ帯域を奪い合う問題を、SmartNICを独立したKVデータ処理階層として使うことで解決する。

- **2025-02 · [HeadInfer: Memory-Efficient LLM Inference by Head-wise Offloading](2025-2502.12574-headinfer-head-wise-kv-offloading.md)**  
  実装：[✓](https://github.com/wdlctc/headinfer) ・ リポジトリ内被引用：2  
  HeadInferの中心は、「1 層分のKV キャッシュすらGPUへ丸ごと戻す必要はない」という点にある。Multi-Head 注意機構では各注意機構 ヘッドを独立に計算し、最後に結果を連結できる。そこで全KVの正本をCPU DRAMへ置き、GPUには現在処理する1個または少数ヘッド分だけを読み込む。

- **2024-10 · [Compute Or Load KV Cache? Why Not Both?](2024-2410.03065-cake-compute-or-load-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Cakeは、長文接頭辞のKVキャッシュがSSDや遠隔ストレージに保存されているとき、GPUで最初から再計算するか低帯域I/Oから全量を読み込むかの二者択一をやめ、両資源を同時に使って初回トークン待ち時間を最小化する。

- **2025-08 · [TokenLake: A Unified Segment-level Prefix Cache Pool for Fine-grained Elastic Long-Context LLM Serving](2025-2508.17219-tokenlake-segment-prefix-cache-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  TokenLakeは、GPUクラスタ上の接頭辞KVキャッシュを各推論インスタンスの所有物として扱うために生じる負荷偏り、重複保存、空き領域の断片化を、全GPUをまたぐ統一セグメント単位キャッシュプールへ置き換える。

- **2025-07 · [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  頻繁に参照されるKVを高速HBM、そうでないKVを大容量DRAMへ置く配置問題をモデル化し、未来の注意機構参照先を完全に知る理想条件との比較から、実用スケジューラにどれだけ改善余地が残るかを測るシミュレーション研究。

- **2025-06 · [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一部要求のKV キャッシュとデコード アテンションをCPUへ移しつつ、アテンション前の線形計算はCPU/GPU向け要求を一つのGPU バッチでまとめ、CPU結果を必要になる直前まで待たないことでCPU アテンションをGPU計算の裏へ隠す方式。

- **2025-09 · [TRACE: Unlocking Effective CXL Bandwidth via Lossless Compression and Precision Scaling](2025-2509.03377-cxl-ndp-transparent-near-data-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL拡張メモリはGPU HBMより大容量・低価格だが、リンク帯域と装置側DRAM帯域が低く、LLMの重みやKVキャッシュを退避すると転送量が性能を支配しやすい。トレースはホスト側のCXL.memインターフェースを変えず、装置内部で数値をビット位置ごとに並べ替えて高圧縮な無損失表現へ変換し、KVではトークンをまたぐチャネル相関も利用する。

- **2025-09 · [SparseServe: Unlocking Parallelism for Dynamic Sparse Attention in Long-Context LLM Serving](2025-2509.24626-sparseserve-dynamic-sparse-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意で未使用KVをDRAMへ逃がし、断片化転送・HBM競合・長文プリフィルを専用機構で抑えることで、vLLM比で初回トークン時間を最大9.26倍短縮し生成スループットを最大3.14倍高めた長文LLMサービング基盤。

- **2025-01 · [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md)**  
  実装：[✓](https://github.com/casys-kaist/Capture) ・ リポジトリ内被引用：0  
  過去トークンを、すぐ使えるKVそのものと、K/Vを作る前のより小さい中間活性値の2形式で混在保存し、重み転送中に活性値からKVを再生成してPCIe転送量とGPU再計算量を釣り合わせる方式。
<!-- survey:auto:end -->
