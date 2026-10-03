# Scheduled worker :30 worklist

Worker: `scheduled-chat-30`  
Generated: `2026-10-03T08:03:14+00:00`

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
| 1 | research | DOI:10.1145/3789240.3822568 | Replacing NVMe Staging in LLM Inference with a High-Bandwidth CXL Memory Expander with an On-Device DMA Controller | [primary](https://www.semanticscholar.org/paper/7a2499fd38665d8205c513eb3740ddedc3675c5e) | `papers/inference/99-other-inference-systems/2026-34514b56228c-replacing-nvme-staging-in-llm-inference-with-a-high-bandwidth-cxl-memory-expander-with-an-on-device-dma-controller.md` |
| 2 | research | DOI:10.1109/INFOCOM59046.2026.11571388 | CoSine: Enhancing LLM Serving via Collaborative and Decoupled Speculative Inference | [primary](https://www.semanticscholar.org/paper/cfe4e4e23b47ae91c7bcb42dba0236152645918a) | `papers/inference/99-other-inference-systems/2026-34f343c5dcff-cosine-enhancing-llm-serving-via-collaborative-and-decoupled-speculative-inference.md` |
| 3 | research | DOI:10.1145/3832810.3832866 | AsymFlow: Enabling Long-Context LLM Serving via CPU-GPU Prefill-Decode Disaggregation | [primary](https://www.semanticscholar.org/paper/50318e12c7f8b36202899a69346fd9920a2e73a9) | `papers/inference/99-other-inference-systems/2026-c24278db090c-asymflow-enabling-long-context-llm-serving-via-cpu-gpu-prefill-decode-disaggregation.md` |
| 4 | research | DOI:10.1145/3793230.3837769 | To Keep or Not to Keep: Learning KV Cache Retention in Disaggregated LLM Serving Systems | [primary](https://www.semanticscholar.org/paper/6db782df823d9da204a59180305aba81d47b3997) | `papers/inference/99-other-inference-systems/2026-5497c425b6df-to-keep-or-not-to-keep-learning-kv-cache-retention-in-disaggregated-llm-serving-systems.md` |
| 5 | research | arXiv:2608.15299 | MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation | [primary](https://arxiv.org/abs/2608.15299) | `papers/inference/02-adaptive-expert-computation-compression/2026-2608.15299-maple-layer-wise-expert-allocation.md` |
| 6 | research | arXiv:2603.18492 | AIMER: Calibration-Free Task-Agnostic MoE Expert Pruning | [primary](https://arxiv.org/abs/2603.18492) | `papers/inference/02-adaptive-expert-computation-compression/2026-2603.18492-aimer-calibration-free-pruning.md` |
| 7 | research | arXiv:2609.08663 | MoEMB: Scaling Universal Multimodal Embeddings with Efficient Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2609.08663) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.08663-moemb-adaptive-computation.md` |
| 8 | research | DOI:10.1145/3832810.3832865 | WAQ-LLM: Optimizing Multi-Instance LLM Deployment via Workload-Aware Queueing Model | [primary](https://www.semanticscholar.org/paper/a3ea92c6fa8233ac57ec595875a2a35f7f640056) | `papers/inference/99-other-inference-systems/2026-eb0724db43f1-waq-llm-optimizing-multi-instance-llm-deployment-via-workload-aware-queueing-model.md` |
| 9 | research | arXiv:2608.15584 | GraniKV: Asymmetric Granularity KV-Cache Paging for Multi-Agent Systems with Long Shared Prefix | [primary](https://www.semanticscholar.org/paper/1e7525745039a88cd6a0e58c0526ef6695ec9214) | `papers/inference/99-other-inference-systems/2026-2608.15584-granikv-asymmetric-granularity-kv-cache-paging-for-multi-agent-systems-with-long-shared-prefix.md` |
| 10 | research | arXiv:2607.06763 | Trees from Marginals: Autoregressive drafting with factorized priors | [primary](https://www.semanticscholar.org/paper/508b0bb474c86faf305f38ae7db6c9af532e2886) | `papers/inference/99-other-inference-systems/2026-2607.06763-trees-from-marginals-autoregressive-drafting-with-factorized-priors.md` |
| 11 | research | DOI:10.1109/JIOT.2026.3709703 | Co-Optimizing Request Scheduling and KV Caching for Edge LLM Serving | [primary](https://www.semanticscholar.org/paper/f25ba2c420a573830f2b4b2f30dd2fcc3adffeb2) | `papers/inference/99-other-inference-systems/2026-de817f8d0333-co-optimizing-request-scheduling-and-kv-caching-for-edge-llm-serving.md` |
| 12 | research | arXiv:2608.19395 | HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads | [primary](https://www.semanticscholar.org/paper/65435abac34942c78717b5d15b0a2e437e59b568) | `papers/inference/99-other-inference-systems/2026-2608.19395-hydra-a-heterogeneous-chiplet-dse-framework-for-serving-dynamic-hybrid-llm-workloads.md` |
| 13 | research | arXiv:2606.01509 | ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts | [primary](https://arxiv.org/abs/2606.01509) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.01509-probmoe-probabilistic-routing.md` |
| 14 | research | arXiv:2602.09316 | Effective MoE-based LLM Compression by Exploiting Heterogeneous Inter-Group Experts Routing Frequency and Information Density | [primary](https://arxiv.org/abs/2602.09316) | `papers/inference/02-adaptive-expert-computation-compression/2026-2602.09316-rfid-moe-heterogeneous-svd-compression.md` |
| 15 | research | arXiv:2407.00945 | Efficient Expert Pruning for Sparse Mixture-of-Experts Language Models: Enhancing Performance and Reducing Inference Costs | [primary](https://arxiv.org/abs/2407.00945) | `papers/inference/02-adaptive-expert-computation-compression/2024-2407.00945-efficient-expert-pruning.md` |
| 16 | research | DOI:10.1145/3789240.3830285 | POSTER: Prediction-Enhanced Expert Prefetching and Eviction for MoE Offloading via PRED-MoE | [primary](https://doi.org/10.1145/3789240.3830285) | `papers/inference/03-expert-prefetch/2026-pred-moe-prefetch-eviction.md` |
| 17 | research | arXiv:2607.12839 | HeteroMosaic: Exposing and Exploiting Heterogeneous Execution Opportunities for Energy-Efficient Edge LLM Inference | [primary](https://arxiv.org/abs/2607.12839) | `papers/inference/99-other-inference-systems/2026-2607.12839-heteromosaic-exposing-and-exploiting-heterogeneous-execution-opportunities-for-energy-efficient-edge-llm-inference.md` |
| 18 | research | arXiv:2608.28911 | SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference | [primary](https://www.semanticscholar.org/paper/d3f7b7e4211810aede1fbf47e1b342071445dacb) | `papers/inference/99-other-inference-systems/2026-2608.28911-semkv-semantic-mixed-precision-kv-cache-quantization-guided-by-the-quality-cliff-for-long-context-llm-inference.md` |
| 19 | research | arXiv:2609.08135 | KBBQ: A Predictive Noise Law and the Limits of Spectrum Flattening in FP4 Quantization | [primary](https://www.semanticscholar.org/paper/384b3e22a60cd9fe55232c2725725a646bec1413) | `papers/inference/99-other-inference-systems/2026-2609.08135-kbbq-a-predictive-noise-law-and-the-limits-of-spectrum-flattening-in-fp4-quantization.md` |
| 20 | research | DOI:10.1109/ICAISISAS68969.2026.11567792 | TDMoE: Tail-probability-based Dynamic-k MoE | [primary](https://doi.org/10.1109/ICAISISAS68969.2026.11567792) | `papers/inference/02-adaptive-expert-computation-compression/2026-tdmoe-tail-probability-dynamic-k.md` |
| 21 | research | DOI:10.1016/j.knosys.2026.116244 | RS-MoE: Coupled expert compression via activation-peak guided collaborative decomposition | [primary](https://doi.org/10.1016/j.knosys.2026.116244) | `papers/inference/02-adaptive-expert-computation-compression/2026-rs-moe-coupled-expert-compression.md` |
| 22 | research | DOI:10.1145/3832810.3832894 | Cross-Layer Performance Analysis of Single-GPU Large Language Model Inference | [primary](https://www.semanticscholar.org/paper/64b1253f0b492e5a855336514fc0457ad35219eb) | `papers/inference/99-other-inference-systems/2026-c4e6405cec16-cross-layer-performance-analysis-of-single-gpu-large-language-model-inference.md` |
| 23 | research | arXiv:2609.19702 | Understanding and Exploiting Diagonal Attention Sparsity in Autoregressive Image Generation | [primary](https://www.semanticscholar.org/paper/54db2b227072dcee4790de99c581d51c7d3c17f7) | `papers/inference/99-other-inference-systems/2026-2609.19702-understanding-and-exploiting-diagonal-attention-sparsity-in-autoregressive-image-generation.md` |
| 24 | research | DOI:10.1016/j.neunet.2025.108274 | Expertfuse: A huffman tree-based gradual expert integration framework for MoE models | [primary](https://doi.org/10.1016/j.neunet.2025.108274) | `papers/inference/02-adaptive-expert-computation-compression/2025-expertfuse-huffman-gradual-expert-integration.md` |
| 25 | research | arXiv:2608.24650 | Simthesizer: An Agent-Driven Simulation Framework for LLM Serving Systems | [primary](https://arxiv.org/abs/2608.24650) | `papers/inference/99-other-inference-systems/2026-2608.24650-simthesizer-an-agent-driven-simulation-framework-for-llm-serving-systems.md` |
| 26 | research | arXiv:2609.07664 | Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs | [primary](https://www.semanticscholar.org/paper/84845b9a9ba10adeb94154d89fac900566597aaf) | `papers/inference/99-other-inference-systems/2026-2609.07664-accuracy-is-not-enough-a-divergence-based-approach-to-evaluate-fidelity-loss-in-quantized-llms.md` |
| 27 | research | arXiv:2609.13682 | LayerRoute: Adaptive Layer-Skipping with LoRA-Preserved Quality for Efficient LLM Inference | [primary](https://arxiv.org/abs/2609.13682) | `papers/inference/99-other-inference-systems/2026-2609.13682-layerroute-adaptive-layer-skipping-with-lora-preserved-quality-for-efficient-llm-inference.md` |
| 28 | research | DOI:10.5281/zenodo.22339206 | A Survey of Inference Processing Units for Large Language Model Inference: Chips, Systems, Algorithms, and Paradigms (2024–2026) | [primary](https://doi.org/10.5281/zenodo.22339206) | `papers/inference/99-other-inference-systems/2026-f8b8eb9da2fe-a-survey-of-inference-processing-units-for-large-language-model-inference-chips-systems-algorithms-and-paradigms-2024202.md` |
| 29 | research | arXiv:2608.24063 | VisCache: Visual KV Cache Pruning for Efficient Vision Large Language Model Inference | [primary](https://www.semanticscholar.org/paper/2655c9d3521d8af9a51c602f9cb9bb3a33f74c31) | `papers/inference/99-other-inference-systems/2026-2608.24063-viscache-visual-kv-cache-pruning-for-efficient-vision-large-language-model-inference.md` |
| 30 | research | arXiv:2511.19480 | Exploiting the Experts: Unauthorized Compression in MoE-LLMs | [primary](https://arxiv.org/abs/2511.19480) | `papers/inference/02-adaptive-expert-computation-compression/2025-2511.19480-unauthorized-moe-compression-expert-attribution.md` |
| 31 | research | arXiv:2506.07366 | MoE-GPS: Guidlines for Prediction Strategy for Dynamic Expert Duplication in MoE Load Balancing | [primary](https://www.semanticscholar.org/paper/b3d726f638aad791664917fc471740ff5c41eef9) | `papers/inference/99-other-inference-systems/2025-2506.07366-moe-gps-guidlines-for-prediction-strategy-for-dynamic-expert-duplication-in-moe-load-balancing.md` |
| 32 | research | DOI:10.1109/NVMSA71223.2026.11658877 | Poster: SAF: Semantic-Aware Flushing for Latency and Jitter Suppression in Continuous VLA Inference on Edge Devices | [primary](https://doi.org/10.1109/NVMSA71223.2026.11658877) | `papers/inference/10-kv-cache-offload-recomputation/2026-saf-semantic-aware-flushing-kv-nvme-edge.md` |
| 33 | research | arXiv:2607.17181 | Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs | [primary](https://www.semanticscholar.org/paper/e7106b6132090e3a5d8f669d7e94ba890e42b781) | `papers/inference/99-other-inference-systems/2026-2607.17181-talaria-session-aware-serverless-serving-of-hundred-billion-parameter-llms.md` |
| 34 | research | arXiv:2405.13019 | A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models | [primary](https://arxiv.org/abs/2405.13019) | `papers/survey/05-accelerated-generation/2024-2405.13019-accelerated-generation-survey.md` |
| 35 | research | DOI:10.1016/j.parco.2026.103216 | SmartBatchLLM: An efficient adaptive hybrid batching strategy for large language model serving | [primary](https://doi.org/10.1016/j.parco.2026.103216) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-smartbatchllm-adaptive-hybrid-batching.md` |
| 36 | research | arXiv:2607.27269 | Beyond KV Reconstruction: Functional Reconstruction for MLA Draft Models in Speculative Decoding | [primary](https://www.semanticscholar.org/paper/0259a9d7148b5b97ddfed795956aaf13cf5da0b1) | `papers/inference/99-other-inference-systems/2026-2607.27269-beyond-kv-reconstruction-functional-reconstruction-for-mla-draft-models-in-speculative-decoding.md` |
| 37 | research | arXiv:2404.14294 | A Survey on Efficient Inference for Large Language Models | [primary](https://arxiv.org/abs/2404.14294) | `papers/survey/03-inference-engines/2024-2404.14294-survey-efficient-inference-llms.md` |
| 38 | research | arXiv:2409.02060 | OLMoE: Open Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2409.02060) | `papers/inference/99-other-inference-systems/2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md` |
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
| 98 | research | arXiv:2110.03888 | M6-10T: A Sharing-Delinking Paradigm for Efficient Multi-Trillion Parameter Pretraining | [primary](https://arxiv.org/abs/2110.03888) | `papers/inference/99-other-inference-systems/2021-2110.03888-m6-10t-a-sharing-delinking-paradigm-for-efficient-multi-trillion-parameter-pretraining.md` |
| 99 | research | arXiv:2602.16284 | Fast KV Compaction via Attention Matching | [primary](https://arxiv.org/abs/2602.16284) | `papers/inference/99-other-inference-systems/2026-2602.16284-fast-kv-compaction-via-attention-matching.md` |
| 100 | research | arXiv:2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | [primary](https://arxiv.org/abs/2508.18265) | `papers/inference/99-other-inference-systems/2025-2508.18265-internvl3-5-advancing-open-source-multimodal-models-in-versatility-reasoning-and-efficiency.md` |
| 101 | research | arXiv:2110.15032 | OneFlow: Redesign the Distributed Deep Learning Framework from Scratch | [primary](https://arxiv.org/abs/2110.15032) | `papers/inference/99-other-inference-systems/2021-2110.15032-oneflow-redesign-the-distributed-deep-learning-framework-from-scratch.md` |
| 102 | research | DOI:10.1145/3731569.3764834 | PrefillOnly: An Inference Engine for Prefill-only Workloads in Large Language Model Applications | [primary](https://doi.org/10.1145/3731569.3764834) | `papers/inference/99-other-inference-systems/0000-cc54e0b027f8-prefillonly-an-inference-engine-for-prefill-only-workloads-in-large-language-model-applications.md` |
| 103 | research | arXiv:2511.00606 | SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding | [primary](https://arxiv.org/abs/2511.00606) | `papers/inference/99-other-inference-systems/2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-decoding.md` |
| 104 | research | arXiv:2606.12370 | Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling | [primary](https://arxiv.org/abs/2606.12370) | `papers/inference/99-other-inference-systems/2026-2606.12370-breaking-entropy-bounds-accelerating-rl-training-via-mtp-with-rejection-sampling.md` |
| 105 | research | arXiv:2502.17421 | LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification | [primary](https://arxiv.org/abs/2502.17421) | `papers/inference/99-other-inference-systems/2025-2502.17421-longspec-long-context-lossless-speculative-decoding-with-efficient-drafting-and-verification.md` |
| 106 | research | arXiv:2601.07891 | KVzap: Fast, Adaptive, and Faithful KV Cache Pruning | [primary](https://arxiv.org/abs/2601.07891) | `papers/inference/99-other-inference-systems/2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md` |
| 107 | research | arXiv:2606.26650 | CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs | [primary](https://arxiv.org/abs/2606.26650) | `papers/inference/99-other-inference-systems/2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md` |
| 108 | research | DOI:10.1109/isca59077.2024.00082 | LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference | [primary](https://doi.org/10.1109/isca59077.2024.00082) | `papers/inference/99-other-inference-systems/0000-6daecc086891-llmcompass-enabling-efficient-hardware-design-for-large-language-model-inference.md` |
| 109 | research | arXiv:2409.01143 | HexiScale: Facilitating Large Language Model Training over Heterogeneous Hardware | [primary](https://arxiv.org/abs/2409.01143) | `papers/inference/99-other-inference-systems/2024-2409.01143-hexiscale-facilitating-large-language-model-training-over-heterogeneous-hardware.md` |
| 110 | research | arXiv:2306.10209 | ZeRO++: Extremely Efficient Collective Communication for Giant Model Training | [primary](https://arxiv.org/abs/2306.10209) | `papers/inference/99-other-inference-systems/2023-2306.10209-zero-extremely-efficient-collective-communication-for-giant-model-training.md` |
| 111 | research | arXiv:2502.12110 | A-Mem: Agentic Memory for LLM Agents | [primary](https://arxiv.org/abs/2502.12110) | `papers/inference/99-other-inference-systems/2025-2502.12110-a-mem-agentic-memory-for-llm-agents.md` |
| 112 | research | arXiv:2401.00134 | Unicron: Economizing Self-Healing LLM Training at Scale | [primary](https://arxiv.org/abs/2401.00134) | `papers/inference/99-other-inference-systems/2024-2401.00134-unicron-economizing-self-healing-llm-training-at-scale.md` |
| 113 | research | arXiv:2206.03382 | Tutel: Adaptive Mixture-of-Experts at Scale | [primary](https://arxiv.org/abs/2206.03382) | `papers/inference/99-other-inference-systems/2022-2206.03382-tutel-adaptive-mixture-of-experts-at-scale.md` |
| 114 | research | arXiv:2312.06635 | Gated Linear Attention Transformers with Hardware-Efficient Training | [primary](https://arxiv.org/abs/2312.06635) | `papers/inference/99-other-inference-systems/2023-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md` |
| 115 | research | arXiv:2511.20975 | Aragog: Just-in-Time Model Routing for Scalable Serving of Agentic Workflows | [primary](https://arxiv.org/abs/2511.20975) | `papers/inference/99-other-inference-systems/2025-2511.20975-aragog-just-in-time-model-routing-for-scalable-serving-of-agentic-workflows.md` |
| 116 | research | arXiv:2203.16487 | Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation | [primary](https://arxiv.org/abs/2203.16487) | `papers/inference/99-other-inference-systems/2022-2203.16487-speculative-decoding-exploiting-speculative-execution-for-accelerating-seq2seq-generation.md` |
| 117 | research | arXiv:2310.07188 | Adaptive Gating in Mixture-of-Experts based Language Models | [primary](https://arxiv.org/abs/2310.07188) | `papers/inference/99-other-inference-systems/2023-2310.07188-adaptive-gating-in-mixture-of-experts-based-language-models.md` |
| 118 | research | arXiv:2504.12397 | Activated LoRA: Fine-tuned LLMs for Intrinsics | [primary](https://arxiv.org/abs/2504.12397) | `papers/inference/99-other-inference-systems/2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md` |
| 119 | research | arXiv:2504.08378 | Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash | [primary](https://arxiv.org/abs/2504.08378) | `papers/inference/99-other-inference-systems/2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-flash.md` |
| 120 | research | arXiv:2407.05467 | The infrastructure powering IBM's Gen AI model development | [primary](https://arxiv.org/abs/2407.05467) | `papers/inference/99-other-inference-systems/2024-2407.05467-the-infrastructure-powering-ibm-s-gen-ai-model-development.md` |
| 121 | research | arXiv:2306.08543 | MiniLLM: On-Policy Distillation of Large Language Models | [primary](https://arxiv.org/abs/2306.08543) | `papers/inference/99-other-inference-systems/2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md` |
| 122 | research | DOI:10.1145/3777466 | Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines | [primary](https://doi.org/10.1145/3777466) | `papers/inference/99-other-inference-systems/2025-704c3dbb57e7-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md` |
| 123 | research | arXiv:2410.04199 | LongGenBench: Long-context Generation Benchmark | [primary](https://arxiv.org/abs/2410.04199) | `papers/inference/99-other-inference-systems/2024-2410.04199-longgenbench-long-context-generation-benchmark.md` |
| 124 | research | DOI:10.1145/3642970.3655835 | Deferred Continuous Batching in Resource-Efficient Large Language Model Serving | [primary](https://doi.org/10.1145/3642970.3655835) | `papers/inference/99-other-inference-systems/2024-cd0254f5f44d-deferred-continuous-batching-in-resource-efficient-large-language-model-serving.md` |
| 125 | research | arXiv:2510.14557 | MX+: Pushing the Limits of Microscaling Formats for Efficient Large Language Model Serving | [primary](https://arxiv.org/abs/2510.14557) | `papers/inference/99-other-inference-systems/2025-2510.14557-mx-pushing-the-limits-of-microscaling-formats-for-efficient-large-language-model-serving.md` |
| 126 | research | arXiv:2604.16957 | Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon | [primary](https://arxiv.org/abs/2604.16957) | `papers/inference/99-other-inference-systems/2026-2604.16957-open-tq-metal-fused-compressed-domain-attention-for-long-context-llm-inference-on-apple-silicon.md` |
| 127 | research | DOI:10.1145/3779212.3790246 | SwiftSpec: Disaggregated Speculative Decoding and Fused Kernels for Low-Latency LLM Inference | [primary](https://doi.org/10.1145/3779212.3790246) | `papers/inference/99-other-inference-systems/2026-92272744585e-swiftspec-disaggregated-speculative-decoding-and-fused-kernels-for-low-latency-llm-inference.md` |
| 128 | research | arXiv:2310.04836 | Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM | [primary](https://arxiv.org/abs/2310.04836) | `papers/inference/99-other-inference-systems/2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md` |
| 129 | research | arXiv:2310.08915 | Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs | [primary](https://arxiv.org/abs/2310.08915) | `papers/inference/99-other-inference-systems/2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md` |
| 130 | research | arXiv:2609.33184 | Resource-Efficient Speculative Decoding for Long-Context LLM Serving | [primary](https://arxiv.org/abs/2609.33184) | `papers/inference/99-other-inference-systems/2026-2609.33184-resource-efficient-speculative-decoding-for-long-context-llm-serving.md` |
| 131 | research | arXiv:2009.14794 | Rethinking Attention with Performers | [primary](https://arxiv.org/abs/2009.14794) | `papers/inference/99-other-inference-systems/2020-2009.14794-rethinking-attention-with-performers.md` |
| 132 | research | arXiv:2602.23200 | InnerQ: Hardware-aware Tuning-free Quantization of KV Cache for Large Language Models | [primary](https://arxiv.org/abs/2602.23200) | `papers/inference/99-other-inference-systems/2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-language-models.md` |
| 133 | research | arXiv:2402.18668 | Simple linear attention language models balance the recall-throughput tradeoff | [primary](https://arxiv.org/abs/2402.18668) | `papers/inference/99-other-inference-systems/2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tradeoff.md` |
| 134 | research | DOI:10.1145/3620665.3640366 | PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation | [primary](https://doi.org/10.1145/3620665.3640366) | `papers/inference/99-other-inference-systems/2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transformation-and-graph-compilation.md` |
| 135 | research | arXiv:2401.06118 | Extreme Compression of Large Language Models via Additive Quantization | [primary](https://arxiv.org/abs/2401.06118) | `papers/inference/99-other-inference-systems/2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md` |
| 136 | research | DOI:10.1145/3642970.3655844 | ALTO: An Efficient Network Orchestrator for Compound AI Systems | [primary](https://doi.org/10.1145/3642970.3655844) | `papers/inference/99-other-inference-systems/2024-01aa9dc12834-alto-an-efficient-network-orchestrator-for-compound-ai-systems.md` |
| 137 | research | arXiv:2402.11295 | OneBit: Towards Extremely Low-bit Large Language Models | [primary](https://arxiv.org/abs/2402.11295) | `papers/inference/99-other-inference-systems/2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md` |
| 138 | research | arXiv:2402.02446 | LQER: Low-Rank Quantization Error Reconstruction for LLMs | [primary](https://arxiv.org/abs/2402.02446) | `papers/inference/99-other-inference-systems/2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md` |
| 139 | research | arXiv:2312.12682 | Mini-GPTs: Efficient Large Language Models through Contextual Pruning | [primary](https://arxiv.org/abs/2312.12682) | `papers/inference/99-other-inference-systems/2023-2312.12682-mini-gpts-efficient-large-language-models-through-contextual-pruning.md` |
| 140 | research | arXiv:2312.13211 | DSFormer: Effective Compression of Text-Transformers by Dense-Sparse Weight Factorization | [primary](https://arxiv.org/abs/2312.13211) | `papers/inference/99-other-inference-systems/2023-2312.13211-dsformer-effective-compression-of-text-transformers-by-dense-sparse-weight-factorization.md` |
| 141 | research | arXiv:2402.12280 | Plato: Plan to Efficiently Decode for Large Language Model Inference | [primary](https://arxiv.org/abs/2402.12280) | `papers/inference/99-other-inference-systems/2024-2402.12280-plato-plan-to-efficiently-decode-for-large-language-model-inference.md` |
| 142 | research | arXiv:2402.17985 | FlattenQuant: Breaking through the Inference Compute-bound for Large Language Models with Per-tensor Quantization | [primary](https://arxiv.org/abs/2402.17985) | `papers/inference/99-other-inference-systems/2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-language-models-with-per-tensor-quantization.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5776** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.48550/arxiv.2408.11850 |  |  | 19 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative Decoding / Parallel Inference Systems, inference-systems, speculative-decoding, speculative-decoding-moe, 投機的デコード／MoE, 投機的デコード／動的候補木／高同時実行LLMサービング | [source](https://doi.org/10.48550/arxiv.2408.11850) |
| 2 | DOI:10.18653/v1/d18-1259 |  |  | 14 | 07-kv-cache-optimization-compression, 13-sparse-attention, Adaptive Expert Computation / Compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング, 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://doi.org/10.18653/v1/d18-1259) |
| 3 | DOI:10.1145/3669940.3707267 |  |  | 13 | KV Cache Optimization / Compression, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Offload / Hierarchical Memory, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, hierarchical-memory-kv-offload-cpu-gpu-attention, moe-inference-expert-placement-caching, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://doi.org/10.1145/3669940.3707267) |
| 4 | arXiv:2409.12186 |  |  | 12 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation, inference-systems, multi-LLM communication / KV-cache semantic transfer, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM, 推論エンジン／推論基盤, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://arxiv.org/abs/2409.12186) |
| 5 | arXiv:2304.01089 |  |  | 11 | Conditional Computation, Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 6 | arXiv:2410.21276 |  |  | 11 | 07-kv-cache-optimization-compression, Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, fine-grained MoE / expert routing / test-time scaling / inference-time sampling, kv-cache-optimization-compression, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, multi-tenant LLM serving / latency attribution / fractional GPU sharing, その他システム研究 | [source](https://arxiv.org/abs/2410.21276) |
| 7 | arXiv:2405.16406 |  |  | 11 | 11-llm-serving-scheduling-disaggregation, 17-pim-near-data-acceleration, FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV cache quantization / rotation-based compression / MoE expert offloading / consumer local inference, inference-systems, kv-cache-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2405.16406) |
| 8 | OpenReview:cFu7ze7xUm |  |  | 11 | 13-sparse-attention, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, other-inference-systems | [source](https://openreview.net/forum?id=cFu7ze7xUm) |
| 9 | DOI:10.48550/arxiv.2404.07413 |  |  | 10 | 02-adaptive-expert-computation-compression, Adaptive computation／cache-aware MoE, MoE compression / expert merging / output approximation / least-squares compression, MoE predictive expert placement / replication / SiDA-MoE, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, moe-parallelism-communication, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2404.07413) |
| 10 | OpenReview:VTF8yNQM66 |  |  | 10 | 13-sparse-attention, Agentic Serving Benchmarking, MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, agentic workflow serving / workflow physical planning / adaptive serving, llm-serving-scheduling-disaggregation, other-inference-systems, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=VTF8yNQM66) |
| 11 | DOI:10.48550/arxiv.2412.00099 |  |  | 10 | 08-edge-on-device-llm-systems, edge-on-device-llm-systems, hardware-accelerators, offload-hierarchical-memory, survey-moe-inference-optimization, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.48550/arxiv.2412.00099) |
| 12 | arXiv:2407.21118 |  |  | 10 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2407.21118) |
| 13 | arXiv:2405.21060 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化, PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management, kv-cache, kv-cache-offload-recomputation, linear attention / delta-rule associative memory / state-space models / Bayesian filtering, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2405.21060) |
| 14 | DOI:10.18653/v1/2024.emnlp-main.422 |  |  | 9 | 05-speculative-decoding-moe, LLM Serving / Scheduling / Disaggregation, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE, other-inference-systems, speculative-decoding, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://doi.org/10.18653/v1/2024.emnlp-main.422) |
| 15 | DOI:10.18653/v1/2024.emnlp-main.890 |  |  | 9 | Adaptive computation／cache-aware MoE, Edge／on-device MoE, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive-expert-computation-compression, moe-inference-expert-offloading, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://doi.org/10.18653/v1/2024.emnlp-main.890) |
| 16 | DOI:10.18653/v1/2020.coling-main.580 |  |  | 9 | 10-kv-キャッシュ-オフロード-recomputation, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, Prefill/Decode Disaggregation / Selective KV Transfer, inference-systems | [source](https://doi.org/10.18653/v1/2020.coling-main.580) |
| 17 | DOI:10.18653/v1/k16-1028 |  |  | 9 | Speculative decoding × MoE, inference-systems, survey-speculative-decoding, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/k16-1028) |
| 18 | arXiv:2309.12307 |  |  | 8 | Conditional Computation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference, KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ, cpu-offload, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, multi-tenant LoRA serving / CPU-assisted inference / rank-aware scheduling | [source](https://arxiv.org/abs/2309.12307) |
| 19 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 20 | DOI:10.1147/sj.52.0078 |  |  | 8 | 14-agentic-inference-serving-runtime, KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, MoE expert offloading / predictive prefetch and cache management, Offload / Hierarchical Memory, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1147/sj.52.0078) |
| 21 | DOI:10.64434/tml.20250910 |  |  | 8 | Agentic Serving Benchmarking, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 22 | DOI:10.1145/3772052.3772239 |  |  | 8 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation, multi-SLO serving / speculative decoding / SLO-aware scheduling / hardware-aware token budgeting, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://doi.org/10.1145/3772052.3772239) |
| 23 | arXiv:1607.06450 |  |  | 7 | Conditional Computation, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 24 | arXiv:2406.00515 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, LLM inference kernel safety / CUDA symbolic execution / model-aware verification, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, kernel-runtime-compilation, serving-scheduling | [source](https://arxiv.org/abs/2406.00515) |
| 25 | arXiv:2303.08302 |  |  | 7 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Weight Quantization / Compression, inference-systems, offload-hierarchical-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2303.08302) |
| 26 | arXiv:2408.11743 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 27 | OpenReview:wHBfxhZu1u |  |  | 7 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-optimization-compression, other-inference-systems, 投機的復号 / LLMサービング・ベンチマーク | [source](https://openreview.net/forum?id=wHBfxhZu1u) |
| 28 | arXiv:2209.11895 |  |  | 7 | KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/2209.11895) |
| 29 | arXiv:2310.15141 |  |  | 7 | LLM inference surveys、roofline performance analysis, inference-systems, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 30 | DOI:10.1145/3711896.3737413 |  |  | 7 | LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3711896.3737413) |
| 31 | arXiv:2411.15124 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, MoE compression / expert matrix decomposition / shared basis reparameterization, adaptive expert computation / dynamic MoE routing / expert sparsification, conditional-computation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2411.15124) |
| 32 | DOI:10.1145/3676641.3716278 |  |  | 6 | 08-edge-on-device-llm-systems, 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 33 | arXiv:2110.03742 |  |  | 6 | Edge／on-device MoE, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference / expert pruning / language-specific expert specialization, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2110.03742) |
| 34 | arXiv:2405.05465 |  |  | 6 | KV Cache Offload / Recomputation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, disaggregated LLM serving / request routing / learned scheduling, kv-cache-memory-management, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2405.05465) |
| 35 | arXiv:2412.10302 |  |  | 6 | Adaptive computation／cache-aware MoE, MoE compression / training-free expert merging / multimodal MoE routing, Quantization × MoE × Offload, adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2412.10302) |
| 36 | arXiv:2509.17765 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 37 | OpenReview:PxoFut3dWW |  |  | 6 | 07-kv-cache-optimization-compression, Adaptive Expert Computation / Compression, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, inference-systems | [source](https://openreview.net/forum?id=PxoFut3dWW) |
| 38 | arXiv:2401.03462 |  |  | 6 | 07-kv-キャッシュ-optimization-compression, KV Cache Compression / Long Context, KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2401.03462) |
| 39 | OpenReview:7Bywt2mQsCe |  |  | 6 | KV Cache Optimization / Compression, Speculative decoding × MoE, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Bywt2mQsCe) |
| 40 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 41 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 42 | arXiv:2204.09179 |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 43 | arXiv:2603.01175 |  |  | 5 | 10-kv-cache-offload-recomputation, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, flash-capacity-tier-inference, hardware-accelerators, offload-hierarchical-memory | [source](https://arxiv.org/abs/2603.01175) |
| 44 | DOI:10.18653/v1/d16-1264 |  |  | 5 | 07-kv-cache-optimization-compression, Adaptive Expert Computation / Compression, adaptive-expert-computation-compression, kv-cache-optimization-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.18653/v1/d16-1264) |
| 45 | arXiv:1805.06085 |  |  | 5 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, cpu-ssd-offload, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1805.06085) |
| 46 | arXiv:2212.10560 |  |  | 5 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2212.10560) |
| 47 | DOI:10.1162/tacl_a_00023 |  |  | 5 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1162/tacl_a_00023) |
| 48 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 49 | arXiv:1811.00937 |  |  | 5 | Adaptive Expert Computation / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1811.00937) |
| 50 | arXiv:2504.07491 |  |  | 5 | 11-llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2504.07491) |
| 51 | OpenReview:KzACYw0MTV |  |  | 5 | 10-kv-キャッシュ-オフロード-recomputation, Prefill/Decode Disaggregation / Selective KV Transfer, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=KzACYw0MTV) |
| 52 | DOI:10.18653/v1/2023.emnlp-main.825 |  |  | 5 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.825) |
| 53 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 54 | arXiv:2402.14905 |  |  | 4 | 10-kv-cache-offload-recomputation, kv-cache-optimization-compression, offload-hierarchical-memory, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2402.14905) |
| 55 | arXiv:2506.06266 |  |  | 4 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-offload-recomputation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2506.06266) |
| 56 | DOI:10.1145/3620666.3651352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 57 | DOI:10.48550/arxiv.2306.11644 |  |  | 4 | on-device LLM inference / mobile inference / Flash offload, other-inference-systems, survey-edge-llm, オフロード／階層メモリ | [source](https://doi.org/10.48550/arxiv.2306.11644) |
| 58 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 59 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 60 | arXiv:2402.06082 |  |  | 4 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 61 | DOI:10.1109/mm.2024.3375352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, Offload / Hierarchical Memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/mm.2024.3375352) |
| 62 | DOI:10.48550/arxiv.2409.12136 |  |  | 4 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, inference-systems, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2409.12136) |
| 63 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 64 | OpenReview:zAdUB0aCTQ |  |  | 4 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://openreview.net/forum?id=zAdUB0aCTQ) |
| 65 | arXiv:2512.19849 |  |  | 4 | Speculative decoding × MoE, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2512.19849) |
| 66 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 67 | OpenReview:SylKikSYDH |  |  | 4 | KV cache sparsity / paged attention / query-aware selection / LLM serving, inference-systems | [source](https://openreview.net/forum?id=SylKikSYDH) |
| 68 | arXiv:2306.02561 |  |  | 3 | LLM routing、hybrid inference、quality-aware model selection, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 69 | arXiv:2312.13558 |  |  | 3 | LLM inference surveys、roofline performance analysis, inference-systems, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 70 | arXiv:2402.06126 |  |  | 3 | Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.06126) |
| 71 | arXiv:2406.03853 |  |  | 3 | adaptive-expert-computation-compression, inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2406.03853) |
| 72 | arXiv:2409.18486 |  |  | 3 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, inference-systems, prefill-decode disaggregation / attention offloading / LLM serving | [source](https://arxiv.org/abs/2409.18486) |
| 73 | arXiv:2411.11055 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 74 | arXiv:2502.16880 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2502.16880) |
| 75 | arXiv:2504.04823 |  |  | 3 | inference-systems, kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2504.04823) |
| 76 | arXiv:2512.22420 |  |  | 3 | llm-serving-scheduling-disaggregation, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2512.22420) |
| 77 | DOI:10.1109/hoti.2015.13 |  |  | 3 | KVキャッシュオフロード・再計算, RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/hoti.2015.13) |
| 78 | DOI:10.1109/lca.2025.3628325 |  |  | 3 | 12-benchmarking-modeling-emulation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, other-inference-systems | [source](https://doi.org/10.1109/lca.2025.3628325) |
| 79 | DOI:10.1109/sc41405.2020.00024 |  |  | 3 | Adaptive computation／cache-aware MoE, その他システム研究, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/sc41405.2020.00024) |
| 80 | DOI:10.1145/3458864.3467882 |  |  | 3 | Edge／on-device MoE, LLMサービング・スケジューリング・分離実行, other-inference-systems | [source](https://doi.org/10.1145/3458864.3467882) |
| 81 | DOI:10.1145/3630106.3658542 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3630106.3658542) |
| 82 | DOI:10.1145/3725843.3756121 |  |  | 3 | PIM / Near-Data Acceleration, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3725843.3756121) |
| 83 | DOI:10.1145/3779212.3790187 |  |  | 3 | MoE expert offloading / predictive prefetch and cache management, hierarchical-memory-kv-offload-cpu-gpu-attention, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.1145/3779212.3790187) |
| 84 | DOI:10.52202/079017-1601 |  |  | 3 | agent-runtime-sandbox-state-management, agentic GPU kernel generation / harness engineering / profile-guided optimization, agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://doi.org/10.52202/079017-1601) |
| 85 | OpenReview:c8McWs4Av0 |  |  | 3 | Adaptive Expert Computation / Compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=c8McWs4Av0) |
| 86 | OpenReview:LywifFNXV5 |  |  | 3 | CPU長文推論・近似注意, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://openreview.net/forum?id=LywifFNXV5) |
| 87 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 88 | arXiv:2004.02984 |  |  | 3 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2004.02984) |
| 89 | arXiv:2210.09461 |  |  | 3 | inference-systems, on-device LLM / heterogeneous inference / NPU offloading | [source](https://arxiv.org/abs/2210.09461) |
| 90 | arXiv:2306.02272 |  |  | 3 | LLM inference surveys、roofline performance analysis, Weight Quantization / Compression | [source](https://arxiv.org/abs/2306.02272) |
| 91 | arXiv:2310.02226 |  |  | 3 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 92 | arXiv:2311.07226 |  |  | 3 | Expert Prefetch, inference-systems | [source](https://arxiv.org/abs/2311.07226) |
| 93 | arXiv:2403.12422 |  |  | 3 | survey-distributed-training-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.12422) |
| 94 | arXiv:2407.10969 |  |  | 3 | Adaptive Expert Computation / Compression, Conditional Computation | [source](https://arxiv.org/abs/2407.10969) |
| 95 | arXiv:2409.02813 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2409.02813) |
| 96 | arXiv:2412.13171 |  |  | 3 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2412.13171) |
| 97 | arXiv:2503.18773 |  |  | 3 | KV Cache Offload / Recomputation, batch inference / event-driven runtime / MoE serving / offload | [source](https://arxiv.org/abs/2503.18773) |
| 98 | arXiv:2602.08676 |  |  | 3 | Other Inference Systems / Lossless Parallel Decoding, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2602.08676) |
| 99 | DOI:10.1016/s0166-218x |  |  | 3 | KVキャッシュ制約下のLLMサービング・スケジューリング, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1016/s0166-218x) |
| 100 | DOI:10.1145/3085572 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1145/3085572) |
| 101 | DOI:10.1145/3600006.3613139 |  |  | 3 | CPUオフロード / 活性化疎性 / 階層メモリ, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling | [source](https://doi.org/10.1145/3600006.3613139) |
| 102 | DOI:10.1145/3695053.3731051 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://doi.org/10.1145/3695053.3731051) |
| 103 | DOI:10.1162/tacl%5fa%5f00266 |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.1162/tacl%5fa%5f00266) |
| 104 | DOI:10.18653/v1/2024.acl-long.91 |  |  | 3 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2024.acl-long.91) |
| 105 | DOI:10.57967/hf/2497 |  |  | 3 | KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, adaptive-expert-computation-compression | [source](https://doi.org/10.57967/hf/2497) |
| 106 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 107 | OpenReview:MaYzugDmQV |  |  | 3 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 108 | OpenReview:ul4W26KEKz |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://openreview.net/forum?id=ul4W26KEKz) |
| 109 | arXiv:2405.12528 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2405.12528) |
| 110 | arXiv:2606.04101 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2606.04101) |
| 111 | DOI:10.18653/v1/p19-1102 |  |  | 3 | KV-cache compression / attention-based token selection / long-context inference | [source](https://doi.org/10.18653/v1/p19-1102) |
| 112 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 113 | OpenReview:2GmDdhBdDk |  |  | 3 |  | [source](https://openreview.net/forum?id=2GmDdhBdDk) |
| 114 | arXiv:1412.7024 |  |  | 2 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 115 | arXiv:1902.09574 |  |  | 2 | inference-systems, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 116 | arXiv:1906.02041 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1906.02041) |
| 117 | arXiv:1909.11556 |  |  | 2 | inference-systems, speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 118 | arXiv:2005.14187 |  |  | 2 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 119 | arXiv:2104.07012 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 120 | arXiv:2206.01859 |  |  | 2 | inference-systems, post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2206.01859) |
| 121 | arXiv:2303.11366 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 122 | arXiv:2305.11206 |  |  | 2 | KVキャッシュ最適化／適応圧縮, inference-systems | [source](https://arxiv.org/abs/2305.11206) |
| 123 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 124 | arXiv:2307.08072 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 125 | arXiv:2308.07107 |  |  | 2 | KV cache compression / sparse attention / long-context inference, serving-scheduling | [source](https://arxiv.org/abs/2308.07107) |
| 126 | arXiv:2309.08600 |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 127 | arXiv:2309.10691 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2309.10691) |
| 128 | arXiv:2309.14393 |  |  | 2 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 129 | arXiv:2310.00746 |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 130 | arXiv:2310.08041 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2310.08041) |
| 131 | arXiv:2311.00502 |  |  | 2 | CPU推論、行列拡張、異種実行、ルーフライン最適化, inference-systems | [source](https://arxiv.org/abs/2311.00502) |
| 132 | arXiv:2311.09550 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 133 | arXiv:2311.17311 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 134 | arXiv:2312.03788 |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 135 | arXiv:2312.11918 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11918) |
| 136 | arXiv:2401.02038 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 137 | arXiv:2401.13601 |  |  | 2 | LLM inference surveys、roofline performance analysis, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2401.13601) |
| 138 | arXiv:2402.00025 |  |  | 2 | GPU疎行列カーネル／二重疎LLM推論／SIMTマイクロアーキテクチャ, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.00025) |
| 139 | arXiv:2402.09353 |  |  | 2 | Conditional Computation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.09353) |
| 140 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 141 | arXiv:2402.14808 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, inference/11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14808) |
| 142 | arXiv:2402.19427 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2402.19427) |
| 143 | arXiv:2403.06764 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.06764) |
| 144 | arXiv:2403.09347 |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 145 | arXiv:2404.05567 |  |  | 2 | MoE expert pruning / expert merging / redundancy-aware compression / global budget allocation, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2404.05567) |
| 146 | arXiv:2404.09336 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2404.09336) |
| 147 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 148 | arXiv:2405.16587 |  |  | 2 | Conditional Computation, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.16587) |
| 149 | arXiv:2406.00059 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation | [source](https://arxiv.org/abs/2406.00059) |
| 150 | arXiv:2406.04594 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.04594) |
| 151 | arXiv:2406.08673 |  |  | 2 | 大規模分散学習・整合学習基盤, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2406.08673) |
| 152 | arXiv:2406.11939 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2406.11939) |
| 153 | arXiv:2406.18820 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18820) |
| 154 | arXiv:2407.07000 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.07000) |
| 155 | arXiv:2407.09816 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.09816) |
| 156 | arXiv:2407.11511 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2407.11511) |
| 157 | arXiv:2408.04323 |  |  | 2 | Agentic inference and serving runtime, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2408.04323) |
| 158 | arXiv:2409.17146 |  |  | 2 | Adaptive computation／cache-aware MoE, adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/2409.17146) |
| 159 | arXiv:2410.00161 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.00161) |
| 160 | arXiv:2410.03834 |  |  | 2 | llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2410.03834) |
| 161 | arXiv:2410.07985 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.07985) |
| 162 | arXiv:2410.13212 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.13212) |
| 163 | arXiv:2410.14720 |  |  | 2 | MoE compression / expert pruning / neuron-level recombination / expert reconstruction, System-aware KV cache | [source](https://arxiv.org/abs/2410.14720) |
| 164 | arXiv:2410.19274 |  |  | 2 | edge-on-device-llm-systems, flash-capacity-tier-inference | [source](https://arxiv.org/abs/2410.19274) |
| 165 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 166 | arXiv:2411.04468 |  |  | 2 | Agentic Serving Benchmarking, other-inference-systems | [source](https://arxiv.org/abs/2411.04468) |
| 167 | arXiv:2411.04996 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 168 | arXiv:2411.15242 |  |  | 2 | PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management | [source](https://arxiv.org/abs/2411.15242) |
| 169 | arXiv:2412.03603 |  |  | 2 | diffusion language model inference / KV cache / training-free acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.03603) |
| 170 | arXiv:2412.14468 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLMサービング・接頭辞キャッシュ・マルチテナント隔離 | [source](https://arxiv.org/abs/2412.14468) |
| 171 | arXiv:2501.09686 |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2501.09686) |
| 172 | arXiv:2501.12370 |  |  | 2 | MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://arxiv.org/abs/2501.12370) |
| 173 | arXiv:2502.03461 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2502.03461) |
| 174 | arXiv:2502.06768 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2502.06768) |
| 175 | arXiv:2502.11946 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.11946) |
| 176 | arXiv:2502.14317 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, inference-systems | [source](https://arxiv.org/abs/2502.14317) |
| 177 | arXiv:2502.17599 |  |  | 2 | KV cache eviction / multimodal KV cache compression / diversity-aware token selection, inference-systems | [source](https://arxiv.org/abs/2502.17599) |
| 178 | arXiv:2503.08415 |  |  | 2 | KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, other-inference-systems | [source](https://arxiv.org/abs/2503.08415) |
| 179 | arXiv:2503.23100 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2503.23100) |
| 180 | arXiv:2504.05299 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2504.05299) |
| 181 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 182 | arXiv:2504.12463 |  |  | 2 | Expert Prefetch, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2504.12463) |
| 183 | arXiv:2504.16112 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.16112) |
| 184 | arXiv:2504.17768 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.17768) |
| 185 | arXiv:2505.04921 |  |  | 2 | 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2505.04921) |
| 186 | arXiv:2505.07608 |  |  | 2 | kv-cache-optimization-compression, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2505.07608) |
| 187 | arXiv:2505.14631 |  |  | 2 | Conditional Computation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2505.14631) |
| 188 | arXiv:2505.20353 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2505.20353) |
| 189 | arXiv:2506.01048 |  |  | 2 | llm-serving-scheduling-disaggregation, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://arxiv.org/abs/2506.01048) |
| 190 | arXiv:2506.13585 |  |  | 2 | kv-cache-reuse-position-independent-caching, speculative-decoding | [source](https://arxiv.org/abs/2506.13585) |
| 191 | arXiv:2506.20639 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, inference-systems | [source](https://arxiv.org/abs/2506.20639) |
| 192 | arXiv:2507.09942 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2507.09942) |
| 193 | arXiv:2507.16099 |  |  | 2 | inference-systems, 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2507.16099) |
| 194 | arXiv:2507.19595 |  |  | 2 | KV Cache Optimization / Compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2507.19595) |
| 195 | arXiv:2508.07227 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2508.07227) |
| 196 | arXiv:2508.10395 |  |  | 2 | 17-pim-near-data-acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2508.10395) |
| 197 | arXiv:2508.18298 |  |  | 2 | kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18298) |
| 198 | arXiv:2509.18883 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.18883) |
| 199 | arXiv:2509.23951 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.23951) |
| 200 | arXiv:2510.05373 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2510.05373) |
| 201 | arXiv:2510.12633 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.12633) |
| 202 | arXiv:2510.24273 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化 | [source](https://arxiv.org/abs/2510.24273) |
| 203 | arXiv:2511.16108 |  |  | 2 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2511.16108) |
| 204 | arXiv:2511.21689 |  |  | 2 | 14-agentic-inference-serving-runtime, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2511.21689) |
| 205 | arXiv:2512.04123 |  |  | 2 | Agentic Serving Benchmarking, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.04123) |
| 206 | arXiv:2512.12087 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.12087) |
| 207 | arXiv:2512.17077 |  |  | 2 | llm-serving-scheduling-disaggregation, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2512.17077) |
| 208 | arXiv:2601.06521 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2601.06521) |
| 209 | arXiv:2601.09527 |  |  | 2 | LLMサービング・スケジューリング・分離実行, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://arxiv.org/abs/2601.09527) |
| 210 | arXiv:2601.19092 |  |  | 2 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム, dynamic megakernel compilation and GPU task scheduling | [source](https://arxiv.org/abs/2601.19092) |
| 211 | arXiv:2602.02599 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2602.02599) |
| 212 | arXiv:2603.07685 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems | [source](https://arxiv.org/abs/2603.07685) |
| 213 | arXiv:2604.15409 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2604.15409) |
| 214 | arXiv:2606.03928 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2606.03928) |
| 215 | arXiv:2607.04031 |  |  | 2 | 10-kv-cache-offload-recomputation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2607.04031) |
| 216 | DOI:10.1109/cvpr.2018.00286 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, hardware-accelerators | [source](https://doi.org/10.1109/cvpr.2018.00286) |
| 217 | DOI:10.1109/hcs55958.2022.9895629 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1109/hcs55958.2022.9895629) |
| 218 | DOI:10.1109/hotchips.2019.8875654 |  |  | 2 | KV Cache Optimization / Compression, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/hotchips.2019.8875654) |
| 219 | DOI:10.1109/hpca61900.2025.00127 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00127) |
| 220 | DOI:10.1109/inpar.2012.6339596 |  |  | 2 | GPU architecture and tensor-computation orchestration, kernel-runtime-compilation | [source](https://doi.org/10.1109/inpar.2012.6339596) |
| 221 | DOI:10.1109/isca59077.2024.00036 |  |  | 2 | CXL memory pooling / KV cache offload / disaggregated memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/isca59077.2024.00036) |
| 222 | DOI:10.1109/jssc.2022.3200718 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/jssc.2022.3200718) |
| 223 | DOI:10.1109/lca.2026.3695938 |  |  | 2 | HBF / hierarchical memory / KV-cache management / LLM serving, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3695938) |
| 224 | DOI:10.1109/mm.2024.3373763 |  |  | 2 | KV Cache Offload / Recomputation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2024.3373763) |
| 225 | DOI:10.1109/tbdata.2019.2921572 |  |  | 2 | RAG runtime / distributed orchestration / agentic workflows, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/tbdata.2019.2921572) |
| 226 | DOI:10.1109/tpwrs.2022.3173250 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1109/tpwrs.2022.3173250) |
| 227 | DOI:10.1137/0117039 |  |  | 2 | llm-serving-scheduling-disaggregation, オフロード／階層メモリ | [source](https://doi.org/10.1137/0117039) |
| 228 | DOI:10.1145/2485922.2485964 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/2485922.2485964) |
| 229 | DOI:10.1145/3092026 |  |  | 2 | KV-cache scheduling / non-clairvoyant scheduling / LLM serving scheduling, KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching | [source](https://doi.org/10.1145/3092026) |
| 230 | DOI:10.1145/3437801.3441620 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3437801.3441620) |
| 231 | DOI:10.1145/3466752.3480125 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3466752.3480125) |
| 232 | DOI:10.1145/3538643.3539742 |  |  | 2 | 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3538643.3539742) |
| 233 | DOI:10.1145/3575693.3575724 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3575693.3575724) |
| 234 | DOI:10.1145/3582016.3582047 |  |  | 2 | 02-hardware-accelerators, kv-cache-optimization-compression | [source](https://doi.org/10.1145/3582016.3582047) |
| 235 | DOI:10.1145/3620665.3640410 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620665.3640410) |
| 236 | DOI:10.1145/3627703.3629578 |  |  | 2 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, serving-scheduling | [source](https://doi.org/10.1145/3627703.3629578) |
| 237 | DOI:10.1145/3669940.3707231 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/3669940.3707231) |
| 238 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 239 | DOI:10.1145/3710848.3710869 |  |  | 2 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 240 | DOI:10.1145/3731569.3764829 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3731569.3764829) |
| 241 | DOI:10.1145/3779212.3790188 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790188) |
| 242 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 243 | DOI:10.1609/aaai.v38i16.29720 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1609/aaai.v38i16.29720) |
| 244 | DOI:10.18653/v1/2022.acl-long.502 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/2022.acl-long.502) |
| 245 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 246 | DOI:10.18653/v1/2024.findings-emnlp.899 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.899) |
| 247 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 248 | DOI:10.48550/arxiv.2304.07327 |  |  | 2 | KVキャッシュ最適化／適応圧縮, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2304.07327) |
| 249 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 250 | DOI:10.52202/079017-0381 |  |  | 2 | early-exit-offloading-self-speculative-decoding, speculative-decoding | [source](https://doi.org/10.52202/079017-0381) |
| 251 | DOI:10.52202/085713-1380 |  |  | 2 | 99-other-inference-systems, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/085713-1380) |
| 252 | OpenReview:0LXotew9Du |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=0LXotew9Du) |
| 253 | OpenReview:B1VZqjAcYX |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, inference-systems | [source](https://openreview.net/forum?id=B1VZqjAcYX) |
| 254 | OpenReview:cJd1BgZ9CS |  |  | 2 | speculative-decoding, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://openreview.net/forum?id=cJd1BgZ9CS) |
| 255 | OpenReview:EKJhH5D5wA |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=EKJhH5D5wA) |
| 256 | OpenReview:H-VlwsYvVi |  |  | 2 | Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=H-VlwsYvVi) |
| 257 | OpenReview:ho7ZUS1z8A |  |  | 2 | MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / atomic expert pruning / second-order pruning | [source](https://openreview.net/forum?id=ho7ZUS1z8A) |
| 258 | OpenReview:KeHes2SVxs |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://openreview.net/forum?id=KeHes2SVxs) |
| 259 | OpenReview:qCaq3jGb0S |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=qCaq3jGb0S) |
| 260 | OpenReview:rAcgDBdKnP |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=rAcgDBdKnP) |
| 261 | OpenReview:SFN6Wm7YBI |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=SFN6Wm7YBI) |
| 262 | OpenReview:yeeIGM3N6w |  |  | 2 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency | [source](https://openreview.net/forum?id=yeeIGM3N6w) |
| 263 | arXiv:1703.09844 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1703.09844) |
| 264 | arXiv:1905.10650 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1905.10650) |
| 265 | arXiv:1908.09355 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1908.09355) |
| 266 | arXiv:2110.12894 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 267 | arXiv:2210.03057 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 268 | arXiv:2211.15533 |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2211.15533) |
| 269 | arXiv:2303.07129 |  |  | 2 | Edge／on-device MoE | [source](https://arxiv.org/abs/2303.07129) |
| 270 | arXiv:2305.10250 |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 271 | arXiv:2306.13596 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 272 | arXiv:2402.05406 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2402.05406) |
| 273 | arXiv:2403.17887 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2403.17887) |
| 274 | arXiv:2404.08698 |  |  | 2 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2404.08698) |
| 275 | arXiv:2406.15786 |  |  | 2 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2406.15786) |
| 276 | arXiv:2407.11963 |  |  | 2 | serving-scheduling | [source](https://arxiv.org/abs/2407.11963) |
| 277 | arXiv:2409.15647 |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2409.15647) |
| 278 | arXiv:2410.19313 |  |  | 2 | diffusion-llm-inference / caching / low-precision | [source](https://arxiv.org/abs/2410.19313) |
| 279 | arXiv:2412.00402 |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2412.00402) |
| 280 | arXiv:2501.03895 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2501.03895) |
| 281 | arXiv:2502.07780 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next | [source](https://arxiv.org/abs/2502.07780) |
| 282 | arXiv:2505.07686 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2505.07686) |
| 283 | arXiv:2506.06122 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2506.06122) |
| 284 | arXiv:2506.22694 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2506.22694) |
| 285 | arXiv:2511.14617 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2511.14617) |
| 286 | arXiv:2512.18674 |  |  | 2 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.18674) |
| 287 | arXiv:2603.01426 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2603.01426) |
| 288 | arXiv:2604.24432 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2604.24432) |
| 289 | arXiv:2605.09992 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2605.09992) |
| 290 | arXiv:2605.22791 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2605.22791) |
| 291 | DOI:10.1109/infocom53939.2023.10228874 |  |  | 2 | moe-parallelism-communication | [source](https://doi.org/10.1109/infocom53939.2023.10228874) |
| 292 | DOI:10.1145/3241539.3241559 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3241539.3241559) |
| 293 | DOI:10.1145/3786655 |  |  | 2 | kv-cache-reuse-position-independent-caching | [source](https://doi.org/10.1145/3786655) |
| 294 | DOI:10.18653/v1/2020.emnlp-main.550 |  |  | 2 | survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2020.emnlp-main.550) |
| 295 | DOI:10.18653/v1/2023.emnlp-main.232 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.232) |
| 296 | DOI:10.18653/v1/2023.findings-emnlp.936 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://doi.org/10.18653/v1/2023.findings-emnlp.936) |
| 297 | DOI:10.18653/v1/2024.findings-acl.195 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.195) |
| 298 | DOI:10.18653/v1/2025.emnlp-main.844 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2025.emnlp-main.844) |
| 299 | DOI:10.5281/zenodo.1234 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://doi.org/10.5281/zenodo.1234) |
| 300 | OpenReview:6PmJoRfdaK |  |  | 2 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=6PmJoRfdaK) |
| 301 | OpenReview:CQsmMYmlP5T |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=CQsmMYmlP5T) |
| 302 | OpenReview:LWMS4pk2vK |  |  | 2 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=LWMS4pk2vK) |
| 303 | OpenReview:qrMo6R7lOS |  |  | 2 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=qrMo6R7lOS) |
| 304 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 305 | OpenReview:uREj4ZuGJE |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://openreview.net/forum?id=uREj4ZuGJE) |
| 306 | arXiv:2102.12702 |  |  | 2 |  | [source](https://arxiv.org/abs/2102.12702) |
| 307 | arXiv:2310.03533 |  |  | 2 |  | [source](https://arxiv.org/abs/2310.03533) |
| 308 | arXiv:2404.08856 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.08856) |
| 309 | arXiv:2410.15704 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.15704) |
| 310 | arXiv:2505.11594 |  |  | 2 |  | [source](https://arxiv.org/abs/2505.11594) |
| 311 | DOI:10.18653/v1/2026.findings-eacl.31 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2026.findings-eacl.31) |
| 312 | DOI:10.48550/arxiv.2410.11305 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2410.11305) |
| 313 | OpenReview:4D0f16Vwc3 |  |  | 2 |  | [source](https://openreview.net/forum?id=4D0f16Vwc3) |
| 314 | OpenReview:i1uGbfHHpH |  |  | 2 |  | [source](https://openreview.net/forum?id=i1uGbfHHpH) |
| 315 | OpenReview:QV79qiKAjD |  |  | 2 |  | [source](https://openreview.net/forum?id=QV79qiKAjD) |
| 316 | arXiv:1205.2618 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1205.2618) |
| 317 | arXiv:1211.3711 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1211.3711) |
| 318 | arXiv:1301.3781 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 319 | arXiv:1402.3511 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1402.3511) |
| 320 | arXiv:1410.0759 |  |  | 1 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン | [source](https://arxiv.org/abs/1410.0759) |
| 321 | arXiv:1505.05571 |  |  | 1 | MoE数値再現性・決定論的推論・実行時互換性 | [source](https://arxiv.org/abs/1505.05571) |
| 322 | arXiv:1506.03099 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1506.03099) |
| 323 | arXiv:1511.01837 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 324 | arXiv:1511.06939 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 325 | arXiv:1602.01528 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1602.01528) |
| 326 | arXiv:1602.02830 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1602.02830) |
| 327 | arXiv:1603.05118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1603.05118) |
| 328 | arXiv:1604.01696 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1604.01696) |
| 329 | arXiv:1609.05140 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1609.05140) |
| 330 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 331 | arXiv:1611.01578 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1611.01578) |
| 332 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 333 | arXiv:1702.02815 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1702.02815) |
| 334 | arXiv:1703.05160 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 335 | arXiv:1704.04497 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1704.04497) |
| 336 | arXiv:1704.05426 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1704.05426) |
| 337 | arXiv:1705.06963 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 338 | arXiv:1706.03471 |  |  | 1 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://arxiv.org/abs/1706.03471) |
| 339 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 340 | arXiv:1708.04552 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1708.04552) |
| 341 | arXiv:1709.02755 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1709.02755) |
| 342 | arXiv:1710.09437 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1710.09437) |
| 343 | arXiv:1711.02782 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.02782) |
| 344 | arXiv:1711.05073 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1711.05073) |
| 345 | arXiv:1712.01887 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1712.01887) |
| 346 | arXiv:1712.09763 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.09763) |
| 347 | arXiv:1802.05365 |  |  | 1 | Training Offload / Memory Systems | [source](https://arxiv.org/abs/1802.05365) |
| 348 | arXiv:1802.08760 |  |  | 1 | KV cache quantization / long-context inference / activation compression | [source](https://arxiv.org/abs/1802.08760) |
| 349 | arXiv:1804.06028 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/1804.06028) |
| 350 | arXiv:1805.06407 |  |  | 1 | CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/1805.06407) |
| 351 | arXiv:1806.08159 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1806.08159) |
| 352 | arXiv:1807.11205 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1807.11205) |
| 353 | arXiv:1808.09121 |  |  | 1 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling | [source](https://arxiv.org/abs/1808.09121) |
| 354 | arXiv:1809.04281 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1809.04281) |
| 355 | arXiv:1810.03264 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.03264) |
| 356 | arXiv:1810.09305 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1810.09305) |
| 357 | arXiv:1811.03115 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/1811.03115) |
| 358 | arXiv:1812.01608 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1812.01608) |
| 359 | arXiv:1902.00732 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1902.00732) |
| 360 | arXiv:1902.05613 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.05613) |
| 361 | arXiv:1902.10186 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1902.10186) |
| 362 | arXiv:1903.01699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1903.01699) |
| 363 | arXiv:1904.06376 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1904.06376) |
| 364 | arXiv:1905.00537 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1905.00537) |
| 365 | arXiv:1905.07799 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 366 | arXiv:1906.05714 |  |  | 1 | 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/1906.05714) |
| 367 | arXiv:1907.01989 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1907.01989) |
| 368 | arXiv:1908.08593 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1908.08593) |
| 369 | arXiv:1908.11365 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1908.11365) |
| 370 | arXiv:1909.03368 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1909.03368) |
| 371 | arXiv:1909.10351 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1909.10351) |
| 372 | arXiv:1910.04732 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1910.04732) |
| 373 | arXiv:1910.06360 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 374 | arXiv:1911.02116 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1911.02116) |
| 375 | arXiv:1911.04610 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1911.04610) |
| 376 | arXiv:1911.08772 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1911.08772) |
| 377 | arXiv:2001.01072 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/2001.01072) |
| 378 | arXiv:2002.07376 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.07376) |
| 379 | arXiv:2002.09919 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.09919) |
| 380 | arXiv:2002.10957 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.10957) |
| 381 | arXiv:2003.03033 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.03033) |
| 382 | arXiv:2003.08295 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.08295) |
| 383 | arXiv:2004.03329 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2004.03329) |
| 384 | arXiv:2004.08900 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 385 | arXiv:2004.11867 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 386 | arXiv:2005.00770 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00770) |
| 387 | arXiv:2005.07647 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2005.07647) |
| 388 | arXiv:2006.06762 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2006.06762) |
| 389 | arXiv:2006.10901 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2006.10901) |
| 390 | arXiv:2006.12467 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/2006.12467) |
| 391 | arXiv:2007.07779 |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 392 | arXiv:2008.00051 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2008.00051) |
| 393 | arXiv:2009.06106 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 394 | arXiv:2009.07253 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2009.07253) |
| 395 | arXiv:2009.08553 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2009.08553) |
| 396 | arXiv:2010.02394 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 397 | arXiv:2010.03093 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.03093) |
| 398 | arXiv:2010.03768 |  |  | 1 | augmented LLM serving / KV cache management / predictive scheduling / vLLM | [source](https://arxiv.org/abs/2010.03768) |
| 399 | arXiv:2010.11125 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2010.11125) |
| 400 | arXiv:2010.14701 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2010.14701) |
| 401 | arXiv:2011.04006 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2011.04006) |
| 402 | arXiv:2011.13456 |  |  | 1 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2011.13456) |
| 403 | arXiv:2012.12624 |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 404 | arXiv:2012.15701 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2012.15701) |
| 405 | arXiv:2101.01321 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2101.01321) |
| 406 | arXiv:2102.01672 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2102.01672) |
| 407 | arXiv:2102.07835 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2102.07835) |
| 408 | arXiv:2102.08942 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2102.08942) |
| 409 | arXiv:2103.03330 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2103.03330) |
| 410 | arXiv:2103.13076 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2103.13076) |
| 411 | arXiv:2104.12470 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2104.12470) |
| 412 | arXiv:2105.05944 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2105.05944) |
| 413 | arXiv:2105.11098 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2105.11098) |
| 414 | arXiv:2105.14940 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.14940) |
| 415 | arXiv:2106.04489 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.04489) |
| 416 | arXiv:2106.07139 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2106.07139) |
| 417 | arXiv:2106.10595 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2106.10595) |
| 418 | arXiv:2107.05407 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/2107.05407) |
| 419 | arXiv:2107.13686 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2107.13686) |
| 420 | arXiv:2108.08877 |  |  | 1 | 07-kv-キャッシュ-optimization-compression | [source](https://arxiv.org/abs/2108.08877) |
| 421 | arXiv:2109.04404 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2109.04404) |
| 422 | arXiv:2109.09115 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2109.09115) |
| 423 | arXiv:2109.11295 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2109.11295) |
| 424 | arXiv:2110.04366 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.04366) |
| 425 | arXiv:2110.08419 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2110.08419) |
| 426 | arXiv:2110.15191 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2110.15191) |
| 427 | arXiv:2111.00680 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2111.00680) |
| 428 | arXiv:2112.01488 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2112.01488) |
| 429 | arXiv:2112.06598 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2112.06598) |
| 430 | arXiv:2112.08608 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.08608) |
| 431 | arXiv:2112.14397 |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 432 | arXiv:2201.06618 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2201.06618) |
| 433 | arXiv:2202.01279 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.01279) |
| 434 | arXiv:2202.05747 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2202.05747) |
| 435 | arXiv:2202.08904 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2202.08904) |
| 436 | arXiv:2202.13914 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.13914) |
| 437 | arXiv:2203.01670 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.01670) |
| 438 | arXiv:2203.05740 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2203.05740) |
| 439 | arXiv:2203.09509 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.09509) |
| 440 | arXiv:2203.14680 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2203.14680) |
| 441 | arXiv:2204.03324 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.03324) |
| 442 | arXiv:2204.06683 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 443 | arXiv:2204.09656 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.09656) |
| 444 | arXiv:2205.00445 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.00445) |
| 445 | arXiv:2205.05243 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2205.05243) |
| 446 | arXiv:2205.10364 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10364) |
| 447 | arXiv:2205.11916 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2205.11916) |
| 448 | arXiv:2205.13603 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2205.13603) |
| 449 | arXiv:2206.08474 |  |  | 1 | adaptive expert computation / expert pruning / depth-aware MoE compression | [source](https://arxiv.org/abs/2206.08474) |
| 450 | arXiv:2207.05952 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 451 | arXiv:2207.12598 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2207.12598) |
| 452 | arXiv:2208.03299 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2208.03299) |
| 453 | arXiv:2208.09225 |  |  | 1 | 投機的デコード・バッチ推論 | [source](https://arxiv.org/abs/2208.09225) |
| 454 | arXiv:2209.07858 |  |  | 1 | Mixture-of-Experts inference / processing-in-memory / heterogeneous scheduling / expert placement | [source](https://arxiv.org/abs/2209.07858) |
| 455 | arXiv:2209.12356 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2209.12356) |
| 456 | arXiv:2210.02747 |  |  | 1 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference | [source](https://arxiv.org/abs/2210.02747) |
| 457 | arXiv:2210.05709 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2210.05709) |
| 458 | arXiv:2210.08674 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2210.08674) |
| 459 | arXiv:2210.13438 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2210.13438) |
| 460 | arXiv:2210.15373 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.15373) |
| 461 | arXiv:2211.01267 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.01267) |
| 462 | arXiv:2211.06033 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 463 | arXiv:2211.09699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 464 | arXiv:2211.15089 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 465 | arXiv:2212.02855 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2212.02855) |
| 466 | arXiv:2212.04088 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.04088) |
| 467 | arXiv:2212.05238 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.05238) |
| 468 | arXiv:2212.10325 |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2212.10325) |
| 469 | arXiv:2212.10509 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 470 | arXiv:2212.12017 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 471 | arXiv:2301.04104 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.04104) |
| 472 | arXiv:2301.06672 |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2301.06672) |
| 473 | arXiv:2301.08984 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2301.08984) |
| 474 | arXiv:2301.12503 |  |  | 1 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2301.12503) |
| 475 | arXiv:2302.02451 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.02451) |
| 476 | arXiv:2302.04863 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.04863) |
| 477 | arXiv:2302.07080 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2302.07080) |
| 478 | arXiv:2302.10025 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2302.10025) |
| 479 | arXiv:2302.12066 |  |  | 1 | foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2302.12066) |
| 480 | arXiv:2302.13214 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.13214) |
| 481 | arXiv:2303.02141 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2303.02141) |
| 482 | arXiv:2303.05510 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2303.05510) |
| 483 | arXiv:2303.06296 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2303.06296) |
| 484 | arXiv:2303.10512 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.10512) |
| 485 | arXiv:2303.14524 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2303.14524) |
| 486 | arXiv:2303.16634 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2303.16634) |
| 487 | arXiv:2303.17605 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2303.17605) |
| 488 | arXiv:2304.02643 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2304.02643) |
| 489 | arXiv:2304.03271 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/2304.03271) |
| 490 | arXiv:2304.04556 |  |  | 1 | KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://arxiv.org/abs/2304.04556) |
| 491 | arXiv:2304.08243 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2304.08243) |
| 492 | arXiv:2304.09433 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2304.09433) |
| 493 | arXiv:2304.11062 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2304.11062) |
| 494 | arXiv:2304.15010 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 495 | arXiv:2305.02538 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 496 | arXiv:2305.03726 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.03726) |
| 497 | arXiv:2305.06942 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2305.06942) |
| 498 | arXiv:2305.09098 |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.09098) |
| 499 | arXiv:2305.10435 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2305.10435) |
| 500 | arXiv:2305.13304 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.13304) |

## Machine-readable

同じ割当は [worker-worklist-30.json](worker-worklist-30.json) にあります。

