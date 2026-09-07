# Accelerate

Accelerateの主要な機能・性能更新を継続的に記録する集約ページ。分散学習、CPUへの状態退避（CPU offload）、FSDP、DeepSpeed連携、compileなど、複数GPU / CPUを使う学習実行基盤の変更を扱う。

## 現在できること

- 通常のPyTorch training loopを大きく書き換えず、single CPU / GPU、multi-GPU、TPU、multi-nodeへ同じcodeを展開できる。
- DDP、FSDP、DeepSpeedなどの分散学習backendを共通のlauncher / configurationから利用できる。
- FP16 / BF16 / FP8などのmixed precision、gradient accumulation、device placement、checkpoint保存・再開を統一的に扱える。
- 大きなmodelのinferenceでは、weightを複数GPU・CPU DRAM・diskへ配置するdevice mapとCPU / disk offloadを使い、単一GPU memoryを超えるmodelをloadできる。
- notebook、MPI multi-CPU、cluster launcherなど実行環境差を吸収し、既存PyTorch codeの分散化を薄い抽象化で行える。

以下の更新履歴は、これらの機能のうち**FSDP、低精度学習、compile、CPU offload、CPU分散実行**が最近どう拡張されたかを記録している。

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
