---
canonical_id: DOI:10.1002/spe.3422
title: 'SubKV: Quantizing Long Context KV Cache for Sub-billion Parameter Language Models on Edge Devices'
summary: SubKVは小型LLMのキーをチャネル別、値をトークン別に低ビット量子化し、注意スコアに基づく動的FP16ウィンドウと先頭attention sinkの高精度保持を組み合わせる。H2O-Danube3-500Mの2ビットKVでWikiText2困惑度12.27（FP16
  11.68）を維持し、A800のShareGPT型負荷ではスループット1.39～2.17倍を報告する。ただしLongBenchでは2ビット化による精度低下がある。
list_summary: 小型LLMのKVを非対称2/4ビット量子化し、注意の強い直近トークンと先頭sinkをFP16で保護する。
authors:
- Ziqian Zeng
- Tao Zhang
- Zhengdong Lu
- Wenjun Li
- Huiping Zhuang
- Hongen Shao
- Sin G. Teo
- Xiaofeng Zou
published: '2025-04-01'
publication: 'Software: Practice and Experience, 55(8), 1287–1304'
publication_type: 査読付きジャーナル論文
publication_status: published
source: https://oar.a-star.edu.sg/storage/y/y32pddmzjq/software-practice-and-experience-1.pdf
sources:
- https://oar.a-star.edu.sg/storage/y/y32pddmzjq/software-practice-and-experience-1.pdf
- https://doi.org/10.1002/spe.3422
implementation: H2O-Danube3-500M、MobileLLM-600M/1B、TinyLlama-1.1B-chatでKVを量子化。主比較はgroup size 32、FP16残差window 32。LongBench、WikiText2、C4を評価。NVIDIA
  A800 80GBでShareGPT型負荷を合成し、最大バッチとスループットを実測。エッジ端末上の消費電力・遅延は未測定。
code: null
last_checked: '2026-10-30'
worker_id: scheduled-chat-00
scheduled_slot: '00'
worker_run_key: 20261030-2202-scheduled-chat-00/r01
worker_completed_at: '2026-10-30T22:11:00+09:00'
reference_main_sha: f62375f526e53e338a3ea74e689a900c4d224731
under16kb_reaudit_target_path: papers/inference/07-kv-cache-optimization-compression/2025-cf4ae1fdc15a-subkv-quantizing-long-context-kv-cache-for-sub-billion-parameter-languag.md
under16kb_reaudit_source_git_blob_sha: e4e8e056075434b30e580ab1fe155d0b3e8d398e
under16kb_reaudit_source_sha256: 2a9015c5c50d38afcaa3aab3e0f78746cffa156510554e1f98c459119c50c2f5
under16kb_reaudit_version: 2026-10-07-v1
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: '2026-10-30'
audit_version: 1
references:
- canonical_id: arXiv:2305.17118
- canonical_id: arXiv:2401.18079
- canonical_id: arXiv:2402.12065
- canonical_id: arXiv:2208.07339
- canonical_id: arXiv:2310.01801
- canonical_id: arXiv:2405.06219
- canonical_id: arXiv:2306.03078
- canonical_id: arXiv:2210.17323
- canonical_id: arXiv:2306.07629
- canonical_id: arXiv:2308.13137
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2403.01241
- canonical_id: DOI:10.1002/spe.3422
- canonical_id: arXiv:2305.13245
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.298
- canonical_id: arXiv:2402.02750
references_checked_at: '2026-10-30'
references_source: primary-pdf-reference-section
references_total: 62
---

# SubKV：小型LLMの長文脈KVを低ビット化し、重要な領域だけ高精度に保つ

## 概要

10億パラメータ前後の小型言語モデルは重み容量が比較的小さいが、生成が長くなると過去トークンの鍵・値（KV）キャッシュが増え、端末側のメモリを圧迫する。単純にKV全体を2ビットへ丸めると、鍵の一部チャネルにある外れ値や、最初のトークンに注意が集まる現象によって品質が大きく悪化する。ZengらのSubKVは、**鍵をチャネル別、値をトークン別に量子化する非対称な粒度**を採用し、直近の重要なトークンと先頭の注意集中領域を高精度で残す。

H2O-Danube3-500MのWikiText2困惑度はFP16の11.68に対し、2ビットSubKVで12.27、4ビットでは11.69だった。2ビットのKVメモリは最大5倍削減され、NVIDIA A800 80GB上のShareGPT型合成負荷では、バッチ容量が最大1.6倍、スループットが1.39～2.17倍となった。一方、2ビット化ではLongBench平均がモデルによって1ポイント以上低下し、個別の要約課題ではさらに大きな悪化がある。圧縮率・速度・品質を別々に確認する必要がある。

## 問題設定と設計上の観察

KVキャッシュは各注意層で過去トークンの鍵と値を保存する。モデル重みを4ビットへ圧縮しても、KVが16ビットのままなら文脈長に比例してメモリが増える。小型モデルでは重みが小さい分、長い文脈でKVが占める割合が大きくなる。低ビット化には尺度とゼロ点を決める単位が重要であり、全チャネルを同じ尺度で量子化すると一部の極端な値に分解能を奪われる。

著者らの分布観察では、鍵の外れ値は特定チャネルに偏り、値はトークンごとに分布が変わる。そのため鍵はチャネルごと、値はトークンごとに尺度を求める。さらに先頭トークンは注意の集中点（attention sink）として長く参照されるため、ここを2ビットへ丸めると誤差の影響が全体へ波及する。最近生成したトークンも、今後高い注意を受ける可能性があるので、直ちにすべて低ビット化するのは望ましくない。

## 手法

### 1. 鍵と値の非対称量子化

鍵キャッシュの同じチャネルを複数トークンにわたってまとめ、チャネル単位の最小・最大値から量子化尺度とゼロ点を決める。これにより外れ値を含むチャネルの大きな値域が、他チャネルの細かな変化を潰すことを防ぐ。値キャッシュは各トークンのチャネル集合を単位として量子化し、トークンごとの分布変化を扱う。両者を同じ粒度で量子化しないことが中心的な設計である。

鍵のチャネル別量子化には、生成が逐次進むという難しさがある。新しいトークンが来るたびに過去全体の尺度を計算し直すと、読み書き量が大きくなる。SubKVは鍵をGトークンごとのグループに区切り、完成したグループだけを低ビットで保持する。新しく到着した鍵は一時的なFP16領域に追加し、グループの境界が揃った時に量子化する。これによりオンライン生成でもチャネル別の尺度を扱える。

### 2. 三領域への分割と注意計算

KVを、最初のFトークンを保つ高精度領域、Gトークン単位で量子化した中央領域、直近Nトークンの高精度残差領域へ分割する。問い合わせQが来ると、三領域それぞれで鍵との内積を求め、注意スコアを連結して正規化する。量子化済み領域では尺度とゼロ点を使い、対応する値もトークン別に復元する。先頭と直近の領域はFP16で計算する。論文§3.5の式(5)～(9)は、この三領域の注意スコアを組み立てる処理を記述する。

この方式はモデル重みを再学習しないが、混合精度の注意演算とグループ管理を実装する必要がある。単にKVを2ビットの配列へ変換するだけでは、先頭保護や動的ウィンドウの効果を得られない。高精度領域の分だけ実際の圧縮率は16/2=8倍より小さくなる。

### 3. 動的ウィンドウ：注意スコアで残すトークンを選ぶ

新しい鍵が到着すると直近ウィンドウへ加え、softmax後の注意重みを参照する。新規トークンの注意スコアとウィンドウ端の古いトークンの注意スコアを比較し、新しい方が重要なら古い方を量子化済みグループへ送る。そうでなければ、重要度の低い新規トークンを直ちに量子化せず、ウィンドウを一時的に拡張する規則を使う。目的は固定長の最近傍保持ではなく、注意の強いトークンを高精度で長く保つことである。

ウィンドウが伸びればFP16の保持量が増え、圧縮率は下がる。注意スコアを参照するための演算と制御も必要である。どのトークンが将来も重要かを完全に予測できるわけではなく、GやNはモデルと負荷に応じて調整しなければならない。

### 4. 注意集中点の保護

最初のトークンをFP16で保持する領域は、直近の残差ウィンドウとは別に存在する。先頭が多くの問い合わせから参照される場合、ここを低ビット化すると注意重みの分布が不安定になる。H2O-Danube3-500Mの4k入力では、2ビットでsink保護なしのWikiText2困惑度12.54が、保護ありでは11.22へ改善する。4ビットでは10.61から10.58への小さな改善にとどまるため、低ビットほど重要な機構である。

## 評価条件

| 項目 | 原著の条件 | 解釈上の注意 |
|---|---|---|
| 対象モデル | H2O-Danube3-500M、MobileLLM-600M、MobileLLM-1B、TinyLlama-1.1B-chat | 7B以上やMoEは未評価 |
| 文脈長 | LongBenchでH2O-Danube3は最大8192、他は2048。困惑度比較は2048 | 超長文脈の保証ではない |
| 比較 | FP16、KIVI、KVQuant、SKVQ、SubKV-4bit/2bit | グループサイズ32、残差長32を基本に揃える |
| 品質 | LongBenchの8タスク、WikiText2・C4困惑度 | LongBench平均は異種指標の平均 |
| 速度 | NVIDIA A800 80GB、ShareGPT由来の合成負荷 | 入力平均161、出力平均338トークン |
| 感度 | sink保護の有無、グループ8/16/32、窓16/32/64/128 | 圧縮率と品質が非単調に変化 |

LongBenchのQasper、QMSum、MultiNews、TREC、TriviaQA、SAMSum、LCC、RepoBench-Pは、それぞれF1、ROUGE-L、正答率、コード類似度など異なる指標を使う。平均値を単一の正答率と解釈しない。最大バッチの比較はGPU全体の容量がほぼ同じ条件でのスループットであり、単一要求の遅延改善ではない。

## 主要結果

### LongBenchの平均品質

| モデル | FP16 | SubKV 4ビット | SubKV 2ビット | 2ビットの差 |
|---|---:|---:|---:|---:|
| H2O-Danube3-500M | 34.16 | 34.33 | 33.58 | -0.58 |
| MobileLLM-600M | 32.38 | 32.39 | 31.27 | -1.11 |
| MobileLLM-1B | 35.90 | 35.85 | 34.59 | -1.31 |
| TinyLlama-1.1B-chat | 36.13 | 36.08 | 34.61 | -1.52 |

原著Table 3。4ビットでは平均がほぼ維持されるが、2ビットでは全モデルで低下する。特にMobileLLM-1BのMultiNewsはFP16の13.21から2ビットで8.94へ低下する。平均が1.31ポイント低下したという要約だけでは、この個別の大きな悪化を捉えられない。H2O-Danube3のRepoBench-Pも28.51から25.63へ低下する。逆にH2O-Danube3のQMSumは18.74から19.04へわずかに上がるなど、課題ごとに方向が異なる。

### 困惑度と比較方式

H2O-Danube3-500MのWikiText2困惑度はFP16で11.68、SubKV-4bitで11.69、SubKV-2bitで12.27。2ビットではKIVIが13.42、KVQuantが17.58であり、SubKVの誤差が比較的小さい。TinyLlama-1.1B-chatでは4ビットのWikiText2/C4困惑度悪化がそれぞれ0.03/0.02、2ビットでは0.69/1.06と大きくなる。これは原著Table 4の結果であり、ビット幅を下げると全タスクで品質が維持されるという意味ではない。

### メモリ削減とスループット

H2O-Danube3-500Mの4k/8k文脈では、4ビットの困惑度がFP16とほぼ同等で、KV容量を最大3.31倍削減できる。2ビットでは困惑度の劣化を伴いながら最大5倍のKV容量削減となる（原著Fig.7）。これはKV部分の圧縮率であり、モデル重みやGPU全体のメモリを同じ倍率で削減するものではない。

原著Fig.8の速度測定では、単一A800 80GB上でH2O-Danube3-500Mを実行し、ShareGPT由来の平均入力161・平均出力338トークンの負荷を合成する。FP16とほぼ同じ最大GPUメモリ使用量で、SubKVは最大バッチを1.6倍まで増やし、スループットを1.39～2.17倍へ高める。利得の一部はバッチ容量が増えたことによる。端末の単一要求遅延やエネルギー効率をこの数値から推定してはならない。

### 構成要素除去：先頭保護とグループ・窓長

| 設定 | WikiText2困惑度 | C4困惑度 | 読み方 |
|---|---:|---:|---|
| 4ビット、sink保護なし | 10.61 | 13.93 | 先頭も量子化 |
| 4ビット、sink保護あり | **10.58** | **13.92** | 効果は小さい |
| 2ビット、sink保護なし | 12.54 | 14.98 | 大きな誤差 |
| 2ビット、sink保護あり | **11.22** | **14.28** | 特にWikiText2で1.32改善 |

原著Table 5。さらにTable 6でグループサイズ8/16/32を比較すると困惑度は14.11/10.87/11.03で、16が最良である。Table 7の窓長16/32/64/128では10.96/10.88/11.01/10.77で、128が最良、64が最悪だった。窓を広げれば必ず精度が上がるという単調な関係はない。固定のグループ・窓長をあらゆるモデルへそのまま適用するのは避けるべきである。

## 既存研究との差

KIVIも鍵をチャネル別、値をトークン別に量子化するが、SubKVは小型モデルでの分布と長文脈を中心に評価し、注意スコアに応じて高精度残差領域を調整する動的ウィンドウと、先頭の注意集中点を独立に保護する処理を組み合わせる。KVQuantやSKVQと同じビット幅・残差長で比較し、特に2ビット時の品質悪化を抑える。重み量子化とは別の処理であり、モデル重みが小さくてもKVが長文脈で支配的になる場合に有効である。

## 限界と実務上の注意

対象は500M～1.1Bの小型モデルで、最大文脈長はH2O-Danube3の8192、他は2048である。128k以上の長文脈、7B以上のLLM、MoE、端末NPUでの品質・速度は測定されていない。原著の限界節は、低ビット化が課題能力へ不均等に影響すること、追加の計算費用が発生すること、モバイル機器向けカーネル最適化が未完成であることを明記する。

速度測定はメモリ帯域が律速になりやすい生成段階を中心としており、プロンプト処理で大量のKVを一度に圧縮する際の性能は十分に評価されていない。長文脈の品質が平均的に維持されても、特定の要約・検索課題が悪化する可能性がある。実装を採用する場合は、2ビットの平均値だけでなく、個別タスク、先頭保護、窓長、実際のGPUカーネル、単一要求の遅延を独立に検証する必要がある。

## 一次資料

- [著者公開の査読済み全文PDF](https://oar.a-star.edu.sg/storage/y/y32pddmzjq/software-practice-and-experience-1.pdf)：§3の量子化・動的ウィンドウ・先頭保護、§4のTable 3～7、Fig.7～9、Limitationsを確認。
- [正式書誌](https://doi.org/10.1002/spe.3422)：Software: Practice and Experience、2025年4月1日公開。
