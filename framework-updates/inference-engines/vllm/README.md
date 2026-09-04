# vLLM

vLLMの主要な機能・性能更新を継続的に記録する集約ページです。KV cache階層化、disaggregated serving、MoE、speculative decoding、kernel改善などを扱います。

## 2026-09-05

- **Manual `ActivationQuantFusionPass` initial application — merged 2026-09-03**: static FP8 activation quantizationのmanual fusion migrationを開始。producer側で`maybe_fused_act_quant`を使い、linearが対応する`input_quant_key`を公開している場合、`SiluAndMul + kFp8StaticTensorSym`を`fused silu_and_mul_quant` kernelへ流す。Llama MLPの`down_proj`から利用し、manual fusionが発火した場合はcompiler側の`ActivationQuantFusionPass`と二重fusionしない。PR本文には速度benchmarkはない。[PR #51415](https://github.com/vllm-project/vllm/pull/51415)

## 2026-09-04

- **[Perf] Prefetch the weight before the PDL wait in fused_q_kv_rmsnorm — merged 2026-09-03**: Programmatic Dependent Launch (PDL) の待機前に依存しないgamma weight loadを先行させ、幅2048以上では8 warp化。Kimi-K3 / DeepSeek-V4のattention frontendで使うfused Q/KV RMSNorm kernelを **4.02 → 3.55 µs（約12%短縮）**。[PR #55020](https://github.com/vllm-project/vllm/pull/55020)
- **[Perf][Kimi-K3] Cut MLA decode concat/cache epilogue latency — merged 2026-09-03**: MLA decodeのquery concat + KV cache insert kernelで、token数に応じたwarp-per-row分割、依存待ち前の独立load、consumer FMHAのearly triggerを組み合わせた。kernel latencyは **2.95 → 2.06 µs（30%短縮）**、stable decode ITLは **約0.40%短縮**。[PR #54896](https://github.com/vllm-project/vllm/pull/54896)

## 初期収録期間

2026-06-03〜2026-09-03

## 要点

3か月でv0.23.0〜v0.28.0が公開され、multi-tier KV cache、NIXL P/D分離、DeepEP v2、dynamic speculative decoding、tiered disk KV、weight offloadまで一続きのserving基盤へ拡張された。2026-09-05時点ではactivation quantizationのmanual fusion経路も追加されている。

## 主要更新

- **2026-06-15 — v0.23.0（released）**: breakable CUDA Graph、pipeline bubble削減、object-storeをsecondary tierにするmulti-tier KV cache、request別offload policyを追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.23.0)
- **2026-06-29 — v0.24.0（released）**: async batched KV tier lookup、NIXLによるprefill→decode KV push、DeepEP v2、DFlashを追加。FlashInfer sparse index cacheはTTFT 2〜4%、prefill planningはE2E throughput 4%、FP8 scaled-mm padding bypassは20%、MoE buffer preallocationは9〜14%向上。[release](https://github.com/vllm-project/vllm/releases/tag/v0.24.0)
- **2026-07-11 — v0.25.0（released）**: dynamic speculative decoding、full CUDA Graph、Universal speculative decoding、DSpark、token-selective KV offload、object-store/NIXL connector、async EPLB、RDMA NIC選択を追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.25.0)
- **2026-07-27 — v0.26.0（released）**: KV offload metrics、DP-replica-aware tiering、hybrid DFlashとMoE routing kernelを強化。specialized routingでTPOT 2.94%、`fused_topk_bias`はkernel 1.5〜2倍。[release](https://github.com/vllm-project/vllm/releases/tag/v0.26.0)
- **2026-08-10 — v0.27.0（released）**: FlashAttention 4 FP8 KV cache、sequence parallelism、generic P2P KV secondary tier、pluggable eviction、NIXL P/D分離、MoRIIO TP↔DPを追加。sparse MLAの空launch削減は約2倍、router skipはTTFT 3.4%、workspace再利用は3.9%向上。[release](https://github.com/vllm-project/vllm/releases/tag/v0.27.0)
- **2026-08-26 — v0.28.0（released）**: adaptive speculative budgetでDSpark TTFT約60%改善、shared-expert shardingで約17 GiB/GPU削減。E/P/D disaggregation、weight offload、tiered disk KV、partial KV load、GPU↔CPU sync除去、online MXFP4/NVFP4 kernelを追加。[release](https://github.com/vllm-project/vllm/releases/tag/v0.28.0)
