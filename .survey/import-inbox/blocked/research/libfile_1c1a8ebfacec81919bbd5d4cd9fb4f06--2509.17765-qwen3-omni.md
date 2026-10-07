---
canonical_id: arXiv:2509.17765
title: Qwen3-Omni Technical Report
authors: [Jin Xu, Zhifang Guo, Hangrui Hu, Yunfei Chu, Xiong Wang, Jinzheng He, Yuxuan Wang, Xian Shi, Ting He, Xinfa Zhu, Yuanjun Lv, Yongqi Wang, Dake Guo, He Wang, Linhan Ma, Pei Zhang, Xinyu Zhang, Hongkun Hao, Zishan Guo, Baosong Yang, Bin Zhang, Ziyang Ma, Xipin Wei, Shuai Bai, Keqin Chen, Xuejing Liu, Peng Wang, Mingkun Yang, Dayiheng Liu, Xingzhang Ren, Bo Zheng, Rui Men, Fan Zhou, Bowen Yu, Jianxin Yang, Le Yu, Jingren Zhou, Junyang Lin]
published: '2025-09-22'
publication: arXiv
publication_type: テクニカルレポート
publication_status: arXiv preprint
source: https://arxiv.org/abs/2509.17765
sources: [https://arxiv.org/abs/2509.17765, https://arxiv.org/html/2509.17765]
summary: Qwen3-Omniは理解を担うThinkerと音声生成を担うTalkerを分離した混合専門家モデル（MoE）のマルチモーダルLLMである。Talkerは複数音声コードブックを自己回帰生成し、従来のブロック拡散を軽量な因果ConvNetへ置換して最初のcodec frameからストリーミング可能にする。cold start時の理論first-packet latencyは234 msで、30B-A3B系を公開する。
list_summary: "Thinker–Talker型MoEと因果ConvNet音声復号を組み合わせ、マルチモーダル理解を保ちながら低頻度-start音声first-packet 遅延 234 msを実現する。"
arxiv_id: '2509.17765'
arxiv_categories:
  primary: cs.CL
  cross_list: [cs.AI, cs.CV, eess.AS]
implementation: Qwen公式リポジトリで30B-A3B、Thinking、Captioner系を公開。論文はストリーミング音声生成の構成要素別遅延を評価する。
code: https://github.com/QwenLM/Qwen3-Omni
last_checked: '2026-10-07'
worker_completed_at: '2026-10-07T16:27:33+09:00'
worker_run_key: '20261007-1627-scheduled-chat-30/r01'
reference_main_sha: 29f4b109769b6b8ca44d7851dd3d03858d75bb27
last_audited: null
audit_version: 0
---

# Qwen3-Omni Technical Report

## 概要
Qwen3-Omniはテキスト・画像・音声・動画の理解と音声生成を1系列へ統合しつつ、リアルタイム音声応答の初期遅延を抑える設計を採る。中心は理解・推論を行うThinkerと、音声トークンを生成するTalkerの分離である。両者を混合専門家モデル（Mixture of Experts; MoE）化し、総パラメータ数を増やしながら各トークンで活性化する計算量を抑える。

## 問題設定
統合マルチモーダルモデルでは、音声出力のために重い拡散復号を追加すると、LLMが回答内容を決めても最初の音声packetが出るまで待たされる。さらに音声codecは複数コードブックを持つため、全コードを大規模Transformerだけで逐次生成すると実時間率が悪化する。

## 手法
Thinkerは入力モダリティを統合して意味表現とテキスト応答を生成する。TalkerはThinkerの表現を条件として音声codec トークンを生成する。30B-A3B構成ではThinkerは総30Bのうち約3Bを活性化し、Talkerも総3Bのうち約0.3Bを活性化するため、密な同規模モデルより1 段階当たりの計算を抑える。

音声側では複数コードブックを使い、主要な自己回帰系列とは別に多トークン予測器（multi-トークン predictor; MTP）で残りのcodec トークンを生成する。さらに従来のブロック-wise diffusionを因果畳み込みネットワーク（causal ConvNet）へ置き換える。これにより最初のcodec frameが得られた時点から波形を生成でき、後続ブロックの完成を待たない。

## 評価
|項目|報告値・条件|
|---|---|
|Thinker|30B total / 約3B 活性|
|Talker|3B total / 約0.3B 活性|
|音声フレーム|約80 ms単位|
|低頻度-start first-packet 遅延|理論234 ms|
|言語対応|テキスト 119言語、speech understanding 19言語、speech generation 10言語|
|音声・音声視覚ベンチマーク|36件中open-source SOTA 32件、overall SOTA 22件|

234 msは単一のカーネル時間ではなく、入力前処理、Thinker、Talker、MTP、codec復号の初期経路を合算した理論エンドツーエンド値である。したがって本論文の推論システム上の貢献は、単にMoEでFLOPsを減らすことではなく、音声生成critical pathをストリーミング可能な部品へ分解した点にある。

## 既存研究との差
Qwen2.5-Omni系のThinker–Talker分離を発展させ、理解・生成の双方でMoEを利用する。また音声出力で拡散方式を使わず、自己回帰codecと軽量ConvNetを組み合わせることでfirst-packet 遅延を明示的な設計目標にしている。

## 限界
234 msは低頻度-start時の理論値で、ネットワーク転送、サーバ待ち行列、バッチ競合を含む実サービスSLOではない。論文は幅広い能力ベンチマークを主に扱い、GPUメモリ、最大同時要求数、実運用スループットなど一般的な推論提供指標は中心評価ではない。