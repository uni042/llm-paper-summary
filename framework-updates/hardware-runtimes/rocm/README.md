# ROCm

ROCm Core SDK、RCCL、AITER、Composable Kernelのうち、LLM推論・学習へ直接関係する主要更新を継続的に記録する集約ページ。GPU実行runtime、集合通信、MoE / attention kernel、低bit計算、storage→GPU転送などを扱う。

## 現在できること

- HIPでAMD GPU上のcompute kernelを実行し、PyTorch等の上位frameworkからCUDAに近いprogramming modelでAMD GPUを利用できる。
- RCCLでAllReduce、AllGather、Reduce-Scatter、All-to-All等のmulti-GPU集合通信を行い、data / tensor / expert parallelismを支えられる。
- AITERとComposable Kernelでattention、GEMM、MoE、quantization、paged KV等のLLM向け専用kernelを利用できる。
- FP8 / FP4等の低bit weight・activation・KVを扱い、memory trafficと保存容量を削減できる。
- HIP Graphで繰り返すkernel列を再利用し、decodeやtraining stepのCPU launch overheadを減らせる。
- 対応環境ではstorage→GPU direct transferを使い、checkpoint / offload dataをCPU DRAM経由せずGPUへ移すdata pathを構成できる。

以下の更新履歴は、**集合通信、low-bit MoE、paged / compressed KV、sparse attention、Graph実行、storage I/O**の主要改善を記録している。

## 初期収録期間

2026-06-03〜2026-09-03

## GA / release済み

### 2026-07-16 — ROCm Core SDK 7.14.0

- **HIP execution contextによるCU分割**: GPUのCU（Compute Unit; NVIDIAのSMに相当する演算unit）を複数workloadへ分けて使う実行contextを追加。推論・通信・別kernelを同一GPU上で干渉を抑えながら共存させる基盤になる。

- **batch async memory API**: 複数のmemory copy / allocation関連操作をまとめて非同期発行し、CPU側API呼び出しと同期overheadを減らす。

- **HIP Graph replay改善**: 一度captureしたGPU kernel列を繰り返し再生するGraph実行pathを改善し、tokenごとに同じkernel列が走るdecode workloadでCPU launch overheadを下げやすくする。

- **hipFile storage→GPU direct transfer**: storageからCPU DRAMへ一度copyしてからGPUへ送る代わりに、対応環境ではstorageとGPU memory間のdirect data pathを使えるようにする。NVMe offload / checkpoint load等でCPU memory bandwidth消費を減らせる。

- **RCCL hierarchical AllGather**: node内の高速linkとnode間networkを別段階として使い、分割parameter等を全GPUへ集めるAllGatherをtopologyに合わせて実行。

- **direct Reduce-Scatter**: gradient等を合算しつつ各GPUへshardするReduce-Scatterのcopy / stagingを減らす。

- **Copy Engine collective**: GPU compute unitだけでなく専用copy engineを集合通信へ利用し、computeと通信を重ねやすくする。

release noteには比較可能なend-to-end LLM性能値なし。[release](https://github.com/ROCm/legacy-rocm-build/releases/tag/rocm-7.14.0)

### 2026-07-27〜09-02 — AITER v0.1.19〜0.1.21

AITERはAMD GPU向けにattention、MoE、GEMM、quantization等のLLM kernelを提供するlibrary。この期間は以下を追加。

- **low-bit MoE**: FP8 / FP4等のexpert weight / activationを展開せず低bitのままmatrix multiplyする経路。
- **fused route / quant / scatter**: MoE routing後のtoken選択、activation量子化、expert GPU向け並べ替えを別々のkernelにせずまとめて実行。
- **FP4 KV compression**: KV cacheを4-bit形式へ圧縮してcontextあたりmemoryと転送量を削減。
- **paged MQA**: MQA（Multi-Query Attention）用KVをpage単位で管理し、長さの異なるrequest間のmemory断片化を抑える。
- **sparse MLA backward**: MLA（Multi-head Latent Attention）の学習時backwardで、選択された一部のKV / latent位置だけに勾配計算を行うsparse path。
- **MXFP8 passthrough fused MoE**: expert-parallel通信前後でFP8 activationを不要にdequantize→requantizeせず、そのまま次kernelへ渡す。

[v0.1.19](https://github.com/ROCm/aiter/releases/tag/v0.1.19) [v0.1.20](https://github.com/ROCm/aiter/releases/tag/v0.1.20) [v0.1.21](https://github.com/ROCm/aiter/releases/tag/v0.1.21)

### AITER #4307（merged）— FP4 MoE decode GEMM2

MoE expert MLPの2段目matrix multiplyを、1 stepでexpertへ届くtoken数の範囲（token bucket）ごとに専用kernelへ分けて最適化。

MI355Xでbucketにより **5〜22% kernel改善**、vLLM end-to-endでは **2.4%向上**。[PR #4307](https://github.com/ROCm/aiter/pull/4307)

### AITER #4954（merged）— MXFP8 activation再量子化の削減

expert parallelism（EP）のAll-to-All後もactivation自体は同じMXFP8値を使えるのに、従来は受信側layoutに合わせて一度再量子化する処理が入る場合があった。

このPRは数値本体を再変換せず、**scale metadataだけを新しいtoken配置へ並べ替える**。DeepSeek-V4-Pro TP8 / DP8 / EP8でthroughput **6.4〜9.8%向上**、TPOT **6.2〜9.3%改善**。[PR #4954](https://github.com/ROCm/aiter/pull/4954)

### AITER #4766（merged）— sparse MLA training backward

MLA trainingのbackwardで全context位置へdenseに勾配を計算せず、sparse attentionで実際に選択されたtop-k位置だけ処理するkernelを追加。

MI355X、T=4096 / top-k=1024で **5.261 ms、522 TFLOPS**。[PR #4766](https://github.com/ROCm/aiter/pull/4766)

### AITER #4804（merged）— gfx1250 BF16 GEMM

gfx1250 architecture向けにBF16 GEMM kernelを専用化し、汎用kernelでは使い切れなかったtile shape・wave schedulingを調整。120 shapesのkernel time幾何平均で **6.82倍**。[PR #4804](https://github.com/ROCm/aiter/pull/4804)

## 未マージ

### Composable Kernel #3760 / AITER #4388（Draft）

**2048-token単位の大pageをpaged KVから直接読むattention kernel案。**

通常はKV pageをattention kernelが扱いやすい小blockへ詰め直す場合があるが、この案は大きいpage layoutをそのまま処理し、中間copy / repackを避ける。

MI250X BF16 MQAで、128K context **141.54 → 83.24 ms**、256K **284.62 → 168.19 ms**。ただしDraft段階のためGA（General Availability; 正式提供）性能としては扱わない。[CK #3760](https://github.com/ROCm/composable_kernel/pull/3760) [AITER #4388](https://github.com/ROCm/aiter/pull/4388)

### 用語メモ

- **HIP**: AMD GPU向けのCUDAに近いGPU programming runtime / API。
- **RCCL**: AMD GPU向け集合通信library。NCCLに相当し、AllReduce / AllGather / All-to-All等を提供する。
- **AITER**: AMD GPU向けLLM kernel library。attention、MoE、quantization等の高性能kernelを提供する。
- **Composable Kernel**: AMD向けにGEMM / attention等をtemplate化して生成・最適化するkernel library。
- **passthrough**: 低精度dataを中間で高精度へ戻さず、その表現のまま次処理へ渡すこと。
