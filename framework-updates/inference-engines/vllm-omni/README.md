# vLLM-Omni

vLLM-Omniの主要な機能・性能更新を継続的に記録する集約ページ。vLLM本体とは別に、音声・画像・動画・拡散モデル・VLAなどを含む**オムニモーダル推論と多段階serving**の更新を追跡する。

## 現在できること

- **オムニモーダルmodel serving**: textだけでなくspeech、audio、image、video、diffusion、vision-language-action等のmulti-stage modelを共通runtimeで扱う。
- **多段階pipelineの分離実行**: autoregressive stage、encoder、diffusion / decoder等を独立stageとして配置し、stageごとにbatching・GPU配置を変えられる。
- **full-duplex / realtime interaction**: engine所有sessionにより、入力と出力が重なる音声中心の双方向interactionを扱える。
- **stage間KV / multimodal payload転送**: MooncakeやNIXL等を利用し、AR→DiT等のstage間でKV、text、visual/audio latent、layout metadataを転送・再利用できる。
- **continuous / request batching**: diffusionや音声、画像生成を含む複数requestをbatch化し、stageごとのGPU利用率を高める。
- **memory / offload最適化**: component単位offload、FP8等の低精度、prefix / projection cache、KV reuseを利用できる。
- **multi-hardware対応**: NVIDIA CUDAに加え、Ascend NPU、Intel XPU、ROCm等の対応を拡張している。

## 主要更新

### 2026-09-25 — v0.30.0（released）

- **統一full-duplex serving**: `DuplexOmni` / `DuplexOmniEngine` / `DuplexOrchestrator` を導入し、session ownershipとlifecycleをengine側へ移した。
- **native cross-stage KV / payload transfer**: diffusion KVのstage間転送・再利用、Mooncake AR→DiT handoff、KV prefetch、HunyuanImage3のcross-request paged prefix cache、NIXLによるconditioning payload転送を追加。
- **interactive world-model / streaming video**: stepwise generation、mid-stream camera control、streaming VAE decode、chunked video encodingと非同期転送を強化。
- **memory / serving拡張**: component-selective offload、AR-stage FP8 KV、multi-process API serving、RL rollout serving API等を追加。
- **vLLM 0.30.0へrebase**し、speech / image / audiovisual generation / VLAの対応範囲を拡張。

一次資料:
- https://github.com/vllm-project/vllm-omni
- https://github.com/vllm-project/vllm-omni/releases/tag/v0.30.0

## 追跡方針

通常のvLLM更新とは分けて、vLLM-Omni固有のmulti-stage scheduling、full-duplex、audio / video / diffusion serving、stage間KV / payload transfer、memory / offload、hardware backendの主要変更を追う。単なるmodel allowlist追加や軽微なbug fixは原則除外する。
