---
canonical_id: "arXiv:2408.10188"
title: "LongVILA: Scaling Long-Context Visual Language Models for Long Videos"
summary: "LongVILAは長時間video向けVLMをalgorithm-system co-designし、Multi-Modal Sequence Parallelismでvision tokenとtext tokenをGPU間へ分割する。256 GPUで2M contextをgradient checkpointingなしに扱い、ring-style sequence parallelism比2.1–5.7倍、Megatron hybrid context/tensor parallelism比1.1–1.4倍の高速化を報告する。"
list_summary: "multi-modal 系列 並列化で長videoの視覚・言語トークンを分散し、2M 文脈までのVLM学習・推論を多数GPUへscaleさせる。"
authors: ["Yukang Chen","Fuzhao Xue","Dacheng Li","Qinghao Hu","Ligeng Zhu","Xiuyu Li","Yunhao Fang","Haotian Tang","Shang Yang","Zhijian Liu","Ethan He","Hongxu Yin","Pavlo Molchanov","Jan Kautz","Linxi Fan","Yuke Zhu","Yao Lu","Song Han"]
published: "2024-08-19"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2408.10188"
sources: ["https://arxiv.org/abs/2408.10188"]
implementation: "VILAを長videoへ拡張し、MM-SPを最大256 GPUでtraining/inference評価。公式LongVILAコード・モデル公開。"
code: "https://github.com/NVlabs/VILA/tree/main/longvila"
last_checked: "2026-10-06"
arxiv_id: "2408.10188"
arxiv_categories: {primary: "cs.CV", cross_list: ["cs.AI","cs.CL"]}
worker_completed_at: "2026-10-06T09:46:00+09:00"
worker_run_key: "20261006-0930-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
LongVILAは長時間video理解でframe数を増やすとvisual トークンが巨大化し、単一GPUへ注意機構 状態を置けなくなる問題を、モデル学習手順と分散実行系の両方から解く。VILAの入力を8 frameから2048 frameへ拡張し、長文脈拡張とlong-video supervised 微調整を追加する。

## 手法
中心となる多モーダル系列並列（Multi-Modal Sequence Parallelism; MM-SP）は、テキストだけを想定した系列 並列化を画像・video トークンへ拡張する。長いトークン 系列をGPU群へ分割し、各deviceが保持する活性値/KV状態を減らす一方、注意機構に必要な情報を通信する。

既存ring 注意機構は長系列で通信と計算の同期が律速になりやすい。MM-SPはmulti-modal トークン配置と並列軸を調整し、文脈 並列化とテンソル 並列化を組み合わせてGPU メモリと通信を分散する。Hugging Face Transformersへ統合可能な形で実装されている。

## 評価条件
|項目|条件|
|---|---|
|モデル|LongVILA-7B等|
|最大文脈|2M トークン|
|最大GPU|256 GPUs|
|video|最大2048 sampled frames、探索対象評価6000 frames|
|比較|ZigZag Ring Attention、Megatron CP+TP等|

## 主要結果
256 GPUで2M-トークン 文脈の学習を勾配 checkpointingなしで実行する。MM-SPはring-style 系列 並列化比2.1–5.7倍高速で、Megatronのhybrid 文脈/テンソル 並列化比でも1.1–1.4倍高速と報告する。個別評価では最適化されたMegatron ring-style CPに3.1–4.3倍の差を示す条件もある。

モデル側では6000-frame・100万トークン超の探索対象-in-a-haystackで99.8% accuracy、VideoMMEでsubtitleあり65.1%を示す。長文脈を「動かせる」だけでなく、増やしたframeを実際に検索・理解へ使えていることを確認する評価である。

## 限界
主なシステム利得は多数GPU環境の系列 並列化であり、単一GPUや民生 GPUへ直接移植できる高速化ではない。長video用微調整と大規模分散環境が必要で、純テキスト 推論提供のcontinuous batchingやKV オフロードは評価対象外である。