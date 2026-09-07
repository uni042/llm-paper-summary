# TensorRT-LLM

TensorRT-LLMの主要な機能・性能更新を継続的に記録する集約ページ。正式release前のrelease candidate（RC）は、stable版と混同しないよう明示して記録する。

この期間は、**KV cacheをGPU外へ階層化すること、prefill / decodeを別workerへ分離すること、CUDA Graph適用範囲を広げること、MoE通信と低bit KVを強化すること**が中心。

## 現在できること

- **NVIDIA GPU向けcompiled LLM serving**: modelをTensorRT-LLM向けengine / runtimeへbuildし、NVIDIA GPU用に選ばれたattention、GEMM、normalization、MoE等のkernelで実行できる。Python model codeをそのまま逐次実行するより、graph・precision・kernelをまとめて最適化することを狙う。
- **continuous / in-flight batching**: 生成途中のrequestをbatchへ出し入れし、終了したrequestのslotへ新着requestを入れられる。固定batchの終了待ちを減らし、GPU throughputを高く保ちやすい。
- **paged KV cache**: KVをpage / block単位で確保し、長さの違うrequestが混在しても大きな連続領域をrequestごとに予約せずに済む。block reuseとprefix reuseにより同じKVを再利用できる。
- **KV cacheの階層化**: GPU HBMだけでなくCPU memory、disk等の下位tierへKVをoffloadし、必要なblockだけprefetch / onloadできる。GPU memory容量を超えるconversation / contextを保持できる一方、PCIe / storage I/Oがlatencyへ効く。
- **cold KV compression**: しばらく使わないKV pageを低bit / codecで圧縮し、下位tierの保存容量と再転送量を減らせる。hot pageとcold pageでprecision / storage costを分ける考え方。
- **conversation / prefix KV reuse**: 過去conversationや同じprefixから作ったKV blockを再利用し、system promptや長い共通contextを繰り返しprefillする計算を減らせる。
- **prefill / decode分離**: promptをまとめて処理するprefill workerと、1 tokenずつ生成するdecode workerを別GPU群へ分けられる。phaseごとのcompute / bandwidth特性に合わせ、cluster resourceを別々に割り当てられる。
- **KV transceiver / connector**: prefill側で生成したKVをdecode側や外部cacheへ送受信できる。NIXL等を使ってGPU間 / node間data movementを行い、CPU stagingや再計算を減らせる。
- **tensor / pipeline parallelism**: dense modelを複数GPUへ分割し、単一GPUに収まらないmodelを実行できる。model size、layer構成、GPU間linkに応じて分割方法を選ぶ。
- **expert parallelism / MoE**: MoE expertを複数GPUへ分散し、routingされたtokenだけを対応expertへ送る。All-to-All通信でpaddingや不要writeを減らし、低bit expert kernelも使える。
- **低bit weight / activation**: FP8、FP4、NVFP4、INT8等のprecisionでweightやactivationを扱い、HBM使用量・HBM traffic・matrix compute costを削減できる。hardware世代ごとのTensor Core対応が性能を左右する。
- **低bit KV cache**: FP8 / FP4等でKV自体を保持し、長contextで支配的になるcache memoryとworker間転送量を減らせる。model weightとKVを別precisionで最適化できる。
- **投機的デコード**: EAGLE、DFlash、DSpark等で複数token候補をdraftし、target modelでまとめて検証できる。候補が受理されればtarget forward回数を減らせる。
- **tree型speculative decoding**: draft候補を単一列ではなくtree状に展開し、複数branchを1回のtarget実行で検証できる。途中tokenが外れても別branchを採用できる可能性を残し、acceptanceを上げる狙いがある。
- **chunked / fine-grained prefill**: 長いpromptを小さいchunkへ分け、schedulerがdecode requestと混ぜて実行できる。巨大prefillによるmemory peakとdecodeの長時間stallを減らせる。
- **context / sequence parallel系実行**: 長いsequenceのattention / KVを複数GPUへ分割し、1 GPU当たりのKV memoryとattention workを減らせる。long-context modelをmulti-GPUへ拡張する手段。
- **CUDA Graph**: decode等で繰り返すkernel列をcaptureし、CPUから毎token大量のkernelをlaunchするoverheadを減らせる。prefillもshape bucketごとにcaptureし、適用範囲を広げられる。
- **breakable / dynamic Graph利用**: Graph化できない一部operationだけ通常kernel pathへ逃がし、それ以外をGraphのまま実行できる。完全固定shapeを要求する場合よりproduction workloadへ適用しやすい。
- **fused kernel**: attention前後のnormalization、quantization、MoE routing / MLP等をまとめ、中間tensorのHBM書き戻しとkernel launch回数を減らせる。
- **memory pool / VMM管理**: GPU仮想memoryを使って大きなKV / workspace poolを柔軟に割り当て、長時間servingの断片化やprocess間memory共有を改善できる。
- **multimodal pipeline**: vision encoder等を含むmodelも実行し、encoder側にもCUDA Graph等の最適化を適用できる。text decoder以外の前処理計算も同じruntime stackへ統合できる。
- **distributed serving coordination**: Ray等を使って複数workerを管理し、P/D分離、multi-GPU parallelism、KV poolをclusterとして構成できる。単一engineだけでなく大規模NVIDIA serving stackとして使える。
- **production向けC++ runtime**: cache managerやcritical pathをC++側へ寄せ、Python scheduling / object overheadを減らす方向の設計を取る。TensorRT / CUDA ecosystemと密接に連携することが強み。

以下の更新履歴は、**KVCacheManager、tiered KV、P/D分離、低bit KV / MoE、投機的デコード、Graph実行**がstable / RCでどう広がったかを追う。

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
