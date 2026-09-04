# Megatron-Core

Megatron-Coreの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-23 — Core 0.18.0（released）**: Megatron-FSDP A2A overlap、HybridEP fusion、GroupGEMM＋SwiGLU＋quantize fused MLP、full-model CUDA Graph、MXFP8／NVFP4 parameter gatherを追加。[release](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.18.0)
- **2026-08-19 — Core 0.19.0（released）**: Quantile Balancing router、fused shared-expert MLP、DeepEP／HybridEP THD dispatch、NCCL EP dispatcher、per-sequence AlltoAll fusion、CUDA-Graph-compatible activation offload、streaming quantized checkpoint loadを追加。[release](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.19.0)
- **2026-08-02〜08-19 — activation recompute（merged into `dev`）**: EP A2A overlapとfull recomputeを併用し、stage単位からlayer／segment単位へ細分化。[#5869](https://github.com/NVIDIA/Megatron-LM/pull/5869) [#6311](https://github.com/NVIDIA/Megatron-LM/pull/6311)
- **2026-08-18 — chunked optimizer-state offload（merged into `dev`）**: optimizer state／master weightをpinned CPU canonical storageへ置き、bounded chunkだけGPUへrestore・update・offloadしてpeak memoryを抑える。[PR #6244](https://github.com/NVIDIA/Megatron-LM/pull/6244)

## 注視すべきPR

- **#5745（Open）**: inference-only DeepEP v2 dispatcher。decode／chunked-prefill bufferを分離しCUDA Graph capture可能なlayoutを導入。[PR #5745](https://github.com/NVIDIA/Megatron-LM/pull/5745)
