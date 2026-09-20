---
canonical_id: DOI:10.1145/3676641.3715996
arxiv_id: '2410.18038'
doi: 10.1145/3676641.3715996
arxiv_categories:
  primary: cs.LG
  cross_list:
  - cs.DC
title: 'POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference'
summary: POD-Attentionは、計算律速のプリフィル注意とメモリ帯域律速のデコード注意を別カーネルで逐次実行するためGPU資源が交互に遊ぶ問題を、単一GPUカーネル内で両者を同じSMへ同時配置して解く。CTAが配置先SMを実行時に読み、SMごとのチケットでプリフィルかデコードを選ぶSM認識型CTAスケジューリングにより、ハードウェアのCTA配置に依存せず相補的な処理を共存させる。FlashAttention 2.6.1を基礎にデコードのタイル縮小、2/4 CTA構成の自動選択、仮想デコードCTA、プリフィル分割数制限を組み合わせ、A100上で注意計算を最大59%、平均28%高速化した。Sarathi-Serveへ統合した評価ではオフライン処理量を最大22%改善し、オンラインではTTFT、TBT、要求完了遅延を同時に改善する。
list_summary: プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。
authors:
- Aditya K Kamath
- Ramya Prabhu
- Jayashree Mohan
- Simon Peter
- Ramachandran Ramjee
- Ashish Panwar
authors_affiliations: University of Washington; Microsoft Research
published: '2025-03-30'
publication: ASPLOS 2025, Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2
publication_type: 査読付き国際会議論文
publication_status: ASPLOS 2025採択・出版。arXiv:2410.18038は2024年10月23日に初版公開。
lineage: kernel-runtime-compilation
topics:
- LLMサービング
- GPU注意カーネル
- ハイブリッドバッチ
- プリフィル・デコード重畳
- SM認識スケジューリング
importance: 長文LLMサービングで相補的な計算資源を使うプリフィル注意とデコード注意をSM内で直接重ね、ハイブリッドバッチの注意ボトルネックをカーネル層で解消する。
hardware_evaluation: NVIDIA A100 80GBを1〜2基使用し、Yi-6B、Llama-2-7B、Llama-3-8Bを実機評価。
hardware_details: Yi-6BはA100 1基、Llama-2-7BとLlama-3-8BはA100 2基のテンソル並列。Ubuntu 22.04、CUDA 12.4、PyTorch 2.4。
quality_effect: モデル演算の意味や重みを変えず注意カーネルの実行方式だけを変更するため、生成品質を近似で低下させない。
bottlenecks:
- プリフィル注意の低メモリ帯域利用
- デコード注意の低演算器利用
- 別カーネル逐次実行
- CTAのSM共配置保証不足
- 長文で増大する注意計算時間
evidence_locations:
- §3 Concurrent Execution
- §4 POD-Attention
- §5 Evaluation
- §6 Related Work
- Appendix A Artifact Appendix
references:
- canonical_id: arXiv:2409.17264
  arxiv_id: '2409.17264'
- canonical_id: arXiv:2403.02310
- canonical_id: arXiv:2308.16369
  arxiv_id: '2308.16369'
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.298
  doi: 10.18653/v1/2023.emnlp-main.298
- canonical_id: arXiv:2411.11217
  arxiv_id: '2411.11217'
- canonical_id: arXiv:2406.06858
  arxiv_id: '2406.06858'
- canonical_id: arXiv:2307.08691
  openreview_id: mZn2Xyh9Ec
- canonical_id: arXiv:2205.14135
- canonical_id: DOI:10.1109/inpar.2012.6339596
  doi: 10.1109/inpar.2012.6339596
- canonical_id: arXiv:2401.08671
  arxiv_id: '2401.08671'
- canonical_id: arXiv:2401.11181
  arxiv_id: '2401.11181'
- canonical_id: OpenReview:stXtBqyTWX
  openreview_id: stXtBqyTWX
- canonical_id: DOI:10.1145/3503222.3507778
  doi: 10.1145/3503222.3507778
- canonical_id: DOI:10.1109/cgo57630.2024.10444873
  doi: 10.1109/cgo57630.2024.10444873
- canonical_id: arXiv:2412.08585
  arxiv_id: '2412.08585'
- canonical_id: DOI:10.1145/2600212.2600228
  doi: 10.1145/2600212.2600228
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: DOI:10.1109/cgo53902.2022.9741270
  doi: 10.1109/cgo53902.2022.9741270
- canonical_id: DOI:10.1109/tpds.2014.2313342
  doi: 10.1109/tpds.2014.2313342
- canonical_id: DOI:10.1145/3572848.3577479
  doi: 10.1145/3572848.3577479
- canonical_id: DOI:10.1145/2451116.2451160
  doi: 10.1145/2451116.2451160
- canonical_id: arXiv:2311.18677
  doi: 10.1109/isca59077.2024.00019
- canonical_id: arXiv:2405.04437
  doi: 10.1145/3669940.3707256
- canonical_id: arXiv:2405.10480
  arxiv_id: '2405.10480'
- canonical_id: OpenReview:tVConYid20
  openreview_id: tVConYid20
- canonical_id: arXiv:2401.00588
- canonical_id: arXiv:2312.12456
  doi: 10.1145/3694715.3695964
- canonical_id: arXiv:2408.00741
  arxiv_id: '2408.00741'
- canonical_id: DOI:10.1109/sc.2014.21
  doi: 10.1109/sc.2014.21
- canonical_id: DOI:10.1145/3567955.3567959
  doi: 10.1145/3567955.3567959
- canonical_id: DOI:10.1109/hpca.2016.7446078
  doi: 10.1109/hpca.2016.7446078
- canonical_id: DOI:10.1145/2751205.2751213
  doi: 10.1145/2751205.2751213
- canonical_id: DOI:10.1145/3694715.3695948
  doi: 10.1145/3694715.3695948
- canonical_id: arXiv:2305.05920
  arxiv_id: '2305.05920'
- canonical_id: DOI:10.1109/micro.2012.19
  doi: 10.1109/micro.2012.19
- canonical_id: arXiv:2501.01005
  arxiv_id: '2501.01005'
- canonical_id: DOI:10.1145/3018743.3018754
  doi: 10.1145/3018743.3018754
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: DOI:10.1109/tc.2022.3214088
  doi: 10.1109/tc.2022.3214088
- canonical_id: arXiv:2312.07104
  openreview_id: VqkAKQibpq
- canonical_id: arXiv:2401.09670
- canonical_id: arXiv:2408.12757
  arxiv_id: '2408.12757'
references_checked_at: '2026-09-20'
references_source: arxiv-html-reference-section
references_total: 66
source: https://arxiv.org/abs/2410.18038
sources:
- https://arxiv.org/abs/2410.18038
- https://ar5iv.labs.arxiv.org/html/2410.18038
- https://doi.org/10.1145/3676641.3715996
code: https://github.com/microsoft/vattention/tree/main/pod_attn
implementation: FlashAttention v2.6.1を基礎とするCUDAカーネルとして実装され、Sarathi-Serveへ統合。Docker、GitHub、Zenodoの再現用成果物を公開。
last_checked: '2026-09-20'
last_audited: null
audit_version: 0
---

# POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference

> プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。
## 書誌情報
- **著者**: Aditya K Kamath, Ramya Prabhu, Jayashree Mohan, Simon Peter, Ramachandran Ramjee, Ashish Panwar
- **著者・所属**: University of Washington; Microsoft Research
- **公開**: ASPLOS 2025, Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2
- **種別**: 査読付き国際会議論文
- **対象**: LLMサービング、GPU注意カーネル、ハイブリッドバッチ、プリフィル・デコード重畳、SM認識スケジューリング
- **実装**: FlashAttention v2.6.1を基礎とするCUDAカーネルとして実装され、Sarathi-Serveへ統合。Docker、GitHub、Zenodoの再現用成果物を公開。
## 概要
POD-Attentionは、計算律速のプリフィル注意とメモリ帯域律速のデコード注意を別カーネルで逐次実行するためGPU資源が交互に遊ぶ問題を、単一GPUカーネル内で両者を同じSMへ同時配置して解く。CTAが配置先SMを実行時に読み、SMごとのチケットでプリフィルかデコードを選ぶSM認識型CTAスケジューリングにより、ハードウェアのCTA配置に依存せず相補的な処理を共存させる。FlashAttention 2.6.1を基礎にデコードのタイル縮小、2/4 CTA構成の自動選択、仮想デコードCTA、プリフィル分割数制限を組み合わせ、A100上で注意計算を最大59%、平均28%高速化した。Sarathi-Serveへ統合した評価ではオフライン処理量を最大22%改善し、オンラインではTTFT、TBT、要求完了遅延を同時に改善する。

POD-Attentionはプリフィル注意とデコード注意を単一カーネルへCTA単位で融合し、CTAがGPUへ配置された後に自分のSM番号とSMごとの実行履歴を読んで担当処理を決めるSM認識型CTAスケジューリングを導入する。これによりCUDAのハードウェアスケジューラがCTAをどのSMへ置くかを事前に制御できなくても、各SMへ演算律速CTAと帯域律速CTAを意図的に共配置できる。さらに融合時だけ問題になる資源干渉を抑えるため、デコードの小タイル化、2/4 CTA構成、仮想CTA、プリフィルのKV方向分割制限を組み合わせる。
## 問題設定
LLM推論では入力列を並列処理するプリフィルが演算律速、1トークンずつ生成するデコードがメモリ帯域律速になる。Sarathi-Serve等は両フェーズの要求を同じ反復へ混ぜるハイブリッドバッチで線形演算の重み読み出しを共有するが、注意計算はFlashAttention等のプリフィル用カーネルとデコード用カーネルを直列に実行する。長文では注意が反復時間の60%以上を占め得る一方、プリフィル注意のメモリ帯域利用は5%未満、デコード注意の演算利用は10%未満になる場合があり、一方の資源が必要な直後に同じ資源が遊ぶ。CUDAストリーム、素朴なCTA並列、warp融合ではSM単位の共配置保証、同期障壁、stragglerの問題があり、相補的な資源需要を安定して重ねられない。
## 新規性
POD-Attentionはプリフィル注意とデコード注意を単一カーネルへCTA単位で融合し、CTAがGPUへ配置された後に自分のSM番号とSMごとの実行履歴を読んで担当処理を決めるSM認識型CTAスケジューリングを導入する。これによりCUDAのハードウェアスケジューラがCTAをどのSMへ置くかを事前に制御できなくても、各SMへ演算律速CTAと帯域律速CTAを意図的に共配置できる。さらに融合時だけ問題になる資源干渉を抑えるため、デコードの小タイル化、2/4 CTA構成、仮想CTA、プリフィルのKV方向分割制限を組み合わせる。
## 手法
### 手法のあらまし
入力はSarathi-Serve等のスケジューラが作った、一つのプリフィルチャンクと複数のデコード要求を含むハイブリッドバッチである。まずPOD-Attentionはバッチ形状、文脈長、ヘッド構成からプリフィル注意とデコード注意に必要なCTA数を別々に算出し、その合計CTA数を持つ単一の融合カーネルを起動する。次に各CTAがGPUのハードウェアスケジューラによってSMへ配置された後、代表スレッドがSM識別子を読み、そのSM専用の原子的カウンタからチケットを取得する。チケットと現在バッチのプリフィル対デコードCTA比から担当処理を決め、担当側の未割当CTA番号を原子的に確保する。予定数を超えた場合はもう一方へ切り替え、決定した処理種別とCTA番号を共有メモリへ書いてCTA内の全スレッドへ渡す。その後、同じwrapperカーネル内からFlashAttention由来のプリフィルまたはデコードdevice関数を呼び出す。こうして同一SM上の別CTAが、Tensor Coreを多く使うプリフィルとHBM帯域を多く使うデコードを並行実行する。最後に各CTAが通常の正確なattention出力を生成し、Sarathi-Serveの後続レイヤーへ返す。融合による資源競合を抑えるため、起動前に2 CTA/SMまたは4 CTA/SMを選び、デコードのQSLタイルを16へ縮小し、仮想デコードCTAとプリフィル分割上限も適用する。出力の数値的意味は元の注意計算と同じで、変更するのはGPU上の配置と実行順だけである。

### SM認識型CTAスケジューリング
入力としてプリフィル・デコードそれぞれの必要CTA数と、GPUハードウェアが実際に決めた配置先SMを使う。CTAの代表スレッドはPTXのSM識別子を読み、そのSM専用の原子的カウンタを加算してチケットを得る。比例方針では現在バッチの必要CTA比に沿ってチケットをプリフィルまたはデコードへ写像し、50:50方針では交互に割り当てる。続いて処理種別ごとの未使用CTA番号を原子的に確保し、片側を使い切っていればもう一方へ切り替える。最終決定を共有メモリへ書き、CTA内の全スレッドが同じ処理を開始する。これによりハードウェアスケジューラ自体を改造せず、各SMに演算律速と帯域律速のCTAを共配置でき、CUDAストリームだけでは保証できないSM内資源重畳を作る。

### デコード用小タイル
入力はデコード要求のqueryと既存KVキャッシュで、通常のFlashAttention系カーネルではTensor Core利用に合わせてQSL方向へ64〜128程度の大きいタイルを使う。しかしデコードは実質1トークンで、Grouped Query Attentionでもquery側長は小さいため、大タイルの大部分はゼロ埋めされた不要演算になる。デコード単独ならHBM帯域律速なので余分な演算は目立たないが、融合時には同じSMのプリフィルが必要とするTensor Coreを奪う。POD-AttentionはA100上のCUTLASS Tensor Core演算で使えるQSL長16へ縮め、デコードの演算利用を約10%まで抑える一方、大バッチで必要なメモリ帯域利用を維持する。その結果、解放した演算資源を同居プリフィルへ渡し、両処理の並行時間を増やす。

### 2/4 CTA構成の自動選択
入力としてバッチ内のプリフィル・デコード比、文脈長、各CTAの共有メモリ要求を使い、SM当たり同時常駐CTA数を2または4から選ぶ。長文でプリフィル計算が重い場合は2 CTA/SMにして1 CTA当たりの共有メモリを増やし、大きいプリフィルタイルを使えるようにする。デコード比率が高い場合は4 CTA/SMにし、例えばプリフィル1 CTAとデコード3 CTAのように細かい比率で共配置する。8 CTA/SMも検証したが、共有資源が細分化され多くの条件で逆効果だったため採用しない。この選択により、固定構成では一方のワークロードで発生する共有メモリ不足または粗い配置比率を避け、バッチ特性に応じて重畳可能量を増やす。

### 仮想デコードCTA
融合カーネルではカーネル起動時にCTA当たりの共有メモリ量を一つに決めるため、必要量の大きいプリフィルに合わせるとデコードCTAへ不要な共有メモリを予約してしまう。デコードは小さいタイルを使うため実際の共有メモリ需要はプリフィルの約4分の1である。そこで元のデコードCTAをwarp単位の複数の仮想CTAへ分割し、CTA全体の同期障壁をwarp同期へ置き換える。各仮想CTAは独立したデコードタイルを処理し、少ない共有メモリで複数のデコード仕事を同時収容する。これにより共有メモリの過剰予約でSM常駐数が下がることを防ぎ、プリフィルCTAとデコード処理の共存密度を高める。

### プリフィル分割数制限
チャンク化プリフィルではqueryトークン数が制限されるため、FlashDecodingと同様にKV方向へ処理を分割してCTA数を増やすとGPUを埋めやすい。ただし分割した各CTAは同じqueryを読み直すため、分割数に比例してHBM読み出しが増える。プリフィル単独なら並列性向上がこの費用を上回る場合があるが、POD-Attentionでは同じSMでデコードCTAもKVキャッシュを読み、帯域競合が発生する。そこでプリフィルのKV方向分割を経験的に最大2 waveを満たす程度へ制限する。必要な並列性は確保しつつ余分なquery再読込を抑え、デコードが使う帯域を残すことで、融合前より両者を重ねやすくする。

### 全体のデータ／制御の流れ
FlashAttention 2.6.1のプリフィル・デコードカーネルをGPU内から呼べるdevice関数へ変換し、CUDAのblockIdx依存を引数化した上で一つのwrapperカーネルから呼び分ける。Sarathi-Serveのチャンク化プリフィルと継続的ハイブリッドバッチへ組み込み、既存スケジューラが作るバッチを変更せず注意演算部分だけ置換する。SM単位のカウンタ、処理種別ごとのCTA割当カウンタ、共有メモリ上の担当通知を使い、CPU側の細粒度介入なしでGPU内部の割当を完結させる。
## 評価条件
- **ハードウェア**: NVIDIA A100 80GB 1基（Yi-6B）、NVIDIA A100 80GB 2基・テンソル並列（Llama-2-7B、Llama-3-8B）、Ubuntu 22.04 / CUDA 12.4 / PyTorch 2.4
- **データセット／トレース**: arXiv-Summarization由来ワークロード、内部企業ワークロード
- **比較対象**: FlashAttention 2.6.1のプリフィル・デコード直列実行、FlashAttentionを別CUDAストリームで並列実行、HFuseによるFlashAttention warp融合、FlashInfer 0.2.0直列実行、FlashInferのプリフィル用カーネルで一括処理、元のvLLMスケジューラ、Sarathi-Serve
実機評価であり、Yi-6BはA100 1基、Llama-2-7BとLlama-3-8BはA100 2基のテンソル並列。長文・ハイブリッドバッチが中心で、注意が直列実行時間の20%以上を占める条件を注意単体評価の対象とする。Hopper世代とFlashAttention-3への拡張は将来課題。
## 主要結果
POD-Attentionは1000超のハイブリッドバッチで注意計算をFlashAttention直列実行より最大59%、平均28%高速化し、評価点の25%では理論上の完全重畳に対して10%以内へ到達した。Sarathi-Serveへ統合するとオフライン処理量をモデル別に19〜22%改善し、オンラインではSarathiの低TBT特性を維持しながらTTFTと要求完了遅延を大きく下げる。

- 注意計算高速化 / 最大59%、平均28% (比較対象: FlashAttentionプリフィル・デコード直列実行; 条件: 3モデル、1000超のハイブリッドバッチ) — 演算律速と帯域律速の注意CTAを同じSMへ共配置することで両資源を同時利用する。

- 理論ピークへの接近 / 評価条件の25%で理論ピーク高速化の10%以内 (比較対象: 完全重畳の理論値; 条件: 注意単体評価) — SM認識配置が多くの条件でほぼ完全な資源重畳を実現する。

- オフライン処理量 / Sarathi比 Yi-6B 22%、Llama-2-7B 20%、Llama-3-8B 19%向上 (比較対象: Sarathi-Serve; 条件: 16K長文要求) — 注意だけでなく端から端のサービング処理量へ利得が波及する。

- P99 TTFT / Sarathi比最大4.3倍短縮 (比較対象: Sarathi-Serve; 条件: オンライン、内部・arXiv系ワークロード) — ハイブリッドバッチ内でプリフィルがデコードと資源競合する時間を短縮する。

- P99 TBT / Sarathi比10〜20%短縮 (比較対象: Sarathi-Serve; 条件: オンライン評価) — Sarathiの生成停止抑制を維持しつつ各反復の注意時間も削る。

- P99要求完了遅延 / vLLM比最大42%短縮（内部106.8秒対151.8秒）、arXiv系最大17%短縮（333秒対401.2秒） (比較対象: 元のvLLM; 条件: 高負荷オンライン評価) — TTFTだけを優先するvLLMより、全要求の完了時間と対話性の均衡を改善する。

- 注意カーネル消費エネルギー / 最大35%、平均20.5%削減 (比較対象: FlashAttention直列実行; 条件: 注意単体プロファイル) — 実行時間短縮にほぼ比例してエネルギーも減る。

- 比例CTA割当 / 50:50割当より最大14%高速 (比較対象: 固定50:50 CTA割当; 条件: 8K文脈・負荷増加時) — 少数側の処理をSM全体へ散らし資源重畳と競合抑制を両立する。

### 負の結果・境界条件
- FlashInferのプリフィル用カーネルでプリフィルとデコードを一括処理すると高文脈長で最大40%悪化し、デコードの余分な演算がプリフィルと競合する。
- HFuseは中央値で11%改善するがstragglerによりFlashAttention直列より最大13%遅くなる場合がある。
- P:D比が12未満ではデコードのみ、18超ではプリフィルのみの反復が増え、重畳機会が減るためPOD-Attentionの利得が小さくなる。
- 8 CTA/SMは一部条件のみわずかに改善し、多くの条件で2/4 CTA構成より悪化する。

### 結果の読み方
利得はプリフィルとデコードが同じ反復へ混在し、注意が十分大きい条件で最大になる。長文では注意の割合が増え、プリフィルのTensor Core需要とデコードのHBM帯域需要を同じSMで重ねる余地が大きい。逆に片方だけのバッチでは相補資源を重ねる対象がない。融合時には単に同時実行するだけでなく、デコードの余分なTensor Core使用とプリフィルの余分な帯域使用を抑えることが性能の鍵になる。
## 品質への影響
正確な注意計算を維持するカーネル実装の最適化であり、近似・量子化・枝刈りによる品質低下を伴わない。
## 既存研究との差
CUDAストリームや素朴なCTA並列は異種処理のSM共配置を保証できず、warp単位の水平融合は一方の処理が長引くstragglerとCTA同期の影響を受ける。POD-AttentionはCTAをSMへ配置した後で担当を決めるため、GPUのハードウェア配置を変更せず共配置を保証し、CTA間の独立性も維持する。NanoFlowが大きいバッチを演算単位の小バッチへ分割してCUDAストリームで異種演算を重ねるのに対し、POD-Attentionは一つのハイブリッドバッチ内部の注意を融合するため、長文で注意比率が高い条件を主対象とする。
## 限界
- 主評価はNVIDIA A100であり、HopperとFlashAttention-3への対応は論文時点で将来課題。
- 利得はプリフィルとデコードが混在するハイブリッドバッチの割合に依存し、片方だけが支配するワークロードでは小さい。
- 注意が全反復時間の小さい短文条件では端から端の改善余地も小さい。
- プリフィル・デコード比、文脈長、チャンク長によって最適なCTA構成が変わるため実行時選択が必要。
- 2GPUを超える大規模テンソル並列や異種GPUでの一般化は評価されていない。
## 実装状態
FlashAttention 2.6.1を基礎とするCUDA実装をSarathi-Serveへ統合し、GitHubのmicrosoft/vattention内pod_attn、Docker、Zenodoで成果物を公開している。ASPLOS 2025のartifact appendixに再現環境と実行コマンドが記載されている。
## 研究上の位置づけ
LLMサービングにおけるプリフィル・デコード干渉を、ノード分離やスケジューリングだけでなくGPUカーネル内の資源相補性として扱った研究である。長文ハイブリッドバッチで注意が支配的になる状況に対し、SMレベルのソフトウェア配置制御という実装可能な解を示す。
## 一次資料
- https://arxiv.org/abs/2410.18038
- https://ar5iv.labs.arxiv.org/html/2410.18038
- https://doi.org/10.1145/3676641.3715996
