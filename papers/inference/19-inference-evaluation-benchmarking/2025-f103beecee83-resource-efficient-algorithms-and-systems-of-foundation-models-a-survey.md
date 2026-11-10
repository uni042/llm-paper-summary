---
canonical_id: DOI:10.1145/3706418
doi: 10.1145/3706418
title: 'Resource-efficient Algorithms and Systems of Foundation Models: A Survey'
authors:
- Mengwei Xu
- Dongqi Cai
- Wangsong Yin
- Shangguang Wang
- Xin Jin
- Xuanzhe Liu
published: '2025-01-09'
publication: ACM Computing Surveys 57(5), Article 110, 39 pages
publication_type: peer-reviewed journal survey
publication_status: published
source: https://www.caidongqi.com/pdf/CSUR25-llm-survey.pdf
sources:
- https://www.caidongqi.com/pdf/CSUR25-llm-survey.pdf
- https://doi.org/10.1145/3706418
implementation: 独立した新規推論システムではなく、2024年頃までの基盤モデルの構造・圧縮・学習・クラウド/エッジ推論のアルゴリズムと実装を比較分類したサーベイ。表3に当時の推論基盤を整理するが、本論文自体の実装はない。
code: null
last_checked: '2026-10-25'
worker_completed_at: '2026-10-25T21:30:00+09:00'
worker_id: scheduled-chat-30
worker_run_key: 20261025-2130-scheduled-chat-30/r01
reference_main_sha: 4c59610190aa807694851df13fbca80e49813f19
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
returned_research_repair: true
returned_research_source_path: .survey/import-inbox/blocked/research/retry-research-ef1d16605523--0-libfile_406b0fe2d7dc8191970f3f0f7f0a0ff6--start-snapshot-20261024.md
summary: 2025年のACM Computing Surveys掲載サーベイ。基盤モデルの計算・メモリ費用を構造、アルゴリズム、システムの3層に分け、注意近似・MoE・早期終了、量子化/枝刈り、KVキャッシュ、クラウドのprefill/decode分離、エッジのCPU/GPUオフロードまでを統一的に整理する。独自ベンチマークではなく各引用研究の異なる条件の数値を紹介しており、例えばH2Oの最大1.9倍の遅延改善と29倍のスループットは同一条件の一括測定値として解釈できない。2024年までの研究を中心とするため、2026年の実装選定には後続研究と現行コードの再確認が必要。
list_summary: 基盤モデルの効率化を構造・圧縮アルゴリズム・クラウド/エッジシステムに分解し、KV・MoE・量子化・推論スケジューリングを横断整理した39ページの査読サーベイ。
references:
- canonical_id: arXiv:2401.08671
- canonical_id: arXiv:2306.13649
  arxiv_id: '2306.13649'
- canonical_id: arXiv:2403.02310
- canonical_id: arXiv:2308.16369
  arxiv_id: '2308.16369'
- canonical_id: arXiv:2312.11514
  arxiv_id: '2312.11514'
- canonical_id: arXiv:2207.00032
- canonical_id: arXiv:2305.15805
  arxiv_id: '2305.15805'
- canonical_id: arXiv:2310.05424
  arxiv_id: '2310.05424'
- canonical_id: arXiv:2012.15701
  arxiv_id: '2012.15701'
- canonical_id: arXiv:2106.15183
  arxiv_id: '2106.15183'
- canonical_id: arXiv:2308.14711
  arxiv_id: '2308.14711'
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: arXiv:2304.11062
  arxiv_id: '2304.11062'
- canonical_id: arXiv:2205.14756
  arxiv_id: '2205.14756'
- canonical_id: arXiv:2305.17530
  arxiv_id: '2305.17530'
- canonical_id: DOI:10.1145/3706418
- canonical_id: arXiv:2306.07967
  arxiv_id: '2306.07967'
- canonical_id: arXiv:2307.13304
  arxiv_id: '2307.13304'
- canonical_id: DOI:10.48550/arxiv.2302.01318
- canonical_id: arXiv:2103.14899
  arxiv_id: '2103.14899'
- canonical_id: arXiv:2310.18167
  arxiv_id: '2310.18167'
- canonical_id: arXiv:2111.00160
  arxiv_id: '2111.00160'
- canonical_id: arXiv:2309.12307
  arxiv_id: '2309.12307'
- canonical_id: arXiv:2110.07814
  arxiv_id: '2110.07814'
- canonical_id: arXiv:2305.14788
  arxiv_id: '2305.14788'
- canonical_id: arXiv:2307.08691
  arxiv_id: '2307.08691'
- canonical_id: arXiv:2205.14135
- canonical_id: arXiv:2212.14052
  arxiv_id: '2212.14052'
- canonical_id: arXiv:2311.03748
  arxiv_id: '2311.03748'
- canonical_id: arXiv:2307.02628
  arxiv_id: '2307.02628'
- canonical_id: arXiv:2208.07339
  arxiv_id: '2208.07339'
- canonical_id: arXiv:2305.14314
  arxiv_id: '2305.14314'
- canonical_id: arXiv:2306.03078
  arxiv_id: '2306.03078'
- canonical_id: arXiv:2307.02486
  arxiv_id: '2307.02486'
- canonical_id: arXiv:2312.00678
  arxiv_id: '2312.00678'
- canonical_id: arXiv:2301.00234
  arxiv_id: '2301.00234'
- canonical_id: arXiv:2010.11929
  arxiv_id: '2010.11929'
- canonical_id: arXiv:2112.06905
- canonical_id: arXiv:2309.17425
  arxiv_id: '2309.17425'
- canonical_id: arXiv:2101.03961
- canonical_id: arXiv:2103.14636
- canonical_id: arXiv:2301.00774
- canonical_id: arXiv:2210.17323
  arxiv_id: '2210.17323'
- canonical_id: arXiv:2301.12726
  arxiv_id: '2301.12726'
- canonical_id: arXiv:2304.14108
  arxiv_id: '2304.14108'
- canonical_id: arXiv:2307.06945
  arxiv_id: '2307.06945'
- canonical_id: arXiv:2001.08950
  arxiv_id: '2001.08950'
- canonical_id: arXiv:2312.00752
  arxiv_id: '2312.00752'
- canonical_id: arXiv:2111.00396
  arxiv_id: '2111.00396'
- canonical_id: arXiv:2306.08543
  arxiv_id: '2306.08543'
- canonical_id: DOI:10.1145/3579371.3589038
  doi: 10.1145/3579371.3589038
- canonical_id: arXiv:2310.10700
  arxiv_id: '2310.10700'
- canonical_id: arXiv:2002.10941
  arxiv_id: '2002.10941'
- canonical_id: arXiv:1510.00149
  arxiv_id: '1510.00149'
- canonical_id: arXiv:1506.02626
  arxiv_id: '1506.02626'
- canonical_id: arXiv:2402.12354
  arxiv_id: '2402.12354'
- canonical_id: arXiv:2311.01906
  arxiv_id: '2311.01906'
- canonical_id: arXiv:2310.03270
  arxiv_id: '2310.03270'
- canonical_id: arXiv:2310.07702
  arxiv_id: '2310.07702'
- canonical_id: arXiv:2212.10071
  arxiv_id: '2212.10071'
- canonical_id: arXiv:2311.01282
  arxiv_id: '2311.01282'
- canonical_id: arXiv:2305.02301
  arxiv_id: '2305.02301'
- canonical_id: arXiv:2305.11234
  arxiv_id: '2305.11234'
- canonical_id: arXiv:2104.02112
  arxiv_id: '2104.02112'
- canonical_id: arXiv:2207.05557
  arxiv_id: '2207.05557'
- canonical_id: arXiv:2312.08901
  arxiv_id: '2312.08901'
- canonical_id: arXiv:2212.10670
  arxiv_id: '2212.10670'
- canonical_id: arXiv:2102.08124
  arxiv_id: '2102.08124'
- canonical_id: arXiv:2206.03382
- canonical_id: arXiv:2310.05736
  arxiv_id: '2310.05736'
- canonical_id: arXiv:2311.11514
  arxiv_id: '2311.11514'
- canonical_id: arXiv:2310.01655
  arxiv_id: '2310.01655'
- canonical_id: arXiv:2001.08361
  arxiv_id: '2001.08361'
- canonical_id: arXiv:2309.14021
  arxiv_id: '2309.14021'
- canonical_id: arXiv:2010.07003
  arxiv_id: '2010.07003'
- canonical_id: arXiv:2305.14152
  arxiv_id: '2305.14152'
- canonical_id: arXiv:2306.07629
  arxiv_id: '2306.07629'
- canonical_id: arXiv:2302.14017
  arxiv_id: '2302.14017'
- canonical_id: arXiv:2304.02643
  arxiv_id: '2304.02643'
- canonical_id: arXiv:2212.05055
  arxiv_id: '2212.05055'
- canonical_id: arXiv:2308.15030
  arxiv_id: '2308.15030'
- canonical_id: arXiv:2112.13890
  arxiv_id: '2112.13890'
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: arXiv:2109.04838
  arxiv_id: '2109.04838'
- canonical_id: arXiv:2306.02272
  arxiv_id: '2306.02272'
- canonical_id: arXiv:2306.00317
  arxiv_id: '2306.00317'
- canonical_id: arXiv:2104.08691
  arxiv_id: '2104.08691'
- canonical_id: arXiv:2211.17192
- canonical_id: arXiv:2309.10020
  arxiv_id: '2309.10020'
- canonical_id: arXiv:2203.14509
  arxiv_id: '2203.14509'
- canonical_id: arXiv:2203.07814
- canonical_id: arXiv:2209.15200
  arxiv_id: '2209.15200'
- canonical_id: arXiv:2306.00980
  arxiv_id: '2306.00980'
- canonical_id: arXiv:2401.05459
  arxiv_id: '2401.05459'
- canonical_id: arXiv:2310.08659
  arxiv_id: '2310.08659'
- canonical_id: arXiv:2306.11222
  arxiv_id: '2306.11222'
- canonical_id: arXiv:2206.01191
  arxiv_id: '2206.01191'
- canonical_id: arXiv:2305.16742
  arxiv_id: '2305.16742'
- canonical_id: arXiv:2306.00477
  arxiv_id: '2306.00477'
- canonical_id: arXiv:2306.00978
  arxiv_id: '2306.00978'
- canonical_id: arXiv:2309.04965
  arxiv_id: '2309.04965'
- canonical_id: arXiv:2310.08041
  arxiv_id: '2310.08041'
- canonical_id: arXiv:2202.09778
  arxiv_id: '2202.09778'
- canonical_id: arXiv:2302.02210
  arxiv_id: '2302.02210'
- canonical_id: arXiv:2402.09353
  arxiv_id: '2402.09353'
- canonical_id: arXiv:2305.07027
  arxiv_id: '2305.07027'
- canonical_id: DOI:10.1007/s11432-021-3528-7
  doi: 10.1007/s11432-021-3528-7
- canonical_id: arXiv:2305.17118
  arxiv_id: '2305.17118'
- canonical_id: arXiv:2305.17888
  arxiv_id: '2305.17888'
- canonical_id: arXiv:2310.17157
- canonical_id: arXiv:2409.15790
  arxiv_id: '2409.15790'
- canonical_id: arXiv:2305.11627
  arxiv_id: '2305.11627'
- canonical_id: arXiv:2209.10655
  arxiv_id: '2209.10655'
- canonical_id: arXiv:2110.02178
  arxiv_id: '2110.02178'
- canonical_id: arXiv:2404.02948
  arxiv_id: '2404.02948'
- canonical_id: arXiv:2111.15668
  arxiv_id: '2111.15668'
- canonical_id: arXiv:2312.15234
  arxiv_id: '2312.15234'
- canonical_id: arXiv:2305.09781
  arxiv_id: '2305.09781'
- canonical_id: arXiv:2311.15566
  arxiv_id: '2311.15566'
- canonical_id: arXiv:2110.15943
  arxiv_id: '2110.15943'
- canonical_id: arXiv:2305.16300
  arxiv_id: '2305.16300'
- canonical_id: arXiv:2305.16820
  arxiv_id: '2305.16820'
- canonical_id: arXiv:2104.04473
- canonical_id: arXiv:2211.09761
  arxiv_id: '2211.09761'
- canonical_id: arXiv:2304.03946
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: arXiv:2303.06349
  arxiv_id: '2303.06349'
- canonical_id: arXiv:2205.03436
  arxiv_id: '2205.03436'
- canonical_id: arXiv:2111.11124
  arxiv_id: '2111.11124'
- canonical_id: arXiv:2311.18677
  arxiv_id: '2311.18677'
- canonical_id: arXiv:2212.09748
  arxiv_id: '2212.09748'
- canonical_id: arXiv:2305.13048
  arxiv_id: '2305.13048'
- canonical_id: arXiv:2401.04081
  arxiv_id: '2401.04081'
- canonical_id: arXiv:2302.10866
  arxiv_id: '2302.10866'
- canonical_id: arXiv:2211.05102
- canonical_id: arXiv:2310.02409
  arxiv_id: '2310.02409'
- canonical_id: arXiv:1910.02054
- canonical_id: arXiv:2106.02034
  arxiv_id: '2106.02034'
- canonical_id: arXiv:2101.06840
- canonical_id: arXiv:2310.11028
  arxiv_id: '2310.11028'
- canonical_id: arXiv:2302.03773
  arxiv_id: '2302.03773'
- canonical_id: arXiv:2311.03285
  arxiv_id: '2311.03285'
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2301.13741
  arxiv_id: '2301.13741'
- canonical_id: arXiv:2010.02502
  arxiv_id: '2010.02502'
- canonical_id: arXiv:2312.12456
  arxiv_id: '2312.12456'
- canonical_id: arXiv:2306.11695
  arxiv_id: '2306.11695'
- canonical_id: arXiv:2307.08621
  arxiv_id: '2307.08621'
- canonical_id: arXiv:2310.15141
  openreview_id: d0mGsaheuT
- canonical_id: arXiv:2011.14203
  arxiv_id: '2011.14203'
- canonical_id: arXiv:2203.10705
  arxiv_id: '2203.10705'
- canonical_id: arXiv:2308.02019
  arxiv_id: '2308.02019'
- canonical_id: arXiv:2109.06952
  arxiv_id: '2109.06952'
- canonical_id: arXiv:2012.12877
  arxiv_id: '2012.12877'
- canonical_id: arXiv:2307.09288
  arxiv_id: '2307.09288'
- canonical_id: arXiv:2310.19975
  arxiv_id: '2310.19975'
- canonical_id: arXiv:2306.04050
  arxiv_id: '2306.04050'
- canonical_id: arXiv:2303.14189
  arxiv_id: '2303.14189'
- canonical_id: arXiv:2311.17049
  arxiv_id: '2311.17049'
- canonical_id: arXiv:2305.16701
  arxiv_id: '2305.16701'
- canonical_id: arXiv:2312.03863
  arxiv_id: '2312.03863'
- canonical_id: arXiv:2310.11453
  arxiv_id: '2310.11453'
- canonical_id: arXiv:2012.09852
  doi: 10.1109/hpca51647.2021.00018
- canonical_id: arXiv:2006.04768
  arxiv_id: '2006.04768'
- canonical_id: arXiv:2312.04793
  arxiv_id: '2312.04793'
- canonical_id: arXiv:2304.03284
  arxiv_id: '2304.03284'
- canonical_id: arXiv:2210.17451
  arxiv_id: '2210.17451'
- canonical_id: DOI:10.1145/3600006.3613145
- canonical_id: arXiv:2304.09145
  arxiv_id: '2304.09145'
- canonical_id: arXiv:2308.15272
  arxiv_id: '2308.15272'
- canonical_id: arXiv:2210.03162
  arxiv_id: '2210.03162'
- canonical_id: arXiv:2305.05920
  arxiv_id: '2305.05920'
- canonical_id: arXiv:2310.06694
  arxiv_id: '2310.06694'
- canonical_id: arXiv:2201.00520
  arxiv_id: '2201.00520'
- canonical_id: arXiv:2211.10438
  arxiv_id: '2211.10438'
- canonical_id: arXiv:2309.17453
  arxiv_id: '2309.17453'
- canonical_id: arXiv:2004.12993
  arxiv_id: '2004.12993'
- canonical_id: arXiv:2309.04255
  arxiv_id: '2309.04255'
- canonical_id: arXiv:2407.05858
  arxiv_id: '2407.05858'
- canonical_id: arXiv:2307.00526
  arxiv_id: '2307.00526'
- canonical_id: arXiv:2401.08092
  arxiv_id: '2401.08092'
- canonical_id: arXiv:2309.14717
  arxiv_id: '2309.14717'
- canonical_id: DOI:10.1007/s11432-024-4227-2
  doi: 10.1007/s11432-024-4227-2
- canonical_id: arXiv:2311.10986
  arxiv_id: '2311.10986'
- canonical_id: arXiv:2304.13712
  arxiv_id: '2304.13712'
- canonical_id: arXiv:2309.15275
  arxiv_id: '2309.15275'
- canonical_id: arXiv:2310.16836
  arxiv_id: '2310.16836'
- canonical_id: arXiv:2206.01861
- canonical_id: DOI:10.18653/v1/2021.naacl-main.463
  arxiv_id: '2105.11618'
- canonical_id: arXiv:2308.14352
  arxiv_id: '2308.14352'
- canonical_id: arXiv:2411.05046
  arxiv_id: '2411.05046'
- canonical_id: arXiv:2112.07658
  arxiv_id: '2112.07658'
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: DOI:10.1145/3636534
  doi: 10.1145/3636534
- canonical_id: arXiv:2304.01089
  arxiv_id: '2304.01089'
- canonical_id: arXiv:2007.14062
- canonical_id: arXiv:2111.09881
  arxiv_id: '2111.09881'
- canonical_id: arXiv:2401.03868
  arxiv_id: '2401.03868'
- canonical_id: arXiv:2105.14103
  arxiv_id: '2105.14103'
- canonical_id: arXiv:2210.03052
- canonical_id: arXiv:2309.08168
- canonical_id: arXiv:2305.18403
  arxiv_id: '2305.18403'
- canonical_id: arXiv:2110.01786
- canonical_id: arXiv:2306.14048
  arxiv_id: '2306.14048'
- canonical_id: arXiv:2204.04362
  arxiv_id: '2204.04362'
- canonical_id: arXiv:2304.11277
  arxiv_id: '2304.11277'
- canonical_id: arXiv:2310.19102
  arxiv_id: '2310.19102'
- canonical_id: arXiv:2311.16567
  arxiv_id: '2311.16567'
- canonical_id: arXiv:2312.07104
  arxiv_id: '2312.07104'
- canonical_id: arXiv:2006.04152
- canonical_id: arXiv:2308.07633
  arxiv_id: '2308.07633'
- canonical_id: arXiv:2309.02411
  arxiv_id: '2309.02411'
- canonical_id: arXiv:2001.04451
references_checked_at: '2026-11-10'
references_source: primary-pdf-reference-section
last_audited: null
audit_version: 0
references_total: 318
---

# Resource-efficient Algorithms and Systems of Foundation Models — 基盤モデル効率化の階層横断サーベイ

## 概要

Xu・Cai・Yin・Wang・Jin・Liuによる39ページの査読付きサーベイは、基盤モデルの「効率」を単一のモデル圧縮率やGPU演算速度として扱わず、**モデル構造、学習・圧縮・推論アルゴリズム、実行システム**という異なる介入点に分解する。対象は言語モデルだけでなくViT、拡散モデル、画像・言語の複合モデルに及ぶ。LLM推論基盤にとって重要なのは、同じ重みの圧縮でも、GPU上に収まること、KVキャッシュを保持すること、長い入力をprefillすること、1トークンずつdecodeすることでは支配的な費用が異なると示している点である。論文は2025年1月刊行だが、主に2024年までの研究を対象とする。〔原著§1、§2、§4.3–4.4、§5〕

本論文は新しいスケジューラや量子化器を実装して測定した研究ではない。後述する最大1.9倍、29倍、5倍などの値は**それぞれ引用元論文の条件下で報告された値**であり、本サーベイが同じGPU・同じモデル・同じ入力長で再測定した横並び比較ではない。この区別を保つことが、LLM推論フレームワークの選定やローカルGPUへの適用判断に不可欠である。〔原著§4.3、表1–3、§5.3–5.4〕

## 問題設定と対象範囲

著者は物理的資源を主対象とし、GPU/TPU計算、HBM/DRAM、永続ストレージ、ネットワーク帯域を分析する。訓練データ数とプライバシーは「資源」の主定義から外すが、エッジ展開の課題としてプライバシーを議論する。選定対象は主としてCSRankings収録会議と、影響力があると判断したarXiv論文であり、2020年以降の文献を中心に構成される。ハードウェア回路の全領域を網羅するものではなく、アルゴリズムとシステムの工夫が中心である。〔原著§1 Scope and Rationales〕

同じTransformerでも入力系列長を `T`、隠れ次元を `d` とすると、原著§2は注意計算を概ね `O(T²d)`、FFNを `O(Td²)` と整理する。これらは演算量の次数であり、実時間の優劣を直接決めない。短いdecodeでは過去KVの読み込みが律速になりやすく、長いprefillでは行列演算・注意計算が大きい。GPU演算性能、メモリ帯域、CPU/GPU転送、バッチ編成を切り分けなければ、単純なFLOPs削減率から処理率を推定できない。〔原著§2、§5.3〕

| 最適化する資源 | 主要な入力・状態 | 典型的な律速 | サーベイが整理する介入点 |
|---|---|---|---|
| モデル重み | 線形層、専門家重み | HBM容量、重み読み出し | PTQ/QAT、枝刈り、低ランク分解、MoE |
| 入力処理 | 長いプロンプト、注意行列 | 注意計算、GPUカーネルのI/O | 疎/線形注意、FlashAttention、chunked prefill |
| 逐次生成 | 過去のK/V、要求ごとの出力長 | KV読み出し、低バッチ時の帯域 | KV eviction、Flash-Decoding、動的バッチ |
| 多数リクエスト | 要求到着・待ち行列・SLO | Head-of-line blocking、prefill干渉 | iteration-level scheduling、分離実行 |
| エッジ実行 | 小容量DRAM/HBM、SSD、CPU | 重みの載せ替え、CPU/GPU転送 | PowerInfer、LLM in a flash、量子化、NPU |

## 手法：分類軸と具体的な処理経路

### 1. モデル構造を変更する層（§3）

第一の層は、モデルが**どの状態を保持し、どの演算を行うか**自体を変える。注意機構について原著表1は標準Transformer、Reformer、Hyena、SSM、線形Transformer、RetNet、RWKVを時間・空間計算量で比較する。例えば標準注意の系列長二乗の行列に対し、線形注意は特徴写像と行列積の結合則を利用して鍵・値の要約状態を保持する。RWKVは再帰的状態へ置き換えるため、表1では系列長に依存しない状態容量 `O(d)` を示す。ただし、固定状態へ情報を集約する方式は全履歴の任意の位置を損失なく検索できることを意味しない。表の次数は理論的な演算/状態の見積りであり、同一GPUでの実測速度比較ではない。〔原著§3.1、表1〕

第二に、動的ニューラルネットワークは入力に応じて計算経路を変える。MoEではルータが活性化する専門家を選択し、総パラメータ数を増やしてもトークンごとの演算を疎に保つ。一方、専門家の配置・ルーティング・all-to-all通信が新しいボトルネックになる。早期終了では中間層で十分な確信度が得られれば後段を省略するが、生成モデルのトークンごとに層数を変えるとKVキャッシュとバッチの整合性が難しくなる。サーベイはFREE、SkipDecode、PABEE、DeeBERTを同じ「早期終了」の系統として整理するが、判別型BERTの分類早期終了と自己回帰LLMの逐次生成は同じ評価問題ではない。〔原著§3.2〕

第三に、拡散モデルでは繰り返しノイズ除去する**ステップ数**が主要な最適化対象となる。DDIM、DPM-Solverの数値解法によるステップ削減、潜在空間での拡散、MobileViTやEfficientViTの視覚エンコーダ効率化を扱う。DPM-Solverの10～20ステップという紹介値は画像生成の条件に関するもので、LLMのdecodeトークン数に置き換えてはならない。〔原著§3.3–3.4〕

### 2. 学習後の重みと推論状態を縮める層（§4）

モデル圧縮の分類は**構造化枝刈り、非構造化枝刈り、動的/文脈依存枝刈り、蒸留、量子化、低ランク分解**である。構造化枝刈りはヘッドやチャネルを削除して実際の行列形状を小さくするため、密な行列演算器でも高速化し得る。非構造化枝刈りは個別重みをゼロ化するが、疎行列のインデックスや専用カーネルの費用を無視するとメモリ/速度の利得を過大評価する。LLM-Prunerは構造の重要度を勾配から推定し、LoRAで品質を回復する。LoRAPruneはLoRAの重み・勾配を重要度推定に組み込み、チャネル・注意ヘッドを反復削除する。〔原著§4.4.1、表2〕

量子化ではQATが低精度の誤差を学習時に取り込むのに対し、PTQは学習済みモデルを少量の校正等で変換する。原著は**重みのみ**と**重み・活性の同時量子化**を分け、LLM特有の活性外れ値が低ビット化を難しくする点を強調する。SpQRは少数の重要重みを高精度で保存し、残りを低精度化する。QLoRAやLoftQは低精度重みとLoRA微調整の接続に位置付けられる。低ランク分解では大行列を複数の小行列に近似し、TensorGPTの埋め込み圧縮やLoSparseの低ランク＋疎性を例示する。圧縮後の重みサイズと、推論時の復元演算・キャッシュ・量子化スケールを含む総メモリは別の量である。〔原著§4.4.2–4.4.4、表2〕

LLM推論で重み圧縮と区別すべきなのが**KVキャッシュ圧縮**である。H2Oは履歴注意の重要度から保持すべきトークンを選び、Scissorhandsは重要な過去位置を残してKV容量を抑える。Landmark Attentionはブロックのランドマークを介して大容量・低速メモリへの退避を可能にする。KV evictionではモデル重みは同じまま、系列長・バッチ数に比例して増える実行時状態を削る。保持トークン選択が将来の質問に必要な情報を落とす場合は品質が悪化するため、平均PPLと長文脈検索精度を分けて評価する必要がある。〔原著§4.3.3–4.3.4〕

### 3. 推論基盤の配置・スケジューリング層（§5）

サーベイのシステム層はクラウド推論とエッジ推論を区別する。クラウドでは多数の要求を処理するため、モデル内部の計算最適化だけでなく、到着する要求を**どの単位で混ぜ、いつprefillし、いつdecodeするか**が重要になる。Orcaは反復単位のバッチ化を導入し、長さが異なる要求を同時に進める。FastServeは反復単位のプリエンプションとKV退避を組み合わせ、長い要求が短い要求を待たせる問題を扱う。SARATHI/Sarathi-Serveは長いprefillをチャンク化してdecodeと混ぜ、prefillによる生成停滞を抑える。Splitwiseはprefillとdecodeの計算・帯域特性の違いに応じて別のマシンへ配置する。これらは同じ「高速化」でも、遅延分布、TTFT、TPOT、総処理率、GPU使用量という異なる目的を持つ。〔原著§5.3〕

GPUカーネル側ではFlashAttention/FlashAttention-2が主にprefillで中間注意行列のHBM往復を減らし、Flash-Decoding/FlashDecoding++はdecode時の小さい行列形状に合わせて処理を分割する。ソフトウェア側のスケジューラがKVブロックを確保できても、カーネルが実際の転送量を減らせるとは限らない。逆に高速カーネルがあっても、要求間でprefillがdecodeを長時間妨げればサービス品質は改善しない。〔原著§5.3〕

エッジではCPU/GPU協調と永続ストレージが重要になる。PowerInferは高頻度に活性化するニューロンをGPUへ置き、低頻度のニューロンをCPUで処理してGPU容量と転送量を節約する。LLM in a flashはフラッシュから必要な重みを読み出す際、転送量削減と連続I/Oを重視する。STIはロードする重みの重要度に応じて精度を変える。これはGPUに全モデルを置くクラウド方式とは異なり、演算器の理論性能より、**必要な重みを必要なタイミングでどのメモリ階層から持ってくるか**が支配的になる設計である。〔原著§5.4〕

### 4. 複数の層をつなぐ比較枠組み

同一の圧縮手法でも、導入時には (a) 量子化・枝刈りによる事前変換時間、(b) 常駐重み・一時バッファ、(c) prefill、(d) decode、(e) KV退避・復元、(f) バッチと要求長分布を分けて測るべきである。原著表3のvLLM、LightLLM、TGI、TensorRT-LLM、llama.cpp、MLC-LLMは、それぞれ得意とする配置・機能が異なる。表3は**2024年時点の機能分類**であり、2026年現在の最新バージョンの対応表ではない。〔原著表3、§5.3–5.4〕

## 評価：本サーベイが実際に提供する証拠

### 評価の性質

**本論文には統一された新規ベンチマーク、共通ハードウェアでの全方式再測定、再現実験用コードがない。** 原著§2の演算・保存量の比較図、表1の理論計算量、表2の圧縮手法と課題、表3の公開ツール分類、および引用先の個別実験が主な根拠である。以下の数値は原著に紹介された引用元結果を整理したものであり、同一ワークロードの順位表ではない。〔原著§2–5、表1–3〕

| 論点 | サーベイが記載する例・数値 | 指標の意味 | 解釈上の制約 |
|---|---|---|---|
| 計算量 | Transformer注意 `O(T²d)`、RWKV状態 `O(d)` | 演算/状態の理論次数 | 実測tokens/sでも長文検索精度でもない |
| 長文脈 | LM-Infiniteは128K系列での生成を紹介 | 取り扱える入力長 | 128Kの任意位置検索精度を保証しない |
| KV管理 | H2Oは遅延最大1.9倍改善、処理率最大29倍と紹介 | 引用元研究の最大改善 | 両最大値の同一モデル・同一バッチ条件は本サーベイから断定できない |
| KV削減 | Scissorhandsは推論KVメモリを最大5分の1へ | 実行時KVの保存量 | 全GPUメモリやモデル重みの5分の1ではない |
| 動的実行 | EfficientViTはRestormer比最大6.4倍と紹介 | 画像復元系の高速化 | 自己回帰LLMの速度比較ではない |
| 分解圧縮 | TensorGPTは埋め込み層を最大38.40倍圧縮 | 特定層の容量 | モデル全体が38.40倍縮小するわけではない |
| 推論ツール | vLLM/LightLLM/TGI/TRT-LLM/llama.cppを表3に掲載 | 当時の機能分類 | 性能順位や2026年版の対応状況は未測定 |

原著の長文脈・量子化・MoEの紹介には多数の速度改善倍率が現れるが、論文固有のGPU、モデル、系列長、バッチ、精度、測定区間を揃えた統計的比較ではない。実務的には、候補を発見するための地図として使い、採用する方式の一次論文・コード・現行GPUで再評価する必要がある。特に「最大値」だけを組み合わせて総合高速化率を積算するのは不適切である。

### 重要な負の結果・評価の不足

本サーベイは個別方式の失敗例を統一的に収集したメタ分析ではない。モデル容量の削減がGPU上の計算を短縮しない条件、低ビット化による品質低下、長文脈での検索失敗、CPU/GPU転送による逆転、異なるバッチでの処理率変化は、横断的な失敗率として数値化されていない。表2は構造化枝刈りの再学習負担、量子化の外れ値、低精度変換の難しさを**課題**として整理するが、各方式の同一条件での悪化幅を示すものではない。〔原著§4.4、表2〕

## 限界・適用条件

**時点の限界。** 2025年1月の論文だが、中心となる収録研究は2024年までである。2025–2026年の新しい推論基盤、量子化形式、投機的復号、MoE配置の変更を自動的には反映しない。表3を現在のAPI/対応カーネル一覧として使ってはならない。

**対象選定の限界。** 著者は会議ランキングと手動選定を利用しており、全世界の研究を網羅する系統的レビュー（PRISMA型）ではない。視覚・拡散・学習も大きく含まれ、LLM推論システムだけの深掘りとしては粒度が粗い。

**評価の限界。** 異なる研究の倍率を同じ表に並べることはできても、共通ベンチマークでの順位は確定できない。ハードウェア世代、GPUメモリ容量、KVの保持方式、要求長、バッチ、生成品質の測定が揃わないためである。特に本サーベイ自体は新規システムを実装・測定していない。

**理論の限界。** 計算量が線形でも、カーネルの実装、GPU占有率、メモリ帯域、転送、同期、量子化復元で実測が逆転することがある。RWKV/SSMの固定状態は任意の長距離情報の無損失保持を意味しない。

**ローカル環境への限界。** 単一の12GB GPUと32GBホストRAMでの動作を、本サーベイが紹介するクラウド・A100級GPUの結果から直接推定できない。実機ではモデル常駐容量、KV使用量、CPUオフロード帯域、TTFT/TPOT、品質を独立に測る必要がある。

## 既存研究との関係・調査上の使い方

このサーベイは新規方式を提案する代わりに、個別の論文を**どの階層のどのボトルネックを変える研究か**で分類できる点が価値である。例えばH2OとScissorhandsは実行時KV容量、FlashAttentionはGPU上の注意演算I/O、Sarathi-Serveはprefillとdecodeの干渉、Splitwiseは異なる実行段階のGPU配置、PowerInferはエッジのCPU/GPU重み配置を変える。これらを単一の「高速LLM推論」というラベルで混同すると、改善が生じる条件を見誤る。

読解キューへの適用では、まず各論文の主目的を「重み容量」「KV容量」「HBM I/O」「CPU/GPU転送」「バッチ処理」「要求SLO」「モデル品質」に分類し、次に主要な処理順・ハードウェア・測定区間・負の結果を一次論文で確認する。この使い方は本サーベイが提示した分類の実務的な応用であり、著者が新たに実証したベンチマークではない。

## 一次資料

- 著者公開の掲載版全文（39ページ）：<https://www.caidongqi.com/pdf/CSUR25-llm-survey.pdf>
- ACM掲載版・DOI：<https://doi.org/10.1145/3706418>
- 構造分類：原著§3・表1。アルゴリズム：§4・表2。実行システム：§5・表3。将来方向：§6。

## 品質セルフレビュー

掲載版39ページの本文・図表・分類・参考文献を照合し、独自測定ではないことを冒頭と評価節に明記した。方式名だけを置換できる一般的な高速化説明ではなく、サーベイ固有の§3/4/5分類と各系統のボトルネックの違いを主軸に構成した。元の差し戻し原稿はGitHubのblocked pathが404で取得できなかったため、旧本文の差分修正ではなく一次論文から独立に再構成した。2026年の最新実装を本サーベイに帰属させず、未検証の速度比較も行わない。
