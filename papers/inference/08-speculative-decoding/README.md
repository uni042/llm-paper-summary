<!-- survey:auto:start -->
## 自動生成の論文一覧（4本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus](2026-2609.15504-orthrus-numerical-precision-losslessness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Orthrusの無損失投機的復号を独立再現し、BF16では生成軌跡の完全一致が43〜45%に留まる一方、FP32では1,190件すべて一致することを示した再現・評価研究。

- **2026-02 · [Vegas: Self-Speculative Decoding with Verification-Guided Sparse Attention](2026-2602.07223-specattn-sparse-attention-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/platformxlab/vegas) ・ リポジトリ内被引用：0  
  検証で得た注意ロジットを次の疎な候補生成へ再利用し、鍵値選択の追加走査を抑えながら損失なし自己投機復号を高速化する。

### 2年前（2024-10〜2025-09）

- **2025-09 · [Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding](2025-2509.04576-communication-efficient-distributed-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散投機的デコードの上り通信を語彙全体分布から上位K疎ロジットへ圧縮し、出力分布を維持したまま通信量と最適ドラフト長を共同最適化する。

- **2024-12 · [Dovetail: A CPU/GPU Heterogeneous Speculative Decoding for LLM inference](2024-2412.18934-dovetail-cpu-gpu-heterogeneous-speculative-decoding.md)**  
  実装：[✓](https://github.com/ddInference/Dovetail) ・ リポジトリ内被引用：1  
  ターゲットLLMをCPU、深くした小型ドラフトをGPUへ分離し、候補数削減・動的ゲート融合・複数Transformerブロックで低VRAM環境の投機的デコードを高速化する。
<!-- survey:auto:end -->
