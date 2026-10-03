# Scheduled worker :45 worklist

Worker: `scheduled-chat-45`  
Generated: `2026-10-03T13:58:01+00:00`

このページはこのworker専用の再構築可能な選択索引です。他のScheduled worker用ページとは候補を重複させません（十分な在庫がある場合）。
正本は `.survey/work-queue/jobs/`、claim、論文実体、relevance ledgerです。処理直前に最新正本を再確認してください。

- このページに割り当てられた候補だけを使用する。
- Library-first runでは、同じidentityの完成原稿・探索結果がChatGPT Libraryへ保存済みならskipする。
- 最新状態で処理済み・claim済み・対象外ならskipし、同じページ内の次候補へ進む。
- Discoveryは候補提示面にすぎない。10件へ数える前にcanonical identityをGitHubとChatGPT Libraryの両方で照合して未処理の新規候補だと確認し、その後に一次資料本文を読み、accept / unrelated / borderline を判定する。既処理・重複が判明した候補は10件から外して補充する。タイトル・要旨だけでacceptしない。

## 未処理 Research / Audit

ready総数: **606** / 未claim総数: **459** / このworker向け: **153**

| # | score | 種別 | identity | title | source | 想定配置先 |
|---:|---:|---|---|---|---|---|
| 1 | 0 | research | arXiv:1701.06538 | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | [primary](https://arxiv.org/abs/1701.06538) | `papers/inference/05-moe/2017-1701.06538-sparsely-gated-moe.md` |
| 2 | 0 | research | arXiv:1805.02867 | Online normalizer calculation for softmax | [primary](https://arxiv.org/abs/1805.02867) | `papers/inference/99-other-inference-systems/2018-1805.02867-online-normalizer-calculation-for-softmax.md` |
| 3 | 0 | research | arXiv:2006.02464 | Serving DNNs like Clockwork: Performance Predictability from the Bottom Up | [primary](https://arxiv.org/abs/2006.02464) | `papers/inference/99-other-inference-systems/2020-2006.02464-serving-dnns-like-clockwork-performance-predictability-from-the-bottom-up.md` |
| 4 | 0 | research | arXiv:2009.14794 | Rethinking Attention with Performers | [primary](https://arxiv.org/abs/2009.14794) | `papers/inference/99-other-inference-systems/2020-2009.14794-rethinking-attention-with-performers.md` |
| 5 | 0 | research | arXiv:2101.03961 | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | [primary](https://arxiv.org/abs/2101.03961) | `papers/inference/99-other-inference-systems/2021-2101.03961-switch-transformers-scaling-to-trillion-parameter-models-with-simple-and-efficient-sparsity.md` |
| 6 | 0 | research | arXiv:2109.01611 | Multi-model Machine Learning Inference Serving with GPU Spatial Partitioning | [primary](https://arxiv.org/abs/2109.01611) | `papers/inference/99-other-inference-systems/2021-2109.01611-multi-model-machine-learning-inference-serving-with-gpu-spatial-partitioning.md` |
| 7 | 0 | research | arXiv:2110.14895 | Pipeline Parallelism for Inference on Heterogeneous Edge Computing | [primary](https://arxiv.org/abs/2110.14895) | `papers/inference/99-other-inference-systems/2021-2110.14895-pipeline-parallelism-for-inference-on-heterogeneous-edge-computing.md` |
| 8 | 0 | research | arXiv:2201.12023 | Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning | [primary](https://arxiv.org/abs/2201.12023) | `papers/inference/99-other-inference-systems/2022-2201.12023-alpa-automating-inter-and-intra-operator-parallelism-for-distributed-deep-learning.md` |
| 9 | 0 | research | arXiv:2206.01861 | ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers | [primary](https://arxiv.org/abs/2206.01861) | `papers/inference/99-other-inference-systems/2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-scale-transformers.md` |
| 10 | 0 | research | arXiv:2209.01188 | Petals: Collaborative Inference and Fine-tuning of Large Models | [primary](https://arxiv.org/abs/2209.01188) | `papers/inference/99-other-inference-systems/2022-2209.01188-petals-collaborative-inference-and-fine-tuning-of-large-models.md` |
| 11 | 0 | research | arXiv:2301.00774 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | [primary](https://www.semanticscholar.org/paper/909ad57ce8caa6b390a65ae09db352d27d8f3996) | `papers/inference/99-other-inference-systems/2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md` |
| 12 | 0 | research | arXiv:2305.01625 | Unlimiformer: Long-Range Transformers with Unlimited Length Input | [primary](https://arxiv.org/abs/2305.01625) | `papers/inference/99-other-inference-systems/2023-2305.01625-unlimiformer-long-range-transformers-with-unlimited-length-input.md` |
| 13 | 0 | research | arXiv:2305.16300 | Landmark Attention: Random-Access Infinite Context Length for Transformers | [primary](https://arxiv.org/abs/2305.16300) | `papers/inference/99-other-inference-systems/2023-2305.16300-landmark-attention-random-access-infinite-context-length-for-transformers.md` |
| 14 | 0 | research | arXiv:2306.08543 | MiniLLM: On-Policy Distillation of Large Language Models | [primary](https://arxiv.org/abs/2306.08543) | `papers/inference/99-other-inference-systems/2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md` |
| 15 | 0 | research | arXiv:2307.06945 | In-context Autoencoder for Context Compression in a Large Language Model | [primary](https://arxiv.org/abs/2307.06945) | `papers/inference/99-other-inference-systems/2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md` |
| 16 | 0 | research | arXiv:2309.16354 | Transformer-VQ: Linear-Time Transformers via Vector Quantization | [primary](https://arxiv.org/abs/2309.16354) | `papers/inference/99-other-inference-systems/2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md` |
| 17 | 0 | research | arXiv:2310.05015 | Compresso: Structured Pruning with Collaborative Prompting Learns Compact Large Language Models | [primary](https://arxiv.org/abs/2310.05015) | `papers/inference/99-other-inference-systems/2023-2310.05015-compresso-structured-pruning-with-collaborative-prompting-learns-compact-large-language-models.md` |
| 18 | 0 | research | arXiv:2310.06927 | Sparse Fine-tuning for Inference Acceleration of Large Language Models | [primary](https://arxiv.org/abs/2310.06927) | `papers/inference/99-other-inference-systems/2023-2310.06927-sparse-fine-tuning-for-inference-acceleration-of-large-language-models.md` |
| 19 | 0 | research | arXiv:2310.08915 | Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs | [primary](https://arxiv.org/abs/2310.08915) | `papers/inference/99-other-inference-systems/2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md` |
| 20 | 0 | research | arXiv:2311.01282 | FlashDecoding++: Faster Large Language Model Inference on GPUs | [primary](https://arxiv.org/abs/2311.01282) | `papers/inference/99-other-inference-systems/2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md` |
| 21 | 0 | research | arXiv:2312.09193 | Fast Sampling via Discrete Non-Markov Diffusion Models with Predetermined Transition Time | [primary](https://arxiv.org/abs/2312.09193) | `papers/inference/99-other-inference-systems/2023-2312.09193-fast-sampling-via-discrete-non-markov-diffusion-models-with-predetermined-transition-time.md` |
| 22 | 0 | research | arXiv:2312.15234 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | [primary](https://arxiv.org/abs/2312.15234) | `papers/inference/99-other-inference-systems/2023-2312.15234-towards-efficient-generative-large-language-model-serving-a-survey-from-algorithms-to-systems.md` |
| 23 | 0 | research | arXiv:2401.04658 | Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models | [primary](https://arxiv.org/abs/2401.04658) | `papers/inference/99-other-inference-systems/2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengths-in-large-language-models.md` |
| 24 | 0 | research | arXiv:2401.08383 | Exploiting Inter-Layer Expert Affinity for Accelerating Mixture-of-Experts Model Inference | [primary](https://arxiv.org/abs/2401.08383) | `papers/inference/99-other-inference-systems/2024-2401.08383-exploiting-inter-layer-expert-affinity-for-accelerating-mixture-of-experts-model-inference.md` |
| 25 | 0 | research | arXiv:2402.02082 | GliDe with a CaPE: A Low-Hassle Method to Accelerate Speculative Decoding | [primary](https://arxiv.org/abs/2402.02082) | `papers/inference/99-other-inference-systems/2024-2402.02082-glide-with-a-cape-a-low-hassle-method-to-accelerate-speculative-decoding.md` |
| 26 | 0 | research | arXiv:2402.04902 | L4Q: Parameter Efficient Quantization-Aware Fine-Tuning on Large Language Models | [primary](https://arxiv.org/abs/2402.04902) | `papers/inference/99-other-inference-systems/2024-2402.04902-l4q-parameter-efficient-quantization-aware-fine-tuning-on-large-language-models.md` |
| 27 | 0 | research | arXiv:2402.10076 | QUICK: Quantization-aware Interleaving and Conflict-free Kernel for efficient LLM inference | [primary](https://arxiv.org/abs/2402.10076) | `papers/inference/99-other-inference-systems/2024-2402.10076-quick-quantization-aware-interleaving-and-conflict-free-kernel-for-efficient-llm-inference.md` |
| 28 | 0 | research | arXiv:2402.11295 | OneBit: Towards Extremely Low-bit Large Language Models | [primary](https://arxiv.org/abs/2402.11295) | `papers/inference/99-other-inference-systems/2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md` |
| 29 | 0 | research | arXiv:2402.12280 | Plato: Plan to Efficiently Decode for Large Language Model Inference | [primary](https://arxiv.org/abs/2402.12280) | `papers/inference/99-other-inference-systems/2024-2402.12280-plato-plan-to-efficiently-decode-for-large-language-model-inference.md` |
| 30 | 0 | research | arXiv:2402.15220 | ChunkAttention: Efficient Self-Attention with Prefix-Aware KV Cache and Two-Phase Partition | [primary](https://arxiv.org/abs/2402.15220) | `papers/inference/99-other-inference-systems/2024-2402.15220-chunkattention-efficient-self-attention-with-prefix-aware-kv-cache-and-two-phase-partition.md` |
| 31 | 0 | research | arXiv:2402.17985 | FlattenQuant: Breaking through the Inference Compute-bound for Large Language Models with Per-tensor Quantization | [primary](https://arxiv.org/abs/2402.17985) | `papers/inference/99-other-inference-systems/2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-language-models-with-per-tensor-quantization.md` |
| 32 | 0 | research | arXiv:2403.01136 | LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Aware Partition and Adaptive Quantization | [primary](https://arxiv.org/abs/2403.01136) | `papers/inference/99-other-inference-systems/2024-2403.01136-llm-pq-serving-llm-on-heterogeneous-clusters-with-phase-aware-partition-and-adaptive-quantization.md` |
| 33 | 0 | research | arXiv:2403.03853 | ShortGPT: Layers in Large Language Models are More Redundant Than You Expect | [primary](https://arxiv.org/abs/2403.03853) | `papers/inference/99-other-inference-systems/2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-expect.md` |
| 34 | 0 | research | arXiv:2403.08245 | Scattered Mixture-of-Experts Implementation | [primary](https://arxiv.org/abs/2403.08245) | `papers/inference/99-other-inference-systems/2024-2403.08245-scattered-mixture-of-experts-implementation.md` |
| 35 | 0 | research | arXiv:2403.12844 | MELTing Point: Mobile Evaluation of Language Transformers | [primary](https://arxiv.org/abs/2403.12844) | `papers/inference/99-other-inference-systems/2024-2403.12844-melting-point-mobile-evaluation-of-language-transformers.md` |
| 36 | 0 | research | arXiv:2403.16971 | AIOS: LLM Agent Operating System | [primary](https://arxiv.org/abs/2403.16971) | `papers/inference/99-other-inference-systems/2024-2403.16971-aios-llm-agent-operating-system.md` |
| 37 | 0 | research | arXiv:2404.00456 | QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs | [primary](https://arxiv.org/abs/2404.00456) | `papers/inference/99-other-inference-systems/2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md` |
| 38 | 0 | research | arXiv:2404.03605 | Mitigating the Impact of Outlier Channels for Language Model Quantization with Activation Regularization | [primary](https://arxiv.org/abs/2404.03605) | `papers/inference/99-other-inference-systems/2024-2404.03605-mitigating-the-impact-of-outlier-channels-for-language-model-quantization-with-activation-regularization.md` |
| 39 | 0 | research | arXiv:2404.06954 | Accelerating Inference in Large Language Models with a Unified Layer Skipping Strategy | [primary](https://arxiv.org/abs/2404.06954) | `papers/inference/99-other-inference-systems/2024-2404.06954-accelerating-inference-in-large-language-models-with-a-unified-layer-skipping-strategy.md` |
| 40 | 0 | research | arXiv:2404.08763 |  | [primary](https://arxiv.org/abs/2404.08763) | `papers/inference/99-other-inference-systems/2024-2404.08763-paper.md` |
| 41 | 0 | research | arXiv:2404.12457 | RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation | [primary](https://arxiv.org/abs/2404.12457) | `papers/inference/99-other-inference-systems/2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md` |
| 42 | 0 | research | arXiv:2405.05465 | Vidur: A Large-Scale Simulation Framework For LLM Inference | [primary](https://arxiv.org/abs/2405.05465) | `papers/inference/99-other-inference-systems/2024-2405.05465-vidur-a-large-scale-simulation-framework-for-llm-inference.md` |
| 43 | 0 | research | arXiv:2405.14297 | Dynamic Mixture of Experts: An Auto-Tuning Approach for Efficient Transformer Models | [primary](https://arxiv.org/abs/2405.14297) | `papers/inference/02-adaptive-expert-computation-compression/2024-2405.14297-dynmoe-auto-tuning.md` |
| 44 | 0 | research | arXiv:2405.16406 | SpinQuant: LLM quantization with learned rotations | [primary](https://arxiv.org/abs/2405.16406) | `papers/inference/99-other-inference-systems/2024-2405.16406-spinquant-llm-quantization-with-learned-rotations.md` |
| 45 | 0 | research | arXiv:2406.06858 | FLUX: Fast Software-based Communication Overlap On GPUs Through Kernel Fusion | [primary](https://arxiv.org/abs/2406.06858) | `papers/inference/99-other-inference-systems/2024-2406.06858-flux-fast-software-based-communication-overlap-on-gpus-through-kernel-fusion.md` |
| 46 | 0 | research | arXiv:2407.00088 | T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge | [primary](https://arxiv.org/abs/2407.00088) | `papers/inference/99-other-inference-systems/2024-2407.00088-t-mac-cpu-renaissance-via-table-lookup-for-low-bit-llm-deployment-on-edge.md` |
| 47 | 0 | research | arXiv:2407.05467 | The infrastructure powering IBM's Gen AI model development | [primary](https://arxiv.org/abs/2407.05467) | `papers/inference/99-other-inference-systems/2024-2407.05467-the-infrastructure-powering-ibm-s-gen-ai-model-development.md` |
| 48 | 0 | research | arXiv:2407.12391 | LLM Inference Serving: Survey of Recent Advances and Opportunities | [primary](https://arxiv.org/abs/2407.12391) | `papers/inference/99-other-inference-systems/2024-2407.12391-llm-inference-serving-survey-of-recent-advances-and-opportunities.md` |
| 49 | 0 | research | arXiv:2409.00142 | Dynamic Depth Decoding: Faster Speculative Decoding for LLMs | [primary](https://arxiv.org/abs/2409.00142) | `papers/inference/99-other-inference-systems/2024-2409.00142-dynamic-depth-decoding-faster-speculative-decoding-for-llms.md` |
| 50 | 0 | research | arXiv:2409.02060 | OLMoE: Open Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2409.02060) | `papers/inference/99-other-inference-systems/2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md` |
| 51 | 0 | research | arXiv:2410.04199 | LongGenBench: Long-context Generation Benchmark | [primary](https://arxiv.org/abs/2410.04199) | `papers/inference/99-other-inference-systems/2024-2410.04199-longgenbench-long-context-generation-benchmark.md` |
| 52 | 0 | research | arXiv:2411.01288 | Hexa-MoE: Efficient and Heterogeneous-aware Training for Mixture-of-Experts | [primary](https://arxiv.org/abs/2411.01288) | `papers/inference/99-other-inference-systems/2024-2411.01288-hexa-moe-efficient-and-heterogeneous-aware-training-for-mixture-of-experts.md` |
| 53 | 0 | research | arXiv:2412.03213 | ClusterKV: Manipulating LLM KV Cache in Semantic Space for Recallable Compression | [primary](https://arxiv.org/abs/2412.03213) | `papers/inference/99-other-inference-systems/2024-2412.03213-clusterkv-manipulating-llm-kv-cache-in-semantic-space-for-recallable-compression.md` |
| 54 | 0 | research | arXiv:2412.15803 | WebLLM: A High-Performance In-Browser LLM Inference Engine | [primary](https://arxiv.org/abs/2412.15803) | `papers/inference/99-other-inference-systems/2024-2412.15803-webllm-a-high-performance-in-browser-llm-inference-engine.md` |
| 55 | 0 | research | arXiv:2412.21187 | Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs | [primary](https://arxiv.org/abs/2412.21187) | `papers/inference/99-other-inference-systems/2024-2412.21187-do-not-think-that-much-for-2-3-on-the-overthinking-of-o1-like-llms.md` |
| 56 | 0 | research | arXiv:2502.09334 | ThunderServe: High-performance and Cost-efficient LLM Serving in Cloud Environments | [primary](https://arxiv.org/abs/2502.09334) | `papers/inference/99-other-inference-systems/2025-2502.09334-thunderserve-high-performance-and-cost-efficient-llm-serving-in-cloud-environments.md` |
| 57 | 0 | research | arXiv:2502.14051 | RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression | [primary](https://arxiv.org/abs/2502.14051) | `papers/inference/99-other-inference-systems/2025-2502.14051-rocketkv-accelerating-long-context-llm-inference-via-two-stage-kv-cache-compression.md` |
| 58 | 0 | research | arXiv:2502.18137 | SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference | [primary](https://arxiv.org/abs/2502.18137) | `papers/inference/99-other-inference-systems/2025-2502.18137-spargeattention-accurate-and-training-free-sparse-attention-accelerating-any-model-inference.md` |
| 59 | 0 | research | arXiv:2503.00979 | Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs | [primary](https://arxiv.org/abs/2503.00979) | `papers/inference/99-other-inference-systems/2025-2503.00979-dialogue-without-limits-constant-sized-kv-caches-for-extended-responses-in-llms.md` |
| 60 | 0 | research | arXiv:2503.18989 | A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models | [primary](https://arxiv.org/abs/2503.18989) | `papers/inference/99-other-inference-systems/2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-large-language-models.md` |
| 61 | 0 | research | arXiv:2504.12397 | Activated LoRA: Fine-tuned LLMs for Intrinsics | [primary](https://arxiv.org/abs/2504.12397) | `papers/inference/99-other-inference-systems/2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md` |
| 62 | 0 | research | arXiv:2504.19720 | Taming the Titans: A Survey of Efficient LLM Inference Serving | [primary](https://arxiv.org/abs/2504.19720) | `papers/inference/99-other-inference-systems/2025-2504.19720-taming-the-titans-a-survey-of-efficient-llm-inference-serving.md` |
| 63 | 0 | research | arXiv:2505.20225 | FLAME-MoE: A Transparent End-to-End Research Platform for Mixture-of-Experts Language Models | [primary](https://arxiv.org/abs/2505.20225) | `papers/inference/99-other-inference-systems/2025-2505.20225-flame-moe-a-transparent-end-to-end-research-platform-for-mixture-of-experts-language-models.md` |
| 64 | 0 | research | arXiv:2506.02634 | KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider | [primary](https://arxiv.org/abs/2506.02634) | `papers/inference/99-other-inference-systems/2025-2506.02634-kvcache-cache-in-the-wild-characterizing-and-optimizing-kvcache-cache-at-a-large-cloud-provider.md` |
| 65 | 0 | research | arXiv:2506.09397 | SLED: A Speculative LLM Decoding Framework for Efficient Edge Serving | [primary](https://arxiv.org/abs/2506.09397) | `papers/inference/99-other-inference-systems/2025-2506.09397-sled-a-speculative-llm-decoding-framework-for-efficient-edge-serving.md` |
| 66 | 0 | research | arXiv:2507.00390 | MoNE: Replacing Redundant Experts with Lightweight Novices for Structured Pruning of MoE | [primary](https://arxiv.org/abs/2507.00390) | `papers/inference/02-adaptive-expert-computation-compression/2025-2507.00390-mone-lightweight-novices.md` |
| 67 | 0 | research | arXiv:2507.15465 | The New LLM Bottleneck: A Systems Perspective on Latent Attention and Mixture-of-Experts | [primary](https://arxiv.org/abs/2507.15465) | `papers/inference/99-other-inference-systems/2025-2507.15465-the-new-llm-bottleneck-a-systems-perspective-on-latent-attention-and-mixture-of-experts.md` |
| 68 | 0 | research | arXiv:2508.02401 | CompressKV: Semantic Retrieval Heads Know What Tokens are Not Important Before Generation | [primary](https://arxiv.org/abs/2508.02401) | `papers/inference/99-other-inference-systems/2025-2508.02401-compresskv-semantic-retrieval-heads-know-what-tokens-are-not-important-before-generation.md` |
| 69 | 0 | research | arXiv:2508.11661 | Sparse Attention across Multiple-context KV Cache | [primary](https://arxiv.org/abs/2508.11661) | `papers/inference/99-other-inference-systems/2025-2508.11661-sparse-attention-across-multiple-context-kv-cache.md` |
| 70 | 0 | research | arXiv:2509.01229 | LiquidGEMM: Hardware-Efficient W4A8 GEMM Kernel for High-Performance LLM Serving | [primary](https://arxiv.org/abs/2509.01229) | `papers/inference/99-other-inference-systems/2025-2509.01229-liquidgemm-hardware-efficient-w4a8-gemm-kernel-for-high-performance-llm-serving.md` |
| 71 | 0 | research | arXiv:2509.15940 | arXiv:2509.15940 | [primary](https://arxiv.org/abs/2509.15940) | `papers/inference/99-other-inference-systems/2025-2509.15940-arxiv-2509-15940.md` |
| 72 | 0 | research | arXiv:2509.26520 | Training Matryoshka Mixture-of-Experts for Elastic Inference-Time Expert Utilization | [primary](https://arxiv.org/abs/2509.26520) | `papers/inference/02-adaptive-expert-computation-compression/2025-2509.26520-matryoshka-moe-elastic-expert-utilization.md` |
| 73 | 0 | research | arXiv:2510.04371 | Speculative Actions: A Lossless Framework for Faster Agentic Systems | [primary](https://arxiv.org/abs/2510.04371) | `papers/inference/99-other-inference-systems/2025-2510.04371-speculative-actions-a-lossless-framework-for-faster-agentic-systems.md` |
| 74 | 0 | research | arXiv:2510.12872 | KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems | [primary](https://www.semanticscholar.org/paper/471de4fab0885f45dffb717512741128775bcbaa) | `papers/inference/99-other-inference-systems/2025-2510.12872-kvcomm-online-cross-context-kv-cache-communication-for-efficient-llm-based-multi-agent-systems.md` |
| 75 | 0 | research | arXiv:2510.14557 | MX+: Pushing the Limits of Microscaling Formats for Efficient Large Language Model Serving | [primary](https://arxiv.org/abs/2510.14557) | `papers/inference/99-other-inference-systems/2025-2510.14557-mx-pushing-the-limits-of-microscaling-formats-for-efficient-large-language-model-serving.md` |
| 76 | 0 | research | arXiv:2510.16040 | Kelle: Co-design KV Caching and eDRAM for Efficient LLM Serving in Edge Computing | [primary](https://arxiv.org/abs/2510.16040) | `papers/inference/06-kv-cache-memory/2025-2510.16040-kelle-kv-cache-edram-edge-serving.md` |
| 77 | 0 | research | arXiv:2511.03475 | ContextPilot: Fast Long-Context Inference via Context Reuse | [primary](https://www.semanticscholar.org/paper/55e8ff688d13948dfbb496af1b565057f5ba5114) | `papers/inference/99-other-inference-systems/2025-2511.03475-contextpilot-fast-long-context-inference-via-context-reuse.md` |
| 78 | 0 | research | arXiv:2511.10676 | Pre-Attention Expert Prediction and Prefetching for Mixture-of-Experts Large Language Models | [primary](https://arxiv.org/abs/2511.10676) | `papers/inference/99-other-inference-systems/2025-2511.10676-pre-attention-expert-prediction-and-prefetching-for-mixture-of-experts-large-language-models.md` |
| 79 | 0 | research | arXiv:2511.19480 | Exploiting the Experts: Unauthorized Compression in MoE-LLMs | [primary](https://arxiv.org/abs/2511.19480) | `papers/inference/02-adaptive-expert-computation-compression/2025-2511.19480-unauthorized-moe-compression-expert-attribution.md` |
| 80 | 0 | research | arXiv:2512.22195 | MatKV: Trading Compute for Flash Storage in LLM Inference | [primary](https://arxiv.org/abs/2512.22195) | `papers/inference/99-other-inference-systems/2025-2512.22195-matkv-trading-compute-for-flash-storage-in-llm-inference.md` |
| 81 | 0 | research | arXiv:2601.05524 | Double: Breaking the Acceleration Limit via Double Retrieval Speculative Parallelism | [primary](https://arxiv.org/abs/2601.05524) | `papers/inference/99-other-inference-systems/2026-2601.05524-double-breaking-the-acceleration-limit-via-double-retrieval-speculative-parallelism.md` |
| 82 | 0 | research | arXiv:2601.19139 | Native LLM and MLLM Inference at Scale on Apple Silicon | [primary](https://arxiv.org/abs/2601.19139) | `papers/inference/99-other-inference-systems/2026-2601.19139-native-llm-and-mllm-inference-at-scale-on-apple-silicon.md` |
| 83 | 0 | research | arXiv:2602.09316 | Effective MoE-based LLM Compression by Exploiting Heterogeneous Inter-Group Experts Routing Frequency and Information Density | [primary](https://arxiv.org/abs/2602.09316) | `papers/inference/02-adaptive-expert-computation-compression/2026-2602.09316-rfid-moe-heterogeneous-svd-compression.md` |
| 84 | 0 | research | arXiv:2602.11812 | Predicting LLM Output Length via Entropy-Guided Representations | [primary](https://arxiv.org/abs/2602.11812) | `papers/inference/99-other-inference-systems/2026-2602.11812-predicting-llm-output-length-via-entropy-guided-representations.md` |
| 85 | 0 | research | arXiv:2602.22603 | SideQuest: Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning | [primary](https://arxiv.org/abs/2602.22603) | `papers/inference/99-other-inference-systems/2026-2602.22603-sidequest-model-driven-kv-cache-management-for-long-horizon-agentic-reasoning.md` |
| 86 | 0 | research | arXiv:2603.02599 | SUN: Shared Use of Next-token Prediction for Efficient Multi-LLM Disaggregated Serving | [primary](https://arxiv.org/abs/2603.02599) | `papers/inference/99-other-inference-systems/2026-2603.02599-sun-shared-use-of-next-token-prediction-for-efficient-multi-llm-disaggregated-serving.md` |
| 87 | 0 | research | arXiv:2603.10087 | Pooling Engram Conditional Memory in Large Language Models using CXL | [primary](http://arxiv.org/abs/2603.10087) | `papers/inference/99-other-inference-systems/2026-2603.10087-pooling-engram-conditional-memory-in-large-language-models-using-cxl.md` |
| 88 | 0 | research | arXiv:2603.18492 | AIMER: Calibration-Free Task-Agnostic MoE Expert Pruning | [primary](https://arxiv.org/abs/2603.18492) | `papers/inference/02-adaptive-expert-computation-compression/2026-2603.18492-aimer-calibration-free-pruning.md` |
| 89 | 0 | research | arXiv:2604.04722 | Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs | [primary](https://arxiv.org/abs/2604.04722) | `papers/inference/99-other-inference-systems/2026-2604.04722-don-t-waste-bits-adaptive-kv-cache-quantization-for-lightweight-on-device-llms.md` |
| 90 | 0 | research | arXiv:2604.11035 | Introspective Diffusion Language Models | [primary](https://arxiv.org/abs/2604.11035) | `papers/inference/99-other-inference-systems/2026-2604.11035-introspective-diffusion-language-models.md` |
| 91 | 0 | research | arXiv:2604.19835 | Expert Upcycling: Shifting the Compute-Efficient Frontier of Mixture-of-Experts | [primary](https://arxiv.org/abs/2604.19835) | `papers/training/02-distributed-heterogeneous-moe-training/2026-2604.19835-expert-upcycling-progressive-moe-expansion.md` |
| 92 | 0 | research | arXiv:2605.05696 | Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving | [primary](https://arxiv.org/abs/2605.05696) | `papers/inference/99-other-inference-systems/2026-2605.05696-irminsul-mla-native-position-independent-caching-for-agentic-llm-serving.md` |
| 93 | 0 | research | arXiv:2605.14249 | EnergyLens: Predictive Energy-Aware Exploration for Multi-GPU LLM Inference Optimization | [primary](https://arxiv.org/abs/2605.14249) | `papers/inference/99-other-inference-systems/2026-2605.14249-energylens.md` |
| 94 | 0 | research | arXiv:2605.26289 | Stateful Inference for Low-Latency Multi-Agent Tool Calling | [primary](https://arxiv.org/abs/2605.26289) | `papers/inference/99-other-inference-systems/2026-2605.26289-stateful-inference-for-low-latency-multi-agent-tool-calling.md` |
| 95 | 0 | research | arXiv:2606.01387 | Fail-Closed Lowering of Resident KV Claims onto LLM Serving Runtimes | [primary](https://arxiv.org/abs/2606.01387) | `papers/inference/99-other-inference-systems/2026-2606.01387-fail-closed-lowering-of-resident-kv-claims-onto-llm-serving-runtimes.md` |
| 96 | 0 | research | arXiv:2606.03819 | TreeFlash: Parallel AR-Approximation for Faster Speculative Decoding | [primary](https://arxiv.org/abs/2606.03819) | `papers/inference/99-other-inference-systems/2026-2606.03819-treeflash-parallel-ar-approximation-for-faster-speculative-decoding.md` |
| 97 | 0 | research | arXiv:2606.13054 | TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization | [primary](https://arxiv.org/abs/2606.13054) | `papers/inference/99-other-inference-systems/2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post-training-quantization.md` |
| 98 | 0 | research | arXiv:2606.16352 | Communication-Efficient Verifiable Attention for LLM Inference | [primary](https://arxiv.org/abs/2606.16352) | `papers/inference/99-other-inference-systems/2026-2606.16352-communication-efficient-verifiable-attention-for-llm-inference.md` |
| 99 | 0 | research | arXiv:2606.26650 | CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs | [primary](https://arxiv.org/abs/2606.26650) | `papers/inference/99-other-inference-systems/2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md` |
| 100 | 0 | research | arXiv:2607.06763 | Trees from Marginals: Autoregressive drafting with factorized priors | [primary](https://www.semanticscholar.org/paper/508b0bb474c86faf305f38ae7db6c9af532e2886) | `papers/inference/99-other-inference-systems/2026-2607.06763-trees-from-marginals-autoregressive-drafting-with-factorized-priors.md` |
| 101 | 0 | research | arXiv:2607.12839 | HeteroMosaic: Exposing and Exploiting Heterogeneous Execution Opportunities for Energy-Efficient Edge LLM Inference | [primary](https://arxiv.org/abs/2607.12839) | `papers/inference/99-other-inference-systems/2026-2607.12839-heteromosaic-exposing-and-exploiting-heterogeneous-execution-opportunities-for-energy-efficient-edge-llm-inference.md` |
| 102 | 0 | research | arXiv:2607.17415 | Transition-Aware Backend Dispatch for Edge LLM Inference | [primary](https://www.semanticscholar.org/paper/d338b6749faaf0cf77c1afd032c77f84257b9f3d) | `papers/inference/99-other-inference-systems/2026-2607.17415-transition-aware-backend-dispatch-for-edge-llm-inference.md` |
| 103 | 0 | research | arXiv:2608.01526 | An Internet for the KV Cache: Rethinking Classical Infrastructure Boundaries in the LLM Inference Age | [primary](https://arxiv.org/abs/2608.01526) | `papers/inference/99-other-inference-systems/2026-2608.01526-an-internet-for-the-kv-cache-rethinking-classical-infrastructure-boundaries-in-the-llm-inference-age.md` |
| 104 | 0 | research | arXiv:2608.07890 | Router Sensitivity Under Lightweight Fine-Tuning Identifies Prunable Experts in Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2608.07890) | `papers/inference/02-adaptive-expert-computation-compression/2026-2608.07890-router-sensitivity-prunable-experts.md` |
| 105 | 0 | research | arXiv:2608.13524 | DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees | [primary](https://arxiv.org/abs/2608.13524) | `papers/inference/99-other-inference-systems/2026-2608.13524-dartree-speculative-diffusion-decoding-with-autoregressive-draft-trees.md` |
| 106 | 0 | research | arXiv:2608.15118 | Collective Communication for Distributed LLM Systems: Planning, Runtime Adaptation, and Computation Coordination | [primary](https://arxiv.org/abs/2608.15118) | `papers/inference/99-other-inference-systems/2026-2608.15118-collective-communication-for-distributed-llm-systems-planning-runtime-adaptation-and-computation-coordination.md` |
| 107 | 0 | research | arXiv:2608.19395 | HYDRA: A Heterogeneous Chiplet DSE Framework for Serving Dynamic Hybrid LLM Workloads | [primary](https://www.semanticscholar.org/paper/65435abac34942c78717b5d15b0a2e437e59b568) | `papers/inference/99-other-inference-systems/2026-2608.19395-hydra-a-heterogeneous-chiplet-dse-framework-for-serving-dynamic-hybrid-llm-workloads.md` |
| 108 | 0 | research | arXiv:2608.23296 | Sigmoid Attention as a Better Substrate for Learned KV Cache Eviction | [primary](https://www.semanticscholar.org/paper/097ed39586269776fb7418043e6af681a3676f0b) | `papers/inference/99-other-inference-systems/2026-2608.23296-sigmoid-attention-as-a-better-substrate-for-learned-kv-cache-eviction.md` |
| 109 | 0 | research | arXiv:2608.25053 | Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels | [primary](https://www.semanticscholar.org/paper/61247ec0864a2c3fc0b9cbe68fb6e1495961a02b) | `papers/inference/99-other-inference-systems/2026-2608.25053-hydra-phase-aware-workload-characterization-of-llm-inference-across-edge-soc-generations-backends-and-quantization-level.md` |
| 110 | 0 | research | arXiv:2608.28911 | SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference | [primary](https://www.semanticscholar.org/paper/d3f7b7e4211810aede1fbf47e1b342071445dacb) | `papers/inference/99-other-inference-systems/2026-2608.28911-semkv-semantic-mixed-precision-kv-cache-quantization-guided-by-the-quality-cliff-for-long-context-llm-inference.md` |
| 111 | 0 | research | arXiv:2609.02652 | Unfolding the Leech Lattice: Fused Multi-Shell Decoding and VRAM Layouts for 2-Bit LLM Weights | [primary](https://www.semanticscholar.org/paper/e367265fbfc519f2fe477b741f7b2d57372c3783) | `papers/inference/99-other-inference-systems/2026-2609.02652-unfolding-the-leech-lattice-fused-multi-shell-decoding-and-vram-layouts-for-2-bit-llm-weights.md` |
| 112 | 0 | research | arXiv:2609.06128 | Substrate-Portable Execution for Production LLM Workflows | [primary](https://arxiv.org/abs/2609.06128) | `papers/inference/99-other-inference-systems/2026-2609.06128-substrate-portable-production-llm-workflows.md` |
| 113 | 0 | research | arXiv:2609.07786 | Signed Rescue Routing: Harm-Aware Cascades for Efficient LLM Inference | [primary](https://arxiv.org/abs/2609.07786) | `papers/inference/99-other-inference-systems/2026-2609.07786-signed-rescue-routing-harm-aware-cascades-for-efficient-llm-inference.md` |
| 114 | 0 | research | arXiv:2609.08307 | A Measurement Study of LLM Inference Trade-offs Across Edge Continuum Hardware | [primary](https://arxiv.org/abs/2609.08307) | `papers/inference/99-other-inference-systems/2026-2609.08307-a-measurement-study-of-llm-inference-trade-offs-across-edge-continuum-hardware.md` |
| 115 | 0 | research | arXiv:2609.11716 | Why Does Post-Training Quantization Work? | [primary](https://www.semanticscholar.org/paper/92b8bb2aa2e91d22e81ec850e61ced274289eb57) | `papers/inference/99-other-inference-systems/2026-2609.11716-why-does-post-training-quantization-work.md` |
| 116 | 0 | research | arXiv:2609.13486 | Mixture-of-Experts Language Models Can Be Strong and Efficient Retrievers | [primary](https://arxiv.org/abs/2609.13486) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.13486-efficient-moe-retrievers-adaptive-expert-count.md` |
| 117 | 0 | research | arXiv:2609.14850 | Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference | [primary](https://arxiv.org/abs/2609.14850) | `papers/inference/99-other-inference-systems/2026-2609.14850-self-orchestrating-language-models.md` |
| 118 | 0 | research | arXiv:2609.16503 | Dense to MoE Adaptation for Compact Vision Language Action Policies | [primary](https://arxiv.org/abs/2609.16503) | `papers/inference/02-adaptive-expert-computation-compression/2026-2609.16503-adade-dynamic-expert-deactivation.md` |
| 119 | 0 | research | arXiv:2609.21450 | Understanding LLM Quantization through Activation-Guided Compensation and Orthogonal Residuals | [primary](https://www.semanticscholar.org/paper/4bc350d63aeade610b2ffccc236935ac34647a3d) | `papers/inference/99-other-inference-systems/2026-2609.21450-understanding-llm-quantization-through-activation-guided-compensation-and-orthogonal-residuals.md` |
| 120 | 0 | research | arXiv:2609.22158 | StepKV: Step-Aware KV Cache Compression for LLM Agents | [primary](https://arxiv.org/abs/2609.22158) | `papers/inference/99-other-inference-systems/2026-2609.22158-stepkv-step-aware-kv-cache-compression-for-llm-agents.md` |
| 121 | 0 | research | arXiv:2609.25916 | Beyond Scalar Sensitivity: Activation-Aware Mixed-Precision LLM Quantization with Cross-Layer Refinement | [primary](https://www.semanticscholar.org/paper/21bd7e3b09e4e1b7a72197bcca5e270539335449) | `papers/inference/99-other-inference-systems/2026-2609.25916-beyond-scalar-sensitivity-activation-aware-mixed-precision-llm-quantization-with-cross-layer-refinement.md` |
| 122 | 0 | research | arXiv:2609.33184 | Resource-Efficient Speculative Decoding for Long-Context LLM Serving | [primary](https://arxiv.org/abs/2609.33184) | `papers/inference/99-other-inference-systems/2026-2609.33184-resource-efficient-speculative-decoding-for-long-context-llm-serving.md` |
| 123 | 0 | research | DOI:10.1016/j.knosys.2026.116244 | RS-MoE: Coupled expert compression via activation-peak guided collaborative decomposition | [primary](https://doi.org/10.1016/j.knosys.2026.116244) | `papers/inference/02-adaptive-expert-computation-compression/2026-rs-moe-coupled-expert-compression.md` |
| 124 | 0 | research | DOI:10.1016/j.parco.2026.103216 | SmartBatchLLM: An efficient adaptive hybrid batching strategy for large language model serving | [primary](https://doi.org/10.1016/j.parco.2026.103216) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-smartbatchllm-adaptive-hybrid-batching.md` |
| 125 | 0 | research | DOI:10.1109/ICAISISAS68969.2026.11567792 | TDMoE: Tail-probability-based Dynamic-k MoE | [primary](https://doi.org/10.1109/ICAISISAS68969.2026.11567792) | `papers/inference/02-adaptive-expert-computation-compression/2026-tdmoe-tail-probability-dynamic-k.md` |
| 126 | 0 | research | DOI:10.1109/ICWS72778.2026.00129 | QueueBreak: A Trace-to-Diagnosis Pipeline for Tail Latency in Agentic LLM Services | [primary](https://www.semanticscholar.org/paper/aa516e10879a6aa96b08ffd635832854788de3a5) | `papers/inference/99-other-inference-systems/2020-2026.00129-queuebreak-a-trace-to-diagnosis-pipeline-for-tail-latency-in-agentic-llm-services.md` |
| 127 | 0 | research | DOI:10.1109/INFOCOM59046.2026.11571388 | CoSine: Enhancing LLM Serving via Collaborative and Decoupled Speculative Inference | [primary](https://www.semanticscholar.org/paper/cfe4e4e23b47ae91c7bcb42dba0236152645918a) | `papers/inference/99-other-inference-systems/2026-34f343c5dcff-cosine-enhancing-llm-serving-via-collaborative-and-decoupled-speculative-inference.md` |
| 128 | 0 | research | DOI:10.1109/isca59077.2024.00082 | LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference | [primary](https://doi.org/10.1109/isca59077.2024.00082) | `papers/inference/99-other-inference-systems/0000-6daecc086891-llmcompass-enabling-efficient-hardware-design-for-large-language-model-inference.md` |
| 129 | 0 | research | DOI:10.1109/JIOT.2026.3709703 | Co-Optimizing Request Scheduling and KV Caching for Edge LLM Serving | [primary](https://www.semanticscholar.org/paper/f25ba2c420a573830f2b4b2f30dd2fcc3adffeb2) | `papers/inference/99-other-inference-systems/2026-de817f8d0333-co-optimizing-request-scheduling-and-kv-caching-for-edge-llm-serving.md` |
| 130 | 0 | research | DOI:10.1109/LCA.2026.3703982 | HBM-HBF-Centric Memory Pooling Architecture With Custom Base Die for Terabyte-Scale LLM Inference | [primary](https://ieeexplore.ieee.org/document/11568525/) | `papers/inference/99-other-inference-systems/2026-a21e1445aad5-hbm-hbf-centric-memory-pooling-architecture-with-custom-base-die-for-terabyte-scale-llm-inference.md` |
| 131 | 0 | research | DOI:10.1109/TCAD.2025.3648674 | DuoPIM: RRAM–DRAM Hybrid PIM Acceleration for Flexible-Batch LLM Decoding | [primary](https://www.semanticscholar.org/paper/bccca75ef45fe933f099b3ff1fd54d7a8077b8c1) | `papers/inference/99-other-inference-systems/2026-930e81a91eca-duopim-rramdram-hybrid-pim-acceleration-for-flexible-batch-llm-decoding.md` |
| 132 | 0 | research | DOI:10.1109/TNET.2024.3355010 | DistMind: Efficient Resource Disaggregation for Deep Learning Workloads | [primary](https://www.semanticscholar.org/paper/1112ac74f9299838c8a354f778fbbfd951dfc50c) | `papers/inference/99-other-inference-systems/2026-d66009615d04-distmind-efficient-resource-disaggregation-for-deep-learning-workloads.md` |
| 133 | 0 | research | DOI:10.1145/3341301.3359646 | PipeDream: generalized pipeline parallelism for DNN training | [primary](https://doi.org/10.1145/3341301.3359646) | `papers/inference/99-other-inference-systems/2026-ad68cc79ebe7-pipedream-generalized-pipeline-parallelism-for-dnn-training.md` |
| 134 | 0 | research | DOI:10.1145/3600006.3613145 | GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints | [primary](https://doi.org/10.1145/3600006.3613145) | `papers/inference/99-other-inference-systems/0000-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-checkpoints.md` |
| 135 | 0 | research | DOI:10.1145/3606557.3606559 | Make It Real: An End-to-End Implementation of A Physically Disaggregated Data Center | [primary](https://doi.org/10.1145/3606557.3606559) | `papers/inference/99-other-inference-systems/0000-47de7e2f8a1f-make-it-real-an-end-to-end-implementation-of-a-physically-disaggregated-data-center.md` |
| 136 | 0 | research | DOI:10.1145/3620666.3651380 | NeuPIMs: NPU-PIM Heterogeneous Acceleration for Batched LLM Inferencing | [primary](https://doi.org/10.1145/3620666.3651380) | `papers/inference/99-other-inference-systems/0000-53abd3a104f5-neupims-npu-pim-heterogeneous-acceleration-for-batched-llm-inferencing.md` |
| 137 | 0 | research | DOI:10.1145/3662006.3662067 | Hybrid SLM and LLM for Edge-Cloud Collaborative Inference | [primary](https://doi.org/10.1145/3662006.3662067) | `papers/inference/99-other-inference-systems/2024-7a6bf47fa469-hybrid-slm-and-llm-for-edge-cloud-collaborative-inference.md` |
| 138 | 0 | research | DOI:10.1145/3690624.3709196 | ResMoE: Space-efficient Compression of Mixture of Experts LLMs via Residual Restoration | [primary](https://doi.org/10.1145/3690624.3709196) | `papers/inference/99-other-inference-systems/0000-097fa558562e-resmoe-space-efficient-compression-of-mixture-of-experts-llms-via-residual-restoration.md` |
| 139 | 0 | research | DOI:10.1145/3725338 | PQCache: Product Quantization-based KVCache for Long Context LLM Inference | [primary](https://doi.org/10.1145/3725338) | `papers/inference/99-other-inference-systems/0000-24362ae4b461-pqcache-product-quantization-based-kvcache-for-long-context-llm-inference.md` |
| 140 | 0 | research | DOI:10.1145/3731569.3764834 | PrefillOnly: An Inference Engine for Prefill-only Workloads in Large Language Model Applications | [primary](https://doi.org/10.1145/3731569.3764834) | `papers/inference/99-other-inference-systems/0000-cc54e0b027f8-prefillonly-an-inference-engine-for-prefill-only-workloads-in-large-language-model-applications.md` |
| 141 | 0 | research | DOI:10.1145/3773772 | Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving | [primary](https://doi.org/10.1145/3773772) | `papers/inference/99-other-inference-systems/0000-aa24341e05f1-mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md` |
| 142 | 0 | research | doi:10.1145/3788106 | Towards Scalable Storage Architectures for GPU Clusters Running Large Language Models | [primary](https://doi.org/10.1145/3788106) | `papers/inference/99-other-inference-systems/2026-80288018997a-towards-scalable-storage-architectures-for-gpu-clusters-running-large-language-models.md` |
| 143 | 0 | research | DOI:10.1145/3789240.3828750 | ARK: Avoiding Routing Collisions for KV Cache Transfer in Disaggregated LLM Inference | [primary](https://www.semanticscholar.org/paper/713681b5ad435a87d94c6eb057a4b06f97a99c22) | `papers/inference/99-other-inference-systems/2026-5d556af29afc-ark-avoiding-routing-collisions-for-kv-cache-transfer-in-disaggregated-llm-inference.md` |
| 144 | 0 | research | DOI:10.1145/3789240.3830285 | POSTER: Prediction-Enhanced Expert Prefetching and Eviction for MoE Offloading via PRED-MoE | [primary](https://doi.org/10.1145/3789240.3830285) | `papers/inference/03-expert-prefetch/2026-pred-moe-prefetch-eviction.md` |
| 145 | 0 | research | DOI:10.1145/3806645.3807596 | Scaling Attention Beyond GPUs for LLM Inference | [primary](https://www.semanticscholar.org/paper/04f3ee7dd762dff9b6aad25bfb930e1984f74a09) | `papers/inference/99-other-inference-systems/2026-c3c79f91845d-scaling-attention-beyond-gpus-for-llm-inference.md` |
| 146 | 0 | research | DOI:10.1145/3830086 | CELLServe: An SLO-Aware and Cost Efficient LLMs Serving System for Serverless Computing Environments | [primary](https://doi.org/10.1145/3830086) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-cellserve-serverless-pd-disaggregation.md` |
| 147 | 0 | research | DOI:10.1145/3832810.3832840 | RPSC: Robust LLM Scheduling by Tolerating Prediction Inaccuracy and Mitigating Tail Latency | [primary](https://www.semanticscholar.org/paper/d6928989c68496141ed1c5c207f742bc9cad96db) | `papers/inference/99-other-inference-systems/2026-a9f776eee2e3-rpsc-robust-llm-scheduling-by-tolerating-prediction-inaccuracy-and-mitigating-tail-latency.md` |
| 148 | 0 | research | DOI:10.1145/3832810.3832866 | AsymFlow: Enabling Long-Context LLM Serving via CPU-GPU Prefill-Decode Disaggregation | [primary](https://www.semanticscholar.org/paper/50318e12c7f8b36202899a69346fd9920a2e73a9) | `papers/inference/99-other-inference-systems/2026-c24278db090c-asymflow-enabling-long-context-llm-serving-via-cpu-gpu-prefill-decode-disaggregation.md` |
| 149 | 0 | research | DOI:10.1145/3838177.3841735 | Congestion-Aware Serving of Agentic LLM Applications | [primary](https://www.semanticscholar.org/paper/adc66da23cd03d90f351c1db39703742f0ec85d9) | `papers/inference/99-other-inference-systems/2026-80e75f6f533b-congestion-aware-serving-of-agentic-llm-applications.md` |
| 150 | 0 | research | DOI:10.18653/v1/2023.emnlp-main.298 | GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints | [primary](https://aclanthology.org/2023.emnlp-main.298/) | `papers/inference/99-other-inference-systems/0000-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-checkpoints.md` |
| 151 | 0 | research | DOI:10.24963/ijcai.2026/657 | DoMoE: Domain-Aware Semantic Expert Prediction for Efficient MoE Inference Under Expert Offloading | [primary](https://doi.org/10.24963/ijcai.2026/657) | `papers/inference/03-expert-prefetch/2026-domoe-domain-aware-semantic-expert-prediction.md` |
| 152 | 0 | research | OpenAlex:W7165293849 | Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale | [primary](https://hdl.handle.net/10919/143438) | `papers/inference/99-other-inference-systems/2026-2f1f58b49e98-disaggregated-llm-serving-with-cxl-shared-memory-kv-cache-at-rack-scale.md` |
| 153 | 0 | research | SemanticScholar:d79a26226393f687ddbc375e32055b40b8ad8d38 | GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism | [primary](https://www.semanticscholar.org/paper/d79a26226393f687ddbc375e32055b40b8ad8d38) | `papers/inference/99-other-inference-systems/2026-e5d747247a09-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **6875** / このworker向け: **500**

| # | score | identity | title | published | venue | citations | 関連数 | 系統候補 | source |
|---:|---:|---|---|---|---|---:|---:|---|---|
| 1 | 0 | arXiv:1107.0740 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1107.0740) |
| 2 | 0 | arXiv:1203.0056 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1203.0056) |
| 3 | 0 | arXiv:1207.0580 |  |  |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/1207.0580) |
| 4 | 0 | arXiv:1211.5590 |  |  |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1211.5590) |
| 5 | 0 | arXiv:1301.3781 |  |  |  |  | 1 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1301.3781) |
| 6 | 0 | arXiv:1311.2540 |  |  |  |  | 3 | KV Cache Optimization / Compression, KV cache quantization / entropy coding / long-context serving / attention kernel co-design | [source](https://arxiv.org/abs/1311.2540) |
| 7 | 0 | arXiv:1312.6211 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1312.6211) |
| 8 | 0 | arXiv:1405.3866 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1405.3866) |
| 9 | 0 | arXiv:1407.3561 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1407.3561) |
| 10 | 0 | arXiv:1410.0759 |  |  |  |  | 3 | GPUカーネル自動最適化、LLMエージェント、ハードウェアプロファイル、CUDAコンパイル・実行ツールチェーン, inference-systems | [source](https://arxiv.org/abs/1410.0759) |
| 11 | 0 | arXiv:1412.6115 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1412.6115) |
| 12 | 0 | arXiv:1412.7024 |  |  |  |  | 3 | Weight Quantization / Compression, llama.cpp・WebGPU・ブラウザ内オンデバイス推論・量子化カーネル | [source](https://arxiv.org/abs/1412.7024) |
| 13 | 0 | arXiv:1504.00325 |  |  |  |  | 1 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1504.00325) |
| 14 | 0 | arXiv:1506.02438 |  |  |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/1506.02438) |
| 15 | 0 | arXiv:1506.06726 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1506.06726) |
| 16 | 0 | arXiv:1508.03619 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1508.03619) |
| 17 | 0 | arXiv:1511.05641 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1511.05641) |
| 18 | 0 | arXiv:1511.06297 |  |  |  |  | 6 | Conditional Computation, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, inference-systems | [source](https://arxiv.org/abs/1511.06297) |
| 19 | 0 | arXiv:1511.06939 |  |  |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1511.06939) |
| 20 | 0 | arXiv:1512.02595 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1512.02595) |
| 21 | 0 | arXiv:1601.06733 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1601.06733) |
| 22 | 0 | arXiv:1602.02068 |  |  |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/1602.02068) |
| 23 | 0 | arXiv:1602.07360 |  |  |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1602.07360) |
| 24 | 0 | arXiv:1603.05027 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1603.05027) |
| 25 | 0 | arXiv:1603.07396 |  |  |  |  | 1 | adaptive expert computation / null experts / data sparsity / multimodal MoE | [source](https://arxiv.org/abs/1603.07396) |
| 26 | 0 | arXiv:1605.08695 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1605.08695) |
| 27 | 0 | arXiv:1606.06160 |  |  |  |  | 3 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.06160) |
| 28 | 0 | arXiv:1607.08022 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1607.08022) |
| 29 | 0 | arXiv:1609.00076 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1609.00076) |
| 30 | 0 | arXiv:1610.02136 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1610.02136) |
| 31 | 0 | arXiv:1611.01576 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1611.01576) |
| 32 | 0 | arXiv:1611.01704 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1611.01704) |
| 33 | 0 | arXiv:1612.07837 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1612.07837) |
| 34 | 0 | arXiv:1701.05517 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1701.05517) |
| 35 | 0 | arXiv:1702.04008 |  |  |  |  | 1 | unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1702.04008) |
| 36 | 0 | arXiv:1703.04247 |  |  |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/1703.04247) |
| 37 | 0 | arXiv:1704.04368 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1704.04368) |
| 38 | 0 | arXiv:1704.04861 |  |  |  |  | 3 | KV Cache Optimization / Compression, inference-systems, on-device LLM inference / mobile inference / Flash offload | [source](https://arxiv.org/abs/1704.04861) |
| 39 | 0 | arXiv:1705.03122 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1705.03122) |
| 40 | 0 | arXiv:1706.00885 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1706.00885) |
| 41 | 0 | arXiv:1707.08052 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1707.08052) |
| 42 | 0 | arXiv:1709.01686 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1709.01686) |
| 43 | 0 | arXiv:1710.01878 |  |  |  |  | 3 | MoE compression / task-agnostic expert pruning / expert merging / representation similarity | [source](https://arxiv.org/abs/1710.01878) |
| 44 | 0 | arXiv:1710.10903 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1710.10903) |
| 45 | 0 | arXiv:1711.09224 |  |  |  |  | 3 | 02-hardware-accelerators, unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1711.09224) |
| 46 | 0 | arXiv:1712.01887 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1712.01887) |
| 47 | 0 | arXiv:1712.09763 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1712.09763) |
| 48 | 0 | arXiv:1802.05365 |  |  |  |  | 1 | Training Offload / Memory Systems | [source](https://arxiv.org/abs/1802.05365) |
| 49 | 0 | arXiv:1802.06901 |  |  |  |  | 3 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, inference-systems | [source](https://arxiv.org/abs/1802.06901) |
| 50 | 0 | arXiv:1803.00567 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1803.00567) |
| 51 | 0 | arXiv:1803.07416 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1803.07416) |
| 52 | 0 | arXiv:1804.04849 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1804.04849) |
| 53 | 0 | arXiv:1804.06087 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1804.06087) |
| 54 | 0 | arXiv:1805.04623 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1805.04623) |
| 55 | 0 | arXiv:1805.06407 |  |  |  |  | 1 | CPU推論、行列拡張、異種実行、ルーフライン最適化 | [source](https://arxiv.org/abs/1805.06407) |
| 56 | 0 | arXiv:1806.02847 |  |  |  |  | 2 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.02847) |
| 57 | 0 | arXiv:1806.09055 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1806.09055) |
| 58 | 0 | arXiv:1807.11143 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1807.11143) |
| 59 | 0 | arXiv:1808.06866 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1808.06866) |
| 60 | 0 | arXiv:1808.09121 |  |  |  |  | 1 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling | [source](https://arxiv.org/abs/1808.09121) |
| 61 | 0 | arXiv:1809.00732 |  |  |  |  | 1 | 位置非依存キャッシュ / PagedAttention / 階層KVキャッシュ | [source](https://arxiv.org/abs/1809.00732) |
| 62 | 0 | arXiv:1809.09600 |  |  |  |  | 13 | KV cache offloading / hierarchical storage / lossy KV compression, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, inference-systems, survey-moe-inference-optimization, 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/1809.09600) |
| 63 | 0 | arXiv:1810.00602 |  |  |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/1810.00602) |
| 64 | 0 | arXiv:1810.03292 |  |  |  |  | 1 | MoE expert pruning / causal interpretability / expert importance metrics | [source](https://arxiv.org/abs/1810.03292) |
| 65 | 0 | arXiv:1810.09868 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1810.09868) |
| 66 | 0 | arXiv:1811.00937 |  |  |  |  | 5 | Adaptive Expert Computation / Compression, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1811.00937) |
| 67 | 0 | arXiv:1811.03115 |  |  |  |  | 2 | inference-systems, 投機的デコード / 分布保存型デコード高速化 | [source](https://arxiv.org/abs/1811.03115) |
| 68 | 0 | arXiv:1811.08886 |  |  |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/1811.08886) |
| 69 | 0 | arXiv:1812.06162 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1812.06162) |
| 70 | 0 | arXiv:1901.04085 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1901.04085) |
| 71 | 0 | arXiv:1902.00732 |  |  |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1902.00732) |
| 72 | 0 | arXiv:1902.04610 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1902.04610) |
| 73 | 0 | arXiv:1902.08295 |  |  |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1902.08295) |
| 74 | 0 | arXiv:1902.09574 |  |  |  |  | 4 | inference-systems, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware | [source](https://arxiv.org/abs/1902.09574) |
| 75 | 0 | arXiv:1903.01611 |  |  |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/1903.01611) |
| 76 | 0 | arXiv:1903.05566 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1903.05566) |
| 77 | 0 | arXiv:1904.00962 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1904.00962) |
| 78 | 0 | arXiv:1904.03711 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1904.03711) |
| 79 | 0 | arXiv:1904.09223 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1904.09223) |
| 80 | 0 | arXiv:1904.09679 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1904.09679) |
| 81 | 0 | arXiv:1905.03243 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1905.03243) |
| 82 | 0 | arXiv:1905.06566 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/1905.06566) |
| 83 | 0 | arXiv:1905.08836 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1905.08836) |
| 84 | 0 | arXiv:1905.13678 |  |  |  |  | 1 | unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/1905.13678) |
| 85 | 0 | arXiv:1906.00532 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1906.00532) |
| 86 | 0 | arXiv:1906.03741 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1906.03741) |
| 87 | 0 | arXiv:1906.04341 |  |  |  |  | 2 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/1906.04341) |
| 88 | 0 | arXiv:1906.07155 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1906.07155) |
| 89 | 0 | arXiv:1906.10771 |  |  |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1906.10771) |
| 90 | 0 | arXiv:1907.01989 |  |  |  |  | 1 | モバイル異種推論、DAGスケジューリング、CPU-GPU協調実行 | [source](https://arxiv.org/abs/1907.01989) |
| 91 | 0 | arXiv:1907.04840 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1907.04840) |
| 92 | 0 | arXiv:1907.12009 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1907.12009) |
| 93 | 0 | arXiv:1908.06189 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1908.06189) |
| 94 | 0 | arXiv:1908.08345 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1908.08345) |
| 95 | 0 | arXiv:1908.09378 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1908.09378) |
| 96 | 0 | arXiv:1908.11365 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1908.11365) |
| 97 | 0 | arXiv:1909.01315 |  |  |  |  | 2 | sparse attention / KV-cache bandwidth reduction | [source](https://arxiv.org/abs/1909.01315) |
| 98 | 0 | arXiv:1909.03368 |  |  |  |  | 1 | LLMサービング／予測型スケジューリング | [source](https://arxiv.org/abs/1909.03368) |
| 99 | 0 | arXiv:1909.08593 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1909.08593) |
| 100 | 0 | arXiv:1909.11556 |  |  |  |  | 5 | inference-systems, speculative decoding / LLM serving / adaptive scheduling | [source](https://arxiv.org/abs/1909.11556) |
| 101 | 0 | arXiv:1910.01108 |  |  |  |  | 17 | LLM Serving / Scheduling / Disaggregation, LLMサービング／予測型スケジューリング, Speculative Decoding, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, speculative decoding / heterogeneous CPU-GPU inference / consumer hardware, 投機的デコード / 分布保存型デコード高速化, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/1910.01108) |
| 102 | 0 | arXiv:1910.04915 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1910.04915) |
| 103 | 0 | arXiv:1910.06360 |  |  |  |  | 3 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1910.06360) |
| 104 | 0 | arXiv:1910.09455 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1910.09455) |
| 105 | 0 | arXiv:1911.00172 |  |  |  |  | 3 |  | [source](https://arxiv.org/abs/1911.00172) |
| 106 | 0 | arXiv:1911.02727 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1911.02727) |
| 107 | 0 | arXiv:1911.03631 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.03631) |
| 108 | 0 | arXiv:1911.03918 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.03918) |
| 109 | 0 | arXiv:1911.07176 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.07176) |
| 110 | 0 | arXiv:1911.11313 |  |  |  |  | 2 | inference-systems, 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1911.11313) |
| 111 | 0 | arXiv:1912.01703 |  |  |  |  | 14 | 05-speculative-decoding-moe, 13-sparse-attention, GPU Kernel Framework, GPUカーネル融合／SwiGLU／LLM推論ランタイム, Offload / Hierarchical Memory, inference-systems, その他システム研究, オフロード／階層メモリ | [source](https://arxiv.org/abs/1912.01703) |
| 112 | 0 | arXiv:1912.12180 |  |  |  |  | 2 | training-memory-systems, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/1912.12180) |
| 113 | 0 | arXiv:2001.04063 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2001.04063) |
| 114 | 0 | arXiv:2001.06838 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2001.06838) |
| 115 | 0 | arXiv:2002.03932 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.03932) |
| 116 | 0 | arXiv:2002.07650 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.07650) |
| 117 | 0 | arXiv:2002.08307 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2002.08307) |
| 118 | 0 | arXiv:2002.09919 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.09919) |
| 119 | 0 | arXiv:2002.10957 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.10957) |
| 120 | 0 | arXiv:2002.12410 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2002.12410) |
| 121 | 0 | arXiv:2003.04807 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2003.04807) |
| 122 | 0 | arXiv:2003.08295 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.08295) |
| 123 | 0 | arXiv:2003.12462 |  |  |  |  | 1 | マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2003.12462) |
| 124 | 0 | arXiv:2004.03329 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2004.03329) |
| 125 | 0 | arXiv:2004.06190 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2004.06190) |
| 126 | 0 | arXiv:2004.08994 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2004.08994) |
| 127 | 0 | arXiv:2004.11886 |  |  |  |  | 2 | Speculative Decoding, inference-systems | [source](https://arxiv.org/abs/2004.11886) |
| 128 | 0 | arXiv:2005.00247 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2005.00247) |
| 129 | 0 | arXiv:2005.00928 |  |  |  |  | 1 | 拡散LLM推論 / 近似KVキャッシュ / 細粒度トークン更新 / 復号順序制御 | [source](https://arxiv.org/abs/2005.00928) |
| 130 | 0 | arXiv:2005.06537 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2005.06537) |
| 131 | 0 | arXiv:2005.08100 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2005.08100) |
| 132 | 0 | arXiv:2006.00996 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2006.00996) |
| 133 | 0 | arXiv:2006.06478 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2006.06478) |
| 134 | 0 | arXiv:2006.10518 |  |  |  |  | 1 | post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2006.10518) |
| 135 | 0 | arXiv:2006.11527 |  |  |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2006.11527) |
| 136 | 0 | arXiv:2006.16669 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2006.16669) |
| 137 | 0 | arXiv:2007.03152 |  |  |  |  | 1 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計 | [source](https://arxiv.org/abs/2007.03152) |
| 138 | 0 | arXiv:2007.07779 |  |  |  |  | 1 | many-adapter LLM serving / LoRA serving / inference scheduling | [source](https://arxiv.org/abs/2007.07779) |
| 139 | 0 | arXiv:2007.12673 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2007.12673) |
| 140 | 0 | arXiv:2008.00623 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2008.00623) |
| 141 | 0 | arXiv:2009.05230 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2009.05230) |
| 142 | 0 | arXiv:2009.06106 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2009.06106) |
| 143 | 0 | arXiv:2009.07177 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2009.07177) |
| 144 | 0 | arXiv:2009.07453 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2009.07453) |
| 145 | 0 | arXiv:2009.08553 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2009.08553) |
| 146 | 0 | arXiv:2009.12836 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2009.12836) |
| 147 | 0 | arXiv:2010.00710 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2010.00710) |
| 148 | 0 | arXiv:2010.02523 |  |  |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2010.02523) |
| 149 | 0 | arXiv:2010.03379 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03379) |
| 150 | 0 | arXiv:2010.03983 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2010.03983) |
| 151 | 0 | arXiv:2010.07003 |  |  |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2010.07003) |
| 152 | 0 | arXiv:2010.11443 |  |  |  |  | 1 | agentic LLM serving / KV-cache retention and offload / tool-call scheduling / progress-aware systems | [source](https://arxiv.org/abs/2010.11443) |
| 153 | 0 | arXiv:2010.15327 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2010.15327) |
| 154 | 0 | arXiv:2011.01060 |  |  |  |  | 2 | kv-cache-offload-recomputation, multi-agent LLM serving / cross-stage KV reuse / sparse KV rectification | [source](https://arxiv.org/abs/2011.01060) |
| 155 | 0 | arXiv:2011.04393 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2011.04393) |
| 156 | 0 | arXiv:2011.06997 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2011.06997) |
| 157 | 0 | arXiv:2011.14203 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2011.14203) |
| 158 | 0 | arXiv:2012.11346 |  |  |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2012.11346) |
| 159 | 0 | arXiv:2012.15688 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2012.15688) |
| 160 | 0 | arXiv:2012.15833 |  |  |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2012.15833) |
| 161 | 0 | arXiv:2101.00408 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2101.00408) |
| 162 | 0 | arXiv:2101.09671 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2101.09671) |
| 163 | 0 | arXiv:2102.01672 |  |  |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2102.01672) |
| 164 | 0 | arXiv:2102.04803 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2102.04803) |
| 165 | 0 | arXiv:2102.07835 |  |  |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2102.07835) |
| 166 | 0 | arXiv:2102.08942 |  |  |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/2102.08942) |
| 167 | 0 | arXiv:2102.12122 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2102.12122) |
| 168 | 0 | arXiv:2103.03330 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2103.03330) |
| 169 | 0 | arXiv:2103.07191 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2103.07191) |
| 170 | 0 | arXiv:2103.13076 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2103.13076) |
| 171 | 0 | arXiv:2104.06599 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2104.06599) |
| 172 | 0 | arXiv:2104.07358 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2104.07358) |
| 173 | 0 | arXiv:2104.08691 |  |  |  |  | 12 | 02-adaptive-expert-computation-compression, Conditional Computation, LLM Serving / Scheduling / Disaggregation, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, many-adapter LLM serving / LoRA serving / inference scheduling, survey-long-context-serving, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2104.08691) |
| 174 | 0 | arXiv:2104.13478 |  |  |  |  | 1 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection | [source](https://arxiv.org/abs/2104.13478) |
| 175 | 0 | arXiv:2105.05944 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2105.05944) |
| 176 | 0 | arXiv:2105.08928 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2105.08928) |
| 177 | 0 | arXiv:2105.11618 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2105.11618) |
| 178 | 0 | arXiv:2105.13880 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2105.13880) |
| 179 | 0 | arXiv:2105.14940 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2105.14940) |
| 180 | 0 | arXiv:2106.03764 |  |  |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2106.03764) |
| 181 | 0 | arXiv:2106.04972 |  |  |  |  | 1 | multi-tier LLM serving / task offloading / model cascading / edge-cloud collaboration | [source](https://arxiv.org/abs/2106.04972) |
| 182 | 0 | arXiv:2106.07139 |  |  |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2106.07139) |
| 183 | 0 | arXiv:2106.08823 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2106.08823) |
| 184 | 0 | arXiv:2106.15772 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2106.15772) |
| 185 | 0 | arXiv:2107.00910 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.00910) |
| 186 | 0 | arXiv:2107.05407 |  |  |  |  | 1 | 99-other-inference-systems | [source](https://arxiv.org/abs/2107.05407) |
| 187 | 0 | arXiv:2107.09200 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.09200) |
| 188 | 0 | arXiv:2107.13686 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2107.13686) |
| 189 | 0 | arXiv:2108.05036 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2108.05036) |
| 190 | 0 | arXiv:2108.12409 |  |  |  |  | 9 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, LLM inference surveys、roofline performance analysis, cpu-offload, inference-systems, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2108.12409) |
| 191 | 0 | arXiv:2109.02008 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2109.02008) |
| 192 | 0 | arXiv:2109.04838 |  |  |  |  | 3 |  | [source](https://arxiv.org/abs/2109.04838) |
| 193 | 0 | arXiv:2109.06243 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2109.06243) |
| 194 | 0 | arXiv:2109.09115 |  |  |  |  | 2 | KVキャッシュ再利用／圧縮／ネットワーク転送, inference-systems | [source](https://arxiv.org/abs/2109.09115) |
| 195 | 0 | arXiv:2109.11295 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2109.11295) |
| 196 | 0 | arXiv:2110.02037 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2110.02037) |
| 197 | 0 | arXiv:2110.04366 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.04366) |
| 198 | 0 | arXiv:2110.07431 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2110.07431) |
| 199 | 0 | arXiv:2110.08387 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2110.08387) |
| 200 | 0 | arXiv:2110.09132 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.09132) |
| 201 | 0 | arXiv:2110.13283 |  |  |  |  | 1 | llm-serving-systems | [source](https://arxiv.org/abs/2110.13283) |
| 202 | 0 | arXiv:2111.00160 |  |  |  |  | 2 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2111.00160) |
| 203 | 0 | arXiv:2111.00856 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2111.00856) |
| 204 | 0 | arXiv:2111.05754 |  |  |  |  | 3 |  | [source](https://arxiv.org/abs/2111.05754) |
| 205 | 0 | arXiv:2111.09883 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2111.09883) |
| 206 | 0 | arXiv:2112.00861 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.00861) |
| 207 | 0 | arXiv:2112.02624 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.02624) |
| 208 | 0 | arXiv:2112.06598 |  |  |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2112.06598) |
| 209 | 0 | arXiv:2112.07916 |  |  |  |  | 2 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2112.07916) |
| 210 | 0 | arXiv:2112.10769 |  |  |  |  | 1 | kv-cache-memory | [source](https://arxiv.org/abs/2112.10769) |
| 211 | 0 | arXiv:2112.12731 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.12731) |
| 212 | 0 | arXiv:2201.03533 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2201.03533) |
| 213 | 0 | arXiv:2201.07207 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2201.07207) |
| 214 | 0 | arXiv:2201.11903 |  |  |  |  | 14 | 13-sparse-attention, Adaptive Expert Computation / Compression, Conditional Computation, KV cache eviction / heavy hitters / sparse attention / efficient inference, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, Offload / Hierarchical Memory, Speculative Decoding / Parallel Inference Systems, speculative decoding / edge-assisted serving / distributed inference / pipeline scheduling | [source](https://arxiv.org/abs/2201.11903) |
| 215 | 0 | arXiv:2202.02643 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2202.02643) |
| 216 | 0 | arXiv:2202.05262 |  |  |  |  | 1 | dense-to-MoE conversion / conditional FFN computation / expert routing | [source](https://arxiv.org/abs/2202.05262) |
| 217 | 0 | arXiv:2202.07654 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2202.07654) |
| 218 | 0 | arXiv:2202.08791 |  |  |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2202.08791) |
| 219 | 0 | arXiv:2202.12015 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2202.12015) |
| 220 | 0 | arXiv:2203.00386 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2203.00386) |
| 221 | 0 | arXiv:2203.03131 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2203.03131) |
| 222 | 0 | arXiv:2203.05740 |  |  |  |  | 2 | inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2203.05740) |
| 223 | 0 | arXiv:2203.06850 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2203.06850) |
| 224 | 0 | arXiv:2203.09040 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2203.09040) |
| 225 | 0 | arXiv:2203.11014 |  |  |  |  | 1 | 適応的エキスパート計算・圧縮、エキスパート統合、推薦向け混合エキスパート | [source](https://arxiv.org/abs/2203.11014) |
| 226 | 0 | arXiv:2203.17189 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.17189) |
| 227 | 0 | arXiv:2204.01691 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2204.01691) |
| 228 | 0 | arXiv:2204.03458 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2204.03458) |
| 229 | 0 | arXiv:2204.06125 |  |  |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2204.06125) |
| 230 | 0 | arXiv:2204.07689 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.07689) |
| 231 | 0 | arXiv:2204.09656 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2204.09656) |
| 232 | 0 | arXiv:2205.00445 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.00445) |
| 233 | 0 | arXiv:2205.04713 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2205.04713) |
| 234 | 0 | arXiv:2205.05243 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2205.05243) |
| 235 | 0 | arXiv:2205.07523 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.07523) |
| 236 | 0 | arXiv:2205.10625 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2205.10625) |
| 237 | 0 | arXiv:2205.11913 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.11913) |
| 238 | 0 | arXiv:2205.12411 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12411) |
| 239 | 0 | arXiv:2205.13603 |  |  |  |  | 1 | kernel-runtime-compilation | [source](https://arxiv.org/abs/2205.13603) |
| 240 | 0 | arXiv:2206.01859 |  |  |  |  | 2 | inference-systems, post-training quantization / second-order compression / weight-only LLM inference | [source](https://arxiv.org/abs/2206.01859) |
| 241 | 0 | arXiv:2206.08474 |  |  |  |  | 1 | adaptive expert computation / expert pruning / depth-aware MoE compression | [source](https://arxiv.org/abs/2206.08474) |
| 242 | 0 | arXiv:2206.11349 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2206.11349) |
| 243 | 0 | arXiv:2207.00220 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2207.00220) |
| 244 | 0 | arXiv:2207.06881 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2207.06881) |
| 245 | 0 | arXiv:2207.10551 |  |  |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2207.10551) |
| 246 | 0 | arXiv:2208.02025 |  |  |  |  | 1 | LLM推論カーネル融合／メガカーネル／GPUコンパイラ・ランタイム | [source](https://arxiv.org/abs/2208.02025) |
| 247 | 0 | arXiv:2208.03306 |  |  |  |  | 4 | adaptive expert computation / learning-free MoE compression / expert pruning and merging / topological selection, adaptive-expert-computation-compression, mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2208.03306) |
| 248 | 0 | arXiv:2208.05592 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2208.05592) |
| 249 | 0 | arXiv:2208.08227 |  |  |  |  | 1 | adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2208.08227) |
| 250 | 0 | arXiv:2208.10442 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2208.10442) |
| 251 | 0 | arXiv:2208.11945 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2208.11945) |
| 252 | 0 | arXiv:2209.07738 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2209.07738) |
| 253 | 0 | arXiv:2209.10505 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2209.10505) |
| 254 | 0 | arXiv:2209.11895 |  |  |  |  | 8 | KV Cache Optimization / Compression, KV cache sparsity / paged attention / query-aware selection / LLM serving, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Long-context serving / KV cache benchmark, 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/2209.11895) |
| 255 | 0 | arXiv:2209.13258 |  |  |  |  | 3 | llm-serving-scheduling-disaggregation, モデルカスケード / 複数LLMサービング / 経路・配置共同最適化 / SLO対応スケジューリング | [source](https://arxiv.org/abs/2209.13258) |
| 256 | 0 | arXiv:2209.15189 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2209.15189) |
| 257 | 0 | arXiv:2210.02303 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.02303) |
| 258 | 0 | arXiv:2210.02747 |  |  |  |  | 1 | LLM serving / execution-state reuse / KV cache / CUDA graph runtime / on-device inference | [source](https://arxiv.org/abs/2210.02747) |
| 259 | 0 | arXiv:2210.03057 |  |  |  |  | 3 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2210.03057) |
| 260 | 0 | arXiv:2210.05144 |  |  |  |  | 2 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2210.05144) |
| 261 | 0 | arXiv:2210.06726 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2210.06726) |
| 262 | 0 | arXiv:2210.07535 |  |  |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.07535) |
| 263 | 0 | arXiv:2210.08726 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.08726) |
| 264 | 0 | arXiv:2210.11416 |  |  |  |  | 9 | 99-other-inference-systems, Adaptive Expert Computation / Compression, LLM routing、hybrid inference、quality-aware model selection, inference-systems, 投機的復号・オンライン適応・知識蒸留, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2210.11416) |
| 265 | 0 | arXiv:2210.11948 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.11948) |
| 266 | 0 | arXiv:2210.14102 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2210.14102) |
| 267 | 0 | arXiv:2210.15373 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.15373) |
| 268 | 0 | arXiv:2211.00593 |  |  |  |  | 2 | reasoning-model compression / post-training pruning / calibration-data selection / causal intervention | [source](https://arxiv.org/abs/2211.00593) |
| 269 | 0 | arXiv:2211.01267 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.01267) |
| 270 | 0 | arXiv:2211.05719 |  |  |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2211.05719) |
| 271 | 0 | arXiv:2211.07349 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.07349) |
| 272 | 0 | arXiv:2211.08411 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2211.08411) |
| 273 | 0 | arXiv:2211.11586 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2211.11586) |
| 274 | 0 | arXiv:2211.15089 |  |  |  |  | 2 | diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion | [source](https://arxiv.org/abs/2211.15089) |
| 275 | 0 | arXiv:2212.00768 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2212.00768) |
| 276 | 0 | arXiv:2212.02855 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2212.02855) |
| 277 | 0 | arXiv:2212.04088 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.04088) |
| 278 | 0 | arXiv:2212.05238 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2212.05238) |
| 279 | 0 | arXiv:2212.06817 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2212.06817) |
| 280 | 0 | arXiv:2212.08410 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2212.08410) |
| 281 | 0 | arXiv:2212.10445 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2212.10445) |
| 282 | 0 | arXiv:2212.10544 |  |  |  |  | 1 | training-memory-systems | [source](https://arxiv.org/abs/2212.10544) |
| 283 | 0 | arXiv:2212.10650 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2212.10650) |
| 284 | 0 | arXiv:2212.12017 |  |  |  |  | 2 | 99-other-inference-systems, Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2212.12017) |
| 285 | 0 | arXiv:2301.00407 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2301.00407) |
| 286 | 0 | arXiv:2301.03598 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.03598) |
| 287 | 0 | arXiv:2301.05605 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.05605) |
| 288 | 0 | arXiv:2301.07069 |  |  |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2301.07069) |
| 289 | 0 | arXiv:2301.08984 |  |  |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, inference-systems | [source](https://arxiv.org/abs/2301.08984) |
| 290 | 0 | arXiv:2301.11235 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2301.11235) |
| 291 | 0 | arXiv:2301.12444 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.12444) |
| 292 | 0 | arXiv:2301.13688 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.13688) |
| 293 | 0 | arXiv:2302.02451 |  |  |  |  | 3 | KV cache eviction / heavy hitters / sparse attention / efficient inference, inference-systems | [source](https://arxiv.org/abs/2302.02451) |
| 294 | 0 | arXiv:2302.03770 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.03770) |
| 295 | 0 | arXiv:2302.04863 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.04863) |
| 296 | 0 | arXiv:2302.06590 |  |  |  |  | 1 | agentic serving workload characterization / KV-cache / inference benchmarking | [source](https://arxiv.org/abs/2302.06590) |
| 297 | 0 | arXiv:2302.07736 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2302.07736) |
| 298 | 0 | arXiv:2302.09419 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2302.09419) |
| 299 | 0 | arXiv:2302.10025 |  |  |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2302.10025) |
| 300 | 0 | arXiv:2302.11529 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2302.11529) |
| 301 | 0 | arXiv:2302.12128 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.12128) |
| 302 | 0 | arXiv:2302.12510 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2302.12510) |
| 303 | 0 | arXiv:2302.14520 |  |  |  |  | 1 | LLM Serving / Reasoning | [source](https://arxiv.org/abs/2302.14520) |
| 304 | 0 | arXiv:2303.00566 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2303.00566) |
| 305 | 0 | arXiv:2303.02861 |  |  |  |  | 1 | 02-adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2303.02861) |
| 306 | 0 | arXiv:2303.04129 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.04129) |
| 307 | 0 | arXiv:2303.06135 |  |  |  |  | 3 | LLM Serving / Reasoning, fine-grained MoE / expert routing / test-time scaling / inference-time sampling | [source](https://arxiv.org/abs/2303.06135) |
| 308 | 0 | arXiv:2303.06349 |  |  |  |  | 2 | training-memory-systems | [source](https://arxiv.org/abs/2303.06349) |
| 309 | 0 | arXiv:2303.08117 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2303.08117) |
| 310 | 0 | arXiv:2303.10512 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.10512) |
| 311 | 0 | arXiv:2303.11381 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11381) |
| 312 | 0 | arXiv:2303.13003 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2303.13003) |
| 313 | 0 | arXiv:2303.15056 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.15056) |
| 314 | 0 | arXiv:2303.16504 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.16504) |
| 315 | 0 | arXiv:2303.17564 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.17564) |
| 316 | 0 | arXiv:2303.17605 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2303.17605) |
| 317 | 0 | arXiv:2304.01196 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.01196) |
| 318 | 0 | arXiv:2304.01483 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.01483) |
| 319 | 0 | arXiv:2304.02643 |  |  |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2304.02643) |
| 320 | 0 | arXiv:2304.03271 |  |  |  |  | 1 | serving-disaggregation | [source](https://arxiv.org/abs/2304.03271) |
| 321 | 0 | arXiv:2304.04488 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2304.04488) |
| 322 | 0 | arXiv:2304.05128 |  |  |  |  | 2 | training-memory-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2304.05128) |
| 323 | 0 | arXiv:2304.08485 |  |  |  |  | 3 | speculative-decoding, マルチモーダルLLM配信／符号化・入力処理・デコード分離／SLO指向スケジューリング | [source](https://arxiv.org/abs/2304.08485) |
| 324 | 0 | arXiv:2304.09842 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.09842) |
| 325 | 0 | arXiv:2304.13276 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2304.13276) |
| 326 | 0 | arXiv:2304.15010 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2304.15010) |
| 327 | 0 | arXiv:2305.02538 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2305.02538) |
| 328 | 0 | arXiv:2305.05252 |  |  |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2305.05252) |
| 329 | 0 | arXiv:2305.06983 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2305.06983) |
| 330 | 0 | arXiv:2305.07895 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.07895) |
| 331 | 0 | arXiv:2305.10250 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.10250) |
| 332 | 0 | arXiv:2305.11206 |  |  |  |  | 2 | KVキャッシュ最適化／適応圧縮, inference-systems | [source](https://arxiv.org/abs/2305.11206) |
| 333 | 0 | arXiv:2305.13304 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2305.13304) |
| 334 | 0 | arXiv:2305.13803 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2305.13803) |
| 335 | 0 | arXiv:2305.14239 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.14239) |
| 336 | 0 | arXiv:2305.14481 |  |  |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2305.14481) |
| 337 | 0 | arXiv:2305.14705 |  |  |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2305.14705) |
| 338 | 0 | arXiv:2305.14877 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.14877) |
| 339 | 0 | arXiv:2305.15062 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.15062) |
| 340 | 0 | arXiv:2305.15387 |  |  |  |  | 1 | KV cache compression / sparse attention / long-context inference | [source](https://arxiv.org/abs/2305.15387) |
| 341 | 0 | arXiv:2305.16243 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.16243) |
| 342 | 0 | arXiv:2305.16635 |  |  |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2305.16635) |
| 343 | 0 | arXiv:2305.17144 |  |  |  |  | 3 | inference-systems, other-inference-systems | [source](https://arxiv.org/abs/2305.17144) |
| 344 | 0 | arXiv:2305.18201 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.18201) |
| 345 | 0 | arXiv:2305.18466 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.18466) |
| 346 | 0 | arXiv:2305.19414 |  |  |  |  | 1 | MoEエキスパート予測・キャッシュ・プリフェッチ | [source](https://arxiv.org/abs/2305.19414) |
| 347 | 0 | arXiv:2305.19798 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.19798) |
| 348 | 0 | arXiv:2306.00622 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2306.00622) |
| 349 | 0 | arXiv:2306.02003 |  |  |  |  | 2 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2306.02003) |
| 350 | 0 | arXiv:2306.02561 |  |  |  |  | 3 | LLM routing、hybrid inference、quality-aware model selection, inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2306.02561) |
| 351 | 0 | arXiv:2306.03081 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.03081) |
| 352 | 0 | arXiv:2306.04050 |  |  |  |  | 2 | Expert Prefetch, MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2306.04050) |
| 353 | 0 | arXiv:2306.04933 |  |  |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.04933) |
| 354 | 0 | arXiv:2306.05443 |  |  |  |  | 1 | on-device LLM serving / TEE / TrustZone / mobile NPU isolation | [source](https://arxiv.org/abs/2306.05443) |
| 355 | 0 | arXiv:2306.06965 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.06965) |
| 356 | 0 | arXiv:2306.09539 |  |  |  |  | 2 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2306.09539) |
| 357 | 0 | arXiv:2306.11197 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.11197) |
| 358 | 0 | arXiv:2306.12929 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2306.12929) |
| 359 | 0 | arXiv:2306.14565 |  |  |  |  | 1 | adaptive expert computation / dynamic MoE routing / gating uncertainty | [source](https://arxiv.org/abs/2306.14565) |
| 360 | 0 | arXiv:2306.17806 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.17806) |
| 361 | 0 | arXiv:2307.01189 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.01189) |
| 362 | 0 | arXiv:2307.02485 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.02485) |
| 363 | 0 | arXiv:2307.03109 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2307.03109) |
| 364 | 0 | arXiv:2307.04339 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04339) |
| 365 | 0 | arXiv:2307.06281 |  |  |  |  | 2 | 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2307.06281) |
| 366 | 0 | arXiv:2307.07319 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.07319) |
| 367 | 0 | arXiv:2307.07735 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2307.07735) |
| 368 | 0 | arXiv:2307.08191 |  |  |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2307.08191) |
| 369 | 0 | arXiv:2307.09782 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, Quantization × MoE × Offload | [source](https://arxiv.org/abs/2307.09782) |
| 370 | 0 | arXiv:2307.10554 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2307.10554) |
| 371 | 0 | arXiv:2307.12234 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.12234) |
| 372 | 0 | arXiv:2307.12966 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12966) |
| 373 | 0 | arXiv:2307.15043 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.15043) |
| 374 | 0 | arXiv:2308.00352 |  |  |  |  | 11 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, inference-systems, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation, survey-long-context-serving, マルチエージェントKVキャッシュ共有／位置非依存キャッシュ／KVキャッシュ圧縮 | [source](https://arxiv.org/abs/2308.00352) |
| 375 | 0 | arXiv:2308.02151 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.02151) |
| 376 | 0 | arXiv:2308.04035 |  |  |  |  | 1 | LLMエージェント／生涯学習／推論時メモリ／経験再生／推論予算制御 | [source](https://arxiv.org/abs/2308.04035) |
| 377 | 0 | arXiv:2308.06522 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.06522) |
| 378 | 0 | arXiv:2308.07124 |  |  |  |  | 1 | 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2308.07124) |
| 379 | 0 | arXiv:2308.07317 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.07317) |
| 380 | 0 | arXiv:2308.08747 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.08747) |
| 381 | 0 | arXiv:2308.09687 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.09687) |
| 382 | 0 | arXiv:2308.10835 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.10835) |
| 383 | 0 | arXiv:2308.12908 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation, 先行するNPUの単一計算領域DVFSを、部品単位の空間的DVFSへ拡張。ReGateなどの電力遮断とは補完関係。 | [source](https://arxiv.org/abs/2308.12908) |
| 384 | 0 | arXiv:2308.13894 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2308.13894) |
| 385 | 0 | arXiv:2308.15022 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.15022) |
| 386 | 0 | arXiv:2309.01029 |  |  |  |  | 1 | Structured Pruning / Architecture Search | [source](https://arxiv.org/abs/2309.01029) |
| 387 | 0 | arXiv:2309.02784 |  |  |  |  | 3 | LLM inference surveys、roofline performance analysis, Structured Pruning / Architecture Search, inference-systems | [source](https://arxiv.org/abs/2309.02784) |
| 388 | 0 | arXiv:2309.05519 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.05519) |
| 389 | 0 | arXiv:2309.06589 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.06589) |
| 390 | 0 | arXiv:2309.08600 |  |  |  |  | 2 | 17-pim-near-data-acceleration, adaptive-expert-computation-compression | [source](https://arxiv.org/abs/2309.08600) |
| 391 | 0 | arXiv:2309.09400 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2309.09400) |
| 392 | 0 | arXiv:2309.10400 |  |  |  |  | 2 | KV cache quantization / long-context inference / activation compression, KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2309.10400) |
| 393 | 0 | arXiv:2309.11668 |  |  |  |  | 1 | LLM Serving / Reasoning | [source](https://arxiv.org/abs/2309.11668) |
| 394 | 0 | arXiv:2309.13761 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2309.13761) |
| 395 | 0 | arXiv:2309.14393 |  |  |  |  | 3 | LLM serving / energy management / cluster scheduling / dynamic reconfiguration, inference-systems, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2309.14393) |
| 396 | 0 | arXiv:2309.15789 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2309.15789) |
| 397 | 0 | arXiv:2309.17452 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2309.17452) |
| 398 | 0 | arXiv:2310.00746 |  |  |  |  | 2 | Edge／on-device MoE, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2310.00746) |
| 399 | 0 | arXiv:2310.01405 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2310.01405) |
| 400 | 0 | arXiv:2310.01655 |  |  |  |  | 3 | GPU Kernel Framework, KV cache eviction / heavy hitters / sparse attention / efficient inference, KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2310.01655) |
| 401 | 0 | arXiv:2310.03025 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2310.03025) |
| 402 | 0 | arXiv:2310.03589 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.03589) |
| 403 | 0 | arXiv:2310.03744 |  |  |  |  | 3 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.03744) |
| 404 | 0 | arXiv:2310.05204 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.05204) |
| 405 | 0 | arXiv:2310.05424 |  |  |  |  | 3 | speculative decoding / draft-model design, 投機的デコード／動的LLMサービング／GPU空間多重化 | [source](https://arxiv.org/abs/2310.05424) |
| 406 | 0 | arXiv:2310.06116 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.06116) |
| 407 | 0 | arXiv:2310.07147 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.07147) |
| 408 | 0 | arXiv:2310.07820 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.07820) |
| 409 | 0 | arXiv:2310.09949 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.09949) |
| 410 | 0 | arXiv:2310.11454 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.11454) |
| 411 | 0 | arXiv:2310.12670 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.12670) |
| 412 | 0 | arXiv:2310.13650 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2310.13650) |
| 413 | 0 | arXiv:2310.15301 |  |  |  |  | 1 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2310.15301) |
| 414 | 0 | arXiv:2310.18339 |  |  |  |  | 2 | Adaptive Expert Computation / Compression, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.18339) |
| 415 | 0 | arXiv:2310.19852 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2310.19852) |
| 416 | 0 | arXiv:2311.00502 |  |  |  |  | 3 | CPU推論、行列拡張、異種実行、ルーフライン最適化, inference-systems | [source](https://arxiv.org/abs/2311.00502) |
| 417 | 0 | arXiv:2311.02462 |  |  |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2311.02462) |
| 418 | 0 | arXiv:2311.04897 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.04897) |
| 419 | 0 | arXiv:2311.05908 |  |  |  |  | 1 | GPU Kernel Framework | [source](https://arxiv.org/abs/2311.05908) |
| 420 | 0 | arXiv:2311.07574 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.07574) |
| 421 | 0 | arXiv:2311.08377 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2311.08377) |
| 422 | 0 | arXiv:2311.08981 |  |  |  |  | 2 | speculative decoding / context compression / agentic LLM inference, survey-speculative-decoding | [source](https://arxiv.org/abs/2311.08981) |
| 423 | 0 | arXiv:2311.09550 |  |  |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-low-bit-llm | [source](https://arxiv.org/abs/2311.09550) |
| 424 | 0 | arXiv:2311.11501 |  |  |  |  | 2 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復, multi-LoRA serving / multi-agent KV cache sharing / low-rank cache representation | [source](https://arxiv.org/abs/2311.11501) |
| 425 | 0 | arXiv:2311.12785 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2311.12785) |
| 426 | 0 | arXiv:2311.13541 |  |  |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2311.13541) |
| 427 | 0 | arXiv:2311.14652 |  |  |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2311.14652) |
| 428 | 0 | arXiv:2311.17005 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2311.17005) |
| 429 | 0 | arXiv:2311.17541 |  |  |  |  | 2 | agentic serving / workflow-aware scheduling / memory-aware dispatch, other-inference-systems | [source](https://arxiv.org/abs/2311.17541) |
| 430 | 0 | arXiv:2312.00858 |  |  |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2312.00858) |
| 431 | 0 | arXiv:2312.03134 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2312.03134) |
| 432 | 0 | arXiv:2312.03788 |  |  |  |  | 2 | Quantization × MoE × Offload, kernel-runtime-compilation | [source](https://arxiv.org/abs/2312.03788) |
| 433 | 0 | arXiv:2312.04511 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2312.04511) |
| 434 | 0 | arXiv:2312.04985 |  |  |  |  | 16 | KV cache compression / sparse attention / long-context inference, KV cache quantization / long-context inference / activation compression, Offload / Hierarchical Memory, Sparse Attention, inference-systems, kv-cache-optimization-compression, llm-serving-scheduling-disaggregation, sparse attention / KV-cache bandwidth reduction, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置 | [source](https://arxiv.org/abs/2312.04985) |
| 435 | 0 | arXiv:2312.06341 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.06341) |
| 436 | 0 | arXiv:2312.06837 |  |  |  |  | 1 | GPU Kernel Framework | [source](https://arxiv.org/abs/2312.06837) |
| 437 | 0 | arXiv:2312.08618 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.08618) |
| 438 | 0 | arXiv:2312.10244 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2312.10244) |
| 439 | 0 | arXiv:2312.12391 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2312.12391) |
| 440 | 0 | arXiv:2312.14852 |  |  |  |  | 3 | 分散MoE推論 / 専門家配置 / エッジ推論 / 動的専門家移行, 投機的デコード／多トークン予測／強化学習ロールアウト高速化／オンラインドラフトヘッド学習 | [source](https://arxiv.org/abs/2312.14852) |
| 441 | 0 | arXiv:2312.17172 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.17172) |
| 442 | 0 | arXiv:2401.00122 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2401.00122) |
| 443 | 0 | arXiv:2401.00908 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.00908) |
| 444 | 0 | arXiv:2401.02038 |  |  |  |  | 3 | llm-serving-scheduling-disaggregation, survey-distributed-training-systems | [source](https://arxiv.org/abs/2401.02038) |
| 445 | 0 | arXiv:2401.04044 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.04044) |
| 446 | 0 | arXiv:2401.04700 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.04700) |
| 447 | 0 | arXiv:2401.07339 |  |  |  |  | 3 | FPGA LLM acceleration / vector quantization / memory-based computation / heterogeneous inference, inference-systems, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2401.07339) |
| 448 | 0 | arXiv:2401.07886 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2401.07886) |
| 449 | 0 | arXiv:2401.10660 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.10660) |
| 450 | 0 | arXiv:2401.12973 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2401.12973) |
| 451 | 0 | arXiv:2401.13919 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.13919) |
| 452 | 0 | arXiv:2401.14228 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.14228) |
| 453 | 0 | arXiv:2401.15969 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.15969) |
| 454 | 0 | arXiv:2401.18058 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.18058) |
| 455 | 0 | arXiv:2402.00838 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.00838) |
| 456 | 0 | arXiv:2402.01147 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.01147) |
| 457 | 0 | arXiv:2402.01788 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.01788) |
| 458 | 0 | arXiv:2402.02791 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.02791) |
| 459 | 0 | arXiv:2402.03578 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.03578) |
| 460 | 0 | arXiv:2402.04248 |  |  |  |  | 3 | prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2402.04248) |
| 461 | 0 | arXiv:2402.05406 |  |  |  |  | 3 | Adaptive Expert Computation / Compression, inference-systems | [source](https://arxiv.org/abs/2402.05406) |
| 462 | 0 | arXiv:2402.06126 |  |  |  |  | 3 | Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE | [source](https://arxiv.org/abs/2402.06126) |
| 463 | 0 | arXiv:2402.07945 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.07945) |
| 464 | 0 | arXiv:2402.08644 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.08644) |
| 465 | 0 | arXiv:2402.09733 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.09733) |
| 466 | 0 | arXiv:2402.10930 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.10930) |
| 467 | 0 | arXiv:2402.11819 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.11819) |
| 468 | 0 | arXiv:2402.12451 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.12451) |
| 469 | 0 | arXiv:2402.13485 |  |  |  |  | 1 | Speculative Decoding | [source](https://arxiv.org/abs/2402.13485) |
| 470 | 0 | arXiv:2402.14034 |  |  |  |  | 6 | 14-agentic-inference-serving-runtime, LLMサービング・スケジューリング・分離実行, agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling, agentic serving / workflow-aware scheduling / memory-aware dispatch, kv-cache-offload-recomputation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14034) |
| 471 | 0 | arXiv:2402.14808 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation, inference/11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2402.14808) |
| 472 | 0 | arXiv:2402.14905 |  |  |  |  | 4 | 10-kv-cache-offload-recomputation, kv-cache-optimization-compression, offload-hierarchical-memory, モバイルMoE推論・エキスパートオフロード・投機的復号・フラッシュ配置・NPUスケジューリング | [source](https://arxiv.org/abs/2402.14905) |
| 473 | 0 | arXiv:2402.16667 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.16667) |
| 474 | 0 | arXiv:2402.16823 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.16823) |
| 475 | 0 | arXiv:2402.17177 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.17177) |
| 476 | 0 | arXiv:2402.17764 |  |  |  |  | 12 | 08-edge-on-device-llm-systems, Conditional Computation, LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, heterogeneous memory offloading / consumer-device LLM inference / SSD-GPU pipeline, offload-hierarchical-memory, post-training quantization / ternary LLM / packed inference, survey-distributed-training-systems, survey-low-bit-llm, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.17764) |
| 477 | 0 | arXiv:2402.18158 |  |  |  |  | 6 | Quantization × MoE × Offload, Weight Quantization / Compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2402.18158) |
| 478 | 0 | arXiv:2402.18679 |  |  |  |  | 2 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2402.18679) |
| 479 | 0 | arXiv:2402.19427 |  |  |  |  | 7 | 11-llm-serving-scheduling-disaggregation, KV Cache Offload / Recomputation, prefix caching / hybrid attention-SSM serving | [source](https://arxiv.org/abs/2402.19427) |
| 480 | 0 | arXiv:2403.01384 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2403.01384) |
| 481 | 0 | arXiv:2403.02352 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.02352) |
| 482 | 0 | arXiv:2403.03187 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2403.03187) |
| 483 | 0 | arXiv:2403.03514 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.03514) |
| 484 | 0 | arXiv:2403.04706 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2403.04706) |
| 485 | 0 | arXiv:2403.04976 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.04976) |
| 486 | 0 | arXiv:2403.06659 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.06659) |
| 487 | 0 | arXiv:2403.08251 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.08251) |
| 488 | 0 | arXiv:2403.08857 |  |  |  |  | 1 | Sparse Attention / VLM Inference | [source](https://arxiv.org/abs/2403.08857) |
| 489 | 0 | arXiv:2403.10081 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.10081) |
| 490 | 0 | arXiv:2403.10446 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.10446) |
| 491 | 0 | arXiv:2403.12031 |  |  |  |  | 6 | MoE quantization / heterogeneous model-instance routing / quality-aware serving / risk calibration, llm-serving-scheduling-disaggregation, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2403.12031) |
| 492 | 0 | arXiv:2403.12766 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.12766) |
| 493 | 0 | arXiv:2403.14624 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.14624) |
| 494 | 0 | arXiv:2403.16125 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2403.16125) |
| 495 | 0 | arXiv:2403.19135 |  |  |  |  | 1 | MoE専門家オフロード / 混合精度 / 専門家キャッシュ | [source](https://arxiv.org/abs/2403.19135) |
| 496 | 0 | arXiv:2403.20327 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.20327) |
| 497 | 0 | arXiv:2404.02060 |  |  |  |  | 3 | Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2404.02060) |
| 498 | 0 | arXiv:2404.02747 |  |  |  |  | 1 | diffusion language model inference / KV cache / training-free acceleration | [source](https://arxiv.org/abs/2404.02747) |
| 499 | 0 | arXiv:2404.05567 |  |  |  |  | 2 | MoE expert pruning / expert merging / redundancy-aware compression / global budget allocation, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2404.05567) |
| 500 | 0 | arXiv:2404.07647 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2404.07647) |

## Machine-readable

同じ割当は [worker-worklist-45.json](worker-worklist-45.json) にあります。

