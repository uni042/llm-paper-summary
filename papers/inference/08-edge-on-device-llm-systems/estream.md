---
canonical_id: "arXiv:2609.06551"
arxiv_id: "2609.06551"
title: "EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs"
summary: "モバイルNPUの静的グラフ制約とMoEの要求単位での専門家集合の高密度化を、共有専門家グラフ、実行時ルート・重みアドレス束縛、UFS上の専門家仮想化、UFS–NPUパイプラインで解消し、スマートフォン上の全NPU MoEプリフィルを実現する。"
source: "https://arxiv.org/abs/2609.06551"
last_audited: null
audit_version: 0
---

# EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs
## 書誌情報
- **著者**: Junming Zhang, Zhenzhe Zheng, Fan Wu, Xiaoyao Huang, Jie Wu
- **公開**: arXiv:2609.06551v1, 2026-09-06
- **種別**: arXiv preprint
- **対象**: on-device LLM、MoE prefill、mobile NPU、expert virtualization、UFS streaming、edge inference
- **実装**: C++20ホストランタイムとllama.cppのHexagon対応を拡張した低水準HTPバックエンド。約23K物理行のC/C++を追加。独立した公式公開コードURLは本文・arXivページでは確認できない。
## 問題設定
MoEは各tokenで少数の専門家だけを選ぶが、複数tokenのprefillでは要求全体として専門家集合の大半を触るため、専門家重みがモバイルDRAMへほぼ全量常駐しやすい。一方、モバイルNPUの一般的なグラフ実行系はトポロジ、tensor容量、parameter bindingを事前確定するため、実行時に変わる専門家・route数・parameter位置を効率よく扱えない。CPU/GPUへroutingやexpert実行を逃がすとNPUの高い行列演算性能を活かせず、既存offloadもdecode localityやCPU/GPU計算中心である。
## 新規性
専門家間で演算トポロジが不変であることと、論理的に活性化された専門家が同時に物理常駐する必要はないことを利用する。1つの共有専門家NPUグラフに実行時route extentとparameter addressを束縛し、専門家全体をUFS上に置いたまま固定サイズのNPU可視arenaへgroup単位で流す。さらにUFS読出しとNPU計算を有限buffer producer-consumer pipelineとしてモデル化し、group size・I/O queue depth・bank countを自動選択する。
## 手法
offlineでは専門家重みをNPUが直接消費するtile-major layoutへ変換し、専門家をgroup化してUFSへ配置する。onlineではnon-expert処理中からgroup読出しを開始し、route確定後に不要groupを捨て、必要groupだけを固定bankへ読み込む。bankがReadyになった後だけ共有専門家グラフへparameter bindingを公開し、NPU完了後にbankを再利用する。routeのgather、gate/up、SwiGLU、down、scatter-addは1つのroute-aware fused operatorへ統合する。

### Topology-invariant expert graph sharing
同じshape classの専門家で1つのNPUグラフを共有し、route descriptor、valid extent、placement map、parameter addressだけを呼出し時に変更する。専門家ごとのgraph再構築やtensor再確保を避ける。

### Composed sparse route and parameter binding
routing結果とexpert-to-slot placement mapをNPU内で結合し、物理slotごとのCSR風route表を構築する。empty slotを飛ばし、token row・router weight・parameter addressを直接fused operatorへ渡す。

### Fused intra-NPU expert pipeline
DMA、HVX、HMXをVTCM上で重畳し、gatherからweighted scatter-addまでを1演算に融合する。中間tensorのDRAM materializationとdispatch境界を減らす。

### Bounded expert arena
B個のbank×G専門家だけをNPU可視memoryへ保持し、Available→Filling→Ready→InUse→Availableのstateで安全に再利用する。論理的な専門家数に依存せず物理常駐量をBGWeへ制限する。

### UFS–NPU pipeline auto-configuration
group size G、queue depth Q、bank count Bをmax-plus recurrenceで評価し、memory budget内で予測latencyを最小化する。UFS bandwidth profileでQを先に決め、各GについてBを探索する。

Qualcomm Hexagon HTPのscalar/HVX/HMX/DMA資源を直接協調させ、UDMABUF-backed DMA-BUFへO_DIRECT preadvでoffline-packed weightを直接読込む。non-FFN実行中にroute確定前prefetchを始め、実行中groupと次groupのUFS loadを重ねる。初期prefetch順序はoffline group順で、route確定後はinactive groupをskipする。
## 評価条件
- **Hardware**: OnePlus PLK110 smartphone、Snapdragon 8 Elite Gen 5 (SM8850)、Hexagon v81 HTP、Adreno GPU、2 prime + 6 performance Oryon CPU cores、15.1 GiB memory、UFS 4.1 storage
- **Software**: Android 16、C++20 EStream runtime、llama.cpp Hexagon support extension、Qualcomm FastRPC / DSPQueue / cDSP、O_DIRECT preadv + UDMABUF-backed DMA-BUF、Qualcomm QPT for SoC energy
- **Model**: OLMoE-1B-7B、LFM2.5-8B-A1B、DeepSeek-V2-Lite、Qwen3-30B-A3B、Mixtral-8x7B
- **Dataset / Trace**: C4 prefixes、MASSIVE、WinoGrande、ToxicChat、HellaSwag、ARC-Challenge、NFCorpus、SciFact、LAMBADA、BoolQ
- **Baseline**: llama.cpp-CPU、MNN-CPU、MNN-OpenCL、ONNX Runtime GenAI CPU、EdgeMoE reproduction、PowerInfer parameter-streaming backend port、same-backend fully resident NPU reference、QNN-switch per-expert contexts、naive streaming、coarse layer streaming
- **Correctness**: model weightとrouting decisionは保持するが、fused NPU pathとstreamingにより有限精度演算順序は変わる。200例/benchmarkのHost reference比較ではOLMoE/LFM2.5のC4 PPL差は0.1%未満、DeepSeekもPPLは安定しARC-Cのみ3.0 point差、Qwen3は相対PPL 5.51%悪化・task score差最大3.0 pointだった。
- **Precision**: expertとlarge non-expert matrixはGGUF Q4_0、activationはFP32、HMX operandとKV cacheはFP16。OLMoE output headはQ6_K、DeepSeek MLAの一部はFP16。activation quantizationやapproximation-based sparsityは不使用。
- **Primary input lengths**: C4 prefix 256–4096 tokens。主要比較は3モデル×6長さ=18設定。TTFTはOS page cacheをdropしたfresh process 3回のmedian。
- **Application tests**: 7 dataset、各32 length-stratified examplesを共通sourceとしてmodelごとにtokenize。1 warm-up後のmean request latencyとpeak physical memoryを測定。
- **Energy**: 128–2048 tokenのsteady-state prefillでQPTがgross SoC energyを積算。
- **Auto-tuning**: 1K C4 calibrationでGごとのservice profileを採取。platformでは95% peak grouped-read bandwidthを満たす最小Q=2を固定し、memory budgetごとにG/Bを選ぶ。
latency、peak physical memory、energy、qualityを別々に評価し、baselinesは対応するmodel/runtime pairを調整して比較する。大規模modelでは起動・初期化を含むより厳しいenergy boundaryも示す。auto-configuratorは184個のproduction-supported Q/B/G sweepと比較する。
prefill-only workloadを対象にし、autoregressive decodeは最適化対象外。commercial Qualcomm smartphone上のsingle-device full-NPU MoE prefillを主対象とする。
## 主要結果
EStreamは短いpromptではNPU dispatch/pipeline fillを償却できずCPU runtimeが速い場合があるが、promptが長くなるほどUFS loadをNPU計算で隠せるため優位が拡大する。主要18設定では非offload baselineより大幅に高速かつ省memoryで、PowerInferにも全設定で勝ち、最大46.7B MoEを商用スマートフォン上でfull-NPU prefillできた。

- Pure-prefill TTFT speedup / 2.25–27.57× (baseline: fastest completed non-offloading baseline at each point; condition: OLMoE/LFM2.5/DeepSeek-V2-Lite, 256–4096 tokens, 18 settings) — input長の増加に伴いNPU計算でexpert I/Oを隠せるため優位が大きくなる。

- Peak physical memory reduction / 6.45–12.29× (baseline: fastest completed non-offloading baseline; condition: same 18 settings) — expert residencyを固定arenaへ制限する効果。

- Against PowerInfer / 2.96–50.78× faster; 1.16–1.69× less memory (baseline: PowerInfer; condition: same 18 settings) — CPU/GPU-oriented parameter streamingよりfull-NPU streamingが優位。

- 4K TTFT / 2.12 / 2.14 / 9.53 s (baseline: 58.45 / 51.15 / 120.02 s fastest non-offloading competitors; condition: OLMoE / LFM2.5 / DeepSeek-V2-Lite at 4096 tokens) — long prefillで大きな速度差。

- Large-model scaling / Qwen3 211.7–599.1 tok/s at 1.46–1.87 GiB; Mixtral 144.5–301.5 tok/s at 2.77–4.11 GiB (baseline: EStream standalone; condition: Qwen3-30B-A3B and Mixtral-8x7B, 1K–4K) — 30.5B/46.7B total parametersをスマートフォンmemory内で処理。

- Energy efficiency / 1.19–8.41×; geometric mean 4.08× (baseline: strongest completed baseline; condition: 21 model-length settings, 128–2048 tokens) — 全完了設定で最高のtokens/J。

- Application workload crossover / within 8% at ToxicChat; 1.03–1.21× faster at HellaSwag; 3.79–5.75× faster on ARC-C/NFCorpus/SciFact (baseline: latency-leading baseline; condition: mean prompt lengths 66, 80, 368–405 tokens) — 非常に短いrequestではCPUが有利だが、およそ66–80 tokens付近でcrossover。

- Pipeline bubble rate / 34.41% → 21.36% → 9.05% (baseline: on-demand → post-routing prefetch → pre-routing prefetch; condition: 1024-token OLMoE) — non-FFN中からのprefetchでUFS待ちを大きく隠す。

- Auto-configurator quality / 9/12 exact minima; zero median regret; 3.45% worst-case regret (baseline: exhaustive Q/B/G sweep; condition: 12 model-budget pairs) — 短いhardware profileでPareto近傍を再現。

- Resident-NPU tradeoff at 4K / 3.73–5.41× less memory with 4.3–23.0% higher latency (baseline: same-backend I/O-free resident NPU; condition: 4K inputs) — bounded residencyのI/O overheadがlong promptでかなり隠れる。

### 負の結果・境界条件
- **Very short prompts**: MASSIVE 16 tokensとWinoGrande 23 tokensではoptimized CPU runtimeが速く、NPU dispatchとpipeline fillを償却できない。
- **Numerical alignment**: Qwen3はHost referenceに対しC4 PPLが相対5.51%悪化し、task score差も最大3.0 point。exact arithmetic orderは保持されない。
- **Full residency remains faster**: I/O-free NPU-residentは1.04–5.63×高速だが、3.73–6.36×多いmemoryを使う。
- **More banks are not always better**: producerがNPUを十分供給できると追加bankはlatencyを改善せずmemoryだけ増やす。

中心的な利点は、MoEのrequest-level densificationを『全expert同時常駐』へ結びつけず、動的routeとparameter addressを共有NPU graphへ結びつけたことである。storage streamingをNPU executionと共同設計した結果、memory capacityとeffective model capacityを切り離している。
## 品質への影響
approximation-based sparsityやrouting変更は行わないが、finite-precision operation order変更による数値差は存在する。3モデルでは概ね小さいがQwen3で相対PPL 5.51%差があり、完全なbitwise同等性はない。
## 既存研究との差
- FlexGenやLLM in a Flashのようなdense modelのmemory/storage offloadではなく、request単位でほぼ全expertを触るMoE prefillをモバイルNPU上で扱う。
- MoE-Infinity、PowerInfer、KTransformers等のCPU/GPU中心のexpert offload/prefetchとは異なり、routingからexpert演算までfull-NPU pathを維持し、UFSからNPU可視arenaへ直接重みを流す。
- NPUMoEはApple NPU上のprefillに近いが、expert graph容量がprecompiledでrouting/aggregationはCPU、全weight常駐を前提とする。EStreamはruntime route extentとstreamed parameter addressを共有graphへ束縛し、resident memoryを固定する。
- PowerInfer-2はUFS readとNPU-centric prefillのoverlapに近いが、precompiled graph variantsを使い、本文によれば公開mobile implementationがない。EStreamはdynamic parameter bindingとbounded residencyを統合する。
## 限界
- autoregressive MoE decodeは対象外。1 token/stepではHMXを飽和させたりstorage loadを隠したりしにくく、decode-specific expert cache/prediction/batchingが必要。
- 実装と主要評価はQualcomm Hexagon v81 / Snapdragon 8 Elite Gen 5に依存し、他NPUへのportabilityはprogrammable vector/matrix/DMA interfaceを仮定する。
- 異なるexpert dimensionsやexpert-specific operatorを持つmodelでは複数shared graph templateが必要。
- 現在のweight-only Q4_0より強い量子化はUFS trafficを減らせる一方、HVX dequantization costが増えpipeline balanceを崩し得る。
- 短いpromptではCPU runtimeが依然速い。prefill-onlyの全request長で一律優位ではない。
- Qwen3ではHost referenceとの数値差が他modelより大きく、C4 PPL相対5.51%悪化を報告する。
- 独立した公開コードrepositoryは本文/arXivページから確認できず、再現可能な完全artifact公開状況は不明。
## 実装状態
約23K物理行のC/C++を追加したC++20 host runtimeとllama.cpp Hexagon拡張を実装。FastRPC、DSPQueue、HVX/HMX/DMA、UDMABUF-backed DMA-BUF、O_DIRECT preadvを使用する。論文は実装詳細を開示するが、公式公開repository URLは確認できない。
## 研究上の位置づけ
edge/on-device LLM systemの中でも、storage-backed expert virtualizationとprogrammable NPU executionを直接組み合わせる系統。『MoE sparse activationでもprefill request全体ではexpert working setがほぼdenseになる』点を出発点に、capacity不足をcache hit率の問題としてではなく、固定arena上のvirtualized residencyとUFS–NPU overlap問題として扱う。SSD/NVMe offload研究に対しても、flash tierを単なる低速backing storeではなくNPU execution scheduleと共同最適化する設計例として有用。
## 監査メモ
arXiv v1本文をIntroductionからDiscussion/Conclusionまで確認し、system design、implementation、18 primary settings、application workload、energy、quality、auto-tuning、ablation、negative results、portability/decode limitationsを照合した。追加auditを必須とする明確な未確認事項はない。
## 一次資料
- https://arxiv.org/abs/2609.06551
- https://arxiv.org/html/2609.06551
