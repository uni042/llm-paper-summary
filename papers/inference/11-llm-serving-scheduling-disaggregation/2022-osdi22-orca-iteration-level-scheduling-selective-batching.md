---
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "Orca: A Distributed Serving System for Transformer-Based Generative Models"
summary: "output tokenを1つ生成するたびにbatchを組み替え、長さや進行位置が異なるrequestを途中からbatchへ出し入れできるようにした分散LLM serving system。"
authors_affiliations: "Gyeong-In Yu, Joo Seong Jeong（Seoul National University）; Geon-Woo Kim（FriendliAI / Seoul National University）; Soojeong Kim（FriendliAI）; Byung-Gon Chun（FriendliAI / Seoul National University）"
published: "2022-07-11"
publication_status: "OSDI 2022"
lineage: "LLM Serving / Scheduling / Disaggregation"
topics: ["Continuous batching","Selective batching","Distributed inference","Tensor parallelism","Pipeline parallelism"]
importance: "高"
hardware_evaluation: "実機"
canonical_id: "DOI:10.5555/3600237.3600268"
doi: "10.5555/3600237.3600268"
last_audited: "2026-09-08"
audit_version: 1
evaluation_type: "real-hardware"
implementation_status: "code-unavailable"
source: "https://www.usenix.org/conference/osdi22/presentation/yu"
code: ""
last_checked: "2026-09-08"
---

# Orca: A Distributed Serving System for Transformer-Based Generative Models

> output tokenを1つ生成するたびにbatchを組み替え、長さや進行位置が異なるrequestを途中からbatchへ出し入れできるようにした分散LLM serving system。

## 概要

従来のinference serverでは、一度batchを作ると、そのbatch内のrequestがすべて終了するまで中身を変えない方式が一般的だった。しかしLLMの生成ではrequestごとにoutput長が異なるため、短いrequestが終わっても長いrequestを待つことになり、その間に新しく来たrequestも参加できない。

Orcaは、**request全体ではなく「output tokenを1つ生成する処理」を1回の単位としてschedulerへ戻す**。1 token生成するたびに終了したrequestを外し、新着requestを加えられるため、batchを継続的に組み替えられる。現在一般的なcontinuous batchingの基礎になった考え方である。

ただし途中からbatchへ入ったrequestはsequence長が揃わない。そこでOrcaは、attentionだけrequestごとに処理し、LinearやLayerNormなどは全requestのtokenをまとめて計算する。論文ではこの方法を **selective batching** と呼ぶ。

## 問題設定

LLM生成は1 tokenごとにmodel全体を繰り返し実行するため、本来はtoken生成の間にrequestを入れ替えられる。ところがrequest単位でbatchを固定すると、短いrequestが終わってもGPU枠が空かず、新着requestも待たされる。

## 手法

### 1. 1 token生成ごとにbatchを見直す

1回のmodel実行後にschedulerへ制御を戻し、終了requestを除き、新着requestを追加して次iterationを組む。

### 2. attention以外はまとめて計算する

sequence長が異なってもLinear、LayerNorm、GeLUなどはtokenをまとめて処理できるため一括実行し、attentionだけrequestごとの過去K/V長に合わせて個別処理する。

### 3. 複数GPUへmodelを分割する

大規模modelではtensor parallelismとpipeline parallelismを組み合わせ、341B modelまで評価している。

## 評価

主な環境はAzureのA100 40GB clusterで、GPT 13B / 101B / 175B / 341BをFP16で評価した。baselineはNVIDIA FasterTransformer。

GPT-3 175Bで同程度のlatency条件に揃えた比較では、FasterTransformerに対して**36.9倍のthroughput**を報告している。

## 既存研究との差

Orcaはbatchをrequest単位で固定せずiteration単位へ細粒度化し、sequence長が異なるrequestをselective batchingで同居させる。後続のvLLMはこのcontinuous batchingをKV cacheのpaged memory管理と組み合わせ、FastServeはさらに実行中requestのpreemptionを加えた。

## 限界

- 評価modelはGPT系列が中心で、現在のGQA / MLAなどは対象外。
- 最大contextは2048 tokenで、現在のlong-context servingとは条件が異なる。
- production traceではなくsynthetic workload中心。
- 著者による一般公開のOrca実装は確認できない。

## 一般的な実装上の含意

LLM servingではrequest全体をschedulerの最小単位にする必要はなく、token generation iterationの境界でrequestを入れ替えることでoutput長のばらつきを吸収できる。また、全operatorを同じbatch形状へ押し込まず、attentionだけ個別処理する設計でも高い利用率を得られる。

## 一次資料

- OSDI 2022: https://www.usenix.org/conference/osdi22/presentation/yu
- 論文PDF: https://www.usenix.org/system/files/osdi22-yu.pdf

## 更新履歴

- 2026-09-08: 正式監査。OSDI 2022書誌、canonical DOI、主要性能値、実機評価、公開code状況を確認し監査metadataを追加。本文の実質内容は変更なし。
- 2026-09-07: 狭い専門用語を減らし、手法の動作が分かる表現へ全面的に整理。
- 2026-09-06: Serving / Scheduling系統の引用探索から追加。
