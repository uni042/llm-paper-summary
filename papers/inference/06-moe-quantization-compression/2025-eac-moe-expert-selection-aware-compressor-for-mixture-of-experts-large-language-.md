---
canonical_id: ACL:2025.acl-long.633
arxiv_id: '2508.01625'
doi: 10.18653/v1/2025.acl-long.633
openreview_id: null
arxiv_categories:
  primary: cs.LG
  cross_list:
  - cs.AI
last_audited: '2026-09-10'
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: 'EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models'
summary: 量子化後も元モデルと近いexpertが選ばれるようrouter上位expertの誤差を重点的に補正し、prefillでほとんど使われないexpertを入力ごとに省く圧縮手法。
list_summary: "EAC-MoEは、量子化でルータが選ぶ専門家がずれる誤差を重点補正し、プリフィルで低頻度専門家を入力単位に枝刈りして、品質と容量を両立する。"
authors_affiliations: Yuanteng Chen, Yuantian Shao, Peisong Wang, Jian Cheng／Chinese Academy of Sciences, UCAS, Nanjing University of Science and Technology, AIRIA, [Maicro.ai](http://Maicro.ai)
published: '2025-08-03'
publication_status: Published
lineage: Quantization × MoE × Offload
topics:
- Quantization
- Dynamic Top-k
- Quality-cost
- Edge／on-device
importance: 高
hardware_evaluation: 実機
source: https://aclanthology.org/2025.acl-long.633/
code: null
implementation: 公式コード公開はarXivおよびACL Anthologyの一次資料で確認できず
last_checked: '2026-09-11'
authors:
- Yuanteng Chen
- Yuantian Shao
- Peisong Wang
- Jian Cheng
publication: ACL 2025
publication_type: Conference paper
sources:
- https://aclanthology.org/2025.acl-long.633/
implementation_status: official-code-not-confirmed
references:
- canonical_id: arXiv:2404.14219
  arxiv_id: '2404.14219'
- canonical_id: DOI:10.18653/v1/n19-1245
  doi: 10.18653/v1/n19-1245
- canonical_id: OpenReview:xXTkbTBmqq
  openreview_id: xXTkbTBmqq
- canonical_id: OpenReview:rAcgDBdKnP
  openreview_id: rAcgDBdKnP
- canonical_id: DOI:10.18653/v1/2022.emnlp-main.804
  doi: 10.18653/v1/2022.emnlp-main.804
- canonical_id: OpenReview:vXxardq6db
  openreview_id: vXxardq6db
- canonical_id: arXiv:2404.00456
  arxiv_id: '2404.00456'
- canonical_id: arXiv:2108.07732
  arxiv_id: '2108.07732'
- canonical_id: arXiv:2107.03374
  arxiv_id: '2107.03374'
- canonical_id: arXiv:1803.05457
  arxiv_id: '1803.05457'
- canonical_id: arXiv:2110.14168
  arxiv_id: '2110.14168'
- canonical_id: arXiv:2401.06066
  arxiv_id: '2401.06066'
- canonical_id: arXiv:2501.12948
  arxiv_id: '2501.12948'
- canonical_id: arXiv:2412.19437
  arxiv_id: '2412.19437'
- canonical_id: arXiv:2407.21783
  arxiv_id: '2407.21783'
- canonical_id: arXiv:2210.17323
  arxiv_id: '2210.17323'
- canonical_id: DOI:10.5281/zenodo.12608602
  doi: 10.5281/zenodo.12608602
- canonical_id: arXiv:2410.06270
  arxiv_id: '2410.06270'
- canonical_id: DOI:10.1162/neco.1991.3.1.79
  doi: 10.1162/neco.1991.3.1.79
- canonical_id: arXiv:2401.04088
  arxiv_id: '2401.04088'
- canonical_id: DOI:10.1162/neco.1994.6.2.181
  doi: 10.1162/neco.1994.6.2.181
- canonical_id: arXiv:2109.10465
  arxiv_id: '2109.10465'
- canonical_id: arXiv:2406.08155
  arxiv_id: '2406.08155'
- canonical_id: arXiv:2402.18158
  arxiv_id: '2402.18158'
- canonical_id: arXiv:2407.00945
  arxiv_id: '2407.00945'
- canonical_id: arXiv:2402.14800
  doi: 10.18653/v1/2024.acl-long.334
- canonical_id: arXiv:1609.07843
  arxiv_id: '1609.07843'
- canonical_id: DOI:10.18653/v1/2020.acl-main.92
  doi: 10.18653/v1/2020.acl-main.92
- canonical_id: DOI:10.48550/arxiv.2404.05089
  doi: 10.48550/arxiv.2404.05089
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: DOI:10.18653/v1/d19-1454
  doi: 10.18653/v1/d19-1454
- canonical_id: arXiv:2308.13137
  arxiv_id: '2308.13137'
- canonical_id: arXiv:1701.06538
  arxiv_id: '1701.06538'
- canonical_id: arXiv:2306.11695
  arxiv_id: '2306.11695'
- canonical_id: arXiv:2307.09288
  arxiv_id: '2307.09288'
- canonical_id: arXiv:2410.12013
  arxiv_id: '2410.12013'
- canonical_id: arXiv:2407.10671
  arxiv_id: '2407.10671'
- canonical_id: arXiv:2404.02852
  arxiv_id: '2404.02852'
- canonical_id: OpenReview:c8McWs4Av0
  openreview_id: c8McWs4Av0
- canonical_id: OpenReview:S1lN69AT-
  openreview_id: S1lN69AT-
references_checked_at: '2026-09-11'
references_source: arxiv-html-reference-section
references_total: 69
---

# EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models

> EAC-MoEは、量子化でルータが選ぶ専門家がずれる誤差を重点補正し、プリフィルで低頻度専門家を入力単位に枝刈りして、品質と容量を両立する。

## 概要

EAC-MoEは、量子化誤差を「エキスパートの出力値が少しずれる」だけでなく、**そのずれによって次のルータが別エキスパートを選んでしまうこと**まで含めて扱う。論文ではこのルーティングのずれを `expert-shift` と呼び、QESCで補正する。さらにプリフィル中のエキスパート利用頻度を見て、ほとんど使われないエキスパートをPESFでpruneする。

RTX 3090のMixtral-8x7Bでは、元の16ビットモデルの必要メモリ93.41GBをQESC+PESFで18.98GBにし、元/削減後の必要メモリ容量比93.41÷18.98=4.92倍と報告した。同じ元の16ビットモデルを比較対象とするE2E context-latency speedupは1.68倍で、平均精度低下は1%未満だった。平均2.06ビットではEAC-MoEの精度65.90、MC-MoEの精度62.56で、ルータの専門家ずれを補正した差が現れた。
## 手法のあらまし

### 1. 量子化誤差で次layerのexpert選択まで変わる

MoEではある層の量子化誤差が隠れ 状態へ入り、その隠れ 状態を次層のルータが読む。

その結果、元モデルではエキスパート A/BがTop-kだったのに、量子化後はA/Cになることがある。論文ではこれを **エキスパート-shift** と呼ぶ。

つまり量子化誤差は、単にエキスパート出力の近似誤差として終わらず、**ルーティング経路そのものを変えて後段へ増幅する**。

この増幅がMoE量子化を密 FFN量子化より難しくする。密 モデルならある層の小さい出力誤差は次層へ連続値として伝わるが、MoE ルータにはTop-kという離散境界がある。2 エキスパートのスコアが近いトークンでは小さな隠れ-状態誤差でも順位が反転し、その後は全く別のエキスパート 重みを通るため誤差が不連続に大きくなる。EAC-MoEはこの選択境界を守ることを量子化目的へ直接入れる。

### 2. `QESC`：router上位expertの順位を保つように量子化する

量子化 with エキスパート-選択 較正（QESC）は、通常のMSEだけでなく、ルータのTop-k選択を保つことを重視して量子化する。

QESC内の `TopK-MSE` は、全エキスパート出力を同じ重みで合わせるのではなく、**ルータ上位へ入るエキスパートとその出力のずれを重点的に小さくする**損失である。

狙いは「全出力を平均的に近づける」よりも、**元モデルと同じエキスパート rankingを維持すること**にある。

TopK-MSEで上位候補を重視するのは、ルータ下位エキスパートのスコアを多少誤っても実際の順伝播には選ばれず影響しない一方、Top-k境界付近の誤差はエキスパート-shiftを起こすためである。限られた量子化補正予算をルーティング decisionへ効く部分へ集中し、同じビット幅でもnative 実行 pathを維持しやすくする。したがってQESCは単なる低ビット 重み再構成ではなく、MoEの離散エキスパート-選択を保護する較正である。

### 3. routingのずれだけでも品質が悪化する

Mixtralの分析では、FPでルーティング shiftを起こさない状態のPPL 3.84に対し、FPでもshiftを許すと4.17、量子化だけで4.21、量子化＋shiftで4.65となる。

このため、ルーティング shiftを別の誤差要因として扱う意味がある。

### 4. `PESF`：prefill系列でほぼ使われないexpertを落とす

枝刈り 基づく on エキスパート-選択 頻度（PESF）は、現在の入力sequenceのプリフィル中に各エキスパートが何回選ばれたかを集計し、頻度が極端に低いエキスパートを実行集合から外す。

モデル-全体な静的枝刈りではなく、**入力sequenceごとにprune対象が変わる**。

ただし頻度を集めるには複数トークンが必要なので、1 トークンずつ進むデコードへそのまま適用する方式ではない。

PESFはプリフィル中に同じsequenceの多数トークンを観測できることを利用する。長いprompt内で一度も、あるいはほとんど選ばれなかったエキスパートはその入力domainでは重要度が低い可能性が高く、後続プリフィル処理から外すことで実GEMM数を減らせる。ただしデコードでは将来トークンのルーティングが変わる可能性があり、プリフィル頻度だけを根拠にエキスパートを恒久削除すると必要エキスパートを失う危険がある。このため適用phaseを分けている。

## 評価

### まず見るところ
- **結論:** 量子化後のルーティングずれまで校正すると、同じ低ビットでも品質を守りやすい。プリフィルでは低頻度エキスパート 枝刈りも追加できる。
- **圧縮:** MixtralをRTX 3090へ収められる規模まで軽量化。
- **品質:** moderate 枝刈りなら低下は小さいが、強く削ると明確に崩れる。
- **実速度:** RTX 3090で低ビット化＋枝刈りによる実高速化倍率を確認。
- **注意点:** PESFはsequence/プリフィル単位で、トークンごとのデコード 枝刈りではない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### Mixtralの主要結果

| 項目 | 結果 |
|---|---:|
| メモリ削減 | 4.92倍 |
| エンドツーエンド 高速化倍率 | 1.68倍 |
| 平均精度低下 | 1%未満 |

### 低bit条件でMC-MoEと比較

| 平均ビット | 方式 | PPL | 精度 | 高速化倍率 |
|---:|---|---:|---:|---:|
| 2.06 | MC-MoE | 5.51 | 62.56 | 1.80倍 |
| 2.06 | EAC-MoE | 5.14 | 65.90 | 1.82倍 |
| 2.56 | MC-MoE | 4.74 | 68.65 | 1.71倍 |
| 2.56 | EAC-MoE | 4.58 | 68.60 | 1.74倍 |

2.06 ビットの厳しい条件ではルーティングを保つ量子化補正の差が大きい。

### PESFのquality–compute trade-off

Mixtralで約30% 枝刈りした条件では、full 精度平均72.64に対し72.19と低下は小さい。一方、より攻撃的に削ると58.22まで落ちる。

したがってPESFは「不要エキスパートを無料で削れる」方式ではなく、**sequence 頻度を使って品質劣化を抑えながら枝刈り量を増やす方式**である。

### 適用範囲

評価はMixtral、Phi-3.5-MoE、DeepSeek-MoE-16B、Qwen1.5-MoE-A2.7B、RTX 3090。CPU/SSD オフロード トラフィックや671B級、デコード時の逐次枝刈りは未評価である。

</details>

## 引用関係
登録済みの [Examining Post-学習 量子化 for Mixture-of-エキスパート: A ベンチマーク](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)、[Mixture 圧縮器 for Mixture-of-エキスパート LLMs 利得 より多く](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)、[Not 全て エキスパート are Equal: 効率的 エキスパート 枝刈り and Skipping for Mixture-of-エキスパート 大きい Language モデル](../02-adaptive-expert-computation-compression/2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md) を引用する。
## 一次資料
- [ACL Anthology](https://aclanthology.org/2025.acl-long.633/)
- [arXiv](https://arxiv.org/abs/2508.01625)
## 更新履歴
- 2026-09-07: expert-shift / TopK-MSE / QESCをrouter上位expertの保持という具体的な処理として説明し直した。
