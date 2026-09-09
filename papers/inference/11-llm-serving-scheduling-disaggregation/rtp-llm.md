---
canonical_id: "arXiv:2605.29639"
arxiv_id: "2605.29639"
title: "RTP-LLM: High-Performance Alibaba LLM Inference Engine"
summary: "Alibabaの大規模実運用LLM inference engine。model loading、prefill/decode分離、cache-aware traffic scheduling、GPU/CPU/RDMA/3FSの4階層KV cache、speculative decoding、TP/PP/DP/EP、weight/KV quantization、ViT-LLM分離を単一serving stackへ統合する。vLLM/SGLangとのcontrolled benchmarkに加えAlibaba実trafficを使い、個別最適化だけでなくproduction orchestrationを含む統合systemとして評価する。"
source: "https://arxiv.org/abs/2605.29639"
last_audited: null
audit_version: 0
---

# RTP-LLM: High-Performance Alibaba LLM Inference Engine
## 書誌情報
- **著者**: Boyu Tan, Jiarui Guo, Zongwei Lv, Haobo Sun, Tong Yang, Kan Liu, Xinfei Shi, Zetao Hu, Yaxin Yu, Chi Zhang, Jianning Zhang, Xi Yang, Wei Zhang, Bo Cai, Silu Zhou, Xiyu Wang, Na He, Yinghao Yu, Wending Bao, Guiyang Huang, Yuxing Yuan, Juncheng Yin, Nan Wang, Lin Yang, Zechao Zhang, Lu Chen, Guoding Li, Tao Lan, Lin Qu
- **公開**: arXiv:2605.29639v1, 2026-05-28
- **種別**: arXiv preprint
- **対象**: LLM inference engine、production serving、prefill-decode disaggregation、hierarchical KV cache、traffic scheduling、model loading、speculative decoding、quantization、multimodal serving、MoE parallelism
- **実装**: 公式implementationは https://github.com/alibaba/rtp-llm でApache-2.0公開。Alibaba Group内のTaobao、Tmall、Cainiao等を含むproduction serviceで利用されると論文・公式repositoryが記載する。
## 問題設定
production LLM servingではrequest長・load・model architectureが大きく変動し、prefill/decodeのresource mismatch、KV cache容量、600B級modelのloading、MoE/multimodal/speculative decodingなどを個別最適化だけで同時に扱いにくい。特に長文と高concurrencyではKV cache reuseとtraffic routingがTTFT、必要machine数、memory効率へ直結する。
## 新規性
単一の新algorithmより、model loading、PD serving、4階層KV cache、cache-aware global scheduling、speculative decoding、TP/PP/DP/EP、weight/KV quantization、ViT-LLM分離をproduction-ready inference stackへ統合し、Alibabaの実trafficで各機構を評価した点に価値がある。
## 手法
Frontendがtoken/block hashを生成し、Masterがworker load、KV cache分布、latency予測を見てbatch/routingを決める。PD-FusionとPD-Disaggregationを選択でき、KVはGPU→local CPU→RDMA remote CPU→3FSの順で探索する。model loadingはfile-order sequential I/O、single-reader+broadcast、shared pinned buffer reuse、I/O/broadcast overlapで高速化する。decode acceleration、quantization、multimodalも同じengineに統合する。

### Global Master and traffic scheduling
Prefillはlength-similar batchingとpredicted completion time、Decodeはchat/cache affinity、load、KV occupancyを用いてroutingする。worker状態は高頻度に収集する。

### Four-tier KV cache
GPU block cache、local CPU memory、RDMA remote CPU memory、distributed 3FSを階層化し、hash prefix matchingとLRU/reference countでreuseする。local/remote lookupを並列実行してworker scoreへ統合する。

### PD deployment
PD-FusionとPD-Disaggregationをサポートし、分離時はPrefill/Decodeを独立nodeへ置いて個別scaleし、KVをNCCL/InfiniBand等で転送する。

### Optimized model loading
model-structure順ではなくfile順に読み、1 processだけがfileを読みdistributed broadcast、shared pinned memory再利用、I/Oとbroadcastのpipeline overlapでFUSE/cloud storageのsequential accessを活かす。

### Modular speculative decoding
ProposeExecutor、ScoreExecutor、SpeculativeSampler、SpeculativeUpdaterをC++で分離し、naive、Prompt Lookup、Eagle、MTP等を差し替え可能にする。

### Parallelism and quantization
TP/PP/DP/EPを統合し、weight-only INT4/INT8、FP8、on-the-fly KV quantizationを提供する。

### EPD multimodal disaggregation
ViT encoderをLLM serving nodeから分離し、vision embedding生成とlanguage generationをpipeline化して異種resourceを独立配分する。

requestはFrontend→Master→Inference Nodeへ流れ、Masterがprefix cache matchとcluster stateを統合してplacementを決める。必要KVは最速tierから段階的にGPUへstageし、実行後metadata/LRUを更新する。Name Serviceはservice discovery/heartbeat、Carbonはnode failure時の自動restartを担当し、Masterがglobal schedulingを担う。
## 評価条件
- **Hardware**: evaluation servers: Linux 5.10 x86_64, 64 CPU cores, 600 GB RAM, 8 GPUs per server、PD production evaluation: 5 nodes x 8 GPUs; 4 prefill nodes and 1 decode node、NCCL IBRC over InfiniBand for prefill-to-decode KV transfer、NVLink-class high-speed intra-node interconnect assumed for tensor parallel communication
- **Software**: RTP-LLM C++ serving engine、Alibaba 3FS distributed storage、RDMA remote CPU KV cache、DeepEP for MoE All2All、IBM fastsafetensors integration plus RTP fastsafetensors、NCCL、official open-source alibaba/rtp-llm
- **Model**: Qwen 7B and Qwen 4B production traffic services、Qwen3-Coder-480B-A35B-Instruct-FP8、DeepSeek-V3-0324、Qwen3-235B-A22B with MTP、Qwen3-32B、Qwen/Qwen2.5-VL-7B-Instruct、additional 8B-32B models including Qwen3-8B, Qwen2.5-14B-Instruct and Moonlight-16B-A3B for loading
- **Dataset / Trace**: real Alibaba internal Robot Q&A traffic、real Taobao Merchant Service traffic、1,000 real merchant data-agent queries、WikiText-2 sampled subset for quantization perplexity、GQA for multimodal framework comparison
- **Baseline**: vLLM、SGLang、traffic scheduling disabled within RTP-LLM for production scheduling ablation、multiple TP/DP deployment configurations under equal GPU budget
- **Correctness**: Speculative sampling follows proposal-score-verify-update semantics intended to preserve target-model output distribution. Quantization fidelity is measured by WikiText-2 perplexity: reported configurations span PPL 7.59-8.09 versus baseline 7.59-7.67, with RTP-LLM within 0.01 PPL of baseline in the compared AWQ/FP8-KV settings described by the paper. Multimodal framework comparison uses identical decoding parameters.
- **production comparison workload**: For PD disaggregation and speculative sampling framework comparisons, paper states input 200K tokens and output 16K tokens throughout.
- **PD large-MoE deployment**: Qwen3-Coder-480B-A35B-Instruct-FP8 with FP8 KV cache; 5 nodes, each 8 GPUs; prefill 4 nodes/decode 1 node; TP=8, EP=8, DP=1 per node; prefill batch 64, decode concurrency 128.
- **speculative controlled test**: DeepSeek-V3-0324, TP=8/DP=1, max_batch_size=32, max_new_tokens=500, FP8 KV cache, speculative step size 1.
- **real MTP test**: Qwen3-235B-A22B, 1,000 production queries, average input 19.5K and output 800 tokens, concurrency 64-512; compares 4TPx4, 1TP8DP, 2TP4DP, 2TP8DP.
- **quantization test**: Qwen3-32B single GPU, max_batch_size=64, top-p=1, top-k=1, temperature=0; max_new_tokens 500/800/1000/1200; Baseline, AWQ(FP8), FP8 KV cache.
- **multimodal test**: Qwen2.5-VL-7B-Instruct on GQA, TP=2 across two GPUs, max_batch_size=64, max_new_tokens=500, top-p=1, top-k=1, temperature=0.
Evaluation intentionally mixes production A/B-style workloads and controlled framework benchmarks. Traffic scheduling is measured against the same service with scheduling disabled; PD and speculative decoding use real online models/workloads as well as framework baselines; model loading, quantization, and EPD use controlled comparisons against vLLM/SGLang.
Strongest evidence is production deployment and end-to-end engineering effectiveness, but different subsections use different models/workloads/configurations. The paper does not establish that every RTP-LLM component individually causes the full headline speedups, and does not report broad statistical confidence intervals across repeated deployments.
## 主要結果
RTP-LLMはproduction stack全体を対象とし、loading、cache-aware scheduling、PD、speculative decoding、quantization、multimodal分離でそれぞれ改善を示す。特にPD評価ではTTFT/cache hitは大幅改善する一方、raw throughputはSGLang/vLLMとほぼ同等であり、利得の中心がprefix reuseとlatency/SLO側である点が重要。

- production TTFT P95 reduction / 37.2% / 35.4% (baseline: traffic scheduling off; condition: Internal Robot Q&A: 83.3->52.3 ms; Taobao Merchant Service: 350->226 ms) — cache-aware traffic schedulingがreal serviceのTTFTを安定して改善。Taobaoではinference P95も1760->1210 ms、31.3%削減。

- prefix cache reuse length / 26.6 -> 83.8 tokens (+215%) (baseline: traffic scheduling off; condition: Internal Robot Q&A production workload) — 同条件でprefill machineを80->20へ75%削減しつつ平均TTFTを維持。Taobao workloadのreuseは833->840で改善幅は小さい。

- PD cache hit rate / 45.09% (baseline: SGLang 28.70%; vLLM 19.10%; condition: Qwen3-Coder-480B-A35B-Instruct-FP8, 5-node PD production deployment) — 1.57x/2.36x高いcache hit。

- PD TTFT / 1338.38 ms (baseline: SGLang 6322.7 ms; vLLM 7134.8 ms; condition: same Qwen3-Coder production evaluation) — 4.72x/5.33x短いTTFT。ただしthroughputは1081.72 tokens/sでSGLang 1152.95、vLLM 1084.58とほぼ同等。

- speculative decoding throughput / 187.53 tokens/s (baseline: vLLM 167.95; SGLang 75.785 tokens/s; condition: DeepSeek-V3-0324, TP=8, FP8 KV, max_new_tokens=500) — 1.12x/2.48x throughput。direct C++ launchによるoperator invocation overhead削減も寄与。

- large-model loading speedup / 4.70-6.27x (baseline: SGLang/vLLM; condition: Qwen3-235B-A22B; TP=4: RTP 37.1s vs 177.4/174.3s, TP=8: 33.0s vs 206.7/204.0s) — parallel shared readingとI/O-broadcast overlapによりTP増加でloadingが悪化せず、baselineはTP4->8で約16.5-17.0%悪化。

- quantized inference TTFT / 1.9-3.0x reduction (baseline: SGLang/vLLM; condition: Qwen3-32B across AWQ(FP8), FP8 KV Cache and baseline configurations) — 長sequenceでも低TTFTを維持。WikiText-2 PPLは7.59-8.09でbaseline 7.59-7.67に近い。

- EPD multimodal throughput / 6288.48 tokens/s (baseline: SGLang 3374.24; vLLM 2492.69 tokens/s; condition: Qwen2.5-VL-7B-Instruct on GQA, TP=2) — 1.86x/2.52x throughput。TTFT 1737.48 msはSGLang 4103.1、vLLM 3688.3より2.36x/2.12x短い。

### 負の結果・境界条件
- **PD throughput is not higher**: Qwen3-Coder PD評価のtokens/sはRTP-LLM 1081.72、SGLang 1152.95、vLLM 1084.58で、RTP-LLMの主な利得はthroughputではなくcache hitとTTFT。
- **cache-reuse gain is workload-dependent**: Internal Robot Q&Aでは26.6->83.8 tokensだが、Taobao Merchant Serviceでは833->840 tokensに留まる。
- **parallelism trade-off in production**: real 235B MoE+MTPでは4TPx4が低concurrency TPOT、1TP8DPが高concurrency latency、2TP4DPがthroughputに有利で、単一配置が全load域で最良ではない。

RTP-LLMの強みは単一kernelの絶対性能より、cache localityをglobal schedulerへ組み込み、phase/model modalityごとにresourceを分離し、loadingからdecodeまでproduction lifecycle全体を最適化する点にある。各最適化の利得はworkloadごとに異なるため、headline speedupをsystem全体の一様な倍率として解釈すべきではない。
## 品質への影響
speculative decodingはtarget-model verificationを用い、quantizationではWikiText-2 PPLを併記する。FP8/weight-only/KV quantizationはmemory/latencyを改善するが、precision lossはconfiguration依存であり、paperもPPLを別指標として評価する。
## 既存研究との差
- DistServeはprefill/decode分離とSLO-goodput、phase別parallelism/placementを主問題とするのに対し、RTP-LLMはPDをproduction engineの一要素として、global traffic scheduling、prefix-cache affinity、4階層KV cache、fault recovery、model loadingまで統合する。
- Mooncake/MemServe系のKV-centric disaggregated servingと近いが、RTP-LLMはGPU/local CPU/RDMA remote CPU/3FSのstorage hierarchyをMaster schedulingへ直接結び、同時にspeculative decoding、quantization、MoE parallelism、multimodal servingを一つのengineで提供する。
- vLLM/SGLangのような汎用open-source serving engineと直接競合するproduction frameworkであり、単一paper algorithmではなく多数のengineering optimizationを統合したsystem reportという性格が強い。
- HeteroPanaceaがP/D/A/F分離とstage専用hardwareの設計空間をsimulationで探索するのに対し、RTP-LLM paperは実cluster上のPD、ViT-LLM EPD、cache-aware routingをproduction trafficで検証する。hardware stage specializationの体系的searchは主題ではない。
- model-loading側ではfile-order I/O、single-reader distributed broadcast、shared pinned-buffer reuse、I/O-communication overlapを組み合わせ、serving開始前のelastic deployment latencyもsystem objectiveへ含める点が特徴。
## 限界
- 広範な機能を異なるmodel/workloadで個別評価しており、全機能を同一条件で逐次ablationした統一end-to-end実験ではないため、headline改善を単一機構へ帰属できない。
- production workloadの一部はAlibaba内部serviceで、trace、request distribution、cluster運用条件を外部から完全再現できない。
- PD評価ではTTFT/cache hitが大幅改善する一方tokens/sはSGLang/vLLMとほぼ同等で、throughput優位を一般化できない。
- cache reuse改善はworkload依存で、Internal Robot Q&Aは+215%だがTaobao Merchant Serviceは833->840 tokensに留まる。
- 汎用評価serverは8 GPU/node等を示すが、すべてのsubexperimentでGPU型、baseline version、tuning条件、繰り返し回数やconfidence intervalが十分詳細に示されるわけではない。
- 3FS、Carbon等Alibaba固有infrastructureとの統合がproduction設計の一部であり、他環境で同等のhierarchical cache/fault-recovery behaviorを得るには代替実装が必要。
- quantization qualityは主にsampled WikiText-2 PPLで評価され、reasoning/code/multimodal等のdownstream quality影響は広く検証されていない。
- cost、energy、multi-tenant isolationの定量比較やfailure/recovery時間の詳細benchmarkは本論文の中心評価に含まれない。
## 実装状態
Alibaba公式repository `alibaba/rtp-llm` がApache-2.0で公開されている。公式READMEはproduction利用、PD disaggregation、speculative decoding、DeepEP、FP8 KV cache、quantization等を案内する。ただし論文中の全production configurationと公開main branchのexact commit対応は明記されていないため、再現時はversion固定が必要。
## 研究上の位置づけ
主系統はLLM Serving / Scheduling / Disaggregation。production-proven serving engineとしてPD、hierarchical KV cache、cache-aware schedulingを核に、model loading、speculative decoding、MoE parallelism、quantization、multimodal EPDまでcross-layer統合する。個別最適化論文の寄せ集めではなく、production orchestrationと実traffic validationを持つ総合serving systemとして位置づける。
## 監査メモ
arXiv v1をIntroductionからConclusionまで確認し、system architecture、4-tier KV cache、loading、traffic scheduling、speculative framework、parallelism、quantization、multimodal、全evaluation subsectionとnegative resultを照合した。公式GitHubとApache-2.0公開も確認済み。PDではTTFT優位とthroughput非優位を分離して記録し、production schedulingの+215% cache reuseも対象workloadを限定した。追加auditを必須とする明確な未確認事項はない。
## 一次資料
- https://arxiv.org/abs/2605.29639
- https://arxiv.org/pdf/2605.29639
- https://github.com/alibaba/rtp-llm
