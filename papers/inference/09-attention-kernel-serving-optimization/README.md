<!-- survey:auto:start -->
## 自動生成の論文一覧（3本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Sample-Guided Exact Top-K Selection for Long-Context Sparse Attention](2026-2609.08450-sample-guided-exact-topk-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、長文脈の疎な注意機構で使う正確なTop-K選択が、最終的にはK個しか残さないにもかかわらず、文脈長に比例するスコア行を複数回走査してしまう問題を扱う。提案法HPC-Ops Top-Kは、固定間隔で抜き出した現在行の標本から粗い上側境界を予測し、必須の全行走査で候補集合の十分性を証明すると同時に候補形成と先頭桁ヒストグラム構築を融合する。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLM推論で重みやKVキャッシュを小容量のオンチップキャッシュとHBMの間で繰り返し移動するエネルギーを、モノリシック3次元集積（Monolithic 3D; M3D）による数百MB〜GB級のオンチップメモリでどこまで減らせるかを評価する。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、LLMを処理するニューラル処理装置（Neural Processing Unit; NPU）で、チップ全体を同じ電圧・周波数にする従来の動的電圧・周波数制御（動的 Voltage and Frequency Scaling; DVFS）では、行列演算器、ベクトル演算器、SRAM、HBM、チップ間接続の利用率差を活かせない問題を扱う。

### 1年以上前

該当なし。
<!-- survey:auto:end -->
