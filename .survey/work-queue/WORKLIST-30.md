# Scheduled worker :30 worklist

Worker: `scheduled-chat-30`  
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
| 143 | research | arXiv:2310.06927 | Sparse Fine-tuning for Inference Acceleration of Large Language Models | [primary](https://arxiv.org/abs/2310.06927) | `papers/inference/99-other-inference-systems/2023-2310.06927-sparse-fine-tuning-for-inference-acceleration-of-large-language-models.md` |
| 144 | research | arXiv:2303.08302 | ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation | [primary](https://arxiv.org/abs/2303.08302) | `papers/inference/99-other-inference-systems/2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehensive-study-to-low-rank-compensation.md` |
| 145 | research | DOI:10.1145/3620666.3651329 | Characterizing Power Management Opportunities for LLMs in the Cloud | [primary](https://doi.org/10.1145/3620666.3651329) | `papers/inference/99-other-inference-systems/2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md` |
| 146 | research | arXiv:2404.07904 | HGRN2: Gated Linear RNNs with State Expansion | [primary](https://arxiv.org/abs/2404.07904) | `papers/inference/99-other-inference-systems/2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md` |
| 147 | research | arXiv:2403.15388 | LLaVA-Prumerge: Adaptive Token Reduction for Efficient Large Multimodal Models | [primary](https://arxiv.org/abs/2403.15388) | `papers/inference/99-other-inference-systems/2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-models.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **6901** / このworker向け: **500**

| # | identity | title | year | 関連数 | 系統候補 | source |
|---:|---|---|---:|---:|---|---|
| 1 | arXiv:2304.01089 |  |  | 19 | Conditional Computation, Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, Weight Quantization / Compression, inference-systems, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 2 | arXiv:1910.01108 |  |  | 17 | LLM Serving / Scheduling / Disaggregation, LLMサービング／予測型スケジューリング, Speculative Decoding, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 投機的デコード / 分布保存型デコード高速化, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1910.01108) |
| 3 | arXiv:2312.04985 |  |  | 16 | KV cache compression / sparse attention / long-context inference, KV cache quantization / long-context inference / activation compression, Offload / Hierarchical Memory, Sparse Attention, inference-systems, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, sparse attention / KV-cache bandwidth reduction, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2312.04985) |
| 4 | arXiv:2407.12820 |  |  | 15 | 07-kv-cache-optimization-compression, KV Cache Offload / Recomputation, KVキャッシュ最適化・CPU退避・疎注意・ページ化KV管理, inference-systems, kv-cache-offload-recomputation, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://arxiv.org/abs/2407.12820) |
| 5 | arXiv:1912.01703 |  |  | 14 | 05-speculative-decoding-moe, 13-sparse-attention, GPU Kernel Framework, GPUカーネル融合／SwiGLU／LLM推論ランタイム, Offload / Hierarchical Memory, inference-systems, その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/1912.01703) |
| 6 | DOI:10.1016/j.neucom.2023.127063 |  |  | 14 | 02-hardware-accelerators, GPU architecture and tensor-computation orchestration, KV-cache reuse / personalized memory serving / retrieval-augmented serving / GPU-native retrieval, KVキャッシュ低ランク圧縮／適応ランク選択／KV量子化／注意カーネル高速化, KVキャッシュ最適化／圧縮, Sparse Attention, llm-serving-scheduling-disaggregation, other-inference-systems | [source](https://doi.org/10.1016/j.neucom.2023.127063) |
| 7 | arXiv:1808.08745 |  |  | 13 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 8 | OpenReview:tcbBPnfwxS |  |  | 13 | Adaptive Expert Computation / Compression, LLM Serving / Scheduling, MoE compression / structured pruning / atomic expert pruning / second-order pruning, Speculative Decoding, inference-systems, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=tcbBPnfwxS) |
| 9 | arXiv:2501.12599 |  |  | 12 | 11-llm-serving-scheduling-disaggregation, Conditional Computation, LLM Serving / Reasoning, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, inference-systems, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, serving-scheduling, 推論ベンチマーク・推論大規模言語モデルのサービング評価, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2501.12599) |
| 10 | arXiv:2410.21276 |  |  | 12 | 07-kv-cache-optimization-compression, Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, agentic inference / persistent memory, fine-grained MoE / expert routing / test-time scaling / inference-time sampling, kv-cache-optimization-compression, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation, multi-tenant LLM serving / latency attribution / fractional GPU sharing, その他システム研究 | [source](https://arxiv.org/abs/2410.21276) |
| 11 | arXiv:2506.12708 |  |  | 12 | 12-moe-parallelism-communication, KVキャッシュ圧縮・分離サービング・ネットワーク転送・投機的生成, MoE serving / attention-MoE disaggregation / asynchronous inference, chunked-prefill scheduling / fairness / latency control, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2506.12708) |
| 12 | arXiv:2308.00352 |  |  | 11 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, survey-long-context-serving, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://arxiv.org/abs/2308.00352) |
| 13 | DOI:10.48550/arxiv.2404.07413 |  |  | 11 | 02-adaptive-expert-computation-compression, Adaptive computation／cache-aware MoE, MoE compression / expert merging / output approximation / least-squares compression, MoE predictive expert placement / replication / SiDA-MoE, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, Quantization × MoE × Offload, moe-parallelism-communication, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2404.07413) |
| 14 | DOI:10.1609/aaai.v34i05.6239 |  |  | 11 | Adaptive computation／cache-aware MoE, KV cache management benchmarking, MoE compression / training-free expert merging / multimodal MoE routing, adaptive-expert-computation-compression, early-exit-offloading-self-speculative-decoding, inference-systems | [source](https://doi.org/10.1609/aaai.v34i05.6239) |
| 15 | DOI:10.18653/v1/2024.acl-long.623 |  |  | 10 | 02-hardware-accelerators, 14-agentic-inference-serving-runtime, KV Cache Offload / Recomputation, LLMサービング・接頭辞キャッシュ・マルチテナント隔離, Offload / Hierarchical Memory, fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, inference-systems, llm-serving-scheduling-disaggregation, 要求間KVキャッシュ再利用・穴埋め推論・コード補完・継続事前学習 | [source](https://doi.org/10.18653/v1/2024.acl-long.623) |
| 16 | arXiv:1911.11641 |  |  | 10 | 16-weight-quantization-compression, Conditional Computation, adaptive-expert-computation-compression, kv-cache-memory, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, moe-quantization-compression | [source](https://arxiv.org/abs/1911.11641) |
| 17 | DOI:10.1145/3394486.3406703 |  |  | 10 | GPU collective communication / communication compression / LLM serving disaggregation, KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems, kernel-runtime-compilation, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3394486.3406703) |
| 18 | DOI:10.48550/arxiv.2402.08268 |  |  | 10 | 10-kv-キャッシュ-オフロード-recomputation, serving-scheduling | [source](https://doi.org/10.48550/arxiv.2402.08268) |
| 19 | arXiv:2503.20215 |  |  | 9 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, Sparse Attention / VLM Inference, Speculative Decoding, batch inference / event-driven runtime / MoE serving / offload, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2503.20215) |
| 20 | DOI:10.64434/tml.20250910 |  |  | 9 | Agentic Serving Benchmarking, Inference Kernel / Determinism, LLM Serving / Scheduling / Disaggregation, LLMサービング／スケジューリング／分離, speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://doi.org/10.64434/tml.20250910) |
| 21 | arXiv:2210.11416 |  |  | 9 | 99-other-inference-systems, Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, inference-systems, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 22 | arXiv:2405.14366 |  |  | 9 | KV Cache Offload / Retrieval / Compression, KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, inference-systems, kv-cache-offload-recomputation, other-inference-systems | [source](https://arxiv.org/abs/2405.14366) |
| 23 | DOI:10.5281/zenodo.5371628 |  |  | 9 | KV Cache Optimization / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Weight Quantization / Compression, inference-systems, kv-cache-optimization-compression, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://doi.org/10.5281/zenodo.5371628) |
| 24 | arXiv:2311.13581 |  |  | 9 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, 投機的復号 / EAGLE | [source](https://arxiv.org/abs/2311.13581) |
| 25 | DOI:10.1145/3676641.3716278 |  |  | 8 | 08-edge-on-device-llm-systems, 14-agentic-inference-serving-runtime, LLM Serving / Scheduling / Disaggregation, LLMサービング・スケジューリング・分離実行, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, inference-systems, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://doi.org/10.1145/3676641.3716278) |
| 26 | arXiv:2511.21631 |  |  | 8 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, MoE compression / training-free expert merging / multimodal MoE routing, adaptive expert computation / dynamic MoE routing / gating uncertainty, flash-capacity-tier-inference, inference-systems | [source](https://arxiv.org/abs/2511.21631) |
| 27 | arXiv:2209.11895 |  |  | 8 | KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Long-context serving / KV cache benchmark, 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/2209.11895) |
| 28 | OpenReview:chfJJYC3iL |  |  | 8 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, MoE圧縮 / 専門家統合 / 専門家枝刈り / REAP後継, Other Inference Systems / Lossless Parallel Decoding, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=chfJJYC3iL) |
| 29 | arXiv:2401.00625 |  |  | 7 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, System-aware KV cache, distributed LLM inference / communication-aware serving, llm-serving-systems, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.00625) |
| 30 | arXiv:1805.06085 |  |  | 7 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, cpu-ssd-offload, inference-systems, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1805.06085) |
| 31 | arXiv:2509.17765 |  |  | 7 | 11-llm-serving-scheduling-disaggregation, LLM Serving / Scheduling / Disaggregation, inference-systems, llm-serving-scheduling-disaggregation, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2509.17765) |
| 32 | arXiv:2309.05463 |  |  | 7 | Weight Quantization / Compression, inference-systems, survey-edge-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.05463) |
| 33 | DOI:10.1162/tacl_a_00023 |  |  | 7 | 10-kv-キャッシュ-オフロード-recomputation, KV cache compression / training-free eviction / attention sink / FlashAttention-compatible inference, inference-systems, 疎注意 / KVキャッシュ選択 / 長文脈推論 | [source](https://doi.org/10.1162/tacl_a_00023) |
| 34 | OpenReview:uccHPGDlao |  |  | 7 | 05-speculative-decoding-moe, Speculative decoding × MoE, inference-systems, survey-speculative-decoding | [source](https://openreview.net/forum?id=uccHPGDlao) |
| 35 | arXiv:2504.09285 |  |  | 7 | LLM serving / prefill-decode disaggregation, llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.09285) |
| 36 | DOI:10.1162/tacl_a_00276 |  |  | 7 | Speculative Decoding / Parallel Inference Systems, inference-systems, survey-speculative-decoding | [source](https://doi.org/10.1162/tacl_a_00276) |
| 37 | arXiv:2402.14034 |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 38 | DOI:10.1145/3695053.3731008 |  |  | 6 | 17-pim-near-data-acceleration, MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, PIM / Near-Data Acceleration, attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3695053.3731008) |
| 39 | arXiv:2504.21318 |  |  | 6 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression, Prefill/Decode Disaggregation / Selective KV Transfer, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2504.21318) |
| 40 | OpenReview:xXTkbTBmqq |  |  | 6 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分, Quantization × MoE × Offload, inference-systems, task-specific MoE pruning / translation specialist extraction / expert routing specialization | [source](https://openreview.net/forum?id=xXTkbTBmqq) |
| 41 | arXiv:2402.18158 |  |  | 6 | Quantization × MoE × Offload, Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.18158) |
| 42 | DOI:10.1109/ispass57527.2023.00035 |  |  | 6 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, other-inference-systems | [source](https://doi.org/10.1109/ispass57527.2023.00035) |
| 43 | arXiv:2012.15701 |  |  | 6 | Conditional Computation, Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2012.15701) |
| 44 | arXiv:2403.12031 |  |  | 6 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 45 | DOI:10.18653/v1/2023.emnlp-main.825 |  |  | 6 | 07-kv-cache-optimization-compression, Long-context serving / KV cache benchmark, adaptive-expert-computation-compression | [source](https://doi.org/10.18653/v1/2023.emnlp-main.825) |
| 46 | OpenReview:7Bywt2mQsCe |  |  | 6 | KV Cache Optimization / Compression, Speculative decoding × MoE, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Bywt2mQsCe) |
| 47 | arXiv:1904.09324 |  |  | 6 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1904.09324) |
| 48 | OpenReview:L057s2Rq8O |  |  | 6 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=L057s2Rq8O) |
| 49 | OpenReview:ALzTQUgW8a |  |  | 6 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ALzTQUgW8a) |
| 50 | DOI:10.1145/3620666.3651352 |  |  | 5 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, inference-systems, long-context sparse attention / KV-cache bandwidth reduction / GPU-PIM heterogeneous decoding / predictive attention masks, offload-hierarchical-memory, speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime | [source](https://doi.org/10.1145/3620666.3651352) |
| 51 | arXiv:1603.08983 |  |  | 5 | 99-other-inference-systems, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, conditional computation / mixture-of-experts / mixture-of-depths / KV-cache quantization / adaptive inference | [source](https://arxiv.org/abs/1603.08983) |
| 52 | DOI:10.1109/micro56248.2022.00051 |  |  | 5 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, inference-systems, kv-cache-memory | [source](https://doi.org/10.1109/micro56248.2022.00051) |
| 53 | OpenReview:Bl8u7ZRlbM |  |  | 5 | 11-llm-serving-scheduling-disaggregation, KV cache reuse / context caching / multi-tenant LLM serving / selective recomputation, agent serving / KV-cache reuse / latent communication / DAG workflows, many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://openreview.net/forum?id=Bl8u7ZRlbM) |
| 54 | arXiv:2302.10866 |  |  | 5 | Conditional Computation, inference-systems, training-memory-systems | [source](https://arxiv.org/abs/2302.10866) |
| 55 | arXiv:2405.21075 |  |  | 5 | 11-llm-serving-scheduling-disaggregation, 13-sparse-attention, Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2405.21075) |
| 56 | DOI:10.1145/3779212.3790135 |  |  | 5 | LLM Serving / Speculative Decoding / Multi-tenant Resource Reuse, agentic workflow serving / multi-LLM serving / GPU allocation / fractional placement, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790135) |
| 57 | arXiv:1909.11556 |  |  | 5 | inference-systems, speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 58 | arXiv:2406.18139 |  |  | 5 | inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2406.18139) |
| 59 | DOI:10.18653/v1/2023.findings-emnlp.936 |  |  | 5 | Adaptive Expert Computation / Compression, inference-systems | [source](https://doi.org/10.18653/v1/2023.findings-emnlp.936) |
| 60 | arXiv:1910.13461 |  |  | 5 | inference-systems | [source](https://arxiv.org/abs/1910.13461) |
| 61 | arXiv:2208.03306 |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 62 | arXiv:2412.16434 |  |  | 4 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation, other-inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2412.16434) |
| 63 | arXiv:2506.06266 |  |  | 4 | KV Cache Optimization / Compression, KV cache compression / KV eviction / probabilistic inference / importance sampling, kv-cache-offload-recomputation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2506.06266) |
| 64 | DOI:10.1109/hpca53966.2022.00082 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, inference-systems, kv-cache-memory, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca53966.2022.00082) |
| 65 | DOI:10.1109/tmc.2024.3513457 |  |  | 4 | 05-speculative-decoding-moe, 08-edge-on-device-llm-systems, Edge / On-device LLM Systems, hardware-accelerators | [source](https://doi.org/10.1109/tmc.2024.3513457) |
| 66 | DOI:10.18653/v1/2025.acl-long.1126 |  |  | 4 | 10-kv-cache-offload-recomputation, distributed LLM serving / KV cache / latent attention / GPU fabrics, dynamic-pd-disaggregation, kv-cache-offload-recomputation | [source](https://doi.org/10.18653/v1/2025.acl-long.1126) |
| 67 | OpenReview:1qvx610Cu7 |  |  | 4 | 07-kv-cache-optimization-compression, MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, inference-systems, sparse attention / learned context ranking / long-context LLM inference | [source](https://openreview.net/forum?id=1qvx610Cu7) |
| 68 | OpenReview:uNrFpDPMyo |  |  | 4 | 10-kv-キャッシュ-オフロード-recomputation, CXL memory pooling / KV cache offload / disaggregated memory, KV Cache Optimization / Compression, other-inference-systems | [source](https://openreview.net/forum?id=uNrFpDPMyo) |
| 69 | arXiv:2311.10122 |  |  | 4 | Adaptive computation／cache-aware MoE, KV cache compression for multimodal inference, inference-systems | [source](https://arxiv.org/abs/2311.10122) |
| 70 | arXiv:2402.06082 |  |  | 4 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 71 | arXiv:2407.04014 |  |  | 4 | inference-systems, llm-serving-scheduling-disaggregation, serving-disaggregation | [source](https://arxiv.org/abs/2407.04014) |
| 72 | arXiv:2411.05239 |  |  | 4 | distributed LLM inference / communication-aware serving, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2411.05239) |
| 73 | arXiv:2502.17416 |  |  | 4 | Conditional Computation, adaptive-expert-computation-compression, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2502.17416) |
| 74 | arXiv:2507.11851 |  |  | 4 | Other Inference Systems / Lossless Parallel Decoding, inference-systems, speculative-decoding | [source](https://arxiv.org/abs/2507.11851) |
| 75 | DOI:10.1109/mm.2024.3375352 |  |  | 4 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, Offload / Hierarchical Memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/mm.2024.3375352) |
| 76 | DOI:10.1145/3572848.3577479 |  |  | 4 | 02-hardware-accelerators, inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1145/3572848.3577479) |
| 77 | DOI:10.1145/3731569.3764808 |  |  | 4 | edge-on-device-llm-systems, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://doi.org/10.1145/3731569.3764808) |
| 78 | DOI:10.48550/arxiv.2409.12136 |  |  | 4 | MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, inference-systems, survey-moe-inference-optimization | [source](https://doi.org/10.48550/arxiv.2409.12136) |
| 79 | OpenReview:R8sQPpGCv0 |  |  | 4 | 02-hardware-accelerators, KV cache memory management / streaming inference / attention sinks / length extrapolation, other-inference-systems | [source](https://openreview.net/forum?id=R8sQPpGCv0) |
| 80 | arXiv:1902.09574 |  |  | 4 | inference-systems, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 81 | arXiv:2004.02984 |  |  | 4 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2004.02984) |
| 82 | arXiv:2405.05329 |  |  | 4 | KV Cache Optimization / Compression, inference-systems | [source](https://arxiv.org/abs/2405.05329) |
| 83 | arXiv:2408.12570 |  |  | 4 | PIM / Near-Data Acceleration, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2408.12570) |
| 84 | DOI:10.1109/hpca57654.2024.00078 |  |  | 4 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, offload-hierarchical-memory | [source](https://doi.org/10.1109/hpca57654.2024.00078) |
| 85 | DOI:10.1145/3695053.3731092 |  |  | 4 | CPU推論、行列拡張、異種実行、ルーフライン最適化, block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://doi.org/10.1145/3695053.3731092) |
| 86 | OpenReview:MaYzugDmQV |  |  | 4 | Expert Prefetch, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=MaYzugDmQV) |
| 87 | OpenReview:ziezViPoN1 |  |  | 4 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=ziezViPoN1) |
| 88 | arXiv:2403.09054 |  |  | 4 | Conditional Computation | [source](https://arxiv.org/abs/2403.09054) |
| 89 | arXiv:2501.00663 |  |  | 4 | prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2501.00663) |
| 90 | DOI:10.48550/arxiv.2305.14152 |  |  | 4 | LLM inference surveys、roofline performance analysis | [source](https://doi.org/10.48550/arxiv.2305.14152) |
| 91 | arXiv:1704.04861 |  |  | 3 | KV Cache Optimization / Compression, inference-systems, on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1704.04861) |
| 92 | arXiv:2203.06390 |  |  | 3 | Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.06390) |
| 93 | arXiv:2307.01952 |  |  | 3 | Diffusion LLM Inference, LLM Serving / Scheduling / Disaggregation, MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2307.01952) |
| 94 | arXiv:2309.05516 |  |  | 3 | Expert Prefetch, inference-systems, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 95 | arXiv:2310.01655 |  |  | 3 | GPU Kernel Framework, KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2310.01655) |
| 96 | arXiv:2401.12522 |  |  | 3 | inference-systems, speculative-decoding, 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/2401.12522) |
| 97 | arXiv:2404.03605 |  |  | 3 | Conditional Computation, Quantization × MoE × Offload, inference-systems | [source](https://arxiv.org/abs/2404.03605) |
| 98 | arXiv:2406.00059 |  |  | 3 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, agentic serving / production workload characterization / KV-cache lifecycle / resource reclamation, inference-systems | [source](https://arxiv.org/abs/2406.00059) |
| 99 | arXiv:2406.11939 |  |  | 3 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2406.11939) |
| 100 | arXiv:2409.01990 |  |  | 3 | KV cache sparsity / paged attention / query-aware selection / LLM serving, inference-systems, moe | [source](https://arxiv.org/abs/2409.01990) |
| 101 | arXiv:2410.03834 |  |  | 3 | inference-systems, llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2410.03834) |
| 102 | arXiv:2410.17891 |  |  | 3 | Speculative Decoding, diffusion language model inference / KV cache / training-free acceleration, 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2410.17891) |
| 103 | arXiv:2411.11055 |  |  | 3 | Speculative decoding × MoE, inference-systems, 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://arxiv.org/abs/2411.11055) |
| 104 | arXiv:2502.06768 |  |  | 3 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory, diffusion language model inference / KV cache / training-free acceleration, inference-systems | [source](https://arxiv.org/abs/2502.06768) |
| 105 | arXiv:2503.09567 |  |  | 3 | Graph-CoT / multi-agent serving / KV-cache reuse, LLM Serving / Reasoning, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2503.09567) |
| 106 | arXiv:2504.17307 |  |  | 3 | KV Cache Offload / Recomputation, LLM Serving / Distributed Communication, LLMサービング／スケジューリング／分離実行 | [source](https://arxiv.org/abs/2504.17307) |
| 107 | arXiv:2507.14111 |  |  | 3 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2507.14111) |
| 108 | DOI:10.1016/j.jpdc.2017.12.007 |  |  | 3 | GPU architecture and tensor-computation orchestration, LLM Serving / Distributed Communication, inference-systems | [source](https://doi.org/10.1016/j.jpdc.2017.12.007) |
| 109 | DOI:10.1109/lca.2026.3705817 |  |  | 3 | HBF / hierarchical memory / KV-cache management / LLM serving, KVキャッシュ階層メモリ・SSD/HBFオフロード・フラッシュ特性評価, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3705817) |
| 110 | DOI:10.1109/sc41406.2024.00094 |  |  | 3 | KV Cache Optimization / Compression, llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1109/sc41406.2024.00094) |
| 111 | DOI:10.1145/3458864.3467882 |  |  | 3 | Edge／on-device MoE, LLMサービング・スケジューリング・分離実行, other-inference-systems | [source](https://doi.org/10.1145/3458864.3467882) |
| 112 | DOI:10.1145/3575693.3576933 |  |  | 3 | inference-systems, kernel-runtime-compilation, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://doi.org/10.1145/3575693.3576933) |
| 113 | DOI:10.1145/3695053.3731101 |  |  | 3 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators | [source](https://doi.org/10.1145/3695053.3731101) |
| 114 | DOI:10.1145/3779212.3790187 |  |  | 3 | MoE expert offloading / predictive prefetch and cache management, hierarchical-memory-kv-offload-cpu-gpu-attention, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://doi.org/10.1145/3779212.3790187) |
| 115 | DOI:10.48550/arxiv.2507.17702 |  |  | 3 | adaptive expert computation / compression; end-side sparse MoE, fine-grained MoE / atomic experts / product routing / expert-centric GPU scheduling, 拡散LLM推論／動的復号粒度／配信スケジューリング／KVキャッシュ／GPU飽和制御 | [source](https://doi.org/10.48550/arxiv.2507.17702) |
| 116 | OpenReview:1YDeZU8Lt5 |  |  | 3 | MoE expert pruning / expert clustering / task-specific model compression, MoE推論・エキスパートオフロード・エキスパートキャッシュ・ルーティング局所性, MoE量子化 / 混合精度 / 共有スペクトル基底 / 活性依存ビット配分 | [source](https://openreview.net/forum?id=1YDeZU8Lt5) |
| 117 | OpenReview:CS2JWaziYr |  |  | 3 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=CS2JWaziYr) |
| 118 | OpenReview:rJl-b3RcF7 |  |  | 3 | MoE architecture / hardware-software co-design / latent expert computation / Nemotron-3, MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://openreview.net/forum?id=rJl-b3RcF7) |
| 119 | OpenReview:VtmBAGCN7o |  |  | 3 | 14-agentic-inference-serving-runtime, MoE圧縮 / expert pruning / expert merging / post-compression adjustment, agentic workflow serving / workflow physical planning / adaptive serving | [source](https://openreview.net/forum?id=VtmBAGCN7o) |
| 120 | arXiv:1311.2540 |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 121 | arXiv:1711.09224 |  |  | 3 | 02-hardware-accelerators, unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1711.09224) |
| 122 | arXiv:2105.06990 |  |  | 3 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2105.06990) |
| 123 | arXiv:2302.02451 |  |  | 3 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2302.02451) |
| 124 | arXiv:2304.08485 |  |  | 3 | speculative-decoding, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.08485) |
| 125 | arXiv:2307.08072 |  |  | 3 | CPUオフロード / 活性化疎性 / 階層メモリ, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.08072) |
| 126 | arXiv:2310.03744 |  |  | 3 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 127 | arXiv:2311.05232 |  |  | 3 | LLM inference surveys、roofline performance analysis, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2311.05232) |
| 128 | arXiv:2401.13601 |  |  | 3 | LLM inference surveys、roofline performance analysis, multimodal mixture-of-experts / dynamic expert allocation / budget-aware routing | [source](https://arxiv.org/abs/2401.13601) |
| 129 | arXiv:2402.09353 |  |  | 3 | Conditional Computation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.09353) |
| 130 | arXiv:2403.12422 |  |  | 3 | survey-distributed-training-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.12422) |
| 131 | arXiv:2407.05483 |  |  | 3 | Long-context serving / KV cache benchmark, linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2407.05483) |
| 132 | arXiv:2408.04667 |  |  | 3 | Inference Kernel / Determinism, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2408.04667) |
| 133 | arXiv:2409.02813 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2409.02813) |
| 134 | arXiv:2410.12876 |  |  | 3 | inference-systems, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.12876) |
| 135 | arXiv:2411.04996 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 14-agentic-inference-serving-runtime | [source](https://arxiv.org/abs/2411.04996) |
| 136 | arXiv:2412.16545 |  |  | 3 | 10-kv-cache-offload-recomputation, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2412.16545) |
| 137 | arXiv:2503.16419 |  |  | 3 | Conditional Computation, LLM Serving / Reasoning | [source](https://arxiv.org/abs/2503.16419) |
| 138 | arXiv:2506.01844 |  |  | 3 | 18-vla-inference-quantization-evaluation, LLM Inference / VLA Quantization / Low-Bit Inference | [source](https://arxiv.org/abs/2506.01844) |
| 139 | arXiv:2507.19595 |  |  | 3 | KV Cache Optimization / Compression, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2507.19595) |
| 140 | arXiv:2510.08544 |  |  | 3 | llm-serving-scheduling-disaggregation, offload-hierarchical-memory | [source](https://arxiv.org/abs/2510.08544) |
| 141 | arXiv:2602.23881 |  |  | 3 | 11-llm-serving-scheduling-disaggregation, 投機的デコード、並列ブロックドラフタ、DFlash、受理率指向学習。 | [source](https://arxiv.org/abs/2602.23881) |
| 142 | DOI:10.1109/hpca61900.2025.00126 |  |  | 3 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00126) |
| 143 | DOI:10.1109/mm.2022.3163226 |  |  | 3 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2022.3163226) |
| 144 | DOI:10.1145/3453483.3454083 |  |  | 3 | dynamic megakernel compilation and GPU task scheduling, kernel-runtime-compilation | [source](https://doi.org/10.1145/3453483.3454083) |
| 145 | DOI:10.1145/3627535.3638466 |  |  | 3 | KV Cache Optimization / Compression, serving-scheduling | [source](https://doi.org/10.1145/3627535.3638466) |
| 146 | DOI:10.1145/3710848.3710869 |  |  | 3 | Adaptive computation／cache-aware MoE, moe-parallelism-communication | [source](https://doi.org/10.1145/3710848.3710869) |
| 147 | DOI:10.1162/tacl%5fa%5f00266 |  |  | 3 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment | [source](https://doi.org/10.1162/tacl%5fa%5f00266) |
| 148 | DOI:10.18653/v1/2023.acl-long.792 |  |  | 3 | inference-systems, multi-LLM serving / hardware-aware routing / SLO-aware scheduling / load balancing | [source](https://doi.org/10.18653/v1/2023.acl-long.792) |
| 149 | DOI:10.5281/zenodo.1234 |  |  | 3 | inference-systems, エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://doi.org/10.5281/zenodo.1234) |
| 150 | OpenReview:6PmJoRfdaK |  |  | 3 | inference-systems, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=6PmJoRfdaK) |
| 151 | OpenReview:BOfDKxfwt0 |  |  | 3 | KV-cache scheduling / non-clairvoyant scheduling / memory-constrained batching, llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=BOfDKxfwt0) |
| 152 | OpenReview:jxpsAj7ltE |  |  | 3 | Adaptive Expert Computation / Compression, adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://openreview.net/forum?id=jxpsAj7ltE) |
| 153 | OpenReview:uBaFH7aQnC |  |  | 3 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=uBaFH7aQnC) |
| 154 | arXiv:1410.5401 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/1410.5401) |
| 155 | arXiv:1809.08887 |  |  | 3 | 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/1809.08887) |
| 156 | arXiv:1910.06360 |  |  | 3 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 157 | arXiv:2205.07324 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2205.07324) |
| 158 | arXiv:2212.08136 |  |  | 3 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.08136) |
| 159 | arXiv:2305.19466 |  |  | 3 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2305.19466) |
| 160 | arXiv:2402.01032 |  |  | 3 | sparse attention / KV-cache bandwidth reduction | [source](https://arxiv.org/abs/2402.01032) |
| 161 | arXiv:2404.02060 |  |  | 3 | Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2404.02060) |
| 162 | arXiv:2405.10637 |  |  | 3 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2405.10637) |
| 163 | arXiv:2410.13848 |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2410.13848) |
| 164 | arXiv:2503.14476 |  |  | 3 | 99-other-inference-systems | [source](https://arxiv.org/abs/2503.14476) |
| 165 | arXiv:2606.04101 |  |  | 3 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2606.04101) |
| 166 | DOI:10.1145/3638757 |  |  | 3 | inference-systems | [source](https://doi.org/10.1145/3638757) |
| 167 | OpenReview:dHng2O0Jjr |  |  | 3 | agentic serving / KV cache eviction / persistent multi-turn serving | [source](https://openreview.net/forum?id=dHng2O0Jjr) |
| 168 | arXiv:1911.00172 |  |  | 3 |  | [source](https://arxiv.org/abs/1911.00172) |
| 169 | arXiv:2204.00408 |  |  | 3 |  | [source](https://arxiv.org/abs/2204.00408) |
| 170 | arXiv:2505.11594 |  |  | 3 |  | [source](https://arxiv.org/abs/2505.11594) |
| 171 | DOI:10.18653/v1/p19-1580 |  |  | 3 |  | [source](https://doi.org/10.18653/v1/p19-1580) |
| 172 | arXiv:1409.3215 |  |  | 2 | MoE expert offloading / predictive prefetch and cache management, inference-systems | [source](https://arxiv.org/abs/1409.3215) |
| 173 | arXiv:1802.04730 |  |  | 2 | GPU Kernel Framework, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/1802.04730) |
| 174 | arXiv:1903.05662 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, Weight Quantization / Compression | [source](https://arxiv.org/abs/1903.05662) |
| 175 | arXiv:1909.06708 |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1909.06708) |
| 176 | arXiv:2004.07320 |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2004.07320) |
| 177 | arXiv:2006.10901 |  |  | 2 | inference-systems, オフロード／階層メモリ | [source](https://arxiv.org/abs/2006.10901) |
| 178 | arXiv:2010.03768 |  |  | 2 | augmented LLM serving / KV cache management / predictive scheduling / vLLM, inference-systems | [source](https://arxiv.org/abs/2010.03768) |
| 179 | arXiv:2102.08602 |  |  | 2 | training-memory-systems, 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2102.08602) |
| 180 | arXiv:2104.07012 |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/2104.07012) |
| 181 | arXiv:2107.11906 |  |  | 2 | inference-systems, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2107.11906) |
| 182 | arXiv:2110.14883 |  |  | 2 | inference-systems, training-memory-systems | [source](https://arxiv.org/abs/2110.14883) |
| 183 | arXiv:2203.05740 |  |  | 2 | inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.05740) |
| 184 | arXiv:2206.01859 |  |  | 2 | inference-systems, post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2206.01859) |
| 185 | arXiv:2210.03350 |  |  | 2 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, inference-systems | [source](https://arxiv.org/abs/2210.03350) |
| 186 | arXiv:2301.08721 |  |  | 2 | inference-systems, kv-cache-memory | [source](https://arxiv.org/abs/2301.08721) |
| 187 | arXiv:2303.10130 |  |  | 2 | MoE inference / on-device LLM / expert offloading / expert caching, inference-systems | [source](https://arxiv.org/abs/2303.10130) |
| 188 | arXiv:2304.05128 |  |  | 2 | training-memory-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2304.05128) |
| 189 | arXiv:2305.07759 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.07759) |
| 190 | arXiv:2306.04050 |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 191 | arXiv:2307.09782 |  |  | 2 | LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.09782) |
| 192 | arXiv:2308.12908 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2308.12908) |
| 193 | arXiv:2309.10400 |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 194 | arXiv:2310.00746 |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 195 | arXiv:2310.18339 |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 196 | arXiv:2311.09550 |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 197 | arXiv:2311.17311 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 198 | arXiv:2312.03788 |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 199 | arXiv:2312.11918 |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11918) |
| 200 | arXiv:2401.14112 |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 201 | arXiv:2402.03216 |  |  | 2 | 07-kv-cache-optimization-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2402.03216) |
| 202 | arXiv:2402.12851 |  |  | 2 | survey-low-bit-llm, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2402.12851) |
| 203 | arXiv:2402.18679 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 204 | arXiv:2403.09032 |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2403.09032) |
| 205 | arXiv:2403.20041 |  |  | 2 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://arxiv.org/abs/2403.20041) |
| 206 | arXiv:2404.09173 |  |  | 2 | KV Cache Compression / Long Context, inference-systems | [source](https://arxiv.org/abs/2404.09173) |
| 207 | arXiv:2404.13628 |  |  | 2 | 02-adaptive-expert-computation-compression, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2404.13628) |
| 208 | arXiv:2405.11530 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2405.11530) |
| 209 | arXiv:2405.21015 |  |  | 2 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation, その他システム研究 | [source](https://arxiv.org/abs/2405.21015) |
| 210 | arXiv:2406.04594 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.04594) |
| 211 | arXiv:2406.07394 |  |  | 2 | Edge／on-device MoE, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2406.07394) |
| 212 | arXiv:2406.11612 |  |  | 2 | 11-llm-serving-スケジューラ-disaggregation, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2406.11612) |
| 213 | arXiv:2406.18820 |  |  | 2 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2406.18820) |
| 214 | arXiv:2407.08296 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, survey-low-bit-llm | [source](https://arxiv.org/abs/2407.08296) |
| 215 | arXiv:2407.11239 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2407.11239) |
| 216 | arXiv:2408.04323 |  |  | 2 | Agentic inference and serving runtime, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2408.04323) |
| 217 | arXiv:2409.16040 |  |  | 2 | MoE expert offloading / cross-layer expert prediction / adaptive prefetch / expert cache management / cache-aware routing, inference-systems | [source](https://arxiv.org/abs/2409.16040) |
| 218 | arXiv:2409.17481 |  |  | 2 | Conditional Computation, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2409.17481) |
| 219 | arXiv:2410.02223 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.02223) |
| 220 | arXiv:2410.03090 |  |  | 2 | inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2410.03090) |
| 221 | arXiv:2410.07985 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2410.07985) |
| 222 | arXiv:2410.13212 |  |  | 2 | KV cache compression / multi-agent KV sharing, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2410.13212) |
| 223 | arXiv:2410.14720 |  |  | 2 | MoE compression / expert pruning / neuron-level recombination / expert reconstruction, System-aware KV cache | [source](https://arxiv.org/abs/2410.14720) |
| 224 | arXiv:2410.19274 |  |  | 2 | edge-on-device-llm-systems, flash-capacity-tier-inference | [source](https://arxiv.org/abs/2410.19274) |
| 225 | arXiv:2411.04905 |  |  | 2 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2411.04905) |
| 226 | arXiv:2411.14199 |  |  | 2 | inference-systems, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2411.14199) |
| 227 | arXiv:2411.19799 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, inference-systems | [source](https://arxiv.org/abs/2411.19799) |
| 228 | arXiv:2412.12488 |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2412.12488) |
| 229 | arXiv:2501.01257 |  |  | 2 | inference-systems, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://arxiv.org/abs/2501.01257) |
| 230 | arXiv:2501.09686 |  |  | 2 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2501.09686) |
| 231 | arXiv:2501.12370 |  |  | 2 | MoE serving / expert offload / dynamic HBM repartitioning / KV-cache management / multi-turn agentic serving, 専門家混合推論 / バッチ対応専門家選択 / 専門家並列 / 投機的デコーディング | [source](https://arxiv.org/abs/2501.12370) |
| 232 | arXiv:2502.01662 |  |  | 2 | federated inference / speculative decoding / communication-efficient LLM inference, speculative decoding / multi-drafter serving / heterogeneous multi-node inference / pipeline scheduling | [source](https://arxiv.org/abs/2502.01662) |
| 233 | arXiv:2502.03461 |  |  | 2 | Graph-CoT / multi-agent serving / KV-cache reuse, MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2502.03461) |
| 234 | arXiv:2502.06703 |  |  | 2 | Mixture-of-Experts / test-time scaling / verifier-guided search / adaptive expert activation, inference-systems | [source](https://arxiv.org/abs/2502.06703) |
| 235 | arXiv:2502.08246 |  |  | 2 | inference-systems, sparse attention / learned context ranking / long-context LLM inference | [source](https://arxiv.org/abs/2502.08246) |
| 236 | arXiv:2502.11946 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.11946) |
| 237 | arXiv:2502.14317 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, inference-systems | [source](https://arxiv.org/abs/2502.14317) |
| 238 | arXiv:2502.15304 |  |  | 2 | 07-kv-cache-optimization-compression, KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2502.15304) |
| 239 | arXiv:2503.07545 |  |  | 2 | LLM配信／KVキャッシュ制約／連続バッチ処理／待ち行列・力学系, LLM配信／スケジューリング／分離 | [source](https://arxiv.org/abs/2503.07545) |
| 240 | arXiv:2503.13444 |  |  | 2 | kv-cache-offload-recomputation, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2503.13444) |
| 241 | arXiv:2503.24358 |  |  | 2 | KV cache quantization / RoPE-aware compression / packed attention serving, System-aware KV cache | [source](https://arxiv.org/abs/2503.24358) |
| 242 | arXiv:2504.06214 |  |  | 2 | llm-serving-scheduling-disaggregation, long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/2504.06214) |
| 243 | arXiv:2504.10903 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2504.10903) |
| 244 | arXiv:2504.16112 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, offload-hierarchical-memory | [source](https://arxiv.org/abs/2504.16112) |
| 245 | arXiv:2504.20101 |  |  | 2 | llm-serving-scheduling-disaggregation, 異種GPUサービング・分散推論・パイプライン並列・動的ルーティング | [source](https://arxiv.org/abs/2504.20101) |
| 246 | arXiv:2505.06708 |  |  | 2 | MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2505.06708) |
| 247 | arXiv:2505.10475 |  |  | 2 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, inference-systems | [source](https://arxiv.org/abs/2505.10475) |
| 248 | arXiv:2505.14681 |  |  | 2 | MoE routing / key expert enhancement / dynamic expert pruning / inference acceleration, fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2505.14681) |
| 249 | arXiv:2505.21411 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, 専門家混合推論・三次元NAND・計算内メモリ・フラッシュ内処理・端末内推論 | [source](https://arxiv.org/abs/2505.21411) |
| 250 | arXiv:2506.01928 |  |  | 2 | Other Inference Systems / Lossless Parallel Decoding, inference-systems | [source](https://arxiv.org/abs/2506.01928) |
| 251 | arXiv:2506.14038 |  |  | 2 | moe-quantization-compression, その他システム研究 | [source](https://arxiv.org/abs/2506.14038) |
| 252 | arXiv:2506.20639 |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference, inference-systems | [source](https://arxiv.org/abs/2506.20639) |
| 253 | arXiv:2507.02770 |  |  | 2 | GPU機密計算の性能評価、LLMサービング、KVキャッシュ退避、機密マルチGPU基盤, confidential inference / trusted execution environment / split inference / differential privacy | [source](https://arxiv.org/abs/2507.02770) |
| 254 | arXiv:2507.16099 |  |  | 2 | inference-systems, 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2507.16099) |
| 255 | arXiv:2508.02324 |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.02324) |
| 256 | arXiv:2508.07227 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://arxiv.org/abs/2508.07227) |
| 257 | arXiv:2508.10395 |  |  | 2 | 17-pim-near-data-acceleration, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2508.10395) |
| 258 | arXiv:2509.01142 |  |  | 2 | diffusion LLM inference / KV caching / fused attention / parallel decoding, 拡散言語モデルサービング・KVキャッシュ・プリフィル/デコード分離・連続バッチング | [source](https://arxiv.org/abs/2509.01142) |
| 259 | arXiv:2509.23202 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2509.23202) |
| 260 | arXiv:2510.00231 |  |  | 2 | KV cache compression / KV eviction / probabilistic inference / importance sampling, KVキャッシュ退避／長文推論／KV選択／KV量子化 | [source](https://arxiv.org/abs/2510.00231) |
| 261 | arXiv:2510.06513 |  |  | 2 | offload-hierarchical-memory, オフロード／階層メモリ | [source](https://arxiv.org/abs/2510.06513) |
| 262 | arXiv:2510.17483 |  |  | 2 | adaptive-expert-computation-compression, diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2510.17483) |
| 263 | arXiv:2511.05502 |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2511.05502) |
| 264 | arXiv:2511.20048 |  |  | 2 | llm-serving-scheduling-disaggregation, エージェント型大規模言語モデル配信／投機的道具実行／言語モデル・道具共同スケジューリング | [source](https://arxiv.org/abs/2511.20048) |
| 265 | arXiv:2512.01644 |  |  | 2 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, LLM serving resource provisioning / CPU-GPU orchestration / multi-GPU inference | [source](https://arxiv.org/abs/2512.01644) |
| 266 | arXiv:2512.07647 |  |  | 2 | 07-kv-cache-optimization-compression, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2512.07647) |
| 267 | arXiv:2512.16473 |  |  | 2 | Edge／on-device MoE, LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2512.16473) |
| 268 | arXiv:2601.02872 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://arxiv.org/abs/2601.02872) |
| 269 | arXiv:2601.07568 |  |  | 2 | edge-on-device-llm-systems, inference-systems | [source](https://arxiv.org/abs/2601.07568) |
| 270 | arXiv:2601.11589 |  |  | 2 | LLM Serving / Scheduling / Disaggregation, disaggregated LLM serving / request routing / learned scheduling | [source](https://arxiv.org/abs/2601.11589) |
| 271 | arXiv:2601.22379 |  |  | 2 | 07-kv-cache-optimization-compression, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2601.22379) |
| 272 | arXiv:2602.21224 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト, 投機的復号・ブロック拡散提案・検証器中間表現の再利用 | [source](https://arxiv.org/abs/2602.21224) |
| 273 | arXiv:2603.28101 |  |  | 2 | LLM inference simulation / disaggregated serving / performance modeling, agentic LLM serving / pipeline parallelism / serving scheduling / speculative decoding | [source](https://arxiv.org/abs/2603.28101) |
| 274 | arXiv:2605.20315 |  |  | 2 | 11-llm-serving-scheduling-disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2605.20315) |
| 275 | arXiv:2606.22874 |  |  | 2 | 13-sparse-attention, kv-cache-optimization-compression | [source](https://arxiv.org/abs/2606.22874) |
| 276 | DOI:10.1007/978-3-319-58667-0_18 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1007/978-3-319-58667-0_18) |
| 277 | DOI:10.1038/s41467-024-45563-x |  |  | 2 | KVキャッシュ退避／長文推論／KV選択／KV量子化, inference-systems | [source](https://doi.org/10.1038/s41467-024-45563-x) |
| 278 | DOI:10.1109/dac63849.2025.11132870 |  |  | 2 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード, offload-hierarchical-memory | [source](https://doi.org/10.1109/dac63849.2025.11132870) |
| 279 | DOI:10.1109/hcs55958.2022.9895629 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, offload-hierarchical-memory | [source](https://doi.org/10.1109/hcs55958.2022.9895629) |
| 280 | DOI:10.1109/hotchips.2019.8875654 |  |  | 2 | KV Cache Optimization / Compression, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation | [source](https://doi.org/10.1109/hotchips.2019.8875654) |
| 281 | DOI:10.1109/hpca47549.2020.00030 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, kv-cache-memory | [source](https://doi.org/10.1109/hpca47549.2020.00030) |
| 282 | DOI:10.1109/hpca61900.2025.00127 |  |  | 2 | offload-hierarchical-memory, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/hpca61900.2025.00127) |
| 283 | DOI:10.1109/iccv.2019.00038 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, mixed-precision weight quantization / Fisher sensitivity / RL bit allocation | [source](https://doi.org/10.1109/iccv.2019.00038) |
| 284 | DOI:10.1109/ipdps.2001.924976 |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://doi.org/10.1109/ipdps.2001.924976) |
| 285 | DOI:10.1109/isca.2016.41 |  |  | 2 | inference-systems, offload-hierarchical-memory | [source](https://doi.org/10.1109/isca.2016.41) |
| 286 | DOI:10.1109/iscas51556.2021.9401196 |  |  | 2 | GPU architecture and tensor-computation orchestration, inference-systems | [source](https://doi.org/10.1109/iscas51556.2021.9401196) |
| 287 | DOI:10.1109/isscc42614.2022.9731711 |  |  | 2 | DRAM-PIMによるLLMデコード高速化 / 長文脈注意のチャネル並列化・KV容量管理, inference-systems | [source](https://doi.org/10.1109/isscc42614.2022.9731711) |
| 288 | DOI:10.1109/lca.2023.3305386 |  |  | 2 | inference-systems, offload-hierarchical-memory | [source](https://doi.org/10.1109/lca.2023.3305386) |
| 289 | DOI:10.1109/lca.2026.3695938 |  |  | 2 | HBF / hierarchical memory / KV-cache management / LLM serving, オフロード／階層メモリ | [source](https://doi.org/10.1109/lca.2026.3695938) |
| 290 | DOI:10.1109/mm.2023.3256384 |  |  | 2 | LLM serving simulation / heterogeneous accelerators / disaggregation / memory hierarchy / hardware-software co-design, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1109/mm.2023.3256384) |
| 291 | DOI:10.1109/mm.2025.3592688 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, moe-parallelism-communication | [source](https://doi.org/10.1109/mm.2025.3592688) |
| 292 | DOI:10.1109/tc.2020.2984496 |  |  | 2 | inference-systems, 端末内LLM・処理内メモリ・LPDDR-PIM・重み配置・実行時並べ替え | [source](https://doi.org/10.1109/tc.2020.2984496) |
| 293 | DOI:10.1109/tpds.2022.3217824 |  |  | 2 | Inference Kernel / Determinism, other-inference-systems | [source](https://doi.org/10.1109/tpds.2022.3217824) |
| 294 | DOI:10.1115/1.3662552 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1115/1.3662552) |
| 295 | DOI:10.1145/1365490.1365500 |  |  | 2 | hardware-accelerators, inference-systems | [source](https://doi.org/10.1145/1365490.1365500) |
| 296 | DOI:10.1145/224056.224064 |  |  | 2 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/224056.224064) |
| 297 | DOI:10.1145/2517349.2522716 |  |  | 2 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/2517349.2522716) |
| 298 | DOI:10.1145/3123939.3124544 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, inference-systems | [source](https://doi.org/10.1145/3123939.3124544) |
| 299 | DOI:10.1145/3240765.3240801 |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, inference-systems | [source](https://doi.org/10.1145/3240765.3240801) |
| 300 | DOI:10.1145/3352460.3358284 |  |  | 2 | inference-systems, offload-hierarchical-memory | [source](https://doi.org/10.1145/3352460.3358284) |
| 301 | DOI:10.1145/3466752.3480080 |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference, inference-systems | [source](https://doi.org/10.1145/3466752.3480080) |
| 302 | DOI:10.1145/3538643.3539742 |  |  | 2 | 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://doi.org/10.1145/3538643.3539742) |
| 303 | DOI:10.1145/3575693.3575754 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-offload-routing | [source](https://doi.org/10.1145/3575693.3575754) |
| 304 | DOI:10.1145/3591300 |  |  | 2 | GPUカーネル融合／SwiGLU／LLM推論ランタイム, LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://doi.org/10.1145/3591300) |
| 305 | DOI:10.1145/3620665.3640410 |  |  | 2 | llm-serving-scheduling-disaggregation, moe-parallelism-communication | [source](https://doi.org/10.1145/3620665.3640410) |
| 306 | DOI:10.1145/3649506 |  |  | 2 | MoE expert pruning / expert clustering / task-specific model compression, Offload / Hierarchical Memory | [source](https://doi.org/10.1145/3649506) |
| 307 | DOI:10.1145/3689031.3696070 |  |  | 2 | inference-systems, serving-scheduling | [source](https://doi.org/10.1145/3689031.3696070) |
| 308 | DOI:10.1145/3695053.3731064 |  |  | 2 | MoE serving / attention-MoE disaggregation / asynchronous inference, inference-systems | [source](https://doi.org/10.1145/3695053.3731064) |
| 309 | DOI:10.1145/3725843.3756041 |  |  | 2 | GPU architecture and tensor-computation orchestration, GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://doi.org/10.1145/3725843.3756041) |
| 310 | DOI:10.1145/3731569.3764829 |  |  | 2 | Prefill/Decode Disaggregation / Selective KV Transfer, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3731569.3764829) |
| 311 | DOI:10.1145/3779212.3790188 |  |  | 2 | heterogeneous distributed inference / collective communication / cross-stack serving / communication compilation, llm-serving-scheduling-disaggregation | [source](https://doi.org/10.1145/3779212.3790188) |
| 312 | DOI:10.1147/rd.395.0575 |  |  | 2 | hardware-accelerators, inference-systems | [source](https://doi.org/10.1147/rd.395.0575) |
| 313 | DOI:10.1609/aaai.v38i16.29720 |  |  | 2 | 10-kv-キャッシュ-オフロード-recomputation, 14-agentic-inference-serving-runtime | [source](https://doi.org/10.1609/aaai.v38i16.29720) |
| 314 | DOI:10.18653/v1/2022.acl-long.502 |  |  | 2 | 07-kv-cache-optimization-compression, KVキャッシュ最適化／適応圧縮 | [source](https://doi.org/10.18653/v1/2022.acl-long.502) |
| 315 | DOI:10.18653/v1/2024.emnlp-main.1038 |  |  | 2 | fine-grained MoE inference / expert skipping / expert pruning / serving efficiency, offload-hierarchical-memory | [source](https://doi.org/10.18653/v1/2024.emnlp-main.1038) |
| 316 | DOI:10.18653/v1/2024.findings-emnlp.899 |  |  | 2 | kv-cache-optimization-compression, query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://doi.org/10.18653/v1/2024.findings-emnlp.899) |
| 317 | DOI:10.18653/v1/2026.acl-long.83 |  |  | 2 | 13-sparse-attention, KVキャッシュ最適化／圧縮 | [source](https://doi.org/10.18653/v1/2026.acl-long.83) |
| 318 | DOI:10.18653/v1/p19-1346 |  |  | 2 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment, inference-systems | [source](https://doi.org/10.18653/v1/p19-1346) |
| 319 | DOI:10.48550/arxiv.2212.04356 |  |  | 2 | inference-systems, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系 | [source](https://doi.org/10.48550/arxiv.2212.04356) |
| 320 | DOI:10.52202/068431-2198 |  |  | 2 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, early-exit-offloading-self-speculative-decoding | [source](https://doi.org/10.52202/068431-2198) |
| 321 | DOI:10.52202/075280-2020 |  |  | 2 | early-exit-offloading-self-speculative-decoding, inference-systems | [source](https://doi.org/10.52202/075280-2020) |
| 322 | DOI:10.52202/079017-3180 |  |  | 2 | adaptive-expert-computation-compression, low-bit VLM inference / microscaling / hardware-software co-design | [source](https://doi.org/10.52202/079017-3180) |
| 323 | DOI:10.57967/hf/0638 |  |  | 2 | inference-systems, survey-speculative-decoding | [source](https://doi.org/10.57967/hf/0638) |
| 324 | OpenReview:2c7pfOqu9k |  |  | 2 | speculative decoding / hybrid-attention serving / recurrent linear attention / SGLang runtime, その他の推論システム | [source](https://openreview.net/forum?id=2c7pfOqu9k) |
| 325 | OpenReview:B1VZqjAcYX |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, inference-systems | [source](https://openreview.net/forum?id=B1VZqjAcYX) |
| 326 | OpenReview:d0mGsaheuT |  |  | 2 | inference-systems, 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://openreview.net/forum?id=d0mGsaheuT) |
| 327 | OpenReview:EKJhH5D5wA |  |  | 2 | speculative-decoding, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=EKJhH5D5wA) |
| 328 | OpenReview:H4DqfPSibmx |  |  | 2 | Speculative decoding × MoE, kv-cache-offload-recomputation | [source](https://openreview.net/forum?id=H4DqfPSibmx) |
| 329 | OpenReview:JFygzwx8SJ |  |  | 2 | KV Cache Optimization / Compression, kv-cache-optimization-compression | [source](https://openreview.net/forum?id=JFygzwx8SJ) |
| 330 | OpenReview:mtSSFiqW6y |  |  | 2 | speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=mtSSFiqW6y) |
| 331 | OpenReview:R0SoZvqXyQ |  |  | 2 | llm-serving-scheduling-disaggregation, serving-scheduling | [source](https://openreview.net/forum?id=R0SoZvqXyQ) |
| 332 | OpenReview:rsY6J3ZaTF |  |  | 2 | speculative decoding / draft-model design, 自己投機的復号・長文脈推論・疎注意・連続バッチ処理 | [source](https://openreview.net/forum?id=rsY6J3ZaTF) |
| 333 | OpenReview:uLYc4L3C81A |  |  | 2 | Conditional Computation, inference-systems | [source](https://openreview.net/forum?id=uLYc4L3C81A) |
| 334 | OpenReview:YolJOZOGhI |  |  | 2 | KV cache persistence / edge multi-agent inference / storage offload, KVキャッシュ記憶、長期LLMエージェント、アクセス制御 | [source](https://openreview.net/forum?id=YolJOZOGhI) |
| 335 | arXiv:1312.6114 |  |  | 2 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 336 | arXiv:1703.09844 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1703.09844) |
| 337 | arXiv:1806.02847 |  |  | 2 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 338 | arXiv:1902.04610 |  |  | 2 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1902.04610) |
| 339 | arXiv:1905.00537 |  |  | 2 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1905.00537) |
| 340 | arXiv:1906.00532 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1906.00532) |
| 341 | arXiv:1909.01315 |  |  | 2 | sparse attention / KV-cache bandwidth reduction | [source](https://arxiv.org/abs/1909.01315) |
| 342 | arXiv:2004.08900 |  |  | 2 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 343 | arXiv:2009.14167 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2009.14167) |
| 344 | arXiv:2011.04006 |  |  | 2 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2011.04006) |
| 345 | arXiv:2103.13076 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2103.13076) |
| 346 | arXiv:2110.12894 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 347 | arXiv:2112.01488 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2112.01488) |
| 348 | arXiv:2204.09656 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2204.09656) |
| 349 | arXiv:2205.10625 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2205.10625) |
| 350 | arXiv:2208.09225 |  |  | 2 | 投機的デコード・バッチ推論 | [source](https://arxiv.org/abs/2208.09225) |
| 351 | arXiv:2210.13438 |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2210.13438) |
| 352 | arXiv:2211.15533 |  |  | 2 | Speculative Decoding | [source](https://arxiv.org/abs/2211.15533) |
| 353 | arXiv:2212.10509 |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2212.10509) |
| 354 | arXiv:2303.02141 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2303.02141) |
| 355 | arXiv:2303.17951 |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2303.17951) |
| 356 | arXiv:2305.07622 |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2305.07622) |
| 357 | arXiv:2305.14160 |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 358 | arXiv:2305.18403 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.18403) |
| 359 | arXiv:2306.03805 |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2306.03805) |
| 360 | arXiv:2306.13596 |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 361 | arXiv:2309.14021 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.14021) |
| 362 | arXiv:2312.03134 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2312.03134) |
| 363 | arXiv:2402.00157 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.00157) |
| 364 | arXiv:2403.03187 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.03187) |
| 365 | arXiv:2403.17887 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2403.17887) |
| 366 | arXiv:2404.18322 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2404.18322) |
| 367 | arXiv:2405.06001 |  |  | 2 | survey-low-bit-llm | [source](https://arxiv.org/abs/2405.06001) |
| 368 | arXiv:2406.02924 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2406.02924) |
| 369 | arXiv:2406.15319 |  |  | 2 | KVキャッシュ退避・再計算・階層ストレージ・接頭辞キャッシュ | [source](https://arxiv.org/abs/2406.15319) |
| 370 | arXiv:2407.11963 |  |  | 2 | serving-scheduling | [source](https://arxiv.org/abs/2407.11963) |
| 371 | arXiv:2408.00264 |  |  | 2 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2408.00264) |
| 372 | arXiv:2409.03215 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2409.03215) |
| 373 | arXiv:2410.02725 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2410.02725) |
| 374 | arXiv:2410.12388 |  |  | 2 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2410.12388) |
| 375 | arXiv:2410.19313 |  |  | 2 | diffusion-llm-inference / caching / low-precision | [source](https://arxiv.org/abs/2410.19313) |
| 376 | arXiv:2411.05902 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2411.05902) |
| 377 | arXiv:2412.12094 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2412.12094) |
| 378 | arXiv:2412.18547 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2412.18547) |
| 379 | arXiv:2501.03895 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2501.03895) |
| 380 | arXiv:2501.17399 |  |  | 2 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2501.17399) |
| 381 | arXiv:2502.03387 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2502.03387) |
| 382 | arXiv:2502.08691 |  |  | 2 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2502.08691) |
| 383 | arXiv:2502.14786 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2502.14786) |
| 384 | arXiv:2502.20586 |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2502.20586) |
| 385 | arXiv:2504.00906 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2504.00906) |
| 386 | arXiv:2505.07686 |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2505.07686) |
| 387 | arXiv:2505.20411 |  |  | 2 | other | [source](https://arxiv.org/abs/2505.20411) |
| 388 | arXiv:2505.23419 |  |  | 2 | ローカル大規模言語モデル推論／Apple Silicon／統合メモリ／推論基盤比較／複数機推論 | [source](https://arxiv.org/abs/2505.23419) |
| 389 | arXiv:2506.06122 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2506.06122) |
| 390 | arXiv:2506.22694 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2506.22694) |
| 391 | arXiv:2508.18224 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2508.18224) |
| 392 | arXiv:2509.25140 |  |  | 2 | エージェントメモリ、動的ベクトル検索、ANNインデックス、マルチエージェント基盤、CPU-GPU階層メモリ | [source](https://arxiv.org/abs/2509.25140) |
| 393 | arXiv:2510.20733 |  |  | 2 | multi-LLM communication / KV-cache semantic transfer | [source](https://arxiv.org/abs/2510.20733) |
| 394 | arXiv:2511.19269 |  |  | 2 | block diffusion LLM serving / KV-cache offloading / sparse attention / heterogeneous CPU-GPU memory | [source](https://arxiv.org/abs/2511.19269) |
| 395 | arXiv:2601.06007 |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2601.06007) |
| 396 | arXiv:2603.08721 |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2603.08721) |
| 397 | arXiv:2604.24432 |  |  | 2 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2604.24432) |
| 398 | arXiv:2605.09992 |  |  | 2 | speculative-decoding | [source](https://arxiv.org/abs/2605.09992) |
| 399 | arXiv:2605.22791 |  |  | 2 | linear attention / delta-rule associative memory / state-space models / Bayesian filtering | [source](https://arxiv.org/abs/2605.22791) |
| 400 | DOI:10.1109/cvpr52733.2024.00913 |  |  | 2 | 13-sparse-attention | [source](https://doi.org/10.1109/cvpr52733.2024.00913) |
| 401 | DOI:10.1109/iccad45719.2019.8942127 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/iccad45719.2019.8942127) |
| 402 | DOI:10.1109/isca45697.2020.00045 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isca45697.2020.00045) |
| 403 | DOI:10.1109/isca66397.2026.00021 |  |  | 2 | MoE expert offloading / predictive prefetch and cache management | [source](https://doi.org/10.1109/isca66397.2026.00021) |
| 404 | DOI:10.1109/isscc.2017.7870333 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/isscc.2017.7870333) |
| 405 | DOI:10.1109/sc41405.2020.00073 |  |  | 2 | inference-systems | [source](https://doi.org/10.1109/sc41405.2020.00073) |
| 406 | DOI:10.1145/2541940.2541941 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2541940.2541941) |
| 407 | DOI:10.1145/2939672.2939785 |  |  | 2 | inference-systems | [source](https://doi.org/10.1145/2939672.2939785) |
| 408 | DOI:10.1145/3241539.3241559 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3241539.3241559) |
| 409 | DOI:10.1145/3447993.3483249 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3447993.3483249) |
| 410 | DOI:10.1145/3510611 |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://doi.org/10.1145/3510611) |
| 411 | DOI:10.1145/3581791.3596831 |  |  | 2 | Edge／on-device MoE | [source](https://doi.org/10.1145/3581791.3596831) |
| 412 | DOI:10.1145/3710848.3710868 |  |  | 2 | Adaptive computation／cache-aware MoE | [source](https://doi.org/10.1145/3710848.3710868) |
| 413 | DOI:10.1162/tacl_a_00290 |  |  | 2 | inference-systems | [source](https://doi.org/10.1162/tacl_a_00290) |
| 414 | DOI:10.18653/v1/2020.acl-main.204 |  |  | 2 | Conditional Computation | [source](https://doi.org/10.18653/v1/2020.acl-main.204) |
| 415 | DOI:10.18653/v1/2020.findings-emnlp.372 |  |  | 2 | 投機的デコード / 分布保存型デコード高速化 | [source](https://doi.org/10.18653/v1/2020.findings-emnlp.372) |
| 416 | DOI:10.18653/v1/2022.findings-acl.177 |  |  | 2 | MoE compression / training-free expert merging / multimodal MoE routing | [source](https://doi.org/10.18653/v1/2022.findings-acl.177) |
| 417 | DOI:10.18653/v1/2023.emnlp-main.183 |  |  | 2 | 投機的復号・ターゲット隠れ状態再利用・並列ブロックドラフト | [source](https://doi.org/10.18653/v1/2023.emnlp-main.183) |
| 418 | DOI:10.18653/v1/2023.emnlp-main.907 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/2023.emnlp-main.907) |
| 419 | DOI:10.18653/v1/2024.emnlp-main.897 |  |  | 2 | kv-cache-optimization-compression | [source](https://doi.org/10.18653/v1/2024.emnlp-main.897) |
| 420 | DOI:10.18653/v1/2025.acl-long.671 |  |  | 2 | Mixture-of-Experts / adaptive expert computation / layer-wise expert allocation / task-conditioned routing | [source](https://doi.org/10.18653/v1/2025.acl-long.671) |
| 421 | DOI:10.18653/v1/d18-2012 |  |  | 2 | 投機的復号・異種語彙・トークナイザ互換性・損失なし検証 | [source](https://doi.org/10.18653/v1/d18-2012) |
| 422 | DOI:10.18653/v1/s17-2001 |  |  | 2 | adaptive expert computation / expert merging / curvature-aware merging / game-theoretic optimization | [source](https://doi.org/10.18653/v1/s17-2001) |
| 423 | DOI:10.64434/tml.20251026 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://doi.org/10.64434/tml.20251026) |
| 424 | OpenReview:7Ttk3RzDeu |  |  | 2 | 07-kv-cache-optimization-compression | [source](https://openreview.net/forum?id=7Ttk3RzDeu) |
| 425 | OpenReview:br4H61LOoI |  |  | 2 | inference-systems | [source](https://openreview.net/forum?id=br4H61LOoI) |
| 426 | OpenReview:CybBmzWBX0 |  |  | 2 | early-exit-offloading-self-speculative-decoding | [source](https://openreview.net/forum?id=CybBmzWBX0) |
| 427 | OpenReview:DOZiCWyK0N |  |  | 2 | llm-serving-scheduling-disaggregation | [source](https://openreview.net/forum?id=DOZiCWyK0N) |
| 428 | OpenReview:ISqx8giekS |  |  | 2 | kv-cache-optimization-compression | [source](https://openreview.net/forum?id=ISqx8giekS) |
| 429 | OpenReview:LWMS4pk2vK |  |  | 2 | query-aware sparse attention / KV selection / tail compensation / CPU offload | [source](https://openreview.net/forum?id=LWMS4pk2vK) |
| 430 | OpenReview:qrMo6R7lOS |  |  | 2 | multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://openreview.net/forum?id=qrMo6R7lOS) |
| 431 | OpenReview:tVConYid20 |  |  | 2 | kernel-runtime-compilation | [source](https://openreview.net/forum?id=tVConYid20) |
| 432 | OpenReview:v3w2a7EInO |  |  | 2 | Conditional Computation | [source](https://openreview.net/forum?id=v3w2a7EInO) |
| 433 | OpenReview:YrycTjllL0 |  |  | 2 | KVキャッシュ圧縮・疎注意・階層メモリ・長文脈MoE推論 | [source](https://openreview.net/forum?id=YrycTjllL0) |
| 434 | arXiv:2006.16362 |  |  | 2 |  | [source](https://arxiv.org/abs/2006.16362) |
| 435 | arXiv:2104.06022 |  |  | 2 |  | [source](https://arxiv.org/abs/2104.06022) |
| 436 | arXiv:2212.10554 |  |  | 2 |  | [source](https://arxiv.org/abs/2212.10554) |
| 437 | arXiv:2310.01405 |  |  | 2 |  | [source](https://arxiv.org/abs/2310.01405) |
| 438 | arXiv:2402.14830 |  |  | 2 |  | [source](https://arxiv.org/abs/2402.14830) |
| 439 | arXiv:2404.08819 |  |  | 2 |  | [source](https://arxiv.org/abs/2404.08819) |
| 440 | arXiv:2406.09246 |  |  | 2 |  | [source](https://arxiv.org/abs/2406.09246) |
| 441 | arXiv:2410.04417 |  |  | 2 |  | [source](https://arxiv.org/abs/2410.04417) |
| 442 | arXiv:2411.07140 |  |  | 2 |  | [source](https://arxiv.org/abs/2411.07140) |
| 443 | arXiv:2501.13987 |  |  | 2 |  | [source](https://arxiv.org/abs/2501.13987) |
| 444 | arXiv:2503.07518 |  |  | 2 |  | [source](https://arxiv.org/abs/2503.07518) |
| 445 | arXiv:2506.08373 |  |  | 2 |  | [source](https://arxiv.org/abs/2506.08373) |
| 446 | DOI:10.1145/3503222.3507752 |  |  | 2 |  | [source](https://doi.org/10.1145/3503222.3507752) |
| 447 | DOI:10.18653/v1/2021.findings-acl.449 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/2021.findings-acl.449) |
| 448 | DOI:10.18653/v1/d19-1223 |  |  | 2 |  | [source](https://doi.org/10.18653/v1/d19-1223) |
| 449 | DOI:10.48550/arxiv.2309.03852 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2309.03852) |
| 450 | DOI:10.48550/arxiv.2411.02886 |  |  | 2 |  | [source](https://doi.org/10.48550/arxiv.2411.02886) |
| 451 | OpenReview:4D0f16Vwc3 |  |  | 2 |  | [source](https://openreview.net/forum?id=4D0f16Vwc3) |
| 452 | OpenReview:Ai8Hw3AXqks |  |  | 2 |  | [source](https://openreview.net/forum?id=Ai8Hw3AXqks) |
| 453 | OpenReview:iBBcRUlOAPR |  |  | 2 |  | [source](https://openreview.net/forum?id=iBBcRUlOAPR) |
| 454 | OpenReview:n6SCkn2QaG |  |  | 2 |  | [source](https://openreview.net/forum?id=n6SCkn2QaG) |
| 455 | OpenReview:tkiZQlL04w |  |  | 2 |  | [source](https://openreview.net/forum?id=tkiZQlL04w) |
| 456 | arXiv:1203.0056 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1203.0056) |
| 457 | arXiv:1207.0580 |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 458 | arXiv:1211.5590 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1211.5590) |
| 459 | arXiv:1307.2118 |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1307.2118) |
| 460 | arXiv:1406.7362 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1406.7362) |
| 461 | arXiv:1411.1792 |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1411.1792) |
| 462 | arXiv:1505.05571 |  |  | 1 | MoE数値再現性・決定論的推論・実行時互換性 | [source](https://arxiv.org/abs/1505.05571) |
| 463 | arXiv:1506.03099 |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1506.03099) |
| 464 | arXiv:1508.04025 |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1508.04025) |
| 465 | arXiv:1511.05950 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 466 | arXiv:1511.08228 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1511.08228) |
| 467 | arXiv:1601.06733 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1601.06733) |
| 468 | arXiv:1602.02068 |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/1602.02068) |
| 469 | arXiv:1602.07360 |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1602.07360) |
| 470 | arXiv:1603.05691 |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1603.05691) |
| 471 | arXiv:1606.02891 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.02891) |
| 472 | arXiv:1609.05140 |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1609.05140) |
| 473 | arXiv:1611.00712 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1611.00712) |
| 474 | arXiv:1611.01600 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1611.01600) |
| 475 | arXiv:1612.07837 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 476 | arXiv:1702.02815 |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/1702.02815) |
| 477 | arXiv:1703.04247 |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1703.04247) |
| 478 | arXiv:1705.03122 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1705.03122) |
| 479 | arXiv:1707.01873 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 480 | arXiv:1710.10903 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1710.10903) |
| 481 | arXiv:1712.01887 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1712.01887) |
| 482 | arXiv:1801.10198 |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1801.10198) |
| 483 | arXiv:1802.06509 |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1802.06509) |
| 484 | arXiv:1803.05407 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1803.05407) |
| 485 | arXiv:1804.06028 |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/1804.06028) |
| 486 | arXiv:1805.04833 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1805.04833) |
| 487 | arXiv:1806.08159 |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1806.08159) |
| 488 | arXiv:1807.11143 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 489 | arXiv:1808.08558 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1808.08558) |
| 490 | arXiv:1809.00732 |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 491 | arXiv:1810.00602 |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/1810.00602) |
| 492 | arXiv:1810.05291 |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.05291) |
| 493 | arXiv:1811.01088 |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1811.01088) |
| 494 | arXiv:1812.01243 |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1812.01243) |
| 495 | arXiv:1812.09764 |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/1812.09764) |
| 496 | arXiv:1902.05613 |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1902.05613) |
| 497 | arXiv:1902.09113 |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1902.09113) |
| 498 | arXiv:1903.01611 |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1903.01611) |
| 499 | arXiv:1904.01145 |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1904.01145) |
| 500 | arXiv:1904.10631 |  |  | 1 | long-context training / hierarchical memory / activation recomputation / KV-cache offload | [source](https://arxiv.org/abs/1904.10631) |

## Machine-readable

同じ割当は [worker-worklist-30.json](worker-worklist-30.json) にあります。

