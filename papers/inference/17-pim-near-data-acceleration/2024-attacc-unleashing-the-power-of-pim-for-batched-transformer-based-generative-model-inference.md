---
canonical_id: DOI:10.1145/3620665.3640422
doi: 10.1145/3620665.3640422
last_audited: '2026-09-28'
audit_version: 2
title: AttAcc! Unleashing the Power of PIM for Batched Transformer-based Generative Model Inference
summary: バッチ推論では全結合層（Fully Connected layer; FC）は重み再利用でGPU利用率を上げられる一方、生成段階の注意は各要求固有のKVキャッシュを毎トークン読み、バッチを増やしても低い演算/バイト比が残る。AttAccはこの非対称性に合わせ、FCをxPU、注意をHBMベースのメモリ内処理（Processing-In-Memory; PIM）へ分担する異種システムを設計する。PIMではGEMV演算器をDRAM bank近傍、softmaxをbuffer dieへ置き、head-level pipelineとFFN co-processingでxPU/PIMの空きを重ねる。Ramulator系シミュレータと実GPU検証を組み合わせたASPLOS 2024評価では、同一1280GB容量の従来GPU系に対し175Bモデルで最大2.81倍の性能、2.67倍のエネルギー効率を報告する。
list_summary: GPUではバッチ化しても帯域律速の注意だけが残る点を狙い、FCをxPU、KV注意をHBM-PIMへ分担するAttAcc。bank-level PIM、head-level pipeline、FFN co-processingを組み合わせ、175Bで同容量GPU系比最大2.81倍の性能・2.67倍のエネルギー効率を報告する。
authors:
- Jaehyun Park
- Jaewan Choi
- Kwanhee Kyung
- Michael Jaemin Kim
- Yongsuk Kwon
- Nam Sung Kim
- Jung Ho Ahn
published: '2024-04-27'
publication: ASPLOS 2024, pp. 103-119
publication_type: peer-reviewed-conference
publication_status: Published
lineage: inference-systems
topics:
- PIM
- HBM
- KVキャッシュ
- 注意高速化
- 異種推論
source: https://doi.org/10.1145/3620665.3640422
sources:
- https://doi.org/10.1145/3620665.3640422
- https://github.com/scale-snu/attacc_simulator
last_checked: '2026-09-28'
code: https://github.com/scale-snu/attacc_simulator
implementation: xPU側のGPUシミュレータと、Ramulator 2.0を拡張したHBM3-PIMシミュレータを公開。bank、bank-group、buffer-dieの3配置、電力制約、head-level pipeline、FFN co-processingを切り替えて評価できる。
implementation_status: official-public-simulator
hardware_evaluation: simulation-with-real-GPU-validation
hardware_details: DGX A100を基準とするシミュレーション。HBM3 5.2Gbps/pin、DGXBase 640GB、DGXLargeおよびDGX+AttAccは1280GB級容量で比較。PIM算術器はASAP7 7nmで合成し、DRAM側面積は1z-nmプロセスへ換算。シミュレータはOPT-66Bの実DGX A100結果で検証。
quality_effect: モデル演算を近似・量子化しないFP16主評価では生成品質を変えない。別途INT8感度評価も行うが、中心主張は実行配置の変更である。
evidence_locations:
- §2
- §3
- §4-6
- Figures 7-13
- §7.1-7.5
- Figures 14-17
references:
- canonical_id: arXiv:2305.13245
- canonical_id: DOI:10.1109/tcsi.2019.2945617
  doi: 10.1109/tcsi.2019.2945617
- canonical_id: DOI:10.1109/hpca51647.2021.00080
  doi: 10.1109/hpca51647.2021.00080
- canonical_id: DOI:10.1109/micro.2016.7783753
  doi: 10.1109/micro.2016.7783753
- canonical_id: DOI:10.48550/arxiv.2005.14165
  doi: 10.48550/arxiv.2005.14165
- canonical_id: DOI:10.1109/isscc.2017.7870333
  doi: 10.1109/isscc.2017.7870333
- canonical_id: DOI:10.1109/hpca.2016.7446095
  doi: 10.1109/hpca.2016.7446095
- canonical_id: DOI:10.1145/3458817.3476146
  doi: 10.1145/3458817.3476146
- canonical_id: DOI:10.1109/lca.2023.3305386
  doi: 10.1109/lca.2023.3305386
- canonical_id: DOI:10.1016/j.mejo.2016.04.006
  doi: 10.1016/j.mejo.2016.04.006
- canonical_id: DOI:10.1109/hotchips.2019.8875680
  doi: 10.1109/hotchips.2019.8875680
- canonical_id: DOI:10.1109/hpca.2015.7056040
  doi: 10.1109/hpca.2015.7056040
- canonical_id: DOI:10.1145/3352460.3358260
  doi: 10.1145/3352460.3358260
- canonical_id: DOI:10.1145/3037697.3037702
  doi: 10.1145/3037697.3037702
- canonical_id: DOI:10.1109/isca45697.2020.00071
  doi: 10.1109/isca45697.2020.00071
- canonical_id: DOI:10.1145/3579371.3589038
  doi: 10.1145/3579371.3589038
- canonical_id: DOI:10.1145/3445814.3446749
  doi: 10.1145/3445814.3446749
- canonical_id: DOI:10.1109/hpca47549.2020.00035
  doi: 10.1109/hpca47549.2020.00035
- canonical_id: DOI:10.1109/isca52012.2021.00060
  doi: 10.1109/isca52012.2021.00060
- canonical_id: DOI:10.1109/micro50266.2020.00040
  doi: 10.1109/micro50266.2020.00040
- canonical_id: DOI:10.1109/micro56248.2022.00051
  doi: 10.1109/micro56248.2022.00051
- canonical_id: DOI:10.1145/3307650.3322237
  doi: 10.1145/3307650.3322237
- canonical_id: DOI:10.1109/vlsit.2018.8510682
  doi: 10.1109/vlsit.2018.8510682
- canonical_id: DOI:10.1145/3579371.3589350
  doi: 10.1145/3579371.3589350
- canonical_id: DOI:10.1109/isca52012.2021.00010
  doi: 10.1109/isca52012.2021.00010
- canonical_id: DOI:10.1109/imw.2017.7939084
  doi: 10.1109/imw.2017.7939084
- canonical_id: DOI:10.1109/tc.2020.2984496
  doi: 10.1109/tc.2020.2984496
- canonical_id: DOI:10.1109/isca.2016.41
  doi: 10.1109/isca.2016.41
- canonical_id: DOI:10.1145/2366231.2337202
  doi: 10.1145/2366231.2337202
- canonical_id: DOI:10.1109/lca.2015.2414456
  doi: 10.1109/lca.2015.2414456
- canonical_id: DOI:10.1145/3352460.3358284
  doi: 10.1145/3352460.3358284
- canonical_id: DOI:10.1109/isca52012.2021.00013
  doi: 10.1109/isca52012.2021.00013
- canonical_id: DOI:10.1109/isscc42614.2022.9731711
  doi: 10.1109/isscc42614.2022.9731711
- canonical_id: DOI:10.1145/3123939.3123977
  doi: 10.1145/3123939.3123977
- canonical_id: DOI:10.1145/3466752.3480125
  doi: 10.1145/3466752.3480125
- canonical_id: DOI:10.1109/isbi.2008.4541126
  doi: 10.1109/isbi.2008.4541126
- canonical_id: DOI:10.1145/3123939.3124545
  doi: 10.1145/3123939.3124545
- canonical_id: DOI:10.1145/3466752.3480080
  doi: 10.1145/3466752.3480080
- canonical_id: DOI:10.1109/isscc42614.2022.9731562
  doi: 10.1109/isscc42614.2022.9731562
- canonical_id: DOI:10.1109/jssc.2022.3193354
  doi: 10.1109/jssc.2022.3193354
- canonical_id: DOI:10.1145/3460971
  doi: 10.1145/3460971
- canonical_id: arXiv:2311.18677
  arxiv_id: '2311.18677'
- canonical_id: DOI:10.1145/3579371.3589057
  doi: 10.1145/3579371.3589057
- canonical_id: DOI:10.1109/jssc.2022.3232096
  doi: 10.1109/jssc.2022.3232096
- canonical_id: DOI:10.1145/3123939.3124544
  doi: 10.1145/3123939.3124544
- canonical_id: DOI:10.1109/isvlsi.2014.94
  doi: 10.1109/isvlsi.2014.94
- canonical_id: DOI:10.1109/hoti51249.2020.00016
  doi: 10.1109/hoti51249.2020.00016
- canonical_id: arXiv:1911.02150
- canonical_id: DOI:10.1109/tcad.2018.2857044
  doi: 10.1109/tcad.2018.2857044
- canonical_id: DOI:10.1109/isscc.2018.8310252
  doi: 10.1109/isscc.2018.8310252
- canonical_id: DOI:10.1109/mcse.2010.69
  doi: 10.1109/mcse.2010.69
- canonical_id: DOI:10.48550/arxiv.1706.03762
  doi: 10.48550/arxiv.1706.03762
- canonical_id: arXiv:2012.09852
  doi: 10.1109/hpca51647.2021.00018
- canonical_id: DOI:10.1109/jssc.2019.2939682
  doi: 10.1109/jssc.2019.2939682
- canonical_id: DOI:10.1109/iedm.2016.7838333
  doi: 10.1109/iedm.2016.7838333
- canonical_id: arXiv:2211.10438
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: DOI:10.1109/lca.2022.3182387
  doi: 10.1109/lca.2022.3182387
- canonical_id: DOI:10.1109/micro50266.2020.00071
  doi: 10.1109/micro50266.2020.00071
- canonical_id: DOI:10.1109/hpca53966.2022.00082
  doi: 10.1109/hpca53966.2022.00082
references_checked_at: '2026-10-03'
references_source: crossref-deposited-reference-metadata
references_total: 68
---

# AttAcc! Unleashing the Power of PIM for Batched Transformer-based Generative Model Inference

> GPUではバッチ化しても帯域律速の注意だけが残る点を狙い、FCをxPU、KV注意をHBM-PIMへ分担するAttAcc。bank-level PIM、head-level pipeline、FFN co-processingを組み合わせ、175Bで同容量GPU系比最大2.81倍の性能・2.67倍のエネルギー効率を報告する。

## 概要

大規模言語モデル（Large Language Model; LLM）の生成では、事前充填に相当する要約段階（summarization stage）と、1トークンずつ繰り返す生成段階（generation stage）で計算特性が異なる。生成段階では、全結合層（Fully Connected layer; FC）がモデル重みを読む一方、注意層は要求ごとに異なる鍵・値キャッシュ（Key-Value cache; KVキャッシュ）を毎トークン読み直す。

通常、バッチサイズを増やすとFCは同じ重みを複数要求で再利用できるため、行列–ベクトル積に近かった処理を行列–行列積へ近づけ、GPUの演算器を使いやすくできる。しかし注意層では、各要求のKVキャッシュが別物なのでデータ自体を共有できない。バッチを増やしても演算/バイト比が低いままで、GPU計算利用率を上げても高帯域メモリ（High Bandwidth Memory; HBM）からKVを読む時間が残る。

AttAccはこの非対称性を前提に、**計算密度の高いFCはGPU/TPUのようなxPUへ残し、メモリ帯域律速の注意だけをHBM内部のメモリ内処理（Processing-In-Memory; PIM）へ移す**。PIM側ではKVをDRAM bank近傍に保持したまま行列–ベクトル積（General Matrix-Vector Multiplication; GEMV）を行い、巨大なKV全体をGPUへ運ばない。

最終ASPLOS 2024版はさらに、PIM演算器の配置、softmax配置、xPU–PIM間の実行プロトコル、head-level pipeline、FFN co-processingまで共同設計する。評価は製造済みAttAccチップの実測ではなく、実DGX A100で検証したシミュレータと論理合成に基づく。同一1280GB級メモリ容量の従来GPU系と比べ、175B生成モデルで最大2.81倍の性能、2.67倍のエネルギー効率を報告する。

## 問題設定

### バッチ化でFCは速くなるが注意は速くなりにくい

生成段階のFCでは、1要求だけならベクトル×巨大重み行列となり、重み読出しが支配的になる。複数要求を同時に処理すれば同じ重みをバッチ内で共有でき、1回読んだ重みに対してより多くの積和演算を行える。このためバッチサイズを上げるほどGPUの計算利用率が改善する。

一方、注意で読むKVキャッシュは要求ごとに異なる。各ヘッドでは現在トークンの小さなQベクトルと、過去全トークンのK/V行列を掛けるため、入力・出力に対して読まなければならないKVが非常に大きい。論文はGPT-3 175Bを例に、注意GEMVで外部へ出入りするデータ量が内部で読むKV量より桁違いに小さいことを示し、計算をメモリ側へ置けば外部帯域を節約できるとする。

さらに長い文脈ではKV容量そのものが最大バッチを制限する。バッチが小さくなるとFCの重み再利用も落ちるため、注意の容量・帯域問題が間接的にFC性能まで悪化させる。

### PIMへ全部移せばよいわけではない

PIMはメモリ内部帯域を使える一方、GPUほど高い汎用演算性能を持たない。FCまでPIMへ全面移行すると、計算密度の高い部分でGPUの強みを捨てることになる。

AttAccの設計原理は、層ごとの律速に合わせて資源を分けることである。GPU/xPUはFCを担当し、AttAccはKVを大量に読む注意を担当する。そのうえで両装置の待機時間をpipelineとco-processingで重ねる。

## AttAccの処理全体

1. 初期化時にホストがモデル構成と要求情報をAttAcc controllerへ登録する。
2. 要約段階はxPUで実行し、各decoderで生成したK/Vをその都度AttAccのHBMへ転送する。
3. 生成段階ではxPUがQ/K/V射影を計算する。
4. 新しいK/VベクトルをAttAcc側の既存KVへ追記し、QベクトルもGEMV bufferへ送る。
5. AttAccが各headのscore GEMV、softmax、context GEMVをKVの近傍で実行する。
6. attention出力だけをxPUへ戻し、projectionや残るFCをxPU側で実行する。
7. head-level pipelineとFFN co-processingでxPUとAttAccの空き時間を減らす。
8. 要求が終了するとcontrollerのrequest stateを更新し、残存要求の系列長を次生成段階へ進める。

外部interconnectを通るのはQ/K/Vの小さな新規ベクトルとattention出力が中心で、過去全KVを毎反復GPUへ読み戻す必要がない。

## 手法

### 1. GEMV演算器をどこまでDRAMへ近づけるか

論文は三つのPIM配置を比較する。

| 構成 | GEMV演算器の位置 | 特徴 |
|---|---|---|
| AttAcc-buffer | HBM buffer dieのpseudo-channel単位 | 実装しやすいが内部帯域の利用度が低い |
| AttAcc-BG | DRAM dieのbank-group単位 | より高い内部帯域、電力・面積費用も増える |
| AttAcc-bank | 各DRAM bank近傍 | 最大のbank並列性と短いデータ移動距離、最も細粒度 |

bank側へ近づけるほどKVを外へ動かさず並列GEMVできるが、演算器数、DRAMプロセス上の面積、同時動作電力が増える。AttAcc-bankではHBM3の電力制約下でもpseudo-channel当たり複数bankのGEMVを並列化し、総合的なエネルギー–遅延–面積積（Energy-Delay-Area Product; EDAP）が最良となるため最終構成に選ぶ。

論文評価ではbank-level構成の面積増加をおおむね10%以内に抑えている。つまり無限に演算器を足すのではなく、HBM電力制約を満たす同時動作数に制限する。

### 2. softmaxはbuffer dieへ置く

attentionではscore GEMVの後にsoftmax、その後context GEMVが続く。softmaxは各head全体の値を集約するため、bankごとに複製すると演算器数とSRAMが過剰になる。

そこでGEMVはbank近傍、softmaxはHBM buffer dieへ分離する。bankから集約したscoreをbuffer dieでsoftmaxし、その結果をcontext GEMVへ送り返す。GEMVほど大きな帯域を要求しないsoftmaxを浅い層へ置くことで、内部帯域と実装面積を両立する。

### 3. head-level pipelineでxPUとAttAccを重ねる

素朴に「FCを全部終えてからattention」「attention全部を終えてから次のFC」とすると、xPUとPIMが交互に待つ。AttAccはattention head単位で処理できることを利用し、あるheadをPIMで処理している間にxPUが別headのQKV生成やprojectionを進める。

PIM内部でも、あるheadのsoftmaxをbuffer dieで処理している間に別headのGEMVをDRAM側で進めるattention-level pipelineを使う。これにより異なる演算資源の空きを重ねる。

論文ではhead-level pipelineだけで素朴なDGX+AttAccに対し最大1.15倍の追加改善を報告する。一方、バッチを二分してpipelineする方式はFC側の有効バッチを減らし重み再利用を悪化させるため、評価条件では逆効果と判断している。

### 4. FFN co-processingでPIMの空き時間を再利用する

multi-head attentionとFFNの間にはlayer normalizationがあり、FFNを単純にattentionと完全重畳できない。その結果、attention終了後にPIM側が空く時間が生じる。

AttAccはFFN重みの一部をPIM側にも複製し、GPUとPIMでFF1/FF2を分担する。FF1はcolumn-wise、FF2はrow-wiseに分割し、GELUを挟んでも不要な装置間転送が増えないようにする。バッチや系列長で最適offload量が変わるため、xPU側とAttAcc側の両方へ一部重みを複製して柔軟に分担する。

このco-processingはhead-level pipelineに加えて最大約1.10倍の改善を与える。重要なのは、PIMを「注意専用固定回路」として放置せず、attention外のidle区間にも帯域型FC処理を割り当てる点である。

## 評価

### 評価条件

| 項目 | 条件 |
|---|---|
| 評価形態 | 自作シミュレータ＋Ramulator系PIMモデル＋論理合成。AttAcc実チップではない |
| 検証 | OPT-66Bを実NVIDIA DGX A100で実行しGPU側シミュレーションを較正 |
| GPU基準 | DGX A100相当 |
| メモリ | HBM3、5.2 Gbps/pin |
| DGXBase | 640GB |
| DGXLarge | 1280GB |
| DGX+AttAcc | 1280GB級でDGX側とAttAcc側へ容量分担 |
| AttAcc内部帯域 | 電力制約下で最大約242 TB/s、DGXBase集約帯域の約9倍 |
| PIM論理 | GEMV/softmax等をVerilogで設計しASAP7 7nmで合成、DRAM側面積へ換算 |
| モデル | LLaMA 65B、GPT-3 175B、MT-NLG 530B。公開simulatorではOPT-66B等も対応 |
| 精度 | 主にFP16、別途INT8感度評価 |
| ワークロード | 複数の入力長・出力長、10,000要求の処理、SLO制約あり/なし |
| 主指標 | execution time、throughput、energy/token、energy efficiency、area、EDAP |

### 代表的な結果

| 比較 | 結果 | 解釈 |
|---|---|---|
| 175B、同容量従来GPU系 | 最大2.81倍の性能 | 抽象に掲げる同容量比較のheadline |
| 175B、同容量従来GPU系 | 最大2.67倍のエネルギー効率 | KVをPIM内部で読む効果 |
| 素朴なDGX+AttAcc → head-level pipeline | 最大1.15倍追加改善 | xPU/PIM待ちを重畳 |
| pipeline後 → FFN co-processing追加 | 最大1.10倍追加改善 | PIM idle時間をFCへ利用 |
| FP16→INT8感度 | DGXBase比最大3.47倍、DGXLarge比最大2.59倍 | 低ビットでGPU側バッチも増えてもPIM利得が残る |
| AttAcc-bank | 面積増加約10%以内 | bank-level PIMの費用を明示 |

最終構成はモデルと系列長によって改善率が変わる。LLaMA 65B、GPT-3 175B、MT-NLG 530Bの個別条件では、DGXBaseに対する倍率と、同容量DGXLargeに対する倍率に大きな差がある。これはAttAccの利得の一部が「PIM帯域」だけでなく、追加KV容量によって大きなバッチを載せられることから生じるためである。

したがって公平な読み方では、640GB DGXBaseに対する大きな倍率と、1280GB DGXLargeに対する同容量比較を分離する必要がある。論文の175B headline 2.81倍は後者を含む条件での最大値として扱う。

### なぜ長文脈・大バッチで効き方が変わるか

系列長が長いほどKVキャッシュが大きくなり、attention時間と容量圧力が増えるためPIMの内部帯域が効きやすい。一方、KVが大きすぎて最大バッチが小さくなるとFCの重み再利用が低下するため、追加容量によってバッチを増やせる効果も大きい。

SLOが厳しい場合は「容量上は載る最大バッチ」より前に遅延制約がバッチ上限を決める。この領域では単にHBM容量を倍増したDGXLargeでもバッチを増やせないのに、attention自体を短縮するAttAccは上限を押し広げられる。論文がSLO別評価を行う理由はここにある。

## 既存研究との差

従来のPIM型Transformerアクセラレータには、モデルの大部分をメモリ側へ移す設計もある。しかしFCはバッチ化により演算密度を高められ、GPU/xPUの行列演算器が得意である。AttAccはPIMを万能アクセラレータとせず、**バッチ化しても低演算密度のまま残るKV attentionへ集中させる**。

通常のGPU最適化はattentionカーネルを融合してHBM往復を減らすが、decodeでは過去KVそのものを読む必要がある。AttAccはKVの保存位置と演算位置を一致させ、GPUの外部HBM帯域を経由しない点で異なる。

また単純なGPU＋PIM分業に加えて、head-level pipelineとFFN co-processingまで含める。異種装置を導入しただけでは片側の待ち時間が増えるため、処理粒度をhead単位まで細かくして重畳することがエンドツーエンド改善に必要になる。

## 限界・実装状況

最大の制約は、AttAccが製造済みPIMシステムではなくシミュレーション評価であることだ。GPU側は実DGX A100結果で検証し、PIM演算器は論理合成、メモリはRamulator系モデルを用いるが、実HBM-PIM製品でcontroller、熱、歩留まり、実interconnectを含めて測った結果ではない。

また主モデルはLLaMA 65B、GPT-3 175B、MT-NLG 530B世代で、現在一般的なグループ化問い合わせ注意（Grouped-Query Attention; GQA）、マルチ問い合わせ注意（Multi-Query Attention; MQA）、KV量子化、ページ化KV管理との組合せは主評価ではない。これらはKV帯域・容量を下げるためAttAccの相対利得を変え得る。

追加HBM-PIMはコストと実装複雑性を伴う。特にbank-level演算器はDRAM dieへロジックを追加し、電力制約下で同時動作数を制御する必要がある。面積増加が約10%以内でも、商用DRAMへ統合できることを直接実証したわけではない。

xPUとAttAcc間にもQ/K/V更新、attention出力、制御命令の転送が残る。KV全体を運ぶより小さいが、interconnectが遅い環境や小モデル・短文脈では固定費が相対的に大きくなる。

## 一般的な実装上の含意

異種アクセラレータでは、演算子を「Transformerだから同じ装置」とまとめるのではなく、実際の演算/バイト比とデータ再利用性で分けるべきである。AttAccでは、同じdecoder内でもFCはバッチで再利用できる重み中心、attentionは要求固有KV中心であり、最適装置が異なる。

またPIMを導入するときは内部帯域の最大値だけでなく、DRAM電力制約、演算器配置、softmaxの集約位置、装置間pipelineまで評価する必要がある。理論帯域が高くても、同時bank動作や転送待ちで使えなければエンドツーエンド利得にはならない。

## 一次資料

- DOI: https://doi.org/10.1145/3620665.3640422
- 公式シミュレータ: https://github.com/scale-snu/attacc_simulator

## 修正履歴

- 2026-09-28（修正済み）: 最新品質ガイドに合わせ、バッチ化でFCの演算密度は上がる一方、要求固有KVを読むattentionは帯域律速のまま残る因果背景を追加。AttAcc-buffer/BG/bankの配置比較、bank-level PIMとbuffer-die softmax、実行時KV転送、head-level pipeline、FFN co-processingを具体化した。シミュレーション条件、同容量比較、175Bで最大2.81倍性能・2.67倍エネルギー効率、面積・INT8感度、実PIM未評価という限界を表で整理し、公式シミュレータも追記した。
