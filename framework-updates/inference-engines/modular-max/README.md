# Modular MAX

Modular MAXの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-18 — MAX v26.4（released）**: native FP8 attention／FP8 KV cache、EAGLE draft KVのhost／disk offload、speculative overlap scheduler、TP+EPを追加。FP8 KVはBF16相当精度でcapacity約2倍、FlashAttention-4 prefillはB200で1.05〜1.5倍。[release notes](https://max.modular.com/releases/v26.4/)
- **2026-08-11 — MAX v26.5（released）**: NVIDIA／AMD VMM defragmenting allocator、compiled graph内weight sharding、MXint8 KV cache、Rust tiered KV connectorとasync onloadを追加。DP-EP NVFP4で約10 GiB/GPU削減、KV memory約半分。
- 同releaseでshared expertをside stream実行しrouted expertとoverlap。warm MEF cacheはfirst-call compileを約5.6秒→16.7 ms、DFlashでdecode最大約1.3倍。[release notes](https://max.modular.com/releases/v26.5/)
