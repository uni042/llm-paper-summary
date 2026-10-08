---
canonical_id: arXiv:2405.13792
title: "xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token"
summary: "検索拡張生成（Retrieval-Augmented Generation; RAG）で取得文書本文をLLMへ投入せず、既存のdense retrieverが持つ文書embeddingをmodality bridgeでLLM表現空間へ写像し、文書1件を1 tokenとして扱う。retrieverとLLMを凍結したまま、6知識集約taskで平均10%以上改善し、非圧縮RAG比で総FLOPsを3.53倍削減する。"
list_summary: "取得文書embeddingを1 トークンへ写像して本文トークンを置換し、RAGの文脈長と総FLOPsを大幅に削減する。"
authors: [Xin Cheng, Xun Wang, Xingxing Zhang, Tao Ge, Si-Qing Chen, Furu Wei, Huishuai Zhang, Dongyan Zhao]
published: "2024-05-22"
publication: "NeurIPS 2024"
publication_type: "Conference"
publication_status: "published"
source: "https://arxiv.org/abs/2405.13792"
sources: ["https://arxiv.org/abs/2405.13792"]
implementation: "retrieverとLLMを凍結し、modality bridgeだけを学習。dense 7Bから8x7B MoEまで複数backbone、6 knowledge-intensive taskで評価。"
code: null
last_checked: "2026-10-07"
arxiv_id: "2405.13792"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.AI", "cs.IR"]
worker_completed_at: "2026-10-07T16:57:10+09:00"
worker_run_key: "20261007-1657-scheduled-chat-00/r02"
last_audited: null
audit_version: 0
---

## 概要

検索拡張生成（Retrieval-Augmented Generation; RAG）は外部文書を検索し、その本文をプロンプトへ追加してLLMに回答させる。しかし検索文書が長いほどLLMの入力トークンが増え、プリフィル計算、注意機構、KV キャッシュが増大する。xRAGは、検索器がすでに計算している固定長の**文書embedding**を再利用し、文書本文全体を1個の連続トークンへ置き換える。

中心となるのは小さなmodality bridgeである。密 retrieverのembedding空間をLLMのトークン embedding空間へ変換し、LLMには通常のテキスト トークンと同様に1個の検索 トークンとして入力する。retrieverとLLM本体は凍結されるため、既存RAG stackを大きく再学習せずに導入できる。

6つのknowledge-intensive タスクで平均10%以上の改善を示し、複数datasetでは非圧縮RAGと同等性能を保ちながら、総FLOPsを3.53倍削減した。密 7Bから8x7B MoEまで基盤モデルを変えて成立することも確認している。

## 問題設定

通常RAGでは、検索段階で文書を密 embeddingへ変換して類似度検索した後、選ばれた文書の**テキスト本体をもう一度LLMへtokenizeして投入する**。つまり検索用には固定長embeddingを使っているのに、生成段階では長い本文トークン列へ戻る。この二重表現が文脈長を増やす。

既存の文脈 compressionは文書を要約したりトークンを選別したりするが、圧縮処理自体に追加モデルが必要だったり、多数トークンが残ったりする。xRAGは検索用embeddingに文書意味がすでに圧縮されている点を利用する。

## 手法

xRAGはretrieverが生成した文書embeddingを**検索 modality**の特徴とみなす。modality bridgeはこのベクトルをLLMの隠れ dimensionへ写像し、LLMが解釈できる連続embeddingへ変換する。1文書の本文トークン列はこの1 トークンに置換される。

学習するのはbridgeだけで、retrieverとLLMは固定する。これにより、事前にofflineで構築済みのdocument embedding indexをそのまま再利用できる。検索結果ごとに別の圧縮モデルを実行して長い要約を作る必要もない。

生成時には質問テキスト トークンと、取得文書を表す圧縮トークンをLLMへ与える。文書長が数百トークンでもLLM側では1 トークンなので、プリフィル時に処理する系列 lengthを大きく減らせる。削減対象はLLMの注意機構/MLP計算とKV キャッシュであり、検索自体のembedding検索コストは残る。

## 評価

| 観点 | 条件・結果 |
|---|---|
| タスク | 6 knowledge-intensive tasks |
| 基盤モデル | 密 7Bから8x7B MoEまで |
| 学習対象 | modality bridgeのみ |
| 圧縮 | 文書embeddingを1 トークンとして投入 |
| 品質 | 6 タスク平均で10%以上改善 |
| 計算 | 非圧縮方式に対し総FLOPsを3.53倍削減 |
| 互換性 | retriever/LLMを凍結しoffline embeddingを再利用 |

性能改善は単なるトークン削減だけでなく、retriever embeddingが検索に有用な文書意味を既に保持していることを示す。一方で、元本文を完全に捨てるため、embeddingに保持されない細かな文字列情報には弱くなる可能性がある。

## 既存研究との差

要約型compressionは別モデルで本文を短く再生成し、トークン 枝刈りは元トークン列から一部を残す。xRAGは本文トークンを直接扱わず、検索段階ですでに存在する密 embeddingを別modalityとしてLLMへ融合する点が異なる。追加の文書圧縮推論を避けられる。

## 限界

1 トークンへ圧縮すると、固有名詞の綴り、数値、引用箇所などretriever embeddingが損失した細粒度情報をLLMが参照できない。bridge学習が必要で、任意のretriever/LLM組合せに完全学習不要ではない。またFLOPs削減は文脈長削減を反映するが、実際のonline 推論提供 遅延やスループットはbatching、カーネル、キャッシュ 命中等にも依存し、論文のFLOPs倍率と一致するとは限らない。

## 一次資料

- https://arxiv.org/abs/2405.13792