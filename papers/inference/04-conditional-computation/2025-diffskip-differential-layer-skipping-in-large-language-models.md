---
canonical_id: "ACL:2025.findings-acl.377"
last_audited: "2026-09-10"
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "DiffSkip: Differential Layer Skipping in Large Language Models"
summary: "tokenごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定layer削除より品質を保ちながら計算量を減らす。"
authors_affiliations: "一次資料記載の著者ら（Findings of ACL 2025）"
published: "2025-07-27"
publication_status: "Published"
lineage: "Conditional Computation"
topics: ["Dynamic depth","Quality-cost","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2025.findings-acl.377/"
code: ""
last_checked: "2026-09-02"
---

# DiffSkip: Differential Layer Skipping in Large Language Models

> tokenごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定layer削除より品質を保ちながら計算量を減らす。

## 概要
DiffSkipは、元LLMのFFNをmodelから削除せずに残し、**tokenごとに各FFNを実行するか、小さい代替変換だけで済ませるか**をrouterで選ぶdynamic skipping手法である。

着眼点は、あるtokenに対してFFN前後のhidden state差が小さいlayerは、そのtokenの表現をほとんど変えておらず、重いFFN計算を省ける可能性があるというもの。

元LLMのweightは固定し、後半layerへrouterと小型adapterだけを追加学習する。4 FFN skip程度なら固定layer削除よりかなり品質を守れる。

一方、論文の重要な結果は速度面で、**FLOPsを減らしても連続decodeのwall-clockはほぼ速くならない**。routerとadapterのweight read、tokenごとの分岐、GPU batchの分割がFFN削減分を相殺するためである。

## 手法のあらまし

### 1. FFN前後の表現差を冗長性の手掛かりにする

各FFNについて、入力hidden stateと出力hidden stateの差を見る。

差が小さいtokenは、そのFFNが表現をほとんど変えていないと考え、skipしやすい候補とする。

論文名の`Differential`はこの**layer変換前後の差分**を利用することに由来する。

論文が利用するもう一つの観察は、同じlayer内でself-attentionによる変化量と後続FFNによる変化量に強い相関があることである。FFNを実際に計算してから『変化が小さかったのでskipすべきだった』と判断しても計算削減にならないため、先に得られるattention側の差分をrouter signalとして使い、これから来るFFNの必要性を予測する。つまり安い前段情報から高価な後段変換の価値を推定する構造になっている。

### 2. Routerは後半layerだけに置く

初期layerは文脈形成への寄与が大きく、skipすると後続layerへ影響が広がりやすい。

そこでrouterは後半16 layerにだけ配置し、前半は常にfull executionする。

### 3. `Skip Adapter`：重いFFNを飛ばす時も小さな補正だけは行う

FFNを完全に飛ばしたhidden stateをそのまま次layerへ送ると表現分布がずれるため、skip側では小型adapterを通す。

adapterは元FFNよりかなり小さいが、完全なidentityではない。

このためDiffSkipは「FFNをゼロコストで飛ばす」というより、**大きいFFNを小さい近似変換へ置き換える**方式と見る方が正確である。

adapterが必要なのは、residual connectionがあってもFFNを完全identityにすると、後続layerが学習時に見てきたhidden-state分布からずれるためである。元LLMはfreezeしているので後続weight側をskip入力へ適応させられない。小型adapterだけをfine-tuneして、FFNを省いたtokenを元modelの表現空間へ近づけることで、dynamic routeを追加しても既存checkpointの大部分を変更せずに済む。

### 4. Skip / executeの離散判断を学習できるようにする

推論時には「FFNを実行する / skipする」の二択だが、そのままでは通常のgradientでrouterを学習しにくい。

そこで学習時だけ、離散選択を滑らかに近似してgradientをrouterへ流し、推論時にはhardな二択へ戻す。論文ではこの仕組みに`SparseMixer`を使う。

### 5. `Target Skip Count k`：平均で何FFN省くかを学習時に指定する

lossには、平均skip数を目標 `k` に近づけるpenaltyを入れる。

論文では4 skip / 8 skipなど、計算budgetごとに別設定を学習する。

つまり実行時に自由に任意kへ変える方式ではなく、**学習したbudget付近で使う**。

budget penaltyはrouterが全tokenをexecuteして品質だけを最大化する退化解と、逆に全tokenをskipして計算だけを最小化する退化解の間へ誘導する。各token・layerの局所判断は自由でもbatch全体では平均skip数をk付近へ保つため、品質比較を同程度のcompute budgetで行える。kを変えるとrouterが学ぶ境界自体も変わるので、単一checkpointで連続的に任意のspeed-quality点を選べるわけではない。

### 6. FFNだけをskipし、attentionは残す

主にFFN blockをskip対象とし、attentionは毎layer残す。

これにより文脈接続を維持しながら、計算量の大きいFFNだけをtokenごとに減らす。

## 評価

### まず見るところ
- **結論:** tokenごとにFFNを省くか判断すると、同じ数のFFNを固定的に省く方法より品質を守れる。
- **品質:** 4 skipではかなり良好、8 skipでは数学・推論taskから劣化が見える。
- **理論計算:** FFN FLOPsは減る。
- **実速度:** **連続decodeではほぼspeedupなし**。
- **重要な示唆:** conditional computationは、異なる経路を通るtokenを効率よくまとめる専用kernelがないとGPU速度へ直結しにくい。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### Llama-3-8B：主要結果

| Setting | MMLU | HellaSwag | WinoGrande | GSM8K | BBH | XSum | 平均保持率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 67.3 | 70.6 | 74.4 | 67.9 | 52.4 | 12.2 | 100% |
| 4 FFN skip | 66.3 | 73.2 | 74.3 | 64.8 | 50.2 | 12.3 | **99.0%** |
| 8 FFN skip | 62.4 | 68.7 | 74.2 | 57.8 | 44.6 | 10.7 | 91.3% |

4 skipなら多くのtaskでほぼ維持できるが、8 skipではreasoning系の低下が目立つ。

### Multi-token生成：固定skipとの比較

| Method | 4 skip保持率 | 8 skip保持率 |
|---|---:|---:|
| DiffSkip | **97.4%** | **91.3%** |
| EarlyExit | 55.0% | 48.0% |
| ShortGPT | 50.0% | 44.8% |
| LaCo | 91.5% | 65.3% |
| MindSkip | 53.7% | 47.9% |

長いgenerationでは、tokenごとに再判定するDiffSkipの利点が大きい。

### モデルサイズとskip余地

| Model | 平均skip数 |
|---|---:|
| Llama-3.2-3B | 3.1 |
| Llama-2-7B | 4.3 |
| Llama-2-13B | **9.1** |

大きいmodelほどFFN前後の表現差が小さいlayerが多く、skip余地も増える傾向。

### 数学data不足の影響

Tulu-v2に数学dataが少ないため、Llama-3-8BのGSM8Kは8 skipで67.9→57.2まで低下する。

数学強化dataを入れると改善するため、routerが「どのtokenならFFNを省いてよいか」を学ぶ能力はtraining data分布に依存する。

### Adapterの必要性

| Skip補正 | 品質保持率 |
|---|---:|
| Adapterなし | 23.2% |
| Linear adapter | 85.8% |
| Weightなし簡易補正 | 95.0% |
| Full DiffSkip | 最良 |

FFNをただ飛ばすだけでは成立しない。

### 実速度

8×A6000、batch 8、出力5 tokenではthroughputは小幅改善するが、**連続decodeでは実質speedupなし**。

主因は次の通り。

| Overhead | 内容 |
|---|---|
| Router | 毎token・毎可変layerでskip判断が必要 |
| Adapter | skipしても小さい別weightを読む |
| Branching | tokenごとに実行経路が異なる |
| Weight I/O | FFNとadapter双方のweight accessが発生 |
| GPU効率 | 同じbatch内のtokenが別経路へ分かれて一括計算しにくい |

FLOPsだけ見れば削減していても、memory-boundなdecodeでは計算量が主ボトルネックではない。

### 制約

- conditional routeを効率よく処理する専用kernel未実装。
- training data分布に依存。
- budget `k` ごとに学習が必要。
- 小型modelではskip余地が少ない。

</details>

## 一次資料
- [論文](https://aclanthology.org/2025.findings-acl.377/)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: differential signal / skip adapterを補足し、品質とwall-clockの差を表形式へ整理。
- 2026-09-07: SparseMixer / branching / kernel inefficiency等を、skip判断とGPU実行への具体的な影響として平易化。
