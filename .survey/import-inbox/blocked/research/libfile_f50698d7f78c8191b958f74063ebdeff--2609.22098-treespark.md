---
canonical_id: "arXiv:2609.22098"
title: "TreeSpark: Calibrated, Load-Adaptive Draft Trees for Semi-Autoregressive Speculative Decoding"
summary: "TreeSparkは半自己回帰drafterの既存Markov headから親条件付き確率を取り出してedge acceptanceへ較正し、path survivalに基づくbest-first tree展開と負荷適応budgetを行うlossless speculative decodingである。同じdrafterの調整済みchain比で1 round当たり受理draft tokenを15〜25%増やし、単一request wall-clockを8〜14%高速化し、高負荷時はtreeをchainへ縮退させる。"
list_summary: "親条件付き受理確率で下書き木をbest-first展開し、roundごとの期待利得と推論提供負荷に応じてtree幅を変える無損失 投機的復号。"
authors: ["Huapeng Zhou","Huayu Wang","Xinyu Wang"]
published: "2026-08-12"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2609.22098"
sources: ["https://arxiv.org/abs/2609.22098","https://github.com/PopSoda2002/TreeSpark"]
implementation: "半自己回帰block drafter上でfixed tree、tuned chainと比較し、temperature別acceptance、single-request wall-clock、serving load適応を評価。公式code/artifact公開。"
code: "https://github.com/PopSoda2002/TreeSpark"
last_checked: "2026-10-06"
arxiv_id: "2609.22098"
arxiv_categories: {primary: "cs.CL", cross_list: []}
reference_main_sha: "7755cc2d70dde454ac2743f6c86772df469b9478"
worker_completed_at: "2026-10-06T19:04:00+09:00"
worker_run_key: "20261006-1830-scheduled-chat-30/r02"
last_audited: null
audit_version: 0
---
## 概要
投機的復号（投機的復号）は軽量drafterが複数トークンを提案し、対象モデルがまとめて検証することで対象 順伝播回数を減らす。半自己回帰（semi-autoregressive）ブロック drafterでは一回の基盤モデル passからブロック全体を出せるためドラフト自体は安いが、各位置の周辺確率だけでtreeを広げると「どの親トークンから続く候補か」を無視して誤った分岐へ検証budgetを使う。

TreeSparkはdrafterに既存のMarkov ヘッドが持つ親条件付き分布を利用し、各edgeの受理確率へ較正する。そこからpath全体が生存する確率を計算し、best-firstで価値の高いノードからtreeを展開する。固定ノード数ではなく、そのroundの予測利得と推論提供 読み込みに応じて停止点も変える。

## 問題設定
tree 投機的復号では複数continuationを一度の対象 順伝播で検証できるが、ノード数を増やすほど対象側注意機構/GEMMとメモリを消費する。per-position marginalが高いトークンでも、低確率の親からしか到達しないなら実際に受理される確率は低い。

また単一リクエストでは広いtreeが得でも、同時リクエストが増えると検証 バッチが大きくなりqueueingを悪化させる。固定tree budgetはこの負荷変化へ適応できない。

## 手法
### 親条件付きedge score
半自己回帰drafterのMarkov ヘッドから、候補トークンが特定parentを延長する条件付き分布を読む。新しい大規模drafterを学習せず、既存ヘッドの出力を利用するため追加ドラフト コストは小さい。

### acceptance calibrationとpath survival
raw確率を対象によるedge 受理率確率へ較正し、rootからノードまでのedge生存確率を組み合わせてpath survivalを得る。tree候補の順位を位置ごとのmarginalではなく「そのノードまで実際に到達して受理される確率」で決める。

### best-first展開とround停止
最も高い期待受理利得を持つfrontier ノードから展開し、追加ノードの期待利益が検証コストを上回る間だけtreeを広げる。roundごとのdrafter確信度が低ければ早く止まり、高ければ広いtreeを使う。

### load-adaptive serving
同時負荷が高いと対象 検証 容量が貴重になるためtree budgetを縮小し、極端な場合はchainへ戻す。低負荷では余剰computeを使って分岐を増やし、受理トークン/roundを伸ばす。

### lossless sampling
temperature付きsamplingでも分布を変えないよう、siblingをreplacementなしで標本し、recursive rejection時に対応するresidual 分布を使う。したがってtree形状や負荷適応を変えても対象 分布を保持する。

## 評価条件
|項目|内容|
|---|---|
|drafter|semi-autoregressive ブロック drafter + Markov ヘッド|
|比較|matched fixed-budget tree、tuned chain|
|sampling|複数temperature、無損失 recursive rejection|
|指標|accepted ドラフト トークン/round、single-リクエスト 実時間、読み込み下スループット/遅延|
|適応|round別tree停止、推論提供 読み込み別tree縮小|
|実装|公式コード/artifact公開|

## 主要結果
同じdrafterの調整済みchainと比較し、TreeSparkは1 round当たり受理ドラフト トークンを15〜25%増やし、single-リクエスト 実時間 復号を8〜14%高速化する。matched fixed budgetのtreeに対しても全temperatureで適応型 treeが改善する。

負荷が上昇するとtreeを段階的に縮め、検証側の余剰容量がなくなる領域ではchainへ近づく。このため単一リクエストで最適化した広いtreeを高負荷でも固定してqueueingを悪化させる挙動を避ける。

## 既存研究との差
従来tree方式は各ドラフト位置のmarginalを独立に順位付けしやすく、親子依存を失う。TreeSparkはMarkov ヘッドの親条件付き分布を直接edge スコアへ使う。またtree サイズを静的hyperparameterにせず、round内のpath survivalと推論提供 読み込みの二段階で変える。

## 限界
Markov ヘッドを持つ半自己回帰drafterを前提とし、通常の自己回帰drafterへ同じ追加費用で適用できるとは限らない。較正が分布変化で崩れるとノード rankingが悪化する。高負荷時はchainへ縮退するため、tree固有の受理率利得も小さくなる。