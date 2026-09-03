# Edge／on-device MoE

収録論文: 4本。公開日が新しい順。

- 2026-08-17 — [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)
  - GPU・CPU・RAM・PCIeを統合資源として扱い、global expert cache、帯域適応CPU/GPU実行、KV再利用を一体化した個人PC向けMoE runtime。
- 2025-04-21 — [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)
  - トークン単位とデバイス単位の二段階routingを協調させ、edge環境でMoEの計算量とデータ移動を抑える手法。
- 2024-06-10 — [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)
  - 活性疎性を利用してNPU・GPU・CPUを協調させ、メモリ制約の厳しいモバイル端末で大規模LLMを動かす推論システム。
- 2023-08-29 — [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)
  - 実expertを少数のvirtual expert枠へ動的に写像し、指定メモリ予算内で既成MoEの品質とswap遅延を調整する方式。
