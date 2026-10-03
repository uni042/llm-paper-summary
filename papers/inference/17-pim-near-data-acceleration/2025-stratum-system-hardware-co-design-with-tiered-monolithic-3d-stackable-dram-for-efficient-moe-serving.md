---
canonical_id: DOI:10.1145/3725843.3756043
arxiv_id: '2510.05245'
doi: 10.1145/3725843.3756043
title: 'Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving'
summary: モノリシック3D積層可能DRAM（Monolithic 3D-Stackable DRAM; Mono3D DRAM）の高い内部帯域を近メモリ処理（Near-Memory Processing; NMP）へ使い、縦方向の層ごとに異なるアクセス遅延を8段階の内部メモリ階層として積極利用するMoE推論基盤。話題分類から専門家の利用確率を予測し、hot expertを高速tierへ置く。MICRO 2025のcross-layer評価ではGPU基準比で復号スループットをOLMoE 8.29倍、Mixtral 5.39倍、Qwen2.5 6.13倍、Llama-4 4.48倍、エネルギー効率を最大7.66倍に改善する。
list_summary: Mono3D DRAM＋近メモリ処理をGPUと統合し、層ごとの遅延差を8-tier化、話題別のhot expert配置へ利用してGPU比最大8.29倍の復号スループットを示す。
publication: MICRO 2025
publication_type: conference
publication_status: Published
published: '2025-10-18'
lineage: inference-systems
topics:
- MoE
- 近メモリ処理
- 3D DRAM
- expert placement
source: https://doi.org/10.1145/3725843.3756043
sources:
- https://doi.org/10.1145/3725843.3756043
- https://arxiv.org/abs/2510.05245
last_checked: '2026-09-28'
last_audited: '2026-09-28'
audit_version: 2
authors:
- Yue Pan
- Zihan Xia
- Po-Kai Hsu
- Lanxiang Hu
- Hyungyo Kim
- Janak Sharda
- Minxuan Zhou
- Nam Sung Kim
- Shimeng Yu
- Tajana Rosing
- Mingu Kang
code: null
implementation: Mono3D DRAMをロジックdieへCu-Cu hybrid bondingし、GPUとは2.5D silicon interposerで接続する提案architecture。NMP processor、8-tier memory mapping、topic-aware hot/cold expert placementとSLO-aware request dispatchを共同設計する。
implementation_status: architecture-and-simulator-described-no-official-code-confirmed
hardware_evaluation: cross-layer simulation / modeling
hardware_details: Stratum-S/L/XLをRTX A6000/H100級GPU baselineと比較。Mono3D DRAM device・circuit・architecture modelとNMP system simulationを統合し、実製造されたStratum siliconの測定ではない。
quality_effect: expert routing自体を近似して別expertへ置換するのではなく、topic別の利用確率を主に物理配置とrequest schedulingへ使う。予測missは主に性能へ影響し、元のexpert計算を省略する設計ではない。
evidence_locations:
- sections 2-4
- section 6
- figure 16
- figure 17
- table 4
arxiv_categories:
  primary: cs.AR
  cross_list: []
references:
- canonical_id: DOI:10.1109/ieeestd.2019.8766229
  doi: 10.1109/ieeestd.2019.8766229
- canonical_id: DOI:10.1109/isscc.2017.7870333
  doi: 10.1109/isscc.2017.7870333
- canonical_id: DOI:10.1109/iedm13553.2020.9371905
  doi: 10.1109/iedm13553.2020.9371905
- canonical_id: arXiv:2403.04132
  arxiv_id: '2403.04132'
- canonical_id: arXiv:1904.10509
  arxiv_id: '1904.10509'
- canonical_id: DOI:10.1109/isscc49657.2024.10454327
  doi: 10.1109/isscc49657.2024.10454327
- canonical_id: DOI:10.1109/vlsitechnologyandcir46783.2024.10631471
  doi: 10.1109/vlsitechnologyandcir46783.2024.10631471
- canonical_id: DOI:10.1109/mm.2023.3256796
  doi: 10.1109/mm.2023.3256796
- canonical_id: DOI:10.1109/mm.2021.3061394
  doi: 10.1109/mm.2021.3061394
- canonical_id: arXiv:1803.05457
  arxiv_id: '1803.05457'
- canonical_id: arXiv:2110.14168
  arxiv_id: '2110.14168'
- canonical_id: arXiv:2401.06066
  arxiv_id: '2401.06066'
- canonical_id: arXiv:2501.12948
  arxiv_id: '2501.12948'
- canonical_id: arXiv:2412.19437
  arxiv_id: '2412.19437'
- canonical_id: arXiv:2010.11929
  arxiv_id: '2010.11929'
- canonical_id: arXiv:2112.06905
  arxiv_id: '2112.06905'
- canonical_id: arXiv:2101.03961
  arxiv_id: '2101.03961'
- canonical_id: arXiv:2502.06643
  arxiv_id: '2502.06643'
- canonical_id: arXiv:2407.21783
  arxiv_id: '2407.21783'
- canonical_id: DOI:10.23919/vlsitechnologyandcir57934.2023.10185290
  doi: 10.23919/vlsitechnologyandcir57934.2023.10185290
- canonical_id: arXiv:2410.17954
  arxiv_id: '2410.17954'
- canonical_id: DOI:10.1109/mnano.2025.3533815
  doi: 10.1109/mnano.2025.3533815
- canonical_id: DOI:10.1109/iedm50854.2024.10873439
  doi: 10.1109/iedm50854.2024.10873439
- canonical_id: DOI:10.1109/hcs55958.2022.9895480
  doi: 10.1109/hcs55958.2022.9895480
- canonical_id: arXiv:2401.04088
  arxiv_id: '2401.04088'
- canonical_id: arXiv:2001.08361
  arxiv_id: '2001.08361'
- canonical_id: arXiv:2402.07871
  arxiv_id: '2402.07871'
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: DOI:10.1109/tcsi.2024.3362822
  doi: 10.1109/tcsi.2024.3362822
- canonical_id: DOI:10.1145/3123939.3123977
  doi: 10.1145/3123939.3123977
- canonical_id: arXiv:2409.02060
  arxiv_id: '2409.02060'
- canonical_id: DOI:10.1145/3123939.3124545
  doi: 10.1145/3123939.3124545
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: DOI:10.1145/3620665.3640422
  doi: 10.1145/3620665.3640422
- canonical_id: DOI:10.1109/isscc42614.2022.9731562
  doi: 10.1109/isscc42614.2022.9731562
- canonical_id: DOI:10.1145/3460971
  doi: 10.1145/3460971
- canonical_id: DOI:10.1109/isscc49661.2025.10904543
  doi: 10.1109/isscc49661.2025.10904543
- canonical_id: arXiv:2411.19799
  arxiv_id: '2411.19799'
- canonical_id: DOI:10.1109/isvlsi.2014.94
  doi: 10.1109/isvlsi.2014.94
- canonical_id: arXiv:2409.16040
  arxiv_id: '2409.16040'
- canonical_id: arXiv:2507.20534
  arxiv_id: '2507.20534'
- canonical_id: DOI:10.1109/ectc.2016.155
  doi: 10.1109/ectc.2016.155
- canonical_id: arXiv:1706.03762
  arxiv_id: '1706.03762'
- canonical_id: DOI:10.18653/v1/w17-4413
  doi: 10.18653/v1/w17-4413
- canonical_id: DOI:10.1109/ted.2024.3520074
  doi: 10.1109/ted.2024.3520074
- canonical_id: arXiv:2401.14361
  arxiv_id: '2401.14361'
- canonical_id: arXiv:2412.15115
  arxiv_id: '2412.15115'
- canonical_id: arXiv:2401.08383
  arxiv_id: '2401.08383'
- canonical_id: arXiv:2409.01141
  arxiv_id: '2409.01141'
- canonical_id: arXiv:2205.01068
  arxiv_id: '2205.01068'
references_checked_at: '2026-10-03'
references_source: arxiv-html-reference-section
references_total: 92
---

# Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving

> Mono3D DRAM＋近メモリ処理をGPUと統合し、層ごとの遅延差を8-tier化、話題別のhot 専門家配置へ利用してGPU比最大8.29倍の復号スループットを示す。

## 概要

混合専門家モデル（Mixture of Experts; MoE）は、各トークンで少数の専門家だけを実行するため演算は疎にできる。しかし専門家 FFNはモデル 重みの大部分を占めるので、**そのトークンで使わない専門家も含め、全専門家の重みをどこかへ保存する必要がある**。特にデコードは1 step当たりの計算量が小さく、必要重みをメモリから読む時間が相対的に大きいため、GPUの演算器よりメモリ 帯域が律速になりやすい。

Stratumはこの問題を「より多くのHBMを載せる」だけでは解かない。提案するモノリシック3D積層可能DRAM（Monolithic 3D-Stackable DRAM; Mono3D DRAM）は、DRAM cell 層を縦方向へ大量に積み、logic dieと細かいCu-Cu hybrid bondingで接続する。従来HBMのTSVより細密な垂直接続を使えるため、メモリ stack内部では非常に高い帯域をlogic側へ供給できる。

ただしGPUとの2.5D silicon interposerを通る外部帯域は依然として限られる。そこで専門家計算と注意機構の一部をメモリ近傍の近メモリ処理（Near-Memory Processing; NMP）へ移し、巨大重みを毎回GPUへ運ばず、その場で処理する。

Mono3D DRAMには別の癖がある。縦に数百〜1024 層まで伸ばすと、wordlineの長さと寄生抵抗・容量が位置によって変わり、上層と下層でaccess 遅延が均一でなくなる。通常なら最悪遅延に合わせてメモリ全体を遅く動かすところを、Stratumはこの不均一性を **8段階のメモリ tier** として利用する。

さらにMoEでは専門家利用頻度がリクエスト topicに依存するという観察から、話題分類で次に使われやすい専門家を推定し、hot 専門家を速いtier、cold 専門家を遅いtierへ置く。つまりStratumの中心は、**新しいメモリ technologyの内部遅延差を欠点ではなく専門家 配置の資源へ変えること**にある。

MICRO 2025のcross-層評価では、GPU 比較対象比の平均デコード スループットがOLMoEで8.29倍、Mixtralで5.39倍、Qwen2.5で6.13倍、Llama-4で4.48倍。Energy 効率は最大7.66倍を報告する。ただしこれは製造chipの実測ではなく、device/circuit/構成/システムを跨いだシミュレーション・modeling結果である。

## 問題設定

### HBMの「GPU外側bandwidth」だけでなく、memory内部も使う

HBMは多数のDRAM dieをTSVでstackし、GPUへ広いinterfaceを提供する。しかしデコードのようなメモリ律速 ワークロードでは、GPU compute capabilityが増えても重み/KVの供給が追い付かなければ演算器は待つ。

HBM base dieへNMPを置く既存方式は、GPUまでdataを運ばない点では有利だが、DRAM dieからbase dieへ抜けるTSVの本数・pitchが内部帯域の上限になる。StratumがMono3D DRAMに注目する理由は、メモリ cell 層とlogic dieの間をより細かなhybrid bondingでつなぎ、stack内部帯域をNMPから直接使えるためである。

### 1024 layer級の縦積層ではaccess latencyが均一でない

Mono3D DRAMのwordlineはstaircase構造で外へ引き出される。Layer位置によってルーティング lengthが変わるため、積層数を増やすほどaccess 遅延差が大きくなる。

全層を最遅層に合わせれば制御は簡単だが、高速層の性能を捨てることになる。Stratumはメモリ address spaceをaccess 遅延別に8 tierへ分け、速いtierへ頻繁に読むdataを集める。

ここでMoEとの相性が良い。すべての専門家を同頻度で読むわけではないため、hot/coldを正しく予測できれば、容量は全tierを使いながら、実際のaccessの多くを高速tierへ偏らせられる。

## 手法のあらまし

Stratumは三層の設計からなる。

1. **Hardware:** Mono3D DRAMをlogic dieへhybrid bondingし、NMP processorを置く。GPUとはsilicon interposerで接続する。
2. **Memory mapping:** DRAM 層を遅延で8 tierへ分け、専門家/注意機構 dataをNMPのlocalityとtier速度に合わせて配置する。
3. **Serving システム:** リクエスト topicを軽量classifierで分類し、topicごとの専門家 活性値 profileからhot/cold 専門家を決める。SLOを守りながら同topic リクエストをqueue/分配し、hot dataを高速tierで再利用しやすくする。

入力はリクエスト topicと事前測定した専門家 活性値 frequency、出力は専門家の物理tier配置とリクエスト 分配 orderである。Inference中はルーティングが本来選んだ専門家を実行し、topic predictionは「どの専門家を速いメモリへ置くか」のhintとして使う。

## 手法

### 1. Mono3D DRAM + NMP — expert weightをGPUまで往復させない

Mono3D DRAM stackの下に高性能logic dieを置き、専門家 FFNと注意機構向けのprocessing unitを実装する。Memory cellとlogicをCu-Cu hybrid bondingで接続するため、外部interposerへ出る前の高い内部帯域を計算へ使える。

Expert FFNでは重みをNMP近傍から読み、その場でmatrix operationを進める。AttentionでもKVをメモリ側で処理する。結果だけをGPU側と交換すればよく、巨大な重み/KV trafficを外部interfaceへ毎回流す量を減らせる。

ただしNMP unit同士の通信が新たな律速にならないよう、論文は専門家/注意機構 data mappingとprocessing パイプラインを共同設計し、計算・活性値・processing-unit間通信を重ねる。

### 2. 8-tier in-memory tiering — 最悪latency基準をやめる

縦方向の層 遅延を測定モデルから分類し、Mono3D DRAMを8 tierへ区切る。Fast tierは小容量だが低遅延、slow tierはより遅いという階層として扱う。

No-tiering方式では最も遅い層に合わせたtimingをメモリ全体へ適用する。Tieringでは各領域を実際の遅延に近いtimingで使えるため、同じMono3D DRAMでもeffective 帯域が上がる。

評価ではtiering + optimized mappingがno-tieringに対しモデルに応じて約1.32〜1.45倍の追加スループットをもたらす。したがって8.29倍というheadlineの全てが「新メモリだから」ではなく、**遅延 heterogeneityをシステムから利用する部分にも独立した寄与がある**。

### 3. Topic-aware hot expert placement — request内容から速いtierを使うexpertを決める

MoE ルーティングの専門家 活性値にはtopic localityがある。同じ分野の質問が続けば、一部専門家が繰り返し選ばれやすい。

Stratumは軽量topic classifierでリクエストを粗いtopicへ分類し、offline profileしたtopic別専門家 活性値 probabilityを参照する。利用確率の高い専門家をhotとしてfast tierへ、低い専門家をcoldとしてslow tierへ配置する。

ここで予測を外してもモデル出力の専門家を変更するわけではない。Cold tierにある専門家を読むため遅くなるだけなので、qualityではなくperformanceのmissになる。この性質により、aggressiveな配置 predictionを使いやすい。

### 4. Topic-aware scheduling — hot expertの再利用とSLOを両立する

Expert 配置だけをtopic-awareにしても、リクエストがtopic A→B→C→Aのように高速で切り替わればhot setの交換が頻発する。そこでスケジューラは同topic リクエストをまとめて処理し、hot 専門家配置を再利用する。

一方、バッチ形成のために待ち過ぎれば遅延 SLOを破る。Stratumはtopic localityを高めるqueueingとSLO制約を組み合わせ、専門家 swap回数とリクエスト待ち時間を両方制御する。

論文のworst-case寄りのswap検証でも、短い系列・バッチ 1で連続リクエストのtopicが異なる条件におけるswap オーバーヘッドは1%未満の時間割合として報告される。通常caseだけでなく、topic変化のコストを別評価している点が重要である。

## 評価

### 代表的な評価条件

| Model | Model規模 / 専門家構成 | GPU 比較対象 | Stratum構成 |
|---|---|---|---|
| OLMoE-1B-7B | 7B total、64 エキスパート / top-8 | RTX A6000 | Stratum-S |
| Mixtral 8×7B | 約47B、8 エキスパート / top-2 | H100 ×2 | Stratum-L |
| Qwen2.5-32B | 32B 密 | H100 ×2 | Stratum-L |
| Llama-4 Scout | 約109B、shared + 16 エキスパート / top-1 | H100 ×4 | Stratum-XL |

GPU側はvLLM系のスループット-oriented 推論提供を基準にし、Stratum側はMono3D DRAM device/circuit モデルとNMP システム シミュレーションを組み合わせる。Qwen2.5という密 モデルも含め、MoE固有の専門家-配置効果だけでなく、NMP/注意機構側の寄与も分けて見られる構成になっている。

### 代表的な結果

| Model | Decode スループット vs GPU | Energy 効率 vs GPU |
|---|---:|---:|
| OLMoE | 8.29× | 7.66× |
| Mixtral | 5.39× | 2.74× |
| Qwen2.5 | 6.13× | 3.51× |
| Llama-4 | 4.48× | 4.87× |

Decode lengthが長くなるほどGPU 比較対象は注意機構のメモリ trafficで強くメモリ律速になり、Stratumとの差が広がる。Headlineの最大値だけでなく、全4 モデルで方向が揃っている点がシステム-level主張を支える。

### Tieringの寄与

| Model | Tiering + mapping のno-tiering比 |
|---|---:|
| OLMoE | 約1.45× |
| Mixtral | 約1.39× |
| Qwen2.5 | 約1.32× |
| Llama-4 | 約1.34× |

これは「Mono3D DRAMを使う」ことと、「その内部遅延差を8-tierとして使う」ことを分離するablationである。最悪遅延へ揃えるだけでもHBMより内部帯域は高いが、tier-aware mappingでさらに伸びる。

### Expert placementの感度

Hot 専門家 hit rateが高くなるほどMoE MLP 遅延は下がり、システム スループットは上がる。論文のtopic predictionではモデルごとにhot-専門家 hit率が異なり、ルーティング localityが強いモデルほど配置 benefitも得やすい。

したがってtopic classificationが難しいdomain、topicが頻繁に切り替わるtraffic、専門家利用がほぼ均一なMoEでは、話題別tieringの追加利得は縮む。逆にMono3D/NMP自体のbenefitはそれとは独立して残る。

## 既存研究との差

HBM-based PIM/NMPはGPUまでのdata movementを減らすが、HBM stack内部ではTSV帯域が制約になり得る。StratumはMono3D DRAMの高密度hybrid bondingを使い、**メモリ内部帯域を大きくした上でlogic die NMPへ渡す**点がハードウェア側の差である。

一方、MoE-Infinityや専門家 キャッシュ型のオフロードは既存CPU/GPU/SSD階層で「何を先読み・キャッシュするか」を最適化する。Stratumは新メモリ technologyの内部にfast/slow tierそのものを作り、topic-aware 配置を物理メモリ layoutへ落とす。

つまりsoftware-onlyな専門家 キャッシュの代替ではなく、専門家 localityをメモリ deviceの遅延 heterogeneityへ直接対応付けるハードウェア-システム co-designである。

## 限界・実装状況

最重要の制約は、Stratumが市販GPUへsoftwareだけで導入できる技術ではないことだ。Mono3D DRAM、hybrid bonding、専用logic die、NMP processorを前提にする新構成である。

また評価はcross-層 シミュレーション/modelingであり、Stratum-S/L/XLを実製造してGPU 比較対象と同一rackで測った結果ではない。Device 遅延、power、interconnect、NMP utilizationのモデル誤差が最終スループット/energyへ影響する。

Topic-aware 配置の利得は専門家 活性値 localityに依存する。Traffic distributionが学習/profile時から変化するとhot set予測が悪化し、tier swapが増える。SLO-aware スケジューラもtopic groupingのためリクエストを待たせるので、極端に低trafficなtopicではbatching benefitが得にくい。

一方、paperはno-tiering、hot-hit-rate sensitivity、専門家 swap オーバーヘッドを個別に評価しており、headline 高速化倍率だけでは見えない依存条件をある程度切り分けている。

## 一般的な実装上の含意

Memory technologyの「不均一性」は、常に最悪値へ揃えて隠す必要はない。Access frequencyを予測できるワークロードでは、遅延の異なる物理領域をsoftware-visibleなtierへ変換し、hot data 配置へ使える。

MoEはその好例で、専門家 活性値が疎かつ偏るため、全専門家を最速メモリへ置けなくても、**よく使う専門家だけをfast tierへ置けば平均access timeを大きく下げられる**。この発想はCXL、HBM tier、DRAM/NVMe階層にも一般化できる。

## 一次資料

- MICRO 2025 / DOI: https://doi.org/10.1145/3725843.3756043
- arXiv: https://arxiv.org/abs/2510.05245

## 修正履歴

- 2026-09-28（修正済み）: 最新品質ガイドに合わせ、汎用的な「観測・選択・資源削減」説明を削除。Mono3D DRAMとHBMの内部帯域差、z方向遅延 heterogeneity、8-tier メモリ、NMP execution、topic-aware hot/cold 専門家 配置、SLO-aware スケジューラを因果順に説明。OLMoE/Mixtral/Qwen2.5/Llama-4のGPU 比較対象、スループット・energy表、tiering ablation、hot-hit-rate依存、シミュレーション scopeを追記。
