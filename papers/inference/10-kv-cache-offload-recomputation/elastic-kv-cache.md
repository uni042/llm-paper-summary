---
canonical_id: "arXiv:2608.23658"
arxiv_id: "2608.23658"
title: "Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap"
summary: "prefill activation reserveをdecode中だけKVへ貸すCUDA VMM機構を実装しつつ、small chunkでもTTFTがほぼ悪化せず単純なchunk縮小の方が有利というnegative resultを示す。"
source: "https://arxiv.org/abs/2608.23658"
last_audited: null
audit_version: 0
---

# Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap

## 書誌情報
- **著者**: Sathishkumar Sivashanmugam
- **公開日**: 2026-08-24
- **状態**: arXiv preprint v1
- **実装**: userspace CUDA VMM、torch pluggable allocator、block-pool gate、scheduler controller。attention kernel/driver patch不要。

## 一文要約
vLLMが大prefill用に常時確保するactivation reserveをdecode中だけKV poolへ貸し、prefill直前に返す仕組みを実装した。しかし8192-token chunkでも32768-token chunkよりmedian TTFTが約1%遅いだけで、単にmax_num_batched_tokensを下げる方がKV容量を多く確保でき、Elastic controllerは実用上の優位を示せなかった。

## 問題設定
vLLMは起動時に最大prefillのactivation peakを予約し、残りをKV cacheにする。Qwen2.5-7B、TP1ではchunk 2048→32768でKV容量が約366K→308K tokenへ減り、約3.1 GiBのreserveが生じる。このreserveはdecode-only時には遊休するため、KVへ時間貸しできるかを検証する。

## 手法
各layerでbase+elastic分の連続virtual addressを予約し、CUDA VMMでbase handleとelastic handleを同じrangeへmapする。baseは常駐、elasticだけ上位sub-rangeをmap/unmapするため、attention kernelには常に単一連続pointerとして見える。elastic領域のblock-idはcommit時だけpoolへ追加し、decommit前にdrainする。

schedulerは次batchがdecode-onlyかprefillを含むか1 step先に知るため、decode-onlyでcommit、prefill直前にdecommitする。CUDA graphsとprefix caching併用でも動作し、toggle前後でbit-identical generationを確認。

## 評価条件
**A100-SXM4 40GB、Qwen2.5-7B-Instruct FP16、vLLM 0.23.0、gpu_memory_utilization=0.9、max_model_len=32768**。3.09 GiB / 28 layersでlive controllerのdecommitは**3.8 ms**、recommitは**23.8 ms**。

staticにreserve全量をKVへ足すと約314K→370K tokenへ増えるが、62K-token prefill burstで約2.3 GiB activationが必要になりOOM。dynamic toggleはprefill直前に4.4 msでdecommitして同burstを完走した。

## 決定的な結果
40 background decode sequence中へ約25K-token promptを6本投入してTTFTを比較。

| Mode | median TTFT | max TTFT | KV capacity |
|---|---:|---:|---:|
| chunk 8192 | 4.97 s | 6.07 s | 375K |
| chunk 32768 | 4.91 s | 5.79 s | 314K |
| Elastic 32768 | 4.90 s | 5.76 s | 364K |

small chunkのmedian penaltyは約1%で、Elasticはlatencyを維持してもKV容量で8192 chunkに負ける。prefillはcompute-boundで総FLOPsがほぼ不変、decodeは280 sequenceでも8192-token budgetの約3%しか消費しないため、chunk分割によるhead-of-line penaltyが小さい。

## Scope
decode-only時間はchat 95–97%、bursty 72–97%、long-context 90–99.8%で十分長い。問題はtensor parallelismでreserve比率が薄まることで、**7B TP1 16%、32B TP4 7.7%、7B TP4 2.7%**。著者は評価範囲でElasticが単純なchunk縮小を上回る構成を見つけられなかった。

有効条件は「small chunkがprefill throughputを明確に落とし、同時にKVがscarce」である。

## 既存研究との差
vAttentionはdriver patchを用いるUVM demand paging、Jengaはfixed budget内のKV sizingが中心。本論文はactivation reserveとKV poolを時間共有するkernel-transparent VMM機構を作り、さらに**機構は正しく動くが現在のvLLMでは機会が薄い**ことをnegative resultとして示した点が重要。

## 限界
評価は単一A100-40GB、Qwen2.5-7B、vLLM 0.23.0中心。別GPU、別model、memory-bound prefillや異なるschedulerでは結論が変わる可能性がある。

## 一次資料
- https://arxiv.org/abs/2608.23658
- https://arxiv.org/pdf/2608.23658
