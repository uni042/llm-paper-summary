---
title: "CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints"
summary: "予測expertをfallbackなしで確定実行し、OWAでnative routing weightを準備済みexpertへ再配分することでoffload miss待ちを除く近似MoE方式。"
authors_affiliations: "Han Li, Jingwei Sun, Junqing Lin, Guangzhong Sun／University of Science and Technology of China"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert prefetch","Expert substitution","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39454"
code: ""
last_checked: "2026-09-03"
---

# CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints

> 予測expertをfallbackなしで確定実行し、OWAでnative routing weightを準備済みexpertへ再配分することでoffload miss待ちを除く近似MoE方式。

## 概要

CommitMoEは、expert prefetchで最も厄介な**prediction miss時のfallback loadそのものを捨てる**。

通常のlossless prefetchは予測が外れるとnative expertを追加loadするため、そのmiss latencyがcritical pathへ戻る。

CommitMoEは予測expertを単なる候補ではなく実行対象としてcommitし、native routerとの不一致があっても追加loadしない。

その代わり、native routerの確率massを、すでにresident / prefetched済みのexpertへ`Output-Weight Adjustment (OWA)`で再配分する。

したがって高速化の代償は明確で、**native expert computationを置換するapproximate inference**である。

## 手法のあらまし

### 1. `Commit Router`

現在tokenの状態から次MoE layerのexpert selectionを予測する軽量MLP。

1-layer版は主に隣接layer相関を使い、2-layer版はcross-token情報も扱う。

native routerはfreezeし、teacher distributionとのKL divergenceでpredictorだけを学習する。

### 2. Prefetchしたexpertをcommitする

予測expertは次layer到達前にCPU DRAMからGPUへ非同期transferする。

次layerでnative routerが別expertを選んでも、そのnative miss expertをloadし直さない。

これが`fallback-free`の意味である。

### 3. Router certaintyをKLで測る

native router distributionが一様に近いtokenでは、どのexpertを選ぶかの確信度が低い。

著者らは、そのような低certainty tokenほどexpert substitutionによる出力変化も小さい傾向を観察する。

この経験則を、fallbackを捨てる根拠に使う。

### 4. `OWA`：Output-Weight Adjustment

predictionとnative Top-kが完全一致ならnative routing weightをそのまま使う。

一部一致 / 完全不一致の場合は、native routerのweight massを準備済みexpertへ再配分する。

単純にuniform weightで代替するよりnative routing informationを残す狙いがある。

### 5. Lossless prefetchとの違い

| 方式 | Prediction miss時 | 品質 |
|---|---|---|
| ProMoE / SpecPrefetch | native expertを追加load | lossless |
| Speculating Experts | native expertをload + recompute | lossless |
| CommitMoE | native missをloadせず予測expertを実行 | **approximate** |

CommitMoEの大きなspeedupは、このfallback elimination込みで解釈する必要がある。

## 評価

### まず見るところ
- **結論:** fallback loadを完全に消すと大幅高速化できるが、native expertを置換する近似手法になる。
- **速度:** offloading baseline比1.3〜9.4×。
- **品質:** 平均benchmark scoreは元モデルに近いが、token-level output一致やworst caseは保証しない。
- **I/O:** CPU DRAM→GPUのnative miss transferをprediction hit/missに関係なく回避する。
- **注意点:** lossless prefetchのspeedupと同列比較しないことが重要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 実機環境

| 環境 | GPU | CPU | PCIe |
|---|---|---|---|
| High-end | RTX 4090 | Xeon W5-3435X | Gen4 x16 |
| Legacy | RTX 2080 Ti | Xeon E5-2680 v4 | Gen3 x16 |

### Models

- Qwen1.5-MoE-Chat
- DeepSeek-V2-Lite-Chat
- Mixtral-8x7B-Instruct

runtimeはPyTorch + MoE-Infinity拡張。

### Speedup

MoE-Infinityを含むoffloading baselineに対し、end-to-endで約1.3〜9.4×高速化。

speedup幅は、

- PCIe帯域
- cache容量
- routing predictability

へ強く依存する。

### 完全不一致時の品質観察

prediction expertとnative Top-kが一つも一致しないケースでも、平均task scoreが大きく崩れない例を報告する。

| Model / Task | Native | Commit型置換 |
|---|---:|---:|
| Qwen GSM8K | 53.22 | 54.51 |
| Qwen BBH | 36.67 | 36.75 |
| DeepSeek task A | 69.59 | 69.74 |
| DeepSeek task B | 49.12 | 49.16 |

これは低certainty tokenではexpert substitution toleranceが高いという観察を支持するが、一般的な安全保証ではない。

### 品質解釈の注意

平均accuracyが維持されても、

- token probability distribution
- free-form generation
- rare prompt
- long-context累積誤差

が同じとは限らない。

### 制約

- approximate inference。
- SSD/NVMe未評価。
- long-generation cumulative errorの詳細評価は限定的。
- energy/token未評価。
- official code未確認。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39454)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39454/43415)

## 更新履歴
- 2026-09-04: Commit Router / router certainty / OWA / fallback-free substitutionを整理し、lossless prefetchとの差を明示。
