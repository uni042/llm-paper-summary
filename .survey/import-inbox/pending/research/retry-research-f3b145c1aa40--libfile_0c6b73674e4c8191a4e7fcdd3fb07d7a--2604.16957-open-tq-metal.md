---
canonical_id: "arXiv:2604.16957"
title: "Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon"
summary: "Open-TQ-MetalはApple Silicon上でKVキャッシュを実行時INT4量子化し、完全なdequantization行列を作らず圧縮表現のままattentionを計算するMetal kernelを実装する。Gemma 4 31BとLlama 3.1 70Bの330実験で、128K contextのattentionをdequantize-then-attend比48倍高速化し、KVを40GBから12.5GBへ圧縮、64GB Mac単体でLlama 3.1 70Bの128K推論を可能にする。"
list_summary: "INT4 KVを展開せずMetal カーネル内で直接注意機構し、Apple Siliconの長文脈LLMでKV容量とdequantization 通信量を同時に削減する。"
authors: ["Sai Vegasena"]
published: "2026-04-18"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2604.16957"
sources: ["https://arxiv.org/abs/2604.16957"]
implementation: "Apple Silicon向けcustom Metal compute shaderとしてsdpa_int4等を実装し、Gemma 4 31B/Llama 3.1 70Bで330条件を評価。確認済み一次資料から公式repository URLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2604.16957"
arxiv_categories:
  primary: "cs.LG"
  cross_list: []
worker_completed_at: "2026-10-06T20:45:00+09:00"
worker_run_key: "20261006-2000-scheduled-chat-00/r02"
reference_main_sha: "d53224842a1f044cfc1d642e6a55c7bd8d266c48"
last_audited: null
audit_version: 0
---

## 概要
長文脈推論ではKVキャッシュが巨大になり、統合メモリ容量だけでなく注意機構ごとの読出し帯域を消費する。KVをINT4化しても、注意機構前にFP16行列へ完全展開する方式では一時メモリとdequantization 通信量が残る。Open-TQ-MetalはApple SiliconのMetal compute shaderでINT4 KVを読み、その場で必要値だけ復号して注意機構積へ投入する圧縮領域融合注意機構を実装する。

Gemma 4 31BとLlama 3.1 70Bを含む330実験で、128K 文脈時のfused sdpa_int4 カーネルはdequantize-then-attend基準より48倍高速、KV容量を40GBから12.5GBへ3.2倍圧縮する。64GB 民生 Mac上でLlama 3.1 70Bの128K 文脈を実行可能にし、FP16と同一top-1 トークン 予測を報告する。

## 問題設定
Apple SiliconはCPU/GPUが統合メモリを共有するためPCIe転送は不要だが、70B級モデルと長大KVを同じ64GB空間へ置くと容量が先に限界へ達する。量子化KVを毎段階完全展開すれば、容量を節約してもメモリ 帯域とtemporary バッファで利点を失う。

またKV量子化誤差はモデル 構成で同じように効かない。論文は注意機構 scale factorがangular 量子化の誤差感度を左右し、Gemma 4のattn_scale=1.0ではLlama標準の1/sqrt(d)よりdirectional errorが25〜100倍増幅されると分析する。

## 手法
### On-the-fly INT4 KV
プリフィル/デコードで生成したKVをINT4へ量子化して保持し、長さに比例するキャッシュ容量を削減する。FP16 KVを別途常駐させないため、128K 文脈でもモデル 重みとキャッシュを64GB unified メモリへ収めやすくする。

### Fused compressed-domain attention
sdpa_int4 Metal カーネルは量子化ブロックとscaleを読み、register/tile内で必要値を復号して問い合わせとの積へ直結する。FP16 KV行列を大域 メモリへ書き戻さないため、「INT4 read → FP16 materialization → 注意機構 read」という余分な往復を除く。

### Architecture-aware quantization分析
単一量子化方式を全モデルへ同一適用するのではなく、注意機構 scalingが量子化角度誤差をスコアへどう増幅するかをGemma/Llamaで比較する。これによりPolarQuant等が構成によって成功・失敗する理由をモデル サイズではなく注意機構 scaleへ結び付ける。

## 評価条件
|項目|内容|
|---|---|
|ハードウェア|64GB 民生 Mac / Apple Silicon|
|models|Gemma 4 31B、Llama 3.1 70B|
|実験数|330|
|文脈|最大128K|
|KV precision|INT4、比較FP16/dequantize-then-attend|
|カーネル|custom Metal sdpa_int4|

## 主要結果
128K 文脈でfused sdpa_int4 注意機構はdequantize-then-attend基準比48倍高速化する。KV メモリは40GBから12.5GBへ低下し3.2倍圧縮となる。これにより既存フレームワークでは容量上困難だったLlama 3.1 70B・128Kを64GB Mac単体で動作させる。

品質については対象実験でFP16 inferenceと同一top-1 トークン 予測を報告する。ただしこれは全ベンチマーク スコアの完全同一を意味せず、トークン選択一致という評価である。構成分析ではGemma 4の注意機構 scaleがangular 量子化 errorを25〜100倍強く増幅する条件を示す。

## 既存研究との差
一般的なKV量子化は保存容量を減らしても、既存注意機構 カーネルへ渡すためFP16へ展開する場合がある。本方式は量子化表現を注意機構 カーネルの入力形式そのものにし、中間dequantization matrixを作らない。さらにApple Silicon/Metalを直接対象にし、CUDA中心のKV圧縮研究とは異なるメモリ hierarchyで実測する。

## 限界
48倍は注意機構 カーネルのdequantize-then-attend比較であり、モデル全体のエンドツーエンド generationが48倍になるという値ではない。評価ハードウェアはApple Siliconで、CUDA GPUへそのまま外挿できない。top-1一致は強い局所品質指標だが、長文QA等の全タスク品質を網羅するものではない。

## 一次資料
- https://arxiv.org/abs/2604.16957