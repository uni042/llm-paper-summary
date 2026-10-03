# Scheduled worker :00 worklist

Worker: `scheduled-chat-00`  
Generated: `2026-10-03T02:01:36+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **623** / 未claim総数: **476** / このworker向け: **159**

| # | 種別 | identity | title | source | 想定配置先 |
|---:|---|---|---|---|---|
| 1 | research | DOI:10.1145/3789240.3829347 | DynamoServe: A Distributed Tiered Memory System for Multi-tenant LLM Serving | [primary](https://www.semanticscholar.org/paper/3fada5fea76c30b6fb0f156189b080168f66e241) | `papers/inference/99-other-inference-systems/2026-3eaac796b1c5-dynamoserve-a-distributed-tiered-memory-system-for-multi-tenant-llm-serving.md` |
| 2 | research | DOI:10.1109/INFOCOM59046.2026.11571450 | Enabling Memory-Disaggregated Cloud Infrastructure for LLMs: An Adaptive CXL-based KV Cache Scheduling Approach | [primary](https://doi.org/10.1109/INFOCOM59046.2026.11571450) | `papers/inference/99-other-inference-systems/2026-95a006929f30-enabling-memory-disaggregated-cloud-infrastructure-for-llms-an-adaptive-cxl-based-kv-cache-scheduling-approach.md` |
| 3 | research | DOI:10.1145/3712285.3759903 | Diff-MoE: Efficient Batched MoE Inference with Priority-Driven Differential Expert Caching | [primary](https://doi.org/10.1145/3712285.3759903) | `papers/inference/04-moe-offload-expert-cache/2025-diff-moe-priority-driven-differential-expert-caching.md` |
| 4 | research | DOI:10.1145/3821219 | AdaptiveKV: Accelerating KV Cache Offloading with a Bandwidth-Adaptive Memory Allocation Mechanism | [primary](https://doi.org/10.1145/3821219) | `papers/inference/99-other-inference-systems/2026-96d0bc7068f2-adaptivekv-accelerating-kv-cache-offloading-with-a-bandwidth-adaptive-memory-allocation-mechanism.md` |
| 5 | research | DOI:10.1145/3789240.3828750 | ARK: Avoiding Routing Collisions for KV Cache Transfer in Disaggregated LLM Inference | [primary](https://www.semanticscholar.org/paper/713681b5ad435a87d94c6eb057a4b06f97a99c22) | `papers/inference/99-other-inference-systems/2026-5d556af29afc-ark-avoiding-routing-collisions-for-kv-cache-transfer-in-disaggregated-llm-inference.md` |
| 6 | research | arXiv:2603.02217 | Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression | [primary](https://arxiv.org/abs/2603.02217) | `papers/inference/02-adaptive-expert-computation-compression/2026-2603.02217-router-calibration-moe-compression.md` |
| 7 | research | arXiv:2604.10603 | MoEITS: A Green AI approach for simplifying MoE-LLMs | [primary](https://arxiv.org/abs/2604.10603) | `papers/inference/02-adaptive-expert-computation-compression/2026-2604.10603-moeits-information-theoretic-simplification.md` |
| 8 | research | arXiv:2609.13486 | Mixture-of-Experts Language Models Can Be Strong and Efficient Retrievers | [primary](https://arxiv.org/abs/2609.13486) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.13486-efficient-moe-retrievers-adaptive-expert-count.md` |
| 9 | research | DOI:10.1145/3838177.3841735 | Congestion-Aware Serving of Agentic LLM Applications | [primary](https://www.semanticscholar.org/paper/adc66da23cd03d90f351c1db39703742f0ec85d9) | `papers/inference/99-other-inference-systems/2026-80e75f6f533b-congestion-aware-serving-of-agentic-llm-applications.md` |
| 10 | research | DOI:10.1145/3789240.3829201 | Balancing and Beyond: Communication-Centric Optimizations in Expert Parallelism | [primary](https://www.semanticscholar.org/paper/eac99489e90aa20cb13cb7d63f53c9014b797164) | `papers/inference/99-other-inference-systems/2026-0e42e21dd7f9-balancing-and-beyond-communication-centric-optimizations-in-expert-parallelism.md` |
| 11 | research | DOI:10.1109/TCAD.2025.3648674 | DuoPIM: RRAM–DRAM Hybrid PIM Acceleration for Flexible-Batch LLM Decoding | [primary](https://www.semanticscholar.org/paper/bccca75ef45fe933f099b3ff1fd54d7a8077b8c1) | `papers/inference/99-other-inference-systems/2026-930e81a91eca-duopim-rramdram-hybrid-pim-acceleration-for-flexible-batch-llm-decoding.md` |
| 12 | research | arXiv:2609.11687 | Structured Transforms for Low-Overhead Quantization of Language Models | [primary](https://www.semanticscholar.org/paper/aa2d1e435c726e052e5550468c8d4cf60db59331) | `papers/inference/99-other-inference-systems/2026-2609.11687-structured-transforms-for-low-overhead-quantization-of-language-models.md` |
| 13 | research | arXiv:2509.26520 | Training Matryoshka Mixture-of-Experts for Elastic Inference-Time Expert Utilization | [primary](https://arxiv.org/abs/2509.26520) | `papers/inference/02-adaptive-expert-computation-compression/2025-2509.26520-matryoshka-moe-elastic-expert-utilization.md` |
| 14 | research | arXiv:2602.11192 | MELINOE: Fine-Tuning Enables Memory-Efficient Inference for Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2602.11192) | `papers/inference/02-adaptive-expert-computation-compression/2026-2602.11192-melinoe-memory-efficient-inference.md` |
| 15 | research | arXiv:2507.00390 | MoNE: Replacing Redundant Experts with Lightweight Novices for Structured Pruning of MoE | [primary](https://arxiv.org/abs/2507.00390) | `papers/inference/02-adaptive-expert-computation-compression/2025-2507.00390-mone-lightweight-novices.md` |
| 16 | research | arXiv:2609.16503 | Dense to MoE Adaptation for Compact Vision Language Action Policies | [primary](https://arxiv.org/abs/2609.16503) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.16503-adade-dynamic-expert-deactivation.md` |
| 17 | research | OpenAlex:W7165293849 | Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale | [primary](https://hdl.handle.net/10919/143438) | `papers/inference/99-other-inference-systems/2026-2f1f58b49e98-disaggregated-llm-serving-with-cxl-shared-memory-kv-cache-at-rack-scale.md` |
| 18 | research | DOI:10.1145/3832810.3832840 | RPSC: Robust LLM Scheduling by Tolerating Prediction Inaccuracy and Mitigating Tail Latency | [primary](https://www.semanticscholar.org/paper/d6928989c68496141ed1c5c207f742bc9cad96db) | `papers/inference/99-other-inference-systems/2026-a9f776eee2e3-rpsc-robust-llm-scheduling-by-tolerating-prediction-inaccuracy-and-mitigating-tail-latency.md` |
| 19 | research | arXiv:2608.25053 | Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels | [primary](https://www.semanticscholar.org/paper/61247ec0864a2c3fc0b9cbe68fb6e1495961a02b) | `papers/inference/99-other-inference-systems/2026-2608.25053-hydra-phase-aware-workload-characterization-of-llm-inference-across-edge-soc-generations-backends-and-quantization-level.md` |
| 20 | research | arXiv:2605.29350 | ConMoE: Expert-Pool Consolidation via Prototype Reassignment for MoE Compression | [primary](https://arxiv.org/abs/2605.29350) | `papers/inference/02-adaptive-expert-computation-compression/2026-2605.29350-conmoe-prototype-reassignment-compression.md` |
| 21 | research | arXiv:2605.28207 | Pruning and Distilling Mixture-of-Experts into Dense Language Models | [primary](https://arxiv.org/abs/2605.28207) | `papers/inference/02-adaptive-expert-computation-compression/2026-2605.28207-prune-distill-moe-to-dense.md` |
| 22 | research | DOI:10.1016/j.neunet.2026.109469 | DR-EFT: Exploring and reloading domain-representative experts for the memory-constrained fine-tuning of MoE large models | [primary](https://doi.org/10.1016/j.neunet.2026.109469) | `papers/training/01-training-offload-memory-systems/2026-dr-eft-domain-representative-expert-finetuning.md` |
| 23 | research | arXiv:2605.19775 | Understanding Inference Scaling for LLMS: Bottlenecks, Trade-Offs, and Performance Principles | [primary](https://www.semanticscholar.org/paper/930b5019707807053d41976f1cb09512a8dd9b18) | `papers/inference/99-other-inference-systems/2026-2605.19775-understanding-inference-scaling-for-llms-bottlenecks-trade-offs-and-performance-principles.md` |
| 24 | research | arXiv:2609.11716 | Why Does Post-Training Quantization Work? | [primary](https://www.semanticscholar.org/paper/92b8bb2aa2e91d22e81ec850e61ced274289eb57) | `papers/inference/99-other-inference-systems/2026-2609.11716-why-does-post-training-quantization-work.md` |
| 25 | research | arXiv:2604.19835 | Expert Upcycling: Shifting the Compute-Efficient Frontier of Mixture-of-Experts | [primary](https://arxiv.org/abs/2604.19835) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2604.19835-expert-upcycling-progressive-moe-expansion.md` |
| 26 | research | DOI:10.1109/JIOT.2026.3718029 | Efficient LLM Coserving at the Edge via Resource-Aware Cooperative Scheduling | [primary](https://www.semanticscholar.org/paper/3f71f011292d4504aa0b754cb9854b3140cba51b) | `papers/inference/99-other-inference-systems/2026-d935ef5e0c55-efficient-llm-coserving-at-the-edge-via-resource-aware-cooperative-scheduling.md` |
| 27 | research | arXiv:2609.08115 | Router Prior Bias: Preserving Base Routing Structure in MoE Post-Training | [primary](https://arxiv.org/abs/2609.08115) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2609.08115-router-prior-bias-soft-router-anchoring.md` |
| 28 | research | DOI:10.1109/TMC.2026.3697502 | CALSI: Context-Aware Layer Skipping Inference for On-Device LLM Serving | [primary](https://www.semanticscholar.org/paper/b55f24c3e3257011b8dc6ea308c4f54242ab7e53) | `papers/inference/99-other-inference-systems/2026-392ca7562b95-calsi-context-aware-layer-skipping-inference-for-on-device-llm-serving.md` |
| 29 | research | arXiv:2607.04164 | BrownoutMoE: Structure-Aware Expert Grouping for Efficient and Accurate LLM Web-based Services | [primary](https://www.semanticscholar.org/paper/f8b43d078a89a2622af43b6f1855dffcece37dbb) | `papers/inference/99-other-inference-systems/2026-2607.04164-brownoutmoe-structure-aware-expert-grouping-for-efficient-and-accurate-llm-web-based-services.md` |
| 30 | research | arXiv:2405.14636 | PerLLM: Personalized Inference Scheduling with Edge-Cloud Collaboration for Diverse LLM Services | [primary](https://arxiv.org/abs/2405.14636) | `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2405.14636-perllm.md` |
| 31 | research | arXiv:1909.08053 | Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | [primary](https://arxiv.org/abs/1909.08053) | `papers/training/03-pipeline-parallel-modular-training/2019-1909.08053-megatron-lm.md` |
| 32 | research | DOI:10.1109/IMNS67862.2026.11655252 | Characterizing Predictability–Latency Trade-offs of KV-Cache SSD Offloading in LMCache for LLM Serving Systems | [primary](https://doi.org/10.1109/IMNS67862.2026.11655252) | `papers/inference/10-kv-cache-offload-recomputation/2026-lmcache-kv-cache-ssd-offloading-predictability-latency.md` |
| 33 | research | arXiv:2609.02652 | Unfolding the Leech Lattice: Fused Multi-Shell Decoding and VRAM Layouts for 2-Bit LLM Weights | [primary](https://www.semanticscholar.org/paper/e367265fbfc519f2fe477b741f7b2d57372c3783) | `papers/inference/99-other-inference-systems/2026-2609.02652-unfolding-the-leech-lattice-fused-multi-shell-decoding-and-vram-layouts-for-2-bit-llm-weights.md` |
| 34 | research | arXiv:2407.04656 | Lazarus: Resilient and Elastic Training of Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2407.04656) | `papers/inference/99-other-inference-systems/2024-2407.04656-lazarus-resilient-and-elastic-training-of-mixture-of-experts-models.md` |
| 35 | research | DOI:10.1145/3830086 | CELLServe: An SLO-Aware and Cost Efficient LLMs Serving System for Serverless Computing Environments | [primary](https://doi.org/10.1145/3830086) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-cellserve-serverless-pd-disaggregation.md` |
| 36 | research | arXiv:2605.25550 | DisagFusion: Asynchronous Pipeline Parallelism and Elastic Scheduling for Disaggregated Diffusion Serving | [primary](https://arxiv.org/abs/2605.25550) | `papers/inference/99-other-inference-systems/2026-2605.25550-disagfusion-asynchronous-pipeline-parallelism-and-elastic-scheduling-for-disaggregated-diffusion-serving.md` |
| 37 | research | arXiv:2608.14376 | CoRun: Padding is Simple and Efficient for Deterministic LLM Inference | [primary](https://arxiv.org/abs/2608.14376) | `papers/inference/99-other-inference-systems/2026-2608.14376-corun-padding-is-simple-and-efficient-for-deterministic-llm-inference.md` |
| 38 | research | DOI:10.1109/LES.2025.3616900 | LPC: Efficient Lossless Parameter Compression for Deploying LLM Inference on Edge Systems | [primary](https://www.semanticscholar.org/paper/369189b30f08cc120594b39a7e352a38e5a72228) | `papers/inference/99-other-inference-systems/2026-43ece4bae0c5-lpc-efficient-lossless-parameter-compression-for-deploying-llm-inference-on-edge-systems.md` |
| 39 | research | arXiv:2608.21952 | SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality | [primary](https://arxiv.org/abs/2608.21952) | `papers/inference/99-other-inference-systems/2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md` |
| 40 | research | arXiv:2608.13966 | QUASAR: Lowering the Loss Floor of Quantization-Aware Training with Loss-Aware Reconstruction | [primary](https://arxiv.org/abs/2608.13966) | `papers/inference/99-other-inference-systems/2026-2608.13966-quasar-lowering-the-loss-floor-of-quantization-aware-training-with-loss-aware-reconstruction.md` |
| 41 | research | DOI:10.1109/LCA.2026.3660969 | H3: Hybrid Architecture Using High Bandwidth Memory and High Bandwidth Flash for Cost-Efficient LLM Inference | [primary](https://doi.org/10.1109/LCA.2026.3660969) | `papers/inference/99-other-inference-systems/2026-27b000808907-h3-hybrid-architecture-using-high-bandwidth-memory-and-high-bandwidth-flash-for-cost-efficient-llm-inference.md` |
| 42 | research | DOI:10.1145/3789240.3822569 | Memory as a First‑Class Resource in AI‑Factory Simulation | [primary](https://www.semanticscholar.org/paper/ab6071dcfef2e4a7092fdb5866e5a34485b28d51) | `papers/inference/99-other-inference-systems/2026-739d27a164e4-memory-as-a-firstclass-resource-in-aifactory-simulation.md` |
| 43 | research | DOI:10.1109/JCC72984.2026.00058 | UNAS: Urgency- and Fairness-Aware Scheduling for SLO-Oriented LLM Serving | [primary](https://doi.org/10.1109/JCC72984.2026.00058) | `papers/inference/99-other-inference-systems/2020-2026.00058-unas-urgency-and-fairness-aware-scheduling-for-slo-oriented-llm-serving.md` |
| 44 | research | arXiv:2306.11695 | A Simple and Effective Pruning Approach for Large Language Models | [primary](https://arxiv.org/abs/2306.11695) | `papers/inference/99-other-inference-systems/2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md` |
| 45 | research | arXiv:2608.28444 | Sliding-window beats linear attention | [primary](https://www.semanticscholar.org/paper/633f43137abd58fdd39606b868b27eccafae8625) | `papers/inference/99-other-inference-systems/2026-2608.28444-sliding-window-beats-linear-attention.md` |
| 46 | research | arXiv:2608.15118 | Collective Communication for Distributed LLM Systems: Planning, Runtime Adaptation, and Computation Coordination | [primary](https://arxiv.org/abs/2608.15118) | `papers/inference/99-other-inference-systems/2026-2608.15118-collective-communication-for-distributed-llm-systems-planning-runtime-adaptation-and-computation-coordination.md` |
| 47 | research | arXiv:2609.00363 | Deterministic LLM Inference Across GPU Kernels: Power-of-Two INT8 Quantization Scales and the Limits of Tolerance-Based Conformance | [primary](https://arxiv.org/abs/2609.00363) | `papers/inference/99-other-inference-systems/2026-2609.00363-deterministic-llm-inference-gpu-kernels-int8.md` |
| 48 | research | arXiv:2507.19427 | Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding | [primary](https://arxiv.org/abs/2507.19427) | `papers/inference/99-other-inference-systems/2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective-decoding.md` |
| 49 | research | DOI:10.1109/TNET.2024.3355010 | DistMind: Efficient Resource Disaggregation for Deep Learning Workloads | [primary](https://www.semanticscholar.org/paper/1112ac74f9299838c8a354f778fbbfd951dfc50c) | `papers/inference/99-other-inference-systems/2026-d66009615d04-distmind-efficient-resource-disaggregation-for-deep-learning-workloads.md` |
| 50 | research | arXiv:2605.06472 | Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management | [primary](https://arxiv.org/abs/2605.06472) | `papers/inference/99-other-inference-systems/2026-2605.06472-efficient-serving-for-dynamic-agent-workflows-with-prediction-based-kv-cache-management.md` |
| 51 | research | DOI:10.1109/ICWS72778.2026.00157 | Towards Efficient and Reliable On-Device Multi-Agent Systems: Challenges, Technologies and Explorations | [primary](https://www.semanticscholar.org/paper/6b7fe9189df482320578bffea03b382d9220ecda) | `papers/inference/99-other-inference-systems/2020-2026.00157-towards-efficient-and-reliable-on-device-multi-agent-systems-challenges-technologies-and-explorations.md` |
| 52 | research | arXiv:2604.07144 | Autopoiesis: A Self-Evolving System Paradigm for LLM Serving Under Runtime Dynamics | [primary](https://arxiv.org/abs/2604.07144) | `papers/inference/99-other-inference-systems/2026-2604.07144-autopoiesis-self-evolving-llm-serving-runtime-dynamics.md` |
| 53 | research | DOI:10.1109/CCGrid68966.2026.00014 | Quicktopia: Iteration-Level GPU Frequency Control for Energy–Latency Co-Optimization in LLM Inference | [primary](https://www.semanticscholar.org/paper/88a222b2340b8906e15edd5efd58293b25fc38ce) | `papers/inference/99-other-inference-systems/2020-2026.00014-quicktopia-iteration-level-gpu-frequency-control-for-energylatency-co-optimization-in-llm-inference.md` |
| 54 | research | arXiv:2603.04797 | Hardware-Software Co-design for 3D-DRAM-based LLM Serving Accelerator | [primary](https://arxiv.org/abs/2603.04797) | `papers/inference/99-other-inference-systems/2026-2603.04797-hardware-software-co-design-for-3d-dram-based-llm-serving-accelerator.md` |
| 55 | research | arXiv:2406.02500 | Towards Efficient Mixture of Experts: A Holistic Study of Compression Techniques | [primary](https://arxiv.org/abs/2406.02500) | `papers/inference/02-adaptive-expert-computation-compression/2024-2406.02500-towards-efficient-mixture-of-experts-holistic-compression.md` |
| 56 | research | arXiv:2409.10516 | RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval | [primary](https://arxiv.org/abs/2409.10516) | `papers/inference/10-kv-cache-offload-recomputation/2024-2409.10516-retrievalattention-vector-retrieval.md` |
| 57 | research | arXiv:2502.10517 | KernelBench: Can LLMs Write Efficient GPU Kernels? | [primary](https://arxiv.org/abs/2502.10517) | `papers/inference/99-other-inference-systems/2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md` |
| 58 | research | arXiv:2311.01282 | FlashDecoding++: Faster Large Language Model Inference on GPUs | [primary](https://arxiv.org/abs/2311.01282) | `papers/inference/99-other-inference-systems/2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md` |
| 59 | research | arXiv:2301.00774 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | [primary](https://www.semanticscholar.org/paper/909ad57ce8caa6b390a65ae09db352d27d8f3996) | `papers/inference/99-other-inference-systems/2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md` |
| 60 | research | DOI:10.1145/3805621.3807651 | Hardware-Aware Co-Design of Multi-Chip LLM Serving via Performance Modeling | [primary](https://doi.org/10.1145/3805621.3807651) | `papers/inference/99-other-inference-systems/2026-dae506ee161c-hardware-aware-co-design-of-multi-chip-llm-serving-via-performance-modeling.md` |
| 61 | research | arXiv:2510.16040 | Kelle: Co-design KV Caching and eDRAM for Efficient LLM Serving in Edge Computing | [primary](https://arxiv.org/abs/2510.16040) | `papers/inference/06-kv-cache-memory/2025-2510.16040-kelle-kv-cache-edram-edge-serving.md` |
| 62 | audit | arXiv:2504.03775 | FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling | [primary](https://arxiv.org/abs/2504.03775) | `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.03775-flowkv-low-latency-transfer-load-aware.md` |
| 63 | research | arXiv:2608.09225 | Governing the KV Cache: Preventing Timing Side-Channel Leakage in Multi-Tenant LLM Inference | [primary](https://arxiv.org/abs/2608.09225) | `papers/inference/99-other-inference-systems/2026-2608.09225-governing-kv-cache-multitenant-isolation.md` |
| 64 | research | arXiv:2510.14392 | FairBatching: Fairness-Aware Batch Formation for LLM Inference | [primary](https://arxiv.org/abs/2510.14392) | `papers/inference/99-other-inference-systems/2025-2510.14392-fairbatching-fairness-aware-batch-formation-for-llm-inference.md` |
| 65 | research | arXiv:2608.05926 | BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge | [primary](https://arxiv.org/abs/2608.05926) | `papers/inference/08-edge-on-device-llm-systems/2026-2608.05926-balance-hybrid-autoregressive-speculative-edge.md` |
| 66 | research | DOI:10.1109/tkde.2025.3554028 | A Survey on Mixture of Experts in Large Language Models | [primary](https://doi.org/10.1109/TKDE.2025.3554028) | `papers/inference/99-other-inference-systems/2026-9d9dc7b7bf03-a-survey-on-mixture-of-experts-in-large-language-models.md` |
| 67 | research | arXiv:2608.29745 | JITterFlip: Uncovering Fault Attack Surfaces in JIT-Compiled LLM Serving | [primary](https://arxiv.org/abs/2608.29745) | `papers/inference/99-other-inference-systems/2026-2608.29745-jitterflip-jit-compiled-llm-serving-fault-surfaces.md` |
| 68 | research | arXiv:2404.14527 | Mélange: Cost Efficient Large Language Model Serving by Exploiting GPU Heterogeneity | [primary](https://arxiv.org/abs/2404.14527) | `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2404.14527-melange-cost-efficient-llm-serving-gpu-heterogeneity.md` |
| 69 | research | arXiv:2404.12457 | RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2404.12457) | `papers/inference/99-other-inference-systems/2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md` |
| 70 | research | arXiv:2402.02082 | GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding | [primary](https://arxiv.org/abs/2402.02082) | `papers/inference/99-other-inference-systems/2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md` |
| 71 | research | arXiv:2209.01188 | Petals: Collaborative Inference and Fine-tuning of Large Models | [primary](https://arxiv.org/abs/2209.01188) | `papers/inference/99-other-inference-systems/2022-2209.01188-petals-collaborative-inference-and-fine-tuning-of-large-models.md` |
| 72 | research | arXiv:2603.07810 | Temperature-Aware Scheduling of LLM Inference in Large-Scale Geo-Distributed Edge Data Centers with Distributed Optimization | [primary](https://arxiv.org/abs/2603.07810) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2603.07810-temperature-aware-geo-distributed-llm-scheduling.md` |
| 73 | research | arXiv:2206.01861 | ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers | [primary](https://arxiv.org/abs/2206.01861) | `papers/inference/99-other-inference-systems/2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-scale-transformers.md` |
| 74 | research | SemanticScholar:d79a26226393f687ddbc375e32055b40b8ad8d38 | GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism | [primary](https://www.semanticscholar.org/paper/d79a26226393f687ddbc375e32055b40b8ad8d38) | `papers/inference/99-other-inference-systems/2026-e5d747247a09-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism.md` |
| 75 | research | arXiv:2202.08906 | ST-MoE | [primary](https://arxiv.org/abs/2202.08906) | `papers/inference/99-other-inference-systems/2022-2202.08906-st-moe.md` |
| 76 | research | arXiv:2402.04396 | QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks | [primary](https://arxiv.org/abs/2402.04396) | `papers/inference/99-other-inference-systems/2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-codebooks.md` |
| 77 | research | arXiv:2008.12260 | Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning | [primary](https://arxiv.org/abs/2008.12260) | `papers/inference/99-other-inference-systems/2020-2008.12260-pollux-co-adaptive-cluster-scheduling-for-goodput-optimized-deep-learning.md` |
| 78 | research | arXiv:2006.02464 | Serving DNNs like Clockwork: Performance Predictability from the Bottom Up | [primary](https://arxiv.org/abs/2006.02464) | `papers/inference/99-other-inference-systems/2020-2006.02464-serving-dnns-like-clockwork-performance-predictability-from-the-bottom-up.md` |
| 79 | research | arXiv:2504.15720 | SeaLLM: Service-Aware and Latency-Optimized Resource Sharing for Large Language Model Inference | [primary](https://arxiv.org/abs/2504.15720) | `papers/inference/99-other-inference-systems/2025-2504.15720-seallm-service-aware-and-latency-optimized-resource-sharing-for-large-language-model-inference.md` |
| 80 | research | arXiv:2511.17560 | A3: Attention-Aware Accurate KV Cache Fusion for Fast Large Language Model Serving | [primary](https://arxiv.org/abs/2511.17560) | `papers/inference/99-other-inference-systems/2025-2511.17560-a3-attention-aware-accurate-kv-cache-fusion-for-fast-large-language-model-serving.md` |
| 81 | research | arXiv:2511.13676 | T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization | [primary](https://arxiv.org/abs/2511.13676) | `papers/inference/99-other-inference-systems/2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-place-simd-alu-reorganization.md` |
| 82 | research | arXiv:2503.16428 | XAttention: Block Sparse Attention with Antidiagonal Scoring | [primary](https://arxiv.org/abs/2503.16428) | `papers/inference/99-other-inference-systems/2025-2503.16428-xattention-block-sparse-attention-with-antidiagonal-scoring.md` |
| 83 | research | arXiv:2601.05109 | Nalar: A Serving Framework for Agent Workflows | [primary](https://arxiv.org/abs/2601.05109) | `papers/inference/99-other-inference-systems/2026-2601.05109-nalar-a-serving-framework-for-agent-workflows.md` |
| 84 | research | arXiv:2402.18096 | No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization | [primary](https://arxiv.org/abs/2402.18096) | `papers/inference/99-other-inference-systems/2024-2402.18096-no-token-left-behind-reliable-kv-cache-compression-via-importance-aware-mixed-precision-quantization.md` |
| 85 | research | arXiv:2502.18137 | SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference | [primary](https://arxiv.org/abs/2502.18137) | `papers/inference/99-other-inference-systems/2025-2502.18137-spargeattention-accurate-and-training-free-sparse-attention-accelerating-any-model-inference.md` |
| 86 | research | arXiv:2403.07652 | Harder Tasks Need More Experts: Dynamic Routing in MoE Models | [primary](https://arxiv.org/abs/2403.07652) | `papers/inference/99-other-inference-systems/2024-2403.07652-harder-tasks-need-more-experts-dynamic-routing-in-moe-models.md` |
| 87 | research | arXiv:2403.01136 | LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Aware Partition and Adaptive Quantization | [primary](https://arxiv.org/abs/2403.01136) | `papers/inference/99-other-inference-systems/2024-2403.01136-llm-pq-serving-llm-on-heterogeneous-clusters-with-phase-aware-partition-and-adaptive-quantization.md` |
| 88 | research | arXiv:2511.07427 | DynaKV: Enabling Accurate and Efficient Long-Sequence LLM Decoding on Smartphones | [primary](https://arxiv.org/abs/2511.07427) | `papers/inference/99-other-inference-systems/2025-2511.07427-dynakv-enabling-accurate-and-efficient-long-sequence-llm-decoding-on-smartphones.md` |
| 89 | research | DOI:10.1145/3689031.3696072 | Fast State Restoration in LLM Serving with HCache | [primary](https://doi.org/10.1145/3689031.3696072) | `papers/inference/99-other-inference-systems/0000-c57896a0996e-fast-state-restoration-in-llm-serving-with-hcache.md` |
| 90 | research | arXiv:2506.02634 | KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider | [primary](https://arxiv.org/abs/2506.02634) | `papers/inference/99-other-inference-systems/2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at-a-large-cloud-provider.md` |
| 91 | research | arXiv:2402.15220 | ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition | [primary](https://arxiv.org/abs/2402.15220) | `papers/inference/99-other-inference-systems/2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-two-phase-partition.md` |
| 92 | research | arXiv:2510.08731 | When to Reason: Semantic Router for vLLM | [primary](https://arxiv.org/abs/2510.08731) | `papers/inference/99-other-inference-systems/2025-2510.08731-when-to-reason-semantic-router-for-vllm.md` |
| 93 | research | arXiv:2403.08245 | Scattered Mixture-of-Experts Implementation | [primary](https://arxiv.org/abs/2403.08245) | `papers/inference/99-other-inference-systems/2024-2403.08245-scattered-mixture-of-experts-implementation.md` |
| 94 | research | arXiv:2109.01611 | Multi-model Machine Learning Inference Serving with GPU Spatial Partitioning | [primary](https://arxiv.org/abs/2109.01611) | `papers/inference/99-other-inference-systems/2021-2109.01611-multi-model-machine-learning-inference-serving-with-gpu-spatial-partitioning.md` |
| 95 | research | DOI:10.1145/3725338 | PQCache: Product Quantization-based KVCache for Long Context LLM Inference | [primary](https://doi.org/10.1145/3725338) | `papers/inference/99-other-inference-systems/0000-24362ae4b461-pqcache-product-quantization-based-kvcache-for-long-context-llm-inference.md` |
| 96 | research | arXiv:2602.09721 | Revealing the Challenges of Attention-FFN Disaggregation for Modern MoE Models and Hardware Systems | [primary](https://arxiv.org/abs/2602.09721) | `papers/inference/99-other-inference-systems/2026-2602.09721-revealing-the-challenges-of-attention-ffn-disaggregation-for-modern-moe-models-and-hardware-systems.md` |
| 97 | research | DOI:10.52202/079017-0722 | SnapKV: LLM Knows What You are Looking for Before Generation | [primary](https://doi.org/10.52202/079017-0722) | `papers/inference/99-other-inference-systems/0000-838f46f28a47-snapkv-llm-knows-what-you-are-looking-for-before-generation.md` |
| 98 | research | arXiv:2509.24663 | InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation | [primary](https://arxiv.org/abs/2509.24663) | `papers/inference/99-other-inference-systems/2025-2509.24663-infllm-v2-dense-sparse-switchable-attention-for-seamless-short-to-long-adaptation.md` |
| 99 | research | arXiv:2201.12023 | Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning | [primary](https://arxiv.org/abs/2201.12023) | `papers/inference/99-other-inference-systems/2022-2201.12023-alpa-automating-inter-and-intra-operator-parallelism-for-distributed-deep-learning.md` |
| 100 | research | DOI:10.18653/v1/2025.acl-long.1211 | RefreshKV: Updating Small KV Cache During Long-form Generation | [primary](https://doi.org/10.18653/v1/2025.acl-long.1211) | `papers/inference/99-other-inference-systems/0000-a2b748353aae-refreshkv-updating-small-kv-cache-during-long-form-generation.md` |
| 101 | research | arXiv:2410.17375 | AMUSD: Asynchronous Multi-Device Speculative Decoding for LLM Acceleration | [primary](https://arxiv.org/abs/2410.17375) | `papers/inference/99-other-inference-systems/2024-2410.17375-amusd-asynchronous-multi-device-speculative-decoding-for-llm-acceleration.md` |
| 102 | research | arXiv:2110.14895 | Pipeline Parallelism for Inference on Heterogeneous Edge Computing | [primary](https://arxiv.org/abs/2110.14895) | `papers/inference/99-other-inference-systems/2021-2110.14895-pipeline-parallelism-for-inference-on-heterogeneous-edge-computing.md` |
| 103 | research | arXiv:2509.17396 | EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments | [primary](https://arxiv.org/abs/2509.17396) | `papers/inference/99-other-inference-systems/2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-resource-constrained-environments.md` |
| 104 | research | arXiv:2602.02579 | ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2602.02579) | `papers/inference/99-other-inference-systems/2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cache-reuse-in-retrieval-augmented-generation.md` |
| 105 | research | arXiv:2511.00606 | SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding | [primary](https://arxiv.org/abs/2511.00606) | `papers/inference/99-other-inference-systems/2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-decoding.md` |
| 106 | research | arXiv:2606.12370 | Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling | [primary](https://arxiv.org/abs/2606.12370) | `papers/inference/99-other-inference-systems/2026-2606.12370-breaking-entropy-bounds-accelerating-rl-training-via-mtp-with-rejection-sampling.md` |
| 107 | research | arXiv:2502.17421 | LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification | [primary](https://arxiv.org/abs/2502.17421) | `papers/inference/99-other-inference-systems/2025-2502.17421-longspec-long-context-lossless-speculative-decoding-with-efficient-drafting-and-verification.md` |
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
| 126 | research | arXiv:2407.05467 | The infrastructure powering IBM's Gen AI model development | [primary](https://arxiv.org/abs/2407.05467) | `papers/inference/99-other-inference-systems/2024-2407.05467-the-infrastructure-powering-ibm-s-gen-ai-model-development.md` |
| 127 | research | arXiv:2510.15312 | Accelerating Mobile Language Model via Speculative Decoding and NPU-Coordinated Execution | [primary](https://arxiv.org/abs/2510.15312) | `papers/inference/99-other-inference-systems/2025-2510.15312-accelerating-mobile-language-model-via-speculative-decoding-and-npu-coordinated-execution.md` |
| 128 | research | arXiv:2401.04658 | Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models | [primary](https://arxiv.org/abs/2401.04658) | `papers/inference/99-other-inference-systems/2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengths-in-large-language-models.md` |
| 129 | research | arXiv:2403.05676 | PipeRAG: Fast Retrieval-Augmented Generation via Algorithm-System Co-design | [primary](https://arxiv.org/abs/2403.05676) | `papers/inference/99-other-inference-systems/2024-2403.05676-piperag-fast-retrieval-augmented-generation-via-algorithm-system-co-design.md` |
| 130 | research | DOI:10.1145/3777466 | Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines | [primary](https://doi.org/10.1145/3777466) | `papers/inference/99-other-inference-systems/2025-704c3dbb57e7-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md` |
| 131 | research | arXiv:2409.01366 | CHESS: Optimizing LLM Inference via Channel-Wise Thresholding and Selective Sparsification | [primary](https://arxiv.org/abs/2409.01366) | `papers/inference/99-other-inference-systems/2024-2409.01366-chess-optimizing-llm-inference-via-channel-wise-thresholding-and-selective-sparsification.md` |
| 132 | research | arXiv:2502.10424 | QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache | [primary](https://arxiv.org/abs/2502.10424) | `papers/inference/99-other-inference-systems/2025-2502.10424-quantspec-self-speculative-decoding-with-hierarchical-quantized-kv-cache.md` |
| 133 | research | arXiv:2512.15176 | DEER: Draft with Diffusion, Verify with Autoregressive Models | [primary](https://arxiv.org/abs/2512.15176) | `papers/inference/99-other-inference-systems/2025-2512.15176-deer-draft-with-diffusion-verify-with-autoregressive-models.md` |
| 134 | research | DOI:10.1145/3642970.3655835 | Deferred Continuous Batching in Resource-Efficient Large Language Model Serving | [primary](https://doi.org/10.1145/3642970.3655835) | `papers/inference/99-other-inference-systems/2024-cd0254f5f44d-deferred-continuous-batching-in-resource-efficient-large-language-model-serving.md` |
| 135 | research | arXiv:2510.14557 | MX+: Pushing the Limits of Microscaling Formats for Efficient Large Language Model Serving | [primary](https://arxiv.org/abs/2510.14557) | `papers/inference/99-other-inference-systems/2025-2510.14557-mx-pushing-the-limits-of-microscaling-formats-for-efficient-large-language-model-serving.md` |
| 136 | research | arXiv:2606.13392 | MiniMax Sparse Attention | [primary](https://arxiv.org/abs/2606.13392) | `papers/inference/99-other-inference-systems/2026-2606.13392-minimax-sparse-attention.md` |
| 137 | research | DOI:10.1145/3725843.3756078 | LLM.265: Video Codecs are Secretly Tensor Codecs | [primary](https://doi.org/10.1145/3725843.3756078) | `papers/inference/99-other-inference-systems/2025-5a2b2924d4e3-llm-265-video-codecs-are-secretly-tensor-codecs.md` |
| 138 | research | arXiv:2502.18755 | M-ANT: Efficient Low-bit Group Quantization for LLMs via Mathematically Adaptive Numerical Type | [primary](https://arxiv.org/abs/2502.18755) | `papers/inference/99-other-inference-systems/2025-2502.18755-m-ant-efficient-low-bit-group-quantization-for-llms-via-mathematically-adaptive-numerical-type.md` |
| 139 | research | arXiv:2310.03003 | From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference | [primary](https://arxiv.org/abs/2310.03003) | `papers/inference/99-other-inference-systems/2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-model-inference.md` |
| 140 | research | arXiv:2309.16354 | Transformer-VQ: Linear-Time Transformers via Vector Quantization | [primary](https://arxiv.org/abs/2309.16354) | `papers/inference/99-other-inference-systems/2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md` |
| 141 | research | arXiv:2310.06178 | Look-Up mAI GeMM: Increasing AI GeMMs Performance by Nearly 2.5x via msGeMM | [primary](https://arxiv.org/abs/2310.06178) | `papers/inference/99-other-inference-systems/2023-2310.06178-look-up-mai-gemm-increasing-ai-gemms-performance-by-nearly-2-5x-via-msgemm.md` |
| 142 | research | arXiv:2305.05176 | FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance | [primary](https://arxiv.org/abs/2305.05176) | `papers/inference/99-other-inference-systems/2023-2305.05176-frugalgpt-how-to-use-large-language-models-while-reducing-cost-and-improving-performance.md` |
| 143 | research | arXiv:2609.36322 | Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression | [primary](https://arxiv.org/abs/2609.36322) | `papers/inference/99-other-inference-systems/2026-2609.36322-periodic-weak-spots-phase-sensitivity-from-chunked-kv-cache-compression.md` |
| 144 | research | arXiv:2609.33385 | OLED-MoE: Accelerating MoE-Based dLLM Inference via Inter-Iteration Locality-Aware Expert Offloading | [primary](https://arxiv.org/abs/2609.33385) | `papers/inference/99-other-inference-systems/2026-2609.33385-oled-moe-accelerating-moe-based-dllm-inference-via-inter-iteration-locality-aware-expert-offloading.md` |
| 145 | research | arXiv:2310.07096 | Sparse Universal Transformer | [primary](https://arxiv.org/abs/2310.07096) | `papers/inference/99-other-inference-systems/2023-2310.07096-sparse-universal-transformer.md` |
| 146 | research | arXiv:2404.19737 | Better & Faster Large Language Models via Multi-token Prediction | [primary](https://arxiv.org/abs/2404.19737) | `papers/inference/99-other-inference-systems/2024-2404.19737-better-faster-large-language-models-via-multi-token-prediction.md` |
| 147 | research | arXiv:2403.04643 | QAQ: Quality Adaptive Quantization for LLM KV Cache | [primary](https://arxiv.org/abs/2403.04643) | `papers/inference/99-other-inference-systems/2024-2403.04643-qaq-quality-adaptive-quantization-for-llm-kv-cache.md` |
| 148 | research | arXiv:2307.08621 | Retentive Network: A Successor to Transformer for Large Language Models | [primary](https://arxiv.org/abs/2307.08621) | `papers/inference/99-other-inference-systems/2023-2307.08621-retentive-network-a-successor-to-transformer-for-large-language-models.md` |
| 149 | research | arXiv:2411.16102 | BlendServe: Optimizing Offline Inference for Auto-regressive Large Models with Resource-aware Batching | [primary](https://arxiv.org/abs/2411.16102) | `papers/inference/99-other-inference-systems/2024-2411.16102-blendserve-optimizing-offline-inference-for-auto-regressive-large-models-with-resource-aware-batching.md` |
| 150 | research | arXiv:2510.06175 | VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization | [primary](https://arxiv.org/abs/2510.06175) | `papers/inference/99-other-inference-systems/2025-2510.06175-vecinfer-efficient-llm-inference-with-low-bit-kv-cache-via-outlier-suppressed-vector-quantization.md` |
| 151 | research | arXiv:2511.11733 | Speculative Decoding in Decentralized LLM Inference: Turning Communication Latency into Computation Throughput | [primary](https://arxiv.org/abs/2511.11733) | `papers/inference/99-other-inference-systems/2025-2511.11733-speculative-decoding-in-decentralized-llm-inference-turning-communication-latency-into-computation-throughput.md` |
| 152 | research | arXiv:2405.14852 | PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression | [primary](https://arxiv.org/abs/2405.14852) | `papers/inference/99-other-inference-systems/2024-2405.14852-pv-tuning-beyond-straight-through-estimation-for-extreme-llm-compression.md` |
| 153 | research | arXiv:2311.15436 | Learning to Skip for Language Modeling | [primary](https://arxiv.org/abs/2311.15436) | `papers/inference/99-other-inference-systems/2023-2311.15436-learning-to-skip-for-language-modeling.md` |
| 154 | research | arXiv:2604.04722 | Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs | [primary](https://arxiv.org/abs/2604.04722) | `papers/inference/99-other-inference-systems/2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-device-llms.md` |
| 155 | research | DOI:10.1145/3620665.3640366 | PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation | [primary](https://doi.org/10.1145/3620665.3640366) | `papers/inference/99-other-inference-systems/2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transformation-and-graph-compilation.md` |
| 156 | research | arXiv:2602.13836 | Speculative Decoding with a Speculative Vocabulary | [primary](https://arxiv.org/abs/2602.13836) | `papers/inference/99-other-inference-systems/2026-2602.13836-speculative-decoding-with-a-speculative-vocabulary.md` |
| 157 | research | arXiv:2401.06118 | Extreme Compression of Large Language Models via Additive Quantization | [primary](https://arxiv.org/abs/2401.06118) | `papers/inference/99-other-inference-systems/2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md` |
| 158 | research | DOI:10.18653/v1/2026.findings-acl.1655 | LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation | [primary](https://aclanthology.org/2026.findings-acl.1655/) | `papers/inference/99-other-inference-systems/2026-df65c3a3c97c-logitspec-accelerating-retrieval-based-speculative-decoding-via-next-next-token-speculation.md` |
| 159 | research | DOI:10.1145/3642970.3655844 | ALTO: An Efficient Network Orchestrator for Compound AI Systems | [primary](https://doi.org/10.1145/3642970.3655844) | `papers/inference/99-other-inference-systems/2024-01aa9dc12834-alto-an-efficient-network-orchestrator-for-compound-ai-systems.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5372** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | arXiv:2502.09992 |  |  | 21 | 04-moe-parallelism-communication, Other Inference Systems / Lossless Parallel Decoding, Speculative Decoding, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, diffusion language model inference / KV cache / training-free acceleration, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, diffusion-llm-inference / caching / low-precision, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, speculative decoding / parallel drafting / diffusion-inspired language modeling, speculative-decoding, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。, 投機的復号・ブロック拡散提案・検証器中間表現の再利用, 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2502.09992) |
| 2 | DOI:10.1145/3669940.3707267 |  |  | 13 | KV Cache Optimization / Compression, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Offload / Hierarchical Memory, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, hierarchical-memory-kv-offload-cpu-gpu-attention, moe-inference-expert-placement-caching, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://doi.org/10.1145/3669940.3707267) |
| 3 | OpenReview:QOXrVMiHGK |  |  | 12 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative Decoding / Parallel Inference Systems, speculative-decoding, speculative-decoding-moe, 投機的デコード／動的候補木／高同時実行LLMサービング | [source](https://openreview.net/forum?id=QOXrVMiHGK) |
| 4 | OpenReview:Byj72udxe |  |  | 11 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, Offload / Hierarchical Memory, Quantization × MoE × Offload, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization, dense-to-MoE conversion / conditional FFN computation / expert routing, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://openreview.net/forum?id=Byj72udxe) |
| 5 | arXiv:2304.01089 |  |  | 10 | Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 6 | DOI:10.48550/arxiv.2501.14743 |  |  | 10 | 11-llm-serving-scheduling-disaggregation, 12-moe-parallelism-communication, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2501.14743) |
| 7 | arXiv:2104.08691 |  |  | 9 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, many-adapter LLM serving / LoRA serving / inference scheduling, survey-long-context-serving, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2104.08691) |
| 8 | DOI:10.18653/v1/2024.emnlp-main.422 |  |  | 9 | 05-speculative-decoding-moe, LLM Serving / Scheduling / Disaggregation, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE, other-inference-systems, speculative-decoding, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://doi.org/10.18653/v1/2024.emnlp-main.422) |
| 9 | DOI:10.18653/v1/2024.emnlp-main.890 |  |  | 9 | Adaptive computation／cache-aware MoE, Edge／on-device MoE, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive-expert-computation-compression, moe-inference-expert-offloading, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://doi.org/10.18653/v1/2024.emnlp-main.890) |
| 10 | arXiv:2410.21276 |  |  | 9 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, fine-grained MoE / expert routing / test-time scaling / inference-time sampling, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, multi-tenant LLM serving / latency attribution / fractional GPU sharing, その他システム研究 | [source](https://arxiv.org/abs/2410.21276) |
| 11 | arXiv:2201.11903 |  |  | 8 | 13-sparse-attention, Adaptive Expert Computation / Compression, Conditional Computation, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, Offload / Hierarchical Memory, Speculative Decoding / Parallel Inference Systems, speculative decoding / edge-assisted serving / distributed inference / pipeline scheduling | [source](https://arxiv.org/abs/2201.11903) |
| 12 | arXiv:1808.08745 |  |  | 8 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 13 | arXiv:2501.12599 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, Conditional Computation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation, serving-scheduling, 推論ベンチマーク・推論大規模言語モデルのサービング評価, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.12599) |
| 14 | arXiv:2305.13048 |  |  | 8 | KV Cache Offload / Recomputation, kv-cache, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling, 推論エンジン／推論基盤, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2305.13048) |
| 15 | DOI:10.1147/sj.52.0078 |  |  | 8 | 14-agentic-inference-serving-runtime, KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, MoE expert offloading / predictive prefetch and cache management, Offload / Hierarchical Memory, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1147/sj.52.0078) |
| 16 | arXiv:1911.11641 |  |  | 8 | 16-weight-quantization-compression, adaptive-expert-computation-compression, kv-cache-memory, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-quantization-compression | [source](https://arxiv.org/abs/1911.11641) |
| 17 | DOI:10.1609/aaai.v34i05.6239 |  |  | 8 | Adaptive computation／cache-aware MoE, KV cache management benchmarking, MoE compression / training-free expert merging / multimodal MoE routing, adaptive-expert-computation-compression, early-exit-offloading-self-speculative-decoding | [source](https://doi.org/10.1609/aaai.v34i05.6239) |
| 18 | DOI:10.48550/arxiv.2412.00099 |  |  | 8 | hardware-accelerators, offload-hierarchical-memory, survey-moe-inference-optimization, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.48550/arxiv.2412.00099) |
| 19 | arXiv:1912.01703 |  |  | 7 | 05-speculative-decoding-moe, 13-sparse-attention, GPUカーネル融合／SwiGLU／LLM推論ランタイム, Offload / Hierarchical Memory, その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/1912.01703) |
| 20 | OpenReview:nZeVKeeFYf9 |  |  | 7 | 18-vla-inference-quantization-evaluation, KV cache sparsity / paged attention / query-aware selection / LLM serving, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, llm-serving-systems, その他システム研究 | [source](https://openreview.net/forum?id=nZeVKeeFYf9) |
| 21 | arXiv:2308.12966 |  |  | 7 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 22 | DOI:10.18653/v1/2020.coling-main.580 |  |  | 7 | 10-kv-キャッシュ-オフロード-recomputation, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, Prefill/Decode Disaggregation / Selective KV Transfer | [source](https://doi.org/10.18653/v1/2020.coling-main.580) |
| 23 | arXiv:2203.14685 |  |  | 7 | Adaptive Expert Computation / Compression, MoE推論・エキスパート配置・全対全通信スケジューリング・異種GPU, survey-moe-inference-optimization, その他システム研究 | [source](https://arxiv.org/abs/2203.14685) |
| 24 | arXiv:2502.16982 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2502.16982) |
| 25 | arXiv:1607.06450 |  |  | 6 | LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 26 | arXiv:2501.14249 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, LLM Serving / Scheduling / Disaggregation, Other Inference Systems / Lossless Parallel Decoding, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2501.14249) |
| 27 | OpenReview:v8L0pN6EOi |  |  | 6 | KV Cache Optimization / Compression, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, reasoning-model compression / post-training pruning / calibration-data selection / causal intervention, speculative-decoding, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://openreview.net/forum?id=v8L0pN6EOi) |
| 28 | arXiv:2309.04255 |  |  | 6 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 29 | DOI:10.1145/3768628 |  |  | 6 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 30 | arXiv:2405.14366 |  |  | 6 | KV Cache Offload / Retrieval / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation, other-inference-systems | [source](https://arxiv.org/abs/2405.14366) |
| 31 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 32 | DOI:10.18653/v1/p17-1099 |  |  | 6 | LLM serving / CPU-GPU heterogeneous inference / SLO-aware scheduling / KV-cache offloading, speculative-decoding, 投機的復号 / LLMサービング・ベンチマーク, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://doi.org/10.18653/v1/p17-1099) |
| 33 | OpenReview:RkRrPp7GKO |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=RkRrPp7GKO) |
| 34 | DOI:10.48550/arxiv.2402.08268 |  |  | 6 | 10-kv-キャッシュ-オフロード-recomputation, serving-scheduling | [source](https://doi.org/10.48550/arxiv.2402.08268) |
| 35 | OpenReview:poE54GOq2l |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=poE54GOq2l) |
| 36 | arXiv:2204.09179 |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 37 | arXiv:2504.21318 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 38 | DOI:10.1145/3676641.3716278 |  |  | 5 | 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 39 | OpenReview:7kQjbCQwtT |  |  | 5 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-inference-expert-offloading, moe-quantization-compression, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=7kQjbCQwtT) |
| 40 | arXiv:2209.11895 |  |  | 5 | KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/2209.11895) |
| 41 | DOI:10.1109/ispass48437.2020.00018 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass48437.2020.00018) |
| 42 | OpenReview:Bl8u7ZRlbM |  |  | 5 | 11-llm-serving-scheduling-disaggregation, KV cache reuse / context caching / multi-tenant LLM serving / selective recomputation, agent serving / KV-cache reuse / latent communication / DAG workflows, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://openreview.net/forum?id=Bl8u7ZRlbM) |
| 43 | arXiv:2311.13581 |  |  | 5 | LLM inference surveys、roofline performance analysis, survey-speculative-decoding, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2311.13581) |
| 44 | arXiv:2501.08313 |  |  | 5 | 13-sparse-attention, moe-parallelism-communication, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.08313) |
| 45 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 46 | OpenReview:tcbBPnfwxS |  |  | 5 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=tcbBPnfwxS) |
| 47 | DOI:10.18653/v1/n18-2097 |  |  | 5 | llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 48 | arXiv:1603.08983 |  |  | 4 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 49 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 50 | arXiv:2310.18813 |  |  | 4 | speculative-decoding, survey-speculative-decoding, 投機的デコード・バッチ推論, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2310.18813) |
| 51 | arXiv:2503.20314 |  |  | 4 | MoE inference / expert parallelism / expert replication / load balancing, MoE routing / expert offloading / temporal expert persistence, llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://arxiv.org/abs/2503.20314) |
| 52 | DOI:10.1145/3732941 |  |  | 4 | LLM Serving / Scheduling / Disaggregation, dynamic-pd-disaggregation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3732941) |
| 53 | DOI:10.48550/arxiv.2404.15159 |  |  | 4 | Adaptive Expert Computation / Compression, MoE-LoRA / パラメータ効率的微調整 / マージ可能アダプタ / ルータ不要自己ルーティング, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, survey-low-bit-llm | [source](https://doi.org/10.48550/arxiv.2404.15159) |
| 54 | OpenReview:L4uaAR4ArM |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, speculative-decoding | [source](https://openreview.net/forum?id=L4uaAR4ArM) |
| 55 | OpenReview:z5uVAKwmjf |  |  | 4 | 14-agentic-inference-serving-runtime, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, LLMサービング／自動スケーリング／広域ルーティング, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=z5uVAKwmjf) |
| 56 | DOI:10.1109/mm.2024.3375352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, Offload / Hierarchical Memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/mm.2024.3375352) |
| 57 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 58 | arXiv:2512.19849 |  |  | 4 | Speculative decoding × MoE, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2512.19849) |
| 59 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 60 | arXiv:2402.06082 |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 61 | arXiv:2506.06266 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2506.06266) |
| 62 | arXiv:2602.02276 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2602.02276) |
| 63 | DOI:10.1109/hpca53966.2022.00082 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, kv-cache-memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca53966.2022.00082) |
| 64 | DOI:10.1109/lca.2026.3705817 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3705817) |
| 65 | DOI:10.1109/sc41406.2024.00094 |  |  | 3 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1109/sc41406.2024.00094) |
| 66 | DOI:10.1145/3458864.3467882 |  |  | 3 | Edge／on-device MoE, LLMサービング・スケジューリング・分離実行, other-inference-systems | [source](https://doi.org/10.1145/3458864.3467882) |
| 67 | DOI:10.1145/3630106.3658542 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3630106.3658542) |
| 68 | DOI:10.1145/3725843.3756121 |  |  | 3 | PIM / Near-Data Acceleration, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756121) |
| 69 | DOI:10.1145/3779212.3790187 |  |  | 3 | MoE expert offloading / predictive prefetch and cache management, hierarchical-memory-kv-offload-cpu-gpu-attention, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.1145/3779212.3790187) |
| 70 | DOI:10.52202/075280-2279 |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, other-inference-systems | [source](https://doi.org/10.52202/075280-2279) |
| 71 | OpenReview:1YDeZU8Lt5 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=1YDeZU8Lt5) |
| 72 | OpenReview:CS2JWaziYr |  |  | 3 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=CS2JWaziYr) |
| 73 | OpenReview:rJl-b3RcF7 |  |  | 3 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=rJl-b3RcF7) |
| 74 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 75 | arXiv:2209.13258 |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 76 | arXiv:2502.02617 |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02617) |
| 77 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 78 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 79 | DOI:10.1145/3620665.3640383 |  |  | 3 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, serving-scheduling | [source](https://doi.org/10.1145/3620665.3640383) |
| 80 | DOI:10.1145/3779212.3790226 |  |  | 3 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3779212.3790226) |
| 81 | DOI:10.18653/v1/2021.naacl-main.365 |  |  | 3 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference | [source](https://doi.org/10.18653/v1/2021.naacl-main.365) |
| 82 | DOI:10.18653/v1/d19-1454 |  |  | 3 | Conditional Computation, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/d19-1454) |
| 83 | DOI:10.57967/hf/2497 |  |  | 3 | KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, adaptive-expert-computation-compression | [source](https://doi.org/10.57967/hf/2497) |
| 84 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 85 | OpenReview:MaYzugDmQV |  |  | 3 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 86 | OpenReview:rkgNKkHtvB |  |  | 3 | 10-kv-cache-offload-recomputation, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rkgNKkHtvB) |
| 87 | arXiv:2606.04101 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2606.04101) |
| 88 | DOI:10.18653/v1/p19-1102 |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference | [source](https://doi.org/10.18653/v1/p19-1102) |
| 89 | OpenReview:KG6aBfGi6e |  |  | 3 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=KG6aBfGi6e) |
| 90 | arXiv:1905.05702 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Sparse Attention | [source](https://arxiv.org/abs/1905.05702) |
| 91 | arXiv:2104.07012 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 92 | arXiv:2305.05252 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 93 | arXiv:2306.02561 |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 94 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 95 | arXiv:2307.08072 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 96 | arXiv:2308.07107 |  |  | 2 | KV cache compression / sparse attention / long-context inference, serving-scheduling | [source](https://arxiv.org/abs/2308.07107) |
| 97 | arXiv:2309.05463 |  |  | 2 | survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 98 | arXiv:2309.09558 |  |  | 2 | offload-hierarchical-memory, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://arxiv.org/abs/2309.09558) |
| 99 | arXiv:2309.11235 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2309.11235) |
| 100 | arXiv:2309.15531 |  |  | 2 | KV cache quantization / long-context inference / activation compression, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.15531) |
| 101 | arXiv:2310.02226 |  |  | 2 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 102 | arXiv:2310.08041 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2310.08041) |
| 103 | arXiv:2311.01635 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.01635) |
| 104 | arXiv:2311.10122 |  |  | 2 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference | [source](https://arxiv.org/abs/2311.10122) |
| 105 | arXiv:2311.17311 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 106 | arXiv:2312.03788 |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 107 | arXiv:2312.07987 |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 108 | arXiv:2312.14852 |  |  | 2 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 109 | arXiv:2401.03462 |  |  | 2 | 07-kv-キャッシュ-optimization-compression, KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2401.03462) |
| 110 | arXiv:2401.12522 |  |  | 2 | speculative-decoding, 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/2401.12522) |
| 111 | arXiv:2401.14112 |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 112 | arXiv:2402.02716 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2402.02716) |
| 113 | arXiv:2402.09025 |  |  | 2 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 114 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 115 | arXiv:2402.14762 |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 116 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 117 | arXiv:2403.05525 |  |  | 2 | Quantization × MoE × Offload, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 118 | arXiv:2403.09032 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 119 | arXiv:2403.14123 |  |  | 2 | moe-parallelism-communication, offload-hierarchical-memory | [source](https://arxiv.org/abs/2403.14123) |
| 120 | arXiv:2404.07972 |  |  | 2 | 14-agentic-inference-serving-runtime, KVキャッシュオフロード・再計算 | [source](https://arxiv.org/abs/2404.07972) |
| 121 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 122 | arXiv:2405.11530 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2405.11530) |
| 123 | arXiv:2405.21075 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention | [source](https://arxiv.org/abs/2405.21075) |
| 124 | arXiv:2406.03736 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2406.03736) |
| 125 | arXiv:2406.04594 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.04594) |
| 126 | arXiv:2406.11612 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2406.11612) |
| 127 | arXiv:2406.14963 |  |  | 2 | kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2406.14963) |
| 128 | arXiv:2406.18820 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18820) |
| 129 | arXiv:2407.04014 |  |  | 2 | llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 130 | arXiv:2407.09141 |  |  | 2 | 06-moe-quantization-compression, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.09141) |
| 131 | arXiv:2407.11239 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2407.11239) |
| 132 | arXiv:2407.17789 |  |  | 2 | 14-agentic-inference-serving-runtime, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2407.17789) |
| 133 | arXiv:2408.15881 |  |  | 2 | Speculative decoding × MoE, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2408.15881) |
| 134 | arXiv:2409.09071 |  |  | 2 | on-device LLM / heterogeneous inference / NPU offloading, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://arxiv.org/abs/2409.09071) |
| 135 | arXiv:2409.17422 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2409.17422) |
| 136 | arXiv:2410.00161 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.00161) |
| 137 | arXiv:2410.06511 |  |  | 2 | その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/2410.06511) |
| 138 | arXiv:2410.10989 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, その他システム研究 | [source](https://arxiv.org/abs/2410.10989) |
| 139 | arXiv:2410.14720 |  |  | 2 | MoE compression / expert pruning / neuron-level recombination / expert reconstruction, System-aware KV cache | [source](https://arxiv.org/abs/2410.14720) |
| 140 | arXiv:2410.20650 |  |  | 2 | kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2410.20650) |
| 141 | arXiv:2411.00918 |  |  | 2 | MoE圧縮 / expert merging / subspace alignment / SVD / adaptive clustering, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2411.00918) |
| 142 | arXiv:2411.04468 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2411.04468) |
| 143 | arXiv:2411.04996 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 144 | arXiv:2411.15100 |  |  | 2 | kv-cache-optimization-compression, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.15100) |
| 145 | arXiv:2412.03603 |  |  | 2 | diffusion language model inference / KV cache / training-free acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.03603) |
| 146 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 147 | arXiv:2412.16545 |  |  | 2 | 10-kv-cache-offload-recomputation, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2412.16545) |
| 148 | arXiv:2501.12370 |  |  | 2 | MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://arxiv.org/abs/2501.12370) |
| 149 | arXiv:2502.03461 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2502.03461) |
| 150 | arXiv:2502.07861 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.07861) |
| 151 | arXiv:2502.12444 |  |  | 2 | 10-kv-cache-offload-recomputation, CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/2502.12444) |
| 152 | arXiv:2502.17416 |  |  | 2 | Conditional Computation, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2502.17416) |
| 153 | arXiv:2503.07545 |  |  | 2 | LLM配信／KVキャッシュ制約／連続バッチ処理／待ち行列・力学系, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2503.07545) |
| 154 | arXiv:2503.09567 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2503.09567) |
| 155 | arXiv:2503.23100 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2503.23100) |
| 156 | arXiv:2504.04823 |  |  | 2 | kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2504.04823) |
| 157 | arXiv:2504.09014 |  |  | 2 | LLMサービング／スケジューリング／分離実行, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2504.09014) |
| 158 | arXiv:2504.12463 |  |  | 2 | Expert Prefetch, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2504.12463) |
| 159 | arXiv:2504.16112 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.16112) |
| 160 | arXiv:2504.17768 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.17768) |
| 161 | arXiv:2505.04921 |  |  | 2 | 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2505.04921) |
| 162 | arXiv:2505.07608 |  |  | 2 | kv-cache-optimization-compression, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2505.07608) |
| 163 | arXiv:2505.16552 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.16552) |
| 164 | arXiv:2506.01048 |  |  | 2 | llm-serving-scheduling-disaggregation, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://arxiv.org/abs/2506.01048) |
| 165 | arXiv:2506.14038 |  |  | 2 | moe-quantization-compression, その他システム研究 | [source](https://arxiv.org/abs/2506.14038) |
| 166 | arXiv:2507.07120 |  |  | 2 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2507.07120) |
| 167 | arXiv:2507.14111 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2507.14111) |
| 168 | arXiv:2507.19595 |  |  | 2 | KV Cache Optimization / Compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2507.19595) |
| 169 | arXiv:2508.06447 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, System-aware KV cache | [source](https://arxiv.org/abs/2508.06447) |
| 170 | arXiv:2508.08712 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08712) |
| 171 | arXiv:2508.16712 |  |  | 2 | LLM serving scheduling / chunked prefill / MoE inference, llm-serving-systems | [source](https://arxiv.org/abs/2508.16712) |
| 172 | arXiv:2509.01142 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2509.01142) |
| 173 | arXiv:2509.23202 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2509.23202) |
| 174 | arXiv:2510.00231 |  |  | 2 | KV cache compression / KV eviction / probabilistic inference / importance sampling, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2510.00231) |
| 175 | arXiv:2510.05373 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2510.05373) |
| 176 | arXiv:2510.12633 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.12633) |
| 177 | arXiv:2510.24273 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化 | [source](https://arxiv.org/abs/2510.24273) |
| 178 | arXiv:2511.16108 |  |  | 2 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2511.16108) |
| 179 | arXiv:2511.21689 |  |  | 2 | 14-agentic-inference-serving-runtime, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2511.21689) |
| 180 | arXiv:2512.04123 |  |  | 2 | Agentic Serving Benchmarking, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.04123) |
| 181 | arXiv:2512.12087 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.12087) |
| 182 | arXiv:2512.17077 |  |  | 2 | llm-serving-scheduling-disaggregation, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2512.17077) |
| 183 | arXiv:2601.06521 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2601.06521) |
| 184 | arXiv:2601.10088 |  |  | 2 | hardware-accelerators, 分離型LLMサービング／予測型スケジューリング／KVメモリ認識型配置 | [source](https://arxiv.org/abs/2601.10088) |
| 185 | arXiv:2601.21351 |  |  | 2 | MoE serving / Attention-FFN disaggregation / analytical provisioning / hardware-aware deployment search, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2601.21351) |
| 186 | arXiv:2602.08005 |  |  | 2 | System-aware KV cache, kv-cache-memory-management | [source](https://arxiv.org/abs/2602.08005) |
| 187 | arXiv:2603.18016 |  |  | 2 | 05-speculative-decoding-moe, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://arxiv.org/abs/2603.18016) |
| 188 | arXiv:2605.04595 |  |  | 2 | KVキャッシュ制約下のLLMサービング・スケジューリング, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2605.04595) |
| 189 | arXiv:2606.17034 |  |  | 2 | KVキャッシュ再利用・選択的再計算・RAGキャッシュ編集, inference/14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2606.17034) |
| 190 | DOI:10.1016/j.parco.2015.09.001 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, hardware-accelerators | [source](https://doi.org/10.1016/j.parco.2015.09.001) |
| 191 | DOI:10.1109/dac63849.2025.11132870 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, offload-hierarchical-memory | [source](https://doi.org/10.1109/dac63849.2025.11132870) |
| 192 | DOI:10.1109/hcs59251.2023.10254717 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/hcs59251.2023.10254717) |
| 193 | DOI:10.1109/hpca47549.2020.00030 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, kv-cache-memory | [source](https://doi.org/10.1109/hpca47549.2020.00030) |
| 194 | DOI:10.1109/iccv.2019.00038 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation | [source](https://doi.org/10.1109/iccv.2019.00038) |
| 195 | DOI:10.1109/isca45697.2020.00047 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/isca45697.2020.00047) |
| 196 | DOI:10.1109/ispass.2019.00042 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, 長文推論・KVキャッシュ先読み・要求パッキング・オンチップメモリ・HBM帯域最適化 | [source](https://doi.org/10.1109/ispass.2019.00042) |
| 197 | DOI:10.1109/lca.2025.3566692 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/lca.2025.3566692) |
| 198 | DOI:10.1109/micro61859.2024.00021 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/micro61859.2024.00021) |
| 199 | DOI:10.1109/mm.2024.3420728 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/mm.2024.3420728) |
| 200 | DOI:10.1109/tc.1985.6312218 |  |  | 2 | survey-speculative-decoding, 投機的復号 / 無損失復号高速化 | [source](https://doi.org/10.1109/tc.1985.6312218) |
| 201 | DOI:10.1115/1.3662552 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1115/1.3662552) |
| 202 | DOI:10.1145/1966445.1966473 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Expert Prefetch | [source](https://doi.org/10.1145/1966445.1966473) |
| 203 | DOI:10.1145/2517349.2522716 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/2517349.2522716) |
| 204 | DOI:10.1145/3297858.3304043 |  |  | 2 | hardware-accelerators, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3297858.3304043) |
| 205 | DOI:10.1145/3445814.3446714 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3445814.3446714) |
| 206 | DOI:10.1145/3492321.3519584 |  |  | 2 | MoE serving resilience / decoupled attention-expert serving / KV checkpointing, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3492321.3519584) |
| 207 | DOI:10.1145/3552326.3567508 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory | [source](https://doi.org/10.1145/3552326.3567508) |
| 208 | DOI:10.1145/3575693.3575754 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3575693.3575754) |
| 209 | DOI:10.1145/3591300 |  |  | 2 | GPUカーネル融合／SwiGLU／LLM推論ランタイム, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://doi.org/10.1145/3591300) |
| 210 | DOI:10.1145/3620665.3640410 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620665.3640410) |
| 211 | DOI:10.1145/3627703.3629578 |  |  | 2 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, serving-scheduling | [source](https://doi.org/10.1145/3627703.3629578) |
| 212 | DOI:10.1145/3650200.3656636 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, 分散推論／集団通信圧縮／量子化AllReduce／XLA・TPU | [source](https://doi.org/10.1145/3650200.3656636) |
| 213 | DOI:10.1145/3676641.3716252 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3676641.3716252) |
| 214 | DOI:10.1145/3710848.3710869 |  |  | 2 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 215 | DOI:10.1145/3731569.3764829 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3731569.3764829) |
| 216 | DOI:10.1145/3779212.3790188 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790188) |
| 217 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 218 | DOI:10.1609/aaai.v38i16.29720 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1609/aaai.v38i16.29720) |
| 219 | DOI:10.18653/v1/2022.findings-acl.189 |  |  | 2 | Conditional Computation, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/2022.findings-acl.189) |
| 220 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 221 | DOI:10.18653/v1/2025.acl-long.531 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/2025.acl-long.531) |
| 222 | DOI:10.48550/arxiv.2410.13056 |  |  | 2 | 16-weight-quantization-compression, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.48550/arxiv.2410.13056) |
| 223 | DOI:10.52202/068431-2198 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, early-exit-offloading-self-speculative-decoding | [source](https://doi.org/10.52202/068431-2198) |
| 224 | DOI:10.52202/079017-0040 |  |  | 2 | KV Cache Optimization / Compression, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://doi.org/10.52202/079017-0040) |
| 225 | DOI:10.52202/079017-3801 |  |  | 2 | KV Cache Optimization / Compression, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks | [source](https://doi.org/10.52202/079017-3801) |
| 226 | OpenReview:0LXotew9Du |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=0LXotew9Du) |
| 227 | OpenReview:c5BOcHM6J8 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=c5BOcHM6J8) |
| 228 | OpenReview:EKJhH5D5wA |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=EKJhH5D5wA) |
| 229 | OpenReview:H-VlwsYvVi |  |  | 2 | Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=H-VlwsYvVi) |
| 230 | OpenReview:ho7ZUS1z8A |  |  | 2 | MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / atomic expert pruning / second-order pruning | [source](https://openreview.net/forum?id=ho7ZUS1z8A) |
| 231 | OpenReview:KeHes2SVxs |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://openreview.net/forum?id=KeHes2SVxs) |
| 232 | OpenReview:qCaq3jGb0S |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=qCaq3jGb0S) |
| 233 | OpenReview:rAcgDBdKnP |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=rAcgDBdKnP) |
| 234 | OpenReview:Uh17FiwF4q |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising | [source](https://openreview.net/forum?id=Uh17FiwF4q) |
| 235 | OpenReview:yeeIGM3N6w |  |  | 2 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency | [source](https://openreview.net/forum?id=yeeIGM3N6w) |
| 236 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 237 | DOI:10.1109/infocom53939.2023.10228874 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1109/infocom53939.2023.10228874) |
| 238 | DOI:10.14778/3626292.3626303 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.14778/3626292.3626303) |
| 239 | DOI:10.18653/v1/2024.emnlp-main.897 |  |  | 2 | kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.897) |
| 240 | DOI:10.18653/v1/2025.acl-long.671 |  |  | 2 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing | [source](https://doi.org/10.18653/v1/2025.acl-long.671) |
| 241 | DOI:10.5281/zenodo.1234 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://doi.org/10.5281/zenodo.1234) |
| 242 | OpenReview:9k27IITeAZ |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=9k27IITeAZ) |
| 243 | OpenReview:PxoFut3dWW |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=PxoFut3dWW) |
| 244 | OpenReview:tcisuhGsQZ |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=tcisuhGsQZ) |
| 245 | OpenReview:ulCAPXYXfa |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer | [source](https://openreview.net/forum?id=ulCAPXYXfa) |
| 246 | DOI:10.48550/arxiv.2304.08354 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2304.08354) |
| 247 | OpenReview:2GmDdhBdDk |  |  | 2 |  | [source](https://openreview.net/forum?id=2GmDdhBdDk) |
| 248 | OpenReview:FJFVmeXusW |  |  | 2 |  | [source](https://openreview.net/forum?id=FJFVmeXusW) |
| 249 | OpenReview:QV79qiKAjD |  |  | 2 |  | [source](https://openreview.net/forum?id=QV79qiKAjD) |
| 250 | arXiv:1205.2618 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 251 | arXiv:1211.5590 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1211.5590) |
| 252 | arXiv:1305.0445 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1305.0445) |
| 253 | arXiv:1312.6211 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 254 | arXiv:1409.3215 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1409.3215) |
| 255 | arXiv:1504.00325 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1504.00325) |
| 256 | arXiv:1506.02640 |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1506.02640) |
| 257 | arXiv:1511.01837 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 258 | arXiv:1511.06939 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 259 | arXiv:1602.01528 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1602.01528) |
| 260 | arXiv:1602.02830 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1602.02830) |
| 261 | arXiv:1603.05118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1603.05118) |
| 262 | arXiv:1604.01696 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1604.01696) |
| 263 | arXiv:1609.05140 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1609.05140) |
| 264 | arXiv:1611.01540 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/1611.01540) |
| 265 | arXiv:1611.01704 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1611.01704) |
| 266 | arXiv:1701.03499 |  |  | 1 | NPU-PIM統合メモリ、近データ処理、LLM推論メモリ階層。NeuPIMs、IANUS、FACILの静的配置を動的実行へ拡張する。 | [source](https://arxiv.org/abs/1701.03499) |
| 267 | arXiv:1703.04247 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1703.04247) |
| 268 | arXiv:1703.09844 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1703.09844) |
| 269 | arXiv:1704.04861 |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1704.04861) |
| 270 | arXiv:1705.03122 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1705.03122) |
| 271 | arXiv:1705.07565 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1705.07565) |
| 272 | arXiv:1706.09254 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1706.09254) |
| 273 | arXiv:1707.08514 |  |  | 1 | 10-kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1707.08514) |
| 274 | arXiv:1708.06519 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1708.06519) |
| 275 | arXiv:1709.04571 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1709.04571) |
| 276 | arXiv:1711.00123 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1711.00123) |
| 277 | arXiv:1711.04291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1711.04291) |
| 278 | arXiv:1712.01208 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/1712.01208) |
| 279 | arXiv:1712.07040 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1712.07040) |
| 280 | arXiv:1802.04730 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/1802.04730) |
| 281 | arXiv:1802.06509 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1802.06509) |
| 282 | arXiv:1803.05407 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1803.05407) |
| 283 | arXiv:1805.06407 |  |  | 1 | CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/1805.06407) |
| 284 | arXiv:1806.08159 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1806.08159) |
| 285 | arXiv:1807.11205 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1807.11205) |
| 286 | arXiv:1808.09121 |  |  | 1 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling | [source](https://arxiv.org/abs/1808.09121) |
| 287 | arXiv:1809.04281 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1809.04281) |
| 288 | arXiv:1810.00602 |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/1810.00602) |
| 289 | arXiv:1810.05291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.05291) |
| 290 | arXiv:1811.01088 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1811.01088) |
| 291 | arXiv:1811.08886 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/1811.08886) |
| 292 | arXiv:1812.09764 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1812.09764) |
| 293 | arXiv:1902.03383 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/1902.03383) |
| 294 | arXiv:1902.09113 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1902.09113) |
| 295 | arXiv:1903.00089 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1903.00089) |
| 296 | arXiv:1903.04611 |  |  | 1 | 01-offload-hierarchical-memory | [source](https://arxiv.org/abs/1903.04611) |
| 297 | arXiv:1904.06376 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1904.06376) |
| 298 | arXiv:1904.10631 |  |  | 1 | long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/1904.10631) |
| 299 | arXiv:1905.07799 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 300 | arXiv:1906.04341 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 301 | arXiv:1906.10771 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1906.10771) |
| 302 | arXiv:1907.02684 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1907.02684) |
| 303 | arXiv:1908.09355 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1908.09355) |
| 304 | arXiv:1908.11645 |  |  | 1 | LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計 | [source](https://arxiv.org/abs/1908.11645) |
| 305 | arXiv:1909.06708 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/1909.06708) |
| 306 | arXiv:1909.12486 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1909.12486) |
| 307 | arXiv:1910.05316 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/1910.05316) |
| 308 | arXiv:1910.07475 |  |  | 1 | 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1910.07475) |
| 309 | arXiv:1911.03014 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/1911.03014) |
| 310 | arXiv:1911.08731 |  |  | 1 | moe-quantization-compression | [source](https://arxiv.org/abs/1911.08731) |
| 311 | arXiv:1912.12180 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1912.12180) |
| 312 | arXiv:2002.08307 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2002.08307) |
| 313 | arXiv:2002.11054 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2002.11054) |
| 314 | arXiv:2003.10555 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2003.10555) |
| 315 | arXiv:2004.03329 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2004.03329) |
| 316 | arXiv:2004.08994 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2004.08994) |
| 317 | arXiv:2004.11886 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2004.11886) |
| 318 | arXiv:2005.00770 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00770) |
| 319 | arXiv:2005.07647 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2005.07647) |
| 320 | arXiv:2006.00996 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2006.00996) |
| 321 | arXiv:2006.10901 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2006.10901) |
| 322 | arXiv:2007.01045 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2007.01045) |
| 323 | arXiv:2007.09818 |  |  | 1 | 06-moe-quantization-compression | [source](https://arxiv.org/abs/2007.09818) |
| 324 | arXiv:2008.00401 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2008.00401) |
| 325 | arXiv:2009.06489 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2009.06489) |
| 326 | arXiv:2009.08065 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2009.08065) |
| 327 | arXiv:2009.13239 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2009.13239) |
| 328 | arXiv:2010.02502 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2010.02502) |
| 329 | arXiv:2010.03633 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2010.03633) |
| 330 | arXiv:2010.07003 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2010.07003) |
| 331 | arXiv:2010.14701 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2010.14701) |
| 332 | arXiv:2011.04006 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2011.04006) |
| 333 | arXiv:2011.13456 |  |  | 1 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2011.13456) |
| 334 | arXiv:2012.12624 |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 335 | arXiv:2012.15828 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2012.15828) |
| 336 | arXiv:2101.09671 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2101.09671) |
| 337 | arXiv:2102.06621 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2102.06621) |
| 338 | arXiv:2102.08602 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2102.08602) |
| 339 | arXiv:2102.11972 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2102.11972) |
| 340 | arXiv:2103.03404 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2103.03404) |
| 341 | arXiv:2104.08771 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2104.08771) |
| 342 | arXiv:2105.03036 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.03036) |
| 343 | arXiv:2105.11618 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2105.11618) |
| 344 | arXiv:2105.14940 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.14940) |
| 345 | arXiv:2106.04489 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.04489) |
| 346 | arXiv:2106.07139 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2106.07139) |
| 347 | arXiv:2106.15339 |  |  | 1 | MoE推論／CPU-GPU協調オフロード／階層メモリ／性能モデル／高スループットバッチ推論 | [source](https://arxiv.org/abs/2106.15339) |
| 348 | arXiv:2107.10989 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2107.10989) |
| 349 | arXiv:2108.06098 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2108.06098) |
| 350 | arXiv:2109.02132 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2109.02132) |
| 351 | arXiv:2109.08406 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2109.08406) |
| 352 | arXiv:2109.11067 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2109.11067) |
| 353 | arXiv:2109.15082 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2109.15082) |
| 354 | arXiv:2110.07431 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2110.07431) |
| 355 | arXiv:2110.13283 |  |  | 1 | llm-serving-systems | [source](https://arxiv.org/abs/2110.13283) |
| 356 | arXiv:2111.00364 |  |  | 1 | hardware-accelerators | [source](https://arxiv.org/abs/2111.00364) |
| 357 | arXiv:2111.12293 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2111.12293) |
| 358 | arXiv:2112.03097 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2112.03097) |
| 359 | arXiv:2112.07916 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2112.07916) |
| 360 | arXiv:2112.14938 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2112.14938) |
| 361 | arXiv:2202.01279 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.01279) |
| 362 | arXiv:2202.05747 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2202.05747) |
| 363 | arXiv:2202.08904 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2202.08904) |
| 364 | arXiv:2203.00091 |  |  | 1 | 13-sparse-attention | [source](https://arxiv.org/abs/2203.00091) |
| 365 | arXiv:2203.05482 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.05482) |
| 366 | arXiv:2203.07814 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2203.07814) |
| 367 | arXiv:2203.14680 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2203.14680) |
| 368 | arXiv:2204.05999 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2204.05999) |
| 369 | arXiv:2204.07675 |  |  | 1 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2204.07675) |
| 370 | arXiv:2204.13807 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2204.13807) |
| 371 | arXiv:2205.05243 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2205.05243) |
| 372 | arXiv:2205.10569 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10569) |
| 373 | arXiv:2205.12411 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12411) |
| 374 | arXiv:2205.13792 |  |  | 1 | 推論中のKVQ再計算をストレージ読出しへ置換し、階層キャッシュと遅延制約付きスケジューラを組み合わせるLLM推論省エネルギー化。 | [source](https://arxiv.org/abs/2205.13792) |
| 375 | arXiv:2206.08474 |  |  | 1 | adaptive expert computation / expert pruning / depth-aware MoE compression | [source](https://arxiv.org/abs/2206.08474) |
| 376 | arXiv:2207.07061 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2207.07061) |
| 377 | arXiv:2207.12598 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2207.12598) |
| 378 | arXiv:2208.03299 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2208.03299) |
| 379 | arXiv:2208.09225 |  |  | 1 | 投機的デコード・バッチ推論 | [source](https://arxiv.org/abs/2208.09225) |
| 380 | arXiv:2209.07858 |  |  | 1 | Mixture-of-Experts inference / processing-in-memory / heterogeneous scheduling / expert placement | [source](https://arxiv.org/abs/2209.07858) |
| 381 | arXiv:2209.12356 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2209.12356) |
| 382 | arXiv:2210.02747 |  |  | 1 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference | [source](https://arxiv.org/abs/2210.02747) |
| 383 | arXiv:2210.03350 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2210.03350) |
| 384 | arXiv:2210.06726 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2210.06726) |
| 385 | arXiv:2210.09461 |  |  | 1 | on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2210.09461) |
| 386 | arXiv:2210.13438 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2210.13438) |
| 387 | arXiv:2210.17223 |  |  | 1 | moe-inference-expert-offloading | [source](https://arxiv.org/abs/2210.17223) |
| 388 | arXiv:2211.05719 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2211.05719) |
| 389 | arXiv:2211.07349 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.07349) |
| 390 | arXiv:2211.10435 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2211.10435) |
| 391 | arXiv:2211.15533 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2211.15533) |
| 392 | arXiv:2212.02855 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2212.02855) |
| 393 | arXiv:2212.04356 |  |  | 1 | エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2212.04356) |
| 394 | arXiv:2212.05339 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2212.05339) |
| 395 | arXiv:2212.10403 |  |  | 1 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2212.10403) |
| 396 | arXiv:2212.10511 |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2212.10511) |
| 397 | arXiv:2301.00407 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.00407) |
| 398 | arXiv:2301.05217 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2301.05217) |
| 399 | arXiv:2301.07069 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2301.07069) |
| 400 | arXiv:2301.11233 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2301.11233) |
| 401 | arXiv:2301.12900 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2301.12900) |
| 402 | arXiv:2302.02599 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.02599) |
| 403 | arXiv:2302.06590 |  |  | 1 | agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2302.06590) |
| 404 | arXiv:2302.09632 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.09632) |
| 405 | arXiv:2302.11750 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2302.11750) |
| 406 | arXiv:2302.12510 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.12510) |
| 407 | arXiv:2303.00980 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.00980) |
| 408 | arXiv:2303.04129 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.04129) |
| 409 | arXiv:2303.06153 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2303.06153) |
| 410 | arXiv:2303.08117 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2303.08117) |
| 411 | arXiv:2303.11366 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 412 | arXiv:2303.14524 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2303.14524) |
| 413 | arXiv:2303.16634 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2303.16634) |
| 414 | arXiv:2304.02643 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2304.02643) |
| 415 | arXiv:2304.03271 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/2304.03271) |
| 416 | arXiv:2304.04556 |  |  | 1 | KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://arxiv.org/abs/2304.04556) |
| 417 | arXiv:2304.08243 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2304.08243) |
| 418 | arXiv:2304.08485 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.08485) |
| 419 | arXiv:2304.10592 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.10592) |
| 420 | arXiv:2304.13712 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2304.13712) |
| 421 | arXiv:2305.00660 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.00660) |
| 422 | arXiv:2305.02633 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/2305.02633) |
| 423 | arXiv:2305.04701 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.04701) |
| 424 | arXiv:2305.07759 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2305.07759) |
| 425 | arXiv:2305.10250 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 426 | arXiv:2305.12870 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.12870) |
| 427 | arXiv:2305.13450 |  |  | 1 | dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2305.13450) |
| 428 | arXiv:2305.14387 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2305.14387) |
| 429 | arXiv:2305.14705 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2305.14705) |
| 430 | arXiv:2305.15066 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2305.15066) |
| 431 | arXiv:2305.16380 |  |  | 1 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化 | [source](https://arxiv.org/abs/2305.16380) |
| 432 | arXiv:2305.17144 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2305.17144) |
| 433 | arXiv:2305.19414 |  |  | 1 | MoEエキスパート予測・キャッシュ・プリフェッチ | [source](https://arxiv.org/abs/2305.19414) |
| 434 | arXiv:2306.02224 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2306.02224) |
| 435 | arXiv:2306.03805 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2306.03805) |
| 436 | arXiv:2306.05179 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2306.05179) |
| 437 | arXiv:2306.08162 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2306.08162) |
| 438 | arXiv:2306.12420 |  |  | 1 | multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2306.12420) |
| 439 | arXiv:2306.16636 |  |  | 1 | sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2306.16636) |
| 440 | arXiv:2307.02839 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2307.02839) |
| 441 | arXiv:2307.05300 |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2307.05300) |
| 442 | arXiv:2307.07735 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.07735) |
| 443 | arXiv:2307.12169 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12169) |
| 444 | arXiv:2307.15190 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2307.15190) |
| 445 | arXiv:2308.04035 |  |  | 1 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御 | [source](https://arxiv.org/abs/2308.04035) |
| 446 | arXiv:2308.11596 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2308.11596) |
| 447 | arXiv:2309.02784 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2309.02784) |
| 448 | arXiv:2309.14021 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.14021) |
| 449 | arXiv:2310.01542 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.01542) |
| 450 | arXiv:2310.04607 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.04607) |
| 451 | arXiv:2310.06003 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.06003) |
| 452 | arXiv:2310.08433 |  |  | 1 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2310.08433) |
| 453 | arXiv:2310.11454 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.11454) |
| 454 | arXiv:2310.13650 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.13650) |
| 455 | arXiv:2310.17157 |  |  | 1 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2310.17157) |
| 456 | arXiv:2310.19852 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.19852) |
| 457 | arXiv:2311.01544 |  |  | 1 | 06-moe-quantization-compression | [source](https://arxiv.org/abs/2311.01544) |
| 458 | arXiv:2311.02684 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2311.02684) |
| 459 | arXiv:2311.07226 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2311.07226) |
| 460 | arXiv:2311.08692 |  |  | 1 | speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2311.08692) |
| 461 | arXiv:2311.11696 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2311.11696) |
| 462 | arXiv:2311.13381 |  |  | 1 | survey-edge-llm | [source](https://arxiv.org/abs/2311.13381) |
| 463 | arXiv:2311.14652 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2311.14652) |
| 464 | arXiv:2312.02213 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2312.02213) |
| 465 | arXiv:2312.03414 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2312.03414) |
| 466 | arXiv:2312.04455 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2312.04455) |
| 467 | arXiv:2312.06674 |  |  | 1 | MoE serving / expert offloading / prefill-only serving | [source](https://arxiv.org/abs/2312.06674) |
| 468 | arXiv:2312.08583 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2312.08583) |
| 469 | arXiv:2312.11819 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11819) |
| 470 | arXiv:2312.13010 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2312.13010) |
| 471 | arXiv:2312.15166 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2312.15166) |
| 472 | arXiv:2401.00368 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2401.00368) |
| 473 | arXiv:2401.02330 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2401.02330) |
| 474 | arXiv:2401.04842 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.04842) |
| 475 | arXiv:2401.06201 |  |  | 1 | 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://arxiv.org/abs/2401.06201) |
| 476 | arXiv:2401.06915 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2401.06915) |
| 477 | arXiv:2401.07872 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2401.07872) |
| 478 | arXiv:2401.08329 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2401.08329) |
| 479 | arXiv:2401.09149 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2401.09149) |
| 480 | arXiv:2401.10491 |  |  | 1 | speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2401.10491) |
| 481 | arXiv:2401.12377 |  |  | 1 | LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2401.12377) |
| 482 | arXiv:2401.14268 |  |  | 1 | multi-SLO serving / speculative decoding / SLO-aware scheduling / hardware-aware token budgeting | [source](https://arxiv.org/abs/2401.14268) |
| 483 | arXiv:2401.17268 |  |  | 1 | distributed LLM inference / communication-aware serving | [source](https://arxiv.org/abs/2401.17268) |
| 484 | arXiv:2402.02446 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.02446) |
| 485 | arXiv:2402.03687 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2402.03687) |
| 486 | arXiv:2402.04497 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2402.04497) |
| 487 | arXiv:2402.04902 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.04902) |
| 488 | arXiv:2402.05964 |  |  | 1 | Prefill/Decode Disaggregation / Production LLM Serving | [source](https://arxiv.org/abs/2402.05964) |
| 489 | arXiv:2402.07927 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2402.07927) |
| 490 | arXiv:2402.09727 |  |  | 1 | KV cache reuse / agentic memory / dynamic retrieval / prefill acceleration | [source](https://arxiv.org/abs/2402.09727) |
| 491 | arXiv:2402.10631 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.10631) |
| 492 | arXiv:2402.11700 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2402.11700) |
| 493 | arXiv:2402.12280 |  |  | 1 | KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ | [source](https://arxiv.org/abs/2402.12280) |
| 494 | arXiv:2402.12991 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.12991) |
| 495 | arXiv:2402.13991 |  |  | 1 | KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference | [source](https://arxiv.org/abs/2402.13991) |
| 496 | arXiv:2402.16197 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2402.16197) |
| 497 | arXiv:2402.16843 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.16843) |
| 498 | arXiv:2402.17753 |  |  | 1 | inference/14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2402.17753) |
| 499 | arXiv:2402.19282 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2402.19282) |
| 500 | arXiv:2403.00376 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2403.00376) |

## Machine-readable

同じ割当は [worker-worklist-00.json](worker-worklist-00.json) にあります。

