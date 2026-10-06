---
canonical_id: "arXiv:2608.01662"
title: "LongCat Sparse Attention: Taming the Lightning via Streaming-aware Hierarchical Cross-Layer Indexing"
summary: "LongCat Sparse Attention（LSA）はDeepSeek Sparse AttentionのLightning Indexerが持つO(L^2) scoringと散在KVによる非連続HBM accessを、Streaming-Aware、Cross-Layer、Hierarchicalの3種indexingで削減する。69B-A3B～560B-A27Bでfull attention相当の品質を保ち、最大1M tokenのnative trainingを可能にする。"
list_summary: "疎注意機構のindexer計算と散在KV アクセスを、連続ストリーム領域・層間index再利用・粗密二段検索で同時に削減するハードウェア-aware sparse 注意機構。"
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
last_audited: null
audit_version: 0
---
## 概要
動的疎注意機構は各問い合わせが見るKV トークンをK個へ絞れば本体注意機構をO(KL)へ減らせるが、候補を選ぶindexer自身が全接頭辞をスコアすると系列全体ではO(L^2)が残る。さらに選ばれたKVがHBM上で散在すると、理論FLOPsを減らしてもメモリ transactionがまとまらない。LSAはこの「index選択コスト」と「選択後のハードウェア アクセス」の両方を対象にする。

## 手法
Streaming-Aware Indexing（ストリーミング対応indexing）は、注意機構 sinkと直近sliding windowのように高確率で必要なトークンを固定の連続領域として注意機構 budgetへ予約する。残りだけを動的sparse indexerで選ぶため、選択トークンのおよそ半分を連続HBM アクセスへ変換できる。Hybrid Sparse Attention カーネルは連続windowと動的sparse 分岐を別ストリームで処理し、online softmaxで結果を統合する。

Cross-Layer Indexing（層間index再利用）は、ある層で得た選択indexを連続する複数層へ共有する。層ごとにO(L^2) indexerを回す回数を減らし、cross-層 distillationで共有先層の注意機構分布とのずれを抑える。

Hierarchical Indexing（階層indexing）は全トークンを一度に精密スコアせず、page等の粗い単位で候補を絞ってからトークン単位へ降りるcoarse-to-fine方式を使う。文脈が100万トークン級になったときindexerが注意機構本体を上回る問題を抑える。

## 評価条件
|項目|内容|
|---|---|
|モデル|LongCat系 69B-A3B～560B-A27B|
|比較|全体 注意機構、DeepSeek Sparse Attention系|
|文脈|最大1M トークンのnative 学習|
|実装|Hybrid Sparse Attention カーネル|
|品質|general-purpose / long-文脈 ベンチマーク|

## 主要結果
69B-A3Bから560B-A27Bまで、一般タスクとlong-文脈 タスクで全体 注意機構と同等水準の品質を維持する。従来indexerは1024K トークンで層 遅延の90%以上を占め得るが、LSAはindex計算の共有・階層化とHBM アクセス連続化を組み合わせてこのシステム ボトルネックを削る。

公開モデル LongCat-Flash-Lite-Sparse 69B-A3BはLSAを組み込み、1M-トークン 文脈をnativeに扱う。さらにLSAはLongCat-2.0 1.6T-A48Bの長文脈機構にも用いられる。

## 既存研究との差・限界
DeepSeek Sparse Attentionのように「重要トークンを選ぶ」だけでなく、indexer自体の計算量と選択後のメモリ layoutまで共同設計する。固定ストリーム領域の比率やcross-層共有が合わない注意機構 patternでは品質/効率の交換が変わる。cross-層 distillationを含むため既存チェックポイントへ完全学習不要で差し替える方式ではなく、HBM layoutと専用カーネルへの依存もある。