---
canonical_id: "arXiv:2202.08791"
title: "cosFormer: Rethinking Softmax in Attention"
summary: "cosFormerはsoftmax attentionの非負性と近いtokenを強調する再重み付けを、ReLU特徴写像とcosine距離再重み付けで置き換える線形attentionである。attention行列を明示的に作らず結合順序を変えて系列長に対する計算・memoryを線形化し、Long-Range Arenaで当時の線形Transformer系SOTAを達成する。"
list_summary: "ReLUによる非負特徴とcosine距離重みを使う分解可能注意機構で、softmaxを使わず長系列注意機構を線形時間・メモリへ変換する。"
authors: ["Zhen Qin","Weixuan Sun","Hui Deng","Dongxu Li","Yunshen Wei","Baohong Lv","Junjie Yan","Lingpeng Kong","Yiran Zhong"]
published: "2022-02-17"
publication: "ICLR 2022"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2202.08791"
sources: ["https://arxiv.org/abs/2202.08791"]
implementation: "language modeling、machine translation、Long-Range Arena等でsoftmax Transformerと線形attention baselineを比較。公式OpenNLPLabコードを公開。"
code: "https://github.com/OpenNLPLab/cosFormer"
last_checked: "2026-10-06"
arxiv_id: "2202.08791"
arxiv_categories: {primary: "cs.CL", cross_list: []}
worker_completed_at: "2026-10-06T15:48:00+09:00"
worker_run_key: "20261006-1530-scheduled-chat-30/r01"
reference_main_sha: "0bbe57b3f448170074d516761dd9f8c955981e5e"
last_audited: null
audit_version: 0
---
## 概要
softmax 注意機構は問い合わせ-key全組合せのスコアを作るため系列長Nに対してO(N²)の計算とメモリを要する。カーネル feature mapで注意機構を分解すればKとVを先に集約できるが、単純近似ではsoftmax特有の「正の重み」と「重要位置へ集中する分布」を失い品質が落ちる。cosFormerはこの二性質を明示的に再構成する。

## 手法
問い合わせとkeyへReLUを適用して特徴を非負にする。これにより注意機構 重みも非負となり、softmaxの第一の性質を満たす。

次に問い合わせ位置iとkey位置jの距離に応じたcosine係数を掛ける。近いトークンほど大きく、離れるほど小さくなるよう再重み付けし、softmaxが作る尖った分布の代替とする。このcosine項は三角関数の積和公式で問い合わせ側特徴とkey側特徴へ分解できるため、N×N 注意機構 matrixを作る必要がない。

分解後はKとVの集約を先に行い、その結果へ各Qを掛ける。通常注意機構のO(N²d)に対して系列長方向をO(Nd²)へ変え、注意機構 matrixのO(N²) メモリも避ける。causal 注意機構では接頭辞累積和を使い未来トークンを見ないようにする。

## 評価条件
|項目|内容|
|---|---|
|タスク|language modeling、machine translation、Long-Range Arena|
|比較|vanilla softmax Transformer、Linear Transformer、Performer等|
|注意機構|causal / cross 注意機構双方|
|指標|パープレキシティ、BLEU、LRA accuracy、speed/メモリ scaling|
|実装|公式PyTorchコード公開|

## 主要結果
language modelingとテキスト understandingでvanilla Transformerと同等またはそれ以上の品質を示し、Long-Range Arenaでは当時の線形Transformer系で状態-of-the-artを報告する。つまり計算量を線形化するだけでなく、softmax近似で起こりがちな品質低下を抑えることが主結果である。

系列長が伸びるほど二乗注意機構との差が大きくなり、メモリ使用量と実行時間のscalingが改善する。一方、短い系列ではカーネル オーバーヘッドの比率が高く、理論計算量の差ほど実時間差が出ない。

## 既存研究との差
Performer等がsoftmax カーネルをrandom featureで近似するのに対し、cosFormerはsoftmaxそのものの近似精度を追うのではなく、非負性と局所的な注意機構集中という二つの性質を決定的なfeature mapで再現する。random feature samplingを必要としない。

## 限界
cosine距離重みは位置差に基づく固定priorなので、遠距離トークンが重要なタスクではsoftmaxのcontent-dependentな集中を完全には再現できない。評価は現代の数十B パラメータ decoder-only LLM 推論提供ではなく、比較的小規模Transformerを中心とするため、FlashAttention世代のカーネルとの実機差は別途検証が必要である。