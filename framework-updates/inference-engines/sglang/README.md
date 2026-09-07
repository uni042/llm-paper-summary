# SGLang

SGLangの主要な機能・性能更新を継続的に記録する集約ページ。投機的デコード（speculative decoding）、階層KV cache（hierarchical KV cache）、MoE負荷分散、GPU間通信、CUDA Graph、長文向けattention最適化などを扱う。

## 現在できること

- **高throughput multi-request serving**: continuous batchingで生成途中のrequestをbatchへ出し入れし、paged attentionで長さの異なるKVをpage単位に管理できる。固定batchの終了待ちとKVの過剰予約を減らし、GPUを多数requestで共有しやすい。
- **chunked prefill**: 長いpromptを小さいchunkへ分け、decode requestと混ぜて処理できる。1件の巨大prefillが他requestのtoken生成を長時間止める問題を抑え、TTFTとTPOTのbalanceを取りやすくする。
- **RadixAttention / prefix cache**: token prefixをradix treeとして管理し、同じsystem prompt、tool履歴、document prefix等を持つrequest間でKVを共有できる。agent treeやmulti-turn chatで同じprefixを何度もprefillする計算を減らせる。
- **階層cache**: KVやhybrid / recurrent stateをGPU HBMだけでなくCPU等の下位tierへ置き、必要なblockだけGPUへ戻せる。HBM容量を超えるcontext / session stateを保持できる一方、host-device転送量が新しい律速になる。
- **hybrid / recurrent state cache**: full attentionのKVだけでなく、linear attention、SSM、convolution等が持つstateもmodelに合う形式で保持できる。通常KVとは違うstateを一律pageへ押し込まず、memoryの無駄を減らせる。
- **prefill / decode分離**: prefill workerとdecode workerを別GPU群へ分け、KVをworker間で転送できる。prefillは大きいmatrix throughput、decodeは低latency / memory bandwidthを重視するなどphaseごとに最適化できる。
- **tensor / pipeline / data parallelism**: dense modelを複数GPU / nodeへ分割し、model sizeとrequest throughputの両方を拡張できる。parallel groupをserving topologyへ合わせて組み合わせられる。
- **expert parallelism / MoE serving**: MoE expertをGPU間へ分散し、routingされたtokenを対応expertへ送る。token dispatcher、All-to-All通信backend、shared expert最適化を組み合わせられる。
- **MoE load balancing**: expertごとのtoken偏りを観測し、重いexpertへの集中を緩和するrouting / placement調整を利用できる。平均負荷だけでなくtail側の混雑を減らし、遅いexpertがlayer全体を待たせる時間を抑える。
- **投機的デコード**: draft model、MTP、DSpark等で複数token候補を先に生成し、target modelでまとめてverifyできる。受理率が高ければtarget forward回数を減らせる。
- **adaptive draft制御**: confidenceや過去の受理状況を使って候補数を増減し、外れtokenを大量に作る無駄を減らせる。長contextではdraft用index / metadataを再利用して補助処理costも抑える。
- **recurrent model向けspeculative verify**: draft tokenが拒否されたときにrecurrent stateを正しい位置へ戻しながら、Transformer以外のstateful architectureでもmulti-token verifyを扱える。
- **sparse / long-context attention**: 長いcontextの全位置を毎回attentionせず、重要なsubsetだけ読むsparse attention / sparse MLA系kernelを利用できる。KV read量とattention計算をcontext長に対して削減できる。
- **context parallelism**: 長contextのKV / attentionを複数GPUへ分割し、1 GPU当たりのcache memoryを減らせる。長文modelを単一GPUのHBM制約から拡張するための手段。
- **量子化**: FP4、FP8、INT4、AWQ、GPTQ等のweight / activation / KV形式を利用できる。model memory、HBM traffic、KV capacityを用途に応じて削減できる。
- **multi-LoRA serving**: 複数LoRA adapterを同じbase model上でrequestごとに切り替え、batch内で処理できる。base weightを複製せず複数tenant / taskを1 serverへ載せられる。
- **structured output**: grammar、JSON schema等でtoken候補を制約し、parse可能なresponseを直接生成できる。tool callingやdata extractionで後処理failureを減らせる。
- **CUDA Graph**: decodeや投機的verifyの繰り返しkernel列をcaptureし、1 tokenごとのCPU launch overheadを削減できる。dynamic servingと固定Graphを両立するため、shape / buffer管理もruntime側で行う。
- **kernel fusion / CPU-GPU同期削減**: routing、metadata処理、D2H / H2D copy前後の小operationをまとめ、GPUがCPUの判断を待つ回数や中間tensorのHBM trafficを減らせる。
- **RL / post-training rollout backend**: RLHF / RL training frameworkからpolicy modelのgeneration backendとして呼び出し、高throughput rolloutを生成できる。trainingとservingを別runtimeへ分けつつ、weight更新後のrolloutへつなげる用途に使える。
- **OpenAI互換API / production serving**: applicationからchat / completion endpointとして利用でき、単一GPUからdistributed clusterまで同じserving stackで構成できる。
- **structured LLM program実行の系譜**: 単純な1 request = 1 promptだけでなく、branch、tool call、共有prefixを持つLLM applicationの実行をruntime側で効率化する設計を持つことがSGLangの特徴。

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
