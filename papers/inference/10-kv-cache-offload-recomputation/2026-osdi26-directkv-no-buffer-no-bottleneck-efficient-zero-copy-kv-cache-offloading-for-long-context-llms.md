---
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
last_checked: "2026-09-06"
---

# No Buffer, No Bottleneck: Efficient Zero-Copy KV Cache Offloading for Long-Context LLMs

> GH200でCPU DRAM上のKV cacheをGPU HBMへ一度コピーせず、GPUのattention kernelから直接読み、同じCPU側dataを何度も読まないよう計算順序とkernelを作り直すzero-copy KV offload system。

## 概要

DirectKVは、長contextでGPU HBMに収まらなくなるKV cacheをCPU memoryへ置きながら、**attention実行前にKVをGPU bufferへコピーしない**zero-copy offload systemである。

ここでいう **zero-copy** は、「CPU上のKVを使うたびにGPU HBMへ明示的にcopyしてから計算する」のではなく、**GPU kernel自身がCPU DRAM上のKVを直接読む**方式を指す。

従来のswap型offloadはCPU上のKV blockをGPUへ一度copyしてからattentionを実行するため、GPU側にcopy先となる一時bufferが必要になり、CPU→GPUの読み込みとGPU→CPUへの書き戻しも発生する。DirectKVはGPUから直接参照できるCPU memoryを使い、attention kernel自身が必要なKVだけをCPU側から読む。

ただし通常のGPU kernelをそのままzero-copy化すると、同じCPU-resident dataを何度も読み直してinterconnect trafficが増え、NVLink-C2Cでも大幅に遅くなる。そこでDirectKVは**CPU側dataを一度読んだらできるだけ長く再利用する計算順序**、loadとcomputeの並行化、K/V生成とattentionの統合を組み合わせ、CPU memory accessをcritical bottleneckにしないようkernelを作り直している。

## 問題設定

CPU memoryへKVをoffloadする既存systemの多くは、attention kernelがKVをHBM上に置く前提のため、CPU-resident KVを一度GPU staging bufferへ移す必要がある。

この **staging buffer** は、CPU上のdataをGPU計算へ渡す前に一時的に置いておくGPU側のcopy先を指す。

この方式には2つのcostがある。

- staging buffer自体がHBMを消費し、offloadで得たいmemory容量を一部失う
- decodeごとにKVをCPU→GPUへ読み、生成したKVを書き戻すためinterconnect trafficが増える

GH200 / GB200ではCPU-GPU間がNVLink-C2Cで最大900 GB/s級になり、PCIeより大幅に高速であるため、CPU memoryをGPUから直接読むzero-copyが現実的になる。一方HBMは約4 TB/sとさらに速く、naive zero-copyでは依然として帯域差が露出する。

論文のmicrobenchmarkではnaive zero-copyはPCIeで20倍超、NVLink-C2Cでも約2倍遅くなり、GPU L2 hit rateも約77%から32.3%へ低下した。

## 手法

### 1. KVをGPUから直接参照できるCPU memoryへ置く

KV Cache Managerは`cudaHostAlloc`を使い、OSにswapされずGPUから直接address指定できるpage-locked host bufferを確保する。一般に **pinned memory** と呼ばれる領域である。

GPU kernelはこのKVを直接参照するため、明示的な`cudaMemcpyAsync`とHBM staging bufferが不要になる。

prefillで生成したKVもCPU bufferへ書き、decodeでは過去KVをそこから直接再利用する。KV自体を捨てるrecomputation方式ではない。

### 2. CPU側dataを一度読んだら何度も再利用する計算順序に変える

GPU行列演算は大きなmatrixを小さいblockへ分割して処理する。論文の **tiling** はこの分割方法を指す。

naive kernelではCPU memory上の同じKV blockを複数の計算blockから繰り返し読むため、remote trafficが増幅する。

DirectKVはCPU側のdataをGPU内の高速なshared memoryへ一度読み込んだら、GPU HBM上の別dataを順に変えながらできるだけ長く再利用する。これにより**遅いCPU-GPU interconnectのtrafficを減らし、その代わり増えるaccessを高速なHBM側へ寄せる**。

論文のmatrix multiplication例ではCPU→GPU trafficを33.5 GBから0.4 GBまで減らし、naive zero-copyの106 msを54 msへ短縮した。

### 3. Data load担当とcompute担当を並行して走らせる

Hopper GPUでは複数threadのまとまりを役割分担させ、現在のblockを計算している間に次のblockをCPU/HBMから先読みする。

論文の **warp-level pipelining** は、この「計算担当が処理中に、別担当が次dataを先に準備する」方式を指す。

microbenchmarkではHBM throughputを0.3 TB/sから1.3 TB/sへ高め、54 msから48 msへさらに短縮している。

### 4. K/Vを作る処理とattentionを同じkernelへまとめる

別kernelでK/Vを生成してCPUへ書き、その後attention kernelが再びCPUから読むと、生成直後の同じKVがCPU-GPU間を余計に往復する。

DirectKVはK/V projectionとattentionを1つのGPU kernelへまとめ、新しく生成したK/VをGPU内の高速bufferに残したまま即座にattentionへ使う。必要なKVだけ最後にCPU memoryへwrite-backする。

つまり論文の **kernel fusion** は、別々なら中間dataをmemoryへ書いて再読込する処理を一つのkernelへまとめ、その往復を消すことを意味する。

### 5. Prefillとdecodeで「どちらのdataを再利用するか」を変える

prefillでは多数のQ tokenがあるため、CPU-resident KVを繰り返しfetchしないようQ側を順に処理して同じKVを再利用する。

decodeではQが1 tokenだけなので、CPU上のK/V blockを一度ずつstreamしながらattentionを進める。

同じzero-copy方針でもphaseごとにreuseすべきdataを変えることで、remote-memory trafficを抑える。

## 評価

### 条件

| 項目 | 条件 |
|---|---|
| 主環境 | NVIDIA GH200 Grace-Hopper Superchip |
| GPU memory | 96GB HBM3 |
| CPU memory | LPDDR5X |
| Interconnect | NVLink-C2C |
| PCIe比較 | H100 PCIe Gen5 |
| Model | Llama-3.1-8B、OPT-13B、OPT-30B |
| Dataset | ShareGPT、Alpaca |
| Context | 主に1K〜32K |
| Baseline | SGLang、Pie、NEO、FlexGen |
| 実装 | CUDA 12.4、CUTLASS 3+、FlashAttention-3拡張 |

### 主要結果

DirectKVはGH200上で既存offload方式に対し、**CPU-GPU transfer量を最大50%削減、GPU memory使用量を43%削減、end-to-end performanceを最大1.2倍改善**した。

context lengthを1K〜32Kへ伸ばした評価ではoffload方式の中で一貫して低latencyで、16KではNEO / Pie比約1.3倍、FlexGen比約1.7倍高速だった。32KではNEO、Pie、SGLangがOOMになる条件でもDirectKVは動作した。

高request rateでも、OPT-13B / 30BでGPU-only SGLangがOOMする領域まで処理を継続し、30 req/sで他のoffload方式より低いper-token latencyを維持している。

component評価ではCPU-aware tilingがnaive zero-copy比でCPU-GPU trafficを最大50%、latencyを最大70%削減した。K/V生成とattentionをまとめたkernelは別kernel方式よりHBM throughputを最大3.5倍にし、kernel latencyを約2.5〜3倍短縮した。

## 既存研究との差

### Swap型offloadとの違い

PieなどはCPU上のKVをGPU staging bufferへprefetchしてからattentionする。DirectKVは**KVをHBMへ一度copyせず、GPU kernelがCPU memoryから直接読む**ため、buffer容量と往復copyを削減する。

### NEO / FastDecodeとの違い

NEOやFastDecodeはKVがあるCPU側へattention計算も移すことでPCIe transferを減らす。DirectKVはCPUをstorageとして使いながら**attention計算はGPUに残す**。その代わり高帯域NVLink-C2Cと専用kernelを必要とする。

### KVPR / CAPTUREとの違い

KVPRやCAPTUREは「KVを運ぶ代わりに一部をGPUで作り直す」方式でI/Oを減らす。DirectKVはKVを保持したままCPU memoryから直接読むため再計算を行わず、interconnectとkernel dataflowの改善でI/O costを下げる。

## 限界

- 性能上の主対象はGH200/GB200のような高帯域CPU-GPU superchipであり、通常PCIe環境ではzero-copyをcapacity extensionとしては使えても性能利得が限定される。
- Hopper世代の高速非同期data transfer機能、thread-group制御、shared memoryを前提としたkernel設計で、他GPU architectureへの移植には再設計が必要。
- 評価modelはLlama-3.1-8BとOPT-13B/30Bで、MoEやより大規模なGQA modelは未評価。
- CPU memoryをKV storageとして使うため、host DRAM容量・帯域が新しいresource constraintになる。
- full-GPU KVが収まる場合はSGLangのようなHBM-resident方式の方が最速である。

## 一般的な実装上の含意

DirectKVは、host-device interconnectが高速化すると「offload = explicit copy」という前提自体を変えられることを示す。ただしzero-copy APIを使うだけでは不十分で、**memory tierごとの帯域差に合わせてkernel内のdata再利用順序まで設計し直す必要がある**。

CXLやNVLink-C2Cのようなheterogeneous memory環境では、placement policyだけでなくkernel access patternまで含めたmemory-compute co-designが重要になる。

## 引用関係

- **引用探索から発見:** NEO / FlexGen / KV offload系を直接baselineとするOSDI 2026研究。
- **主要な先行研究:** Pie、NEO、FlexGen、CPU attention offload、remote/disaggregated KV cache研究。
- **系統上の位置:** KV cacheをCPU/storageへ置く研究群のうち、recomputationではなくzero-copy remote accessを選ぶ枝に位置する。

## 一次資料

- OSDI 2026: https://www.usenix.org/conference/osdi26/presentation/luo
- 論文PDF: https://www.usenix.org/system/files/osdi26-luo.pdf
- 公式コード: https://github.com/shutianluo/DirectKV

## 更新履歴

- 2026-09-06: 引用関係探索から追加。OSDI 2026最終版と公式codeに基づき概要・手法・評価・限界を整理。
- 2026-09-07: zero-copy、pinned memory、staging buffer、tiling、warp-level pipeline、kernel fusionを処理内容ベースで平易化。
