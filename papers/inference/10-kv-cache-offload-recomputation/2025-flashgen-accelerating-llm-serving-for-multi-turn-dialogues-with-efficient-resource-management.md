---
canonical_id: DOI:10.1145/3676641.3716245
doi: 10.1145/3676641.3716245
last_audited: '2026-09-28'
audit_version: 2
title: Accelerating LLM Serving for Multi-turn Dialogues with Efficient Resource Management
summary: 多輪対話では各ターンのpromptに過去会話が再び含まれるため、通常のLLM配信基盤は同じ履歴トークンの鍵・値キャッシュ（Key-Value cache; KVキャッシュ）を毎回再計算しやすい。同時に、履歴の累積でprompt長がばらつき、先着順（First-Come-First-Served; FCFS）では巨大promptが先頭にいるだけで、残りGPUメモリへ収まる短い要求まで待たせるhead-of-line blockingが起こる。FlashGenはGPUメモリ・host DRAM・NVMe SSDの多段KVキャッシュFlashGen-Cacheと、メモリへ収まる要求を先に差し込みつつ飢餓を防ぐFlashGen-Schedを組み合わせる。2×A100 80GB、224GB host cache、RAID-0 NVMe SSD、ShareGPTでOPT/Llama-2を評価し、同程度のlatency boundaryでOPT-30BはvLLM比1.63倍、Llama-2 70Bは2.85倍のthroughputを報告する。
list_summary: 多輪会話の履歴KV再計算と長promptによるFCFS head-of-line blockingを、GPU/DRAM/SSDの多段KV保持と飢餓なし要求reorderingで同時に解くFlashGen。2×A100のShareGPT評価でOPT-30B 1.63倍、Llama-2 70B 2.85倍のthroughputを報告する。
authors:
- Jinwoo Jeong
- Jeongseob Ahn
published: '2025-03'
publication: ASPLOS 2025, pp. 1-15
publication_type: peer-reviewed-conference
publication_status: Published
lineage: inference-systems
topics:
- 多輪対話
- KVキャッシュ
- 階層メモリ
- SSD
- LLM配信スケジューリング
source: https://doi.org/10.1145/3676641.3716245
sources:
- https://doi.org/10.1145/3676641.3716245
- https://jeongseob.github.io/assets/talks/jeong_asplos2025_talk.pdf
last_checked: '2026-09-28'
code: null
implementation: vLLMを基盤に、GPU/host DRAM/SSDの多段KV cache managerと要求reordering schedulerを追加。storageからの復元が待ち時間に隠せない場合は再計算へ切り替える。
implementation_status: paper-and-author-materials-confirmed; official-code-url-not-recorded-here
hardware_evaluation: real-hardware-serving
hardware_details: Azure Standard_NC48ads_A100_v4、NVIDIA A100 80GB×2、DRAM 440GB中224GBをKV cacheへ使用、NVMe SSD 960GB×2をRAID-0。
quality_effect: KV値やモデル計算を近似しないため出力品質は変えない。主な交換条件はKV復元I/O、GPUメモリ占有、要求公平性、tail latency。
evidence_locations:
- motivation
- FlashGen-Cache
- FlashGen-Sched
- evaluation
- author ASPLOS 2025 slides
references:
- canonical_id: arXiv:2403.02310
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.298
  doi: 10.18653/v1/2023.emnlp-main.298
- canonical_id: arXiv:2207.00032
  doi: 10.1109/sc41404.2022.00051
- canonical_id: DOI:10.1145/3620665.3640366
  doi: 10.1145/3620665.3640366
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: arXiv:2107.03374
  arxiv_id: '2107.03374'
- canonical_id: arXiv:2205.14135
- canonical_id: arXiv:2403.19708
- canonical_id: arXiv:2406.17565
  arxiv_id: '2406.17565'
- canonical_id: arXiv:2309.14509
  arxiv_id: '2309.14509'
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: arXiv:2401.02669
  arxiv_id: '2401.02669'
- canonical_id: arXiv:2401.08671
- canonical_id: DOI:10.1037/0033--2909.85.3.618
  doi: 10.1037/0033--2909.85.3.618
- canonical_id: arXiv:1911.02150
  arxiv_id: '1911.02150'
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2302.13971
  arxiv_id: '2302.13971'
- canonical_id: DOI:10.18653/v1/2024.acl-long.623
  doi: 10.18653/v1/2024.acl-long.623
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: arXiv:2205.01068
  arxiv_id: '2205.01068'
- canonical_id: arXiv:2312.07104
  arxiv_id: '2312.07104'
references_checked_at: '2026-10-03'
references_source: crossref-deposited-reference-metadata
references_total: 39
---

# Accelerating LLM Serving for Multi-turn Dialogues with Efficient Resource Management

> 多輪会話の履歴KV再計算と長promptによるFCFS head-of-line blockingを、GPU/DRAM/SSDの多段KV保持と飢餓なし要求reorderingで同時に解くFlashGen。2×A100のShareGPT評価でOPT-30B 1.63倍、Llama-2 70B 2.85倍のthroughputを報告する。

## 概要

多輪対話では、第2ターン以降のpromptに「過去のuser発話＋assistant応答＋今回の質問」が繰り返し含まれる。通常の大規模言語モデル（Large Language Model; LLM）配信基盤が前回ターンの内部状態を保持していなければ、すでに一度処理した履歴トークンについて鍵・値キャッシュ（Key-Value cache; KVキャッシュ）を再計算してから今回の新規promptへ進む。

履歴が長くなるほど、この再計算は初回トークン遅延（Time To First Token; TTFT）を押し上げる。しかし全sessionのKVをGPUへ永久保存することはできない。GPUメモリから追い出したKVをhost DRAMへ置いても、高並列時にはhost側も埋まる。SSDまで使えば容量は増えるが、GPUへ戻すI/Oが再計算より遅い場合がある。

もう一つの問題はスケジューリングである。多輪対話ではsessionごとに履歴長が大きく異なる。先着順（First-Come-First-Served; FCFS）でqueue先頭に巨大promptがあり、その要求全体を載せるだけのGPU KV容量が空いていないと、後ろに「今の空き領域だけで処理できる短い要求」があっても待つ。これがhead-of-line blockingで、GPUメモリの空きとbatching機会を同時に浪費する。

FlashGenはこの二つを分けて扱う。FlashGen-CacheはGPUメモリ、host DRAM、SSDへ過去ターンKVを階層保持し、復元が有利なときだけ再利用する。FlashGen-Schedはqueue順を安全に入れ替え、現在のGPU空きへ収まる要求を先に処理しながら、古い大要求が永遠に後回しにならない飢餓防止機構を入れる。

2枚のA100 80GB、224GBのhost KV cache、2台のNVMe SSDをRAID-0にしたAzure環境で、ShareGPTを使いOPT-13B/30BとLlama-2 13B/70Bを評価する。OPT-30BではvLLM比1.63倍、Llama-2 70Bでは2.85倍のthroughputを同程度のlatency boundaryで報告し、p95 TTFTも代表条件で90%以上短縮する。

## 問題設定

### 多輪対話は「同じ履歴を何度もprefillする」負荷になる

1ターン目で計算した過去トークンのK/Vは、次ターンでも同じ値である。それでも配信基盤がsession終了時にKVを破棄すると、第2ターンの長いpromptを先頭から再度prefillしなければならない。

著者のOPT-13B＋A100 80GBの動機実験では、履歴長が伸びるにつれて再計算latencyが急増し、GPUまたはhostにKVを残した場合との差が拡大する。したがって多輪対話では「新規promptを速く計算する」だけでなく、「前回までに計算済みのKVをどこまで安価に保持・復元できるか」が重要になる。

### host DRAMだけでも高並列では足りない

GPU cache miss時にhost DRAMからKVを戻す方式は、GPUより容量が大きいが有限である。ShareGPT＋OPT-30Bの例ではclient数を増やすとGPU＋hostのKV hit rateが低下する。長時間生きる多数sessionの全履歴をDRAMだけへ置くことは難しい。

SSDを第3tierにすれば容量は大幅に増える。ただしSSD→DRAM→GPU転送は遅いため、何でもSSDから復元すると低負荷時には「GPUでKVを再計算する方が速い」という逆転が起こる。FlashGenはSSDを容量tierとして利用しつつ、復元を待ち時間へ隠せるかで再利用/再計算を選ぶ。

### 長promptがFCFS queueを塞ぐ

GPUにはある程度free memoryが残っていても、queue先頭要求が必要とするKV容量より小さければFCFS schedulerはその要求をdispatchできない。その後ろに小要求があっても待たせれば、空きメモリが遊ぶ。

多輪化でprompt長分散が広がるほどこの問題が増える。著者資料ではShareGPTでFCFSによる未使用GPU memoryが生じることを示し、request reorderingを独立した第2の最適化対象にしている。

## FlashGenの処理全体

1. あるsessionのturnが完了したら、その履歴KVをGPUだけでなく下位tierへ保持できる状態にする。
2. 次のturnが到着した際、GPUに履歴KVがあればそのまま再利用する。
3. host DRAMにあればGPUへ復元するために必要な領域を確保し、既存GPU KVを必要に応じてevictする。
4. SSDにしかない場合は、要求が実行される前にSSD→hostへstagingしてI/Oをqueue待ちへ重ねる。
5. stagingを隠す待ち要求がないなど、SSD復元がcritical pathになる場合はKVを読み戻さずGPUで履歴を再計算する。
6. schedulerは現在のfree GPU memoryへ収まる要求をqueue後方から探し、FCFSを一時的に越えてdispatchする。
7. 後回し要求が長く待つとpromotion対象とし、必要なら先に差し込んだ要求をpreemptして領域を作り、飢餓を防ぐ。
8. CacheとSchedを同時に使い、KV再計算削減とGPU memory利用率向上を組み合わせる。

## 手法

### 1. FlashGen-Cache: GPU–DRAM–SSDの多段KV cache

cache hitの位置で処理経路が変わる。

| KVの所在 | 処理 |
|---|---|
| GPU | 履歴KVをそのまま使って即時実行 |
| host DRAM | GPU側に領域を作りKVを転送してから実行 |
| SSD | まずhost DRAMへstagingし、その後GPUへ復元 |
| どこにも有効なcacheがない/復元が不利 | 履歴tokenを再prefillしてKVを再計算 |

SSDは単なるswap領域ではない。要求がqueueで待っている間にhostへ先読みすることで、低帯域I/Oをcritical pathから外すことを狙う。

またKVのGPU復元には既存KVのevictionが伴うため、cache managerはsession単位の所在とGPU free spaceを追跡する。多段化の目的は「常に最下位tierから読む」ことではなく、再計算より安いtier hitを増やすことにある。

### 2. SSD復元が隠せないときは再計算する

SSD bandwidthはGPU計算に比べて遅く、低負荷でqueueが空いているとprefetch時間を他要求処理へ重ねられない。FlashGenはこの場合、SSD stagingを待つより履歴promptを再計算する経路へ切り替える。

これは重要な負の条件である。階層cache方式の性能は「cache hit率」だけでは決まらず、hitしたtierからの復元latencyが再計算latencyより短いか、またはI/Oを他処理で隠せるかで決まる。

### 3. FlashGen-Sched: free GPU memoryを埋めるrequest reordering

FCFSで先頭要求が入らない場合、FlashGen-Schedは後ろの要求から現在のfree memoryへ収まるものを探してdispatchする。短いhistoryのsessionや必要KVがGPUへ既にあるsessionを先に走らせれば、空いていたGPU memoryをbatchに使える。

著者の評価では、平均GPU memory utilizationがvLLMの90.65%から96.58%へ増えた。モデル別ではFlashGen-Schedによって平均batch request数が1.06〜1.15倍増える。ここがthroughput改善へつながる。

### 4. reorderingによる飢餓をpreemptionで防ぐ

短い要求ばかりを先に選ぶと、巨大promptが永遠に待つ可能性がある。そこで後回し要求をpromotionし、その要求をdispatchするのに必要なmemoryが足りなければ、先にreorderして入れた要求をpreemptする。

つまりFlashGen-Schedはshortest-first schedulerではない。「空きmemoryを一時的に有効利用する」ことと「古い要求の順番を最終的には守る」ことを両立する設計である。

## 評価

### 評価条件

| 項目 | 条件 |
|---|---|
| 環境 | Azure Standard_NC48ads_A100_v4 |
| GPU | NVIDIA A100 80GB ×2 |
| host DRAM | 440GB中224GBをKV cachingへ使用 |
| storage | NVMe SSD 960GB ×2、RAID-0 |
| dataset | ShareGPT |
| models | OPT-13B、OPT-30B、Llama-2 13B、Llama-2 70B |
| baselines | vLLM、CachedAttention |
| ablation | FlashGen-Schedのみ、FlashGen-Cacheのみ、両方 |
| 主指標 | end-to-end latency、throughput、p95 TTFT、GPU memory utilization、平均batch size |

### 代表的な評価結果

| 条件 | vLLM/比較対象 | FlashGen | 改善 |
|---|---:|---:|---:|
| OPT-30B、ShareGPT | vLLM | — | 同程度latency boundaryでthroughput 1.63倍 |
| Llama-2 70B、ShareGPT | vLLM | — | throughput 2.85倍 |
| OPT-30B p95 TTFT代表点 | 16.87 s | 1.29 s | 約92%短縮 |
| Llama-2 13B p95 TTFT代表点 | 6.96 s | 0.51 s | 約93%短縮 |
| 4モデル平均GPU memory utilization | 90.65% | FlashGen-Sched 96.58% | 約5.9ポイント増 |
| 平均batch request数 | vLLM相当 | FlashGen-Sched | モデル別1.06〜1.15倍 |

p95 TTFTのablationでは、OPT-30BでCachedAttention 7.79秒、Schedのみ14.2秒、Cacheのみ3.82秒、両方のFlashGen 1.29秒である。Llama-2 13Bでは順に2.58秒、3.46秒、2.37秒、0.51秒となる。Cacheが履歴prefillを削り、Schedがmemory空きを埋めるため、両者の組合せで最も大きくなる。

throughputのheadlineはモデル依存である。著者発表資料の全体結論ではFlashGenを1.63倍改善として要約している一方、論文abstractではLlama-2 70Bについて2.85倍を報告する。したがって「常に2.85倍」ではなく、モデルサイズ・KV圧力・loadに応じて利得が変わる。

## 既存研究との差

vLLMのページ化注意（PagedAttention）はGPU memory内のKV fragmentationを減らすが、session間隔が長い多輪対話についてGPU–DRAM–SSD全体へhistory KVを永続化することが主眼ではない。

CachedAttentionはmulti-turnのKV reuseを扱うが、FlashGenはGPU/host/storageの三tierと、「storage復元が遅ければrecompute」という選択を加える。またcacheだけでなく、long promptによるFCFS head-of-line blockingをscheduler側でも解く。

FlashGenの特徴は、KV cache容量問題とrequest scheduling問題を別々の機構に分け、同時に使う点である。cacheだけではGPU memoryの空きを十分埋められず、schedulerだけではhistory再計算を消せない。

## 限界・実装状況

評価はA100 80GB×2と特定のhost DRAM/NVMe構成に依存する。PCIe帯域、SSD帯域、CPU memory容量が変われば「復元か再計算か」の境界も変わる。CXLやGrace HopperのようにCPU–GPU memory接続が異なる環境では再評価が必要である。

モデルはOPTとLlama-2世代であり、グループ化問い合わせ注意（Grouped-Query Attention; GQA）、KV量子化、prefix sharingが標準化した新しいモデルでは1session当たりKV容量が変わる。KVが小さくなればSSD tierの必要性やschedulerのmemory pressureも変わる。

ShareGPTは実会話のturn構造を持つが、実productionでのsession再来間隔、client数、SSD耐久性、failure recoveryを完全には再現しない。特にSSDへKVを継続保存する場合、書込量とdevice寿命は運用上の追加評価点になる。

reorderingは公平性機構を持つが、preemption自体にもstate移動・再schedule費用がある。短要求を優先しすぎるとtail latencyへ跳ね返るため、throughputだけでなくper-session latency distributionを見る必要がある。

## 一般的な実装上の含意

多輪対話では、KV cacheを「1回のrequest中だけ生きる一時状態」ではなく「sessionをまたいで再利用できる中間成果物」として扱う価値がある。再計算コストが高い履歴ほど、下位memory tierへ保存する意味が大きい。

ただし階層memoryでは、capacityだけでなくrestoration latencyと隠蔽可能性をschedulerと同時に見る必要がある。FlashGenがSSD hitでも再計算へ戻る経路を持つのは、storage利用を目的化せずend-to-end latencyで選択しているためである。

## 一次資料

- DOI: https://doi.org/10.1145/3676641.3716245
- 著者ASPLOS 2025発表資料: https://jeongseob.github.io/assets/talks/jeong_asplos2025_talk.pdf

## 修正履歴

- 2026-09-28（修正済み）: 最新品質ガイドに合わせ、多輪対話で同じhistory KVを再計算する問題と、長promptがFCFS queueを塞いでGPU memoryを遊ばせる問題を分離して因果的に説明。FlashGen-CacheのGPU/DRAM/SSD hit経路、SSD stagingを隠せない場合のrecompute fallback、FlashGen-Schedのreorderingとstarvation-free preemptionを具体化した。2×A100実機条件、OPT/Llama-2のthroughput、p95 TTFT、GPU memory utilization、batch sizeの結果を表で追加した。
