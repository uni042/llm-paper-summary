# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-03T07:59:10+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **574** / 未claim総数: **427** / このworker向け: **142**

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
| 98 | research | arXiv:2201.12023 | Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning | [primary](https://arxiv.org/abs/2201.12023) | `papers/inference/99-other-inference-systems/2022-2201.12023-alpa-automating-inter-and-intra-operator-parallelism-for-distributed-deep-learning.md` |
| 99 | research | arXiv:2409.00142 | Dynamic Depth Decoding: Faster Speculative Decoding for LLMs | [primary](https://arxiv.org/abs/2409.00142) | `papers/inference/99-other-inference-systems/2024-2409.00142-dynamic-depth-decoding-faster-speculative-decoding-for-llms.md` |
| 100 | research | arXiv:2006.09616 | Dynamic Tensor Rematerialization | [primary](https://arxiv.org/abs/2006.09616) | `papers/inference/99-other-inference-systems/2020-2006.09616-dynamic-tensor-rematerialization.md` |
| 101 | research | arXiv:2509.17396 | EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments | [primary](https://arxiv.org/abs/2509.17396) | `papers/inference/99-other-inference-systems/2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-resource-constrained-environments.md` |
| 102 | research | arXiv:2602.02579 | ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2602.02579) | `papers/inference/99-other-inference-systems/2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cache-reuse-in-retrieval-augmented-generation.md` |
| 103 | research | arXiv:2510.20171 | Collective Communication for 100k+ GPUs | [primary](https://arxiv.org/abs/2510.20171) | `papers/inference/99-other-inference-systems/2025-2510.20171-collective-communication-for-100k-gpus.md` |
| 104 | research | DOI:10.1145/3731569.3764823 | Jenga: Effective Memory Management for Serving LLM with Heterogeneity | [primary](https://doi.org/10.1145/3731569.3764823) | `papers/inference/99-other-inference-systems/0000-c5994a53cb83-jenga-effective-memory-management-for-serving-llm-with-heterogeneity.md` |
| 105 | research | arXiv:2410.06916 | SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration | [primary](https://arxiv.org/abs/2410.06916) | `papers/inference/99-other-inference-systems/2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleration.md` |
| 106 | research | arXiv:2408.01803 | STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs | [primary](https://arxiv.org/abs/2408.01803) | `papers/inference/99-other-inference-systems/2024-2408.01803-stbllm-breaking-the-1-bit-barrier-with-structured-binary-llms.md` |
| 107 | research | arXiv:2604.11035 | Introspective Diffusion Language Models | [primary](https://arxiv.org/abs/2604.11035) | `papers/inference/99-other-inference-systems/2026-2604.11035-introspective-diffusion-language-models.md` |
| 108 | research | DOI:10.1145/3773772 | Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving | [primary](https://doi.org/10.1145/3773772) | `papers/inference/99-other-inference-systems/0000-aa24341e05f1-mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md` |
| 109 | research | arXiv:2412.19442 | A Survey on Large Language Model Acceleration based on KV Cache Management | [primary](https://arxiv.org/abs/2412.19442) | `papers/inference/99-other-inference-systems/2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-management.md` |
| 110 | research | DOI:10.18653/v1/2023.emnlp-main.298 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | [primary](https://aclanthology.org/2023.emnlp-main.298/) | `papers/inference/99-other-inference-systems/0000-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-checkpoints.md` |
| 111 | research | arXiv:2104.04473 | Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM | [primary](https://arxiv.org/abs/2104.04473) | `papers/inference/99-other-inference-systems/2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-megatron-lm.md` |
| 112 | research | arXiv:2411.01288 | Hexa-MoE: Efficient and Heterogeneous-aware Training for Mixture-of-Experts | [primary](https://arxiv.org/abs/2411.01288) | `papers/inference/99-other-inference-systems/2024-2411.01288-hexa-moe-efficient-and-heterogeneous-aware-training-for-mixture-of-experts.md` |
| 113 | research | arXiv:2411.18424 | FastSwitch: Optimizing Context Switching Efficiency in Fairness-aware Large Language Model Serving | [primary](https://arxiv.org/abs/2411.18424) | `papers/inference/99-other-inference-systems/2024-2411.18424-fastswitch-optimizing-context-switching-efficiency-in-fairness-aware-large-language-model-serving.md` |
| 114 | research | arXiv:2503.18989 | A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models | [primary](https://arxiv.org/abs/2503.18989) | `papers/inference/99-other-inference-systems/2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-large-language-models.md` |
| 115 | research | arXiv:2507.19635 | Efficient and Scalable Agentic AI with Heterogeneous Systems | [primary](https://arxiv.org/abs/2507.19635) | `papers/inference/99-other-inference-systems/2025-2507.19635-efficient-and-scalable-agentic-ai-with-heterogeneous-systems.md` |
| 116 | research | DOI:10.1145/3695053.3730999 | WindServe: Efficient Phase-Disaggregated LLM Serving with Stream-based Dynamic Scheduling | [primary](https://doi.org/10.1145/3695053.3730999) | `papers/inference/99-other-inference-systems/2025-8e0fd88d7ddc-windserve-efficient-phase-disaggregated-llm-serving-with-stream-based-dynamic-scheduling.md` |
| 117 | research | arXiv:2507.11417 | Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations | [primary](https://arxiv.org/abs/2507.11417) | `papers/inference/99-other-inference-systems/2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference-via-simulations.md` |
| 118 | research | arXiv:2506.07530 | BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation | [primary](https://arxiv.org/abs/2506.07530) | `papers/inference/99-other-inference-systems/2025-2506.07530-bitvla-1-bit-vision-language-action-models-for-robotics-manipulation.md` |
| 119 | research | arXiv:2503.00634 | Efficiently Editing Mixture-of-Experts Models with Compressed Experts | [primary](https://arxiv.org/abs/2503.00634) | `papers/inference/99-other-inference-systems/2025-2503.00634-efficiently-editing-mixture-of-experts-models-with-compressed-experts.md` |
| 120 | research | arXiv:2510.15312 | Accelerating Mobile Language Model via Speculative Decoding and NPU-Coordinated Execution | [primary](https://arxiv.org/abs/2510.15312) | `papers/inference/99-other-inference-systems/2025-2510.15312-accelerating-mobile-language-model-via-speculative-decoding-and-npu-coordinated-execution.md` |
| 121 | research | arXiv:2302.08007 | With Shared Microexponents, A Little Shifting Goes a Long Way | [primary](https://arxiv.org/abs/2302.08007) | `papers/inference/99-other-inference-systems/2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md` |
| 122 | research | arXiv:2407.00088 | T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge | [primary](https://arxiv.org/abs/2407.00088) | `papers/inference/99-other-inference-systems/2024-2407.00088-t-mac-cpu-renaissance-via-table-lookup-for-low-bit-llm-deployment-on-edge.md` |
| 123 | research | arXiv:2412.04964 | Flash Communication: Reducing Tensor Parallelization Bottleneck for Fast Large Language Model Inference | [primary](https://arxiv.org/abs/2412.04964) | `papers/inference/99-other-inference-systems/2024-2412.04964-flash-communication-reducing-tensor-parallelization-bottleneck-for-fast-large-language-model-inference.md` |
| 124 | research | arXiv:2408.03314 | Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters | [primary](https://arxiv.org/abs/2408.03314) | `papers/inference/99-other-inference-systems/2024-2408.03314-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model-parameters.md` |
| 125 | research | arXiv:2412.21187 | Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs | [primary](https://arxiv.org/abs/2412.21187) | `papers/inference/99-other-inference-systems/2024-2412.21187-do-not-think-that-much-for-2-3-on-the-overthinking-of-o1-like-llms.md` |
| 126 | research | DOI:10.1145/3725843.3756078 | LLM.265: Video Codecs are Secretly Tensor Codecs | [primary](https://doi.org/10.1145/3725843.3756078) | `papers/inference/99-other-inference-systems/2025-5a2b2924d4e3-llm-265-video-codecs-are-secretly-tensor-codecs.md` |
| 127 | research | arXiv:2609.22158 | StepKV: Step-Aware KV Cache Compression for LLM Agents | [primary](https://arxiv.org/abs/2609.22158) | `papers/inference/99-other-inference-systems/2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md` |
| 128 | research | arXiv:2309.16354 | Transformer-VQ: Linear-Time Transformers via Vector Quantization | [primary](https://arxiv.org/abs/2309.16354) | `papers/inference/99-other-inference-systems/2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md` |
| 129 | research | arXiv:2608.13524 | DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees | [primary](https://arxiv.org/abs/2608.13524) | `papers/inference/99-other-inference-systems/2026-2608.13524-dartree-speculative-diffusion-decoding-with-autoregressive-draft-trees.md` |
| 130 | research | arXiv:2310.07096 | Sparse Universal Transformer | [primary](https://arxiv.org/abs/2310.07096) | `papers/inference/99-other-inference-systems/2023-2310.07096-sparse-universal-transformer.md` |
| 131 | research | arXiv:2310.06694 | Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning | [primary](https://arxiv.org/abs/2310.06694) | `papers/inference/99-other-inference-systems/2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pruning.md` |
| 132 | research | arXiv:2601.04719 | GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models | [primary](https://arxiv.org/abs/2601.04719) | `papers/inference/99-other-inference-systems/2026-2601.04719-gpu-accelerated-int8-quantization-for-kv-cache-compression-in-large-language-models.md` |
| 133 | research | arXiv:2609.30854 | The KV Cache Is the New Memory Wall | [primary](https://arxiv.org/abs/2609.30854) | `papers/inference/99-other-inference-systems/2026-2609.30854-the-kv-cache-is-the-new-memory-wall.md` |
| 134 | research | arXiv:2602.13836 | Speculative Decoding with a Speculative Vocabulary | [primary](https://arxiv.org/abs/2602.13836) | `papers/inference/99-other-inference-systems/2026-2602.13836-speculative-decoding-with-a-speculative-vocabulary.md` |
| 135 | research | DOI:10.18653/v1/2026.findings-acl.1655 | LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation | [primary](https://aclanthology.org/2026.findings-acl.1655/) | `papers/inference/99-other-inference-systems/2026-df65c3a3c97c-logitspec-accelerating-retrieval-based-speculative-decoding-via-next-next-token-speculation.md` |
| 136 | research | DOI:10.1145/3662006.3662067 | Hybrid SLM and LLM for Edge-Cloud Collaborative Inference | [primary](https://doi.org/10.1145/3662006.3662067) | `papers/inference/99-other-inference-systems/2024-7a6bf47fa469-hybrid-slm-and-llm-for-edge-cloud-collaborative-inference.md` |
| 137 | research | arXiv:2401.10480 | Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning | [primary](https://arxiv.org/abs/2401.10480) | `papers/inference/99-other-inference-systems/2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reasoning.md` |
| 138 | research | arXiv:2402.05964 | A Survey on Transformer Compression | [primary](https://arxiv.org/abs/2402.05964) | `papers/inference/99-other-inference-systems/2024-2402.05964-a-survey-on-transformer-compression.md` |
| 139 | research | arXiv:2312.09193 | Fast Sampling via Discrete Non-Markov Diffusion Models with Predetermined Transition Time | [primary](https://arxiv.org/abs/2312.09193) | `papers/inference/99-other-inference-systems/2023-2312.09193-fast-sampling-via-discrete-non-markov-diffusion-models-with-predetermined-transition-time.md` |
| 140 | research | arXiv:2402.10631 | BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation | [primary](https://arxiv.org/abs/2402.10631) | `papers/inference/99-other-inference-systems/2024-2402.10631-bitdistiller-unleashing-the-potential-of-sub-4-bit-llms-via-self-distillation.md` |
| 141 | research | arXiv:2402.17463 | Training-Free Long-Context Scaling of Large Language Models | [primary](https://arxiv.org/abs/2402.17463) | `papers/inference/99-other-inference-systems/2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md` |
| 142 | research | arXiv:2402.14160 | Recursive Speculative Decoding: Accelerating LLM Inference via Sampling Without Replacement | [primary](https://arxiv.org/abs/2402.14160) | `papers/inference/99-other-inference-systems/2024-2402.14160-recursive-speculative-decoding-accelerating-llm-inference-via-sampling-without-replacement.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5446** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3694715.3695948 |  |  | 15 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 2 | arXiv:1910.01108 |  |  | 12 | LLM Serving / Scheduling / Disaggregation, LLMサービング／予測型スケジューリング, Speculative Decoding, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 投機的デコード / 分布保存型デコード高速化, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1910.01108) |
| 3 | arXiv:2304.04487 |  |  | 12 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 投機的デコード / 自己投機的デコード / 層スキップ | [source](https://arxiv.org/abs/2304.04487) |
| 4 | arXiv:2601.03267 |  |  | 11 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, 投機的デコードにおける自己回帰ドラフトと並列ドラフトの折衷, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2601.03267) |
| 5 | DOI:10.1016/j.neucom.2023.127063 |  |  | 11 | 02-hardware-accelerators, GPU architecture and tensor-computation orchestration, KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, Sparse Attention, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://doi.org/10.1016/j.neucom.2023.127063) |
| 6 | arXiv:2309.00071 |  |  | 10 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Adaptive computation／cache-aware MoE, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, kv-cache-offload-recomputation, moe | [source](https://arxiv.org/abs/2309.00071) |
| 7 | OpenReview:VTF8yNQM66 |  |  | 10 | 13-sparse-attention, Agentic Serving Benchmarking, MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, agentic workflow serving / workflow physical planning / adaptive serving, llm-serving-scheduling-disaggregation, other-inference-systems, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=VTF8yNQM66) |
| 8 | arXiv:2104.08691 |  |  | 9 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, many-adapter LLM serving / LoRA serving / inference scheduling, survey-long-context-serving, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2104.08691) |
| 9 | DOI:10.18653/v1/2024.acl-long.623 |  |  | 9 | 02-hardware-accelerators, 14-agentic-inference-serving-runtime, KV Cache Offload / Recomputation, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Offload / Hierarchical Memory, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, llm-serving-scheduling-disaggregation, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.18653/v1/2024.acl-long.623) |
| 10 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 11 | arXiv:1911.11641 |  |  | 9 | 16-weight-quantization-compression, Conditional Computation, adaptive-expert-computation-compression, kv-cache-memory, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-quantization-compression | [source](https://arxiv.org/abs/1911.11641) |
| 12 | arXiv:2410.21276 |  |  | 9 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, fine-grained MoE / expert routing / test-time scaling / inference-time sampling, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, multi-tenant LLM serving / latency attribution / fractional GPU sharing, その他システム研究 | [source](https://arxiv.org/abs/2410.21276) |
| 13 | DOI:10.1145/3394486.3406703 |  |  | 9 | GPU collective communication / communication compression / LLM serving disaggregation, KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems, kernel-runtime-compilation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3394486.3406703) |
| 14 | arXiv:2409.06669 |  |  | 8 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, Quantization × MoE × Offload, Speculative decoding × MoE, adaptive expert computation / dynamic MoE routing / expert sparsification, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2409.06669) |
| 15 | arXiv:2501.12599 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, Conditional Computation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation, serving-scheduling, 推論ベンチマーク・推論大規模言語モデルのサービング評価, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.12599) |
| 16 | arXiv:2305.13048 |  |  | 8 | KV Cache Offload / Recomputation, kv-cache, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling, 推論エンジン／推論基盤, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2305.13048) |
| 17 | DOI:10.1147/sj.52.0078 |  |  | 8 | 14-agentic-inference-serving-runtime, KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, MoE expert offloading / predictive prefetch and cache management, Offload / Hierarchical Memory, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1147/sj.52.0078) |
| 18 | OpenReview:nZeVKeeFYf9 |  |  | 8 | 18-vla-inference-quantization-evaluation, KV cache sparsity / paged attention / query-aware selection / LLM serving, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, llm-serving-systems, その他システム研究 | [source](https://openreview.net/forum?id=nZeVKeeFYf9) |
| 19 | arXiv:1809.09600 |  |  | 8 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 20 | arXiv:2305.16300 |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.16300) |
| 21 | DOI:10.5281/zenodo.10256836 |  |  | 7 | Adaptive Expert Computation / Compression, Conditional Computation, Expert Prefetch, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation, 投機復号・自己投機・ループ型Transformer・推論パイプライン, 投機的復号・Orthrus・推論再現性・数値精度 | [source](https://doi.org/10.5281/zenodo.10256836) |
| 22 | arXiv:2308.12966 |  |  | 7 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 23 | arXiv:2503.20215 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, batch inference / event-driven runtime / MoE serving / offload, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2503.20215) |
| 24 | OpenReview:chfJJYC3iL |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, Other Inference Systems / Lossless Parallel Decoding, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=chfJJYC3iL) |
| 25 | DOI:10.18653/v1/2025.emnlp-main.334 |  |  | 7 | 10-kv-cache-offload-recomputation, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, kv-cache-reuse-position-independent-caching, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://doi.org/10.18653/v1/2025.emnlp-main.334) |
| 26 | arXiv:2407.21118 |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2407.21118) |
| 27 | DOI:10.1145/3711896.3737413 |  |  | 7 | LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3711896.3737413) |
| 28 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 29 | DOI:10.48550/arxiv.2407.12391 |  |  | 6 | SLO-aware LLM serving scheduling, System-aware KV cache, disaggregated LLM serving / request routing / learned scheduling, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://doi.org/10.48550/arxiv.2407.12391) |
| 30 | arXiv:2110.04260 |  |  | 6 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference systems / expert parallelism / model compression / knowledge distillation, Quantization × MoE × Offload, inference-systems, その他システム研究 | [source](https://arxiv.org/abs/2110.04260) |
| 31 | DOI:10.1145/3768628 |  |  | 6 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 32 | arXiv:2405.14366 |  |  | 6 | KV Cache Offload / Retrieval / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation, other-inference-systems | [source](https://arxiv.org/abs/2405.14366) |
| 33 | arXiv:2509.17765 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 34 | OpenReview:Bkg6RiCqY7 |  |  | 6 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 35 | DOI:10.18653/v1/n18-2097 |  |  | 6 | inference-systems, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 36 | arXiv:2311.04939 |  |  | 6 | KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.04939) |
| 37 | OpenReview:mZn2Xyh9Ec |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=mZn2Xyh9Ec) |
| 38 | arXiv:2001.09977 |  |  | 5 | LLM Serving / Scheduling / Disaggregation, cross-layer LLM serving / SLO-aware scheduling / predictive routing / heterogeneous inference, serving-scheduling, speculative decoding / LLM serving / adaptive scheduling, その他システム研究 | [source](https://arxiv.org/abs/2001.09977) |
| 39 | arXiv:2304.09145 |  |  | 5 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 40 | arXiv:2603.01175 |  |  | 5 | 10-kv-cache-offload-recomputation, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, flash-capacity-tier-inference, hardware-accelerators, offload-hierarchical-memory | [source](https://arxiv.org/abs/2603.01175) |
| 41 | DOI:10.1145/3695053.3731008 |  |  | 5 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 42 | arXiv:1811.02883 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM inference simulation / disaggregated serving / performance modeling, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://arxiv.org/abs/1811.02883) |
| 43 | arXiv:2306.06000 |  |  | 5 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, SLO-aware LLM serving / chunked prefill / multi-resource scheduling, SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2306.06000) |
| 44 | DOI:10.18653/v1/d17-1082 |  |  | 5 | Adaptive computation／cache-aware MoE, Conditional Computation, MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, sparse attention / learned context ranking / long-context LLM inference | [source](https://doi.org/10.18653/v1/d17-1082) |
| 45 | OpenReview:xXTkbTBmqq |  |  | 5 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分, Quantization × MoE × Offload, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=xXTkbTBmqq) |
| 46 | arXiv:2501.08313 |  |  | 5 | 13-sparse-attention, moe-parallelism-communication, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.08313) |
| 47 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 48 | DOI:10.1145/3725843.3756062 |  |  | 5 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3725843.3756062) |
| 49 | arXiv:1603.08983 |  |  | 4 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 50 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 51 | arXiv:2412.16434 |  |  | 4 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation, other-inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2412.16434) |
| 52 | DOI:10.1145/3620666.3651352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 53 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 54 | OpenReview:L4uaAR4ArM |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, speculative-decoding | [source](https://openreview.net/forum?id=L4uaAR4ArM) |
| 55 | OpenReview:z5uVAKwmjf |  |  | 4 | 14-agentic-inference-serving-runtime, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, LLMサービング／自動スケーリング／広域ルーティング, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=z5uVAKwmjf) |
| 56 | arXiv:2203.08913 |  |  | 4 | LLM inference surveys、roofline performance analysis, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 57 | DOI:10.18653/v1/2021.naacl-main.365 |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems | [source](https://doi.org/10.18653/v1/2021.naacl-main.365) |
| 58 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 59 | arXiv:2512.19849 |  |  | 4 | Speculative decoding × MoE, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2512.19849) |
| 60 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 61 | arXiv:2312.04916 |  |  | 3 | early-exit-offloading-self-speculative-decoding, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 62 | arXiv:2402.06082 |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 63 | arXiv:2409.01990 |  |  | 3 | KV cache sparsity / paged attention / query-aware selection / LLM serving, inference-systems, moe | [source](https://arxiv.org/abs/2409.01990) |
| 64 | arXiv:2503.08311 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2503.08311) |
| 65 | arXiv:2512.22420 |  |  | 3 | llm-serving-scheduling-disaggregation, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2512.22420) |
| 66 | DOI:10.1109/hoti.2015.13 |  |  | 3 | KVキャッシュオフロード・再計算, RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/hoti.2015.13) |
| 67 | DOI:10.1109/lca.2025.3628325 |  |  | 3 | 12-benchmarking-modeling-emulation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, other-inference-systems | [source](https://doi.org/10.1109/lca.2025.3628325) |
| 68 | DOI:10.1109/sc41405.2020.00024 |  |  | 3 | Adaptive computation／cache-aware MoE, その他システム研究, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/sc41405.2020.00024) |
| 69 | DOI:10.1145/1534530.1534544 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, offload-hierarchical-memory, オフロード／階層メモリ | [source](https://doi.org/10.1145/1534530.1534544) |
| 70 | DOI:10.1145/3620666.3651379 |  |  | 3 | kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 71 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 72 | DOI:10.1145/3731569.3764813 |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764813) |
| 73 | DOI:10.52202/075280-2279 |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, other-inference-systems | [source](https://doi.org/10.52202/075280-2279) |
| 74 | OpenReview:1YDeZU8Lt5 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=1YDeZU8Lt5) |
| 75 | OpenReview:CS2JWaziYr |  |  | 3 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=CS2JWaziYr) |
| 76 | OpenReview:rJl-b3RcF7 |  |  | 3 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=rJl-b3RcF7) |
| 77 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 78 | arXiv:1904.09324 |  |  | 3 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1904.09324) |
| 79 | arXiv:2209.13258 |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 80 | arXiv:2310.05424 |  |  | 3 | speculative decoding / draft-model design, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2310.05424) |
| 81 | arXiv:2311.10122 |  |  | 3 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference | [source](https://arxiv.org/abs/2311.10122) |
| 82 | arXiv:2406.18139 |  |  | 3 | inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2406.18139) |
| 83 | arXiv:2408.15881 |  |  | 3 | Speculative decoding × MoE, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2408.15881) |
| 84 | arXiv:2602.08676 |  |  | 3 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2602.08676) |
| 85 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 86 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 87 | DOI:10.1145/3620665.3640383 |  |  | 3 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, serving-scheduling | [source](https://doi.org/10.1145/3620665.3640383) |
| 88 | DOI:10.1145/3779212.3790226 |  |  | 3 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3779212.3790226) |
| 89 | DOI:10.18653/v1/2023.emnlp-main.825 |  |  | 3 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.825) |
| 90 | DOI:10.18653/v1/w17-4413 |  |  | 3 | Adaptive computation／cache-aware MoE, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/w17-4413) |
| 91 | DOI:10.57967/hf/2497 |  |  | 3 | KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, adaptive-expert-computation-compression | [source](https://doi.org/10.57967/hf/2497) |
| 92 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 93 | OpenReview:MaYzugDmQV |  |  | 3 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 94 | OpenReview:rJ4km2R5t7 |  |  | 3 | MoE inference / task-specific expert pruning / sparse-to-dense conversion, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rJ4km2R5t7) |
| 95 | OpenReview:ul4W26KEKz |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://openreview.net/forum?id=ul4W26KEKz) |
| 96 | arXiv:2606.04101 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2606.04101) |
| 97 | DOI:10.18653/v1/p19-1102 |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference | [source](https://doi.org/10.18653/v1/p19-1102) |
| 98 | OpenReview:KG6aBfGi6e |  |  | 3 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=KG6aBfGi6e) |
| 99 | arXiv:1412.7024 |  |  | 2 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 100 | arXiv:1904.01038 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/1904.01038) |
| 101 | arXiv:1906.04284 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/1906.04284) |
| 102 | arXiv:1910.06188 |  |  | 2 | dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems | [source](https://arxiv.org/abs/1910.06188) |
| 103 | arXiv:2005.14187 |  |  | 2 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 104 | arXiv:2203.06390 |  |  | 2 | Weight Quantization / Compression, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.06390) |
| 105 | arXiv:2210.09461 |  |  | 2 | inference-systems, on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2210.09461) |
| 106 | arXiv:2305.11206 |  |  | 2 | KVキャッシュ最適化／適応圧縮, inference-systems | [source](https://arxiv.org/abs/2305.11206) |
| 107 | arXiv:2306.02707 |  |  | 2 | llm-serving-scheduling-disaggregation, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2306.02707) |
| 108 | arXiv:2307.01952 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2307.01952) |
| 109 | arXiv:2307.09782 |  |  | 2 | LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.09782) |
| 110 | arXiv:2308.09723 |  |  | 2 | Quantization × MoE × Offload, kv-cache-memory | [source](https://arxiv.org/abs/2308.09723) |
| 111 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 112 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 113 | arXiv:2309.14393 |  |  | 2 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 114 | arXiv:2310.00746 |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 115 | arXiv:2310.03744 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 116 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 117 | arXiv:2311.08981 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, survey-speculative-decoding | [source](https://arxiv.org/abs/2311.08981) |
| 118 | arXiv:2311.13171 |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 119 | arXiv:2312.00678 |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 120 | arXiv:2312.07987 |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 121 | arXiv:2312.14852 |  |  | 2 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 122 | arXiv:2401.06080 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.06080) |
| 123 | arXiv:2401.14021 |  |  | 2 | KV Cache Optimization / Compression, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2401.14021) |
| 124 | arXiv:2402.01680 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 125 | arXiv:2402.09353 |  |  | 2 | Conditional Computation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.09353) |
| 126 | arXiv:2402.13116 |  |  | 2 | Speculative Decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.13116) |
| 127 | arXiv:2402.14808 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, inference/11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14808) |
| 128 | arXiv:2402.19427 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2402.19427) |
| 129 | arXiv:2403.06764 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.06764) |
| 130 | arXiv:2403.09347 |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 131 | arXiv:2404.05567 |  |  | 2 | MoE expert pruning / expert merging / redundancy-aware compression / global budget allocation, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2404.05567) |
| 132 | arXiv:2404.09336 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2404.09336) |
| 133 | arXiv:2405.03133 |  |  | 2 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.03133) |
| 134 | arXiv:2405.21015 |  |  | 2 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation, その他システム研究 | [source](https://arxiv.org/abs/2405.21015) |
| 135 | arXiv:2406.02430 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.02430) |
| 136 | arXiv:2406.04594 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.04594) |
| 137 | arXiv:2406.08673 |  |  | 2 | 大規模分散学習・整合学習基盤, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2406.08673) |
| 138 | arXiv:2406.11939 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2406.11939) |
| 139 | arXiv:2406.18820 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18820) |
| 140 | arXiv:2407.07000 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.07000) |
| 141 | arXiv:2407.09816 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.09816) |
| 142 | arXiv:2407.11511 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2407.11511) |
| 143 | arXiv:2408.04323 |  |  | 2 | Agentic inference and serving runtime, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2408.04323) |
| 144 | arXiv:2409.17066 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline | [source](https://arxiv.org/abs/2409.17066) |
| 145 | arXiv:2409.18486 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, prefill-decode disaggregation / attention offloading / LLM serving | [source](https://arxiv.org/abs/2409.18486) |
| 146 | arXiv:2410.02660 |  |  | 2 | kv-cache-optimization-compression, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2410.02660) |
| 147 | arXiv:2410.06511 |  |  | 2 | その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/2410.06511) |
| 148 | arXiv:2410.10989 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, その他システム研究 | [source](https://arxiv.org/abs/2410.10989) |
| 149 | arXiv:2410.14720 |  |  | 2 | MoE compression / expert pruning / neuron-level recombination / expert reconstruction, System-aware KV cache | [source](https://arxiv.org/abs/2410.14720) |
| 150 | arXiv:2410.20650 |  |  | 2 | kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2410.20650) |
| 151 | arXiv:2411.00918 |  |  | 2 | MoE圧縮 / expert merging / subspace alignment / SVD / adaptive clustering, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2411.00918) |
| 152 | arXiv:2411.04468 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2411.04468) |
| 153 | arXiv:2411.04996 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 154 | arXiv:2411.15242 |  |  | 2 | PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management | [source](https://arxiv.org/abs/2411.15242) |
| 155 | arXiv:2412.03603 |  |  | 2 | diffusion language model inference / KV cache / training-free acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.03603) |
| 156 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 157 | arXiv:2412.16545 |  |  | 2 | 10-kv-cache-offload-recomputation, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2412.16545) |
| 158 | arXiv:2501.12370 |  |  | 2 | MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://arxiv.org/abs/2501.12370) |
| 159 | arXiv:2502.03461 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2502.03461) |
| 160 | arXiv:2502.07861 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.07861) |
| 161 | arXiv:2502.12444 |  |  | 2 | 10-kv-cache-offload-recomputation, CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/2502.12444) |
| 162 | arXiv:2502.16880 |  |  | 2 | Speculative decoding × MoE, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2502.16880) |
| 163 | arXiv:2502.17599 |  |  | 2 | KV cache eviction / multimodal KV cache compression / diversity-aware token selection, inference-systems | [source](https://arxiv.org/abs/2502.17599) |
| 164 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 165 | arXiv:2503.13444 |  |  | 2 | kv-cache-offload-recomputation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2503.13444) |
| 166 | arXiv:2503.24047 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2503.24047) |
| 167 | arXiv:2504.05299 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2504.05299) |
| 168 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 169 | arXiv:2504.13914 |  |  | 2 | 推論ベンチマーク・推論大規模言語モデルのサービング評価, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2504.13914) |
| 170 | arXiv:2504.16397 |  |  | 2 | agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2504.16397) |
| 171 | arXiv:2504.18154 |  |  | 2 | prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.18154) |
| 172 | arXiv:2505.06252 |  |  | 2 | kv-cache-offload-recomputation, その他システム研究 | [source](https://arxiv.org/abs/2505.06252) |
| 173 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 174 | arXiv:2505.20353 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2505.20353) |
| 175 | arXiv:2506.01844 |  |  | 2 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2506.01844) |
| 176 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 177 | arXiv:2507.09942 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2507.09942) |
| 178 | arXiv:2507.16731 |  |  | 2 | 05-speculative-decoding-moe, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2507.16731) |
| 179 | arXiv:2508.01002 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2508.01002) |
| 180 | arXiv:2508.07227 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2508.07227) |
| 181 | arXiv:2508.10395 |  |  | 2 | 17-pim-near-data-acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2508.10395) |
| 182 | arXiv:2508.17196 |  |  | 2 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.17196) |
| 183 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 184 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 185 | arXiv:2510.01290 |  |  | 2 | inference/07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2510.01290) |
| 186 | arXiv:2510.06513 |  |  | 2 | offload-hierarchical-memory, オフロード／階層メモリ | [source](https://arxiv.org/abs/2510.06513) |
| 187 | arXiv:2510.15330 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.15330) |
| 188 | arXiv:2510.25741 |  |  | 2 | adaptive-expert-computation-compression, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://arxiv.org/abs/2510.25741) |
| 189 | arXiv:2511.16682 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2511.16682) |
| 190 | arXiv:2511.23404 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2511.23404) |
| 191 | arXiv:2512.05916 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.05916) |
| 192 | arXiv:2512.14142 |  |  | 2 | LLMサービング／スケジューリング／分離, other | [source](https://arxiv.org/abs/2512.14142) |
| 193 | arXiv:2512.20848 |  |  | 2 | PIM / Near-Data Acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.20848) |
| 194 | arXiv:2601.07526 |  |  | 2 | 14-agentic-inference-serving-runtime, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2601.07526) |
| 195 | arXiv:2601.11589 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, disaggregated LLM serving / request routing / learned scheduling | [source](https://arxiv.org/abs/2601.11589) |
| 196 | arXiv:2601.22379 |  |  | 2 | 07-kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2601.22379) |
| 197 | arXiv:2602.21224 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2602.21224) |
| 198 | arXiv:2603.28101 |  |  | 2 | LLM inference simulation / disaggregated serving / performance modeling, agentic LLM serving / pipeline parallelism / serving scheduling / speculative decoding | [source](https://arxiv.org/abs/2603.28101) |
| 199 | arXiv:2605.20315 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2605.20315) |
| 200 | arXiv:2606.22874 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2606.22874) |
| 201 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 202 | DOI:10.1109/dac63849.2025.11133274 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory-kv-offload-cpu-gpu-attention | [source](https://doi.org/10.1109/dac63849.2025.11133274) |
| 203 | DOI:10.1109/hcs61935.2024.10664793 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hcs61935.2024.10664793) |
| 204 | DOI:10.1109/hpca56546.2023.10071120 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://doi.org/10.1109/hpca56546.2023.10071120) |
| 205 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 2 | moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 206 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 207 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 208 | DOI:10.1109/lca.2025.3597323 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1109/lca.2025.3597323) |
| 209 | DOI:10.1109/mm.2023.3256384 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2023.3256384) |
| 210 | DOI:10.1109/mm.2025.3592688 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, moe-parallelism-communication | [source](https://doi.org/10.1109/mm.2025.3592688) |
| 211 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 212 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 213 | DOI:10.1145/224056.224064 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/224056.224064) |
| 214 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 215 | DOI:10.1145/3352460.3358302 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3352460.3358302) |
| 216 | DOI:10.1145/3453483.3454083 |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 217 | DOI:10.1145/3503222.3507738 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3503222.3507738) |
| 218 | DOI:10.1145/3572848.3577479 |  |  | 2 | 02-hardware-accelerators, kernel-runtime-compilation | [source](https://doi.org/10.1145/3572848.3577479) |
| 219 | DOI:10.1145/3575693.3576933 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3575693.3576933) |
| 220 | DOI:10.1145/3600006.3613139 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling | [source](https://doi.org/10.1145/3600006.3613139) |
| 221 | DOI:10.1145/3620666.3651369 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651369) |
| 222 | DOI:10.1145/3636534.3649379 |  |  | 2 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3636534.3649379) |
| 223 | DOI:10.1145/3669940.3707231 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/3669940.3707231) |
| 224 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 225 | DOI:10.1145/3725843.3756041 |  |  | 2 | GPU architecture and tensor-computation orchestration, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://doi.org/10.1145/3725843.3756041) |
| 226 | DOI:10.1145/3767742 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3767742) |
| 227 | DOI:10.1145/3779212.3790236 |  |  | 2 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790236) |
| 228 | DOI:10.1177/1094342005051521 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators | [source](https://doi.org/10.1177/1094342005051521) |
| 229 | DOI:10.1609/aaai.v40i36.40255 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.1609/aaai.v40i36.40255) |
| 230 | DOI:10.18653/v1/2022.findings-acl.189 |  |  | 2 | Conditional Computation, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/2022.findings-acl.189) |
| 231 | DOI:10.18653/v1/2024.findings-acl.57 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.57) |
| 232 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 233 | DOI:10.48550/arxiv.2507.11851 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, speculative-decoding | [source](https://doi.org/10.48550/arxiv.2507.11851) |
| 234 | DOI:10.52202/075280-1506 |  |  | 2 | early-exit-offloading-self-speculative-decoding, kv-cache-optimization-compression | [source](https://doi.org/10.52202/075280-1506) |
| 235 | DOI:10.52202/079017-3180 |  |  | 2 | adaptive-expert-computation-compression, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.52202/079017-3180) |
| 236 | DOI:10.57967/hf/0638 |  |  | 2 | inference-systems, survey-speculative-decoding | [source](https://doi.org/10.57967/hf/0638) |
| 237 | OpenReview:8Wuvhh0LYW |  |  | 2 | 17-pim-near-data-acceleration, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=8Wuvhh0LYW) |
| 238 | OpenReview:cJd1BgZ9CS |  |  | 2 | speculative-decoding, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://openreview.net/forum?id=cJd1BgZ9CS) |
| 239 | OpenReview:FAeU7516MR |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE | [source](https://openreview.net/forum?id=FAeU7516MR) |
| 240 | OpenReview:H4DqfPSibmx |  |  | 2 | Speculative decoding × MoE, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=H4DqfPSibmx) |
| 241 | OpenReview:JFygzwx8SJ |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=JFygzwx8SJ) |
| 242 | OpenReview:mtSSFiqW6y |  |  | 2 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=mtSSFiqW6y) |
| 243 | OpenReview:R0SoZvqXyQ |  |  | 2 | llm-serving-scheduling-disaggregation, serving-scheduling | [source](https://openreview.net/forum?id=R0SoZvqXyQ) |
| 244 | OpenReview:rsY6J3ZaTF |  |  | 2 | speculative decoding / draft-model design, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=rsY6J3ZaTF) |
| 245 | OpenReview:vXxardq6db |  |  | 2 | Quantization × MoE × Offload, 投機的デコード／MoE | [source](https://openreview.net/forum?id=vXxardq6db) |
| 246 | OpenReview:YolJOZOGhI |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://openreview.net/forum?id=YolJOZOGhI) |
| 247 | arXiv:1809.08887 |  |  | 2 | 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/1809.08887) |
| 248 | arXiv:2009.14167 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2009.14167) |
| 249 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 250 | arXiv:2305.14160 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 251 | arXiv:2404.08698 |  |  | 2 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2404.08698) |
| 252 | arXiv:2408.05636 |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2408.05636) |
| 253 | arXiv:2502.07780 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next | [source](https://arxiv.org/abs/2502.07780) |
| 254 | arXiv:2511.19269 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://arxiv.org/abs/2511.19269) |
| 255 | arXiv:2602.08404 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2602.08404) |
| 256 | DOI:10.1109/infocom53939.2023.10228874 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1109/infocom53939.2023.10228874) |
| 257 | DOI:10.1145/3786655 |  |  | 2 | kv-cache-reuse-position-independent-caching | [source](https://doi.org/10.1145/3786655) |
| 258 | DOI:10.18653/v1/2023.emnlp-main.907 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/2023.emnlp-main.907) |
| 259 | DOI:10.18653/v1/2024.naacl-long.222 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.naacl-long.222) |
| 260 | DOI:10.18653/v1/2025.naacl-long.328 |  |  | 2 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://doi.org/10.18653/v1/2025.naacl-long.328) |
| 261 | OpenReview:7zNYY1E2fq |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論 | [source](https://openreview.net/forum?id=7zNYY1E2fq) |
| 262 | OpenReview:D9cnZNZfxX |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=D9cnZNZfxX) |
| 263 | OpenReview:RlqYCpTu1P |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=RlqYCpTu1P) |
| 264 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 265 | arXiv:1710.09412 |  |  | 2 |  | [source](https://arxiv.org/abs/1710.09412) |
| 266 | arXiv:2311.04902 |  |  | 2 |  | [source](https://arxiv.org/abs/2311.04902) |
| 267 | DOI:10.18653/v1/2021.sustainlp-1.5 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2021.sustainlp-1.5) |
| 268 | DOI:10.48550/arxiv.2304.08354 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2304.08354) |
| 269 | OpenReview:2GmDdhBdDk |  |  | 2 |  | [source](https://openreview.net/forum?id=2GmDdhBdDk) |
| 270 | OpenReview:FJFVmeXusW |  |  | 2 |  | [source](https://openreview.net/forum?id=FJFVmeXusW) |
| 271 | OpenReview:QV79qiKAjD |  |  | 2 |  | [source](https://openreview.net/forum?id=QV79qiKAjD) |
| 272 | arXiv:1205.2618 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 273 | arXiv:1211.3711 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1211.3711) |
| 274 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 275 | arXiv:1402.3511 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1402.3511) |
| 276 | arXiv:1410.0759 |  |  | 1 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン | [source](https://arxiv.org/abs/1410.0759) |
| 277 | arXiv:1505.05571 |  |  | 1 | MoE数値再現性・決定論的推論・実行時互換性 | [source](https://arxiv.org/abs/1505.05571) |
| 278 | arXiv:1506.03099 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1506.03099) |
| 279 | arXiv:1511.01837 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 280 | arXiv:1511.06939 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 281 | arXiv:1602.01528 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1602.01528) |
| 282 | arXiv:1602.02830 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1602.02830) |
| 283 | arXiv:1603.05118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1603.05118) |
| 284 | arXiv:1604.01696 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1604.01696) |
| 285 | arXiv:1609.05140 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1609.05140) |
| 286 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 287 | arXiv:1611.01578 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 288 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 289 | arXiv:1702.02815 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1702.02815) |
| 290 | arXiv:1703.05160 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 291 | arXiv:1704.04684 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/1704.04684) |
| 292 | arXiv:1704.05426 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 293 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 294 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 295 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 296 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 297 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 298 | arXiv:1710.09437 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1710.09437) |
| 299 | arXiv:1711.02782 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.02782) |
| 300 | arXiv:1711.05073 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1711.05073) |
| 301 | arXiv:1712.01887 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1712.01887) |
| 302 | arXiv:1712.09763 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.09763) |
| 303 | arXiv:1802.05365 |  |  | 1 | Training Offload / Memory Systems | [source](https://arxiv.org/abs/1802.05365) |
| 304 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 305 | arXiv:1804.06087 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 306 | arXiv:1806.02847 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 307 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 308 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 309 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 310 | arXiv:1810.00602 |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/1810.00602) |
| 311 | arXiv:1810.05291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.05291) |
| 312 | arXiv:1811.01088 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1811.01088) |
| 313 | arXiv:1811.08886 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/1811.08886) |
| 314 | arXiv:1812.09764 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1812.09764) |
| 315 | arXiv:1902.03383 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/1902.03383) |
| 316 | arXiv:1902.09113 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1902.09113) |
| 317 | arXiv:1903.01611 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1903.01611) |
| 318 | arXiv:1903.05662 |  |  | 1 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference | [source](https://arxiv.org/abs/1903.05662) |
| 319 | arXiv:1904.10631 |  |  | 1 | long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/1904.10631) |
| 320 | arXiv:1905.07799 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 321 | arXiv:1906.05714 |  |  | 1 | 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/1906.05714) |
| 322 | arXiv:1906.11024 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/1906.11024) |
| 323 | arXiv:1907.12009 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1907.12009) |
| 324 | arXiv:1908.10084 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1908.10084) |
| 325 | arXiv:1909.03368 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1909.03368) |
| 326 | arXiv:1909.10351 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1909.10351) |
| 327 | arXiv:1910.04732 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1910.04732) |
| 328 | arXiv:1910.06360 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 329 | arXiv:1911.02116 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 330 | arXiv:1911.04610 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1911.04610) |
| 331 | arXiv:1911.08772 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1911.08772) |
| 332 | arXiv:2001.01072 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/2001.01072) |
| 333 | arXiv:2002.08155 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2002.08155) |
| 334 | arXiv:2002.10345 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.10345) |
| 335 | arXiv:2002.11054 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2002.11054) |
| 336 | arXiv:2003.07013 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.07013) |
| 337 | arXiv:2003.12462 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2003.12462) |
| 338 | arXiv:2004.08900 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 339 | arXiv:2004.11867 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 340 | arXiv:2005.00770 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00770) |
| 341 | arXiv:2005.07647 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2005.07647) |
| 342 | arXiv:2006.06762 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2006.06762) |
| 343 | arXiv:2006.10901 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2006.10901) |
| 344 | arXiv:2006.12467 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 345 | arXiv:2007.07779 |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 346 | arXiv:2008.00051 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 347 | arXiv:2009.06106 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 348 | arXiv:2009.08034 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2009.08034) |
| 349 | arXiv:2009.09736 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2009.09736) |
| 350 | arXiv:2010.02502 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2010.02502) |
| 351 | arXiv:2010.03379 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03379) |
| 352 | arXiv:2010.03983 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03983) |
| 353 | arXiv:2010.11443 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2010.11443) |
| 354 | arXiv:2010.16248 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2010.16248) |
| 355 | arXiv:2011.04393 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2011.04393) |
| 356 | arXiv:2012.07463 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2012.07463) |
| 357 | arXiv:2012.15613 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2012.15613) |
| 358 | arXiv:2012.15833 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2012.15833) |
| 359 | arXiv:2101.09671 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2101.09671) |
| 360 | arXiv:2102.06621 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2102.06621) |
| 361 | arXiv:2102.08602 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2102.08602) |
| 362 | arXiv:2102.11972 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2102.11972) |
| 363 | arXiv:2103.03404 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2103.03404) |
| 364 | arXiv:2104.08771 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2104.08771) |
| 365 | arXiv:2105.03036 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.03036) |
| 366 | arXiv:2105.11098 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2105.11098) |
| 367 | arXiv:2105.14940 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.14940) |
| 368 | arXiv:2106.04489 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.04489) |
| 369 | arXiv:2106.07139 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2106.07139) |
| 370 | arXiv:2106.15339 |  |  | 1 | MoE推論／CPU-GPU協調オフロード／階層メモリ／性能モデル／高スループットバッチ推論 | [source](https://arxiv.org/abs/2106.15339) |
| 371 | arXiv:2107.10989 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2107.10989) |
| 372 | arXiv:2108.05036 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2108.05036) |
| 373 | arXiv:2109.00859 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2109.00859) |
| 374 | arXiv:2109.05472 |  |  | 1 | 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2109.05472) |
| 375 | arXiv:2109.10686 |  |  | 1 | 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2109.10686) |
| 376 | arXiv:2109.11817 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2109.11817) |
| 377 | arXiv:2110.06296 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2110.06296) |
| 378 | arXiv:2110.09132 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.09132) |
| 379 | arXiv:2111.00160 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 380 | arXiv:2111.00856 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2111.00856) |
| 381 | arXiv:2112.02958 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2112.02958) |
| 382 | arXiv:2112.06749 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2112.06749) |
| 383 | arXiv:2112.10769 |  |  | 1 | kv-cache-memory | [source](https://arxiv.org/abs/2112.10769) |
| 384 | arXiv:2112.14938 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2112.14938) |
| 385 | arXiv:2201.10520 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2201.10520) |
| 386 | arXiv:2202.05239 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2202.05239) |
| 387 | arXiv:2202.07848 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2202.07848) |
| 388 | arXiv:2202.10447 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2202.10447) |
| 389 | arXiv:2203.00386 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2203.00386) |
| 390 | arXiv:2203.05740 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2203.05740) |
| 391 | arXiv:2203.09509 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.09509) |
| 392 | arXiv:2203.17189 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.17189) |
| 393 | arXiv:2204.05832 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2204.05832) |
| 394 | arXiv:2204.07675 |  |  | 1 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2204.07675) |
| 395 | arXiv:2204.11574 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2204.11574) |
| 396 | arXiv:2205.04934 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2205.04934) |
| 397 | arXiv:2205.06126 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2205.06126) |
| 398 | arXiv:2205.11380 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2205.11380) |
| 399 | arXiv:2205.12701 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12701) |
| 400 | arXiv:2206.02845 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2206.02845) |
| 401 | arXiv:2207.05952 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 402 | arXiv:2207.12598 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2207.12598) |
| 403 | arXiv:2208.03299 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2208.03299) |
| 404 | arXiv:2208.09225 |  |  | 1 | 投機的デコード・バッチ推論 | [source](https://arxiv.org/abs/2208.09225) |
| 405 | arXiv:2209.07858 |  |  | 1 | Mixture-of-Experts inference / processing-in-memory / heterogeneous scheduling / expert placement | [source](https://arxiv.org/abs/2209.07858) |
| 406 | arXiv:2209.12356 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2209.12356) |
| 407 | arXiv:2210.02747 |  |  | 1 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference | [source](https://arxiv.org/abs/2210.02747) |
| 408 | arXiv:2210.03350 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2210.03350) |
| 409 | arXiv:2210.07535 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.07535) |
| 410 | arXiv:2210.11948 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 411 | arXiv:2210.14793 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 412 | arXiv:2211.00107 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.00107) |
| 413 | arXiv:2211.05719 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2211.05719) |
| 414 | arXiv:2211.07349 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.07349) |
| 415 | arXiv:2211.10435 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2211.10435) |
| 416 | arXiv:2211.16750 |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2211.16750) |
| 417 | arXiv:2212.03613 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2212.03613) |
| 418 | arXiv:2212.04356 |  |  | 1 | エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2212.04356) |
| 419 | arXiv:2212.05339 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2212.05339) |
| 420 | arXiv:2212.10403 |  |  | 1 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2212.10403) |
| 421 | arXiv:2212.10511 |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2212.10511) |
| 422 | arXiv:2301.00407 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.00407) |
| 423 | arXiv:2301.05217 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2301.05217) |
| 424 | arXiv:2301.07069 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2301.07069) |
| 425 | arXiv:2301.11233 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2301.11233) |
| 426 | arXiv:2301.12900 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2301.12900) |
| 427 | arXiv:2302.02599 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.02599) |
| 428 | arXiv:2302.06590 |  |  | 1 | agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2302.06590) |
| 429 | arXiv:2302.09419 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.09419) |
| 430 | arXiv:2302.10866 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2302.10866) |
| 431 | arXiv:2302.12066 |  |  | 1 | foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2302.12066) |
| 432 | arXiv:2302.13214 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.13214) |
| 433 | arXiv:2303.02141 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2303.02141) |
| 434 | arXiv:2303.05510 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2303.05510) |
| 435 | arXiv:2303.06296 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2303.06296) |
| 436 | arXiv:2303.10130 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2303.10130) |
| 437 | arXiv:2303.11381 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11381) |
| 438 | arXiv:2303.15375 |  |  | 1 | cpu-offload | [source](https://arxiv.org/abs/2303.15375) |
| 439 | arXiv:2303.17564 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.17564) |
| 440 | arXiv:2304.01468 |  |  | 1 | SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2304.01468) |
| 441 | arXiv:2304.03094 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2304.03094) |
| 442 | arXiv:2304.03589 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2304.03589) |
| 443 | arXiv:2304.05128 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2304.05128) |
| 444 | arXiv:2304.08244 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2304.08244) |
| 445 | arXiv:2304.10411 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2304.10411) |
| 446 | arXiv:2304.12244 |  |  | 1 | multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 447 | arXiv:2304.15010 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 448 | arXiv:2305.02538 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 449 | arXiv:2305.04044 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2305.04044) |
| 450 | arXiv:2305.06984 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.06984) |
| 451 | arXiv:2305.08367 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.08367) |
| 452 | arXiv:2305.10266 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.10266) |
| 453 | arXiv:2305.12870 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.12870) |
| 454 | arXiv:2305.13450 |  |  | 1 | dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2305.13450) |
| 455 | arXiv:2305.14481 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2305.14481) |
| 456 | arXiv:2305.14806 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2305.14806) |
| 457 | arXiv:2305.15294 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2305.15294) |
| 458 | arXiv:2305.16635 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2305.16635) |
| 459 | arXiv:2305.17455 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.17455) |
| 460 | arXiv:2305.19414 |  |  | 1 | MoEエキスパート予測・キャッシュ・プリフェッチ | [source](https://arxiv.org/abs/2305.19414) |
| 461 | arXiv:2306.02224 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2306.02224) |
| 462 | arXiv:2306.03805 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2306.03805) |
| 463 | arXiv:2306.05179 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2306.05179) |
| 464 | arXiv:2306.08162 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2306.08162) |
| 465 | arXiv:2306.12420 |  |  | 1 | multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2306.12420) |
| 466 | arXiv:2306.16636 |  |  | 1 | sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2306.16636) |
| 467 | arXiv:2307.02839 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2307.02839) |
| 468 | arXiv:2307.05300 |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2307.05300) |
| 469 | arXiv:2307.07735 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.07735) |
| 470 | arXiv:2307.12169 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12169) |
| 471 | arXiv:2307.15190 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2307.15190) |
| 472 | arXiv:2308.03421 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2308.03421) |
| 473 | arXiv:2308.07317 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.07317) |
| 474 | arXiv:2308.12043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2308.12043) |
| 475 | arXiv:2309.07418 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2309.07418) |
| 476 | arXiv:2309.14021 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.14021) |
| 477 | arXiv:2310.01812 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.01812) |
| 478 | arXiv:2310.04361 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2310.04361) |
| 479 | arXiv:2310.05421 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.05421) |
| 480 | arXiv:2310.07147 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.07147) |
| 481 | arXiv:2310.10046 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.10046) |
| 482 | arXiv:2310.12670 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.12670) |
| 483 | arXiv:2310.16355 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2310.16355) |
| 484 | arXiv:2310.19852 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.19852) |
| 485 | arXiv:2311.02462 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2311.02462) |
| 486 | arXiv:2311.07989 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2311.07989) |
| 487 | arXiv:2311.11586 |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2311.11586) |
| 488 | arXiv:2311.13381 |  |  | 1 | survey-edge-llm | [source](https://arxiv.org/abs/2311.13381) |
| 489 | arXiv:2312.00858 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.00858) |
| 490 | arXiv:2312.03414 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2312.03414) |
| 491 | arXiv:2312.05253 |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2312.05253) |
| 492 | arXiv:2312.11819 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11819) |
| 493 | arXiv:2401.04044 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.04044) |
| 494 | arXiv:2402.08644 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.08644) |
| 495 | arXiv:2402.13485 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2402.13485) |
| 496 | arXiv:2403.00858 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2403.00858) |
| 497 | arXiv:2403.02545 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2403.02545) |
| 498 | arXiv:2403.03432 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2403.03432) |
| 499 | arXiv:2403.04797 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2403.04797) |
| 500 | arXiv:2403.06659 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.06659) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

