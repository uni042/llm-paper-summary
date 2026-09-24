# ONNX Runtime GenAI

ONNX Runtime GenAIの主要な機能・性能更新を継続的に記録する集約ページ。hardware別model variant、Execution Provider、KV cache共有memory、低bit model builderなど、同じmodelを複数deviceへ展開しやすくする変更を扱う。

## 現在できること

- **ONNX graph上でautoregressive generation**: decoder-only LLM等をONNX Runtime上で実行し、token生成loop、KV cache更新、samplingをruntime APIから制御できる。通常のONNX graph inferenceだけでなく「1 token生成→cache更新→次token」の状態fulな生成処理をまとめて扱う。
- **複数Execution Providerへの展開**: CUDA、DirectML、QNN、CPU等のExecution Providerを使い、同じ上位APIからNVIDIA GPU、Windows GPU、Qualcomm accelerator、CPU等へmodelを展開できる。hardwareごとにapplication code全体を書き直す必要を減らす。
- **hardware別model variant**: 同じlogical modelについて、backendやprecisionの異なる複数buildを1 packageへ持たせ、実行deviceに応じて適切なvariantを選べる。deviceごとに別model directoryを配布・管理する負担を減らせる。
- **generation制御**: greedy / sampling / beam search等のdecoding設定、stop condition、sequence stateをruntime APIから制御できる。application側でtoken loopを完全に自前実装せずに済む。
- **KV cache管理**: 過去tokenのK/Vをruntimeが保持し、decodeごとにprompt全体を再計算せず次tokenだけ処理できる。backendによってはcache memoryの配置方法まで最適化できる。
- **zero-copy KV**: 対応deviceではCPUとacceleratorが同じbacking memoryを参照するshared allocationへKVを置き、host bufferとdevice buffer間のcopyを減らせる。特にtokenごとにread / writeするKVでcopy削減がlatencyへ効く。
- **低bit model build**: INT8等へmodelを変換し、weight memoryとstorage量を削減できる。model packageのdownload size、device memory、weight bandwidthを減らせる一方、精度とbackend kernel対応を確認する必要がある。
- **backend別graph最適化**: Execution Providerに応じてoperator fusion、precision、memory allocationを変えられる。上位modelは同じでも、実際のgraph / kernelをhardwareへ合わせてbuildできる。
- **C++ / Python applicationへの組込み**: desktop、edge、native applicationからgeneration APIを呼び出せる。server専用runtimeではなく、application process内でlocal inferenceする用途にも向く。
- **edge / client deployment**: DirectMLやQNN等を使い、datacenter GPUだけでなくWindows PCやQualcomm系deviceへ生成modelを持ち込める。model sizeとdevice memoryが制約になるため量子化との組合せが重要。
- **portable model packageの位置づけ**: 高throughput multi-tenant servingのschedulerより、ONNX Runtime ecosystemを使って同じapplication / model familyを複数hardwareへ展開することに強みがある。

以下の更新履歴は、対応model追加ではなく、**同じmodelをどれだけ多様なdeviceへ持ち運べるか、KVやweightのcopy / memory量をどこまで減らせるか、hardwareごとのbuild管理をどこまで簡素化できるか**を変える主要機能だけを記録する。

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
