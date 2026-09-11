<!-- survey:auto:start -->
## 自動生成の論文一覧（5本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-06 | [A Spatio-Temporal Expert Prefetching Framework for Efficient MoE-based LLM Inference](2026-2606.15453-spatio-temporal-expert-prefetching.md) | ✓ | 1 | 混合専門家モデル（Mixture of エキスパート; MoE）のデコードでは、各トークンのゲート結果が出るまで必要なエキスパートが確定せず、巨大なエキスパート重みをオフチップDRAMから都度読み込む待ち時間が性能を制限する。ST-MoEは、隣接MoE層の選択結果と直前トークンの選択結果に強い相関があることを利用し。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [MoE Expert Execution in Disaggregated LLM Serving with a High-Bandwidth ReRAM Near-Memory Architecture](2026-2608.13962-reram-near-memory-disaggregated-moe-execution.md) | ✓ | 0 | 注意機構とフィードフォワード網（FFN）を別のハードウェア群へ分離するLLMサービングで、MoE専門家重みをReRAM近傍メモリへ常駐させ、対話型デコードの小さいバッチでも高い重み読出し帯域密度を確保するReXpertを提案する。単に重み転送を消すだけでは、専門家ルーティングの偏りで高頻度専門家が律速し。 |
| 2026-08 | [DynaNDE: Dynamic Near-Data Expert Scheduling for Batched MoE Inference](2026-2609.00407-dynande-near-data-expert-scheduling.md) | ✓ | 0 | MoE型LLMでは、巨大なエキスパート重みをNPUメモリへすべて保持できないため、選択されたエキスパートを外部メモリから転送する処理が大きな待ち時間を生む。処理近傍計算（Near-Data Processing; NDP）を使えば重みの近くでエキスパート計算を実行できるが、既存のMoNDEはPCIe帯域とNDP帯域の比に基づく固定的な割り当てであり。 |
| 2026-08 | [APEX: Adaptive Expert Prefetching for Memory-Efficient Edge MoE Inference](2026-2608.11688-apex-adaptive-expert-prefetching.md) | ✓ | 0 | エッジ環境の混合専門家モデル（Mixture of エキスパート; MoE）では、大量のエキスパート重みを高速なパッケージ内メモリへ常駐させにくく、低価格な外部メモリから必要な重みを都度転送する待ち時間がデコード性能を制限する。APEXは各MoE層の注意計算より前に補助ルータを置き。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-09 | [DuoServe-MoE: Dual-Phase Expert Prefetch and Caching for LLM Inference QoS Assurance](2025-2509.07379-duoserve-moe-dual-phase-prefetch-cache.md) | ✓ | 1 | DuoServe-MoEは、混合専門家モデル（Mixture of エキスパート; MoE）のプリフィルとデコードでエキスパート活性化密度が異なる点を利用し、単一GPU・CPUオフロード環境でフェーズ別に転送方式を切り替える推論サービングシステムである。プリフィルでは多数トークンのため実質的に多くのエキスパートが使われるので予測せず。 |
<!-- survey:auto:end -->
