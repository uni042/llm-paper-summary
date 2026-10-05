---
canonical_id: "arXiv:1901.10430"
title: "Pay Less Attention with Lightweight and Dynamic Convolutions"
summary: "Lightweight/Dynamic Convolutionは自己注意を局所1次元畳み込みへ置換し、channel間で共有する正規化kernelと、各time stepの入力から予測するdynamic kernelでcontextを混合する。系列長に対する計算を二次attentionから線形へ変え、WMT翻訳・言語モデル・要約で強いTransformerを上回り、WMT14 En-Deで29.7 BLEUを報告する。"
list_summary: "経路共有のlightweight convolutionと入力依存動的 カーネルで自己注意を線形時間の局所混合へ置き換え、翻訳・言語モデル・要約で品質を維持する。"
authors: ["Felix Wu","Angela Fan","Alexei Baevski","Yann N. Dauphin","Michael Auli"]
published: "2019-01-29"
publication: "International Conference on Learning Representations 2019"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/1901.10430"
sources: ["https://arxiv.org/abs/1901.10430", "https://github.com/facebookresearch/fairseq"]
implementation: "fairseqでLightweight/Dynamic Convolutionを実装し、machine translation、language modeling、abstractive summarizationでTransformer self-attentionと比較。"
code: "https://github.com/facebookresearch/fairseq"
last_checked: "2026-10-06"
arxiv_id: "1901.10430"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.LG"]}
worker_completed_at: "2026-10-06T07:56:00+09:00"
worker_run_key: "20261006-0730-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
本論文は、Transformerの自己注意が各トークンから全トークンへの重みを計算しなくても、高品質な系列 modelingが可能かを検証する。Lightweight Convolutionは通常のdepthwise convolutionをさらに簡素化し、複数経路でカーネルを共有する。Dynamic Convolutionはそのカーネルを固定パラメータではなく現在time 段階の隠れ 状態から予測する。

自己注意が系列長nに対してn²個のトークン対を扱うのに対し、カーネル幅kを固定した畳み込みはO(nk)で線形に増える。論文は翻訳、言語モデル、要約で強いself-注意機構 比較対象と同等以上の品質を示し、WMT14 English-Germanで29.7 BLEUを報告した。

## 問題設定
標準self-注意機構は各問い合わせが系列全体のkeyと比較するため、長さが増えると計算・メモリが二次増加する。また各ヘッドの射影と注意機構 matrix生成には大きなmatrix演算が必要になる。

通常convolutionは局所windowしか見ない代わりに線形時間だが、経路ごとに独立カーネルを持つdepthwise convolutionでもパラメータが増え、固定カーネルは入力内容に応じて「どの位置を見るか」を変えられない。

## 手法
Lightweight Convolutionでは隠れ 経路を複数グループへ分け、グループ内経路で同じ1次元カーネルを共有する。カーネル 重みにはsoftmax正規化をかけ、window内の重みを安定した凸結合にする。重み dropoutも適用して過学習を抑える。

カーネル幅は層ごとに変えられ、下層は狭い局所pattern、上層は広い文脈を扱う構成を取れる。固定幅なら計算は系列長に線形で、全トークン対matrixを保持しない。

Dynamic Convolutionでは各time 段階の隠れ vectorへ小さなlinear 射影を適用し、その位置専用のk個のカーネル 重みを生成する。つまりself-注意機構のように入力依存の重み付けを行うが、比較対象は局所windowに限定され、keyとのpairwise dot productを作らない。

生成時はcausal convolutionとして未来位置をmaskし、直近k トークンの活性値だけを保持すればよい。注意機構の全履歴参照とは異なり、状態量はwindow幅に制約される一方、windowより遠い情報はstacked 層を通じて間接的に伝播する。

## 評価条件
|観点|内容|
|---|---|
|タスク|WMT machine translation、language modeling、CNN/DailyMail summarization|
|比較|Transformer self-注意機構、convolutional seq2seq等|
|方式|Lightweight Convolution、Dynamic Convolution|
|複雑度|固定カーネル幅で系列長に線形|
|実装|fairseq系|

## 主要結果
Dynamic ConvolutionはWMT14 English-Germanで29.7 BLEUを達成し、当時の強いself-注意機構結果を上回った。翻訳以外のlanguage modelingとabstractive summarizationでもself-注意機構に競争力ある、または改善する結果を示す。

この結果は「全トークン対注意機構が品質に必須ではない」ことを示す一方、効率評価は現代LLM 推論提供のTTFT/TPOTではない。主な計算上の利点はO(n²) 注意機構 matrixをO(nk)局所convolutionへ置き換える構造的削減である。

## 既存研究との差
通常depthwise convolutionより経路共有でパラメータを減らし、Dynamic Convolutionでは入力依存カーネルによって固定convolutionの表現力不足を補う。self-注意機構の問い合わせ-key比較とは異なり、現在位置だけからwindow 重みを予測するため計算を抑える。

## 限界
局所window外のトークンへ1 層で直接アクセスできず、非常に長距離のcopy/検索には注意機構より不利になり得る。評価は2019年のencoder-decoder中心で、現代decoder-only LLM、KV キャッシュ、FlashAttention、continuous batchingとの実測比較はない。