# ExLlama

ExLlama系の主要な機能・性能更新を継続的に記録する集約ページ。ExLlamaV2の後継であるExLlamaV3も同じ系統として扱う。GPU memoryへ収まりきらないMoE expert / KV cacheのCPU offload、投機的デコード（speculative decoding）、MTP、VRAM allocatorなどを中心に記録する。

## 現在できること

- **consumer GPUでの低bit推論**: NVIDIA GPUを中心に、EXL3などの2〜8 bit級weight量子化を使ってmodel本体のVRAM使用量とweight読出し量を削減できる。量子化形式に合わせた専用kernelでdecode速度を維持することを狙う。
- **複数requestの同時serving**: continuous / dynamic batchingで、到着時刻や生成長が異なるrequestを同じGPU上で継続的にbatchへ出し入れできる。固定batchの終了待ちを減らし、対話serverでGPUが空く時間を減らせる。
- **複数GPUへのmodel配置**: tensor parallelismでdense計算を複数GPUへ分割し、MoEではexpert parallelismでexpert群を別GPUへ配置できる。dense部分とexpert部分を同じ分割規則へ固定せず、GPU枚数とVRAM容量に合わせて配置を変えられる。
- **MoE expertのCPU offload**: 全expertをVRAMへ常駐させず、一部をCPU DRAMへ置いて必要なexpertを利用する構成を取れる。巨大MoEを少ないVRAMで動かせる代わりに、CPU memory帯域とPCIe転送が新しい律速になり得る。
- **KV cacheの容量削減と階層化**: KVを2〜8 bitへ量子化してtoken当たりのcache量を減らせるほか、VRAMに収まらないKV pageをCPU DRAMへ退避できる。長contextや複数conversationを同時保持するときのVRAM pressureを下げられる。
- **投機的デコード**: draft model、MTP、n-gram等で複数token候補を先に作り、target modelでまとめて検証できる。draft量やconfidence thresholdも動的に調整でき、外れた候補を大量に計算する無駄を抑えられる。
- **LoRA・multimodal・API serving**: LoRA adapter、画像等を含むmultimodal modelを扱え、TabbyAPI等と組み合わせればOpenAI互換APIとして複数clientへ提供できる。Hugging Face Transformers pluginとして既存workflowからbackend利用することもできる。

以下の更新履歴は、これらの主要能力が**どのhardware構成まで使えるようになったか、VRAM / CPU RAM / PCIeをどう使い分けられるようになったか、decodeの無駄やallocator断片化をどこまで減らしたか**という観点で追う。

## 初期収録期間

2026-06-03〜2026-09-03

ExLlamaV2には期間内の本質的更新がなく、後継のExLlamaV3を同じ系統として追跡する。

## 要点

この期間のExLlamaV3は、**GPUへ置くexpert / KVとCPUへ逃がす部分を実行中に調整しながら、投機的デコードのdraft量もworkloadに合わせて変える**方向へ進んでいる。

固定的に「このlayerは全部CPU」と決めるのではなく、GPU memory残量や利用状況に合わせて一部expert・cacheをCPUへ移すため、VRAM容量とPCIe / CPU RAM bandwidthのtrade-offを細かく調整できる。

## 主要更新

### 2026-07-25 — ExLlamaV3 v1.2.0（released）

- **experimental expert-layer CPU offload**: MoE layerのexpert weightをCPU RAMへ退避し、必要なexpertだけGPU計算へ使う経路を追加。巨大MoEを少ないVRAMで動かせる一方、expert読込がCPU memory / PCIe bandwidthへ依存する。

- **dynamic draft window**: 投機的デコードで先読みするtoken数を固定せず、直近の受理状況などに応じて増減する。draftしすぎによる無駄なverifyを減らす狙い。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.2.0)

### 2026-07-31 — v1.3.0（released）

- **第2階層CPU KV cache**: 過去tokenのKVをすべてVRAMへ置かず、一部pageをCPU RAMへ退避できるようにした。

- **page / checkpoint eviction policy**: cache容量が足りなくなったとき、どのKV pageやcheckpointを残し、どれを追い出すかをpolicyで選べるようにする。

  これにより長contextや複数conversationを扱うとき、単純な「古いものから全部捨てる」以外のcache管理が可能になる。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.3.0)

### 2026-08-06 — v1.4.0（released）

- **AVX-512 CPU offload path高速化**: CPUへ退避したweight / expert計算で、512-bit幅のSIMD命令AVX-512を使う経路を改善。

- **prefill高速化**: 長いpromptをまとめて処理するprefill pathも調整。release noteには比較可能な公式数値なし。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.4.0)

### 2026-08-23 — v1.4.3（released）

- **partial CPU expert offloadを動的配置へ変更**: MoE layer全体ではなくexpert単位でCPU / GPU配置を変えられるようにし、VRAM残量へ合わせたより細かいoffloadを可能にした。

- **self-calibrating confidence threshold**: 投機的デコードでdraftを続けるか止めるかのconfidence閾値を固定せず、実際の受理傾向から自動調整する。

- **TP時のCPU cache offload**: tensor parallelism（TP）でmodelを複数GPUへ分割している場合にもCPU側KV/cache階層を利用できるようにした。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.4.3)

### 2026-08-31 — v1.4.5（released）

- **MoE MTP高速化**: MoE modelでMTP（Multi-Token Prediction; 複数token予測）を使う際のdraft / verify pathを高速化。

- **MoE layerのslab allocation**: expertごとに細かくVRAM領域を確保して隙間を増やす代わりに、大きな連続領域（slab）を先に確保して内部で分配する方式へ変更。

  これにより異なるshapeのallocationを繰り返して生じるVRAM断片化（fragmentation）と、alignmentによる未使用領域を減らす。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.4.5)

### 2026-09-02 — v1.4.6（released）

- **Windows向けexperimental n-gram streaming**: 直前のtoken列に一致する過去n-gramを使って次token候補を先読みする軽量なdraft方式を追加。別のneural draft modelを動かさず、既出token patternから候補を作るためdraft costが小さい。

[release](https://github.com/turboderp-org/exllamav3/releases/tag/v1.4.6)

### 用語メモ

- **CPU offload**: GPU memoryへ置ききれないweightやKVをCPU RAMへ置き、必要時だけGPU側から利用する方式。
- **eviction policy**: cacheが満杯になったとき、何を追い出すか決める規則。
- **slab allocation**: 大きなmemory領域をまとめて確保し、その中から小領域を切り出すallocator方式。細かいallocationによる断片化を減らせる。
- **n-gram drafting**: 過去に現れた連続token patternを基に将来tokenを予測する、model-freeに近い投機候補生成方式。
