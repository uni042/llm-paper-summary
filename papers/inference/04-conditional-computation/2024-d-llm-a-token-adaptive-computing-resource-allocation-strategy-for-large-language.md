---
canonical_id: NeurIPS2024:03469b1a66e351b18272be23baf3b809
arxiv_id: null
doi: 10.52202/079017-0055
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
title: 'D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language
  Models'
summary: 各token・各layerで『このlayerを実行するか』を小型moduleが判断し、skipしたtokenのKVも後続attentionから外すことで、計算量とKV使用量をtokenごとに変える。
authors_affiliations: 一次資料記載の著者ら（NeurIPS 2024）
published: '2024-12-15'
publication_status: Published
lineage: Conditional Computation
topics:
- Dynamic depth
- KV cache offload
- Quality-cost
importance: 高
hardware_evaluation: 実機
source: https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html
code: https://github.com/Jyk-122/D-LLM
implementation: 公式実装あり（Jyk-122/D-LLM）
last_checked: '2026-09-11'
authors:
- Jiang, Yikun
- Wang, Huanyu
- Xie, Lei
- Zhao, Hanbin
- Zhang, Chao
- Qian, Hui
- Lui, John C.
publication: Advances in Neural Information Processing Systems
publication_type: conference paper
sources:
- https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html
---

# D-LLM: A トークン 適応型 Computing Resource Allocation Strategy for Large Language Models

> 各トークン・各層で「この層を実行するか」を小型moduleが判断し、skipしたトークンのKVも後続attentionから外すことで、計算量とKV使用量をトークンごとに変える。

## 概要
D-LLMは、**各トークン・各層ごとに「この層を実行するかskipするか」を学習する**動的 depth方式である。

系列全体を同じ深度で処理する層 枝刈りとは異なり、同じ層でもトークン Aは実行、トークン Bはskipという分岐が起こる。難しいトークンへ多くの計算を割き、単純なトークンは浅く処理することを狙う。

各層の前に小型decision moduleを追加し、目標計算量 `Ω` に近づくようskip率を学習する。さらに、skipしたトークンのKVを後続attentionから隠すことで、computeだけでなくKV容量も削る。

Llama 2 7Bではfull-depth LoRAの約55〜59%のFLOPs、Llama 3 8Bでは約52〜55%程度まで減らしながら、多くのtaskで同等以上の品質を示す。ただし論文の中心指標はFLOPsで、**FLOPs半減＝wall-clock 2倍高速化を実証した研究ではない**。

## 手法のあらまし

### 1. 小型moduleがトークンごとにexecute / skipを決める

各Transformer 層の直前に小型moduleを置き、現在のhidden stateから、

- この層を実行する
- この層をskipする

の2択を出す。

この判定がトークン単位なので、同一バッチ・同一層でも実行経路が分かれる。

### 2. 0/1のskip判断を学習できるよう、学習時だけ滑らかな近似を使う

execute / skipは本来0/1の離散判断なので、そのままでは通常のgradientを流しにくい。

D-LLMは学習中だけGumbel-Softmaxという方法で「execute寄り / skip寄り」の連続値を作り、forwardではhardな0/1選択を使いつつ、backwardでは連続値のgradientを利用する。

要するに、**推論時は本当に層を飛ばすが、学習時だけ微分可能な近似を使う**。

### 3. 平均skip率を目標計算量 `Ω` に近づける

単に「skipできるところは全部skip」と学習すると、品質重視ならほぼ全層実行、計算量重視なら過剰skipへ崩れやすい。

そこで平均skip率と指定した目標 `Ω` の差をlossへ加え、全体の計算量を狙ったbudgetへ寄せる。

`Ω`を変えることで、品質重視・計算量重視の別modelを作れる。

### 4. 最初の2 層は必ず実行する

初期層まで動的にskipすると表現形成が不安定になるため、実験では最初の2 層をdecision対象外にする。

全32 層を完全自由にrouteしているわけではない。

先頭層を固定することは学習安定性だけでなく、すべてのトークンが共有する最低限の表現基盤を確保する役割も持つ。各トークンが最初から別経路へ分かれると、後段の決定モジュールが受け取る隠れ状態の分布まで大きくばらつくため、実行／スキップ判断の学習が難しくなる。固定前段を置くことで、動的分岐を後半の冗長性が大きい領域へ限定している。

### 5. SkipしたトークンのKVも後続attentionから外す

D-LLMでは、あるトークンが層 `l` をskipした場合、そのトークンのK/Vを後続queryから参照させない。

これにより層計算だけでなくKV storageも減らせる。

ただし長距離文脈を失いやすくなるため、文頭の最初 `m` トークンは必ずKVを残す。本実験では `m=2` が最良だった。

このKV除外が必要なのは、あるトークンが層を飛ばした場合、その層にはそのトークンのK/Vが存在しないからである。後続トークンだけが同じ層を実行して欠損した位置を通常のAttention対象に含めると、系列内で参照可能な状態が不整合になる。D-LLMは欠損位置を明示的にAttention対象から外し、『計算しなかった状態を存在するものとして扱わない』ことで動的深度とKVキャッシュを整合させる。

### 6. 追加学習が必要

元checkpointへ推論時だけ差し込むtraining-free手法ではない。

決定モジュールの判断は、その判断によって途中層を飛ばした状態でも最終タスクを解けるようにモデル本体と共同で適応する必要がある。したがって既存チェックポイントへ未学習の判定器だけを追加しても、スキップ後の表現変化やKV除外に本体が適応しておらず、論文と同じ品質・計算量交換は期待できない。

Llama本体をLoRAで適応しつつdecision moduleも学習するため、導入コストは固定層 枝刈りより高い。

## 評価

### まず見るところ
- **結論:** トークンごとの層 skippingで、品質を大きく落とさずFLOPsを約半分まで減らせる。
- **重要な注意:** **主結果はFLOPsでありwall-clockではない**。
- **KV:** skip トークンのKVを後続attentionから外すとKV容量も約45%削減できるが、長文文脈とのtrade-offがある。
- **実装上の課題:** トークンごとの不規則分岐はGPUでまとめて計算しにくいため、理論計算削減を速度へ変換する専用実行時が必要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 評価設定

| 項目 | 設定 |
|---|---|
| Models | Llama 2 7B / Llama 3 8B |
| 層 | 32 |
| Training | LoRA + decision module |
| Tasks | Alpaca, SAMSum, GSM8K, MaWPS, BoolQ, PIQA, SIQA, OBQA, MMLU |
| FLOPs 比較対象 | Full-depth LoRA = 1.00 |

### Llama 2 7B：代表結果

| Task | D-LLM品質 | 正規化FLOPs |
|---|---:|---:|
| Alpaca | PPL 6.01 | 0.59 |
| SAMSum | PPL 3.18 | 0.55 |
| GSM8K | Acc 0.29 | 0.59 |
| MaWPS | Acc 0.74 | 0.56 |
| BoolQ | Acc 0.73 | 0.52 |
| PIQA | Acc 0.84 | 0.52 |
| SIQA | Acc 0.82 | 0.54 |
| OBQA | Acc 0.80 | 0.53 |
| MMLU | Acc 0.53 | 0.55 |

多くのtaskで**full-depthの約半分強の計算量**へ落としている。

### Llama 3 8B

複数taskで55%未満のFLOPsでもfull-depth LoRAと同等以上を維持する。

### さらに強くskipした場合

MaWPSやOBQAでは30〜40% FLOPsでも比較対象を上回る条件がある一方、SAMSumのようにtaskによっては計算量を削りすぎるとPPLが悪化する。

### KVをどこまで保護するか

| 設定 | 傾向 |
|---|---|
| m=0 | 文頭文脈を失いやすい |
| m=1 | 改善 |
| **m=2** | 最良 |
| m=4 / 8 | 保護量が増えメモリ削減が小さくなる |

skipしたトークンのKVをどう扱うかは品質へ大きく影響し、単に層を飛ばすだけでは不十分である。

### FLOPsとwall-clockを分けて読む理由

D-LLMではトークンごとに経路が違うため、GPU側では、

- 毎トークンのdecision module実行
- トークンごとに実行層が違うことによるバッチ分割
- KVを参照させるトークンを変えるmask生成
- 同じ演算へまとめにくい不規則なトークン grouping

が追加される。

そのため `FLOPs 0.55` を「1.82倍高速」と読み替えることはできない。大規模バッチのwall-clock 高速化倍率は主評価ではない。

実際のランタイムで速度へ変換するには、同じ層を実行するトークンをまとめ直して十分大きなGPU処理単位を作り、スキップしたトークンはそのカーネルへ投入しない仕組みが必要になる。分岐ごとに小さな処理を個別発行すると、FLOPsを減らしてもカーネル起動やトークン再配置の固定費が増える。したがってD-LLMは『どの計算を省けるか』を示すモデル側手法であり、その省略可能性を壁時計時間へ変える実行系最適化は別の重要課題である。

### 制約

- decision moduleの学習が必要。
- `Ω`、loss重み、学習時の離散判断近似parameterに依存。
- 長文ではKV 追い出しが文脈を損ねる可能性。
- 動的 branchをGPUで高速化する専用カーネル/実行時が必要。

</details>

## 一次資料
- [論文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html)
- [公式コード](https://github.com/Jyk-122/D-LLM)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: decision module / Gumbel-Softmax / KV 追い出しを補足し、FLOPsと実速度を分離して整理。
- 2026-09-07: Gumbel-Softmax / straight-through / acceleration-ratio loss / branch divergence等を、skip判断とGPU実行の具体的な意味へ平易化。
