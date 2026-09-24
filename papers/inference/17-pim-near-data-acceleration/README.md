# PIM / Near-Data Acceleration

メモリ内処理（PIM）、メモリ近傍処理、ストレージ内処理（in-storage）、計算機能を持つHBM/NAND/DIMMなどへLLM演算を寄せ、データ移動そのものを減らす推論アクセラレーション研究をまとめる。

## 分類境界

主要貢献がPIM/CIM、near-memory、in-storage、memory-side computeによってLLM演算・検索・逆量子化・attention等をデータ近傍で実行する研究を含め、受動的なSSD/CPUへの保存・転送だけのoffloadは含めない。

### 含める研究

- HBM/DIMM/NAND上のPIM・CIM
- near-memory weight dequantization
- in-storage retrieval／memory-side attention

### 含めない研究

- 受動的なSSD/NVMe offload
- 計算機能を持たない単なる階層メモリ配置

## 近傍系統

- [01-offload-hierarchical-memory](../01-offload-hierarchical-memory/)
- [10-kv-cache-offload-recomputation](../10-kv-cache-offload-recomputation/)
- [08-edge-on-device-llm-systems](../08-edge-on-device-llm-systems/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（7本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [AMEND: Audited Margins Enable Nonblocking Drops in GPU-PIM LLM Decoding](2026-2609.09823-amend-audited-margins-enable-nonblocking-drops-in-gpu-pim-llm-decoding.md)**  
  実装：[✓](https://github.com/Miketan1/AMEND_code) ・ リポジトリ内被引用：0  
  過去ステップで監査した注意マージンから次の生存ブロックを先行予測し、GPUの生存ブロック計算と高帯域メモリ内計算による補集合監査を並列化して、キー転送と直列待ちを同時に削減する長文デコード設計。

- **2026-08 · [Rethinking Unified Memory for NPU-PIM Systems: Dual-View Memory for Dynamic Inference of LLM](2026-2608.06989-dual-view-memory-npu-pim.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NPU/PIMで共有する物理配置と各デバイスが見る論理配置を分離し、実行時の演算特性に応じて実行先を切り替えても帯域を落とさない統合メモリ方式。

- **2026-07 · [StreamDQ: Near-Memory Weight DeQuantization in Custom HBM for Scalable AI Inference Acceleration](2026-2607.08993-streamdq-near-memory-weight-dequantization-custom-hbm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBMベースダイ上で重みを読み出しながら逆量子化し、GPU側CUDA逆量子化と中間重みの余分なHBM往復を除去する近メモリ推論機構。

- **2026-07 · [D-NOVA: In-Storage Retrieval Accelerator via Dual-Bound 3D NAND-Optimized Similarity Search with Vector Adaptation](2026-2607.17538-d-nova-in-storage-retrieval-accelerator-via-dual-bound-3d-nand-optimized-similarity-search-with-vector-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAGのベクトル検索を三次元NAND配列内の二重境界検出へ変換し、候補埋め込みの外部読出しを避けてCPU比最大41.7倍高速化する。

- **2026-05 · [NASiC: 3D NAND-based CAM-Selected Multibit CIM Architecture for Efficient On-Device Mixture-of-Experts LLM Inference](2026-2605.23294-nasic-3d-nand-based-cam-selected-multibit-cim-architecture-for-efficient-on-device-mixture-of-experts-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三次元NAND内部で専門家番号の照合と選択専門家の計算を一体化し、多値記憶とブロック並列化によって専門家混合モデルを高密度に直接実行する。

- **2026-03 · [PIM-SHERPA: Software Method for On-device LLM Inference by Resolving PIM Memory Attribute and Layout Inconsistencies](2026-2603.09216-pim-sherpa-software-method-for-on-device-llm-inference-by-resolving-pim-memory-attribute-and-layout-inconsistencies.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PIM向け重みを一つだけ保持し、キャッシュ可能バッファへの実行時並べ替えで前処理と生成の属性・配置矛盾を解消してDRAM容量を約半減する。

### 2年前（2024-10〜2025-09）

- **2025-04 · [CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM](2025-2504.17584-chime-a-case-for-efficient-long-context-attention-fc-disaggregated-inference-with-dimm-pim.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  KV容量と注意帯域を同時拡張できるDIMM-PIMへデコード注意を分離し、GPU全結合層と重畳してHBM-PIM比最大5.15倍のスループットを得る。
<!-- survey:auto:end -->
