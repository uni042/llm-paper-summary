# MLX

MLXの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-08-18 — v0.32.1（released）**: CUDA RMSNormのregister pressureを下げ、B200で形状により13〜52%改善。`mx.array(host_buffer, copy=False)`によるunified memoryのzero-copy CPU importも追加。[PR #3850](https://github.com/ml-explore/mlx/pull/3850)
- **2026-08-25 — v0.32.2（released）**: GQA decodeでK/V blockの重複loadを削減し、M5 Pro kernel最大1.27倍、Qwen3-30B-A3B E2E decode最大約9.5%向上。[PR #4077](https://github.com/ml-explore/mlx/pull/4077)
- **同 — fused full-attention**: head_dim=256でscore tensorをmaterializeしないNAX kernelを追加。M5 Maxでkernel 1.3〜2.57倍、32K prefill約27%、peak memory 34.6→26.5 GB。[PR #3842](https://github.com/ml-explore/mlx/pull/3842)
- **同 — quantized MoE matmul**: 不要なexpert tile行を処理するSIMD groupを起動しないよう変更し、prefill 2.2〜7.0%改善。[PR #4352](https://github.com/ml-explore/mlx/pull/4352)
