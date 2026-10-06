---
canonical_id: "DOI:10.1109/ACCESS.2024.3409745"
title: "Measuring and Improving the Energy Efficiency of Large Language Models Inference"
summary: "本研究はCPU・DRAM・GPU・storageの消費energyをsoftwareから測るEnergyMeterを実装し、Pythia/BLOOM/Dolly等のLLM推論でmodel size、layer構成、batch、量子化がenergy/tokenとlatencyへ与える影響を実測する。batch拡大はGPU飽和までenergy/tokenを最大20倍改善し、量子化は条件によりenergyを最大約2倍、latencyを3倍超改善する一方、latencyだけではenergyを推定できないことを示す。"
list_summary: "EnergyMeterでLLM推論のCPU/GPU/DRAM/storage消費を分解計測し、batch・量子化・architectureがenergy/tokenとlatencyへ与える実測則を整理する。"
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
---
## 概要
LLM推論の最適化ではlatencyやthroughputが中心になりやすいが、短時間で高電力を使う構成と、低電力でも長時間かかる構成は同じenergyにならない。本研究は推論energyをCPU、memory、GPU、storageへ分解して測るEnergyMeterを作り、model構造、batch size、量子化を変えた実測からenergy効率の条件を整理する。

## 手法
CPUはIntel RAPLの累積joule counterを開始・終了時に読み、GPUはpyNVML経由で既定500ms間隔のpower drawをsamplingして時間積分する。storageもLinux上のsoftware計測を組み込み、単なるwall outletの総電力ではなくcomponent別寄与を追えるようにする。

この計測器でHugging Face Transformersの複数model familyを同一推論workflowへ載せる。model sizeだけでなくlayer数、attention/FFN並列性、batch、weight quantizationを独立に変え、jouleとlatencyをtoken単位で比較する。

## 評価条件
|項目|内容|
|---|---|
|model|Pythia 70M～6.9B、BLOOM、Dolly v2、OpenLLaMA等|
|runtime|PyTorch / Hugging Face Transformers|
|計測|Intel RAPL、pyNVML、memory/storage software meter|
|操作変数|parameter数、layer構成、batch size、quantization|
|指標|J/token、latency/token、GPU utilization|

## 主要結果
parameter数とenergyは概ね増加するが単純比例ではない。Pythia-2.8Bは1.4Bよりenergyが37%以上高い一方latency差は3.5%に留まる例があり、latencyをenergyの代理指標にできない。同程度の3B model間でも最も非効率なmodelは最も効率的なBLOOM 3Bよりenergyが47%、latencyが83%高い。

batch sizeを増やすとGPUの並列度が上がり、GPUが飽和するまでrequest/token当たりenergyが大きく下がる。実験範囲では最大20倍のenergy削減を観測する。量子化もmemory trafficと演算を減らし、条件によってenergy効率を最大約2倍、latencyを3倍超改善するが、bit数を下げ続ければ必ず改善するわけではなく実装効率で頭打ちになる。

## 既存研究との差
training時のcarbon/energy測定ではなく、繰り返し実行されるinferenceをcomponent別に測り、serving knobであるbatchとquantizationへ結び付ける。単一のmodel FLOPsからenergyを推定せず、architectureの並列性が同parameter数でも実測差を生むことを示す。

## 限界
RAPLは主にIntel bare-metalへ依存し、GPU powerはsampling近似である。accuracyは研究の主評価外で、量子化による品質低下とのPareto最適化は行っていない。古い世代のmodel/runtimeを含むため、FlashAttentionやmodern continuous batching環境で絶対値は再測定が必要だが、「GPU飽和までbatch効率が上がる」「latencyとenergyは同値でない」というsystem観測は有用である。