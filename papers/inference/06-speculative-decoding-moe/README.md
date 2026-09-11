# Speculative Decoding × MoE / 投機的デコード × MoE

投機的デコード、ドラフトモデル運用、および混合専門家モデル（Mixture of Experts; MoE）との組み合わせを扱う推論システム研究の系統。

<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md) | ✓ | 0 | メモリ容量が小さいエッジ端末で複数のドラフトモデルを使う適応型投機的デコードでは、精度の高いドラフトを選べても、そのモデルがメモリに常駐していなければNVMe SSDからの読み込み待ちが発生し、受理トークン数の改善が実際の生成速度へ結び付かない。 |
| 2026-01 | [WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching](2026-2601.11652-wisp-distributed-speculative-serving-edge.md) | ✓ | 0 | エッジ端末が小型ドラフトモデルで候補トークンを生成し、サーバー側の大型モデルがまとめて検証する分散投機的デコードでは、最初に棄却される位置を越えてドラフトを作る計算が無駄になり、さらにキャッシュ状態や新規トークン数が異なる要求を同じGPUバッチへ混ぜると検証時間の長い要求が他の要求まで遅らせる。 |

### 1年以上前

該当なし。
<!-- survey:auto:end -->
