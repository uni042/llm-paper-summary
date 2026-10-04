---
canonical_id: "DOI:10.1109/HPCA53966.2022.00082"
title: "TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer"
summary: "TransPIMはTransformerの低データ再利用と大きなメモリ占有量に対し、トークン単位 データフローで層間データ移動を減らし、HBMへ軽量なPIM/NMC機構を追加してメモリ近傍で演算するソフトウェア・ハードウェア共同設計である。評価では既存メモリ基盤 アクセラレータ比3.7–9.1倍、GPU比22.1–114.9倍、既存ASIC比2.0倍スループットを報告する。"
list_summary: "トークン単位データフローとHBM内PIM・ニアメモリ処理を協調させ、Transformerの低再利用なメモリ 通信量を削減する専用アクセラレータ。"
authors: ["Minxuan Zhou","Weihong Xu","Jaeyoung Kang","Tajana Rosing"]
published: "2022-04"
publication: "IEEE International Symposium on High-Performance Computer Architecture (HPCA 2022)"
publication_type: "conference"
publication_status: "published"
source: "https://doi.org/10.1109/HPCA53966.2022.00082"
sources: ["https://doi.org/10.1109/HPCA53966.2022.00082"]
implementation: "HBMを基盤とするPIM/NMC hybrid アクセラレータをarchitecture simulationで評価し、Transformer ワークロードをGPU、既存メモリ基盤 アクセラレータ、ASIC アクセラレータと比較。確認済み一次資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T17:27:00+09:00"
worker_run_key: "20261004-1700-scheduled-chat-00/r01"
last_audited: null
audit_version: 0
---
# TransPIM: A Memory-based Acceleration via Software-Hardware Co-Design for Transformer

## 概要
Transformerは大きな重み・活性値を持つ一方、演算ごとのデータ 再利用がCNNより低い部分が多く、外部メモリ 通信量によって計算器が遊休しやすい。従来のメモリ内処理（PIM）/ニアメモリ計算（NMC）アクセラレータはCNNの高い演算密度を前提にしたデータフローが多く、Transformerの注意機構やトークン逐次処理へそのまま適用すると層間データ移動が支配的になる。

TransPIMはソフトウェア側のトークン単位 データフローと、ハードウェア側のHBM内PIM＋ニアメモリ処理を共同設計する。トークンに必要な複数層処理をメモリ 階層上で近接させ、従来の層単位実行で発生する中間データの往復を減らす。評価では既存メモリ基盤 アクセラレータより3.7–9.1倍高速、GPUより22.1–114.9倍高速、既存ASIC アクセラレータより2.0倍のスループットを報告する。

## 問題設定
Transformerの線形 層と注意機構は大規模行列を読むが、特に推論の小バッチ条件では重み 再利用が低い。GPUは高い演算ピークを持っていても、HBMから演算器へ重みを供給できなければ利用率が下がる。PIMはメモリ バンク近傍で演算して帯域を増やせるが、単に既存CNN アクセラレータのデータフローを移植するとTransformerの層間依存とトークン処理に適合しない。

## 手法
### token-based dataflow
従来の層単位 データフローは一つの層について多数トークンを処理し、その中間結果をメモリへ書き戻して次層へ移る。TransPIMはトークンを中心に処理を進め、トークンに必要な演算を複数段へ流すことで、中間活性値の層間往復を減らす。

この変更は外部メモリ 通信量を減らす一方、層ごとに最大バッチをまとめる方式より演算並列化が変わる。そのためハードウェア側もトークン フローに合わせたバンク配置と通信経路が必要になる。

### PIM/NMC hybrid
HBM 構成へ軽量な演算機構を追加し、メモリ バンク内部または近傍で行列演算を処理する。大量の重みを遠いGPU コアへ運ぶ代わりにデータのある場所で計算し、高い内部帯域を利用する。

すべてをPIMだけへ押し込むのではなく、演算特性に応じてPIMとニアメモリ側を組み合わせる。これによりメモリ-intensiveな処理と、より集約した演算の双方を同一階層で処理する。

### data communication
トークン単位 フローでは段間の依存を保ちながら中間データを移動する必要がある。TransPIMはHBMのバンク/経路並列性を利用し、PIM/NMC間通信を従来のホスト経由往復より短くする。ソフトウェア スケジューラとハードウェア 割当を別々に決めず、データ 転送を最小化するよう共同設計する点が中心である。

## 評価条件
|項目|条件|
|---|---|
|対象|Transformer inference|
|方式|HBM基盤 PIM/NMC hybrid 構成|
|比較|既存メモリ基盤 アクセラレータ、GPU、ASIC アクセラレータ|
|指標|遅延/高速化倍率、スループット|
|評価形態|ハードウェア 構成評価|

## 主要結果
既存メモリ基盤 アクセラレータに対して3.7–9.1倍の高速化を報告する。これはTransformer向けトークン データフローとPIM/NMC分担により、従来方式の不必要なデータ 転送を減らした効果を含む。

従来型 アクセラレータとの比較ではGPUより22.1–114.9倍高速、既存ASIC基盤 アクセラレータより2.0倍スループットを報告する。これらは専用ハードウェア モデル上の比較であり、現行GPU上のソフトウェア 最適化倍率として読むべきではない。

## 既存研究との差
従来PIM アクセラレータの多くはCNNの計算集約的なデータフローを主対象にする。TransPIMはTransformerの低再利用とメモリ-intensive性を前提にトークン単位 データフローへ変更し、HBMのPIMとニアメモリ 演算器を協調させる。通常GPU ランタイムのカーネル融合やKV キャッシュ管理とは異なり、メモリ 構成自体を変更するハードウェア・ソフトウェア共同設計である。

## 限界
専用HBM 構成を仮定するため、既存GPUへソフトウェアだけで導入できない。論文は現代のdecoder-only LLM 推論提供で一般的なPagedAttention、連続バッチ処理、GQA、MoE等より前のTransformer ワークロードを中心にしており、2026年の本番 LLM ワークロードへ倍率を直接一般化できない。評価値はハードウェア構成とシミュレーション/モデル 仮定に依存する。

## 一次資料
- https://doi.org/10.1109/HPCA53966.2022.00082