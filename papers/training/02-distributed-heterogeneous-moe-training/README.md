# Distributed / Heterogeneous MoE Training

MoEを多数GPUへ分散して学習すると、tokenごとに使うエキスパート（expert）が変わるため、通常のdense modelより**GPUごとの仕事量が偏りやすく、expertへtokenを送るGPU間通信も大きくなりやすい**。

この系統では、

- 人気expertを必要な数だけ複製する
- expertを別GPUへ移す
- attentionとexpertで異なる並列化を使う
- 新旧GPUへ得意な処理を分担させる
- paddingや重複token通信を減らす

といった方法で、**最も遅いGPUの待ち時間、GPU間通信量、GPUメモリ使用量を減らすMoE学習研究**をまとめる。

CPUやSSDへモデルを退避することが中心の研究は `01-training-offload-memory-systems/` に分類し、ここでは主にGPU間の配置・複製・通信・並列化を扱う。

<!-- survey:auto:start -->
## 自動生成の論文一覧（5本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

該当なし。

### 2年前（2024-10〜2025-09）

- **2025-04 · [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：1  
  注意機構とMoEで異なるGPU並列化グループを組み、同じGPU集合を処理ごとに組み替えて、エキスパートの不要なノード間通信を減らす大規模学習方式。

- **2025-08 · [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/X-MoE) ・ リポジトリ内被引用：0  
  大規模MoEで実トークンだけを詰めて通信し、同一ノード宛ての重複送信をまとめ、MoE部分の系列分割も変えて、paddingとノード間通信を減らすHPC学習システム。

- **2025-04 · [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的に複製するエキスパート重みと、移動させない巨大な最適化状態を分離配置し、ルーティング負荷に応じて重みの複製数だけを毎反復調整するMoE学習システム。

- **2025-04 · [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新旧GPUの性能差に合わせて注意機構を新GPU、エキスパート計算を旧GPUへ主に割り当て、処理を重ねて異種GPUクラスタの待ち時間を減らすMoE学習方式。

### 4年前（2022-10〜2023-09）

- **2023-04 · [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MoEのルーティング偏りを監視し、負荷の高いエキスパートだけを必要なGPUへ複製・移動して、トークンを捨てずにGPU間の待ち時間を減らす学習システム。
<!-- survey:auto:end -->
