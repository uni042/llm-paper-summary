---
canonical_id: arXiv:2507.21526
arxiv_id: '2507.21526'
arxiv_categories:
  primary: cs.CL
  cross_list: []
title: Accelerating Prefilling via Decoding-time Contribution Sparsity
summary: TriangleMixはprefillの注意スコアの大小ではなく、生成開始位置への勾配寄与が小さい中間領域を特定し、一部の層を三角形の静的疎注意へ置換する。Llama 3.1 8Bの128K入力では対象注意カーネル750msから49ms（15.3倍）、全体TTFT34.5秒から23.4秒（32%減）。RULER平均は90.4から90.2へ小幅低下する。
list_summary: 生成トークンへの勾配寄与が小さい中間注意領域を層別に省き、長文脈prefillを再学習なしで高速化するTriangleMix。
authors:
- Zhiyuan He
- Yike Zhang
- Chengruidong Zhang
- Huiqiang Jiang
- Yuqing Yang
- Lili Qiu
published: '2025-07-29'
publication: arXiv preprint arXiv:2507.21526v4
publication_type: preprint
publication_status: preprint
source: https://arxiv.org/pdf/2507.21526
sources:
- https://arxiv.org/pdf/2507.21526
- https://arxiv.org/abs/2507.21526
code: https://aka.ms/TriangleMix
implementation: 著者は公開コードURLを提示。実測は長文脈LLMでの注意カーネル時間とend-to-end TTFT、RULER/LongBench/GSM-Infiniteの精度を含む。
worker_id: scheduled-chat-00
scheduled_slot: '00'
worker_run_key: 20261026-1400-scheduled-chat-00/r01
reference_main_sha: e9c03e35d41f2e71bf77e59a17030ac874e94ca5
worker_completed_at: '2026-10-26T14:00:00+09:00'
last_checked: '2026-10-26'
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
published_year: 2025
year: 2025
lineage: 99-other-inference-systems
implementation_status: research-prototype
last_audited: null
audit_version: 0
---

# Accelerating Prefilling via Decoding-time Contribution Sparsity — TriangleMix

## 概要

TriangleMixは長文脈の入力を処理するprefill段階で、すべての因果注意スコアを計算しなくても、その後の生成にほとんど影響しない領域があるという観察を利用する。重要なのは、注意スコアが小さい箇所を捨てる従来の疎注意とは異なり、**注意スコア自体は大きくても、プロンプト末尾以降の生成に寄与しない**領域を捨てる点である。原著はこれを生成時寄与の疎性（decoding-time contribution sparsity）と呼び、勾配による感度評価から層を選ぶ。

Llama-3.1-8B-Instructの128K入力では、三角形注意を適用した対象層の注意カーネルが750msから49msへ短縮（15.3倍）する。ただしモデル全層の計算が15.3倍になるわけではなく、モデル全体のTTFTは34.5秒から23.4秒（32%減）となる。RULERの4K〜128K平均は通常注意90.4、TriangleMix90.2で、同一ではなく0.2点の差がある。

## 問題設定

通常の因果注意は系列長 $N$ に対し $QK^T$ の二次元領域を計算する。MInference、FlexPrefill、XAttentionは入力に応じて重要なブロックを予測する動的疎注意を採用するが、どのブロックを計算するかを推定する追加コストがある。StreamingLLMのような固定窓は軽いが、長距離の検索に必要な情報まで捨てやすい。単に「スコアが高いブロックは重要」と見なすと、実際には後続の生成結果に寄与しない部分もprefillで計算してしまう。

論文は、プロンプトの各位置の注意スコアが将来のどの出力位置へ影響するかを、生成開始位置に関する勾配で分析する。具体的には注意行列をStreaming領域、Last Q–K領域、Middle Q–K領域へ分割する。StreamingとLast Q–Kは生成への寄与が大きい一方、Middle Q–Kは層によって寄与が著しく小さい。これは「過去のある注意が直後の予測には効くが、十分先の生成位置にはほとんど効かない」という影響範囲の局所性に対応する。

## 手法

### 1. 注意ブロックの生成時寄与を測る

入力はモデルの層別注意行列、因果マスク、および評価用のプロンプトである。通常注意は $A=\mathrm{Softmax}(QK^T/\sqrt d - c(1-M))$ で表される。論文は候補ブロックの注意スコアに対する生成開始トークンの感度を逆伝播で調べ、ブロックの寄与を測る。高い注意スコアと高い生成時寄与が必ずしも一致しないため、静的な大きさだけに基づく重要度推定では捉えられない層間差が得られる。

原著のSection 2.3では2,048トークンのプロンプトを用い、クエリ位置512〜1024に対応するブロックを落とした場合の困惑度を、直後の1024〜1152位置と末尾側の1920〜2048位置で比較する。Llama-3.1-8Bでは、全層で落とすと直後の困惑度8.31→8.76だが、半分の層だけ落とすと末尾側は7.81→7.82にとどまる。ここから「中間領域をどの層でも削除してよい」ではなく、「寄与の小さい層だけを選ぶべき」と結論する。

### 2. 寄与の小さい層だけ三角形注意へ切り替える

各層 $l_i$ についてMiddle Q–Kの生成時寄与 $Grad(M_{middle},l_i)$ を算出し、小さい順に $L_{tri}$ 層を選択する。選択層ではMiddle Q–Kを省略し、直近窓と先頭のsinkトークンを残す三角形状の固定注意を使う。残りの層は密な注意を維持する。選択層の計算量は系列長に対して二次から一次へ減ると論文は述べるが、全層が一次になるわけではない。

この層選択は、実行時にブロックのインデックスを推定する動的疎注意と異なり、モデルごとの事前勾配分析で固定される。実験ではLlama-3.1-8BとLlama-3-8B-262Kに16層、Qwen2.5-7Bに8層を設定した。sinkトークン8、局所窓512という条件も明示されている。異なるモデルで同じ層数を強制すると精度を失うため、層選択は再学習不要であっても事前の校正不要ではない。

### 3. 動的疎注意との組み合わせ

三角形注意を適用しない層を密な注意のまま残す代わりに、MInference、FlexPrefill、XAttentionへ置換できる。選択層は固定パターンのためブロック推定が不要で、他層は動的方式の適応性を使う。これにより、全層を動的方式にした場合より追加のprefill計算を減らせる。もっとも、動的方式の誤判定と三角形層の削除が同時に起きるため、組合せの精度が必ず改善するとは限らない。原著Table 3では、Qwen2.5のMInference単独RULER平均85.7に対し組合せ84.5へ下がる条件もある。

## 評価条件

| 軸 | 実験設定 |
|---|---|
| モデル | Llama-3.1-8B-Instruct、Llama-3-8B-Instruct-262K、Qwen2.5-7B-Instruct |
| 品質評価 | RULER 4K〜128K、LongBench、GSM-Infinite |
| 比較 | Dense、Streaming、Triangleのみ、StreamingMix、DuoAttention、MInference、FlexPrefill、XAttentionと各組合せ |
| 層数 | Llama系列 $L_{tri}=16$、Qwen2.5 $L_{tri}=8$（品質重視の設定） |
| 固定窓 | sink 8トークン、局所窓512トークン |
| 性能 | 注意カーネル時間（ms）とモデル全体のTTFT（秒）を分けて測定 |

## 評価結果と主要な発見

| 条件 | 比較方式 | TriangleMix/提案 | 解釈 |
|---|---|---|---|
| Llama-3.1-8B、RULER平均4K〜128K | Dense 90.4 | TriangleMix 90.2 | 平均0.2点低下。ほぼ同等だが完全一致ではない |
| Llama-3-8B-262K、同平均 | Dense 86.5 | TriangleMix 86.6 | 平均0.1点上回る |
| Qwen2.5-7B、同平均 | Dense 86.0 | TriangleMix 85.6 | 平均0.4点低下 |
| Llama-3.1-8B、128K、注意カーネル | Dense 750ms | Triangle 49ms | 選択層のカーネル15.3倍。モデル全体の倍率ではない |
| Llama-3.1-8B、32K、TTFT | Dense 4.1秒 | TriangleMix 3.6秒 | 12%短縮 |
| Llama-3.1-8B、128K、TTFT | Dense 34.5秒 | TriangleMix 23.4秒 | 32%短縮 |
| 同128K、MInference併用 | MInference 18.0秒 | 組合せ14.5秒 | 動的方式単独から約19%短縮 |
| Qwen2.5、RULER平均、MInference併用 | MInference 85.7 | 組合せ84.5 | 組合せによる精度低下の反例 |

原著Table 5は対象注意カーネル時間を、Table 6は全体TTFTを示す。128Kで15.3倍と32%減は別の計測対象であり、相互に換算してはいけない。RULER以外のGSM-Infiniteでは、Llama-3.1の平均0.076→0.074、Llama-3-262Kの0.060→0.060、Qwen2.5の0.161→0.169という結果があり、モデルによって符号が異なる。いずれも「すべてのタスクで完全に無損失」と断言できる証拠ではない。

## 感度評価・負の結果

Section 3.3では $L_{tri}$ を0から全層まで2層刻みで変え、RULER 64Kの精度を確認する。Llama-3.1-8BとLlama-3-8B-262Kは20層を置換しても原性能の99.7%、100.0%を維持する一方、Qwen2.5-7Bでは8層置換で98.2%を維持する程度である。モデル間の層別寄与構造が異なるため、固定層数や「半分の層」という設定を無条件に移植してはいけない。

Triangleのみを全層に適用した場合、Llama-3.1のRULER平均は72.7まで落ち、Dense90.4と大きく離れる。Streamingのみは36.5でさらに悪い。LongBenchではTriangle単独がPassageRetrievalで弱く、StreamingMixはTRECなど文脈内学習で弱いと論文は報告する。削除する中間注意は、浅い層で検索に必要なことがあるため、混合構成と層選択が性能保持の中心である。

また、128KのTTFTではTriangleMix単独23.4秒に対しMInference単独18.0秒のため、**TriangleMixが常に動的疎注意より速いわけではない**。組合せで14.5秒となることは、静的方式の補完性を示すが、実装複雑性や校正の追加費用を含む総コストは別途評価すべきである。

## 既存研究との差・実装上の注意

MInferenceなどは入力ごとの注意ブロック推定を行い、StreamingLLMは固定の先頭と局所窓だけを使う。DuoAttentionはヘッドごとに異なる注意形態を学習して使い分けるが、追加の学習が必要になる。TriangleMixは層単位の固定パターンを事前の勾配分析で選び、実行時の推定を避ける。テンソル並列時に同一層内のヘッドが異なるパターンとなるDuoAttentionの負荷不均衡を避けやすい点も原著は指摘する。

提案はprefillの注意計算を対象とし、KVキャッシュの長期保持量やdecodeの毎トークン帯域を直接削減する手法ではない。性能数値は長文脈を扱う特定のLLM、パターン、カーネル実装のもので、短文入力・別のGPU・異なるAttention実装で同じ倍率になるとは限らない。公式コードの配布先は著者が `https://aka.ms/TriangleMix` として提示している。

## 一次資料

- Zhiyuan He et al., *Accelerating Prefilling via Decoding-time Contribution Sparsity*, arXiv:2507.21526v4（PDFのヘッダーで2026-04-21改訂を確認）。`https://arxiv.org/pdf/2507.21526`。
- 根拠箇所: Section 2.2〜2.4（勾配、局所的影響、層選択）、Table 1（中間領域削除と困惑度）、Table 2〜4（精度）、Fig.6（層数感度）、Table 5（カーネル）、Table 6（TTFT）。
