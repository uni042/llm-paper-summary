# Speculative Decoding × MoE / 投機的デコード × MoE

投機的デコード、ドラフトモデル運用、および混合専門家モデル（Mixture of Experts; MoE）との組み合わせを扱う推論システム研究の系統。

<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

| 論文 | 一文要約 |
|---|---|
| [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md) | メモリ容量が小さいエッジ端末で複数のドラフトモデルを使う適応型投機的デコードでは、精度の高いドラフトを選べても、そのモデルがメモリに常駐していなければNVMe SSDからの読み込み待ちが発生し、受理トークン数の改善が実際の生成速度へ結び付かない。MemSpecは、入力プロンプトと直近の生成トークンから有望なドラフトを予測し、上位候補を小さな常駐集合として先回りで管理する。実行時は常駐中で最も有望なドラフトを使い続け、より良い非常駐モデルは背景で非同期に先読みするため、モデル読み込みでデコードを止めない。Jetson Orin Nano実機で、バンディット方式の適応型比較対象より定常生成スループットを平均40.7%改善し、動的オラクルの95〜97%に達する。 |
<!-- survey:auto:end -->
