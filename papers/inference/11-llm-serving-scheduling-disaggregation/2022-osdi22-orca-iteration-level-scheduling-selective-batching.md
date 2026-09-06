---
title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
summary: "output tokenを1つ生成するたびにbatchを組み替え、長さや進行位置が異なるrequestを途中からbatchへ出し入れできるようにした分散LLM serving system。"
authors_affiliations: "Gyeong-In Yu, Joo Seong Jeong（Seoul National University）; Geon-Woo Kim（FriendliAI / Seoul National University）; Soojeong Kim（FriendliAI）; Byung-Gon Chun（FriendliAI / Seoul National University）"
published: "2022-07-11"
publication_status: "OSDI 2022"
lineage: "LLM Serving / Scheduling / Disaggregation"
topics: ["Continuous batching","Selective batching","Distributed inference","Tensor parallelism","Pipeline parallelism"]
importance: "高"
hardware_evaluation: "実機"
source: "https://www.usenix.org/conference/osdi22/presentation/yu"
code: ""
last_checked: "2026-09-07"
---

# Orca: A Distributed Serving System for Transformer-Based Generative Models

> output tokenを1つ生成するたびにbatchを組み替え、長さや進行位置が異なるrequestを途中からbatchへ出し入れできるようにした分散LLM serving system。

## 概要

従来のinference serverでは、一度batchを作ると、そのbatch内のrequestがすべて終了するまで中身を変えない方式が一般的だった。しかしLLMの生成ではrequestごとにoutput長が異なるため、短いrequestが終わっても長いrequestを待つことになり、その間に新しく来たrequestも参加できない。

Orcaは、**request全体ではなく「output tokenを1つ生成する処理」を1回の単位としてschedulerへ戻す**。1 token生成するたびに終了したrequestを外し、新着requestを加えられるため、batchを継続的に組み替えられる。現在一般的なcontinuous batchingの基礎になった考え方である。

ただし途中からbatchへ入ったrequestはsequence長が揃わない。そこでOrcaは、attentionだけrequestごとに処理し、LinearやLayerNormなどは全requestのtokenをまとめて計算する。論文ではこの方法を **selective batching** と呼ぶ。

## 問題設定

LLM生成は1 tokenごとにmodel全体を繰り返し実行するため、本来はtoken生成の間にrequestを入れ替えられる。ところがrequest単位でbatchを固定すると、

- 短いrequestが終わっても長いrequestが終わるまでGPU枠が空かない
- batch開始後に来たrequestが長く待つ
- input / output長の差が大きいほどGPU利用効率が下がる

という問題が起きる。

一方で、requestを自由に途中参加させると各requestの処理済みtoken数が異なる。特にattentionはrequestごとに参照する過去token数が違うため、すべてを同じ形のtensorへ単純にまとめることはできない。

## 手法

### 1. 1 token生成ごとにbatchを見直す

Orcaは1回のmodel実行が終わるたびにschedulerへ制御を戻す。schedulerは、

- 終了したrequestを除く
- 新しいrequestを追加する
- memoryとbatch sizeを見て次に実行するrequestを決める

という処理を行う。

これにより、新着requestは現在の長いrequestが完全に終わるまで待つ必要がなくなる。

### 2. attention以外はまとめて計算する

requestごとにsequence長が違っても、Linear、LayerNorm、GeLUなどは各tokenを独立にまとめて処理できる。そこでOrcaは全requestのtokenを1つの2次元tensorへ並べて、これらの演算を一括実行する。

attentionだけはrequestごとに過去K/Vの長さが違うため個別に計算し、その後また結果をまとめる。

つまり、**model全体を無理に同じbatch形式へ合わせるのではなく、まとめやすい演算だけをbatch化する**。

### 3. 複数GPUへmodelを分割する

大規模modelではtensor parallelismとpipeline parallelismを組み合わせる。schedulerは各GPUのmemoryとpipelineの実行順も考慮し、341B modelまで評価している。

## 評価

主な環境はAzureのA100 40GB clusterで、GPT 13B / 101B / 175B / 341BをFP16で評価した。baselineはNVIDIA FasterTransformer。

GPT-3 175Bで、1 tokenあたりのlatencyを同程度に揃えた比較では、FasterTransformerの0.185 request/sに対してOrcaは6.81 request/sで、**36.9倍のthroughput**を報告している。

この差の主因は、requestの終了を待たずにbatchの空きへ新しいrequestを入れられることにある。

## 既存研究との差

### 従来の固定batchとの違い

従来方式はbatch全体のgeneration終了まで中身を変えにくい。Orcaは**output tokenを1つ生成するたびにbatchを変更できる**。

### vLLMとの関係

Orcaはbatchを柔軟に組み替えられるようにしたが、KV cacheのmemory割当は後のvLLMほど柔軟ではない。vLLMはOrca型のcontinuous batchingに、KV cacheを固定長blockで必要な分だけ確保する仕組みを加えた。

### FastServeとの関係

FastServeはOrcaのようにtoken生成ごとにschedulerへ戻る仕組みを使い、さらに**実行中requestを一時停止して優先順位を変える**ところまで拡張した。

## 限界

- 評価modelはGPT系列が中心で、現在のGQA / MLAなどは対象外。
- 最大contextは2048 tokenで、現在のlong-context servingとは条件が異なる。
- end-to-end workloadはsynthetic traceで、production traceではない。
- attentionとそれ以外でbatching方法を変えるため、execution engine側の変更が必要。
- 著者による一般公開のOrca実装は確認できない。

## 一般的な実装上の含意

Orcaの重要な点は、LLM servingでは**request全体をschedulerの最小単位にする必要がない**と示したことにある。output tokenを1つ生成する区切りでrequestを入れ替えれば、到着時刻やoutput長が異なるrequestを同じGPUで効率よく混在させられる。

また、すべての演算を同じ方法でbatch化する必要もない。attentionのようにrequestごとの差が大きい演算は個別に扱い、それ以外だけをまとめる設計でも十分な効率を得られる。

## コード

著者による一般公開のOrca実装repositoryは確認できなかった。

## 引用関係

- FastServe、Sarathi-Serve、vLLMなどから基礎研究として引用される。
- 後続研究では、Orcaのcontinuous batchingを土台にKV memory管理、request優先順位、prefill分割などが追加された。

## 一次資料

- OSDI 2022: https://www.usenix.org/conference/osdi22/presentation/yu
- 論文PDF: https://www.usenix.org/system/files/osdi22-yu.pdf

## 更新履歴

- 2026-09-07: 狭い専門用語を減らし、手法の動作が分かる表現へ全面的に整理。
- 2026-09-06: Serving / Scheduling系統の引用探索から追加。