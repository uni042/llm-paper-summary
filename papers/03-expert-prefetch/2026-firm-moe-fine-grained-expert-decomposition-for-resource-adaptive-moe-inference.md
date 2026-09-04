---
title: "FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference"
summary: "expertをsub-expertへ分解し、複数前層の合意予測と資源適応prefetchでCPU→GPU weight trafficを細粒度に制御するMoE推論方式。"
authors_affiliations: "Keyu Chen, Qihang Zhou, Bin Qian, Zhenyu Wen, Wenchao Meng, Shibo He／Zhejiang University, Zhejiang University of Technology"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39106"
code: ""
last_checked: "2026-09-03"
---

# FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference

> expertをsub-expertへ分解し、複数前層の合意予測と資源適応prefetchでCPU→GPU weight trafficを細粒度に制御するMoE推論方式。

## 概要

FIRM-MoEは、通常のexpert offloadが**expert全体を一つの転送単位として扱うため粒度が粗すぎる**点を問題にする。

MoE expert FFNはgate / up / down projectionなど複数weight matrixから構成される。FIRM-MoEはこれらを独立にload可能なsub-expertへ分解し、限られたVRAMへ必要部分だけをcache / prefetchする。

さらに、単一前層からのpredictionはmissが多く、候補を増やすだけでは無駄transferが増える。そこで複数前層の予測が一致したexpertを高信頼とする`Meeting-of-Layers (MoL)`を使う。

最後に`HEOP`がlayer群ごとのrouting特性とhardware resourceを見て、予測範囲・prefetch数を自動調整する。

native router / Top-k / expert計算は維持するため、expert substitution型ではなくlossless寄りのsystem optimizationである。

## 手法のあらまし

### 1. `Fine-Grained Expert Decomposition`

各expertを、

- `W_gate`
- `W_up`
- `W_down`

などのprojection単位へ分け、それぞれ独立したsub-expertとして管理する。

expert丸ごとloadする方式よりcache allocationを細かくでき、不要なweight trafficを減らす。

### 2. Sub-expert単位のcache / prefetch

GPU VRAMにはexpert全体ではなく、必要なprojectionを個別にresident化できる。

cache missでもexpert全体を移す必要がなく、必要sub-expertだけをCPU DRAMから送る。

### 3. `Meeting-of-Layers (MoL)`

対象layerより前の複数layer `P` が、それぞれ次expert候補を`K`個ずつ予測する。

複数layerで同じexpertが候補に現れた場合、そのcandidateを高confidenceとみなしてprefetch priorityを上げる。

単一predictor top-kよりfalse positiveを減らす狙いである。

### 4. Prediction数を増やしすぎない

prefetch候補を増やせばrecallは上がるが、unused weight transferも増える。

MoLは単純にcandidate unionを広げるのではなく、複数layerのagreementで絞り込む。

### 5. `HEOP`：Hierarchical Expert Offloading and Prefetching

浅層・中層・深層でrouting predictabilityとcompute slackが異なるため、全層へ同じ`P`,`K`を使わない。

HEOPはlayer groupごとに、

- 何層前から見るか `P`
- 何expert候補を出すか `K`
- cache / prefetch量

を調整する。

### 6. Resource-adaptive search

VRAM容量、transfer cost、cache miss costを含むobjectiveを作り、hill-climbingで設定を探索する。

GPU memoryが小さい環境では細粒度cacheを強く使い、bandwidthに余裕があればprefetchを増やす、といった適応を行う。

## 評価

### まず見るところ
- **結論:** expertをprojection単位へ細分化し、複数前層のagreementで先読みすると、小cacheほど無駄transferを減らしやすい。
- **速度:** baseline比平均約1.31×、最大約1.5×。厳しいcache条件ではprefetch baseline比最大約1.8×。
- **メモリ:** 最大約2.8×のmemory savingを報告。
- **品質:** native routerと元expert計算を維持するためlossless寄り。
- **注意点:** sub-expert管理のmetadata / small-transfer overheadがhardware次第で不利になり得る。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 実機環境

| 項目 | 設定 |
|---|---|
| GPU | RTX 3090 24GB |
| CPU | 32-core |
| Host memory | 64GB |
| PCIe | Gen4 |

### Models

- Qwen1.5-MoE-A2.7B
- Qwen3-30B-A3B
- DeepSeek-MoE-16B
- DeepSeek-V2-Lite
- OLMoE-1B-7B

TruthfulQAとShareGPT系workloadを使用。

### End-to-end speed

Fiddler / llama.cppなどに対し、

- 平均：約1.31×
- 最大：約1.5×

のspeedup。

### 厳しいcache条件

Qwen系でexpert cache容量を128に制限した条件では、基本prefetch方式比で最大約1.8×。

cacheが小さいほどexpert丸ごとtransferの無駄が相対的に大きくなり、fine-grained decompositionの利点が増える。

### Memory savings

最大約2.8×のmemory savingを報告する。

これはexpert数をpruneするのではなく、**residentにするweight単位を細かくして必要部分だけ保持する**ことで得る。

### Ablation的な意味

性能向上は主に、

1. fine-grained decomposition
2. MoLによるfalse-positive prefetch削減
3. HEOPによるlayer別resource tuning

の組み合わせで出る。

### 制約

- sub-expert metadata管理が増える。
- small DMA transferが多すぎるhardwareでは効率低下の可能性。
- routing correlationが弱いmodelではMoL利得が縮む。
- SSD/NVMe未評価。
- official codeは一次資料で確認できない。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39106)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39106/43068)

## 更新履歴
- 2026-09-04: fine-grained decomposition / MoL / HEOPを分離し、cache制約下の速度・memory評価を表形式へ整理。
