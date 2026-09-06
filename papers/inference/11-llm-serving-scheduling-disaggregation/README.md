# LLM Serving / Scheduling / Disaggregation

複数のrequestを複数GPU / nodeで処理するLLM servingについて、**requestを実行する順番、batchの組み方、prefillとdecodeへのGPU配分、KV cacheの再利用、複数GPU間でのrequest移動、GPU数の増減**などを調整し、待ち時間とGPU効率を改善する研究をまとめる。

この系統では、単一requestのkernel高速化よりも、**「どのrequestを先に処理するか」「どのGPUへ送るか」「prefillとdecodeを同じGPUで処理するか分けるか」「過去のKV cacheをどこまで再利用するか」「混雑したGPUから別GPUへrequestを移すか」**といった、serving system全体の制御が中心になる。

ここで使う **SLO（Service Level Objective）** は「最初のtokenが返るまでの時間や、その後のtoken間隔などについて設定した性能目標」を指す。論文によっては **goodput** という語を使うが、このREADMEでは原則として「SLOを満たして処理できるrequest数」と言い換える。

KV cacheをCPU / storageへ退避すること自体が主目的の研究は `KV Cache Offload / Recomputation`、MoE expertの配置や転送が主目的の研究は各MoE系統に分類する。

## 収録論文

収録論文: 23本。公開日が新しい順。

- 2025-01-24 — [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)
  - client間の処理量差を一定範囲に抑えつつ、その範囲内では同じprefixを共有するrequestを同じGPUへ集め、KV cacheの再利用と公平性を両立する。
- 2025-01-14 — [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)
  - interactive requestとbatch requestで異なるSLOを考慮し、GPU内のbatch sizeとcluster全体のGPU数を混雑状況に応じて別々に調整する。
- 2024-08-28 — [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)
  - promptから正確な出力長を当てるのではなく「どのrequestが短そうか」という順番を予測し、短いrequestを先に処理して長いrequestによる待ち時間を減らす。
- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
  - prefillとdecodeを別GPU群へ分け、CPU DRAM・SSD・networkを使ったcluster全体のKV cacheとrequest配置をまとめて管理し、長context requestの処理量を高める。
- 2024-06-25 — [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)
  - GPU HBMとCPU DRAMにあるKV cacheを複数instanceから共有できるようにし、過去contextの再利用とprefill / decode分離を同じ仕組みで扱う。
- 2024-06-05 — [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)
  - batch / interactive request、複数model、異なるSLOを同じqueueで扱い、予測待ち時間を使ってrequestの順番と実行先GPUを調整する。
- 2024-06-05 — [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)
  - 実行中requestとKV cacheを、停止時間を小さく保ったまま別GPUへ移し、GPU間の混雑差やmemory不足を実行中に修正する。
- 2024-05-30 — [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)
  - 複数のLLM callがどの順で依存し、どのprompt部分を共有しているかをserving側へ伝え、application全体を見て並列実行・batching・prefix再利用を調整する。
- 2024-05-08 — [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)
  - 同じprefixを持つrequestを同じGPUへ送ると得られるKV再利用の利益と、そのGPUが混雑する不利益を比較して、request配置を決める。
- 2024-04-25 — [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)
  - ユーザーが実際に文章を読む速度まで考慮し、すでに十分先まで生成済みのrequestを一時停止して、待たされているrequestへGPU時間を回す。
- 2024-03-23 — [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)
  - multi-turn conversationの過去KVをDRAM / SSDへ保存し、次のturnで必要になる部分を先読みして、過去conversationの再計算を減らす。
- 2024-03-04 — [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)
  - 長いprefillを小さく分割し、decodeを先に処理したうえで残った計算枠へprefillを入れ、長いpromptがdecodeを長時間止めるのを防ぐ。
- 2024-01-25 — [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)
  - modelをまだGPUへ読み込んでいない状態からの起動時間を短くするため、checkpointをlocal SSD / DRAMへ保持し、modelがある場所を優先してrequestを配置する。
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
  - prefillとdecodeを別GPU群へ分け、それぞれのGPU数と並列化方法を、最初のtokenが返るまでの時間とtoken生成間隔のSLOに合わせて別々に決める。
- 2024-01-09 — [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)
  - 長いpromptを小分けにし、短いprefillやdecodeと同じforwardへ混ぜて、1回のforwardで処理するtoken数を揃え、処理時間のばらつきを抑える。
- 2023-12-31 — [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)
  - clientごとにこれまで処理した入力・出力token量を記録し、処理量が少ないclientを優先することで、GPUを遊ばせずにclient間の公平性を保つ。
- 2023-12-12 — [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)
  - 複数のgeneration callや条件分岐を含む処理をruntimeが理解し、共有prefixを木構造で管理してKVを再利用する仕組みなどを使って、application全体の実行を効率化する。
- 2023-12-09 — [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)
  - multi-turn conversationの過去KVをrequest終了後もGPU / CPUに残し、次のturnで同じhistoryを再びprefillする計算を避ける。
- 2023-11-30 — [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)
  - prefillとdecodeを別machine poolへ分け、それぞれに向くGPUや電力設定を使い分けて、cluster全体のthroughput・cost・消費電力を改善する。
- 2023-11-27 — [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)
  - 安価だが突然利用できなくなる可能性があるspot GPUの増減に合わせてmodel配置を組み替え、既存weight / KVを再利用しながらrequestを継続する。
- 2023-09-12 — [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)
  - KV cacheを固定長blockへ分け、必要になった分だけmemoryを割り当てることで、未使用領域を減らし、同時に処理できるrequest数を増やす。
- 2023-05-10 — [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)
  - output tokenを1つ生成する区切りごとにrequestを一時停止・再開できるようにし、短いrequestを優先しながらKVを先回りしてGPUへ戻して待ち時間を減らす。
- 2022-07-11 — [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)
  - output tokenを1つ生成するたびにbatchを組み替え、長さや進行位置が異なるrequestを途中からbatchへ出し入れできるようにする。

## 主な技術の分岐

- **1 token生成ごとにbatchを組み替える:** Orcaはrequest全体が終わるのを待たず、output tokenを1つ生成するたびに新しいrequestをbatchへ入れられるようにした。
- **KV cacheを必要量だけ確保する:** vLLMはKV cacheを固定長blockで管理し、requestごとに最大長分を先に確保する無駄を減らす。
- **実行中requestの優先順位を変える:** FastServeはtoken生成の区切りでrequestを一時停止できるようにし、短いrequestを先に進めて長いrequestによる待ちを減らす。
- **出力が短そうなrequestを予測する:** Efficient LLM Scheduling by Learning to Rankは、正確な出力長ではなくrequest同士の長短の順番を予測して短いrequestを優先する。
- **長いprefillを小分けにする:** DeepSpeed-FastGenとSarathi-Serveは、長いpromptを一度に処理せず小さな単位へ分け、decodeと交互または同じforwardで処理して長時間の停止を防ぐ。
- **SLOに合わせてqueueを並べ替える:** QLMは予測待ち時間、残りSLO余裕、modelがすでにGPUへ載っているか、GPUの混雑度を見てrequest順序と実行先を決める。
- **混雑に応じてGPU数を変える:** ChironはGPU内batch sizeとcluster全体のinstance数を別々に調整し、急な混雑にはまずbatch調整、それでも足りなければGPUを増やす。
- **ユーザーが読む速度を考慮する:** Andesは「生成済みtokenがユーザーの読む速度より十分先行しているrequest」を一時停止し、すぐにtokenが必要なrequestへ計算時間を回す。
- **共有prefixを再利用しやすいGPUへ送る:** PrebleはKV再利用で節約できる計算量とGPUの混雑を比べ、同じprefixを持つrequestを集めすぎないように配置する。
- **client間の公平性とprefix再利用を両立する:** Fairness in Serving LLMsはclientごとの処理量を揃える。Locality-aware Fair Schedulingは、その公平性を壊さない範囲で共有prefixを持つrequestをまとめる。
- **複数LLM callの依存関係を利用する:** Parrotはcall間で受け渡す値と依存関係をserving側へ伝え、SGLangはprogram構造と共有prefix cacheを使って複数callをまとめて効率化する。
- **conversationのKVをrequest間で再利用する:** PensieveはGPU / CPUへ過去KVを残し、CachedAttentionはさらにDRAM / SSDも使って長期間保持・先読みする。
- **prefillとdecodeを別GPU群へ分ける:** DistServeは両phaseを独立に増減できるようにし、それぞれのlatency目標に合わせてGPU数を決める。
- **prefill / decode分離と共有KV cacheを組み合わせる:** MemServeはGPU HBMとCPU DRAMをまたぐ共有KV poolを作り、どのinstanceからでも過去contextを再利用できるようにする。
- **phaseごとに異なるhardwareを使う:** Splitwiseはprefillとdecodeにそれぞれ適したGPUや電力設定を割り当てる。
- **modelの起動待ちを減らす:** ServerlessLLMはcheckpointがすでにlocal SSD / DRAMにあるGPUを優先し、model loadingを高速化する。
- **不安定なspot GPUを使う:** SpotServeはGPUが突然増減してもmodel配置とrequest状態を組み替えて処理を継続する。
- **実行中requestを別GPUへ移す:** LlumnixはKVを転送しながら元GPUでdecodeを続け、最後の短い差分だけ停止して移すことで移動時の停止を短くする。
- **cluster全体でKV cacheを共有する:** MooncakeはCPU DRAM・SSD・networkを使ってKVをGPU間で再利用し、どのGPUへrequestを送るかとKV再利用を同時に決める。

この系統では今後も、専門用語そのものより**「何をどこからどこへ動かすのか」「何を基準にrequest順序を決めるのか」「その結果どの待ち時間やresource使用量が減るのか」**が分かる説明を優先する。