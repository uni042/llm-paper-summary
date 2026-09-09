---
canonical_id: "arXiv:2609.00891"
arxiv_id: "2609.00891"
title: "CacheBridge: Efficient Cross-Model KV Cache Transfer"
summary: "モデル間KVキャッシュ転送の全head回帰をarchitecture対応headへ局所化し、attention感度重み付けとfused GPU fittingを組み合わせ、Qwen3 14B→32Bで99.83%のtarget retentionを維持しつつmapperを8分の1、適用を最大3.0×高速化する。"
source: "https://arxiv.org/abs/2609.00891"
last_audited: null
audit_version: 0
---

# CacheBridge: Efficient Cross-Model KV Cache Transfer

## 書誌情報
- **著者**: Xingyu Qu, Siyuan Lu, Zhiyu Chen, Sheng Wang, Tao Lin
- **所属**: Westlake University, Wuhan University, Amazon（論文記載）
- **公開日**: 2026-09-01
- **状態**: arXiv preprint v1
- **コード**: arXiv本文・著者公開ページから公式実装repositoryは確認できず。

## 問題設定
複数LLMをrouting、cost-quality cascade、agent pipelineなどで切り替える場合、同じprefixを引き継いでもKVキャッシュはモデル固有表現なので受信側モデルが再prefillしなければならない。長文になるほどこの再計算がhandoff latencyを支配する。

直前研究のFull-Head Mappingは、source/targetのaligned KV traceからtraining-freeなaffine ridge mapperをclosed formで作り、target側prefillを省く。しかし各target KV headを、選択したsource layer内の**全source KV head**から予測するため、(1) architecture差に弱い、(2) coordinate-wiseなKV再構成誤差と実際のcontinuation品質が一致しない、(3) mapper容量とonline affine計算量がsupport幅に比例する、(4) target layerごとに異なるtop-k source layerを使うためoffline fitting時のgather/materializationが重い、という問題がある。

## 手法
CacheBridgeはオンライン時のinterfaceをaffine mappingのまま維持しつつ、mapper support、calibration objective、construction pathの3点を同時に変える。

### Head-Local
Full-Head Mappingではtarget headごとに、選択された各source layerの全KV headをfeatureへ連結する。Head-Localは各target KV headをarchitecture metadataから決めた**対応source KV head 1個**だけに制約し、cross-layer aggregationだけを残す。評価した3方向はいずれもsource/targetが8 KV headsなので対応はidentity assignmentを使う。

source KV head数を `H_s` とすると、K/V両方の非bias係数数はfull-headに対して理論上 `1/H_s` となる。今回の評価では `H_s=8` なのでmapper係数・storageと主要affine workを8分の1へ削減する。これは単なる圧縮ではなく、GQAのquery-to-KV ownershipに沿わないcross-head相関を回帰から排除する構造的制約でもある。

### Attn-Repair
通常のridge fittingはすべてのKV coordinate誤差を同等に扱うが、実際のdecode出力への影響はreceiver側のquery・attention mass・downstream layerによって異なる。Attn-Repairはtarget modelのcausal attentionからK/V誤差の一次近似感度を求め、tokenごとのsample weightとしてridge regressionへ入れる。

KとVで別々の感度を計算し、32個の対数間隔prefix boundaryでfirst-future-queryを観測する。極端な重み集中でeffective sample sizeが崩れないよう、raw weightを一様重みへshrinkし、Kish effective sample sizeがfeature widthに応じたfloor以上になる最大係数を使う。オンライン時のmapper supportや適用コードは変わらず、変化するのはofflineで得られる係数値だけである。
## Fused-Fit
Head-Localでもtarget layerごとに選択source layer集合が異なるため、素朴な実装では非連続gather、centering、weighting用tensorのmaterializeが大量に発生する。Fused-Fitはridge solverが必要とするweighted mean、covariance、cross-covarianceという十分統計だけを構築する。

2-passの新しいGPU kernelで、最初にweighted meanを求め、2回目に観測をbounded chunkで走査する。kernel内で選択されたhead-local blockのgather・center・weightを行い、連続したper-head panelへ出力してhead-batched matrix multiplicationで統計量を蓄積する。したがってfull observation tensorを保持せず、scratch memoryはchunk sizeに対してboundedになる。ridge solver、regularization、serialized mapper schema、online affine interfaceは維持される。

## 評価条件
- **Transfer directions**:
  - Ministral 3 3B → 14B
  - Ministral 3 8B → 14B
  - Qwen3 14B → 32B
- **Attention**: すべてdense GQA、source/targetとも8 KV heads
- **Calibration**: FineWeb-Edu、長さ1,024 token。主要比較は500 sequence、4 tokenごとにsampleして128,000 token position
- **Selected source layers**: 3B→14Bで20、8B→14Bで12、Qwen3で8
- **Ridge**: `lambda=0.01`。比較法でcalibration row、layer selection、ridge strength、token sampling、evaluation exampleを固定
- **Quality**: HellaSwagを含むtask accuracy、target standaloneに対するmean target retention、NLL、KV reconstruction R²
- **System metrics**: serialized mapper storage、1,024-token prefixのmapper application latency、offline mapper construction time
- **Construction timing**: Qwen3の500-sequence構築は4×NVIDIA H800で測定。trace collection、layer selection、attention-weight生成、evaluation、scheduler delayは除外し、mapper construction部分のみを測る

## 主要結果

### Quality recovery
Full-Head Mappingは同じ8-head KV interfaceでもMinistral 3で大きく崩れる。HellaSwagでは、
- Ministral 3 3B→14B: **52.2% → 72.6%**（CacheBridge、+20.4 pt）
- Ministral 3 8B→14B: **44.4% → 76.0%**（+31.6 pt）

mean target retentionはそれぞれ **65.89% → 88.23%**、**59.43% → 97.57%**へ改善する。一方Qwen3 14B→32Bでは既存full-headも比較的良好で、CacheBridgeは**99.83%**を維持し、Full-Head Mappingの99.72%と同等以上だった。

### Mapper容量とonline cost
Qwen3 14B→32Bではserialized mapper storageを **4.296 GB → 0.538 GB**へ削減し、理論どおり約8分の1になった。1,024-token prefixでのapplication latencyは **65.12 ms → 21.66 ms**で、最大**3.0×高速**。target側re-prefillを避ける目的に対して、mapper自体のsupport幅がhandoff costを食い潰す問題を抑えている。

### Calibration効率とAttn-Repair
Qwen3では50 calibration sequencesでもCacheBridgeは**99.89% mean retention**を得て、Full-Head Mappingの500 sequencesでの99.44%を上回るbudget sweep結果を報告する。attention weightingはKV R²自体をほぼ改善しない一方、continuation retentionやlong-prefix NLLを改善しており、「coordinate reconstructionが良いこと」と「receiverの生成品質が良いこと」を分離して示している。

具体例としてQwen3でK/V R²はおおむね **0.678/0.655 → 0.672/0.654**と変わらないが、4KでのNLLは **2.446 → 2.350**へ低下した。
### Offline construction
Qwen3 14B→32B、500 calibration sequencesのmapper constructionは、generic pathの **92.63秒**からFused-Fitのmedian **8.63秒**へ短縮され、**10.7×高速**。この値はend-to-end servingではなく、十分統計生成からsolverへ渡すmapper construction経路の改善を測る。

## 既存研究との差
前身のClosed-Form Linear Mapping / Full-Head Mappingは「異なるモデル間でもKV表現に線形構造があり、training-free ridge mappingでprefill reuseが可能」という点を示した。CacheBridgeはその基本interfaceを変えず、**どのheadをfeatureへ入れるか**、**どの誤差を重視してfitするか**、**不規則supportをGPU上でどう構築するか**をsystem-levelに再設計している。

Cache-to-Cacheやlearned latent communicationのようにtranslator networkを学習する方式とは異なり、task-specificなtranslator trainingを追加せずclosed-form affine artifactを使う。そのためonline pathは軽いが、source-target pairごとにoffline mapperを構築・保持する必要は残る。

リポジトリ内のLMCache、Cake、CacheFlow等が主に**同一モデル内**でKVをmemory/storage階層へ退避・復元して再計算を避けるのに対し、CacheBridgeは**モデルを切り替えるとKV表現自体が互換でない**問題を対象とする。したがって、階層memory/offloadとcross-model conversionは競合というより補完関係にあり、変換後KVをどこへ置くか・どう転送するかは別のsystems問題として残る。

## 品質・適用範囲・限界
- 実証は**同一model family内**の3 transfer directionに限定され、すべてdense GQAかつsource/targetが8 KV headsである。
- 異なるKV-head数、cross-family transfer、sparse/sliding-window attention、linear/hybrid attentionへの一般化は未実証。
- mapperはdirectionalで、source→targetごとに別artifactが必要。多数modelを自由に切り替える環境ではpair数に応じたoffline管理costが発生する。
- 評価はhandoff直後のcontinuation品質が中心で、長いmulti-turn chainで異モデル間handoffを何度も繰り返した際の誤差蓄積は十分検証されていない。
- Attn-Repairはfull receiver Jacobianではなくattention-localな一次近似とdiagonal surrogateを使う。cross-tokenやK-V間のoff-diagonal項は捨てている。
- Fused-Fitの10.7×はmapper construction区間だけの値で、trace収集などを含むend-to-end calibration時間ではない。
- approximationされたKVを利用するため、同一modelのexact KV reuseと異なり品質riskはゼロではない。特に未評価architectureへ外挿する根拠はまだない。

## 実装状態
論文は新しいfused GPU kernelを実装して性能評価しているが、arXiv本文および確認した著者公開ページでは公式code repositoryへのリンクを確認できなかった。再現性評価ではこの点を未確認事項として扱う。

## 一次資料
- https://arxiv.org/abs/2609.00891
- https://arxiv.org/html/2609.00891
