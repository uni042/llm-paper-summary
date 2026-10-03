---
canonical_id: "DOI:10.1145/3777466"
title: "Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines"
authors: ["Michael Davies","Neal Crago","Karthikeyan Sankaralingam","Stephen W. Keckler"]
published: "2025-11-01"
summary: "KitsuneはGPUの通常の一括同期型カーネル実行では、依存演算が時間方向に直列化されSIMT core・Tensor Core・帯域などが交互に遊休する問題に対し、依存する複数カーネルのCTAを同時常駐させる「空間パイプライン」を導入するGPUハードウェア/コンパイラ協調方式である。CUDA風API、資源種別を考慮するgrid scheduler、オンチップproducer-consumer通信、PyTorch Dynamoコンパイラを組み合わせる。5つの深層学習challenge workloadで推論最大2.8倍、学習最大2.2倍、off-chip trafficを推論最大99%・学習最大45%削減する。"
list_summary: "依存GPUカーネルのCTAをSM上へ同時常駐させ、オンチップでproducer-consumer転送する空間パイプラインとPyTorchコンパイラでDL推論の遊休資源とHBM往復を削減する。"
source: "https://doi.org/10.1145/3777466"
worker_completed_at: "2026-10-03T08:06:00+09:00"
worker_run_key: "20261003-0750-scheduled-chat-45"
reference_main_sha: "c6b4225a61c6c358d9faf707386cae9ba8d84ae1"
---

# Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines

## 概要

GPUの深層学習実行は通常、演算子ごとにカーネルを起動し、producerカーネルが完了して中間結果をHBMへ書いた後、consumerカーネルがそれを読み戻す一括同期型で進む。縦方向カーネル融合はこの往復を減らせるが、巨大融合カーネル化するとレジスタ・共有メモリ・スケジューリングが複雑になり、異なる種類の演算資源を柔軟に重ねにくい。

Kitsuneは依存カーネルを1個へ融合する代わりに、複数カーネルの協調スレッド配列（cooperative thread array; CTA）を同じGPUへ同時常駐させ、producerが作ったtileをconsumerへオンチップで渡す「空間パイプライン（spatial pipeline）」を提案する。Tensor Core主体のCTAとSIMT主体のCTAを同時に置き、別々の演算資源を並行利用する。

実現にはCUDA風のpipeline API、資源種別を認識するgrid scheduler、CTA間のオンチップ通信primitive、PyTorch Dynamoからパイプラインを抽出・配置するコンパイラを組み合わせる。5つの深層学習challenge applicationで、推論は最大2.8倍、学習は最大2.2倍高速化し、off-chip trafficをそれぞれ最大99%・45%削減する。

## 問題設定

通常のGPUはカーネル内の多数CTAを空いているSMへ割り当てるが、依存する次カーネルはproducer完了まで開始できない。Tensor Coreを多用するGEMMの実行中にはSIMT資源が余り、要素演算中にはTensor Coreが余るなど、演算子ごとの資源偏りが時間的な遊休を作る。

さらにproducerの出力をHBM/L2へ書き、直後のconsumerが再読出しするため、依存演算間の中間tensorがoff-chip trafficを増やす。batchを大きくすればGPUを埋められる場合もあるが、低遅延推論ではbatch拡大自体が要求遅延と衝突する。

縦方向融合は中間tensorをレジスタ等へ残せるが、複数演算を単一カーネルへ書き換える必要があり、異種演算の資源配分とreduction並列性を同時に扱うのが難しい。Kitsuneはカーネル境界を保ったまま空間的に重ねる。

## 手法

### CUDA空間パイプライン抽象

KitsuneはCUDA Graphに似た形で複数カーネルと依存関係を登録する `cudaPipeline` 型の抽象を置く。ただし意味は「順に起動するgraph」ではなく、「構成カーネルのCTAを同時residentにできるよう協調配置するpipeline」である。

各カーネルには主に使う動的資源がSIMTかTensorかというmetadataを付ける。呼出し側は同時常駐可能なCTA数へ制限し、producer/consumerの依存関係を明示する。これが後段schedulerの配置条件になる。

### 資源種別を考慮するgrid scheduler

通常のgrid schedulerは空きoccupancyを見てCTAを貪欲に割り当てるため、別カーネルのCTAが同じSMへ対になって配置される保証がない。KitsuneはSIMT用とTensor用の二つのarbiterを追加し、異なる資源種別のCTAを同じSMへ組み合わせる。

これによりproducerとconsumerを時間分割せず、片方がTensor Coreを使う間にもう片方がSIMT core等を使える。変更は完全な新GPUアーキテクチャではなく、既存occupancy情報を使うgrid schedulerへの比較的小さい拡張として設計される。

### オンチップproducer-consumer通信

空間パイプラインではproducerがtileを作り終えた時点でconsumer CTAへ渡し、全producerカーネル完了を待たない。中間データをHBMへ往復させず、L2/共有経路や同期primitiveを用いてtile単位で流す。

このデータフロー実行により、カーネル間のglobal barrierを細粒度依存へ置き換え、off-chip trafficを削減する。同時にreduction次元をpipeline並列性へ利用できるため、batchだけに依存せずGPU並列性を増やせる。

### PyTorch Dynamoコンパイラ

アプリケーション側へ手書きpipelineを要求しないため、KitsuneはPyTorch 2.0 Dynamoでforward/backward graphを抽出する。コンパイラは候補subgraphを選び、pipeline patternとcost modelから構成を決め、整数線形計画でCTA数・資源割当を選ぶ。

最終的に各pipeline nodeのCTAをSMへ割り当て、提案primitiveを使うコードへ落とす。ハードウェアprimitiveだけでなく、どの演算列を空間化するかをcompiler backendが決める点がシステム全体の一部である。

## 評価条件

|項目|内容|
|---|---|
|対象|深層学習の推論・学習、5 challenge applications|
|実行系|PyTorch DynamoベースのKitsune compiler|
|比較概念|通常bulk-synchronous GPU実行、縦方向融合等|
|主資源|SIMT core、Tensor Core、SM occupancy、off-chip memory traffic|
|評価|性能倍率、off-chip traffic削減|
|性質|実GPUの現行機能だけでなく、提案grid-scheduler/API拡張を含むhardware-software co-design|

## 主要結果

|条件|結果|読み取れること|
|---|---:|---|
|推論challenge workload|最大2.8倍高速化|依存演算の空間重畳が低利用資源を埋める|
|学習challenge workload|最大2.2倍高速化|forwardだけでなくbackward graphにも適用可能|
|推論off-chip traffic|最大99%削減|中間tensorのHBM往復をほぼ除去できる構成がある|
|学習off-chip traffic|最大45%削減|より複雑な状態保持でもtraffic削減が残る|
|初期preprintの範囲|推論1.3〜2.3倍、学習1.1〜2.4倍|workloadごとに利得幅が大きい|

## 既存研究との差

CUDA streamsによる並行カーネル実行は独立カーネルを重ねられるが、依存producer/consumerを同一SMへ資源補完的に配置する保証がない。縦方向融合は依存を消せるが、複数演算を巨大カーネルへ統合し、compilerとkernel実装の複雑性を増す。

Kitsuneはカーネル単位のプログラム構造を保ちつつ、CTA粒度で依存演算を空間配置する。そのため「融合して1カーネルにする」と「別カーネルとして時間順に流す」の中間に、細粒度dataflow実行を追加する。

## 限界

Kitsuneは現行CUDAソフトウェアだけで完全実現する方式ではなく、CUDA APIとGPU grid schedulerへの変更を含む。したがって論文の速度値を現在の市販GPUへライブラリを導入するだけで再現できるわけではない。

また最大2.8倍・99%削減は5 challenge workloadの最良条件で、全演算列に共通する値ではない。producerとconsumerの資源利用が補完的で、tile依存をオンチップで流せる場合ほど有利であり、同じ資源を奪い合う演算や同時常駐できない巨大CTAでは利得が小さくなる。

本サーベイの観点ではLLM専用システムではなく汎用DL GPU実行基盤である。そのためLLM固有のKVキャッシュ、MoEルーティング、オンラインサービングSLOは直接評価していない。推論カーネル実行モデルとしての関連性を中心に読む必要がある。

## 一次資料

- https://doi.org/10.1145/3777466