# LMDeploy

LMDeployの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-24 — v0.14.0（released）**: FP8 KV cache、prefix cache再設計、CUDA Graph capture batch-size設定、DP kernel dispatch改善。[releases](https://github.com/InternLM/lmdeploy/releases)
- **2026-07-31 — v0.15.0（released）**: page／slab／object allocatorとobject-cache schedulerで旧managerを置換し、prefix trie、recurrent state、cache lifecycleを統合。[PR #4717](https://github.com/InternLM/lmdeploy/pull/4717)
- **2026-08-06 — SSM prefix matcher（v0.16.0収録）**: Python trie全走査をbounded NumPy exact-checkへ置換。batch512／128K contextでp99約5.23秒→120.81 ms。host metadataは512 checkpointで約520 MiB。[PR #4788](https://github.com/InternLM/lmdeploy/pull/4788)
- **2026-08-19 — v0.16.0（released）**: SM90 BF16/FP8 GEMM、blocked-FP8 MoE、decode CUDA Graph、SSM prefix cacheを追加。H200×8でcompletion throughput 24.91%、steady throughput 13.29%、TPOT 18.14→14.83 ms。[PR #4827](https://github.com/InternLM/lmdeploy/pull/4827)
- **2026-09-01 — v0.17.0（released）**: DeepEPv2、Mooncake KV connector、CUDA PDL、paged attention、compact blocked-FP8 MoE、speculative前後処理fusionを追加。MTP5 graph-buffer fill 2.019→1.102 ms。[PR #4877](https://github.com/InternLM/lmdeploy/pull/4877)

[リリース一覧](https://github.com/InternLM/lmdeploy/releases)
