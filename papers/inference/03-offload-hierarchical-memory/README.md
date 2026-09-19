<!-- survey:auto:start -->
## 自動生成の論文一覧（3本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

該当なし。

### 2年前（2024-10〜2025-09）

- **2025-05 · [SpecOffload: Unlocking Latent GPU Capacity for LLM Inference on Resource-Constrained Devices](2025-2505.10259-specoffload-unlocking-latent-gpu-capacity-for-llm-inference.md)**  
  実装：[✓](https://github.com/MobiSense/SpecOffload-public) ・ リポジトリ内被引用：3  
  オフロード中に遊休するGPU計算時間と低効率なGPUメモリへ投機的デコードのドラフトモデルを配置し、CPU計算・重み転送・ドラフト生成を重ねてFlexGen比最大2.54倍のスループットを実現する。

- **2025-04 · [Shared Disk KV Cache Management for Efficient Multi-Instance Inference in RAG-Powered LLMs](2025-2504.11765-shared-disk-kv-cache-rag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAG文書のKVキャッシュをNVMe SSDへ永続化して複数LLMインスタンスで共有し、待ち行列時間にCPU等で先行生成することで重複プリフィルを削減する。

- **2025-04 · [Cost-Efficient LLM Serving in the Cloud: VM Selection with KV Cache Offloading](2025-2504.11816-infersave-vm-selection-kv-offloading.md)**  
  実装：[✓](https://github.com/lass-lab/InferSave) ・ リポジトリ内被引用：0  
  SLO・モデル/入出力長・GPU価格/VRAM/帯域からKVオフロード率と実効TPSを予測し、AWS上で最も安価に要件を満たすVMを自動選択する。
<!-- survey:auto:end -->
