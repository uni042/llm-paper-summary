---
canonical_id: DOI:10.1145/3712285.3759903
doi: 10.1145/3712285.3759903
title: 'Diff-MoE: Efficient Batched MoE Inference with Priority-Driven Differential Expert Caching'
summary: Diff-MoEはCPUに退避したMoE専門家をGPUへ読み込む際、層ごとの常駐高優先キャッシュ、短期再利用用の中優先キャッシュ、共有の一時低優先キャッシュを分ける。オフラインで大域的に頻出する専門家を固定し、オンラインの活性頻度から短期的に頻出する専門家を優先保存し、6層GRUで次のMoE層の専門家を予測して転送を重ねる。単一H200のSwitch-Base/Largeで、DeepSpeed-Offload比平均2.74倍、Pre-gated MoE比2.22倍、MoE-Infinity比1.55倍の処理量改善を報告。メモリ消費は他のオフロード方式より多い。
list_summary: Diff-MoEは層別の固定・動的・一時キャッシュと専門家予測を組み合わせ、バッチ推論の専門家転送を減らしてDeepSpeed比平均2.74倍の処理量改善を報告する。
authors:
- Kexin Li
- Wenkan Huang
- Qinggang Wang
- Long Zheng
- Xiaofei Liao
- Hai Jin
- Jingling Xue
published: 2025-11
publication: Proceedings of SC 2025, pp. 1951–1965 (November 2025)
publication_type: peer-reviewed conference paper
publication_status: published
source: https://doi.org/10.1145/3712285.3759903
sources:
- https://dl.acm.org/doi/pdf/10.1145/3712285.3759903
- https://dl.acm.org/doi/10.1145/3712285.3759903
implementation: NVIDIA FasterTransformerを基盤とし、層別の専門家キャッシュとPyTorch 6層GRU予測器を実装。論文のArtifact Descriptionに再現用資産を記載するが、公式の恒久公開URLは本稿確認時点で未検証。
code: null
last_checked: '2026-10-30'
worker_id: scheduled-chat-00
worker_completed_at: '2026-10-30T01:48:00+09:00'
worker_run_key: 20261030-0145-scheduled-chat-45/r01
reference_main_sha: f58938feee07830ed68765a638cb207d03adecd1
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: DOI:10.1109/sc41405.2020.00073
  doi: 10.1109/sc41405.2020.00073
- canonical_id: arXiv:2207.00032
  doi: 10.1109/sc41404.2022.00051
- canonical_id: DOI:10.48550/arxiv.2210.11416
  doi: 10.48550/arxiv.2210.11416
- canonical_id: arXiv:1412.3555
  arxiv_id: '1412.3555'
- canonical_id: DOI:10.18653/v1/2024.acl-long.70
  doi: 10.18653/v1/2024.acl-long.70
- canonical_id: DOI:10.18653/v1/n19-1423
  doi: 10.18653/v1/n19-1423
- canonical_id: arXiv:2312.17238
  doi: 10.48550/arxiv.2312.17238
- canonical_id: arXiv:2502.06888
  doi: 10.48550/arxiv.2502.06888
- canonical_id: arXiv:2101.03961
- canonical_id: arXiv:2502.17298
  doi: 10.48550/arxiv.2502.17298
- canonical_id: arXiv:2206.03382
- canonical_id: DOI:10.1109/isca59077.2024.00078
  doi: 10.1109/isca59077.2024.00078
- canonical_id: DOI:10.48550/arxiv.2401.04088
  doi: 10.48550/arxiv.2401.04088
- canonical_id: arXiv:2402.07033
  openreview_id: N5fVv6PZGz.
- canonical_id: arXiv:1909.05858
  arxiv_id: '1909.05858'
- canonical_id: arXiv:2310.02410
  doi: 10.48550/arxiv.2310.02410
- canonical_id: arXiv:2006.16668
  openreview_id: qrwe7XHTmYb.
- canonical_id: DOI:10.18653/v1/2020.acl-main.703
  doi: 10.18653/v1/2020.acl-main.703
- canonical_id: DOI:10.1145/3649329.3656507
  doi: 10.1145/3649329.3656507
- canonical_id: arXiv:2402.14800
  doi: 10.18653/v1/2024.acl-long.334
- canonical_id: DOI:10.18653/v1/d18-1206
  doi: 10.18653/v1/d18-1206
- canonical_id: DOI:10.48550/arxiv.2303.08774
  doi: 10.48550/arxiv.2303.08774
- canonical_id: DOI:10.3390/info14040242
  doi: 10.3390/info14040242
- canonical_id: DOI:10.18653/v1/d16-1264
  doi: 10.18653/v1/d16-1264
- canonical_id: DOI:10.1162/tacl_a_00266
  doi: 10.1162/tacl_a_00266
- canonical_id: arXiv:1910.01108
  arxiv_id: '1910.01108'
- canonical_id: arXiv:1701.06538
  openreview_id: B1ckMDqlg.
- canonical_id: arXiv:2410.22134
  doi: 10.48550/arxiv.2410.22134
- canonical_id: DOI:10.1145/3649329.3655945
  doi: 10.1145/3649329.3655945
- canonical_id: DOI:10.1109/micro61859.2024.00040
  doi: 10.1109/micro61859.2024.00040
- canonical_id: DOI:10.1109/micro56248.2022.00088
  doi: 10.1109/micro56248.2022.00088
- canonical_id: DOI:10.1145/3431920.3439288
  doi: 10.1145/3431920.3439288
- canonical_id: DOI:10.1109/hpca53966.2022.00022
  doi: 10.1109/hpca53966.2022.00022
- canonical_id: DOI:10.1145/3390523
  doi: 10.1145/3390523
- canonical_id: DOI:10.1109/iccv48922.2021.00009
  doi: 10.1109/iccv48922.2021.00009
- canonical_id: DOI:10.1109/tpami.2023.3275156
  doi: 10.1109/tpami.2023.3275156
- canonical_id: arXiv:2401.14361
  arxiv_id: '2401.14361'
- canonical_id: arXiv:2411.01016
  doi: 10.18653/v1/2024.findings-emnlp.612
- canonical_id: arXiv:2205.10034
  doi: 10.1109/tsc.2024.3399654
- canonical_id: DOI:10.1109/micro61859.2024.00105
  doi: 10.1109/micro61859.2024.00105
- canonical_id: DOI:10.48550/arxiv.2402.14891
  doi: 10.48550/arxiv.2402.14891
references_checked_at: '2026-10-29'
references_source: crossref-deposited-reference-metadata
references_total: 57
---

# Diff-MoE：大規模バッチでも専門家の局所性を保つ三段階GPUキャッシュと先読み

## 書誌・対象

Li、Huang、Wang、Zheng、Liao、Jin、Xueによる2025年のACM会議論文（DOI:10.1145/3712285.3759903）。Mixture-of-Experts（MoE）型言語モデルでは、各トークンが一部の専門家だけを実行するため演算量を抑えられるが、全専門家の重みをGPUメモリへ常駐させると容量を圧迫する。Diff-MoEは専門家の大部分をCPUメモリに置き、GPUにある限られたキャッシュを大規模バッチ推論で効率よく使う仕組みである。2026年10月30日にACM原著PDF全15ページのAlgorithm 1、Figure 5〜14、実験条件、付録を確認した。

## 概要

単純なオンデマンドオフロードでは、ゲートが専門家を選んでからCPUからGPUへ重みを転送するため、転送完了まで計算が待つ。先読み方式も存在するが、バッチを大きくすると同時に活性化される専門家が増え、1層の計算時間で隠せる転送数を超える。全層で共有するLRUキャッシュでは、一つの大きなバッチが多数の専門家を要求するとキャッシュがほぼ入れ替わり、次の生成ステップで同じ層の専門家を再利用できない。

Diff-MoEは活性の二種類の局所性を利用する。推論全体で頻出する専門家は大域的ホットとして固定し、短い生成区間で繰り返し使われる専門家は局所的ホットとして優先度を動的に更新する。GPUキャッシュを層別の高優先（HPC）・中優先（MPC）と全層共有の低優先（LPC）へ分け、次のMoE層で使われそうな専門家を軽量予測器で先読みする。Switch-BaseのXSum評価ではDeepSpeed-Offload比1.99〜3.46倍、平均2.74倍、Pre-gated MoE比平均2.22倍、MoE-Infinity比平均1.55倍のトークン処理量を報告する。ただしキャッシュを多く残すため、他のオフロード方式よりGPUメモリを多く使う。

## 問題設定：バッチ拡大で転送が増える

MoEのゲートは入力トークンごとに専門家を選ぶ。バッチ1では少数の専門家だけが必要でも、バッチ64では複数要求の選択集合の和が大きくなり、同じ層で多数の専門家をGPUへ読み込むことになる。DeepSpeed-Offloadは選択後の転送を待ち、Pre-gated MoEは次層を先読みするが、バッチ64で34専門家が活性化する場合でも計算に重ねて隠せる転送は約2専門家分に限られる。MoE-Infinityは全層で共有するキャッシュを持つが、36専門家分のキャッシュへ34専門家を要求すると入れ替わりが頻発し、同じ層の次ステップで再利用できない。

Diff-MoEの着眼点は、活性化された専門家をすべて同じ優先度で扱わないことである。モデル全体で常に使われる少数と、現在の入力系列・短時間だけ繰り返す専門家を分ければ、限られた容量でも再利用率を高められる。専門家の移動量を減らすことは、転送を隠す時間が短い大バッチ条件で特に重要である。

## 手法

### 1. 専門家の優先度を初期化・更新する

オフラインのタスク適応時に各MoE層で活性頻度を数え、上位N個を大域的ホット専門家としてHPCへ固定する。これらの優先度は最大値MaxPに設定し、推論中も変更しない。その他の専門家は優先度0から開始し、推論時のゲート選択に応じて更新する。活性化された専門家はΔincだけ加点し、GPUに残っているが選ばれなかった専門家はΔdec_inだけ減点し、GPU外で非活性の専門家はΔdec_outだけ減点する。原著ではΔinc=1、Δdec_in=0.4、Δdec_out=0.2であり、キャッシュ内で使われない専門家を速く降格させる。

優先度がthreshold_hot以上の非大域専門家を局所的ホット、それ未満をコールドと分類する。threshold_hotはΔincと等しく、1回活性化された専門家は中優先キャッシュへの候補になる。MaxPをthreshold_hotの2倍にして、活性が繰り返された専門家には短い非活性期間を耐える余地を残す。ただし差を大きくしすぎると古い専門家が居座り、小さすぎると再利用前に追い出される。優先度は単なるLRU時刻ではなく、最近の活性と継続的な使用を反映する。

### 2. 高・中・低優先キャッシュを分離する

各MoE層のHPCは大域的ホット専門家を固定し、MPCは短期的に頻出する専門家を保持する。MPCの容量はHPCの2倍とする。全層共有のLPCは、現在の層で必要になった未キャッシュ専門家を一時保持する領域と、次層の予測専門家を先読みする領域を持つ。実際の計算時にはゲートが選んだ専門家がHPC・MPC・LPCに存在するかを調べ、なければCPUメモリからLPCへ読み込む。必要な専門家が揃ったらバッチ内トークンを専門家ごとに集めて実行し、出力を元の順序へ戻す。

計算後、LPCのうち局所的ホットと判定された専門家は、その層のMPCへ昇格する候補になる。MPCに空きがあれば追加し、満杯なら現在のMPC内でthreshold_hot未満に落ちた低優先専門家を候補と交換する。全員がthreshold_hot以上なら交換しない。この制約が、バッチの一時的な大量要求でキャッシュ全体が入れ替わるのを防ぐ。残った一時LPCは解放し、次層の先読み分だけを引き継ぐ。

### 3. 次のMoE層の専門家を予測する

専門家の活性には層間の相関があるため、著者は6層GRUをPyTorchで学習する。タスク適応時に収集した活性履歴を8:2に分けて学習・検証し、現在のMoE層で選ばれた専門家IDと履歴状態から、次層で各専門家が使われる確率分布を出す。バッチでは各サンプルの確率分布を集約し、すでにHPC/MPCに存在する専門家を除外して上位候補を選ぶ。バッチ4以下では1専門家、それより大きいバッチでは最大2専門家を先読みする。

この上限は任意の節約ではなく、現在の層の計算中に隠せる転送数から決める。バッチ4から64へ増えても計算時間は約1.26倍にしか増えず、34専門家を全て先読みする時間はない。複数層先の予測を増やすと直近で必要な転送を妨げる可能性があるため、次のMoE層だけを予測する。予測が外れた場合は通常のオンデマンド転送へ戻るので、予測器の精度と転送を隠す時間が実効利得を左右する。

### 4. 1層を通る処理の全体像

入力トークンのゲートが専門家集合を決め、優先度管理器が活性履歴を更新する。GPU上にない専門家はLPCへ転送され、各専門家の計算を実行する。終了後にLPCの専門家をMPCへ昇格するか破棄するか決め、次層の予測分布から未キャッシュ専門家を選んで転送を開始する。これを各MoE層で繰り返す。高優先の固定保存、中優先の層別再利用、低優先の一時受け皿、次層先読みの4つが連結して初めて、バッチ拡大時の転送待ちを削減できる。

## 評価

### 実験環境・比較条件

| 項目 | 原著の条件 | 解釈 |
|---|---|---|
| GPU | NVIDIA H200 141GB、単一GPU | 高帯域・大容量GPUでの実機評価 |
| CPU・DRAM | Xeon Gold 6430×2、ホストDRAM 1TB | 専門家をCPU側に保持 |
| 転送 | PCIe 5.0、双方向128GB/s | オフロードの通信条件 |
| 実装 | NVIDIA FasterTransformerベース | 他ランタイムへの性能外挿不可 |
| モデル | Switch-Base 7B、Switch-Large 26B | 12/24層、半数がMoE、各層128専門家 |
| タスク | XSum要約、SQuAD QA、CoQA対話QA | 3種類の入力分布 |
| デフォルト | top-1ルーティング、キャッシュ比率α=5%、次層先読み最大2専門家 | 比率は2/5/10%でも比較 |
| 比較 | No-Offload、DeepSpeed-Offload、Pre-gated MoE、MoE-Infinity | No-Offloadは容量を使う上限参考 |
| 指標 | tokens/s、GPUピークGB、キャッシュ命中率、tokens/(GB·s) | 速度とメモリ効率を分離 |

No-Offloadは全重みをH200へ載せる参考上限であり、オフロード方式と同じメモリ使用量ではない。MoE-Infinityとは同じキャッシュ容量（Switch-Baseのα=5%で36専門家）を揃えて比較する。したがって「全重み常駐より常に速い」という研究ではなく、GPUメモリを節約しつつオフロード方式の転送待ちを減らすことが対象である。

### 処理量とバッチ拡大の影響

Switch-BaseのXSumでは、DeepSpeed-Offload比1.99〜3.46倍（平均2.74倍）、Pre-gated MoE比1.66〜2.82倍（平均2.22倍）、MoE-Infinity比1.19〜1.93倍（平均1.55倍）を報告する。バッチ64ではDeepSpeedが約18千tokens/s、Pre-gated MoEが22千、MoE-Infinityが36千、Diff-MoEが61.5千となる。これらは原著Figure 7の特定モデル・タスクの測定であり、モデルやタスクを変えた平均と混同しない。

バッチ64でSwitch-Base/LargeとXSum・SQuAD・CoQAを比較したFigure 8では、DeepSpeed比1.72〜3.37倍、Pre-gated比1.60〜2.82倍、MoE-Infinity比1.30〜3.27倍の範囲でDiff-MoEが上回る。バッチが大きいほど活性化する専門家が増え、単純なオンデマンド転送や全層共有キャッシュでは通信が支配的になる。一方、Diff-MoEは大域・局所の再利用を保持するため、転送量の増加を抑えられる。

### GPUメモリとメモリ効率

原著Figure 9では、Diff-MoEのGPUピークメモリは全重み常駐の平均約16%であるが、DeepSpeed-Offloadの1.36倍、Pre-gated MoEの1.13倍を消費する。キャッシュを多く残すことで通信を減らす方式なので、同じGPU容量で最も小さいメモリ使用量を達成する研究ではない。メモリ効率（tokens/(GB·s)）ではFigure 10でNo-Offload比平均5.16倍、DeepSpeed比1.97倍、Pre-gated比1.60倍と報告する。速度だけを示して容量費用を隠してはいけない。

### キャッシュ容量の感度と命中率

キャッシュ比率αを2%、5%、10%で比較すると、2%では頻出専門家を十分に保持できず、10%では処理量の追加改善が小さい一方でメモリを消費する。原著は5%が速度と容量の均衡に優れると結論する。Figure 12のバッチ64では、MoE-Infinityの命中率約19%、LRU約7%に対してDiff-MoE約49%。バッチ128では比較方式がほぼ0%に落ちてもDiff-MoEは約29%を維持する。小バッチでは全層共有キャッシュが柔軟なため、LRUとの差が小さい条件もある。

### 次層予測器の精度と立ち上がり

Figure 14の次層専門家予測では、バッチ1のtop-1精度が56.3%、バッチ16ではtop-1/top-2とも90%超、バッチ64では約98%と報告する。バッチ内で各サンプルの予測確率を集約すると、頻出専門家が強調されるためである。ただし予測器の学習には事前の活性履歴が必要で、未知の分布やタスクへ直ちに同じ精度で適用できる保証はない。原著は長期の分布変化に伴う再学習コストを主な評価軸としていない。

## 限界・負の結果

第一に、GPUメモリ消費は他のオフロード方式より多い。5%キャッシュで平均16%の全重み常駐メモリを使い、DeepSpeedの1.36倍、Pre-gatedの1.13倍になる。GPU容量が厳しい場合、処理量の改善と引き換えに必要なキャッシュ容量を確保できない可能性がある。2%では命中率が落ち、10%では追加メモリの割に利得が小さい。

第二に、実験はSwitch-Base/Largeのtop-1専門家と特定の3タスク、単一H200＋PCIe 5.0に集中する。専門家の共有度、ルーティング分布、活性専門家数が異なる巨大MoE、複数GPU・複数ノード、NVLink上の専門家分散、低帯域PCIeでは転送と計算の均衡が変わる。モデルの推論品質を改善する研究ではなく、同じモデルの専門家実行を高速化するシステムである。

第三に、GRU予測器は事前の活性履歴で学習する。バッチ1ではtop-1予測精度が約56%にとどまり、予測を増やしすぎると不要な転送が帯域を奪う。そこで最大2専門家・次層のみの予測に制限している。異なるタスクへ切り替わるときの予測器の適応速度や継続学習の費用は、今回の評価だけでは定量的に保証されない。

## 既存方式との差・適用範囲

DeepSpeed-Offloadは必要時に専門家を転送するため、バッチが大きいほど待ちが増える。Pre-gated MoEは先読みするが、同時に活性化する専門家の増加を計算時間で隠しきれない。MoE-Infinityは共有キャッシュの再利用を狙うが、バッチが大きいと層をまたぐ入れ替わりが激しい。Diff-MoEは層別HPC/MPCと共有LPCを分け、優先度更新によって短期再利用を守り、GRUの次層予測を補助的に使う。主たる貢献は単独の予測精度ではなく、**大バッチでも層ごとの専門家局所性を失わないキャッシュ管理**にある。

## 一次資料と照合範囲

- ACM原著PDF（全15ページ、Algorithm 1、Figure 5〜14、§3〜7、付録）：https://dl.acm.org/doi/pdf/10.1145/3712285.3759903 。2026年10月30日に直接取得して手法・評価表・負の条件を確認した。
- 出版社書誌：https://dl.acm.org/doi/10.1145/3712285.3759903 。DOIと著者を確認した。
- 実験値は原著のSwitch-Base/Large、H200、PCIe 5.0、キャッシュ比率5%を基準として記載し、No-Offloadとオフロード方式のメモリ条件の違いを明記した。

## 書誌メタデータ修復（2026-10-30）

SC 2025の会議開催月に基づき出版月を2025-11と記載し、書誌記録に合わせて著者順と掲載ページ1951–1965を整えた。原著本文に基づく技術説明・数値は維持した。
