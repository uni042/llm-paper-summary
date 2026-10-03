# Scheduled worker :00 worklist

Worker: `scheduled-chat-00`  
Generated: `2026-10-03T13:58:01+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **606** / 未claim総数: **459** / このworker向け: **153**

| # | score | 種別 | identity | title | source | 想定配置先 |
|---:|---:|---|---|---|---|---|
| 1 | 74 | audit | arXiv:2503.03777 | FlexInfer: Breaking Memory Constraint via Flexible and Efficient Offloading for On-Device LLM Inference | [primary](https://arxiv.org/abs/2503.03777) | `papers/inference/01-offload-hierarchical-memory/2025-2503.03777-flexinfer-flexible-efficient-on-device-offloading.md` |
| 2 | 0 | research | arXiv:1712.05889 | Ray: A Distributed Framework for Emerging AI Applications | [primary](https://arxiv.org/abs/1712.05889) | `papers/inference/99-other-inference-systems/2017-1712.05889-ray-a-distributed-framework-for-emerging-ai-applications.md` |
| 3 | 0 | research | arXiv:1909.08053 | Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | [primary](https://arxiv.org/abs/1909.08053) | `papers/training/03-pipeline-parallel-modular-training/2019-1909.08053-megatron-lm.md` |
| 4 | 0 | research | arXiv:2006.09616 | Dynamic Tensor Rematerialization | [primary](https://arxiv.org/abs/2006.09616) | `papers/inference/99-other-inference-systems/2020-2006.09616-dynamic-tensor-rematerialization.md` |
| 5 | 0 | research | arXiv:2010.05680 | TurboTransformers: an efficient GPU serving system for transformer models | [primary](https://arxiv.org/abs/2010.05680) | `papers/inference/99-other-inference-systems/2020-2010.05680-turbotransformers-an-efficient-gpu-serving-system-for-transformer-models.md` |
| 6 | 0 | research | arXiv:2101.06840 | ZeRO-Offload: Democratizing Billion-Scale Model Training | [primary](https://arxiv.org/abs/2101.06840) | `papers/inference/99-other-inference-systems/2021-2101.06840-zero-offload-democratizing-billion-scale-model-training.md` |
| 7 | 0 | research | arXiv:2110.02861 | 8-bit Optimizers via Block-wise Quantization | [primary](https://arxiv.org/abs/2110.02861) | `papers/training/01-training-offload-memory-systems/2021-2110.02861-8-bit-optimizers.md` |
| 8 | 0 | research | arXiv:2110.15032 | OneFlow: Redesign the Distributed Deep Learning Framework from Scratch | [primary](https://arxiv.org/abs/2110.15032) | `papers/inference/99-other-inference-systems/2021-2110.15032-oneflow-redesign-the-distributed-deep-learning-framework-from-scratch.md` |
| 9 | 0 | research | arXiv:2202.08906 | ST-MoE | [primary](https://arxiv.org/abs/2202.08906) | `papers/inference/99-other-inference-systems/2022-2202.08906-st-moe.md` |
| 10 | 0 | research | arXiv:2206.03382 | Tutel: Adaptive Mixture-of-Experts at Scale | [primary](https://arxiv.org/abs/2206.03382) | `papers/inference/99-other-inference-systems/2022-2206.03382-tutel-adaptive-mixture-of-experts-at-scale.md` |
| 11 | 0 | research | arXiv:2210.12924 | OLLA: Optimizing the Lifetime and Location of Arrays to Reduce the Memory Usage of Neural Networks | [primary](https://arxiv.org/abs/2210.12924) | `papers/inference/99-other-inference-systems/2022-2210.12924-olla-optimizing-the-lifetime-and-location-of-arrays-to-reduce-the-memory-usage-of-neural-networks.md` |
| 12 | 0 | research | arXiv:2302.08007 | With Shared Microexponents, A Little Shifting Goes a Long Way | [primary](https://arxiv.org/abs/2302.08007) | `papers/inference/99-other-inference-systems/2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md` |
| 13 | 0 | research | arXiv:2305.11860 | Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs | [primary](https://arxiv.org/abs/2305.11860) | `papers/inference/99-other-inference-systems/2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-and-coding-with-llms.md` |
| 14 | 0 | research | arXiv:2305.17888 | LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | [primary](https://arxiv.org/abs/2305.17888) | `papers/inference/99-other-inference-systems/2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md` |
| 15 | 0 | research | arXiv:2306.10209 | ZeRO++: Extremely Efficient Collective Communication for Giant Model Training | [primary](https://arxiv.org/abs/2306.10209) | `papers/inference/99-other-inference-systems/2023-2306.10209-zero-extremely-efficient-collective-communication-for-giant-model-training.md` |
| 16 | 0 | research | arXiv:2308.13137 | OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models | [primary](https://arxiv.org/abs/2308.13137) | `papers/inference/99-other-inference-systems/2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-models.md` |
| 17 | 0 | research | arXiv:2310.03003 | From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference | [primary](https://arxiv.org/abs/2310.03003) | `papers/inference/99-other-inference-systems/2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-model-inference.md` |
| 18 | 0 | research | arXiv:2310.06694 | Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning | [primary](https://arxiv.org/abs/2310.06694) | `papers/inference/99-other-inference-systems/2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pruning.md` |
| 19 | 0 | research | arXiv:2310.07096 | Sparse Universal Transformer | [primary](https://arxiv.org/abs/2310.07096) | `papers/inference/99-other-inference-systems/2023-2310.07096-sparse-universal-transformer.md` |
| 20 | 0 | research | arXiv:2310.09259 | QUIK: Towards End-to-end 4-Bit Inference on Generative Large Language Models | [primary](https://arxiv.org/abs/2310.09259) | `papers/inference/99-other-inference-systems/2023-2310.09259-quik-towards-end-to-end-4-bit-inference-on-generative-large-language-models.md` |
| 21 | 0 | research | arXiv:2311.01927 | GateLoop: Fully Data-Controlled Linear Recurrence for Sequence Modeling | [primary](https://arxiv.org/abs/2311.01927) | `papers/inference/99-other-inference-systems/2023-2311.01927-gateloop-fully-data-controlled-linear-recurrence-for-sequence-modeling.md` |
| 22 | 0 | research | arXiv:2312.12682 | Mini-GPTs: Efficient Large Language Models through Contextual Pruning | [primary](https://arxiv.org/abs/2312.12682) | `papers/inference/99-other-inference-systems/2023-2312.12682-mini-gpts-efficient-large-language-models-through-contextual-pruning.md` |
| 23 | 0 | research | arXiv:2401.00134 | Unicron: Economizing Self-Healing LLM Training at Scale | [primary](https://arxiv.org/abs/2401.00134) | `papers/inference/99-other-inference-systems/2024-2401.00134-unicron-economizing-self-healing-llm-training-at-scale.md` |
| 24 | 0 | research | arXiv:2401.06118 | Extreme Compression of Large Language Models via Additive Quantization | [primary](https://arxiv.org/abs/2401.06118) | `papers/inference/99-other-inference-systems/2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md` |
| 25 | 0 | research | arXiv:2401.10480 | Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning | [primary](https://arxiv.org/abs/2401.10480) | `papers/inference/99-other-inference-systems/2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reasoning.md` |
| 26 | 0 | research | arXiv:2402.02446 | LQER: Low-Rank Quantization Error Reconstruction for LLMs | [primary](https://arxiv.org/abs/2402.02446) | `papers/inference/99-other-inference-systems/2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md` |
| 27 | 0 | research | arXiv:2402.05109 | Hydra: Sequentially-Dependent Draft Heads for Medusa Decoding | [primary](https://arxiv.org/abs/2402.05109) | `papers/inference/99-other-inference-systems/2024-2402.05109-hydra-sequentially-dependent-draft-heads-for-medusa-decoding.md` |
| 28 | 0 | research | arXiv:2402.10517 | Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs | [primary](https://arxiv.org/abs/2402.10517) | `papers/inference/99-other-inference-systems/2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md` |
| 29 | 0 | research | arXiv:2402.11700 | Why Lift so Heavy? Slimming Large Language Models by Cutting Off the Layers | [primary](https://arxiv.org/abs/2402.11700) | `papers/inference/99-other-inference-systems/2024-2402.11700-why-lift-so-heavy-slimming-large-language-models-by-cutting-off-the-layers.md` |
| 30 | 0 | research | arXiv:2402.13720 | Ouroboros: Generating Longer Drafts Phrase by Phrase for Faster Speculative Decoding | [primary](https://arxiv.org/abs/2402.13720) | `papers/inference/99-other-inference-systems/2024-2402.13720-ouroboros-generating-longer-drafts-phrase-by-phrase-for-faster-speculative-decoding.md` |
| 31 | 0 | research | arXiv:2402.17463 | Training-Free Long-Context Scaling of Large Language Models | [primary](https://arxiv.org/abs/2402.17463) | `papers/inference/99-other-inference-systems/2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md` |
| 32 | 0 | research | arXiv:2402.18096 | No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization | [primary](https://arxiv.org/abs/2402.18096) | `papers/inference/99-other-inference-systems/2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-mixed-precision-quantization.md` |
| 33 | 0 | research | arXiv:2403.01241 | IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact | [primary](https://arxiv.org/abs/2403.01241) | `papers/inference/99-other-inference-systems/2024-2403.01241-intactkv-improving-large-language-model-quantization-by-keeping-pivot-tokens-intact.md` |
| 34 | 0 | research | arXiv:2403.05821 | Optimizing LLM Queries in Relational Data Analytics Workloads | [primary](https://arxiv.org/abs/2403.05821) | `papers/inference/99-other-inference-systems/2024-2403.05821-optimizing-llm-queries-in-relational-data-analytics-workloads.md` |
| 35 | 0 | research | arXiv:2403.09054 | Keyformer: KV Cache Reduction through Key Tokens Selection for Efficient Generative Inference | [primary](https://arxiv.org/abs/2403.09054) | `papers/inference/99-other-inference-systems/2024-2403.09054-keyformer-kv-cache-reduction-through-key-tokens-selection-for-efficient-generative-inference.md` |
| 36 | 0 | research | arXiv:2403.15388 | LLaVA-Prumerge: Adaptive Token Reduction for Efficient Large Multimodal Models | [primary](https://arxiv.org/abs/2403.15388) | `papers/inference/99-other-inference-systems/2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-models.md` |
| 37 | 0 | research | arXiv:2403.20306 | Towards Greener LLMs: Bringing Energy-Efficiency to the Forefront of LLM Inference | [primary](https://arxiv.org/abs/2403.20306) | `papers/inference/99-other-inference-systems/2024-2403.20306-towards-greener-llms-bringing-energy-efficiency-to-the-forefront-of-llm-inference.md` |
| 38 | 0 | research | arXiv:2404.02258 | Mixture-of-Depths: Dynamically allocating compute in transformer-based language models | [primary](https://arxiv.org/abs/2404.02258) | `papers/inference/02-adaptive-expert-computation-compression/2024-2404.02258-mixture-of-depths-dynamic-compute.md` |
| 39 | 0 | research | arXiv:2404.03865 | FFN-SkipLLM: A Hidden Gem for Autoregressive Decoding with Adaptive Feed Forward Skipping | [primary](https://arxiv.org/abs/2404.03865) | `papers/inference/99-other-inference-systems/2024-2404.03865-ffn-skipllm-a-hidden-gem-for-autoregressive-decoding-with-adaptive-feed-forward-skipping.md` |
| 40 | 0 | research | arXiv:2404.07904 | HGRN2: Gated Linear RNNs with State Expansion | [primary](https://arxiv.org/abs/2404.07904) | `papers/inference/99-other-inference-systems/2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md` |
| 41 | 0 | research | arXiv:2404.08856 | On Speculative Decoding for Multimodal Large Language Models | [primary](https://arxiv.org/abs/2404.08856) | `papers/inference/99-other-inference-systems/2024-2404.08856-on-speculative-decoding-for-multimodal-large-language-models.md` |
| 42 | 0 | research | arXiv:2404.14294 | A Survey on Efficient Inference for Large Language Models | [primary](https://arxiv.org/abs/2404.14294) | `papers/survey/03-inference-engines/2024-2404.14294-survey-efficient-inference-llms.md` |
| 43 | 0 | research | arXiv:2405.12532 | PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference | [primary](https://arxiv.org/abs/2405.12532) | `papers/inference/99-other-inference-systems/2024-2405.12532-pyramidinfer-pyramid-kv-cache-compression-for-high-throughput-llm-inference.md` |
| 44 | 0 | research | arXiv:2405.14366 | MiniCache: KV Cache Compression in Depth Dimension for Large Language Models | [primary](https://arxiv.org/abs/2405.14366) | `papers/inference/99-other-inference-systems/2024-2405.14366-minicache-kv-cache-compression-in-depth-dimension-for-large-language-models.md` |
| 45 | 0 | research | arXiv:2406.02500 | Towards Efficient Mixture of Experts: A Holistic Study of Compression Techniques | [primary](https://arxiv.org/abs/2406.02500) | `papers/inference/02-adaptive-expert-computation-compression/2024-2406.02500-towards-efficient-mixture-of-experts-holistic-compression.md` |
| 46 | 0 | research | arXiv:2406.14066 | TurboSpec: Closed-loop Speculation Control System for Optimizing LLM Serving Goodput | [primary](https://arxiv.org/abs/2406.14066) | `papers/inference/99-other-inference-systems/2024-2406.14066-turbospec-closed-loop-speculation-control-system-for-optimizing-llm-serving-goodput.md` |
| 47 | 0 | research | arXiv:2407.00945 | Efficient Expert Pruning for Sparse Mixture-of-Experts Language Models: Enhancing Performance and Reducing Inference Costs | [primary](https://arxiv.org/abs/2407.00945) | `papers/inference/02-adaptive-expert-computation-compression/2024-2407.00945-efficient-expert-pruning.md` |
| 48 | 0 | research | arXiv:2407.08454 | Model Tells You Where to Merge: Adaptive KV Cache Merging for LLMs on Long-Context Tasks | [primary](https://arxiv.org/abs/2407.08454) | `papers/inference/99-other-inference-systems/2024-2407.08454-model-tells-you-where-to-merge-adaptive-kv-cache-merging-for-llms-on-long-context-tasks.md` |
| 49 | 0 | research | arXiv:2408.01803 | STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs | [primary](https://arxiv.org/abs/2408.01803) | `papers/inference/99-other-inference-systems/2024-2408.01803-stbllm-breaking-the-1-bit-barrier-with-structured-binary-llms.md` |
| 50 | 0 | research | arXiv:2409.01141 | Duplex: A Device for Large Language Models with Mixture of Experts, Grouped Query Attention, and Continuous Batching | [primary](https://arxiv.org/abs/2409.01141) | `papers/inference/99-other-inference-systems/2024-2409.01141-duplex-a-device-for-large-language-models-with-mixture-of-experts-grouped-query-attention-and-continuous-batching.md` |
| 51 | 0 | research | arXiv:2409.10516 | RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval | [primary](https://arxiv.org/abs/2409.10516) | `papers/inference/10-kv-cache-offload-recomputation/2024-2409.10516-retrievalattention-vector-retrieval.md` |
| 52 | 0 | research | arXiv:2410.06916 | SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration | [primary](https://arxiv.org/abs/2410.06916) | `papers/inference/99-other-inference-systems/2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleration.md` |
| 53 | 0 | research | arXiv:2411.04975 | SuffixDecoding: A Model-Free Approach to Speeding Up Large Language Model Inference | [primary](https://arxiv.org/abs/2411.04975) | `papers/inference/99-other-inference-systems/2024-2411.04975-suffixdecoding-a-model-free-approach-to-speeding-up-large-language-model-inference.md` |
| 54 | 0 | research | arXiv:2412.04964 | Flash Communication: Reducing Tensor Parallelization Bottleneck for Fast Large Language Model Inference | [primary](https://arxiv.org/abs/2412.04964) | `papers/inference/99-other-inference-systems/2024-2412.04964-flash-communication-reducing-tensor-parallelization-bottleneck-for-fast-large-language-model-inference.md` |
| 55 | 0 | research | arXiv:2412.17246 | Fast and Live Model Auto Scaling with O(1) Host Caching | [primary](https://arxiv.org/abs/2412.17246) | `papers/inference/99-other-inference-systems/2024-2412.17246-fast-and-live-model-auto-scaling-with-o-1-host-caching.md` |
| 56 | 0 | research | arXiv:2502.04420 | KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference | [primary](https://arxiv.org/abs/2502.04420) | `papers/inference/99-other-inference-systems/2025-2502.04420-kvtuner-sensitivity-aware-layer-wise-mixed-precision-kv-cache-quantization-for-efficient-and-nearly-lossless-llm-inferen.md` |
| 57 | 0 | research | arXiv:2502.10517 | KernelBench: Can LLMs Write Efficient GPU Kernels? | [primary](https://arxiv.org/abs/2502.10517) | `papers/inference/99-other-inference-systems/2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md` |
| 58 | 0 | research | arXiv:2502.15734 | Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2502.15734) | `papers/inference/99-other-inference-systems/2025-2502.15734-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-generation.md` |
| 59 | 0 | research | arXiv:2503.00392 | Progressive Sparse Attention: Algorithm and System Co-design for Efficient Attention in LLM Serving | [primary](https://arxiv.org/abs/2503.00392) | `papers/inference/99-other-inference-systems/2025-2503.00392-progressive-sparse-attention-algorithm-and-system-co-design-for-efficient-attention-in-llm-serving.md` |
| 60 | 0 | research | arXiv:2503.05248 | Optimizing LLM Inference Throughput via Memory-aware and SLA-constrained Dynamic Batching | [primary](https://arxiv.org/abs/2503.05248) | `papers/inference/99-other-inference-systems/2025-2503.05248-optimizing-llm-inference-throughput-via-memory-aware-and-sla-constrained-dynamic-batching.md` |
| 61 | 0 | research | arXiv:2504.08378 | Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash | [primary](https://arxiv.org/abs/2504.08378) | `papers/inference/99-other-inference-systems/2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-flash.md` |
| 62 | 0 | research | arXiv:2504.15720 | SeaLLM: Service-Aware and Latency-Optimized Resource Sharing for Large Language Model Inference | [primary](https://arxiv.org/abs/2504.15720) | `papers/inference/99-other-inference-systems/2025-2504.15720-seallm-service-aware-and-latency-optimized-resource-sharing-for-large-language-model-inference.md` |
| 63 | 0 | research | arXiv:2505.13109 | FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference | [primary](https://arxiv.org/abs/2505.13109) | `papers/inference/99-other-inference-systems/2025-2505.13109-freekv-boosting-kv-cache-retrieval-for-efficient-llm-inference.md` |
| 64 | 0 | research | arXiv:2505.24133 | R-KV: Redundancy-aware KV Cache Compression for Reasoning Models | [primary](https://arxiv.org/abs/2505.24133) | `papers/inference/99-other-inference-systems/2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md` |
| 65 | 0 | research | arXiv:2506.07366 | MoE-GPS: Guidlines for Prediction Strategy for Dynamic Expert Duplication in MoE Load Balancing | [primary](https://www.semanticscholar.org/paper/b3d726f638aad791664917fc471740ff5c41eef9) | `papers/inference/99-other-inference-systems/2025-2506.07366-moe-gps-guidlines-for-prediction-strategy-for-dynamic-expert-duplication-in-moe-load-balancing.md` |
| 66 | 0 | research | arXiv:2506.20187 | Breaking the Boundaries of Long-Context LLM Inference: Adaptive KV Management on a Single Commodity GPU | [primary](https://arxiv.org/abs/2506.20187) | `papers/inference/99-other-inference-systems/2025-2506.20187-breaking-the-boundaries-of-long-context-llm-inference-adaptive-kv-management-on-a-single-commodity-gpu.md` |
| 67 | 0 | research | arXiv:2507.09019 | On Evaluating Performance of LLM Inference Systems | [primary](https://arxiv.org/abs/2507.09019) | `papers/inference/99-other-inference-systems/2025-2507.09019-on-evaluating-performance-of-llm-inference-systems.md` |
| 68 | 0 | research | arXiv:2507.19427 | Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding | [primary](https://arxiv.org/abs/2507.19427) | `papers/inference/99-other-inference-systems/2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective-decoding.md` |
| 69 | 0 | research | arXiv:2508.02520 | Huawei Cloud Model-as-a-Service on the CloudMatrix384 SuperPod | [primary](https://arxiv.org/abs/2508.02520) | `papers/inference/99-other-inference-systems/2025-2508.02520-huawei-cloud-model-as-a-service-on-the-cloudmatrix384-superpod.md` |
| 70 | 0 | research | arXiv:2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | [primary](https://arxiv.org/abs/2508.18265) | `papers/inference/99-other-inference-systems/2025-2508.18265-internvl3-5-advancing-open-source-multimodal-models-in-versatility-reasoning-and-efficiency.md` |
| 71 | 0 | research | arXiv:2509.09420 | HD-MoE: Hybrid and Dynamic Parallelism for Mixture-of-Expert LLMs with 3D Near-Memory Processing | [primary](https://arxiv.org/abs/2509.09420) | `papers/inference/99-other-inference-systems/2025-2509.09420-hd-moe-hybrid-and-dynamic-parallelism-for-mixture-of-expert-llms-with-3d-near-memory-processing.md` |
| 72 | 0 | research | arXiv:2509.17396 | EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments | [primary](https://arxiv.org/abs/2509.17396) | `papers/inference/99-other-inference-systems/2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-resource-constrained-environments.md` |
| 73 | 0 | research | arXiv:2510.00615 | ACON: Optimizing Context Compression for Long-horizon LLM Agents | [primary](https://arxiv.org/abs/2510.00615) | `papers/inference/99-other-inference-systems/2025-2510.00615-acon-optimizing-context-compression-for-long-horizon-llm-agents.md` |
| 74 | 0 | research | arXiv:2510.08731 | When to Reason: Semantic Router for vLLM | [primary](https://arxiv.org/abs/2510.08731) | `papers/inference/99-other-inference-systems/2025-2510.08731-when-to-reason-semantic-router-for-vllm.md` |
| 75 | 0 | research | arXiv:2510.13602 | NOSA: Native and Offloadable Sparse Attention | [primary](https://arxiv.org/abs/2510.13602) | `papers/inference/99-other-inference-systems/2025-2510.13602-nosa-native-and-offloadable-sparse-attention.md` |
| 76 | 0 | research | arXiv:2510.14973 | Attention Is All You Need for KV Cache in Diffusion LLMs | [primary](https://arxiv.org/abs/2510.14973) | `papers/inference/99-other-inference-systems/2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md` |
| 77 | 0 | research | arXiv:2510.20171 | Collective Communication for 100k+ GPUs | [primary](https://arxiv.org/abs/2510.20171) | `papers/inference/99-other-inference-systems/2025-2510.20171-collective-communication-for-100k-gpus.md` |
| 78 | 0 | research | arXiv:2511.04805 | PuzzleMoE: Efficient Compression of Large Mixture-of-Experts Models via Sparse Expert Merging and Bit-packed inference | [primary](https://arxiv.org/abs/2511.04805) | `papers/inference/02-adaptive-expert-computation-compression/2025-2511.04805-puzzlemoe-sparse-merging-bitpacked.md` |
| 79 | 0 | research | arXiv:2511.13676 | T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization | [primary](https://arxiv.org/abs/2511.13676) | `papers/inference/99-other-inference-systems/2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-place-simd-alu-reorganization.md` |
| 80 | 0 | research | arXiv:2511.20975 | Aragog: Just-in-Time Model Routing for Scalable Serving of Agentic Workflows | [primary](https://arxiv.org/abs/2511.20975) | `papers/inference/99-other-inference-systems/2025-2511.20975-aragog-just-in-time-model-routing-for-scalable-serving-of-agentic-workflows.md` |
| 81 | 0 | research | arXiv:2601.04719 | GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models | [primary](https://arxiv.org/abs/2601.04719) | `papers/inference/99-other-inference-systems/2026-2601.04719-gpu-accelerated-int8-quantization-for-kv-cache-compression-in-large-language-models.md` |
| 82 | 0 | research | arXiv:2601.07891 | KVzap: Fast, Adaptive, and Faithful KV Cache Pruning | [primary](https://arxiv.org/abs/2601.07891) | `papers/inference/99-other-inference-systems/2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md` |
| 83 | 0 | research | arXiv:2602.02579 | ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2602.02579) | `papers/inference/99-other-inference-systems/2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cache-reuse-in-retrieval-augmented-generation.md` |
| 84 | 0 | research | arXiv:2602.09721 | Revealing the Challenges of Attention-FFN Disaggregation for Modern MoE Models and Hardware Systems | [primary](https://arxiv.org/abs/2602.09721) | `papers/inference/99-other-inference-systems/2026-2602.09721-revealing-the-challenges-of-attention-ffn-disaggregation-for-modern-moe-models-and-hardware-systems.md` |
| 85 | 0 | research | arXiv:2602.13836 | Speculative Decoding with a Speculative Vocabulary | [primary](https://arxiv.org/abs/2602.13836) | `papers/inference/99-other-inference-systems/2026-2602.13836-speculative-decoding-with-a-speculative-vocabulary.md` |
| 86 | 0 | research | arXiv:2602.23200 | InnerQ: Hardware-aware Tuning-free Quantization of KV Cache for Large Language Models | [primary](https://arxiv.org/abs/2602.23200) | `papers/inference/99-other-inference-systems/2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-language-models.md` |
| 87 | 0 | research | arXiv:2603.04797 | Hardware-Software Co-design for 3D-DRAM-based LLM Serving Accelerator | [primary](https://arxiv.org/abs/2603.04797) | `papers/inference/99-other-inference-systems/2026-2603.04797-hardware-software-co-design-for-3d-dram-based-llm-serving-accelerator.md` |
| 88 | 0 | research | arXiv:2603.13605 | Orla: A Library for Serving LLM-Based Multi-Agent Systems | [primary](https://arxiv.org/abs/2603.13605) | `papers/inference/99-other-inference-systems/2026-2603.13605-orla-a-library-for-serving-llm-based-multi-agent-systems.md` |
| 89 | 0 | research | arXiv:2603.24517 | AVO: Agentic Variation Operators for Autonomous Evolutionary Search | [primary](https://arxiv.org/abs/2603.24517) | `papers/inference/99-other-inference-systems/2026-2603.24517-avo-agentic-variation-operators-for-autonomous-evolutionary-search.md` |
| 90 | 0 | research | arXiv:2604.07144 | Autopoiesis: A Self-Evolving System Paradigm for LLM Serving Under Runtime Dynamics | [primary](https://arxiv.org/abs/2604.07144) | `papers/inference/99-other-inference-systems/2026-2604.07144-autopoiesis-self-evolving-llm-serving-runtime-dynamics.md` |
| 91 | 0 | research | arXiv:2604.16400 | CoLLM: Continuous Adaptation for SLO-Aware LLM Serving on Shared GPU Clusters | [primary](https://arxiv.org/abs/2604.16400) | `papers/inference/99-other-inference-systems/2026-2604.16400-collm-continuous-adaptation-for-slo-aware-llm-serving-on-shared-gpu-clusters.md` |
| 92 | 0 | research | arXiv:2604.22312 | Guess-Verify-Refine: Data-Aware Top-K for Sparse-Attention Decoding on Blackwell via Temporal Correlation | [primary](https://arxiv.org/abs/2604.22312) | `papers/inference/99-other-inference-systems/2026-2604.22312-guess-verify-refine-data-aware-top-k-for-sparse-attention-decoding-on-blackwell-via-temporal-correlation.md` |
| 93 | 0 | research | arXiv:2605.06472 | Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management | [primary](https://arxiv.org/abs/2605.06472) | `papers/inference/99-other-inference-systems/2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-cache-management.md` |
| 94 | 0 | research | arXiv:2605.19775 | Understanding Inference Scaling for LLMS: Bottlenecks, Trade-Offs, and Performance Principles | [primary](https://www.semanticscholar.org/paper/930b5019707807053d41976f1cb09512a8dd9b18) | `papers/inference/99-other-inference-systems/2026-2605.19775-understanding-inference-scaling-for-llms-bottlenecks-trade-offs-and-performance-principles.md` |
| 95 | 0 | research | arXiv:2605.28207 | Pruning and Distilling Mixture-of-Experts into Dense Language Models | [primary](https://arxiv.org/abs/2605.28207) | `papers/inference/02-adaptive-expert-computation-compression/2026-2605.28207-prune-distill-moe-to-dense.md` |
| 96 | 0 | research | arXiv:2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | [primary](https://arxiv.org/abs/2606.01509) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.01509-probmoe-probabilistic-routing.md` |
| 97 | 0 | research | arXiv:2606.05538 | Less is MoE: Trimming Experts in Domain-Specialist Language Models | [primary](https://arxiv.org/abs/2606.05538) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.05538-less-is-moe-fisher-trimming.md` |
| 98 | 0 | research | arXiv:2606.13126 | MiniPIC: Flexible Position-Independent Caching in <100LOC | [primary](https://www.semanticscholar.org/paper/a8ad278ee75a875f56e632252c1b7c23b0033e32) | `papers/inference/99-other-inference-systems/2026-2606.13126-minipic-flexible-position-independent-caching-in-100loc.md` |
| 99 | 0 | research | arXiv:2606.19025 | FoMoE: Breaking the Full-Replica Barrier with a Federation of MoEs | [primary](https://arxiv.org/abs/2606.19025) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2606.19025-fomoe-federation-partial-expert-replication.md` |
| 100 | 0 | research | arXiv:2606.30560 | TraceLab: Characterizing Coding Agent Workloads for LLM Serving | [primary](https://www.semanticscholar.org/paper/5d3da10e6ce527c3f636d25137ce1f37004d22f9) | `papers/inference/99-other-inference-systems/2026-2606.30560-tracelab-characterizing-coding-agent-workloads-for-llm-serving.md` |
| 101 | 0 | research | arXiv:2607.08215 | On the Limitations of Non-GPU AI Accelerators for Large-Model Inference: A Field Study of MoE and Multimodal Serving on Huawei Ascend | [primary](https://arxiv.org/abs/2607.08215) | `papers/inference/99-other-inference-systems/2026-2607.08215-on-the-limitations-of-non-gpu-ai-accelerators-for-large-model-inference-a-field-study-of-moe-and-multimodal-serving-on-h.md` |
| 102 | 0 | research | arXiv:2607.16100 | Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives | [primary](https://arxiv.org/abs/2607.16100) | `papers/inference/99-other-inference-systems/2026-2607.16100-every-microsecond-matters-near-speed-of-light-gpu-collectives.md` |
| 103 | 0 | research | arXiv:2607.27269 | Beyond KV Reconstruction: Functional Reconstruction for MLA Draft Models in Speculative Decoding | [primary](https://www.semanticscholar.org/paper/0259a9d7148b5b97ddfed795956aaf13cf5da0b1) | `papers/inference/99-other-inference-systems/2026-2607.27269-beyond-kv-reconstruction-functional-reconstruction-for-mla-draft-models-in-speculative-decoding.md` |
| 104 | 0 | research | arXiv:2608.04991 | RAC: Reference-Aware Activation Compression for Communication-Efficient Split LLM Inference | [primary](https://arxiv.org/abs/2608.04991) | `papers/inference/08-edge-on-device-llm-systems/2026-2608.04991-rac-reference-aware-activation-compression.md` |
| 105 | 0 | research | arXiv:2608.09225 | Governing the KV Cache: Preventing Timing Side-Channel Leakage in Multi-Tenant LLM Inference | [primary](https://arxiv.org/abs/2608.09225) | `papers/inference/99-other-inference-systems/2026-2608.09225-governing-kv-cache-multitenant-isolation.md` |
| 106 | 0 | research | arXiv:2608.13966 | QUASAR: Lowering the Loss Floor of Quantization-Aware Training with Loss-Aware Reconstruction | [primary](https://arxiv.org/abs/2608.13966) | `papers/inference/99-other-inference-systems/2026-2608.13966-quasar-lowering-the-loss-floor-of-quantization-aware-training-with-loss-aware-reconstruction.md` |
| 107 | 0 | research | arXiv:2608.15299 | MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation | [primary](https://arxiv.org/abs/2608.15299) | `papers/inference/02-adaptive-expert-computation-compression/2026-2608.15299-maple-layer-wise-expert-allocation.md` |
| 108 | 0 | research | arXiv:2608.19659 | FleetSieve: Decision-Critical Profiling for SLO-Aware LLM Fleet Configuration | [primary](https://www.semanticscholar.org/paper/fa41fc861a398c7598a8884ab0b6ea4c5ab8306c) | `papers/inference/99-other-inference-systems/2026-2608.19659-fleetsieve-decision-critical-profiling-for-slo-aware-llm-fleet-configuration.md` |
| 109 | 0 | research | arXiv:2608.24063 | VisCache: Visual KV Cache Pruning for Efficient Vision Large Language Model Inference | [primary](https://www.semanticscholar.org/paper/2655c9d3521d8af9a51c602f9cb9bb3a33f74c31) | `papers/inference/99-other-inference-systems/2026-2608.24063-viscache-visual-kv-cache-pruning-for-efficient-vision-large-language-model-inference.md` |
| 110 | 0 | research | arXiv:2608.25431 | Here is a GIFT: Enforcing User Data Isolation in LLM Serving via GPU Information Flow Tracking | [primary](https://arxiv.org/abs/2608.25431) | `papers/inference/99-other-inference-systems/2026-2608.25431-here-is-a-gift-enforcing-user-data-isolation-in-llm-serving-via-gpu-information-flow-tracking.md` |
| 111 | 0 | research | arXiv:2608.29745 | JITterFlip: Uncovering Fault Attack Surfaces in JIT-Compiled LLM Serving | [primary](https://arxiv.org/abs/2608.29745) | `papers/inference/99-other-inference-systems/2026-2608.29745-jitterflip-jit-compiled-llm-serving-fault-surfaces.md` |
| 112 | 0 | research | arXiv:2609.03949 | VestigeKV: The NoPE-MLA KV Cache Carries Its Own Sparse-Attention Signal in a Vestigial Branch | [primary](https://arxiv.org/abs/2609.03949) | `papers/inference/99-other-inference-systems/2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-sparse-attention-signal-in-a-vestigial-branch.md` |
| 113 | 0 | research | arXiv:2609.06940 | Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management | [primary](https://www.semanticscholar.org/paper/4affda1dbe50475a3be782dcc62391802b20986e) | `papers/inference/99-other-inference-systems/2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-management.md` |
| 114 | 0 | research | arXiv:2609.08115 | Router Prior Bias: Preserving Base Routing Structure in MoE Post-Training | [primary](https://arxiv.org/abs/2609.08115) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2609.08115-router-prior-bias-soft-router-anchoring.md` |
| 115 | 0 | research | arXiv:2609.08663 | MoEMB: Scaling Universal Multimodal Embeddings with Efficient Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2609.08663) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.08663-moemb-adaptive-computation.md` |
| 116 | 0 | research | arXiv:2609.12075 | Efficient Vision-Language-Action Management and Serving for Robot Factories | [primary](https://www.semanticscholar.org/paper/f36477dbebdd9fcf27cc6f1155da649e6000f765) | `papers/inference/99-other-inference-systems/2026-2609.12075-efficient-vision-language-action-management-and-serving-for-robot-factories.md` |
| 117 | 0 | research | arXiv:2609.13682 | LayerRoute: Adaptive Layer-Skipping with LoRA-Preserved Quality for Efficient LLM Inference | [primary](https://arxiv.org/abs/2609.13682) | `papers/inference/99-other-inference-systems/2026-2609.13682-layerroute-adaptive-layer-skipping-with-lora-preserved-quality-for-efficient-llm-inference.md` |
| 118 | 0 | research | arXiv:2609.14864 | GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems | [primary](https://arxiv.org/abs/2609.14864) | `papers/inference/12-benchmarking-modeling-emulation/2026-2609.14864-gguf-metadata-llamacpp-throughput.md` |
| 119 | 0 | research | arXiv:2609.18526 | Running an LLM Locally Doesn't Keep Prompts Private: They Survive in Allocator Memory After Inference | [primary](https://arxiv.org/abs/2609.18526) | `papers/inference/99-other-inference-systems/2026-2609.18526-local-llm-prompts-survive-allocator-memory-after-inference.md` |
| 120 | 0 | research | arXiv:2609.21672 | Accelerating Dense LLMs via L0-regularized Mixture-of-Experts | [primary](https://www.semanticscholar.org/paper/6a5dbd9fa51ed94d2de8cafc0ca37a8e39ef73a0) | `papers/inference/99-other-inference-systems/2026-2609.21672-accelerating-dense-llms-via-l0-regularized-mixture-of-experts.md` |
| 121 | 0 | research | arXiv:2609.23585 | Global Ranks Survive, Selected Heads Shift: BOS-Sink Topology under 4-bit Weight-Only Quantization | [primary](https://www.semanticscholar.org/paper/f992275cced1c153a71a0ad630ebbff2f1ddefa1) | `papers/inference/99-other-inference-systems/2026-2609.23585-global-ranks-survive-selected-heads-shift-bos-sink-topology-under-4-bit-weight-only-quantization.md` |
| 122 | 0 | research | arXiv:2609.30854 | The KV Cache Is the New Memory Wall | [primary](https://arxiv.org/abs/2609.30854) | `papers/inference/99-other-inference-systems/2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md` |
| 123 | 0 | research | arXiv:2609.38090 | Mira: Memory-Efficient MoE Inference Using Adaptive Caching and Predictive Expert Staging | [primary](https://arxiv.org/abs/2609.38090) | `papers/inference/99-other-inference-systems/2026-2609.38090-mira-memory-efficient-moe-inference-using-adaptive-caching-and-predictive-expert-staging.md` |
| 124 | 0 | research | DOI:10.1016/j.neunet.2025.108274 | Expertfuse: A huffman tree-based gradual expert integration framework for MoE models | [primary](https://doi.org/10.1016/j.neunet.2025.108274) | `papers/inference/02-adaptive-expert-computation-compression/2025-expertfuse-huffman-gradual-expert-integration.md` |
| 125 | 0 | research | DOI:10.1109/2575-8411.2026.00035 | KV Cache Reuse for Elastic LLM Inference on Edge Devices | [primary](https://doi.org/10.1109/2575-8411.2026.00035) | `papers/inference/99-other-inference-systems/2020-2026.00035-kv-cache-reuse-for-elastic-llm-inference-on-edge-devices.md` |
| 126 | 0 | research | DOI:10.1109/icassp55912.2026.11465104 | Parsimony, Order and Balance: Principles for Compressing Mixture-of-Experts Models | [primary](https://doi.org/10.1109/icassp55912.2026.11465104) | `papers/inference/02-adaptive-expert-computation-compression/2026-parsimony-order-balance-moe-compression.md` |
| 127 | 0 | research | DOI:10.1109/ICWS72778.2026.00157 | Towards Efficient and Reliable On-Device Multi-Agent Systems: Challenges, Technologies and Explorations | [primary](https://www.semanticscholar.org/paper/6b7fe9189df482320578bffea03b382d9220ecda) | `papers/inference/99-other-inference-systems/2020-2026.00157-towards-efficient-and-reliable-on-device-multi-agent-systems-challenges-technologies-and-explorations.md` |
| 128 | 0 | research | DOI:10.1109/INFOCOM59046.2026.11571450 | Enabling Memory-Disaggregated Cloud Infrastructure for LLMs: An Adaptive CXL-based KV Cache Scheduling Approach | [primary](https://doi.org/10.1109/INFOCOM59046.2026.11571450) | `papers/inference/99-other-inference-systems/2026-95a006929f30-enabling-memory-disaggregated-cloud-infrastructure-for-llms-an-adaptive-cxl-based-kv-cache-scheduling-approach.md` |
| 129 | 0 | research | DOI:10.1109/ISCA66397.2026.00101 | STEP: Adaptive Spatio-Temporal Expert Prefetching for Low-Latency and Memory-Efficient MoE Inference | [primary](https://www.semanticscholar.org/paper/425c61cd261a06e425849f3f96364ce6a8ab8ed0) | `papers/inference/99-other-inference-systems/2020-2026.00101-step-adaptive-spatio-temporal-expert-prefetching-for-low-latency-and-memory-efficient-moe-inference.md` |
| 130 | 0 | research | DOI:10.1109/JIOT.2026.3718029 | Efficient LLM Coserving at the Edge via Resource-Aware Cooperative Scheduling | [primary](https://www.semanticscholar.org/paper/3f71f011292d4504aa0b754cb9854b3140cba51b) | `papers/inference/99-other-inference-systems/2026-d935ef5e0c55-efficient-llm-coserving-at-the-edge-via-resource-aware-cooperative-scheduling.md` |
| 131 | 0 | research | DOI:10.1109/LES.2025.3616900 | LPC: Efficient Lossless Parameter Compression for Deploying LLM Inference on Edge Systems | [primary](https://www.semanticscholar.org/paper/369189b30f08cc120594b39a7e352a38e5a72228) | `papers/inference/99-other-inference-systems/2026-43ece4bae0c5-lpc-efficient-lossless-parameter-compression-for-deploying-llm-inference-on-edge-systems.md` |
| 132 | 0 | research | DOI:10.1109/tkde.2025.3554028 | A Survey on Mixture of Experts in Large Language Models | [primary](https://doi.org/10.1109/TKDE.2025.3554028) | `papers/inference/99-other-inference-systems/2026-9d9dc7b7bf03-a-survey-on-mixture-of-experts-in-large-language-models.md` |
| 133 | 0 | research | DOI:10.1109/TON.2026.3704584 | Efficient Mixture-of-Experts Model Inference at the Edge via Adaptive Expert Merging | [primary](https://doi.org/10.1109/TON.2026.3704584) | `papers/inference/02-adaptive-expert-computation-compression/2026-adaptive-expert-merging-edge.md` |
| 134 | 0 | research | DOI:10.1145/3373376.3378530 | SwapAdvisor: Pushing Deep Learning Beyond the GPU Memory Limit via Smart Swapping | [primary](https://doi.org/10.1145/3373376.3378530) | `papers/inference/99-other-inference-systems/0000-4b209e34401e-swapadvisor-pushing-deep-learning-beyond-the-gpu-memory-limit-via-smart-swapping.md` |
| 135 | 0 | research | DOI:10.1145/3600006.3613157 | Mira: A Program-Behavior-Guided Far Memory System | [primary](https://doi.org/10.1145/3600006.3613157) | `papers/inference/99-other-inference-systems/2026-3a6cb9499537-mira-a-program-behavior-guided-far-memory-system.md` |
| 136 | 0 | research | DOI:10.1145/3620665.3640366 | PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation | [primary](https://doi.org/10.1145/3620665.3640366) | `papers/inference/99-other-inference-systems/2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transformation-and-graph-compilation.md` |
| 137 | 0 | research | DOI:10.1145/3642970.3655835 | Deferred Continuous Batching in Resource-Efficient Large Language Model Serving | [primary](https://doi.org/10.1145/3642970.3655835) | `papers/inference/99-other-inference-systems/2024-cd0254f5f44d-deferred-continuous-batching-in-resource-efficient-large-language-model-serving.md` |
| 138 | 0 | research | DOI:10.1145/3676641.3716009 | PAPI: Exploiting Dynamic Parallelism in Large Language Model Decoding with a Processing-In-Memory-Enabled Computing System | [primary](https://doi.org/10.1145/3676641.3716009) | `papers/inference/99-other-inference-systems/0000-71a3fb195e7b-papi-exploiting-dynamic-parallelism-in-large-language-model-decoding-with-a-processing-in-memory-enabled-computing-syste.md` |
| 139 | 0 | research | DOI:10.1145/3695053.3730999 | WindServe: Efficient Phase-Disaggregated LLM Serving with Stream-based Dynamic Scheduling | [primary](https://doi.org/10.1145/3695053.3730999) | `papers/inference/99-other-inference-systems/2025-8e0fd88d7ddc-windserve-efficient-phase-disaggregated-llm-serving-with-stream-based-dynamic-scheduling.md` |
| 140 | 0 | research | DOI:10.1145/3725843.3756078 | LLM.265: Video Codecs are Secretly Tensor Codecs | [primary](https://doi.org/10.1145/3725843.3756078) | `papers/inference/99-other-inference-systems/2025-5a2b2924d4e3-llm-265-video-codecs-are-secretly-tensor-codecs.md` |
| 141 | 0 | research | DOI:10.1145/3770855.3817626 | OrionInfer: Low-Overhead Parallelism Switching and Live Migration for Efficient LLM Serving | [primary](https://doi.org/10.1145/3770855.3817626) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-orioninfer-parallelism-switching-live-migration.md` |
| 142 | 0 | research | DOI:10.1145/3777466 | Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines | [primary](https://doi.org/10.1145/3777466) | `papers/inference/99-other-inference-systems/2025-704c3dbb57e7-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md` |
| 143 | 0 | research | DOI:10.1145/3789240.3822568 | Replacing NVMe Staging in LLM Inference with a High-Bandwidth CXL Memory Expander with an On-Device DMA Controller | [primary](https://www.semanticscholar.org/paper/7a2499fd38665d8205c513eb3740ddedc3675c5e) | `papers/inference/99-other-inference-systems/2026-34514b56228c-replacing-nvme-staging-in-llm-inference-with-a-high-bandwidth-cxl-memory-expander-with-an-on-device-dma-controller.md` |
| 144 | 0 | research | DOI:10.1145/3789240.3829201 | Balancing and Beyond: Communication-Centric Optimizations in Expert Parallelism | [primary](https://www.semanticscholar.org/paper/eac99489e90aa20cb13cb7d63f53c9014b797164) | `papers/inference/99-other-inference-systems/2026-0e42e21dd7f9-balancing-and-beyond-communication-centric-optimizations-in-expert-parallelism.md` |
| 145 | 0 | research | DOI:10.1145/3793230.3837769 | To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems | [primary](https://www.semanticscholar.org/paper/6db782df823d9da204a59180305aba81d47b3997) | `papers/inference/99-other-inference-systems/2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-serving-systems.md` |
| 146 | 0 | research | DOI:10.1145/3816440.3818527 | L2Mersit: A Scaling-Free Sub-8-bit Data Format for On-Device Reliable Large Language Model Serving | [primary](https://doi.org/10.1145/3816440.3818527) | `papers/inference/99-other-inference-systems/2026-3bf3ae07c250-l2mersit-a-scaling-free-sub-8-bit-data-format-for-on-device-reliable-large-language-model-serving.md` |
| 147 | 0 | research | DOI:10.1145/3832810.3832814 | SSQT: A Hardware-Friendly Fusion Compression Framework of Structured Sparsification and Sensitivity-Driven Quantization for Large-Scale Language Models | [primary](https://www.semanticscholar.org/paper/0b010b82f5fb03e74943d7486f9ea2da1edb828e) | `papers/inference/99-other-inference-systems/2026-153cd3135a6e-ssqt-a-hardware-friendly-fusion-compression-framework-of-structured-sparsification-and-sensitivity-driven-quantization-f.md` |
| 148 | 0 | research | DOI:10.1145/3832810.3832859 | CrossServe: Cross-Layer Scheduling for SLO Optimization in Multi-Tenant LLM Serving | [primary](https://www.semanticscholar.org/paper/43d9c475fecdcadc273a07d0d8ddd02d2c4e0aa4) | `papers/inference/99-other-inference-systems/2026-aacd4c06a02a-crossserve-cross-layer-scheduling-for-slo-optimization-in-multi-tenant-llm-serving.md` |
| 149 | 0 | research | DOI:10.1145/3832810.3832869 | CARE-MoE: Correlation-Aware Expert Placement and Semantic Equivalence Routing for MoE LLM Inference on Edge Devices | [primary](https://www.semanticscholar.org/paper/21fc6b1af66296c39fefd6e52e29d679963f6068) | `papers/inference/99-other-inference-systems/2026-9f0ddbf86051-care-moe-correlation-aware-expert-placement-and-semantic-equivalence-routing-for-moe-llm-inference-on-edge-devices.md` |
| 150 | 0 | research | DOI:10.13140/rg.2.2.28167.37282 | KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache | [primary](https://doi.org/10.13140/rg.2.2.28167.37282) | `papers/inference/99-other-inference-systems/0000-4a3b69939af0-kivi-a-tuning-free-asymmetric-2bit-quantization-for-kv-cache.md` |
| 151 | 0 | research | DOI:10.18653/v1/2026.findings-acl.1655 | LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation | [primary](https://aclanthology.org/2026.findings-acl.1655/) | `papers/inference/99-other-inference-systems/2026-df65c3a3c97c-logitspec-accelerating-retrieval-based-speculative-decoding-via-next-next-token-speculation.md` |
| 152 | 0 | research | DOI:10.52202/079017-0722 | SnapKV: LLM Knows What You are Looking for Before Generation | [primary](https://doi.org/10.52202/079017-0722) | `papers/inference/99-other-inference-systems/0000-838f46f28a47-snapkv-llm-knows-what-you-are-looking-for-before-generation.md` |
| 153 | 0 | research | OpenReview:EQgEMAD4kv | CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences | [primary](https://openreview.net/forum?id=EQgEMAD4kv) | `papers/inference/99-other-inference-systems/0000-e6d13afe4c72-cake-cascading-and-adaptive-kv-cache-eviction-with-layer-preferences.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **6875** / このworker向け: **500**

| # | score | identity | title | published | venue | citations | 関連数 | 系統候補 | source |
|---:|---:|---|---|---|---|---:|---:|---|---|
| 1 | 0 | arXiv:0811.3171 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/0811.3171) |
| 2 | 0 | arXiv:1109.3843 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1109.3843) |
| 3 | 0 | arXiv:1205.2618 |  |  |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 4 | 0 | arXiv:1211.0361 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1211.0361) |
| 5 | 0 | arXiv:1212.0402 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 6 | 0 | arXiv:1305.0445 |  |  |  |  | 2 | Conditional Computation, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1305.0445) |
| 7 | 0 | arXiv:1312.4461 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1312.4461) |
| 8 | 0 | arXiv:1402.3511 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1402.3511) |
| 9 | 0 | arXiv:1406.1078 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1406.1078) |
| 10 | 0 | arXiv:1409.3215 |  |  |  |  | 2 | MoE expert offloading / predictive prefetch and cache management, inference-systems | [source](https://arxiv.org/abs/1409.3215) |
| 11 | 0 | arXiv:1410.5401 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/1410.5401) |
| 12 | 0 | arXiv:1412.6550 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1412.6550) |
| 13 | 0 | arXiv:1502.05477 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1502.05477) |
| 14 | 0 | arXiv:1505.00387 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1505.00387) |
| 15 | 0 | arXiv:1506.02640 |  |  |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1506.02640) |
| 16 | 0 | arXiv:1507.05910 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1507.05910) |
| 17 | 0 | arXiv:1508.04025 |  |  |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 18 | 0 | arXiv:1511.05946 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1511.05946) |
| 19 | 0 | arXiv:1511.06530 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1511.06530) |
| 20 | 0 | arXiv:1511.07289 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1511.07289) |
| 21 | 0 | arXiv:1512.03385 |  |  |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1512.03385) |
| 22 | 0 | arXiv:1601.06759 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 23 | 0 | arXiv:1602.02410 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 24 | 0 | arXiv:1603.01025 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1603.01025) |
| 25 | 0 | arXiv:1603.05118 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1603.05118) |
| 26 | 0 | arXiv:1603.08983 |  |  |  |  | 5 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 27 | 0 | arXiv:1606.02858 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1606.02858) |
| 28 | 0 | arXiv:1607.03250 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1607.03250) |
| 29 | 0 | arXiv:1608.03665 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1608.03665) |
| 30 | 0 | arXiv:1609.05140 |  |  |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1609.05140) |
| 31 | 0 | arXiv:1611.00712 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 32 | 0 | arXiv:1611.01578 |  |  |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 33 | 0 | arXiv:1611.07409 |  |  |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1611.07409) |
| 34 | 0 | arXiv:1612.08083 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1612.08083) |
| 35 | 0 | arXiv:1702.02815 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1702.02815) |
| 36 | 0 | arXiv:1703.01365 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1703.01365) |
| 37 | 0 | arXiv:1703.05160 |  |  |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 38 | 0 | arXiv:1704.04497 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1704.04497) |
| 39 | 0 | arXiv:1704.05426 |  |  |  |  | 2 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 40 | 0 | arXiv:1705.04146 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1705.04146) |
| 41 | 0 | arXiv:1706.03471 |  |  |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 42 | 0 | arXiv:1708.04552 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 43 | 0 | arXiv:1709.02755 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 44 | 0 | arXiv:1710.09282 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/1710.09282) |
| 45 | 0 | arXiv:1711.03016 |  |  |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1711.03016) |
| 46 | 0 | arXiv:1712.01208 |  |  |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/1712.01208) |
| 47 | 0 | arXiv:1712.05382 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.05382) |
| 48 | 0 | arXiv:1801.10198 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1801.10198) |
| 49 | 0 | arXiv:1802.05751 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1802.05751) |
| 50 | 0 | arXiv:1802.08760 |  |  |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 51 | 0 | arXiv:1803.02155 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1803.02155) |
| 52 | 0 | arXiv:1803.08240 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1803.08240) |
| 53 | 0 | arXiv:1804.05058 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1804.05058) |
| 54 | 0 | arXiv:1804.08198 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1804.08198) |
| 55 | 0 | arXiv:1805.04833 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1805.04833) |
| 56 | 0 | arXiv:1805.08166 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1805.08166) |
| 57 | 0 | arXiv:1806.03822 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1806.03822) |
| 58 | 0 | arXiv:1806.10779 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1806.10779) |
| 59 | 0 | arXiv:1807.11205 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1807.11205) |
| 60 | 0 | arXiv:1808.08558 |  |  |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 61 | 0 | arXiv:1808.10583 |  |  |  |  | 1 | multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/1808.10583) |
| 62 | 0 | arXiv:1809.04281 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1809.04281) |
| 63 | 0 | arXiv:1809.10853 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1809.10853) |
| 64 | 0 | arXiv:1810.02340 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1810.02340) |
| 65 | 0 | arXiv:1810.05291 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.05291) |
| 66 | 0 | arXiv:1811.00414 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1811.00414) |
| 67 | 0 | arXiv:1811.01088 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1811.01088) |
| 68 | 0 | arXiv:1811.04909 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1811.04909) |
| 69 | 0 | arXiv:1812.01243 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1812.01243) |
| 70 | 0 | arXiv:1812.09764 |  |  |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1812.09764) |
| 71 | 0 | arXiv:1901.08544 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1901.08544) |
| 72 | 0 | arXiv:1902.00751 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.00751) |
| 73 | 0 | arXiv:1902.05613 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.05613) |
| 74 | 0 | arXiv:1902.09113 |  |  |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1902.09113) |
| 75 | 0 | arXiv:1902.10186 |  |  |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 76 | 0 | arXiv:1903.01699 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 77 | 0 | arXiv:1903.05662 |  |  |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, Weight Quantization / Compression | [source](https://arxiv.org/abs/1903.05662) |
| 78 | 0 | arXiv:1904.01038 |  |  |  |  | 4 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/1904.01038) |
| 79 | 0 | arXiv:1904.05862 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1904.05862) |
| 80 | 0 | arXiv:1904.09324 |  |  |  |  | 6 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1904.09324) |
| 81 | 0 | arXiv:1904.10631 |  |  |  |  | 1 | long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/1904.10631) |
| 82 | 0 | arXiv:1905.03439 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1905.03439) |
| 83 | 0 | arXiv:1905.07129 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 84 | 0 | arXiv:1905.10650 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1905.10650) |
| 85 | 0 | arXiv:1906.00091 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1906.00091) |
| 86 | 0 | arXiv:1906.01502 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1906.01502) |
| 87 | 0 | arXiv:1906.04165 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1906.04165) |
| 88 | 0 | arXiv:1906.04721 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1906.04721) |
| 89 | 0 | arXiv:1906.08172 |  |  |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1906.08172) |
| 90 | 0 | arXiv:1906.11024 |  |  |  |  | 3 | 99-other-inference-systems, inference-systems | [source](https://arxiv.org/abs/1906.11024) |
| 91 | 0 | arXiv:1907.02684 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1907.02684) |
| 92 | 0 | arXiv:1907.05686 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1907.05686) |
| 93 | 0 | arXiv:1907.12461 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1907.12461) |
| 94 | 0 | arXiv:1908.06605 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1908.06605) |
| 95 | 0 | arXiv:1908.08593 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1908.08593) |
| 96 | 0 | arXiv:1908.09791 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1908.09791) |
| 97 | 0 | arXiv:1908.11645 |  |  |  |  | 1 | LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計 | [source](https://arxiv.org/abs/1908.11645) |
| 98 | 0 | arXiv:1909.02480 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1909.02480) |
| 99 | 0 | arXiv:1909.05803 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1909.05803) |
| 100 | 0 | arXiv:1909.09577 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1909.09577) |
| 101 | 0 | arXiv:1909.12486 |  |  |  |  | 2 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1909.12486) |
| 102 | 0 | arXiv:1910.02610 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1910.02610) |
| 103 | 0 | arXiv:1910.05316 |  |  |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/1910.05316) |
| 104 | 0 | arXiv:1910.06611 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1910.06611) |
| 105 | 0 | arXiv:1910.09700 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1910.09700) |
| 106 | 0 | arXiv:1911.02116 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 107 | 0 | arXiv:1911.03014 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/1911.03014) |
| 108 | 0 | arXiv:1911.03829 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.03829) |
| 109 | 0 | arXiv:1911.04610 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1911.04610) |
| 110 | 0 | arXiv:1911.08731 |  |  |  |  | 1 | moe-quantization-compression | [source](https://arxiv.org/abs/1911.08731) |
| 111 | 0 | arXiv:1911.11641 |  |  |  |  | 10 | 16-weight-quantization-compression, Conditional Computation, adaptive-expert-computation-compression, kv-cache-memory, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-quantization-compression | [source](https://arxiv.org/abs/1911.11641) |
| 112 | 0 | arXiv:1912.08777 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1912.08777) |
| 113 | 0 | arXiv:2001.01072 |  |  |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/2001.01072) |
| 114 | 0 | arXiv:2001.04246 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2001.04246) |
| 115 | 0 | arXiv:2001.09977 |  |  |  |  | 6 | LLM Serving / Scheduling / Disaggregation, cross-layer LLM serving / SLO-aware scheduling / predictive routing / heterogeneous inference, inference-systems, serving-scheduling, speculative decoding / LLM serving / adaptive scheduling, その他システム研究 | [source](https://arxiv.org/abs/2001.09977) |
| 116 | 0 | arXiv:2002.07106 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.07106) |
| 117 | 0 | arXiv:2002.08155 |  |  |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2002.08155) |
| 118 | 0 | arXiv:2002.08909 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.08909) |
| 119 | 0 | arXiv:2002.10345 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.10345) |
| 120 | 0 | arXiv:2002.11054 |  |  |  |  | 4 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2002.11054) |
| 121 | 0 | arXiv:2003.02245 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2003.02245) |
| 122 | 0 | arXiv:2003.06713 |  |  |  |  | 1 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement | [source](https://arxiv.org/abs/2003.06713) |
| 123 | 0 | arXiv:2003.10555 |  |  |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2003.10555) |
| 124 | 0 | arXiv:2004.00026 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2004.00026) |
| 125 | 0 | arXiv:2004.04494 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2004.04494) |
| 126 | 0 | arXiv:2004.07320 |  |  |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2004.07320) |
| 127 | 0 | arXiv:2004.10964 |  |  |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2004.10964) |
| 128 | 0 | arXiv:2004.14560 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2004.14560) |
| 129 | 0 | arXiv:2005.00628 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 130 | 0 | arXiv:2005.03454 |  |  |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 131 | 0 | arXiv:2005.07647 |  |  |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2005.07647) |
| 132 | 0 | arXiv:2005.12872 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2005.12872) |
| 133 | 0 | arXiv:2006.02419 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2006.02419) |
| 134 | 0 | arXiv:2006.06762 |  |  |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2006.06762) |
| 135 | 0 | arXiv:2006.10901 |  |  |  |  | 2 | inference-systems, オフロード／階層メモリ | [source](https://arxiv.org/abs/2006.10901) |
| 136 | 0 | arXiv:2006.12467 |  |  |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 137 | 0 | arXiv:2007.01045 |  |  |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2007.01045) |
| 138 | 0 | arXiv:2007.04785 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2007.04785) |
| 139 | 0 | arXiv:2007.09818 |  |  |  |  | 1 | 06-moe-quantization-compression | [source](https://arxiv.org/abs/2007.09818) |
| 140 | 0 | arXiv:2008.00051 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 141 | 0 | arXiv:2008.02217 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2008.02217) |
| 142 | 0 | arXiv:2009.05257 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2009.05257) |
| 143 | 0 | arXiv:2009.06489 |  |  |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2009.06489) |
| 144 | 0 | arXiv:2009.07253 |  |  |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2009.07253) |
| 145 | 0 | arXiv:2009.08034 |  |  |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2009.08034) |
| 146 | 0 | arXiv:2009.09736 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2009.09736) |
| 147 | 0 | arXiv:2009.13239 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2009.13239) |
| 148 | 0 | arXiv:2010.02394 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 149 | 0 | arXiv:2010.02559 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2010.02559) |
| 150 | 0 | arXiv:2010.03633 |  |  |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2010.03633) |
| 151 | 0 | arXiv:2010.05315 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.05315) |
| 152 | 0 | arXiv:2010.07611 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2010.07611) |
| 153 | 0 | arXiv:2010.13002 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.13002) |
| 154 | 0 | arXiv:2010.16248 |  |  |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2010.16248) |
| 155 | 0 | arXiv:2011.02999 |  |  |  |  | 1 | 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://arxiv.org/abs/2011.02999) |
| 156 | 0 | arXiv:2011.05864 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2011.05864) |
| 157 | 0 | arXiv:2011.07831 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2011.07831) |
| 158 | 0 | arXiv:2012.07436 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2012.07436) |
| 159 | 0 | arXiv:2012.12624 |  |  |  |  | 2 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 160 | 0 | arXiv:2012.15701 |  |  |  |  | 6 | Conditional Computation, Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2012.15701) |
| 161 | 0 | arXiv:2101.00063 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2101.00063) |
| 162 | 0 | arXiv:2101.01321 |  |  |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2101.01321) |
| 163 | 0 | arXiv:2101.10277 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2101.10277) |
| 164 | 0 | arXiv:2102.02611 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2102.02611) |
| 165 | 0 | arXiv:2102.06621 |  |  |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2102.06621) |
| 166 | 0 | arXiv:2102.08124 |  |  |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2102.08124) |
| 167 | 0 | arXiv:2102.11174 |  |  |  |  | 1 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2102.11174) |
| 168 | 0 | arXiv:2102.12702 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2102.12702) |
| 169 | 0 | arXiv:2103.03404 |  |  |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2103.03404) |
| 170 | 0 | arXiv:2103.10360 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2103.10360) |
| 171 | 0 | arXiv:2103.17239 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2103.17239) |
| 172 | 0 | arXiv:2104.07012 |  |  |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 173 | 0 | arXiv:2104.07567 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2104.07567) |
| 174 | 0 | arXiv:2104.08771 |  |  |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2104.08771) |
| 175 | 0 | arXiv:2105.03036 |  |  |  |  | 2 | MoE inference / expert pruning / language-specific expert specialization, inference-systems | [source](https://arxiv.org/abs/2105.03036) |
| 176 | 0 | arXiv:2105.06990 |  |  |  |  | 3 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2105.06990) |
| 177 | 0 | arXiv:2105.09938 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2105.09938) |
| 178 | 0 | arXiv:2105.12002 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2105.12002) |
| 179 | 0 | arXiv:2105.14450 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2105.14450) |
| 180 | 0 | arXiv:2106.03594 |  |  |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2106.03594) |
| 181 | 0 | arXiv:2106.04489 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.04489) |
| 182 | 0 | arXiv:2106.05974 |  |  |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2106.05974) |
| 183 | 0 | arXiv:2106.07340 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2106.07340) |
| 184 | 0 | arXiv:2106.10595 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2106.10595) |
| 185 | 0 | arXiv:2107.00641 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.00641) |
| 186 | 0 | arXiv:2107.02561 |  |  |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2107.02561) |
| 187 | 0 | arXiv:2107.06419 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2107.06419) |
| 188 | 0 | arXiv:2107.10989 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2107.10989) |
| 189 | 0 | arXiv:2107.14203 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.14203) |
| 190 | 0 | arXiv:2108.06098 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2108.06098) |
| 191 | 0 | arXiv:2108.12659 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2108.12659) |
| 192 | 0 | arXiv:2109.02132 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2109.02132) |
| 193 | 0 | arXiv:2109.05093 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2109.05093) |
| 194 | 0 | arXiv:2109.08406 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2109.08406) |
| 195 | 0 | arXiv:2109.10686 |  |  |  |  | 1 | 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2109.10686) |
| 196 | 0 | arXiv:2109.11817 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2109.11817) |
| 197 | 0 | arXiv:2110.03252 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2110.03252) |
| 198 | 0 | arXiv:2110.06296 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2110.06296) |
| 199 | 0 | arXiv:2110.07577 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2110.07577) |
| 200 | 0 | arXiv:2110.08419 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2110.08419) |
| 201 | 0 | arXiv:2110.10305 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.10305) |
| 202 | 0 | arXiv:2110.14883 |  |  |  |  | 2 | inference-systems, training-memory-systems | [source](https://arxiv.org/abs/2110.14883) |
| 203 | 0 | arXiv:2111.00364 |  |  |  |  | 1 | hardware-accelerators | [source](https://arxiv.org/abs/2111.00364) |
| 204 | 0 | arXiv:2111.01338 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2111.01338) |
| 205 | 0 | arXiv:2111.08566 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2111.08566) |
| 206 | 0 | arXiv:2111.12293 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2111.12293) |
| 207 | 0 | arXiv:2112.01488 |  |  |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2112.01488) |
| 208 | 0 | arXiv:2112.02958 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2112.02958) |
| 209 | 0 | arXiv:2112.06749 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2112.06749) |
| 210 | 0 | arXiv:2112.08608 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.08608) |
| 211 | 0 | arXiv:2112.11037 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.11037) |
| 212 | 0 | arXiv:2112.14397 |  |  |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 213 | 0 | arXiv:2201.05767 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2201.05767) |
| 214 | 0 | arXiv:2201.10520 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2201.10520) |
| 215 | 0 | arXiv:2201.13425 |  |  |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2201.13425) |
| 216 | 0 | arXiv:2202.04200 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2202.04200) |
| 217 | 0 | arXiv:2202.05747 |  |  |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2202.05747) |
| 218 | 0 | arXiv:2202.07800 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2202.07800) |
| 219 | 0 | arXiv:2202.08904 |  |  |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2202.08904) |
| 220 | 0 | arXiv:2202.13914 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.13914) |
| 221 | 0 | arXiv:2203.01670 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.01670) |
| 222 | 0 | arXiv:2203.03466 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2203.03466) |
| 223 | 0 | arXiv:2203.06390 |  |  |  |  | 3 | Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.06390) |
| 224 | 0 | arXiv:2203.07814 |  |  |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2203.07814) |
| 225 | 0 | arXiv:2203.09509 |  |  |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.09509) |
| 226 | 0 | arXiv:2203.13240 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2203.13240) |
| 227 | 0 | arXiv:2204.00408 |  |  |  |  | 3 |  | [source](https://arxiv.org/abs/2204.00408) |
| 228 | 0 | arXiv:2204.03178 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2204.03178) |
| 229 | 0 | arXiv:2204.05832 |  |  |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2204.05832) |
| 230 | 0 | arXiv:2204.06683 |  |  |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 231 | 0 | arXiv:2204.07705 |  |  |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2204.07705) |
| 232 | 0 | arXiv:2204.11574 |  |  |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2204.11574) |
| 233 | 0 | arXiv:2205.01848 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 234 | 0 | arXiv:2205.04934 |  |  |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2205.04934) |
| 235 | 0 | arXiv:2205.06126 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2205.06126) |
| 236 | 0 | arXiv:2205.10364 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10364) |
| 237 | 0 | arXiv:2205.11380 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2205.11380) |
| 238 | 0 | arXiv:2205.11916 |  |  |  |  | 2 | Offload / Hierarchical Memory, inference-systems | [source](https://arxiv.org/abs/2205.11916) |
| 239 | 0 | arXiv:2205.12674 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.12674) |
| 240 | 0 | arXiv:2205.13792 |  |  |  |  | 1 | 推論中のKVQ再計算をストレージ読出しへ置換し、階層キャッシュと遅延制約付きスケジューラを組み合わせるLLM推論省エネルギー化。 | [source](https://arxiv.org/abs/2205.13792) |
| 241 | 0 | arXiv:2206.02845 |  |  |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection, inference-systems | [source](https://arxiv.org/abs/2206.02845) |
| 242 | 0 | arXiv:2206.08896 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2206.08896) |
| 243 | 0 | arXiv:2206.13329 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2206.13329) |
| 244 | 0 | arXiv:2207.05221 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2207.05221) |
| 245 | 0 | arXiv:2207.07061 |  |  |  |  | 5 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2207.07061) |
| 246 | 0 | arXiv:2207.11154 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2207.11154) |
| 247 | 0 | arXiv:2208.02813 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 248 | 0 | arXiv:2208.04202 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2208.04202) |
| 249 | 0 | arXiv:2208.06064 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2208.06064) |
| 250 | 0 | arXiv:2208.09225 |  |  |  |  | 2 | 投機的デコード・バッチ推論 | [source](https://arxiv.org/abs/2208.09225) |
| 251 | 0 | arXiv:2208.11174 |  |  |  |  | 1 | 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://arxiv.org/abs/2208.11174) |
| 252 | 0 | arXiv:2209.03143 |  |  |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 253 | 0 | arXiv:2209.07858 |  |  |  |  | 1 | Mixture-of-Experts inference / processing-in-memory / heterogeneous scheduling / expert placement | [source](https://arxiv.org/abs/2209.07858) |
| 254 | 0 | arXiv:2209.10655 |  |  |  |  | 1 | training-memory-systems | [source](https://arxiv.org/abs/2209.10655) |
| 255 | 0 | arXiv:2209.12356 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2209.12356) |
| 256 | 0 | arXiv:2209.14756 |  |  |  |  | 1 | KV-cache memory management / random-access-constrained accelerators | [source](https://arxiv.org/abs/2209.14756) |
| 257 | 0 | arXiv:2209.15352 |  |  |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 258 | 0 | arXiv:2210.02406 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.02406) |
| 259 | 0 | arXiv:2210.03044 |  |  |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2210.03044) |
| 260 | 0 | arXiv:2210.03350 |  |  |  |  | 2 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, inference-systems | [source](https://arxiv.org/abs/2210.03350) |
| 261 | 0 | arXiv:2210.05709 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2210.05709) |
| 262 | 0 | arXiv:2210.07183 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.07183) |
| 263 | 0 | arXiv:2210.08006 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.08006) |
| 264 | 0 | arXiv:2210.09461 |  |  |  |  | 4 | inference-systems, on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2210.09461) |
| 265 | 0 | arXiv:2210.11610 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.11610) |
| 266 | 0 | arXiv:2210.12353 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.12353) |
| 267 | 0 | arXiv:2210.14215 |  |  |  |  | 1 | training-memory-systems | [source](https://arxiv.org/abs/2210.14215) |
| 268 | 0 | arXiv:2210.17223 |  |  |  |  | 1 | moe-inference-expert-offloading | [source](https://arxiv.org/abs/2210.17223) |
| 269 | 0 | arXiv:2211.00635 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.00635) |
| 270 | 0 | arXiv:2211.05109 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.05109) |
| 271 | 0 | arXiv:2211.05953 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2211.05953) |
| 272 | 0 | arXiv:2211.07828 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2211.07828) |
| 273 | 0 | arXiv:2211.09699 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 274 | 0 | arXiv:2211.12485 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.12485) |
| 275 | 0 | arXiv:2211.15533 |  |  |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2211.15533) |
| 276 | 0 | arXiv:2212.01349 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2212.01349) |
| 277 | 0 | arXiv:2212.03613 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2212.03613) |
| 278 | 0 | arXiv:2212.04092 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2212.04092) |
| 279 | 0 | arXiv:2212.05339 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2212.05339) |
| 280 | 0 | arXiv:2212.08136 |  |  |  |  | 3 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.08136) |
| 281 | 0 | arXiv:2212.10325 |  |  |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2212.10325) |
| 282 | 0 | arXiv:2212.10509 |  |  |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 283 | 0 | arXiv:2212.10554 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2212.10554) |
| 284 | 0 | arXiv:2212.10947 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2212.10947) |
| 285 | 0 | arXiv:2212.14024 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2212.14024) |
| 286 | 0 | arXiv:2301.02111 |  |  |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.02111) |
| 287 | 0 | arXiv:2301.04104 |  |  |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.04104) |
| 288 | 0 | arXiv:2301.05843 |  |  |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2301.05843) |
| 289 | 0 | arXiv:2301.08658 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.08658) |
| 290 | 0 | arXiv:2301.10226 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.10226) |
| 291 | 0 | arXiv:2301.12017 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2301.12017) |
| 292 | 0 | arXiv:2301.12503 |  |  |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2301.12503) |
| 293 | 0 | arXiv:2301.13823 |  |  |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2301.13823) |
| 294 | 0 | arXiv:2302.02599 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.02599) |
| 295 | 0 | arXiv:2302.04062 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2302.04062) |
| 296 | 0 | arXiv:2302.05442 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.05442) |
| 297 | 0 | arXiv:2302.06784 |  |  |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2302.06784) |
| 298 | 0 | arXiv:2302.09019 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.09019) |
| 299 | 0 | arXiv:2302.09632 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.09632) |
| 300 | 0 | arXiv:2302.10866 |  |  |  |  | 5 | Conditional Computation, inference-systems, training-memory-systems | [source](https://arxiv.org/abs/2302.10866) |
| 301 | 0 | arXiv:2302.11750 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2302.11750) |
| 302 | 0 | arXiv:2302.12170 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2302.12170) |
| 303 | 0 | arXiv:2302.13214 |  |  |  |  | 3 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2302.13214) |
| 304 | 0 | arXiv:2302.14827 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.14827) |
| 305 | 0 | arXiv:2303.00980 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.00980) |
| 306 | 0 | arXiv:2303.03428 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.03428) |
| 307 | 0 | arXiv:2303.04226 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.04226) |
| 308 | 0 | arXiv:2303.06153 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2303.06153) |
| 309 | 0 | arXiv:2303.07129 |  |  |  |  | 2 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 310 | 0 | arXiv:2303.10130 |  |  |  |  | 2 | MoE inference / on-device LLM / expert offloading / expert caching, inference-systems | [source](https://arxiv.org/abs/2303.10130) |
| 311 | 0 | arXiv:2303.10733 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.10733) |
| 312 | 0 | arXiv:2303.12345 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.12345) |
| 313 | 0 | arXiv:2303.13375 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.13375) |
| 314 | 0 | arXiv:2303.15375 |  |  |  |  | 1 | cpu-offload | [source](https://arxiv.org/abs/2303.15375) |
| 315 | 0 | arXiv:2303.16634 |  |  |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2303.16634) |
| 316 | 0 | arXiv:2303.17568 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.17568) |
| 317 | 0 | arXiv:2303.17951 |  |  |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2303.17951) |
| 318 | 0 | arXiv:2304.01238 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2304.01238) |
| 319 | 0 | arXiv:2304.02015 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.02015) |
| 320 | 0 | arXiv:2304.03094 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2304.03094) |
| 321 | 0 | arXiv:2304.03589 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2304.03589) |
| 322 | 0 | arXiv:2304.04556 |  |  |  |  | 1 | KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://arxiv.org/abs/2304.04556) |
| 323 | 0 | arXiv:2304.05970 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.05970) |
| 324 | 0 | arXiv:2304.09145 |  |  |  |  | 11 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Weight Quantization / Compression, inference-systems, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 325 | 0 | arXiv:2304.12110 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.12110) |
| 326 | 0 | arXiv:2304.14317 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.14317) |
| 327 | 0 | arXiv:2305.01181 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.01181) |
| 328 | 0 | arXiv:2305.03726 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.03726) |
| 329 | 0 | arXiv:2305.06300 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.06300) |
| 330 | 0 | arXiv:2305.07622 |  |  |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 331 | 0 | arXiv:2305.08852 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.08852) |
| 332 | 0 | arXiv:2305.10435 |  |  |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2305.10435) |
| 333 | 0 | arXiv:2305.12356 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.12356) |
| 334 | 0 | arXiv:2305.13450 |  |  |  |  | 1 | dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2305.13450) |
| 335 | 0 | arXiv:2305.14045 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.14045) |
| 336 | 0 | arXiv:2305.14325 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.14325) |
| 337 | 0 | arXiv:2305.14516 |  |  |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://arxiv.org/abs/2305.14516) |
| 338 | 0 | arXiv:2305.14771 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.14771) |
| 339 | 0 | arXiv:2305.14952 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2305.14952) |
| 340 | 0 | arXiv:2305.15066 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2305.15066) |
| 341 | 0 | arXiv:2305.15717 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.15717) |
| 342 | 0 | arXiv:2305.16264 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.16264) |
| 343 | 0 | arXiv:2305.16938 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.16938) |
| 344 | 0 | arXiv:2305.17444 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.17444) |
| 345 | 0 | arXiv:2305.18354 |  |  |  |  | 1 | 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2305.18354) |
| 346 | 0 | arXiv:2305.18691 |  |  |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.18691) |
| 347 | 0 | arXiv:2305.19420 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.19420) |
| 348 | 0 | arXiv:2305.20069 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.20069) |
| 349 | 0 | arXiv:2306.00802 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.00802) |
| 350 | 0 | arXiv:2306.02224 |  |  |  |  | 2 | Expert Prefetch, inference-systems | [source](https://arxiv.org/abs/2306.02224) |
| 351 | 0 | arXiv:2306.02707 |  |  |  |  | 3 | llm-serving-scheduling-disaggregation, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2306.02707) |
| 352 | 0 | arXiv:2306.03310 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.03310) |
| 353 | 0 | arXiv:2306.04509 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2306.04509) |
| 354 | 0 | arXiv:2306.05179 |  |  |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2306.05179) |
| 355 | 0 | arXiv:2306.06000 |  |  |  |  | 6 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, SLO-aware LLM serving / chunked prefill / multi-resource scheduling, SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2306.06000) |
| 356 | 0 | arXiv:2306.08162 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2306.08162) |
| 357 | 0 | arXiv:2306.09782 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.09782) |
| 358 | 0 | arXiv:2306.11227 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.11227) |
| 359 | 0 | arXiv:2306.13549 |  |  |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 360 | 0 | arXiv:2306.16636 |  |  |  |  | 1 | sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2306.16636) |
| 361 | 0 | arXiv:2307.00067 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2307.00067) |
| 362 | 0 | arXiv:2307.01952 |  |  |  |  | 3 | Diffusion LLM Inference, LLM Serving / Scheduling / Disaggregation, MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2307.01952) |
| 363 | 0 | arXiv:2307.02666 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2307.02666) |
| 364 | 0 | arXiv:2307.03393 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.03393) |
| 365 | 0 | arXiv:2307.04964 |  |  |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2307.04964) |
| 366 | 0 | arXiv:2307.06908 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.06908) |
| 367 | 0 | arXiv:2307.07443 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.07443) |
| 368 | 0 | arXiv:2307.08072 |  |  |  |  | 3 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 369 | 0 | arXiv:2307.08352 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.08352) |
| 370 | 0 | arXiv:2307.10169 |  |  |  |  | 3 |  | [source](https://arxiv.org/abs/2307.10169) |
| 371 | 0 | arXiv:2307.10802 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2307.10802) |
| 372 | 0 | arXiv:2307.12375 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.12375) |
| 373 | 0 | arXiv:2307.13692 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.13692) |
| 374 | 0 | arXiv:2307.15190 |  |  |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2307.15190) |
| 375 | 0 | arXiv:2308.00692 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.00692) |
| 376 | 0 | arXiv:2308.02565 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.02565) |
| 377 | 0 | arXiv:2308.04371 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.04371) |
| 378 | 0 | arXiv:2308.07037 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.07037) |
| 379 | 0 | arXiv:2308.07134 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.07134) |
| 380 | 0 | arXiv:2308.07921 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2308.07921) |
| 381 | 0 | arXiv:2308.09313 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.09313) |
| 382 | 0 | arXiv:2308.09723 |  |  |  |  | 3 | KV Cache Optimization / Compression, Quantization × MoE × Offload, kv-cache-memory | [source](https://arxiv.org/abs/2308.09723) |
| 383 | 0 | arXiv:2308.11596 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2308.11596) |
| 384 | 0 | arXiv:2308.12966 |  |  |  |  | 9 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, inference-systems, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 385 | 0 | arXiv:2308.14363 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2308.14363) |
| 386 | 0 | arXiv:2308.15272 |  |  |  |  | 1 | on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2308.15272) |
| 387 | 0 | arXiv:2309.01885 |  |  |  |  | 4 | 16-weight-quantization-compression, LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.01885) |
| 388 | 0 | arXiv:2309.05463 |  |  |  |  | 7 | Weight Quantization / Compression, inference-systems, survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 389 | 0 | arXiv:2309.05858 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.05858) |
| 390 | 0 | arXiv:2309.06687 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.06687) |
| 391 | 0 | arXiv:2309.08715 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.08715) |
| 392 | 0 | arXiv:2309.09558 |  |  |  |  | 2 | offload-hierarchical-memory, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://arxiv.org/abs/2309.09558) |
| 393 | 0 | arXiv:2309.10691 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 394 | 0 | arXiv:2309.12252 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.12252) |
| 395 | 0 | arXiv:2309.13879 |  |  |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, other-inference-systems | [source](https://arxiv.org/abs/2309.13879) |
| 396 | 0 | arXiv:2309.14592 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.14592) |
| 397 | 0 | arXiv:2309.17012 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.17012) |
| 398 | 0 | arXiv:2310.00280 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.00280) |
| 399 | 0 | arXiv:2310.00811 |  |  |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2310.00811) |
| 400 | 0 | arXiv:2310.01469 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.01469) |
| 401 | 0 | arXiv:2310.01812 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.01812) |
| 402 | 0 | arXiv:2310.03094 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.03094) |
| 403 | 0 | arXiv:2310.03716 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.03716) |
| 404 | 0 | arXiv:2310.04361 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2310.04361) |
| 405 | 0 | arXiv:2310.05418 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.05418) |
| 406 | 0 | arXiv:2310.05916 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.05916) |
| 407 | 0 | arXiv:2310.06117 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.06117) |
| 408 | 0 | arXiv:2310.07521 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.07521) |
| 409 | 0 | arXiv:2310.08041 |  |  |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2310.08041) |
| 410 | 0 | arXiv:2310.10046 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.10046) |
| 411 | 0 | arXiv:2310.11960 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.11960) |
| 412 | 0 | arXiv:2310.12931 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.12931) |
| 413 | 0 | arXiv:2310.14189 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.14189) |
| 414 | 0 | arXiv:2310.16355 |  |  |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2310.16355) |
| 415 | 0 | arXiv:2310.18813 |  |  |  |  | 8 | Speculative Decoding, inference-systems, speculative-decoding, survey-speculative-decoding, 投機的デコード・バッチ推論, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2310.18813) |
| 416 | 0 | arXiv:2310.20329 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.20329) |
| 417 | 0 | arXiv:2311.01544 |  |  |  |  | 1 | 06-moe-quantization-compression | [source](https://arxiv.org/abs/2311.01544) |
| 418 | 0 | arXiv:2311.03658 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.03658) |
| 419 | 0 | arXiv:2311.04902 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2311.04902) |
| 420 | 0 | arXiv:2311.05997 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.05997) |
| 421 | 0 | arXiv:2311.07989 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2311.07989) |
| 422 | 0 | arXiv:2311.08692 |  |  |  |  | 1 | speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2311.08692) |
| 423 | 0 | arXiv:2311.08993 |  |  |  |  | 1 | KV Cache Compression / Long Context | [source](https://arxiv.org/abs/2311.08993) |
| 424 | 0 | arXiv:2311.10122 |  |  |  |  | 4 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference, inference-systems | [source](https://arxiv.org/abs/2311.10122) |
| 425 | 0 | arXiv:2311.11586 |  |  |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2311.11586) |
| 426 | 0 | arXiv:2311.12793 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2311.12793) |
| 427 | 0 | arXiv:2311.13581 |  |  |  |  | 9 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2311.13581) |
| 428 | 0 | arXiv:2311.15180 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.15180) |
| 429 | 0 | arXiv:2311.17043 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2311.17043) |
| 430 | 0 | arXiv:2311.17842 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.17842) |
| 431 | 0 | arXiv:2312.02406 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.02406) |
| 432 | 0 | arXiv:2312.03209 |  |  |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.03209) |
| 433 | 0 | arXiv:2312.03815 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.03815) |
| 434 | 0 | arXiv:2312.04916 |  |  |  |  | 4 | early-exit-offloading-self-speculative-decoding, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 435 | 0 | arXiv:2312.05215 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2312.05215) |
| 436 | 0 | arXiv:2312.06662 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.06662) |
| 437 | 0 | arXiv:2312.07987 |  |  |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 438 | 0 | arXiv:2312.08901 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.08901) |
| 439 | 0 | arXiv:2312.11819 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11819) |
| 440 | 0 | arXiv:2312.13558 |  |  |  |  | 3 | LLM inference surveys、roofline performance analysis, inference-systems, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 441 | 0 | arXiv:2312.15123 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.15123) |
| 442 | 0 | arXiv:2312.17244 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2312.17244) |
| 443 | 0 | arXiv:2401.00448 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.00448) |
| 444 | 0 | arXiv:2401.01313 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.01313) |
| 445 | 0 | arXiv:2401.02643 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.02643) |
| 446 | 0 | arXiv:2401.04081 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.04081) |
| 447 | 0 | arXiv:2401.04881 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.04881) |
| 448 | 0 | arXiv:2401.07793 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.07793) |
| 449 | 0 | arXiv:2401.08406 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.08406) |
| 450 | 0 | arXiv:2401.12224 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.12224) |
| 451 | 0 | arXiv:2401.13601 |  |  |  |  | 3 | LLM inference surveys、roofline performance analysis, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2401.13601) |
| 452 | 0 | arXiv:2401.14021 |  |  |  |  | 4 | KV Cache Optimization / Compression, inference-systems, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2401.14021) |
| 453 | 0 | arXiv:2401.14732 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.14732) |
| 454 | 0 | arXiv:2401.16160 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.16160) |
| 455 | 0 | arXiv:2402.00025 |  |  |  |  | 2 | GPU疎行列カーネル／二重疎LLM推論／SIMTマイクロアーキテクチャ, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.00025) |
| 456 | 0 | arXiv:2402.01032 |  |  |  |  | 3 | sparse attention / KV-cache bandwidth reduction | [source](https://arxiv.org/abs/2402.01032) |
| 457 | 0 | arXiv:2402.01353 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.01353) |
| 458 | 0 | arXiv:2402.02244 |  |  |  |  | 5 | KV Cache Compression / Long Context, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 459 | 0 | arXiv:2402.03216 |  |  |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 460 | 0 | arXiv:2402.03666 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.03666) |
| 461 | 0 | arXiv:2402.04401 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.04401) |
| 462 | 0 | arXiv:2402.05935 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.05935) |
| 463 | 0 | arXiv:2402.07456 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.07456) |
| 464 | 0 | arXiv:2402.08132 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.08132) |
| 465 | 0 | arXiv:2402.09025 |  |  |  |  | 3 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 466 | 0 | arXiv:2402.10193 |  |  |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2402.10193) |
| 467 | 0 | arXiv:2402.11573 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.11573) |
| 468 | 0 | arXiv:2402.12038 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2402.12038) |
| 469 | 0 | arXiv:2402.12851 |  |  |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 470 | 0 | arXiv:2402.13499 |  |  |  |  | 3 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2402.13499) |
| 471 | 0 | arXiv:2402.14261 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.14261) |
| 472 | 0 | arXiv:2402.14830 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2402.14830) |
| 473 | 0 | arXiv:2402.15607 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.15607) |
| 474 | 0 | arXiv:2402.16714 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.16714) |
| 475 | 0 | arXiv:2402.16827 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.16827) |
| 476 | 0 | arXiv:2402.17193 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.17193) |
| 477 | 0 | arXiv:2402.18013 |  |  |  |  | 6 | inference-systems, llm-serving-scheduling-disaggregation, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2402.18013) |
| 478 | 0 | arXiv:2402.18381 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.18381) |
| 479 | 0 | arXiv:2402.18700 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.18700) |
| 480 | 0 | arXiv:2403.00858 |  |  |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2403.00858) |
| 481 | 0 | arXiv:2403.01590 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.01590) |
| 482 | 0 | arXiv:2403.02545 |  |  |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2403.02545) |
| 483 | 0 | arXiv:2403.03432 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2403.03432) |
| 484 | 0 | arXiv:2403.03699 |  |  |  |  | 1 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://arxiv.org/abs/2403.03699) |
| 485 | 0 | arXiv:2403.04945 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.04945) |
| 486 | 0 | arXiv:2403.05525 |  |  |  |  | 3 | Quantization × MoE × Offload, inference-systems, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 487 | 0 | arXiv:2403.06764 |  |  |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.06764) |
| 488 | 0 | arXiv:2403.08312 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.08312) |
| 489 | 0 | arXiv:2403.09032 |  |  |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 490 | 0 | arXiv:2403.10131 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.10131) |
| 491 | 0 | arXiv:2403.10616 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.10616) |
| 492 | 0 | arXiv:2403.12313 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2403.12313) |
| 493 | 0 | arXiv:2403.12958 |  |  |  |  | 1 | 10-kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2403.12958) |
| 494 | 0 | arXiv:2403.14734 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.14734) |
| 495 | 0 | arXiv:2403.17887 |  |  |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2403.17887) |
| 496 | 0 | arXiv:2403.19776 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2403.19776) |
| 497 | 0 | arXiv:2404.01230 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2404.01230) |
| 498 | 0 | arXiv:2404.02183 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2404.02183) |
| 499 | 0 | arXiv:2404.04475 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2404.04475) |
| 500 | 0 | arXiv:2404.06910 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2404.06910) |

## Machine-readable

同じ割当は [worker-worklist-00.json](worker-worklist-00.json) にあります。

