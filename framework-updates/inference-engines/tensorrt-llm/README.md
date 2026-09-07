# TensorRT-LLM

TensorRT-LLMの主要な機能・性能更新を継続的に記録する集約ページ。正式release前のrelease candidate（RC）は、stable版と混同しないよう明示して記録する。

この期間は、**KV cacheをGPU外へ階層化すること、prefill / decodeを別workerへ分離すること、CUDA Graph適用範囲を広げること、MoE通信と低bit KVを強化すること**が中心。

## 現在できること

- NVIDIA GPU向けにLLMをcompile・最適化し、paged KV cache、continuous batching、量子化、multi-GPUで高throughput servingできる。
- tensor / pipeline / expert parallelismやprefill/decode分離を使い、複数GPU・複数nodeへ拡張できる。
- KV cacheをpage単位で管理し、CPUやdiskなどGPU外tierへ退避・再利用する構成を取れる。
- FP8 / FP4 / NVFP4等の低bit weight・KV・MoE実行と、EAGLE系を含む投機的デコードを利用できる。
- CUDA Graphや専用kernelを使って、decode時のCPU launch overheadとGPU memory trafficを削減できる。

以下の更新履歴は、特に**KVCacheManagerV2、disk / tiered KV、P/D分離、CUDA Graph、MoE通信、低bit KV**の拡張を追っている。RC機能はstable releaseと分けて扱う。

## 初期収録期間

2026-06-03〜2026-09-03

対象期間の更新はv1.3.0 release candidate群で、以下はすべて**正式版前（pre-release）**の機能である。

## 主要更新

### 2026-06-10〜06-30 — rc18〜rc20

- **GPU間memory共有基盤をCUDA IPCからVMM / MNNVLへ拡張**: VMM（Virtual Memory Management; GPU仮想memory管理）を使い、複数process / GPU間でmemory領域をより柔軟に共有・再配置できるようにする方向へ移行。
- **KVCacheManagerV2**: KV cache blockの割当、再利用、offload、外部tierとの転送をまとめて扱う新cache managerをC++側へ導入。
- **disk KV cache**: GPU / CPU memoryだけでなくdiskもKVの下位階層として利用できるようにする。
- **非同期Ulysses（async Ulysses）**: 長いsequenceを複数GPUへ分割するsequence parallel系通信を、計算とより重ねて実行する。
- **EAGLE3 dynamic tree**: 投機的デコード（speculative decoding）で候補tokenを固定本数ではなくtree状に展開し、状況に応じて検証する。
- **KV prefetch block数制御**: 下位tierからGPUへKVを戻す際、先読み量を明示的に調整できるようにする。
- **MXFP8 / NVFP4 MoE**: MoE expert計算を低bit形式で実行し、memory量とmatrix multiply costを削減。
- **multimodal encoderのCUDA Graph対応**: 画像などのencoder側にもCUDA Graphを適用し、CPU launch overheadを減らす。

[rc18](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc18) [rc19](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc19) [rc20](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc20)

### 2026-07-15〜07-31 — rc21〜rc23

- **KV cache transceiver / offload**: KV blockを別workerや別memory tierへ送受信する役割をcache managerへ統合。
- **分離serving coordinator（disaggregated coordinator）**: promptを処理するprefill workerと、token生成するdecode workerを別GPU群へ分ける構成を管理。
- **DFlash / DSpark**: draft候補を先に作り本体modelでまとめて検証する投機的デコード方式を追加。
- **FP4 KV cache**: KV cache自体を4-bit形式で保持し、context長あたりmemoryを削減。
- **runtime KV compression**: 実行中にKVを圧縮し、cache容量と転送量を減らす。
- **fine-grained context chunk**: 長いpromptをより細かいchunkへ分け、prefillのmemory peakとscheduler自由度を改善。
- **conversation単位KV reuse**: 会話の共通prefixなど、以前計算したKVをrequestをまたいで再利用する。

[rc21](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc21) [rc22](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc22) [rc23](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc23)

### 2026-08-12 — rc24

- **prefill CUDA Graph / capture bucket**: prompt長などが異なるrequestをいくつかのshape区分へまとめ、それぞれにCUDA Graphを事前captureする。完全一致shapeだけに限定するよりGraphを再利用しやすくする。
- **breakable graph**: Graph実行中でも一部処理だけ通常kernel pathへ逃がせる構成を追加し、CUDA Graphを適用できるworkload範囲を拡大。
- **KVCacheManagerV2 paged attention / block reuse**: KVを固定連続領域ではなくpage / block単位で管理し、解放済みblockや同一prefix blockを再利用。
- **batched KV compaction**: 断片化したKV block整理を複数requestまとめて処理し、管理overheadを削減。
- **Ray / NIXL disaggregation**: Rayでworker群を管理し、NIXLを使ってprefill→decode間のKVを高速転送する構成を追加。

[release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc24)

### 2026-08-31 — rc25

- **KVCacheManagerV2を主要modelで既定化**: 新cache管理系を実運用pathへ移行。
- **zero-copy token passing**: worker間でtoken情報を渡す際、不要な中間buffer copyを減らす。
- **distributed pool rebalance**: 複数workerにまたがるmemory / KV poolの偏りを再配分。
- **cold-page codec**: しばらく使わないKV pageを圧縮し、下位tierの容量・転送量を減らす。
- **DSA writeback overlap**: attention関連stateの書き戻しを次計算と重ね、critical pathから外す。
- **counted-write MoE A2A**: MoEのAll-to-All通信で、実token数に応じた送信量だけを扱いpaddingや不要writeを減らす。
- **tiered GVR TopK**: routing / Top-k処理をmemory階層と連携して効率化する実装を追加。

[release](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.3.0rc25)

## 読み方の注意

release noteには比較可能なend-to-end benchmarkが少なく、上記は「機能が入ったこと」と「内部pathが変わったこと」を中心に記録している。特にv1.3.0 RC群は正式版前なので、APIや既定値がstable releaseまでに変わる可能性がある。

### 用語メモ

- **KV cache**: 過去tokenのattention用Key / Valueを保存し、decode時の再計算を避けるmemory。
- **paged attention**: KVを小さいblock単位で管理し、requestごとの長さが違ってもVRAM断片化を抑える方式。
- **disaggregated serving**: prefillとdecode、あるいはexpert処理などを別GPU群へ分けるserving構成。
- **CUDA Graph**: GPU kernelの起動列を事前記録し、CPUから毎回kernelをlaunchするoverheadを減らす仕組み。
