# SGLang

SGLangの主要な機能・性能更新を継続的に記録する集約ページです。speculative decoding、hierarchical cache、MoE／通信kernel、CUDA Graphなどを扱います。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-13 — v0.5.13（released）**: Spec V2を既定化し、FutureMapとforward-stream転送でper-step syncを削減。HiCacheをhybrid modelの既定にし、Intel CPU+GPU EPDでP99 TTFT／request throughputを最大約1.3倍に改善。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.13)
- **2026-06-26 — v0.5.14（released）**: int8 recurrent-state checkpoint pool、speculative convolution-window cache dedup（cache footprint半減）、Waterfill/LPLB MoE balancing、NVFP4 MoEを追加。KDA CuteDSL prefillはTriton比1.08〜1.52倍。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.14)
- **2026-07-10 — v0.5.15（released）**: Spec V2 schedulerのD2H/H2D sync除去とmetadata fusionでE2E TPS 11%向上。IndexShare MTPは長文draft-step costを最大1.9倍削減し、sparse FlashMLAは長文throughputを10%以上改善。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.15)
- **2026-07-25 — v0.5.16（released）**: confidence-driven DSpark、DSA cache-layer split、ReplaySSM Ring Spec-Verifyを追加。CP4のper-rank KV memoryを74%、spec verification scratchを11.5→1.8 GB/GPUへ削減。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.16)
- **2026-08-22 — v0.5.18（released）**: checkpoint stagingとCUDA Graph captureを重畳し、plain起動比35.6秒対84.8秒。TP LMHead通信を単一all-to-allへ置換し、B200で320→169 µs、TPOT 36.97→35.67 ms。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.18)
