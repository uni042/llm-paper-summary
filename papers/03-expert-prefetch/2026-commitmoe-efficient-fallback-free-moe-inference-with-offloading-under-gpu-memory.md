---
title: "CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints"
summary: "次層expertを先読みし、予測が外れても追加ロードへ戻らず予測expertを確定実行することで、MoE重みオフロードの待ち時間を除く手法。"
authors_affiliations: "Han Li, Jingwei Sun, Junqing Lin, Guangzhong Sun／University of Science and Technology of China"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert prefetch","Expert substitution","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39454"
code: ""
last_checked: "2026-09-03"
---

# CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints

> 次層expertを先読みし、予測が外れても追加ロードへ戻らず予測expertを確定実行することで、MoE重みオフロードの待ち時間を除く手法。

## 概要
CommitMoEは、GPUメモリに全expert重みを保持できないMixture-of-Experts（MoE）推論で、CPU DRAMからGPUへ行うweight offload（重みオフロード）の転送待ちを削減する研究である。従来のexpert prefetch（専門家の先読み）は、次層で使うexpertを予測して転送を開始する一方、予測が外れるとnative router（元モデルのルーター）が選んだexpertを改めてロードするfallbackを必要とする。この追加ロードがクリティカルパスに残るため、予測精度が十分高くても高速化が頭打ちになる。CommitMoEは発想を反転し、予測したexpertを「候補」ではなく実行対象としてcommitし、誤予測時にもon-demand loadingへ戻らない。著者らはrouter分布の確信度を一様分布とのKL divergenceで測り、確信度が低く予測しにくいtokenほどexpert置換に対する出力感度も低いという経験的性質を示す。これを根拠に、予測が完全一致しない場合でも品質を保ちやすい領域でfallbackを省く。対象はexpert weightのCPU–GPU転送であり、KV cache offloadではない。通常のPCIe接続CPUメモリを用い、SSD／NVMe、HBF、CXLは評価対象外である。AAAI 2026掲載論文で、MoE-Infinityを土台とした実機runtime評価まで含む。
## 手法のあらまし
中核はCommit RouterとOutput-Weight Adjustment（OWA）である。Commit Routerは現在のtoken状態から次のMoE layerで選択されるexpertを予測する軽量MLPで、同一tokenの隣接層相関を使う1層MLP版と、cross-token情報も扱う2層MLP版を検討する。元モデルと予測器は分離され、native routerは凍結したまま、教師router分布とのKL divergenceを最小化する蒸留で予測器だけを学習する。推論時は予測結果に基づき次層expertを非同期にCPUからGPUへ転送し、native routerの確定を待たずに準備する。次層到達後、予測集合とnative Top-kが一致すれば通常のrouter重みで実行し、一部だけ一致した場合はOWAがnative routerの確率質量を実際に常駐・先読み済みのexpertへ再配分する。完全不一致でも追加のcache-miss expertをロードせず、準備済みexpertを使うため転送待ちが復活しない。実装はPyTorchとMoE-Infinityを拡張し、expert transferとGPU計算を別CUDA streamで重ねる。これは「高精度な予測を目指すだけ」のprefetchではなく、router certaintyとsubstitution toleranceの相関を利用して、予測ミス処理そのものを排除する設計である。代償として出力は厳密には元モデルと同一でなく、品質保証は統計的評価に依存する。
## 評価
Qwen1.5-MoE-Chat、DeepSeek-V2-Lite-Chat、Mixtral-8x7B-Instructを、RTX 4090＋Xeon W5-3435X（PCIe 4.0 x16）およびRTX 2080 Ti＋Xeon E5-2680 v4（PCIe 3.0 x16）で評価している。MoE-Infinityを含むoffloading baselineに対し、end-to-end推論を1.3〜9.4倍高速化しながら、複数の言語理解・推論ベンチマークで元モデルに近い品質を維持した。特に、予測expertがnative Top-kと一つも一致しないケースを置換しても、QwenのGSM8Kは53.22から54.51、BBHは36.67から36.75、DeepSeekでは69.59から69.74、49.12から49.16となり、低確信度tokenでの置換が必ずしも品質低下につながらないという観察を支える。ただし、この結果は平均的なtask scoreであり、個々のtoken出力の一致やworst-case品質を保証しない。速度向上幅はPCIe世代、cache容量、モデルのrouting予測可能性に大きく依存する。評価は実機で、trace-driven simulationのみではないが、SSD読出し量、energy/token、長文での累積誤差は主要指標として扱われていない。コード公開は論文一次資料から確認できず、再現性と他runtimeへの移植コストは今後の課題である。
## 引用関係
登録済みの [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](../01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)、[MoE-Lightning: High-Throughput MoE Inference with CPU-GPU-I/O Pipelining](../01-offload-hierarchical-memory/2024-2411.11217-moe-lightning-high-throughput-moe-inference-with-cpu-gpu-i-o-pipelining.md)、[Fast Inference of Mixture-of-Experts Language Models with Offloading](../01-offload-hierarchical-memory/2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md) などを参考文献に含み、MoE-Infinity上で実装・比較している。
## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39454)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39454/43415)

