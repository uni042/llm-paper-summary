---
canonical_id: "arXiv:2510.09665"
arxiv_id: "2510.09665"
last_audited: null
audit_version: 0
storage_targets: ["CPU DRAM","local disk","remote disk","Redis","object storage","NFS","GPU-Direct Storage"]
bottlenecks: ["KV cache I/O granularity","CPU-GPU transfer bandwidth","remote storage bandwidth","cache hit ratio","prefill latency"]
hardware_details: "主評価は8×NVIDIA H100サーバ。PD分離ではprefiller/decoder間をNVLink接続。感度評価ではB200も使用。"
quality_effect: "KV cache再利用のためモデル品質そのものは原理上変えない。context truncationはprefix hit率を約85%→45%へ低下させる実運用上の副作用を報告。"
evidence_locations: ["arXiv v2 HTML §4-§9","Fig.8-16","Table 4-5"]
title: "LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference"
summary: "vLLM/SGLangのKV cacheをGPU外へ抽出し、CPU・disk・remote storage・networkを跨いで再利用/転送する汎用KV cache layer。大粒度chunk転送、compute-I/O overlap、zero-copy、標準connector APIによりprefix reuseとprefill-decode分離を実用化する。"
authors_affiliations: "Yuhan Liu, Jiayi Yao, Yihua Cheng, Yuwei An, Xiaokun Chen, Shaoting Feng, Yuyang Huang, Samuel Shen, Rui Zhang, Kuntai Du, Junchen Jiang（Tensormesh Inc.; University of Chicago）"
published: "2025-10-08"
publication_status: "arXiv preprint v2 (2025-12-05)"
lineage: "KV Cache Offload / Recomputation"
topics: ["KV cache offload","Prefix caching","Prefill-decode disaggregation","Hierarchical storage","vLLM","SGLang","RDMA","KV transfer"]
importance: "高"
hardware_evaluation: "実機"
source: "https://arxiv.org/abs/2510.09665"
code: "https://github.com/LMCache/LMCache"
last_checked: "2026-09-09"
---

# LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference

> vLLM / SGLangが生成するKV cacheをGPU内部だけの一時状態から切り離し、CPU memory、local/remote storage、networkを跨いで永続化・再利用・転送できる独立KV cache layerとして扱う。大粒度chunk転送、compute-I/O overlap、zero-copy、標準connector APIを組み合わせ、prefix reuseとprefill–decode分離を実用規模で成立させる。

## 概要

LMCacheは、LLM推論エンジン内のKV cacheを外部ストレージ階層へ取り出し、別query・別engineから再利用できるようにするオープンソースのKV cache基盤である。対象は主に2つで、同一prefixを持つ後続queryでprefill計算を省く**cross-query context caching**と、prefill GPUからdecode GPUへKVを移送する**prefill–decode disaggregation**である。

従来のvLLMやSGLangにもGPU↔CPUのKV転送機構はあるが、単一node中心で、cross-node transfer、複数storage tier、統一管理APIまでを一体化してはいない。LMCacheは推論engineとstorage/networkの間に「KV cache layer」を置き、KVをGPU内部実装の副産物ではなく、位置・寿命・転送・圧縮を明示的に管理可能なデータとして扱う。

主要な設計点は、(1) paged attentionの小pageをそのまま転送せず大きなchunkへ束ねる、(2) inferenceとKV I/Oをlayer単位・query単位でoverlapする、(3)不要な複製を避けるzero-copy/参照管理、(4) vLLM/SGLangの内部変更から外部KV layerを隔離する標準connector、(5) lookup / move / pin / compress等を提供するcontroller API、である。

## 問題設定

KV cacheは従来、1 queryのdecode中だけGPU memoryへ保持され、query終了後に破棄される。しかし長文context、RAG、agent、multi-turn会話では、過去に計算したprefixのKVを別queryで再利用できればprefillを省ける。またprefillとdecodeを別GPUへ分離する構成では、prefillが生成したKVをdecode側へ高速に渡す必要がある。

LMCacheの実利用統計では、GPU memoryに収まらないKV cache量が増加し、GPU外へ保存したtokenの再利用回数も増えている。論文では、直近利用者の19%以上でGPU外保存tokenが平均1.5回以上再利用されるとしており、「一度退避したKVを再びGPUへ戻す」こと自体が一般的な処理になりつつあると主張する。

一方、vLLM等のpaged memoryではKV pageが16–64KB程度の細粒度に分割される。小さいI/Oを大量発行するとPCIeやnetwork bandwidthを飽和できない。論文が引用する測定では64KB転送は4GB/s、256KBで13GB/s、16MB以上で約49GB/sに達する例があり、KV転送ではgranularityが主要bottleneckになる。

## 手法

### 1. 推論engineとstorage/networkの間にKV cache layerを置く

LMCacheは推論engineからKV cache pageの位置とtoken metadataをconnector経由で受け取り、storage managerとtransfer channelを通してCPU、disk、remote storage等へ保存する。

読み出し時はtoken列からcache hitを調べ、該当KVをback-endから取得してGPUのpaged memoryへ戻す。中央controllerは各instance・storage deviceにどのtokenのKVがあるかを追跡し、cache-aware routingやmigrationにも利用できる。

### 2. pageではなくchunk単位で転送する

vLLMの1 layerあたりpageはモデルにより約20–63KBと小さく、そのまま1 copyずつ転送するとDMA/CUDA launch・metadata処理の固定費が支配的になる。

LMCacheは複数page・複数layerを**既定256 tokenのchunk**へまとめる。store時はscattered GPU pagesから専用CUDA kernelで連続bufferへ集約し、そのbufferをDMAで下位tierへ送る。load時は逆にchunkを連続bufferへ読み、paged memoryへ分解する。

decodeで新規生成されるKVもtokenごとに即保存せず、chunkが貯まるまでbufferしてからまとめて書く。

### 3. computeとI/Oを重ねる

**Layer-wise pipelining**ではcompute streamとdata-movement streamを分離し、layer 1を計算している間にlayer 2のKVを非同期loadする。GPUに追加で必要なbufferは概ね1 layer分に抑える。

**Asynchronous prefetch**では、schedulerで待機中のqueryが実行されるまでのqueue時間を利用して、remote disk→CPU→GPUなど遅いtierから先読みする。実際の推論開始時にはより高速なtierへKVを移しておく。

### 4. 不要なcopyを作らない

同じKVをCPU・disk・remote object storageなど複数宛先へ同時保存する際、宛先ごとの完全copyを生成せず、reference counterで共通dataを共有する。

さらにGPU free pageの全量をCPUへ複製するのではなく、start/current/end pointerで「事前複製しておく範囲」を管理するdynamic offloadingを採用する。複製量を減らすほどmemory節約になるが、急なGPU page割当時にoffload完了待ちstallが起こりやすくなるtrade-offがある。

### 5. 推論engineからconnectorを分離する

vLLM/SGLangはattention kernelやKV layoutが頻繁に変わるため、LMCacheは標準connector APIを定義する。scheduler側ではexternal cache hit token数をprefix cache hitとして扱い、model runner側ではlayer前後にload/store hookを入れる。

代表的APIには、cache hit token数を返す `get_num_new_matched_tokens`、page allocation後のstate更新、connector metadata構築、layer-wise load/store開始・待機がある。

### 6. KVをfirst-class objectとして管理する

中央controllerは全instanceのcache位置を集約し、上位routerやoperatorへlookup / move / clear / pin / unpin / compress / decompressなどのAPIを提供する。

このため単なるoffload libraryではなく、cache-aware routing、scale-down前のKV migration、peer-to-peer共有、特定documentのpinなどを上位policyから制御できる。

## 評価

### 条件

| 項目 | 内容 |
|---|---|
| LMCache | v0.3.6 |
| vLLM | v0.10.2（GPU prefix caching）/ v0.11.0（native CPU offload） |
| 主hardware | 8× NVIDIA H100 server |
| PD構成 | prefiller / decoderを分離、NVLink接続 |
| 主model | Llama-3.1-8B/70B、Sao10K-L3-8B、Qwen2.5-Coder-32B、Qwen3-Coder-480B-A35B-FP8、Qwen2.5-72B |
| workload | multi-round Q&A、LongBench、vLLM random workload、企業trace |
| metrics | TTFT、ITL、throughput、component transfer latency |

CPU offload評価では1 queryあたり既定10K token程度のdocument contextと短いquestion、最大100 output tokenを使い、LMCacheのCPU KV容量を最大500GBにしている。

### Single-node CPU offload

5モデルで、LMCacheは低QPS時にbaselineより**1.9–8.1倍小さいTTFT**を示した。同一TTFTで処理可能なquery rateは最強baseline比**2.3–14倍**。QPS=1でITLも最良baselineより7–92%小さい。

主因はGPU memoryのみのprefix cacheより大容量CPU DRAMでhit率を上げられることと、vLLM native CPU offloadのpage-by-page転送よりLMCacheのchunk転送が高bandwidthを引き出すことにある。

### 実trace

企業F/Gのtoken長分布を再現したtraceで、LMCacheはbasic vLLMに対して高QPS条件で**TTFTを3.7–6.8倍短縮**し、**ITLを19–58%削減**した。

### Centralized remote storage

GPU nodeと15Gbpsで接続した中央remote storageからKVを再利用する構成では、basic vLLM比で**1.3–3倍のthroughput改善**を報告する。

ただしremote bandwidthが低い場合、短context・小modelではKV loadがprefillより遅くなる。遠隔storageは容量によるhit率向上とload delayのtrade-offがある。

### Transfer component

CPUからGPUへのload bandwidthは、LMCacheが**400Gbps**、vLLM native CPU offloadが**88Gbps**。論文はこの差をchunk-vs-page transfer granularityに帰属している。

query-level asynchronous loadingによりcomputeとloadを重ねると、end-to-end delayが**1.46倍改善**した。

### Context length / network bandwidth感度

B200評価では、networkが32Gbpsの場合、remote KV loadがprefillより速くなるのは入力長が**256K token超**の領域だった。一方64/128Gbpsでは評価した全context lengthでloadがprefillを上回る。

したがって「cache hitなら常にload」ではなく、context length、model速度、network bandwidthから**load-vs-recomputeのcrossover pointを動的判定する必要がある**。

### SGLang

Qwen3-32B、H100×2、TP=2では、LMCache CPU offloadはSGLang native CPU offloadと概ね同等性能だった。LMCacheの優位は単一node CPU offloadの絶対性能より、distributed/hierarchical storage backendと統一管理層にある。

## 実運用から得た知見

### Remote storageでもprefillより速い場合がある

高速object storageを使う企業Cでは、remote KV loadによりfull prefill比でTTFTを22–32%削減した例を報告する。remote storageを「遅い容量tier」とだけ捉えるのは適切でなく、context長とnetwork帯域次第ではlatencyも改善できる。

### Context truncationはprefix cacheを壊す

企業Fの実traceでは、最新tokenだけを残すtruncationによりprefix cache hit率が**約85%から45%**へ低下した。長文context管理policyとKV reuse policyを独立に設計すると、大きな性能損失が起こり得る。

### Productionでは柔軟性と互換性が重要

LMCacheは研究prototypeからproduction frameworkへ移行する過程で、特殊attention統合よりもstorage backend拡張、engine互換性、container deploymentを優先した。現在はNFS、WEKA、GPU-Direct Storage、Mooncake Store、NIXL、S3、InfiniStore、Valkey等へ対応し、NVIDIA/AMD/Ascend/TPUとvLLM/SGLangを跨ぐとしている。

## 既存研究との差

### vLLM / SGLang native offload

native CPU offloadはengine内部に統合された単一node向け機構で、LMCacheはengine外に独立したstorage/communication layerを設け、cross-node・multi-tier・controller APIまで対象にする。

### Mooncake / InfiniStore / 3FS

これらはdistributed object/store層として強いが、LMCacheはpaged inference engineの小tensorを効率よく出し入れする「glue layer」と標準connectorを主眼にする。storage backendそのものより、engine↔storageのdata pathと管理semanticが研究対象である。

### CacheGen / IMPRESS / selective compression系

これらがKV表現削減・重要度選択・圧縮policyへ重点を置くのに対し、LMCacheは原則としてKV内容を変えず、transfer granularity、pipeline、zero-copy、placement/control APIでI/O効率と運用性を改善する。controllerにはcompress APIもあるが、特定圧縮方式自体は主貢献ではない。

## 限界

- 主要end-to-end比較はLMCache著者自身の実装・環境で行われ、commercial baselineはblack-box比較で内部条件を揃えきれない。
- LMCacheの優位はcache reuseが存在するworkloadで大きく、reuseが少ない場合はstorage/I/O追加コストだけが残り得る。
- remote backendは帯域が低いとprefillより遅く、32GbpsのB200評価では256K token超でようやくloadが有利になる。
- SGLang native CPU offloadとの単一node比較では性能差は小さく、すべてのengine/backendでLMCacheが高速というわけではない。
- dynamic offloadingにはCPU側重複量とGPU page allocation stallのtrade-offがある。
- 実利用統計はopt-in利用者や匿名企業traceに依存し、一般workload全体を代表するとは限らない。
- controllerが集中metadata viewを持つため、大規模clusterでのcontroller scalability / consistencyは本論文の主要評価対象ではない。

## 研究上の含意

LMCacheの重要点は、KV cacheを「GPU memory節約のために一時退避する対象」から、**推論cluster全体を跨ぐstorage/communication primitive**へ引き上げたことにある。

特に、KVの価値は「保存できるか」よりも、「再計算よりloadが速い条件を判定できるか」「どのtierからloadするか」「どのengineへroutingするか」に移っている。今後はcache hit率、context length、model prefill速度、network/storage bandwidth、GPU queue状況を同時に見て、load / recompute / migrateを動的に選ぶ制御が重要になる。

SSD活用の観点では、LMCacheはlocal/remote diskやGPU-Direct Storageをbackendとして取り込めるが、論文の主評価はCPU DRAMやremote storage中心である。SSD tier固有のqueue depth、random I/O、read amplification、write endurance、prefetch policyをLLM serving schedulerと共同最適化する余地は残っている。

## 一次資料

- arXiv: https://arxiv.org/abs/2510.09665
- HTML: https://arxiv.org/html/2510.09665
- Code: https://github.com/LMCache/LMCache

## 更新履歴

- 2026-09-09: workflow v9のqueue型サーベイで新規精読。arXiv v2全文に基づき手法・評価・実運用知見・限界を整理。
