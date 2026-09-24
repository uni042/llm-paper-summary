# ROCm

ROCm Core SDK、RCCL、AITER、Composable Kernelのうち、LLM推論・学習へ直接関係する主要更新を継続的に記録する集約ページ。GPU実行runtime、集合通信、MoE / attention kernel、低bit計算、storage→GPU転送などを扱う。

## 現在できること

- **AMD GPU上の汎用compute**: HIPでAMD GPU向けkernelを実行し、PyTorch等の上位frameworkからCUDAに近いprogramming modelでAMD GPUを利用できる。LLM frameworkはHIP / ROCm backendを通じて同じmodel codeをAMD hardwareへ持ち込める。
- **device memory管理**: GPU memory allocation、copy、stream、event、async operationを扱い、model weight、activation、KV cache、workspaceをruntime側で配置できる。LLMでは細かいallocationとcopyが頻繁なためasync APIとpool管理が性能へ効く。
- **HIP Graph**: 繰り返すdecode / training kernel列をcaptureして再生し、token / stepごとにCPUから大量のkernelをlaunchするoverheadを減らせる。固定shape / bufferを使うhot pathほど効果が出やすい。
- **GPU resource partitioning**: execution context等でCompute Unitを複数workloadへ分け、同一GPU上で推論、通信、別kernelを干渉を抑えながら共存させる基盤を利用できる。servingでcompute resourceを分ける用途へつながる。
- **multi-GPU集合通信**: RCCLでAllReduce、AllGather、Reduce-Scatter、All-to-All等を実行し、data / tensor / expert parallelismを支えられる。LLM training / servingのdistributed executionで不可欠なdata movement層。
- **topology-aware collective**: node内高速linkとnode間networkを階層的に使い、AllGather等をhardware topologyへ合わせて実行できる。multi-nodeで全通信を同じ経路へ流すよりnetwork bottleneckを抑えられる。
- **computeと通信のoverlap**: Copy Engineや別streamを使い、collective communication / memory copyをmatrix computeと重ねられる。通信量そのものを減らせなくてもGPU idle時間を隠せる。
- **AITERによるLLM専用kernel**: attention、GEMM、MoE、routing、quantization、KV cache等のLLM hot pathをAMD GPU向けに最適化したkernelを利用できる。vLLM等の上位runtimeがbackendとして呼び出せる。
- **Composable Kernel**: GEMM、attention等のtile / layout / precisionをtemplate化し、GPU architectureとtensor shapeに合うkernelを生成・選択できる。汎用kernel1本では性能が出にくいLLM shapeをhardware別に最適化する基盤。
- **low-bit GEMM**: FP8、FP4等のweight / activationを低bitのままmatrix multiplyへ流し、HBM使用量、weight読出し、Tensor / Matrix Core compute costを削減できる。hardware世代ごとの対応precisionが重要。
- **low-bit MoE**: MoE expert weight / activationをFP8 / FP4等で扱い、expert数が多いmodelのHBM footprintとexpert GEMMのmemory trafficを減らせる。
- **fused MoE routing path**: routing、token index整理、activation quantization、scatter等を複数kernelに分けずfusionし、routing後にtokenをexpert GPUへ送るまでのlaunch / HBM trafficを削減できる。
- **expert-parallel passthrough**: All-to-All前後で低bit activationを不要にdequantize→requantizeせず、そのまま通信・次kernelへ渡せる。数値本体の再変換を省き、scale metadataだけを新layoutへ合わせる方式を利用できる。
- **paged KV cache kernel**: requestごとのKVをpage単位で管理し、長さの違うrequestが混在しても大きな連続memoryを予約せずに済む。LLM servingのmemory断片化とcache allocationを抑えられる。
- **low-bit KV compression**: FP4等へKVを圧縮し、長contextで増えるHBM使用量とworker / tier間転送量を削減できる。同じGPU memoryで保持できるtoken数を増やせる。
- **MQA / GQA向けattention**: K/V head共有を前提としたpaged attention kernelを利用し、同じK/Vを不要に複製して読むmemory trafficを減らせる。
- **MLA / sparse attention**: MLAの圧縮latentやsparse top-k位置だけを処理するkernelを利用できる。長contextで全positionへdense attention / backwardを行うcomputeとmemory trafficを減らせる。
- **training backward専用kernel**: sparse MLA backward等、forwardだけでなくgradient計算のhot pathにも専用kernelを持つ。AMD GPUをinferenceだけでなく大規模LLM trainingへ使うための基盤になる。
- **architecture-specific kernel tuning**: gfx系architectureごとにtile shape、wave scheduling、memory layoutを専用化し、汎用kernelでは使い切れないGPU resourceを利用できる。
- **storage→GPU direct transfer**: 対応環境ではcheckpoint / offload dataをCPU DRAMへ一度copyせずstorageからGPU memoryへ移せる。NVMe offload、checkpoint load、large-model startupでCPU memory bandwidthとcopy回数を減らせる。
- **async memory / batched operation**: 複数copy / allocation操作をまとめて非同期発行し、CPU API callと同期回数を削減できる。token単位で細かいdata movementが起こるservingでhost overheadを下げる。
- **PyTorch / serving frameworkのhardware層**: ROCm自身はvLLMのようなrequest schedulerやMegatronのtraining recipeを提供するのではなく、それらがAMD GPU上で使うruntime、collective、kernel、memory / I/O primitiveを提供する位置づけ。

以下の更新履歴は、**LLM frameworkがAMD GPUで利用できる実行primitiveそのものがどう増えたか、通信・低bit・MoE・KV・Graph・storage I/Oのcritical pathをどこまで短くできるか**を追う。

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
