<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

| 論文 | 一文要約 |
|---|---|
| [Every Expert Counts: ExactMoE for Memory-Efficient W4A16 Inference](2026-2608.15383-exactmoe-memory-efficient-w4a16-inference.md) | ExactMoEは、混合専門家モデル（Mixture of エキスパート; MoE）のルータや専門家集合を削らず、ルータが選んだ全専門家をGPUで実行しながらGPUメモリ使用量を下げる推論方式である。専門家のゲート・アップ・ダウン射影だけをグループ128単位の4ビット重みに変換し、GPUカーネルがそのまま消費できるMARLIN形式で固定CPUメモリへ全専門家を保持する。実行時はGPU上の専門家スロットキャッシュに必要な専門家を圧縮形式のまま転送し、同時に必要な専門家数がスロット数を超える場合は複数波へ分けて融合MoEカーネルで実行する。OLMoE-1B-7Bでは16スロットで予約GPUメモリを87.04%削減しつつBF16の81.85%のデコード性能を維持し、全64専門家常駐時はBF16より47.4%高速だった。 |
<!-- survey:auto:end -->
