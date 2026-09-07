# LMDeploy

LMDeployの主要な機能・性能更新を継続的に記録する集約ページ。KV cache管理、prefix cache、recurrent / SSM state、CUDA Graph、MoE、prefill/decode分離、外部KV connectorなどを扱う。

## 初期収録期間

2026-06-03〜2026-09-03

## 要点

この期間のLMDeployは、**KVやrecurrent stateを共通のcache objectとして管理し、GPU memory allocatorとcache schedulerを作り直すこと**、さらに**MoE通信・低精度GEMM・prefill/decode分離を強化すること**が中心。

## 主要更新

### 2026-06-24 — v0.14.0（released）

- **FP8 KV cache**: 過去tokenのKey / ValueをBF16等より小さいFP8で保持し、context長あたりのGPU memoryを削減。
- **prefix cache再設計**: request間で同じprompt prefixが現れたとき、以前計算したKVを再利用するcache管理を刷新。
- **CUDA Graph capture batch-size設定**: request batch sizeごとにどのshapeをGraph capture対象にするか調整可能にした。
- **data-parallel kernel dispatch改善**: 複数replicaへrequest / kernelを振り分ける経路を改善。

[releases](https://github.com/InternLM/lmdeploy/releases)

### 2026-07-31 — v0.15.0（released）

- **page / slab / object allocator + object-cache scheduler**: 旧cache managerを置き換え、KV pageだけでなくprefix trie、recurrent state、各cache objectの生成・再利用・破棄を統一管理。

  - **page allocator**: KVなどを固定小block単位で割り当てる。
  - **slab allocator**: 大きいmemory領域を先に確保し、その内部を切り分けて小allocationの断片化を減らす。
  - **object cache**: 「KV page」「SSM state」など種類の違うcacheを共通のlifecycleで管理する。

[PR #4717](https://github.com/InternLM/lmdeploy/pull/4717)

### 2026-08-06 — SSM prefix matcher（v0.16.0収録）

- **Python trie全走査をbounded NumPy exact-checkへ置換**: SSM（State Space Model）系cacheで、長いrequest prefixが既存checkpointと一致するか探す際、Python objectのtrie全体を辿る方式をやめた。

  候補範囲を絞ってNumPy上でtoken列を比較することで、batch 512／128K contextのp99 matching timeを **約5.23秒 → 120.81 ms**へ短縮。

  代わりにCPU側へprefix metadataを保持し、512 checkpointでは約520 MiBを使う。つまり**host RAMを増やしてprefix lookup latencyを下げるtrade-off**。[PR #4788](https://github.com/InternLM/lmdeploy/pull/4788)

### 2026-08-19 — v0.16.0（released）

- **SM90 BF16 / FP8 GEMM**: Hopper世代GPU向けに行列積kernelを最適化。
- **blocked-FP8 MoE**: expert weightをblockごとのscaleでFP8化し、MoE matrix multiplyのmemory trafficと演算costを削減。
- **decode CUDA Graph**: 1-token decode kernel列をGraph化し、CPU launch overheadを削減。
- **SSM prefix cache**: recurrent / state-space modelでもprefix再利用を正式機能へ統合。

H200×8でcompletion throughput **24.91%向上**、steady throughput **13.29%向上**、TPOTは **18.14 → 14.83 ms**。[PR #4827](https://github.com/InternLM/lmdeploy/pull/4827)

### 2026-09-01 — v0.17.0（released）

- **DeepEPv2**: MoE token dispatch / combineのGPU間通信backendを更新し、expert parallel通信を高速化。
- **Mooncake KV connector**: 外部KV cache / disaggregated serving基盤Mooncakeと接続し、別worker間でKVを共有・転送できるようにする。
- **CUDA PDL**: PDL（Programmatic Dependent Launch）を使い、前kernel完了をCPUが確認して次kernelをlaunchする往復を減らす。
- **paged attention**: KVをpage単位で管理してmemory断片化を抑えるattention pathを追加・強化。
- **compact blocked-FP8 MoE**: routingされたexpert / tokenだけに合わせて低精度MoE data layoutを圧縮し、不要なpaddingやmemory trafficを削減。
- **speculative前後処理fusion**: draft / verify前後の小kernelをまとめ、投機的デコードの管理overheadを削減。

MTP depth 5のGraph buffer fillは **2.019 → 1.102 ms**。[PR #4877](https://github.com/InternLM/lmdeploy/pull/4877)

[リリース一覧](https://github.com/InternLM/lmdeploy/releases)

### 用語メモ

- **prefix cache**: request先頭の同一token列について以前作ったKV / recurrent stateを再利用するcache。
- **SSM（State Space Model）**: attentionのKVとは異なるrecurrent stateをtoken間で持ち越すsequence model系統。
- **allocator**: GPU / CPU memoryのどの領域を何byte単位で割り当て、解放後にどう再利用するか管理する仕組み。
- **PDL（Programmatic Dependent Launch）**: GPU kernel間の依存起動をGPU側で処理し、CPU同期を減らすCUDA機能。
