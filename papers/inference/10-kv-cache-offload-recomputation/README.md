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
## 自動生成の論文一覧（53本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-10 | [LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference](2025-2510.09665-lmcache.md) | [✓](https://github.com/LMCache/LMCache) | 25 | LMCacheの本質は、KVキャッシュ（KV キャッシュ）を「1台のGPU上で1 リクエストのデコードを速くする一時バッファ」から、複数リクエスト・複数推論エンジン・複数保存 階層の間で保存・検索・転送できる独立データ オブジェクトへ昇格させることにある。同じ文書やシステム 入力を別リクエストが使うなら過去KVを再利用し。 |
| 2026-05 | [KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference](2026-2605.18071-kvdrive-holistic-multi-tier-kv-cache-management.md) | ✓ | 2 | 長文脈のデコードではKV キャッシュがGPU HBMに収まらないため、CPU DRAMへ退避し、注意機構に必要なKVだけをGPUへ戻す方式が使われる。しかし文脈やバッチが大きくなると、必要KVを探す処理とホスト→GPU転送がデコード時間の大きな割合を占める。またCPU DRAM自体も容量上限があるためSSDまで使う必要があるが。 |
| 2025-11 | [LiteCache: A Query Similarity-Driven, GPU-Centric KVCache Subsystem for Efficient LLM Inference](2025-2511.14510-litecache-gpu-centric-kv-offloading.md) | ✓ | 2 | LiteCacheは、長文LLMでKVキャッシュをCPUへ退避し必要なtop-kだけGPUへ戻す方式が、細粒度キャッシュ管理をCPUで行うためCPU処理・同期・カーネル起動がボトルネックとなり、CUDAグラフも使いにくい問題を扱う。隣接デコード段階の同一注意ヘッドではクエリ方向が似てtop-k KV集合も大きく重なる観測から。 |
| 2026-08 | [Heterogeneous LLM Serving with General-Purpose Processing-Near-Memory for Retrieval-Based Sparse Attention](2026-2608.03555-karat-pnm-retrieval-sparse-attention.md) | ✓ | 1 | 100万トークン級の長文で検索型疎注意を使うLLMでは、毎ステップ読むKV量は減っても全KVキャッシュと索引キーの保存容量は減らない。KARATはKVと索引を大容量LPDDR搭載の汎用処理近傍メモリへ移し、GPUを重み・MoE計算へ専念させ、異種デバイス間をマイクロバッチでパイプライン化することで、同一電力制約下の同時実行数とデコード処理量を高める。 |
| 2026-08 | [Cross-Model KV Cache Transfer in LLM Families: A Closed-Form Linear Mapping for Prefill Reuse](2026-2608.03893-cross-model-kv-cache-transfer.md) | ✓ | 1 | 同一モデル系列の大小モデルを途中で切り替える運用では、受信側モデルが蓄積済み文脈を最初からプリフィルし直すため、長い会話ほど切替コストが大きくなる。本論文は送信元モデルのKVキャッシュを受信先のKV表現へ直接写像し、再プリフィルを省く。KVヘッド数とヘッド次元が一致するモデル対では層間KVに強い線形構造があることを示し。 |
| 2026-05 | [VeriCache: Turning Lossy KV Cache into Lossless LLM Inference](2026-2605.17613-vericache-lossless-kv-compression.md) | ✓ | 1 | 長文LLM推論ではKVキャッシュを間引き・量子化するとGPUメモリ使用量と転送量を減らせる一方、各トークンで生じる小さな分布差が生成列全体で累積し、コード生成や関数呼び出しでは形式上自然でも機能的に誤った出力へ崩れる。VeriCacheは圧縮KVキャッシュを高速な候補生成にだけ使い。 |
| 2026-05 | [Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving](2026-2605.03375-tutti-making-ssd-backed-kv-cache-practical-for-long-context-llm-serving.md) | ✓ | 1 | NVMe SSD上へ退避したKVキャッシュを戻す際、CPUが大量の小さなI/O要求を発行する従来方式をやめ、GPU自身がSSDへの非同期I/Oを制御してKVをまとめて転送することで、SSD容量を使いながらDRAM基盤の キャッシュに近い推論性能を狙うシステム。 |
| 2026-04 | [HybridGen: Efficient LLM Generative Inference via CPU-GPU Hybrid Computing](2026-2604.18529-hybridgen-efficient-llm-generative-inference-via-cpu-gpu-hybrid-computing.md) | ✓ | 1 | 長文生成では巨大化したKVキャッシュをCPUへ退避すると転送量が増え、CPU側で注意機構を計算すると今度はCPU計算が律速になる。HybridGenはKVキャッシュをCPU側とGPU側へ分け、各側が手元のKVに対する注意スコアを並列計算し、GPUで結合・正規化する。さらにCPUが次層の計算を投機的に先行し。 |
| 2026-03 | [TTKV: Temporal-Tiered KV Cache for Long-Context LLM Inference](2026-2604.19769-ttkv-temporal-tiered-kv-cache.md) | ✓ | 1 | TTKVは、長文推論で増え続けるKVキャッシュを、最近のトークンを置くGPU HBMの高速階層と、古いトークンを圧縮して置くホストDRAMの低速階層に分ける。単なる退避ではなく、キーを8ビット、値を4ビットで差分量子化し、低速階層を128トークン単位のブロックに整理する。デコード時は必要度の高いブロックだけを非同期に先読みし。 |
| 2026-01 | [SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips](2026-2601.20309-superinfer-slo-aware-rotary-scheduling-and-memory-management-for-llm-inference-on-superchips.md) | [✓](https://github.com/Supercomputing-System-AI-Lab/SuperInfer) | 1 | SuperInferは、KV キャッシュ不足時にリクエストを単純に待たせる・スワップするだけでは、高い-読み込み時に先に入った長いリクエストが後続を塞ぐ ヘッド-of-line blocking が起き、user-facing 遅延目標を守れない問題を扱う。 |
| 2025-12 | [CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving](2025-2512.11920-cxl-speckv-fpga-disaggregated-kv.md) | ✓ | 1 | 長文脈LLMのKVキャッシュをGPU HBMだけに保持できない問題に対し、CXL接続メモリへ低温KVを退避し、FPGAで圧縮・展開とDMA制御を行う階層メモリ方式である。論文はさらに小型LSTMで将来トークンを予測し、将来位置のKVをGPU側へ投機的に先読みすると説明する。監査では、会議採録と公開実装の存在は確認できた一方。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](2026-2609.04852-kvmem-virtualizing-million-token-agent-workspaces.md) | [✓](https://github.com/kvmem/kvmem-qw3) | 0 | KVMemは「100万トークンをGPUで一度に注意機構する」仕組みではない。エージェントが過去に処理した100万トークン規模の履歴を検索可能な論理ワークスペースとして保持し、その時の質問に必要な一部だけをモデル本来の文脈 窓へ戻して推論する仕組みである。しかも古い履歴をテキストとして保存するのではなく、すでに計算済みのKV キャッシュをGPU。 |
| 2026-09 | [CacheBridge: Efficient Cross-Model KV Cache Transfer](2026-2609.00891-cachebridge.md) | ✓ | 0 | CacheBridgeを理解するには、まず「なぜ別のLLMへ会話を渡すだけで長い再計算が必要なのか」を押さえる必要がある。 |
| 2026-08 | [OasisKV: Scaling In-Decode KV Cache Beyond HBM with Lookahead Sparse Prefetching](2026-2608.08097-oasiskv-lookahead-sparse-prefetching.md) | ✓ | 0 | OasisKVは、長文LLMのデコードで完全KVキャッシュをGPU HBMへ保持するとバッチ数が制限され、CPU・遠隔メモリへ置いて必要時に取得するとPCIeやネットワーク転送がクリティカルパスになる問題を扱う。投機的デコードのドラフトトークンを一段先の注意予測信号として再利用し。 |
| 2026-08 | [Minima-KV: Retention-Preserving KV Cache Compression with Mixed-Format Paged Attention](2026-2608.23834-minima-kv-mixed-format-paged-attention.md) | ✓ | 0 | 長文推論のKVキャッシュを一律の精度で保持するとHBM容量と帯域を消費する一方、重要度が低いと判断した過去トークンを削除する方式は、後から注意が戻った位置を参照できない。Minima-KVは稼働中要求の論理KVページを削除せず、最近のページと保護対象の古いページをFP8。 |
| 2026-08 | [Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap](2026-2608.23658-elastic-kv-cache.md) | ✓ | 0 | この論文は、提案機構そのものよりも「複雑な仕組みを作って正しく動かしたが、もっと単純な既存設定がほぼ同じ問題を解いていた」という否定的な結果が重要な研究である。 |
| 2026-07 | [No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs](2026-osdi26-directkv-no-buffer-no-bottleneck-efficient-zero-copy-kv-cache-offloading-for-long-context-llms.md) | [✓](https://github.com/shutianluo/DirectKV) | 0 | DirectKVは、長文脈でGPU HBMに収まらなくなるKVキャッシュをCPU メモリへ置きながら、注意機構実行前にKVをGPU バッファへコピーしないゼロコピー オフロード システムである。 |
| 2026-07 | [Learning Agent Execution for KV-Cache Management in Agentic Serving](2026-2608.14624-cachescout.md) | ✓ | 0 | CacheScoutが対象にするのは、一つのLLMを繰り返し呼ぶ普通の対話ではなく、複数のLLMエージェントが役割分担するシステムである。 |
| 2026-07 | [DualDecoder: Accelerate Long Context LLM Inference by Predictive Prefetch](2026-2607.26475-dualdecoder-predictive-prefetch.md) | ✓ | 0 | 長文LLMで疎なKVキャッシュだけをGPUへ読み込む方式は、KV本体を減らしても検索や再構成に使う補助状態を全層分GPUへ常駐させるため、実際のメモリ節約が小さくなりやすい。DualDecoderは、直前に投機生成したトークンから次トークンが参照しそうなKV位置を予測し。 |
| 2026-07 | [A Photonic-CXL Memory Appliance for Scalable KV Cache Management in LLM Inference](2026-2607.27187-photonic-cxl-memory-appliance-kv-cache.md) | ✓ | 0 | 大規模LLM配信では、長文・複数ターン会話のKVキャッシュをGPU HBMだけに保持できず、CPU側DRAMやSSDへ階層化すると容量は増えるが、再利用時の転送帯域と遅延が新たなボトルネックになる。本論文は、CXL 3.1の共有メモリを受動光ファイバ網で16ホストへ接続するフォトニックCXLメモリアプライアンスを設計し。 |
| 2026-07 | [A CXL Memory Rack for Multi-Turn LLM Serving](2026-2607.18141-hymcache-cxl-hybrid-memory-kv-cache.md) | ✓ | 0 | 複数ターンLLMでは過去の接頭辞から得たKVキャッシュを再利用するとプリフィル計算を省ける一方、共有KVをTB級まで蓄えるとGPU HBMや通常DRAMの容量単価が問題になる。HyMCacheは、小容量のデバイス内DRAMと大容量SSDをCXLインターフェースの背後で一つのメモリ領域として見せるCXLハイブリッドメモリを使い。 |
| 2026-06 | [SwiftCache: Efficient LLM Serving for Multi-turn Conversations with Heterogeneous KV Cache Sharing](2026-2606.16135-swiftcache-heterogeneous-kv-cache-sharing.md) | ✓ | 0 | SwiftCacheの発想は、CPUやSSDへKV キャッシュを逃がす前に、同じserver内で別モデルが使っていないGPU メモリを借りられないかというものだ。長い会話を処理するモデルを主モデル（マスター）、KV需要が小さいモデルを作業モデル（ワーカー）として。 |
| 2026-06 | [PolyKV: Heterogeneous Retention and Allocation for KV Cache Compression](2026-2606.15157-polykv-heterogeneous-kv-retention-allocation.md) | ✓ | 0 | 長文脈LLMのKVキャッシュ圧縮では、従来は全Transformer層へ同じ追い出し規則とほぼ同じ容量を適用することが多い。PolyKVは、層ごと・プリフィル/デコード段階ごとに『どの既存追い出し方式を使うか』と『何トークン分のKV容量を与えるか』を別々に選べる設計空間へ拡張する。小さな校正集合でFullKVとの差を層単位に測り。 |
| 2026-05 | [Adaptive KV Cache Reuse for Fast Long-Context LLM Serving](2026-2605.24022-cachetune-adaptive-kv-reuse.md) | ✓ | 0 | CacheTuneは、検索拡張生成や複数文書質問応答のように、再利用したい文書断片が最終入力の先頭に固定されない長文推論を対象とするKVキャッシュ再利用方式である。断片を個別に計算したKVを単純連結すると、本来は前方の別断片を参照して形成される層内表現が欠け、生成品質が落ちる。CacheTuneはKV列を周波数領域で解析し。 |
| 2026-04 | [DUAL-BLADE: Dual-Path NVMe-Direct KV-Cache Offloading for Edge LLM Inference](2026-2604.26557-dual-blade-nvme-direct-kv-offloading.md) | ✓ | 0 | メモリ制約の強い単一GPUエッジ環境でKVキャッシュをNVMe SSDへ退避すると、通常のmmap経路はOSページキャッシュが作業集合より小さい領域で激しくスラッシングし、さらにVFS・ファイルシステム・ブロック層の処理がSSD帯域を使い切れない。Dual-Bladeは、利用可能なページキャッシュ量に収まるKVだけを通常経路へ置き。 |
| 2026-04 | [CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration](2026-2604.25080-cacheflow.md) | ✓ | 0 | CacheFlowが扱うのは、「前に一度計算した長い文脈をもう一度使いたいが、そのKVキャッシュはGPUメモリから追い出されている」という状況である。 |
| 2026-03 | [Swarm: Co-Activation Aware KVCache Offloading Across Multiple SSDs](2026-2603.17803-swarm-co-activation-aware-kvcache-offloading-across-multiple-ssds.md) | ✓ | 0 | 注意機構で一緒に参照されやすいKV キャッシュを事前にまとめ、そのグループ内のKVを複数SSDへ分散配置することで、1回のKV読み出しを複数SSDから並列に行い、単一SSDの帯域上限を超える実効I/O帯域を得る方式。 |
| 2026-03 | [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](2026-2603.27138-scoutattention-efficient-kv-cache-offloading-layer-ahead-cpu-precomputation.md) | ✓ | 0 | 長文脈のKVキャッシュの大部分をCPU DRAMへ置きながら、GPUにある重要ブロックはGPU、CPUにしかない重要ブロックだけはCPUで注意機構を計算し、さらに次層でCPUが担当する注意機構を1層早く開始することで、KV転送待ちとCPU計算待ちの両方を減らす。 |
| 2026-02 | [ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs](2026-2602.07721-pariskv-fast-drift-robust-kv-cache-retrieval.md) | ✓ | 0 | 完全精度のKV キャッシュをCPU DRAMへ置いたまま、GPU上の小さなキー要約だけで現在のクエリに重要なトークンを二段階検索し、選ばれたKVだけをGPUからCPU メモリへ直接読みに行くことで、長い生成中に検索indexが古くなる問題とCPU検索・CPU主導転送の待ち時間を同時に減らすKV 検索 システム。 |
| 2026-02 | [PAM: Processing Across Memory Hierarchy for Efficient KV-centric LLM Serving System](2026-2602.11521-pam-processing-across-memory.md) | ✓ | 0 | 大規模言語モデルの逐次生成では、KVキャッシュの容量と注意計算に必要なメモリ帯域が同時に増える。安価なDDRやSSDへKVを置くだけでは、最下層に多数のKVが集中して低帯域側が新たな律速になる。PAMはHBM・DDR・SSDの各階層へメモリ内処理（Processing-In-メモリ; PIM）機能を持たせ。 |
| 2026-02 | [KEEP: A KV-Cache-Centric Memory Management System for Efficient Embodied Planning](2026-2602.23592-keep-kv-cache-centric-embodied-memory.md) | ✓ | 0 | 長期の具身計画では、エージェント状態、物体状態、過去行動、完了タスクなどの記憶を毎ステップの長い入力へ含める。生成する行動は短い一方、入力は数万トークンになり得るため、プリフィルが計画遅延の大半を占める。同じ記憶片のKVキャッシュを再利用すれば計算を省けるが、物体状態のような動的記憶が変わると。 |
| 2026-02 | [HillInfer: Efficient Long-Context LLM Inference on the Edge with Hierarchical KV Eviction using SmartSSD](2026-2602.18750-hillinfer-smartssd-hierarchical-kv-eviction.md) | ✓ | 0 | 長文LLMをメモリ制約の厳しいPCで動かす際、GPU・CPUだけではKVキャッシュを保持しきれずSSDへ退避すると、毎デコード段で重要度評価のため大量KVを読み戻す入出力が支配的になる。HillInferは、完全な注意計算ではなくトークン重要度の軽量な内積評価だけをSamsung SmartSSD内のFPGAへ移し。 |
| 2026-02 | [ForesightKV: Optimizing KV Cache Eviction for Reasoning Models by Learning Long-Term Contribution](2026-2602.03203-foresightkv-long-term-contribution-eviction.md) | ✓ | 0 | 長い推論連鎖ではKVキャッシュが生成長に比例して増えるが、現在の注意だけで重要度を決める追い出し方式は、今は目立たなくても数百〜数千トークン後に再利用される意味依存KVを捨てやすい。ForesightKVは完全な推論軌跡の将来注意を使うGolden 追い出しで『将来一度でも強く参照されるKV』を教師化し。 |
| 2026-02 | [Efficient Remote KV Cache Reuse with GPU-native Video Codec](2026-2602.09725-kvfetcher-gpu-native-media-asic.md) | ✓ | 0 | 遠隔KVキャッシュ再利用では、同じ接頭辞のKVキャッシュを別ノードやストレージから取得して長いプリフィル計算を省ける一方、一般的なクラウドの数十Gbps以下のネットワークでは転送時間が利益を打ち消す。既存の圧縮方式は転送量を減らせても、CUDAコアを使う展開処理が推論と競合したり。 |
| 2026-02 | [CHESS: Context-aware Hierarchical Efficient Semantic Selection for Long-Context LLM Inference](2026-2602.20732-chess-context-aware-hierarchical-selection.md) | ✓ | 0 | CHESSは長文推論のKVキャッシュを単純に削るのではなく、現在の生成文脈に意味的に関連するページを毎段階で再構成するアルゴリズム・システム協調設計である。KVをGrid→Chunk→Pageの三階層の論理表現で要約し。 |
| 2025-12 | [Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading](2025-2601.19910-understanding-bottlenecks-kv-offloading.md) | ✓ | 0 | 本研究は新しいKV オフロード ランタイムを提案するのではなく、CPU DRAMからKVを戻す費用が、prefix キャッシュで節約したプリフィル計算をいつ上回るのかを定量化する。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-11 | [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md) | [✓](https://github.com/NEO-MLSys25/NEO) | 20 | NEOは、GPU メモリ不足でKV キャッシュを十分に保持できずバッチ 大きさが小さくなる問題に対して、一部リクエストのデコード 注意機構とKV キャッシュだけをローカル CPUへ移すオンライン LLM 推論 システムである。 |
| 2024-03 | [FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines](2024-2403.11421-fastdecode-high-throughput-gpu-efficient-llm-serving-using-heterogeneous-pipelines.md) | ✓ | 18 | FastDecodeは、KV キャッシュをCPU メモリへ退避するだけではPCIe転送がボトルネックになる問題に対し、KV キャッシュだけでなく、それを利用するアテンション計算もCPU側へ移すLLM 推論提供 システムである。 |
| 2024-10 | [ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference](2024-2410.21465-shadowkv-low-rank-key-value-offload.md) | [✓](https://github.com/ByteDance-Seed/ShadowKV) | 17 | ShadowKVは、長文LLMでKVキャッシュをGPUへ全保持するとバッチ数が制限され、CPUへ全退避すると疎なKVを毎トークン取得するPCIe遅延が大きい問題を扱う。回転位置埋め込み適用前のキーが系列ごとに強い低ランク構造を持つことを利用し、キーの低ランク表現・チャンク代表値・少数の外れ値だけGPUへ残し。 |
| 2024-11 | [KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation](2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md) | [✓](https://github.com/chaoyij/KVPR) | 10 | KVPRは、KV キャッシュをCPU DRAMへオフロードしたときにPCIe転送がデコードのボトルネックになる問題に対し、KV キャッシュの一部を転送せずGPUで再計算する研究である。 |
| 2024-09 | [InstAttention: In-Storage Attention Offloading for Cost-Effective Long-Context LLM Inference（preprint: InstInfer）](2024-2409.04992-instattention-instinfer-in-storage-attention-offloading.md) | ✓ | 9 | InstAttentionは、SSDへKV キャッシュを置く従来オフロードではデコードのたびにKVをSSD→ホスト→GPUへ読み戻すI/Oがボトルネックになる問題を、アテンション計算そのものをストレージ側へ移すことで解消する。 |
| 2025-05 | [RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference](2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md) | ✓ | 8 | 長文脈のKV キャッシュをCPU メモリ上のベクトル 保存として検索対象にし、注意機構に重要なトークンだけをGPUへ取り出すことで、全KVをGPUへ保持・走査するメモリ容量と帯域を減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論システム。 |
| 2024-11 | [Pie: Pooling CPU Memory for LLM Inference](2024-2411.09317-pie-pooling-cpu-memory-for-llm-inference.md) | ✓ | 6 | Pieは、KV キャッシュをCPU メモリへオフロードするとGPU メモリは空く一方、必要になってからスワップインするとCPU→GPU転送待ちがデコード 遅延へ直接乗る問題に対し、次に使う層のKVを事前に読み戻し、現在のGPU計算と転送を重ねる研究である。 |
| 2024-07 | [Aqua: Network-Accelerated Memory Offloading for LLMs in Scale-Up GPU Domains](2024-2407.21255-aqua-network-accelerated-memory-offloading-for-llms-in-scale-up-gpu-domains.md) | [✓](https://github.com/aquaml/aqua) | 6 | Aquaは、LLM 推論提供で要求が一時的に集中してKV キャッシュがHBMを使い切ると、後続要求が長く待たされTTFTが悪化する問題を扱う。 |
| 2025-03 | [SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs](2025-2503.16163-specache-speculative-kv-caching.md) | ✓ | 3 | Transformerの逐次生成では、過去トークンのキー/値をKVキャッシュ（KV キャッシュ）として保存する。これがあるため、次トークンを生成するたびに過去トークン全体のキー/値を再計算する必要はない。一方でKV キャッシュは文脈長にほぼ比例して増え、長文を扱うほどGPU VRAMを圧迫する。 |
| 2025-09 | [ShadowServe: Interference-Free KV Cache Fetching for Distributed Prefix Caching](2025-2509.16857-shadowserve-smartnic-kv-fetching.md) | ✓ | 2 | ShadowServeは、分散接頭辞キャッシュで圧縮KVキャッシュを遠隔保存先から取得するとき、GPU上の復号・逆量子化がLLMのデコード計算と同じ演算資源・メモリ帯域を奪い合う問題を、SmartNICを独立したKVデータ処理階層として使うことで解決する。ホストCPUは取得要求を非同期管理する制御面だけを担当し、ネットワーク取得、Deflate展開。 |
| 2025-02 | [HeadInfer: Memory-Efficient LLM Inference by Head-wise Offloading](2025-2502.12574-headinfer-head-wise-kv-offloading.md) | [✓](https://github.com/wdlctc/headinfer) | 2 | HeadInferの中心は、「1 層分のKV キャッシュすらGPUへ丸ごと戻す必要はない」という点にある。Multi-Head 注意機構では各注意機構 ヘッドを独立に計算し、最後に結果を連結できる。そこで全KVの正本をCPU DRAMへ置き。 |
| 2024-10 | [Compute Or Load KV Cache? Why Not Both?](2024-2410.03065-cake-compute-or-load-kv-cache.md) | ✓ | 2 | Cakeは、長文接頭辞のKVキャッシュがSSDや遠隔ストレージに保存されているとき、GPUで最初から再計算するか低帯域I/Oから全量を読み込むかの二者択一をやめ、両資源を同時に使って初回トークン待ち時間を最小化する。入力をチャンク化し、GPUは先頭から順方向へKVを再計算する一方、I/O処理は末尾から逆方向へ保存済みKVを読み込み。 |
| 2025-08 | [TokenLake: A Unified Segment-level Prefix Cache Pool for Fine-grained Elastic Long-Context LLM Serving](2025-2508.17219-tokenlake-segment-prefix-cache-pool.md) | ✓ | 1 | TokenLakeは、GPUクラスタ上の接頭辞KVキャッシュを各推論インスタンスの所有物として扱うために生じる負荷偏り、重複保存、空き領域の断片化を、全GPUをまたぐ統一セグメント単位キャッシュプールへ置き換える。宣言型インターフェースでクエリテンソルと接頭辞注意機構をキャッシュ管理側へ公開し。 |
| 2025-07 | [Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System](2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md) | ✓ | 1 | この研究は、GH200のように高速HBMと大容量LPDDRを高速接続網で組み合わせられるハードウェアで、どのKVを高速で小さいメモリへ置き、どのKVを遅い代わりに大容量のメモリへ置くべきかを扱う。 |
| 2025-06 | [APEX: Asynchronous Parallel CPU-GPU Execution for Online LLM Inference on Constrained GPUs](2025-2506.03296-apex-asynchronous-parallel-cpu-gpu-execution-for-online-llm-inference-on-constrained-gpus.md) | ✓ | 1 | APEXは、NEOやFastDecodeと同じくKV キャッシュとデコード アテンションの一部をCPUへ移してGPU メモリを空けるが、主眼はCPU オフロードそのものではなく、CPUとGPUをどう重ねて実行するかにある。 |
| 2025-09 | [TRACE: Unlocking Effective CXL Bandwidth via Lossless Compression and Precision Scaling](2025-2509.03377-cxl-ndp-transparent-near-data-processing.md) | ✓ | 0 | CXL拡張メモリはGPU HBMより大容量・低価格だが、リンク帯域と装置側DRAM帯域が低く、LLMの重みやKVキャッシュを退避すると転送量が性能を支配しやすい。トレースはホスト側のCXL.memインターフェースを変えず、装置内部で数値をビット位置ごとに並べ替えて高圧縮な無損失表現へ変換し。 |
| 2025-01 | [Throughput-Oriented LLM Inference via KV-Activation Hybrid Caching with A Single GPU](2025-2501.01792-throughput-oriented-llm-inference-via-kv-activation-hybrid-caching-with-a-single-gpu.md) | [✓](https://github.com/casys-kaist/Capture) | 0 | 取得は、モデル 重みとKV キャッシュの両方をホスト メモリへオフロードするスループット重視推論で、過去トークンの状態を、KVそのものとして保存するか、K/Vを作る直前の小さい中間活性値として保存するかを混在させるシステムである。 |
<!-- survey:auto:end -->
