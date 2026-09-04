# Megatron-LM

Megatron-LM repository全体の主要なシステム更新を継続的に記録する集約ページです。Megatron-Core固有の詳細は[Megatron-Core](../megatron-core/)を参照してください。

## 初期収録期間

2026-06-03〜2026-09-03

Megatron-LM repositoryの主要システム更新はMegatron-Core releaseと`dev` PRとして提供された。

## 要点

- Core 0.18.0／0.19.0でMoE A2A overlap、HybridEP／DeepEP、fused MoE MLP、CUDA Graph、低精度parameter gather、Quantile Balancing routerを追加。
- `dev`へactivation recomputeとchunked optimizer-state／master-weight CPU offloadがmergeされた。
- inference-only DeepEP v2 dispatcherは期間末時点でOpen。

- [Megatron-LM releases](https://github.com/NVIDIA/Megatron-LM/releases)
