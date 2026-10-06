---
canonical_id: "arXiv:2602.22603"
title: "SideQuest: Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning"
summary: "SideQuestは長期agentでtool出力がcontextを占有する問題に対し、reasoning model自身へ補助threadでtokenの将来有用性を判断させ、不要になったtool由来KVをevictする。215 traceで学習したgpt-oss-20bによりpeak tokenを最大65%削減し、SGLang/H100実測ではthroughputを828から1523 token/sへ84%改善する。"
list_summary: "主reasoningと並列の補助threadでLLM自身に古いtool 文脈の寿命を判断させ、意味的に不要なKVを追い出しして長期agentのキャッシュを縮小する。"
authors: ["Sanjay Kariyappa","G. Edward Suh"]
published: "2026-02-26"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2602.22603"
sources: ["https://arxiv.org/abs/2602.22603"]
implementation: "gpt-oss-20bを215 traceでfine-tuneし、FRAMES/BrowseCompで評価。SGLangとNVIDIA H100でserving throughput・KV使用量・runtimeを実測。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2602.22603"
arxiv_categories: {primary: "cs.AI", cross_list: ["cs.LG"]}
worker_completed_at: "2026-10-06T10:56:00+09:00"
worker_run_key: "20261006-1030-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
長期のweb browsingやdeep researchでは、検索結果やwebpage本文など外部検索由来トークンが文脈の大半を占める。従来のKV 枝刈りは注意機構 スコア等のheuristicで重要度を推定するが、多段reasoningでは「今は参照されないが後で必要になる情報」と「役目を終えたtool出力」を区別できず、圧縮率を上げるとタスク成功率が崩れやすい。

SideQuestはLarge Reasoning Model自身の意味理解をメモリ managerとして使う。主reasoningとは別の補助タスクとして「どのtool出力がもう不要か」を判断させ、その判断トークンを主文脈へ混ぜずにKVを追い出しする。

## 手法
学習dataではbase policyのagent trajectoryから各tool 出力が最後に使われた位置を求め、より強いannotation モデルに「なぜこの情報は以後不要か」のreasoningを生成させる。main トレースには元policyを壊さないためのlogit distillationを使い、auxiliary トレースにはメモリ-management タスクのcross-entropy lossを使う。

推論時には主threadが通常のagent reasoningを続ける一方、補助threadが文脈中のtool出力を評価する。補助タスクのトークンは主KVへ残さないため、メモリ管理の説明自体が文脈 pollutionを増やさない。不要と判断された領域のKVを削除し、その後のデコードで読むキャッシュ量を減らす。

## 評価条件
|項目|条件|
|---|---|
|モデル|fine-tuned gpt-oss-20b|
|学習data|215 high-quality トレース|
|ベンチマーク|FRAMES 424 samples、BrowseComp 500 samples|
|推論提供|SGLang、NVIDIA H100|
|比較|非圧縮、H2O、SnapKV、R-KV等|
|指標|accuracy、peak トークン、KV read、スループット、総ランタイム|

## 主要結果
peak トークン utilizationを56–65%、KV キャッシュ メモリ readを53–71%削減し、in-分布でaccuracy低下約2%、out-of-分布で約5%に抑える。類似圧縮率のheuristic 比較対象ではaccuracy低下とunparsable response増加が大きい。

SGLang/H100の実推論提供ではスループットが828から1523 トークン/sへ83.9%増加し、peak KV usageを53.9%、ベンチマーク総ランタイムを36.8%削減する。キャッシュ容量だけでなく実時間へ効果が変換された点が重要である。

## 既存研究との差
注意機構 スコアや位置heuristicではなく、モデル自身がtool情報の意味的寿命をreasoningする。メモリ管理を主reasoningに直接書き込まず並列 auxiliary threadへ分離することで、管理処理による文脈汚染を避ける。

## 限界
215 トレースで有効性を示す一方、学習したメモリ judgmentが異なるagent/tool domainへ一般化する保証はない。誤追い出しは後続reasoningで回復不能になり得る。補助threadにも計算コストがあり、KV削減が小さい短タスクでは利得が縮む。