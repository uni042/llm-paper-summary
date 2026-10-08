---
canonical_id: arXiv:2603.05451
title: "FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling"
summary: "FlashAttention-4は、Blackwell世代でTensor Coreだけが大幅に高速化し、共有メモリ帯域と指数演算器が相対的な律速へ移ったことに合わせて注意カーネルを再設計する。非同期MMAとTensor Memoryを使うパイプライン、FMAによる指数関数の一部代替、条件付きsoftmax再スケーリング、2-CTA MMAを組み合わせ、B200・BF16でcuDNN 9.13比最大1.3倍、Triton比最大2.7倍、最大1613 TFLOPs/sを報告する。"
list_summary: "Blackwellの非対称な資源性能に合わせ、非同期MMA・指数演算分散・2-CTA MMAで注意カーネルを再設計し、B200で最大1613 TFLOPs/sを達成。"
authors:
  - Ted Zadouri
  - Markus Hoehnerbach
  - Jay Shah
  - Timmy Liu
  - Vijay Thakkar
  - Tri Dao
published: "2026-03-05"
publication: arXiv
publication_type: プレプリント
publication_status: arXiv preprint
source: https://arxiv.org/abs/2603.05451
sources:
  - https://arxiv.org/abs/2603.05451
  - https://arxiv.org/pdf/2603.05451
implementation: "Blackwell向けFlashAttention-4をCuTe-DSL/Pythonで実装し、B200上のBF16注意カーネルをcuDNN 9.13およびTriton等と比較。公式実装はDao-AILab/flash-attentionのflash_attn/cuteで公開されている。"
code: https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn/cute
last_checked: "2026-10-07"
arxiv_id: "2603.05451"
arxiv_categories:
  primary: cs.CL
  cross_list: []
worker_completed_at: "2026-10-07T17:35:03+09:00"
worker_run_key: "20261007-1735-scheduled-chat-30/r01"
reference_main_sha: "96e46e336be8e3716ca9bb21c93a09c05bf96666"
last_audited: null
audit_version: 0
---

## 概要

FlashAttention-4は、NVIDIA Blackwell世代で生じた「行列積だけが急速に高速化し、その周辺処理が追いつかない」という新しい注意計算の律速を対象にした、アルゴリズムとGPUカーネルの協調設計である。Hopper H100向けのFlashAttention-3では非同期実行とワープ特化が有効だったが、B200ではBF16 Tensor Coreの理論性能がH100の約1 PFLOPSから2.25 PFLOPSへ増える一方、共有メモリ読出し帯域や指数演算器の処理率はほぼ据え置かれる。そのため従来の「行列積を速くする」だけでは、softmaxや共有メモリ転送が先に詰まる。

論文の簡易ルーフライン解析では、典型的な128×128×128タイルで行列積が1024 cycle、指数演算も1024 cycle、共有メモリ読出しが768 cycleとなる。そこでFlashAttention-4は、Tensor Memory（TMEM）へ非同期MMAの累積結果を置き、行列積とsoftmaxを異なるワープグループで重ねる。さらに指数関数の一部をFMA命令による多項式近似へ逃がし、不要なsoftmax再スケーリングを省略する。逆伝播では2つの協調スレッドブロックを使う2-CTA MMAにより共有メモリ転送とdQの大域アトミック加算を減らす。

B200上のBF16評価では、FlashAttention-4はcuDNN 9.13比で最大1.3倍、Triton実装比で最大2.7倍の高速化を示し、最大1613 TFLOPs/s、理論ピークの約71%に達する。実装はC++テンプレートではなくPython内のCuTe-DSLで記述され、コンパイル時間も従来実装より20〜30倍短縮される。したがって本研究は単なるFlashAttentionの世代更新ではなく、GPU世代交代で律速資源が移動したときに、注意アルゴリズム側も資源配分を組み替える必要性を示す事例である。

## 問題設定

FlashAttention系列は、注意行列全体をHBMへ書き出さず、タイル単位で読み込みとオンラインsoftmaxを融合することでI/O量を削減してきた。FlashAttention-3はHopperの非同期行列積とワープ特化を利用したが、Blackwellではハードウェアの性能比が変わる。B200のBF16 MMAは1 SM・1 clock当たり8192演算へ倍増したのに対し、指数演算器は16演算/clock/SM、共有メモリ読出しは128 bytes/clock/SM程度に留まる。

この非対称な性能向上により、softmaxの指数演算や共有メモリからMMAオペランドを供給する時間が、Tensor Coreの演算時間と同等またはそれ以上になる。論文は、単純なHopper向けカーネルの移植ではBlackwellの演算性能を使い切れないことを、資源別cycle数から示す。特に長系列では注意の計算量そのものが大きいため、Tensor Coreを待たせる周辺処理がエンドツーエンドのカーネル性能へ直結する。

## 手法

### 非同期MMAとsoftmaxの重畳

BlackwellではMMAの累積値をレジスタではなく各SMのTensor Memoryへ直接非同期に書き込める。FlashAttention-4はこの性質を利用し、1つのスレッドブロックで2つのqueryタイルを交互に処理する。片方のタイルがTensor CoreでQK^TやPVを計算している間、別のワープグループがもう片方のsoftmaxを処理する。128×128という大きなMMAタイルとTMEMにより、Hopperで問題だった累積値のレジスタ圧迫を軽減し、行列積と非行列積処理の重なりを増やす。

softmax処理では各スレッドが行を担当し、最大値、指数化、行和を計算する。出力の再スケーリングは専用の補正ワープグループへ分離され、Tensor Coreの主要経路から外される。TMEMの容量は有限なので、S/P/Oの各タイルをどの時点で保持するかをパイプライン全体で調整する必要があり、単に「TMEMを使う」だけではなく配置と実行順序が設計の中心になる。

### 指数演算のFMA側への分散

softmaxでは多数の指数関数を計算するが、B200の専用MUFUは16演算/clock/SMであり、8192演算/clock/SMのMMAと大きな差がある。FlashAttention-4は指数計算の一部をCody–Waite型の範囲縮小と低次数多項式へ置き換え、通常の浮動小数点FMAユニットにも仕事を分散する。整数部は浮動小数点表現の指数ビット操作で処理し、小数部だけをHorner法の多項式で近似する。

ただし全てをソフトウェア指数へ置換すると、中間値と係数のためのレジスタ消費が増え、かえってspillが発生する。そのため各softmax行の10〜25%程度だけをFMA側で計算し、残りはMUFUへ残す。3次多項式はFP32ではハードウェア指数より誤差が大きいが、BF16へ丸めた後は量子化誤差が支配的になり、99%の入力でハードウェア実装と1 BF16 ULP以内に収まる。これは精度形式を前提に、未使用に近い演算資源へ処理を移す設計である。

### 条件付きsoftmax再スケーリング

オンラインsoftmaxは新しいkeyブロックで行最大値が更新されるたびに、既存の部分出力を指数係数で再スケーリングする。Blackwellではこの非MMA処理も相対的に高価になる。FlashAttention-4は最大値変化が十分小さい場合に再スケーリングをその場で実行せず、最終正規化へ補正を遅延する条件付き方式を導入する。目的はsoftmaxの数学的処理を変えることより、クリティカルパス上の指数・乗算処理を減らすことにある。

この方式は近似を含むため、無条件に省略するのではなく閾値を設ける。BF16で必要な数値精度と実際の最大値更新幅を利用し、性能上の利得と誤差を釣り合わせる。論文の精度評価では、指数近似とBF16丸めを分離して確認し、BF16条件では近似誤差より表現精度自体の誤差が支配的であることを示している。

### 2-CTA MMAによる逆伝播の共有メモリ削減

逆伝播ではdQ、dK、dVを求めるため複数のMMAと中間行列が必要で、共有メモリ帯域がより強い律速になる。128^3タイルの解析では、1-CTA構成のMMAが2560 cycleなのに対し共有メモリ処理は3328 cycleと約30%大きい。Blackwellの2-CTA MMAは、2つのCTAが1つのMMAへ協調参加し、Bオペランドを半分ずつ自分の共有メモリへ保持できる。

FlashAttention-4はこのモードをdQ計算へ組み込み、分散共有メモリでdSタイルの半分をCTA間交換する。これによりMMAへ供給する共有メモリ量だけでなく、大域メモリ上のdQへ行うアトミック加算回数も半減する。ルーフライン上の共有メモリcycleは3328から2688へ下がり、MMAの2560 cycleとの差が約5%まで縮む。代償としてCTAを固定ペアで起動し、TMEMとMMAのモードをペア全体で一貫させる制約が加わる。

### スケジューリングと再現可能実行

因果マスクや可変系列長では、CTAごとの処理量が不均一になる。FlashAttention-4は長い仕事を先に配置するスケジューリングとhead方向の配置調整を使い、後半に重いCTAだけが残るtailを抑える。また強化学習など再現性が必要な用途向けに決定的な逆伝播モードも用意し、大域reductionの書込み順をセマフォで直列化する。

決定性は並列reductionを制限するため無料ではなく、非決定版より性能が下がる。この点は「最速カーネル」と「再現可能なカーネル」を同じ性能値として扱わないために重要である。論文はカーネル設計だけでなく、負荷不均衡と再現性という実運用上の制約までBlackwell向けに扱っている。

## 評価

| 項目 | 条件 |
|---|---|
| 主アクセラレータ | NVIDIA Blackwell B200 |
| 精度 | BF16入力、FP32累積を中心に評価 |
| 比較対象 | cuDNN 9.13、Triton実装、FlashAttention系列 |
| 対象処理 | 注意のforward / backward、因果・非因果、可変長を含む |
| 実装 | CuTe-DSLをPythonへ埋め込んだカーネル |
| 主指標 | TFLOPs/s、相対高速化、資源cycle、数値誤差、コンパイル時間 |

主要な性能結果では、B200・BF16条件でcuDNN 9.13に対して最大1.3倍、Tritonに対して最大2.7倍となり、ピーク1613 TFLOPs/s、理論性能の約71%へ達する。特に4K以上の系列長では比較対象を継続的に上回ると報告される。一方、新しいcuDNN版はFlashAttention-4由来の技法を取り込んで性能差が縮むため、「全てのcuDNNに常に1.3倍」という結果ではない。

| 観点 | 結果 | 読み取れること |
|---|---|---|
| forward性能 | cuDNN 9.13比最大1.3倍、Triton比最大2.7倍 | Blackwell固有の非MMA律速対策が実カーネル性能へ反映 |
| 最大スループット | 1613 TFLOPs/s、約71%利用率 | Tensor Core以外の律速を隠蔽して高い実効利用率へ到達 |
| forward資源解析 | 128^3でMMA 1024、共有メモリ768、指数1024 cycle | 指数演算がMMAと同程度の律速である |
| backward資源解析 | 共有メモリ3328→2688 cycle（2-CTA） | 共有メモリとMMAの差を約30%から約5%へ縮小 |
| 指数近似精度 | 3次近似はBF16丸め後にハードウェアとほぼ同等 | FMAへ指数処理を分散してもBF16用途では誤差増が限定的 |
| コンパイル | CuTe-DSLで従来C++テンプレート比20〜30倍短縮 | カーネル開発・派生実装の反復時間も削減 |

この評価は主として注意カーネル単体の性能であり、LLMサービング全体のトークン毎秒や要求遅延を直接示すものではない。したがって1613 TFLOPs/sや2.7倍を、そのままモデル全体の生成速度倍率として解釈してはいけない。

## 既存研究との差

FlashAttention-1/2は主にHBMとのI/O削減と並列度改善、FlashAttention-3はHopperの非同期実行とワープ特化へ焦点を置いた。FlashAttention-4ではBlackwellでTensor Coreだけが大幅に伸びた結果、softmax指数演算と共有メモリが新しい律速へ移ったことを出発点にしている。つまり同じ注意式を高速化する系列でも、世代ごとのハードウェア資源比に合わせて最適化対象を移している。

また、低精度注意のように演算そのものをINT8/FP4へ落とす方式とは異なり、中心評価はBF16のままパイプライン、指数計算資源、TMEM、CTA協調を再設計する。近似を導入する箇所は指数関数の一部と条件付き再スケーリングに限定し、その誤差をBF16の表現誤差と分けて検証している点も特徴である。

## 限界

性能利得はBlackwellのTMEM、非同期MMA、2-CTA MMAなどへ強く依存するため、Hopper以前のGPUへ同じ設計をそのまま適用できない。B300/GB300では指数演算器自体の性能も変わるため、B200で最適な指数処理分担が将来世代でも最適とは限らない。

また主要評価は注意カーネルであり、モデル全体のサービング遅延、KVキャッシュ管理、通信、MLPなど別の律速を含むエンドツーエンド評価ではない。新しいcuDNNが本研究の技法を取り込むと差が縮むことも、利得が固定的ではないことを示す。決定的逆伝播もreduction順序を制約するため、非決定版と同じピーク性能は得られない。

## 一次資料

- arXiv: https://arxiv.org/abs/2603.05451
- PDF: https://arxiv.org/pdf/2603.05451
- 公式実装: https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn/cute