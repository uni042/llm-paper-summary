---
title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
summary: "request全体ではなくoutput token生成1 iterationごとにbatchを組み替え、attention以外はtoken単位でまとめて計算することで、異なる長さ・進行位置のrequestを同じbatchで効率よくserveする分散LLM serving system。"
authors_affiliations: "Gyeong-In Yu, Joo Seong Jeong（Seoul National University）; Geon-Woo Kim（FriendliAI / Seoul National University）; Soojeong Kim（FriendliAI）; Byung-Gon Chun（FriendliAI / Seoul National University）"
published: "2022-07-11"
publication_status: "OSDI 2022"
lineage: "LLM Serving / Scheduling / Disaggregation"
topics: ["Iteration-level scheduling","Selective batching","Continuous batching","Distributed inference","Tensor parallelism","Pipeline parallelism"]
importance: "高"
hardware_evaluation: "実機"
source: "https://www.usenix.org/conference/osdi22/presentation/yu"
code: ""
last_checked: "2026-09-06"
---

# Orca: A Distributed Serving System for Transformer-Based Generative Models

> request全体ではなくoutput token生成1 iterationごとにbatchを組み替え、attention以外はtoken単位でまとめて計算することで、異なる長さ・進行位置のrequestを同じbatchで効率よくserveする分散LLM serving system。

## 概要

Orcaは、従来のinference serverが**batchをrequest単位で固定し、batch内の全requestが終わるまで組み替えない**ことがautoregressive generationに合わない点を問題にした研究である。

生成requestは必要なoutput token数が異なる。固定batchでは短いrequestが終わっても長いrequestを待つ必要があり、その間に到着したrequestもbatch終了まで参加できない。

Orcaはschedulerとexecution engineの境界を変更し、engineを**1 iterationだけ**実行して毎回schedulerへ戻す。各iterationの終了時点でfinished requestを外し、新着requestを加えられるため、batchを継続的に組み替えられる。

一方、異なる時点から参加したrequestはsequence lengthや現在位置が揃わないため、通常のbatch tensorにはまとめにくい。そこでOrcaは**selective batching**を導入し、attentionだけrequest別に実行し、Linear・LayerNorm・GeLUなどは全requestのtokenを平坦化してまとめて計算する。

このiteration-level schedulingは、後のvLLMやFastServeなどLLM serving systemで広く使われるcontinuous batchingの基礎となった。

## 問題設定

一般的なrequest-level batchingでは、一度engineへbatchを渡すと各requestの全generationが終わるまでschedulerが介入できない。

autoregressive generationでは1 tokenごとにmodel全体を繰り返し実行するため、本来はiteration間にrequestを入れ替えられる。しかし既存interfaceはこの性質を利用できず、

- 早く終了したrequestが長いrequestを待つ
- batch開始後に来たrequestが長時間queueで待つ
- requestごとのinput / output length差がbatch efficiencyを悪化させる

という問題が生じる。

ただしiterationごとに任意のrequestをbatchへ入れると、requestごとに処理済みtoken数が異なる。特にattentionは各requestの過去tokenだけを参照するため、単純に全requestを同じdense batch tensorへまとめられない。

Orcaは**scheduler granularityとoperator batchingを同時に変える**ことで、この2つの問題を解く。

## 手法

### 1. Iteration-level scheduling

schedulerはbatchを「requestが完了するまで」engineへ渡すのではなく、**1回のmodel iterationだけ**実行させる。

iterationが終わるたびにschedulerは、

- EOSなどで終了したrequestを除く
- 新着requestを追加する
- memoryやmax batch sizeを考慮して次のbatchを決める

という判断を行う。

これにより新着requestは現在のbatch全体が終わるのではなく、最長でも現在の1 iteration程度待てばbatchへ参加できる。

### 2. Selective batching

異なるrequestはsequence lengthが違うため、attention inputを通常の `[batch, sequence, hidden]` tensorに揃えにくい。

Orcaは非attention operatorについて、各requestのtokenをまとめて`[total_tokens, hidden]`の2次元tensorへ平坦化する。Linear、LayerNorm、Add、GeLUなどはrequest境界を意識しなくても計算できるため、この形で一括実行できる。

attention直前でtensorをrequestごとにsplitし、それぞれの過去K/Vに対してattentionを実行した後、結果をmergeして再び他operatorをbatch処理する。

attention自体にはmodel parameterがないため、weight reuseの観点ではLinear等ほどbatching benefitが大きくなく、個別実行による損失を比較的小さく抑えられる。

### 3. Distributed execution

数百B parameter modelを扱うため、Orcaはintra-layer parallelismとinter-layer parallelismを組み合わせる。

schedulerはiterationごとのrequest setに加え、pipeline stage間のmemory allocationとexecution orderも管理する。341B modelまでscaleする構成を評価している。

### 4. Schedulerとengineを密結合する

一般的なserving systemではschedulerとexecution engineを抽象化されたrequest-level interfaceで分離するが、そのinterfaceではiteration-level controlやselective batchingを表現しにくい。

Orcaは両者を密に統合し、batch metadata、sequence position、request completionなどをiterationごとに共有する。論文では、この機能を保ったまま一般的なscheduler-engine interfaceを設計することはfuture workとして残している。

## 評価

### 条件

| 項目 | 条件 |
|---|---|
| Cloud | Azure ND96asr A100 v4 |
| GPU | 1 VMあたり8× NVIDIA A100 40GB |
| GPU interconnect | NVLink |
| Node network | 8× Mellanox 200Gbps HDR InfiniBand / VM |
| Models | GPT 13B / 101B / 175B / 341B |
| Precision | FP16 |
| Max context | 2048 tokens |
| Baseline | NVIDIA FasterTransformer |

13Bは1 GPU、101Bは8 GPU、175Bは16 GPU、341Bは32 GPUを使う構成で評価している。

end-to-end workloadは当時公開のproduction LLM traceがなかったためsynthetic traceを使用し、input lengthは32〜512 token、最大generation lengthは1〜128 tokenから生成している。

### 主要結果

GPT-3 175Bで、median normalized latencyを約190ms/tokenに合わせた比較では、FasterTransformerの**0.185 request/s**に対しOrcaは**6.81 request/s**で、**36.9倍のthroughput**を達成した。

101B / 175B / 341Bのような大規模構成では、arrival time、input length、generation lengthが異なるrequestをiterationごとにbatchへ取り込める効果が大きく、同程度のlatencyでorder-of-magnitudeのthroughput差が生じる条件がある。

engine単体ではselective batchingによりattentionを個別実行するため、単純で均一なbatchではFasterTransformerと同等またはやや不利な条件もある。一方、175Bのdistributed構成ではcontrol / data planeの設計も効き、engine単体でも最大約47%高速な条件を報告している。

## 既存研究との差

### 従来のrequest-level batchingとの違い

Triton + FasterTransformerのような構成では、schedulerがbatchを作った後はbatch全体のgenerationが終わるまでrequest setを変えにくい。

Orcaは**1 token generationごとにschedulerへcontrolを戻す**ため、finished requestの即時返却とlate-arriving requestの途中参加を可能にする。

### vLLM / PagedAttentionとの関係

Orcaはiteration-level schedulingを導入したが、KV cache memory自体は後のvLLMほど柔軟には管理しない。vLLMはこのscheduling modelの上にPagedAttentionを導入し、KV memory fragmentationとcopy duplicationを大幅に減らす。

### FastServeとの関係

FastServeもiteration boundaryを使うが、Orcaよりさらに進めて**running requestをpreemptしpriorityを変更する**。Orcaが「batch membershipを毎iteration変えられる」基盤を作り、FastServeがそれをpriority schedulingへ拡張した関係にある。

## 限界

- 評価modelはGPT系列のみで、GQA / MLAなど現代的attention architectureは対象外。
- max sequence lengthは2048で、現在のlong-context servingとはmemory / attention bottleneckの比率が異なる。
- end-to-end workloadはsynthetic traceであり、production traceでの評価ではない。
- selective batchingはexecution engine側のoperator-awareな変更が必要で、既存engineへschedulerだけ追加する方式ではない。
- schedulerとengineを密結合しており、一般的なserving abstractionを維持したまま同じ制御を行うinterfaceは未解決。
- 公式の一般公開実装repositoryは確認できなかった。

## 一般的な実装上の含意

Orcaの重要な示唆は、autoregressive servingでは**requestをschedulerの最小単位にする必要がない**ことである。1 token generationを自然なscheduling boundaryとして使えば、異なるarrival timeやoutput lengthを持つrequestを高頻度にbatchへ出し入れできる。

また、batchingをmodel全体へ一律適用せず、parameter reuseのbenefitが大きいoperatorだけをまとめることで、irregular sequence shapeとGPU効率を両立できる。この「operatorごとにbatching strategyを変える」という考え方は、後続のcontinuous batching / paged attention runtimeにもつながる。

## コード

論文・USENIX公式ページから、著者による一般公開のOrca実装repositoryは確認できなかった。

## 引用関係

- FastServe / Sarathi-Serve / vLLM周辺の引用鎖から基礎研究として追加。
- 主要な先行研究: Triton Inference Server、FasterTransformer、Megatron-LM、DeepSpeed。
- 主要な後続方向: vLLM / PagedAttention、FastServe、Sarathi-Serveなどのcontinuous batching・memory management・preemptive scheduling。

## 一次資料

- OSDI 2022: https://www.usenix.org/conference/osdi22/presentation/yu
- 論文PDF: https://www.usenix.org/system/files/osdi22-yu.pdf

## 更新履歴

- 2026-09-06: Serving / Scheduling系統の引用探索から追加。OSDI 2022最終版を基準に概要・手法・評価・限界を整理。
