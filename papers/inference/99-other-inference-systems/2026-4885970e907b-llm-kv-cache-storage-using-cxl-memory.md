---
canonical_id: DOI:10.1109/LCA.2026.3720952
doi: 10.1109/LCA.2026.3720952
title: LLM KV Cache Storage Using CXL Memory
summary: 長文脈・多数同時要求では、注意機構の過去状態を保持するKVキャッシュがGPUの高帯域メモリ（High Bandwidth Memory; HBM）を圧迫し、容量超過時の再計算が推論性能を大きく落とす。本論文は、vLLMとLMCacheの同一ソフトウェア経路からKVキャッシュをCPU DRAMまたは4種類のCXLメモリへ退避し、保存先そのものの性能差を実機で比較する。DRAM型のCMM-D、スイッチ型のCMM-B、ネットワーク越しのメモリプールをホストから透過的なNUMA領域として見せるCMM-MP、DRAMキャッシュとNANDを組み合わせる大容量CMM-Hを評価した。Llama-3.1-8B-InstructとA100 40GBを用いた評価では、122Kトークン入力でCMM-D、CMM-B、CMM-MPがGPU VRAM基準に対して要求スループットを約9倍にし、初回トークン時間（Time to First Token; TTFT）を最大16分の1まで短縮した。CMM-Hは性能を抑える代わりに大容量・低コスト側へ設計点を移すことを示す。
list_summary: vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。
authors:
- Kwan Huen
- Gongjin Sun
- Mehdi Nik
- Caroline Kahn
- Elham Movahedian
- Senthil Murugesapandian
- Michael Wasef
- Shuyu Lyu
- Dongyang Li
- Edmund Au
- Brian Luu
- Jason Scott
- Ranjitha Gopalakrishna
- Namita Kumar
- Amir Beygi
- Vitorio Cargnini
- Ramdas Kachare
authors_affiliations: メモリ Solutions Lab, Samsung Semiconductor, Inc., San Jose, CA, USA
published: '2026-01-01'
publication: IEEE Computer Architecture Letters, January 2026
publication_type: Journal Article
publication_status: Accepted for publication
publication_version: Author accepted manuscript
lineage: KVキャッシュ・階層メモリ・CXLオフロード
topics:
- KVキャッシュ
- CXLメモリ
- 階層メモリ
- オフロード
- 長文脈推論
- メモリ分離
importance: CXLを単一のDRAM拡張器だけでなく、スイッチ型プール、ネットワーク透過型プール、DRAMとNANDのハイブリッドまで同じvLLM・LMCache経路で比較しており、KVキャッシュの階層メモリ設計で性能・容量・分離性を選ぶための実測資料になる。
hardware_evaluation: 実機評価。デュアルソケットIntel Xeon、512GB DDR5、NVIDIA A100 40GBと複数のSamsung CXL試作・製品系デバイスを使用。
hardware_details: ホストは各ソケット64コアのIntel Xeon、512GB DDR5-4800。GPUはNVIDIA A100 40GB HBM2e。CXL対象はCMM-D 256GB、CMM-B、6台288GBのCMM-MP、3.84TB SSDを背後に持つCMM-H。
quality_effect: 近似計算やKV量子化ではなく、既に計算したKV状態の保存場所を変える方式であるため、方式自体はモデル出力品質を変更しない。論文は生成品質指標の差を評価しておらず、性能と容量を中心に測定している。
storage_targets:
- GPU HBM
- CPU DRAM
- CXL DRAM
- CXLメモリプール
- CXL DRAM-NANDハイブリッド
bottlenecks:
- GPU HBM容量
- KVキャッシュ再計算
- 退避先の帯域と遅延
- 大容量化に伴う共有メモリ不足
evidence_locations:
- I. Introduction
- II. Background and Motivation
- III. Design and Implementation
- IV. Evaluation
- V. Conclusion
- References
references:
- canonical_id: arXiv:2510.09665
  arxiv_id: '2510.09665'
- canonical_id: arXiv:2508.18572
  arxiv_id: '2508.18572'
- canonical_id: arXiv:2412.12491
  arxiv_id: '2412.12491'
references_checked_at: '2026-09-25'
references_source: primary-reference-section
references_total: 13
source: https://doi.org/10.1109/LCA.2026.3720952
sources:
- https://doi.org/10.1109/LCA.2026.3720952
- https://www.researchgate.net/publication/411814165_LLM_KV_Cache_Storage_using_CXL_Memory
implementation: vLLM 0.19.0+cu128とLMCache 0.4.2を使う実機構成で、単一ソケット向けの非同期取得処理を複数OSスレッドへ変更してLMCache側の取得性能を高めている。CXLデバイスはCPUを持たないNUMAノードとして公開し、LMCache本体は変更せず既存のメモリ確保経路を使う。公開コードURLは確認できない。
implementation_status: 研究用の実機統合・評価。CXL側は製品系デバイスと概念実証（proof of concept; PoC）を含む。
evaluation_type: Real-hardware systems evaluation
last_checked: '2026-09-25'
audit_version: 0
code: null
last_audited: null
---

# LLM KV Cache Storage Using CXL Memory

> vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。
## 書誌情報
- **著者**: Kwan Huen, Gongjin Sun, Mehdi Nik, Caroline Kahn, Elham Movahedian, Senthil Murugesapandian, Michael Wasef, Shuyu Lyu, Dongyang Li, Edmund Au, Brian Luu, Jason Scott, Ranjitha Gopalakrishna, Namita Kumar, Amir Beygi, Vitorio Cargnini, Ramdas Kachare
- **著者・所属**: メモリ Solutions Lab, Samsung Semiconductor, Inc., San Jose, CA, USA
- **公開**: IEEE Computer Architecture Letters, January 2026
- **種別**: Journal Article
- **対象**: KVキャッシュ、CXLメモリ、階層メモリ、オフロード、長文脈推論、メモリ分離
- **実装**: vLLM 0.19.0+cu128とLMCache 0.4.2を使う実機構成で、単一ソケット向けの非同期取得処理を複数OSスレッドへ変更してLMCache側の取得性能を高めている。CXLデバイスはCPUを持たないNUMAノードとして公開し、LMCache本体は変更せず既存のメモリ確保経路を使う。公開コードURLは確認できない。
## 概要
長文脈・多数同時要求では、注意機構の過去状態を保持するKVキャッシュがGPUの高帯域メモリ（High Bandwidth Memory; HBM）を圧迫し、容量超過時の再計算が推論性能を大きく落とす。本論文は、vLLMとLMCacheの同一ソフトウェア経路からKVキャッシュをCPU DRAMまたは4種類のCXLメモリへ退避し、保存先そのものの性能差を実機で比較する。DRAM型のCMM-D、スイッチ型のCMM-B、ネットワーク越しのメモリプールをホストから透過的なNUMA領域として見せるCMM-MP、DRAMキャッシュとNANDを組み合わせる大容量CMM-Hを評価した。Llama-3.1-8B-InstructとA100 40GBを用いた評価では、122Kトークン入力でCMM-D、CMM-B、CMM-MPがGPU VRAM基準に対して要求スループットを約9倍にし、初回トークン時間（Time to First Token; TTFT）を最大16分の1まで短縮した。CMM-Hは性能を抑える代わりに大容量・低コスト側へ設計点を移すことを示す。

本論文の新規性は、CXLを一種類のDRAM拡張器として測るのではなく、直接接続のDRAM型CMM-D、CXLスイッチで複数デバイスを束ねるCMM-B、バックエンド通信までデバイス側で処理して遠隔DRAMを一つのNUMA領域として見せるCMM-MP、DRAMキャッシュの背後にNANDを置くCMM-Hという4つの設計点を、同じvLLM・LMCache経路と同じモデル・負荷で比較した点にある。特にメモリプール型とDRAM-NANDハイブリッド型をKVキャッシュ退避で同一条件に置き、分離性や容量を増やしてもDRAM型ではシステムDRAMに近い性能を保てること、NAND型では容量と性能の交換条件が明確になることを示す。
## 問題設定
長文脈や多数同時要求では、自己注意で再利用する鍵・値テンソルを保持するKVキャッシュが入力長と同時要求数にほぼ比例して増える。GPU HBMに収まらなくなると、キャッシュを捨てて再計算するか別階層へ退避する必要があり、前者は長いプリフィル計算を繰り返すため遅い。CPU DRAMは遅延が小さい一方で容量が有限で他用途とも競合し、NVMe SSDは容量が大きいがアクセス遅延と帯域が不利である。遠隔直接メモリアクセス（Remote Direct Memory Access; RDMA）型の遠隔保存は拡張性を得られるものの専用の通信・ソフトウェア経路を必要とする。このため、通常のロード・ストアで扱え、DRAM級の応答性と分離メモリの容量拡張を両立し得るCXLをKV退避先としてどこまで実用化できるかが問題になる。
## 新規性
本論文の新規性は、CXLを一種類のDRAM拡張器として測るのではなく、直接接続のDRAM型CMM-D、CXLスイッチで複数デバイスを束ねるCMM-B、バックエンド通信までデバイス側で処理して遠隔DRAMを一つのNUMA領域として見せるCMM-MP、DRAMキャッシュの背後にNANDを置くCMM-Hという4つの設計点を、同じvLLM・LMCache経路と同じモデル・負荷で比較した点にある。特にメモリプール型とDRAM-NANDハイブリッド型をKVキャッシュ退避で同一条件に置き、分離性や容量を増やしてもDRAM型ではシステムDRAMに近い性能を保てること、NAND型では容量と性能の交換条件が明確になることを示す。
## 手法
### 手法のあらまし
処理の中心は、vLLMが推論中に生成したKVキャッシュをLMCacheがGPU HBMと外部メモリの間で管理する共通経路である。GPU側のキャッシュ容量が不足すると、LMCacheは使用頻度の低いKVページを退避先へ移し、後続要求が同じ文脈を再利用するときは保存済みページを取得してGPUへ戻す。これにより、キャッシュを捨てて長い入力を再度プリフィルするよりも、外部メモリからの転送が十分速ければ計算を省ける。評価では退避先をLinuxのメモリ結合（mbind）で選び、システムDRAMと各CXLデバイスを同じメモリ確保経路に載せる。CXLデバイスはいずれもCPUを持たないNUMAノードとしてホストへ公開されるため、LMCacheからは通常のホストメモリと同じように確保でき、CXL専用のLMCache変更は不要である。

CMM-Dはホストへ直接接続したDRAM拡張器、CMM-BはCXLスイッチの下にCMM-Dを配置したプール、CMM-MPはローカル・遠隔のDRAMボードを内部ネットワークで束ねつつホストには一続きのNUMA範囲として見せる。CMM-MPでは遠隔アクセスの信頼性処理や転送をデバイス側が担うため、ホスト側に遠隔直接メモリアクセス（Remote Direct Memory Access; RDMA）の専用経路を追加しない。CMM-Hは大きなNAND領域をDRAMデバイスキャッシュで隠蔽し、局所性が高いアクセスではDRAMを使いながらテラバイト級容量を提供する。さらにLMCacheの単一ソケット向け非同期取得処理を複数OSスレッドへ変更し、ソフトウェア側が退避デバイスの帯域を不必要に制限しないようにして、保存媒体の差を比較しやすくしている。

### 共通のKVキャッシュ退避経路
vLLMが生成したKVページをLMCacheが管理し、GPU HBMが逼迫したときに外部階層へ移し、再利用要求では保存済みページを再取得する。全ての退避先を同じvLLM・LMCache構成で扱い、Linuxのメモリ結合で割当先NUMAノードだけを切り替えるため、デバイスごとに異なるアプリケーション実装を持たない。CXL側もCPUを持たないNUMAノードとして見えるので、LMCacheの通常のCPUメモリ確保経路をそのまま使える。

単一ソケット向け非同期取得だけは複数OSスレッド化して取得処理の並列度を上げ、ソフトウェア側の直列処理がCXL比較のボトルネックになりにくいようにする。この統一経路により、同じ要求・同じモデルで保存先だけを交換でき、測定された差をソフトウェア実装差ではなくメモリ階層の特性へ対応づけやすくなる。

### DRAM型とプール型CXLの透過的拡張
CMM-DはGen5 x8のCXL.memを介して256GB DRAMを追加する直接接続型で、CMM-BはCXLスイッチ配下に同種デバイスを置いて共有・拡張可能な構成にする。CMM-MPはさらに、複数のDRAMボードを200/400GbE級の内部ネットワークで束ね、ホストからはローカルと遠隔を含む一つの連続NUMA範囲として公開する。

ローカルアドレスはボード上のDRAMで処理し、遠隔アドレスはデバイス内部の通信部が転送するため、ホストは標準ロード・ストアのままでよい。この設計により、KVキャッシュをより大きな共有プールへ伸ばしながら、RDMA用のホスト側通信スタックを追加せずに分離メモリを利用できる。評価ではスイッチや遠隔プール化がKVアクセスへ追加する負担が、システムDRAMとの差として直接現れる。

### DRAM-NANDハイブリッドによる容量優先階層
CMM-Hは3.84TB級NVMe SSDのNANDを大容量の背後記憶にし、前段のDRAMをデバイスキャッシュとして使うCXL Type-3構成である。ホストには通常のCXLメモリとして見せつつ、デバイス内部でアクセス局所性を利用して頻繁に使うデータをDRAMへ保持する。これにより1GB当たりのコストと総容量をDRAMのみのCXLより有利にできる。

一方、キャッシュに当たらないKV取得ではNAND帯域・遅延が表面化する。したがって本方式はDRAM型CXLの単純な高速版ではなく、非常に大きいKV保存量を優先し、その代わりに初回トークン時間や取得時間を受け入れる階層として評価される。長文脈で再計算を避ける利益がNAND取得時間を上回るかどうかが、CMM-Hを選ぶ境界条件になる。

### 全体のデータ／制御の流れ
一つの要求を追うと、まずvLLMが入力をプリフィルして各層のKV状態をGPU HBMへ生成する。GPU上の保持量が増えるとLMCacheがKVページを選び、NUMA割当で指定されたシステムDRAMまたはCXL領域へ退避する。後続要求が保存済み文脈を再利用すると、LMCacheは外部階層からKVを取得してGPUへ戻し、再計算を減らす。

CMM-Dでは取得が直結DRAM、CMM-BではCXLスイッチ配下DRAM、CMM-MPでは必要に応じてデバイス内部ネットワーク越しの遠隔DRAM、CMM-HではDRAMデバイスキャッシュまたは背後NANDへ到達する。上位のvLLMとLMCacheから見る操作は共通であり、性能差は主に各階層の容量・帯域・遅延と、長い入力を再計算せずに済む効果の釣り合いとして現れる。
## 評価条件
- **ハードウェア**: デュアルソケットIntel Xeon（各64コア、Model 173）、512GB DDR5-4800、NVIDIA A100 40GB HBM2e（PCIe Gen4 x16）。退避先は256GB CMM-D、CXLスイッチ型CMM-B、6デバイス合計288GBのCMM-MP、3.84TB SSDを持つCMM-H、およびシステムDRAM。
- **ソフトウェア**: Ubuntu 24.04 LTS（カーネル 6.8.0-101）、vLLM 0.19.0+cu128、LMCache 0.4.2。LMCacheの単一ソケット向け非同期取得を複数OSスレッド化。
- **モデル**: Llama-3.1-8B-Instructの密モデル。
- **データセット／トレース**: vLLMの配信ベンチマーク（vllm bench serve）のランダム入力。入力長512〜122Kトークン、同時要求は最大64、条件に応じて14・28・56・64要求を使用。最大集約KVキャッシュは約231GB。
- **比較対象**: キャッシュなし、GPU VRAMのみ、システムDDR5 DRAM
- **正確性・品質**: KV内容を近似変換せず保存先だけを変更する。生成品質のベンチマークは行わず、主にスループット、初回トークン時間、処理時間内訳を評価する。
同一のvLLM・LMCacheソフトウェアスタックで退避先だけを切り替え、入力長と同時要求数を変えて長文脈・大容量KV条件を作る。GPU HBMに収まらない条件では、GPUのみの基準は不足分を必要に応じて再計算する。要求スループット、総トークン毎秒、初回トークン時間、64K入力時のプリフィル・デコード・検索・取得の時間内訳を比較し、CXL構成のメモリプール化やNAND背後化がどの段階へ影響するかを見る。
実機のシステム評価であり、単一の密モデル、単一A100 GPU、特定のIntel XeonホストとSamsung/XConn系CXL構成に限定される。CMM-MPやCMM-Hには概念実証ハードウェアを含むため、他世代GPU・CXL・ネットワークへの一般化は追加検証が必要である。RDMA型退避との直接実測比較は今後の課題として残る。
## 主要結果
KVキャッシュがGPU HBMに収まる短い条件ではGPU計算が支配的だが、入力が長くなり外部KV容量が効く領域ではDRAM型CXLの利点が大きくなる。122Kトークン入力ではCMM-D、CMM-B、CMM-MPがGPU VRAMのみの基準に対して要求スループットを約9倍へ高め、初回トークン時間を最大16分の1に短縮した。これらはシステムDRAMに近い性能を示し、CXLスイッチやCMM-MPの遠隔プール化がKVワークロードで大きな追加低下を生まない。一方、NANDを背後に持つCMM-Hは容量優先の設計で、改善幅は小さくなる。

- 要求スループット / 約9倍 (比較対象: GPU VRAMのみ; 条件: 122Kトークン入力でCMM-D、CMM-B、CMM-MPを使用) — HBM不足時に長いKVを再計算するよりDRAM級CXLから再取得する方が速く、長文脈ほど退避の効果が大きくなる。

- 要求スループット / 約3倍 (比較対象: GPU VRAMのみ; 条件: 8Kトークン入力でCXL退避を使用) — 中程度の入力長でもキャッシュ再利用が効くが、同時実行数16を超えるとスループットは飽和し、別の計算・実行資源が支配的になる。

- 初回トークン時間（TTFT） / 最大16分の1 (比較対象: GPU VRAMのみ; 条件: 122Kトークン入力でCMM-D、CMM-B、CMM-MPを使用) — 長い入力のKVを保持できることで再プリフィルを避け、CXL取得遅延より省ける計算時間が大きくなる。

- 要求スループット / 約2倍 (比較対象: GPU VRAMのみ; 条件: 122Kトークン入力でCMM-Hを使用) — NAND背後の大容量化でも再計算回避の効果は得られるが、DRAM型CXLより低い媒体帯域が改善幅を制限する。

### 負の結果・境界条件
- CMM-HはDRAM型CXLより取得が遅く、122K入力の要求スループット改善は約2倍に留まり、CMM-D・CMM-B・CMM-MPの約9倍を大きく下回る。
- CMM-Hは短い入力側で初回トークン時間が約50%高くなる条件があり、NAND背後の大容量化は低遅延を常に改善するわけではない。
- 8K入力では同時実行数16を超えて要求スループットが飽和し、退避先だけを高速化しても無制限には伸びない。

### 結果の読み方
改善幅は、外部階層からKVを読む時間と、KVを保持できないためにプリフィルを再計算する時間の差で決まる。CMM-D、CMM-B、CMM-MPはDRAMを主体とするため取得時間が小さく、64K入力の暖機済み条件でも取得は総遅延の小さな部分に留まり、システムDRAMに近づく。入力が長いほど再計算回避の価値が増えるためGPU VRAMのみとの差が広がる。CMM-HではNAND帯域が取得とプリフィル待ちに現れ、同じ容量拡張でも性能側の交換条件が強い。
## 品質への影響
KVキャッシュの値を量子化・枝刈り・予測で変更せず、保存場所と取得経路だけを変えるため、方式は原理上無損失である。論文は精度や生成品質の改善を主張せず、品質指標を別途比較していない。
## 既存研究との差
- LMCacheはGPUとホスト側階層のKV管理機構を提供するのに対し、本論文はその上でCXLメモリの物理構成を変えたときの性能差を測る。
- StrataなどのSSD階層化研究がソフトウェア側の階層管理を主題にするのに対し、本論文は同じLMCache経路でDRAM型CXL、スイッチ型プール、ネットワーク透過型プール、DRAM-NANDハイブリッドを並べる。
- 既存のCXL KV研究が主にDRAM型メモリ拡張へ集中していたのに対し、CMM-BとCMM-MPによるプール化、およびCMM-Hによるハイブリッド容量階層まで含めて、性能・容量・分離性の設計空間を広げる。
## 限界
- 評価モデルはLlama-3.1-8B-Instructの1種類で、GPUもA100 40GBの単一構成に限られる。
- CMM-MPとCMM-Hには概念実証ハードウェアを含み、製品世代やCXL世代が変わると帯域・遅延の関係も変わり得る。
- 負荷はvLLMのランダム入力ベンチマークであり、実運用トレースの局所性やマルチテナント干渉を直接評価していない。
- RDMA型の遠隔KV退避とは同一実機条件で直接比較しておらず、論文自身が今後の比較課題に挙げる。
- 評価用のLMCache取得経路には複数OSスレッド化の変更があるが、その変更を含む公開コードURLは確認できない。
## 実装状態
vLLM 0.19.0+cu128とLMCache 0.4.2へ複数種類のCXLデバイスをNUMAメモリとして接続した実機試作である。LMCache本体のCXL専用変更は不要だが、単一ソケット向け非同期取得処理を複数OSスレッド化している。論文本文から再現用公開コードURLは確認できない。
## 研究上の位置づけ
KVキャッシュの新しい管理アルゴリズムを提案する研究というより、CXLを階層メモリ・分離メモリの退避先として採用する際のシステム設計点を実測で比較する研究に位置づく。とくに、直接接続DRAMだけでなくメモリプールとNAND背後型まで同じ推論基盤で比較するため、将来のKVキャッシュ配置器が容量・帯域・コストに応じて階層を選ぶ際の基礎データになる。
## 一次資料
- https://doi.org/10.1109/LCA.2026.3720952
- https://www.researchgate.net/publication/411814165_LLM_KV_Cache_Storage_using_CXL_Memory
