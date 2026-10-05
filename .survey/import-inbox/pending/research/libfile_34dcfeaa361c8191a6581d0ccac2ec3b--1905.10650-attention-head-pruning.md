---
canonical_id: "arXiv:1905.10650"
title: "Are Sixteen Heads Really Better than One?"
summary: "TransformerとBERTの注意ヘッドを推論時に除去し、多数のヘッドが冗長であることを実証した。損失のゲート感度に基づく反復枝刈りでBERTのヘッド40%程度まで性能を保ち、50%枝刈り時に高バッチで最大17.5%の推論速度向上を測定した。"
list_summary: "注意ヘッドの損失感度を用いて推論時に冗長ヘッドを削除し、BERTで高バッチ時最大17.5%の実測高速化を示した。"
authors: [Paul Michel, Omer Levy, Graham Neubig]
published: "2019-05-25"
publication: "NeurIPS 2019"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/1905.10650"
sources: ["https://arxiv.org/abs/1905.10650"]
implementation: "WMT14 En-Fr TransformerとBERT-baseを用いてヘッドmasking・反復枝刈りを実装し、GTX 1080 TiでBERT推論速度を実測。一次資料から専用公式コードURLは確認できなかった。"
code: null
last_checked: "2026-10-05"
arxiv_id: "1905.10650"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.LG"]
worker_completed_at: "2026-10-05T23:50:00+09:00"
worker_run_key: "20261005-2300-scheduled-chat-00/r01"
---

## 概要

本論文は、多頭注意（multi-head attention）の全ヘッドが推論時にも必要なのかを実験的に検証し、かなりの割合が冗長であることを示す。WMT14英仏翻訳の16ヘッドTransformerと、MultiNLIで微調整した12ヘッドBERT-baseを対象に、個別ヘッドをmaskして性能変化を測定し、さらに損失のヘッドmaskに対する感度を重要度として反復的に枝刈りする。

単一ヘッド除去では、WMT encoder self-attentionの96ヘッド中、統計的に有意な性能変化を生じたのは8ヘッドだけだった。層ごとに最重要ヘッドだけ残す実験でも、多くの層は大幅な悪化を起こさない。一方でencoder-decoder attentionの最終層を単一ヘッドにすると13.56 BLEU低下するなど、冗長性は一様ではない。

## 問題設定

多頭注意はTransformerの標準構成だが、ヘッド数を増やしたことによる表現力と、学習後の推論で実際に必要な計算量は同一ではない。もし学習後に不要なヘッドを特定できれば、再学習せずにパラメータと計算を削減できる可能性がある。

しかし、層単位で一律にヘッド数を減らすと重要なヘッドまで消す危険がある。必要なのは、モデル全体の中でどのヘッドが損失へ影響するかを比較し、重要度の低いものから削除する方法である。

## 手法

各ヘッドhに二値mask ξ_hを導入し、ξ_h=0ならそのヘッド出力をゼロにする。まず一つずつmaskしてBLEUまたは分類精度の変化を観測し、冗長性を直接測る。

反復枝刈りでは、重要度 I_h = E|∂L/∂ξ_h| を用いる。これはヘッドのmaskをわずかに変えたとき損失がどれだけ変化しやすいかを一次感度で近似する。絶対値を取ることで、正負の勾配が平均時に打ち消し合うことを避ける。WMTではtraining dataの一部から重要度を推定し、層ごとにL2正規化する。

全ヘッドを重要度順に並べ、低い側から10%ずつ削除して性能を再評価する。この方式は組合せ探索を避けつつ、層をまたいで冗長なヘッドを除去できる。maskだけでなく実際にヘッドを削除すると、対応するQ/K/Vと出力投影の部分も減るため、メモリと演算の両方を削減できる。

## 評価条件

| 項目 | WMT | BERT |
|---|---|---|
| モデル | 6層・16ヘッド Transformer large | BERT-base、12層・12ヘッド |
| タスク | WMT14 En→Fr | MultiNLI matched |
| 指標 | BLEU | accuracy |
| 追加検証 | MTNT | MultiNLI mismatched |
| 速度測定 | — | GeForce GTX 1080 Ti、2台のmachineで各3回 |
| 速度batch | — | 1 / 4 / 16 / 64 |

## 主要結果

WMTのencoder self-attentionでは96ヘッドのうち、単独除去で有意な変化を生じたのは8ヘッドで、その半数はむしろBLEUが改善した。BERTでは多くの層を単一ヘッドまで落としても有意差が出ない一方、WMTのencoder-decoder attentionには強く依存する層がある。

反復枝刈りではWMTで約20%、BERTで約40%のヘッドを削除しても目立つ性能低下がない。BERTの全ヘッドを50%削除した実測では、batch 1の17.0 examples/sが17.3、batch 4の67.3が69.1、batch 16の114.0が134.0、batch 64の124.7が146.6 examples/sとなり、batch 16と64では17.5%高速化した。小batchでは速度差がほぼ消えるため、演算削減が常に同じ割合のend-to-end高速化になるわけではない。

## 既存研究との差

一般的な重み枝刈りでは個々のweightを対象にするのに対し、本論文は注意ヘッドという構造単位を直接削除する。重要度はmask変数に対する損失感度として定義され、モデル全体を横断してヘッドを比較できる。また単なる精度分析に留まらず、物理的なヘッド削除後の推論速度を実測した点が推論効率の観点で重要である。

## 限界

速度評価はBERTとGTX 1080 Ti中心で、現代のdecoder-only LLM、FlashAttention、KVキャッシュ付き生成では同じ倍率を保証しない。WMTではencoder-decoder attentionが自己注意より枝刈りに敏感であり、ヘッド冗長性は機構・層・タスク依存である。さらに40～50%を超えて削ると性能が急落し、単純に全層を単一ヘッドへ縮めることはできない。

## 一次資料

- https://arxiv.org/abs/1905.10650