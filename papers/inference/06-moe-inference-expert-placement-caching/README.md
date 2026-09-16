<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-07 · [ExpertPlex: A High-Goodput Disaggregated Serving System for MoE LLMs with Adaptive Persistent Kernels](2026-2607.18002-expertplex-disaggregated-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意計算だけを相分離し巨大MoEエキスパートを共有、タイル単位の適応型永続カーネルと注意側起動の片側通信で相間干渉を抑え、H800上でインスタンス単位P/D分離比最大2.01倍の有効スループットを達成する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [PLoRA: An NDP-Enhanced Pooled-Memory System for Cost-Efficient Multi-LoRA Serving](2026-2608.05483-plora-pooled-memory-multilora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PLoRAはLoRAアダプタとKVキャッシュをCXL級共有メモリへ置き、NDPで縮約して小さな結果だけをGPUへ返し、バッチ別戦略選択で1000超アダプタを低遅延に処理する。
<!-- survey:auto:end -->
