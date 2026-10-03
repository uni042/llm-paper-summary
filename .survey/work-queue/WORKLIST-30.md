# Scheduled worker :30 worklist

Worker: `scheduled-chat-30`  
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
| 98 | research | arXiv:2407.09486 | ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving | [primary](https://arxiv.org/abs/2407.09486) | `papers/inference/99-other-inference-systems/2024-2407.09486-enova-autoscaling-towards-cost-effective-and-stable-serverless-llm-serving.md` |
| 99 | research | arXiv:1911.02972 | Blockwise Self-Attention for Long Document Understanding | [primary](https://arxiv.org/abs/1911.02972) | `papers/inference/99-other-inference-systems/2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md` |
| 100 | research | arXiv:2409.00142 | Dynamic Depth Decoding: Faster Speculative Decoding for LLMs | [primary](https://arxiv.org/abs/2409.00142) | `papers/inference/99-other-inference-systems/2024-2409.00142-dynamic-depth-decoding-faster-speculative-decoding-for-llms.md` |
| 101 | research | arXiv:2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | [primary](https://arxiv.org/abs/2508.18265) | `papers/inference/99-other-inference-systems/2025-2508.18265-internvl3-5-advancing-open-source-multimodal-models-in-versatility-reasoning-and-efficiency.md` |
| 102 | research | arXiv:2601.21473 | arXiv:2601.21473 | [primary](https://arxiv.org/abs/2601.21473) | `papers/inference/99-other-inference-systems/2026-2601.21473-arxiv-2601-21473.md` |
| 103 | research | arXiv:2604.26256 | DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training | [primary](https://arxiv.org/abs/2604.26256) | `papers/inference/99-other-inference-systems/2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-model-training.md` |
| 104 | research | OpenReview:EQgEMAD4kv | CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences | [primary](https://openreview.net/forum?id=EQgEMAD4kv) | `papers/inference/99-other-inference-systems/0000-e6d13afe4c72-cake-cascading-and-adaptive-kv-cache-eviction-with-layer-preferences.md` |
| 105 | research | arXiv:2510.20171 | Collective Communication for 100k+ GPUs | [primary](https://arxiv.org/abs/2510.20171) | `papers/inference/99-other-inference-systems/2025-2510.20171-collective-communication-for-100k-gpus.md` |
| 106 | research | DOI:10.1145/3731569.3764823 | Jenga: Effective Memory Management for Serving LLM with Heterogeneity | [primary](https://doi.org/10.1145/3731569.3764823) | `papers/inference/99-other-inference-systems/0000-c5994a53cb83-jenga-effective-memory-management-for-serving-llm-with-heterogeneity.md` |
| 107 | research | arXiv:2410.06916 | SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration | [primary](https://arxiv.org/abs/2410.06916) | `papers/inference/99-other-inference-systems/2024-2410.06916-swift-on-the-fly-self-speculative-decoding-for-llm-inference-acceleration.md` |
| 108 | research | arXiv:2601.07891 | KVzap: Fast, Adaptive, and Faithful KV Cache Pruning | [primary](https://arxiv.org/abs/2601.07891) | `papers/inference/99-other-inference-systems/2026-2601.07891-kvzap-fast-adaptive-and-faithful-kv-cache-pruning.md` |
| 109 | research | arXiv:2606.26650 | CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs | [primary](https://arxiv.org/abs/2606.26650) | `papers/inference/99-other-inference-systems/2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md` |
| 110 | research | arXiv:2508.02401 | CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation | [primary](https://arxiv.org/abs/2508.02401) | `papers/inference/99-other-inference-systems/2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-before-generation.md` |
| 111 | research | DOI:10.1145/3773772 | Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving | [primary](https://doi.org/10.1145/3773772) | `papers/inference/99-other-inference-systems/0000-aa24341e05f1-mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md` |
| 112 | research | arXiv:2412.19442 | A Survey on Large Language Model Acceleration based on KV Cache Management | [primary](https://arxiv.org/abs/2412.19442) | `papers/inference/99-other-inference-systems/2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-management.md` |
| 113 | research | DOI:10.18653/v1/2023.emnlp-main.298 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | [primary](https://aclanthology.org/2023.emnlp-main.298/) | `papers/inference/99-other-inference-systems/0000-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-checkpoints.md` |
| 114 | research | arXiv:2502.12110 | A-Mem: Agentic Memory for LLM Agents | [primary](https://arxiv.org/abs/2502.12110) | `papers/inference/99-other-inference-systems/2025-2502.12110-a-mem-agentic-memory-for-llm-agents.md` |
| 115 | research | arXiv:2401.00134 | Unicron: Economizing Self-Healing LLM Training at Scale | [primary](https://arxiv.org/abs/2401.00134) | `papers/inference/99-other-inference-systems/2024-2401.00134-unicron-economizing-self-healing-llm-training-at-scale.md` |
| 116 | research | DOI:10.1145/3676641.3716009 | PAPI: Exploiting Dynamic Parallelism in Large Language Model Decoding with a Processing-In-Memory-Enabled Computing System | [primary](https://doi.org/10.1145/3676641.3716009) | `papers/inference/99-other-inference-systems/0000-71a3fb195e7b-papi-exploiting-dynamic-parallelism-in-large-language-model-decoding-with-a-processing-in-memory-enabled-computing-syste.md` |
| 117 | research | arXiv:2411.18424 | FastSwitch: Optimizing Context Switching Efficiency in Fairness-aware Large Language Model Serving | [primary](https://arxiv.org/abs/2411.18424) | `papers/inference/99-other-inference-systems/2024-2411.18424-fastswitch-optimizing-context-switching-efficiency-in-fairness-aware-large-language-model-serving.md` |
| 118 | research | arXiv:2503.18989 | A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models | [primary](https://arxiv.org/abs/2503.18989) | `papers/inference/99-other-inference-systems/2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-large-language-models.md` |
| 119 | research | arXiv:2511.20975 | Aragog: Just-in-Time Model Routing for Scalable Serving of Agentic Workflows | [primary](https://arxiv.org/abs/2511.20975) | `papers/inference/99-other-inference-systems/2025-2511.20975-aragog-just-in-time-model-routing-for-scalable-serving-of-agentic-workflows.md` |
| 120 | research | arXiv:2310.09832 | Merging Experts into One: Improving Computational Efficiency of Mixture of Experts | [primary](https://arxiv.org/abs/2310.09832) | `papers/inference/99-other-inference-systems/2023-2310.09832-merging-experts-into-one-improving-computational-efficiency-of-mixture-of-experts.md` |
| 121 | research | DOI:10.1145/3695053.3730999 | WindServe: Efficient Phase-Disaggregated LLM Serving with Stream-based Dynamic Scheduling | [primary](https://doi.org/10.1145/3695053.3730999) | `papers/inference/99-other-inference-systems/2025-8e0fd88d7ddc-windserve-efficient-phase-disaggregated-llm-serving-with-stream-based-dynamic-scheduling.md` |
| 122 | research | arXiv:2507.11417 | Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations | [primary](https://arxiv.org/abs/2507.11417) | `papers/inference/99-other-inference-systems/2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference-via-simulations.md` |
| 123 | research | arXiv:2504.12397 | Activated LoRA: Fine-tuned LLMs for Intrinsics | [primary](https://arxiv.org/abs/2504.12397) | `papers/inference/99-other-inference-systems/2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md` |
| 124 | research | arXiv:2505.13326 | Thinking Short and Right Over Thinking Long: Serving LLM Reasoning Efficiently and Accurately | [primary](https://arxiv.org/abs/2505.13326) | `papers/inference/99-other-inference-systems/2025-2505.13326-thinking-short-and-right-over-thinking-long-serving-llm-reasoning-efficiently-and-accurately.md` |
| 125 | research | arXiv:2503.07605 | SEAP: Training-free Sparse Expert Activation Pruning Unlock the Brainpower of Large Language Models | [primary](https://arxiv.org/abs/2503.07605) | `papers/inference/99-other-inference-systems/2025-2503.07605-seap-training-free-sparse-expert-activation-pruning-unlock-the-brainpower-of-large-language-models.md` |
| 126 | research | arXiv:2408.05646 | Eigen Attention: Attention in Low-Rank Space for KV Cache Compression | [primary](https://arxiv.org/abs/2408.05646) | `papers/inference/99-other-inference-systems/2024-2408.05646-eigen-attention-attention-in-low-rank-space-for-kv-cache-compression.md` |
| 127 | research | arXiv:2507.11941 | BlockBPE: Parallel BPE Tokenization | [primary](https://arxiv.org/abs/2507.11941) | `papers/inference/99-other-inference-systems/2025-2507.11941-blockbpe-parallel-bpe-tokenization.md` |
| 128 | research | arXiv:2306.08543 | MiniLLM: On-Policy Distillation of Large Language Models | [primary](https://arxiv.org/abs/2306.08543) | `papers/inference/99-other-inference-systems/2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md` |
| 129 | research | arXiv:2404.05892 | Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence | [primary](https://arxiv.org/abs/2404.05892) | `papers/inference/99-other-inference-systems/2024-2404.05892-eagle-and-finch-rwkv-with-matrix-valued-states-and-dynamic-recurrence.md` |
| 130 | research | arXiv:2407.00088 | T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge | [primary](https://arxiv.org/abs/2407.00088) | `papers/inference/99-other-inference-systems/2024-2407.00088-t-mac-cpu-renaissance-via-table-lookup-for-low-bit-llm-deployment-on-edge.md` |
| 131 | research | arXiv:2410.05076 | TidalDecode: Fast and Accurate LLM Decoding with Position Persistent Sparse Attention | [primary](https://arxiv.org/abs/2410.05076) | `papers/inference/99-other-inference-systems/2024-2410.05076-tidaldecode-fast-and-accurate-llm-decoding-with-position-persistent-sparse-attention.md` |
| 132 | research | arXiv:2603.06199 | FlashPrefill: Instantaneous Pattern Discovery and Thresholding for Ultra-Fast Long-Context Prefilling | [primary](https://arxiv.org/abs/2603.06199) | `papers/inference/99-other-inference-systems/2026-2603.06199-flashprefill-instantaneous-pattern-discovery-and-thresholding-for-ultra-fast-long-context-prefilling.md` |
| 133 | research | arXiv:2511.05814 | In-depth Analysis on Caching and Pre-fetching in Mixture of Experts Offloading | [primary](https://arxiv.org/abs/2511.05814) | `papers/inference/99-other-inference-systems/2025-2511.05814-in-depth-analysis-on-caching-and-pre-fetching-in-mixture-of-experts-offloading.md` |
| 134 | research | arXiv:2408.03314 | Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters | [primary](https://arxiv.org/abs/2408.03314) | `papers/inference/99-other-inference-systems/2024-2408.03314-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model-parameters.md` |
| 135 | research | arXiv:2412.21187 | Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs | [primary](https://arxiv.org/abs/2412.21187) | `papers/inference/99-other-inference-systems/2024-2412.21187-do-not-think-that-much-for-2-3-on-the-overthinking-of-o1-like-llms.md` |
| 136 | research | arXiv:2604.16957 | Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon | [primary](https://arxiv.org/abs/2604.16957) | `papers/inference/99-other-inference-systems/2026-2604.16957-open-tq-metal-fused-compressed-domain-attention-for-long-context-llm-inference-on-apple-silicon.md` |
| 137 | research | arXiv:2506.09397 | SLED: A Speculative LLM Decoding Framework for Efficient Edge Serving | [primary](https://arxiv.org/abs/2506.09397) | `papers/inference/99-other-inference-systems/2025-2506.09397-sled-a-speculative-llm-decoding-framework-for-efficient-edge-serving.md` |
| 138 | research | arXiv:2609.22158 | StepKV: Step-Aware KV Cache Compression for LLM Agents | [primary](https://arxiv.org/abs/2609.22158) | `papers/inference/99-other-inference-systems/2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md` |
| 139 | research | arXiv:2310.04836 | Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM | [primary](https://arxiv.org/abs/2310.04836) | `papers/inference/99-other-inference-systems/2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md` |
| 140 | research | arXiv:2609.31415 | Evaluating the accuracy of KV cache reuse techniques | [primary](https://arxiv.org/abs/2609.31415) | `papers/inference/99-other-inference-systems/2026-2609.31415-evaluating-the-accuracy-of-kv-cache-reuse-techniques.md` |
| 141 | research | arXiv:2310.08915 | Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs | [primary](https://arxiv.org/abs/2310.08915) | `papers/inference/99-other-inference-systems/2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md` |
| 142 | research | arXiv:2608.13524 | DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees | [primary](https://arxiv.org/abs/2608.13524) | `papers/inference/99-other-inference-systems/2026-2608.13524-dartree-speculative-diffusion-decoding-with-autoregressive-draft-trees.md` |
| 143 | research | arXiv:2606.03819 | TreeFlash: Parallel AR-Approximation for Faster Speculative Decoding | [primary](https://arxiv.org/abs/2606.03819) | `papers/inference/99-other-inference-systems/2026-2606.03819-treeflash-parallel-ar-approximation-for-faster-speculative-decoding.md` |
| 144 | research | arXiv:2609.33184 | Resource-Efficient Speculative Decoding for Long-Context LLM Serving | [primary](https://arxiv.org/abs/2609.33184) | `papers/inference/99-other-inference-systems/2026-2609.33184-resource-efficient-speculative-decoding-for-long-context-llm-serving.md` |
| 145 | research | arXiv:2504.19720 | Taming the Titans: A Survey of Efficient LLM Inference Serving | [primary](https://arxiv.org/abs/2504.19720) | `papers/inference/99-other-inference-systems/2025-2504.19720-taming-the-titans-a-survey-of-efficient-llm-inference-serving.md` |
| 146 | research | arXiv:2009.14794 | Rethinking Attention with Performers | [primary](https://arxiv.org/abs/2009.14794) | `papers/inference/99-other-inference-systems/2020-2009.14794-rethinking-attention-with-performers.md` |
| 147 | research | arXiv:2310.06694 | Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning | [primary](https://arxiv.org/abs/2310.06694) | `papers/inference/99-other-inference-systems/2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pruning.md` |
| 148 | research | arXiv:2305.11627 | LLM-Pruner: On the Structural Pruning of Large Language Models | [primary](https://arxiv.org/abs/2305.11627) | `papers/inference/99-other-inference-systems/2023-2305.11627-llm-pruner-on-the-structural-pruning-of-large-language-models.md` |
| 149 | research | arXiv:2410.13846 | LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation | [primary](https://arxiv.org/abs/2410.13846) | `papers/inference/99-other-inference-systems/2024-2410.13846-lighttransfer-your-long-context-llm-is-secretly-a-hybrid-model-with-effortless-adaptation.md` |
| 150 | research | arXiv:2509.00579 | KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache | [primary](https://arxiv.org/abs/2509.00579) | `papers/inference/99-other-inference-systems/2025-2509.00579-kvcomp-a-high-performance-llm-aware-lossy-compression-framework-for-kv-cache.md` |
| 151 | research | arXiv:2602.23200 | InnerQ: Hardware-aware Tuning-free Quantization of KV Cache for Large Language Models | [primary](https://arxiv.org/abs/2602.23200) | `papers/inference/99-other-inference-systems/2026-2602.23200-innerq-hardware-aware-tuning-free-quantization-of-kv-cache-for-large-language-models.md` |
| 152 | research | arXiv:2007.14062 | Big Bird: Transformers for Longer Sequences | [primary](https://arxiv.org/abs/2007.14062) | `papers/inference/99-other-inference-systems/2020-2007.14062-big-bird-transformers-for-longer-sequences.md` |
| 153 | research | arXiv:2402.18668 | Simple linear attention language models balance the recall-throughput tradeoff | [primary](https://arxiv.org/abs/2402.18668) | `papers/inference/99-other-inference-systems/2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tradeoff.md` |
| 154 | research | arXiv:2609.13205 | Self-Indexing Attention for Compression-Compatible Sparse Long-Context LLM Inference | [primary](https://arxiv.org/abs/2609.13205) | `papers/inference/99-other-inference-systems/2026-2609.13205-self-indexing-attention-for-compression-compatible-sparse-long-context-llm-inference.md` |
| 155 | research | arXiv:2607.02980 | Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling | [primary](https://arxiv.org/abs/2607.02980) | `papers/inference/99-other-inference-systems/2026-2607.02980-hierarchical-sparse-attention-done-right-toward-infinite-context-modeling.md` |
| 156 | research | arXiv:2603.24517 | AVO: Agentic Variation Operators for Autonomous Evolutionary Search | [primary](https://arxiv.org/abs/2603.24517) | `papers/inference/99-other-inference-systems/2026-2603.24517-avo-agentic-variation-operators-for-autonomous-evolutionary-search.md` |
| 157 | research | arXiv:2403.19887 | Jamba: A Hybrid Transformer-Mamba Language Model | [primary](https://arxiv.org/abs/2403.19887) | `papers/inference/99-other-inference-systems/2024-2403.19887-jamba-a-hybrid-transformer-mamba-language-model.md` |
| 158 | research | arXiv:2510.06126 | lm-Meter: Unveiling Runtime Inference Latency for On-Device Language Models | [primary](https://arxiv.org/abs/2510.06126) | `papers/inference/99-other-inference-systems/2025-2510.06126-lm-meter-unveiling-runtime-inference-latency-for-on-device-language-models.md` |
| 159 | research | DOI:10.1145/3662006.3662067 | Hybrid SLM and LLM for Edge-Cloud Collaborative Inference | [primary](https://doi.org/10.1145/3662006.3662067) | `papers/inference/99-other-inference-systems/2024-7a6bf47fa469-hybrid-slm-and-llm-for-edge-cloud-collaborative-inference.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **5372** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | DOI:10.1145/3694715.3695948 |  |  | 15 | LLM serving / multi-SLO scheduling / admission control / speculative decoding / multi-replica routing, MoE serving / attention-MoE disaggregation / asynchronous inference, Offload / Hierarchical Memory, Prefill/Decode Disaggregation / Selective KV Transfer, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, kernel-runtime-compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3694715.3695948) |
| 2 | DOI:10.18653/v1/d18-1259 |  |  | 12 | 07-kv-cache-optimization-compression, 13-sparse-attention, Adaptive Expert Computation / Compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング, 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://doi.org/10.18653/v1/d18-1259) |
| 3 | arXiv:2406.12793 |  |  | 12 | 07-kv-cache-optimization-compression, Edge / On-device LLM Systems, KV cache compression / sparse attention / long-context inference, KVキャッシュ退避／長文推論／KV選択／KV量子化, llm-serving-scheduling-disaggregation, その他システム研究 | [source](https://arxiv.org/abs/2406.12793) |
| 4 | DOI:10.1016/j.neucom.2023.127063 |  |  | 11 | 02-hardware-accelerators, GPU architecture and tensor-computation orchestration, KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, Sparse Attention, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://doi.org/10.1016/j.neucom.2023.127063) |
| 5 | DOI:10.48550/arxiv.2404.07413 |  |  | 10 | 02-adaptive-expert-computation-compression, Adaptive computation／cache-aware MoE, MoE compression / expert merging / output approximation / least-squares compression, MoE predictive expert placement / replication / SiDA-MoE, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, moe-parallelism-communication, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2404.07413) |
| 6 | OpenReview:VTF8yNQM66 |  |  | 10 | 13-sparse-attention, Agentic Serving Benchmarking, MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, agentic workflow serving / workflow physical planning / adaptive serving, llm-serving-scheduling-disaggregation, other-inference-systems, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=VTF8yNQM66) |
| 7 | arXiv:2405.21060 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化, PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management, kv-cache, kv-cache-offload-recomputation, linear attention / delta-rule associative memory / state-space models / Bayesian filtering, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2405.21060) |
| 8 | arXiv:2309.00071 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Adaptive computation／cache-aware MoE, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, kv-cache-offload-recomputation, moe | [source](https://arxiv.org/abs/2309.00071) |
| 9 | OpenReview:qrwe7XHTmYb |  |  | 9 | Adaptive Expert Computation / Compression, Adaptive computation／cache-aware MoE, LLM Serving / Multi-Model Serving / Memory Disaggregation, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, Speculative decoding × MoE, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=qrwe7XHTmYb) |
| 10 | DOI:10.48550/arxiv.2409.12186 |  |  | 9 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification, 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM, 推論エンジン／推論基盤, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.48550/arxiv.2409.12186) |
| 11 | arXiv:2309.12307 |  |  | 8 | Conditional Computation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference, KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ, cpu-offload, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, multi-tenant LoRA serving / CPU-assisted inference / rank-aware scheduling | [source](https://arxiv.org/abs/2309.12307) |
| 12 | arXiv:2308.00352 |  |  | 8 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, survey-long-context-serving, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://arxiv.org/abs/2308.00352) |
| 13 | OpenReview:Ti67584b98 |  |  | 8 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Other Inference Systems / Lossless Parallel Decoding, Speculative decoding × MoE, kv-cache-optimization-compression, sparse attention / learned context ranking / long-context LLM inference, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://openreview.net/forum?id=Ti67584b98) |
| 14 | arXiv:2401.15947 |  |  | 8 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis, MoE expert pruning / expert clustering / task-specific model compression, Quantization × MoE × Offload, オフロード／階層メモリ, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2401.15947) |
| 15 | DOI:10.18653/v1/2020.emnlp-demos.6 |  |  | 8 | 13-sparse-attention, MoE expert offloading / predictive prefetch and cache management, early-exit-offloading-self-speculative-decoding, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, kv-cache-optimization-compression, other-inference-systems | [source](https://doi.org/10.18653/v1/2020.emnlp-demos.6) |
| 16 | arXiv:2304.04487 |  |  | 8 | LLM inference surveys、roofline performance analysis, Speculative Decoding, survey-speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 投機的デコード / 自己投機的デコード / 層スキップ | [source](https://arxiv.org/abs/2304.04487) |
| 17 | arXiv:1809.09600 |  |  | 8 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 18 | arXiv:2305.16300 |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, KV cache quantization / long-context inference / activation compression, KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.16300) |
| 19 | arXiv:2406.00515 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, LLM inference kernel safety / CUDA symbolic execution / model-aware verification, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, kernel-runtime-compilation, serving-scheduling | [source](https://arxiv.org/abs/2406.00515) |
| 20 | OpenReview:WE_vluYUL-X |  |  | 7 | RAG runtime / distributed orchestration / agentic workflows, agentic serving / KV cache eviction / persistent multi-turn serving, agentic serving workload characterization / KV-cache / inference benchmarking, agentic workflow serving / workflow physical planning / adaptive serving, kv-cache-optimization-compression, エージェント型LLMサービング／プリフィル・デコード分離／異種GPUスケジューリング | [source](https://openreview.net/forum?id=WE_vluYUL-X) |
| 21 | arXiv:2408.03326 |  |  | 7 | kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, low-bit VLM inference / microscaling / hardware-software co-design, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2408.03326) |
| 22 | OpenReview:chfJJYC3iL |  |  | 7 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, Other Inference Systems / Lossless Parallel Decoding, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=chfJJYC3iL) |
| 23 | DOI:10.18653/v1/2025.emnlp-main.334 |  |  | 7 | 10-kv-cache-offload-recomputation, KVキャッシュ再利用／KVキャッシュ圧縮／長文脈推論, kv-cache-reuse-position-independent-caching, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://doi.org/10.18653/v1/2025.emnlp-main.334) |
| 24 | arXiv:2509.16941 |  |  | 7 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2509.16941) |
| 25 | arXiv:2402.14034 |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 26 | arXiv:2502.02737 |  |  | 6 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2502.02737) |
| 27 | arXiv:2110.03742 |  |  | 6 | Edge／on-device MoE, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference / expert pruning / language-specific expert specialization, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2110.03742) |
| 28 | arXiv:2405.05465 |  |  | 6 | KV Cache Offload / Recomputation, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, disaggregated LLM serving / request routing / learned scheduling, kv-cache-memory-management, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2405.05465) |
| 29 | arXiv:1704.04683 |  |  | 6 | MoE inference systems / expert parallelism / model compression / knowledge distillation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, early-exit-offloading-self-speculative-decoding, moe-parallelism-communication | [source](https://arxiv.org/abs/1704.04683) |
| 30 | arXiv:2408.11743 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, Adaptive computation／cache-aware MoE, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2408.11743) |
| 31 | arXiv:2509.17765 |  |  | 6 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 32 | OpenReview:Bkg6RiCqY7 |  |  | 6 | Expert Prefetch, KVキャッシュ・注意アーキテクチャ, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, その他システム研究 | [source](https://openreview.net/forum?id=Bkg6RiCqY7) |
| 33 | arXiv:2311.04939 |  |  | 6 | KVキャッシュ退避／長文推論／KV選択／KV量子化, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2311.04939) |
| 34 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 35 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 36 | arXiv:2304.09145 |  |  | 5 | KV cache quantization / long-context inference / activation compression, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, kv-cache-memory, survey-low-bit-llm, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2304.09145) |
| 37 | arXiv:2603.01175 |  |  | 5 | 10-kv-cache-offload-recomputation, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, flash-capacity-tier-inference, hardware-accelerators, offload-hierarchical-memory | [source](https://arxiv.org/abs/2603.01175) |
| 38 | DOI:10.1145/3695053.3731008 |  |  | 5 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 39 | arXiv:1811.02883 |  |  | 5 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM inference simulation / disaggregated serving / performance modeling, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://arxiv.org/abs/1811.02883) |
| 40 | arXiv:2212.10560 |  |  | 5 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2212.10560) |
| 41 | DOI:10.18653/v1/d17-1082 |  |  | 5 | Adaptive computation／cache-aware MoE, Conditional Computation, MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, sparse attention / learned context ranking / long-context LLM inference | [source](https://doi.org/10.18653/v1/d17-1082) |
| 42 | OpenReview:tyEyYT267x |  |  | 5 | Other Inference Systems / Lossless Parallel Decoding, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion LLM inference / adaptive feature caching / KV cache / parallel denoising, speculative-decoding | [source](https://openreview.net/forum?id=tyEyYT267x) |
| 43 | arXiv:2401.03868 |  |  | 5 | LLM inference surveys、roofline performance analysis, hierarchical-memory, kv-cache-memory | [source](https://arxiv.org/abs/2401.03868) |
| 44 | arXiv:2504.07491 |  |  | 5 | 11-llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2504.07491) |
| 45 | DOI:10.18653/v1/2024.findings-emnlp.612 |  |  | 5 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性 | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.612) |
| 46 | OpenReview:uccHPGDlao |  |  | 5 | 05-speculative-decoding-moe, Speculative decoding × MoE, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 47 | DOI:10.18653/v1/n19-1246 |  |  | 5 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.18653/v1/n19-1246) |
| 48 | arXiv:1805.06085 |  |  | 4 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, cpu-ssd-offload, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1805.06085) |
| 49 | arXiv:2210.11416 |  |  | 4 | Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 50 | arXiv:2402.14905 |  |  | 4 | 10-kv-cache-offload-recomputation, kv-cache-optimization-compression, offload-hierarchical-memory, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2402.14905) |
| 51 | DOI:10.1145/3503222.3507778 |  |  | 4 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, kernel-runtime-compilation, llm-serving-scheduling-disaggregation, テンソル並列推論／通信計算重畳／集合通信融合／配信カーネル | [source](https://doi.org/10.1145/3503222.3507778) |
| 52 | DOI:10.18653/v1/2025.acl-long.1126 |  |  | 4 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics, dynamic-pd-disaggregation, kv-cache-offload-recomputation | [source](https://doi.org/10.18653/v1/2025.acl-long.1126) |
| 53 | DOI:10.5281/zenodo.5371628 |  |  | 4 | KV Cache Optimization / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.5281/zenodo.5371628) |
| 54 | OpenReview:stXtBqyTWX |  |  | 4 | Speculative decoding × MoE, activation-aware expert placement and multi-node MoE inference, kernel-runtime-compilation, moe-inference-expert-offloading | [source](https://openreview.net/forum?id=stXtBqyTWX) |
| 55 | arXiv:1811.00937 |  |  | 4 | Adaptive Expert Computation / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1811.00937) |
| 56 | OpenReview:BAakY1hNKS |  |  | 4 | 14-agentic-inference-serving-runtime, llm-serving-scheduling-disaggregation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=BAakY1hNKS) |
| 57 | OpenReview:zAdUB0aCTQ |  |  | 4 | agentic serving workload characterization / KV-cache / inference benchmarking, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://openreview.net/forum?id=zAdUB0aCTQ) |
| 58 | arXiv:2603.05451 |  |  | 4 | diffusion LLM inference / KV caching / fused attention / parallel decoding, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2603.05451) |
| 59 | OpenReview:ziezViPoN1 |  |  | 4 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=ziezViPoN1) |
| 60 | arXiv:2410.17891 |  |  | 3 | Speculative Decoding, diffusion language model inference / KV cache / training-free acceleration, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2410.17891) |
| 61 | arXiv:2511.00739 |  |  | 3 | LLM Serving / Scheduling / Disaggregation, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference, agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2511.00739) |
| 62 | DOI:10.1007/s11432-024-4235-6 |  |  | 3 | MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / null experts / data sparsity / multimodal MoE, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1007/s11432-024-4235-6) |
| 63 | DOI:10.1109/lca.2023.3333759 |  |  | 3 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, low-bit VLM inference / microscaling / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/lca.2023.3333759) |
| 64 | DOI:10.1109/micro56248.2022.00051 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, kv-cache-memory | [source](https://doi.org/10.1109/micro56248.2022.00051) |
| 65 | DOI:10.1109/tmc.2024.3513457 |  |  | 3 | 05-speculative-decoding-moe, Edge / On-device LLM Systems, hardware-accelerators | [source](https://doi.org/10.1109/tmc.2024.3513457) |
| 66 | DOI:10.1145/3489517.3530428 |  |  | 3 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3489517.3530428) |
| 67 | DOI:10.1145/3676641.3716011 |  |  | 3 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, MoE serving / attention-MoE disaggregation / asynchronous inference, serving-scheduling | [source](https://doi.org/10.1145/3676641.3716011) |
| 68 | DOI:10.1145/3731569.3764808 |  |  | 3 | edge-on-device-llm-systems, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764808) |
| 69 | DOI:10.1162/tacl_a_00023 |  |  | 3 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1162/tacl_a_00023) |
| 70 | DOI:10.52202/079017-1601 |  |  | 3 | agent-runtime-sandbox-state-management, agentic GPU kernel generation / harness engineering / profile-guided optimization, agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://doi.org/10.52202/079017-1601) |
| 71 | OpenReview:5Qe7AGO3Eq |  |  | 3 | 17-pim-near-data-acceleration, kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=5Qe7AGO3Eq) |
| 72 | OpenReview:hmOwOZWzYE |  |  | 3 | KV Cache Optimization / Compression, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=hmOwOZWzYE) |
| 73 | OpenReview:tO3ASKZlok |  |  | 3 | 07-kv-cache-optimization-compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=tO3ASKZlok) |
| 74 | OpenReview:YicbFdNTTy |  |  | 3 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation, オフロード／階層メモリ | [source](https://openreview.net/forum?id=YicbFdNTTy) |
| 75 | arXiv:2311.05232 |  |  | 3 | LLM inference surveys、roofline performance analysis, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2311.05232) |
| 76 | arXiv:2602.10604 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2602.10604) |
| 77 | DOI:10.1109/hcs59251.2023.10254711 |  |  | 3 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, offload-hierarchical-memory | [source](https://doi.org/10.1109/hcs59251.2023.10254711) |
| 78 | DOI:10.1145/3577193.3593704 |  |  | 3 | KV Cache Optimization / Compression, その他システム研究 | [source](https://doi.org/10.1145/3577193.3593704) |
| 79 | DOI:10.1145/3695053.3731051 |  |  | 3 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design | [source](https://doi.org/10.1145/3695053.3731051) |
| 80 | DOI:10.1162/tacl%5fa%5f00266 |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.1162/tacl%5fa%5f00266) |
| 81 | DOI:10.18653/v1/2023.emnlp-main.825 |  |  | 3 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.825) |
| 82 | DOI:10.18653/v1/w17-4413 |  |  | 3 | Adaptive computation／cache-aware MoE, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/w17-4413) |
| 83 | OpenReview:2jwAjomEDB |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=2jwAjomEDB) |
| 84 | OpenReview:jxpsAj7ltE |  |  | 3 | Adaptive Expert Computation / Compression, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=jxpsAj7ltE) |
| 85 | OpenReview:pPjZIOuQuF |  |  | 3 | 10-kv-キャッシュ-オフロード-recomputation, 13-sparse-attention | [source](https://openreview.net/forum?id=pPjZIOuQuF) |
| 86 | OpenReview:uBaFH7aQnC |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=uBaFH7aQnC) |
| 87 | DOI:10.1145/3714983.3714987 |  |  | 3 | KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成 | [source](https://doi.org/10.1145/3714983.3714987) |
| 88 | OpenReview:dHng2O0Jjr |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving | [source](https://openreview.net/forum?id=dHng2O0Jjr) |
| 89 | arXiv:1311.2540 |  |  | 2 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 90 | arXiv:1906.04284 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/1906.04284) |
| 91 | arXiv:2203.06390 |  |  | 2 | Weight Quantization / Compression, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.06390) |
| 92 | arXiv:2306.00317 |  |  | 2 | Quantization × MoE × Offload, hardware-accelerators | [source](https://arxiv.org/abs/2306.00317) |
| 93 | arXiv:2306.02707 |  |  | 2 | llm-serving-scheduling-disaggregation, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2306.02707) |
| 94 | arXiv:2307.01952 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2307.01952) |
| 95 | arXiv:2307.09782 |  |  | 2 | LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.09782) |
| 96 | arXiv:2308.09723 |  |  | 2 | Quantization × MoE × Offload, kv-cache-memory | [source](https://arxiv.org/abs/2308.09723) |
| 97 | arXiv:2309.05516 |  |  | 2 | Expert Prefetch, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 98 | arXiv:2309.10400 |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 99 | arXiv:2309.13879 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, other-inference-systems | [source](https://arxiv.org/abs/2309.13879) |
| 100 | arXiv:2310.00746 |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 101 | arXiv:2310.03744 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 102 | arXiv:2310.15141 |  |  | 2 | LLM inference surveys、roofline performance analysis, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 103 | arXiv:2311.08981 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, survey-speculative-decoding | [source](https://arxiv.org/abs/2311.08981) |
| 104 | arXiv:2311.11501 |  |  | 2 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2311.11501) |
| 105 | arXiv:2311.17541 |  |  | 2 | agentic serving / workflow-aware scheduling / memory-aware dispatch, other-inference-systems | [source](https://arxiv.org/abs/2311.17541) |
| 106 | arXiv:2312.04511 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2312.04511) |
| 107 | arXiv:2312.11918 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11918) |
| 108 | arXiv:2312.16862 |  |  | 2 | LLM inference surveys、roofline performance analysis, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2312.16862) |
| 109 | arXiv:2401.06080 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.06080) |
| 110 | arXiv:2401.13601 |  |  | 2 | LLM inference surveys、roofline performance analysis, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2401.13601) |
| 111 | arXiv:2402.00025 |  |  | 2 | GPU疎行列カーネル／二重疎LLM推論／SIMTマイクロアーキテクチャ, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.00025) |
| 112 | arXiv:2402.03216 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 113 | arXiv:2402.09353 |  |  | 2 | Conditional Computation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.09353) |
| 114 | arXiv:2402.13116 |  |  | 2 | Speculative Decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.13116) |
| 115 | arXiv:2402.14808 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, inference/11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14808) |
| 116 | arXiv:2402.19427 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/2402.19427) |
| 117 | arXiv:2403.06764 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2403.06764) |
| 118 | arXiv:2403.09347 |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 119 | arXiv:2404.05567 |  |  | 2 | MoE expert pruning / expert merging / redundancy-aware compression / global budget allocation, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2404.05567) |
| 120 | arXiv:2404.09336 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2404.09336) |
| 121 | arXiv:2404.14897 |  |  | 2 | speculative-decoding, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2404.14897) |
| 122 | arXiv:2405.16587 |  |  | 2 | Conditional Computation, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2405.16587) |
| 123 | arXiv:2406.00059 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation | [source](https://arxiv.org/abs/2406.00059) |
| 124 | arXiv:2406.03853 |  |  | 2 | adaptive-expert-computation-compression, speculative-decoding | [source](https://arxiv.org/abs/2406.03853) |
| 125 | arXiv:2406.07394 |  |  | 2 | Edge／on-device MoE, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.07394) |
| 126 | arXiv:2406.11931 |  |  | 2 | MoE compression / structured pruning / atomic expert pruning / second-order pruning, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.11931) |
| 127 | arXiv:2406.18485 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18485) |
| 128 | arXiv:2406.20094 |  |  | 2 | adaptive-expert-computation-compression, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2406.20094) |
| 129 | arXiv:2407.07000 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2407.07000) |
| 130 | arXiv:2407.09816 |  |  | 2 | adaptive expert computation / dynamic MoE routing / expert sparsification, offload-hierarchical-memory | [source](https://arxiv.org/abs/2407.09816) |
| 131 | arXiv:2407.11511 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2407.11511) |
| 132 | arXiv:2408.04323 |  |  | 2 | Agentic inference and serving runtime, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2408.04323) |
| 133 | arXiv:2409.01990 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2409.01990) |
| 134 | arXiv:2409.17066 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline | [source](https://arxiv.org/abs/2409.17066) |
| 135 | arXiv:2409.18486 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, prefill-decode disaggregation / attention offloading / LLM serving | [source](https://arxiv.org/abs/2409.18486) |
| 136 | arXiv:2410.02660 |  |  | 2 | kv-cache-optimization-compression, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2410.02660) |
| 137 | arXiv:2410.07985 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.07985) |
| 138 | arXiv:2410.13212 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.13212) |
| 139 | arXiv:2410.17196 |  |  | 2 | llm-serving-scheduling-disaggregation, その他の推論システム | [source](https://arxiv.org/abs/2410.17196) |
| 140 | arXiv:2410.23079 |  |  | 2 | KVキャッシュオフロード／階層メモリ, System-aware KV cache | [source](https://arxiv.org/abs/2410.23079) |
| 141 | arXiv:2411.01738 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2411.01738) |
| 142 | arXiv:2411.04905 |  |  | 2 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2411.04905) |
| 143 | arXiv:2411.05239 |  |  | 2 | distributed LLM inference / communication-aware serving, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2411.05239) |
| 144 | arXiv:2411.15242 |  |  | 2 | PIM / Near-Data Acceleration, hybrid Mamba-Transformer inference memory management | [source](https://arxiv.org/abs/2411.15242) |
| 145 | arXiv:2412.06769 |  |  | 2 | 99-other-inference-systems, Conditional Computation | [source](https://arxiv.org/abs/2412.06769) |
| 146 | arXiv:2412.13171 |  |  | 2 | Conditional Computation, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2412.13171) |
| 147 | arXiv:2501.09959 |  |  | 2 | 07-kv-キャッシュ-optimization-compression, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2501.09959) |
| 148 | arXiv:2501.19309 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, 投機的デコード／メモリ制約推論／分散・バッチ投機実行 | [source](https://arxiv.org/abs/2501.19309) |
| 149 | arXiv:2502.04677 |  |  | 2 | KVキャッシュ管理 / エージェント型LLM配信 / 接頭辞優先スケジューリング / 予測型追い出し, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2502.04677) |
| 150 | arXiv:2502.09696 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://arxiv.org/abs/2502.09696) |
| 151 | arXiv:2502.15304 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2502.15304) |
| 152 | arXiv:2502.17419 |  |  | 2 | Conditional Computation, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2502.17419) |
| 153 | arXiv:2503.07572 |  |  | 2 | 14-agentic-inference-serving-runtime, Conditional Computation | [source](https://arxiv.org/abs/2503.07572) |
| 154 | arXiv:2503.13444 |  |  | 2 | kv-cache-offload-recomputation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2503.13444) |
| 155 | arXiv:2503.24047 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, LLMサービング・スケジューリング・KVキャッシュ保持 | [source](https://arxiv.org/abs/2503.24047) |
| 156 | arXiv:2504.05299 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論, foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2504.05299) |
| 157 | arXiv:2504.09936 |  |  | 2 | KV Cache Optimization / Compression, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2504.09936) |
| 158 | arXiv:2504.13914 |  |  | 2 | 推論ベンチマーク・推論大規模言語モデルのサービング評価, 適応的専門家計算 / MoE routing / expert diversity / parameter-free optimization | [source](https://arxiv.org/abs/2504.13914) |
| 159 | arXiv:2504.16397 |  |  | 2 | agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2504.16397) |
| 160 | arXiv:2504.18154 |  |  | 2 | prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS, オフロード／階層メモリ | [source](https://arxiv.org/abs/2504.18154) |
| 161 | arXiv:2505.06252 |  |  | 2 | kv-cache-offload-recomputation, その他システム研究 | [source](https://arxiv.org/abs/2505.06252) |
| 162 | arXiv:2505.11916 |  |  | 2 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, dynamic-pd-disaggregation | [source](https://arxiv.org/abs/2505.11916) |
| 163 | arXiv:2505.20353 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, moe | [source](https://arxiv.org/abs/2505.20353) |
| 164 | arXiv:2506.01844 |  |  | 2 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2506.01844) |
| 165 | arXiv:2506.15564 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://arxiv.org/abs/2506.15564) |
| 166 | arXiv:2507.09942 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2507.09942) |
| 167 | arXiv:2507.16731 |  |  | 2 | 05-speculative-decoding-moe, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2507.16731) |
| 168 | arXiv:2508.01002 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2508.01002) |
| 169 | arXiv:2508.07227 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2508.07227) |
| 170 | arXiv:2508.10395 |  |  | 2 | 17-pim-near-data-acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2508.10395) |
| 171 | arXiv:2508.17196 |  |  | 2 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.17196) |
| 172 | arXiv:2509.02718 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2509.02718) |
| 173 | arXiv:2509.23678 |  |  | 2 | adaptive expert computation / compression; end-side sparse MoE, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2509.23678) |
| 174 | arXiv:2510.01290 |  |  | 2 | inference/07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2510.01290) |
| 175 | arXiv:2510.06513 |  |  | 2 | offload-hierarchical-memory, オフロード／階層メモリ | [source](https://arxiv.org/abs/2510.06513) |
| 176 | arXiv:2510.15330 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2510.15330) |
| 177 | arXiv:2510.25741 |  |  | 2 | adaptive-expert-computation-compression, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://arxiv.org/abs/2510.25741) |
| 178 | arXiv:2511.16682 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論, 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2511.16682) |
| 179 | arXiv:2511.23404 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2511.23404) |
| 180 | arXiv:2512.05916 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.05916) |
| 181 | arXiv:2512.14142 |  |  | 2 | LLMサービング／スケジューリング／分離, other | [source](https://arxiv.org/abs/2512.14142) |
| 182 | arXiv:2512.20848 |  |  | 2 | PIM / Near-Data Acceleration, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2512.20848) |
| 183 | arXiv:2601.07526 |  |  | 2 | 14-agentic-inference-serving-runtime, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2601.07526) |
| 184 | arXiv:2601.11589 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, disaggregated LLM serving / request routing / learned scheduling | [source](https://arxiv.org/abs/2601.11589) |
| 185 | arXiv:2601.22379 |  |  | 2 | 07-kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2601.22379) |
| 186 | arXiv:2602.21224 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2602.21224) |
| 187 | arXiv:2603.28101 |  |  | 2 | LLM inference simulation / disaggregated serving / performance modeling, agentic LLM serving / pipeline parallelism / serving scheduling / speculative decoding | [source](https://arxiv.org/abs/2603.28101) |
| 188 | arXiv:2605.20315 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2605.20315) |
| 189 | arXiv:2606.22874 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2606.22874) |
| 190 | DOI:10.1109/cgo51591.2021.9370308 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, kernel-runtime-compilation | [source](https://doi.org/10.1109/cgo51591.2021.9370308) |
| 191 | DOI:10.1109/dac63849.2025.11133274 |  |  | 2 | Offload / Hierarchical Memory, hierarchical-memory-kv-offload-cpu-gpu-attention | [source](https://doi.org/10.1109/dac63849.2025.11133274) |
| 192 | DOI:10.1109/hcs61935.2024.10664793 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hcs61935.2024.10664793) |
| 193 | DOI:10.1109/hpca56546.2023.10071120 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://doi.org/10.1109/hpca56546.2023.10071120) |
| 194 | DOI:10.1109/ieeestd.2019.8766229 |  |  | 2 | moe-parallelism-communication, survey-low-bit-llm | [source](https://doi.org/10.1109/ieeestd.2019.8766229) |
| 195 | DOI:10.1109/isca52012.2021.00049 |  |  | 2 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/isca52012.2021.00049) |
| 196 | DOI:10.1109/isscc49663.2026.11409285 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, hardware-accelerators | [source](https://doi.org/10.1109/isscc49663.2026.11409285) |
| 197 | DOI:10.1109/lca.2025.3597323 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1109/lca.2025.3597323) |
| 198 | DOI:10.1109/mm.2023.3256384 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2023.3256384) |
| 199 | DOI:10.1109/mm.2025.3592688 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, moe-parallelism-communication | [source](https://doi.org/10.1109/mm.2025.3592688) |
| 200 | DOI:10.1109/tmc.2025.3546466 |  |  | 2 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Offload / Hierarchical Memory | [source](https://doi.org/10.1109/tmc.2025.3546466) |
| 201 | DOI:10.1126/science.abq1158 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1126/science.abq1158) |
| 202 | DOI:10.1145/224056.224064 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/224056.224064) |
| 203 | DOI:10.1145/2934664 |  |  | 2 | 14-agentic-inference-serving-runtime, RAG runtime / distributed orchestration / agentic workflows | [source](https://doi.org/10.1145/2934664) |
| 204 | DOI:10.1145/3352460.3358302 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3352460.3358302) |
| 205 | DOI:10.1145/3453483.3454083 |  |  | 2 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 206 | DOI:10.1145/3503222.3507738 |  |  | 2 | long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.1145/3503222.3507738) |
| 207 | DOI:10.1145/3572848.3577479 |  |  | 2 | 02-hardware-accelerators, kernel-runtime-compilation | [source](https://doi.org/10.1145/3572848.3577479) |
| 208 | DOI:10.1145/3575693.3576933 |  |  | 2 | kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3575693.3576933) |
| 209 | DOI:10.1145/3600006.3613139 |  |  | 2 | CPUオフロード / 活性化疎性 / 階層メモリ, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling | [source](https://doi.org/10.1145/3600006.3613139) |
| 210 | DOI:10.1145/3620666.3651369 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620666.3651369) |
| 211 | DOI:10.1145/3636534.3649379 |  |  | 2 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3636534.3649379) |
| 212 | DOI:10.1145/3669940.3707231 |  |  | 2 | llm-serving-scheduling-disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://doi.org/10.1145/3669940.3707231) |
| 213 | DOI:10.1145/3689031.3717481 |  |  | 2 | 13-sparse-attention, 低ビット疎推論／GPUカーネル／エッジ推論 | [source](https://doi.org/10.1145/3689031.3717481) |
| 214 | DOI:10.1145/3725843.3756041 |  |  | 2 | GPU architecture and tensor-computation orchestration, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://doi.org/10.1145/3725843.3756041) |
| 215 | DOI:10.1145/3767742 |  |  | 2 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル, prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://doi.org/10.1145/3767742) |
| 216 | DOI:10.1145/3779212.3790236 |  |  | 2 | inference/11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790236) |
| 217 | DOI:10.1177/1094342005051521 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, hardware-accelerators | [source](https://doi.org/10.1177/1094342005051521) |
| 218 | DOI:10.1609/aaai.v40i36.40255 |  |  | 2 | speculative decoding / context compression / agentic LLM inference, 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.1609/aaai.v40i36.40255) |
| 219 | DOI:10.18653/v1/2023.acl-long.689 |  |  | 2 | Speculative Decoding, survey-speculative-decoding | [source](https://doi.org/10.18653/v1/2023.acl-long.689) |
| 220 | DOI:10.18653/v1/2024.findings-acl.57 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.57) |
| 221 | DOI:10.18653/v1/d18-1206 |  |  | 2 | Adaptive computation／cache-aware MoE, 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/d18-1206) |
| 222 | DOI:10.48550/arxiv.2507.11851 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, speculative-decoding | [source](https://doi.org/10.48550/arxiv.2507.11851) |
| 223 | DOI:10.52202/075280-0943 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/075280-0943) |
| 224 | DOI:10.52202/079017-0381 |  |  | 2 | early-exit-offloading-self-speculative-decoding, speculative-decoding | [source](https://doi.org/10.52202/079017-0381) |
| 225 | DOI:10.52202/085713-1380 |  |  | 2 | 99-other-inference-systems, 投機復号・自己投機・ループ型Transformer・推論パイプライン | [source](https://doi.org/10.52202/085713-1380) |
| 226 | OpenReview:8Wuvhh0LYW |  |  | 2 | 17-pim-near-data-acceleration, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=8Wuvhh0LYW) |
| 227 | OpenReview:cJd1BgZ9CS |  |  | 2 | speculative-decoding, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://openreview.net/forum?id=cJd1BgZ9CS) |
| 228 | OpenReview:FAeU7516MR |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, Speculative decoding × MoE | [source](https://openreview.net/forum?id=FAeU7516MR) |
| 229 | OpenReview:H4DqfPSibmx |  |  | 2 | Speculative decoding × MoE, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=H4DqfPSibmx) |
| 230 | OpenReview:JFygzwx8SJ |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=JFygzwx8SJ) |
| 231 | OpenReview:mtSSFiqW6y |  |  | 2 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=mtSSFiqW6y) |
| 232 | OpenReview:R0SoZvqXyQ |  |  | 2 | llm-serving-scheduling-disaggregation, serving-scheduling | [source](https://openreview.net/forum?id=R0SoZvqXyQ) |
| 233 | OpenReview:rsY6J3ZaTF |  |  | 2 | speculative decoding / draft-model design, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=rsY6J3ZaTF) |
| 234 | OpenReview:vXxardq6db |  |  | 2 | Quantization × MoE × Offload, 投機的デコード／MoE | [source](https://openreview.net/forum?id=vXxardq6db) |
| 235 | OpenReview:YolJOZOGhI |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://openreview.net/forum?id=YolJOZOGhI) |
| 236 | arXiv:2408.05636 |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2408.05636) |
| 237 | DOI:10.1109/isca66397.2026.00021 |  |  | 2 | MoE expert offloading / predictive prefetch and cache management | [source](https://doi.org/10.1109/isca66397.2026.00021) |
| 238 | DOI:10.18653/v1/2023.emnlp-main.391 |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.391) |
| 239 | DOI:10.18653/v1/2024.findings-acl.195 |  |  | 2 | KV Cache Optimization / Compression | [source](https://doi.org/10.18653/v1/2024.findings-acl.195) |
| 240 | DOI:10.18653/v1/2025.emnlp-main.844 |  |  | 2 | 05-speculative-decoding-moe | [source](https://doi.org/10.18653/v1/2025.emnlp-main.844) |
| 241 | OpenReview:44PwmgOpAt |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=44PwmgOpAt) |
| 242 | OpenReview:bTHFrqhASY |  |  | 2 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=bTHFrqhASY) |
| 243 | OpenReview:qrMo6R7lOS |  |  | 2 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=qrMo6R7lOS) |
| 244 | OpenReview:tDRYrAkOB7 |  |  | 2 | KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference | [source](https://openreview.net/forum?id=tDRYrAkOB7) |
| 245 | DOI:10.18653/v1/2021.sustainlp-1.5 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2021.sustainlp-1.5) |
| 246 | DOI:10.48550/arxiv.2411.02886 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.02886) |
| 247 | OpenReview:4D0f16Vwc3 |  |  | 2 |  | [source](https://openreview.net/forum?id=4D0f16Vwc3) |
| 248 | OpenReview:i1uGbfHHpH |  |  | 2 |  | [source](https://openreview.net/forum?id=i1uGbfHHpH) |
| 249 | OpenReview:tkiZQlL04w |  |  | 2 |  | [source](https://openreview.net/forum?id=tkiZQlL04w) |
| 250 | arXiv:1205.6711 |  |  | 1 | kv-cache | [source](https://arxiv.org/abs/1205.6711) |
| 251 | arXiv:1212.0402 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1212.0402) |
| 252 | arXiv:1307.2118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1307.2118) |
| 253 | arXiv:1402.3511 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1402.3511) |
| 254 | arXiv:1410.0759 |  |  | 1 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン | [source](https://arxiv.org/abs/1410.0759) |
| 255 | arXiv:1505.05571 |  |  | 1 | MoE数値再現性・決定論的推論・実行時互換性 | [source](https://arxiv.org/abs/1505.05571) |
| 256 | arXiv:1506.03099 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1506.03099) |
| 257 | arXiv:1511.05641 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1511.05641) |
| 258 | arXiv:1512.03385 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1512.03385) |
| 259 | arXiv:1602.02068 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/1602.02068) |
| 260 | arXiv:1602.07360 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1602.07360) |
| 261 | arXiv:1603.05691 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1603.05691) |
| 262 | arXiv:1606.02891 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.02891) |
| 263 | arXiv:1609.09548 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1609.09548) |
| 264 | arXiv:1611.01576 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1611.01576) |
| 265 | arXiv:1611.07409 |  |  | 1 | llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1611.07409) |
| 266 | arXiv:1701.05517 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1701.05517) |
| 267 | arXiv:1703.05160 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1703.05160) |
| 268 | arXiv:1704.02147 |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1704.02147) |
| 269 | arXiv:1704.05021 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1704.05021) |
| 270 | arXiv:1705.06419 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1705.06419) |
| 271 | arXiv:1705.09786 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1705.09786) |
| 272 | arXiv:1707.00110 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1707.00110) |
| 273 | arXiv:1708.00055 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1708.00055) |
| 274 | arXiv:1708.08197 |  |  | 1 | KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://arxiv.org/abs/1708.08197) |
| 275 | arXiv:1710.01878 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/1710.01878) |
| 276 | arXiv:1711.02782 |  |  | 1 | 02-hardware-accelerators | [source](https://arxiv.org/abs/1711.02782) |
| 277 | arXiv:1711.05073 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/1711.05073) |
| 278 | arXiv:1712.01887 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1712.01887) |
| 279 | arXiv:1712.09763 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.09763) |
| 280 | arXiv:1802.05365 |  |  | 1 | Training Offload / Memory Systems | [source](https://arxiv.org/abs/1802.05365) |
| 281 | arXiv:1802.06901 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/1802.06901) |
| 282 | arXiv:1804.06028 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/1804.06028) |
| 283 | arXiv:1806.00187 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.00187) |
| 284 | arXiv:1807.09810 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1807.09810) |
| 285 | arXiv:1808.04444 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1808.04444) |
| 286 | arXiv:1808.10583 |  |  | 1 | multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/1808.10583) |
| 287 | arXiv:1809.08887 |  |  | 1 | 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/1809.08887) |
| 288 | arXiv:1810.03264 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.03264) |
| 289 | arXiv:1810.09305 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1810.09305) |
| 290 | arXiv:1811.03115 |  |  | 1 | 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/1811.03115) |
| 291 | arXiv:1812.01608 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1812.01608) |
| 292 | arXiv:1902.00732 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1902.00732) |
| 293 | arXiv:1902.05613 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.05613) |
| 294 | arXiv:1902.09574 |  |  | 1 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 295 | arXiv:1903.01611 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1903.01611) |
| 296 | arXiv:1903.05662 |  |  | 1 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference | [source](https://arxiv.org/abs/1903.05662) |
| 297 | arXiv:1904.09324 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/1904.09324) |
| 298 | arXiv:1905.00537 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1905.00537) |
| 299 | arXiv:1906.01502 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1906.01502) |
| 300 | arXiv:1906.05714 |  |  | 1 | 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/1906.05714) |
| 301 | arXiv:1906.11024 |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/1906.11024) |
| 302 | arXiv:1907.12009 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1907.12009) |
| 303 | arXiv:1908.10084 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1908.10084) |
| 304 | arXiv:1909.03368 |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1909.03368) |
| 305 | arXiv:1909.09577 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1909.09577) |
| 306 | arXiv:1909.13271 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1909.13271) |
| 307 | arXiv:1910.06188 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1910.06188) |
| 308 | arXiv:1910.09700 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1910.09700) |
| 309 | arXiv:1911.04610 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1911.04610) |
| 310 | arXiv:1911.08772 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1911.08772) |
| 311 | arXiv:2001.01072 |  |  | 1 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/2001.01072) |
| 312 | arXiv:2002.09919 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.09919) |
| 313 | arXiv:2002.11985 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.11985) |
| 314 | arXiv:2003.12462 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2003.12462) |
| 315 | arXiv:2004.07320 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2004.07320) |
| 316 | arXiv:2004.10964 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2004.10964) |
| 317 | arXiv:2004.14769 |  |  | 1 | MoE expert pruning / trajectory-aware compression / task-specific MoE compression | [source](https://arxiv.org/abs/2004.14769) |
| 318 | arXiv:2005.00928 |  |  | 1 | 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御 | [source](https://arxiv.org/abs/2005.00928) |
| 319 | arXiv:2005.08025 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2005.08025) |
| 320 | arXiv:2006.06762 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2006.06762) |
| 321 | arXiv:2006.11527 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2006.11527) |
| 322 | arXiv:2007.03152 |  |  | 1 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://arxiv.org/abs/2007.03152) |
| 323 | arXiv:2007.12626 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2007.12626) |
| 324 | arXiv:2008.05221 |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2008.05221) |
| 325 | arXiv:2009.07253 |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2009.07253) |
| 326 | arXiv:2009.08553 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2009.08553) |
| 327 | arXiv:2009.14167 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2009.14167) |
| 328 | arXiv:2010.02523 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2010.02523) |
| 329 | arXiv:2010.03768 |  |  | 1 | augmented LLM serving / KV cache management / predictive scheduling / vLLM | [source](https://arxiv.org/abs/2010.03768) |
| 330 | arXiv:2010.11125 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2010.11125) |
| 331 | arXiv:2010.16248 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2010.16248) |
| 332 | arXiv:2011.04393 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2011.04393) |
| 333 | arXiv:2012.07463 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2012.07463) |
| 334 | arXiv:2012.15613 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2012.15613) |
| 335 | arXiv:2012.15833 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2012.15833) |
| 336 | arXiv:2102.01672 |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2102.01672) |
| 337 | arXiv:2102.07835 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2102.07835) |
| 338 | arXiv:2102.08942 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2102.08942) |
| 339 | arXiv:2103.02143 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2103.02143) |
| 340 | arXiv:2103.07191 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2103.07191) |
| 341 | arXiv:2104.12470 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2104.12470) |
| 342 | arXiv:2105.05944 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2105.05944) |
| 343 | arXiv:2105.13878 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2105.13878) |
| 344 | arXiv:2106.03594 |  |  | 1 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2106.03594) |
| 345 | arXiv:2106.04972 |  |  | 1 | multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2106.04972) |
| 346 | arXiv:2106.08254 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.08254) |
| 347 | arXiv:2107.02561 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2107.02561) |
| 348 | arXiv:2107.11906 |  |  | 1 | long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2107.11906) |
| 349 | arXiv:2108.08877 |  |  | 1 | 07-kv-キャッシュ-optimization-compression | [source](https://arxiv.org/abs/2108.08877) |
| 350 | arXiv:2109.04404 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2109.04404) |
| 351 | arXiv:2109.09115 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2109.09115) |
| 352 | arXiv:2109.11295 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2109.11295) |
| 353 | arXiv:2110.04366 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2110.04366) |
| 354 | arXiv:2110.08419 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2110.08419) |
| 355 | arXiv:2110.15191 |  |  | 1 | distributed attention / sequence parallelism / blockwise attention / long-context transformers | [source](https://arxiv.org/abs/2110.15191) |
| 356 | arXiv:2111.00680 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2111.00680) |
| 357 | arXiv:2112.01488 |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2112.01488) |
| 358 | arXiv:2112.06598 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2112.06598) |
| 359 | arXiv:2112.10769 |  |  | 1 | kv-cache-memory | [source](https://arxiv.org/abs/2112.10769) |
| 360 | arXiv:2201.06618 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2201.06618) |
| 361 | arXiv:2202.05239 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2202.05239) |
| 362 | arXiv:2202.07848 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2202.07848) |
| 363 | arXiv:2202.10447 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2202.10447) |
| 364 | arXiv:2203.00386 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2203.00386) |
| 365 | arXiv:2203.05740 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2203.05740) |
| 366 | arXiv:2203.09509 |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.09509) |
| 367 | arXiv:2204.01691 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2204.01691) |
| 368 | arXiv:2204.06125 |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2204.06125) |
| 369 | arXiv:2204.07705 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2204.07705) |
| 370 | arXiv:2205.00445 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.00445) |
| 371 | arXiv:2205.06126 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2205.06126) |
| 372 | arXiv:2205.11380 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2205.11380) |
| 373 | arXiv:2205.12701 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12701) |
| 374 | arXiv:2206.01859 |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2206.01859) |
| 375 | arXiv:2207.00220 |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2207.00220) |
| 376 | arXiv:2207.09238 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2207.09238) |
| 377 | arXiv:2208.02025 |  |  | 1 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム | [source](https://arxiv.org/abs/2208.02025) |
| 378 | arXiv:2208.05592 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2208.05592) |
| 379 | arXiv:2208.11174 |  |  | 1 | 復号注意・共有接頭辞・鍵値キャッシュ・GPUカーネル・vLLM | [source](https://arxiv.org/abs/2208.11174) |
| 380 | arXiv:2209.10505 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.10505) |
| 381 | arXiv:2209.14756 |  |  | 1 | KV-cache memory management / random-access-constrained accelerators | [source](https://arxiv.org/abs/2209.14756) |
| 382 | arXiv:2210.03044 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2210.03044) |
| 383 | arXiv:2210.05144 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2210.05144) |
| 384 | arXiv:2210.07535 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.07535) |
| 385 | arXiv:2210.10340 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2210.10340) |
| 386 | arXiv:2210.14102 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.14102) |
| 387 | arXiv:2211.00107 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.00107) |
| 388 | arXiv:2211.05953 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2211.05953) |
| 389 | arXiv:2211.08403 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2211.08403) |
| 390 | arXiv:2211.11586 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2211.11586) |
| 391 | arXiv:2211.16750 |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2211.16750) |
| 392 | arXiv:2212.04037 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2212.04037) |
| 393 | arXiv:2212.05191 |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2212.05191) |
| 394 | arXiv:2212.08136 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.08136) |
| 395 | arXiv:2212.10445 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2212.10445) |
| 396 | arXiv:2212.10650 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2212.10650) |
| 397 | arXiv:2301.02111 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.02111) |
| 398 | arXiv:2301.05843 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2301.05843) |
| 399 | arXiv:2301.08721 |  |  | 1 | kv-cache-memory | [source](https://arxiv.org/abs/2301.08721) |
| 400 | arXiv:2301.11235 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2301.11235) |
| 401 | arXiv:2301.13823 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2301.13823) |
| 402 | arXiv:2302.04062 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2302.04062) |
| 403 | arXiv:2302.07080 |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2302.07080) |
| 404 | arXiv:2302.10025 |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2302.10025) |
| 405 | arXiv:2302.12066 |  |  | 1 | foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2302.12066) |
| 406 | arXiv:2302.13214 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2302.13214) |
| 407 | arXiv:2303.02141 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2303.02141) |
| 408 | arXiv:2303.05510 |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2303.05510) |
| 409 | arXiv:2303.06296 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2303.06296) |
| 410 | arXiv:2303.10130 |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2303.10130) |
| 411 | arXiv:2303.11381 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11381) |
| 412 | arXiv:2303.15375 |  |  | 1 | cpu-offload | [source](https://arxiv.org/abs/2303.15375) |
| 413 | arXiv:2304.01468 |  |  | 1 | SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2304.01468) |
| 414 | arXiv:2304.03094 |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2304.03094) |
| 415 | arXiv:2304.03589 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2304.03589) |
| 416 | arXiv:2304.05128 |  |  | 1 | 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2304.05128) |
| 417 | arXiv:2304.08244 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2304.08244) |
| 418 | arXiv:2304.09433 |  |  | 1 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2304.09433) |
| 419 | arXiv:2304.11062 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2304.11062) |
| 420 | arXiv:2304.14979 |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2304.14979) |
| 421 | arXiv:2305.01625 |  |  | 1 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2305.01625) |
| 422 | arXiv:2305.03653 |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2305.03653) |
| 423 | arXiv:2305.06942 |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2305.06942) |
| 424 | arXiv:2305.08367 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2305.08367) |
| 425 | arXiv:2305.10435 |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2305.10435) |
| 426 | arXiv:2305.13304 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.13304) |
| 427 | arXiv:2305.14152 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.14152) |
| 428 | arXiv:2305.14481 |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2305.14481) |
| 429 | arXiv:2305.14806 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2305.14806) |
| 430 | arXiv:2305.15294 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2305.15294) |
| 431 | arXiv:2305.16635 |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2305.16635) |
| 432 | arXiv:2305.18354 |  |  | 1 | 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2305.18354) |
| 433 | arXiv:2305.19466 |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2305.19466) |
| 434 | arXiv:2306.02295 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02295) |
| 435 | arXiv:2306.04757 |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2306.04757) |
| 436 | arXiv:2306.05443 |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/2306.05443) |
| 437 | arXiv:2306.09539 |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2306.09539) |
| 438 | arXiv:2306.13596 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 439 | arXiv:2306.16837 |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.16837) |
| 440 | arXiv:2307.04251 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04251) |
| 441 | arXiv:2307.06281 |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2307.06281) |
| 442 | arXiv:2307.08191 |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2307.08191) |
| 443 | arXiv:2307.12966 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12966) |
| 444 | arXiv:2308.02019 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2308.02019) |
| 445 | arXiv:2308.07124 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2308.07124) |
| 446 | arXiv:2308.12043 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2308.12043) |
| 447 | arXiv:2309.07418 |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2309.07418) |
| 448 | arXiv:2309.16739 |  |  | 1 | multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2309.16739) |
| 449 | arXiv:2310.02277 |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2310.02277) |
| 450 | arXiv:2310.05015 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.05015) |
| 451 | arXiv:2310.06927 |  |  | 1 | MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2310.06927) |
| 452 | arXiv:2310.09259 |  |  | 1 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.09259) |
| 453 | arXiv:2310.12036 |  |  | 1 | 大規模分散学習・整合学習基盤 | [source](https://arxiv.org/abs/2310.12036) |
| 454 | arXiv:2310.15123 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2310.15123) |
| 455 | arXiv:2310.19233 |  |  | 1 | 10-kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.19233) |
| 456 | arXiv:2311.00176 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.00176) |
| 457 | arXiv:2311.02262 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2311.02262) |
| 458 | arXiv:2311.03301 |  |  | 1 | MoE expert pruning / trajectory-aware compression / task-specific MoE compression | [source](https://arxiv.org/abs/2311.03301) |
| 459 | arXiv:2311.08105 |  |  | 1 | distributed LLM inference / communication-aware serving | [source](https://arxiv.org/abs/2311.08105) |
| 460 | arXiv:2311.10372 |  |  | 1 | LLM inference kernel safety / CUDA symbolic execution / model-aware verification | [source](https://arxiv.org/abs/2311.10372) |
| 461 | arXiv:2311.11829 |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2311.11829) |
| 462 | arXiv:2311.13541 |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2311.13541) |
| 463 | arXiv:2312.00784 |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2312.00784) |
| 464 | arXiv:2312.03113 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2312.03113) |
| 465 | arXiv:2312.03732 |  |  | 1 | MoE-LoRA / パラメータ効率的微調整 / マージ可能アダプタ / ルータ不要自己ルーティング | [source](https://arxiv.org/abs/2312.03732) |
| 466 | arXiv:2312.05181 |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2312.05181) |
| 467 | arXiv:2312.06677 |  |  | 1 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2312.06677) |
| 468 | arXiv:2312.08935 |  |  | 1 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2312.08935) |
| 469 | arXiv:2312.12379 |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2312.12379) |
| 470 | arXiv:2312.13211 |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2312.13211) |
| 471 | arXiv:2312.16733 |  |  | 1 | CPUオフロード / 活性化疎性 / 階層メモリ | [source](https://arxiv.org/abs/2312.16733) |
| 472 | arXiv:2401.01312 |  |  | 1 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2401.01312) |
| 473 | arXiv:2401.02731 |  |  | 1 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2401.02731) |
| 474 | arXiv:2401.04883 |  |  | 1 | diffusion-llm-inference / caching / low-precision | [source](https://arxiv.org/abs/2401.04883) |
| 475 | arXiv:2401.06761 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2401.06761) |
| 476 | arXiv:2401.07159 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2401.07159) |
| 477 | arXiv:2401.08138 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2401.08138) |
| 478 | arXiv:2401.08383 |  |  | 1 | activation-aware expert placement and multi-node MoE inference | [source](https://arxiv.org/abs/2401.08383) |
| 479 | arXiv:2401.10225 |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2401.10225) |
| 480 | arXiv:2401.11202 |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.11202) |
| 481 | arXiv:2401.12503 |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2401.12503) |
| 482 | arXiv:2401.14490 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2401.14490) |
| 483 | arXiv:2402.00159 |  |  | 1 | Adaptive computation／cache-aware MoE | [source](https://arxiv.org/abs/2402.00159) |
| 484 | arXiv:2402.02643 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2402.02643) |
| 485 | arXiv:2402.03694 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2402.03694) |
| 486 | arXiv:2402.04636 |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2402.04636) |
| 487 | arXiv:2402.05119 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.05119) |
| 488 | arXiv:2402.06967 |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.06967) |
| 489 | arXiv:2402.07939 |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2402.07939) |
| 490 | arXiv:2402.10076 |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2402.10076) |
| 491 | arXiv:2402.10685 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2402.10685) |
| 492 | arXiv:2402.11960 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.11960) |
| 493 | arXiv:2402.12345 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.12345) |
| 494 | arXiv:2402.13499 |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2402.13499) |
| 495 | arXiv:2402.14160 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14160) |
| 496 | arXiv:2402.16775 |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2402.16775) |
| 497 | arXiv:2402.17463 |  |  | 1 | moe | [source](https://arxiv.org/abs/2402.17463) |
| 498 | arXiv:2402.17985 |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2402.17985) |
| 499 | arXiv:2403.00001 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2403.00001) |
| 500 | arXiv:2403.00801 |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2403.00801) |

## Machine-readable

同じ割当は [worker-worklist-30.json](worker-worklist-30.json) にあります。

