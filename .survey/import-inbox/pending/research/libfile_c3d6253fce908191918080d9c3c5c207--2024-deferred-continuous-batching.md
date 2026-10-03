---
canonical_id: "DOI:10.1145/3642970.3655835"
title: "Deferred Continuous Batching in Resource-Efficient Large Language Model Serving"
authors: ["Yongjun He", "Yao Lu", "Gustavo Alonso"]
published: "2024-04-22"
summary: "FineInferはGPU資源が限られた環境でLLM推論とLoRA等のパラメータ効率fine-tuningを同居させる際、job切替のモデル再ロードや待ち行列が長くなる問題を扱う。遅延連続バッチ（deferred continuous batching）は推論要求の遅延余裕を追跡し、余裕があるiterationだけfine-tuning batchを混ぜる。さらにbase model multiplexingと異種batchingで同じ層の重み読出しを推論・学習間で共有し、状態/KVをtask別に管理する。評価ではfine-tuning遅延を最大3倍改善し、モデルがGPUメモリを超える条件では最大50倍改善しつつ推論SLAを守る。"
list_summary: "推論要求の遅延余裕に応じてfine-tuning iterationを差し込む遅延連続バッチと重み共有型異種batchingにより、限られたGPUで推論SLAを守りつつfine-tuningを高速化する。"
source: "https://doi.org/10.1145/3642970.3655835"
worker_completed_at: "2026-10-03T05:58:00+09:00"
worker_run_key: "20261003-0545-scheduled-chat-45"
reference_main_sha: "e7d11a1ba6865891d8156766cef11ea559fddc97"
---

# Deferred Continuous Batching in Resource-Efficient Large Language Model Serving

## 概要
オンプレミスなどGPU台数が少ない環境では、同じbase LLMに対する推論とLoRA等のパラメータ効率fine-tuningが同時に到着する。別々に実行すると新jobを待たせるか、既存jobを停止してモデルを入れ替える必要があり、特にモデルがGPUメモリへ収まらずCPU-GPU間で層を移動する場合は切替費が非常に大きい。

FineInferはbase modelを共有したまま推論とfine-tuningを同居させる。中心となる遅延連続バッチ（deferred continuous batching）は、各推論要求が許容できる遅延余裕を監視し、その余裕内だけfine-tuning iterationを挿入する。さらに異種batchingで同じTransformer層の重みを一度ロードした際に推論forwardとfine-tuning forward/backwardへ使う。

評価では従来のjob切替/待機方式に対してfine-tuning遅延を最大3倍改善し、モデルがGPUメモリを超えるCPU-GPU実行では最大50倍の改善を報告する。推論側は設定した遅延境界を守ることを優先する。

## 問題設定
推論は自己回帰的に短いiterationを繰り返し、fine-tuningはforward/backwardとoptimizer状態を必要とする。単純な時間分割ではfine-tuning iterationが長いため、推論要求がその間待たされSLAを破りやすい。

一方、推論を常に優先すると到着率が高いとfine-tuningが飢餓状態になる。モデルがGPUに収まらない場合は、jobごとに同じbase weightをCPUから再転送すること自体が主要費用になる。

## 手法
### 遅延連続バッチ
schedulerは推論queue Q_i、fine-tuning queue Q_f、推論1 iteration推定時間t_i、fine-tuning iteration推定時間t_fを持つ。各推論要求rについて到着からの遅延d_rと許容遅延bound d_rbを追跡する。

次のfine-tuning iterationを入れた場合に d_r + t_f - t_i がboundへ達する要求があれば、そのiterationは推論専用にする。余裕があればfine-tuning batchを取り出して異種modeを実行する。これにより固定比率ではなく、現在の推論待ち時間からfine-tuningを延期・実行する。

### base model multiplexing
推論adapterとfine-tuning adapterは同じbase modelを共有する。特にGPUメモリを超えるモデルではTransformer層を順にCPUからGPUへ読み、同じ層がresidentな間に両taskの計算を進める。

この構造により「推論用にbase weightを読む」「fine-tuning用にもう一度同じweightを読む」という転送をまとめる。モデルoffload条件ほどデータ移動削減の価値が大きく、最大50倍という結果もこの領域で現れる。

### 異種batchingと状態分離
推論入力とfine-tuning sampleを同じ層実行へまとめるが、中間状態を無差別に共有しない。fine-tuningにはoptimizer stateとactivation、推論にはKV cacheが必要で、両方を全sampleへ持つとメモリが爆発する。

論文のLlama2-7B例では、rank-8 LoRA + AdamW、batch 4、長さ256のfine-tuningに追加3.14GB、推論batch相当にはKV約0.5GBが必要で、単純異種batchingを32系列へ広げると追加116.48GB相当になる。FineInferはtaskごとに必要状態だけを保持し、iteration/request境界で不要状態を解放する。

## 評価条件
|項目|内容|
|---|---|
|用途|同一base LLMの推論 + パラメータ効率fine-tuning同時実行|
|代表方式|LoRA系adapter、AdamW|
|資源条件|GPU内に収まる場合と、CPU-GPU offloadが必要な場合|
|比較|job切替・queueingを行う既存運用|
|指標|fine-tuning完了遅延、推論SLA、データ移動/メモリ|
|代表状態例|Llama2-7B FP16、rank-8 LoRA、batch 4、sample長256|

## 主要結果
|条件|結果|意味|
|---|---:|---|
|一般的な資源制約条件|fine-tuning遅延 最大3倍改善|推論の隙間へtraining iterationを入れる効果|
|モデル > GPU memory|最大50倍改善|base weight再転送の共有効果が支配的|
|Llama2-7B状態例|fine-tuning 3.14GB + 推論KV 0.5GB|異種taskの状態要求が異なる|
|単純32系列異種batch例|追加116.48GB相当|状態分離なしでは同居が非現実的|

## 既存研究との差
通常の連続バッチは自己回帰推論要求同士をiteration境界で入れ替え、空いたslotへ新要求を入れる。FineInferは異種のfine-tuning iterationまで候補にし、推論要求の残り遅延予算に基づいて挿入可否を決める。

LoRA multi-tenant servingは複数adapterの推論を同一base modelで共有するが、backward/optimizerを伴うfine-tuningとの同時実行は扱いが異なる。FineInferはbase weight共有とtask別状態管理を組み合わせる。

## 限界
主な価値は推論とfine-tuningを同じ限られた資源へ載せる環境にあり、推論専用大規模clusterでは目的が異なる。最大50倍はモデルがGPU容量を超えてweight転送が支配する条件で、GPU内に全weightが常駐する条件へ一般化できない。

fine-tuningを挿入できる量は推論到着率と遅延boundに依存する。高負荷で推論余裕がなくなればfine-tuningは延期され、学習throughputが低下する。また評価は2024年時点の研究prototypeで、最新サービングruntimeへの統合性能は別途確認が必要である。

## 一次資料
- https://doi.org/10.1145/3642970.3655835
- https://www.research-collection.ethz.ch/server/api/core/bitstreams/eb66706a-ee39-4e2a-b958-4de5e3b3291a/content