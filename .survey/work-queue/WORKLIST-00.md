# Scheduled worker :00 worklist

Worker: `scheduled-chat-00`  
Generated: `2026-10-03T09:08:45+00:00`

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

未判定総数: **7010** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | arXiv:2502.09992 |  |  | 29 | 04-moe-parallelism-communication, Diffusion LLM Inference, Other Inference Systems / Lossless Parallel Decoding, Speculative Decoding, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, diffusion language model inference / KV cache / training-free acceleration, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, diffusion-llm-inference / caching / low-precision, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, speculative decoding / parallel drafting / diffusion-inspired language modeling, speculative-decoding, speculative-parallel-decoding, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。, 投機的復号・ブロック拡散提案・検証器中間表現の再利用, 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2502.09992) |
| 2 | DOI:10.48550/arxiv.2408.11850 |  |  | 19 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative Decoding / Parallel Inference Systems, inference-systems, speculative-decoding, speculative-decoding-moe, 投機的デコード／MoE, 投機的デコード／動的候補木／高同時実行LLMサービング | [source](https://doi.org/10.48550/arxiv.2408.11850) |
| 3 | DOI:10.1145/3694715.3695948 |  |  | 17 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 4 | arXiv:2312.04985 |  |  | 16 | KV cache compression / sparse attention / long-context inference, KV cache quantization / long-context inference / activation compression, Offload / Hierarchical Memory, Sparse Attention, inference-systems, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, sparse attention / KV-cache bandwidth reduction, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2312.04985) |
| 5 | arXiv:2407.12820 |  |  | 15 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, inference-systems, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://arxiv.org/abs/2407.12820) |
| 6 | arXiv:1912.01703 |  |  | 14 | 05-speculative-decoding-moe, 13-sparse-attention, GPU Kernel Framework, GPUカーネル融合／SwiGLU／LLM推論ランタイム, Offload / Hierarchical Memory, inference-systems, その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/1912.01703) |
| 7 | DOI:10.1016/j.neucom.2023.127063 |  |  | 14 | 02-hardware-accelerators, GPU architecture and tensor-computation orchestration, KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ最適化／圧縮, Sparse Attention, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://doi.org/10.1016/j.neucom.2023.127063) |
| 8 | arXiv:1808.08745 |  |  | 13 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 9 | OpenReview:tcbBPnfwxS |  |  | 13 | Adaptive Expert Computation / Compression, LLM Serving / Scheduling, MoE compression / structured pruning / atomic expert pruning / second-order pruning, Speculative Decoding, inference-systems, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=tcbBPnfwxS) |
| 10 | arXiv:2501.12599 |  |  | 12 | 11-llm-serving-scheduling-disaggregation, Conditional Computation, LLM Serving / Reasoning, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, inference-systems, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, serving-scheduling, 推論ベンチマーク・推論大規模言語モデルのサービング評価, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.12599) |
| 11 | arXiv:2402.17764 |  |  | 12 | 08-edge-on-device-llm-systems, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline, offload-hierarchical-memory, post-training quantization / ternary LLM / packed inference, survey-distributed-training-systems, survey-low-bit-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.17764) |
| 12 | arXiv:2304.04487 |  |  | 12 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 投機的デコード / 自己投機的デコード / 層スキップ | [source](https://arxiv.org/abs/2304.04487) |
| 13 | DOI:10.48550/arxiv.2311.04939 |  |  | 12 | KV Cache Compression / Long Context, KVキャッシュ退避／長文推論／KV選択／KV量子化, inference-systems, kv-cache-offload-recomputation, prefix caching / hybrid attention-SSM serving | [source](https://doi.org/10.48550/arxiv.2311.04939) |
| 14 | arXiv:2601.03267 |  |  | 11 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, 投機的デコードにおける自己回帰ドラフトと並列ドラフトの折衷, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2601.03267) |
| 15 | arXiv:2304.09145 |  |  | 11 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Weight Quantization / Compression, inference-systems, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 16 | arXiv:2407.21118 |  |  | 11 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2407.21118) |
| 17 | DOI:10.18653/v1/2024.emnlp-main.890 |  |  | 10 | Adaptive computation／cache-aware MoE, Edge／on-device MoE, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive-expert-computation-compression, moe-inference-expert-offloading, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://doi.org/10.18653/v1/2024.emnlp-main.890) |
| 18 | DOI:10.48550/arxiv.2412.00099 |  |  | 10 | 08-edge-on-device-llm-systems, edge-on-device-llm-systems, hardware-accelerators, offload-hierarchical-memory, survey-moe-inference-optimization, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.48550/arxiv.2412.00099) |
| 19 | DOI:10.18653/v1/2025.emnlp-main.334 |  |  | 10 | 10-kv-cache-offload-recomputation, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, inference-systems, kv-cache-reuse-position-independent-caching, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://doi.org/10.18653/v1/2025.emnlp-main.334) |
| 20 | DOI:10.18653/v1/2024.emnlp-main.422 |  |  | 9 | 05-speculative-decoding-moe, LLM Serving / Scheduling / Disaggregation, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE, other-inference-systems, speculative-decoding, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://doi.org/10.18653/v1/2024.emnlp-main.422) |
| 21 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 22 | OpenReview:qrwe7XHTmYb |  |  | 9 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, LLM Serving / Multi-Model Serving / Memory Disaggregation, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, Speculative decoding × MoE, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=qrwe7XHTmYb) |
| 23 | arXiv:2308.12966 |  |  | 9 | KV cache compression for multimodal inference, adaptive expert computation / dynamic MoE routing / gating uncertainty, inference-systems, その他システム研究, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2308.12966) |
| 24 | arXiv:2501.14249 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, LLM Serving / Scheduling / Disaggregation, Other Inference Systems / Lossless Parallel Decoding, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2501.14249) |
| 25 | DOI:10.5281/zenodo.5371628 |  |  | 9 | KV Cache Optimization / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Weight Quantization / Compression, inference-systems, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.5281/zenodo.5371628) |
| 26 | arXiv:2306.09212 |  |  | 9 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2306.09212) |
| 27 | arXiv:2409.06669 |  |  | 8 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, Quantization × MoE × Offload, Speculative decoding × MoE, adaptive expert computation / dynamic MoE routing / expert sparsification, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, mixture-of-experts / diffusion LLM inference / expert sharing / memory-traffic reduction, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2409.06669) |
| 28 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 29 | arXiv:2511.21631 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / dynamic MoE routing / gating uncertainty, flash-capacity-tier-inference, inference-systems | [source](https://arxiv.org/abs/2511.21631) |
| 30 | OpenReview:wHBfxhZu1u |  |  | 8 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, KVキャッシュ退避／長文推論／KV選択／KV量子化, inference-systems, kv-cache-optimization-compression, other-inference-systems, 投機的復号 / LLMサービング・ベンチマーク | [source](https://openreview.net/forum?id=wHBfxhZu1u) |
| 31 | arXiv:2408.11743 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 32 | DOI:10.18653/v1/n18-2097 |  |  | 8 | 08-edge-on-device-llm-systems, inference-systems, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.18653/v1/n18-2097) |
| 33 | arXiv:2401.00625 |  |  | 7 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, System-aware KV cache, distributed LLM inference / communication-aware serving, llm-serving-systems, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.00625) |
| 34 | OpenReview:WE_vluYUL-X |  |  | 7 | RAG runtime / distributed orchestration / agentic workflows, agentic serving / KV cache eviction / persistent multi-turn serving, agentic serving workload characterization / KV-cache / inference benchmarking, agentic workflow serving / workflow physical planning / adaptive serving, kv-cache-optimization-compression, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://openreview.net/forum?id=WE_vluYUL-X) |
| 35 | arXiv:2212.10560 |  |  | 7 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2212.10560) |
| 36 | DOI:10.1145/3768628 |  |  | 7 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 37 | arXiv:2412.10302 |  |  | 7 | Adaptive computation／cache-aware MoE, MoE compression / training-free expert merging / multimodal MoE routing, Quantization × MoE × Offload, adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2412.10302) |
| 38 | OpenReview:Bkg6RiCqY7 |  |  | 7 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 39 | arXiv:2310.15141 |  |  | 7 | LLM inference surveys、roofline performance analysis, inference-systems, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 40 | arXiv:2509.16941 |  |  | 7 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2509.16941) |
| 41 | OpenReview:EytBpUGB1Z |  |  | 7 | KV Cache Optimization / Compression, Sparse Attention / VLM Inference | [source](https://openreview.net/forum?id=EytBpUGB1Z) |
| 42 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 43 | OpenReview:v8L0pN6EOi |  |  | 6 | KV Cache Optimization / Compression, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, reasoning-model compression / post-training pruning / calibration-data selection / causal intervention, speculative-decoding, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://openreview.net/forum?id=v8L0pN6EOi) |
| 44 | DOI:10.1145/3503222.3507778 |  |  | 6 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.1145/3503222.3507778) |
| 45 | arXiv:2203.08913 |  |  | 6 | LLM inference surveys、roofline performance analysis, inference-systems, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 46 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 47 | DOI:10.1145/3620666.3651379 |  |  | 6 | inference-systems, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651379) |
| 48 | arXiv:2401.03868 |  |  | 6 | LLM inference surveys、roofline performance analysis, hierarchical-memory, kv-cache-memory | [source](https://arxiv.org/abs/2401.03868) |
| 49 | arXiv:2508.18298 |  |  | 6 | inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18298) |
| 50 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 6 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 51 | OpenReview:rkgNKkHtvB |  |  | 6 | 10-kv-cache-offload-recomputation, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems | [source](https://openreview.net/forum?id=rkgNKkHtvB) |
| 52 | arXiv:2412.06769 |  |  | 6 | 99-other-inference-systems, Conditional Computation | [source](https://arxiv.org/abs/2412.06769) |
| 53 | OpenReview:mZn2Xyh9Ec |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=mZn2Xyh9Ec) |
| 54 | arXiv:2204.09179 |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 55 | DOI:10.18653/v1/2024.findings-acl.57 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Long-context serving / KV cache benchmark, inference-systems, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.57) |
| 56 | arXiv:2402.02244 |  |  | 5 | KV Cache Compression / Long Context, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 57 | DOI:10.1145/3732941 |  |  | 5 | LLM Serving / Scheduling / Disaggregation, dynamic-pd-disaggregation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3732941) |
| 58 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 59 | arXiv:2402.01680 |  |  | 5 | llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 60 | arXiv:2406.07887 |  |  | 5 | Long-context serving / KV cache benchmark, PIM / Near-Data Acceleration, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2406.07887) |
| 61 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 5 | Speculative Decoding, inference-systems, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 62 | arXiv:2207.07061 |  |  | 5 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2207.07061) |
| 63 | arXiv:2603.05451 |  |  | 5 | diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2603.05451) |
| 64 | DOI:10.48550/arxiv.2412.18910 |  |  | 5 | 05-speculative-decoding-moe, inference-systems | [source](https://doi.org/10.48550/arxiv.2412.18910) |
| 65 | OpenReview:2GmDdhBdDk |  |  | 5 | inference-systems | [source](https://openreview.net/forum?id=2GmDdhBdDk) |
| 66 | arXiv:2309.01885 |  |  | 4 | 16-weight-quantization-compression, LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.01885) |
| 67 | arXiv:2503.08311 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, KV Cache Optimization / Compression, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, inference-systems | [source](https://arxiv.org/abs/2503.08311) |
| 68 | arXiv:2511.00739 |  |  | 4 | LLM Serving / Scheduling / Disaggregation, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, agentic serving workload characterization / KV-cache / inference benchmarking, inference-systems | [source](https://arxiv.org/abs/2511.00739) |
| 69 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 4 | Inference Kernel / Determinism, inference-systems, moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 70 | DOI:10.1145/3630106.3658542 |  |  | 4 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3630106.3658542) |
| 71 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 72 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 73 | OpenReview:z5uVAKwmjf |  |  | 4 | 14-agentic-inference-serving-runtime, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, LLMサービング／自動スケーリング／広域ルーティング, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=z5uVAKwmjf) |
| 74 | arXiv:2311.10122 |  |  | 4 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference, inference-systems | [source](https://arxiv.org/abs/2311.10122) |
| 75 | arXiv:2402.06082 |  |  | 4 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 76 | arXiv:2407.04014 |  |  | 4 | inference-systems, llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 77 | arXiv:2411.05239 |  |  | 4 | distributed LLM inference / communication-aware serving, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2411.05239) |
| 78 | arXiv:2502.17416 |  |  | 4 | Conditional Computation, adaptive-expert-computation-compression, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2502.17416) |
| 79 | arXiv:2507.11851 |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2507.11851) |
| 80 | DOI:10.1109/mm.2024.3375352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, Offload / Hierarchical Memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/mm.2024.3375352) |
| 81 | DOI:10.1145/3572848.3577479 |  |  | 4 | 02-hardware-accelerators, inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/3572848.3577479) |
| 82 | DOI:10.1145/3731569.3764808 |  |  | 4 | edge-on-device-llm-systems, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764808) |
| 83 | DOI:10.48550/arxiv.2409.12136 |  |  | 4 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, inference-systems, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2409.12136) |
| 84 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 85 | arXiv:1902.09574 |  |  | 4 | inference-systems, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 86 | arXiv:2004.02984 |  |  | 4 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2004.02984) |
| 87 | arXiv:2405.05329 |  |  | 4 | KV Cache Optimization / Compression, inference-systems | [source](https://arxiv.org/abs/2405.05329) |
| 88 | arXiv:2408.12570 |  |  | 4 | PIM / Near-Data Acceleration, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2408.12570) |
| 89 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 90 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 91 | OpenReview:MaYzugDmQV |  |  | 4 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 92 | OpenReview:ziezViPoN1 |  |  | 4 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=ziezViPoN1) |
| 93 | arXiv:2403.09054 |  |  | 4 | Conditional Computation | [source](https://arxiv.org/abs/2403.09054) |
| 94 | arXiv:2501.00663 |  |  | 4 | prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2501.00663) |
| 95 | DOI:10.48550/arxiv.2305.14152 |  |  | 4 | LLM inference surveys、roofline performance analysis | [source](https://doi.org/10.48550/arxiv.2305.14152) |
| 96 | arXiv:1704.04861 |  |  | 3 | KV Cache Optimization / Compression, inference-systems, on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1704.04861) |
| 97 | arXiv:2203.06390 |  |  | 3 | Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.06390) |
| 98 | arXiv:2307.01952 |  |  | 3 | Diffusion LLM Inference, LLM Serving / Scheduling / Disaggregation, MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2307.01952) |
| 99 | arXiv:2309.05516 |  |  | 3 | Expert Prefetch, inference-systems, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 100 | arXiv:2310.01655 |  |  | 3 | GPU Kernel Framework, KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2310.01655) |
| 101 | arXiv:2401.12522 |  |  | 3 | inference-systems, speculative-decoding, 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/2401.12522) |
| 102 | arXiv:2404.03605 |  |  | 3 | Conditional Computation, Quantization × MoE × Offload, inference-systems | [source](https://arxiv.org/abs/2404.03605) |
| 103 | arXiv:2406.00059 |  |  | 3 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, inference-systems | [source](https://arxiv.org/abs/2406.00059) |
| 104 | arXiv:2406.11939 |  |  | 3 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2406.11939) |
| 105 | arXiv:2409.01990 |  |  | 3 | KV cache sparsity / paged attention / query-aware selection / LLM serving, inference-systems, moe | [source](https://arxiv.org/abs/2409.01990) |
| 106 | arXiv:2410.03834 |  |  | 3 | inference-systems, llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2410.03834) |
| 107 | arXiv:2410.17891 |  |  | 3 | Speculative Decoding, diffusion language model inference / KV cache / training-free acceleration, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2410.17891) |
| 108 | arXiv:2411.11055 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 109 | arXiv:2502.06768 |  |  | 3 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration, inference-systems | [source](https://arxiv.org/abs/2502.06768) |
| 110 | arXiv:2503.09567 |  |  | 3 | Graph-CoT / multi-agent serving / KV-cache reuse, LLM Serving / Reasoning, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2503.09567) |
| 111 | arXiv:2504.17307 |  |  | 3 | KV Cache Offload / Recomputation, LLM Serving / Distributed Communication, LLMサービング／スケジューリング／分離実行 | [source](https://arxiv.org/abs/2504.17307) |
| 112 | arXiv:2507.14111 |  |  | 3 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2507.14111) |
| 113 | DOI:10.1016/j.jpdc.2017.12.007 |  |  | 3 | GPU architecture and tensor-computation orchestration, LLM Serving / Distributed Communication, inference-systems | [source](https://doi.org/10.1016/j.jpdc.2017.12.007) |
| 114 | DOI:10.1109/lca.2026.3705817 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3705817) |
| 115 | DOI:10.1109/sc41406.2024.00094 |  |  | 3 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1109/sc41406.2024.00094) |
| 116 | DOI:10.1145/3458864.3467882 |  |  | 3 | Edge／on-device MoE, LLMサービング・スケジューリング・分離実行, other-inference-systems | [source](https://doi.org/10.1145/3458864.3467882) |
| 117 | DOI:10.1145/3575693.3576933 |  |  | 3 | inference-systems, kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3575693.3576933) |
| 118 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 119 | DOI:10.1145/3779212.3790187 |  |  | 3 | MoE expert offloading / predictive prefetch and cache management, hierarchical-memory-kv-offload-cpu-gpu-attention, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.1145/3779212.3790187) |
| 120 | DOI:10.48550/arxiv.2507.17702 |  |  | 3 | adaptive expert computation / compression; end-side sparse MoE, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://doi.org/10.48550/arxiv.2507.17702) |
| 121 | OpenReview:1YDeZU8Lt5 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=1YDeZU8Lt5) |
| 122 | OpenReview:CS2JWaziYr |  |  | 3 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=CS2JWaziYr) |
| 123 | OpenReview:rJl-b3RcF7 |  |  | 3 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=rJl-b3RcF7) |
| 124 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 125 | arXiv:1311.2540 |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 126 | arXiv:1711.09224 |  |  | 3 | 02-hardware-accelerators, unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1711.09224) |
| 127 | arXiv:2105.06990 |  |  | 3 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2105.06990) |
| 128 | arXiv:2302.02451 |  |  | 3 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2302.02451) |
| 129 | arXiv:2304.08485 |  |  | 3 | speculative-decoding, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.08485) |
| 130 | arXiv:2307.08072 |  |  | 3 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 131 | arXiv:2310.03744 |  |  | 3 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 132 | arXiv:2311.05232 |  |  | 3 | LLM inference surveys、roofline performance analysis, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2311.05232) |
| 133 | arXiv:2401.02038 |  |  | 3 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 134 | arXiv:2402.09025 |  |  | 3 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 135 | arXiv:2403.06764 |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.06764) |
| 136 | arXiv:2406.15786 |  |  | 3 | inference-systems, offload-hierarchical-memory | [source](https://arxiv.org/abs/2406.15786) |
| 137 | arXiv:2407.07000 |  |  | 3 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.07000) |
| 138 | arXiv:2408.08696 |  |  | 3 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2408.08696) |
| 139 | arXiv:2409.17146 |  |  | 3 | Adaptive computation／cache-aware MoE, adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2409.17146) |
| 140 | arXiv:2410.23079 |  |  | 3 | KVキャッシュオフロード／階層メモリ, System-aware KV cache | [source](https://arxiv.org/abs/2410.23079) |
| 141 | arXiv:2411.17116 |  |  | 3 | Long-context serving / KV cache benchmark, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2411.17116) |
| 142 | arXiv:2502.02617 |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02617) |
| 143 | arXiv:2504.16054 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2504.16054) |
| 144 | arXiv:2506.13585 |  |  | 3 | kv-cache-reuse-position-independent-caching, speculative-decoding | [source](https://arxiv.org/abs/2506.13585) |
| 145 | arXiv:2508.17196 |  |  | 3 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.17196) |
| 146 | arXiv:2602.08676 |  |  | 3 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2602.08676) |
| 147 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 148 | DOI:10.1109/isca45697.2020.00047 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/isca45697.2020.00047) |
| 149 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 150 | DOI:10.1145/3503222.3507709 |  |  | 3 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, inference-systems | [source](https://doi.org/10.1145/3503222.3507709) |
| 151 | DOI:10.1145/3636534.3649379 |  |  | 3 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3636534.3649379) |
| 152 | DOI:10.1145/3719330.3721230 |  |  | 3 | 08-edge-on-device-llm-systems, KV Cache Offload / Recomputation | [source](https://doi.org/10.1145/3719330.3721230) |
| 153 | DOI:10.18653/v1/2020.emnlp-main.550 |  |  | 3 | inference-systems, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2020.emnlp-main.550) |
| 154 | DOI:10.18653/v1/2024.acl-long.814 |  |  | 3 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.814) |
| 155 | DOI:10.5281/zenodo.1234 |  |  | 3 | inference-systems, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://doi.org/10.5281/zenodo.1234) |
| 156 | OpenReview:6PmJoRfdaK |  |  | 3 | inference-systems, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=6PmJoRfdaK) |
| 157 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 158 | OpenReview:jxpsAj7ltE |  |  | 3 | Adaptive Expert Computation / Compression, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=jxpsAj7ltE) |
| 159 | OpenReview:uBaFH7aQnC |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=uBaFH7aQnC) |
| 160 | arXiv:1410.5401 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/1410.5401) |
| 161 | arXiv:1809.08887 |  |  | 3 | 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/1809.08887) |
| 162 | arXiv:1910.06360 |  |  | 3 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 163 | arXiv:2205.07324 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2205.07324) |
| 164 | arXiv:2212.08136 |  |  | 3 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.08136) |
| 165 | arXiv:2305.19466 |  |  | 3 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2305.19466) |
| 166 | arXiv:2402.01032 |  |  | 3 | sparse attention / KV-cache bandwidth reduction | [source](https://arxiv.org/abs/2402.01032) |
| 167 | arXiv:2404.02060 |  |  | 3 | Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2404.02060) |
| 168 | arXiv:2404.07904 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2404.07904) |
| 169 | arXiv:2407.01527 |  |  | 3 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化 | [source](https://arxiv.org/abs/2407.01527) |
| 170 | arXiv:2411.04330 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2411.04330) |
| 171 | arXiv:2506.05176 |  |  | 3 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2506.05176) |
| 172 | DOI:10.1145/3530811 |  |  | 3 | inference-systems | [source](https://doi.org/10.1145/3530811) |
| 173 | DOI:10.18653/v1/2023.emnlp-main.362 |  |  | 3 | inference-systems | [source](https://doi.org/10.18653/v1/2023.emnlp-main.362) |
| 174 | OpenReview:KG6aBfGi6e |  |  | 3 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=KG6aBfGi6e) |
| 175 | arXiv:2111.05754 |  |  | 3 |  | [source](https://arxiv.org/abs/2111.05754) |
| 176 | arXiv:2411.03312 |  |  | 3 |  | [source](https://arxiv.org/abs/2411.03312) |
| 177 | arXiv:2512.15489 |  |  | 3 |  | [source](https://arxiv.org/abs/2512.15489) |
| 178 | arXiv:1404.5997 |  |  | 2 | inference-systems, その他システム研究 | [source](https://arxiv.org/abs/1404.5997) |
| 179 | arXiv:1711.03016 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1711.03016) |
| 180 | arXiv:1811.03115 |  |  | 2 | inference-systems, 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/1811.03115) |
| 181 | arXiv:1906.04284 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/1906.04284) |
| 182 | arXiv:1912.12180 |  |  | 2 | training-memory-systems, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1912.12180) |
| 183 | arXiv:2005.14187 |  |  | 2 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 184 | arXiv:2009.12812 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2009.12812) |
| 185 | arXiv:2101.01321 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2101.01321) |
| 186 | arXiv:2103.02143 |  |  | 2 | CPU長文推論・近似注意, inference-systems | [source](https://arxiv.org/abs/2103.02143) |
| 187 | arXiv:2106.03764 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2106.03764) |
| 188 | arXiv:2109.11067 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2109.11067) |
| 189 | arXiv:2201.13425 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2201.13425) |
| 190 | arXiv:2205.11916 |  |  | 2 | Offload / Hierarchical Memory, inference-systems | [source](https://arxiv.org/abs/2205.11916) |
| 191 | arXiv:2207.10551 |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2207.10551) |
| 192 | arXiv:2212.12017 |  |  | 2 | 99-other-inference-systems, Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 193 | arXiv:2301.11233 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2301.11233) |
| 194 | arXiv:2303.16199 |  |  | 2 | inference-systems, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 195 | arXiv:2305.05252 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 196 | arXiv:2305.11206 |  |  | 2 | KVキャッシュ最適化／適応圧縮, inference-systems | [source](https://arxiv.org/abs/2305.11206) |
| 197 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 198 | arXiv:2308.06093 |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 199 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 200 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 201 | arXiv:2310.00746 |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 202 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 203 | arXiv:2311.09550 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 204 | arXiv:2311.17311 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 205 | arXiv:2312.03788 |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 206 | arXiv:2312.11918 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11918) |
| 207 | arXiv:2401.14112 |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 208 | arXiv:2402.03216 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 209 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 210 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 211 | arXiv:2403.07816 |  |  | 2 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2403.07816) |
| 212 | arXiv:2403.15447 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, inference-systems | [source](https://arxiv.org/abs/2403.15447) |
| 213 | arXiv:2404.05567 |  |  | 2 | MoE expert pruning / expert merging / redundancy-aware compression / global budget allocation, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2404.05567) |
| 214 | arXiv:2404.11018 |  |  | 2 | 07-kv-cache-optimization-compression, 13-sparse-attention | [source](https://arxiv.org/abs/2404.11018) |
| 215 | arXiv:2404.18416 |  |  | 2 | inference-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2404.18416) |
| 216 | arXiv:2405.16587 |  |  | 2 | Conditional Computation, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.16587) |
| 217 | arXiv:2406.04127 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2406.04127) |
| 218 | arXiv:2406.06025 |  |  | 2 | Long-context serving / KV cache benchmark, MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next | [source](https://arxiv.org/abs/2406.06025) |
| 219 | arXiv:2406.08673 |  |  | 2 | 大規模分散学習・整合学習基盤, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2406.08673) |
| 220 | arXiv:2406.18629 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2406.18629) |
| 221 | arXiv:2407.03211 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.03211) |
| 222 | arXiv:2407.10855 |  |  | 2 | kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.10855) |
| 223 | arXiv:2407.17789 |  |  | 2 | 14-agentic-inference-serving-runtime, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2407.17789) |
| 224 | arXiv:2409.15518 |  |  | 2 | inference-systems, multi-tenant LLM serving / latency attribution / fractional GPU sharing | [source](https://arxiv.org/abs/2409.15518) |
| 225 | arXiv:2409.17066 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline | [source](https://arxiv.org/abs/2409.17066) |
| 226 | arXiv:2410.00161 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.00161) |
| 227 | arXiv:2410.02713 |  |  | 2 | Sparse Attention / VLM Inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.02713) |
| 228 | arXiv:2410.05589 |  |  | 2 | 投機的デコード／動的LLMサービング／GPU空間多重化, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2410.05589) |
| 229 | arXiv:2410.10989 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, その他システム研究 | [source](https://arxiv.org/abs/2410.10989) |
| 230 | arXiv:2410.13835 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2410.13835) |
| 231 | arXiv:2410.17840 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.17840) |
| 232 | arXiv:2411.00918 |  |  | 2 | MoE圧縮 / expert merging / subspace alignment / SVD / adaptive clustering, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2411.00918) |
| 233 | arXiv:2411.10640 |  |  | 2 | Edge／on-device MoE, inference-systems | [source](https://arxiv.org/abs/2411.10640) |
| 234 | arXiv:2411.17309 |  |  | 2 | Offload / Hierarchical Memory, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.17309) |
| 235 | arXiv:2412.03603 |  |  | 2 | diffusion language model inference / KV cache / training-free acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.03603) |
| 236 | arXiv:2412.21023 |  |  | 2 | inference-systems, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2412.21023) |
| 237 | arXiv:2501.08219 |  |  | 2 | inference-systems, moe-parallelism-communication | [source](https://arxiv.org/abs/2501.08219) |
| 238 | arXiv:2501.10714 |  |  | 2 | Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2501.10714) |
| 239 | arXiv:2501.19324 |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2501.19324) |
| 240 | arXiv:2502.03261 |  |  | 2 | inference-systems, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://arxiv.org/abs/2502.03261) |
| 241 | arXiv:2502.04677 |  |  | 2 | KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2502.04677) |
| 242 | arXiv:2502.07864 |  |  | 2 | inference-systems, offload-hierarchical-memory | [source](https://arxiv.org/abs/2502.07864) |
| 243 | arXiv:2502.11147 |  |  | 2 | inference-systems, 長時間推論向けKVキャッシュ削除 | [source](https://arxiv.org/abs/2502.11147) |
| 244 | arXiv:2502.13652 |  |  | 2 | adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2502.13652) |
| 245 | arXiv:2502.14856 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, inference-systems | [source](https://arxiv.org/abs/2502.14856) |
| 246 | arXiv:2503.07154 |  |  | 2 | Diffusion LLM Inference, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2503.07154) |
| 247 | arXiv:2503.08415 |  |  | 2 | KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, other-inference-systems | [source](https://arxiv.org/abs/2503.08415) |
| 248 | arXiv:2503.24047 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2503.24047) |
| 249 | arXiv:2504.05299 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2504.05299) |
| 250 | arXiv:2504.10479 |  |  | 2 | 10-kv-cache-offload-recomputation, inference-systems | [source](https://arxiv.org/abs/2504.10479) |
| 251 | arXiv:2504.13914 |  |  | 2 | 推論ベンチマーク・推論大規模言語モデルのサービング評価, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2504.13914) |
| 252 | arXiv:2504.18154 |  |  | 2 | prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.18154) |
| 253 | arXiv:2505.06252 |  |  | 2 | kv-cache-offload-recomputation, その他システム研究 | [source](https://arxiv.org/abs/2505.06252) |
| 254 | arXiv:2505.09989 |  |  | 2 | inference-systems, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2505.09989) |
| 255 | arXiv:2505.14631 |  |  | 2 | Conditional Computation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2505.14631) |
| 256 | arXiv:2505.20353 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2505.20353) |
| 257 | arXiv:2506.01048 |  |  | 2 | llm-serving-scheduling-disaggregation, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://arxiv.org/abs/2506.01048) |
| 258 | arXiv:2506.09092 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems | [source](https://arxiv.org/abs/2506.09092) |
| 259 | arXiv:2506.15742 |  |  | 2 | Diffusion LLM Inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2506.15742) |
| 260 | arXiv:2506.23719 |  |  | 2 | agentic serving workload characterization / KV-cache / inference benchmarking, inference-systems | [source](https://arxiv.org/abs/2506.23719) |
| 261 | arXiv:2507.09942 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2507.09942) |
| 262 | arXiv:2508.01002 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2508.01002) |
| 263 | arXiv:2508.07101 |  |  | 2 | 13-sparse-attention, inference-systems | [source](https://arxiv.org/abs/2508.07101) |
| 264 | arXiv:2508.08712 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08712) |
| 265 | arXiv:2508.16712 |  |  | 2 | LLM serving scheduling / chunked prefill / MoE inference, llm-serving-systems | [source](https://arxiv.org/abs/2508.16712) |
| 266 | arXiv:2509.18883 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.18883) |
| 267 | arXiv:2509.23951 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.23951) |
| 268 | arXiv:2510.05373 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2510.05373) |
| 269 | arXiv:2510.15330 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.15330) |
| 270 | arXiv:2510.25741 |  |  | 2 | adaptive-expert-computation-compression, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://arxiv.org/abs/2510.25741) |
| 271 | arXiv:2511.16682 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2511.16682) |
| 272 | arXiv:2511.23404 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2511.23404) |
| 273 | arXiv:2512.05916 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.05916) |
| 274 | arXiv:2512.14142 |  |  | 2 | LLMサービング／スケジューリング／分離, other | [source](https://arxiv.org/abs/2512.14142) |
| 275 | arXiv:2512.20848 |  |  | 2 | PIM / Near-Data Acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.20848) |
| 276 | arXiv:2601.07526 |  |  | 2 | 14-agentic-inference-serving-runtime, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2601.07526) |
| 277 | arXiv:2601.10088 |  |  | 2 | hardware-accelerators, 分離型LLMサービング／予測型スケジューリング／KVメモリ認識型配置 | [source](https://arxiv.org/abs/2601.10088) |
| 278 | arXiv:2601.21351 |  |  | 2 | MoE serving / Attention-FFN disaggregation / analytical provisioning / hardware-aware deployment search, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2601.21351) |
| 279 | arXiv:2602.08005 |  |  | 2 | System-aware KV cache, kv-cache-memory-management | [source](https://arxiv.org/abs/2602.08005) |
| 280 | arXiv:2603.18016 |  |  | 2 | 05-speculative-decoding-moe, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://arxiv.org/abs/2603.18016) |
| 281 | arXiv:2605.04595 |  |  | 2 | KVキャッシュ制約下のLLMサービング・スケジューリング, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2605.04595) |
| 282 | arXiv:2606.17034 |  |  | 2 | KVキャッシュ再利用・選択的再計算・RAGキャッシュ編集, inference/14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2606.17034) |
| 283 | arXiv:2607.16673 |  |  | 2 | 99-other-inference-systems, その他の推論システム | [source](https://arxiv.org/abs/2607.16673) |
| 284 | DOI:10.1016/j.vlsi.2017.02.002 |  |  | 2 | 17-pim-near-data-acceleration, cpu-offload | [source](https://doi.org/10.1016/j.vlsi.2017.02.002) |
| 285 | DOI:10.1109/cvpr.2018.00286 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, hardware-accelerators | [source](https://doi.org/10.1109/cvpr.2018.00286) |
| 286 | DOI:10.1109/dac63849.2025.11133274 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory-kv-offload-cpu-gpu-attention | [source](https://doi.org/10.1109/dac63849.2025.11133274) |
| 287 | DOI:10.1109/hcs61935.2024.10664793 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hcs61935.2024.10664793) |
| 288 | DOI:10.1109/hoti66940.2025.00024 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, inference-systems | [source](https://doi.org/10.1109/hoti66940.2025.00024) |
| 289 | DOI:10.1109/hpca56546.2023.10071120 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://doi.org/10.1109/hpca56546.2023.10071120) |
| 290 | DOI:10.1109/iccad66269.2025.11240867 |  |  | 2 | 17-pim-near-data-acceleration, offload-hierarchical-memory | [source](https://doi.org/10.1109/iccad66269.2025.11240867) |
| 291 | DOI:10.1109/inpar.2012.6339596 |  |  | 2 | GPU architecture and tensor-computation orchestration, kernel-runtime-compilation | [source](https://doi.org/10.1109/inpar.2012.6339596) |
| 292 | DOI:10.1109/ipdpsw.2018.00091 |  |  | 2 | Inference Kernel / Determinism, hardware-accelerators | [source](https://doi.org/10.1109/ipdpsw.2018.00091) |
| 293 | DOI:10.1109/isca59077.2024.00036 |  |  | 2 | CXL memory pooling / KV cache offload / disaggregated memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/isca59077.2024.00036) |
| 294 | DOI:10.1109/isscc42614.2022.9731694 |  |  | 2 | 17-pim-near-data-acceleration, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/isscc42614.2022.9731694) |
| 295 | DOI:10.1109/jssc.2022.3200718 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/jssc.2022.3200718) |
| 296 | DOI:10.1109/lca.2025.3597323 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1109/lca.2025.3597323) |
| 297 | DOI:10.1109/micro61859.2024.00021 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/micro61859.2024.00021) |
| 298 | DOI:10.1109/mm.2024.3420728 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/mm.2024.3420728) |
| 299 | DOI:10.1109/tc.1985.6312218 |  |  | 2 | survey-speculative-decoding, 投機的復号 / 無損失復号高速化 | [source](https://doi.org/10.1109/tc.1985.6312218) |
| 300 | DOI:10.1109/tpds.2019.2928289 |  |  | 2 | inference-systems, moe-inference-expert-placement-caching | [source](https://doi.org/10.1109/tpds.2019.2928289) |
| 301 | DOI:10.1109/vlsitechnologyandcir46769.2022.9830277 |  |  | 2 | inference-systems, kv-cache-memory | [source](https://doi.org/10.1109/vlsitechnologyandcir46769.2022.9830277) |
| 302 | DOI:10.1137/0117039 |  |  | 2 | llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://doi.org/10.1137/0117039) |
| 303 | DOI:10.1145/1966445.1966473 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Expert Prefetch | [source](https://doi.org/10.1145/1966445.1966473) |
| 304 | DOI:10.1145/2491956.2462176 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/2491956.2462176) |
| 305 | DOI:10.1145/3092026 |  |  | 2 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching | [source](https://doi.org/10.1145/3092026) |
| 306 | DOI:10.1145/3211346.3211354 |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://doi.org/10.1145/3211346.3211354) |
| 307 | DOI:10.1145/3330345.3330351 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3330345.3330351) |
| 308 | DOI:10.1145/3437801.3441620 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3437801.3441620) |
| 309 | DOI:10.1145/3492321.3524270 |  |  | 2 | agent-runtime-sandbox-state-management, inference-systems | [source](https://doi.org/10.1145/3492321.3524270) |
| 310 | DOI:10.1145/3575693.3575724 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3575693.3575724) |
| 311 | DOI:10.1145/3582016.3582047 |  |  | 2 | 02-hardware-accelerators, kv-cache-optimization-compression | [source](https://doi.org/10.1145/3582016.3582047) |
| 312 | DOI:10.1145/3620665.3640365 |  |  | 2 | hardware-accelerators, inference-systems | [source](https://doi.org/10.1145/3620665.3640365) |
| 313 | DOI:10.1145/3632775.3662830 |  |  | 2 | inference-systems, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3632775.3662830) |
| 314 | DOI:10.1145/3676641.3716252 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3676641.3716252) |
| 315 | DOI:10.1145/3694715.3695963 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing | [source](https://doi.org/10.1145/3694715.3695963) |
| 316 | DOI:10.1145/3710848.3710871 |  |  | 2 | Inference Kernel / Determinism, Speculative decoding × MoE | [source](https://doi.org/10.1145/3710848.3710871) |
| 317 | DOI:10.1145/3727200.3727217 |  |  | 2 | inference-systems, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3727200.3727217) |
| 318 | DOI:10.1145/3768165 |  |  | 2 | Edge / On-device LLM Systems, speculative-decoding-moe | [source](https://doi.org/10.1145/3768165) |
| 319 | DOI:10.1145/3805475 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3805475) |
| 320 | DOI:10.1177/1094342005051521 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators | [source](https://doi.org/10.1177/1094342005051521) |
| 321 | DOI:10.18653/v1/2021.acl-long.334 |  |  | 2 | Adaptive Expert Computation / Compression, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://doi.org/10.18653/v1/2021.acl-long.334) |
| 322 | DOI:10.18653/v1/2024.acl-long.776 |  |  | 2 | KV Cache Optimization / Compression, inference-systems | [source](https://doi.org/10.18653/v1/2024.acl-long.776) |
| 323 | DOI:10.18653/v1/2024.findings-emnlp.266 |  |  | 2 | KV Cache Optimization / Compression, Long-context serving / KV cache benchmark | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.266) |
| 324 | DOI:10.18653/v1/2025.acl-long.531 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/2025.acl-long.531) |
| 325 | DOI:10.18653/v1/p18-1082 |  |  | 2 | Speculative Decoding, inference-systems | [source](https://doi.org/10.18653/v1/p18-1082) |
| 326 | DOI:10.3115/1075812.1075835 |  |  | 2 | Weight Quantization / Compression, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation | [source](https://doi.org/10.3115/1075812.1075835) |
| 327 | DOI:10.48550/arxiv.2410.13056 |  |  | 2 | 16-weight-quantization-compression, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.48550/arxiv.2410.13056) |
| 328 | DOI:10.52202/075280-1506 |  |  | 2 | early-exit-offloading-self-speculative-decoding, kv-cache-optimization-compression | [source](https://doi.org/10.52202/075280-1506) |
| 329 | DOI:10.52202/079017-0381 |  |  | 2 | early-exit-offloading-self-speculative-decoding, speculative-decoding | [source](https://doi.org/10.52202/079017-0381) |
| 330 | DOI:10.52202/085713-1380 |  |  | 2 | 99-other-inference-systems, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/085713-1380) |
| 331 | OpenReview:0LXotew9Du |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=0LXotew9Du) |
| 332 | OpenReview:B1l8BtlCb |  |  | 2 | inference-systems, speculative-decoding | [source](https://openreview.net/forum?id=B1l8BtlCb) |
| 333 | OpenReview:cJd1BgZ9CS |  |  | 2 | speculative-decoding, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://openreview.net/forum?id=cJd1BgZ9CS) |
| 334 | OpenReview:dXiGWqBoxaD |  |  | 2 | 07-kv-cache-optimization-compression, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=dXiGWqBoxaD) |
| 335 | OpenReview:FbhjirzvJG |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=FbhjirzvJG) |
| 336 | OpenReview:ho7ZUS1z8A |  |  | 2 | MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / atomic expert pruning / second-order pruning | [source](https://openreview.net/forum?id=ho7ZUS1z8A) |
| 337 | OpenReview:KeHes2SVxs |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://openreview.net/forum?id=KeHes2SVxs) |
| 338 | OpenReview:qCaq3jGb0S |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=qCaq3jGb0S) |
| 339 | OpenReview:rAcgDBdKnP |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=rAcgDBdKnP) |
| 340 | OpenReview:Uh17FiwF4q |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising | [source](https://openreview.net/forum?id=Uh17FiwF4q) |
| 341 | OpenReview:yeeIGM3N6w |  |  | 2 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency | [source](https://openreview.net/forum?id=yeeIGM3N6w) |
| 342 | OpenReview:zUYfbdNl1m |  |  | 2 | augmented LLM serving / KV cache management / predictive scheduling / vLLM, inference-systems | [source](https://openreview.net/forum?id=zUYfbdNl1m) |
| 343 | arXiv:1611.01578 |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 344 | arXiv:1712.07040 |  |  | 2 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1712.07040) |
| 345 | arXiv:1902.03383 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/1902.03383) |
| 346 | arXiv:1904.09675 |  |  | 2 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 347 | arXiv:1905.10650 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1905.10650) |
| 348 | arXiv:1908.09791 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1908.09791) |
| 349 | arXiv:1910.04732 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1910.04732) |
| 350 | arXiv:2009.07118 |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2009.07118) |
| 351 | arXiv:2010.15327 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2010.15327) |
| 352 | arXiv:2102.07831 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2102.07831) |
| 353 | arXiv:2110.04366 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.04366) |
| 354 | arXiv:2111.08566 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2111.08566) |
| 355 | arXiv:2203.03466 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2203.03466) |
| 356 | arXiv:2205.05131 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2205.05131) |
| 357 | arXiv:2207.12598 |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2207.12598) |
| 358 | arXiv:2210.06726 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2210.06726) |
| 359 | arXiv:2211.15089 |  |  | 2 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 360 | arXiv:2212.10403 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2212.10403) |
| 361 | arXiv:2302.09632 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.09632) |
| 362 | arXiv:2303.07129 |  |  | 2 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 363 | arXiv:2304.09433 |  |  | 2 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2304.09433) |
| 364 | arXiv:2305.00660 |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.00660) |
| 365 | arXiv:2305.10250 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 366 | arXiv:2305.14160 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 367 | arXiv:2305.18403 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.18403) |
| 368 | arXiv:2306.03805 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2306.03805) |
| 369 | arXiv:2306.13596 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 370 | arXiv:2309.14021 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.14021) |
| 371 | arXiv:2312.03134 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2312.03134) |
| 372 | arXiv:2402.00157 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.00157) |
| 373 | arXiv:2403.03187 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.03187) |
| 374 | arXiv:2403.16971 |  |  | 2 | other | [source](https://arxiv.org/abs/2403.16971) |
| 375 | arXiv:2404.05221 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2404.05221) |
| 376 | arXiv:2404.18322 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2404.18322) |
| 377 | arXiv:2405.06001 |  |  | 2 | survey-low-bit-llm | [source](https://arxiv.org/abs/2405.06001) |
| 378 | arXiv:2406.02924 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2406.02924) |
| 379 | arXiv:2406.15319 |  |  | 2 | KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ | [source](https://arxiv.org/abs/2406.15319) |
| 380 | arXiv:2407.11963 |  |  | 2 | serving-scheduling | [source](https://arxiv.org/abs/2407.11963) |
| 381 | arXiv:2408.00264 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2408.00264) |
| 382 | arXiv:2409.03215 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2409.03215) |
| 383 | arXiv:2410.02725 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2410.02725) |
| 384 | arXiv:2410.12388 |  |  | 2 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2410.12388) |
| 385 | arXiv:2410.19313 |  |  | 2 | diffusion-llm-inference / caching / low-precision | [source](https://arxiv.org/abs/2410.19313) |
| 386 | arXiv:2411.05902 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2411.05902) |
| 387 | arXiv:2412.12094 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2412.12094) |
| 388 | arXiv:2412.18547 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2412.18547) |
| 389 | arXiv:2501.03895 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2501.03895) |
| 390 | arXiv:2501.17399 |  |  | 2 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2501.17399) |
| 391 | arXiv:2502.03387 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.03387) |
| 392 | arXiv:2502.08691 |  |  | 2 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.08691) |
| 393 | arXiv:2502.14786 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.14786) |
| 394 | arXiv:2502.20586 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2502.20586) |
| 395 | arXiv:2504.00906 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2504.00906) |
| 396 | arXiv:2505.07686 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2505.07686) |
| 397 | arXiv:2505.20411 |  |  | 2 | other | [source](https://arxiv.org/abs/2505.20411) |
| 398 | arXiv:2505.23419 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2505.23419) |
| 399 | arXiv:2506.06122 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2506.06122) |
| 400 | arXiv:2506.22694 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2506.22694) |
| 401 | arXiv:2508.18224 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18224) |
| 402 | arXiv:2509.25140 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2509.25140) |
| 403 | arXiv:2510.20733 |  |  | 2 | multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2510.20733) |
| 404 | arXiv:2511.19269 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://arxiv.org/abs/2511.19269) |
| 405 | arXiv:2601.06007 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2601.06007) |
| 406 | arXiv:2603.08721 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2603.08721) |
| 407 | arXiv:2604.24432 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2604.24432) |
| 408 | arXiv:2605.09992 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2605.09992) |
| 409 | arXiv:2605.22791 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2605.22791) |
| 410 | DOI:10.1109/cvpr52733.2024.00913 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.1109/cvpr52733.2024.00913) |
| 411 | DOI:10.1109/iccad45719.2019.8942127 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/iccad45719.2019.8942127) |
| 412 | DOI:10.1109/isca45697.2020.00045 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isca45697.2020.00045) |
| 413 | DOI:10.1109/isca66397.2026.00021 |  |  | 2 | MoE expert offloading / predictive prefetch and cache management | [source](https://doi.org/10.1109/isca66397.2026.00021) |
| 414 | DOI:10.1109/isscc.2017.7870333 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isscc.2017.7870333) |
| 415 | DOI:10.1109/sc41405.2020.00073 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/sc41405.2020.00073) |
| 416 | DOI:10.1145/2541940.2541941 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2541940.2541941) |
| 417 | DOI:10.1145/2939672.2939785 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2939672.2939785) |
| 418 | DOI:10.1145/3241539.3241559 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3241539.3241559) |
| 419 | DOI:10.1145/3447993.3483249 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3447993.3483249) |
| 420 | DOI:10.1145/3510611 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3510611) |
| 421 | DOI:10.1145/3581791.3596831 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3581791.3596831) |
| 422 | DOI:10.1145/3710848.3710868 |  |  | 2 | Adaptive computation／cache-aware MoE | [source](https://doi.org/10.1145/3710848.3710868) |
| 423 | DOI:10.1162/tacl_a_00290 |  |  | 2 | inference-systems | [source](https://doi.org/10.1162/tacl_a_00290) |
| 424 | DOI:10.18653/v1/2020.acl-main.204 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.18653/v1/2020.acl-main.204) |
| 425 | DOI:10.18653/v1/2020.findings-emnlp.372 |  |  | 2 | 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/2020.findings-emnlp.372) |
| 426 | DOI:10.18653/v1/2022.findings-acl.177 |  |  | 2 | MoE compression / training-free expert merging / multimodal MoE routing | [source](https://doi.org/10.18653/v1/2022.findings-acl.177) |
| 427 | DOI:10.18653/v1/2023.emnlp-main.183 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.18653/v1/2023.emnlp-main.183) |
| 428 | DOI:10.18653/v1/2023.emnlp-main.907 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/2023.emnlp-main.907) |
| 429 | DOI:10.18653/v1/2024.emnlp-main.897 |  |  | 2 | kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.897) |
| 430 | DOI:10.18653/v1/2025.acl-long.671 |  |  | 2 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing | [source](https://doi.org/10.18653/v1/2025.acl-long.671) |
| 431 | DOI:10.18653/v1/d18-2012 |  |  | 2 | 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/d18-2012) |
| 432 | DOI:10.18653/v1/s17-2001 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/s17-2001) |
| 433 | DOI:10.64434/tml.20251026 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://doi.org/10.64434/tml.20251026) |
| 434 | OpenReview:7Ttk3RzDeu |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Ttk3RzDeu) |
| 435 | OpenReview:br4H61LOoI |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=br4H61LOoI) |
| 436 | OpenReview:CybBmzWBX0 |  |  | 2 | early-exit-offloading-self-speculative-decoding | [source](https://openreview.net/forum?id=CybBmzWBX0) |
| 437 | OpenReview:DOZiCWyK0N |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=DOZiCWyK0N) |
| 438 | OpenReview:ISqx8giekS |  |  | 2 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ISqx8giekS) |
| 439 | OpenReview:LWMS4pk2vK |  |  | 2 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=LWMS4pk2vK) |
| 440 | OpenReview:qrMo6R7lOS |  |  | 2 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=qrMo6R7lOS) |
| 441 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 442 | OpenReview:v3w2a7EInO |  |  | 2 | Conditional Computation | [source](https://openreview.net/forum?id=v3w2a7EInO) |
| 443 | OpenReview:YrycTjllL0 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://openreview.net/forum?id=YrycTjllL0) |
| 444 | arXiv:1710.09282 |  |  | 2 |  | [source](https://arxiv.org/abs/1710.09282) |
| 445 | arXiv:2011.00943 |  |  | 2 |  | [source](https://arxiv.org/abs/2011.00943) |
| 446 | arXiv:2104.06022 |  |  | 2 |  | [source](https://arxiv.org/abs/2104.06022) |
| 447 | arXiv:2208.11945 |  |  | 2 |  | [source](https://arxiv.org/abs/2208.11945) |
| 448 | arXiv:2302.04089 |  |  | 2 |  | [source](https://arxiv.org/abs/2302.04089) |
| 449 | arXiv:2310.01405 |  |  | 2 |  | [source](https://arxiv.org/abs/2310.01405) |
| 450 | arXiv:2401.12973 |  |  | 2 |  | [source](https://arxiv.org/abs/2401.12973) |
| 451 | arXiv:2402.18510 |  |  | 2 |  | [source](https://arxiv.org/abs/2402.18510) |
| 452 | arXiv:2404.08819 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.08819) |
| 453 | arXiv:2405.10825 |  |  | 2 |  | [source](https://arxiv.org/abs/2405.10825) |
| 454 | arXiv:2410.02367 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.02367) |
| 455 | arXiv:2410.20290 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.20290) |
| 456 | arXiv:2412.17747 |  |  | 2 |  | [source](https://arxiv.org/abs/2412.17747) |
| 457 | arXiv:2502.19732 |  |  | 2 |  | [source](https://arxiv.org/abs/2502.19732) |
| 458 | arXiv:2506.08027 |  |  | 2 |  | [source](https://arxiv.org/abs/2506.08027) |
| 459 | arXiv:cs/9809099 |  |  | 2 |  | [source](https://arxiv.org/abs/cs/9809099) |
| 460 | DOI:10.18653/v1/2020.acl-main.703 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2020.acl-main.703) |
| 461 | DOI:10.18653/v1/2026.findings-eacl.31 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2026.findings-eacl.31) |
| 462 | DOI:10.48550/arxiv.2304.08354 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2304.08354) |
| 463 | DOI:10.48550/arxiv.2410.11305 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2410.11305) |
| 464 | DOI:10.5555/3291168.3291211 |  |  | 2 |  | [source](https://doi.org/10.5555/3291168.3291211) |
| 465 | OpenReview:A1ztozypga |  |  | 2 |  | [source](https://openreview.net/forum?id=A1ztozypga) |
| 466 | OpenReview:i1uGbfHHpH |  |  | 2 |  | [source](https://openreview.net/forum?id=i1uGbfHHpH) |
| 467 | OpenReview:mXpq6ut8J3 |  |  | 2 |  | [source](https://openreview.net/forum?id=mXpq6ut8J3) |
| 468 | OpenReview:SJg7KhVKPH |  |  | 2 |  | [source](https://openreview.net/forum?id=SJg7KhVKPH) |
| 469 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 470 | arXiv:1205.6711 |  |  | 1 | kv-cache | [source](https://arxiv.org/abs/1205.6711) |
| 471 | arXiv:1211.3711 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1211.3711) |
| 472 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 473 | arXiv:1402.3511 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1402.3511) |
| 474 | arXiv:1410.0510 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1410.0510) |
| 475 | arXiv:1504.00325 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1504.00325) |
| 476 | arXiv:1506.02640 |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1506.02640) |
| 477 | arXiv:1508.03619 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1508.03619) |
| 478 | arXiv:1511.05641 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1511.05641) |
| 479 | arXiv:1511.07289 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1511.07289) |
| 480 | arXiv:1512.06890 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1512.06890) |
| 481 | arXiv:1602.01528 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1602.01528) |
| 482 | arXiv:1602.02830 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1602.02830) |
| 483 | arXiv:1603.05118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1603.05118) |
| 484 | arXiv:1604.01696 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1604.01696) |
| 485 | arXiv:1609.00076 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1609.00076) |
| 486 | arXiv:1610.02136 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1610.02136) |
| 487 | arXiv:1611.01576 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1611.01576) |
| 488 | arXiv:1611.07409 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1611.07409) |
| 489 | arXiv:1701.05517 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1701.05517) |
| 490 | arXiv:1703.03664 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1703.03664) |
| 491 | arXiv:1703.06114 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1703.06114) |
| 492 | arXiv:1704.04684 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/1704.04684) |
| 493 | arXiv:1705.05249 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1705.05249) |
| 494 | arXiv:1705.07565 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1705.07565) |
| 495 | arXiv:1706.09254 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1706.09254) |
| 496 | arXiv:1707.08514 |  |  | 1 | 10-kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1707.08514) |
| 497 | arXiv:1708.06519 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1708.06519) |
| 498 | arXiv:1709.04571 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1709.04571) |
| 499 | arXiv:1711.00123 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1711.00123) |
| 500 | arXiv:1711.04291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1711.04291) |

## Machine-readable

同じ割当は [worker-worklist-00.json](worker-worklist-00.json) にあります。

