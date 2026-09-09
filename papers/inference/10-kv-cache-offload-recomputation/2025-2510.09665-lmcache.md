---
canonical_id: "arXiv:2510.09665"
arxiv_id: "2510.09665"
last_audited: "2026-09-09"
audit_version: 1
title: "LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference"
authors_affiliations: "Yuhan Liu, Jiayi Yao, Yihua Cheng, Yuwei An, Xiaokun Chen, Shaoting Feng, Yuyang Huang, Samuel Shen, Rui Zhang, Kuntai Du, Junchen Jiang（Tensormesh Inc.; University of Chicago）"
published: "2025-10-08"
publication_status: "arXiv preprint v2 (2025-12-05); 査読済final publicationは一次資料から未確認"
lineage: "KV Cache Offload / Recomputation"
hardware_evaluation: "実機"
hardware_details: "主評価は8×NVIDIA H100。prefill-decode分離はNVLink。感度評価はB200。"
source: "https://arxiv.org/abs/2510.09665"
code: "https://github.com/LMCache/LMCache"
last_checked: "2026-09-09"
---

# LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference

> vLLM/SGLangのKV cacheをGPU外へ抽出し、CPU・disk・remote storage・networkを跨いで再利用・転送する汎用KV cache layer。大粒度chunk転送、計算とI/Oの重畳、copy削減、標準connector APIを組み合わせる。

## 正式監査

2026-09-09にarXiv v2本文と公式LMCache repositoryを突合した。arXivはv2（2025-12-05）。査読済conference/journal final版は確認できない。著者はarXiv v2の11名を正とし、Rui Zhangを含む。公式repository READMEのcitationにはRui Zhangが欠ける版があるため、書誌はarXiv本文を優先する。

公式実装は LMCache/LMCache。主評価は実機で、single-nodeは8×H100、prefill-decode分離はprefiller/decoderをNVLink接続し、感度評価にB200を用いる。比較対象はLMCache v0.3.6、vLLM v0.10.2 GPU prefix caching、vLLM v0.11.0 native CPU offload、匿名commercial endpoint 2種。

## 問題設定と手法

長文context、RAG、multi-turn会話では過去prefixのKVを再利用できればprefillを省ける。またprefillとdecodeを分離する構成ではKVを別GPUへ高速転送する必要がある。paged attentionではKVが小pageに分割されるため、pageごとのcopyではCUDA/DMAの固定overheadが支配的になる。

LMCacheは推論engineとstorage/networkの間に独立KV cache layerを置く。複数page/layerを既定256-token chunkへまとめ、scattered GPU pagesを連続bufferへ集約して転送する。layer-wise pipelineとquery-level asynchronous loadingでcomputeとI/Oを重ね、reference countingで不要copyを抑える。dynamic offloadingはGPU free pageの事前複製量と将来のallocation stallをpointerで制御する。

標準connectorによりvLLM/SGLangの内部変更を吸収し、central controllerはlookup、move、clear、pin、compression等の操作を提供する。

## 評価条件

| 項目 | 内容 |
|---|---|
| LMCache | v0.3.6 |
| vLLM | v0.10.2 GPU prefix caching / v0.11.0 native CPU offload |
| Hardware | 8×H100、PD分離はNVLink、感度評価はB200 |
| Model | Llama-3.1-8B/70B、Qwen2.5-Coder-32B、Qwen3-Coder-480B-A35B-FP8、Qwen2.5-72Bほか |
| Workload | multi-round Q&A、LongBench、vLLM random workload、企業trace |
| Metrics | TTFT、ITL、throughput、transfer latency |

single-node CPU offloadでは既定10K-token document context＋短いquestion、最大100 output token、最大500GB CPU KV容量。PD分離評価では8K input / 200 output token。

## 主要結果

- single-node CPU offload: best baseline比でTTFT **1.9–8.1×短縮**、同TTFT時のquery rate **2.3–14×向上**、QPS=1でITL **7–92%削減**。
- 企業trace replay: basic vLLM比でTTFT **3.7–6.8×短縮**、ITL **19–58%削減**。
- 15Gbps central remote storage: throughput **1.3–3×向上**。
- prefill-decode分離: vLLM native比でmean TTFT **1.5–1.8×低下**、mean ITL **1.1–1.7×低下**。
- CPU→GPU loading bandwidth: LMCache **400Gbps**、vLLM native **88Gbps**。
- asynchronous loading: end-to-end delay **1.46×改善**。
- B200感度評価: 32Gbps networkではremote KV loadがprefillより速いのは入力 **256K token超**。64/128Gbpsでは評価全context lengthでloadが有利。

abstractの「up to 15× throughput」は本文の個別比較より強い集約表現であるため、repo本文では条件の明確な2.3–14×等を優先する。

## 実機・品質・限界

主要end-to-end値は実機測定。企業F/Gについてはproprietary model自体ではなく、企業traceのtoken-length分布を公開modelへ適用したtrace-driven replayである。commercial endpoint比較はblack-boxで内部hardware/implementationを完全には揃えられない。

KV内容を変えない再利用・移送なのでmodel quality自体は原理上変えない。ただしcontext truncationはprefix reuseを破壊し、企業traceでhit率が約85%から45%へ低下した。

cache reuseが乏しいworkloadでは追加I/O overheadだけが残り得る。remote backendは低帯域時にprefillより遅くなる。central controllerの大規模cluster scalability/consistencyは主要評価対象外。SGLang native CPU offloadとの差が小さい場合もあり、全engine/backendで絶対優位ではない。

## 既存系統との差

vLLM/SGLang native offloadがengine内部・単一node中心なのに対し、LMCacheはengine外に独立storage/communication layerを設け、cross-node、multi-tier storage、controller APIまで扱う。Mooncake/InfiniStore/3FS等がstorageそのものを主対象にするのに対し、LMCacheはpaged inference engineとstorageをつなぐdata pathとconnector semanticが中心である。KV compression研究と異なり、主貢献は転送粒度、pipeline、copy削減、配置・制御にある。

## 研究上の含意

KV cacheをGPU memoryの一時状態ではなくcluster全体を跨ぐstorage/communication primitiveとして扱う点が重要である。今後はcache hitだけでloadを決めず、context length、model prefill速度、network/storage bandwidth、GPU queueを見てload / recompute / migrateを動的選択する制御が重要になる。

SSDについてはlocal diskやGPU-Direct Storageをbackendに取り込めるが、主評価はCPU DRAMとnetworked storage中心で、SSD queue depth、random I/O、prefetch、write enduranceをserving schedulerと共同最適化する余地が残る。

## 一次資料

- https://arxiv.org/abs/2510.09665
- https://arxiv.org/html/2510.09665
- https://github.com/LMCache/LMCache

## 更新履歴

- 2026-09-09: workflow v9 formal audit。arXiv v2、公式repository、書誌、実機条件、主要値、実機/trace区別を再確認。
