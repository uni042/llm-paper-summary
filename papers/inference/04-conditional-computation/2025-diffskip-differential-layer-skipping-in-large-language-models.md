---
title: "DiffSkip: Differential Layer Skipping in Large Language Models"
summary: "隣接層の表現差分を指標に冗長な層を選択的に飛ばし、品質劣化を抑えてLLM推論を高速化する方式。"
authors_affiliations: "一次資料記載の著者ら（Findings of ACL 2025）"
published: "2025-07-27"
publication_status: "Published"
lineage: "Conditional computation"
topics: ["Dynamic depth","Quality-cost","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2025.findings-acl.377/"
code: ""
last_checked: "2026-09-02"
---

# DiffSkip: Differential Layer Skipping in Large Language Models

> 隣接層の表現差分を指標に冗長な層を選択的に飛ばし、品質劣化を抑えてLLM推論を高速化する方式。

## 概要
DiffSkipは、元LLMのFFNを消さずに残し、**tokenごとに各FFNを実行するかskipするか**を小型routerで選ぶdynamic skipping手法である。

着眼点は、あるtokenに対してFFN前後の表現差が小さい層は、そのtokenにとって変換寄与が小さく、skip余地があるというもの。

元LLMのweightは凍結し、後半層へrouterとadapterだけを追加学習する。4 FFN skip程度なら固定layer削除よりかなり品質を守れる。

一方、論文の重要な結果は速度面で、**FLOPsを減らしても連続decodeのwall-clockはほぼ速くならない**。routerとadapterのweight fetch、tokenごとの分岐、I/OがFFN削減分を相殺するためである。

## 手法のあらまし

### 1. `Differential Signal`：FFNの入出力差を冗長性の手掛かりにする

各FFNについて、入力hidden stateと出力hidden stateの差を見る。

差が小さいtokenは、そのFFNが表現をほとんど変えていないと考え、skipしやすい候補とする。

論文名の `Differential` はこの**層変換前後の差分**を利用することに由来する。

### 2. Routerは後半層だけに置く

初期層は文脈形成への寄与が大きく、skipすると影響が広がりやすい。

そこでrouterは後半16層にだけ配置し、前半は常にfull executionする。

### 3. `Skip Adapter`

FFNを飛ばしたhidden stateをそのまま次層へ送ると表現分布がずれるため、skip側には小型adapterを通す。

adapterは元FFNよりかなり小さいが、完全なidentityではない。

このためDiffSkipは「FFNをゼロコストで飛ばす」というより、**大きいFFNを小さい近似変換へ置き換える**方式と見る方が正確である。

### 4. `SparseMixer`

routerのhardなskip/execute選択を学習可能にするためSparseMixerを使う。

推論時は離散的な経路選択をしつつ、学習時にはgradientが流れるようにする役割を持つ。

### 5. `Target Skip Count k`

lossには、平均skip数を目標 `k` に近づけるpenaltyを入れる。

論文では4 skip / 8 skipなど、計算budgetごとに別設定を学習する。

つまり実行時に自由に任意kへ変える方式ではなく、**学習したbudget付近で使う**。

### 6. FFNだけをskipし、attentionは残す

比較を公平にするため、主にFFN blockをskip対象とする。

attentionは毎層残すので、文脈接続を維持しながらFFN計算だけを削る設計になっている。

## 評価

### まず見るところ
- **結論:** token-adaptive FFN skipは固定skipより品質を守れる。
- **品質:** 4 skipではかなり良好、8 skipでは数学・推論taskから劣化が見える。
- **理論計算:** FFN FLOPsは減る。
- **実速度:** **連続decodeではほぼspeedupなし**。
- **重要な示唆:** conditional computationは専用kernel/token groupingなしではGPU速度に直結しない。

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

大きいmodelほど冗長性が高く、skip余地も増える傾向。

### 数学data不足の影響

Tulu-v2に数学dataが少ないため、Llama-3-8BのGSM8Kは8 skipで67.9→57.2まで低下する。

数学強化dataを入れると改善するため、routerの「難しいtoken判定」は学習data分布に依存する。

### Adapter ablation

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
| Router | 毎token・毎可変層で判定 |
| Adapter | skipしても別weightを読む |
| Branching | tokenごとに経路が異なる |
| Weight I/O | FFNとadapter双方のfetchが発生 |
| Kernel inefficiency | dense batchが分割される |

FLOPsだけ見れば削減していても、memory-boundなdecodeでは計算量が主ボトルネックではない。

### 制約

- specialized kernel未実装。
- training data分布に依存。
- budget `k` ごとに学習が必要。
- 小型modelではskip余地が少ない。

</details>

## 一次資料
- [論文](https://aclanthology.org/2025.findings-acl.377/)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: differential signal / skip adapterを補足し、品質とwall-clockの差を表形式へ整理。
