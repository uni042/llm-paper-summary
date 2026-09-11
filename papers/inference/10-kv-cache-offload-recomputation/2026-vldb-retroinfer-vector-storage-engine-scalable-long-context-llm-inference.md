---
canonical_id: arXiv:2505.02922
arxiv_id: '2505.02922'
title: 'RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference'
summary: 長contextのKV cacheをCPU memory上の**vector storageとして検索対象にし、attentionに重要なtokenだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するmemory容量とbandwidthを減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論system。
source: https://arxiv.org/abs/2505.02922
last_audited: '2026-09-10'
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
authors:
- Yaoqi Chen
- Jinkai Zhang
- Baotong Lu
- Qianxi Zhang
- Chengruidong Zhang
- Jing Liu
- Jingjia Luo
- Di Liu
- Huiqiang Jiang
- Qi Chen
- Bailu Ding
- Xiao Yan
- Jiawei Jiang
- Chen Chen
- Mingxing Zhang
- Cheng Li
- Yuqing Yang
- Fan Yang
- Mao Yang
published: '2025-05-05'
arxiv_categories:
  primary: cs.LG
  cross_list: []
publication: arXiv
publication_type: プレプリント
publication_status: arXiv preprint
sources:
- https://arxiv.org/abs/2505.02922
- https://arxiv.org/pdf/2505.02922
code: null
last_checked: '2026-09-11'
implementation: 実装形態の詳細は既存本文の手法・評価記述を参照。公式コードURLはメタデータ確認時点で確認できず。
implementation_status: official-code-not-confirmed
---

# RetroInfer: A Vector Storage Engine for Scalable Long-Context LLM Inference

## 書誌情報

- **著者:** Yaoqi Chen, Jinkai Zhang, Baotong Lu, Qianxi Zhang, Chengruidong Zhang, Jing Liu, Jingjia Luo, Di Liu, Huiqiang Jiang, Qi Chen, Bailu Ding, Xiao Yan, Jiawei Jiang, Chen Chen, Mingxing Zhang, Cheng Li, Yuqing Yang, Fan Yang, Mao Yang
- **掲載:** Proceedings of その VLDB Endowment (PVLDB), Vol. 19, No. 5, pp. 1016–1031, 2026
- **DOI:** 10.14778/3796195.3796212
- **arXiv:** 2505.02922
- **公式実装:** https://github.com/microsoft/RetrievalAttention

## 一文要約

長文脈のKV キャッシュをCPU メモリ上の**ベクトル 保存として検索対象にし、注意機構に重要なトークンだけをGPUへ取り出す**ことで、全KVをGPUへ保持・走査するメモリ容量と帯域を減らしつつ、検索誤差による精度低下を抑えるGPU–CPU協調推論システム。

## 問題設定

長大文脈 LLMではKV キャッシュが文脈長に比例して増える。KVをすべてGPU HBMへ置けない場合はCPU DRAMへのオフロードが候補になるが、各デコード 段階で大量のKVをGPUへ戻せばCPU–GPU転送がボトルネックになる。一方、注意機構 sparsityを利用して少数トークンだけを検索する既存方式では、重要トークンの取りこぼしを避けようとすると検索量が増え、検索量を絞ると完全な 注意機構との差が大きくなりやすい。

RetroInferはこの問題を、KV キャッシュを単なるオフロード データではなく**問い合わせに応じて必要ベクトルを取り出す保存 システム**として扱うことで解く。

したがって、容量を増やすだけの退避方式とは異なり、検索で選んだ部分だけを転送し、残りの注意機構への寄与は推定で補う。検索精度、GPUへ戻す量、CPU側の保持量を一つの資源配分として扱うことが、長い文脈で転送を抑える要点である。

## 手法

### Attention-aWare VEctor index（wave index）

wave 索引は、現在の問い合わせに対して大きな注意機構を持つ可能性がある鍵をCPU側のKV集合から探す索引である。一般的な近似最近傍検索をそのまま使うのではなく、注意機構計算で必要な精度と検索費用を直接意識した構成にする。

RetroInferは注意機構対象を大きく3種類に分ける。

1. **安定 zone:** 繰り返し重要になりやすく、GPU側へ残して直接計算する部分。
2. **検索 zone:** 問い合わせに応じてCPU側索引から候補を検索し、必要なKVをGPUへ転送して正確に注意機構を計算する部分。
3. **推定 zone:** 全トークンをGPUへ運ばず、クラスタ単位の情報から残りの注意機構寄与を推定する部分。

この分割により、「精度のために全KVを取得する」か「転送削減のために強く切り捨てる」かの二択を避ける。推定誤差に上限を設けながら、正確な計算が必要な候補へ検索 予算を集中する。

### segmented clustering

長い文脈全体を毎回大規模クラスタ化すると索引構築・更新自体が高費用になる。そこで系列を区間へ分割し、各区間内で鍵をクラスタ化する。トークン生成に伴う新しいKVも局所的に追加できるため、巨大な全体 索引を繰り返し作り直す必要を減らす。

区間単位に分けるもう一つの利点は、検索索引の更新費用と検索精度を局所化できることである。長文脈全体を一つのクラスタ空間として再最適化すると、新トークン追加のたびに広い範囲の中心点や割当が変化し得る。既存区間を固定したまま末尾側だけ更新できれば、デコードの重要 経路で行う索引 保守を小さく保ち、CPU検索をGPU 注意機構と重ねやすくなる。

### wave buffer

wave バッファはGPU HBMとCPU DRAMの間で、どのKVをGPUへ残すか、どの検索 / 注意機構計算をCPUまたはGPUで進めるか、いつKVを転送するかを管理するバッファ 管理器である。CPU側の検索・データ 転送・GPU側注意機構を重ね、GPUがCPU 検索を待つ時間を減らす。

このためRetroInferは単なる疎-注意機構 アルゴリズムではなく、**索引・KV配置・CPU/GPU間転送・注意機構 実行をまとめて設計したシステム**になっている。

## 評価条件

論文および公式実装ではLlama 3系、Qwen 2.5系などの長大文脈 モデルを対象とし、RULER / LongBench等の長大文脈 ワークロードで評価している。公式実装はGPU–CPU構成を提供し、Llama-3-8B-1048Kの約120K-トークン 実演ではバッチ 4で約35 GBのGPU メモリと70 GBのCPU メモリを必要条件の目安としている。

比較対象には完全な 注意機構および既存の疎-注意機構 / KV 検索方式が含まれる。

## 主要結果

- **120K 文脈:** 完全な 注意機構に対してデコード スループットを最大 **4.4×** 改善。
- **1 百万 トークン 文脈:** 疎-注意機構 比較対象に対して最大 **12.2×** のデコード スループットを報告。
- 長大文脈 ベンチマークでは、検索量を抑えながら完全な-注意機構-水準の精度を維持したと報告している。

これらは単純なCPU オフロードの速度向上ではなく、**GPUへ実際に戻すKV量そのものを注意機構-考慮した 検索で減らした効果**を含む。

## 既存研究との差

単純なKV オフロードはCPU DRAMを容量拡張として使うが、デコードごとに必要KVを大量転送するとPCIe / 接続網 帯域が限界になる。RetroInferはCPU DRAMを検索可能なベクトル 保存として扱い、問い合わせごとに必要性が高いKVだけをGPUへ移す。

また、単純な疎 注意機構と比べると、固定パターンでKVを削るのではなく、wave 索引で問い合わせ-依存したな候補を検索し、検索しない部分にも注意機構寄与の推定を残すことで精度と検索 費用のトレードオフを扱う点が異なる。

公式repositoryは先行研究RetrievalAttentionの実装も含み、RetroInferはそのベクトル-検索型長大文脈 推論を、索引構築とGPU–CPU バッファ管理まで含む保存-エンジンとして発展させた位置付けである。

## 限界

- CPU DRAMへ大きなKV集合を保持するため、GPU HBM不足は緩和できてもホスト メモリ容量は必要になる。
- 検索、クラスタ推定、GPU–CPU転送を追加するため、短文脈やKVが十分HBMへ収まる条件ではシステム オーバーヘッドが相対的に大きくなり得る。
- 効果は注意機構 sparsityと索引が重要KVを十分正確に拾えることに依存する。モデル / ワークロードによって最適な検索 予算やキャッシュ 比率の調整が必要になる。
- SSDを通常のブロック 保存としてKVの主階層にする方式ではなく、中心はCPU DRAMとGPU HBMの協調である。したがってSSD/NVMe容量を直接利用するKV オフロード システムとはメモリ hierarchy上の制約が異なる。

## 一般的な実装上の含意

長大文脈 KV オフロードでは、保存 階層を増やすだけではなく、**「次の注意機構に必要なKVを全部転送する必要があるのか」まで変える**とCPU–GPU 帯域 要件そのものを下げられる。特にKV キャッシュをベクトル データベースに近い検索対象として扱えば、メモリ 管理器と注意機構 sparsityを別々に最適化するのではなく、検索 精度、GPU キャッシュ量、CPU メモリ量、転送 帯域を一つの予算として設計できる。

一方、この方向では索引構築・更新費用が新たなシステム 費用になるため、RetroInferの分割された クラスタ化のように増分 更新可能な索引設計が重要になる。

## 引用関係

- **先行:** RetrievalAttention (arXiv:2409.10516) — 注意機構 sparsityをベクトル 検索として扱う直接の前身。公式repositoryも共通。
- **関連:** CPU KV オフロード / 疎 注意機構研究。KVをCPUへ置くだけでなく、必要部分集合を選んで転送する系統に位置する。
- **後続・近接:** 2026年のmulti-階層 KV management研究はDRAM / SSDを含む配置・I/O スケジューリングを強く扱うのに対し、RetroInferはCPU上のKVから何を取得するかという検索側を中心に最適化する。

## 一次資料

- PVLDB / DOI: https://doi.org/10.14778/3796195.3796212
- arXiv: https://arxiv.org/abs/2505.02922
- Microsoft Research: https://www.microsoft.com/en-us/research/publication/retroinfer-a-vector-storage-engine-for-scalable-long-context-llm-inference/
- Official code: https://github.com/microsoft/RetrievalAttention
