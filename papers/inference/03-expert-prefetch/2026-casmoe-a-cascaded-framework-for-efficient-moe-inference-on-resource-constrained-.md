---
title: "CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices"
summary: "routing履歴検索と学習型predictorをcascadeし、promptから全層expert候補を早期生成してresource-constrained MoEのprefetchを効率化する。"
authors_affiliations: "Chengcheng Wang, Haowen He, Liang Zhao, Xiaoheng Deng, Lixin Duan, Shaohua Wan／UESTC, Shenyang Aerospace University, Central South University"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39816"
code: ""
last_checked: "2026-09-03"
---

# CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices

> routing履歴検索と学習型predictorをcascadeし、promptから全層expert候補を早期生成してresource-constrained MoEのprefetchを効率化する。

## 概要

CasMoEは、expert prefetchの予測方法を1つに固定せず、**過去routing patternの検索**と**学習型predictor**を段階接続する。

類似promptが過去databaseに存在する場合は検索結果をそのまま使い、未知性が高いpromptだけ学習型predictorへ回す。

これにより、毎回predictorを実行する方式より予測overheadを下げつつ、履歴検索だけでは弱いdomain shiftにも対応する。

さらにpromptを一度処理して全MoE layerの候補expertをまとめて予測するため、深いlayerのprefetchを早く開始できる。

native router / Top-kは変更せず、予測はcache warming専用なのでlossless型である。

## 手法のあらまし

### 1. `EAM`：Expert Activation Matcher

過去promptの表現と、それに対応する全layerのexpert activation patternをdatabaseへ保存する。

新しいpromptが来たら近い表現を検索し、十分近い既知patternがあれば、そのrouting patternをprefetch計画として再利用する。

non-parametricなので追加predictor推論を省ける。

### 2. `EAP`：Expert Activation Predictor

EAMで十分なmatchが得られないpromptは、学習型EAPへ送る。

EAPは軽量encoderとlayer別prediction headからなり、prompt表現から全layerのexpert候補を一括予測する。

### 3. Contrastive learning

EAPの表現空間では、routing patternが似るpromptを近づけ、異なるpromptを離す。

単純multi-label classificationより、prompt semanticとexpert activation patternの対応を学びやすくする狙いがある。

### 4. Cascade gate

retrieval confidenceやinput noveltyを見て、

- EAMだけで確定
- EAPへfallback

を切り替える。

類似promptでは検索の低cost性、未知promptではpredictorのgeneralizationを使う。

### 5. 全層candidateを早期prefetch

prompt段階で全layerのcandidateを出すため、layerごとにpredictorを待つ方式より深いlayerのtransferを早く始められる。

CPU DRAMからGPUへcandidate expertを非同期transferし、native gate到達時のcache hitを高める。

### 6. Lossless型

予測候補が外れてもnative routerが最終selectionを行う。

予測expertをnative expertの代わりに確定実行するCommitMoEとは異なる。

## 評価

### まず見るところ
- **結論:** 類似promptは履歴検索、未知promptはpredictorへ回すcascadeで、prediction costとprefetch開始時刻を両立する。
- **速度:** on-demand baseline比throughput約65.13%改善を報告。
- **品質:** native routingを維持し、平均task performanceを96.6%以上保持。
- **I/O:** CPU DRAM→GPU expert prefetch。SSD/NVMeは扱わない。
- **注意点:** database coverage、類似度threshold、workload driftへ依存し、公式codeは確認できない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 主要比較

論文ではresource-constrained device上で、

- on-demand loading
- cache型
- 学習型prefetch型

と比較する。

### Throughput

on-demand baselineに対し、throughputを約65.13%改善。

主な利得は、

- EAM hit時にpredictor計算を省ける
- prompt時点で深いlayerまでprefetch開始できる

ことによる。

### 品質

元モデルのtask performanceを96.6%以上保持したと報告する。

ただしこれは平均benchmark scoreであり、per-token output identityやtail-qualityを直接示す指標ではない。

### EAM / EAPの役割分担

| Input type | 主経路 | 利点 |
|---|---|---|
| 過去と類似 | EAM | predictor latencyを省ける |
| 未知性が高い | EAP | retrieval-onlyよりgeneralizeしやすい |

### Databaseのtrade-off

routing pattern databaseを大きくするとcoverageは増える一方、

- retrieval memory
- search cost
- update cost

も増える。

workload driftが強い場合、古いEAM patternの価値は低下する。

### 制約

- database構築が必要。
- similarity threshold tuningが必要。
- predictor trainingが必要。
- official runtime codeは一次資料で確認できない。
- PCIe bytes/tokenやtail missの詳細Paretoは限定的。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39816)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39816/43777)

## 更新履歴
- 2026-09-04: EAM / EAP / cascade gate / all-layer predictionを分離して説明し、評価を表形式へ整理。
