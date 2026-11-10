# TensorRT Edge-LLM

TensorRT Edge-LLMの主要な機能・性能更新を継続的に記録する集約ページ。TensorRT-LLM本体とは別に、**Jetson / DRIVE / DGX Spark等のedge・physical AI向けC++ LLM/VLM推論runtime**として追跡する。

## 現在できること

- **edge向けC++推論runtime**: NVIDIA Jetson、DRIVE、DGX Spark、IGX等でtext / vision / audio / speech / action modelを実行する。
- **TensorRT engine build**: Hugging Face checkpoint→ONNX→C++ engineの標準経路に加え、対応modelではONNXを介さないexperimental direct engine builderも利用できる。
- **量子化・低精度推論**: NVFP4、FP8、INT4等を利用し、edge環境のmemory容量と帯域制約へ適応する。
- **投機的デコード**: MTP、DFlash / DFlash2、DSpark、EAGLE3等を利用できるmodel / platformがある。
- **KV cache reuse**: multi-turn LLMやVLMのmedia-aware context cache、paged KV reuse等を扱う。
- **OpenAI互換server**: experimental serverでreasoning parser、streaming、video input等を提供し、in-flight batchingも段階的に導入している。
- **multi-device**: DGX Spark等でtensor parallel構成を扱う。
- **multimodal / physical AI**: VLM、ASR、TTS、video、VLA / policy inferenceまで対象を広げている。

## 主要更新

### 2026-09-29 — v0.11.0（released）

- **Python wheel配布**: 対応x86-64 / AArch64 platform向けにpublished wheelを追加。
- **in-flight batching**: experimental OpenAI-compatible serverへopt-in single-rank in-flight batchingを導入。
- **guided decoding**: XGrammarを使ったJSON / JSON Schema / regex / EBNF / structural tag / choices制約を追加。
- **DFlash2 / Qwen3.8**: Qwen3.8 DFlash2 speculative decodingを追加し、Nemotron / Gemmaのspeculative経路も拡張。
- **IGX Thor / multi-device**: IGX Thorを正式対応し、Qwen3.5 tensor-parallel inferenceを追加。
- **runtime / memory**: bounded Gemma 4 sliding-window KV、DiffusionGemma prompt-KV reuse、GPU media hashing、Blackwell向けpaged FMHAやMoE kernel等を強化。

### 2026-09-03 — v0.10.1（released）

- 2台のDGX Sparkを使うexperimental TP=2、Qwen3.8-27B DSpark、FP8 ViT attention、DART visual-token pruningを追加。
- experimental OpenAI-compatible serverを再設計し、公式release noteではdisk usageを60〜99%削減、cold launch timeを50%削減と報告。

一次資料:
- https://github.com/NVIDIA/TensorRT-Edge-LLM
- https://github.com/NVIDIA/TensorRT-Edge-LLM/releases/tag/v0.11.0
- https://github.com/NVIDIA/TensorRT-Edge-LLM/releases/tag/v0.10.1

## 追跡方針

TensorRT-LLM本体とは分け、edge hardware固有のengine build、低bit kernel、KV / context reuse、speculative decoding、multi-device、OpenAI-compatible serving、multimodal / physical-AI pipelineの主要変更を追う。単なるmodel追加だけで主要能力が変わらない更新や軽微なcorrectness fixは原則除外する。
