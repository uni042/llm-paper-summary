---
title: "CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices"
summary: "学習済み予測器と過去routing patternの検索器をcascadeし、promptから全層のexpertを先読みして資源制約下のMoE推論を高速化する。"
authors_affiliations: "Chengcheng Wang, Haowen He, Liang Zhao, Xiaoheng Deng, Lixin Duan, Shaohua Wan／UESTC, Shenyang Aerospace University, Central South University"
published: "2026-03-14"
publication_status: "Published"
lineage: "Expert prefetch"
topics: ["CPU offload","Expert cache","Expert prefetch","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://ojs.aaai.org/index.php/AAAI/article/view/39816"
code: ""
last_checked: "2026-09-03"
---

# CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices

> 学習済み予測器と過去routing patternの検索器をcascadeし、promptから全層のexpertを先読みして資源制約下のMoE推論を高速化する。

## 概要
CasMoEは、メモリの小さいconsumer／edge deviceでMoEを動かす際、expertのcache missとCPU–GPU weight transferがdecode遅延を支配する問題を扱う。既存の予測型prefetchは、モデルごとに学習したpredictorの推論コストが無視できない一方、単純な履歴照合だけでは未知入力やrouting変化へ弱い。CasMoEは、parametricなExpert Activation Predictor（EAP）とnon-parametricなExpert Activation Matcher（EAM）をcascade（段階接続）し、入力に応じて安価な検索と学習済み予測を使い分ける。promptを一度解析して全MoE layerのexpert activationを先に推定するため、layerごとに予測器を呼び出すoverheadと転送開始の遅れを抑える。過去と類似したrouting patternならdatabase検索を使い、未知性が高い入力では学習型predictorへ切り替える設計である。対象はexpert weightのCPU–GPU offload／prefetchで、KV cache offloadではない。通常のhost memoryとGPUを想定し、SSD／NVMe、HBF、CXL固有のI/O mechanismは扱わない。AAAI 2026掲載で、既存のMoE-Infinity、Fiddler、DAOP、ProMoE、SiDA-MoE、FineMoEを引用し、予測方式を二者択一ではなくcascadeとして統合した後続研究に位置付けられる。
## 手法のあらまし
EAPは軽量encoderと複数のprediction headからなり、prompt表現から各層で活性化されるexpert集合を一括予測する。学習ではcontrastive learningを用いて、routing patternが近い入力を表現空間でも近づけ、異なるpatternを分離する。これにより単純なmulti-label classificationより入力意味とexpert activationの対応を捉えやすくする。EAMは過去のprompt表現と全層activation patternを格納したdatabaseを検索し、十分近い既知patternがあれば学習済みEAPを実行せず、そのpatternをprefetch計画として再利用する。cascade gateはretrieval confidenceや入力の難しさを基にEAMで確定するかEAPへ送るかを選ぶ。得られた全層のexpert候補を早い段階からCPU→GPUへ非同期転送し、native routerが実際に選ぶ前にcacheを暖める。元モデルのrouterやTop-kは変更せず、予測はresource allocationにのみ用いるため、推論意味論を直接書き換えるexpert substitutionではない。一方、適応粒度は主にprompt／sequenceとlayerであり、各decode tokenのcache状態を見て必要native miss数Kを変える方式ではない。固定の層別候補数とcascade選択により、予測コストとcache hit率を均衡させる。
## 評価

### まず見るところ
- **結論:** 類似promptはrouting履歴検索、未知promptは学習型predictorへ回すcascadeで、予測コストを抑えながら全層のprefetchを早く始められる。
- **速度・効率:** on-demandより大きくthroughputを改善するが、効果はrouting-pattern databaseがworkloadをどれだけ覆うかに依存する。
- **品質:** native router/Top-kは変更せず、予測はprefetch用なので原理上は**lossless型**。ただし報告は平均task performance保持率中心。
- **メモリ・I/O:** CPU DRAM→GPUのexpert weight prefetch。SSD/NVMeは対象外。
- **評価の強さ／注意点:** **実機runtimeあり**。database構築範囲、類似度threshold、workload driftに敏感で、公式コードは確認できない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

論文は複数のMoEモデルとresource-constrained device条件で、on-demand loading、cache型、学習型prefetch型を比較する。主要結果として、on-demand baselineに対してthroughputを65.13%改善しながら、元モデルのtask performanceを96.6%以上保持したと報告する。EAMを利用できる既知・類似promptでは予測器の計算を省けるため、EAP単独よりprefetch開始が早く、全層予測によって深い層の転送を前倒しできる。未知入力ではEAPへfallbackするため、履歴検索だけの方式よりactivation recallを維持しやすい。評価は実機runtimeを含み、純粋なtrace-driven simulationのみではないが、報告値はprompt分布、pattern databaseの構築範囲、類似度thresholdに依存する。databaseが大きくなると検索memoryと更新コストが増え、workload driftが強い場合にはEAMの利点が薄れる。また、品質保持率は平均benchmark scoreであり、長いgenerationにおける誤予測のtail behaviorやPCIe bytes/tokenの詳細なPareto frontierは十分ではない。公式コードは一次資料から確認できず、database構築、predictor training、runtime連携まで含めた再現性は今後の課題である。

</details>

## 引用関係
登録済みの [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](../01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md)、[ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](../02-adaptive-computation-cache-aware-moe/2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)、[Fast Inference of Mixture-of-Experts Language Models with Offloading](../01-offload-hierarchical-memory/2023-2312.17238-fast-inference-of-mixture-of-experts-language-models-with-offloading.md) などの系譜を引き、予測と履歴照合をcascadeする。
## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39816)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39816/43777)

