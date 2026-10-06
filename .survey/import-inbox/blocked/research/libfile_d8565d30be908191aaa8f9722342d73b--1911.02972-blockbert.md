---
canonical_id: "arXiv:1911.02972"
title: "Blockwise Self-Attention for Long Document Understanding"
summary: "BlockBERTはself-attention行列をblock分割し、各attention headが一部のblock pairだけを計算する構造化疎attentionをBERTへ導入する。RoBERTa系比較でtraining memoryを18.7～36.1%、training timeを12.0～25.1%削減し、test時のinference timeを27.8%短縮しながらQA精度を維持または改善する。"
list_summary: "注意機構行列を規則的なブロック maskへ分割しヘッドごとに異なるブロック接続を割り当て、長文書BERTのメモリと推論時間を削減する構造化疎注意機構。"
authors: ["Jiezhong Qiu","Hao Ma","Omer Levy","Scott Wen-tau Yih","Sinong Wang","Jie Tang"]
published: "2019-11-07"
publication: "Findings of EMNLP 2020"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/1911.02972"
sources: ["https://arxiv.org/abs/1911.02972","https://doi.org/10.18653/v1/2020.findings-emnlp.232"]
implementation: "BERT/RoBERTa系encoderへblockwise sparse multi-head attentionを実装し、language-model pretrainingと長さの異なるquestion-answering benchmarkでmemory、training/inference time、accuracyを評価。"
code: "https://github.com/xptree/BlockBERT"
last_checked: "2026-10-06"
arxiv_id: "1911.02972"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.LG"]}
worker_completed_at: "2026-10-06T15:52:00+09:00"
worker_run_key: "20261006-1530-scheduled-chat-30/r01"
reference_main_sha: "0bbe57b3f448170074d516761dd9f8c955981e5e"
last_audited: null
audit_version: 0
---
## 概要
BERT型Transformerのself-注意機構は系列 length Nに対してN×Nの注意機構 matrixを作るため、長文書ではメモリと計算時間が急増する。BlockBERTはモデル widthや層数を削るのではなく、注意機構 matrixの接続自体を規則的なブロック sparse patternへ変える。

## 問題設定
ヘッド数や隠れ dimensionを減らす一般的なモデル compressionは表現能力も直接削る。BlockBERTは各ヘッドが全トークン pairを見る必要はないと考え、短距離・長距離の異なる依存を複数ヘッドへ分担させることで密 注意機構の冗長計算を省く。

## 手法
系列をn個の連続ブロックへ分けると注意機構 matrixはn×n個のブロックになる。各maskは問い合わせ ブロックごとに一つのkey/value ブロックへ接続するpermutation patternを持ち、異なるshift/permutationを複数用意する。

multi-ヘッド 注意機構ではヘッドごとに異なるブロック maskを割り当てる。あるヘッドは同じブロック内の局所 依存関係を、別ヘッドは離れたブロックへの接続を担当できる。全ヘッドを合わせれば複数種類の距離を覆いつつ、各ヘッド単体では密 N×N スコアを計算しない。

ブロック単位の規則性があるため、任意のunstructured sparsityよりmatrix multiplicationへ載せやすい。注意機構以外のFFN等は通常BERTと同じため、削減率はモデル全体では注意機構比率に制約される。

## 評価条件
|項目|内容|
|---|---|
|モデル|BERT/RoBERTa系encoder|
|タスク|language-モデル pretraining、複数question answering ベンチマーク|
|入力|paragraph lengthを複数条件で変更|
|比較|密 RoBERTa/BERT系|
|指標|メモリ、学習 time、inference time、予測 accuracy|

## 主要結果
学習ではメモリ使用量を18.7～36.1%削減し、学習時間を12.0～25.1%短縮する。削減幅にrangeがあるのは系列 length等の条件で注意機構が全コストに占める割合が変わるためである。

test時にはRoBERTa系比較対象に対してinference timeを27.8%短縮し、予測 accuracyは同等または一部タスクで改善する。したがって単なるFLOPs推定ではなく、実測inference timeでも構造化sparsityの利得を確認している。

## 既存研究との差
固定局所 windowだけでは遠距離依存関係を直接結べない。BlockBERTは複数のブロック permutationを注意機構 ヘッドへ分散し、局所とnon-局所 connectionを同じ層内で持つ。後年のLongformer/BigBird等と同様の疎注意機構系だが、ヘッドごとのブロック structureという単純な実装単位を強く利用する。

## 限界
評価はencoder-only BERT世代であり、autoregressive decoderのKV キャッシュやcontinuous batchingは扱わない。ブロック サイズとmask配置は固定構造なので、入力ごとに重要トークンを選ぶ動的 sparse 注意機構ほど適応的ではない。現代GPUのFlashAttentionとの比較も論文時点では存在しない。