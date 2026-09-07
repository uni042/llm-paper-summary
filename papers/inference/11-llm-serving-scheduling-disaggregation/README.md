# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

## 収録論文

収録論文: 27本。公開日が新しい順。

- 2026-07-30 — [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)
  - P/D分離時に全KVを送らず、重要KVをprefill中に先送りし、不足分をlocal読出しと並列remote取得、残りをnetwork idle時に転送してstage切替待ちを減らす。
- 2026-07-18 — [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)
  - 未知の出力長に対するKV予約量、GPU並列構成、routing、prefix cachingを分布変化まで考慮して共同最適化し、過剰予約とpreemption costを抑える。
- 2026-06-23 — [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)
  - cold MoE群のFFN weight用GPU poolとKV/attention用GPU poolを分け、変動するKV需要をmodel横断で共有して長contextとtail latencyを改善する。
- 2025-01-24 — [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)
- 2025-01-14 — [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)
- 2024-08 — [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)
  - scenario別にP/D groupと比率を調整し、idle prefillへのrerouteと連続bufferを使うKV転送を統合して数万NPU規模のproduction servingを扱う。
- 2024-08-28 — [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)
- 2024-07-01 — [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)
- 2024-06-25 — [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)
- 2024-06-05 — [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)
- 2024-06-05 — [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)
- 2024-05-30 — [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)
- 2024-05-08 — [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)
- 2024-04-25 — [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)
- 2024-03-23 — [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)
- 2024-03-04 — [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)
- 2024-01-25 — [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)
- 2024-01-17 — [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)
- 2024-01-09 — [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)
- 2023-12-31 — [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)
- 2023-12-12 — [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)
- 2023-12-09 — [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)
- 2023-11-30 — [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)
- 2023-11-27 — [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)
- 2023-09-12 — [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)
- 2023-05-10 — [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)
- 2022-07-11 — [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)

## 主な技術の分岐

- continuous batching / preemption: Orca、vLLM、FastServe。
- chunked prefill: DeepSpeed-FastGen、Sarathi-Serve。
- prefix-aware routing / cache reuse: SGLang、Preble、Pensieve、CachedAttention、Mooncake。
- P/D disaggregation: Splitwise、DistServe、Mooncake、P/D-Serve、SmartGen。
- multi-model memory disaggregation: CrossPoolはcold MoEのFFN weight poolとKV/attention poolを分離する。
- uncertainty-aware KV reservation: Robust KV Cache Managementは出力長分布のshiftを考慮して予約・routing・GPU構成を共同最適化する。
