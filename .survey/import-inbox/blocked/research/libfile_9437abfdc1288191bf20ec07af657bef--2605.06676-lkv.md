---
canonical_id: "arXiv:2605.06676"
title: "LKV: End-to-End Learning of Head-wise Budgets and Token Selection for LLM KV Cache Eviction"
summary: "LKVはKV cache evictionをend-to-end differentiableにし、LKV-Hでattention headごとの保持budget、LKV-Tでattention matrixをmaterializeせずtoken重要度を学習する。LongBenchでは15% KV retentionでもnear-lossless性能を示し、ablationからtoken selectorよりhead-wise budget学習が品質維持の主要因であることを示す。"
list_summary: "KV 追い出しのヘッド別budgetとトークン重要度をタスク 目的関数からエンドツーエンド学習し、固定heuristic配分を置き換えて15% retentionでも長文脈品質を保つ。"
authors: ["Enshuai Zhou","Yifan Hao","Chao Wang","Rui Zhang","Di Huang","Jiaming Guo","Xing Hu","Zidong Du","Qi Guo","Yunji Chen"]
published: "2026-04-22"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2605.06676"
sources: ["https://arxiv.org/abs/2605.06676"]
implementation: "LongBenchとRULERで高圧縮KV evictionを評価。LKV-H/LKV-Tを既存LLMへ付加してhead-wise budgetとtoken selectionを学習。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2605.06676"
arxiv_categories: {primary: "cs.LG", cross_list: ["cs.CL"]}
worker_completed_at: "2026-10-06T16:57:00+09:00"
worker_run_key: "20261006-1630-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
長文脈ではKV キャッシュがトークン数に比例して増え、同時リクエスト数を制約する。従来の追い出しはヘッドごとのbudgetを固定統計やheuristicで決め、トークン selectionも注意機構 スコア、sink、recency等の代理指標へ依存する。LKVは「どのヘッドへ何トークン残すか」と「どのトークンを残すか」をタスク lossから直接学習する。

## 問題設定
注意機構 ヘッドは役割が異なり、検索型ヘッドと局所型ヘッドへ同じKV budgetを与えるのは非効率である。手作業budgetはモデル/タスクが変わると最適でなくなる。また注意機構 matrixをimportance算出のためにmaterializeするとFlashAttention系のメモリ効率を壊す。

## 手法
LKV-Hは全体KV budgetをヘッドごとへ配るlearnable budgeting moduleである。離散的な保持数を直接最適化せず、differentiableな割当表現を通してタスク 目的関数から「どのヘッドへ容量を寄せるか」を学ぶ。

LKV-Tはトークン側のimportanceをkey/value自身の内在表現から求め、全体 注意機構 matrixを保存せずselectionする。ヘッド budgetとトークン スコアを同じエンドツーエンド 目的関数で共同学習するため、budget heuristicとselection heuristicの独立調整を避ける。

推論時は学習済みヘッド budgetに従って各ヘッドのKVを追い出しする。タスク 目的関数へ直接alignしたbudgetなので、uniform budgetや手作りヘッド classより圧縮時の重要ヘッド破壊を減らす。

## 評価条件
|項目|内容|
|---|---|
|ベンチマーク|LongBench、RULER|
|比較|既存KV 追い出し/compression heuristic|
|圧縮|15% retentionを含む高圧縮率|
|構成|LKV-H ヘッド budget + LKV-T トークン selection|
|指標|long-文脈 タスク accuracy、retention ratio、ablation|

## 主要結果
LongBenchではKV キャッシュを15%だけ保持する条件でもnear-無損失性能を報告し、RULERでも高圧縮率で状態-of-the-art水準を示す。

ablationではLKV-Tのトークン selection改善より、LKV-Hによるヘッド-wise budget学習の寄与が支配的である。これはKV圧縮で「どのトークンか」だけでなく「どのヘッドへメモリを配るか」が主要な品質要因であることを示す。

## 既存研究との差
H2O、StreamingLLM、SnapKV等のheuristic selectionは固定のimportance ruleを使う。LKVはbudget allocation自体をタスク 目的関数へ組み込み、selectionと共同学習する。また注意機構 matrix materializationを避けるためmodern fused 注意機構 pathと両立しやすい。

## 限界
学習不要ではなく、対象モデル/タスク分布で追加学習が必要である。15% retentionのnear-無損失性はベンチマーク条件に依存し、未知タスクで同じ保証はない。learned budgetが分布 shiftにどこまでrobustかはdeployment時の再評価が必要である。