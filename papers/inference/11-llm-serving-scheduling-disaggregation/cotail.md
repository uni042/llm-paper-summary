---
canonical_id: "arXiv:2609.05425"
arxiv_id: "2609.05425"
doi: "10.48550/arXiv.2609.05425"
title: "Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server"
summary: "GPUサーバの余剰host CPUへCPU workloadをco-locationした際のLLM serving劣化を、GPU kernel遅延ではなくGPU投入前のCPU-side serving stageのtail amplificationとして診断する。Core Path Tail Index（CPTI）とCore Tail Suppression（CTS）を導入し、workload risk、NVTX stage tail、OS-level protection、decode SLOを組み合わせるCoTail手順により、held-out条件でも固定ルールで保護方式を選択する。"
source: "https://arxiv.org/abs/2609.05425"
last_audited: null
audit_version: 0
---

# Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server
## 書誌情報
- **著者**: Guanjie Cheng, Guowei Li, Yingying Wen, Xinkui Zhao, Zhe Liu, Shuiguang Deng
- **公開**: arXiv:2609.05425v1, 2026-05-26
- **種別**: arXiv preprint / cs.DC
- **対象**: LLM serving、CPU co-location interference、tail latency diagnosis、OS resource control、NUMA、real-time scheduling
- **実装**: 実験手順・launch/profiling command・workload定義・OS protection設定は本文/付録に詳述される。arXiv本文およびGitHub検索で著者公式コードrepositoryは確認できず、公開実装URLは未確認。
## 問題設定
GPUサーバではLLM推論中もhost CPU資源が余るためCPU workloadのco-locationは利用率向上に有効だが、外部CPU workloadがLLM serving pathのどこを阻害し、どのOS-level protectionを選ぶべきかは十分整理されていない。著者らは、単純なGPU kernel時間やCUDA launch指標だけではend-to-endのthroughput/TTFT/TPOT悪化を説明できず、GPU work submissionより前のCPU-side service-stage tailが主要な診断信号になることを示す。
## 新規性
CPU co-location干渉をmacro metricだけで分類せず、NVTXで観測したcore serving stageのP95/P99 tail amplificationをCPTIとして集約し、保護後の抑制率をCTSとして定量化する。さらにworkload-only hardware screening、service-stage診断、OS protection選択、common-baseline decode SLO validationを1つの運用手順CoTailへ統合し、primary setupで凍結したルールをheld-out model/framework/workloadへ適用する。
## 手法
CoTailは、まずCPU workload単体のhardware profileからLOW/MEDIUM/HIGH riskをscreeningする。非自明なcaseではunprotected co-locationをNVTX付きでprofileし、scheduler.step、batch.construct、model.execute、model.forwardのtailからCPTIとdominant stageを求める。service-tail支配ならEngineCoreだけをreal-time化するrt、cache/topology感度かつTTFT支配ならNUMA isolation、両方のsignalが強いmixed caseならrt+numaを候補とし、最後にcommon-baseline decode SLOと必要に応じCTS>0を確認して採否を決める。

### Core Path Tail Index (CPTI)
4つのcore serving stageについて、同一protectionのno-interference baselineに対する正のP95/P99 normalized tail amplificationを平均する。各stageはuniform weight 1/4。値が大きいほどCPU-side serving pathのtail amplificationが強い。

### Core Tail Suppression (CTS)
CTS=1-CPTI(w,p)/(CPTI(w,none)+1e-6)として、protection pがunprotected時のtail amplificationをどれだけ抑えたかを測る。負値はprotectionがtailを悪化させたことを示す。

### EngineCore-targeted rt
framework-specific EngineCore Linux TIDだけをSCHED_FIFO priority 50へ昇格し、他のserving threadとco-tenantは通常のCFSに残す。vLLMではVLLM::EngineCore、SGLangではsglang::EngineCoreをruntimeで同定する。

### NUMA isolation
LLM serverを選択GPUにlocalなNUMA nodeへ固定し、interfering workloadを反対socketへ隔離する。scheduler latencyではなくlocality/cache/memory/topology由来の干渉を狙う。

### Frozen decision procedure
primary vLLM/DeepSeek条件だけでthreshold・risk label・policy ruleをcalibrateし、その後held-out model/frameworkと未使用CPU workloadへ固定ルールを適用してpost-hoc fittingを避ける。

CoTailはuniversal cluster schedulerではなくsame-platformのmeasurement-driven operator procedureとして設計される。候補protectionはnone/nice/cgroup/rt/numaを基本とし、mixed-riskのみrt+numaを追加検証する。候補がcommon-baseline SLOを満たさなければco-locationをrejectし、tail-diagnosed caseではpositive CTSも要求する。
## 評価条件
- **Hardware**: dual-socket AMD EPYC 7T83、128 physical cores / 256 logical threads、8× NVIDIA RTX 4090 server; each serving experiment uses a single GPU
- **Software**: Linux CFS / nice / cgroup v2 / SCHED_FIFO / NUMA affinity、NVIDIA Nsight Systems + NVTX、vLLM、SGLang
- **Model**: Primary: DeepSeek-R1-Distill-Qwen-7B on vLLM、Held-out: Llama-3.1-8B on vLLM、Held-out: Mistral-7B on vLLM、Held-out: DeepSeek-R1-Distill-Qwen-7B on SGLang
- **Dataset / Trace**: stress-ng and seven application-level CPU co-tenants spanning compute/cache/I/O/network/mixed behavior、Held-out CPU workloads: image-preprocess, sqlite-txn, text-search, zstd-compress
- **Baseline**: none、nice、cgroup CPU weighting、EngineCore-targeted rt、NUMA isolation、targeted mixed-risk validation: rt+numa、selector baselines: Always-rt, Hardware-only, Macro-only
- **Correctness**: 本研究の対象はmodel output品質ではなくserving性能とco-location SLOである。protectionはmodel計算を近似・変更せずOS scheduling/localityを制御する。tail diagnosisの妥当性はservice-stage tailとmacro degradationの相関、CTSと回復の整合、schedstat/delay-injection等の補助検証で確認するが、著者らは全干渉経路のformal causal proofとは主張しない。
- **Serving mode**: single-GPU LLM serving on a multi-GPU server; tensor/pipeline parallel multi-GPU inferenceは対象外
- **Client**: closed-loop batched client、batch size 32、最大512 generated tokens/request
- **Measurement**: 10 measurement rounds、8 s warmup。throughput、TTFT、TPOTとNVTX stage latency distributionを収集
- **rt**: framework-specific EngineCore TIDのみSCHED_FIFO priority 50。他thread/co-tenantはCFS
- **nice**: LLM serving processを概ねnice=-15、interfering workloadはdefault
- **cgroup**: LLM cpu.weight=5000、interfering workload cpu.weight=50
- **numa**: GPU1ではLLMをCPUs 0–63,128–191、workloadを64–127,192–255へ分離
- **Held-out validation**: threshold/risk label/policy-selection rulesをprimary vLLM/DeepSeek条件で固定してから別model/frameworkおよび4 unseen CPU workloadsで評価
CPTIはscheduler.step、batch.construct、model.execute、model.forwardのP95/P99正規化tail amplificationをuniform weightで集約する。primary experimentでmechanismとdecision ruleを作り、held-outでは保護結果を見る前にCoTail recommendationを決める。小標本のbootstrap confidence intervalは10,000 resamplesで計算するが、formal inferenceではなくdescriptive robustness summaryとして扱う。
同一dual-socket GPU server上の外部host-CPU co-location interferenceを対象とする。GPU memory oversubscriptionを前提とせず、主にGPU work submission前のCPU-side serving path、OS scheduler、NUMA/localityの干渉を扱う。
## 主要結果
最も強い干渉ではCPU co-locationがserving性能を数倍悪化させる一方、GPU kernelそのものの遅延よりCPU-side serving stageのtail amplificationが強い診断信号だった。EngineCore-targeted rtはscheduler/batch/execution tail型で大きくCPTIを抑え、NUMA isolationはcache/memory/topology-sensitiveなTTFT型で有効だった。CoTailは両者をworkloadとstage diagnosisに応じて選択し、held-out条件でも固定ルールでSLO達成率とdeployment costを改善した。

- Unprotected nginx throughput degradation / -78.8% (baseline: no-interference LLM-alone; condition: primary vLLM / DeepSeek-R1-Distill-Qwen-7B setup) — host CPU co-locationだけでserving throughputが大幅に低下する代表例。

- Unprotected nginx TTFT increase / +429.5% (baseline: no-interference LLM-alone; condition: primary setup) — request admission/batching等を含むlatencyへの影響が大きい。

- Unprotected nginx TPOT increase / +362.4% (baseline: no-interference LLM-alone; condition: primary setup) — decode pathもCPU-side interferenceで深刻に悪化する。

- nginx throughput recovery / up to 4.4× (baseline: unprotected nginx co-location; condition: CoTail-guided protection) — 適切なOS protectionで大部分のthroughput lossを回復できる。

- nginx TPOT recovery / up to 4.5× reduction (baseline: unprotected nginx co-location; condition: CoTail-guided protection) — tail型干渉へのtargeted protectionがdecode latencyを大きく改善する。

- Common-baseline held-out SLO success / 12/12 oracle-feasible cases (baseline: Always-rt 10/12; Macro-only 11/12; condition: held-out model/framework/workload set; frozen CoTail rules) — primary conditionで決めたruleを凍結しても、評価可能caseすべてでdeployment SLOを満たした。

- RT exposure / 22/28 cases (baseline: Always-rt 28/28; condition: cost-aware selector evaluation) — 常時real-time schedulingよりRT利用を減らしながらSLOを維持する。

- Mean co-tenant slowdown / 51.21% (baseline: Always-rt 56.65%; condition: cost-aware selector evaluation) — LLM保護だけでなくco-tenant utilityの損失も抑える。

- EngineCore RT-covered CPU time / 310.22 s (baseline: Always-rt 403.46 s; condition: evaluated deployment cases) — real-time schedulingを必要なcaseへ限定できる。

- Held-out image-preprocess CPTI suppression / CPTI 15.62 → 0.24; CTS 98.5% (baseline: unprotected → rt; condition: held-out workload) — batch.construct-dominant tailをEngineCore-targeted rtがほぼ除去した。

- Held-out zstd-compress protection / CPTI 5.56 → 1.07; CTS 80.7% (baseline: unprotected → rt+numa; condition: mixed-risk held-out workload) — scheduler/service-tailとtopology signalを併せ持つcaseではcombined policyが選択された。

### 負の結果・境界条件
- **nice / cgroup**: 多くのworkloadでunprotectedに近いまま、soft priorityやproportional CPU weightだけではcore-path tailを十分抑えられなかった。held-outではcgroupによりCPTIが悪化するcaseもある。
- **rt is not universal**: rtはTPOT/throughput recoveryに強いがTTFTで常に最良ではない。ffmpegではNUMA isolationがTTFT increaseを103.6%から9.4%へ抑え、rtの58.4%より良かった。
- **CTS does not capture every NUMA benefit**: NUMAはlocality/topology経路でmacro metricを改善できるため、CTSが小さい・負でもTTFT等が改善するcaseがある。CoTailはCTS単独ではなくworkload hardware signalとmacro SLO validationを併用する。
- **Causality scope**: service-stage tailとmacro degradationの相関・介入整合性は強いが、著者らはすべてのinterference channelを形式的に因果証明したとは主張しない。

本研究の中心は新しいLLM kernelではなく、host-side interferenceをservice-stage tailへ分解し、既存OS mechanismを症状に応じて選択するdiagnosis/control loopにある。特に『常にrt』ではclean protection overheadとco-tenant costが発生するため、CPTI/CTSとworkload signalを用いて必要なcaseだけ強い保護へ上げる点が実運用上重要。
## 品質への影響
model weight、attention、sampling、KV cache内容などmodel計算自体は変更しないため、推論品質の近似trade-offを導入する方式ではない。評価対象はserving throughput/TTFT/TPOTとco-tenant utilityであり、生成品質benchmarkは主題ではない。
## 既存研究との差
- vLLM/SGLang等のserving engine内部最適化やbatch/KV管理を直接改造するのではなく、外部CPU co-tenantが既存serving pathへ与える干渉をOS側から診断・緩和する。
- CUDA kernel execution timeやlaunch/queue metricだけで原因推定せず、NVTXでinstrumentしたscheduler.step、batch.construct、model.execute、model.forwardのP95/P99 tailを主要信号にする。
- 単一のisolation policyを常用するのではなく、service-tail型はEngineCore-targeted rt、cache/topology-sensitive TTFT型はNUMA、mixed型はrt+numaへ分岐し、最後にcommon-baseline SLOで採否を検証する。
- CPTI/CTSはresource utilizationそのものではなく、no-interference baselineからのservice-stage tail amplificationと、そのprotectionによる抑制を明示的に測る。
## 限界
- primary hardwareはdual-socket AMD EPYC 7T83 + RTX 4090の1 server platformで、著者自身もhardware-counter/CPTI thresholdは異なるCPU topology、GPU interconnect、kernel、serving engine、background workload mixでrecalibrationが必要としている。
- multi-GPU server上でのsingle-GPU servingを評価対象とし、tensor parallelismやpipeline parallelismを使うdistributed inferenceのhost-side interferenceは直接評価していない。
- CoTailはsame-platform diagnostic procedureであり、global cluster scheduler、tenant fairness policy、admission-control systemとしての完全な設計ではない。
- EngineCore-targeted SCHED_FIFOは強いOS mechanismであり、production利用ではruntime limit、priority ceiling、watchdog rollback、admission controlとの併用が必要と著者らが明記する。
- bootstrap confidence intervalは反復数が小さいためdescriptive robustness summaryであり、formal statistical inferenceの保証ではない。
- CPTI/CTSはCPU-side service-tail経路を要約するためNUMA/locality由来の改善を完全には表現せず、macro SLO validationとの併用が必要。
- 評価したcandidate protection集合内でoracleを定義しているため、未評価のOS/runtime protectionがより良い可能性は残る。
## 実装状態
論文はserving launch command、Nsight/NVTX profiling、CPU workload構成、nice/cgroup/rt/NUMA設定、CoTail decision algorithmを付録まで具体的に記載する。rtはruntimeでframework-specific EngineCore TIDを同定してSCHED_FIFO priority 50へ昇格する。公開GitHub code repositoryはarXiv本文・landing page・GitHub検索から確認できず、第三者が取得可能な公式実装は未確認。
## 研究上の位置づけ
LLM serving scheduling/disaggregation系統のうち、GPU内のbatch schedulingやKV placementではなく、GPU serverのhost CPUを他workloadへ開放した際のcross-workload interference controlを扱う。『GPUが速いままでも、GPUへ仕事を渡す前のCPU serving pathがtail化してsystem throughputを壊す』ことを定量化し、OS scheduler/NUMA protectionをserving-specific observabilityで選択する点が特徴。GPU資源だけでなくhost-side resource managementをLLM serving SLOの一部として扱う研究として位置づけられる。
## 監査メモ
一次資料v1本文・付録まで確認。著者/所属、primary/held-out hardware・model/framework、protection設定、CPTI/CTS定義、主要macro result、held-out selector result、negative result、scope/caveatを照合した。公開コードURLのみ確認できなかったため、その点を未確認として明記し、現時点では追加auditを必須とはしない。
## 一次資料
- https://arxiv.org/abs/2609.05425
- https://arxiv.org/html/2609.05425v1
