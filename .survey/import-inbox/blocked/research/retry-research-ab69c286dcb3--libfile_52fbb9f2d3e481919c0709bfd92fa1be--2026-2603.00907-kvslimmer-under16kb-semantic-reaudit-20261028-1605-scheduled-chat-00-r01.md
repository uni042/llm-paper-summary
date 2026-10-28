---
canonical_id: "arXiv:2603.00907"
arxiv_id: "2603.00907"
arxiv_categories:
  primary: "cs.CL"
  cross_list: []
title: "KVSlimmer: Theoretical Insights and Practical Optimizations for Asymmetric KV Merging"
authors:
  - Lianjun Liu
  - Hongli An
  - Weiqi Yan
  - Xin Du
  - Shengchuan Zhang
  - Huazhong Liu
  - Yunshan Zhong
published: "2026-03"
publication: "arXiv preprint arXiv:2603.00907v2"
publication_type: preprint
publication_status: "arXivプレプリントv2"
source: "https://arxiv.org/pdf/2603.00907"
sources:
  - "https://arxiv.org/pdf/2603.00907"
  - "https://arxiv.org/abs/2603.00907"
code: "https://github.com/lianjunl13-sudo/KVSlimmer"
implementation: "隣接Keyの交差Hessian項を含む二次近似の結合係数を前向きAttention変数から閉形式で求め、勾配逆伝播なしでKVチャンクを圧縮。A100上でLongBenchとLongBenchV2、実行時間・GPUメモリを比較する。"
summary: "KVSlimmerはQ/KとVの射影行列のスペクトル差から隣接トークンのKV非対称性を説明し、Key間の交差Hessianを考慮した前向き変数由来のマージ係数で逆伝播を不要にする。Llama3.1-8BのLongBench平均はAsymKV43.12から44.04へ改善し、A100上のAsymKV比で平均実行時間28%・チャンク512のピークメモリ約29%削減。ただしFull Context48.07には届かない。"
list_summary: "隣接Keyの交差Hessianを含むKVマージ係数を前向き計算から導出し、AsymKVの逆伝播費用を削減。LongBenchとA100で品質・時間・メモリの交換関係を測定する。"
last_checked: "2026-10-28"
worker_id: scheduled-chat-00
scheduled_slot: "00"
worker_run_key: "20261028-1605-scheduled-chat-00/r01"
worker_completed_at: "2026-10-28T16:05:10+09:00"
reference_main_sha: "dbf858b44c95f353af792ab4f176528ce6a08b85"
under16kb_reaudit_target_path: "papers/inference/99-other-inference-systems/2026-2603.00907-kvslimmer-theoretical-insights-and-practical-optimizations-for-asymmetri.md"
under16kb_reaudit_source_git_blob_sha: "995a848539cf9f1664bb8eb5580b8a87055cada1"
under16kb_reaudit_source_sha256: "130119b52c2f9c49b48e0ebec6a8a0bc1e12a2bc113e24d26e7bd056f8586bc3"
under16kb_reaudit_version: "2026-10-07-v1"
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
last_audited: null
audit_version: 0
---

# KVSlimmer：交差Hessianを扱う勾配不要の非対称KVマージ

## 概要

KVSlimmerは、長文脈LLMのKVキャッシュで隣接したKeyは似ているのにValueは異なる内容を運びやすいという非対称性を利用し、履歴トークンを少数の代表KVへ結合する方式である。既存のAsymKVはKeyの重要度を二次近似で求めるが、隣接Key間の交差Hessian項を省略し、勾配の逆伝播に依存する。KVSlimmerはAttentionの前向き変数から交差項を含む結合係数を導き、逆伝播を不要にする。さらにQ/K/V射影行列のスペクトル分布から、なぜKeyとValueの隣接類似性が異なるかを説明する。

NVIDIA A100 80GB上でLlama3.1-8B-InstructのLongBench平均はAsymKV43.12からKVSlimmer44.04へ0.92ポイント改善する。平均実行時間はAsymKV比0.72（約28%短縮）、チャンク512のピークGPUメモリは32.9GBから23.4GB（約29%削減）である。一方、非圧縮のLongBench48.07には届かず、要約・few-shotではAsymKVより悪い結果もある。**比較対象AsymKVに対する高速化・省メモリと、非圧縮との品質差を分けて評価すべき研究**である。

## 問題設定：削除と結合、KeyとValueの違い

長文脈の自己注意は、過去の各トークンについてKeyとValueを保存する。KV削除は不要と予測したトークンを捨てるためメモリを減らせるが、後で必要になっても復元できない。KVマージは複数トークンの情報を一つの代表表現へまとめるため、履歴の一部を残せる。ただし単純にKeyとValueを同じ重みで平均すると、似たKeyを圧縮しやすい利点と、異なるValueを混ぜて内容を壊す危険を区別できない。

AsymKVは隣接Keyの類似性を観測し、二次損失近似でKeyの重み付き結合を求める。一方ValueはKeyと異なる集約則を使う。しかし実装ではKey同士のHessian交差ブロックを省略し、勾配の二乗によるFisher型近似に頼るため、計算費用と近似誤差が生じる。KVSlimmerは射影行列の特異値の分布と入力の投影方向を使って非対称性を分析し、前向きAttentionのsoftmax・値・出力から交差項を含む結合係数を導く。隣接トークンを主対象とするため、遠く離れた意味的関連トークンの大域クラスタリングを行う方式ではない。

## 手法：スペクトル分析からマージ係数へ

### 1. Q/K/Vの隣接類似性を射影のスペクトルで説明する

入力の隠れ状態 `x_t` を射影行列Wで変換した `y_t=x_t W` を考える。隣接出力のコサイン類似度は、入力空間の誘導計量 `M=WW^T` で書き直せる。Wを特異値分解すると、Mの固有値はWの特異値の二乗となり、隣接類似度への各スペクトル成分の寄与を分解できる。上位固有値へエネルギーが集中すれば、入力の多くが共通の支配的方向へ写されやすい。

原著Figure 2ではLlama3.1-8BとMistral-7Bの層別解析により、Q/K射影は上位成分への集中が強く、隣接トークンの出力が似やすい。一方V射影のエネルギーは比較的分散し、隣接トークンの違いが保持されやすい。これは「任意の入力で必ずKeyが似る」という無条件の定理ではない。スペクトルの集中と入力が各方向へどう投影されるかの両方が類似度を決める。実測したモデル・層の傾向を一般化しすぎないことが重要である。

### 2. Key間の交差Hessianを省略しない

Attentionの出力は、各トークンの注意重みα_iとValue v_iの加重和 `o=Σ_i α_i v_i` である。Key k_iを変更すると、対応するlogitだけでなくsoftmaxの正規化を通して他トークンの注意重みも変わる。隣接する二つのKeyを代表Key k*へ置換するとき、損失の二次近似には各Key自身のHessianに加えて二つのKeyの交差ブロックが現れる。AsymKVの実用近似はこの交差項を捨てるが、KVSlimmerはsoftmaxの微分からその構造を導出する。

原著§4.1では、Keyに関するHessianブロックが `q q^T` と、注意重み、Value、Attention出力、損失の出力勾配からなるスカラー係数の積として表せることを示す。さらに隣接Keyの類似性に基づく関係を利用して、式33の閉形式の結合係数を得る。実装時には前向き計算で得られるα、v、oなどを使うため、AsymKVのように各マージで逆伝播を実行する必要がない。前向き変数だけで済むことがGPUメモリと時間の削減に結び付く。

ただしHessianの**微分式を正確に導いた**ことと、二次近似で得たマージ後の下流損失が厳密に最適であることは同義ではない。閉形式を簡約する際には隣接Keyが似るという経験的条件を用いる。異なる話題の境界や強く異質な隣接トークンでは近似が崩れる可能性がある。論文の「exact Hessian」は、その導出対象と仮定を明確にして読む必要がある。

### 3. Valueの集約とチャンク圧縮

KeyはHessian由来の重み付き結合を行い、Valueは情報の異質性を考慮した別の集約を行う。原著の出発点であるAsymKVではValueを単純加算し、Attentionの正規化と整合させる。KVSlimmerもKeyとValueを同じ係数で一律に平均するわけではない。圧縮時には、保存済みKVが予算を超えたところで隣接ペアを一定数まとめてマージし、キャッシュ長を予算まで戻すチャンク処理を使う。

標準実験は保存予算2048トークン、チャンク512、先頭32トークンの保持である。チャンクを大きくすると一度の圧縮で処理するペアが増え、メモリの一時ピークも大きくなり得る。KVSlimmerは逆伝播を省くため、AsymKVと比べてチャンクが大きいときのメモリ増加を抑えやすい。ただし全層の圧縮率は一律で、層別に最適な予算を自動配分する仕組みは実装していない。マージ後に元の個別トークンを完全に復元することもできない。

## 評価・主要結果

### 条件とLongBench

原著§5ではNVIDIA A100 80GB一枚、Llama3.1-8B-Instruct、Mistral-7B-Instruct-v0.3、Qwen2-1.5B-Instructを用いる。LongBenchは英語16課題で、単一文書・複数文書・要約・few-shot・合成・コードの各カテゴリを含む。比較はStreamingLLM、LongCache、H2O、LLMLingua-2、CaM、AsymKVなどである。H2Oには直近2048・重要512の別枠を設定しており、全方式が完全に同じ保持トークン数という意味ではない。結果は正答率・タスクスコアであり、GPU時間やメモリの指標とは別に読む。

| LongBench平均 | 非圧縮 | AsymKV | KVSlimmer | AsymKVとの差 |
|---|---:|---:|---:|---:|
| Llama3.1-8B-Instruct | 48.07 | 43.12 | 44.04 | +0.92 |
| Mistral-7B-Instruct-v0.3 | 46.15 | 40.88 | 41.28 | +0.40 |
| Qwen2-1.5B-Instruct | 34.29 | 31.98 | 32.45 | +0.47 |

Llama3.1-8Bでは合成課題がAsymKV39.39から44.52へ5.13ポイント改善する一方、要約は27.30から27.19、few-shotは65.66から65.00へ低下する。Mistralでも単一文書33.71→33.42、複数文書32.81→32.62、要約27.04→26.83と悪化する条件がある。平均では上回るが、すべての課題に優越するわけではない。非圧縮との差はLlamaで4.03ポイント、Mistralで4.87ポイント残る。

### LongBenchV2の難易度別結果

Llama3.1-8B、保存枠8192でLongBenchV2を評価する。AsymKV全体30.02に対しKVSlimmer30.22と僅かに改善するが、Hardは29.90→28.62、Mediumは27.44→25.12と悪化する。Easyは30.23→32.81、Shortは32.78→36.11、Longは28.85→30.56と改善し、全体平均を押し上げる。長文脈に強いという主張は、難問を含むすべての部分集合で強いという意味ではない。ベンチマークの入力長が最大2Mトークンを含むことと、GPUがその全トークンのKVを無圧縮保持することも別である。

### A100での実行時間とピークGPUメモリ

原著Figure 4のAsymKVに対するLongBench実行時間比は平均0.72、すなわち約28%短縮である。HotpotQAでは44%、MusiQue・NarrativeQA・PassageCountなどでは約38%短縮するが、GovReportやMultiNewsのような短いタスクでは差が小さい。逆伝播を不要にしたことが主な要因であり、**非圧縮KVに対する28%高速化を示した結果ではない**。

| チャンクサイズ | AsymKVピークGPUメモリ | KVSlimmerピーク | 差 |
|---|---:|---:|---:|
| 128 | 20.2GB | 17.4GB | 約14%削減 |
| 256 | 23.9GB | 19.1GB | 約20%削減 |
| 512 | 32.9GB | 23.4GB | 約29%削減 |
| 1024 | 57.5GB | 35.2GB | 約39%削減 |
| 1536 | AsymKVはOOM | 51.4GB | 実行可否の差 |

原著Figure 6は16課題平均のピークメモリで、チャンクが大きいほどAsymKVの逆伝播負荷が増すことを示す。Figure 7のHotpotQAで保持率10%にした条件ではAsymKV比で遅延約20%、メモリ約27%削減と報告する。保持率は元系列に対する保存トークン比であり、生成速度や正答率のパーセントではない。これらは条件ごとの実測であり、他のGPU・異なるバッチへ同じ倍率をそのまま適用できない。

## 限界・負の結果

KVSlimmerはAsymKVより軽量だが、隣接Keyの類似性という観測的性質を利用する。意味的に近いトークンが離れている場合や、隣接トークンの内容が急に変わる場合の最適なマージを保証しない。二次近似の損失と実際の生成品質は同じではなく、マージしたKVから元の情報を完全に復元できない。原著§6は、非隣接・大域的なマージと層別圧縮率の最適化を今後の課題としている。

平均精度の改善は0.40〜0.92ポイント程度で、LongBenchV2のHard/MediumやLongBenchの要約・few-shotでは負の結果がある。速度とメモリの大きな改善は、比較対象AsymKVの逆伝播費用が大きいことに依存する。勾配不要の他方式や、専用カーネルを用いた別のKV圧縮方式に対して同じ利得があるとは確認できない。非圧縮の品質との差を残したまま、運用上のGPUメモリ・待ち時間を削減する選択肢として評価すべきである。

## 一次資料と再監査範囲

- Lianjun Liu et al., *KVSlimmer: Theoretical Insights and Practical Optimizations for Asymmetric KV Merging*, arXiv:2603.00907v2, https://arxiv.org/pdf/2603.00907
- 公式コード：https://github.com/lianjunl13-sudo/KVSlimmer
- 原著§3（スペクトル分解と隣接類似性）、§4（交差Hessianと閉形式の結合）、§5の表1・2、Figure 4〜7（LongBench、LongBenchV2、A100実測）、§6（非隣接マージと層別予算の限界）を照合。
