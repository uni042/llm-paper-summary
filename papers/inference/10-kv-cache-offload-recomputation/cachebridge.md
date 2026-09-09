---
canonical_id: "arXiv:2609.00891"
arxiv_id: "2609.00891"
title: "CacheBridge: Efficient Cross-Model KV Cache Transfer"
summary: "同じ長い入力を別のLLMへ引き継ぐと、通常は新しいモデルが最初からprefillして自分用のKVキャッシュを作り直す必要がある。CacheBridgeは元モデルのKVから受信モデルのKVを線形変換で近似し、この再計算を避ける。各KV headを全headから予測する従来法を対応headだけへ限定し、生成品質に効く誤差をattention感度で重く学習し、変換係数の構築もGPU上で融合することで、品質を保ちながら変換器の容量・適用時間・構築時間を削減する。"
source: "https://arxiv.org/abs/2609.00891"
last_audited: "2026-09-09"
audit_version: 1
---

# CacheBridge: Efficient Cross-Model KV Cache Transfer

> 同じ長い入力を別のLLMへ引き継ぐと、通常は新しいモデルが最初からprefillして自分用のKVキャッシュを作り直す必要がある。CacheBridgeは元モデルのKVから受信モデルのKVを線形変換で近似し、この再計算を避ける。各KV headを全headから予測する従来法を対応headだけへ限定し、生成品質に効く誤差をattention感度で重く学習し、変換係数の構築もGPU上で融合することで、品質を保ちながら変換器の容量・適用時間・構築時間を削減する。

## 書誌情報

- **著者**: Xingyu Qu, Siyuan Lu, Zhiyu Chen, Sheng Wang, Tao Lin
- **所属**: Westlake University, Wuhan University, Amazon（論文記載）
- **公開**: 2026-09-01, arXiv v1
- **種別**: プレプリント（preprint）
- **主題**: モデル間KVキャッシュ転送（cross-model KV cache transfer）、LLM切替、線形写像、GQA、handoff latency
- **実装**: 論文は融合GPUカーネルを実装して評価しているが、arXiv v1および確認された著者公開ページでは公式コードリポジトリを確認できない。

## 概要

CacheBridgeを理解するには、まず「なぜ別のLLMへ会話を渡すだけで長い再計算が必要なのか」を押さえる必要がある。

LLMは入力文を最初に処理する**入力処理（prefill）**で、各トークンについて注意機構（attention）用のKeyとValueを計算し、**KVキャッシュ（KV cache）**として保存する。その後の逐次生成（decode）では、このKVを再利用するため、過去の全文を毎回モデルへ通し直さなくて済む。

しかしKVキャッシュは「入力文そのもの」ではない。各モデルの層、重み、attention headによって作られた内部表現である。したがって、例えば14Bモデルが100Kトークンの文脈をすでに処理していても、32Bモデルへ切り替えた瞬間、その32Bモデルは通常100Kトークンを最初からprefillし、自分用のKVを作り直す必要がある。

これは複数モデルを使い分けるシステムで大きな問題になる。例えば、

- 簡単な要求は小型モデル、難しい要求だけ大型モデルへ昇格する
- 安価なモデルで始め、品質が必要な部分だけ高価なモデルへ渡す
- エージェント処理の段階ごとに別モデルを使う

といった構成では、モデル切替のたびに長いprefixを再処理すると、その再計算がhandoff latencyを支配する。

そこで先行研究は、**元モデルのKVから受信モデルのKVを線形変換で予測する**方法を提案している。少量の共通テキストを両モデルへ通し、「source KV → target KV」の対応例を集めれば、追加のニューラルネットを学習せず、リッジ回帰（ridge regression）の閉形式解で変換係数を作れる。

CacheBridgeはこの基本発想を捨てずに、従来法の変換器が大きすぎ、モデルによって品質が崩れ、構築にも時間が掛かる問題を整理して改良する。

## 問題設定

### 「KVを転送する」とは、単にメモリコピーすることではない

同じモデルの別GPUへKVを移すだけなら、データをコピーすればよい。値の意味は同じだからである。

一方、別モデル間では、同じトークンについても内部のKey/Value表現が異なる。sourceモデルの第20層・head 3のKeyベクトルを、targetモデルの第20層・head 3としてそのまま使っても正しいattentionにはならない。

したがってcross-model transferでは、

```text
source modelのKV
      ↓
変換器（mapper）
      ↓
target modelが使える近似KV
```

という「表現変換」が必要になる。

### 従来のFull-Head Mappingが大きくなる理由

先行するFull-Head Mappingでは、target側の1つのKV headを予測するとき、選ばれたsource layerにある**全source KV head**を入力特徴として使う。

例えばsource側に8 KV headsあり、target head 3を予測するとする。従来法はsource head 0〜7の情報を全部連結して回帰する。

この方式は柔軟だが、問題もある。

1. 入力特徴量がhead数に比例して大きくなる。
2. 変換係数ファイルも大きくなる。
3. handoff時に実行する行列積も増える。
4. 本来対応していないhead間の偶然の相関まで学習し、別architectureでは品質が崩れる可能性がある。

評価対象のQwen3/Ministralではsource/targetとも8 KV headsなので、もし「target head 3はsource head 3だけを見れば十分」なら、特徴量を理論上8分の1へ減らせる。

## 手法のあらまし

CacheBridgeは、変換方式を3つの観点から作り直す。

第一に、**どのKV headから予測するか**を制限する。全source headを使わず、architecture上対応する1 headだけを見るHead-Localを導入する。

第二に、**どの誤差を小さくすべきか**を変える。単にKVベクトルの各座標を均等に再現するのではなく、その誤差がtargetモデルのattentionへどれだけ影響するかを使って回帰サンプルへ重みを付ける。これがAttn-Repairである。

第三に、**変換係数をどう構築するか**を最適化する。必要なsource layer/headを巨大な中間テンソルへ集めてから回帰するのではなく、GPUカーネル内で必要な統計量だけを直接蓄積するFused-Fitを使う。

オンラインhandoff時にやることは最後まで単純なaffine mappingのままである。つまり複雑なニューラルtranslatorを毎回推論する方式ではない。

## 手法

### 1. Head-Local — 対応するKV headだけから予測する

Grouped Query Attention（GQA）では、複数のquery headが少数のKV headを共有する。各KV headには、対応するquery群との役割上の対応がある。

Full-Head Mappingはtargetの1 headをsourceの全headから予測するが、CacheBridgeはこの構造を利用し、**target headごとに対応するsource head 1個だけ**を使う。

評価した3 transfer方向ではsource/targetともKV head数が8なので、head 0→0、1→1のようなidentity対応を使う。

ただしlayer方向は1対1に固定しない。target layerを予測するために複数のsource layerを使う**層間集約（cross-layer aggregation）**は残す。

つまり、

- head方向: 1つに絞る
- layer方向: 必要な複数層を組み合わせる

という設計である。

source KV head数を`H_s`とすると、非bias係数数は理論上Full-Headの`1/H_s`になる。今回`H_s=8`なので8分の1である。

この削減は単なる圧縮ではない。**GQA上で対応しないheadの情報を回帰から外すことが正則化として働き、architecture差に対してむしろ品質が改善する場合がある**というのが論文の重要な観察である。

### 2. なぜ「KVの二乗誤差が小さい」だけでは不十分なのか

通常のリッジ回帰では、target KVと予測KVの座標ごとの二乗誤差を均等に小さくする。

しかしLLMにとってすべてのKV誤差が同じ重要度ではない。

ある過去tokenを次のqueryがほとんどattentionしないなら、そのtokenのKey/Valueに多少誤差があっても生成結果へほぼ影響しない。一方、次のqueryが強く注目するtokenのKeyが少しずれると、attention scoreやsoftmaxが変わり、その後の出力へ大きく影響する可能性がある。

したがって、単純なKV再構成R²が高いmapperが、必ずしもcontinuation品質の高いmapperとは限らない。

### 3. Attn-Repair — 生成に効くKV誤差を重くfitする

Attn-Repairはtargetモデル自身のcausal attentionを観測し、**どのtoken位置のK/V誤差が将来queryへ効きやすいか**を近似する。

長さの異なるprefix境界を32点用意し、それぞれで「このprefixの直後に来る最初のfuture query」が過去KVをどう見るかを測る。

そのattention massや一次感度から、各training sampleへ重みを付けてweighted ridge regressionを行う。KとVでは影響の仕方が違うため、別々の重みを作る。

直感的には、

- 将来ほぼ見られないtoken → 誤差を多少許す
- 将来強く見られるtoken → より正確に合わせる

というfitである。

これにより「全KV座標を平均的に似せる」のではなく、**targetモデルが実際の生成で使う部分を優先して合わせる**。

### 4. 重みが一部sampleへ集中しすぎないようにする

attention感度をそのまま重みにすると、ごく少数のtokenだけが極端に大きな重みを持ち、回帰が不安定になる可能性がある。

そこでAttn-Repairは感度重みを一様重みへ少し戻す**縮小（shrinkage）**を行う。

どこまで戻すかはKishの有効標本数（effective sample size）を使って決め、回帰特徴幅に対して十分な実効サンプル数が残る範囲で、可能な限りattention感度を反映する。

ここは「attentionが大きいtokenだけで学習する」のではなく、**重要度を使いつつ回帰の数値安定性も確保する**ための仕組みである。

### 5. Mapper構築では何を計算しているのか

線形リッジ回帰の解を得るために、全観測データを最後まで保持する必要はない。

必要なのは主に、

- 入力特徴の平均
- target側の平均
- 入力同士の共分散
- 入力とtargetの交差共分散

といった**十分統計（sufficient statistics）**である。

ところがtarget layerごとに使うsource layerが違うため、素朴な実装では「必要なlayer/headだけ集める→巨大な連続テンソルへコピー→centerする→sample weightを掛ける」という一時データ生成が大量に起こる。

これがoffline mapper constructionの大きなコストになる。

### 6. Fused-Fit — 巨大な中間テンソルを作らず統計量だけ蓄積する

Fused-Fitは2-passのGPUカーネルでこの処理をまとめる。

1 pass目でweighted meanを計算する。
2 pass目で観測をbounded chunkずつ走査し、その場で必要なhead-local blockをgatherし、centerし、重み付けし、共分散・交差共分散へ蓄積する。

つまり、すべてのcalibration tokenについて巨大な`[samples × features]`テンソルを作って保持するのではなく、**小さなchunkだけを作業領域に置き、最終的に必要な行列統計へ畳み込む**。

scratch memoryは全datasetサイズではなくchunk sizeで決まる。

重要なのは、Fused-Fitが回帰の数学やオンラインmapper形式を変えていないことだ。solver、regularization、保存schema、handoff時のaffine mappingは同じで、構築経路だけを高速化する。

### 7. 実際のhandoff時の流れ

一度source-target pair用mapperを作れば、オンライン時は概ね次の流れになる。

```text
source modelがprefixをprefill済み
        ↓
source KV cacheが存在
        ↓
CacheBridge mapperを各layer/headへ適用
        ↓
target用の近似KV cacheを生成
        ↓
target modelはprefix再prefillを省略してdecode開始
```

したがって長文prefixほど、targetの再prefillを避ける価値が大きくなる。

一方、mapper適用自体にも時間が掛かるので、変換係数を8分の1にしてonline affine workを減らすことがsystem上重要になる。

## 評価

### まず見るところ

- **目的**: sourceモデルで処理済みの長文prefixをtargetモデルへ渡す際、targetの再prefillを減らす。
- **品質**: Ministral transferではFull-Head Mappingが大きく崩れる条件をHead-Local + Attn-Repairが回復する。
- **容量**: Qwen3 14B→32Bでmapper 4.296 GB→0.538 GB、約8分の1。
- **オンライン適用**: 1024-token prefixで65.12 ms→21.66 ms、最大3.0倍高速。
- **オフライン構築**: Qwen3条件で92.63 s→8.63 s、10.7倍高速。
- **重要な注意**: target KVを近似生成するため、同一モデル内のexact KV reuseと違って品質リスクはゼロではない。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### Transfer方向

- Ministral 3 3B → 14B
- Ministral 3 8B → 14B
- Qwen3 14B → 32B

すべてdense GQAで、source/targetとも8 KV heads。

calibrationはFineWeb-Eduの1024-token sequence。主要比較では500 sequence、4 tokenごとにsampleし128,000 token positionを使う。

source layerの選択数は3B→14Bで20、8B→14Bで12、Qwen3で8。ridge係数は`lambda=0.01`。

### Ministralでの品質回復

HellaSwagではFull-Head MappingからCacheBridgeへ変えると、

| Transfer | Full-Head | CacheBridge |
|---|---:|---:|
| Ministral 3B→14B | 52.2% | 72.6% |
| Ministral 8B→14B | 44.4% | 76.0% |

mean target retentionは

- 3B→14B: **65.89% → 88.23%**
- 8B→14B: **59.43% → 97.57%**

へ改善する。

この結果は「特徴量を増やすほど回帰が良い」とは限らず、architectureに沿ったhead-local制約が有効な例である。

### Qwen3では品質を維持したままmapperを小さくできる

Qwen3 14B→32BではFull-Headも比較的良好で、target retentionは99.72%。CacheBridgeは**99.83%**を維持する。

一方、serialized mapper storageは

**4.296 GB → 0.538 GB**

で約8分の1になる。

1024-token prefixへのmapper application latencyは

**65.12 ms → 21.66 ms**

で最大3.0倍高速。

### Attn-RepairはR²ではなくcontinuation品質を改善する

Qwen3でK/V reconstruction R²は概ね

**0.678 / 0.655 → 0.672 / 0.654**

と、むしろほぼ変わらない。

それでも4K prefixでのNLLは

**2.446 → 2.350**

へ改善する。

これは論文の重要な結果で、**KV座標の再構成精度と、そのKVを使った生成品質は同じ指標ではない**ことを示す。

### 少ないcalibrationでも高いretention

Qwen3では50 calibration sequencesでもCacheBridgeは**99.89% mean retention**を報告し、Full-Head Mappingを500 sequencesでfitした99.44%を上回るbudget sweep結果がある。

### Fused-Fitの構築時間

Qwen3 14B→32B、500 calibration sequences、4×NVIDIA H800で、mapper construction区間は

**92.63 s → 8.63 s**

となり**10.7倍高速**。

ただしこの数字はtrace collection、layer selection、attention weight生成、evaluation、scheduler delayを含まない。end-to-end calibration全体が10.7倍になるという意味ではない。

</details>

## 主要結果の読み方

CacheBridgeの中心的な示唆は、「より多くのsource情報を回帰へ入れればtarget KVをより良く再現できる」とは限らないことである。

GQAのarchitecture上、target headと対応関係の薄いsource headsを大量に入れると、calibration dataset上の座標誤差は下がっても、実際のcontinuationに必要な構造を壊す場合がある。

また、評価指標も重要である。R²がほぼ変わらないのにNLLやtask retentionが改善することから、KV変換では「target KVに数値的にどれだけ近いか」だけではなく、**その誤差がattentionと最終生成へどう伝播するか**を見る必要がある。

システム面では、長文prefillを省くためのmapper自体が数GBあり、適用に数十ms掛かると、handoff高速化の利点を削る。Head-Localは品質改善と同時にmapperのonline costも減らすため、algorithmとsystemの両方へ効いている。

## 品質への影響

CacheBridgeはtargetモデルの正確なKVを再計算するのではなく、source KVから近似する。

したがって同一モデル内のKV cache hitのようなlossless reuseではない。target retention、task accuracy、NLLを測る必要がある。

評価した同一family・8-head GQA条件では高いretentionを示すが、未評価architectureへそのまま適用して品質が保たれる保証はない。

## 既存研究との差

- **Full-Head Mapping / Closed-Form Linear Mapping**: cross-model KVをtraining-free ridge mappingで作れるという基本interfaceを継承し、head support・objective・構築経路を改良する。
- **学習型translator**: 小さなニューラルネットを追加学習してlatent/KVを変換する方式と異なり、closed-form affine artifactなのでonline pathが単純。ただしsource-target pairごとのmapper構築は必要。
- **LMCache / CacheFlow等**: 主に同一モデルのKVを別memory tierへ保存・復元する。CacheBridgeは**モデルが変わるとKVの意味自体が違う**問題を解く。
- **Prefill/decode分離**: 同じモデル内でKVを別nodeへ移すだけなら変換不要。CacheBridgeはモデルhandoffを跨ぐため、memory transferとは別にrepresentation conversionが必要になる。

## 限界

- 実証は同一model family内の3 transfer方向のみ。
- すべてdense GQAかつsource/targetとも8 KV headsであり、異なるhead数での対応付けは未実証。
- cross-family transfer、sliding-window/sparse attention、linear/hybrid attentionは未評価。
- mapperはdirectionalで、A→BとB→Aは別artifact。モデル数が多いとpair管理量が増える。
- handoffを何度も繰り返すagentic workflowでの誤差蓄積は十分評価されていない。
- Attn-Repairはfull receiver Jacobianではなくattention-localな一次近似で、cross-tokenやK/V間の全相互作用をモデル化しない。
- Fused-Fitの10.7倍はmapper construction部分だけで、calibration全工程のend-to-end値ではない。
- 公式コードリポジトリはarXiv v1時点で確認できない。

## 一般的な実装上の含意

複数LLMを使い分けるシステムでは、モデル切替コストを「重みの切替」だけで考えない方がよい。

長文状態を持つ場合、実際には

1. モデル重みを用意する
2. 既存prefixの状態をどうtargetへ引き継ぐか
3. KVを再計算するか、転送するか、変換するか
4. 変換artifact自体の容量と適用時間
5. 近似状態による品質低下

まで含めてhandoff costになる。

特にagent/cascadeでモデルを頻繁に切り替えるなら、KV cacheは単なるmemory objectではなく**モデル固有の実行状態**として扱う必要がある。CacheBridgeは、この状態を別モデルへ変換できれば長文再prefillを避けられる可能性を示している。

## 一次資料

- arXiv: https://arxiv.org/abs/2609.00891
- HTML: https://arxiv.org/html/2609.00891

## 更新履歴

- 2026-09-09: MoE-Infinity基準に合わせて全面改稿。cross-model KV transferの意味、Full-Headの問題、Head-Local、Attn-Repair、Fused-Fit、品質とsystem costの関係を論文未読者向けに説明。
