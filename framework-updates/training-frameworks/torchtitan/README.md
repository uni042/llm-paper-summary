# TorchTitan

TorchTitanの主要な機能・性能更新を継続的に記録する集約ページ。PyTorch-nativeな大規模LLM学習で、MoE token dispatcher、通信と計算の重ね合わせ、CUDA Graph、pipeline parallelism、FSDP、activation checkpointing、低精度optimizerなどを扱う。

## 現在できること

- **PyTorch-native大規模training**: PyTorchのmodel codeを中心に保ちながら、FSDP、tensor / pipeline / expert parallelismを組み合わせてmulti-GPU / multi-node trainingを構成できる。
- **dense / MoE両対応**: dense TransformerだけでなくMoEを学習でき、routing後のtokenをexpert GPUへ送るdispatcherを複数backendから選べる。
- **FSDPとparameter sharding**: parameter・gradient・optimizer stateをGPU間へ分割し、data parallel replicaごとの重複memoryを削減できる。
- **communication overlap**: parameter gather、gradient通信、MoE token交換をcomputeと重ね、GPUがnetwork完了を待つ時間を減らせる。
- **activation checkpoint / recomputation**: どのactivationを保持し、どこを再計算するかをpolicyとして構成し、長sequence時のpeak VRAMを下げられる。
- **低精度training**: FP8 / FP4 / BF16 optimizer state等を使い、matrix演算・state保持・通信量を削減できる。数値精度と収束のtrade-offは別途評価が必要。
- **CUDA Graph / whole-step graph**: forward、backward、optimizer周辺まで広い範囲をGraph化し、Python schedulingとkernel launch overheadを減らせる。
- **pipeline schedule最適化**: model layerを複数stageへ分割し、microbatchのforward / backwardを重ねてpipeline bubbleを減らせる。
- **compiler / graph transformation連携**: graph解析からactivation memory、pipeline partition、parallel executionを調整し、手作業のparallel tuningを減らせる。

以下の更新履歴は、**PyTorch-nativeなままどこまでparallelism・MoE通信・graph化・低精度学習を統合できるか**を中心に追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-09-03 — v0.3.0（released）

#### unified token dispatcher

MoE routing後のtokenをexpert GPUへ送る通信層を、

- Standard
- MinimalAsyncEP
- DeepEP
- HybridEP

で別々に扱うのではなく、共通interfaceへ統合した。

**token dispatcher**は、

1. routing結果から送信先expertを決める
2. tokenをGPU間で交換する
3. expert計算後の出力を元token順へ戻す

役割を持つ。

backendを共通化することで、hardware / networkに合わせて通信方式を切り替えつつ、上位model codeを同じまま使いやすくする。

#### communication overlap / CUDA Graph

GPU間通信を完全に待ってから次計算へ進むのではなく、到着したdataから計算を始めるなど、communicationとcomputeを重ねる経路を強化。

また繰り返し同じkernel列をCUDA Graphへcaptureし、CPU launch overheadを減らす。

#### GraphTrainer / GraphPP

- **whole-step graph**: forward、backward、optimizer周辺をより広い単位でgraph化し、1 training step全体のPython / CPU scheduling overheadを減らす。
- **FSDP / EP overlap**: parameter gatherやgradient通信とMoE expert通信を可能な範囲で同時進行させる。
- **activation-memory pass**: graphを解析し、どのactivationがmemoryを多く使うかを基に保持 / recompute policyを決めやすくする。
- **pipeline partition**: model layerを複数pipeline stageへどう分割するかをgraphから決定・調整する。
- **DualPipeV**: forward / backward microbatchを双方向に流し、pipeline bubbleを減らすscheduleを統合。

#### 低精度学習

- **BF16 optimizer state**: 一部optimizer stateをFP32ではなくBF16で保持しmemoryと通信量を減らす。
- **MXFP8 / NVFP4 / Float8**: matrix multiplyやparameter / activationを8-bit / 4-bit系形式で扱い、GPU memory trafficと演算costを削減。

低精度化は単なるlossless runtime optimizationではなく、数値表現が変わるため、精度・収束とのtrade-offを別途確認する必要がある。

#### composable activation-checkpoint policy

activation checkpointingは、forward中間結果をすべて保存せず、一部をbackward時に再計算してGPU memoryを節約する方式。

v0.3.0では「どの層・演算を保存し、どこを再計算するか」を複数policyとして組み合わせやすくした。

#### declarative `spmd_types`

SPMD（Single Program, Multiple Data）は同じprogramを複数GPUで実行し、rankごとに異なるdata shardを処理する分散実行方式。

`spmd_types`はparallelismの役割を宣言的に記述し、model code内へrank判定を散在させずにTP / DP / EP等の分割を構成しやすくする。

release noteには比較可能なthroughput / peak-memory benchmark値がないため、v0.3.0は主に**training architectureの統合・抽象化が進んだrelease**として記録する。

[release](https://github.com/pytorch/torchtitan/releases/tag/v0.3.0)

### 用語メモ

- **FSDP（Fully Sharded Data Parallel; 完全分割データ並列）**: parameter・gradient・optimizer stateをGPU間へ分割する方式。
- **EP（Expert Parallelism; エキスパート並列）**: MoE expertをGPU間へ分散する方式。
- **pipeline bubble**: pipeline stage間の処理時間差や依存関係によってGPUが仕事を待つ空白時間。
- **activation checkpointing**: activation memoryを節約する代わりにbackward時の再計算を増やす方式。
