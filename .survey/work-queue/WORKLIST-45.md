# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-02T07:03:25+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **534** / 未claim総数: **387** / このworker向け: **129**

| # | 種別 | identity | title | source | 想定配置先 |
|---:|---|---|---|---|---|
| 1 | research | DOI:10.1145/3832810.3832869 | CARE-MoE: Correlation-Aware Expert Placement and Semantic Equivalence Routing for MoE LLM Inference on Edge Devices | [primary](https://www.semanticscholar.org/paper/21fc6b1af66296c39fefd6e52e29d679963f6068) | `papers/inference/99-other-inference-systems/2026-9f0ddbf86051-care-moe-correlation-aware-expert-placement-and-semantic-equivalence-routing-for-moe-llm-inference-on-edge-devices.md` |
| 2 | research | DOI:10.1109/ICC59461.2026.11587970 | InKubeator: Pre-warming In-Memory KV Caches from Disk for Elastic LLM Serving | [primary](https://doi.org/10.1109/ICC59461.2026.11587970) | `papers/inference/99-other-inference-systems/2026-805ee7ad7ae4-inkubeator-pre-warming-in-memory-kv-caches-from-disk-for-elastic-llm-serving.md` |
| 3 | research | DOI:10.1145/3832810.3832859 | CrossServe: Cross-Layer Scheduling for SLO Optimization in Multi-Tenant LLM Serving | [primary](https://www.semanticscholar.org/paper/43d9c475fecdcadc273a07d0d8ddd02d2c4e0aa4) | `papers/inference/99-other-inference-systems/2026-aacd4c06a02a-crossserve-cross-layer-scheduling-for-slo-optimization-in-multi-tenant-llm-serving.md` |
| 4 | research | DOI:10.1145/3832810.3832827 | ReliefServe: Relieving GPU Pressure in Multi-Model Serving via Selective CPU Escape | [primary](https://www.semanticscholar.org/paper/30f2fe44afe7a63e4a4e20c8f5083c129e09ae80) | `papers/inference/99-other-inference-systems/2026-ef0cbb7f0917-reliefserve-relieving-gpu-pressure-in-multi-model-serving-via-selective-cpu-escape.md` |
| 5 | research | arXiv:2511.04805 | PuzzleMoE: Efficient Compression of Large Mixture-of-Experts Models via Sparse Expert Merging and Bit-packed inference | [primary](https://arxiv.org/abs/2511.04805) | `papers/inference/02-adaptive-expert-computation-compression/2025-2511.04805-puzzlemoe-sparse-merging-bitpacked.md` |
| 6 | research | arXiv:2405.14297 | Dynamic Mixture of Experts: An Auto-Tuning Approach for Efficient Transformer Models | [primary](https://arxiv.org/abs/2405.14297) | `papers/inference/02-adaptive-expert-computation-compression/2024-2405.14297-dynmoe-auto-tuning.md` |
| 7 | research | DOI:10.24963/ijcai.2026/657 | DoMoE: Domain-Aware Semantic Expert Prediction for Efficient MoE Inference Under Expert Offloading | [primary](https://doi.org/10.24963/ijcai.2026/657) | `papers/inference/03-expert-prefetch/2026-domoe-domain-aware-semantic-expert-prediction.md` |
| 8 | research | DOI:10.1109/ISCA66397.2026.00101 | STEP: Adaptive Spatio-Temporal Expert Prefetching for Low-Latency and Memory-Efficient MoE Inference | [primary](https://www.semanticscholar.org/paper/425c61cd261a06e425849f3f96364ce6a8ab8ed0) | `papers/inference/99-other-inference-systems/2020-2026.00101-step-adaptive-spatio-temporal-expert-prefetching-for-low-latency-and-memory-efficient-moe-inference.md` |
| 9 | research | arXiv:2609.15810 | VC-Attention: Value Smoothing and Softmax Casting for Low-bit Attention | [primary](https://www.semanticscholar.org/paper/d26fb643c9c194cb4d34bd660b031a61d5f72f5d) | `papers/inference/99-other-inference-systems/2026-2609.15810-vc-attention-value-smoothing-and-softmax-casting-for-low-bit-attention.md` |
| 10 | research | arXiv:2606.13126 | MiniPIC: Flexible Position-Independent Caching in <100LOC | [primary](https://www.semanticscholar.org/paper/a8ad278ee75a875f56e632252c1b7c23b0033e32) | `papers/inference/99-other-inference-systems/2026-2606.13126-minipic-flexible-position-independent-caching-in-100loc.md` |
| 11 | research | DOI:10.1145/3832810.3832814 | SSQT: A Hardware-Friendly Fusion Compression Framework of Structured Sparsification and Sensitivity-Driven Quantization for Large-Scale Language Models | [primary](https://www.semanticscholar.org/paper/0b010b82f5fb03e74943d7486f9ea2da1edb828e) | `papers/inference/99-other-inference-systems/2026-153cd3135a6e-ssqt-a-hardware-friendly-fusion-compression-framework-of-structured-sparsification-and-sensitivity-driven-quantization-f.md` |
| 12 | research | arXiv:2608.07890 | Router Sensitivity Under Lightweight Fine-Tuning Identifies Prunable Experts in Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2608.07890) | `papers/inference/02-adaptive-expert-computation-compression/2026-2608.07890-router-sensitivity-prunable-experts.md` |
| 13 | research | arXiv:2606.15716 | How to Score Experts for One-Shot MoE Expert Pruning: A Unified Formulation and Selection Principle | [primary](https://arxiv.org/abs/2606.15716) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.15716-one-shot-expert-pruning-scoring.md` |
| 14 | research | arXiv:2508.18376 | DualSparse-MoE: Coordinating Tensor/Neuron-Level Sparsity with Expert Partition and Reconstruction | [primary](https://arxiv.org/abs/2508.18376) | `papers/inference/02-adaptive-expert-computation-compression/2025-2508.18376-dualsparse-moe.md` |
| 15 | research | DOI:10.1109/TON.2026.3704584 | Efficient Mixture-of-Experts Model Inference at the Edge via Adaptive Expert Merging | [primary](https://doi.org/10.1109/TON.2026.3704584) | `papers/inference/02-adaptive-expert-computation-compression/2026-adaptive-expert-merging-edge.md` |
| 16 | research | arXiv:2609.03949 | VestigeKV: The NoPE-MLA KV Cache Carries Its Own Sparse-Attention Signal in a Vestigial Branch | [primary](https://arxiv.org/abs/2609.03949) | `papers/inference/99-other-inference-systems/2026-2609.03949-vestigekv-the-nope-mla-kv-cache-carries-its-own-sparse-attention-signal-in-a-vestigial-branch.md` |
| 17 | research | DOI:10.21203/rs.3.rs-10952127/v1 | Reasoning-Aware Error-Bounded KV-Cache Compression and Sparse Attention for Long-Context LLMs | [primary](https://doi.org/10.21203/rs.3.rs-10952127/v1) | `papers/inference/99-other-inference-systems/2026-0ef8e5385098-reasoning-aware-error-bounded-kv-cache-compression-and-sparse-attention-for-long-context-llms.md` |
| 18 | research | arXiv:2607.28069 | SemPIC: Learning Semantic Position-Independent KV Caches | [primary](https://www.semanticscholar.org/paper/f48d751da47d9a84046858a1ef820b02aa7775b1) | `papers/inference/99-other-inference-systems/2026-2607.28069-sempic-learning-semantic-position-independent-kv-caches.md` |
| 19 | research | DOI:10.1109/INFOCOM59046.2026.11571717 | SemCache: Semantic-Aware Cache Sharing for Efficient Multi-User LoRA-Adapted LLM Inference at the Edge | [primary](https://doi.org/10.1109/INFOCOM59046.2026.11571717) | `papers/inference/99-other-inference-systems/2026-7056d9defe0d-semcache-semantic-aware-cache-sharing-for-efficient-multi-user-lora-adapted-llm-inference-at-the-edge.md` |
| 20 | research | arXiv:2606.05538 | Less is MoE: Trimming Experts in Domain-Specialist Language Models | [primary](https://arxiv.org/abs/2606.05538) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.05538-less-is-moe-fisher-trimming.md` |
| 21 | research | arXiv:2505.17639 | PreMoE: Proactive Inference for Efficient Mixture-of-Experts | [primary](https://arxiv.org/abs/2505.17639) | `papers/inference/02-adaptive-expert-computation-compression/2025-2505.17639-premoe-proactive-sparse-specialists.md` |
| 22 | research | arXiv:2609.12075 | Efficient Vision-Language-Action Management and Serving for Robot Factories | [primary](https://www.semanticscholar.org/paper/f36477dbebdd9fcf27cc6f1155da649e6000f765) | `papers/inference/99-other-inference-systems/2026-2609.12075-efficient-vision-language-action-management-and-serving-for-robot-factories.md` |
| 23 | research | arXiv:2608.19659 | FleetSieve: Decision-Critical Profiling for SLO-Aware LLM Fleet Configuration | [primary](https://www.semanticscholar.org/paper/fa41fc861a398c7598a8884ab0b6ea4c5ab8306c) | `papers/inference/99-other-inference-systems/2026-2608.19659-fleetsieve-decision-critical-profiling-for-slo-aware-llm-fleet-configuration.md` |
| 24 | research | arXiv:2606.19025 | FoMoE: Breaking the Full-Replica Barrier with a Federation of MoEs | [primary](https://arxiv.org/abs/2606.19025) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2606.19025-fomoe-federation-partial-expert-replication.md` |
| 25 | research | DOI:10.1109/TPDS.2026.3729988 | FairCache: Demystifying Cache-Induced Unfairness in Multi-Tenant Large Language Model Serving | [primary](https://www.semanticscholar.org/paper/69e16a381bb1a483fb9a5e494bc895ad74bb412a) | `papers/inference/99-other-inference-systems/2026-e490b2439d3f-faircache-demystifying-cache-induced-unfairness-in-multi-tenant-large-language-model-serving.md` |
| 26 | research | DOI:10.1109/icassp55912.2026.11465104 | Parsimony, Order and Balance: Principles for Compressing Mixture-of-Experts Models | [primary](https://doi.org/10.1109/icassp55912.2026.11465104) | `papers/inference/02-adaptive-expert-computation-compression/2026-parsimony-order-balance-moe-compression.md` |
| 27 | research | arXiv:2609.07786 | Signed Rescue Routing: Harm-Aware Cascades for Efficient LLM Inference | [primary](https://arxiv.org/abs/2609.07786) | `papers/inference/99-other-inference-systems/2026-2609.07786-signed-rescue-routing-harm-aware-cascades-for-efficient-llm-inference.md` |
| 28 | research | arXiv:2609.13846 | Affinity-Aware Sharding for Delayed Tensor Parallelism | [primary](https://arxiv.org/abs/2609.13846) | `papers/inference/99-other-inference-systems/2026-2609.13846-affinity-aware-sharding-for-delayed-tensor-parallelism.md` |
| 29 | research | arXiv:2110.02861 | 8-bit Optimizers via Block-wise Quantization | [primary](https://arxiv.org/abs/2110.02861) | `papers/training/01-training-offload-memory-systems/2021-2110.02861-8-bit-optimizers.md` |
| 30 | research | arXiv:1909.08053 | Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | [primary](https://arxiv.org/abs/1909.08053) | `papers/training/03-pipeline-parallel-modular-training/2019-1909.08053-megatron-lm.md` |
| 31 | research | DOI:10.1109/NVMSA71223.2026.11658877 | Poster: SAF: Semantic-Aware Flushing for Latency and Jitter Suppression in Continuous VLA Inference on Edge Devices | [primary](https://doi.org/10.1109/NVMSA71223.2026.11658877) | `papers/inference/10-kv-cache-offload-recomputation/2026-saf-semantic-aware-flushing-kv-nvme-edge.md` |
| 32 | research | arXiv:2607.17181 | Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs | [primary](https://www.semanticscholar.org/paper/e7106b6132090e3a5d8f669d7e94ba890e42b781) | `papers/inference/99-other-inference-systems/2026-2607.17181-talaria-session-aware-serverless-serving-of-hundred-billion-parameter-llms.md` |
| 33 | research | arXiv:2405.13019 | A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models | [primary](https://arxiv.org/abs/2405.13019) | `papers/survey/05-accelerated-generation/2024-2405.13019-accelerated-generation-survey.md` |
| 34 | research | DOI:10.1016/j.parco.2026.103216 | SmartBatchLLM: An efficient adaptive hybrid batching strategy for large language model serving | [primary](https://doi.org/10.1016/j.parco.2026.103216) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-smartbatchllm-adaptive-hybrid-batching.md` |
| 35 | research | arXiv:2607.27269 | Beyond KV Reconstruction: Functional Reconstruction for MLA Draft Models in Speculative Decoding | [primary](https://www.semanticscholar.org/paper/0259a9d7148b5b97ddfed795956aaf13cf5da0b1) | `papers/inference/99-other-inference-systems/2026-2607.27269-beyond-kv-reconstruction-functional-reconstruction-for-mla-draft-models-in-speculative-decoding.md` |
| 36 | research | arXiv:2404.14294 | A Survey on Efficient Inference for Large Language Models | [primary](https://arxiv.org/abs/2404.14294) | `papers/survey/03-inference-engines/2024-2404.14294-survey-efficient-inference-llms.md` |
| 37 | research | arXiv:2409.02060 | OLMoE: Open Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2409.02060) | `papers/inference/99-other-inference-systems/2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md` |
| 38 | research | arXiv:2608.21952 | SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality | [primary](https://arxiv.org/abs/2608.21952) | `papers/inference/99-other-inference-systems/2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md` |
| 39 | research | arXiv:2608.13966 | QUASAR: Lowering the Loss Floor of Quantization-Aware Training with Loss-Aware Reconstruction | [primary](https://arxiv.org/abs/2608.13966) | `papers/inference/99-other-inference-systems/2026-2608.13966-quasar-lowering-the-loss-floor-of-quantization-aware-training-with-loss-aware-reconstruction.md` |
| 40 | research | DOI:10.1109/LCA.2026.3660969 | H3: Hybrid Architecture Using High Bandwidth Memory and High Bandwidth Flash for Cost-Efficient LLM Inference | [primary](https://doi.org/10.1109/LCA.2026.3660969) | `papers/inference/99-other-inference-systems/2026-27b000808907-h3-hybrid-architecture-using-high-bandwidth-memory-and-high-bandwidth-flash-for-cost-efficient-llm-inference.md` |
| 41 | research | DOI:10.1145/3789240.3822569 | Memory as a First‑Class Resource in AI‑Factory Simulation | [primary](https://www.semanticscholar.org/paper/ab6071dcfef2e4a7092fdb5866e5a34485b28d51) | `papers/inference/99-other-inference-systems/2026-739d27a164e4-memory-as-a-firstclass-resource-in-aifactory-simulation.md` |
| 42 | research | DOI:10.1109/JCC72984.2026.00058 | UNAS: Urgency- and Fairness-Aware Scheduling for SLO-Oriented LLM Serving | [primary](https://doi.org/10.1109/JCC72984.2026.00058) | `papers/inference/99-other-inference-systems/2020-2026.00058-unas-urgency-and-fairness-aware-scheduling-for-slo-oriented-llm-serving.md` |
| 43 | research | arXiv:2306.11695 | A Simple and Effective Pruning Approach for Large Language Models | [primary](https://arxiv.org/abs/2306.11695) | `papers/inference/99-other-inference-systems/2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md` |
| 44 | research | arXiv:2608.28444 | Sliding-window beats linear attention | [primary](https://www.semanticscholar.org/paper/633f43137abd58fdd39606b868b27eccafae8625) | `papers/inference/99-other-inference-systems/2026-2608.28444-sliding-window-beats-linear-attention.md` |
| 45 | research | arXiv:2608.15118 | Collective Communication for Distributed LLM Systems: Planning, Runtime Adaptation, and Computation Coordination | [primary](https://arxiv.org/abs/2608.15118) | `papers/inference/99-other-inference-systems/2026-2608.15118-collective-communication-for-distributed-llm-systems-planning-runtime-adaptation-and-computation-coordination.md` |
| 46 | research | arXiv:2609.00363 | Deterministic LLM Inference Across GPU Kernels: Power-of-Two INT8 Quantization Scales and the Limits of Tolerance-Based Conformance | [primary](https://arxiv.org/abs/2609.00363) | `papers/inference/99-other-inference-systems/2026-2609.00363-deterministic-llm-inference-gpu-kernels-int8.md` |
| 47 | research | arXiv:2507.19427 | Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding | [primary](https://arxiv.org/abs/2507.19427) | `papers/inference/99-other-inference-systems/2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective-decoding.md` |
| 48 | research | DOI:10.1109/TNET.2024.3355010 | DistMind: Efficient Resource Disaggregation for Deep Learning Workloads | [primary](https://www.semanticscholar.org/paper/1112ac74f9299838c8a354f778fbbfd951dfc50c) | `papers/inference/99-other-inference-systems/2026-d66009615d04-distmind-efficient-resource-disaggregation-for-deep-learning-workloads.md` |
| 49 | research | arXiv:2605.06472 | Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management | [primary](https://arxiv.org/abs/2605.06472) | `papers/inference/99-other-inference-systems/2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-cache-management.md` |
| 50 | research | DOI:10.1109/ICWS72778.2026.00157 | Towards Efficient and Reliable On-Device Multi-Agent Systems: Challenges, Technologies and Explorations | [primary](https://www.semanticscholar.org/paper/6b7fe9189df482320578bffea03b382d9220ecda) | `papers/inference/99-other-inference-systems/2020-2026.00157-towards-efficient-and-reliable-on-device-multi-agent-systems-challenges-technologies-and-explorations.md` |
| 51 | research | arXiv:2604.07144 | Autopoiesis: A Self-Evolving System Paradigm for LLM Serving Under Runtime Dynamics | [primary](https://arxiv.org/abs/2604.07144) | `papers/inference/99-other-inference-systems/2026-2604.07144-autopoiesis-self-evolving-llm-serving-runtime-dynamics.md` |
| 52 | research | DOI:10.1109/CCGrid68966.2026.00014 | Quicktopia: Iteration-Level GPU Frequency Control for Energy–Latency Co-Optimization in LLM Inference | [primary](https://www.semanticscholar.org/paper/88a222b2340b8906e15edd5efd58293b25fc38ce) | `papers/inference/99-other-inference-systems/2020-2026.00014-quicktopia-iteration-level-gpu-frequency-control-for-energylatency-co-optimization-in-llm-inference.md` |
| 53 | research | arXiv:2603.04797 | Hardware-Software Co-design for 3D-DRAM-based LLM Serving Accelerator | [primary](https://arxiv.org/abs/2603.04797) | `papers/inference/99-other-inference-systems/2026-2603.04797-hardware-software-co-design-for-3d-dram-based-llm-serving-accelerator.md` |
| 54 | research | arXiv:2406.02500 | Towards Efficient Mixture of Experts: A Holistic Study of Compression Techniques | [primary](https://arxiv.org/abs/2406.02500) | `papers/inference/02-adaptive-expert-computation-compression/2024-2406.02500-towards-efficient-mixture-of-experts-holistic-compression.md` |
| 55 | research | arXiv:2409.10516 | RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval | [primary](https://arxiv.org/abs/2409.10516) | `papers/inference/10-kv-cache-offload-recomputation/2024-2409.10516-retrievalattention-vector-retrieval.md` |
| 56 | research | arXiv:2502.10517 | KernelBench: Can LLMs Write Efficient GPU Kernels? | [primary](https://arxiv.org/abs/2502.10517) | `papers/inference/99-other-inference-systems/2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md` |
| 57 | research | arXiv:2311.01282 | FlashDecoding++: Faster Large Language Model Inference on GPUs | [primary](https://arxiv.org/abs/2311.01282) | `papers/inference/99-other-inference-systems/2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md` |
| 58 | research | arXiv:2301.00774 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | [primary](https://www.semanticscholar.org/paper/909ad57ce8caa6b390a65ae09db352d27d8f3996) | `papers/inference/99-other-inference-systems/2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md` |
| 59 | research | DOI:10.1145/3805621.3807651 | Hardware-Aware Co-Design of Multi-Chip LLM Serving via Performance Modeling | [primary](https://doi.org/10.1145/3805621.3807651) | `papers/inference/99-other-inference-systems/2026-dae506ee161c-hardware-aware-co-design-of-multi-chip-llm-serving-via-performance-modeling.md` |
| 60 | research | arXiv:2510.16040 | Kelle: Co-design KV Caching and eDRAM for Efficient LLM Serving in Edge Computing | [primary](https://arxiv.org/abs/2510.16040) | `papers/inference/06-kv-cache-memory/2025-2510.16040-kelle-kv-cache-edram-edge-serving.md` |
| 61 | audit | arXiv:2504.03775 | FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling | [primary](https://arxiv.org/abs/2504.03775) | `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.03775-flowkv-low-latency-transfer-load-aware.md` |
| 62 | research | arXiv:2608.09225 | Governing the KV Cache: Preventing Timing Side-Channel Leakage in Multi-Tenant LLM Inference | [primary](https://arxiv.org/abs/2608.09225) | `papers/inference/99-other-inference-systems/2026-2608.09225-governing-kv-cache-multitenant-isolation.md` |
| 63 | research | arXiv:2510.14392 | FairBatching: Fairness-Aware Batch Formation for LLM Inference | [primary](https://arxiv.org/abs/2510.14392) | `papers/inference/99-other-inference-systems/2025-2510.14392-fairbatching-fairness-aware-batch-formation-for-llm-inference.md` |
| 64 | research | arXiv:2608.05926 | BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge | [primary](https://arxiv.org/abs/2608.05926) | `papers/inference/08-edge-on-device-llm-systems/2026-2608.05926-balance-hybrid-autoregressive-speculative-edge.md` |
| 65 | research | DOI:10.1109/tkde.2025.3554028 | A Survey on Mixture of Experts in Large Language Models | [primary](https://doi.org/10.1109/TKDE.2025.3554028) | `papers/inference/99-other-inference-systems/2026-9d9dc7b7bf03-a-survey-on-mixture-of-experts-in-large-language-models.md` |
| 66 | research | arXiv:2608.29745 | JITterFlip: Uncovering Fault Attack Surfaces in JIT-Compiled LLM Serving | [primary](https://arxiv.org/abs/2608.29745) | `papers/inference/99-other-inference-systems/2026-2608.29745-jitterflip-jit-compiled-llm-serving-fault-surfaces.md` |
| 67 | research | arXiv:2404.14527 | Mélange: Cost Efficient Large Language Model Serving by Exploiting GPU Heterogeneity | [primary](https://arxiv.org/abs/2404.14527) | `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2404.14527-melange-cost-efficient-llm-serving-gpu-heterogeneity.md` |
| 68 | research | arXiv:2404.12457 | RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2404.12457) | `papers/inference/99-other-inference-systems/2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md` |
| 69 | research | arXiv:2402.02082 | GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding | [primary](https://arxiv.org/abs/2402.02082) | `papers/inference/99-other-inference-systems/2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md` |
| 70 | research | arXiv:2209.01188 | Petals: Collaborative Inference and Fine-tuning of Large Models | [primary](https://arxiv.org/abs/2209.01188) | `papers/inference/99-other-inference-systems/2022-2209.01188-petals-collaborative-inference-and-fine-tuning-of-large-models.md` |
| 71 | research | arXiv:2603.07810 | Temperature-Aware Scheduling of LLM Inference in Large-Scale Geo-Distributed Edge Data Centers with Distributed Optimization | [primary](https://arxiv.org/abs/2603.07810) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2603.07810-temperature-aware-geo-distributed-llm-scheduling.md` |
| 72 | research | arXiv:2206.01861 | ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers | [primary](https://arxiv.org/abs/2206.01861) | `papers/inference/99-other-inference-systems/2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-scale-transformers.md` |
| 73 | research | SemanticScholar:d79a26226393f687ddbc375e32055b40b8ad8d38 | GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism | [primary](https://www.semanticscholar.org/paper/d79a26226393f687ddbc375e32055b40b8ad8d38) | `papers/inference/99-other-inference-systems/2026-e5d747247a09-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism.md` |
| 74 | research | arXiv:2202.08906 | ST-MoE | [primary](https://arxiv.org/abs/2202.08906) | `papers/inference/99-other-inference-systems/2022-2202.08906-st-moe.md` |
| 75 | research | arXiv:2402.04396 | QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks | [primary](https://arxiv.org/abs/2402.04396) | `papers/inference/99-other-inference-systems/2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-codebooks.md` |
| 76 | research | arXiv:2008.12260 | Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning | [primary](https://arxiv.org/abs/2008.12260) | `papers/inference/99-other-inference-systems/2020-2008.12260-pollux-co-adaptive-cluster-scheduling-for-goodput-optimized-deep-learning.md` |
| 77 | research | arXiv:2006.02464 | Serving DNNs like Clockwork: Performance Predictability from the Bottom Up | [primary](https://arxiv.org/abs/2006.02464) | `papers/inference/99-other-inference-systems/2020-2006.02464-serving-dnns-like-clockwork-performance-predictability-from-the-bottom-up.md` |
| 78 | research | arXiv:2504.15720 | SeaLLM: Service-Aware and Latency-Optimized Resource Sharing for Large Language Model Inference | [primary](https://arxiv.org/abs/2504.15720) | `papers/inference/99-other-inference-systems/2025-2504.15720-seallm-service-aware-and-latency-optimized-resource-sharing-for-large-language-model-inference.md` |
| 79 | research | arXiv:2511.17560 | A3: Attention-Aware Accurate KV Cache Fusion for Fast Large Language Model Serving | [primary](https://arxiv.org/abs/2511.17560) | `papers/inference/99-other-inference-systems/2025-2511.17560-a3-attention-aware-accurate-kv-cache-fusion-for-fast-large-language-model-serving.md` |
| 80 | research | arXiv:2511.13676 | T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization | [primary](https://arxiv.org/abs/2511.13676) | `papers/inference/99-other-inference-systems/2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-place-simd-alu-reorganization.md` |
| 81 | research | arXiv:2503.16428 | XAttention: Block Sparse Attention with Antidiagonal Scoring | [primary](https://arxiv.org/abs/2503.16428) | `papers/inference/99-other-inference-systems/2025-2503.16428-xattention-block-sparse-attention-with-antidiagonal-scoring.md` |
| 82 | research | arXiv:2601.05109 | Nalar: A Serving Framework for Agent Workflows | [primary](https://arxiv.org/abs/2601.05109) | `papers/inference/99-other-inference-systems/2026-2601.05109-nalar-a-serving-framework-for-agent-workflows.md` |
| 83 | research | arXiv:2402.18096 | No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization | [primary](https://arxiv.org/abs/2402.18096) | `papers/inference/99-other-inference-systems/2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-mixed-precision-quantization.md` |
| 84 | research | arXiv:2502.18137 | SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference | [primary](https://arxiv.org/abs/2502.18137) | `papers/inference/99-other-inference-systems/2025-2502.18137-spargeattention-accurate-and-training-free-sparse-attention-accelerating-any-model-inference.md` |
| 85 | research | arXiv:2403.07652 | Harder Tasks Need More Experts: Dynamic Routing in MoE Models | [primary](https://arxiv.org/abs/2403.07652) | `papers/inference/99-other-inference-systems/2024-2403.07652-harder-tasks-need-more-experts-dynamic-routing-in-moe-models.md` |
| 86 | research | arXiv:2403.01136 | LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Aware Partition and Adaptive Quantization | [primary](https://arxiv.org/abs/2403.01136) | `papers/inference/99-other-inference-systems/2024-2403.01136-llm-pq-serving-llm-on-heterogeneous-clusters-with-phase-aware-partition-and-adaptive-quantization.md` |
| 87 | research | arXiv:2511.07427 | DynaKV: Enabling Accurate and Efficient Long-Sequence LLM Decoding on Smartphones | [primary](https://arxiv.org/abs/2511.07427) | `papers/inference/99-other-inference-systems/2025-2511.07427-dynakv-enabling-accurate-and-efficient-long-sequence-llm-decoding-on-smartphones.md` |
| 88 | research | DOI:10.1145/3689031.3696072 | Fast State Restoration in LLM Serving with HCache | [primary](https://doi.org/10.1145/3689031.3696072) | `papers/inference/99-other-inference-systems/0000-c57896a0996e-fast-state-restoration-in-llm-serving-with-hcache.md` |
| 89 | research | arXiv:2506.02634 | KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider | [primary](https://arxiv.org/abs/2506.02634) | `papers/inference/99-other-inference-systems/2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at-a-large-cloud-provider.md` |
| 90 | research | arXiv:2402.15220 | ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition | [primary](https://arxiv.org/abs/2402.15220) | `papers/inference/99-other-inference-systems/2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-two-phase-partition.md` |
| 91 | research | arXiv:2510.08731 | When to Reason: Semantic Router for vLLM | [primary](https://arxiv.org/abs/2510.08731) | `papers/inference/99-other-inference-systems/2025-2510.08731-when-to-reason-semantic-router-for-vllm.md` |
| 92 | research | arXiv:2403.08245 | Scattered Mixture-of-Experts Implementation | [primary](https://arxiv.org/abs/2403.08245) | `papers/inference/99-other-inference-systems/2024-2403.08245-scattered-mixture-of-experts-implementation.md` |
| 93 | research | arXiv:2109.01611 | Multi-model Machine Learning Inference Serving with GPU Spatial Partitioning | [primary](https://arxiv.org/abs/2109.01611) | `papers/inference/99-other-inference-systems/2021-2109.01611-multi-model-machine-learning-inference-serving-with-gpu-spatial-partitioning.md` |
| 94 | research | DOI:10.1145/3725338 | PQCache: Product Quantization-based KVCache for Long Context LLM Inference | [primary](https://doi.org/10.1145/3725338) | `papers/inference/99-other-inference-systems/0000-24362ae4b461-pqcache-product-quantization-based-kvcache-for-long-context-llm-inference.md` |
| 95 | research | arXiv:2602.09721 | Revealing the Challenges of Attention-FFN Disaggregation for Modern MoE Models and Hardware Systems | [primary](https://arxiv.org/abs/2602.09721) | `papers/inference/99-other-inference-systems/2026-2602.09721-revealing-the-challenges-of-attention-ffn-disaggregation-for-modern-moe-models-and-hardware-systems.md` |
| 96 | research | DOI:10.52202/079017-0722 | SnapKV: LLM Knows What You are Looking for Before Generation | [primary](https://doi.org/10.52202/079017-0722) | `papers/inference/99-other-inference-systems/0000-838f46f28a47-snapkv-llm-knows-what-you-are-looking-for-before-generation.md` |
| 97 | research | arXiv:2509.24663 | InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation | [primary](https://arxiv.org/abs/2509.24663) | `papers/inference/99-other-inference-systems/2025-2509.24663-infllm-v2-dense-sparse-switchable-attention-for-seamless-short-to-long-adaptation.md` |
| 98 | research | arXiv:2201.12023 | Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning | [primary](https://arxiv.org/abs/2201.12023) | `papers/inference/99-other-inference-systems/2022-2201.12023-alpa-automating-inter-and-intra-operator-parallelism-for-distributed-deep-learning.md` |
| 99 | research | DOI:10.18653/v1/2025.acl-long.1211 | RefreshKV: Updating Small KV Cache During Long-form Generation | [primary](https://doi.org/10.18653/v1/2025.acl-long.1211) | `papers/inference/99-other-inference-systems/0000-a2b748353aae-refreshkv-updating-small-kv-cache-during-long-form-generation.md` |
| 100 | research | arXiv:2410.17375 | AMUSD: Asynchronous Multi-Device Speculative Decoding for LLM Acceleration | [primary](https://arxiv.org/abs/2410.17375) | `papers/inference/99-other-inference-systems/2024-2410.17375-amusd-asynchronous-multi-device-speculative-decoding-for-llm-acceleration.md` |
| 101 | research | arXiv:2006.09616 | Dynamic Tensor Rematerialization | [primary](https://arxiv.org/abs/2006.09616) | `papers/inference/99-other-inference-systems/2020-2006.09616-dynamic-tensor-rematerialization.md` |
| 102 | research | arXiv:2110.15032 | OneFlow: Redesign the Distributed Deep Learning Framework from Scratch | [primary](https://arxiv.org/abs/2110.15032) | `papers/inference/99-other-inference-systems/2021-2110.15032-oneflow-redesign-the-distributed-deep-learning-framework-from-scratch.md` |
| 103 | research | DOI:10.1145/3731569.3764834 | PrefillOnly: An Inference Engine for Prefill-only Workloads in Large Language Model Applications | [primary](https://doi.org/10.1145/3731569.3764834) | `papers/inference/99-other-inference-systems/0000-cc54e0b027f8-prefillonly-an-inference-engine-for-prefill-only-workloads-in-large-language-model-applications.md` |
| 104 | research | arXiv:2411.01783 | Context Parallelism for Scalable Million-Token Inference | [primary](https://arxiv.org/abs/2411.01783) | `papers/inference/99-other-inference-systems/2024-2411.01783-context-parallelism-for-scalable-million-token-inference.md` |
| 105 | research | arXiv:2601.12967 | Sutradhara: An Intelligent Orchestrator-Engine Co-design for Tool-based Agentic Inference | [primary](https://arxiv.org/abs/2601.12967) | `papers/inference/99-other-inference-systems/2026-2601.12967-sutradhara-an-intelligent-orchestrator-engine-co-design-for-tool-based-agentic-inference.md` |
| 106 | research | DOI:10.1145/3731569.3764823 | Jenga: Effective Memory Management for Serving LLM with Heterogeneity | [primary](https://doi.org/10.1145/3731569.3764823) | `papers/inference/99-other-inference-systems/0000-c5994a53cb83-jenga-effective-memory-management-for-serving-llm-with-heterogeneity.md` |
| 107 | research | DOI:10.1109/hpca61900.2025.00103 | throttLL’eM: Predictive GPU Throttling for Energy Efficient LLM Inference Serving | [primary](https://doi.org/10.1109/hpca61900.2025.00103) | `papers/inference/99-other-inference-systems/0000-f8a5c43e140a-throttllem-predictive-gpu-throttling-for-energy-efficient-llm-inference-serving.md` |
| 108 | research | arXiv:2507.10524 | Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation | [primary](https://arxiv.org/abs/2507.10524) | `papers/inference/99-other-inference-systems/2025-2507.10524-mixture-of-recursions-learning-dynamic-recursive-depths-for-adaptive-token-level-computation.md` |
| 109 | research | DOI:10.1145/3690624.3709196 | ResMoE: Space-efficient Compression of Mixture of Experts LLMs via Residual Restoration | [primary](https://doi.org/10.1145/3690624.3709196) | `papers/inference/99-other-inference-systems/0000-097fa558562e-resmoe-space-efficient-compression-of-mixture-of-experts-llms-via-residual-restoration.md` |
| 110 | research | arXiv:2410.10759 | SplitLLM: Collaborative Inference of LLMs for Model Placement and Throughput Optimization | [primary](https://arxiv.org/abs/2410.10759) | `papers/inference/99-other-inference-systems/2024-2410.10759-splitllm-collaborative-inference-of-llms-for-model-placement-and-throughput-optimization.md` |
| 111 | research | DOI:10.1109/iiswc63097.2024.00012 | LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale | [primary](https://doi.org/10.1109/iiswc63097.2024.00012) | `papers/inference/99-other-inference-systems/0000-4302fa896bd8-llmservingsim-a-hw-sw-co-simulation-infrastructure-for-llm-inference-serving-at-scale.md` |
| 112 | research | arXiv:2409.01143 | HexiScale: Facilitating Large Language Model Training over Heterogeneous Hardware | [primary](https://arxiv.org/abs/2409.01143) | `papers/inference/99-other-inference-systems/2024-2409.01143-hexiscale-facilitating-large-language-model-training-over-heterogeneous-hardware.md` |
| 113 | research | arXiv:2306.10209 | ZeRO++: Extremely Efficient Collective Communication for Giant Model Training | [primary](https://arxiv.org/abs/2306.10209) | `papers/inference/99-other-inference-systems/2023-2306.10209-zero-extremely-efficient-collective-communication-for-giant-model-training.md` |
| 114 | research | DOI:10.1145/3669940.3707285 | Medusa: Accelerating Serverless LLM Inference with Materialization | [primary](https://doi.org/10.1145/3669940.3707285) | `papers/inference/99-other-inference-systems/0000-8c4404f09758-medusa-accelerating-serverless-llm-inference-with-materialization.md` |
| 115 | research | arXiv:2512.14080 | SonicMoE: Accelerating MoE with IO and Tile-aware Optimizations | [primary](https://arxiv.org/abs/2512.14080) | `papers/inference/99-other-inference-systems/2025-2512.14080-sonicmoe-accelerating-moe-with-io-and-tile-aware-optimizations.md` |
| 116 | research | arXiv:2402.11131 | Speculative Streaming: Fast LLM Inference without Auxiliary Models | [primary](https://arxiv.org/abs/2402.11131) | `papers/inference/99-other-inference-systems/2024-2402.11131-speculative-streaming-fast-llm-inference-without-auxiliary-models.md` |
| 117 | research | arXiv:2505.05286 | HEXGEN-TEXT2SQL: Optimizing LLM Inference Request Scheduling for Agentic Text-to-SQL Workflow | [primary](https://arxiv.org/abs/2505.05286) | `papers/inference/99-other-inference-systems/2025-2505.05286-hexgen-text2sql-optimizing-llm-inference-request-scheduling-for-agentic-text-to-sql-workflow.md` |
| 118 | research | arXiv:2312.06635 | Gated Linear Attention Transformers with Hardware-Efficient Training | [primary](https://arxiv.org/abs/2312.06635) | `papers/inference/99-other-inference-systems/2023-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md` |
| 119 | research | arXiv:2410.18517 | KVSharer: Efficient Inference via Layer-Wise Dissimilar KV Cache Sharing | [primary](https://arxiv.org/abs/2410.18517) | `papers/inference/99-other-inference-systems/2024-2410.18517-kvsharer-efficient-inference-via-layer-wise-dissimilar-kv-cache-sharing.md` |
| 120 | research | arXiv:2404.05019 | Shortcut-connected Expert Parallelism for Accelerating Mixture-of-Experts | [primary](https://arxiv.org/abs/2404.05019) | `papers/inference/99-other-inference-systems/2024-2404.05019-shortcut-connected-expert-parallelism-for-accelerating-mixture-of-experts.md` |
| 121 | research | arXiv:2412.18169 | KUNSERVE: Parameter-centric Memory Management for Efficient Memory Overloading Handling in LLM Serving | [primary](https://arxiv.org/abs/2412.18169) | `papers/inference/99-other-inference-systems/2024-2412.18169-kunserve-parameter-centric-memory-management-for-efficient-memory-overloading-handling-in-llm-serving.md` |
| 122 | research | arXiv:2310.07188 | Adaptive Gating in Mixture-of-Experts based Language Models | [primary](https://arxiv.org/abs/2310.07188) | `papers/inference/99-other-inference-systems/2023-2310.07188-adaptive-gating-in-mixture-of-experts-based-language-models.md` |
| 123 | research | arXiv:2510.01336 | HiSpec: Hierarchical Speculative Decoding for LLMs | [primary](https://arxiv.org/abs/2510.01336) | `papers/inference/99-other-inference-systems/2025-2510.01336-hispec-hierarchical-speculative-decoding-for-llms.md` |
| 124 | research | arXiv:2505.20225 | FLAME-MoE: A Transparent End-to-End Research Platform for Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2505.20225) | `papers/inference/99-other-inference-systems/2025-2505.20225-flame-moe-a-transparent-end-to-end-research-platform-for-mixture-of-experts-language-models.md` |
| 125 | research | arXiv:2503.00634 | Efficiently Editing Mixture-of-Experts Models with Compressed Experts | [primary](https://arxiv.org/abs/2503.00634) | `papers/inference/99-other-inference-systems/2025-2503.00634-efficiently-editing-mixture-of-experts-models-with-compressed-experts.md` |
| 126 | research | arXiv:2411.09688 | Squeezed Attention: Accelerating Long Context Length LLM Inference | [primary](https://arxiv.org/abs/2411.09688) | `papers/inference/99-other-inference-systems/2024-2411.09688-squeezed-attention-accelerating-long-context-length-llm-inference.md` |
| 127 | research | arXiv:2408.05646 | Eigen Attention: Attention in Low-Rank Space for KV Cache Compression | [primary](https://arxiv.org/abs/2408.05646) | `papers/inference/99-other-inference-systems/2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md` |
| 128 | research | arXiv:2507.11941 | BlockBPE: Parallel BPE Tokenization | [primary](https://arxiv.org/abs/2507.11941) | `papers/inference/99-other-inference-systems/2025-2507.11941-blockbpe-parallel-bpe-tokenization.md` |
| 129 | research | arXiv:2306.08543 | MiniLLM: On-Policy Distillation of Large Language Models | [primary](https://arxiv.org/abs/2306.08543) | `papers/inference/99-other-inference-systems/2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5530** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3694715.3695948 |  |  | 15 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 2 | DOI:10.1145/3669940.3707267 |  |  | 13 | KV Cache Optimization / Compression, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Offload / Hierarchical Memory, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, hierarchical-memory-kv-offload-cpu-gpu-attention, moe-inference-expert-placement-caching, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://doi.org/10.1145/3669940.3707267) |
| 3 | OpenReview:QOXrVMiHGK |  |  | 12 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative Decoding / Parallel Inference Systems, speculative-decoding, speculative-decoding-moe, 投機的デコード／動的候補木／高同時実行LLMサービング | [source](https://openreview.net/forum?id=QOXrVMiHGK) |
| 4 | OpenReview:Byj72udxe |  |  | 11 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, Offload / Hierarchical Memory, Quantization × MoE × Offload, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization, dense-to-MoE conversion / conditional FFN computation / expert routing, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://openreview.net/forum?id=Byj72udxe) |
| 5 | OpenReview:cFu7ze7xUm |  |  | 11 | 13-sparse-attention, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, other-inference-systems | [source](https://openreview.net/forum?id=cFu7ze7xUm) |
| 6 | DOI:10.48550/arxiv.2404.07413 |  |  | 10 | 02-adaptive-expert-computation-compression, Adaptive computation／cache-aware MoE, MoE compression / expert merging / output approximation / least-squares compression, MoE predictive expert placement / replication / SiDA-MoE, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, moe-parallelism-communication, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2404.07413) |
| 7 | OpenReview:VTF8yNQM66 |  |  | 10 | 13-sparse-attention, Agentic Serving Benchmarking, MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, agentic workflow serving / workflow physical planning / adaptive serving, llm-serving-scheduling-disaggregation, other-inference-systems, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=VTF8yNQM66) |
| 8 | arXiv:2502.00722 |  |  | 10 | 01-offload-hierarchical-memory, llm-serving-scheduling-disaggregation, llm-serving-systems, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング, 異種GPUサービング・分散推論・パイプライン並列・動的ルーティング, 異種GPU・事前充填/復号分離サービング | [source](https://arxiv.org/abs/2502.00722) |
| 9 | arXiv:1606.05250 |  |  | 9 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV Cache Optimization / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE compression / expert merging / output approximation / least-squares compression, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1606.05250) |
| 10 | DOI:10.1162/neco.1991.3.1.79 |  |  | 9 | Adaptive computation／cache-aware MoE, Expert Prefetch, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization, adaptive-expert-computation-compression, dynamic-pd-disaggregation, オフロード／階層メモリ | [source](https://doi.org/10.1162/neco.1991.3.1.79) |
| 11 | arXiv:2209.05433 |  |  | 9 | 02-hardware-accelerators, KV Cache Optimization / Compression, KVキャッシュ退避／長文推論／KV選択／KV量子化, LLM inference surveys、roofline performance analysis, LLM学習／階層メモリ／CPU退避／勾配チェックポイント／自動構成探索, flash-capacity-tier-inference, survey-low-bit-llm | [source](https://arxiv.org/abs/2209.05433) |
| 12 | arXiv:2411.16102 |  |  | 9 | KV Cache Offload / Recomputation, LLM serving scheduling / hybrid QoS / KV cache management, MoE serving / expert offloading / prefill-only serving, llm-serving-scheduling-disaggregation, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング, オフロード／階層メモリ, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2411.16102) |
| 13 | OpenReview:qrwe7XHTmYb |  |  | 9 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, LLM Serving / Multi-Model Serving / Memory Disaggregation, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, Speculative decoding × MoE, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=qrwe7XHTmYb) |
| 14 | arXiv:2503.09573 |  |  | 9 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, diffusion language model inference / KV cache / training-free acceleration, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://arxiv.org/abs/2503.09573) |
| 15 | arXiv:2201.11903 |  |  | 8 | 13-sparse-attention, Adaptive Expert Computation / Compression, Conditional Computation, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, Offload / Hierarchical Memory, Speculative Decoding / Parallel Inference Systems, speculative decoding / edge-assisted serving / distributed inference / pipeline scheduling | [source](https://arxiv.org/abs/2201.11903) |
| 16 | arXiv:2409.06669 |  |  | 8 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, Quantization × MoE × Offload, Speculative decoding × MoE, adaptive expert computation / dynamic MoE routing / expert sparsification, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2409.06669) |
| 17 | arXiv:2402.17764 |  |  | 8 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline, offload-hierarchical-memory, post-training quantization / ternary LLM / packed inference, survey-distributed-training-systems, survey-low-bit-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.17764) |
| 18 | OpenReview:Ti67584b98 |  |  | 8 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Other Inference Systems / Lossless Parallel Decoding, Speculative decoding × MoE, kv-cache-optimization-compression, sparse attention / learned context ranking / long-context LLM inference, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://openreview.net/forum?id=Ti67584b98) |
| 19 | arXiv:2401.15947 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis, MoE expert pruning / expert clustering / task-specific model compression, Quantization × MoE × Offload, オフロード／階層メモリ, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2401.15947) |
| 20 | DOI:10.18653/v1/2020.emnlp-demos.6 |  |  | 8 | 13-sparse-attention, MoE expert offloading / predictive prefetch and cache management, early-exit-offloading-self-speculative-decoding, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, kv-cache-optimization-compression, other-inference-systems | [source](https://doi.org/10.18653/v1/2020.emnlp-demos.6) |
| 21 | arXiv:2304.04487 |  |  | 8 | LLM inference surveys、roofline performance analysis, Speculative Decoding, survey-speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 投機的デコード / 自己投機的デコード / 層スキップ | [source](https://arxiv.org/abs/2304.04487) |
| 22 | DOI:10.1609/aaai.v34i05.6239 |  |  | 8 | Adaptive computation／cache-aware MoE, KV cache management benchmarking, MoE compression / training-free expert merging / multimodal MoE routing, adaptive-expert-computation-compression, early-exit-offloading-self-speculative-decoding | [source](https://doi.org/10.1609/aaai.v34i05.6239) |
| 23 | DOI:10.48550/arxiv.2412.00099 |  |  | 8 | hardware-accelerators, offload-hierarchical-memory, survey-moe-inference-optimization, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.48550/arxiv.2412.00099) |
| 24 | arXiv:2312.05821 |  |  | 7 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, MoE専門家オフロード / 混合精度 / 専門家キャッシュ, edge LLM inference / SSD near-storage processing / DRAM PIM / activation sparsity / heterogeneous acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.05821) |
| 25 | arXiv:2402.12065 |  |  | 7 | KV Cache Optimization / Compression, LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload, System-aware KV cache, distributed LLM inference / communication-aware serving, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.12065) |
| 26 | OpenReview:nZeVKeeFYf9 |  |  | 7 | 18-vla-inference-quantization-evaluation, KV cache sparsity / paged attention / query-aware selection / LLM serving, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, llm-serving-systems, その他システム研究 | [source](https://openreview.net/forum?id=nZeVKeeFYf9) |
| 27 | arXiv:2308.12966 |  |  | 7 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 28 | DOI:10.18653/v1/2020.coling-main.580 |  |  | 7 | 10-kv-キャッシュ-オフロード-recomputation, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, Prefill/Decode Disaggregation / Selective KV Transfer | [source](https://doi.org/10.18653/v1/2020.coling-main.580) |
| 29 | arXiv:2203.14685 |  |  | 7 | Adaptive Expert Computation / Compression, MoE推論・エキスパート配置・全対全通信スケジューリング・異種GPU, survey-moe-inference-optimization, その他システム研究 | [source](https://arxiv.org/abs/2203.14685) |
| 30 | arXiv:2407.21118 |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2407.21118) |
| 31 | DOI:10.1145/3711896.3737413 |  |  | 7 | LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3711896.3737413) |
| 32 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 33 | DOI:10.48550/arxiv.2407.12391 |  |  | 6 | SLO-aware LLM serving scheduling, System-aware KV cache, disaggregated LLM serving / request routing / learned scheduling, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://doi.org/10.48550/arxiv.2407.12391) |
| 34 | arXiv:2306.09212 |  |  | 6 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2306.09212) |
| 35 | arXiv:2511.21631 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / dynamic MoE routing / gating uncertainty, flash-capacity-tier-inference | [source](https://arxiv.org/abs/2511.21631) |
| 36 | arXiv:2303.08302 |  |  | 6 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Weight Quantization / Compression, offload-hierarchical-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2303.08302) |
| 37 | arXiv:2408.11743 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 38 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 39 | DOI:10.18653/v1/p17-1099 |  |  | 6 | LLM serving / CPU-GPU heterogeneous inference / SLO-aware scheduling / KV-cache offloading, speculative-decoding, 投機的復号 / LLMサービング・ベンチマーク, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://doi.org/10.18653/v1/p17-1099) |
| 40 | OpenReview:RkRrPp7GKO |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=RkRrPp7GKO) |
| 41 | DOI:10.48550/arxiv.2402.08268 |  |  | 6 | 10-kv-キャッシュ-オフロード-recomputation, serving-scheduling | [source](https://doi.org/10.48550/arxiv.2402.08268) |
| 42 | OpenReview:poE54GOq2l |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=poE54GOq2l) |
| 43 | arXiv:2204.09179 |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 44 | arXiv:2504.21318 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 45 | DOI:10.1145/3676641.3716278 |  |  | 5 | 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 46 | OpenReview:7kQjbCQwtT |  |  | 5 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-inference-expert-offloading, moe-quantization-compression, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=7kQjbCQwtT) |
| 47 | arXiv:2209.11895 |  |  | 5 | KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/2209.11895) |
| 48 | DOI:10.1109/ispass48437.2020.00018 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass48437.2020.00018) |
| 49 | OpenReview:Bl8u7ZRlbM |  |  | 5 | 11-llm-serving-scheduling-disaggregation, KV cache reuse / context caching / multi-tenant LLM serving / selective recomputation, agent serving / KV-cache reuse / latent communication / DAG workflows, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://openreview.net/forum?id=Bl8u7ZRlbM) |
| 50 | arXiv:2311.13581 |  |  | 5 | LLM inference surveys、roofline performance analysis, survey-speculative-decoding, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2311.13581) |
| 51 | arXiv:2501.08313 |  |  | 5 | 13-sparse-attention, moe-parallelism-communication, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.08313) |
| 52 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 53 | OpenReview:tcbBPnfwxS |  |  | 5 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=tcbBPnfwxS) |
| 54 | DOI:10.18653/v1/n18-2097 |  |  | 5 | llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 55 | arXiv:1603.08983 |  |  | 4 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 56 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 57 | arXiv:2310.18813 |  |  | 4 | speculative-decoding, survey-speculative-decoding, 投機的デコード・バッチ推論, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2310.18813) |
| 58 | arXiv:2503.20314 |  |  | 4 | MoE inference / expert parallelism / expert replication / load balancing, MoE routing / expert offloading / temporal expert persistence, llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://arxiv.org/abs/2503.20314) |
| 59 | DOI:10.1145/3620666.3651352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 60 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 61 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 62 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 63 | arXiv:2203.08913 |  |  | 4 | LLM inference surveys、roofline performance analysis, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 64 | OpenReview:cSimKw5p6R |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, agentic workflow serving / workflow physical planning / adaptive serving, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://openreview.net/forum?id=cSimKw5p6R) |
| 65 | arXiv:2402.18013 |  |  | 4 | llm-serving-scheduling-disaggregation, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2402.18013) |
| 66 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 67 | arXiv:2402.02244 |  |  | 3 | LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 68 | arXiv:2503.08311 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2503.08311) |
| 69 | arXiv:2512.22420 |  |  | 3 | llm-serving-scheduling-disaggregation, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2512.22420) |
| 70 | DOI:10.1109/hoti.2015.13 |  |  | 3 | KVキャッシュオフロード・再計算, RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/hoti.2015.13) |
| 71 | DOI:10.1109/lca.2025.3628325 |  |  | 3 | 12-benchmarking-modeling-emulation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, other-inference-systems | [source](https://doi.org/10.1109/lca.2025.3628325) |
| 72 | DOI:10.1109/sc41405.2020.00024 |  |  | 3 | Adaptive computation／cache-aware MoE, その他システム研究, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/sc41405.2020.00024) |
| 73 | DOI:10.1145/1534530.1534544 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, offload-hierarchical-memory, オフロード／階層メモリ | [source](https://doi.org/10.1145/1534530.1534544) |
| 74 | DOI:10.1145/3620666.3651379 |  |  | 3 | kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 75 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 76 | DOI:10.1145/3731569.3764813 |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764813) |
| 77 | DOI:10.48550/arxiv.2507.17702 |  |  | 3 | adaptive expert computation / compression; end-side sparse MoE, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://doi.org/10.48550/arxiv.2507.17702) |
| 78 | OpenReview:1qvx610Cu7 |  |  | 3 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 79 | OpenReview:c8McWs4Av0 |  |  | 3 | Adaptive Expert Computation / Compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=c8McWs4Av0) |
| 80 | OpenReview:LywifFNXV5 |  |  | 3 | CPU長文推論・近似注意, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://openreview.net/forum?id=LywifFNXV5) |
| 81 | OpenReview:TrjbxzRcnf- |  |  | 3 | KVキャッシュ・注意アーキテクチャ, KVキャッシュ再利用／圧縮／ネットワーク転送, other-inference-systems | [source](https://openreview.net/forum?id=TrjbxzRcnf-) |
| 82 | OpenReview:z3JZzu9EA3 |  |  | 3 | KV Cache Optimization / Compression, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=z3JZzu9EA3) |
| 83 | arXiv:2409.02813 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2409.02813) |
| 84 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 85 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 86 | DOI:10.1145/3581784.3607062 |  |  | 3 | Sparse Attention, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1145/3581784.3607062) |
| 87 | DOI:10.1145/3719330.3721230 |  |  | 3 | 08-edge-on-device-llm-systems, KV Cache Offload / Recomputation | [source](https://doi.org/10.1145/3719330.3721230) |
| 88 | DOI:10.1162/tacl%5fa%5f00276 |  |  | 3 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://doi.org/10.1162/tacl%5fa%5f00276) |
| 89 | DOI:10.18653/v1/2024.acl-long.814 |  |  | 3 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.814) |
| 90 | DOI:10.48550/arxiv.2409.12136 |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2409.12136) |
| 91 | OpenReview:ayi7qezU87 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://openreview.net/forum?id=ayi7qezU87) |
| 92 | OpenReview:LKEJPySnlt |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=LKEJPySnlt) |
| 93 | OpenReview:rJ4km2R5t7 |  |  | 3 | MoE inference / task-specific expert pruning / sparse-to-dense conversion, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rJ4km2R5t7) |
| 94 | OpenReview:ul4W26KEKz |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://openreview.net/forum?id=ul4W26KEKz) |
| 95 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 96 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 97 | arXiv:1412.7024 |  |  | 2 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 98 | arXiv:2011.01060 |  |  | 2 | kv-cache-offload-recomputation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification | [source](https://arxiv.org/abs/2011.01060) |
| 99 | arXiv:2212.01378 |  |  | 2 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2212.01378) |
| 100 | arXiv:2306.02272 |  |  | 2 | LLM inference surveys、roofline performance analysis, Weight Quantization / Compression | [source](https://arxiv.org/abs/2306.02272) |
| 101 | arXiv:2306.04050 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 102 | arXiv:2307.04964 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2307.04964) |
| 103 | arXiv:2308.06093 |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 104 | arXiv:2308.12908 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2308.12908) |
| 105 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 106 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 107 | arXiv:2309.14393 |  |  | 2 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 108 | arXiv:2310.01655 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2310.01655) |
| 109 | arXiv:2310.05424 |  |  | 2 | speculative decoding / draft-model design, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2310.05424) |
| 110 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 111 | arXiv:2311.09550 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 112 | arXiv:2311.13171 |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 113 | arXiv:2312.00678 |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 114 | arXiv:2312.04916 |  |  | 2 | early-exit-offloading-self-speculative-decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 115 | arXiv:2312.13558 |  |  | 2 | LLM inference surveys、roofline performance analysis, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 116 | arXiv:2401.02038 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 117 | arXiv:2401.07339 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.07339) |
| 118 | arXiv:2401.14021 |  |  | 2 | KV Cache Optimization / Compression, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2401.14021) |
| 119 | arXiv:2402.01680 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 120 | arXiv:2402.06126 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.06126) |
| 121 | arXiv:2402.12289 |  |  | 2 | Expert Prefetch, survey-edge-llm | [source](https://arxiv.org/abs/2402.12289) |
| 122 | arXiv:2402.13718 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.13718) |
| 123 | arXiv:2402.18158 |  |  | 2 | Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.18158) |
| 124 | arXiv:2403.03507 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, その他システム研究 | [source](https://arxiv.org/abs/2403.03507) |
| 125 | arXiv:2403.07816 |  |  | 2 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2403.07816) |
| 126 | arXiv:2403.12422 |  |  | 2 | survey-distributed-training-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.12422) |
| 127 | arXiv:2404.07839 |  |  | 2 | hybrid Mamba-Transformer inference memory management, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2404.07839) |
| 128 | arXiv:2404.13628 |  |  | 2 | 02-adaptive-expert-computation-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2404.13628) |
| 129 | arXiv:2405.03133 |  |  | 2 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.03133) |
| 130 | arXiv:2405.21015 |  |  | 2 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation, その他システム研究 | [source](https://arxiv.org/abs/2405.21015) |
| 131 | arXiv:2406.02430 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.02430) |
| 132 | arXiv:2406.04127 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2406.04127) |
| 133 | arXiv:2406.08673 |  |  | 2 | 大規模分散学習・整合学習基盤, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2406.08673) |
| 134 | arXiv:2406.11939 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2406.11939) |
| 135 | arXiv:2406.18629 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2406.18629) |
| 136 | arXiv:2407.00128 |  |  | 2 | Speculative Decoding / Parallel Inference Systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.00128) |
| 137 | arXiv:2407.08296 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, survey-low-bit-llm | [source](https://arxiv.org/abs/2407.08296) |
| 138 | arXiv:2407.10855 |  |  | 2 | kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.10855) |
| 139 | arXiv:2407.12821 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2407.12821) |
| 140 | arXiv:2408.06292 |  |  | 2 | LLMサービング／自動スケーリング／広域ルーティング, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2408.06292) |
| 141 | arXiv:2409.06857 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, offload-hierarchical-memory | [source](https://arxiv.org/abs/2409.06857) |
| 142 | arXiv:2409.17146 |  |  | 2 | Adaptive computation／cache-aware MoE, adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2409.17146) |
| 143 | arXiv:2410.00037 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.00037) |
| 144 | arXiv:2410.05589 |  |  | 2 | 投機的デコード／動的LLMサービング／GPU空間多重化, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2410.05589) |
| 145 | arXiv:2410.10762 |  |  | 2 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10762) |
| 146 | arXiv:2410.13461 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2410.13461) |
| 147 | arXiv:2410.17840 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.17840) |
| 148 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 149 | arXiv:2411.02335 |  |  | 2 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, adaptive expert computation / compression; end-side sparse MoE | [source](https://arxiv.org/abs/2411.02335) |
| 150 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 151 | arXiv:2411.11055 |  |  | 2 | Speculative decoding × MoE, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 152 | arXiv:2411.17309 |  |  | 2 | Offload / Hierarchical Memory, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.17309) |
| 153 | arXiv:2412.12488 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.12488) |
| 154 | arXiv:2412.14468 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLMサービング・接頭辞キャッシュ・マルチテナント隔離 | [source](https://arxiv.org/abs/2412.14468) |
| 155 | arXiv:2501.10714 |  |  | 2 | Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2501.10714) |
| 156 | arXiv:2502.01662 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2502.01662) |
| 157 | arXiv:2502.06768 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2502.06768) |
| 158 | arXiv:2502.10424 |  |  | 2 | kv-cache-optimization-compression, speculative-decoding-sparse-verification-kv-selection | [source](https://arxiv.org/abs/2502.10424) |
| 159 | arXiv:2502.15304 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2502.15304) |
| 160 | arXiv:2502.17419 |  |  | 2 | Conditional Computation, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2502.17419) |
| 161 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 162 | arXiv:2503.13444 |  |  | 2 | kv-cache-offload-recomputation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2503.13444) |
| 163 | arXiv:2503.24047 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2503.24047) |
| 164 | arXiv:2504.05299 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2504.05299) |
| 165 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 166 | arXiv:2504.13914 |  |  | 2 | 推論ベンチマーク・推論大規模言語モデルのサービング評価, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2504.13914) |
| 167 | arXiv:2504.16397 |  |  | 2 | agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2504.16397) |
| 168 | arXiv:2504.18154 |  |  | 2 | prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.18154) |
| 169 | arXiv:2505.06252 |  |  | 2 | kv-cache-offload-recomputation, その他システム研究 | [source](https://arxiv.org/abs/2505.06252) |
| 170 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 171 | arXiv:2505.20353 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2505.20353) |
| 172 | arXiv:2506.01844 |  |  | 2 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2506.01844) |
| 173 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 174 | arXiv:2507.09942 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2507.09942) |
| 175 | arXiv:2507.16731 |  |  | 2 | 05-speculative-decoding-moe, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2507.16731) |
| 176 | arXiv:2508.01002 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2508.01002) |
| 177 | arXiv:2508.07227 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2508.07227) |
| 178 | arXiv:2508.10395 |  |  | 2 | 17-pim-near-data-acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2508.10395) |
| 179 | arXiv:2508.17196 |  |  | 2 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.17196) |
| 180 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 181 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 182 | arXiv:2510.01290 |  |  | 2 | inference/07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2510.01290) |
| 183 | arXiv:2510.06513 |  |  | 2 | offload-hierarchical-memory, オフロード／階層メモリ | [source](https://arxiv.org/abs/2510.06513) |
| 184 | arXiv:2510.15330 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.15330) |
| 185 | arXiv:2510.25741 |  |  | 2 | adaptive-expert-computation-compression, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://arxiv.org/abs/2510.25741) |
| 186 | arXiv:2511.16682 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2511.16682) |
| 187 | arXiv:2511.23404 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2511.23404) |
| 188 | arXiv:2512.05916 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.05916) |
| 189 | arXiv:2512.14142 |  |  | 2 | LLMサービング／スケジューリング／分離, other | [source](https://arxiv.org/abs/2512.14142) |
| 190 | arXiv:2512.20848 |  |  | 2 | PIM / Near-Data Acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.20848) |
| 191 | arXiv:2601.07526 |  |  | 2 | 14-agentic-inference-serving-runtime, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2601.07526) |
| 192 | arXiv:2601.11589 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, disaggregated LLM serving / request routing / learned scheduling | [source](https://arxiv.org/abs/2601.11589) |
| 193 | arXiv:2601.22379 |  |  | 2 | 07-kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2601.22379) |
| 194 | arXiv:2602.13836 |  |  | 2 | speculative-decoding, 投機的デコードにおける自己回帰ドラフトと並列ドラフトの折衷 | [source](https://arxiv.org/abs/2602.13836) |
| 195 | arXiv:2603.07904 |  |  | 2 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2603.07904) |
| 196 | arXiv:2603.28101 |  |  | 2 | LLM inference simulation / disaggregated serving / performance modeling, agentic LLM serving / pipeline parallelism / serving scheduling / speculative decoding | [source](https://arxiv.org/abs/2603.28101) |
| 197 | arXiv:2605.20315 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2605.20315) |
| 198 | arXiv:2606.22874 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2606.22874) |
| 199 | DOI:10.1016/j.parco.2015.09.001 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, hardware-accelerators | [source](https://doi.org/10.1016/j.parco.2015.09.001) |
| 200 | DOI:10.1109/dac63849.2025.11132870 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, offload-hierarchical-memory | [source](https://doi.org/10.1109/dac63849.2025.11132870) |
| 201 | DOI:10.1109/hcs59251.2023.10254717 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/hcs59251.2023.10254717) |
| 202 | DOI:10.1109/hpca47549.2020.00030 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, kv-cache-memory | [source](https://doi.org/10.1109/hpca47549.2020.00030) |
| 203 | DOI:10.1109/iccv.2019.00038 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation | [source](https://doi.org/10.1109/iccv.2019.00038) |
| 204 | DOI:10.1109/isca45697.2020.00047 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/isca45697.2020.00047) |
| 205 | DOI:10.1109/ispass.2019.00042 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, 長文推論・KVキャッシュ先読み・要求パッキング・オンチップメモリ・HBM帯域最適化 | [source](https://doi.org/10.1109/ispass.2019.00042) |
| 206 | DOI:10.1109/lca.2025.3566692 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/lca.2025.3566692) |
| 207 | DOI:10.1109/micro61859.2024.00021 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/micro61859.2024.00021) |
| 208 | DOI:10.1109/mm.2024.3420728 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/mm.2024.3420728) |
| 209 | DOI:10.1109/tc.1985.6312218 |  |  | 2 | survey-speculative-decoding, 投機的復号 / 無損失復号高速化 | [source](https://doi.org/10.1109/tc.1985.6312218) |
| 210 | DOI:10.1115/1.3662552 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1115/1.3662552) |
| 211 | DOI:10.1145/1966445.1966473 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Expert Prefetch | [source](https://doi.org/10.1145/1966445.1966473) |
| 212 | DOI:10.1145/2517349.2522716 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/2517349.2522716) |
| 213 | DOI:10.1145/3297858.3304043 |  |  | 2 | hardware-accelerators, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3297858.3304043) |
| 214 | DOI:10.1145/3445814.3446714 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3445814.3446714) |
| 215 | DOI:10.1145/3492321.3519584 |  |  | 2 | MoE serving resilience / decoupled attention-expert serving / KV checkpointing, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3492321.3519584) |
| 216 | DOI:10.1145/3552326.3567508 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory | [source](https://doi.org/10.1145/3552326.3567508) |
| 217 | DOI:10.1145/3575693.3575724 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3575693.3575724) |
| 218 | DOI:10.1145/3582016.3582047 |  |  | 2 | 02-hardware-accelerators, kv-cache-optimization-compression | [source](https://doi.org/10.1145/3582016.3582047) |
| 219 | DOI:10.1145/3605573.3605613 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3605573.3605613) |
| 220 | DOI:10.1145/3627535.3638466 |  |  | 2 | KV Cache Optimization / Compression, serving-scheduling | [source](https://doi.org/10.1145/3627535.3638466) |
| 221 | DOI:10.1145/3642970.3655844 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://doi.org/10.1145/3642970.3655844) |
| 222 | DOI:10.1145/3662006.3662067 |  |  | 2 | 05-speculative-decoding-moe, Edge / On-device LLM Systems | [source](https://doi.org/10.1145/3662006.3662067) |
| 223 | DOI:10.1145/3676641.3716252 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3676641.3716252) |
| 224 | DOI:10.1145/3710848.3710869 |  |  | 2 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 225 | DOI:10.1145/3725843.3756115 |  |  | 2 | PIM / Near-Data Acceleration, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756115) |
| 226 | DOI:10.1145/3768165 |  |  | 2 | Edge / On-device LLM Systems, speculative-decoding-moe | [source](https://doi.org/10.1145/3768165) |
| 227 | DOI:10.1145/3779212.3790236 |  |  | 2 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790236) |
| 228 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 229 | DOI:10.1609/aaai.v38i16.29720 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1609/aaai.v38i16.29720) |
| 230 | DOI:10.18653/v1/2022.emnlp-main.823 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/2022.emnlp-main.823) |
| 231 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 2 | Speculative Decoding, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 232 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 233 | DOI:10.18653/v1/2025.acl-long.531 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/2025.acl-long.531) |
| 234 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 235 | DOI:10.48550/arxiv.2304.07327 |  |  | 2 | KVキャッシュ最適化／適応圧縮, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2304.07327) |
| 236 | DOI:10.48550/arxiv.2410.13056 |  |  | 2 | 16-weight-quantization-compression, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.48550/arxiv.2410.13056) |
| 237 | DOI:10.48550/arxiv.2602.08676 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://doi.org/10.48550/arxiv.2602.08676) |
| 238 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 239 | DOI:10.52202/079017-0381 |  |  | 2 | early-exit-offloading-self-speculative-decoding, speculative-decoding | [source](https://doi.org/10.52202/079017-0381) |
| 240 | DOI:10.52202/085713-1380 |  |  | 2 | 99-other-inference-systems, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/085713-1380) |
| 241 | OpenReview:8Wuvhh0LYW |  |  | 2 | 17-pim-near-data-acceleration, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=8Wuvhh0LYW) |
| 242 | OpenReview:cJd1BgZ9CS |  |  | 2 | speculative-decoding, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://openreview.net/forum?id=cJd1BgZ9CS) |
| 243 | OpenReview:FAeU7516MR |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE | [source](https://openreview.net/forum?id=FAeU7516MR) |
| 244 | OpenReview:H4DqfPSibmx |  |  | 2 | Speculative decoding × MoE, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=H4DqfPSibmx) |
| 245 | OpenReview:JFygzwx8SJ |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=JFygzwx8SJ) |
| 246 | OpenReview:mtSSFiqW6y |  |  | 2 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=mtSSFiqW6y) |
| 247 | OpenReview:R0SoZvqXyQ |  |  | 2 | llm-serving-scheduling-disaggregation, serving-scheduling | [source](https://openreview.net/forum?id=R0SoZvqXyQ) |
| 248 | OpenReview:rsY6J3ZaTF |  |  | 2 | speculative decoding / draft-model design, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=rsY6J3ZaTF) |
| 249 | OpenReview:vXxardq6db |  |  | 2 | Quantization × MoE × Offload, 投機的デコード／MoE | [source](https://openreview.net/forum?id=vXxardq6db) |
| 250 | OpenReview:YolJOZOGhI |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://openreview.net/forum?id=YolJOZOGhI) |
| 251 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 252 | arXiv:2402.10517 |  |  | 2 | LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計 | [source](https://arxiv.org/abs/2402.10517) |
| 253 | arXiv:2404.00242 |  |  | 2 | 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://arxiv.org/abs/2404.00242) |
| 254 | arXiv:2407.07304 |  |  | 2 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2407.07304) |
| 255 | arXiv:2410.05076 |  |  | 2 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.05076) |
| 256 | arXiv:2412.04964 |  |  | 2 | moe-parallelism-communication | [source](https://arxiv.org/abs/2412.04964) |
| 257 | arXiv:2512.15176 |  |  | 2 | speculative decoding / parallel drafting / diffusion-inspired language modeling | [source](https://arxiv.org/abs/2512.15176) |
| 258 | arXiv:2604.16957 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2604.16957) |
| 259 | DOI:10.1109/dac63849.2025.11132479 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer | [source](https://doi.org/10.1109/dac63849.2025.11132479) |
| 260 | DOI:10.1109/isca66397.2026.00021 |  |  | 2 | MoE expert offloading / predictive prefetch and cache management | [source](https://doi.org/10.1109/isca66397.2026.00021) |
| 261 | DOI:10.1145/3642970.3655835 |  |  | 2 | 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1145/3642970.3655835) |
| 262 | DOI:10.1145/3772052.3772264 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3772052.3772264) |
| 263 | DOI:10.18653/v1/2023.emnlp-main.391 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.391) |
| 264 | DOI:10.18653/v1/2024.findings-acl.195 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.195) |
| 265 | DOI:10.18653/v1/2025.emnlp-main.844 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2025.emnlp-main.844) |
| 266 | DOI:10.5281/zenodo.1234 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://doi.org/10.5281/zenodo.1234) |
| 267 | OpenReview:9k27IITeAZ |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=9k27IITeAZ) |
| 268 | OpenReview:PxoFut3dWW |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=PxoFut3dWW) |
| 269 | OpenReview:SuYO70ZxZX |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=SuYO70ZxZX) |
| 270 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 271 | DOI:10.18653/v1/d19-1223 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/d19-1223) |
| 272 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 273 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 274 | OpenReview:OS5dqxmmtl |  |  | 2 |  | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 275 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 276 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 277 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 278 | arXiv:1312.6114 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 279 | arXiv:1404.5997 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1404.5997) |
| 280 | arXiv:1411.1792 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1411.1792) |
| 281 | arXiv:1506.02438 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 282 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 283 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 284 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 285 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 286 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 287 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 288 | arXiv:1606.06160 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 289 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 290 | arXiv:1611.01578 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 291 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 292 | arXiv:1703.03664 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1703.03664) |
| 293 | arXiv:1703.06114 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1703.06114) |
| 294 | arXiv:1704.04684 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/1704.04684) |
| 295 | arXiv:1704.05426 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 296 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 297 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 298 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 299 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 300 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 301 | arXiv:1710.09437 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1710.09437) |
| 302 | arXiv:1711.03936 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 303 | arXiv:1711.09224 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.09224) |
| 304 | arXiv:1712.05382 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.05382) |
| 305 | arXiv:1801.10198 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1801.10198) |
| 306 | arXiv:1802.05751 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1802.05751) |
| 307 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 308 | arXiv:1804.06087 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 309 | arXiv:1806.02847 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 310 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 311 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 312 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 313 | arXiv:1809.11096 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1809.11096) |
| 314 | arXiv:1810.03292 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1810.03292) |
| 315 | arXiv:1810.09868 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1810.09868) |
| 316 | arXiv:1811.05233 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 317 | arXiv:1812.06162 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1812.06162) |
| 318 | arXiv:1902.00751 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.00751) |
| 319 | arXiv:1902.08295 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1902.08295) |
| 320 | arXiv:1902.10186 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 321 | arXiv:1903.01699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 322 | arXiv:1904.01038 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1904.01038) |
| 323 | arXiv:1904.09675 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 324 | arXiv:1905.07129 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 325 | arXiv:1906.02041 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/1906.02041) |
| 326 | arXiv:1906.08172 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1906.08172) |
| 327 | arXiv:1907.01989 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1907.01989) |
| 328 | arXiv:1908.08593 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1908.08593) |
| 329 | arXiv:1908.11365 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1908.11365) |
| 330 | arXiv:1909.05803 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1909.05803) |
| 331 | arXiv:1909.11556 |  |  | 1 | speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 332 | arXiv:1910.04915 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1910.04915) |
| 333 | arXiv:1910.06360 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 334 | arXiv:1911.02116 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 335 | arXiv:1911.04997 |  |  | 1 | MoE expert parallelism / dynamic load balancing / expert prefetching | [source](https://arxiv.org/abs/1911.04997) |
| 336 | arXiv:1911.11313 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 337 | arXiv:2002.08155 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2002.08155) |
| 338 | arXiv:2002.10941 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2002.10941) |
| 339 | arXiv:2003.06713 |  |  | 1 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement | [source](https://arxiv.org/abs/2003.06713) |
| 340 | arXiv:2004.02984 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2004.02984) |
| 341 | arXiv:2004.08900 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 342 | arXiv:2004.11867 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 343 | arXiv:2005.00628 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 344 | arXiv:2005.03454 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 345 | arXiv:2005.14187 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 346 | arXiv:2006.10518 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 347 | arXiv:2006.12467 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 348 | arXiv:2007.07779 |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 349 | arXiv:2008.00051 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 350 | arXiv:2009.06106 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 351 | arXiv:2009.08034 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2009.08034) |
| 352 | arXiv:2009.09736 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2009.09736) |
| 353 | arXiv:2010.02394 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 354 | arXiv:2010.03379 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03379) |
| 355 | arXiv:2010.03983 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03983) |
| 356 | arXiv:2010.11443 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2010.11443) |
| 357 | arXiv:2011.02999 |  |  | 1 | 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://arxiv.org/abs/2011.02999) |
| 358 | arXiv:2011.06327 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2011.06327) |
| 359 | arXiv:2012.11346 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2012.11346) |
| 360 | arXiv:2012.15701 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2012.15701) |
| 361 | arXiv:2101.08744 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2101.08744) |
| 362 | arXiv:2102.02611 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2102.02611) |
| 363 | arXiv:2102.08124 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2102.08124) |
| 364 | arXiv:2102.11174 |  |  | 1 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2102.11174) |
| 365 | arXiv:2103.03330 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2103.03330) |
| 366 | arXiv:2104.06599 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2104.06599) |
| 367 | arXiv:2104.13478 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2104.13478) |
| 368 | arXiv:2105.06990 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2105.06990) |
| 369 | arXiv:2105.14450 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2105.14450) |
| 370 | arXiv:2106.03764 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2106.03764) |
| 371 | arXiv:2106.05974 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2106.05974) |
| 372 | arXiv:2106.10595 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2106.10595) |
| 373 | arXiv:2107.05407 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/2107.05407) |
| 374 | arXiv:2108.05036 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2108.05036) |
| 375 | arXiv:2109.00859 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2109.00859) |
| 376 | arXiv:2109.05472 |  |  | 1 | 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2109.05472) |
| 377 | arXiv:2109.10686 |  |  | 1 | 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2109.10686) |
| 378 | arXiv:2109.11817 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2109.11817) |
| 379 | arXiv:2110.06296 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2110.06296) |
| 380 | arXiv:2110.12894 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 381 | arXiv:2111.00160 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 382 | arXiv:2111.00856 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2111.00856) |
| 383 | arXiv:2112.02958 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2112.02958) |
| 384 | arXiv:2112.06749 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2112.06749) |
| 385 | arXiv:2112.14397 |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 386 | arXiv:2201.13425 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2201.13425) |
| 387 | arXiv:2202.05262 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2202.05262) |
| 388 | arXiv:2202.08791 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2202.08791) |
| 389 | arXiv:2202.13914 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.13914) |
| 390 | arXiv:2203.03131 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2203.03131) |
| 391 | arXiv:2203.06850 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2203.06850) |
| 392 | arXiv:2203.11014 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2203.11014) |
| 393 | arXiv:2204.05832 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2204.05832) |
| 394 | arXiv:2204.06683 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 395 | arXiv:2204.11574 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2204.11574) |
| 396 | arXiv:2205.04934 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2205.04934) |
| 397 | arXiv:2205.10364 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10364) |
| 398 | arXiv:2205.11916 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2205.11916) |
| 399 | arXiv:2205.13603 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2205.13603) |
| 400 | arXiv:2206.02845 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2206.02845) |
| 401 | arXiv:2207.05952 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 402 | arXiv:2207.10551 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2207.10551) |
| 403 | arXiv:2208.02813 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 404 | arXiv:2208.08227 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 405 | arXiv:2209.03143 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 406 | arXiv:2209.11429 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 407 | arXiv:2209.15352 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 408 | arXiv:2210.03057 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 409 | arXiv:2210.05709 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2210.05709) |
| 410 | arXiv:2210.08674 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2210.08674) |
| 411 | arXiv:2210.11948 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 412 | arXiv:2210.14793 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 413 | arXiv:2211.00593 |  |  | 1 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 414 | arXiv:2211.06033 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 415 | arXiv:2211.09699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 416 | arXiv:2211.15089 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 417 | arXiv:2212.00768 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.00768) |
| 418 | arXiv:2212.04088 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.04088) |
| 419 | arXiv:2212.05238 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.05238) |
| 420 | arXiv:2212.10325 |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2212.10325) |
| 421 | arXiv:2212.10509 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 422 | arXiv:2212.12017 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 423 | arXiv:2301.04104 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.04104) |
| 424 | arXiv:2301.06672 |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2301.06672) |
| 425 | arXiv:2301.08984 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2301.08984) |
| 426 | arXiv:2301.12503 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2301.12503) |
| 427 | arXiv:2302.02451 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.02451) |
| 428 | arXiv:2302.04863 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.04863) |
| 429 | arXiv:2302.09419 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.09419) |
| 430 | arXiv:2302.11529 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2302.11529) |
| 431 | arXiv:2302.12480 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.12480) |
| 432 | arXiv:2302.14502 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2302.14502) |
| 433 | arXiv:2303.02861 |  |  | 1 | 02-adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.02861) |
| 434 | arXiv:2303.06135 |  |  | 1 | fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2303.06135) |
| 435 | arXiv:2303.07129 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 436 | arXiv:2303.10512 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.10512) |
| 437 | arXiv:2303.13003 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2303.13003) |
| 438 | arXiv:2303.16199 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 439 | arXiv:2304.02017 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 440 | arXiv:2304.03208 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2304.03208) |
| 441 | arXiv:2304.04488 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2304.04488) |
| 442 | arXiv:2304.05332 |  |  | 1 | LLM inference kernel safety / CUDA symbolic execution / model-aware verification | [source](https://arxiv.org/abs/2304.05332) |
| 443 | arXiv:2304.08442 |  |  | 1 | MoE推論／エキスパート並列／エキスパート配置／全対全通信／負荷分散 | [source](https://arxiv.org/abs/2304.08442) |
| 444 | arXiv:2304.10411 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2304.10411) |
| 445 | arXiv:2304.12244 |  |  | 1 | multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 446 | arXiv:2304.15010 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 447 | arXiv:2305.02538 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 448 | arXiv:2305.04044 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2305.04044) |
| 449 | arXiv:2305.07622 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 450 | arXiv:2305.10010 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10010) |
| 451 | arXiv:2305.11860 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2305.11860) |
| 452 | arXiv:2305.13412 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2305.13412) |
| 453 | arXiv:2305.14160 |  |  | 1 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 454 | arXiv:2305.14516 |  |  | 1 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://arxiv.org/abs/2305.14516) |
| 455 | arXiv:2305.14952 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2305.14952) |
| 456 | arXiv:2305.15387 |  |  | 1 | KV cache compression / sparse attention / long-context inference | [source](https://arxiv.org/abs/2305.15387) |
| 457 | arXiv:2305.17126 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2305.17126) |
| 458 | arXiv:2305.18691 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.18691) |
| 459 | arXiv:2306.02003 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 460 | arXiv:2306.02896 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02896) |
| 461 | arXiv:2306.04933 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 462 | arXiv:2306.06624 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2306.06624) |
| 463 | arXiv:2306.09782 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.09782) |
| 464 | arXiv:2306.13596 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 465 | arXiv:2306.16636 |  |  | 1 | sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2306.16636) |
| 466 | arXiv:2307.01189 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.01189) |
| 467 | arXiv:2307.04251 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04251) |
| 468 | arXiv:2307.05300 |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2307.05300) |
| 469 | arXiv:2307.07697 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2307.07697) |
| 470 | arXiv:2307.08191 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2307.08191) |
| 471 | arXiv:2307.12169 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12169) |
| 472 | arXiv:2307.15043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.15043) |
| 473 | arXiv:2308.01285 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2308.01285) |
| 474 | arXiv:2308.03210 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2308.03210) |
| 475 | arXiv:2308.03958 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2308.03958) |
| 476 | arXiv:2308.06744 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2308.06744) |
| 477 | arXiv:2308.10502 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2308.10502) |
| 478 | arXiv:2308.11030 |  |  | 1 | cpu-offload | [source](https://arxiv.org/abs/2308.11030) |
| 479 | arXiv:2308.11761 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2308.11761) |
| 480 | arXiv:2308.15136 |  |  | 1 | KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval | [source](https://arxiv.org/abs/2308.15136) |
| 481 | arXiv:2309.01172 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2309.01172) |
| 482 | arXiv:2309.05135 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2309.05135) |
| 483 | arXiv:2309.07870 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2309.07870) |
| 484 | arXiv:2309.13345 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2309.13345) |
| 485 | arXiv:2309.16588 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.16588) |
| 486 | arXiv:2310.00726 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2310.00726) |
| 487 | arXiv:2310.01427 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2310.01427) |
| 488 | arXiv:2310.02255 |  |  | 1 | multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2310.02255) |
| 489 | arXiv:2310.03003 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2310.03003) |
| 490 | arXiv:2310.04064 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2310.04064) |
| 491 | arXiv:2310.04836 |  |  | 1 | 16-weight-quantization-compression | [source](https://arxiv.org/abs/2310.04836) |
| 492 | arXiv:2310.05209 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.05209) |
| 493 | arXiv:2310.05915 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.05915) |
| 494 | arXiv:2310.06625 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.06625) |
| 495 | arXiv:2310.07096 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.07096) |
| 496 | arXiv:2310.07999 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2310.07999) |
| 497 | arXiv:2310.09130 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.09130) |
| 498 | arXiv:2310.09478 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2310.09478) |
| 499 | arXiv:2310.10908 |  |  | 1 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2310.10908) |
| 500 | arXiv:2310.11703 |  |  | 1 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2310.11703) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

