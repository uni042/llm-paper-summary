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
