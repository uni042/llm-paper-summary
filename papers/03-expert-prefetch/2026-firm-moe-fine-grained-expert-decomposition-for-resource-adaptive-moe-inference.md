---
title: "FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference"
summary: "expertを行列単位のsub-expertへ分解し、複数前層の合意予測と資源適応型prefetchでCPU–GPU転送量を抑えるMoE推論方式。"
authors_affiliations: "Keyu Chen, Qihang Zhou, Bin Qian, Zhenyu Wen, Wenchao Meng, Shibo He／Zhejiang University, Zhejiang University of Technology"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39106"
code: ""
last_checked: "2026-09-03"
---

# FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference

> expertを行列単位のsub-expertへ分解し、複数前層の合意予測と資源適応型prefetchでCPU–GPU転送量を抑えるMoE推論方式。

## 概要
FIRM-MoEは、expert全体を一つの不可分な転送単位とする従来のMoE offloadingが、実際に必要な計算以上のweight trafficを生む点を問題にする。Transformerのexpert FFNはgate、up、down projectionなど複数の行列から成り、選択されたexpertでも各成分の寄与や転送タイミングは一様ではない。そこでexpertを独立にロード可能なfine-grained sub-expertへ分解し、GPUメモリ容量とCPU–GPU帯域に応じて、必要な部分だけをcache／prefetch（キャッシュ／先読み）する。さらに、単一の直前層だけから予測すると外れやすく、予測数を増やすと無駄な転送が増えるという問題に対し、複数の先行層による合意を使って高信頼候補を選ぶ。システムは利用可能なVRAM、計算時間、転送コストに合わせて予測範囲とprefetch数を自動調整する。対象はCPU DRAMからGPUへのexpert weight offloadであり、KV cache offloadではない。通常のPCIe 4.0接続を用いた実機評価で、SSD／NVMe、HBF、CXLは使わない。AAAI 2026の掲載論文で、resource-constrained GPU上のMoE inferenceにおいて、予測精度だけでなく転送粒度とcache効率を同時に設計した点が重要である。
## 手法のあらまし
第一の構成要素はFine-Grained Expert Decompositionである。各expertのWgate、Wup、Wdownを独立したsub-expertとして扱い、runtimeが必要部分を別々にCPUからGPUへロードできるようにする。これにより、expert単位のprefetchで発生する過剰転送を減らし、限られたVRAMをより細かく配分できる。第二はMeeting-of-Layers（MoL）で、対象層より前のP層がそれぞれ次層のexpert候補をK個予測し、複数層で一致する高信頼候補を優先して先読みする。単一予測器のTop-kをそのまま転送する方式より、外れ候補を減らしつつ利用頻度の偏りにも耐える設計である。第三はHierarchical Expert Offloading and Prefetching（HEOP）で、浅層・中層・深層ごとにrouting特性と計算余裕が異なることを利用し、各groupのKとPを自動調整する。探索目的は未使用prefetchのコストとcache missのコストを重み付きで最小化することで、hill-climbingにより資源条件に適した設定を求める。cache residency、予測信頼度、転送可能時間をまとめて扱う一方、tokenごとにnative Top-k自体を変える手法ではなく、元routerの選択結果を満たすためのロードを細粒度化・前倒しする方式である。
## 評価
RTX 3090 24GB、32-core CPU、64GB host memory、PCIe 4.0の単一マシンで、Qwen1.5-MoE-A2.7B、Qwen3-30B-A3B、DeepSeek-MoE-16B、DeepSeek-V2-Lite、OLMoE-1B-7Bを評価し、TruthfulQAとShareGPT由来workloadを用いる。Fiddlerやllama.cppなどのbaselineに対し、平均1.31倍、最大1.5倍の速度向上と、最大2.8倍のmemory savingsを報告する。Qwen系でexpert cache容量を128に制限した条件では、基本的なprefetch方式に対して最大1.8倍となり、細粒度分解とMoLが小容量cacheで特に効くことを示す。評価はend-to-end実機であり、simulation-onlyではない。ただし速度向上はモデルのexpert構造、sub-expert転送の実装効率、層間routing相関に依存し、細粒度化によるmetadata管理や小さな転送の増加が別のhardwareで不利になる可能性がある。品質面ではnative routerと元expert計算を保持するため、置換・pruning型より原理上の劣化は小さいが、論文の中心はthroughputとmemoryで、PPLやKL divergenceを横断的にPareto評価する構成ではない。公式コードは一次資料上で確認できず、再現可能なruntime統合は未解決である。
## 引用関係
登録済みの [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](../01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)、[MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](../01-offload-hierarchical-memory/2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)、[Fast Inference of Mixture-of-Experts Language Models with Offloading](../01-offload-hierarchical-memory/2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md) などを引用し、expert単位offloadをsub-expert単位へ細粒度化する後続研究である。
## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39106)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39106/43068)

