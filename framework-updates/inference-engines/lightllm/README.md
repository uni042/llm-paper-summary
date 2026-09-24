# LightLLM

LightLLMの主要な機能・性能更新を継続的に記録する集約ページ。GPU / CPU / diskへまたがるKV・recurrent state cache、prefill/decode分離、MoE kernel、投機的デコード（speculative decoding）、RL serving向けweight更新などを扱う。

## 現在できること

- **高並列LLM serving**: continuous batchingとtoken単位schedulerで、生成長や到着時刻が異なる多数requestを同じGPU上で継続的に処理できる。1つの長いrequestがbatch全体の終了を待たせる固定batch方式よりGPU idleを減らせる。
- **prefix / Radix cache**: 同じtoken prefixを持つrequest間でKVを共有し、system promptや長い共通contextのprefillを繰り返さずに済む。cache hitが高いagent / chat workloadではTTFTとGPU計算量を大きく減らせる。
- **hybrid architecture向けstate cache**: full attentionのKVと、linear attention / SSM / convolution layerが持つrecurrent stateを同一粒度で扱わず、それぞれに合う保存単位で管理できる。hybrid modelで不要なpaddingやmemory浪費を抑えられる。
- **GPU→CPU→diskの階層cache**: GPU HBMだけでなくCPU DRAM、local diskまでKV / recurrent stateの退避先にできる。GPUに残すhot dataと下位tierへ逃がすcold dataを分け、長contextや多数sessionをGPU memory容量以上に保持できる。
- **CPU側KV量子化とNUMA配置**: CPUへ退避したKVをFP8 / INT8等へ低bit化してhost RAM使用量と再転送量を減らせる。multi-socket serverでは担当GPUに近いNUMA nodeへcacheを置き、不要なCPU interconnect経由を避けられる。
- **prefill / decode分離**: 長いpromptを処理するprefill workerと1 tokenずつ生成するdecode workerを別GPU群へ分けられる。必要なKVをworker間で転送し、prefillの大きいbatch処理とdecodeの低latency要求を別々に最適化できる。
- **cache-aware scheduling**: requestをどのworkerへ送るか決めるとき、必要なKVがすでにどこに存在するかを考慮できる。load balanceだけでなく、KV再計算やworker間転送を減らす方向へscheduleできる。
- **MoE distributed execution**: tensor / data / expert parallelismを使い、MoE expertを複数GPUへ分散できる。routing後のtoken整理、expert計算、通信前後処理をfused kernelへまとめ、細かいkernel launchやmemory trafficを減らせる。
- **量子化と低精度実行**: FP8 / INT8 / AWQ等のweight・activation・KV形式を使い、model weightとcacheのmemory footprint、HBM trafficを削減できる。用途に応じてmodel本体とKVを別精度で運用できる。
- **投機的デコード**: MTP / EAGLE系で複数token候補を先に作り、target modelでまとめて検証できる。候補受理率が高ければtarget forward回数を減らせる。
- **RL / post-training rollout連携**: rollout serverを停止せず、training processで更新されたweightをonlineで反映できる。weight更新後は古いweightで作ったKV / prefix cacheをflushし、pause / resumeを含めて「生成→学習→新weightで再生成」のloopを回せる。
- **NIXL等を使うdata movement**: GPU / CPU / remote worker間のKV転送を専用data movement layerへ載せ、serving runtime本体が転送方式を個別実装する負担を減らせる。

以下の更新履歴は、これらの主要能力について**cacheをどのmemory階層まで広げられるか、P/D分離時のKV移動をどこまで減らせるか、MoEやRL rolloutの実行経路をどう軽くできるか**を中心に追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-08-10 — v1.2.0（released）

#### RL serving向けonline更新

- **online weight update**: RLHF / reinforcement-learning serving中に、別training processで更新されたmodel weightをserver停止なしで反映できるようにする。
- **cache flush**: weightが変わった後、古いweightで作ったKV / prefix cacheを明示的に無効化する。
- **pause / resume**: rollout workerを一時停止し、weight交換後に再開できる制御を追加。

これは通常の固定model servingより、trainingとinferenceを交互に回すRL workload向けの機能。

#### Hybrid Radix Cache

**Hybrid Radix Cache**は、同じprefix token列をradix treeで共有しながら、model architectureごとに異なるstateを別粒度で管理するcache。

- full-attention layer: tokenごとのKV block
- linear attention / convolution layer: convolution stateやSSM state

を同一cache objectとして雑に扱わず、それぞれに合うpage粒度で保存する。

hybrid modelでは「attention layerは大量KVを持つが、linear layerは小さいrecurrent stateを持つ」といった違いがあるため、同じblock sizeを強制するとmemoryを浪費しやすい。Hybrid Radix Cacheはこの差を吸収し、CPU offloadにも対応する。

#### multi-level cache

cache階層を、

`GPU → CPU → disk`

まで拡張し、以下をまとめて扱う。

- **quantized CPU KV**: CPUへ退避したKVを低bit化し、host RAM使用量とGPUへ戻す転送量を削減。
- **FP8 / INT8 KV**: cacheを低精度で保持して容量を増やす。
- **NUMA-aware placement**: 複数CPU socket環境で、担当GPUに近いCPU memoryへcacheを置く。
- **NIXL transfer**: GPU / CPU / remote worker間でKVを高速転送するdata movement layerを利用。
- **cache-aware P/D scheduling**: prefill / decode workerを選ぶとき、必要なKVがすでにどこへ存在するかを考慮し、無駄なcache移動を減らす。

#### その他

- **MTP / EAGLE**: 複数token候補を先に生成し、本体modelでまとめて検証する投機的デコード方式。
- **TMA MoE kernel**: Hopper GPUのTMA（Tensor Memory Accelerator）を使い、expert weight / activationのglobal memory↔shared memory転送を計算と重ねる。
- **fused MoE preparation**: routing後のexpert index整理やtoken並べ替えなど小処理をまとめ、kernel launchとmemory trafficを減らす。
- **disk cache v1.0**: CPU memoryからも溢れるKV / stateをlocal diskへ退避する正式path。
- **AWQ / FP8**: weight量子化と低精度実行形式の対応拡張。

release本文には比較可能なend-to-end性能値が掲載されていないため、ここでは機能・architecture変化として記録する。

[release](https://github.com/ModelTC/lightllm/releases/tag/v1.2.0)

### 用語メモ

- **Radix cache**: token prefixをtreeとして共有し、同じprefixを持つ複数requestでKVを再利用するcache。
- **NUMA（Non-Uniform Memory Access）**: CPU socketによってmemoryへの距離・帯域が異なる構成。GPUに近いNUMA nodeへbufferを置くとPCIe転送が速くなりやすい。
- **P/D scheduling**: prompt処理のprefill workerとtoken生成のdecode workerを別々に選ぶscheduler。
- **TMA（Tensor Memory Accelerator）**: NVIDIA Hopper世代で大きなtensor block転送を専用hardwareへ任せ、GPU computeとmemory copyを重ねやすくする機能。
