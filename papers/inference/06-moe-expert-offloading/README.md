<!-- survey:auto:start -->
## 自動生成の論文一覧（5本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-06 · [A Spatio-Temporal Expert Prefetching Framework for Efficient MoE-based LLM Inference](2026-2606.15453-spatio-temporal-expert-prefetching.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ST-MoEは、隣接層と直前トークンのゲート相関から次層専門家を予測してオフチップDRAMから先読みし、誤り時は正しい重みを追加取得してデコードの転送待ちを減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [MoE Expert Execution in Disaggregated LLM Serving with a High-Bandwidth ReRAM Near-Memory Architecture](2026-2608.13962-reram-near-memory-disaggregated-moe-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ReXpertは、MoE専門家重みを容量比例帯域のReRAMへ常駐させ、共起する専門家を局所共有して、GPUのHBM重み読出しと小バッチFFNの供給律速を減らす。

- **2026-08 · [DynaNDE: Dynamic Near-Data Expert Scheduling for Batched MoE Inference](2026-2609.00407-dynande-near-data-expert-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DynaNDEは、専門家ごとのトークン数・演算性能・重み転送・キャッシュ再利用を遅延モデルで比較し、各層をNPU実行とNDP実行へ動的分割して転送待ちを減らす。

- **2026-08 · [APEX: Adaptive Expert Prefetching for Memory-Efficient Edge MoE Inference](2026-2608.11688-apex-adaptive-expert-prefetching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  APEXは、補助ルータの不確実性から各トークンの最小先読み候補数を決め、正確な実ルータで不足専門家を補完して、エッジMoEの外部メモリ転送待ちを削減する。

### 2年前（2024-10〜2025-09）

- **2025-09 · [DuoServe-MoE: Dual-Phase Expert Prefetch and Caching for LLM Inference QoS Assurance](2025-2509.07379-duoserve-moe-dual-phase-prefetch-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DuoServe-MoEは、密なプリフィルでは二重ストリーム転送、疎なデコードでは次層専門家をMLP予測して先読みするようフェーズ別に切替え、CPU→GPU転送待ちを隠す。
<!-- survey:auto:end -->
