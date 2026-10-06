---
canonical_id: "DOI:10.1109/JIOT.2024.3524255"
title: "EdgeShard: Efficient LLM Inference via Collaborative Edge Computing"
summary: "EdgeShardは異種edge deviceとcloudの計算・memory・link帯域を考慮し、LLM layerを連続shardへ分割してdevice選択と配置を動的計画法で同時最適化する。15台の実機testbedでLlama2 7B/13B/70Bを評価し、最大50%のlatency削減と約2倍のthroughputを達成し、単体deviceではOOMする70Bも協調実行する。"
list_summary: "異種edge/cloud資源へLLM 層 shardを動的計画法で配置し、通信と計算を同時に最適化して単体メモリを超えるLLM推論を可能にする。"
authors: ["EdgeShard authors"]
published: "2025-05"
publication: "IEEE Internet of Things Journal"
publication_type: "journal"
publication_status: "published"
source: "https://doi.org/10.1109/JIOT.2024.3524255"
sources: ["https://doi.org/10.1109/JIOT.2024.3524255","https://arxiv.org/abs/2405.14371"]
implementation: "12 Jetson AGX Orin、2 Jetson Orin NX、RTX 3090 cloud serverからなる15-device testbedでLlama2 7B/13B/70Bを実測。"
code: null
last_checked: "2026-10-06"
worker_completed_at: "2026-10-06T13:42:00+09:00"
worker_run_key: "20261006-1330-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
EdgeShardは、1台ではメモリ不足になるLLMを複数のedge deviceとcloud serverへ層単位で分割する協調推論方式である。単純な均等分割では、deviceごとの演算性能・メモリ容量とリンク帯域が違うため、遅い段または大きな活性値転送がパイプライン全体を律速する。そこでdevice選択とモデル partitionを同時に解く。

## 問題設定
edge-onlyでは大規模モデルがOOMし、cloud オフロードでは低帯域WANが活性値転送を支配する。モデル圧縮は品質損失を伴い得る。EdgeShardは重みを削らず、各層の計算コストと層境界で生じる通信コストを配置問題として扱う。

## 手法
Transformerの連続層をshardとしてdeviceへ割り当て、前段の隠れ 活性値を次deviceへ転送する。候補deviceにはメモリ上限、演算速度、相互帯域があり、あるpartitionが実行可能かをまず制約で判定する。

最適化はdevice selectionとpartition boundaryを組み合わせ、遅延またはスループット目的を最小化/最大化する動的計画法で解く。均等層数ではなく、速いdeviceへ重い区間を寄せたり、狭いリンクを跨ぐ回数と転送量を抑えたりできる。

## 評価条件
|項目|内容|
|---|---|
|edge|12×Jetson AGX Orin 32GB、2×Jetson Orin NX 16GB|
|cloud|RTX 3090 24GB server|
|モデル|Llama2 7B / 13B / 70B|
|比較|single edge、均等cloud-edge、最適化cloud-edge等|
|指標|遅延、トークン/s、OOM可否、帯域感度|

## 主要結果
Llama2-7BではEdgeShardが75.88ms、52.45 トークン/sを達成し、single-device系の約140ms・約24 トークン/sに対して遅延をほぼ半減、スループットを約2.2倍にする。13Bでもcloud-edge 比較対象比で遅延を28.8～45.7%削減し、スループットを約2.2倍へ高める。

70Bは単一edgeや一部比較対象がメモリ不足で実行不能なのに対し、EdgeShardは複数deviceへ重みを分散して推論可能にする。これは速度改善だけでなく、aggregate メモリを使って実行可能モデル サイズを拡張する効果である。

## 既存研究との差・限界
単純cloud オフロードと違い、cloud依存を固定せずedge間も含めてshard配置を選ぶ。重み 量子化のようにモデル表現を変えないので精度を落とさない。一方、パイプライン境界の活性値転送はリンク帯域に敏感で、低帯域では通信が支配する。評価は特定Jetson/3090構成であり、modern datacenter interconnect向けテンソル 並列化との直接比較ではない。