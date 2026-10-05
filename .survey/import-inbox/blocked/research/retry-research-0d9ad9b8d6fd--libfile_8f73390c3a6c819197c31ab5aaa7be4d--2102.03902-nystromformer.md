---
canonical_id: "arXiv:2102.03902"
title: "Nyströmformer: A Nyström-Based Algorithm for Approximating Self-Attention"
summary: "Nyströmformerはsoftmax自己注意行列をNyström法で近似し、系列から選ぶlandmarkを介した3つの小行列積と擬似逆行列で全token対attentionを近似する。landmark数を固定すれば時間・メモリを系列長に対して線形化でき、GLUE/IMDBで標準attentionに近い品質、Long Range Arenaで競争力ある長系列性能を示す。"
list_summary: "Nyström法で少数landmarkからsoftmax 注意機構行列を再構成し、標準自己注意の二次メモリ・計算を線形近似へ置き換える。"
authors: ["Yunyang Xiong","Zhanpeng Zeng","Rudrasis Chakraborty","Mingxing Tan","Glenn Fung","Yin Li","Vikas Singh"]
published: "2021-02-07"
publication: "AAAI Conference on Artificial Intelligence 2021"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2102.03902"
sources: ["https://arxiv.org/abs/2102.03902", "https://github.com/mlpen/Nystromformer"]
implementation: "BERT系encoderへNyström self-attentionを組み込み、GLUE、IMDB、Long Range Arenaで標準attentionおよびefficient attention方式と比較。公式実装公開。"
code: "https://github.com/mlpen/Nystromformer"
last_checked: "2026-10-06"
arxiv_id: "2102.03902"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.LG"]}
worker_completed_at: "2026-10-06T07:52:00+09:00"
worker_run_key: "20261006-0730-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
Nyströmformerは、標準Transformerのsoftmax自己注意行列そのものを低ランク近似し、系列長に対する二次計算と二次メモリを避ける方式である。Nyström法は大きな行列の一部の列・行をlandmarkとして選び、その交差部分の擬似逆行列から全体を近似する。

自己注意へ直接適用するにはsoftmaxの正規化が行列全体に依存するため単純な列samplingでは扱いにくい。Nyströmformerは問い合わせ/keyをsegmentごとに平均してlandmark 問い合わせ/keyを作り、3個のsoftmax小行列へ分解して近似注意機構を構成する。

## 問題設定
長さn、ヘッド次元dの標準自己注意はQK^Tにn×n行列を作るため、時間・メモリがO(n²)になる。長文書では活性値 メモリが急増し、系列を数千トークンへ伸ばすことが難しい。

既存のsparse 注意機構は接続patternを固定し、カーネル近似はsoftmaxをfeature mapへ置換する。Nyströmformerは注意機構 matrixを低ランクとみなし、行列近似の立場から少数landmarkで復元する。

## 手法
系列をm個のsegmentへ分け、各segmentの問い合わせ/key平均をlandmarkとして作る。全問い合わせからlandmark keyへの注意機構、landmark 問い合わせ間注意機構、landmark 問い合わせから全keyへの注意機構の3行列を計算する。

中央のm×m 注意機構行列にはMoore-Penrose擬似逆行列が必要になる。直接SVDすると高価なため、論文は反復的な擬似逆近似を使う。mを系列長より十分小さく固定すれば、主要なトークン-landmark積はO(nm)になり、nに対して線形に増える。

近似注意機構だけでは局所情報が弱くなる場合があるため、valueへdepthwise convolutionを加えるresidual connectionを導入する。これは近傍トークン間の局所patternを低コストで補い、低ランク近似で失われる局所性を補完する。

## 評価条件
|観点|内容|
|---|---|
|基盤モデル|BERT系encoder|
|標準長タスク|GLUE、IMDB|
|長系列|Long Range Arena|
|比較|標準self-注意機構、Linformer、Performer等|
|複雑度|landmark数m固定時に系列長nへ線形|

## 主要結果
GLUEとIMDBの通常系列長では標準self-注意機構と概ね同等、一部タスクではわずかに上回る結果を示す。Long Range Arenaでは他のefficient 注意機構方式に対して競争力あるaccuracyを示し、数千トークンへ系列を伸ばせることを確認した。

効率利得はmがnより十分小さい条件で生じる。mを増やせば近似精度は上がる一方、トークン-landmark積と中央行列の処理費用が増えるため、品質と速度・メモリの交換条件になる。

## 既存研究との差
Linformerがkey/value系列次元をlearned 射影で縮約するのに対し、Nyströmformerはsoftmax 注意機構 matrixをlandmarkから近似する。Performerのrandom featureとは異なり、Nyström法という決定的な低ランク行列近似を使う。

## 限界
評価はencoder中心で、現代decoder-only LLMのKV キャッシュ付き逐次生成やcontinuous batchingを直接扱わない。landmark数とsegment平均が情報ボトルネックになり、注意機構行列が低ランクで表しにくい入力では近似誤差が増え得る。