---
canonical_id: DOI:10.18653/v1/2021.eacl-main.8
title: "BERxiT: Early Exiting for BERT with Better Fine-Tuning and Extension to Regression"
summary: "BERxiTは、BERT系Transformerの各中間層へ予測headを置き、入力ごとに十分な確信が得られた層で計算を終了する早期終了を改善する。複数出口を同時学習するとbackboneの最適化が競合する問題へ交互fine-tuningを導入し、分類確率のconfidenceが使えない回帰にも学習型exit判定器を拡張する。BERT/RoBERTa/ALBERTおよびDistilBERTで品質と計算量の交換条件を改善する。"
list_summary: "中間層exitを交互fine-tuningで安定化し、学習型exit判定で回帰にも早期終了を拡張して、BERT系推論の入力別計算量を削減。"
authors:
  - Ji Xin
  - Raphael Tang
  - Yaoliang Yu
  - Jimmy Lin
published: "2021-04"
publication: "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume"
publication_type: 国際会議論文
publication_status: published
source: https://aclanthology.org/2021.eacl-main.8/
sources:
  - https://aclanthology.org/2021.eacl-main.8/
  - https://aclanthology.org/2021.eacl-main.8.pdf
implementation: "BERT、RoBERTa、ALBERTとDistilBERTへ複数中間exitを追加し、分類・回帰タスクで品質と計算量の交換条件を評価。公式コードはcastorini/berxitで公開されている。"
code: https://github.com/castorini/berxit
last_checked: "2026-10-07"
worker_completed_at: "2026-10-07T17:35:03+09:00"
worker_run_key: "20261007-1735-scheduled-chat-30/r01"
reference_main_sha: "96e46e336be8e3716ca9bb21c93a09c05bf96666"
last_audited: null
audit_version: 0
---

## 概要

BERxiTは、入力ごとに必要なTransformer層数が異なることを利用してBERT系モデルの推論計算量を削減する早期終了（early exiting）方式である。通常のBERTは簡単な入力でも最終層まで全層を通るが、早期終了では各中間層へ予測headを置き、十分に信頼できる予測が得られた入力だけ途中で停止する。難しい入力は後段まで進むため、品質と平均計算量を連続的に調整できる。

先行するDeeBERT等では、複数の中間classifierを一度にfine-tuningすると、浅い出口と深い出口が同じbackboneへ異なる勾配を与え、事前学習済みBERTの能力を十分に引き出せない問題があった。またexit判定をsoftmax confidenceやentropyへ依存すると、分類のような確率分布を出すタスクには使えても、連続値を直接予測する回帰へそのまま適用できない。

BERxiTはこれらへ、backboneと中間出口の学習を分ける交互fine-tuningと、入力の中間表現から「ここで終了してよいか」を学ぶlearning-to-exit（LTE）moduleを導入する。BERT、RoBERTa、ALBERTに加え、既に圧縮されたDistilBERTとも組み合わせられることを示し、早期終了を単独の圧縮法ではなく他の高速化と重ねられる入力適応計算として位置付ける。

## 問題設定

Transformer encoderの各層は同じ幅のhidden stateを次層へ渡すため、標準推論では入力の難しさに関係なく固定深度を実行する。しかし分類・回帰タスクでは、浅い層ですでに正しい判断に十分な入力と、深い文脈処理が必要な入力が混在する。固定深度は前者へ不要な計算を割り当てる。

早期終了は各層の予測を監視して計算を打ち切るが、出口を増やすと学習目標も増える。全出口のlossを同時にbackboneへ流すと、浅い出口を早く良くしたい勾配と最終層の表現を良くしたい勾配が競合し得る。さらに「最大class確率が閾値を超えたらexit」のような規則は回帰には自然なconfidenceを定義できない。

## 手法

### 複数出口構造

BERxiTはTransformer各層のhidden stateへtask headを接続する。推論時には第1層から順にhidden stateと中間予測を計算し、exit条件を満たせば残りのTransformer層を実行せずその予測を返す。条件を満たさない場合だけ次層へ進み、最終層では必ず予測を返す。

この構造では平均実行層数が直接計算量の代理になる。exit閾値を厳しくすれば多くの入力が深層まで進み品質重視になり、緩くすれば浅いexitが増えて速度重視になる。重要なのは、モデル全体を1つの小型モデルへ置換するのではなく、同じモデル内で入力別に深度を変える点である。

### 交互fine-tuning

BERxiTの交互学習は、複数出口とbackboneを常に同時更新するのではなく、学習対象を切り替えて最適化する。これにより中間headを強くするためのlossが事前学習済みbackboneを過度に変形することを避け、最終出口の品質と早期出口の有用性を両立させる。

この機構が効く理由は、早期終了モデルでは「全層を使った最良予測」と「途中層でも使える予測」の二つの目標があるからである。単純なjoint trainingでは同じパラメータへ両目標が同時に作用するが、交互更新は役割を分離し、backboneの表現力を保ちながら各出口を適応させる。

### 学習型exit判定

分類では中間softmaxの最大確率やentropyをconfidenceとして使える。しかし回帰出力は単一または少数の連続値であり、「予測値が大きいほど確信が高い」とは言えない。BERxiTはこの判定自体を学習するLTE moduleを追加する。

LTEは中間表現を入力として、その層で終了することが適切かを予測する。これによりexit判定をtask outputの形式から切り離し、分類だけでなく回帰にも適用できる。追加moduleの計算費用は生じるが、残りの複数Transformer層を省略できる入力では十分小さい。

## 評価

論文はBERT、RoBERTa、ALBERTを用い、分類だけでなく回帰を含むNLPタスクで品質と効率の交換曲線を比較する。またDistilBERTとの組合せを評価し、モデル圧縮と入力適応深度が排他的ではないことを確認する。

| 観点 | BERxiTで確認する内容 |
|---|---|
| fine-tuning | 単純joint trainingに対し交互学習が品質–効率曲線を改善するか |
| exit判定 | confidence規則だけでなくLTEが分類・回帰で機能するか |
| backbone | BERTだけでなくRoBERTa、ALBERTへ一般化するか |
| 他高速化との併用 | DistilBERTへ早期終了を重ねても利得が残るか |
| 効率指標 | 平均実行層数・計算量を下げたときのtask品質 |

主要な結論は、提案fine-tuningが従来の早期終了学習より良い品質–効率交換を作り、LTEにより回帰へ早期終了を拡張できることである。固定の単一速度倍率を主張する研究ではなく、exit閾値を動かしたPareto曲線として評価する点に注意が必要である。

## なぜ効くか

BERT系encoderでは全入力が同じ深度を必要とするわけではない。浅い層で既にclassや回帰値を十分予測できる入力について、後段のself-attentionとFFNを全て省けば、その入力の計算量を直接削減できる。難しい入力は最終層まで残るので、全モデルを一律に浅くするより品質低下を制御しやすい。

一方、早期exitの価値は中間予測が十分強く、exit判定が誤らないことに依存する。BERxiTは前者を交互fine-tuning、後者をLTEで改善する。つまり新しい高速kernelを導入するのではなく、「どの入力に何層使うか」という条件付き計算を改善する研究である。

## 既存研究との差

DeeBERTなど先行方式は、中間classifierのconfidenceを使って簡単な入力を早く終了させる考え方を示した。BERxiTは早期終了そのものの発明ではなく、複数出口モデルのfine-tuning方法とexit判定方法を改善する。特に回帰への拡張は、class確率に依存するexit規則では扱いにくかった領域を広げる。

DistilBERTとの併用評価も重要である。蒸留はモデル全体を恒常的に浅くするのに対し、BERxiTは入力ごとにさらに深度を変えるため、静的圧縮と動的計算削減を重ねられる。

## 限界

中間層で正しく予測できない難しい入力が多いデータ分布では、多くの入力が最終層まで進み速度利得は小さくなる。逆にexitを積極的にしすぎると、まだ表現が成熟していない浅い層の誤予測を確定して品質が落ちる。したがって運用では品質要件に合わせたexit閾値が必要である。

また対象はencoder型BERT系列の分類・回帰が中心であり、現代のdecoder-only LLMでtokenを逐次生成するサービングとは計算構造が異なる。中間headとLTEの追加メモリ・計算もゼロではない。BERxiTの結果をそのまま生成LLMのTPOT高速化倍率として扱うことはできない。

## 一次資料

- ACL Anthology: https://aclanthology.org/2021.eacl-main.8/
- PDF: https://aclanthology.org/2021.eacl-main.8.pdf
- 公式実装: https://github.com/castorini/berxit