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

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

該当なし。

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2023-04 | [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md) | ✓ | 2 | MoE学習中のルーティング（routing）偏りを監視し、負荷が高いエキスパート（expert）だけを必要数複製・移動して、tokenを捨てずにGPU間の待ち時間を減らすシステム。 |
| 2025-04 | [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md) | [✓](https://github.com/NVIDIA/Megatron-LM) | 1 | attention部分とMoE部分で別々のGPU並列化構成を使い、同じGPU群を処理ごとに異なる論理グループとして組み替えることで、不要なノード間通信を減らす大規模MoE学習方式。 |

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-08 | [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md) | [✓](https://github.com/Supercomputing-System-AI-Lab/X-MoE) | 0 | expert数とTop-kが大きい新しいMoEで、空のpadding領域を通信しないtoken配置、node間の重複送信削減、MoE部分専用のsequence分割を組み合わせて大規模HPC学習を効率化する。 |
| 2025-04 | [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md) | ✓ | 0 | 動的に複製したいexpert重みと、巨大で移動コストの高いoptimizer stateの配置を切り離し、optimizer stateを動かさずにexpert複製数を毎iteration調整するMoE学習システム。 |
| 2025-04 | [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md) | ✓ | 0 | 新しいGPUへattention、旧世代GPUへexpert計算を主に割り当て、処理を重ねながらexpert数を非対称に配置して、異種GPUクラスタの待ち時間を減らすMoE学習方式。 |
<!-- survey:auto:end -->
