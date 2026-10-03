# Scheduled worker :30 worklist

Worker: `scheduled-chat-30`  
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
| 1 | 72 | audit | arXiv:2504.03775 | FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling | [primary](https://arxiv.org/abs/2504.03775) | `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.03775-flowkv-low-latency-transfer-load-aware.md` |
| 2 | 0 | research | arXiv:1802.05799 | Horovod: fast and easy distributed deep learning in TensorFlow | [primary](https://arxiv.org/abs/1802.05799) | `papers/inference/99-other-inference-systems/2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md` |
| 3 | 0 | research | arXiv:1911.02972 | Blockwise Self-Attention for Long Document Understanding | [primary](https://arxiv.org/abs/1911.02972) | `papers/inference/99-other-inference-systems/2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md` |
| 4 | 0 | research | arXiv:2008.12260 | Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning | [primary](https://arxiv.org/abs/2008.12260) | `papers/inference/99-other-inference-systems/2020-2008.12260-pollux-co-adaptive-cluster-scheduling-for-goodput-optimized-deep-learning.md` |
| 5 | 0 | research | arXiv:2010.13887 | LightSeq: A High Performance Inference Library for Sequence Processing and Generation | [primary](https://arxiv.org/abs/2010.13887) | `papers/inference/99-other-inference-systems/2020-2010.13887-lightseq-a-high-performance-inference-library-for-sequence-processing-and-generation.md` |
| 6 | 0 | research | arXiv:2104.04473 | Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM | [primary](https://arxiv.org/abs/2104.04473) | `papers/inference/99-other-inference-systems/2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-megatron-lm.md` |
| 7 | 0 | research | arXiv:2110.03888 | M6-10T: A Sharing-Delinking Paradigm for Efficient Multi-Trillion Parameter Pretraining | [primary](https://arxiv.org/abs/2110.03888) | `papers/inference/99-other-inference-systems/2021-2110.03888-m6-10t-a-sharing-delinking-paradigm-for-efficient-multi-trillion-parameter-pretraining.md` |
| 8 | 0 | research | arXiv:2112.06905 | GLaM: Efficient Scaling of Language Models with Mixture-of-Experts | [primary](https://arxiv.org/abs/2112.06905) | `papers/inference/99-other-inference-systems/2021-2112.06905-glam-efficient-scaling-of-language-models-with-mixture-of-experts.md` |
| 9 | 0 | research | arXiv:2203.16487 | Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation | [primary](https://arxiv.org/abs/2203.16487) | `papers/inference/99-other-inference-systems/2022-2203.16487-speculative-decoding-exploiting-speculative-execution-for-accelerating-seq2seq-generation.md` |
| 10 | 0 | research | arXiv:2206.09557 | LUT-GEMM: Quantized Matrix Multiplication based on LUTs for Efficient Inference in Large-Scale Generative Language Models | [primary](https://arxiv.org/abs/2206.09557) | `papers/inference/99-other-inference-systems/2022-2206.09557-lut-gemm-quantized-matrix-multiplication-based-on-luts-for-efficient-inference-in-large-scale-generative-language-models.md` |
| 11 | 0 | research | arXiv:2211.10017 | Who Says Elephants Can't Run: Bringing Large Scale MoE Models into Cloud Scale Production | [primary](https://arxiv.org/abs/2211.10017) | `papers/inference/99-other-inference-systems/2022-2211.10017-who-says-elephants-can-t-run-bringing-large-scale-moe-models-into-cloud-scale-production.md` |
| 12 | 0 | research | arXiv:2303.08302 | ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation | [primary](https://arxiv.org/abs/2303.08302) | `papers/inference/99-other-inference-systems/2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehensive-study-to-low-rank-compensation.md` |
| 13 | 0 | research | arXiv:2305.13048 | RWKV: Reinventing RNNs for the Transformer Era | [primary](https://arxiv.org/abs/2305.13048) | `papers/inference/99-other-inference-systems/2023-2305.13048-rwkv-reinventing-rnns-for-the-transformer-era.md` |
| 14 | 0 | research | arXiv:2306.02272 | OWQ: Outlier-Aware Weight Quantization for Efficient Fine-Tuning and Inference of Large Language Models | [primary](https://arxiv.org/abs/2306.02272) | `papers/inference/99-other-inference-systems/2023-2306.02272-owq-outlier-aware-weight-quantization-for-efficient-fine-tuning-and-inference-of-large-language-models.md` |
| 15 | 0 | research | arXiv:2306.11695 | A Simple and Effective Pruning Approach for Large Language Models | [primary](https://arxiv.org/abs/2306.11695) | `papers/inference/99-other-inference-systems/2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md` |
| 16 | 0 | research | arXiv:2309.04255 | LLMCad: Fast and Scalable On-device Large Language Model Inference | [primary](https://arxiv.org/abs/2309.04255) | `papers/inference/99-other-inference-systems/2023-2309.04255-llmcad-fast-and-scalable-on-device-large-language-model-inference.md` |
| 17 | 0 | research | arXiv:2310.04836 | Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM | [primary](https://arxiv.org/abs/2310.04836) | `papers/inference/99-other-inference-systems/2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md` |
| 18 | 0 | research | arXiv:2310.06839 | LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression | [primary](https://arxiv.org/abs/2310.06839) | `papers/inference/99-other-inference-systems/2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-via-prompt-compression.md` |
| 19 | 0 | research | arXiv:2310.07188 | Adaptive Gating in Mixture-of-Experts based Language Models | [primary](https://arxiv.org/abs/2310.07188) | `papers/inference/99-other-inference-systems/2023-2310.07188-adaptive-gating-in-mixture-of-experts-based-language-models.md` |
| 20 | 0 | research | arXiv:2310.09832 | Merging Experts into One: Improving Computational Efficiency of Mixture of Experts | [primary](https://arxiv.org/abs/2310.09832) | `papers/inference/99-other-inference-systems/2023-2310.09832-merging-experts-into-one-improving-computational-efficiency-of-mixture-of-experts.md` |
| 21 | 0 | research | arXiv:2312.06635 | Gated Linear Attention Transformers with Hardware-Efficient Training | [primary](https://arxiv.org/abs/2312.06635) | `papers/inference/99-other-inference-systems/2023-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md` |
| 22 | 0 | research | arXiv:2312.13211 | DSFormer: Effective Compression of Text-Transformers by Dense-Sparse Weight Factorization | [primary](https://arxiv.org/abs/2312.13211) | `papers/inference/99-other-inference-systems/2023-2312.13211-dsformer-effective-compression-of-text-transformers-by-dense-sparse-weight-factorization.md` |
| 23 | 0 | research | arXiv:2401.03462 | Long Context Compression with Activation Beacon | [primary](https://arxiv.org/abs/2401.03462) | `papers/inference/99-other-inference-systems/2024-2401.03462-long-context-compression-with-activation-beacon.md` |
| 24 | 0 | research | arXiv:2401.06761 | APAR: LLMs Can Do Auto-Parallel Auto-Regressive Decoding | [primary](https://arxiv.org/abs/2401.06761) | `papers/inference/99-other-inference-systems/2024-2401.06761-apar-llms-can-do-auto-parallel-auto-regressive-decoding.md` |
| 25 | 0 | research | arXiv:2402.01771 | BlackMamba: Mixture of Experts for State-Space Models | [primary](https://arxiv.org/abs/2402.01771) | `papers/inference/99-other-inference-systems/2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md` |
| 26 | 0 | research | arXiv:2402.04396 | QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks | [primary](https://arxiv.org/abs/2402.04396) | `papers/inference/99-other-inference-systems/2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-codebooks.md` |
| 27 | 0 | research | arXiv:2402.05964 | A Survey on Transformer Compression | [primary](https://arxiv.org/abs/2402.05964) | `papers/inference/99-other-inference-systems/2024-2402.05964-a-survey-on-transformer-compression.md` |
| 28 | 0 | research | arXiv:2402.10631 | BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation | [primary](https://arxiv.org/abs/2402.10631) | `papers/inference/99-other-inference-systems/2024-2402.10631-bitdistiller-unleashing-the-potential-of-sub-4-bit-llms-via-self-distillation.md` |
| 29 | 0 | research | arXiv:2402.11960 | DB-LLM: Accurate Dual-Binarization for Efficient LLMs | [primary](https://arxiv.org/abs/2402.11960) | `papers/inference/99-other-inference-systems/2024-2402.11960-db-llm-accurate-dual-binarization-for-efficient-llms.md` |
| 30 | 0 | research | arXiv:2402.14160 | Recursive Speculative Decoding: Accelerating LLM Inference via Sampling Without Replacement | [primary](https://arxiv.org/abs/2402.14160) | `papers/inference/99-other-inference-systems/2024-2402.14160-recursive-speculative-decoding-accelerating-llm-inference-via-sampling-without-replacement.md` |
| 31 | 0 | research | arXiv:2402.17762 | Massive Activations in Large Language Models | [primary](https://arxiv.org/abs/2402.17762) | `papers/inference/99-other-inference-systems/2024-2402.17762-massive-activations-in-large-language-models.md` |
| 32 | 0 | research | arXiv:2402.18668 | Simple linear attention language models balance the recall-throughput tradeoff | [primary](https://arxiv.org/abs/2402.18668) | `papers/inference/99-other-inference-systems/2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tradeoff.md` |
| 33 | 0 | research | arXiv:2403.01632 | SynCode: LLM Generation with Grammar Augmentation | [primary](https://arxiv.org/abs/2403.01632) | `papers/inference/99-other-inference-systems/2024-2403.01632-syncode-llm-generation-with-grammar-augmentation.md` |
| 34 | 0 | research | arXiv:2403.07652 | Harder Tasks Need More Experts: Dynamic Routing in MoE Models | [primary](https://arxiv.org/abs/2403.07652) | `papers/inference/99-other-inference-systems/2024-2403.07652-harder-tasks-need-more-experts-dynamic-routing-in-moe-models.md` |
| 35 | 0 | research | arXiv:2403.09919 | Recurrent Drafter for Fast Speculative Decoding in Large Language Models | [primary](https://arxiv.org/abs/2403.09919) | `papers/inference/99-other-inference-systems/2024-2403.09919-recurrent-drafter-for-fast-speculative-decoding-in-large-language-models.md` |
| 36 | 0 | research | arXiv:2403.15447 | Decoding Compressed Trust: Scrutinizing the Trustworthiness of Efficient LLMs Under Compression | [primary](https://arxiv.org/abs/2403.15447) | `papers/inference/99-other-inference-systems/2024-2403.15447-decoding-compressed-trust-scrutinizing-the-trustworthiness-of-efficient-llms-under-compression.md` |
| 37 | 0 | research | arXiv:2404.00242 | DeFT: Decoding with Flash Tree-attention for Efficient Tree-structured LLM Inference | [primary](https://arxiv.org/abs/2404.00242) | `papers/inference/99-other-inference-systems/2024-2404.00242-deft-decoding-with-flash-tree-attention-for-efficient-tree-structured-llm-inference.md` |
| 38 | 0 | research | arXiv:2404.02837 | Cherry on Top: Parameter Heterogeneity and Quantization in Large Language Models | [primary](https://arxiv.org/abs/2404.02837) | `papers/inference/99-other-inference-systems/2024-2404.02837-cherry-on-top-parameter-heterogeneity-and-quantization-in-large-language-models.md` |
| 39 | 0 | research | arXiv:2404.04793 | SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget | [primary](https://arxiv.org/abs/2404.04793) | `papers/inference/99-other-inference-systems/2024-2404.04793-squeezeattention-2d-management-of-kv-cache-in-llm-inference-via-layer-wise-optimal-budget.md` |
| 40 | 0 | research | arXiv:2404.08698 | Lossless Acceleration of Large Language Model via Adaptive N-gram Parallel Decoding | [primary](https://arxiv.org/abs/2404.08698) | `papers/inference/99-other-inference-systems/2024-2404.08698-lossless-acceleration-of-large-language-model-via-adaptive-n-gram-parallel-decoding.md` |
| 41 | 0 | research | arXiv:2404.10308 | Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs | [primary](https://arxiv.org/abs/2404.10308) | `papers/inference/99-other-inference-systems/2024-2404.10308-hierarchical-context-merging-better-long-context-understanding-for-pre-trained-llms.md` |
| 42 | 0 | research | arXiv:2404.14527 | Mélange: Cost Efficient Large Language Model Serving by Exploiting GPU Heterogeneity | [primary](https://arxiv.org/abs/2404.14527) | `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2404.14527-melange-cost-efficient-llm-serving-gpu-heterogeneity.md` |
| 43 | 0 | research | arXiv:2405.13019 | A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models | [primary](https://arxiv.org/abs/2405.13019) | `papers/survey/05-accelerated-generation/2024-2405.13019-accelerated-generation-survey.md` |
| 44 | 0 | research | arXiv:2405.14636 | PerLLM: Personalized Inference Scheduling with Edge-Cloud Collaboration for Diverse LLM Services | [primary](https://arxiv.org/abs/2405.14636) | `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2405.14636-perllm.md` |
| 45 | 0 | research | arXiv:2406.03482 | QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead | [primary](https://arxiv.org/abs/2406.03482) | `papers/inference/99-other-inference-systems/2024-2406.03482-qjl-1-bit-quantized-jl-transform-for-kv-cache-quantization-with-zero-overhead.md` |
| 46 | 0 | research | arXiv:2406.15486 | SampleAttention: Near-Lossless Acceleration of Long Context LLM Inference with Adaptive Structured Sparse Attention | [primary](https://arxiv.org/abs/2406.15486) | `papers/inference/99-other-inference-systems/2024-2406.15486-sampleattention-near-lossless-acceleration-of-long-context-llm-inference-with-adaptive-structured-sparse-attention.md` |
| 47 | 0 | research | arXiv:2407.04656 | Lazarus: Resilient and Elastic Training of Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2407.04656) | `papers/inference/99-other-inference-systems/2024-2407.04656-lazarus-resilient-and-elastic-training-of-mixture-of-experts-models.md` |
| 48 | 0 | research | arXiv:2407.09486 | ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving | [primary](https://arxiv.org/abs/2407.09486) | `papers/inference/99-other-inference-systems/2024-2407.09486-enova-autoscaling-towards-cost-effective-and-stable-serverless-llm-serving.md` |
| 49 | 0 | research | arXiv:2408.03314 | Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters | [primary](https://arxiv.org/abs/2408.03314) | `papers/inference/99-other-inference-systems/2024-2408.03314-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model-parameters.md` |
| 50 | 0 | research | arXiv:2409.01143 | HexiScale: Facilitating Large Language Model Training over Heterogeneous Hardware | [primary](https://arxiv.org/abs/2409.01143) | `papers/inference/99-other-inference-systems/2024-2409.01143-hexiscale-facilitating-large-language-model-training-over-heterogeneous-hardware.md` |
| 51 | 0 | research | arXiv:2409.17264 | No Request Left Behind: Tackling Heterogeneity in Long-Context LLM Inference with Medha | [primary](https://arxiv.org/abs/2409.17264) | `papers/inference/99-other-inference-systems/2024-2409.17264-no-request-left-behind-tackling-heterogeneity-in-long-context-llm-inference-with-medha.md` |
| 52 | 0 | research | arXiv:2410.14731 | MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection | [primary](https://arxiv.org/abs/2410.14731) | `papers/inference/99-other-inference-systems/2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md` |
| 53 | 0 | research | arXiv:2411.18424 | FastSwitch: Optimizing Context Switching Efficiency in Fairness-aware Large Language Model Serving | [primary](https://arxiv.org/abs/2411.18424) | `papers/inference/99-other-inference-systems/2024-2411.18424-fastswitch-optimizing-context-switching-efficiency-in-fairness-aware-large-language-model-serving.md` |
| 54 | 0 | research | arXiv:2412.14711 | ReMoE: Fully Differentiable Mixture-of-Experts with ReLU Routing | [primary](https://arxiv.org/abs/2412.14711) | `papers/inference/99-other-inference-systems/2024-2412.14711-remoe-fully-differentiable-mixture-of-experts-with-relu-routing.md` |
| 55 | 0 | research | arXiv:2412.19442 | A Survey on Large Language Model Acceleration based on KV Cache Management | [primary](https://arxiv.org/abs/2412.19442) | `papers/inference/99-other-inference-systems/2024-2412.19442-a-survey-on-large-language-model-acceleration-based-on-kv-cache-management.md` |
| 56 | 0 | research | arXiv:2502.07115 | Online Scheduling for LLM Inference with KV Cache Constraints | [primary](https://arxiv.org/abs/2502.07115) | `papers/inference/99-other-inference-systems/2025-2502.07115-online-scheduling-for-llm-inference-with-kv-cache-constraints.md` |
| 57 | 0 | research | arXiv:2502.12110 | A-Mem: Agentic Memory for LLM Agents | [primary](https://arxiv.org/abs/2502.12110) | `papers/inference/99-other-inference-systems/2025-2502.12110-a-mem-agentic-memory-for-llm-agents.md` |
| 58 | 0 | research | arXiv:2502.17421 | LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification | [primary](https://arxiv.org/abs/2502.17421) | `papers/inference/99-other-inference-systems/2025-2502.17421-longspec-long-context-lossless-speculative-decoding-with-efficient-drafting-and-verification.md` |
| 59 | 0 | research | arXiv:2503.00634 | Efficiently Editing Mixture-of-Experts Models with Compressed Experts | [primary](https://arxiv.org/abs/2503.00634) | `papers/inference/99-other-inference-systems/2025-2503.00634-efficiently-editing-mixture-of-experts-models-with-compressed-experts.md` |
| 60 | 0 | research | arXiv:2503.16428 | XAttention: Block Sparse Attention with Antidiagonal Scoring | [primary](https://arxiv.org/abs/2503.16428) | `papers/inference/99-other-inference-systems/2025-2503.16428-xattention-block-sparse-attention-with-antidiagonal-scoring.md` |
| 61 | 0 | research | arXiv:2504.11750 | Characterizing and Optimizing LLM Inference Workloads on CPU-GPU Coupled Architectures | [primary](https://arxiv.org/abs/2504.11750) | `papers/inference/99-other-inference-systems/2025-2504.11750-characterizing-and-optimizing-llm-inference-workloads-on-cpu-gpu-coupled-architectures.md` |
| 62 | 0 | research | arXiv:2504.19519 | Efficient and Adaptable Overlapping for Computation and Communication via Signaling and Reordering | [primary](https://arxiv.org/abs/2504.19519) | `papers/inference/99-other-inference-systems/2025-2504.19519-efficient-and-adaptable-overlapping-for-computation-and-communication-via-signaling-and-reordering.md` |
| 63 | 0 | research | arXiv:2505.17639 | PreMoE: Proactive Inference for Efficient Mixture-of-Experts | [primary](https://arxiv.org/abs/2505.17639) | `papers/inference/02-adaptive-expert-computation-compression/2025-2505.17639-premoe-proactive-sparse-specialists.md` |
| 64 | 0 | research | arXiv:2505.24298 | AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning | [primary](https://arxiv.org/abs/2505.24298) | `papers/inference/99-other-inference-systems/2025-2505.24298-areal-a-large-scale-asynchronous-reinforcement-learning-system-for-language-reasoning.md` |
| 65 | 0 | research | arXiv:2506.07530 | BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation | [primary](https://arxiv.org/abs/2506.07530) | `papers/inference/99-other-inference-systems/2025-2506.07530-bitvla-1-bit-vision-language-action-models-for-robotics-manipulation.md` |
| 66 | 0 | research | arXiv:2506.24045 | Agent.xpu: Efficient Scheduling of Agentic LLM Workloads on Heterogeneous SoC | [primary](https://arxiv.org/abs/2506.24045) | `papers/inference/99-other-inference-systems/2025-2506.24045-agent-xpu-efficient-scheduling-of-agentic-llm-workloads-on-heterogeneous-soc.md` |
| 67 | 0 | research | arXiv:2507.11417 | Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations | [primary](https://arxiv.org/abs/2507.11417) | `papers/inference/99-other-inference-systems/2025-2507.11417-quantifying-the-energy-consumption-and-carbon-emissions-of-llm-inference-via-simulations.md` |
| 68 | 0 | research | arXiv:2507.19635 | Efficient and Scalable Agentic AI with Heterogeneous Systems | [primary](https://arxiv.org/abs/2507.19635) | `papers/inference/99-other-inference-systems/2025-2507.19635-efficient-and-scalable-agentic-ai-with-heterogeneous-systems.md` |
| 69 | 0 | research | arXiv:2508.08448 | Towards Efficient and Practical GPU Multitasking in the Era of LLM | [primary](https://arxiv.org/abs/2508.08448) | `papers/inference/99-other-inference-systems/2025-2508.08448-towards-efficient-and-practical-gpu-multitasking-in-the-era-of-llm.md` |
| 70 | 0 | research | arXiv:2508.18376 | DualSparse-MoE: Coordinating Tensor/Neuron-Level Sparsity with Expert Partition and Reconstruction | [primary](https://arxiv.org/abs/2508.18376) | `papers/inference/02-adaptive-expert-computation-compression/2025-2508.18376-dualsparse-moe.md` |
| 71 | 0 | research | arXiv:2509.12993 | HPIM: Heterogeneous Processing-In-Memory-based Accelerator for Large Language Models Inference | [primary](https://arxiv.org/abs/2509.12993) | `papers/inference/99-other-inference-systems/2025-2509.12993-hpim-heterogeneous-pim-llm-inference.md` |
| 72 | 0 | research | arXiv:2509.18362 | FastMTP: Accelerating LLM Inference with Enhanced Multi-Token Prediction | [primary](https://arxiv.org/abs/2509.18362) | `papers/inference/99-other-inference-systems/2025-2509.18362-fastmtp-accelerating-llm-inference-with-enhanced-multi-token-prediction.md` |
| 73 | 0 | research | arXiv:2510.02758 | TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling | [primary](https://arxiv.org/abs/2510.02758) | `papers/inference/99-other-inference-systems/2025-2510.02758-tokenflow-responsive-llm-text-streaming-serving-under-request-burst-via-preemptive-scheduling.md` |
| 74 | 0 | research | arXiv:2510.12357 | MoBiLE: Efficient Mixture-of-Experts Inference on Consumer GPU with Mixture of Big Little Experts | [primary](https://arxiv.org/abs/2510.12357) | `papers/inference/99-other-inference-systems/2025-2510.12357-mobile-efficient-mixture-of-experts-inference-on-consumer-gpu-with-mixture-of-big-little-experts.md` |
| 75 | 0 | research | arXiv:2510.14392 | FairBatching: Fairness-Aware Batch Formation for LLM Inference | [primary](https://arxiv.org/abs/2510.14392) | `papers/inference/99-other-inference-systems/2025-2510.14392-fairbatching-fairness-aware-batch-formation-for-llm-inference.md` |
| 76 | 0 | research | arXiv:2510.15312 | Accelerating Mobile Language Model via Speculative Decoding and NPU-Coordinated Execution | [primary](https://arxiv.org/abs/2510.15312) | `papers/inference/99-other-inference-systems/2025-2510.15312-accelerating-mobile-language-model-via-speculative-decoding-and-npu-coordinated-execution.md` |
| 77 | 0 | research | arXiv:2511.00606 | SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding | [primary](https://arxiv.org/abs/2511.00606) | `papers/inference/99-other-inference-systems/2025-2511.00606-specdiff-2-scaling-diffusion-drafter-alignment-for-faster-speculative-decoding.md` |
| 78 | 0 | research | arXiv:2511.07427 | DynaKV: Enabling Accurate and Efficient Long-Sequence LLM Decoding on Smartphones | [primary](https://arxiv.org/abs/2511.07427) | `papers/inference/99-other-inference-systems/2025-2511.07427-dynakv-enabling-accurate-and-efficient-long-sequence-llm-decoding-on-smartphones.md` |
| 79 | 0 | research | arXiv:2511.17560 | A3: Attention-Aware Accurate KV Cache Fusion for Fast Large Language Model Serving | [primary](https://arxiv.org/abs/2511.17560) | `papers/inference/99-other-inference-systems/2025-2511.17560-a3-attention-aware-accurate-kv-cache-fusion-for-fast-large-language-model-serving.md` |
| 80 | 0 | research | arXiv:2512.14080 | SonicMoE: Accelerating MoE with IO and Tile-aware Optimizations | [primary](https://arxiv.org/abs/2512.14080) | `papers/inference/99-other-inference-systems/2025-2512.14080-sonicmoe-accelerating-moe-with-io-and-tile-aware-optimizations.md` |
| 81 | 0 | research | arXiv:2601.05109 | Nalar: A Serving Framework for Agent Workflows | [primary](https://arxiv.org/abs/2601.05109) | `papers/inference/99-other-inference-systems/2026-2601.05109-nalar-a-serving-framework-for-agent-workflows.md` |
| 82 | 0 | research | arXiv:2601.17668 | Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction | [primary](https://arxiv.org/abs/2601.17668) | `papers/inference/99-other-inference-systems/2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md` |
| 83 | 0 | research | arXiv:2602.03560 | HySparse: A Hybrid Sparse Attention Architecture with Oracle Token Selection and KV Cache Sharing | [primary](https://arxiv.org/abs/2602.03560) | `papers/inference/99-other-inference-systems/2026-2602.03560-hysparse-a-hybrid-sparse-attention-architecture-with-oracle-token-selection-and-kv-cache-sharing.md` |
| 84 | 0 | research | arXiv:2602.11192 | MELINOE: Fine-Tuning Enables Memory-Efficient Inference for Mixture-of-Experts Models | [primary](https://arxiv.org/abs/2602.11192) | `papers/inference/02-adaptive-expert-computation-compression/2026-2602.11192-melinoe-memory-efficient-inference.md` |
| 85 | 0 | research | arXiv:2602.16284 | Fast KV Compaction via Attention Matching | [primary](https://arxiv.org/abs/2602.16284) | `papers/inference/99-other-inference-systems/2026-2602.16284-fast-kv-compaction-via-attention-matching.md` |
| 86 | 0 | research | arXiv:2603.02217 | Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression | [primary](https://arxiv.org/abs/2603.02217) | `papers/inference/02-adaptive-expert-computation-compression/2026-2603.02217-router-calibration-moe-compression.md` |
| 87 | 0 | research | arXiv:2603.07810 | Temperature-Aware Scheduling of LLM Inference in Large-Scale Geo-Distributed Edge Data Centers with Distributed Optimization | [primary](https://arxiv.org/abs/2603.07810) | `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2603.07810-temperature-aware-geo-distributed-llm-scheduling.md` |
| 88 | 0 | research | arXiv:2603.13606 | NCCL EP: Towards a Unified Expert Parallel Communication API for NCCL | [primary](https://arxiv.org/abs/2603.13606) | `papers/inference/99-other-inference-systems/2026-2603.13606-nccl-ep-towards-a-unified-expert-parallel-communication-api-for-nccl.md` |
| 89 | 0 | research | arXiv:2603.28458 | HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention | [primary](https://arxiv.org/abs/2603.28458) | `papers/inference/99-other-inference-systems/2026-2603.28458-hisa-efficient-hierarchical-indexing-for-fine-grained-sparse-attention.md` |
| 90 | 0 | research | arXiv:2604.10603 | MoEITS: A Green AI approach for simplifying MoE-LLMs | [primary](https://arxiv.org/abs/2604.10603) | `papers/inference/02-adaptive-expert-computation-compression/2026-2604.10603-moeits-information-theoretic-simplification.md` |
| 91 | 0 | research | arXiv:2604.16957 | Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon | [primary](https://arxiv.org/abs/2604.16957) | `papers/inference/99-other-inference-systems/2026-2604.16957-open-tq-metal-fused-compressed-domain-attention-for-long-context-llm-inference-on-apple-silicon.md` |
| 92 | 0 | research | arXiv:2604.26256 | DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training | [primary](https://arxiv.org/abs/2604.26256) | `papers/inference/99-other-inference-systems/2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-model-training.md` |
| 93 | 0 | research | arXiv:2605.06676 | LKV: End-to-End Learning of Head-wise Budgets and Token Selection for LLM KV Cache Eviction | [primary](https://www.semanticscholar.org/paper/9dbefa4becfe4a6ae3decde6fabad3ab975cde52) | `papers/inference/99-other-inference-systems/2026-2605.06676-lkv-end-to-end-learning-of-head-wise-budgets-and-token-selection-for-llm-kv-cache-eviction.md` |
| 94 | 0 | research | arXiv:2605.25550 | DisagFusion: Asynchronous Pipeline Parallelism and Elastic Scheduling for Disaggregated Diffusion Serving | [primary](https://arxiv.org/abs/2605.25550) | `papers/inference/99-other-inference-systems/2026-2605.25550-disagfusion-asynchronous-pipeline-parallelism-and-elastic-scheduling-for-disaggregated-diffusion-serving.md` |
| 95 | 0 | research | arXiv:2605.29350 | ConMoE: Expert-Pool Consolidation via Prototype Reassignment for MoE Compression | [primary](https://arxiv.org/abs/2605.29350) | `papers/inference/02-adaptive-expert-computation-compression/2026-2605.29350-conmoe-prototype-reassignment-compression.md` |
| 96 | 0 | research | arXiv:2606.02982 | DriftSched: Adaptive QoS-Aware Scheduling under Runtime Token Drift for Multi-Tenant GPU Inference | [primary](https://arxiv.org/abs/2606.02982) | `papers/inference/99-other-inference-systems/2026-2606.02982-driftsched-adaptive-qos-aware-scheduling-under-runtime-token-drift-for-multi-tenant-gpu-inference.md` |
| 97 | 0 | research | arXiv:2606.12370 | Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling | [primary](https://arxiv.org/abs/2606.12370) | `papers/inference/99-other-inference-systems/2026-2606.12370-breaking-entropy-bounds-accelerating-rl-training-via-mtp-with-rejection-sampling.md` |
| 98 | 0 | research | arXiv:2606.15716 | How to Score Experts for One-Shot MoE Expert Pruning: A Unified Formulation and Selection Principle | [primary](https://arxiv.org/abs/2606.15716) | `papers/inference/02-adaptive-expert-computation-compression/2026-2606.15716-one-shot-expert-pruning-scoring.md` |
| 99 | 0 | research | arXiv:2606.21238 | Recency/Frequency Adaptive KV Caching for Large Language Model Serving | [primary](https://www.semanticscholar.org/paper/4634757f8c6adc509d5f919486320b78e8847787) | `papers/inference/99-other-inference-systems/2026-2606.21238-recency-frequency-adaptive-kv-caching-for-large-language-model-serving.md` |
| 100 | 0 | research | arXiv:2607.04164 | BrownoutMoE: Structure-Aware Expert Grouping for Efficient and Accurate LLM Web-based Services | [primary](https://www.semanticscholar.org/paper/f8b43d078a89a2622af43b6f1855dffcece37dbb) | `papers/inference/99-other-inference-systems/2026-2607.04164-brownoutmoe-structure-aware-expert-grouping-for-efficient-and-accurate-llm-web-based-services.md` |
| 101 | 0 | research | arXiv:2607.10987 | [AAFLOW+] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows | [primary](https://www.semanticscholar.org/paper/e45860ca84d523ee9b55d4824181233e7945d456) | `papers/inference/99-other-inference-systems/2026-2607.10987-aaflow-stateful-operator-abstraction-with-zero-copy-distributed-kv-cache-orchestration-for-multi-agent-workflows.md` |
| 102 | 0 | research | arXiv:2607.17181 | Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs | [primary](https://www.semanticscholar.org/paper/e7106b6132090e3a5d8f669d7e94ba890e42b781) | `papers/inference/99-other-inference-systems/2026-2607.17181-talaria-session-aware-serverless-serving-of-hundred-billion-parameter-llms.md` |
| 103 | 0 | research | arXiv:2607.28069 | SemPIC: Learning Semantic Position-Independent KV Caches | [primary](https://www.semanticscholar.org/paper/f48d751da47d9a84046858a1ef820b02aa7775b1) | `papers/inference/99-other-inference-systems/2026-2607.28069-sempic-learning-semantic-position-independent-kv-caches.md` |
| 104 | 0 | research | arXiv:2608.05926 | BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge | [primary](https://arxiv.org/abs/2608.05926) | `papers/inference/08-edge-on-device-llm-systems/2026-2608.05926-balance-hybrid-autoregressive-speculative-edge.md` |
| 105 | 0 | research | arXiv:2608.11045 | ReRound: Reconstructive Rounding to Resolve Midpoint Ambiguity in Calibration-Free LLM Quantization | [primary](https://arxiv.org/abs/2608.11045) | `papers/inference/99-other-inference-systems/2026-2608.11045-reround-reconstructive-rounding-to-resolve-midpoint-ambiguity-in-calibration-free-llm-quantization.md` |
| 106 | 0 | research | arXiv:2608.14376 | CoRun: Padding is Simple and Efficient for Deterministic LLM Inference | [primary](https://arxiv.org/abs/2608.14376) | `papers/inference/99-other-inference-systems/2026-2608.14376-corun-padding-is-simple-and-efficient-for-deterministic-llm-inference.md` |
| 107 | 0 | research | arXiv:2608.15584 | GraniKV: Asymmetric Granularity KV-Cache Paging for Multi-Agent Systems with Long Shared Prefix | [primary](https://www.semanticscholar.org/paper/1e7525745039a88cd6a0e58c0526ef6695ec9214) | `papers/inference/99-other-inference-systems/2026-2608.15584-granikv-asymmetric-granularity-kv-cache-paging-for-multi-agent-systems-with-long-shared-prefix.md` |
| 108 | 0 | research | arXiv:2608.22503 | Understanding the Synchronization Tax in GPU Scale-Up Domains | [primary](https://arxiv.org/abs/2608.22503) | `papers/inference/99-other-inference-systems/2026-2608.22503-understanding-the-synchronization-tax-in-gpu-scale-up-domains.md` |
| 109 | 0 | research | arXiv:2608.24650 | Simthesizer: An Agent-Driven Simulation Framework for LLM Serving Systems | [primary](https://arxiv.org/abs/2608.24650) | `papers/inference/99-other-inference-systems/2026-2608.24650-simthesizer-an-agent-driven-simulation-framework-for-llm-serving-systems.md` |
| 110 | 0 | research | arXiv:2608.28444 | Sliding-window beats linear attention | [primary](https://www.semanticscholar.org/paper/633f43137abd58fdd39606b868b27eccafae8625) | `papers/inference/99-other-inference-systems/2026-2608.28444-sliding-window-beats-linear-attention.md` |
| 111 | 0 | research | arXiv:2609.00363 | Deterministic LLM Inference Across GPU Kernels: Power-of-Two INT8 Quantization Scales and the Limits of Tolerance-Based Conformance | [primary](https://arxiv.org/abs/2609.00363) | `papers/inference/99-other-inference-systems/2026-2609.00363-deterministic-llm-inference-gpu-kernels-int8.md` |
| 112 | 0 | research | arXiv:2609.04875 | Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents | [primary](https://arxiv.org/abs/2609.04875) | `papers/inference/99-other-inference-systems/2026-2609.04875-forgetting-without-restarting-execution-state-unlearning-for-stateful-llm-agents.md` |
| 113 | 0 | research | arXiv:2609.07664 | Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs | [primary](https://www.semanticscholar.org/paper/84845b9a9ba10adeb94154d89fac900566597aaf) | `papers/inference/99-other-inference-systems/2026-2609.07664-accuracy-is-not-enough-a-divergence-based-approach-to-evaluate-fidelity-loss-in-quantized-llms.md` |
| 114 | 0 | research | arXiv:2609.08135 | KBBQ: A Predictive Noise Law and the Limits of Spectrum Flattening in FP4 Quantization | [primary](https://www.semanticscholar.org/paper/384b3e22a60cd9fe55232c2725725a646bec1413) | `papers/inference/99-other-inference-systems/2026-2609.08135-kbbq-a-predictive-noise-law-and-the-limits-of-spectrum-flattening-in-fp4-quantization.md` |
| 115 | 0 | research | arXiv:2609.11687 | Structured Transforms for Low-Overhead Quantization of Language Models | [primary](https://www.semanticscholar.org/paper/aa2d1e435c726e052e5550468c8d4cf60db59331) | `papers/inference/99-other-inference-systems/2026-2609.11687-structured-transforms-for-low-overhead-quantization-of-language-models.md` |
| 116 | 0 | research | arXiv:2609.12378 | An Open-Source End-to-End FHE Implementation for Privacy-Preserving Llama 3 8B Inference | [primary](https://arxiv.org/abs/2609.12378) | `papers/inference/99-other-inference-systems/2026-2609.12378-odin-fhe-privacy-preserving-llama-inference.md` |
| 117 | 0 | research | arXiv:2609.13846 | Affinity-Aware Sharding for Delayed Tensor Parallelism | [primary](https://arxiv.org/abs/2609.13846) | `papers/inference/99-other-inference-systems/2026-2609.13846-affinity-aware-sharding-for-delayed-tensor-parallelism.md` |
| 118 | 0 | research | arXiv:2609.15810 | VC-Attention: Value Smoothing and Softmax Casting for Low-bit Attention | [primary](https://www.semanticscholar.org/paper/d26fb643c9c194cb4d34bd660b031a61d5f72f5d) | `papers/inference/99-other-inference-systems/2026-2609.15810-vc-attention-value-smoothing-and-softmax-casting-for-low-bit-attention.md` |
| 119 | 0 | research | arXiv:2609.19702 | Understanding and Exploiting Diagonal Attention Sparsity in Autoregressive Image Generation | [primary](https://www.semanticscholar.org/paper/54db2b227072dcee4790de99c581d51c7d3c17f7) | `papers/inference/99-other-inference-systems/2026-2609.19702-understanding-and-exploiting-diagonal-attention-sparsity-in-autoregressive-image-generation.md` |
| 120 | 0 | research | arXiv:2609.22106 | PRQuant: Permutation Residual Quantization for Low-Overhead Inference | [primary](https://arxiv.org/abs/2609.22106) | `papers/inference/99-other-inference-systems/2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md` |
| 121 | 0 | research | arXiv:2609.25442 | WeightBridge: An Efficient Weight Transfer Library for Reinforcement Learning | [primary](https://arxiv.org/abs/2609.25442) | `papers/inference/99-other-inference-systems/2026-2609.25442-weightbridge-an-efficient-weight-transfer-library-for-reinforcement-learning.md` |
| 122 | 0 | research | arXiv:2609.31415 | Evaluating the accuracy of KV cache reuse techniques | [primary](https://arxiv.org/abs/2609.31415) | `papers/inference/99-other-inference-systems/2026-2609.31415-evaluating-the-accuracy-of-kv-cache-reuse-techniques.md` |
| 123 | 0 | research | DOI:10.1016/j.compeleceng.2026.111505 | Component-aware self-speculative decoding for hybrid language models: An architectural viability study | [primary](https://doi.org/10.1016/j.compeleceng.2026.111505) | `papers/inference/99-other-inference-systems/2026-component-aware-self-speculative-decoding-hybrid-language-models.md` |
| 124 | 0 | research | DOI:10.1016/j.neunet.2026.109469 | DR-EFT: Exploring and reloading domain-representative experts for the memory-constrained fine-tuning of MoE large models | [primary](https://doi.org/10.1016/j.neunet.2026.109469) | `papers/training/01-training-offload-memory-systems/2026-dr-eft-domain-representative-expert-finetuning.md` |
| 125 | 0 | research | DOI:10.1109/CCGrid68966.2026.00014 | Quicktopia: Iteration-Level GPU Frequency Control for Energy–Latency Co-Optimization in LLM Inference | [primary](https://www.semanticscholar.org/paper/88a222b2340b8906e15edd5efd58293b25fc38ce) | `papers/inference/99-other-inference-systems/2020-2026.00014-quicktopia-iteration-level-gpu-frequency-control-for-energylatency-co-optimization-in-llm-inference.md` |
| 126 | 0 | research | DOI:10.1109/ICC59461.2026.11587970 | InKubeator: Pre-warming In-Memory KV Caches from Disk for Elastic LLM Serving | [primary](https://doi.org/10.1109/ICC59461.2026.11587970) | `papers/inference/99-other-inference-systems/2026-805ee7ad7ae4-inkubeator-pre-warming-in-memory-kv-caches-from-disk-for-elastic-llm-serving.md` |
| 127 | 0 | research | DOI:10.1109/IMNS67862.2026.11655252 | Characterizing Predictability–Latency Trade-offs of KV-Cache SSD Offloading in LMCache for LLM Serving Systems | [primary](https://doi.org/10.1109/IMNS67862.2026.11655252) | `papers/inference/10-kv-cache-offload-recomputation/2026-lmcache-kv-cache-ssd-offloading-predictability-latency.md` |
| 128 | 0 | research | DOI:10.1109/INFOCOM59046.2026.11571717 | SemCache: Semantic-Aware Cache Sharing for Efficient Multi-User LoRA-Adapted LLM Inference at the Edge | [primary](https://doi.org/10.1109/INFOCOM59046.2026.11571717) | `papers/inference/99-other-inference-systems/2026-7056d9defe0d-semcache-semantic-aware-cache-sharing-for-efficient-multi-user-lora-adapted-llm-inference-at-the-edge.md` |
| 129 | 0 | research | DOI:10.1109/JCC72984.2026.00058 | UNAS: Urgency- and Fairness-Aware Scheduling for SLO-Oriented LLM Serving | [primary](https://doi.org/10.1109/JCC72984.2026.00058) | `papers/inference/99-other-inference-systems/2020-2026.00058-unas-urgency-and-fairness-aware-scheduling-for-slo-oriented-llm-serving.md` |
| 130 | 0 | research | DOI:10.1109/LCA.2026.3660969 | H3: Hybrid Architecture Using High Bandwidth Memory and High Bandwidth Flash for Cost-Efficient LLM Inference | [primary](https://doi.org/10.1109/LCA.2026.3660969) | `papers/inference/99-other-inference-systems/2026-27b000808907-h3-hybrid-architecture-using-high-bandwidth-memory-and-high-bandwidth-flash-for-cost-efficient-llm-inference.md` |
| 131 | 0 | research | DOI:10.1109/NVMSA71223.2026.11658877 | Poster: SAF: Semantic-Aware Flushing for Latency and Jitter Suppression in Continuous VLA Inference on Edge Devices | [primary](https://doi.org/10.1109/NVMSA71223.2026.11658877) | `papers/inference/10-kv-cache-offload-recomputation/2026-saf-semantic-aware-flushing-kv-nvme-edge.md` |
| 132 | 0 | research | DOI:10.1109/TMC.2026.3697502 | CALSI: Context-Aware Layer Skipping Inference for On-Device LLM Serving | [primary](https://www.semanticscholar.org/paper/b55f24c3e3257011b8dc6ea308c4f54242ab7e53) | `papers/inference/99-other-inference-systems/2026-392ca7562b95-calsi-context-aware-layer-skipping-inference-for-on-device-llm-serving.md` |
| 133 | 0 | research | DOI:10.1109/TPDS.2026.3729988 | FairCache: Demystifying Cache-Induced Unfairness in Multi-Tenant Large Language Model Serving | [primary](https://www.semanticscholar.org/paper/69e16a381bb1a483fb9a5e494bc895ad74bb412a) | `papers/inference/99-other-inference-systems/2026-e490b2439d3f-faircache-demystifying-cache-induced-unfairness-in-multi-tenant-large-language-model-serving.md` |
| 134 | 0 | research | DOI:10.1145/3552326.3587438 | Tabi: An Efficient Multi-Level Inference System for Large Language Models | [primary](https://doi.org/10.1145/3552326.3587438) | `papers/inference/99-other-inference-systems/2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md` |
| 135 | 0 | research | DOI:10.1145/3600006.3613175 | Sia: Heterogeneity-aware, goodput-optimized ML-cluster scheduling | [primary](https://doi.org/10.1145/3600006.3613175) | `papers/inference/99-other-inference-systems/2026-2c2071afa90d-sia-heterogeneity-aware-goodput-optimized-ml-cluster-scheduling.md` |
| 136 | 0 | research | DOI:10.1145/3620666.3651329 | Characterizing Power Management Opportunities for LLMs in the Cloud | [primary](https://doi.org/10.1145/3620666.3651329) | `papers/inference/99-other-inference-systems/2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md` |
| 137 | 0 | research | DOI:10.1145/3642970.3655844 | ALTO: An Efficient Network Orchestrator for Compound AI Systems | [primary](https://doi.org/10.1145/3642970.3655844) | `papers/inference/99-other-inference-systems/2024-01aa9dc12834-alto-an-efficient-network-orchestrator-for-compound-ai-systems.md` |
| 138 | 0 | research | DOI:10.1145/3689031.3696072 | Fast State Restoration in LLM Serving with HCache | [primary](https://doi.org/10.1145/3689031.3696072) | `papers/inference/99-other-inference-systems/0000-c57896a0996e-fast-state-restoration-in-llm-serving-with-hcache.md` |
| 139 | 0 | research | DOI:10.1145/3712285.3759903 | Diff-MoE: Efficient Batched MoE Inference with Priority-Driven Differential Expert Caching | [primary](https://doi.org/10.1145/3712285.3759903) | `papers/inference/04-moe-offload-expert-cache/2025-diff-moe-priority-driven-differential-expert-caching.md` |
| 140 | 0 | research | DOI:10.1145/3731569.3764823 | Jenga: Effective Memory Management for Serving LLM with Heterogeneity | [primary](https://doi.org/10.1145/3731569.3764823) | `papers/inference/99-other-inference-systems/0000-c5994a53cb83-jenga-effective-memory-management-for-serving-llm-with-heterogeneity.md` |
| 141 | 0 | research | DOI:10.1145/3772052.3772264 | Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment | [primary](https://doi.org/10.1145/3772052.3772264) | `papers/inference/99-other-inference-systems/2025-6987e5a4e5ec-cauchy-a-cost-efficient-llm-serving-system-through-adaptive-heterogeneous-deployment.md` |
| 142 | 0 | research | DOI:10.1145/3779212.3790246 | SwiftSpec: Disaggregated Speculative Decoding and Fused Kernels for Low-Latency LLM Inference | [primary](https://doi.org/10.1145/3779212.3790246) | `papers/inference/99-other-inference-systems/2026-92272744585e-swiftspec-disaggregated-speculative-decoding-and-fused-kernels-for-low-latency-llm-inference.md` |
| 143 | 0 | research | DOI:10.1145/3789240.3822569 | Memory as a First‑Class Resource in AI‑Factory Simulation | [primary](https://www.semanticscholar.org/paper/ab6071dcfef2e4a7092fdb5866e5a34485b28d51) | `papers/inference/99-other-inference-systems/2026-739d27a164e4-memory-as-a-firstclass-resource-in-aifactory-simulation.md` |
| 144 | 0 | research | DOI:10.1145/3789240.3829347 | DynamoServe: A Distributed Tiered Memory System for Multi-tenant LLM Serving | [primary](https://www.semanticscholar.org/paper/3fada5fea76c30b6fb0f156189b080168f66e241) | `papers/inference/99-other-inference-systems/2026-3eaac796b1c5-dynamoserve-a-distributed-tiered-memory-system-for-multi-tenant-llm-serving.md` |
| 145 | 0 | research | DOI:10.1145/3805621.3807651 | Hardware-Aware Co-Design of Multi-Chip LLM Serving via Performance Modeling | [primary](https://doi.org/10.1145/3805621.3807651) | `papers/inference/99-other-inference-systems/2026-dae506ee161c-hardware-aware-co-design-of-multi-chip-llm-serving-via-performance-modeling.md` |
| 146 | 0 | research | DOI:10.1145/3821219 | AdaptiveKV: Accelerating KV Cache Offloading with a Bandwidth-Adaptive Memory Allocation Mechanism | [primary](https://doi.org/10.1145/3821219) | `papers/inference/99-other-inference-systems/2026-96d0bc7068f2-adaptivekv-accelerating-kv-cache-offloading-with-a-bandwidth-adaptive-memory-allocation-mechanism.md` |
| 147 | 0 | research | DOI:10.1145/3832810.3832827 | ReliefServe: Relieving GPU Pressure in Multi-Model Serving via Selective CPU Escape | [primary](https://www.semanticscholar.org/paper/30f2fe44afe7a63e4a4e20c8f5083c129e09ae80) | `papers/inference/99-other-inference-systems/2026-ef0cbb7f0917-reliefserve-relieving-gpu-pressure-in-multi-model-serving-via-selective-cpu-escape.md` |
| 148 | 0 | research | DOI:10.1145/3832810.3832865 | WAQ-LLM: Optimizing Multi-Instance LLM Deployment via Workload-Aware Queueing Model | [primary](https://www.semanticscholar.org/paper/a3ea92c6fa8233ac57ec595875a2a35f7f640056) | `papers/inference/99-other-inference-systems/2026-eb0724db43f1-waq-llm-optimizing-multi-instance-llm-deployment-via-workload-aware-queueing-model.md` |
| 149 | 0 | research | DOI:10.1145/3832810.3832894 | Cross-Layer Performance Analysis of Single-GPU Large Language Model Inference | [primary](https://www.semanticscholar.org/paper/64b1253f0b492e5a855336514fc0457ad35219eb) | `papers/inference/99-other-inference-systems/2026-c4e6405cec16-cross-layer-performance-analysis-of-single-gpu-large-language-model-inference.md` |
| 150 | 0 | research | DOI:10.18653/v1/2021.naacl-industry.15 | LightSeq: A High Performance Inference Library for Transformers | [primary](https://doi.org/10.18653/v1/2021.naacl-industry.15) | `papers/inference/99-other-inference-systems/0000-439132b7c6e4-lightseq-a-high-performance-inference-library-for-transformers.md` |
| 151 | 0 | research | DOI:10.21203/rs.3.rs-10952127/v1 | Reasoning-Aware Error-Bounded KV-Cache Compression and Sparse Attention for Long-Context LLMs | [primary](https://doi.org/10.21203/rs.3.rs-10952127/v1) | `papers/inference/99-other-inference-systems/2026-0ef8e5385098-reasoning-aware-error-bounded-kv-cache-compression-and-sparse-attention-for-long-context-llms.md` |
| 152 | 0 | research | DOI:10.5281/zenodo.22339206 | A Survey of Inference Processing Units for Large Language Model Inference: Chips, Systems, Algorithms, and Paradigms (2024–2026) | [primary](https://doi.org/10.5281/zenodo.22339206) | `papers/inference/99-other-inference-systems/2026-f8b8eb9da2fe-a-survey-of-inference-processing-units-for-large-language-model-inference-chips-systems-algorithms-and-paradigms-2024202.md` |
| 153 | 0 | research | SemanticScholar:7945684818786fcb32cf92bace2566d7d6bc8945 | LegoOS: A Disseminated, Distributed OS for Hardware Resource Disaggregation | [primary](https://www.semanticscholar.org/paper/7945684818786fcb32cf92bace2566d7d6bc8945) | `papers/inference/99-other-inference-systems/2026-6793b18ad544-legoos-a-disseminated-distributed-os-for-hardware-resource-disaggregation.md` |

## リスト入り判定待ち Discovery候補

未判定総数: **6875** / このworker向け: **500**

| # | score | identity | title | published | venue | citations | 関連数 | 系統候補 | source |
|---:|---:|---|---|---|---|---:|---:|---|---|
| 1 | 0 | arXiv:0902.0271 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/0902.0271) |
| 2 | 0 | arXiv:1202.3974 |  |  |  |  | 1 | MoE推論／ハイブリッドボンディング3Dメモリ／エキスパートキャッシュ／自己投機的デコード | [source](https://arxiv.org/abs/1202.3974) |
| 3 | 0 | arXiv:1205.6711 |  |  |  |  | 1 | kv-cache | [source](https://arxiv.org/abs/1205.6711) |
| 4 | 0 | arXiv:1211.3711 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1211.3711) |
| 5 | 0 | arXiv:1212.1609 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1212.1609) |
| 6 | 0 | arXiv:1307.2118 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/1307.2118) |
| 7 | 0 | arXiv:1312.6114 |  |  |  |  | 2 | serving-disaggregation | [source](https://arxiv.org/abs/1312.6114) |
| 8 | 0 | arXiv:1404.5997 |  |  |  |  | 2 | inference-systems, その他システム研究 | [source](https://arxiv.org/abs/1404.5997) |
| 9 | 0 | arXiv:1406.7362 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1406.7362) |
| 10 | 0 | arXiv:1410.0510 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1410.0510) |
| 11 | 0 | arXiv:1411.1792 |  |  |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1411.1792) |
| 12 | 0 | arXiv:1412.6553 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1412.6553) |
| 13 | 0 | arXiv:1502.05698 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1502.05698) |
| 14 | 0 | arXiv:1505.05571 |  |  |  |  | 1 | MoE数値再現性・決定論的推論・実行時互換性 | [source](https://arxiv.org/abs/1505.05571) |
| 15 | 0 | arXiv:1506.03099 |  |  |  |  | 1 | MoE expert offloading / predictive prefetch and cache management | [source](https://arxiv.org/abs/1506.03099) |
| 16 | 0 | arXiv:1507.06149 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1507.06149) |
| 17 | 0 | arXiv:1511.01837 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1511.01837) |
| 18 | 0 | arXiv:1511.05950 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1511.05950) |
| 19 | 0 | arXiv:1511.06744 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1511.06744) |
| 20 | 0 | arXiv:1511.08228 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1511.08228) |
| 21 | 0 | arXiv:1512.06890 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1512.06890) |
| 22 | 0 | arXiv:1602.01528 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/1602.01528) |
| 23 | 0 | arXiv:1602.02830 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1602.02830) |
| 24 | 0 | arXiv:1603.04467 |  |  |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1603.04467) |
| 25 | 0 | arXiv:1603.05691 |  |  |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/1603.05691) |
| 26 | 0 | arXiv:1604.01696 |  |  |  |  | 1 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1604.01696) |
| 27 | 0 | arXiv:1606.02891 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1606.02891) |
| 28 | 0 | arXiv:1607.06450 |  |  |  |  | 14 | Conditional Computation, GPU Kernel Framework, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, adaptive expert computation / compression; end-side sparse MoE, confidential inference / trusted execution environment / split inference / differential privacy, inference-systems, sparse attention / long-context Transformer, state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/1607.06450) |
| 29 | 0 | arXiv:1608.08710 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/1608.08710) |
| 30 | 0 | arXiv:1609.09548 |  |  |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/1609.09548) |
| 31 | 0 | arXiv:1611.01540 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/1611.01540) |
| 32 | 0 | arXiv:1611.01600 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1611.01600) |
| 33 | 0 | arXiv:1612.04426 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1612.04426) |
| 34 | 0 | arXiv:1701.03499 |  |  |  |  | 1 | NPU-PIM統合メモリ、近データ処理、LLM推論メモリ階層。NeuPIMs、IANUS、FACILの静的配置を動的実行へ拡張する。 | [source](https://arxiv.org/abs/1701.03499) |
| 35 | 0 | arXiv:1702.03044 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1702.03044) |
| 36 | 0 | arXiv:1703.03664 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1703.03664) |
| 37 | 0 | arXiv:1703.09844 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1703.09844) |
| 38 | 0 | arXiv:1704.04683 |  |  |  |  | 7 | MoE inference systems / expert parallelism / model compression / knowledge distillation, diffusion language models / masked diffusion / parallel decoding / AR-to-diffusion conversion, early-exit-offloading-self-speculative-decoding, moe-parallelism-communication | [source](https://arxiv.org/abs/1704.04683) |
| 39 | 0 | arXiv:1704.07535 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1704.07535) |
| 40 | 0 | arXiv:1705.06963 |  |  |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/1705.06963) |
| 41 | 0 | arXiv:1707.01873 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1707.01873) |
| 42 | 0 | arXiv:1709.00103 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1709.00103) |
| 43 | 0 | arXiv:1709.09582 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1709.09582) |
| 44 | 0 | arXiv:1710.10723 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1710.10723) |
| 45 | 0 | arXiv:1711.03936 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/1711.03936) |
| 46 | 0 | arXiv:1712.01312 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1712.01312) |
| 47 | 0 | arXiv:1712.07040 |  |  |  |  | 2 | KV Cache Offload / Recomputation | [source](https://arxiv.org/abs/1712.07040) |
| 48 | 0 | arXiv:1802.04730 |  |  |  |  | 2 | GPU Kernel Framework, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/1802.04730) |
| 49 | 0 | arXiv:1802.06509 |  |  |  |  | 1 | 分散学習 / 混合専門家モデル / 自動シャーディング / SPMD | [source](https://arxiv.org/abs/1802.06509) |
| 50 | 0 | arXiv:1802.08770 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1802.08770) |
| 51 | 0 | arXiv:1803.05407 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/1803.05407) |
| 52 | 0 | arXiv:1803.08494 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1803.08494) |
| 53 | 0 | arXiv:1804.06028 |  |  |  |  | 1 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/1804.06028) |
| 54 | 0 | arXiv:1805.00907 |  |  |  |  | 2 | GPU Kernel Framework, inference-systems | [source](https://arxiv.org/abs/1805.00907) |
| 55 | 0 | arXiv:1805.06085 |  |  |  |  | 7 | LLM inference surveys、roofline performance analysis, LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, cpu-ssd-offload, inference-systems, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/1805.06085) |
| 56 | 0 | arXiv:1806.00187 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1806.00187) |
| 57 | 0 | arXiv:1806.08159 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/1806.08159) |
| 58 | 0 | arXiv:1807.09810 |  |  |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/1807.09810) |
| 59 | 0 | arXiv:1808.04444 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1808.04444) |
| 60 | 0 | arXiv:1808.08745 |  |  |  |  | 13 | KV cache eviction / heavy hitters / sparse attention / efficient inference, Offload / Hierarchical Memory, inference-systems, llm-serving-scheduling-disaggregation, offload-hierarchical-memory, オフロード／階層メモリ, 投機的デコード・バッチ推論, 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1808.08745) |
| 61 | 0 | arXiv:1808.10792 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1808.10792) |
| 62 | 0 | arXiv:1809.08887 |  |  |  |  | 3 | 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/1809.08887) |
| 63 | 0 | arXiv:1809.11096 |  |  |  |  | 1 | kv-cache-optimization-compression | [source](https://arxiv.org/abs/1809.11096) |
| 64 | 0 | arXiv:1810.03264 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1810.03264) |
| 65 | 0 | arXiv:1810.09305 |  |  |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/1810.09305) |
| 66 | 0 | arXiv:1811.00783 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1811.00783) |
| 67 | 0 | arXiv:1811.02883 |  |  |  |  | 6 | GPUシミュレーション・AIカーネル・ハードウェア/ソフトウェア協調設計, LLM inference simulation / disaggregated serving / performance modeling, Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, hardware-accelerators, inference-systems | [source](https://arxiv.org/abs/1811.02883) |
| 68 | 0 | arXiv:1811.05233 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/1811.05233) |
| 69 | 0 | arXiv:1812.01608 |  |  |  |  | 1 | sparse attention / long-context Transformer | [source](https://arxiv.org/abs/1812.01608) |
| 70 | 0 | arXiv:1901.03429 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1901.03429) |
| 71 | 0 | arXiv:1901.08634 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1901.08634) |
| 72 | 0 | arXiv:1902.03383 |  |  |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/1902.03383) |
| 73 | 0 | arXiv:1902.06822 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1902.06822) |
| 74 | 0 | arXiv:1902.09506 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/1902.09506) |
| 75 | 0 | arXiv:1903.00089 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/1903.00089) |
| 76 | 0 | arXiv:1903.04611 |  |  |  |  | 1 | 01-offload-hierarchical-memory | [source](https://arxiv.org/abs/1903.04611) |
| 77 | 0 | arXiv:1903.09588 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1903.09588) |
| 78 | 0 | arXiv:1904.01145 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/1904.01145) |
| 79 | 0 | arXiv:1904.06376 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1904.06376) |
| 80 | 0 | arXiv:1904.09675 |  |  |  |  | 2 | other-inference-systems | [source](https://arxiv.org/abs/1904.09675) |
| 81 | 0 | arXiv:1905.00537 |  |  |  |  | 2 | MoE inference systems / expert parallelism / model compression / knowledge distillation | [source](https://arxiv.org/abs/1905.00537) |
| 82 | 0 | arXiv:1905.05702 |  |  |  |  | 3 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計, Sparse Attention, inference-systems | [source](https://arxiv.org/abs/1905.05702) |
| 83 | 0 | arXiv:1905.07799 |  |  |  |  | 2 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/1905.07799) |
| 84 | 0 | arXiv:1905.11259 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1905.11259) |
| 85 | 0 | arXiv:1906.00300 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1906.00300) |
| 86 | 0 | arXiv:1906.02041 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1906.02041) |
| 87 | 0 | arXiv:1906.04284 |  |  |  |  | 2 | 10-kv-cache-offload-recomputation, Sparse Attention | [source](https://arxiv.org/abs/1906.04284) |
| 88 | 0 | arXiv:1906.05714 |  |  |  |  | 1 | 大規模言語モデル重み量子化 / 混合精度 / 疎量子化 | [source](https://arxiv.org/abs/1906.05714) |
| 89 | 0 | arXiv:1906.08237 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1906.08237) |
| 90 | 0 | arXiv:1906.12085 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1906.12085) |
| 91 | 0 | arXiv:1907.02711 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1907.02711) |
| 92 | 0 | arXiv:1907.06627 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1907.06627) |
| 93 | 0 | arXiv:1908.03903 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1908.03903) |
| 94 | 0 | arXiv:1908.08167 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1908.08167) |
| 95 | 0 | arXiv:1908.09355 |  |  |  |  | 3 | Conditional Computation | [source](https://arxiv.org/abs/1908.09355) |
| 96 | 0 | arXiv:1908.10084 |  |  |  |  | 3 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/1908.10084) |
| 97 | 0 | arXiv:1908.11775 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1908.11775) |
| 98 | 0 | arXiv:1909.03186 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1909.03186) |
| 99 | 0 | arXiv:1909.06708 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, inference-systems | [source](https://arxiv.org/abs/1909.06708) |
| 100 | 0 | arXiv:1909.10351 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/1909.10351) |
| 101 | 0 | arXiv:1909.13271 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/1909.13271) |
| 102 | 0 | arXiv:1910.04732 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/1910.04732) |
| 103 | 0 | arXiv:1910.06188 |  |  |  |  | 3 | Weight Quantization / Compression, dense-to-MoE conversion / conditional FFN computation / expert routing, inference-systems | [source](https://arxiv.org/abs/1910.06188) |
| 104 | 0 | arXiv:1910.07475 |  |  |  |  | 1 | 端末LLM・ニューロン疎性・階層メモリ推論 | [source](https://arxiv.org/abs/1910.07475) |
| 105 | 0 | arXiv:1910.13461 |  |  |  |  | 5 | inference-systems | [source](https://arxiv.org/abs/1910.13461) |
| 106 | 0 | arXiv:1911.02685 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.02685) |
| 107 | 0 | arXiv:1911.03584 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.03584) |
| 108 | 0 | arXiv:1911.03894 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1911.03894) |
| 109 | 0 | arXiv:1911.04997 |  |  |  |  | 1 | MoE expert parallelism / dynamic load balancing / expert prefetching | [source](https://arxiv.org/abs/1911.04997) |
| 110 | 0 | arXiv:1911.08772 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/1911.08772) |
| 111 | 0 | arXiv:1912.00818 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1912.00818) |
| 112 | 0 | arXiv:1912.10077 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/1912.10077) |
| 113 | 0 | arXiv:2001.01969 |  |  |  |  | 1 | Conditional Computation | [source](https://arxiv.org/abs/2001.01969) |
| 114 | 0 | arXiv:2001.04698 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2001.04698) |
| 115 | 0 | arXiv:2002.00762 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.00762) |
| 116 | 0 | arXiv:2002.07376 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2002.07376) |
| 117 | 0 | arXiv:2002.08240 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.08240) |
| 118 | 0 | arXiv:2002.09434 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2002.09434) |
| 119 | 0 | arXiv:2002.10941 |  |  |  |  | 1 | Sparse Attention | [source](https://arxiv.org/abs/2002.10941) |
| 120 | 0 | arXiv:2002.11985 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2002.11985) |
| 121 | 0 | arXiv:2003.03033 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.03033) |
| 122 | 0 | arXiv:2003.07013 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.07013) |
| 123 | 0 | arXiv:2003.11535 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2003.11535) |
| 124 | 0 | arXiv:2004.02984 |  |  |  |  | 4 | Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2004.02984) |
| 125 | 0 | arXiv:2004.05986 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2004.05986) |
| 126 | 0 | arXiv:2004.08900 |  |  |  |  | 2 | その他システム研究 | [source](https://arxiv.org/abs/2004.08900) |
| 127 | 0 | arXiv:2004.11867 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2004.11867) |
| 128 | 0 | arXiv:2004.14769 |  |  |  |  | 1 | MoE expert pruning / trajectory-aware compression / task-specific MoE compression | [source](https://arxiv.org/abs/2004.14769) |
| 129 | 0 | arXiv:2005.00770 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2005.00770) |
| 130 | 0 | arXiv:2005.04305 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2005.04305) |
| 131 | 0 | arXiv:2005.08025 |  |  |  |  | 1 | serving-scheduling | [source](https://arxiv.org/abs/2005.08025) |
| 132 | 0 | arXiv:2005.14187 |  |  |  |  | 2 | inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2005.14187) |
| 133 | 0 | arXiv:2006.03669 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2006.03669) |
| 134 | 0 | arXiv:2006.08748 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2006.08748) |
| 135 | 0 | arXiv:2006.11316 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2006.11316) |
| 136 | 0 | arXiv:2006.16362 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2006.16362) |
| 137 | 0 | arXiv:2007.01852 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2007.01852) |
| 138 | 0 | arXiv:2007.04825 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2007.04825) |
| 139 | 0 | arXiv:2007.12626 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2007.12626) |
| 140 | 0 | arXiv:2008.00401 |  |  |  |  | 1 | MoE inference / expert pruning / language-specific expert specialization | [source](https://arxiv.org/abs/2008.00401) |
| 141 | 0 | arXiv:2008.05221 |  |  |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2008.05221) |
| 142 | 0 | arXiv:2009.05647 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2009.05647) |
| 143 | 0 | arXiv:2009.07118 |  |  |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2009.07118) |
| 144 | 0 | arXiv:2009.07268 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2009.07268) |
| 145 | 0 | arXiv:2009.08065 |  |  |  |  | 1 | large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency | [source](https://arxiv.org/abs/2009.08065) |
| 146 | 0 | arXiv:2009.12812 |  |  |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2009.12812) |
| 147 | 0 | arXiv:2009.14167 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2009.14167) |
| 148 | 0 | arXiv:2010.02502 |  |  |  |  | 2 | diffusion LLM / mixture-of-experts / adaptive expert routing / memory-bound inference | [source](https://arxiv.org/abs/2010.02502) |
| 149 | 0 | arXiv:2010.03093 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.03093) |
| 150 | 0 | arXiv:2010.03768 |  |  |  |  | 2 | augmented LLM serving / KV cache management / predictive scheduling / vLLM, inference-systems | [source](https://arxiv.org/abs/2010.03768) |
| 151 | 0 | arXiv:2010.05478 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2010.05478) |
| 152 | 0 | arXiv:2010.11125 |  |  |  |  | 1 | 分散MoE学習 / ZeRO / CPUオフロード / 多次元並列 | [source](https://arxiv.org/abs/2010.11125) |
| 153 | 0 | arXiv:2010.14701 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2010.14701) |
| 154 | 0 | arXiv:2011.00943 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2011.00943) |
| 155 | 0 | arXiv:2011.04006 |  |  |  |  | 2 | CPU長文推論・近似注意 | [source](https://arxiv.org/abs/2011.04006) |
| 156 | 0 | arXiv:2011.06327 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2011.06327) |
| 157 | 0 | arXiv:2011.13456 |  |  |  |  | 1 | Other Inference Systems / Lossless Parallel Decoding | [source](https://arxiv.org/abs/2011.13456) |
| 158 | 0 | arXiv:2012.07463 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2012.07463) |
| 159 | 0 | arXiv:2012.15613 |  |  |  |  | 1 | kv-cache-memory-management | [source](https://arxiv.org/abs/2012.15613) |
| 160 | 0 | arXiv:2012.15828 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2012.15828) |
| 161 | 0 | arXiv:2101.00234 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2101.00234) |
| 162 | 0 | arXiv:2101.08744 |  |  |  |  | 1 | MoE inference / on-device LLM / expert offloading / expert caching | [source](https://arxiv.org/abs/2101.08744) |
| 163 | 0 | arXiv:2101.11986 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2101.11986) |
| 164 | 0 | arXiv:2102.03315 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2102.03315) |
| 165 | 0 | arXiv:2102.07831 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2102.07831) |
| 166 | 0 | arXiv:2102.08602 |  |  |  |  | 2 | training-memory-systems, 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2102.08602) |
| 167 | 0 | arXiv:2102.11972 |  |  |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2102.11972) |
| 168 | 0 | arXiv:2103.02143 |  |  |  |  | 2 | CPU長文推論・近似注意, inference-systems | [source](https://arxiv.org/abs/2103.02143) |
| 169 | 0 | arXiv:2103.03841 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2103.03841) |
| 170 | 0 | arXiv:2103.10427 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2103.10427) |
| 171 | 0 | arXiv:2104.06022 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2104.06022) |
| 172 | 0 | arXiv:2104.07091 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2104.07091) |
| 173 | 0 | arXiv:2104.08663 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2104.08663) |
| 174 | 0 | arXiv:2104.12470 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2104.12470) |
| 175 | 0 | arXiv:2105.05233 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2105.05233) |
| 176 | 0 | arXiv:2105.08306 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2105.08306) |
| 177 | 0 | arXiv:2105.11098 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2105.11098) |
| 178 | 0 | arXiv:2105.13878 |  |  |  |  | 3 | Conditional Computation | [source](https://arxiv.org/abs/2105.13878) |
| 179 | 0 | arXiv:2105.14528 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2105.14528) |
| 180 | 0 | arXiv:2106.03650 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2106.03650) |
| 181 | 0 | arXiv:2106.04554 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2106.04554) |
| 182 | 0 | arXiv:2106.06168 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2106.06168) |
| 183 | 0 | arXiv:2106.08254 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2106.08254) |
| 184 | 0 | arXiv:2106.15339 |  |  |  |  | 1 | MoE推論／CPU-GPU協調オフロード／階層メモリ／性能モデル／高スループットバッチ推論 | [source](https://arxiv.org/abs/2106.15339) |
| 185 | 0 | arXiv:2107.00652 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2107.00652) |
| 186 | 0 | arXiv:2107.03006 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.03006) |
| 187 | 0 | arXiv:2107.07566 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2107.07566) |
| 188 | 0 | arXiv:2107.11906 |  |  |  |  | 2 | inference-systems, long-context inference / dynamic sparse attention / hierarchical attention / post-hoc attention acceleration | [source](https://arxiv.org/abs/2107.11906) |
| 189 | 0 | arXiv:2108.03298 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2108.03298) |
| 190 | 0 | arXiv:2108.08877 |  |  |  |  | 1 | 07-kv-キャッシュ-optimization-compression | [source](https://arxiv.org/abs/2108.08877) |
| 191 | 0 | arXiv:2109.00859 |  |  |  |  | 1 | その他システム研究 | [source](https://arxiv.org/abs/2109.00859) |
| 192 | 0 | arXiv:2109.04404 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2109.04404) |
| 193 | 0 | arXiv:2109.05472 |  |  |  |  | 1 | 推論基盤比較・Pareto最適化・量子化・KV cache・speculative decoding・batching | [source](https://arxiv.org/abs/2109.05472) |
| 194 | 0 | arXiv:2109.08668 |  |  |  |  | 4 | 99-other-inference-systems, Conditional Computation, inference-systems | [source](https://arxiv.org/abs/2109.08668) |
| 195 | 0 | arXiv:2109.11067 |  |  |  |  | 2 | LLM Serving / Scheduling / Disaggregation, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2109.11067) |
| 196 | 0 | arXiv:2109.15082 |  |  |  |  | 1 | survey-low-bit-llm | [source](https://arxiv.org/abs/2109.15082) |
| 197 | 0 | arXiv:2110.03742 |  |  |  |  | 7 | Edge／on-device MoE, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, MoE inference / expert pruning / language-specific expert specialization, inference-systems, large-scale LLM inference / tensor partitioning / TPU serving / KV-cache memory efficiency, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2110.03742) |
| 198 | 0 | arXiv:2110.06821 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.06821) |
| 199 | 0 | arXiv:2110.07814 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.07814) |
| 200 | 0 | arXiv:2110.08499 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2110.08499) |
| 201 | 0 | arXiv:2110.12894 |  |  |  |  | 2 | Conditional Computation | [source](https://arxiv.org/abs/2110.12894) |
| 202 | 0 | arXiv:2110.15191 |  |  |  |  | 2 | distributed attention / sequence parallelism / blockwise attention / long-context transformers, training-memory-systems | [source](https://arxiv.org/abs/2110.15191) |
| 203 | 0 | arXiv:2111.00680 |  |  |  |  | 1 | offload-hierarchical-memory | [source](https://arxiv.org/abs/2111.00680) |
| 204 | 0 | arXiv:2111.01697 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2111.01697) |
| 205 | 0 | arXiv:2111.08915 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2111.08915) |
| 206 | 0 | arXiv:2112.00029 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2112.00029) |
| 207 | 0 | arXiv:2112.02052 |  |  |  |  | 1 | unstructured sparsity / GPU inference kernels | [source](https://arxiv.org/abs/2112.02052) |
| 208 | 0 | arXiv:2112.03097 |  |  |  |  | 1 | MoE routing / expert offloading / temporal expert persistence | [source](https://arxiv.org/abs/2112.03097) |
| 209 | 0 | arXiv:2112.07210 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2112.07210) |
| 210 | 0 | arXiv:2112.10508 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2112.10508) |
| 211 | 0 | arXiv:2112.11446 |  |  |  |  | 8 | Adaptive computation／cache-aware MoE, LLM Serving / Scheduling / Disaggregation, Speculative Decoding, オフロード／階層メモリ, 投機的デコード / 分布保存型デコード高速化, 推論ベンチマーク・推論大規模言語モデルのサービング評価 | [source](https://arxiv.org/abs/2112.11446) |
| 212 | 0 | arXiv:2112.14938 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2112.14938) |
| 213 | 0 | arXiv:2201.06618 |  |  |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2201.06618) |
| 214 | 0 | arXiv:2201.11227 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2201.11227) |
| 215 | 0 | arXiv:2202.01279 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2202.01279) |
| 216 | 0 | arXiv:2202.05239 |  |  |  |  | 1 | Weight Quantization / Compression | [source](https://arxiv.org/abs/2202.05239) |
| 217 | 0 | arXiv:2202.05924 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2202.05924) |
| 218 | 0 | arXiv:2202.07848 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2202.07848) |
| 219 | 0 | arXiv:2202.10447 |  |  |  |  | 1 | 注意カーネル最適化 / 入出力認識アルゴリズム / 長文脈 / GPUメモリ階層 | [source](https://arxiv.org/abs/2202.10447) |
| 220 | 0 | arXiv:2203.00091 |  |  |  |  | 1 | 13-sparse-attention | [source](https://arxiv.org/abs/2203.00091) |
| 221 | 0 | arXiv:2203.02073 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2203.02073) |
| 222 | 0 | arXiv:2203.05482 |  |  |  |  | 1 | MoE圧縮 / expert pruning / expert merging / post-compression adjustment | [source](https://arxiv.org/abs/2203.05482) |
| 223 | 0 | arXiv:2203.06569 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.06569) |
| 224 | 0 | arXiv:2203.08913 |  |  |  |  | 6 | LLM inference surveys、roofline performance analysis, inference-systems, survey-long-context-serving, 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2203.08913) |
| 225 | 0 | arXiv:2203.10705 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2203.10705) |
| 226 | 0 | arXiv:2203.14680 |  |  |  |  | 1 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング | [source](https://arxiv.org/abs/2203.14680) |
| 227 | 0 | arXiv:2204.00595 |  |  |  |  | 1 | GPU Kernel Framework | [source](https://arxiv.org/abs/2204.00595) |
| 228 | 0 | arXiv:2204.03324 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2204.03324) |
| 229 | 0 | arXiv:2204.05999 |  |  |  |  | 2 | inference-systems, 大規模言語モデルによるカーネル最適化、配備状況を考慮した推論最適化、エージェント型コード最適化 | [source](https://arxiv.org/abs/2204.05999) |
| 230 | 0 | arXiv:2204.07675 |  |  |  |  | 3 | dense-to-MoE restructuring / activation sparsity / analytical routing / hierarchical MoE, training-memory-systems | [source](https://arxiv.org/abs/2204.07675) |
| 231 | 0 | arXiv:2204.09179 |  |  |  |  | 5 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning, Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM, MoE inference / task-specific expert pruning / sparse-to-dense conversion | [source](https://arxiv.org/abs/2204.09179) |
| 232 | 0 | arXiv:2204.13807 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2204.13807) |
| 233 | 0 | arXiv:2205.02209 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.02209) |
| 234 | 0 | arXiv:2205.05131 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2205.05131) |
| 235 | 0 | arXiv:2205.07324 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2205.07324) |
| 236 | 0 | arXiv:2205.10569 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2205.10569) |
| 237 | 0 | arXiv:2205.11465 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.11465) |
| 238 | 0 | arXiv:2205.12255 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.12255) |
| 239 | 0 | arXiv:2205.12701 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2205.12701) |
| 240 | 0 | arXiv:2205.14217 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2205.14217) |
| 241 | 0 | arXiv:2206.03126 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2206.03126) |
| 242 | 0 | arXiv:2206.08916 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2206.08916) |
| 243 | 0 | arXiv:2206.14858 |  |  |  |  | 2 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2206.14858) |
| 244 | 0 | arXiv:2207.05952 |  |  |  |  | 1 | Mixture-of-Experts / random routing / self-slimmable networks / dropout regularization | [source](https://arxiv.org/abs/2207.05952) |
| 245 | 0 | arXiv:2207.09238 |  |  |  |  | 1 | other-inference-systems | [source](https://arxiv.org/abs/2207.09238) |
| 246 | 0 | arXiv:2207.12598 |  |  |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2207.12598) |
| 247 | 0 | arXiv:2208.03299 |  |  |  |  | 3 | KVキャッシュ再利用／圧縮／ネットワーク転送 | [source](https://arxiv.org/abs/2208.03299) |
| 248 | 0 | arXiv:2208.05395 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2208.05395) |
| 249 | 0 | arXiv:2208.08124 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2208.08124) |
| 250 | 0 | arXiv:2208.10041 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2208.10041) |
| 251 | 0 | arXiv:2208.11663 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2208.11663) |
| 252 | 0 | arXiv:2209.06794 |  |  |  |  | 1 | training-memory-systems | [source](https://arxiv.org/abs/2209.06794) |
| 253 | 0 | arXiv:2209.08167 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2209.08167) |
| 254 | 0 | arXiv:2209.11429 |  |  |  |  | 1 | agentic serving / workflow-aware scheduling / memory-aware dispatch | [source](https://arxiv.org/abs/2209.11429) |
| 255 | 0 | arXiv:2209.12951 |  |  |  |  | 1 | GPU Kernel Framework | [source](https://arxiv.org/abs/2209.12951) |
| 256 | 0 | arXiv:2209.15001 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2209.15001) |
| 257 | 0 | arXiv:2209.15430 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2209.15430) |
| 258 | 0 | arXiv:2210.02441 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.02441) |
| 259 | 0 | arXiv:2210.03052 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.03052) |
| 260 | 0 | arXiv:2210.03871 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.03871) |
| 261 | 0 | arXiv:2210.06423 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.06423) |
| 262 | 0 | arXiv:2210.07316 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2210.07316) |
| 263 | 0 | arXiv:2210.08674 |  |  |  |  | 1 | LLM routing、hybrid inference、quality-aware model selection | [source](https://arxiv.org/abs/2210.08674) |
| 264 | 0 | arXiv:2210.10340 |  |  |  |  | 1 | state space models / selective SSM / recurrent inference / hardware-aware sequence modeling | [source](https://arxiv.org/abs/2210.10340) |
| 265 | 0 | arXiv:2210.11794 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2210.11794) |
| 266 | 0 | arXiv:2210.13438 |  |  |  |  | 2 | 11-llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2210.13438) |
| 267 | 0 | arXiv:2210.14793 |  |  |  |  | 1 | Edge／on-device MoE | [source](https://arxiv.org/abs/2210.14793) |
| 268 | 0 | arXiv:2211.00107 |  |  |  |  | 1 | Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2211.00107) |
| 269 | 0 | arXiv:2211.01095 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2211.01095) |
| 270 | 0 | arXiv:2211.05322 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.05322) |
| 271 | 0 | arXiv:2211.06033 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2211.06033) |
| 272 | 0 | arXiv:2211.08403 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2211.08403) |
| 273 | 0 | arXiv:2211.10435 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2211.10435) |
| 274 | 0 | arXiv:2211.12588 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2211.12588) |
| 275 | 0 | arXiv:2211.16750 |  |  |  |  | 2 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2211.16750) |
| 276 | 0 | arXiv:2212.01378 |  |  |  |  | 2 | Adaptive Expert Computation / Compression, Mixture-of-Experts / differentiable routing / parameter merging / modular learning | [source](https://arxiv.org/abs/2212.01378) |
| 277 | 0 | arXiv:2212.04037 |  |  |  |  | 1 | LLM Serving / Scheduling / Disaggregation | [source](https://arxiv.org/abs/2212.04037) |
| 278 | 0 | arXiv:2212.05191 |  |  |  |  | 1 | MoE動的クラスタリング / shared-base low-rank residual / hierarchical routing / expert offloading | [source](https://arxiv.org/abs/2212.05191) |
| 279 | 0 | arXiv:2212.06713 |  |  |  |  | 1 | Long-context serving / KV cache benchmark | [source](https://arxiv.org/abs/2212.06713) |
| 280 | 0 | arXiv:2212.08153 |  |  |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2212.08153) |
| 281 | 0 | arXiv:2212.10403 |  |  |  |  | 2 | attention-FC disaggregation / DIMM-PIM / KV-cache capacity-bandwidth scaling / heterogeneous inference | [source](https://arxiv.org/abs/2212.10403) |
| 282 | 0 | arXiv:2212.10511 |  |  |  |  | 1 | 鍵・値キャッシュ再利用 / 検索拡張生成 / 長文脈推論 | [source](https://arxiv.org/abs/2212.10511) |
| 283 | 0 | arXiv:2212.10560 |  |  |  |  | 7 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停, KV Cache Offload / Recomputation, LLM Serving / Scheduling / Disaggregation, adaptive-expert-computation-compression, inference-systems | [source](https://arxiv.org/abs/2212.10560) |
| 284 | 0 | arXiv:2212.11468 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2212.11468) |
| 285 | 0 | arXiv:2212.14052 |  |  |  |  | 4 | inference-systems | [source](https://arxiv.org/abs/2212.14052) |
| 286 | 0 | arXiv:2301.02828 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.02828) |
| 287 | 0 | arXiv:2301.05217 |  |  |  |  | 1 | KV cache sparsity / paged attention / query-aware selection / LLM serving | [source](https://arxiv.org/abs/2301.05217) |
| 288 | 0 | arXiv:2301.06672 |  |  |  |  | 1 | 近メモリ処理 / HBMベースダイ / 重みのみ量子化 / 逆量子化 / LLM推論アクセラレーション | [source](https://arxiv.org/abs/2301.06672) |
| 289 | 0 | arXiv:2301.08721 |  |  |  |  | 2 | inference-systems, kv-cache-memory | [source](https://arxiv.org/abs/2301.08721) |
| 290 | 0 | arXiv:2301.11233 |  |  |  |  | 2 | Weight Quantization / Compression, inference-systems | [source](https://arxiv.org/abs/2301.11233) |
| 291 | 0 | arXiv:2301.12132 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2301.12132) |
| 292 | 0 | arXiv:2301.12900 |  |  |  |  | 1 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2301.12900) |
| 293 | 0 | arXiv:2302.00083 |  |  |  |  | 5 |  | [source](https://arxiv.org/abs/2302.00083) |
| 294 | 0 | arXiv:2302.02676 |  |  |  |  | 1 | training-memory-systems | [source](https://arxiv.org/abs/2302.02676) |
| 295 | 0 | arXiv:2302.04089 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2302.04089) |
| 296 | 0 | arXiv:2302.06476 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.06476) |
| 297 | 0 | arXiv:2302.07080 |  |  |  |  | 1 | Offload / Hierarchical Memory | [source](https://arxiv.org/abs/2302.07080) |
| 298 | 0 | arXiv:2302.09210 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2302.09210) |
| 299 | 0 | arXiv:2302.09664 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.09664) |
| 300 | 0 | arXiv:2302.10870 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2302.10870) |
| 301 | 0 | arXiv:2302.12066 |  |  |  |  | 1 | foundation-model deployment benchmarking / hardware-aware inference profiling / edge AI | [source](https://arxiv.org/abs/2302.12066) |
| 302 | 0 | arXiv:2302.12480 |  |  |  |  | 1 | Adaptive Expert Computation / Compression | [source](https://arxiv.org/abs/2302.12480) |
| 303 | 0 | arXiv:2302.14502 |  |  |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2302.14502) |
| 304 | 0 | arXiv:2303.00001 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.00001) |
| 305 | 0 | arXiv:2303.02141 |  |  |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2303.02141) |
| 306 | 0 | arXiv:2303.04048 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.04048) |
| 307 | 0 | arXiv:2303.05510 |  |  |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2303.05510) |
| 308 | 0 | arXiv:2303.06296 |  |  |  |  | 1 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2303.06296) |
| 309 | 0 | arXiv:2303.07895 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2303.07895) |
| 310 | 0 | arXiv:2303.10158 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.10158) |
| 311 | 0 | arXiv:2303.11366 |  |  |  |  | 2 | inference-systems, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2303.11366) |
| 312 | 0 | arXiv:2303.12557 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.12557) |
| 313 | 0 | arXiv:2303.14524 |  |  |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2303.14524) |
| 314 | 0 | arXiv:2303.16199 |  |  |  |  | 2 | inference-systems, 重み専用量子化 / 推論カーネル | [source](https://arxiv.org/abs/2303.16199) |
| 315 | 0 | arXiv:2303.16854 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.16854) |
| 316 | 0 | arXiv:2303.17580 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2303.17580) |
| 317 | 0 | arXiv:2304.01089 |  |  |  |  | 19 | Conditional Computation, Expert Prefetch, LLM inference surveys、roofline performance analysis, LLM推論メモリ階層／無損失圧縮／KVキャッシュ圧縮／動的量子化／メモリ制御器協調設計, MoE inference / on-device LLM / expert offloading / expert caching, Quantization × MoE × Offload, Weight Quantization / Compression, inference-systems, kv-cache-memory, survey-low-bit-llm, 端末内LLM推論・三次元NAND・フラッシュ内計算・KVキャッシュ配置, 端末内LLM推論／フラッシュ計算／チップレット／重み退避 | [source](https://arxiv.org/abs/2304.01089) |
| 318 | 0 | arXiv:2304.01468 |  |  |  |  | 1 | SLO-aware LLM serving scheduling | [source](https://arxiv.org/abs/2304.01468) |
| 319 | 0 | arXiv:2304.02017 |  |  |  |  | 2 | Speculative Decoding / Parallel Inference Systems | [source](https://arxiv.org/abs/2304.02017) |
| 320 | 0 | arXiv:2304.03208 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2304.03208) |
| 321 | 0 | arXiv:2304.04487 |  |  |  |  | 12 | LLM inference surveys、roofline performance analysis, Speculative Decoding, inference-systems, survey-speculative-decoding, エージェント駆動システム最適化／LLMサービング基盤自動生成／対象特化実行系, 投機的デコード / 自己投機的デコード / 層スキップ | [source](https://arxiv.org/abs/2304.04487) |
| 322 | 0 | arXiv:2304.04675 |  |  |  |  | 1 | LLM Serving / Reasoning | [source](https://arxiv.org/abs/2304.04675) |
| 323 | 0 | arXiv:2304.08243 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2304.08243) |
| 324 | 0 | arXiv:2304.09433 |  |  |  |  | 2 | LLM serving scheduling / hybrid QoS / KV cache management | [source](https://arxiv.org/abs/2304.09433) |
| 325 | 0 | arXiv:2304.12244 |  |  |  |  | 4 | inference-systems, multi-model LLM serving / prompt routing / resource allocation | [source](https://arxiv.org/abs/2304.12244) |
| 326 | 0 | arXiv:2304.15004 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2304.15004) |
| 327 | 0 | arXiv:2305.01505 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2305.01505) |
| 328 | 0 | arXiv:2305.04859 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.04859) |
| 329 | 0 | arXiv:2305.06942 |  |  |  |  | 2 | inference-systems, kernel-runtime-compilation | [source](https://arxiv.org/abs/2305.06942) |
| 330 | 0 | arXiv:2305.07759 |  |  |  |  | 2 | KV cache sparsity / paged attention / query-aware selection / LLM serving, edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.07759) |
| 331 | 0 | arXiv:2305.09098 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2305.09098) |
| 332 | 0 | arXiv:2305.11175 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.11175) |
| 333 | 0 | arXiv:2305.13246 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.13246) |
| 334 | 0 | arXiv:2305.13655 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.13655) |
| 335 | 0 | arXiv:2305.14160 |  |  |  |  | 2 | KV-cache compression / attention-based token selection / long-context inference | [source](https://arxiv.org/abs/2305.14160) |
| 336 | 0 | arXiv:2305.14387 |  |  |  |  | 1 | speculative-decoding | [source](https://arxiv.org/abs/2305.14387) |
| 337 | 0 | arXiv:2305.14625 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.14625) |
| 338 | 0 | arXiv:2305.14806 |  |  |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2305.14806) |
| 339 | 0 | arXiv:2305.14992 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.14992) |
| 340 | 0 | arXiv:2305.15294 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2305.15294) |
| 341 | 0 | arXiv:2305.15838 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.15838) |
| 342 | 0 | arXiv:2305.16380 |  |  |  |  | 1 | KVキャッシュ圧縮 / 量子化 / 推論メモリ最適化 | [source](https://arxiv.org/abs/2305.16380) |
| 343 | 0 | arXiv:2305.17126 |  |  |  |  | 1 | 投機的デコード / 知識蒸留 / ドラフトモデル整合 | [source](https://arxiv.org/abs/2305.17126) |
| 344 | 0 | arXiv:2305.17455 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.17455) |
| 345 | 0 | arXiv:2305.18403 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2305.18403) |
| 346 | 0 | arXiv:2305.18846 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2305.18846) |
| 347 | 0 | arXiv:2305.19466 |  |  |  |  | 3 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2305.19466) |
| 348 | 0 | arXiv:2306.00317 |  |  |  |  | 3 | Quantization × MoE × Offload, hardware-accelerators, inference-systems | [source](https://arxiv.org/abs/2306.00317) |
| 349 | 0 | arXiv:2306.01200 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.01200) |
| 350 | 0 | arXiv:2306.02295 |  |  |  |  | 2 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02295) |
| 351 | 0 | arXiv:2306.02896 |  |  |  |  | 1 | KV cache eviction / heavy hitters / sparse attention / efficient inference | [source](https://arxiv.org/abs/2306.02896) |
| 352 | 0 | arXiv:2306.03805 |  |  |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction | [source](https://arxiv.org/abs/2306.03805) |
| 353 | 0 | arXiv:2306.04757 |  |  |  |  | 1 | オフロード／階層メモリ | [source](https://arxiv.org/abs/2306.04757) |
| 354 | 0 | arXiv:2306.05424 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2306.05424) |
| 355 | 0 | arXiv:2306.06624 |  |  |  |  | 1 | KVキャッシュ再利用 / エージェント型LLM / ツール呼出し / KV圧縮 / 構造的枝刈り | [source](https://arxiv.org/abs/2306.06624) |
| 356 | 0 | arXiv:2306.09212 |  |  |  |  | 9 | Mixture-of-Experts / dynamic expert activation / heterogeneous experts / sparse upcycling, MoE compression / expert matrix decomposition / shared basis reparameterization, MoE compression / structured pruning / expert merging / knowledge distillation / Qwen3-Next, adaptive-expert-computation-compression, dynamic top-k MoE routing / load-balanced routing / long-context hybrid attention / physical AI foundation models | [source](https://arxiv.org/abs/2306.09212) |
| 357 | 0 | arXiv:2306.11089 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2306.11089) |
| 358 | 0 | arXiv:2306.12420 |  |  |  |  | 1 | multi-model serving / disaggregated serving / cross-model KV reuse | [source](https://arxiv.org/abs/2306.12420) |
| 359 | 0 | arXiv:2306.13596 |  |  |  |  | 2 | KVキャッシュ圧縮 / 注意疎性 / 値ベクトル考慮型追放 / 厳密予算キャッシュ設計 | [source](https://arxiv.org/abs/2306.13596) |
| 360 | 0 | arXiv:2306.16837 |  |  |  |  | 1 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2306.16837) |
| 361 | 0 | arXiv:2307.00198 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.00198) |
| 362 | 0 | arXiv:2307.02419 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.02419) |
| 363 | 0 | arXiv:2307.02839 |  |  |  |  | 1 | CPU/GPU階層メモリ・モデル重みオフロード・SLO指向サービング・PCIe帯域調停 | [source](https://arxiv.org/abs/2307.02839) |
| 364 | 0 | arXiv:2307.04251 |  |  |  |  | 1 | llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2307.04251) |
| 365 | 0 | arXiv:2307.05300 |  |  |  |  | 1 | agentic LLM serving / prefix caching / hierarchical KV cache / workflow-aware scheduling | [source](https://arxiv.org/abs/2307.05300) |
| 366 | 0 | arXiv:2307.06962 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.06962) |
| 367 | 0 | arXiv:2307.07697 |  |  |  |  | 1 | Graph-CoT / multi-agent serving / KV-cache reuse | [source](https://arxiv.org/abs/2307.07697) |
| 368 | 0 | arXiv:2307.08189 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2307.08189) |
| 369 | 0 | arXiv:2307.08941 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2307.08941) |
| 370 | 0 | arXiv:2307.10485 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2307.10485) |
| 371 | 0 | arXiv:2307.12169 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2307.12169) |
| 372 | 0 | arXiv:2307.12856 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.12856) |
| 373 | 0 | arXiv:2307.14984 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2307.14984) |
| 374 | 0 | arXiv:2307.16883 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2307.16883) |
| 375 | 0 | arXiv:2308.02019 |  |  |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2308.02019) |
| 376 | 0 | arXiv:2308.03421 |  |  |  |  | 1 | Expert Prefetch | [source](https://arxiv.org/abs/2308.03421) |
| 377 | 0 | arXiv:2308.06093 |  |  |  |  | 2 | survey-moe-inference-optimization, 適応的専門家計算 / 専門家統合 / オンラインMoE推論 / ニューラルバンディット | [source](https://arxiv.org/abs/2308.06093) |
| 378 | 0 | arXiv:2308.07107 |  |  |  |  | 2 | KV cache compression / sparse attention / long-context inference, serving-scheduling | [source](https://arxiv.org/abs/2308.07107) |
| 379 | 0 | arXiv:2308.07201 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.07201) |
| 380 | 0 | arXiv:2308.08469 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.08469) |
| 381 | 0 | arXiv:2308.09583 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2308.09583) |
| 382 | 0 | arXiv:2308.10755 |  |  |  |  | 1 | latent-space inference / semantic compression | [source](https://arxiv.org/abs/2308.10755) |
| 383 | 0 | arXiv:2308.12241 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.12241) |
| 384 | 0 | arXiv:2308.13320 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2308.13320) |
| 385 | 0 | arXiv:2308.14711 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.14711) |
| 386 | 0 | arXiv:2308.16898 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2308.16898) |
| 387 | 0 | arXiv:2309.02726 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2309.02726) |
| 388 | 0 | arXiv:2309.05516 |  |  |  |  | 3 | Expert Prefetch, inference-systems, kv-cache-memory | [source](https://arxiv.org/abs/2309.05516) |
| 389 | 0 | arXiv:2309.06342 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.06342) |
| 390 | 0 | arXiv:2309.08520 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2309.08520) |
| 391 | 0 | arXiv:2309.09117 |  |  |  |  | 1 | speculative decoding / context compression / agentic LLM inference | [source](https://arxiv.org/abs/2309.09117) |
| 392 | 0 | arXiv:2309.10305 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.10305) |
| 393 | 0 | arXiv:2309.11235 |  |  |  |  | 3 | KVキャッシュ動的メモリ管理／PagedAttention代替, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2309.11235) |
| 394 | 0 | arXiv:2309.12499 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.12499) |
| 395 | 0 | arXiv:2309.14021 |  |  |  |  | 2 | 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2309.14021) |
| 396 | 0 | arXiv:2309.15531 |  |  |  |  | 3 | KV cache quantization / long-context inference / activation compression, inference-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2309.15531) |
| 397 | 0 | arXiv:2309.17179 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2309.17179) |
| 398 | 0 | arXiv:2310.00566 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.00566) |
| 399 | 0 | arXiv:2310.00844 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2310.00844) |
| 400 | 0 | arXiv:2310.01542 |  |  |  |  | 1 | survey-moe-inference-optimization | [source](https://arxiv.org/abs/2310.01542) |
| 401 | 0 | arXiv:2310.02226 |  |  |  |  | 3 | kv-cache-optimization-compression, latent-space inference / semantic compression | [source](https://arxiv.org/abs/2310.02226) |
| 402 | 0 | arXiv:2310.03533 |  |  |  |  | 3 | inference-systems | [source](https://arxiv.org/abs/2310.03533) |
| 403 | 0 | arXiv:2310.03731 |  |  |  |  | 1 | KV Cache Optimization / Compression | [source](https://arxiv.org/abs/2310.03731) |
| 404 | 0 | arXiv:2310.04607 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.04607) |
| 405 | 0 | arXiv:2310.05421 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2310.05421) |
| 406 | 0 | arXiv:2310.06003 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.06003) |
| 407 | 0 | arXiv:2310.06500 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.06500) |
| 408 | 0 | arXiv:2310.07713 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.07713) |
| 409 | 0 | arXiv:2310.08433 |  |  |  |  | 1 | LLM serving / global scheduling / predictive load balancing / KV-cache migration avoidance | [source](https://arxiv.org/abs/2310.08433) |
| 410 | 0 | arXiv:2310.10436 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.10436) |
| 411 | 0 | arXiv:2310.12541 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.12541) |
| 412 | 0 | arXiv:2310.12962 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2310.12962) |
| 413 | 0 | arXiv:2310.15141 |  |  |  |  | 7 | LLM inference surveys、roofline performance analysis, inference-systems, speculative decoding / draft-model design | [source](https://arxiv.org/abs/2310.15141) |
| 414 | 0 | arXiv:2310.17157 |  |  |  |  | 2 | Conditional Computation, MoE inference / intra-expert activation sparsity / sparse GPU kernels / vLLM | [source](https://arxiv.org/abs/2310.17157) |
| 415 | 0 | arXiv:2310.19295 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2310.19295) |
| 416 | 0 | arXiv:2311.00176 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.00176) |
| 417 | 0 | arXiv:2311.01635 |  |  |  |  | 2 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置, survey-distributed-training-systems | [source](https://arxiv.org/abs/2311.01635) |
| 418 | 0 | arXiv:2311.04823 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.04823) |
| 419 | 0 | arXiv:2311.05232 |  |  |  |  | 3 | LLM inference surveys、roofline performance analysis, LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2311.05232) |
| 420 | 0 | arXiv:2311.07468 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.07468) |
| 421 | 0 | arXiv:2311.08360 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.08360) |
| 422 | 0 | arXiv:2311.08719 |  |  |  |  | 1 | agentic inference / persistent memory | [source](https://arxiv.org/abs/2311.08719) |
| 423 | 0 | arXiv:2311.09047 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.09047) |
| 424 | 0 | arXiv:2311.11195 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.11195) |
| 425 | 0 | arXiv:2311.12424 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.12424) |
| 426 | 0 | arXiv:2311.13171 |  |  |  |  | 2 | MoE inference / expert offloading / expert cache / edge inference / CPU-GPU scheduling, MoE weight pruning / router-aware compression / post-training pruning / knowledge distillation | [source](https://arxiv.org/abs/2311.13171) |
| 427 | 0 | arXiv:2311.14030 |  |  |  |  | 1 | MoE推論／SSDストリーミング／エキスパート先読み／ルーティング予測／量子化回復 | [source](https://arxiv.org/abs/2311.14030) |
| 428 | 0 | arXiv:2311.16502 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2311.16502) |
| 429 | 0 | arXiv:2311.17311 |  |  |  |  | 2 | llm-serving-scheduling-disaggregation, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2311.17311) |
| 430 | 0 | arXiv:2312.00678 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2312.00678) |
| 431 | 0 | arXiv:2312.03003 |  |  |  |  | 1 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2312.03003) |
| 432 | 0 | arXiv:2312.03414 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2312.03414) |
| 433 | 0 | arXiv:2312.04257 |  |  |  |  | 1 | 検索拡張生成・三次元NAND・記憶内検索・ベクトル検索・計算ストレージ | [source](https://arxiv.org/abs/2312.04257) |
| 434 | 0 | arXiv:2312.04927 |  |  |  |  | 4 |  | [source](https://arxiv.org/abs/2312.04927) |
| 435 | 0 | arXiv:2312.05253 |  |  |  |  | 1 | 拡散型LLM推論 / 近似KVキャッシュ / 並列復号 | [source](https://arxiv.org/abs/2312.05253) |
| 436 | 0 | arXiv:2312.06674 |  |  |  |  | 1 | MoE serving / expert offloading / prefill-only serving | [source](https://arxiv.org/abs/2312.06674) |
| 437 | 0 | arXiv:2312.08583 |  |  |  |  | 1 | LLM inference surveys、roofline performance analysis | [source](https://arxiv.org/abs/2312.08583) |
| 438 | 0 | arXiv:2312.08937 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.08937) |
| 439 | 0 | arXiv:2312.11918 |  |  |  |  | 2 | KVキャッシュ動的メモリ管理／PagedAttention代替, survey-distributed-training-systems | [source](https://arxiv.org/abs/2312.11918) |
| 440 | 0 | arXiv:2312.14238 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2312.14238) |
| 441 | 0 | arXiv:2312.16862 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, llm-serving-scheduling-disaggregation | [source](https://arxiv.org/abs/2312.16862) |
| 442 | 0 | arXiv:2312.17276 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2312.17276) |
| 443 | 0 | arXiv:2401.00625 |  |  |  |  | 7 | LLMサービング、エッジ推論、協調推論、資源管理・スケジューリング, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, System-aware KV cache, distributed LLM inference / communication-aware serving, llm-serving-systems, survey-moe-inference-optimization, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.00625) |
| 444 | 0 | arXiv:2401.01923 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.01923) |
| 445 | 0 | arXiv:2401.03868 |  |  |  |  | 6 | LLM inference surveys、roofline performance analysis, hierarchical-memory, kv-cache-memory | [source](https://arxiv.org/abs/2401.03868) |
| 446 | 0 | arXiv:2401.04679 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2401.04679) |
| 447 | 0 | arXiv:2401.06080 |  |  |  |  | 2 | Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2401.06080) |
| 448 | 0 | arXiv:2401.07872 |  |  |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2401.07872) |
| 449 | 0 | arXiv:2401.09486 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.09486) |
| 450 | 0 | arXiv:2401.12522 |  |  |  |  | 3 | inference-systems, speculative-decoding, 投機的復号・オンライン適応・知識蒸留 | [source](https://arxiv.org/abs/2401.12522) |
| 451 | 0 | arXiv:2401.13841 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.13841) |
| 452 | 0 | arXiv:2401.14112 |  |  |  |  | 2 | LLM inference surveys、roofline performance analysis, survey-low-bit-llm | [source](https://arxiv.org/abs/2401.14112) |
| 453 | 0 | arXiv:2401.15947 |  |  |  |  | 9 | Adaptive computation／cache-aware MoE, LLM inference surveys、roofline performance analysis, MoE expert pruning / expert clustering / task-specific model compression, Quantization × MoE × Offload, オフロード／階層メモリ, 適応的エキスパート計算・圧縮 / マルチモーダルMoE推論 / 動的エキスパート省略 | [source](https://arxiv.org/abs/2401.15947) |
| 454 | 0 | arXiv:2401.17221 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2401.17221) |
| 455 | 0 | arXiv:2402.00157 |  |  |  |  | 2 | inference-systems | [source](https://arxiv.org/abs/2402.00157) |
| 456 | 0 | arXiv:2402.01108 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.01108) |
| 457 | 0 | arXiv:2402.01680 |  |  |  |  | 5 | llm-serving-scheduling-disaggregation, multi-LLM communication / KV-cache semantic transfer, エージェント向けKVキャッシュ管理・階層メモリ・プログラム単位スケジューリング | [source](https://arxiv.org/abs/2402.01680) |
| 458 | 0 | arXiv:2402.02716 |  |  |  |  | 2 | Multi-core NPU Architecture / LLM Serving Scheduling and Disaggregation, Reasoning-model post-training / RLVR systems / distributed RL / parallel LLM training and inference | [source](https://arxiv.org/abs/2402.02716) |
| 459 | 0 | arXiv:2402.03563 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.03563) |
| 460 | 0 | arXiv:2402.03898 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2402.03898) |
| 461 | 0 | arXiv:2402.05201 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.05201) |
| 462 | 0 | arXiv:2402.06082 |  |  |  |  | 4 | KV Cache Optimization / Compression, KV cache quantization / RoPE-aware compression / packed attention serving, other-inference-systems | [source](https://arxiv.org/abs/2402.06082) |
| 463 | 0 | arXiv:2402.07754 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.07754) |
| 464 | 0 | arXiv:2402.08178 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.08178) |
| 465 | 0 | arXiv:2402.09353 |  |  |  |  | 3 | Conditional Computation, kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2402.09353) |
| 466 | 0 | arXiv:2402.10685 |  |  |  |  | 1 | 疎注意／長文脈学習 | [source](https://arxiv.org/abs/2402.10685) |
| 467 | 0 | arXiv:2402.11684 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.11684) |
| 468 | 0 | arXiv:2402.12289 |  |  |  |  | 2 | Expert Prefetch, survey-edge-llm | [source](https://arxiv.org/abs/2402.12289) |
| 469 | 0 | arXiv:2402.13116 |  |  |  |  | 3 | Speculative Decoding, 推論エンジン／推論基盤 | [source](https://arxiv.org/abs/2402.13116) |
| 470 | 0 | arXiv:2402.13583 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.13583) |
| 471 | 0 | arXiv:2402.14762 |  |  |  |  | 2 | Expert Prefetch, 投機的復号 / LLMサービング・ベンチマーク | [source](https://arxiv.org/abs/2402.14762) |
| 472 | 0 | arXiv:2402.14866 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.14866) |
| 473 | 0 | arXiv:2402.15758 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2402.15758) |
| 474 | 0 | arXiv:2402.16775 |  |  |  |  | 1 | Quantization × MoE × Offload | [source](https://arxiv.org/abs/2402.16775) |
| 475 | 0 | arXiv:2402.16844 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.16844) |
| 476 | 0 | arXiv:2402.17532 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.17532) |
| 477 | 0 | arXiv:2402.18154 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.18154) |
| 478 | 0 | arXiv:2402.18510 |  |  |  |  | 2 |  | [source](https://arxiv.org/abs/2402.18510) |
| 479 | 0 | arXiv:2402.19047 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2402.19047) |
| 480 | 0 | arXiv:2403.01273 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.01273) |
| 481 | 0 | arXiv:2403.01969 |  |  |  |  | 1 | edge-on-device-llm-systems | [source](https://arxiv.org/abs/2403.01969) |
| 482 | 0 | arXiv:2403.02901 |  |  |  |  | 1 | prefill-decode disaggregation / KV-cache transfer / energy-aware serving / DVFS | [source](https://arxiv.org/abs/2403.02901) |
| 483 | 0 | arXiv:2403.03507 |  |  |  |  | 2 | MoE expert pruning / expert importance estimation / iterative pruning / post-pruning correction, その他システム研究 | [source](https://arxiv.org/abs/2403.03507) |
| 484 | 0 | arXiv:2403.04690 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.04690) |
| 485 | 0 | arXiv:2403.04951 |  |  |  |  | 1 | 先頭共有・鍵値キャッシュ・検索拡張生成・要求処理順・組合せ最適化 | [source](https://arxiv.org/abs/2403.04951) |
| 486 | 0 | arXiv:2403.05826 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2403.05826) |
| 487 | 0 | arXiv:2403.07816 |  |  |  |  | 2 | mixture-of-experts / modular pretraining / expert specialization / memory-efficient selective deployment, survey-moe-inference-optimization | [source](https://arxiv.org/abs/2403.07816) |
| 488 | 0 | arXiv:2403.08763 |  |  |  |  | 1 | 投機的デコード・ドラフトモデル事前学習・分布外一般化・ターゲット横断再利用 | [source](https://arxiv.org/abs/2403.08763) |
| 489 | 0 | arXiv:2403.09347 |  |  |  |  | 2 | survey-distributed-training-systems, survey-long-context-serving | [source](https://arxiv.org/abs/2403.09347) |
| 490 | 0 | arXiv:2403.10266 |  |  |  |  | 1 | survey-distributed-training-systems | [source](https://arxiv.org/abs/2403.10266) |
| 491 | 0 | arXiv:2403.10750 |  |  |  |  | 1 | inference-systems | [source](https://arxiv.org/abs/2403.10750) |
| 492 | 0 | arXiv:2403.12422 |  |  |  |  | 3 | survey-distributed-training-systems, survey-low-bit-llm | [source](https://arxiv.org/abs/2403.12422) |
| 493 | 0 | arXiv:2403.14403 |  |  |  |  | 1 | LLMサービング、ワークフロー実行、分散スケジューリング、RAG/エージェント基盤。 | [source](https://arxiv.org/abs/2403.14403) |
| 494 | 0 | arXiv:2403.15796 |  |  |  |  | 1 | survey-long-context-serving | [source](https://arxiv.org/abs/2403.15796) |
| 495 | 0 | arXiv:2403.18802 |  |  |  |  | 1 | kv-cache-offload-recomputation | [source](https://arxiv.org/abs/2403.18802) |
| 496 | 0 | arXiv:2403.20041 |  |  |  |  | 2 | edge-on-device-llm-systems, モバイル端末内LLM推論／フラッシュ帯域を考慮したコールドスタート最適化 | [source](https://arxiv.org/abs/2403.20041) |
| 497 | 0 | arXiv:2404.01744 |  |  |  |  | 2 | 08-edge-on-device-llm-systems | [source](https://arxiv.org/abs/2404.01744) |
| 498 | 0 | arXiv:2404.02445 |  |  |  |  | 1 | LLMサービング／配備構成探索／自動並列化・圧縮選択／負荷対応配置 | [source](https://arxiv.org/abs/2404.02445) |
| 499 | 0 | arXiv:2404.05446 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2404.05446) |
| 500 | 0 | arXiv:2404.07204 |  |  |  |  | 1 |  | [source](https://arxiv.org/abs/2404.07204) |

## Machine-readable

同じ割当は [worker-worklist-30.json](worker-worklist-30.json) にあります。

