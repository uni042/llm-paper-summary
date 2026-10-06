---
canonical_id: "arXiv:2608.01662"
title: "LongCat Sparse Attention: Taming the Lightning via Streaming-aware Hierarchical Cross-Layer Indexing"
summary: "LongCat Sparse Attention（LSA）はDeepSeek Sparse AttentionのLightning Indexerが持つO(L^2) scoringと散在KVによる非連続HBM accessを、Streaming-Aware、Cross-Layer、Hierarchicalの3種indexingで削減する。69B-A3B～560B-A27Bでfull attention相当の品質を保ち、最大1M tokenのnative trainingを可能にする。"
list_summary: "疎attentionのindexer計算と散在KV accessを、連続stream領域・layer間index再利用・粗密二段検索で同時に削減するhardware-aware sparse attention。"
authors: ["Wen Zan","Jiaqi Zhang","Jianchao Tan","Hong Liu","Cunguang Wang","Xiang Li","Duyue Ma","Guanyu Wu","Yifan Lu","Fengcun Li","Yerui Sun","Peng Pei","Yuchen Xie","Xunliang Cai"]
published: "2026-08-03"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2608.01662"
sources: ["https://arxiv.org/abs/2608.01662"]
implementation: "69B-A3Bから560B-A27Bまでscale評価し、Hybrid Sparse Attention kernelを実装。LongCat-Flash-Lite-Sparse 69B-A3Bを公開。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2608.01662"
arxiv_categories: {primary: "cs.AI", cross_list: ["cs.CL","cs.DC","cs.LG"]}
worker_completed_at: "2026-10-06T14:02:00+09:00"
worker_run_key: "20261006-1330-scheduled-chat-30/r02"
---
## 概要
動的疎attentionは各queryが見るKV tokenをK個へ絞れば本体attentionをO(KL)へ減らせるが、候補を選ぶindexer自身が全prefixをscoreすると系列全体ではO(L^2)が残る。さらに選ばれたKVがHBM上で散在すると、理論FLOPsを減らしてもmemory transactionがまとまらない。LSAはこの「index選択cost」と「選択後のhardware access」の両方を対象にする。

## 手法
Streaming-Aware Indexing（ストリーミング対応indexing）は、attention sinkと直近sliding windowのように高確率で必要なtokenを固定の連続領域としてattention budgetへ予約する。残りだけを動的sparse indexerで選ぶため、選択tokenのおよそ半分を連続HBM accessへ変換できる。Hybrid Sparse Attention kernelは連続windowと動的sparse branchを別streamで処理し、online softmaxで結果を統合する。

Cross-Layer Indexing（層間index再利用）は、あるlayerで得た選択indexを連続する複数layerへ共有する。layerごとにO(L^2) indexerを回す回数を減らし、cross-layer distillationで共有先layerのattention分布とのずれを抑える。

Hierarchical Indexing（階層indexing）は全tokenを一度に精密scoreせず、page等の粗い単位で候補を絞ってからtoken単位へ降りるcoarse-to-fine方式を使う。contextが100万token級になったときindexerがattention本体を上回る問題を抑える。

## 評価条件
|項目|内容|
|---|---|
|model|LongCat系 69B-A3B～560B-A27B|
|比較|full attention、DeepSeek Sparse Attention系|
|context|最大1M tokenのnative training|
|実装|Hybrid Sparse Attention kernel|
|品質|general-purpose / long-context benchmark|

## 主要結果
69B-A3Bから560B-A27Bまで、一般taskとlong-context taskでfull attentionと同等水準の品質を維持する。従来indexerは1024K tokenでlayer latencyの90%以上を占め得るが、LSAはindex計算の共有・階層化とHBM access連続化を組み合わせてこのsystem bottleneckを削る。

公開model LongCat-Flash-Lite-Sparse 69B-A3BはLSAを組み込み、1M-token contextをnativeに扱う。さらにLSAはLongCat-2.0 1.6T-A48Bの長文脈機構にも用いられる。

## 既存研究との差・限界
DeepSeek Sparse Attentionのように「重要tokenを選ぶ」だけでなく、indexer自体の計算量と選択後のmemory layoutまで共同設計する。固定stream領域の比率やcross-layer共有が合わないattention patternでは品質/効率の交換が変わる。cross-layer distillationを含むため既存checkpointへ完全training-freeで差し替える方式ではなく、HBM layoutと専用kernelへの依存もある。