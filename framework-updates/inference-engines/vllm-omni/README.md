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

### 2026-11-22 — vLLM-Omni v0.34.0（正式版）

- v0.34.0rc1からの正式版。vLLM 0.34.0へrebaseし、autoregressive / generation stageはModel Runner V2へ移行。776件のPR（185名、うち初回61名）。
- 新モデル: MiniMax-H3-Image（画像生成・編集）、FLUX.3 (Klein)、PAN2（text/image-to-video）、Hy-Nomas-Diffusers、Haru-4B（full-duplex音声対話）、Ming-3.0系（TTS Tiny / Audio Flash）、Stable Audio 3 Medium、SAM 3 / 3.1、Video Depth Anything、NVIDIA Alpamayo 2 Super、Runway Praxis-1。
- **分散duplex serving**: stage replicaを独立runtimeへ配置しつつsessionをreplica groupへ固定。外部orchestrator向けの実験的 `/v1/run` API。CausVidの生成中video streaming、sessionのKV状態を保つ Noisy Pipeline Parallelism も追加。
- **runtime**: 同時request時のOmni prefix-cache overhead削減、AR KV cacheと後段speech stage向けhidden stateのLMCache CPU offloading、HunyuanImage3 の AR/DiT stage間 CUDA IPC weight sharing。
- [公式release](https://github.com/vllm-project/vllm-omni/releases/tag/v0.34.0)

### 2026-11-18 — vLLM-Omni v0.34.0rc1（公開候補版）

- upstream vLLM 0.34.0への整合を目的とする初のRC。AR / generation stageでModelRunner V2が必須となり、Python 3.11〜3.13とvLLM 0.34.0の一致が必要。
- 新モデル: Haru-4B（speech-to-speech）、MiniMax-H3-Image（画像生成・編集）、PAN2（video生成）。duplex stage間のsession-aware routing、Qwen3-Omni duplex session向けMooncake KV / hidden-state cachingを追加。MiniCPM-o 4.5でCUDA V2 K-step decodingを有効化し、MOSS-TTS-Nano / MOSS-TTS-RealtimeをV2へ移行。
- **互換性（breaking的変更）**: 旧Omni V1 runnerを選択するworkflowは拒否される（Drama 3 / Fish-Omni、LFM3-Omni、PersonaPlex、YuE2、Qwen3-TTS / Qwen3-OmniのROCm・MUSA override等）。Kokoro-82MとJoyAI-Image-Editは廃止。ネイティブvLLM 0.34のAscend実行は未検証と明記されている。
- [公式release](https://github.com/vllm-project/vllm-omni/releases/tag/v0.34.0rc1)

### 2026-11-04 — vLLM-Omni v0.33.0rc1（公開候補版）

- upstream vLLM 0.33.0（正式版）への整合を目的とするRC。runtime integration、依存更新、インストール手順、upgrade-validation修正が中心で、release notesに新モデル・benchmark・breaking changeの記載はない。
- [公式release](https://github.com/vllm-project/vllm-omni/releases/tag/v0.33.0rc1)

### 2026-10-28 — vLLM-Omni v0.32.0（正式版）

- v0.32.0rc1からの正式版。vLLM 0.32.0への整合。Rayベースのmulti-node inference（任意）、`/v1/realtime` のserver VAD、full-duplex serving。
- 新モデル: YuE2-3B（text-to-music）、Qwen-Image-2.1 / 2.1-Turbo、Kandinsky6、MOSS-Image、TaoMate-H3、LTX 2.5 text-to-audio、single-stage Qwen3-TTS。
- 互換性: Python >=3.11,<3.14 と vLLM 0.32.0が必須。output-type名はcanonical spelling（`text` / `image` / `audio` / `latent` / `token_ids`）が必須となり、legacy aliasは拒否される（breaking的変更）。インストール例はCUDA 13.0。
- [公式release](https://github.com/vllm-project/vllm-omni/releases/tag/v0.32.0)

### 2026-10-19 — vLLM-Omni v0.32.0rc1（公開候補版）

- v0.31.0rc1から297件の変更を取り込み、vLLM本体v0.32.0へ整合。正式版ではなくrelease candidate。
- session-aware replica placement、複数frontendをまたぐfull-duplex audio serving、`/v1/realtime`のserver-side VAD、RL learnerからserving workerへのweight transferを追加。
- MOSS-Image、TaoMate-H3 streaming、LTX 2.5、JoyAI、YuE2を拡張。PersonaPlexのstage-wise batching / CUDA Graph / memory最適化、diffusion attentionのCUDA FA3 FP8とMammothModa2 DiTのonline FP8も含む。
- Python `>=3.11,<3.14`。release時点ではPyPI wheel / container imageがpipeline待ちと記載されていた。すべてのmodelが初日から対応するとは扱わない。
- 出典: [v0.32.0rc1 release](https://github.com/vllm-project/vllm-omni/releases/tag/v0.32.0rc1)

### 2026-10-06 — vLLM-Omni v0.31.0rc1（公開候補版・pre-release）

- **多ノード推論**: Ray実行器を任意選択で追加し、段階ごとのGPUをクラスタ全体へ割り当て、環境情報を伝播できるようにした。vLLM本体0.31.0へ追随。
- **多段階転送・双方向実行**: V1とModel Runner V2の混在段階を扱う共有実行、チャンク転送のバイト単位バックプレッシャー（byte backpressure）、双方向出力と中断処理の上限制御を追加。Qwen3-TTSの単一GPU・単一段階音声生成、Qwen3-Omniのリアルタイム提供、MiniCPM-oのKVスライディングウィンドウも改善。
- **互換性・検証上の注意**: 出力型の旧別名を拒否し、`text`、`image`、`audio`、`latent`、`token_ids` の正規名を要求する。公式nightlyは54 passed / 3 failed / 4 brokenで全テスト成功ではなく、MiniCPM-o長時間音声の失敗が残る。安定版v0.30.0と混同しない。
- 一次資料: https://github.com/vllm-project/vllm-omni/releases/tag/v0.31.0rc1

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
