---
canonical_id: "arXiv:2604.25080"
arxiv_id: "2604.25080"
title: "CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration"
summary: "KVキャッシュ復元をトークン・層・GPUの3軸並列問題として扱い、バッチ認識スケジューリングで再計算とI/Oを重畳してTTFTを10–62%削減する。"
source: "https://arxiv.org/abs/2604.25080"
last_audited: null
audit_version: 0
---

# CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration

## 書誌情報
- **著者**: Sean Nian, Jiahao Fang, Qilong Feng, Zhiyu Wu, Fan Lai
- **所属**: University of Illinois Urbana-Champaign, National University of Singapore
- **公開日**: 2026-04-28
- **状態**: arXiv preprint v1
- **コード**: 公式公開repositoryは確認できず。論文実装はvLLMとLMCache上。

## 問題設定
長文chat、RAG、agent pipelineではGPU外へ退避したKVキャッシュの復元がTTFTを支配する。再計算はattentionにより長さとともに超線形に増え、I/Oは帯域制約を受ける。既存hybrid方式は主にrequest単位で両者を選び、token位置・layer・multi-GPU・batch内resource contentionを十分利用しない。

## 手法
**Token-wise**: cached prefixを通常512-token chunkに分け、先頭から再計算するpointerと末尾からKVを読むpointerを同時に進める。後方tokenほど再計算costが高いため、長いprefixで有利。

**Layer-wise**: layer 0からの再計算と最終layerからのKV読み込みを並行する。offline profilingでtoken-wiseとのcrossover lengthを求め、短いsequenceではlayer-wiseを選ぶ。

**Multi-GPU**: pipeline stage境界のhidden activationを保存し、各GPUが自身のmodel shardのKVを独立復元することでstage間の逐次依存を緩和する。

**Batch-aware scheduler**: 各requestのcompute/I/O pointerをglobalに調停し、残り再計算costの大きい長prefixへI/Oを優先配分する。

## 評価条件
- **Models**: Qwen3-8B、Llama-3.1-8B、Qwen3-30B-A3B
- **Workloads**: LMSYS-Chat、WildChat、SWE-Bench
- **GPU**: L40S 46GB、A100 40GB、H100 80GB
- **I/O**: 10 / 40 / 80 Gbps、default 10 Gbps
- **Baselines**: vLLM、SGLang HiCache、LMCache v0.3.1、Cake
- **Metric**: TTFT、GPU利用率、I/O利用率

## 主要結果
- TTFTを既存方式比 **10–62%削減**、全体で **1.1–1.7×**改善。
- 長さ6K→30KでvLLM/SGLangとの差は **1.1×→1.7×**へ拡大。
- KV復元中の平均利用率は **GPU 88% / I/O 78%**。LMCacheはGPU 10%、vLLMはGPU 91%だがI/Oはほぼ未使用。
- multi-GPU最適化を外すと平均復元latencyは **0.21→0.29秒**へ38%増加。2DのみでもvLLMより24%高速。
- H100で40 / 80 Gbps時に **1.7× / 1.5×**改善。
- Qwen3-30B-A3B、10 Gbpsで2×L40S / A100でも **1.6× / 1.5×**改善。
- batch size 2 / 4 / 8で **1.6–2.6×**改善。

## 既存研究との差
LMCache等はKVを階層memoryへ置く仕組み、Cakeはtoken軸のcompute/load hybridが中心。CacheFlowはtoken・layer・GPUの3軸を統合し、さらにbatch内の共有compute/I/O競合を同じschedulerで扱う。HCacheのhidden-state restorationやMooncakeのKV transfer overlapとも補完的。

## 品質と限界
KV圧縮・量子化・token pruning等の近似は使わないためmodel品質への直接trade-offはない。理論上のmulti-GPU線形scaleは均等partition等を仮定し、実機ではload imbalanceで弱まる。評価はNVIDIA GPUと10–80 Gbps中心で、異なるstorage/runtimeへの一般化は未検証。公式code公開も確認できない。

## 一次資料
- https://arxiv.org/abs/2604.25080
- https://arxiv.org/html/2604.25080v1
