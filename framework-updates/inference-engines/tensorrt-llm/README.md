# TensorRT-LLM

TensorRT-LLMの主要な機能・性能更新を継続的に記録する集約ページです。pre-releaseは正式版と区別して記録します。

## 初期収録期間

2026-06-03〜2026-09-03

対象期間の更新はv1.3.0 release candidate群で、すべてpre-releaseである。

## 主要更新

- **2026-06-10〜06-30 — rc18〜rc20**: CUDA IPCからVMM/MNNVLへの移行、C++ KVCacheManagerV2、disk KV cache、async Ulysses、EAGLE3 dynamic tree、KV prefetch block数制御、MXFP8／NVFP4 MoE、CUDA Graph multimodal encoderを追加。[rc18](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc18) [rc19](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc19) [rc20](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc20)
- **2026-07-15〜07-31 — rc21〜rc23**: cache managerのtransceiver／offload、disaggregated coordinator、DFlash／DSpark、FP4 KV cache、runtime KV compression、fine-grained context chunk、conversation単位KV reuseを追加。[rc21](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc21) [rc22](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc22) [rc23](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc23)
- **2026-08-12 — rc24**: prefill CUDA Graphとcapture bucket、breakable graph、KVCacheManagerV2のpaged attention／block reuse、batched KV compaction、Ray/NIXL disaggregationを追加。[release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc24)
- **2026-08-31 — rc25**: KVCacheManagerV2を主要モデルで既定化し、zero-copy token passing、distributed pool rebalance、cold-page codec、DSA writeback overlap、CFT counted-write MoE A2A、tiered GVR TopKを追加。[release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc25)

release noteには比較可能な総合性能値がほぼなく、正式版前の状態である点に注意が必要。
