# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-03T13:22:57+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **589** / 未claim総数: **442** / このworker向け: **147**

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
| 143 | research | arXiv:2310.05015 | Compresso: Structured Pruning with Collaborative Prompting Learns Compact Large Language Models | [primary](https://arxiv.org/abs/2310.05015) | `papers/inference/99-other-inference-systems/2023-2310.05015-compresso-structured-pruning-with-collaborative-prompting-learns-compact-large-language-models.md` |
| 144 | research | arXiv:2405.05465 | Vidur: A Large-Scale Simulation Framework For LLM Inference | [primary](https://arxiv.org/abs/2405.05465) | `papers/inference/99-other-inference-systems/2024-2405.05465-vidur-a-large-scale-simulation-framework-for-llm-inference.md` |
| 145 | research | arXiv:2401.03462 | Long Context Compression with Activation Beacon | [primary](https://arxiv.org/abs/2401.03462) | `papers/inference/99-other-inference-systems/2024-2401.03462-long-context-compression-with-activation-beacon.md` |
| 146 | research | arXiv:2402.01771 | BlackMamba: Mixture of Experts for State-Space Models | [primary](https://arxiv.org/abs/2402.01771) | `papers/inference/99-other-inference-systems/2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md` |
| 147 | research | arXiv:2404.08856 | On Speculative Decoding for Multimodal Large Language Models | [primary](https://arxiv.org/abs/2404.08856) | `papers/inference/99-other-inference-systems/2024-2404.08856-on-speculative-decoding-for-multimodal-large-language-models.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **6901** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3458817.3476209 |  |  | 19 | Conditional Computation, GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, distributed LLM inference / communication-aware serving, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-offload-routing, other-inference-systems, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime, オフロード／階層メモリ | [source](https://doi.org/10.1145/3458817.3476209) |
| 2 | DOI:10.1145/3694715.3695948 |  |  | 17 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 3 | OpenReview:VTF8yNQM66 |  |  | 15 | 13-sparse-attention, Agentic Serving Benchmarking, Long-context serving / KV cache benchmark, MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, agentic workflow serving / workflow physical planning / adaptive serving, inference-systems, llm-serving-scheduling-disaggregation, other-inference-systems, query-aware sparse attention / KV selection / tail compensation / CPU offload, その他の推論システム | [source](https://openreview.net/forum?id=VTF8yNQM66) |
| 4 | arXiv:1607.06450 |  |  | 14 | Conditional Computation, GPU Kernel Framework, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, inference-systems, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 5 | arXiv:2201.11903 |  |  | 14 | 13-sparse-attention, Adaptive Expert Computation / Compression, Conditional Computation, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, Offload / Hierarchical Memory, Speculative Decoding / Parallel Inference Systems, speculative decoding / edge-assisted serving / distributed inference / pipeline scheduling | [source](https://arxiv.org/abs/2201.11903) |
| 6 | arXiv:2405.21060 |  |  | 13 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化, PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management, inference-systems, kv-cache, kv-cache-offload-recomputation, linear attention / delta-rule associative memory / state-space models / Bayesian filtering, prefix caching / hybrid attention-SSM serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2405.21060) |
| 7 | arXiv:2409.12186 |  |  | 13 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation, inference-systems, multi-LLM communication / KV-cache semantic transfer, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM, 推論エンジン／推論基盤, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://arxiv.org/abs/2409.12186) |
| 8 | arXiv:1809.09600 |  |  | 13 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, inference-systems, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 9 | arXiv:2104.08691 |  |  | 12 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, many-adapter LLM serving / LoRA serving / inference scheduling, survey-long-context-serving, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2104.08691) |
| 10 | arXiv:2305.16300 |  |  | 12 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/2305.16300) |
| 11 | arXiv:2501.08313 |  |  | 12 | 13-sparse-attention, inference-systems, moe-parallelism-communication, prefix caching / hybrid attention-SSM serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.08313) |
| 12 | arXiv:2309.04255 |  |  | 11 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, Speculative Decoding, edge-on-device-llm-systems, inference-systems, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 13 | DOI:10.48550/arxiv.2501.14743 |  |  | 11 | 11-llm-serving-scheduling-disaggregation, 12-moe-parallelism-communication, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, LLM Serving / Scheduling / Disaggregation, LLM serving / prefill-decode disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2501.14743) |
| 14 | DOI:10.18653/v1/2020.coling-main.580 |  |  | 11 | 10-kv-キャッシュ-オフロード-recomputation, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, Prefill/Decode Disaggregation / Selective KV Transfer, inference-systems | [source](https://doi.org/10.18653/v1/2020.coling-main.580) |
| 15 | arXiv:2407.12391 |  |  | 10 | SLO-aware LLM serving scheduling, System-aware KV cache, disaggregated LLM serving / request routing / learned scheduling, inference-systems, llm-serving-scheduling-disaggregation, survey-moe-inference-optimization, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.12391) |
| 16 | DOI:10.48550/arxiv.2412.00099 |  |  | 10 | 08-edge-on-device-llm-systems, edge-on-device-llm-systems, hardware-accelerators, offload-hierarchical-memory, survey-moe-inference-optimization, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.48550/arxiv.2412.00099) |
| 17 | DOI:10.18653/v1/2025.emnlp-main.334 |  |  | 10 | 10-kv-cache-offload-recomputation, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, inference-systems, kv-cache-reuse-position-independent-caching, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://doi.org/10.18653/v1/2025.emnlp-main.334) |
| 18 | DOI:10.18653/v1/2024.emnlp-main.422 |  |  | 9 | 05-speculative-decoding-moe, LLM Serving / Scheduling / Disaggregation, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE, other-inference-systems, speculative-decoding, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://doi.org/10.18653/v1/2024.emnlp-main.422) |
| 19 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 20 | OpenReview:qrwe7XHTmYb |  |  | 9 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, LLM Serving / Multi-Model Serving / Memory Disaggregation, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, Speculative decoding × MoE, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=qrwe7XHTmYb) |
| 21 | arXiv:2308.12966 |  |  | 9 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, inference-systems, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 22 | arXiv:2501.14249 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, LLM Serving / Scheduling / Disaggregation, Other Inference Systems / Lossless Parallel Decoding, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2501.14249) |
| 23 | arXiv:2108.12409 |  |  | 9 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLM inference surveys、roofline performance analysis, cpu-offload, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2108.12409) |
| 24 | arXiv:2409.06669 |  |  | 8 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, Quantization × MoE × Offload, Speculative decoding × MoE, adaptive expert computation / dynamic MoE routing / expert sparsification, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2409.06669) |
| 25 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 26 | arXiv:2512.20856 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, PIM / Near-Data Acceleration, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2512.20856) |
| 27 | arXiv:2408.11743 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 28 | DOI:10.18653/v1/n18-2097 |  |  | 8 | 08-edge-on-device-llm-systems, inference-systems, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 29 | arXiv:2110.03742 |  |  | 7 | Edge／on-device MoE, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference / expert pruning / language-specific expert specialization, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2110.03742) |
| 30 | arXiv:2212.10560 |  |  | 7 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2212.10560) |
| 31 | DOI:10.1145/3768628 |  |  | 7 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 32 | arXiv:2412.10302 |  |  | 7 | Adaptive computation／cache-aware MoE, MoE compression / training-free expert merging / multimodal MoE routing, Quantization × MoE × Offload, adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2412.10302) |
| 33 | OpenReview:Bkg6RiCqY7 |  |  | 7 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 34 | arXiv:2310.15141 |  |  | 7 | LLM inference surveys、roofline performance analysis, inference-systems, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 35 | arXiv:2509.16941 |  |  | 7 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2509.16941) |
| 36 | OpenReview:EytBpUGB1Z |  |  | 7 | KV Cache Optimization / Compression, Sparse Attention / VLM Inference | [source](https://openreview.net/forum?id=EytBpUGB1Z) |
| 37 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 38 | OpenReview:v8L0pN6EOi |  |  | 6 | KV Cache Optimization / Compression, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, reasoning-model compression / post-training pruning / calibration-data selection / causal intervention, speculative-decoding, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://openreview.net/forum?id=v8L0pN6EOi) |
| 39 | DOI:10.1145/3503222.3507778 |  |  | 6 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.1145/3503222.3507778) |
| 40 | arXiv:2203.08913 |  |  | 6 | LLM inference surveys、roofline performance analysis, inference-systems, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 41 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 42 | DOI:10.1145/3620666.3651379 |  |  | 6 | inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 43 | arXiv:2401.03868 |  |  | 6 | LLM inference surveys、roofline performance analysis, hierarchical-memory, kv-cache-memory | [source](https://arxiv.org/abs/2401.03868) |
| 44 | arXiv:2508.18298 |  |  | 6 | inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18298) |
| 45 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 6 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 46 | OpenReview:rkgNKkHtvB |  |  | 6 | 10-kv-cache-offload-recomputation, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems | [source](https://openreview.net/forum?id=rkgNKkHtvB) |
| 47 | arXiv:2412.06769 |  |  | 6 | 99-other-inference-systems, Conditional Computation | [source](https://arxiv.org/abs/2412.06769) |
| 48 | OpenReview:mZn2Xyh9Ec |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=mZn2Xyh9Ec) |
| 49 | arXiv:2204.09179 |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 50 | DOI:10.18653/v1/2024.findings-acl.57 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Long-context serving / KV cache benchmark, inference-systems, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.57) |
| 51 | arXiv:2402.02244 |  |  | 5 | KV Cache Compression / Long Context, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 52 | DOI:10.1145/3732941 |  |  | 5 | LLM Serving / Scheduling / Disaggregation, dynamic-pd-disaggregation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3732941) |
| 53 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 54 | arXiv:2402.01680 |  |  | 5 | llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 55 | arXiv:2406.07887 |  |  | 5 | Long-context serving / KV cache benchmark, PIM / Near-Data Acceleration, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2406.07887) |
| 56 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 5 | Speculative Decoding, inference-systems, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 57 | arXiv:2207.07061 |  |  | 5 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2207.07061) |
| 58 | arXiv:2603.05451 |  |  | 5 | diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2603.05451) |
| 59 | DOI:10.48550/arxiv.2412.18910 |  |  | 5 | 05-speculative-decoding-moe, inference-systems | [source](https://doi.org/10.48550/arxiv.2412.18910) |
| 60 | OpenReview:2GmDdhBdDk |  |  | 5 | inference-systems | [source](https://openreview.net/forum?id=2GmDdhBdDk) |
| 61 | arXiv:2309.01885 |  |  | 4 | 16-weight-quantization-compression, LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.01885) |
| 62 | arXiv:2503.08311 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, inference-systems | [source](https://arxiv.org/abs/2503.08311) |
| 63 | arXiv:2511.00739 |  |  | 4 | LLM Serving / Scheduling / Disaggregation, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, agentic serving workload characterization / KV-cache / inference benchmarking, inference-systems | [source](https://arxiv.org/abs/2511.00739) |
| 64 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 4 | Inference Kernel / Determinism, inference-systems, moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 65 | DOI:10.1145/3630106.3658542 |  |  | 4 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3630106.3658542) |
| 66 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 67 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 68 | OpenReview:z5uVAKwmjf |  |  | 4 | 14-agentic-inference-serving-runtime, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, LLMサービング／自動スケーリング／広域ルーティング, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=z5uVAKwmjf) |
| 69 | arXiv:2312.04916 |  |  | 4 | early-exit-offloading-self-speculative-decoding, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 70 | arXiv:2404.07972 |  |  | 4 | 14-agentic-inference-serving-runtime, KVキャッシュオフロード・再計算, inference-systems | [source](https://arxiv.org/abs/2404.07972) |
| 71 | arXiv:2408.06292 |  |  | 4 | LLMサービング／自動スケーリング／広域ルーティング, inference-systems, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2408.06292) |
| 72 | arXiv:2411.15100 |  |  | 4 | inference-systems, kv-cache-optimization-compression, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.15100) |
| 73 | arXiv:2503.18773 |  |  | 4 | KV Cache Offload / Recomputation, batch inference / event-driven runtime / MoE serving / offload, inference-systems | [source](https://arxiv.org/abs/2503.18773) |
| 74 | arXiv:2508.02193 |  |  | 4 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, inference-systems, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2508.02193) |
| 75 | DOI:10.1145/3466752.3480125 |  |  | 4 | inference-systems, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3466752.3480125) |
| 76 | DOI:10.1145/3600006.3613139 |  |  | 4 | CPUオフロード / 活性化疎性 / 階層メモリ, Long-context serving / KV cache benchmark, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling | [source](https://doi.org/10.1145/3600006.3613139) |
| 77 | DOI:10.18653/v1/2024.acl-long.91 |  |  | 4 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression, inference-systems | [source](https://doi.org/10.18653/v1/2024.acl-long.91) |
| 78 | OpenReview:BAakY1hNKS |  |  | 4 | 14-agentic-inference-serving-runtime, llm-serving-scheduling-disaggregation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=BAakY1hNKS) |
| 79 | OpenReview:TrjbxzRcnf- |  |  | 4 | KVキャッシュ・注意アーキテクチャ, KVキャッシュ再利用／圧縮／ネットワーク転送, other-inference-systems | [source](https://openreview.net/forum?id=TrjbxzRcnf-) |
| 80 | arXiv:1904.01038 |  |  | 4 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/1904.01038) |
| 81 | arXiv:2210.09461 |  |  | 4 | inference-systems, on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2210.09461) |
| 82 | arXiv:2407.10969 |  |  | 4 | Adaptive Expert Computation / Compression, Conditional Computation | [source](https://arxiv.org/abs/2407.10969) |
| 83 | arXiv:2507.01449 |  |  | 4 | inference-systems, 投機的デコード／MoE | [source](https://arxiv.org/abs/2507.01449) |
| 84 | DOI:10.1145/3577193.3593704 |  |  | 4 | KV Cache Optimization / Compression, その他システム研究 | [source](https://doi.org/10.1145/3577193.3593704) |
| 85 | DOI:10.1162/tacl_a_00638 |  |  | 4 | KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, Long-context serving / KV cache benchmark | [source](https://doi.org/10.1162/tacl_a_00638) |
| 86 | OpenReview:OS5dqxmmtl |  |  | 4 | Long-context serving / KV cache benchmark, inference-systems | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 87 | arXiv:2212.08153 |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2212.08153) |
| 88 | arXiv:2405.12528 |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2405.12528) |
| 89 | DOI:10.1145/3714983.3714987 |  |  | 4 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成 | [source](https://doi.org/10.1145/3714983.3714987) |
| 90 | OpenReview:bTHFrqhASY |  |  | 4 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=bTHFrqhASY) |
| 91 | arXiv:1905.05702 |  |  | 3 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Sparse Attention, inference-systems | [source](https://arxiv.org/abs/1905.05702) |
| 92 | arXiv:2306.00317 |  |  | 3 | Quantization × MoE × Offload, hardware-accelerators, inference-systems | [source](https://arxiv.org/abs/2306.00317) |
| 93 | arXiv:2308.09723 |  |  | 3 | KV Cache Optimization / Compression, Quantization × MoE × Offload, kv-cache-memory | [source](https://arxiv.org/abs/2308.09723) |
| 94 | arXiv:2309.14393 |  |  | 3 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, inference-systems, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 95 | arXiv:2312.13558 |  |  | 3 | LLM inference surveys、roofline performance analysis, inference-systems, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 96 | arXiv:2402.06126 |  |  | 3 | Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.06126) |
| 97 | arXiv:2404.14897 |  |  | 3 | inference-systems, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2404.14897) |
| 98 | arXiv:2406.03853 |  |  | 3 | adaptive-expert-computation-compression, inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2406.03853) |
| 99 | arXiv:2407.09141 |  |  | 3 | 06-moe-quantization-compression, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.09141) |
| 100 | arXiv:2409.06857 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, edge-on-device-llm-systems, offload-hierarchical-memory | [source](https://arxiv.org/abs/2409.06857) |
| 101 | arXiv:2410.06511 |  |  | 3 | inference-systems, その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/2410.06511) |
| 102 | arXiv:2411.01738 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2411.01738) |
| 103 | arXiv:2501.14794 |  |  | 3 | 08-edge-on-device-llm-systems, inference-systems, マルチモーダルLLM向けの近メモリ処理と異種メモリ配置を、チップレット接続と実行時マッピングで統合する研究。 | [source](https://arxiv.org/abs/2501.14794) |
| 104 | arXiv:2502.16880 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2502.16880) |
| 105 | arXiv:2504.09014 |  |  | 3 | LLM Serving / Distributed Communication, LLMサービング／スケジューリング／分離実行, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2504.09014) |
| 106 | arXiv:2506.00413 |  |  | 3 | Diffusion LLM Inference, inference-systems, speculative-parallel-decoding | [source](https://arxiv.org/abs/2506.00413) |
| 107 | arXiv:2512.22420 |  |  | 3 | llm-serving-scheduling-disaggregation, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2512.22420) |
| 108 | DOI:10.1109/ispass.2019.00042 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, inference-systems, 長文推論・KVキャッシュ先読み・要求パッキング・オンチップメモリ・HBM帯域最適化 | [source](https://doi.org/10.1109/ispass.2019.00042) |
| 109 | DOI:10.1109/mm.2024.3373763 |  |  | 3 | KV Cache Offload / Recomputation, inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2024.3373763) |
| 110 | DOI:10.1145/1534530.1534544 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, offload-hierarchical-memory, オフロード／階層メモリ | [source](https://doi.org/10.1145/1534530.1534544) |
| 111 | DOI:10.1145/3489517.3530428 |  |  | 3 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3489517.3530428) |
| 112 | DOI:10.1145/3669940.3707231 |  |  | 3 | inference-systems, llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/3669940.3707231) |
| 113 | DOI:10.1145/3725843.3756121 |  |  | 3 | PIM / Near-Data Acceleration, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756121) |
| 114 | DOI:10.14778/3415478.3415530 |  |  | 3 | LLM Serving / Distributed Communication, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.14778/3415478.3415530) |
| 115 | DOI:10.52202/075280-2279 |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, other-inference-systems | [source](https://doi.org/10.52202/075280-2279) |
| 116 | OpenReview:5Qe7AGO3Eq |  |  | 3 | 17-pim-near-data-acceleration, kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=5Qe7AGO3Eq) |
| 117 | OpenReview:hmOwOZWzYE |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=hmOwOZWzYE) |
| 118 | OpenReview:SFN6Wm7YBI |  |  | 3 | dynamic megakernel compilation and GPU task scheduling, inference-systems, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=SFN6Wm7YBI) |
| 119 | OpenReview:YicbFdNTTy |  |  | 3 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, オフロード／階層メモリ | [source](https://openreview.net/forum?id=YicbFdNTTy) |
| 120 | arXiv:1410.0759 |  |  | 3 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems | [source](https://arxiv.org/abs/1410.0759) |
| 121 | arXiv:1802.06901 |  |  | 3 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1802.06901) |
| 122 | arXiv:2204.07675 |  |  | 3 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, training-memory-systems | [source](https://arxiv.org/abs/2204.07675) |
| 123 | arXiv:2302.13214 |  |  | 3 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2302.13214) |
| 124 | arXiv:2305.17144 |  |  | 3 | inference-systems, other-inference-systems | [source](https://arxiv.org/abs/2305.17144) |
| 125 | arXiv:2309.11235 |  |  | 3 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2309.11235) |
| 126 | arXiv:2310.05424 |  |  | 3 | speculative decoding / draft-model design, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2310.05424) |
| 127 | arXiv:2312.14852 |  |  | 3 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 128 | arXiv:2402.05406 |  |  | 3 | Adaptive Expert Computation / Compression, inference-systems | [source](https://arxiv.org/abs/2402.05406) |
| 129 | arXiv:2402.13116 |  |  | 3 | Speculative Decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.13116) |
| 130 | arXiv:2406.15786 |  |  | 3 | inference-systems, offload-hierarchical-memory | [source](https://arxiv.org/abs/2406.15786) |
| 131 | arXiv:2407.07000 |  |  | 3 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.07000) |
| 132 | arXiv:2408.08696 |  |  | 3 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2408.08696) |
| 133 | arXiv:2409.17146 |  |  | 3 | Adaptive computation／cache-aware MoE, adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2409.17146) |
| 134 | arXiv:2410.23079 |  |  | 3 | KVキャッシュオフロード／階層メモリ, System-aware KV cache | [source](https://arxiv.org/abs/2410.23079) |
| 135 | arXiv:2411.17116 |  |  | 3 | Long-context serving / KV cache benchmark, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2411.17116) |
| 136 | arXiv:2502.02617 |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02617) |
| 137 | arXiv:2504.16054 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2504.16054) |
| 138 | arXiv:2506.13585 |  |  | 3 | kv-cache-reuse-position-independent-caching, speculative-decoding | [source](https://arxiv.org/abs/2506.13585) |
| 139 | arXiv:2508.17196 |  |  | 3 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.17196) |
| 140 | arXiv:2602.08676 |  |  | 3 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2602.08676) |
| 141 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 142 | DOI:10.1109/isca45697.2020.00047 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/isca45697.2020.00047) |
| 143 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 144 | DOI:10.1145/3503222.3507709 |  |  | 3 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, inference-systems | [source](https://doi.org/10.1145/3503222.3507709) |
| 145 | DOI:10.1145/3636534.3649379 |  |  | 3 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3636534.3649379) |
| 146 | DOI:10.1145/3719330.3721230 |  |  | 3 | 08-edge-on-device-llm-systems, KV Cache Offload / Recomputation | [source](https://doi.org/10.1145/3719330.3721230) |
| 147 | DOI:10.18653/v1/2020.emnlp-main.550 |  |  | 3 | inference-systems, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2020.emnlp-main.550) |
| 148 | DOI:10.18653/v1/2024.acl-long.814 |  |  | 3 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.814) |
| 149 | DOI:10.57967/hf/2497 |  |  | 3 | KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, adaptive-expert-computation-compression | [source](https://doi.org/10.57967/hf/2497) |
| 150 | OpenReview:8Wuvhh0LYW |  |  | 3 | 17-pim-near-data-acceleration, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=8Wuvhh0LYW) |
| 151 | OpenReview:bsCCJHbO8A |  |  | 3 | inference-systems, 推論エンジン／推論基盤 | [source](https://openreview.net/forum?id=bsCCJHbO8A) |
| 152 | OpenReview:LKEJPySnlt |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=LKEJPySnlt) |
| 153 | OpenReview:ul4W26KEKz |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://openreview.net/forum?id=ul4W26KEKz) |
| 154 | arXiv:1606.06160 |  |  | 3 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 155 | arXiv:1908.09355 |  |  | 3 | Conditional Computation | [source](https://arxiv.org/abs/1908.09355) |
| 156 | arXiv:2102.12702 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2102.12702) |
| 157 | arXiv:2208.03299 |  |  | 3 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2208.03299) |
| 158 | arXiv:2301.12017 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2301.12017) |
| 159 | arXiv:2310.03533 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2310.03533) |
| 160 | arXiv:2402.04248 |  |  | 3 | prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2402.04248) |
| 161 | arXiv:2404.04475 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2404.04475) |
| 162 | arXiv:2405.14105 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2405.14105) |
| 163 | arXiv:2411.03519 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2411.03519) |
| 164 | arXiv:2504.16891 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2504.16891) |
| 165 | DOI:10.1109/tpds.2022.3144614 |  |  | 3 | inference-systems | [source](https://doi.org/10.1109/tpds.2022.3144614) |
| 166 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 167 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 168 | arXiv:2109.04838 |  |  | 3 |  | [source](https://arxiv.org/abs/2109.04838) |
| 169 | arXiv:2307.10169 |  |  | 3 |  | [source](https://arxiv.org/abs/2307.10169) |
| 170 | arXiv:2511.11571 |  |  | 3 |  | [source](https://arxiv.org/abs/2511.11571) |
| 171 | arXiv:1305.0445 |  |  | 2 | Conditional Computation, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1305.0445) |
| 172 | arXiv:1603.04467 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1603.04467) |
| 173 | arXiv:1805.00907 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1805.00907) |
| 174 | arXiv:1906.02041 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1906.02041) |
| 175 | arXiv:1911.11313 |  |  | 2 | inference-systems, 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 176 | arXiv:2004.11886 |  |  | 2 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2004.11886) |
| 177 | arXiv:2009.08034 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2009.08034) |
| 178 | arXiv:2011.01060 |  |  | 2 | kv-cache-offload-recomputation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification | [source](https://arxiv.org/abs/2011.01060) |
| 179 | arXiv:2102.11972 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2102.11972) |
| 180 | arXiv:2105.03036 |  |  | 2 | MoE inference / expert pruning / language-specific expert specialization, inference-systems | [source](https://arxiv.org/abs/2105.03036) |
| 181 | arXiv:2109.09115 |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems | [source](https://arxiv.org/abs/2109.09115) |
| 182 | arXiv:2110.15191 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2110.15191) |
| 183 | arXiv:2204.05999 |  |  | 2 | inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2204.05999) |
| 184 | arXiv:2206.02845 |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection, inference-systems | [source](https://arxiv.org/abs/2206.02845) |
| 185 | arXiv:2212.01378 |  |  | 2 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2212.01378) |
| 186 | arXiv:2301.08984 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, inference-systems | [source](https://arxiv.org/abs/2301.08984) |
| 187 | arXiv:2303.11366 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 188 | arXiv:2305.05252 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 189 | arXiv:2305.11206 |  |  | 2 | KVキャッシュ最適化／適応圧縮, inference-systems | [source](https://arxiv.org/abs/2305.11206) |
| 190 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 191 | arXiv:2308.06093 |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 192 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 193 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 194 | arXiv:2310.08041 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2310.08041) |
| 195 | arXiv:2311.01635 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.01635) |
| 196 | arXiv:2311.11501 |  |  | 2 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2311.11501) |
| 197 | arXiv:2311.17541 |  |  | 2 | agentic serving / workflow-aware scheduling / memory-aware dispatch, other-inference-systems | [source](https://arxiv.org/abs/2311.17541) |
| 198 | arXiv:2312.04511 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2312.04511) |
| 199 | arXiv:2312.16862 |  |  | 2 | LLM inference surveys、roofline performance analysis, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2312.16862) |
| 200 | arXiv:2402.00025 |  |  | 2 | GPU疎行列カーネル／二重疎LLM推論／SIMTマイクロアーキテクチャ, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.00025) |
| 201 | arXiv:2402.10193 |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2402.10193) |
| 202 | arXiv:2402.14762 |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 203 | arXiv:2403.03507 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, その他システム研究 | [source](https://arxiv.org/abs/2403.03507) |
| 204 | arXiv:2403.09347 |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 205 | arXiv:2404.03413 |  |  | 2 | inference-systems, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2404.03413) |
| 206 | arXiv:2404.09336 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2404.09336) |
| 207 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 208 | arXiv:2405.14428 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2405.14428) |
| 209 | arXiv:2406.02430 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.02430) |
| 210 | arXiv:2406.05317 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2406.05317) |
| 211 | arXiv:2406.07476 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2406.07476) |
| 212 | arXiv:2406.18485 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18485) |
| 213 | arXiv:2407.00128 |  |  | 2 | Speculative Decoding / Parallel Inference Systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.00128) |
| 214 | arXiv:2407.09816 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.09816) |
| 215 | arXiv:2407.11511 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2407.11511) |
| 216 | arXiv:2409.12640 |  |  | 2 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2409.12640) |
| 217 | arXiv:2409.16546 |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, inference-systems | [source](https://arxiv.org/abs/2409.16546) |
| 218 | arXiv:2410.00037 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.00037) |
| 219 | arXiv:2410.02660 |  |  | 2 | kv-cache-optimization-compression, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2410.02660) |
| 220 | arXiv:2410.04343 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.04343) |
| 221 | arXiv:2410.10934 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10934) |
| 222 | arXiv:2410.13461 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2410.13461) |
| 223 | arXiv:2410.17196 |  |  | 2 | llm-serving-scheduling-disaggregation, その他の推論システム | [source](https://arxiv.org/abs/2410.17196) |
| 224 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 225 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 226 | arXiv:2411.15242 |  |  | 2 | PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management | [source](https://arxiv.org/abs/2411.15242) |
| 227 | arXiv:2412.01447 |  |  | 2 | inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2412.01447) |
| 228 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 229 | arXiv:2501.03035 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2501.03035) |
| 230 | arXiv:2501.09959 |  |  | 2 | 07-kv-キャッシュ-optimization-compression, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2501.09959) |
| 231 | arXiv:2501.15368 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2501.15368) |
| 232 | arXiv:2502.01776 |  |  | 2 | Sparse Attention / VLM Inference, attention kernel / heterogeneous batched inference / KV-cache layout | [source](https://arxiv.org/abs/2502.01776) |
| 233 | arXiv:2502.04507 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2502.04507) |
| 234 | arXiv:2502.07861 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.07861) |
| 235 | arXiv:2502.09696 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2502.09696) |
| 236 | arXiv:2502.12444 |  |  | 2 | 10-kv-cache-offload-recomputation, CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/2502.12444) |
| 237 | arXiv:2502.14752 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2502.14752) |
| 238 | arXiv:2502.17599 |  |  | 2 | KV cache eviction / multimodal KV cache compression / diversity-aware token selection, inference-systems | [source](https://arxiv.org/abs/2502.17599) |
| 239 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 240 | arXiv:2503.23100 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2503.23100) |
| 241 | arXiv:2504.02605 |  |  | 2 | LLMサービング・スケジューリング・KVキャッシュ保持, inference-systems | [source](https://arxiv.org/abs/2504.02605) |
| 242 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 243 | arXiv:2504.12463 |  |  | 2 | Expert Prefetch, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2504.12463) |
| 244 | arXiv:2504.17768 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.17768) |
| 245 | arXiv:2505.04921 |  |  | 2 | 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2505.04921) |
| 246 | arXiv:2505.07608 |  |  | 2 | kv-cache-optimization-compression, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2505.07608) |
| 247 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 248 | arXiv:2505.16552 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.16552) |
| 249 | arXiv:2505.24034 |  |  | 2 | LLM Serving / Distributed Communication, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2505.24034) |
| 250 | arXiv:2506.04108 |  |  | 2 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2506.04108) |
| 251 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 252 | arXiv:2506.20807 |  |  | 2 | inference-systems, other-inference-systems | [source](https://arxiv.org/abs/2506.20807) |
| 253 | arXiv:2507.07120 |  |  | 2 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2507.07120) |
| 254 | arXiv:2507.16731 |  |  | 2 | 05-speculative-decoding-moe, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2507.16731) |
| 255 | arXiv:2508.06447 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, System-aware KV cache | [source](https://arxiv.org/abs/2508.06447) |
| 256 | arXiv:2508.08438 |  |  | 2 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08438) |
| 257 | arXiv:2508.16653 |  |  | 2 | 低ビット疎推論／GPUカーネル／エッジ推論, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2508.16653) |
| 258 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 259 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 260 | arXiv:2510.03293 |  |  | 2 | Expert Prefetch, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.03293) |
| 261 | arXiv:2510.12633 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.12633) |
| 262 | arXiv:2510.24273 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化 | [source](https://arxiv.org/abs/2510.24273) |
| 263 | arXiv:2511.16108 |  |  | 2 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2511.16108) |
| 264 | arXiv:2511.21689 |  |  | 2 | 14-agentic-inference-serving-runtime, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2511.21689) |
| 265 | arXiv:2512.04123 |  |  | 2 | Agentic Serving Benchmarking, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.04123) |
| 266 | arXiv:2512.12087 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.12087) |
| 267 | arXiv:2512.17077 |  |  | 2 | llm-serving-scheduling-disaggregation, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2512.17077) |
| 268 | arXiv:2601.06521 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2601.06521) |
| 269 | arXiv:2601.09527 |  |  | 2 | LLMサービング・スケジューリング・分離実行, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://arxiv.org/abs/2601.09527) |
| 270 | arXiv:2601.19092 |  |  | 2 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム, dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2601.19092) |
| 271 | arXiv:2602.02599 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2602.02599) |
| 272 | arXiv:2603.07685 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems | [source](https://arxiv.org/abs/2603.07685) |
| 273 | arXiv:2604.15409 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2604.15409) |
| 274 | arXiv:2606.03928 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2606.03928) |
| 275 | arXiv:2607.04031 |  |  | 2 | 10-kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2607.04031) |
| 276 | DOI:10.1016/j.parco.2015.09.001 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, hardware-accelerators | [source](https://doi.org/10.1016/j.parco.2015.09.001) |
| 277 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 278 | DOI:10.1109/dac63849.2025.11132883 |  |  | 2 | 17-pim-near-data-acceleration, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/dac63849.2025.11132883) |
| 279 | DOI:10.1109/hcs59251.2023.10254717 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/hcs59251.2023.10254717) |
| 280 | DOI:10.1109/hotchips.2019.8875680 |  |  | 2 | inference-systems, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hotchips.2019.8875680) |
| 281 | DOI:10.1109/hpca47549.2020.00035 |  |  | 2 | inference-systems, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1109/hpca47549.2020.00035) |
| 282 | DOI:10.1109/hpcc-css-icess.2015.82 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1109/hpcc-css-icess.2015.82) |
| 283 | DOI:10.1109/ijcnn.1993.716791 |  |  | 2 | MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, inference-systems | [source](https://doi.org/10.1109/ijcnn.1993.716791) |
| 284 | DOI:10.1109/ipdps47924.2020.00070 |  |  | 2 | Inference Kernel / Determinism, hardware-accelerators | [source](https://doi.org/10.1109/ipdps47924.2020.00070) |
| 285 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 286 | DOI:10.1109/isscc42614.2022.9731565 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, inference-systems | [source](https://doi.org/10.1109/isscc42614.2022.9731565) |
| 287 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 288 | DOI:10.1109/lca.2025.3566692 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/lca.2025.3566692) |
| 289 | DOI:10.1109/micro50266.2020.00071 |  |  | 2 | inference-systems, kv-cache-memory | [source](https://doi.org/10.1109/micro50266.2020.00071) |
| 290 | DOI:10.1109/mm.2023.3256796 |  |  | 2 | Expert Prefetch, inference-systems | [source](https://doi.org/10.1109/mm.2023.3256796) |
| 291 | DOI:10.1109/tbdata.2019.2921572 |  |  | 2 | RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/tbdata.2019.2921572) |
| 292 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 293 | DOI:10.1109/tpwrs.2022.3173250 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1109/tpwrs.2022.3173250) |
| 294 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 295 | DOI:10.1145/1810085.1810091 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/1810085.1810091) |
| 296 | DOI:10.1145/2485922.2485964 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/2485922.2485964) |
| 297 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 298 | DOI:10.1145/3133901 |  |  | 2 | kernel-runtime-compilation, unstructured sparsity / GPU inference kernels | [source](https://doi.org/10.1145/3133901) |
| 299 | DOI:10.1145/3297858.3304043 |  |  | 2 | hardware-accelerators, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3297858.3304043) |
| 300 | DOI:10.1145/3437801.3441593 |  |  | 2 | inference-systems, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3437801.3441593) |
| 301 | DOI:10.1145/3470496.3527440 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/3470496.3527440) |
| 302 | DOI:10.1145/3552326.3567508 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory | [source](https://doi.org/10.1145/3552326.3567508) |
| 303 | DOI:10.1145/3581784.3607034 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3581784.3607034) |
| 304 | DOI:10.1145/3605573.3605613 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3605573.3605613) |
| 305 | DOI:10.1145/3620666.3651369 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651369) |
| 306 | DOI:10.1145/3650200.3656636 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, 分散推論／集団通信圧縮／量子化AllReduce／XLA・TPU | [source](https://doi.org/10.1145/3650200.3656636) |
| 307 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 308 | DOI:10.1145/3706418 |  |  | 2 | 08-edge-on-device-llm-systems, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3706418) |
| 309 | DOI:10.1145/3725843.3756115 |  |  | 2 | PIM / Near-Data Acceleration, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756115) |
| 310 | DOI:10.1145/3767742 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3767742) |
| 311 | DOI:10.1145/3779212.3790236 |  |  | 2 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790236) |
| 312 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 313 | DOI:10.1609/aaai.v40i36.40255 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.1609/aaai.v40i36.40255) |
| 314 | DOI:10.18653/v1/2022.emnlp-main.823 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/2022.emnlp-main.823) |
| 315 | DOI:10.18653/v1/2024.findings-acl.179 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, 投機的デコード／MoE | [source](https://doi.org/10.18653/v1/2024.findings-acl.179) |
| 316 | DOI:10.18653/v1/2024.naacl-long.109 |  |  | 2 | inference-systems, multi-model LLM serving / prompt routing / resource allocation | [source](https://doi.org/10.18653/v1/2024.naacl-long.109) |
| 317 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 318 | DOI:10.18653/v1/w19-4828 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/w19-4828) |
| 319 | DOI:10.48550/arxiv.2304.11062 |  |  | 2 | inference-systems, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.48550/arxiv.2304.11062) |
| 320 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 321 | DOI:10.52202/079017-0040 |  |  | 2 | KV Cache Optimization / Compression, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://doi.org/10.52202/079017-0040) |
| 322 | DOI:10.52202/079017-3801 |  |  | 2 | KV Cache Optimization / Compression, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks | [source](https://doi.org/10.52202/079017-3801) |
| 323 | OpenReview:0fJfVOSUra |  |  | 2 | 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://openreview.net/forum?id=0fJfVOSUra) |
| 324 | OpenReview:acJ3vdFljk |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=acJ3vdFljk) |
| 325 | OpenReview:c5BOcHM6J8 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=c5BOcHM6J8) |
| 326 | OpenReview:dwPdYFqVWO |  |  | 2 | Speculative decoding × MoE, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://openreview.net/forum?id=dwPdYFqVWO) |
| 327 | OpenReview:FAeU7516MR |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE | [source](https://openreview.net/forum?id=FAeU7516MR) |
| 328 | OpenReview:HklBjCEKvH |  |  | 2 | Speculative Decoding, other-inference-systems | [source](https://openreview.net/forum?id=HklBjCEKvH) |
| 329 | OpenReview:JZfg6wGi6g |  |  | 2 | KV Cache Optimization / Compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=JZfg6wGi6g) |
| 330 | OpenReview:NGPmH3vbAA_ |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=NGPmH3vbAA_) |
| 331 | OpenReview:R7fv5NWfMm |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=R7fv5NWfMm) |
| 332 | OpenReview:RyOpooIxDF |  |  | 2 | inference-systems, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://openreview.net/forum?id=RyOpooIxDF) |
| 333 | OpenReview:xdNAVP7TGy |  |  | 2 | kv-cache-offload-recomputation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://openreview.net/forum?id=xdNAVP7TGy) |
| 334 | OpenReview:ySQH0oDyp7 |  |  | 2 | 18-vla-inference-quantization-evaluation, inference-systems | [source](https://openreview.net/forum?id=ySQH0oDyp7) |
| 335 | arXiv:1512.03385 |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1512.03385) |
| 336 | arXiv:1704.05426 |  |  | 2 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 337 | arXiv:1808.06866 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1808.06866) |
| 338 | arXiv:1902.09506 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1902.09506) |
| 339 | arXiv:1905.07799 |  |  | 2 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 340 | arXiv:1906.04341 |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 341 | arXiv:1909.12486 |  |  | 2 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1909.12486) |
| 342 | arXiv:2005.08100 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2005.08100) |
| 343 | arXiv:2010.02502 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2010.02502) |
| 344 | arXiv:2012.12624 |  |  | 2 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 345 | arXiv:2105.09938 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2105.09938) |
| 346 | arXiv:2111.00160 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 347 | arXiv:2112.07916 |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2112.07916) |
| 348 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 349 | arXiv:2206.14858 |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2206.14858) |
| 350 | arXiv:2210.05144 |  |  | 2 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2210.05144) |
| 351 | arXiv:2211.00593 |  |  | 2 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 352 | arXiv:2211.16750 |  |  | 2 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2211.16750) |
| 353 | arXiv:2302.09210 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2302.09210) |
| 354 | arXiv:2303.06349 |  |  | 2 | training-memory-systems | [source](https://arxiv.org/abs/2303.06349) |
| 355 | arXiv:2304.02017 |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 356 | arXiv:2305.10250 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 357 | arXiv:2305.14516 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://arxiv.org/abs/2305.14516) |
| 358 | arXiv:2306.02003 |  |  | 2 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 359 | arXiv:2306.04933 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 360 | arXiv:2307.06281 |  |  | 2 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2307.06281) |
| 361 | arXiv:2309.17452 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2309.17452) |
| 362 | arXiv:2312.12391 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2312.12391) |
| 363 | arXiv:2402.08644 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.08644) |
| 364 | arXiv:2403.10616 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.10616) |
| 365 | arXiv:2404.01744 |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2404.01744) |
| 366 | arXiv:2404.19124 |  |  | 2 | 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2404.19124) |
| 367 | arXiv:2405.06640 |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2405.06640) |
| 368 | arXiv:2406.09827 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2406.09827) |
| 369 | arXiv:2406.16635 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2406.16635) |
| 370 | arXiv:2407.13623 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2407.13623) |
| 371 | arXiv:2408.12320 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2408.12320) |
| 372 | arXiv:2409.03752 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2409.03752) |
| 373 | arXiv:2410.05265 |  |  | 2 | survey-low-bit-llm | [source](https://arxiv.org/abs/2410.05265) |
| 374 | arXiv:2410.13232 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2410.13232) |
| 375 | arXiv:2411.00114 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2411.00114) |
| 376 | arXiv:2411.10109 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2411.10109) |
| 377 | arXiv:2412.12687 |  |  | 2 | distributed speculative decoding / edge collaborative inference / communication-efficient inference | [source](https://arxiv.org/abs/2412.12687) |
| 378 | arXiv:2412.19821 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2412.19821) |
| 379 | arXiv:2501.06322 |  |  | 2 | multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2501.06322) |
| 380 | arXiv:2502.00299 |  |  | 2 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.00299) |
| 381 | arXiv:2502.05171 |  |  | 2 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2502.05171) |
| 382 | arXiv:2502.09601 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.09601) |
| 383 | arXiv:2502.16440 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3 | [source](https://arxiv.org/abs/2502.16440) |
| 384 | arXiv:2502.21074 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.21074) |
| 385 | arXiv:2504.19678 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2504.19678) |
| 386 | arXiv:2505.15778 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2505.15778) |
| 387 | arXiv:2505.20674 |  |  | 2 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.20674) |
| 388 | arXiv:2505.23885 |  |  | 2 | multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2505.23885) |
| 389 | arXiv:2506.06326 |  |  | 2 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2506.06326) |
| 390 | arXiv:2507.01079 |  |  | 2 | 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2507.01079) |
| 391 | arXiv:2509.09090 |  |  | 2 | 18-vla-inference-quantization-evaluation | [source](https://arxiv.org/abs/2509.09090) |
| 392 | arXiv:2510.03346 |  |  | 2 | agent serving / KV-cache reuse / latent communication / DAG workflows | [source](https://arxiv.org/abs/2510.03346) |
| 393 | arXiv:2511.09557 |  |  | 2 | Expert Prefetch | [source](https://arxiv.org/abs/2511.09557) |
| 394 | arXiv:2512.14681 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2512.14681) |
| 395 | arXiv:2602.08404 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2602.08404) |
| 396 | arXiv:2603.19610 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2603.19610) |
| 397 | arXiv:2604.26779 |  |  | 2 | 99-other-inference-systems | [source](https://arxiv.org/abs/2604.26779) |
| 398 | arXiv:2605.12825 |  |  | 2 | 投機的復号・Orthrus・推論再現性・数値精度 | [source](https://arxiv.org/abs/2605.12825) |
| 399 | DOI:10.1016/j.neunet.2017.12.012 |  |  | 2 | Speculative Decoding | [source](https://doi.org/10.1016/j.neunet.2017.12.012) |
| 400 | DOI:10.1109/hpca51647.2021.00049 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference | [source](https://doi.org/10.1109/hpca51647.2021.00049) |
| 401 | DOI:10.1109/imw.2017.7939084 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/imw.2017.7939084) |
| 402 | DOI:10.1109/isca52012.2021.00010 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isca52012.2021.00010) |
| 403 | DOI:10.1109/isocc53507.2021.9613933 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.1109/isocc53507.2021.9613933) |
| 404 | DOI:10.1109/isvlsi.2014.94 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isvlsi.2014.94) |
| 405 | DOI:10.1109/tpami.2018.2889473 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/tpami.2018.2889473) |
| 406 | DOI:10.1145/2749469.2749475 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2749469.2749475) |
| 407 | DOI:10.1145/3123939.3123977 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/3123939.3123977) |
| 408 | DOI:10.1145/3342195.3392698 |  |  | 2 | agent-runtime-sandbox-state-management | [source](https://doi.org/10.1145/3342195.3392698) |
| 409 | DOI:10.1145/3460971 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/3460971) |
| 410 | DOI:10.1145/3575693.3575748 |  |  | 2 | offload-hierarchical-memory | [source](https://doi.org/10.1145/3575693.3575748) |
| 411 | DOI:10.1145/3617232.3624871 |  |  | 2 | agent-runtime-sandbox-state-management | [source](https://doi.org/10.1145/3617232.3624871) |
| 412 | DOI:10.1145/3710848.3710878 |  |  | 2 | Adaptive computation／cache-aware MoE | [source](https://doi.org/10.1145/3710848.3710878) |
| 413 | DOI:10.1162/tacl_a_00475 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.1162/tacl_a_00475) |
| 414 | DOI:10.18653/v1/2020.acl-main.537 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.18653/v1/2020.acl-main.537) |
| 415 | DOI:10.18653/v1/2021.eacl-main.74 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.18653/v1/2021.eacl-main.74) |
| 416 | DOI:10.18653/v1/2022.findings-naacl.55 |  |  | 2 | inference-systems | [source](https://doi.org/10.18653/v1/2022.findings-naacl.55) |
| 417 | DOI:10.18653/v1/2023.emnlp-main.232 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.232) |
| 418 | DOI:10.18653/v1/2024.emnlp-main.1124 |  |  | 2 | Long-context serving / KV cache benchmark | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1124) |
| 419 | DOI:10.18653/v1/2024.findings-acl.195 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.195) |
| 420 | DOI:10.18653/v1/2025.emnlp-main.844 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2025.emnlp-main.844) |
| 421 | DOI:10.18653/v1/p16-1162 |  |  | 2 | 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/p16-1162) |
| 422 | DOI:10.3115/1073083.1073135 |  |  | 2 | confidential inference / trusted execution environment / split inference / differential privacy | [source](https://doi.org/10.3115/1073083.1073135) |
| 423 | OpenReview:0GRBKLBjJE |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=0GRBKLBjJE) |
| 424 | OpenReview:7zNYY1E2fq |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論 | [source](https://openreview.net/forum?id=7zNYY1E2fq) |
| 425 | OpenReview:COZDy0WYGg |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=COZDy0WYGg) |
| 426 | OpenReview:D9cnZNZfxX |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=D9cnZNZfxX) |
| 427 | OpenReview:h0ZfDIrj7T |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=h0ZfDIrj7T) |
| 428 | OpenReview:KUNzEQMWU7 |  |  | 2 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://openreview.net/forum?id=KUNzEQMWU7) |
| 429 | OpenReview:nJgS06sX3O |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=nJgS06sX3O) |
| 430 | OpenReview:RlqYCpTu1P |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=RlqYCpTu1P) |
| 431 | OpenReview:uPv9Y3gmAI5 |  |  | 2 | MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=uPv9Y3gmAI5) |
| 432 | OpenReview:vo9t20wsmd |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=vo9t20wsmd) |
| 433 | arXiv:1608.08710 |  |  | 2 |  | [source](https://arxiv.org/abs/1608.08710) |
| 434 | arXiv:2011.00943 |  |  | 2 |  | [source](https://arxiv.org/abs/2011.00943) |
| 435 | arXiv:2201.03533 |  |  | 2 |  | [source](https://arxiv.org/abs/2201.03533) |
| 436 | arXiv:2302.04089 |  |  | 2 |  | [source](https://arxiv.org/abs/2302.04089) |
| 437 | arXiv:2311.12793 |  |  | 2 |  | [source](https://arxiv.org/abs/2311.12793) |
| 438 | arXiv:2402.18510 |  |  | 2 |  | [source](https://arxiv.org/abs/2402.18510) |
| 439 | arXiv:2404.16821 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.16821) |
| 440 | arXiv:2407.12077 |  |  | 2 |  | [source](https://arxiv.org/abs/2407.12077) |
| 441 | arXiv:2410.15704 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.15704) |
| 442 | arXiv:2411.14033 |  |  | 2 |  | [source](https://arxiv.org/abs/2411.14033) |
| 443 | arXiv:2502.01960 |  |  | 2 |  | [source](https://arxiv.org/abs/2502.01960) |
| 444 | arXiv:2504.12285 |  |  | 2 |  | [source](https://arxiv.org/abs/2504.12285) |
| 445 | arXiv:2510.06189 |  |  | 2 |  | [source](https://arxiv.org/abs/2510.06189) |
| 446 | DOI:10.1145/3636534.3649361 |  |  | 2 |  | [source](https://doi.org/10.1145/3636534.3649361) |
| 447 | DOI:10.18653/v1/2022.bigscience-1.9 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2022.bigscience-1.9) |
| 448 | DOI:10.18653/v1/n19-1309 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/n19-1309) |
| 449 | DOI:10.48550/arxiv.2402.04347 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2402.04347) |
| 450 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 451 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 452 | OpenReview:FJFVmeXusW |  |  | 2 |  | [source](https://openreview.net/forum?id=FJFVmeXusW) |
| 453 | OpenReview:JXhROKNZzOc |  |  | 2 |  | [source](https://openreview.net/forum?id=JXhROKNZzOc) |
| 454 | OpenReview:QV79qiKAjD |  |  | 2 |  | [source](https://openreview.net/forum?id=QV79qiKAjD) |
| 455 | arXiv:1109.3843 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1109.3843) |
| 456 | arXiv:1205.2618 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 457 | arXiv:1211.0361 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1211.0361) |
| 458 | arXiv:1212.0402 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 459 | arXiv:1312.6211 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 460 | arXiv:1407.3561 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1407.3561) |
| 461 | arXiv:1412.6115 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1412.6115) |
| 462 | arXiv:1506.02438 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 463 | arXiv:1507.05910 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1507.05910) |
| 464 | arXiv:1511.01837 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 465 | arXiv:1511.06939 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 466 | arXiv:1512.02595 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1512.02595) |
| 467 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 468 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 469 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 470 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 471 | arXiv:1607.08022 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1607.08022) |
| 472 | arXiv:1609.09548 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1609.09548) |
| 473 | arXiv:1611.01540 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/1611.01540) |
| 474 | arXiv:1611.01704 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1611.01704) |
| 475 | arXiv:1701.03499 |  |  | 1 | NPU-PIM統合メモリ、近データ処理、LLM推論メモリ階層。NeuPIMs、IANUS、FACILの静的配置を動的実行へ拡張する。 | [source](https://arxiv.org/abs/1701.03499) |
| 476 | arXiv:1702.04008 |  |  | 1 | unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1702.04008) |
| 477 | arXiv:1703.05160 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 478 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 479 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 480 | arXiv:1711.03936 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 481 | arXiv:1712.05382 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.05382) |
| 482 | arXiv:1802.05365 |  |  | 1 | Training Offload / Memory Systems | [source](https://arxiv.org/abs/1802.05365) |
| 483 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 484 | arXiv:1803.07416 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1803.07416) |
| 485 | arXiv:1804.06087 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 486 | arXiv:1805.06407 |  |  | 1 | CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/1805.06407) |
| 487 | arXiv:1806.10779 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1806.10779) |
| 488 | arXiv:1807.11205 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1807.11205) |
| 489 | arXiv:1808.09121 |  |  | 1 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling | [source](https://arxiv.org/abs/1808.09121) |
| 490 | arXiv:1809.04281 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1809.04281) |
| 491 | arXiv:1810.03264 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.03264) |
| 492 | arXiv:1810.09305 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1810.09305) |
| 493 | arXiv:1811.05233 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 494 | arXiv:1812.01608 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1812.01608) |
| 495 | arXiv:1902.00732 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1902.00732) |
| 496 | arXiv:1902.06822 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1902.06822) |
| 497 | arXiv:1902.10186 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 498 | arXiv:1903.01699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 499 | arXiv:1904.03711 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1904.03711) |
| 500 | arXiv:1905.06566 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1905.06566) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

