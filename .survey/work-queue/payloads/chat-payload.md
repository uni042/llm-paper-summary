---
canonical_id: "arXiv:2608.16157"
arxiv_id: "2608.16157"
title: "FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
summary: "GPU・CPU・host memory・PCIeを一体として扱い、prefillのexpert転送重畳とdecode missの帯域適応CPU/GPU分担でconsumer hardware上の大規模MoE servingを高速化する。"
source: "https://arxiv.org/abs/2608.16157"
last_audited: null
audit_version: 0
---

# FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution

## 書誌情報
- **著者**: Shuo Yang, Xiaoze Fan, Melissa Pan, Haocheng Xi, Zhe Wang, Shanlin Sun, Kurt Keutzer, Song Han, Matei Zaharia, Chenfeng Xu, Ion Stoica
- **公開日**: 2026-08-17
- **状態**: arXiv preprint v1
- **コード**: https://github.com/FlashML-org/FreeToken

## 問題設定
MoEはtokenごとのactive expertが少なく計算量は小さいが、完全expert poolはconsumer GPUのVRAMを超える。prefillでは長promptがほぼ全expertをactivateして大量転送が発生し、decodeではcache miss、agent workloadではcontext編集による再prefillが支配的になる。

## 手法
**Prefill**では2つのfull-layer bufferを使い、GPUがlayer lを計算中にlayer l+1の全expertをPCIe転送する。hybrid-attention model向けにはthinking/tool call/tool output等のsemantic boundaryへrecurrent-state checkpointを置き、context編集後に新suffixだけ再prefillする。

**Decode**では共有LRU expert cacheをrouting localityへ追従させる。miss数m、実測PCIe帯域B_P、CPU expert処理帯域B_HからGPUへfetchする数を概ね q*=m×B_P/B_H とし、残りをCPU上で直接計算する。transferとCPU branchを並行実行し、partial outputをexactにmergeする。

scheduler safe pointではGPU expert cacheを再構成し、変動するVRAM budgetや増大するKV cache需要へ適応する。expert poolはhost側をsource of truthとする。

## 実装
GPU側でrouting-dependent cache controlを行い、fixed-shape bufferとvalid countを使ってCUDA Graph互換を維持する。CPU branchもpersistent C++ workerを介してgraph実行へ統合。FreeToken Weight形式でexpertを最終host layoutへdirect I/Oし、startup時のrepackを減らす。

## 評価
RTX 4060 Laptop 8GBからRTX PRO 6000 96GBまで6環境。Qwen3.6-35B-A3B、DeepSeek-V4-Flash 284B/13B active、GLM-5.2 753B/40B activeを用い、AIME、SWE-bench coding agent、Claude Code、OpenClaw email/calendarを評価。比較はllama.cpp、Ollama、KTransformers、MoE-Infinity。

## 主要結果
- RTX 5090: Qwen3.6 **77–83 tok/s**、DeepSeek-V4-Flash **22–25 tok/s**。
- strongest baseline比decode throughput **1.5–2.3×**。
- agent workloadでもsingle-turn比decode低下を**12%以内**に維持。
- worst-turn TTFTは全条件**44秒未満**、各baselineは少なくとも1条件で150秒超。
- 8GB RTX 4060 laptopで35B modelを**39.3 tok/s**。
- consumer 5環境でstrongest baseline比**1.3–2.1×**。
- RTX PRO 6000 1枚でGLM-5.2 753Bを**14.9 tok/s**、llama.cpp 7.3 tok/s。
- full-layer overlap無効時に対しprefill throughputを4k/8k/16k promptで**19/25/26%**改善。
- 同一cache容量でexpert miss率はQwen/DeepSeekで**16/39%**、KTransformers 41/59%、llama.cpp 62/89%。

## 既存研究との差
既存expert offload/prefetchはmiss率削減が中心だが、FreeTokenは残るmissをPCIe transferとCPU direct executionへ実測帯域比で分ける。静的CPU expert配置とも異なり、routingに追従するcache、prefill transfer overlap、agent state reuse、runtime memory resizeを統合する。

## 品質と限界
CPU/GPUで同じexpert weightをexactに計算し、expert skip等の近似は導入しない。完全expert poolを置けるhost memoryは必要で、巨大modelではworkstation級RAMが要る。高速pathはpinned memoryとPCIe/host bandwidthに依存し、評価はNVIDIA discrete GPU中心。

## 一次資料
- https://arxiv.org/abs/2608.16157
- https://arxiv.org/html/2608.16157v1
- https://github.com/FlashML-org/FreeToken
