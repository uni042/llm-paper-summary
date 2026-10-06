---
canonical_id: "arXiv:2603.13606"
title: "NCCL EP: Towards a Unified Expert Parallel Communication API for NCCL"
summary: "NCCL EPはMoEのexpert parallelism向けdispatch/combine通信をNCCL Device API上へ統合し、decode向け低遅延（LL）modeとprefill/training向け高throughput（HT）modeを提供する。LLは小batchでdirect RDMA+NVLink all-to-allとdouble buffering、HTは大batchでNVLink domain内集約後にinter-node RDMAを行う。H100 clusterで評価し、vLLM統合によるend-to-end inferenceも示す。"
list_summary: "MoEの分配/結合をNCCL Device APIへ統合し、小バッチ デコード用LLと大バッチ プリフィル用HTを使い分けてGPU起点のRDMA/NVLink 専門家通信を提供する。"
authors: ["Amos Goldman","Nimrod Boker","Maayan Sheraizin","Nimrod Admoni","Artem Polyakov","Subhadeep Bhattacharya","Fan Yu","Kai Sun","Georgios Theodorakis","Hsin-Chun Yin","Peter-Jan Gootzen","Aamir Shafi","Assaf Ravid","Salvatore Di Girolamo","Manjunath Gorentla Venkata","Gil Bloch"]
published: "2026-03-13"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2603.13606"
sources: ["https://arxiv.org/abs/2603.13606","https://github.com/NVIDIA/nccl"]
implementation: "NCCL Device API上にC/Pythonのdispatch/combine APIを実装し、H100 multi-node clusterでLL/HT kernelを評価、vLLM統合でend-to-end MoE inferenceを測定。実装はNVIDIA NCCL系repositoryで公開されている。"
code: "https://github.com/NVIDIA/nccl"
last_checked: "2026-10-06"
arxiv_id: "2603.13606"
arxiv_categories:
  primary: "cs.DC"
  cross_list: []
worker_completed_at: "2026-10-06T11:25:00+09:00"
worker_run_key: "20261006-1100-scheduled-chat-00/r01"
reference_main_sha: "3e052b967c7905af42ea292d8e91d2f747ff9aed"
last_audited: null
audit_version: 0
---

## 概要

混合専門家モデル（Mixture of Experts; MoE）を複数GPUへ専門家 並列化で配置すると、ルータが選んだ専門家のGPUへトークンを送る分配と、計算後の出力を元トークン順へ戻す結合が各MoE層で必要になる。近年はGPU起点RDMAを使うDeepEP等の専用libraryが高性能を示す一方、通信stackがNCCL本体と分かれ、topology管理やAPI統合が複雑になる。

NCCL EPはこのMoE通信をNCCL Device API上へ構築し、`ncclEpDispatch`と`ncclEpCombine`という統一primitiveを提供する。デコードの小バッチには低遅延（Low-Latency; LL）mode、プリフィルや学習の大バッチには高スループット（High-Throughput; HT）modeを使う。H100 multi-ノード環境でカーネル性能を評価し、vLLM統合によるエンドツーエンド推論も示す。

## 問題設定

専門家 並列化ではトークンごとに宛先ランクが異なり、通常の固定集合通信より不規則な全対全通信になる。デコードは1〜128 トークン級の小さいメッセージが多く、software オーバーヘッドとhop数が支配的になる。一方プリフィル/学習は4096 トークン以上の大バッチになり、ネットワーク帯域を飽和させる大きな転送が中心になる。

一つの通信algorithmで両方を最適化するのは難しい。さらにCPUが各転送を起動するとカーネル 起動やホスト synchronizationがcritical pathへ入りやすい。NCCL EPはGPU-initiated networkingとtopology-aware NCCL infrastructureを共通基盤にし、ワークロード サイズに応じて通信algorithmを分ける。

## 手法

### 統一dispatch/combine API

ルータのtop-k 専門家 assignmentからhandleを作り、分配でトークンを専門家所有ランクへ送り、専門家計算後に結合で出力を元ランクへ返す。CとPython interfaceを提供し、MoE フレームワーク側が独自RDMA protocolを直接管理する必要を減らす。

NCCL Device APIのLoad-Store Accessible（LSA）操作とGPU-Initiated Networking（GIN）を使い、NVLinkとRDMAをGPU側から駆動する。CPU involvementをcritical pathから外し、NCCLのtopology detectionとネットワーク pluginを再利用する。

### LL mode

LLは小バッチ デコード向けで、ランク間をdirect 全対全通信 RDMA+NVLink meshとして扱う。階層集約を挟まずhopを減らし、double バッファで分配/結合や計算との重畳を可能にする。

小メッセージでは帯域最大化より固定遅延を抑える方が重要なため、このdirect pathを選ぶ。対象は概ね1〜128 トークン規模である。

### HT mode

HTは4096 トークン以上のプリフィル/学習向けで、まずNVLink domain内でトークンを集約し、その後ノード間 RDMAを行う階層通信を使う。大メッセージでは集約によってネットワーク transactionをまとめ、ノード間帯域を効率良く使う。

LLとHTを同じAPI下へ置くことで、推論提供 システムは局面に応じてalgorithmを選びながらルーティング metadataと通信管理を共通化できる。

## 評価条件

| 項目 | 条件 |
|---|---|
| accelerator | NVIDIA H100 cluster |
| interconnect | NVLink + ノード間 RDMA |
| ワークロード | MoE 分配/結合 |
| LL対象 | 小バッチ、概ね1〜128 トークン |
| HT対象 | 大バッチ、概ね4096 トークン以上 |
| システム integration | vLLM |
| 指標 | 分配/結合 カーネル性能、エンドツーエンド inference |

## 主要結果

論文はH100 multi-ノード構成でLL カーネルが既存GPU-initiated 専門家 通信 libraryと競争力のある性能を持つことを示し、HTについても大バッチ向け階層通信のscaleを評価する。さらにvLLMへ統合し、通信マイクロベンチマークだけでなくMoE inference pathで利用可能であることを確認する。

重要なのは単一のheadline倍率より、デコードとプリフィルで異なるメッセージ geometryへ別algorithmを割り当てながら、同一NCCL APIへ統合した点である。公開実装でもLL/HT、分配/結合、Python bindingが提供される。

## 既存研究との差

DeepEPやHybrid-EPはMoE専用GPU-initiated 通信の性能を示したが、NCCLとは別のlibraryとして構築される。NCCL EPはLSA/GINを含むNCCL Device API上へ同じ通信patternを実装し、NCCLのtopology awareness、ネットワーク plugin、既存communicator ecosystemへ統合する。

## 限界

LLとHTには対象バッチ範囲があり、中間領域ではalgorithm選択が必要になる。初期公開実装には対応隠れ dimension、top-k、shared-メモリ資源、ノード数などの制約がある。論文評価はH100中心であり、他GPU世代・ネットワーク topologyでは再測定が必要である。

## 一次資料

- https://arxiv.org/abs/2603.13606
- https://github.com/NVIDIA/nccl