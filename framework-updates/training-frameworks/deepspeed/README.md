# DeepSpeed

DeepSpeedの主要な機能・性能更新を継続的に記録する集約ページ。MoE並列、ZeRO、CPU / NVMe offload、activation offload、CUDA Graph、Triton kernelなど、大規模学習のGPU memoryと通信・待ち時間へ影響する変更を扱う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-16〜07-23 — v0.19.2 / v0.19.3（released）

- **AutoEP**: MoEのexpert parallelism（EP）構成をhardware・expert数・model shapeに合わせて自動選択する機能。利用者が手作業で「何GPUへexpertをどう分けるか」を決める負担を減らす。

- **AutoTP + EP parallel folding**: dense部分で使うtensor parallelism（TP）とMoE部分で使うexpert parallelism（EP）を同じGPU集合へ別mappingで重ねる。attentionとexpertへ同じ並列groupを強制せず、通信量とmemory balanceをmodel構造に合わせる。

[v0.19.2](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.2) [v0.19.3](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.3)

### 2026-08-03 — Triton grouped-GEMM（merged）

MoEでは1 layer内に複数expertの小さなmatrix multiplyが並ぶ。従来はexpertごとにloopしてkernelを起動し、途中でGPU→CPU同期も発生していた。

**grouped-GEMM**は複数expertのGEMM（General Matrix Multiplication; 行列積）を1つの大きなGPU kernelでまとめて処理し、expertごとのkernel launchとdevice→host同期を削減する。

Ampere / Ada GPUで16 expertsのforwardは **0.256 → 0.107 ms**、forward+backwardは **1.093 → 0.589 ms**。[PR #8180](https://github.com/deepspeedai/DeepSpeed/pull/8180)

### 2026-08-06〜08-27 — v0.19.4〜v0.19.6（released）

- **DeepNVMe pinned buffer**: NVMe offload時にGPU転送へ使うCPU側bufferをピン留めメモリ（pinned memory）として再利用し、毎回のallocationやpage lockを減らす。

- **ZeRO-3 asynchronous gradient offload**: ZeRO-3でGPU上にできたgradientをCPUへ非同期に送り、次のGPU計算と転送を重ねる。GPUが全gradient転送完了を待つ時間を減らす。

- **HybridEngine CUDA Graph**: training / inferenceを切り替えるRLHF系HybridEngineで、繰り返し同じshapeのGPU kernel列をCUDA Graphへcaptureし、CPU launch overheadを削減。

- **fused Triton SwiGLU**: SwiGLU activationの複数elementwise処理を1 kernelへまとめ、中間tensor書き戻しとkernel launchを減らす。

[v0.19.4](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.4) [v0.19.5](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.5) [v0.19.6](https://github.com/deepspeedai/DeepSpeed/releases/tag/v0.19.6)

### 2026-08-21 — non-reentrant activation CPU offload（merged）

順伝播で作った活性値（activation）をbackwardまでGPUへ保持せず、CPU DRAMへ非同期退避する機能。

- CPU側に再利用可能なpinned memory poolを確保
- 専用CUDA side streamでGPU→CPU offload / CPU→GPU restoreを進める
- backwardで必要になる前にactivationをGPUへ戻す

ことで、main compute streamを止めにくくする。

H200／Qwen3-8B、16K sequenceではpeak CUDA memory **22.46 → 19.89 GiB**。step timeは **2.0%増**に抑え、同期的にcopyするblocking方式より **1.7倍高速**。[PR #8282](https://github.com/deepspeedai/DeepSpeed/pull/8282)

### 用語メモ

- **ZeRO-3**: parameter、gradient、optimizer stateをGPU間へ分割し、各GPUがmodel全状態を持たなくて済むようにする方式。
- **pinned memory**: OSが別場所へ移動しないよう固定したCPU memory。GPUとのDMA転送を高速化しやすい。
- **side stream**: main GPU計算とは別CUDA streamでcopyなどを走らせ、可能な範囲で計算と重ねる方式。
- **parallel folding**: 同じ物理GPU集合をmodel部分ごとに異なるlogical parallel groupとして使うこと。
