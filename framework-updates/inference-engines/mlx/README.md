# MLX

MLXの主要な機能・性能更新を継続的に記録する集約ページ。Apple Silicon向けGPU kernel、統一memory（unified memory）、attention、量子化MoE、CPU↔GPU data共有など、MLX基盤そのものの性能改善を扱う。

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
