---
canonical_id: "DOI:10.1109/CCGrid68966.2026.00023"
arxiv_id: null
doi: "10.1109/CCGrid68966.2026.00023"
openreview_id: null
arxiv_categories: {primary: null, cross_list: []}
last_audited: "2026-10-01"
audit_version: 1
storage_targets: ["GPU HBM", "CPU DRAM", "EBS/NVMe-class storage", "remote attention GPU"]
bottlenecks: ["KV cache capacity", "PCIe/storage bandwidth", "network bandwidth", "cloud VM cost"]
hardware_details: "AWS GPU instances including T4, A10G, L4, L40S; evaluation over multiple offloading topologies"
quality_effect: "近似ではなく配置・オフロード方式選択であり、モデル品質そのものは変更しない。"
evidence_locations: ["CCGrid 2026 paper, Sections III-VI, Tables VII-VIII"]
references: []
references_checked_at: "2026-10-01"
references_source: "primary-reference-section"
references_total: 29
title: "LLM-PILOT: SLO-Aware and Cost-Efficient LLM Serving on Public Cloud VM Clusters via Offloading"
summary: "長文脈LLMではKVキャッシュがGPUメモリを圧迫するため、ホストメモリやストレージへのKVオフロード、別GPUへの注意計算オフロードが有効になるが、AWSのVMはGPU・CPU・メモリ・ネットワーク帯域を固定セットで販売するため、最安の構成はワークロードとSLOによって変わる。LLM-PILOTはScale-up、Multi-pass、KV cache offloading、Attention offloadingとVM組合せを共通探索空間に置き、計算・PCIe/ストレージ・ネットワーク・待ち行列を含む階層的性能モデルを線形回帰で校正し、TTFT/TBT/TPS制約を満たす候補の中から費用効率最大の構成を選ぶ。AWS実機では決定的環境でMAPE 6%以内、共有AOの待ち行列を含む条件でもR² 0.89以上を示し、High-End比2.05倍、既存方式比最大2.31倍の費用効率を報告した。"
list_summary: "KV退避・注意計算退避・VM構成をSLO制約下で同時探索し、I/Oと待ち行列まで校正した性能モデルでAWSの費用効率を既存方式比最大2.31倍へ改善するLLM-PILOTを提案。"
authors: ["Jinwoo Kim", "Kihyun Kim", "Hyunsun Chung", "Jihoon Yang", "James J. Kim", "Dong Li", "Youngjae Kim"]
authors_affiliations: "Sogang University; Soteria Inc.; University of California, Merced"
published: "2026-05-01"
publication: "IEEE CCGrid 2026"
publication_type: "conference"
publication_status: "Published"
lineage: "cloud LLM serving / KV offloading / attention offloading / cost optimization"
topics: ["KV cache offloading", "attention offloading", "SLO", "cloud serving", "cost optimization"]
importance: "オフロード方式単体ではなく、クラウドVMの固定資源束とSLOを含めて構成選択を自動化する。"
hardware_evaluation: "AWS実機＋トレース駆動評価"
source: "https://doi.org/10.1109/CCGrid68966.2026.00023"
sources: ["https://discos.sogang.ac.kr/file/2026/intl_conf/CCGRID_2026_J_Kim.pdf"]
code: ""
implementation: "分析性能モデルと探索器。KVO/AO/単一GPU/Multi-passを統一モデル化。"
worker_completed_at: "2026-10-01T15:51:00Z"
worker_run_key: "scheduled-chat-45-20261001-1545"
last_checked: "2026-10-01"
---

# LLM-PILOT: SLO-Aware and Cost-Efficient LLM Serving on Public Cloud VM Clusters via Offloading

> KV退避・注意計算退避・VM構成をSLO制約下で同時探索し、I/Oと待ち行列まで校正した性能モデルでAWSの費用効率を既存方式比最大2.31倍へ改善するLLM-PILOTを提案。

## 概要

長文脈LLMのデコードでは、過去トークンのKVキャッシュを毎ステップ参照するため、系列長とバッチが増えるほどGPUメモリ容量と帯域が支配的になる。高価な大容量GPUへ単純に拡張する代わりに、KVをCPUメモリやストレージへ退避するKVキャッシュ・オフロード（KVO）、あるいはKVを保持する別GPUへ注意計算自体を移す注意計算オフロード（AO）が使える。しかしクラウドVMではGPU、DRAM、ネットワーク、ストレージ帯域が独立に購入できず、例えばネットワーク帯域を上げるためだけに不要なメモリやCPUまで増やす必要がある。

LLM-PILOTはこの構成選択を、サービス品質目標（Service-Level Objective; SLO）を満たす候補の中で費用効率を最大化する問題として解く。候補には高性能単一GPU、メモリ不足時のMulti-pass、CPU/ストレージKVO、1:1・並列・共有AOを含める。各方式のプリフィル・デコード時間を、GPU計算量、KV転送量、PCIe/ストレージ帯域、ネットワーク帯域、共有AOの待ち行列から解析的に予測し、実機との差を線形回帰で校正する。

AWS実機では、単一L40Sの計算律速条件でR²=0.99、MAPE約2%台、1:1 AOでもR² 0.95以上・MAPE 6.2%以下を示した。ストレージKVOではI/O変動のため誤差が増えるが、それでも構成の優劣を探索するモデルとして利用する。最終的な構成選択ではHigh-End戦略比2.05倍、既存方式比最大2.31倍の費用効率を達成し、既存方式ではSLO違反となる資源負荷の高い領域でも実行可能な構成を見つけた。

## 問題設定

KVキャッシュ量は概ねバッチ、総系列長、層数、隠れ次元、精度に比例する。長文脈と大バッチを同時に扱うと、モデル重みが収まっていてもKVがGPU HBMを使い切る。KVOは容量問題を外部メモリへ逃がせるが、デコードごとに蓄積KVを転送するため系列長に比例してI/Oが増える。AOはKVを補助GPU側へ置き、主GPUから現在トークンの活性値だけを送って注意結果を返すため、長文脈で転送量が系列長に比例しにくい一方、毎トークンのネットワーク通信と補助GPU待ち行列が新たな制約になる。

クラウドではさらに、インスタンスの資源が束になっている。論文のAWS例では、同じT4系列でもネットワーク帯域を25から50Gbpsへ上げるためにホストメモリが16から128GiBへ増え、料金も大きく上がる。したがって「最速GPU」「最安GPU」「KVOを使う」といった単一ルールではなく、ワークロードの入力/出力長、バッチ、TTFT、トークン間時間（TBT）、必要TPS、料金を同時に見る必要がある。

## 手法のあらまし

利用者はモデル、ワークロード、予算、SLOを入力する。LLM-PILOTは利用可能VMとScale-up、Multi-pass、KVO、AOの組合せから探索空間を作る。次に各候補についてプリフィルとデコードの解析性能モデルを評価し、事前の少量プロファイルから得た線形回帰係数で理論値を実機寄りに補正する。SLOを満たさない候補を除外し、残った候補について有効スループットを料金で割った費用効率を比較する。

## 手法

### 1. SLOを満たした後の過剰性能を価値として数えない

リアルタイムサービスではTPS下限に加えてTTFTとTBTの上限を課し、バッチサービスでは主にTPS下限を課す。費用効率では実TPSをそのまま使わず、必要TPSを上限とした有効スループットを用いる。つまりSLOを十分超えて高速な高価GPUが、必要以上の速度だけで有利にならない。SLOを満たす候補では有効スループットが同じになるため、実質的に「要求性能を満たす最小費用構成」を探す問題へ変換される。

### 2. KVO — 容量を外部へ逃がす代わりに系列長依存I/Oをモデル化する

KVO候補では、GPUに残すKV割合と外部へ置く割合から必要転送量を計算し、CPUメモリやEBS等の実効帯域で転送時間を見積もる。注意計算は主GPUで行うため、外部KVを毎デコードステップに取り込む必要があり、長文脈ほど転送時間が増える。ストレージKVOは容量単価を下げられる一方、EBS帯域や実効I/Oの揺らぎが大きく、性能モデル誤差も増える。

### 3. AO — KVと注意計算を補助GPUへ置き、転送量を現在トークン中心にする

AOでは主GPUがQKV射影や全結合層を担当し、補助GPUがKVを保持して注意計算を行う。主GPUは現在ステップの活性値を送り、補助GPUから注意結果を受け取る。KVOのように蓄積KV全体を毎回移動しないため、論文のモデルではAO転送量は系列長ではなく主にバッチに比例する。長文脈ほどこの差が大きくなるが、ネットワーク往復が毎トークン発生するため低帯域VMではTBTを満たせない。

AOは1:1だけでなく、K組を並列にしてバッチを分割する構成と、複数主GPUが1台のAO機を共有するN:1構成を扱う。並列AOは費用を増やして遅延を下げる。共有AOは利用率を上げるが、要求が集中すると待ち行列が生じるため、LLM-PILOTはM/D/1待ち行列の平均待ち時間をデコード時間へ加える。負荷率が1へ近づくと待ち時間が急増し、SLO違反リスクが高まる。

### 4. Multi-pass — メモリ不足を分割実行で回避する代替案も同じ探索空間に置く

単一GPUでKVが収まらない場合、バッチをk個の小バッチへ分けて逐次処理するMulti-passも候補に含める。追加VMや外部転送は不要だが、各小バッチが独立実行されるため全体時間は概ねk倍になり、スループットが下がる。オフロードを導入する複雑さや料金と、単純分割による性能低下を同じSLO・費用基準で比較できる点が重要である。

### 5. 線形回帰校正 — 理論FLOPs/帯域と実機の差を少量プロファイルで吸収する

解析モデルだけでは、注意の不規則メモリアクセス、カーネル起動、共有資源競合、実効帯域低下を正確に表せない。そこで予測時間Tpredに対し、実測時間Treal = β1 Tpred + β0の線形補正をハードウェア構成ごとに学習する。β1は理論性能からの効率低下、β0は固定遅延を吸収する。これは構成ごとの一度きりのオフライン費用であり、実行時のLLM推論へ追加処理を入れない。

## 評価

### 代表的な評価条件

| 項目 | 代表設定 |
|---|---|
| クラウド | AWS、N. Virginiaのインスタンス料金・仕様 |
| 主なGPU | T4、A10G、L4、L40S等 |
| High-End比較 | g6e.2xlarge、L40S 48GB |
| AO比較 | g5.xlarge主GPU + g4dn.4xlarge AO機 |
| KVO比較 | g4dn.xlarge + EBSストレージ |
| InferSave比較 | g5.4xlarge、必要時g5.8xlargeへ拡張 |
| バッチ範囲 | B=1〜32、代表スナップショットB=32 |
| ワークロード例 | 生成128/1024、均衡512/512、要約1024/128（入力/出力） |

### 代表的な評価結果

| 条件 | 指標 | 結果 | 読み取れること |
|---|---|---:|---|
| L40S単一GPU | R² / MAPE | 0.99 / ≤2.3% | 計算律速では解析モデルが実機を高精度に追従 |
| 1:1 AO | R² / MAPE | ≥0.95 / ≤6.2% | ネットワークを含めても校正後は実用的な予測精度 |
| 共有AO N:1 | R² / MAPE | 0.93〜0.95 / 5.8〜7.1% | 待ち行列を明示モデル化する必要性を確認 |
| ストレージKVO | R² / MAPE | 0.89〜0.94 / 8.2〜11.2% | I/O変動が最大の予測誤差源 |
| 構成最適化 | 費用効率 | High-End比2.05倍 | 必要以上の高性能VMを避ける効果 |
| 構成最適化 | 費用効率 | 既存方式比最大2.31倍 | オフロード方式とVMを同時選択する効果 |

B=32の実測/予測例では、High-End生成ワークロードが39.4秒/38.5秒、1:1 AOが68.5秒/65.2秒、ストレージKVOが368.5秒/335.2秒だった。KVOは容量を大きく拡張できるが、長い生成では蓄積KVのI/Oが支配的になり、単純に「安価な外部容量を使えば得」とはならない。一方AOは長文脈で転送量の系列長依存を抑えられるが、ネットワーク帯域と共有時の待ち行列がSLOを決める。

## 既存研究との差

InferSaveはホストメモリKVOを用いてクラウド費用とSLOを扱うが、複数VMによるAOやストレージKVOまで同じ探索空間に入れない。MélangeやSplitWiseのような異種GPU配置研究はGPU内にKVが収まる前提が強く、長文脈でKVがGPU容量を超える場合の外部階層を十分扱わない。LLM-PILOTは「どのオフロード方式を使うか」と「どのVMを何台組み合わせるか」を分離せず、I/Oと料金、SLOを一体で探索する点が中心的な差である。

## 限界・実装状況

性能モデルは少量プロファイルによる校正を必要とし、新しいGPU・ネットワーク・ストレージ構成では係数を取り直す必要がある。特にストレージKVOはI/O変動が大きく、MAPEが10%前後まで上がる条件がある。共有AOも負荷率が1へ近づくと待ち時間が非線形に増えるため、平均モデルだけで尾部遅延を完全に保証するわけではない。評価はAWS中心であり、他クラウドの料金体系や専用相互接続へそのまま一般化できるとは限らない。

## 一般的な実装上の含意

オフロードの可否をGPUメモリ容量だけで決めるべきではない。KVOは外部容量の単価と帯域、AOはネットワークと補助GPU料金、共有構成は待ち行列まで含めて比較する必要がある。また、SLOを超える余剰性能を費用効率へ加点しない設計にすると、クラウドの過剰プロビジョニングを避けやすい。

## 一次資料

- DOI: 10.1109/CCGrid68966.2026.00023
- https://discos.sogang.ac.kr/file/2026/intl_conf/CCGRID_2026_J_Kim.pdf