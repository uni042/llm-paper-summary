---
canonical_id: "DOI:10.1109/isca59077.2024.00082"
title: "LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference"
summary: "LLM推論用ハードウェア設計を実機試作なしで比較するため、演算子性能モデル、最適マッピング探索、面積ベースのコストモデルを統合した評価基盤。実機に対する推論遅延誤差は平均4.1%で、4×A100上のGPT-3 175B推論と26,400通りのマッピング探索を汎用機で16分以内に模擬し、A100比最大3.41倍の性能/コストとなる設計候補を探索した。"
list_summary: "演算子性能・最適マッピング・面積コストを統合し、LLM推論アクセラレータの性能/コスト設計空間を高速に探索するハードウェア評価基盤。"
authors: ["Hengrui Zhang","August Ning","Rohan Baskar Prabhakar","David Wentzlaff"]
published: "2024-06-29"
publication: "ISCA 2024"
publication_type: "Conference"
publication_status: "Published"
source: "https://doi.org/10.1109/ISCA59077.2024.00082"
sources: ["https://doi.org/10.1109/ISCA59077.2024.00082","https://ieeexplore.ieee.org/document/10609604"]
implementation: "LLM推論演算子の性能モデル、mapper、area-based cost modelを実装し、A100等の実機測定との誤差検証とGPT-3 175B設計空間探索を実施。公式コードはPrincetonUniversity/LLMCompass。"
code: "https://github.com/PrincetonUniversity/LLMCompass"
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T04:04:00+09:00"
worker_run_key: "20261004-0345-scheduled-chat-45/r01"
last_audited: null
audit_version: 0
---
# LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference

## 概要
LLM推論アクセラレータを設計するとき、演算器数、メモリ種類・帯域、チップ面積、並列配置を変えるたびにRTL実装や実機評価を行うのは現実的でない。しかもLLMは層ごとにGEMM、注意機構、通信など性質の異なる演算を含み、同じハードウェアでもマッピング次第で性能が大きく変わる。LLMCompassは、ハードウェア記述から演算子性能を予測し、mapperが高速な配置・scheduleを探索し、面積ベースのコスト モデルで性能/コストまで比較する。

実機との比較では各種演算子・入力 サイズの遅延誤差が平均10.9%、LLM推論全体では平均4.1%。4台のNVIDIA A100でGPT-3 175Bを実行する構成を、26,400回のmapper パラメータ searchを含めて汎用ハードウェア上16分以内でシミュレーションする。設計探索ではcompute capabilityを下げる、HBMを通常DRAMへ置き換える等の候補から、A100比最大3.41倍のperformance/コストを示す設計を導く。

## 問題設定
従来のアクセラレータシミュレータは一般DNNを対象とするものが多く、LLMの巨大な重み footprint、autoregressive デコード、テンソル 並列通信を含む推論を高速かつ十分な精度で評価することが難しい。一方、実GPUだけで設計探索すると、存在しないメモリ構成や演算器比率を試せず、探索可能な点が市販品へ限定される。

LLM推論ではプリフィルとデコードで演算特性が違う。大きな行列を処理するプリフィルは演算能力の影響が強い一方、デコードは小バッチで重みを繰り返し読むためメモリ帯域の影響が強い。この違いを無視した単一peak FLOPS指標では、設計変更の価値を判断できない。

## 手法
### 性能モデル
LLMCompassは各演算子を対象ハードウェアへmappingした際の実行時間を推定する。計算資源、オンチップバッファ、外部メモリ 帯域などを設計パラメータとして扱い、単なるルーフラインの上限値ではなく実行scheduleを含めて遅延を評価する。

### Mapper
同じ演算子でもtile サイズ、loop order、並列化方法によってdata 再利用とメモリ 通信量が変わる。mapperは候補mappingを探索し、対象ハードウェアで性能が良いscheduleを選ぶ。GPT-3 175Bの4×A100例で26,400 roundsのパラメータ searchを含めても16分以内という速度は、ハードウェア design space explorationを反復可能にするための重要な性質である。

### 面積・コストモデル
性能だけ高い巨大チップを選ぶのではなく、演算器やSRAM等が占める面積からコストを推定しperformance/コストを比較する。これにより「HBMを増やす」「computeを増やす」といった直感的設計だけでなく、デコードが帯域律速ならcomputeを減らして面積・費用を下げる構成も候補になる。

## 評価条件・主要結果
| 観点 | 結果 |
|---|---|
| 演算子予測 | 実機比平均10.9% 遅延 error |
| LLM E2E予測 | 平均4.1% 遅延 error |
| 代表探索 | GPT-3 175B、4×NVIDIA A100 ノード |
| 探索量 | mapper 26,400 roundsを含む |
| シミュレーション時間 | commodity ハードウェアで16分以内 |
| design探索 | A100比最大3.41倍 performance/コスト |

4.1%という値は「提案アクセラレータが4.1%速い」という意味ではなく、LLMCompassの予測値と実機測定の誤差である。3.41倍は探索された設計の性能/コスト改善であり、単純な遅延倍率とは区別する必要がある。

## 既存研究との差
一般DNN向け性能モデルや単一演算子のanalytical モデルに対し、LLMCompassはLLM ワークロード、mapping search、area/コストを一体化する。特に「存在するGPUのベンチマーク」ではなく、未製造のハードウェア configurationをLLM推論全体で比較できる点がハードウェア/software co-designに向く。

## 限界
性能モデルは実機の全てのランタイム効果を再現するわけではなく、カーネル実装、キャッシュ挙動、集合通信 library、software オーバーヘッドが変われば誤差も変わる。探索結果は想定technology/コスト モデルに依存する。さらに2024年以降のMoE、disaggregated 推論提供、投機的復号、agentic ワークロードなどをそのまま代表するわけではなく、新しい演算子や通信patternにはモデル拡張が必要になる。

## 一次資料
- https://doi.org/10.1109/ISCA59077.2024.00082
- https://ieeexplore.ieee.org/document/10609604
- https://github.com/PrincetonUniversity/LLMCompass