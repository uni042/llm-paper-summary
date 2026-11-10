# Mistral.rs

Mistral.rsの主要な機能・性能更新を継続的に記録する集約ページ。CPU量子化kernel、attention、MoE、LoRA、投機的デコード（speculative decoding）、CUDA Graph、同時request schedulingなどを扱う。

## 現在できること

- **複数hardware backendでのlocal / server inference**: CPU、CUDA GPU、Apple MetalでLLM / multimodal modelを実行できる。desktopからGPU serverまで同じruntime系で扱える一方、利用できるkernelや量子化形式はbackendごとに異なる。
- **continuous batchingとpaged attention**: 複数requestを同時に進め、生成が終わったrequestをbatchから外しながら新しいrequestを追加できる。KVをpage単位で管理することで、最大context分の連続領域をrequestごとに先取りするmemory浪費を減らせる。
- **多様なmodel / weight形式**: Hugging Face checkpoint、GGUF、独自量子化形式を扱える。2〜8 bit、GPTQ、AWQ、HQQ、FP8等を選び、VRAM / RAM容量と速度・精度のtrade-offを調整できる。
- **layer単位のdevice / precision配置**: layerごとにCPU / GPU、量子化精度を変えられるため、全modelを同じdevice・同じbit幅へ固定せずhardware容量に合わせて配置できる。大きいmodelでは一部layerをCPUへ逃がしてVRAM不足を回避できる。
- **multi-GPU / distributed inference**: 複数GPUへmodelや計算を分け、単一GPUに収まらないmodelや高いserving並列度へ拡張できる。通信costが増えるため、GPU間linkとmodel shapeに応じて利得が変わる。
- **prefix cacheとKV streaming**: 共通prefixのKVを再利用し、同じsystem prompt等を繰り返しprefillする計算を減らせる。GQAでは共有K/Vを不要に複製せずstreamしながら使い、memory trafficを減らす経路も持つ。
- **LoRA / X-LoRA serving**: base modelを再loadせず、request単位でadapterを切り替えられる。dynamic load / unloadにより、複数用途のadapterを1つのserverへ載せつつ、使っていないadapterのmemoryを解放できる。
- **MoE向け低bit実行**: routingされたexpertだけをindexで選び、量子化weightのままGEMV / GEMMを実行できる。全expertを毎token計算せず、decode時のweight読出し量を抑える。
- **投機的デコード**: MTP / DFlash等で複数token候補を先に生成し、target modelでまとめて検証できる。acceptance rateを見てdraft depthを自動調整し、候補を作りすぎる無駄を抑えられる。
- **GPU側でのverifyとCUDA Graph**: draft tokenの受理判定やargmaxをGPU上でまとめて行い、CPUとの同期を減らせる。CUDA Graphで繰り返すdraft / verify kernel列をcaptureし、tokenごとのlaunch overheadも下げられる。
- **recurrent modelのrollback**: GDN等のrecurrent stateを持つmodelでも、投機候補が拒否されたとき最後に確定したtoken位置へstateを巻き戻せる。KV cacheだけを持つTransformer以外にもspeculative decodingを広げるための機能。
- **API / agentic serving**: OpenAI互換・Anthropic互換API、web UI、tool calling、MCP client、code / shell executionを備え、単なるtext completionだけでなくtool-using agentのruntimeとして使える。

以下の更新履歴は、これらの主要能力について**CPU / GPUそれぞれの低bit kernel、cacheとdevice配置、adapter切替、複数request scheduling、投機的デコードのGPU完結度**がどう改善されたかを追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-25 — v0.8.23（released）

- **量子化taskのthread pool scheduling改善**: `IsqExecutor`が、量子化対象tensorのmetadataや一時buffer使用量を見ながらCPU threadへtaskを振り分けるようにした。

  量子化では複数tensorを並行変換すると、一時memoryが膨らんだり、特定taskだけ重くなったりする。この変更は「thread数だけ均等配分」ではなく、taskのmemory / work量を考慮して初期変換時間とpeak memoryを安定させるためのもの。[PR #2283](https://github.com/EricLBuehler/mistral.rs/pull/2283)

### 2026-07-07 — v0.9.0（released）

- **runtime-dispatched CPU repacking**: CPU種類に応じてAVX2 / AVX-512など利用可能な命令を実行時に選び、量子化weightをそのCPUで行列積しやすい配置へ並べ替える。
- **decode / prefill attention改善**: prompt一括処理と1-token decodeで別々に適したattention kernelを使う。
- **GQA KV streaming**: GQA（Grouped-Query Attention）で共有されるK/V headを、不要に複製せずstreamしながら計算してmemory trafficを削減。
- **量子化MoE indexed-expert GEMV**: routingされたexpertだけをindexで選び、1-token decode向けのmatrix-vector multiply（GEMV）を量子化weightのまま実行。

Qwen3-4B Q4K decodeは **1.79〜1.81倍**、Gemma4-E4B prefillは **2.2〜2.8倍**。[PR #2311](https://github.com/EricLBuehler/mistral.rs/pull/2311)

### 2026-08-14 — v0.9.1（released）

- **true LoRA kernel**: LoRAの低rank追加計算をbase weightへ事前mergeせず、推論時に専用kernelで実行する経路を追加。adapterを差し替えやすくする。
- **dynamic adapter loading**: serverを再起動せず、requestや利用状況に応じてLoRA adapterをload / unloadできるようにする。
- **LM head / embedding quantization**: 出力語彙projectionとembeddingも低bit化し、巨大語彙modelのmemory使用量を削減。
- **concurrent serving scheduler**: 複数requestを同時に進めるschedulerを追加し、1 requestずつ直列処理する場合のGPU idleを減らす。

[PR #2351](https://github.com/EricLBuehler/mistral.rs/pull/2351)

### 2026-08-20 — v0.9.2（released）

- **MTP speculative decoding**: modelのMTP（Multi-Token Prediction; 複数token予測）headでdraft tokenを作り、本体modelでまとめて検証する。
- **device-side verification**: draft token受理判定をCPUへ戻さずGPU側で進め、GPU→CPU同期を減らす。
- **batch argmax**: 複数token位置の最大logit選択をbatchでまとめ、kernel launch数を削減。
- **GDN rollback**: recurrent / GDN系modelでdraft tokenが拒否されたとき、stateを最後に確定したtoken位置まで戻せるようにする。

27B Q4／GB10で **19.5 → 24.6 tok/s**、code promptでは **21.3 → 29.4 tok/s**。[PR #2385](https://github.com/EricLBuehler/mistral.rs/pull/2385)

### 同release — DFlash

- **batch drafter**: 複数requestのdraft生成をまとめる。
- **受理率EMAによるdraft depth選択**: acceptance rateの指数移動平均（Exponential Moving Average; EMA）を見て、先読みtoken数を動的に増減する。
- **CUDA Graph**: draft / verify kernel列を事前captureし、CPU launch overheadを削減。

同時実行8 requestで約 **70 → 86.7 tok/s**。[PR #2388](https://github.com/EricLBuehler/mistral.rs/pull/2388)

[リリース一覧](https://github.com/EricLBuehler/mistral.rs/releases)

### 用語メモ

- **GEMV（General Matrix-Vector Multiplication; 行列×ベクトル積）**: 1 token decodeで多用される計算。batchが小さいためmemory bandwidth律速になりやすい。
- **repacking**: 量子化weightの数値自体は変えず、CPU/GPUが読みやすいmemory layoutへ並べ替えること。
- **device-side verification**: speculative decodingの受理判定をGPU上で完結し、CPUとの往復を減らす実装。
