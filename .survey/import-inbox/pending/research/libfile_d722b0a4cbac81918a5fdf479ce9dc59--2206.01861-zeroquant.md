---
canonical_id: "arXiv:2206.01861"
title: "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers"
summary: "ZeroQuantは重み・活性化の細粒度量子化、データ不要の層単位知識蒸留、量子化/逆量子化を融合する最適化バックエンドを統合した推論パイプラインである。INT8でBERT/GPT系を最大5.19倍/4.16倍高速化し、INT4/INT8混合でFP16比3分の1のメモリ使用量を報告する。"
list_summary: "細粒度INT8/INT4量子化と融合バックエンドで量子化変換のオーバーヘッドを抑え、Transformer推論を最大約5.2倍高速化する。"
authors: ["Zhewei Yao","Reza Yazdani Aminabadi","Minjia Zhang","Xiaoxia Wu","Conglong Li","Yuxiong He"]
published: "2022-06-04"
publication: "NeurIPS 2022"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2206.01861"
sources: ["https://arxiv.org/abs/2206.01861"]
implementation: "大規模Transformer向け量子化と専用推論バックエンドを統合して実機評価。公式コードURLは今回確認した一次arXivページから特定できなかった。"
code: null
last_checked: "2026-10-05"
arxiv_id: "2206.01861"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.LG"]
worker_completed_at: "2026-10-05T23:58:00+09:00"
worker_run_key: "20261005-2330-scheduled-chat-30/r01"
---

## 概要
ZeroQuantは、学習済みTransformerを再学習なしまたは低コストで低ビット化し、メモリ削減だけでなく実測推論高速化まで得ることを目的とする。重み・活性化を細粒度に量子化する方式、層単位知識蒸留（layer-by-layer knowledge distillation; LKD）、量子化と逆量子化のオーバーヘッドを消す最適化バックエンドを一体化している。

## 問題設定
低ビット量子化は重み転送量と行列積コストを減らせるが、活性化の外れ値や層ごとの感度差で精度が落ちる。また量子化/逆量子化kernelを別々に挿入すると、その変換とメモリアクセスが速度利得を食い潰す。ZeroQuantは数値誤差と実装オーバーヘッドを同時に扱う。

## 手法
重みと活性化をハードウェアで扱いやすい細粒度単位で量子化し、INT8を基本として感度の高い構成ではFFN重みをINT4、attention重みと活性化をINT8とする。精度低下が大きい層にはLKDを適用し、元の学習データを必要とせず層出力を合わせる。

システム側では量子化/逆量子化を周辺演算へ融合し、中間テンソルの追加読み書きとkernel launchを削減する。したがって「モデルサイズが小さい」だけでなく、低ビットGEMMへ実行経路をつなげて実測速度を得る。

## 評価条件
| 観点 | 内容 |
|---|---|
| モデル | BERT、GPT-3系、GPT-J 6B、GPT-NeoX 20B |
| 精度 | FP16基準、W8A8、FFN W4 + attention W8 + A8 |
| 主指標 | 推論速度、メモリ使用量、タスク精度 |

## 主要結果
| 条件 | 結果 | 読み取り |
|---|---|---|
| BERT INT8 | FP16比最大5.19倍高速 | 低ビット実行とbackend融合が効く |
| GPT-3系 INT8 | FP16比最大4.16倍高速 | 生成系でも速度利得 |
| INT4/INT8混合 | FP16比3倍のメモリ削減 | より低いweight bitで容量を圧縮 |
| GPT-J 6B / GPT-NeoX 20B | FP16相当精度で最大約5.2倍効率改善 | 大規模公開モデルへ適用可能 |

## 既存研究との差
量子化方式だけでなく、データ不要LKDと実行バックエンドを含むend-to-endパイプラインとして設計し、量子化/逆量子化の実装コストまで削った点が特徴である。

## 限界
低ビット化の許容誤差はモデル・層に依存し、INT4ではLKD等の補償が必要になる。評価世代は現在の最新LLMより小さく、現代的なattention kernelや連続バッチング環境との組合せは論文の直接評価外である。

## 一次資料
- https://arxiv.org/abs/2206.01861