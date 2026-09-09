---
canonical_id: "arXiv:2608.03741"
arxiv_id: "2608.03741"
title: "When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference"
summary: "エージェント型LLM推論でprefill/decodeだけでなくattention/FFNまで分離する4段PDAFを、段ごとの異種NPU、並列度、相互接続、量子化と合わせて探索するイベント駆動シミュレータHeteroPanaceaを提案する。分離の利得はworkloadとhardware design spaceに強く依存し、prefill-heavy領域ではcustom NPU上のPDAFが有利になる一方、商用GPUではPDが多くの条件でPDAFと同等以上になる。"
source: "https://arxiv.org/abs/2608.03741"
last_audited: null
audit_version: 0
---

# When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference
## 書誌情報
- **著者**: Przemyslaw Forys, Haoran Wu, Can Xiao, Jiayi Nie, Tony Liu, Rika Antonova, Timothy Jones, Robert Mullins, Wayne Luk, Aaron Zhao, George A. Constantinides
- **公開**: arXiv:2608.03741v1, 2026-08-04
- **種別**: arXiv preprint
- **対象**: LLM serving、prefill-decode disaggregation、attention-FFN disaggregation、agentic inference、heterogeneous NPU、hardware-software co-design、mixed precision、parallelism search
- **実装**: 論文はHeteroPanacea simulator、configuration、evaluation scriptsをacceptance後に公開予定と記載している。arXiv v1本文では公開済みartifactを確認できない。
## 問題設定
エージェント型LLMは長い反復コンテキストを持ち、prefillとdecodeだけでなくattentionとFFNでも演算量・メモリ容量・帯域要求が大きく異なる。従来のPD分離はdecode-attentionとdecode-FFN等を同じpoolに残すため、各段に最適なhardwareを独立選択できず、分離通信のoverheadが利得を上回る条件も明確でない。
## 新規性
ND、PD、AF、4段PDAFを同一のsystem-level simulatorで比較し、各stageのNPU/GPU構成、TP/PP/DP/EP、memory/interconnect、precisionを横断的に扱う。単に分離方式を提案するのではなく、workload geometryとhardware specializationの双方から『いつ分離が得か』を探索する点が中心。
## 手法
各stageをroofline型のcompute/memoryモデルで評価し、D2D/N2N通信、batching、KV容量、decode反復をevent-driven simulationで結合する。hardware searchは解析的なstage demand scoreで候補を絞り、power/cost budget内でstageごとの候補を割り当てた後、上位構成だけを詳細simulationしてtokens/s最大の設計を選ぶ。量子化はPA/PF/DA/DFごとに独立precisionを設定し、task accuracyも測定する。

### ND/PD/AF/PDAF topology
prefill/decode分離に加えattention/FFNを分離し、PDAFではprefill-attention、prefill-FFN、decode-attention、decode-FFNを独立pool化する。

### Stage roofline and power model
stage実行時間をFLOPs/実効computeとbytes/実効bandwidthの最大値で近似し、MHA/GQA/MLA、dense/MoE、memory technology、device powerをparameterizeする。

### Parallelism and interconnect model
TP/PP/DP/EPをpool単位で設定し、intra-node D2Dとinter-node N2Nを分離してall-reduce、all-to-all、activation、KV transferを表現する。

### Event-driven serving simulator
request arrival、prefill batching、decode FIFO admission、stage completion、transfer、KV容量制約をeventとして進め、memory-aware continuous batchingを模擬する。

### Hardware and parallelism search
stage demandに対する解析scoreとbudget allocationで探索空間を縮小し、top-Kだけをsimulationして最終throughputを比較する。

### Stage-wise mixed precision
MXint系precisionをPA/PF/DA/DFごとに切り替え、MASEのPhaseAutoSwitchでprefill/decodeに応じた設定を適用し、accuracy sensitivityを実測する。

各requestは選択したdisaggregation topologyに従いstage poolを移動する。pool内ではstage専用hardwareとparallelismで実行し、pool間ではactivation/KVをN2N転送する。simulationはstageのservice capabilityとbatch/KV制約を統合し、search layerが同じworkloadに対してND/PD/AF/PDAFの最適構成を比較する。
## 評価条件
- **Hardware**: parameterized custom NPU design space: 25-20000 TFLOPS with SRAM/HBM/DDR/LPDDR/GDDR capacity-bandwidth choices、commercial AWS EC2 GPU design space including H100, A100, L40S, L4, A10G, T4, V100, M60、8x NVIDIA B200 component-level validation platform、NVSwitch-class intra-domain interconnect up to 3600 GB/s bidirectional and 50 GB/s InfiniBand-class cross-domain link in NPU experiments
- **Software**: HeteroPanacea event-driven simulator、PLENA-derived parameterized NPU model、roofline-based stage performance and power models、MASE-based MXint stage-wise quantization with PhaseAutoSwitch
- **Model**: DeepSeek-V4 Pro、DeepSeek-V4 Flash、Llama-3.1-405B、Llama 4 Maverick、Llama 4 Scout、GLM-4.6、GPT-OSS、Qwen3-235B-A22B、Qwen 32B-class model for quantization sensitivity
- **Dataset / Trace**: synthetic serving workloads parameterized by input/output token ratio、BFCL for stage-wise quantization accuracy、GSM8K for stage-wise quantization accuracy
- **Baseline**: ND: non-disaggregated serving、PD: prefill/decode disaggregation、AF: attention/FFN disaggregation、PDAF: prefill/decode plus attention/FFN four-stage disaggregation、real B200 kernel/communication measurements for component validation
- **Correctness**: Simulator components are compared with measurements on B200 hardware. Reported simulated/real ratios for tensor-parallel execution are 0.79x, 1.00x, 1.06x and 1.02x for 1/2/4/8 GPUs; pipeline-parallel ratios are 0.67x, 0.77x, 0.84x and 0.90x. Communication checks report P2P ratios 0.82x-1.00x and expert all-to-all 0.86x-1.21x across tested message sizes. Quantization quality is checked empirically on BFCL and GSM8K.
- **request workload**: 500 requests per configuration at fixed 125 requests/s; output length fixed at 1000 tokens and input length varied through I/O ratios, with request lengths sampled around target values.
- **workload sweep**: I/O ratios span strongly decode-heavy to strongly prefill-heavy regimes, including 0.01, 1, 10, 100, 500 and 1000 cases discussed in results.
- **parallelism**: TP, PP, DP and EP are independently selectable per execution pool; D2D and N2N links model different communication domains.
- **main precision**: main NPU/GPU design sweeps use full precision; stage-wise quantization is evaluated separately because joint MoE quantization search is expensive.
- **GPU budget**: commercial GPU search uses fixed USD/hour budget and provider instance/device catalog rather than arbitrary custom compute-memory ratios.
- **NPU budget**: custom NPU search uses fixed installed-power budget and stage-specific compute/memory choices.
For each topology the search first scores feasible hardware candidates analytically against stage demand, allocates the fixed budget across stages, keeps promising joint configurations, and then performs detailed event-driven simulation; throughput in tokens/s selects the winner. Model ablations vary KV/attention and expert-compute characteristics to identify which architectural dimensions control the crossover.
Primary conclusions are simulation-based hardware/software design-space results rather than end-to-end deployed serving measurements. Component models are validated on real B200 hardware, but scheduling/batching/topology results themselves are not reproduced as a full production deployment.
## 主要結果
HeteroPanaceaは『分離そのもの』よりもworkload shapeとstage専用hardwareの組合せが性能を決めることを示す。custom NPUではprefill-heavyになるとPDAFが一貫して強くなる一方、commercial GPU catalogでは4段分離の自由度をhardware構成に変換しにくく、PDがPDAFと同等以上になる条件が多い。

- custom-NPU PDAF throughput vs ND / 1.05-1.92× (baseline: ND; condition: I/O=100, 8 evaluated models) — PDAFは8/8でNDを上回り、6/8モデルで最良topology。Llama 4 Maverick 1.81×、Scout 1.77×。

- average PDAF crossover / 0.48× -> 2.10× (baseline: ND; condition: custom NPU; average changes from I/O=1 to I/O=10) — prefill比率の上昇で分離overheadからstage specialization利得へ急速に反転する。I/O=1000ではdecode underutilizationで1.27×まで低下。

- commercial-GPU PD throughput vs ND / 1.18-2.50× (baseline: ND; condition: I/O=0.01, 8 models) — PDは8/8でNDを上回るが、別workloadでは非一様。I/O=100では6/8モデルでPDがPDAF以上。

- AF-only performance / 0.20-0.65× (baseline: ND; condition: custom NPU, I/O=100) — attention/FFNだけの分離は通信overheadを回収できず常に不利。GPU sweepでもAFのbestは0.96×でNDを超えない。

- tensor-parallel component validation / 0.79× / 1.00× / 1.06× / 1.02× (baseline: real B200 measurement; condition: simulated/real latency ratio at 1/2/4/8 GPUs) — roofline/communication component modelはTPで概ね実測近傍。

- pipeline-parallel component validation / 0.67× / 0.77× / 0.84× / 0.90× (baseline: real B200 measurement; condition: simulated/real latency ratio at 1/2/4/8 GPUs) — PPではsimulationが実測latencyをより強く過小評価し、end-to-end結果の不確実性要因となる。

- stage-specific 4-bit accuracy sensitivity / BFCL 20/11/12/20%, GSM8K 47/79/80/15% (baseline: 8-bit BFCL 21%, GSM8K 75%; condition: only PF/DA/PA/DF respectively changed to 4-bit on Qwen 32B-class experiment) — どのstageを低精度化できるかはmodelだけでなくworkload/taskに依存する。

### 負の結果・境界条件
- **low/balanced-ratio custom NPU**: I/O=0.01および1ではNDが全モデルで最良。分離通信とpool fragmentationがspecialization利得を上回る。
- **commercial GPU limits four-stage specialization**: PDAFのstage assignmentはほぼH100に収束し、compute/memory比をstageごとに独立設計できないためcustom NPUほど4段分離が効かない。
- **active-expert growth**: active expertsを増やしてFFN compute/weight trafficを増大させるとPDAF利得が崩れ、例としてDeepSeek-V4-Flashは1.41×から4x active expertsで0.43×、8xで0.38×まで低下する。

PDAFの価値はstage間のresource mismatchが大きく、かつそれを異種hardwareへ実際に写像できる場合に生まれる。decode-attentionは大容量・高帯域memoryと比較的低compute、prefill stagesとdecode-FFNは高computeを要求するため、custom hardwareでは分離がresource right-sizingにつながる。commercial GPUでは同じ自由度が得にくい。
## 品質への影響
main throughput sweepはfull precisionでquality trade-offを避けている。別のstage-wise quantization実験では4-bit化するstageとtaskによってaccuracy低下が極端に異なり、performance-onlyなprecision選択は安全でないことを示す。
## 既存研究との差
- Splitwise、DistServe、PD-Serve等のprefill/decode分離研究に対し、HeteroPanaceaはattention/FFNまで独立pool化したAF/PDAFを含め、stageごとのhardware構成とparallelismを設計変数として比較する。
- MooncakeやMemServeがKV cache中心のdisaggregated memory/transfer architectureを主眼とするのに対し、本研究はcompute、memory bandwidth/capacity、interconnect、precisionを含むstage-level hardware-software co-designを主眼とする。
- ConServe等のagentic serving研究とは長期multi-turn/agentic workloadという動機を共有するが、主対象はconversation-level schedulingではなく、workload geometryに応じたdisaggregation topologyと異種hardwareの設計空間である。
- production serving engineではなくsimulation frameworkとして、分離方式の優劣とhardware specializationの効果を分解して調べることが主な貢献。
## 限界
- 主要throughput結論はsystem-level simulationであり、ND/PD/AF/PDAF全体を実機clusterでend-to-end再現した結果ではない。
- component validationではTPは概ね実測に近いがPPはsimulationが実測latencyを0.67-0.90×に過小評価しており、pipeline-heavy設計の絶対値には不確実性がある。
- 量子化評価は1モデル相当とBFCL/GSM8Kの2 taskに限定され、全8モデルのjoint topology/hardware/precision searchは行っていない。
- commercial GPU結果は特定cloud providerのcatalogとprice/budgetに依存し、別provider、最新GPU、将来価格でPDAFとPDの優劣が変わり得る。
- 500 requests/configurationのsimulation結果について本文から反復run、seed sweep、confidence intervalを確認できず、stochastic workloadに対する統計的頑健性は限定的。
- simulator/config/evaluation scriptsはacceptance後公開予定とされ、arXiv v1時点では再現用artifactを直接検証できない。
## 実装状態
HeteroPanaceaは論文中で実装されたevent-driven simulatorとして記述されるが、arXiv v1はfull simulator/configuration/evaluation scriptsをacceptance後に公開予定としており、公開済みrepositoryは本文から確認できない。
## 研究上の位置づけ
主系統はLLM serving/scheduling/disaggregation。既存のPD-servingを、prefill/decode×attention/FFNの4段分離とstage専用異種hardwareまで拡張し、agentic workloadでdisaggregationが得になる条件をcross-stack simulationで特定するhardware-software co-design研究。MoE、mixed precision、parallelism searchも横断テーマとして含む。
## 監査メモ
arXiv v1全文を確認し、main sweep、component validation、model ablation、stage-wise quantization、limitationsまで照合した。abstractの『up to 75%』、本文introの『up to 2.06×』、NPU average crossoverの『2.10× at I/O=10』は異なる比較/集約条件のheadline値として扱い、単一の最大値に統合しない。条件を分けて記録したため追加auditを必須とする未解決事項はない。
## 一次資料
- https://arxiv.org/abs/2608.03741
- https://arxiv.org/pdf/2608.03741
