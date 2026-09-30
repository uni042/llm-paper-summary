---
canonical_id: "arXiv:2507.19635"
title: "Efficient and Scalable Agentic AI with Heterogeneous Systems"
authors: "Zain Asgar, Michelle Nguyen, Sachin Katti"
summary: "エージェント処理をLLM推論・KV保存・tool call・memory lookup・CPU処理等の動的dataflow graphへ分解し、MLIR表現、resource cost model、SLA制約付き配置最適化、異種runtimeでCPU/GPU/acceleratorへ配置するシステム設計を提案する。実測に較正した性能モデルではB200::Gaudi3が総じて高いTCO効率を示し、H100::Gaudi3がB200::B200と同等以上になる条件も報告する。"
list_summary: "エージェント実行グラフを細粒度operatorへ分解し、計算・メモリ・帯域とSLAを基に異種CPU/GPU/acceleratorへTCO最小化配置する。"
worker_completed_at: "2026-10-01T05:56:25+09:00"
worker_run_key: "20261001-0556-scheduled-chat-00"
reference_main_sha: "2b09804c68bab047ea6bce22654156580391198d"
source: "https://arxiv.org/abs/2507.19635"
---

# Efficient and Scalable Agentic AI with Heterogeneous Systems

## 概要
AIエージェントは単一LLM呼び出しではなく、音声認識、複数LLM推論、検索、ツール呼び出し、KVキャッシュ、CPU上の整形処理などが条件分岐・反復を伴って接続された動的ワークロードである。全処理を最新GPUだけで動かすと、ネットワーク待ちやメモリ容量中心の処理にも高価な計算資源を割り当てることになる。

本論文はエージェントを有向データフローグラフとして表し、各nodeをさらに細粒度operatorへ分解して、計算量・メモリ帯域・容量・ネットワーク・CPU能力に応じて異種hardwareへ配置する設計を提案する。MLIR（Multi-Level Intermediate Representation）を中間表現に使い、hardwareごとの実装を生成し、runtime orchestratorがend-to-endのサービス水準合意（service-level agreement; SLA）を満たす配置を選ぶ。評価は実測値で較正した性能モデルを使い、H100、B200、Gaudi 3、MI300X等の異種prefill/decode組合せの総保有コスト（total cost of ownership; TCO）を比較する。

## 問題設定
エージェントグラフ内のresource bottleneckはnodeごとに異なる。LLM prefillは計算量が大きく、decodeはKVアクセスによるメモリ帯域依存が強い。KV storeは容量とnetwork I/O、tool callは外部network latency、JSON処理等はCPUが中心になる。均質GPU clusterでは、この異質性を無視してすべての処理に同じ高価なresource bundleを購入する。

さらに、個別operatorの最安hardwareを選ぶだけでは不十分である。異種device間のstate transfer、tensor parallel通信、prefill→decode KV転送がend-to-end latencyへ加算されるため、配置問題はgraph dependencyと通信費を含めて解く必要がある。

## 手法
### エージェントを動的dataflow graphへ変換
workloadを `G=(V,E)` とし、nodeをAgent、Tool Call、Model Execution、Memory、General Purpose Compute、Control Flow等として表す。Model Executionはさらにprefill/decodeへ分割でき、KV cacheは独立stateとして表現する。edgeはtoken、hidden state、tool output、control signal等の依存を持ち、同期・非同期・条件分岐・有限反復も表現する。

### resource cost modelと配置最適化
各task `i` とhardware class `j` について、compute、memory、bandwidth等のresource demandとdevice性能を使って実行時間を見積もり、static latency、data movement、communication overheadを加える。各taskをどのhardwareへ割り当てるかを、cost最小化とlatency/capacity/throughput制約の最適化問題として解く。論文の仮定下では凸最適化へ落とせる。

### MLIRとruntime orchestration
graphをMLIR系の中間表現へ落とし、operatorごとに異なるbackend codeを生成できるようにする。runtimeは配置計画に従ってoperatorをCPU、NVIDIA GPU、Intel Gaudi、AMD accelerator等へdispatchし、必要なstateをnetwork経由で移動する。prefill/decode分離では左deviceがprefill、右deviceがdecodeを担当する `A::B` 表記で構成を評価する。

## 評価条件
|項目|内容|
|---|---|
|モデル|Llama 3 8B / 70B、FP16 / FP8|
|hardware候補|A40、A100、Gaudi 3、MI300X、H100、B200|
|interactive SLA|TTFT ≤ 250 ms、token間時間 ≤ 20 ms|
|offline目的|maximize tokens/s/$|
|系列1|input 512 / output 4096（decode-heavy）|
|系列2|input 4096 / output 512（prefill-heavy）|
|TCO|4年償却、金利8%、電力$0.40/kWh、最大TDP仮定|
|性能|hardware実測にfitした性能モデルによるsimulation|
|parallelism|tensor / pipeline parallelism、disaggregated inference|

## 主要結果
B200::Gaudi 3はFP8を中心にinteractive・batch双方で最良のTCO benefitを示し、B200::B200よりも利得が残る。H100::Gaudi 3も多くの条件でB200::B200と同等かやや良く、既存Hopper世代をGaudi 3と組み合わせれば全面的なBlackwell更新を避けられる可能性を示す。

prefill-heavy条件ではGaudi 3のcost-performanceが効き、decode-heavy条件でも少し長いtoken間遅延を許容できればGaudi 3が低い限界費用から選ばれる。tensor parallel度を上げる初期段階ではlatencyが下がるが、さらに増やすとdevice間通信が支配し、計算利得を打ち消す。これはoptimizerがcompute性能だけでなくnetwork costを含める必要性を裏付ける。

## 既存研究との差
vLLM等は主に単一モデルサービング内部を最適化し、prefill/decode分離も一つのモデルpipelineを対象とする。本論文はそれらをエージェントgraphの一nodeとして扱い、tool call、memory lookup、CPU処理まで同じ配置問題へ含める。hardwareも同一vendor・同一世代に限定せず、vendorをまたぐ異種構成をTCOとSLAで選ぶ。

## 限界
主要TCO結果は、hardware測定へfitした**性能モデル上のsimulation**であり、全組合せを実clusterでend-to-end測定した結果ではない。hardware価格は2025年6月頃の公開販売情報、電力・償却条件も仮定であり、実データセンターのcolocation費や非反復エンジニアリング費は含まない。異種device間のcompiler/runtime統合、network fabric、vendor差によるkernel対応が実配備の追加費用になる。したがって「H100+Gaudi 3が常にB200より安い」という一般則ではなく、論文のcost modelとSLA条件での結果として読む必要がある。

## 一次資料
- https://arxiv.org/abs/2507.19635
- https://arxiv.org/pdf/2507.19635