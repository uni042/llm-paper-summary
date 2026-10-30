---
canonical_id: "DOI:10.1007/s44443-026-00541-9"
title: "Mitigating the impact of activation smoothing on weights: A channel permutation and smoothing-based LLMs quantization method"
summary: "CHAMP-QはW4A8量子化で、活性outlierを平滑化すると逆スケールにより重み側のgroup内分散が悪化する問題を解く。HNSはoutlierの強度に応じて対数・冪乗スケールを切り替え、MFCPは平均・分散・L2ノルムからチャネル感度を求め、類似チャネルを同一groupへ並べ替える。LLaMA-2-7BのWikiText2困惑度6.1461、5ゼロショット平均67.65%。LLaMA-1-30Bで最大1.74倍のピークメモリ削減、B=8のLLaMA-1-7Bで総遅延1.29倍短縮。B=1では7Bが1.04倍、13Bが1.08倍にとどまり、decode時間の88.62%はW4A8 GEMM以外が占める。"
list_summary: "強い活性outlierを対数スケールで抑えるHNSと、平滑化で重み側に生じるoutlierをgroup内へ集めるMFCPでW4A8精度を改善。小バッチでは実測速度利得が小さい。"
authors:
  - "Yanyao Guan"
  - "Yunhe Cui"
  - "Langtao Zhao"
  - "Guowei Shen"
  - "Yi Chen"
  - "Chun Guo"
published: "2026-03-05"
publication: "Journal of King Saud University - Computer and Information Sciences 38(6), 2026"
publication_type: "査読付きジャーナル論文"
publication_status: "published"
source: "https://link.springer.com/article/10.1007/s44443-026-00541-9"
sources:
  - "https://link.springer.com/article/10.1007/s44443-026-00541-9"
  - "https://doi.org/10.1007/s44443-026-00541-9"
implementation: "W4A8、重みgroup-wise 1024、活性dynamic per-token、Pileから512サンプル・各512トークンの校正。LLaMA-1/2とQwen2.5、T5を評価。NVIDIA A6000 48GB、PyTorch/CUDA、B=1とB=8の1,024入力＋512生成で遅延・メモリを計測。"
code: null
last_checked: "2026-10-30"
worker_id: "scheduled-chat-00"
worker_completed_at: "2026-10-30T19:04:52+09:00"
worker_run_key: "20261030-1904-scheduled-chat-00/r02"
reference_main_sha: "6b0942fd32351ae5dfc03bf3acb6727c8e398cbd"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
research_worklist_rank: 28
last_audited: null
audit_version: 0
---
# CHAMP-Q：活性平滑化が生む重みの量子化誤差をチャネル並べ替えで抑える

## 概要

LLMを4ビット重み・8ビット活性（W4A8）で動かすには、活性の巨大なoutlierを抑えつつ、4ビット重みのgroup内スケールを安定させる必要がある。SmoothQuant系の活性平滑化は、活性の大きいチャネルを小さくする代わりに、重みへ逆スケールを掛けて数学的な線形変換を保存する。この結果、活性の分布は改善しても、重みの一部のチャネルが大きくなり、group-wise量子化の誤差が増えることがある。

CHAMP-Qは、**HNS（Hybrid Numerical Smoothing）**で強い活性outlierと通常のoutlierを別々の規則で平滑化し、**MFCP（Multi-dimensional Feature-aware Channel Permutation）**で平滑化後の重みチャネルを似た分布ごとに並べ、同じ量子化groupへまとめる。LLaMA-2-7BではWikiText2困惑度6.1461、ゼロショット5タスク平均67.65%を得た。LLaMA-1-30Bではピークメモリを最大1.74倍削減する一方、B=1の7B/13Bでの速度比は1.04/1.08倍と小さい。B=8の7Bではprefill1.22倍、decode1.46倍、全体1.29倍の高速化となる。モデル容量の削減と推論時間の削減は同じ比率ではない。

## 問題設定

W4A8の活性量子化では、最大値の大きい少数チャネルが量子化スケールを支配する。活性値をs_jで割り、対応する重みチャネルをs_j倍する平滑化はFP演算では等価でも、重みを4ビットに丸めると元の値を再現できない。group-wise量子化では同一group内の最大値がスケールを決めるため、異なる大きさのチャネルが混ざると小さな重みの分解能が落ちる。著者らはこれを活性平滑化が生む「重み側の新しいoutlier」と捉える。

一方、outlierの強度が極端に大きいチャネルでは、通常の冪乗型平滑化だけでは十分に抑えられない。強いoutlierへ大きなs_jを使うと、今度は重み側の値がさらに増幅される。この二つの誤差源を一つの固定スケールで扱うのではなく、活性側の平滑化と重みgroupの配置を別々に最適化するのが研究の出発点である。

## 手法

### 1. HNS：outlier強度によってスケールの計算を切り替える

校正サンプルをモデルへ通し、各線形層入力のチャネルごとの最大活性値act_max,jを集計する。チャネル分布から百分位閾値V_sigを求め、それを超える強いoutlierチャネルと、通常のoutlierチャネルを分ける。論文の標準設定はv_sig=1%で、LLaMA-2-7Bの感度評価では0.5～1.2%付近の困惑度が低く、0.1%の極端な設定は不利だった。

強いoutlierには対数領域に基づく平滑化スケールを使い、極端な活性の影響を圧縮する。通常のoutlierには、活性と重みの最大値をともに考慮する冪乗型スケールを使う。前者は強い活性値の抑制を優先し、後者は活性と重みの量子化難度を釣り合わせる。標準の冪乗係数αは0.5。v_sigやαは小さな候補集合で自動調整する選択肢も示されるが、追加校正が必要となる。

計算したスケールは、線形層の直前にある正規化層の重みと、後続の線形層の重みに相反する係数として吸収する。これによりFP計算では元の線形変換を保ち、推論時に明示的な活性平滑化カーネルを毎回走らせる必要を減らす。**対数変換で活性そのものを非線形に書き換えるのではなく、outlierの強度に応じた平滑化係数の選択が中心**である。

### 2. MFCP：平滑化後の重みチャネルを似たgroupへ並べる

HNSで活性outlierを抑えた後、重みの各入力チャネルについて平均、分散、L2ノルムを抽出する。三つの特徴を正規化し、重み係数λ1・λ2・λ3で合成してチャネルごとの量子化感度を得る。標準値は(1,1,1)。感度が近いチャネルを隣接させる順序へ並べ替え、group-wise量子化の同じgroupに類似分布の重みが入るようにする。

並べ替えに合わせて入力活性のチャネル順も一致させるため、FP計算の線形変換は保存できる。group内の最大値・分散が小さくなれば、同じ4ビット幅でも小さな重みをより細かく表現できる。MFCPは重みの量子化誤差を下げるための配置最適化であり、単に重みをソートして圧縮率を上げる方式ではない。

一部の層では推論時に活性チャネルのpermutationが必要となり、追加のカーネル処理が生じる。論文のB=8のdecodeプロファイルではこの処理は0.4424ms/token、時間比0.41%と小さいが、ゼロではない。チャネル順序の変更が他の演算やfused kernelへ及ぼす実装上の影響は無視できない。

### 3. W4A8の実装と校正条件

重みは4ビット、活性は8ビットで量子化する。重みは標準でgroup size 1024、活性はdynamic per-tokenを使い、対称量子化でINT8 GEMMへ渡す。実装ではINT4重みを計算に適した表現へ変換・逆量子化し、活性INT8と組み合わせてINT32の積和を行い、最終出力をFP16へ戻す。低ビット重みを格納しても、演算中の一時変換とスケール適用が必要であり、メモリ容量の削減率とカーネル速度は別問題である。

校正にはPileからランダムに抽出した512サンプルを使い、各サンプルを512トークンに揃える。SmoothQuant、OutlierSuppression+、AWQ、QuaRotを同じW4A8設定で再現し、SpinQuantは学習型回転の設定を合わせて別途比較する。SpinQuantの回転学習はLLaMA-2-7Bだけでも同論文のハードウェアで20時間超を要し、CHAMP-Qの学習不要という特徴は校正・導入コストの比較に現れる。

## 評価条件

| 項目 | 一次論文での設定 |
|---|---|
| モデル | LLaMA-1/2の7B・13B・30B等、追加検証にQwen2.5-3B/7B、T5系列 |
| 量子化 | W4A8、重みgroup-wise 1024、活性dynamic per-token、対称量子化。SpinQuant比較ではgroup size 128を揃える |
| 校正 | Pileから512サンプル、各512トークン。HNSのv_sig=1%、α=0.5、MFCP係数(1,1,1) |
| 精度 | WikiText2困惑度、PIQA・ARC・HellaSwag・WinoGrande等のゼロショット平均。T5ではRTE/SQuAD/CNN-DailyMail等も追加 |
| 計算環境 | NVIDIA A6000 48GB、PyTorch/CUDA。B=1またはB=8 |
| 遅延 | 入力1024トークン＋生成512トークン、prefill・decode・全体遅延、GPUピークメモリ |
| 比較 | FP16、SQ、OS+、AWQ、QuaRot、SpinQuant、HNSのみ、MFCPを外した構成、group size感度 |

主な数値は論文本文§5のTable 1～12およびFig.5～7に基づく。B=1の速度とB=8の速度を同じバッチ条件として混ぜない。特に、SpinQuantとの比較は学習済み回転の校正コストが大きく異なる。

## 評価結果

### W4A8の品質

| 比較条件 | 値 | 読み取れること |
|---|---:|---|
| LLaMA-2-7B・CHAMP-QのWikiText2困惑度 | 6.1461 | 論文Table 1の主結果 |
| LLaMA-2-7B・CHAMP-Qの5タスク平均正解率 | 67.65% | 同じW4A8条件でSQ/OS+/AWQ/QuaRotより高いと報告 |
| LLaMA-2-7B/13B・SpinQuant比較 | SpinQuantが平均約1.0～1.5ポイント上回る | CHAMP-Qは全方式に一律に勝つわけではない |
| LLaMA-2-7B・HNSのみ、group size 128 | 平均正解率67.84% | OS+が約0.02ポイント上回る例がある |
| LLaMA-2-7B・HNSのみ、group size 512 | 平均正解率67.76%、困惑度6.0740 | group変更下でもHNSが良好 |
| LLaMA-2-7B・HNSのみ、group size 1024 | 平均正解率66.96%、困惑度6.2183 | groupを粗くすると品質が変わる |

Table 1・2・11。CHAMP-Qは学習不要のW4A8で高い精度を示すが、学習を使うSpinQuantの方が精度で有利な条件がある。HNS単独でも細かいgroupではOS+がわずかに上回り、MFCPとの併用によってgroup内重み分布を改善する必要性がある。LLaMA-2-7Bの主結果は複数タスクの平均であり、全個別タスクの勝利を意味しない。

### メモリと速度：バッチサイズが重要

| 測定 | CHAMP-Qの結果 | 比較条件 |
|---|---:|---|
| LLaMA-1-30Bのピークメモリ | 最大1.74倍削減 | B=1、入力1024・生成512 |
| LLaMA-1-7Bの全体速度 | 1.04倍 | B=1、同系列長 |
| LLaMA-1-13Bの全体速度 | 1.08倍 | B=1、同系列長 |
| LLaMA-1-7Bのprefill速度 | 1.22倍 | B=8、入力1024 |
| LLaMA-1-7Bのdecode速度 | 1.46倍 | B=8、生成512 |
| LLaMA-1-7Bの全体速度 | 1.29倍 | B=8、入力1024・生成512 |

論文Table 3・4。大きいモデルでは重み容量削減がピークメモリへ効くが、小バッチではW4A8カーネル以外の処理が遅延を支配し、1.04～1.08倍程度の速度改善にとどまる。B=8では線形層の演算をまとめやすくなり、decodeが1.46倍、全体が1.29倍になる。abstractの最大1.45倍前後という数字は、全てのモデル・バッチで得られた速度比ではない。

### decodeプロファイルとアブレーション

| B=8・decode GPU時間の内訳 | 割合 |
|---|---:|
| MFCPのオンラインpermutation | 0.41%（0.4424ms/token） |
| dynamic per-token活性量子化 | 4.57% |
| W4A8 GEMM | 6.39% |
| その他（attention、softmax、正規化、制御など） | 88.62% |

論文Table 5。GEMMを高速化しても、その他の処理が88.62%残る条件では、システム全体の速度改善には上限がある。著者らはpermutationと活性量子化をW4A8 GEMMへ融合し、カーネル起動やグローバルメモリ転送を減らすことを将来課題に挙げる。

MFCP係数(λ1,λ2,λ3)の感度評価では、(2,1,1)、(1,2,1)、(1,1,2)のような小さな変更でも基準順序とのSpearman相関は0.99以上、WikiText2困惑度は6.14～6.15に収まった（Table 7）。一方、v_sigを0.1%にすると困惑度が悪化し、0.5～1.2%付近で最小となる（Fig.6）。MFCPを外すと平均精度が約1～3ポイント低下し、さらにHNSも外すと悪化する（Table 8）。この結果は、チャネル順序だけでもoutlier平滑化だけでも十分でないことを示す。

Qwen2.5-3BではQuaRotが重み共有（tie_word_embeddings=true）の影響を受けやすく、CHAMP-Qはこの回転に依存しないため良好だった。T5-small/base/largeでも概ねFP16に近いが、T5-3Bでは一部タスクで量子化による品質低下が目立つ。モデル構造・サイズによって効果は変わる。

## 既存研究との差

SmoothQuantは活性outlierを重みへ移すことでINT8活性量子化を容易にするが、重みを4ビットへ落とすと逆スケールで増えたgroup内outlierが問題になる。CHAMP-Qは活性側にHNS、重み側にMFCPを置き、二つの誤差を連続して抑える。QuaRotやSpinQuantのような回転方式とは異なり、チャネルの分布特徴に基づく並べ替えを用い、学習済み回転を必要としない。単にper-channel量子化を細かくするのではなく、group size 1024でも品質を維持する設計が特徴である。

## 限界

第一に、B=1では7Bが1.04倍、13Bが1.08倍しか速くならず、W4A8の容量削減がそのまま速度へ転換されない。decode時間の大半はGEMM以外の処理で、permutation・活性量子化の追加処理も存在する。異なるGPUやバッチでの速度改善を保証するものではない。

第二に、HNSの閾値v_sigは校正分布へ依存し、0.1%など極端な値では性能が悪化する。MFCPは活性チャネルも対応して並べ替える必要があり、特定の融合カーネルやモデルのweight tyingとの整合性を実装で確保しなければならない。

第三に、SpinQuantの方がLLaMA-2で平均精度を1.0～1.5ポイント上回る条件があり、CHAMP-Qが最高精度の唯一の方式ではない。SpinQuantは20時間超の回転学習コストを伴うため、校正時間と精度を別々に評価する必要がある。

第四に、主な精度評価はWikiText2と短いゼロショットタスクであり、長文脈、数十万トークン、複数要求の連続バッチ、MoEのexpertごとのoutlier、量子化されたKVキャッシュとの併用は十分に検証されていない。T5-3Bでの一部タスクの悪化は、他アーキテクチャへ無条件に適用できないことを示す。

## 一次資料

- https://link.springer.com/article/10.1007/s44443-026-00541-9 （§4のHNS/MFCP、§5のTable 1～12、実測速度とアブレーション、付録の誤差上界）
- https://doi.org/10.1007/s44443-026-00541-9 （2026-03-05オンライン公開、正式書誌）
