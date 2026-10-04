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
プリフィルとデコードを別ノード群へ分離するLLMサービングでは、KVキャッシュを残すか捨てるかの費用構造が単一GPUのLRUと異なる。missするとプリフィル再計算だけでなく、生成したKVをデコード側へネットワーク転送する。一方、再利用されないKVを大域 プールへ保存しても、作成時の転送とメモリ占有を無駄にする。KVLearnはこの判断をオンライン学習付きの費用最適化へ置き換える。

## 手法
Prefix Reuse Predictor（PRP）は接頭辞の構造・時間特徴16次元から将来再利用確率を予測する。モデル重みには触れず、追い出し等で後から得られる再利用 ラベルを再生 バッファへ蓄積し、軽量MLPをoff-path更新する。

Cost-Aware Retention Score（CARS）は予測確率だけでなく、ブロックを捨てた場合の再計算費用R、再利用時の転送費用T、保持中のストレージ費用Uを同じ尺度へ変換する。公開実装では概念的に `CARS=P_hat*(R-T)-U` とし、長い接頭辞ほど再計算費用が増えるため、同じ再利用確率でも保持価値が高くなる。

Adaptive Threshold Controller（ATC）はプール 占有率と命中状況を閉ループで観測し、KEEP判定閾値を調整する。固定閾値では通信量 局面やメモリ pressureが変わった際に過剰受入れ/過剰追い出しへ偏るためである。これによりPRPの予測値を直接離散 判定にせず、システム状態へ追従させる。

## 評価条件
|項目|条件|
|---|---|
|ワークロード|テキスト + マルチモーダル セッション|
|構成|globally disaggregated プリフィル/ストレージ/デコード|
|代表校正|A100 + LLaMA-3-8B|
|相互接続網既定|InfiniBand HDR 200 Gbps相当、25 GB/s|
|比較|No-Cache、LRU-Pool、Mooncake型、理想条件|
|指標|TTFT、KV transfer volume、スループット|

## 主要結果
KVLearnはエンドツーエンドの最初のトークンまでの時間（TTFT）をNo-Cache比最大56%、LRU-Pool比最大38%、Mooncake型分離比較対象比最大33%削減する。LRU-Pool比のノード間 KV transfer volumeは最大53%削減され、MM-Sessionではスループットが理想条件の約5%以内に収まる。つまり命中率だけを最大化するより、再計算・転送・保持費用を同時に考えた方が分離環境の実コストへ一致する。

## 既存研究との差
LRU/LFUは過去のアクセスを主に使い、接頭辞長による再計算費用やネットワーク 帯域を直接表現しない。KVLearnは将来再利用を学習し、同じ再利用確率でもブロック長や相互接続網条件で保持価値を変える。さらに閾値をメモリ pressureへ適応させるため、予測と資源 制御を分離している。

## 限界
PRPは過去ラベルから学ぶため、急なワークロード分布変化では予測が遅れる。コスト モデルの係数もGPU、モデル、ネットワークごとに校正が必要である。テンソル 転送自体はKVLearnの責務外であり、RDMA/NCCL データ転送面の性能が低ければルーティング 判定だけでは解消できない。

## 一次資料
- https://doi.org/10.1145/3793230.3837769
- https://github.com/FastLM/KVLearn