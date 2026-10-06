---
canonical_id: "arXiv:2412.18547"
title: "Token-Budget-Aware LLM Reasoning"
summary: "TALEは問題難度に応じたreasoning token budgetを選び、Chain-of-Thoughtの冗長生成を削る。推論時にbudgetを推定するTALE-EPは平均token使用量67%削減・accuracy低下3%未満、post-training版TALE-PTはtokenを約50%削減する。"
list_summary: "問題ごとに適切な推論トークン予算を推定またはpost-学習で内在化し、CoTの過剰生成を抑えてデコード トークン・API費用を削減する。"
authors: ["Tingxu Han","Zhenting Wang","Chunrong Fang","Shiyu Zhao","Shiqing Ma","Zhenyu Chen"]
published: "2024-12-24"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2412.18547"
sources: ["https://arxiv.org/abs/2412.18547"]
implementation: "GPT-4o/mini、Yi-lightning、o3-mini、Llama-3.1-8B-Instruct等でTALE-EP/PTを評価。公式コード公開。"
code: "https://github.com/GeniusHTX/TALE"
last_checked: "2026-10-06"
arxiv_id: "2412.18547"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.AI","cs.LG"]}
worker_completed_at: "2026-10-06T09:53:00+09:00"
worker_run_key: "20261006-0930-scheduled-chat-30/r02"
last_audited: null
audit_version: 0
---
## 概要
Chain-of-Thought（CoT）は正答率を上げる一方、簡単な問題にも長いreasoningを生成してデコード トークンと料金を増やす。TALEは「短くしすぎると逆に制約を守れずトークンが増える」というトークン elasticityを観測し、問題ごとに無理のないbudgetを選ぶ。

## 手法
推論時方式TALE-EP（estimation and prompting）は、別のbudget estimatorへ問題を見せて必要reasoning長をzero-shot推定し、そのbudgetを解答プロンプトへ入れる。全問題へ固定上限を課さず、算術と大学レベル問題で異なるbudgetを割り当てる。

TALE-PTはofflineで各問題の適切なbudgetを探索し、そのbudget下で正答した短いreasoningをdataset化する。その後、教師あり微調整（SFT）または直接選好最適化（DPO）とLoRAで、明示budgetなしでも短く考える性質をbase モデルへ内在化する。offline searchはGSM8K 7473問でA100約354分の一回限りの費用を要する。

## 評価条件
|項目|条件|
|---|---|
|モデル|GPT-4o、GPT-4o-mini、Yi-lightning、o3-mini、Llama-3.1-8B-Instruct|
|タスク|GSM8K、GSM8K-Zero、MathBench、追加生成タスク|
|比較|Direct Answer、vanilla CoT|
|指標|accuracy、出力 トークン、API expense|

## 主要結果
TALE-EPは総括で出力 トークンを平均67%削減し、accuracy低下を3%未満に抑える。GPT-4o-mini中心の表ではvanilla CoT平均461.25 トークン・83.75% accuracyに対しTALE-EPは148.72 トークン・81.03%、費用は289.78から118.46（10^-5ドル/標本）へ下がる。

モデル横断MathBench-Collegeでは出力 トークンを平均64.63%、expenseを45.30%削減する。TALE-PTはvanilla CoT比でトークンを約50%削減し、GSM8KのLlama-3.1-8BではSFT版が241.51→139.63 トークンへ減らしつつaccuracyを77.56→78.57%へ上げる。

## 負の結果・限界
budgetを小さくしすぎるとトークン elasticityによりかえって制約遵守が崩れる。TALE-EPはestimator call自体の費用があり、小型モデルではaccuracy低下が大きくなりやすい。TALE-PTは推論時の追加estimatorを不要にする代わり、offline budget searchとpost-学習を要求する。