---
canonical_id: title:spaceserve-spatial-multiplexing-of-complementary-encoders-and-decoders-for-multimodal-llms
openreview_id: w4qJ056WhI
doi: 10.52202/085713-2652
title: 'SpaceServe: Spatial Multiplexing of Complementary Encoders and Decoders for Multimodal LLMs'
authors:
- Zhicheng Li
- Shuoming Zhang
- Jiacheng Zhao
- Siqi Li
- Xiyu Shi
- Yangyu Zhang
- Shuaijiang Li
- Donglin Yu
- Zheming Yang
- Yuan Wen
- Huimin Cui
published: 2025-12
publication: Advances in Neural Information Processing Systems 38 (NeurIPS 2025)
publication_type: conference
publication_status: published
source: https://proceedings.neurips.cc/paper_files/paper/2025/file/720e7ebc49c84252abc0754dddf80976-Paper-Conference.pdf
sources:
- https://proceedings.neurips.cc/paper_files/paper/2025/file/720e7ebc49c84252abc0754dddf80976-Paper-Conference.pdf
- https://openreview.net/forum?id=w4qJ056WhI
code: https://github.com/gofreelee/SpaceServe
implementation: NVIDIA A100 SXMを8基搭載した単一サーバーで、libsmctrl等のSM割当機構により視覚エンコーダとLLMデコーダをSM単位で空間分離。オフラインの演算子別プロファイルから資源効用曲線を構築し、オンラインSISとエンコーダ用TWSRTFを組み合わせる。vLLM v1を比較対象としてQwen2-VL系列とMoE系VLMを評価。
summary: SpaceServeはマルチモーダルLLMの計算律速な視覚エンコーダとメモリ律速なテキストデコーダを、GPUの異なるSM群へ同時配置する空間多重化サービング基盤。演算子別資源効用曲線からSM割当を決めるSISと、視覚要求を時間窓内で短い順にバッチ化するTWSRTFを用いる。NeurIPS 2025の8×A100実測では、Qwen2-VL-2Bの10 req/sでvLLM v1比TPOT最大28.9倍改善する一方、TTFTは改善せず一部条件で悪化する。原worklistに付いたDOI:10.1145/3695053.3730987は別論文AIMを指すため使用しない。
list_summary: 視覚エンコーダとLLMデコーダをSM単位で空間分離し、動的な資源配分と視覚要求バッチ化でMLLMのTPOTを削減。10 RPSで最大28.9倍、TTFTは改善せず。
last_checked: '2026-10-30'
worker_id: scheduled-chat-45
worker_run_key: 20261030-0245-scheduled-chat-45/r01
previous_worker_run_key: 20261030-0155-scheduled-chat-00/r01
reference_main_sha: 2796fce9eb89505f4aaa1cc81769656cba98f54b
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
identity_warning: Worklist DOI:10.1145/3695053.3730987 resolves to unrelated ISCA paper AIM. This summary uses NeurIPS official PDF and normalized title identity; GitHub import inbox should resolve canonical identity.
worker_completed_at: '2026-10-30T02:52:00+09:00'
metadata_repair_source: https://proceedings.neurips.cc/paper_files/paper/2025/hash/720e7ebc49c84252abc0754dddf80976-Abstract-Conference.html
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2403.02310
- canonical_id: arXiv:2205.14135
- canonical_id: arXiv:2010.05680
- canonical_id: arXiv:2405.21075
  arxiv_id: '2405.21075'
- canonical_id: arXiv:2407.21783
  arxiv_id: '2407.21783'
- canonical_id: arXiv:2408.08147
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: arXiv:2404.14469
- canonical_id: arXiv:2302.11665
- canonical_id: arXiv:2412.19437
  arxiv_id: '2412.19437'
- canonical_id: arXiv:2409.09086
- canonical_id: arXiv:2311.18677
- canonical_id: arXiv:1909.08053
- canonical_id: arXiv:2501.05460
- canonical_id: arXiv:2302.13971
  arxiv_id: '2302.13971'
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: arXiv:2312.05516
- canonical_id: arXiv:2312.07104
- canonical_id: arXiv:2401.09670
references_checked_at: '2026-10-29'
references_source: primary-pdf-reference-section
references_total: 42
---

# SpaceServe：視覚エンコーダとLLMデコーダをGPU内で空間多重化するサービング方式

## 概要

マルチモーダルLLMは画像・動画などを処理するエンコーダと、テキストを逐次生成するデコーダを組み合わせる。画像エンコーダは大きな行列演算を行う計算律速、デコーダの1トークン生成は重み・KVキャッシュの読み込みが支配的なメモリ律速になりやすい。一般的なサービング基盤は両者を同じGPU上で時間的に交互実行するため、長い画像エンコードの間はデコーダの次トークン生成が待たされ、TPOTが増える。

SpaceServeは両者を別GPUへ完全に分けるのではなく、**同じGPUの異なるStreaming Multiprocessor（SM）群へ空間的に配置**する。エンコーダの計算資源需要とデコーダのメモリ帯域需要が補完的であることを利用し、同じ時間に異なる資源を消費させる。SMを何基ずつ割り当てるかはオフラインの演算子プロファイルから作る資源効用曲線に基づき、要求の画像解像度・入力長・負荷に応じてオンラインで変える。さらにエンコーダ要求は時間窓内で小さい入力を先にバッチ化し、待ち行列と大要求の飢餓を調整する。

NeurIPS 2025公式論文では8基のA100 SXMを持つ単一ノードで、Qwen2-VL-2B/7B、Qwen2.5-VL-32B、Qwen2-VL-72B、DeepSeek-VL2、Kimi-VLを評価する。Qwen2-VL-2Bの10要求/秒で、vLLM v1比のTPOTが最大28.9倍改善する条件がある。一方、TTFTはほぼ同等か一部悪化し、エンコーダ単体の処理時間を短縮する課題は残る。速度改善はモデルの演算数削減ではなく、エンコードとデコードの実行干渉を取り除くことによる。

## 問題設定と既存手法との差

画像の解像度が上がると、エンコーダの計算量は増えるが、デコーダの1トークン生成で必要な重み読み込みの性質は大きく変わらない。原著Table 1はQwen2-VL-7BのA100上のArithmetic Intensity（FLOPs/byte）を示し、512×512画像ではエンコーダ338.21、デコーダdecode 0.887、2048×2048画像ではエンコーダ8826.97、decodeは0.887である。つまりエンコーダは計算密度が高く、decodeは非常に低い。両者を同時に実行すれば、計算ユニットとメモリ帯域の空き部分を相互に利用できる余地がある。

vLLMの通常パイプラインでは、画像エンコード・prefill・decodeを時間的に切り替えるため、エンコーダの長いカーネルがdecodeを遮る。MPSで複数プロセスを同じGPUに載せても、異なるカーネルが同一SM内でレジスタ・L1キャッシュ・共有メモリ・演算器を競合し、安定した低TPOTを保証しない。SpaceServeはSM群を明示的に分けて干渉を抑え、同時実行の資源配分を要求ごとに調整する。P/D分離のDistServeやSplitwiseとは異なり、マルチモーダルの**エンコーダとデコーダの補完性**を主対象とする。

## 手法

### 1. エンコーダ・デコーダを論理的に分離し、GPU内で再結合する

SpaceServeは入力前処理を行うCPUプロセス、画像・動画などのモダリティエンコーダ、共有テキストデコーダを分けて管理する。エンコーダで得たモダリティトークンをデコーダへ渡すが、実行先は必ずしも別GPUである必要はない。同じGPU上の異なるSM集合を使い、エンコーダの計算カーネルとデコーダのメモリ律速カーネルを並行実行する。GPUのSM単位で空間分割することで、同一SM上の資源競合を抑える。

この構造では、エンコーダだけを最速にすることが目的ではない。デコーダのトークン生成を長いエンコーダ処理で止めないことが、全体のTPOTを下げる鍵になる。エンコーダを完全に独立したGPUへ置く場合は別GPUの容量・転送費用が必要になるが、SpaceServeは同一GPU内の余剰資源を使うため、SM割当を適切に調整できれば効率を高められる。

### 2. オフラインの演算子別Resource–Utility Curve

原著§3.1は、GPUのSM割当率と各演算のレイテンシの関係が線形ではないことを指摘する。画像解像度、視覚パッチ数、テキスト長によって、行列積やAttentionの形状と演算密度が変わる。単にSMを半分与えれば時間が2倍になると仮定するモデルでは、適切な割当を選べない。

そこで、行列積とAttentionなど主要演算子を異なる入力形状・SM割当数で測定し、演算子ごとの性能データベースを構築する。Algorithm 1はモデルの層構造から各層の演算子形状を計算し、測定済みの演算時間と層のオーバーヘッドを積み上げ、モデル全体のSM数→実行時間の資源効用曲線を作る。実行時には入力の解像度や長さから適切な曲線を参照する。

このプロファイリングはモデル・GPU・入力形状に依存するため、全く別のGPUへ移すと再測定が必要となる可能性がある。GPUの空きSM数を機械的に等分するのではなく、エンコーダとデコーダの限界利得を比較して割り当てるための基盤である。

### 3. TWSRTF：エンコーダ用の時間窓付き短ジョブ優先

画像エンコーダは入力解像度やパッチ数で処理時間が大きく変わる。小さい要求を先にまとめると平均待ち時間を減らせるが、単純な最短ジョブ優先では大きい画像・動画要求が飢餓状態になる。SpaceServeのTime-Windowed Shortest Remaining Time First（TWSRTF）は、固定時間窓内に到着した要求を取り出し、パッチ数の少ない順に並べて、GPUのバッチ容量を超えない範囲でまとめる。

窓を設けることで順序変更の範囲を限定し、要求を無期限に後回しにすることを避ける。バッチ容量はパッチ総数に基づいて制約し、計算密度の高いエンコーダが過大なバッチでGPUを占有することを防ぐ。TWSRTFはエンコーダの待ち行列に適用する方式であり、テキストデコーダの通常の動的バッチ処理を置き換えるものではない。

### 4. SIS：オンラインでSM割当を更新する

Space-Inference Scheduler（SIS）は新しいエンコーダ要求が到着すると、画像解像度・パッチ数・入力長・実行中デコーダの状態を取得する。オフラインの資源効用曲線から、エンコーダとデコーダへ割り当てるSM数を決める。NVIDIAではlibsmctrlなどのSM制御、AMDではHIPのCU maskのような実行時分割機構を利用する。単なるCUDAストリーム並行実行ではなく、異なるSM群を明示的に割り当てることが重要である。

デコーダのメモリ帯域を使う処理は、SMを増やしてもほとんど速くならない場合がある。そのようなときは余剰SMをエンコーダへ割り当て、decodeのTPOTを維持しつつ画像処理を進める。逆にデコーダの負荷が大きい場合は、SM割当を調整する。固定のSM分割より入力の変化へ追従できる点がSISの役割である。

### 5. 実行順序と資源競合の扱い

CPUで入力を受け付け、TWSRTFがエンコーダの実行バッチを作ると、SISがデコーダの状態と照合してSM割当を更新する。エンコーダの出力トークンが準備できたらデコーダ側の入力として利用し、デコーダはテキストを生成する。この間、別要求のエンコーダ処理が進行できるため、画像のエンコード時間と既存要求のdecode時間を重畳できる。

重要なのは、単一要求のエンコーダの処理時間を劇的に短縮するわけではない点である。大きな画像のエンコード自体が遅ければ、その要求のTTFTは長いままになる。効果が大きいのは、多数の要求が混在し、エンコーダとデコーダの時間分割がdecodeをブロックしていた条件である。

## 評価

### 実験条件

原著§4はIntel Xeon Gold 6430 CPUと8基のNVIDIA A100 SXMを持つ単一サーバーを使用する。Qwen2-VL-2B/7Bは単一GPU、Qwen2.5-VL-32Bは4GPU、Qwen2-VL-72Bは8GPUのTensor Parallel構成。MMMU-ProとVideo-MMEから1740例を抽出し、画像8割・動画2割の混合負荷を作る。比較対象はvLLM v1であり、到着率2〜10 req/sを変えてTTFTとTPOTを測定する。加えてMoE型MLLMのDeepSeek-VL2とKimi-VL、高解像度画像の条件を検証する。

| モデル、10 req/s | vLLM v1 TPOT | SpaceServe TPOT | 本文報告の速度比 |
|---|---:|---:|---:|
| Qwen2-VL-2B | 約365ms | 約12.62ms | 最大28.9倍 |
| Qwen2-VL-7B | 約489ms | 約40ms | 約12.3倍 |
| Qwen2.5-VL-32B | 約522ms | 約144ms | 約3.62倍 |
| Qwen2-VL-72B | 約489ms | 約155.8ms | 約3.14倍 |
| DeepSeek-VL2（MoE） | 122.5ms | 30.0ms | 4.08倍 |
| Kimi-VL（MoE） | 482.0ms | 49.0ms | 9.84倍 |

原著Figure 3の図上の丸め値と本文のより細かい実測値には小さな差があるため、表では本文の数値を優先した。28.9倍はQwen2-VL-2Bの特定の高負荷条件における**TPOT比**であり、TTFTや総要求処理量が28.9倍になったという意味ではない。モデルが大きくなると速度比は小さくなるが、72Bでも同じ8GPU構成でTPOTの改善がある。

### 解像度への感度

原著Table 3は10 req/sで画像解像度を変えた場合のTPOTを比較する。224×224ではvLLM 23.6ms、SpaceServe 17.2msで1.37倍。512×512では38.6ms対25.9msで1.49倍。1024×1024では212.6ms対35.6msで5.97倍。2048×2048では470.7ms対38.0msで12.39倍となる。解像度が高くなるほど視覚エンコーダが計算律速となり、時間分割方式でdecodeが待たされるため、空間多重化の利得が大きくなる。

一方、TTFTは2048×2048でvLLM 139.35秒、SpaceServe 135.76秒と依然非常に長い。1024×1024ではvLLM 15.31秒、SpaceServe 15.54秒でわずかに悪化する。高解像度でもdecode待ちを減らす効果はあるが、単一画像のエンコード時間そのものは主要なボトルネックとして残る。

### アブレーション：MPSとSM分割、TWSRTF

原著Figure 4はQwen2-VL-7Bで、単にMPSで二つのプロセスを並行させた場合と、SMを明示分割したSpaceServeを比較する。10 req/sのTPOTはMPS約127msに対してSpaceServe約40ms、約3.2倍の差がある。2 req/sではMPS約90msに対してSpaceServe約30msであり、空間分割がSM内部の資源競合を減らす効果を示す。原著はエンコーダ用TWSRTFを外した条件も評価し、負荷が上がるほど短い視覚要求のバッチ化が有利になることを示す。単なる別CUDAストリームの起動だけで同じ利得を得られるとは限らない。

### TTFTの負の結果

原著付録BのTable 4は、SpaceServeがTTFTを大きく改善しないことを明確に示す。Qwen2-VL-2Bの10 req/sではvLLM 26.038秒に対しSpaceServe 27.437秒で悪化する。Qwen2.5-VL-32Bでは47.547秒対48.966秒、Qwen2-VL-72Bでは42.067秒対43.834秒である。Qwen2-VL-7Bでも38.795秒対39.086秒と小さく悪化する。これらはTPOTの大幅改善と同時に成立するため、システムの良し悪しはどちらのSLOを重視するかに依存する。

## 限界

著者は付録Aで、SpaceServeが主にTPOTの改善を実現した一方、**TTFTは既存のvLLM v1と同程度にとどまる**ことを限界として認める。画像エンコーダの単独処理時間が長い場合、SMの同時配置だけでは初回トークンまでの時間を短縮できない。高解像度でTTFTが数十〜百秒規模となる条件があり、インタラクティブなSLOを満たすにはエンコーダ自体の高速化が別途必要である。

評価は単一の8×A100サーバーと特定のQwen2-VL/DeepSeek-VL2/Kimi-VL系列、画像・動画比8:2の混合データに限られる。SM単位の制御はGPUランタイムの機能に依存し、すべてのGPUで同じ細粒度分割が可能とは限らない。オフラインの演算子別プロファイルはモデルとGPUに依存するため、別のアーキテクチャや入力分布へ移す場合は再プロファイルが必要となる。

28.9倍の改善はvLLM v1の時間分割でdecodeが強くブロックされる高負荷条件で得られた値である。入力負荷が小さい、エンコーダとデコーダの資源需要が補完的でない、あるいはGPUが全面的に計算・メモリ両方で飽和している条件では同じ改善率は期待できない。実際に224×224ではTPOTの改善が1.37倍にとどまる。推論品質の変更を目的とした手法ではないが、モデル出力の意味的品質や多様なSLOの公平性を網羅的に検証したものでもない。

## 既存研究との差と位置づけ

WindServeはprefillとdecodeの役割をまたいで仕事を移し、別CUDAストリームで干渉を減らす。SpaceServeはマルチモーダルの**エンコーダとテキストデコーダ**に焦点を当て、GPUのSM群を明示的に分割する。従来のP/D分離は異なるGPU・インスタンス間の仕事配置が主眼であり、SpaceServeは同じGPUの計算・メモリ資源の補完性を使う。MPSと比較してSM内部のレジスタやL1キャッシュの競合を減らす点も特徴である。

本サーベイでは「マルチモーダルLLMサービング・GPU空間多重化」に分類する。Qwen3-VLなど視覚エンコーダとデコーダを持つモデルをGPUで配備する際、視覚エンコードの計算とdecodeのメモリI/Oをどう重畳するかという研究上の視点を提供する。ただしRTX4070級の単一GPUやWindows環境で同じSM制御を利用できるとは限らず、論文の8×A100実測をそのまま移植可能と考えるべきではない。

## identityと一次資料の監査注記

worklistにはSpaceServeに `DOI:10.1145/3695053.3730987` が付いていたが、このDOIのACM公式PDFは「AIM: Software and Hardware Co-design for Architecture-level IR-drop Mitigation in High-performance PIM」であり、**SpaceServeとは別論文**だった。誤ったDOIをcanonical identityとして採用すると、AIMとの衝突や誤搬送が発生する。今回の原稿はNeurIPS公式PDFとOpenReviewを一次資料とし、タイトルに基づく暫定identityを採用した。GitHub import inboxにおいて正式なidentity照合を行う必要がある。

- [NeurIPS 2025公式PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/720e7ebc49c84252abc0754dddf80976-Paper-Conference.pdf)：§2のAI比較、§3のSIS/TWSRTF/SM分割、§4のFigure 3–4・Table 2–3、付録A–Bの限界・TTFTを照合。
- [OpenReview正式ページ](https://openreview.net/forum?id=w4qJ056WhI)：会議論文の同定。
- [誤指定DOIのACM PDF](https://dl.acm.org/doi/pdf/10.1145/3695053.3730987)：別論文AIMを指すことを確認。SpaceServeの参照文献としては使用しない。
