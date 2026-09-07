# vLLM

vLLMの主要な機能・性能更新を継続的に記録する集約ページ。KV cacheの階層化、prefill / decode分離、MoE、投機的デコード（speculative decoding）、weight offload、GPU kernel改善など、実際のserving性能や必要memoryへ影響する更新を扱う。

## 現在できること

- continuous batchingとpaged KV cacheを使い、多数requestを同時に高throughputでservingできる。
- KV cacheをGPU HBMだけでなくCPU DRAM、remote memory、object storage、diskなど複数階層へ置ける。
- prefillとdecodeを別GPU群へ分けるP/D分離、さらにMoE expert処理も分離する構成を扱える。
- tensor / pipeline / data / expert parallelism、MoE、低bit weight / activation / KV、投機的デコードを組み合わせられる。
- weight offloadや外部KV connectorを使い、単一GPU memoryを超えるmodel・context・request数へ対応できる。
- OpenAI互換serving基盤として、単一GPUから分散clusterまで同じruntime系で構成できる。

以下の更新履歴は、これらの能力のうち**KV階層化、分離serving、投機的デコード、MoE通信、offload、GPU kernel fusion**がどう拡張されたかを記録している。

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
