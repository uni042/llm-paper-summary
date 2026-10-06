---
canonical_id: "arXiv:2603.02217"
title: "Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression"
summary: "本研究はMoEのexpert pruning/editing/merging後にexpertだけを変えてrouterを固定するとrouter-expert mismatchが残ることを分析し、元modelのnext-token分布をunlabeled data上で蒸留してrouterだけを校正するRouter KDを提案する。全3 compression paradigmで性能を一貫して回復し、特にexpert数が多いfine-grained MoEで効果が大きい。"
list_summary: "MoE圧縮後の品質低下をルータ-専門家 mismatchとして捉え、専門家を再学習せずルータだけを元モデルの出力分布へ蒸留して枝刈り・editing・mergingを横断的に補正する。"
authors: ["Sieun Hyeon","Jaeyoung Do"]
published: "2026-02-10"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2603.02217"
sources: ["https://arxiv.org/abs/2603.02217"]
implementation: "expert pruning、expert editing、expert mergingの代表手法を複数MoEで圧縮し、unlabeled calibration dataによるrouter-only knowledge distillationを評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2603.02217"
arxiv_categories: {primary: "cs.LG", cross_list: ["cs.AI"]}
worker_completed_at: "2026-10-06T16:59:00+09:00"
worker_run_key: "20261006-1630-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
MoE モデルのメモリ footprintを減らす代表手段には専門家 枝刈り、専門家 editing、専門家 mergingがある。これらは専門家 重みや専門家集合を変える一方、ルータを元モデルのまま残すことが多い。本論文は圧縮後の品質低下の一部が「変更後専門家へ古いルーティング 判定を適用するルータ-専門家 mismatch」に由来すると整理する。

## 問題設定
ルータはpretraining中に元の専門家集合・専門家表現に合わせて判定 boundaryを学んでいる。専門家を削除・統合・低ランク化すると、同じトークンを同じ専門家 indexへ送っても元と同じ機能にならない。専門家 パラメータを追加retrainingしないことだけを「retraining-free」とみなすと、この制御 planeのずれを放置する。

fine-grained MoEは多数の小専門家から選ぶためルーティング boundaryが複雑で、少数大専門家のcoarse-grained MoEより圧縮変更の影響をルータが受けやすい。

## 手法
Router Knowledge Distillation（Router KD）は圧縮後専門家を固定したままルータ パラメータだけを更新する。calibration dataにラベルは不要で、元の未圧縮モデルをteacherとしてnext-トークン 分布を取得し、圧縮モデルの出力 分布が近づくようルータを蒸留する。

この方法は専門家 重みを再学習しないため、枝刈りで削除した容量を戻したりmergingをやり直したりしない。変更するパラメータはルータという小部分だけで、既存のretrieving-free compression パイプラインへpost-calibrationとして追加できる。

論文は圧縮手法をExpert Pruning、Expert Editing、Expert Mergingの三群に整理し、特定手法専用の補正ではなくルータ mismatchという共通原因を検証する。

## 評価条件
|項目|内容|
|---|---|
|compression|専門家 枝刈り / editing / merging|
|calibration|unlabeled data、teacherは元モデル|
|更新パラメータ|ルータのみ|
|比較|各compression手法そのまま vs Router KD追加|
|観点|fine-grained / coarse-grained MoE、下流品質|

## 主要結果
三つのcompression paradigm全てでRouter KDが一貫した性能回復を示す。特に専門家数が多いfine-grained MoEで改善幅が大きく、ルータ 判定 boundaryの複雑さとmismatchの関係を支持する。

重要なのは、専門家側を再学習しなくてもルータだけを再適合させれば品質が戻る点である。したがってdeployment向けMoE compressionでは、パラメータ削減手法だけでなくルーティング calibrationを一つの工程として扱うべきだと結論付ける。

## 既存研究との差
既存の枝刈り/merging研究は「どの専門家を削る・まとめるか」を中心にする。本研究は圧縮後もルータを固定する慣行を横断的に検証し、compression familyに依存しないルータ-only correctionを提示する。

## 限界
完全な学習不要ではなく、少量とはいえcalibration dataとteacher 順伝播、ルータ optimizationが必要である。元モデルの出力をteacherとして使えるdeployment準備段階を前提とする。専門家自体の容量 lossが大きすぎる場合、ルータ calibrationだけでは情報を復元できない。