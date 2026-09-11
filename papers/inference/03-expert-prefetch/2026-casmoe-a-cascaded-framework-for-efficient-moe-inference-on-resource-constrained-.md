---
canonical_id: AAAI:39816
arxiv_id: null
doi: 10.1609/aaai.v40i31.39816
openreview_id: null
arxiv_categories:
  primary: null
  cross_list: []
last_audited: '2026-09-10'
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: 'CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices'
summary: 過去に似たpromptがあればその時のexpert利用履歴を再利用し、似た履歴がなければ学習済みpredictorで全layerのexpert候補を予測して、CPUからGPUへの先読みを早く始める。
authors_affiliations: Chengcheng Wang, Haowen He, Liang Zhao, Xiaoheng Deng, Lixin Duan, Shaohua Wan／UESTC, Shenyang Aerospace University, Central South University
published: '2026-03-14'
publication_status: Published
lineage: Expert Prefetch
topics:
- CPU offload
- Expert cache
- Expert prefetch
- Edge／on-device
importance: 高
hardware_evaluation: 実機
source: https://ojs.aaai.org/index.php/AAAI/article/view/39816
code: null
implementation: 公式コード公開の記載はAAAI掲載ページで確認できず
last_checked: '2026-09-11'
authors:
- Chengcheng Wang
- Haowen He
- Liang Zhao
- Xiaoheng Deng
- Lixin Duan
- Shaohua Wan
publication: Proceedings of the AAAI Conference on Artificial Intelligence
publication_type: conference paper
sources:
- https://ojs.aaai.org/index.php/AAAI/article/view/39816
implementation_status: official-code-not-confirmed
---

# CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices

> 過去に似た入力文があればその時のエキスパート利用履歴を再利用し、似た履歴がなければ学習済み予測器で全層のエキスパート候補を予測して、CPUからGPUへの先読みを早く始める。

## 概要

CasMoEは、エキスパート 先読みの予測方法を1つに固定せず、**過去ルーティング パターンの検索**と**学習型予測器**を段階的に使い分ける。

類似入力文が過去データベースに存在する場合は、その入力文で使われたエキスパート履歴をそのまま利用する。十分似た履歴が見つからない入力文だけ学習型予測器へ回す。

これにより、毎回予測器を実行する方式より予測計算を減らしつつ、履歴検索だけでは対応しにくい新しい種類の入力文にも対応する。

さらに入力文を一度処理して全MoE 層の候補エキスパートをまとめて予測するため、深い層で使うエキスパートも早い段階から転送を始められる。

元の ルータ / Top-kは変更せず、予測はキャッシュ warming専用なので無損失型である。

二段構成の意味は、検索と学習予測を精度競争させるのではなくコストの違うfallbackとして使うことにある。既知ワークロードでは履歴検索だけで全層候補を得られるため追加モデル実行を避けられ、未知入力文だけ高コストなEAPへ送る。データベース 被覆が高まるほどonline 予測器利用率を下げられる一方、ワークロード shiftが大きい環境では検索hitを過信すると誤先読みが増える。

## 手法のあらまし

### 1. `EAM`：似た過去promptからexpert利用履歴を探す

過去入力文の表現と、それに対応する全層のエキスパート 活性値 パターンをデータベースへ保存する。

新しい入力文が来たら近い表現を検索し、十分似た既知入力文があれば、その時のエキスパート利用パターンを先読み計画として再利用する。

論文ではこの検索部を`Expert Activation Matcher (EAM)`と呼ぶ。追加モデルを実行せず、**過去の似たリクエストを検索するだけで将来エキスパートを予測する**のが役割である。

### 2. `EAP`：似た履歴がないpromptは学習済みpredictorで予測する

EAMで十分なmatchが得られない入力文は、学習型の`Expert Activation Predictor (EAP)`へ送る。

EAPは軽量encoderと層別prediction headからなり、入力文表現から全層のエキスパート候補を一括予測する。

### 3. 「似たroutingをするprompt」を近い表現へ学習する

EAPのencoderは、意味が近いだけでなく**実際に似たエキスパート利用パターンを持つ入力文同士が近いvectorになるように学習する**。

これにより、入力文表現をエキスパート 活性値 predictionへ使いやすくする。論文ではcontrastive learningを使うが、目的はこのルーティング類似性を表現へ反映することにある。

### 4. 検索だけで済ませるかpredictorへ回すかを切り替える

過去入力文との類似度や「どれくらい未知の入力か」を見て、

- 十分似た履歴がある → EAMの検索結果を使う
- 似た履歴がない → EAPで新しく予測する

を切り替える。

論文ではcascade gateと呼ぶが、本質は**安い履歴検索で済むリクエストと、予測器が必要なリクエストを分ける判断**である。

### 5. Prompt時点で全layerのcandidateを出して先読み開始を早める

入力文段階で全層のcandidate エキスパートを出すため、層ごとに予測器を待つ方式より深い層の転送を早く始められる。

CPU DRAMからGPUへcandidate エキスパートを非同期転送し、元の gate到達時に必要エキスパートがすでにGPUへある割合を高める。

全層を入力文時点で予測する利点は、深い層ほど長い先読み窓を確保できることである。ただし早く予測するほど実際のデコード 隠れ 状態をまだ観測していないため、将来ルーティングの不確実性も高い。CasMoEは入力文-level履歴や予測器へ依存する代わりに、転送開始を大幅に前倒ししてPCIe 遅延を多くの前段計算へ隠す設計といえる。

### 6. Lossless型

予測候補が外れても元の ルータが最終selectionを行う。

予測エキスパートを元の エキスパートの代わりに確定実行するCommitMoEとは異なる。

このためCasMoEは、予測を外したときにモデル出力を近似する方式ではなく、候補の準備だけを早める方式として整理できる。最終的なエキスパート選択は元のゲートに任せ、先読みが外れた場合も正しい計算へ戻る。

したがって評価では、候補が当たった割合だけでなく、候補が必要になるまでに転送を終えた割合も確認する必要がある。検索段階の精度と実行段階の待ち時間を分けて見ることで、カスケード構成の効果を正しく解釈できる。

特に入力文の分布が変わる環境では、履歴の再利用率と予測器への切り替え率を同時に追うことが重要になる。

## 評価

### まず見るところ
- **結論:** 類似入力文は履歴検索、未知入力文は予測器へ回すことで、prediction コストを抑えながら深い層の先読みも早く開始できる。
- **速度:** on-demand 比較対象比スループット約65.13%改善を報告。
- **品質:** 元の ルーティングを維持し、平均タスク performanceを96.6%以上保持。
- **I/O:** CPU DRAM→GPU エキスパート 先読み。SSD/NVMeは扱わない。
- **注意点:** データベースにどれだけ過去パターンが蓄積しているか、類似とみなすthreshold、ワークロードの変化へ依存し、公式codeは確認できない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 主要比較

論文では資源-constrained device上で、

- 必要になってからエキスパートを読む方式
- エキスパート キャッシュを使う方式
- 学習型予測器で先読みする方式

と比較する。

### Throughput

on-demand 比較対象に対し、スループットを約65.13%改善。

主な利得は、

- 過去に似た入力文がある時は予測器計算を省ける
- 入力文時点で深い層まで先読み開始できる

ことによる。

### 品質

元モデルのタスク performanceを96.6%以上保持したと報告する。

ただしこれは平均ベンチマーク スコアであり、トークンごと 出力 identityや最悪ケースの品質を直接示す指標ではない。

### EAM / EAPの役割分担

| 入力 type | 主経路 | 利点 |
|---|---|---|
| 過去と類似 | 過去履歴検索 | 予測器 遅延を省ける |
| 未知性が高い | 学習型予測器 | 検索だけより新しい入力文へ対応しやすい |

### Databaseのtrade-off

ルーティング パターン データベースを大きくすると過去と似た入力文を見つけやすくなる一方、

- データベース メモリ
- 検索 コスト
- 古いパターンを更新するコスト

も増える。

ワークロードが大きく変わる場合、古いルーティング履歴の価値は低下する。

そのためデータベースは単なるキャッシュではなく、予測精度と検索コストを同時に決める状態になる。小さすぎればEAP呼出しが増え、大きすぎれば近傍検索と更新の管理コストが増える。また意味的に似ていてもルーティングが異なる入力文を再利用すると不要エキスパートを先読みするため、EAM表現はsemantic similarityだけでなくエキスパート 活性値 similarityを反映する必要がある。

### 制約

- データベース構築が必要。
- どの程度似ていれば履歴を再利用するかのthreshold tuningが必要。
- 予測器 trainingが必要。
- 公式 実行時 codeは一次資料で確認できない。
- PCIe bytes/トークンや予測ミスが多いリクエストの詳細な速度・品質trade-offは限定的。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39816)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39816/43777)

## 更新履歴
- 2026-09-04: EAM / EAP / cascade gate / all-層 predictionを分離して説明し、評価を表形式へ整理。
- 2026-09-07: EAM / EAP / cascade / contrastive learning / データベース 被覆等を、検索と予測の具体的な役割として平易化。
