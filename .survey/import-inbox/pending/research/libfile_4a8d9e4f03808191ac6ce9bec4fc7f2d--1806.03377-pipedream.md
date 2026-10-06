---
canonical_id: "DOI:10.1145/3341301.3359646"
title: "PipeDream: Generalized Pipeline Parallelism for DNN Training"
summary: "PipeDreamはDNN layerを複数GPUへ計算量と通信量を考慮して分割し、異なるmini-batchのforward/backwardを1F1B型に重ねるpipeline parallel training systemである。parameter versioningにより非同期pipelineでもforwardとbackwardのweight整合を保ち、data parallel比で通信量を最大95%削減し、5モデル・2クラスタの評価でtime-to-accuracyを最大5倍短縮する。"
list_summary: "層分割、forward/backwardのpipeline重畳、weight versioningを組み合わせ、通信律速の分散DNN学習でGPU idleと通信量を削減する。"
authors: ["Aaron Harlap","Deepak Narayanan","Amar Phanishayee","Vivek Seshadri","Nikhil Devanur","Greg Ganger","Phil Gibbons"]
published: "2018-06-08"
publication: "SOSP 2019"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/1806.03377"
sources: ["https://arxiv.org/abs/1806.03377"]
implementation: "複数GPU・複数machine上のpipeline parallel DNN training systemとして実装し、5種類のDNNと2種類のclusterでdata parallel trainingと比較。確認済み一次資料から公式code URLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "1806.03377"
arxiv_categories:
  primary: "cs.DC"
  cross_list: []
worker_completed_at: "2026-10-06T18:18:00+09:00"
worker_run_key: "20261006-1800-scheduled-chat-00/r01"
reference_main_sha: "f5213871027dd0aa06635e6ff813a108d30ea80d"
---

## 概要

データ並列（data parallelism）は各GPUへmodel全体を複製し、mini-batchを分けてgradientを同期する。modelが大きい、あるいはnetworkが遅いとgradient同期が計算時間を上回り、GPUが通信待ちになる。PipeDreamはmodelのlayerを複数stageへ分け、異なるmini-batchのforwardとbackwardをpipelineとして重ねることで、modelを分割しながらGPUを連続稼働させる。

単純なpipeline trainingでは、forwardとbackwardの間に他mini-batchのparameter updateが入り、同じsampleが異なるweight versionを見る問題がある。PipeDreamはweight versioningを導入し、forward時に使ったversionを対応するbackwardでも使う。さらにprofile結果からlayer partitionを決め、通信量とstage計算時間を均衡させる。大規模DNNではdata parallel比で通信を最大95%削減し、5 model・2 clusterでtime-to-target-accuracyを最大5倍短縮する。

## 問題設定

data parallel trainingではGPU数を増やすほどgradient collectiveが増え、model parameterが大きい場合はnetwork bandwidthが律速になる。model parallelismならweightを分割できるが、layerを単純に直列stageへ分けるだけでは1 mini-batchの処理中に他stageがidleになる「pipeline bubble」が大きい。

GPipe型の同期pipelineは複数micro-batchでbubbleを埋められるが、1 batch分のforwardを流してからbackwardを流すためactivation保持量が増え、update間隔も長くなる。PipeDreamはforwardとbackwardを細粒度に交互実行してsteady stateの利用率を上げる。

## 手法

### Profile-based partitioning

各layerのforward/backward計算時間、parameter量、activation transfer量をprofileし、連続layerをpipeline stageへ割り当てる。目的はstage間の処理時間を均しつつ、境界を跨ぐ通信を減らすことにある。必要なら1 stageをdata-parallel replica化し、遅いstageのthroughputを上げる。

### 1F1B scheduling

pipelineが満たされた後、各stageはforward 1件とbackward 1件を交互に処理する。異なるmini-batchが同時に異なるstageへ存在するため、単一batchのlayer依存を待つ時間を別batchの計算で埋める。通信も隣接stage間のactivation/gradient転送が中心になり、全weight gradientを全GPUへ同期するdata parallelより通信量を抑えられる。

### Weight stashing

非同期に複数mini-batchが流れると、あるmini-batchのforward後に別batchのbackward/updateでweightが変わる。PipeDreamはforward時のparameter versionをstashし、同じmini-batchのbackwardで対応versionを使う。これによりforward/backwardの局所的一貫性を保つ。

### Vertical synchronization

完全同期SGDと同じ更新系列ではなくpipeline由来のstalenessが残るため、PipeDreamはpipeline内のversion進行を制御する。time-to-accuracy評価を採用し、単なるsamples/sだけでなく、stalenessを含めて目標精度へ到達するまでの実時間で比較する。

## 評価条件

| 項目 | 内容 |
|---|---|
| workload | 5種類のDNN |
| hardware | 2種類のmulti-GPU cluster |
| 比較 | data-parallel training等 |
| 主指標 | time-to-target-accuracy、通信量、GPU utilization |
| 分割 | layer profileに基づくpipeline stage |
| scheduling | forward/backwardを重ねるpipeline |

## 主要結果

大きいDNNではdata parallelに比べ通信量を最大95%削減する。pipeline stage間のactivation/gradientだけを主に送るため、model全parameterのgradient同期がnetworkを占有する条件ほど差が大きい。

5種類のDNNを2 clusterで評価し、time-to-accuracyはdata parallel比で最大5倍高速化する。これはraw throughputだけではなく、parameter stalenessが収束へ与える影響も含んだ指標である。networkが十分高速でdata parallelの同期が小さい場合や、layer分割が不均衡になるmodelでは利得は縮む。

## 既存研究との差

通常のmodel parallelismは1 mini-batchをlayer順に流すためGPU idleが大きい。同期型pipelineはmicro-batchでbubbleを減らすが、activation memoryや同期点が残る。PipeDreamは異なるmini-batchのforward/backwardを継続的に重ね、weight stashingで非同期pipelineの整合性問題を処理する。

## 限界

pipelineはstage間の最遅stageでthroughputが決まるため、layerを均等に分割できないmodelでは利用率が落ちる。weight versionを複数保持する追加memoryも必要になる。評価は現在のLLM以前のDNNが中心で、Transformerの巨大sequence、ZeRO/FSDP、現代の高速interconnectと組み合わせた結果を直接示すものではない。

## 一次資料

- https://arxiv.org/abs/1806.03377