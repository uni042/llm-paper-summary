---
canonical_id: DOI:10.52202/085713-1587
doi: 10.52202/085713-1587
title: 'HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference'
summary: HiFCは、長文脈LLM推論でGPU HBMから溢れるKVキャッシュを高価なホストDRAMではなく市販NVMe SSDへ直接退避する方式である。GPUダイレクトストレージ（GPU Direct Storage; GDS）でGPUとSSDを直結し、擬似SLC領域、追記型の順次ブロック配置、4 KB整列を組み合わせてSSDのランダム書込み低下と摩耗を抑える。vLLMの系列パイプラインがSSD交換遅延を計算と重ねることで、DRAM交換に近いエンドツーエンド性能を維持しながら大容量KV領域の費用を削減する。
list_summary: GPUとNVMe SSDをGDSで直結し、pSLCと順次KVブロック配置でDRAMなしのKV交換を実現し、長文脈推論の性能を保ちながら容量費用を削減する。
authors:
- Inho Jeong
- Sunghyeon Woo
- Sol Namkung
- Dongsuk Jeon
published: '2025-12-02'
publication: Advances in Neural Information Processing Systems 38 (NeurIPS 2025) Main Conference Track
publication_type: Conference paper
publication_status: Published
lineage: KV cache offload / SSD swapping / GPU Direct Storage
topics:
- KVキャッシュ
- SSDオフロード
- GPUダイレクトストレージ
- 長文脈推論
importance: 市販SSDをDRAM代替のKV交換層として実機統合し、性能、耐久性、総所有費用を同時評価したストレージ階層型LLM推論研究。
hardware_evaluation: Dell PowerEdge R750xa、2基のIntel Xeon Silver 4310、2基のNVIDIA A100 80 GiB、256 GiB DDR4、1 TB NVMe Gen4 SSDの200 GiB pSLC領域を用いた実機評価。
quality_effect: KVキャッシュ内容を近似・圧縮する手法ではなく保存場所と転送経路を変更するため、数値品質を意図的に劣化させない。
references_checked_at: '2026-09-19'
references_source: primary-reference-section
references_total: 36
source: https://papers.nips.cc/paper_files/paper/2025/file/4431224d3762aa655f0aee4eaf04ff16-Paper-Conference.pdf
sources:
- https://papers.nips.cc/paper_files/paper/2025/hash/4431224d3762aa655f0aee4eaf04ff16-Abstract-Conference.html
- https://papers.nips.cc/paper_files/paper/2025/file/4431224d3762aa655f0aee4eaf04ff16-Paper-Conference.pdf
implementation: vLLM v0.6.6へフラッシュキャッシュブロック割当器とGDS対応キャッシュエンジンを統合。CUDA Toolkit 12.3、PyTorch 2.5.1、GDS 1.8.1.2で評価。
last_checked: '2026-09-19'
code: null
references: []
last_audited: null
audit_version: 0
---

# HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference

> GPUとNVMe SSDをGDSで直結し、pSLCと順次KVブロック配置でDRAMなしのKV交換を実現し、長文脈推論の性能を保ちながら容量費用を削減する。
## 書誌情報
- **著者**: Inho Jeong, Sunghyeon Woo, Sol Namkung, Dongsuk Jeon
- **公開**: Advances in Neural Information Processing Systems 38 (NeurIPS 2025) Main Conference Track
- **種別**: Conference paper
- **対象**: KVキャッシュ、SSDオフロード、GPUダイレクトストレージ、長文脈推論
- **実装**: vLLM v0.6.6へフラッシュキャッシュブロック割当器とGDS対応キャッシュエンジンを統合。CUDA Toolkit 12.3、PyTorch 2.5.1、GDS 1.8.1.2で評価。
## 概要
HiFCは、長文脈LLM推論でGPU HBMから溢れるKVキャッシュを高価なホストDRAMではなく市販NVMe SSDへ直接退避する方式である。GPUダイレクトストレージ（GPU Direct Storage; GDS）でGPUとSSDを直結し、擬似SLC領域、追記型の順次ブロック配置、4 KB整列を組み合わせてSSDのランダム書込み低下と摩耗を抑える。vLLMの系列パイプラインがSSD交換遅延を計算と重ねることで、DRAM交換に近いエンドツーエンド性能を維持しながら大容量KV領域の費用を削減する。

HiFCはホストDRAMをKV交換経路から完全に外し、市販NVMe SSDの擬似SLC領域をGPUの直接交換先としてvLLMへ組み込む。GPUダイレクトストレージでGPUメモリとSSDを直接DMA転送し、フラッシュキャッシュ専用ブロック割当器が追記型に物理順序を維持することで、高速な順次I/Oへ変換する。さらに4 KB整列した層別キー・バリュー領域のオフセットを事前計算し、実行時のアドレス計算と断片化を抑える。専用計算ストレージを必要とせず、交換遅延をvLLMの系列並列実行の余裕時間へ隠す点が特徴である。

代表結果として、長文脈推論スループット差はDS-Llama-8B、DS-Qwen-14B、Mistral-7BとQasper/GovReport/NarrativeQAでDRAM KV交換に対して概ね1〜2%以内。SSDの生帯域差を系列パイプラインの計算重畳で隠し、DRAM交換相当の性能を維持する。
## 問題設定
長文脈や多数同時要求では、注意機構が再利用するキー・バリュー（KV）キャッシュが文脈長とバッチ数に比例して増え、GPU HBMを超える。vLLMは溢れたブロックをホストDRAMへ交換できるが、大容量DRAMは購入費と電力費が高い。NVMe SSDは安価で大容量だが、従来経路ではSSDからCPU DRAMを経由してGPUへ運ぶため余分なPCIe転送が発生し、ランダムな小書込みはSSD内部の書込み増幅とガベージコレクションを招いて帯域と寿命を悪化させる。このため単純なSSD置換ではDRAM交換と同じ性能を得にくい。
## 新規性
HiFCはホストDRAMをKV交換経路から完全に外し、市販NVMe SSDの擬似SLC領域をGPUの直接交換先としてvLLMへ組み込む。GPUダイレクトストレージでGPUメモリとSSDを直接DMA転送し、フラッシュキャッシュ専用ブロック割当器が追記型に物理順序を維持することで、高速な順次I/Oへ変換する。さらに4 KB整列した層別キー・バリュー領域のオフセットを事前計算し、実行時のアドレス計算と断片化を抑える。専用計算ストレージを必要とせず、交換遅延をvLLMの系列並列実行の余裕時間へ隠す点が特徴である。
## 手法
### 手法のあらまし
HiFCはvLLMのGPUブロックとCPUブロックに加えて、SSD上のフラッシュキャッシュブロックを導入する。デコードでHBMが不足すると、スケジューラは被害系列群を選び、そのKVブロックをフラッシュキャッシュへ追い出す。キャッシュエンジンはKVテンソル自体を4 KB整列GDSバッファとして再利用し、最大16スレッドのI/O発行でGPUからSSDへ直接書くため、CPU DRAMへの中継コピーを行わない。空いたGPUブロックは次の活動系列へ直ちに再割当され、他系列のデコードを継続する。追い出された系列が再開可能になると、同じ経路でSSDからGPUへKVを戻す。SSD側では固定サイズのフラッシュキャッシュブロックを古い論理アドレスへ再利用せず末尾へ追記し、物理的に連続した書込みを形成する。対象SSDでは200 GiBの擬似SLC領域だけをKV交換に使い、TLC領域への移行や大域的なランダム書込みを避ける。層、キー・バリュー種別、ブロック番号から4 KB境界のバイトオフセットを事前計算した表を使い、GDSへ直接渡す。SSDの生の交換帯域はDRAMより低いが、vLLMは複数系列をパイプライン化しており、ある系列の交換中に別系列を計算できる。交換時間がこのパイプライン余裕時間を超えない限り、SSD遅延はエンドツーエンド性能へ現れない。

### フラッシュキャッシュブロック割当器
vLLMの既存GPU・CPUブロック管理へSSD上のフラッシュキャッシュブロックを追加する。HBMが尽きるとスケジューラが被害系列を選び、その系列のKVブロックを固定サイズのSSDブロックへ割り当てる。ブロックは32〜128トークンなど既存のページ単位と互換にし、GPU側のブロック表と同じ粒度で追跡する。空き領域は古い位置をランダムに再利用せず末尾へ追記するため、論理的な交換イベントをSSDが得意な連続書込みへ変換できる。64トークン付近は交換効率と不要な交換・断片化の均衡点となり、大き過ぎるブロックでは余分な交換が増える。

### フラッシュ特性を考慮した配置とpSLC
市販TLC SSDのうち約200 GiBの擬似SLC領域をKV専用領域として使う。SLC相当では1セル1ビットとして扱うため書込み耐久性と持続帯域が高く、追記型の順次アクセスと組み合わせることで書込み増幅率を約1.02まで抑える。各層のキー領域とバリュー領域について4 KB LBA境界へ整列したバイトオフセットを事前計算し、GDS要求へ直接渡す。これにより実行時に散在する小領域を探索せず、層番号とKV種別から連続領域を決定できる。実測ではpSLC内の順次書込みが平均4.715 GiB/s、順次読出しが4.987 GiB/sである一方、ランダム書込みは1.617 GiB/sへ落ちる。さらにpSLC容量を越えて900 GiB範囲へ書くと1.689 GiB/sまで低下するため、性能はこの配置規律とSSD固有のpSLC挙動に依存する。

### GDS直接交換と遅延隠蔽
GPUダイレクトストレージ（GPU Direct Storage; GDS）を使い、GPU HBMとNVMe SSDの間をホストDRAMなしで直接転送する。キャッシュエンジンはCUDA側のKVテンソルを整列済みI/Oバッファとして利用し、複数スレッドで要求を並行発行する。交換そのものはDRAMより遅いが、vLLMのスケジューラは交換対象系列を一時停止して別の活動系列を実行するため、十分な同時系列があればI/O時間を計算の隙間へ隠せる。論文のモデルでは交換時間がパイプラインの許容停止時間を超えた場合だけ性能低下が表面化するので、短文脈や低並列では利点が弱くなる。

### 全体のデータ／制御の流れ
HiFCは専用計算ストレージを要求せず、GDS対応NVIDIA GPUと市販NVMe SSDをvLLMへ統合するソフトウェア方式である。GPU:SSDを1:1、複数GPUで1台共有、複数GPUと複数SSDの構成へ拡張できるが、共有時はSSD帯域の競合を避けるスケジューリングが必要になる。
## 評価条件
- **ハードウェア**: Dell PowerEdge R750xa、Intel Xeon Silver 4310×2、NVIDIA A100 80 GiB×2、256 GiB DDR4。HiFC用に1 TB NVMe Gen4 SSDの200 GiB pSLC領域、システム用にSamsung PM893 7.68 TB SATA SSDを使用。
- **ソフトウェア**: Ubuntu 22.04.5 LTS、vLLM v0.6.6、CUDA Toolkit 12.3、PyTorch 2.5.1、GDS 1.8.1.2。vLLMへフラッシュキャッシュ割当器とGDS交換機構を統合。
主評価はDeepSeek-R1-Distill-Qwen-32B。追加でDeepSeek-Llama-8B、DeepSeek-Qwen-14B、Mistral-7BをQasper、GovReport、NarrativeQAで評価。DRAM交換とHiFCを入力・出力長、同時系列数、ブロックサイズ、GPU:SSD構成を変えて比較し、gdsioで順次・ランダムI/O帯域、SMARTログで書込み増幅率、100 GiBまでのKV初期化時間、3年間の購入費・電力費も測定・推定した。
実GPUと市販NVMe SSDを用いたシステム実測であり、シミュレーションだけではない。ただしpSLC挙動と耐久性は製品依存で、評価は制御されたSSD構成に限定される。100B超モデルは未評価で、短文脈・低並列・共有SSDの帯域競合では結果が一般化しない可能性がある。
## 主要結果
HiFCは長文脈の実機評価でDRAM交換とほぼ同じエンドツーエンドスループットを維持し、複数モデル・データセットでも差を概ね1〜2%に抑えた。pSLC内の順次GDS読み書きは約4.7〜5.0 GiB/sを維持し、追記配置により書込み増幅率は1.02となった。128 GiB DRAMを1 TiB pSLC構成SSDで置き換える比較では、当初の3年間総費用を4.5分の1にし、更新価格では6.1分の1と推定している。

- 長文脈推論スループット差 / 概ね1〜2%以内 (比較対象: DRAM KV交換; 条件: DS-Llama-8B、DS-Qwen-14B、Mistral-7BとQasper/GovReport/NarrativeQA) — SSDの生帯域差を系列パイプラインの計算重畳で隠し、DRAM交換相当の性能を維持する。

- GovReportスループット / 182 トークン/s (比較対象: DRAM交換172 トークン/s; 条件: DS-Llama-8B、2 GPU環境の代表評価) — 専用GDS経路によりDRAM競合を避け、評価条件ではSSD交換が律速にならない。

- 書込み増幅率 / 1.02 (比較対象: SSD仕様上の代表値1.40; 条件: 232.5 GiBのKV追記交換) — 順次追記配置が内部の余分なNAND書込みを抑え、耐久性を改善する。

- 3年間メモリ拡張費 / $136、DRAM比4.5分の1 (比較対象: 128 GiB DRAM $614; 条件: 初期費用と電力費を含む論文主表のTCOモデル) — 大容量KV交換層としてSSDを使う経済的動機を定量化する。

- 100 GiB KV初期化時間 / 32秒 (比較対象: DRAM 90秒; 条件: 10〜100 GiBのセッション初期化比較) — 事前生成フラッシュキャッシュファイルを直接利用するため大容量で初期化が2.81倍高速になる。

### 負の結果・境界条件
- DRAMの生の交換帯域はHiFCより2倍以上高く、HiFCの優位はI/O自体の低遅延化ではなく重畳による隠蔽に依存する。pSLC内の順次書込みは平均4.715 GiB/sだがランダム書込みは1.617 GiB/s、900 GiB範囲へ広げた順次書込みも1.689 GiB/sまで低下する。128・256トークンの大ブロックでは64トークン付近より不要な交換が増える。短文脈や遅延敏感、共有SSD競合ではフラッシュ遅延が表面化し得る。

### 結果の読み方
十分な同時系列があると、ある系列をSSDへ交換する間に別系列のGPU計算を進められるため、交換時間がパイプライン余裕時間以内なら性能差が見えない。逆に並列度が低い場合やSSDアクセスがランダム化すると余裕時間を使い切り、DRAMとの差が現れる。HiFCは媒体そのものをDRAM並みに速くするのではなく、アクセス形状とスケジューリングをSSDに合わせる方式である。
## 品質への影響
KV値を近似変換せずそのまま退避・復元するため、方式自体による生成品質低下は想定しない。評価の主眼は性能、容量、耐久性、費用である。
## 既存研究との差
vLLM標準のDRAM交換はCPUメモリを容量層として使うのに対し、HiFCはDRAMを交換経路から外す。FlexGen型SSDオフロードがCPU DRAM中継を含むのに対しGDSでGPUとSSDを直結する。InstInferのような計算ストレージ方式はSSD側で注意計算を実行する専用CSDを必要とするが、HiFCは市販NVMe SSDへ通常のKVブロックを退避し、vLLMスケジューラでI/O遅延を隠す。AttentionStoreのDRAM/SSD階層とも異なり、オンライン長文脈推論でDRAMなしを狙う。
## 限界
短文脈または単一要求に近い低並列環境では、SSD交換遅延を別系列の計算で隠す余裕が小さく、トークン処理遅延が増える可能性がある。複数GPUが1台のSSDを共有する場合は帯域競合を避けるスケジューリングが必要である。安定した性能にはpSLC設定、ファイルシステム、LBA配置などSSD固有の調整知識を要する。評価SSDの耐久性と内部ガベージコレクション特性は製品依存であり、100B超モデルへの一般化も未検証である。
## 実装状態
vLLM v0.6.6を基盤にフラッシュキャッシュブロック割当、追記配置、CUDA/GDSキャッシュエンジンを実装し、市販A100 GPUとNVMe Gen4 SSDで実機評価している。新規データセットや事前学習モデルは公開せず、論文は実装方式と評価を報告する。
## 研究上の位置づけ
KVキャッシュの階層メモリ研究のうち、SSDを低価格な大容量交換層として実用化する系統に位置する。重要なのはSSDの遅さを単純に受け入れるのではなく、GDSによる中継排除、順次I/O化、pSLC耐久性、系列パイプラインによる遅延隠蔽を一体化し、性能だけでなく3年間費用と寿命まで設計指標へ含めた点である。
## 一次資料
- https://papers.nips.cc/paper_files/paper/2025/hash/4431224d3762aa655f0aee4eaf04ff16-Abstract-Conference.html
- https://papers.nips.cc/paper_files/paper/2025/file/4431224d3762aa655f0aee4eaf04ff16-Paper-Conference.pdf
