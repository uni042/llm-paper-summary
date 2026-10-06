---
canonical_id: "arXiv:2005.14187"
title: "HAT: Hardware-Aware Transformers for Efficient Natural Language Processing"
summary: "HATは異種layerと任意encoder-decoder attentionを含むSuperTransformerをweight sharingで一度学習し、実機latencyを制約にevolutionary searchしてhardwareごとのSubTransformerを選ぶ。WMT'14 En-DeのRaspberry Pi-4ではTransformer比最大3倍高速・3.7倍小型、Evolved Transformer比2.7倍高速を品質低下なしで達成する。"
list_summary: "SuperTransformerから実測ハードウェア 遅延を制約に構成を探索し、CPU・GPU・IoTごとに異なる低遅延Transformerを自動設計する。"
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
last_audited: null
audit_version: 0
---

## 概要

TransformerのFLOPsが少なくても実機遅延が短いとは限らず、同じ構成でもGPUとARM CPUでは律速が異なる。HATはこの差をneural 構成 searchへ直接組み込み、理論演算量ではなく対象ハードウェアで測った遅延を制約としてTransformerを設計する。多数候補を個別学習せず、巨大なSuperTransformerを一度重み sharingで学習し、その部分ネットワークであるSubTransformerを高速に評価する。

WMT'14 En-DeをRaspberry Pi-4で実行した代表条件では、Transformer 比較対象比最大3倍高速・3.7倍小型、Evolved Transformer比2.7倍高速・3.6倍小型を性能低下なしで達成する。Evolved Transformerに比べ探索費用は12,041分の1であり、ハードウェアごとに別構成を探す運用を現実的にする。

## 問題設定

Transformer-Bigは30-word翻訳でもRaspberry Pi上で約20秒かかる例があり、edge deploymentではモデル qualityだけでなく実遅延が制約になる。FLOPsはメモリ アクセス、演算形状、並列化を表さないため遅延 代理指標として不十分で、同FLOPsでもハードウェアにより速度が大きく異なる。

実際、HATがGPU向けに選んだモデルはTITAN Xpで147 msだがARM CPUでは6491 ms、ARM向けモデルはGPUで184 msだがARMでは6042 msとなる。同じBLEU水準でも最適構造が入れ替わるため、一つの「efficient Transformer」を全deviceへ使い回すのではなく、対象 ハードウェアを探索loopへ入れる必要がある。

## 手法

### SuperTransformerとweight sharing

encoder/decoderの層数、embedding/隠れ dimension、ヘッド数などが異なる多数のcandidateを一つのSuperTransformerへ包含する。各段階でSubTransformerを標本して共有重みを更新するため、候補ごとに最初から学習する必要がない。

探索時はcandidateが継承した重みでvalidation loss/BLEU 代理指標を測る。論文では継承重みの順位とfrom-scratch学習後の順位が概ね一致することを確認し、この代理指標で高価な候補再学習を置換する。

### heterogeneous layer

従来Transformerは各層を同じwidth/ヘッド構成で反復するが、HATでは層ごとに異なるdimensionやヘッド構成を許す。ハードウェアによって得意なmatrix 形状が違うため、均一構造より遅延 constraintへ細かく適応できる。

探索結果ではGPU向けモデルはwide/shallow、Raspberry Pi向けはdeep/thinとなる。これはGPU 遅延がembedding/隠れ dimensionへ比較的鈍感なのに対しARM CPUが強く影響される実測profileと対応する。

### arbitrary encoder-decoder attention

通常decoder 層はencoder最終層へ注意機構する。HATは各decoder 層が複数の異なるencoder 層へ接続できるようsearch spaceを広げ、浅いencoder表現も直接利用可能にする。探索モデルではdecoder 層の10%が3 encoder 層、40%が2 層へ注意機構し、この自由度が実際に選択される。

### hardware-aware evolutionary search

candidateを対象 deviceで実測して遅延 constraintを満たすものだけを残し、SuperTransformerから継承したquality 代理指標をfitnessとしてevolutionary searchする。FLOPs予測ではなく実device measurementを使うため、CPU/GPUごとのメモリ・並列化差を自然に反映する。

## 評価条件

| 項目 | 条件 |
|---|---|
| タスク | WMT'14 En-De/En-Fr、WMT'19 En-De、IWSLT'14 De-En |
| ハードウェア | Raspberry Pi-4 Cortex-A72、Intel Xeon E5-2640、NVIDIA TITAN Xp |
| 遅延測定 | 300回、最速/最遅各10%除外後に中央80%平均 |
| 系列 | WMT平均30、IWSLT平均23 トークン |
| 比較対象 | Transformer、Evolved Transformer、Lite Transformer等 |
| search | SuperTransformer + evolutionary search |

## 主要結果

| 比較 | 遅延/サイズ | 品質・条件 |
|---|---|---|
| vs Transformer | 最大3倍高速、3.7倍小型 | WMT'14、Raspberry Pi、性能低下なし |
| vs Evolved Transformer | 2.7倍高速、3.6倍小型 | search コスト 12,041分の1 |
| searched vs largest SubTransformer | 1.5倍低遅延、1.5倍小型 | BLEUはむしろ高い |
| 4-bit 量子化併用 | Transformer-Big比25倍小型 | BLEU低下は僅少 |

WMT'14 En-Deでは同じsearch family内でもRaspberry Pi向けHATがBLEU 28.15・6042 ms、GPU向けHATがBLEU 28.10・6491 msとなり、ハードウェア-specific searchの必要性を直接示す。TITAN Xpでは逆にGPU向けが147 ms、ARM向けが184 msである。

SuperTransformerの重み sharingによりEvolved Transformerのようにcandidateを個別学習せず、探索時CO2/computeを4桁削減する。さらに新ハードウェア向けcandidateは継承重みを10K 段階だけfine-tuneしても40K 段階 from-scratchと同等性能となり、再探索後の学習 コストを4分の1へ減らせる。

## 既存研究との差

Evolved Transformer等のNASは構成を自動探索するが、候補ごとの学習 コストが大きく、対象 ハードウェアの実遅延を直接目的にしない方式もある。HATはOnce-for-All型の重み sharingとハードウェア measurementを組み合わせ、同一SuperTransformerからdevice-specific モデルを切り出す。Lite Transformerのような一つの手設計efficient 構成とも異なり、ハードウェアが変わればモデル 形状自体を変える。

## 限界

評価は主に機械翻訳Transformerで、decoder-only LLMのKV キャッシュやcontinuous batchingを対象にした研究ではない。新ハードウェアごとに遅延 lookup/measurementとevolutionary searchが必要で、完全にzero-コストではない。また2020年のTITAN Xp/ARM環境で得たwide-vs-deep傾向を現代GPUへそのまま適用できない。探索自体に学習を使うため、既存チェックポイントをランタイムだけで高速化する方式でもない。

## 一次資料

- https://arxiv.org/abs/2005.14187
- https://arxiv.org/html/2005.14187v1
- https://github.com/mit-han-lab/hardware-aware-transformers