# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

## 収録論文

収録論文: 7本。公開日が新しい順。

- 2026-09-02 — [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md)
  - edgeで将来状態を先回りcacheし、speculative reject時のedge-cloud全体rollbackをlocal lookupへ置き換えながらWAN転送量を抑える。
- 2026-09-01 — [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)
  - 他applicationがRAMを要求したとき、LLMのweightとKVを必要量だけ圧縮RAM / Flashへ退避し、実行順を考えた復帰でmobile multitasking時のTTFT悪化を抑える。
- 2026-08-17 — [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)
  - 個人PCのGPU・CPU・RAM・PCIe帯域をまとめて見て、expert cache、CPU/GPU分担、KVとのVRAM配分をhardware条件に合わせて変えるMoE runtime。
- 2026-06-17 — [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md)
  - full MoEをdiskへ置き、routingされたexpertだけを上限付きcacheへmaterializeしてlocal memory budgetを守る。
- 2025-04-21 — [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)
  - native routerが選んだexpertごとにINT2/3/4のprecisionを追加routerで選び、SSD読込とGPU計算をdevice特性に合わせて重ねる。
- 2024-06-10 — [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)
  - よく使うweightを高速memoryへ残し、NPU・CPU・DRAM・UFS Flashを役割分担させてスマートフォン上で大規模LLMを動かす。
- 2023-08-29 — [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)
  - GPUには少数のexpert slotだけを置き、RAM上のactual expert weightを必要に応じてslotへ入れ替えて指定memory budget内で既存MoEを動かす。
