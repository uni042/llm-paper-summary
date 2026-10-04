---
canonical_id: "DOI:10.1145/3821219"
title: "AdaptiveKV: Accelerating KV Cache Offloading with a Bandwidth-Adaptive Memory Allocation Mechanism"
summary: "AdaptiveKVはGPU HBMからホストへKVキャッシュを退避する際、DDRとCXLメモリの実効帯域がGPU負荷・NUMA配置・退避規模で変動する問題を扱う。GPU memory conch model、実行時の最適配分率予測器、NUMA node間dynamic interleavingを組み合わせ、固定tieringより帯域を使い切る。既存方式比でLLM inference throughputを最大1.90倍へ改善し、CXL/DDR帯域比8%超が少なくとも5%高速化を得る境界と報告する。"
list_summary: "DDR/CXLの実効帯域を実行時予測し、KVページの階層・NUMA配分を動的変更してオフロード帯域を最大化する。"
authors: ["Yibo Tang","Lizhou Wu","Yang Ou","Sunfeng Gao","Yanjing Wang","Zicong Wang","Xingyun Qi","Jiaqing Xu","Fangxu Lv","Liquan Xiao","Mingche Lai"]
published: "2026-07-10"
publication: "ACM Transactions on Architecture and Code Optimization"
publication_type: "journal"
publication_status: "published"
source: "https://doi.org/10.1145/3821219"
sources: ["https://doi.org/10.1145/3821219"]
implementation: "実CXL/DDR環境のGPU memory bandwidth profilingに基づくallocation predictorとNUMA page interleavingを実装し、さらに性能可変なFPGA CXL memory emulatorで適用境界を評価。一次資料から公式コードURLは確認できなかった。"
code: null
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T08:43:00+09:00"
worker_run_key: "20261004-0800-scheduled-chat-00/r01"
last_audited: null
audit_version: 0
---
# AdaptiveKV: Accelerating KV Cache Offloading with a Bandwidth-Adaptive Memory Allocation Mechanism

## 概要
長文脈・大バッチのLLM推論ではKVキャッシュがGPU HBMを圧迫するため、古いKVをCPU側メモリへ退避する方式が使われる。しかし複数GPUが同時にホスト DDRを読むと帯域が競合し、KVをHBMから追い出せてもデコードがホスト 帯域待ちになる。Compute Express Link（CXL）メモリを追加すれば容量と帯域を増やせるが、CXLは常にDDRより速いわけではなく、device特性、read/write比、GPU負荷、NUMA配置で実効帯域が変わる。

AdaptiveKVは「DDR優先」「CXL優先」の固定方針ではなく、現在のオフロード規模と各メモリ 階層の帯域からKV pageの配分率を実行時に選ぶ。GPU メモリ conch モデルで複数階層を同時利用したときの帯域形状を表し、軽量predictorが最適な割合を推定し、動的 interleavingがNUMA ノードへpageを実際に配置する。既存の状態-of-the-art メモリ 戦略比で推論スループットを最大1.90倍にし、CXL-to-DDR 帯域 ratioが8%を超えると少なくとも5%の高速化が得られる境界をFPGA emulatorで示す。

## 問題設定
KV オフロードでは容量だけでなく「次の注意機構までに必要KVをどれだけ速く読めるか」が重要になる。ホスト DDRへ一括配置すると複数GPUが同じメモリ controllerを競合し、CXLへ一括配置するとCXL リンクやdevice側帯域が律速になる。OSの一般的なinterleaveはページ数を均等化しても、各階層の実効帯域比が等しいとは限らない。

さらにGPUからのメモリ アクセスはCPU ベンチマークと異なる通信量を作るため、CPU側の静的NUMA policyだけでは最適配分を予測しにくい。AdaptiveKVはGPU ワークロードでCXL-HBM/DDR経路をプロファイリングし、KV オフロード専用の帯域指向allocationとして扱う。

## 手法

### GPU memory conch model
プロファイリングでは、DDRとCXLへ割り当てるpage比率を変えると総帯域が単調に片方へ寄るのではなく、複数経路を並行利用することで最大値を持つ「conch」形状が現れる。この形をGPU数、KV規模、メモリ特性ごとにモデル化し、単純な容量比ではなく帯域最大点をallocation 対象にする。

このモデルにより、CXLがDDRより単体帯域で劣る場合でも、一部通信量をCXLへ逃がしてDDR controller競合を減らせば総帯域が上がる条件を捉える。

### 実行時配分率予測
全配分率を毎リクエスト総当たりするとプロファイリング オーバーヘッドが大きいため、ランタイム predictorが現在のオフロード条件から最適なDDR/CXL allocation ratioを推定する。入力条件が変わればratioも更新し、multi-GPU負荷やKV量の変動へ追従する。

予測値はpage 配置の目標比率となり、単に「CXLを追加メモリとして使う」だけでなく、利用する帯域を能動的に調整する点が特徴である。

### 動的NUMA interleaving
予測した割合を実際のメモリ pageへ反映するため、available NUMA ノード間でKV pageを動的interleaveする。各ノードへ均等round-robinするのではなく、予測された帯域比に応じた重み付き配置を行うことで、複数メモリ controllerとCXL pathを並行に使う。

KV内容や注意機構計算は変更しないため、品質を近似で交換する方式ではない。追加費用はプロファイリング、predictor、page 配置管理であり、速度利得はメモリ 帯域がデコード律速になっている条件で大きい。

## 評価条件
|項目|条件|
|---|---|
|対象|LLM KV キャッシュ ホスト オフロード|
|メモリ|ホスト DDR + CXL メモリ プール|
|負荷|GPU/multi-GPU inference、複数オフロード規模|
|追加評価|性能可変FPGA CXL メモリ emulator|
|比較|固定/既存メモリ allocation 戦略|
|指標|実効メモリ 帯域、LLM inference スループット|

## 主要結果
|条件|結果|意味|
|---|---:|---|
|既存状態-of-the-art 戦略比|最大1.90倍スループット|階層間帯域配分の最適化が実推論へ反映|
|CXL/DDR 帯域 ratio > 8%|少なくとも5%推論高速化|低速CXLでも一定帯域以上ならDDR競合分散に価値がある|
|multi-階層同時利用|固定一方配置より高い総帯域|容量ではなくaggregate 帯域を最適化すべきことを支持|

FPGA emulatorでCXL性能を変えた実験は、特定deviceだけの結果ではなく「どの程度のCXLなら導入価値が出るか」を境界として示す役割を持つ。8%という値は論文の評価構成での境界であり、すべての基盤に普遍的な閾値ではない。

## 既存研究との差
従来のKV オフロードはGPU/CPU間の転送量、プリフェッチ、追い出しを主に最適化する。CXL tiering研究も容量 expansionを重視することが多い。AdaptiveKVはGPUがホスト メモリを読む際の実効帯域曲線を直接測り、DDRとCXLのページ配分率をランタイムで変える点が中心である。KVを圧縮・削除するのではなく、同じKVをどのメモリ controllerへ置くかで帯域を稼ぐ。

## 限界
CXL deviceとNUMA topologyごとに帯域特性が異なるため、プロファイリング/モデル calibrationが必要になる。GPU HBM内にKVが収まりホスト オフロードが律速でない条件では利得は小さい。8%境界や最大1.90倍は評価ハードウェア・GPU数・KV規模に依存し、CXL世代やDDR構成が変われば再測定が必要である。

## 一次資料
- https://doi.org/10.1145/3821219