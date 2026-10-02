# Scheduled worker :00 worklist

Worker: `scheduled-chat-00`  
Generated: `2026-10-02T07:11:18+00:00`

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
| 31 | research | arXiv:2506.07366 | MoE-GPS: Guidlines for Prediction Strategy for Dynamic Expert Duplication in MoE Load Balancing | [primary](https://www.semanticscholar.org/paper/b3d726f638aad791664917fc471740ff5c41eef9) | `papers/inference/99-other-inference-systems/2025-2506.07366-moe-gps-guidlines-for-prediction-strategy-for-dynamic-expert-duplication-in-moe-load-balancing.md` |
| 32 | research | DOI:10.1145/3806645.3807596 | Scaling Attention Beyond GPUs for LLM Inference | [primary](https://www.semanticscholar.org/paper/04f3ee7dd762dff9b6aad25bfb930e1984f74a09) | `papers/inference/99-other-inference-systems/2026-c3c79f91845d-scaling-attention-beyond-gpus-for-llm-inference.md` |
| 33 | research | arXiv:2509.12993 | HPIM: Heterogeneous Processing-In-Memory-based Accelerator for Large Language Models Inference | [primary](https://arxiv.org/abs/2509.12993) | `papers/inference/99-other-inference-systems/2025-2509.12993-hpim-heterogeneous-pim-llm-inference.md` |
| 34 | research | DOI:10.1145/3770855.3817626 | OrionInfer: Low-Overhead Parallelism Switching and Live Migration for Efficient LLM Serving | [primary](https://doi.org/10.1145/3770855.3817626) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-orioninfer-parallelism-switching-live-migration.md` |
| 35 | research | arXiv:2609.06940 | Unified AI Gateway: A Framework for Joint Model Routing and KV Cache Management | [primary](https://www.semanticscholar.org/paper/4affda1dbe50475a3be782dcc62391802b20986e) | `papers/inference/99-other-inference-systems/2026-2609.06940-unified-ai-gateway-a-framework-for-joint-model-routing-and-kv-cache-management.md` |
| 36 | research | arXiv:2609.22106 | PRQuant: Permutation Residual Quantization for Low-Overhead Inference | [primary](https://arxiv.org/abs/2609.22106) | `papers/inference/99-other-inference-systems/2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md` |
| 37 | research | arXiv:2608.22503 | Understanding the Synchronization Tax in GPU Scale-Up Domains | [primary](https://arxiv.org/abs/2608.22503) | `papers/inference/99-other-inference-systems/2026-2608.22503-understanding-the-synchronization-tax-in-gpu-scale-up-domains.md` |
| 38 | research | arXiv:2404.08763 |  | [primary](https://arxiv.org/abs/2404.08763) | `papers/inference/99-other-inference-systems/2024-2404.08763-paper.md` |
| 39 | research | DOI:10.1145/3816440.3818527 | L2Mersit: A Scaling-Free Sub-8-bit Data Format for On-Device Reliable Large Language Model Serving | [primary](https://doi.org/10.1145/3816440.3818527) | `papers/inference/99-other-inference-systems/2026-3bf3ae07c250-l2mersit-a-scaling-free-sub-8-bit-data-format-for-on-device-reliable-large-language-model-serving.md` |
| 40 | research | arXiv:2403.03853 | ShortGPT: Layers in Large Language Models are More Redundant Than You Expect | [primary](https://arxiv.org/abs/2403.03853) | `papers/inference/99-other-inference-systems/2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-expect.md` |
| 41 | research | arXiv:2606.30560 | TraceLab: Characterizing Coding Agent Workloads for LLM Serving | [primary](https://www.semanticscholar.org/paper/5d3da10e6ce527c3f636d25137ce1f37004d22f9) | `papers/inference/99-other-inference-systems/2026-2606.30560-tracelab-characterizing-coding-agent-workloads-for-llm-serving.md` |
| 42 | research | arXiv:2112.06905 | GLaM: Efficient Scaling of Language Models with Mixture-of-Experts | [primary](https://arxiv.org/abs/2112.06905) | `papers/inference/99-other-inference-systems/2021-2112.06905-glam-efficient-scaling-of-language-models-with-mixture-of-experts.md` |
| 43 | research | arXiv:2609.14850 | Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference | [primary](https://arxiv.org/abs/2609.14850) | `papers/inference/99-other-inference-systems/2026-2609.14850-self-orchestrating-language-models.md` |
| 44 | research | arXiv:2607.10987 | [AAFLOW+] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows | [primary](https://www.semanticscholar.org/paper/e45860ca84d523ee9b55d4824181233e7945d456) | `papers/inference/99-other-inference-systems/2026-2607.10987-aaflow-stateful-operator-abstraction-with-zero-copy-distributed-kv-cache-orchestration-for-multi-agent-workflows.md` |
| 45 | research | arXiv:2601.19139 | Native LLM and MLLM Inference at Scale on Apple Silicon | [primary](https://arxiv.org/abs/2601.19139) | `papers/inference/99-other-inference-systems/2026-2601.19139-native-llm-and-mllm-inference-at-scale-on-apple-silicon.md` |
| 46 | research | arXiv:2609.04875 | Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents | [primary](https://arxiv.org/abs/2609.04875) | `papers/inference/99-other-inference-systems/2026-2609.04875-forgetting-without-restarting-execution-state-unlearning-for-stateful-llm-agents.md` |
| 47 | research | arXiv:2512.22195 | MatKV: Trading Compute for Flash Storage in LLM Inference | [primary](https://arxiv.org/abs/2512.22195) | `papers/inference/99-other-inference-systems/2025-2512.22195-matkv-trading-compute-for-flash-storage-in-llm-inference.md` |
| 48 | research | arXiv:2502.09334 | ThunderServe: High-performance and Cost-efficient LLM Serving in Cloud Environments | [primary](https://arxiv.org/abs/2502.09334) | `papers/inference/99-other-inference-systems/2025-2502.09334-thunderserve-high-performance-and-cost-efficient-llm-serving-in-cloud-environments.md` |
| 49 | research | arXiv:2511.03475 | ContextPilot: Fast Long-Context Inference via Context Reuse | [primary](https://www.semanticscholar.org/paper/55e8ff688d13948dfbb496af1b565057f5ba5114) | `papers/inference/99-other-inference-systems/2025-2511.03475-contextpilot-fast-long-context-inference-via-context-reuse.md` |
| 50 | research | arXiv:2609.14864 | GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems | [primary](https://arxiv.org/abs/2609.14864) | `papers/inference/12-benchmarking-modeling-emulation/2026-2609.14864-gguf-metadata-llamacpp-throughput.md` |
| 51 | research | arXiv:2211.10017 | Who Says Elephants Can't Run: Bringing Large Scale MoE Models into Cloud Scale Production | [primary](https://arxiv.org/abs/2211.10017) | `papers/inference/99-other-inference-systems/2022-2211.10017-who-says-elephants-can-t-run-bringing-large-scale-moe-models-into-cloud-scale-production.md` |
| 52 | research | arXiv:2606.16352 | Communication-Efficient Verifiable Attention for LLM Inference | [primary](https://arxiv.org/abs/2606.16352) | `papers/inference/99-other-inference-systems/2026-2606.16352-communication-efficient-verifiable-attention-for-llm-inference.md` |
| 53 | research | arXiv:2609.06128 | Substrate-Portable Execution for Production LLM Workflows | [primary](https://arxiv.org/abs/2609.06128) | `papers/inference/99-other-inference-systems/2026-2609.06128-substrate-portable-production-llm-workflows.md` |
| 54 | research | arXiv:2511.10676 | Pre-Attention Expert Prediction and Prefetching for Mixture-of-Experts Large Language Models | [primary](https://arxiv.org/abs/2511.10676) | `papers/inference/99-other-inference-systems/2025-2511.10676-pre-attention-expert-prediction-and-prefetching-for-mixture-of-experts-large-language-models.md` |
| 55 | research | arXiv:2607.17415 | Transition-Aware Backend Dispatch for Edge LLM Inference | [primary](https://www.semanticscholar.org/paper/d338b6749faaf0cf77c1afd032c77f84257b9f3d) | `papers/inference/99-other-inference-systems/2026-2607.17415-transition-aware-backend-dispatch-for-edge-llm-inference.md` |
| 56 | research | arXiv:2608.04991 | RAC: Reference-Aware Activation Compression for Communication-Efficient Split LLM Inference | [primary](https://arxiv.org/abs/2608.04991) | `papers/inference/08-edge-on-device-llm-systems/2026-2608.04991-rac-reference-aware-activation-compression.md` |
| 57 | research | arXiv:2605.06676 | LKV: End-to-End Learning of Head-wise Budgets and Token Selection for LLM KV Cache Eviction | [primary](https://www.semanticscholar.org/paper/9dbefa4becfe4a6ae3decde6fabad3ab975cde52) | `papers/inference/99-other-inference-systems/2026-2605.06676-lkv-end-to-end-learning-of-head-wise-budgets-and-token-selection-for-llm-kv-cache-eviction.md` |
| 58 | research | arXiv:2602.11812 | Predicting LLM Output Length via Entropy-Guided Representations | [primary](https://arxiv.org/abs/2602.11812) | `papers/inference/99-other-inference-systems/2026-2602.11812-predicting-llm-output-length-via-entropy-guided-representations.md` |
| 59 | research | arXiv:2402.17762 | Massive Activations in Large Language Models | [primary](https://arxiv.org/abs/2402.17762) | `papers/inference/99-other-inference-systems/2024-2402.17762-massive-activations-in-large-language-models.md` |
| 60 | research | arXiv:2404.02258 | Mixture-of-Depths: Dynamically allocating compute in transformer-based language models | [primary](https://arxiv.org/abs/2404.02258) | `papers/inference/02-adaptive-expert-computation-compression/2024-2404.02258-mixture-of-depths-dynamic-compute.md` |
| 61 | research | arXiv:2605.26289 | Stateful Inference for Low-Latency Multi-Agent Tool Calling | [primary](https://arxiv.org/abs/2605.26289) | `papers/inference/99-other-inference-systems/2026-2605.26289-stateful-inference-for-low-latency-multi-agent-tool-calling.md` |
| 62 | research | arXiv:2609.12378 | An Open-Source End-to-End FHE Implementation for Privacy-Preserving Llama 3 8B Inference | [primary](https://arxiv.org/abs/2609.12378) | `papers/inference/99-other-inference-systems/2026-2609.12378-odin-fhe-privacy-preserving-llama-inference.md` |
| 63 | research | arXiv:2504.11750 | Characterizing and Optimizing LLM Inference Workloads on CPU-GPU Coupled Architectures | [primary](https://arxiv.org/abs/2504.11750) | `papers/inference/99-other-inference-systems/2025-2504.11750-characterizing-and-optimizing-llm-inference-workloads-on-cpu-gpu-coupled-architectures.md` |
| 64 | research | arXiv:2608.25431 | Here is a GIFT: Enforcing User Data Isolation in LLM Serving via GPU Information Flow Tracking | [primary](https://arxiv.org/abs/2608.25431) | `papers/inference/99-other-inference-systems/2026-2608.25431-here-is-a-gift-enforcing-user-data-isolation-in-llm-serving-via-gpu-information-flow-tracking.md` |
| 65 | research | arXiv:2405.12532 | PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference | [primary](https://arxiv.org/abs/2405.12532) | `papers/inference/99-other-inference-systems/2024-2405.12532-pyramidinfer-pyramid-kv-cache-compression-for-high-throughput-llm-inference.md` |
| 66 | research | arXiv:2609.18526 | Running an LLM Locally Doesn't Keep Prompts Private: They Survive in Allocator Memory After Inference | [primary](https://arxiv.org/abs/2609.18526) | `papers/inference/99-other-inference-systems/2026-2609.18526-local-llm-prompts-survive-allocator-memory-after-inference.md` |
| 67 | research | arXiv:2608.01526 | An Internet for the KV Cache: Rethinking Classical Infrastructure Boundaries in the LLM Inference Age | [primary](https://arxiv.org/abs/2608.01526) | `papers/inference/99-other-inference-systems/2026-2608.01526-an-internet-for-the-kv-cache-rethinking-classical-infrastructure-boundaries-in-the-llm-inference-age.md` |
| 68 | research | arXiv:2609.21450 | Understanding LLM Quantization through Activation-Guided Compensation and Orthogonal Residuals | [primary](https://www.semanticscholar.org/paper/4bc350d63aeade610b2ffccc236935ac34647a3d) | `papers/inference/99-other-inference-systems/2026-2609.21450-understanding-llm-quantization-through-activation-guided-compensation-and-orthogonal-residuals.md` |
| 69 | research | arXiv:2407.08454 | Model Tells You Where to Merge: Adaptive KV Cache Merging for LLMs on Long-Context Tasks | [primary](https://arxiv.org/abs/2407.08454) | `papers/inference/99-other-inference-systems/2024-2407.08454-model-tells-you-where-to-merge-adaptive-kv-cache-merging-for-llms-on-long-context-tasks.md` |
| 70 | research | arXiv:2101.03961 | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | [primary](https://arxiv.org/abs/2101.03961) | `papers/inference/99-other-inference-systems/2021-2101.03961-switch-transformers-scaling-to-trillion-parameter-models-with-simple-and-efficient-sparsity.md` |
| 71 | research | DOI:10.1145/3373376.3378530 | SwapAdvisor: Pushing Deep Learning Beyond the GPU Memory Limit via Smart Swapping | [primary](https://doi.org/10.1145/3373376.3378530) | `papers/inference/99-other-inference-systems/0000-4b209e34401e-swapadvisor-pushing-deep-learning-beyond-the-gpu-memory-limit-via-smart-swapping.md` |
| 72 | research | arXiv:2403.20306 | Towards Greener LLMs: Bringing Energy-Efficiency to the Forefront of LLM Inference | [primary](https://arxiv.org/abs/2403.20306) | `papers/inference/99-other-inference-systems/2024-2403.20306-towards-greener-llms-bringing-energy-efficiency-to-the-forefront-of-llm-inference.md` |
| 73 | research | DOI:10.18653/v1/2021.naacl-industry.15 | LightSeq: A High Performance Inference Library for Transformers | [primary](https://doi.org/10.18653/v1/2021.naacl-industry.15) | `papers/inference/99-other-inference-systems/0000-439132b7c6e4-lightseq-a-high-performance-inference-library-for-transformers.md` |
| 74 | research | DOI:10.1145/3600006.3613175 | Sia: Heterogeneity-aware, goodput-optimized ML-cluster scheduling | [primary](https://doi.org/10.1145/3600006.3613175) | `papers/inference/99-other-inference-systems/2026-2c2071afa90d-sia-heterogeneity-aware-goodput-optimized-ml-cluster-scheduling.md` |
| 75 | research | SemanticScholar:7945684818786fcb32cf92bace2566d7d6bc8945 | LegoOS: A Disseminated, Distributed OS for Hardware Resource Disaggregation | [primary](https://www.semanticscholar.org/paper/7945684818786fcb32cf92bace2566d7d6bc8945) | `papers/inference/99-other-inference-systems/2026-6793b18ad544-legoos-a-disseminated-distributed-os-for-hardware-resource-disaggregation.md` |
| 76 | research | DOI:10.1145/3341301.3359646 | PipeDream: generalized pipeline parallelism for DNN training | [primary](https://doi.org/10.1145/3341301.3359646) | `papers/inference/99-other-inference-systems/2026-ad68cc79ebe7-pipedream-generalized-pipeline-parallelism-for-dnn-training.md` |
| 77 | research | arXiv:2010.05680 | TurboTransformers: an efficient GPU serving system for transformer models | [primary](https://arxiv.org/abs/2010.05680) | `papers/inference/99-other-inference-systems/2020-2010.05680-turbotransformers-an-efficient-gpu-serving-system-for-transformer-models.md` |
| 78 | research | arXiv:2305.17888 | LLM-QAT: Data-Free Quantization Aware Training for Large Language Models | [primary](https://arxiv.org/abs/2305.17888) | `papers/inference/99-other-inference-systems/2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md` |
| 79 | research | arXiv:1805.02867 | Online normalizer calculation for softmax | [primary](https://arxiv.org/abs/1805.02867) | `papers/inference/99-other-inference-systems/2018-1805.02867-online-normalizer-calculation-for-softmax.md` |
| 80 | research | arXiv:2603.28458 | HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention | [primary](https://arxiv.org/abs/2603.28458) | `papers/inference/99-other-inference-systems/2026-2603.28458-hisa-efficient-hierarchical-indexing-for-fine-grained-sparse-attention.md` |
| 81 | research | arXiv:2503.00979 | Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs | [primary](https://arxiv.org/abs/2503.00979) | `papers/inference/99-other-inference-systems/2025-2503.00979-dialogue-without-limits-constant-sized-kv-caches-for-extended-responses-in-llms.md` |
| 82 | research | arXiv:2402.13720 | Ouroboros: Generating Longer Drafts Phrase by Phrase for Faster Speculative Decoding | [primary](https://arxiv.org/abs/2402.13720) | `papers/inference/99-other-inference-systems/2024-2402.13720-ouroboros-generating-longer-drafts-phrase-by-phrase-for-faster-speculative-decoding.md` |
| 83 | research | arXiv:2508.08448 | Towards Efficient and Practical GPU Multitasking in the Era of LLM | [primary](https://arxiv.org/abs/2508.08448) | `papers/inference/99-other-inference-systems/2025-2508.08448-towards-efficient-and-practical-gpu-multitasking-in-the-era-of-llm.md` |
| 84 | research | arXiv:2505.13109 | FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference | [primary](https://arxiv.org/abs/2505.13109) | `papers/inference/99-other-inference-systems/2025-2505.13109-freekv-boosting-kv-cache-retrieval-for-efficient-llm-inference.md` |
| 85 | research | arXiv:2406.15486 | SampleAttention: Near-Lossless Acceleration of Long Context LLM Inference with Adaptive Structured Sparse Attention | [primary](https://arxiv.org/abs/2406.15486) | `papers/inference/99-other-inference-systems/2024-2406.15486-sampleattention-near-lossless-acceleration-of-long-context-llm-inference-with-adaptive-structured-sparse-attention.md` |
| 86 | research | arXiv:2411.04975 | SuffixDecoding: A Model-Free Approach to Speeding Up Large Language Model Inference | [primary](https://arxiv.org/abs/2411.04975) | `papers/inference/99-other-inference-systems/2024-2411.04975-suffixdecoding-a-model-free-approach-to-speeding-up-large-language-model-inference.md` |
| 87 | research | arXiv:2506.20187 | Breaking the Boundaries of Long-Context LLM Inference: Adaptive KV Management on a Single Commodity GPU | [primary](https://arxiv.org/abs/2506.20187) | `papers/inference/99-other-inference-systems/2025-2506.20187-breaking-the-boundaries-of-long-context-llm-inference-adaptive-kv-management-on-a-single-commodity-gpu.md` |
| 88 | research | arXiv:2502.04420 | KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference | [primary](https://arxiv.org/abs/2502.04420) | `papers/inference/99-other-inference-systems/2025-2502.04420-kvtuner-sensitivity-aware-layer-wise-mixed-precision-kv-cache-quantization-for-efficient-and-nearly-lossless-llm-inferen.md` |
| 89 | research | arXiv:2507.09019 | On Evaluating Performance of LLM Inference Systems | [primary](https://arxiv.org/abs/2507.09019) | `papers/inference/99-other-inference-systems/2025-2507.09019-on-evaluating-performance-of-llm-inference-systems.md` |
| 90 | research | arXiv:2510.12357 | MoBiLE: Efficient Mixture-of-Experts Inference on Consumer GPU with Mixture of Big Little Experts | [primary](https://arxiv.org/abs/2510.12357) | `papers/inference/99-other-inference-systems/2025-2510.12357-mobile-efficient-mixture-of-experts-inference-on-consumer-gpu-with-mixture-of-big-little-experts.md` |
| 91 | research | arXiv:2404.00456 | QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs | [primary](https://arxiv.org/abs/2404.00456) | `papers/inference/99-other-inference-systems/2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md` |
| 92 | research | DOI:10.1109/micro61859.2024.00105 | Duplex: A Device for Large Language Models with Mixture of Experts, Grouped Query Attention, and Continuous Batching | [primary](https://doi.org/10.1109/micro61859.2024.00105) | `papers/inference/99-other-inference-systems/0000-0d72b2f1ac11-duplex-a-device-for-large-language-models-with-mixture-of-experts-grouped-query-attention-and-continuous-batching.md` |
| 93 | research | arXiv:2510.04371 | Speculative Actions: A Lossless Framework for Faster Agentic Systems | [primary](https://arxiv.org/abs/2510.04371) | `papers/inference/99-other-inference-systems/2025-2510.04371-speculative-actions-a-lossless-framework-for-faster-agentic-systems.md` |
| 94 | research | arXiv:2406.03482 | QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead | [primary](https://arxiv.org/abs/2406.03482) | `papers/inference/99-other-inference-systems/2024-2406.03482-qjl-1-bit-quantized-jl-transform-for-kv-cache-quantization-with-zero-overhead.md` |
| 95 | research | DOI:10.1145/3725273 | Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation | [primary](https://doi.org/10.1145/3725273) | `papers/inference/99-other-inference-systems/0000-f3a794c4a5ee-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-generation.md` |
| 96 | research | arXiv:2412.15803 | WebLLM: A High-Performance In-Browser LLM Inference Engine | [primary](https://arxiv.org/abs/2412.15803) | `papers/inference/99-other-inference-systems/2024-2412.15803-webllm-a-high-performance-in-browser-llm-inference-engine.md` |
| 97 | research | arXiv:2508.02520 | Huawei Cloud Model-as-a-Service on the CloudMatrix384 SuperPod | [primary](https://arxiv.org/abs/2508.02520) | `papers/inference/99-other-inference-systems/2025-2508.02520-huawei-cloud-model-as-a-service-on-the-cloudmatrix384-superpod.md` |
| 98 | research | arXiv:2407.09486 | ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving | [primary](https://arxiv.org/abs/2407.09486) | `papers/inference/99-other-inference-systems/2024-2407.09486-enova-autoscaling-towards-cost-effective-and-stable-serverless-llm-serving.md` |
| 99 | research | arXiv:1911.02972 | Blockwise Self-Attention for Long Document Understanding | [primary](https://arxiv.org/abs/1911.02972) | `papers/inference/99-other-inference-systems/2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md` |
| 100 | research | arXiv:2409.00142 | Dynamic Depth Decoding: Faster Speculative Decoding for LLMs | [primary](https://arxiv.org/abs/2409.00142) | `papers/inference/99-other-inference-systems/2024-2409.00142-dynamic-depth-decoding-faster-speculative-decoding-for-llms.md` |
| 101 | research | arXiv:2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | [primary](https://arxiv.org/abs/2508.18265) | `papers/inference/99-other-inference-systems/2025-2508.18265-internvl3-5-advancing-open-source-multimodal-models-in-versatility-reasoning-and-efficiency.md` |
| 102 | research | arXiv:2110.14895 | Pipeline Parallelism for Inference on Heterogeneous Edge Computing | [primary](https://arxiv.org/abs/2110.14895) | `papers/inference/99-other-inference-systems/2021-2110.14895-pipeline-parallelism-for-inference-on-heterogeneous-edge-computing.md` |
| 103 | research | arXiv:2509.17396 | EpiCache: Episodic KV Cache Management for Long-Term Conversation on Resource-Constrained Environments | [primary](https://arxiv.org/abs/2509.17396) | `papers/inference/99-other-inference-systems/2025-2509.17396-epicache-episodic-kv-cache-management-for-long-term-conversation-on-resource-constrained-environments.md` |
| 104 | research | arXiv:2602.02579 | ProphetKV: User-Query-Driven Selective Recomputation for Efficient KV Cache Reuse in Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2602.02579) | `papers/inference/99-other-inference-systems/2026-2602.02579-prophetkv-user-query-driven-selective-recomputation-for-efficient-kv-cache-reuse-in-retrieval-augmented-generation.md` |
| 105 | research | arXiv:2511.00606 | SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding | [primary](https://arxiv.org/abs/2511.00606) | `papers/inference/99-other-inference-systems/2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-decoding.md` |
| 106 | research | arXiv:2510.02758 | TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling | [primary](https://arxiv.org/abs/2510.02758) | `papers/inference/99-other-inference-systems/2025-2510.02758-tokenflow-responsive-llm-text-streaming-serving-under-request-burst-via-preemptive-scheduling.md` |
| 107 | research | arXiv:2606.13054 | TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization | [primary](https://arxiv.org/abs/2606.13054) | `papers/inference/99-other-inference-systems/2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post-training-quantization.md` |
| 108 | research | arXiv:2410.06916 | SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration | [primary](https://arxiv.org/abs/2410.06916) | `papers/inference/99-other-inference-systems/2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleration.md` |
| 109 | research | arXiv:2601.07891 | KVzap: Fast, Adaptive, and Faithful KV Cache Pruning | [primary](https://arxiv.org/abs/2601.07891) | `papers/inference/99-other-inference-systems/2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md` |
| 110 | research | arXiv:2606.26650 | CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs | [primary](https://arxiv.org/abs/2606.26650) | `papers/inference/99-other-inference-systems/2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md` |
| 111 | research | arXiv:2508.02401 | CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation | [primary](https://arxiv.org/abs/2508.02401) | `papers/inference/99-other-inference-systems/2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-before-generation.md` |
| 112 | research | DOI:10.1145/3773772 | Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving | [primary](https://doi.org/10.1145/3773772) | `papers/inference/99-other-inference-systems/0000-aa24341e05f1-mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md` |
| 113 | research | arXiv:2412.19442 | A Survey on Large Language Model Acceleration based on KV Cache Management | [primary](https://arxiv.org/abs/2412.19442) | `papers/inference/99-other-inference-systems/2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-management.md` |
| 114 | research | DOI:10.18653/v1/2023.emnlp-main.298 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | [primary](https://aclanthology.org/2023.emnlp-main.298/) | `papers/inference/99-other-inference-systems/0000-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-checkpoints.md` |
| 115 | research | arXiv:2502.12110 | A-Mem: Agentic Memory for LLM Agents | [primary](https://arxiv.org/abs/2502.12110) | `papers/inference/99-other-inference-systems/2025-2502.12110-a-mem-agentic-memory-for-llm-agents.md` |
| 116 | research | arXiv:2401.00134 | Unicron: Economizing Self-Healing LLM Training at Scale | [primary](https://arxiv.org/abs/2401.00134) | `papers/inference/99-other-inference-systems/2024-2401.00134-unicron-economizing-self-healing-llm-training-at-scale.md` |
| 117 | research | DOI:10.1145/3676641.3716009 | PAPI: Exploiting Dynamic Parallelism in Large Language Model Decoding with a Processing-In-Memory-Enabled Computing System | [primary](https://doi.org/10.1145/3676641.3716009) | `papers/inference/99-other-inference-systems/0000-71a3fb195e7b-papi-exploiting-dynamic-parallelism-in-large-language-model-decoding-with-a-processing-in-memory-enabled-computing-syste.md` |
| 118 | research | arXiv:2411.18424 | FastSwitch: Optimizing Context Switching Efficiency in Fairness-aware Large Language Model Serving | [primary](https://arxiv.org/abs/2411.18424) | `papers/inference/99-other-inference-systems/2024-2411.18424-fastswitch-optimizing-context-switching-efficiency-in-fairness-aware-large-language-model-serving.md` |
| 119 | research | arXiv:2503.18989 | A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models | [primary](https://arxiv.org/abs/2503.18989) | `papers/inference/99-other-inference-systems/2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-large-language-models.md` |
| 120 | research | arXiv:2511.20975 | Aragog: Just-in-Time Model Routing for Scalable Serving of Agentic Workflows | [primary](https://arxiv.org/abs/2511.20975) | `papers/inference/99-other-inference-systems/2025-2511.20975-aragog-just-in-time-model-routing-for-scalable-serving-of-agentic-workflows.md` |
| 121 | research | arXiv:2310.09832 | Merging Experts into One: Improving Computational Efficiency of Mixture of Experts | [primary](https://arxiv.org/abs/2310.09832) | `papers/inference/99-other-inference-systems/2023-2310.09832-merging-experts-into-one-improving-computational-efficiency-of-mixture-of-experts.md` |
| 122 | research | DOI:10.1145/3695053.3730999 | WindServe: Efficient Phase-Disaggregated LLM Serving with Stream-based Dynamic Scheduling | [primary](https://doi.org/10.1145/3695053.3730999) | `papers/inference/99-other-inference-systems/2025-8e0fd88d7ddc-windserve-efficient-phase-disaggregated-llm-serving-with-stream-based-dynamic-scheduling.md` |
| 123 | research | arXiv:2507.11417 | Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations | [primary](https://arxiv.org/abs/2507.11417) | `papers/inference/99-other-inference-systems/2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference-via-simulations.md` |
| 124 | research | arXiv:2504.12397 | Activated LoRA: Fine-tuned LLMs for Intrinsics | [primary](https://arxiv.org/abs/2504.12397) | `papers/inference/99-other-inference-systems/2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md` |
| 125 | research | arXiv:2505.13326 | Thinking Short and Right Over Thinking Long: Serving LLM Reasoning Efficiently and Accurately | [primary](https://arxiv.org/abs/2505.13326) | `papers/inference/99-other-inference-systems/2025-2505.13326-thinking-short-and-right-over-thinking-long-serving-llm-reasoning-efficiently-and-accurately.md` |
| 126 | research | arXiv:2503.07605 | SEAP: Training-free Sparse Expert Activation Pruning Unlock the Brainpower of Large Language Models | [primary](https://arxiv.org/abs/2503.07605) | `papers/inference/99-other-inference-systems/2025-2503.07605-seap-training-free-sparse-expert-activation-pruning-unlock-the-brainpower-of-large-language-models.md` |
| 127 | research | arXiv:2410.09426 | FlatQuant: Flatness Matters for LLM Quantization | [primary](https://arxiv.org/abs/2410.09426) | `papers/inference/99-other-inference-systems/2024-2410.09426-flatquant-flatness-matters-for-llm-quantization.md` |
| 128 | research | arXiv:2510.27656 | fabric-lib: RDMA Point-to-Point Communication for LLM Systems | [primary](https://arxiv.org/abs/2510.27656) | `papers/inference/99-other-inference-systems/2025-2510.27656-fabric-lib-rdma-point-to-point-communication-for-llm-systems.md` |
| 129 | research | arXiv:2507.08143 | Compactor: Calibrated Query-Agnostic KV Cache Compression with Approximate Leverage Scores | [primary](https://arxiv.org/abs/2507.08143) | `papers/inference/99-other-inference-systems/2025-2507.08143-compactor-calibrated-query-agnostic-kv-cache-compression-with-approximate-leverage-scores.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5522** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.5281/zenodo.12608602 |  |  | 29 | 16-weight-quantization-compression, Adaptive computation／cache-aware MoE, KV Cache Optimization / Compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, Other Inference Systems, Quantization × MoE × Offload, Sparse Attention, adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression, diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression, 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://doi.org/10.5281/zenodo.12608602) |
| 2 | DOI:10.1145/3620665.3640366 |  |  | 14 | 02-hardware-accelerators, 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, KVキャッシュ・注意アーキテクチャ, adaptive-expert-computation-compression, dynamic megakernel compilation and GPU task scheduling, hardware-accelerators, hierarchical-memory-kv-offload-cpu-gpu-attention, kernel-runtime-compilation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3620665.3640366) |
| 3 | DOI:10.18653/v1/d18-1259 |  |  | 12 | 07-kv-cache-optimization-compression, 13-sparse-attention, Adaptive Expert Computation / Compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング, 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://doi.org/10.18653/v1/d18-1259) |
| 4 | arXiv:2406.12793 |  |  | 12 | 07-kv-cache-optimization-compression, Edge / On-device LLM Systems, KV cache compression / sparse attention / long-context inference, KVキャッシュ退避／長文推論／KV選択／KV量子化, llm-serving-scheduling-disaggregation, その他システム研究 | [source](https://arxiv.org/abs/2406.12793) |
| 5 | DOI:10.1016/j.neucom.2023.127063 |  |  | 11 | 02-hardware-accelerators, GPU architecture and tensor-computation orchestration, KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, Sparse Attention, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://doi.org/10.1016/j.neucom.2023.127063) |
| 6 | arXiv:2304.01089 |  |  | 10 | Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 7 | arXiv:2407.12820 |  |  | 10 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://arxiv.org/abs/2407.12820) |
| 8 | arXiv:2305.05176 |  |  | 10 | LLM routing、hybrid inference、quality-aware model selection, RAGの入力圧縮と推論サーバーのメモリ管理を、要求単位のハードウェア認識型ルーティングで結び付ける研究。, adaptive-expert-computation-compression, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2305.05176) |
| 9 | arXiv:2506.12708 |  |  | 10 | 12-moe-parallelism-communication, KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, MoE serving / attention-MoE disaggregation / asynchronous inference, chunked-prefill scheduling / fairness / latency control, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2506.12708) |
| 10 | arXiv:2104.08691 |  |  | 9 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, many-adapter LLM serving / LoRA serving / inference scheduling, survey-long-context-serving, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2104.08691) |
| 11 | DOI:10.18653/v1/2024.acl-long.623 |  |  | 9 | 02-hardware-accelerators, 14-agentic-inference-serving-runtime, KV Cache Offload / Recomputation, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Offload / Hierarchical Memory, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, llm-serving-scheduling-disaggregation, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.18653/v1/2024.acl-long.623) |
| 12 | arXiv:2307.02486 |  |  | 9 | 10-kv-cache-offload-recomputation, KV Cache Offload / Recomputation, MoE serving / attention-MoE disaggregation / asynchronous inference, kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2307.02486) |
| 13 | arXiv:2607.02770 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://arxiv.org/abs/2607.02770) |
| 14 | arXiv:2405.16406 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 17-pim-near-data-acceleration, FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV cache quantization / rotation-based compression / MoE expert offloading / consumer local inference, kv-cache-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2405.16406) |
| 15 | DOI:10.48550/arxiv.2409.12186 |  |  | 9 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM, 推論エンジン／推論基盤, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.48550/arxiv.2409.12186) |
| 16 | arXiv:2309.12307 |  |  | 8 | Conditional Computation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference, KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ, cpu-offload, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, multi-tenant LoRA serving / CPU-assisted inference / rank-aware scheduling | [source](https://arxiv.org/abs/2309.12307) |
| 17 | arXiv:1808.08745 |  |  | 8 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 18 | arXiv:2404.19737 |  |  | 8 | 05-speculative-decoding-moe, 99-other-inference-systems, CPU推論、行列拡張、異種実行、ルーフライン最適化, Other Inference Systems / Lossless Parallel Decoding, adaptive-expert-computation-compression, 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2404.19737) |
| 19 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 20 | arXiv:2512.20856 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, PIM / Near-Data Acceleration, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2512.20856) |
| 21 | DOI:10.64434/tml.20250910 |  |  | 8 | Agentic Serving Benchmarking, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 22 | arXiv:2403.04643 |  |  | 8 | Conditional Computation, KV Cache Optimization / Compression, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, System-aware KV cache, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.04643) |
| 23 | arXiv:1809.09600 |  |  | 8 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 24 | arXiv:2009.14794 |  |  | 7 | CPU長文推論・近似注意, KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, kv-cache-offload-recomputation, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2009.14794) |
| 25 | arXiv:2401.00625 |  |  | 7 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, System-aware KV cache, distributed LLM inference / communication-aware serving, llm-serving-systems, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.00625) |
| 26 | arXiv:2406.00515 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, LLM inference kernel safety / CUDA symbolic execution / model-aware verification, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, kernel-runtime-compilation, serving-scheduling | [source](https://arxiv.org/abs/2406.00515) |
| 27 | OpenReview:WE_vluYUL-X |  |  | 7 | RAG runtime / distributed orchestration / agentic workflows, agentic serving / KV cache eviction / persistent multi-turn serving, agentic serving workload characterization / KV-cache / inference benchmarking, agentic workflow serving / workflow physical planning / adaptive serving, kv-cache-optimization-compression, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://openreview.net/forum?id=WE_vluYUL-X) |
| 28 | arXiv:2408.03326 |  |  | 7 | kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, low-bit VLM inference / microscaling / hardware-software co-design, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2408.03326) |
| 29 | OpenReview:chfJJYC3iL |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, Other Inference Systems / Lossless Parallel Decoding, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=chfJJYC3iL) |
| 30 | arXiv:2502.02770 |  |  | 7 | 07-kv-cache-optimization-compression, KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02770) |
| 31 | arXiv:2502.16982 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2502.16982) |
| 32 | arXiv:1607.06450 |  |  | 6 | LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 33 | arXiv:2501.14249 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, LLM Serving / Scheduling / Disaggregation, Other Inference Systems / Lossless Parallel Decoding, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2501.14249) |
| 34 | OpenReview:v8L0pN6EOi |  |  | 6 | KV Cache Optimization / Compression, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, reasoning-model compression / post-training pruning / calibration-data selection / causal intervention, speculative-decoding, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://openreview.net/forum?id=v8L0pN6EOi) |
| 35 | arXiv:2309.04255 |  |  | 6 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 36 | DOI:10.1145/3768628 |  |  | 6 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, System-aware KV cache, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3768628) |
| 37 | arXiv:2401.06118 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, Quantization × MoE × Offload, post-training quantization / ternary LLM / packed inference, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.06118) |
| 38 | arXiv:2412.03213 |  |  | 6 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2412.03213) |
| 39 | arXiv:2509.17765 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 40 | OpenReview:Bkg6RiCqY7 |  |  | 6 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 41 | arXiv:2311.04939 |  |  | 6 | KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.04939) |
| 42 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 43 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 44 | arXiv:2304.09145 |  |  | 5 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 45 | arXiv:2603.01175 |  |  | 5 | 10-kv-cache-offload-recomputation, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, flash-capacity-tier-inference, hardware-accelerators, offload-hierarchical-memory | [source](https://arxiv.org/abs/2603.01175) |
| 46 | DOI:10.1145/3695053.3731008 |  |  | 5 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 47 | arXiv:1811.02883 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM inference simulation / disaggregated serving / performance modeling, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://arxiv.org/abs/1811.02883) |
| 48 | arXiv:2212.10560 |  |  | 5 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2212.10560) |
| 49 | DOI:10.18653/v1/d17-1082 |  |  | 5 | Adaptive computation／cache-aware MoE, Conditional Computation, MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, sparse attention / learned context ranking / long-context LLM inference | [source](https://doi.org/10.18653/v1/d17-1082) |
| 50 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 51 | arXiv:2401.03868 |  |  | 5 | LLM inference surveys、roofline performance analysis, hierarchical-memory, kv-cache-memory | [source](https://arxiv.org/abs/2401.03868) |
| 52 | arXiv:2504.07491 |  |  | 5 | 11-llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2504.07491) |
| 53 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 5 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 54 | OpenReview:uccHPGDlao |  |  | 5 | 05-speculative-decoding-moe, Speculative decoding × MoE, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 55 | DOI:10.18653/v1/n19-1246 |  |  | 5 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.18653/v1/n19-1246) |
| 56 | arXiv:1805.06085 |  |  | 4 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, cpu-ssd-offload, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1805.06085) |
| 57 | arXiv:2210.11416 |  |  | 4 | Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 58 | arXiv:2402.14905 |  |  | 4 | 10-kv-cache-offload-recomputation, kv-cache-optimization-compression, offload-hierarchical-memory, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2402.14905) |
| 59 | arXiv:2509.00579 |  |  | 4 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design, Quantization × MoE × Offload, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2509.00579) |
| 60 | DOI:10.1145/3732941 |  |  | 4 | LLM Serving / Scheduling / Disaggregation, dynamic-pd-disaggregation, llm-serving-scheduling-disaggregation, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3732941) |
| 61 | DOI:10.48550/arxiv.2404.15159 |  |  | 4 | Adaptive Expert Computation / Compression, MoE-LoRA / パラメータ効率的微調整 / マージ可能アダプタ / ルータ不要自己ルーティング, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, survey-low-bit-llm | [source](https://doi.org/10.48550/arxiv.2404.15159) |
| 62 | OpenReview:L4uaAR4ArM |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, speculative-decoding | [source](https://openreview.net/forum?id=L4uaAR4ArM) |
| 63 | OpenReview:z5uVAKwmjf |  |  | 4 | 14-agentic-inference-serving-runtime, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, LLMサービング／自動スケーリング／広域ルーティング, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=z5uVAKwmjf) |
| 64 | DOI:10.1109/mm.2024.3375352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, Offload / Hierarchical Memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/mm.2024.3375352) |
| 65 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 66 | arXiv:2512.19849 |  |  | 4 | Speculative decoding × MoE, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2512.19849) |
| 67 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 68 | arXiv:2402.06082 |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 69 | arXiv:2506.06266 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2506.06266) |
| 70 | arXiv:2602.02276 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2602.02276) |
| 71 | DOI:10.1109/hpca53966.2022.00082 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, kv-cache-memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca53966.2022.00082) |
| 72 | DOI:10.1109/lca.2026.3705817 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3705817) |
| 73 | DOI:10.1109/sc41406.2024.00094 |  |  | 3 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1109/sc41406.2024.00094) |
| 74 | DOI:10.1145/3458864.3467882 |  |  | 3 | Edge／on-device MoE, LLMサービング・スケジューリング・分離実行, other-inference-systems | [source](https://doi.org/10.1145/3458864.3467882) |
| 75 | DOI:10.1145/3630106.3658542 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3630106.3658542) |
| 76 | DOI:10.1145/3725843.3756121 |  |  | 3 | PIM / Near-Data Acceleration, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756121) |
| 77 | DOI:10.1145/3779212.3790187 |  |  | 3 | MoE expert offloading / predictive prefetch and cache management, hierarchical-memory-kv-offload-cpu-gpu-attention, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.1145/3779212.3790187) |
| 78 | DOI:10.52202/075280-2279 |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, other-inference-systems | [source](https://doi.org/10.52202/075280-2279) |
| 79 | OpenReview:1YDeZU8Lt5 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=1YDeZU8Lt5) |
| 80 | OpenReview:CS2JWaziYr |  |  | 3 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=CS2JWaziYr) |
| 81 | OpenReview:rJl-b3RcF7 |  |  | 3 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=rJl-b3RcF7) |
| 82 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 83 | arXiv:2209.13258 |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 84 | arXiv:2502.02617 |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02617) |
| 85 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 86 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 87 | DOI:10.1145/3620665.3640383 |  |  | 3 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, serving-scheduling | [source](https://doi.org/10.1145/3620665.3640383) |
| 88 | DOI:10.1145/3779212.3790226 |  |  | 3 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory | [source](https://doi.org/10.1145/3779212.3790226) |
| 89 | DOI:10.18653/v1/2021.naacl-main.365 |  |  | 3 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference | [source](https://doi.org/10.18653/v1/2021.naacl-main.365) |
| 90 | DOI:10.18653/v1/d19-1454 |  |  | 3 | Conditional Computation, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/d19-1454) |
| 91 | DOI:10.57967/hf/2497 |  |  | 3 | KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, adaptive-expert-computation-compression | [source](https://doi.org/10.57967/hf/2497) |
| 92 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 93 | OpenReview:MaYzugDmQV |  |  | 3 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 94 | OpenReview:rkgNKkHtvB |  |  | 3 | 10-kv-cache-offload-recomputation, dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://openreview.net/forum?id=rkgNKkHtvB) |
| 95 | arXiv:2606.04101 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2606.04101) |
| 96 | DOI:10.18653/v1/p19-1102 |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference | [source](https://doi.org/10.18653/v1/p19-1102) |
| 97 | OpenReview:KG6aBfGi6e |  |  | 3 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=KG6aBfGi6e) |
| 98 | arXiv:1905.05702 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Sparse Attention | [source](https://arxiv.org/abs/1905.05702) |
| 99 | arXiv:2104.07012 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 100 | arXiv:2305.05252 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 101 | arXiv:2306.02561 |  |  | 2 | LLM routing、hybrid inference、quality-aware model selection, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 102 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 103 | arXiv:2307.08072 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 104 | arXiv:2308.07107 |  |  | 2 | KV cache compression / sparse attention / long-context inference, serving-scheduling | [source](https://arxiv.org/abs/2308.07107) |
| 105 | arXiv:2309.05463 |  |  | 2 | survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 106 | arXiv:2309.09558 |  |  | 2 | offload-hierarchical-memory, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://arxiv.org/abs/2309.09558) |
| 107 | arXiv:2309.11235 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2309.11235) |
| 108 | arXiv:2309.15531 |  |  | 2 | KV cache quantization / long-context inference / activation compression, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.15531) |
| 109 | arXiv:2310.02226 |  |  | 2 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 110 | arXiv:2310.08041 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2310.08041) |
| 111 | arXiv:2311.01635 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.01635) |
| 112 | arXiv:2311.10122 |  |  | 2 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference | [source](https://arxiv.org/abs/2311.10122) |
| 113 | arXiv:2311.17311 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 114 | arXiv:2312.03788 |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 115 | arXiv:2312.07987 |  |  | 2 | conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2312.07987) |
| 116 | arXiv:2312.14852 |  |  | 2 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 117 | arXiv:2401.03462 |  |  | 2 | 07-kv-キャッシュ-optimization-compression, KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2401.03462) |
| 118 | arXiv:2401.12522 |  |  | 2 | speculative-decoding, 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/2401.12522) |
| 119 | arXiv:2401.14112 |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 120 | arXiv:2402.02716 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2402.02716) |
| 121 | arXiv:2402.09025 |  |  | 2 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 122 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 123 | arXiv:2402.14762 |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 124 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 125 | arXiv:2403.05525 |  |  | 2 | Quantization × MoE × Offload, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 126 | arXiv:2403.09032 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 127 | arXiv:2403.14123 |  |  | 2 | moe-parallelism-communication, offload-hierarchical-memory | [source](https://arxiv.org/abs/2403.14123) |
| 128 | arXiv:2404.07972 |  |  | 2 | 14-agentic-inference-serving-runtime, KVキャッシュオフロード・再計算 | [source](https://arxiv.org/abs/2404.07972) |
| 129 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 130 | arXiv:2405.11530 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2405.11530) |
| 131 | arXiv:2405.21075 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention | [source](https://arxiv.org/abs/2405.21075) |
| 132 | arXiv:2406.03736 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2406.03736) |
| 133 | arXiv:2406.04594 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.04594) |
| 134 | arXiv:2406.11612 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2406.11612) |
| 135 | arXiv:2406.14963 |  |  | 2 | kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2406.14963) |
| 136 | arXiv:2406.18820 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18820) |
| 137 | arXiv:2407.04014 |  |  | 2 | llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 138 | arXiv:2407.09141 |  |  | 2 | 06-moe-quantization-compression, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.09141) |
| 139 | arXiv:2407.11239 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2407.11239) |
| 140 | arXiv:2407.17789 |  |  | 2 | 14-agentic-inference-serving-runtime, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2407.17789) |
| 141 | arXiv:2408.15881 |  |  | 2 | Speculative decoding × MoE, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2408.15881) |
| 142 | arXiv:2409.09071 |  |  | 2 | on-device LLM / heterogeneous inference / NPU offloading, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://arxiv.org/abs/2409.09071) |
| 143 | arXiv:2409.17422 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2409.17422) |
| 144 | arXiv:2410.00161 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.00161) |
| 145 | arXiv:2410.06511 |  |  | 2 | その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/2410.06511) |
| 146 | arXiv:2410.10989 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, その他システム研究 | [source](https://arxiv.org/abs/2410.10989) |
| 147 | arXiv:2410.14720 |  |  | 2 | MoE compression / expert pruning / neuron-level recombination / expert reconstruction, System-aware KV cache | [source](https://arxiv.org/abs/2410.14720) |
| 148 | arXiv:2410.20650 |  |  | 2 | kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2410.20650) |
| 149 | arXiv:2411.00918 |  |  | 2 | MoE圧縮 / expert merging / subspace alignment / SVD / adaptive clustering, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2411.00918) |
| 150 | arXiv:2411.04468 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2411.04468) |
| 151 | arXiv:2411.04996 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 152 | arXiv:2411.15100 |  |  | 2 | kv-cache-optimization-compression, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.15100) |
| 153 | arXiv:2412.03603 |  |  | 2 | diffusion language model inference / KV cache / training-free acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.03603) |
| 154 | arXiv:2412.12639 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2412.12639) |
| 155 | arXiv:2412.16545 |  |  | 2 | 10-kv-cache-offload-recomputation, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2412.16545) |
| 156 | arXiv:2501.12370 |  |  | 2 | MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://arxiv.org/abs/2501.12370) |
| 157 | arXiv:2502.03461 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2502.03461) |
| 158 | arXiv:2502.07861 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.07861) |
| 159 | arXiv:2502.11946 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.11946) |
| 160 | arXiv:2502.16880 |  |  | 2 | Speculative decoding × MoE, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2502.16880) |
| 161 | arXiv:2503.01586 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2503.01586) |
| 162 | arXiv:2503.08415 |  |  | 2 | KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, other-inference-systems | [source](https://arxiv.org/abs/2503.08415) |
| 163 | arXiv:2503.18773 |  |  | 2 | KV Cache Offload / Recomputation, batch inference / event-driven runtime / MoE serving / offload | [source](https://arxiv.org/abs/2503.18773) |
| 164 | arXiv:2503.24358 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, System-aware KV cache | [source](https://arxiv.org/abs/2503.24358) |
| 165 | arXiv:2504.06214 |  |  | 2 | llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2504.06214) |
| 166 | arXiv:2504.12216 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, 拡散型LLM推論・鍵値キャッシュ・疎注意・動的破棄 | [source](https://arxiv.org/abs/2504.12216) |
| 167 | arXiv:2504.16054 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2504.16054) |
| 168 | arXiv:2504.17307 |  |  | 2 | KV Cache Offload / Recomputation, LLMサービング／スケジューリング／分離実行 | [source](https://arxiv.org/abs/2504.17307) |
| 169 | arXiv:2504.20101 |  |  | 2 | llm-serving-scheduling-disaggregation, 異種GPUサービング・分散推論・パイプライン並列・動的ルーティング | [source](https://arxiv.org/abs/2504.20101) |
| 170 | arXiv:2505.06708 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2505.06708) |
| 171 | arXiv:2505.14681 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2505.14681) |
| 172 | arXiv:2505.21411 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2505.21411) |
| 173 | arXiv:2506.13585 |  |  | 2 | kv-cache-reuse-position-independent-caching, speculative-decoding | [source](https://arxiv.org/abs/2506.13585) |
| 174 | arXiv:2507.02770 |  |  | 2 | GPU機密計算の性能評価、LLMサービング、KVキャッシュ退避、機密マルチGPU基盤, confidential inference / trusted execution environment / split inference / differential privacy | [source](https://arxiv.org/abs/2507.02770) |
| 175 | arXiv:2507.11948 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, kernel-runtime-compilation | [source](https://arxiv.org/abs/2507.11948) |
| 176 | arXiv:2507.18071 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2507.18071) |
| 177 | arXiv:2508.02193 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2508.02193) |
| 178 | arXiv:2508.08438 |  |  | 2 | LLMサービング・接頭辞キャッシュ・マルチテナント隔離, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08438) |
| 179 | arXiv:2508.16653 |  |  | 2 | 低ビット疎推論／GPUカーネル／エッジ推論, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2508.16653) |
| 180 | arXiv:2508.18298 |  |  | 2 | kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18298) |
| 181 | arXiv:2509.18883 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.18883) |
| 182 | arXiv:2509.23951 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.23951) |
| 183 | arXiv:2510.03293 |  |  | 2 | Expert Prefetch, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.03293) |
| 184 | arXiv:2510.08544 |  |  | 2 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.08544) |
| 185 | arXiv:2510.17483 |  |  | 2 | adaptive-expert-computation-compression, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2510.17483) |
| 186 | arXiv:2511.05502 |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2511.05502) |
| 187 | arXiv:2511.20048 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2511.20048) |
| 188 | arXiv:2512.01644 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2512.01644) |
| 189 | arXiv:2512.07647 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.07647) |
| 190 | arXiv:2512.16473 |  |  | 2 | Edge／on-device MoE, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.16473) |
| 191 | arXiv:2601.02872 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://arxiv.org/abs/2601.02872) |
| 192 | arXiv:2601.09527 |  |  | 2 | LLMサービング・スケジューリング・分離実行, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://arxiv.org/abs/2601.09527) |
| 193 | arXiv:2601.19092 |  |  | 2 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム, dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2601.19092) |
| 194 | arXiv:2602.02599 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2602.02599) |
| 195 | arXiv:2602.21224 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2602.21224) |
| 196 | arXiv:2603.18016 |  |  | 2 | 05-speculative-decoding-moe, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://arxiv.org/abs/2603.18016) |
| 197 | arXiv:2604.15409 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2604.15409) |
| 198 | arXiv:2606.03928 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2606.03928) |
| 199 | arXiv:2607.02980 |  |  | 2 | 07-kv-cache-optimization-compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2607.02980) |
| 200 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 201 | DOI:10.1109/dac63849.2025.11133274 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory-kv-offload-cpu-gpu-attention | [source](https://doi.org/10.1109/dac63849.2025.11133274) |
| 202 | DOI:10.1109/hcs61935.2024.10664793 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hcs61935.2024.10664793) |
| 203 | DOI:10.1109/hpca56546.2023.10071120 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://doi.org/10.1109/hpca56546.2023.10071120) |
| 204 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 2 | moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 205 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 206 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 207 | DOI:10.1109/lca.2025.3597323 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1109/lca.2025.3597323) |
| 208 | DOI:10.1109/mm.2023.3256384 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2023.3256384) |
| 209 | DOI:10.1109/mm.2025.3592688 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, moe-parallelism-communication | [source](https://doi.org/10.1109/mm.2025.3592688) |
| 210 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 211 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 212 | DOI:10.1145/224056.224064 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/224056.224064) |
| 213 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 214 | DOI:10.1145/3352460.3358302 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3352460.3358302) |
| 215 | DOI:10.1145/3453483.3454083 |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 216 | DOI:10.1145/3503222.3507738 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3503222.3507738) |
| 217 | DOI:10.1145/3552326.3587438 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.1145/3552326.3587438) |
| 218 | DOI:10.1145/3575693.3575754 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3575693.3575754) |
| 219 | DOI:10.1145/3591300 |  |  | 2 | GPUカーネル融合／SwiGLU／LLM推論ランタイム, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://doi.org/10.1145/3591300) |
| 220 | DOI:10.1145/3620665.3640410 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620665.3640410) |
| 221 | DOI:10.1145/3627703.3629578 |  |  | 2 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, serving-scheduling | [source](https://doi.org/10.1145/3627703.3629578) |
| 222 | DOI:10.1145/3649506 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, Offload / Hierarchical Memory | [source](https://doi.org/10.1145/3649506) |
| 223 | DOI:10.1145/3669940.3707231 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/3669940.3707231) |
| 224 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 225 | DOI:10.1145/3725843.3756041 |  |  | 2 | GPU architecture and tensor-computation orchestration, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://doi.org/10.1145/3725843.3756041) |
| 226 | DOI:10.1145/3731569.3764829 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3731569.3764829) |
| 227 | DOI:10.1145/3769102.3770608 |  |  | 2 | 05-speculative-decoding-moe, Edge / On-device LLM Systems | [source](https://doi.org/10.1145/3769102.3770608) |
| 228 | DOI:10.1145/3779212.3790246 |  |  | 2 | Edge / On-device LLM Systems, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3779212.3790246) |
| 229 | DOI:10.1177/1094342005051521 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators | [source](https://doi.org/10.1177/1094342005051521) |
| 230 | DOI:10.1609/aaai.v40i36.40255 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.1609/aaai.v40i36.40255) |
| 231 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 2 | Speculative Decoding, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 232 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 233 | DOI:10.18653/v1/2025.acl-long.531 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/2025.acl-long.531) |
| 234 | DOI:10.18653/v1/p19-1355 |  |  | 2 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.18653/v1/p19-1355) |
| 235 | DOI:10.48550/arxiv.2410.13056 |  |  | 2 | 16-weight-quantization-compression, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.48550/arxiv.2410.13056) |
| 236 | DOI:10.52202/068431-0805 |  |  | 2 | 07-kv-cache-optimization-compression, other-inference-systems | [source](https://doi.org/10.52202/068431-0805) |
| 237 | DOI:10.52202/075280-1506 |  |  | 2 | early-exit-offloading-self-speculative-decoding, kv-cache-optimization-compression | [source](https://doi.org/10.52202/075280-1506) |
| 238 | DOI:10.52202/079017-3180 |  |  | 2 | adaptive-expert-computation-compression, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.52202/079017-3180) |
| 239 | OpenReview:0fJfVOSUra |  |  | 2 | 11-llm-serving-scheduling-disaggregation, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://openreview.net/forum?id=0fJfVOSUra) |
| 240 | OpenReview:acJ3vdFljk |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=acJ3vdFljk) |
| 241 | OpenReview:dwPdYFqVWO |  |  | 2 | Speculative decoding × MoE, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://openreview.net/forum?id=dwPdYFqVWO) |
| 242 | OpenReview:FbhjirzvJG |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=FbhjirzvJG) |
| 243 | OpenReview:HklBjCEKvH |  |  | 2 | Speculative Decoding, other-inference-systems | [source](https://openreview.net/forum?id=HklBjCEKvH) |
| 244 | OpenReview:JZfg6wGi6g |  |  | 2 | KV Cache Optimization / Compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=JZfg6wGi6g) |
| 245 | OpenReview:NGPmH3vbAA_ |  |  | 2 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=NGPmH3vbAA_) |
| 246 | OpenReview:R7fv5NWfMm |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=R7fv5NWfMm) |
| 247 | OpenReview:SFN6Wm7YBI |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=SFN6Wm7YBI) |
| 248 | OpenReview:xdNAVP7TGy |  |  | 2 | kv-cache-offload-recomputation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://openreview.net/forum?id=xdNAVP7TGy) |
| 249 | arXiv:1511.06297 |  |  | 2 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1511.06297) |
| 250 | arXiv:2311.15436 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2311.15436) |
| 251 | arXiv:2403.05676 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2403.05676) |
| 252 | arXiv:2405.14852 |  |  | 2 | survey-low-bit-llm | [source](https://arxiv.org/abs/2405.14852) |
| 253 | arXiv:2409.01366 |  |  | 2 | Edge／on-device MoE | [source](https://arxiv.org/abs/2409.01366) |
| 254 | arXiv:2412.00876 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.00876) |
| 255 | arXiv:2511.05814 |  |  | 2 | Edge／on-device MoE | [source](https://arxiv.org/abs/2511.05814) |
| 256 | arXiv:2603.13606 |  |  | 2 | distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2603.13606) |
| 257 | DOI:10.1109/cstic55103.2022.9856846 |  |  | 2 | 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1109/cstic55103.2022.9856846) |
| 258 | DOI:10.1109/infocom53939.2023.10228874 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1109/infocom53939.2023.10228874) |
| 259 | DOI:10.1145/3579371.3589351 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3 | [source](https://doi.org/10.1145/3579371.3589351) |
| 260 | DOI:10.1145/3725843.3756118 |  |  | 2 | low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3725843.3756118) |
| 261 | DOI:10.14778/3626292.3626303 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.14778/3626292.3626303) |
| 262 | DOI:10.18653/v1/2024.emnlp-main.897 |  |  | 2 | kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.897) |
| 263 | DOI:10.18653/v1/2025.acl-long.671 |  |  | 2 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing | [source](https://doi.org/10.18653/v1/2025.acl-long.671) |
| 264 | DOI:10.18653/v1/2026.findings-acl.1655 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2026.findings-acl.1655) |
| 265 | OpenReview:7zNYY1E2fq |  |  | 2 | KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論 | [source](https://openreview.net/forum?id=7zNYY1E2fq) |
| 266 | OpenReview:P0GOk5wslg |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=P0GOk5wslg) |
| 267 | OpenReview:RlqYCpTu1P |  |  | 2 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=RlqYCpTu1P) |
| 268 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 269 | DOI:10.18653/v1/d19-1223 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/d19-1223) |
| 270 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 271 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 272 | OpenReview:OS5dqxmmtl |  |  | 2 |  | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 273 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 274 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 275 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 276 | arXiv:1312.6114 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 277 | arXiv:1404.5997 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1404.5997) |
| 278 | arXiv:1411.1792 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1411.1792) |
| 279 | arXiv:1506.02438 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 280 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 281 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 282 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 283 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 284 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 285 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 286 | arXiv:1606.06160 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 287 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 288 | arXiv:1611.01578 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 289 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 290 | arXiv:1703.03664 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1703.03664) |
| 291 | arXiv:1703.06114 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1703.06114) |
| 292 | arXiv:1704.04684 |  |  | 1 | 07-kv-cache-optimization-compression | [source](https://arxiv.org/abs/1704.04684) |
| 293 | arXiv:1704.05426 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 294 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 295 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 296 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 297 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 298 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 299 | arXiv:1710.09437 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1710.09437) |
| 300 | arXiv:1711.03936 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 301 | arXiv:1711.09224 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.09224) |
| 302 | arXiv:1712.05382 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.05382) |
| 303 | arXiv:1801.10198 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1801.10198) |
| 304 | arXiv:1802.05751 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1802.05751) |
| 305 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 306 | arXiv:1804.06087 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 307 | arXiv:1806.02847 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 308 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 309 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 310 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 311 | arXiv:1809.11096 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1809.11096) |
| 312 | arXiv:1810.03292 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1810.03292) |
| 313 | arXiv:1810.09868 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1810.09868) |
| 314 | arXiv:1811.05233 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 315 | arXiv:1812.06162 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1812.06162) |
| 316 | arXiv:1902.00751 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.00751) |
| 317 | arXiv:1902.08295 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1902.08295) |
| 318 | arXiv:1902.10186 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 319 | arXiv:1903.01699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 320 | arXiv:1904.01038 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1904.01038) |
| 321 | arXiv:1904.09675 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 322 | arXiv:1905.07129 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 323 | arXiv:1906.02041 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/1906.02041) |
| 324 | arXiv:1906.08172 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1906.08172) |
| 325 | arXiv:1907.01989 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1907.01989) |
| 326 | arXiv:1908.08593 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1908.08593) |
| 327 | arXiv:1908.11365 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1908.11365) |
| 328 | arXiv:1909.05803 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1909.05803) |
| 329 | arXiv:1909.11556 |  |  | 1 | speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 330 | arXiv:1910.04915 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1910.04915) |
| 331 | arXiv:1910.06360 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 332 | arXiv:1911.02116 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 333 | arXiv:1911.04997 |  |  | 1 | MoE expert parallelism / dynamic load balancing / expert prefetching | [source](https://arxiv.org/abs/1911.04997) |
| 334 | arXiv:1911.11313 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 335 | arXiv:2002.08155 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2002.08155) |
| 336 | arXiv:2002.10941 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2002.10941) |
| 337 | arXiv:2003.06713 |  |  | 1 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement | [source](https://arxiv.org/abs/2003.06713) |
| 338 | arXiv:2004.02984 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2004.02984) |
| 339 | arXiv:2004.08900 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 340 | arXiv:2004.11867 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 341 | arXiv:2005.00628 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 342 | arXiv:2005.03454 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 343 | arXiv:2005.14187 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 344 | arXiv:2006.10518 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 345 | arXiv:2006.12467 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 346 | arXiv:2007.07779 |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 347 | arXiv:2008.00051 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 348 | arXiv:2009.06106 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 349 | arXiv:2009.08034 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2009.08034) |
| 350 | arXiv:2009.09736 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2009.09736) |
| 351 | arXiv:2010.02394 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 352 | arXiv:2010.03379 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03379) |
| 353 | arXiv:2010.03983 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03983) |
| 354 | arXiv:2010.11443 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2010.11443) |
| 355 | arXiv:2011.02999 |  |  | 1 | 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://arxiv.org/abs/2011.02999) |
| 356 | arXiv:2011.06327 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2011.06327) |
| 357 | arXiv:2012.11346 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2012.11346) |
| 358 | arXiv:2012.15701 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2012.15701) |
| 359 | arXiv:2101.08744 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2101.08744) |
| 360 | arXiv:2102.02611 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2102.02611) |
| 361 | arXiv:2102.08124 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2102.08124) |
| 362 | arXiv:2102.11174 |  |  | 1 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2102.11174) |
| 363 | arXiv:2103.03330 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2103.03330) |
| 364 | arXiv:2104.06599 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2104.06599) |
| 365 | arXiv:2104.13478 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2104.13478) |
| 366 | arXiv:2105.06990 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2105.06990) |
| 367 | arXiv:2105.14450 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2105.14450) |
| 368 | arXiv:2106.03764 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2106.03764) |
| 369 | arXiv:2106.05974 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2106.05974) |
| 370 | arXiv:2106.10595 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2106.10595) |
| 371 | arXiv:2107.05407 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/2107.05407) |
| 372 | arXiv:2108.05036 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2108.05036) |
| 373 | arXiv:2109.00859 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2109.00859) |
| 374 | arXiv:2109.05472 |  |  | 1 | 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2109.05472) |
| 375 | arXiv:2109.10686 |  |  | 1 | 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2109.10686) |
| 376 | arXiv:2109.11817 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2109.11817) |
| 377 | arXiv:2110.06296 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2110.06296) |
| 378 | arXiv:2110.12894 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 379 | arXiv:2111.00160 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 380 | arXiv:2111.00856 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2111.00856) |
| 381 | arXiv:2112.02958 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2112.02958) |
| 382 | arXiv:2112.06749 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2112.06749) |
| 383 | arXiv:2112.14397 |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 384 | arXiv:2201.13425 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2201.13425) |
| 385 | arXiv:2202.05262 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2202.05262) |
| 386 | arXiv:2202.08791 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2202.08791) |
| 387 | arXiv:2202.13914 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.13914) |
| 388 | arXiv:2203.03131 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2203.03131) |
| 389 | arXiv:2203.06850 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2203.06850) |
| 390 | arXiv:2203.11014 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2203.11014) |
| 391 | arXiv:2204.05832 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2204.05832) |
| 392 | arXiv:2204.06683 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 393 | arXiv:2204.11574 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2204.11574) |
| 394 | arXiv:2205.04934 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2205.04934) |
| 395 | arXiv:2205.10364 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10364) |
| 396 | arXiv:2205.11916 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2205.11916) |
| 397 | arXiv:2205.13603 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2205.13603) |
| 398 | arXiv:2206.02845 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2206.02845) |
| 399 | arXiv:2207.05952 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 400 | arXiv:2207.10551 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2207.10551) |
| 401 | arXiv:2208.02813 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 402 | arXiv:2208.08227 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 403 | arXiv:2209.03143 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 404 | arXiv:2209.11429 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 405 | arXiv:2209.15352 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 406 | arXiv:2210.03057 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 407 | arXiv:2210.05709 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2210.05709) |
| 408 | arXiv:2210.08674 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2210.08674) |
| 409 | arXiv:2210.11948 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 410 | arXiv:2210.14793 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 411 | arXiv:2211.00593 |  |  | 1 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 412 | arXiv:2211.06033 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 413 | arXiv:2211.09699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 414 | arXiv:2211.15089 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 415 | arXiv:2212.00768 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.00768) |
| 416 | arXiv:2212.04088 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.04088) |
| 417 | arXiv:2212.05238 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.05238) |
| 418 | arXiv:2212.10325 |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2212.10325) |
| 419 | arXiv:2212.10509 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 420 | arXiv:2212.12017 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 421 | arXiv:2301.04104 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.04104) |
| 422 | arXiv:2301.06672 |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2301.06672) |
| 423 | arXiv:2301.08984 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2301.08984) |
| 424 | arXiv:2301.12503 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2301.12503) |
| 425 | arXiv:2302.02451 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.02451) |
| 426 | arXiv:2302.04863 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.04863) |
| 427 | arXiv:2302.09419 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.09419) |
| 428 | arXiv:2302.11529 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2302.11529) |
| 429 | arXiv:2302.12480 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.12480) |
| 430 | arXiv:2302.14502 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2302.14502) |
| 431 | arXiv:2303.02861 |  |  | 1 | 02-adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.02861) |
| 432 | arXiv:2303.06135 |  |  | 1 | fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2303.06135) |
| 433 | arXiv:2303.07129 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 434 | arXiv:2303.10512 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.10512) |
| 435 | arXiv:2303.13003 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2303.13003) |
| 436 | arXiv:2303.16199 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 437 | arXiv:2304.02017 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 438 | arXiv:2304.03208 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2304.03208) |
| 439 | arXiv:2304.04488 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2304.04488) |
| 440 | arXiv:2304.05332 |  |  | 1 | LLM inference kernel safety / CUDA symbolic execution / model-aware verification | [source](https://arxiv.org/abs/2304.05332) |
| 441 | arXiv:2304.08442 |  |  | 1 | MoE推論／エキスパート並列／エキスパート配置／全対全通信／負荷分散 | [source](https://arxiv.org/abs/2304.08442) |
| 442 | arXiv:2304.10411 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2304.10411) |
| 443 | arXiv:2304.12244 |  |  | 1 | multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 444 | arXiv:2304.15010 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 445 | arXiv:2305.02538 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 446 | arXiv:2305.04044 |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2305.04044) |
| 447 | arXiv:2305.07622 |  |  | 1 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 448 | arXiv:2305.10010 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10010) |
| 449 | arXiv:2305.11860 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2305.11860) |
| 450 | arXiv:2305.13412 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2305.13412) |
| 451 | arXiv:2305.14160 |  |  | 1 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 452 | arXiv:2305.14516 |  |  | 1 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://arxiv.org/abs/2305.14516) |
| 453 | arXiv:2305.14952 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2305.14952) |
| 454 | arXiv:2305.15387 |  |  | 1 | KV cache compression / sparse attention / long-context inference | [source](https://arxiv.org/abs/2305.15387) |
| 455 | arXiv:2305.17126 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2305.17126) |
| 456 | arXiv:2305.18691 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.18691) |
| 457 | arXiv:2306.02003 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 458 | arXiv:2306.02896 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02896) |
| 459 | arXiv:2306.04933 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 460 | arXiv:2306.06624 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2306.06624) |
| 461 | arXiv:2306.09782 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.09782) |
| 462 | arXiv:2306.13596 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 463 | arXiv:2306.16636 |  |  | 1 | sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2306.16636) |
| 464 | arXiv:2307.01189 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.01189) |
| 465 | arXiv:2307.04251 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04251) |
| 466 | arXiv:2307.05300 |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2307.05300) |
| 467 | arXiv:2307.07697 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2307.07697) |
| 468 | arXiv:2307.08191 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2307.08191) |
| 469 | arXiv:2307.12169 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12169) |
| 470 | arXiv:2307.15043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.15043) |
| 471 | arXiv:2308.01285 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2308.01285) |
| 472 | arXiv:2308.03210 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2308.03210) |
| 473 | arXiv:2308.03958 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2308.03958) |
| 474 | arXiv:2308.06744 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2308.06744) |
| 475 | arXiv:2308.10502 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2308.10502) |
| 476 | arXiv:2308.11030 |  |  | 1 | cpu-offload | [source](https://arxiv.org/abs/2308.11030) |
| 477 | arXiv:2308.11761 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2308.11761) |
| 478 | arXiv:2308.15136 |  |  | 1 | KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval | [source](https://arxiv.org/abs/2308.15136) |
| 479 | arXiv:2309.01172 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2309.01172) |
| 480 | arXiv:2309.05135 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2309.05135) |
| 481 | arXiv:2309.07870 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2309.07870) |
| 482 | arXiv:2309.13345 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2309.13345) |
| 483 | arXiv:2309.16588 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.16588) |
| 484 | arXiv:2310.00726 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2310.00726) |
| 485 | arXiv:2310.01427 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2310.01427) |
| 486 | arXiv:2310.02255 |  |  | 1 | multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2310.02255) |
| 487 | arXiv:2310.03003 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2310.03003) |
| 488 | arXiv:2310.04064 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2310.04064) |
| 489 | arXiv:2310.04836 |  |  | 1 | 16-weight-quantization-compression | [source](https://arxiv.org/abs/2310.04836) |
| 490 | arXiv:2310.05209 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.05209) |
| 491 | arXiv:2310.05915 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.05915) |
| 492 | arXiv:2310.06625 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.06625) |
| 493 | arXiv:2310.07096 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.07096) |
| 494 | arXiv:2310.07999 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2310.07999) |
| 495 | arXiv:2310.09130 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.09130) |
| 496 | arXiv:2310.09478 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2310.09478) |
| 497 | arXiv:2310.10908 |  |  | 1 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2310.10908) |
| 498 | arXiv:2310.11703 |  |  | 1 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2310.11703) |
| 499 | arXiv:2310.12462 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2310.12462) |
| 500 | arXiv:2310.12773 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.12773) |

## Machine-readable

同じ割当は [worker-worklist-00.json](worker-worklist-00.json) にあります。

