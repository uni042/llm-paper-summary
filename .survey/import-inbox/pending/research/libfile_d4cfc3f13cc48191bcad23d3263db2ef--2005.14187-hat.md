---
canonical_id: "arXiv:2005.14187"
title: "HAT: Hardware-Aware Transformers for Efficient Natural Language Processing"
summary: "HATは異種layerと任意encoder-decoder attentionを含むSuperTransformerをweight sharingで一度学習し、実機latencyを制約にevolutionary searchしてhardwareごとのSubTransformerを選ぶ。WMT'14 En-DeのRaspberry Pi-4ではTransformer比最大3倍高速・3.7倍小型、Evolved Transformer比2.7倍高速を品質低下なしで達成する。"
list_summary: "SuperTransformerから実測hardware latencyを制約にarchitectureを探索し、CPU・GPU・IoTごとに異なる低遅延Transformerを自動設計する。"
authors: ["Hanrui Wang","Zhanghao Wu","Zhijian Liu","Han Cai","Ligeng Zhu","Chuang Gan","Song Han"]
published: "2020-05-28"
publication: "Annual Meeting of the Association for Computational Linguistics (ACL 2020)"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2005.14187"
sources: ["https://arxiv.org/abs/2005.14187","https://arxiv.org/html/2005.14187v1"]
implementation: "SuperTransformerとhardware-aware evolutionary searchを実装し、Raspberry Pi-4 ARM、Intel Xeon、NVIDIA TITAN Xp上で4翻訳taskの実測latencyとBLEUを評価。公式コード公開。"
code: "https://github.com/mit-han-lab/hardware-aware-transformers"
last_checked: "2026-10-06"
arxiv_id: "2005.14187"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.LG","cs.NE"]
worker_completed_at: "2026-10-06T08:36:00+09:00"
worker_run_key: "20261006-0800-scheduled-chat-00/r02"
reference_main_sha: "4537b47af2c2241e12a0fb074c518f87230c70a2"
---

## 概要

TransformerのFLOPsが少なくても実機latencyが短いとは限らず、同じarchitectureでもGPUとARM CPUでは律速が異なる。HATはこの差をneural architecture searchへ直接組み込み、理論演算量ではなく対象hardwareで測ったlatencyを制約としてTransformerを設計する。多数候補を個別学習せず、巨大なSuperTransformerを一度weight sharingで学習し、その部分networkであるSubTransformerを高速に評価する。

WMT'14 En-DeをRaspberry Pi-4で実行した代表条件では、Transformer baseline比最大3倍高速・3.7倍小型、Evolved Transformer比2.7倍高速・3.6倍小型を性能低下なしで達成する。Evolved Transformerに比べ探索費用は12,041分の1であり、hardwareごとに別architectureを探す運用を現実的にする。

## 問題設定

Transformer-Bigは30-word翻訳でもRaspberry Pi上で約20秒かかる例があり、edge deploymentではmodel qualityだけでなく実latencyが制約になる。FLOPsはmemory access、演算shape、parallelismを表さないためlatency proxyとして不十分で、同FLOPsでもhardwareにより速度が大きく異なる。

実際、HATがGPU向けに選んだmodelはTITAN Xpで147 msだがARM CPUでは6491 ms、ARM向けmodelはGPUで184 msだがARMでは6042 msとなる。同じBLEU水準でも最適構造が入れ替わるため、一つの「efficient Transformer」を全deviceへ使い回すのではなく、target hardwareを探索loopへ入れる必要がある。

## 手法

### SuperTransformerとweight sharing

encoder/decoderのlayer数、embedding/hidden dimension、head数などが異なる多数のcandidateを一つのSuperTransformerへ包含する。各stepでSubTransformerをsampleして共有weightを更新するため、候補ごとに最初からtrainingする必要がない。

探索時はcandidateが継承したweightでvalidation loss/BLEU proxyを測る。論文では継承weightの順位とfrom-scratch学習後の順位が概ね一致することを確認し、このproxyで高価な候補再学習を置換する。

### heterogeneous layer

従来Transformerは各layerを同じwidth/head構成で反復するが、HATではlayerごとに異なるdimensionやhead構成を許す。hardwareによって得意なmatrix shapeが違うため、均一構造よりlatency constraintへ細かく適応できる。

探索結果ではGPU向けmodelはwide/shallow、Raspberry Pi向けはdeep/thinとなる。これはGPU latencyがembedding/hidden dimensionへ比較的鈍感なのに対しARM CPUが強く影響される実測profileと対応する。

### arbitrary encoder-decoder attention

通常decoder layerはencoder最終layerへattentionする。HATは各decoder layerが複数の異なるencoder layerへ接続できるようsearch spaceを広げ、浅いencoder表現も直接利用可能にする。探索modelではdecoder layerの10%が3 encoder layer、40%が2 layerへattentionし、この自由度が実際に選択される。

### hardware-aware evolutionary search

candidateをtarget deviceで実測してlatency constraintを満たすものだけを残し、SuperTransformerから継承したquality proxyをfitnessとしてevolutionary searchする。FLOPs予測ではなく実device measurementを使うため、CPU/GPUごとのmemory・parallelism差を自然に反映する。

## 評価条件

| 項目 | 条件 |
|---|---|
| task | WMT'14 En-De/En-Fr、WMT'19 En-De、IWSLT'14 De-En |
| hardware | Raspberry Pi-4 Cortex-A72、Intel Xeon E5-2640、NVIDIA TITAN Xp |
| latency測定 | 300回、最速/最遅各10%除外後に中央80%平均 |
| sequence | WMT平均30、IWSLT平均23 token |
| baseline | Transformer、Evolved Transformer、Lite Transformer等 |
| search | SuperTransformer + evolutionary search |

## 主要結果

| 比較 | latency/size | 品質・条件 |
|---|---|---|
| vs Transformer | 最大3倍高速、3.7倍小型 | WMT'14、Raspberry Pi、性能低下なし |
| vs Evolved Transformer | 2.7倍高速、3.6倍小型 | search cost 12,041分の1 |
| searched vs largest SubTransformer | 1.5倍低latency、1.5倍小型 | BLEUはむしろ高い |
| 4-bit quantization併用 | Transformer-Big比25倍小型 | BLEU低下は僅少 |

WMT'14 En-Deでは同じsearch family内でもRaspberry Pi向けHATがBLEU 28.15・6042 ms、GPU向けHATがBLEU 28.10・6491 msとなり、hardware-specific searchの必要性を直接示す。TITAN Xpでは逆にGPU向けが147 ms、ARM向けが184 msである。

SuperTransformerのweight sharingによりEvolved Transformerのようにcandidateを個別trainingせず、探索時CO2/computeを4桁削減する。さらに新hardware向けcandidateは継承weightを10K stepだけfine-tuneしても40K step from-scratchと同等性能となり、再探索後のtraining costを4分の1へ減らせる。

## 既存研究との差

Evolved Transformer等のNASはarchitectureを自動探索するが、候補ごとのtraining costが大きく、target hardwareの実latencyを直接目的にしない方式もある。HATはOnce-for-All型のweight sharingとhardware measurementを組み合わせ、同一SuperTransformerからdevice-specific modelを切り出す。Lite Transformerのような一つの手設計efficient architectureとも異なり、hardwareが変わればmodel shape自体を変える。

## 限界

評価は主に機械翻訳Transformerで、decoder-only LLMのKV cacheやcontinuous batchingを対象にした研究ではない。新hardwareごとにlatency lookup/measurementとevolutionary searchが必要で、完全にzero-costではない。また2020年のTITAN Xp/ARM環境で得たwide-vs-deep傾向を現代GPUへそのまま適用できない。探索自体にtrainingを使うため、既存checkpointをruntimeだけで高速化する方式でもない。

## 一次資料

- https://arxiv.org/abs/2005.14187
- https://arxiv.org/html/2005.14187v1
- https://github.com/mit-han-lab/hardware-aware-transformers