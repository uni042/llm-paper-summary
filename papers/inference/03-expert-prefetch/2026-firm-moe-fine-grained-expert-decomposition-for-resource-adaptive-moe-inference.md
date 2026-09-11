---
canonical_id: AAAI:39106
arxiv_id: null
doi: 10.1609/aaai.v40i24.39106
openreview_id: null
arxiv_categories:
  primary: null
  cross_list: []
last_audited: '2026-09-10'
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: 'FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference'
summary: expert weightを複数の小さな行列単位へ分け、複数の前layerが共通して必要と予測したexpert部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。
authors_affiliations: Keyu Chen, Qihang Zhou, Bin Qian, Zhenyu Wen, Wenchao Meng, Shibo He／Zhejiang University, Zhejiang University of Technology
published: '2026-03-14'
publication_status: Published
lineage: Expert Prefetch
topics:
- CPU offload
- Expert cache
- Expert prefetch
- Quality-cost
importance: 高
hardware_evaluation: 実機
source: https://ojs.aaai.org/index.php/AAAI/article/view/39106
code: null
implementation: 公式コード公開の記載はAAAI掲載ページで確認できず
last_checked: '2026-09-11'
authors:
- Keyu Chen
- Qihang Zhou
- Bin Qian
- Zhenyu Wen
- Wenchao Meng
- Shibo He
publication: Proceedings of the AAAI Conference on Artificial Intelligence
publication_type: conference paper
sources:
- https://ojs.aaai.org/index.php/AAAI/article/view/39106
implementation_status: official-code-not-confirmed
references:
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: arXiv:2308.12066
- canonical_id: arXiv:2308.15030
- canonical_id: arXiv:2402.07033
- canonical_id: arXiv:2104.07857
- canonical_id: arXiv:2312.17238
references_checked_at: '2026-09-11'
references_source: primary-pdf-reference-section
references_total: 1
---

# FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference

> エキスパート 重みを複数の小さな行列単位へ分け、複数の前層が共通して必要と予測したエキスパート部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。

## 概要

FIRM-MoEは、通常のエキスパート オフロードが**エキスパート全体を一つの転送単位として扱うため、必要のない重みまでまとめて運びやすい**点を問題にする。

要するに、必要な部分だけを細かく運び、複数の予測が一致した時だけ先読みを強めることで、限られたメモリと転送帯域を無駄なく使う。

MoE エキスパート FFNはgate / up / down projectionなど複数重み matrixから構成される。FIRM-MoEはこれらを独立に読み込み可能な小単位へ分け、限られたVRAMへ必要部分だけをキャッシュ / 先読みする。

さらに、単一前層からのpredictionはミスが多く、候補を増やすだけでは無駄転送が増える。そこで**複数の前層が同じエキスパートを必要と予測した時に、そのエキスパートを高信頼とみなして優先する**。

最後に、層ごとのルーティング特性とhardware 資源を見て、何層前から予測するか・何エキスパート分を先読みするかを自動調整する。

元の ルータ / Top-k / エキスパート計算は維持するため、エキスパート substitution型ではなく無損失寄りのsystem optimizationである。

## 手法

### 1. Expertをprojection単位へ分ける

各エキスパートを、

- `W_gate`
- `W_up`
- `W_down`

などのprojection単位へ分け、それぞれ独立した小さな重み単位として管理する。

エキスパート丸ごと読み込みする方式よりGPU キャッシュ容量を細かく使え、不要な重み 転送を減らせる。

細粒度化の利点は、予測が部分的に当たった場合にも転送済みbyteを無駄にしにくいことにある。エキスパート全体を一単位にすると一部projectionだけ先に必要でも全重みを運ぶが、分解後は実行順や残りメモリに合わせて必要部分から配置できる。ただし単位を小さくしすぎるとmetadataとDMA発行回数が増えるため、分解粒度自体にもhardware依存の最適点がある。

### 2. 小さいweight単位でcache / prefetchする

GPU VRAMにはエキスパート全体ではなく、必要なprojectionを個別に置ける。

キャッシュ ミスでもエキスパート全体を移す必要がなく、必要な重み部分だけをCPU DRAMから送る。

この性質はVRAMが数エキスパート分しか空いていない状況で特に効く。丸ごとキャッシュでは空き容量より少し大きいエキスパートを全く置けないが、projection単位なら一部だけ常駐にして残りを後続計算と重ねて送れる。その結果、capacity制約を『何エキスパート置けるか』という離散問題から『何byteのsub-エキスパートを先に置くか』という連続に近い配分問題へ細かくできる。

### 3. 複数前layerの予測が一致したexpertを優先する

対象層より前の複数層が、それぞれ次エキスパート候補を予測する。

複数層で同じエキスパートが候補に現れた場合、そのエキスパートは将来実際に必要になる可能性が高いとみなし、先読み 優先度を上げる。

論文ではこの仕組みを`Meeting-of-Layers (MoL)`と呼ぶ。単一予測器の候補を全部先読みするより、**複数予測の合意で候補を絞り、誤予測転送を減らす**のが目的である。

### 4. Prediction数を増やしすぎない

先読み候補を増やせば本当に必要なエキスパートを含める割合は上がるが、使わない重み 転送も増える。

MoLは単純にcandidateの和集合を広げるのではなく、複数層で一致した候補を優先してこのtrade-offを抑える。

### 5. Layerごとに予測距離と先読み数を変える

浅層・中層・深層でルーティングの予測しやすさと、次層までに使える計算時間が異なるため、全層へ同じ設定を使わない。

論文の`HEOP`は層 groupごとに、

- 何層前から予測するか
- 何エキスパート候補を先読みするか
- GPU キャッシュへどれだけ容量を割くか

を変える仕組みである。

この層別設定により、予測しやすい層では先読みを厚くし、相関の弱い層では候補を絞るという使い分けができる。

### 6. VRAM・転送時間に合う設定を探索する

GPU メモリ容量、エキスパートを送る時間、キャッシュ ミスした時の待ち時間をコストとして、予測距離や先読み数の候補を少しずつ変えながら速い設定を探す。

GPU メモリが小さい環境では重みを細かく保持する利点を重視し、PCIe帯域に余裕があれば先読みを増やす、といった適応を行う。

同じモデルでも最適な予測距離はdeviceによって変わる。遠い層を早く予測すれば転送時間は長く確保できるが、ルーティング相関が弱まり誤先読みも増える。近い層だけなら予測は当たりやすいが転送を隠す時間が不足する。HEOPはこの精度-versus-lookaheadのtrade-offをVRAMとPCIeの実測コストへ結びつけ、固定の『n 層 ahead』設定を全deviceへ押し付けない。

この探索により、同じモデルでも端末のメモリ容量や転送速度に応じて先読みの粒度を変えられる。細分化の利得は常に一定ではなく、分割管理の負担と実際の転送時間を合わせて判断する。

実測で得た転送時間を設定探索へ戻すことで、静的な予測距離では扱えない端末差も反映できる。

## 評価

### まず見るところ
- **結論:** エキスパートをprojection単位へ細分化し、複数前層の予測が一致したものを優先して先読みすると、小キャッシュほど無駄転送を減らしやすい。
- **速度:** 比較対象比平均約1.31×、最大約1.5×。厳しいキャッシュ条件では先読み 比較対象比最大約1.8×。
- **メモリ:** 最大約2.8×のメモリ savingを報告。
- **品質:** 元の ルータと元エキスパート計算を維持するため無損失寄り。
- **注意点:** 重みを細かく分け過ぎると、管理情報や小さいDMA 転送の回数が増えて不利になる可能性がある。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 実機環境

| 項目 | 設定 |
|---|---|
| GPU | RTX 3090 24GB |
| CPU | 32-core |
| ホスト メモリ | 64GB |
| PCIe | Gen4 |

### Models

- Qwen1.5-MoE-A2.7B
- Qwen3-30B-A3B
- DeepSeek-MoE-16B
- DeepSeek-V2-Lite
- OLMoE-1B-7B

TruthfulQAとShareGPT系ワークロードを使用。

### End-to-end speed

Fiddler / llama.cppなどに対し、

- 平均：約1.31×
- 最大：約1.5×

の高速化倍率。

### 厳しいcache条件

Qwen系でエキスパート キャッシュ容量を128に制限した条件では、基本先読み方式比で最大約1.8×。

キャッシュが小さいほどエキスパート丸ごと転送の無駄が相対的に大きくなり、重み分割の利点が増える。

### Memory savings

最大約2.8×のメモリ savingを報告する。

これはエキスパート数を枝刈りするのではなく、**GPUへ置く重み単位を細かくして必要部分だけ保持する**ことで得る。

### 各要素の役割

性能向上は主に、

1. エキスパート 重みを小単位へ分解する
2. 複数前層の予測合意で誤先読みを減らす
3. 層ごとに予測距離・先読み量を調整する

の組み合わせで出る。

### 制約

- 小重み単位ごとの管理情報が増える。
- small DMA 転送が多すぎるhardwareでは効率低下の可能性。
- ルーティング correlationが弱いモデルでは複数層合意の利得が縮む。
- SSD/NVMe未評価。
- 公式 codeは一次資料で確認できない。

</details>

## 一次資料
- [AAAI公式ページ](https://ojs.aaai.org/index.php/AAAI/article/view/39106)
- [AAAI公式PDF](https://ojs.aaai.org/index.php/AAAI/article/view/39106/43068)

## 更新履歴
- 2026-09-04: fine-grained decomposition / MoL / HEOPを分離し、キャッシュ制約下の速度・メモリ評価を表形式へ整理。
- 2026-09-07: sub-エキスパート / MoL / HEOP / objective 検索等を、重み分割・予測合意・資源調整として平易化。
