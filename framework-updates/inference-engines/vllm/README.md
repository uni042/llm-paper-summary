# vLLM

vLLMの主要な機能・性能更新を継続的に記録する集約ページ。KV cacheの階層化、prefill / decode分離、MoE、投機的デコード（speculative decoding）、weight offload、GPU kernel改善など、実際のserving性能や必要memoryへ影響する更新を扱う。

## 現在できること

- **高throughput multi-request serving**: continuous batchingでrequestを生成途中でもbatchへ出し入れし、短いrequestが終わった後も新しいrequestを同じGPUへ流せる。固定batchの終了待ちを減らし、GPU utilizationとthroughputを上げる。
- **PagedAttention / paged KV cache**: requestごとのKVを固定した大きい連続領域ではなくpage単位で管理する。最大context分を事前予約するmemory浪費や外部断片化を減らし、同じGPUでより多くのrequestを保持できる。
- **prefix caching**: 同じprefixを持つrequest間で既計算KVを共有し、長いsystem prompt、RAG文書、agent履歴等のprefillを再計算せずに済む。cache hitが高いworkloadではTTFTとGPU計算量を大きく減らせる。
- **階層KV cache**: GPU HBMだけでなくCPU DRAM、peer / remote memory、object storage、disk等をKVの下位tierとして使える。hot KVだけをGPUに残し、cold KVを外へ逃がしてcontext長や同時session数をGPU memory容量以上に伸ばせる。
- **KV offload policy / eviction policy**: どのKVをGPUへ残し、どれを下位tierへ追い出すかをpolicyとして切り替えられる。単純LRUだけでなくworkload特性に応じてcache hitと転送量のbalanceを調整できる。
- **prefill / decode分離**: 長いpromptをまとめて処理するprefill workerと1 tokenずつ生成するdecode workerを別GPU群へ分けられる。prefillはcompute throughput、decodeはmemory bandwidth / latencyを重視するなど、phaseごとにhardwareを別最適化できる。
- **KV worker間転送**: P/D分離時にprefill側で作ったKVをdecode側へNIXL等で直接送れる。CPU stagingや再計算を減らし、network / RDMA経路へKV移動を載せられる。
- **E/P/D分離**: MoE expert計算、prefill、decodeを別GPU poolへ分ける構成も扱える。dense attentionとexpert計算のresource特性が異なる大規模MoE servingで、GPU poolを役割別に割り当てられる。
- **tensor / pipeline / data parallelism**: dense modelを複数GPU / nodeへ分散し、model sizeとrequest throughputの両方を拡張できる。parallelismごとに通信patternが異なるため、cluster topologyに応じて組み合わせる。
- **expert parallelism / MoE serving**: MoE expertをGPU間へ分散し、routingされたtokenだけを対応expertへ送る。DeepEP等のbackend、specialized routing kernel、shared expert分割を使い、All-to-All通信とexpert memoryを削減できる。
- **weight offload**: GPUへ常駐させるweight量を減らし、CPU等へ一部を置くことで単一GPU memoryを超えるmodelを実行できる。VRAM節約と引き換えにhost-device転送がdecode latencyへ効くため、model sizeと速度のtrade-offを調整する機能。
- **weight / activation / KV量子化**: FP8、INT8、INT4、FP4、NVFP4、MXFP4等の低bit形式をhardware / modelに応じて利用できる。model footprint、HBM traffic、KV capacityを別々に最適化できる。
- **投機的デコード**: draft model、MTP、DSpark、DFlash等で複数token候補を先に作り、target modelでまとめてverifyできる。受理率が高ければtarget forward回数を減らせる。
- **adaptive speculative decoding**: requestや直近の受理率を見てdraft token数を動的に増減し、候補を作りすぎる無駄とtarget forward削減のbalanceを取れる。workloadによって最適draft depthが変わる問題へ対応する。
- **chunked prefill / scheduling**: 長いpromptを小さいchunkへ分け、decode requestと混ぜてGPUへ流せる。巨大prefillがdecodeを長時間止めるhead-of-line blockingを減らし、TTFTとITLの両立を狙える。
- **sequence / context parallel系実行**: 長contextのattentionやKVを複数GPUへ分け、1 GPU当たりのKV memoryを減らせる。長文で単一GPUのcache容量を超える構成へ拡張できる。
- **MLA / sparse attention対応kernel**: MLAの圧縮latentやsparse indexを前提とした専用kernelを使い、通常のMHA用pathへ無理に変換するmemory / compute overheadを減らせる。
- **CUDA Graph**: decode等で繰り返すkernel列をcaptureし、tokenごとのCPU launch overheadを減らせる。full / breakable graph等でdynamic servingとGraphの両立範囲を広げている。
- **kernel fusion / compiler pass**: activation→quantization、RMSNorm、MoE routing等の小operationをfused kernelへまとめ、中間tensorのHBM書き戻しとkernel launchを削減できる。
- **external KV connector**: KV storeやremote memory backendをconnector経由で差し替えられ、serving engine本体とdata placementを分離できる。multi-node / disaggregated servingで重要。
- **OpenAI互換API**: chat / completion等をOpenAI互換endpointとして提供し、既存applicationからserving backendを差し替えやすい。
- **distributed deployment**: 単一GPU、multi-GPU、multi-node clusterまで同じserving stackで構成できる。scheduler、cache、parallelism、connectorを組み合わせ、単なるkernel libraryではなくcluster serving基盤として使える。
- **metrics / observability**: KV hit率、offload量、queue、latency等を観測し、cache policyやcapacity planningを調整できる。大規模運用では「速いkernel」だけでなく、どこが律速かを見られることが重要。

以下の更新履歴は、**memory階層、分離serving、MoE通信、量子化、投機的デコード、GPU kernel**がどこまで実用範囲を広げたかを追う。

## 2026-09-11

- **ROCm共有expertの複数stream重ね合わせ範囲を拡大 — merged 2026-09-10 UTC**: Qwen3.5-35B-A3Bのgfx950・TP8/DP1・同時実行64で出力throughput **4,566→5,967 tok/s（+30.7%）**、DeepSeek-V4-Proでは **2,010→2,374 tok/s（+18.1%）**。共有expert計算を別streamへ重ねる条件を拡張し、skinny GEMMの並行実行安全性も修正。[PR #56098](https://github.com/vllm-project/vllm/pull/56098)

- **batched CUTLASSのMoE workspace過剰確保を解消 — merged 2026-09-10 UTC**: dispatch rank数の二重計上を除去し、DeepSeek-V3・DP32・local expert 16の例で共有workspaceを **112 GiB→3.5 GiB / GPU** に削減。大規模expert parallel時の不要なGPUメモリ予約を大幅に減らす。[PR #55579](https://github.com/vllm-project/vllm/pull/55579)

## 2026-09-10

- **Qwen3.8 PLEのCPU退避とEngram並列化 — merged 2026-09-09**: PLE埋め込み表をページ固定したCPUメモリへ保持し、GPUがCUDAの統一仮想アドレス（Unified Virtual Addressing; UVA）から必要行を直接読む経路を追加。Engramテンソル並列（Engram Tensor Parallelism; ETP）もTP×DPへ拡張。単一実測ではCPU退避後も性能は概ね横ばいで、GPUメモリ配置の自由度を高める更新。[PR #54371](https://github.com/vllm-project/vllm/pull/54371)

## 2026-09-05

- **手動activation quantization fusionの適用開始 — merged 2026-09-03**: これまでcompiler passが後から検出して融合していた「活性化関数の実行 → FP8量子化」を、model実装側から明示的に1つのfused kernelへ流せる経路を追加した。

  具体的にはLlama MLPの`down_proj`前で、`SiluAndMul`による活性化と静的FP8量子化（static FP8 activation quantization）を、`fused silu_and_mul_quant`へまとめられるようにする。

  **融合（fusion）**は、別々のGPU kernelなら中間結果をVRAMへ書き戻して再読込する処理を1つにまとめ、kernel起動回数とmemory trafficを減らす最適化である。手動fusionが使われた場合はcompiler側の`ActivationQuantFusionPass`が同じ処理をもう一度融合しないよう制御する。

  このPRには独立した速度benchmarkはなく、現時点では「fusionをmodel側から確実に適用できる基盤」の追加として見るのが適切。[PR #51415](https://github.com/vllm-project/vllm/pull/51415)

## 2026-09-04

- **依存待ち前にweightを先読みするfused Q/KV RMSNorm改善 — merged 2026-09-03**: PDL（Programmatic Dependent Launch; GPU kernel間の依存関係をGPU側で待つ仕組み）で前処理完了を待っている間にも、前処理結果へ依存しないgamma weightは読み込める。そのため待機前にweight loadを開始し、memory accessと依存待ちを重ねるよう変更した。さらにhidden width 2048以上では8 warp化。Kimi-K3 / DeepSeek-V4のattention前段で使うfused Q/KV RMSNorm kernelを **4.02 → 3.55 µs（約12%短縮）**。[PR #55020](https://github.com/vllm-project/vllm/pull/55020)

- **MLA decodeのquery連結＋KV cache書き込み短縮 — merged 2026-09-03**: MLA（Multi-head Latent Attention; K/Vを低次元latentへ圧縮して保持するattention）のdecode前処理で、queryの連結と新しいKV cache entryの書き込みを行うkernelを改善した。token数に応じて1行を処理するwarp数を変え、依存待ち前に独立loadを進め、後続attention kernelも可能な時点で早く起動する。kernel latencyは **2.95 → 2.06 µs（30%短縮）**、安定decode時のtoken間遅延（Inter-Token Latency; ITL）は **約0.40%短縮**。[PR #54896](https://github.com/vllm-project/vllm/pull/54896)

## 初期収録期間

2026-06-03〜2026-09-03

## 要点

この3か月でvLLMは、単一GPUの高速推論engineというより、**KV cacheをGPU外へ階層化し、prefillとdecodeを別workerへ分離し、MoE通信・投機的デコード・weight offloadまで統合するserving基盤**へ広がっている。

特に重要なのは以下の流れ。

1. KV cacheをGPU以外のCPU・object storage・diskなどへ逃がすmulti-tier化
2. prompt処理のprefillとtoken生成のdecodeを別GPU群へ分けるP/D分離（prefill/decode disaggregation）
3. draft modelや複数token予測を使い、1回の本体model実行で複数tokenを確定するspeculative decoding
4. MoE expert通信やrouting kernelの低遅延化
5. GPU memoryへ収まらないweight / KVを外部tierへ置くoffload

## 主要更新

- **2026-06-15 — v0.23.0（released）**: CUDA Graphを途中で抜けられるbreakable graph、pipeline bubble削減、object storageを第2階層として使うmulti-tier KV cache、requestごとに異なるoffload policyを追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.23.0)

- **2026-06-29 — v0.24.0（released）**: KV cacheが外部tierに存在するかを複数requestまとめて非同期確認する仕組み、NIXLによるprefill worker→decode workerへのKV直接転送、MoE通信backendのDeepEP v2、投機的デコード方式DFlashを追加。FlashInfer sparse-index cacheでTTFT 2〜4%、prefill planningでend-to-end throughput 4%、FP8行列積の不要padding回避で20%、MoE buffer前確保で9〜14%向上。[release](https://github.com/vllm-project/vllm/releases/tag/v0.24.0)

- **2026-07-11 — v0.25.0（released）**: workloadに合わせてdraft量を変えるdynamic speculative decoding、より広範囲をcaptureするfull CUDA Graph、複数方式を統一的に扱うUniversal speculative decoding、DSpark、token単位KV offload、object-store / NIXL connector、非同期expert負荷分散（EPLB）、RDMA NIC選択を追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.25.0)

- **2026-07-27 — v0.26.0（released）**: KV offload量やhit率を観測するmetrics、data-parallel replicaごとにcache階層を意識するtiering、DFlashとMoE routing kernelを強化。specialized routingでTPOT（Time Per Output Token; 出力1 tokenあたり時間）2.94%改善、`fused_topk_bias` kernelは1.5〜2倍高速化。[release](https://github.com/vllm-project/vllm/releases/tag/v0.26.0)

- **2026-08-10 — v0.27.0（released）**: FlashAttention 4でFP8 KV cache対応、sequence parallelism、汎用P2P KV secondary tier、差し替え可能なcache eviction policy、NIXLによるP/D分離、MoRIIOによるtensor-parallel ↔ data-parallel間KV移動を追加。sparse MLAの空kernel launch削減は約2倍、router skipはTTFT 3.4%、workspace再利用は3.9%改善。[release](https://github.com/vllm-project/vllm/releases/tag/v0.27.0)

- **2026-08-26 — v0.28.0（released）**: requestや負荷に応じて投機token数を変えるadaptive speculative budgetによりDSpark TTFT約60%改善。shared expertをGPU間分割して約17 GiB/GPU削減。さらにExpert / Prefill / Decodeを別GPU群へ分けるE/P/D分離、weight offload、diskを含むtiered KV、KVの部分読込、不要なGPU↔CPU同期除去、MXFP4/NVFP4 low-bit kernelを追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.28.0)

### 用語メモ

- **TTFT（Time To First Token; 最初のtokenが返るまでの時間）**: prompt送信から最初の出力までの待ち時間。
- **TPOT（Time Per Output Token; 出力tokenあたり時間）** / **ITL（Inter-Token Latency; token間遅延）**: 生成開始後の体感速度を見る指標。
- **P/D分離（Prefill/Decode disaggregation）**: promptを一括処理するprefillと、1 tokenずつ生成するdecodeを別GPU群へ分け、各段階に適したhardware割当を行う方式。
- **multi-tier KV cache**: KV cacheをGPU HBMだけでなくCPU DRAM、remote memory、object storage、diskなど複数階層へ置く方式。
