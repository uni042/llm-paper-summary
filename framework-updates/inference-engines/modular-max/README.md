# Modular MAX

Modular MAXの主要な機能・性能更新を継続的に記録する集約ページ。FP8 / INT8系低精度KV、tiered KV cache、仮想memory allocator、MoE並列、投機的デコード（speculative decoding）、compile cacheなどを扱う。

## 現在できること

- **NVIDIA / AMD GPU向けcompiled serving**: LLM serving graphを事前compileし、runtime時にPythonやframeworkの動的dispatchを繰り返す量を減らせる。model graphとkernel選択をまとめて最適化し、同じmodel / shapeの繰り返し実行を軽くする。
- **continuous batching**: 到着時刻・生成長の異なる複数requestを継続的にbatchへ出し入れできる。固定batchの終了待ちを避け、GPUをより高い利用率で回せる。
- **paged KV cache**: requestごとのKVを固定した大きい連続領域ではなくpage単位で割り当て、長さの違うrequestが混在してもmemory断片化と過剰予約を抑えられる。
- **tiered KV cache**: KVをGPU HBMだけでなくCPU DRAM、disk等の下位tierへ置ける。hotなKVをGPUへ残し、coldなconversation / prefixを下位tierへ逃がすことで、GPU memory容量を超えるsession stateを保持できる。
- **非同期KV onload / offload**: 下位tierから必要なKVをGPUへ戻す処理をGPU計算と重ね、decode直前までcopy完了を待つ時間を減らせる。tiered cacheの性能はPCIe / storage bandwidthとprefetch精度に依存する。
- **低bit KV cache**: FP8 / MXint8等でKVを保持し、BF16等よりtoken当たりのcache量を減らせる。同じGPU memoryでcontext長や同時request数を増やせるが、量子化誤差と対応kernelが制約になる。
- **仮想memory allocator**: VMMで仮想addressとphysical GPU pageを分離し、長時間servingで発生するmemory断片化を抑えられる。大きなKV / workspace領域を確保し直すためにserverを止める必要を減らす狙いがある。
- **multi-GPU parallelism**: tensor / data / expert parallelismを組み合わせ、dense部分とMoE expert部分を別の分割軸で複数GPUへ配置できる。model sizeとrequest並列度の両方を拡張できる。
- **MoE routed / shared expertの並行実行**: routingされたexpert群と全tokenが通るshared expertを別streamで同時実行し、片方が終わるまで待つ直列部分を減らせる。低bit MoEも組み合わせてexpert weightのmemoryを削減できる。
- **投機的デコード**: EAGLE / DFlash系でdraft tokenを先に作り、target modelでまとめてverifyできる。draft生成・verify・cache移動を重ねるschedulerにより、単にtoken候補を増やすだけでなくpipeline全体のidleを減らす。
- **draft側KVのoffload**: speculative decodingではtargetだけでなくdraft modelもKVを持つためVRAM消費が増える。draft KVをCPU / diskへ逃がして、投機的デコードを有効にしてもtarget model用VRAMを圧迫しすぎない構成を取れる。
- **compiled artifact cache**: 一度compileしたmodel / shapeの実行artifactを保存し、次回起動時や同一graph再利用時のcompile待ちを短縮できる。interactive servingでfirst request latencyを抑えるのに効く。
- **CUDA Graph系の繰り返し実行**: decode等で繰り返すkernel列をgraphとして再利用し、1 tokenごとのCPU launch overheadを減らせる。

以下の更新履歴は、これらの主要能力について**GPU外KVをどこまで実用的に使えるか、低bit cacheとVMMでmemory容量をどこまで伸ばせるか、MoE・speculative decoding・compileの待ち時間をどこまで重ねて隠せるか**を追う。

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
