---
canonical_id: "arXiv:2607.23765"
title: "WISERouter: LLM Routing with Workload Budget Constraint"
summary: "WISERouterはLLM routingをworkload全体の予算制約付きcontextual multi-armed banditとして定式化し、queryごとの固定budgetではなく高価なmodelを使う場所をworkload内で配分する。offline版は履歴interactionだけで学習でき、online版はO(sqrt(T)) regretを持ち、RouterBenchとSWE-Benchで固定予算を守りながら既存routingより高いutilityを示す。"
list_summary: "LLM選択をワークロード全体の予算制約付きbanditとして扱い、問い合わせ間で費用を融通しながら品質と総コストを最適化するルータ。"
authors: ["Yifei Li","Zihui Gao","Laks V. S. Lakshmanan"]
published: "2026-07-26"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.23765"
sources: ["https://arxiv.org/abs/2607.23765"]
implementation: "RouterBenchとSWE-Benchでoffline/online routingを評価。denseなquery-model全組合せ教師を要求せず、historical interactionまたはonline explorationを利用。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.23765"
arxiv_categories: {primary: "cs.LG", cross_list: []}
worker_completed_at: "2026-10-06T12:45:00+09:00"
worker_run_key: "20261006-1230-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
複数LLMから問い合わせごとにモデルを選ぶルーティングでは、高性能モデルほど高価というtrade-offを扱う。既存方式には、heuristicで総budgetを厳密に守れないものと、各問い合わせへ同じ固定budgetを課して簡単な問い合わせで余った予算を難しい問い合わせへ回せないものがある。WISERouterはbudgetを個々の問い合わせではなくワークロード全体へ課す。

## 手法
各問い合わせの特徴を文脈、モデル選択をarm、品質をreward、利用料金等をコストとする制約付き文脈バンディット（constrained contextual multi-armed bandit）として定式化する。制約は時間区間全体の累積コストへ課されるため、ルータは簡単な問い合わせに安価なモデルを使い、価値の高い問い合わせへ高価なモデルを割り当てられる。

WR-Offlineは過去に実際に選ばれたモデルと観測reward/コストから学習し、全問い合わせ×全モデルの密 ラベルを必要としない。WR-Onlineは運用中にexplorationを行って不確実性を減らしながらbudget constraintを追跡する。理論上、時間長Tに対してO(√T)のsublinear regretを示す。

## 評価条件
|項目|条件|
|---|---|
|ベンチマーク|RouterBench、SWE-Bench|
|方式|WR-Offline、WR-Online|
|比較|既存LLM ルータ、固定per-問い合わせ budget方式|
|制約|ワークロード-level cumulative budget|
|指標|タスク utility、budget adherence、exploration data量|

## 主要結果
WR-Offlineは固定総budget下で既存比較対象より高いperformanceを示し、budget constraintへの追従も改善する。WR-Onlineは比較対象と同等水準のperformanceへ、より少ないexploration dataで到達する。

重要なのは「常に安いモデルを選ぶ」ことではなく、問い合わせ間で予算を再配分できる点である。同じ平均コストでも、難しい問い合わせへ高性能モデルを集中できるため固定per-問い合わせ budgetよりutilityを上げられる。

## 既存研究との差・限界
supervised ルータのように全問い合わせ-モデル pairの結果を収集せず、logged interactionから学べる。online版は探索を必要とするため、初期運用では一部問い合わせへsuboptimal モデルを選ぶコストがある。品質rewardと金銭コストが観測可能であることを前提とし、モデル 遅延や容量 constraintを同時に扱うproduction スケジューラそのものではない。