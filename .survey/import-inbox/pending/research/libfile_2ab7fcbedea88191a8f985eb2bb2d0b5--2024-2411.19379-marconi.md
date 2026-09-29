---
canonical_id: "arXiv:2411.19379"
arxiv_id: "2411.19379"
title: "Marconi: Prefix Caching for the Era of Hybrid LLMs"
authors: ["Rui Pan","Zhuang Wang","Zhen Jia","Can Karakus","Luca Zancato","Tri Dao","Yida Wang","Ravi Netravali"]
published: 2024-11-28
publication_status: "Preprint"
lineage: "prefix caching / hybrid attention-SSM serving"
topics: ["prefix cache", "hybrid LLM", "SSM", "serving"]
summary: "MarconiはAttention層と状態空間モデル（SSM）層を混在させたHybrid LLM向け接頭辞キャッシュである。SSM状態は系列長にかかわらず固定サイズで逐次上書きされるため、Transformer KVのように任意位置で切って部分一致を再利用できず、単純LRUでは大きな状態を大量に保存して再利用率が落ちる。Marconiは将来の完全一致・部分一致の再利用可能性を見積もるadmissionと、節約FLOP/byteをrecencyへ加えるevictionを導入する。8×A100-40GB上のLMSys、ShareGPT、SWEBench等で、拡張vLLM比のtoken hit rateを平均4.5〜34.4倍にし、p95 TTFTを最大71.1%（617ms）削減した。"
list_summary: "部分切り出しできないSSM状態の再利用可能性と節約FLOP/byteを評価して、Hybrid LLMの接頭辞キャッシュへ入れる状態・追い出す状態を選ぶ。"
source: "https://arxiv.org/abs/2411.19379"
sources: ["https://arxiv.org/abs/2411.19379"]
code: "https://github.com/ruipeterpan/marconi"
worker_completed_at: "2026-09-29T23:58:00+09:00"
worker_run_key: "scheduled-chat-00-20260929T2355+0900"
reference_main_sha: "7a15c14afa8d2913bdc62695efd86faf4f9c5739"
---

# Marconi: Prefix Caching for the Era of Hybrid LLMs

> 部分切り出しできないSSM状態の再利用可能性と節約FLOP/byteを評価して、Hybrid LLMの接頭辞キャッシュへ入れる状態・追い出す状態を選ぶ。

## 概要

Transformerの接頭辞キャッシュは、共通プロンプトのKVを保存して次の要求でプリフィル計算を飛ばす。KVは系列次元を持つため、長い保存列の途中まで一致した場合でも一致部分だけ切り出して再利用できる。ところがAttention層と状態空間モデル（State Space Model; SSM）層を混在させたHybrid LLMでは、SSM状態が入力を順次畳み込んだ固定サイズ状態であり、途中時点へロールバックできない。

Marconiはこの性質を前提に、何でもキャッシュする方針をやめる。要求が将来どの種類の一致として再利用されそうかを分類してadmissionを制御し、evictionでは最終利用時刻だけでなく「その状態を再利用したときに節約できるFLOPをキャッシュ占有量で割った効率」を加味する。LMSys、ShareGPT、SWEBenchで拡張vLLM比のtoken hit rateを平均4.5倍、7.3倍、34.4倍へ引き上げ、p95の初回トークン時間（Time To First Token; TTFT）を最大71.1%、617ms削減した。

## 問題設定

HybridモデルではAttention層1に対してSSM層6〜10程度を挟む構成が使われる。SSMは長い系列でも状態サイズが一定で効率的だが、その状態は各トークンで上書きされる集約表現である。1000トークンまで処理した状態から800トークン時点の状態を切り出すことはできない。

そのため、既存Transformer向け接頭辞キャッシュをそのまま拡張すると、部分一致のたびにAttention KVは再利用できてもSSM状態は使えず、完全一致する系列終端の状態だけが有効になる。要求終了時の全状態を無条件に保存すると、大きなSSM状態が多数入り、将来完全一致しないエントリが容量を圧迫する。

## 手法のあらまし

Marconiは基数木（radix tree）で接頭辞を管理し、各ノードについて「再利用される可能性」と「再利用時に節約する計算量」を別々に評価する。新しい要求が終わったときは、将来の一致パターンから有用性が低い状態をそもそも入れない。容量不足時は、最終利用時刻とFLOP効率を組み合わせたutility scoreが低いノードから追い出す。

### Hybrid固有のadmission

Transformerでは長い系列の途中一致もKVの一部を使えるが、SSM状態はその位置と完全一致しなければ使えない。Marconiは要求履歴から、完全一致、既存接頭辞の延長、分岐などのヒット形態を区別し、保存候補がどの程度再利用されるかを推定する。再利用見込みが低い大きなSSM状態を無条件に入れないことで、同じ容量をヒット可能性の高い接頭辞へ回す。

この設計は単純LRUと異なり「最近使ったから保存」だけでは決めない。Hybridモデルでは一つのキャッシュエントリにAttention KVとSSM状態が混在し、同じバイト数でも再計算時のFLOP節約が系列長によって変わるためである。

### FLOP-aware eviction

各基数木ノードnに対し、`S(n)=recency(n)+α*flop_efficiency(n)` を計算する。`flop_efficiency` はそのノードを再利用したとき節約できる計算量を占有バイトで正規化した値で、recencyとともに0〜1へ正規化する。容量が必要になるとSが低いノードから順に削除する。

SSM状態は系列長が長くなっても固定サイズだが、長い接頭辞を再計算するとFLOP節約は大きい。そのためサイズだけを見る方式ではこの価値を表せない。Marconiは長い系列の状態を残しやすくし、短い系列のヒット率を一部犠牲にしても総計算節約を増やす。

### αのオンライン調整

αを固定するとワークロードごとに最適値が変わる。Marconiは起動時をLRU相当のα=0とし、最初のeviction後に基数木のスナップショットを取る。その後、最初のevictionまでに観測した要求数の5〜15倍をbootstrap期間として要求情報を記録する。

bootstrap後、CPUコア上で複数αをグリッド探索し、記録要求を再生してヒット率が最大になる値を選ぶ。探索は非同期で数秒程度、論文ではしばしば単一要求のプリフィル＋デコード時間より短い。したがってGPU推論を止めずにワークロード特性へ追従できるが、起動直後はLRU挙動になる。

## 評価

| 項目 | 代表設定 |
|---|---|
| サーバ | AWS p4d.24xlarge |
| GPU | 8× NVIDIA A100 40GB |
| CPU/DRAM | 96× Intel Xeon Platinum 8275CL、1152GB DDR4 |
| ワークロード | LMSys、ShareGPT、SWEBenchほか |
| モデル | Attention/SSM Hybrid、SSM-only、比率・状態次元を変えた構成 |
| 比較 | vLLM+、SGLang+（Hybrid対応へ拡張）、LRU |
| 指標 | token hit rate、FLOP savings、p95 TTFT |

| 条件 | 結果 | 読み取れること |
|---|---|---|
| LMSys | vLLM+比 hit rate 4.5倍 | 一般会話でもadmissionが無駄な状態を減らす |
| ShareGPT | 7.3倍 | 接頭辞再利用の多い会話負荷で利得拡大 |
| SWEBench | 34.4倍 | 数百〜数万tokenの広い長さ分布で特に有効 |
| FLOP-aware eviction | LRU比 hit rate +19.0〜219.7% | 長い接頭辞の計算価値を容量配分へ反映 |
| p95 TTFT | 最大71.1% / 617ms削減 | hit rate改善が実際の先頭応答遅延へつながる |
| 感度 | 長文脈、高SSM層比、大SSM状態ほど改善 | Hybrid固有の状態コストが強いほど効果大 |

## 既存研究との差

vLLMやSGLangのTransformer向け接頭辞キャッシュはKVをトークンブロックで管理し、LRU等で追い出せる。Hybridへ機械的に拡張すると、SSM状態の「途中を切り出せない」という性質を無視するため、キャッシュしたのに再利用できない状態が増える。

一般的なサイズ・コスト考慮キャッシュも、SSM状態では「サイズ一定なのに再計算FLOPは系列長で増える」ためサイズを価値の代理にできない。MarconiはHybridモデルの計算構造から節約FLOP/byteを明示的に算出する点で異なる。

## 限界・実装状況

起動直後は十分な履歴がなくα=0のLRUとして動くため、定常状態ほどの利得は得られない。bootstrapとCPU再生が必要で、急激にワークロード分布が変わる場合は過去履歴から選んだαが遅れて追従する。評価はA100クラスタと特定Hybrid構成が中心で、SSM以外の再帰層を持つ全モデルへ同じヒット率倍率を保証しない。長文脈・高SSM比ほど有利という結果は、逆に短文脈やAttention主体では改善幅が小さくなることを意味する。

## 一次資料

- https://arxiv.org/abs/2411.19379
- https://github.com/ruipeterpan/marconi