---
canonical_id: ACL:2025.findings-acl.377
arxiv_id: null
doi: 10.18653/v1/2025.findings-acl.377
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
title: 'DiffSkip: Differential Layer Skipping in Large Language Models'
summary: tokenごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定layer削除より品質を保ちながら計算量を減らす。
authors_affiliations: 一次資料記載の著者ら（Findings of ACL 2025）
published: '2025-07-27'
publication_status: Published
lineage: Conditional Computation
topics:
- Dynamic depth
- Quality-cost
- Edge／on-device
importance: 高
hardware_evaluation: 実機
source: https://aclanthology.org/2025.findings-acl.377/
code: null
implementation: 公式コード公開の記載はACL Anthology掲載ページで確認できず
last_checked: '2026-09-11'
authors:
- Xuan Luo
- Weizhi Wang
- Xifeng Yan
publication: 'Findings of the Association for Computational Linguistics: ACL 2025'
publication_type: conference paper
sources:
- https://aclanthology.org/2025.findings-acl.377/
implementation_status: official-code-not-confirmed
references:
- canonical_id: ACL:2024.acl-long.681
  arxiv_id: '2310.10449'
references_checked_at: '2026-09-11'
references_source: primary-pdf-reference-section
references_total: 1
---

# DiffSkip: Differential 層 Skipping in Large Language Models

> トークンごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定層削除より品質を保ちながら計算量を減らす。

## 概要
DiffSkipは、元LLMのFFNをmodelから削除せずに残し、**トークンごとに各FFNを実行するか、小さい代替変換だけで済ませるか**をルータで選ぶ動的 skipping手法である。

判断の対象はモデル全体ではなく各トークンと各層の組み合わせであるため、表現をほとんど変えない箇所だけを狙って計算を省ける。元の重みを残したまま軽い経路を追加するので、品質を確認しながら削減量を調整できる。

着眼点は、あるトークンに対してFFN前後のhidden state差が小さい層は、そのトークンの表現をほとんど変えておらず、重いFFN計算を省ける可能性があるというもの。

元LLMの重みは固定し、後半層へルータと小型adapterだけを追加学習する。4 FFN skip程度なら固定層削除よりかなり品質を守れる。

一方、論文の重要な結果は速度面で、**FLOPsを減らしても連続デコードのwall-clockはほぼ速くならない**。ルータとadapterの重み read、トークンごとの分岐、GPU バッチの分割がFFN削減分を相殺するためである。

## 手法

### 1. FFN前後の表現差を冗長性の手掛かりにする

各FFNについて、入力hidden stateと出力hidden stateの差を見る。

差が小さいトークンは、そのFFNが表現をほとんど変えていないと考え、skipしやすい候補とする。

論文名の`Differential`はこの**層変換前後の差分**を利用することに由来する。

論文が利用するもう一つの観察は、同じ層内でself-attentionによる変化量と後続FFNによる変化量に強い相関があることである。FFNを実際に計算してから『変化が小さかったのでskipすべきだった』と判断しても計算削減にならないため、先に得られるattention側の差分をルータ signalとして使い、これから来るFFNの必要性を予測する。つまり安い前段情報から高価な後段変換の価値を推定する構造になっている。

### 2. ルータは後半層だけに置く

初期層は文脈形成への寄与が大きく、skipすると後続層へ影響が広がりやすい。

そこでルータは後半16 層にだけ配置し、前半は常にfull executionする。

### 3. `Skip Adapter`：重いFFNを飛ばす時も小さな補正だけは行う

FFNを完全に飛ばしたhidden stateをそのまま次層へ送ると表現分布がずれるため、skip側では小型adapterを通す。

adapterは元FFNよりかなり小さいが、完全なidentityではない。

このためDiffSkipは「FFNをゼロコストで飛ばす」というより、**大きいFFNを小さい近似変換へ置き換える**方式と見る方が正確である。

adapterが必要なのは、residual connectionがあってもFFNを完全identityにすると、後続層が学習時に見てきたhidden-state分布からずれるためである。元LLMはfreezeしているので後続重み側をskip入力へ適応させられない。小型adapterだけをfine-tuneして、FFNを省いたトークンを元modelの表現空間へ近づけることで、動的 routeを追加しても既存checkpointの大部分を変更せずに済む。

### 4. Skip / executeの離散判断を学習できるようにする

推論時には「FFNを実行する / skipする」の二択だが、そのままでは通常のgradientでルータを学習しにくい。

そこで学習時だけ、離散選択を滑らかに近似してgradientをルータへ流し、推論時にはhardな二択へ戻す。論文ではこの仕組みに`SparseMixer`を使う。

### 5. `Target Skip Count k`：平均で何FFN省くかを学習時に指定する

lossには、平均skip数を目標 `k` に近づけるpenaltyを入れる。

論文では4 skip / 8 skipなど、計算budgetごとに別設定を学習する。

つまり実行時に自由に任意kへ変える方式ではなく、**学習したbudget付近で使う**。

budget penaltyはルータが全トークンをexecuteして品質だけを最大化する退化解と、逆に全トークンをskipして計算だけを最小化する退化解の間へ誘導する。各トークン・層の局所判断は自由でもバッチ全体では平均skip数をk付近へ保つため、品質比較を同程度のcompute budgetで行える。kを変えるとルータが学ぶ境界自体も変わるので、単一checkpointで連続的に任意のspeed-quality点を選べるわけではない。

### 6. FFNだけをskipし、attentionは残す

主にFFN blockをskip対象とし、attentionは毎層残す。

これにより文脈接続を維持しながら、計算量の大きいFFNだけをトークンごとに減らす。

以上の整理は、提案手法の動作原理と前提条件を保ったまま、一次資料の記述を要約したものである。

## 評価

一方で、トークンごとの経路分岐はGPU上で処理を分割し、ルータや小型変換の読み出しも増やす。したがって、演算数の削減がそのまま実時間の短縮になるとは限らず、実装上のまとめ方まで含めて評価する必要がある。
品質を保つ効果と、分岐管理に伴う負担を同時に測ることが、手法の実用性を判断する鍵になる。
この差を明示することで、理論計算量と実運用上の遅延を混同しない。
特に連続生成では、経路が細かく分かれるほどこの差が広がりやすい。
品質と速度の両面を実機で測ることが不可欠である。ルータの判断を増やすだけでは、理論上の省計算を利用者が感じる短縮へ変換できない。評価は、どの層をどのトークンで省いたか、追加部品がどの程度の読み出しを生むか、そしてGPUの実行単位がどれだけ細切れになるかを併せて確認する必要がある。
したがって、単一の平均値ではなく、入力長とバッチ条件を変えた結果を読む必要がある。
入力の違いによる揺れを含めて判断する。
理論値だけで実運用の改善を判断してはいけない。
入力長、バッチの大きさ、GPUの実装によって、分岐を処理する費用は異なる。したがって品質の維持と実時間の短縮を同じ条件で測定し、どの条件で利点が現れるかを確かめる必要がある。

### まず見るところ
- **結論:** トークンごとにFFNを省くか判断すると、同じ数のFFNを固定的に省く方法より品質を守れる。
- **品質:** 4 skipではかなり良好、8 skipでは数学・推論taskから劣化が見える。
- **理論計算:** FFN FLOPsは減る。
- **実速度:** **連続デコードではほぼ高速化倍率なし**。
- **重要な示唆:** 条件al computationは、異なる経路を通るトークンを効率よくまとめる専用カーネルがないとGPU速度へ直結しにくい。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### Llama-3-8B：主要結果

| Setting | MMLU | HellaSwag | WinoGrande | GSM8K | BBH | XSum | 平均保持率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 比較対象 | 67.3 | 70.6 | 74.4 | 67.9 | 52.4 | 12.2 | 100% |
| 4 FFN skip | 66.3 | 73.2 | 74.3 | 64.8 | 50.2 | 12.3 | **99.0%** |
| 8 FFN skip | 62.4 | 68.7 | 74.2 | 57.8 | 44.6 | 10.7 | 91.3% |

4 skipなら多くのtaskでほぼ維持できるが、8 skipではreasoning系の低下が目立つ。

### Multi-トークン生成：固定skipとの比較

| Method | 4 skip保持率 | 8 skip保持率 |
|---|---:|---:|
| DiffSkip | **97.4%** | **91.3%** |
| EarlyExit | 55.0% | 48.0% |
| ShortGPT | 50.0% | 44.8% |
| LaCo | 91.5% | 65.3% |
| MindSkip | 53.7% | 47.9% |

長いgenerationでは、トークンごとに再判定するDiffSkipの利点が大きい。

### モデルサイズとskip余地

| Model | 平均skip数 |
|---|---:|
| Llama-3.2-3B | 3.1 |
| Llama-2-7B | 4.3 |
| Llama-2-13B | **9.1** |

大きいmodelほどFFN前後の表現差が小さい層が多く、skip余地も増える傾向。

### 数学data不足の影響

Tulu-v2に数学dataが少ないため、Llama-3-8BのGSM8Kは8 skipで67.9→57.2まで低下する。

数学強化dataを入れると改善するため、ルータが「どのトークンならFFNを省いてよいか」を学ぶ能力はtraining data分布に依存する。

### Adapterの必要性

| Skip補正 | 品質保持率 |
|---|---:|
| Adapterなし | 23.2% |
| Linear adapter | 85.8% |
| 重みなし簡易補正 | 95.0% |
| Full DiffSkip | 最良 |

FFNをただ飛ばすだけでは成立しない。

### 実速度

8×A6000、バッチ 8、出力5 トークンではスループットは小幅改善するが、**連続デコードでは実質高速化倍率なし**。

主因は次の通り。

| オーバーヘッド | 内容 |
|---|---|
| ルータ | 毎トークン・毎可変層でskip判断が必要 |
| Adapter | skipしても小さい別重みを読む |
| Branching | トークンごとに実行経路が異なる |
| 重み I/O | FFNとadapter双方の重み accessが発生 |
| GPU効率 | 同じバッチ内のトークンが別経路へ分かれて一括計算しにくい |

FLOPsだけ見れば削減していても、メモリ-boundなデコードでは計算量が主ボトルネックではない。

### 制約

- 条件al routeを効率よく処理する専用カーネル未実装。
- training data分布に依存。
- budget `k` ごとに学習が必要。
- 小型modelではskip余地が少ない。

</details>

## 一次資料
- [論文](https://aclanthology.org/2025.findings-acl.377/)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: differential signal / skip adapterを補足し、品質とwall-clockの差を表形式へ整理。
- 2026-09-07: SparseMixer / branching / カーネル inefficiency等を、skip判断とGPU実行への具体的な影響として平易化。
