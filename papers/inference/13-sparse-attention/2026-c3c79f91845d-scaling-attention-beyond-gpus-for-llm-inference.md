---
canonical_id: "DOI:10.1145/3806645.3807596"
title: "Scaling Attention Beyond GPUs for LLM Inference"
summary: "Beyondは、長文脈LLMのKVキャッシュがGPU HBMを超えるとPCIe再転送が律速になる問題に対し、最近のKVはGPUで密注意、重要な古いKVはCPU DRAM上でhead別疎注意として並列処理し、log-sum-expで結果を融合するCPU–GPU協調attention runtimeである。"
list_summary: "GPU上のrecent KVとCPU上のsalient KVを並列注意機構し、PCIe転送を抑えて長文脈LLMをGPU容量外へ拡張する。"
authors: ["Weishu Deng","Yujie Yang","Peiran Du","Lingfeng Xiang","Zhen Lin","Chen Zhong","Faraz Ahmed","Lianjie Cao","Puneet Sharma","Song Jiang","Hui Lu","Jia Rao"]
published: "2026-07"
publication: "35th ACM International Symposium on High-Performance Parallel and Distributed Computing (HPDC 2026)"
publication_type: "conference"
publication_status: "published"
source: "https://doi.org/10.1145/3806645.3807596"
sources: ["https://doi.org/10.1145/3806645.3807596"]
implementation: "commodity GPUとCPU DRAMを使うdrop-in runtimeとして、KV offloadとCPU–GPU hybrid attentionを実装し、複数モデル・長文脈workloadで評価。今回確認した一次・著者資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T07:10:00+09:00"
worker_run_key: "20261004-0700-scheduled-chat-00/r01"
last_audited: null
audit_version: 0
---
# Scaling Attention Beyond GPUs for LLM Inference

## 概要
長文脈推論ではキー・バリュー（KV）キャッシュが文脈長と同時要求数に比例して増え、GPUの高帯域メモリ（HBM）を超える。単純なCPUオフロードは、注意機構のたびに必要KVをPCIe経由でGPUへ戻すため、GPU演算器よりCPU–GPUリンクが律速になる。Beyondは「CPU DRAMを低速な退避先」とみなさず、CPU側の計算能力とメモリ帯域も注意機構処理へ参加させる。

## 問題設定
既存のKV オフロードはCPUへ置いたKVを選択的にGPUへ再転送するが、転送量を減らすための疎化は品質低下を招き得る。一方、全KVを戻せばPCIe帯域を使い切る。Beyondの狙いは、recent トークンの局所情報をGPU上の密注意で確実に保持しつつ、古い文脈のうち重要部分だけをCPU上で直接処理し、PCIeを通るデータを注意機構出力など小さい中間値へ縮めることである。

## 手法
Beyondは連続デコード中にKVの重要度を追跡し、recent KVをGPU HBMへ、長期文脈のsalient KVをCPU DRAMへ配置する。GPU側はrecent KVに対して通常の密 注意機構を実行する。CPU側はヘッドごとに選ばれたsalient KVへsparse 注意機構を並列実行し、CPUのDRAM帯域とvector computeを利用する。

二つの注意機構は独立なsoftmax正規化を持つため、単純加算では全体 注意機構と整合しない。Beyondは各部分のlog-sum-exp統計を使ってGPU側とCPU側の出力を再正規化して融合する。これによりCPU側KV本体をGPUへ移動せず、両メモリ 階層の帯域を同時利用する。KV選択はヘッド単位で行われ、全ヘッドへ同一の疎集合を強制する方式より文脈依存性を残す。

## 評価条件
|項目|条件|
|---|---|
|対象|長文脈・multi-user LLM inference|
|構成|commodity GPU + CPU DRAM、PCIe接続|
|比較|GPU-only/全体 注意機構、KV オフロード/sparse-注意機構系比較対象|
|主指標|対応文脈長、バッチ scalability、遅延/スループット、accuracy|
|実装|recent 密 GPU 注意機構 + salient sparse CPU 注意機構|

## 主要結果
論文は、KVがGPU容量を超える領域でCPUとGPUのaggregate メモリ 帯域を利用し、既存のsparse/オフロード 比較対象より長い系列と大きいバッチを処理できると報告する。重要なのはCPUを単なるストレージにせず注意機構実行主体にすることで、PCIe再読込を最小化しながらrecent部分は密のまま維持する点である。公開abstractは単一の普遍的高速化倍率倍率を主張しておらず、条件別数値は本文表を参照すべきである。

## 既存研究との差
CPU オフロード方式は通常、GPU演算のためのデータ供給源としてCPUを使う。Beyondは注意機構をメモリ 階層ごとに分割し、CPU側でも注意機構を計算して最後にsoftmax整合な融合を行う。このため「転送するKVを選ぶ」だけでなく「KVが存在する場所で計算する」設計へ変えている。

## 限界
CPU性能、DRAM帯域、PCIe世代、GPU HBM容量の比率で最適な分担は変わる。疎化された古い文脈だけをCPU側で見るため、重要度選択が外れるワークロードでは全体 注意機構との差が増える可能性がある。GPU間NVLinkを使うmulti-GPU clusterやプリフィル/デコード分離環境への一般化は、今回確認した一次資料では中心評価ではない。

## 一次資料
- https://doi.org/10.1145/3806645.3807596