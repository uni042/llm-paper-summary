---
canonical_id: "DOI:10.1145/3689031.3696075"
title: "HybridFlow: A Flexible and Efficient RLHF Framework"
summary: "HybridFlowはRLHFを複数LLMから成る分散データフローとして扱い、モデル間は単一コントローラ、各モデル内部は複数コントローラで実行する階層型プログラミングモデルを導入する。さらに3D-HybridEngineでactorの学習・生成間の再シャーディングを冗長weightなしで行い、自動GPU配置と合わせてDeepSpeed-Chat、OpenRLHF、NeMo-Aligner等に対し1.53〜20.57倍のスループット改善を報告する。"
list_summary: "RLHFのモデル間制御とモデル内分散実行を分離し、actor再シャーディングとGPU配置を最適化して複数RLHF方式のスループットを高める。"
authors: ["Guangming Sheng","Chi Zhang","Zilingfeng Ye","Xibin Wu","Wang Zhang","Ru Zhang","Yanghua Peng","Haibin Lin","Chuan Wu"]
published: "2024-09-28"
publication: "EuroSys 2025"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2409.19256"
sources: ["https://arxiv.org/abs/2409.19256","https://github.com/volcengine/verl"]
implementation: "HybridFlowはverlとして公開され、PPO、Safe-RLHF、ReMax等のRLHFデータフローを複数GPUで評価する。3D parallelism、ZeRO、FSDPと生成用並列化を統合する。"
code: "https://github.com/volcengine/verl"
last_checked: "2026-10-06"
arxiv_id: "2409.19256"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.DC"]
worker_completed_at: "2026-10-06T18:13:00+09:00"
worker_run_key: "20261006-1800-scheduled-chat-00/r01"
reference_main_sha: "f5213871027dd0aa06635e6ff813a108d30ea80d"
---

## 概要

人間フィードバック強化学習（reinforcement learning from human feedback; RLHF）は、actor、critic、reference policy、reward modelなど複数の大規模言語モデル（LLM）を、生成・推論・学習という異なる役割で反復実行する。通常の分散学習と違い、各モデル内部ではテンソル並列・パイプライン並列・データ並列を使う一方、モデル間では生成結果、log probability、value、rewardなどを別の分割形状へ再配置して渡す必要がある。HybridFlowはこの「モデル内部の分散計算」と「モデル間データフロー」を別階層として表現する。

モデル間は単一コントローラ（single-controller）が順序と転送を統括し、モデル内部は各GPU側の複数コントローラ（multi-controller）で既存の高性能分散ランタイムを動かす。actorについては、学習に向く3次元並列構成と生成に向く構成を切り替える3D-HybridEngineを設計し、weightの二重保持を避けて再シャーディングする。さらにRLHFデータフロー全体を見て各モデルのGPU配置を選ぶ。評価では既存RLHFシステムに対し1.53〜20.57倍のスループット改善を報告する。

## 問題設定

PPO型RLHFでは、actorが応答を生成し、critic・reference・reward modelがその応答を評価し、その後actorとcriticを更新する。actor学習は計算律速になりやすく大きなモデル並列度が有利だが、自己回帰生成はメモリ帯域律速になりやすく、同じGPU数ならモデル並列度を下げてデータ並列replicaを増やす方が高スループットになり得る。

そのため学習と生成でactorのweight配置を変えたいが、70B modelでは1 iterationごとに140GBのweight転送が生じ得る。既存方式には学習用と生成用のactor copyを二重保持するもの、同じ並列構成を固定して生成効率を犠牲にするもの、ZeROからtensor parallelへ高コストに再シャーディングするものがある。また各model programへpoint-to-point転送処理を埋め込むmulti-controller設計は、RLHF algorithmを変えるたびに依存model側のcodeまで修正しやすい。

## 手法

### 階層型ハイブリッド制御

HybridFlowはactor、critic、reference、reward modelをnodeとして扱い、node間の依存を中央の単一コントローラが記述する。単一コントローラは各GPU operatorを逐一dispatchせず、「actor.generate」「critic.compute_values」のような粗粒度APIを呼ぶため、巨大LLM内部のdispatch overheadを中央へ集めない。

各node内部ではMegatron系3D並列、ZeRO、FSDPなど既存の複数コントローラ方式をそのまま使う。これによりGPU間collectiveは各ランタイムが高速に実行し、node間のmany-to-many転送だけを上位controllerが調停する。

### Transfer protocol

modelごとに並列度が違うため、送信側のtensor partitionと受信側が必要とするpartitionは一致しない。HybridFlowはこの再配置をtransfer protocolとしてAPIの裏へ隠し、RLHF algorithmのcontrol flowからcollective通信の詳細を分離する。結果としてactorの実装を変えてもcritic/reward側へ通信codeを波及させにくい。

### 3D-HybridEngine

actorのtrainingとgenerationは同じweightを使うが、最適な並列配置が異なる。3D-HybridEngineはtraining側のpipeline/tensor/data parallel shardからgeneration側の配置へweightを再編し、生成後に戻す。別copyを常駐させず、必要な通信だけを行うため、OpenRLHF型の二重weight memoryと単純な全量転送を避ける。

### 自動device mapping

各RLHF nodeはtraining、inference、generationで計算量とmemory footprintが異なる。HybridFlowはmodel size、workload、data dependencyを使い、modelを同じGPU集合へcolocateするか別集合へ分けるかを探索する。分離すれば独立nodeを並列実行できる一方idle GPUが生じ、colocateすればmemoryを共有する代わり逐次実行になるため、その交換条件をデータフロー全体で選ぶ。

## 評価条件

| 項目 | 内容 |
|---|---|
| RLHF方式 | PPO、Safe-RLHF、ReMax等 |
| 比較対象 | DeepSpeed-Chat、OpenRLHF、NeMo-Aligner等 |
| actor処理 | 自己回帰生成と分散学習を反復 |
| 並列方式 | 3D parallelism、ZeRO、FSDP、生成側model/data parallel |
| 主指標 | RLHF training throughput、stage time、resharding overhead |
| 公開実装 | verl |

## 主要結果

既存RLHF systemとの比較で、model size、cluster scale、RLHF algorithmに応じて1.53〜20.57倍のthroughput改善を報告する。改善幅が大きく変わるのは、baselineごとにactorの二重保持、固定配置、再シャーディングなど異なる制約を持つためである。

論文のprofilingではactor trainingとgenerationが主要時間を占め、HybridFlowでも合計58.9%に達する例がある。このため3D-HybridEngineによる両stageの並列構成切替は局所的最適化ではなくiteration全体へ効く。一方、RLHF algorithmやmodel比率が変われば最適placementも変わるため、単一固定配置を全条件の最適解とはしていない。

## 既存研究との差

DeepSpeed-ChatはZeRO学習とtensor-parallel生成の間でactorを変換し、OpenRLHFは学習用・生成用actorを別copyとして保持する。NeMo-Alignerは同じ3D partitionを両stageで共有する。HybridFlowはweightを二重保持せずにstage間で3D配置を変えられる点と、モデル間dataflowを中央制御へ分離してRLHF algorithmを組み替えやすくする点を同時に扱う。

## 限界

RLHF全体の高速化はactor/critic/rewardのmodel size比、生成長、cluster規模、network、選択したRLHF algorithmに依存する。1.53〜20.57倍は単一条件の普遍的倍率ではない。また本方式は複数modelを持つRLHF pipelineを対象とし、通常のpretrainingだけに同じdataflow abstractionを導入して同等の利得が出ることを示すものではない。

## 一次資料

- https://arxiv.org/abs/2409.19256
- https://github.com/volcengine/verl