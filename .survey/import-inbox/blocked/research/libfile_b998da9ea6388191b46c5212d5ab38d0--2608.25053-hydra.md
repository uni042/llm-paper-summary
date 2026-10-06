---
canonical_id: "arXiv:2608.25053"
title: "Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels"
summary: "Hydraはedge SoC上のLLM推論をprefill/decodeへ分け、HuggingFace Transformersとllama.cppの共通prompt timing schemaをhardware telemetryと結合する計測基盤である。AGX Xavier/Orin/Thor、7 family・13 instruction-tuned LLM、5 execution formatを約107K prompt recordで比較し、backend、量子化、SoC世代、入出力長がlatency・memory traffic・power・energyへ与える影響を分離して示す。"
list_summary: "プリフィル/デコード別のtimingとSoC telemetryを統合し、edge LLMのbackend・量子化・ハードウェア世代・系列長の性能/energy差を再現可能に比較する。"
authors: ["Amir Taherin","Sana Taghipour Anvari","Charles Amante","Yixiao Chen","Ruben Noroian","Zlatan Feric","Nicolas Bohm Agostini","Pu Zhao","José Cano","Bin Ren","Yanzhi Wang","David Kaeli"]
published: "2026-08-25"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2608.25053"
sources: ["https://arxiv.org/abs/2608.25053","https://github.com/amirtaherin/hydra"]
implementation: "HuggingFace Transformersとllama.cppを同一schemaで計測し、Jetson AGX Xavier/Orin/Thorのtelemetryを統合。約107K per-prompt recordと実装を公式repositoryで公開。"
code: "https://github.com/amirtaherin/hydra"
last_checked: "2026-10-06"
arxiv_id: "2608.25053"
arxiv_categories:
  primary: "cs.AR"
  cross_list: []
worker_completed_at: "2026-10-06T20:29:00+09:00"
worker_run_key: "20261006-2000-scheduled-chat-00/r01"
reference_main_sha: "d53224842a1f044cfc1d642e6a55c7bd8d266c48"
last_audited: null
audit_version: 0
---

## 概要
edge端末のLLM推論は、モデル サイズやbit幅だけでは性能を予測できない。プリフィルは複数トークンをまとめて処理して計算律速になりやすい一方、デコードは1 トークンずつ進みメモリ 通信量やランタイム オーバーヘッドの影響を受ける。さらにHuggingFace Transformersとllama.cppでは演算子構成が異なり、同じモデル/ハードウェアでも時間の使われ方が変わる。

Hydraは両backendへ共通のper-プロンプト timing schemaを入れ、プリフィル/デコード時間とSoCの資源/power telemetryを同じrecordへ結合する。AGX Xavier、Orin、Thorの3世代、7 familyの13 instruction-tuned LLM、5 execution formatを測り、約107K recordを公開する。目的は新しい高速化方式ではなく、edge inferenceのボトルネックを局面単位で再現可能に比較することにある。

## 問題設定
エンドツーエンド 遅延だけを見ると、プリフィル短縮とデコード悪化、GPU利用率改善とCPU オーバーヘッド増加、power上昇とenergy/トークン改善など異なる現象が同じ総時間へ畳み込まれる。量子化もメモリ 通信量を減らすが、dequantizationやbackend固有カーネルによって瞬間powerが単調に下がるとは限らない。

ハードウェア世代比較でもpeak computeだけでは不十分である。新しいSoCは絶対powerが高くてもトークン当たりenergyを下げられる場合があり、旧世代と同じutilization値を同じ意味として扱えない。

## 手法
### 共通prompt schema
Transformersとllama.cppの各リクエストからプロンプト条件、プリフィル、デコード、生成長などを共通形式で記録する。backend固有のlogを後処理で無理に揃えるのではなく、局面 boundaryを明示して同じ分析軸へ載せる。

### Hardware telemetry融合
CPU/GPU利用率、メモリ 通信量、power等の時系列telemetryをプロンプト recordへ対応付ける。これにより「遅い」だけでなく、compute、メモリ、software オーバーヘッドのどこで時間とenergyを消費したかを追う。

### 多次元sweep
SoC世代、モデル family/サイズ、execution format、backend、入力/出力 lengthを変えて同一schemaへ蓄積する。単一モデルのベンチマークではなく、条件間interactionを分析できるdatasetを作ること自体が成果である。

## 評価条件
|項目|内容|
|---|---|
|SoC|NVIDIA Jetson AGX Xavier、AGX Orin、AGX Thor|
|モデル|7 family、13 instruction-tuned LLM|
|backend|HuggingFace Transformers、llama.cpp|
|形式|5 execution format/precision構成|
|系列長|入力/出力 lengthを独立に変化|
|規模|約107K per-プロンプト records|

## 主要結果
集約遅延だけではbackend差を説明できず、局面別に見るとランタイム構造が遅延の発生箇所を変える。量子化はメモリ 通信量と総energyを概ね減らすが、power drawはbit幅に対して単調ではないため、「低bitなら常に低power」という単純な推定は成立しない。

系列長感度では、入力を1Kから5K トークンへ増やした場合の総energy増加が11〜34%なのに対し、出力を1Kから5Kへ増やすと5倍超になる条件を報告する。デコードの反復回数がedge energyへ強く効くことを示す。新世代SoCはpeak powerだけでなくenergy/トークンで評価すべきという結果も得る。

## 既存研究との差
通常のLLM ベンチマークはトークン/sや総遅延を中心に比較する。Hydraは局面 timingとハードウェア telemetryを同一プロンプトへ結合し、backend・precision・ハードウェア世代を横断して同じschemaで比較する点が異なる。さらにトレース corpusを公開し、後続のスケジューラ/energy policy研究へ入力できる。

## 限界
対象はJetson AGX 3世代であり、desktop GPU、mobile NPU、Apple Silicon等へ直接一般化できない。計測フレームワークは性能を自動最適化するものではなく、観測結果から最適backend/precisionを選ぶpolicyは別途必要である。約107K recordは広いが、全モデル・全文脈長を網羅するものではない。

## 一次資料
- https://arxiv.org/abs/2608.25053
- https://github.com/amirtaherin/hydra