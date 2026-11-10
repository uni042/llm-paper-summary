---
canonical_id: arXiv:2412.10319
arxiv_id: '2412.10319'
title: 'SCBench: A KV Cache-Centric Analysis of Long-Context Methods'
authors:
- Yucheng Li
- Huiqiang Jiang
- Qianhui Wu
- Xufang Luo
- Surin Ahn
- Chengruidong Zhang
- Amir H. Abdi
- Dongsheng Li
- Jianfeng Gao
- Yuqing Yang
- Lili Qiu
published: 2024-12-13
publication_status: Preprint
lineage: Long-context serving / KV cache benchmark
topics:
- 長文脈推論
- KVキャッシュ
- ベンチマーク
- 疎注意
summary: SCBenchは長文脈方式を単発要求ではなく、同じ長い文脈を複数ターン・複数要求で再利用するKVキャッシュの全ライフサイクルから評価する。生成・圧縮・検索・読み込みの4段階、12タスク、931セッション/4,853クエリ、13方式を比較し、デコード時KVをsub-O(n)へ落とす方式は初回要求では良くても後続要求で急落しやすいこと、正確な文字列検索にはO(n)メモリが重要なこと、長い生成ではQuery分布変化で動的疎性も劣化することを示す。
list_summary: 共有長文脈を複数ターンで再利用する12タスクを用い、KV生成・圧縮・検索・読み込みの各方式が初回だけでなく後続要求でどう崩れるかを比較する。


reference_main_sha: 1b23235b6236736a5f91f6cb7b8052ed0b9b2251
source: https://arxiv.org/abs/2412.10319
sources:
- https://arxiv.org/abs/2412.10319
- https://arxiv.org/html/2412.10319
references_checked_at: '2026-10-03'
references_source: arxiv-html-reference-section
references:
- canonical_id: arXiv:2411.17116
  arxiv_id: '2411.17116'
- canonical_id: OpenReview:AB6XpMzvqH
  openreview_id: AB6XpMzvqH
- canonical_id: arXiv:2305.13245
  doi: 10.18653/v1/2023.emnlp-main.298
- canonical_id: arXiv:2407.05483
  arxiv_id: '2407.05483'
- canonical_id: DOI:10.18653/v1/2024.acl-long.401
  doi: 10.18653/v1/2024.acl-long.401
- canonical_id: DOI:10.18653/v1/2024.acl-long.172
  doi: 10.18653/v1/2024.acl-long.172
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: DOI:10.18653/v1/2023.acl-long.110
  doi: 10.18653/v1/2023.acl-long.110
- canonical_id: arXiv:2406.02069
  arxiv_id: '2406.02069'
- canonical_id: arXiv:2410.16179
  openreview_id: ALzTQUgW8a
- canonical_id: arXiv:1904.10509
  arxiv_id: '1904.10509'
- canonical_id: arXiv:2404.15949
  arxiv_id: '2404.15949'
- canonical_id: arXiv:2307.08691
  openreview_id: mZn2Xyh9Ec
- canonical_id: OpenReview:ztn8FCR1td
  openreview_id: ztn8FCR1td
- canonical_id: arXiv:2404.02690
  arxiv_id: '2404.02690'
- canonical_id: arXiv:2412.14468
  arxiv_id: '2412.14468'
- canonical_id: arXiv:2407.21783
  arxiv_id: '2407.21783'
- canonical_id: DOI:10.18653/v1/2023.acl-long.839
  doi: 10.18653/v1/2023.acl-long.839
- canonical_id: arXiv:2406.14909
  arxiv_id: '2406.14909'
- canonical_id: arXiv:2405.08944
  arxiv_id: '2405.08944'
- canonical_id: arXiv:2310.01801
  openreview_id: uNrFpDPMyo
- canonical_id: arXiv:2311.04934
- canonical_id: arXiv:2406.12793
  arxiv_id: '2406.12793'
- canonical_id: arXiv:2312.00752
  openreview_id: tEYskw1VY2
- canonical_id: OpenReview:uYLFoz1vlAC
  openreview_id: uYLFoz1vlAC
- canonical_id: arXiv:2308.16137
  doi: 10.18653/v1/2024.naacl-long.222
- canonical_id: arXiv:2212.06713
  arxiv_id: '2212.06713'
- canonical_id: OpenReview:g4OTKRKfS7R
  openreview_id: g4OTKRKfS7R
- canonical_id: OpenReview:6osgTNnAZQ
  openreview_id: 6osgTNnAZQ
- canonical_id: arXiv:2411.09688
  arxiv_id: '2411.09688'
- canonical_id: OpenReview:kIoBbc76Sy
  openreview_id: kIoBbc76Sy
- canonical_id: OpenReview:duRRoGeoQT
  openreview_id: duRRoGeoQT
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.825
  doi: 10.18653/v1/2023.emnlp-main.825
- canonical_id: arXiv:2407.02490
  openreview_id: fPBACAbqSN
- canonical_id: OpenReview:VTF8yNQM66
  openreview_id: VTF8yNQM66
- canonical_id: arXiv:2404.12457
  arxiv_id: '2404.12457'
- canonical_id: arXiv:2402.05099
  arxiv_id: '2402.05099'
- canonical_id: DOI:10.18653/v1/2024.emnlp-main.1124
  doi: 10.18653/v1/2024.emnlp-main.1124
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: arXiv:2502.20766
  openreview_id: OfjIlbelrT
- canonical_id: DOI:10.18653/v1/2024.acl-long.859
  doi: 10.18653/v1/2024.acl-long.859
- canonical_id: arXiv:2404.02060
  arxiv_id: '2404.02060'
- canonical_id: arXiv:2310.06201
  doi: 10.18653/v1/2023.emnlp-main.391
- canonical_id: arXiv:2404.14469
  openreview_id: poE54GOq2l
- canonical_id: arXiv:2403.19887
  arxiv_id: '2403.19887'
- canonical_id: DOI:10.48550/arxiv.2405.04434
  arxiv_id: '2405.04434'
- canonical_id: arXiv:2409.10516
  arxiv_id: '2409.10516'
- canonical_id: arXiv:2406.06025
  arxiv_id: '2406.06025'
- canonical_id: DOI:10.1162/tacl_a_00638
  doi: 10.1162/tacl_a_00638
- canonical_id: arXiv:2305.17118
  openreview_id: JZfg6wGi6g
- canonical_id: arXiv:2402.02750
  openreview_id: L057s2Rq8O
- canonical_id: arXiv:2502.13189
  arxiv_id: '2502.13189'
- canonical_id: arXiv:2404.07143
  arxiv_id: '2404.07143'
- canonical_id: arXiv:2403.09636
  openreview_id: tDRYrAkOB7
- canonical_id: arXiv:2209.11895
  arxiv_id: '2209.11895'
- canonical_id: DOI:10.18653/v1/2024.findings-acl.57
  doi: 10.18653/v1/2024.findings-acl.57
- canonical_id: OpenReview:7SaXczaBpG
  openreview_id: 7SaXczaBpG
- canonical_id: arXiv:2407.00079
- canonical_id: arXiv:2403.05530
  arxiv_id: '2403.05530'
- canonical_id: arXiv:2406.07522
  openreview_id: bIlnpVM4bc
- canonical_id: OpenReview:OS5dqxmmtl
  openreview_id: OS5dqxmmtl
- canonical_id: arXiv:1911.02150
  arxiv_id: '1911.02150'
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2408.03314
  arxiv_id: '2408.03314'
- canonical_id: arXiv:2410.21465
  arxiv_id: '2410.21465'
- canonical_id: arXiv:2404.11912
  openreview_id: HVK6nl3i97
- canonical_id: arXiv:2307.08621
  arxiv_id: '2307.08621'
- canonical_id: arXiv:2405.05254
  openreview_id: 25Ioxw576r
- canonical_id: arXiv:2406.10774
  openreview_id: KzACYw0MTV
- canonical_id: DOI:10.1145/3315508.3329973
  doi: 10.1145/3315508.3329973
- canonical_id: arXiv:2409.12640
  arxiv_id: '2409.12640'
- canonical_id: arXiv:2406.07887
  arxiv_id: '2406.07887'
- canonical_id: OpenReview:jp3gWrMuIZ
  openreview_id: jp3gWrMuIZ
- canonical_id: arXiv:2309.17453
  openreview_id: NG7sS51zVF
- canonical_id: OpenReview:cFu7ze7xUm
  openreview_id: cFu7ze7xUm
- canonical_id: arXiv:2502.14866
  arxiv_id: '2502.14866'
- canonical_id: arXiv:2405.16444
  arxiv_id: '2405.16444'
- canonical_id: arXiv:2410.02694
  arxiv_id: '2410.02694'
- canonical_id: DOI:10.18653/v1/2020.acl-main.444
  doi: 10.18653/v1/2020.acl-main.444
- canonical_id: DOI:10.18653/v1/2024.findings-emnlp.266
  doi: 10.18653/v1/2024.findings-emnlp.266
- canonical_id: arXiv:2502.11089
  arxiv_id: '2502.11089'
- canonical_id: arXiv:2306.14048
- canonical_id: arXiv:2312.07104
  openreview_id: VqkAKQibpq
- canonical_id: DOI:10.1145/3600006.3613139
  doi: 10.1145/3600006.3613139
- canonical_id: arXiv:2406.15486
  arxiv_id: '2406.15486'
arxiv_categories:
  primary: cs.CL
  cross_list:
  - cs.LG
publication: arXiv
publication_type: プレプリント
code: null
implementation: 実装形態の詳細は既存本文の手法・評価記述を参照。公式コードURLはメタデータ確認時点で確認できず。
implementation_status: official-code-not-confirmed
last_checked: '2026-10-03'
references_total: 105


last_audited: '2026-10-08'
audit_version: 2
under16kb_reaudit_target_path: papers/inference/13-sparse-attention/2024-2412.10319-scbench-a-kv-cache-centric-analysis-of-long-context-methods.md
under16kb_reaudit_source_git_blob_sha: '8c810eafb11365bdf0099da981c59e4203a46968'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
worker_run_key: 'interactive-20261008-bottom-up-reaudit-r2-2412.10319'
worker_completed_at: '2026-10-07T22:47:42.561Z'

---

# SCBench: A KV Cache-Centric Analysis of Long-Context Methods

> 共有長文脈を複数ターンで再利用する12タスクを用い、KV生成・圧縮・検索・読み込みの各方式が初回だけでなく後続要求でどう崩れるかを比較する。

## 概要
長文脈向けの疎注意、KV eviction、量子化、検索型attentionは、多くの場合1つの長いpromptに1回質問するベンチマークで評価される。しかし実際のサービングでは、同じ文書やコードベースに対して複数の質問を続け、prefix cacheとしてKVを再利用する。SCBenchはこの差を埋めるため、KVキャッシュの生成、圧縮、検索、読み込みという4段階から長文脈方式を整理し、共有文脈を複数ターン・複数要求で使うベンチマークを構築する。

12タスク、931セッション、4,853クエリを含み、文字列検索、意味検索、全体情報処理、複数タスクの4能力を測る。13の長文脈方式を複数のLlama/Qwen/GLM/Mamba/Jamba系モデルで比較した結果、デコード時KVをsub-O(n)へ削る方式は初回質問では強くても後続質問で急落しやすい。対してKV全体をO(n)で保持しつつプリフィルや読み込み計算を疎化する方式は、複数要求でより頑健だった。

## 問題設定
Query依存のKV圧縮は、最初の質問に必要な情報だけを残せば高い圧縮率を得られる。しかし同じ長文脈に次の質問が来たとき、前のQueryでは不要だった情報が必要になる可能性がある。一度捨てたKVは元promptを再プリフィルしない限り復元できない。このため単発ベンチマークは、キャッシュ再利用時の情報欠落を過小評価する。

SCBenchは長文脈方式を計算量だけでなくKVライフサイクル上の位置で分類する。生成段階では疎attentionや状態空間モデル、圧縮段階ではKV dropping/量子化、検索段階では過去KVの再利用、読み込み段階ではHBM/DRAM/SSD等から必要KVだけをGPU SRAMへ読む方式を扱う。

## 手法：ベンチマーク設計
### 共有文脈の二モード
複数ターンモードでは1セッション内で同じ長文脈へ連続質問する。複数要求モードではセッションをまたいで共有文脈のKVを再利用する。どちらも「一度作ったKVを別Queryが再利用する」点を評価できる。

### 12タスク
文字列検索にはkey-value検索、prefix-suffix検索、multi-hop変数追跡を含む。意味検索にはRepoQAや長文QA、全体情報処理にはmany-shot in-context learning、要約、配列統計、複数タスクには要約+needle検索やRepoQA+KV検索を組み合わせる。平均入力長はタスクにより22Kから1.5Mトークン級まで広がる。

全体では931セッション、4,853クエリ、平均約5ターンである。例えばkey-value検索は125K入力、100セッション/500ターン、RepoQAは65K入力、88セッション/440ターン、中国語QAは平均1.5M入力を持つ。単純なneedle検索だけでなく、Queryが変わると必要箇所も変わる構成になっている。

### 比較方式
評価対象はMamba、Jamba、A-shape/Tri-shape/MInference、LLMLingua-2、StreamingLLM、SnapKV、PyramidKV、KIVI、CacheBlend、Quest、RetrievalAttentionなどを含む。これらをKV生成・圧縮・検索・読み込みへ配置し、プリフィル計算量、デコード計算量、KV容量がO(n)かsub-O(n)かを整理する。

## 手法：三形状の疎注意
分析だけでなく、SCBenchは学習不要のTri-shapeも提案する。A-shapeはattention sinkと局所窓を残すが、Tri-shapeは入力末尾のQuery領域も三角形状に保持する。初回Queryで必要なプリフィル接続を増やしつつ、全attentionより計算を削減する。複数要求では完全KVを保持するため、最初のQueryに依存して過去情報を不可逆に捨てる方式より頑健になる。

## 評価：主な結果
最も重要な発見は、**sub-O(n)メモリのデコードは複数ターンで非常に厳しい**ことである。StreamingLLMやSnapKVのようにKVそのものを落とす方式は最初の質問では良くても、後続Queryで必要な情報が変わると性能が落ちる。一方、O(n) KVを保持して計算だけを疎化する方式は複数要求でfull attentionへ近い性能を保ちやすい。

タスク種類でも圧縮耐性が違う。要約など全体統計を使うタスクは比較的圧縮しやすいが、ランダムなkey-valueの完全一致検索は入力の情報をほぼ全て保持する必要があり、O(n)空間が重要になる。全方式は圧縮予算を下げるほど悪化するが、sub-O(n)方式は1/4予算付近で急落する一方、RetrievalAttentionやKIVIのようにO(n)の情報保持を維持する方式は高圧縮でも相対的に頑健である。

さらに長い生成ではQuery/attention分布がターンとともに変化する。初期Queryから重要KVを推定した動的疎方式でも、生成が長くなると重要度分布がずれ、RetrievalAttentionのようなO(n)保持方式でも性能低下が観測される。したがって「動的なら安全」という単純な結論にもならない。

## 評価条件
|項目|内容|
|---|---|
|セッション/クエリ|931 / 4,853|
|能力カテゴリ|文字列検索、意味検索、全体情報、複数タスク|
|共有モード|複数ターン、複数要求|
|方式|13長文脈方式、8カテゴリ|
|モデル|Llama-3.1 8B/70B、Qwen2.5 32B/72B、Llama-3-8B-262K、GLM-4-9B-1M、Codestral Mamba、Jamba-1.5-mini等|
|入力長|タスク平均22K〜1.5M級|

### キャッシュ再利用を基準にした評価結果

単発要求と複数ターンの差は、記憶した情報を後から取り出せるかどうかで現れる。最初の質問に適する情報だけを優先して保存する方式では、後続の質問が別の箇所を参照すると必要な情報を失っている可能性がある。論文の図3は、同一文脈に対する質問の回数が増えるほど、記憶量を文脈長より低い次数へ抑える方式が苦しくなることを示す。一方、文脈全体に対応する情報を残す方式は後続質問に比較的強い。ただし情報を残していれば無条件で正確というわけではなく、検索機構や長文生成時の注意分布の変化も評価する必要がある。

12タスクは、文字列をそのまま探す能力、意味から関連情報を探す能力、文脈全体をまとめる能力、複数の課題を一つの長文へ適用する能力に分かれる。特に文字列の完全一致検索は、捨てた情報を文脈の一般的な要約から復元できないため、圧縮方式の苦手な条件になりやすい。要約能力だけで評価するとこうした弱点を見逃す。論文は931セッションと4,853クエリを用いて同じ内容を繰り返し利用する状況を組み込み、単発の長文理解ベンチマークとの差を明確にした。

圧縮予算を小さくした結果、情報の保持量を大幅に減らす方式では精度が急落する条件が観察される。ただしこれは全方式に同一の処理速度やハードウェア利用効率を保証する比較ではなく、主にタスクごとの品質の頑健性を調べた結果である。また、生成が長く続く場合は後半の問い合わせの性質が変わり、最初の問い合わせへ適応して選んだ注意対象が陳腐化する。動的な疎注意であっても、最初の分布に依存した状態では安全ではない。

追試する場合には、初回要求の得点だけでなく、同一文脈を共有した二回目以降の得点を個別に報告するべきである。さらに保持する記憶量、入力処理に必要な計算、後続要求での検索コストを分けることで、記憶量を減らす方式と計算だけを間引く方式を混同せず比較できる。本文が対象とする八種類の長文脈方式の分類は、単一の総合点ではなく、どの段階で何を省くかを比較する枠組みとして解釈する。

## 既存研究との差
LongBenchやRULERは長文脈能力を広く測るが、SCBenchの中心は「同じKVを次のQueryへ持ち越したときに方式の近似がどう累積するか」である。また各方式を単に疎attention/量子化と分類せず、KVの生成・圧縮・検索・読み込みという実装ライフサイクルへ置くことで、メモリを捨てる方式と、メモリは残して計算だけ減らす方式の差を明示する。

## 限界
ベンチマーク結果は採用したモデルと12タスクに依存し、実サービスの全トラフィック分布を再現するものではない。SCBenchは品質劣化の構造分析が中心で、各方式の実機サービングTPSや運用コストを統一ランタイム上で完全比較するベンチマークではない。また1.5M級入力など極端なタスクを含むため、実運用の中央値とは異なる場合がある。

## 一次資料
- https://arxiv.org/abs/2412.10319
- https://arxiv.org/html/2412.10319
