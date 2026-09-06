# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。GPUだけに頼らずCPU / NPU / storageも使い、どの計算やweightをどのdeviceへ置くかを動的に決める手法が中心となる。

単なる小型model化ではなく、既存の比較的大きなLLM / MoEを限られたhardwareで実用速度に近づけるruntime・scheduling・memory管理を主対象とする。

## 収録論文

収録論文: 4本。公開日が新しい順。

- 2026-08-17 — [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)
  - expert cache、CPU / GPUの実行分担、KV再利用をまとめて制御し、その時のmemory bandwidthに合わせて個人PC上のMoE実行方法を変える。
- 2025-04-21 — [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)
  - どのexpertを使うかだけでなく、どのdeviceでそのexpertを実行するかも同時に決め、edge環境の計算量とdevice間転送を減らす。
- 2024-06-10 — [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)
  - 実際に活性化する計算が一部に偏る性質を利用し、smartphoneのNPU・GPU・CPUへ処理を分担して大きなLLMを動かす。
- 2023-08-29 — [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)
  - 多数のexpertを少数の常駐slotへ入れ替えながら使い、指定したmemory budget内で既存MoEを動かせるようにする。
