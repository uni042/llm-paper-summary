# LightLLM

LightLLMの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-08-10 — v1.2.0（released）**: RL serving向けonline weight update／cache flush／pause-resume、disaggregated ViT worker、Hybrid Radix Cacheを追加。
- Hybrid Radix Cacheはfull-attention KVとlinear-attentionのconvolution／SSM stateを異なるpage粒度で管理し、CPU offloadへ対応。
- multi-level cacheはGPU→CPU→disk、quantized CPU KV、FP8／INT8 KV、NUMA-aware placement、NIXL transfer、cache-aware P/D schedulingを統合。
- MTP／EAGLE、TMA MoE kernel、fused MoE preparation、disk cache v1.0、AWQ／FP8も収録。release本文に比較可能な性能値はない。

[release](https://github.com/ModelTC/lightllm/releases/tag/v1.2.0)
