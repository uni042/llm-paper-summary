---
canonical_id: "ACL:2025.acl-long.633"
last_audited: null
audit_version: 0
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models"
summary: "量子化後も元モデルと近いexpertが選ばれるようrouter上位expertの誤差を重点的に補正し、prefillでほとんど使われないexpertを入力ごとに省く圧縮手法。"
authors_affiliations: "Yuanteng Chen, Yuantian Shao, Peisong Wang, Jian Cheng／Chinese Academy of Sciences, UCAS, Nanjing University of Science and Technology, AIRIA, [Maicro.ai](http://Maicro.ai)"
published: "2025-08-03"
publication_status: "Published"
lineage: "Quantization × MoE × Offload"
topics: ["Quantization","Dynamic Top-k","Quality-cost","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2025.acl-long.633/"
code: ""
last_checked: "2026-09-03"
---

# EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models

> 量子化後も元モデルと近いexpertが選ばれるようrouter上位expertの誤差を重点的に補正し、prefillでほとんど使われないexpertを入力ごとに省く圧縮手法。

## 概要
EAC-MoEは、量子化誤差を「expertの出力値が少しずれる」だけでなく、**そのずれによって次のrouterが別expertを選んでしまうこと**まで含めて扱う。論文ではこのroutingのずれを `expert-shift` と呼び、QESCで補正する。さらにprefill中のexpert利用頻度を見て、ほとんど使われないexpertをPESFでpruneする。

## 手法のあらまし

### 1. 量子化誤差で次layerのexpert選択まで変わる

MoEではあるlayerの量子化誤差がhidden stateへ入り、そのhidden stateを次layerのrouterが読む。

その結果、元モデルではexpert A/BがTop-kだったのに、量子化後はA/Cになることがある。論文ではこれを **expert-shift** と呼ぶ。

つまり量子化誤差は、単にexpert出力の近似誤差として終わらず、**routing経路そのものを変えて後段へ増幅する**。

### 2. `QESC`：router上位expertの順位を保つように量子化する

Quantization with Expert-Selection Calibration（QESC）は、通常のMSEだけでなく、routerのTop-k選択を保つことを重視して量子化する。

QESC内の `TopK-MSE` は、全expert出力を同じ重みで合わせるのではなく、**router上位へ入るexpertとその出力のずれを重点的に小さくする**損失である。

狙いは「全出力を平均的に近づける」よりも、**元モデルと同じexpert rankingを維持すること**にある。

### 3. routingのずれだけでも品質が悪化する

Mixtralの分析では、FPでrouting shiftを起こさない状態のPPL 3.84に対し、FPでもshiftを許すと4.17、量子化だけで4.21、量子化＋shiftで4.65となる。

このため、routing shiftを別の誤差要因として扱う意味がある。

### 4. `PESF`：prefill系列でほぼ使われないexpertを落とす

Pruning based on Expert-Selection Frequency（PESF）は、現在の入力sequenceのprefill中に各expertが何回選ばれたかを集計し、頻度が極端に低いexpertを実行集合から外す。

model-globalな静的pruningではなく、**入力sequenceごとにprune対象が変わる**。

ただしfrequencyを集めるには複数tokenが必要なので、1 tokenずつ進むdecodeへそのまま適用する方式ではない。

## 評価

### まず見るところ
- **結論:** 量子化後のroutingずれまで校正すると、同じ低bitでも品質を守りやすい。prefillでは低頻度expert pruningも追加できる。
- **圧縮:** MixtralをRTX 3090へ収められる規模まで軽量化。
- **品質:** moderate pruningなら低下は小さいが、強く削ると明確に崩れる。
- **実速度:** RTX 3090で低bit化＋pruningによる実speedupを確認。
- **注意点:** PESFはsequence/prefill単位で、tokenごとのdecode pruningではない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### Mixtralの主要結果

| 項目 | 結果 |
|---|---:|
| memory削減 | 4.92倍 |
| end-to-end speedup | 1.68倍 |
| 平均accuracy低下 | 1%未満 |

### 低bit条件でMC-MoEと比較

| 平均bit | 方式 | PPL | accuracy | speedup |
|---:|---|---:|---:|---:|
| 2.06 | MC-MoE | 5.51 | 62.56 | 1.80倍 |
| 2.06 | EAC-MoE | 5.14 | 65.90 | 1.82倍 |
| 2.56 | MC-MoE | 4.74 | 68.65 | 1.71倍 |
| 2.56 | EAC-MoE | 4.58 | 68.60 | 1.74倍 |

2.06 bitの厳しい条件ではroutingを保つ量子化補正の差が大きい。

### PESFのquality–compute trade-off

Mixtralで約30% pruningした条件では、full precision平均72.64に対し72.19と低下は小さい。一方、より攻撃的に削ると58.22まで落ちる。

したがってPESFは「不要expertを無料で削れる」方式ではなく、**sequence frequencyを使って品質劣化を抑えながらpruning量を増やす方式**である。

### 適用範囲

評価はMixtral、Phi-3.5-MoE、DeepSeek-MoE-16B、Qwen1.5-MoE-A2.7B、RTX 3090。CPU/SSD offload trafficや671B級、decode時の逐次pruningは未評価である。

</details>

## 引用関係
登録済みの [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)、[Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)、[Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](../02-adaptive-expert-computation-compression/2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md) を引用する。
## 一次資料
- [ACL Anthology](https://aclanthology.org/2025.acl-long.633/)
- [arXiv](https://arxiv.org/abs/2508.01625)
## 更新履歴
- 2026-09-07: expert-shift / TopK-MSE / QESCをrouter上位expertの保持という具体的な処理として説明し直した。
