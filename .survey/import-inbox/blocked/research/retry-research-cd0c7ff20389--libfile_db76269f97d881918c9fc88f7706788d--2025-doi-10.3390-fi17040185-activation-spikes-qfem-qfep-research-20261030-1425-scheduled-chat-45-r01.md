---
canonical_id: "DOI:10.3390/fi17040185"
arxiv_id: "2405.14428"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.LG"]
title: "Mitigating Quantization Errors Due to Activation Spikes in Gated Linear Unit-Based Large Language Models"
summary: "SwiGLU等のGLU型FFNでは、特定層のdown projection入力にごく少数トークン由来の巨大なactivation spikeが現れ、per-tensor量子化のscaleを支配する。QFeMはmax/median比の大きい線形moduleをactivation量子化対象から外し、QFePはspikeを誘発する短いprefixをFP16で事前計算してKVを再利用する。LLaMA-2でW8A8精度を7〜16%改善、13Bで遅延最大10.4%削減と報告。ただし非量子化moduleのコスト、Gemmaでの不完全な回復、固定prefixの文脈依存性が残る。"
list_summary: "GLU FFNの少数トークン由来activation spikeをQFeMの部分非量子化とQFePの事前prefix KVで回避し、W8A8の精度と遅延を改善。"
authors:
  - "Jaewoo Yang"
  - "Hayun Kim"
  - "Junyung Ji"
  - "Younghoon Kim"
published: "2025-04-21"
publication: "Future Internet 17(4), 185 (2025)"
publication_type: "journal"
publication_status: "published"
source: "https://doi.org/10.3390/fi17040185"
sources:
  - "https://www.mdpi.com/1999-5903/17/4/185"
  - "https://arxiv.org/abs/2405.14428"
implementation: "PyTorch 2.2/Transformers 4.38.1。C4の512校正サンプルでmodule別のactivation max/median比を測り、QFeMでは高比率moduleをW8A16相当で実行。QFePでは最初にspikeを生む短いprefixを非量子化計算し、そのKVを再利用。"
code: "https://github.com/onnoo/activation-spikes"
last_checked: "2026-10-30"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-30T14:23:00+09:00"
worker_run_key: "20261030-1408-scheduled-chat-45/r01"
reference_main_sha: "8a4c43d4d90ff181c263ce52251dd48734928dda"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
research_job_source: "WORKLIST-45.md rank 36"
last_audited: null
audit_version: 0
---
# Activation spikes：GLU型LLMの活性化量子化を阻害する局所スパイクと二つの回避策

## 概要

W8A8などの重み・活性化同時量子化は、INT8の行列積を使える一方、scaleの推定に少数の異常に大きい活性化値が混入すると、通常トークンに割り当てられる有効な量子化段階が粗くなる。Yangらは、この問題を一般的な外れ値と区別して**activation spike**と呼び、SwiGLU/GeGLUを採用するLLMのFFN内に、モデル層とトークン位置に依存する極端な入力活性化が発生することを示した。

提案するQFeM（Quantization-free Module）は、spikeが強い線形moduleだけ活性化をFP16で扱い、他の大部分のmoduleでは量子化の速度・メモリ上の利益を残す。QFeP（Quantization-free Prefix）は、spikeが最初の特定トークンで発生する性質を利用し、spikeを起こす短いprefixを事前に非量子化実行してKVキャッシュへ格納する。両者は独立に適用でき、同時利用も可能である。狙いは量子化対象全体のbit数を上げることではなく、局所的なspikeがscale推定を壊す原因だけを取り除くことである。

## 問題設定とspikeの観測

Pre-LN型Transformerでは、block入力の隠れ状態が正規化されても、GLU型FFN内部の`up`/`gate`出力の要素積から生じる`down` projectionの入力が必ず小さくなるわけではない。著者は`query`、`out`、`up`、`down`などの線形moduleの**入力活性化**を個別に観測し、隠れ状態そのものの外れ値と混同しない。C4から512サンプルを採り、module・層・トークンごとの絶対最大値に基づくscaleを測定した。

Figure 1ではGLUを使うモデルの初期層・終盤層にあるFFNの`down`入力で突出したscaleが生じる。Figure 2ではBOS、改行、アポストロフィなど少数のトークンがspikeを誘発し、同じトークンが再登場したときには初回ほど大きなspikeが生じない場合を示す。つまりspikeはトークン種だけでなく**最初の出現位置と文脈**に依存する。per-tensor量子化では最大値が全体のscaleを決めるため、通常トークンの値が粗い離散段階に丸められる。per-token量子化はこの問題を緩和し得るが、scaleの粒度を細かくする分、実装と実行コストが増える。

Table 1では、トークンごとのscaleの最大値と中央値の比が大きいmodule上位4個だけを活性化量子化したときに、perplexityと最終隠れ状態のMSEが大きく悪化した。一方、比率が中位・下位のmodule4個を量子化した場合は悪化が小さい。これは量子化誤差がすべての層に均一に広がるのではなく、少数の高感度moduleに集中することを裏付ける。

## 手法

### QFeM：module単位で活性化量子化を回避する

校正入力を用いてmodule mのトークン別入力scale集合をS_mとし、`r_m = max(S_m)/median(S_m)`を計算する。r_mが大きいmoduleほど、一部トークンのspikeが通常トークンの量子化scaleを支配している。閾値αを超えるmodule集合M_unqについては活性化をINT8化せずFP16で処理し、それ以外は通常のW8A8を適用する。対象moduleの重みはINT8のまま保持し、演算時にFP16へ戻すため、対象moduleの実行は実質的にW8A16相当になる。重みも含めてすべてFP16へ戻すという意味ではない。

αを下げれば非量子化moduleが増えて精度は保ちやすいが、INT8行列積の利益は減る。αを上げればINT8の適用範囲は広がるが、spikeによる誤差が再発する。著者は校正集合上のperplexityとmodule数を見ながら二分探索で閾値を決める。Figure 4のLLaMA-2-13B例では二つの性能曲線の交点付近としてαがおよそ16になるが、これは全モデルに共通する普遍定数ではない。MoEのMixtralではexpertごとに校正する必要があるため、expert分布の偏りを無視して一律のmodule選択を行わない。

### QFeP：初回spikeをprefixに隔離してKVを再利用する

QFePは、BOSなどspikeを起こすトークンの最初の出現を、実ユーザー入力より前の固定短文prefixへ移す。prefix部分だけをFP16で事前実行し、そのKVを保存して、後続の通常入力は量子化したモデルで処理する。既にprefixでspikeを生じさせたため、後続で同じトークンが現れてもspikeが弱まり、通常入力のper-tensor scaleを過度に大きくしにくい。論文の実験ではBOS、文脈トークン、spike誘発トークンを含む**3トークン程度のprefix**を使う。

これは通常のprompt engineeringでモデルに新しい指示を与えることとは異なる。prefixのKVを再利用し、問題となる高精度計算を一度に隔離するための推論経路上の処理である。ただしprefixの位置をKVに保持する以上、利用可能なコンテキスト長をわずかに消費し、モデル・tokenizerごとにspike誘発トークンの探索が必要になる。QFeMとQFePは異なる原因への対処なので併用できるが、両方の費用が常にゼロになるわけではない。

## 評価条件と比較対象

| 項目 | 一次論文の記載 |
|---|---|
| モデル | LLaMA-2 7B/13B/70B、LLaMA-3、Mistral-7B、Mixtral-8x7B、SOLAR-10.7B、Gemma-7B等のGLU型LLM |
| GPU | 小型モデルはRTX 4090、大型はA100。Python 3.10、PyTorch 2.2、Transformers 4.38.1 |
| 校正 | C4の512サンプル。module別・token別scaleを観測し、QFeMの閾値やQFePのprefixを事前選択 |
| 基本量子化 | 重みper-channel、活性化dynamic per-tensor、対称INT8。per-token、static per-tensor、W6A6/W4A4も比較 |
| 精度評価 | WikiText-2 perplexity、PIQA・LAMBADA・HellaSwag・WinoGrandeのzero-shot accuracy |
| 比較 | FP16、素のW8A8、per-token activation quantization、SmoothQuant、OutlierSuppressionPlus、QFeM、QFeP、併用 |
| 速度・メモリ | Figure 7で固定長列の推論遅延対精度、Table 5で1K/2Kトークンの最大メモリ使用量 |

## 定量結果と負の結果

| 出典・条件 | 観測値 | 注意点 |
|---|---|---|
| 論文結論、LLaMA-2 | QFeM/QFePにより素の量子化比でzero-shot accuracyが約7〜16%改善 | これはモデル・量子化条件に依存する範囲。全LLMで一律の絶対accuracy上昇ではない |
| 論文結論、LLaMA-2-13B | perplexityが最大85.4%減少、QFeMで推論遅延最大10.4%削減 | 量子化baselineとの比較であり、FP16比の10.4%高速化と同一ではない |
| 論文結論、LLaMA-2-7B | perplexityが50%以上改善、QFePの2Kトークン時の追加メモリは0.05%未満 | prefixの3トークンKVの追加量であり、他のバッチサイズ・モデルでの割合は変わる |
| Appendix E、7B、BMM非量子化/量子化 | W8A8 62.08% / 61.66%、+QFeP 68.69% / 68.30% | BMMを量子化するとわずかに低下。spike対策で全誤差が消えるわけではない |
| Appendix E、13B、BMM非量子化/量子化 | W8A8 55.29% / 55.43%、+QFeP 69.91% / 69.77% | BMM量子化による差は小さい。QFePの改善幅とBMM効果を区別 |
| Appendix E、70B、BMM非量子化/量子化 | W8A8 66.87% / 66.75%、+QFeP 72.62% / 72.69% | BMM量子化後もQFePの効果が残る例 |
| Figure 5、Gemma | QFeM/QFePを用いても他のSwiGLUモデルほどFP16水準へ戻らない | GeGLU採用の違いが一因と著者は推測。完全回復は保証されない |
| Figure 5、Mixtral | 素のW8A8でもspike由来の性能低下が比較的小さい | expertへトークンが分散するためとの著者の説明。MoEすべてが同じとは限らない |
| Figure 7、static per-tensor | 速度面では最も速いが精度が大きく悪化 | QFeM/QFePだけではstatic量子化の残る問題を完全には解決できない |

QFeMは一部moduleのactivationをFP16のまま処理するので、モデル容量と推論時間の節約率が「全module INT8」より小さくなることがある。Table 5では7BのQFeMメモリはAQ2に近い一方、70Bの1K条件では追加メモリを要した。QFePもKVを事前保持するので、追加メモリが厳密にゼロではない。Figure 7の動的per-token（AQ1）は精度を保ちやすいが、coarse-grained方式（AQ2/AQ3）の方が速い条件がある。QFeMでAQ2の精度をAQ1へ近づけつつ高速化するのが主眼であり、すべての指標で全比較方式を支配するとは主張できない。

## 限界・実装上の論点

第一に、spikeの発生位置とトークンはモデル・tokenizer・GLUの種類に依存する。QFePは固定prefixを使うので、BOSや改行などの初回出現が既知であることを利用するが、入力文脈やモデル更新によって別のspikeが生じる可能性がある。prefixは元のユーザー入力より前に入るため、位置埋め込みやsystem promptとの相互作用も実装で確認すべきである。

第二に、QFeMは高感度moduleをFP16演算へ戻すトレードオフを持つ。αの選択には校正perplexityが必要で、完全に校正不要ではない。MoEではexpert別の活性化分布が異なり、expertごとの観測・閾値決定が必要になる。特に12GB級GPUでの導入可否を判断する際は、重みINT8保存量だけでなく、W8A16経路の一時活性化、KVキャッシュ、バッチサイズ、実行カーネルのサポートを合算する必要がある。

第三に、量子化誤差の原因はspikeだけではない。GemmaのGeGLUで回復が不完全であること、static per-tensor方式では大きな精度劣化が残ること、7BのBMM量子化で小さな性能低下が残ることがその証拠である。SmoothQuant等の外れ値緩和と組み合わせても、すべてのモデル・低bit条件でFP16と同じ性能を保証するわけではない。

第四に、評価の遅延値は固定列長や特定GPUでの比較であり、実運用の同時リクエスト、prefill/decode分離、長文KV再利用、スループットとtail latencyの関係を包括的に測ったものではない。推論速度最大10.4%改善という結果を、全モデル・全負荷条件へ外挿してはならない。

本論文は、activation quantizationの**局所的なspikeを避ける設計**として、SmoothQuant、OutlierSuppressionPlus、IntactKV、prefixing attention sinksと関連する。特にQFePはKVキャッシュをメモリ圧縮のためではなく、非量子化prefixの計算結果を再利用するために用いる点が異なる。低bit化で速度が落ちる、あるいは量子化品質が崩れる原因の切り分けに有用である。

## 一次資料・書誌の照合

- [Future Internet 17(4), 185、DOI:10.3390/fi17040185](https://www.mdpi.com/1999-5903/17/4/185)：2025-04-21、著者4名、本文§3〜5、Table 1〜5、Appendix A〜E、結論の数値を確認。
- [arXiv:2405.14428](https://arxiv.org/abs/2405.14428)：2024年の先行版は題名が短く著者が3名。DOI正式版と同一研究系列だが、書誌・評価の正本は正式出版版を採用。
- [著者実装](https://github.com/onnoo/activation-spikes)：QFeM/QFePの実装・再現用リポジトリ。
