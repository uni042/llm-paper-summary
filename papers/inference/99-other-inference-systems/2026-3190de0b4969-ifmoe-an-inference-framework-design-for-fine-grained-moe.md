---
canonical_id: mlforsystems-neurips2024-paper41
title: 'IFMoE: An Inference Framework Design for Fine-grained MoE'
summary: 細粒度MoE推論では、従来の専門家並列が注意層・正規化・共有専門家など非専門家パラメータを各GPUへ複製してKVキャッシュ容量を圧迫し、専門家数が多いほどGroupedGEMMもメモリ帯域律速になる。IFMoEは共有部分をテンソル並列、ルーティング専門家を専門家並列に分ける混成配置で重複を減らし、空いたメモリを大バッチと長文脈へ回す。さらに同じMoEモデルの活性専門家数を減らした近似モデルを草稿生成器として使い、10トークンごとに完全専門家設定で再符号化してKVキャッシュを修整する。Qwen2-57B-A14B-InstructをA6000×4、Deepseek-Lite-ChatをA6000×2で評価し、推論速度と処理量を30%以上改善する一方、近似方式のため一部課題で品質低下を残す。
list_summary: 共有部分をテンソル並列化して細粒度MoEの重複メモリを減らし、少数専門家で草稿生成した後に完全専門家設定でKVキャッシュを修整して復号を高速化する。
authors:
- Yuwei An
- Zhuoming Chen
- Beidi Chen
published: '2024-12-15'
publication: Machine Learning for Systems Workshop at NeurIPS 2024
publication_type: workshop paper
publication_status: published workshop paper
topics:
- fine-grained MoE
- エキスパート parallelism
- tensor parallelism
- speculative デコード
- KV キャッシュ
hardware_evaluation: Qwen2-57B-A14B-InstructはNVIDIA A6000を4基、Deepseek-Lite-ChatはA6000を2基使用。最大バッチはそれぞれ256と200。
quality_effect: 草稿トークンをすべて受理する近似方式で完全同値ではない。XSumとIFEvalはほぼ同等だが、GSM8KはDeepseek-Liteで67.7→63.8、Qwen2で75.4→71.1へ低下する。
references:
- canonical_id: arXiv:2110.14168
  arxiv_id: '2110.14168'
- canonical_id: arXiv:2302.01318
  arxiv_id: '2302.01318'
references_checked_at: '2026-09-16T06:20:00Z'
references_source: primary PDF references section
references_total: 19
source: https://mlforsystems.org/assets/papers/neurips2024/paper41.pdf
sources:
- https://mlforsystems.org/assets/papers/neurips2024/paper41.pdf
implementation: 論文はCutlass版GroupedGEMMを利用したIFMoE試作と実機評価を記載するが、公開コードURLは本文で確認できない。
last_checked: '2026-09-16'
code: null
last_audited: null
audit_version: 0
---

# IFMoE: An Inference Framework Design for Fine-grained MoE

## 概要
IFMoEは、細粒度Mixture-of-Experts（MoE）モデルの推論で生じるメモリ重複とexpert計算遅延を同時に狙う推論フレームワークである。従来のExpert Parallelism（EP）はexpert以外のパラメータを各GPUへ複製するため、細粒度MoEでexpert数が増えるほど、モデル本体よりもKV cacheや大きなbatchへ回したいVRAMを圧迫する。IFMoEはこの配置を分解し、attentionやshared expertなど共有部分へTensor Parallelism（TP）、routed expertへEPを適用することで、非expert部分の重複を減らす。

第二の狙いはGroupedGEMMの遅延である。細粒度MoEではtokenが複数expertへ分散されるため、expert fusion kernelが細かな行列積を多数処理し、実測ではexpert数増加に伴ってGPU計算資源利用率が下がる。IFMoEは同じモデルのactive expert数だけを減らした近似版をdraft modelとして用いる。draft側で10 tokenを生成した後、完全なexpert数へ戻してcontextを再符号化し、KV cacheを補正する。通常のspeculative decodingのようなreject/resampleではなく、近似draftをそのまま受け入れるため完全同値ではない。

## 問題設定
細粒度MoEでは、expertを細分化して専門化を進めるほど推論時の実装効率が下がりやすい。IFMoEが対象とする主なボトルネックは二つある。

第一に、従来EPではrouted expertだけでなくattention、normalization、shared expert等の非expert部分もGPUごとに複製される。学習では通信回避との交換条件として合理的でも、推論ではこの重複VRAMがKV cacheやbatch sizeを制限し、長文脈・高throughputで不利になる。

第二に、expert layerで使うGroupedGEMMは、active expert数が多く各expertへ入るtoken数が小さくなると、十分な演算密度を得にくい。論文は細粒度MoEのexpert融合処理が推論遅延へ大きく寄与すると観察し、単純なkernel最適化以外の方法でexpert計算量そのものを減らす。

## 手法
IFMoEの配置方式は、共有パラメータとrouted expertを別のparallelismで扱う。attention・normalization・shared expert等はTensor Parallelismで分割し、routed expertはExpert ParallelismでGPU間へ配置する。これにより、EPだけで全モデルを配置する場合より非expertパラメータの重複を削減する。削減されたVRAMはKV cacheやより大きなbatchへ再配分できる。

推論計算では、元モデルと同じ重みを使いつつ、各tokenでactiveにするexpert数だけを減らしたdraft設定を作る。draft設定で一定数のtokenを生成し、その後に完全expert設定で既生成contextを再符号化してKV cacheを更新する。論文の主要設定では10 tokenごとに完全設定へ戻る。draft tokenを検証して棄却する通常のspeculative decodingとは異なり、近似tokenを受理するため、速度向上と品質の交換が存在する。

## 評価
評価モデルはQwen2-57B-A14B-InstructとDeepseek-Lite-Chat。Qwen2はNVIDIA A6000を4基、Deepseek-LiteはA6000を2基用いる。論文はbatch size、sequence length、active expert数等を変え、従来EP配置とIFMoEの混成配置、およびdraft expert削減を比較する。Qwen2では最大batch 256、Deepseek-Liteでは最大batch 200まで評価している。

品質評価にはXSum、IFEval、GSM8Kを用いる。近似draftを受理するため完全な出力同値性は保証されないが、XSumとIFEvalでは大きな差が出にくい。一方GSM8KではDeepseek-Liteが67.7から63.8、Qwen2が75.4から71.1へ低下し、推論品質への影響が確認される。

## 結果
論文は、混成TP+EP配置により非expert部分の重複を削減し、より大きなbatchとKV cacheを確保できることを示す。さらにdraft側でactive expert数を減らすことでexpert layerのGroupedGEMM負荷を抑え、完全expert設定による周期的な再符号化を組み合わせる。

主要な結論は、対象構成で推論latencyとthroughputを30%以上改善できるというもの。ただしこれは完全同値な最適化ではなく、特に推論・算術タスクでは品質低下が残る。したがってIFMoEの価値は、同一品質を絶対条件とするservingではなく、多少の近似を許容してメモリ容量とthroughputを引き上げたい環境で大きい。

## 既存研究との差
従来のMoE serving最適化はexpert offload、expert placement、通信削減、kernel fusion、load balancingなどを中心に扱う。IFMoEは、細粒度MoEに特有の「非expert重複」と「active expert数増加によるGroupedGEMM効率低下」を同時に扱う点が異なる。

また、通常のspeculative decodingが小型draft modelとtarget modelの出力一致を検証し、reject時にtarget側へ戻るのに対し、IFMoEは同一MoEモデル内でactive expert数を変えることで近似draftを作る。tokenを棄却せず周期的にKV cacheを修整するため実装上は軽いが、その代わり品質保証を失う。

## 限界
最大の制約は近似性である。draft tokenをtarget設定で逐次検証しないため、完全な生成同値性はなく、GSM8Kのような誤差が蓄積しやすい課題では品質低下が観測される。また、評価GPUはA6000に限られ、H100/H200等の新しいGPUや高速interconnectで同じボトルネック比率になるかは未確認である。

さらに、効果は対象MoEの共有パラメータ比率、active expert数、expert粒度、batch size、sequence lengthに依存する。expert計算が十分に大きくGroupedGEMM効率が高いモデルや、非expert重複が支配的でない構成では利得が小さくなる可能性がある。
