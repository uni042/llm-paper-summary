<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-07 · [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](2026-2607.05147-dspark-confidence-scheduled-speculative-decoding.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSpec) ・ リポジトリ内被引用：4  
  並列ドラフトの後半受理率低下を軽量な逐次ヘッドで抑え、較正した接頭辞生存確率と実機処理能力から検証長を負荷適応で配分し、実トラフィックで同等処理能力時のユーザー当たり生成速度を57〜85%改善する。

- **2026-06 · [DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding](2026-2606.02091-dflare.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：3  
  ブロック拡散ドラフトの各層へ異なる標的層混合を注入し、ドラフト深さ・標的知識・学習データを拡張して受理長と実時間高速化を伸ばす。

- **2026-05 · [ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios](2026-2604.09603-echo.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  高同時実行時の投機的デコードを固定検証予算の配分問題として扱い、信頼度の高い深さだけで候補木を伸縮し、バッチ内要求間で予算を再配分するSGLang統合方式。

- **2026-05 · [D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting](2026-2605.18810-d-pace.md)**  
  実装：[✓](https://github.com/Lucas-TY/D-PACE) ・ リポジトリ内被引用：3  
  並列投機ドラフタで、受理接頭辞長への位置別寄与から交差エントロピー重みを毎例動的に計算し、固定位置減衰より受理長と実測高速化を改善する。

- **2026-07 · [AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding](2026-2607.25852-angelspec.md)**  
  実装：[✓](https://github.com/Tencent/AngelSpec) ・ リポジトリ内被引用：2  
  会話には短い多トークン予測、コード・数学には並列草稿DFlyを使い分け、実行時負荷に応じて検証深度も動的調整する推測デコード基盤。

- **2026-05 · [Draft-OPD: On-Policy Distillation for Speculative Draft Models](2026-2605.29343-draft-opd.md)**  
  実装：[✓](https://github.com/haodilei/Draft-OPD) ・ リポジトリ内被引用：2  
  投機的復号の検証で露出したドラフト誤り位置から提案を再生し、教師分布でオンポリシー蒸留することで受理長と無損失推論速度を高める。

- **2026-08 · [S2-MoE: Enabling Efficient Self-Speculative Decoding for Mixture-of-Experts on Edge Devices](2026-2608.15018-s2-moe-self-speculative-decoding-edge.md)**  
  実装：[✓](https://github.com/angerybob/S2-MoE) ・ リポジトリ内被引用：1  
  エッジ向けMoEで、専門家再利用を考慮した投機展開・ゲーティング・文脈共有を組み合わせ、専門家読み出しを抑えながら自己投機的復号を高速化する。

- **2026-02 · [SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding](2026-2604.09557-speed-bench-speculative-decoding-benchmark.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号を意味多様性・入力長・エントロピー・並列度の軸で統一評価し、合成入力の平均23%過大評価やバッチ依存の最適ドラフト長など、従来ベンチマークの順位偏りを明らかにする。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers](2026-2609.17184-loopspec-pipelined-self-speculative-looped-transformers.md)**  
  実装：[✓](https://github.com/kaist-flexml-lab/loopspec) ・ リポジトリ内被引用：0  
  ループ型Transformerの中間再帰状態を投機提案に使い、未来ドラフトと現在検証をパイプライン化して最大6.83倍高速化する。

- **2026-09 · [DFlow: Enabling Verifier Information Flow in Block Diffusion Speculative Decoding](2026-2609.06498-dflow-verifier-information-flow-block-diffusion.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却された後続位置の対象モデル中間表現を次の投機生成回へ再利用し、対象モデルの追加計算なしでブロック拡散型投機的復号の平均受理長を約10〜13%改善する。

- **2026-09 · [Carryover Drafting: Recycling Rejected States for Speculative Decoding](2026-2609.14717-carryover-drafting-recycling-rejected-states.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却されたターゲット隠れ状態を次回ドラフトの一時KV文脈へ再利用し、追加投影器なしで受理長を6.5〜14.7%改善する。

- **2026-07 · [AdaptiveSD A Stability-Aware, Runtime-Adaptive Speculative Decoding Framework with Multi-Policy Orchestration for CPU-Constrained LLM Inference](2026-2607.03876-adaptivesd-runtime-adaptive-cpu-constrained.md)**  
  実装：[✓](https://github.com/sadrasa97/adaptive-speculate-decoding) ・ リポジトリ内被引用：0  
  CPU資源・受理率・遅延・KV圧力を監視し、投機深度を閉ループ制御して資源飽和と遅延変動を抑える適応投機デコード。

- **2026-04 · [NanoSpec: Accelerating Speculative Decoding using Minimalist In-Context Vocabularies](2026-2605.26444-microspec-lightweight-in-context-vocabularies.md)**  
  実装：[✓](https://github.com/csAugust/NanoSpec) ・ リポジトリ内被引用：0  
  文脈と直近候補から毎ステップ3000未満の動的ドラフト語彙を作り、必要なLMヘッド重みを非同期収集して射影計算を削減する投機的デコード最適化。EAGLE-2のドラフト時間を平均51.6%削減する。

- **2026-04 · [FASER: Fine-Grained Phase Management for Speculative Decoding in Dynamic LLM Serving](2026-2604.20503-faser-fine-grained-phase-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的負荷下の投機的デコードを、リクエスト別投機長、検証途中の棄却枝刈り、ドラフトと検証のフロンティア単位重畳で細粒度化し、vLLM上で最大53%のスループット向上と最大1.92倍の遅延改善を示す。
<!-- survey:auto:end -->
