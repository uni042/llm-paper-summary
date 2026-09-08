---
canonical_id: "AAAI:39816"
last_audited: null
audit_version: 0
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices"
summary: "過去に似たpromptがあればその時のexpert利用履歴を再利用し、似た履歴がなければ学習済みpredictorで全layerのexpert候補を予測して、CPUからGPUへの先読みを早く始める。"
authors_affiliations: "Chengcheng Wang, Haowen He, Liang Zhao, Xiaoheng Deng, Lixin Duan, Shaohua Wan／UESTC, Shenyang Aerospace University, Central South University"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert Prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39816"
code: ""
last_checked: "2026-09-03"
---

# CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices

> 過去に似たpromptがあればその時のexpert利用履歴を再利用し、似た履歴がなければ学習済みpredictorで全layerのexpert候補を予測して、CPUからGPUへの先読みを早く始める。

## 概要

CasMoEは、expert prefetchの予測方法を1つに固定せず、**過去routing patternの検索**と**学習型predictor**を段階的に使い分ける。

類似promptが過去databaseに存在する場合は、そのpromptで使われたexpert履歴をそのまま利用する。十分似た履歴が見つからないpromptだけ学習型predictorへ回す。

これにより、毎回predictorを実行する方式より予測計算を減らしつつ、履歴検索だけでは対応しにくい新しい種類のpromptにも対応する。

さらにpromptを一度処理して全MoE layerの候補expertをまとめて予測するため、深いlayerで使うexpertも早い段階から転送を始められる。

native router / Top-kは変更せず、予測はcache warming専用なのでlossless型である。

## 手法のあらまし

### 1. `EAM`：似た過去promptからexpert利用履歴を探す

過去promptの表現と、それに対応する全layerのexpert activation patternをdatabaseへ保存する。

新しいpromptが来たら近い表現を検索し、十分似た既知promptがあれば、その時のexpert利用patternをprefetch計画として再利用する。

論文ではこの検索部を`Expert Activation Matcher (EAM)`と呼ぶ。追加modelを実行せず、**過去の似たrequestを検索するだけで将来expertを予測する**のが役割である。

### 2. `EAP`：似た履歴がないpromptは学習済みpredictorで予測する

EAMで十分なmatchが得られないpromptは、学習型の`Expert Activation Predictor (EAP)`へ送る。

EAPは軽量encoderとlayer別prediction headからなり、prompt表現から全layerのexpert候補を一括予測する。

### 3. 「似たroutingをするprompt」を近い表現へ学習する

EAPのencoderは、意味が近いだけでなく**実際に似たexpert利用patternを持つprompt同士が近いvectorになるように学習する**。

これにより、prompt表現をexpert activation predictionへ使いやすくする。論文ではcontrastive learningを使うが、目的はこのrouting類似性を表現へ反映することにある。

### 4. 検索だけで済ませるかpredictorへ回すかを切り替える

過去promptとの類似度や「どれくらい未知の入力か」を見て、

- 十分似た履歴がある → EAMの検索結果を使う
- 似た履歴がない → EAPで新しく予測する

を切り替える。

論文ではcascade gateと呼ぶが、本質は**安い履歴検索で済むrequestと、predictorが必要なrequestを分ける判断**である。

### 5. Prompt時点で全layerのcandidateを出して先読み開始を早める

prompt段階で全layerのcandidate expertを出すため、layerごとにpredictorを待つ方式より深いlayerのtransferを早く始められる。

CPU DRAMからGPUへcandidate expertを非同期transferし、native gate到達時に必要expertがすでにGPUへある割合を高める。

### 6. Lossless型

予測候補が外れてもnative routerが最終selectionを行う。

予測expertをnative expertの代わりに確定実行するCommitMoEとは異なる。

## 評価

### まず見るところ
- **結論:** 類似promptは履歴検索、未知promptはpredictorへ回すことで、prediction costを抑えながら深いlayerのprefetchも早く開始できる。
- **速度:** on-demand baseline比throughput約65.13%改善を報告。
- **品質:** native routingを維持し、平均task performanceを96.6%以上保持。
- **I/O:** CPU DRAM→GPU expert prefetch。SSD/NVMeは扱わない。
- **注意点:** databaseにどれだけ過去patternが蓄積しているか、類似とみなすthreshold、workloadの変化へ依存し、公式codeは確認できない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 主要比較

論文ではresource-constrained device上で、

- 必要になってからexpertを読む方式
- expert cacheを使う方式
- 学習型predictorで先読みする方式

と比較する。

### Throughput

on-demand baselineに対し、throughputを約65.13%改善。

主な利得は、

- 過去に似たpromptがある時はpredictor計算を省ける
- prompt時点で深いlayerまでprefetch開始できる

ことによる。

### 品質

元modelのtask performanceを96.6%以上保持したと報告する。

ただしこれは平均benchmark scoreであり、per-token output identityや最悪ケースの品質を直接示す指標ではない。

### EAM / EAPの役割分担

| Input type | 主経路 | 利点 |
|---|---|---|
| 過去と類似 | 過去履歴検索 | predictor latencyを省ける |
| 未知性が高い | 学習型predictor | 検索だけより新しいpromptへ対応しやすい |

### Databaseのtrade-off

routing pattern databaseを大きくすると過去と似たpromptを見つけやすくなる一方、

- database memory
- search cost
- 古いpatternを更新するcost

も増える。

workloadが大きく変わる場合、古いrouting履歴の価値は低下する。

### 制約

- database構築が必要。
- どの程度似ていれば履歴を再利用するかのthreshold tuningが必要。
- predictor trainingが必要。
- official runtime codeは一次資料で確認できない。
- PCIe bytes/tokenや予測missが多いrequestの詳細な速度・品質trade-offは限定的。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39816)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39816/43777)

## 更新履歴
- 2026-09-04: EAM / EAP / cascade gate / all-layer predictionを分離して説明し、評価を表形式へ整理。
- 2026-09-07: EAM / EAP / cascade / contrastive learning / database coverage等を、検索と予測の具体的な役割として平易化。
