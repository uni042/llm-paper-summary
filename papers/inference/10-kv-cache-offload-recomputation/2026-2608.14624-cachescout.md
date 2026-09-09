---
canonical_id: "arXiv:2608.14624"
arxiv_id: "2608.14624"
title: "Learning Agent Execution for KV-Cache Management in Agentic Serving"
summary: "複数のLLMエージェントを順番に呼ぶシステムでは、各エージェント固有のsystem promptやtool定義が何度も再利用される。CacheScoutは『今のエージェントの次に誰が呼ばれやすいか』を実行履歴から軽量に学習し、近く再利用されそうなエージェントの固定prefix KVをGPUに残し、空き時間には次候補のKVを先に作ることで再prefillを減らす。"
source: "https://arxiv.org/abs/2608.14624"
last_audited: "2026-09-09"
audit_version: 1
---

# Learning Agent Execution for KV-Cache Management in Agentic Serving

> 複数のLLMエージェントを順番に呼ぶシステムでは、各エージェント固有のsystem promptやtool定義が何度も再利用される。CacheScoutは「今のエージェントの次に誰が呼ばれやすいか」を実行履歴から軽量に学習し、近く再利用されそうなエージェントの固定prefix KVをGPUに残し、空き時間には次候補のKVを先に作ることで再prefillを減らす。

## 書誌情報

- **著者**: Rui Zhang, Chaeeun Kim, Shaoting Feng, Kuntai Du, Yuhan Liu, Yi Zhong, Cheng-Wei Ching, Junchen Jiang, Liting Hu
- **公開**: 2026-07-16, arXiv v1
- **種別**: プレプリント（preprint）
- **主題**: エージェント型LLM提供（agentic serving）、KVキャッシュ管理、prefix cache、online learning、prefetch
- **実装**: vLLM v0.11 V1 engine上に約2,300行のruntime logicと約800行のpatchを実装。論文時点ではコード・benchmark suiteは将来公開予定。

## 概要

CacheScoutが対象にするのは、**一つのLLMを繰り返し呼ぶ普通のchatではなく、複数のLLMエージェントが役割分担するシステム**である。

例えばソフトウェア開発エージェントなら、

1. supervisorが依頼を読む
2. plannerが計画を作る
3. coderがコードを書く
4. reviewerが確認する
5. 必要ならcoderへ戻る

といった順に複数agentを呼ぶ。

各agentは単に名前が違うだけではなく、固有のsystem prompt、tool定義、skill説明、few-shot例などを持つ。これらはそのagentが呼ばれるたびに同じ内容をprefixとしてLLMへ入力する。

LLMはprefixを最初に入力処理（prefill）すると、その結果を**KVキャッシュ（KV cache）**として保持できる。同じprefixをまた使うなら、そのKVが残っていれば再prefillしなくて済む。

問題はGPUメモリが有限なことである。多くのagent・多くのsessionが同時に動くと、すべてのKVを残せない。一般的なprefix cacheは「最近使ったblock」などを基準に古いものを追い出すため、**今は使っていないが数step後にほぼ確実に再利用されるagentの固定prefix**を捨ててしまう場合がある。

CacheScoutは、agent workflowにはある程度の順序性があることを利用する。「plannerの次はcoderが来やすい」「reviewerの次はcoderか終了が多い」といった遷移をonlineで学習し、将来価値の高いKVを保護する。

## 問題設定

### Session historyとagent固定prefixは再利用の性質が違う

LLM cacheには大きく二種類のprefixが混在する。

一つは**session history**で、その会話固有の過去メッセージである。これは同じsession内では使うが、別sessionでは再利用しにくい。

もう一つは各agentの**固定文脈（agent anchor）**で、system prompt、tool descriptions、skills、few-shot examplesなどである。これは同じagentが呼ばれるたび、多数sessionを跨いで何度も使える。

論文の4 workloadでは、固定文脈はprompt token全体の**53〜62%**を占める。anchor blockの平均再利用回数は**49〜173回**で、session-history blockの12〜15回より約4〜13倍高い。

したがって、同じ「最近使われていないKV」でも価値は大きく違う。

### なぜLRUだけでは足りないのか

LRU（Least Recently Used）は「最後に使った時刻が古いものから追い出す」cache policyである。

普通のcacheでは有効だが、agent workflowでは次のようなことが起こる。

```text
Planner → Coder → Reviewer → Coder
```

Reviewer実行中、CoderのKVは「最近使っていない」のでLRU上は追い出し候補になる。しかしworkflowから見れば、次にCoderへ戻る確率が高い。

つまりagent servingでは**過去のrecencyより、未来の呼出し確率の方が重要な場合がある**。

## 手法のあらまし

CacheScoutは複雑な深層予測モデルを使わない。

まず各agentを固定prefixのfingerprintで識別し、実際の実行順から「agent Aの次にagent Bが何回呼ばれたか」をcountする。これで小さな遷移表を作る。

次に現在agentから近い将来に到達しそうなagentほど、そのanchor KVへ高い生存優先度を与える。cacheが満杯になれば、未来価値が低いものから追い出す。

さらにrequest間にGPUの空き時間がある場合、最も有力な次agentの固定prefixを通常のprefill処理へ先に通し、KVをwarm-upする。

ただしworkflowがランダムに近く予測できない場合は、積極的なprefetchを止める。

## 手法

### 1. Agentをprefix fingerprintで識別する

runtimeは、各agentのsystem prompt等の固定prefixからfingerprintを作り、「これはplanner」「これはcoder」といったagent identityを認識する。

ユーザー側が事前にworkflow graphを登録する必要はない。実際にどのagent prefixが呼ばれたかだけを観測する。

この設計により、framework内部の明示的なagent名やapplication-specific metadataに強く依存しない。

### 2. Transition Learner — 次agentを単純な遷移回数で学習する

現在agentを`A`、次に呼ばれたagentを`B`とすると、runtimeは`A→B`のcounterを1増やす。

これを繰り返し、

`P(next=B | current=A)`

を実行回数から推定する。

これは**一次マルコフモデル（first-order Markov model）**である。「次に誰が来るかは、主に現在誰かで決まる」と近似し、それより前の長い履歴は使わない。

モデルとしては非常に単純だが、agent workflowには決まった役割遷移があることが多いため十分機能する。

論文ではPipeline、Debate、SelectorGroupChatなどで遷移分布の不確実性が下がり、約50 dispatch以内に次agent top-1精度が**76〜86%**へ達する条件を示す。

### 3. なぜonline learningにするのか

workflowをofflineで学習する方式では、applicationごとに事前traceが必要になる。さらにpromptやagent構成が変わると再学習が必要になる。

CacheScoutは数個のcounterを更新するだけなので、実行しながら適応できる。

新しいworkflowなら最初は情報がないため、通常cacheに近い挙動をし、遷移を観測するほど予測性を増す。

### 4. Survival-guided eviction — 近く再利用されるanchorを残す

現在agentから遷移graphをたどり、将来呼ばれそうなagentへ**生存スコア（survival score）**を与える。

現在位置から近く、遷移確率が高いagentほど高く評価する。

ただし最終eviction priorityを予測だけで決めるわけではなく、

- survival score
- 最近使われたかというrecency
- そのKVを失った場合の再構築cost

などを組み合わせる。

そのため予測性が低いworkflowでは、実質的にLRU寄りへ戻る。

### 5. 「anchorを守る」と何が速くなるのか

あるagentのanchor KVがcacheに残っていれば、そのagentを再び呼んだとき、system promptやtool definitionsをもう一度prefillする必要がない。

ユーザー固有の最新会話部分だけを追加処理してdecodeへ進める。

固定prefixがprompt tokenの半分以上を占めるagent workloadでは、この差がTTFTへ直接効く。

### 6. Background prefetch — idle時間に次agentをwarm-upする

cacheにまだ次agentのanchorがない場合でも、今のrequest処理と次requestの間にGPUが空いていれば、次候補のanchorを事前prefillできる。

CacheScoutは最有力のnext agentについて**warmup request**をbackgroundで発行する。

これは近似KVを作るのではなく、通常のprefill pipelineを先に実行してexact KVをcacheへ入れる方式である。

したがって予測が当たれば次agentのTTFTが減る。外れれば不要なGPU計算をしただけで、model品質は変わらない。

### 7. 不確実なときはprefetchしない

予測分布が

- coder 90%
- planner 5%
- reviewer 5%

なら先読み価値は高い。

一方、

- coder 34%
- planner 33%
- reviewer 33%

なら1つをprefetchしても外れやすい。

論文は遷移分布のentropy reductionを使い、十分予測可能なときだけprefetchする**適応ゲート（adaptive gating）**を入れる。

これにより高負荷時に誤prefetchが本来requestのGPU時間を奪うリスクを抑える。

### 8. Hot pathを軽く保つ

cache policyが高性能でも、requestごとに重い予測modelを動かせばserving latencyを増やす。

CacheScoutの状態は数十agentでも**25 KB未満**、hot-pathの処理P99は**6 µs未満**と報告される。

これは一次Markov counterを選んだ理由でもあり、system-levelでは予測精度だけでなく**予測器そのもののoverhead**が重要になる。

## 評価

### まず見るところ

- **KV hit**: vanilla vLLM比+10〜18ポイント、81〜85%。
- **TTFT**: 平均18〜45%削減。
- **turn latency**: 平均29〜38%削減。
- **throughput**: peak 19〜57%向上。
- **大規模MoE**: Qwen3-235B-A22B-FP8 / 4×H200でも平均TTFT 33〜54%削減。
- **品質**: exact prefix KVを通常prefillで作って再利用するため、近似cacheではない。
- **効きにくい条件**: workflowがランダム、anchorが頻繁に変わる、高負荷でidle時間がない場合。

<details>
<summary>評価条件・詳細な数値を開く</summary>

6-agent supervisor frameworkでLlama-3.1-8B-Instructを用い、GSM8K、MT-Bench、GAIA、SWE-benchを評価する。比較はvanilla vLLMとContinuum。

さらにQwen3-235B-A22B-FP8を4×H200で評価する。

### KV-cache hit rate

vanilla vLLM比で**+10〜18ポイント**改善し、全体で**81〜85%**。

### TTFT

平均TTFTは**18〜45%削減**。

代表値:

| Workload | Baseline median TTFT | CacheScout |
|---|---:|---:|
| GAIA | 231 ms | 114 ms |
| GSM8K | 239 ms | 115 ms |

SWE-benchのP99 TTFTは**711 ms → 342 ms**。

### End-to-end turn latency / throughput

- 平均per-turn latency: **29〜38%削減**
- peak throughput: **19〜57%向上**
- 同一平均latency budgetでvanilla vLLMの**1.7〜12倍**のarrival loadを処理

### 大規模MoE

Qwen3-235B-A22B-FP8 / 4×H200では

- 平均TTFT: **33〜54%削減**
- throughput: **37%向上**

を報告する。

</details>

## 主要結果の読み方

CacheScoutは、prefix cacheの価値を「内容が一致するか」だけでなく**workflow上いつ再利用されるか**で評価する研究である。

同じagent anchorは何十〜百回も使えるため、本来cache価値が高い。しかしrecencyだけでは、一時的に別agentへ移っただけで追い出される。

agent execution orderがある程度予測可能なら、将来再利用確率をcache policyへ入れるだけでhit rateを改善できる。

一方、この利得はagent semanticsに依存する。完全にランダムなtool/agent選択であれば未来予測は効かず、通常LRUとの差は小さくなる。

## 品質への影響

CacheScoutはKVを圧縮・近似しない。

cache hit時は以前通常のprefillで生成した同一prefixのKVを再利用し、prefetchでも通常prefillでKVを生成する。

したがって誤予測の影響は**品質ではなく計算資源の無駄**として現れる。外れprefetchが多いとGPU競合でlatency/throughputが悪くなる。

## 既存研究との差

- **vLLM / SGLang prefix cache**: 内容一致とrecencyを扱うが、将来どのagentが呼ばれるかは予測しない。
- **Continuum / InferCept**: tool call中などsession内のKV保持と関連する。CacheScoutは複数agent間の固定anchor再利用を主対象にする。
- **static workflow graph方式**: application側がgraph/annotationを提供する方式と異なり、実行履歴からonlineで遷移を学習する。
- **KV offload研究**: CPU/SSDへKVを置く位置を決めるのではなく、主にGPU内cacheで**何を残すか・何を先に作るか**を決める。両者は組み合わせ可能。

## 限界

- 一次Markovなので、数step前の履歴やtask内容で分岐するworkflowは捉えにくい。
- agentの固定prefix自体が頻繁に変わるとcross-session reuseが減る。
- Randomに近いworkflowでは遷移予測価値が低い。
- 高負荷でGPU idle時間がほとんどなければbackground prefetchの余地が小さい。
- 主実装はvLLMで、他serving engineへの移植評価は限定的。
- 論文時点で公式コード公開は確認できず、第三者再現性は未確立。

## 一般的な実装上の含意

エージェント型LLMではKV cache policyへ**application semantics**を持ち込む価値がある。

従来cacheはtoken hash、サイズ、recencyなど低レベル情報だけを見ることが多い。しかしagent workloadでは、

- どのprefixがagent固有か
- どのagentが次に呼ばれやすいか
- 再構築costはいくらか

という上位情報が将来reuseをよく説明する。

これはKV以外にも応用できる。tool sandbox、model replica、LoRA adapter、retrieval indexなども、workflow遷移が分かればprefetch/evictionを先回りできる。

ただし予測器のoverheadが大きいと本末転倒なので、**低精度でもµs級で更新できる予測器の方がservingでは有利な場合がある**という点も重要である。

## 一次資料

- arXiv: https://arxiv.org/abs/2608.14624
- PDF: https://arxiv.org/pdf/2608.14624

## 更新履歴

- 2026-09-09: MoE-Infinity基準に合わせて全面改稿。agent anchor、prefix cache、Markov遷移、survival-guided eviction、background prefetch、adaptive gatingを論文未読者向けに説明。
