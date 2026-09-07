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

## 収録論文

収録論文: 5本。公開日が新しい順。

- 2025-08-18 — [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)
  - expert数とTop-kが大きいMoEで、空のpadding領域を通信せず、同じnode宛ての重複token送信もまとめる。MoE部分だけsequence配置を変え、AMDを含む大規模HPCで通信量と活性値メモリを減らす。
- 2025-04-28 — [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)
  - expert重みは人気度に応じてGPU上で動かす一方、巨大な最適化状態（optimizer state）はhost側へ固定する。expertを複製・再配置してもoptimizer stateまで毎回移さずに済む。
- 2025-04-21 — [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)
  - attention部分とMoE部分で別々のGPU並列グループを使い、同じGPU集合を処理ごとに異なる論理構成へ組み替える。MoEの全対全通信を高速なnode内接続へ閉じ込めやすくする。
- 2025-04-04 — [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)
  - 新しいGPUへattention、旧世代GPUへexpert計算を主に割り当てる。両方を同時進行させ、expert数もGPU性能に応じて非対称に配置して待ち時間を減らす。
- 2023-04-08 — [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)
  - routingでtokenが集中したhot expertだけを別GPUへ複製・移動し、元のroutingを変えずに複製間へtokenを分散する。token dropなしで特定GPUへの負荷集中を緩和する。
