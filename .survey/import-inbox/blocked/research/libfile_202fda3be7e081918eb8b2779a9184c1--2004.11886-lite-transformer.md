---
canonical_id: arXiv:2004.11886
title: Lite Transformer with Long-Short Range Attention
authors: [Zhanghao Wu, Zhijian Liu, Ji Lin, Yujun Lin, Song Han]
published: '2020-04-24'
publication: ICLR 2020
publication_type: 査読会議論文
publication_status: published
source: https://arxiv.org/abs/2004.11886
sources: [https://arxiv.org/abs/2004.11886, https://arxiv.org/html/2004.11886]
summary: Lite Transformerは自己注意headを局所畳み込みと長距離注意へ分業させる長短距離注意（LSRA）で、モバイルNLPの計算量を削減する。500M/100M MAC制約でvanilla TransformerよりWMT14 En-Fr BLEUを1.2/1.7改善し、baseモデル比では計算量2.5倍削減を0.3 BLEU低下で達成する。枝刈り・量子化併用でモデルサイズを18.2倍圧縮する。
list_summary: "注意ヘッドを局所畳み込みと長距離注意へ分業し、モバイル向けに計算量2.5倍削減、枝刈り・量子化併用でモデルサイズ18.2倍圧縮を実現する。"
arxiv_id: '2004.11886'
arxiv_categories:
  primary: cs.CL
  cross_list: []
implementation: モバイルNLP向けLite Transformerを実装し、翻訳・要約・言語モデリングでMAC制約下の品質と圧縮率を評価。
code: https://github.com/mit-han-lab/lite-transformer
last_checked: '2026-10-07'
worker_completed_at: '2026-10-07T16:27:33+09:00'
worker_run_key: '20261007-1627-scheduled-chat-30/r01'
reference_main_sha: 29f4b109769b6b8ca44d7851dd3d03858d75bb27
last_audited: null
audit_version: 0
---

# Lite Transformer with Long-Short Range Attention

## 概要
モバイル環境ではTransformerの自己注意とFFNが計算・メモリ予算を圧迫する。Lite Transformerは全ヘッドに同じ役割を持たせず、局所依存は軽量な畳み込み、長距離依存は自己注意に分担させる長短距離注意（Long-Short Range Attention; LSRA）を導入する。

## 問題設定
局所的な語順や短距離依存まで全トークン対の注意で処理する必要はない一方、畳み込みだけでは文全体の長距離関係を失う。LSRAは経路を2群に分け、片方へ局所convolution、もう片方へ注意機構を適用し、両出力を結合する。

## 手法
短距離分岐は軽量convolutionで近傍情報を処理する。長距離分岐は自己注意を残すが、全経路を使わないため通常Transformerより計算を削減する。この分業を各層へ組み込み、単純に層数や幅を削る場合より同じMAC予算で表現力を維持する。

論文は構造変更だけでなく、枝刈りと量子化を後段で併用し、edge deployment時のモデルサイズも削減する。したがって計算量削減とストレージ削減を別々に積み上げる構成である。

## 評価
|条件|結果|
|---|---|
|WMT14 En-Fr、500M MAC|vanilla Transformerより+1.2 BLEU|
|WMT14 En-Fr、100M MAC|vanilla Transformerより+1.7 BLEU|
|Transformer base比較|計算量2.5倍削減、BLEU低下0.3|
|枝刈り+量子化|モデルサイズ18.2倍圧縮|
|language modeling、約500M MAC|Transformerよりパープレキシティ 1.8改善|
|Evolved Transformer比較|mobile settingで+0.5 BLEU|

計算量を減らしただけでなく、固定MAC予算で品質が通常Transformerを上回る点がLSRAの設計根拠になる。一方、2.5倍は理論/演算量ベースの削減であり、現代GPU上のLLM デコード実測高速化と同一視すべきではない。

## 既存研究との差
単純な局所 注意機構では長距離依存を失い、全体 注意機構ではモバイル予算を超える。LSRAは同一層内で局所 convolutionと大域 注意機構を並行させる。自動構成 searchを使うEvolved Transformerに対し、手設計で探索計算を必要としない。

## 限界
評価対象は当時の翻訳・要約・言語モデルで、現在の数十B規模decoder-only LLMやKV キャッシュ付き推論提供ではない。MAC削減がそのまま実時間 遅延へ変換されるかはハードウェア実装に依存する。