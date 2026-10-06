---
canonical_id: "arXiv:2204.09656"
title: "A Fast Post-Training Pruning Framework for Transformers"
summary: "本手法は学習済みTransformerを再学習せず構造化枝刈りするため、Fisher情報による軽量mask search、mask rearrangement、layer出力を再構成するmask tuningを組み合わせる。BERT-baseとDistilBERTのGLUE/SQuADで精度低下を1%未満に抑えつつFLOPsを最大2倍削減し、推論遅延を最大1.56倍高速化、単一GPUで3分未満に枝刈りする。"
list_summary: "Fisher情報によるヘッド/filter選択とmask再配置・局所再構成により、再学習なしでTransformerを数分で構造化枝刈りし実測推論を高速化する。"
authors: ["Woosuk Kwon","Sehoon Kim","Michael W. Mahoney","Joseph Hassoun","Kurt Keutzer","Amir Gholami"]
published: "2022-03-29"
publication: "NeurIPS 2022"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2204.09656"
sources: ["https://arxiv.org/abs/2204.09656"]
implementation: "BERT-baseとDistilBERTを対象に、sample datasetだけを使うpost-training structured pruningとして実装し、GLUE/SQuADでFLOPs、latency、accuracy、pruning timeを評価。確認済み一次資料から公式code URLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2204.09656"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.CL"]
worker_completed_at: "2026-10-06T18:28:00+09:00"
worker_run_key: "20261006-1800-scheduled-chat-00/r01"
reference_main_sha: "f5213871027dd0aa06635e6ff813a108d30ea80d"
last_audited: null
audit_version: 0
---

## 概要

構造化枝刈り（structured 枝刈り）は注意機構 ヘッドやfeed-順伝播 filterを丸ごと削除するため、非構造疎性と違って通常の密 カーネルでもテンソル dimensionを小さくできる。しかし従来のTransformer 枝刈りは枝刈り後に長い微調整を行うものが多く、モデルごとの再学習コストがdeploymentの障害になる。

本論文は学習済みモデルと少量標本だけから数分で構造化枝刈りを行う。Fisher情報を使うmask searchで削除候補を選び、mask rearrangementで同じsparsity内の組合せを改善し、最後にmask tuningで各層の出力を元モデルへ近づける。BERT-base/DistilBERTでは精度低下1%未満でFLOPsを最大2倍削減し、推論遅延を最大1.56倍高速化する。

## 問題設定

単純なmagnitude 枝刈りは重み単位の非構造疎性を作りやすいが、一般GPUでは専用sparse カーネルなしに実測速度へ結びつきにくい。注意機構 ヘッドやFFN neuronを構造単位で削れば行列dimensionそのものを縮められるが、どの構造を削るかを誤るとaccuracyが急落する。

従来のiterative 枝刈り + 微調整はこのaccuracyを回復できる一方、pretrained Transformerごとに大量の勾配 段階が必要になる。deployment前の短時間処理という要件と両立しない。

## 手法

### Fisher情報によるmask search

各注意機構 ヘッドとFFN filterへ二値 maskを置き、標本 data上のloss感度からFisher情報ベースの重要度を推定する。資源 constraintに合わせ、重要度の低い構造から削る。全重みを再学習せず、mask選択だけを軽量に探索する。

### Mask rearrangement

独立importanceだけで選ぶと、同一層内の構造間相関を無視する。mask rearrangementは枝刈り数を変えずにmask位置を入れ替え、近似されたloss増加が小さい組合せへ修正する。したがってFLOPs budgetを維持したままselection errorを減らす。

### Mask tuning

mask確定後、元層の活性値を対象として残存構造のscale等を調整し、枝刈り 層の出力を再構成する。エンドツーエンド 微調整ではなく層局所の再構成なので、数分というpost-学習 budgetへ収める。

### Resource-aware pruning

注意機構とFFNは同じ1構造を削ってもFLOPs/遅延への寄与が違う。資源 constraintを探索へ含め、単純に全層同率で削るのではなく、accuracyへの影響と計算削減を釣り合わせる。

## 評価条件

| 項目 | 内容 |
|---|---|
| models | BERT-base、DistilBERT |
| tasks | GLUE、SQuAD |
| 枝刈り | 注意機構 ヘッド / FFN filterのstructured 枝刈り |
| 学習 | 全体 retrainingなし、標本 dataによるpost-学習処理 |
| 指標 | accuracy/F1、FLOPs、実測遅延、枝刈り時間 |
| 枝刈り時間 | 単一GPUで3分未満 |

## 主要結果

精度低下を1%未満に抑えた条件でFLOPsを最大2.0倍削減し、推論遅延を最大1.56倍高速化する。FLOPs削減率より遅延 高速化倍率が小さいことから、残る演算子やメモリ/起動 オーバーヘッドが実測時間を支配する部分も確認できる。

枝刈り自体は単一GPUで3分未満で完了し、再学習を伴う既存枝刈り方式より2桁以上短い。mask searchだけでなくrearrangementとtuningを加えることで、同じ資源 budgetでaccuracyを回復する。

## 既存研究との差

Movement 枝刈り等は微調整過程でsparsityを学習する。本方式はpretrained モデルを固定したpost-学習段階で構造選択と局所再構成を済ませるため、deploymentごとの学習 コストを抑える。SparseGPTのような後年のLLM 重み 枝刈りより対象モデルは小さいが、通常密 演算子へ直接反映できるstructured sparsityを狙う点が異なる。

## 限界

評価はBERT-baseとDistilBERTが中心で、数十〜数百B パラメータのdecoder-only LLMへ同じ3分未満の処理時間を外挿できない。1.56倍は実測最大値であり、FLOPs 2倍削減が常に2倍遅延になるわけではない。標本 dataの代表性が低い場合、Fisher importanceと活性値 reconstructionの品質も低下し得る。

## 一次資料

- https://arxiv.org/abs/2204.09656