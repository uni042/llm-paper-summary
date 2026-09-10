---
canonical_id: "arXiv:2505.02922"
arxiv_id: "2505.02922"
title: "RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference"
summary: "長contextのKV cacheをCPU memory上の**vector storageとして検索対象にし、attentionに重要なtokenだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するmemory容量とbandwidthを減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論system。"
source: "https://arxiv.org/abs/2505.02922"
last_audited: "2026-09-10"
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
---

# RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference

## 書誌情報

- **著者:** Yaoqi Chen, Jinkai Zhang, Baotong Lu, Qianxi Zhang, Chengruidong Zhang, Jing Liu, Jingjia Luo, Di Liu, Huiqiang Jiang, Qi Chen, Bailu Ding, Xiao Yan, Jiawei Jiang, Chen Chen, Mingxing Zhang, Cheng Li, Yuqing Yang, Fan Yang, Mao Yang
- **掲載:** Proceedings of the VLDB Endowment (PVLDB), Vol. 19, No. 5, pp. 1016–1031, 2026
- **DOI:** 10.14778/3796195.3796212
- **arXiv:** 2505.02922
- **公式実装:** https://github.com/microsoft/RetrievalAttention

## 一文要約

長contextのKV cacheをCPU memory上の**vector storageとして検索対象にし、attentionに重要なtokenだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するmemory容量とbandwidthを減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論system。

## 問題設定

long-context LLMではKV cacheがcontext長に比例して増える。KVをすべてGPU HBMへ置けない場合はCPU DRAMへのoffloadが候補になるが、各decode stepで大量のKVをGPUへ戻せばCPU–GPU転送がbottleneckになる。一方、attention sparsityを利用して少数tokenだけを検索する既存方式では、重要tokenの取りこぼしを避けようとすると検索量が増え、検索量を絞るとfull attentionとの差が大きくなりやすい。

RetroInferはこの問題を、KV cacheを単なるoffload dataではなく**queryに応じて必要vectorを取り出すstorage system**として扱うことで解く。

## 手法

### Attention-aWare VEctor index（wave index）

wave indexは、現在のqueryに対して大きなattentionを持つ可能性があるkeyをCPU側のKV集合から探すindexである。一般的な近似最近傍検索をそのまま使うのではなく、attention計算で必要な精度と検索costを直接意識した構成にする。

RetroInferはattention対象を大きく3種類に分ける。

1. **steady zone:** 繰り返し重要になりやすく、GPU側へ残して直接計算する部分。
2. **retrieval zone:** queryに応じてCPU側indexから候補を検索し、必要なKVをGPUへ転送して正確にattentionを計算する部分。
3. **estimation zone:** 全tokenをGPUへ運ばず、cluster単位の情報から残りのattention寄与を推定する部分。

この分割により、「精度のために全KVをretrieveする」か「転送削減のために強く切り捨てる」かの二択を避ける。推定誤差に上限を設けながら、正確な計算が必要な候補へretrieval budgetを集中する。

### segmented clustering

長いcontext全体を毎回大規模cluster化するとindex構築・更新自体が高costになる。そこでsequenceをsegmentへ分割し、各segment内でkeyをcluster化する。token生成に伴う新しいKVも局所的に追加できるため、巨大なglobal indexを繰り返し作り直す必要を減らす。

segment単位に分けるもう一つの利点は、検索indexの更新costと検索精度を局所化できることである。長context全体を一つのcluster空間として再最適化すると、新token追加のたびに広い範囲のcentroidや割当が変化し得る。既存segmentを固定したまま末尾側だけ更新できれば、decodeのcritical pathで行うindex maintenanceを小さく保ち、CPU検索をGPU attentionと重ねやすくなる。

### wave buffer

wave bufferはGPU HBMとCPU DRAMの間で、どのKVをGPUへ残すか、どのretrieval / attention計算をCPUまたはGPUで進めるか、いつKVを転送するかを管理するbuffer managerである。CPU側の検索・data transfer・GPU側attentionを重ね、GPUがCPU retrievalを待つ時間を減らす。

このためRetroInferは単なるsparse-attention algorithmではなく、**index・KV配置・CPU/GPU間転送・attention executionをまとめて設計したsystem**になっている。

## 評価条件

論文および公式実装ではLlama 3系、Qwen 2.5系などのlong-context modelを対象とし、RULER / LongBench等のlong-context workloadで評価している。公式実装はGPU–CPU構成を提供し、Llama-3-8B-1048Kの約120K-token demoではbatch 4で約35 GBのGPU memoryと70 GBのCPU memoryを必要条件の目安としている。

比較対象にはfull attentionおよび既存のsparse-attention / KV retrieval方式が含まれる。

## 主要結果

- **120K context:** full attentionに対してdecode throughputを最大 **4.4×** 改善。
- **1 million token context:** sparse-attention baselineに対して最大 **12.2×** のdecode throughputを報告。
- long-context benchmarkでは、retrieval量を抑えながらfull-attention-levelのaccuracyを維持したと報告している。

これらは単純なCPU offloadの速度向上ではなく、**GPUへ実際に戻すKV量そのものをattention-aware retrievalで減らした効果**を含む。

## 既存研究との差

単純なKV offloadはCPU DRAMを容量拡張として使うが、decodeごとに必要KVを大量転送するとPCIe / interconnect bandwidthが限界になる。RetroInferはCPU DRAMを検索可能なvector storeとして扱い、queryごとに必要性が高いKVだけをGPUへ移す。

また、単純なsparse attentionと比べると、固定patternでKVを削るのではなく、wave indexでquery-dependentな候補を検索し、retrievalしない部分にもattention寄与の推定を残すことでaccuracyとretrieval costのtrade-offを扱う点が異なる。

公式repositoryは先行研究RetrievalAttentionの実装も含み、RetroInferはそのvector-retrieval型long-context inferenceを、index構築とGPU–CPU buffer管理まで含むstorage-engineとして発展させた位置付けである。

## 限界

- CPU DRAMへ大きなKV集合を保持するため、GPU HBM不足は緩和できてもhost memory容量は必要になる。
- retrieval、cluster推定、GPU–CPU転送を追加するため、短contextやKVが十分HBMへ収まる条件ではsystem overheadが相対的に大きくなり得る。
- 効果はattention sparsityとindexが重要KVを十分正確に拾えることに依存する。model / workloadによって最適なretrieval budgetやcache ratioの調整が必要になる。
- SSDを通常のblock storageとしてKVの主tierにする方式ではなく、中心はCPU DRAMとGPU HBMの協調である。したがってSSD/NVMe容量を直接利用するKV offload systemとはmemory hierarchy上の制約が異なる。

## 一般的な実装上の含意

long-context KV offloadでは、storage tierを増やすだけではなく、**「次のattentionに必要なKVを全部転送する必要があるのか」まで変える**とCPU–GPU bandwidth requirementそのものを下げられる。特にKV cacheをvector databaseに近い検索対象として扱えば、memory managerとattention sparsityを別々に最適化するのではなく、retrieval accuracy、GPU cache量、CPU memory量、transfer bandwidthを一つのbudgetとして設計できる。

一方、この方向ではindex構築・更新costが新たなsystem costになるため、RetroInferのsegmented clusteringのようにincremental update可能なindex設計が重要になる。

## 引用関係

- **先行:** RetrievalAttention (arXiv:2409.10516) — attention sparsityをvector retrievalとして扱う直接の前身。公式repositoryも共通。
- **関連:** CPU KV offload / sparse attention研究。KVをCPUへ置くだけでなく、必要subsetを選んで転送する系統に位置する。
- **後続・近接:** 2026年のmulti-tier KV management研究はDRAM / SSDを含む配置・I/O schedulingを強く扱うのに対し、RetroInferはCPU上のKVから何をretrieveするかという検索側を中心に最適化する。

## 一次資料

- PVLDB / DOI: https://doi.org/10.14778/3796195.3796212
- arXiv: https://arxiv.org/abs/2505.02922
- Microsoft Research: https://www.microsoft.com/en-us/research/publication/retroinfer-a-vector-storage-engine-for-scalable-long-context-llm-inference/
- Official code: https://github.com/microsoft/RetrievalAttention
