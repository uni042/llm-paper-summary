---
canonical_id: "arXiv:2302.10866"
title: "Hyena Hierarchy: Towards Larger Convolutional Language Models"
summary: "Hyenaはattentionの二次計算を、暗黙parameter化した長畳み込みとdata-controlled gatingの階層へ置換するsubquadratic sequence operatorである。WikiText103/The Pileでdense-attention-free modelとしてTransformer品質に達し、sequence 2Kでtraining computeを20%削減、operator単体では8Kでattentionの2倍、64Kで100倍高速と報告する。"
list_summary: "暗黙長畳み込みと入力依存gatingを階層化して注意機構を置換し、長系列ほど有利なsubquadratic language モデルを構成する。"
authors: ["Michael Poli", "Stefano Massaroli", "Eric Nguyen", "Daniel Y. Fu", "Tri Dao", "Stephen Baccus", "Yoshua Bengio", "Stefano Ermon", "Christopher Ré"]
published: "2023-02-21"
publication: "ICML"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2302.10866"
sources: ["https://arxiv.org/abs/2302.10866"]
implementation: "Hyena operatorとlanguage modelを実装し、WikiText103、The Pile、長距離recall/reasoning taskで品質・compute・operator速度を評価。公式実装を公開。"
code: "https://github.com/HazyResearch/safari"
last_checked: "2026-10-06"
arxiv_id: "2302.10866"
arxiv_categories:
  primary: "cs.LG"
  cross_list: []
worker_completed_at: "2026-10-06T07:00:00+09:00"
worker_run_key: "20261006-0700-scheduled-chat-00/r01"
reference_main_sha: "b66aec387fad5bd8e23d8ba03ddab4b574484e1b"
last_audited: null
audit_version: 0
---

## 概要
自己注意は任意のトークン対を直接比較できるが、系列長Lに対して注意行列がL×Lとなり、長文脈で計算・メモリが急増する。Hyenaは暗黙的にパラメータ化した長畳み込みと入力依存gatingを複数段重ね、密 注意機構を使わず長距離interactionを表現する。WikiText103/The PileでTransformer品質へ到達し、2K 系列では同品質へ必要な学習 computeを20%削減する。演算子 ベンチマークでは最適化注意機構に対し8Kで2倍、64Kで100倍高速と報告する。

## 問題設定
通常convolutionはカーネル長が文脈長と同じならパラメータ数も増える。FFTで計算量を抑えても固定カーネルだけでは問い合わせに応じて参照先を変える注意機構のdata dependenceを表現しにくい。Hyenaは「長いfilterを少数パラメータから生成すること」と「入力-dependent ゲートでfilter出力を選択的に通すこと」を組み合わせる。

## 手法
### implicit long convolution
長さLのfilter coefficientをそのまま学習パラメータとして持たず、位置を入力する小ネットワークから生成する。文脈を伸ばしてもパラメータ数がfilter長へ線形増加せず長距離カーネルを表現できる。

### data-controlled gating
入力系列から複数射影を作り、一方を長畳み込みへ通し、別射影を要素積ゲートとして掛ける。固定filterの出力を入力内容に応じて抑制・強調する。

### Hyena hierarchy
gatingとlong convolutionを複数orderで階層的に反復する。orderを上げるほど複数トークン間の高次interactionを表現でき、注意機構のpairwise interactionに近い役割をsubquadratic 演算子で担う。

### FFT実装
長畳み込みはFFT domainで実行しdirect convolutionのO(L²)を避ける。系列が長いほど注意機構との差が拡大する。

## 評価条件
| 観点 | 内容 |
|---|---|
| data | WikiText103、The Pile |
| タスク | language modeling、long-range 再取得/reasoning |
| 比較対象 | Transformer 注意機構、既存subquadratic 演算子 |
| 系列 | 2K 学習比較、8K/64K 演算子速度比較 |
| 指標 | パープレキシティ/accuracy、学習 compute、演算子 遅延 |

## 主要結果
| 条件 | 比較 | 結果 | 注意点 |
|---|---|---:|---|
| language modeling | Transformer | 同等品質 | 密 注意機構なし |
| 系列 2K | 同品質Transformer | 学習 compute -20% | 学習側compute |
| 演算子 8K | optimized 注意機構 | 2倍高速 | 演算子単体 |
| 演算子 64K | optimized 注意機構 | 100倍高速 | 演算子単体 |
| long-range タスク | 他subquadratic方式 | accuracy +50pt超の条件 | 再取得/reasoning能力 |

100倍は64Kにおける演算子比較であり、language モデル全体のトークン/sが100倍になることを意味しない。射影、MLP等は残るためエンドツーエンド改善は小さくなる。

## 既存研究との差
S4/H3などのSSMや長畳み込み系はsubquadraticだが注意機構との表現力差が課題だった。Hyenaはimplicit filterとdata-controlled ゲートを階層化し、密 注意機構層を残さず標準language modeling品質を狙う。

## 限界
最大速度倍率は演算子 マイクロベンチマークでエンドツーエンド 推論提供評価ではない。FFTは短系列では固定オーバーヘッドがあり常に注意機構より有利とは限らない。既存Transformer チェックポイントへランタイムだけで適用する方式でもない。

## 一次資料
- https://arxiv.org/abs/2302.10866
- https://github.com/HazyResearch/safari
