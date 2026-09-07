# LightLLM

LightLLMの主要な機能・性能更新を継続的に記録する集約ページ。GPU / CPU / diskへまたがるKV・recurrent state cache、prefill/decode分離、MoE kernel、投機的デコード（speculative decoding）、RL serving向けweight更新などを扱う。

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
