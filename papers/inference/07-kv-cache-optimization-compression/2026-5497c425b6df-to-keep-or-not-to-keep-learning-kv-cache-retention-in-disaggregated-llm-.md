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

KVLearnは、プリフィル（prefill）とデコード（decode）を別node poolへ分離するLLM servingで、KV cacheを「残す／捨てる」判断を単なるLRUではなく期待cost最小化として扱う。分離構成ではcache missのcostが同一device上の再計算だけではない。prefill nodeでprefixを再計算した後、そのKV blockをdecode nodeへnetwork転送する必要がある。一方で、再利用されないblockをglobal KV poolへ保存すると、保存時の追加転送とmemory占有を先払いしたまま無駄にする。

KVLearnは、将来のprefix再利用確率を学習するPrefix Reuse Predictor（PRP）、その確率を再計算・転送・保存costへ変換するCost-Aware Retention Score（CARS）、pool pressureとhit状況に応じてKEEP閾値を変えるAdaptive Threshold Controller（ATC）の3要素を組み合わせる。model weightやattention計算は変更せず、global KV pool coordinatorのadmission/eviction pathへ置く制御機構である。

## 問題設定

古典的なLRU/LFUはrecency/frequencyを使うが、同じ再利用確率でもblockの価値は同一ではない。長いprefix、特にimage/video由来の大量tokenを含むmultimodal requestは、miss時のprefill再計算が高価で、KV tensor自体も大きい。一方、高速fabricでは転送costが下がるため、保存すべきreuse thresholdも変わる。

したがって保持判断には、将来reuse probability、miss時recompute cost、reuse時transfer cost、poolに置き続けるstorage opportunity cost、現在のpool occupancyを同時に扱う必要がある。KVLearnはこれらをonlineに結び付ける。

## 手法

### 1. Prefix Reuse Predictor（PRP）

PRPはblock `b` の構造・時間的特徴 `x(b)` から再利用確率 `P̂(b)=fθ(x(b))∈[0,1]` を出す軽量predictorである。公開実装の既定値ではfeature dimension 16、hidden size 32の小さなnetworkを使い、LLM本体のhidden stateやweightには触れない。

reuse labelは要求到着時には分からないので、evictionや一定horizon経過後に「再利用された／されなかった」という遅延labelを得る。これをreplay bufferへ蓄積し、既定ではbuffer 20k、100 labelごとのmini-batchでoff-path更新する。静的traceから一度学習して固定するのではなく、workloadのreuse patternへオンライン追従する設計である。

### 2. Cost-Aware Retention Score（CARS）

KV block sizeは公開実装で `|b| = 2·ℓ·h_kv·d_h·L·δ` と見積もる。miss時の再計算cost `R(b)` は短prefixのbandwidth-bound領域では `α_bw L`、長prefixのcompute-bound領域では `α_flop L²`、reuse時transfer costは `T(b)=|b|/β`、保持costは `U(b)=γ|b|Δt` とする。

最終scoreは `CARS(b)=P̂(b)·(R(b)-T(b))-U(b,Δt)` で、ATCの閾値 `θ` を超えたblockだけKEEPする。これは「reuseされたときに回避できるrecompute minus transfer」の期待値から保存costを引く。prefill costがsuper-linearになる長いprefixでは、必要reuse probabilityが低くても保持価値が上がる。逆にstorage pressureやtransfer costが高い場合はscoreが下がる。

### 3. Adaptive Threshold Controller（ATC）

CARSが同じでも、poolが空いている時と満杯に近い時でadmission aggressivenessは変えるべきである。ATCはpool occupancyとhit率をfeedbackとしてKEEP thresholdをclosed-loop調整する。公開実装の既定値はtarget occupancy `ρ*=0.85`、比例gain `Kp=2e-2`、積分gain `Ki=5e-4`、hit floor `0.55` である。

PRPは「reuseされそうか」、CARSは「reuseされるならどれだけ得か」、ATCは「今どれだけ厳しく入れるべきか」を担当し、prediction・cost modeling・resource controlを分離する。

### 4. Serving stackへの統合

KVLearnはMooncake型の `P → S → D`、すなわちprefill・storage/global pool・decodeの分離topologyを想定する。radix prefix hitならlookup、miss後にprefillしたblockについてadmitを呼び、eviction等から遅延labelをPRPへ返す。ATCはperiodic tickでpool状態を追跡する。

KVLearn自身はRDMA/NCCLによるtensor movementを実装しない。data planeは既存stackへ任せ、control planeでkeep/discard decisionだけを提供する。

## 評価条件

論文・公式実装はtextとmultimodal workloadの双方を対象とし、No-Cache、LRU-Pool、Mooncake-style disaggregated baseline、およびoracleに近い理想条件と比較する。主要指標は最初のtokenまでの時間（time to first token; TTFT）、inter-node KV transfer volume、throughputである。

公式実装のcost calibration例はA100 + LLaMA-3-8Bで、`α_bw≈0.026 ms/token`、`α_flop≈8×10^-6 ms/token²`、bandwidth/compute境界 `L×=512`。fabric既定値はInfiniBand HDR 200 Gbps相当の `β=25 GB/s` である。別GPU/model/fabricへ移す場合には再校正が必要になる。

## 主要結果

end-to-end TTFTはNo-Cache比で最大56%、LRU-Pool比で最大38%、Mooncake-style分離baseline比で最大33%削減される。inter-node KV transfer volumeはLRU-Pool比で最大53%削減される。LRUがreuseされないblockでもrecencyでpoolへ入れやすいのに対し、KVLearnは保存時の追加転送と将来価値を比較してadmissionを抑えるためである。

multimodalのMM-Session workloadではthroughputがoracleの約5%以内に収まる。image/video由来の長いprefixはrecompute costが大きく、長さ依存costをscoreへ明示的に入れる利点が出やすい。公式実装でも、prefillがsuper-linearになる領域ではprefixが長いほどoptimal reuse thresholdが下がる設計になっている。

## 既存研究との差

LRU/LFUはrecency/frequencyをproxyとして使うが、recompute cost・fabric bandwidth・block sizeを直接比較しない。Mooncake型のdisaggregated servingはKVの分離保存・転送基盤を提供するが、「生成したblockを保存すべきか」というadmission policy自体は別問題である。

KVLearnはreuse predictionだけでもない。reuse probabilityをsystem costへ写像するCARSと、resource pressureに応じてdecision thresholdを動かすATCを組み合わせ、予測精度とserving objectiveを接続する。

## 限界

PRPは遅延labelから学ぶため、workload distributionが急変した直後は過去patternに引きずられる。CARSの `α_bw`、`α_flop`、`β`、storage cost係数はhardware/model/networkごとに変わるため、別環境で無校正のまま同じ判断が最適とは限らない。

公開実装はkeep/evict controlに焦点を当て、RDMA/NCCL transfer engine、KV compression、model execution kernelそのものは範囲外である。network congestionやdata-plane implementationが支配的な環境ではadmission policyだけではTTFTを十分に下げられない。headline改善値も特定workload・topologyでの最大値であり、すべてのreuse分布で同じ削減率を保証するものではない。

## 一次資料

- https://doi.org/10.1145/3793230.3837769
- https://github.com/FastLM/KVLearn
