# SGLang

SGLangの主要な機能・性能更新を継続的に記録する集約ページ。投機的デコード（speculative decoding）、階層KV cache（hierarchical KV cache）、MoE負荷分散、GPU間通信、CUDA Graph、長文向けattention最適化などを扱う。

## 現在できること

- **高throughput serving**: continuous batching、paged attention、chunked prefillを使い、長prompt requestと短いdecode requestを同じGPU上で効率よく混在させられる。
- **prefix cache**: RadixAttention系のcacheで同じprefixを持つrequestのKVを共有し、system prompt、tool履歴、tree状のagent workflowでprefill再計算を減らせる。
- **階層cache**: KVやhybrid / recurrent stateをGPUだけでなくCPU等の下位tierへ保持し、必要なblockだけGPUへ戻せる。長contextや高並列servingでHBM使用量を抑えられる。
- **prefill / decode分離と分散serving**: prefillとdecodeを別workerへ分け、tensor / pipeline / expert / data parallelismと組み合わせてclusterを構成できる。
- **MoE serving**: expert parallelism、token dispatcher、負荷分散、shared expert最適化を使い、routingの偏りとGPU間All-to-All通信を抑えられる。
- **投機的デコード**: draft model、MTP、DSpark等で複数token候補を先に作り、target verify回数を減らせる。長context向けにはdraft stepのmetadata再利用やcache削減も行う。
- **量子化と低bit execution**: FP4 / FP8 / INT4 / AWQ / GPTQ等を使い、weight・activation・KVのmemory trafficを削減できる。
- **structured output / multi-LoRA**: grammar / JSON等の制約付き生成や、複数LoRA adapterを同一serverでbatch処理する運用に対応する。
- **RL / post-training rollout**: 学習frameworkからrollout backendとして呼び出し、policy modelの生成を高速serving側で処理できる。
- **CUDA Graph / kernel最適化**: recurrentなdecode stepやMoE前後処理をGraph / fused kernelへまとめ、CPU同期と小kernel起動を減らせる。

以下の更新履歴は、**cache階層、長文処理、MoE負荷分散、speculative path、GPU同期削減**の拡張を追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 要点

この期間のSGLangは、**1 tokenずつ本体modelを呼ぶ回数を減らす投機的デコード、KVやrecurrent stateをGPU外も含めて再利用するcache、MoEでtokenが偏ったときの負荷分散、GPU kernel起動・CPU/GPU同期の削減**を同時に進めている。

特にrelease noteには独自略語が多いため、以下では「何を減らす変更か」を基準に整理する。

## 主要更新

- **2026-06-13 — v0.5.13（released）**: 投機的デコード基盤のSpec V2を既定化。draft / verify処理の途中でCPUとの同期が頻発しないよう、FutureMapとforward-stream転送でstepごとの待ち合わせを減らした。

  **HiCache**はKV cacheやhybrid model stateをGPUだけでなくCPUなど下位階層にも保持し、必要なblockだけ戻す階層cache。hybrid modelで既定化され、Intel CPU+GPUを使うEPD構成ではP99 TTFTとrequest throughputを最大約1.3倍改善。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.13)

- **2026-06-26 — v0.5.14（released）**: recurrent modelが次tokenへ持ち越すstateをINT8で保存するcheckpoint pool、投機的デコード用convolution windowの重複cache削減、MoE expert間の負荷を均すWaterfill / LPLB、NVFP4 MoEを追加。

  convolution-window cacheの重複排除ではcache footprintを約半分へ削減。KDA CuteDSL prefill kernelはTriton実装比 **1.08〜1.52倍**。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.14)

- **2026-07-10 — v0.5.15（released）**: Spec V2 schedulerでGPU→CPU（D2H）/ CPU→GPU（H2D）の同期を減らし、metadata処理もfusionしてend-to-end TPSを **11%向上**。

  **IndexShare MTP**はMTP（Multi-Token Prediction; 複数token予測）の各draft stepで長いcontext indexを毎回作り直さず共有し、長文時のdraft計算costを最大 **1.9倍削減**。sparse FlashMLAは、長いcontextのうちattentionで実際に読む位置を絞り、長文throughputを **10%以上改善**。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.15)

- **2026-07-25 — v0.5.16（released）**: draft候補を信頼度に応じて増減するconfidence-driven DSpark、DSAのcache layer分割、ReplaySSM向けRing Spec-Verifyを追加。

  context parallelismを4分割するCP4では、各GPUが保持するKV memoryを **74%削減**。投機候補を検証するための一時領域（spec verification scratch）も **11.5 → 1.8 GB/GPU**へ削減。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.16)

- **2026-08-22 — v0.5.18（released）**: model checkpointをGPUへ読み込む処理とCUDA Graph captureを並行し、起動時間を **84.8秒 → 35.6秒**へ短縮。

  tensor parallelism（TP）でLM Headの結果をGPU間共有するとき、複数通信を単一All-to-Allへまとめ、B200で **320 → 169 µs**。TPOT（Time Per Output Token; 出力1 tokenあたり時間）は **36.97 → 35.67 ms**。[release](https://github.com/sgl-project/sglang/releases/tag/v0.5.18)

### 用語メモ

- **投機的デコード（speculative decoding）**: 小さいdraft modelやMTP headで将来token候補を先に作り、大きな本体modelでまとめて検証することで、本体model呼び出し回数を減らす方式。
- **階層cache（hierarchical cache）**: 高速・小容量のGPU memoryと、低速・大容量のCPU memoryなどをcache階層として使い分ける方式。
- **D2H / H2D**: Device-to-Host / Host-to-Device。GPU→CPU、CPU→GPU転送を指す。
- **TPOT（Time Per Output Token; 出力tokenあたり時間）**: 生成開始後に1 tokenを追加するのにかかる時間。
