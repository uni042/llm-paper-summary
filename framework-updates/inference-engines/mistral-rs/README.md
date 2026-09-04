# Mistral.rs

Mistral.rsの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-25 — v0.8.23（released）**: `IsqExecutor`で量子化taskをmetadata／temporary buffer認識のthread poolへ配分。[PR #2283](https://github.com/EricLBuehler/mistral.rs/pull/2283)
- **2026-07-07 — v0.9.0（released）**: runtime-dispatched CPU repacking、decode／prefill attention、GQA KV streaming、quantized MoE indexed-expert GEMVを追加。Qwen3-4B Q4K decodeは1.79〜1.81倍、Gemma4-E4B prefillは2.2〜2.8倍。[PR #2311](https://github.com/EricLBuehler/mistral.rs/pull/2311)
- **2026-08-14 — v0.9.1（released）**: true LoRA kernel、dynamic adapter loading、LM head／embedding quantization、concurrent serving schedulerを追加。[PR #2351](https://github.com/EricLBuehler/mistral.rs/pull/2351)
- **2026-08-20 — v0.9.2（released）**: MTP speculative decoding、device-side verification、batch argmax、GDN rollbackを追加。27B Q4／GB10で19.5→24.6 tok/s、code promptで21.3→29.4 tok/s。[PR #2385](https://github.com/EricLBuehler/mistral.rs/pull/2385)
- **同 — DFlash**: batch drafter、acceptance-rate EMAによるdraft depth選択、CUDA Graphを追加。同時実行8で約70→86.7 tok/s。[PR #2388](https://github.com/EricLBuehler/mistral.rs/pull/2388)

[リリース一覧](https://github.com/EricLBuehler/mistral.rs/releases)
