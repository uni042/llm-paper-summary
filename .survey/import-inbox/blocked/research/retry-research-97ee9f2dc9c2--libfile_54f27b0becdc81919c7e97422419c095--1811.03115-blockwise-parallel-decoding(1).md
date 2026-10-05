---
canonical_id: "arXiv:1811.03115"
title: "Blockwise Parallel Decoding for Deep Autoregressive Models"
summary: "Blockwise Parallel Decodingは複数の補助prediction headで将来の複数tokenを同時提案し、元のscoring modelが左から検証して一致する最長prefixだけを一度にcommitする。greedy decodingと同一品質の設定でiteration数を最大2倍削減し、品質を少し許容すると最大7倍、wall-clockでは最大4倍の高速化を報告する、投機的復号の先駆的方式である。"
list_summary: "複数将来トークンを並列提案し、元モデルで検証した最長一致接頭辞をまとめて確定することで自己回帰デコードの逐次段階数を削減する。"
authors: ["Mitchell Stern","Noam Shazeer","Jakob Uszkoreit"]
published: "2018-11-07"
publication: "NeurIPS"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/1811.03115"
sources: ["https://arxiv.org/abs/1811.03115"]
implementation: "self-attention sequence modelでmachine translationとimage super-resolutionを評価し、greedy decodingに対するiteration数とwall-clockを測定。"
code: null
last_checked: "2026-10-06"
arxiv_id: "1811.03115"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.CL"]
worker_completed_at: "2026-10-06T07:00:00+09:00"
worker_run_key: "20261006-0700-scheduled-chat-00/r01"
reference_main_sha: "b66aec387fad5bd8e23d8ba03ddab4b574484e1b"
last_audited: null
audit_version: 0
---

## 概要
自己回帰モデルは次トークンが確定するまでその次を生成できないため、Transformerのように系列を並列処理できる構成でもデコードは1 トークンずつ進む。Blockwise Parallel Decodingは1回のモデル evaluationで複数の将来位置を提案し、その候補を元のscoring モデルで並列検証して、greedy 復号と整合する最長接頭辞をまとめて受理する。

品質を変えない設定ではgreedy decoderのiteration数を最大約2倍削減し、少量の品質低下を許す設定では最大7倍まで削減する。実時間では最速条件で標準greedy 復号比最大4倍の高速化を報告する。後年の投機的復号（投機的復号）と同じ「安い提案を作り、強いモデルで並列検証する」発想の先駆けである。

## 問題設定
autoregressive factorizationではトークン t+1がトークン tへ依存するため、通常デコードのcritical pathは出力長に比例する。self-注意機構 モデルは学習時に全位置を並列計算できても、inference時のgreedy generationではこの依存を避けられない。

複数トークンを無条件に同時生成するnon-autoregressive方式はiterationを減らせるが、条件付き依存を弱めるため品質が落ちやすい。必要なのは、最終的なscoring モデルの判断を保ちながら、1 iterationで1 トークン以上進む仕組みである。

## 手法
### block proposal
通常の次トークン ヘッドに加えて、現在接頭辞から2 段階先、3 段階先など複数offsetのトークンを予測する補助ヘッドを学習する。1回の順伝播で将来ブロック全体の候補を並列に得る。

### parallel scoring
提案ブロックを接頭辞へ仮置きし、self-注意機構 モデルが複数位置を並列処理できる性質を使って各位置のgreedy 予測を一度に計算する。補助ヘッドの候補をそのまま信頼せず、元モデルのスコアを検証に使う。

### longest-prefix acceptance
左から候補とscoring モデルの予測を比較し、一致する最長接頭辞だけをcommitする。最初に不一致となった位置ではscoring モデル自身のトークンを採用して次iterationへ進む。厳密設定ではこの規則により標準greedy decoderと同じ出力を維持できる。

### speed-quality tradeoff
受理基準を緩めればより長いブロックをcommitでき、iteration数をさらに減らせるが出力 qualityは変化する。論文は無損失なgreedy-equivalent設定と、品質を少し許容して高速化を増やす設定を分けて評価する。

## 評価条件
| 観点 | 内容 |
|---|---|
| 構成 | deep self-注意機構 autoregressive モデル |
| タスク | machine translation、image super-resolution |
| 比較対象 | standard greedy 復号 |
| 指標 | 復号 iterations、実時間、タスク quality |
| 並列化 | future-トークン proposal + 並列 validation |

## 主要結果
| 条件 | 比較 | 結果 | 品質 |
|---|---|---:|---|
| strict validation | greedy decoder | iteration最大約2倍削減 | lossなし |
| relaxed 条件 | greedy decoder | iteration最大約7倍削減 | slight degradation |
| fastest implementation | greedy decoder | 実時間最大4倍高速 | 条件依存 |

iteration削減と実時間 高速化倍率は同一ではない。1 iterationあたりは複数positionをスコアする追加計算があるため、7倍のiteration削減が7倍の実時間短縮にはならず、実測最大は4倍である。

## 既存研究との差
non-autoregressive generationは全トークンを並列生成して逐次依存を捨てるのに対し、本方式はautoregressive scoring モデルを検証へ残す。後のドラフト-モデル型投機的復号と比べると、別小モデルではなく同モデルに将来offset用ヘッドを追加してproposalを作る点が異なる。

## 限界
補助ヘッドを学習する必要があり、既存チェックポイントへ完全学習不要で適用する方式ではない。候補が頻繁に外れるタスクでは1 iterationあたりのadvanceが1 トークンへ近づき、追加proposal/検証計算だけが残る。評価は現在の大規模LLM 推論提供以前のmachine translation等が中心で、KV キャッシュやcontinuous batchingとの統合は論文の主評価外である。

## 一次資料
- https://arxiv.org/abs/1811.03115