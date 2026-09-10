# Speculative Decoding × MoE / 投機的デコード × MoE

投機的デコード、ドラフトモデル運用、および混合専門家モデル（Mixture of Experts; MoE）との組み合わせを扱う推論システム研究の系統。

<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

| 論文 | 一文要約 |
|---|---|
| [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md) | メモリ容量が小さいエッジ端末で複数のドラフトモデルを使う適応型投機的デコードでは、精度の高いドラフトを選べても、そのモデルがメモリに常駐していなければNVMe SSDからの読み込み待ちが発生し、受理トークン数の改善が実際の生成速度へ結び付かない。MemSpecは、入力プロンプトと直近の生成トークンから有望なドラフトを予測し、上位候補を小さな常駐集合として先回りで管理する。実行時は常駐中で最も有望なドラフトを使い続け、より良い非常駐モデルは背景で非同期に先読みするため、モデル読み込みでデコードを止めない。Jetson Orin Nano実機で、バンディット方式の適応型比較対象より定常生成スループットを平均40.7%改善し、動的オラクルの95〜97%に達する。 |
| [WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching](2026-2601.11652-wisp-distributed-speculative-serving-edge.md) | エッジ端末が小型ドラフトモデルで候補トークンを生成し、サーバー側の大型モデルがまとめて検証する分散投機的デコードでは、最初に棄却される位置を越えてドラフトを作る計算が無駄になり、さらにキャッシュ状態や新規トークン数が異なる要求を同じGPUバッチへ混ぜると検証時間の長い要求が他の要求まで遅らせる。WISPは、エッジ側で軽量な棄却予測器を使って棄却直前にドラフトを打ち切り、サーバー側では残りのサービス品質目標（Service-Level Objective; SLO）余裕と予測検証時間から緊急度と有効処理量密度を計算してバッチを組む。A100 80GB上のQwen3-32B評価では全体有効スループット631.86トークン/秒を示し、中央集約型の326.12、SLEDの170.82を上回る。 |
<!-- survey:auto:end -->
