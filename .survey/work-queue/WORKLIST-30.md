# Scheduled worker :30 worklist

Worker: `scheduled-chat-30`  
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

未判定総数: **5446** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.48550/arxiv.2408.11850 |  |  | 15 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative Decoding / Parallel Inference Systems, inference-systems, speculative-decoding, speculative-decoding-moe, 投機的デコード／動的候補木／高同時実行LLMサービング | [source](https://doi.org/10.48550/arxiv.2408.11850) |
| 2 | DOI:10.1145/3669940.3707267 |  |  | 13 | KV Cache Optimization / Compression, LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Offload / Hierarchical Memory, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, hierarchical-memory-kv-offload-cpu-gpu-attention, moe-inference-expert-placement-caching, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://doi.org/10.1145/3669940.3707267) |
| 3 | arXiv:2312.04985 |  |  | 12 | KV cache compression / sparse attention / long-context inference, KV cache quantization / long-context inference / activation compression, Offload / Hierarchical Memory, Sparse Attention, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2312.04985) |
| 4 | arXiv:2304.01089 |  |  | 11 | Conditional Computation, Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 5 | arXiv:2407.12820 |  |  | 11 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://arxiv.org/abs/2407.12820) |
| 6 | DOI:10.48550/arxiv.2404.07413 |  |  | 10 | 02-adaptive-expert-computation-compression, Adaptive computation／cache-aware MoE, MoE compression / expert merging / output approximation / least-squares compression, MoE predictive expert placement / replication / SiDA-MoE, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, moe-parallelism-communication, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2404.07413) |
| 7 | DOI:10.48550/arxiv.2501.14743 |  |  | 10 | 11-llm-serving-scheduling-disaggregation, 12-moe-parallelism-communication, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Offload / Recomputation, KVキャッシュオフロード／階層メモリ, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.48550/arxiv.2501.14743) |
| 8 | arXiv:1808.08745 |  |  | 9 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 9 | arXiv:2405.21060 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化, PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management, kv-cache, kv-cache-offload-recomputation, linear attention / delta-rule associative memory / state-space models / Bayesian filtering, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2405.21060) |
| 10 | arXiv:2309.04255 |  |  | 9 | 10-kv-cache-offload-recomputation, LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, offload-hierarchical-memory, on-device LLM / heterogeneous inference / NPU offloading, survey-speculative-decoding | [source](https://arxiv.org/abs/2309.04255) |
| 11 | OpenReview:qrwe7XHTmYb |  |  | 9 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, LLM Serving / Multi-Model Serving / Memory Disaggregation, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, Speculative decoding × MoE, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=qrwe7XHTmYb) |
| 12 | arXiv:2405.16406 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 17-pim-near-data-acceleration, FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, KV cache quantization / rotation-based compression / MoE expert offloading / consumer local inference, kv-cache-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2405.16406) |
| 13 | arXiv:2311.13581 |  |  | 9 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2311.13581) |
| 14 | arXiv:2309.12307 |  |  | 8 | Conditional Computation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference, KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ, cpu-offload, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, multi-tenant LoRA serving / CPU-assisted inference / rank-aware scheduling | [source](https://arxiv.org/abs/2309.12307) |
| 15 | arXiv:2308.00352 |  |  | 8 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, survey-long-context-serving, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://arxiv.org/abs/2308.00352) |
| 16 | arXiv:2112.11446 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 17 | arXiv:2512.20856 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 99-other-inference-systems, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, PIM / Near-Data Acceleration, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2512.20856) |
| 18 | DOI:10.64434/tml.20250910 |  |  | 8 | Agentic Serving Benchmarking, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 19 | DOI:10.1145/3772052.3772239 |  |  | 8 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation, multi-SLO serving / speculative decoding / SLO-aware scheduling / hardware-aware token budgeting, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://doi.org/10.1145/3772052.3772239) |
| 20 | arXiv:1607.06450 |  |  | 7 | Conditional Computation, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 21 | arXiv:2406.00515 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, LLM inference kernel safety / CUDA symbolic execution / model-aware verification, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, kernel-runtime-compilation, serving-scheduling | [source](https://arxiv.org/abs/2406.00515) |
| 22 | arXiv:2101.00190 |  |  | 7 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2101.00190) |
| 23 | arXiv:2408.11743 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 24 | DOI:10.18653/v1/k16-1028 |  |  | 7 | Speculative decoding × MoE, inference-systems, survey-speculative-decoding, 投機的デコード／動的候補木／高同時実行LLMサービング, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/k16-1028) |
| 25 | arXiv:2203.14685 |  |  | 7 | Adaptive Expert Computation / Compression, MoE推論・エキスパート配置・全対全通信スケジューリング・異種GPU, survey-moe-inference-optimization, その他システム研究 | [source](https://arxiv.org/abs/2203.14685) |
| 26 | arXiv:2310.15141 |  |  | 7 | LLM inference surveys、roofline performance analysis, inference-systems, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 27 | arXiv:2509.16941 |  |  | 7 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2509.16941) |
| 28 | arXiv:2402.14034 |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 29 | arXiv:2502.02737 |  |  | 6 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2502.02737) |
| 30 | arXiv:2110.03742 |  |  | 6 | Edge／on-device MoE, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference / expert pruning / language-specific expert specialization, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2110.03742) |
| 31 | arXiv:2511.21631 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / dynamic MoE routing / gating uncertainty, flash-capacity-tier-inference | [source](https://arxiv.org/abs/2511.21631) |
| 32 | arXiv:2303.08302 |  |  | 6 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Weight Quantization / Compression, offload-hierarchical-memory, survey-low-bit-llm | [source](https://arxiv.org/abs/2303.08302) |
| 33 | arXiv:2503.17407 |  |  | 6 | 10-kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2503.17407) |
| 34 | DOI:10.5281/zenodo.5371628 |  |  | 6 | KV Cache Optimization / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.5281/zenodo.5371628) |
| 35 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 6 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 36 | OpenReview:RkRrPp7GKO |  |  | 6 | KV Cache Optimization / Compression, kv-cache-offload-recomputation, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=RkRrPp7GKO) |
| 37 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 38 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 39 | arXiv:2210.11416 |  |  | 5 | Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, inference-systems, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 40 | arXiv:2504.21318 |  |  | 5 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 41 | DOI:10.1145/3676641.3716278 |  |  | 5 | 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 42 | OpenReview:7kQjbCQwtT |  |  | 5 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-inference-expert-offloading, moe-quantization-compression, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=7kQjbCQwtT) |
| 43 | arXiv:2212.10560 |  |  | 5 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2212.10560) |
| 44 | DOI:10.1162/tacl_a_00023 |  |  | 5 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1162/tacl_a_00023) |
| 45 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 46 | arXiv:2403.12031 |  |  | 5 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 47 | arXiv:2504.19516 |  |  | 5 | llm-serving-scheduling-disaggregation, serving-scheduling, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.19516) |
| 48 | OpenReview:uccHPGDlao |  |  | 5 | 05-speculative-decoding-moe, Speculative decoding × MoE, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 49 | OpenReview:EytBpUGB1Z |  |  | 5 | KV Cache Optimization / Compression | [source](https://openreview.net/forum?id=EytBpUGB1Z) |
| 50 | arXiv:2108.12409 |  |  | 4 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLM inference surveys、roofline performance analysis, cpu-offload, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2108.12409) |
| 51 | arXiv:2402.14905 |  |  | 4 | 10-kv-cache-offload-recomputation, kv-cache-optimization-compression, offload-hierarchical-memory, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2402.14905) |
| 52 | DOI:10.1145/3503222.3507778 |  |  | 4 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.1145/3503222.3507778) |
| 53 | DOI:10.18653/v1/2025.acl-long.1126 |  |  | 4 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics, dynamic-pd-disaggregation, kv-cache-offload-recomputation | [source](https://doi.org/10.18653/v1/2025.acl-long.1126) |
| 54 | OpenReview:4exx1hUffq |  |  | 4 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, Speculative decoding × MoE, other-inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=4exx1hUffq) |
| 55 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 56 | arXiv:1811.00937 |  |  | 4 | Adaptive Expert Computation / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1811.00937) |
| 57 | DOI:10.1162/tacl_a_00276 |  |  | 4 | Speculative Decoding / Parallel Inference Systems, inference-systems, survey-speculative-decoding | [source](https://doi.org/10.1162/tacl_a_00276) |
| 58 | OpenReview:cSimKw5p6R |  |  | 4 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, agentic workflow serving / workflow physical planning / adaptive serving, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://openreview.net/forum?id=cSimKw5p6R) |
| 59 | arXiv:2402.18013 |  |  | 4 | llm-serving-scheduling-disaggregation, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2402.18013) |
| 60 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 61 | arXiv:2306.02561 |  |  | 3 | LLM routing、hybrid inference、quality-aware model selection, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 62 | arXiv:2402.02244 |  |  | 3 | LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, Sparse Attention, survey-long-context-serving | [source](https://arxiv.org/abs/2402.02244) |
| 63 | arXiv:2404.14897 |  |  | 3 | inference-systems, speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2404.14897) |
| 64 | arXiv:2411.11055 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 65 | arXiv:2511.00739 |  |  | 3 | LLM Serving / Scheduling / Disaggregation, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2511.00739) |
| 66 | DOI:10.1007/s11432-024-4235-6 |  |  | 3 | MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / null experts / data sparsity / multimodal MoE, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1007/s11432-024-4235-6) |
| 67 | DOI:10.1109/lca.2023.3333759 |  |  | 3 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, low-bit VLM inference / microscaling / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/lca.2023.3333759) |
| 68 | DOI:10.1109/micro56248.2022.00051 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, kv-cache-memory | [source](https://doi.org/10.1109/micro56248.2022.00051) |
| 69 | DOI:10.1109/tmc.2024.3513457 |  |  | 3 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, hardware-accelerators | [source](https://doi.org/10.1109/tmc.2024.3513457) |
| 70 | DOI:10.1145/3489517.3530428 |  |  | 3 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3489517.3530428) |
| 71 | DOI:10.1145/3676641.3716011 |  |  | 3 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, MoE serving / attention-MoE disaggregation / asynchronous inference, serving-scheduling | [source](https://doi.org/10.1145/3676641.3716011) |
| 72 | DOI:10.1145/3731569.3764808 |  |  | 3 | edge-on-device-llm-systems, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764808) |
| 73 | DOI:10.48550/arxiv.2507.17702 |  |  | 3 | adaptive expert computation / compression; end-side sparse MoE, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://doi.org/10.48550/arxiv.2507.17702) |
| 74 | OpenReview:1qvx610Cu7 |  |  | 3 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 75 | OpenReview:c8McWs4Av0 |  |  | 3 | Adaptive Expert Computation / Compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=c8McWs4Av0) |
| 76 | OpenReview:LywifFNXV5 |  |  | 3 | CPU長文推論・近似注意, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://openreview.net/forum?id=LywifFNXV5) |
| 77 | OpenReview:TrjbxzRcnf- |  |  | 3 | KVキャッシュ・注意アーキテクチャ, KVキャッシュ再利用／圧縮／ネットワーク転送, other-inference-systems | [source](https://openreview.net/forum?id=TrjbxzRcnf-) |
| 78 | OpenReview:z3JZzu9EA3 |  |  | 3 | KV Cache Optimization / Compression, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=z3JZzu9EA3) |
| 79 | arXiv:2207.07061 |  |  | 3 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2207.07061) |
| 80 | arXiv:2309.05463 |  |  | 3 | survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 81 | arXiv:2311.07226 |  |  | 3 | Expert Prefetch, inference-systems | [source](https://arxiv.org/abs/2311.07226) |
| 82 | arXiv:2402.09025 |  |  | 3 | Conditional Computation, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.09025) |
| 83 | arXiv:2407.10969 |  |  | 3 | Adaptive Expert Computation / Compression, Conditional Computation | [source](https://arxiv.org/abs/2407.10969) |
| 84 | arXiv:2502.02617 |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2502.02617) |
| 85 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 86 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 87 | DOI:10.1145/3581784.3607062 |  |  | 3 | Sparse Attention, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1145/3581784.3607062) |
| 88 | DOI:10.1145/3719330.3721230 |  |  | 3 | 08-edge-on-device-llm-systems, KV Cache Offload / Recomputation | [source](https://doi.org/10.1145/3719330.3721230) |
| 89 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 3 | Speculative Decoding, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 90 | DOI:10.18653/v1/d19-1454 |  |  | 3 | Conditional Computation, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/d19-1454) |
| 91 | DOI:10.48550/arxiv.2412.18910 |  |  | 3 | 05-speculative-decoding-moe, inference-systems | [source](https://doi.org/10.48550/arxiv.2412.18910) |
| 92 | OpenReview:ayi7qezU87 |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://openreview.net/forum?id=ayi7qezU87) |
| 93 | OpenReview:LKEJPySnlt |  |  | 3 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=LKEJPySnlt) |
| 94 | OpenReview:PxoFut3dWW |  |  | 3 | Adaptive Expert Computation / Compression, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=PxoFut3dWW) |
| 95 | OpenReview:uBaFH7aQnC |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=uBaFH7aQnC) |
| 96 | arXiv:2405.14105 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2405.14105) |
| 97 | DOI:10.14778/3551793.3551828 |  |  | 3 | その他システム研究 | [source](https://doi.org/10.14778/3551793.3551828) |
| 98 | OpenReview:hslOzRxzXL |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://openreview.net/forum?id=hslOzRxzXL) |
| 99 | arXiv:1311.2540 |  |  | 2 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 100 | arXiv:1902.09574 |  |  | 2 | inference-systems, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 101 | arXiv:1906.02041 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1906.02041) |
| 102 | arXiv:1909.11556 |  |  | 2 | inference-systems, speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 103 | arXiv:2004.11886 |  |  | 2 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2004.11886) |
| 104 | arXiv:2104.07012 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 105 | arXiv:2206.01859 |  |  | 2 | inference-systems, post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2206.01859) |
| 106 | arXiv:2305.05252 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 107 | arXiv:2306.02272 |  |  | 2 | LLM inference surveys、roofline performance analysis, Weight Quantization / Compression | [source](https://arxiv.org/abs/2306.02272) |
| 108 | arXiv:2306.13549 |  |  | 2 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2306.13549) |
| 109 | arXiv:2307.08072 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 110 | arXiv:2308.07107 |  |  | 2 | KV cache compression / sparse attention / long-context inference, serving-scheduling | [source](https://arxiv.org/abs/2308.07107) |
| 111 | arXiv:2309.05516 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 112 | arXiv:2309.10400 |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 113 | arXiv:2309.13879 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, other-inference-systems | [source](https://arxiv.org/abs/2309.13879) |
| 114 | arXiv:2309.16739 |  |  | 2 | inference-systems, multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2309.16739) |
| 115 | arXiv:2310.02226 |  |  | 2 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 116 | arXiv:2310.17157 |  |  | 2 | Conditional Computation, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2310.17157) |
| 117 | arXiv:2311.01635 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.01635) |
| 118 | arXiv:2311.11501 |  |  | 2 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2311.11501) |
| 119 | arXiv:2311.17541 |  |  | 2 | agentic serving / workflow-aware scheduling / memory-aware dispatch, other-inference-systems | [source](https://arxiv.org/abs/2311.17541) |
| 120 | arXiv:2312.04511 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2312.04511) |
| 121 | arXiv:2312.13558 |  |  | 2 | LLM inference surveys、roofline performance analysis, 長文脈注意・KVキャッシュ最適化 / 近似近傍検索・深層ハッシュ | [source](https://arxiv.org/abs/2312.13558) |
| 122 | arXiv:2401.02038 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 123 | arXiv:2401.13601 |  |  | 2 | LLM inference surveys、roofline performance analysis, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2401.13601) |
| 124 | arXiv:2402.00025 |  |  | 2 | GPU疎行列カーネル／二重疎LLM推論／SIMTマイクロアーキテクチャ, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.00025) |
| 125 | arXiv:2402.03216 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 126 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 127 | arXiv:2402.14762 |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 128 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 129 | arXiv:2403.05525 |  |  | 2 | Quantization × MoE × Offload, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.05525) |
| 130 | arXiv:2403.09032 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 131 | arXiv:2404.03605 |  |  | 2 | Conditional Computation, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2404.03605) |
| 132 | arXiv:2404.07972 |  |  | 2 | 14-agentic-inference-serving-runtime, KVキャッシュオフロード・再計算 | [source](https://arxiv.org/abs/2404.07972) |
| 133 | arXiv:2404.14619 |  |  | 2 | survey-edge-llm, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2404.14619) |
| 134 | arXiv:2405.16587 |  |  | 2 | Conditional Computation, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.16587) |
| 135 | arXiv:2406.00059 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation | [source](https://arxiv.org/abs/2406.00059) |
| 136 | arXiv:2406.04127 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2406.04127) |
| 137 | arXiv:2406.07394 |  |  | 2 | Edge／on-device MoE, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.07394) |
| 138 | arXiv:2406.11931 |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.11931) |
| 139 | arXiv:2406.18629 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2406.18629) |
| 140 | arXiv:2407.04014 |  |  | 2 | llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 141 | arXiv:2407.09141 |  |  | 2 | 06-moe-quantization-compression, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2407.09141) |
| 142 | arXiv:2407.11239 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2407.11239) |
| 143 | arXiv:2407.17789 |  |  | 2 | 14-agentic-inference-serving-runtime, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2407.17789) |
| 144 | arXiv:2409.06857 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, offload-hierarchical-memory | [source](https://arxiv.org/abs/2409.06857) |
| 145 | arXiv:2409.17481 |  |  | 2 | Conditional Computation, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2409.17481) |
| 146 | arXiv:2410.00161 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.00161) |
| 147 | arXiv:2410.05589 |  |  | 2 | 投機的デコード／動的LLMサービング／GPU空間多重化, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2410.05589) |
| 148 | arXiv:2410.10762 |  |  | 2 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.10762) |
| 149 | arXiv:2410.13461 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2410.13461) |
| 150 | arXiv:2410.17840 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.17840) |
| 151 | arXiv:2410.24164 |  |  | 2 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference, early-exit-offloading-self-speculative-decoding | [source](https://arxiv.org/abs/2410.24164) |
| 152 | arXiv:2411.02335 |  |  | 2 | MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, adaptive expert computation / compression; end-side sparse MoE | [source](https://arxiv.org/abs/2411.02335) |
| 153 | arXiv:2411.04965 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2411.04965) |
| 154 | arXiv:2411.15100 |  |  | 2 | kv-cache-optimization-compression, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2411.15100) |
| 155 | arXiv:2412.01447 |  |  | 2 | inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2412.01447) |
| 156 | arXiv:2412.12488 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.12488) |
| 157 | arXiv:2412.14468 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLMサービング・接頭辞キャッシュ・マルチテナント隔離 | [source](https://arxiv.org/abs/2412.14468) |
| 158 | arXiv:2501.10714 |  |  | 2 | Quantization × MoE × Offload, その他システム研究 | [source](https://arxiv.org/abs/2501.10714) |
| 159 | arXiv:2502.01662 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2502.01662) |
| 160 | arXiv:2502.06768 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2502.06768) |
| 161 | arXiv:2502.11946 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.11946) |
| 162 | arXiv:2502.15304 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2502.15304) |
| 163 | arXiv:2502.17419 |  |  | 2 | Conditional Computation, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2502.17419) |
| 164 | arXiv:2503.07545 |  |  | 2 | LLM配信／KVキャッシュ制約／連続バッチ処理／待ち行列・力学系, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2503.07545) |
| 165 | arXiv:2503.09567 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2503.09567) |
| 166 | arXiv:2503.23100 |  |  | 2 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2503.23100) |
| 167 | arXiv:2504.04823 |  |  | 2 | kernel-runtime-compilation, 端末MoE推論、エキスパートオフロード、無損失圧縮、階層キャッシュ、異種資源スケジューリング | [source](https://arxiv.org/abs/2504.04823) |
| 168 | arXiv:2504.09014 |  |  | 2 | LLMサービング／スケジューリング／分離実行, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2504.09014) |
| 169 | arXiv:2504.12463 |  |  | 2 | Expert Prefetch, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2504.12463) |
| 170 | arXiv:2504.16112 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.16112) |
| 171 | arXiv:2504.17768 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.17768) |
| 172 | arXiv:2505.04921 |  |  | 2 | 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論, 拡散型LLM推論・特徴キャッシュ・KVキャッシュ・並列復号 | [source](https://arxiv.org/abs/2505.04921) |
| 173 | arXiv:2505.07608 |  |  | 2 | kv-cache-optimization-compression, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2505.07608) |
| 174 | arXiv:2505.16552 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2505.16552) |
| 175 | arXiv:2506.01048 |  |  | 2 | llm-serving-scheduling-disaggregation, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://arxiv.org/abs/2506.01048) |
| 176 | arXiv:2506.14038 |  |  | 2 | moe-quantization-compression, その他システム研究 | [source](https://arxiv.org/abs/2506.14038) |
| 177 | arXiv:2507.07120 |  |  | 2 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics | [source](https://arxiv.org/abs/2507.07120) |
| 178 | arXiv:2507.14111 |  |  | 2 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2507.14111) |
| 179 | arXiv:2507.19595 |  |  | 2 | KV Cache Optimization / Compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2507.19595) |
| 180 | arXiv:2508.06447 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, System-aware KV cache | [source](https://arxiv.org/abs/2508.06447) |
| 181 | arXiv:2508.08712 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.08712) |
| 182 | arXiv:2508.16712 |  |  | 2 | LLM serving scheduling / chunked prefill / MoE inference, llm-serving-systems | [source](https://arxiv.org/abs/2508.16712) |
| 183 | arXiv:2509.01142 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2509.01142) |
| 184 | arXiv:2509.23202 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2509.23202) |
| 185 | arXiv:2510.00231 |  |  | 2 | KV cache compression / KV eviction / probabilistic inference / importance sampling, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2510.00231) |
| 186 | arXiv:2510.05373 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2510.05373) |
| 187 | arXiv:2510.12633 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.12633) |
| 188 | arXiv:2510.24273 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化 | [source](https://arxiv.org/abs/2510.24273) |
| 189 | arXiv:2511.16108 |  |  | 2 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2511.16108) |
| 190 | arXiv:2511.21689 |  |  | 2 | 14-agentic-inference-serving-runtime, multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2511.21689) |
| 191 | arXiv:2512.04123 |  |  | 2 | Agentic Serving Benchmarking, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.04123) |
| 192 | arXiv:2512.12087 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.12087) |
| 193 | arXiv:2512.17077 |  |  | 2 | llm-serving-scheduling-disaggregation, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2512.17077) |
| 194 | arXiv:2601.06521 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2601.06521) |
| 195 | arXiv:2601.10088 |  |  | 2 | hardware-accelerators, 分離型LLMサービング／予測型スケジューリング／KVメモリ認識型配置 | [source](https://arxiv.org/abs/2601.10088) |
| 196 | arXiv:2601.21351 |  |  | 2 | MoE serving / Attention-FFN disaggregation / analytical provisioning / hardware-aware deployment search, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2601.21351) |
| 197 | arXiv:2602.08005 |  |  | 2 | System-aware KV cache, kv-cache-memory-management | [source](https://arxiv.org/abs/2602.08005) |
| 198 | arXiv:2603.18016 |  |  | 2 | 05-speculative-decoding-moe, LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse | [source](https://arxiv.org/abs/2603.18016) |
| 199 | arXiv:2605.04595 |  |  | 2 | KVキャッシュ制約下のLLMサービング・スケジューリング, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2605.04595) |
| 200 | arXiv:2606.17034 |  |  | 2 | KVキャッシュ再利用・選択的再計算・RAGキャッシュ編集, inference/14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2606.17034) |
| 201 | DOI:10.1016/j.parco.2015.09.001 |  |  | 2 | MoE数値再現性・決定論的推論・実行時互換性, hardware-accelerators | [source](https://doi.org/10.1016/j.parco.2015.09.001) |
| 202 | DOI:10.1109/dac63849.2025.11132870 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, offload-hierarchical-memory | [source](https://doi.org/10.1109/dac63849.2025.11132870) |
| 203 | DOI:10.1109/hcs59251.2023.10254717 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, cpu-offload | [source](https://doi.org/10.1109/hcs59251.2023.10254717) |
| 204 | DOI:10.1109/hpca47549.2020.00030 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, kv-cache-memory | [source](https://doi.org/10.1109/hpca47549.2020.00030) |
| 205 | DOI:10.1109/iccv.2019.00038 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation | [source](https://doi.org/10.1109/iccv.2019.00038) |
| 206 | DOI:10.1109/isca45697.2020.00047 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/isca45697.2020.00047) |
| 207 | DOI:10.1109/ispass.2019.00042 |  |  | 2 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, 長文推論・KVキャッシュ先読み・要求パッキング・オンチップメモリ・HBM帯域最適化 | [source](https://doi.org/10.1109/ispass.2019.00042) |
| 208 | DOI:10.1109/lca.2025.3566692 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/lca.2025.3566692) |
| 209 | DOI:10.1109/micro61859.2024.00021 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1109/micro61859.2024.00021) |
| 210 | DOI:10.1109/mm.2024.3420728 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://doi.org/10.1109/mm.2024.3420728) |
| 211 | DOI:10.1109/tc.1985.6312218 |  |  | 2 | survey-speculative-decoding, 投機的復号 / 無損失復号高速化 | [source](https://doi.org/10.1109/tc.1985.6312218) |
| 212 | DOI:10.1115/1.3662552 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1115/1.3662552) |
| 213 | DOI:10.1145/1966445.1966473 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, Expert Prefetch | [source](https://doi.org/10.1145/1966445.1966473) |
| 214 | DOI:10.1145/2517349.2522716 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/2517349.2522716) |
| 215 | DOI:10.1145/3297858.3304043 |  |  | 2 | hardware-accelerators, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3297858.3304043) |
| 216 | DOI:10.1145/3445814.3446714 |  |  | 2 | agent-runtime-sandbox-state-management, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3445814.3446714) |
| 217 | DOI:10.1145/3492321.3519584 |  |  | 2 | MoE serving resilience / decoupled attention-expert serving / KV checkpointing, 学習チェックポイント・GPU-CPU転送・SSD永続化・障害回復 | [source](https://doi.org/10.1145/3492321.3519584) |
| 218 | DOI:10.1145/3552326.3567508 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory | [source](https://doi.org/10.1145/3552326.3567508) |
| 219 | DOI:10.1145/3575693.3575754 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3575693.3575754) |
| 220 | DOI:10.1145/3591300 |  |  | 2 | GPUカーネル融合／SwiGLU／LLM推論ランタイム, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://doi.org/10.1145/3591300) |
| 221 | DOI:10.1145/3620665.3640410 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620665.3640410) |
| 222 | DOI:10.1145/3627703.3629578 |  |  | 2 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, serving-scheduling | [source](https://doi.org/10.1145/3627703.3629578) |
| 223 | DOI:10.1145/3650200.3656636 |  |  | 2 | GPU collective communication / communication compression / LLM serving disaggregation, 分散推論／集団通信圧縮／量子化AllReduce／XLA・TPU | [source](https://doi.org/10.1145/3650200.3656636) |
| 224 | DOI:10.1145/3676641.3716252 |  |  | 2 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3676641.3716252) |
| 225 | DOI:10.1145/3710848.3710869 |  |  | 2 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 226 | DOI:10.1145/3731569.3764829 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3731569.3764829) |
| 227 | DOI:10.1145/3779212.3790188 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790188) |
| 228 | DOI:10.1162/neco.1994.6.2.181 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://doi.org/10.1162/neco.1994.6.2.181) |
| 229 | DOI:10.1609/aaai.v38i16.29720 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1609/aaai.v38i16.29720) |
| 230 | DOI:10.18653/v1/2022.emnlp-main.823 |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/2022.emnlp-main.823) |
| 231 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 232 | DOI:10.18653/v1/2025.acl-long.531 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, Quantization × MoE × Offload | [source](https://doi.org/10.18653/v1/2025.acl-long.531) |
| 233 | DOI:10.48550/arxiv.2410.13056 |  |  | 2 | 16-weight-quantization-compression, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.48550/arxiv.2410.13056) |
| 234 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 235 | DOI:10.52202/079017-0381 |  |  | 2 | early-exit-offloading-self-speculative-decoding, speculative-decoding | [source](https://doi.org/10.52202/079017-0381) |
| 236 | DOI:10.52202/085713-1380 |  |  | 2 | 99-other-inference-systems, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/085713-1380) |
| 237 | OpenReview:0LXotew9Du |  |  | 2 | KV Cache Optimization / Compression, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=0LXotew9Du) |
| 238 | OpenReview:c5BOcHM6J8 |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=c5BOcHM6J8) |
| 239 | OpenReview:EKJhH5D5wA |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=EKJhH5D5wA) |
| 240 | OpenReview:H-VlwsYvVi |  |  | 2 | Speculative Decoding, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=H-VlwsYvVi) |
| 241 | OpenReview:ho7ZUS1z8A |  |  | 2 | MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / atomic expert pruning / second-order pruning | [source](https://openreview.net/forum?id=ho7ZUS1z8A) |
| 242 | OpenReview:KeHes2SVxs |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://openreview.net/forum?id=KeHes2SVxs) |
| 243 | OpenReview:qCaq3jGb0S |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=qCaq3jGb0S) |
| 244 | OpenReview:rAcgDBdKnP |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, Quantization × MoE × Offload | [source](https://openreview.net/forum?id=rAcgDBdKnP) |
| 245 | OpenReview:Uh17FiwF4q |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising | [source](https://openreview.net/forum?id=Uh17FiwF4q) |
| 246 | OpenReview:yeeIGM3N6w |  |  | 2 | MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency | [source](https://openreview.net/forum?id=yeeIGM3N6w) |
| 247 | arXiv:1703.09844 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1703.09844) |
| 248 | arXiv:1908.09355 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1908.09355) |
| 249 | arXiv:2110.12894 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 250 | arXiv:2211.15533 |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2211.15533) |
| 251 | arXiv:2402.05406 |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2402.05406) |
| 252 | arXiv:2408.00264 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2408.00264) |
| 253 | arXiv:2412.19821 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2412.19821) |
| 254 | arXiv:2509.18085 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding | [source](https://arxiv.org/abs/2509.18085) |
| 255 | arXiv:2512.18674 |  |  | 2 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.18674) |
| 256 | DOI:10.1109/hpca61900.2025.00086 |  |  | 2 | low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1109/hpca61900.2025.00086) |
| 257 | DOI:10.1109/isocc53507.2021.9613933 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.1109/isocc53507.2021.9613933) |
| 258 | DOI:10.18653/v1/2023.emnlp-main.391 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.391) |
| 259 | DOI:10.18653/v1/2024.findings-acl.195 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.195) |
| 260 | DOI:10.18653/v1/2025.emnlp-main.844 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2025.emnlp-main.844) |
| 261 | OpenReview:44PwmgOpAt |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=44PwmgOpAt) |
| 262 | OpenReview:bTHFrqhASY |  |  | 2 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=bTHFrqhASY) |
| 263 | OpenReview:qrMo6R7lOS |  |  | 2 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=qrMo6R7lOS) |
| 264 | OpenReview:tDRYrAkOB7 |  |  | 2 | KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference | [source](https://openreview.net/forum?id=tDRYrAkOB7) |
| 265 | OpenReview:v3w2a7EInO |  |  | 2 | Conditional Computation | [source](https://openreview.net/forum?id=v3w2a7EInO) |
| 266 | arXiv:2310.03533 |  |  | 2 |  | [source](https://arxiv.org/abs/2310.03533) |
| 267 | DOI:10.18653/v1/2021.findings-acl.449 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2021.findings-acl.449) |
| 268 | DOI:10.18653/v1/p19-1580 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/p19-1580) |
| 269 | DOI:10.48550/arxiv.2411.05787 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.05787) |
| 270 | OpenReview:78Nn4QJTEN |  |  | 2 |  | [source](https://openreview.net/forum?id=78Nn4QJTEN) |
| 271 | OpenReview:OS5dqxmmtl |  |  | 2 |  | [source](https://openreview.net/forum?id=OS5dqxmmtl) |
| 272 | arXiv:1202.3974 |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 273 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 274 | arXiv:1212.0402 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 275 | arXiv:1312.6211 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 276 | arXiv:1409.3215 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1409.3215) |
| 277 | arXiv:1504.00325 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1504.00325) |
| 278 | arXiv:1506.02640 |  |  | 1 | on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1506.02640) |
| 279 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 280 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 281 | arXiv:1601.06759 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1601.06759) |
| 282 | arXiv:1602.02410 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1602.02410) |
| 283 | arXiv:1603.05027 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 284 | arXiv:1603.07396 |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 285 | arXiv:1606.06160 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 286 | arXiv:1610.02136 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1610.02136) |
| 287 | arXiv:1611.01576 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1611.01576) |
| 288 | arXiv:1611.07409 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1611.07409) |
| 289 | arXiv:1701.05517 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1701.05517) |
| 290 | arXiv:1703.04247 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1703.04247) |
| 291 | arXiv:1704.02147 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1704.02147) |
| 292 | arXiv:1704.05021 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1704.05021) |
| 293 | arXiv:1705.06419 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1705.06419) |
| 294 | arXiv:1705.09786 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1705.09786) |
| 295 | arXiv:1707.00110 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1707.00110) |
| 296 | arXiv:1708.00055 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1708.00055) |
| 297 | arXiv:1708.08197 |  |  | 1 | KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://arxiv.org/abs/1708.08197) |
| 298 | arXiv:1710.01878 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/1710.01878) |
| 299 | arXiv:1711.00123 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1711.00123) |
| 300 | arXiv:1711.04291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1711.04291) |
| 301 | arXiv:1712.01208 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/1712.01208) |
| 302 | arXiv:1712.07040 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1712.07040) |
| 303 | arXiv:1802.04730 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/1802.04730) |
| 304 | arXiv:1802.06509 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1802.06509) |
| 305 | arXiv:1804.06028 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/1804.06028) |
| 306 | arXiv:1806.00187 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.00187) |
| 307 | arXiv:1807.09810 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1807.09810) |
| 308 | arXiv:1808.04444 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1808.04444) |
| 309 | arXiv:1808.10583 |  |  | 1 | multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/1808.10583) |
| 310 | arXiv:1809.11096 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1809.11096) |
| 311 | arXiv:1810.03292 |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1810.03292) |
| 312 | arXiv:1810.09868 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1810.09868) |
| 313 | arXiv:1811.05233 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 314 | arXiv:1812.06162 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1812.06162) |
| 315 | arXiv:1902.00751 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.00751) |
| 316 | arXiv:1902.08295 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1902.08295) |
| 317 | arXiv:1903.00089 |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1903.00089) |
| 318 | arXiv:1903.04611 |  |  | 1 | 01-offload-hierarchical-memory | [source](https://arxiv.org/abs/1903.04611) |
| 319 | arXiv:1904.09675 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 320 | arXiv:1905.07129 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1905.07129) |
| 321 | arXiv:1906.04341 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 322 | arXiv:1906.10771 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1906.10771) |
| 323 | arXiv:1907.02684 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1907.02684) |
| 324 | arXiv:1908.09378 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1908.09378) |
| 325 | arXiv:1908.11645 |  |  | 1 | LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計 | [source](https://arxiv.org/abs/1908.11645) |
| 326 | arXiv:1909.09577 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1909.09577) |
| 327 | arXiv:1909.13271 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1909.13271) |
| 328 | arXiv:1910.05316 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/1910.05316) |
| 329 | arXiv:1910.09700 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1910.09700) |
| 330 | arXiv:1911.03014 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/1911.03014) |
| 331 | arXiv:1911.08731 |  |  | 1 | moe-quantization-compression | [source](https://arxiv.org/abs/1911.08731) |
| 332 | arXiv:1912.12180 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1912.12180) |
| 333 | arXiv:2001.04246 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2001.04246) |
| 334 | arXiv:2002.09919 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.09919) |
| 335 | arXiv:2002.10957 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.10957) |
| 336 | arXiv:2003.06713 |  |  | 1 | agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement | [source](https://arxiv.org/abs/2003.06713) |
| 337 | arXiv:2003.10555 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2003.10555) |
| 338 | arXiv:2004.07320 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2004.07320) |
| 339 | arXiv:2004.10964 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2004.10964) |
| 340 | arXiv:2005.00628 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00628) |
| 341 | arXiv:2005.03454 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.03454) |
| 342 | arXiv:2006.00996 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2006.00996) |
| 343 | arXiv:2006.10518 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 344 | arXiv:2006.11527 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2006.11527) |
| 345 | arXiv:2007.03152 |  |  | 1 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://arxiv.org/abs/2007.03152) |
| 346 | arXiv:2007.12626 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2007.12626) |
| 347 | arXiv:2008.05221 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2008.05221) |
| 348 | arXiv:2009.07253 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2009.07253) |
| 349 | arXiv:2009.08553 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2009.08553) |
| 350 | arXiv:2010.02394 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2010.02394) |
| 351 | arXiv:2010.03093 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.03093) |
| 352 | arXiv:2010.03768 |  |  | 1 | augmented LLM serving / KV cache management / predictive scheduling / vLLM | [source](https://arxiv.org/abs/2010.03768) |
| 353 | arXiv:2010.11125 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2010.11125) |
| 354 | arXiv:2010.14701 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2010.14701) |
| 355 | arXiv:2011.04006 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2011.04006) |
| 356 | arXiv:2011.13456 |  |  | 1 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2011.13456) |
| 357 | arXiv:2012.12624 |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2012.12624) |
| 358 | arXiv:2012.15828 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2012.15828) |
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
| 372 | arXiv:2107.13686 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2107.13686) |
| 373 | arXiv:2108.08877 |  |  | 1 | 07-kv-キャッシュ-optimization-compression | [source](https://arxiv.org/abs/2108.08877) |
| 374 | arXiv:2109.04404 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2109.04404) |
| 375 | arXiv:2109.09115 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2109.09115) |
| 376 | arXiv:2109.11295 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2109.11295) |
| 377 | arXiv:2110.04366 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.04366) |
| 378 | arXiv:2110.08419 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2110.08419) |
| 379 | arXiv:2110.15191 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2110.15191) |
| 380 | arXiv:2111.00680 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2111.00680) |
| 381 | arXiv:2112.01488 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2112.01488) |
| 382 | arXiv:2112.06598 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2112.06598) |
| 383 | arXiv:2112.08608 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.08608) |
| 384 | arXiv:2112.14397 |  |  | 1 | MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2112.14397) |
| 385 | arXiv:2201.06618 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2201.06618) |
| 386 | arXiv:2202.01279 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.01279) |
| 387 | arXiv:2202.05747 |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2202.05747) |
| 388 | arXiv:2202.08904 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2202.08904) |
| 389 | arXiv:2203.00091 |  |  | 1 | 13-sparse-attention | [source](https://arxiv.org/abs/2203.00091) |
| 390 | arXiv:2203.05482 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.05482) |
| 391 | arXiv:2203.07814 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2203.07814) |
| 392 | arXiv:2203.14680 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2203.14680) |
| 393 | arXiv:2204.03324 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.03324) |
| 394 | arXiv:2204.06683 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2204.06683) |
| 395 | arXiv:2204.09656 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.09656) |
| 396 | arXiv:2205.00445 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.00445) |
| 397 | arXiv:2205.05243 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2205.05243) |
| 398 | arXiv:2205.10569 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10569) |
| 399 | arXiv:2205.12411 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12411) |
| 400 | arXiv:2205.13792 |  |  | 1 | 推論中のKVQ再計算をストレージ読出しへ置換し、階層キャッシュと遅延制約付きスケジューラを組み合わせるLLM推論省エネルギー化。 | [source](https://arxiv.org/abs/2205.13792) |
| 401 | arXiv:2207.00220 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2207.00220) |
| 402 | arXiv:2207.10551 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2207.10551) |
| 403 | arXiv:2208.02813 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2208.02813) |
| 404 | arXiv:2208.08227 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 405 | arXiv:2209.03143 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.03143) |
| 406 | arXiv:2209.11429 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 407 | arXiv:2209.15352 |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2209.15352) |
| 408 | arXiv:2210.03057 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 409 | arXiv:2210.06726 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2210.06726) |
| 410 | arXiv:2210.10340 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2210.10340) |
| 411 | arXiv:2210.14102 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.14102) |
| 412 | arXiv:2210.17223 |  |  | 1 | moe-inference-expert-offloading | [source](https://arxiv.org/abs/2210.17223) |
| 413 | arXiv:2211.01267 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.01267) |
| 414 | arXiv:2211.06033 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 415 | arXiv:2211.09699 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2211.09699) |
| 416 | arXiv:2211.15089 |  |  | 1 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 417 | arXiv:2212.02855 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2212.02855) |
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
| 429 | arXiv:2302.07080 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2302.07080) |
| 430 | arXiv:2302.10025 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2302.10025) |
| 431 | arXiv:2302.11750 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2302.11750) |
| 432 | arXiv:2302.12510 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.12510) |
| 433 | arXiv:2303.00980 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.00980) |
| 434 | arXiv:2303.04129 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.04129) |
| 435 | arXiv:2303.06153 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2303.06153) |
| 436 | arXiv:2303.08117 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2303.08117) |
| 437 | arXiv:2303.11366 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 438 | arXiv:2303.14524 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2303.14524) |
| 439 | arXiv:2303.16634 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2303.16634) |
| 440 | arXiv:2303.17605 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2303.17605) |
| 441 | arXiv:2304.02643 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2304.02643) |
| 442 | arXiv:2304.03271 |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/2304.03271) |
| 443 | arXiv:2304.04556 |  |  | 1 | KV cache compression / KV eviction / probabilistic inference / importance sampling | [source](https://arxiv.org/abs/2304.04556) |
| 444 | arXiv:2304.08243 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2304.08243) |
| 445 | arXiv:2304.09433 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2304.09433) |
| 446 | arXiv:2304.11062 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2304.11062) |
| 447 | arXiv:2304.14979 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2304.14979) |
| 448 | arXiv:2305.01625 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2305.01625) |
| 449 | arXiv:2305.03653 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2305.03653) |
| 450 | arXiv:2305.06942 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2305.06942) |
| 451 | arXiv:2305.07759 |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2305.07759) |
| 452 | arXiv:2305.10250 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 453 | arXiv:2305.11860 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2305.11860) |
| 454 | arXiv:2305.13412 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2305.13412) |
| 455 | arXiv:2305.14387 |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2305.14387) |
| 456 | arXiv:2305.14705 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2305.14705) |
| 457 | arXiv:2305.15066 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2305.15066) |
| 458 | arXiv:2305.16380 |  |  | 1 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化 | [source](https://arxiv.org/abs/2305.16380) |
| 459 | arXiv:2305.17144 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2305.17144) |
| 460 | arXiv:2305.18691 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.18691) |
| 461 | arXiv:2306.02003 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 462 | arXiv:2306.02896 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02896) |
| 463 | arXiv:2306.04933 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 464 | arXiv:2306.06624 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2306.06624) |
| 465 | arXiv:2306.09782 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.09782) |
| 466 | arXiv:2306.14565 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2306.14565) |
| 467 | arXiv:2307.01189 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.01189) |
| 468 | arXiv:2307.04339 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04339) |
| 469 | arXiv:2307.07697 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2307.07697) |
| 470 | arXiv:2307.08352 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.08352) |
| 471 | arXiv:2307.15043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.15043) |
| 472 | arXiv:2308.02019 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2308.02019) |
| 473 | arXiv:2308.07124 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2308.07124) |
| 474 | arXiv:2308.11596 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2308.11596) |
| 475 | arXiv:2309.02784 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2309.02784) |
| 476 | arXiv:2309.13761 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2309.13761) |
| 477 | arXiv:2310.01542 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.01542) |
| 478 | arXiv:2310.03025 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.03025) |
| 479 | arXiv:2310.05015 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.05015) |
| 480 | arXiv:2310.06927 |  |  | 1 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2310.06927) |
| 481 | arXiv:2310.09259 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.09259) |
| 482 | arXiv:2310.12036 |  |  | 1 | 大規模分散学習・整合学習基盤 | [source](https://arxiv.org/abs/2310.12036) |
| 483 | arXiv:2310.15123 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2310.15123) |
| 484 | arXiv:2310.19295 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.19295) |
| 485 | arXiv:2311.01544 |  |  | 1 | 06-moe-quantization-compression | [source](https://arxiv.org/abs/2311.01544) |
| 486 | arXiv:2311.05997 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.05997) |
| 487 | arXiv:2311.08692 |  |  | 1 | speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2311.08692) |
| 488 | arXiv:2311.12785 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2311.12785) |
| 489 | arXiv:2311.14030 |  |  | 1 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復 | [source](https://arxiv.org/abs/2311.14030) |
| 490 | arXiv:2312.03209 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.03209) |
| 491 | arXiv:2312.04455 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2312.04455) |
| 492 | arXiv:2312.08583 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2312.08583) |
| 493 | arXiv:2401.01923 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.01923) |
| 494 | arXiv:2402.02791 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.02791) |
| 495 | arXiv:2402.10685 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2402.10685) |
| 496 | arXiv:2402.16775 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2402.16775) |
| 497 | arXiv:2403.01632 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2403.01632) |
| 498 | arXiv:2403.03218 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2403.03218) |
| 499 | arXiv:2403.03952 |  |  | 1 | 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2403.03952) |
| 500 | arXiv:2403.04951 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/2403.04951) |

## Machine-readable

同じ割当は [worker-worklist-30.json](worker-worklist-30.json) にあります。

