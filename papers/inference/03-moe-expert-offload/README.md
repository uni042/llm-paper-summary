<!-- survey:auto:start -->
## 自動生成の論文一覧（4本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-04 · [SpecMoE: A Fast and Efficient Mixture-of-Experts Inference via Self-Assisted Speculative Decoding](2026-2604.10152-specmoe-self-assisted-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  MoE自身の常駐層と少数ホットエキスパートをドラフト化し、投機検証でエキスパート転送を集約してCPU/SSDオフロードMoEの通信量と推論時間を削減する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-05 · [Fast MoE Inference via Predictive Prefetching and Expert Replication](2026-2605.11537-predictive-prefetching-expert-replication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  次バッチの人気専門家をSRUで予測し、需要に比例して専門家をGPU上へ複製してトークン待ちを並列化するMoE推論方式。

- **2026-01 · [Making MoE-based LLM Inference Resilient with TARRAGON](2026-2601.01310-tarragon-resilient-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意側とエキスパート側を別故障領域に分け、動的エキスパート経路、増分KVチェックポイント、影エキスパートで故障ワーカーだけを自己修復し、MoE推論の全体再起動を避ける。

### 2年前（2024-10〜2025-09）

- **2025-06 · [HarMoEny: Efficient Multi-GPU Inference of MoE Models](2025-2506.12417-harmoeny-efficient-multi-gpu-moe-inference.md)**  
  実装：[✓](https://github.com/sacs-epfl/HarMoEny) ・ リポジトリ内被引用：3  
  MoEの動的な専門家人気偏りに対し、トークンを空きGPUへ再配置し必要な専門家重みを非同期先読みして同期待ちを削減する。
<!-- survey:auto:end -->
