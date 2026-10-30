---
canonical_id: "DOI:10.1109/IISWC66894.2025.00019"
arxiv_id: "2507.02456"
arxiv_categories:
  primary: "cs.AR"
  cross_list: []
title: "Keeping up with Large Language Models: A Holistic Methodology of Compute, Memory, Communication, and Cost Modeling"
summary: "Optimus系の解析性能モデルにFlashAttention、MoE、DP/TP/SP/PP/EPの5次元並列、トポロジー別collective、チップレット製造コストを統合し、LLM推論・学習の速度対費用を事前予測する。8xA100上のFlashAttentionモデルで1.3〜1.7倍の高速化傾向を予測し誤差8%以内、MoEの大規模構成ではモデル予測で6.1倍、FlashAttention併用6.5倍を示す。ただしMoEの負荷不均衡を無視し256GPUで予測がずれ、モデル推定を実機ベンチマークと混同できない。"
list_summary: "FlashAttention・MoE・5D並列・ネットワーク・チップレット製造費を統合するLLM解析モデル。設計探索向けで実機サービング性能保証ではない。"
authors:
  - "Wenzhe Guo"
  - "Joyjit Kundu"
  - "Uras Tos"
  - "Weijiang Kong"
  - "Giuliano Sisto"
  - "Timon Evenblij"
  - "Manu Perumkunnil"
published: "2025-11-20"
publication: "IEEE IISWC 2025, pp.116-126"
publication_type: "conference"
publication_status: "published"
source: "https://doi.org/10.1109/IISWC66894.2025.00019"
sources:
  - "https://arxiv.org/pdf/2507.02456"
  - "https://arxiv.org/abs/2507.02456"
  - "https://doi.org/10.1109/IISWC66894.2025.00019"
implementation: "既存のOptimus解析モデルへhierarchical roofline、FlashAttentionタイル転送、MoEのexpert並列、トポロジー別collective通信、chiplet costの階層的モデルを追加。GPUクラスタ構成・帯域・面積・歩留まりを入力して実装前の速度/費用を推定する。"
code: null
last_checked: "2026-10-30"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-30T14:25:00+09:00"
worker_run_key: "20261030-1408-scheduled-chat-45/r01"
reference_main_sha: "8a4c43d4d90ff181c263ce52251dd48734928dda"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
research_job_source: "WORKLIST-45.md rank 39"
last_audited: null
audit_version: 0
---
# LLM性能・コスト統合モデル：FlashAttention、MoE、5D並列とチップレット製造費の共同探索

## 概要と対象範囲

本研究は新しいattention kernelやサービングエンジンを実装してtoken/sを直接改善する論文ではない。GPUクラスタ上のLLM学習・推論を、計算、HBM/SRAM、ネットワークcollective、チップレット製造費の各側面から解析的に見積もり、**ハードウェアの設計前に性能対費用を比較できるモデル**を構築する。著者らは既存のOptimusモデルを拡張し、FlashAttention、Mixture-of-Experts、expert parallelismを含む5次元並列、トポロジーに対応する通信アルゴリズム、半導体製造費の階層モデルを統合した。

従来のrooflineだけでは、FlashAttentionがHBM転送を減らす効果、MoEで少数expertのみ活性化する一方で全expertを保持するメモリ負担、GPU間all-to-allの混雑、chiplet分割で歩留まりは上がるが組立費とdie-to-die IOが増えるトレードオフを一緒に扱いにくい。性能だけでなく製造費を含めることで、最速の構成が必ずしも単位費用当たり最良ではないことを可視化する。研究の主な用途は大規模クラスタの設計探索であり、個々のユーザー要求のSLOを保証するオンラインスケジューラではない。

## 手法：システム表現、性能予測、製造費を接続

### 階層rooflineとFlashAttention

システムモジュールはアクセラレータの演算ピーク、各階層メモリ帯域、通信リンク、面積・電力制約を受け取り、task graphを構築する。性能予測では各演算のFLOPsと転送byte数から階層rooflineの実行時間を見積もり、並列化戦略に応じて通信時間を加える。既知GPUの性能を使う場合はマイクロアーキテクチャ生成器を省略できる。GPUの全命令をcycle-accurateに模擬するのではなく、モデル演算とデータ移動の支配項を解析式で計算するため、大規模な設計空間を探索できる。

FlashAttentionのモデルは、標準attentionで`QK^T`のスコア行列、softmax確率、`PV`の中間結果をHBMへ繰り返し書き戻す方式と、SRAM上でタイル処理してonline softmaxを進める方式の差を表現する。論文§III-Bの式(1)ではFlashAttentionの時間を、HBMロード、GEMM、点演算・reduction、HBMストアの和として表す。タイルサイズはSRAM容量とhead dimensionに制約される。これにより単純なFLOPs削減ではなく、HBMトラフィックを減らすことでメモリ律速から計算律速へ移る挙動を近似する。

ただしQKV projectionやMLPまで自動的に高速化されるわけではない。FlashAttentionがattention本体の転送を減らしても、他の演算が残るためE2E倍率には上限がある。原著は条件によってattentionが全時間の60%超を占める例を挙げ、単一kernelの改善倍率をそのまま全モデルの倍率としないよう注意している。

### MoEと5次元並列

MoEでは全expertを常に計算するのではなく、routerが選んだ少数expertのみ実行するため、活性パラメータ数に対する計算量が減る。一方、総expertの重みを保持するメモリ容量と、expertへのtoken分配・回収のall-to-all通信が増える。モデルはexpert数、各tokenのtop-k、EP degreeを含めて計算と通信を推定する。従来のDP/TP/SP/PPにEPを加え、**5D（data, tensor, sequence, pipeline, expert）**の配置候補を比較する。

DPは複製とバッチ分割、TPは層内の行列分割、SPはsequence方向の分割、PPは層の段階分割、EPはexpertを異なるGPUに配置する方式であり、どの次元を増やしても通信の種類・量が同じではない。たとえばEPのall-to-allはrouter分布に依存し、TPのcollectiveは各層の同期を生む。ネットワーク側はfully connected、switch、ring、2D mesh等のホップ数、リンク帯域、collectiveアルゴリズムを使って通信時間を計算する。大規模化による演算並列性の利益と、GPU数増による通信遅延を同時に比較する。

### チップレット費用モデル

コストモジュールは論理die、HBMスタック、die-to-die IO、インターポーザ、パッケージング、テスト、欠陥密度と歩留まりを階層的に扱う。論理dieを小分割すると単一dieの歩留まりは改善し得るが、IO領域・接続・組立費が増える。論文はnegative binomial yieldモデルを用い、システム構成から総コストを計算する。性能予測とコスト予測を接続することで、A100型のlogic die面積やHBM本数を変えた複数設計について、GPT3-175Bの学習・推論時間と費用のPareto関係を比較する。

## 評価条件と検証の性格

| 観点 | 一次論文の条件 |
|---|---|
| FlashAttention検証 | GPT2-small 125M、GPT2-medium 355M、文脈1K〜4K、A100-40GB×8、NVLink gen3。公開測定データとの比較 |
| MoE検証 | DeepSpeed-TEDのGPT3-6.7Bベース、batch 1024、V100 16GBを搭載するSummit、TP=4でGPU数・expert数を変更 |
| ネットワーク検証 | 16 V100、NVLink 150GB/s、64MB〜1.5GBのall-reduce。ASTRA-simと実測値を比較 |
| FlashAttention case study | GPT2-XL 1.5B、16 H100、文脈2048、batchサイズとGPU世代A100/H100/B200を変更 |
| MoE case study | Megatron 145B対MoE 139B（活性13B、32expert）、256 GPU、EP/TP/DPを設定 |
| 推論ネットワーク | Llama 80B、A100 8/16 GPU、fully connected・switch・ring・2D mesh |
| 費用モデル | GPT3-175B、1024 GPU、A100のHBM 4/5/6/8本や半面積logic dieを比較 |

これらはすべて単一の実機で全構成を実装した実験ではない。検証用の公開実測データと、検証済みモデルを用いた仮想構成のwhat-if推定を明確に区別する必要がある。

## 主要結果と負の結果

| 出典 | 結果 | 解釈 |
|---|---|---|
| Figure 2、FlashAttention検証 | 公開実験の高速化1.3〜1.7倍に対し予測誤差**8%以内** | 8xA100、GPT2-small/mediumという限定条件でのモデル精度 |
| Figure 2、4K文脈 | 1Kの非FlashAttention実装比で4KのFlashAttention実装が1.3〜1.4倍速い条件を提示 | 入力長が異なる比較なので、同一入力の単純な倍率ではない |
| Figure 3、MoE検証 | DeepSpeed-TEDのbaselineと最適化版の実測境界の間に予測が位置 | load imbalanceとduplicate-token dropping、通信認識checkpointingはモデル外 |
| Figure 3、256GPU | GPU数が大きいと**負荷不均衡の影響を過小評価**し予測がずれる | 解析モデルの明示的な負の結果 |
| Figure 4、通信 | all-reduceの予測時間はASTRA-simと実機の間。差の一因はswitching latency | 完全なネットワークcycle simulatorではない |
| Figure 5、FlashAttention | batch増で予測上の改善が大きくなる。A100→H100→B200でcompute/HBM帯域比が変化 | GPU世代差とbatch形状の仮定に依存 |
| Figure 6、MoE-139B | Megatron-145B比**約6.1倍**、FlashAttention併用で**約6.5倍**の予測 | 256GPUの解析ケーススタディ。実機token/sの直接測定ではない |
| Figure 6、TP併用 | TPが強い条件ではFlashAttentionの追加利益が**約1.1倍**に縮小 | attention以外の計算・通信が支配し、単独kernelの利益が隠れる |
| Figure 4、Llama80B推論 | fully connectedが最良、switchが次点、ring・2D meshはhop数増で不利 | トポロジー・リンク帯域の固定条件でのモデル予測 |
| Figure 7、費用対時間 | HBM本数・logic die面積を変えると、最短時間と最低費用が一致しない | 正規化費用・正規化時間であり、製品価格や実際のTCOではない |

Figure 6の6.1倍と6.5倍は、計算量の異なるdense/MoEモデルのモデル予測であり、同一品質を実測した速度比較ではない。MoEの活性13Bという仮定と全重み139Bの保持容量は両立する。高い倍率は計算量削減によるもので、メモリ容量やall-to-all通信が不要になることを意味しない。

## 限界とサーベイ上の意義

最大の制約は、解析モデルが平均的な演算・通信量を推定する一方で、実サーバーのリクエスト到着分布、dynamic batching、prefill/decodeの混在、GPUカーネル起動オーバーヘッド、ネットワーク輻輳、tail latencyを十分に捉えないことである。論文はMoEのload imbalanceをモデル化していないと明記し、256GPUの検証で差が出ている。MoE expertの偏った選択、GPU間転送の非対称性、キュー待ち時間が大きい本番サービングに、そのままE2E SLO予測器として適用するのは不適切である。

FlashAttentionの性能モデルもv1を中心に検証され、FlashAttention-2/3のカーネル最適化、量子化GEMM、複雑なfused opの実行時間をすべて保証するものではない。実装上のbatch形状とメモリ階層が変われば、rooflineの支配項も変わる。GPU世代の比較も仮定したピーク演算性能・HBM帯域・NVLink性能に依存する。

費用モデルは半導体製造のarea/yield/assemblyを対象にしており、電力料金、運用人員、クラウド課金、設備償却、故障率、ネットワーク設備の長期TCOをすべて含むわけではない。正規化された製造コストを利用者のGPUレンタル費と同一視できない。性能最適化の選択は、用途に応じて実測値で再校正する必要がある。

それでも、MoEのexpert parallelismとFlashAttentionの効果がネットワークとメモリ階層でどう変わるか、GPU増設が通信費用に負ける点、HBM容量増加の費用対効果を一つの設計空間で比較できる点は重要である。サーベイでは、**推論サーバーを直接高速化する方式ではなく、ハードウェア・並列配置・費用を共同探索する解析モデル**として分類する。vLLM/SGLangなどの実装実験、TTFT/TPOTを測るベンチマークとは役割を分けて扱う。

## 一次資料

- [arXiv:2507.02456v1 PDF（11ページ）](https://arxiv.org/pdf/2507.02456)：§III〜V、Figure 1〜7、FlashAttention・MoE・通信・費用モデル、負荷不均衡の限界を確認。
- [IEEE IISWC 2025 DOI](https://doi.org/10.1109/IISWC66894.2025.00019)：正式出版題名・会議・2025-11-20のIEEE Xplore公開日を確認。
- [arXiv書誌](https://arxiv.org/abs/2507.02456)：先行版の題名は「System-performance and cost modeling of Large Language Model training and inference」。著者7名・初稿2025-07-03。
