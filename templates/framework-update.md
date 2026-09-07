# YYYY-MM-DD — 更新名

> 一文で「何が変わり、どの計算・copy・通信・memory使用量・待ち時間を減らす変更か」を説明する。PR固有のclass名・pass名・kernel名だけで説明を終えない。

## 記述ルール

狭いframework / hardware固有語を使う場合は、最初に日本語で意味を説明し、必要なら正式英語名を括弧内に残す。

例:

- 「GPU kernel間の依存起動をCPU往復なしで進める仕組み（Programmatic Dependent Launch; PDL）」
- 「GPUの仮想addressとphysical pageを分離してmemory断片化を抑える仮想memory管理（Virtual Memory Management; VMM）」
- 「CPU / GPUが同じbacking memoryを参照してcopyを省くzero-copy」

## 概要

- 変更前は何がbottleneckだったか
- 変更後はdata / compute flowがどう変わるか
- 対象がprefill、decode、training、MoE、KV cache、offload等のどこか

を数文でまとめる。

## 変更された仕組み

固有名を列挙するだけでなく、変更前と変更後でdataや計算がどう流れるかを書く。

必要なら、

`変更前: ... → ... → ...`

`変更後: ... → ...`

のように示す。

## 対象hardware / workload

- GPU / CPU / accelerator
- single-GPU / multi-GPU / multi-node
- prefill / decode / concurrent serving / training
- model / precision / context length

など、性能値を一般化するために必要な条件を書く。

## 性能結果

数値だけでなく、改善が何の待ち時間・転送・計算削減によるものかを書く。

以下を区別する。

- kernel microbenchmark と end-to-end throughput / latency
- TTFT / TPOT / ITL / training step time
- theoretical improvement と 実測
- 単一request と concurrent serving

独立benchmarkがない場合は「公式性能値なし」と明記し、機能追加だけからspeedupを推測しない。

## 既存方式との差

同じ目的の既存pathがある場合、

- 何を置き換えたか
- 互換fallbackがあるか
- 新しいtrade-offが何か

を書く。

## 状態

- PR / release:
- status: Released / Merged / Open / Draft / Closed
- first observed:
- last checked:

**Open / Draft PRの性能値を正式releaseの性能として扱わない。** 状態が変わった場合は新しい重複項目を作るより既存記録を更新する。

## 一次資料

- 公式release / PR / documentationを優先する。
