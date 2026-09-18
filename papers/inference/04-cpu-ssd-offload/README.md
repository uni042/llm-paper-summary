<!-- survey:auto:start -->
## 自動生成の論文一覧（4本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [LLM Inference in a Flash!](2026-2609.16161-llm-inference-in-a-flash.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フラッシュ内計算向けに整数のみのLLM推論と静的辞書型KV圧縮を共同設計し、品質をほぼ維持したまま動的KV転送を約15分の1へ削減する。

### 2年前（2024-10〜2025-09）

- **2025-07 · [SLIM: A Heterogeneous Accelerator for Edge Inference of Sparse Large Language Model via Adaptive Thresholding](2025-2507.09201-slim-near-storage-pim-sparse-edge-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  適応しきい値で活性FFNニューロンだけを読み、3D NAND近傍処理とDRAM内処理を統合してエッジLLMのPCIe重量転送を回避する。

### 3年前（2023-10〜2024-09）

- **2024-09 · [Cambricon-LLM: A Chiplet-Based Hybrid Architecture for On-Device Inference of 70B LLM](2024-2409.15654-cambricon-llm-chiplet-flash-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  NPUと演算機能付きNANDフラッシュをチップレット接続し、重み近傍計算とハードウェア認識タイル化で70B級の端末内推論を実現する。

- **2024-06 · [Endor: Hardware-Friendly Sparse Format for Offloaded LLM Inference](2024-2406.11674-endor-hardware-friendly-sparse-offloaded-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非構造枝刈り重みを非ゼロ値と位置ビットマップへ分離し、CPU/SSDからGPUへの転送量を減らして、退避LLM推論を最大約2.37倍高速化する。
<!-- survey:auto:end -->
