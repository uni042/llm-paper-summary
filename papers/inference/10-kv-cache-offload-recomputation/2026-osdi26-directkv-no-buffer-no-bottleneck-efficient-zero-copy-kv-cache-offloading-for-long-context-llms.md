---
canonical_id: "USENIX:OSDI26:luo"
arxiv_id: null
doi: null
openreview_id: null
arxiv_categories:
  primary: null
  cross_list: []
last_audited: null
audit_version: 0
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs"
summary: "GH200でCPU DRAM上のKV cacheをGPU HBMへ一度コピーせず、GPUのattention kernelから直接読み、同じCPU側dataを何度も読まないよう計算順序とkernelを作り直すzero-copy KV offload system。"
authors_affiliations: "Shutian Luo, Haiying Shen（University of Virginia）"
published: "2026-07-13"
publication_status: "OSDI 2026"
lineage: "KV Cache Offload / Recomputation"
topics: ["KV cache offload","Zero-copy","CPU pinned memory","NVLink-C2C","Kernel-memory co-design","Long-context inference"]
importance: "高"
hardware_evaluation: "実機"
source: "https://www.usenix.org/conference/osdi26/presentation/luo"
code: "https://github.com/shutianluo/DirectKV"
implementation: "公式実装あり（shutianluo/DirectKV）"
last_checked: "2026-09-06"
---

# No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs

> GH200でCPU DRAM上のKVキャッシュをGPU HBMへ一度コピーせず、GPUの注意機構 カーネルから直接読み、同じCPU側データを何度も読まないよう計算順序とカーネルを作り直すゼロコピー KV オフロード システム。

## 概要

DirectKVは、長文脈でGPU HBMに収まらなくなるKVキャッシュをCPU メモリへ置きながら、**注意機構実行前にKVをGPU バッファへコピーしない**ゼロコピー オフロード システムである。

ここでいう **ゼロコピー** は、「CPU上のKVを使うたびにGPU HBMへ明示的にコピーしてから計算する」のではなく、**GPU カーネル自身がCPU DRAM上のKVを直接読む**方式を指す。

従来のswap型オフロードはCPU上のKV ブロックをGPUへ一度コピーしてから注意機構を実行するため、GPU側にコピー先となる一時バッファが必要になり、CPU→GPUの読み込みとGPU→CPUへの書き戻しも発生する。DirectKVはGPUから直接参照できるCPU メモリを使い、注意機構 カーネル自身が必要なKVだけをCPU側から読む。

ただし通常のGPU カーネルをそのままゼロコピー化すると、同じCPU-常駐 データを何度も読み直して接続網 trafficが増え、NVLink-C2Cでも大幅に遅くなる。そこでDirectKVは**CPU側データを一度読んだらできるだけ長く再利用する計算順序**、loadと計算の並行化、K/V生成と注意機構の統合を組み合わせ、CPU メモリ accessを重要な ボトルネックにしないようカーネルを作り直している。

## 問題設定

CPU メモリへKVをオフロードする既存システムの多くは、注意機構 カーネルがKVをHBM上に置く前提のため、CPU-常駐 KVを一度GPU 中継バッファへ移す必要がある。

この **中継バッファ** は、CPU上のデータをGPU計算へ渡す前に一時的に置いておくGPU側のコピー先を指す。

この方式には2つのコストがある。

- 中継バッファ自体がHBMを消費し、オフロードで得たいメモリ容量を一部失う
- デコードごとにKVをCPU→GPUへ読み、生成したKVを書き戻すため接続網 trafficが増える

GH200 / GB200ではCPU-GPU間がNVLink-C2Cで最大900 GB/s級になり、PCIeより大幅に高速であるため、CPU メモリをGPUから直接読むゼロコピーが現実的になる。一方HBMは約4 TB/sとさらに速く、単純な ゼロコピーでは依然として帯域差が露出する。

論文のmicrobenchmarkでは単純な ゼロコピーはPCIeで20倍超、NVLink-C2Cでも約2倍遅くなり、GPU L2 ヒット 速度も約77%から32.3%へ低下した。

## 手法

### 1. KVをGPUから直接参照できるCPU memoryへ置く

KVキャッシュ管理機構は`cudaHostAlloc`を使い、OSにswapされずGPUから直接アドレス指定できるページ固定ホスト バッファを確保する。一般に **固定メモリ** と呼ばれる領域である。

GPU カーネルはこのKVを直接参照するため、明示的な`cudaMemcpyAsync`とHBM 中継バッファが不要になる。

プリフィルで生成したKVもCPU バッファへ書き、デコードでは過去KVをそこから直接再利用する。KV自体を捨てる再計算方式ではない。

### 2. CPU側dataを一度読んだら何度も再利用する計算順序に変える

GPU行列演算は大きな行列を小さいブロックへ分割して処理する。論文の **tiling** はこの分割方法を指す。

単純な カーネルではCPU メモリ上の同じKV ブロックを複数の計算ブロックから繰り返し読むため、遠隔転送量が増幅する。

DirectKVはCPU側のデータをGPU内の高速な共有d メモリへ一度読み込んだら、GPU HBM上の別データを順に変えながらできるだけ長く再利用する。これにより**遅いCPU-GPU 接続網のtrafficを減らし、その代わり増えるaccessを高速なHBM側へ寄せる**。

論文の行列 multiplication例ではCPU→GPU trafficを33.5 GBから0.4 GBまで減らし、単純な ゼロコピーの106 msを54 msへ短縮した。

### 3. Data load担当とcompute担当を並行して走らせる

Hopper GPUでは複数スレッドのまとまりを役割分担させ、現在のブロックを計算している間に次のブロックをCPU/HBMから先読みする。

論文の **warp-level pipelining** は、この「計算担当が処理中に、別担当が次データを先に準備する」方式を指す。

microbenchmarkではHBM スループットを0.3 TB/sから1.3 TB/sへ高め、54 msから48 msへさらに短縮している。

### 4. K/Vを作る処理とattentionを同じkernelへまとめる

別カーネルでK/Vを生成してCPUへ書き、その後注意機構 カーネルが再びCPUから読むと、生成直後の同じKVがCPU-GPU間を余計に往復する。

DirectKVはK/V 射影と注意機構を1つのGPU カーネルへまとめ、新しく生成したK/VをGPU内の高速バッファに残したまま即座に注意機構へ使う。必要なKVだけ最後にCPU メモリへ書き込み-後段する。

つまり論文の **カーネル 融合** は、別々なら中間データをメモリへ書いて再読込する処理を一つのカーネルへまとめ、その往復を消すことを意味する。

### 5. Prefillとdecodeで「どちらのdataを再利用するか」を変える

プリフィルでは多数のQ トークンがあるため、CPU-常駐 KVを繰り返しfetchしないようQ側を順に処理して同じKVを再利用する。

デコードではQが1 トークンだけなので、CPU上のK/V ブロックを一度ずつストリームしながら注意機構を進める。

同じゼロコピー方針でも段階ごとに再利用すべきデータを変えることで、remote-メモリ trafficを抑える。

## 評価

### 条件

| 項目 | 条件 |
|---|---|
| 主環境 | NVIDIA GH200 Grace-Hopper Superchip |
| GPU メモリ | 96GB HBM3 |
| CPU メモリ | LPDDR5X |
| Interconnect | NVLink-C2C |
| PCIe比較 | H100 PCIe Gen5 |
| Model | Llama-3.1-8B、OPT-13B、OPT-30B |
| Dataset | ShareGPT、Alpaca |
| Context | 主に1K〜32K |
| Baseline | SGLang、Pie、NEO、FlexGen |
| 実装 | CUDA 12.4、CUTLASS 3+、FlashAttention-3拡張 |

### 主要結果

DirectKVはGH200上で既存オフロード方式に対し、**CPU-GPU 転送量を最大50%削減、GPU メモリ使用量を43%削減、エンドツーエンド 性能を最大1.2倍改善**した。

文脈 長さを1K〜32Kへ伸ばした評価ではオフロード方式の中で一貫して低遅延で、16KではNEO / Pie比約1.3倍、FlexGen比約1.7倍高速だった。32KではNEO、Pie、SGLangがOOMになる条件でもDirectKVは動作した。

高リクエスト 速度でも、OPT-13B / 30BでGPU-のみ SGLangがOOMする領域まで処理を継続し、30 req/sで他のオフロード方式より低いトークンごと 遅延を維持している。

構成要素評価ではCPU-aware tilingが単純な ゼロコピー比でCPU-GPU trafficを最大50%、遅延を最大70%削減した。K/V生成と注意機構をまとめたカーネルは別カーネル方式よりHBM スループットを最大3.5倍にし、カーネル 遅延を約2.5〜3倍短縮した。

## 既存研究との差

### Swap型offloadとの違い

PieなどはCPU上のKVをGPU 中継バッファへプリフェッチしてから注意機構を計算する。DirectKVは**KVをHBMへ一度コピーせず、GPU カーネルがCPU メモリから直接読む**ため、バッファ容量と往復コピーを削減する。

### NEO / FastDecodeとの違い

NEOやFastDeコードはKVがあるCPU側へ注意機構計算も移すことでPCIe 転送を減らす。DirectKVはCPUを保存領域として使いながら**注意機構計算はGPUに残す**。その代わり高帯域NVLink-C2Cと専用カーネルを必要とする。

### KVPR / CAPTUREとの違い

KVPRやCAPTUREは「KVを運ぶ代わりに一部をGPUで作り直す」方式でI/Oを減らす。DirectKVはKVを保持したままCPU メモリから直接読むため再計算を行わず、接続網とカーネル dataflowの改善でI/O コストを下げる。

## 限界

- 性能上の主対象はGH200/GB200のような高帯域CPU-GPU superchipであり、通常PCIe環境ではゼロコピーを容量 extensionとしては使えても性能利得が限定される。
- Hopper世代の高速非同期データ 転送機能、スレッド-group制御、共有d メモリを前提としたカーネル設計で、他GPU 構成への移植には再設計が必要。
- 評価モデルはLlama-3.1-8BとOPT-13B/30Bで、MoEやより大規模なGQA モデルは未評価。
- CPU メモリをKV 保存領域として使うため、ホストDRAM容量・帯域が新しい資源 制約になる。
- full-GPU KVが収まる場合はSGLangのようなHBM-常駐方式の方が最速である。

## 一般的な実装上の含意

DirectKVは、ホスト-デバイス 接続網が高速化すると「オフロード = 明示的なコピー」という前提自体を変えられることを示す。ただしゼロコピー APIを使うだけでは不十分で、**メモリ 階層ごとの帯域差に合わせてカーネル内のデータ再利用順序まで設計し直す必要がある**。

CXLやNVLink-C2Cのような異種の メモリ環境では、配置 方策だけでなくカーネル アクセスパターンまで含めたメモリ-計算 協調設計が重要になる。

## 引用関係

- **引用探索から発見:** NEO / FlexGen / KV オフロード系を直接比較対象とするOSDI 2026研究。
- **主要な先行研究:** Pie、NEO、FlexGen、CPU上の注意機構 オフロード、remote/分離型 KVキャッシュ研究。
- **系統上の位置:** KVキャッシュをCPU/保存領域へ置く研究群のうち、再計算ではなくゼロコピー 遠隔アクセスを選ぶ枝に位置する。

## 一次資料

- OSDI 2026: https://www.usenix.org/conference/osdi26/presentation/luo
- 論文PDF: https://www.usenix.org/system/files/osdi26-luo.pdf
- 公式コード: https://github.com/shutianluo/DirectKV

## 更新履歴

- 2026-09-06: 引用関係探索から追加。OSDI 2026最終版と公式codeに基づき概要・手法・評価・限界を整理。
- 2026-09-07: zero-copy、pinned memory、staging buffer、tiling、warp-level pipeline、カーネル fusionを処理内容ベースで平易化。
