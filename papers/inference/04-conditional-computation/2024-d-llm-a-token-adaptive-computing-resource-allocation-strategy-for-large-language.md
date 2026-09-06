---
title: "D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models"
summary: "各token・各layerで『このlayerを実行するか』を小型moduleが判断し、skipしたtokenのKVも後続attentionから外すことで、計算量とKV使用量をtokenごとに変える。"
authors_affiliations: "一次資料記載の著者ら（NeurIPS 2024）"
published: "2024-12-15"
publication_status: "Published"
lineage: "Conditional Computation"
topics: ["Dynamic depth","KV cache offload","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html"
code: "https://github.com/Jyk-122/D-LLM"
last_checked: "2026-09-02"
---

# D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models

> 各token・各layerで「このlayerを実行するか」を小型moduleが判断し、skipしたtokenのKVも後続attentionから外すことで、計算量とKV使用量をtokenごとに変える。

## 概要
D-LLMは、**各token・各layerごとに「このlayerを実行するかskipするか」を学習する**dynamic depth方式である。

系列全体を同じ深度で処理するlayer pruningとは異なり、同じlayerでもtoken Aは実行、token Bはskipという分岐が起こる。難しいtokenへ多くの計算を割き、単純なtokenは浅く処理することを狙う。

各layerの前に小型decision moduleを追加し、目標計算量 `Ω` に近づくようskip率を学習する。さらに、skipしたtokenのKVを後続attentionから隠すことで、computeだけでなくKV容量も削る。

Llama 2 7Bではfull-depth LoRAの約55〜59%のFLOPs、Llama 3 8Bでは約52〜55%程度まで減らしながら、多くのtaskで同等以上の品質を示す。ただし論文の中心指標はFLOPsで、**FLOPs半減＝wall-clock 2倍高速化を実証した研究ではない**。

## 手法のあらまし

### 1. 小型moduleがtokenごとにexecute / skipを決める

各Transformer layerの直前に小型moduleを置き、現在のhidden stateから、

- このlayerを実行する
- このlayerをskipする

の2択を出す。

この判定がtoken単位なので、同一batch・同一layerでも実行経路が分かれる。

### 2. 0/1のskip判断を学習できるよう、学習時だけ滑らかな近似を使う

execute / skipは本来0/1の離散判断なので、そのままでは通常のgradientを流しにくい。

D-LLMは学習中だけGumbel-Softmaxという方法で「execute寄り / skip寄り」の連続値を作り、forwardではhardな0/1選択を使いつつ、backwardでは連続値のgradientを利用する。

要するに、**推論時は本当にlayerを飛ばすが、学習時だけ微分可能な近似を使う**。

### 3. 平均skip率を目標計算量 `Ω` に近づける

単に「skipできるところは全部skip」と学習すると、品質重視ならほぼ全layer実行、計算量重視なら過剰skipへ崩れやすい。

そこで平均skip率と指定した目標 `Ω` の差をlossへ加え、全体の計算量を狙ったbudgetへ寄せる。

`Ω`を変えることで、品質重視・計算量重視の別modelを作れる。

### 4. 最初の2 layerは必ず実行する

初期layerまで動的にskipすると表現形成が不安定になるため、実験では最初の2 layerをdecision対象外にする。

全32 layerを完全自由にrouteしているわけではない。

### 5. SkipしたtokenのKVも後続attentionから外す

D-LLMでは、あるtokenがlayer `l` をskipした場合、そのtokenのK/Vを後続queryから参照させない。

これによりlayer計算だけでなくKV storageも減らせる。

ただし長距離文脈を失いやすくなるため、文頭の最初 `m` tokenは必ずKVを残す。本実験では `m=2` が最良だった。

### 6. 追加学習が必要

元checkpointへ推論時だけ差し込むtraining-free手法ではない。

Llama本体をLoRAで適応しつつdecision moduleも学習するため、導入コストは固定layer pruningより高い。

## 評価

### まず見るところ
- **結論:** tokenごとのlayer skippingで、品質を大きく落とさずFLOPsを約半分まで減らせる。
- **重要な注意:** **主結果はFLOPsでありwall-clockではない**。
- **KV:** skip tokenのKVを後続attentionから外すとKV容量も約45%削減できるが、長文文脈とのtrade-offがある。
- **実装上の課題:** tokenごとの不規則分岐はGPUでまとめて計算しにくいため、理論計算削減を速度へ変換する専用runtimeが必要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 評価設定

| 項目 | 設定 |
|---|---|
| Models | Llama 2 7B / Llama 3 8B |
| Layers | 32 |
| Training | LoRA + decision module |
| Tasks | Alpaca, SAMSum, GSM8K, MaWPS, BoolQ, PIQA, SIQA, OBQA, MMLU |
| FLOPs baseline | Full-depth LoRA = 1.00 |

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

MaWPSやOBQAでは30〜40% FLOPsでもbaselineを上回る条件がある一方、SAMSumのようにtaskによっては計算量を削りすぎるとPPLが悪化する。

### KVをどこまで保護するか

| 設定 | 傾向 |
|---|---|
| m=0 | 文頭文脈を失いやすい |
| m=1 | 改善 |
| **m=2** | 最良 |
| m=4 / 8 | 保護量が増えmemory削減が小さくなる |

skipしたtokenのKVをどう扱うかは品質へ大きく影響し、単にlayerを飛ばすだけでは不十分である。

### FLOPsとwall-clockを分けて読む理由

D-LLMではtokenごとに経路が違うため、GPU側では、

- 毎tokenのdecision module実行
- tokenごとに実行layerが違うことによるbatch分割
- KVを参照させるtokenを変えるmask生成
- 同じ演算へまとめにくい不規則なtoken grouping

が追加される。

そのため `FLOPs 0.55` を「1.82倍高速」と読み替えることはできない。大規模batchのwall-clock speedupは主評価ではない。

### 制約

- decision moduleの学習が必要。
- `Ω`、loss重み、学習時の離散判断近似parameterに依存。
- 長文ではKV evictionが文脈を損ねる可能性。
- dynamic branchをGPUで高速化する専用kernel/runtimeが必要。

</details>

## 一次資料
- [論文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html)
- [公式コード](https://github.com/Jyk-122/D-LLM)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: decision module / Gumbel-Softmax / KV evictionを補足し、FLOPsと実速度を分離して整理。
- 2026-09-07: Gumbel-Softmax / straight-through / acceleration-ratio loss / branch divergence等を、skip判断とGPU実行の具体的な意味へ平易化。
