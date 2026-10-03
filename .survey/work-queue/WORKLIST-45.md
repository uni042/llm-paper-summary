# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-03T09:08:45+00:00`

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

未判定総数: **7010** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3458817.3476209 |  |  | 19 | Conditional Computation, GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, distributed LLM inference / communication-aware serving, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-offload-routing, other-inference-systems, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime, オフロード／階層メモリ | [source](https://doi.org/10.1145/3458817.3476209) |
| 2 | arXiv:2406.12793 |  |  | 17 | 07-kv-cache-optimization-compression, Edge / On-device LLM Systems, KV cache compression / sparse attention / long-context inference, KVキャッシュ退避／長文推論／KV選択／KV量子化, Long-context serving / KV cache benchmark, inference-systems, llm-serving-scheduling-disaggregation, その他システム研究 | [source](https://arxiv.org/abs/2406.12793) |
| 3 | arXiv:2309.00071 |  |  | 16 | 07-kv-cache-optimization-compression, 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Adaptive computation／cache-aware MoE, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, inference-systems, kv-cache-offload-recomputation, moe | [source](https://arxiv.org/abs/2309.00071) |
| 4 | arXiv:2305.13048 |  |  | 15 | KV Cache Offload / Recomputation, edge-on-device-llm-systems, inference-systems, kv-cache, kv-cache-optimization-compression, prefix caching / hybrid attention-SSM serving, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling, 推論エンジン／推論基盤, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2305.13048) |
| 5 | OpenReview:Byj72udxe |  |  | 14 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, Offload / Hierarchical Memory, Quantization × MoE × Offload, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://openreview.net/forum?id=Byj72udxe) |
| 6 | arXiv:2405.16406 |  |  | 14 | 11-llm-serving-scheduling-disaggregation, 17-pim-near-data-acceleration, FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV cache quantization / rotation-based compression / MoE expert offloading / consumer local inference, Weight Quantization / Compression, inference-systems, kv-cache-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2405.16406) |
| 7 | DOI:10.1145/3669940.3707267 |  |  | 13 | KV Cache Optimization / Compression, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Offload / Hierarchical Memory, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, hierarchical-memory-kv-offload-cpu-gpu-attention, moe-inference-expert-placement-caching, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://doi.org/10.1145/3669940.3707267) |
| 8 | OpenReview:nZeVKeeFYf9 |  |  | 13 | 18-vla-inference-quantization-evaluation, KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, llm-serving-systems, その他システム研究 | [source](https://openreview.net/forum?id=nZeVKeeFYf9) |
| 9 | OpenReview:cFu7ze7xUm |  |  | 13 | 13-sparse-attention, KV Cache Optimization / Compression, Long-context serving / KV cache benchmark, Prefill/Decode Disaggregation / Selective KV Transfer, other-inference-systems | [source](https://openreview.net/forum?id=cFu7ze7xUm) |
| 10 | arXiv:2309.12307 |  |  | 12 | Conditional Computation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference, KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ, cpu-offload, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, inference-systems, multi-tenant LoRA serving / CPU-assisted inference / rank-aware scheduling | [source](https://arxiv.org/abs/2309.12307) |
| 11 | arXiv:2305.16300 |  |  | 12 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/2305.16300) |
| 12 | arXiv:2501.08313 |  |  | 12 | 13-sparse-attention, inference-systems, moe-parallelism-communication, prefix caching / hybrid attention-SSM serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.08313) |
| 13 | arXiv:2309.04255 |  |  | 11 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, Speculative Decoding, edge-on-device-llm-systems, inference-systems, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 14 | DOI:10.48550/arxiv.2501.14743 |  |  | 11 | 11-llm-serving-scheduling-disaggregation, 12-moe-parallelism-communication, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, LLM Serving / Scheduling / Disaggregation, LLM serving / prefill-decode disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2501.14743) |
| 15 | DOI:10.18653/v1/2020.coling-main.580 |  |  | 11 | 10-kv-キャッシュ-オフロード-recomputation, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, Prefill/Decode Disaggregation / Selective KV Transfer, inference-systems | [source](https://doi.org/10.18653/v1/2020.coling-main.580) |
| 16 | arXiv:2407.12391 |  |  | 10 | SLO-aware LLM serving scheduling, System-aware KV cache, disaggregated LLM serving / request routing / learned scheduling, inference-systems, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.12391) |
| 17 | arXiv:2101.00190 |  |  | 10 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2101.00190) |
| 18 | DOI:10.1145/3394486.3406703 |  |  | 10 | GPU collective communication / communication compression / LLM serving disaggregation, KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems, kernel-runtime-compilation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3394486.3406703) |
| 19 | DOI:10.48550/arxiv.2402.08268 |  |  | 10 | 10-kv-キャッシュ-オフロード-recomputation, serving-scheduling | [source](https://doi.org/10.48550/arxiv.2402.08268) |
| 20 | arXiv:2503.20215 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, Sparse Attention / VLM Inference, Speculative Decoding, batch inference / event-driven runtime / MoE serving / offload, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2503.20215) |
| 21 | DOI:10.64434/tml.20250910 |  |  | 9 | Agentic Serving Benchmarking, Inference Kernel / Determinism, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 22 | arXiv:2210.11416 |  |  | 9 | 99-other-inference-systems, Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, inference-systems, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 23 | arXiv:2405.14366 |  |  | 9 | KV Cache Offload / Retrieval / Compression, KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, inference-systems, kv-cache-offload-recomputation, other-inference-systems | [source](https://arxiv.org/abs/2405.14366) |
| 24 | DOI:10.5281/zenodo.10256836 |  |  | 9 | Adaptive Expert Computation / Compression, Conditional Computation, Expert Prefetch, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation, 投機復号・自己投機・ループ型Transformer・推論パイプライン, 投機的復号・Orthrus・推論再現性・数値精度 | [source](https://doi.org/10.5281/zenodo.10256836) |
| 25 | arXiv:2203.14685 |  |  | 9 | Adaptive Expert Computation / Compression, MoE推論・エキスパート配置・全対全通信スケジューリング・異種GPU, inference-systems, survey-moe-inference-optimization, その他システム研究 | [source](https://arxiv.org/abs/2203.14685) |
| 26 | arXiv:2401.03462 |  |  | 9 | 07-kv-キャッシュ-optimization-compression, KV Cache Compression / Long Context, KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り, inference-systems | [source](https://arxiv.org/abs/2401.03462) |
| 27 | DOI:10.1145/3676641.3716278 |  |  | 8 | 08-edge-on-device-llm-systems, 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, inference-systems, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 28 | arXiv:2405.05465 |  |  | 8 | KV Cache Offload / Recomputation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, disaggregated LLM serving / request routing / learned scheduling, inference-systems, kv-cache-memory-management, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2405.05465) |
| 29 | DOI:10.1147/sj.52.0078 |  |  | 8 | 14-agentic-inference-serving-runtime, KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, MoE expert offloading / predictive prefetch and cache management, Offload / Hierarchical Memory, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1147/sj.52.0078) |
| 30 | arXiv:2303.08302 |  |  | 8 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Weight Quantization / Compression, inference-systems, offload-hierarchical-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2303.08302) |
| 31 | OpenReview:chfJJYC3iL |  |  | 8 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, Other Inference Systems / Lossless Parallel Decoding, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=chfJJYC3iL) |
| 32 | arXiv:2306.02272 |  |  | 8 | LLM inference surveys、roofline performance analysis, Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2306.02272) |
| 33 | DOI:10.1145/3620666.3651329 |  |  | 7 | KV Cache Offload / Recomputation, MoE推論／CPU-GPU協調オフロード／階層メモリ／性能モデル／高スループットバッチ推論, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, inference-systems, llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3620666.3651329) |
| 34 | arXiv:2110.04260 |  |  | 7 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference systems / expert parallelism / model compression / knowledge distillation, Quantization × MoE × Offload, inference-systems, その他システム研究 | [source](https://arxiv.org/abs/2110.04260) |
| 35 | arXiv:2509.17765 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, inference-systems, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 36 | arXiv:2309.05463 |  |  | 7 | Weight Quantization / Compression, inference-systems, survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 37 | DOI:10.1162/tacl_a_00023 |  |  | 7 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1162/tacl_a_00023) |
| 38 | OpenReview:uccHPGDlao |  |  | 7 | 05-speculative-decoding-moe, Speculative decoding × MoE, inference-systems, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 39 | arXiv:2504.09285 |  |  | 7 | LLM serving / prefill-decode disaggregation, llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.09285) |
| 40 | DOI:10.1162/tacl_a_00276 |  |  | 7 | Speculative Decoding / Parallel Inference Systems, inference-systems, survey-speculative-decoding | [source](https://doi.org/10.1162/tacl_a_00276) |
| 41 | arXiv:2402.14034 |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 42 | DOI:10.1145/3695053.3731008 |  |  | 6 | 17-pim-near-data-acceleration, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 43 | arXiv:2504.21318 |  |  | 6 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 44 | OpenReview:xXTkbTBmqq |  |  | 6 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分, Quantization × MoE × Offload, inference-systems, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=xXTkbTBmqq) |
| 45 | arXiv:2402.18158 |  |  | 6 | Quantization × MoE × Offload, Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.18158) |
| 46 | DOI:10.1109/ispass57527.2023.00035 |  |  | 6 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass57527.2023.00035) |
| 47 | arXiv:2012.15701 |  |  | 6 | Conditional Computation, Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2012.15701) |
| 48 | arXiv:2403.12031 |  |  | 6 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 49 | DOI:10.18653/v1/2023.emnlp-main.825 |  |  | 6 | 07-kv-cache-optimization-compression, Long-context serving / KV cache benchmark, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.825) |
| 50 | OpenReview:7Bywt2mQsCe |  |  | 6 | KV Cache Optimization / Compression, Speculative decoding × MoE, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Bywt2mQsCe) |
| 51 | arXiv:1904.09324 |  |  | 6 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1904.09324) |
| 52 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 53 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 54 | DOI:10.1145/3620666.3651352 |  |  | 5 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, inference-systems, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 55 | arXiv:1603.08983 |  |  | 5 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 56 | DOI:10.1109/micro56248.2022.00051 |  |  | 5 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, inference-systems, kv-cache-memory | [source](https://doi.org/10.1109/micro56248.2022.00051) |
| 57 | OpenReview:Bl8u7ZRlbM |  |  | 5 | 11-llm-serving-scheduling-disaggregation, KV cache reuse / context caching / multi-tenant LLM serving / selective recomputation, agent serving / KV-cache reuse / latent communication / DAG workflows, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://openreview.net/forum?id=Bl8u7ZRlbM) |
| 58 | arXiv:2302.10866 |  |  | 5 | Conditional Computation, inference-systems, training-memory-systems | [source](https://arxiv.org/abs/2302.10866) |
| 59 | arXiv:2405.21075 |  |  | 5 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2405.21075) |
| 60 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 61 | arXiv:1909.11556 |  |  | 5 | inference-systems, speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 62 | arXiv:2406.18139 |  |  | 5 | inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2406.18139) |
| 63 | DOI:10.18653/v1/2023.findings-emnlp.936 |  |  | 5 | Adaptive Expert Computation / Compression, inference-systems | [source](https://doi.org/10.18653/v1/2023.findings-emnlp.936) |
| 64 | arXiv:1910.13461 |  |  | 5 | inference-systems | [source](https://arxiv.org/abs/1910.13461) |
| 65 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 66 | arXiv:2412.16434 |  |  | 4 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation, other-inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2412.16434) |
| 67 | arXiv:2506.06266 |  |  | 4 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-offload-recomputation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2506.06266) |
| 68 | DOI:10.1109/hpca53966.2022.00082 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, inference-systems, kv-cache-memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca53966.2022.00082) |
| 69 | DOI:10.1109/tmc.2024.3513457 |  |  | 4 | 05-speculative-decoding-moe, 08-edge-on-device-llm-systems, Edge / On-device LLM Systems, hardware-accelerators | [source](https://doi.org/10.1109/tmc.2024.3513457) |
| 70 | DOI:10.18653/v1/2025.acl-long.1126 |  |  | 4 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics, dynamic-pd-disaggregation, kv-cache-offload-recomputation | [source](https://doi.org/10.18653/v1/2025.acl-long.1126) |
| 71 | OpenReview:1qvx610Cu7 |  |  | 4 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, inference-systems, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 72 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 73 | arXiv:2310.09259 |  |  | 4 | 11-llm-serving-scheduling-disaggregation, Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2310.09259) |
| 74 | arXiv:2401.14021 |  |  | 4 | KV Cache Optimization / Compression, inference-systems, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2401.14021) |
| 75 | arXiv:2406.06484 |  |  | 4 | inference-systems, linear attention / delta-rule associative memory / state-space models / Bayesian filtering, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2406.06484) |
| 76 | arXiv:2410.20650 |  |  | 4 | inference-systems, kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2410.20650) |
| 77 | arXiv:2412.14468 |  |  | 4 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2412.14468) |
| 78 | arXiv:2504.16397 |  |  | 4 | agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2504.16397) |
| 79 | arXiv:2602.02276 |  |  | 4 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2602.02276) |
| 80 | DOI:10.1145/3503222.3507738 |  |  | 4 | inference-systems, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3503222.3507738) |
| 81 | DOI:10.1145/3627703.3629578 |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, inference-systems, serving-scheduling | [source](https://doi.org/10.1145/3627703.3629578) |
| 82 | DOI:10.18653/v1/w17-4413 |  |  | 4 | Adaptive computation／cache-aware MoE, adaptive-expert-computation-compression, inference-systems | [source](https://doi.org/10.18653/v1/w17-4413) |
| 83 | OpenReview:cSimKw5p6R |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, agentic workflow serving / workflow physical planning / adaptive serving, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://openreview.net/forum?id=cSimKw5p6R) |
| 84 | OpenReview:zAdUB0aCTQ |  |  | 4 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://openreview.net/forum?id=zAdUB0aCTQ) |
| 85 | arXiv:2002.11054 |  |  | 4 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2002.11054) |
| 86 | arXiv:2304.12244 |  |  | 4 | inference-systems, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 87 | arXiv:2408.10188 |  |  | 4 | dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, inference-systems | [source](https://arxiv.org/abs/2408.10188) |
| 88 | arXiv:2512.19849 |  |  | 4 | Speculative decoding × MoE, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2512.19849) |
| 89 | DOI:10.1145/3581784.3607062 |  |  | 4 | Sparse Attention, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1145/3581784.3607062) |
| 90 | DOI:10.18653/v1/d19-1454 |  |  | 4 | Conditional Computation, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/d19-1454) |
| 91 | OpenReview:pPjZIOuQuF |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, 13-sparse-attention | [source](https://openreview.net/forum?id=pPjZIOuQuF) |
| 92 | arXiv:2212.14052 |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2212.14052) |
| 93 | arXiv:2410.02694 |  |  | 4 | Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2410.02694) |
| 94 | DOI:10.18653/v1/p19-1102 |  |  | 4 | KV-cache compression / attention-based token selection / long-context inference | [source](https://doi.org/10.18653/v1/p19-1102) |
| 95 | arXiv:2312.04927 |  |  | 4 |  | [source](https://arxiv.org/abs/2312.04927) |
| 96 | arXiv:1910.06188 |  |  | 3 | Weight Quantization / Compression, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems | [source](https://arxiv.org/abs/1910.06188) |
| 97 | arXiv:2306.02561 |  |  | 3 | LLM routing、hybrid inference、quality-aware model selection, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 98 | arXiv:2309.02784 |  |  | 3 | LLM inference surveys、roofline performance analysis, Structured Pruning / Architecture Search, inference-systems | [source](https://arxiv.org/abs/2309.02784) |
| 99 | arXiv:2309.15531 |  |  | 3 | KV cache quantization / long-context inference / activation compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.15531) |
| 100 | arXiv:2401.07339 |  |  | 3 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.07339) |
| 101 | arXiv:2403.05525 |  |  | 3 | Quantization × MoE × Offload, inference-systems, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 102 | arXiv:2405.03133 |  |  | 3 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, inference-systems, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.03133) |
| 103 | arXiv:2406.11931 |  |  | 3 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.11931) |
| 104 | arXiv:2407.12821 |  |  | 3 | Agentic Serving Benchmarking, inference-systems, other-inference-systems | [source](https://arxiv.org/abs/2407.12821) |
| 105 | arXiv:2409.18486 |  |  | 3 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, inference-systems, prefill-decode disaggregation / attention offloading / LLM serving | [source](https://arxiv.org/abs/2409.18486) |
| 106 | arXiv:2410.10762 |  |  | 3 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10762) |
| 107 | arXiv:2411.02335 |  |  | 3 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, adaptive expert computation / compression; end-side sparse MoE, inference-systems | [source](https://arxiv.org/abs/2411.02335) |
| 108 | arXiv:2501.19309 |  |  | 3 | federated inference / speculative decoding / communication-efficient LLM inference, inference-systems, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2501.19309) |
| 109 | arXiv:2503.01586 |  |  | 3 | KV cache quantization / RoPE-aware compression / packed attention serving, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2503.01586) |
| 110 | arXiv:2504.12216 |  |  | 3 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, inference-systems, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2504.12216) |
| 111 | arXiv:2507.11948 |  |  | 3 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2507.11948) |
| 112 | DOI:10.1007/s11432-024-4235-6 |  |  | 3 | MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / null experts / data sparsity / multimodal MoE, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1007/s11432-024-4235-6) |
| 113 | DOI:10.1109/lca.2025.3628325 |  |  | 3 | 12-benchmarking-modeling-emulation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, other-inference-systems | [source](https://doi.org/10.1109/lca.2025.3628325) |
| 114 | DOI:10.1109/sc41405.2020.00024 |  |  | 3 | Adaptive computation／cache-aware MoE, その他システム研究, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/sc41405.2020.00024) |
| 115 | DOI:10.1145/3352460.3358302 |  |  | 3 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators, inference-systems | [source](https://doi.org/10.1145/3352460.3358302) |
| 116 | DOI:10.1145/3492321.3519584 |  |  | 3 | MoE serving resilience / decoupled attention-expert serving / KV checkpointing, inference-systems, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3492321.3519584) |
| 117 | DOI:10.1145/3676641.3716025 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, inference-systems, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://doi.org/10.1145/3676641.3716025) |
| 118 | DOI:10.1145/3731569.3764813 |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764813) |
| 119 | DOI:10.48550/arxiv.2304.07327 |  |  | 3 | KVキャッシュ最適化／適応圧縮, inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2304.07327) |
| 120 | DOI:10.52202/079017-1601 |  |  | 3 | agent-runtime-sandbox-state-management, agentic GPU kernel generation / harness engineering / profile-guided optimization, agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://doi.org/10.52202/079017-1601) |
| 121 | OpenReview:c8McWs4Av0 |  |  | 3 | Adaptive Expert Computation / Compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=c8McWs4Av0) |
| 122 | OpenReview:LywifFNXV5 |  |  | 3 | CPU長文推論・近似注意, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://openreview.net/forum?id=LywifFNXV5) |
| 123 | OpenReview:tO3ASKZlok |  |  | 3 | 07-kv-cache-optimization-compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=tO3ASKZlok) |
| 124 | OpenReview:z3JZzu9EA3 |  |  | 3 | KV Cache Optimization / Compression, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=z3JZzu9EA3) |
| 125 | arXiv:1412.7024 |  |  | 3 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 126 | arXiv:1906.11024 |  |  | 3 | 99-other-inference-systems, inference-systems | [source](https://arxiv.org/abs/1906.11024) |
| 127 | arXiv:2209.13258 |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 128 | arXiv:2303.06135 |  |  | 3 | LLM Serving / Reasoning, fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2303.06135) |
| 129 | arXiv:2306.02707 |  |  | 3 | llm-serving-scheduling-disaggregation, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2306.02707) |
| 130 | arXiv:2310.02226 |  |  | 3 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 131 | arXiv:2311.00502 |  |  | 3 | CPU推論、行列拡張、異種実行、ルーフライン最適化, inference-systems | [source](https://arxiv.org/abs/2311.00502) |
| 132 | arXiv:2312.14852 |  |  | 3 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 133 | arXiv:2402.05406 |  |  | 3 | Adaptive Expert Computation / Compression, inference-systems | [source](https://arxiv.org/abs/2402.05406) |
| 134 | arXiv:2402.13116 |  |  | 3 | Speculative Decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.13116) |
| 135 | arXiv:2403.18814 |  |  | 3 | inference-systems, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2403.18814) |
| 136 | arXiv:2407.05483 |  |  | 3 | Long-context serving / KV cache benchmark, linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2407.05483) |
| 137 | arXiv:2408.04667 |  |  | 3 | Inference Kernel / Determinism, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2408.04667) |
| 138 | arXiv:2409.02813 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2409.02813) |
| 139 | arXiv:2410.12876 |  |  | 3 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.12876) |
| 140 | arXiv:2411.04996 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 141 | arXiv:2412.16545 |  |  | 3 | 10-kv-cache-offload-recomputation, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2412.16545) |
| 142 | arXiv:2503.16419 |  |  | 3 | Conditional Computation, LLM Serving / Reasoning | [source](https://arxiv.org/abs/2503.16419) |
| 143 | arXiv:2506.01844 |  |  | 3 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2506.01844) |
| 144 | arXiv:2507.19595 |  |  | 3 | KV Cache Optimization / Compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2507.19595) |
| 145 | arXiv:2510.08544 |  |  | 3 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.08544) |
| 146 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 147 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 148 | DOI:10.1109/mm.2022.3163226 |  |  | 3 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2022.3163226) |
| 149 | DOI:10.1145/3453483.3454083 |  |  | 3 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 150 | DOI:10.1145/3627535.3638466 |  |  | 3 | KV Cache Optimization / Compression, serving-scheduling | [source](https://doi.org/10.1145/3627535.3638466) |
| 151 | DOI:10.1145/3710848.3710869 |  |  | 3 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 152 | DOI:10.1162/tacl%5fa%5f00266 |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.1162/tacl%5fa%5f00266) |
| 153 | DOI:10.18653/v1/2023.acl-long.792 |  |  | 3 | inference-systems, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://doi.org/10.18653/v1/2023.acl-long.792) |
| 154 | DOI:10.48550/arxiv.2403.04797 |  |  | 3 | inference-systems, survey-long-context-serving | [source](https://doi.org/10.48550/arxiv.2403.04797) |
| 155 | OpenReview:2jwAjomEDB |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=2jwAjomEDB) |
| 156 | OpenReview:ayi7qezU87 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://openreview.net/forum?id=ayi7qezU87) |
| 157 | OpenReview:H-VlwsYvVi |  |  | 3 | Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=H-VlwsYvVi) |
| 158 | OpenReview:rJ4km2R5t7 |  |  | 3 | MoE inference / task-specific expert pruning / sparse-to-dense conversion, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rJ4km2R5t7) |
| 159 | OpenReview:ulCAPXYXfa |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, inference-systems | [source](https://openreview.net/forum?id=ulCAPXYXfa) |
| 160 | arXiv:1710.01878 |  |  | 3 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/1710.01878) |
| 161 | arXiv:1908.10084 |  |  | 3 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1908.10084) |
| 162 | arXiv:2105.13878 |  |  | 3 | Conditional Computation | [source](https://arxiv.org/abs/2105.13878) |
| 163 | arXiv:2210.03057 |  |  | 3 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 164 | arXiv:2305.06983 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2305.06983) |
| 165 | arXiv:2311.04902 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2311.04902) |
| 166 | arXiv:2402.13499 |  |  | 3 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2402.13499) |
| 167 | arXiv:2404.04793 |  |  | 3 | other-inference-systems | [source](https://arxiv.org/abs/2404.04793) |
| 168 | arXiv:2405.14105 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2405.14105) |
| 169 | arXiv:2411.03519 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2411.03519) |
| 170 | arXiv:2504.16891 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2504.16891) |
| 171 | DOI:10.1109/tpds.2022.3144614 |  |  | 3 | inference-systems | [source](https://doi.org/10.1109/tpds.2022.3144614) |
| 172 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 173 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 174 | arXiv:2109.04838 |  |  | 3 |  | [source](https://arxiv.org/abs/2109.04838) |
| 175 | arXiv:2307.10169 |  |  | 3 |  | [source](https://arxiv.org/abs/2307.10169) |
| 176 | arXiv:2511.11571 |  |  | 3 |  | [source](https://arxiv.org/abs/2511.11571) |
| 177 | arXiv:1305.0445 |  |  | 2 | Conditional Computation, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1305.0445) |
| 178 | arXiv:1603.04467 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1603.04467) |
| 179 | arXiv:1805.00907 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1805.00907) |
| 180 | arXiv:1906.02041 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1906.02041) |
| 181 | arXiv:1911.11313 |  |  | 2 | inference-systems, 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 182 | arXiv:2004.11886 |  |  | 2 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2004.11886) |
| 183 | arXiv:2009.08034 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2009.08034) |
| 184 | arXiv:2011.01060 |  |  | 2 | kv-cache-offload-recomputation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification | [source](https://arxiv.org/abs/2011.01060) |
| 185 | arXiv:2102.11972 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2102.11972) |
| 186 | arXiv:2105.03036 |  |  | 2 | MoE inference / expert pruning / language-specific expert specialization, inference-systems | [source](https://arxiv.org/abs/2105.03036) |
| 187 | arXiv:2109.09115 |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems | [source](https://arxiv.org/abs/2109.09115) |
| 188 | arXiv:2110.15191 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2110.15191) |
| 189 | arXiv:2204.05999 |  |  | 2 | inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2204.05999) |
| 190 | arXiv:2206.02845 |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection, inference-systems | [source](https://arxiv.org/abs/2206.02845) |
| 191 | arXiv:2212.01378 |  |  | 2 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2212.01378) |
| 192 | arXiv:2301.08984 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, inference-systems | [source](https://arxiv.org/abs/2301.08984) |
| 193 | arXiv:2303.11366 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 194 | arXiv:2305.03653 |  |  | 2 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, inference-systems | [source](https://arxiv.org/abs/2305.03653) |
| 195 | arXiv:2305.07759 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.07759) |
| 196 | arXiv:2306.04050 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 197 | arXiv:2307.09782 |  |  | 2 | LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.09782) |
| 198 | arXiv:2308.12908 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2308.12908) |
| 199 | arXiv:2309.10400 |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 200 | arXiv:2309.16739 |  |  | 2 | inference-systems, multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2309.16739) |
| 201 | arXiv:2310.17157 |  |  | 2 | Conditional Computation, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2310.17157) |
| 202 | arXiv:2311.08981 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, survey-speculative-decoding | [source](https://arxiv.org/abs/2311.08981) |
| 203 | arXiv:2311.13171 |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 204 | arXiv:2312.00678 |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 205 | arXiv:2312.07987 |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 206 | arXiv:2401.06080 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.06080) |
| 207 | arXiv:2402.02716 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2402.02716) |
| 208 | arXiv:2402.12289 |  |  | 2 | Expert Prefetch, survey-edge-llm | [source](https://arxiv.org/abs/2402.12289) |
| 209 | arXiv:2402.14808 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, inference/11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14808) |
| 210 | arXiv:2403.03952 |  |  | 2 | 14-agentic-inference-serving-runtime, inference-systems | [source](https://arxiv.org/abs/2403.03952) |
| 211 | arXiv:2403.09347 |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 212 | arXiv:2404.03413 |  |  | 2 | inference-systems, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2404.03413) |
| 213 | arXiv:2404.09336 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2404.09336) |
| 214 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 215 | arXiv:2405.14428 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2405.14428) |
| 216 | arXiv:2406.02430 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.02430) |
| 217 | arXiv:2406.05317 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2406.05317) |
| 218 | arXiv:2406.07476 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2406.07476) |
| 219 | arXiv:2406.18485 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18485) |
| 220 | arXiv:2407.00128 |  |  | 2 | Speculative Decoding / Parallel Inference Systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.00128) |
| 221 | arXiv:2407.09816 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.09816) |
| 222 | arXiv:2407.11511 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2407.11511) |
| 223 | arXiv:2409.12640 |  |  | 2 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2409.12640) |
| 224 | arXiv:2409.16546 |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, inference-systems | [source](https://arxiv.org/abs/2409.16546) |
| 225 | arXiv:2410.00037 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.00037) |
| 226 | arXiv:2410.02660 |  |  | 2 | kv-cache-optimization-compression, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2410.02660) |
| 227 | arXiv:2410.04343 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.04343) |
| 228 | arXiv:2410.10934 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10934) |
| 229 | arXiv:2410.13461 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2410.13461) |
| 230 | arXiv:2410.17196 |  |  | 2 | llm-serving-scheduling-disaggregation, その他の推論システム | [source](https://arxiv.org/abs/2410.17196) |
| 231 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 232 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 233 | arXiv:2411.15242 |  |  | 2 | PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management | [source](https://arxiv.org/abs/2411.15242) |
| 234 | arXiv:2412.01447 |  |  | 2 | inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2412.01447) |
| 235 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 236 | arXiv:2501.03035 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2501.03035) |
| 237 | arXiv:2501.09959 |  |  | 2 | 07-kv-キャッシュ-optimization-compression, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2501.09959) |
| 238 | arXiv:2501.15368 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2501.15368) |
| 239 | arXiv:2502.01776 |  |  | 2 | Sparse Attention / VLM Inference, attention kernel / heterogeneous batched inference / KV-cache layout | [source](https://arxiv.org/abs/2502.01776) |
| 240 | arXiv:2502.04507 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2502.04507) |
| 241 | arXiv:2502.07861 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.07861) |
| 242 | arXiv:2502.09696 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2502.09696) |
| 243 | arXiv:2502.12444 |  |  | 2 | 10-kv-cache-offload-recomputation, CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/2502.12444) |
| 244 | arXiv:2502.14752 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2502.14752) |
| 245 | arXiv:2502.17599 |  |  | 2 | KV cache eviction / multimodal KV cache compression / diversity-aware token selection, inference-systems | [source](https://arxiv.org/abs/2502.17599) |
| 246 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 247 | arXiv:2503.23100 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2503.23100) |
| 248 | arXiv:2504.02605 |  |  | 2 | LLMサービング・スケジューリング・KVキャッシュ保持, inference-systems | [source](https://arxiv.org/abs/2504.02605) |
| 249 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 250 | arXiv:2504.12463 |  |  | 2 | Expert Prefetch, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2504.12463) |
| 251 | arXiv:2504.17768 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.17768) |
| 252 | arXiv:2505.04921 |  |  | 2 | 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2505.04921) |
| 253 | arXiv:2505.07608 |  |  | 2 | kv-cache-optimization-compression, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2505.07608) |
| 254 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 255 | arXiv:2505.16552 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.16552) |
| 256 | arXiv:2505.24034 |  |  | 2 | LLM Serving / Distributed Communication, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2505.24034) |
| 257 | arXiv:2506.04108 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2506.04108) |
| 258 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 259 | arXiv:2506.20807 |  |  | 2 | inference-systems, other-inference-systems | [source](https://arxiv.org/abs/2506.20807) |
| 260 | arXiv:2507.07120 |  |  | 2 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2507.07120) |
| 261 | arXiv:2507.16731 |  |  | 2 | 05-speculative-decoding-moe, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2507.16731) |
| 262 | arXiv:2508.06447 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, System-aware KV cache | [source](https://arxiv.org/abs/2508.06447) |
| 263 | arXiv:2508.08438 |  |  | 2 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08438) |
| 264 | arXiv:2508.16653 |  |  | 2 | 低ビット疎推論／GPUカーネル／エッジ推論, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2508.16653) |
| 265 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 266 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 267 | arXiv:2510.03293 |  |  | 2 | Expert Prefetch, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.03293) |
| 268 | arXiv:2510.12633 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.12633) |
| 269 | arXiv:2510.24273 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化 | [source](https://arxiv.org/abs/2510.24273) |
| 270 | arXiv:2511.16108 |  |  | 2 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2511.16108) |
| 271 | arXiv:2511.21689 |  |  | 2 | 14-agentic-inference-serving-runtime, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2511.21689) |
| 272 | arXiv:2512.04123 |  |  | 2 | Agentic Serving Benchmarking, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.04123) |
| 273 | arXiv:2512.12087 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.12087) |
| 274 | arXiv:2512.17077 |  |  | 2 | llm-serving-scheduling-disaggregation, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2512.17077) |
| 275 | arXiv:2601.06521 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2601.06521) |
| 276 | arXiv:2601.09527 |  |  | 2 | LLMサービング・スケジューリング・分離実行, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://arxiv.org/abs/2601.09527) |
| 277 | arXiv:2601.19092 |  |  | 2 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム, dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2601.19092) |
| 278 | arXiv:2602.02599 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2602.02599) |
| 279 | arXiv:2603.07685 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems | [source](https://arxiv.org/abs/2603.07685) |
| 280 | arXiv:2604.15409 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2604.15409) |
| 281 | arXiv:2606.03928 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2606.03928) |
| 282 | arXiv:2607.04031 |  |  | 2 | 10-kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2607.04031) |
| 283 | DOI:10.1016/j.parco.2015.09.001 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, hardware-accelerators | [source](https://doi.org/10.1016/j.parco.2015.09.001) |
| 284 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 285 | DOI:10.1109/dac63849.2025.11132883 |  |  | 2 | 17-pim-near-data-acceleration, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/dac63849.2025.11132883) |
| 286 | DOI:10.1109/hcs59251.2023.10254717 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/hcs59251.2023.10254717) |
| 287 | DOI:10.1109/hotchips.2019.8875680 |  |  | 2 | inference-systems, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hotchips.2019.8875680) |
| 288 | DOI:10.1109/hpca47549.2020.00035 |  |  | 2 | inference-systems, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1109/hpca47549.2020.00035) |
| 289 | DOI:10.1109/hpcc-css-icess.2015.82 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1109/hpcc-css-icess.2015.82) |
| 290 | DOI:10.1109/ijcnn.1993.716791 |  |  | 2 | MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, inference-systems | [source](https://doi.org/10.1109/ijcnn.1993.716791) |
| 291 | DOI:10.1109/ipdps47924.2020.00070 |  |  | 2 | Inference Kernel / Determinism, hardware-accelerators | [source](https://doi.org/10.1109/ipdps47924.2020.00070) |
| 292 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 293 | DOI:10.1109/isscc42614.2022.9731565 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, inference-systems | [source](https://doi.org/10.1109/isscc42614.2022.9731565) |
| 294 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 295 | DOI:10.1109/lca.2025.3566692 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/lca.2025.3566692) |
| 296 | DOI:10.1109/micro50266.2020.00071 |  |  | 2 | inference-systems, kv-cache-memory | [source](https://doi.org/10.1109/micro50266.2020.00071) |
| 297 | DOI:10.1109/mm.2023.3256796 |  |  | 2 | Expert Prefetch, inference-systems | [source](https://doi.org/10.1109/mm.2023.3256796) |
| 298 | DOI:10.1109/tbdata.2019.2921572 |  |  | 2 | RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/tbdata.2019.2921572) |
| 299 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 300 | DOI:10.1109/tpwrs.2022.3173250 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1109/tpwrs.2022.3173250) |
| 301 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 302 | DOI:10.1145/1810085.1810091 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/1810085.1810091) |
| 303 | DOI:10.1145/2485922.2485964 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/2485922.2485964) |
| 304 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 305 | DOI:10.1145/3133901 |  |  | 2 | kernel-runtime-compilation, unstructured sparsity / GPU inference kernels | [source](https://doi.org/10.1145/3133901) |
| 306 | DOI:10.1145/3297858.3304043 |  |  | 2 | hardware-accelerators, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3297858.3304043) |
| 307 | DOI:10.1145/3437801.3441593 |  |  | 2 | inference-systems, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3437801.3441593) |
| 308 | DOI:10.1145/3470496.3527440 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/3470496.3527440) |
| 309 | DOI:10.1145/3552326.3567508 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory | [source](https://doi.org/10.1145/3552326.3567508) |
| 310 | DOI:10.1145/3581784.3607034 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3581784.3607034) |
| 311 | DOI:10.1145/3605573.3605613 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3605573.3605613) |
| 312 | DOI:10.1145/3620666.3651369 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651369) |
| 313 | DOI:10.1145/3650200.3656636 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, 分散推論／集団通信圧縮／量子化AllReduce／XLA・TPU | [source](https://doi.org/10.1145/3650200.3656636) |
| 314 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 315 | DOI:10.1145/3706418 |  |  | 2 | 08-edge-on-device-llm-systems, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3706418) |
| 316 | DOI:10.1145/3725843.3756115 |  |  | 2 | PIM / Near-Data Acceleration, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756115) |
| 317 | DOI:10.1145/3767742 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3767742) |
| 318 | DOI:10.1145/3779212.3790236 |  |  | 2 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790236) |
| 319 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 320 | DOI:10.1609/aaai.v40i36.40255 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.1609/aaai.v40i36.40255) |
| 321 | DOI:10.18653/v1/2022.emnlp-main.823 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/2022.emnlp-main.823) |
| 322 | DOI:10.18653/v1/2024.findings-acl.179 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, 投機的デコード／MoE | [source](https://doi.org/10.18653/v1/2024.findings-acl.179) |
| 323 | DOI:10.18653/v1/2024.naacl-long.109 |  |  | 2 | inference-systems, multi-model LLM serving / prompt routing / resource allocation | [source](https://doi.org/10.18653/v1/2024.naacl-long.109) |
| 324 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 325 | DOI:10.18653/v1/w19-4828 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/w19-4828) |
| 326 | DOI:10.48550/arxiv.2304.11062 |  |  | 2 | inference-systems, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.48550/arxiv.2304.11062) |
| 327 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 328 | DOI:10.52202/079017-0040 |  |  | 2 | KV Cache Optimization / Compression, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://doi.org/10.52202/079017-0040) |
| 329 | DOI:10.52202/079017-3801 |  |  | 2 | KV Cache Optimization / Compression, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks | [source](https://doi.org/10.52202/079017-3801) |
| 330 | OpenReview:0fJfVOSUra |  |  | 2 | 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://openreview.net/forum?id=0fJfVOSUra) |
| 331 | OpenReview:acJ3vdFljk |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=acJ3vdFljk) |
| 332 | OpenReview:c5BOcHM6J8 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=c5BOcHM6J8) |
| 333 | OpenReview:dwPdYFqVWO |  |  | 2 | Speculative decoding × MoE, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://openreview.net/forum?id=dwPdYFqVWO) |
| 334 | OpenReview:FAeU7516MR |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE | [source](https://openreview.net/forum?id=FAeU7516MR) |
| 335 | OpenReview:HklBjCEKvH |  |  | 2 | Speculative Decoding, other-inference-systems | [source](https://openreview.net/forum?id=HklBjCEKvH) |
| 336 | OpenReview:JZfg6wGi6g |  |  | 2 | KV Cache Optimization / Compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=JZfg6wGi6g) |
| 337 | OpenReview:NGPmH3vbAA_ |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=NGPmH3vbAA_) |
| 338 | OpenReview:R7fv5NWfMm |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=R7fv5NWfMm) |
| 339 | OpenReview:RyOpooIxDF |  |  | 2 | inference-systems, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://openreview.net/forum?id=RyOpooIxDF) |
| 340 | OpenReview:xdNAVP7TGy |  |  | 2 | kv-cache-offload-recomputation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://openreview.net/forum?id=xdNAVP7TGy) |
| 341 | OpenReview:ySQH0oDyp7 |  |  | 2 | 18-vla-inference-quantization-evaluation, inference-systems | [source](https://openreview.net/forum?id=ySQH0oDyp7) |
| 342 | arXiv:1512.03385 |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1512.03385) |
| 343 | arXiv:1704.05426 |  |  | 2 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 344 | arXiv:1808.06866 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1808.06866) |
| 345 | arXiv:1902.09506 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1902.09506) |
| 346 | arXiv:1905.07799 |  |  | 2 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 347 | arXiv:1906.04341 |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 348 | arXiv:1909.12486 |  |  | 2 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1909.12486) |
| 349 | arXiv:2005.08100 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2005.08100) |
| 350 | arXiv:2010.02502 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2010.02502) |
| 351 | arXiv:2012.12624 |  |  | 2 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 352 | arXiv:2105.09938 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2105.09938) |
| 353 | arXiv:2111.00160 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 354 | arXiv:2112.07916 |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2112.07916) |
| 355 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 356 | arXiv:2206.14858 |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2206.14858) |
| 357 | arXiv:2210.05144 |  |  | 2 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2210.05144) |
| 358 | arXiv:2211.00593 |  |  | 2 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 359 | arXiv:2211.16750 |  |  | 2 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2211.16750) |
| 360 | arXiv:2302.09210 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2302.09210) |
| 361 | arXiv:2303.06349 |  |  | 2 | training-memory-systems | [source](https://arxiv.org/abs/2303.06349) |
| 362 | arXiv:2304.02017 |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 363 | arXiv:2304.10592 |  |  | 2 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.10592) |
| 364 | arXiv:2305.07622 |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 365 | arXiv:2305.13304 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.13304) |
| 366 | arXiv:2305.17455 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.17455) |
| 367 | arXiv:2306.02295 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02295) |
| 368 | arXiv:2306.09539 |  |  | 2 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2306.09539) |
| 369 | arXiv:2307.10802 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2307.10802) |
| 370 | arXiv:2311.14652 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2311.14652) |
| 371 | arXiv:2401.07886 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2401.07886) |
| 372 | arXiv:2402.17177 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.17177) |
| 373 | arXiv:2403.10616 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.10616) |
| 374 | arXiv:2404.01744 |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2404.01744) |
| 375 | arXiv:2404.16054 |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2404.16054) |
| 376 | arXiv:2405.04233 |  |  | 2 | Diffusion LLM Inference | [source](https://arxiv.org/abs/2405.04233) |
| 377 | arXiv:2405.18218 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2405.18218) |
| 378 | arXiv:2406.12930 |  |  | 2 | survey-low-bit-llm | [source](https://arxiv.org/abs/2406.12930) |
| 379 | arXiv:2407.04620 |  |  | 2 | prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2407.04620) |
| 380 | arXiv:2407.19126 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2407.19126) |
| 381 | arXiv:2408.15237 |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2408.15237) |
| 382 | arXiv:2409.15647 |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2409.15647) |
| 383 | arXiv:2410.08292 |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2410.08292) |
| 384 | arXiv:2410.18982 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2410.18982) |
| 385 | arXiv:2411.04368 |  |  | 2 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2411.04368) |
| 386 | arXiv:2412.00402 |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2412.00402) |
| 387 | arXiv:2412.16339 |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2412.16339) |
| 388 | arXiv:2501.01818 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2501.01818) |
| 389 | arXiv:2501.12570 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2501.12570) |
| 390 | arXiv:2502.02743 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2502.02743) |
| 391 | arXiv:2502.07780 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next | [source](https://arxiv.org/abs/2502.07780) |
| 392 | arXiv:2502.12067 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.12067) |
| 393 | arXiv:2502.20122 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.20122) |
| 394 | arXiv:2503.13657 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2503.13657) |
| 395 | arXiv:2505.03756 |  |  | 2 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2505.03756) |
| 396 | arXiv:2505.18227 |  |  | 2 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2505.18227) |
| 397 | arXiv:2505.22375 |  |  | 2 | chunked-prefill scheduling / fairness / latency control | [source](https://arxiv.org/abs/2505.22375) |
| 398 | arXiv:2505.24857 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2505.24857) |
| 399 | arXiv:2506.13759 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2506.13759) |
| 400 | arXiv:2508.03332 |  |  | 2 | hardware-accelerators | [source](https://arxiv.org/abs/2508.03332) |
| 401 | arXiv:2509.18085 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding | [source](https://arxiv.org/abs/2509.18085) |
| 402 | arXiv:2510.04374 |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.04374) |
| 403 | arXiv:2511.14617 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2511.14617) |
| 404 | arXiv:2512.18674 |  |  | 2 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.18674) |
| 405 | arXiv:2603.01426 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2603.01426) |
| 406 | arXiv:2604.05546 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2604.05546) |
| 407 | arXiv:2605.09649 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2605.09649) |
| 408 | arXiv:2605.18053 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2605.18053) |
| 409 | DOI:10.1109/cstic55103.2022.9856846 |  |  | 2 | 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1109/cstic55103.2022.9856846) |
| 410 | DOI:10.1109/hpca61900.2025.00086 |  |  | 2 | low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1109/hpca61900.2025.00086) |
| 411 | DOI:10.1109/infocom53939.2023.10228874 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1109/infocom53939.2023.10228874) |
| 412 | DOI:10.1109/isca59077.2024.00080 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isca59077.2024.00080) |
| 413 | DOI:10.1109/ispass48437.2020.00016 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/ispass48437.2020.00016) |
| 414 | DOI:10.1109/mm.2021.3058217 |  |  | 2 | 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1109/mm.2021.3058217) |
| 415 | DOI:10.1137/s0097539795288490 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://doi.org/10.1137/s0097539795288490) |
| 416 | DOI:10.1145/2872362.2872368 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2872362.2872368) |
| 417 | DOI:10.1145/3132747.3132780 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/3132747.3132780) |
| 418 | DOI:10.1145/3373376.3378512 |  |  | 2 | agent-runtime-sandbox-state-management | [source](https://doi.org/10.1145/3373376.3378512) |
| 419 | DOI:10.1145/3477132.3483580 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/3477132.3483580) |
| 420 | DOI:10.1145/3581784.3607073 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1145/3581784.3607073) |
| 421 | DOI:10.1145/3695053.3731025 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/3695053.3731025) |
| 422 | DOI:10.1145/3786655 |  |  | 2 | kv-cache-reuse-position-independent-caching | [source](https://doi.org/10.1145/3786655) |
| 423 | DOI:10.14778/3626292.3626303 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.14778/3626292.3626303) |
| 424 | DOI:10.18653/v1/2020.emnlp-main.83 |  |  | 2 | speculative-decoding | [source](https://doi.org/10.18653/v1/2020.emnlp-main.83) |
| 425 | DOI:10.18653/v1/2021.naacl-main.463 |  |  | 2 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://doi.org/10.18653/v1/2021.naacl-main.463) |
| 426 | DOI:10.18653/v1/2023.acl-long.754 |  |  | 2 | Speculative Decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.754) |
| 427 | DOI:10.18653/v1/2023.emnlp-main.391 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.391) |
| 428 | DOI:10.18653/v1/2024.emnlp-main.808 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.808) |
| 429 | DOI:10.18653/v1/2024.naacl-long.222 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.naacl-long.222) |
| 430 | DOI:10.18653/v1/2025.naacl-long.328 |  |  | 2 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://doi.org/10.18653/v1/2025.naacl-long.328) |
| 431 | DOI:10.18653/v1/p18-2124 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/p18-2124) |
| 432 | DOI:10.48550/arxiv.2310.12963 |  |  | 2 | multi-model LLM serving / prompt routing / resource allocation | [source](https://doi.org/10.48550/arxiv.2310.12963) |
| 433 | OpenReview:44PwmgOpAt |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=44PwmgOpAt) |
| 434 | OpenReview:9k27IITeAZ |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=9k27IITeAZ) |
| 435 | OpenReview:CQsmMYmlP5T |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=CQsmMYmlP5T) |
| 436 | OpenReview:dfqsW38v1X |  |  | 2 | MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=dfqsW38v1X) |
| 437 | OpenReview:HTpMOl6xSI |  |  | 2 | task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=HTpMOl6xSI) |
| 438 | OpenReview:loMa99A4p8 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding | [source](https://openreview.net/forum?id=loMa99A4p8) |
| 439 | OpenReview:P0GOk5wslg |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=P0GOk5wslg) |
| 440 | OpenReview:tcisuhGsQZ |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=tcisuhGsQZ) |
| 441 | OpenReview:uREj4ZuGJE |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=uREj4ZuGJE) |
| 442 | OpenReview:xcqSOfHt4g |  |  | 2 | diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising | [source](https://openreview.net/forum?id=xcqSOfHt4g) |
| 443 | arXiv:1608.08710 |  |  | 2 |  | [source](https://arxiv.org/abs/1608.08710) |
| 444 | arXiv:2006.16362 |  |  | 2 |  | [source](https://arxiv.org/abs/2006.16362) |
| 445 | arXiv:2102.03315 |  |  | 2 |  | [source](https://arxiv.org/abs/2102.03315) |
| 446 | arXiv:2201.03533 |  |  | 2 |  | [source](https://arxiv.org/abs/2201.03533) |
| 447 | arXiv:2212.10554 |  |  | 2 |  | [source](https://arxiv.org/abs/2212.10554) |
| 448 | arXiv:2307.03109 |  |  | 2 |  | [source](https://arxiv.org/abs/2307.03109) |
| 449 | arXiv:2311.12793 |  |  | 2 |  | [source](https://arxiv.org/abs/2311.12793) |
| 450 | arXiv:2402.14830 |  |  | 2 |  | [source](https://arxiv.org/abs/2402.14830) |
| 451 | arXiv:2404.08801 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.08801) |
| 452 | arXiv:2404.16821 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.16821) |
| 453 | arXiv:2407.12077 |  |  | 2 |  | [source](https://arxiv.org/abs/2407.12077) |
| 454 | arXiv:2410.15704 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.15704) |
| 455 | arXiv:2411.14033 |  |  | 2 |  | [source](https://arxiv.org/abs/2411.14033) |
| 456 | arXiv:2502.01960 |  |  | 2 |  | [source](https://arxiv.org/abs/2502.01960) |
| 457 | arXiv:2504.12285 |  |  | 2 |  | [source](https://arxiv.org/abs/2504.12285) |
| 458 | arXiv:2510.06189 |  |  | 2 |  | [source](https://arxiv.org/abs/2510.06189) |
| 459 | DOI:10.1145/3636534.3649361 |  |  | 2 |  | [source](https://doi.org/10.1145/3636534.3649361) |
| 460 | DOI:10.18653/v1/2022.bigscience-1.9 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2022.bigscience-1.9) |
| 461 | DOI:10.18653/v1/n19-1309 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/n19-1309) |
| 462 | DOI:10.48550/arxiv.2402.04347 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2402.04347) |
| 463 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 464 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 465 | OpenReview:FJFVmeXusW |  |  | 2 |  | [source](https://openreview.net/forum?id=FJFVmeXusW) |
| 466 | OpenReview:JXhROKNZzOc |  |  | 2 |  | [source](https://openreview.net/forum?id=JXhROKNZzOc) |
| 467 | OpenReview:QV79qiKAjD |  |  | 2 |  | [source](https://openreview.net/forum?id=QV79qiKAjD) |
| 468 | arXiv:1109.3843 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1109.3843) |
| 469 | arXiv:1205.2618 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 470 | arXiv:1211.0361 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1211.0361) |
| 471 | arXiv:1212.0402 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 472 | arXiv:1312.6211 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 473 | arXiv:1407.3561 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1407.3561) |
| 474 | arXiv:1412.6115 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1412.6115) |
| 475 | arXiv:1506.02438 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 476 | arXiv:1507.05910 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1507.05910) |
| 477 | arXiv:1511.01837 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 478 | arXiv:1511.06939 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 479 | arXiv:1512.02595 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1512.02595) |
| 480 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 481 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 482 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 483 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 484 | arXiv:1607.08022 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1607.08022) |
| 485 | arXiv:1609.09548 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1609.09548) |
| 486 | arXiv:1611.01540 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/1611.01540) |
| 487 | arXiv:1611.01704 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1611.01704) |
| 488 | arXiv:1701.03499 |  |  | 1 | NPU-PIM統合メモリ、近データ処理、LLM推論メモリ階層。NeuPIMs、IANUS、FACILの静的配置を動的実行へ拡張する。 | [source](https://arxiv.org/abs/1701.03499) |
| 489 | arXiv:1702.04008 |  |  | 1 | unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1702.04008) |
| 490 | arXiv:1703.05160 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 491 | arXiv:1704.04497 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1704.04497) |
| 492 | arXiv:1705.03122 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1705.03122) |
| 493 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 494 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 495 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 496 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 497 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 498 | arXiv:1710.10903 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1710.10903) |
| 499 | arXiv:1711.03936 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 500 | arXiv:1712.01208 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/1712.01208) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

