<!-- survey:auto:start -->
## 自動生成の論文一覧（4本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-03 · [TriMoE: Augmenting GPU with AMX-Enabled CPU and DIMM-NDP for High-Throughput MoE Inference via Offloading](2026-2603.01058-trimoe-gpu-cpu-ndp-offloading.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高・中・低頻度専門家をGPU・行列演算CPU・DIMM近傍処理へ三分し、予測付き再配置で単一GPUのMoEオフロードを高速化する。

### 2年前（2024-10〜2025-09）

- **2025-05 · [FloE: On-the-Fly MoE Inference on Memory-constrained GPU](2025-2505.05950-floe-on-the-fly-moe-inference.md)**  
  実装：[✓](https://github.com/zju-stu-lizheng/FloE) ・ リポジトリ内被引用：2  
  専門家内部の不要チャネルを予測して転送対象を削り、次層の専門家を先読みすることで、小容量GPU上のMoE推論を高速化する。

- **2025-03 · [Accelerating MoE Model Inference with Expert Sharding](2025-2503.08467-moe-expert-sharding.md)**  
  実装：[✓](https://github.com/sacs-epfl/moe-inference) ・ リポジトリ内被引用：0  
  全エキスパートを全GPUへテンソル分割してルーティング偏りを計算負荷偏りから切り離し、カーネル融合でMoEエンコーダ推論を高速化する。

- **2024-10 · [Optimizing Mixture-of-Experts Inference Time Combining Model Deployment and Communication Scheduling](2024-2410.17043-aurora-moe-deployment-communication-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEのエキスパート配置・異種GPU割当・全対全通信順序を共同最適化し、4クラスタ条件を理論化して異種同居では二部マッチング近似を用い、最大3.54倍高速化する。
<!-- survey:auto:end -->
