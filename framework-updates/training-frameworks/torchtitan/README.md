# TorchTitan

TorchTitanの主要な機能・性能更新を継続的に記録する集約ページ。PyTorch-nativeな大規模LLM学習で、MoE token dispatcher、通信と計算の重ね合わせ、CUDA Graph、pipeline parallelism、FSDP、activation checkpointing、低精度optimizerなどを扱う。

## 現在できること

- **PyTorch-nativeな大規模training stack**: PyTorchのmodel / optimizer codeを中心に保ちながら、multi-GPU / multi-node trainingへ拡張できる。専用DSLへmodel全体を書き換えず、PyTorch ecosystemのcompiler・distributed機能を組み合わせることを重視する。
- **FSDPによるstate sharding**: parameter・gradient・optimizer stateをdata-parallel rank間へ分割し、各GPUがmodel stateを完全複製するmemory costを減らせる。大きいmodelをdata parallelで学習する際の基本的なmemory削減手段。
- **tensor parallelism**: 1 layer内の大きなmatrix計算を複数GPUへ分割し、hidden size / FFNが単一GPUに収まりにくいmodelを学習できる。node内高速linkを使う構成と相性がよい。
- **pipeline parallelism**: model layerを複数stageへ分け、異なるmicrobatchのforward / backwardをstage間で重ねられる。model depthを分散しつつ、scheduleによってpipeline bubbleを減らす。
- **expert parallelism / MoE training**: MoE expertをGPU間へ分散し、routingされたtokenを対応expertへ送って戻す。総parameter数の大きいMoEを全GPUへexpert複製せず学習できる。
- **複数parallelismの合成**: FSDP / data parallelism、tensor、pipeline、expert parallelismを組み合わせられる。model size、expert数、cluster topologyに合わせてparallel axesを選べる。
- **unified token dispatcher**: MoE routing後のtoken交換を共通interfaceとして扱い、Standard、MinimalAsyncEP、DeepEP、HybridEP等の通信backendを上位model codeを変えず切り替えられる。
- **communication overlap**: FSDP parameter gather、gradient通信、MoE token交換等をcomputeと重ね、GPUがnetwork完了を待つ時間を減らせる。通信量そのものだけでなくcritical path上の待ち時間を隠す。
- **activation checkpointing / recomputation**: forward中間値をすべて保存せずbackward時に再計算し、長sequenceや大modelのpeak VRAMを下げられる。どのoperator / layerを保存するかpolicyとして組み合わせられる。
- **activation-memory解析**: graphを解析し、どのactivationがmemoryを多く占めるかを見ながらrecompute対象を決める仕組みを使える。単純な「全layer再計算」よりcompute追加を抑えやすい。
- **低精度training**: Float8、MXFP8、NVFP4等でmatrix計算やparameter / activationを低bit化し、HBM trafficとTensor Core compute costを削減できる。数値精度・収束とのtrade-offを確認する必要がある。
- **低精度optimizer state**: optimizer stateの一部をBF16等で保持し、FP32常駐よりmemoryを減らせる。optimizer stateはparameter本体の複数倍になることがあるため大規模modelで効く。
- **CUDA Graph**: 繰り返すforward / backward / optimizer周辺のkernel列をcaptureし、Python / CPUから毎step大量のkernelをlaunchするoverheadを減らせる。
- **whole-step graph**: layer単位ではなくtraining step全体に近い範囲をgraph化し、Python scheduling、dispatcher、optimizer周辺を含むhost overheadを広く削減できる。
- **GraphTrainer / graph transformation**: training graphを解析・変換し、parallelism、activation memory、communication overlapをprogrammaticに調整できる。手作業でmodel codeへ通信やcheckpoint logicを散在させる量を減らす。
- **automatic / assisted pipeline partition**: graph情報を基にmodel layerをpipeline stageへどう分けるか調整できる。各stageのcompute / memoryを均し、遅いstageが全体throughputを制限する問題を減らす。
- **advanced pipeline scheduling**: DualPipeV等でforward / backward microbatchを複数方向に重ね、pipeline bubbleを減らせる。単純な1F1Bよりnetwork / computeの空白時間を抑えることを狙う。
- **declarative SPMD configuration**: `spmd_types`等でrankごとのparallel roleを宣言し、model code内へrank判定やgroup生成を大量に埋め込まずTP / DP / EPを構成しやすい。
- **dense / MoE共通training framework**: dense TransformerとMoEを同じPyTorch-native stackで扱い、model architectureによってtraining infrastructureを全面的に分けずに済む。
- **checkpoint / job restart**: distributed training stateを保存・復元し、長時間jobの再開へ使える。FSDPや複数parallelismを使う場合でもsharded stateを扱うことが前提になる。
- **PyTorch compiler ecosystemとの連携**: `torch.compile`やgraph transformation等をtraining stackへ統合し、PyTorch自体のcompiler改善を大規模LLM trainingへ取り込みやすい。
- **研究用parallelism実験基盤**: 新しいdispatcher、pipeline schedule、low-precision format、Graph変換を比較的PyTorchに近い形で試せるため、production pretrainingだけでなくsystems researchの実装基盤としても使える。

以下の更新履歴は、**PyTorch-nativeなままparallelism、MoE通信、graph化、activation memory、低精度学習をどこまで一体化できるか**を中心に追う。

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
