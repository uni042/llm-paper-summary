# ONNX Runtime GenAI

ONNX Runtime GenAIの主要な機能・性能更新を継続的に記録する集約ページ。hardware別model variant、Execution Provider、KV cache共有memory、低bit model builderなど、同じmodelを複数deviceへ展開しやすくする変更を扱う。

## 現在できること

- ONNX Runtime上でdecoder-only LLM等のautoregressive generationを行い、sampling、beam search、KV cache管理をruntime APIから制御できる。
- CUDA、DirectML、QNN、CPU等のExecution Providerを使い、同じ上位APIから異なるhardware backendへ展開できる。
- 同じlogical modelにhardware別build variantを持たせ、実行deviceに応じて適切なgraph / precisionを選択できる。
- INT8等の低bit modelをbuildし、weight memoryとstorage量を削減できる。
- 対応backendではCPUとacceleratorが共有するmemoryへKVを置き、不要なhost-device copyを避けられる。
- C++ / Python等からgeneration loopへ組み込み、desktop / edge application向けのlocal inference runtimeとして利用できる。

以下の更新履歴は、**hardware variant、zero-copy KV、低bit model build**など、device展開とmemory効率を変える主要機能だけを記録している。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-07-30 — v0.15.0（released）

- **1つのmodel packageへ複数build variantを同梱**: 同じlogical modelについて、CUDA向け、DirectML向け、QNN向けなど異なるhardware / Execution Provider用のbuildを1 packageへ入れ、load時に現在のdeviceへ合うvariantを選べるようにした。

  **Execution Provider（実行provider）**は、ONNX graphの各演算をCUDA、DirectML、QNN、CPUなどどのbackendで実行するかを担当する層。これにより利用者がhardwareごとに別model directoryを管理する必要を減らす。[PR #2227](https://github.com/microsoft/onnxruntime-genai/pull/2227)

- **QNN GPU zero-copy KV cache**: Qualcomm QNN系GPUで、CPUからも参照できるshared GPU memoryへKV cacheを確保し、CPU buffer↔GPU buffer間の不要なcopyを避けるallocatorを追加。

  **zero-copy**はdataを別memory領域へ複製せず、CPUとGPUが同じbacking memoryを参照する方式。KV cacheはtoken生成のたびに読み書きされるため、copyを省ければlatencyとmemory bandwidth消費を減らせる。公式説明ではlarge speedupとされるが比較可能な数値は未掲載。[PR #2105](https://github.com/microsoft/onnxruntime-genai/pull/2105)

- **INT8 model builder**: model変換時にINT8精度を選べるようにし、FP16 / FP32より小さいweightと対応kernelを使えるようにした。1要素8 bitなのでmodel memoryとstorage量を削減できる一方、精度維持には適切なscale / quantization方式が必要。[PR #2275](https://github.com/microsoft/onnxruntime-genai/pull/2275)

## 未リリース扱い

WebGPU KV cacheを4-bitへpackする**TurboQuant**はchangelogに言及がある一方、対応PR #2084は収録期間末時点でDraft / WIPだったため、stable実装としては扱わない。[PR #2084](https://github.com/microsoft/onnxruntime-genai/pull/2084)

[releases](https://github.com/microsoft/onnxruntime-genai/releases)

### 用語メモ

- **Execution Provider**: ONNX RuntimeでCUDA、CPU、DirectML、QNNなど実際の演算backendを選択・実行する仕組み。
- **model variant**: 同じmodel architecture / weightを、hardwareやprecisionに合わせて異なるgraph・kernel構成へbuildした実行版。
- **shared memory allocator**: CPUとacceleratorから共通に参照できるmemory領域を確保し、data copyを減らすallocator。
