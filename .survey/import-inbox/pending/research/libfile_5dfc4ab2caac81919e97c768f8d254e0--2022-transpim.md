---
canonical_id: "DOI:10.1109/HPCA53966.2022.00082"
title: "TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer"
summary: "TransPIMはTransformerの低data reuseと大きなmemory footprintに対し、token-based dataflowでlayer間データ移動を減らし、HBMへ軽量なPIM/NMC機構を追加してmemory近傍で演算するsoftware-hardware co-designである。評価では既存memory-based accelerator比3.7–9.1倍、GPU比22.1–114.9倍、既存ASIC比2.0倍throughputを報告する。"
list_summary: "token単位dataflowとHBM内PIM・near-memory処理を協調させ、Transformerの低reuseなmemory trafficを削減する専用accelerator。"
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
---
# TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer

## 概要
Transformerは大きなweight・activationを持つ一方、演算ごとのdata reuseがCNNより低い部分が多く、外部memory trafficによって計算器が遊休しやすい。従来のprocessing-in-memory（PIM）/near-memory computing（NMC）acceleratorはCNNの高い演算密度を前提にしたdataflowが多く、Transformerのattentionやtoken逐次処理へそのまま適用するとlayer間データ移動が支配的になる。

TransPIMはsoftware側のtoken-based dataflowと、hardware側のHBM内PIM＋near-memory処理を共同設計する。tokenに必要な複数layer処理をmemory hierarchy上で近接させ、従来のlayer-based実行で発生する中間dataの往復を減らす。評価では既存memory-based acceleratorより3.7–9.1倍高速、GPUより22.1–114.9倍高速、既存ASIC acceleratorより2.0倍のthroughputを報告する。

## 問題設定
Transformerのlinear layerとattentionは大規模matrixを読むが、特に推論の小batch条件ではweight reuseが低い。GPUは高い演算peakを持っていても、HBMから演算器へweightを供給できなければ利用率が下がる。PIMはmemory bank近傍で演算して帯域を増やせるが、単に既存CNN acceleratorのdataflowを移植するとTransformerのlayer間依存とtoken処理に適合しない。

## 手法
### token-based dataflow
従来のlayer-based dataflowは一つのlayerについて多数tokenを処理し、その中間結果をmemoryへ書き戻して次layerへ移る。TransPIMはtokenを中心に処理を進め、tokenに必要な演算を複数stageへ流すことで、中間activationのlayer間往復を減らす。

この変更は外部memory trafficを減らす一方、layerごとに最大batchをまとめる方式より演算parallelismが変わる。そのためhardware側もtoken flowに合わせたbank配置と通信経路が必要になる。

### PIM/NMC hybrid
HBM architectureへ軽量な演算機構を追加し、memory bank内部または近傍でmatrix演算を処理する。大量のweightを遠いGPU coreへ運ぶ代わりにdataのある場所で計算し、高い内部bandwidthを利用する。

すべてをPIMだけへ押し込むのではなく、演算特性に応じてPIMとnear-memory側を組み合わせる。これによりmemory-intensiveな処理と、より集約した演算の双方を同一hierarchyで処理する。

### data communication
token-based flowではstage間の依存を保ちながら中間dataを移動する必要がある。TransPIMはHBMのbank/channel並列性を利用し、PIM/NMC間通信を従来のhost経由往復より短くする。software schedulingとhardware mappingを別々に決めず、data movementを最小化するよう共同設計する点が中心である。

## 評価条件
|項目|条件|
|---|---|
|対象|Transformer inference|
|方式|HBM-based PIM/NMC hybrid architecture|
|比較|既存memory-based accelerator、GPU、ASIC accelerator|
|指標|latency/speedup、throughput|
|評価形態|hardware architecture評価|

## 主要結果
既存memory-based acceleratorに対して3.7–9.1倍の高速化を報告する。これはTransformer向けtoken dataflowとPIM/NMC分担により、従来方式の不必要なdata movementを減らした効果を含む。

conventional acceleratorとの比較ではGPUより22.1–114.9倍高速、既存ASIC-based acceleratorより2.0倍throughputを報告する。これらは専用hardware model上の比較であり、現行GPU上のsoftware optimization倍率として読むべきではない。

## 既存研究との差
従来PIM acceleratorの多くはCNNのcompute-intensiveなdataflowを主対象にする。TransPIMはTransformerの低reuseとmemory-intensive性を前提にtoken-based dataflowへ変更し、HBMのPIMとnear-memory engineを協調させる。通常GPU runtimeのkernel融合やKV cache管理とは異なり、memory architecture自体を変更するhardware-software co-designである。

## 限界
専用HBM architectureを仮定するため、既存GPUへsoftwareだけで導入できない。論文は現代のdecoder-only LLM servingで一般的なPagedAttention、continuous batching、GQA、MoE等より前のTransformer workloadを中心にしており、2026年のproduction LLM workloadへ倍率を直接一般化できない。評価値はhardware構成とsimulation/model assumptionsに依存する。

## 一次資料
- https://doi.org/10.1109/HPCA53966.2022.00082