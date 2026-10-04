---
canonical_id: "arXiv:2608.15299"
title: "MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation"
summary: "MAPLEは、全layerで同じ数のexpertを起動するMoE推論に対し、layerごとのexpert数感度を測り、global routed-expert budgetをheterogeneousに再配分する。感度重み付き閉形式allocationを初期解とし、sensitivity-constrained genetic searchでrefineする。4種MoEの75% expert budgetでpruning・uniform baselineを上回り、DeepSeek-MoE-16BではSGLang単一A6000のlatencyを2.860秒から1.940秒へ32.2%削減しthroughputを47.4%改善した。"
list_summary: "layerごとのexpert数感度を測ってglobal expert budgetを再配分し、重み変更なし・再学習なしでMoEのactive computationを減らすplug-and-play方式。"
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
---

# MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation

## 概要

疎活性化MoEは通常、全layerで同じtop-k expert数を使う。しかしlayerごとの冗長性は均一ではなく、expertを1個減らしただけで精度が崩れるlayerと、複数減らしてもほとんど影響しないlayerがある。globalな計算budgetだけを決めて一律にkを下げると、この異質性を無視する。

MAPLEは各layerだけexpert数を変えたときのvalidation accuracyを測り、layer sensitivityを作る。感度が高いlayerには元のexpert数に近い容量を残し、低感度layerへ削減を集中する。重みの枝刈りや再学習は行わず、pretrained MoEのrouting時にlayer別kを使うplug-and-play方式である。

初期allocationは感度重み付き最小二乗問題の閉形式解で求め、その後10 candidate×10 generationのgenetic searchでrefineする。4 modelを75% routed-expert budgetで評価し、DeepSeek-MoE-16Bではfull-budget uniformよりARC-E、ARC-C、BoolQがそれぞれ65.09→71.40、48.49→51.50、80.03→82.38へ改善した。SGLang単一GPUではlatency 32.2%減、throughput 47.4%増を実測する。

## 問題設定

MoEの総parameter数ではなく1 tokenが実行するexpert数を減らせばFFN計算量を減らせるが、一律削減はsensitive layerまで同じ割合で削る。逆に全layerへ元のkを残すと、redundant layerへ不要な計算を払う。

MAPLEはmodel size圧縮ではない。全expert weightを保持したまま、layerごとのactive expert数だけ変える。このためVRAM footprintは基本的に残るが、routing後のexpert computationとdispatch/reductionを削れる条件ではlatencyを下げられる。

## 手法

### layer sensitivity probing

各layerについて他layerを固定し、そのlayerのactive expert数だけ1から元のkまで変えてvalidation accuracyを測る。各layerについて最良expert数と、expert数変化に対するaccuracy rangeを得る。rangeが大きいlayerをsensitive、小さいlayerをredundantとみなす。

論文はaccuracy rangeのほかweight variance、異なるexpert数でのoutput deviationも比較する。実task accuracyを使うrangeが最も安定し、genetic refinementでも少ないgenerationで高い結果へ到達したためdefaultになる。

### 閉形式budget allocation

各layerをそのlayer固有のpreferred expert数から離すpenaltyをsensitivityで重み付けし、全layerのexpert総数がglobal budgetに一致するよう配分する。感度が高いlayerほどpreferred countからの逸脱penaltyが大きくなり、budget不足分は低感度layerへ多く割り当てられる。

この解は探索の初期値であり、headline accuracyを単独で生むわけではない。DeepSeek-MoE-16BのARC-Eでは閉形式初期解64.39からgenetic refinement後71.40まで7.01 point伸びるため、refinementの寄与は大きい。

### sensitivity-constrained genetic refinement

初期allocationから10 candidateを作り10 generation探索する。global budgetと各layerの上下限を守りつつ、sensitive layerのmutationを小さく、redundant layerを大きく動かす。validation accuracyを直接fitnessに使い、上位2 eliteを保持する。

k=1となったlayerではrouter argmaxで1 expertだけを実行し、multi-expert dispatch、weighted combination、reductionを省く専用pathを使う。vLLM版ではこのk=1 pathのfused CUDA kernelも評価している。

## 評価条件

|項目|条件|
|---|---|
|GPU|NVIDIA RTX A6000 48 GB|
|budget|元のrouted-expert総数の75%|
|model|DeepSeek-MoE-16B、DeepSeek-V2-Lite、OLMoE-1B-7B、Moonlight-16B-A3B|
|task|ARC-C、ARC-E、BoolQ、PIQA、RTE、追加でGSM8K/BBH|
|serving|SGLang 0.4.6、vLLM|
|配置|single GPU、2-GPU pipeline parallel、2-GPU expert parallel|
|search|10 candidates × 10 generations|
|測定|serving latency / throughputは5 run平均|

## 主要結果

|条件|指標|比較|MAPLE|読み取れること|
|---|---|---|---|---|
|DeepSeek-MoE-16B, 75% budget|平均accuracy|full uniform 71.71 / LExI 69.45|74.34|active expert削減でもfull baselineを上回る|
|同, ARC-E|accuracy|full 65.09|71.40|+6.31 point|
|同, ARC-C|accuracy|full 48.49|51.50|+3.01 point|
|同, BoolQ|accuracy|full 80.03|82.38|+2.35 point|
|Moonlight, 75%|平均accuracy|full 78.36|77.74|他75%方式には勝つがfullには0.62 point負ける|
|SGLang single A6000|latency|full 2.860 s|1.940 s|32.2%削減|
|同|throughput|full uniform|+47.4%|active compute削減が単一GPUで効く|
|SGLang 2 GPU|speed gain|full|3.9〜5.2%|通信・同期が残り利得縮小|
|vLLM single GPU|speed gain|full|4.58%|runtime/kernel構成に依存|
|offline calibration, DeepSeek-MoE-16B|GPU-hours|—|7.39 h|plug-and-playでも事前探索費用は必要|

## 既存研究との差

SparseGPT、Wanda、MoNE等のpruning系はweight/expert構造を削るのに対し、MAPLEは全weightを保持してrouting時のlayer別kだけを変える。LExIもheterogeneous expert allocationを行うが、synthetic inputとweight statisticsを使うのに対し、MAPLEはtask validationに対するexpert-count sensitivityを直接測る。

uniform 75%方式との違いは「何個削るか」ではなく「どのlayerから削るか」である。したがって同じglobal active-expert budgetでもaccuracyと実行時間が変わる。

## 限界

全expert weightを保持するためmodel footprintそのものは縮まらない。単一GPU SGLangでは大きな利得がある一方、2-GPUでは3.9〜5.2%、vLLM single-GPUでは4.58%まで縮む。通信、同期、kernel launchなどexpert FFN以外が支配するとactive expert削減の効果は薄まる。

またallocation決定にtask validation dataとoffline calibrationが必要で、DeepSeek-MoE-16Bでは5 task合計7.39 GPU-hoursを要する。Moonlightでは75% MAPLEがfull baselineを0.62 point下回り、expert削減が常にfull-budget品質を上回るわけでもない。

## 一次資料

- https://arxiv.org/abs/2608.15299