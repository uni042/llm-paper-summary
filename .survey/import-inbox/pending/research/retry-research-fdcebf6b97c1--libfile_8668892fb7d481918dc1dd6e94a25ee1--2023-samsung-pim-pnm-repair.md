---
canonical_id: "DOI:10.1109/HCS59251.2023.10254711"
title: "Samsung PIM/PNM for Transformer Based AI: Energy Efficiency on PIM/PNM Cluster"
summary: "Transformer生成のメモリ帯域律速を、HBM/LPDDR内演算とCXL近傍演算でデータ移動そのものを減らして改善するSamsungのPIM/PNMシステム群を報告する。"
list_summary: "HBM・LPDDR・CXLの各メモリ階層へ演算を寄せ、Transformer生成のGEMVと大容量モデル配置で帯域・電力・容量制約を緩和する。"
authors: ["Jin Hyun Kim","Yuhwan Ro","Jinin So","Sukhan Lee","Shinhaeng Kang","YeonGon Cho","Hyeonsu Kim","Byeongho Kim","Kyungsoo Kim","Sangsoo Park","Jin-Seong Kim","Sanghoon Cha","Won-Jo Lee","Jin Jung","Jong-Geon Lee","Jieun Lee","JoonHo Song","Seungwon Lee","Jeonghyeon Cho","Jaehoon Yu","Kyomin Sohn"]
published: "2023-08"
publication: "2023 IEEE Hot Chips 35 Symposium (HCS)"
publication_type: "conference"
publication_status: "published"
source: "https://www.hc2023.hotchips.org/assets/program/conference/day1/PIM/23_HC35_PIM_PNM_Samsung_final.pdf"
sources: ["https://www.hc2023.hotchips.org/assets/program/conference/day1/PIM/23_HC35_PIM_PNM_Samsung_final.pdf","https://doi.org/10.1109/HCS59251.2023.10254711"]
implementation: "SamsungのHBM-PIM、LPDDR-PIM、CXL-PNMを実機測定とシミュレーションで評価。公開コードURLは一次資料から確認できなかった。"
code: null
last_checked: "2026-10-08"
worker_completed_at: "2026-10-08T03:25:58+09:00"
worker_run_key: "20261008-0325-scheduled-chat-30/repair-r01"
reference_main_sha: "d50824fe2088a6ebdc80b1a81ec856137bb5f08c"
quality_self_review_passed: true
quality_self_review_version: "2026-10-07-v1"
last_audited: null
audit_version: 0
---

## 概要

Transformerの逐次生成では、巨大な重み行列を毎トークン読み出す行列・ベクトル積が多く、演算器よりメモリ帯域が律速になりやすい。SamsungのHot Chips 35報告は、このデータ移動を減らすため、メモリ内処理とメモリ近傍処理をHBM、LPDDR、CXLへ配置した複数のシステムを示す。通常GPUの演算性能を増やすのではなく、重みの近くで積和を行うことで外部バスを跨ぐバイト数を減らす設計である。

資料はHBM-PIMを備えたアクセラレータ、端末向けLPDDR-PIM、大容量モデル向けCXL-PNMまで同じメモリ中心設計を拡張する。PIM/PNMが常にGPUより高速という結果ではなく、容量、通信、電力まで含めた配置交換条件を示す点が重要である。

## 問題設定

通常GPUでは重みをHBMから演算器へ運ぶ。プリフィルは複数トークンをまとめた行列・行列積が多く計算器を使いやすいが、復号は1トークンずつ処理するため行列・ベクトル積となり、重み読出し量に対して演算量が少ない。したがってピーク演算性能を増やしてもHBM帯域が先に飽和する。

メモリ内処理はDRAMバンク近傍に演算器を置き、重みを外部バスへ出さず積和を処理する。メモリ近傍処理はCXLメモリ装置の近くへ演算を置き、大容量メモリとデータ移動削減を組み合わせる。どちらもモデルの計算量自体を減らすのではなく、メモリ階層を跨ぐデータ移動を減らす。

## 手法

### HBM-PIM

多頭注意とフィードフォワードの線形層で発生する行列・ベクトル積をHBM-PIMへ移す。入力ベクトルをPIMへ渡し、バンクへ分散配置した重みとの積和をメモリ側で行い、縮約結果をGPUへ戻す。生成トークンが増えて行列・ベクトル積の比率が上がるほど、重みを外部へ繰り返し運ばない効果が大きくなる。

主演算のすべてをPIMへ移すわけではない。計算密度の高い処理やPIM非対応演算はGPU側に残し、メモリ律速部分を選んでオフロードする。この分業によりGPU演算器とPIM内部帯域を併用するが、対応演算の制約とデータ受渡しが追加費用になる。

### PIMクラスタ

単一カードだけでなく、複数PIM装置をクラスタへ拡張する。混合専門家モデルでは各トークンが一部専門家だけを使うため、専門家重みの配置と通信が重要になる。PIM側へメモリ律速演算を寄せてもノード間通信は残るため、クラスタ評価は単体PIMの帯域改善だけでなく分散時の交換条件を確認する。

### LPDDR-PIM

LPDDR-PIMではバンク近傍へSIMD浮動小数点演算器とレジスタを置き、BLAS1/BLAS2型のメモリ律速演算を対象とする。LPDDRはHBMより低消費電力で端末に適するが、絶対帯域も異なる。PIMによってバンク内部並列性を直接使い、CPU/GPUとの往復を減らすことが狙いである。

### CXL-PNM

CXL-PNMは大容量メモリ拡張と近傍演算を組み合わせ、GPUメモリへ全モデルを収める必要を減らす。単一装置の演算性能だけでなく、複数装置へ大容量モデルを保持し、GPU間にモデルを細かく分割した際の通信を避けることが価値になる。容量制約が強いLLMほどこの効果が重要になる。

## 評価

| 構成 | 主な評価観点 | 読み取れること |
|---|---|---|
| HBM-PIM | GPT系生成 | 復号の行列・ベクトル積をメモリ側へ寄せることで速度とエネルギー効率を改善 |
| PIMクラスタ | 混合専門家モデル | 単体帯域だけでなく専門家配置とノード間通信を含む交換条件を評価 |
| LPDDR-PIM | 端末Transformer | 低電力メモリで外部I/O削減の効果を評価し、一部はシミュレーション |
| CXL-PNM | 大容量LLM | 単体性能より容量とGPU間通信回避が重要になる条件を評価 |

HBM-PIMの生成結果は、出力長が長く行列・ベクトル積を繰り返す条件でメモリ側演算が効くことを示す。速度とエネルギーの双方が改善し得るのは、外部データ移動を減らしてGPU側の待ちとI/O電力を同時に減らすためである。

CXL-PNMは単一装置のピーク性能だけでGPUを上回ることを目的としていない。複数装置と大容量モデルの条件では、モデルをPNM側へ保持してGPU間通信を避ける効果が支配的になり得る。この点はHBM-PIMとCXL-PNMで最適化対象が異なることを示す。

資料は実機測定、クラスタ測定、シミュレーションを混在させているため、各数値の評価形態を分けて解釈する必要がある。特にLPDDR-PIMやCXL-PNMの一部結果を、すべて製品実機で得られた結果として扱ってはいけない。

## 既存研究との差

一般GPUは高い演算性能とHBM帯域を持つが、復号の重み転送は依然として帯域律速になり得る。本報告は同じ演算をより高速なGPUへ移すのではなく、HBM、LPDDR、CXLという異なるメモリ階層ごとに演算をデータ側へ寄せる。端末、単体アクセラレータ、クラスタ、大容量CXLまで同一のデータ移動削減原理を展開している点が特徴である。

## 限界

PIM/PNMで高速化しやすいのは行列・ベクトル積などメモリ律速演算であり、計算律速の行列・行列積や対応外演算はGPU等へ残る。専用メモリ装置とソフトウェアスタックが必要で、一般GPUだけで再現できない。LPDDR-PIMやCXL-PNMにはシミュレーション評価が含まれ、製品実機で同じ絶対性能が保証されるわけではない。容量・通信・電力を含めて初めて有利になる構成がある。