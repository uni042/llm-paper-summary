---
canonical_id: "arXiv:2602.06154"
title: "MoSE: Mixture of Slimmable Experts for Efficient and Adaptive Language Models"
summary: "MoSEはMoEのexpert内部をnestedなslimmable構造にし、routerが「どのexpertか」だけでなく「expertを何割実行するか」まで変えられる単一modelを学習する。OpenWebText上のGPT実験でfull-widthの標準MoEと同等以上の品質を保ち、固定FLOPs budgetではrouter confidenceから幅を決めるtest-time適応によりaccuracy-compute Pareto frontierを改善する。"
list_summary: "MoE 専門家を可変幅の入れ子構造にして、専門家選択と専門家内部の計算量を同時に条件付き制御し、連続的な品質―FLOPs交換を可能にする。"
authors: ["Nurbek Tastan","Stefanos Laskaridis","Karthik Nandakumar","Samuel Horvath"]
published: "2026-02-05"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2602.06154"
sources: ["https://arxiv.org/abs/2602.06154"]
implementation: "OpenWebTextで学習したGPT系MoEを用い、複数expert幅、runtime width policy、固定FLOPs budgetでperplexity/compute trade-offを評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2602.06154"
arxiv_categories: {primary: "cs.LG", cross_list: []}
worker_completed_at: "2026-10-06T12:48:00+09:00"
worker_run_key: "20261006-1230-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
通常の混合専門家（Mixture-of-Experts; MoE）はトークンごとに専門家を疎に選ぶが、選ばれた専門家のFFNは常に全幅で実行する。このためtop-kや専門家数を変えない限り計算量の粒度が粗い。MoSEは各専門家を入れ子状の可変幅ネットワークにし、同じ専門家でもトークンに応じて一部経路だけを実行できるようにする。

## 手法
各専門家の小幅subnetworkは大幅subnetworkの接頭辞として含まれるslimmable構造を持つ。一つの重み集合を複数幅で共有するため、deployment時に幅ごとのモデルを別々に保持する必要がない。学習では複数幅を同時に標本するmulti-width 学習を標準MoE 目的関数と組み合わせ、狭いsubnetworkも単独で機能するようにする。

推論時はルータ probability/confidenceを計算難度の代理指標として使い、専門家ごとの実行幅を決める。固定FLOPs budgetの下では軽量なtest-time 学習でconfidenceからwidthへのmappingを調整し、budgetを超えずに難しいトークンへ広い専門家を配分する。

これにより条件付き計算は専門家間の選択だけでなく専門家内部へも拡張される。top-kを整数で切り替える方式より細かな計算量調整が可能で、同一チェックポイントから複数deployment budgetへ対応できる。

## 評価条件
|項目|条件|
|---|---|
|モデル|GPT系MoE|
|学習 data|OpenWebText|
|比較|標準全体-width MoE、固定幅設定|
|制御|ルータ confidence/probabilityに基づく専門家 width|
|指標|language modeling品質、FLOPs、Pareto frontier|

## 主要結果
全体 widthでは標準MoEと同等以上の性能を保ち、幅を適応化した設定では同等品質に必要なFLOPsを削減してaccuracy-compute Pareto frontierを一貫して外側へ移す。単に全専門家を一律に細くするより、ルータ confidenceに応じてトークンごとに幅を変える方が固定budgetを有効利用する。

## 既存研究との差・限界
標準MoEが「専門家を選ぶ」離散的conditional computationなのに対し、MoSEは選択後の専門家幅も条件付きにする。動的幅の実利は可変形状を効率よく実行できるランタイムに依存し、FLOPs削減がそのままGPU 実時間高速化になるとは限らない。評価はOpenWebText上のGPT実験が中心で、大規模production MoE 推論提供の通信・専門家 並列化を直接評価していない。