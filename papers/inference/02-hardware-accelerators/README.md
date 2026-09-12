<!-- survey:auto:start -->
## 自動生成の論文一覧（3本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](2026-2609.10970-fengshui-chiplet-neural-accelerator-codesign.md)**  
  実装：[✓](https://github.com/CrucibleComputingGroup/fengshui) ・ リポジトリ内被引用：0  
  再利用可能な少数チップレット群そのものと演算子単位の専用アクセラレータ構成を共同探索し、計算データフロー・メモリ・並列方式・配置配線を演算子ごとに最適化してNREを抑えつつLLM推論のエネルギー効率を高める。

- **2026-07 · [FlashAccel: Leveraging High-Bandwidth Flash (HBF) for High-Throughput LLM Inference](2026-2607.10186-flashaccel-high-bandwidth-flash-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBM級帯域・大容量の高帯域フラッシュをGPUへ統合し、SRAM先読み、重み/KV専用配置、KVの選択的HBM複製、追記型永続管理を協調させて、モデル重みとKVキャッシュをフラッシュ上で直接高並列アクセスする推論アクセラレータ。

### 2年前（2024-10〜2025-09）

- **2025-01 · [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](2025-2501.01005-flashinfer-attention-engine-serving.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer) ・ リポジトリ内被引用：17  
  多様なKV配置と注意派生形をブロック疎形式と実行時コンパイルで統一し、可変系列長を固定CTAへ動的に負荷均衡しながらCUDAグラフ互換性も保つ、LLMサービング向け高性能注意エンジン。
<!-- survey:auto:end -->
