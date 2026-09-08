---
canonical_id: "AAAI:39106"
last_audited: null
audit_version: 0
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference"
summary: "expert weightを複数の小さな行列単位へ分け、複数の前layerが共通して必要と予測したexpert部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。"
authors_affiliations: "Keyu Chen, Qihang Zhou, Bin Qian, Zhenyu Wen, Wenchao Meng, Shibo He／Zhejiang University, Zhejiang University of Technology"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert Prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39106"
code: ""
last_checked: "2026-09-03"
---

# FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference

> expert weightを複数の小さな行列単位へ分け、複数の前layerが共通して必要と予測したexpert部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。

## 概要

FIRM-MoEは、通常のexpert offloadが**expert全体を一つの転送単位として扱うため、必要のないweightまでまとめて運びやすい**点を問題にする。

MoE expert FFNはgate / up / down projectionなど複数weight matrixから構成される。FIRM-MoEはこれらを独立にload可能な小単位へ分け、限られたVRAMへ必要部分だけをcache / prefetchする。

さらに、単一前layerからのpredictionはmissが多く、候補を増やすだけでは無駄transferが増える。そこで**複数の前layerが同じexpertを必要と予測した時に、そのexpertを高信頼とみなして優先する**。

最後に、layerごとのrouting特性とhardware resourceを見て、何layer前から予測するか・何expert分を先読みするかを自動調整する。

native router / Top-k / expert計算は維持するため、expert substitution型ではなくlossless寄りのsystem optimizationである。

## 手法のあらまし

### 1. Expertをprojection単位へ分ける

各expertを、

- `W_gate`
- `W_up`
- `W_down`

などのprojection単位へ分け、それぞれ独立した小さなweight単位として管理する。

expert丸ごとloadする方式よりGPU cache容量を細かく使え、不要なweight transferを減らせる。

### 2. 小さいweight単位でcache / prefetchする

GPU VRAMにはexpert全体ではなく、必要なprojectionを個別に置ける。

cache missでもexpert全体を移す必要がなく、必要なweight部分だけをCPU DRAMから送る。

### 3. 複数前layerの予測が一致したexpertを優先する

対象layerより前の複数layerが、それぞれ次expert候補を予測する。

複数layerで同じexpertが候補に現れた場合、そのexpertは将来実際に必要になる可能性が高いとみなし、prefetch priorityを上げる。

論文ではこの仕組みを`Meeting-of-Layers (MoL)`と呼ぶ。単一predictorの候補を全部先読みするより、**複数予測の合意で候補を絞り、誤予測transferを減らす**のが目的である。

### 4. Prediction数を増やしすぎない

prefetch候補を増やせば本当に必要なexpertを含める割合は上がるが、使わないweight transferも増える。

MoLは単純にcandidateの和集合を広げるのではなく、複数layerで一致した候補を優先してこのtrade-offを抑える。

### 5. Layerごとに予測距離と先読み数を変える

浅層・中層・深層でroutingの予測しやすさと、次layerまでに使える計算時間が異なるため、全layerへ同じ設定を使わない。

論文の`HEOP`はlayer groupごとに、

- 何layer前から予測するか
- 何expert候補を先読みするか
- GPU cacheへどれだけ容量を割くか

を変える仕組みである。

### 6. VRAM・転送時間に合う設定を探索する

GPU memory容量、expertを送る時間、cache missした時の待ち時間をcostとして、予測距離やprefetch数の候補を少しずつ変えながら速い設定を探す。

GPU memoryが小さい環境ではweightを細かく保持する利点を重視し、PCIe帯域に余裕があればprefetchを増やす、といった適応を行う。

## 評価

### まず見るところ
- **結論:** expertをprojection単位へ細分化し、複数前layerの予測が一致したものを優先して先読みすると、小cacheほど無駄transferを減らしやすい。
- **速度:** baseline比平均約1.31×、最大約1.5×。厳しいcache条件ではprefetch baseline比最大約1.8×。
- **メモリ:** 最大約2.8×のmemory savingを報告。
- **品質:** native routerと元expert計算を維持するためlossless寄り。
- **注意点:** weightを細かく分け過ぎると、管理情報や小さいDMA transferの回数が増えて不利になる可能性がある。

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

cacheが小さいほどexpert丸ごとtransferの無駄が相対的に大きくなり、weight分割の利点が増える。

### Memory savings

最大約2.8×のmemory savingを報告する。

これはexpert数をpruneするのではなく、**GPUへ置くweight単位を細かくして必要部分だけ保持する**ことで得る。

### 各要素の役割

性能向上は主に、

1. expert weightを小単位へ分解する
2. 複数前layerの予測合意で誤prefetchを減らす
3. layerごとに予測距離・先読み量を調整する

の組み合わせで出る。

### 制約

- 小weight単位ごとの管理情報が増える。
- small DMA transferが多すぎるhardwareでは効率低下の可能性。
- routing correlationが弱いmodelでは複数layer合意の利得が縮む。
- SSD/NVMe未評価。
- official codeは一次資料で確認できない。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39106)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39106/43068)

## 更新履歴
- 2026-09-04: fine-grained decomposition / MoL / HEOPを分離し、cache制約下の速度・memory評価を表形式へ整理。
- 2026-09-07: sub-expert / MoL / HEOP / objective search等を、weight分割・予測合意・資源調整として平易化。
