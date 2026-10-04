---
canonical_id: "DOI:10.1109/HPCA53966.2022.00082"
title: "TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer"
summary: "TransPIMはTransformerの低data reuseと大きなmemory footprintに対し、token-based dataflowでlayer間データ移動を減らし、HBMへ軽量なPIM/NMC機構を追加してmemory近傍で演算するsoftware-hardware co-designである。評価では既存memory-based accelerator比3.7–9.1倍、GPU比22.1–114.9倍、既存ASIC比2.0倍throughputを報告する。"
list_summary: "トークン単位dataflowとHBM内PIM・near-メモリ処理を協調させ、Transformerの低再利用なメモリ 通信量を削減する専用accelerator。"
authors: ["Minxuan Zhou","Weihong Xu","Jaeyoung Kang","Tajana Rosing"]
published: "2022-04"
publication: "IEEE International Symposium on High-Performance Computer Architecture (HPCA 2022)"
publication_type: "conference"
publication_status: "published"
source: "https://doi.org/10.1109/HPCA53966.2022.00082"
sources: ["https://doi.org/10.1109/HPCA53966.2022.00082"]
implementation: "HBMを基盤とするPIM/NMC hybrid acceleratorをarchitecture simulationで評価し、Transformer workloadをGPU、既存memory-based accelerator、ASIC acceleratorと比較。確認済み一次資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T17:27:00+09:00"
worker_run_key: "20261004-1700-scheduled-chat-00/r01"
last_audited: null
audit_version: 0
---
# TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer

## 概要
Transformerは大きな重み・活性値を持つ一方、演算ごとのdata 再利用がCNNより低い部分が多く、外部メモリ 通信量によって計算器が遊休しやすい。従来のprocessing-in-メモリ（PIM）/near-メモリ computing（NMC）acceleratorはCNNの高い演算密度を前提にしたdataflowが多く、Transformerの注意機構やトークン逐次処理へそのまま適用すると層間データ移動が支配的になる。

TransPIMはsoftware側のトークン-based dataflowと、ハードウェア側のHBM内PIM＋near-メモリ処理を共同設計する。トークンに必要な複数層処理をメモリ hierarchy上で近接させ、従来の層-based実行で発生する中間dataの往復を減らす。評価では既存メモリ-based acceleratorより3.7–9.1倍高速、GPUより22.1–114.9倍高速、既存ASIC acceleratorより2.0倍のスループットを報告する。

## 問題設定
Transformerのlinear 層と注意機構は大規模matrixを読むが、特に推論の小バッチ条件では重み 再利用が低い。GPUは高い演算peakを持っていても、HBMから演算器へ重みを供給できなければ利用率が下がる。PIMはメモリ bank近傍で演算して帯域を増やせるが、単に既存CNN acceleratorのdataflowを移植するとTransformerの層間依存とトークン処理に適合しない。

## 手法
### token-based dataflow
従来の層-based dataflowは一つの層について多数トークンを処理し、その中間結果をメモリへ書き戻して次層へ移る。TransPIMはトークンを中心に処理を進め、トークンに必要な演算を複数段へ流すことで、中間活性値の層間往復を減らす。

この変更は外部メモリ 通信量を減らす一方、層ごとに最大バッチをまとめる方式より演算並列化が変わる。そのためハードウェア側もトークン flowに合わせたbank配置と通信経路が必要になる。

### PIM/NMC hybrid
HBM 構成へ軽量な演算機構を追加し、メモリ bank内部または近傍でmatrix演算を処理する。大量の重みを遠いGPU coreへ運ぶ代わりにdataのある場所で計算し、高い内部帯域を利用する。

すべてをPIMだけへ押し込むのではなく、演算特性に応じてPIMとnear-メモリ側を組み合わせる。これによりメモリ-intensiveな処理と、より集約した演算の双方を同一hierarchyで処理する。

### data communication
トークン-based flowでは段間の依存を保ちながら中間dataを移動する必要がある。TransPIMはHBMのbank/経路並列性を利用し、PIM/NMC間通信を従来のホスト経由往復より短くする。software スケジューラとハードウェア mappingを別々に決めず、data 転送を最小化するよう共同設計する点が中心である。

## 評価条件
|項目|条件|
|---|---|
|対象|Transformer inference|
|方式|HBM-based PIM/NMC hybrid 構成|
|比較|既存メモリ-based accelerator、GPU、ASIC accelerator|
|指標|遅延/高速化倍率、スループット|
|評価形態|ハードウェア 構成評価|

## 主要結果
既存メモリ-based acceleratorに対して3.7–9.1倍の高速化を報告する。これはTransformer向けトークン dataflowとPIM/NMC分担により、従来方式の不必要なdata 転送を減らした効果を含む。

conventional acceleratorとの比較ではGPUより22.1–114.9倍高速、既存ASIC-based acceleratorより2.0倍スループットを報告する。これらは専用ハードウェア モデル上の比較であり、現行GPU上のsoftware optimization倍率として読むべきではない。

## 既存研究との差
従来PIM acceleratorの多くはCNNのcompute-intensiveなdataflowを主対象にする。TransPIMはTransformerの低再利用とメモリ-intensive性を前提にトークン-based dataflowへ変更し、HBMのPIMとnear-メモリ engineを協調させる。通常GPU ランタイムのカーネル融合やKV キャッシュ管理とは異なり、メモリ 構成自体を変更するハードウェア-software co-designである。

## 限界
専用HBM 構成を仮定するため、既存GPUへsoftwareだけで導入できない。論文は現代のdecoder-only LLM 推論提供で一般的なPagedAttention、continuous batching、GQA、MoE等より前のTransformer ワークロードを中心にしており、2026年のproduction LLM ワークロードへ倍率を直接一般化できない。評価値はハードウェア構成とシミュレーション/モデル assumptionsに依存する。

## 一次資料
- https://doi.org/10.1109/HPCA53966.2022.00082