# Mistral.rs

Mistral.rsの主要な機能・性能更新を継続的に記録する集約ページ。CPU量子化kernel、attention、MoE、LoRA、投機的デコード（speculative decoding）、CUDA Graph、同時request schedulingなどを扱う。

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
