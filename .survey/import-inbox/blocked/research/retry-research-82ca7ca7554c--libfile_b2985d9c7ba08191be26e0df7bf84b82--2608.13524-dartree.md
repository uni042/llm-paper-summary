---
canonical_id: "arXiv:2608.13524"
title: "DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees"
summary: "DARTreeはdiffusion drafterのposition-wise marginal予測へ既存のautoregressive correction headをtree全branchへ拡張し、各depthのnodeをbatchで一括展開してからbest-first pruningする。追加学習なしで7 benchmarkを評価し、最大12.97 token/verificationを受理、DFlash比98.6%、Domino比27.9%長いacceptanceと最大9.73倍のlossless speedupを報告する。"
list_summary: "diffusionの並列ブロック ドラフトへ自己回帰補正をtree単位で適用し、逐次heap操作を避けながら分岐品質と無損失 投機的復号速度を高める。"
authors: ["Tianyi Li","Yaxin Luo","Xinyi Shang","Zhiqiang Shen"]
published: "2026-08-13"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2608.13524"
sources: ["https://arxiv.org/abs/2608.13524"]
implementation: "math/code/chatの7 benchmark、4つのmodel-temperature構成でDFlash、Domino等とacceptance lengthとwall-clock speedupを比較。training-free。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2608.13524"
arxiv_categories: {primary: "cs.CL", cross_list: []}
worker_completed_at: "2026-10-06T11:54:00+09:00"
worker_run_key: "20261006-1130-scheduled-chat-30/r02"
last_audited: null
audit_version: 0
---
## 概要
拡散型言語モデルをdrafterに使う投機的復号（投機的復号）はブロック全体を並列予測できるが、各位置の分布は選ばれた前トークンを条件にしないmarginalである。chain向け自己回帰補正を入れても、treeの各分岐へ条件依存を伝えなければ候補深度とともに対象モデルとのずれが増える。DARTreeは既存の自己回帰補正ヘッドをtreeへ学習不要で拡張する。

## 手法
各深さで現在の全ノードを一つのバッチとしてAR correction ヘッドへ通し、親トークンを条件にしたcandidate スコアを作る。ノードごとに逐次priority queueを更新するのではなく、深さ単位で固定幅のcandidate treeをまず構築する。

tree生成後にbest-first 枝刈りを行い、対象モデルへ渡す検証 treeだけを選ぶ。この順序によりAR-ヘッド inferenceをheap操作から分離し、GPU上では深さ内のノードを並列に処理できる。対象 検証は通常の投機的復号と同様に無損失で、対象 分布を変更しない。

## 評価条件
|項目|条件|
|---|---|
|タスク|math、コード、chatの7 ベンチマーク|
|設定|4 モデル-temperature構成|
|比較|DFlash、Domino等|
|指標|average 受理率 length、無損失 高速化倍率|
|学習|追加学習なし|

## 主要結果
全4 モデル-temperature構成で平均受理率 lengthと高速化倍率が比較手法中最高となる。最大条件では1 検証 round当たり12.97 トークンを受理し、DFlashより98.6%、Dominoより27.9%長い。

ローカル測定した通常autoregressive 復号比では最大9.73倍の無損失 高速化倍率を報告する。候補を増やすだけでなく、分岐ごとに自己回帰条件を入れることで深いtreeのproposal qualityを保つことが寄与する。

## 既存研究との差・限界
DFlashは並列性が高いがposition間依存が弱く、chain correctionは一本のドラフト pathに限定される。DARTreeはcorrectionをtree全体へbatched展開する。最大9.73倍は特定モデル/タスク/temperatureの上限であり、tree幅・深さを増やすほどドラフト/検証計算も増える。既存AR correction ヘッドを前提にするため、任意のdiffusion drafterへ完全に無変更で適用できるわけではない。