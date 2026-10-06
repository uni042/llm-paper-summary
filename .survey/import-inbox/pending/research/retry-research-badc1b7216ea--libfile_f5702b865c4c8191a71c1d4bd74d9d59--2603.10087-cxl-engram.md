---
canonical_id: "arXiv:2603.10087"
title: "Pooling Engram Conditional Memory in Large Language Models using CXL"
summary: "本研究はLLMの静的知識を巨大embedding tableへ分離するEngram conditional memoryを、Compute Express Link（CXL）memory poolへoffloadする。疎で細粒度なlookupに対してRDMAより低遅延なload/store accessを使い、prefetchを組み合わせてSGLangへ統合し、local DRAMに近いend-to-end推論性能でEngram容量をhost外へ拡張する。"
list_summary: "疎なEngram embedding lookupをCXL共有メモリへオフロードし、プリフェッチとSGLang統合で局所 DRAM近傍の性能を保ちながらLLMの条件付きメモリ容量を拡張する。"
authors: ["Ruiyang Ma","Teng Ma","Zhiyuan Su","Hantian Zha","Xinpeng Zhao","Xuchun Shang","Xingrui Yi","Zheng Liu","Zhu Cao","An Wu","Zhichong Dou","Ziqian Liu","Daikang Kuang","Guojie Luo"]
published: "2026-03-10"
publication: "arXiv preprint; submitted to EuroMLSys 2026"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2603.10087"
sources: ["https://arxiv.org/abs/2603.10087"]
implementation: "CXL memory poolへEngram tableを配置し、SGLangの推論pathへ統合。local DRAM、CXL、RDMA系配置を比較してend-to-end性能を評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2603.10087"
arxiv_categories: {primary: "cs.AR", cross_list: ["cs.DC"]}
worker_completed_at: "2026-10-06T13:56:00+09:00"
worker_run_key: "20261006-1330-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
Engram conditional メモリは、LLMが毎トークン同じ密 FFNで全知識を計算する代わりに、静的な知識を巨大embedding tableへ置き、入力に対応する少数entryだけをlookupする。計算量は抑えられる一方、table容量が大きくなるとGPU/ホスト DRAMへ常駐できない。本論文はこのtableをCompute Express Link（CXL）で接続した共有メモリ プールへ置く。

## 問題設定
Engram アクセスは連続した大ブロック転送ではなく、トークンに応じた少数entryへの細粒度・疎アクセスになる。このpatternではRDMAのようなネットワーク越しbulk transferはsoftware/ネットワーク オーバーヘッドが相対的に大きい。一方CXL メモリはCPUの読み込み/store address spaceとして扱え、remote メモリながら細粒度アクセスを低オーバーヘッドで発行できる。

## 手法
Engram embedding tableをCXL プールへ移し、LLM本体の密 重みとは別メモリ 階層として管理する。inference時に必要なentryだけをCXLから取得するため、Engram容量をGPU/ホスト DRAM容量から切り離せる。複数ホストからプールを共有できれば、各ノードへ同じ巨大tableを複製する必要も減る。

アクセス 遅延をそのままcritical pathへ置かないため、Engramの予測可能なアクセスを利用してプリフェッチする。現在の計算と次entry取得を重ね、CXLの追加遅延を隠す。SGLangへ統合することでマイクロベンチマークだけでなく実際のLLM generation pathで評価する。

## 評価条件
|項目|内容|
|---|---|
|対象|Engram conditional メモリ付きLLM|
|メモリ|局所 DRAM、CXL メモリ プール、RDMA系remote アクセス|
|ランタイム|SGLang統合|
|アクセス|疎・細粒度embedding lookup|
|指標|lookup 遅延、エンドツーエンド inference performance、メモリ scalability|

## 主要結果
CXL配置はRDMAよりEngramの細粒度アクセスへ適し、プリフェッチを組み合わせたSGLang統合では局所 DRAMに近いエンドツーエンド性能を達成する。主な価値は「GPUを速くする」より、巨大な条件付きメモリを低階層へ逃がしてもgeneration critical pathを大きく悪化させない点にある。

## 既存研究との差
一般的なLLM オフロードは密 層 重みやKV キャッシュをCPU/SSDへ移すが、本研究はアクセス sparsityの高いEngram tableに対象を限定する。そのため全重みを毎トークン転送する方式と違い、CXLの細粒度読み込み/store特性を活かしやすい。

## 限界
Engramを持たない通常Transformerへそのまま適用するメモリ拡張ではない。CXL ハードウェアとメモリ プール構成が必要で、プリフェッチが外れるアクセス patternではremote 遅延が露出する。評価はEngram lookupの特性を前提としており、密 重み オフロードやKV オフロードの性能を代表しない。