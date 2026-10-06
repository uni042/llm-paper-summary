---
canonical_id: "DOI:10.1109/ACCESS.2024.3409745"
title: "Measuring and Improving the Energy Efficiency of Large Language Models Inference"
summary: "本研究はCPU・DRAM・GPU・storageの消費energyをsoftwareから測るEnergyMeterを実装し、Pythia/BLOOM/Dolly等のLLM推論でmodel size、layer構成、batch、量子化がenergy/tokenとlatencyへ与える影響を実測する。batch拡大はGPU飽和までenergy/tokenを最大20倍改善し、量子化は条件によりenergyを最大約2倍、latencyを3倍超改善する一方、latencyだけではenergyを推定できないことを示す。"
list_summary: "EnergyMeterでLLM推論のCPU/GPU/DRAM/ストレージ消費を分解計測し、バッチ・量子化・構成がenergy/トークンと遅延へ与える実測則を整理する。"
authors: ["Mauricio Fadel Argerich","Marta Patiño-Martínez"]
published: "2024-06-05"
publication: "IEEE Access"
publication_type: "journal"
publication_status: "published"
source: "https://doi.org/10.1109/ACCESS.2024.3409745"
sources: ["https://doi.org/10.1109/ACCESS.2024.3409745"]
implementation: "EnergyMeterをPythonで実装し、Intel RAPL、pyNVML等を用いてCPU/memory/GPU/storage energyを計測。Hugging Face Transformers上のPythia、BLOOM、Dolly v2等で推論を実測。"
code: null
last_checked: "2026-10-06"
worker_completed_at: "2026-10-06T13:58:00+09:00"
worker_run_key: "20261006-1330-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
LLM推論の最適化では遅延やスループットが中心になりやすいが、短時間で高電力を使う構成と、低電力でも長時間かかる構成は同じenergyにならない。本研究は推論energyをCPU、メモリ、GPU、ストレージへ分解して測るEnergyMeterを作り、モデル構造、バッチ サイズ、量子化を変えた実測からenergy効率の条件を整理する。

## 手法
CPUはIntel RAPLの累積joule counterを開始・終了時に読み、GPUはpyNVML経由で既定500ms間隔のpower drawをsamplingして時間積分する。ストレージもLinux上のsoftware計測を組み込み、単なるwall outletの総電力ではなく構成要素別寄与を追えるようにする。

この計測器でHugging Face Transformersの複数モデル familyを同一推論workflowへ載せる。モデル サイズだけでなく層数、注意機構/FFN並列性、バッチ、重み 量子化を独立に変え、jouleと遅延をトークン単位で比較する。

## 評価条件
|項目|内容|
|---|---|
|モデル|Pythia 70M～6.9B、BLOOM、Dolly v2、OpenLLaMA等|
|ランタイム|PyTorch / Hugging Face Transformers|
|計測|Intel RAPL、pyNVML、メモリ/ストレージ software meter|
|操作変数|パラメータ数、層構成、バッチ サイズ、量子化|
|指標|J/トークン、遅延/トークン、GPU utilization|

## 主要結果
パラメータ数とenergyは概ね増加するが単純比例ではない。Pythia-2.8Bは1.4Bよりenergyが37%以上高い一方遅延差は3.5%に留まる例があり、遅延をenergyの代理指標にできない。同程度の3B モデル間でも最も非効率なモデルは最も効率的なBLOOM 3Bよりenergyが47%、遅延が83%高い。

バッチ サイズを増やすとGPUの並列度が上がり、GPUが飽和するまでリクエスト/トークン当たりenergyが大きく下がる。実験範囲では最大20倍のenergy削減を観測する。量子化もメモリ 通信量と演算を減らし、条件によってenergy効率を最大約2倍、遅延を3倍超改善するが、bit数を下げ続ければ必ず改善するわけではなく実装効率で頭打ちになる。

## 既存研究との差
学習時のcarbon/energy測定ではなく、繰り返し実行されるinferenceを構成要素別に測り、推論提供 knobであるバッチと量子化へ結び付ける。単一のモデル FLOPsからenergyを推定せず、構成の並列性が同パラメータ数でも実測差を生むことを示す。

## 限界
RAPLは主にIntel bare-metalへ依存し、GPU powerはsampling近似である。accuracyは研究の主評価外で、量子化による品質低下とのPareto最適化は行っていない。古い世代のモデル/ランタイムを含むため、FlashAttentionやmodern continuous batching環境で絶対値は再測定が必要だが、「GPU飽和までバッチ効率が上がる」「遅延とenergyは同値でない」というシステム観測は有用である。