# MLX

MLXの主要な機能・性能更新を継続的に記録する集約ページ。Apple Silicon向けGPU kernel、統一memory（unified memory）、attention、量子化MoE、CPU↔GPU data共有など、MLX基盤そのものの性能改善を扱う。

## 現在できること

- **Apple Silicon向け汎用array / ML基盤**: NumPyに近いarray APIとPyTorchに近い`mlx.nn` / optimizer APIで、modelの構築・学習・推論を行える。LLM専用runtimeではなく、MLX LMなど上位libraryが使う低level tensor / neural-network基盤。
- **automatic differentiation**: forward計算からgradientを自動構築し、training loopを実装できる。手書きbackwardを避けつつ、custom functionや低level operatorと組み合わせられる。
- **lazy execution**: operationを呼んだ時点ですぐ全tensorを計算せず、結果が必要になるまでgraphとして保持する。複数operationをまとめて最適化したり、不要な中間計算を省いたりできる余地を作る。
- **dynamic graphとcompile**: Pythonの柔軟なmodel codeを保ちながら、繰り返し部分をcompileして実行overheadを減らせる。shapeやcontrol flowによって再compile costが発生するため、固定的なhot pathほど利得が大きい。
- **統一memoryの直接利用**: CPUとGPUが同じphysical memory poolを共有するApple Siliconの構成を前提に、同じarrayをCPU / GPUから参照できる。従来型discrete GPUのような明示的host→device copyを減らせる一方、CPUとGPUは同じmemory bandwidthを奪い合う。
- **zero-copy host data import**: CPU側に既にあるbufferをcopyせずMLX arrayとして参照できる。token buffer、preprocessing結果、外部libraryから渡されたdataなどで不要なmemory duplicationを減らせる。
- **CPU / GPU operation配置**: operationごとにCPUまたはGPUへ配置できるため、GPU向きの大きいmatrix計算とCPU向きの軽い処理を使い分けられる。上位runtime側でdevice placementを組むための基盤になる。
- **量子化matrix演算**: 低bit weightを展開しきらずmatrix multiplyへ使うoperatorを持ち、LLMのweight memoryとmemory trafficを削減できる。量子化形式ごとのscale管理と専用kernelが性能を左右する。
- **attention専用kernel**: full attention、GQA等でscore tensorを完全にmaterializeせずblock単位に計算するkernelを利用できる。長contextでは中間memoryとHBM trafficの削減が大きい。
- **MoE向けoperator**: routingされたexpertだけを処理する量子化matrix multiply等を使い、tokenが届いていないexpertへ不要なGPU workを割り当てない実行ができる。
- **vectorization / batching変換**: 同じfunctionを複数sampleへ自動的にvectorizeする仕組みを使い、Python loopを減らしてdevice上の並列計算へ変換できる。
- **distributed computationの基盤**: 上位MLX ecosystemから複数device / hostを使う分散実行へ接続できる。MLX自体はtensor・通信・graph実行の土台であり、LLM固有schedulerやserving APIは上位libraryが担う。
- **LLM以外の上位workload**: image generation、speech、vision等でも同じtensor / kernel基盤を利用できるため、multimodal pipeline内で複数modelをApple Silicon上へまとめて載せる用途にも使える。

以下の更新履歴は、これらの基盤能力のうち**統一memoryをどこまでcopyなしで使えるか、attention / GQA / MoEのHBM trafficをどこまで減らせるか、GPU occupancyをどこまで改善できるか**を中心に追う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-08-18 — v0.32.1（released）

- **CUDA RMSNormのregister pressure削減**: RMSNorm kernelが1 threadあたりに使うGPU register数を減らし、同時実行できるthread block数を増やした。registerを使いすぎるとGPU上で同時に走れる処理数が減るため、この削減はoccupancy改善につながる。B200ではtensor shapeにより **13〜52%改善**。[PR #3850](https://github.com/ml-explore/mlx/pull/3850)

- **CPU bufferのzero-copy import**: `mx.array(host_buffer, copy=False)`で、CPU側にすでにあるdataを別領域へ複製せずMLX arrayとして参照できるようにした。

  Apple Siliconの**統一memory（unified memory）**ではCPUとGPUが同じ物理memory poolを共有するため、不要なCPU→GPU copyを避けられる場合がある。zero-copyは「dataを移動せず、同じmemoryを別APIから参照する」ことを意味する。

### 2026-08-25 — v0.32.2（released）

- **GQA decodeのK/V重複load削減**: GQA（Grouped-Query Attention）では複数query headが同じK/V headを共有する。従来は同じK/V blockを複数回読む場合があったため、共有K/Vを再利用してmemory trafficを削減した。M5 Proではkernel最大 **1.27倍**、Qwen3-30B-A3Bのend-to-end decodeは最大 **約9.5%改善**。[PR #4077](https://github.com/ml-explore/mlx/pull/4077)

- **fused full-attention**: head dimension 256のattentionで、巨大なattention score tensorをVRAMへ完全生成（materialize）せず、計算途中のblockだけを保持するNAX kernelを追加。

  中間scoreを書き出して再読込するmemory trafficを減らし、M5 Maxでkernel **1.3〜2.57倍**、32K-token prefill **約27%高速化**、peak memory **34.6 → 26.5 GB**。[PR #3842](https://github.com/ml-explore/mlx/pull/3842)

- **量子化MoE matrix multiply改善**: routingされていないexpert領域までGPU SIMD groupを起動していた無駄を削除し、実際にtokenが届いたexpert tileだけ処理するよう変更。prefill **2.2〜7.0%改善**。[PR #4352](https://github.com/ml-explore/mlx/pull/4352)

### 用語メモ

- **register pressure（register圧）**: 1 threadが使うregister数が多すぎて、GPU上で同時実行できるthread数が減る状態。
- **GQA（Grouped-Query Attention）**: 複数query headでK/V headを共有し、KV cache量を減らすattention方式。
- **materialize**: 中間計算結果を実際の大きなtensorとしてmemoryへ書き出すこと。融合kernelではこれを避けることでmemory trafficを減らせる。
- **SIMD group**: 複数laneが同じ命令を並列実行するGPUの実行単位。
