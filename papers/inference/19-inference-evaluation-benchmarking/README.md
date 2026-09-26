<!-- survey:auto:start -->
## 自動生成の論文一覧（4本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [Diagnose Before You Compress: Prediction-Independent Bottleneck Witness Refinement for LLM Serving Traces](2026-2608.00423-bottleneck-preserving-witnessing.md)**  
  実装：[✓](https://github.com/llmllmllm/BPW) ・ リポジトリ内被引用：0  
  スケジューリング・入力処理・生成・KVキャッシュの各ボトルネックを実機測定で独立確認し、四要素すべてに複数の証拠を残す小さなLLMサービング再生用トレースを選ぶ。

- **2026-06 · [Benchmarking LLM Serving Systems for Agentic AI Workloads with XPerf](2026-2608.20370-xperf-benchmarking-llm-serving-agentic-ai-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント実行を呼出し依存グラフとして記録・再生し、8種類の実アプリでサービング負荷とハードウェア指標を再現可能に測る評価基盤を提示する。

- **2026-04 · [Reasoning Language Model Inference Serving Unveiled: An Empirical Study](2025-2510.18672-reasoning-language-model-inference-serving-unveiled.md)**  
  実装：[✓](https://github.com/lqinfdim/RLMServing) ・ リポジトリ内被引用：0  
  推論大規模言語モデルは通常の言語モデルと異なり、キャッシュ使用量が大きく変動し、少数の遅い要求が処理全体を引き延ばす。著者らは評価枠組みASUとベンチマークASU-Perfを導入し、複数のサービング最適化がモデル規模や負荷によって効いたり逆効果になったりすることを、実機評価と到着負荷の再現で示す。

- **2026-04 · [Comparative Characterization of KV Cache Management Strategies for LLM Inference](2026-2604.05012-comparative-characterization-kv-cache-management-strategies-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLM、H2O、InfiniGenをH100実機で比較し、GPUメモリを最大約70%減らすH2O、初期事実を保ちやすいInfiniGen、速度に優れるvLLMの条件別の使い分けを明らかにする。
<!-- survey:auto:end -->
