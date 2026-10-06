---
canonical_id: "arXiv:2601.10155"
title: "LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers"
summary: "LOOKATはattention scoreを内積類似度検索とみなし、keyをproduct quantizationでsubspace codeへ圧縮し、queryとcodebookの内積表をlookupしてscoreを求める。INT4/8のようにkeyをFP16へ逆量子化してから読む必要をなくし、GPT-2評価でkeyを64倍圧縮しつつoutput cosine fidelity 95.7%、Spearman rank correlation 0.95超を報告する。"
list_summary: "KV keyをproduct-量子化 コードへ置換し、問い合わせ-codebook lookupで注意機構 スコアを直接計算して逆量子化帯域を避ける。"
authors: ["Aryan Karmore"]
published: "2026-01-15"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2601.10155"
sources: ["https://arxiv.org/abs/2601.10155"]
implementation: "GPT-2のattention keyをproduct quantizationし、自然文・code・technical text等でoutput fidelity、KL divergence、rank correlationを評価。sequence length 1024まで検証。確認した一次資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2601.10155"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.AI"]
worker_completed_at: "2026-10-06T15:49:00+09:00"
worker_run_key: "20261006-1500-scheduled-chat-00/r02"
reference_main_sha: "e42a664c3f677e45648eede99ddcb91d93c9c1b7"
last_audited: null
audit_version: 0
---

## 概要

通常の低bit KV量子化は保存容量を減らしても、注意機構 スコアを計算する直前にkeyをFP16へ逆量子化し、全key vectorを演算器へ読み込む。このためedge deviceのようにDRAM帯域が小さい環境では、保存bit数ほど注意機構帯域が減らない。LOOKATは`QK^T`が問い合わせに対するinner-product similarity searchであることを利用し、vector databaseのproduct 量子化（PQ）とasymmetric distance computation（ADC）を注意機構へ持ち込む。

key vectorを複数subspaceへ分け、各subspaceを学習済みcodebookのindexだけで保存する。問い合わせ到着時には問い合わせ subvectorと全centroidの内積を小さいlookup tableへ先に計算し、各トークンのkey スコアは保存indexで表を引いて加算する。圧縮keyをFP16へ展開しないため、key帯域を直接減らせる。

## 問題設定

自己回帰デコードでは過去トークンのkey/valueを毎段階参照するため、文脈 lengthに比例してKV キャッシュの読み出し量が増える。INT4/INT8 scalar 量子化はキャッシュ ストレージを圧縮できるが、標準GEMM/注意機構へ入れる前のdequantizationと展開後データ移動が残る。

LOOKATの狙いはkeyの数値を高精度に復元することではなく、注意機構で重要な「どのkeyが問い合わせと近いか」という順位構造を圧縮表現のまま再現することにある。

## 手法

### Product Quantization

d次元keyをm個のsubvectorへ分割し、各subspaceにK個のcentroidを持つcodebookを学習する。各key subvectorは最も近いcentroidのindexだけを保存する。たとえば1-byte indexなら、FP16の64次元key全体を読む代わりに少数byteを読む。

### Asymmetric Distance Computation

問い合わせは量子化せず高精度のまま使う。各問い合わせ subvectorとcodebook centroidの内積を事前に`m×K`個だけ計算してlookup tableへ置く。トークンごとの注意機構 スコアは、そのトークンが持つm個のコード indexで表を引き、値を加算して近似する。

この構造では全トークンの全体 keyをDRAMから読む必要がなく、帯域コストは主にコード index列になる。代わりに問い合わせごとのtable作成とlookup/addの計算が増え、メモリ律速 注意機構をcompute寄りへ移す。

## 評価条件

| 項目 | 条件 |
|---|---|
| モデル | GPT-2 |
| 対象 | 注意機構 key キャッシュ |
| 文脈 | 最大1024 トークンまで検証 |
| 比較 | FP16、INT4/INT8 scalar 量子化 |
| 指標 | 出力 cosine fidelity、KL divergence、Spearman ランク correlation、top 注意機構保持 |
| 学習 | モデル retrainingなし、codebook calibrationのみ |

## 主要結果

64倍key圧縮のLOOKAT-2で出力 cosine fidelity 95.7%、32倍圧縮のLOOKAT-4で95.0%を報告する。全LOOKAT設定で注意機構 rankingのSpearman相関は概ね0.95を超え、keyの絶対値再構成よりranking保持を狙う設計が機能する。

一方、文脈 lengthを64から1024へ伸ばすとfidelityは低下し、長文脈ほど近似誤差が蓄積する。1024 トークンでもランク correlationは高い水準を保つが、評価はGPT-2規模であり、現代LLMの数万〜百万トークン 文脈を実証したものではない。

## 既存研究との差

KIVI等のscalar KV量子化はkey/valueの各数値を低bitへし、注意機構計算時に数値表現へ戻す。LOOKATはkeyをvector-search コードへ変換し、復元せずlookup tableから内積近似値を直接得る。このため「ストレージ圧縮」だけでなくkey read 帯域そのものを減らすことを目的にする。

## 限界

現行評価ではvalueはFP16のままで、KV キャッシュ全体が64倍になるわけではない。codebook品質はcalibration dataへ依存し、長文脈ではfidelity低下が観測される。また高速lookupを活かす専用カーネル/NPU実装の実測遅延は十分検証されておらず、64倍という値はkey ストレージ圧縮率であってエンドツーエンド 高速化倍率ではない。

## 一次資料

- https://arxiv.org/abs/2601.10155