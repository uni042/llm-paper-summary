# Pipeline-Native CPU Inference

CPU向け単一トークン推論で、Transformerの層間依存構造、重み配置、実行スケジュールを共同設計する研究を収録する。標準モデルのまま行う量子化やカーネル高速化とは異なり、推論時のデータ移動順序を変えるためにモデル構造そのものを設計する研究を扱う。

## 収録論文

- [Pipeline-Native Transformers: Co-Designing Model Architecture and CPU Inference for Bandwidth-Efficient Autoregressive Decode](2026-2608.23841-pipeline-native-transformers.md) — 層間依存を緩めたモデルとCPUタイル型ストリーミングランタイムを共同設計する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [Pipeline-Native Transformers: Co-Designing Model Architecture and CPU Inference for Bandwidth-Efficient Autoregressive Decode](2026-2608.23841-pipeline-native-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  毎トークン、実際に使う重みを読み込むため、実行順と配置はメモリ帯域を左右する。本論文は、汎用Transformerを実行するランタイムだけを最適化する従来の分離設計を見直し、層間依存関係を変更したモデル構造とCPU推論ランタイムを一緒に設計する独立研究報告である。
<!-- survey:auto:end -->
