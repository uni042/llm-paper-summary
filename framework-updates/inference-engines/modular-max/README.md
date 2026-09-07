# Modular MAX

Modular MAXの主要な機能・性能更新を継続的に記録する集約ページ。FP8 / INT8系低精度KV、tiered KV cache、仮想memory allocator、MoE並列、投機的デコード（speculative decoding）、compile cacheなどを扱う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-18 — MAX v26.4（released）

- **native FP8 attention / FP8 KV cache**: attention計算とKV cacheをFP8のまま扱う経路を追加し、BF16へ毎回展開するmemory trafficを減らす。

  KVをBF16からFP8へすると1要素あたりの保存量をほぼ半分にできるため、同じGPU memoryで保持できるcontext長や同時request数を増やせる。release noteでは精度はBF16相当を維持しつつKV capacity約2倍と報告。

- **EAGLE draft KVのhost / disk offload**: 投機的デコードでdraft model側が作るKVをGPUへ常駐させず、CPU memoryやdiskへ退避できるようにする。draft modelを追加したことでVRAM不足になる問題を緩和する。

- **speculative overlap scheduler**: draft生成、target verify、cache移動などを直列に待たず、依存しない部分を同時進行させるschedulerを追加。

- **TP + EP**: tensor parallelism（TP）とexpert parallelism（EP）を組み合わせ、dense部分とMoE expert部分を複数GPUへ別方式で分割できるようにする。

- **FlashAttention-4 prefill**: B200で **1.05〜1.5倍**のprefill高速化を報告。

[release notes](https://max.modular.com/releases/v26.4/)

### 2026-08-11 — MAX v26.5（released）

- **NVIDIA / AMD VMM defragmenting allocator**: VMM（Virtual Memory Management; 仮想memory管理）を使い、GPU上の仮想addressと実physical pageを分離して管理するallocatorを追加。

  長時間servingで大小さまざまなKV / workspaceを確保・解放すると、空きmemoryが細切れになる**断片化（fragmentation）**が起きる。VMM allocatorはphysical pageを再配置しつつ仮想addressを保ち、連続した大領域を確保しやすくする。

- **compiled graph内weight sharding**: 複数GPUへ分割したweightを、compile済みgraphの中で直接扱う。graph外で毎回split / gatherする処理を減らす。

- **MXint8 KV cache**: blockごとのscaleを持つ8-bit整数KVを追加。BF16 KVに比べmemoryを約半分へ削減する方向の機能。

- **Rust tiered KV connector + async onload**: GPU外のKV tierと接続するdata movement層をRustで実装し、下位tierからGPUへKVを戻す処理を非同期化。GPU計算中に次requestのKVを先読みできるようにする。

- **DP-EP NVFP4**: data parallelismとexpert parallelismを組み合わせたMoEでNVFP4 weight / stateを使い、対象構成で **約10 GiB/GPU削減**。

- **shared expertをside streamで実行**: routed expertとは別に全tokenが通るshared expertを別CUDA streamへ載せ、両者を同時実行する。片方の終了を待ってからもう片方を始める直列実行を避ける。

- **warm MEF cache**: compile済み実行artifactをcacheし、同じshape / modelを再利用するとき初回compileを省く。first-call compileを **約5.6秒 → 16.7 ms**へ短縮。

- **DFlash**: 投機的デコードのdraft / verifyを最適化し、decode最大 **約1.3倍**。

[release notes](https://max.modular.com/releases/v26.5/)

### 用語メモ

- **tiered KV cache**: KVをGPUだけでなくCPU、disk、remote memoryなど複数階層へ置く方式。
- **VMM（Virtual Memory Management; 仮想memory管理）**: programから見えるaddressと実際のGPU physical memory pageを分離し、再配置や大領域管理をしやすくする仕組み。
- **onload**: CPU / diskなど下位memory tierにあるdataをGPUへ戻す処理。offloadの逆。
- **side stream**: main computeとは別CUDA streamで独立処理を走らせ、可能な範囲で同時実行する方式。
