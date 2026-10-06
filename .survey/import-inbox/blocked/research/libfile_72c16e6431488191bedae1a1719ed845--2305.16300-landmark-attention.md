---
canonical_id: "arXiv:2305.16300"
title: "Landmark Attention: Random-Access Infinite Context Length for Transformers"
summary: "Landmark Attentionは入力をblockへ分け、各block末尾のlandmark tokenをそのblockの要約兼routing keyとして学習させる。推論時はlandmarkへのattention scoreで関連blockを選び、そのblockのtokenだけを詳細attentionへ展開するため、別retrieverなしでTransformer自身が過去文脈をrandom accessできる。LLaMA 7Bをfine-tuneして32K超のcontextへ拡張した。"
list_summary: "各文脈 ブロックをlandmark トークンで索引化し、注意機構自身が関連ブロックだけを選んで展開することで全履歴へのrandom アクセスと長文脈効率を両立する。"
authors: ["Amirkeivan Mohtashami","Martin Jaggi"]
published: "2023-05-25"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2305.16300"
sources: ["https://arxiv.org/abs/2305.16300"]
implementation: "Transformer/LLaMA 7Bへlandmark attentionを導入し、language modelingと長文脈retrievalを評価。32K超contextで推論を実証し公式実装を公開。"
code: "https://github.com/epfml/landmark-attention"
last_checked: "2026-10-06"
arxiv_id: "2305.16300"
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
長文脈Transformerで全過去トークンへ注意機構するとKV保持と注意機構計算が文脈長に比例して増える。局所/recurrent メモリは古い情報へのrandom アクセスを弱め、外部検索はモデル本体と別のembedding/indexを必要とする。Landmark Attentionは入力ブロックごとにlandmark トークンを挿入し、モデル自身の注意機構 スコアをブロック 検索 スコアとして使う。

推論時は全過去ブロックのlandmarkだけをまず比較し、スコアの高いブロックを選んで、そのブロック内トークンのKVを詳細注意機構へ展開する。これにより全履歴を候補として残しつつ各段階で読むトークン数を制限する。LLaMA 7Bをfine-tuneした実験では32Kを超える文脈へ拡張し、Transformer-XLと同程度の性能をより少ないretrieved トークンで達成した。

## 問題設定
sliding-window 注意機構は計算をboundedにできるがwindow外情報を直接参照できない。Transformer-XL型recurrenceは過去状態を順次圧縮/再利用するため、任意の古いブロックを内容に応じて選ぶrandom アクセスが弱い。RAGのような外部retrieverはrandom アクセスできるが、検索 表現とLM 注意機構が別学習系になる。

必要なのは、過去を完全破棄せず、問い合わせごとに少数ブロックだけを選び、その選択をLM自身の注意機構機構で学習する方法である。

## 手法
### landmark token
固定長ブロックの境界にlandmark トークンを追加する。ブロック内トークンがlandmarkへ情報を集約するよう注意機構 maskと学習を設計し、landmarkが「このブロックを後で読む価値」を判定する代表トークンになる。

### two-stage attention
現在問い合わせはまずlandmark群へ注意機構し、関連度の高いブロックを選ぶ。選択後、そのブロックに含まれる通常トークンを注意機構候補へ展開する。全トークンへスコアを計算する代わりに、粗いブロック selectionと細かいトークン 注意機構を分離する。

### random-access memory
古いブロックのKVはメモリ hierarchyへ保持でき、landmark indexだけを高速層へ置く。選ばれたブロックだけを詳細注意機構用に取得するため、CPU/SSD等の大容量層との統合余地がある。論文はspecialized data structureとの互換性を設計上の利点として述べる。

### training
通常Transformerへlandmark トークンと対応maskを追加してfine-tuneし、検索を別lossだけで学習するのではなくlanguage modeling 目的関数を通して「どのブロックを読むと次トークン予測に有効か」を学ばせる。

## 評価条件
| 観点 | 内容 |
|---|---|
| モデル | Transformer系、LLaMA 7B 微調整 |
| 文脈 | 32K超まで実証 |
| 比較対象 | Transformer-XL等 |
| 指標 | language modeling quality、retrieved トークン数、長文脈利用 |
| 検索 | モデル 注意機構内のlandmark ルーティング |

## 主要結果
Transformer-XLと比較可能な性能を保ちながら、各段階で検索するトークン数を大きく制限できる。LLaMA 7Bでは32K超文脈でのinferenceを実証し、元の短い文脈 limitを越えて過去ブロックへアクセスできる。

32Kは「32K全トークンへ毎段階 密 注意機構する」意味ではない。landmarkでブロックを選別し、選択ブロックだけを詳細注意機構へ入れることがメモリ/compute削減の核心である。

## 既存研究との差
Transformer-XLのrecurrent メモリは時間順の状態再利用、RAGは外部retrieverによるdocument selectionである。Landmark AttentionはTransformerの注意機構そのものをretrieverとして使い、同じ表現空間でブロック selectionとトークン processingを行う。局所 注意機構と違ってwindow外ブロックも候補から消さない。

## 限界
landmark ルーティングを学ぶ微調整が必要で、既存チェックポイントへ完全学習不要で適用できない。過去KVを外部メモリへ置く場合の実I/O 遅延やキャッシュ policyは別システム問題であり、論文の中心評価ではない。検索が誤ると必要ブロックが詳細注意機構へ入らず品質が落ちる。

## 一次資料
- https://arxiv.org/abs/2305.16300
- https://github.com/epfml/landmark-attention