---
canonical_id: "arXiv:2606.15652"
title: "MosaicQuant: Inlier-Outlier Disaggregation for Unified 4-Bit LLM Quantization"
summary: "MosaicQuantはweight全体をdense 4-bit baseへ量子化し、outlier量子化誤差だけをsparse 4-bit residualで補償することでmixed precisionを避ける。ZipperEngineがdense GEMMとsparse residualを同一4-bit pipelineへ融合し、LLaMA3/Qwen3でFP16近傍の精度を維持しつつW16A16比最大1.24倍の推論高速化を得る。"
list_summary: "outlierを高精度に残さず4-bit sparse residualへ分離し、密/sparse演算を融合カーネルで重ねてuniformな4-bit LLM推論を実現する。"
authors: ["Yangjia Hu","Haodong Wang","Zicong Hong","Qianli Liu","Quanxin Shou","Jian Lin","Song Guo","Xiaowei Shen","Xiangjun Huang","Dian Wang","Jian Yang"]
published: "2026-06-14"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2606.15652"
sources: ["https://arxiv.org/abs/2606.15652"]
implementation: "LLaMA3とQwen3で4-bit weight/activation量子化を評価し、ZipperEngineの融合4-bit GEMM kernelでend-to-end inference speedを測定。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2606.15652"
arxiv_categories: {primary: "cs.LG", cross_list: []}
worker_completed_at: "2026-10-06T11:57:00+09:00"
worker_run_key: "20261006-1130-scheduled-chat-30/r02"
last_audited: null
audit_version: 0
---
## 概要
4-bit量子化はメモリ 通信量と演算量を下げられるが、通常値（inlier）と少数の大振幅値（outlier）を同じ狭い表現範囲へ押し込むと精度が落ちる。既存mixed-precision方式はoutlierだけFP16/8bitへ残すが、precision変換や別カーネル、追加data 転送により低bit実行の速度利得を削る。MosaicQuantはoutlierも4bitのまま扱う。

## 手法
重み matrix全体を密 4-bit baseへ量子化する。inlierはこのbaseで十分表現し、outlierによって大きくなった量子化誤差は、誤差寄与が大きいブロックだけを選んだsparse 4-bit residualとして別に保持する。高精度outlier matrixを作らないため表現は4bitへ統一される。

ただし密 カーネルの後にsparse カーネルを別実行すると起動/data 転送 オーバーヘッドが残る。ZipperEngineはsparse ブロック計算を密 4-bit GEMMのパイプラインへ融合し、密 tile処理とresidual処理を重畳する。表現だけでなくexecution pathも低bitへ統一するのがシステム上の要点である。

## 評価条件
|項目|条件|
|---|---|
|モデル|LLaMA3、Qwen3系列|
|量子化|統一4-bit base + sparse 4-bit residual|
|比較|W16A16、既存4-bit/mixed-precision方式|
|実装|ZipperEngine fused カーネル|
|指標|パープレキシティ/タスク精度、カーネル/エンドツーエンド速度|

## 主要結果
FP16に近い品質を維持しつつ、W16A16 比較対象比で最大1.24倍の推論高速化倍率を報告する。重要なのはmixed precisionでaccuracyを救うのではなく、補償成分も4bitへ揃えてprecision conversionを排除した点である。

誤差が全重みへ均等に分布するのではなく、少数のerror-critical ブロックへ集中する観測を使うため、residualをsparseに保てる。ZipperEngineにより別sparse カーネルを逐次実行する場合のオーバーヘッドも抑える。

## 既存研究との差・限界
AWQ/GPTQ系のuniform低bit化と、outlierを高精度へ逃がすmixed-precision方式の中間ではなく、baseとresidualの双方を4bitにする別設計である。最大1.24倍はW16A16との比較であり、成熟した別4-bit カーネルに対する固定倍率ではない。sparse residual密度とハードウェアの4-bit supportによって実利は変わる。