---
canonical_id: "arXiv:2608.15299"
title: "MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation"
summary: "MAPLEは、全layerで同じ数のexpertを起動するMoE推論に対し、layerごとのexpert数感度を測り、global routed-expert budgetをheterogeneousに再配分する。感度重み付き閉形式allocationを初期解とし、sensitivity-constrained genetic searchでrefineする。4種MoEの75% expert budgetでpruning・uniform baselineを上回り、DeepSeek-MoE-16BではSGLang単一A6000のlatencyを2.860秒から1.940秒へ32.2%削減しthroughputを47.4%改善した。"
list_summary: "層ごとの専門家数感度を測って大域 専門家 budgetを再配分し、重み変更なし・再学習なしでMoEの活性 computationを減らすplug-and-play方式。"
authors:
  - Lie Li
  - Wen Li
  - Junxiao Shen
  - Gusheng Hu
published: "2026-08"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2608.15299"
sources:
  - "https://arxiv.org/abs/2608.15299"
implementation: "DeepSeek-MoE-16B等4種MoEへ重み変更なしで適用し、SGLang 0.4.6とvLLMで実測する。確認済み一次資料から公式repository URLは特定できなかった。"
code: null
last_checked: "2026-10-04"
arxiv_id: "2608.15299"
arxiv_categories:
  primary: "cs.LG"
  cross_list: []
worker_completed_at: "2026-10-04T09:58:00+09:00"
worker_run_key: "20261004-0930-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---

# MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation

## 概要

疎活性化MoEは通常、全層で同じtop-k 専門家数を使う。しかし層ごとの冗長性は均一ではなく、専門家を1個減らしただけで精度が崩れる層と、複数減らしてもほとんど影響しない層がある。大域な計算budgetだけを決めて一律にkを下げると、この異質性を無視する。

MAPLEは各層だけ専門家数を変えたときのvalidation accuracyを測り、層 sensitivityを作る。感度が高い層には元の専門家数に近い容量を残し、低感度層へ削減を集中する。重みの枝刈りや再学習は行わず、pretrained MoEのルーティング時に層別kを使うplug-and-play方式である。

初期allocationは感度重み付き最小二乗問題の閉形式解で求め、その後10 candidate×10 generationのgenetic searchでrefineする。4 モデルを75% routed-専門家 budgetで評価し、DeepSeek-MoE-16Bでは全体-budget uniformよりARC-E、ARC-C、BoolQがそれぞれ65.09→71.40、48.49→51.50、80.03→82.38へ改善した。SGLang単一GPUでは遅延 32.2%減、スループット 47.4%増を実測する。

## 問題設定

MoEの総パラメータ数ではなく1 トークンが実行する専門家数を減らせばFFN計算量を減らせるが、一律削減はsensitive 層まで同じ割合で削る。逆に全層へ元のkを残すと、redundant 層へ不要な計算を払う。

MAPLEはモデル サイズ圧縮ではない。全専門家 重みを保持したまま、層ごとの活性 専門家数だけ変える。このためVRAM footprintは基本的に残るが、ルーティング後の専門家 computationと分配/reductionを削れる条件では遅延を下げられる。

## 手法

### layer sensitivity probing

各層について他層を固定し、その層の活性 専門家数だけ1から元のkまで変えてvalidation accuracyを測る。各層について最良専門家数と、専門家数変化に対するaccuracy rangeを得る。rangeが大きい層をsensitive、小さい層をredundantとみなす。

論文はaccuracy rangeのほか重み 分散、異なる専門家数での出力 deviationも比較する。実タスク accuracyを使うrangeが最も安定し、genetic refinementでも少ないgenerationで高い結果へ到達したためdefaultになる。

### 閉形式budget allocation

各層をその層固有のpreferred 専門家数から離すpenaltyをsensitivityで重み付けし、全層の専門家総数が大域 budgetに一致するよう配分する。感度が高い層ほどpreferred countからの逸脱penaltyが大きくなり、budget不足分は低感度層へ多く割り当てられる。

この解は探索の初期値であり、headline accuracyを単独で生むわけではない。DeepSeek-MoE-16BのARC-Eでは閉形式初期解64.39からgenetic refinement後71.40まで7.01 point伸びるため、refinementの寄与は大きい。

### sensitivity-constrained genetic refinement

初期allocationから10 candidateを作り10 generation探索する。大域 budgetと各層の上下限を守りつつ、sensitive 層のmutationを小さく、redundant 層を大きく動かす。validation accuracyを直接fitnessに使い、上位2 eliteを保持する。

k=1となった層ではルータ argmaxで1 専門家だけを実行し、multi-専門家 分配、weighted combination、reductionを省く専用pathを使う。vLLM版ではこのk=1 pathのfused CUDA カーネルも評価している。

## 評価条件

|項目|条件|
|---|---|
|GPU|NVIDIA RTX A6000 48 GB|
|budget|元のrouted-専門家総数の75%|
|モデル|DeepSeek-MoE-16B、DeepSeek-V2-Lite、OLMoE-1B-7B、Moonlight-16B-A3B|
|タスク|ARC-C、ARC-E、BoolQ、PIQA、RTE、追加でGSM8K/BBH|
|推論提供|SGLang 0.4.6、vLLM|
|配置|single GPU、2-GPU パイプライン 並列、2-GPU 専門家 並列|
|search|10 candidates × 10 generations|
|測定|推論提供 遅延 / スループットは5 試行平均|

## 主要結果

|条件|指標|比較|MAPLE|読み取れること|
|---|---|---|---|---|
|DeepSeek-MoE-16B, 75% budget|平均accuracy|全体 uniform 71.71 / LExI 69.45|74.34|活性 専門家削減でも全体 比較対象を上回る|
|同, ARC-E|accuracy|全体 65.09|71.40|+6.31 point|
|同, ARC-C|accuracy|全体 48.49|51.50|+3.01 point|
|同, BoolQ|accuracy|全体 80.03|82.38|+2.35 point|
|Moonlight, 75%|平均accuracy|全体 78.36|77.74|他75%方式には勝つが全体には0.62 point負ける|
|SGLang single A6000|遅延|全体 2.860 s|1.940 s|32.2%削減|
|同|スループット|全体 uniform|+47.4%|活性 compute削減が単一GPUで効く|
|SGLang 2 GPU|speed gain|全体|3.9〜5.2%|通信・同期が残り利得縮小|
|vLLM single GPU|speed gain|全体|4.58%|ランタイム/カーネル構成に依存|
|offline calibration, DeepSeek-MoE-16B|GPU-hours|—|7.39 h|plug-and-playでも事前探索費用は必要|

## 既存研究との差

SparseGPT、Wanda、MoNE等の枝刈り系は重み/専門家構造を削るのに対し、MAPLEは全重みを保持してルーティング時の層別kだけを変える。LExIもheterogeneous 専門家 allocationを行うが、合成 入力と重み statisticsを使うのに対し、MAPLEはタスク validationに対する専門家-count sensitivityを直接測る。

uniform 75%方式との違いは「何個削るか」ではなく「どの層から削るか」である。したがって同じ大域 活性-専門家 budgetでもaccuracyと実行時間が変わる。

## 限界

全専門家 重みを保持するためモデル footprintそのものは縮まらない。単一GPU SGLangでは大きな利得がある一方、2-GPUでは3.9〜5.2%、vLLM single-GPUでは4.58%まで縮む。通信、同期、カーネル 起動など専門家 FFN以外が支配すると活性 専門家削減の効果は薄まる。

またallocation決定にタスク validation dataとoffline calibrationが必要で、DeepSeek-MoE-16Bでは5 タスク合計7.39 GPU-hoursを要する。Moonlightでは75% MAPLEが全体 比較対象を0.62 point下回り、専門家削減が常に全体-budget品質を上回るわけでもない。

## 一次資料

- https://arxiv.org/abs/2608.15299