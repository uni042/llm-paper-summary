---
canonical_id: "arXiv:2607.09153"
title: "KV-PRM: Efficient Process Reward Modeling via KV-Cache Transfer for Multi-Agent Test-Time Scaling"
summary: "KV-PRMはagent生成時に既に作られたKV cacheをprocess reward modelへ直接渡し、全trajectory textの再encodeを1個のverify token readoutへ置換する。scoring complexityをO(L^2)からO(L)へ下げ、Qwen3 0.6B/4B/8Bで最大約5000倍のFLOPs削減、37倍のlatency削減、34.2倍のper-sequence memory削減を報告する。"
list_summary: "multi-agent reasoningの生成KVをreward モデルへ直接転送し、trajectory再encodeを避けてtest-time scalingの検証コストを大幅に削減する。"
authors: ["Peng Kuang","Haibo Jin","Xiaoyu Han","Yanli Wang","Xiaopeng Yuan","Ye Yu","Kaidi Xu","Haohan Wang"]
published: "2026-07-10"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.09153"
sources: ["https://arxiv.org/abs/2607.09153"]
implementation: "Qwen3-0.6B/4B/8BをMATH、GSM8K、AIME等で評価し、NVIDIA GH200 120GB上でscoring latency/memoryを実測。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.09153"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.AI"]}
worker_completed_at: "2026-10-06T11:41:00+09:00"
worker_run_key: "20261006-1130-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
多エージェント（multi-agent）推論のtest-time scalingでは、beam searchやMCTSが途中trajectoryを何度も過程報酬モデル（Process Reward Model; PRM）へ渡す。通常のテキスト PRMは、そのたびに同じ長いtrajectoryを先頭から再encodeする。KV-PRMは生成agentが既に計算したキー・バリューキャッシュ（KV キャッシュ）をPRMへ転送し、再encodeを省く。

## 問題設定
長さLのtrajectoryをテキスト PRMが毎回注意機構でencodeするとscoring計算がO(L^2)に増える。探索分岐数も増えるtest-time scalingでは、reward モデルが本体生成より大きなボトルネックになり得る。

## 手法
KV-PRMはagentの生成KVを入力状態として受け取り、その後ろに単一のverify トークンを追加する。このトークンの隠れ 状態だけからrewardを読むため、既存trajectoryの全トークンを再計算しない。追加注意機構は既存KVを一度読むだけなのでscoring complexityはO(L)になる。

著者はKV表現が離散テキストより多い情報を保持し得ることを形式化し、読み出し トークン数kを増やしたときの近似gapが指数的に縮む一方、限界利得も減ることを示す。実用設計ではk=1を中心にする。

## 評価条件
|項目|条件|
|---|---|
|モデル|Qwen3 0.6B / 4B / 8B|
|タスク|MATH、GSM8K、AIME等|
|探索|Beam Search、MCTS、Weighted Voting|
|GPU|NVIDIA GH200 120GB|
|指標|accuracy、scoring FLOPs、遅延、per-系列 メモリ|

## 主要結果
テキスト PRMと同等以上のタスク性能を保ちながら、典型的trajectoryでscoring FLOPsを最大約5000倍削減する。実時間では15～37倍高速で、8B・4096 トークンでは1 scoring callがText-PRM 172.0msに対しKV-PRM 4.6msである。

per-系列 メモリ増分は最大34.2倍小さくなる。これにより同一GPUで探索分岐を増やしやすい。単なる理論FLOPsだけでなくGH200上の遅延へ利得が変換されている。

## 既存研究との差・限界
既存PRMが生成済みテキストを再入力するのに対し、生成時の内部状態を別モデルへ引き渡す。これはKV キャッシュを単なる注意機構高速化用メモリではなく、下流 verifierへの中間表現として再利用する点が特徴である。agentとPRM間で互換なKV表現が必要で、異種構成/API越しの一般的なキャッシュ transferは自明ではない。