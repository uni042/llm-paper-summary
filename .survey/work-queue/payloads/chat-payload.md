---
canonical_id: "arXiv:2608.14624"
arxiv_id: "2608.14624"
title: "Learning Agent Execution for KV-Cache Management in Agentic Serving"
summary: "CacheScoutはagent実行遷移をオンライン学習し、再利用されやすい固定文脈KVを予測的に保持・事前取得するvLLM上のruntime。"
source: "https://arxiv.org/abs/2608.14624"
last_audited: null
audit_version: 0
---

# Learning Agent Execution for KV-Cache Management in Agentic Serving

## 書誌情報
- **著者**: Rui Zhang, Chaeeun Kim, Shaoting Feng, Kuntai Du, Yuhan Liu, Yi Zhong, Cheng-Wei Ching, Junchen Jiang, Liting Hu
- **公開日**: 2026-07-16
- **状態**: arXiv preprint v1, cs.AI
- **実装**: vLLM v0.11 V1 engine上。約2,300行のruntime logicと約800行のpatch。本文ではcode/benchmark suiteは将来公開予定。

## 一文要約
マルチエージェントLLMで「次にどのagentが呼ばれるか」を軽量なonline transition modelで学習し、その予測をKV-cache evictionとbackground prefetchへ使うことで、同じsystem prompt・tool定義等の再prefillを減らす。

## 問題設定
各agentのsystem prompt、tool definitions、skills、few-shot例からなる固定prefix（agent anchor）は繰り返し利用される。4 workloadでは固定文脈がprompt tokenの53–62%を占め、anchor blockの平均再利用回数は49–173回で、session-history blockの12–15回より4–13倍高い。一方vLLM等のprefix cacheはcontent hashとrecency中心で、blockのagent identityや将来reuseを知らないため、別agent実行中に価値の高いanchorをLRUで追い出し再計算する。

## 手法
### Transition Learner
prompt-prefix fingerprintでagentを識別し、現在agentから次agentへのtransition countをonline更新する。1次Markov modelで遷移確率を推定し、offline trainingや事前定義workflow graphを不要にする。Pipeline/Debate/SelectorGroupChatのentropy reductionは1.0/0.78/0.57で、単純なonline counterでも約50 dispatch以内に次agent top-1精度76–86%へ達する。

### Survival-guided eviction
学習したtransition graph上で現在agentから近いagentほど高いsurvival scoreを与え、そのanchor KVを保護する。最終priorityはsurvival、recency、reconstruction costを組み合わせるため、予測性が弱いとLRU寄りへ戻る。

### Background prefetch
request間のidle時間に最有力の次agentへwarmup requestを発行し、固定prefixを通常prefill pipelineで先にKV化する。entropy reductionが閾値未満ならprefetchを止めるadaptive gatingで誤予測時のGPU浪費を抑える。

## 評価条件
6-agent supervisor frameworkでLlama-3.1-8B-Instructを用い、GSM8K、MT-Bench、GAIA、SWE-benchを評価。比較はvanilla vLLMとContinuum。さらにQwen3-235B-A22B-FP8を4×H200で評価した。

## 主要結果
- KV-cache hit rate: vanilla vLLM比 **+10–18ポイント**、**81–85%**。
- 平均TTFT: **18–45%削減**。
- median TTFT: GAIA **231→114 ms**、GSM8K **239→115 ms**。
- SWE-bench P99 TTFT: **711→342 ms**。
- 平均per-turn latency: **29–38%削減**。
- peak throughput: **19–57%向上**。
- 同一平均latency budget下でvanilla vLLMの**1.7–12×**のarrival load。
- Qwen3-235B-A22B-FP8 / 4×H200では平均TTFT **33–54%削減**、throughput **37%向上**。
- runtime stateは数十agentでも**25 KB未満**、hot-path処理P99は**6 µs未満**。

## 品質への影響
同一prefixの正確なKVを再利用するcache policyであり、KV圧縮・量子化や近似attentionは導入しないため、機構自体にmodel品質trade-offはない。誤prefetchの影響は品質ではなくGPU競合・throughput側に現れる。

## 既存研究との差
vLLM/SGLang等はprefix内容の一致を扱うが将来agent reuseを予測しない。Continuum/InferCeptは主にsession内tool call中のKV保持、KVFlow/Parrot等はstatic graphやannotation依存が強い。近接するPBKVもfuture invocationを予測するが、CacheScoutは1次Markov counterという極めて軽いonline modelに寄せ、µs級hot-path overheadを狙う。Tutti/LMCache/KVDrive等のoffload系とは補完的で、CacheScoutは主に「GPU内で何を残すか」をagent semanticsで決める。

## 限界
1次Markovなので長履歴やtask context依存の分岐は捉えにくい。固定prefixが頻繁に変わるとcross-session reuseが減る。Randomに近いworkflowでは予測利益が小さい。主実装はvLLMのみ。論文時点では公式code公開を確認できず第三者再現性は未確立。高負荷でidle時間が少ない場合はprefetch効果も縮小する。

## 一次資料
- https://arxiv.org/abs/2608.14624
- https://arxiv.org/pdf/2608.14624
