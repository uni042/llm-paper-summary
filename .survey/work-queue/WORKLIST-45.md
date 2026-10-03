# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-03T02:01:36+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **623** / 未claim総数: **476** / このworker向け: **158**

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
| 30 | research | arXiv:2603.10087 | Pooling Engram Conditional Memory in Large Language Models using CXL | [primary](http://arxiv.org/abs/2603.10087) | `papers/inference/99-other-inference-systems/2026-2603.10087-pooling-engram-conditional-memory-in-large-language-models-using-cxl.md` |
| 31 | research | DOI:10.1109/2575-8411.2026.00035 | KV Cache Reuse for Elastic LLM Inference on Edge Devices | [primary](https://doi.org/10.1109/2575-8411.2026.00035) | `papers/inference/99-other-inference-systems/2020-2026.00035-kv-cache-reuse-for-elastic-llm-inference-on-edge-devices.md` |
| 32 | research | DOI:10.1145/3806645.3807596 | Scaling Attention Beyond GPUs for LLM Inference | [primary](https://www.semanticscholar.org/paper/04f3ee7dd762dff9b6aad25bfb930e1984f74a09) | `papers/inference/99-other-inference-systems/2026-c3c79f91845d-scaling-attention-beyond-gpus-for-llm-inference.md` |
| 33 | research | arXiv:2509.12993 | HPIM: Heterogeneous Processing-In-Memory-based Accelerator for Large Language Models Inference | [primary](https://arxiv.org/abs/2509.12993) | `papers/inference/99-other-inference-systems/2025-2509.12993-hpim-heterogeneous-pim-llm-inference.md` |
| 34 | research | DOI:10.1145/3770855.3817626 | OrionInfer: Low-Overhead Parallelism Switching and Live Migration for Efficient LLM Serving | [primary](https://doi.org/10.1145/3770855.3817626) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-orioninfer-parallelism-switching-live-migration.md` |
| 35 | research | arXiv:2609.06940 | Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management | [primary](https://www.semanticscholar.org/paper/4affda1dbe50475a3be782dcc62391802b20986e) | `papers/inference/99-other-inference-systems/2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-management.md` |
| 36 | research | arXiv:2609.22106 | PRQuant: Permutation Residual Quantization for Low-Overhead Inference | [primary](https://arxiv.org/abs/2609.22106) | `papers/inference/99-other-inference-systems/2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md` |
| 37 | research | arXiv:2608.22503 | Understanding the Synchronization Tax in GPU Scale-Up Domains | [primary](https://arxiv.org/abs/2608.22503) | `papers/inference/99-other-inference-systems/2026-2608.22503-understanding-the-synchronization-tax-in-gpu-scale-up-domains.md` |
| 38 | research | arXiv:2404.08763 |  | [primary](https://arxiv.org/abs/2404.08763) | `papers/inference/99-other-inference-systems/2024-2404.08763-paper.md` |
| 39 | research | arXiv:2608.11045 | ReRound: Reconstructive Rounding to Resolve Midpoint Ambiguity in Calibration-Free LLM Quantization | [primary](https://arxiv.org/abs/2608.11045) | `papers/inference/99-other-inference-systems/2026-2608.11045-reround-reconstructive-rounding-to-resolve-midpoint-ambiguity-in-calibration-free-llm-quantization.md` |
| 40 | research | DOI:10.1109/LCA.2026.3703982 | HBM-HBF-Centric Memory Pooling Architecture With Custom Base Die for Terabyte-Scale LLM Inference | [primary](https://ieeexplore.ieee.org/document/11568525/) | `papers/inference/99-other-inference-systems/2026-a21e1445aad5-hbm-hbf-centric-memory-pooling-architecture-with-custom-base-die-for-terabyte-scale-llm-inference.md` |
| 41 | research | arXiv:2608.23296 | Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction | [primary](https://www.semanticscholar.org/paper/097ed39586269776fb7418043e6af681a3676f0b) | `papers/inference/99-other-inference-systems/2026-2608.23296-sigmoid-attention-as-a-better-substrate-for-learned-kv-cache-eviction.md` |
| 42 | research | arXiv:2605.05696 | Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving | [primary](https://arxiv.org/abs/2605.05696) | `papers/inference/99-other-inference-systems/2026-2605.05696-irminsul-mla-native-position-independent-caching-for-agentic-llm-serving.md` |
| 43 | research | arXiv:1701.06538 | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | [primary](https://arxiv.org/abs/1701.06538) | `papers/inference/05-moe/2017-1701.06538-sparsely-gated-moe.md` |
| 44 | research | DOI:10.1109/ICWS72778.2026.00129 | QueueBreak: A Trace-to-Diagnosis Pipeline for Tail Latency in Agentic LLM Services | [primary](https://www.semanticscholar.org/paper/aa516e10879a6aa96b08ffd635832854788de3a5) | `papers/inference/99-other-inference-systems/2020-2026.00129-queuebreak-a-trace-to-diagnosis-pipeline-for-tail-latency-in-agentic-llm-services.md` |
| 45 | research | arXiv:2607.16100 | Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives | [primary](https://arxiv.org/abs/2607.16100) | `papers/inference/99-other-inference-systems/2026-2607.16100-every-microsecond-matters-near-speed-of-light-gpu-collectives.md` |
| 46 | research | arXiv:2605.14249 | EnergyLens: Predictive Energy-Aware Exploration for Multi-GPU LLM Inference Optimization | [primary](https://arxiv.org/abs/2605.14249) | `papers/inference/99-other-inference-systems/2026-2605.14249-energylens.md` |
| 47 | research | DOI:10.1016/j.compeleceng.2026.111505 | Component-aware self-speculative decoding for hybrid language models: An architectural viability study | [primary](https://doi.org/10.1016/j.compeleceng.2026.111505) | `papers/inference/99-other-inference-systems/2026-component-aware-self-speculative-decoding-hybrid-language-models.md` |
| 48 | research | arXiv:2412.14711 | ReMoE: Fully Differentiable Mixture-of-Experts with ReLU Routing | [primary](https://arxiv.org/abs/2412.14711) | `papers/inference/99-other-inference-systems/2024-2412.14711-remoe-fully-differentiable-mixture-of-experts-with-relu-routing.md` |
| 49 | research | arXiv:2606.21238 | Recency/Frequency Adaptive KV Caching for Large Language Model Serving | [primary](https://www.semanticscholar.org/paper/4634757f8c6adc509d5f919486320b78e8847787) | `papers/inference/99-other-inference-systems/2026-2606.21238-recency-frequency-adaptive-kv-caching-for-large-language-model-serving.md` |
| 50 | research | arXiv:2609.25916 | Beyond Scalar Sensitivity: Activation-Aware Mixed-Precision LLM Quantization with Cross-Layer Refinement | [primary](https://www.semanticscholar.org/paper/21bd7e3b09e4e1b7a72197bcca5e270539335449) | `papers/inference/99-other-inference-systems/2026-2609.25916-beyond-scalar-sensitivity-activation-aware-mixed-precision-llm-quantization-with-cross-layer-refinement.md` |
| 51 | research | arXiv:2609.25442 | WeightBridge: An Efficient Weight Transfer Library for Reinforcement Learning | [primary](https://arxiv.org/abs/2609.25442) | `papers/inference/99-other-inference-systems/2026-2609.25442-weightbridge-an-efficient-weight-transfer-library-for-reinforcement-learning.md` |
| 52 | research | arXiv:2409.17264 | No Request Left Behind: Tackling Heterogeneity in Long-Context LLM Inference with Medha | [primary](https://arxiv.org/abs/2409.17264) | `papers/inference/99-other-inference-systems/2024-2409.17264-no-request-left-behind-tackling-heterogeneity-in-long-context-llm-inference-with-medha.md` |
| 53 | research | doi:10.1145/3788106 | Towards Scalable Storage Architectures for GPU Clusters Running Large Language Models | [primary](https://doi.org/10.1145/3788106) | `papers/inference/99-other-inference-systems/2026-80288018997a-towards-scalable-storage-architectures-for-gpu-clusters-running-large-language-models.md` |
| 54 | research | arXiv:2603.02599 | SUN: Shared Use of Next-token Prediction for Efficient Multi-LLM Disaggregated Serving | [primary](https://arxiv.org/abs/2603.02599) | `papers/inference/99-other-inference-systems/2026-2603.02599-sun-shared-use-of-next-token-prediction-for-efficient-multi-llm-disaggregated-serving.md` |
| 55 | research | arXiv:2609.21672 | Accelerating Dense LLMs via L0-regularized Mixture-of-Experts | [primary](https://www.semanticscholar.org/paper/6a5dbd9fa51ed94d2de8cafc0ca37a8e39ef73a0) | `papers/inference/99-other-inference-systems/2026-2609.21672-accelerating-dense-llms-via-l0-regularized-mixture-of-experts.md` |
| 56 | research | arXiv:2502.07115 | Online Scheduling for LLM Inference with KV Cache Constraints | [primary](https://arxiv.org/abs/2502.07115) | `papers/inference/99-other-inference-systems/2025-2502.07115-online-scheduling-for-llm-inference-with-kv-cache-constraints.md` |
| 57 | research | arXiv:2510.12872 | KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems | [primary](https://www.semanticscholar.org/paper/471de4fab0885f45dffb717512741128775bcbaa) | `papers/inference/99-other-inference-systems/2025-2510.12872-kvcomm-online-cross-context-kv-cache-communication-for-efficient-llm-based-multi-agent-systems.md` |
| 58 | research | arXiv:2312.15234 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | [primary](https://arxiv.org/abs/2312.15234) | `papers/inference/99-other-inference-systems/2023-2312.15234-towards-efficient-generative-large-language-model-serving-a-survey-from-algorithms-to-systems.md` |
| 59 | audit | arXiv:2503.03777 | FlexInfer: Breaking Memory Constraint via Flexible and Efficient Offloading for On-Device LLM Inference | [primary](https://arxiv.org/abs/2503.03777) | `papers/inference/01-offload-hierarchical-memory/2025-2503.03777-flexinfer-flexible-efficient-on-device-offloading.md` |
| 60 | research | arXiv:2406.06858 | FLUX: Fast Software-based Communication Overlap On GPUs Through Kernel Fusion | [primary](https://arxiv.org/abs/2406.06858) | `papers/inference/99-other-inference-systems/2024-2406.06858-flux-fast-software-based-communication-overlap-on-gpus-through-kernel-fusion.md` |
| 61 | research | arXiv:2603.13605 | Orla: A Library for Serving LLM-Based Multi-Agent Systems | [primary](https://arxiv.org/abs/2603.13605) | `papers/inference/99-other-inference-systems/2026-2603.13605-orla-a-library-for-serving-llm-based-multi-agent-systems.md` |
| 62 | research | arXiv:2606.02982 | DriftSched: Adaptive QoS-Aware Scheduling under Runtime Token Drift for Multi-Tenant GPU Inference | [primary](https://arxiv.org/abs/2606.02982) | `papers/inference/99-other-inference-systems/2026-2606.02982-driftsched-adaptive-qos-aware-scheduling-under-runtime-token-drift-for-multi-tenant-gpu-inference.md` |
| 63 | research | arXiv:2609.08307 | A Measurement Study of LLM Inference Trade-offs Across Edge Continuum Hardware | [primary](https://arxiv.org/abs/2609.08307) | `papers/inference/99-other-inference-systems/2026-2609.08307-a-measurement-study-of-llm-inference-trade-offs-across-edge-continuum-hardware.md` |
| 64 | research | arXiv:2607.08215 | On the Limitations of Non-GPU AI Accelerators for Large-Model Inference: A Field Study of MoE and Multimodal Serving on Huawei Ascend | [primary](https://arxiv.org/abs/2607.08215) | `papers/inference/99-other-inference-systems/2026-2607.08215-on-the-limitations-of-non-gpu-ai-accelerators-for-large-model-inference-a-field-study-of-moe-and-multimodal-serving-on-h.md` |
| 65 | research | arXiv:2010.13887 | LightSeq: A High Performance Inference Library for Sequence Processing and Generation | [primary](https://arxiv.org/abs/2010.13887) | `papers/inference/99-other-inference-systems/2020-2010.13887-lightseq-a-high-performance-inference-library-for-sequence-processing-and-generation.md` |
| 66 | research | arXiv:2509.01229 | LiquidGEMM: Hardware-Efficient W4A8 GEMM Kernel for High-Performance LLM Serving | [primary](https://arxiv.org/abs/2509.01229) | `papers/inference/99-other-inference-systems/2025-2509.01229-liquidgemm-hardware-efficient-w4a8-gemm-kernel-for-high-performance-llm-serving.md` |
| 67 | research | arXiv:2604.16400 | CoLLM: Continuous Adaptation for SLO-Aware LLM Serving on Shared GPU Clusters | [primary](https://arxiv.org/abs/2604.16400) | `papers/inference/99-other-inference-systems/2026-2604.16400-collm-continuous-adaptation-for-slo-aware-llm-serving-on-shared-gpu-clusters.md` |
| 68 | research | arXiv:2406.14066 | TurboSpec: Closed-loop Speculation Control System for Optimizing LLM Serving Goodput | [primary](https://arxiv.org/abs/2406.14066) | `papers/inference/99-other-inference-systems/2024-2406.14066-turbospec-closed-loop-speculation-control-system-for-optimizing-llm-serving-goodput.md` |
| 69 | research | arXiv:2402.05109 | Hydra: Sequentially-Dependent Draft Heads for Medusa Decoding | [primary](https://arxiv.org/abs/2402.05109) | `papers/inference/99-other-inference-systems/2024-2402.05109-hydra-sequentially-dependent-draft-heads-for-medusa-decoding.md` |
| 70 | research | DOI:10.1145/3600006.3613157 | Mira: A Program-Behavior-Guided Far Memory System | [primary](https://doi.org/10.1145/3600006.3613157) | `papers/inference/99-other-inference-systems/2026-3a6cb9499537-mira-a-program-behavior-guided-far-memory-system.md` |
| 71 | research | arXiv:2210.12924 | OLLA: Optimizing the Lifetime and Location of Arrays to Reduce the Memory Usage of Neural Networks | [primary](https://arxiv.org/abs/2210.12924) | `papers/inference/99-other-inference-systems/2022-2210.12924-olla-optimizing-the-lifetime-and-location-of-arrays-to-reduce-the-memory-usage-of-neural-networks.md` |
| 72 | research | arXiv:2606.01387 | Fail-Closed Lowering of Resident KV Claims onto LLM Serving Runtimes | [primary](https://arxiv.org/abs/2606.01387) | `papers/inference/99-other-inference-systems/2026-2606.01387-fail-closed-lowering-of-resident-kv-claims-onto-llm-serving-runtimes.md` |
| 73 | research | arXiv:2609.23585 | Global Ranks Survive, Selected Heads Shift: BOS-Sink Topology under 4-bit Weight-Only Quantization | [primary](https://www.semanticscholar.org/paper/f992275cced1c153a71a0ad630ebbff2f1ddefa1) | `papers/inference/99-other-inference-systems/2026-2609.23585-global-ranks-survive-selected-heads-shift-bos-sink-topology-under-4-bit-weight-only-quantization.md` |
| 74 | research | arXiv:2308.13137 | OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models | [primary](https://arxiv.org/abs/2308.13137) | `papers/inference/99-other-inference-systems/2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-models.md` |
| 75 | research | arXiv:2101.06840 | ZeRO-Offload: Democratizing Billion-Scale Model Training | [primary](https://arxiv.org/abs/2101.06840) | `papers/inference/99-other-inference-systems/2021-2101.06840-zero-offload-democratizing-billion-scale-model-training.md` |
| 76 | research | DOI:10.1145/3606557.3606559 | Make It Real: An End-to-End Implementation of A Physically Disaggregated Data Center | [primary](https://doi.org/10.1145/3606557.3606559) | `papers/inference/99-other-inference-systems/0000-47de7e2f8a1f-make-it-real-an-end-to-end-implementation-of-a-physically-disaggregated-data-center.md` |
| 77 | research | arXiv:1712.05889 | Ray: A Distributed Framework for Emerging AI Applications | [primary](https://arxiv.org/abs/1712.05889) | `papers/inference/99-other-inference-systems/2017-1712.05889-ray-a-distributed-framework-for-emerging-ai-applications.md` |
| 78 | research | arXiv:2206.09557 | LUT-GEMM: Quantized Matrix Multiplication based on LUTs for Efficient Inference in Large-Scale Generative Language Models | [primary](https://arxiv.org/abs/2206.09557) | `papers/inference/99-other-inference-systems/2022-2206.09557-lut-gemm-quantized-matrix-multiplication-based-on-luts-for-efficient-inference-in-large-scale-generative-language-models.md` |
| 79 | research | arXiv:2509.18362 | FastMTP: Accelerating LLM Inference with Enhanced Multi-Token Prediction | [primary](https://arxiv.org/abs/2509.18362) | `papers/inference/99-other-inference-systems/2025-2509.18362-fastmtp-accelerating-llm-inference-with-enhanced-multi-token-prediction.md` |
| 80 | research | arXiv:2508.11661 | Sparse Attention across Multiple-context KV Cache | [primary](https://arxiv.org/abs/2508.11661) | `papers/inference/99-other-inference-systems/2025-2508.11661-sparse-attention-across-multiple-context-kv-cache.md` |
| 81 | research | arXiv:2503.00392 | Progressive Sparse Attention: Algorithm and System Co-design for Efficient Attention in LLM Serving | [primary](https://arxiv.org/abs/2503.00392) | `papers/inference/99-other-inference-systems/2025-2503.00392-progressive-sparse-attention-algorithm-and-system-co-design-for-efficient-attention-in-llm-serving.md` |
| 82 | research | arXiv:2503.05248 | Optimizing LLM Inference Throughput via Memory-aware and SLA-constrained Dynamic Batching | [primary](https://arxiv.org/abs/2503.05248) | `papers/inference/99-other-inference-systems/2025-2503.05248-optimizing-llm-inference-throughput-via-memory-aware-and-sla-constrained-dynamic-batching.md` |
| 83 | research | arXiv:2509.15940 | arXiv:2509.15940 | [primary](https://arxiv.org/abs/2509.15940) | `papers/inference/99-other-inference-systems/2025-2509.15940-arxiv-2509-15940.md` |
| 84 | research | arXiv:2602.22603 | SideQuest: Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning | [primary](https://arxiv.org/abs/2602.22603) | `papers/inference/99-other-inference-systems/2026-2602.22603-sidequest-model-driven-kv-cache-management-for-long-horizon-agentic-reasoning.md` |
| 85 | research | arXiv:2504.19519 | Efficient and Adaptable Overlapping for Computation and Communication via Signaling and Reordering | [primary](https://arxiv.org/abs/2504.19519) | `papers/inference/99-other-inference-systems/2025-2504.19519-efficient-and-adaptable-overlapping-for-computation-and-communication-via-signaling-and-reordering.md` |
| 86 | research | arXiv:2510.13602 | NOSA: Native and Offloadable Sparse Attention | [primary](https://arxiv.org/abs/2510.13602) | `papers/inference/99-other-inference-systems/2025-2510.13602-nosa-native-and-offloadable-sparse-attention.md` |
| 87 | research | arXiv:2509.09420 | HD-MoE: Hybrid and Dynamic Parallelism for Mixture-of-Expert LLMs with 3D Near-Memory Processing | [primary](https://arxiv.org/abs/2509.09420) | `papers/inference/99-other-inference-systems/2025-2509.09420-hd-moe-hybrid-and-dynamic-parallelism-for-mixture-of-expert-llms-with-3d-near-memory-processing.md` |
| 88 | research | arXiv:2604.22312 | Guess-Verify-Refine: Data-Aware Top-K for Sparse-Attention Decoding on Blackwell via Temporal Correlation | [primary](https://arxiv.org/abs/2604.22312) | `papers/inference/99-other-inference-systems/2026-2604.22312-guess-verify-refine-data-aware-top-k-for-sparse-attention-decoding-on-blackwell-via-temporal-correlation.md` |
| 89 | research | arXiv:2506.24045 | Agent.xpu: Efficient Scheduling of Agentic LLM Workloads on Heterogeneous SoC | [primary](https://arxiv.org/abs/2506.24045) | `papers/inference/99-other-inference-systems/2025-2506.24045-agent-xpu-efficient-scheduling-of-agentic-llm-workloads-on-heterogeneous-soc.md` |
| 90 | research | arXiv:2601.17668 | Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction | [primary](https://arxiv.org/abs/2601.17668) | `papers/inference/99-other-inference-systems/2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md` |
| 91 | research | DOI:10.13140/rg.2.2.28167.37282 | KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache | [primary](https://doi.org/10.13140/rg.2.2.28167.37282) | `papers/inference/99-other-inference-systems/0000-4a3b69939af0-kivi-a-tuning-free-asymmetric-2bit-quantization-for-kv-cache.md` |
| 92 | research | arXiv:2601.05524 | Double: Breaking the Acceleration Limit via Double Retrieval Speculative Parallelism | [primary](https://arxiv.org/abs/2601.05524) | `papers/inference/99-other-inference-systems/2026-2601.05524-double-breaking-the-acceleration-limit-via-double-retrieval-speculative-parallelism.md` |
| 93 | research | arXiv:2502.14051 | RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression | [primary](https://arxiv.org/abs/2502.14051) | `papers/inference/99-other-inference-systems/2025-2502.14051-rocketkv-accelerating-long-context-llm-inference-via-two-stage-kv-cache-compression.md` |
| 94 | research | arXiv:2602.03560 | HySparse: A Hybrid Sparse Attention Architecture with Oracle Token Selection and KV Cache Sharing | [primary](https://arxiv.org/abs/2602.03560) | `papers/inference/99-other-inference-systems/2026-2602.03560-hysparse-a-hybrid-sparse-attention-architecture-with-oracle-token-selection-and-kv-cache-sharing.md` |
| 95 | research | arXiv:2412.17246 | Fast and Live Model Auto Scaling with O(1) Host Caching | [primary](https://arxiv.org/abs/2412.17246) | `papers/inference/99-other-inference-systems/2024-2412.17246-fast-and-live-model-auto-scaling-with-o-1-host-caching.md` |
| 96 | research | arXiv:2310.06839 | LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression | [primary](https://arxiv.org/abs/2310.06839) | `papers/inference/99-other-inference-systems/2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-via-prompt-compression.md` |
| 97 | research | arXiv:2510.00615 | ACON: Optimizing Context Compression for Long-horizon LLM Agents | [primary](https://arxiv.org/abs/2510.00615) | `papers/inference/99-other-inference-systems/2025-2510.00615-acon-optimizing-context-compression-for-long-horizon-llm-agents.md` |
| 98 | research | arXiv:2110.03888 | M6-10T: A Sharing-Delinking Paradigm for Efficient Multi-Trillion Parameter Pretraining | [primary](https://arxiv.org/abs/2110.03888) | `papers/inference/99-other-inference-systems/2021-2110.03888-m6-10t-a-sharing-delinking-paradigm-for-efficient-multi-trillion-parameter-pretraining.md` |
| 99 | research | arXiv:2602.16284 | Fast KV Compaction via Attention Matching | [primary](https://arxiv.org/abs/2602.16284) | `papers/inference/99-other-inference-systems/2026-2602.16284-fast-kv-compaction-via-attention-matching.md` |
| 100 | research | DOI:10.1145/3600006.3613145 | GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints | [primary](https://doi.org/10.1145/3600006.3613145) | `papers/inference/99-other-inference-systems/0000-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-checkpoints.md` |
| 101 | research | arXiv:2006.09616 | Dynamic Tensor Rematerialization | [primary](https://arxiv.org/abs/2006.09616) | `papers/inference/99-other-inference-systems/2020-2006.09616-dynamic-tensor-rematerialization.md` |
| 102 | research | arXiv:2110.15032 | OneFlow: Redesign the Distributed Deep Learning Framework from Scratch | [primary](https://arxiv.org/abs/2110.15032) | `papers/inference/99-other-inference-systems/2021-2110.15032-oneflow-redesign-the-distributed-deep-learning-framework-from-scratch.md` |
| 103 | research | DOI:10.1145/3731569.3764834 | PrefillOnly: An Inference Engine for Prefill-only Workloads in Large Language Model Applications | [primary](https://doi.org/10.1145/3731569.3764834) | `papers/inference/99-other-inference-systems/0000-cc54e0b027f8-prefillonly-an-inference-engine-for-prefill-only-workloads-in-large-language-model-applications.md` |
| 104 | research | arXiv:2411.01783 | Context Parallelism for Scalable Million-Token Inference | [primary](https://arxiv.org/abs/2411.01783) | `papers/inference/99-other-inference-systems/2024-2411.01783-context-parallelism-for-scalable-million-token-inference.md` |
| 105 | research | arXiv:2510.02758 | TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling | [primary](https://arxiv.org/abs/2510.02758) | `papers/inference/99-other-inference-systems/2025-2510.02758-tokenflow-responsive-llm-text-streaming-serving-under-request-burst-via-preemptive-scheduling.md` |
| 106 | research | arXiv:2606.13054 | TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization | [primary](https://arxiv.org/abs/2606.13054) | `papers/inference/99-other-inference-systems/2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post-training-quantization.md` |
| 107 | research | arXiv:2507.15465 | The New LLM Bottleneck: A Systems Perspective on Latent Attention and Mixture-of-Experts | [primary](https://arxiv.org/abs/2507.15465) | `papers/inference/99-other-inference-systems/2025-2507.15465-the-new-llm-bottleneck-a-systems-perspective-on-latent-attention-and-mixture-of-experts.md` |
| 108 | research | arXiv:2408.01803 | STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs | [primary](https://arxiv.org/abs/2408.01803) | `papers/inference/99-other-inference-systems/2024-2408.01803-stbllm-breaking-the-1-bit-barrier-with-structured-binary-llms.md` |
| 109 | research | arXiv:2604.11035 | Introspective Diffusion Language Models | [primary](https://arxiv.org/abs/2604.11035) | `papers/inference/99-other-inference-systems/2026-2604.11035-introspective-diffusion-language-models.md` |
| 110 | research | DOI:10.1109/isca59077.2024.00082 | LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference | [primary](https://doi.org/10.1109/isca59077.2024.00082) | `papers/inference/99-other-inference-systems/0000-6daecc086891-llmcompass-enabling-efficient-hardware-design-for-large-language-model-inference.md` |
| 111 | research | arXiv:2505.24298 | AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning | [primary](https://arxiv.org/abs/2505.24298) | `papers/inference/99-other-inference-systems/2025-2505.24298-areal-a-large-scale-asynchronous-reinforcement-learning-system-for-language-reasoning.md` |
| 112 | research | DOI:10.1145/3620666.3651380 | NeuPIMs: NPU-PIM Heterogeneous Acceleration for Batched LLM Inferencing | [primary](https://doi.org/10.1145/3620666.3651380) | `papers/inference/99-other-inference-systems/0000-53abd3a104f5-neupims-npu-pim-heterogeneous-acceleration-for-batched-llm-inferencing.md` |
| 113 | research | arXiv:1802.05799 | Horovod: fast and easy distributed deep learning in TensorFlow | [primary](https://arxiv.org/abs/1802.05799) | `papers/inference/99-other-inference-systems/2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md` |
| 114 | research | arXiv:2104.04473 | Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM | [primary](https://arxiv.org/abs/2104.04473) | `papers/inference/99-other-inference-systems/2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-megatron-lm.md` |
| 115 | research | arXiv:2411.01288 | Hexa-MoE: Efficient and Heterogeneous-aware Training for Mixture-of-Experts | [primary](https://arxiv.org/abs/2411.01288) | `papers/inference/99-other-inference-systems/2024-2411.01288-hexa-moe-efficient-and-heterogeneous-aware-training-for-mixture-of-experts.md` |
| 116 | research | arXiv:2206.03382 | Tutel: Adaptive Mixture-of-Experts at Scale | [primary](https://arxiv.org/abs/2206.03382) | `papers/inference/99-other-inference-systems/2022-2206.03382-tutel-adaptive-mixture-of-experts-at-scale.md` |
| 117 | research | arXiv:2307.06945 | In-context Autoencoder for Context Compression in a Large Language Model | [primary](https://arxiv.org/abs/2307.06945) | `papers/inference/99-other-inference-systems/2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md` |
| 118 | research | arXiv:2403.05821 | Optimizing LLM Queries in Relational Data Analytics Workloads | [primary](https://arxiv.org/abs/2403.05821) | `papers/inference/99-other-inference-systems/2024-2403.05821-optimizing-llm-queries-in-relational-data-analytics-workloads.md` |
| 119 | research | arXiv:2507.19635 | Efficient and Scalable Agentic AI with Heterogeneous Systems | [primary](https://arxiv.org/abs/2507.19635) | `papers/inference/99-other-inference-systems/2025-2507.19635-efficient-and-scalable-agentic-ai-with-heterogeneous-systems.md` |
| 120 | research | arXiv:2203.16487 | Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation | [primary](https://arxiv.org/abs/2203.16487) | `papers/inference/99-other-inference-systems/2022-2203.16487-speculative-decoding-exploiting-speculative-execution-for-accelerating-seq2seq-generation.md` |
| 121 | research | arXiv:2403.09919 | Recurrent Drafter for Fast Speculative Decoding in Large Language Models | [primary](https://arxiv.org/abs/2403.09919) | `papers/inference/99-other-inference-systems/2024-2403.09919-recurrent-drafter-for-fast-speculative-decoding-in-large-language-models.md` |
| 122 | research | arXiv:2510.14973 | Attention Is All You Need for KV Cache in Diffusion LLMs | [primary](https://arxiv.org/abs/2510.14973) | `papers/inference/99-other-inference-systems/2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md` |
| 123 | research | arXiv:2506.07530 | BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation | [primary](https://arxiv.org/abs/2506.07530) | `papers/inference/99-other-inference-systems/2025-2506.07530-bitvla-1-bit-vision-language-action-models-for-robotics-manipulation.md` |
| 124 | research | arXiv:2504.08378 | Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash | [primary](https://arxiv.org/abs/2504.08378) | `papers/inference/99-other-inference-systems/2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-flash.md` |
| 125 | research | arXiv:2410.14731 | MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection | [primary](https://arxiv.org/abs/2410.14731) | `papers/inference/99-other-inference-systems/2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md` |
| 126 | research | arXiv:2510.27656 | fabric-lib: RDMA Point-to-Point Communication for LLM Systems | [primary](https://arxiv.org/abs/2510.27656) | `papers/inference/99-other-inference-systems/2025-2510.27656-fabric-lib-rdma-point-to-point-communication-for-llm-systems.md` |
| 127 | research | arXiv:2507.08143 | Compactor: Calibrated Query-Agnostic KV Cache Compression with Approximate Leverage Scores | [primary](https://arxiv.org/abs/2507.08143) | `papers/inference/99-other-inference-systems/2025-2507.08143-compactor-calibrated-query-agnostic-kv-cache-compression-with-approximate-leverage-scores.md` |
| 128 | research | arXiv:2302.08007 | With Shared Microexponents, A Little Shifting Goes a Long Way | [primary](https://arxiv.org/abs/2302.08007) | `papers/inference/99-other-inference-systems/2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md` |
| 129 | research | arXiv:2402.10517 | Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs | [primary](https://arxiv.org/abs/2402.10517) | `papers/inference/99-other-inference-systems/2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md` |
| 130 | research | arXiv:2609.38090 | Mira: Memory-Efficient MoE Inference Using Adaptive Caching and Predictive Expert Staging | [primary](https://arxiv.org/abs/2609.38090) | `papers/inference/99-other-inference-systems/2026-2609.38090-mira-memory-efficient-moe-inference-using-adaptive-caching-and-predictive-expert-staging.md` |
| 131 | research | arXiv:2410.04199 | LongGenBench: Long-context Generation Benchmark | [primary](https://arxiv.org/abs/2410.04199) | `papers/inference/99-other-inference-systems/2024-2410.04199-longgenbench-long-context-generation-benchmark.md` |
| 132 | research | arXiv:2412.04964 | Flash Communication: Reducing Tensor Parallelization Bottleneck for Fast Large Language Model Inference | [primary](https://arxiv.org/abs/2412.04964) | `papers/inference/99-other-inference-systems/2024-2412.04964-flash-communication-reducing-tensor-parallelization-bottleneck-for-fast-large-language-model-inference.md` |
| 133 | research | arXiv:2412.03213 | ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression | [primary](https://arxiv.org/abs/2412.03213) | `papers/inference/99-other-inference-systems/2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-compression.md` |
| 134 | research | DOI:10.1145/3772052.3772264 | Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment | [primary](https://doi.org/10.1145/3772052.3772264) | `papers/inference/99-other-inference-systems/2025-6987e5a4e5ec-cauchy-a-cost-efficient-llm-serving-system-through-adaptive-heterogeneous-deployment.md` |
| 135 | research | arXiv:2603.13606 | NCCL EP: Towards a Unified Expert Parallel Communication API for NCCL | [primary](https://arxiv.org/abs/2603.13606) | `papers/inference/99-other-inference-systems/2026-2603.13606-nccl-ep-towards-a-unified-expert-parallel-communication-api-for-nccl.md` |
| 136 | research | arXiv:2412.00876 | Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification | [primary](https://arxiv.org/abs/2412.00876) | `papers/inference/99-other-inference-systems/2024-2412.00876-dynamic-llava-efficient-multimodal-large-language-models-via-dynamic-vision-language-context-sparsification.md` |
| 137 | research | DOI:10.1145/3779212.3790246 | SwiftSpec: Disaggregated Speculative Decoding and Fused Kernels for Low-Latency LLM Inference | [primary](https://doi.org/10.1145/3779212.3790246) | `papers/inference/99-other-inference-systems/2026-92272744585e-swiftspec-disaggregated-speculative-decoding-and-fused-kernels-for-low-latency-llm-inference.md` |
| 138 | research | arXiv:2609.22157 | PAGE: Partition-Aware Gated KV-Cache Eviction | [primary](https://arxiv.org/abs/2609.22157) | `papers/inference/99-other-inference-systems/2026-2609.22157-page-partition-aware-gated-kv-cache-eviction.md` |
| 139 | research | arXiv:2309.09507 | Pruning Large Language Models via Accuracy Predictor | [primary](https://arxiv.org/abs/2309.09507) | `papers/inference/99-other-inference-systems/2023-2309.09507-pruning-large-language-models-via-accuracy-predictor.md` |
| 140 | research | arXiv:2307.08045 | Beyond Classical Attention: Quantum Attention for Scalable Computation | [primary](https://arxiv.org/abs/2307.08045) | `papers/inference/99-other-inference-systems/2023-2307.08045-beyond-classical-attention-quantum-attention-for-scalable-computation.md` |
| 141 | research | arXiv:2502.00722 | Demystifying Cost-Efficiency in LLM Serving over Heterogeneous GPUs | [primary](https://arxiv.org/abs/2502.00722) | `papers/inference/99-other-inference-systems/2025-2502.00722-demystifying-cost-efficiency-in-llm-serving-over-heterogeneous-gpus.md` |
| 142 | research | arXiv:2608.02515 | LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference | [primary](https://arxiv.org/abs/2608.02515) | `papers/inference/99-other-inference-systems/2026-2608.02515-livemem-maintaining-memory-state-continuity-in-long-running-llm-inference.md` |
| 143 | research | arXiv:2608.20530 | LiLiCorr: Lightweight Likelihood Correlation of Parallel Drafts for Speculative Decoding | [primary](https://arxiv.org/abs/2608.20530) | `papers/inference/99-other-inference-systems/2026-2608.20530-lilicorr-lightweight-likelihood-correlation-of-parallel-drafts-for-speculative-decoding.md` |
| 144 | research | arXiv:2609.24197 | H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache | [primary](https://arxiv.org/abs/2609.24197) | `papers/inference/99-other-inference-systems/2026-2609.24197-h-spec-parallel-speculative-decoding-without-a-drafter-side-kv-cache.md` |
| 145 | research | arXiv:2402.12065 | WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More | [primary](https://arxiv.org/abs/2402.12065) | `papers/inference/99-other-inference-systems/2024-2402.12065-wkvquant-quantizing-weight-and-key-value-cache-for-large-language-models-gains-more.md` |
| 146 | research | arXiv:2312.05821 | ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models | [primary](https://arxiv.org/abs/2312.05821) | `papers/inference/99-other-inference-systems/2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large-language-models.md` |
| 147 | research | arXiv:2307.02486 | LongNet: Scaling Transformers to 1, 000, 000, 000 Tokens | [primary](https://arxiv.org/abs/2307.02486) | `papers/inference/99-other-inference-systems/2023-2307.02486-longnet-scaling-transformers-to-1-000-000-000-tokens.md` |
| 148 | research | arXiv:2503.09573 | BLOCK DIFFUSION: INTERPOLATING BETWEEN AU-TOREGRESSIVE AND DIFFUSION LANGUAGE MODELS | [primary](https://arxiv.org/abs/2503.09573) | `papers/inference/99-other-inference-systems/2025-2503.09573-block-diffusion-interpolating-between-au-toregressive-and-diffusion-language-models.md` |
| 149 | research | DOI:10.1109/TPDS.2025.3590014 | Cannikin: No Lagger of SLO in Concurrent Multiple LoRA LLM Serving | [primary](https://doi.org/10.1109/TPDS.2025.3590014) | `papers/inference/99-other-inference-systems/2025-fa2b92104549-cannikin-no-lagger-of-slo-in-concurrent-multiple-lora-llm-serving.md` |
| 150 | research | arXiv:2505.24133 | R-KV: Redundancy-aware KV Cache Compression for Reasoning Models | [primary](https://arxiv.org/abs/2505.24133) | `papers/inference/99-other-inference-systems/2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md` |
| 151 | research | arXiv:2601.04719 | GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models | [primary](https://arxiv.org/abs/2601.04719) | `papers/inference/99-other-inference-systems/2026-2601.04719-gpu-accelerated-int8-quantization-for-kv-cache-compression-in-large-language-models.md` |
| 152 | research | arXiv:2404.00242 | DeFT: Decoding with Flash Tree-attention for Efficient Tree-structured LLM Inference | [primary](https://arxiv.org/abs/2404.00242) | `papers/inference/99-other-inference-systems/2024-2404.00242-deft-decoding-with-flash-tree-attention-for-efficient-tree-structured-llm-inference.md` |
| 153 | research | arXiv:2609.30854 | The KV Cache Is the New Memory Wall | [primary](https://arxiv.org/abs/2609.30854) | `papers/inference/99-other-inference-systems/2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md` |
| 154 | research | arXiv:2609.31395 | ActKV: Efficient LLM Agents through Action-Guided KV Cache Management | [primary](https://arxiv.org/abs/2609.31395) | `papers/inference/99-other-inference-systems/2026-2609.31395-actkv-efficient-llm-agents-through-action-guided-kv-cache-management.md` |
| 155 | research | arXiv:2603.07904 | DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models | [primary](https://arxiv.org/abs/2603.07904) | `papers/inference/99-other-inference-systems/2026-2603.07904-dyq-vla-temporal-dynamic-aware-quantization-for-embodied-vision-language-action-models.md` |
| 156 | research | arXiv:2602.15763 | GLM-5: from Vibe Coding to Agentic Engineering | [primary](https://arxiv.org/abs/2602.15763) | `papers/inference/99-other-inference-systems/2026-2602.15763-glm-5-from-vibe-coding-to-agentic-engineering.md` |
| 157 | research | arXiv:2412.06464 | Gated Delta Networks: Improving Mamba2 with Delta Rule | [primary](https://arxiv.org/abs/2412.06464) | `papers/inference/99-other-inference-systems/2024-2412.06464-gated-delta-networks-improving-mamba2-with-delta-rule.md` |
| 158 | research | DOI:10.1145/3552326.3587438 | Tabi: An Efficient Multi-Level Inference System for Large Language Models | [primary](https://doi.org/10.1145/3552326.3587438) | `papers/inference/99-other-inference-systems/2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5372** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3458817.3476209 |  |  | 14 | Conditional Computation, GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, distributed LLM inference / communication-aware serving, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-offload-routing, other-inference-systems, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime, オフロード／階層メモリ | [source](https://doi.org/10.1145/3458817.3476209) |
| 2 | arXiv:2312.04985 |  |  | 12 | KV cache compression / sparse attention / long-context inference, KV cache quantization / long-context inference / activation compression, Offload / Hierarchical Memory, Sparse Attention, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2312.04985) |
| 3 | arXiv:2601.03267 |  |  | 11 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, 投機的デコードにおける自己回帰ドラフトと並列ドラフトの折衷, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2601.03267) |
| 4 | OpenReview:cFu7ze7xUm |  |  | 11 | 13-sparse-attention, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, other-inference-systems | [source](https://openreview.net/forum?id=cFu7ze7xUm) |
| 5 | arXiv:2407.12820 |  |  | 10 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://arxiv.org/abs/2407.12820) |
| 6 | arXiv:2506.12708 |  |  | 10 | 12-moe-parallelism-communication, KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, MoE serving / attention-MoE disaggregation / asynchronous inference, chunked-prefill scheduling / fairness / latency control, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2506.12708) |
| 7 | DOI:10.18653/v1/2024.acl-long.623 |  |  | 9 | 02-hardware-accelerators, 14-agentic-inference-serving-runtime, KV Cache Offload / Recomputation, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Offload / Hierarchical Memory, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, llm-serving-scheduling-disaggregation, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.18653/v1/2024.acl-long.623) |
| 8 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 9 | arXiv:2405.16406 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 17-pim-near-data-acceleration, FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV cache quantization / rotation-based compression / MoE expert offloading / consumer local inference, kv-cache-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2405.16406) |
| 10 | arXiv:1910.01108 |  |  | 8 | LLM Serving / Scheduling / Disaggregation, LLMサービング／予測型スケジューリング, Speculative Decoding, dense-to-MoE conversion / conditional FFN computation / expert routing, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 投機的デコード / 分布保存型デコード高速化, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1910.01108) |
| 11 | arXiv:2409.06669 |  |  | 8 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, Quantization × MoE × Offload, Speculative decoding × MoE, adaptive expert computation / dynamic MoE routing / expert sparsification, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2409.06669) |
| 12 | arXiv:2402.17764 |  |  | 8 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline, offload-hierarchical-memory, post-training quantization / ternary LLM / packed inference, survey-distributed-training-systems, survey-low-bit-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.17764) |
| 13 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 14 | arXiv:2512.20856 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, PIM / Near-Data Acceleration, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2512.20856) |
| 15 | DOI:10.64434/tml.20250910 |  |  | 8 | Agentic Serving Benchmarking, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 16 | DOI:10.1145/3772052.3772239 |  |  | 8 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation, multi-SLO serving / speculative decoding / SLO-aware scheduling / hardware-aware token budgeting, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://doi.org/10.1145/3772052.3772239) |
| 17 | DOI:10.1145/3394486.3406703 |  |  | 8 | GPU collective communication / communication compression / LLM serving disaggregation, KVキャッシュ再利用／圧縮／ネットワーク転送, kernel-runtime-compilation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3394486.3406703) |
| 18 | arXiv:2401.00625 |  |  | 7 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, System-aware KV cache, distributed LLM inference / communication-aware serving, llm-serving-systems, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.00625) |
| 19 | DOI:10.5281/zenodo.10256836 |  |  | 7 | Adaptive Expert Computation / Compression, Conditional Computation, Expert Prefetch, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation, 投機復号・自己投機・ループ型Transformer・推論パイプライン, 投機的復号・Orthrus・推論再現性・数値精度 | [source](https://doi.org/10.5281/zenodo.10256836) |
| 20 | arXiv:2101.00190 |  |  | 7 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2101.00190) |
| 21 | arXiv:2503.20215 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, batch inference / event-driven runtime / MoE serving / offload, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2503.20215) |
| 22 | OpenReview:wHBfxhZu1u |  |  | 7 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-optimization-compression, other-inference-systems, 投機的復号 / LLMサービング・ベンチマーク | [source](https://openreview.net/forum?id=wHBfxhZu1u) |
| 23 | arXiv:2407.21118 |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2407.21118) |
| 24 | DOI:10.1145/3711896.3737413 |  |  | 7 | LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3711896.3737413) |
| 25 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 26 | DOI:10.48550/arxiv.2407.12391 |  |  | 6 | SLO-aware LLM serving scheduling, System-aware KV cache, disaggregated LLM serving / request routing / learned scheduling, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://doi.org/10.48550/arxiv.2407.12391) |
| 27 | arXiv:2306.09212 |  |  | 6 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2306.09212) |
| 28 | arXiv:2511.21631 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / dynamic MoE routing / gating uncertainty, flash-capacity-tier-inference | [source](https://arxiv.org/abs/2511.21631) |
| 29 | arXiv:2303.08302 |  |  | 6 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Weight Quantization / Compression, offload-hierarchical-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2303.08302) |
| 30 | arXiv:2412.10302 |  |  | 6 | Adaptive computation／cache-aware MoE, MoE compression / training-free expert merging / multimodal MoE routing, Quantization × MoE × Offload, adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2412.10302) |
| 31 | DOI:10.1109/ispass57527.2023.00035 |  |  | 6 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass57527.2023.00035) |
| 32 | OpenReview:7Bywt2mQsCe |  |  | 6 | KV Cache Optimization / Compression, Speculative decoding × MoE, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Bywt2mQsCe) |
| 33 | arXiv:2504.09285 |  |  | 6 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.09285) |
| 34 | OpenReview:mZn2Xyh9Ec |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=mZn2Xyh9Ec) |
| 35 | arXiv:2001.09977 |  |  | 5 | LLM Serving / Scheduling / Disaggregation, cross-layer LLM serving / SLO-aware scheduling / predictive routing / heterogeneous inference, serving-scheduling, speculative decoding / LLM serving / adaptive scheduling, その他システム研究 | [source](https://arxiv.org/abs/2001.09977) |
| 36 | arXiv:2503.12491 |  |  | 5 | KV Cache Offload / Recomputation, KV Cache Optimization / Compression, KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2503.12491) |
| 37 | DOI:10.1145/3620666.3651329 |  |  | 5 | KV Cache Offload / Recomputation, MoE推論／CPU-GPU協調オフロード／階層メモリ／性能モデル／高スループットバッチ推論, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3620666.3651329) |
| 38 | DOI:10.18653/v1/d16-1264 |  |  | 5 | 07-kv-cache-optimization-compression, Adaptive Expert Computation / Compression, adaptive-expert-computation-compression, kv-cache-optimization-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.18653/v1/d16-1264) |
| 39 | arXiv:2110.04260 |  |  | 5 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference systems / expert parallelism / model compression / knowledge distillation, Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2110.04260) |
| 40 | arXiv:2306.06000 |  |  | 5 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, SLO-aware LLM serving / chunked prefill / multi-resource scheduling, SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2306.06000) |
| 41 | DOI:10.18653/v1/k16-1028 |  |  | 5 | Speculative decoding × MoE, survey-speculative-decoding, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/k16-1028) |
| 42 | OpenReview:xXTkbTBmqq |  |  | 5 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分, Quantization × MoE × Offload, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=xXTkbTBmqq) |
| 43 | arXiv:2403.12031 |  |  | 5 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 44 | arXiv:2504.19516 |  |  | 5 | llm-serving-scheduling-disaggregation, serving-scheduling, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.19516) |
| 45 | OpenReview:KzACYw0MTV |  |  | 5 | 10-kv-キャッシュ-オフロード-recomputation, Prefill/Decode Disaggregation / Selective KV Transfer, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=KzACYw0MTV) |
| 46 | DOI:10.1145/3725843.3756062 |  |  | 5 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3725843.3756062) |
| 47 | OpenReview:EytBpUGB1Z |  |  | 5 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=EytBpUGB1Z) |
| 48 | arXiv:2108.12409 |  |  | 4 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLM inference surveys、roofline performance analysis, cpu-offload, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2108.12409) |
| 49 | arXiv:2309.01885 |  |  | 4 | 16-weight-quantization-compression, LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.01885) |
| 50 | arXiv:2412.16434 |  |  | 4 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation, other-inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2412.16434) |
| 51 | DOI:10.1145/3620666.3651352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 52 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 53 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 54 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 55 | arXiv:2203.08913 |  |  | 4 | LLM inference surveys、roofline performance analysis, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 56 | OpenReview:cSimKw5p6R |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, agentic workflow serving / workflow physical planning / adaptive serving, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://openreview.net/forum?id=cSimKw5p6R) |
| 57 | arXiv:2402.18013 |  |  | 4 | llm-serving-scheduling-disaggregation, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2402.18013) |
| 58 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 59 | arXiv:2402.02244 |  |  | 3 | LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 60 | arXiv:2503.08311 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2503.08311) |
| 61 | arXiv:2512.22420 |  |  | 3 | llm-serving-scheduling-disaggregation, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2512.22420) |
| 62 | DOI:10.1109/hoti.2015.13 |  |  | 3 | KVキャッシュオフロード・再計算, RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/hoti.2015.13) |
| 63 | DOI:10.1109/lca.2025.3628325 |  |  | 3 | 12-benchmarking-modeling-emulation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, other-inference-systems | [source](https://doi.org/10.1109/lca.2025.3628325) |
| 64 | DOI:10.1109/sc41405.2020.00024 |  |  | 3 | Adaptive computation／cache-aware MoE, その他システム研究, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/sc41405.2020.00024) |
| 65 | DOI:10.1145/1534530.1534544 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, offload-hierarchical-memory, オフロード／階層メモリ | [source](https://doi.org/10.1145/1534530.1534544) |
| 66 | DOI:10.1145/3620666.3651379 |  |  | 3 | kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 67 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 68 | DOI:10.1145/3731569.3764813 |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764813) |
| 69 | DOI:10.48550/arxiv.2507.17702 |  |  | 3 | adaptive expert computation / compression; end-side sparse MoE, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://doi.org/10.48550/arxiv.2507.17702) |
| 70 | OpenReview:1qvx610Cu7 |  |  | 3 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 71 | OpenReview:c8McWs4Av0 |  |  | 3 | Adaptive Expert Computation / Compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=c8McWs4Av0) |
| 72 | OpenReview:LywifFNXV5 |  |  | 3 | CPU長文推論・近似注意, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://openreview.net/forum?id=LywifFNXV5) |
| 73 | OpenReview:TrjbxzRcnf- |  |  | 3 | KVキャッシュ・注意アーキテクチャ, KVキャッシュ再利用／圧縮／ネットワーク転送, other-inference-systems | [source](https://openreview.net/forum?id=TrjbxzRcnf-) |
| 74 | OpenReview:z3JZzu9EA3 |  |  | 3 | KV Cache Optimization / Compression, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=z3JZzu9EA3) |
| 75 | arXiv:2409.02813 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2409.02813) |
| 76 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 77 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 78 | DOI:10.1145/3581784.3607062 |  |  | 3 | Sparse Attention, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1145/3581784.3607062) |
| 79 | DOI:10.1145/3719330.3721230 |  |  | 3 | 08-edge-on-device-llm-systems, KV Cache Offload / Recomputation | [source](https://doi.org/10.1145/3719330.3721230) |
| 80 | DOI:10.1162/tacl%5fa%5f00276 |  |  | 3 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://doi.org/10.1162/tacl%5fa%5f00276) |
| 81 | DOI:10.18653/v1/2024.acl-long.814 |  |  | 3 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.814) |
| 82 | DOI:10.48550/arxiv.2409.12136 |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2409.12136) |
| 83 | OpenReview:ayi7qezU87 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://openreview.net/forum?id=ayi7qezU87) |
| 84 | OpenReview:LKEJPySnlt |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=LKEJPySnlt) |
| 85 | OpenReview:rJ4km2R5t7 |  |  | 3 | MoE inference / task-specific expert pruning / sparse-to-dense conversion, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rJ4km2R5t7) |
| 86 | OpenReview:ul4W26KEKz |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://openreview.net/forum?id=ul4W26KEKz) |
| 87 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 88 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 89 | arXiv:1412.7024 |  |  | 2 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 90 | arXiv:2011.01060 |  |  | 2 | kv-cache-offload-recomputation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification | [source](https://arxiv.org/abs/2011.01060) |
| 91 | arXiv:2212.01378 |  |  | 2 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2212.01378) |
| 92 | arXiv:2306.02272 |  |  | 2 | LLM inference surveys、roofline performance analysis, Weight Quantization / Compression | [source](https://arxiv.org/abs/2306.02272) |
| 93 | arXiv:2306.04050 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 94 | arXiv:2307.04964 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2307.04964) |
| 95 | arXiv:2308.06093 |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 96 | arXiv:2308.12908 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2308.12908) |
| 97 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 98 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 99 | arXiv:2309.14393 |  |  | 2 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 100 | arXiv:2310.01655 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2310.01655) |
| 101 | arXiv:2310.05424 |  |  | 2 | speculative decoding / draft-model design, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2310.05424) |
| 102 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 103 | arXiv:2311.09550 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 104 | arXiv:2311.13171 |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 105 | arXiv:2312.00678 |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 106 | arXiv:2312.04916 |  |  | 2 | early-exit-offloading-self-speculative-decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 107 | arXiv:2312.13558 |  |  | 2 | LLM inference surveys、roofline performance analysis, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 108 | arXiv:2401.02038 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 109 | arXiv:2401.07339 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.07339) |
| 110 | arXiv:2401.14021 |  |  | 2 | KV Cache Optimization / Compression, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2401.14021) |
| 111 | arXiv:2402.01680 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 112 | arXiv:2402.06126 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.06126) |
| 113 | arXiv:2402.12289 |  |  | 2 | Expert Prefetch, survey-edge-llm | [source](https://arxiv.org/abs/2402.12289) |
| 114 | arXiv:2402.13718 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.13718) |
| 115 | arXiv:2402.18158 |  |  | 2 | Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.18158) |
| 116 | arXiv:2403.03507 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, その他システム研究 | [source](https://arxiv.org/abs/2403.03507) |
| 117 | arXiv:2403.07816 |  |  | 2 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2403.07816) |
| 118 | arXiv:2403.12422 |  |  | 2 | survey-distributed-training-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.12422) |
| 119 | arXiv:2404.07839 |  |  | 2 | hybrid Mamba-Transformer inference memory management, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2404.07839) |
| 120 | arXiv:2404.13628 |  |  | 2 | 02-adaptive-expert-computation-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2404.13628) |
| 121 | arXiv:2405.03133 |  |  | 2 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.03133) |
| 122 | arXiv:2405.21015 |  |  | 2 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation, その他システム研究 | [source](https://arxiv.org/abs/2405.21015) |
| 123 | arXiv:2406.02430 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.02430) |
| 124 | arXiv:2406.04127 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2406.04127) |
| 125 | arXiv:2406.08673 |  |  | 2 | 大規模分散学習・整合学習基盤, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2406.08673) |
| 126 | arXiv:2406.11939 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2406.11939) |
| 127 | arXiv:2406.18629 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2406.18629) |
| 128 | arXiv:2407.00128 |  |  | 2 | Speculative Decoding / Parallel Inference Systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.00128) |
| 129 | arXiv:2407.08296 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, survey-low-bit-llm | [source](https://arxiv.org/abs/2407.08296) |
| 130 | arXiv:2407.10855 |  |  | 2 | kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.10855) |
| 131 | arXiv:2407.12821 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2407.12821) |
| 132 | arXiv:2408.06292 |  |  | 2 | LLMサービング／自動スケーリング／広域ルーティング, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2408.06292) |
| 133 | arXiv:2409.06857 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, offload-hierarchical-memory | [source](https://arxiv.org/abs/2409.06857) |
| 134 | arXiv:2409.17146 |  |  | 2 | Adaptive computation／cache-aware MoE, adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2409.17146) |
| 135 | arXiv:2410.00037 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.00037) |
| 136 | arXiv:2410.05589 |  |  | 2 | 投機的デコード／動的LLMサービング／GPU空間多重化, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2410.05589) |
| 137 | arXiv:2410.10762 |  |  | 2 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10762) |
| 138 | arXiv:2410.13461 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2410.13461) |
| 139 | arXiv:2410.17840 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.17840) |
| 140 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 141 | arXiv:2411.02335 |  |  | 2 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, adaptive expert computation / compression; end-side sparse MoE | [source](https://arxiv.org/abs/2411.02335) |
| 142 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 143 | arXiv:2411.11055 |  |  | 2 | Speculative decoding × MoE, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 144 | arXiv:2411.17309 |  |  | 2 | Offload / Hierarchical Memory, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.17309) |
| 145 | arXiv:2412.12488 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.12488) |
| 146 | arXiv:2412.14468 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLMサービング・接頭辞キャッシュ・マルチテナント隔離 | [source](https://arxiv.org/abs/2412.14468) |
| 147 | arXiv:2501.10714 |  |  | 2 | Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2501.10714) |
| 148 | arXiv:2502.01662 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2502.01662) |
| 149 | arXiv:2502.06768 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2502.06768) |
| 150 | arXiv:2502.11946 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.11946) |
| 151 | arXiv:2502.16880 |  |  | 2 | Speculative decoding × MoE, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2502.16880) |
| 152 | arXiv:2503.01586 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2503.01586) |
| 153 | arXiv:2503.08415 |  |  | 2 | KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, other-inference-systems | [source](https://arxiv.org/abs/2503.08415) |
| 154 | arXiv:2503.18773 |  |  | 2 | KV Cache Offload / Recomputation, batch inference / event-driven runtime / MoE serving / offload | [source](https://arxiv.org/abs/2503.18773) |
| 155 | arXiv:2503.24358 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, System-aware KV cache | [source](https://arxiv.org/abs/2503.24358) |
| 156 | arXiv:2504.06214 |  |  | 2 | llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2504.06214) |
| 157 | arXiv:2504.12216 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2504.12216) |
| 158 | arXiv:2504.16054 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2504.16054) |
| 159 | arXiv:2504.17307 |  |  | 2 | KV Cache Offload / Recomputation, LLMサービング／スケジューリング／分離実行 | [source](https://arxiv.org/abs/2504.17307) |
| 160 | arXiv:2504.20101 |  |  | 2 | llm-serving-scheduling-disaggregation, 異種GPUサービング・分散推論・パイプライン並列・動的ルーティング | [source](https://arxiv.org/abs/2504.20101) |
| 161 | arXiv:2505.06708 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2505.06708) |
| 162 | arXiv:2505.14681 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2505.14681) |
| 163 | arXiv:2505.21411 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2505.21411) |
| 164 | arXiv:2506.13585 |  |  | 2 | kv-cache-reuse-position-independent-caching, speculative-decoding | [source](https://arxiv.org/abs/2506.13585) |
| 165 | arXiv:2507.02770 |  |  | 2 | GPU機密計算の性能評価、LLMサービング、KVキャッシュ退避、機密マルチGPU基盤, confidential inference / trusted execution environment / split inference / differential privacy | [source](https://arxiv.org/abs/2507.02770) |
| 166 | arXiv:2507.11948 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, kernel-runtime-compilation | [source](https://arxiv.org/abs/2507.11948) |
| 167 | arXiv:2507.18071 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2507.18071) |
| 168 | arXiv:2508.02193 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2508.02193) |
| 169 | arXiv:2508.08438 |  |  | 2 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08438) |
| 170 | arXiv:2508.16653 |  |  | 2 | 低ビット疎推論／GPUカーネル／エッジ推論, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2508.16653) |
| 171 | arXiv:2508.18298 |  |  | 2 | kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18298) |
| 172 | arXiv:2509.18883 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.18883) |
| 173 | arXiv:2509.23951 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.23951) |
| 174 | arXiv:2510.03293 |  |  | 2 | Expert Prefetch, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.03293) |
| 175 | arXiv:2510.08544 |  |  | 2 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.08544) |
| 176 | arXiv:2510.17483 |  |  | 2 | adaptive-expert-computation-compression, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2510.17483) |
| 177 | arXiv:2511.05502 |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2511.05502) |
| 178 | arXiv:2511.20048 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2511.20048) |
| 179 | arXiv:2512.01644 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2512.01644) |
| 180 | arXiv:2512.07647 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.07647) |
| 181 | arXiv:2512.16473 |  |  | 2 | Edge／on-device MoE, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.16473) |
| 182 | arXiv:2601.02872 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://arxiv.org/abs/2601.02872) |
| 183 | arXiv:2601.09527 |  |  | 2 | LLMサービング・スケジューリング・分離実行, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://arxiv.org/abs/2601.09527) |
| 184 | arXiv:2601.19092 |  |  | 2 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム, dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2601.19092) |
| 185 | arXiv:2602.02599 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2602.02599) |
| 186 | arXiv:2603.07685 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems | [source](https://arxiv.org/abs/2603.07685) |
| 187 | arXiv:2604.15409 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2604.15409) |
| 188 | arXiv:2606.03928 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2606.03928) |
| 189 | arXiv:2607.04031 |  |  | 2 | 10-kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2607.04031) |
| 190 | DOI:10.1109/cvpr.2018.00286 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, hardware-accelerators | [source](https://doi.org/10.1109/cvpr.2018.00286) |
| 191 | DOI:10.1109/hcs55958.2022.9895629 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1109/hcs55958.2022.9895629) |
| 192 | DOI:10.1109/hotchips.2019.8875654 |  |  | 2 | KV Cache Optimization / Compression, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/hotchips.2019.8875654) |
| 193 | DOI:10.1109/hpca61900.2025.00127 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00127) |
| 194 | DOI:10.1109/inpar.2012.6339596 |  |  | 2 | GPU architecture and tensor-computation orchestration, kernel-runtime-compilation | [source](https://doi.org/10.1109/inpar.2012.6339596) |
| 195 | DOI:10.1109/isca59077.2024.00036 |  |  | 2 | CXL memory pooling / KV cache offload / disaggregated memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/isca59077.2024.00036) |
| 196 | DOI:10.1109/jssc.2022.3200718 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/jssc.2022.3200718) |
| 197 | DOI:10.1109/lca.2026.3695938 |  |  | 2 | HBF / hierarchical memory / KV-cache management / LLM serving, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3695938) |
| 198 | DOI:10.1109/mm.2024.3373763 |  |  | 2 | KV Cache Offload / Recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2024.3373763) |
| 199 | DOI:10.1109/tbdata.2019.2921572 |  |  | 2 | RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/tbdata.2019.2921572) |
| 200 | DOI:10.1109/tpwrs.2022.3173250 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1109/tpwrs.2022.3173250) |
| 201 | DOI:10.1137/0117039 |  |  | 2 | llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://doi.org/10.1137/0117039) |
| 202 | DOI:10.1145/2485922.2485964 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/2485922.2485964) |
| 203 | DOI:10.1145/3092026 |  |  | 2 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching | [source](https://doi.org/10.1145/3092026) |
| 204 | DOI:10.1145/3437801.3441620 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3437801.3441620) |
| 205 | DOI:10.1145/3466752.3480125 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3466752.3480125) |
| 206 | DOI:10.1145/3538643.3539742 |  |  | 2 | 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3538643.3539742) |
| 207 | DOI:10.1145/3575693.3575724 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3575693.3575724) |
| 208 | DOI:10.1145/3582016.3582047 |  |  | 2 | 02-hardware-accelerators, kv-cache-optimization-compression | [source](https://doi.org/10.1145/3582016.3582047) |
| 209 | DOI:10.1145/3605573.3605613 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3605573.3605613) |
| 210 | DOI:10.1145/3627535.3638466 |  |  | 2 | KV Cache Optimization / Compression, serving-scheduling | [source](https://doi.org/10.1145/3627535.3638466) |
| 211 | DOI:10.1145/3649506 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, Offload / Hierarchical Memory | [source](https://doi.org/10.1145/3649506) |
| 212 | DOI:10.1145/3676641.3716025 |  |  | 2 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://doi.org/10.1145/3676641.3716025) |
| 213 | DOI:10.1145/3694715.3695963 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing | [source](https://doi.org/10.1145/3694715.3695963) |
| 214 | DOI:10.1145/3725843.3756115 |  |  | 2 | PIM / Near-Data Acceleration, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756115) |
| 215 | DOI:10.1145/3768165 |  |  | 2 | Edge / On-device LLM Systems, speculative-decoding-moe | [source](https://doi.org/10.1145/3768165) |
| 216 | DOI:10.1145/3805475 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3805475) |
| 217 | DOI:10.14778/3415478.3415530 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.14778/3415478.3415530) |
| 218 | DOI:10.18653/v1/2022.emnlp-main.823 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/2022.emnlp-main.823) |
| 219 | DOI:10.18653/v1/2024.acl-long.91 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.91) |
| 220 | DOI:10.18653/v1/2024.findings-emnlp.899 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.899) |
| 221 | DOI:10.48550/arxiv.2304.07327 |  |  | 2 | KVキャッシュ最適化／適応圧縮, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2304.07327) |
| 222 | DOI:10.48550/arxiv.2602.08676 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://doi.org/10.48550/arxiv.2602.08676) |
| 223 | DOI:10.52202/075280-1506 |  |  | 2 | early-exit-offloading-self-speculative-decoding, kv-cache-optimization-compression | [source](https://doi.org/10.52202/075280-1506) |
| 224 | DOI:10.52202/079017-3180 |  |  | 2 | adaptive-expert-computation-compression, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.52202/079017-3180) |
| 225 | OpenReview:0fJfVOSUra |  |  | 2 | 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://openreview.net/forum?id=0fJfVOSUra) |
| 226 | OpenReview:acJ3vdFljk |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=acJ3vdFljk) |
| 227 | OpenReview:dwPdYFqVWO |  |  | 2 | Speculative decoding × MoE, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://openreview.net/forum?id=dwPdYFqVWO) |
| 228 | OpenReview:FbhjirzvJG |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=FbhjirzvJG) |
| 229 | OpenReview:HklBjCEKvH |  |  | 2 | Speculative Decoding, other-inference-systems | [source](https://openreview.net/forum?id=HklBjCEKvH) |
| 230 | OpenReview:JZfg6wGi6g |  |  | 2 | KV Cache Optimization / Compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=JZfg6wGi6g) |
| 231 | OpenReview:NGPmH3vbAA_ |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=NGPmH3vbAA_) |
| 232 | OpenReview:R7fv5NWfMm |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=R7fv5NWfMm) |
| 233 | OpenReview:SFN6Wm7YBI |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=SFN6Wm7YBI) |
| 234 | OpenReview:xdNAVP7TGy |  |  | 2 | kv-cache-offload-recomputation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://openreview.net/forum?id=xdNAVP7TGy) |
| 235 | arXiv:1511.06297 |  |  | 2 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1511.06297) |
| 236 | DOI:10.1109/cstic55103.2022.9856846 |  |  | 2 | 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1109/cstic55103.2022.9856846) |
| 237 | DOI:10.1145/3786655 |  |  | 2 | kv-cache-reuse-position-independent-caching | [source](https://doi.org/10.1145/3786655) |
| 238 | DOI:10.18653/v1/2023.emnlp-main.907 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/2023.emnlp-main.907) |
| 239 | DOI:10.18653/v1/2024.naacl-long.222 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.naacl-long.222) |
| 240 | DOI:10.18653/v1/2025.naacl-long.328 |  |  | 2 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://doi.org/10.18653/v1/2025.naacl-long.328) |
| 241 | OpenReview:7zNYY1E2fq |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論 | [source](https://openreview.net/forum?id=7zNYY1E2fq) |
| 242 | OpenReview:P0GOk5wslg |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=P0GOk5wslg) |
| 243 | OpenReview:RlqYCpTu1P |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=RlqYCpTu1P) |
| 244 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 245 | DOI:10.18653/v1/d19-1223 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/d19-1223) |
| 246 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 247 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 248 | OpenReview:OS5dqxmmtl |  |  | 2 |  | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 249 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 250 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 251 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 252 | arXiv:1312.6114 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 253 | arXiv:1404.5997 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1404.5997) |
| 254 | arXiv:1411.1792 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1411.1792) |
| 255 | arXiv:1506.02438 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 256 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 257 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 258 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 259 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 260 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 261 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 262 | arXiv:1606.06160 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 263 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 264 | arXiv:1611.01578 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 265 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 266 | arXiv:1703.03664 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1703.03664) |
| 267 | arXiv:1703.06114 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1703.06114) |
| 268 | arXiv:1704.04684 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/1704.04684) |
| 269 | arXiv:1704.05426 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 270 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 271 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 272 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 273 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 274 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 275 | arXiv:1710.09437 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1710.09437) |
| 276 | arXiv:1711.03936 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 277 | arXiv:1711.09224 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.09224) |
| 278 | arXiv:1712.05382 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.05382) |
| 279 | arXiv:1801.10198 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1801.10198) |
| 280 | arXiv:1802.05751 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1802.05751) |
| 281 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 282 | arXiv:1804.06087 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 283 | arXiv:1806.02847 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 284 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 285 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 286 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 287 | arXiv:1809.11096 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1809.11096) |
| 288 | arXiv:1810.03292 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1810.03292) |
| 289 | arXiv:1810.09868 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1810.09868) |
| 290 | arXiv:1811.05233 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 291 | arXiv:1812.06162 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1812.06162) |
| 292 | arXiv:1902.00751 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.00751) |
| 293 | arXiv:1902.08295 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1902.08295) |
| 294 | arXiv:1902.10186 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 295 | arXiv:1903.01699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 296 | arXiv:1904.01038 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1904.01038) |
| 297 | arXiv:1904.09675 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 298 | arXiv:1905.07129 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 299 | arXiv:1906.02041 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/1906.02041) |
| 300 | arXiv:1906.08172 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1906.08172) |
| 301 | arXiv:1907.01989 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1907.01989) |
| 302 | arXiv:1908.08593 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1908.08593) |
| 303 | arXiv:1908.11365 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1908.11365) |
| 304 | arXiv:1909.05803 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1909.05803) |
| 305 | arXiv:1909.11556 |  |  | 1 | speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 306 | arXiv:1910.04915 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1910.04915) |
| 307 | arXiv:1910.06360 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 308 | arXiv:1911.02116 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 309 | arXiv:1911.04997 |  |  | 1 | MoE expert parallelism / dynamic load balancing / expert prefetching | [source](https://arxiv.org/abs/1911.04997) |
| 310 | arXiv:1911.11313 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 311 | arXiv:2002.08155 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2002.08155) |
| 312 | arXiv:2002.10941 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2002.10941) |
| 313 | arXiv:2003.06713 |  |  | 1 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement | [source](https://arxiv.org/abs/2003.06713) |
| 314 | arXiv:2004.02984 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2004.02984) |
| 315 | arXiv:2004.08900 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 316 | arXiv:2004.11867 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 317 | arXiv:2005.00628 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 318 | arXiv:2005.03454 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 319 | arXiv:2005.14187 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 320 | arXiv:2006.10518 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 321 | arXiv:2006.12467 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 322 | arXiv:2007.07779 |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 323 | arXiv:2008.00051 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 324 | arXiv:2009.06106 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 325 | arXiv:2009.08034 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2009.08034) |
| 326 | arXiv:2009.09736 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2009.09736) |
| 327 | arXiv:2010.02394 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 328 | arXiv:2010.03379 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03379) |
| 329 | arXiv:2010.03983 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03983) |
| 330 | arXiv:2010.11443 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2010.11443) |
| 331 | arXiv:2011.02999 |  |  | 1 | 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://arxiv.org/abs/2011.02999) |
| 332 | arXiv:2011.06327 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2011.06327) |
| 333 | arXiv:2012.11346 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2012.11346) |
| 334 | arXiv:2012.15701 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2012.15701) |
| 335 | arXiv:2101.08744 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2101.08744) |
| 336 | arXiv:2102.02611 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2102.02611) |
| 337 | arXiv:2102.08124 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2102.08124) |
| 338 | arXiv:2102.11174 |  |  | 1 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2102.11174) |
| 339 | arXiv:2103.03330 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2103.03330) |
| 340 | arXiv:2104.06599 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2104.06599) |
| 341 | arXiv:2104.13478 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2104.13478) |
| 342 | arXiv:2105.06990 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2105.06990) |
| 343 | arXiv:2105.14450 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2105.14450) |
| 344 | arXiv:2106.03764 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2106.03764) |
| 345 | arXiv:2106.05974 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2106.05974) |
| 346 | arXiv:2106.10595 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2106.10595) |
| 347 | arXiv:2107.05407 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/2107.05407) |
| 348 | arXiv:2108.05036 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2108.05036) |
| 349 | arXiv:2109.00859 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2109.00859) |
| 350 | arXiv:2109.05472 |  |  | 1 | 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2109.05472) |
| 351 | arXiv:2109.10686 |  |  | 1 | 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2109.10686) |
| 352 | arXiv:2109.11817 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2109.11817) |
| 353 | arXiv:2110.06296 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2110.06296) |
| 354 | arXiv:2110.12894 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 355 | arXiv:2111.00160 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 356 | arXiv:2111.00856 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2111.00856) |
| 357 | arXiv:2112.02958 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2112.02958) |
| 358 | arXiv:2112.06749 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2112.06749) |
| 359 | arXiv:2112.14397 |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 360 | arXiv:2201.13425 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2201.13425) |
| 361 | arXiv:2202.05262 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2202.05262) |
| 362 | arXiv:2202.08791 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2202.08791) |
| 363 | arXiv:2202.13914 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.13914) |
| 364 | arXiv:2203.03131 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2203.03131) |
| 365 | arXiv:2203.06850 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2203.06850) |
| 366 | arXiv:2203.11014 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2203.11014) |
| 367 | arXiv:2204.05832 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2204.05832) |
| 368 | arXiv:2204.06683 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 369 | arXiv:2204.11574 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2204.11574) |
| 370 | arXiv:2205.04934 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2205.04934) |
| 371 | arXiv:2205.10364 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10364) |
| 372 | arXiv:2205.11916 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2205.11916) |
| 373 | arXiv:2205.13603 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2205.13603) |
| 374 | arXiv:2206.02845 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2206.02845) |
| 375 | arXiv:2207.05952 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 376 | arXiv:2207.10551 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2207.10551) |
| 377 | arXiv:2208.02813 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 378 | arXiv:2208.08227 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 379 | arXiv:2209.03143 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 380 | arXiv:2209.11429 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 381 | arXiv:2209.15352 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 382 | arXiv:2210.03057 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 383 | arXiv:2210.05709 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2210.05709) |
| 384 | arXiv:2210.08674 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2210.08674) |
| 385 | arXiv:2210.11948 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 386 | arXiv:2210.14793 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 387 | arXiv:2211.00593 |  |  | 1 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 388 | arXiv:2211.06033 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 389 | arXiv:2211.09699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 390 | arXiv:2211.15089 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 391 | arXiv:2212.00768 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.00768) |
| 392 | arXiv:2212.04088 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.04088) |
| 393 | arXiv:2212.05238 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.05238) |
| 394 | arXiv:2212.10325 |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2212.10325) |
| 395 | arXiv:2212.10509 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 396 | arXiv:2212.12017 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 397 | arXiv:2301.04104 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.04104) |
| 398 | arXiv:2301.06672 |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2301.06672) |
| 399 | arXiv:2301.08984 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2301.08984) |
| 400 | arXiv:2301.12503 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2301.12503) |
| 401 | arXiv:2302.02451 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.02451) |
| 402 | arXiv:2302.04863 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.04863) |
| 403 | arXiv:2302.09419 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.09419) |
| 404 | arXiv:2302.11529 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2302.11529) |
| 405 | arXiv:2302.12480 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.12480) |
| 406 | arXiv:2302.14502 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2302.14502) |
| 407 | arXiv:2303.02861 |  |  | 1 | 02-adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.02861) |
| 408 | arXiv:2303.06135 |  |  | 1 | fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2303.06135) |
| 409 | arXiv:2303.07129 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 410 | arXiv:2303.10512 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.10512) |
| 411 | arXiv:2303.13003 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2303.13003) |
| 412 | arXiv:2303.16199 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 413 | arXiv:2304.02017 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 414 | arXiv:2304.03208 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2304.03208) |
| 415 | arXiv:2304.04488 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2304.04488) |
| 416 | arXiv:2304.05332 |  |  | 1 | LLM inference kernel safety / CUDA symbolic execution / model-aware verification | [source](https://arxiv.org/abs/2304.05332) |
| 417 | arXiv:2304.08442 |  |  | 1 | MoE推論／エキスパート並列／エキスパート配置／全対全通信／負荷分散 | [source](https://arxiv.org/abs/2304.08442) |
| 418 | arXiv:2304.10411 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2304.10411) |
| 419 | arXiv:2304.12244 |  |  | 1 | multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 420 | arXiv:2304.15010 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 421 | arXiv:2305.02538 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 422 | arXiv:2305.04044 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2305.04044) |
| 423 | arXiv:2305.07622 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 424 | arXiv:2305.10010 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10010) |
| 425 | arXiv:2305.11860 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2305.11860) |
| 426 | arXiv:2305.13412 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2305.13412) |
| 427 | arXiv:2305.14160 |  |  | 1 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 428 | arXiv:2305.14516 |  |  | 1 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://arxiv.org/abs/2305.14516) |
| 429 | arXiv:2305.14952 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2305.14952) |
| 430 | arXiv:2305.15387 |  |  | 1 | KV cache compression / sparse attention / long-context inference | [source](https://arxiv.org/abs/2305.15387) |
| 431 | arXiv:2305.17126 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2305.17126) |
| 432 | arXiv:2305.18691 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.18691) |
| 433 | arXiv:2306.02003 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 434 | arXiv:2306.02896 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02896) |
| 435 | arXiv:2306.04933 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 436 | arXiv:2306.06624 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2306.06624) |
| 437 | arXiv:2306.09782 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.09782) |
| 438 | arXiv:2306.14565 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2306.14565) |
| 439 | arXiv:2307.01189 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.01189) |
| 440 | arXiv:2307.04339 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04339) |
| 441 | arXiv:2307.07697 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2307.07697) |
| 442 | arXiv:2307.08352 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.08352) |
| 443 | arXiv:2307.15043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.15043) |
| 444 | arXiv:2308.03421 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2308.03421) |
| 445 | arXiv:2308.10755 |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2308.10755) |
| 446 | arXiv:2308.15272 |  |  | 1 | on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2308.15272) |
| 447 | arXiv:2309.09117 |  |  | 1 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2309.09117) |
| 448 | arXiv:2310.00811 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2310.00811) |
| 449 | arXiv:2310.03025 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.03025) |
| 450 | arXiv:2310.05421 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.05421) |
| 451 | arXiv:2310.07147 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.07147) |
| 452 | arXiv:2310.10046 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.10046) |
| 453 | arXiv:2310.12670 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.12670) |
| 454 | arXiv:2310.16355 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2310.16355) |
| 455 | arXiv:2310.19295 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.19295) |
| 456 | arXiv:2311.00502 |  |  | 1 | CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/2311.00502) |
| 457 | arXiv:2311.02462 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2311.02462) |
| 458 | arXiv:2311.05997 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.05997) |
| 459 | arXiv:2311.08377 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2311.08377) |
| 460 | arXiv:2311.11586 |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2311.11586) |
| 461 | arXiv:2311.12785 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2311.12785) |
| 462 | arXiv:2311.14030 |  |  | 1 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復 | [source](https://arxiv.org/abs/2311.14030) |
| 463 | arXiv:2312.00858 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.00858) |
| 464 | arXiv:2312.03209 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.03209) |
| 465 | arXiv:2312.04257 |  |  | 1 | 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://arxiv.org/abs/2312.04257) |
| 466 | arXiv:2312.05253 |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2312.05253) |
| 467 | arXiv:2312.06902 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.06902) |
| 468 | arXiv:2312.09193 |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2312.09193) |
| 469 | arXiv:2312.12682 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.12682) |
| 470 | arXiv:2312.14950 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2312.14950) |
| 471 | arXiv:2312.17240 |  |  | 1 | 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2312.17240) |
| 472 | arXiv:2401.01666 |  |  | 1 | 05-speculative-decoding-moe | [source](https://arxiv.org/abs/2401.01666) |
| 473 | arXiv:2401.03568 |  |  | 1 | 17-pim-near-data-acceleration | [source](https://arxiv.org/abs/2401.03568) |
| 474 | arXiv:2401.05761 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2401.05761) |
| 475 | arXiv:2401.06775 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2401.06775) |
| 476 | arXiv:2401.07324 |  |  | 1 | multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2401.07324) |
| 477 | arXiv:2401.08294 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2401.08294) |
| 478 | arXiv:2401.08500 |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2401.08500) |
| 479 | arXiv:2401.10480 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2401.10480) |
| 480 | arXiv:2401.12143 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2401.12143) |
| 481 | arXiv:2401.13920 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2401.13920) |
| 482 | arXiv:2401.15347 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.15347) |
| 483 | arXiv:2402.01173 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.01173) |
| 484 | arXiv:2402.03564 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/2402.03564) |
| 485 | arXiv:2402.03701 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2402.03701) |
| 486 | arXiv:2402.04792 |  |  | 1 | fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2402.04792) |
| 487 | arXiv:2402.05939 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.05939) |
| 488 | arXiv:2402.07839 |  |  | 1 | MoE compression / expert merging / output approximation / least-squares compression | [source](https://arxiv.org/abs/2402.07839) |
| 489 | arXiv:2402.09589 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2402.09589) |
| 490 | arXiv:2402.10462 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.10462) |
| 491 | arXiv:2402.11295 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2402.11295) |
| 492 | arXiv:2402.12052 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.12052) |
| 493 | arXiv:2402.12354 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.12354) |
| 494 | arXiv:2402.13717 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.13717) |
| 495 | arXiv:2402.14852 |  |  | 1 | Speculative decoding × MoE | [source](https://arxiv.org/abs/2402.14852) |
| 496 | arXiv:2402.16819 |  |  | 1 | survey-edge-llm | [source](https://arxiv.org/abs/2402.16819) |
| 497 | arXiv:2402.17702 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.17702) |
| 498 | arXiv:2402.19255 |  |  | 1 | multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2402.19255) |
| 499 | arXiv:2403.00176 |  |  | 1 | on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2403.00176) |
| 500 | arXiv:2403.01241 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2403.01241) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

