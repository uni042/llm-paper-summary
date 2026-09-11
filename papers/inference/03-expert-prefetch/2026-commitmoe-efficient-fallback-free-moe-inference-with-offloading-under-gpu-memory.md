---
canonical_id: AAAI:39454
arxiv_id: null
doi: 10.1609/aaai.v40i27.39454
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
title: 'CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints'
summary: 次layerで使うexpertを予測してGPUへ先読みし、予測が外れても正しいexpertを読み直さず、準備済みexpertをそのまま使うことでoffload待ちをなくす近似MoE方式。
authors_affiliations: Han Li, Jingwei Sun, Junqing Lin, Guangzhong Sun／University of Science and Technology of China
published: '2026-03-14'
publication_status: Published
lineage: Expert Prefetch
topics:
- CPU offload
- Expert prefetch
- Expert substitution
- Quality-cost
importance: 高
hardware_evaluation: 実機
source: https://ojs.aaai.org/index.php/AAAI/article/view/39454
code: null
implementation: 公式コード公開の記載はAAAI掲載ページで確認できず
last_checked: '2026-09-11'
authors:
- Han Li
- Jingwei Sun
- Junqing Lin
- Guangzhong Sun
publication: Proceedings of the AAAI Conference on Artificial Intelligence
publication_type: conference paper
sources:
- https://ojs.aaai.org/index.php/AAAI/article/view/39454
implementation_status: official-code-not-confirmed
---

# CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints

> 次層で使うエキスパートを予測してGPUへ先読みし、予測が外れても正しいエキスパートを読み直さず、準備済みエキスパートをそのまま使うことでオフロード待ちをなくす近似MoE方式。

## 概要

CommitMoEは、エキスパート 先読みで大きな待ち時間になる**prediction ミス時の追加読み込みそのものを行わない**。

通常の無損失 先読みは予測が外れると元の エキスパートをCPUから追加読み込みするため、その時点でGPUが重み到着を待つ。

CommitMoEは予測エキスパートを単なる候補ではなく実行対象として確定し、元の ルータとの不一致があっても正しいエキスパートを読み直さない。

その代わり、元の ルータが本来各エキスパートへ与えた重みを、すでにGPUへ準備できているエキスパートへ振り分け直す。論文ではこれを`Output-Weight Adjustment (OWA)`と呼ぶ。

したがって高速化の代償は明確で、**元の エキスパート computationを置換するapproximate inference**である。

## 手法のあらまし

### 1. `Commit Router`：次layer expertを予測する軽量MLP

現在トークンの状態から次MoE 層のエキスパート selectionを予測する軽量MLPを追加する。

1-層版は主に隣接層のルーティング相関を使い、2-層版は前後トークンの情報も使う。

元の ルータは固定したまま、予測器だけを「元の ルータと近いエキスパート分布を出す」ように学習する。

### 2. Prefetchしたexpertをそのまま実行対象にする

予測エキスパートは次層到達前にCPU DRAMからGPUへ非同期転送する。

次層で元の ルータが別エキスパートを選んでも、その元の エキスパートを読み込みし直さない。

これが`fallback-free`の意味で、**予測ミス時の追加PCIe待ちを完全に消す代わりに元モデルとは違うエキスパートを使う**。

### 3. Native routerが迷っているtokenほど置換影響が小さいという観察を使う

元の ルータの確率が一つのエキスパートへ強く集中していないトークンでは、どのエキスパートを選ぶかの判断が曖昧である。

著者らは、そのようなトークンほどエキスパート substitutionによる出力変化も小さい傾向を観察する。

この経験則を、fallbackを捨てる根拠に使う。ただし一般的な品質保証ではない。

逆にルータ certaintyが高いトークンで予測を外すと、元の モデルが強く必要としていたエキスパートを置換するため影響が大きくなり得る。Commit ルータの予測精度だけでなく、元の ルータがどれだけ一つの選択へ集中しているかを品質riskの手掛かりとして見る理由はここにある。fallback-free化はすべてのミスを同価値として扱うのではなく、ミスが許容されやすい領域が存在するという経験的性質へ依存している。

### 4. `OWA`：本来のrouter weightを準備済みexpertへ振り分け直す

predictionと元の Top-kが完全一致なら元の ルーティング 重みをそのまま使う。

一部一致 / 完全不一致の場合は、元の ルータが本来選んだエキスパートへ割り当てた重みを、GPUへ準備済みのエキスパートへ再配分する。

単純に全エキスパートを同じ重みで混ぜるより、**元の ルータがどれだけ強くエキスパートを必要としていたかという情報を残す**狙いがある。

### 5. Lossless prefetchとの違い

| 方式 | Prediction ミス時 | 品質 |
|---|---|---|
| ProMoE / SpecPrefetch | 元の エキスパートを追加読み込み | 無損失 |
| Speculating エキスパート | 元の エキスパートを読み込み + recompute | 無損失 |
| CommitMoE | 元の ミスを読み込みせず予測エキスパートを実行 | **approximate** |

CommitMoEの大きな高速化倍率は、このfallback elimination込みで解釈する必要がある。

無損失 先読みではprediction ミスのたびに正しいエキスパートを追加読み込みするため、最悪時には予測転送とdemand 転送の両方を支払う。CommitMoEは後者を完全に削るので、PCIeが遅いlegacy環境ほど相対利得が大きくなる。一方その速度は『予測をより早くした』だけでなく『正しい元の エキスパートを待つことをやめた』結果でもあり、品質-preserving system optimizationと同じ条件で比較してはいけない。

さらにOWAはミスした元の エキスパートの関数を再現するものではなく、利用可能なエキスパートの混合係数を調整して出力scaleやルータ preferenceの一部を残す補正である。準備済みエキスパートが元の集合と大きく異なれば、重みを再配分しても失われた非線形変換は戻らない。平均ベンチマークが維持される結果はこの近似が多くの入力で許容されたことを示すが、トークン単位 equivalenceや長期誤差の不存在を示すものではない。

この切り替えは、待ち時間を消す代わりに計算対象を変える明確な判断である。予測が信頼できる場合には準備済み集合をそのまま使い、信頼できない場合にも追加読み込みを待たないため、速度と品質の境界を設定値として明示できる。

この境界を把握するには、平均スループットだけでなく、予測が外れた入力でどのエキスパートが置換されたかも確認する必要がある。置換の頻度と元のルーティングとの差を併記すれば、速度向上が近似の強さに由来することを追跡できる。

この確認を行わずに平均値だけを比較すると、無損失な先読み方式との違いを見落とす。

## 評価

### まず見るところ
- **結論:** prediction ミス時の追加読み込みを完全に消すと大幅高速化できるが、元の エキスパートを置換する近似手法になる。
- **速度:** オフロード 比較対象比1.3〜9.4×。
- **品質:** 平均ベンチマーク スコアは元モデルに近いが、トークン単位 出力一致やworst caseは保証しない。
- **I/O:** CPU DRAM→GPUの元の ミス 転送をprediction hit/ミスに関係なく回避する。
- **注意点:** 無損失 先読みの高速化倍率と同列比較しないことが重要。

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

実行時はPyTorch + MoE-Infinity拡張。

### Speedup

MoE-Infinityを含むオフロード 比較対象に対し、エンドツーエンドで約1.3〜9.4×高速化。

高速化倍率幅は、

- PCIe帯域
- GPUへ置けるエキスパート数
- ルーティングをどれだけ予測しやすいか

へ強く依存する。

### 完全不一致時の品質観察

prediction エキスパートと元の Top-kが一つも一致しないケースでも、平均タスク スコアが大きく崩れない例を報告する。

| モデル / タスク | 元の | Commit型置換 |
|---|---:|---:|
| Qwen GSM8K | 53.22 | 54.51 |
| Qwen BBH | 36.67 | 36.75 |
| DeepSeek タスク A | 69.59 | 69.74 |
| DeepSeek タスク B | 49.12 | 49.16 |

これはルータが迷っているトークンではエキスパート置換への耐性が高いという観察を支持するが、一般的な安全保証ではない。

### 品質解釈の注意

平均精度が維持されても、

- トークン probability distribution
- free-form generation
- rare 入力文
- long-contextで誤差が積み重なる場合

が同じとは限らない。

### 制約

- approximate inference。
- SSD/NVMe未評価。
- long-generationで誤差が積み重なる場合の詳細評価は限定的。
- energy/トークン未評価。
- 公式 code未確認。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39454)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39454/43415)

## 更新履歴
- 2026-09-04: Commit ルータ / ルータ certainty / OWA / fallback-free substitutionを整理し、無損失 先読みとの差を明示。
- 2026-09-07: OWA / fallback-free / certainty / KL等を、予測ミス時に何を実行するかが分かる表現へ平易化。
