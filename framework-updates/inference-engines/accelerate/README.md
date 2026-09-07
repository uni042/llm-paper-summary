# Accelerate

Accelerateの主要な機能・性能更新を継続的に記録する集約ページ。分散学習、CPUへの状態退避（CPU offload）、FSDP、DeepSpeed連携、compileなど、複数GPU / CPUを使う学習実行基盤の変更を扱う。

## 現在できること

- **既存PyTorch codeの分散化**: 通常のPyTorch training loopを大きく書き換えず、single CPU / GPU、multi-GPU、TPU、multi-nodeへ同じcodeを展開できる。device移動、process起動、gradient同期など環境依存処理を`Accelerator`側へまとめるため、local実験からcluster実行へ移るときのcode差分を小さくできる。
- **複数の分散backendを共通設定で利用**: DDP、FSDP、DeepSpeedなどをlauncher / configurationから選択できる。model codeをbackendごとに別実装へ分岐させず、parameter shardingやoptimizer offloadなどbackend固有機能を利用しやすい。
- **mixed precisionとtraining loop管理**: FP16 / BF16 / FP8などのmixed precision、gradient accumulation、gradient clipping、device placementを共通interfaceで扱える。数値精度とmemory / throughputのtrade-offをhardwareに合わせて変更しやすい。
- **checkpoint保存・再開**: modelだけでなくoptimizer、scheduler、random stateなどtraining再開に必要な状態をまとめて保存・復元できる。multi-process trainingでもrankごとの状態管理を利用者側で個別実装する負担を減らす。
- **大規模modelのdevice map配置**: inferenceではlayer / moduleごとにGPU、CPU DRAM、diskへweightを配置し、単一GPUのVRAMを超えるmodelをloadできる。利用可能memoryから自動配置を作ることも、利用者がdevice mapを指定することもできる。
- **CPU / disk offload**: 常時GPUへ置く必要がないweightやstateをCPU DRAM、さらにdiskへ退避し、必要なlayerだけGPUへ移す構成を取れる。VRAM節約と引き換えにPCIeやstorage I/Oがlatencyへ効くため、速度より「modelを載せられること」を優先する用途で有効。
- **FSDP / DeepSpeedとの大規模学習連携**: parameter・gradient・optimizer stateのsharding、CPU offload、ZeRO等をAccelerateの設定から有効化できる。Accelerate自身がすべての低level kernelを持つのではなく、各backendの主要機能を薄い統合層から利用する位置づけ。
- **compileとの併用**: PyTorch compileやregional compilationを分散trainingと組み合わせ、同形状のTransformer blockでcompile結果を再利用できる。初回compile costやPython / kernel launch overheadを減らす方向の最適化に使える。
- **多様な実行環境の吸収**: notebook、MPI multi-CPU、SLURM等のcluster、通常のcommand line launcherを同じ設定系へ寄せられる。特に研究codeを環境ごとに書き換えず再利用したい場合に強い。

以下の更新履歴は、これらの主要能力について**どの分散backend・精度・offload構成まで共通interfaceから使えるようになったか、初回compileやCPU/GPU memory制約をどこまで減らせるようになったか**を追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-19 — v1.8.0（released）

- **FSDP2 FP8 training**: FSDP2（Fully Sharded Data Parallel 2; model parameter・gradient・optimizer stateをGPU間へ分割保持する学習方式）でFP8学習を扱えるようにした。大きなmodel stateを各GPUへ完全複製せず、低精度演算も組み合わせてmemoryと計算量を抑える方向の更新。

- **DeepSpeed regional compilation**: Transformerの同じ形をしたdecoder blockをlayerごとに別々にcompileするのではなく、共通部分のcompile結果を再利用する。model全体の初回compile costを抑える目的。

- **CPU offload**: GPUへ置く必要がない学習stateをCPU DRAMへ退避し、GPU memory不足を緩和する実行経路を追加・強化。

- **Intel CPU distributed training tuning**: CCL（oneAPI Collective Communications Library; Intel向け集合通信）とKMP/OpenMP thread設定を調整し、4th Gen Xeon上のTransformer tensor-parallel trainingで最大 **40%向上**を報告。

個別のFSDP2 FP8 / regional compilation / CPU offloadについて独立benchmarkはrelease noteに掲載されていないため、「新機能が利用可能になったこと」と「Intel CPU分散学習には測定値があること」を分けて読む必要がある。

[releases](https://github.com/huggingface/accelerate/releases)

v1.8.1には、掲載基準を満たす独立した新規性能・memory機能を確認できなかった。

### 用語メモ

- **FSDP（Fully Sharded Data Parallel; 完全分割データ並列）**: model weight、gradient、optimizer stateをGPU間へ分散し、各GPUが全状態を持たなくて済むようにする方式。
- **tensor parallelism（テンソル並列）**: 1つの大きなmatrix計算を複数GPUへ分割する方式。
- **CPU offload**: GPU memory節約のため、parameterやoptimizer stateなどをCPU DRAMへ置き、必要時だけGPUへ戻す方式。
