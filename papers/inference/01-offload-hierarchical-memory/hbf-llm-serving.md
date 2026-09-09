---
canonical_id: "arXiv:2608.13127"
arxiv_id: "2608.13127"
last_audited: null
audit_version: 0
storage_targets: ["HBM", "High-Bandwidth Flash (HBF)", "read-mostly model weights", "MoE expert weights"]
bottlenecks: ["HBM capacity", "model residency", "cross-node expert traffic", "model loading/eviction", "memory access granularity", "flash latency hiding"]
hardware_details: "評価は実HBFではなくシミュレーション。MoE評価はH100-class 4ノード（2 prefill + 2 decode、各8 GPU）、80 GB HBM + 最大512 GB相当HBF/GPUをモデル化。multi-model評価はH100相当4 GPU PD分離、PCIe Gen5 x16 H2D 64 GB/sをモデル化。"
quality_effect: "モデル品質自体は変更しない。HBFをread-mostly model stateの容量拡張として使い、HBM-resident execution pathを維持する前提。"
evidence_locations: ["arXiv v2 PDF §3–§5", "Table 2", "Fig. 8–10"]
title: "Potential Applications of HBF in LLM Serving Systems"
summary: "High-Bandwidth FlashをHBMの代替ではなく容量拡張として統合し、MoE expert replica増加とmulti-model weight residency拡大により通信・model loading・load imbalanceを減らす設計を検討する。実HBF評価ではなく、HBM側実行帯域を損なわない理想化条件のシミュレーションで容量効果を分離評価する。"
authors_affiliations: "Yihan Yin, Yilun Zhao, Zhixin Yun, Guanying Wu, Feng Zhu, Kai Tao, Shu Li, Fei Huang, Zhe Zhang, Shuangchen Li, Hongzhong Zheng（Peking University / Alibaba DAMO Academy / Alibaba Cloud Computing / Hupan Lab）"
published: "2026-08-13"
publication_status: "arXiv preprint v2 (2026-08-14)"
lineage: "Offload / Hierarchical Memory"
topics: ["High-Bandwidth Flash", "HBM", "MoE serving", "expert replication", "multi-model serving", "model residency", "memory hierarchy"]
importance: "高"
hardware_evaluation: "シミュレーション"
source: "https://arxiv.org/abs/2608.13127"
code: ""
last_checked: "2026-09-09"
---

# Potential Applications of HBF in LLM Serving Systems

> High-Bandwidth Flash（HBF）をHBMの直接代替にせず、HBMに収まりきらないread-mostlyなmodel stateを保持する容量tierとして追加することで、MoE expertの複製、multi-model weight residency、load balancingを改善できるかを検討する。主結果は実HBFハードウェアではなく、HBM側の実効帯域を維持できるという前提を置いたサービング・シミュレーションである。

## 概要

本論文は、LLM servingでHBMの帯域だけでなく**容量**が主要制約になりつつあることに着目し、SanDiskが提案するHigh-Bandwidth Flash（HBF）をGPU memory hierarchyへ追加する場合のアーキテクチャとシステム上の使い道を整理する。

HBFは3D NANDを積層し、SLC動作と内部並列性を高めることで高いread bandwidthと大容量を狙う。一方、DRAMベースのHBMよりread latencyが長くaccess granularityも粗く、writeも遅くendurance制約がある。そのため論文はHBFをmutableなKV cacheやruntime bufferへ使うのではなく、**read-mostlyなmodel weight / expert weightのresident setを広げる容量拡張**として扱う。

論文の中心的な考え方は、「容量が増えるとmodel state objectをより多くのdevice/nodeへ常駐させられ、そのobjectを利用可能なhardware setが広がる」というcapacity-residency modelである。MoEではexpert replicaを増やしてremote expert accessとhotspotを減らし、multi-model servingではmodel loading/evictionを減らし、さらにhot model replicaを増やしてload balanceを改善する。

## 背景と問題設定

LLM servingでは、model size、context length、同時に提供するmodel variant数が増え、HBM capacity pressureが強まっている。特にMoEは「1 tokenあたりactive parameterは小さいがtotal parameterは巨大」という性質を持ち、expert set全体を収めるために大規模expert parallelismが必要になる。これによりtokenがremote expertへrouteされるたびにdispatch/combine通信が発生する。

multi-model servingでは、多数のdense/MoE model variantを限られたHBMへ同時常駐できず、cold modelのload/evictやmodel swappingが必要になる。人気が時間変動すると、単純なstatic partitioningではあるGPUがoverloadする一方で別GPUがidleになる。

HBFは高密度NANDをHBM類似の積層構造へ載せることで容量を増やせる可能性があるが、HBMと同じmemory semanticsで細粒度アクセスさせるとlatency/granularityの違いで帯域を使い切れない。このため、単に「HBMをHBFへ置き換える」設計ではなく、HBMとHBFの役割分担が必要になる。

## HBF統合アーキテクチャ

論文はcompute dieから見た実効利用可能帯域を

`Bw_avail = Bw_phy × U_intra × U_inter`

と整理する。`Bw_phy`は物理peak bandwidth、`U_intra`はchannel内部利用率、`U_inter`はchannel間利用率である。HBF導入時にはpeak bandwidthだけでなく、粗いpage access、長いlatency、heterogeneous channelの扱いが両利用率を下げないことが必要になる。

### All-HBF

全HBM stackをHBFへ置換する。容量は大きくできるが、GPU既存の細粒度memory access semanticsとHBFの好む粗粒度accessが合わず、`U_intra`を高く保つのが難しい。論文は現行compute dieを大きく変えずに主memoryとして使う案には否定的である。

### Side-by-side HBM/HBF

HBMとHBFを別stackとしてcompute dieへ直接接続する。HBMをlatency-sensitive access、HBFをcoarse-grained data movementへ使い分けやすい一方、異なるmediaを同一tierとして同時飽和させにくく、`U_inter`が問題になる。

### Daisy-chained HBF extension

HBM外側へHBFを連結する。直接HBM pathを保持できるがI/Oを共有するため、HBF trafficがcritical HBM trafficへ干渉しないarbitrationが必要で、package/interposer areaも増える。

### Integrated HBM/HBF stack

同一stack内部へHBMとHBFを組み込み、stack-level interfaceは均質に見せる方式。HBMがfine-grained / latency-sensitive accessを担当し、HBFはcoarse-grained read-mostly dataを担当する。論文は、stack内部でI/O sharingとschedulingを適切に行えるなら、**HBM-likeなcompute-side bandwidth abstractionを保ちつつ容量を拡張できる最有力案**と位置付ける。

## Capacity-residency model

hardware unit集合を`U`、model-state object集合を`O`とし、各device/node `u`がcapacity `C_u`内でresident object set `R_u`を持つ。object `o`が常駐するhardware set `A_o`が大きいほど、schedulerの選択肢が増える。

容量増加には二つの効果がある。

1. **locality改善**: taskが必要とするobjectがlocal communication domain内に存在する確率が上がり、cross-node accessが減る。
2. **load balancing改善**: 同じobject replicaを複数deviceへ配置し、より空いているdeviceへ仕事を振れる。

MoEではexpertがobject、multi-model servingではmodel weight全体がobjectとなる。

## MoE servingへの適用

HBF容量をexpert replicaへ使う。large-scale expert parallelismではexpertがnode間に分散されるため、remote dispatch/combineが必要になる。extra capacityでexpert replicaをlocal domain内へ増やすと、remote expert accessが減る。またhot expertを複数配置できるため、schedulerがless-loaded replicaを選べる。

### 評価条件

- Model: Qwen3-235B-A22B
- 94 layers / 128 routed experts / top-8 experts per token
- 4 H100-class nodes
- 2 prefill nodes + 2 decode nodes
- 各node 8 GPU
- 1 GPUあたり80 GB HBM + 最大512 GB相当HBF容量をモデル化
- scale-up 900 GB/s、scale-out 400 GB/s
- attention/projectionはdata parallel、MoE FFNはexpert parallel
- expert placementはEPLB型hierarchical replication + expert-load-aware scheduling
- workloadはPoisson arrival、prompt/output平均1024/64 tokens
- 16 hot expertsが90% demandを占めるHotset-Zipf

この評価は**実HBFアクセスを測っていない**。HBF accessがHBM-resident execution pathの実効帯域を下げないと仮定し、追加容量によるsystem-level benefitだけを分離している。

### 主結果

resident expert数をdeviceあたり8→32へ増やすと、平均TPOTは10.20 ms→9.13 msで**10.5%低下**、p95 TPOTは10.74 ms→9.73 msで**9.4%低下**した。

cross-node expert trafficは8-expert baselineに対し、12/16/20/24/32 expertsで45.1% / 33.3% / 22.8% / 17.4% / 16.1%へ低下した。aggregate traffic減少ほどlatencyが下がらない場合があるのは、scale-out barrierがslowest transfer pathに支配されるためである。

request rate 8→32 req/sでは32-expert構成のTPOT改善率が11.1%→15.4%へ増え、40 req/sでは14.8%へやや低下した。decode batchが小さすぎても大きすぎても効果が薄まり、中程度のimbalanceが露出するregimeで容量効果が大きい。

expert accessがmoderately hotな場合の改善が大きく、hot ratio 0.6/0.7で14.8%/15.4%、0.9/0.95では11.1%/7.9%へ低下した。accessが極端に偏るとbaseline配置でも必要expertが予測しやすく、extra replicaで除去できるimbalanceが少なくなる。

## Multi-model servingへの適用

multi-model servingでは、HBF容量を複数model weightのresident set拡大へ使う。全modelが常駐できない場合はHost-to-Device loadとevictionが発生し、TTFTを支配する。全modelが収まった後は、余剰容量をhot model replicationへ利用する。

### 評価条件

- 4 GPUのprefill/decode分離構成（2 prefill + 2 decode）
- 2 placement groups
- H100相当、80 GB HBM/GPU
- PCIe Gen5 x16 H2Dを64 GB/s片方向としてモデル化
- HBF-backed weight residencyをplacement groupあたり最大512 GB、80 GB baselineの6.4倍までsweep
- KV-cache space、compute throughput、H2D bandwidth、KV transfer bandwidthは固定
- schedulerはPrism + KVPR-based dynamic model placement
- 本番trace: 600秒、1500 requests、27 models、1B–40B parameters、Zipf α≈1.49、平均2.5 req/s、合計約620 GB FP16 weights
- rate sensitivity用synthetic trace: 18 models、合計約507 GB

### 主結果

capacityを1×→4×へ増やすと、27 modelすべてが実効placement capacityへ収まり、mean TTFTは196.1 ms→6.8 msで**28.7倍改善**、model activation eventは212→0となった。4×以降はmodel loading除去だけでは追加改善しない「all-fit boundary」に到達する。

all-fit後の余剰容量でhot modelをprefill GPU間に複製すると、prefill load-balance ratioは1×時7.87から4×で約1.03、5–6.4×では1.0へ近づく。4×でreplicationなし6.83 msだったmean TTFTは、replicationありで6.05 msとなり**約11%改善**した。

arrival rate sensitivityでは、1×→4×容量拡大のTTFT speedupが0.5 req/sで4.1倍、1.0で9.1倍、2.0で16.3倍、5.0で19.4倍へ増えた。高rateほどmodel set volatilityによるload待ちが多数requestを巻き込むため、全model residencyの価値が大きい。

## 重要な前提と限界

最大の注意点は、評価がHBF実機のread latency、bandwidth、write endurance、controller overheadを含むhardware measurementではないことである。HBFを**HBM execution pathを邪魔しない追加容量**として抽象化しているため、結果は「そのようなHBF統合が実現した場合に得られる容量効果」の上限寄りの評価と解釈すべきである。

論文自身も、off-package slow path、page-granular readを成立させられない場合、HBF trafficがHBM critical pathへ干渉する場合はbenefitが小さくなると明記する。

また本研究ではmutable KV cacheやruntime bufferをHBFへ置かず、HBMへ残している。したがって、flash write enduranceやfrequent KV updateを含むtiering問題を直接評価していない。

MoE評価も実クラスタ測定ではなくrooflineとevent-driven simulationであり、network contention、controller implementation、real kernel behaviorがモデル誤差になる。multi-model traceはproduction由来だが、execution itselfはsimulatedである。

## 既存研究との差

従来のCPU/SSD offload研究は、HBMに入らないweightやKVを低bandwidth tierから必要時にfetchする設計が多い。これに対し本論文のHBFは、**必要時offload/reloadの遅いtierではなく、GPU近傍で高read bandwidthを持つ大容量resident tier**として扱われる。

MoE側ではexpert offloadingではなく、むしろextra capacityを使ってexpertを**より多く複製してlocalityを高める**点が逆方向の発想である。multi-model側でもcold model swapを高速化するのではなく、まずswap自体を不要にすることを狙う。

この意味で本論文は「どのweightを捨てて必要時に戻すか」より、「大容量flashがGPU近傍にあればどのmodel stateを常駐させるのが最も価値が高いか」を主題とする。

## 研究上の含意

SSD/flash活用研究として重要なのは、HBFの価値が単なるbandwidthの代用品ではなく、**residency constraintを緩和することでschedulerの選択肢を増やすこと**にある点である。

MoEでは「flashからexpertを毎token fetchする」より、「頻繁に使うexpert replicaをHBFへ常駐させ、local routing候補を増やす」方が合理的になり得る。multi-model servingでも「model loadを速くする」より、「active model setを常駐させ、余剰容量でhot model replicationする」という設計になる。

一方、実HBFでこの効果を得るには、page-level prefetch、HBM/HBF間のplacement、stack内I/O arbitration、latency hiding、wear managementをserving schedulerと共同設計する必要がある。特にHBF側実効read bandwidthが想定より低い場合、単純なcapacity benefit simulationと実system性能の間に大きな差が出る可能性がある。

## 一次資料

- arXiv: https://arxiv.org/abs/2608.13127
- PDF: https://arxiv.org/pdf/2608.13127

## 更新履歴

- 2026-09-09: workflow v9で全文精読。v2 PDFに基づきarchitecture、simulation assumptions、MoE/multi-model評価、限界を整理。
