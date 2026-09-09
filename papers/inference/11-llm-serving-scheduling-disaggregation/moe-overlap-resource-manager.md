---
canonical_id: "arXiv:2609.07536"
arxiv_id: "2609.07536"
title: "Analytical Resource Management for Fine-grained MoE Computation-Communication Overlap"
summary: "分散MoEの細粒度な計算・通信重畳で競合する計算CTAと通信CTAのGPU常駐資源を、依存関係と離散的な実行waveを明示した解析モデルから起動時に配分し、COMETの固定通信CTA数をworkload適応型に置き換える。"
source: "https://arxiv.org/abs/2609.07536"
last_audited: null
audit_version: 0
---

# Analytical Resource Management for Fine-grained MoE Computation-Communication Overlap
## 書誌情報
- **著者**: Hongyu Liu, Minyu Cui, Miquel Pericàs
- **公開**: arXiv:2609.07536v1, 2026-09-07; accepted at AI on HPC Workshop at SC26
- **種別**: workshop paper / arXiv preprint
- **対象**: Mixture-of-Experts inference、computation-communication overlap、GPU resource management、analytical performance modeling、CTA residency
- **実装**: 公開COMET A100実装をFLUX codebase内で拡張し、起動時の解析的resource managerを統合。評価はCOMET A100 V2 commit 19831caを基準に実施。
## 問題設定
細粒度重畳ではGEMM2計算CTAとGatherRS通信CTAが同じSM常駐資源を競合する。通信CTA不足ではready splitが滞留し、多すぎるとGEMM2並列度が落ちる。CTAは整数waveで進むため最適配分はtoken数、expert負荷、kernel shape、split数に対して不連続に変わり、固定CTA数では適応できない。
## 新規性
workload、kernel occupancy、GPU常駐制約、split-level readiness依存から候補kernelを実行・計測せず通信CTA数Cを起動直前に解析選択する。計算・通信のwave数と依存関係を同一timelineに置くwave-quantized makespan modelを用いる。
## 手法
Cから通信常駐予約R(C)と残存計算容量P(C)を導出し、router由来expert tile数とcommunication tile数を整数waveへ写像する。split公開時刻と通信完了時刻の再帰から最終makespan T(C)を計算し、C=1..16で最小候補を選ぶ。

### Dependency-constrained residency partition
R(C)=ceil(C/o_comm)、P(C)=o_comp(G-R(C))。A100ではo_comm=1、o_comp=2、G=108。

### Wave-quantized workload model
routed expert countとkernel tile shapeからcompute tile数、token数・world size・hidden dimensionからcommunication tile数を求め、離散wave数へ変換。

### Split-readiness recurrence
compute公開時刻と先行split通信完了を結合してpipeline fill・steady state・drainを予測。

### Relative service-rate normalization
固定C=16で得た基準service rateをreduction dimension、compute tile size、world sizeで補正。

### Launch-time CPU selector
最大16候補をO(E+L|C|)で評価。候補GPU kernelの試行やper-shape winner tableは不要。

既存dispatch後にtile shape、resident blocks/SM、host routed counts、GPU SM数を読み、選択したCでGatherRS通信CTA gridと計算側常駐上限を設定する。元のGEMM2/GatherRS kernel、routing、通信量、readiness protocolは変更しない。
## 評価条件
- **Hardware**: single node with four NVIDIA A100-SXM4-40GB GPUs、NVLink interconnect、108 SMs available to target operator
- **Software**: PyTorch 2.7.1、CUDA 12.6、NCCL 2.26.2、CUTLASS commit df8a550、COMET A100 V2 commit 19831ca、FLUX codebase
- **Model**: Granite-3.1-1B-A400M、Qwen1.5-MoE-A2.7B、DeepSeek-V2-Lite
- **Dataset / Trace**: LMSYS-Chat-1M router traces、uniform routing、real-router p50、real-router p90
- **Baseline**: upstream COMET、Megatron core-TE、FastMoE TP+NCCL、measured oracle sweep C=1..16 for predictor accuracy
- **Correctness**: COMETと提案法は同一input、weight、router assignment、GEMM tile、通信量を使い、4-rank allcloseとcomplete-model出力一致を確認。Hugging Face参照に対して全モデルでlast-token top-1を保持し、Qwen/DeepSeek-V2-Liteはelementwise allcloseも通過。
- **precision**: BF16
- **parallelism**: TP=4/EP=1, TP=2/EP=2, TP=1/EP=4; TP×EP=4
- **batch and sequence**: B=4; S in {1024,2048,4096,8192,16384}
- **routing matrix**: 3 models × uniform/p50/p90 × 5 lengths = 45 configurations per TP/EP configuration
- **measurement**: 20 warmups; operator/layer 60 ABBA-interleaved samples; complete-model/multi-backend 20 samples; median maximum-rank latency; 20,000 block-stratified bootstrap replicates for 95% CI
predictor accuracyはTP=4/EP=1のreal-p90 15 workloadでC=1..16を実測sweepしたoracleと比較。性能はtarget operator、complete post-router MoE layer、complete-model prefillの3境界で評価。
single-node A100/NVLinkのprefill中心。complete-model評価はonline-serving全体やdecode throughputを表さない。
## 主要結果
解析selectorは実測oracleに近いCを低overheadで選び、COMETの固定resource partitionを全評価configurationで改善した。効果はtarget operatorで最大だが、layer全体とcomplete-model prefillにも残る。

- mean predictor regret / 3.22% (baseline: measured oracle; condition: 15 real-p90 TP=4/EP=1 workloads; maximum 10.21%) — per-shape計測なしでもoracle近傍を選択。

- mean solver overhead / 0.157 µs (baseline: standalone analytical selector; condition: launch-time CPU selection) — dispatch経路に対して小さい。

- GEMM2+GatherRS geometric-mean speedup / 2.528× (baseline: COMET; condition: all TP/EP configurations) — maximum 4.218×。

- complete post-router MoE layer geometric-mean speedup / 1.771× (baseline: COMET; condition: all TP/EP configurations) — maximum 2.584×。

- complete-model prefill geometric-mean speedup / 1.185× (baseline: COMET; condition: all TP/EP configurations) — maximum 1.439×。

- TP=2/EP=2 model-level geometric means / 1.336× / 1.211× / 1.232× (baseline: COMET; condition: Granite / Qwen / DeepSeek-V2-Lite) — S>=4096の全feasible pointでCOMET、Megatron core-TE、FastMoE TP+NCCLより高速。

- lowest observed speedup / 1.058× (baseline: COMET; condition: Qwen complete-model prefill, TP=4/EP=1, S=1024) — 全3測定境界・全TP/EP構成でpointwise minimumが1×超。

### 負の結果・境界条件
- **short-input backend crossover**: S=1024ではMegatron core-TEが3モデルすべてで最速。Qwen S=2048でもMegatron core-TEが提案法より高速。
- **DeepSeek memory boundary**: DeepSeek-V2-Lite complete-model prefillのB=4,S=16384はA100 40GBでOOM。
- **architecture scope**: service-rate parameterとlegal C rangeはA100/NVLink kernel family向けに再導出されており、他GPU/多nodeへそのまま移植できない。

主因はwork量削減ではなく同一計算・通信仕事の常駐資源再配分。token tileが増え複数waveになるほど固定partitionの不整合が顕在化し、モデル全体でも利益が蓄積する。
## 品質への影響
FLOPs、routing、通信量、model semanticsを変えずnumerical correctnessを保持するため、accuracy trade-offを導入しない。
## 既存研究との差
- COMET/FLUX/TileLinkなどが細粒度重畳の実行機構や依存表現を作るのに対し、本研究はその機構が存在する前提でcompute/communication CTAの常駐比を起動時に決める。
- NanoFlowやLagomのprofiling・measurement-guided searchと異なり、per-shape candidate executionなしの解析選択を行う。
- DeepEP V2の通信資源解析やStream-Kのwave quantizationと関連するが、非preemptive CTA residencyとsplit-level readiness依存を結合したMoE operator固有のmakespan最適化を対象とする。
## 限界
- 現実装とservice-rate calibrationはsingle-node A100/NVLink kernel family向け。他GPUではoccupancy、tile work、dependency recurrence、legal C range、service rateを再導出する必要がある。
- 最適化対象はGEMM2+GatherRSで、AllGather+GEMM1やattention等は変更しない。
- complete-model評価はprefillのみで、decodeやonline-serving throughputは未評価。
- 短いinputではMegatron core-TEが速い点があり、全backendに対して全shapeで最速ではない。
- DeepSeek-V2-Liteの最長complete-model条件は40GB A100でOOM。
## 実装状態
公開COMET A100 implementation in FLUXへ統合済みと論文が明記。論文評価はCOMET A100 V2 commit 19831ca、CUTLASS df8a550で実施。
## 研究上の位置づけ
分散MoEの細粒度計算・通信重畳に対するlaunch-time resource allocation研究。実行機構そのものより、GPU resident CTAという有限・非preemptive資源とdependency pipelineを解析的に結ぶ点が中心。
## 監査メモ
arXiv v1全文をIntroductionからConclusionまで再確認。system design、hardware/software、3 model、3 TP/EP、router trace、oracle regret、3測定境界、negative result、correctness、portability/decode limitationを確認し、追加auditを必須とする明確な未確認事項はない。
## 一次資料
- https://arxiv.org/abs/2609.07536
- https://arxiv.org/html/2609.07536
