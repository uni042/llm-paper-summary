<!-- survey:auto:start -->
## 自動生成の論文一覧（9本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [Speculative Speculative Decoding](2026-2603.03251-speculative-speculative-decoding.md)**  
  実装：[✓](https://github.com/tanishqkumar/ssd) ・ リポジトリ内被引用：2  
  検証中に受理長と補正トークンを複数予測し、その各結果に続く次ラウンドのドラフトを別GPUで先行生成することで、投機的デコードに残るドラフト待ちを隠す方式。

- **2025-12 · [Speculative Decoding: Performance or Illusion?](2026-2601.11580-speculative-decoding-performance-or-illusion.md)**  
  実装：[✓](https://github.com/orgs/SpecDecode-Bench/repositories) ・ リポジトリ内被引用：1  
  実運用向けvLLMで主要投機的復号を横断評価し、検証支配・バッチ依存・受理変動と理論上限との差を定量化。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-02 · [When RL Meets Adaptive Speculative Training: A Unified Training-Serving System](2026-2602.06932-aurora-adaptive-speculator-training-serving.md)**  
  実装：[✓](https://github.com/togethercomputer/aurora) ・ リポジトリ内被引用：0  
  実配信の採用・棄却トレースからドラフトモデルを非同期更新し、停止なしで重みを差し替える閉ループ型の投機的復号により、初日配備と分布変化への継続適応を実現する。

### 2年前（2024-10〜2025-09）

- **2025-03 · [EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](2025-2503.01840-eagle-3.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：17  
  特徴回帰制約を外して直接トークン予測し、訓練時に自己生成入力を再投入することでドラフト学習のデータ規模拡大を有効化したEAGLE系投機的復号。

- **2025-05 · [SpecMemo: Speculative Decoding is in Your Pocket](2025-2506.01986-specmemo-memory-aware-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的デコードの候補木・KVキャッシュ・デコードヘッドをGPUメモリ予算に合わせて自動調整し、Titan RTXで生成メモリ65%削減・スループット96%維持、8×MI250のLlama-2-70Bでは通常分散復号比2倍を示す。

- **2025-03 · [SPIN: Accelerating Large Language Model Inference with Heterogeneous Speculative Models](2025-2503.15921-spin-heterogeneous-speculative-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求難度に応じて異種の小型下書きモデルを選択し、検証バッチのゼロ埋めを要求分解で減らし、下書き生成と標的検証を小バッチ単位で重ねて投機的デコードを高速化する。

### 4年前（2022-10〜2023-09）

- **2023-02 · [Accelerating Large Language Model Decoding with Speculative Sampling](2023-2302.01318-speculative-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：67  
  小型モデルの複数候補を大型モデルで並列検証し、出力分布を変えず700億パラメータモデルのデコードを最大約2.5倍高速化。

- **2022-11 · [Fast Inference from Transformers via Speculative Decoding](2022-2211.17192-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  軽量モデルの複数トークン提案を対象モデルで並列検証し、出力分布を変えずに直列復号回数を削減する投機的復号の基礎研究。

- **2023-09 · [Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding](2023-2309.08168-draft-verify.md)**  
  実装：[✓](https://openreview.net/attachment?id=ACC2nQYzPYS&name=software) ・ リポジトリ内被引用：10  
  元モデルの中間層を一時的に飛ばして下書きを生成し、完全モデルで一括検証することで、追加下書きモデルなしに最大約2倍の損失なしデコード高速化を実現する。
<!-- survey:auto:end -->
