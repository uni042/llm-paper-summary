# llama.cpp

llama.cppの主要な機能・性能更新を継続的に記録する集約ページです。memory management、MoE、speculative decoding、kernel、同期削減など本質的な更新を扱います。

## 2026-09-05

- **GPU-resident LRU cache for host-offloaded MoE expert weights — Draft / Open**: CPU host memoryへoffloadしたMoE expertの最近使用分をVRAMへLRU cacheする提案。`--moe-expert-cache N`でopt-inし、decode-onlyで動作する。Qwen3.8-Flash-Next UD-Q4_K_XL、2×RTX 3090で **18.4 → 24.2 tok/s（+31%）**。54k-record workloadのrouting traceではstaticなhot expert偏りは弱い一方、時間局所性が強く、推定LRU hit率は64 slotsで約67%、128 slotsで約81%。48 slots/layer（約4.1 GiB VRAM）・2 uploads/layer/stepで測定。現状はmulti-token decode（speculative / MTP）をbypassする。[PR #27861](https://github.com/ggml-org/llama.cpp/pull/27861)

## 初期収録期間

2026-06-03〜2026-09-03

対象期間のmerged PRのうち、memory management、MoE、speculative decoding、kernel、同期削減に関する本質的更新だけを掲載する。

## 要点

CUDA Graphの適用範囲拡大、MoE kernel fusion、DSpark speculative decoding、CPU FFN offloadが主要な前進。加えて2026-09-05時点では、host-offloaded MoE expertをVRAMへ時間局所性ベースでcacheするDraft PRが公開されている。

## 主要更新

- **2026-06-26 — token間同期の削減（merged）**: pipeline parallelism時のCPU→CUDA copyを非同期化し、copyとgraph実行間の同期を1回へ削減。[PR #20793](https://github.com/ggml-org/llama.cpp/pull/20793)
- **2026-07-03 — GDNの冗長CUDA copy削除（merged）**: recurrent snapshotをcacheへ直接書き、4回のcopyを除去。DGX Sparkでdecode約3%、MTP平均約4%向上。[PR #23940](https://github.com/ggml-org/llama.cpp/pull/23940)
- **2026-07-03〜09-01 — MoE fusion群（merged）**: 288-expert top-k fusionでStep-3.7-Flash decode 2.4%向上、activation量子化の重複除去でRTX 5090 prefill 3.4〜5.9%／E2E 2.8〜3.1%向上、weighted reduction fusionでprefill 3.6〜7.1%向上。[#25267](https://github.com/ggml-org/llama.cpp/pull/25267) [#25441](https://github.com/ggml-org/llama.cpp/pull/25441) [#25952](https://github.com/ggml-org/llama.cpp/pull/25952)
- **2026-07-28 — DSpark speculative decoding（merged）**: low-rank Markov head、anchor-first drafting、confidence pruningを実装。RTX 4090／Qwen3-8Bで1.88倍。[PR #25173](https://github.com/ggml-org/llama.cpp/pull/25173)
- **2026-08-11 — CUDA Graph適用範囲拡大（merged）**: stream syncが必要な経路だけgraphを無効化。RTX 5090 parallel decodeでnpl16 13%、npl32 8%、BF16 decode 4.8%向上。[PR #26802](https://github.com/ggml-org/llama.cpp/pull/26802)
- **2026-09-03 — multi-GPU concurrent streams（merged）**: splitごとにgraph optimizationとstreamを独立化。MoE decode 3.7%向上。[PR #28198](https://github.com/ggml-org/llama.cpp/pull/28198)
- **期間内 — `--n-cpu-ffn`（merged）**: dense FFNをCPUへ置くweight offloadを追加。公式性能値なし。[PR #26622](https://github.com/ggml-org/llama.cpp/pull/26622)

KV cacheの量子化領域を起動時に予約し`--fit`へ反映する変更も入ったが、これは主にOOM回避のmemory planningで、速度向上値はない。[PR #23907](https://github.com/ggml-org/llama.cpp/pull/23907)
