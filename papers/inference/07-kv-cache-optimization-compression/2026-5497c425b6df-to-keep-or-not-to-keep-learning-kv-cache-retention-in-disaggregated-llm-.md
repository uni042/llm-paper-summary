---
canonical_id: DOI:10.1145/3793230.3837769
title: 'To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems'
summary: KVLearnはprefill/decode分離環境のKV保持を、再利用確率だけでなく再計算・ネットワーク転送・保存費用を含むオンライン意思決定として扱う。Prefix Reuse Predictor、Cost-Aware Retention Score、Adaptive Threshold Controllerを組み合わせ、TTFTをNo-Cache比最大56%、LRU-Pool比最大38%、Mooncake型比最大33%削減し、KV転送量を最大53%削減する。
list_summary: 再利用予測と再計算・転送・保存費用を統合してKV保持を決め、分離サービングのTTFTとKV転送量を削減する。
authors:
- Dong Liu
- Yanxuan Yu
- Eric Jiang
- Shu Wang
- Ying Nian Wu
published: 2026-09
publication: Proceedings of the 19th ACM International Systems and Storage Conference (SYSTOR 2026)
publication_type: conference
publication_status: published
source: https://doi.org/10.1145/3793230.3837769
sources:
- https://doi.org/10.1145/3793230.3837769
- https://github.com/FastLM/KVLearn
implementation: C++の公開実装をglobal KV pool coordinatorへ統合できる形で提供し、text/multimodal workload、A100校正値、200 Gbps級fabric設定を含む分離servingで評価。
code: https://github.com/FastLM/KVLearn
last_checked: '2026-10-04'
worker_completed_at: '2026-10-04T07:12:00+09:00'
worker_run_key: 20261004-0700-scheduled-chat-00/r01
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2308.12966
  arxiv_id: '2308.12966'
- canonical_id: arXiv:2510.09665
  arxiv_id: '2510.09665'
- canonical_id: DOI:10.52202/068431-1189
  doi: 10.52202/068431-1189
- canonical_id: DOI:10.1145/3149371
  doi: 10.1145/3149371
- canonical_id: arXiv:2401.18079
  arxiv_id: '2401.18079'
- canonical_id: arXiv:2403.05527
  arxiv_id: '2403.05527'
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: arXiv:2312.07533
  arxiv_id: '2312.07533'
- canonical_id: arXiv:2509.12211
  doi: 10.1145/3746027.3758181
- canonical_id: arXiv:2512.11920
  doi: 10.1145/3748173.3779188
- canonical_id: arXiv:2508.06526
  arxiv_id: '2508.06526'
- canonical_id: arXiv:2602.13357
  arxiv_id: '2602.13357'
- canonical_id: DOI:10.1145/3801487.3801812
  doi: 10.1145/3801487.3801812
- canonical_id: arXiv:2604.22901
  arxiv_id: '2604.22901'
- canonical_id: arXiv:2505.20353
  arxiv_id: '2505.20353'
- canonical_id: DOI:10.52202/075280-1516
  doi: 10.52202/075280-1516
- canonical_id: DOI:10.1145/3651890.3672274
  doi: 10.1145/3651890.3672274
- canonical_id: arXiv:2606.19746
  arxiv_id: '2606.19746'
- canonical_id: arXiv:2311.18677
  doi: 10.1109/isca59077.2024.00019
- canonical_id: arXiv:2407.00079
  arxiv_id: '2407.00079'
- canonical_id: DOI:10.5555/3277332.3277335
  doi: 10.5555/3277332.3277335
- canonical_id: arXiv:2309.17453
- canonical_id: arXiv:2405.16444
  arxiv_id: '2405.16444'
- canonical_id: arXiv:2512.18194
  arxiv_id: '2512.18194'
- canonical_id: DOI:10.1609/aaai.v33i01.33019127
  doi: 10.1609/aaai.v33i01.33019127
- canonical_id: arXiv:2306.14048
  doi: 10.52202/075280-1506
- canonical_id: DOI:10.52202/079017-2000
  doi: 10.52202/079017-2000
- canonical_id: arXiv:2401.09670
references_checked_at: '2026-10-04'
references_source: crossref-deposited-reference-metadata
references_total: 34
---

# To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems

## 概要

KVLearnは、プリフィル（プリフィル）とデコード（デコード）を別ノード プールへ分離するLLM サービングで、KV キャッシュを「残す／捨てる」判断を単なるLRUではなく期待コスト最小化として扱う。分離構成ではキャッシュ ミスのコストが同一device上の再計算だけではない。プリフィル ノードで接頭部を再計算した後、そのKV ブロックをデコード ノードへネットワーク転送する必要がある。一方で、再利用されないブロックを大域 KV プールへ保存すると、保存時の追加転送とメモリ占有を先払いしたまま無駄にする。

KVLearnは、将来の接頭部再利用確率を学習する接頭部 再利用 Predictor（PRP）、その確率を再計算・転送・保存コストへ変換するコスト-Aware Retention スコア（CARS）、プール 圧力とヒット状況に応じて保持閾値を変える適応型 閾値 Controller（ATC）の3要素を組み合わせる。モデル 重みや注意計算は変更せず、大域 KV プール coordinatorの受入れ/追い出し pathへ置く制御機構である。

## 問題設定

古典的なLRU/LFUは新しさ/frequencyを使うが、同じ再利用確率でもブロックの価値は同一ではない。長い接頭部、特にimage/video由来の大量トークンを含むマルチモーダル requestは、ミス時のプリフィル再計算が高価で、KV tensor自体も大きい。一方、高速ファブリックでは転送コストが下がるため、保存すべき再利用 閾値も変わる。

したがって保持判断には、将来再利用 確率、ミス時再計算 コスト、再利用時転送 コスト、プールに置き続けるストレージ opportunity コスト、現在のプール 占有率を同時に扱う必要がある。KVLearnはこれらをonlineに結び付ける。

## 手法

### 1. Prefix Reuse Predictor（PRP）

PRPはブロック `b` の構造・時間的特徴 `x(b)` から再利用確率 `P̂(b)=fθ(x(b))∈[0,1]` を出す軽量predictorである。公開実装の既定値ではfeature dimension 16、隠れ 大きさ 32の小さなネットワークを使い、LLM本体の隠れ 状態や重みには触れない。

再利用 ラベルは要求到着時には分からないので、追い出しや一定horizon経過後に「再利用された／されなかった」という遅延ラベルを得る。これをreplay bufferへ蓄積し、既定ではbuffer 20k、100 ラベルごとのmini-batchでoff-path更新する。静的traceから一度学習して固定するのではなく、ワークロードの再利用 パターンへオンライン追従する設計である。

### 2. Cost-Aware Retention Score（CARS）

KV ブロック 大きさは公開実装で `|b| = 2·ℓ·h_kv·d_h·L·δ` と見積もる。ミス時の再計算コスト `R(b)` は短接頭部のbandwidth-bound領域では `α_bw L`、長接頭部のcompute-bound領域では `α_flop L²`、再利用時転送 コストは `T(b)=|b|/β`、保持コストは `U(b)=γ|b|Δt` とする。

最終スコアは `CARS(b)=P̂(b)·(R(b)-T(b))-U(b,Δt)` で、ATCの閾値 `θ` を超えたブロックだけ保持する。これは「再利用されたときに回避できる再計算 minus 転送」の期待値から保存コストを引く。プリフィル コストがsuper-linearになる長い接頭部では、必要再利用 確率が低くても保持価値が上がる。逆にストレージ 圧力や転送 コストが高い場合はスコアが下がる。

### 3. Adaptive Threshold Controller（ATC）

CARSが同じでも、プールが空いている時と満杯に近い時で受入れ aggressivenessは変えるべきである。ATCはプール 占有率とヒット率をfeedbackとして保持 閾値をclosed-loop調整する。公開実装の既定値はtarget 占有率 `ρ*=0.85`、比例gain `Kp=2e-2`、積分gain `Ki=5e-4`、ヒット floor `0.55` である。

PRPは「再利用されそうか」、CARSは「再利用されるならどれだけ得か」、ATCは「今どれだけ厳しく入れるべきか」を担当し、予測・コスト modeling・resource 制御を分離する。

### 4. Serving stackへの統合

KVLearnはMooncake型の `P → S → D`、すなわちプリフィル・ストレージ/大域 プール・デコードの分離topologyを想定する。radix 接頭部 ヒットならlookup、ミス後にプリフィルしたブロックについてadmitを呼び、追い出し等から遅延ラベルをPRPへ返す。ATCはperiodic tickでプール状態を追跡する。

KVLearn自身はRDMA/NCCLによるtensor movementを実装しない。データ planeは既存stackへ任せ、制御 planeで保持/discard decisionだけを提供する。

## 評価条件

論文・公式実装はtextとマルチモーダル ワークロードの双方を対象とし、No-キャッシュ、LRU-プール、Mooncake-style disaggregated baseline、およびoracleに近い理想条件と比較する。主要指標は最初のトークンまでの時間（time to first トークン; TTFT）、inter-ノード KV 転送 volume、スループットである。

公式実装のコスト calibration例はA100 + LLaMA-3-8Bで、`α_bw≈0.026 ms/token`、`α_flop≈8×10^-6 ms/token²`、bandwidth/compute境界 `L×=512`。ファブリック既定値はInfiniBand HDR 200 Gbps相当の `β=25 GB/s` である。別GPU/モデル/ファブリックへ移す場合には再校正が必要になる。

## 主要結果

エンドツーエンド TTFTはNo-キャッシュ比で最大56%、LRU-プール比で最大38%、Mooncake-style分離baseline比で最大33%削減される。inter-ノード KV 転送 volumeはLRU-プール比で最大53%削減される。LRUが再利用されないブロックでも新しさでプールへ入れやすいのに対し、KVLearnは保存時の追加転送と将来価値を比較して受入れを抑えるためである。

マルチモーダルのMM-Session ワークロードではスループットがoracleの約5%以内に収まる。image/video由来の長い接頭部は再計算 コストが大きく、長さ依存コストをスコアへ明示的に入れる利点が出やすい。公式実装でも、プリフィルがsuper-linearになる領域では接頭部が長いほどoptimal 再利用 閾値が下がる設計になっている。

## 既存研究との差

LRU/LFUは新しさ/frequencyをproxyとして使うが、再計算 コスト・ファブリック bandwidth・ブロック 大きさを直接比較しない。Mooncake型のdisaggregated サービングはKVの分離保存・転送基盤を提供するが、「生成したブロックを保存すべきか」という受入れ policy自体は別問題である。

KVLearnは再利用 予測だけでもない。再利用 確率をシステム コストへ写像するCARSと、resource 圧力に応じてdecision 閾値を動かすATCを組み合わせ、予測精度とサービング objectiveを接続する。

## 限界

PRPは遅延ラベルから学ぶため、ワークロード distributionが急変した直後は過去パターンに引きずられる。CARSの `α_bw`、`α_flop`、`β`、ストレージ コスト係数はhardware/モデル/ネットワークごとに変わるため、別環境で無校正のまま同じ判断が最適とは限らない。

公開実装は保持/evict 制御に焦点を当て、RDMA/NCCL 転送 engine、KV 圧縮、モデル execution カーネルそのものは範囲外である。ネットワーク congestionやデータ-plane 実装が支配的な環境では受入れ policyだけではTTFTを十分に下げられない。headline改善値も特定ワークロード・topologyでの最大値であり、すべての再利用分布で同じ削減率を保証するものではない。

## 一次資料

- https://doi.org/10.1145/3793230.3837769
- https://github.com/FastLM/KVLearn
