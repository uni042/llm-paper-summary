---
canonical_id: "arXiv:2608.15127"
arxiv_id: "2608.15127"
last_audited: "2026-09-09"
audit_version: 1
storage_targets: ["GPU KV cache", "sandbox state", "conversation/tool state"]
bottlenecks: ["non-LLM tool latency", "cross-component communication", "idle-but-live state", "context/control-plane overhead", "cache eviction"]
hardware_details: "統制評価では各moduleをDocker container化。RAGはx86_64 server + 8×NVIDIA 4090D。Mini-SWEはDeepSeek-V4-ProをSGLang v0.5.12でself-hostし、他のnon-RAG workloadはAlibaba-Bailian APIを主に使用。"
quality_effect: "主にsystems characterizationと独立したproof-of-concept設計探索であり、モデル品質改善を目的としない。tool-result cacheはexact query/URL reuseとTTLを使用。"
evidence_locations: ["arXiv v1 PDF §3–§9", "Table 1–2", "Fig. 3–26"]
title: "From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems"
summary: "10種類のagentic applicationと24時間のproduction traceを統一計測し、LLM推論だけでは説明できないtool、state、communication、control-planeのbottleneckを体系化するAgentSysBench。task-disaggregated serving、communication-aware placement、state offloading、tool-result cachingの独立PoCも評価する。"
authors_affiliations: "Chaokun Chang, Yukun Zhou, Kaihua Fu, Dakai An, Tianyu Feng, Hanfeng Lu, Sheng Yao, Pu Guo, Yinghao Yu, Yizhou Shan, Bo Li, Binhang Yuan, Wei Wang（HKUST; Yinghao Yu: Alibaba Group; Yizhou Shan: ByteDance）"
published: "2026-08-15"
publication_status: "arXiv preprint v1 (2026-08-15)"
lineage: "LLM Serving / Scheduling / Disaggregation"
topics: ["Agent serving", "Workload characterization", "State offloading", "Task-aware scheduling", "Communication-aware placement", "KV cache management", "Tool-result caching"]
importance: "高"
hardware_evaluation: "実機統制評価＋24時間production trace（一部外部model API）"
source: "https://arxiv.org/abs/2608.15127"
code: "未公開（arXiv v1はAgentSysBenchを今後open sourceで公開すると記載）"
last_checked: "2026-09-09"
---

# From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems

> AgentSysBenchは、agentic applicationをLLM callだけでなく、tool、sandbox、retrieval、persistent state、communicationを含む長時間executionとして計測し、従来のLLM servingの前提がどこで崩れるかを明らかにする。主眼は推論kernel単体ではなく、agent execution全体を対象にしたserving designである。

## 概要

論文は、RAG、DeepResearch、HuggingGPT、Mini-SWE、Codex、WebAgent、GUIAgent、Claude Code、Openclaw、Pi-AutoRの10種類を同一の計測枠組みで扱うbenchmark / measurement toolkit **AgentSysBench** を提案する。

従来のserving研究が1回のLLM inference requestを主要な仕事単位とするのに対し、agentic executionではLLM inference、tool call、external environment operation、state updateが連鎖し、1 requestが数秒から数時間に及ぶ。controlled experimentでは4,641 requests、64,924 LLM calls、118,274 tool callsを測定し、さらに24時間のproduction traceとしてcoding agent 35,037 sessions、search-based QA 141,376 sessions、Openclaw-like agent 2,386 sessions、合計178,799 sessionsを解析する。

主要結論は、agentic workloadではLLM token generationだけを高速化しても全体性能を十分改善できず、**tool、heterogeneous resource、long-lived state、communication、control planeまで含めた協調管理が必要**という点にある。

## 問題設定

agentic workloadをrequest distribution `R`、tool/environment set `T`、model/inference policy `M`、orchestration `O`の組 `W=<R,T,M,O>` とし、serving systemをhardware resource `H`、component-serving mechanism `C`、deployment architecture `A` の組として整理する。観測されるlatencyやresource demandはapplication固有の定数ではなく、workloadとserving system双方の組合せから生じるという立場である。

既存capability benchmarkはtask successを中心に測り、latency breakdown、resource profile、state footprint、tool-call behavior、cross-request redundancyを十分記録しない。一方、既存agent serving研究は少数applicationに絞ったpoint solutionが多く、異なるexecution stack間で比較しにくい。このギャップを埋めるため、workload側とserving側を同時に制御・計測する。

## AgentSysBench

### 対象application

10 workloadは単なるdomain diversityではなく、systems behaviorの違いを意図して選ばれる。RAGは比較的固定pipeline、Mini-SWE/Codex等はReAct loop、DeepResearchはparallelism、planning、branching、loopを含む。toolもvector DB、embedding、shell/filesystem、browser/GUI、MCP、searchなど異なるresource affinityを持つ。

### Serving stackとinstrumentation

componentをDocker container等で分離し、LLM engine、embedding、vector database、sandbox、browser/GUI environment、search serviceをlocal/remoteに配置できる。orchestrator/proxy/sandbox/container layerでoperation traceを取り、cAdvisorでCPU/memory/disk/network、NVIDIA DCGM ExporterでGPU utilization/memory、Prometheusでtime seriesを収集する。

default controlled deploymentでは、RAG以外はcutting-edge NVIDIA GPU server上でmoduleをcontainer化しshared-memory-based virtual networkで接続する。Mini-SWEはDeepSeek-V4-ProをSGLang v0.5.12でself-hostし、他のnon-RAG workflowはAlibaba-Bailian APIを使う。RAGはx86_64 server + 8×4090Dで動かす。embeddingはjina-embeddings-v3 + TEI、RAG/DeepResearchはMilvus、DeepResearchはExa searchを利用する。

## 主要な観測結果

### 1. LLM以外が支配的になる

10 application中5つではtool/environmentが全体latencyをdominantまたはco-dominantにする。GUIAgentではdesktop sandboxが70%以上、Pi-AutoRでは実験runtimeが約90%を占める。agent executionは数秒から数時間までheavy-tailedで、model-only optimizationの限界が明確である。

### 2. Token usageとprefix cache依存

iterative agentはhistory、tool output、system promptを継続追加するためtoken usageが急増する。static prefixを保つapplicationではprefix cache hitが高い一方、contextを頻繁に再構成するworkloadではreuseが大きく落ちる。

cached prefixでもattentionは既存KVを読む必要があり、context長増加に伴うmemory trafficは残る。実測では単一Claude Code sessionで大model利用時のKV cacheが最大約11 GBに達する例を示す。

### 3. 管理すべきstateが多い

論文はstateを3種類に分ける。

- **performance state**: KV cacheなど。失ってもcorrectnessは壊れないがrecompute costが大きい。
- **persistent correctness state**: vector DB collection、filesystem change、installed dependency等。失うとsession semanticsが壊れる。
- **active working set**: compile/test中のsandbox DRAM等。一時的で、quiescent checkpoint時に全て保存する必要はない。

sandboxのmedian peak DRAMは約0.8 GBだが、session peakは28 GBに達する。28 GBはpersistent checkpoint sizeではなくactive working-set peakなので、state offload設計では区別が必要である。

### 4. Cross-stack / invocation heterogeneity

LLMはGPU-bound、vector DBはmemory-bound、sandboxはCPU-bound、network serviceはnetwork-boundとresource affinityが違う。同一taskでもinput/output量によりlatency差が大きく、Mini-SWEの同一trace内LLM invocationは最大30倍、sandbox commandでは最長が最短の171倍となる。

長context requestをshort requestとco-batchするとshort側TPOTが悪化し、shared sandboxもCPU/cache contentionで遅くなる。したがってsingle shared queue / worker poolはhead-of-line blockingやco-batching interferenceを生む。

### 5. Bottleneckが動く

request size、model choice、tool representation、orchestration、hardware allocation、deployment placementの変更だけでdominant componentが変わる。例えばDeepResearchではwriter/summarizerをDeepSeek-V4-FlashからV4-Proへ変えると、embedding中心からLLM中心へbottleneckが移る。token countだけではlatencyを予測できない。

### 6. Long idle-but-live session

production coding-agent 35,037 sessionsでは、median sessionがlifetimeの20%しかactive executionしておらず、70%のsessionがlifetimeの半分未満しかcomputeしていない。idle intervalは秒〜時間に及び、多くは1〜10分である。

この間もsandbox、terminal context、KV cache、conversation historyはresume用に保持される。running/finishedの2状態ではなく`waiting`をfirst-class lifecycle stateにし、correctness stateをdurable tierへcheckpointし、KV等performance stateをreuse予測に応じてretain/offload/prefetchする設計を提案する。

### 7. Control-plane tax

production agentではtool schema、raw observation、history、safety/loop-detection等がcontextとmodel callを消費する。あるsessionのstep 261では次action 151 token生成のため166,721 input tokensを処理している。

35,037 sessions中3,170回のcontext compactionがあり、平均176K input tokens / 5K output tokensを消費する。compaction latencyは平均156 s、p95 161 s、p99 775 s。さらにguardrail等のauxiliary taskが2,684 LLM callsを追加する。

production prefix-cache TTLは5分で、35,037 sessionの59.4%が少なくとも1回cache evictionを経験する。human-paced idle intervalと固定TTLの不一致がre-prefillを招くため、reuse-aware KV policyを主張する。

### 8. Cross-request redundancy

search-based QAの141,376 sessionsは373,678 search invocationsを発生させる。distinct queryの27%が再出現し、それらが全search callの67.3%を占める。

Openclaw-like traceでは2,386 sessions / 4,389 fetch invocationsを分析し、distinct URLの24%が再出現して全fetchの64%を占める。per-sessionではなくshared tool boundaryでcacheする機会がある。

## Design exploration

### Task-disaggregated serving

logical taskごとに独立service / resource poolを与える。Dynamic RAGでcomponent-disaggregated baselineに対し、load levelに応じてaverage latencyを29–40%削減する。異種taskを同一queueへ混ぜることによるHOL blockingとinterferenceを避けるのが狙いである。

### Communication-aware placement

communication量が多いembeddingとvector DBをco-locateする。完全distributed RAGでは高concurrency時にnetwork transferが実行時間の67.5%を占めるが、embedding + vector DB co-locationで平均latencyをlow load時2.8倍、高load時最大4.5倍改善する。

### State offloading

Mini-SWEでLLM planning中にinactive sandboxをoffloadし、次tool step直前にrestoreする。triggerはcontext length予測ではなくin-flight planning callのelapsed timeである。

このPoCではaggregate resident sandbox memoryを平均4.6倍、peak 2.1倍削減し、E2E latency増加は0.5%以内。これはproductionのhuman-paced pauseを直接再生した評価ではなく、controlled Mini-SWE内のinter-component idleを利用した実験である。

### Tool-result caching

exact query cacheとURL-level deduplicationを評価する。10分TTLでquery cacheはredundant search callsを35.2%削減し、aggregate search latencyを19.3%削減。URL cacheはweb-fetch callを11.65%削減し、aggregate fetch latencyを16.5%削減する。

## LLM推論システム研究との関係

1. **KV cache管理**: fixed TTLではhuman-paced returnと合わずre-prefillが多い。session return予測とwaiting stateを使ったretain/offload/prefetchが必要になる。
2. **階層memory/state**: KVだけでなくsandbox、conversation history、tool artifactをcold/warm/hot tierへ配置する余地がある。SSD/NVMeはlong-idle sessionのcorrectness/performance stateを保持する候補になる。
3. **serving scheduling**: task type、resource affinity、communication量、state restoration costを考慮したplacement/queueingが必要になる。

## 正式監査（2026-09-09）

### Identity / bibliography

- canonical identity: arXiv:2608.15127
- arXiv category: cs.OS
- version: v1、2026-08-15
- authorsは原PDF記載順へ修正した。
- affiliationはHKUSTが主要著者群、Yinghao YuがAlibaba Group、Yizhou ShanがByteDance。

### Code / implementation status

arXiv v1本文にはAgentSysBench自体のrepository URLは記載されておらず、IntroductionとConclusionで**今後open sourceとしてreleaseする**と記載している。2026-09-09時点の監査では、論文タイトル/AgentSysBench名に明確に対応する公式repositoryを一次情報として確認できなかったため、`code`は未公開扱いとする。

### Controlled evaluation conditions

AgentSysBench自体は実runtime componentをcontainerized deploymentで計測する。RAGは8×4090D、Mini-SWEはSGLang v0.5.12 + self-hosted DeepSeek-V4-Pro。他のnon-RAG workflowにはAlibaba-Bailian APIが含まれるため、全LLM evaluationを同一GPU条件で比較したものではない。

したがってapplication間のlatency絶対値は「同一model/hardware条件の純粋比較」ではなく、representative application stackをsystems-oriented instrumentationでcharacterizeした値と解釈する必要がある。

### Production trace provenance

論文が公開するtrace descriptionは3 deployed applications、24時間分で、coding agent 35,037 sessions、search-based QA 141,376 sessions、Openclaw-like agent 2,386 sessions。production traceはcontrolled experimentを直接validateするためではなく、user think time、idle-but-live state、control-plane tax、cross-session redundancyなどlaboratory benchmarkでは出にくい現象を補完的に示すものと論文自身が位置付ける。

service/operator名やraw trace自体は本文から完全公開されていないため、production数字は著者提供traceに基づく観測として扱う。

### Key quantitative results verification

本文・図を再照合し、以下を確認した。

- task-disaggregated serving: average latency 29–40%削減
- communication-aware placement: fully distributed比で最大4.5×
- state offloading: average memory 4.6×、peak memory 2.1×削減、latency増加0.5%以内
- query cache (TTL 10 min): search call 35.2%削減、aggregate search latency 19.3%削減
- URL cache (TTL 10 min): web-fetch call 11.65%削減、aggregate fetch latency 16.5%削減
- coding-agent production trace: 35,037 sessions中59.4%がprefix-cache evictionを少なくとも1回経験
- compaction: 3,170 events、平均176K input tokens、平均156 s、p99 775 s

### Real hardware vs simulation

本論文はsimulation-only paperではない。controlled application/component experimentとproduction traceが中心で、実software stack / resource monitorを用いる。一方、外部model APIを使うworkflowもあるため、全結果が同一controlled local hardware measurementではない。

4つのdesign explorationは**独立したproof of concept**であり、4機構を統合したproduction systemのend-to-end evaluationではない。

## 既存研究との差

vLLM/SGLangはLLM inference request内部のexecution/memory効率を主対象とするが、AgentSysBenchはその外側のtool、sandbox、state、networkを含む。Autellix、Parrot、Ayo等が具体的serving mechanismを提案するのに対し、本論文は広いapplication collection + production traceによるworkload characterizationが中心である。

したがって4つのoptimizationは最終architectureというより、characterizationからsystem optimizationへ接続できることを示すPoCとして読むべきである。

## 限界

- 10 applicationはsystems-relevant regionを意図的にcoverする選択であり、全agent workloadの統計的sampleではない。
- non-RAG workflowの一部はexternal model APIを使うため、LLM内部GPU conditionを完全にはcontrolできない。
- production traceは3 deployed service由来で、raw datasetやservice identityが本文だけでは完全再現できない。
- design explorationは独立PoCで、統合production systemではない。
- state-offload PoCはhuman-paced long idleを直接replayせず、Mini-SWEのLLM planning intervalを利用する。
- exact-match / TTL tool cacheはsemantic equivalence、tenant isolation、freshness consistencyを全面的には解かない。

## 研究上の含意

agent servingではSSD/NVMeをmodel weightやKVだけのcapacity tierと見るより、**session state全体の階層化**へ拡張する余地が大きい。KV cache、sandbox filesystem/process state、conversation/tool artifactをwaiting stateで退避し、return predictionを使ってSSD→DRAM→GPUへrestoreする制御が自然である。

またstate restoration costをschedulerへ入れると、単なるGPU load balanceではなく「どのnodeへsessionをresumeさせるか」「どのstateを事前prefetchするか」をjoint optimizationできる。

## 一次資料

- arXiv: https://arxiv.org/abs/2608.15127
- PDF: https://arxiv.org/pdf/2608.15127

## 更新履歴

- 2026-09-09: workflow v9新着探索から新規精読。
- 2026-09-09: 正式監査v1。著者順、affiliation、publication status、code未公開状態、controlled deployment、production trace provenance、主要定量値、実機/外部API/PoC区分を再確認。
