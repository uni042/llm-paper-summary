<!-- survey:auto:start -->
## 自動生成の論文一覧（5本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Sample-Guided Exact Top-K Selection for Long-Context Sparse Attention](2026-2609.08450-sample-guided-exact-topk-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HPC-Ops Top-Kは、標本で上位候補境界を予測し、全行の一回走査で十分性を証明、足りない時だけ回復して正確なK個を選び、長文疎注意の再走査を減らす。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMETは、LLMのタイル配置とメモリ階層転送を回路レベルのSRAM・M3D特性へ接続し、L2容量を増やす利益とアクセス費が釣り合う省エネ設計点を探索する。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

### 4年前（2022-10〜2023-09）

- **2023-07 · [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](2023-2307.08691-flashattention-2.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：60  
  初代FlashAttentionのオンライン・ソフトマックスとタイル分割を保ちつつ、行列積以外の演算とブロック・ワープ間の仕事分割を再設計し、A100で理論演算性能の最大73%と初代比約2倍の高速化を達成する。

### 5年前（2021-10〜2022-09）

- **2022-05 · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](2022-2205.14135-flashattention.md)**  
  実装：[✓](https://github.com/HazyResearch/flash-attention) ・ リポジトリ内被引用：40  
  タイル化、オンラインsoftmax、逆伝播時再計算により二次元注意行列の高帯域メモリ往復を避ける厳密注意カーネル。
<!-- survey:auto:end -->
