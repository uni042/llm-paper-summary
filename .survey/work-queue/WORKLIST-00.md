# Scheduled worker :00 worklist

Worker: `scheduled-chat-00`  
Generated: `2026-10-03T08:03:14+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **574** / 未claim総数: **427** / このworker向け: **143**

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
| 98 | research | arXiv:2407.09486 | ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving | [primary](https://arxiv.org/abs/2407.09486) | `papers/inference/99-other-inference-systems/2024-2407.09486-enova-autoscaling-towards-cost-effective-and-stable-serverless-llm-serving.md` |
| 99 | research | arXiv:1911.02972 | Blockwise Self-Attention for Long Document Understanding | [primary](https://arxiv.org/abs/1911.02972) | `papers/inference/99-other-inference-systems/2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md` |
| 100 | research | DOI:10.1145/3600006.3613145 | GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints | [primary](https://doi.org/10.1145/3600006.3613145) | `papers/inference/99-other-inference-systems/0000-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-checkpoints.md` |
| 101 | research | arXiv:2110.14895 | Pipeline Parallelism for Inference on Heterogeneous Edge Computing | [primary](https://arxiv.org/abs/2110.14895) | `papers/inference/99-other-inference-systems/2021-2110.14895-pipeline-parallelism-for-inference-on-heterogeneous-edge-computing.md` |
| 102 | research | arXiv:2604.26256 | DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training | [primary](https://arxiv.org/abs/2604.26256) | `papers/inference/99-other-inference-systems/2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-model-training.md` |
| 103 | research | OpenReview:EQgEMAD4kv | CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences | [primary](https://openreview.net/forum?id=EQgEMAD4kv) | `papers/inference/99-other-inference-systems/0000-e6d13afe4c72-cake-cascading-and-adaptive-kv-cache-eviction-with-layer-preferences.md` |
| 104 | research | arXiv:2510.02758 | TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling | [primary](https://arxiv.org/abs/2510.02758) | `papers/inference/99-other-inference-systems/2025-2510.02758-tokenflow-responsive-llm-text-streaming-serving-under-request-burst-via-preemptive-scheduling.md` |
| 105 | research | arXiv:2606.13054 | TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization | [primary](https://arxiv.org/abs/2606.13054) | `papers/inference/99-other-inference-systems/2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post-training-quantization.md` |
| 106 | research | arXiv:2507.15465 | The New LLM Bottleneck: A Systems Perspective on Latent Attention and Mixture-of-Experts | [primary](https://arxiv.org/abs/2507.15465) | `papers/inference/99-other-inference-systems/2025-2507.15465-the-new-llm-bottleneck-a-systems-perspective-on-latent-attention-and-mixture-of-experts.md` |
| 107 | research | DOI:10.1145/3690624.3709196 | ResMoE: Space-efficient Compression of Mixture of Experts LLMs via Residual Restoration | [primary](https://doi.org/10.1145/3690624.3709196) | `papers/inference/99-other-inference-systems/0000-097fa558562e-resmoe-space-efficient-compression-of-mixture-of-experts-llms-via-residual-restoration.md` |
| 108 | research | arXiv:2508.02401 | CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation | [primary](https://arxiv.org/abs/2508.02401) | `papers/inference/99-other-inference-systems/2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-before-generation.md` |
| 109 | research | arXiv:2505.24298 | AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning | [primary](https://arxiv.org/abs/2505.24298) | `papers/inference/99-other-inference-systems/2025-2505.24298-areal-a-large-scale-asynchronous-reinforcement-learning-system-for-language-reasoning.md` |
| 110 | research | DOI:10.1145/3620666.3651380 | NeuPIMs: NPU-PIM Heterogeneous Acceleration for Batched LLM Inferencing | [primary](https://doi.org/10.1145/3620666.3651380) | `papers/inference/99-other-inference-systems/0000-53abd3a104f5-neupims-npu-pim-heterogeneous-acceleration-for-batched-llm-inferencing.md` |
| 111 | research | arXiv:1802.05799 | Horovod: fast and easy distributed deep learning in TensorFlow | [primary](https://arxiv.org/abs/1802.05799) | `papers/inference/99-other-inference-systems/2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md` |
| 112 | research | arXiv:2512.14080 | SonicMoE: Accelerating MoE with IO and Tile-aware Optimizations | [primary](https://arxiv.org/abs/2512.14080) | `papers/inference/99-other-inference-systems/2025-2512.14080-sonicmoe-accelerating-moe-with-io-and-tile-aware-optimizations.md` |
| 113 | research | DOI:10.1145/3676641.3716009 | PAPI: Exploiting Dynamic Parallelism in Large Language Model Decoding with a Processing-In-Memory-Enabled Computing System | [primary](https://doi.org/10.1145/3676641.3716009) | `papers/inference/99-other-inference-systems/0000-71a3fb195e7b-papi-exploiting-dynamic-parallelism-in-large-language-model-decoding-with-a-processing-in-memory-enabled-computing-syste.md` |
| 114 | research | arXiv:2307.06945 | In-context Autoencoder for Context Compression in a Large Language Model | [primary](https://arxiv.org/abs/2307.06945) | `papers/inference/99-other-inference-systems/2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md` |
| 115 | research | arXiv:2403.05821 | Optimizing LLM Queries in Relational Data Analytics Workloads | [primary](https://arxiv.org/abs/2403.05821) | `papers/inference/99-other-inference-systems/2024-2403.05821-optimizing-llm-queries-in-relational-data-analytics-workloads.md` |
| 116 | research | arXiv:2310.09832 | Merging Experts into One: Improving Computational Efficiency of Mixture of Experts | [primary](https://arxiv.org/abs/2310.09832) | `papers/inference/99-other-inference-systems/2023-2310.09832-merging-experts-into-one-improving-computational-efficiency-of-mixture-of-experts.md` |
| 117 | research | arXiv:2403.09919 | Recurrent Drafter for Fast Speculative Decoding in Large Language Models | [primary](https://arxiv.org/abs/2403.09919) | `papers/inference/99-other-inference-systems/2024-2403.09919-recurrent-drafter-for-fast-speculative-decoding-in-large-language-models.md` |
| 118 | research | arXiv:2510.14973 | Attention Is All You Need for KV Cache in Diffusion LLMs | [primary](https://arxiv.org/abs/2510.14973) | `papers/inference/99-other-inference-systems/2025-2510.14973-attention-is-all-you-need-for-kv-cache-in-diffusion-llms.md` |
| 119 | research | arXiv:2505.20225 | FLAME-MoE: A Transparent End-to-End Research Platform for Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2505.20225) | `papers/inference/99-other-inference-systems/2025-2505.20225-flame-moe-a-transparent-end-to-end-research-platform-for-mixture-of-experts-language-models.md` |
| 120 | research | arXiv:2410.14731 | MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection | [primary](https://arxiv.org/abs/2410.14731) | `papers/inference/99-other-inference-systems/2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md` |
| 121 | research | arXiv:2401.04658 | Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models | [primary](https://arxiv.org/abs/2401.04658) | `papers/inference/99-other-inference-systems/2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengths-in-large-language-models.md` |
| 122 | research | arXiv:2402.10517 | Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs | [primary](https://arxiv.org/abs/2402.10517) | `papers/inference/99-other-inference-systems/2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md` |
| 123 | research | arXiv:2609.38090 | Mira: Memory-Efficient MoE Inference Using Adaptive Caching and Predictive Expert Staging | [primary](https://arxiv.org/abs/2609.38090) | `papers/inference/99-other-inference-systems/2026-2609.38090-mira-memory-efficient-moe-inference-using-adaptive-caching-and-predictive-expert-staging.md` |
| 124 | research | arXiv:2412.03213 | ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression | [primary](https://arxiv.org/abs/2412.03213) | `papers/inference/99-other-inference-systems/2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-compression.md` |
| 125 | research | DOI:10.1145/3772052.3772264 | Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment | [primary](https://doi.org/10.1145/3772052.3772264) | `papers/inference/99-other-inference-systems/2025-6987e5a4e5ec-cauchy-a-cost-efficient-llm-serving-system-through-adaptive-heterogeneous-deployment.md` |
| 126 | research | arXiv:2603.13606 | NCCL EP: Towards a Unified Expert Parallel Communication API for NCCL | [primary](https://arxiv.org/abs/2603.13606) | `papers/inference/99-other-inference-systems/2026-2603.13606-nccl-ep-towards-a-unified-expert-parallel-communication-api-for-nccl.md` |
| 127 | research | arXiv:2506.09397 | SLED: A Speculative LLM Decoding Framework for Efficient Edge Serving | [primary](https://arxiv.org/abs/2506.09397) | `papers/inference/99-other-inference-systems/2025-2506.09397-sled-a-speculative-llm-decoding-framework-for-efficient-edge-serving.md` |
| 128 | research | arXiv:2310.03003 | From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference | [primary](https://arxiv.org/abs/2310.03003) | `papers/inference/99-other-inference-systems/2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-model-inference.md` |
| 129 | research | arXiv:2609.31415 | Evaluating the accuracy of KV cache reuse techniques | [primary](https://arxiv.org/abs/2609.31415) | `papers/inference/99-other-inference-systems/2026-2609.31415-evaluating-the-accuracy-of-kv-cache-reuse-techniques.md` |
| 130 | research | arXiv:2606.03819 | TreeFlash: Parallel AR-Approximation for Faster Speculative Decoding | [primary](https://arxiv.org/abs/2606.03819) | `papers/inference/99-other-inference-systems/2026-2606.03819-treeflash-parallel-ar-approximation-for-faster-speculative-decoding.md` |
| 131 | research | arXiv:2504.19720 | Taming the Titans: A Survey of Efficient LLM Inference Serving | [primary](https://arxiv.org/abs/2504.19720) | `papers/inference/99-other-inference-systems/2025-2504.19720-taming-the-titans-a-survey-of-efficient-llm-inference-serving.md` |
| 132 | research | arXiv:2505.24133 | R-KV: Redundancy-aware KV Cache Compression for Reasoning Models | [primary](https://arxiv.org/abs/2505.24133) | `papers/inference/99-other-inference-systems/2025-2505.24133-r-kv-redundancy-aware-kv-cache-compression-for-reasoning-models.md` |
| 133 | research | arXiv:2404.00242 | DeFT: Decoding with Flash Tree-attention for Efficient Tree-structured LLM Inference | [primary](https://arxiv.org/abs/2404.00242) | `papers/inference/99-other-inference-systems/2024-2404.00242-deft-decoding-with-flash-tree-attention-for-efficient-tree-structured-llm-inference.md` |
| 134 | research | arXiv:2604.04722 | Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs | [primary](https://arxiv.org/abs/2604.04722) | `papers/inference/99-other-inference-systems/2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-device-llms.md` |
| 135 | research | arXiv:2603.24517 | AVO: Agentic Variation Operators for Autonomous Evolutionary Search | [primary](https://arxiv.org/abs/2603.24517) | `papers/inference/99-other-inference-systems/2026-2603.24517-avo-agentic-variation-operators-for-autonomous-evolutionary-search.md` |
| 136 | research | DOI:10.1145/3552326.3587438 | Tabi: An Efficient Multi-Level Inference System for Large Language Models | [primary](https://doi.org/10.1145/3552326.3587438) | `papers/inference/99-other-inference-systems/2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md` |
| 137 | research | arXiv:2403.01241 | IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact | [primary](https://arxiv.org/abs/2403.01241) | `papers/inference/99-other-inference-systems/2024-2403.01241-intactkv-improving-large-language-model-quantization-by-keeping-pivot-tokens-intact.md` |
| 138 | research | arXiv:2401.08383 | Exploiting Inter-Layer Expert Affinity for Accelerating Mixture-of-Experts Model Inference | [primary](https://arxiv.org/abs/2401.08383) | `papers/inference/99-other-inference-systems/2024-2401.08383-exploiting-inter-layer-expert-affinity-for-accelerating-mixture-of-experts-model-inference.md` |
| 139 | research | arXiv:2402.04902 | L4Q: Parameter Efficient Quantization-Aware Fine-Tuning on Large Language Models | [primary](https://arxiv.org/abs/2402.04902) | `papers/inference/99-other-inference-systems/2024-2402.04902-l4q-parameter-efficient-quantization-aware-fine-tuning-on-large-language-models.md` |
| 140 | research | arXiv:2401.06761 | APAR: LLMs Can Do Auto-Parallel Auto-Regressive Decoding | [primary](https://arxiv.org/abs/2401.06761) | `papers/inference/99-other-inference-systems/2024-2401.06761-apar-llms-can-do-auto-parallel-auto-regressive-decoding.md` |
| 141 | research | arXiv:2402.11700 | Why Lift so Heavy? Slimming Large Language Models by Cutting Off the Layers | [primary](https://arxiv.org/abs/2402.11700) | `papers/inference/99-other-inference-systems/2024-2402.11700-why-lift-so-heavy-slimming-large-language-models-by-cutting-off-the-layers.md` |
| 142 | research | arXiv:2402.11960 | DB-LLM: Accurate Dual-Binarization for Efficient LLMs | [primary](https://arxiv.org/abs/2402.11960) | `papers/inference/99-other-inference-systems/2024-2402.11960-db-llm-accurate-dual-binarization-for-efficient-llms.md` |
| 143 | research | arXiv:2402.10076 | QUICK: Quantization-aware Interleaving and Conflict-free Kernel for efficient LLM inference | [primary](https://arxiv.org/abs/2402.10076) | `papers/inference/99-other-inference-systems/2024-2402.10076-quick-quantization-aware-interleaving-and-conflict-free-kernel-for-efficient-llm-inference.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5776** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | arXiv:2502.09992 |  |  | 25 | 04-moe-parallelism-communication, Other Inference Systems / Lossless Parallel Decoding, Speculative Decoding, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, diffusion language model inference / KV cache / training-free acceleration, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, diffusion-llm-inference / caching / low-precision, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, speculative decoding / parallel drafting / diffusion-inspired language modeling, speculative-decoding, speculative-parallel-decoding, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。, 投機的復号・ブロック拡散提案・検証器中間表現の再利用, 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2502.09992) |
| 2 | DOI:10.1145/3694715.3695948 |  |  | 15 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 3 | arXiv:2309.00071 |  |  | 13 | 07-kv-cache-optimization-compression, 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Adaptive computation／cache-aware MoE, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, inference-systems, kv-cache-offload-recomputation, moe | [source](https://arxiv.org/abs/2309.00071) |
| 4 | arXiv:1910.01108 |  |  | 12 | LLM Serving / Scheduling / Disaggregation, LLMサービング／予測型スケジューリング, Speculative Decoding, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 投機的デコード / 分布保存型デコード高速化, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1910.01108) |
| 5 | arXiv:2406.12793 |  |  | 12 | 07-kv-cache-optimization-compression, Edge / On-device LLM Systems, KV cache compression / sparse attention / long-context inference, KVキャッシュ退避／長文推論／KV選択／KV量子化, llm-serving-scheduling-disaggregation, その他システム研究 | [source](https://arxiv.org/abs/2406.12793) |
| 6 | arXiv:2309.04255 |  |  | 11 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, Speculative Decoding, edge-on-device-llm-systems, inference-systems, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 7 | OpenReview:Byj72udxe |  |  | 11 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, Offload / Hierarchical Memory, Quantization × MoE × Offload, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization, dense-to-MoE conversion / conditional FFN computation / expert routing, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://openreview.net/forum?id=Byj72udxe) |
| 8 | arXiv:2506.12708 |  |  | 11 | 12-moe-parallelism-communication, KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, MoE serving / attention-MoE disaggregation / asynchronous inference, chunked-prefill scheduling / fairness / latency control, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2506.12708) |
| 9 | arXiv:1808.08745 |  |  | 10 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 10 | DOI:10.48550/arxiv.2501.14743 |  |  | 10 | 11-llm-serving-scheduling-disaggregation, 12-moe-parallelism-communication, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2501.14743) |
| 11 | DOI:10.1609/aaai.v34i05.6239 |  |  | 10 | Adaptive computation／cache-aware MoE, KV cache management benchmarking, MoE compression / training-free expert merging / multimodal MoE routing, adaptive-expert-computation-compression, early-exit-offloading-self-speculative-decoding, inference-systems | [source](https://doi.org/10.1609/aaai.v34i05.6239) |
| 12 | arXiv:1809.09600 |  |  | 10 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, inference-systems, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 13 | arXiv:2308.00352 |  |  | 9 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, survey-long-context-serving, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://arxiv.org/abs/2308.00352) |
| 14 | DOI:10.18653/v1/2024.acl-long.623 |  |  | 9 | 02-hardware-accelerators, 14-agentic-inference-serving-runtime, KV Cache Offload / Recomputation, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Offload / Hierarchical Memory, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, llm-serving-scheduling-disaggregation, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.18653/v1/2024.acl-long.623) |
| 15 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 16 | arXiv:2401.15947 |  |  | 9 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis, MoE expert pruning / expert clustering / task-specific model compression, Quantization × MoE × Offload, オフロード／階層メモリ, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2401.15947) |
| 17 | DOI:10.1145/3394486.3406703 |  |  | 9 | GPU collective communication / communication compression / LLM serving disaggregation, KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems, kernel-runtime-compilation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3394486.3406703) |
| 18 | arXiv:2201.11903 |  |  | 8 | 13-sparse-attention, Adaptive Expert Computation / Compression, Conditional Computation, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, Offload / Hierarchical Memory, Speculative Decoding / Parallel Inference Systems, speculative decoding / edge-assisted serving / distributed inference / pipeline scheduling | [source](https://arxiv.org/abs/2201.11903) |
| 19 | OpenReview:Ti67584b98 |  |  | 8 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Other Inference Systems / Lossless Parallel Decoding, Speculative decoding × MoE, kv-cache-optimization-compression, sparse attention / learned context ranking / long-context LLM inference, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://openreview.net/forum?id=Ti67584b98) |
| 20 | arXiv:2512.20856 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, PIM / Near-Data Acceleration, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2512.20856) |
| 21 | DOI:10.5281/zenodo.10256836 |  |  | 8 | Adaptive Expert Computation / Compression, Conditional Computation, Expert Prefetch, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation, 投機復号・自己投機・ループ型Transformer・推論パイプライン, 投機的復号・Orthrus・推論再現性・数値精度 | [source](https://doi.org/10.5281/zenodo.10256836) |
| 22 | arXiv:2405.14366 |  |  | 8 | KV Cache Offload / Retrieval / Compression, KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation, other-inference-systems | [source](https://arxiv.org/abs/2405.14366) |
| 23 | DOI:10.18653/v1/p17-1099 |  |  | 8 | LLM serving / CPU-GPU heterogeneous inference / SLO-aware scheduling / KV-cache offloading, speculative-decoding, 投機的復号 / LLMサービング・ベンチマーク, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://doi.org/10.18653/v1/p17-1099) |
| 24 | arXiv:2502.02737 |  |  | 7 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, speculative-parallel-decoding, 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2502.02737) |
| 25 | arXiv:2101.00190 |  |  | 7 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2101.00190) |
| 26 | arXiv:2408.03326 |  |  | 7 | kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, low-bit VLM inference / microscaling / hardware-software co-design, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2408.03326) |
| 27 | DOI:10.5281/zenodo.5371628 |  |  | 7 | KV Cache Optimization / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.5281/zenodo.5371628) |
| 28 | arXiv:2203.14685 |  |  | 7 | Adaptive Expert Computation / Compression, MoE推論・エキスパート配置・全対全通信スケジューリング・異種GPU, survey-moe-inference-optimization, その他システム研究 | [source](https://arxiv.org/abs/2203.14685) |
| 29 | DOI:10.18653/v1/n18-2097 |  |  | 7 | 08-edge-on-device-llm-systems, inference-systems, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 30 | arXiv:2509.16941 |  |  | 7 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2509.16941) |
| 31 | arXiv:2402.14034 |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 32 | arXiv:2503.12491 |  |  | 6 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KV Cache Optimization / Compression, KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2503.12491) |
| 33 | OpenReview:v8L0pN6EOi |  |  | 6 | KV Cache Optimization / Compression, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, reasoning-model compression / post-training pruning / calibration-data selection / causal intervention, speculative-decoding, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://openreview.net/forum?id=v8L0pN6EOi) |
| 34 | arXiv:2304.09145 |  |  | 6 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 35 | DOI:10.1145/3768628 |  |  | 6 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 36 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 37 | OpenReview:Bkg6RiCqY7 |  |  | 6 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 38 | OpenReview:uccHPGDlao |  |  | 6 | 05-speculative-decoding-moe, Speculative decoding × MoE, inference-systems, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 39 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 6 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 40 | arXiv:2504.09285 |  |  | 6 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.09285) |
| 41 | OpenReview:poE54GOq2l |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=poE54GOq2l) |
| 42 | arXiv:2001.09977 |  |  | 5 | LLM Serving / Scheduling / Disaggregation, cross-layer LLM serving / SLO-aware scheduling / predictive routing / heterogeneous inference, serving-scheduling, speculative decoding / LLM serving / adaptive scheduling, その他システム研究 | [source](https://arxiv.org/abs/2001.09977) |
| 43 | arXiv:2504.21318 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 44 | DOI:10.1145/3695053.3731008 |  |  | 5 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 45 | arXiv:1603.08983 |  |  | 5 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 46 | arXiv:2108.12409 |  |  | 5 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLM inference surveys、roofline performance analysis, cpu-offload, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2108.12409) |
| 47 | DOI:10.1109/ispass48437.2020.00018 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass48437.2020.00018) |
| 48 | OpenReview:Bl8u7ZRlbM |  |  | 5 | 11-llm-serving-scheduling-disaggregation, KV cache reuse / context caching / multi-tenant LLM serving / selective recomputation, agent serving / KV-cache reuse / latent communication / DAG workflows, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://openreview.net/forum?id=Bl8u7ZRlbM) |
| 49 | arXiv:1511.06297 |  |  | 5 | Conditional Computation, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, inference-systems | [source](https://arxiv.org/abs/1511.06297) |
| 50 | arXiv:2403.12031 |  |  | 5 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 51 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 52 | DOI:10.1145/3725843.3756062 |  |  | 5 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3725843.3756062) |
| 53 | DOI:10.48550/arxiv.2412.18910 |  |  | 5 | 05-speculative-decoding-moe, inference-systems | [source](https://doi.org/10.48550/arxiv.2412.18910) |
| 54 | arXiv:2402.02244 |  |  | 4 | KV Cache Compression / Long Context, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 55 | arXiv:2503.20314 |  |  | 4 | MoE inference / expert parallelism / expert replication / load balancing, MoE routing / expert offloading / temporal expert persistence, llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://arxiv.org/abs/2503.20314) |
| 56 | DOI:10.1145/3503222.3507778 |  |  | 4 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.1145/3503222.3507778) |
| 57 | DOI:10.18653/v1/2025.acl-long.1126 |  |  | 4 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics, dynamic-pd-disaggregation, kv-cache-offload-recomputation | [source](https://doi.org/10.18653/v1/2025.acl-long.1126) |
| 58 | OpenReview:1qvx610Cu7 |  |  | 4 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, inference-systems, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 59 | OpenReview:stXtBqyTWX |  |  | 4 | Speculative decoding × MoE, activation-aware expert placement and multi-node MoE inference, kernel-runtime-compilation, moe-inference-expert-offloading | [source](https://openreview.net/forum?id=stXtBqyTWX) |
| 60 | arXiv:2203.08913 |  |  | 4 | LLM inference surveys、roofline performance analysis, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 61 | arXiv:2507.11851 |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2507.11851) |
| 62 | DOI:10.18653/v1/2021.naacl-main.365 |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems | [source](https://doi.org/10.18653/v1/2021.naacl-main.365) |
| 63 | OpenReview:cSimKw5p6R |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, agentic workflow serving / workflow physical planning / adaptive serving, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://openreview.net/forum?id=cSimKw5p6R) |
| 64 | OpenReview:TrjbxzRcnf- |  |  | 4 | KVキャッシュ・注意アーキテクチャ, KVキャッシュ再利用／圧縮／ネットワーク転送, other-inference-systems | [source](https://openreview.net/forum?id=TrjbxzRcnf-) |
| 65 | arXiv:2507.01449 |  |  | 4 | inference-systems, 投機的デコード／MoE | [source](https://arxiv.org/abs/2507.01449) |
| 66 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 67 | OpenReview:pPjZIOuQuF |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, 13-sparse-attention | [source](https://openreview.net/forum?id=pPjZIOuQuF) |
| 68 | arXiv:2212.08153 |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2212.08153) |
| 69 | arXiv:2312.04916 |  |  | 3 | early-exit-offloading-self-speculative-decoding, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2312.04916) |
| 70 | arXiv:2402.01680 |  |  | 3 | llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 71 | arXiv:2405.03133 |  |  | 3 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, inference-systems, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.03133) |
| 72 | arXiv:2409.06857 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, edge-on-device-llm-systems, offload-hierarchical-memory | [source](https://arxiv.org/abs/2409.06857) |
| 73 | arXiv:2411.02335 |  |  | 3 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, adaptive expert computation / compression; end-side sparse MoE, inference-systems | [source](https://arxiv.org/abs/2411.02335) |
| 74 | arXiv:2501.19309 |  |  | 3 | federated inference / speculative decoding / communication-efficient LLM inference, inference-systems, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2501.19309) |
| 75 | arXiv:2503.08311 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2503.08311) |
| 76 | arXiv:2511.00739 |  |  | 3 | LLM Serving / Scheduling / Disaggregation, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2511.00739) |
| 77 | DOI:10.1007/s11432-024-4235-6 |  |  | 3 | MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / null experts / data sparsity / multimodal MoE, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1007/s11432-024-4235-6) |
| 78 | DOI:10.1109/lca.2023.3333759 |  |  | 3 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, low-bit VLM inference / microscaling / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/lca.2023.3333759) |
| 79 | DOI:10.1109/micro56248.2022.00051 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, kv-cache-memory | [source](https://doi.org/10.1109/micro56248.2022.00051) |
| 80 | DOI:10.1145/1534530.1534544 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, offload-hierarchical-memory, オフロード／階層メモリ | [source](https://doi.org/10.1145/1534530.1534544) |
| 81 | DOI:10.1145/3620666.3651379 |  |  | 3 | kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 82 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 83 | DOI:10.1145/3731569.3764813 |  |  | 3 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764813) |
| 84 | DOI:10.52202/075280-2279 |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, other-inference-systems | [source](https://doi.org/10.52202/075280-2279) |
| 85 | OpenReview:5Qe7AGO3Eq |  |  | 3 | 17-pim-near-data-acceleration, kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=5Qe7AGO3Eq) |
| 86 | OpenReview:hmOwOZWzYE |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=hmOwOZWzYE) |
| 87 | OpenReview:tO3ASKZlok |  |  | 3 | 07-kv-cache-optimization-compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=tO3ASKZlok) |
| 88 | OpenReview:z3JZzu9EA3 |  |  | 3 | KV Cache Optimization / Compression, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=z3JZzu9EA3) |
| 89 | arXiv:2209.13258 |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 90 | arXiv:2304.12244 |  |  | 3 | inference-systems, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 91 | arXiv:2309.05463 |  |  | 3 | survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 92 | arXiv:2311.05232 |  |  | 3 | LLM inference surveys、roofline performance analysis, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2311.05232) |
| 93 | arXiv:2402.09025 |  |  | 3 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 94 | arXiv:2406.20094 |  |  | 3 | adaptive-expert-computation-compression, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2406.20094) |
| 95 | arXiv:2408.15881 |  |  | 3 | Speculative decoding × MoE, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2408.15881) |
| 96 | arXiv:2412.06769 |  |  | 3 | 99-other-inference-systems, Conditional Computation | [source](https://arxiv.org/abs/2412.06769) |
| 97 | arXiv:2502.17419 |  |  | 3 | Conditional Computation, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2502.17419) |
| 98 | arXiv:2510.01290 |  |  | 3 | inference/07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2510.01290) |
| 99 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 100 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 101 | DOI:10.1145/3581784.3607062 |  |  | 3 | Sparse Attention, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1145/3581784.3607062) |
| 102 | DOI:10.1145/3636534.3649379 |  |  | 3 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3636534.3649379) |
| 103 | DOI:10.1145/3779212.3790226 |  |  | 3 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3779212.3790226) |
| 104 | DOI:10.18653/v1/2024.acl-long.814 |  |  | 3 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.814) |
| 105 | DOI:10.18653/v1/w17-4413 |  |  | 3 | Adaptive computation／cache-aware MoE, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/w17-4413) |
| 106 | OpenReview:ayi7qezU87 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://openreview.net/forum?id=ayi7qezU87) |
| 107 | OpenReview:LKEJPySnlt |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=LKEJPySnlt) |
| 108 | OpenReview:uBaFH7aQnC |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=uBaFH7aQnC) |
| 109 | arXiv:2405.10637 |  |  | 3 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2405.10637) |
| 110 | arXiv:2506.05176 |  |  | 3 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2506.05176) |
| 111 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 112 | OpenReview:dHng2O0Jjr |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving | [source](https://openreview.net/forum?id=dHng2O0Jjr) |
| 113 | DOI:10.18653/v1/p19-1580 |  |  | 3 |  | [source](https://doi.org/10.18653/v1/p19-1580) |
| 114 | arXiv:1311.2540 |  |  | 2 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 115 | arXiv:1802.06901 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1802.06901) |
| 116 | arXiv:1905.05702 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Sparse Attention | [source](https://arxiv.org/abs/1905.05702) |
| 117 | arXiv:1909.06708 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1909.06708) |
| 118 | arXiv:2004.11886 |  |  | 2 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2004.11886) |
| 119 | arXiv:2103.02143 |  |  | 2 | CPU長文推論・近似注意, inference-systems | [source](https://arxiv.org/abs/2103.02143) |
| 120 | arXiv:2204.05999 |  |  | 2 | inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2204.05999) |
| 121 | arXiv:2302.10866 |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2302.10866) |
| 122 | arXiv:2305.07759 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.07759) |
| 123 | arXiv:2306.04050 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 124 | arXiv:2307.04964 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2307.04964) |
| 125 | arXiv:2308.06093 |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 126 | arXiv:2309.05516 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 127 | arXiv:2309.10400 |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 128 | arXiv:2309.13879 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, other-inference-systems | [source](https://arxiv.org/abs/2309.13879) |
| 129 | arXiv:2309.16739 |  |  | 2 | inference-systems, multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2309.16739) |
| 130 | arXiv:2310.03744 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 131 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 132 | arXiv:2311.08981 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, survey-speculative-decoding | [source](https://arxiv.org/abs/2311.08981) |
| 133 | arXiv:2311.13171 |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 134 | arXiv:2312.00678 |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 135 | arXiv:2312.07987 |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 136 | arXiv:2312.16862 |  |  | 2 | LLM inference surveys、roofline performance analysis, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2312.16862) |
| 137 | arXiv:2401.07339 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.07339) |
| 138 | arXiv:2401.14112 |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 139 | arXiv:2402.03216 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 140 | arXiv:2402.12289 |  |  | 2 | Expert Prefetch, survey-edge-llm | [source](https://arxiv.org/abs/2402.12289) |
| 141 | arXiv:2402.14762 |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 142 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 143 | arXiv:2403.05525 |  |  | 2 | Quantization × MoE × Offload, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 144 | arXiv:2403.09032 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 145 | arXiv:2404.03605 |  |  | 2 | Conditional Computation, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2404.03605) |
| 146 | arXiv:2404.07972 |  |  | 2 | 14-agentic-inference-serving-runtime, KVキャッシュオフロード・再計算 | [source](https://arxiv.org/abs/2404.07972) |
| 147 | arXiv:2404.13628 |  |  | 2 | 02-adaptive-expert-computation-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2404.13628) |
| 148 | arXiv:2405.11530 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2405.11530) |
| 149 | arXiv:2405.21075 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention | [source](https://arxiv.org/abs/2405.21075) |
| 150 | arXiv:2406.04127 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2406.04127) |
| 151 | arXiv:2406.07394 |  |  | 2 | Edge／on-device MoE, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.07394) |
| 152 | arXiv:2406.11931 |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.11931) |
| 153 | arXiv:2406.18629 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2406.18629) |
| 154 | arXiv:2407.04014 |  |  | 2 | llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 155 | arXiv:2407.09141 |  |  | 2 | 06-moe-quantization-compression, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.09141) |
| 156 | arXiv:2407.11239 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2407.11239) |
| 157 | arXiv:2407.17789 |  |  | 2 | 14-agentic-inference-serving-runtime, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2407.17789) |
| 158 | arXiv:2409.17066 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline | [source](https://arxiv.org/abs/2409.17066) |
| 159 | arXiv:2410.00037 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.00037) |
| 160 | arXiv:2410.03090 |  |  | 2 | inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2410.03090) |
| 161 | arXiv:2410.06511 |  |  | 2 | その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/2410.06511) |
| 162 | arXiv:2410.10989 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, その他システム研究 | [source](https://arxiv.org/abs/2410.10989) |
| 163 | arXiv:2410.13835 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2410.13835) |
| 164 | arXiv:2410.17840 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.17840) |
| 165 | arXiv:2410.23079 |  |  | 2 | KVキャッシュオフロード／階層メモリ, System-aware KV cache | [source](https://arxiv.org/abs/2410.23079) |
| 166 | arXiv:2411.01738 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2411.01738) |
| 167 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 168 | arXiv:2411.10640 |  |  | 2 | Edge／on-device MoE, inference-systems | [source](https://arxiv.org/abs/2411.10640) |
| 169 | arXiv:2412.01447 |  |  | 2 | inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2412.01447) |
| 170 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 171 | arXiv:2501.03035 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2501.03035) |
| 172 | arXiv:2501.10714 |  |  | 2 | Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2501.10714) |
| 173 | arXiv:2502.01662 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2502.01662) |
| 174 | arXiv:2502.06703 |  |  | 2 | Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, inference-systems | [source](https://arxiv.org/abs/2502.06703) |
| 175 | arXiv:2502.09696 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2502.09696) |
| 176 | arXiv:2502.13652 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2502.13652) |
| 177 | arXiv:2502.15304 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2502.15304) |
| 178 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 179 | arXiv:2503.13444 |  |  | 2 | kv-cache-offload-recomputation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2503.13444) |
| 180 | arXiv:2503.24358 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, System-aware KV cache | [source](https://arxiv.org/abs/2503.24358) |
| 181 | arXiv:2504.09014 |  |  | 2 | LLMサービング／スケジューリング／分離実行, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2504.09014) |
| 182 | arXiv:2504.12216 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2504.12216) |
| 183 | arXiv:2504.16054 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2504.16054) |
| 184 | arXiv:2504.17307 |  |  | 2 | KV Cache Offload / Recomputation, LLMサービング／スケジューリング／分離実行 | [source](https://arxiv.org/abs/2504.17307) |
| 185 | arXiv:2504.20101 |  |  | 2 | llm-serving-scheduling-disaggregation, 異種GPUサービング・分散推論・パイプライン並列・動的ルーティング | [source](https://arxiv.org/abs/2504.20101) |
| 186 | arXiv:2505.06708 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2505.06708) |
| 187 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 188 | arXiv:2505.16552 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.16552) |
| 189 | arXiv:2506.00413 |  |  | 2 | inference-systems, speculative-parallel-decoding | [source](https://arxiv.org/abs/2506.00413) |
| 190 | arXiv:2506.01928 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, inference-systems | [source](https://arxiv.org/abs/2506.01928) |
| 191 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 192 | arXiv:2507.07120 |  |  | 2 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2507.07120) |
| 193 | arXiv:2507.14111 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2507.14111) |
| 194 | arXiv:2507.18071 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2507.18071) |
| 195 | arXiv:2508.06447 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, System-aware KV cache | [source](https://arxiv.org/abs/2508.06447) |
| 196 | arXiv:2508.08712 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08712) |
| 197 | arXiv:2508.16712 |  |  | 2 | LLM serving scheduling / chunked prefill / MoE inference, llm-serving-systems | [source](https://arxiv.org/abs/2508.16712) |
| 198 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 199 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 200 | arXiv:2510.03293 |  |  | 2 | Expert Prefetch, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.03293) |
| 201 | arXiv:2510.08544 |  |  | 2 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.08544) |
| 202 | arXiv:2510.17483 |  |  | 2 | adaptive-expert-computation-compression, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2510.17483) |
| 203 | arXiv:2511.05502 |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2511.05502) |
| 204 | arXiv:2511.20048 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2511.20048) |
| 205 | arXiv:2512.01644 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2512.01644) |
| 206 | arXiv:2512.07647 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.07647) |
| 207 | arXiv:2512.16473 |  |  | 2 | Edge／on-device MoE, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.16473) |
| 208 | arXiv:2601.02872 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://arxiv.org/abs/2601.02872) |
| 209 | arXiv:2601.07568 |  |  | 2 | edge-on-device-llm-systems, inference-systems | [source](https://arxiv.org/abs/2601.07568) |
| 210 | arXiv:2601.11589 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, disaggregated LLM serving / request routing / learned scheduling | [source](https://arxiv.org/abs/2601.11589) |
| 211 | arXiv:2601.22379 |  |  | 2 | 07-kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2601.22379) |
| 212 | arXiv:2602.21224 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2602.21224) |
| 213 | arXiv:2603.28101 |  |  | 2 | LLM inference simulation / disaggregated serving / performance modeling, agentic LLM serving / pipeline parallelism / serving scheduling / speculative decoding | [source](https://arxiv.org/abs/2603.28101) |
| 214 | arXiv:2605.20315 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2605.20315) |
| 215 | arXiv:2606.22874 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2606.22874) |
| 216 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 217 | DOI:10.1109/dac63849.2025.11133274 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory-kv-offload-cpu-gpu-attention | [source](https://doi.org/10.1109/dac63849.2025.11133274) |
| 218 | DOI:10.1109/hcs61935.2024.10664793 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hcs61935.2024.10664793) |
| 219 | DOI:10.1109/hpca56546.2023.10071120 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://doi.org/10.1109/hpca56546.2023.10071120) |
| 220 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 2 | moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 221 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 222 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 223 | DOI:10.1109/lca.2025.3597323 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1109/lca.2025.3597323) |
| 224 | DOI:10.1109/mm.2023.3256384 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2023.3256384) |
| 225 | DOI:10.1109/mm.2025.3592688 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, moe-parallelism-communication | [source](https://doi.org/10.1109/mm.2025.3592688) |
| 226 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 227 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 228 | DOI:10.1145/224056.224064 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/224056.224064) |
| 229 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 230 | DOI:10.1145/3352460.3358302 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3352460.3358302) |
| 231 | DOI:10.1145/3453483.3454083 |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 232 | DOI:10.1145/3503222.3507738 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3503222.3507738) |
| 233 | DOI:10.1145/3572848.3577479 |  |  | 2 | 02-hardware-accelerators, kernel-runtime-compilation | [source](https://doi.org/10.1145/3572848.3577479) |
| 234 | DOI:10.1145/3575693.3576933 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3575693.3576933) |
| 235 | DOI:10.1145/3605573.3605613 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3605573.3605613) |
| 236 | DOI:10.1145/3627535.3638466 |  |  | 2 | KV Cache Optimization / Compression, serving-scheduling | [source](https://doi.org/10.1145/3627535.3638466) |
| 237 | DOI:10.1145/3650200.3656636 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, 分散推論／集団通信圧縮／量子化AllReduce／XLA・TPU | [source](https://doi.org/10.1145/3650200.3656636) |
| 238 | DOI:10.1145/3676641.3716252 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3676641.3716252) |
| 239 | DOI:10.1145/3706418 |  |  | 2 | 08-edge-on-device-llm-systems, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3706418) |
| 240 | DOI:10.1145/3725843.3756115 |  |  | 2 | PIM / Near-Data Acceleration, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756115) |
| 241 | DOI:10.1145/3768165 |  |  | 2 | Edge / On-device LLM Systems, speculative-decoding-moe | [source](https://doi.org/10.1145/3768165) |
| 242 | DOI:10.1145/3805475 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3805475) |
| 243 | DOI:10.14778/3415478.3415530 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.14778/3415478.3415530) |
| 244 | DOI:10.18653/v1/2021.acl-long.334 |  |  | 2 | Adaptive Expert Computation / Compression, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://doi.org/10.18653/v1/2021.acl-long.334) |
| 245 | DOI:10.18653/v1/2022.findings-acl.189 |  |  | 2 | Conditional Computation, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/2022.findings-acl.189) |
| 246 | DOI:10.18653/v1/2024.findings-acl.57 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.57) |
| 247 | DOI:10.18653/v1/2026.acl-long.83 |  |  | 2 | 13-sparse-attention, KVキャッシュ最適化／圧縮 | [source](https://doi.org/10.18653/v1/2026.acl-long.83) |
| 248 | DOI:10.18653/v1/w19-4828 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/w19-4828) |
| 249 | DOI:10.52202/068431-2198 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, early-exit-offloading-self-speculative-decoding | [source](https://doi.org/10.52202/068431-2198) |
| 250 | DOI:10.52202/079017-0040 |  |  | 2 | KV Cache Optimization / Compression, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://doi.org/10.52202/079017-0040) |
| 251 | DOI:10.52202/079017-3801 |  |  | 2 | KV Cache Optimization / Compression, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks | [source](https://doi.org/10.52202/079017-3801) |
| 252 | OpenReview:0fJfVOSUra |  |  | 2 | 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://openreview.net/forum?id=0fJfVOSUra) |
| 253 | OpenReview:acJ3vdFljk |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=acJ3vdFljk) |
| 254 | OpenReview:c5BOcHM6J8 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=c5BOcHM6J8) |
| 255 | OpenReview:dXiGWqBoxaD |  |  | 2 | 07-kv-cache-optimization-compression, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=dXiGWqBoxaD) |
| 256 | OpenReview:FbhjirzvJG |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=FbhjirzvJG) |
| 257 | OpenReview:HklBjCEKvH |  |  | 2 | Speculative Decoding, other-inference-systems | [source](https://openreview.net/forum?id=HklBjCEKvH) |
| 258 | OpenReview:JZfg6wGi6g |  |  | 2 | KV Cache Optimization / Compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=JZfg6wGi6g) |
| 259 | OpenReview:NGPmH3vbAA_ |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=NGPmH3vbAA_) |
| 260 | OpenReview:R7fv5NWfMm |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=R7fv5NWfMm) |
| 261 | OpenReview:RyOpooIxDF |  |  | 2 | inference-systems, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://openreview.net/forum?id=RyOpooIxDF) |
| 262 | OpenReview:xdNAVP7TGy |  |  | 2 | kv-cache-offload-recomputation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://openreview.net/forum?id=xdNAVP7TGy) |
| 263 | arXiv:1312.6114 |  |  | 2 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 264 | arXiv:1902.09506 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1902.09506) |
| 265 | arXiv:1906.11024 |  |  | 2 | 99-other-inference-systems | [source](https://arxiv.org/abs/1906.11024) |
| 266 | arXiv:2105.13878 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2105.13878) |
| 267 | arXiv:2205.01848 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2205.01848) |
| 268 | arXiv:2211.00593 |  |  | 2 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 269 | arXiv:2212.14052 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2212.14052) |
| 270 | arXiv:2305.07622 |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 271 | arXiv:2305.17455 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.17455) |
| 272 | arXiv:2311.14652 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2311.14652) |
| 273 | arXiv:2403.16971 |  |  | 2 | other | [source](https://arxiv.org/abs/2403.16971) |
| 274 | arXiv:2404.04793 |  |  | 2 | other-inference-systems | [source](https://arxiv.org/abs/2404.04793) |
| 275 | arXiv:2405.18218 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2405.18218) |
| 276 | arXiv:2407.01527 |  |  | 2 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化 | [source](https://arxiv.org/abs/2407.01527) |
| 277 | arXiv:2409.03752 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2409.03752) |
| 278 | arXiv:2410.12876 |  |  | 2 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.12876) |
| 279 | arXiv:2411.05902 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2411.05902) |
| 280 | arXiv:2412.19821 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2412.19821) |
| 281 | arXiv:2502.05171 |  |  | 2 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2502.05171) |
| 282 | arXiv:2503.14476 |  |  | 2 | 99-other-inference-systems | [source](https://arxiv.org/abs/2503.14476) |
| 283 | arXiv:2505.24857 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2505.24857) |
| 284 | arXiv:2506.13759 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2506.13759) |
| 285 | arXiv:2509.18085 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding | [source](https://arxiv.org/abs/2509.18085) |
| 286 | arXiv:2512.14681 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2512.14681) |
| 287 | arXiv:2602.08404 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2602.08404) |
| 288 | arXiv:2604.05546 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2604.05546) |
| 289 | arXiv:2605.09649 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2605.09649) |
| 290 | arXiv:2605.18053 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2605.18053) |
| 291 | DOI:10.1109/hpca61900.2025.00086 |  |  | 2 | low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1109/hpca61900.2025.00086) |
| 292 | DOI:10.1109/isocc53507.2021.9613933 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.1109/isocc53507.2021.9613933) |
| 293 | DOI:10.1145/3581791.3596831 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3581791.3596831) |
| 294 | DOI:10.14778/3626292.3626303 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.14778/3626292.3626303) |
| 295 | DOI:10.18653/v1/2023.emnlp-main.183 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.18653/v1/2023.emnlp-main.183) |
| 296 | DOI:10.18653/v1/2023.emnlp-main.907 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/2023.emnlp-main.907) |
| 297 | DOI:10.18653/v1/2024.emnlp-main.897 |  |  | 2 | kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.897) |
| 298 | DOI:10.18653/v1/2025.acl-long.671 |  |  | 2 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing | [source](https://doi.org/10.18653/v1/2025.acl-long.671) |
| 299 | DOI:10.3115/1073083.1073135 |  |  | 2 | confidential inference / trusted execution environment / split inference / differential privacy | [source](https://doi.org/10.3115/1073083.1073135) |
| 300 | OpenReview:44PwmgOpAt |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=44PwmgOpAt) |
| 301 | OpenReview:9k27IITeAZ |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=9k27IITeAZ) |
| 302 | OpenReview:dfqsW38v1X |  |  | 2 | MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=dfqsW38v1X) |
| 303 | OpenReview:P0GOk5wslg |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=P0GOk5wslg) |
| 304 | OpenReview:tcisuhGsQZ |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=tcisuhGsQZ) |
| 305 | OpenReview:uPv9Y3gmAI5 |  |  | 2 | MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=uPv9Y3gmAI5) |
| 306 | arXiv:1710.09412 |  |  | 2 |  | [source](https://arxiv.org/abs/1710.09412) |
| 307 | arXiv:2307.10169 |  |  | 2 |  | [source](https://arxiv.org/abs/2307.10169) |
| 308 | arXiv:2312.04927 |  |  | 2 |  | [source](https://arxiv.org/abs/2312.04927) |
| 309 | arXiv:2410.02694 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.02694) |
| 310 | arXiv:2503.07518 |  |  | 2 |  | [source](https://arxiv.org/abs/2503.07518) |
| 311 | DOI:10.18653/v1/2021.findings-acl.449 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2021.findings-acl.449) |
| 312 | DOI:10.48550/arxiv.2304.08354 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2304.08354) |
| 313 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 314 | OpenReview:FJFVmeXusW |  |  | 2 |  | [source](https://openreview.net/forum?id=FJFVmeXusW) |
| 315 | OpenReview:OS5dqxmmtl |  |  | 2 |  | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 316 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 317 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 318 | arXiv:1212.0402 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 319 | arXiv:1312.6211 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 320 | arXiv:1409.3215 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1409.3215) |
| 321 | arXiv:1504.00325 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1504.00325) |
| 322 | arXiv:1506.02640 |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1506.02640) |
| 323 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 324 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 325 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 326 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 327 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 328 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 329 | arXiv:1606.06160 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 330 | arXiv:1610.02136 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1610.02136) |
| 331 | arXiv:1611.01576 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1611.01576) |
| 332 | arXiv:1611.07409 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1611.07409) |
| 333 | arXiv:1701.05517 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1701.05517) |
| 334 | arXiv:1703.04247 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1703.04247) |
| 335 | arXiv:1704.02147 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1704.02147) |
| 336 | arXiv:1704.05021 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1704.05021) |
| 337 | arXiv:1705.06419 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1705.06419) |
| 338 | arXiv:1705.09786 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1705.09786) |
| 339 | arXiv:1707.00110 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1707.00110) |
| 340 | arXiv:1708.00055 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1708.00055) |
| 341 | arXiv:1708.08197 |  |  | 1 | KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://arxiv.org/abs/1708.08197) |
| 342 | arXiv:1710.01878 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/1710.01878) |
| 343 | arXiv:1711.00123 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1711.00123) |
| 344 | arXiv:1711.04291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1711.04291) |
| 345 | arXiv:1712.01208 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/1712.01208) |
| 346 | arXiv:1712.07040 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1712.07040) |
| 347 | arXiv:1802.04730 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/1802.04730) |
| 348 | arXiv:1802.06509 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1802.06509) |
| 349 | arXiv:1803.05407 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1803.05407) |
| 350 | arXiv:1805.04623 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1805.04623) |
| 351 | arXiv:1806.02847 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 352 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 353 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 354 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 355 | arXiv:1810.00602 |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/1810.00602) |
| 356 | arXiv:1810.05291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.05291) |
| 357 | arXiv:1811.01088 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1811.01088) |
| 358 | arXiv:1811.08886 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/1811.08886) |
| 359 | arXiv:1812.09764 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1812.09764) |
| 360 | arXiv:1902.03383 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/1902.03383) |
| 361 | arXiv:1902.09113 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1902.09113) |
| 362 | arXiv:1903.01611 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1903.01611) |
| 363 | arXiv:1903.05662 |  |  | 1 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference | [source](https://arxiv.org/abs/1903.05662) |
| 364 | arXiv:1904.10631 |  |  | 1 | long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/1904.10631) |
| 365 | arXiv:1905.07129 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 366 | arXiv:1906.04341 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 367 | arXiv:1906.10771 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1906.10771) |
| 368 | arXiv:1907.12009 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1907.12009) |
| 369 | arXiv:1908.10084 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1908.10084) |
| 370 | arXiv:1908.11775 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1908.11775) |
| 371 | arXiv:1909.09577 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1909.09577) |
| 372 | arXiv:1909.13271 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1909.13271) |
| 373 | arXiv:1910.05316 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/1910.05316) |
| 374 | arXiv:1910.09700 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1910.09700) |
| 375 | arXiv:1911.03014 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/1911.03014) |
| 376 | arXiv:1911.08731 |  |  | 1 | moe-quantization-compression | [source](https://arxiv.org/abs/1911.08731) |
| 377 | arXiv:1912.12180 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1912.12180) |
| 378 | arXiv:2001.04246 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2001.04246) |
| 379 | arXiv:2002.08307 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2002.08307) |
| 380 | arXiv:2002.10941 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2002.10941) |
| 381 | arXiv:2002.11985 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.11985) |
| 382 | arXiv:2003.07013 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.07013) |
| 383 | arXiv:2003.12462 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2003.12462) |
| 384 | arXiv:2004.07320 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2004.07320) |
| 385 | arXiv:2004.10964 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2004.10964) |
| 386 | arXiv:2005.00628 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 387 | arXiv:2005.03454 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 388 | arXiv:2006.00996 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2006.00996) |
| 389 | arXiv:2006.10518 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 390 | arXiv:2006.11527 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2006.11527) |
| 391 | arXiv:2007.03152 |  |  | 1 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://arxiv.org/abs/2007.03152) |
| 392 | arXiv:2007.12626 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2007.12626) |
| 393 | arXiv:2008.05221 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2008.05221) |
| 394 | arXiv:2009.07118 |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2009.07118) |
| 395 | arXiv:2009.08065 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2009.08065) |
| 396 | arXiv:2009.13239 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2009.13239) |
| 397 | arXiv:2010.02523 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2010.02523) |
| 398 | arXiv:2010.03633 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2010.03633) |
| 399 | arXiv:2010.07003 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2010.07003) |
| 400 | arXiv:2010.13002 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.13002) |
| 401 | arXiv:2011.02999 |  |  | 1 | 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://arxiv.org/abs/2011.02999) |
| 402 | arXiv:2011.06327 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2011.06327) |
| 403 | arXiv:2012.11346 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2012.11346) |
| 404 | arXiv:2012.15688 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2012.15688) |
| 405 | arXiv:2012.15833 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2012.15833) |
| 406 | arXiv:2101.09671 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2101.09671) |
| 407 | arXiv:2102.06621 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2102.06621) |
| 408 | arXiv:2102.08602 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2102.08602) |
| 409 | arXiv:2102.11972 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2102.11972) |
| 410 | arXiv:2103.07191 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2103.07191) |
| 411 | arXiv:2104.08771 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2104.08771) |
| 412 | arXiv:2105.03036 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.03036) |
| 413 | arXiv:2105.08928 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2105.08928) |
| 414 | arXiv:2105.14450 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2105.14450) |
| 415 | arXiv:2106.03764 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2106.03764) |
| 416 | arXiv:2106.05974 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2106.05974) |
| 417 | arXiv:2106.08823 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2106.08823) |
| 418 | arXiv:2107.02561 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2107.02561) |
| 419 | arXiv:2107.11906 |  |  | 1 | long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2107.11906) |
| 420 | arXiv:2108.06098 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2108.06098) |
| 421 | arXiv:2109.02132 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2109.02132) |
| 422 | arXiv:2109.08406 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2109.08406) |
| 423 | arXiv:2109.11067 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2109.11067) |
| 424 | arXiv:2109.15082 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2109.15082) |
| 425 | arXiv:2110.07431 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2110.07431) |
| 426 | arXiv:2110.13283 |  |  | 1 | llm-serving-systems | [source](https://arxiv.org/abs/2110.13283) |
| 427 | arXiv:2111.00364 |  |  | 1 | hardware-accelerators | [source](https://arxiv.org/abs/2111.00364) |
| 428 | arXiv:2111.12293 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2111.12293) |
| 429 | arXiv:2112.03097 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2112.03097) |
| 430 | arXiv:2112.07916 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2112.07916) |
| 431 | arXiv:2112.12731 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.12731) |
| 432 | arXiv:2201.05767 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2201.05767) |
| 433 | arXiv:2201.13425 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2201.13425) |
| 434 | arXiv:2202.05262 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2202.05262) |
| 435 | arXiv:2202.08791 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2202.08791) |
| 436 | arXiv:2202.12015 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2202.12015) |
| 437 | arXiv:2203.00386 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2203.00386) |
| 438 | arXiv:2203.05482 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.05482) |
| 439 | arXiv:2203.07814 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2203.07814) |
| 440 | arXiv:2203.13240 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2203.13240) |
| 441 | arXiv:2204.01691 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2204.01691) |
| 442 | arXiv:2204.06125 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2204.06125) |
| 443 | arXiv:2204.07705 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2204.07705) |
| 444 | arXiv:2204.13807 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2204.13807) |
| 445 | arXiv:2205.05131 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2205.05131) |
| 446 | arXiv:2205.07324 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2205.07324) |
| 447 | arXiv:2205.11380 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2205.11380) |
| 448 | arXiv:2205.12701 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12701) |
| 449 | arXiv:2206.02845 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2206.02845) |
| 450 | arXiv:2207.00220 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2207.00220) |
| 451 | arXiv:2207.10551 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2207.10551) |
| 452 | arXiv:2208.02813 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 453 | arXiv:2208.08227 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 454 | arXiv:2209.03143 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 455 | arXiv:2209.11429 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 456 | arXiv:2209.15352 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 457 | arXiv:2210.03350 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2210.03350) |
| 458 | arXiv:2210.07535 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.07535) |
| 459 | arXiv:2210.11948 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 460 | arXiv:2210.14793 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 461 | arXiv:2211.00107 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.00107) |
| 462 | arXiv:2211.05953 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2211.05953) |
| 463 | arXiv:2211.08403 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2211.08403) |
| 464 | arXiv:2211.11586 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2211.11586) |
| 465 | arXiv:2212.00768 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.00768) |
| 466 | arXiv:2212.04037 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2212.04037) |
| 467 | arXiv:2212.05191 |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2212.05191) |
| 468 | arXiv:2212.08410 |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2212.08410) |
| 469 | arXiv:2212.10445 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2212.10445) |
| 470 | arXiv:2212.10650 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2212.10650) |
| 471 | arXiv:2301.02111 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.02111) |
| 472 | arXiv:2301.05843 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2301.05843) |
| 473 | arXiv:2301.08721 |  |  | 1 | kv-cache-memory | [source](https://arxiv.org/abs/2301.08721) |
| 474 | arXiv:2301.11235 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2301.11235) |
| 475 | arXiv:2301.13823 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2301.13823) |
| 476 | arXiv:2302.04062 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2302.04062) |
| 477 | arXiv:2302.06784 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2302.06784) |
| 478 | arXiv:2302.09632 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.09632) |
| 479 | arXiv:2302.11750 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2302.11750) |
| 480 | arXiv:2302.12510 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.12510) |
| 481 | arXiv:2303.00980 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.00980) |
| 482 | arXiv:2303.04129 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.04129) |
| 483 | arXiv:2303.06153 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2303.06153) |
| 484 | arXiv:2303.10130 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2303.10130) |
| 485 | arXiv:2303.13003 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2303.13003) |
| 486 | arXiv:2303.16199 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 487 | arXiv:2303.17568 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.17568) |
| 488 | arXiv:2304.01468 |  |  | 1 | SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2304.01468) |
| 489 | arXiv:2304.03208 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2304.03208) |
| 490 | arXiv:2304.04488 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2304.04488) |
| 491 | arXiv:2304.05332 |  |  | 1 | LLM inference kernel safety / CUDA symbolic execution / model-aware verification | [source](https://arxiv.org/abs/2304.05332) |
| 492 | arXiv:2304.08442 |  |  | 1 | MoE推論／エキスパート並列／エキスパート配置／全対全通信／負荷分散 | [source](https://arxiv.org/abs/2304.08442) |
| 493 | arXiv:2304.10592 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.10592) |
| 494 | arXiv:2304.14979 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2304.14979) |
| 495 | arXiv:2305.01625 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2305.01625) |
| 496 | arXiv:2305.03653 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2305.03653) |
| 497 | arXiv:2305.04701 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.04701) |
| 498 | arXiv:2305.08367 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.08367) |
| 499 | arXiv:2305.10266 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.10266) |
| 500 | arXiv:2305.12870 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.12870) |

## Machine-readable

同じ割当は [worker-worklist-00.json](worker-worklist-00.json) にあります。

