---
canonical_id: "arXiv:2502.18137"
title: "SpargeAttn: Accurate Sparse Attention Accelerating Any Model Inference"
summary: "注意行列の疎性を入力ごとに二段階で検出し、不要なQKおよびPVブロック計算を省略する学習不要の汎用疎注意。選択的token圧縮によるblock予測とsoftmax-awareなonline filterをFlashAttention型実装へ統合し、言語・画像・動画生成で品質を保ちながら実推論を高速化する。"
list_summary: "二段階オンラインフィルタで注意blockを動的に省略し、学習なしで言語・画像・動画モデルの注意計算を高速化する汎用疎注意。"
authors: [Jintao Zhang, Chendong Xiang, Haofeng Huang, Jia Wei, Haocheng Xi, Jun Zhu, Jianfei Chen]
published: "2025-02-25"
publication: "ICML 2025"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2502.18137"
sources: ["https://arxiv.org/abs/2502.18137", "https://github.com/thu-ml/SpargeAttn"]
implementation: "FlashAttention型のblock処理へ二段階filterを統合し、言語・画像・動画生成モデルで実測。公式実装はCUDA/Tritonを公開している。"
code: "https://github.com/thu-ml/SpargeAttn"
last_checked: "2026-10-06"
arxiv_id: "2502.18137"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.AI", "cs.CV"]
worker_completed_at: "2026-10-06T01:51:00+09:00"
worker_run_key: "20261006-0100-scheduled-chat-00/r02"
---

## 概要

SpargeAttnは、注意行列には実際にはほとんど寄与しない要素が多いという疎性を利用し、入力ごとに不要な行列積blockを見つけて計算しない学習不要の注意実装である。固定窓など特定の疎patternを仮定せず、言語、画像、動画で異なるattention patternをオンラインに推定することを狙う。第一段階で安価な近似attention mapから候補blockを絞り、第二段階ではonline softmaxの途中で寄与が十分小さいblockをさらに捨てる。

論文は既存のdense/sparse attention実装に対して条件により2.5～5倍級の注意処理高速化を示し、画像・動画・言語のend-to-end指標を維持する。量子化注意SageAttentionとも直交的に組み合わせられるため、「計算するblock数」と「一blockあたりの演算費」を別々に減らせる。

## 問題設定

標準注意ではQK^Tを作りsoftmax後にVと積を取る。系列長が増えると候補token対が二乗で増えるが、softmax後のattention weightは一様ではなく、多くの位置がほぼゼロになる。最終出力へほとんど寄与しないblockまでdense GEMMで計算すると、長文脈や高解像度動画で大きな無駄になる。

しかし疎patternはモデルや入力で変わる。言語の局所性、画像の空間局所性、動画の時空間構造へ個別の固定patternを作ると汎用性が低い。一方、正確なattention mapを先に全部計算してから小さい要素を捨てても高速化にならない。必要なのは、本計算より十分安価に「計算しなくてよいblock」を予測し、誤って重要blockを落とさない仕組みである。

## 手法

### 第一段階: 選択的token圧縮によるblock予測

QとKをblockへ分け、各block内部のtoken表現がどれだけ似ているかを平均cosine similarityで測る。自己類似度が高いblockではtokenを平均して代表表現へ圧縮してもattention傾向を近似しやすい。逆に類似度が低いblockは圧縮近似が危険なので、保守的に本計算へ残す。

圧縮したQ/Kから低費用の近似attention mapを作り、行ごとの累積確率が閾値へ達するよう重要blockを選ぶ。これが第一段階のmaskになる。近似が信用できない低自己類似blockを強制的に残すことで、速度のために重要な不規則patternを消す危険を抑える。

### 第二段階: softmax-aware filter

第一段階を通過したblockでも、online softmaxを進めると「現在までのglobal maximumに比べて、このblockのlocal maximumが十分小さい」場合がある。指数関数を通すsoftmaxではmaxとの差が大きい値の寄与は急速に小さくなる。

SpargeAttnはこの情報をFlashAttention型のonline softmax処理中に利用し、寄与が無視できるblockについて後続の行列積を省略する。softmax計算で既に得られる最大値を使うため、別の大きな予測kernelを追加せず第二段階の疎化を行える。

### 量子化との統合

疎化は「何個のblockを計算するか」を減らす。SageAttention等の量子化は「残したblockを何bitで計算するか」を軽くする。二つは作用点が異なるため併用でき、SpargeAttn+Sage系の実装では疎化と低bit attentionを組み合わせる。

視覚tokenではHilbert curveのように空間近傍を一次元順序でも近くする並べ替えを使うことで、block内自己類似度を高め、第一段階の圧縮予測を効きやすくする選択肢も示される。

## 評価条件

| 観点 | 内容 |
|---|---|
| 対象 | 言語、画像生成、動画生成の複数モデル |
| 比較 | dense attention、MInference、FlexPrefill等 |
| 実装 | CUDA/Triton、FlashAttention型block処理 |
| 品質 | 各モデルのend-to-end task指標 |
| 効率 | attention kernel速度、end-to-end生成速度、疎率 |
| 追加 | SageAttention系量子化との併用 |

## 主要結果

多様なモデルで注意計算を大きく削減し、条件によって既存dense/sparse attention方式より2.5～5倍級の高速化を示す。動画生成の例ではFull Attentionと近い視覚品質を維持しながら実生成を高速化する。長文脈言語taskでもfull attentionに近い指標を保ち、特定patternだけに最適化した方式より汎用性を示す。

重要なのは、FLOPsの理論削減だけでなく実kernelでblockをskipする点である。一方、2.5～5倍という値はattention処理の条件依存の値であり、FFNや画像decoder等を含む全applicationが同倍率で高速になることを意味しない。疎率が低い入力ではfilter費用に対する利得も小さくなる。

## 既存研究との差

固定窓や特定モデル向けの疎attentionはpatternが合う場合に強いが、別modalや別architectureへ移すと品質を崩しやすい。SpargeAttnは入力表現の自己類似性からオンラインにblockを予測し、さらにsoftmaxの数値状態を使って第二段階でskipするため、事前に一つの疎patternを固定しない。

MInferenceやFlexPrefillのような長文脈LLM向け方式に対し、画像・動画まで同じ基本operatorを適用することを狙う。また学習不要なので既存checkpointを変更せず導入できる。

## 限界

第一段階の予測とmask作成には追加計算が必要で、元attentionが十分短い場合や疎性が弱い場合は利得が小さい。閾値を攻め過ぎれば重要blockを落とし品質を損なうため、速度と近似誤差の交換条件は残る。GPU世代、block size、CUDA実装に性能が依存し、論文のkernel倍率を別hardwareへそのまま外挿できない。

## 一次資料

- https://arxiv.org/abs/2502.18137
- https://github.com/thu-ml/SpargeAttn